/* Scenes (Showcase home). Progressive enhancement only: without this file every scene is a complete, static composition.
   What it adds: each scene pins for about half a screen of scroll and plays two beats, the product first, then the copy.
   Only transform and opacity change, on three elements per scene, and only for scenes on screen.
   Guards: off under prefers-reduced-motion; off for a scene whose copy does not fit the screen; and a frame-time guard
   that parks every scene in its finished state for good if scrolling cannot hold the frame rate.
   WebGL: not shipped. The prototype's shader path could not be tested on real GPUs, so the CSS path is the only path. */
(function () {
  'use strict';
  var root = document.getElementById('scenes');
  if (!root || !('IntersectionObserver' in window) || !window.CSS || !CSS.supports('position', 'sticky')) return;
  var RM = window.matchMedia('(prefers-reduced-motion: reduce)');
  var S = [].slice.call(root.querySelectorAll('.scn')).map(function (el) { return { el: el, pin: el.querySelector('.scn-pin'), col: el.querySelector('.scn-col'), prod: el.querySelector('.scn-prod'), on: false, live: false, k: -1 }; });
  var lite = false, ticking = false, chained = false, scrolled = 0, last = 0, seen = 0, slow = 0, vh = 0, top = 0, hd;

  function measure() {
    if (hd === undefined) { hd = document.querySelector('.q-header'); var pos = hd ? getComputedStyle(hd).position : ''; if (pos !== 'sticky' && pos !== 'fixed') hd = null; }
    /* the header's painted height is its last bar's bottom edge (the header box itself can be taller than what it paints) */
    var t = hd ? Math.max(0, Math.round((hd.lastElementChild || hd).getBoundingClientRect().bottom)) : 0;
    if (t !== top || !vh) { top = t; root.style.setProperty('--scn-top', top + 'px'); }
    vh = window.innerHeight - top;
  }
  function setLive(s, v) {
    if (s.live === v) return;
    s.live = v; s.el.classList.toggle('scn-live', v);
    if (!v) { s.el.style.removeProperty('--k'); s.k = -1; s.col.style.pointerEvents = ''; }
  }
  function arrange() {
    measure();
    var want = !RM.matches && !lite;
    S.forEach(function (s) {
      setLive(s, false);
      if (!want) return;
      /* pin only when the whole composition fits the screen under the header (offsetHeight ignores transforms) */
      var cs = getComputedStyle(s.pin), one = cs.gridTemplateColumns.split(' ').length < 2, a = s.prod.offsetHeight, b = s.col.offsetHeight;
      var need = parseFloat(cs.paddingTop) + parseFloat(cs.paddingBottom) + (one ? a + b + (parseFloat(cs.rowGap) || 0) : Math.max(a, b));
      if (need <= vh) setLive(s, true);
    });
    update();
  }
  function ease(x) { x = x < 0 ? 0 : x > 1 ? 1 : x; return x * x * (3 - 2 * x); }
  function update(now) {
    ticking = false;
    /* frame-time guard: while the page is being scrolled the loop runs every frame, so now - last is a true frame time */
    if (now && chained && seen < 180 && !lite) { seen++; if (now - last > 40) slow++; if (slow >= 30) { goLite(); return; } }
    last = now || 0; chained = false;
    if (now && seen < 180 && !lite && performance.now() - scrolled < 140 && S.some(function (s) { return s.on && s.live; })) { chained = true; ticking = true; requestAnimationFrame(update); }
    var any = false;
    for (var i = 0; i < S.length; i++) {
      var s = S[i]; if (!s.live || !s.on) continue;
      if (!any) { any = true; measure(); }
      var r = s.el.getBoundingClientRect(), range = r.height - vh, p = range > 0 ? (top - r.top) / range : 1;
      var k = Math.round(ease((p - 0.05) / 0.5) * 1000) / 1000;   /* round 3b: a 138vh scene, so the beat starts sooner and holds for the last 45% */
      if (k !== s.k) { s.k = k; s.el.style.setProperty('--k', k); s.col.style.pointerEvents = k < 0.5 ? 'none' : ''; }
    }
  }
  /* the layout stays exactly as it is (still pinned), the beats just stop: no jump for the reader */
  function goLite() { lite = true; root.classList.add('scn-lite'); S.forEach(function (s) { if (s.live) { s.k = 1; s.el.style.setProperty('--k', 1); s.col.style.pointerEvents = ''; } }); window.removeEventListener('scroll', onScroll); }
  function onScroll() { scrolled = performance.now(); if (!ticking) { ticking = true; requestAnimationFrame(update); } }

  var io = new IntersectionObserver(function (es) { es.forEach(function (e) { for (var i = 0; i < S.length; i++) if (S[i].el === e.target) S[i].on = e.isIntersecting; }); onScroll(); }, { rootMargin: '10% 0px' });
  S.forEach(function (s) {
    io.observe(s.el);
    /* keyboard: a link inside copy that has not arrived yet brings its scene to the second beat */
    s.col.addEventListener('focusin', function () { if (s.live && s.k < 0.95) { var r = s.el.getBoundingClientRect(); window.scrollTo(0, window.pageYOffset + r.top - top + (r.height - vh) * 0.72); } });
  });
  window.addEventListener('scroll', onScroll, { passive: true });
  var rz; window.addEventListener('resize', function () { clearTimeout(rz); rz = setTimeout(arrange, 120); });
  if (RM.addEventListener) RM.addEventListener('change', arrange);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(arrange);
  arrange();
  window.__scn = { get lite() { return lite; }, get live() { return S.map(function (s) { return s.live; }); }, get k() { return S.map(function (s) { return s.k; }); } };
})();
