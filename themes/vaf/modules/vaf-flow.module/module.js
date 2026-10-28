(function () {
  var uid = 0;
  function init(root) {
    if (root.getAttribute('data-vaf-ready')) return;
    root.setAttribute('data-vaf-ready', '1');
    var chart = root.querySelector('.vaf-flow__chart');
    var steps = [].slice.call(root.querySelectorAll('.vaf-flow__step'));
    var n = steps.length, cur = 0, id = 'vaf-flow-' + (++uid);
    if (!n) return;
    steps.forEach(function (li, i) {
      var b = li.querySelector('.vaf-flow__btn'), d = li.querySelector('.vaf-flow__detail');
      b.id = id + '-b' + i; d.id = id + '-d' + i; b.setAttribute('aria-controls', d.id);
    });
    function set(i, focusDir) {
      cur = Math.max(0, Math.min(n - 1, i));
      steps.forEach(function (li, j) {
        li.classList.toggle('is-active', j === cur);
        li.classList.toggle('is-done', j < cur);
        li.querySelector('.vaf-flow__btn').setAttribute('aria-expanded', j === cur ? 'true' : 'false');
        li.querySelector('.vaf-flow__detail').hidden = j !== cur;
      });
      chart.style.setProperty('--act', cur + 1);
      if (focusDir) {
        var go = steps[cur].querySelector('.vaf-flow__go[data-dir="' + focusDir + '"]');
        if (!go || go.disabled) go = steps[cur].querySelector('.vaf-flow__btn');
        go.focus();
      }
    }
    root.classList.add('is-js');
    set(0);
    steps.forEach(function (li, i) {
      var b = li.querySelector('.vaf-flow__btn');
      b.addEventListener('click', function () { set(i); });
      b.addEventListener('keydown', function (e) {
        var k = e.key, to = -1;
        if (k === 'ArrowRight' || k === 'ArrowDown') to = i + 1;
        else if (k === 'ArrowLeft' || k === 'ArrowUp') to = i - 1;
        else if (k === 'Home') to = 0;
        else if (k === 'End') to = n - 1;
        if (to < 0 || to > n - 1) return;
        e.preventDefault(); set(to); steps[to].querySelector('.vaf-flow__btn').focus();
      });
      [].forEach.call(li.querySelectorAll('.vaf-flow__go'), function (g) {
        g.addEventListener('click', function () { var d = +g.getAttribute('data-dir'); set(cur + d, String(d)); });
      });
    });
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) { root.classList.add('is-in'); io.disconnect(); } });
      }, { threshold: 0.25 });
      io.observe(chart);
    } else { root.classList.add('is-in'); }
  }
  function boot() { [].forEach.call(document.querySelectorAll('[data-vaf-flow]'), init); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
