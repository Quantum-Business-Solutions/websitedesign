// Playwright QA for built pages: desktop + mobile screenshots, broken images, failed requests, horizontal overflow, empty forms.
// node scripts/qa_pages.js <base-url> <out-dir> /path1 /path2 ...
const { chromium } = require('playwright');
(async () => {
  const [base, outdir, ...paths] = process.argv.slice(2);
  const b = await chromium.launch();
  const report = [];
  for (const [label, w, h] of [['d',1360,900],['m',390,844]]) {
    for (const p of paths) {
      const pg = await b.newPage({ viewport: { width: w, height: h } });
      const fails = [], cons = [];
      pg.on('requestfailed', r => fails.push(r.url().slice(0,100)));
      pg.on('response', r => { if (r.status()>=400) fails.push(r.status()+' '+r.url().slice(0,100)); });
      pg.on('console', m => { if (m.type()==='error') cons.push(m.text().slice(0,120)); });
      await pg.goto(base+p, { waitUntil: 'networkidle', timeout: 60000 }).catch(()=>{});
      await pg.evaluate(async()=>{for(let y=0;y<document.documentElement.scrollHeight;y+=600){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,60))}window.scrollTo(0,0)});
      await pg.waitForTimeout(1200);
      const info = await pg.evaluate(() => {
        const imgs=[...document.images]; 
        return { h: document.documentElement.scrollHeight, overflowX: document.documentElement.scrollWidth > innerWidth+2,
          brokenImgs: imgs.filter(i=>i.complete && i.naturalWidth===0).map(i=>i.src.slice(-60)),
          imgs: imgs.length, sections: document.querySelectorAll('section').length,
          emptyForm: [...document.querySelectorAll('.hs_cos_wrapper_type_form')].filter(e=>!e.querySelector('form,iframe')).length };
      });
      const name = (p.replace(/\W+/g,'_')||'home')+'_'+label;
      const S = label==='d'?1800:2400;
      let i=0; for (let y=0;y<info.h;y+=S,i++) await pg.screenshot({ path:`${outdir}/${name}_${i}.png`, fullPage:true, clip:{x:0,y,width:w,height:Math.min(S,info.h-y)} });
      report.push({ page:p, vp:label, ...info, slices:i, fails:[...new Set(fails)].slice(0,6), cons:[...new Set(cons)].slice(0,3) });
      await pg.close();
    }
  }
  console.log(JSON.stringify(report,null,1));
  await b.close();
})();
