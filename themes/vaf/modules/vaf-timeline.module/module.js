(function () {
  var rm = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  function init(root) {
    if (root.getAttribute('data-vaf-ready')) return;
    root.setAttribute('data-vaf-ready', '1');
    var sc = root.querySelector('.vaf-tl__scroller');
    var items = [].slice.call(root.querySelectorAll('.vaf-tl__item'));
    var prev = root.querySelector('.vaf-tl__go[data-dir="-1"]'), next = root.querySelector('.vaf-tl__go[data-dir="1"]');
    var bar = root.querySelector('.vaf-tl__bar i');
    var wide = window.matchMedia('(min-width:768px)');
    root.classList.add('is-js');
    function update() {
      var max = sc.scrollWidth - sc.clientWidth, x = sc.scrollLeft;
      var horiz = wide.matches && max > 4;
      if (prev) prev.disabled = !horiz || x < 4;
      if (next) next.disabled = !horiz || x > max - 4;
      sc.style.setProperty('--fade-r', horiz && x < max - 4 ? '70px' : '0px');
      if (bar) {
        var w = horiz ? sc.clientWidth / sc.scrollWidth * 100 : 100;
        bar.style.width = w + '%';
        bar.style.left = horiz ? (x / sc.scrollWidth * 100) + '%' : '0';
      }
      if (!('IntersectionObserver' in window) || !wide.matches) items.forEach(function (li) { li.classList.add('is-seen'); });
    }
    function step(dir) {
      var by = Math.max(sc.clientWidth * 0.8, 330) * dir;
      sc.scrollBy({ left: by, behavior: rm ? 'auto' : 'smooth' });
    }
    if (prev) prev.addEventListener('click', function () { step(-1); });
    if (next) next.addEventListener('click', function () { step(1); });
    sc.addEventListener('scroll', function () { window.requestAnimationFrame(update); }, { passive: true });
    window.addEventListener('resize', update);
    if ('IntersectionObserver' in window) {
      var order = 0;
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          if (e.isIntersecting) {
            var li = e.target; io.unobserve(li);
            li.style.transitionDelay = rm ? '0s' : (order++ * 0.12) + 's';
            li.classList.add('is-seen');
            setTimeout(function () { order = Math.max(0, order - 1); }, 400);
          }
        });
      }, { root: wide.matches ? sc : null, threshold: 0.55 });
      items.forEach(function (li) { io.observe(li); });
    }
    update();
  }
  function boot() { [].forEach.call(document.querySelectorAll('[data-vaf-tl]'), init); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
