// Preview page check: full-page screenshots at 1440 and 390, link and image resolution, small text, em dashes, console errors.
// Usage (from websitedesign): node scripts/preview_check.mjs clean/index.html clean/blog/<slug>.html ...
// Pages are relative to ROOT (the client repo). Results in OUT/results.json.
import { chromium } from 'playwright';
import fs from 'fs'; import path from 'path';
const ROOT = '/home/user/kelly-office-solutions';
const OUT = '/tmp/claude-0/-home-user-Claude/798fbbce-ca0c-53c7-a6be-67c5e0055ed0/scratchpad/qa3';
const pages = process.argv.slice(2);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--headless=new','--no-sandbox'] });
const results = [];
for (const p of pages) {
  for (const w of [1440, 390]) {
    const ctx = await b.newContext({ viewport: { width: w, height: w === 390 ? 844 : 900 }, deviceScaleFactor: 1 });
    const page = await ctx.newPage();
    const errs = [];
    page.on('pageerror', e => errs.push(String(e)));
    page.on('console', m => { if (m.type() === 'error' && !/fonts\.g/.test(m.text())) errs.push(m.text()); });
    await page.route(/fonts\.(googleapis|gstatic)\.com/, r => r.abort());
    await page.goto('file://' + path.join(ROOT, p), { waitUntil: 'load' });
    await page.waitForTimeout(600);
    // scroll through to trigger lazy/reveal
    await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 700) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 40)); } window.scrollTo(0, 0); });
    await page.waitForTimeout(400);
    const info = await page.evaluate(() => {
      const links = [...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href'));
      const imgs = [...document.querySelectorAll('img')].map(i => ({ src: i.getAttribute('src'), ok: i.naturalWidth > 0, w: i.getAttribute('width'), h: i.getAttribute('height') }));
      const small = [...document.querySelectorAll('body *')].filter(e => e.children.length === 0 && e.textContent.trim() && parseFloat(getComputedStyle(e).fontSize) < 13).map(e => e.tagName + ':' + e.textContent.trim().slice(0, 30));
      const hs = [...document.querySelectorAll('h1,h2,h3,h4')].map(h => h.tagName + ' ' + h.textContent.trim().slice(0, 40));
      return { sw: document.documentElement.scrollWidth, h: document.body.scrollHeight, links, imgs, small, hs, em: (document.body.innerText.match(/—/g) || []).length, title: document.title };
    });
    const name = p.replace(/\//g, '_').replace('.html', '') + '-' + w + '.png';
    await page.screenshot({ path: path.join(OUT, name), fullPage: true });
    // check links resolve
    const dir = path.dirname(path.join(ROOT, p));
    const broken = info.links.filter(h => h && !/^(#|http|mailto:|tel:)/.test(h)).map(h => h.split('#')[0]).filter(h => h && !fs.existsSync(path.resolve(dir, h)));
    const badImgs = info.imgs.filter(i => !i.ok || !i.w || !i.h);
    results.push({ p, w, sw: info.sw, h: info.h, broken: [...new Set(broken)], badImgs, small: info.small.slice(0, 10), em: info.em, errs, hs: w === 1440 ? info.hs : undefined, title: info.title });
    await ctx.close();
  }
}
await b.close();
fs.writeFileSync(path.join(OUT, 'results.json'), JSON.stringify(results, null, 1));
for (const r of results) console.log(r.p, r.w, 'sw', r.sw, 'h', r.h, 'broken', r.broken.length, r.broken.slice(0,5).join(','), 'badImg', r.badImgs.length, r.badImgs.slice(0,3).map(i=>i.src).join(','), 'small', r.small.length, 'em', r.em, 'errs', r.errs.length, r.errs.slice(0,2).join(' | '));
