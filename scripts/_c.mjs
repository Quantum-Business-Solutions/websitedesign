import { chromium } from 'playwright'; import fs from 'fs';
const [inp, out, y0, y1] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--headless=new','--no-sandbox'] });
const p = await b.newPage(); const data = 'data:image/png;base64,' + fs.readFileSync(inp).toString('base64');
const res = await p.evaluate(async ([d, y0, y1]) => { const img = new Image(); img.src = d; await img.decode(); const w = img.naturalWidth, h = Math.min(+y1, img.naturalHeight) - (+y0); const c = document.createElement('canvas'); c.width = w; c.height = h; c.getContext('2d').drawImage(img, 0, +y0, w, h, 0, 0, w, h); return JSON.stringify({ d: c.toDataURL('image/jpeg', 0.8), W: img.naturalWidth, H: img.naturalHeight }); }, [data, y0, y1]);
const r = JSON.parse(res); fs.writeFileSync(out, Buffer.from(r.d.split(',')[1], 'base64')); console.log(r.W, r.H); await b.close();
