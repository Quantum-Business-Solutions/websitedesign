// 10/10 page gate: one Playwright pass per page at desktop and mobile, scored against the design guardrails.
// node scripts/vaf_page_scorecard.cjs <base-url> <slugs.json> <out.json> [concurrency]
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const [base, slugFile, out, conc = '4'] = process.argv.slice(2);
  const slugs = JSON.parse(fs.readFileSync(slugFile));
  const b = await chromium.launch();
  const results = [];
  const check = async (slug) => {
    const url = base + '/' + slug + '?sc=' + Date.now();
    const r = { slug, score: 10, issues: [] };
    const hit = (pts, msg) => { r.score -= pts; r.issues.push(msg); };
    for (const [label, w, h] of [['d', 1360, 900], ['m', 390, 844]]) {
      const pg = await b.newPage({ viewport: { width: w, height: h } });
      const cons = [], bad = [];
      pg.on('console', m => { if (m.type() === 'error') cons.push(m.text().slice(0, 100)); });
      pg.on('response', x => { if (x.status() >= 400 && !/favicon|hs-analytics|hubspot\.com|hsforms|hscollectedforms|hs-banner/.test(x.url())) bad.push(x.status() + ' ' + x.url().slice(-70)); });
      const resp = await pg.goto(url, { waitUntil: 'networkidle', timeout: 60000 }).catch(() => null);
      if (!resp || resp.status() !== 200) { hit(10, label + ': status ' + (resp && resp.status())); await pg.close(); continue; }
      await pg.evaluate(async () => { for (let y = 0; y < document.documentElement.scrollHeight; y += 700) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 40)); } window.scrollTo(0, 0); });
      await pg.waitForTimeout(500);
      const info = await pg.evaluate(() => {
        const lines = el => { const cs = getComputedStyle(el), lh = parseFloat(cs.lineHeight) || parseFloat(cs.fontSize) * 1.2; return Math.round(el.getBoundingClientRect().height / lh); };
        const heads = [...document.querySelectorAll('h1,h2,h3')].filter(e => e.offsetParent);
        const secs = [...document.querySelectorAll('main section, section')].filter(e => e.offsetHeight > 80);
        const sig = secs.map(s => (s.className.match(/vaf-[a-z0-9]+/) || [''])[0] + '|' + (s.className.match(/flip|alt|q-bg-alt/g) || []).join(''));
        let adj = 0; for (let i = 1; i < sig.length; i++) if (sig[i].split('|')[0] && sig[i] === sig[i - 1]) adj++;
        const imgs = [...document.images].filter(i => i.offsetParent);
        const tiny = [...document.querySelectorAll('p,li,a,span')].filter(e => e.offsetParent && e.children.length === 0 && e.textContent.trim().length > 20 && parseFloat(getComputedStyle(e).fontSize) < 13).length;
        return {
          overflowX: document.documentElement.scrollWidth > innerWidth + 2,
          brokenImgs: imgs.filter(i => i.complete && i.naturalWidth === 0).length,
          noAlt: imgs.filter(i => i.getAttribute('alt') === null).length,
          h1: document.querySelectorAll('h1').length,
          wraps: heads.filter(e => lines(e) >= 4).length,
          adjSame: adj, sections: secs.length, tiny,
          orphanCards: [...document.querySelectorAll('.vc__grid')].filter(g => { const k = [...g.children]; if (k.length < 4) return false; const tops = k.map(c => Math.round(c.getBoundingClientRect().top)); const last = tops[tops.length - 1]; return tops.filter(t => t === last).length === 1; }).length,
          emptyForm: [...document.querySelectorAll('.hs_cos_wrapper_type_form')].filter(e => !e.querySelector('form,iframe')).length,
          words: (document.body.innerText.match(/\w+/g) || []).length,
          rawHubl: /\{\{|\{%/.test(document.body.innerText),
        };
      });
      if (info.overflowX) hit(2, label + ': horizontal overflow');
      if (info.brokenImgs) hit(1, label + ': ' + info.brokenImgs + ' broken images');
      if (info.h1 !== 1) hit(1, label + ': ' + info.h1 + ' h1');
      if (info.wraps) hit(1, label === 'd' ? 'desktop: ' + info.wraps + ' headings wrap to 4+ lines' : null);
      if (label === 'd' && info.adjSame > 1) hit(1, info.adjSame + ' adjacent sections share a layout');
      if (label === 'd' && info.orphanCards) hit(1, 'card grid leaves a single orphan');
      if (info.emptyForm) hit(1, label + ': form did not render');
      if (info.rawHubl) hit(2, label + ': raw HubL visible');
      if (label === 'd' && info.words < 250) hit(1, 'thin page (' + info.words + ' words)');
      if (label === 'd' && info.noAlt > 0) hit(0.5, info.noAlt + ' images missing alt attribute');
      if (bad.length) hit(1, label + ': failed requests ' + [...new Set(bad)].slice(0, 2).join('; '));
      if (cons.length) hit(0.5, label + ': console errors ' + cons[0]);
      await pg.close();
    }
    r.issues = r.issues.filter(Boolean); r.score = Math.max(0, Math.round(r.score * 2) / 2);
    return r;
  };
  const q = [...slugs]; const n = +conc;
  await Promise.all(Array.from({ length: n }, async () => { while (q.length) { const s = q.shift(); try { results.push(await check(s)); } catch (e) { results.push({ slug: s, score: 0, issues: ['crash ' + e.message.slice(0, 80)] }); } } }));
  results.sort((a, b) => a.score - b.score);
  fs.writeFileSync(out, JSON.stringify(results, null, 1));
  const dist = {}; results.forEach(r => dist[r.score] = (dist[r.score] || 0) + 1);
  console.log('distribution', JSON.stringify(dist));
  results.filter(r => r.score < 10).slice(0, 40).forEach(r => console.log(r.score, r.slug || '/', '|', r.issues.join(' ; ')));
  await b.close();
})();
