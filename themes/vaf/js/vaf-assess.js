/* VAF Technology Strength Assessment.
   Mounts on #assess (the sample checklist section) of the assessment page, or on any [data-vaf-assessment] element.
   Questions, fixes and score bands are read from HubDB (editable as a spreadsheet in HubSpot); the copy below is the fallback.
   Results show on the page after the email form is submitted, can be reopened from #r=<code>, and download as a PDF. */
(function () {
  'use strict';
  var CFG = {
    portal: '50498425',
    form: 'e84ef7ce-04f2-4fef-b539-4351bde13b48',
    questionsTable: '451332876',     // HubDB table id, filled in after the table is created
    settingsTable: '450036142',
    phone: '(317) 634-2913',
    consultUrl: '/contact',
    site: 'vanausdall.com'
  };
  var AREAS = ['Information', 'Print', 'Process', 'Communication'];
  var AREA_INTRO = {
    Information: 'Networks, devices, backups and security: who watches them, and whether anyone owns the roadmap.',
    Print: 'Devices, supplies and spend: what a page really costs and who handles the repairs.',
    Process: 'Where paper still lives, which approvals wait in an inbox, and what your records retention really is.',
    Communication: 'Phones, internet and collaboration: what happens on the day something fails.'
  };
  var BANK = [
    ['Information', 'We run vulnerability scans on a regular schedule.', 'optimize', 'Put recurring vulnerability scans on the calendar and track what they find to closure.'],
    ['Information', 'Multi-factor authentication is on for administrator and user accounts.', 'eliminate', 'Turn on MFA for every administrator and user account. It closes the most common way accounts are taken over.'],
    ['Information', 'Server data is backed up nightly, with a copy off site or in the cloud.', 'eliminate', 'Add a nightly backup with an off-site or cloud copy so one failure cannot take your data with it.'],
    ['Information', 'We test that our backups actually restore.', 'optimize', 'Schedule restore tests. A backup nobody has restored is a hope, not a plan.'],
    ['Information', 'We have a written disaster recovery plan that is reviewed once or twice a year.', 'leverage', 'Write the disaster recovery plan down, name an owner and review it twice a year.'],
    ['Print', 'We know what we spend each year on printer supplies and service.', 'optimize', 'Put supplies, service and device costs in one report. Most offices find they are paying for the same printing more than once.'],
    ['Print', 'Our multifunction printers require users to sign in before releasing a print job.', 'eliminate', 'Require sign-in at the device so sensitive pages are never left in an output tray.'],
    ['Print', 'One team owns our printer fleet and sees device reporting in one place.', 'optimize', 'Give the fleet one owner and one dashboard so repairs and toner stop being a scramble.'],
    ['Print', 'Unclaimed print jobs are held, not printed and abandoned.', 'eliminate', 'Hold jobs until the owner is at the device. It cuts waste and keeps documents private.'],
    ['Print', 'We have a replacement plan for devices that are past their service life.', 'leverage', 'List every device by age and plan replacements before the repairs outweigh the cost.'],
    ['Process', 'We have a formal records retention schedule and we follow it.', 'eliminate', 'Adopt a retention schedule. Keeping everything forever is a cost and a legal risk.'],
    ['Process', 'Our documents live in one central, searchable repository.', 'optimize', 'Move documents into one searchable repository so nobody hunts through drives and inboxes.'],
    ['Process', 'Invoices, approvals and HR forms run through a workflow, not a paper trail or an inbox.', 'leverage', 'Automate the approvals that wait longest. They are usually the cheapest wins.'],
    ['Process', 'Paper records are scanned and securely destroyed on a schedule.', 'optimize', 'Scan, index and shred on a schedule. The paper stops growing and the records become findable.'],
    ['Process', 'Visitor and package tracking is digital.', 'leverage', 'Move visitor and package logs off the clipboard so they are searchable and auditable.'],
    ['Communication', 'Our phone system has a documented disaster recovery plan.', 'eliminate', 'Plan where calls go when the phone system or the internet fails, and test it.'],
    ['Communication', 'Staff can take office calls on a smartphone or laptop from anywhere.', 'leverage', 'Let the office number follow people to the field and home on any device.'],
    ['Communication', 'The office has internet redundancy, so one outage does not stop work.', 'eliminate', 'Add a second internet path so a single outage does not take phones and cloud tools down.'],
    ['Communication', 'Calls are recorded wherever compliance requires it.', 'optimize', 'Turn on call recording where rules require it, with retention and access controls.'],
    ['Communication', 'Our chat, video and phone tools are connected to each other.', 'leverage', 'Connect phone, chat and video so a conversation can move between them without friction.']
  ].map(function (r) { return { area: r[0], q: r[1], bucket: r[2], fix: r[3], w: 1 }; });
  var COPY = {
    title: 'Take the Technology Strength Assessment',
    lead: 'Twenty yes or no questions across four areas. About five minutes. You get a score, a short eliminate, optimize and leverage roadmap, and a PDF.',
    formTitle: 'Where should we send your results?',
    formNote: 'A person from the Indianapolis office reviews your answers and can walk the office with you. We use your details only to respond to this request.',
    submit: 'Show my results',
    bands: [[0, 'Exposed', 'Several basics are missing. The first fixes will pay back quickly.'], [40, 'Developing', 'You have a foundation. The gaps below are where to focus next.'], [70, 'Strong', 'A solid base. The roadmap below is about leverage and keeping it that way.']],
    cta: 'Schedule a consultation',
    ctaNote: 'The full assessment has about eighty questions. A specialist can walk your office and confirm every answer.'
  };

  var ST = { i: 0, ans: {}, view: 'intro', bank: BANK, copy: COPY, code: '', lead: null };
  var root;

  function el(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function val(v) { return v && typeof v === 'object' && 'name' in v ? v.name : v; }

  /* ---------- data ---------- */
  function loadHubDb(cb) {
    if (!CFG.questionsTable) return cb();
    var base = 'https://api.hubapi.com/cms/v3/hubdb/tables/';
    fetch(base + CFG.questionsTable + '/rows?portalId=' + CFG.portal + '&limit=200&sort=sort').then(function (r) { return r.ok ? r.json() : Promise.reject(); }).then(function (j) {
      var rows = (j.results || []).map(function (r) { var v = r.values || {}; return { area: String(val(v.area) || ''), q: String(val(v.question) || ''), bucket: String(val(v.bucket) || 'optimize').toLowerCase(), fix: String(val(v.fix) || ''), w: parseFloat(val(v.weight)) || 1, sort: parseFloat(val(v.sort)) || 0 }; })
        .filter(function (r) { return r.q && AREAS.indexOf(r.area) > -1; });
      if (rows.length >= 4) ST.bank = rows;
    }).catch(function () { }).then(function () {
      if (!CFG.settingsTable) return;
      return fetch(base + CFG.settingsTable + '/rows?portalId=' + CFG.portal + '&limit=100').then(function (r) { return r.ok ? r.json() : Promise.reject(); }).then(function (j) {
        (j.results || []).forEach(function (r) {
          var v = r.values || {}; var k = String(val(v.key) || ''), t = String(val(v.value) || '');
          if (!k || !t) return;
          if (k.indexOf('area_') === 0 && AREAS.indexOf(k.slice(5)) > -1) AREA_INTRO[k.slice(5)] = t;
          else if (k.indexOf('band_') === 0) { var bi = parseInt(k.slice(5), 10), parts = t.split('|'); if (ST.copy.bands[bi] && parts.length >= 2) ST.copy.bands[bi] = [ST.copy.bands[bi][0], parts[0].trim(), parts.slice(1).join('|').trim()]; }
          else if (k in COPY && typeof COPY[k] === 'string') ST.copy[k] = t;
        });
      }).catch(function () { });
    }).then(cb);
  }

  /* ---------- scoring ---------- */
  function areaQs(a) { return ST.bank.filter(function (r) { return r.area === a; }); }
  function key(r) { return ST.bank.indexOf(r); }
  function score() {
    var per = {}, tot = 0, max = 0;
    AREAS.forEach(function (a) {
      var qs = areaQs(a), got = 0, m = 0;
      qs.forEach(function (r) { var w = r.w || 1; m += w; if (ST.ans[key(r)] === 1) got += w; });
      per[a] = m ? Math.round(100 * got / m) : 0; tot += got; max += m;
    });
    return { per: per, total: max ? Math.round(100 * tot / max) : 0 };
  }
  function band(n) { var b = ST.copy.bands[0]; ST.copy.bands.forEach(function (x) { if (n >= x[0]) b = x; }); return b; }
  function roadmap() {
    var out = { eliminate: [], optimize: [], leverage: [] };
    ST.bank.forEach(function (r) { if (ST.ans[key(r)] !== 1) (out[r.bucket] || out.optimize).push(r); });
    return out;
  }
  /* answers <-> short code, so a results link can be reopened */
  function encode() { return ST.bank.map(function (r, i) { return ST.ans[i] === 1 ? '1' : '0'; }).join(''); }
  function decode(c) { var a = {}; for (var i = 0; i < ST.bank.length; i++) a[i] = c.charAt(i) === '1' ? 1 : 0; return a; }

  /* ---------- views ---------- */
  function draw() {
    root.innerHTML = '';
    var wrap = el('div', 'va');
    if (ST.view === 'intro') wrap.appendChild(viewIntro());
    else if (ST.view === 'q') wrap.appendChild(viewQ());
    else if (ST.view === 'form') wrap.appendChild(viewForm());
    else wrap.appendChild(viewResults());
    root.appendChild(wrap);
  }
  function head(step) {
    var h = el('div', 'va__top');
    var steps = el('ol', 'va__steps');
    AREAS.concat(['Results']).forEach(function (a, i) { var li = el('li', i < step ? 'is-done' : (i === step ? 'is-on' : ''), '<b>' + (i + 1) + '</b><span>' + esc(a) + '</span>'); steps.appendChild(li); });
    h.appendChild(steps);
    var bar = el('div', 'va__bar'); var f = el('i'); f.style.width = Math.round(100 * step / 5) + '%'; bar.appendChild(f); h.appendChild(bar);
    return h;
  }
  function viewIntro() {
    var d = el('div', 'va__card va__intro');
    d.appendChild(el('h2', 'va__h', esc(ST.copy.title)));
    d.appendChild(el('p', 'va__lead', esc(ST.copy.lead)));
    var g = el('div', 'va__areas');
    AREAS.forEach(function (a, i) { g.appendChild(el('div', 'va__area', '<b>' + (i + 1) + '</b><h3>' + esc(a) + '</h3><p>' + esc(AREA_INTRO[a]) + '</p>')); });
    d.appendChild(g);
    var b = el('button', 'va__btn', 'Start the assessment'); b.type = 'button'; b.onclick = function () { ST.view = 'q'; ST.i = 0; draw(); scrollTop(); };
    d.appendChild(b);
    return d;
  }
  function viewQ() {
    var a = AREAS[ST.i], qs = areaQs(a);
    var d = el('div', 'va__card');
    d.appendChild(head(ST.i));
    d.appendChild(el('h2', 'va__h', esc(a)));
    d.appendChild(el('p', 'va__lead', esc(AREA_INTRO[a])));
    qs.forEach(function (r) {
      var k = key(r);
      var row = el('div', 'va__q');
      row.appendChild(el('p', 'va__qt', esc(r.q)));
      var g = el('div', 'va__opts'); g.setAttribute('role', 'radiogroup'); g.setAttribute('aria-label', r.q);
      [['Yes', 1], ['No', 0], ['Not sure', 0.5]].forEach(function (o) {
        var b = el('button', 'va__opt' + (ST.ans[k] === (o[1] === 0.5 ? 0.5 : o[1]) && k in ST.ans ? ' is-on' : ''), o[0]); b.type = 'button'; b.setAttribute('role', 'radio');
        b.setAttribute('aria-checked', (k in ST.ans && ST.ans[k] === o[1]) ? 'true' : 'false');
        b.onclick = function () { ST.ans[k] = o[1]; Array.prototype.forEach.call(g.children, function (c) { c.classList.remove('is-on'); c.setAttribute('aria-checked', 'false'); }); b.classList.add('is-on'); b.setAttribute('aria-checked', 'true'); next.disabled = !complete(a); };
        g.appendChild(b);
      });
      row.appendChild(g); d.appendChild(row);
    });
    var nav = el('div', 'va__nav');
    var back = el('button', 'va__btn va__btn--ghost', 'Back'); back.type = 'button'; back.onclick = function () { if (ST.i === 0) { ST.view = 'intro'; } else ST.i--; draw(); scrollTop(); };
    var next = el('button', 'va__btn', ST.i === AREAS.length - 1 ? 'Finish' : 'Next: ' + AREAS[ST.i + 1]); next.type = 'button'; next.disabled = !complete(a);
    next.onclick = function () { if (ST.i === AREAS.length - 1) ST.view = 'form'; else ST.i++; draw(); scrollTop(); };
    nav.appendChild(back); nav.appendChild(next); d.appendChild(nav);
    return d;
  }
  function complete(a) { return areaQs(a).every(function (r) { return key(r) in ST.ans; }); }
  function viewForm() {
    var d = el('div', 'va__card');
    d.appendChild(head(4));
    d.appendChild(el('h2', 'va__h', esc(ST.copy.formTitle)));
    d.appendChild(el('p', 'va__lead', esc(ST.copy.formNote)));
    var f = el('form', 'va__form'); f.noValidate = true;
    f.innerHTML = '<label>First name<input name="firstname" autocomplete="given-name" required></label><label>Last name<input name="lastname" autocomplete="family-name" required></label>' +
      '<label class="va__wide">Work email<input name="email" type="email" autocomplete="email" required></label><label>Company<input name="company" autocomplete="organization" required></label><label>Phone (optional)<input name="phone" type="tel" autocomplete="tel"></label>' +
      '<p class="va__err" role="alert" hidden></p><button class="va__btn va__wide" type="submit">' + esc(ST.copy.submit) + '</button>';
    f.onsubmit = function (ev) {
      ev.preventDefault();
      var v = {}; Array.prototype.forEach.call(f.elements, function (x) { if (x.name) v[x.name] = (x.value || '').trim(); });
      var err = f.querySelector('.va__err');
      if (!v.firstname || !v.lastname || !v.company || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v.email)) { err.hidden = false; err.textContent = 'Please complete your name, company and a valid work email.'; return; }
      ST.lead = v; ST.view = 'results'; ST.code = encode();
      try { localStorage.setItem('vafAssess', JSON.stringify({ code: ST.code, lead: v })); } catch (e) { }
      submit(v); history.replaceState(null, '', '#r=' + ST.code); draw(); scrollTop();
    };
    d.appendChild(f);
    var back = el('button', 'va__btn va__btn--ghost va__btn--sm', 'Back'); back.type = 'button'; back.onclick = function () { ST.view = 'q'; ST.i = AREAS.length - 1; draw(); };
    d.appendChild(back);
    return d;
  }
  function viewResults() {
    var s = score(), b = band(s.total), rm = roadmap();
    var d = el('div', 'va__card va__res');
    d.appendChild(head(5));
    var top = el('div', 'va__score');
    top.innerHTML = '<div class="va__ring" style="--p:' + s.total + '"><b>' + s.total + '</b><span>out of 100</span></div><div><p class="va__kicker">Your Technology Strength Score</p><h2 class="va__h">' + esc(b[1]) + '</h2><p class="va__lead">' + esc(b[2]) + '</p></div>';
    d.appendChild(top);
    var bars = el('div', 'va__bars');
    AREAS.forEach(function (a) { bars.appendChild(el('div', 'va__barrow', '<span>' + esc(a) + '</span><div class="va__meter"><i style="width:' + s.per[a] + '%"></i></div><b>' + s.per[a] + '</b>')); });
    d.appendChild(bars);
    var cols = el('div', 'va__road');
    [['eliminate', 'Eliminate', 'Risk and waste to remove first'], ['optimize', 'Optimize', 'What you have, working harder'], ['leverage', 'Leverage', 'Where to grow next']].forEach(function (c) {
      var col = el('div', 'va__col va__col--' + c[0]);
      col.appendChild(el('h3', '', esc(c[1]) + ' <small>' + rm[c[0]].length + '</small>'));
      col.appendChild(el('p', 'va__sub', esc(c[2])));
      var ul = el('ul'); rm[c[0]].slice(0, 6).forEach(function (r) { ul.appendChild(el('li', '', '<b>' + esc(r.area) + '</b> ' + esc(r.fix))); });
      if (!rm[c[0]].length) ul.appendChild(el('li', 'is-none', 'Nothing here. Nice.'));
      col.appendChild(ul); cols.appendChild(col);
    });
    d.appendChild(cols);
    var act = el('div', 'va__actions');
    var pdf = el('button', 'va__btn', 'Download your PDF'); pdf.type = 'button'; pdf.onclick = function () { makePdf(s, b, rm, pdf); };
    var cta = el('a', 'va__btn va__btn--ghost', esc(ST.copy.cta)); cta.href = CFG.consultUrl;
    var again = el('button', 'va__link', 'Retake the assessment'); again.type = 'button'; again.onclick = function () { ST.ans = {}; ST.i = 0; ST.view = 'intro'; history.replaceState(null, '', location.pathname); draw(); scrollTop(); };
    act.appendChild(pdf); act.appendChild(cta); act.appendChild(again); d.appendChild(act);
    d.appendChild(el('p', 'va__note', esc(ST.copy.ctaNote)));
    return d;
  }
  function scrollTop() { var r = root.getBoundingClientRect(); window.scrollTo({ top: window.scrollY + r.top - 110, behavior: 'smooth' }); }

  /* ---------- HubSpot form submit ---------- */
  function submit(v) {
    var s = score(), rm = roadmap();
    var lines = ['Technology Strength Assessment', 'Score: ' + s.total + '/100 (' + band(s.total)[1] + ')'];
    AREAS.forEach(function (a) { lines.push(a + ': ' + s.per[a]); });
    lines.push('Eliminate: ' + rm.eliminate.map(function (r) { return r.q; }).join(' | '));
    lines.push('Optimize: ' + rm.optimize.map(function (r) { return r.q; }).join(' | '));
    lines.push('Leverage: ' + rm.leverage.map(function (r) { return r.q; }).join(' | '));
    lines.push('Results link: ' + location.origin + location.pathname + '#r=' + ST.code);
    var hutk = (document.cookie.match(/hubspotutk=([^;]+)/) || [])[1];
    var body = { submittedAt: String(Date.now()), fields: [{ name: 'firstname', value: v.firstname }, { name: 'lastname', value: v.lastname }, { name: 'email', value: v.email }, { name: 'name', value: v.company }, { name: 'phone', value: v.phone || '' }, { name: 'message', value: lines.join('\n') }],
      context: { pageUri: location.href.split('#')[0], pageName: document.title } };
    if (hutk) body.context.hutk = hutk;
    try { fetch('https://api.hsforms.com/submissions/v3/integration/submit/' + CFG.portal + '/' + CFG.form, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) }).catch(function () { }); } catch (e) { }
  }

  /* ---------- PDF ---------- */
  function loadPdfLib(cb) {
    if (window.jspdf) return cb();
    var s = document.createElement('script'); s.src = 'https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js'; s.onload = cb; s.onerror = function () { window.print(); }; document.head.appendChild(s);
  }
  function makePdf(s, b, rm, btn) {
    btn.disabled = true; var old = btn.textContent; btn.textContent = 'Preparing PDF...';
    loadPdfLib(function () {
      try {
        var J = window.jspdf.jsPDF, doc = new J({ unit: 'pt', format: 'letter' }), W = 612, M = 48, y = 0;
        function page() { doc.setFillColor(15, 30, 51); doc.rect(0, 0, W, 78, 'F'); doc.setTextColor(255); doc.setFont('helvetica', 'bold'); doc.setFontSize(18); doc.text('Technology Strength Assessment', M, 38); doc.setFont('helvetica', 'normal'); doc.setFontSize(10); doc.setTextColor(184, 211, 238); doc.text('Van Ausdall & Farrar  |  Business technology simplified, since 1914', M, 58); y = 112; doc.setTextColor(15, 30, 51); }
        function need(h) { if (y + h > 740) { doc.addPage(); page(); } }
        page();
        var name = ST.lead ? (ST.lead.firstname + ' ' + ST.lead.lastname + ', ' + ST.lead.company) : '';
        doc.setFont('helvetica', 'normal'); doc.setFontSize(11); doc.setTextColor(90, 100, 115); doc.text(name + (name ? '  |  ' : '') + new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' }), M, y); y += 34;
        doc.setTextColor(15, 30, 51); doc.setFont('helvetica', 'bold'); doc.setFontSize(54); doc.text(String(s.total), M, y + 30); doc.setFontSize(12); doc.setFont('helvetica', 'normal'); doc.text('out of 100', M + (s.total > 99 ? 112 : 78), y + 30);
        doc.setFont('helvetica', 'bold'); doc.setFontSize(20); doc.text(b[1], M + 190, y + 12); doc.setFont('helvetica', 'normal'); doc.setFontSize(11); doc.setTextColor(70, 80, 95); doc.text(doc.splitTextToSize(b[2], 330), M + 190, y + 32); y += 72;
        AREAS.forEach(function (a) { doc.setTextColor(15, 30, 51); doc.setFont('helvetica', 'bold'); doc.setFontSize(11); doc.text(a, M, y); doc.setFillColor(226, 234, 243); doc.rect(M + 120, y - 9, 330, 10, 'F'); doc.setFillColor(42, 113, 175); doc.rect(M + 120, y - 9, 330 * s.per[a] / 100, 10, 'F'); doc.text(String(s.per[a]), M + 462, y); y += 24; });
        y += 10;
        [['eliminate', 'Eliminate: risk and waste to remove first'], ['optimize', 'Optimize: what you have, working harder'], ['leverage', 'Leverage: where to grow next']].forEach(function (c) {
          need(60); doc.setFont('helvetica', 'bold'); doc.setFontSize(13); doc.setTextColor(15, 30, 51); doc.text(c[1], M, y); y += 18;
          doc.setFont('helvetica', 'normal'); doc.setFontSize(10.5); doc.setTextColor(50, 60, 75);
          if (!rm[c[0]].length) { doc.text('Nothing here. Nice.', M, y); y += 18; }
          rm[c[0]].forEach(function (r) { var t = doc.splitTextToSize(r.area + ': ' + r.fix, W - 2 * M - 14); need(t.length * 13 + 8); doc.setFillColor(42, 113, 175); doc.circle(M + 3, y - 3, 2, 'F'); doc.text(t, M + 14, y); y += t.length * 13 + 5; });
          y += 10;
        });
        need(80); doc.setFillColor(231, 240, 249); doc.rect(M, y, W - 2 * M, 66, 'F'); doc.setFont('helvetica', 'bold'); doc.setFontSize(12); doc.setTextColor(15, 30, 51); doc.text('Next step', M + 14, y + 22);
        doc.setFont('helvetica', 'normal'); doc.setFontSize(10.5); doc.text(doc.splitTextToSize('A VAF specialist can walk your office and confirm every answer, then build the roadmap with owners and dates. Call ' + CFG.phone + ' or visit ' + CFG.site + '/contact.', W - 2 * M - 28), M + 14, y + 40);
        doc.save('Technology-Strength-Assessment.pdf');
      } catch (e) { window.print(); }
      btn.disabled = false; btn.textContent = old;
    });
  }

  /* ---------- mount ---------- */
  function mount() {
    var host = document.querySelector('[data-vaf-assessment]') || document.getElementById('assess');
    if (!host) return;
    var c = host.querySelector('.q-container') || host;
    root = el('div', 'va__root'); c.innerHTML = ''; c.appendChild(root); host.classList.add('va-host');
    loadHubDb(function () {
      var m = (location.hash.match(/^#r=([01]+)$/) || [])[1], saved = null;
      try { saved = JSON.parse(localStorage.getItem('vafAssess') || 'null'); } catch (e) { }
      if (m && m.length >= ST.bank.length) { ST.ans = decode(m); ST.code = m; ST.lead = saved && saved.code === m ? saved.lead : null; ST.view = 'results'; }
      draw();
    });
  }
  window.VAF_ASSESS = { cfg: CFG, state: ST, score: score };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount); else mount();
})();
