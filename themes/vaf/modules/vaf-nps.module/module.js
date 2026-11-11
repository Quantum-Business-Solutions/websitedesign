/* VAF NPS widget: fills the latest survey comments from CEO Juice, live.
   If the feed is unreachable the block simply stays hidden; the page keeps its typed comments. */
(function () {
  'use strict';
  var box = document.querySelector('[data-vn-comments]');
  if (!box || !window.fetch) return;
  var key = box.getAttribute('data-key'), cust = box.getAttribute('data-customer'), n = parseInt(box.getAttribute('data-count'), 10) || 6;
  function name(s) { s = String(s || '').trim(); return s ? s.charAt(0).toUpperCase() + s.slice(1).toLowerCase() : 'A VAF customer'; }
  function when(s) { var d = new Date(s); return isNaN(d) ? '' : d.toLocaleDateString('en-US', { month: 'long', year: 'numeric' }); }
  fetch('https://api.ceojuice.com/api/Processes/SurveyComments?CustomerNumber=' + encodeURIComponent(cust) + '&AuthKey=' + encodeURIComponent(key) + '&qty=' + Math.max(n, 12))
    .then(function (r) { return r.ok ? r.json() : Promise.reject(); })
    .then(function (rows) {
      var seen = {}, list = box.querySelector('.vn__list'), shown = 0;
      (rows || []).forEach(function (r) {
        var t = String(r.comment || '').trim();
        if (!t || seen[t] || shown >= n) return;
        seen[t] = 1; shown++;
        var li = document.createElement('li'); li.className = 'vn__card';
        var p = document.createElement('p'); p.className = 'vn__q'; p.textContent = t;
        var w = document.createElement('div'); w.className = 'vn__who';
        var b = document.createElement('b'); b.textContent = name(r.contact);
        var s = document.createElement('span'); s.textContent = 'After-service survey' + (when(r.responseDate) ? ', ' + when(r.responseDate) : '');
        w.appendChild(b); w.appendChild(s); li.appendChild(p); li.appendChild(w); list.appendChild(li);
      });
      if (shown) box.hidden = false;
    })
    .catch(function () { });
})();
