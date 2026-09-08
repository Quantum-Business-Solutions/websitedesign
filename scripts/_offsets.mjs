import { chromium } from 'playwright';
// node _offsets.mjs <file.html> <width> : prints section id and offsetTop
const [file, w] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--headless=new','--no-sandbox'] });
const p = await b.newPage({ viewport: { width: +w, height: 900 } });
await p.route(/fonts\.(googleapis|gstatic)\.com/, r => r.abort());
await p.goto('file://' + file); await p.waitForTimeout(400);
console.log(JSON.stringify(await p.evaluate(() => [...document.querySelectorAll('section[id], .pv-ba, .pv-flow, model-viewer, .pv-mv, .pv-fleet, .pv-hot')].map(e => [e.id || e.className.split(' ')[0] || e.tagName, Math.round(e.getBoundingClientRect().top + scrollY), Math.round(e.getBoundingClientRect().height)]))));
await b.close();
