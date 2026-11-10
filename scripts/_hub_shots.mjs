// node _hub_shots.mjs <baseUrl> <outDir> <dir1,dir2,...> [width] [tallHeight]
// One PNG pair per direction for the chooser hub: <outDir>/<dir>-hero.png (first screen) and <outDir>/<dir>-tall.png
// (top of the home page, up to tallHeight). scripts/hub_shots.py turns them into the JPEGs the hub uses.
// require, not import: it also finds a global Playwright through NODE_PATH, which ESM import does not
import { createRequire } from 'node:module';
import fs from 'node:fs';
const { chromium } = createRequire(import.meta.url)('playwright');
import { chromePath } from './_chrome.mjs';
const [base, outDir, dirs, w = '1440', tall = '4200'] = process.argv.slice(2);
const W = +w, HERO_H = Math.round(W * 0.625), TALL = +tall;
const b = await chromium.launch({ executablePath: chromePath(), args: ['--headless=new', '--no-sandbox'] });
const ctx = await b.newContext({ viewport: { width: W, height: HERO_H }, deviceScaleFactor: 1, reducedMotion: 'no-preference' });
// same switches the QA scripts use: consent already given, preview notice already dismissed
await ctx.addInitScript(() => {
  try { localStorage.setItem('pp3-consent', '{"v":1,"choice":"all"}'); sessionStorage.setItem('pv-notice', '0'); } catch (e) {}
});
await ctx.route(/fonts\.(googleapis|gstatic)\.com/, r => r.abort());
let failed = 0;
for (const d of dirs.split(',').filter(Boolean)) {
  const p = await ctx.newPage();
  try {
    await p.goto(`${base}/${d}/index.html`, { waitUntil: 'load', timeout: 45000 });
    // preview-only chrome (direction switcher, sticky bars, notices, launchers) is not part of the design
    await p.addStyleTag({ content: '.pv-switch,.pv-switch-m,.pv-notice,.pv-sticky,.pp3-cc,.pv-util-fab,[class*="pv-launch"]{display:none!important}html{scroll-behavior:auto!important}' });
    await p.waitForTimeout(600);
    const full = await p.evaluate(() => document.documentElement.scrollHeight);
    const h = Math.min(TALL, full);
    // walk the page so scroll reveals, lazy images and counters have all fired, then come back to the top
    for (let y = 0; y <= h + HERO_H; y += Math.round(HERO_H * 0.7)) { await p.evaluate(v => window.scrollTo(0, v), y); await p.waitForTimeout(260); }
    await p.evaluate(() => window.scrollTo(0, 0));
    await p.waitForTimeout(900);
    await p.evaluate(() => Promise.all([...document.images].filter(i => !i.complete).map(i => new Promise(r => { i.onload = i.onerror = r; setTimeout(r, 4000); }))));
    // what the direction really looks like, measured: headline face, grounds and accent, for the hub's chips and swatches
    const look = await p.evaluate(() => {
      const rgb = c => { const m = (c || '').match(/rgba?\(([^)]+)\)/); if (!m) return null; const v = m[1].split(/[ ,/]+/).map(Number); return { r: v[0], g: v[1], b: v[2], a: v.length > 3 ? v[3] : 1 }; };
      const hex = c => '#' + [c.r, c.g, c.b].map(x => Math.round(x).toString(16).padStart(2, '0')).join('');
      const sat = c => { const mx = Math.max(c.r, c.g, c.b), mn = Math.min(c.r, c.g, c.b); return mx ? (mx - mn) / mx : 0; };
      const ground = el => { for (let e = el; e; e = e.parentElement) { const c = rgb(getComputedStyle(e).backgroundColor); if (c && c.a > 0.6) return hex(c); } return '#ffffff'; };
      const face = el => getComputedStyle(el).fontFamily.split(',')[0].replace(/['"]/g, '').trim();
      const vis = el => { const r = el.getBoundingClientRect(); return r.width > 40 && r.height > 12 && getComputedStyle(el).visibility !== 'hidden'; };
      const h1 = [...document.querySelectorAll('h1')].find(vis);
      if (!h1) return null;
      const r = h1.getBoundingClientRect(), cs = getComputedStyle(h1);
      let accent = null;
      for (const el of document.querySelectorAll('main a, main button, header a')) {
        const er = el.getBoundingClientRect(); if (er.top > 1200 || !vis(el)) continue;
        const c = rgb(getComputedStyle(el).backgroundColor); if (c && c.a > 0.9 && sat(c) > 0.45) { accent = hex(c); break; }
      }
      const h2 = [...document.querySelectorAll('main h2')].filter(vis).find(e => e.getBoundingClientRect().top + scrollY > 1100);
      const para = [...document.querySelectorAll('main p')].filter(vis).find(e => e.getBoundingClientRect().top + scrollY > 1100);
      return { h1: { x: r.left, y: r.top + scrollY, w: r.width, h: r.height }, heading_face: face(h1), heading_color: hex(rgb(cs.color)), hero_ground: ground(h1),
        accent, page_ground: h2 ? ground(h2) : ground(document.body), text_color: h2 ? hex(rgb(getComputedStyle(h2).color)) : null, body_face: para ? face(para) : face(document.body) };
    });
    if (look) {
      const pad = 18, c = look.h1;
      const clip = { x: Math.max(0, c.x - pad), y: Math.max(0, c.y - pad), width: Math.min(W - Math.max(0, c.x - pad), c.w + pad * 2), height: Math.min(700, c.h + pad * 2) };
      if (clip.width > 60 && clip.height > 30 && clip.y < 2000) await p.screenshot({ path: `${outDir}/${d}-type.png`, fullPage: true, clip });
      delete look.h1;
      fs.writeFileSync(`${outDir}/${d}-look.json`, JSON.stringify(look));
    }
    await p.screenshot({ path: `${outDir}/${d}-hero.png`, clip: { x: 0, y: 0, width: W, height: HERO_H } });
    await p.screenshot({ path: `${outDir}/${d}-tall.png`, fullPage: true, clip: { x: 0, y: 0, width: W, height: h } });
    console.log(`shot ${d} ${W}x${h} (page ${full})`);
  } catch (e) { failed++; console.error(`failed ${d}: ${e.message.split('\n')[0]}`); }
  await p.close();
}
await b.close();
process.exit(failed ? 2 : 0);
