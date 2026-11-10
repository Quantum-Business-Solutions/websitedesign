"""Polish layer for scripts/preview.py: a last CSS block, a small JS block, the header search (overlay plus the
generation-time index) and the product-name -> page map used by the explorer and journey chips.

Kept apart so the page renderers stay small. Everything here is vanilla JS and plain CSS, no libraries.
No em or en dashes. Registered in preview.py: POLISH_CSS after MOBILE_LAST_CSS, POLISH_JS with the other scripts,
search_html() after the footer, collect() per rendered page and write_index() once per direction.
"""
from __future__ import annotations

import html as _html
import json
import os
import re

# ----------------------------------------------------------------------------- product name -> page

# first match wins, so the more specific patterns come first. Paths are direction-root relative.
PRODUCT_LINKS = [
    (r"scs-vr", "products/scs-vr-virtual-receiver-software.html"),
    (r"scs-1r", "products/scs-1r.html"),
    (r"263lte|265lte", "products/263lte.html"),
    (r"jamalert", "products/jamalert.html"),
    (r"vault", "services/communicators.html"),
    (r"dual ?com|cell ?com", "products/dualcom.html"),
    (r"xr150 and xr550|xr550|xr650", "products/xr550.html"),
    (r"xt30|xt50|xt75", "products/xt75.html"),
    (r"xf6|xr150fc|xr550fc", "products/xf6.html"),
    (r"virtual keypad", "products/virtual-keypad.html"),
    (r"dealer admin", "products/dealer-admin.html"),
    (r"entr[eé]", "products/entre-enterprise.html"),
    (r"x1 series|\bx1\b", "products/x1.html"),
    (r"digital key", "products/digital-key-credential.html"),
    (r"wallet credential|mobile credential", "products/mobile-credential.html"),
    (r"tmsentry", "products/tmsentry.html"),
    (r"xv gateway", "products/xv-gateways-with-alarmvision.html"),
    (r"vk vms", "news/vk-vms.html"),
    (r"vue plus", "services/video.html"),
    (r"1100 series", "services/wireless.html"),
    (r"smoke|pull station|powercom|fire communicator", "services/fire.html"),
    (r"motion, glassbreak|glassbreak", "services/intrusion.html"),
]


def product_href(name: str):
    n = (name or "").lower()
    for pat, href in PRODUCT_LINKS:
        if re.search(pat, n):
            return href
    return None


# ----------------------------------------------------------------------------- search index

_INDEX: dict[str, list] = {}
_PART = re.compile(r"\b(?:[A-Z]{1,5}-?\d{2,5}[A-Z]{0,4}(?:-[A-Z0-9]+)?|UL ?\d{3,4}[A-Z]?|NFPA ?\d+|SOC ?2)\b")


def _text(frag: str) -> str:
    frag = re.sub(r"(?is)<(script|style|template|svg|noscript)\b.*?</\1>", " ", frag)
    frag = re.sub(r"(?s)<[^>]+>", " ", frag)
    frag = _html.unescape(frag)
    return re.sub(r"\s+", " ", frag).strip()


def collect(dslug: str, page: dict, title: str, desc: str, body_html: str):
    t = _text(body_html)
    words = t.split(" ")
    parts = sorted({m.group(0) for m in _PART.finditer(t)})[:60]
    _INDEX.setdefault(dslug, []).append({
        "t": title, "u": page["file"], "d": desc, "b": " ".join(words[:200]), "k": " ".join(parts)})


def write_index(out_dir: str, dslug: str):
    rows = _INDEX.pop(dslug, [])
    with open(os.path.join(out_dir, dslug, "search-index.json"), "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, separators=(",", ":"))


def search_button(mobile=False):
    cls = "pv-sbtn pv-sbtn-m" if mobile else "pv-sbtn"
    return (f'<button type="button" class="{cls}" data-pv-search aria-label="Search the site" aria-haspopup="dialog">'
            '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true" focusable="false">'
            '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.5 15.5 5 5"/></svg>'
            + ('<span>Search</span>' if mobile else '') + '</button>')


def search_html(ctx):
    root = "../" * ctx.get("depth", 0)
    return (f'<div class="pv-search" id="pv-search" data-root="{root}" hidden role="dialog" aria-modal="true" aria-label="Search the site">'
            '<div class="pv-search-box"><div class="pv-search-in"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.5 15.5 5 5"/></svg>'
            '<input type="search" id="pv-search-q" placeholder="Search products, part numbers, pages" aria-label="Search" autocomplete="off" spellcheck="false" role="combobox" aria-expanded="false" aria-autocomplete="list" aria-controls="pv-search-r">'
            '<button type="button" class="pv-search-x" aria-label="Close search">Esc</button></div>'
            '<ul class="pv-search-r" id="pv-search-r" role="listbox" aria-label="Search results"></ul>'
            '<p class="pv-search-h" aria-live="polite">Type to search. Try XR550, UL 864 or dealer portal. Arrow keys to move, Enter to open.</p></div></div>')


# ----------------------------------------------------------------------------- CSS

POLISH_CSS = r"""
/* ===== polish layer (preview_polish.py): loads last and wins ===== */
/* A: mobile sticky bar */
.pv-sticky .b{background:#14171c;color:#fff;border:1px solid rgba(255,255,255,.28)}
.pv-sticky .a{border:1px solid transparent}
@media(max-width:767px){
  body{padding-bottom:0!important}
  body:has(.pv-sticky) .q-footer{padding-bottom:calc(86px + env(safe-area-inset-bottom,0px))}
  html{scroll-padding-bottom:84px}
}
/* B: fast-lane chip */
.pv-sl > button{background:#14171c!important;color:#fff!important;border:1px solid rgba(255,255,255,.3)!important}
.pv-sl > button:focus-visible{outline:3px solid var(--q-gold);outline-offset:3px}
/* C: directions switcher, a collapsed edge tab */
.pv-switch{position:fixed;right:0;left:auto;bottom:auto;top:58%;z-index:90;display:block;padding:0;background:none;box-shadow:none;border-radius:0;backdrop-filter:none;max-width:none;font:13px/1 Inter,system-ui,sans-serif}
.pv-sw-tab{display:flex;align-items:center;gap:8px;writing-mode:vertical-rl;min-height:132px;width:40px;padding:12px 0;justify-content:center;border:1px solid rgba(255,255,255,.22);border-right:0;border-radius:12px 0 0 12px;background:rgba(20,23,28,.96);color:#fff;font:600 13px/1 Inter,system-ui,sans-serif;letter-spacing:.04em;cursor:pointer;box-shadow:0 8px 24px rgba(0,0,0,.2)}
.pv-sw-tab svg{flex:none;writing-mode:horizontal-tb}
.pv-sw-tab:focus-visible{outline:3px solid var(--q-gold);outline-offset:-3px}
.pv-switch .pv-sw-list{position:absolute;right:100%;top:0;margin-right:8px;display:flex;flex-direction:column;gap:2px;min-width:200px;padding:6px;border-radius:14px;background:rgba(20,23,28,.97);box-shadow:0 14px 40px rgba(0,0,0,.35);visibility:hidden;opacity:0;transform:translateX(8px);transition:opacity .18s,transform .18s,visibility 0s .18s}
.pv-switch:hover .pv-sw-list,.pv-switch:focus-within .pv-sw-list,.pv-switch.open .pv-sw-list{visibility:visible;opacity:1;transform:none;transition:opacity .18s,transform .18s}
.pv-switch .pv-sw-list a{display:flex;align-items:center;min-height:44px;padding:0 14px;border-radius:10px;color:#fff;text-decoration:none;white-space:nowrap;font-size:14px}
.pv-switch .pv-sw-list a:hover,.pv-switch .pv-sw-list a:focus-visible{background:rgba(255,255,255,.14);outline:0}
.pv-switch .pv-sw-list a[aria-current]{background:rgba(255,255,255,.2);box-shadow:inset 0 0 0 1px rgba(255,255,255,.35)}
.pv-switch .lbl{display:none}
.pv-switch-m{transition:opacity .25s}
.pv-quiet:not(:focus-within){opacity:0!important;pointer-events:none!important}
@media(max-width:767px){
  .pv-switch{display:none!important}
  .pv-switch-m{display:block;left:10px;right:auto;bottom:max(14px,env(safe-area-inset-bottom,0px))}
  body:has(.pv-sticky) .pv-switch-m{bottom:calc(78px + env(safe-area-inset-bottom,0px))}
  .pv-switch-m summary{padding:0 14px;min-height:44px;font-size:13.5px;font-weight:600;background:rgba(20,23,28,.96);border:1px solid rgba(255,255,255,.2)}
  .pv-switch-m summary svg{flex:none}
  .pv-switch-m .menu{left:0;right:auto}
  .pv-switch-m[open] summary{border-radius:14px}
}
/* D: stat bands */
.pv-hero-stats b{font-size:clamp(26px,3.4vw,40px);white-space:nowrap}
.pv-hero-stats > div{min-width:0}
@media(max-width:640px){
  .pv-hero-stats{grid-template-columns:1fr 1fr;gap:0;border-top:0;margin-top:40px}
  .pv-hero-stats > div,.pv-hero-stats > div:first-child{padding:18px 14px 18px 0;border-left:0;border-top:1px solid var(--border)}
  .pv-hero-stats > div:nth-child(even){padding-left:16px;border-left:1px solid var(--border)}
  .pv-hero-stats b{font-size:clamp(24px,8vw,34px)}
}
.mo-sgrid{align-items:stretch}
.mo-sc{display:flex;transform:none!important}
.mo-sc-in{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:176px;min-width:0;transform:rotateX(var(--rx,0deg)) rotateY(var(--ry,0deg))!important;box-shadow:0 12px 28px rgba(0,5,69,.16)!important}
.mo-sc b{font-size:clamp(30px,3.6vw,52px);white-space:nowrap;max-width:100%}
.mo-sc b.mo-sc-t{font-size:clamp(20px,2.2vw,30px);white-space:normal;overflow-wrap:normal;hyphens:none;line-height:1.1;text-wrap:balance}
@media(max-width:480px){.mo-sc b{font-size:clamp(26px,9vw,36px)}.mo-sc b.mo-sc-t{font-size:20px}.mo-sc-in{min-height:140px}}
[data-dir="press"] .q-eyebrow,.pv-hero-c .q-eyebrow{letter-spacing:.12em}
@media(max-width:480px){[data-dir="press"] .q-eyebrow{letter-spacing:.08em;font-size:12.5px;text-wrap:balance}}
@media(max-width:640px){.lf-hp-mast{flex-direction:column;gap:2px;letter-spacing:.1em;font-size:12.5px}.lf-hp-mast span{text-wrap:balance}}
/* E: dealer portal mock */
.mo-pt{display:block;color:inherit;text-decoration:none}
.mo-pt:focus-visible{outline:3px solid var(--accent-ink);outline-offset:3px}
.mo-tag{position:absolute;top:10px;right:12px;z-index:2;padding:4px 10px;border-radius:999px;background:var(--q-gold);color:var(--cta-fg);font:700 12px/1 var(--q-sans);letter-spacing:.1em;text-transform:uppercase}
.mo-fld{display:grid;gap:6px;text-align:left}.mo-fl{font-size:14px;font-weight:600;color:var(--fg)}
.mo-vh{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.mo-pnote{margin:2px 0 0;font-size:13.5px;color:var(--fg-muted)}
@media(max-width:768px){
  .mo-screen{min-height:0}
  .mo-login{position:relative;inset:auto;padding:28px 16px}
  .mo-screen:not(.is-in) .mo-dash{display:none}
  .mo-screen.is-in .mo-login{display:none}
  .mo-dash{min-height:0}
  .mo-win{animation:none!important}
}
/* G: partner logo strip */
.pv-logos img{height:32px;max-width:132px;width:auto;object-fit:contain;filter:grayscale(1) opacity(.85);mix-blend-mode:multiply}
.pv-logos-track{align-items:center;gap:56px}.pv-logos{gap:56px}
.pv-logos span{font:600 15px/1.2 var(--q-sans);white-space:nowrap}
@media(max-width:767px){
  .pv-logos{display:block;-webkit-mask-image:none;mask-image:none;overflow:visible}
  .pv-logos-track{animation:none;flex-wrap:wrap;justify-content:center;gap:18px 28px}
  .pv-logos-track[aria-hidden]{display:none}
  .pv-logos img{height:28px;max-width:112px}
  .pv-logos span{white-space:normal;text-align:center}
}
/* I: product image wells */
.mo-fc-img,.pv-pimg{aspect-ratio:4/3;background:var(--bg-alt)}
.mo-fc-img img{object-fit:contain;padding:16px;mix-blend-mode:multiply}
.mo-fc-img.is-ph{display:none}
.mo-fnd-grid{align-items:stretch}
.mo-fc-img .ph-ic{width:56px;height:56px;color:var(--fg-muted);opacity:.5}
/* K: tap targets and forms */
.mo-c3-dot{width:44px;height:44px}
.pv-faq summary{min-height:48px}
.pv-faq summary span{display:inline-grid;place-items:center;min-width:44px;min-height:44px}
.mo-chip,.mo-reset{min-height:44px}
.q-header .q-subnav,.q-header .pv-mega{visibility:hidden;clip-path:inset(0 0 100% 0);box-shadow:none}
.q-nav-item:hover > .q-subnav,.q-nav-item:focus-within > .q-subnav{visibility:visible;clip-path:none;box-shadow:0 24px 60px rgba(0,0,0,.22)}
.q-form input[type=text],.q-form input[type=email],.q-form input[type=tel],.q-form input[type=url],.q-form select,.q-form textarea{border:1px solid #6b7280!important}
.q-form label{font-size:14px!important}
.pv-contact label,.q-section label{font-size:14px}
/* M: carousel on phones */
@media(max-width:767px){
  .mo-c3.is-3d .mo-c3-stage{height:380px}
  .mo-c3.is-3d .mo-c3-card{width:230px}
  .mo-c3.is-3d .mo-c3-card:not(.is-act){opacity:0!important;pointer-events:none!important}
  .mo-c3-ctl{flex-wrap:wrap;gap:4px 24px}
  .mo-c3-dots{order:3;width:100%;justify-content:center;flex-wrap:wrap}
}
/* L: search */
.pv-sbtn{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-width:44px;min-height:44px;padding:0 10px;border:0;background:none;color:var(--chrome-fg);border-radius:10px;cursor:pointer;font:600 15px var(--q-sans)}
.pv-sbtn:hover{color:var(--chrome-accent)}.pv-sbtn:focus-visible{outline:3px solid var(--q-gold);outline-offset:2px}
.q-header-in .pv-sbtn:not(.pv-sbtn-m){margin-left:4px}
.pv-sbtn-m{display:none}
@media(max-width:767px){.q-header-in{align-items:center}.q-header-in .pv-sbtn:not(.pv-sbtn-m){margin-left:auto;margin-right:8px}.pv-sbtn-m{display:flex;justify-content:flex-start;width:100%;padding:0 4px;min-height:48px;color:var(--chrome-fg)!important}}
.pv-search{position:fixed;inset:0;z-index:400;display:flex;justify-content:center;align-items:flex-start;padding:min(12vh,96px) 16px 16px;background:rgba(10,14,22,.6);backdrop-filter:blur(3px)}
.pv-search[hidden]{display:none}
.pv-search-box{width:min(680px,100%);max-height:calc(100vh - 32px);display:flex;flex-direction:column;background:var(--bg);color:var(--fg);border:1px solid var(--border);border-radius:16px;box-shadow:0 40px 100px rgba(0,0,0,.4);overflow:hidden}
.pv-search-in{display:flex;align-items:center;gap:12px;padding:0 14px 0 18px;border-bottom:1px solid var(--border);color:var(--fg-muted)}
.pv-search-in input{flex:1;min-width:0;height:60px;border:0;background:none;color:var(--fg);font:500 18px var(--q-sans);outline:0}
.pv-search-in input:focus-visible{outline:0}
.pv-search-x{min-height:36px;padding:0 10px;border:1px solid var(--border);border-radius:8px;background:var(--bg-alt);color:var(--fg-muted);font:600 13px var(--q-sans);cursor:pointer}
.pv-search-r{list-style:none;margin:0;padding:6px;overflow:auto}
.pv-search-r a{display:block;padding:12px 14px;border-radius:10px;text-decoration:none;color:var(--fg);min-height:44px}
.pv-search-r a b{display:block;font-size:16px}.pv-search-r a small{display:block;margin-top:2px;font-size:13px;color:var(--fg-muted)}
.pv-search-r a p{margin:4px 0 0;font-size:14px;line-height:1.45;color:var(--fg-muted)}
.pv-search-r a mark{background:color-mix(in srgb,var(--q-gold) 55%,transparent);color:inherit;border-radius:3px}
.pv-search-r a[aria-selected=true],.pv-search-r a:hover{background:var(--bg-alt);box-shadow:inset 0 0 0 2px var(--q-gold)}
.pv-search-h{margin:0;padding:10px 18px 14px;font-size:13.5px;color:var(--fg-muted);border-top:1px solid var(--border)}
.pv-search-r:empty{display:none}
.pv-search-in input::-webkit-search-cancel-button{display:none}
@media(max-width:767px){.pv-search{padding-top:12px}}
"""

# ----------------------------------------------------------------------------- JS

POLISH_JS = r"""
(function(){
var d=document;
/* directions switcher: touch toggle, fade away while scrolling */
var sw=d.querySelector('.pv-switch'),tab=sw&&sw.querySelector('.pv-sw-tab');
if(tab){tab.addEventListener('click',function(){var o=sw.classList.toggle('open');tab.setAttribute('aria-expanded',o?'true':'false')});
d.addEventListener('keydown',function(e){if(e.key==='Escape'&&sw.classList.contains('open')){sw.classList.remove('open');tab.setAttribute('aria-expanded','false');tab.focus()}});
d.addEventListener('click',function(e){if(!sw.contains(e.target)){sw.classList.remove('open');tab.setAttribute('aria-expanded','false')}})}
var swm=d.querySelector('.pv-switch-m'),qt=0;
if(swm){addEventListener('scroll',function(){if(swm.open||swm.contains(d.activeElement))return;swm.classList.add('pv-quiet');clearTimeout(qt);qt=setTimeout(function(){swm.classList.remove('pv-quiet')},900)},{passive:true})}
/* carousel: arrow keys work while it is in view and nothing is being typed in */
[].forEach.call(d.querySelectorAll('[data-mo=c3]'),function(root){
var inView=false,st=root.querySelector('.mo-c3-stage');
if('IntersectionObserver' in window){new IntersectionObserver(function(es){inView=es[0].isIntersecting},{threshold:.5}).observe(root)}
d.addEventListener('keydown',function(e){
if(!inView||e.defaultPrevented||e.altKey||e.ctrlKey||e.metaKey)return;
if(e.key!=='ArrowLeft'&&e.key!=='ArrowRight')return;
var a=d.activeElement,t=a&&a.tagName;if(t==='INPUT'||t==='TEXTAREA'||t==='SELECT'||(a&&a.isContentEditable))return;
if(a&&a!==d.body&&st&&st.contains(a))return; /* the stage handles its own keys */
var s=d.getElementById('pv-search');if(s&&!s.hidden)return;
var b=root.querySelector('.mo-c3-btn[data-d="'+(e.key==='ArrowRight'?1:-1)+'"]');if(b){e.preventDefault();b.click()}})});
/* finder: image wells that fail to load drop out, last row stays balanced */
[].forEach.call(d.querySelectorAll('.mo-fc-img img'),function(im){var f=function(){im.parentNode.classList.add('is-ph')};im.addEventListener('error',f);if(im.complete&&im.naturalWidth===0&&im.currentSrc)f()});
[].forEach.call(d.querySelectorAll('.mo-fnd-grid'),function(g){
function bal(){var vis=[].filter.call(g.children,function(c){return !c.hidden&&!c.classList.contains('mo-out')});[].forEach.call(g.children,function(x){x.classList.remove('mo-lc1','mo-lc2a','mo-lc2b','mo-lcs')});
var c=innerWidth>=1025?3:innerWidth>=768?2:1,n=vis.length,r=c>1?n%c:0;
if(c===3){if(r===1)vis[n-1].classList.add('mo-lc1');if(r===2){vis[n-2].classList.add('mo-lc2a');vis[n-1].classList.add('mo-lc2b')}}else if(c===2&&r===1)vis[n-1].classList.add('mo-lcs')}
bal();addEventListener('resize',bal);var w=g.closest('.mo-fnd');if(w)w.addEventListener('click',function(){setTimeout(bal,0);setTimeout(bal,340)})});
/* partner marquee: a visible pause control (WCAG 2.2.2) */
[].forEach.call(d.querySelectorAll('.pv-logos'),function(lg){var tr=lg.querySelector('.pv-logos-track');if(!tr||matchMedia('(prefers-reduced-motion: reduce)').matches)return;
var b=d.createElement('button');b.type='button';b.className='pv-lpp';b.setAttribute('aria-pressed','false');b.textContent='Pause scrolling';lg.insertAdjacentElement('afterend',b);
b.addEventListener('click',function(){var o=lg.classList.toggle('pv-still');b.setAttribute('aria-pressed',o?'true':'false');b.textContent=o?'Resume scrolling':'Pause scrolling'})});
/* mobile menu: aria-expanded, scroll lock, focus trap, Esc closes and restores focus */
var mn=d.querySelector('.q-mnav'),ms=mn&&mn.querySelector('summary');
if(mn&&ms){var sync=function(){var o=mn.open;ms.setAttribute('aria-expanded',o?'true':'false');ms.setAttribute('aria-label',o?'Close menu':'Open menu');var sb=d.getElementById('pv-search');d.documentElement.style.overflow=(o||(sb&&!sb.hidden))?'hidden':''};
sync();mn.addEventListener('toggle',sync);
d.addEventListener('keydown',function(e){if(!mn.open)return;
if(e.key==='Escape'){e.preventDefault();mn.open=false;ms.focus()}
else if(e.key==='Tab'){var f=[ms].concat([].slice.call(mn.querySelectorAll('.q-mnav-panel a[href],.q-mnav-panel button,.q-mnav-panel summary'))).filter(function(n){return n.offsetParent!==null||n===ms});var i=f.indexOf(d.activeElement);
if(i<0){e.preventDefault();f[0].focus()}else if(e.shiftKey&&i===0){e.preventDefault();f[f.length-1].focus()}else if(!e.shiftKey&&i===f.length-1){e.preventDefault();f[0].focus()}}});
addEventListener('resize',function(){if(mn.open&&innerWidth>1024){mn.open=false}})}
/* search */
var box=d.getElementById('pv-search');if(!box)return;
var inp=box.querySelector('input'),ul=box.querySelector('.pv-search-r'),hint=box.querySelector('.pv-search-h'),root=box.getAttribute('data-root')||'',idx=null,loading=false,last=null,sel=-1,res=[];
var q=[];function load(cb){if(idx)return cb();q.push(cb);if(loading)return;loading=true;
fetch(root+'search-index.json').then(function(r){return r.json()}).then(function(j){idx=j;loading=false;var f=q;q=[];f.forEach(function(x){x()})}).catch(function(){loading=false;hint.textContent='The search index could not be loaded. It is generated with the build and needs the site served over http.'})}
function open(){last=d.activeElement;if(mn&&mn.open){mn.open=false}box.hidden=false;d.documentElement.style.overflow='hidden';inp.value='';ul.innerHTML='';hint.textContent='Type to search. Try XR550, UL 864 or dealer portal. Arrow keys to move, Enter to open.';load(function(){});inp.focus();setTimeout(function(){inp.focus()},0)}
function close(){inp.setAttribute('aria-expanded','false');inp.removeAttribute('aria-activedescendant');box.hidden=true;d.documentElement.style.overflow='';if(last&&last.focus)last.focus()}
function esc(s){return s.replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function terms(q){return q.toLowerCase().split(/[^a-z0-9\u00e9]+/).filter(function(x){return x.length>0})}
function rx(w){return new RegExp('\\b'+w.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+(w.length<=3?'\\b':''),'i')}
function score(r,ts,q){var t=r.t.toLowerCase(),dd=(r.d||'').toLowerCase(),b=(r.b||'').toLowerCase(),k=(r.k||'').toLowerCase(),s=0;
if(t.indexOf(q)>-1)s+=14;if(k.indexOf(q)>-1)s+=8;if(b.indexOf(q)>-1)s+=6;
for(var i=0;i<ts.length;i++){var w=ts[i],R=rx(w),h=0;
if(R.test(t))h+=10;if(R.test(k))h+=6;if(R.test(dd))h+=4;
var m=b.match(new RegExp(R.source,'gi'));if(m)h+=Math.min(5,m.length);
if(!h)return 0;s+=h}
return s}
function snip(r,ts){var txt=r.b||r.d||'',p=-1;for(var i=0;i<ts.length&&p<0;i++)p=txt.search(rx(ts[i]));
var s=p<0?0:Math.max(0,p-50),out=(s?'\u2026':'')+txt.slice(s,s+150)+(txt.length>s+150?'\u2026':'');var h=esc(out);
ts.forEach(function(w){if(w.length>1)h=h.replace(new RegExp('('+rx(w).source+'[a-z0-9]*)','ig'),'<mark>$1</mark>')});return h}
function show(){var q=inp.value.trim();sel=-1;if(!q){ul.innerHTML='';hint.textContent='Type to search. Try XR550, UL 864 or dealer portal. Arrow keys to move, Enter to open.';return}
if(!idx){hint.textContent='Loading the index...';return}
var ts=terms(q),ql=q.toLowerCase();
res=idx.map(function(r){return{r:r,s:score(r,ts,ql)}}).filter(function(x){return x.s>0}).sort(function(a,b){return b.s-a.s}).slice(0,8);
ul.innerHTML=res.map(function(x,i){return '<li role="presentation"><a role="option" id="pv-sr-'+i+'" href="'+root+esc(x.r.u)+'"><b>'+esc(x.r.t)+'</b><small>'+esc(x.r.u)+'</small><p>'+snip(x.r,ts)+'</p></a></li>'}).join('');
hint.textContent=res.length?res.length+(res.length===1?' result':' results')+'. Arrow keys to move, Enter to open.':'No pages match "'+q+'". Try a part number such as XR550, or a word like dealer.';
if(res.length)mark(0)}
function mark(i){var as=ul.querySelectorAll('a');if(!as.length)return;sel=(i+as.length)%as.length;[].forEach.call(as,function(a,j){a.setAttribute('aria-selected',j===sel?'true':'false')});as[sel].scrollIntoView({block:'nearest'});inp.setAttribute('aria-activedescendant','pv-sr-'+sel)}
inp.addEventListener('input',function(){load(show);show();inp.setAttribute('aria-expanded',ul.children.length?'true':'false');if(!ul.children.length)inp.removeAttribute('aria-activedescendant')});
box.addEventListener('keydown',function(e){
if(e.key==='Escape'){e.preventDefault();close()}
else if(e.key==='ArrowDown'){e.preventDefault();mark(sel+1)}
else if(e.key==='ArrowUp'){e.preventDefault();mark(sel-1)}
else if(e.key==='Enter'){var a=ul.querySelectorAll('a')[Math.max(sel,0)];if(a){e.preventDefault();location.href=a.href}}
else if(e.key==='Tab'){var f=[].slice.call(box.querySelectorAll('input,button,a')).filter(function(n){return n.offsetParent!==null});if(!f.length)return;var i=f.indexOf(d.activeElement);if(e.shiftKey&&i<=0){e.preventDefault();f[f.length-1].focus()}else if(!e.shiftKey&&i===f.length-1){e.preventDefault();f[0].focus()}}});
box.addEventListener('mousedown',function(e){if(e.target===box)close()});
box.querySelector('.pv-search-x').addEventListener('click',close);
[].forEach.call(d.querySelectorAll('[data-pv-search]'),function(b){b.addEventListener('click',function(){var mn=d.querySelector('.q-mnav');if(mn&&mn.open)mn.open=false;open()})});
d.addEventListener('keydown',function(e){if(e.key!=='/'||e.ctrlKey||e.metaKey||e.altKey||!box.hidden)return;var a=d.activeElement,t=a&&a.tagName;if(t==='INPUT'||t==='TEXTAREA'||t==='SELECT'||(a&&a.isContentEditable))return;e.preventDefault();open()});
})();
"""


POLISH_CSS += r"""
/* J: resource cards with a thumbnail */
.pv-res a.pv-has-thumb{padding:0;overflow:hidden;gap:10px}
.pv-res a.pv-has-thumb > :not(.pv-rthumb){margin-left:24px;margin-right:24px}
.pv-res a.pv-has-thumb > span:last-child{margin-bottom:14px}
.pv-res .pv-rthumb{display:block;aspect-ratio:16/9;min-height:0;margin:0 0 6px;padding:0;background:var(--bg-alt);overflow:hidden;font-weight:400}
.pv-rthumb img{width:100%;height:100%;object-fit:cover;display:block}
/* I: finder grid last row balance (classes set by the polish script) */
@media(min-width:1025px){.mo-fnd-grid{grid-template-columns:repeat(6,minmax(0,1fr))}.mo-fnd-grid > .mo-fc{grid-column:span 2}.mo-fnd-grid > .mo-fc.mo-lc1{grid-column:3/span 2}.mo-fnd-grid > .mo-fc.mo-lc2a{grid-column:2/span 2}.mo-fnd-grid > .mo-fc.mo-lc2b{grid-column:4/span 2}}
@media(min-width:768px) and (max-width:1024px){.mo-fnd-grid > .mo-fc.mo-lcs{grid-column:1/-1;width:calc(50% - 11px);justify-self:center}}
.pv-logos.pv-still .pv-logos-track{animation-play-state:paused!important}
.pv-lpp{display:block;margin:10px auto 0;min-height:44px;padding:0 18px;border:1px solid var(--border);border-radius:99px;background:transparent;color:var(--fg-muted);font:600 14px/1 inherit;font-family:inherit;cursor:pointer}.pv-lpp:hover{color:var(--fg);border-color:var(--fg)}.pv-lpp:focus-visible{outline:3px solid var(--accent-ink,#111);outline-offset:3px}
.pv-chip-a{color:inherit;text-decoration:underline;text-decoration-color:rgba(255,255,255,.45);text-underline-offset:3px}
.pv-chip-a:hover,.pv-chip-a:focus-visible{text-decoration-color:var(--q-gold);color:var(--q-gold);outline:0}
"""


POLISH_CSS += r"""
/* K: accessibility states. Forced colors keeps a visible ring and a visible selected state; more contrast thickens it. */
@media (forced-colors:active){
  :focus-visible{outline:3px solid Highlight!important;outline-offset:3px!important;box-shadow:none!important}
  .mo-chip[aria-pressed=true],.pp-chip[aria-pressed=true],.pp3-opt[aria-pressed=true],.p2-cmp[aria-pressed=true],.dw-hs[aria-pressed=true],.dw-lb[aria-expanded=true],.ex-tab[aria-selected=true],.p2-rt-pick[aria-selected=true],.pv-sw-tab[aria-expanded=true]{background:SelectedItem!important;color:SelectedItemText!important;border:2px solid SelectedItemText!important}
  .mo-c3-dot[aria-current=true]::after{background:Highlight!important}
  .pv-lpp,.ex-pp,.hv-pp,.jy-replay,.pv-wpp{border:2px solid ButtonText!important;background:ButtonFace!important;color:ButtonText!important}
}
@media (prefers-reduced-motion:reduce){
  .pv-lh .hero3d.lf-float::after,.pv-lh .hero3d.lf-float img.fallback,.lf-ps-img,.lf-ps-ring.r2,.dw [data-z]{animation:none!important}
  *,*::before,*::after{transition-duration:.01ms!important;transition-delay:0s!important}
  html{scroll-behavior:auto!important}
}
@media (prefers-contrast:more){
  :focus-visible{outline-width:4px!important}
  .pv-lpp,.ex-pp,.hv-pp{border-width:2px}
}
"""
