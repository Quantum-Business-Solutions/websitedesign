// Where Chromium is. The Claude Code Remote environment keeps a pinned build under /opt/pw-browsers (the revision in
// the folder name changes with the image, so it is found, not hard-coded); GitHub Actions installs one with
// `npx playwright install chromium`, which Playwright finds on its own. PW_CHROME overrides both.
import fs from 'node:fs';
import path from 'node:path';
const ROOT = '/opt/pw-browsers';
function pinned() {
  let dirs = [];
  try { dirs = fs.readdirSync(ROOT).filter(d => /^chromium-\d+$/.test(d)).sort().reverse(); } catch { return undefined; }
  for (const d of dirs) for (const sub of ['chrome-linux64', 'chrome-linux']) {
    const p = path.join(ROOT, d, sub, 'chrome');
    if (fs.existsSync(p)) return p;
  }
  return undefined;
}
export const chromePath = () => process.env.PW_CHROME || pinned();
// Launch options every helper shares: the found browser, and the session's outbound proxy when there is one (so web
// fonts load in a sandbox that reaches the network only through it).
export const launchOpts = () => ({
  executablePath: chromePath(), args: ['--headless=new', '--no-sandbox'],
  ...(process.env.HTTPS_PROXY ? { proxy: { server: process.env.HTTPS_PROXY } } : {}),
});
