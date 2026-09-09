import { chromium } from 'playwright'; import fs from 'fs';
import { chromePath } from './_chrome.mjs';
// node _sheet.mjs out.jpg cols tile in1.png in2.png ... : contact sheet on white
const [out, cols, tile, ...ins] = process.argv.slice(2);
const c = +cols, t = +tile, rows = Math.ceil(ins.length / c);
const b = await chromium.launch({ executablePath: chromePath(), args: ['--headless=new','--no-sandbox'] });
const p = await b.newPage({ viewport: { width: c * t, height: rows * t } });
const imgs = ins.map((f, i) => `<img src="data:image/png;base64,${fs.readFileSync(f).toString('base64')}" style="position:absolute;left:${(i % c) * t}px;top:${Math.floor(i / c) * t}px;width:${t}px;height:${t}px;object-fit:contain">`).join('');
await p.setContent(`<body style="margin:0;background:#fff">${imgs}</body>`);
await p.screenshot({ path: out, type: 'jpeg', quality: 85 }); await b.close(); console.log('sheet', out);
