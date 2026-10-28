/* Reading-progress bar for the blog post. Scoped, no globals. */
(function () {
  var root = document.querySelector('[data-vb-art]');
  var bar = document.querySelector('[data-vb-prog]');
  if (!root || !bar || !bar.parentNode) return;
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var wrap = bar.parentNode, ticking = false;
  function update() {
    ticking = false;
    var r = root.getBoundingClientRect(), vh = window.innerHeight;
    var total = r.height - vh * 0.4, done = vh * 0.4 - r.top;
    var p = Math.max(0, Math.min(1, total > 0 ? done / total : 0));
    wrap.classList.toggle('is-on', p > 0 && p < 1);
    bar.style.transform = 'scaleX(' + p.toFixed(3) + ')';
  }
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
  window.addEventListener('resize', update);
  update();
})();
