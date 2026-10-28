/* VAF article: reading progress, table of contents scroll-spy, collapsible contents on small screens. */
(function () {
  var rm = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  function init(root) {
    var prose = root.querySelector('.vf-art__prose');
    var links = [].slice.call(root.querySelectorAll('.vf-art__toclist a'));
    var det = root.querySelector('.vf-art__tocd');
    var bar = document.querySelector('[data-vf-prog]');
    var mq = window.matchMedia ? matchMedia('(max-width: 1024px)') : null;
    function fold() { if (det && mq) det.open = !mq.matches; }
    fold();
    if (mq) { if (mq.addEventListener) mq.addEventListener('change', fold); else if (mq.addListener) mq.addListener(fold); }
    function setActive(id) {
      links.forEach(function (a) {
        var on = a.getAttribute('href') === '#' + id;
        a.classList.toggle('is-active', on);
        if (on) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current');
      });
    }
    if ('IntersectionObserver' in window && prose) {
      var heads = [].slice.call(prose.querySelectorAll('.vf-art__chapter h2[id]'));
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) setActive(e.target.id); });
      }, { rootMargin: '-15% 0px -70% 0px', threshold: 0 });
      heads.forEach(function (h) { io.observe(h); });
    }
    var ticking = false;
    function prog() {
      ticking = false;
      if (!bar || !prose) return;
      var r = prose.getBoundingClientRect(), h = r.height - window.innerHeight * 0.6;
      var p = h > 0 ? Math.min(1, Math.max(0, (-r.top + window.innerHeight * 0.2) / h)) : 0;
      bar.style.transform = 'scaleX(' + p.toFixed(4) + ')';
    }
    function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(prog); } }
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll, { passive: true });
    prog();
    if (bar && bar.parentNode) bar.parentNode.classList.add('is-on');
  }
  function boot() { document.querySelectorAll('[data-vf-art]').forEach(init); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
