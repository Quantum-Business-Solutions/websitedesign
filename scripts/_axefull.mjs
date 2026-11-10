import { chromium } from 'playwright';
import { chromePath } from './_chrome.mjs';
const [file] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: chromePath(), args: ['--headless=new', '--no-sandbox'] });
// Motion reduced, so every scroll reveal is in and nothing is measured halfway through a fade (a reveal starts at
// opacity 0: axe would skip what has not scrolled in and fail what is mid-transition).
const p = await b.newPage({ viewport: { width: 1280, height: 900 }, reducedMotion: 'reduce' });
await p.route(/fonts\.(googleapis|gstatic)\.com/, r => r.abort());
await p.goto('file://' + file); await p.waitForTimeout(700); await p.addScriptTag({ path: '/home/user/websitedesign/node_modules/axe-core/axe.min.js' });
const r = await p.evaluate(async () => { const res = await axe.run(document); return res.violations.map(v => ({ id: v.id, impact: v.impact, n: v.nodes.length, first: v.nodes[0].html.slice(0, 160) })); });
console.log(JSON.stringify(r, null, 1)); await b.close();
