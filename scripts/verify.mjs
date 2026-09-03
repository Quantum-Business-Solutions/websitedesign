#!/usr/bin/env node
/**
 * /verify — the launch gate, as a command.
 *
 * Roadmap item 2. Every check here is already written down as a manual step in
 * process/checklist.md, process/launch-standards.md or process/structured-data.md.
 * Discipline fails under deadline, and deadlines are when it matters, so the
 * checks run themselves.
 *
 *   node scripts/verify.mjs <url> [more urls...] [--out verify-out] [--expect-org "Name"]
 *
 * Exit code 0 = all gates pass, 1 = at least one FAIL. Wire it into CI or run it
 * before a client sees anything.
 */
import { chromium } from 'playwright';
import { readFileSync, mkdirSync, writeFileSync, readdirSync, existsSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import { createRequire } from 'node:module';
import path from 'node:path';

const require = createRequire(import.meta.url);
const AXE = readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8');

const WIDTHS = [
  { name: 'mobile', width: 390, height: 844 },
  { name: 'tablet', width: 768, height: 1024 },
  { name: 'desktop', width: 1440, height: 900 },
];

// Lorem, unfilled tokens, and the tells that a template shipped unedited.
const PLACEHOLDER = [
  /\blorem ipsum\b/i, /\bdolor sit amet\b/i, /\bTODO\b/, /\bFIXME\b/,
  /\bexample\.com\b/i, /\byour company\b/i, /\bcompany name here\b/i,
  /\{\{\s*\w+/, /\blogo here\b/i, /\bplaceholder\b/i, /\bComing soon\b/i,
];

/**
 * Curl-backed request transport.
 *
 * Some sandboxes route outbound HTTPS through a policy proxy that accepts curl but
 * rejects Chromium's TLS handshake outright (connection reset, whatever flags you
 * pass). Rather than give up on the harness there, we intercept every browser request
 * and satisfy it with curl, which inherits the environment's proxy and CA config.
 *
 * Trade-off, stated honestly: subresources still load and render, so screenshots and
 * axe-core are fully valid. Network TIMING is not, so LCP is reported as unavailable
 * rather than as a fake number. Use PageSpeed Insights for real field timing --
 * process/launch-standards.md says so anyway.
 */
function curlFetch(url, method = 'GET') {
  const hdr = '/tmp/.verify-hdr';
  const r = spawnSync('curl', [
    '-sS', '-L', '--max-redirs', '8', '--max-time', '45',
    '-X', method, '-D', hdr, '-o', '-', '--write-out', '%{content_type}', url,
  ], { encoding: 'buffer', maxBuffer: 64 * 1024 * 1024 });
  if (r.status !== 0) return null;
  const out = r.stdout || Buffer.alloc(0);
  let head = '';
  try { head = readFileSync(hdr, 'utf8'); } catch {}
  const blocks = head.trim().split(/\r?\n\r?\n/);
  const last = blocks[blocks.length - 1] || '';
  const lines = last.split(/\r?\n/);
  const status = parseInt((lines[0] || '').split(' ')[1], 10) || 200;
  const headers = {};
  for (const l of lines.slice(1)) {
    const i = l.indexOf(':');
    if (i > 0) {
      const k = l.slice(0, i).trim().toLowerCase();
      // strip hop-by-hop and encoding headers -- curl already decoded the body
      if (['content-encoding', 'content-length', 'transfer-encoding',
           'connection', 'strict-transport-security'].includes(k)) continue;
      headers[k] = l.slice(i + 1).trim();
    }
  }
  // trailing content_type from --write-out
  const ctMatch = out.toString('latin1').match(/([a-z]+\/[a-z0-9.+-]+(?:;[^\n]*)?)$/i);
  let body = out;
  if (ctMatch && !headers['content-type']) headers['content-type'] = ctMatch[1];
  if (ctMatch) body = out.subarray(0, out.length - ctMatch[1].length);
  return { status, headers, body };
}

let USE_CURL = false;

async function installTransport(ctx) {
  if (!USE_CURL) return;
  await ctx.route('**/*', async route => {
    const req = route.request();
    const res = curlFetch(req.url(), req.method() === 'HEAD' ? 'HEAD' : 'GET');
    if (!res) return route.abort();
    await route.fulfill({ status: res.status, headers: res.headers, body: res.body });
  });
}

const args = process.argv.slice(2);
const urls = args.filter(a => !a.startsWith('--'));
const flag = n => { const i = args.indexOf(`--${n}`); return i === -1 ? null : args[i + 1]; };
const OUT = flag('out') || 'verify-out';
const EXPECT_ORG = flag('expect-org');

if (!urls.length) {
  console.error('usage: node scripts/verify.mjs <url> [...] [--out DIR] [--expect-org "Client Name"]');
  process.exit(2);
}

const results = [];
const rec = (url, gate, status, detail) => results.push({ url, gate, status, detail });

function findChromium() {
  // The npm playwright build and the pre-installed browsers can disagree on revision.
  // Prefer whatever is actually on disk over whatever playwright wants to download.
  const root = process.env.PLAYWRIGHT_BROWSERS_PATH || '/opt/pw-browsers';
  const candidates = [];
  try {
    for (const d of readdirSync(root)) {
      if (!d.startsWith('chromium')) continue;
      for (const rel of ['chrome-linux/chrome', 'chrome-linux/headless_shell',
                         'chrome-linux64/chrome', 'chrome-mac/Chromium.app/Contents/MacOS/Chromium']) {
        const p = path.join(root, d, rel);
        if (existsSync(p)) candidates.push(p);
      }
    }
  } catch { /* no browsers dir — fall through to playwright's own resolution */ }
  // full chromium before headless_shell: we need a real browser for CWV and axe
  candidates.sort((a, b) => (a.includes('headless_shell') ? 1 : 0) - (b.includes('headless_shell') ? 1 : 0));
  return candidates[0] || null;
}

async function launch() {
  // Old headless was removed; --headless=new via args is the reliable path here.
  const opts = {
    headless: false,
    args: ['--headless=new', '--no-sandbox', '--disable-dev-shm-usage'],
  };
  const exe = findChromium();
  if (exe) opts.executablePath = exe;

  // Sandboxed environments route outbound HTTPS through a local MITM proxy.
  // Chromium won't pick it up from the environment, so pass it explicitly, and
  // trust that proxy's CA rather than turning verification off.
  const proxy = process.env.HTTPS_PROXY || process.env.https_proxy;
  if (proxy) {
    opts.proxy = { server: proxy, bypass: (process.env.NO_PROXY || '').split(',').join(',') };
    const ca = process.env.NODE_EXTRA_CA_CERTS || '/root/.ccr/ca-bundle.crt';
    if (existsSync(ca)) {
      // Chromium has no CA-file flag; --use-system-ca makes it read the OS store,
      // where the proxy CA is installed. Scoped to the proxy case only.
      opts.args.push('--use-system-ca');
    }
  }
  try {
    return await chromium.launch(opts);
  } catch (e) {
    if (!exe) throw e;
    console.error(`chromium at ${exe} failed to launch, retrying with playwright's own`);
    delete opts.executablePath;
    return chromium.launch(opts);
  }
}

async function auditPage(browser, url) {
  const slug = url.replace(/^https?:\/\//, '').replace(/[^a-z0-9]+/gi, '-').slice(0, 60);

  for (const vp of WIDTHS) {
    const ctx = await browser.newContext({ viewport: { width: vp.width, height: vp.height } });
    await installTransport(ctx);
    const page = await ctx.newPage();

    // ---- Core Web Vitals proxies, installed before navigation
    await page.addInitScript(() => {
      window.__cwv = { lcp: 0, cls: 0, shifts: [] };
      try {
        new PerformanceObserver(l => {
          for (const e of l.getEntries()) window.__cwv.lcp = e.startTime;
        }).observe({ type: 'largest-contentful-paint', buffered: true });
        new PerformanceObserver(l => {
          for (const e of l.getEntries()) {
            if (!e.hadRecentInput) {
              window.__cwv.cls += e.value;
              if (e.value > 0.01) window.__cwv.shifts.push(e.value);
            }
          }
        }).observe({ type: 'layout-shift', buffered: true });
      } catch {}
    });

    let resp;
    try {
      resp = await page.goto(url, { waitUntil: 'networkidle', timeout: 45000 });
    } catch (e) {
      rec(url, `load@${vp.name}`, 'FAIL', String(e.message).slice(0, 160));
      await ctx.close();
      continue;
    }
    if (!resp || !resp.ok()) rec(url, `load@${vp.name}`, 'FAIL', `HTTP ${resp?.status()}`);

    // scroll the whole page so lazy content and shifts actually happen
    await page.evaluate(async () => {
      const step = innerHeight;
      for (let y = 0; y < document.body.scrollHeight; y += step) {
        scrollTo(0, y);
        await new Promise(r => setTimeout(r, 120));
      }
      scrollTo(0, 0);
    });
    await page.waitForTimeout(400);

    mkdirSync(OUT, { recursive: true });
    await page.screenshot({
      path: path.join(OUT, `${slug}-${vp.name}.png`), fullPage: true,
    });

    const cwv = await page.evaluate(() => window.__cwv);
    if (vp.name === 'mobile') {
      // Mobile thresholds, because desktop scores hide exactly these problems.
      if (USE_CURL) {
        rec(url, 'LCP (mobile)', 'WARN',
          'not measurable -- requests are proxied through curl in this environment. ' +
          'Use PageSpeed Insights for real timing.');
      } else {
        rec(url, 'LCP (mobile)', cwv.lcp === 0 ? 'WARN' : cwv.lcp <= 2500 ? 'PASS' : 'FAIL',
          `${Math.round(cwv.lcp)}ms (good <=2500)`);
      }
      rec(url, 'CLS (mobile)', cwv.cls <= 0.1 ? 'PASS' : 'FAIL',
        `${cwv.cls.toFixed(3)} (good <=0.1)`);

      // horizontal overflow — the classic mobile failure
      const overflow = await page.evaluate(() =>
        document.documentElement.scrollWidth - document.documentElement.clientWidth);
      rec(url, 'no horizontal scroll (mobile)', overflow <= 1 ? 'PASS' : 'FAIL', `${overflow}px overflow`);
    }

    // ---- accessibility, at every width (tap targets and reflow differ)
    await page.addScriptTag({ content: AXE });
    const axe = await page.evaluate(async () =>
      await window.axe.run(document, { resultTypes: ['violations'] }));
    const serious = axe.violations.filter(v => ['critical', 'serious'].includes(v.impact));
    rec(url, `a11y@${vp.name}`, serious.length ? 'FAIL' : axe.violations.length ? 'WARN' : 'PASS',
      serious.length
        ? serious.map(v => `${v.id}(${v.nodes.length})`).join(', ')
        : axe.violations.length
          ? `${axe.violations.length} minor: ` + axe.violations.map(v => v.id).join(', ')
          : 'no violations');

    if (vp.name !== 'desktop') { await ctx.close(); continue; }

    // ---------- desktop-only structural checks ----------
    const d = await page.evaluate(() => {
      const q = s => Array.from(document.querySelectorAll(s));
      const imgs = q('img');
      const head = document.head.innerHTML;
      return {
        h1: q('h1').map(h => h.textContent.trim().slice(0, 90)),
        canonical: document.querySelector('link[rel=canonical]')?.href || null,
        ogImage: document.querySelector('meta[property="og:image"]')?.content || null,
        ogTitle: document.querySelector('meta[property="og:title"]')?.content || null,
        twitter: !!document.querySelector('meta[name="twitter:card"]'),
        metaDesc: document.querySelector('meta[name=description]')?.content || null,
        robots: document.querySelector('meta[name=robots]')?.content || null,
        preconnect: q('link[rel=preconnect]').length,
        cssImport: /@import/.test(head),
        jsonld: q('script[type="application/ld+json"]').map(s => s.textContent),
        imgTotal: imgs.length,
        imgLazy: imgs.filter(i => i.loading === 'lazy').length,
        imgNoDims: imgs.filter(i => !i.getAttribute('width') || !i.getAttribute('height')).length,
        imgNoAlt: imgs.filter(i => !i.hasAttribute('alt')).length,
        heroPriority: imgs.slice(0, 2).some(i => i.getAttribute('fetchpriority') === 'high'),
        forms: q('form').length,
        hsForms: q('.hs-form, form.hs-form').length,
        meetings: q('[class*=meetings], iframe[src*=meetings]').length,
        mailto: q('a[href^=mailto]').length,
        tel: q('a[href^=tel]').length,
        links: Array.from(new Set(q('a[href]').map(a => a.href)))
          .filter(h => h.startsWith('http') && !h.includes('#')),
        text: document.body.innerText,
        headings: q('h1,h2,h3,h4').map(h => +h.tagName[1]),
      };
    });

    // SEO head
    rec(url, 'canonical', d.canonical ? 'PASS' : 'FAIL', d.canonical || 'absent');
    rec(url, 'meta description', d.metaDesc ? 'PASS' : 'FAIL',
      d.metaDesc ? `${d.metaDesc.length} chars` : 'absent');
    rec(url, 'og:title', d.ogTitle ? 'PASS' : 'FAIL', d.ogTitle ? 'present' : 'absent');
    rec(url, 'og:image', d.ogImage ? 'PASS' : 'FAIL',
      d.ogImage || 'absent — every social share renders a bare text link');
    rec(url, 'twitter:card', d.twitter ? 'PASS' : 'WARN', d.twitter ? 'present' : 'absent');
    rec(url, 'noindex check', /noindex/i.test(d.robots || '') ? 'FAIL' : 'PASS',
      d.robots || 'no robots meta (indexable)');

    // headings
    rec(url, 'exactly one h1', d.h1.length === 1 ? 'PASS' : 'FAIL',
      `${d.h1.length} found${d.h1.length ? ': ' + d.h1[0] : ''}`);
    let skip = null;
    for (let i = 1; i < d.headings.length; i++) {
      if (d.headings[i] - d.headings[i - 1] > 1) { skip = `h${d.headings[i - 1]} -> h${d.headings[i]}`; break; }
    }
    rec(url, 'heading order', skip ? 'WARN' : 'PASS', skip ? `skips ${skip}` : 'no skipped levels');

    // performance primitives
    rec(url, 'images lazy below fold', d.imgTotal <= 3 || d.imgLazy > 0 ? 'PASS' : 'FAIL',
      `${d.imgLazy}/${d.imgTotal} lazy`);
    rec(url, 'images have width/height', d.imgNoDims === 0 ? 'PASS' : 'FAIL',
      `${d.imgNoDims}/${d.imgTotal} missing dimensions (CLS risk)`);
    rec(url, 'images have alt', d.imgNoAlt === 0 ? 'PASS' : 'FAIL',
      `${d.imgNoAlt}/${d.imgTotal} missing alt`);
    rec(url, 'hero fetchpriority', d.heroPriority ? 'PASS' : 'WARN',
      d.heroPriority ? 'set' : 'no fetchpriority="high" on a leading image');
    rec(url, 'font preconnect', d.preconnect > 0 ? 'PASS' : 'WARN',
      `${d.preconnect} preconnect hints — a CSS @import chain costs extra round trips`);

    // ---- structured data, including WHOSE name is in it
    let orgName = null, invalid = [], types = [];
    for (const raw of d.jsonld) {
      try {
        const parsed = JSON.parse(raw);
        for (const node of (Array.isArray(parsed) ? parsed : [parsed])) {
          const t = node['@type'];
          types.push(Array.isArray(t) ? t.join('/') : t);
          if (t === 'Organization' || t === 'LocalBusiness' ||
              (Array.isArray(t) && t.includes('Organization'))) orgName = node.name;
        }
      } catch (e) { invalid.push(String(e.message).slice(0, 80)); }
    }
    rec(url, 'JSON-LD parses', invalid.length ? 'FAIL' : 'PASS',
      invalid.length ? invalid.join('; ') : `${d.jsonld.length} block(s): ${types.join(', ') || 'none'}`);
    rec(url, 'structured data present', d.jsonld.length ? 'PASS' : 'FAIL',
      d.jsonld.length ? `${d.jsonld.length} block(s)` : 'none on this page');

    if (EXPECT_ORG) {
      const ok = orgName && orgName.toLowerCase().includes(EXPECT_ORG.toLowerCase());
      rec(url, 'Organization names the client', ok ? 'PASS' : 'FAIL',
        `schema says "${orgName || 'nothing'}", expected "${EXPECT_ORG}"`);
    } else if (orgName) {
      const qbs = /quantum business solutions/i.test(orgName);
      rec(url, 'Organization entity', qbs ? 'FAIL' : 'WARN',
        qbs ? `names "${orgName}" — on a client site this is the wrong entity`
            : `names "${orgName}" — pass --expect-org to assert`);
    }

    // ---- conversion paths
    const hard = d.meetings + d.mailto + d.tel +
      (/book a call|request a demo|schedule|contact us|get started/i.test(d.text) ? 1 : 0);
    const soft = d.forms + d.hsForms +
      (/download|free (guide|score|check|audit|assessment)|calculator|estimator|newsletter|subscribe/i.test(d.text) ? 1 : 0);
    rec(url, 'hard conversion path', hard > 0 ? 'PASS' : 'FAIL',
      `${d.meetings} meetings embeds, ${d.mailto} mailto, ${d.tel} tel`);
    rec(url, 'soft conversion path', soft > 0 ? 'PASS' : 'FAIL',
      soft > 0 ? `${d.forms} form(s) / gated offer detected`
               : 'no form, no gated asset — visitors who are not ready to book cannot convert');
    rec(url, 'on-page form', (d.forms + d.hsForms) > 0 ? 'PASS' : 'WARN',
      `${d.forms + d.hsForms} form(s) — every click between intent and capture loses people`);

    // ---- placeholder text
    const hits = PLACEHOLDER.filter(r => r.test(d.text)).map(r => r.source);
    rec(url, 'no placeholder text', hits.length ? 'FAIL' : 'PASS',
      hits.length ? hits.join(', ') : 'clean');

    // ---- links (same-origin only, HEAD, capped)
    const origin = new URL(url).origin;
    const same = d.links.filter(h => h.startsWith(origin)).slice(0, 40);
    const broken = [];
    for (const href of same) {
      try {
        if (USE_CURL) {
          const r = curlFetch(href, 'HEAD');
          if (r && r.status >= 400) broken.push(`${r.status} ${href}`);
        } else {
          const r = await page.request.head(href, { timeout: 12000, maxRedirects: 5 });
          if (r.status() >= 400) broken.push(`${r.status()} ${href}`);
        }
      } catch { /* HEAD not supported — not evidence of breakage */ }
    }
    rec(url, 'no broken internal links', broken.length ? 'FAIL' : 'PASS',
      broken.length ? broken.slice(0, 6).join('; ') : `${same.length} checked`);

    await ctx.close();
  }
}

const browser = await launch();

// Probe the browser's own egress once. If it's blocked, switch to the curl transport
// rather than reporting every page as a load failure.
{
  const ctx = await browser.newContext();
  const pg = await ctx.newPage();
  try {
    await pg.goto(urls[0], { timeout: 20000, waitUntil: 'commit' });
  } catch {
    USE_CURL = true;
    console.log('\x1b[33mbrowser egress blocked — routing requests through curl\x1b[0m');
  }
  await ctx.close();
}

try {
  for (const u of urls) {
    console.log(`\n\x1b[1mauditing ${u}\x1b[0m`);
    await auditPage(browser, u);
  }
} finally {
  await browser.close();
}

// ------------------------------------------------------------------ report
const ICON = { PASS: '\x1b[32mPASS\x1b[0m', WARN: '\x1b[33mWARN\x1b[0m', FAIL: '\x1b[31mFAIL\x1b[0m' };
let fails = 0, warns = 0;
for (const u of urls) {
  const rows = results.filter(r => r.url === u);
  if (!rows.length) continue;
  console.log(`\n${'='.repeat(78)}\n${u}\n${'='.repeat(78)}`);
  const w = Math.max(...rows.map(r => r.gate.length));
  for (const r of rows) {
    if (r.status === 'FAIL') fails++;
    if (r.status === 'WARN') warns++;
    console.log(`  ${ICON[r.status]}  ${r.gate.padEnd(w)}  ${r.detail}`);
  }
}
mkdirSync(OUT, { recursive: true });
writeFileSync(path.join(OUT, 'report.json'), JSON.stringify({
  generatedAt: new Date().toISOString(), urls, results,
}, null, 2));

console.log(`\n${'-'.repeat(78)}`);
console.log(`  ${fails} FAIL   ${warns} WARN   ${results.length - fails - warns} PASS`);
console.log(`  screenshots + report.json in ./${OUT}/`);
console.log(`${'-'.repeat(78)}\n`);
if (fails) console.log('Gate NOT passed. A build nobody looked at is a build nobody checked.\n');
process.exit(fails ? 1 : 0);
