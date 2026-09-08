import { chromium } from 'playwright';
// node _clip.mjs <file.html> <width> <selector> <offsetY> <height> <out.jpg> : clipped screenshot of part of an element
const [file, w, sel, off, h, out] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--headless=new','--no-sandbox'] });
const p = await b.newPage({ viewport: { width: +w, height: 900 } });
await p.route(/fonts\.(googleapis|gstatic)\.com/, r => r.abort());
await p.goto('file://' + file); await p.waitForTimeout(300);
const el = p.locator(sel).first(); await el.scrollIntoViewIfNeeded(); await p.waitForTimeout(1200);
await p.evaluate(() => window.scrollTo(0, 0)); await p.waitForTimeout(200);
const box = await el.boundingBox();
const y = box.y + (+off); const hh = Math.min(+h, box.height - (+off));
await p.screenshot({ path: out, type: 'jpeg', quality: 78, fullPage: true, clip: { x: box.x, y, width: box.width, height: hh } });
await b.close(); console.log(out, Math.round(box.height));
