(function () {
  document.querySelectorAll('[data-vaf-sc]').forEach(function (root) {
    var panels = [].slice.call(root.querySelectorAll('.vaf-sc__panel')), links = [].slice.call(root.querySelectorAll('.vaf-sc__nav a')), bar = root.querySelector('.vaf-sc__prog i');
    if (!panels.length || !('IntersectionObserver' in window)) { panels.forEach(function (p) { p.classList.add('is-on'); }); return; }
    function set(i) {
      links.forEach(function (a, k) { a.classList.toggle('is-on', k === i); });
      if (bar) bar.style.width = ((i + 1) / panels.length * 100) + '%';
    }
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('is-on'); set(+e.target.getAttribute('data-i')); }
      });
    }, { rootMargin: '-35% 0px -45% 0px', threshold: 0 });
    panels.forEach(function (p) { io.observe(p); });
    set(0);
  });
})();
