/* VAF lead form: applies the editable submit label to the HubSpot form once it renders. */
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

  function boot() { document.querySelectorAll('[data-vf-lf]').forEach(function (r) { watch(r, function () { relabel(r); }); }); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
