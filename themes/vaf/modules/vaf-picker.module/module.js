(function () {
  document.querySelectorAll('[data-vaf-pk]').forEach(function (root) {
    var chips = [].slice.call(root.querySelectorAll('.vaf-pk__chip')), cards = [].slice.call(root.querySelectorAll('.vaf-pk__card'));
    if (!chips.length) return;
    root.classList.add('is-js');
    function pick(i) {
      chips.forEach(function (c, k) { c.setAttribute('aria-pressed', k === i ? 'true' : 'false'); });
      cards.forEach(function (c, k) { c.classList.toggle('is-on', k === i); });
      try { sessionStorage.setItem('vafPick', String(i)); } catch (e) { }
    }
    chips.forEach(function (c, i) { c.addEventListener('click', function () { pick(i); }); });
    pick(0);
  });
})();
