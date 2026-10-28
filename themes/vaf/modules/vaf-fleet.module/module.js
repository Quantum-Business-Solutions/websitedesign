(function () {
  var rm = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  function init(root) {
    if (root.getAttribute('data-vaf-ready')) return;
    root.setAttribute('data-vaf-ready', '1');
    var rail = root.querySelector('.vaf-fleet__rail');
    var prev = root.querySelector('.vaf-fleet__go[data-dir="-1"]'), next = root.querySelector('.vaf-fleet__go[data-dir="1"]');
    function update() {
      var max = rail.scrollWidth - rail.clientWidth, x = rail.scrollLeft;
      root.classList.toggle('has-overflow', max > 6);
      prev.disabled = x < 4; next.disabled = x > max - 4;
    }
    function step(dir) {
      var card = rail.querySelector('.vaf-fleet__card');
      var by = (card ? card.offsetWidth + 20 : rail.clientWidth * 0.8) * dir;
      rail.scrollBy({ left: by, behavior: rm ? 'auto' : 'smooth' });
    }
    prev.addEventListener('click', function () { step(-1); });
    next.addEventListener('click', function () { step(1); });
    rail.addEventListener('scroll', function () { window.requestAnimationFrame(update); }, { passive: true });
    window.addEventListener('resize', update);
    update();
    window.addEventListener('load', update);
  }
  function boot() { [].forEach.call(document.querySelectorAll('[data-vaf-fleet]'), init); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
