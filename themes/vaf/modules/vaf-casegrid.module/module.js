(function () {
  document.querySelectorAll('[data-vaf-cg]').forEach(function (root) {
    var cards = [].slice.call(root.querySelectorAll('.vaf-cg__card')), box = root.querySelector('.vaf-cg__filters'), all = (root.querySelector('[data-all-label]') || {}).getAttribute ? root.querySelector('[data-all-label]').getAttribute('data-all-label') : 'All industries';
    var inds = []; cards.forEach(function (c) { var i = c.getAttribute('data-ind'); if (i && inds.indexOf(i) < 0) inds.push(i); });
    if (inds.length < 2) return;
    function make(label, val) { var b = document.createElement('button'); b.type = 'button'; b.textContent = label; b.setAttribute('aria-pressed', val === '' ? 'true' : 'false'); b.onclick = function () { [].forEach.call(box.children, function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); }); cards.forEach(function (c) { c.hidden = !!val && c.getAttribute('data-ind') !== val; }); }; box.appendChild(b); }
    make(all, ''); inds.forEach(function (i) { make(i, i); }); box.hidden = false;
  });
})();
