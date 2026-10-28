(function(){var h=document.getElementById("hero");if(!h)return;var rm=matchMedia('(prefers-reduced-motion: reduce)').matches,fine=matchMedia('(pointer:fine) and (min-width:1025px)').matches;
if(!rm&&fine){var g=h.querySelector('.glow');h.addEventListener('pointermove',function(e){var r=h.getBoundingClientRect();h.style.setProperty('--mx',((e.clientX-r.left)/r.width*100).toFixed(1)+'%');h.style.setProperty('--my',((e.clientY-r.top)/r.height*100).toFixed(1)+'%');
h.querySelectorAll('.pv-depth').forEach(function(c){var d=+c.getAttribute('data-depth')||1,x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;c.style.transform='translate3d('+(-x*10*d).toFixed(1)+'px,'+(-y*10*d).toFixed(1)+'px,0) rotateX('+(y*-4).toFixed(2)+'deg) rotateY('+(x*5).toFixed(2)+'deg)'})});
h.addEventListener('pointerleave',function(){h.querySelectorAll('.pv-depth').forEach(function(c){c.style.transform=''})})}
var cv=h.querySelector('canvas.net');if(cv&&!rm&&cv.getContext){var cx=cv.getContext('2d'),W,H,P=[],run=false,raf=0,col=getComputedStyle(h).getPropertyValue('--q-gold').trim()||'#65bc7b';
function size(){var r=h.getBoundingClientRect();W=cv.width=Math.floor(r.width);H=cv.height=Math.floor(r.height);var n=W<768?22:W<1200?40:56;P=[];for(var i=0;i<n;i++)P.push({x:Math.random()*W,y:Math.random()*H,vx:(Math.random()-.5)*.22,vy:(Math.random()-.5)*.22,r:1.2+Math.random()*1.8})}
function tick(){if(!run)return;cx.clearRect(0,0,W,H);var i,j,a,b,d;for(i=0;i<P.length;i++){a=P[i];a.x+=a.vx;a.y+=a.vy;if(a.x<0||a.x>W)a.vx*=-1;if(a.y<0||a.y>H)a.vy*=-1}
cx.lineWidth=1;for(i=0;i<P.length;i++){a=P[i];for(j=i+1;j<P.length;j++){b=P[j];d=Math.hypot(a.x-b.x,a.y-b.y);if(d<150){cx.globalAlpha=(1-d/150)*.28;cx.strokeStyle=col;cx.beginPath();cx.moveTo(a.x,a.y);cx.lineTo(b.x,b.y);cx.stroke()}}}
for(i=0;i<P.length;i++){a=P[i];cx.globalAlpha=.75;cx.fillStyle=col;cx.beginPath();cx.arc(a.x,a.y,a.r,0,6.283);cx.fill()}cx.globalAlpha=1;raf=requestAnimationFrame(tick)}
size();addEventListener('resize',size,{passive:true});
if('IntersectionObserver' in window){new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting&&!run){run=true;tick()}else if(!e.isIntersecting){run=false;cancelAnimationFrame(raf)}})}).observe(h)}else{run=true;tick()}}})();

/* ---- next script ---- */

(function(){var r=document.getElementById("is-this-you");if(!r)return;var o=r.querySelector("[data-out]"),bs=r.querySelectorAll("input");var msgs=["Check what you cannot answer yes to.", "One is normal.", "Two is a pattern.", "Three or more is the reason the assessment exists. Ten to fifteen minutes gives you the full score."];var cta=r.querySelector("[data-cta]");function u(){var n=0;bs.forEach(function(b){if(b.checked)n++});o.innerHTML=(n?"<b>"+n+" of "+bs.length+"</b> ":"")+(msgs[Math.min(n,msgs.length-1)]);if(cta){if(n>=3){cta.className="q-btn";cta.textContent="Request an assessment"}else{cta.className="q-btn-ghost";cta.innerHTML=cta.getAttribute("data-label")+'<span style="width:22px;height:1px;background:currentColor;display:inline-block"></span>'}}}bs.forEach(function(b){b.addEventListener("change",u)});u()})();

/* ---- next script ---- */

(function(){var w=document.getElementById("ba");if(!w)return;var r=w.querySelector('input');r.addEventListener('input',function(){w.style.setProperty('--pos',r.value+'%')})})();

/* ---- next script ---- */

(function(){var f=document.getElementById("flow");if(!f)return;var D=[["Know your Technology Strength Score", "Four assessments in two parts each: information, print, process and communication. Ten to fifteen minutes online, then a specialist walks the office and confirms the answers against what is actually running.", ["A Technology Summary Scorecard", "Every device, system and vendor inventoried", "The gaps, in plain English"]], ["A roadmap that grows with you", "What to eliminate because you do not need it, what to optimize because you already own it, and what to leverage to grow. Priced, sequenced, and tied to your business goals.", ["Eliminate, optimize and leverage lists", "Options priced side by side", "A sequence with dates"]], ["We implement", "Right-sized equipment, software, security and supplies, installed by VAF's own local people. Users trained before the technician leaves. Numbers ported. Monitoring switched on.", ["Install and training completed on site", "Monitoring live on every device", "One point of contact for every line"]], ["We monitor 24/7", "Proactive monitoring, predictive maintenance and fast local repair keep you running. The Customer Care Center processes requests Monday through Friday, 7:00am to 5:00pm, and responds within 24 hours.", ["Alerts handled before they become tickets", "Supplies before they run out", "A 25-point inspection on every service call"]]],t=f.querySelector('[data-t]'),b=f.querySelector('[data-b]'),r=f.querySelector('[data-r]'),bs=f.querySelectorAll('.node button');
bs.forEach(function(x){x.addEventListener('click',function(){var i=+x.getAttribute('data-i');bs.forEach(function(y,j){y.setAttribute('aria-expanded',j===i?'true':'false')});t.textContent=D[i][0];b.textContent=D[i][1];r.innerHTML=D[i][2].map(function(z){var li=document.createElement('li');li.textContent=z;return li.outerHTML}).join('')})});
if('IntersectionObserver' in window){new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){f.classList.add('in')}})},{threshold:.3}).observe(f)}else{f.classList.add('in')}})();

/* ---- next script ---- */

(function(){var h=document.getElementById("office");if(!h)return;var bs=h.querySelectorAll('.spot');function closeAll(){bs.forEach(function(b){b.setAttribute('aria-expanded','false');document.getElementById(b.getAttribute('aria-controls')).hidden=true})}
bs.forEach(function(b){b.addEventListener('click',function(e){e.stopPropagation();var open=b.getAttribute('aria-expanded')==='true';closeAll();if(!open){b.setAttribute('aria-expanded','true');var p=document.getElementById(b.getAttribute('aria-controls'));p.hidden=false;var r=h.getBoundingClientRect(),pr=p.getBoundingClientRect();if(pr.right>r.right-8)p.style.transform='translate(-100%,12px)';if(pr.left<r.left+8)p.style.transform='translate(0,12px)'}})});
document.addEventListener('click',closeAll);document.addEventListener('keydown',function(e){if(e.key==='Escape')closeAll()})})();

/* ---- next script ---- */

(function(){var r=document.getElementById("markets");if(!r)return;var tabs=r.querySelectorAll("[role=tab]"),panels=r.querySelectorAll("[role=tabpanel]");tabs.forEach(function(t,i){t.addEventListener("click",function(){tabs.forEach(function(x,j){x.setAttribute("aria-selected",j===i?"true":"false");x.tabIndex=j===i?0:-1;panels[j].hidden=j!==i})});t.addEventListener("keydown",function(e){var k=e.key==="ArrowRight"?1:e.key==="ArrowLeft"?-1:0;var n;if(e.key==="Home")n=0;else if(e.key==="End")n=tabs.length-1;else{if(!k)return;n=(i+k+tabs.length)%tabs.length}e.preventDefault();tabs[n].click();tabs[n].focus()})})})();

/* ---- next script ---- */

(function(){var l=document.querySelector('.pv-sl');if(!l)return;var b=l.querySelector('button'),d=l.querySelector('.drawer');var sc=function(){l.classList.toggle('on',scrollY>560)};addEventListener('scroll',sc,{passive:true});sc();b.addEventListener('click',function(){var o=!d.hidden;d.hidden=o;b.setAttribute('aria-expanded',o?'false':'true')});document.addEventListener('keydown',function(e){if(e.key==='Escape'){d.hidden=true;b.setAttribute('aria-expanded','false')}})})();

/* ---- next script ---- */

if(top!==self){document.documentElement.classList.add("embedded")}

/* ---- next script ---- */


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
/* video facade: poster + play, iframe only on click */
document.querySelectorAll('.pv-video[data-embed]').forEach(function(v){
  var b=v.querySelector('button');if(!b)return;
  b.addEventListener('click',function(){var f=document.createElement('iframe');f.src=v.getAttribute('data-embed');f.title=b.getAttribute('aria-label')||'Video';f.allow='autoplay; fullscreen; picture-in-picture';f.allowFullscreen=true;v.innerHTML='';v.appendChild(f)});
});
})();
