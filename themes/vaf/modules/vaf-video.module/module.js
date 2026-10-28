/* VAF video facade: poster and play button now, youtube-nocookie iframe only after a click. */
(function () {
  function load(frame) {
    var id = frame.getAttribute('data-id');
    if (!id) return;
    var f = document.createElement('iframe');
    f.src = 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(id) + '?rel=0&modestbranding=1&autoplay=1&playsinline=1';
    f.title = frame.getAttribute('data-title') || 'Video';
    f.allow = 'autoplay; encrypted-media; fullscreen; picture-in-picture';
    f.setAttribute('allowfullscreen', '');
    f.className = 'vf-vid__iframe';
    frame.textContent = '';
    frame.appendChild(f);
    frame.classList.add('is-playing');
    f.focus();
  }
  function warm() {
    if (document.querySelector('link[data-vf-vid-pc]')) return;
    var l = document.createElement('link');
    l.rel = 'preconnect'; l.href = 'https://www.youtube-nocookie.com'; l.setAttribute('data-vf-vid-pc', '1');
    document.head.appendChild(l);
  }
  function init(frame) {
    var b = frame.querySelector('.vf-vid__btn');
    if (!b) return;
    b.addEventListener('click', function () { load(frame); });
    b.addEventListener('pointerenter', warm, { once: true });
    b.addEventListener('focus', warm, { once: true });
  }
  function boot() { document.querySelectorAll('[data-vf-vid]').forEach(init); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
