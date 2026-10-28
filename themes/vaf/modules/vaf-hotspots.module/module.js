(function () {
  function init(root) {
    if (root.getAttribute('data-vaf-ready')) return;
    root.setAttribute('data-vaf-ready', '1');
    var stage = root.querySelector('.vaf-hot__stage'), box = root.querySelector('.vaf-hot__pops');
    var pins = [].slice.call(root.querySelectorAll('.vaf-hot__pin'));
    var pops = [].slice.call(root.querySelectorAll('.vaf-hot__pop'));
    var links = [].slice.call(root.querySelectorAll('.vaf-hot__list a'));
    var wide = window.matchMedia('(min-width:768px)');
    var closeText = root.getAttribute('data-close') || 'Close';
    var cur = -1, uid = (window.__vafHot = (window.__vafHot || 0) + 1);
    root.classList.add('is-js');
    pins.forEach(function (p, i) {
      pops[i].id = 'vaf-hot-' + uid + '-' + i; p.setAttribute('aria-controls', pops[i].id);
      var x = document.createElement('button'); x.type = 'button'; x.className = 'vaf-hot__close'; x.setAttribute('aria-label', closeText);
      x.innerHTML = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>';
      x.addEventListener('click', function () { close(true); });
      pops[i].appendChild(x);
    });
    function place(i) {
      var pop = pops[i], pin = pins[i];
      if (!wide.matches) return;
      var sr = stage.getBoundingClientRect(), pr = pin.getBoundingClientRect();
      var cx = pr.left + pr.width / 2 - sr.left, cy = pr.top + pr.height / 2 - sr.top;
      var w = pop.offsetWidth, h = pop.offsetHeight;
      var below = cy + 28 + h < sr.height - 8 || cy < sr.height / 2;
      var left = Math.max(12, Math.min(sr.width - w - 12, cx - w / 2));
      var top = below ? cy + 28 : cy - 28 - h;
      if (top < 8) top = 8;
      pop.style.left = left + 'px'; pop.style.top = top + 'px';
      pop.style.setProperty('--ax', Math.max(22, Math.min(w - 22, cx - left)) + 'px');
      pop.classList.toggle('is-below', below); pop.classList.toggle('is-above', !below);
    }
    function mount() {
      pops.forEach(function (pop, i) {
        if (wide.matches) { pins[i].insertAdjacentElement('afterend', pop); }
        else { box.appendChild(pop); pop.style.left = pop.style.top = ''; pop.classList.remove('is-below', 'is-above'); }
      });
      if (!wide.matches && cur < 0) open(0, false);
      if (wide.matches && cur >= 0) place(cur);
    }
    function open(i, focus) {
      cur = i;
      pins.forEach(function (p, j) { p.setAttribute('aria-expanded', j === i ? 'true' : 'false'); });
      pops.forEach(function (p, j) { p.classList.toggle('is-on', j === i); });
      links.forEach(function (a, j) { a.classList.toggle('is-hot', j === i); });
      if (wide.matches) place(i);
    }
    function close(refocus) {
      var was = cur; cur = -1;
      pins.forEach(function (p) { p.setAttribute('aria-expanded', 'false'); });
      pops.forEach(function (p) { p.classList.remove('is-on'); });
      links.forEach(function (a) { a.classList.remove('is-hot'); });
      if (refocus && was > -1) pins[was].focus();
    }
    pins.forEach(function (p, i) {
      p.addEventListener('click', function (e) {
        e.stopPropagation();
        if (cur === i && wide.matches) close(false); else open(i);
      });
    });
    links.forEach(function (a, i) {
      a.addEventListener('mouseenter', function () { pins[i].classList.add('is-hot'); });
      a.addEventListener('mouseleave', function () { pins[i].classList.remove('is-hot'); });
    });
    document.addEventListener('click', function (e) { if (cur > -1 && wide.matches && !root.querySelector('.vaf-hot__pop.is-on').contains(e.target)) close(false); });
    root.addEventListener('keydown', function (e) { if (e.key === 'Escape' && cur > -1 && wide.matches) { e.stopPropagation(); close(true); } });
    var onChange = function () { mount(); };
    if (wide.addEventListener) wide.addEventListener('change', onChange); else wide.addListener(onChange);
    window.addEventListener('resize', function () { if (cur > -1) place(cur); });
    mount();
  }
  function boot() { [].forEach.call(document.querySelectorAll('[data-vaf-hot]'), init); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
