"""Pop pass 1 for the home, system and product pages: section types, CSS and JS.

New section types (all read the theme variables, so Showcase, Clean and Press pick them up):
  doors      three big image doors (dealers, specifiers, owners) on a dark stage, hover lift and tilt
  newsfeat   one featured story card plus two small, each with a thumbnail and a reading cue
  proofband  huge outlined numerals that fill when scrolled into view (verified facts only)
  closer     bold closing call-to-action band in the brand yellow
  subnav     sticky in-page section nav with scroll spy
  panelpick  chip questions that map to a real product (mode "select") or a family chooser (mode "path")
  flowviz    animated "how it connects" chain with real product links
  compare    this product beside its closest siblings, spec facts only
  buybar     sticky product bar that slides in once the hero has scrolled out
  connect    animated "works with" hub: the product in the middle, compatible products around it

Server HTML is complete without JS (the picker lists every candidate, the flow and hub are fully lit, the
numerals are filled, the bar stays hidden). POP1_JS upgrades it. prefers-reduced-motion: no tilt, no
count-up, no travelling signal, no slide; state changes happen instantly.
Registered in preview.py as RENDER_POP1, POP1_CSS and POP1_JS.
Rules: no em or en dashes (E() rewrites any that slip in), nothing under 13px, 44px tap targets.
"""
from __future__ import annotations

import json

POP1_CSS = r"""
/* ===== pop1: shared head ===== */
.pp-hd{text-align:center;max-width:800px;margin:0 auto clamp(34px,4vw,56px)}
.pp-hd .q-h2{margin:20px 0 0}
.pp-hd .q-lead{margin:16px auto 0;max-width:640px}
.pp-hd.left{text-align:left;margin-left:0;max-width:none}
.pp-btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;min-height:48px;padding:0 24px;border-radius:999px;font-weight:700;font-size:15.5px;text-decoration:none;border:2px solid transparent;transition:transform .3s cubic-bezier(.2,.7,.2,1),box-shadow .3s,background .3s,color .3s,border-color .3s;cursor:pointer;font-family:inherit;line-height:1}
.pp-btn.gold{background:var(--q-gold);color:#111;box-shadow:0 14px 30px -14px rgba(255,210,61,.8)}
.pp-btn.gold:hover{transform:translateY(-2px);box-shadow:0 20px 36px -14px rgba(255,210,61,.95)}
.pp-btn.ink{background:#111;color:#fff}.pp-btn.ink:hover{transform:translateY(-2px);background:#000;box-shadow:0 18px 32px -16px rgba(0,0,0,.7)}
.pp-btn.line{border-color:currentColor;color:inherit}.pp-btn.line:hover{transform:translateY(-2px);background:rgba(17,17,17,.08)}
.pp-btn .ar{display:inline-block;transition:transform .3s}.pp-btn:hover .ar{transform:translateX(5px)}
.pp-btn:focus-visible,.pp-chip:focus-visible,.pp-subnav a:focus-visible{outline:3px solid var(--q-gold);outline-offset:3px}

/* ===== doors ===== */
.pp-doors{padding:clamp(64px,8vw,112px) 0}
.pp-doors .pp-hd .q-h2{color:#fff}
.pp-door-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(16px,2vw,30px);perspective:1500px;list-style:none;margin:0;padding:0}
.pp-door{position:relative;display:flex;flex-direction:column;height:100%;border-radius:calc(var(--radius) + 16px);overflow:hidden;background:linear-gradient(180deg,rgba(255,255,255,.1),rgba(255,255,255,.03));border:1px solid rgba(255,255,255,.16);box-shadow:0 40px 80px -44px rgba(0,0,0,.9);transform:translateY(0) rotateX(var(--rx,0deg)) rotateY(var(--ry,0deg));transition:transform .35s cubic-bezier(.2,.7,.2,1),border-color .35s,box-shadow .45s}
.pp-door:hover,.pp-door:focus-within{transform:translateY(-12px) rotateX(var(--rx,0deg)) rotateY(var(--ry,0deg));border-color:rgba(255,210,61,.75);box-shadow:0 0 0 1px rgba(255,210,61,.35),0 64px 96px -44px rgba(0,0,0,.95),0 34px 90px -50px rgba(255,210,61,.55)}
.pp-door-m{position:relative;aspect-ratio:16/11;overflow:hidden;display:grid;place-items:center;background:radial-gradient(circle at 50% 42%,rgba(255,210,61,.3),rgba(255,255,255,.02) 70%)}
.pp-door-m img{max-width:84%;max-height:80%;width:auto;height:auto;object-fit:contain;filter:drop-shadow(0 26px 26px rgba(0,0,0,.5));transition:transform .7s cubic-bezier(.2,.7,.2,1)}
.pp-door-m.cover img{position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:cover;filter:none}
.pp-door-m.cover::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(11,18,32,.1) 30%,rgba(11,18,32,.82))}
.pp-door:hover .pp-door-m img{transform:scale(1.06)}
.pp-door-n{text-shadow:0 2px 14px rgba(0,0,0,.5);position:absolute;right:20px;top:10px;font-family:var(--q-display,var(--q-sans));font-weight:800;font-size:68px;line-height:1;letter-spacing:-.04em;color:transparent;-webkit-text-stroke:1.5px rgba(255,210,61,.75);z-index:2}
.pp-door-k{position:absolute;left:22px;bottom:16px;z-index:2;padding:7px 14px;border-radius:999px;background:var(--q-gold);color:#111;font-size:13px;font-weight:800;letter-spacing:.1em;text-transform:uppercase}
.pp-door-b{display:flex;flex-direction:column;gap:14px;padding:26px 28px 30px;flex:1}
.pp-door-b h3{margin:0;font-size:clamp(22px,2.1vw,29px);line-height:1.14;letter-spacing:-.02em;color:#fff}
.pp-door-b ul{list-style:none;margin:0;padding:0;display:grid;gap:10px}
.pp-door-b li{position:relative;padding-left:30px;font-size:16px;line-height:1.45;color:var(--fg-muted)}
.pp-door-b li::before{content:"";position:absolute;left:0;top:2px;width:20px;height:20px;border-radius:50%;background:var(--q-gold)}
.pp-door-b li::after{content:"";position:absolute;left:7px;top:6px;width:6px;height:10px;border:solid #111;border-width:0 2px 2px 0;transform:rotate(40deg)}
.pp-door-go{margin-top:auto;align-self:flex-start}
.pp-door-go::after{content:"";position:absolute;inset:0;z-index:3}
@media(max-width:1024px){.pp-door-grid{grid-template-columns:minmax(0,1fr);max-width:620px;margin:0 auto}.pp-door-m{aspect-ratio:16/9}}
@media(prefers-reduced-motion:reduce){.pp-door,.pp-door-m img{transition:none}.pp-door:hover,.pp-door:focus-within{transform:none}}

/* ===== newsfeat ===== */
.pp-nf-sec{padding-top:clamp(56px,6vw,88px);padding-bottom:clamp(56px,6vw,88px)}
.pp-nf-head{display:flex;justify-content:space-between;align-items:flex-end;gap:24px 48px;flex-wrap:wrap;margin-bottom:clamp(28px,3.4vw,44px)}
.pp-nf-head .q-h2{margin:18px 0 0;max-width:18ch}
.pp-nf-head .q-lead{margin:0;max-width:340px}
.pp-nf{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(0,1fr);gap:clamp(16px,2vw,26px)}
.pp-nf-side{display:grid;gap:clamp(16px,2vw,26px);grid-template-rows:repeat(2,minmax(0,1fr))}
.pp-nc{position:relative;display:flex;flex-direction:column;border-radius:calc(var(--radius) + 12px);overflow:hidden;background:var(--card);border:1px solid var(--border);color:inherit;text-decoration:none;box-shadow:0 2px 4px rgba(17,24,39,.05),0 26px 44px -32px rgba(17,24,39,.45);transition:transform .4s cubic-bezier(.2,.7,.2,1),box-shadow .4s,border-color .4s}
.pp-nc:hover{transform:translateY(-6px);border-color:var(--q-gold);box-shadow:0 4px 8px rgba(17,24,39,.06),0 44px 64px -30px rgba(17,24,39,.55)}
.pp-nc:focus-visible{outline:3px solid var(--q-gold);outline-offset:3px}
.lf-dark .pp-nc{background:linear-gradient(180deg,rgba(255,255,255,.09),rgba(255,255,255,.03));border-color:rgba(255,255,255,.15)}
.pp-nc-m{position:relative;overflow:hidden;display:grid;place-items:center;background:radial-gradient(circle at 50% 40%,#fff,#e4e9f3 82%)}
.pp-nc.big .pp-nc-m{aspect-ratio:16/9}
.pp-nc-m img{max-width:80%;max-height:84%;width:auto;height:auto;object-fit:contain;mix-blend-mode:multiply;transition:transform .7s cubic-bezier(.2,.7,.2,1)}
.pp-nc.big .pp-nc-m img{max-height:86%}
.pp-nc-m.cover img{position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:cover;mix-blend-mode:normal}
.pp-nc:hover .pp-nc-m img{transform:scale(1.06)}
.pp-nc-k{position:absolute;left:16px;top:16px;z-index:2;padding:6px 12px;border-radius:999px;background:var(--q-gold);color:#111;font-size:13px;font-weight:800;letter-spacing:.06em;text-transform:uppercase}
.pp-nc-b{display:flex;flex-direction:column;gap:10px;padding:22px 26px 26px;flex:1}
.pp-nc.big .pp-nc-b{padding:28px 32px 32px}
.pp-nc-b h3{margin:0;font-size:19px;line-height:1.22;letter-spacing:-.01em;color:var(--fg)}
.pp-nc.big h3{font-size:clamp(25px,2.5vw,35px);line-height:1.12;letter-spacing:-.025em}
.pp-nc-b p{margin:0;font-size:15.5px;line-height:1.55;color:var(--fg-muted)}
.pp-nc.sm p{display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;font-size:14.5px}
.pp-nc-cue{margin-top:auto;padding-top:6px;font-weight:700;font-size:14.5px;color:var(--accent-ink);display:inline-flex;align-items:center;gap:8px}
.pp-nc-cue::after{content:"\2192";transition:transform .3s}.pp-nc:hover .pp-nc-cue::after{transform:translateX(6px)}
.pp-nc.sm{flex-direction:row}
.pp-nc.sm .pp-nc-m{flex:0 0 38%}
.pp-nc.sm .pp-nc-k{left:10px;top:10px;font-size:13px;padding:5px 10px}
.pp-nc.sm .pp-nc-b{padding:20px 22px;justify-content:center}
@media(max-width:1024px){.pp-nf{grid-template-columns:minmax(0,1fr)}.pp-nf-side{grid-template-rows:none}}
@media(max-width:520px){.pp-nc.sm{flex-direction:column}.pp-nc.sm .pp-nc-m{flex:none;aspect-ratio:16/9}.pp-nc.sm .pp-nc-b{padding:18px 20px 22px}}
@media(prefers-reduced-motion:reduce){.pp-nc,.pp-nc-m img{transition:none}.pp-nc:hover{transform:none}}

/* ===== proof ===== */
.pp-proof{padding:clamp(72px,9vw,132px) 0;text-align:center}
.pp-proof .pp-hd .q-h2{color:#fff}
.pp-pr-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(18px,3vw,56px);margin:0 auto;list-style:none;padding:0;align-items:end}
.pp-pr{display:flex;flex-direction:column;align-items:center;gap:14px;min-width:0}
.pp-num{display:block;max-width:100%;font-family:var(--q-display,var(--q-sans));font-weight:800;font-size:clamp(84px,14vw,224px);line-height:.88;letter-spacing:-.055em;color:transparent;-webkit-text-stroke:2px var(--q-gold);background:linear-gradient(180deg,#ffe27a,var(--q-gold)) no-repeat left bottom/100% 100%;-webkit-background-clip:text;background-clip:text;padding-bottom:.04em}
.pp-num.t{font-size:clamp(52px,8vw,126px);letter-spacing:-.04em;white-space:nowrap}
html.pv-js .pp-pr .pp-num{background-size:0% 100%;transition:background-size 1.5s cubic-bezier(.2,.7,.2,1)}
html.pv-js .pp-pr.in .pp-num{background-size:100% 100%}
.pp-pr b{font-size:clamp(17px,1.5vw,21px);line-height:1.3;color:#fff;font-weight:700;max-width:18ch}
.pp-pr span.s{font-size:14.5px;color:var(--fg-muted);margin-top:-6px}
.pp-pr-foot{display:flex;align-items:center;justify-content:center;gap:20px;margin:clamp(40px,5vw,72px) auto 0;color:var(--fg-muted);font-size:clamp(15px,1.4vw,18px);max-width:820px}
.pp-pr-foot::before,.pp-pr-foot::after{content:"";flex:1 1 40px;height:1px;background:linear-gradient(90deg,transparent,rgba(255,210,61,.7))}
.pp-pr-foot::after{background:linear-gradient(90deg,rgba(255,210,61,.7),transparent)}
.pp-pr-foot span{flex:0 1 auto}
@media(max-width:760px){.pp-pr-grid{grid-template-columns:minmax(0,1fr);gap:40px}.pp-num{font-size:clamp(96px,32vw,150px)}.pp-num.t{font-size:clamp(60px,19vw,100px)}}
@media(prefers-reduced-motion:reduce){html.pv-js .pp-pr .pp-num{transition:none;background-size:100% 100%}}

/* ===== closer ===== */
.pp-closer{position:relative;overflow:hidden;isolation:isolate;background:var(--q-gold);color:#111;padding:clamp(64px,8vw,116px) 0;border-bottom:0}
.pp-closer::before{content:"";position:absolute;inset:0;z-index:-1;background:repeating-radial-gradient(circle at 96% 108%,transparent 0 54px,rgba(17,17,17,.09) 54px 56px),radial-gradient(900px 400px at 8% -20%,rgba(255,255,255,.35),transparent 60%)}
.pp-closer .q-container{display:grid;grid-template-columns:minmax(0,1fr);gap:0}
.pp-closer .eb{font-size:13px;letter-spacing:.16em;text-transform:uppercase;font-weight:800;color:#111;opacity:.75;margin:0 0 18px;display:flex;align-items:center;gap:14px}
.pp-closer .eb::before{content:"";width:34px;height:2px;background:#111}
.pp-closer h2{margin:0;color:#111;font-size:clamp(34px,5.6vw,80px);line-height:1;letter-spacing:-.04em;max-width:16ch;font-weight:800}
.pp-closer p{margin:22px 0 0;font-size:clamp(17px,1.6vw,21px);line-height:1.5;max-width:560px;color:#1c1c1c}
.pp-closer .bt{display:flex;flex-wrap:wrap;gap:14px;margin-top:36px}
.pp-closer .pp-btn{min-height:56px;padding:0 30px;font-size:16.5px}
.pp-closer .pp-btn.line{color:#111;border-color:#111}
@media(max-width:520px){.pp-closer .bt .pp-btn{width:100%}}

/* ===== subnav ===== */
.pp-subnav{position:sticky;top:var(--pp-hdr,81px);z-index:40;background:color-mix(in srgb,var(--bg) 90%,transparent);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);border-bottom:1px solid var(--border);box-shadow:0 14px 26px -24px rgba(17,24,39,.55)}
.pp-subnav .q-container{display:flex;align-items:center;gap:20px;min-height:58px}
.pp-sn-t{font-weight:800;font-size:15px;white-space:nowrap;color:var(--fg);display:inline-flex;align-items:center;gap:10px}
.pp-sn-t::before{content:"";width:10px;height:10px;border-radius:50%;background:var(--q-gold);box-shadow:0 0 0 4px color-mix(in srgb,var(--q-gold) 30%,transparent)}
.pp-subnav ul{display:flex;gap:2px;list-style:none;margin:0;padding:0;overflow-x:auto;scrollbar-width:none;flex:1 1 auto;min-width:0}
.pp-subnav ul::-webkit-scrollbar{display:none}
.pp-subnav li{flex:0 0 auto}
.pp-subnav a{position:relative;display:inline-flex;align-items:center;min-height:44px;padding:0 16px;font-weight:600;font-size:15px;color:var(--fg-muted);white-space:nowrap;text-decoration:none;transition:color .25s}
.pp-subnav a::after{content:"";position:absolute;left:16px;right:16px;bottom:4px;height:3px;border-radius:2px;background:var(--q-gold);transform:scaleX(0);transform-origin:left;transition:transform .35s cubic-bezier(.2,.7,.2,1)}
.pp-subnav a:hover{color:var(--fg)}
.pp-subnav a.on{color:var(--fg)}.pp-subnav a.on::after{transform:scaleX(1)}
.pp-sn-cta{flex:0 0 auto;min-height:44px;padding:0 20px;font-size:14.5px}
html:has(.pp-subnav){scroll-padding-top:calc(var(--pp-hdr,81px) + 72px)}
@media(max-width:900px){.pp-subnav .pp-sn-t,.pp-subnav .pp-sn-cta{display:none}.pp-subnav .q-container{gap:0}}
@media(prefers-reduced-motion:reduce){.pp-subnav a,.pp-subnav a::after{transition:none}}

/* ===== panelpick ===== */
.pp-pick{padding:clamp(60px,7vw,100px) 0}
.pp-pk{display:grid;grid-template-columns:minmax(0,.78fr) minmax(0,1.22fr);gap:clamp(18px,2.6vw,40px);align-items:stretch;background:var(--card);border:1px solid var(--border);border-radius:calc(var(--radius) + 20px);padding:clamp(18px,2.8vw,40px);box-shadow:0 2px 4px rgba(17,24,39,.05),0 40px 70px -46px rgba(17,24,39,.5)}
.pp-qs{display:flex;flex-direction:column;gap:26px;justify-content:center;min-width:0}
.pp-q{margin:0;padding:0;border:0;min-width:0}
.pp-q legend{display:flex;align-items:center;gap:12px;padding:0;margin:0 0 12px;font-weight:700;font-size:17px;color:var(--fg)}
.pp-q legend i{font-style:normal;flex:0 0 auto;width:28px;height:28px;border-radius:50%;background:var(--q-gold);color:#111;font-size:14px;font-weight:800;display:grid;place-items:center}
.pp-chips{display:flex;flex-wrap:wrap;gap:8px}
.pp-chip{min-height:44px;padding:0 18px;border-radius:999px;border:1.5px solid var(--border);background:var(--bg);color:var(--fg);font:600 15px/1.2 var(--q-sans);cursor:pointer;transition:transform .25s,background .25s,border-color .25s,box-shadow .25s}
.pp-chip:hover{border-color:var(--q-gold);transform:translateY(-2px)}
.pp-chip[aria-pressed="true"]{background:var(--q-gold);border-color:var(--q-gold);color:#111;box-shadow:0 12px 24px -14px rgba(255,210,61,.95)}
.pp-note{margin:0;display:flex;gap:10px;align-items:flex-start;font-size:14.5px;line-height:1.5;color:var(--fg-muted)}
.pp-note::before{content:"";flex:0 0 18px;height:18px;margin-top:2px;border-radius:50%;border:2px solid var(--q-gold);background:radial-gradient(circle,var(--q-gold) 0 3px,transparent 4px)}
.pp-out{--bg:#0b1220;--bg-alt:#121c30;--fg:#f4f6fb;--fg-muted:#b7c0d3;--border:rgba(255,255,255,.14);--card:rgba(255,255,255,.055);--accent-ink:#ffd23d;color:var(--fg);position:relative;isolation:isolate;overflow:hidden;border-radius:calc(var(--radius) + 14px);padding:clamp(18px,2.4vw,32px);background:radial-gradient(520px 320px at 88% -10%,rgba(255,210,61,.2),transparent 62%),linear-gradient(165deg,#15213a,#0b1220 68%);display:flex;flex-direction:column;gap:16px;min-width:0}
.pp-out-l{margin:0;font-size:13px;letter-spacing:.14em;text-transform:uppercase;font-weight:800;color:#ffd23d}
.pp-rs{display:flex;flex-direction:column;gap:16px}
.pp-rs.swap{animation:pp-swap .45s cubic-bezier(.2,.7,.2,1)}
@keyframes pp-swap{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
.pp-r{display:grid;grid-template-columns:minmax(0,.8fr) minmax(0,1.2fr);gap:clamp(14px,2vw,28px);align-items:center;padding:0;min-width:0}
.pp-r[hidden]{display:none}
.pp-r-i{position:relative;display:grid;place-items:center;min-height:150px;border-radius:calc(var(--radius) + 8px);background:radial-gradient(circle at 50% 45%,rgba(255,210,61,.24),rgba(255,255,255,.03) 70%);aspect-ratio:4/3;overflow:hidden}
.pp-r-i img{max-width:88%;max-height:88%;width:auto;height:auto;object-fit:contain;filter:drop-shadow(0 22px 22px rgba(0,0,0,.5))}
.pp-r-i.light img{background:#fff;padding:10px;border-radius:12px;filter:none}
.pp-r-t{min-width:0}
.pp-r-k{margin:0 0 6px;font-size:13px;letter-spacing:.12em;text-transform:uppercase;font-weight:800;color:#ffd23d}
.pp-r-t h3{margin:0;font-size:clamp(22px,2.2vw,30px);line-height:1.12;letter-spacing:-.02em;color:#fff}
.pp-why{margin:10px 0 0;font-size:16px;line-height:1.5;color:#d6dcea}
.pp-facts{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0 0;padding:0;list-style:none}
.pp-facts li{padding:7px 12px;border-radius:12px;border:1px solid rgba(255,255,255,.18);background:rgba(255,255,255,.06);font-size:13.5px;line-height:1.25;color:#e9edf6}
.pp-facts b{display:block;font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:#b7c0d3;font-weight:600}
.pp-r-go{display:flex;flex-wrap:wrap;gap:10px;margin-top:16px}
.pp-r-go .pp-btn{min-height:44px;padding:0 20px;font-size:15px}
.pp-r-go .pp-btn.line{color:#fff;border-color:rgba(255,255,255,.4)}.pp-r-go .pp-btn.line:hover{border-color:#ffd23d;color:#ffd23d;background:transparent}
.pp-soon{display:inline-block;margin-left:8px;padding:3px 9px;border-radius:999px;background:#ffd23d;color:#111;font-size:13px;font-weight:800;letter-spacing:.04em;text-transform:uppercase;vertical-align:middle}
.pp-also{margin:0;padding:14px 0 0;border-top:1px solid rgba(255,255,255,.14);font-size:14.5px;line-height:1.55;color:#c4ccdc}
.pp-also a{color:#ffd23d;font-weight:700;text-decoration:underline;text-underline-offset:3px}
.pp-also + .pp-also{padding-top:0;border-top:0;margin-top:-6px}
html:not(.pv-js) .pp-qs .pp-chips,html:not(.pv-js) .pp-qs .pp-q{display:none}
html:not(.pv-js) .pp-pk{grid-template-columns:minmax(0,1fr)}
html:not(.pv-js) .pp-qs{display:none}
.pp-stat{display:none}
html:not(.pv-js) .pp-stat{display:block}
@media(max-width:1024px){.pp-pk{grid-template-columns:minmax(0,1fr)}}
@media(max-width:620px){.pp-r{grid-template-columns:minmax(0,1fr)}.pp-r-i{aspect-ratio:16/9}.pp-chip{padding:0 14px}}
@media(prefers-reduced-motion:reduce){.pp-rs.swap{animation:none}.pp-chip{transition:none}}

/* ===== flowviz ===== */
.pp-flow-sec{padding:clamp(60px,7vw,104px) 0}
.pp-flow{--n:5;position:relative;display:grid;grid-template-columns:repeat(var(--n),minmax(0,1fr));list-style:none;margin:0;padding:0}
.pp-fn{position:relative;padding:0 12px;text-align:center;min-width:0;counter-increment:ppf}
.pp-fn-d{position:relative;z-index:2;width:68px;height:68px;margin:0 auto 20px;border-radius:50%;display:grid;place-items:center;font-family:var(--q-display,var(--q-sans));font-size:24px;font-weight:800;background:var(--q-gold);color:#111;box-shadow:0 0 0 7px color-mix(in srgb,var(--q-gold) 22%,transparent),0 18px 34px -14px rgba(255,210,61,.7)}
.pp-fn-d::before{content:counter(ppf)}
.pp-fn::before,.pp-fn::after{content:"";position:absolute;top:33px;left:calc(-50% + 34px);width:calc(100% - 68px);height:3px;border-radius:2px}
.pp-fn:first-child::before,.pp-fn:first-child::after{display:none}
.pp-fn::before{background:repeating-linear-gradient(90deg,rgba(255,255,255,.28) 0 7px,transparent 7px 14px)}
.pp-fn::after{background:var(--q-gold);transform-origin:left;box-shadow:0 0 14px rgba(255,210,61,.7)}
.pp-fn h3{margin:0;font-size:clamp(19px,1.7vw,23px);line-height:1.2;letter-spacing:-.015em;color:var(--fg)}
.pp-fn .w{display:block;margin:6px 0 0;font-size:13px;letter-spacing:.12em;text-transform:uppercase;font-weight:700;color:var(--accent-ink)}
.pp-fn p{margin:12px auto 0;font-size:15.5px;line-height:1.55;color:var(--fg-muted);max-width:26ch}
.pp-fn ul{list-style:none;margin:14px 0 0;padding:0;display:flex;flex-wrap:wrap;gap:6px;justify-content:center}
.pp-fn li a{display:inline-flex;align-items:center;min-height:36px;padding:0 12px;border-radius:999px;border:1px solid var(--border);background:var(--card);color:var(--fg);font-size:13.5px;font-weight:600;text-decoration:none;transition:border-color .25s,background .25s,color .25s,transform .25s}
.pp-fn li a:hover{border-color:var(--q-gold);color:var(--cta-fg);background:var(--q-gold);transform:translateY(-2px)}
.pp-sig{position:absolute;top:27px;left:calc(50% / var(--n));width:15px;height:15px;margin-left:-7px;border-radius:50%;background:#fff;box-shadow:0 0 0 6px rgba(255,210,61,.35),0 0 26px 4px var(--q-gold);opacity:0;z-index:3;pointer-events:none}
html.pv-js .pp-flow:not(.go) .pp-fn::after{transform:scaleX(0)}
html.pv-js .pp-flow:not(.go) .pp-fn-d{background:var(--card);color:var(--fg-muted);box-shadow:none;border:2px solid var(--border)}
html.pv-js .pp-flow.go .pp-fn::after{animation:pp-line .7s cubic-bezier(.4,0,.2,1) calc(var(--i)*.75s - .5s) both}
html.pv-js .pp-flow.go .pp-fn-d{animation:pp-dot .5s cubic-bezier(.2,.7,.2,1) calc(var(--i)*.75s - .2s) both}
html.pv-js .pp-flow.go .pp-sig{animation:pp-sig 6s linear calc(var(--n)*.75s + .2s) infinite}
@keyframes pp-line{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@keyframes pp-dot{0%{transform:scale(.7);background:var(--card);color:var(--fg-muted);box-shadow:none}60%{transform:scale(1.14)}100%{transform:scale(1);background:var(--q-gold);color:#111;box-shadow:0 0 0 7px color-mix(in srgb,var(--q-gold) 22%,transparent),0 18px 34px -14px rgba(255,210,61,.7)}}
@keyframes pp-sig{0%{left:calc(50% / var(--n));opacity:0}6%{opacity:1}94%{opacity:1}100%{left:calc(100% - 50% / var(--n));opacity:0}}
@media(max-width:900px){
 .pp-flow{grid-template-columns:minmax(0,1fr);gap:0}
 .pp-fn{display:grid;grid-template-columns:68px minmax(0,1fr);column-gap:20px;text-align:left;padding:0 0 34px}
 .pp-fn:nth-last-child(2){padding-bottom:0}
 .pp-fn-d{grid-row:1 / span 4;margin:0;width:56px;height:56px;font-size:21px}
 .pp-fn::before,.pp-fn::after{display:block!important;left:27px;top:56px;width:3px;height:calc(100% - 56px)}
 .pp-fn:nth-last-child(2)::before,.pp-fn:nth-last-child(2)::after{display:none!important}
 .pp-fn:first-child::before,.pp-fn:first-child::after{display:block!important}
 .pp-fn::before{background:repeating-linear-gradient(180deg,rgba(255,255,255,.28) 0 7px,transparent 7px 14px)}
 .pp-fn::after{transform-origin:top}
 html.pv-js .pp-flow:not(.go) .pp-fn::after{transform:scaleY(0)}
 .pp-fn p{margin:8px 0 0;max-width:none}
 .pp-fn ul{justify-content:flex-start}
 .pp-sig{display:none}
 @keyframes pp-line{from{transform:scaleY(0)}to{transform:scaleY(1)}}
}
@media(prefers-reduced-motion:reduce){html.pv-js .pp-flow .pp-fn::after,html.pv-js .pp-flow .pp-fn-d,html.pv-js .pp-flow .pp-sig{animation:none!important}html.pv-js .pp-flow:not(.go) .pp-fn::after{transform:none}html.pv-js .pp-flow:not(.go) .pp-fn-d{background:var(--q-gold);color:#111;border:0;box-shadow:0 0 0 7px color-mix(in srgb,var(--q-gold) 22%,transparent)}.pp-sig{display:none}}

/* ===== compare ===== */
.pp-cmp-sec{padding:clamp(56px,6vw,92px) 0}
.pp-cmp{--n:3;border:1px solid var(--border);border-radius:calc(var(--radius) + 16px);background:var(--card);overflow:hidden;box-shadow:0 2px 4px rgba(17,24,39,.05),0 36px 60px -40px rgba(17,24,39,.5)}
.pp-cmp-h,.pp-cmp-r{display:grid;grid-template-columns:minmax(120px,.7fr) repeat(var(--n),minmax(0,1fr))}
.pp-cmp-h{border-bottom:1px solid var(--border)}
.pp-cmp-c{padding:22px 22px 20px;min-width:0;position:relative}
.pp-cmp-c.here{background:linear-gradient(180deg,color-mix(in srgb,var(--q-gold) 22%,var(--card)),color-mix(in srgb,var(--q-gold) 6%,var(--card)))}
.pp-cmp-c.here::before{content:"";position:absolute;left:0;right:0;top:0;height:4px;background:var(--q-gold)}
.pp-cmp-t{min-height:34px}
.pp-cmp-tag{display:inline-block;margin-bottom:10px;padding:4px 10px;border-radius:999px;background:var(--q-gold);color:#111;font-size:13px;font-weight:800;letter-spacing:.06em;text-transform:uppercase}
.pp-cmp-tag.soon{background:var(--fg);color:var(--bg)}
.pp-cmp-img{height:88px;display:flex;align-items:center;margin:0 0 12px}
.pp-cmp-img img{max-height:88px;max-width:100%;width:auto;height:auto;object-fit:contain;mix-blend-mode:multiply}
.pp-cmp-c h3{margin:0;font-size:clamp(18px,1.7vw,22px);line-height:1.2;color:var(--fg)}
.pp-cmp-c h3 a{color:inherit;text-decoration:none}.pp-cmp-c h3 a:hover{color:var(--accent-ink);text-decoration:underline;text-underline-offset:3px}
.pp-cmp-c .k{display:block;margin-top:4px;font-size:14px;color:var(--fg-muted)}
.pp-cmp-r{border-top:1px solid var(--border)}
.pp-cmp-h + .pp-cmp-r{border-top:0}
.pp-cmp-r:nth-child(odd){background:color-mix(in srgb,var(--bg-alt) 55%,transparent)}
.pp-cmp-l{padding:16px 22px;font-size:13px;letter-spacing:.1em;text-transform:uppercase;font-weight:700;color:var(--fg-muted);align-self:center}
.pp-cmp-v{padding:16px 22px;font-size:16.5px;font-weight:600;line-height:1.35;color:var(--fg);align-self:center;min-width:0;overflow-wrap:anywhere}
.pp-cmp-v.here{background:color-mix(in srgb,var(--q-gold) 11%,transparent);font-weight:800}
.pp-cmp-v.na{font-weight:500;font-size:14.5px;color:var(--fg-muted)}
.pp-cmp-n{margin:18px 0 0;font-size:14.5px;color:var(--fg-muted)}
@media(max-width:760px){
 .pp-cmp-h{grid-template-columns:repeat(var(--n),minmax(0,1fr))}.pp-cmp-h > .pp-cmp-l{display:none}
 .pp-cmp-c{padding:16px 12px 14px}.pp-cmp-t{min-height:30px}.pp-cmp-img{height:56px}.pp-cmp-img img{max-height:56px}.pp-cmp-c h3{font-size:15.5px}.pp-cmp-c .k{font-size:13px}.pp-cmp-tag{font-size:13px;padding:3px 8px}
 .pp-cmp-r{grid-template-columns:repeat(var(--n),minmax(0,1fr))}
 .pp-cmp-r > .pp-cmp-l{grid-column:1 / -1;padding:14px 12px 0;font-size:13px}
 .pp-cmp-v{padding:6px 12px 14px;font-size:14.5px}
}

/* ===== buybar ===== */
.pp-bb{position:fixed;left:0;right:0;top:var(--pp-hdr,81px);z-index:45;background:color-mix(in srgb,var(--bg) 98%,transparent);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);border-bottom:1px solid var(--border);box-shadow:0 18px 34px -22px rgba(17,24,39,.6);transform:translateY(-100%);visibility:hidden;opacity:0;transition:transform .4s cubic-bezier(.2,.7,.2,1),opacity .3s,visibility 0s .4s}
.pp-bb.on{transform:none;visibility:visible;opacity:1;transition:transform .4s cubic-bezier(.2,.7,.2,1),opacity .3s,visibility 0s}
.pp-bb .q-container{display:flex;align-items:center;gap:16px;min-height:64px}
.pp-bb-n{flex:1 1 auto;min-width:0;display:flex;align-items:center;gap:14px}
.pp-bb-n img{flex:0 0 auto;height:42px;width:auto;max-width:64px;object-fit:contain}
.pp-bb-n div{min-width:0}
.pp-bb-n b{display:block;font-size:17px;line-height:1.2;color:var(--fg);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.pp-bb-n span{display:block;font-size:13.5px;color:var(--fg-muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.pp-bb-a{flex:0 0 auto;display:flex;gap:8px}
.pp-bb-a .pp-btn{min-height:44px;padding:0 18px;font-size:14.5px;white-space:nowrap}
.pp-bb-a .pp-btn.line{color:var(--fg);border-color:var(--border);background:var(--bg)}.pp-bb-a .pp-btn.line:hover{border-color:var(--q-gold);background:var(--bg)}
.pp-bb .sh{display:none}
@media(max-width:760px){.pp-bb .q-container{gap:10px;min-height:60px}.pp-bb-n img,.pp-bb-n span{display:none}.pp-bb-n b{font-size:15px}.pp-bb-a .pp-btn{padding:0 14px;font-size:14px}.pp-bb .lg{display:none}.pp-bb .sh{display:inline}}
@media(max-width:480px){.pp-bb-n{display:none}.pp-bb-a{flex:1 1 auto}.pp-bb-a .pp-btn{flex:1 1 0;padding:0 8px}}
@media(prefers-reduced-motion:reduce){.pp-bb,.pp-bb.on{transition:none}}

/* ===== connect (works with hub) ===== */
.pp-con-sec{padding:clamp(60px,7vw,104px) 0}
.pp-con{position:relative;display:grid;grid-template-columns:minmax(0,.85fr) minmax(70px,.3fr) minmax(0,1.15fr);gap:0;align-items:stretch}
.pp-con-hub{position:relative;z-index:2;align-self:center;justify-self:end;display:grid;place-items:center;aspect-ratio:1;max-width:400px;width:100%;border-radius:50%}
.pp-con-hub::before{content:"";position:absolute;inset:6%;border-radius:50%;background:radial-gradient(circle,rgba(255,210,61,.3),transparent 66%)}
.pp-con-ring{position:absolute;inset:0;border-radius:50%;border:1px dashed color-mix(in srgb,var(--q-gold) 60%,transparent);animation:pp-spin 60s linear infinite}
.pp-con-ring.r2{inset:13%;border:1px solid var(--border);animation:none}
.pp-con-ring::after{content:"";position:absolute;right:-6px;top:50%;width:12px;height:12px;margin-top:-6px;border-radius:50%;background:var(--q-gold);box-shadow:0 0 18px var(--q-gold)}
.pp-con-core{position:relative;z-index:2;width:62%;display:flex;flex-direction:column;align-items:center;text-align:center;gap:10px}
.pp-con-core img{max-width:100%;max-height:170px;width:auto;height:auto;object-fit:contain;filter:drop-shadow(0 22px 22px rgba(0,0,0,.5))}
.pp-con-core.light img{background:#fff;padding:8px;border-radius:12px;filter:none}
.pp-con-core b{font-size:17px;line-height:1.2;color:var(--fg);background:var(--q-gold);color:#111;padding:6px 14px;border-radius:999px}
.pp-con-svg{display:block;width:100%;height:100%;min-height:100%;z-index:1;pointer-events:none;overflow:visible}
.pp-con-svg path{fill:none;stroke:var(--q-gold);stroke-width:2.5;stroke-linecap:round;vector-effect:non-scaling-stroke;stroke-dasharray:7 9;opacity:.9}
html.pv-js .pp-con:not(.go) .pp-con-svg path{stroke-dasharray:600;stroke-dashoffset:600}
html.pv-js .pp-con.go .pp-con-svg path{stroke-dasharray:7 9;animation:pp-draw 1s ease-out both,pp-flowdash 1.4s linear 1s infinite}
@keyframes pp-draw{from{stroke-dasharray:600;stroke-dashoffset:600}to{stroke-dasharray:600;stroke-dashoffset:0}}
@keyframes pp-flowdash{to{stroke-dashoffset:-32}}
.pp-con-list{position:relative;z-index:2;list-style:none;margin:0;padding:0;display:grid;gap:18px;grid-template-rows:repeat(3,minmax(0,1fr));min-width:0}
.pp-cn{position:relative;display:grid;grid-template-columns:96px minmax(0,1fr);gap:18px;align-items:center;padding:16px 20px 16px 16px;border-radius:calc(var(--radius) + 12px);background:var(--card);border:1px solid var(--border);color:inherit;text-decoration:none;transition:transform .35s cubic-bezier(.2,.7,.2,1),border-color .3s,box-shadow .35s;height:100%}
.pp-cn::before{content:"";position:absolute;left:-8px;top:50%;width:14px;height:14px;margin-top:-7px;border-radius:50%;background:var(--q-gold);box-shadow:0 0 0 5px color-mix(in srgb,var(--q-gold) 28%,transparent)}
.pp-cn:hover{transform:translateX(8px);border-color:var(--q-gold);box-shadow:0 26px 44px -28px rgba(0,0,0,.55),0 0 0 1px color-mix(in srgb,var(--q-gold) 40%,transparent)}
.pp-cn:focus-visible{outline:3px solid var(--q-gold);outline-offset:3px}
.pp-cn-i{display:grid;place-items:center;width:96px;height:84px;border-radius:14px;background:radial-gradient(circle at 50% 40%,#fff,#e4e9f3 85%);overflow:hidden}
.pp-cn-i img{max-width:86%;max-height:86%;width:auto;height:auto;object-fit:contain;mix-blend-mode:multiply}
.pp-cn h3{margin:0;font-size:18px;line-height:1.2;color:var(--fg)}
.pp-cn p{margin:6px 0 0;font-size:14.5px;line-height:1.45;color:var(--fg-muted);display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.pp-cn .go{display:inline-block;margin-top:8px;font-weight:700;font-size:14.5px;color:var(--accent-ink)}
.pp-cn .go::after{content:"\2192";margin-left:8px;display:inline-block;transition:transform .3s}.pp-cn:hover .go::after{transform:translateX(6px)}
@keyframes pp-spin{to{transform:rotate(360deg)}}
@media(max-width:900px){
 .pp-con{grid-template-columns:minmax(0,1fr);gap:0}.pp-con-hub{max-width:300px;justify-self:center}.pp-con-svg{display:none}.pp-cn::before{left:-35px}
 .pp-con-list{margin-top:26px;padding-left:26px;border-left:3px dashed color-mix(in srgb,var(--q-gold) 70%,transparent);margin-left:12px;gap:14px}
 .pp-cn:hover{transform:translateX(4px)}
}
@media(max-width:480px){.pp-cn{grid-template-columns:72px minmax(0,1fr);gap:14px;padding:14px}.pp-cn-i{width:72px;height:64px}}
@media(prefers-reduced-motion:reduce){.pp-con-ring{animation:none}html.pv-js .pp-con .pp-con-svg path{animation:none!important;stroke-dasharray:7 9!important;stroke-dashoffset:0!important}.pp-cn{transition:none}.pp-cn:hover{transform:none}}

/* ===== home rhythm: tighten the dead gaps around the strip and stat band ===== */
html:has(.pp-doors) .pv-partners{padding-bottom:22px}
html:has(.pp-doors) .pv-partners .q-container{padding-top:26px}
html:has(.pp-doors) #facts{padding-top:34px;padding-bottom:58px}
html:has(.pp-doors) #systems{padding-top:64px}
"""

POP1_JS = r"""(function(){
var d=document,rm=matchMedia('(prefers-reduced-motion: reduce)').matches,fine=matchMedia('(pointer:fine) and (min-width:1025px)').matches,io='IntersectionObserver' in window;
function $$(s,r){return [].slice.call((r||d).querySelectorAll(s))}
var hd=d.querySelector('.q-header');
function hh(){if(hd)d.documentElement.style.setProperty('--pp-hdr',Math.round(hd.getBoundingClientRect().height)+'px')}
hh();addEventListener('resize',hh);addEventListener('load',hh);var hq=false;addEventListener('scroll',function(){if(!hq){hq=true;requestAnimationFrame(function(){hq=false;hh()})}},{passive:true});
function watch(els,cb,th){if(!els.length)return;if(!io||rm){els.forEach(function(e){cb(e)});return}
 var o=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting||x.boundingClientRect.top<0){o.unobserve(x.target);cb(x.target)}})},{threshold:th||.25,rootMargin:'0px 0px -6% 0px'});
 els.forEach(function(e){o.observe(e)});
 setTimeout(function(){els.forEach(function(e){var r=e.getBoundingClientRect();if(r.top<-200)cb(e)})},1400)}
/* flow and connect: arm, then light on view */
watch($$('.pp-flow'),function(e){e.classList.add('go')},.3);
watch($$('.pp-con'),function(e){e.classList.add('go')},.3);
/* proof numerals: fill, and count up */
var pr=$$('.pp-pr');
pr.forEach(function(e){var n=e.querySelector('[data-count]');if(n&&io&&!rm){n.setAttribute('data-final',n.textContent);n.textContent='0'}});
watch(pr,function(e,i){e.classList.add('in');var n=e.querySelector('[data-count]');if(!n||rm||!io){if(n&&n.getAttribute('data-final'))n.textContent=n.getAttribute('data-final');return}
 var to=+n.getAttribute('data-count'),t0=null;function st(t){if(t0===null)t0=t;var p=Math.min(1,(t-t0)/1400),v=Math.round(to*(1-Math.pow(1-p,3)));n.textContent=String(v);if(p<1)requestAnimationFrame(st);else n.textContent=n.getAttribute('data-final')}
 requestAnimationFrame(st)},.35);
/* doors: tilt */
if(fine&&!rm){$$('.pp-door').forEach(function(c){c.addEventListener('pointermove',function(e){var b=c.getBoundingClientRect(),x=(e.clientX-b.left)/b.width-.5,y=(e.clientY-b.top)/b.height-.5;c.style.setProperty('--ry',(x*7).toFixed(2)+'deg');c.style.setProperty('--rx',(-y*6).toFixed(2)+'deg')});c.addEventListener('pointerleave',function(){c.style.setProperty('--ry','0deg');c.style.setProperty('--rx','0deg')})})}
/* subnav scroll spy */
$$('.pp-subnav').forEach(function(nav){var links=$$('a',nav),tg=links.map(function(a){return d.getElementById((a.getAttribute('href')||'').replace('#',''))}),tick=false;
 function spy(){tick=false;var line=(parseInt(getComputedStyle(d.documentElement).getPropertyValue('--pp-hdr'))||81)+nav.offsetHeight+60,cur=-1;
  tg.forEach(function(t,i){if(t&&t.getBoundingClientRect().top<=line)cur=i});
  links.forEach(function(a,i){a.classList.toggle('on',i===cur);if(i===cur)a.setAttribute('aria-current','true');else a.removeAttribute('aria-current')});
  var on=links[cur],ul=on&&on.closest('ul');if(on&&ul&&ul.scrollWidth>ul.clientWidth){var l=on.offsetLeft-ul.clientWidth/2+on.offsetWidth/2;ul.scrollLeft=l}}
 addEventListener('scroll',function(){if(!tick){tick=true;requestAnimationFrame(spy)}},{passive:true});spy()});
/* panel picker */
$$('.pp-pk').forEach(function(root){var cfg;try{cfg=JSON.parse(root.getAttribute('data-pp'))}catch(e){return}
 var qs=$$('.pp-q',root),cards=$$('.pp-r',root),box=root.querySelector('.pp-rs'),live=root.querySelector('.pp-live'),st=(cfg.start||[]).slice();
 function match(){for(var i=0;i<cfg.rules.length;i++){var r=cfg.rules[i],ok=true;for(var q=0;q<st.length;q++){var w=r.when[q];if(w&&w.indexOf(st[q])<0){ok=false;break}}if(ok)return r}return cfg.rules[cfg.rules.length-1]}
 function paint(anim){var r=match(),first=null;cards.forEach(function(c){c.hidden=true});
  r.res.forEach(function(s){var c=root.querySelector('.pp-r[data-slug="'+s+'"]');if(!c)return;c.hidden=false;box.appendChild(c);var w=c.querySelector('.pp-why');if(w&&r.why&&r.why[s])w.textContent=r.why[s];if(!first)first=c});
  if(anim&&!rm){box.classList.remove('swap');void box.offsetWidth;box.classList.add('swap')}
  if(live&&first){var h=first.querySelector('h3');live.textContent=(cfg.say||'Suggested: ')+(h?h.textContent:'')}}
 qs.forEach(function(q,qi){$$('.pp-chip',q).forEach(function(b,bi){b.setAttribute('aria-pressed',bi===st[qi]?'true':'false');b.addEventListener('click',function(){st[qi]=bi;$$('.pp-chip',q).forEach(function(x,k){x.setAttribute('aria-pressed',k===bi?'true':'false')});paint(true)})})});
 paint(false)});
/* buy bar */
$$('.pp-bb').forEach(function(bar){var tg=d.getElementById(bar.getAttribute('data-target')||'pstage');if(!tg)return;
 function set(on){bar.classList.toggle('on',on)}
 if(io){new IntersectionObserver(function(es){var e=es[0];set(!e.isIntersecting&&e.boundingClientRect.top<0)},{threshold:0}).observe(tg)}else{addEventListener('scroll',function(){set(tg.getBoundingClientRect().bottom<0)},{passive:true})}});
})();"""


# ------------------------------------------------------------------ renderers

def _hd(s, ctx, cls=""):
    E = ctx["E"]
    eb = f'<div class="q-eyebrow">{E(s["eyebrow"])}</div>' if s.get("eyebrow") else ""
    h = f'<h2 class="q-h2">{E(s["heading"])}</h2>' if s.get("heading") else ""
    lead = f'<p class="q-lead">{E(s["intro"])}</p>' if s.get("intro") else ""
    return f'<div class="pp-hd{(" " + cls) if cls else ""}">{eb}{h}{lead}</div>'


def _img(ctx, path, alt="", w=1200, h=800, lazy=True):
    E = ctx["E"]
    return f'<img src="{E(ctx["rel"](path))}"{ctx["srcset"](path)} alt="{E(alt)}" width="{w}" height="{h}"{" loading=lazy" if lazy else ""} decoding="async">'


def _doors(s, ctx):
    E, L = ctx["E"], ctx["L"]
    out = []
    for i, it in enumerate(s["items"], 1):
        cover = " cover" if it.get("fit") == "cover" else ""
        bl = "".join(f"<li>{E(b)}</li>" for b in it["bullets"])
        out.append(
            f'<li><article class="pp-door"><div class="pp-door-m{cover}">{_img(ctx, it["image"], it.get("alt", ""), 1200, 800)}'
            f'<span class="pp-door-n" aria-hidden="true">{i:02d}</span><span class="pp-door-k">{E(it["kicker"])}</span></div>'
            f'<div class="pp-door-b"><h3>{E(it["title"])}</h3><ul>{bl}</ul>'
            f'<a class="pp-btn gold pp-door-go" href="{E(L(it["href"]))}">{E(it["cta"])}<span class="ar" aria-hidden="true">&rarr;</span></a></div></article></li>')
    return f'{ctx["sec_open"](s, "pp-doors")}<div class="q-container">{_hd(s, ctx)}<ul class="pp-door-grid">{"".join(out)}</ul></div></section>'


def _newsfeat(s, ctx):
    E, L = ctx["E"], ctx["L"]
    thumbs = s.get("thumbs", [])
    cards = []
    for i, it in enumerate(s["items"][:3]):
        kicker, title, body, label, href = it[0], it[1], it[2], it[3], it[4]
        th = thumbs[i] if i < len(thumbs) else None
        media = ""
        if th:
            cov = " cover" if th[1] == "cover" else ""
            media = f'<div class="pp-nc-m{cov}">{_img(ctx, th[0], "", 1200, 800)}<span class="pp-nc-k">{E(kicker)}</span></div>'
        big = i == 0
        cards.append(f'<a class="pp-nc {"big" if big else "sm"}" href="{E(L(href))}">{media}<div class="pp-nc-b"><h3>{E(title)}</h3><p>{E(body)}</p><span class="pp-nc-cue">{E(label)}</span></div></a>')
    side = "".join(cards[1:])
    eyebrow = f"<div class=q-eyebrow>{E(s['eyebrow'])}</div>" if s.get("eyebrow") else ""  # hoisted: nested quotes need Python 3.12
    intro = f"<p class=q-lead>{E(s['intro'])}</p>" if s.get("intro") else ""
    head = (f'<div class="pp-nf-head"><div>{eyebrow}<h2 class="q-h2">{E(s["heading"])}</h2></div>'
            f'{intro}</div>')
    return f'{ctx["sec_open"](s, "pp-nf-sec")}<div class="q-container">{head}<div class="pp-nf">{cards[0]}<div class="pp-nf-side">{side}</div></div></div></section>'


def _proof(s, ctx):
    E = ctx["E"]
    items = []
    for it in s["items"]:
        cnt = f' data-count="{int(it["count"])}"' if it.get("count") else ""
        t = " t" if it.get("text") else ""
        sub = f'<span class="s">{E(it["sub"])}</span>' if it.get("sub") else ""
        items.append(f'<li class="pp-pr"><span class="pp-num{t}"{cnt}>{E(it["n"])}</span><b>{E(it["label"])}</b>{sub}</li>')
    foot = f'<p class="pp-pr-foot"><span>{E(s["foot"])}</span></p>' if s.get("foot") else ""
    return f'{ctx["sec_open"](s, "pp-proof")}<div class="q-container">{_hd(s, ctx)}<ul class="pp-pr-grid">{"".join(items)}</ul>{foot}</div></section>'


def _closer(s, ctx):
    E, L = ctx["E"], ctx["L"]
    eb = f'<p class="eb">{E(s["eyebrow"])}</p>' if s.get("eyebrow") else ""
    sub = f'<p>{E(s["sub"])}</p>' if s.get("sub") else ""
    a, b = s["primary"], s.get("secondary")
    bt = f'<a class="pp-btn ink" href="{E(L(a["href"]))}">{E(a["label"])}<span class="ar" aria-hidden="true">&rarr;</span></a>'
    if b:
        bt += f'<a class="pp-btn line" href="{E(L(b["href"]))}">{E(b["label"])}</a>'
    idattr = f' id="{E(s["id"])}"' if s.get("id") else ""
    return f'<section class="q-section pp-closer"{idattr}><div class="q-container">{eb}<h2>{E(s["heading"])}</h2>{sub}<div class="bt">{bt}</div></div></section>'


def _subnav(s, ctx):
    E, L = ctx["E"], ctx["L"]
    lis = "".join(f'<li><a href="{E(h)}">{E(t)}</a></li>' for t, h in s["items"])
    cta = f'<a class="pp-btn gold pp-sn-cta" href="{E(L(s["cta"]["href"]))}">{E(s["cta"]["label"])}</a>' if s.get("cta") else ""
    return f'<nav class="pp-subnav" aria-label="On this page"><div class="q-container"><span class="pp-sn-t">{E(s["title"])}</span><ul>{lis}</ul>{cta}</div></nav>'


def _panelpick(s, ctx):
    E, L = ctx["E"], ctx["L"]
    qs = []
    for qi, q in enumerate(s["questions"], 1):
        chips = "".join(f'<button type="button" class="pp-chip" aria-pressed="false">{E(o)}</button>' for o in q["options"])
        qs.append(f'<fieldset class="pp-q"><legend><i aria-hidden="true">{qi}</i>{E(q["q"])}</legend><div class="pp-chips">{chips}</div></fieldset>')
    cards = []
    for slug, c in s["cards"].items():
        soon = '<span class="pp-soon">Coming soon, not orderable</span>' if c.get("soon") else ""
        facts = "".join(f'<li><b>{E(k)}</b>{E(v)}</li>' for k, v in c.get("facts", []))
        facts = f'<ul class="pp-facts">{facts}</ul>' if facts else ""
        light = " light" if c.get("light") else ""
        why = c.get("why", "")
        cards.append(
            f'<article class="pp-r" data-slug="{E(slug)}"><div class="pp-r-i{light}">{_img(ctx, c["image"], "", 1200, 800)}</div>'
            f'<div class="pp-r-t"><p class="pp-r-k">{E(c["kicker"])}</p><h3>{E(c["name"])}{soon}</h3><p class="pp-why">{E(why)}</p>{facts}'
            f'<div class="pp-r-go"><a class="pp-btn gold" href="{E(L(c["href"]))}">{E(c.get("cta", "View product"))}<span class="ar" aria-hidden="true">&rarr;</span></a></div></div></article>')
    also = "".join(f'<p class="pp-also">{E(a["text"])} <a href="{E(L(a["href"]))}">{E(a["label"])}</a></p>' for a in s.get("also", []))
    cfg = {"rules": s["rules"], "start": s.get("start", [0] * len(s["questions"])), "say": s.get("say", "Suggested: ")}
    data = E(json.dumps(cfg, ensure_ascii=False, separators=(",", ":")))
    note = f'<p class="pp-note">{E(s.get("note", "A starting point. A dealer confirms the design."))}</p>'
    static = f'<p class="pp-out-l pp-stat">{E(s.get("static_label", "Every option"))}</p>'
    return (f'{ctx["sec_open"](s, "pp-pick")}<div class="q-container">{_hd(s, ctx)}'
            f'<div class="pp-pk" data-pp="{data}"><div class="pp-qs">{"".join(qs)}{note}</div>'
            f'<div class="pp-out lf-dark-in"><p class="pp-out-l">{E(s.get("out_label", "Our suggestion"))}</p>{static}<div class="pp-rs" aria-hidden="false">{"".join(cards)}</div>{also}'
            f'<p class="pp-live" role="status" aria-live="polite" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)"></p></div></div></div></section>')


def _flowviz(s, ctx):
    E, L = ctx["E"], ctx["L"]
    n = len(s["nodes"])
    items = []
    for i, nd in enumerate(s["nodes"], 1):
        chips = "".join(f'<li><a href="{E(L(h))}">{E(t)}</a></li>' for t, h in nd.get("chips", []))
        chips = f"<ul>{chips}</ul>" if chips else ""
        items.append(f'<li class="pp-fn" style="--i:{i}"><span class="pp-fn-d" aria-hidden="true"></span><h3>{E(nd["label"])}</h3><span class="w">{E(nd["when"])}</span><p>{E(nd["text"])}</p>{chips}</li>')
    return (f'{ctx["sec_open"](s, "pp-flow-sec")}<div class="q-container">{_hd(s, ctx)}'
            f'<ol class="pp-flow" style="--n:{n}">{"".join(items)}<span class="pp-sig" aria-hidden="true"></span></ol></div></section>')


def _compare(s, ctx):
    E, L = ctx["E"], ctx["L"]
    cols = s["cols"]
    n = len(cols)
    head = '<div class="pp-cmp-h" role="row"><div class="pp-cmp-l" role="cell"></div>'
    for c in cols:
        tag = ""
        if c.get("here"):
            tag = '<span class="pp-cmp-tag">This product</span>'
        elif c.get("soon"):
            tag = '<span class="pp-cmp-tag soon">Coming soon</span>'
        name = E(c["name"]) if c.get("here") else f'<a href="{E(L(c["href"]))}">{E(c["name"])}</a>'
        head += (f'<div class="pp-cmp-c{" here" if c.get("here") else ""}" role="columnheader"><div class="pp-cmp-t">{tag}</div><div class="pp-cmp-img">{_img(ctx, c["image"], "", 600, 400)}</div>'
                 f'<h3>{name}</h3><span class="k">{E(c["kicker"])}</span></div>')
    head += "</div>"
    rows = ""
    for label, vals in s["rows"]:
        cells = ""
        for ci, v in enumerate(vals):
            cls = "pp-cmp-v" + (" here" if cols[ci].get("here") else "") + (" na" if v is None else "")
            cells += f'<div class="{cls}" role="cell">{E(v) if v is not None else "Not listed on its page"}</div>'
        rows += f'<div class="pp-cmp-r" role="row"><div class="pp-cmp-l" role="rowheader">{E(label)}</div>{cells}</div>'
    note = f'<p class="pp-cmp-n">{E(s["note"])}</p>' if s.get("note") else ""
    return f'{ctx["sec_open"](s, "pp-cmp-sec")}<div class="q-container">{_hd(s, ctx)}<div class="pp-cmp" style="--n:{n}" role="table" aria-label="{E(s.get("heading", "Compare"))}">{head}{rows}</div>{note}</div></section>'


def _buybar(s, ctx):
    E, L = ctx["E"], ctx["L"]
    btns = ""
    if s.get("order"):
        o = s["order"]
        btns += f'<a class="pp-btn gold" href="{E(o["href"])}" target="_blank" rel="noopener" aria-label="{E(o["label"])}"><span class="lg">{E(o["label"])}</span><span class="sh">Order</span></a>'
    if s.get("spec"):
        btns += f'<a class="pp-btn line" href="{E(L(s["spec"]["href"]))}">{E(s["spec"]["label"])}</a>'
    if s.get("ask"):
        btns += f'<a class="pp-btn line" href="{E(L(s["ask"]["href"]))}">{E(s["ask"]["label"])}</a>'
    img = _img(ctx, s["image"], "", 600, 400) if s.get("image") else ""
    return (f'<div class="pp-bb" data-target="{E(s.get("target", "pstage"))}" role="region" aria-label="{E(s["name"])} quick actions"><div class="q-container">'
            f'<div class="pp-bb-n">{img}<div><b>{E(s["name"])}</b><span>{E(s["kicker"])}</span></div></div><div class="pp-bb-a">{btns}</div></div></div>')


def _connect(s, ctx):
    E, L = ctx["E"], ctx["L"]
    hub = s["hub"]
    items = s["items"]
    n = len(items)
    # connector curves, from the hub edge (x=0) to the centre of each card row
    paths = ""
    for i in range(n):
        y = (i + .5) / n * 100
        paths += f'<path d="M0,50 C45,50 55,{y:.1f} 100,{y:.1f}"/>'
    svg = f'<svg class="pp-con-svg" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true" focusable="false">{paths}</svg>'
    cards = "".join(
        f'<li><a class="pp-cn" href="{E(L(it[2]))}"><span class="pp-cn-i">{_img(ctx, it[3], "", 600, 450)}</span>'
        f'<span><h3>{E(it[0])}</h3><p>{E(it[1])}</p><span class="go">{E(s.get("link_label", "Open"))}</span></span></a></li>' for it in items)
    light = " light" if hub.get("light") else ""
    return (f'{ctx["sec_open"](s, "pp-con-sec")}<div class="q-container">{_hd(s, ctx)}<div class="pp-con">'
            f'<div class="pp-con-hub"><span class="pp-con-ring" aria-hidden="true"></span><span class="pp-con-ring r2" aria-hidden="true"></span>'
            f'<div class="pp-con-core{light}">{_img(ctx, hub["image"], hub.get("alt", ""), 1200, 800)}<b>{E(hub["name"])}</b></div></div>'
            f'{svg}<ul class="pp-con-list">{cards}</ul></div></div></section>')


RENDER_POP1 = {"doors": _doors, "newsfeat": _newsfeat, "proofband": _proof, "closer": _closer, "subnav": _subnav, "panelpick": _panelpick,
               "flowviz": _flowviz, "compare": _compare, "buybar": _buybar, "connect": _connect}
