(function () {
  var NS = 'http://www.w3.org/2000/svg', uid = 0;
  function el(n, a, p) { var e = document.createElementNS(NS, n); for (var k in a) e.setAttribute(k, a[k]); if (p) p.appendChild(e); return e; }
  function pt(r, a) { return (300 + r * Math.cos(a)).toFixed(1) + ',' + (300 + r * Math.sin(a)).toFixed(1); }
  function init(root) {
    if (root.getAttribute('data-vaf-ready')) return;
    root.setAttribute('data-vaf-ready', '1');
    var cards = [].slice.call(root.querySelectorAll('.vaf-wheel__card'));
    var tabs = [].slice.call(root.querySelectorAll('.vaf-wheel__tab'));
    var fig = root.querySelector('.vaf-wheel__fig');
    var n = cards.length, cur = 0, id = 'vaf-wheel-' + (++uid);
    if (!n) return;
    var svg = el('svg', { 'class': 'vaf-wheel__svg', viewBox: '0 0 600 600', focusable: 'false' });
    var rOut = 236, rIn = 122, gap = 0.016, segs = [];
    el('circle', { 'class': 'ring-line', cx: 300, cy: 300, r: 272 }, svg);
    for (var i = 0; i < n; i++) {
      var a0 = -Math.PI / 2 + i * 2 * Math.PI / n + gap, a1 = -Math.PI / 2 + (i + 1) * 2 * Math.PI / n - gap, am = (a0 + a1) / 2;
      var large = (a1 - a0) > Math.PI ? 1 : 0;
      var g = el('g', { 'class': 'seg', 'data-i': i }, svg);
      g.style.setProperty('--dx', (Math.cos(am) * 11).toFixed(1) + 'px');
      g.style.setProperty('--dy', (Math.sin(am) * 11).toFixed(1) + 'px');
      g.style.setProperty('--i', i);
      el('path', { d: 'M' + pt(rOut, a0) + ' A' + rOut + ',' + rOut + ' 0 ' + large + ' 1 ' + pt(rOut, a1) + ' L' + pt(rIn, a1) + ' A' + rIn + ',' + rIn + ' 0 ' + large + ' 0 ' + pt(rIn, a0) + ' Z' }, g);
      var rm = (rOut + rIn) / 2, lx = 300 + rm * Math.cos(am), ly = 300 + rm * Math.sin(am);
      var nt = el('text', { 'class': 'num', x: lx.toFixed(1), y: (ly - 12).toFixed(1) }, g); nt.textContent = '0' + (i + 1);
      var lt = el('text', { 'class': 'lab', x: lx.toFixed(1), y: (ly + 10).toFixed(1) }, g); lt.textContent = cards[i].getAttribute('data-short') || '';
      segs.push(g);
    }
    var hg = el('g', { 'class': 'hubg' }, svg);
    el('circle', { 'class': 'hub', cx: 300, cy: 300, r: 108 }, hg);
    el('circle', { 'class': 'hub-ring', cx: 300, cy: 300, r: 96 }, hg);
    var ht = el('text', { 'class': 'hubt', x: 300, y: 304 }, hg); ht.textContent = root.getAttribute('data-hub') || '';
    var hs = el('text', { 'class': 'hubs', x: 300, y: 332 }, hg); hs.textContent = root.getAttribute('data-hub-sub') || '';
    var ringTxt = root.getAttribute('data-ring');
    if (ringTxt) {
      var rr = 288, defs = el('defs', {}, svg);
      el('path', { id: id + '-r', d: 'M300,300 m-' + rr + ',0 a' + rr + ',' + rr + ' 0 1,1 ' + (2 * rr) + ',0 a' + rr + ',' + rr + ' 0 1,1 -' + (2 * rr) + ',0' }, defs);
      var rt = el('text', { 'class': 'ring-text' }, svg);
      var tp = el('textPath', { href: '#' + id + '-r', startOffset: '25%', 'text-anchor': 'middle' }, rt); tp.textContent = ringTxt;
    }
    fig.appendChild(svg);
    function set(i, focus) {
      cur = i;
      cards.forEach(function (c, j) { c.classList.toggle('is-on', j === i); });
      segs.forEach(function (s, j) { s.classList.toggle('on', j === i); });
      tabs.forEach(function (t, j) { t.setAttribute('aria-selected', j === i ? 'true' : 'false'); t.tabIndex = j === i ? 0 : -1; });
      if (focus && tabs[i]) tabs[i].focus();
    }
    root.classList.add('is-js');
    tabs.forEach(function (t, i) {
      t.id = id + '-t' + i; cards[i].id = id + '-p' + i;
      t.setAttribute('aria-controls', cards[i].id); cards[i].setAttribute('role', 'tabpanel'); cards[i].setAttribute('aria-labelledby', t.id);
      t.addEventListener('click', function () { set(i); });
      t.addEventListener('keydown', function (e) {
        var to = -1;
        if (e.key === 'ArrowRight' || e.key === 'ArrowDown') to = (i + 1) % n;
        else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') to = (i - 1 + n) % n;
        else if (e.key === 'Home') to = 0; else if (e.key === 'End') to = n - 1;
        if (to < 0) return; e.preventDefault(); set(to, true);
      });
    });
    segs.forEach(function (g, i) {
      g.addEventListener('mouseenter', function () { set(i); });
      g.addEventListener('click', function () { set(i); });
    });
    set(0);
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { root.classList.add('is-in'); io.disconnect(); } }); }, { threshold: 0.3 });
      io.observe(fig);
    } else root.classList.add('is-in');
  }
  function boot() { [].forEach.call(document.querySelectorAll('[data-vaf-wheel]'), init); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
