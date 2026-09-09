import { chromium } from 'playwright';
import { chromePath } from './_chrome.mjs';
// node _axerule.mjs <file.html> <ruleId> : failing nodes for one rule, grouped by selector shape with the contrast data
const [file, rule] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: chromePath(), args: ['--headless=new','--no-sandbox'] });
const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
await p.route(/fonts\.(googleapis|gstatic)\.com/, r => r.abort());
await p.goto('file://' + file); await p.addScriptTag({ path: '/home/user/websitedesign/node_modules/axe-core/axe.min.js' });
const r = await p.evaluate(async (rule) => { const res = await axe.run(document, { runOnly: [rule] }); const g = {}; for (const v of res.violations) for (const n of v.nodes) { const k = n.target[0].replace(/:nth-child\(\d+\)/g, ''); const d = n.any[0]?.data || {}; (g[k] = g[k] || { n: 0, ex: n.html.slice(0, 120), fg: d.fgColor, bg: d.bgColor, ratio: d.contrastRatio, need: d.expectedContrastRatio }).n++; } return g; }, rule);
console.log(JSON.stringify(r, null, 1)); await b.close();
