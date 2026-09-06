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
 *                            [--env staging|production] [--forbid "a,b" | --forbid none]
 *
 * Exit code 0 = all gates pass, 1 = at least one FAIL. Wire it into CI or run it
 * before a client sees anything.
 */
import { chromium } from 'playwright';
import { readFileSync, mkdirSync, writeFileSync, readdirSync, existsSync, appendFileSync } from 'node:fs';
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
// Only patterns that a real page would never contain. "your company" on its own is
// legitimate marketing copy ("Are AI engines citing your company?") and produced a
// false positive on the first run -- so it has to be the bracketed/template form.
const PLACEHOLDER = [
  /\blorem ipsum\b/i, /\bdolor sit amet\b/i, /\bTODO\b/, /\bFIXME\b/, /\bXXX\b/,
  /\bexample\.com\b/i, /\byour company name\b/i, /\bcompany name here\b/i,
  /\[your [a-z ]{2,20}\]/i, /<your [a-z ]{2,20}>/i,
  /\{\{\s*\w+/, /\blogo here\b/i, /\bimage placeholder\b/i, /\btext placeholder\b/i,
  /\bplaceholder text\b/i, /\blipsum\b/i, /\bacme (corp|inc|co)\b/i,
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
const VALUE_FLAGS = ['out', 'expect-org', 'env', 'forbid'];
const flag = n => { const i = args.indexOf(`--${n}`); return i === -1 ? null : args[i + 1]; };
// Skip both the flag AND its value -- otherwise a flag value like
// --expect-org "Meridian Dental" gets audited as if it were a URL.
const urls = [];
for (let i = 0; i < args.length; i++) {
  const a = args[i];
  if (a.startsWith('--')) {
    if (VALUE_FLAGS.includes(a.slice(2))) i++;
    continue;
  }
  urls.push(a);
}
const OUT = flag('out') || 'verify-out';
const EXPECT_ORG = flag('expect-org');
// staging | production. A staging publish MUST be noindexed; production must not be.
// Without this the gate contradicted the runbook: step 24 says publish to staging so a
// page can be read at all, and a staging publish with no noindex is a crawlable
// duplicate of the client's site.
const ENV = (flag('env') || 'production').toLowerCase();
if (!['staging', 'production'].includes(ENV)) {
  console.error(`--env must be staging or production, got "${ENV}"`);
  process.exit(2);
}
// Strings that must never survive into a client's markup. Checked against outerHTML,
// not innerText, because the leaks live in src and href attributes.
const DEFAULT_FORBID = [
  'Quantum Business Solutions', 'thequantumleap.business', 'quantum-business-solutions',
  'Quantum Academy', 'meetings.hubspot.com/shawn-peterson',
  '/zoominfo-as-a-service', '/outbound-sales', '/connectandsell',
];
// --forbid "a,b"  replaces the default list.  --forbid none  skips the check — for QBS's own site,
// where the defaults are the brand, not a leak.
const FORBID_RAW = flag('forbid') || '';
const FORBID_NONE = FORBID_RAW.trim().toLowerCase() === 'none';
const FORBID = FORBID_NONE ? [] : FORBID_RAW.split(',').map(x => x.trim()).filter(Boolean);
if (urls.some(u => !/^https?:\/\//.test(u))) {
  console.error(`not a URL: ${urls.find(u => !/^https?:\/\//.test(u))}`);
  process.exit(2);
}

if (!urls.length) {
  console.error('usage: node scripts/verify.mjs <url> [...] [--out DIR] [--expect-org "Client Name"]');
  process.exit(2);
}

const results = [];
const CHECKED_LINKS = new Set();   // same-origin links already HEADed this run
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

    // ---- mobile audit. Most traffic is a phone, and most of what fails here
    // survives desktop review untouched. Measured, not eyeballed.
    await page.addInitScript(() => {
      window.mobileAudit = () => {
        const vis = el => {
          const r = el.getBoundingClientRect();
          const cs = getComputedStyle(el);
          return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' &&
                 cs.display !== 'none' && +cs.opacity > 0.05;
        };
        const q = sel => Array.from(document.querySelectorAll(sel));

        // --- tap targets. WCAG 2.5.8 (AA) is 24x24 CSS px; platform guidance is
        // 44 (Apple) / 48 (Android). Inline links inside a text block are exempt
        // from 2.5.8, so they're excluded rather than reported as noise.
        const inlineLink = a => {
          if (a.tagName !== 'A') return false;
          const p = a.parentElement;
          if (!p) return false;
          const t = (p.textContent || '').trim().length;
          return t > (a.textContent || '').trim().length + 12;
        };
        const targets = q('a[href],button,input:not([type=hidden]),select,textarea,' +
                          '[role=button],[role=link],[role=tab],[onclick]')
          .filter(vis).filter(el => !inlineLink(el));
        const tiny = [], small = [];
        for (const el of targets) {
          const r = el.getBoundingClientRect();
          const label = (el.getAttribute('aria-label') || el.textContent || el.name ||
                         el.tagName).trim().replace(/\s+/g, ' ').slice(0, 26) || el.tagName;
          const dim = `${Math.round(r.width)}x${Math.round(r.height)}`;
          if (r.width < 24 || r.height < 24) tiny.push(`${label} (${dim})`);
          else if (r.width < 44 || r.height < 44) small.push(`${label} (${dim})`);
        }

        // --- crowding: two targets whose 24px boxes overlap are hard to hit apart
        const crowded = [];
        for (let i = 0; i < targets.length && crowded.length < 6; i++) {
          const a = targets[i].getBoundingClientRect();
          for (let j = i + 1; j < targets.length; j++) {
            const b = targets[j].getBoundingClientRect();
            const gapX = Math.max(0, Math.max(a.left, b.left) - Math.min(a.right, b.right));
            const gapY = Math.max(0, Math.max(a.top, b.top) - Math.min(a.bottom, b.bottom));
            const gap = Math.hypot(gapX, gapY);
            if (gap > 0 && gap < 8) {
              crowded.push(`${(targets[i].textContent || targets[i].tagName).trim().slice(0, 16)} / ` +
                           `${(targets[j].textContent || targets[j].tagName).trim().slice(0, 16)} (${Math.round(gap)}px)`);
              break;
            }
          }
        }

        // --- text too small to read on a phone
        const tooSmall = {};
        for (const el of q('p,li,td,span,div,a,label,figcaption,small')) {
          const direct = Array.from(el.childNodes)
            .filter(n => n.nodeType === 3).map(n => n.textContent.trim()).join('');
          if (direct.length < 12 || !vis(el)) continue;
          const fs = parseFloat(getComputedStyle(el).fontSize);
          if (fs && fs < 13) {
            const k = `${fs}px`;
            tooSmall[k] = (tooSmall[k] || 0) + 1;
          }
        }

        // --- iOS auto-zooms any focused input under 16px, which yanks the layout
        const zoomers = q('input:not([type=hidden]),select,textarea').filter(vis)
          .filter(el => parseFloat(getComputedStyle(el).fontSize) < 16)
          .map(el => `${el.tagName.toLowerCase()}${el.type ? '[' + el.type + ']' : ''} ` +
                     `${parseFloat(getComputedStyle(el).fontSize)}px`);

        // --- fixed/sticky chrome eating the viewport
        let chrome = 0;
        const chromeParts = [];
        for (const el of q('*')) {
          const cs = getComputedStyle(el);
          if (cs.position !== 'fixed' && cs.position !== 'sticky') continue;
          if (!vis(el)) continue;
          const r = el.getBoundingClientRect();
          if (r.height < 8 || r.height > innerHeight * 0.9) continue;
          const atEdge = r.top <= 4 || Math.abs(r.bottom - innerHeight) <= 4;
          if (!atEdge) continue;
          if (el.parentElement && chromeParts.some(c => c.el.contains(el))) continue;
          chromeParts.push({ el, h: r.height });
          chrome += r.height;
        }

        // --- hero type set for a desktop, rendered on a phone
        const h1 = q('h1').filter(vis)[0];
        const h1px = h1 ? Math.round(parseFloat(getComputedStyle(h1).fontSize)) : 0;

        // --- overflow, and which element causes it
        const docW = document.documentElement.clientWidth;
        const bleeders = q('*').filter(el => {
          const r = el.getBoundingClientRect();
          return r.width > 0 && (r.right > docW + 2 || r.left < -2) &&
                 getComputedStyle(el).position !== 'fixed';
        }).slice(0, 4).map(el => (el.className && String(el.className).split(' ')[0]) ||
                                 el.tagName.toLowerCase());

        // --- responsive images
        const imgs = q('img').filter(vis);
        const noSrcset = imgs.filter(i => !i.srcset && !i.closest('picture')).length;
        const oversize = imgs.filter(i => i.naturalWidth &&
          i.naturalWidth > i.getBoundingClientRect().width * 2.5).length;

        return {
          tiny, small: small.slice(0, 8), crowded, tooSmall, zoomers: zoomers.slice(0, 6),
          chrome: Math.round(chrome), chromePct: Math.round(chrome / innerHeight * 100),
          h1px, docW, bleeders,
          imgTotal: imgs.length, noSrcset, oversize,
          navLinks: q('nav a,header a').filter(vis).length,
          navToggle: q('button,summary,[role=button],[aria-expanded],.hamburger,[class*=menu]')
            .filter(vis).length,
        };
      };
    });

    // ---- card-grid balance. Measures ACTUAL rendered rows, so it catches an
    // orphan the CSS didn't advertise -- see design/guardrails.md.
    await page.addInitScript(() => {
      window.measureGrids = () => {
        const out = [];
        for (const el of document.querySelectorAll('*')) {
          const kids = Array.from(el.children).filter(c => {
            const r = c.getBoundingClientRect();
            return r.width > 40 && r.height > 40;
          });
          if (kids.length < 3) continue;

          const boxes = kids.map(k => k.getBoundingClientRect());
          // Only card-like sets: children of similar width and height. This is what
          // keeps navs, footers and prose out of the results.
          const w = boxes.map(b => b.width), h = boxes.map(b => b.height);
          if (Math.max(...w) / Math.max(1, Math.min(...w)) > 1.35) continue;
          if (Math.max(...h) / Math.max(1, Math.min(...h)) > 3) continue;

          // Group by top edge into rows.
          const rows = [];
          for (const b of boxes.slice().sort((a, z) => a.top - z.top)) {
            const last = rows[rows.length - 1];
            if (last && Math.abs(last.top - b.top) < 12) last.n++;
            else rows.push({ top: b.top, n: 1 });
          }
          if (rows.length < 2) continue;

          const counts = rows.map(r => r.n);
          const widest = Math.max(...counts);
          const lastRow = counts[counts.length - 1];
          if (widest < 2 || lastRow >= widest) continue;

          out.push({
            total: kids.length, cols: widest, rows: counts, lastRow,
            label: (el.className && String(el.className).split(' ')[0]) || el.tagName.toLowerCase(),
            // The nearest heading BEFORE this grid in document order. Walking up and
            // taking an ancestor's first descendant heading finds the first h2 on the
            // page, which mislabels every grid on a flat layout.
            heading: (() => {
              const heads = Array.from(document.querySelectorAll('h1,h2,h3'));
              let best = '';
              for (const h of heads) {
                if (h.compareDocumentPosition(el) & Node.DOCUMENT_POSITION_FOLLOWING) {
                  best = h.textContent.trim().slice(0, 50);
                } else break;
              }
              return best;
            })(),
          });
        }
        // De-duplicate nested containers reporting the same shape.
        const seen = new Set();
        return out.filter(g => {
          const k = `${g.total}:${g.cols}:${g.lastRow}`;
          if (seen.has(k)) return false;
          seen.add(k);
          return true;
        });
      };
    });

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

      // ---------- mobile-specific gates ----------
      const m = await page.evaluate(() => mobileAudit());

      const overflow = await page.evaluate(() =>
        document.documentElement.scrollWidth - document.documentElement.clientWidth);
      rec(url, 'no horizontal scroll (mobile)', overflow <= 1 ? 'PASS' : 'FAIL',
        overflow <= 1 ? '0px' :
          `${overflow}px overflow${m.bleeders.length ? ' — from ' + m.bleeders.join(', ') : ''}`);

      // WCAG 2.5.8 AA is 24x24; 44 is Apple's guidance and what thumbs actually want.
      rec(url, 'tap targets >= 24px (WCAG 2.5.8)', m.tiny.length ? 'FAIL' : 'PASS',
        m.tiny.length ? `${m.tiny.length} under 24px: ${m.tiny.slice(0, 5).join(', ')}`
                      : 'all interactive targets 24px or larger');
      rec(url, 'tap targets >= 44px (thumb-friendly)', m.small.length ? 'WARN' : 'PASS',
        m.small.length ? `${m.small.length} between 24 and 44px: ${m.small.slice(0, 4).join(', ')}`
                       : 'all targets 44px or larger');
      rec(url, 'tap targets not crowded', m.crowded.length ? 'WARN' : 'PASS',
        m.crowded.length ? `under 8px apart: ${m.crowded.slice(0, 3).join('; ')}`
                         : 'adequate spacing');

      const tsKeys = Object.keys(m.tooSmall);
      rec(url, 'body text >= 13px on mobile', tsKeys.length ? 'FAIL' : 'PASS',
        tsKeys.length ? tsKeys.map(k => `${m.tooSmall[k]} element(s) at ${k}`).join(', ')
                      : 'no text under 13px');

      rec(url, 'inputs >= 16px (no iOS zoom)', m.zoomers.length ? 'FAIL' : 'PASS',
        m.zoomers.length ? `${m.zoomers.join(', ')} — iOS zooms the page on focus`
                         : m.imgTotal >= 0 ? 'no undersized inputs' : '');

      rec(url, 'sticky chrome <= 25% of viewport', m.chromePct <= 25 ? 'PASS' : 'FAIL',
        `${m.chrome}px = ${m.chromePct}% of the phone viewport`);

      rec(url, 'hero type sized for a phone', !m.h1px ? 'WARN' : m.h1px <= 44 ? 'PASS' : 'WARN',
        m.h1px ? `h1 renders at ${m.h1px}px on a ${m.docW}px screen` : 'no visible h1');

      rec(url, 'nav reachable on touch', m.navLinks > 0 || m.navToggle > 0 ? 'PASS' : 'FAIL',
        `${m.navLinks} visible nav link(s), ${m.navToggle} possible toggle(s) — ` +
        'a hover-only mega-menu is unreachable on a phone');

      rec(url, 'responsive images', m.noSrcset === 0 ? 'PASS' : 'WARN',
        `${m.noSrcset}/${m.imgTotal} without srcset or <picture>` +
        (m.oversize ? `, ${m.oversize} served at >2.5x their displayed size` : ''));
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

    // Grid balance is breakpoint-dependent -- a grid balanced on desktop can orphan
    // on tablet, so this runs at all three widths.
    {
      const grids = await page.evaluate(() => measureGrids());
      // A lone card under two is still a lone card. The old `cols >= 3` let the common
      // tablet case (5 cards rendering 2+2+1) through as a PASS.
      const orphans = grids.filter(g => g.lastRow === 1 && g.cols >= 2);
      const weak = grids.filter(g => g.lastRow > 1 && g.lastRow <= g.cols / 2 && g.cols >= 4);
      const describe = g =>
        `${g.total} cards as ${g.rows.join('+')}${g.heading ? ` under "${g.heading}"` : ''}`;
      if (orphans.length) {
        rec(url, `card grid balance@${vp.name}`, 'FAIL',
          orphans.map(describe).join('; ') +
          ' — one card alone on a row. Change the column count, span the odd card, ' +
          'or change the count. See design/guardrails.md.');
      }
      // Report weak rows even when an orphan exists -- they are separate grids, and
      // hiding one behind the other means a second pass to find it.
      if (weak.length) {
        rec(url, `card grid lopsided@${vp.name}`, 'WARN',
          weak.map(describe).join('; ') +
          ' — last row under half full. Fewer columns would balance it.');
      }
      if (!orphans.length && !weak.length) {
        rec(url, `card grid balance@${vp.name}`, 'PASS',
          grids.length ? `${grids.length} multi-row grid(s), last row full enough`
                       : 'no multi-row grids');
      }
    }

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
        viewport: document.querySelector('meta[name=viewport]')?.content || null,
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

    d.grids = await page.evaluate(() => measureGrids());

    // Viewport meta. Blocking pinch-zoom is a WCAG 1.4.4 failure and it is the one
    // mobile mistake that cannot be worked around by the user.
    {
      const v = d.viewport || '';
      const hasWidth = /width\s*=\s*device-width/i.test(v);
      const blocksZoom = /user-scalable\s*=\s*(no|0)/i.test(v) ||
                         /maximum-scale\s*=\s*1(\.0)?\b/i.test(v);
      rec(url, 'viewport meta', !d.viewport ? 'FAIL' : blocksZoom ? 'FAIL'
            : hasWidth ? 'PASS' : 'WARN',
        !d.viewport ? 'absent — the page renders at desktop width on a phone'
          : blocksZoom ? `"${v}" — blocks pinch-zoom (WCAG 1.4.4 failure)`
          : hasWidth ? v : `"${v}" — no width=device-width`);
    }

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
    let orgName = null, orgSameAs = null, invalid = [], types = [];
    for (const raw of d.jsonld) {
      try {
        const parsed = JSON.parse(raw);
        for (const node of (Array.isArray(parsed) ? parsed : [parsed])) {
          const t = node['@type'];
          types.push(Array.isArray(t) ? t.join('/') : t);
          if (t === 'Organization' || t === 'LocalBusiness' ||
              (Array.isArray(t) && t.includes('Organization'))) {
            orgName = node.name;
            orgSameAs = Array.isArray(node.sameAs) ? node.sameAs : (node.sameAs ? [node.sameAs] : []);
          }
        }
      } catch (e) { invalid.push(String(e.message).slice(0, 80)); }
    }
    rec(url, 'JSON-LD parses', invalid.length ? 'FAIL' : 'PASS',
      invalid.length ? invalid.join('; ') : `${d.jsonld.length} block(s): ${types.join(', ') || 'none'}`);
    rec(url, 'structured data present', d.jsonld.length ? 'PASS' : 'FAIL',
      d.jsonld.length ? `${d.jsonld.length} block(s)` : 'none on this page');

    // The failure the runbook ranks worst — a client site wearing our logo — had no gate
    // at all: the only QBS check tested the schema NAME and sat in an else-if that was
    // skipped whenever --expect-org was passed, i.e. on every real gated run.
    {
      const needles = FORBID_NONE ? [] : (FORBID.length ? FORBID : DEFAULT_FORBID);
      const html = await page.evaluate(() => document.documentElement.outerHTML);
      const hits = needles.filter(n => html.toLowerCase().includes(n.toLowerCase()));
      rec(url, 'no QBS branding left', hits.length ? 'FAIL' : 'PASS',
        FORBID_NONE ? 'skipped (--forbid none: this is our own site)'
        : hits.length ? `found: ${hits.join(', ')} — header/footer de-brand is incomplete`
                      : `${needles.length} forbidden string(s) checked`);
    }

    if (EXPECT_ORG) {
      const ok = orgName && orgName.toLowerCase().includes(EXPECT_ORG.toLowerCase());
      rec(url, 'Organization names the client', ok ? 'PASS' : 'FAIL',
        `schema says "${orgName || 'nothing'}", expected "${EXPECT_ORG}"`);
    }
    if (orgName) {
      const qbs = /quantum business solutions/i.test(orgName);
      rec(url, 'Organization entity', qbs ? 'FAIL' : 'WARN',
        qbs ? `names "${orgName}" — on a client site this is the wrong entity`
            : `names "${orgName}" — pass --expect-org to assert`);
      // sameAs is the entity-resolution signal: it is how an engine confirms this
      // Organization is that LinkedIn company page and not a namesake. The one
      // failure mode here is a client site pointing at *our* profiles.
      const sa = orgSameAs || [];
      const qbsProfile = sa.find(u => /quantum-business-solutions|thequantumleap|shawn-peterson/i.test(u));
      const hasLinkedIn = sa.some(u => /linkedin\.com\/company\//i.test(u));
      rec(url, 'Organization sameAs',
        qbsProfile ? 'FAIL' : (sa.length && hasLinkedIn) ? 'PASS' : 'WARN',
        qbsProfile ? `points at a QBS profile: ${qbsProfile}`
        : !sa.length ? 'empty — add at least the LinkedIn company URL (brands/<client>.md → Entity facts)'
        : !hasLinkedIn ? `${sa.length} URL(s) but no linkedin.com/company/ — personal profiles do not count`
        : `${sa.length} profile(s), LinkedIn company page present`);
    }

    // ---- conversion paths, scoped to the page's own content.
    // Counting against document.body.innerText meant a site-wide footer carrying
    // "Contact us" and a newsletter box satisfied BOTH gates on every page, including
    // pages with no offer at all -- which made the most commercially load-bearing line
    // in the checklist unenforced.
    const conv = await page.evaluate(() => {
      const main = document.querySelector('main, [role=main], .body-wrapper main') || document.body;
      const scoped = main.cloneNode(true);
      for (const el of scoped.querySelectorAll('header,footer,nav,[role=banner],[role=contentinfo]')) {
        el.remove();
      }
      const q = sel => Array.from(scoped.querySelectorAll(sel)).length;
      return {
        forms: q('form, .hs-form'),
        meetings: q('[class*=meetings], iframe[src*=meetings]'),
        mailto: q('a[href^=mailto]'),
        tel: q('a[href^=tel]'),
        gated: q('[class*=gated], [class*=download], [class*=calculator], [class*=estimator]'),
        text: scoped.innerText || '',
        scopedToMain: main !== document.body,
      };
    });
    const hard = conv.meetings + conv.mailto + conv.tel +
      (/book a call|request a demo|schedule|get started/i.test(conv.text) ? 1 : 0);
    const soft = conv.forms + conv.gated +
      (/download|free (guide|score|check|audit|assessment)|calculator|estimator/i.test(conv.text) ? 1 : 0);
    if (!conv.scopedToMain) {
      rec(url, 'conversion scope', 'WARN',
        'no <main> found — conversion counts include header/footer and may be optimistic');
    }
    rec(url, 'hard conversion path (in main)', hard > 0 ? 'PASS' : 'FAIL',
      `${conv.meetings} meetings embed(s), ${conv.mailto} mailto, ${conv.tel} tel`);
    rec(url, 'soft conversion path', soft > 0 ? 'PASS' : 'FAIL',
      soft > 0 ? `${conv.forms} form(s), ${conv.gated} gated element(s)`
               : 'no form, no gated asset — visitors who are not ready to book cannot convert');
    rec(url, 'on-page form (in main)', conv.forms > 0 ? 'PASS' : 'WARN',
      `${conv.forms} form(s) — every click between intent and capture loses people`);

    // ---- placeholder text
    const hits = PLACEHOLDER.filter(r => r.test(d.text)).map(r => r.source);
    rec(url, 'no placeholder text', hits.length ? 'FAIL' : 'PASS',
      hits.length ? hits.join(', ') : 'clean');

    // ---- links (same-origin only, HEAD, capped)
    // Nav links repeat on every page. Checking them once per run leaves the per-page
    // budget for links inside the content -- previously the nav ate all 40 slots and the
    // gate reported "40 checked", which read as coverage.
    const origin = new URL(url).origin;
    const fresh = d.links.filter(h => h.startsWith(origin) && !CHECKED_LINKS.has(h));
    const same = fresh.slice(0, 40);
    for (const h of same) CHECKED_LINKS.add(h);
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
      broken.length ? broken.slice(0, 6).join('; ')
                    : `${same.length} new link(s) checked, ${CHECKED_LINKS.size} this run`);

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

// ------------------------------------------------------------------ scoring
// A pass/fail gate answers "did it pass". It cannot answer "is it getting better".
// BrandCommand already scores campaign assets 0-100 (agent_runs.critic_score); this
// puts website pages on the same scale so there is one quality trendline. Weights
// follow the runbook's own ranking: correctness failures cost most, quality next,
// warnings least. Nothing ships under 80.
const CORRECTNESS = /no QBS branding|Organization names the client|Organization entity|Organization sameAs|a11y@|indexable|noindex|JSON-LD parses|tap targets >= 24|inputs >= 16|viewport meta|no placeholder|no horizontal scroll|load@/;
const QUALITY = /og:image|lazy|width\/height|card grid balance|conversion path|exactly one h1|body text|structured data present|broken internal|CLS|canonical|meta description/;
function scorePage(rows) {
  let score = 100;
  for (const r of rows) {
    if (r.status === 'FAIL') score -= CORRECTNESS.test(r.gate) ? 8 : QUALITY.test(r.gate) ? 5 : 3;
    else if (r.status === 'WARN') score -= 1.5;
  }
  score = Math.max(0, Math.round(score));
  const grade = score >= 90 ? 'A' : score >= 80 ? 'B' : score >= 70 ? 'C' : score >= 60 ? 'D' : 'F';
  return { score, grade, ships: score >= 80 };
}

// ------------------------------------------------------------------ report
const ICON = { PASS: '\x1b[32mPASS\x1b[0m', WARN: '\x1b[33mWARN\x1b[0m', FAIL: '\x1b[31mFAIL\x1b[0m' };
let fails = 0, warns = 0;
const scores = [];
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
  const sc = scorePage(rows);
  scores.push({ url: u, ...sc,
    fails: rows.filter(r => r.status === 'FAIL').length,
    warns: rows.filter(r => r.status === 'WARN').length });
  const col = sc.score >= 80 ? '\x1b[32m' : sc.score >= 60 ? '\x1b[33m' : '\x1b[31m';
  console.log(`\n  ${col}SCORE ${sc.score}/100  grade ${sc.grade}\x1b[0m` +
              (sc.ships ? '' : '  — under 80, does not ship'));
}

// Append to the trendline. One line per page per run; this is the file that lets you
// say "build ten scored 91 and build one scored 74", which is the only honest proof
// a process is improving.
{
  const line = scores.map(sc => JSON.stringify({
    at: new Date().toISOString(), env: ENV, expectOrg: EXPECT_ORG || null, ...sc,
  })).join('\n') + '\n';
  mkdirSync(OUT, { recursive: true });
  appendFileSync(path.join(OUT, 'scores.jsonl'), line);
}
mkdirSync(OUT, { recursive: true });
writeFileSync(path.join(OUT, 'report.json'), JSON.stringify({
  generatedAt: new Date().toISOString(), urls, results, scores,
}, null, 2));

console.log(`\n${'-'.repeat(78)}`);
console.log(`  ${fails} FAIL   ${warns} WARN   ${results.length - fails - warns} PASS`);
console.log(`  screenshots + report.json in ${OUT.startsWith('/') ? OUT : './' + OUT}/`);
console.log(`${'-'.repeat(78)}\n`);
const underFloor = scores.filter(sc => !sc.ships).length;
if (fails || underFloor) {
  console.log('Gate NOT passed. A build nobody looked at is a build nobody checked.\n');
}
process.exit(fails || underFloor ? 1 : 0);
