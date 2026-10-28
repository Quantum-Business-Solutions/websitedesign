(function () {
  var rm = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  function init(root) {
    if (root.getAttribute('data-vaf-ready')) return;
    root.setAttribute('data-vaf-ready', '1');
    var stage = root.querySelector('.vaf-3d__stage'), tilt = root.querySelector('.vaf-3d__tilt');
    if (!stage || !tilt || rm) return;
    root.classList.add('is-js');
    var down = false;
    function aim(e) {
      var r = stage.getBoundingClientRect();
      var x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
      tilt.style.setProperty('--ry', (x * 34).toFixed(1) + 'deg');
      tilt.style.setProperty('--rx', (-y * 12).toFixed(1) + 'deg');
    }
    function rest() { tilt.style.setProperty('--ry', '0deg'); tilt.style.setProperty('--rx', '0deg'); root.classList.remove('is-active'); }
    stage.addEventListener('pointerenter', function (e) { if (e.pointerType === 'mouse') { root.classList.add('is-active'); aim(e); } });
    stage.addEventListener('pointermove', function (e) { if (e.pointerType === 'mouse' || down) aim(e); });
    stage.addEventListener('pointerdown', function (e) { down = true; root.classList.add('is-active'); aim(e); });
    stage.addEventListener('pointerup', function () { down = false; rest(); });
    stage.addEventListener('pointercancel', function () { down = false; rest(); });
    stage.addEventListener('pointerleave', function () { if (!down) rest(); });
  }
  function boot() { [].forEach.call(document.querySelectorAll('[data-vaf-3d]'), init); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
