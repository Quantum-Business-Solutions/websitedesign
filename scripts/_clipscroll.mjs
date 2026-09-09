import { chromium } from 'playwright';
import { chromePath } from './_chrome.mjs';
// node _clipscroll.mjs <file.html> <width> <offsetY> <height> <out.jpg> : scroll through the whole page first so reveals fire, then clip
const [file, w, off, h, out] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: chromePath(), args: ['--headless=new','--no-sandbox'] });
const p = await b.newPage({ viewport: { width: +w, height: 900 } });
await p.route(/fonts\.(googleapis|gstatic)\.com/, r => r.abort());
await p.goto('file://' + file); await p.waitForTimeout(400);
const total = await p.evaluate(() => document.documentElement.scrollHeight);
for (let y = 0; y < total; y += 600) { await p.evaluate(v => window.scrollTo(0, v), y); await p.waitForTimeout(120); }
await p.evaluate(() => window.scrollTo(0, 0)); await p.waitForTimeout(900);
const hh = Math.min(+h, total - (+off));
await p.screenshot({ path: out, type: 'jpeg', quality: 78, fullPage: true, clip: { x: 0, y: +off, width: +w, height: hh } });
await b.close(); console.log(out, total);
