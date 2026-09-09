// Where Chromium is. The Claude Code Remote environment keeps a pinned build under /opt/pw-browsers; GitHub
// Actions installs one with `npx playwright install chromium`, which Playwright finds on its own. PW_CHROME
// overrides both.
import fs from 'node:fs';
const PINNED = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
export const chromePath = () => process.env.PW_CHROME || (fs.existsSync(PINNED) ? PINNED : undefined);
