import { chromium } from 'playwright';
const [file] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--headless=new','--no-sandbox'] });
const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
await p.route(/fonts\.(googleapis|gstatic)\.com/, r => r.abort());
await p.goto('file://' + file); await p.addScriptTag({ path: '/home/user/websitedesign/node_modules/axe-core/axe.min.js' });
const r = await p.evaluate(async () => { const res = await axe.run(document); return res.violations.map(v => ({ id: v.id, impact: v.impact, n: v.nodes.length, first: v.nodes[0].html.slice(0, 160) })); });
console.log(JSON.stringify(r, null, 1)); await b.close();
