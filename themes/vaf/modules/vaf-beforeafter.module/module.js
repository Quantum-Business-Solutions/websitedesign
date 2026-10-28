(function () {
  var rm = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  function init(root) {
    if (root.getAttribute('data-vaf-ready')) return;
    root.setAttribute('data-vaf-ready', '1');
    var stage = root.querySelector('.vaf-ba__stage'), handle = root.querySelector('.vaf-ba__handle');
    var sws = [].slice.call(root.querySelectorAll('.vaf-ba__sw'));
    var pos = 50, raf = 0, drag = false, touched = false;
    root.classList.add('is-js');
    root.setAttribute('data-side', 'before');
    function paint() {
      stage.style.setProperty('--pos', pos + '%');
      handle.setAttribute('aria-valuenow', Math.round(pos));
      handle.setAttribute('aria-valuetext', Math.round(pos) + ' percent');
    }
    function touch() { if (!touched) { touched = true; root.classList.add('is-touched'); } }
    function tween(to, ms) {
      cancelAnimationFrame(raf);
      var from = pos, t0 = null;
      if (rm || !ms) { pos = to; paint(); return; }
      (function f(ts) {
        if (t0 === null) t0 = ts;
        var k = Math.min(1, (ts - t0) / ms); k = 1 - Math.pow(1 - k, 3);
        pos = from + (to - from) * k; paint();
        if (k < 1) raf = requestAnimationFrame(f);
      })(performance.now());
    }
    function fromX(x) {
      var r = stage.getBoundingClientRect();
      return Math.max(8, Math.min(92, (x - r.left) / r.width * 100));
    }
    stage.addEventListener('pointerdown', function (e) {
      if (e.button > 0 || !window.matchMedia('(min-width:900px)').matches) return;
      drag = true; touch(); root.classList.add('is-drag');
      try { stage.setPointerCapture(e.pointerId); } catch (x) {}
      tween(fromX(e.clientX), 180);
    });
    stage.addEventListener('pointermove', function (e) {
      if (!drag) return;
      cancelAnimationFrame(raf); pos = fromX(e.clientX); paint();
    });
    function end() { drag = false; root.classList.remove('is-drag'); }
    stage.addEventListener('pointerup', end); stage.addEventListener('pointercancel', end);
    handle.addEventListener('keydown', function (e) {
      var k = e.key, to = null;
      if (k === 'ArrowLeft' || k === 'ArrowDown') to = pos - 5;
      else if (k === 'ArrowRight' || k === 'ArrowUp') to = pos + 5;
      else if (k === 'PageDown') to = pos - 20;
      else if (k === 'PageUp') to = pos + 20;
      else if (k === 'Home') to = 8;
      else if (k === 'End') to = 92;
      if (to === null) return;
      e.preventDefault(); touch(); tween(Math.max(8, Math.min(92, to)), 160);
    });
    sws.forEach(function (b) {
      b.addEventListener('click', function () {
        var side = b.getAttribute('data-side');
        root.setAttribute('data-side', side);
        sws.forEach(function (x) { var on = x === b; x.classList.toggle('is-on', on); x.setAttribute('aria-pressed', on ? 'true' : 'false'); });
      });
    });
    paint();
    if ('IntersectionObserver' in window && !rm) {
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          if (e.isIntersecting) {
            io.disconnect();
            if (touched || !window.matchMedia('(min-width:900px)').matches) return;
            setTimeout(function () { if (!touched) tween(36, 700); setTimeout(function () { if (!touched) tween(50, 800); }, 900); }, 500);
          }
        });
      }, { threshold: 0.6 });
      io.observe(stage);
    }
  }
  function boot() { [].forEach.call(document.querySelectorAll('[data-vaf-ba]'), init); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
