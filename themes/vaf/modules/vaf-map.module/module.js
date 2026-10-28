(function () {
  function init(root) {
    if (root.getAttribute('data-vaf-ready')) return;
    root.setAttribute('data-vaf-ready', '1');
    var pins = [].slice.call(root.querySelectorAll('.vaf-map__pin'));
    var rows = [].slice.call(root.querySelectorAll('.vaf-map__row'));
    function hot(i, on) {
      if (pins[i]) pins[i].classList.toggle('is-hot', on);
      if (rows[i]) rows[i].classList.toggle('is-hot', on);
    }
    pins.concat(rows).forEach(function (n) {
      var i = +n.getAttribute('data-i');
      n.addEventListener('mouseenter', function () { hot(i, true); });
      n.addEventListener('mouseleave', function () { hot(i, false); });
      n.addEventListener('focusin', function () { hot(i, true); });
      n.addEventListener('focusout', function () { hot(i, false); });
    });
    root.classList.add('is-js');
    var fig = root.querySelector('.vaf-map__fig');
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { root.classList.add('is-in'); io.disconnect(); } }); }, { threshold: 0.3 });
      io.observe(fig);
    } else root.classList.add('is-in');
  }
  function boot() { [].forEach.call(document.querySelectorAll('[data-vaf-map]'), init); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
