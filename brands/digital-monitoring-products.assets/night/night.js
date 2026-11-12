/* Night shift scene (Showcase home). Vanilla JS, no dependencies. Source: scripts/preview_night.py notes. */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var NSURI = 'http://www.w3.org/2000/svg';
  var el = function (n, a, p) { var e = document.createElementNS(NSURI, n); for (var k in a) e.setAttribute(k, a[k]); if (p) p.appendChild(e); return e; };

  var ns = $('#ns-ns'), stage = $('#ns-stage'), svg = $('#ns-scene'), wire = $('#ns-wire');
  var mqRM = window.matchMedia('(prefers-reduced-motion: reduce)');
  var mqStack = window.matchMedia('(max-width: 899px), (max-aspect-ratio: 1/1)');
  var reduced = mqRM.matches;
  var stacked = mqStack.matches;
  ns.classList.toggle('rm', reduced); ns.classList.add('ns-js');

  /* ---------- seeded random ---------- */
  var seed = 20071;
  function rnd() { seed |= 0; seed = seed + 0x6D2B79F5 | 0; var t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }

  /* ---------- film grain ---------- */
  (function grain() {
    try {
      var c = document.createElement('canvas'); c.width = c.height = 180;
      var x = c.getContext('2d'), d = x.createImageData(180, 180);
      for (var i = 0; i < d.data.length; i += 4) { var v = 90 + rnd() * 165 | 0; d.data[i] = d.data[i + 1] = d.data[i + 2] = v; d.data[i + 3] = 255; }
      x.putImageData(d, 0, 0);
      $('#ns-grain').style.backgroundImage = 'url(' + c.toDataURL('image/png') + ')';
    } catch (e) { /* grain is decorative */ }
  })();

  /* ---------- time of day ---------- */
  var PAL = {
    sky0: ['#2f7fd6', '#272a68', '#04060e'], sky1: ['#7fc0f0', '#a34f7e', '#0a1233'], sky2: ['#dff1fb', '#ffb46a', '#1d2c58'],
    far: ['#a3c0da', '#7a5580', '#0d1630'], far2: ['#b7d0e2', '#96607f', '#111c3c'], treeFar: ['#5f9a72', '#3c3458', '#081022'],
    lawn: ['#7db868', '#4a4a60', '#0a1422'], wallA: ['#c48f73', '#94605a', '#1c2138'], wallB: ['#ece5d9', '#c39a94', '#2c3454'],
    wallC: ['#d9c7ae', '#a4767a', '#20263f'], trim: ['#444956', '#33294a', '#070a14'],
    winLit: ['#a7d2ee', '#ffd58f', '#ffcf6b'], winOff: ['#7fb4dc', '#6a5b8c', '#0e1730'], winHot: ['#c4e2f6', '#ffe4ad', '#ffe19a'], winPanel: ['#8fbfe2', '#8a7fb0', '#2c4f86'],
    asphalt: ['#8a8f99', '#4d4460', '#0c1020'], asphalt2: ['#676c76', '#372f4c', '#04060c'], walk: ['#cfd2d8', '#7c6d90', '#181d33'], paint: ['#f4f4f4', '#b7a8c8', '#313b5e'],
    tree: ['#3f8448', '#2e2a4a', '#060b16'], treeHi: ['#62aa5e', '#4b4069', '#0e1a33'], trunk: ['#5b4636', '#2a2238', '#04070d'],
    fg: ['#18301f', '#120d20', '#010206'], car: ['#b8403c', '#5d3150', '#10152a'],
    cloud: ['#ffffff', '#ffc9a8', '#2a3766'], cloudSh: ['#cfe2f3', '#c9788a', '#141c3c'], rim: ['#ffffff', '#ffb070', '#86a4ee'], fog: ['#ffffff', '#ffc7a0', '#8fa6e0']
  };
  function hex(h) { return [parseInt(h.substr(1, 2), 16), parseInt(h.substr(3, 2), 16), parseInt(h.substr(5, 2), 16)]; }
  var PALRGB = {}; Object.keys(PAL).forEach(function (k) { PALRGB[k] = PAL[k].map(hex); });
  function ss(a, b, x) { var t = Math.max(0, Math.min(1, (x - a) / (b - a))); return t * t * (3 - 2 * t); }
  var T = 1, tod = $('#ns-tod'), sun = $('#ns-sun'), todBtns = $$('.tod-b');
  function setT(t, fromInput) {
    T = Math.max(0, Math.min(1, t));
    var i = T < 0.5 ? 0 : 1, f = T < 0.5 ? T / 0.5 : (T - 0.5) / 0.5, st = ns.style;
    for (var k in PALRGB) { var a = PALRGB[k][i], b = PALRGB[k][i + 1]; st.setProperty('--' + k, 'rgb(' + Math.round(a[0] + (b[0] - a[0]) * f) + ',' + Math.round(a[1] + (b[1] - a[1]) * f) + ',' + Math.round(a[2] + (b[2] - a[2]) * f) + ')'); }
    st.setProperty('--n', ss(0.3, 0.9, T).toFixed(3));
    st.setProperty('--d', (1 - ss(0.1, 0.5, T)).toFixed(3));
    st.setProperty('--stars', ss(0.55, 1, T).toFixed(3));
    st.setProperty('--dusk', Math.pow(Math.max(0, 1 - Math.abs(T - 0.5) * 2.2), 1.3).toFixed(3));
    st.setProperty('--scrim', (1 - 0.25 * ss(0.2, 1, T)).toFixed(3));
    sun.setAttribute('transform', 'translate(' + (1230 + T * 60).toFixed(0) + ' ' + (190 + Math.pow(Math.min(1, T / 0.62), 1.6) * 470).toFixed(0) + ')');
    if (!fromInput) tod.value = Math.round(T * 100);
    tod.setAttribute('aria-valuetext', T < 0.25 ? 'Day' : T < 0.7 ? 'Dusk' : 'Night');
    todBtns[0].classList.toggle('ns-is-on', T < 0.25); todBtns[1].classList.toggle('ns-is-on', T > 0.75);
    todBtns[0].setAttribute('aria-pressed', T < 0.25); todBtns[1].setAttribute('aria-pressed', T > 0.75);
  }
  var tw = null;
  function tweenT(to, dur) {
    if (tw) cancelAnimationFrame(tw);
    if (reduced || !dur) { setT(to); return; }
    var from = T, t0 = performance.now();
    (function step(now) { var p = Math.min(1, (now - t0) / dur), e = p < 0.5 ? 2 * p * p : 1 - Math.pow(-2 * p + 2, 2) / 2; setT(from + (to - from) * e); if (p < 1) tw = requestAnimationFrame(step); else tw = null; })(t0);
  }
  tod.addEventListener('input', function () { if (tw) { cancelAnimationFrame(tw); tw = null; } setT(tod.value / 100, true); });
  todBtns.forEach(function (b) { b.addEventListener('click', function () { tweenT(+b.dataset.t, 1600); }); });
  var qT = /[?&]t=([\d.]+)/.exec(location.search);
  setT(1);

  /* ---------- camera + parallax + cloud ---------- */
  var M = { W: 0, H: 0, s: 1, ox: 0, oy: 0 }, cam = { x: 0, y: 0, z: 1 };
  function measure() { M.W = stage.clientWidth; M.H = stage.clientHeight; M.s = Math.max(M.W / 1600, M.H / 900); M.ox = (M.W - 1600 * M.s) / 2; M.oy = (M.H - 900 * M.s) / 2; }
  function setCam(c, dur) {
    cam = c;
    svg.style.transition = (dur && !reduced) ? 'transform ' + dur + 'ms cubic-bezier(.62,.02,.2,1)' : 'none';
    svg.style.transform = 'translate(' + c.x.toFixed(1) + 'px,' + c.y.toFixed(1) + 'px) scale(' + c.z + ')';
  }
  function camAt(u, v, z, qx, qy) {
    var x = qx - (u * M.s + M.ox) * z, y = qy - (v * M.s + M.oy) * z;
    x = Math.min(-(-380 * M.s + M.ox) * z, Math.max(M.W - (1980 * M.s + M.ox) * z, x));
    y = Math.min(-(-280 * M.s + M.oy) * z, Math.max(M.H - (1000 * M.s + M.oy) * z, y));
    return { x: x, y: y, z: z };
  }
  function scr(u, v, c) { c = c || cam; return [(u * M.s + M.ox) * c.z + c.x + stage.offsetLeft, (v * M.s + M.oy) * c.z + c.y + stage.offsetTop]; }
  function base() { return stacked ? camAt(890, 500, 1.12, M.W / 2, M.H * 0.6) : { x: 0, y: 0, z: 1 }; }
  function seqBase() {
    if (stacked) return camAt(890, 480, 1.12, M.W / 2, M.H * 0.56);
    var free = $('#ns-cards').getBoundingClientRect().left - ns.getBoundingClientRect().left - 20;
    return camAt(880, 450, 1, Math.max(free / 2, 300), (450 * M.s + M.oy));
  }

  var planes = $$('.pl').map(function (g) { return { g: g, d: parseFloat(g.dataset.d) }; });
  var cloud = $('#ns-cloud'), farClouds = $('#ns-farClouds');
  var CLOUD = { x: 1085, y: 262 }, par = { x: 0, y: 0, tx: 0, ty: 0 }, frozen = false, running = true;
  stage.addEventListener('pointermove', function (e) {
    if (e.pointerType === 'touch') return;
    var r = stage.getBoundingClientRect(); par.tx = ((e.clientX - r.left) / r.width - 0.5) * 2; par.ty = ((e.clientY - r.top) / r.height - 0.5) * 2;
  });
  stage.addEventListener('pointerleave', function () { par.tx = 0; par.ty = 0; });
  var lite = false, onscreen = false, played = false, last = 0, slow = 0, seen = 0;
  function goLite() { lite = true; ns.classList.add('ns-lite'); planes.forEach(function (p) { p.g.removeAttribute('transform'); }); }
  function frame(now) {
    if (!running) return;
    if (!reduced && !lite) {
      /* frame-time guard: 12 slow frames in the first 90 and the scene goes still */
      if (last && seen < 90) { seen++; if (now - last > 34) slow++; if (slow >= 12) goLite(); }
      last = now;
      var tx = frozen ? 0 : par.tx, ty = frozen ? 0 : par.ty;
      par.x += (tx - par.x) * 0.06; par.y += (ty - par.y) * 0.06;
      for (var i = 0; i < planes.length; i++) planes[i].g.setAttribute('transform', 'translate(' + (-par.x * 20 * planes[i].d).toFixed(2) + ' ' + (-par.y * 9 * planes[i].d).toFixed(2) + ')');
      if (!frozen) {
        CLOUD.x = 1085 + Math.sin(now / 16000) * 62; CLOUD.y = 262 + Math.sin(now / 9000) * 4;
        cloud.setAttribute('transform', 'translate(' + CLOUD.x.toFixed(2) + ' ' + CLOUD.y.toFixed(2) + ')');
      }
    }
    if (running && !reduced && !lite) requestAnimationFrame(frame);
  }
  function setRun() {
    var r = onscreen && !document.hidden;
    ns.classList.toggle('ns-off', !r);
    if (r && !running) { running = true; last = 0; requestAnimationFrame(frame); } else running = r;
    if (r && !played) { played = true; if (!reduced && !/[?&]t=/.test(location.search)) { setT(0.46); setTimeout(function () { tweenT(1, 2600); }, 250); } }
  }
  running = false;
  if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { onscreen = es[es.length - 1].isIntersecting; setRun(); }, { threshold: 0.05 }).observe(ns);
  else { onscreen = true; setRun(); }

  /* ---------- hotspots + product card ---------- */
  
  var SPOTS = {};
  $$('#ns-points li').forEach(function (li) { var d = li.dataset; SPOTS[d.k] = { chip: d.chip, where: d.where, name: d.name, kind: d.kind, img: d.img, alt: d.alt, fact: d.fact, href: d.href }; });
  var UV = { roof: [760, 340], stair: [900, 426], win: [702, 584], door: [900, 612], panel: [1138, 582], side: [1356, 618], gate: [338, 592], phone: [1166, 790] };
  var pcard = $('#ns-pcard'), cur = null, pinned = false, closeT = null, lead = null;
  var hsEls = {}; $$('.hs').forEach(function (h) { hsEls[h.dataset.k] = h; h.setAttribute('aria-expanded', 'false'); });
  var chipList = $('#ns-chipList'), chips = {};
  Object.keys(SPOTS).forEach(function (k) {
    var li = document.createElement('li'), b = document.createElement('button');
    b.type = 'button'; b.className = 'chip'; b.textContent = SPOTS[k].chip; b.setAttribute('aria-pressed', 'false');
    b.addEventListener('click', function () { if (cur === k) closeSpot(); else { openSpot(k, true); } });
    li.appendChild(b); chipList.appendChild(li); chips[k] = b;
    
  });
  function idle() { return ns.dataset.seq === 'idle'; }
  function placeCard() {
    if (!cur) return;
    if (lead) { lead.remove(); lead = null; }
    if (stacked) { pcard.style.left = ''; pcard.style.top = ''; return; }
    var sr = stage.getBoundingClientRect(), r = $('.hs-ring', hsEls[cur]).getBoundingClientRect();
    var cx = r.left + r.width / 2 - sr.left, cy = r.top + r.height / 2 - sr.top, w = pcard.offsetWidth, h = pcard.offsetHeight;
    var left = cx + 46, side = 1; if (left + w > M.W - 16) { left = cx - 46 - w; side = -1; }
    var top = Math.max(84, Math.min(M.H - h - 20, cy - h * 0.42));
    pcard.style.left = left + 'px'; pcard.style.top = top + 'px';
    lead = el('path', { 'class': 'ns-lead', d: 'M' + (cx + side * 16) + ' ' + cy + 'L' + (side > 0 ? left : left + w) + ' ' + Math.max(top + 16, Math.min(top + h - 16, cy)) }, wire);
  }
  function openSpot(k, pin) {
    if (!idle()) return;
    clearTimeout(closeT);
    if (cur && cur !== k) { hsEls[cur].classList.remove('ns-is-on'); hsEls[cur].setAttribute('aria-expanded', 'false'); chips[cur].setAttribute('aria-pressed', 'false'); }
    var s = SPOTS[k]; cur = k; pinned = !!pin;
    $('#ns-pcWhere').textContent = s.where; $('#ns-pcName').textContent = s.name; $('#ns-pcKind').textContent = s.kind; $('#ns-pcFact').textContent = s.fact;
    var im = $('#ns-pcImg'); im.src = s.img; im.alt = s.alt; $('#ns-pcGo').href = s.href; $('#ns-pcGo').setAttribute('aria-label', 'View the ' + s.name);
    hsEls[k].classList.add('ns-is-on'); hsEls[k].setAttribute('aria-expanded', 'true'); chips[k].setAttribute('aria-pressed', 'true');
    ns.classList.add('has-card'); pcard.hidden = false; pcard.style.animation = 'none'; void pcard.offsetWidth; pcard.style.animation = '';
    if (stacked) { setCam(camAt(UV[k][0], UV[k][1], 1.45, M.W / 2, M.H * 0.34), 700); if (pin) window.scrollTo({ top: stage.getBoundingClientRect().top + window.pageYOffset - hdTop(), behavior: reduced ? 'auto' : 'smooth' }); }
    placeCard();
  }
  function closeSpot() {
    clearTimeout(closeT);
    if (!cur) return;
    hsEls[cur].classList.remove('ns-is-on'); hsEls[cur].setAttribute('aria-expanded', 'false'); chips[cur].setAttribute('aria-pressed', 'false');
    cur = null; pinned = false; pcard.hidden = true; ns.classList.remove('has-card'); if (lead) { lead.remove(); lead = null; }
    if (stacked && idle()) setCam(base(), 600);
  }
  function later() { clearTimeout(closeT); closeT = setTimeout(function () { if (!pinned && !pcard.contains(document.activeElement)) closeSpot(); }, 260); }
  var canHover = window.matchMedia('(hover: hover)').matches;
  Object.keys(hsEls).forEach(function (k) {
    var h = hsEls[k];
    if (canHover) {
      h.addEventListener('pointerenter', function (e) { if (e.pointerType !== 'touch' && !(pinned && cur !== k)) openSpot(k, pinned && cur === k); });
      h.addEventListener('pointerleave', function (e) { if (e.pointerType !== 'touch') later(); });
    }
    h.addEventListener('focus', function () { if (h.matches(':focus-visible') && cur !== k) openSpot(k, false); });
    h.addEventListener('blur', function () { later(); });
    h.addEventListener('click', function () { if (cur === k && pinned) closeSpot(); else openSpot(k, true); });
    h.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); if (cur === k && pinned) closeSpot(); else openSpot(k, true); }
      else if (e.key === 'Escape') closeSpot();
    });
  });
  pcard.addEventListener('pointerenter', function () { clearTimeout(closeT); });
  pcard.addEventListener('pointerleave', function (e) { if (e.pointerType !== 'touch') later(); });
  $('#ns-pcClose').addEventListener('blur', later);
  $('#ns-pcClose').addEventListener('click', function () { var k = cur; closeSpot(); if (k && !stacked) hsEls[k].focus(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && cur) closeSpot(); });
  stage.addEventListener('click', function (e) { if (cur && pinned && !e.target.closest('.hs') && !e.target.closest('.pcard') && !e.target.closest('.ns-top')) closeSpot(); });

  /* ---------- test alarm ---------- */
  var runBtn = $('#ns-runBtn'), runLabel = $('#ns-runLabel'), resetBtn = $('#ns-resetBtn'), stepnav = $('#ns-stepnav'), caption = $('#ns-caption');
  var rail = $$('#ns-rail li'), cMc = $('#ns-cMc'), cPh = $('#ns-cPh'), cCam = $('#ns-cCam'), statusText = $('#ns-statusText');
  var CAPS = [caption.textContent].concat(rail.map(function (li) { return $('span', li).textContent; }));
  var timers = [], anims = [], step = 0, segEls = {};
  function at(ms, fn) { timers.push(setTimeout(fn, ms)); }
  function clearTimers() { timers.forEach(clearTimeout); timers = []; anims.forEach(function (a) { try { a.cancel(); } catch (e) { } }); anims = []; }

  function segPaths() {
    var c = cam, P = function (k) { return scr(UV[k][0], UV[k][1], c); };
    var s = P('win'), p = P('panel'), m = scr(760, 312, c), cl = scr(CLOUD.x, CLOUD.y, c), roofY = scr(0, 392, c)[1];
    var d = {
      A: 'M' + s[0] + ' ' + s[1] + 'Q' + (s[0] + p[0]) / 2 + ' ' + (s[1] + 70 * M.s) + ' ' + p[0] + ' ' + p[1],
      B: 'M' + p[0] + ' ' + p[1] + 'L' + p[0] + ' ' + roofY + 'L' + m[0] + ' ' + roofY + 'L' + m[0] + ' ' + m[1],
      C: 'M' + m[0] + ' ' + m[1] + 'Q' + (m[0] + (cl[0] - m[0]) * 0.25) + ' ' + (cl[1] - 60 * M.s) + ' ' + (cl[0] - 60 * M.s) + ' ' + cl[1]
    };
    if (!stacked) {
      var nr = ns.getBoundingClientRect(), R = function (e) { var r = e.getBoundingClientRect(); return { l: r.left - nr.left, t: r.top - nr.top, w: r.width, h: r.height }; };
      var a = R(cMc), b = R(cPh), e = R(cCam), x0 = cl[0] + 70 * M.s;
      d.D = 'M' + x0 + ' ' + cl[1] + 'C' + (x0 + (a.l - x0) * 0.5) + ' ' + (cl[1] - 40) + ' ' + (a.l - 60) + ' ' + (a.t + a.h / 2) + ' ' + a.l + ' ' + (a.t + a.h / 2);
      d.E = 'M' + (a.l + 26) + ' ' + (a.t + a.h) + 'L' + (b.l + 26) + ' ' + b.t;
      d.F = 'M' + (b.l + 26) + ' ' + (b.t + b.h) + 'L' + (e.l + 26) + ' ' + e.t;
    }
    return d;
  }
  function drawSeg(id, animate, dur) {
    var d = segPaths()[id]; if (!d) return;
    if (segEls[id]) segEls[id].remove();
    var p = el('path', { 'class': 'trail' + (id === 'A' ? ' dotted' : '') + (id === 'C' ? ' beam' : ''), d: d }, wire);
    segEls[id] = p;
    if (!animate) return;
    var L = p.getTotalLength(), head = el('circle', { 'class': 'head', r: id === 'C' ? 6 : 4.5 }, wire), t0 = performance.now();
    if (id !== 'A') { p.style.strokeDasharray = L; p.style.strokeDashoffset = L; } else p.style.opacity = 0;
    (function mv(now) {
      var k = Math.min(1, (now - t0) / dur), e = 1 - Math.pow(1 - k, 2.2), pt = p.getPointAtLength(L * e);
      head.setAttribute('cx', pt.x); head.setAttribute('cy', pt.y);
      if (id !== 'A') p.style.strokeDashoffset = L * (1 - e); else p.style.opacity = e;
      if (k < 1 && p.isConnected) requestAnimationFrame(mv); else head.remove();
    })(t0);
  }
  function clearWires() { Object.keys(segEls).forEach(function (k) { segEls[k].remove(); }); segEls = {}; $$('.head', wire).forEach(function (h) { h.remove(); }); }
  function show(card, on) { card.classList.toggle('show', on); card.setAttribute('aria-hidden', on ? 'false' : 'true'); }
  function curCard(card) { [cMc, cPh, cCam].forEach(function (c) { c.classList.toggle('cur', c === card); c.classList.toggle('ns-hot', c === card); }); }

  /* cumulative state for step n (0..6). Animated extras are layered on by the timeline. */
  function applyStep(n, animated) {
    step = n;
    for (var i = 1; i <= 6; i++) ns.classList.toggle('s' + i, n >= i);
    ns.classList.toggle('alarm', n >= 1 && n < 6);
    rail.forEach(function (li, i) { li.classList.toggle('is-done', i + 1 < n); li.classList.toggle('is-now', i + 1 === n); if (i + 1 === n) li.setAttribute('aria-current', 'step'); else li.removeAttribute('aria-current'); });
    caption.textContent = CAPS[n];
    statusText.textContent = n === 0 ? 'Armed' : n < 6 ? 'In alarm, demo' : 'Armed, alarm cancelled';
    hsEls.win.classList.toggle('alert', n >= 2 && n < 6);
    hsEls.panel.classList.toggle('alert', n >= 3 && n < 6);
    hsEls.roof.classList.toggle('alert', n >= 4 && n < 6);
    hsEls.phone.classList.toggle('alert', n >= 5 && n < 6);
    if (!animated) {
      clearWires();
      if (n >= 3) drawSeg('A'); if (n >= 4) { drawSeg('B'); drawSeg('C'); drawSeg('D'); } if (n >= 5) { drawSeg('E'); drawSeg('F'); }
      show(cMc, n >= 4); show(cPh, n >= 5); show(cCam, n >= 5);
      cCam.classList.toggle('ver', n >= 5); cPh.classList.toggle('tap', n >= 6);
      curCard(n >= 6 ? cPh : n >= 5 ? cCam : n >= 4 ? cMc : null);
    }
  }
  function prep() {
    closeSpot(); clearTimers(); clearWires(); frozen = true;
    [cMc, cPh, cCam].forEach(function (c) { show(c, false); c.classList.remove('ver', 'tap', 'anim-tap', 'cur', 'ns-hot'); });
    stage.classList.remove('shake', 'flashing');
    if (stacked) window.scrollTo({ top: ns.getBoundingClientRect().top + window.pageYOffset - hdTop(), behavior: reduced ? 'auto' : 'smooth' });
  }
  function runAnimated() {
    prep(); ns.dataset.seq = 'run'; measure(); ns.classList.add('anim'); applyStep(0, true);
    runBtn.disabled = true; runLabel.textContent = 'Test alarm running'; resetBtn.hidden = true;
    var sb = seqBase(), zoom = stacked ? 1.7 : 1.55;
    var push = camAt(702, 570, zoom, stacked ? M.W / 2 : Math.min(M.W * 0.42, sb.x + (702 * M.s + M.ox) + 120), M.H * 0.52);
    setCam(push, 1000);
    at(1000, function () { applyStep(1, true); stage.classList.add('flashing', 'shake'); });
    at(1900, function () { applyStep(2, true); });
    at(2500, function () { setCam(sb, 950); });
    at(3550, function () { drawSeg('A', true, 600); });
    at(4150, function () { applyStep(3, true); });
    at(4700, function () { drawSeg('B', true, 520); });
    at(5220, function () { applyStep(4, true); drawSeg('C', true, 620); ns.classList.remove('s4'); });
    at(5840, function () { ns.classList.add('s4'); drawSeg('D', true, 640); });
    at(6400, function () { show(cMc, true); curCard(cMc); });
    at(7250, function () { drawSeg('E', true, 380); });
    at(7600, function () { applyStep(5, true); show(cPh, true); curCard(cPh); });
    at(8300, function () { drawSeg('F', true, 380); });
    at(8650, function () { show(cCam, true); curCard(cCam); });
    at(9700, function () { cCam.classList.add('ver'); });
    at(10300, function () { curCard(cPh); cPh.classList.add('tap', 'anim-tap'); });
    at(10750, function () { applyStep(6, true); });
    at(12000, function () { ns.dataset.seq = 'done'; ns.classList.remove('anim'); runBtn.disabled = false; runLabel.textContent = 'Replay test alarm'; resetBtn.hidden = false; });
  }
  function runStepped() {
    prep(); ns.dataset.seq = 'step'; stepnav.hidden = false; resetBtn.hidden = true; measure();
    setCam(seqBase(), 0); goStep(1); $('#ns-nextBtn').focus();
  }
  function goStep(n) {
    n = Math.max(1, Math.min(6, n)); applyStep(n, false);
    $('#ns-prevBtn').disabled = n === 1; $('#ns-nextBtn').disabled = n === 6;
    $('#ns-nextBtn').textContent = n === 6 ? 'Resolved' : 'Next step';
    if (n === 6) $('#ns-exitBtn').focus(); else if (n === 1 && document.activeElement === $('#ns-prevBtn')) $('#ns-nextBtn').focus();
  }
  function reset(focusRun) {
    clearTimers(); clearWires(); ns.classList.remove('anim'); ns.dataset.seq = 'idle'; measure(); applyStep(0, false);
    stepnav.hidden = true; resetBtn.hidden = true; runBtn.disabled = false; runLabel.textContent = 'Run a test alarm';
    stage.classList.remove('shake', 'flashing'); frozen = false; setCam(base(), 700);
    if (focusRun) runBtn.focus();
  }
  runBtn.addEventListener('click', function () { if (reduced) runStepped(); else runAnimated(); });
  resetBtn.addEventListener('click', function () { reset(true); });
  $('#ns-exitBtn').addEventListener('click', function () { reset(true); });
  $('#ns-nextBtn').addEventListener('click', function () { goStep(step + 1); });
  $('#ns-prevBtn').addEventListener('click', function () { goStep(step - 1); });

  /* ---------- layout + preference changes ---------- */
  function relayout() {
    stacked = mqStack.matches; measure();
    var s = ns.dataset.seq;
    if (s === 'idle') { setCam(base(), 0); if (cur) { if (stacked) setCam(camAt(UV[cur][0], UV[cur][1], 1.45, M.W / 2, M.H * 0.34), 0); placeCard(); } }
    else if (s === 'run') { reset(false); }
    else { setCam(seqBase(), 0); applyStep(step, false); }
  }
  var rz; window.addEventListener('resize', function () { clearTimeout(rz); rz = setTimeout(relayout, 80); });
  (mqRM.addEventListener ? mqRM.addEventListener.bind(mqRM, 'change') : mqRM.addListener.bind(mqRM))(function () {
    reduced = mqRM.matches; ns.classList.toggle('rm', reduced); if (ns.dataset.seq !== 'idle') reset(false);
    if (reduced) { planes.forEach(function (p) { p.g.removeAttribute('transform'); }); }
  });
  document.addEventListener('visibilitychange', setRun);
  measure(); setCam(base(), 0);

  /* round 3b: the sticky header's painted height is measured (its last bar's bottom edge), not assumed to be 96px.
     Measured when the section comes on screen, because the header is taller at the very top of the page. */
  var nsSec = ns.closest ? (ns.closest('.pn-night') || ns) : ns, nsHd = document.querySelector('.q-header');
  if (nsHd) { var nsHp = getComputedStyle(nsHd).position; if (nsHp !== 'sticky' && nsHp !== 'fixed') nsHd = null; }
  function hdTop() {
    var t = nsHd ? Math.max(0, Math.round((nsHd.lastElementChild || nsHd).getBoundingClientRect().bottom)) : 0;
    if (t !== hdTop.last) { hdTop.last = t; nsSec.style.setProperty('--ns-top', t + 'px'); }
    return t;
  }
  if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { if (es[0].isIntersecting) { var b = hdTop.last; hdTop(); if (b !== hdTop.last && !stacked) relayout(); } }, { rootMargin: '0px 0px -30% 0px' }).observe(nsSec);

  /* test hook for deterministic screenshots */
  window.__ns = { get lite() { return lite; }, get running() { return running; }, setT: setT, open: openSpot, close: closeSpot, step: function (n) { prep(); ns.dataset.seq = 'step'; stepnav.hidden = false; measure(); setCam(seqBase(), 0); goStep(n); }, reset: reset };
})();
