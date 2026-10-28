/* vaf-hero: pointer depth + glow, particle network, background video control, stat count-up.
   Every selector is scoped to a .vaf-hero root, so several instances on a page are safe. */
(function () {
  'use strict';
  var mq = function (q) { return window.matchMedia ? window.matchMedia(q) : { matches: false }; };
  var reduced = mq('(prefers-reduced-motion: reduce)');
  var fine = mq('(pointer:fine) and (min-width:1025px)');
  var narrow = mq('(max-width: 767px)');
  function onChange(m, fn) {
    if (!m.addEventListener && !m.addListener) return;
    if (m.addEventListener) m.addEventListener('change', fn); else m.addListener(fn);
  }

  /* ---- stat count-up (split layout) ---- */
  function countUp(root) {
    if (reduced.matches || !('IntersectionObserver' in window)) return;
    var els = [].filter.call(root.querySelectorAll('.pv-hero-stats b'), function (b) {
      var t = b.textContent.trim().replace(/,/g, ''), n = parseFloat(t);
      return !isNaN(n) && n >= 100 && !(t.length === 4 && n > 1800 && n < 2100);
    });
    if (!els.length) return;
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        io.unobserve(e.target);
        var el = e.target, txt = el.textContent.trim();
        var m = txt.match(/^([^0-9]*)([0-9][0-9,]*)(\.[0-9]+)?(.*)$/);
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
      });
    }, { threshold: 0.4 });
    els.forEach(function (b) { io.observe(b); });
  }

  /* ---- layered hero: glow follows the pointer, floating cards drift at different depths ---- */
  function depth(h) {
    if (reduced.matches || !fine.matches) return;
    h.addEventListener('pointermove', function (e) {
      var r = h.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
      h.style.setProperty('--mx', ((x + 0.5) * 100).toFixed(1) + '%');
      h.style.setProperty('--my', ((y + 0.5) * 100).toFixed(1) + '%');
      [].forEach.call(h.querySelectorAll('.pv-depth'), function (c) {
        var d = +c.getAttribute('data-depth') || 1;
        c.style.transform = 'translate3d(' + (-x * 10 * d).toFixed(1) + 'px,' + (-y * 10 * d).toFixed(1) + 'px,0) rotateX(' + (y * -4).toFixed(2) + 'deg) rotateY(' + (x * 5).toFixed(2) + 'deg)';
      });
    });
    h.addEventListener('pointerleave', function () {
      [].forEach.call(h.querySelectorAll('.pv-depth'), function (c) { c.style.transform = ''; });
    });
  }

  /* ---- layered hero: slow particle network, only when there is no video and motion is allowed ---- */
  function network(h) {
    var cv = h.querySelector('canvas.net');
    if (!cv || !cv.getContext) return;
    if (reduced.matches || h.querySelector('video[data-src]')) { cv.style.display = 'none'; return; }
    var cx = cv.getContext('2d'), W = 0, H = 0, P = [], run = false, raf = 0;
    var col = (getComputedStyle(h).getPropertyValue('--q-gold') || '').trim() || '#65bc7b';
    function size() {
      var r = h.getBoundingClientRect();
      W = cv.width = Math.floor(r.width); H = cv.height = Math.floor(r.height);
      var n = W < 768 ? 22 : W < 1200 ? 40 : 56;
      P = [];
      for (var i = 0; i < n; i++) P.push({ x: Math.random() * W, y: Math.random() * H, vx: (Math.random() - 0.5) * 0.22, vy: (Math.random() - 0.5) * 0.22, r: 1.2 + Math.random() * 1.8 });
    }
    function tick() {
      if (!run) return;
      cx.clearRect(0, 0, W, H);
      var i, j, a, b, d;
      for (i = 0; i < P.length; i++) {
        a = P[i]; a.x += a.vx; a.y += a.vy;
        if (a.x < 0 || a.x > W) a.vx *= -1;
        if (a.y < 0 || a.y > H) a.vy *= -1;
      }
      cx.lineWidth = 1;
      for (i = 0; i < P.length; i++) {
        a = P[i];
        for (j = i + 1; j < P.length; j++) {
          b = P[j]; d = Math.hypot(a.x - b.x, a.y - b.y);
          if (d < 150) { cx.globalAlpha = (1 - d / 150) * 0.28; cx.strokeStyle = col; cx.beginPath(); cx.moveTo(a.x, a.y); cx.lineTo(b.x, b.y); cx.stroke(); }
        }
      }
      for (i = 0; i < P.length; i++) { a = P[i]; cx.globalAlpha = 0.75; cx.fillStyle = col; cx.beginPath(); cx.arc(a.x, a.y, a.r, 0, 6.283); cx.fill(); }
      cx.globalAlpha = 1;
      raf = requestAnimationFrame(tick);
    }
    size();
    window.addEventListener('resize', size, { passive: true });
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          if (e.isIntersecting && !run) { run = true; tick(); }
          else if (!e.isIntersecting) { run = false; cancelAnimationFrame(raf); }
        });
      }).observe(h);
    } else { run = true; tick(); }
  }

  /* ---- background video: loads after the poster has painted, never on small screens, data saver or reduced motion ---- */
  function video(h) {
    var v = h.querySelector('video[data-src]');
    var btn = h.querySelector('.vaf-hero__toggle');
    if (!v) return;
    var conn = navigator.connection || navigator.mozConnection || navigator.webkitConnection || {};
    var loaded = false, userPaused = false, inView = true;
    v.muted = true;
    function allowed() {
      return !reduced.matches && !narrow.matches && !conn.saveData && !/^(slow-2g|2g|3g)$/.test(conn.effectiveType || '');
    }
    function paint() {
      /* once a frame is decoded the video shows it, playing or paused; the poster stays underneath */
      h.classList.toggle('is-video-playing', loaded && allowed() && v.readyState >= 2);
      if (btn) {
        btn.hidden = !(loaded && allowed());
        btn.classList.toggle('is-paused', userPaused);
        btn.setAttribute('aria-label', btn.getAttribute(userPaused ? 'data-play-label' : 'data-pause-label') || '');
      }
    }
    function play() {
      if (!allowed() || userPaused || !inView) return;
      if (!loaded) { loaded = true; var wm = v.getAttribute('data-src-webm'); v.src = (wm && v.canPlayType('video/webm; codecs="vp9"')) ? wm : v.getAttribute('data-src'); v.load(); }
      var p = v.play();
      if (p && p.catch) p.catch(function () { paint(); });
    }
    function halt() { if (!v.paused) v.pause(); paint(); }
    function sync() { if (allowed()) play(); else halt(); }
    ['playing', 'pause', 'ended', 'canplay'].forEach(function (ev) { v.addEventListener(ev, paint); });
    if (btn) {
      btn.addEventListener('click', function () {
        userPaused = !userPaused;
        if (userPaused) { v.pause(); } else { play(); }
        paint();
      });
    }
    onChange(reduced, sync); onChange(narrow, sync);
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) {
        inView = es[0].isIntersecting;
        if (inView) play(); else if (!v.paused) v.pause();
      }, { threshold: 0.05 }).observe(h);
    }
    function start() { setTimeout(sync, 150); }
    if (document.readyState === 'complete') start(); else window.addEventListener('load', start);
  }

  function init() {
    [].forEach.call(document.querySelectorAll('.vaf-hero'), function (h) {
      if (h.getAttribute('data-vaf-ready')) return;
      h.setAttribute('data-vaf-ready', '1');
      if (h.classList.contains('vaf-hero--layered')) { depth(h); network(h); video(h); }
      if (h.classList.contains('vaf-hero--split')) { countUp(h); }
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
