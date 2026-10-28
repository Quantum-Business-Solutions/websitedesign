/* VAF contact: submit label, and a topic selector that feeds the HubSpot form field when the form has one. */
(function () {
  function setVal(el, val) {
    var proto = el.tagName === 'SELECT' ? HTMLSelectElement.prototype : el.tagName === 'TEXTAREA' ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
    var d = Object.getOwnPropertyDescriptor(proto, 'value');
    if (d && d.set) d.set.call(el, val); else el.value = val;
    el.dispatchEvent(new Event('input', { bubbles: true }));
    el.dispatchEvent(new Event('change', { bubbles: true }));
  }
  function relabel(root) {
    var label = root.getAttribute('data-submit');
    if (!label) return;
    root.querySelectorAll('.vf-form .hs-button, .vf-form .hsfc-Button, .vf-form input[type=submit], .vf-form button[type=submit]').forEach(function (b) {
      if (b.getAttribute('data-vf-label') === label) return;
      if (b.tagName === 'INPUT') b.value = label; else b.textContent = label;
      b.setAttribute('data-vf-label', label);
    });
  }
  function watch(root, fn) {
    fn();
    if (!window.MutationObserver) return;
    var raf = 0, mo = new MutationObserver(function () { if (!raf) raf = requestAnimationFrame(function () { raf = 0; fn(); }); });
    mo.observe(root, { childList: true, subtree: true });
    setTimeout(function () { mo.disconnect(); }, 60000);
  }

  function findTarget(form) {
    var re = /topic|interest|service|look|subject|solution/i, cand = form.querySelectorAll('select, input[type=text], input:not([type])'), i, el;
    for (i = 0; i < cand.length; i++) { el = cand[i]; if (re.test(el.name || '') || re.test(el.id || '')) return { kind: el.tagName === 'SELECT' ? 'select' : 'text', el: el }; }
    el = form.querySelector('textarea');
    return el ? { kind: 'area', el: el } : null;
  }
  function apply(t, val, state) {
    if (t.kind === 'select') {
      var want = val.toLowerCase(), hit = null;
      [].forEach.call(t.el.options, function (o) { var s = (o.text + '|' + o.value).toLowerCase(); if (!hit && (o.text.toLowerCase() === want || o.value.toLowerCase() === want)) hit = o; });
      if (!hit) [].forEach.call(t.el.options, function (o) { var tx = o.text.toLowerCase(); if (!hit && tx && (want.indexOf(tx) > -1 || tx.indexOf(want) > -1)) hit = o; });
      if (hit) setVal(t.el, hit.value);
    } else if (t.kind === 'text') {
      setVal(t.el, val);
    } else {
      var cur = t.el.value || '';
      if (state.prefix && cur.indexOf(state.prefix) === 0) cur = cur.slice(state.prefix.length);
      state.prefix = 'Topic: ' + val + '\n';
      setVal(t.el, state.prefix + cur);
    }
  }
  function init(root) {
    var wrap = root.querySelector('[data-topic]'), sel = root.querySelector('[data-topic-select]'), state = {}, target = null;
    watch(root, function () {
      relabel(root);
      if (!wrap || target) return;
      var form = root.querySelector('.vf-form form, .vf-form .hsfc-Form');
      if (!form) return;
      target = findTarget(form);
      if (target) { wrap.hidden = false; apply(target, sel.value, state); }
    });
    if (sel) sel.addEventListener('change', function () { if (target && document.body.contains(target.el)) apply(target, sel.value, state); });
  }
  function boot() { document.querySelectorAll('[data-vf-ct]').forEach(init); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
