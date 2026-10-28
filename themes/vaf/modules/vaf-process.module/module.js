(function () {
  function init(root) {
    if (root.getAttribute('data-vaf-ready')) return;
    root.setAttribute('data-vaf-ready', '1');
    var chart = root.querySelector('.vaf-proc__chart');
    var steps = [].slice.call(root.querySelectorAll('.vaf-proc__step'));
    function on(i) {
      steps.forEach(function (li, j) {
        li.classList.toggle('is-on', j === i);
        li.classList.toggle('is-reached', j < i);
      });
      chart.style.setProperty('--act', Math.max(0, Math.min(i, steps.length - 1)));
    }
    steps.forEach(function (li, i) {
      li.addEventListener('mouseenter', function () { on(i); });
      li.addEventListener('focus', function () { on(i); });
      li.addEventListener('click', function () { on(i); });
      li.addEventListener('keydown', function (e) {
        var to = -1;
        if (e.key === 'ArrowRight' || e.key === 'ArrowDown') to = i + 1;
        else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') to = i - 1;
        if (to < 0 || to >= steps.length) return;
        e.preventDefault(); steps[to].focus();
      });
    });
    root.classList.add('is-js');
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          if (e.isIntersecting) {
            root.classList.add('is-in'); io.disconnect();
            var i = 0, t = setInterval(function () { on(i++); if (i > steps.length) { clearInterval(t); } }, 520);
          }
        });
      }, { threshold: 0.25 });
      io.observe(chart);
    } else { root.classList.add('is-in'); on(steps.length); }
  }
  function boot() { [].forEach.call(document.querySelectorAll('[data-vaf-proc]'), init); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
