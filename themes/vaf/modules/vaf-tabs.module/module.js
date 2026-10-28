(function () {
  var uid = 0;
  function init(root) {
    if (root.getAttribute('data-vaf-ready')) return;
    root.setAttribute('data-vaf-ready', '1');
    var list = root.querySelector('.vaf-tabs__list');
    var tabs = [].slice.call(root.querySelectorAll('.vaf-tabs__tab'));
    var panels = [].slice.call(root.querySelectorAll('.vaf-tabs__panel'));
    var vert = window.matchMedia('(min-width:1024px)');
    var id = 'vaf-tabs-' + (++uid);
    root.classList.add('is-js');
    function orient() { list.setAttribute('aria-orientation', vert.matches ? 'vertical' : 'horizontal'); }
    orient();
    if (vert.addEventListener) vert.addEventListener('change', orient); else vert.addListener(orient);
    function select(i, focus) {
      tabs.forEach(function (t, j) {
        var on = j === i;
        t.setAttribute('aria-selected', on ? 'true' : 'false'); t.tabIndex = on ? 0 : -1;
        panels[j].classList.toggle('is-on', on);
      });
      if (focus) tabs[i].focus();
      if (!vert.matches) {
        var t = tabs[i], l = list;
        l.scrollTo ? l.scrollTo({ left: t.offsetLeft - (l.clientWidth - t.offsetWidth) / 2, behavior: 'smooth' }) : (l.scrollLeft = t.offsetLeft - (l.clientWidth - t.offsetWidth) / 2);
      }
    }
    tabs.forEach(function (t, i) {
      t.id = id + '-t' + i; panels[i].id = id + '-p' + i;
      t.setAttribute('aria-controls', panels[i].id); panels[i].setAttribute('aria-labelledby', t.id);
      t.addEventListener('click', function () { select(i); });
      t.addEventListener('keydown', function (e) {
        var k = e.key, to = -1, n = tabs.length;
        if (k === 'ArrowRight' || k === 'ArrowDown') to = (i + 1) % n;
        else if (k === 'ArrowLeft' || k === 'ArrowUp') to = (i - 1 + n) % n;
        else if (k === 'Home') to = 0; else if (k === 'End') to = n - 1;
        if (to < 0) return; e.preventDefault(); select(to, true);
      });
    });
    select(0);
  }
  function boot() { [].forEach.call(document.querySelectorAll('[data-vaf-tabs]'), init); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
