// Downscale the top of a full-page PNG into a hub thumbnail. node scripts/preview_thumb.mjs in.png out.jpg 900 720
import { chromium } from 'playwright'; import fs from 'fs';
// node _thumb.mjs in.png out.jpg srcH outW : top srcH px of the image, downscaled to outW wide
const [inp, out, srcH, outW] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--headless=new','--no-sandbox'] });
const p = await b.newPage();
const data = 'data:image/png;base64,' + fs.readFileSync(inp).toString('base64');
const res = await p.evaluate(async ([d, srcH, outW]) => {
  const img = new Image(); img.src = d; await img.decode();
  const sw = img.naturalWidth, sh = Math.min(+srcH, img.naturalHeight), k = (+outW) / sw;
  const c = document.createElement('canvas'); c.width = +outW; c.height = Math.round(sh * k);
  const g = c.getContext('2d'); g.imageSmoothingQuality = 'high'; g.drawImage(img, 0, 0, sw, sh, 0, 0, c.width, c.height);
  return c.toDataURL('image/jpeg', 0.86);
}, [data, srcH, outW]);
fs.writeFileSync(out, Buffer.from(res.split(',')[1], 'base64'));
await b.close();
