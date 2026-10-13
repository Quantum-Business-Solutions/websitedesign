"""Second showpiece module: motion and depth for the sections that read flat.

  tiles      square photo tiles with an icon, a dark gradient, hover zoom and a scroll-linked drift
  pillars    dark glass cards with a rotating light edge, outlined numbers and an icon (mission, vision, standard)
  timelive   a scroll-driven timeline: a sticky year that flips, a progress spine, milestones that wake up as you reach them
  herocover  a hero with the photograph as the background, slow zoom on scroll, copy over a soft scrim
  zoomtour   a pinned stage where one illustration zooms into each room as you scroll
  guide      the free-guide popup: a realistic book, a calm form that validates after you touch it
  JS4        scroll-linked zoom and drift for the frames and photographs

Same rules as showpiece 1: nothing under 13px, 44px tap targets, no opacity on text, motion respects prefers-reduced-motion,
and every claim on the page is a claim already on Kelly's site.
"""
from __future__ import annotations

import json

from preview_showpiece import _svg as _svg1, ICONS as ICONS1

ICONS2 = {
    "legal": '<path d="M12 3v18M5 21h14M7 7h10M7 7l-3 7a3 3 0 0 0 6 0zM17 7l-3 7a3 3 0 0 0 6 0z"/>',
    "health": '<path d="M12 21s-7-4.5-9-9a5 5 0 0 1 9-3 5 5 0 0 1 9 3c-2 4.5-9 9-9 9z"/><path d="M12 9v6M9 12h6"/>',
    "faith": '<path d="M12 2v4M10 4h4M12 6l-6 5v10h12V11zM10 21v-5h4v5"/>',
    "arch": '<path d="M3 21h18M5 21V10l7-6 7 6v11M9 21v-6h6v6"/>',
    "gear": '<circle cx="12" cy="12" r="3.2"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M19.1 4.9L17 7M7 17l-2.1 2.1"/>',
    "brief": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2M3 13h18"/>',
    "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.6"/>',
    "eye": '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
    "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
    "book": '<path d="M4 4h11a3 3 0 0 1 3 3v13H7a3 3 0 0 1-3-3z"/><path d="M4 17a3 3 0 0 1 3-3h11M9 8h5"/>',
    "lock": '<rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3M12 15v2"/>',
    "cloud": '<path d="M7 18a4.5 4.5 0 0 1-.6-8.96A6 6 0 0 1 18 9a4 4 0 0 1-.5 8z"/><path d="M12 12v6M9 15l3-3 3 3"/>',
    "wifi": '<path d="M2 9a15 15 0 0 1 20 0M5 12.5a10.5 10.5 0 0 1 14 0M8.5 16a5.5 5.5 0 0 1 7 0"/><circle cx="12" cy="19" r="1.2"/>',
    "radar": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><path d="M12 12L19 5"/>',
    "disk": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M7 15h.01M11 15h6M3 10h18"/>',
    "close": '<path d="M6 6l12 12M18 6L6 18"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
}


def _svg(name: str) -> str:
    d = ICONS2.get(name) or ICONS1[name]
    return f'<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">{d}</svg>'


CSS4 = r'''
@media(max-width:820px){.pv-hascut{flex-direction:column;align-items:stretch;min-height:0;padding-bottom:36px}
.pv-hascut .pv-cx,.pv-hascut .pv-cx.tall{position:relative;top:auto;right:auto;bottom:auto;align-self:center;width:min(88vw,440px);height:auto;margin:30px auto 0;transform:translateY(40px);opacity:0}
.pv-hascut .pv-cx.tall{width:auto;height:min(480px,118vw)}
.pv-hascut.in .pv-cx{animation:pv-cx-up 1.1s cubic-bezier(.2,.85,.25,1) .1s forwards}
@keyframes pv-cx-up{from{transform:translateY(40px);opacity:0}to{transform:none;opacity:1}}}
.pv-trust li > b.pv-tic{display:grid;place-items:center;flex:none;width:54px;height:54px;border-radius:16px;font-size:0;line-height:0;color:#fff;background:linear-gradient(145deg,#0b1480,#143a7a 55%,#2f8f55);box-shadow:inset 0 1px 0 rgba(255,255,255,.25),0 10px 24px rgba(0,5,69,.28);transition:transform .35s cubic-bezier(.2,.8,.2,1)}
.pv-trust li:hover > b.pv-tic{transform:translateY(-3px) rotate(-4deg)}
.pv-trust li > b.pv-tic svg{width:28px;height:28px;color:#fff}
@media(max-width:820px){.pv-guide-pill{font-size:0!important;gap:0!important;width:52px;height:52px;min-height:52px;padding:0!important;justify-content:center;border-radius:50%}.pv-guide-pill svg{width:24px;height:24px;margin:0}}
.pv-mkt{scroll-margin-top:150px}
.pv-mkt-grid{display:grid;grid-template-columns:1fr 1fr;gap:clamp(28px,5vw,72px);align-items:center}
.pv-mkt.flip .pv-mkt-img{order:2}
.pv-mkt-img{position:relative;border-radius:calc(var(--radius) + 10px);overflow:hidden;aspect-ratio:4/3;box-shadow:0 30px 70px rgba(0,5,69,.2)}
.pv-mkt-img img{width:100%;height:100%;object-fit:cover;display:block}
.pv-mkt h2{margin:14px 0 0}
.pv-mkt .k{font:700 13px/1 var(--q-sans);letter-spacing:.16em;text-transform:uppercase;color:var(--accent-ink)}
.pv-mkt .lead2{font-size:clamp(20px,1.9vw,26px);line-height:1.3;font-weight:700;margin:14px 0 0;color:var(--fg)}
.pv-mkt p{margin:16px 0 0;color:var(--fg-muted);line-height:1.65;max-width:56ch}
.pv-mkt ul{list-style:none;margin:20px 0 0;padding:0;display:grid;gap:10px}
.pv-mkt li{display:flex;gap:12px;align-items:flex-start;font-size:16px;line-height:1.5}
.pv-mkt li::before{content:"";flex:none;width:9px;height:9px;border-radius:50%;background:var(--q-gold);margin-top:8px}
.pv-mkt .btns{display:flex;gap:12px;flex-wrap:wrap;margin-top:26px}
@media(max-width:860px){.pv-mkt-grid{grid-template-columns:1fr}.pv-mkt.flip .pv-mkt-img{order:0}}
@media(max-width:820px){.pv-lh.vbg .q-container{grid-template-columns:minmax(0,1fr)!important}}
section.q-section.pv-st{padding:clamp(36px,4.5vw,64px) clamp(26px,4.5vw,68px)}
@media(max-width:820px){section.q-section.pv-st{padding:32px 22px;gap:22px}}
@media(max-width:820px){.pv-lh.vbg .q-container,.pv-hascut > .q-container{box-sizing:border-box;padding-left:20px;padding-right:20px;max-width:100%}
.pv-lh.vbg{min-height:0}.pv-lh.vbg .q-h1{font-size:clamp(30px,8.4vw,40px)}
.pv-guide-pill{bottom:calc(84px + env(safe-area-inset-bottom,0px))!important;right:12px!important;min-height:44px}
.pv-lh.vbg .pv-hero-stats{margin-top:28px}}
.body-wrapper > div:has(> .hs_cos_wrapper > .q-header){top:-48px!important}
.body-wrapper .q-header{position:relative!important;top:auto!important}
.q-header.is-scrolled .pv-util{max-height:none!important;opacity:1!important}
.q-header .pv-util{transition:none!important}
.pv-hw,.pv-grid.pv-grid-3{display:flex!important;flex-wrap:wrap;justify-content:center;gap:20px}
.pv-hw>*{flex:0 1 calc((100% - 40px)/3);min-width:240px}
.pv-grid.pv-grid-3>*{flex:0 1 calc((100% - 40px)/3);min-width:260px}
@media(max-width:700px){.pv-hw>*,.pv-grid.pv-grid-3>*{flex-basis:100%}}
.pv-story{align-items:center;gap:40px}
.pv-story .stage{position:relative!important;top:auto!important;height:min(60vh,560px)}
.pv-story .steps{gap:26px!important;padding:0!important}
.pv-story .step{color:var(--fg)!important}
.pv-story model-viewer{touch-action:pan-y}
@media(max-width:900px){.pv-story{grid-template-columns:1fr}}
html[data-dir="showcase"] *,html[data-dir="showcase"] *::before,html[data-dir="showcase"] *::after{--q-serif:"Plus Jakarta Sans",system-ui,-apple-system,"Segoe UI",sans-serif!important;--q-sans:"Plus Jakarta Sans",system-ui,-apple-system,"Segoe UI",sans-serif!important}
.body-wrapper > div:has(> .hs_cos_wrapper > .q-header){position:sticky;top:0;z-index:70}
.pv-crumbs:has(+ main > :is(.pv-dark,.pv-lh,.pv-cover):first-child){background:var(--chrome-bg);border-bottom-color:rgba(255,255,255,.1)}
.pv-crumbs:has(+ main > :is(.pv-dark,.pv-lh,.pv-cover):first-child) :is(ol,a){color:rgba(255,255,255,.78)}
.pv-crumbs:has(+ main > :is(.pv-dark,.pv-lh,.pv-cover):first-child) li + li::before{color:rgba(255,255,255,.4)}
.pv-crumbs:has(+ main > :is(.pv-dark,.pv-lh,.pv-cover):first-child) [aria-current]{color:#fff}
.pv-crumbs:has(+ main > :is(.pv-dark,.pv-lh,.pv-cover):first-child) a:hover{color:var(--q-gold)}
.pv-guide-hsf{margin-top:18px}
.pv-guide-hsf form{display:block!important;border:0!important;padding:0!important;background:none!important;box-shadow:none!important;margin:0!important;max-width:none!important}
.pv-guide-hsf fieldset{display:grid!important;grid-template-columns:1fr 1fr;gap:12px 14px;border:0;margin:0 0 12px!important;padding:0;max-width:none!important;min-width:0}
.pv-guide-hsf .hs-form-field{margin:0!important;width:auto!important;float:none!important;min-width:0}
.pv-guide-hsf .hs_firstname{order:1}.pv-guide-hsf .hs_company{order:2}.pv-guide-hsf .hs_email{order:3;grid-column:1/-1}
.pv-guide-hsf label{display:block;font:600 14px/1.3 var(--q-sans,inherit);color:var(--fg);margin:0 0 6px}
.pv-guide-hsf .hs-form-required{color:#b3261e;margin-left:2px}
.pv-guide-hsf .input{margin:0}
.pv-guide-hsf input.hs-input:not([type=checkbox]):not([type=radio]){width:100%!important;min-height:50px;padding:12px 14px;border:1.5px solid var(--border);border-radius:12px;font:500 16px/1.3 var(--q-sans,inherit);background:var(--card);color:var(--fg);box-sizing:border-box}
.pv-guide-hsf input.hs-input:focus{outline:3px solid var(--q-gold);outline-offset:1px;border-color:var(--fg)}
.pv-guide-hsf .hs-error-msgs{list-style:none;margin:6px 0 0;padding:0}.pv-guide-hsf .hs-error-msg,.pv-guide-hsf .hs-error-msgs label{color:#b3261e;font-size:14px;font-weight:500}
.pv-guide-hsf .hs_submit{margin:4px 0 0!important}.pv-guide-hsf .actions{margin:0!important;padding:0!important}
.pv-guide-hsf input[type=submit],.pv-guide-hsf .hs-button{width:100%;min-height:52px;border:0;border-radius:999px;background:var(--q-gold);color:var(--cta-fg);font:800 16px/1 var(--q-sans,inherit);padding:15px 22px;cursor:pointer;transition:transform .2s,box-shadow .2s}
.pv-guide-hsf input[type=submit]:hover{transform:translateY(-2px);box-shadow:0 14px 30px rgba(0,5,69,.25)}
.pv-guide-hsf .submitted-message{font:600 17px/1.5 var(--q-sans,inherit);color:var(--fg);padding:18px;border-radius:14px;background:color-mix(in srgb,var(--q-gold) 18%,transparent)}
.pv-guide-hsf .legal-consent-container,.pv-guide-hsf .hs-richtext{font-size:13px;line-height:1.5}
@media(max-width:560px){.pv-guide-hsf fieldset{grid-template-columns:1fr}}
@media(min-width:900px){.pv-fleet .rail{grid-auto-flow:row;grid-auto-columns:auto;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));overflow:visible;scroll-snap-type:none;padding-bottom:6px}}
/* ===== showpiece 2: depth for sections that read flat ===== */
@property --a{syntax:"<angle>";inherits:false;initial-value:0deg}
.pv-head{max-width:760px;margin:0 auto 44px;text-align:center}
.pv-head p{color:var(--fg-muted);font-size:18px;line-height:1.6;margin:16px auto 0}
.pv-dark .pv-head p{color:rgba(255,255,255,.84)}

/* tiles */
.pv-tiles{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.pv-tile{position:relative;display:block;aspect-ratio:1/1;border-radius:calc(var(--radius) + 6px);overflow:hidden;color:#fff;text-decoration:none;isolation:isolate;background:#0b1236;box-shadow:0 24px 60px rgba(0,5,69,.18);transition:transform .5s cubic-bezier(.2,.7,.2,1),box-shadow .5s}
.pv-tile:hover,.pv-tile:focus-visible{transform:translateY(-8px);box-shadow:0 40px 90px rgba(0,5,69,.3)}
.pv-tile:focus-visible{outline:3px solid var(--q-gold);outline-offset:4px}
.pv-tile img{position:absolute;inset:-6%;width:112%;height:112%;object-fit:cover;z-index:-2;transform:translate3d(0,var(--dy,0px),0) scale(1.02);transition:transform 1.4s cubic-bezier(.2,.7,.2,1);will-change:transform}
.pv-tile:hover img{transform:translate3d(0,var(--dy,0px),0) scale(1.12)}
.pv-tile::before{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(180deg,rgba(0,5,69,.1) 0%,rgba(0,5,69,.2) 38%,rgba(0,5,69,.92) 100%);transition:background .5s}
.pv-tile:hover::before{background:linear-gradient(180deg,rgba(0,5,69,.28) 0%,rgba(0,5,69,.5) 30%,rgba(0,5,69,.96) 100%)}
.pv-tile::after{content:"";position:absolute;inset:0;border-radius:inherit;box-shadow:inset 0 0 0 1px rgba(255,255,255,.18);pointer-events:none}
.pv-tile .ic{position:absolute;left:20px;top:20px;width:52px;height:52px;border-radius:16px;display:grid;place-items:center;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.34);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);transition:background .4s,transform .4s,color .4s}
.pv-tile .ic svg{width:26px;height:26px;stroke:currentColor;fill:none;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}
.pv-tile:hover .ic{background:var(--q-gold);color:var(--cta-fg);transform:rotate(-6deg) scale(1.06)}
.pv-tile .n{position:absolute;right:22px;top:20px;font:700 14px/1 var(--q-sans);letter-spacing:.14em;color:rgba(255,255,255,.88)}
.pv-tile .tx{position:absolute;left:22px;right:22px;bottom:22px}
.pv-tile h3{font-family:var(--q-serif);font-size:clamp(24px,2.3vw,32px);line-height:1.08;margin:0;color:#fff}
.pv-tile p{margin:10px 0 0;font-size:15.5px;line-height:1.5;color:rgba(255,255,255,.9);max-height:0;overflow:hidden;transition:max-height .55s cubic-bezier(.2,.7,.2,1)}
.pv-tile:hover p,.pv-tile:focus-visible p{max-height:130px}
.pv-tile .go{display:inline-flex;align-items:center;gap:8px;margin-top:12px;font-size:14.5px;font-weight:700;color:var(--q-gold)}
.pv-tile .go svg{width:18px;height:18px;stroke:currentColor;fill:none;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round;transition:transform .35s}
.pv-tile:hover .go svg{transform:translateX(5px)}
@media(hover:none){.pv-tile p{max-height:none}}

/* pillars */
.pv-pil{padding:clamp(56px,7vw,104px) 0}
.pv-pil-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
.pv-pil-card{position:relative;border-radius:calc(var(--radius) + 8px);padding:34px 30px 32px;background:linear-gradient(160deg,rgba(255,255,255,.1),rgba(255,255,255,.03));backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);overflow:hidden;isolation:isolate;min-height:340px;transition:transform .5s cubic-bezier(.2,.7,.2,1)}
.pv-pil-card::before{content:"";position:absolute;inset:0;border-radius:inherit;padding:1.5px;background:conic-gradient(from var(--a),transparent 0 62%,var(--q-gold) 80%,transparent 100%);-webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask-composite:exclude;animation:pv-spin 7s linear infinite;z-index:1;pointer-events:none}
.pv-pil-card:nth-child(2)::before{animation-delay:-2.3s}.pv-pil-card:nth-child(3)::before{animation-delay:-4.6s}
@keyframes pv-spin{to{--a:360deg}}
.pv-pil-card::after{content:"";position:absolute;width:320px;height:320px;left:var(--mx,70%);top:var(--my,0%);margin:-160px 0 0 -160px;border-radius:50%;background:radial-gradient(circle,color-mix(in srgb,var(--q-gold) 42%,transparent),transparent 65%);opacity:0;transition:opacity .4s;pointer-events:none;z-index:-1}
.pv-pil-card:hover::after{opacity:.9}.pv-pil-card:hover{transform:translateY(-8px)}
.pv-pil-num{position:absolute;right:20px;top:2px;font:800 120px/1 var(--q-serif);color:transparent;-webkit-text-stroke:1.5px rgba(255,255,255,.2);letter-spacing:-.05em;pointer-events:none;z-index:-1}
.pv-pil-ic{width:64px;height:64px;border-radius:20px;display:grid;place-items:center;background:var(--q-gold);color:var(--cta-fg);box-shadow:0 18px 40px color-mix(in srgb,var(--q-gold) 42%,transparent);transition:transform .5s cubic-bezier(.3,1.5,.5,1)}
.pv-pil-card:hover .pv-pil-ic{transform:rotate(-8deg) scale(1.1)}
.pv-pil-ic svg{width:30px;height:30px;stroke:currentColor;fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.pv-pil-card h3{font-family:var(--q-serif);font-size:30px;margin:28px 0 12px;color:#fff}
.pv-pil-card p{margin:0;font-size:17px;line-height:1.65;color:rgba(255,255,255,.88)}

/* timelive */
.pv-tl3{position:relative}
.pv-tl3-grid{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:clamp(28px,5vw,80px);align-items:start}
.pv-tl3-pin{position:sticky;top:112px;padding:8px 0}
.pv-tl3-year{font-family:var(--q-serif);font-size:clamp(86px,12vw,190px);line-height:.9;letter-spacing:-.05em;color:var(--fg);font-variant-numeric:tabular-nums;display:block;min-height:1em;overflow:hidden}
.pv-tl3-year span{display:inline-block;animation:pv-yearin .6s cubic-bezier(.2,.8,.2,1) both}
@keyframes pv-yearin{from{transform:translateY(60%);opacity:0}to{transform:none;opacity:1}}
.pv-tl3-now{font-family:var(--q-serif);font-size:clamp(24px,2.6vw,34px);line-height:1.12;margin:18px 0 0;color:var(--accent-ink);min-height:2.4em}
.pv-tl3-bar{height:6px;border-radius:6px;background:var(--border);margin:30px 0 0;overflow:hidden;max-width:420px}
.pv-tl3-bar i{display:block;height:100%;width:0;border-radius:6px;background:linear-gradient(90deg,var(--q-gold),var(--q-gold-bright,var(--q-gold)));transition:width .7s cubic-bezier(.2,.7,.2,1)}
.pv-tl3-dots{display:flex;gap:10px;flex-wrap:wrap;margin-top:18px}
.pv-tl3-dots button{all:unset;box-sizing:border-box;min-width:44px;min-height:44px;display:grid;place-items:center;cursor:pointer;font-size:13.5px;font-weight:700;color:var(--fg-muted);border-radius:12px;padding:0 8px;transition:background .3s,color .3s}
.pv-tl3-dots button:hover{background:var(--bg-alt)}.pv-tl3-dots button:focus-visible{outline:3px solid var(--accent-ink)}
.pv-tl3-dots button[aria-current=true]{background:var(--chrome-bg);color:#fff}
.pv-tl3-list{list-style:none;margin:0;padding:0 0 0 38px;position:relative}
.pv-tl3-list::before{content:"";position:absolute;left:9px;top:12px;bottom:12px;width:3px;border-radius:3px;background:var(--border)}
.pv-tl3-list::after{content:"";position:absolute;left:9px;top:12px;width:3px;height:var(--fill,0px);max-height:calc(100% - 24px);border-radius:3px;background:linear-gradient(180deg,var(--q-gold),var(--q-gold-bright,var(--q-gold)));box-shadow:0 0 18px color-mix(in srgb,var(--q-gold) 60%,transparent);transition:height .35s linear}
.pv-tl3-item{position:relative;min-height:46vh;display:flex;align-items:center;padding:12px 0;transform:translateX(22px) scale(.97);transition:transform .6s cubic-bezier(.2,.7,.2,1)}
.pv-tl3-item.on{transform:none}
.pv-tl3-item:not(.on) .pv-tl3-card{background:transparent;box-shadow:none;transition:background .5s,box-shadow .5s,border-color .5s}
.pv-tl3-item::before{content:"";position:absolute;left:-38px;top:50%;width:21px;height:21px;margin-top:-10px;border-radius:50%;background:var(--bg);border:3px solid var(--border);transition:background .4s,border-color .4s,box-shadow .4s,transform .4s}
.pv-tl3-item.on::before,.pv-tl3-item.past::before{background:var(--q-gold);border-color:var(--q-gold)}
.pv-tl3-item.on::before{box-shadow:0 0 0 8px color-mix(in srgb,var(--q-gold) 28%,transparent);transform:scale(1.15)}
.pv-tl3-card{background:var(--card);border:1px solid var(--border);border-radius:calc(var(--radius) + 6px);padding:30px 32px;box-shadow:0 24px 60px rgba(0,5,69,.08);max-width:560px}
.pv-tl3-item.on .pv-tl3-card{box-shadow:0 34px 80px rgba(0,5,69,.18);border-color:color-mix(in srgb,var(--q-gold) 60%,var(--border))}
.pv-tl3-card .y{font-size:13px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--accent-ink)}
.pv-tl3-card h3{font-family:var(--q-serif);font-size:clamp(24px,2.4vw,32px);line-height:1.12;margin:10px 0 12px;color:var(--fg)}
.pv-tl3-card p{margin:0;font-size:17px;line-height:1.65;color:var(--fg-muted)}

/* herocover */
.pv-cover{position:relative;min-height:min(86vh,760px);display:flex;align-items:center;overflow:hidden;color:#fff;background:var(--chrome-bg);isolation:isolate}
.pv-cover .cvimg{position:absolute;inset:-4%;width:108%;height:108%;object-fit:cover;object-position:62% 50%;z-index:-3;transform:scale(calc(1.02 + var(--hs,0) * .18));will-change:transform}
.pv-cover::before{content:"";position:absolute;inset:0;z-index:-2;background:linear-gradient(90deg,var(--chrome-bg) 0%,color-mix(in srgb,var(--chrome-bg) 88%,transparent) 30%,color-mix(in srgb,var(--chrome-bg) 40%,transparent) 58%,transparent 82%),linear-gradient(180deg,rgba(0,5,69,.45) 0,transparent 24%,transparent 70%,var(--chrome-bg) 100%)}
.pv-cover .q-container{position:relative;z-index:1;width:100%;padding-top:96px;padding-bottom:96px}
.pv-cover.right{justify-content:flex-end}.pv-cover.right .cvimg{object-position:30% 50%}
.pv-cover.right::before{background:linear-gradient(270deg,var(--chrome-bg) 0%,color-mix(in srgb,var(--chrome-bg) 93%,transparent) 40%,color-mix(in srgb,var(--chrome-bg) 62%,transparent) 62%,transparent 82%),linear-gradient(180deg,rgba(0,5,69,.45) 0,transparent 24%,transparent 70%,var(--chrome-bg) 100%)}
.pv-cover.right .in{margin-left:auto;max-width:580px}
.pv-cover .in{max-width:640px;transform:translateY(calc(var(--hs,0) * -40px));opacity:calc(1 - var(--hs,0) * .9)}
.pv-cover .q-h1{color:#fff;margin-top:18px}.pv-cover .q-h1 em{color:var(--q-gold);font-style:normal}
.pv-cover .q-lead{color:rgba(255,255,255,.9);margin-top:20px;max-width:560px}
.pv-cover .q-btn-ghost{color:#fff}
.pv-cover-chips{display:flex;gap:12px;flex-wrap:wrap;margin-top:30px}
.pv-cover-chips span{border:1px solid rgba(255,255,255,.3);background:rgba(8,14,40,.55);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);border-radius:999px;padding:9px 18px;font-size:14.5px;font-weight:600}
.pv-cover-chips b{color:var(--q-gold)}

/* zoomtour */
.pv-zt{position:relative;height:calc((var(--n) + 1) * 78vh);background:var(--chrome-bg)}
.pv-zt-pin{position:sticky;top:0;height:100vh;height:100svh;overflow:hidden;isolation:isolate}
.pv-zt-cam{position:absolute;left:0;top:0;transform-origin:0 0;will-change:transform;z-index:0}
.pv-zt-cam img{display:block;width:100%;height:100%}
.pv-zt-pin::after{content:"";position:absolute;inset:0;z-index:1;pointer-events:none;background:radial-gradient(120% 90% at 50% 45%,transparent 45%,rgba(0,5,69,.55) 100%),linear-gradient(180deg,rgba(0,5,69,.55) 0,transparent 22%,transparent 62%,rgba(0,5,69,.85) 100%)}
.pv-zt-top{position:absolute;left:0;right:0;top:clamp(78px,10vh,118px);z-index:3;text-align:center;padding:0 20px;transition:opacity .5s,transform .5s}
.pv-zt-top::before{content:"";position:absolute;left:0;right:0;top:-110px;bottom:-70px;z-index:-1;background:linear-gradient(180deg,rgba(0,5,69,.92) 0,rgba(0,5,69,.78) 55%,transparent 100%);pointer-events:none}
.pv-zt-top h2{color:#fff;margin:14px auto 0;max-width:780px}
.pv-zt-top .q-eyebrow{color:var(--q-gold)}
.pv-zt-top p{color:rgba(255,255,255,.88);font-size:17px;margin:12px auto 0;max-width:560px}
.pv-zt.zoomed .pv-zt-top{opacity:0;transform:translateY(-16px);pointer-events:none}
.pv-zt-cap{position:absolute;z-index:3;left:clamp(20px,5vw,72px);bottom:clamp(24px,7vh,72px);width:min(460px,calc(100% - 40px));background:rgba(8,14,40,.78);border:1px solid rgba(255,255,255,.22);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);border-radius:calc(var(--radius) + 8px);padding:26px 28px;color:#fff;box-shadow:0 40px 90px rgba(0,0,0,.5);transition:opacity .45s,transform .45s}
.pv-zt:not(.zoomed) .pv-zt-cap{opacity:0;transform:translateY(20px);pointer-events:none}
.pv-zt-cap .k{font-size:13px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--q-gold)}
.pv-zt-cap h3{font-family:var(--q-serif);font-size:clamp(26px,2.6vw,34px);line-height:1.1;margin:10px 0 10px;color:#fff}
.pv-zt-cap p{margin:0;font-size:16.5px;line-height:1.6;color:rgba(255,255,255,.9)}
.pv-zt-cap a{display:inline-flex;align-items:center;gap:8px;margin-top:16px;min-height:44px;font-weight:700;font-size:15px;color:var(--q-gold);text-decoration:none}
.pv-zt-cap a svg{width:18px;height:18px;stroke:currentColor;fill:none;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round;flex:0 0 auto}
.pv-zt-rail{position:absolute;z-index:3;right:clamp(14px,3vw,40px);top:50%;transform:translateY(-50%);display:grid;gap:4px}
.pv-zt-rail button{all:unset;box-sizing:border-box;width:44px;height:44px;display:grid;place-items:center;cursor:pointer;border-radius:50%}
.pv-zt-rail button i{width:12px;height:12px;border-radius:50%;background:rgba(255,255,255,.42);border:2px solid rgba(255,255,255,.7);transition:transform .3s,background .3s}
.pv-zt-rail button[aria-current=true] i{background:var(--q-gold);border-color:var(--q-gold);transform:scale(1.5);box-shadow:0 0 0 6px color-mix(in srgb,var(--q-gold) 30%,transparent)}
.pv-zt-rail button:focus-visible{outline:3px solid #fff}
.pv-zt-hint{position:absolute;z-index:3;left:50%;bottom:22px;transform:translateX(-50%);font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:rgba(255,255,255,.9);display:flex;align-items:center;gap:10px;transition:opacity .4s}
.pv-zt.zoomed .pv-zt-hint{opacity:0}
.pv-zt-hint i{width:2px;height:26px;background:linear-gradient(var(--q-gold),transparent);animation:pv-drop 1.6s ease-in-out infinite}
@keyframes pv-drop{0%{transform:scaleY(0);transform-origin:top}50%{transform:scaleY(1);transform-origin:top}51%{transform-origin:bottom}100%{transform:scaleY(0);transform-origin:bottom}}

/* scroll-linked zoom on frames and photographs */
.pv-sz{overflow:hidden}
.pv-sz > img,.pv-sz > video{transform:scale(calc(1.02 + var(--z,.5) * .16));will-change:transform}
.pv-lh.vid .vframe{transform:translateY(calc(var(--hs,0) * 46px)) scale(calc(1 - var(--hs,0) * .1));transform-origin:50% 0}

/* guide: floating pill + modal */
.pv-guide-pill{position:fixed;right:20px;bottom:88px;z-index:90;display:inline-flex;align-items:center;gap:10px;min-height:48px;padding:0 20px 0 14px;border-radius:999px;border:1px solid rgba(255,255,255,.28);background:var(--chrome-bg);color:#fff;font:600 14.5px/1 var(--q-sans);cursor:pointer;box-shadow:0 18px 44px rgba(0,5,69,.4)}
.pv-guide-pill svg{width:22px;height:22px;stroke:var(--q-gold);fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.pv-guide-pill:hover{border-color:var(--q-gold)}.pv-guide-pill:focus-visible{outline:3px solid var(--q-gold);outline-offset:3px}
.pv-guide-bk{position:fixed;inset:0;z-index:200;display:none;align-items:center;justify-content:center;padding:20px;background:rgba(2,6,28,.72);backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px)}
.pv-guide-bk.open{display:flex;animation:pv-fade .3s ease both}
@keyframes pv-fade{from{opacity:0}to{opacity:1}}
.pv-guide{position:relative;width:min(960px,100%);max-height:calc(100vh - 40px);overflow:auto;border-radius:calc(var(--radius) + 12px);background:var(--card);display:grid;grid-template-columns:1fr 1.05fr;box-shadow:0 60px 140px rgba(0,0,0,.6);animation:pv-pop .5s cubic-bezier(.2,.9,.3,1.1) both}
@keyframes pv-pop{from{opacity:0;transform:translateY(26px) scale(.96)}to{opacity:1;transform:none}}
.pv-guide-art{position:relative;background:radial-gradient(120% 90% at 30% 20%,#0d1a6b,var(--chrome-bg));display:grid;place-items:center;padding:34px;min-height:380px;overflow:hidden}
.pv-guide-art::before{content:"";position:absolute;width:380px;height:380px;border-radius:50%;background:color-mix(in srgb,var(--q-gold) 45%,transparent);filter:blur(80px);left:50%;top:48%;margin:-190px 0 0 -190px}
.pv-guide-book{position:relative;width:min(300px,86%);transform:perspective(1100px) rotateY(var(--ry,-12deg)) rotateX(var(--rx,3deg));transition:transform .25s ease-out;filter:drop-shadow(0 38px 44px rgba(0,0,0,.55))}
.pv-guide-book img{display:block;width:100%;height:auto;border-radius:6px}
.pv-guide-body{padding:clamp(26px,3.4vw,44px)}
.pv-guide-body .k{font-size:13px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--accent-ink)}
.pv-guide-body h2{font-family:var(--q-serif);font-size:clamp(26px,3vw,36px);line-height:1.1;margin:10px 0 12px;color:var(--fg)}
.pv-guide-body > p{margin:0 0 16px;font-size:16px;line-height:1.6;color:var(--fg-muted)}
.pv-guide-body ul{list-style:none;margin:0 0 22px;padding:0;display:grid;gap:8px}
.pv-guide-body li{display:flex;gap:10px;align-items:flex-start;font-size:15.5px;line-height:1.45;color:var(--fg)}
.pv-guide-body li::before{content:"";flex:0 0 20px;height:20px;border-radius:50%;margin-top:1px;background:var(--q-gold);background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23000545' stroke-width='3.4' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M6 12.5l4 4 8-9'/%3E%3C/svg%3E");background-size:70%;background-position:center;background-repeat:no-repeat}
.pv-guide form{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.pv-guide .f{position:relative}.pv-guide .f.full{grid-column:1/-1}
.pv-guide .f input{width:100%;height:56px;box-sizing:border-box;padding:22px 14px 6px;font:500 16px/1.2 var(--q-sans);border:1.5px solid var(--border);border-radius:12px;background:var(--bg);color:var(--fg);transition:border-color .2s,box-shadow .2s}
.pv-guide .f label{position:absolute;left:15px;top:17px;font-size:16px;color:var(--fg-muted);pointer-events:none;transition:transform .2s,font-size .2s,color .2s;transform-origin:0 0}
.pv-guide .f input:focus,.pv-guide .f input:not(:placeholder-shown){padding-top:22px}
.pv-guide .f input:focus ~ label,.pv-guide .f input:not(:placeholder-shown) ~ label{transform:translateY(-11px);font-size:13px;color:var(--accent-ink)}
.pv-guide .f input:focus{outline:none;border-color:var(--q-gold);box-shadow:0 0 0 4px color-mix(in srgb,var(--q-gold) 28%,transparent)}
.pv-guide .f.err input{border-color:#c0392b}.pv-guide .f .m{display:none;font-size:13px;color:#b02a1c;margin:5px 2px 0}.pv-guide .f.err .m{display:block}
.pv-guide .go{grid-column:1/-1;min-height:56px;border:0;border-radius:999px;background:var(--q-gold);color:var(--cta-fg);font:700 16.5px/1 var(--q-sans);cursor:pointer;display:inline-flex;align-items:center;justify-content:center;gap:10px;transition:transform .2s,box-shadow .2s}
.pv-guide .go:hover{transform:translateY(-2px);box-shadow:0 16px 36px color-mix(in srgb,var(--q-gold) 45%,transparent)}.pv-guide .go:focus-visible{outline:3px solid var(--accent-ink);outline-offset:3px}
.pv-guide .go svg{width:20px;height:20px;stroke:currentColor;fill:none;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}
.pv-guide .fine{grid-column:1/-1;margin:2px 0 0;font-size:13px;line-height:1.5;color:var(--fg-muted)}
.pv-guide-x{position:absolute;right:12px;top:12px;z-index:3;width:44px;height:44px;border-radius:50%;border:1px solid var(--border);background:var(--card);color:var(--fg);cursor:pointer;display:grid;place-items:center}
.pv-guide-x svg{width:20px;height:20px;stroke:currentColor;fill:none;stroke-width:2;stroke-linecap:round}.pv-guide-x:focus-visible{outline:3px solid var(--accent-ink)}
.pv-guide-ok{display:none;padding:18px 20px;border-radius:14px;background:color-mix(in srgb,var(--q-gold) 20%,var(--card));border:1px solid var(--q-gold);font-size:16px;line-height:1.55;color:var(--fg)}
.pv-guide.done form{display:none}.pv-guide.done .pv-guide-ok{display:block}.pv-guide.done ul{display:none}

/* layers */
.pv-ly{padding:clamp(56px,7vw,104px) 0}
.pv-ly-grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(24px,4vw,64px);align-items:center}
.pv-ly-art{position:relative;max-width:560px;margin:0 auto;width:100%}
.pv-ly-art svg{width:100%;height:auto;display:block;overflow:visible}
.pv-ly-art .track{fill:none;stroke:rgba(255,255,255,.07);stroke-width:14}
.pv-ly-art .ring{fill:none;stroke:rgba(255,255,255,.55);stroke-width:14;stroke-linecap:round;transform-origin:260px 260px;animation:pv-ringspin 22s linear infinite;transition:stroke .4s,filter .4s;cursor:pointer}
.pv-ly-art .ring.r1{animation-duration:30s;animation-direction:reverse}.pv-ly-art .ring.r2{animation-duration:26s}.pv-ly-art .ring.r3{animation-duration:34s;animation-direction:reverse}.pv-ly-art .ring.r4{animation-duration:38s}
.pv-ly-art .ring.on{stroke:var(--q-gold);stroke-width:18;filter:drop-shadow(0 0 16px color-mix(in srgb,var(--q-gold) 80%,transparent))}
@keyframes pv-ringspin{to{transform:rotate(360deg)}}
.pv-ly-art .core{fill:rgba(255,255,255,.06);stroke:rgba(255,255,255,.3);stroke-width:1.5}
.pv-ly-art .orb{animation:pv-orbfloat 6s ease-in-out infinite;filter:drop-shadow(0 0 14px rgba(99,210,58,.55))}
.pv-ly-list{list-style:none;margin:0;padding:0;display:grid;gap:10px}
.pv-ly-list button{all:unset;box-sizing:border-box;width:100%;display:flex;gap:16px;align-items:flex-start;padding:16px 18px;border-radius:16px;border:1px solid rgba(255,255,255,.14);background:rgba(255,255,255,.05);cursor:pointer;color:#fff;transition:background .3s,border-color .3s,transform .3s;min-height:44px}
.pv-ly-list button:hover{transform:translateX(4px)}
.pv-ly-list button:focus-visible{outline:3px solid #fff;outline-offset:3px}
.pv-ly-list button[aria-pressed=true]{background:rgba(255,255,255,.12);border-color:var(--q-gold)}
.pv-ly-list .ic{flex:0 0 44px;height:44px;border-radius:14px;display:grid;place-items:center;background:rgba(255,255,255,.1);color:#fff;transition:background .3s,color .3s}
.pv-ly-list button[aria-pressed=true] .ic{background:var(--q-gold);color:var(--cta-fg)}
.pv-ly-list .ic svg{width:22px;height:22px;stroke:currentColor;fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.pv-ly-list .tx b{display:block;font-size:17px;margin-bottom:4px}.pv-ly-list .tx span{display:block;font-size:15px;line-height:1.5;color:rgba(255,255,255,.86)}
/* hardware */
.pv-hw{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:20px}
.pv-hw-card{position:relative;background:var(--card);border:1px solid var(--border);border-radius:calc(var(--radius) + 6px);padding:26px;box-shadow:0 20px 50px rgba(0,5,69,.08);transition:transform .4s cubic-bezier(.2,.7,.2,1),box-shadow .4s,border-color .4s;overflow:hidden}
.pv-hw-card:hover{transform:translateY(-8px);box-shadow:0 34px 80px rgba(0,5,69,.18);border-color:var(--q-gold)}
.pv-hw-card .ic{width:56px;height:56px;border-radius:18px;display:grid;place-items:center;background:var(--chrome-bg);color:#fff;margin-bottom:18px;transition:background .4s,color .4s,transform .4s}
.pv-hw-card:hover .ic{background:var(--q-gold);color:var(--cta-fg);transform:rotate(-6deg)}
.pv-hw-card .ic svg{width:28px;height:28px;stroke:currentColor;fill:none;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}
.pv-hw-card .b{font-size:13px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--accent-ink)}
.pv-hw-card h3{font-family:var(--q-serif);font-size:26px;margin:6px 0 8px;color:var(--fg)}.pv-hw-card p{margin:0;font-size:15.5px;line-height:1.6;color:var(--fg-muted)}
.pv-hw-note{margin:18px 0 0;font-size:13.5px;color:var(--fg-muted)}
@media(max-width:1024px){.pv-ly-grid{grid-template-columns:1fr}}
@media(prefers-reduced-motion:reduce){.pv-ly-art .ring,.pv-ly-art .orb{animation:none}}

@media(max-width:1024px){.pv-tiles{grid-template-columns:repeat(2,1fr)}.pv-pil-grid{grid-template-columns:1fr}.pv-pil-card{min-height:0}.pv-tl3-grid{grid-template-columns:1fr}.pv-tl3-pin{top:84px;z-index:3;background:var(--bg);padding:10px 0 14px;border-bottom:1px solid var(--border)}.pv-tl3-year{font-size:clamp(64px,18vw,110px)}.pv-tl3-now{min-height:0;margin-top:6px}.pv-tl3-item{min-height:34vh}.pv-guide{grid-template-columns:1fr}.pv-guide-art{min-height:0;padding:26px 26px 12px}.pv-guide-book{width:min(190px,56%)}}
@media(max-width:640px){.pv-tiles{grid-template-columns:1fr}.pv-tile{aspect-ratio:5/4}.pv-guide form{grid-template-columns:1fr}.pv-guide-pill{right:12px;bottom:84px}.pv-zt-rail{display:none}.pv-zt-cap{padding:20px 22px}}
@media(prefers-reduced-motion:reduce){.pv-pil-card::before{animation:none}.pv-tile img,.pv-tile,.pv-tl3-item,.pv-tl3-bar i,.pv-pil-card,.pv-pil-ic{transition:none}.pv-zt{height:auto}.pv-zt-pin{position:relative;height:auto;min-height:0}.pv-zt-cam{position:relative!important;transform:none!important;width:100%!important;height:auto!important}.pv-zt-cap{position:relative;left:auto;bottom:auto;margin:20px auto;opacity:1!important;transform:none!important;pointer-events:auto!important}.pv-zt-hint{display:none}.pv-sz > img,.pv-sz > video,.pv-cover .cvimg{transform:none}.pv-guide,.pv-guide-bk.open{animation:none}}
'''


def _head(s, ctx, dark=False):
    E = ctx["E"]
    eb = f'<div class="q-eyebrow">{E(s["eyebrow"])}</div>' if s.get("eyebrow") else ""
    intro = f'<p>{E(s["intro"])}</p>' if s.get("intro") else ""
    return f'<div class="pv-head">{eb}<h2 class="q-h2" style="margin-top:18px">{E(s["heading"])}</h2>{intro}</div>'


# ------------------------------------------------------------------------------ tiles

def _tiles(s, ctx):
    E, L, rel = ctx["E"], ctx["L"], ctx["rel"]
    cells = ""
    for i, it in enumerate(s["items"], start=1):
        title, text, image, href, icon = it[:5]
        cells += (f'<a class="pv-tile" href="{E(L(href))}"><img src="{E(rel(image))}" alt="" width="800" height="800" loading="lazy">'
                  f'<span class="ic">{_svg(icon)}</span><span class="n">{i:02d}</span>'
                  f'<span class="tx"><h3>{E(title)}</h3><p>{E(text)}</p><span class="go">{E(s.get("go", "Explore"))}{_svg("arrow")}</span></span></a>')
    return f'{ctx["sec_open"](s)} <div class="q-container">{_head(s, ctx)}<div class="pv-tiles">{cells}</div></div></section>'


# ------------------------------------------------------------------------------ pillars

def _pillars(s, ctx):
    E = ctx["E"]
    cards = "".join(
        f'<div class="pv-pil-card"><span class="pv-pil-num" aria-hidden="true">{i:02d}</span><span class="pv-pil-ic">{_svg(it[2] if len(it) > 2 else ["target", "eye", "shield", "book"][(i - 1) % 4])}</span><h3>{E(it[0])}</h3><p>{E(it[1])}</p></div>'
        for i, it in enumerate(s["items"], start=1))
    eb = f'<div class="q-eyebrow">{E(s["eyebrow"])}</div>' if s.get("eyebrow") else ""
    intro = f'<p>{E(s["intro"])}</p>' if s.get("intro") else ""
    return (f'<section class="q-section pv-dark pv-pil"{f" id={chr(34)}{E(s[chr(105)+chr(100)])}{chr(34)}" if s.get("id") else ""}><div class="pv-grid-bg" aria-hidden="true"></div><div class="pv-orb a" aria-hidden="true"></div><div class="q-container">'
            f'<div class="pv-head">{eb}<h2 class="q-h2" style="margin-top:18px">{E(s["heading"])}</h2>{intro}</div><div class="pv-pil-grid">{cards}</div></div></section>')


# ------------------------------------------------------------------------------ timelive

def _timelive(s, ctx):
    E = ctx["E"]
    sid = s.get("id", "tl3")
    items = s["items"]
    lis = "".join(f'<li class="pv-tl3-item" data-i="{i}"><div class="pv-tl3-card"><div class="y">{E(y)}</div><h3>{E(t)}</h3><p>{E(b)}</p></div></li>' for i, (y, t, b) in enumerate(items))
    dots = "".join(f'<button type="button" data-i="{i}" aria-label="{E(y)}: {E(t)}">{E(y)}</button>' for i, (y, t, b) in enumerate(items))
    data = json.dumps([[y, t] for y, t, b in items], ensure_ascii=False)
    js = ("<script>(function(){var r=document.getElementById('" + sid + "');if(!r)return;var rm=matchMedia('(prefers-reduced-motion: reduce)').matches;"
          "var D=" + data + ",its=[].slice.call(r.querySelectorAll('.pv-tl3-item')),yr=r.querySelector('.pv-tl3-year'),nw=r.querySelector('.pv-tl3-now'),bar=r.querySelector('.pv-tl3-bar i'),dots=[].slice.call(r.querySelectorAll('.pv-tl3-dots button')),list=r.querySelector('.pv-tl3-list'),cur=-1;"
          "function set(i){if(i===cur)return;cur=i;its.forEach(function(e,k){e.classList.toggle('on',k===i);e.classList.toggle('past',k<i)});"
          "yr.innerHTML='<span>'+D[i][0]+'</span>';nw.textContent=D[i][1];bar.style.width=((i+1)/D.length*100)+'%';dots.forEach(function(d,k){d.setAttribute('aria-current',k===i?'true':'false')})}"
          "function fill(){var lr=list.getBoundingClientRect(),m=innerHeight*.5;var h=Math.max(0,Math.min(lr.height-24,m-lr.top-12));list.style.setProperty('--fill',h+'px')}"
          "function pick(){var m=innerHeight*.5,best=0,bd=1e9;its.forEach(function(e,k){var b=e.getBoundingClientRect(),c=b.top+b.height/2,d=Math.abs(c-m);if(d<bd){bd=d;best=k}});set(best);fill()}"
          "if(rm){its.forEach(function(e){e.classList.add('on')});set(0)}else{addEventListener('scroll',function(){requestAnimationFrame(pick)},{passive:true});addEventListener('resize',pick);pick()}"
          "dots.forEach(function(d,k){d.addEventListener('click',function(){var t=its[k].getBoundingClientRect().top+scrollY-innerHeight*.28;scrollTo({top:t,behavior:rm?'auto':'smooth'})})});"
          "})();</script>")
    return (f'{ctx["sec_open"](s)} <div class="q-container pv-tl3" id="{E(sid)}">{_head(s, ctx)}<div class="pv-tl3-grid"><div class="pv-tl3-pin"><span class="pv-tl3-year" aria-hidden="true"><span>{E(items[0][0])}</span></span>'
            f'<p class="pv-tl3-now" aria-live="polite">{E(items[0][1])}</p><div class="pv-tl3-bar" aria-hidden="true"><i></i></div><div class="pv-tl3-dots">{dots}</div></div>'
            f'<ol class="pv-tl3-list">{lis}</ol></div></div>{js}</section>')


# ------------------------------------------------------------------------------ herocover

def _herocover(s, ctx):
    E, RAW, L, rel = ctx["E"], ctx["RAW"], ctx["L"], ctx["rel"]
    btns = ""
    if s.get("primary"):
        btns += f'<a class="q-btn" href="{E(L(s["primary"]["href"]))}">{E(s["primary"]["label"])}</a>'
    if s.get("secondary"):
        btns += f'<a class="q-btn-ghost" href="{E(L(s["secondary"]["href"]))}">{E(s["secondary"]["label"])}<span style="width:22px;height:1px;background:currentColor;display:inline-block"></span></a>'
    chips = "".join(f"<span><b>{E(v)}</b> {E(l)}</span>" for v, l in s.get("chips", []))
    return (f'<section class="q-section pv-cover{" right" if s.get("align") == "right" else ""}" id="{E(s.get("id", "hero"))}"><img class="cvimg" src="{E(rel(s["image"]))}" alt="{E(s.get("alt", ""))}" width="{s.get("image_w", 2400)}" height="{s.get("image_h", 1350)}" fetchpriority="high" decoding="async">'
            f'<div class="q-container"><div class="in"><div class="q-eyebrow">{E(s.get("eyebrow", ""))}</div><h1 class="q-h1">{RAW(s["heading"])}</h1><p class="q-lead">{E(s.get("subhead", ""))}</p>'
            f'<div class="pv-p3d-btns" style="display:flex;gap:14px;flex-wrap:wrap;align-items:center;margin-top:28px">{btns}</div>{f"<div class=pv-cover-chips>{chips}</div>" if chips else ""}</div></div></section>')


# ------------------------------------------------------------------------------ zoomtour

def _zoomtour(s, ctx):
    E, L, rel = ctx["E"], ctx["L"], ctx["rel"]
    sid = s.get("id", "zt")
    stops = s["stops"]
    w, h = s.get("image_w", 3200), s.get("image_h", 1786)
    caps = "".join(
        f'<div class="pv-zt-cap-i" data-i="{i}" hidden><div class="k">{E(st["k"])}</div><h3>{E(st["title"])}</h3><p>{E(st["body"])}</p><a href="{E(L(st["href"]))}">{E(st["label"])}{_svg("arrow")}</a></div>'
        for i, st in enumerate(stops))
    rail = "".join(f'<button type="button" data-i="{i}" aria-label="{E(st["title"])}"><i></i></button>' for i, st in enumerate(stops))
    cams = json.dumps([[st["x"], st["y"], st.get("scale", 2.6)] for st in stops])
    js = ("<script>(function(){var r=document.getElementById('" + sid + "');if(!r)return;var rm=matchMedia('(prefers-reduced-motion: reduce)').matches;"
          "var pin=r.querySelector('.pv-zt-pin'),cam=r.querySelector('.pv-zt-cam'),cap=r.querySelector('.pv-zt-cap'),ci=[].slice.call(r.querySelectorAll('.pv-zt-cap-i')),rl=[].slice.call(r.querySelectorAll('.pv-zt-rail button')),S=" + cams + ",N=S.length,AR=" + str(w) + "/" + str(h) + ",cur=-2;"
          "if(rm){ci.forEach(function(e){e.hidden=false});return}"
          "function ease(t){return t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2}"
          "function frame(){var W=pin.clientWidth,H=pin.clientHeight,cw=Math.max(W,H*AR),ch=cw/AR,ox=(W-cw)/2,oy=(H-ch)/2;cam.style.width=cw+'px';cam.style.height=ch+'px';cam.style.left=ox+'px';cam.style.top=oy+'px';"
          "var b=r.getBoundingClientRect(),span=b.height-innerHeight,p=span>0?Math.max(0,Math.min(1,-b.top/span)):0;"
          "var seg=Math.min(N-1e-6,p*N),i=Math.floor(seg),f=seg-i,t=ease(Math.max(0,Math.min(1,(f-.28)/.44))),a=i===0?[50,50,1]:S[i-1],c=S[i];"
          "var x=a[0]+(c[0]-a[0])*t,y=a[1]+(c[1]-a[1])*t,sc=a[2]+(c[2]-a[2])*t;"
          "var tx=W/2-ox-sc*(x/100)*cw,ty=H/2-oy-sc*(y/100)*ch;tx=Math.min(-ox,Math.max(W-sc*cw-ox,tx));ty=Math.min(-oy,Math.max(H-sc*ch-oy,ty));cam.style.transform='translate('+tx+'px,'+ty+'px) scale('+sc+')';"
          "var idx=f>=.5?i:i-1;if(p>=.995)idx=N-1;if(idx!==cur){cur=idx;r.classList.toggle('zoomed',idx>=0);ci.forEach(function(e,k){e.hidden=k!==idx});rl.forEach(function(e,k){e.setAttribute('aria-current',k===idx?'true':'false')})}}"
          "var ticking=0;function on(){if(!ticking){ticking=1;requestAnimationFrame(function(){ticking=0;frame()})}}addEventListener('scroll',on,{passive:true});addEventListener('resize',on);frame();"
          "rl.forEach(function(e,k){e.addEventListener('click',function(){var b=r.getBoundingClientRect(),span=b.height-innerHeight;scrollTo({top:scrollY+b.top+span*((k+.85)/N),behavior:'smooth'})})});"
          "})();</script>")
    eb = f'<div class="q-eyebrow">{E(s["eyebrow"])}</div>' if s.get("eyebrow") else ""
    return (f'<section class="pv-zt" id="{E(sid)}" style="--n:{len(stops)}" aria-label="{E(s["heading"])}"><div class="pv-zt-pin"><div class="pv-zt-cam"><img src="{E(rel(s["image"]))}" alt="{E(s.get("alt", ""))}" width="{w}" height="{h}" loading="lazy" decoding="async"></div>'
            f'<div class="pv-zt-top">{eb}<h2 class="q-h2">{E(s["heading"])}</h2><p>{E(s.get("intro", ""))}</p></div>'
            f'<div class="pv-zt-cap" aria-live="polite">{caps}</div><div class="pv-zt-rail">{rail}</div>'
            f'<div class="pv-zt-hint"><i></i>{E(s.get("hint", "Scroll to fly in"))}</div></div>{js}</section>')


# ------------------------------------------------------------------------------ guide (popup)

def guide(g, ctx):
    """The free-guide pill and modal. g: {label, eyebrow, title, intro, bullets, book, book_alt, submit, fine, thanks}."""
    E, rel = ctx["E"], ctx["rel"]
    bullets = "".join(f"<li>{E(b)}</li>" for b in g.get("bullets", []))
    js = r"""<script>(function(){var p=document.querySelector('.pv-guide-pill'),bk=document.querySelector('.pv-guide-bk');if(!p||!bk)return;var box=bk.querySelector('.pv-guide'),x=bk.querySelector('.pv-guide-x'),f=bk.querySelector('form'),last=null,rm=matchMedia('(prefers-reduced-motion: reduce)').matches;
function open(){last=document.activeElement;bk.classList.add('open');document.body.style.overflow='hidden';setTimeout(function(){var i=bk.querySelector('input');if(i)i.focus()},50)}
function close(){bk.classList.remove('open');document.body.style.overflow='';if(last)last.focus()}
p.addEventListener('click',open);x.addEventListener('click',close);bk.addEventListener('mousedown',function(e){if(e.target===bk)close()});
addEventListener('keydown',function(e){if(!bk.classList.contains('open'))return;if(e.key==='Escape')close();if(e.key==='Tab'){var f2=[].slice.call(bk.querySelectorAll('button,input,a[href]')).filter(function(n){return !n.disabled&&n.offsetParent});if(!f2.length)return;var a=f2[0],z=f2[f2.length-1];if(e.shiftKey&&document.activeElement===a){e.preventDefault();z.focus()}else if(!e.shiftKey&&document.activeElement===z){e.preventDefault();a.focus()}}});
/* the book follows the pointer */
var art=bk.querySelector('.pv-guide-art'),bookEl=bk.querySelector('.pv-guide-book');if(art&&bookEl&&!rm&&matchMedia('(pointer:fine)').matches){art.addEventListener('pointermove',function(e){var r=art.getBoundingClientRect(),px=(e.clientX-r.left)/r.width-.5,py=(e.clientY-r.top)/r.height-.5;bookEl.style.setProperty('--ry',(-12+px*16)+'deg');bookEl.style.setProperty('--rx',(3-py*10)+'deg')});art.addEventListener('pointerleave',function(){bookEl.style.removeProperty('--ry');bookEl.style.removeProperty('--rx')})}
/* validate only after the visitor has touched a field, or tried to send */
var rules={n:function(v){return v.trim().length>1},e:function(v){return /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v.trim())}};
function chk(inp,force){var w=inp.closest('.f'),k=inp.getAttribute('data-r');if(!k)return true;var ok=rules[k](inp.value);if(inp.__t||force)w.classList.toggle('err',!ok);return ok}
f.querySelectorAll('input').forEach(function(i){i.addEventListener('blur',function(){i.__t=1;chk(i)});i.addEventListener('input',function(){if(i.__t)chk(i)})});
f.addEventListener('submit',function(e){e.preventDefault();var ok=true;f.querySelectorAll('input[data-r]').forEach(function(i){if(!chk(i,true))ok=false});if(!ok){var bad=f.querySelector('.err input');if(bad)bad.focus();return}box.classList.add('done');var t=bk.querySelector('.pv-guide-ok');t.setAttribute('tabindex','-1');t.focus()});
})();</script>"""
    return (f'<button type="button" class="pv-guide-pill" aria-haspopup="dialog">{_svg("book")}{E(g.get("label", "Free guide"))}</button>'
            f'<div class="pv-guide-bk" role="dialog" aria-modal="true" aria-labelledby="pv-guide-t"><div class="pv-guide"><button type="button" class="pv-guide-x" aria-label="Close">{_svg("close")}</button>'
            f'<div class="pv-guide-art"><div class="pv-guide-book"><img src="{E(rel(g["book"]))}" alt="{E(g.get("book_alt", ""))}" width="800" height="1000" loading="lazy"></div></div>'
            f'<div class="pv-guide-body"><div class="k">{E(g.get("eyebrow", "Free guide"))}</div><h2 id="pv-guide-t">{E(g["title"])}</h2><p>{E(g.get("intro", ""))}</p><ul>{bullets}</ul>'
            f'<form novalidate autocomplete="on"><div class="f"><input id="pvg-n" type="text" placeholder=" " autocomplete="given-name" data-r="n"><label for="pvg-n">First name</label><span class="m">Please add your first name.</span></div>'
            f'<div class="f"><input id="pvg-c" type="text" placeholder=" " autocomplete="organization"><label for="pvg-c">Company (optional)</label></div>'
            f'<div class="f full"><input id="pvg-e" type="email" placeholder=" " autocomplete="email" data-r="e" inputmode="email"><label for="pvg-e">Work email</label><span class="m">Please use an email like name@company.com.</span></div>'
            f'<button class="go" type="submit">{E(g.get("submit", "Send me the guide"))}{_svg("arrow")}</button><p class="fine">{E(g.get("fine", "One email with the guide, then an occasional note from a person at Kelly. Unsubscribe any time."))}</p></form>'
            f'<div class="pv-guide-ok" role="status">{E(g.get("thanks", "Thank you. The guide is on its way to your inbox. If it does not arrive in a few minutes, check your spam folder or call 1-800-34-KELLY."))}</div></div></div></div>{js}')


# ------------------------------------------------------------------------------ global scroll FX

JS4 = r"""(function(){var rm=matchMedia('(prefers-reduced-motion: reduce)').matches;if(rm)return;
var sz=[].slice.call(document.querySelectorAll('.pv-pb-img,.pv-p3d-stage.photo,.pv-ita-frame,.vframe video'));
sz.forEach(function(e){var t=e.matches('video')?e.parentElement:e;t.classList.add('pv-sz');if(e.matches('video')){e.parentElement.classList.remove('pv-sz')}});
var zs=[].slice.call(document.querySelectorAll('.pv-pb-img,.pv-p3d-stage.photo,.pv-guide-art'));zs.forEach(function(e){e.classList.add('pv-sz')});
var tiles=[].slice.call(document.querySelectorAll('.pv-tile')),heroHs=[].slice.call(document.querySelectorAll('.pv-lh.vid,.pv-cover,.pv-p3d'));
function tick(){var vh=innerHeight;zs.forEach(function(e){var r=e.getBoundingClientRect();if(r.bottom<0||r.top>vh)return;e.style.setProperty('--z',Math.max(0,Math.min(1,(vh-r.top)/(vh+r.height))).toFixed(3))});
tiles.forEach(function(e){var r=e.getBoundingClientRect();if(r.bottom<0||r.top>vh)return;var c=(r.top+r.height/2-vh/2)/vh;e.style.setProperty('--dy',(c*-26).toFixed(1)+'px')});
heroHs.forEach(function(e){var r=e.getBoundingClientRect();if(r.bottom<0)return;e.style.setProperty('--hs',Math.max(0,Math.min(1,-r.top/Math.max(1,r.height*.8))).toFixed(3))})}
var tk=0;function on(){if(!tk){tk=1;requestAnimationFrame(function(){tk=0;tick()})}}addEventListener('scroll',on,{passive:true});addEventListener('resize',on);tick();
/* cursor glow on the pillars */
if(matchMedia('(pointer:fine)').matches){document.querySelectorAll('.pv-pil-card').forEach(function(c){c.addEventListener('pointermove',function(e){var r=c.getBoundingClientRect();c.style.setProperty('--mx',(e.clientX-r.left)+'px');c.style.setProperty('--my',(e.clientY-r.top)+'px')})})}
})();"""

RENDER_EXTRA4 = {"tiles": _tiles, "pillars": _pillars, "timelive": _timelive, "herocover": _herocover, "zoomtour": _zoomtour}


# ------------------------------------------------------------------------------ layers (concentric protection diagram)

ORB_PATH = ("M520 86 C360 100 250 210 205 350 C270 230 400 160 585 142 C570 115 550 98 520 86 Z M138 82 C120 200 160 400 315 505 C200 470 100 340 75 170 C90 130 115 100 138 82 Z "
            "M250 365 C380 330 520 380 610 460 C600 485 590 495 578 505 C500 420 380 370 250 365 Z")


def _layers(s, ctx):
    E = ctx["E"]
    sid = s.get("id", "layers")
    items = s["items"]  # [title, text, icon]
    n = len(items)
    cx = cy = 260
    radii = [92 + i * 34 for i in range(n)]
    rings = ""
    for i, r in enumerate(radii):
        circ = 2 * 3.14159 * r
        rings += (f'<circle class="ring r{i}" data-i="{i}" cx="{cx}" cy="{cy}" r="{r}" stroke-dasharray="{circ * .24:.1f} {circ * .04:.1f}"/>'
                  f'<circle class="track" cx="{cx}" cy="{cy}" r="{r}"/>')
    k = 44 / 310
    orb = (f'<g transform="translate({cx} {cy})"><g class="orb" transform="scale({k:.4f}) translate(-335 -320)"><circle cx="335" cy="320" r="310" fill="url(#ly-og)"/><circle cx="335" cy="320" r="310" fill="url(#ly-oh)"/><path d="{ORB_PATH}" fill="#D5D6DB"/></g></g>')
    defs = ('<defs><radialGradient id="ly-og" cx="62%" cy="36%" r="78%"><stop offset="0" stop-color="#63D23A"/><stop offset=".5" stop-color="#2FBE1B"/><stop offset="1" stop-color="#198514"/></radialGradient>'
            '<radialGradient id="ly-oh" cx="28%" cy="78%" r="34%"><stop offset="0" stop-color="#9BE87A" stop-opacity=".55"/><stop offset="1" stop-color="#9BE87A" stop-opacity="0"/></radialGradient></defs>')
    svg = f'<svg viewBox="0 0 520 520" role="img" aria-label="{E(s.get("alt", "Layers of protection around your office"))}">{defs}{rings}<circle cx="{cx}" cy="{cy}" r="62" class="core"/>{orb}</svg>'
    lis = "".join(
        f'<li><button type="button" data-i="{i}" aria-pressed="{"true" if i == 0 else "false"}"><span class="ic">{_svg(it[2])}</span><span class="tx"><b>{E(it[0])}</b><span>{E(it[1])}</span></span></button></li>'
        for i, it in enumerate(items))
    js = ("<script>(function(){var r=document.getElementById('" + sid + "');if(!r)return;var rs=[].slice.call(r.querySelectorAll('.ring')),bs=[].slice.call(r.querySelectorAll('.pv-ly-list button'));"
          "function on(i){rs.forEach(function(e,k){e.classList.toggle('on',k===i)});bs.forEach(function(b,k){b.setAttribute('aria-pressed',k===i?'true':'false')})}"
          "bs.forEach(function(b,k){b.addEventListener('mouseenter',function(){on(k)});b.addEventListener('focus',function(){on(k)});b.addEventListener('click',function(){on(k)})});"
          "rs.forEach(function(e,k){e.addEventListener('mouseenter',function(){on(k)})});on(0);"
          "var t=0,rm=matchMedia('(prefers-reduced-motion: reduce)').matches;if(!rm&&'IntersectionObserver' in window){var h=0;new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting&&!t){t=setInterval(function(){if(r.matches(':hover')||r.contains(document.activeElement))return;h=(h+1)%bs.length;on(h)},2600)}else if(!e.isIntersecting){clearInterval(t);t=0}})},{threshold:.3}).observe(r)}"
          "})();</script>")
    eb = f'<div class="q-eyebrow">{E(s["eyebrow"])}</div>' if s.get("eyebrow") else ""
    return (f'<section class="q-section pv-dark pv-ly" id="{E(sid)}"><div class="pv-grid-bg" aria-hidden="true"></div><div class="pv-orb b" aria-hidden="true"></div><div class="q-container"><div class="pv-head">{eb}<h2 class="q-h2" style="margin-top:18px">{E(s["heading"])}</h2><p>{E(s.get("intro", ""))}</p></div>'
            f'<div class="pv-ly-grid"><div class="pv-ly-art">{svg}</div><ul class="pv-ly-list">{lis}</ul></div></div>{js}</section>')


# ------------------------------------------------------------------------------ hardware grid

def _hwgrid(s, ctx):
    E = ctx["E"]
    cards = "".join(f'<div class="pv-hw-card"><span class="ic">{_svg(it[3])}</span><div class="b">{E(it[0])}</div><h3>{E(it[1])}</h3><p>{E(it[2])}</p></div>' for it in s["items"])
    return (f'{ctx["sec_open"](s)} <div class="q-container">{_head(s, ctx)}<div class="pv-hw">{cards}</div>'
            f'{f"<p class=pv-hw-note>{E(s[chr(110)+chr(111)+chr(116)+chr(101)])}</p>" if s.get("note") else ""}</div></section>')


RENDER_EXTRA4.update({"layers": _layers, "hwgrid": _hwgrid})
