import { chromium } from 'playwright'; import fs from 'fs';
// node _fitpng.mjs in.png out.png maxW : scale keeping alpha, trim transparent margins
const [inp, out, maxW] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--headless=new','--no-sandbox'] });
const p = await b.newPage(); const data = 'data:image/png;base64,' + fs.readFileSync(inp).toString('base64');
const r = await p.evaluate(async ([d, mw]) => { const img = new Image(); img.src = d; await img.decode();
  const c0 = document.createElement('canvas'); c0.width = img.naturalWidth; c0.height = img.naturalHeight; const x0 = c0.getContext('2d'); x0.drawImage(img, 0, 0);
  const px = x0.getImageData(0, 0, c0.width, c0.height).data; let minx = c0.width, miny = c0.height, maxx = 0, maxy = 0;
  for (let y = 0; y < c0.height; y += 2) for (let x = 0; x < c0.width; x += 2) { if (px[(y * c0.width + x) * 4 + 3] > 20) { if (x < minx) minx = x; if (x > maxx) maxx = x; if (y < miny) miny = y; if (y > maxy) maxy = y; } }
  const pad = 24; minx = Math.max(0, minx - pad); miny = Math.max(0, miny - pad); maxx = Math.min(c0.width, maxx + pad); maxy = Math.min(c0.height, maxy + pad);
  const w0 = maxx - minx, h0 = maxy - miny; const side = Math.max(w0, h0); const s = Math.min(1, mw / side); const W = Math.round(side * s);
  const c = document.createElement('canvas'); c.width = W; c.height = W; const ctx = c.getContext('2d');
  ctx.drawImage(c0, minx, miny, w0, h0, Math.round((side - w0) / 2 * s), Math.round((side - h0) * s), Math.round(w0 * s), Math.round(h0 * s));
  return JSON.stringify({ d: c.toDataURL('image/png'), W }); }, [data, +maxW]);
const j = JSON.parse(r); fs.writeFileSync(out, Buffer.from(j.d.split(',')[1], 'base64')); console.log(out, j.W, fs.statSync(out).size); await b.close();
