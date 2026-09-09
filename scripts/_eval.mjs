import { chromium } from 'playwright';
import { chromePath } from './_chrome.mjs';
// node _eval.mjs <file.html> "<js expression>"
const [file, expr] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: chromePath(), args: ['--headless=new','--no-sandbox'] });
const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
await p.route(/fonts\.(googleapis|gstatic)\.com|ajax\.googleapis\.com/, r => r.abort());
p.on('pageerror', e => console.log('PAGEERROR', e.message));
await p.goto('file://' + file); await p.waitForTimeout(800);
console.log(JSON.stringify(await p.evaluate(expr))); await b.close();
