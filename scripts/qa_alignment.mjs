// Alignment check: a row of items (badges, dot-separated lists, button groups, stat strips) must sit on the same
// axis as the text around it. Flags a row whose items do not span the container and whose centre is off the
// container centre while a neighbour above or below it is centred. This is the "red dots not centred" defect.
//
// Usage: node scripts/qa_alignment.mjs <url-or-file.html> [...]   (file paths are opened as file://)
// Exit code 1 if anything is flagged, so the gate can fail on it.
import { chromium } from 'playwright';
import { chromePath } from './_chrome.mjs';
import path from 'path';

const targets = process.argv.slice(2);
if (!targets.length) { console.error('usage: node scripts/qa_alignment.mjs <url-or-file> ...'); process.exit(2); }
const TOL = 6; // px
const b = await chromium.launch({ executablePath: chromePath(), args: ['--headless=new', '--no-sandbox'] });
let bad = 0;
for (const t of targets) {
  const url = /^https?:|^file:/.test(t) ? t : 'file://' + path.resolve(t);
  for (const w of [1440, 390]) {
    const ctx = await b.newContext({ viewport: { width: w, height: 900 } });
    const page = await ctx.newPage();
    await page.route(/fonts\.(googleapis|gstatic)\.com/, r => r.abort());
    await page.goto(url, { waitUntil: 'load' });
    await page.waitForTimeout(500);
    await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 700) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 40)); } window.scrollTo(0, 0); });
    const found = await page.evaluate((TOL) => {
      const out = [];
      const centred = el => el && getComputedStyle(el).textAlign === 'center';
      const vis = el => { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0 && getComputedStyle(el).visibility !== 'hidden'; };
      for (const row of document.querySelectorAll('body *')) {
        const cs = getComputedStyle(row);
        if (!/flex|grid/.test(cs.display) || row.children.length < 2 || !vis(row)) continue;
        if (row.closest('nav, header, footer, [role=tablist], .pv-mega')) continue;
        if (/auto|scroll/.test(cs.overflowX) || /auto|scroll/.test(getComputedStyle(row.parentElement).overflowX)) continue; // sideways scrollers are meant to start at the left
        const kids = [...row.children].filter(vis);
        if (kids.length < 2) continue;
        const rr = row.getBoundingClientRect();
        // A list that has collapsed to one column (every item on its own line, same left edge) is a stack, not a row:
        // a timeline with a rail down its left side is meant to be inset. Rows are what this check is about.
        if (/^(OL|UL)$/.test(row.tagName)) {
          const ls = kids.map(k => Math.round(k.getBoundingClientRect().left)), ts = kids.map(k => Math.round(k.getBoundingClientRect().top));
          if (new Set(ls).size === 1 && new Set(ts).size === kids.length) continue;
        }
        const left = Math.min(...kids.map(k => k.getBoundingClientRect().left));
        const right = Math.max(...kids.map(k => k.getBoundingClientRect().right));
        const cw = rr.width, uw = right - left;
        if (uw >= cw * 0.9) continue;            // items span the row: nothing to centre
        if (uw < 40) continue;
        const offset = (left + right) / 2 - (rr.left + rr.right) / 2;
        if (Math.abs(offset) <= TOL) continue;   // centred
        // Is the neighbourhood centred? Look at the row's own text-align and at siblings above and below.
        const near = [];
        // Neighbours only count inside the same section: a centred hero above must not make a left-aligned section below it a defect.
        const scope = row.closest('section') || document.body;
        let p = row;
        for (let i = 0; i < 3 && p && p !== scope; i++, p = p.parentElement) {
          for (const sib of [p.previousElementSibling, p.nextElementSibling]) if (sib && scope.contains(sib)) near.push(sib, ...sib.querySelectorAll('h1,h2,h3,p'));
        }
        const centredNeighbour = near.some(n => vis(n) && centred(n) && n.textContent.trim().length > 3);
        if (centred(row) || centredNeighbour) {
          out.push({ row: row.className || row.tagName, text: kids.map(k => k.textContent.trim()).join(' | ').slice(0, 80), offset: Math.round(offset), left: Math.round(left - rr.left), right: Math.round(rr.right - right) });
        }
      }
      return out;
    }, TOL);
    for (const f of found) { bad++; console.log(`FLAG ${t} @${w}: row "${f.row}" is off-centre by ${f.offset}px (space left ${f.left}px, right ${f.right}px): ${f.text}`); }
    await ctx.close();
  }
}
await b.close();
console.log(bad ? `${bad} alignment problem(s)` : 'alignment: all rows sit on the axis of their neighbours');
process.exit(bad ? 1 : 0);
