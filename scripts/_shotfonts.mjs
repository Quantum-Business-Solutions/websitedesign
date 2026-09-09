import { chromium } from 'playwright';
import { chromePath } from './_chrome.mjs';
// like _shot.mjs but lets Google Fonts load, to judge type
const [file, w, sel, out] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: chromePath(), args: ['--headless=new','--no-sandbox'] });
const p = await b.newPage({ viewport: { width: +w, height: 900 } });
await p.goto('file://' + file, { waitUntil: 'load', timeout: 60000 }).catch(()=>{}); await p.waitForTimeout(2500);
const el = p.locator(sel).first(); await el.scrollIntoViewIfNeeded(); await p.waitForTimeout(1200);
await el.screenshot({ path: out, type: 'jpeg', quality: 80 }); await b.close(); console.log(out);
