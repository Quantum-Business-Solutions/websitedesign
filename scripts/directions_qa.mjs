// The rendered half of scripts/directions_qa.py. Usage: node directions_qa.mjs <out folder> '<json options>'
// Prints a JSON array of {level, check, message, where}. Never throws: a failure to launch is one WARN row.
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';
import path from 'node:path';
import { execSync } from 'node:child_process';

const out = path.resolve(process.argv[2]);
const opt = JSON.parse(process.argv[3] || '{}');
const rows = [];
const add = (level, check, message, where = '') => rows.push({ level, check, message, where });

let chromium;
try {
  const require = createRequire(import.meta.url);
  try { ({ chromium } = require('playwright')); }
  catch { ({ chromium } = require(path.join(execSync('npm root -g').toString().trim(), 'playwright'))); }
} catch (e) {
  console.log(JSON.stringify([{ level: 'WARN', check: 'rendered', message: 'playwright is not installed here: ' + e.message.slice(0, 80), where: '' }]));
  process.exit(0);
}

const HOUSE = { showcase: 'Open Sans', clean: 'Open Sans', press: 'Playfair Display' };
const lum = (r, g, b) => { const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; }; return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b); };
const ratio = (a, b) => { const [hi, lo] = a > b ? [a, b] : [b, a]; return (hi + 0.05) / (lo + 0.05); };

const { launchOpts } = await import('./_chrome.mjs');
const fs = await import('node:fs');
let browser;
try { browser = await chromium.launch(launchOpts()); }
catch (e) {
  console.log(JSON.stringify([{ level: 'WARN', check: 'rendered', message: 'no browser to run the rendered checks: ' + e.message.split('\n')[0].slice(0, 120), where: '' }]));
  process.exit(0);
}
// Faces that never reach a client page (scripts/preview.py REJECTED_FACES): the theme display faces and the script
// and rounded display faces a brief could name.
const REJECTED = /bricolage|fraunces|instrument[ +]serif|pacifico|lobster|caveat|dancing script|satisfy|great vibes|kaushan|permanent marker|amatic|indie flower|shadows into light|sacramento|courgette|comic sans|comic neue|fredoka|baloo|comfortaa|quicksand|nunito(?![ +]sans)|varela round|rounded 1c|chewy|bubblegum|righteous|bangers|luckiest guy|pangolin|gochi hand|patrick hand/i;
const AXE = (() => { try { return createRequire(import.meta.url).resolve('axe-core/axe.min.js'); } catch { return null; } })();
const qaDir = path.join(out, 'qa');
fs.mkdirSync(qaDir, { recursive: true });
const shots = [];

// Every face the browser actually used to draw glyphs in the headings, buttons, numerals and body (CDP platform fonts),
// which is what a visitor sees, not what the stylesheet asked for.
async function facesUsed(page) {
  const cdp = await page.context().newCDPSession(page);
  await cdp.send('DOM.enable'); await cdp.send('CSS.enable');
  const { root } = await cdp.send('DOM.getDocument', { depth: 0 });
  const groups = { headings: 'h1,h2,h3,h4,h5,h6', buttons: 'a.q-btn,.q-btn-ghost,button,.hs-button,input[type=submit],.q-booknow,.btn', numerals: '.pv-stat b,.pv-hero-stats b,.pv-proof b,.pv-badge b,.pv-metric .v,.q-stagenum,.pv-tl .y,.pv-seal .badge b,.pv-flow .dot', body: 'p,li,label,summary,blockquote,figcaption,td,th,a,span' };
  const res = {};
  for (const [g, sel] of Object.entries(groups)) {
    const { nodeIds } = await cdp.send('DOM.querySelectorAll', { nodeId: root.nodeId, selector: sel });
    const fams = new Set();
    for (const id of nodeIds.slice(0, 500)) { try { const { fonts } = await cdp.send('CSS.getPlatformFontsForNode', { nodeId: id }); for (const f of fonts) fams.add(f.familyName); } catch { /* detached */ } }
    res[g] = [...fams];
  }
  await cdp.detach();
  return res;
}

// A full-page picture with every scroll reveal played, for the contact sheet.
async function fullShot(page, file) {
  await page.addStyleTag({ content: '.pv-switch,.pv-switch-m,.pv-sticky,.pv-sl{display:none!important}.q-header{position:static!important}' });
  const h = await page.evaluate(() => document.documentElement.scrollHeight);
  for (let y = 0; y < h; y += 600) { await page.evaluate(v => scrollTo(0, v), y); await page.waitForTimeout(50); }
  await page.evaluate(() => scrollTo(0, 0)); await page.waitForTimeout(350);
  await page.screenshot({ path: file, fullPage: true, type: 'jpeg', quality: 70 });
  return h;
}

// The beauty bar's measurable half (process/directions-standard.md, rule 8), on one page at one width.
async function measure(page) {
  return page.evaluate(() => {
    const vis = e => { const r = e.getBoundingClientRect(), c = getComputedStyle(e); return r.width > 1 && r.height > 1 && c.visibility !== 'hidden' && c.display !== 'none'; };   // opacity is not tested: a scroll reveal starts at 0
    // type floor: the smallest text a visitor is asked to read (HTML text nodes; chart labels inside an SVG scale with it)
    const small = [];
    const tw = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    const seen = new Set();
    for (let n = tw.nextNode(); n; n = tw.nextNode()) {
      const e = n.parentElement; if (!e || seen.has(e) || !n.nodeValue.trim() || e.closest('svg,script,style,noscript,.pv-switch,.pv-switch-m,[hidden],details:not([open]) > :not(summary)')) continue;
      seen.add(e); if (!vis(e)) continue;
      const fs = parseFloat(getComputedStyle(e).fontSize);
      if (fs < 13) small.push({ fs, t: n.nodeValue.trim().slice(0, 40), c: (e.className || e.tagName).toString().slice(0, 40) });
    }
    // heading order: one h1, and no level skipped on the way down
    const hs = [...document.querySelectorAll('main h1,main h2,main h3,main h4,main h5,main h6')].filter(vis).map(h => ({ l: +h.tagName[1], t: h.textContent.trim().slice(0, 50) }));
    const skips = []; for (let i = 1; i < hs.length; i++) if (hs[i].l - hs[i - 1].l > 1) skips.push(`h${hs[i - 1].l} "${hs[i - 1].t}" then h${hs[i].l} "${hs[i].t}"`);
    const h1s = document.querySelectorAll('h1').length;
    // competing accents: saturated colours used as paint (fills, text, rules), by hue family, weighted by how much of the page they cover
    const fam = {};
    const hsl = (r, g, b) => { r /= 255; g /= 255; b /= 255; const mx = Math.max(r, g, b), mn = Math.min(r, g, b), l = (mx + mn) / 2, d = mx - mn; if (!d) return [0, 0, l]; const s = d / (1 - Math.abs(2 * l - 1)); let h = mx === r ? ((g - b) / d) % 6 : mx === g ? (b - r) / d + 2 : (r - g) / d + 4; h = (h * 60 + 360) % 360; return [h, s, l]; };
    const add = (col, w) => { const m = (col || '').match(/rgba?\(([\d.]+)[ ,]+([\d.]+)[ ,]+([\d.]+)(?:[ ,/]+([\d.]+))?/); if (!m) return; if (m[4] !== undefined && +m[4] < 0.5) return; const [h, s, l] = hsl(+m[1], +m[2], +m[3]); if (s < 0.45 || l < 0.2 || l > 0.82) return; const k = Math.round(h / 40) % 9; fam[k] = (fam[k] || 0) + w; };
    for (const e of document.querySelectorAll('main *, header *, footer *')) {
      if (e.closest('svg,img,picture,video,model-viewer,.pv-awards,.pv-logos') || !vis(e)) continue;
      const c = getComputedStyle(e), r = e.getBoundingClientRect(), area = r.width * r.height;
      add(c.backgroundColor, area);
      if ([...e.childNodes].some(n => n.nodeType === 3 && n.nodeValue.trim())) add(c.color, Math.min(area, 4000));
      if (parseFloat(c.borderTopWidth) > 0) add(c.borderTopColor, r.width * 2);
    }
    const total = Object.values(fam).reduce((a, b) => a + b, 0) || 1;
    const families = Object.entries(fam).filter(([, w]) => w / total > 0.04).map(([k]) => +k * 40);
    return { small, skips, h1s, families };
  });
}

try {
  for (const d of opt.dirs || ['showcase', 'clean', 'press']) {
    const url = pathToFileURL(path.join(out, d, 'index.html')).href;
    // motion reduced: every scroll reveal is in, so the type, contrast and axe checks see the whole page, not the first screen
    const page = await browser.newPage({ viewport: { width: 1280, height: 900 }, reducedMotion: 'reduce' });
    try {
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
      await page.waitForTimeout(1200);

      // the heading face the visitor sees must be the one the brief names (house Open Sans when it names none), never the theme default
      const font = await page.evaluate(() => getComputedStyle(document.querySelector('h1')).fontFamily.split(',')[0].replace(/["']/g, '').trim());
      const want = d === 'press' ? HOUSE.press : (opt.heading ? null : HOUSE[d]);
      if (want && font.toLowerCase() !== want.toLowerCase()) add('FAIL', `font-${d}`, `headline is set in ${font}; expected ${want}`, `${d}/index.html`);
      else if (/bricolage/i.test(font)) add('FAIL', `font-${d}`, `${font} is the display face the clients rejected as whimsical`, `${d}/index.html`);
      else add('PASS', `font-${d}`, font);

      // no rejected face anywhere on the page: not drawn in any heading, button, numeral or body line, not even named in the source
      await page.evaluate(() => document.fonts.ready);
      const used = await facesUsed(page);
      const drawn = Object.entries(used).flatMap(([g, f]) => f.filter(x => REJECTED.test(x)).map(x => `${x} in ${g}`));
      const named = [...new Set((fs.readFileSync(path.join(out, d, 'index.html'), 'utf8').match(new RegExp(REJECTED.source, 'gi')) || []).map(x => x.toLowerCase()))];
      if (drawn.length) add('FAIL', `face-leak-${d}`, `a rejected display face is drawn: ${drawn.slice(0, 3).join('; ')}`, `${d}/index.html`);
      else if (named.length) add('FAIL', `face-leak-${d}`, `the page source still names ${named.join(', ')}; it must not be importable`, `${d}/index.html`);
      else add('PASS', `face-leak-${d}`, `headings ${used.headings.slice(0, 2).join(' + ') || 'none'}; buttons ${used.buttons.slice(0, 2).join(' + ') || 'none'}; numerals ${used.numerals.slice(0, 2).join(' + ') || 'none'}`);

      // the measurable half of the beauty bar, desktop: type floor, heading order, competing accents, contrast everywhere
      const md = await measure(page);
      const tiny = md.small.filter(x => x.fs < 12);
      if (tiny.length) add('FAIL', `type-floor-${d}`, `${tiny.length} pieces of text under 12px at 1280, e.g. ${tiny[0].fs}px "${tiny[0].t}" (${tiny[0].c})`, `${d}/index.html`);
      else if (md.small.length) add('WARN', `type-floor-${d}`, `${md.small.length} pieces of text under 13px at 1280, e.g. ${md.small[0].fs}px "${md.small[0].t}" (${md.small[0].c})`, `${d}/index.html`);
      else add('PASS', `type-floor-${d}`, 'nothing under 13px at 1280');
      if (md.h1s !== 1) add('FAIL', `heading-order-${d}`, `${md.h1s} h1 elements; a page has one`, `${d}/index.html`);
      else if (md.skips.length) add('FAIL', `heading-order-${d}`, `${md.skips.length} skipped heading levels, e.g. ${md.skips[0]}`, `${d}/index.html`);
      else add('PASS', `heading-order-${d}`, 'one h1, no level skipped');
      if (md.families.length > 3) add('FAIL', `accent-count-${d}`, `${md.families.length} saturated colour families are used as paint (hues near ${md.families.join(', ')} degrees); the bar is the accent plus at most two`, `${d}/index.html`);
      else if (md.families.length === 3) add('WARN', `accent-count-${d}`, `three saturated colour families (hues near ${md.families.join(', ')} degrees); check they are all the client's`, `${d}/index.html`);
      else add('PASS', `accent-count-${d}`, `${md.families.length} saturated colour ${md.families.length === 1 ? 'family' : 'families'}`);
      if (AXE) {
        await page.addScriptTag({ path: AXE });
        const v = await page.evaluate(async () => (await axe.run(document)).violations.map(x => ({ id: x.id, n: x.nodes.length, first: x.nodes[0].html.slice(0, 90) })));
        const cc = v.find(x => x.id === 'color-contrast');
        if (cc) add('FAIL', `contrast-floor-${d}`, `${cc.n} pieces of text under 4.5:1 (3:1 for large text), e.g. ${cc.first}`, `${d}/index.html`);
        else add('PASS', `contrast-floor-${d}`, 'every line of text clears 4.5:1 (3:1 large)');
        const rest = v.filter(x => x.id !== 'color-contrast');
        if (rest.length) add('FAIL', `axe-${d}`, `${rest.length} accessibility rules fail: ${rest.map(x => `${x.id} (${x.n})`).join(', ').slice(0, 160)}`, `${d}/index.html`);
        else add('PASS', `axe-${d}`, 'no axe violations on the home page');
      }

      // corner shape follows the live site
      const wantR = opt.button_radius ?? opt.radius;
      if (wantR != null && d !== 'press') {
        const br = await page.evaluate(() => { const b = document.querySelector('.q-btn'); return b ? getComputedStyle(b).borderTopLeftRadius : null; });
        if (br !== null && parseFloat(br) !== wantR) add('FAIL', `radius-${d}`, `buttons are ${br}; the live site's button radius is ${wantR}px`, `${d}/index.html`);
        else add('PASS', `radius-${d}`, br ?? 'no button on the first screen');
      }

      // legibility of the first screen's headline and lead: sample what is behind the text with the text hidden
      for (const sel of ['h1', '.q-lead']) {
        const box = await page.evaluate((s) => {
          const e = document.querySelector(s); if (!e) return null;
          const r = e.getBoundingClientRect(), c = getComputedStyle(e).color.match(/[\d.]+/g).map(Number);
          return { x: Math.max(0, r.x), y: Math.max(0, r.y), w: Math.min(r.width, 1280), h: Math.min(r.height, 400), c };
        }, sel);
        if (!box || box.h < 8 || box.y > 880) continue;
        await page.addStyleTag({ content: `${sel}{visibility:hidden!important}` });
        const buf = await page.screenshot({ clip: { x: box.x, y: box.y, width: Math.max(8, box.w), height: Math.max(8, Math.min(box.h, 880 - box.y)) }, type: 'png' });
        await page.addStyleTag({ content: `${sel}{visibility:visible!important}` });
        const px = await page.evaluate(async (b64) => {
          const img = new Image(); img.src = 'data:image/png;base64,' + b64; await img.decode();
          const c = document.createElement('canvas'); c.width = Math.min(img.width, 120); c.height = Math.min(img.height, 60);
          const x = c.getContext('2d'); x.drawImage(img, 0, 0, c.width, c.height);
          return Array.from(x.getImageData(0, 0, c.width, c.height).data);
        }, buf.toString('base64'));
        const L = []; for (let i = 0; i < px.length; i += 4) L.push(lum(px[i], px[i + 1], px[i + 2]));
        L.sort((a, b) => a - b);
        const tl = lum(box.c[0], box.c[1], box.c[2]);
        const bg = tl > 0.5 ? L[Math.floor(L.length * 0.9)] : L[Math.floor(L.length * 0.1)];   // the worst part of the ground behind the text
        const cr = ratio(tl, bg), need = sel === 'h1' ? 3 : 4.5;
        if (cr < need) add('FAIL', `legible-${sel === 'h1' ? 'headline' : 'lead'}-${d}`, `contrast ${cr.toFixed(1)}:1 behind the ${sel === 'h1' ? 'headline' : 'lead line'} (needs ${need}:1)`, `${d}/index.html`);
        else add('PASS', `legible-${sel === 'h1' ? 'headline' : 'lead'}-${d}`, `${cr.toFixed(1)}:1`);
      }

      // phone: no sideways scroll, logo present and not stretched
      await page.setViewportSize({ width: 390, height: 800 });
      await page.waitForTimeout(400);
      const mm = await measure(page);
      const tinyM = mm.small.filter(x => x.fs < 12);
      if (tinyM.length) add('FAIL', `type-floor-phone-${d}`, `${tinyM.length} pieces of text under 12px at 390, e.g. ${tinyM[0].fs}px "${tinyM[0].t}" (${tinyM[0].c})`, `${d}/index.html`);
      else if (mm.small.length) add('WARN', `type-floor-phone-${d}`, `${mm.small.length} pieces of text under 13px at 390, e.g. ${mm.small[0].fs}px "${mm.small[0].t}"`, `${d}/index.html`);
      else add('PASS', `type-floor-phone-${d}`, 'nothing under 13px at 390');
      const m = await page.evaluate(() => ({ over: document.scrollingElement.scrollWidth - innerWidth, logo: (() => { const i = document.querySelector('header img, .q-logo img'); return i ? { w: i.naturalWidth, h: i.naturalHeight, shown: i.getBoundingClientRect().height } : null; })() }));
      if (m.over > 2) add('FAIL', `overflow-${d}`, `${m.over}px of sideways scroll at 390`, `${d}/index.html`); else add('PASS', `overflow-${d}`, 'no sideways scroll at 390');
      if (d === 'showcase') {
        if (!m.logo) add('FAIL', 'logo-shown', 'no logo image in the header');
        else if (m.logo.shown < 24) add('WARN', 'logo-shown', `the header logo is ${Math.round(m.logo.shown)}px tall on a phone; make it bigger or send a vector`);
        else add('PASS', 'logo-shown', `${Math.round(m.logo.shown)}px tall at 390`);
      }
    } catch (e) {
      add('WARN', `rendered-${d}`, e.message.slice(0, 120), `${d}/index.html`);
    }
    await page.close();
    // the pictures: the home page, whole, at 1280 and 390, with motion reduced so every reveal is in
    for (const w of [1280, 390]) {
      const sp = await browser.newPage({ viewport: { width: w, height: w === 390 ? 800 : 900 }, reducedMotion: 'reduce' });
      try {
        await sp.goto(url, { waitUntil: 'load', timeout: 30000 });
        await sp.evaluate(() => document.fonts.ready);
        const file = `${d}-home-${w}.jpg`;
        const h = await fullShot(sp, path.join(qaDir, file));
        shots.push({ dir: d, w, h, file });
      } catch (e) { add('WARN', `picture-${d}-${w}`, e.message.slice(0, 120), `${d}/index.html`); }
      await sp.close();
    }
  }

  // the contact sheet: one picture a person can judge at a glance, and a page that puts it beside the gate's result
  if (shots.length) {
    const dirs = [...new Set(shots.map(s => s.dir))];
    const DW = 420, PW = 150, GAP = 18, CAP = 5200;
    const cols = dirs.map(d => {
      const a = shots.find(s => s.dir === d && s.w === 1280), b = shots.find(s => s.dir === d && s.w === 390);
      const img = (s, w) => s ? `<div style="width:${w}px;max-height:${CAP}px;overflow:hidden;border:1px solid #d9dce2;border-radius:6px;background:#fff"><img src="${s.file}" style="width:${w}px;display:block"></div>` : '';
      return `<div><div style="font:600 15px/1.2 Arial,sans-serif;color:#14171c;margin:0 0 10px"><span style="text-transform:capitalize">${d}</span> <span style="font-weight:400;color:#5a6070">1280 and 390</span></div><div style="display:flex;gap:${GAP}px;align-items:flex-start">${img(a, DW)}${img(b, PW)}</div></div>`;
    }).join('');
    const sheet = await browser.newPage({ viewport: { width: dirs.length * (DW + PW + GAP * 2) + GAP * 2, height: 900 } });
    const tmp = path.join(qaDir, '_sheet.html');     // a file beside the pictures, so the browser may load them
    fs.writeFileSync(tmp, `<!doctype html><meta charset="utf-8"><body style="margin:0;padding:${GAP}px;background:#f3f4f6"><div style="display:flex;gap:${GAP * 2}px;align-items:flex-start">${cols}</div></body>`);
    await sheet.goto(pathToFileURL(tmp).href, { waitUntil: 'load' });
    await sheet.waitForTimeout(300);
    await sheet.screenshot({ path: path.join(qaDir, 'contact-sheet.jpg'), fullPage: true, type: 'jpeg', quality: 72 });
    await sheet.close();
    fs.rmSync(tmp, { force: true });
    add('PASS', 'contact-sheet', `qa/contact-sheet.jpg and qa/index.html: the home page of ${dirs.join(', ')} at 1280 and 390`);
    fs.writeFileSync(path.join(qaDir, 'shots.json'), JSON.stringify(shots));
  }
} finally { await browser.close(); }
console.log(JSON.stringify(rows));
