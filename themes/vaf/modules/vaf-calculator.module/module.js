/* VAF print cost estimator. Rates come from data attributes on the module root (editable fields). */
(function () {
  function init(root) {
    if (root.getAttribute('data-ready')) return;
    root.setAttribute('data-ready', '1');
    var R = {
      mono: +root.getAttribute('data-mono') || 0, color: +root.getAttribute('data-color') || 0,
      minutes: +root.getAttribute('data-minutes') || 0, hourly: +root.getAttribute('data-hourly') || 0,
      saving: (+root.getAttribute('data-saving') || 0) / 100, orders: +root.getAttribute('data-orders') || 0
    };
    var inputs = {};
    ['d', 'm', 'c'].forEach(function (k) {
      inputs[k] = { rng: root.querySelector('.vf-calc__rng[data-k=' + k + ']'), num: root.querySelector('.vf-calc__num[data-k=' + k + ']') };
    });
    function out(n) { return root.querySelector('[data-out=' + n + ']'); }
    var live = root.querySelector('[data-live]'), timer = 0;
    var fmt = function (n) { return Math.round(n).toLocaleString('en-US'); };
    var usd = function (n) { return '$' + fmt(n); };
    function val(k) { var v = +inputs[k].rng.value; return isFinite(v) ? v : 0; }
    function fill(r) { var mx = +r.max || 1, mn = +r.min || 0; r.style.setProperty('--p', (((+r.value - mn) / (mx - mn)) * 100).toFixed(1) + '%'); }
    function calc() {
      var d = val('d'), m = val('m'), c = val('c');
      var perMonth = m * R.mono + c * R.color;
      var hours = d * R.minutes / 60 * 52;
      var labor = hours * R.hourly, pages = perMonth * 12, year = pages + labor;
      out('total').textContent = usd(year);
      out('pagesyr').textContent = usd(pages);
      out('laboryr').textContent = usd(labor);
      out('cpp').textContent = '$' + ((m + c) ? perMonth / (m + c) : 0).toFixed(3);
      out('hours').textContent = fmt(hours);
      out('save').textContent = usd(year * R.saving) + ' / yr';
      out('orders').textContent = fmt(d * R.orders);
      var share = year ? (pages / year) * 100 : 50;
      root.querySelector('[data-bar=pages]').style.width = share.toFixed(1) + '%';
      root.querySelector('[data-bar=labor]').style.width = (100 - share).toFixed(1) + '%';
      ['d', 'm', 'c'].forEach(function (k) { fill(inputs[k].rng); });
      return year;
    }
    function announce(year) {
      clearTimeout(timer);
      timer = setTimeout(function () { live.textContent = 'Estimated print spend ' + usd(year) + ' a year.'; }, 600);
    }
    ['d', 'm', 'c'].forEach(function (k) {
      var i = inputs[k];
      i.rng.addEventListener('input', function () { i.num.value = i.rng.value; announce(calc()); });
      i.num.addEventListener('input', function () {
        var v = parseFloat(i.num.value);
        if (!isFinite(v)) return;
        var mx = +i.rng.max, mn = +i.rng.min;
        i.rng.value = Math.max(mn, Math.min(mx, v));
        announce(calc());
      });
      i.num.addEventListener('change', function () { i.num.value = i.rng.value; });
    });
    root.classList.add('is-js');
    calc();
  }
  function boot() { document.querySelectorAll('[data-vf-calc]').forEach(init); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
