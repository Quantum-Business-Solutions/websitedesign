import { chromium } from 'playwright'; import fs from 'fs';
import { chromePath } from './_chrome.mjs';
// node _axe.mjs <file.html> <ruleId> : print nodes failing one axe rule
const [file, rule] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: chromePath(), args: ['--headless=new','--no-sandbox'] });
const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
await p.route(/fonts\.(googleapis|gstatic)\.com|ajax\.googleapis\.com/, r => r.abort());
await p.goto('file://' + file); await p.addScriptTag({ path: 'node_modules/axe-core/axe.min.js' });
const r = await p.evaluate(async (rule) => { const res = await axe.run(document, { runOnly: [rule] }); return res.violations.map(v => v.nodes.map(n => ({ target: n.target, html: n.html.slice(0, 300) }))); }, rule);
console.log(JSON.stringify(r, null, 1)); await b.close();
