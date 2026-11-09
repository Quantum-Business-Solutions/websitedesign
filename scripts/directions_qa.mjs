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

const browser = await chromium.launch();
try {
  for (const d of opt.dirs || ['showcase', 'clean', 'press']) {
    const url = pathToFileURL(path.join(out, d, 'index.html')).href;
    const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
    try {
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
      await page.waitForTimeout(1200);

      // the heading face the visitor sees must be the one the brief names (house Open Sans when it names none), never the theme default
      const font = await page.evaluate(() => getComputedStyle(document.querySelector('h1')).fontFamily.split(',')[0].replace(/["']/g, '').trim());
      const want = d === 'press' ? HOUSE.press : (opt.heading ? null : HOUSE[d]);
      if (want && font.toLowerCase() !== want.toLowerCase()) add('FAIL', `font-${d}`, `headline is set in ${font}; expected ${want}`, `${d}/index.html`);
      else if (/bricolage/i.test(font)) add('FAIL', `font-${d}`, `${font} is the display face the clients rejected as whimsical`, `${d}/index.html`);
      else add('PASS', `font-${d}`, font);

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
  }
} finally { await browser.close(); }
console.log(JSON.stringify(rows));
