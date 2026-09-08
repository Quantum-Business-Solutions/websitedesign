import { chromium } from 'playwright';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--headless=new','--no-sandbox'] });
const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
await p.route(/fonts\.(googleapis|gstatic)\.com/, r => r.abort());
await p.goto('file:///home/user/vanausdall/index.html'); await p.waitForTimeout(400);
const first = p.locator('#alist article').first(); await first.scrollIntoViewIfNeeded(); await p.waitForTimeout(400);
const box = await first.boundingBox(); const box3 = await p.locator('#alist article').nth(2).boundingBox();
await p.screenshot({ path: '/tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa/cards2-top.jpg', type: 'jpeg', quality: 80, fullPage: true, clip: { x: box.x - 8, y: box.y - 8, width: box.width + 16, height: (box3.y + box3.height) - box.y + 16 } });
await b.close(); console.log('ok');
