(function () {
  document.querySelectorAll('[data-walk]').forEach(function (stage) {
    var pins = Array.prototype.slice.call(stage.querySelectorAll('.ro-walk__pin'));
    var cards = Array.prototype.slice.call(stage.querySelectorAll('.ro-walk__card'));
    var count = stage.querySelector('[data-count]'); var active = 0;
    var main = pins.map(function (p, i) { return p.classList.contains('ro-walk__pin--before') ? -1 : i; }).filter(function (i) { return i >= 0; });
    function show(i) {
      if (i < 0) i = pins.length - 1; if (i >= pins.length) i = 0; active = i;
      pins.forEach(function (p, k) { p.classList.toggle('is-active', k === i); p.setAttribute('aria-expanded', k === i ? 'true' : 'false'); });
      cards.forEach(function (c, k) { c.classList.toggle('is-active', k === i); });
      var m = main.indexOf(i); if (count) count.textContent = (m >= 0 ? (m + 1) : '×') + ' / ' + main.length;
    }
    pins.forEach(function (p, i) {
      p.addEventListener('click', function () { show(i); });
      p.addEventListener('mouseenter', function () { if (window.matchMedia('(pointer: fine)').matches) show(i); });
    });
    stage.querySelectorAll('[data-step]').forEach(function (b) { b.addEventListener('click', function () { var m = main.indexOf(active); if (m < 0) m = 0; var n = (m + parseInt(b.getAttribute('data-step'), 10) + main.length) % main.length; show(main[n]); }); });
    stage.querySelectorAll('.ro-walk__tb').forEach(function (b) {
      b.addEventListener('click', function () {
        var after = b.getAttribute('data-state') === 'after';
        stage.classList.toggle('is-after', after);
        stage.querySelectorAll('.ro-walk__tb').forEach(function (x) { x.classList.toggle('is-on', x === b); });
        if (after && pins[active] && pins[active].classList.contains('ro-walk__pin--before')) { var n = pins.findIndex(function (p) { return !p.classList.contains('ro-walk__pin--before'); }); if (n >= 0) show(n); }
      });
    });
    show(0);
    stage.addEventListener('keydown', function (e) { var m = Math.max(0, main.indexOf(active)); if (e.key === 'ArrowRight') show(main[(m + 1) % main.length]); if (e.key === 'ArrowLeft') show(main[(m - 1 + main.length) % main.length]); });
  });
})();
