/* vaf-partners: pause and play for the scrolling logos (WCAG 2.2.2). Hover and focus also pause via CSS. */
(function () {
  'use strict';
  function init() {
    [].forEach.call(document.querySelectorAll('.vaf-partners__stage'), function (st) {
      var b = st.querySelector('.vaf-partners__pause');
      if (!b || b.getAttribute('data-vaf-ready')) return;
      b.setAttribute('data-vaf-ready', '1');
      b.hidden = false;
      function label() { b.textContent = b.getAttribute(st.classList.contains('is-paused') ? 'data-play-label' : 'data-pause-label') || ''; }
      b.addEventListener('click', function () { st.classList.toggle('is-paused'); label(); });
      label();
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
