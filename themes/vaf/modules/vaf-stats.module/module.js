/* vaf-stats: count the large figures up when they scroll into view. Skipped for reduced motion and for years. */
(function () {
  'use strict';
  var rm = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function run(el) {
    var txt = el.textContent.trim(), m = txt.match(/^([^0-9]*)([0-9][0-9,]*)(\.[0-9]+)?(.*)$/);
    if (!m) return;
    var pre = m[1], dec = m[3] || '', suf = m[4], comma = m[2].indexOf(',') > -1;
    var target = parseFloat(m[2].replace(/,/g, '') + dec), places = dec ? dec.length - 1 : 0, t0 = null;
    function fmt(v) {
      var f = v.toFixed(places);
      if (comma) { var p = f.split('.'); p[0] = p[0].replace(/\B(?=(\d{3})+(?!\d))/g, ','); f = p.join('.'); }
      return pre + f + suf;
    }
    function step(ts) {
      if (t0 === null) t0 = ts;
      var k = Math.min(1, (ts - t0) / 1400);
      k = 1 - Math.pow(1 - k, 3);
      el.textContent = fmt(target * k);
      if (k < 1) requestAnimationFrame(step); else el.textContent = txt;
    }
    el.textContent = fmt(0);
    requestAnimationFrame(step);
  }
  /* one size per row of figures: the smallest size any figure needs, so the numbers read as a set */
  function equalise() {
    [].forEach.call(document.querySelectorAll('.vaf-stats__grid'), function (g) {
      var bs = g.querySelectorAll('.pv-stat b'), min = Infinity, i;
      g.style.removeProperty('--vaf-fs');
      for (i = 0; i < bs.length; i++) bs[i].style.removeProperty('font-size');
      for (i = 0; i < bs.length; i++) min = Math.min(min, parseFloat(getComputedStyle(bs[i]).fontSize) || min);
      if (isFinite(min)) g.style.setProperty('--vaf-fs', min + 'px');
    });
  }
  function sizing() {
    equalise();
    var t = 0;
    window.addEventListener('resize', function () { clearTimeout(t); t = setTimeout(equalise, 120); }, { passive: true });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(equalise);
  }
  function init() {
    sizing();
    if (rm || !('IntersectionObserver' in window)) return;
    var els = [].filter.call(document.querySelectorAll('.vaf-stats .pv-stat b'), function (b) {
      if (b.getAttribute('data-vaf-ready')) return false;
      var t = b.textContent.trim().replace(/,/g, ''), n = parseFloat(t);
      return !isNaN(n) && n >= 100 && !(t.length === 4 && n > 1800 && n < 2100);
    });
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { io.unobserve(e.target); run(e.target); } });
    }, { threshold: 0.4 });
    els.forEach(function (b) { b.setAttribute('data-vaf-ready', '1'); io.observe(b); });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
