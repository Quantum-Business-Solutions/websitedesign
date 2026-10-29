/* VAF lead-magnet popup: "27 Technology Tips for 2027".
   Copy, rules and the 27 tips live in HubDB (editable in HubSpot). Submits to a HubSpot form; the PDF is built in the browser.
   Open it from anywhere with a link to #tips or an element with data-vaf-tips. */
(function () {
  'use strict';
  var d = document;
  var C = { portal: '50498425', form: 'd7e2045f-49b0-43d8-8e5b-f712393c82b5', tips: '451425916', settings: '450036143', phone: '(317) 634-2913', site: 'vanausdall.com' };
  var S = {
    enabled: 'yes', eyebrow: 'Free guide', headline: '27 Technology Tips for 2027',
    sub: "A plain-English checklist from Indiana's office technology team. Security, phones, print and paperwork, in about ten minutes.",
    button: 'Send me the tips', privacy: 'We use your details to send this guide and follow up about technology. You can opt out at any time.',
    success_title: 'Your tips are ready', success_text: 'Download the PDF now. A specialist from the Indianapolis office may follow up to see which tips fit your office.',
    download_button: 'Download the PDF',
    bullets: 'Close the security gaps attackers try first|Cut print and paper waste|Keep phones and internet working when it counts',
    pill: 'Free guide: 27 Tips', delay_seconds: '20', cooldown_days: '14', exclude_paths: '/policies/,/technology-strength-assessment,/contact,/support'
  };
  var AREAS = ['Information', 'Communication', 'Print', 'Process'];
  var TIPS = null, el, opened = false, last;
  var API = 'https://api.hubapi.com/cms/v3/hubdb/tables/';

  function ls(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { } return null; }
  function mk(t, c, h) { var e = document.createElement(t); if (c) e.className = c; if (h != null) e.innerHTML = h; return e; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function v(x) { return x && typeof x === 'object' && 'name' in x ? x.name : x; }

  function loadSettings(cb) {
    fetch(API + C.settings + '/rows?portalId=' + C.portal + '&limit=100').then(function (r) { return r.ok ? r.json() : Promise.reject(); }).then(function (j) {
      (j.results || []).forEach(function (r) { var k = String(v((r.values || {}).key) || ''), t = String(v((r.values || {}).value) || ''); if (k && t && k in S) S[k] = t; });
    }).catch(function () { }).then(cb);
  }
  function loadTips(cb) {
    if (TIPS) return cb(TIPS);
    fetch(API + C.tips + '/rows?portalId=' + C.portal + '&limit=100&sort=sort').then(function (r) { return r.ok ? r.json() : Promise.reject(); }).then(function (j) {
      var t = (j.results || []).map(function (r) { var x = r.values || {}; return { area: String(v(x.area) || ''), title: String(v(x.title) || ''), tip: String(v(x.tip) || ''), sort: parseFloat(v(x.sort)) || 0 }; }).filter(function (r) { return r.title; });
      TIPS = t.length ? t : null; cb(TIPS);
    }).catch(function () { cb(null); });
  }

  function excluded() { var p = location.pathname; return S.exclude_paths.split(',').some(function (f) { f = f.trim(); return f && p.indexOf(f) > -1; }); }
  function cooled() { var t = parseInt(ls('vafTipsSeen') || '0', 10); return t && Date.now() - t < parseFloat(S.cooldown_days) * 864e5; }

  function open(force) {
    if (opened) return; opened = true; last = document.activeElement;
    if (!force) ls('vafTipsSeen', String(Date.now()));
    el = mk('div', 'vp'); el.setAttribute('role', 'dialog'); el.setAttribute('aria-modal', 'true'); el.setAttribute('aria-labelledby', 'vp-h');
    var card = mk('div', 'vp__card');
    card.innerHTML = '<button type="button" class="vp__x" aria-label="Close">&times;</button>' +
      '<div class="vp__art" aria-hidden="true"><div class="vp__stage"><div class="vp__book"><div class="vp__face vp__front"><span class="vp__plate"><img src="https://50498425.fs1.hubspotusercontent-na1.net/hubfs/50498425/vaf/assets/logo-600.png" alt="" width="150" height="30"></span><b class="vp__bn">27</b><b class="vp__bt">Technology<br>Tips</b><b class="vp__by">for 2027</b><i class="vp__rule"></i><span class="vp__bs">A practical guide for Indiana offices</span><span class="vp__bf">VAN AUSDALL &amp; FARRAR&nbsp;&nbsp;|&nbsp;&nbsp;SINCE 1914</span></div><div class="vp__face vp__spine"></div><div class="vp__face vp__pages"></div><div class="vp__face vp__back"></div></div><div class="vp__shadow"></div></div></div>' +
      '<div class="vp__body"></div>';
    el.appendChild(card); document.body.appendChild(el);
    form();
    requestAnimationFrame(function () { el.classList.add('is-open'); card.querySelector('input').focus(); });
    el.addEventListener('click', function (e) { if (e.target === el) close(); });
    card.querySelector('.vp__x').onclick = close;
    document.addEventListener('keydown', key);
    loadTips(function () { });
  }
  function close() { if (!el) return; document.removeEventListener('keydown', key); el.remove(); el = null; opened = false; if (last && last.focus) try { last.focus(); } catch (e) { } }
  function key(e) {
    if (e.key === 'Escape') return close();
    if (e.key !== 'Tab' || !el) return;
    var f = el.querySelectorAll('button,input,a[href]'); if (!f.length) return;
    var a = f[0], b = f[f.length - 1];
    if (e.shiftKey && document.activeElement === a) { e.preventDefault(); b.focus(); } else if (!e.shiftKey && document.activeElement === b) { e.preventDefault(); a.focus(); }
  }
  function bullets() {
    var b = (S.bullets || '').split('|').map(function (x) { return x.trim(); }).filter(Boolean);
    return b.length ? '<ul class="vp__ul">' + b.map(function (x) { return '<li>' + esc(x) + '</li>'; }).join('') + '</ul>' : '';
  }
  function form() {
    var b = el.querySelector('.vp__body');
    b.innerHTML = '<p class="vp__eyebrow">' + esc(S.eyebrow) + '</p><h2 class="vp__h" id="vp-h">' + esc(S.headline) + '</h2><p class="vp__sub">' + esc(S.sub) + '</p>' + bullets() +
      '<form class="vp__form" novalidate><div class="vp__row"><label>First name<input name="firstname" autocomplete="given-name" required></label><label>Last name<input name="lastname" autocomplete="family-name" required></label></div><label>Work email<input name="email" type="email" autocomplete="email" required></label><label>Company website or domain<input name="website" autocomplete="organization-url" placeholder="yourcompany.com" required></label>' +
      '<p class="vp__err" role="alert" hidden></p><button class="vp__btn" type="submit">' + esc(S.button) + '</button><button class="vp__skip" type="button">No thanks</button></form><p class="vp__fine">' + esc(S.privacy) + '</p>';
    var f = b.querySelector('form');
    b.querySelector('.vp__skip').onclick = close;
    f.onsubmit = function (e) {
      e.preventDefault();
      var fn = f.elements.firstname.value.trim(), ln = f.elements.lastname.value.trim(), em = f.elements.email.value.trim(), web = f.elements.website.value.trim(), er = f.querySelector('.vp__err');
      if (!fn || !ln || !web || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(em)) { er.hidden = false; er.textContent = 'Please add your name, a valid work email and your company website or domain.'; return; }
      var btn = f.querySelector('.vp__btn'); btn.disabled = true;
      var hutk = (document.cookie.match(/hubspotutk=([^;]+)/) || [])[1];
      var body = { submittedAt: String(Date.now()), fields: [{ name: 'firstname', value: fn }, { name: 'lastname', value: ln }, { name: 'email', value: em }, { name: 'website', value: web }], context: { pageUri: location.href, pageName: document.title } };
      if (hutk) body.context.hutk = hutk;
      fetch('https://api.hsforms.com/submissions/v3/integration/submit/' + C.portal + '/' + C.form, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) })
        .then(function (r) { if (!r.ok) throw 0; }).then(function () { ls('vafTipsSeen', String(Date.now() + 365 * 864e5)); done(fn); })
        .catch(function () { btn.disabled = false; er.hidden = false; er.textContent = 'Something went wrong. Please try again or call ' + C.phone + '.'; });
    };
  }
  function done(name) {
    var b = el.querySelector('.vp__body');
    b.innerHTML = '<p class="vp__eyebrow">' + esc(S.eyebrow) + '</p><h2 class="vp__h" id="vp-h">' + esc(S.success_title) + '</h2><p class="vp__sub">' + esc(S.success_text) + '</p>' +
      '<button class="vp__btn" type="button">' + esc(S.download_button) + '</button><p class="vp__fine">Want to see where your office stands? <a href="/technology-strength-assessment">Take the Technology Strength Assessment</a>.</p>';
    var d = b.querySelector('.vp__btn'); d.focus();
    d.onclick = function () { d.disabled = true; var t = d.textContent; d.textContent = 'Preparing PDF...'; pdf(name, function (ok) { d.disabled = false; d.textContent = ok ? t : 'Try again'; }); };
  }

  function lib(cb) {
    if (window.jspdf) return cb(true);
    var s = document.createElement('script'); s.src = 'https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js'; s.onload = function () { cb(true); }; s.onerror = function () { cb(false); }; document.head.appendChild(s);
  }
  var LOGO;
  function logoData(cb) {
    if (LOGO !== undefined) return cb(LOGO);
    fetch('https://50498425.fs1.hubspotusercontent-na1.net/hubfs/50498425/vaf/assets/logo-600.png').then(function (r) { return r.blob(); }).then(function (b) {
      var fr = new FileReader(); fr.onload = function () { LOGO = fr.result; cb(LOGO); }; fr.readAsDataURL(b);
    }).catch(function () { LOGO = null; cb(null); });
  }
  function pdf(name, cb) {
    loadTips(function (tips) {
      if (!tips) return cb(false);
      lib(function (ok) {
        if (!ok) return cb(false);
        logoData(function (logo) {
          try {
            var doc = new window.jspdf.jsPDF({ unit: 'pt', format: 'letter' }), W = 612, M = 54, y = 0, n = 0;
            // cover: white brand band with the logo, navy field, big 27
            doc.setFillColor(15, 30, 51); doc.rect(0, 0, W, 792, 'F');
            doc.setFillColor(255, 255, 255); doc.rect(0, 0, W, 130, 'F');
            doc.setFillColor(42, 113, 175); doc.rect(0, 130, W, 5, 'F');
            if (logo) { try { doc.addImage(logo, 'PNG', M, 42, 236, 46.8); } catch (e) { } } else { doc.setTextColor(15, 30, 51); doc.setFont('helvetica', 'bold'); doc.setFontSize(20); doc.text('Van Ausdall & Farrar', M, 70); }
            doc.setTextColor(143, 194, 242); doc.setFont('helvetica', 'bold'); doc.setFontSize(170); doc.text('27', M, 350);
            doc.setTextColor(255); doc.setFontSize(34); doc.text('Technology Tips', M, 412); doc.text('for 2027', M, 454);
            doc.setFillColor(143, 194, 242); doc.rect(M, 478, 64, 4, 'F');
            doc.setFont('helvetica', 'normal'); doc.setFontSize(13.5); doc.setTextColor(197, 214, 232);
            doc.text(doc.splitTextToSize(S.sub, W - 2 * M - 40), M, 512);
            ['Information', 'Communication', 'Print', 'Process'].forEach(function (a, i) {
              var x = M + i * 128; doc.setFillColor(27, 61, 102); doc.roundedRect(x, 600, 118, 30, 15, 15, 'F');
              doc.setTextColor(230, 238, 247); doc.setFont('helvetica', 'bold'); doc.setFontSize(10.5); doc.text(a, x + 59, 619, { align: 'center' });
            });
            doc.setFont('helvetica', 'normal'); doc.setFontSize(10.5); doc.setTextColor(143, 194, 242);
            doc.text('Indianapolis, since 1914  |  (317) 634-2913  |  vanausdall.com' + (name ? '  |  Prepared for ' + name : ''), M, 740);
            function page() {
              doc.addPage(); doc.setFillColor(255, 255, 255); doc.rect(0, 0, W, 792, 'F');
              if (logo) { try { doc.addImage(logo, 'PNG', M, 18, 118, 23.4); } catch (e) { } }
              doc.setTextColor(106, 123, 144); doc.setFont('helvetica', 'bold'); doc.setFontSize(10); doc.text('27 TECHNOLOGY TIPS FOR 2027', W - M, 34, { align: 'right' });
              doc.setFillColor(42, 113, 175); doc.rect(0, 52, W, 3, 'F'); y = 92;
            }
            page();
            ['Information', 'Communication', 'Print', 'Process'].forEach(function (a) {
              var set = tips.filter(function (t) { return t.area === a; }); if (!set.length) return;
              if (y > 630) page();
              doc.setFillColor(231, 240, 249); doc.roundedRect(M, y - 16, W - 2 * M, 28, 6, 6, 'F');
              doc.setFillColor(42, 113, 175); doc.rect(M, y - 16, 5, 28, 'F');
              doc.setTextColor(15, 30, 51); doc.setFont('helvetica', 'bold'); doc.setFontSize(12); doc.text(a.toUpperCase(), M + 16, y + 2); y += 36;
              set.forEach(function (t) {
                n++;
                var body = doc.splitTextToSize(t.tip, W - 2 * M - 40), h = 18 + body.length * 14 + 14;
                if (y + h > 730) page();
                doc.setFillColor(42, 113, 175); doc.circle(M + 12, y - 4, 12, 'F'); doc.setTextColor(255); doc.setFontSize(10); doc.setFont('helvetica', 'bold'); doc.text(String(n), M + 12, y - 0.5, { align: 'center' });
                doc.setTextColor(15, 30, 51); doc.setFontSize(12.5); doc.text(doc.splitTextToSize(t.title, W - 2 * M - 40), M + 36, y);
                doc.setFont('helvetica', 'normal'); doc.setFontSize(10.5); doc.setTextColor(66, 84, 107); doc.text(body, M + 36, y + 17);
                y += h;
              });
              y += 8;
            });
            if (y > 590) page();
            doc.setFillColor(15, 30, 51); doc.roundedRect(M, y, W - 2 * M, 112, 10, 10, 'F');
            doc.setTextColor(143, 194, 242); doc.setFont('helvetica', 'bold'); doc.setFontSize(10.5); doc.text('NEXT STEP', M + 22, y + 28);
            doc.setTextColor(255); doc.setFontSize(15); doc.text('Want help with any of these?', M + 22, y + 50);
            doc.setFont('helvetica', 'normal'); doc.setFontSize(10.5); doc.setTextColor(197, 214, 232);
            doc.text(doc.splitTextToSize('A Van Ausdall & Farrar specialist can walk your office, show where you stand and build a short plan with owners and dates. Call ' + C.phone + ' or visit ' + C.site + '/technology-strength-assessment.', W - 2 * M - 44), M + 22, y + 68);
            var N = doc.getNumberOfPages();
            for (var i = 2; i <= N; i++) {
              doc.setPage(i); doc.setDrawColor(219, 229, 240); doc.line(M, 752, W - M, 752);
              doc.setFont('helvetica', 'normal'); doc.setFontSize(8.5); doc.setTextColor(106, 123, 144);
              doc.text('Van Ausdall & Farrar  |  6430 E 75th Street, Indianapolis, IN 46250  |  (317) 634-2913  |  vanausdall.com', M, 768);
              doc.text(String(i - 1), W - M, 768, { align: 'right' });
            }
            doc.save('27-Technology-Tips-for-2027.pdf');
            cb(true);
          } catch (e) { cb(false); }
        });
      });
    });
  }

  function pill() {
    if (d.querySelector('.vp-pill') || (parseInt(ls('vafTipsSeen') || '0', 10) > Date.now() + 864e5)) return;
    var b = mk('button', 'vp-pill', '<span class="vp-pill__bk" aria-hidden="true"></span>' + esc(S.pill)); b.type = 'button'; b.setAttribute('aria-label', S.headline);
    b.onclick = function () { open(true); }; d.body.appendChild(b); requestAnimationFrame(function () { b.classList.add('is-on'); });
  }
  function init() {
    window.VAF_TIPS_OPEN = function () { loadSettings(function () { open(true); }); };
    document.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('a[href="#tips"],[data-vaf-tips]');
      if (a) { e.preventDefault(); window.VAF_TIPS_OPEN(); }
    });
    loadSettings(function () {
      if (S.enabled.toLowerCase() !== 'yes' || excluded()) return;
      setTimeout(pill, 6000);
      if (cooled()) return;
      var ready = false, scrolled = false, fired = false;
      function go() { if (!fired && ready && scrolled && !document.querySelector('.vp')) { fired = true; open(false); } }
      setTimeout(function () { ready = true; go(); }, parseFloat(S.delay_seconds) * 1000);
      window.addEventListener('scroll', function () { if (!scrolled && window.scrollY > window.innerHeight * 0.25) { scrolled = true; go(); } }, { passive: true });
      if (window.matchMedia('(hover:hover)').matches) document.addEventListener('mouseout', function (e) { if (!fired && e.clientY <= 0 && !e.relatedTarget && ready) { scrolled = true; go(); } });
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
