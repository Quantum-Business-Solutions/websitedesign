(function () {
  var roots = document.querySelectorAll('[data-vt-car]');
  Array.prototype.forEach.call(roots, function (root) {
    var track = root.querySelector('[data-vt-track]');
    var ctrl = root.querySelector('[data-vt-ctrl]');
    var prev = root.querySelector('[data-vt-prev]');
    var next = root.querySelector('[data-vt-next]');
    var count = root.querySelector('[data-vt-count]');
    var slides = track ? track.querySelectorAll('.vt__slide') : [];
    if (!track || !ctrl || !prev || !next || !slides.length) return;
    ctrl.hidden = false;
    var ticking = false;
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    function step() {
      var a = slides[0], b = slides[1];
      return b ? b.offsetLeft - a.offsetLeft : a.offsetWidth;
    }
    function update() {
      ticking = false;
      var max = track.scrollWidth - track.clientWidth;
      var atStart = track.scrollLeft <= 8, atEnd = track.scrollLeft >= max - 8;
      prev.setAttribute('aria-disabled', atStart ? 'true' : 'false');
      next.setAttribute('aria-disabled', atEnd ? 'true' : 'false');
      var first = Math.round(track.scrollLeft / step());
      var perView = Math.max(1, Math.round(track.clientWidth / step()));
      var last = Math.min(slides.length, first + perView);
      if (atEnd) last = slides.length;
      count.textContent = (perView > 1 ? (first + 1) + ' to ' + last : (first + 1)) + ' of ' + slides.length;
    }
    function go(dir) {
      track.scrollBy({ left: dir * track.clientWidth, behavior: reduce ? 'auto' : 'smooth' });
    }
    prev.addEventListener('click', function () { if (prev.getAttribute('aria-disabled') !== 'true') go(-1); });
    next.addEventListener('click', function () { if (next.getAttribute('aria-disabled') !== 'true') go(1); });
    track.addEventListener('scroll', function () { if (!ticking) { ticking = true; window.requestAnimationFrame(update); } }, { passive: true });
    window.addEventListener('resize', update);
    update();
  });
})();
