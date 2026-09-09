import { chromium } from 'playwright'; import fs from 'fs';
import { chromePath } from './_chrome.mjs';
// node _resize.mjs in.png outbase   -> outbase-1200.jpg (1200x800 cover) and outbase-600.jpg
const [inp, outb] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: chromePath(), args: ['--headless=new','--no-sandbox'] });
const p = await b.newPage();
const data = 'data:image/png;base64,' + fs.readFileSync(inp).toString('base64');
for (const [w, h] of [[1200, 800], [600, 400]]) {
  const out = await p.evaluate(async ([d, w, h]) => { const img = new Image(); img.src = d; await img.decode(); const c = document.createElement('canvas'); c.width = w; c.height = h; const ctx = c.getContext('2d'); const s = Math.max(w / img.naturalWidth, h / img.naturalHeight); const sw = w / s, sh = h / s; ctx.drawImage(img, (img.naturalWidth - sw) / 2, (img.naturalHeight - sh) / 2, sw, sh, 0, 0, w, h); return c.toDataURL('image/jpeg', 0.84); }, [data, w, h]);
  fs.writeFileSync(`${outb}-${w}.jpg`, Buffer.from(out.split(',')[1], 'base64'));
}
await b.close();
