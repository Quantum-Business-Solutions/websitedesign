import { chromium } from 'playwright';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--headless=new','--no-sandbox'] });
const ctx = await b.newContext({ viewport: { width: 1280, height: 900 }, userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36' });
const targets = { linkedin: 'https://www.linkedin.com/company/van-ausdall-&-farrar', facebook: 'https://www.facebook.com/Vanausdallinc/', instagram: 'https://www.instagram.com/vanausdallinc/', youtube: 'https://www.youtube.com/results?search_query=van+ausdall+farrar' };
for (const [k, u] of Object.entries(targets)) {
  const p = await ctx.newPage();
  try {
    const r = await p.goto(u, { waitUntil: 'domcontentloaded', timeout: 25000 });
    await p.waitForTimeout(2500);
    const title = await p.title(); const url = p.url();
    const txt = (await p.evaluate(() => document.body.innerText)).replace(/\s+/g, ' ').slice(0, 1500);
    const desc = await p.evaluate(() => (document.querySelector('meta[property="og:description"], meta[name="description"]') || {}).content || '');
    console.log(`== ${k} status=${r && r.status()} final=${url}\n title: ${title}\n desc: ${desc}\n text: ${txt.slice(0, 700)}\n`);
    await p.screenshot({ path: `/tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa/social-${k}.jpg`, type: 'jpeg', quality: 60 });
  } catch (e) { console.log(`== ${k} ERROR ${e.message.split('\n')[0]}`); }
  await p.close();
}
await b.close();
