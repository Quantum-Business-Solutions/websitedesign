import { chromium } from 'playwright';
// node _shot.mjs <file.html> <width> <selector> <out.jpg> : element screenshot after scrolling it into view
const [file, w, sel, out] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--headless=new','--no-sandbox'] });
const p = await b.newPage({ viewport: { width: +w, height: 900 } });
await p.route(/fonts\.(googleapis|gstatic)\.com/, r => r.abort());
await p.goto('file://' + file); await p.waitForTimeout(300);
const el = p.locator(sel).first(); await el.scrollIntoViewIfNeeded(); await p.waitForTimeout(1700);
await el.screenshot({ path: out, type: 'jpeg', quality: 80 }); await b.close(); console.log(out);
