"""Signature modules for the preview generator: the pieces that make a buyer stop scrolling.

Each renderer is self-contained (markup, and inline JS where the module is interactive). All motion
is gated on prefers-reduced-motion and, where it uses the pointer, on (pointer:fine). Every module
degrades to readable, static HTML with no JS.

Registered into preview.py as RENDER_EXTRA2 / EXTRA_CSS2, next to preview_sections.
"""
from __future__ import annotations

import json
import math

EXTRA_CSS2 = r"""
/* ===== layered hero (dark, floating cards, pointer glow) ===== */
.pv-lh{position:relative;overflow:hidden;background:var(--chrome-bg);color:#fff;isolation:isolate}
.pv-lh .bg{position:absolute;inset:0;z-index:0}
.pv-lh .bg img{width:100%;height:100%;object-fit:cover;display:block;opacity:.55;transform:scale(1.04);animation:pv-kb 38s ease-in-out infinite alternate}
@keyframes pv-kb{from{transform:scale(1.04) translate(0,0)}to{transform:scale(1.14) translate(-1.5%,1%)}}
.pv-lh .net{position:absolute;inset:0;z-index:0;width:100%;height:100%;pointer-events:none;opacity:.9}
.pv-lh .hero3d{position:relative;height:580px;margin-left:12%;animation:pv-float 8s ease-in-out infinite}
@keyframes pv-float{0%,100%{transform:translateY(0)}50%{transform:translateY(-12px)}}
.pv-lh .hero3d model-viewer{width:100%;height:100%;display:block;--poster-color:transparent}
.pv-lh .hero3d .fallback{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;filter:drop-shadow(0 40px 60px rgba(0,0,0,.5))}
.pv-lh .hero3d model-viewer:defined + .fallback{display:none}
.pv-lh .hero3d .disc{position:absolute;left:10%;right:10%;bottom:26px;height:60px;border-radius:50%;background:radial-gradient(ellipse at center,color-mix(in srgb,var(--q-gold) 45%,transparent),transparent 70%);filter:blur(6px);z-index:-1}
.pv-lh .stack.has3d .fcard.a{right:auto;left:-32px;top:auto;bottom:-16px;width:min(310px,100%);z-index:3;padding:22px 22px 20px}
.pv-lh .lane{margin-top:26px;display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.pv-lh .lane .k{font-size:13px;letter-spacing:.12em;text-transform:uppercase;font-weight:700;color:rgba(255,255,255,.7);margin-right:6px}
.pv-lh .lane a{display:inline-flex;align-items:center;min-height:40px;padding:0 14px;border-radius:999px;border:1px solid rgba(255,255,255,.28);color:#fff;text-decoration:none;font-size:14px;font-weight:600;background:rgba(255,255,255,.06)}
.pv-lh .lane a:hover{border-color:var(--q-gold);color:var(--q-gold)}
.pv-lh .bg::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,color-mix(in srgb,var(--chrome-bg) 92%,transparent) 0%,color-mix(in srgb,var(--chrome-bg) 78%,transparent) 45%,color-mix(in srgb,var(--chrome-bg) 40%,transparent) 100%),linear-gradient(180deg,transparent 60%,var(--chrome-bg) 100%)}
.pv-lh .glow{position:absolute;inset:-20%;z-index:0;pointer-events:none;background:radial-gradient(600px circle at var(--mx,70%) var(--my,40%),color-mix(in srgb,var(--q-gold) 26%,transparent),transparent 60%);transition:opacity .4s;opacity:.9}
.pv-lh .q-container{position:relative;z-index:1;display:grid;grid-template-columns:1.1fr .9fr;gap:56px;align-items:center;padding-top:104px;padding-bottom:120px}
.pv-lh .q-eyebrow{color:var(--q-gold)}.pv-lh .q-eyebrow::before{background:var(--q-gold)}
.pv-lh .q-h1{color:#fff;margin-top:22px}.pv-lh .q-h1 em{color:var(--q-gold);font-style:normal}
.pv-lh .q-lead{color:rgba(255,255,255,.82);max-width:560px;margin-top:24px}
.pv-lh .pv-btns .q-btn{background:var(--q-gold);color:var(--cta-fg);border-color:var(--q-gold)}
.pv-lh .pv-btns .q-btn-ghost{color:#fff;border-color:rgba(255,255,255,.35)}
.pv-lh .pv-hero-stats{border-top-color:rgba(255,255,255,.18)}.pv-lh .pv-hero-stats > div{border-left-color:rgba(255,255,255,.18)}
.pv-lh .pv-hero-stats b{color:#fff}.pv-lh .pv-hero-stats span{color:rgba(255,255,255,.7)}
.pv-lh .stack{position:relative;min-height:640px;perspective:1200px}
.pv-lh .fcard{position:absolute;width:min(350px,100%);background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);border-radius:calc(var(--radius) + 8px);padding:26px 26px 22px;color:#fff;box-shadow:0 30px 80px rgba(0,0,0,.45);transform-style:preserve-3d;transition:transform .35s ease,box-shadow .35s ease;will-change:transform}
.pv-lh .fcard.a{right:0;top:0;z-index:2}.pv-lh .fcard.b{left:0;top:340px;z-index:1;background:rgba(255,255,255,.96);color:var(--fg,#111);border-color:rgba(255,255,255,.9)}
.pv-lh .fcard .k{font-size:13px;letter-spacing:.14em;text-transform:uppercase;font-weight:700;color:var(--q-gold);margin-bottom:10px}
.pv-lh .fcard.b .k{color:var(--accent-ink)}
.pv-lh .fcard .t{margin:0 0 8px;font-size:21px;line-height:1.2;font-weight:700;letter-spacing:-.01em}
.pv-lh .fcard p{margin:0;font-size:14.5px;line-height:1.55;color:rgba(255,255,255,.78)}.pv-lh .fcard.b p{color:var(--fg-muted,#555)}
.pv-lh .fcard ul{list-style:none;margin:14px 0 0;padding:0;display:grid;gap:8px}
.pv-lh .fcard li{display:flex;gap:10px;align-items:flex-start;font-size:14px;line-height:1.45}
.pv-lh .fcard li::before{content:"";flex:none;width:16px;height:16px;border-radius:50%;background:var(--q-gold);margin-top:2px;box-shadow:inset 0 0 0 4px color-mix(in srgb,var(--q-gold) 35%,#000)}
.pv-lh .fcard.b li::before{box-shadow:inset 0 0 0 4px #fff}
.pv-lh .fcard .go{display:inline-flex;align-items:center;gap:8px;margin-top:18px;min-height:44px;padding:0 18px;border-radius:999px;background:var(--q-gold);color:var(--cta-fg);font-weight:700;text-decoration:none;font-size:14.5px}
.pv-lh .fcard.b .links{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:16px}
.pv-lh .fcard.b .links a{display:flex;align-items:center;min-height:44px;padding:0 12px;border:1px solid var(--border,#ddd);border-radius:10px;text-decoration:none;color:var(--fg,#111);font-weight:600;font-size:14px;background:#fff}
.pv-lh .fcard.b .links a:hover{border-color:var(--accent-ink);color:var(--accent-ink)}
.pv-lh .note{margin-top:22px;font-size:13.5px;color:rgba(255,255,255,.62)}
@media(max-width:1024px){.pv-lh .q-container{grid-template-columns:1fr;gap:40px;padding-top:72px;padding-bottom:88px}.pv-lh .stack{min-height:0;display:grid;gap:16px;perspective:none}.pv-lh .fcard{position:static;width:100%;transform:none!important}.pv-lh .hero3d{height:380px;margin-left:0;animation:none}.pv-lh .stack.has3d .fcard.a{position:static;width:100%}}
@media(prefers-reduced-motion:reduce){.pv-lh .glow{display:none}.pv-lh .fcard{transition:none}.pv-lh .bg img,.pv-lh .hero3d{animation:none}.pv-lh .net{display:none}}

/* ===== services wheel ===== */
.pv-wheel{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:center}
.pv-wheel svg{width:100%;max-width:560px;height:auto;display:block;margin:0 auto}
.pv-wheel .seg{fill:var(--bg-alt);stroke:var(--bg);stroke-width:3;cursor:pointer;transition:fill .2s,transform .25s;transform-origin:center;transform-box:view-box}
.pv-wheel .seg:hover,.pv-wheel .seg.on,.pv-wheel a:focus-visible .seg{fill:var(--q-gold)}
.pv-wheel .lab{font:600 13px/1.2 var(--q-sans);fill:var(--fg);pointer-events:none}
.pv-wheel .seg.on ~ .lab,.pv-wheel g:hover .lab{fill:var(--cta-fg)}
.pv-wheel .hub{fill:var(--chrome-bg)}.pv-wheel .hubt{font:800 22px/1 var(--q-serif);fill:#fff;text-anchor:middle;letter-spacing:-.02em}.pv-wheel .hubs{font:600 11px/1 var(--q-sans);fill:rgba(255,255,255,.75);text-anchor:middle;letter-spacing:.12em;text-transform:uppercase}
.pv-wheel .ring{font:700 12px/1 var(--q-sans);fill:var(--fg-muted);letter-spacing:.22em}
.pv-wheel .panel{min-height:220px}
.pv-wheel .panel .q-eyebrow{margin-bottom:12px}
.pv-wheel .panel h3{margin:0 0 12px;font-size:28px;line-height:1.15;letter-spacing:-.02em}
.pv-wheel .panel p{margin:0;color:var(--fg-muted);font-size:16px;line-height:1.6}
.pv-wheel .panel .go{display:inline-flex;align-items:center;min-height:44px;margin-top:18px;font-weight:700;color:var(--accent-ink);text-decoration:none}
.pv-wheel .panel .go::after{content:"";width:22px;height:1px;background:currentColor;margin-left:10px}
.pv-wheel ol{list-style:none;margin:22px 0 0;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:6px 18px}.pv-wheel ol li:last-child:nth-child(odd){grid-column:1/-1}
.pv-wheel ol a{display:flex;align-items:center;gap:10px;min-height:44px;text-decoration:none;color:var(--fg);font-size:14.5px;font-weight:600;border-bottom:1px solid var(--border)}
.pv-wheel ol a:hover,.pv-wheel ol a.on{color:var(--accent-ink)}
.pv-wheel ol a i{width:8px;height:8px;border-radius:50%;background:var(--q-gold);flex:none}
@media(max-width:1024px){.pv-wheel{grid-template-columns:1fr;gap:28px}.pv-wheel ol{grid-template-columns:1fr}}

/* ===== process flow (the chart) ===== */
.pv-flow{position:relative}
.pv-flow .track{position:relative;display:grid;grid-template-columns:repeat(var(--n,5),1fr);gap:18px;margin-top:56px}
.pv-flow .line{position:absolute;left:calc(100% / var(--n) / 2);right:calc(100% / var(--n) / 2);top:26px;height:2px;background:var(--border);z-index:0}
.pv-flow .line i{position:absolute;inset:0;background:var(--q-gold);transform-origin:left;transform:scaleX(0);transition:transform 1.4s cubic-bezier(.2,.7,.2,1)}
.pv-flow.in .line i{transform:scaleX(1)}
.pv-flow .node{position:relative;z-index:1;text-align:center}
.pv-flow .dot{width:54px;height:54px;border-radius:50%;background:var(--bg);border:2px solid var(--border);display:grid;place-items:center;margin:0 auto;font:800 18px/1 var(--q-serif);color:var(--fg-muted);transition:background .3s,border-color .3s,color .3s,transform .3s}
.pv-flow.in .node .dot{border-color:var(--q-gold);color:var(--fg)}
.pv-flow .node[aria-expanded="true"] .dot,.pv-flow .node:hover .dot{background:var(--q-gold);color:var(--cta-fg);border-color:var(--q-gold);transform:scale(1.08)}
.pv-flow .node button{all:unset;cursor:pointer;display:block;width:100%}
.pv-flow .node h3{margin:16px 0 6px;font-size:17px;line-height:1.25;font-weight:700}
.pv-flow .node .when{font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:var(--accent-ink);font-weight:700}
.pv-flow .node p{margin:8px 0 0;font-size:14px;line-height:1.5;color:var(--fg-muted)}
.pv-flow .detail{margin-top:34px;border:1px solid var(--border);border-radius:calc(var(--radius) + 6px);background:var(--card);padding:28px 30px;display:grid;grid-template-columns:1.2fr 1fr;gap:32px;align-items:start}
.pv-flow .detail .k{font-size:13px;letter-spacing:.14em;text-transform:uppercase;font-weight:700;color:var(--accent-ink);margin-bottom:8px}
.pv-flow .detail h4{margin:0 0 8px;font-size:22px;line-height:1.2}
.pv-flow .detail p{margin:0;color:var(--fg-muted);line-height:1.6}
.pv-flow .detail ul{margin:0;padding-left:0;list-style:none;display:grid;gap:8px}
.pv-flow .detail li{display:flex;gap:10px;align-items:flex-start;font-size:15px;line-height:1.5}.pv-flow .detail li::before{content:"";width:8px;height:8px;border-radius:50%;background:var(--q-gold);flex:none;margin-top:8px}
@media(max-width:767px){.pv-flow .track{grid-template-columns:1fr;gap:0;margin-top:34px}.pv-flow .line{left:26px;right:auto;top:0;bottom:0;width:2px;height:auto}.pv-flow .line i{transform-origin:top;transform:scaleY(0)}.pv-flow.in .line i{transform:scaleY(1)}.pv-flow .node{text-align:left;padding:14px 0}.pv-flow .node button{display:grid;grid-template-columns:54px minmax(0,1fr);column-gap:16px;align-items:start}.pv-flow .node .dot{margin:0;grid-row:1/4}.pv-flow .node h3{margin-top:14px;grid-column:2}.pv-flow .node .when,.pv-flow .node p{grid-column:2}.pv-flow .detail{grid-template-columns:1fr}}
@media(prefers-reduced-motion:reduce){.pv-flow .line i{transition:none;transform:none}}

/* ===== fleet showcase ===== */
.pv-fleet{margin-top:44px;position:relative}
.pv-fleet .rail{display:grid;grid-auto-flow:column;grid-auto-columns:minmax(260px,1fr);gap:18px;overflow-x:auto;scroll-snap-type:x mandatory;padding:6px 4px 26px;scrollbar-width:thin}
.pv-fleet .rail::-webkit-scrollbar{height:6px}.pv-fleet .rail::-webkit-scrollbar-thumb{background:var(--border);border-radius:6px}
.pv-fleet .dev{scroll-snap-align:start;background:var(--card);border:1px solid var(--border);border-radius:calc(var(--radius) + 8px);padding:22px 22px 20px;text-decoration:none;color:var(--fg);display:flex;flex-direction:column;transform-style:preserve-3d;transition:transform .25s,box-shadow .25s}
.pv-fleet .dev:hover{box-shadow:0 24px 50px rgba(0,0,0,.12)}
.pv-fleet .dev .img{aspect-ratio:1;display:grid;place-items:center;position:relative}
.pv-fleet .dev .img::after{content:"";position:absolute;left:14%;right:14%;bottom:8%;height:14px;border-radius:50%;background:radial-gradient(ellipse at center,rgba(0,0,0,.18),transparent 70%)}
.pv-fleet .dev img{width:86%;height:86%;object-fit:contain;display:block;position:relative;z-index:1;filter:drop-shadow(0 18px 24px rgba(0,0,0,.14));transform:translateZ(30px)}
.pv-fleet .dev .band{font-size:13px;letter-spacing:.12em;text-transform:uppercase;font-weight:700;color:var(--accent-ink);margin-top:10px}
.pv-fleet .dev h3{margin:6px 0 4px;font-size:19px;line-height:1.25;font-weight:700}
.pv-fleet .dev .brands{font-size:13.5px;color:var(--fg-muted)}
.pv-fleet .dev ul{margin:12px 0 0;padding:0;list-style:none;display:grid;gap:6px;font-size:14px;color:var(--fg)}
.pv-fleet .dev li{display:flex;gap:8px}.pv-fleet .dev li::before{content:"";width:6px;height:6px;border-radius:50%;background:var(--q-gold);flex:none;margin-top:8px}
.pv-fleet .dev .go{margin-top:auto;padding-top:16px;font-weight:700;color:var(--accent-ink);font-size:14.5px}
.pv-fleet .arrows{position:absolute;right:0;top:-58px;display:flex;gap:8px}
.pv-fleet .arrows button{width:44px;height:44px;border-radius:50%;border:1px solid var(--border);background:var(--bg);color:var(--fg);cursor:pointer;font-size:18px;display:grid;place-items:center}
.pv-fleet .arrows button:hover{border-color:var(--accent-ink);color:var(--accent-ink)}
@media(max-width:767px){.pv-fleet .arrows{display:none}.pv-fleet .rail{grid-auto-columns:82%}}

/* ===== commitments seal ===== */
.pv-seal{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin-top:44px}
.pv-seal .item{display:grid;grid-template-columns:64px 1fr;gap:16px;align-items:start;padding:22px;border:1px solid var(--border);border-radius:calc(var(--radius) + 6px);background:var(--card)}
.pv-seal .badge{width:64px;height:64px;border-radius:50%;background:conic-gradient(var(--q-gold) 0 75%,color-mix(in srgb,var(--q-gold) 30%,transparent) 75% 100%);display:grid;place-items:center;position:relative}
.pv-seal .badge::before{content:"";position:absolute;inset:6px;border-radius:50%;background:var(--card)}
.pv-seal .badge b{position:relative;font:800 15px/1 var(--q-serif);color:var(--fg);letter-spacing:-.02em;text-align:center}
.pv-seal h3{margin:0 0 6px;font-size:16.5px;line-height:1.3;font-weight:700}
.pv-seal p{margin:0;font-size:14px;line-height:1.5;color:var(--fg-muted)}
.pv-seal .src{grid-column:1/-1;font-size:13px;color:var(--fg-muted);margin-top:4px}
@media(max-width:1024px){.pv-seal{grid-template-columns:repeat(2,1fr)}}
@media(max-width:480px){.pv-seal{grid-template-columns:1fr}}

/* ===== before / after slider ===== */
.pv-ba{margin-top:44px;position:relative;display:grid;border-radius:calc(var(--radius) + 8px);overflow:hidden;border:1px solid var(--border);background:var(--card);--pos:50%}.pv-ba .before,.pv-ba .after{grid-area:1/1}
.pv-ba .pane{padding:40px 44px 56px;min-height:400px;box-sizing:border-box}.pv-ba .before .pane{max-width:50%;padding-right:64px}.pv-ba .after .pane{padding-left:calc(50% + 44px)}
.pv-ba .after{position:relative;background:var(--chrome-bg);color:#fff;clip-path:inset(0 0 0 var(--pos));transition:clip-path .05s linear}
.pv-ba .after .pane{height:100%}
.pv-ba .k{font-size:13px;letter-spacing:.14em;text-transform:uppercase;font-weight:700;color:var(--accent-ink);margin-bottom:12px}.pv-ba .after .k{color:var(--q-gold)}
.pv-ba h3{margin:0 0 14px;font-size:clamp(22px,2.2vw,30px);line-height:1.12;letter-spacing:-.02em;overflow-wrap:anywhere}
.pv-ba ul{list-style:none;margin:0;padding:0;display:grid;gap:10px;max-width:46ch}
.pv-ba li{display:flex;gap:10px;font-size:15.5px;line-height:1.5}.pv-ba .before li::before{content:"";width:8px;height:8px;border-radius:50%;background:var(--fg-muted);flex:none;margin-top:8px;opacity:.5}
.pv-ba .after li::before{content:"";width:8px;height:8px;border-radius:50%;background:var(--q-gold);flex:none;margin-top:8px}
.pv-ba .after p,.pv-ba .before p{margin:0 0 14px;color:inherit;opacity:.8}
.pv-ba .handle{position:absolute;top:0;bottom:0;left:var(--pos);width:2px;background:var(--q-gold);transform:translateX(-1px);z-index:3;pointer-events:none}
.pv-ba .handle::after{content:"\2194";position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:48px;height:48px;border-radius:50%;background:var(--q-gold);color:var(--cta-fg);display:grid;place-items:center;font-size:20px;font-weight:700;box-shadow:0 10px 30px rgba(0,0,0,.25)}
.pv-ba input[type=range]{position:absolute;inset:0;width:100%;height:100%;margin:0;opacity:0;cursor:ew-resize;z-index:4}
.pv-ba .hint{position:absolute;bottom:14px;left:50%;transform:translateX(-50%);font-size:13px;letter-spacing:.1em;text-transform:uppercase;color:var(--fg-muted);z-index:2;pointer-events:none}
@media(max-width:767px){.pv-ba{display:block}.pv-ba .pane{padding:26px 22px;min-height:0}.pv-ba .before .pane{max-width:none;padding-right:22px}.pv-ba .after{position:static;clip-path:none}.pv-ba .after .pane{height:auto;padding-left:22px}.pv-ba .handle,.pv-ba input,.pv-ba .hint{display:none}.pv-ba h3{font-size:24px}.pv-ba li{font-size:14.5px}}

/* ===== office hotspots ===== */
.pv-hot{position:relative;margin-top:44px;border-radius:calc(var(--radius) + 8px);overflow:hidden;border:1px solid var(--border);background:var(--bg-alt)}
.pv-hot img{width:100%;height:auto;display:block}
.pv-hot .spot{position:absolute;transform:translate(-50%,-50%);width:36px;height:36px;border-radius:50%;border:0;background:var(--q-gold);color:var(--cta-fg);font:800 15px/1 var(--q-sans);cursor:pointer;box-shadow:0 0 0 6px color-mix(in srgb,var(--q-gold) 35%,transparent),0 10px 24px rgba(0,0,0,.3);display:grid;place-items:center;transition:transform .2s}
.pv-hot .spot:hover,.pv-hot .spot[aria-expanded="true"]{transform:translate(-50%,-50%) scale(1.12)}
.pv-hot .spot::after{content:"";position:absolute;inset:-6px;border-radius:50%;border:2px solid var(--q-gold);animation:pv-pulse 2.2s ease-out infinite;opacity:0}
@keyframes pv-pulse{0%{transform:scale(.8);opacity:.9}100%{transform:scale(1.9);opacity:0}}
.pv-hot .pop{position:absolute;z-index:5;width:min(300px,80vw);background:var(--bg);color:var(--fg);border:1px solid var(--border);border-radius:14px;padding:18px 18px 16px;box-shadow:0 24px 60px rgba(0,0,0,.25);transform:translate(-50%,12px)}
.pv-hot .pop[hidden]{display:none}
.pv-hot .pop .k{font-size:12px;letter-spacing:.14em;text-transform:uppercase;font-weight:700;color:var(--accent-ink)}
.pv-hot .pop h3{margin:6px 0 6px;font-size:17px;line-height:1.25}
.pv-hot .pop p{margin:0;font-size:14px;line-height:1.5;color:var(--fg-muted)}
.pv-hot .pop a{display:inline-flex;align-items:center;min-height:36px;margin-top:8px;font-weight:700;color:var(--accent-ink);text-decoration:none;font-size:14px}
.pv-hot-list{display:grid;grid-template-columns:repeat(4,1fr);gap:12px 24px;margin-top:22px;padding:0;list-style:none}
.pv-hot-list a{display:flex;align-items:center;gap:10px;min-height:44px;text-decoration:none;color:var(--fg);font-size:14.5px;font-weight:600;border-bottom:1px solid var(--border)}
.pv-hot-list a b{width:26px;height:26px;border-radius:50%;background:var(--q-gold);color:var(--cta-fg);display:grid;place-items:center;font-size:13px;flex:none}
@media(max-width:1024px){.pv-hot-list{grid-template-columns:repeat(2,1fr)}.pv-hot-list li:last-child:nth-child(odd){grid-column:1/-1}}
@media(max-width:767px){.pv-hot .spot{width:30px;height:30px;font-size:13px}.pv-hot .pop{transform:translate(-50%,10px)}.pv-hot-list{grid-template-columns:1fr}}
@media(prefers-reduced-motion:reduce){.pv-hot .spot::after{animation:none}}

/* ===== support launcher (desktop) ===== */
.pv-sl{position:fixed;left:18px;bottom:18px;z-index:88;display:none;opacity:0;transform:translateY(10px);transition:opacity .3s,transform .3s;pointer-events:none}.pv-sl.on{opacity:1;transform:none;pointer-events:auto}
@media(min-width:768px){.pv-sl{display:block}}
.pv-sl > button{display:inline-flex;align-items:center;gap:10px;min-height:48px;padding:0 18px 0 14px;border-radius:999px;border:0;background:var(--chrome-bg);color:#fff;font:600 14.5px/1 var(--q-sans);cursor:pointer;box-shadow:0 14px 34px rgba(0,0,0,.28)}
.pv-sl > button i{width:10px;height:10px;border-radius:50%;background:var(--q-gold);box-shadow:0 0 0 4px color-mix(in srgb,var(--q-gold) 30%,transparent)}
.pv-sl .drawer{position:absolute;left:0;bottom:60px;width:340px;background:var(--bg);color:var(--fg);border:1px solid var(--border);border-radius:16px;box-shadow:0 30px 80px rgba(0,0,0,.3);padding:20px 20px 16px}
.pv-sl .drawer[hidden]{display:none}
.pv-sl .drawer .k{font-size:12px;letter-spacing:.14em;text-transform:uppercase;font-weight:700;color:var(--accent-ink)}
.pv-sl .drawer h3{margin:6px 0 12px;font-size:19px;line-height:1.2}
.pv-sl .drawer .grid{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.pv-sl .drawer a{display:flex;align-items:center;min-height:46px;padding:0 12px;border:1px solid var(--border);border-radius:10px;text-decoration:none;color:var(--fg);font-weight:600;font-size:14px;background:var(--card)}
.pv-sl .drawer a:hover{border-color:var(--accent-ink);color:var(--accent-ink)}
.pv-sl .drawer .call{grid-column:1/-1;background:var(--q-gold);color:var(--cta-fg);border-color:var(--q-gold);justify-content:center}
.pv-sl .drawer p{margin:12px 0 0;font-size:13px;color:var(--fg-muted)}
.menu-open .pv-sl{display:none}

/* ===== 3D model ===== */
.pv-3d{margin-top:44px;border-radius:calc(var(--radius) + 8px);overflow:hidden;border:1px solid var(--border);background:radial-gradient(ellipse at 50% 80%,color-mix(in srgb,var(--q-gold) 14%,transparent),transparent 60%),var(--bg-alt);position:relative}
.pv-3d model-viewer{width:100%;height:520px;display:block;--poster-color:transparent}
.pv-3d .hint{position:absolute;left:18px;bottom:14px;font-size:13px;letter-spacing:.1em;text-transform:uppercase;color:var(--fg-muted);pointer-events:none}
.pv-3d img{width:100%;height:520px;object-fit:contain;display:block}.pv-3d .fallback{position:absolute;inset:0;height:100%;padding:24px;box-sizing:border-box}.pv-3d model-viewer:defined + .fallback{display:none}.pv-3d model-viewer:not(:defined){height:520px}
@media(max-width:767px){.pv-3d model-viewer,.pv-3d img,.pv-3d model-viewer:not(:defined){height:360px}.pv-3d .fallback{height:100%}}
"""


def _btns(s, ctx):
    E = ctx["E"]
    out = ""
    if s.get("primary"):
        out += f'<a class="q-btn" href="{E(ctx["L"](s["primary"]["href"]))}">{E(s["primary"]["label"])}</a>'
    if s.get("secondary"):
        out += f'<a class="q-btn-ghost" href="{E(ctx["L"](s["secondary"]["href"]))}">{E(s["secondary"]["label"])}<span style="width:22px;height:1px;background:currentColor;display:inline-block"></span></a>'
    return f'<div class="pv-btns">{out}</div>' if out else ""


def _hero_layered(s, ctx):
    """Dark hero: background plate, pointer glow, headline, proof strip, two floating cards with depth."""
    E, RAW, L = ctx["E"], ctx["RAW"], ctx["L"]
    hid = s.get("id", "hero")
    bg = f'<div class="bg"><img src="{E(ctx["rel"](s["image"]))}" alt="" width="{s.get("image_w", 2100)}" height="{s.get("image_h", 900)}" fetchpriority="high" decoding="async"></div>' if s.get("image") else '<div class="bg"></div>'
    stats = ""
    if s.get("stats"):
        cells = "".join(f'<div><b data-static>{E(v)}</b><span>{E(l)}</span></div>' for v, l in s["stats"])
        stats = f'<div class="pv-hero-stats">{cells}</div>'
    a = s.get("card_a", {})
    b = s.get("card_b", {})
    la = "".join(f"<li>{E(x)}</li>" for x in a.get("items", []))
    ca = (f'<div class="fcard a pv-depth" data-depth="1"><div class="k">{E(a.get("eyebrow", ""))}</div><p class="t">{E(a.get("title", ""))}</p><p>{E(a.get("body", ""))}</p><ul>{la}</ul>'
          f'<a class="go" href="{E(L(a.get("href", "contact.html")))}">{E(a.get("label", "Start"))}</a></div>') if a else ""
    lb = "".join(f'<a href="{E(L(h))}">{E(t)}</a>' for t, h in b.get("links", []))
    cb = (f'<div class="fcard b pv-depth" data-depth="2"><div class="k">{E(b.get("eyebrow", ""))}</div><p class="t">{E(b.get("title", ""))}</p><p>{E(b.get("body", ""))}</p><div class="links">{lb}</div></div>') if b else ""
    lane = ""
    three = ""
    if s.get("model"):
        # the device takes the stack; the customer links move under the copy as a strip
        lane = (f'<div class="lane"><span class="k">{E(b.get("eyebrow", "Already a customer?"))}</span>{lb}</div>') if b else ""
        cb = ""
        three = (f'<div class="hero3d pv-depth" data-depth="1"><div class="disc" aria-hidden="true"></div>'
                 f'<model-viewer src="{E(ctx["rel"](s["model"]))}" poster="{E(ctx["rel"](s["poster"]))}" alt="{E(s.get("model_alt", "A rotatable multifunction device"))}" camera-controls disable-zoom auto-rotate rotation-per-second="14deg" shadow-intensity="0" exposure="1.1" interaction-prompt="none" camera-orbit="35deg 78deg auto" loading="eager" reveal="auto"></model-viewer>'
                 f'<img class="fallback" src="{E(ctx["rel"](s["poster"]))}" alt="" width="1200" height="1200" decoding="async">'
                 f'<script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.5.0/model-viewer.min.js"></script></div>')
    note = f'<div class="note">{E(s["note"])}</div>' if s.get("note") else ""
    js = f"""<script>(function(){{var h=document.getElementById("{hid}");if(!h)return;var rm=matchMedia('(prefers-reduced-motion: reduce)').matches,fine=matchMedia('(pointer:fine) and (min-width:1025px)').matches;
if(!rm&&fine){{var g=h.querySelector('.glow');h.addEventListener('pointermove',function(e){{var r=h.getBoundingClientRect();h.style.setProperty('--mx',((e.clientX-r.left)/r.width*100).toFixed(1)+'%');h.style.setProperty('--my',((e.clientY-r.top)/r.height*100).toFixed(1)+'%');
h.querySelectorAll('.pv-depth').forEach(function(c){{var d=+c.getAttribute('data-depth')||1,x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;c.style.transform='translate3d('+(-x*10*d).toFixed(1)+'px,'+(-y*10*d).toFixed(1)+'px,0) rotateX('+(y*-4).toFixed(2)+'deg) rotateY('+(x*5).toFixed(2)+'deg)'}})}});
h.addEventListener('pointerleave',function(){{h.querySelectorAll('.pv-depth').forEach(function(c){{c.style.transform=''}})}})}}
var cv=h.querySelector('canvas.net');if(cv&&!rm&&cv.getContext){{var cx=cv.getContext('2d'),W,H,P=[],run=false,raf=0,col=getComputedStyle(h).getPropertyValue('--q-gold').trim()||'#65bc7b';
function size(){{var r=h.getBoundingClientRect();W=cv.width=Math.floor(r.width);H=cv.height=Math.floor(r.height);var n=W<768?22:W<1200?40:56;P=[];for(var i=0;i<n;i++)P.push({{x:Math.random()*W,y:Math.random()*H,vx:(Math.random()-.5)*.22,vy:(Math.random()-.5)*.22,r:1.2+Math.random()*1.8}})}}
function tick(){{if(!run)return;cx.clearRect(0,0,W,H);var i,j,a,b,d;for(i=0;i<P.length;i++){{a=P[i];a.x+=a.vx;a.y+=a.vy;if(a.x<0||a.x>W)a.vx*=-1;if(a.y<0||a.y>H)a.vy*=-1}}
cx.lineWidth=1;for(i=0;i<P.length;i++){{a=P[i];for(j=i+1;j<P.length;j++){{b=P[j];d=Math.hypot(a.x-b.x,a.y-b.y);if(d<150){{cx.globalAlpha=(1-d/150)*.28;cx.strokeStyle=col;cx.beginPath();cx.moveTo(a.x,a.y);cx.lineTo(b.x,b.y);cx.stroke()}}}}}}
for(i=0;i<P.length;i++){{a=P[i];cx.globalAlpha=.75;cx.fillStyle=col;cx.beginPath();cx.arc(a.x,a.y,a.r,0,6.283);cx.fill()}}cx.globalAlpha=1;raf=requestAnimationFrame(tick)}}
size();addEventListener('resize',size,{{passive:true}});
if('IntersectionObserver' in window){{new IntersectionObserver(function(es){{es.forEach(function(e){{if(e.isIntersecting&&!run){{run=true;tick()}}else if(!e.isIntersecting){{run=false;cancelAnimationFrame(raf)}}}})}}).observe(h)}}else{{run=true;tick()}}}}}})();</script>"""
    style = f' style="--chrome-bg:{E(s["bg"])};--chrome-fg:#fff;--chrome-muted:rgba(255,255,255,.72);--chrome-border:rgba(255,255,255,.14)"' if s.get("bg") else ""
    return f'''<section class="q-section pv-lh" id="{E(hid)}"{style}>{bg}<canvas class="net" aria-hidden="true"></canvas><div class="glow" aria-hidden="true"></div><div class="q-container"><div>{f'<div class="q-eyebrow">{E(s["eyebrow"])}</div>' if s.get("eyebrow") else ""}
<h1 class="q-h1">{RAW(s["heading"])}</h1><div class="q-lead">{E(s.get("subhead", ""))}</div>{_btns(s, ctx)}{lane}{note}{stats}</div>
<div class="stack{" has3d" if three else ""}">{three}{ca}{cb}</div></div>{js}</section>'''


def _wheel(s, ctx):
    """Services wheel: N segments, each a link; hover or focus swaps the panel beside it."""
    E, L = ctx["E"], ctx["L"]
    wid = s.get("id", "wheel")
    items = s["items"]  # [title, blurb, href, short]
    n = len(items)
    cx = cy = 280
    r_out, r_in = 250, 118
    segs = []
    labels = []
    for i, it in enumerate(items):
        a0 = -math.pi / 2 + i * 2 * math.pi / n + 0.012
        a1 = -math.pi / 2 + (i + 1) * 2 * math.pi / n - 0.012
        def pt(r, a):
            return f"{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}"
        large = 1 if (a1 - a0) > math.pi else 0
        d = f"M{pt(r_out, a0)} A{r_out},{r_out} 0 {large} 1 {pt(r_out, a1)} L{pt(r_in, a1)} A{r_in},{r_in} 0 {large} 0 {pt(r_in, a0)} Z"
        am = (a0 + a1) / 2
        lx, ly = cx + (r_in + r_out) / 2 * math.cos(am), cy + (r_in + r_out) / 2 * math.sin(am)
        short = it[3] if len(it) > 3 else it[0]
        words = short.split()
        lines = [" ".join(words[:2]), " ".join(words[2:])] if len(words) > 2 else [short]
        tspans = "".join(f'<tspan x="{lx:.1f}" dy="{"0" if k == 0 else "1.2em"}">{E(t)}</tspan>' for k, t in enumerate(lines) if t)
        segs.append(f'<a href="{E(L(it[2]))}" data-i="{i}" aria-label="{E(it[0])}"><g><path class="seg" d="{d}"/><text class="lab" x="{lx:.1f}" y="{ly - (6 if len(lines) > 1 else 0):.1f}" text-anchor="middle">{tspans}</text></g></a>')
        labels.append(f'<li><a href="{E(L(it[2]))}" data-i="{i}"><i></i>{E(it[0])}</a></li>')
    hub_t = E(s.get("hub", "Kelly"))
    hub_s = E(s.get("hub_sub", "one partner"))
    ring_id = f"{wid}-ring"
    svg = (f'<svg viewBox="0 0 560 560" role="group" aria-labelledby="{wid}-t"><title id="{wid}-t">{E(s.get("alt", "The service lines as a wheel"))}</title>'
           f'<defs><path id="{ring_id}" d="M{cx},{cy} m-{r_out + 18},0 a{r_out + 18},{r_out + 18} 0 1,1 {2 * (r_out + 18)},0"/></defs>'
           f'{"".join(segs)}<circle class="hub" cx="{cx}" cy="{cy}" r="{r_in - 10}"/><text class="hubt" x="{cx}" y="{cy + 2}">{hub_t}</text><text class="hubs" x="{cx}" y="{cy + 24}">{hub_s}</text>'
           f'<text class="ring"><textPath href="#{ring_id}" startOffset="50%" text-anchor="middle">{E(s.get("ring", "EVERYTHING AN OFFICE RUNS ON"))}</textPath></text></svg>')
    first = items[0]
    panel = (f'<div class="panel" data-panel><div class="q-eyebrow">{E(s.get("panel_eyebrow", "Hover a segment"))}</div><h3 data-t>{E(first[0])}</h3><p data-b>{E(first[1])}</p>'
             f'<a class="go" data-l href="{E(L(first[2]))}">{E(s.get("link_label", "See the service"))}</a><ol>{"".join(labels)}</ol></div>')
    data = json.dumps([[it[0], it[1], L(it[2])] for it in items], ensure_ascii=False)
    js = f"""<script>(function(){{var w=document.getElementById("{wid}");if(!w)return;var D={data},t=w.querySelector('[data-t]'),b=w.querySelector('[data-b]'),l=w.querySelector('[data-l]'),cur=0;
function show(i){{cur=i;t.textContent=D[i][0];b.textContent=D[i][1];l.setAttribute('href',D[i][2]);w.querySelectorAll('.seg').forEach(function(p,j){{p.classList.toggle('on',j===i)}});w.querySelectorAll('ol a').forEach(function(a,j){{a.classList.toggle('on',j===i)}})}}
w.querySelectorAll('svg a, ol a').forEach(function(a){{var i=+a.getAttribute('data-i');a.addEventListener('mouseenter',function(){{show(i)}});a.addEventListener('focus',function(){{show(i)}})}});show(0);
if(!matchMedia('(prefers-reduced-motion: reduce)').matches){{var tm=setInterval(function(){{if(w.matches(':hover'))return;show((cur+1)%D.length)}},3200);w.addEventListener('pointerenter',function(){{clearInterval(tm)}},{{once:true}})}}}})();</script>"""
    head = f'<div class="pv-center" style="margin-bottom:40px"><div class="q-eyebrow">{E(s.get("eyebrow", ""))}</div><h2 class="q-h2" style="margin-top:22px;max-width:760px">{E(s["heading"])}</h2>{f"<p class=q-lead style=max-width:640px;margin:16px_auto_0>{E(s[chr(105)+chr(110)+chr(116)+chr(114)+chr(111)])}</p>".replace("_", " ") if s.get("intro") else ""}</div>'
    return f'{ctx["sec_open"](s)} <div class="q-container" id="{E(wid)}">{head}<div class="pv-wheel">{svg}{panel}</div></div></section>'


def _flow(s, ctx):
    """Process chart: numbered nodes on a line that draws on scroll; each node opens a detail panel."""
    E = ctx["E"]
    fid = s.get("id", "flow")
    steps = s["steps"]  # {label, when, summary, title, body, receive:[...]}
    n = len(steps)
    nodes = "".join(
        f'<div class="node" role="presentation"><button type="button" data-i="{i}" aria-expanded="{"true" if i == 0 else "false"}" aria-controls="{fid}-d"><div class="dot">{i + 1}</div><h3>{E(st["label"])}</h3>'
        + (f'<div class="when">{E(st["when"])}</div>' if st.get("when") else "") + f'<p>{E(st.get("summary", ""))}</p></button></div>'
        for i, st in enumerate(steps))
    first = steps[0]
    rec = "".join(f"<li>{E(x)}</li>" for x in first.get("receive", []))
    detail = (f'<div class="detail" id="{fid}-d" role="region" aria-live="polite"><div><div class="k" data-k>{E(s.get("detail_eyebrow", "What happens"))}</div><h4 data-t>{E(first.get("title", first["label"]))}</h4><p data-b>{E(first.get("body", ""))}</p></div>'
              f'<div><div class="k">{E(s.get("receive_label", "What you receive"))}</div><ul data-r>{rec}</ul></div></div>')
    data = json.dumps([[st.get("title", st["label"]), st.get("body", ""), st.get("receive", [])] for st in steps], ensure_ascii=False)
    js = f"""<script>(function(){{var f=document.getElementById("{fid}");if(!f)return;var D={data},t=f.querySelector('[data-t]'),b=f.querySelector('[data-b]'),r=f.querySelector('[data-r]'),bs=f.querySelectorAll('.node button');
bs.forEach(function(x){{x.addEventListener('click',function(){{var i=+x.getAttribute('data-i');bs.forEach(function(y,j){{y.setAttribute('aria-expanded',j===i?'true':'false')}});t.textContent=D[i][0];b.textContent=D[i][1];r.innerHTML=D[i][2].map(function(z){{var li=document.createElement('li');li.textContent=z;return li.outerHTML}}).join('')}})}});
if('IntersectionObserver' in window){{new IntersectionObserver(function(es){{es.forEach(function(e){{if(e.isIntersecting){{f.classList.add('in')}}}})}},{{threshold:.3}}).observe(f)}}else{{f.classList.add('in')}}}})();</script>"""
    head = f'<div class="pv-center"><div class="q-eyebrow">{E(s.get("eyebrow", ""))}</div><h2 class="q-h2" style="margin-top:22px;max-width:760px">{E(s["heading"])}</h2>{f"<p class=q-lead style=max-width:640px;margin:16px_auto_0>{E(s[chr(105)+chr(110)+chr(116)+chr(114)+chr(111)])}</p>".replace("_", " ") if s.get("intro") else ""}</div>'
    return f'{ctx["sec_open"](s)} <div class="q-container pv-flow" id="{E(fid)}" style="--n:{n}">{head}<div class="track"><div class="line" aria-hidden="true"><i></i></div>{nodes}</div>{detail}</div>{js}</section>'


def _fleet(s, ctx):
    """Device showcase: a scroll-snap rail of cutout product cards."""
    E, L = ctx["E"], ctx["L"]
    fid = s.get("id", "fleet")
    cards = []
    for it in s["items"]:  # {title, band, brands, image, bullets, href}
        bl = "".join(f"<li>{E(x)}</li>" for x in it.get("bullets", []))
        cards.append(f'<a class="dev pv-tilt" href="{E(L(it["href"]))}"><div class="img"><img src="{E(ctx["rel"](it["image"]))}" alt="{E(it.get("alt", it["title"]))}" width="600" height="600" loading="lazy" decoding="async"></div><div class="band">{E(it.get("band", ""))}</div><h3>{E(it["title"])}</h3><div class="brands">{E(it.get("brands", ""))}</div><ul>{bl}</ul><span class="go">{E(it.get("label", "See the product"))}</span></a>')
    js = f"""<script>(function(){{var f=document.getElementById("{fid}");if(!f)return;var r=f.querySelector('.rail');f.querySelectorAll('.arrows button').forEach(function(b){{b.addEventListener('click',function(){{r.scrollBy({{left:(b.getAttribute('data-d')==='l'?-1:1)*(r.clientWidth*.8),behavior:'smooth'}})}})}})}})();</script>"""
    head = f'<div class="pv-split"><h2 class="q-h2">{E(s["heading"])}</h2><p>{E(s.get("intro", ""))}</p></div>'
    return f'{ctx["sec_open"](s)} <div class="q-container" id="{E(fid)}">{head}<div class="pv-fleet"><div class="arrows" aria-hidden="true"><button type="button" data-d="l" tabindex="-1">&#8592;</button><button type="button" data-d="r" tabindex="-1">&#8594;</button></div><div class="rail">{"".join(cards)}</div></div></div>{js}</section>'


def _seal(s, ctx):
    """Commitments strip: badge marks with the things every customer gets. Sourced lines only."""
    E = ctx["E"]
    items = "".join(f'<div class="item"><div class="badge" aria-hidden="true"><b>{E(m)}</b></div><div><h3>{E(t)}</h3><p>{E(d)}</p></div></div>' for m, t, d in s["items"])
    src = f'<p class="src">{E(s["source"])}</p>' if s.get("source") else ""
    head = f'<div class="pv-center"><div class="q-eyebrow">{E(s.get("eyebrow", ""))}</div><h2 class="q-h2" style="margin-top:22px;max-width:760px">{E(s["heading"])}</h2>{f"<p class=q-lead style=max-width:640px;margin:16px_auto_0>{E(s[chr(105)+chr(110)+chr(116)+chr(114)+chr(111)])}</p>".replace("_", " ") if s.get("intro") else ""}</div>'
    return f'{ctx["sec_open"](s)} <div class="q-container">{head}<div class="pv-seal">{items}{src}</div></div></section>'


def _beforeafter(s, ctx):
    """Draggable comparison of two states, driven by a range input for keyboard and touch."""
    E = ctx["E"]
    bid = s.get("id", "ba")
    b, a = s["before"], s["after"]
    lb = "".join(f"<li>{E(x)}</li>" for x in b.get("items", []))
    la = "".join(f"<li>{E(x)}</li>" for x in a.get("items", []))
    js = f"""<script>(function(){{var w=document.getElementById("{bid}");if(!w)return;var r=w.querySelector('input');r.addEventListener('input',function(){{w.style.setProperty('--pos',r.value+'%')}})}})();</script>"""
    head = f'<div class="pv-center"><div class="q-eyebrow">{E(s.get("eyebrow", ""))}</div><h2 class="q-h2" style="margin-top:22px;max-width:760px">{E(s["heading"])}</h2></div>'
    return (f'{ctx["sec_open"](s)} <div class="q-container">{head}<div class="pv-ba" id="{E(bid)}">'
            f'<div class="pane before"><div class="k">{E(b.get("eyebrow", "Before"))}</div><h3>{E(b["title"])}</h3><p>{E(b.get("body", ""))}</p><ul>{lb}</ul></div>'
            f'<div class="after"><div class="pane"><div class="k">{E(a.get("eyebrow", "After"))}</div><h3>{E(a["title"])}</h3><p>{E(a.get("body", ""))}</p><ul>{la}</ul></div></div>'
            f'<div class="handle" aria-hidden="true"></div><div class="hint">{E(s.get("hint", "Drag to compare"))}</div>'
            f'<input type="range" min="8" max="92" value="50" aria-label="{E(s.get("range_label", "Compare before and after"))}"></div></div>{js}</section>')


def _hotspots(s, ctx):
    """One image, N numbered hotspots, each opening a popover. A list of the same links below for touch and AT."""
    E, L = ctx["E"], ctx["L"]
    hid = s.get("id", "hot")
    spots, pops, lst = [], [], []
    for i, it in enumerate(s["items"], 1):  # {x, y, title, body, href, k}
        spots.append(f'<button type="button" class="spot" style="left:{it["x"]}%;top:{it["y"]}%" aria-expanded="false" aria-controls="{hid}-p{i}" aria-label="{E(it["title"])}">{i}</button>')
        pops.append(f'<div class="pop" id="{hid}-p{i}" hidden style="left:{it["x"]}%;top:{it["y"]}%"><div class="k">{E(it.get("k", ""))}</div><h3>{E(it["title"])}</h3><p>{E(it["body"])}</p><a href="{E(L(it["href"]))}">{E(it.get("label", "See it"))}</a></div>')
        lst.append(f'<li><a href="{E(L(it["href"]))}"><b>{i}</b>{E(it["title"])}</a></li>')
    js = f"""<script>(function(){{var h=document.getElementById("{hid}");if(!h)return;var bs=h.querySelectorAll('.spot');function closeAll(){{bs.forEach(function(b){{b.setAttribute('aria-expanded','false');document.getElementById(b.getAttribute('aria-controls')).hidden=true}})}}
bs.forEach(function(b){{b.addEventListener('click',function(e){{e.stopPropagation();var open=b.getAttribute('aria-expanded')==='true';closeAll();if(!open){{b.setAttribute('aria-expanded','true');var p=document.getElementById(b.getAttribute('aria-controls'));p.hidden=false;var r=h.getBoundingClientRect(),pr=p.getBoundingClientRect();if(pr.right>r.right-8)p.style.transform='translate(-100%,12px)';if(pr.left<r.left+8)p.style.transform='translate(0,12px)'}}}})}});
document.addEventListener('click',closeAll);document.addEventListener('keydown',function(e){{if(e.key==='Escape')closeAll()}})}})();</script>"""
    head = f'<div class="pv-center"><div class="q-eyebrow">{E(s.get("eyebrow", ""))}</div><h2 class="q-h2" style="margin-top:22px;max-width:760px">{E(s["heading"])}</h2>{f"<p class=q-lead style=max-width:640px;margin:16px_auto_0>{E(s[chr(105)+chr(110)+chr(116)+chr(114)+chr(111)])}</p>".replace("_", " ") if s.get("intro") else ""}</div>'
    return (f'{ctx["sec_open"](s)} <div class="q-container">{head}<div class="pv-hot" id="{E(hid)}"><img src="{E(ctx["rel"](s["image"]))}" alt="{E(s.get("alt", ""))}" width="{s.get("image_w", 1600)}" height="{s.get("image_h", 900)}" loading="lazy" decoding="async">{"".join(spots)}{"".join(pops)}</div>'
            f'<ol class="pv-hot-list">{"".join(lst)}</ol></div>{js}</section>')


def _launcher(s, ctx):
    """Floating 'already a customer' launcher with the fast-lane links. Desktop only; the sticky bar covers phones."""
    E, L = ctx["E"], ctx["L"]
    links = "".join(f'<a href="{E(L(h))}">{E(t)}</a>' for t, h in s.get("links", []))
    call = f'<a class="call" href="{E(ctx["brand"].get("phone_href", "#"))}">Call {E(ctx["brand"].get("phone", ""))}</a>' if ctx["brand"].get("phone") else ""
    js = """<script>(function(){var l=document.querySelector('.pv-sl');if(!l)return;var b=l.querySelector('button'),d=l.querySelector('.drawer');var sc=function(){l.classList.toggle('on',scrollY>560)};addEventListener('scroll',sc,{passive:true});sc();b.addEventListener('click',function(){var o=!d.hidden;d.hidden=o;b.setAttribute('aria-expanded',o?'false':'true')});document.addEventListener('keydown',function(e){if(e.key==='Escape'){d.hidden=true;b.setAttribute('aria-expanded','false')}})})();</script>"""
    return (f'<div class="pv-sl"><button type="button" aria-expanded="false" aria-controls="pv-sl-d"><i aria-hidden="true"></i>{E(s.get("label", "Already a customer?"))}</button>'
            f'<div class="drawer" id="pv-sl-d" hidden><div class="k">{E(s.get("eyebrow", "The fast lane"))}</div><h3>{E(s.get("title", "What do you need?"))}</h3><div class="grid">{links}{call}</div><p>{E(s.get("note", ""))}</p></div></div>{js}')


def _model3d(s, ctx):
    """Interactive 3D model via model-viewer, with a poster image fallback when the GLB is absent."""
    E = ctx["E"]
    head = f'<div class="pv-split"><h2 class="q-h2">{E(s["heading"])}</h2><p>{E(s.get("intro", ""))}</p></div>'
    if s.get("model"):
        mv = (f'<model-viewer src="{E(ctx["rel"](s["model"]))}" poster="{E(ctx["rel"](s["poster"]))}" alt="{E(s.get("alt", "3D model"))}" camera-controls auto-rotate rotation-per-second="18deg" shadow-intensity="1" exposure="1.05" interaction-prompt="none" loading="lazy" reveal="auto"></model-viewer>'
              f'<img class="fallback" src="{E(ctx["rel"](s["poster"]))}" alt="" width="1200" height="1200" loading="lazy">'
              f'<script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.5.0/model-viewer.min.js"></script>')
    else:
        mv = f'<img src="{E(ctx["rel"](s["poster"]))}" alt="{E(s.get("alt", ""))}" width="1200" height="1200" loading="lazy">'
    return f'{ctx["sec_open"](s)} <div class="q-container">{head}<div class="pv-3d">{mv}<div class="hint">{E(s.get("hint", "Drag to rotate"))}</div></div></div></section>'


RENDER_EXTRA2 = {
    "hero-layered": _hero_layered, "wheel": _wheel, "flow": _flow, "fleet": _fleet, "seal": _seal,
    "beforeafter": _beforeafter, "hotspots": _hotspots, "model3d": _model3d,
}
