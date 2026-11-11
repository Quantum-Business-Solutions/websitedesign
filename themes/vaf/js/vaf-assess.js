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
  var BANK = [  // area, question, bucket, recommendation, good answer (yes, no, or none = profile question, not scored). 80 questions, 10 per step. Mirrors the HubDB table.
    ['Information', 'Do you execute periodic vulnerability scans in order to test for your security position?', 'optimize', 'Put recurring vulnerability scans on the calendar and track every finding to closure.', 'yes'],
    ['Information', 'Do you enable multi-factor authentication, for administrator and user accounts, in order to improve security for all accessed systems including email, line-of-business and VPN?', 'eliminate', 'Turn on multi-factor authentication for every administrator and user account, including email, line-of-business apps and VPN. It closes the most common way accounts are taken over.', 'yes'],
    ['Information', 'Are your business\'s password and password change policies managed centrally and strong enough to protect your data?', 'eliminate', 'Manage passwords and password changes centrally, with a policy strong enough that a stolen password is not the way in.', 'yes'],
    ['Information', 'Is your server data backed up nightly with more than one instance that is stored off-site or in the cloud?', 'eliminate', 'Back up server data every night and keep more than one copy, with at least one off site or in the cloud, so one failure cannot take your data with it.', 'yes'],
    ['Information', 'Do you have someone patch your servers and computers at least once a month?', 'optimize', 'Patch servers and computers at least once a month, and name the person responsible.', 'yes'],
    ['Information', 'Do you have procedures in place to review updates for your corporate firewall(s)?', 'optimize', 'Review corporate firewall updates on a schedule so a known weakness is not left open.', 'yes'],
    ['Information', 'Are you confident that all computers in your company have a common anti-virus program that is centrally managed and that the computers consistently receive updated signature files?', 'eliminate', 'Put one centrally managed anti-virus on every computer, so every machine gets current signature files.', 'yes'],
    ['Information', 'Do you have a procedure to perform restoration tests of your backups in order to assure they are working properly?', 'optimize', 'Schedule restore tests for your backups. A backup nobody has restored is a hope, not a plan.', 'yes'],
    ['Information', 'Do you have a written Disaster Recovery Plan that includes IT systems and is revised once or twice a year?', 'leverage', 'Write the disaster recovery plan down, include your IT systems, name an owner and revise it once or twice a year.', 'yes'],
    ['Information', 'Do you utilize device monitoring software in order to detect and remediate system issues and concerns quickly?', 'optimize', 'Use device monitoring software so system problems are caught and fixed before users notice.', 'yes'],
    ['Information', 'In the event of a power outage, do you know that you have a battery backup system that will keep your router, firewall and servers running for a minimum of 30 minutes?', 'optimize', 'Add a battery backup that keeps your router, firewall and servers running for at least 30 minutes in a power outage.', 'yes'],
    ['Information', 'Do you utilize security awareness training to make sure users are trained to avoid email and web-based hacking attempts?', 'optimize', 'Train every user to spot email and web-based hacking attempts, and repeat the training on a schedule.', 'yes'],
    ['Information', 'Do you have software and operating systems that are in end-of-life status?', 'eliminate', 'Replace software and operating systems that have reached end of life. They no longer receive security fixes.', 'no'],
    ['Information', 'Do you utilize server virtualization in order to leverage fault tolerance and disaster recovery gains?', 'leverage', 'Look at server virtualization for fault tolerance and faster disaster recovery.', 'yes'],
    ['Information', 'Do you have the ability to send encrypted email when sharing potentially sensitive information?', 'optimize', 'Add the ability to send encrypted email when you share sensitive information.', 'yes'],
    ['Information', 'Do you assess your technology vendors annually to ensure they extend your security standards and policies?', 'optimize', 'Assess your technology vendors every year to confirm they extend your security standards.', 'yes'],
    ['Information', 'Do you share written Internet Usage and Corporate Email policies with your end users?', 'optimize', 'Share written Internet usage and corporate email policies with every user.', 'yes'],
    ['Information', 'Do you have an operable employee onboarding and offboarding policy as it relates to IT?', 'optimize', 'Write an IT onboarding and offboarding policy so access is granted and removed on time.', 'yes'],
    ['Information', 'Do you have a multi-cloud strategy that ensures common authentication, security and policies apply across all cloud vendors?', 'leverage', 'Plan a multi-cloud strategy so the same authentication, security and policies apply everywhere.', 'yes'],
    ['Information', 'Do you have computers that are older than five years?', 'optimize', 'Replace computers older than five years on a schedule, so aging machines do not slow people down or add risk.', 'no'],
    ['Print', 'Does your company have a strong and defined print strategy?', 'leverage', 'Define a print strategy: which devices you need, who owns them and what the goals are.', 'yes'],
    ['Print', 'Are all of your printer devices networked?', 'optimize', 'Put every printer on the network so it can be monitored, secured and managed.', 'yes'],
    ['Print', 'Do you know how much you spend annually on printer supplies and service?', 'optimize', 'Put supplies, service and device costs in one annual report so you know what printing really costs.', 'yes'],
    ['Print', 'Have you ever had a strategic print assessment completed?', 'leverage', 'Have a strategic print assessment done to find the cost, risk and waste in your fleet.', 'yes'],
    ['Print', 'Are you aware of current security concerns regarding printers?', 'eliminate', 'Learn the current security risks of printers and multifunction devices, and close the gaps.', 'yes'],
    ['Print', 'Are print workflow efficiencies critical to your company’s success?', 'optimize', '', 'none'],
    ['Print', 'Does your company have any sensitive customer or company information that should not be printed or should be restricted?', 'optimize', '', 'none'],
    ['Print', 'Does your company have a strategy to track printing of sensitive information?', 'eliminate', 'Track the printing of sensitive information so you can see who printed what.', 'yes'],
    ['Print', 'Are your MFP’s capable of authenticating for end user security?', 'eliminate', 'Require users to authenticate at the multifunction device so documents are released only to the right person.', 'yes'],
    ['Print', 'Is most scanning done on MFPs?', 'leverage', 'Move scanning onto your multifunction devices to cut hand-offs and speed up document workflows.', 'yes'],
    ['Print', 'Do you ever run out of toner or other print related supplies?', 'optimize', 'Set up automatic supply replenishment so you never run out of toner or other print supplies.', 'no'],
    ['Print', 'Do you have a specific replacement strategy for when a printer breaks?', 'optimize', 'Agree a replacement plan for when a printer breaks, so work does not stop.', 'yes'],
    ['Print', 'Do you utilize desktop printers for color printing?', 'optimize', '', 'none'],
    ['Print', 'Do you have enough critical high-volume printers to meet your print needs?', 'optimize', 'Match your high-volume printers to your critical print needs, so peaks do not stall the office.', 'yes'],
    ['Print', 'Do any of your printers or MFP’s frequently have unclaimed print jobs?', 'eliminate', 'Turn on secure print release so jobs are not left unclaimed in the output tray.', 'no'],
    ['Print', 'Is your company still utilizing a on premise print server?', 'optimize', '', 'none'],
    ['Print', 'Are you confident and pleased that the supplier of the devices is providing excellent service, and the cost of the related supplies/services is appropriate?', 'optimize', 'Hold your device supplier to the service you expect, and change supplier if they cannot meet it.', 'yes'],
    ['Print', 'Do you have enough backup printers in storage in case they ever need to be deployed?', 'optimize', 'Keep enough backup printers in storage so a failure is a swap, not a delay.', 'yes'],
    ['Print', 'Do you utilize any thermal print devices?', 'optimize', '', 'none'],
    ['Print', 'Does company management receive weekly/monthly reports detailing print/copy activity, job details and cost?', 'optimize', 'Send management regular print and copy activity reports with job detail and costs.', 'yes'],
    ['Process', 'Does your company have and execute a formal records retention schedule?', 'eliminate', 'Adopt a formal records retention schedule and follow it.', 'yes'],
    ['Process', 'Does your company have a centralized document repository for your business records?', 'optimize', 'Keep business records in one centralized, searchable repository.', 'yes'],
    ['Process', 'Are your current business processes more than 50% paper based?', 'eliminate', 'Move paper-based processes to electronic workflows to cut handling time and errors.', 'no'],
    ['Process', 'Does your company utilize a clear defined strategy that allows you to continue operating at 100% if the building and/or paper records were not accessible?', 'eliminate', 'Write a continuity strategy so the business keeps operating at full capacity if the building or the paper records are not accessible.', 'yes'],
    ['Process', 'Are more than 50% of your department records stored and accessed as paper files?', 'eliminate', 'Convert paper department files to searchable electronic records.', 'no'],
    ['Process', 'Does your administrative staff currently perform more than 50% of the day to day office services (copy print, mail, shipping/receiving, scanning)?', 'optimize', 'Take routine office services off your administrative staff so they can focus on higher-value work.', 'no'],
    ['Process', 'Does your company screen visitors or employees for Temperatures and/or health screening?', 'optimize', '', 'none'],
    ['Process', 'Are you relocating, remodeling or opening a new location in the next 2 years?', 'optimize', '', 'none'],
    ['Process', 'Does your company currently automate your AP processing?', 'leverage', 'Automate accounts payable processing to cut manual entry and speed approvals.', 'yes'],
    ['Process', 'Does your company currently automate your HR/ON-BOARDING processes?', 'leverage', 'Automate HR and onboarding paperwork.', 'yes'],
    ['Process', 'Is your LEGAL/CONTRACT MANAGEMENT documentation automated?', 'leverage', 'Automate legal and contract documentation.', 'yes'],
    ['Process', 'Does your company experience high turnover in your administrative staff and/or in-house resource center?', 'optimize', 'Add a managed office-services option so staff turnover does not disrupt daily work.', 'no'],
    ['Process', 'Does your company have a centralized resource center for office services?', 'optimize', 'Set up a centralized resource center for office services.', 'yes'],
    ['Process', 'Does your company have a coverage plan when an employee is out ill or vacation?', 'optimize', 'Put a coverage plan in place for when an employee is out sick or on vacation.', 'yes'],
    ['Process', 'Does your company utilize a paper visitor management system to track visitors as they enter and leave your organization?', 'optimize', 'Replace the paper visitor log with an electronic visitor management system.', 'no'],
    ['Process', 'Does your company currently deploy an electronic conference room management system for scheduling and usage tracking?', 'leverage', 'Use an electronic conference room management system for scheduling.', 'yes'],
    ['Process', 'Does your company currently track inbound packages from the time they are received (dock) through delivery to the end recipient (desktop)?', 'optimize', 'Track inbound packages from the dock to the desktop.', 'yes'],
    ['Process', 'Is your company currently taking full advantage of carrier and USPS discounts for outgoing overnight mail parcels and USPS mail?', 'optimize', 'Take full advantage of carrier and USPS discounts on outgoing mail and overnight shipping.', 'yes'],
    ['Process', 'Does your company currently have an electronic forms management and/or print submission tool ?', 'leverage', 'Use an electronic forms management or print submission tool.', 'yes'],
    ['Process', 'Does your company have to outsource most of your print technology to local printers?', 'optimize', 'Bring print work in house or onto one managed service instead of outsourcing most of it to local printers.', 'no'],
    ['Communication', 'Is your data switching infrastructure Power over Ethernet (PoE) compliant?', 'optimize', 'Use Power over Ethernet compliant switching so phones, access points and cameras can be powered from the network.', 'yes'],
    ['Communication', 'Is your internet service satisfactory to your current business needs?', 'optimize', 'Review your internet service against what the business needs now, and fix the gaps.', 'yes'],
    ['Communication', 'Do you subscribe to multiple internet services for traffic steering, shaping and/or failover?', 'eliminate', 'Subscribe to more than one internet service for traffic steering, shaping and failover.', 'yes'],
    ['Communication', 'Do you have a disaster recovery plan for your business phone system?', 'eliminate', 'Write a disaster recovery plan for your business phone system.', 'yes'],
    ['Communication', 'Do you currently support remote users that are fully integrated with your phone system?', 'leverage', 'Fully integrate remote users with your phone system.', 'yes'],
    ['Communication', 'Do you currently utilize an IP based phone system?', 'optimize', 'Move to an IP-based phone system.', 'yes'],
    ['Communication', 'Is your phone system cloud based?', 'leverage', 'Look at a cloud-based phone system.', 'yes'],
    ['Communication', 'Are your Smart Phones connected to your corporate phone system (extension dialing, real time presence, corporate directory)?', 'leverage', 'Connect smart phones to your corporate phone system for extension dialing and real-time presence.', 'yes'],
    ['Communication', 'Do you have the ability to record calls today?', 'optimize', 'Add call recording.', 'yes'],
    ['Communication', 'Do you have a desktop client to manage call activity, real time presence, and call routing?', 'leverage', 'Give users a desktop client to manage call activity, real-time presence and call routing.', 'yes'],
    ['Communication', 'Do you use Microsoft Teams for Videoconferencing and Collaboration?', 'leverage', 'Use Microsoft Teams for video conferencing and collaboration, connected to your phone system.', 'yes'],
    ['Communication', 'Can you currently use your desktop or laptop as your phone?', 'leverage', 'Let people use a desktop or laptop as their phone.', 'yes'],
    ['Communication', 'Do you have appropriate Wi-Fi coverage?', 'optimize', 'Fix Wi-Fi coverage gaps so every work area is covered.', 'yes'],
    ['Communication', 'Do your meetings ever start late or not work effectively due to technology?', 'optimize', 'Fix the technology behind late or ineffective meetings.', 'no'],
    ['Communication', 'Does your phone system have contact center functionality that queues calls, emails and chat requests within high call volume groups?', 'leverage', 'Add contact center functionality that queues calls, emails and chat requests in high call volume groups.', 'yes'],
    ['Communication', 'Do you utilize call reports to analyze employee productivity?', 'optimize', 'Use call reports to see employee productivity.', 'yes'],
    ['Communication', 'Do you have a dedicated employee or team to handle conference room technology in your workplace?', 'optimize', 'Give conference room technology a dedicated owner or team.', 'yes'],
    ['Communication', 'Are you satisfied with your current conference room technology', 'optimize', 'Improve the conference room technology that is not working well for you.', 'yes'],
    ['Communication', 'Does your company have a mobile service plan?', 'optimize', '', 'none'],
    ['Communication', 'If yes, does your company have 50 or more mobile devices managed under a company mobile plan?', 'optimize', '', 'none'],
  ].map(function (r) { return { area: r[0], q: r[1], bucket: r[2], fix: r[3], good: r[4] || 'yes', w: r[4] === 'none' ? 0 : 1 }; });
  var COPY = {
    title: 'Take the Technology Strength Assessment',
    lead: 'Eighty yes or no questions in four areas, taken in eight short steps of ten. About 10 to 15 minutes. You get a score, an eliminate, optimize and leverage roadmap, and a PDF.',
    formTitle: 'Where should we send your results?',
    formNote: 'A person from the Indianapolis office reviews your answers and can walk the office with you. We use your details only to respond to this request.',
    submit: 'Show my results',
    bands: [[0, 'Exposed', 'Several basics are missing. The first fixes will pay back quickly.'], [40, 'Developing', 'You have a foundation. The gaps below are where to focus next.'], [70, 'Strong', 'A solid base. The roadmap below is about leverage and keeping it that way.']],
    cta: 'Schedule a consultation',
    ctaNote: 'A specialist can walk your office, confirm every answer and build the roadmap with you.'
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
      var rows = (j.results || []).map(function (r) { var v = r.values || {}; return { area: String(val(v.area) || ''), q: String(val(v.question) || ''), bucket: String(val(v.bucket) || 'optimize').toLowerCase(), fix: String(val(v.fix) || ''), good: (function (g) { g = String(g || 'yes').toLowerCase(); return g === 'no' || g === 'none' ? g : 'yes'; })(val(v.good)), w: isNaN(parseFloat(val(v.weight))) ? 1 : parseFloat(val(v.weight)), sort: parseFloat(val(v.sort)) || 0 }; })
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
  /* eight steps: each area in parts of ten questions, in the order of the table */
  var PART = 10;
  function steps() { var out = []; AREAS.forEach(function (a) { var qs = areaQs(a), n = Math.max(1, Math.ceil(qs.length / PART)); for (var p = 0; p < n; p++) out.push({ area: a, part: p + 1, parts: n, qs: qs.slice(p * PART, (p + 1) * PART) }); }); return out; }
  function scored(r) { return r.good !== 'none' && r.w !== 0; }
  function isGood(r) { var a = ST.ans[key(r)]; return r.good === 'no' ? a === 0 : a === 1; }
  function key(r) { return ST.bank.indexOf(r); }
  function score() {
    var per = {}, tot = 0, max = 0;
    AREAS.forEach(function (a) {
      var qs = areaQs(a), got = 0, m = 0;
      qs.forEach(function (r) { if (!scored(r)) return; var w = r.w || 1; m += w; if (isGood(r)) got += w; });
      per[a] = m ? Math.round(100 * got / m) : 0; tot += got; max += m;
    });
    return { per: per, total: max ? Math.round(100 * tot / max) : 0 };
  }
  function band(n) { var b = ST.copy.bands[0]; ST.copy.bands.forEach(function (x) { if (n >= x[0]) b = x; }); return b; }
  function roadmap() {
    var out = { eliminate: [], optimize: [], leverage: [] };
    ST.bank.forEach(function (r) { if (scored(r) && r.fix && !isGood(r)) (out[r.bucket] || out.optimize).push(r); });
    return out;
  }
  /* answers <-> short code, so a results link can be reopened */
  function encode() { return ST.bank.map(function (r, i) { return ST.ans[i] === 1 ? '1' : (ST.ans[i] === 0.5 ? '5' : '0'); }).join(''); }
  function decode(c) { var a = {}; for (var i = 0; i < ST.bank.length; i++) a[i] = c.charAt(i) === '1' ? 1 : (c.charAt(i) === '5' ? 0.5 : 0); return a; }

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
  function head(pos) {   /* pos: steps completed, 0 to 9 (eight question steps, then the contact step, then results) */
    var h = el('div', 'va__top'), n = steps().length, ai = pos >= n + 1 ? AREAS.length + 1 : (pos >= n ? AREAS.length : Math.floor(pos / Math.max(1, n / AREAS.length)));
    var list = el('ol', 'va__steps');
    AREAS.concat(['Results']).forEach(function (a, i) { var li = el('li', i < ai ? 'is-done' : (i === ai ? 'is-on' : ''), '<b>' + (i + 1) + '</b><span>' + esc(a) + '</span>'); list.appendChild(li); });
    h.appendChild(list);
    var bar = el('div', 'va__bar'); var f = el('i'); f.style.width = Math.round(100 * pos / (n + 1)) + '%'; bar.appendChild(f); h.appendChild(bar);
    if (pos <= n - 1) { var left = Math.max(1, Math.round((n - pos) * 1.5)); h.appendChild(el('p', 'va__pace', 'Step ' + (pos + 1) + ' of ' + n + ' &middot; about ' + left + ' minute' + (left === 1 ? '' : 's') + ' left')); }
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
    var S = steps(), cur = S[ST.i], a = cur.area, qs = cur.qs;
    var d = el('div', 'va__card');
    d.appendChild(head(ST.i));
    d.appendChild(el('h2', 'va__h', esc(a) + (cur.parts > 1 ? ' <small class="va__part">Part ' + cur.part + ' of ' + cur.parts + '</small>' : '')));
    d.appendChild(el('p', 'va__lead', esc(AREA_INTRO[a])));
    qs.forEach(function (r) {
      var k = key(r);
      var row = el('div', 'va__q');
      row.appendChild(el('p', 'va__qt', esc(r.q)));
      var g = el('div', 'va__opts'); g.setAttribute('role', 'radiogroup'); g.setAttribute('aria-label', r.q);
      [['Yes', 1], ['No', 0], ['Not sure', 0.5]].forEach(function (o) {
        var b = el('button', 'va__opt' + (ST.ans[k] === (o[1] === 0.5 ? 0.5 : o[1]) && k in ST.ans ? ' is-on' : ''), o[0]); b.type = 'button'; b.setAttribute('role', 'radio');
        b.setAttribute('aria-checked', (k in ST.ans && ST.ans[k] === o[1]) ? 'true' : 'false');
        b.onclick = function () { ST.ans[k] = o[1]; Array.prototype.forEach.call(g.children, function (c) { c.classList.remove('is-on'); c.setAttribute('aria-checked', 'false'); }); b.classList.add('is-on'); b.setAttribute('aria-checked', 'true'); next.disabled = !complete(ST.i); };
        g.appendChild(b);
      });
      row.appendChild(g); d.appendChild(row);
    });
    var nav = el('div', 'va__nav');
    var back = el('button', 'va__btn va__btn--ghost', 'Back'); back.type = 'button'; back.onclick = function () { if (ST.i === 0) { ST.view = 'intro'; } else ST.i--; draw(); scrollTop(); };
    var nx = S[ST.i + 1], next = el('button', 'va__btn', !nx ? 'Finish' : (nx.area !== a ? 'Next: ' + nx.area : 'Next: part ' + nx.part)); next.type = 'button'; next.disabled = !complete(ST.i);
    next.onclick = function () { if (ST.i === S.length - 1) ST.view = 'form'; else ST.i++; draw(); scrollTop(); };
    nav.appendChild(back); nav.appendChild(next); d.appendChild(nav);
    return d;
  }
  function complete(i) { var c = steps()[i]; return !!c && c.qs.every(function (r) { return key(r) in ST.ans; }); }
  function viewForm() {
    var d = el('div', 'va__card');
    d.appendChild(head(steps().length));
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
    var back = el('button', 'va__btn va__btn--ghost va__btn--sm', 'Back'); back.type = 'button'; back.onclick = function () { ST.view = 'q'; ST.i = steps().length - 1; draw(); };
    d.appendChild(back);
    return d;
  }
  function viewResults() {
    var s = score(), b = band(s.total), rm = roadmap();
    var d = el('div', 'va__card va__res');
    d.appendChild(head(steps().length + 1));
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
  var LOGO;
  function logoData(cb) {
    if (LOGO !== undefined) return cb(LOGO);
    fetch('https://50498425.fs1.hubspotusercontent-na1.net/hubfs/50498425/vaf/assets/logo-600.png').then(function (r) { return r.blob(); }).then(function (x) {
      var fr = new FileReader(); fr.onload = function () { LOGO = fr.result; cb(LOGO); }; fr.readAsDataURL(x);
    }).catch(function () { LOGO = null; cb(null); });
  }
  function makePdf(s, b, rm, btn) {
    btn.disabled = true; var old = btn.textContent; btn.textContent = 'Preparing PDF...';
    loadPdfLib(function () {
      logoData(function (logo) {
        try {
          var J = window.jspdf.jsPDF, doc = new J({ unit: 'pt', format: 'letter' }), W = 612, M = 48, y = 0;
          function head() {
            doc.setFillColor(255, 255, 255); doc.rect(0, 0, W, 90, 'F');
            if (logo) { try { doc.addImage(logo, 'PNG', M, 24, 190, 37.7); } catch (e) { } } else { doc.setTextColor(15, 30, 51); doc.setFont('helvetica', 'bold'); doc.setFontSize(16); doc.text('Van Ausdall & Farrar', M, 50); }
            doc.setTextColor(106, 123, 144); doc.setFont('helvetica', 'bold'); doc.setFontSize(10); doc.text('TECHNOLOGY STRENGTH ASSESSMENT', W - M, 46, { align: 'right' });
            doc.setFillColor(42, 113, 175); doc.rect(0, 90, W, 4, 'F'); y = 132; doc.setTextColor(15, 30, 51);
          }
          function need(h) { if (y + h > 730) { doc.addPage(); head(); } }
          head();
          var name = ST.lead ? (ST.lead.firstname + ' ' + ST.lead.lastname + ', ' + ST.lead.company) : '';
          doc.setFont('helvetica', 'normal'); doc.setFontSize(11); doc.setTextColor(90, 100, 115); doc.text(name + (name ? '  |  ' : '') + new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' }), M, y); y += 20;
          // score panel
          doc.setFillColor(15, 30, 51); doc.roundedRect(M, y, W - 2 * M, 112, 12, 12, 'F');
          doc.setTextColor(143, 194, 242); doc.setFont('helvetica', 'bold'); doc.setFontSize(64); doc.text(String(s.total), M + 28, y + 76);
          doc.setFontSize(12); doc.setFont('helvetica', 'normal'); doc.setTextColor(197, 214, 232); doc.text('out of 100', M + 28 + (s.total > 99 ? 132 : 92), y + 76);
          doc.setTextColor(143, 194, 242); doc.setFont('helvetica', 'bold'); doc.setFontSize(10.5); doc.text('YOUR TECHNOLOGY STRENGTH SCORE', M + 250, y + 36);
          doc.setTextColor(255); doc.setFontSize(24); doc.text(b[1], M + 250, y + 64);
          doc.setFont('helvetica', 'normal'); doc.setFontSize(10.5); doc.setTextColor(197, 214, 232); doc.text(doc.splitTextToSize(b[2], W - 2 * M - 270), M + 250, y + 82); y += 142;
          AREAS.forEach(function (a) { doc.setTextColor(15, 30, 51); doc.setFont('helvetica', 'bold'); doc.setFontSize(11.5); doc.text(a, M, y); doc.setFillColor(226, 234, 243); doc.roundedRect(M + 120, y - 10, 330, 12, 6, 6, 'F'); if (s.per[a] > 0) { doc.setFillColor(42, 113, 175); doc.roundedRect(M + 120, y - 10, Math.max(12, 330 * s.per[a] / 100), 12, 6, 6, 'F'); } doc.text(String(s.per[a]), M + 468, y); y += 26; });
          y += 12;
          [['eliminate', 'Eliminate: risk and waste to remove first', [194, 65, 12]], ['optimize', 'Optimize: what you have, working harder', [42, 113, 175]], ['leverage', 'Leverage: where to grow next', [15, 122, 77]]].forEach(function (c) {
            need(70); doc.setFillColor(c[2][0], c[2][1], c[2][2]); doc.rect(M, y - 13, 5, 20, 'F');
            doc.setFont('helvetica', 'bold'); doc.setFontSize(13.5); doc.setTextColor(15, 30, 51); doc.text(c[1], M + 14, y + 2); y += 26;
            doc.setFont('helvetica', 'normal'); doc.setFontSize(10.5); doc.setTextColor(50, 60, 75);
            if (!rm[c[0]].length) { doc.text('Nothing here. Nice.', M + 14, y); y += 18; }
            rm[c[0]].forEach(function (r) { var t = doc.splitTextToSize(r.area + ': ' + r.fix, W - 2 * M - 30); need(t.length * 13 + 8); doc.setFillColor(c[2][0], c[2][1], c[2][2]); doc.circle(M + 17, y - 3, 2.4, 'F'); doc.text(t, M + 28, y); y += t.length * 13 + 5; });
            y += 8;
          });
          need(92); doc.setFillColor(15, 30, 51); doc.roundedRect(M, y, W - 2 * M, 82, 10, 10, 'F');
          doc.setTextColor(143, 194, 242); doc.setFont('helvetica', 'bold'); doc.setFontSize(10.5); doc.text('NEXT STEP', M + 22, y + 22);
          doc.setTextColor(255); doc.setFontSize(13); doc.text('Let a specialist confirm every answer', M + 22, y + 40);
          doc.setFont('helvetica', 'normal'); doc.setFontSize(10.5); doc.setTextColor(197, 214, 232);
          doc.text(doc.splitTextToSize('A VAF specialist can walk your office, then build the roadmap with owners and dates. Call ' + CFG.phone + ' or visit ' + CFG.site + '/contact.', W - 2 * M - 44), M + 22, y + 56);
          var N = doc.getNumberOfPages();
          for (var i = 1; i <= N; i++) {
            doc.setPage(i); doc.setDrawColor(219, 229, 240); doc.line(M, 752, W - M, 752); doc.setFont('helvetica', 'normal'); doc.setFontSize(8.5); doc.setTextColor(106, 123, 144);
            doc.text('Van Ausdall & Farrar  |  6430 E 75th Street, Indianapolis, IN 46250  |  (317) 634-2913  |  vanausdall.com', M, 768); doc.text(String(i), W - M, 768, { align: 'right' });
          }
          doc.save('Technology-Strength-Assessment.pdf');
        } catch (e) { window.print(); }
        btn.disabled = false; btn.textContent = old;
      });
    });
  }

  /* ---------- mount ---------- */
  function mount() {
    var host = document.querySelector('[data-vaf-assessment]') || document.getElementById('assess');
    if (!host) return;
    var c = host.querySelector('.q-container') || host;
    root = el('div', 'va__root'); Array.prototype.forEach.call(c.children, function (k) { k.style.display = 'none'; k.setAttribute('aria-hidden', 'true'); }); c.appendChild(root); host.classList.add('va-host');
    loadHubDb(function () {
      var m = (location.hash.match(/^#r=([015]+)$/) || [])[1], saved = null;
      try { saved = JSON.parse(localStorage.getItem('vafAssess') || 'null'); } catch (e) { }
      if (m && m.length >= ST.bank.length) { ST.ans = decode(m); ST.code = m; ST.lead = saved && saved.code === m ? saved.lead : null; ST.view = 'results'; }
      draw();
    });
  }
  window.VAF_ASSESS = { cfg: CFG, state: ST, score: score };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount); else mount();
})();
