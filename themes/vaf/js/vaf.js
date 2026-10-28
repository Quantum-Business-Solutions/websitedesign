/* VAF site behaviours: count-up stats, hero parallax, card tilt, bottom bar, header fold, mobile menu, support drawer */
(function(){
var rm=matchMedia('(prefers-reduced-motion: reduce)').matches;
/* count-up on stat numbers */
var stats=[].filter.call(document.querySelectorAll('.pv-stat b,.pv-hero-stats b,.pv-proof b'),function(b){if(b.hasAttribute('data-static'))return false;var t=b.textContent.trim().replace(/,/g,''),n=parseFloat(t);return !isNaN(n)&&n>=100&&!(t.length===4&&n>1800&&n<2100)});
if(!rm&&'IntersectionObserver' in window&&stats.length){
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(!e.isIntersecting)return;io.unobserve(e.target);var el=e.target,txt=el.textContent.trim(),m=txt.match(/^([^0-9]*)([0-9][0-9,]*)(\.[0-9]+)?(.*)$/);if(!m)return;var pre=m[1],intp=m[2].replace(/,/g,''),dec=m[3]||'',suf=m[4],target=parseFloat(intp+dec),places=dec?dec.length-1:0,comma=m[2].indexOf(',')>-1,t0=null;function fmt(v){var f=v.toFixed(places);if(comma){var parts=f.split('.');parts[0]=parts[0].replace(/\B(?=(\d{3})+(?!\d))/g,',');f=parts.join('.')}return pre+f+suf}function step(ts){if(t0===null)t0=ts;var k=Math.min(1,(ts-t0)/1400);k=1-Math.pow(1-k,3);el.textContent=fmt(target*k);if(k<1)requestAnimationFrame(step);else el.textContent=txt}el.textContent=fmt(0);requestAnimationFrame(step)})},{threshold:.4});
  stats.forEach(function(b){io.observe(b)});
}
/* hero image: slow parallax against the scroll */
var hero=document.querySelector('.pv-hero-img img');
if(hero&&!rm&&matchMedia('(min-width:1025px)').matches){
  var raf=0;function move(){raf=0;var r=hero.getBoundingClientRect(),c=(r.top+r.height/2-innerHeight/2)/innerHeight;hero.style.transform='translateY('+(-c*14).toFixed(1)+'px)'}
  hero.style.willChange='transform';addEventListener('scroll',function(){if(!raf)raf=requestAnimationFrame(move)},{passive:true});move();
}
/* cards: light 3D tilt toward the pointer */
if(!rm&&matchMedia('(pointer:fine) and (min-width:1025px)').matches){
  document.querySelectorAll('.pv-tilt').forEach(function(c){
    c.style.transformStyle='preserve-3d';c.style.transition='transform .25s ease, box-shadow .25s ease';
    c.addEventListener('pointermove',function(e){var r=c.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;c.style.transform='perspective(900px) rotateX('+(-y*6).toFixed(2)+'deg) rotateY('+(x*6).toFixed(2)+'deg) translateY(-3px)'});
    c.addEventListener('pointerleave',function(){c.style.transform=''});
  });
}
/* bottom bar: stay out of the way while the hero's own buttons are on screen */
var stk=document.querySelector('.pv-sticky'),hb=document.querySelector('main .pv-btns');
if(stk&&hb&&'IntersectionObserver' in window){new IntersectionObserver(function(es){es.forEach(function(e){stk.classList.toggle('pv-sticky-off',e.isIntersecting)})},{threshold:.2}).observe(hb)}
/* header: fold the utility bar away after the first scroll */
var hd=document.querySelector('.q-header');if(hd){var sc=function(){hd.classList.toggle('is-scrolled',scrollY>80)};addEventListener('scroll',sc,{passive:true});sc()}
/* mobile menu open: hide the bottom bars so the panel is not covered */
var mn=document.querySelector('.q-mnav');if(mn){mn.addEventListener('toggle',function(){document.documentElement.classList.toggle('menu-open',mn.open)})}
})();
(function(){var l=document.querySelector('.pv-sl');if(!l)return;var b=l.querySelector('button'),d=l.querySelector('.drawer');var sc=function(){l.classList.toggle('on',scrollY>560)};addEventListener('scroll',sc,{passive:true});sc();b.addEventListener('click',function(){var o=!d.hidden;d.hidden=o;b.setAttribute('aria-expanded',o?'false':'true')});document.addEventListener('keydown',function(e){if(e.key==='Escape'){d.hidden=true;b.setAttribute('aria-expanded','false')}})})();

/* scroll reveal: sections ease in once, never hide content without JS or with reduced motion */
(function(){
  if(!('IntersectionObserver' in window)||matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  document.documentElement.classList.add('vaf-js');
  var els=[].slice.call(document.querySelectorAll('main .q-section:not(.pv-lh) .q-container > *'));
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px',threshold:.06});
  els.forEach(function(el,i){el.classList.add('vaf-rv');el.classList.add('d'+(i%3+1));io.observe(el)});
  setTimeout(function(){els.forEach(function(el){el.classList.add('in')})},6000);
})();
