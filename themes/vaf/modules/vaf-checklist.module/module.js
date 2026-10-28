/* VAF checklist: live score ring, band message, nothing stored. Scoped per instance. */
(function () {
  var C = 2 * Math.PI * 52;
  var rm = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  function init(root) {
    if (root.getAttribute('data-ready')) return;
    root.setAttribute('data-ready', '1');
    var boxes = root.querySelectorAll('.vf-chk__in');
    var total = boxes.length;
    var mid = +root.getAttribute('data-mid') || 4, high = +root.getAttribute('data-high') || 8;
    var msgs = [0, 1, 2, 3].map(function (i) { return root.getAttribute('data-m' + i) || ''; });
    var card = root.querySelector('.vf-chk__card');
    var bar = root.querySelector('.vf-chk__bar');
    var num = root.querySelector('[data-n]');
    var msg = root.querySelector('[data-msg]');
    var sr = root.querySelector('[data-sr]');
    var reset = root.querySelector('[data-reset]');
    var mini = root.querySelector('[data-mini]');
    var minibar = root.querySelector('[data-minibar]');
    var noun = (root.querySelector('.vf-chk__num span') || {}).textContent || '';
    var last = -1;
    bar.style.strokeDasharray = C.toFixed(2);
    function band(n) { return n <= 0 ? 0 : n >= high ? 3 : n >= mid ? 2 : 1; }
    function update(announce) {
      var n = 0;
      boxes.forEach(function (b) { if (b.checked) n++; });
      var bd = band(n);
      bar.style.strokeDashoffset = (C * (1 - (total ? n / total : 0))).toFixed(2);
      num.textContent = n;
      msg.textContent = msgs[bd];
      sr.textContent = n + ' of ' + total + ' ' + noun.replace(/^of\s+\d+\s+/, '') + '. ';
      card.setAttribute('data-band', bd);
      root.setAttribute('data-band', bd);
      reset.hidden = n === 0;
      if (mini) mini.textContent = n + ' of ' + total;
      if (minibar) minibar.style.width = (total ? (n / total) * 100 : 0) + '%';
      if (!rm && n !== last && last !== -1) {
        num.classList.remove('is-bump'); void num.offsetWidth; num.classList.add('is-bump');
      }
      last = n;
      if (!announce) sr.textContent = '';
    }
    boxes.forEach(function (b) { b.addEventListener('change', function () { update(true); }); });
    reset.addEventListener('click', function () {
      boxes.forEach(function (b) { b.checked = false; });
      update(true);
      if (boxes[0]) boxes[0].focus();
    });
    root.classList.add('is-js');
    update(false);
  }
  function boot() { document.querySelectorAll('[data-vf-chk]').forEach(init); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
