(function () {
  'use strict';
  var d = document, w = window;
  function $(s, r) { return (r || d).querySelector(s); }
  function $$(s, r) { return [].slice.call((r || d).querySelectorAll(s)); }
  function mk(t, c, h) { var e = d.createElement(t); if (c) e.className = c; if (h != null) e.innerHTML = h; return e; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  /* skip link, for keyboard and screen reader users */
  if (!$('.wow-skip') && $('#main,#q-content')) { var sk = mk('a', 'wow-skip', 'Skip to content'); sk.href = $('#main') ? '#main' : '#q-content'; d.body.insertBefore(sk, d.body.firstChild); }

  /* scroll progress and back to top */
  var bar = mk('div', 'wow-prog'); bar.setAttribute('aria-hidden', 'true'); d.body.appendChild(bar);
  var top = mk('button', 'wow-top', '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path d="M12 19V5M5 12l7-7 7 7" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>');
  top.type = 'button'; top.setAttribute('aria-label', 'Back to top'); d.body.appendChild(top);
  top.onclick = function () { w.scrollTo({ top: 0, behavior: 'smooth' }); };
  var tick = false;
  function onScroll() {
    if (tick) return; tick = true;
    requestAnimationFrame(function () {
      var h = d.documentElement.scrollHeight - w.innerHeight;
      bar.style.transform = 'scaleX(' + (h > 0 ? Math.min(1, w.scrollY / h) : 0) + ')';
      top.classList.toggle('is-on', w.scrollY > 1200); tick = false;
    });
  }
  w.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  /* open now: the Customer Care Center keeps Monday to Friday, 7:00am to 5:00pm Indianapolis time */
  function indy() {
    var p = new Intl.DateTimeFormat('en-US', { timeZone: 'America/Indiana/Indianapolis', weekday: 'short', hour: 'numeric', minute: 'numeric', hour12: false }).formatToParts(new Date()), o = {};
    p.forEach(function (x) { o[x.type] = x.value; });
    return { day: o.weekday, mins: (parseInt(o.hour, 10) % 24) * 60 + parseInt(o.minute, 10) };
  }
  function status() {
    try {
      var t = indy(), wk = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'].indexOf(t.day) > -1, open = wk && t.mins >= 420 && t.mins < 1020;
      if (open) return { open: true, text: 'Open now, until 5:00pm ET' };
      var nextDay = t.day === 'Fri' ? 'Monday' : (t.day === 'Sat' ? 'Monday' : (t.day === 'Sun' ? 'Monday' : (t.mins >= 1020 ? 'tomorrow' : 'today')));
      return { open: false, text: 'Closed, opens ' + nextDay + ' at 7:00am ET' };
    } catch (e) { return null; }
  }
  var st = status();
  if (st) {
    var chip = function () { return mk('span', 'wow-open' + (st.open ? ' is-open' : ''), '<i aria-hidden="true"></i>' + esc(st.text)); };
    var u = $('.pv-util .q-container'); if (u) u.insertBefore(chip(), u.firstChild);
    var meta = $('.vv__meta'); if (meta) { var li = mk('li'); li.appendChild(chip()); meta.insertBefore(li, meta.firstChild); }
  }

  /* command palette: Ctrl or Cmd + K, or press / */
  var items = [], seen = {};
  function add(label, href, hint, act) { var k = label + '|' + href; if (!label || seen[k]) return; seen[k] = 1; items.push({ label: label.replace(/\s+/g, ' ').trim(), href: href, hint: hint || '', act: act }); }
  function collect() {
    if (items.length) return;
    add('Take the Technology Strength Assessment', '/technology-strength-assessment', 'Tool');
    add('Get the 27 Technology Tips for 2027', '', 'Free guide', function () { if (w.VAF_TIPS_OPEN) w.VAF_TIPS_OPEN(); });
    add('Call (317) 634-2913', 'tel:+13176342913', 'Phone');
    add('Get directions to our Indianapolis office', 'https://www.google.com/maps/dir/?api=1&destination=Van+Ausdall+%26+Farrar+6430+E+75th+Street+Indianapolis+IN+46250', 'Map');
    $$('.q-header a[href], .q-footer a[href], .pv-mega a[href]').forEach(function (a) {
      if (a.hostname !== w.location.hostname || a.closest('.q-footer-social')) return;
      var t = (a.textContent || '').replace(/\s+/g, ' ').trim(); if (t.length > 2 && t.length < 80 && a.pathname.length > 1) add(t, a.pathname, (a.closest('.q-footer') ? 'Footer' : 'Menu'));
    });
  }
  var pal, input, list, cur = [], idx = 0, last;
  function render() {
    var q = input.value.toLowerCase().split(/\s+/).filter(Boolean);
    cur = items.filter(function (it) { var s = (it.label + ' ' + it.hint).toLowerCase(); return q.every(function (t) { return s.indexOf(t) > -1; }); }).slice(0, 40);
    idx = 0; list.innerHTML = '';
    if (!cur.length) { list.innerHTML = '<li style="padding:16px;color:#6a7b90">No match. Try “phones”, “security” or “print”.</li>'; return; }
    cur.forEach(function (it, i) {
      var li = mk('li', i === 0 ? 'is-on' : ''), el;
      if (it.act) { el = mk('button', '', '<span>' + esc(it.label) + '</span><small>' + esc(it.hint) + '</small>'); el.type = 'button'; el.onclick = function () { closePal(); it.act(); }; }
      else { el = mk('a', '', '<span>' + esc(it.label) + '</span><small>' + esc(it.hint) + '</small>'); el.href = it.href; }
      li.appendChild(el); list.appendChild(li);
    });
  }
  function mark() { $$('li', list).forEach(function (li, i) { li.classList.toggle('is-on', i === idx); if (i === idx) li.scrollIntoView({ block: 'nearest' }); }); }
  function openPal() {
    if (pal) return; collect(); last = d.activeElement;
    pal = mk('div', 'wow-pal'); pal.setAttribute('role', 'dialog'); pal.setAttribute('aria-modal', 'true'); pal.setAttribute('aria-label', 'Search the site');
    var box = mk('div', 'wow-pal__box'); input = mk('input'); input.type = 'text'; input.placeholder = 'Search pages and actions...'; input.setAttribute('aria-label', 'Search'); list = mk('ul');
    box.appendChild(input); box.appendChild(list); box.appendChild(mk('div', 'wow-pal__foot', '<span>↑ ↓ to move</span><span>Enter to open</span><span>Esc to close</span>')); pal.appendChild(box); d.body.appendChild(pal);
    render(); requestAnimationFrame(function () { pal.classList.add('is-open'); input.focus(); });
    input.addEventListener('input', render);
    pal.addEventListener('click', function (e) { if (e.target === pal) closePal(); });
  }
  function closePal() { if (!pal) return; pal.remove(); pal = null; if (last && last.focus) try { last.focus(); } catch (e) { } }
  d.addEventListener('keydown', function (e) {
    var tag = (e.target.tagName || '').toLowerCase(), typing = tag === 'input' || tag === 'textarea' || tag === 'select' || e.target.isContentEditable;
    if ((e.key === 'k' || e.key === 'K') && (e.ctrlKey || e.metaKey)) { e.preventDefault(); pal ? closePal() : openPal(); return; }
    if (e.key === '/' && !typing && !pal) { e.preventDefault(); openPal(); return; }
    if (!pal) return;
    if (e.key === 'Escape') { closePal(); }
    else if (e.key === 'ArrowDown') { e.preventDefault(); idx = Math.min(cur.length - 1, idx + 1); mark(); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); idx = Math.max(0, idx - 1); mark(); }
    else if (e.key === 'Enter' && cur[idx]) { e.preventDefault(); var it = cur[idx]; if (it.act) { closePal(); it.act(); } else { w.location.href = it.href; } }
  });
  var u2 = $('.pv-util .q-container');
  if (u2) { var kb = mk('button', 'wow-k', 'Search <kbd>' + (/Mac|iPhone|iPad/.test(navigator.platform) ? '⌘K' : 'Ctrl K') + '</kbd>'); kb.type = 'button'; kb.setAttribute('aria-label', 'Search the site'); kb.onclick = openPal; u2.insertBefore(kb, u2.querySelector('.pv-phone') || null); }

  /* spotlight glow that follows the pointer on cards and panels */
  if (w.matchMedia && w.matchMedia('(hover:hover)').matches && !w.matchMedia('(prefers-reduced-motion:reduce)').matches) {
    $$('.vr__card, .fcard, .vaf-sc__panel, .vaf-tl__card, .vaf-wheel__card, .pv-stat').forEach(function (c) {
      c.classList.add('wow-spot');
      c.addEventListener('pointermove', function (e) { var r = c.getBoundingClientRect(); c.style.setProperty('--mx', (e.clientX - r.left) + 'px'); c.style.setProperty('--my', (e.clientY - r.top) + 'px'); }, { passive: true });
    });
  }


  /* case-study metrics count up as they scroll into view */
  if (w.IntersectionObserver && !(w.matchMedia && w.matchMedia('(prefers-reduced-motion:reduce)').matches)) {
    var cio = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return; cio.unobserve(e.target);
        var el = e.target, txt = el.textContent.trim(), m = txt.match(/^([^0-9]*)([0-9][0-9,]*)(\.[0-9]+)?(.*)$/);
        if (!m) return;
        var pre = m[1], num = parseFloat(m[2].replace(/,/g, '') + (m[3] || '')), places = m[3] ? m[3].length - 1 : 0, comma = m[2].indexOf(',') > -1, suf = m[4], t0 = null;
        if (num >= 1900 && num <= 2100 && !comma && !places) return;
        function fmt(v) { var f = v.toFixed(places); if (comma) { var a = f.split('.'); a[0] = a[0].replace(/\B(?=(\d{3})+(?!\d))/g, ','); f = a.join('.'); } return pre + f + suf; }
        function step(ts) { if (t0 === null) t0 = ts; var k = Math.min(1, (ts - t0) / 1300); k = 1 - Math.pow(1 - k, 3); el.textContent = fmt(num * k); if (k < 1) requestAnimationFrame(step); else el.textContent = txt; }
        el.textContent = fmt(0); requestAnimationFrame(step);
      });
    }, { threshold: 0.5 });
    $$('.vcs__v').forEach(function (el) { cio.observe(el); });
  }

  /* returning visitors: remember the last service they read and offer to pick it up */
  try {
    var path = w.location.pathname;
    if (/^\/(services|solutions|industries)/.test(path)) {
      var h1 = $('h1'); if (h1) localStorage.setItem('vafLast', JSON.stringify({ p: path, t: h1.textContent.replace(/\s+/g, ' ').trim().slice(0, 70), ts: Date.now() }));
    } else if (path === '/' && !sessionStorage.getItem('vafGreeted')) {
      var last = JSON.parse(localStorage.getItem('vafLast') || 'null');
      if (last && Date.now() - last.ts > 3600e3 && Date.now() - last.ts < 30 * 864e5) {
        sessionStorage.setItem('vafGreeted', '1');
        setTimeout(function () {
          var g = mk('div', 'wow-greet', '<span>Welcome back. Pick up where you left off: <a href="' + esc(last.p) + '">' + esc(last.t) + '</a></span><button type="button" aria-label="Dismiss">&times;</button>');
          g.querySelector('button').onclick = function () { g.remove(); }; d.body.appendChild(g); setTimeout(function () { if (g.parentNode) g.remove(); }, 14000);
        }, 2500);
      }
    }
  } catch (e) { }

  /* a hello for the curious */
  try { console.log('%cVan Ausdall & Farrar', 'font:800 18px system-ui;color:#2a71af', '\nBuilt on HubSpot, edited in HubSpot. Press Ctrl+K to search. We are hiring: /careers'); } catch (e) { }
})();
