import { chromium } from 'playwright'; import fs from 'fs';
// node _fit.mjs in.png out.jpg maxW  -> scaled to maxW keeping aspect
const [inp, out, maxW] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--headless=new','--no-sandbox'] });
const p = await b.newPage(); const data = 'data:image/png;base64,' + fs.readFileSync(inp).toString('base64');
const r = await p.evaluate(async ([d, mw]) => { const img = new Image(); img.src = d; await img.decode(); const s = Math.min(1, mw / img.naturalWidth); const w = Math.round(img.naturalWidth * s), h = Math.round(img.naturalHeight * s); const c = document.createElement('canvas'); c.width = w; c.height = h; c.getContext('2d').drawImage(img, 0, 0, w, h); return JSON.stringify({ d: c.toDataURL('image/jpeg', 0.84), w, h }); }, [data, +maxW]);
const j = JSON.parse(r); fs.writeFileSync(out, Buffer.from(j.d.split(',')[1], 'base64')); console.log(out, j.w, j.h); await b.close();
