/* Quantum 2026 theme runtime — progressive enhancement, reduced-motion aware */
(function(){
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion:reduce)').matches;

  // ---- count-up on scroll: <span data-count="25" data-suffix="%" data-prefix="$"> ----
  function fmt(el, v){ return (el.dataset.prefix||'') + v + (el.dataset.suffix||''); }
  function countUp(el){
    var target = parseFloat(el.dataset.count); if(isNaN(target)) return;
    if(reduce){ el.textContent = fmt(el, target % 1 ? target : Math.round(target)); return; }
    var dur = 1200, start = performance.now(), dec = (target % 1 !== 0);
    function tick(now){
      var t = Math.min(1,(now-start)/dur), e = 1-Math.pow(1-t,3), v = target*e;
      el.textContent = fmt(el, dec ? v.toFixed(1) : Math.round(v));
      if(t<1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }
  var counters = document.querySelectorAll('[data-count]');
  if(counters.length){
    if('IntersectionObserver' in window){
      var io = new IntersectionObserver(function(es){
        es.forEach(function(x){ if(x.isIntersecting){ countUp(x.target); io.unobserve(x.target); } });
      }, {threshold:0.4});
      counters.forEach(function(c){ io.observe(c); });
    } else counters.forEach(countUp);
  }

  // ---- reveal on scroll: .q-reveal-on ----
  var reveals = document.querySelectorAll('.q-reveal-on');
  if(reveals.length && !reduce && 'IntersectionObserver' in window){
    var ro = new IntersectionObserver(function(es){
      es.forEach(function(x){ if(x.isIntersecting){ x.target.classList.add('q-reveal'); ro.unobserve(x.target); } });
    }, {threshold:0.15});
    reveals.forEach(function(r){ ro.observe(r); });
  } else reveals.forEach(function(r){ r.classList.add('q-reveal'); });

  // ---- testimonial slider: [data-q-slider] with .q-slide children ----
  document.querySelectorAll('[data-q-slider]').forEach(function(root){
    var slides = [].slice.call(root.querySelectorAll('.q-slide')); if(slides.length<2) return;
    var i=0, dotsWrap = root.querySelector('[data-q-dots]'), timer;
    slides.forEach(function(s,n){ s.style.display = n?'none':''; });
    var dots = slides.map(function(_,n){
      var d=document.createElement('button'); d.setAttribute('aria-label','Slide '+(n+1));
      d.className='q-dot'+(n?'':' is-active'); d.onclick=function(){ go(n); reset(); };
      if(dotsWrap) dotsWrap.appendChild(d); return d;
    });
    function go(n){ slides[i].style.display='none'; dots[i].classList.remove('is-active'); i=n; slides[i].style.display=''; dots[i].classList.add('is-active'); }
    function next(){ go((i+1)%slides.length); }
    function reset(){ if(reduce||!timer) return; clearInterval(timer); timer=setInterval(next,6000); }
    var prev=root.querySelector('[data-q-prev]'), nxt=root.querySelector('[data-q-next]');
    if(prev) prev.onclick=function(){ go((i-1+slides.length)%slides.length); reset(); };
    if(nxt) nxt.onclick=function(){ next(); reset(); };
    if(!reduce){ timer=setInterval(next,6000); root.onmouseenter=function(){ clearInterval(timer); }; root.onmouseleave=reset; }
  });

  // ---- tabs a11y: [data-q-tabs] with [role=tab] + [role=tabpanel] ----
  document.querySelectorAll('[data-q-tabs]').forEach(function(root){
    var tabs=[].slice.call(root.querySelectorAll('[role=tab]')), panels=[].slice.call(root.querySelectorAll('[role=tabpanel]'));
    function sel(n){ tabs.forEach(function(t,k){ var on=k===n; t.setAttribute('aria-selected',on); t.tabIndex=on?0:-1; if(panels[k]) panels[k].hidden=!on; }); }
    tabs.forEach(function(t,n){ t.onclick=function(){ sel(n); t.focus(); };
      t.onkeydown=function(e){ if(e.key==='ArrowRight'){ e.preventDefault(); sel((n+1)%tabs.length); tabs[(n+1)%tabs.length].focus(); }
        else if(e.key==='ArrowLeft'){ e.preventDefault(); var p=(n-1+tabs.length)%tabs.length; sel(p); tabs[p].focus(); } };
    });
    sel(0);
  });

  // ---- scroll-spy for TOC anchors: nav[data-q-spy] a[href^="#"] ----
  document.querySelectorAll('nav[data-q-spy]').forEach(function(nav){
    var links=[].slice.call(nav.querySelectorAll('a[href^="#"]'));
    var targets=links.map(function(l){ return document.getElementById(l.getAttribute('href').slice(1)); });
    if(!('IntersectionObserver' in window)) return;
    var spy=new IntersectionObserver(function(es){
      es.forEach(function(x){ if(x.isIntersecting){ var k=targets.indexOf(x.target); links.forEach(function(l,n){ l.classList.toggle('is-active',n===k); }); } });
    },{rootMargin:'-40% 0px -55% 0px'});
    targets.forEach(function(t){ if(t) spy.observe(t); });
  });
})();

/* ===== POP LAYER v1 — scroll reveal + gradient/count-up stats (propagates to all Void pages) ===== */
(function(){
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion:reduce)').matches;
  // scroll-reveal every content section (skip the hero)
  var secs = [].slice.call(document.querySelectorAll('main .q-section, main .dnd-section'));
  if(secs.length && !reduce && 'IntersectionObserver' in window){
    var io = new IntersectionObserver(function(es){ es.forEach(function(x){ if(x.isIntersecting){ x.target.classList.add('q-in'); io.unobserve(x.target); } }); }, {threshold:0.12});
    secs.forEach(function(s,i){ if(i===0) return; s.classList.add('q-anim'); io.observe(s); });
  }
  // mark numeric stat cards -> gradient numerals + count-up
  function countUp(el, raw){
    var m = raw.match(/^([^\d]*)([\d.,]+)(.*)$/); if(!m){ el.textContent = raw; return; }
    var pre=m[1], numStr=m[2].replace(/,/g,''), suf=m[3], target=parseFloat(numStr), dec=(numStr.indexOf('.')>=0);
    if(reduce || isNaN(target)){ el.textContent = raw; return; }
    var dur=1300, start=null;
    function tick(ts){ if(!start)start=ts; var t=Math.min(1,(ts-start)/dur), e=1-Math.pow(1-t,3), v=target*e;
      var shown = dec ? v.toFixed(1) : Math.round(v);
      if(target>=1000) shown = Math.round(v).toLocaleString();
      el.textContent = pre + shown + suf; if(t<1) requestAnimationFrame(tick); }
    requestAnimationFrame(tick);
  }
  document.querySelectorAll('.q-prose .q-cards').forEach(function(grid){
    var cards=[].slice.call(grid.querySelectorAll('.q-card')), stat=0;
    cards.forEach(function(c){ var h=c.querySelector('h4'); if(h && /^\s*[$]?[\d.,]+\s*[%xX+MK]*\s*$/.test(h.textContent)){ c.classList.add('is-stat'); c.setAttribute('data-raw', h.textContent.trim()); stat++; } });
    if(stat>=2 && stat>=cards.length-1) grid.classList.add('is-stats');
  });
  var statEls=[].slice.call(document.querySelectorAll('.q-card.is-stat h4'));
  if(statEls.length){
    if(!reduce && 'IntersectionObserver' in window){
      var so=new IntersectionObserver(function(es){ es.forEach(function(x){ if(x.isIntersecting){ countUp(x.target, x.target.closest('.q-card').getAttribute('data-raw')); so.unobserve(x.target); } }); },{threshold:0.4});
      statEls.forEach(function(e){ so.observe(e); });
    }
  }
})();
