"""Creative-director lift for the home, system and product pages: stage sections ("dark": true), product stage,
designed spec grid, image-led cards, and the per-direction home heroes (grid for Clean, front page for Press).

Everything reads the theme variables the re-skin writes (--bg, --bg-alt, --fg, --fg-muted, --border, --card,
--q-gold, --accent-ink, --cta-fg, --radius), so Showcase, Clean and Press pick it up. A section with
"dark": true becomes a navy stage by redefining those variables locally, so every existing renderer
(cards, faq, leadform, detail, showcase3d, network) flips with it. Motion is gated on prefers-reduced-motion
and (pointer:fine). Registered in preview.py as RENDER_EXTRA4 and EXTRA_CSS4.
"""
from __future__ import annotations

import re

EXTRA_CSS4 = r"""
/* ===== stage sections: navy ground, accent glow, hairline top ===== */
.lf-dark{--bg:#0b1220;--bg-alt:#121c30;--fg:#f4f6fb;--fg-muted:#b7c0d3;--border:rgba(255,255,255,.14);--card:rgba(255,255,255,.055);--accent-ink:#ffd23d;--q-gold:#ffd23d;--q-gold-bright:#ffe27a;--cta-fg:#111;
 position:relative;isolation:isolate;color:var(--fg);overflow:hidden;
 background:radial-gradient(900px 440px at 88% -8%,rgba(255,210,61,.16),transparent 62%),radial-gradient(700px 380px at 4% 108%,rgba(80,120,255,.14),transparent 60%),linear-gradient(165deg,#121c30,#0b1220 64%)}
.lf-dark::before{content:"";position:absolute;left:0;right:0;top:0;height:1px;background:linear-gradient(90deg,transparent,rgba(255,210,61,.7),transparent);z-index:1}
.lf-dark::after{content:"";position:absolute;inset:0;z-index:-1;opacity:.5;pointer-events:none;background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px);background-size:56px 56px;mask-image:radial-gradient(ellipse at 50% 30%,#000,transparent 75%);-webkit-mask-image:radial-gradient(ellipse at 50% 30%,#000,transparent 75%)}
.lf-dark .q-h2,.lf-dark .q-h1{color:#fff}
.lf-dark .q-btn-ghost{color:#fff}
.lf-dark .q-card{background:linear-gradient(180deg,rgba(255,255,255,.08),rgba(255,255,255,.03));border-color:rgba(255,255,255,.14);box-shadow:0 24px 50px -30px rgba(0,0,0,.7)}
.lf-dark .q-card:hover{border-color:rgba(255,210,61,.55);box-shadow:0 30px 60px -28px rgba(0,0,0,.8),0 0 0 1px rgba(255,210,61,.25)}
.lf-dark .pv-faq details{border-color:rgba(255,255,255,.14)}
.lf-dark .q-form{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.14);border-radius:calc(var(--radius) + 8px);padding:30px;box-shadow:0 30px 70px -40px rgba(0,0,0,.8)}
.lf-dark .q-form input[type=text],.lf-dark .q-form input[type=email],.lf-dark .q-form input[type=tel],.lf-dark .q-form select{background:rgba(255,255,255,.07);border-color:rgba(255,255,255,.2);color:#fff}
.lf-dark .q-form label{color:var(--fg-muted)}
.lf-dark .pv-form-note,.lf-dark .pv-contact p{color:var(--fg-muted)}
.lf-dark .pv-contact a[href^=tel]{color:#fff}

/* ===== polish on the light sections: depth, lift, tint ===== */
.q-section.q-bg-alt:not(.lf-dark){background:linear-gradient(180deg,var(--bg-alt),color-mix(in srgb,var(--bg-alt) 62%,var(--bg)))}
.q-section:not(.lf-dark) .pv-grid .q-card{box-shadow:0 1px 2px rgba(17,24,39,.05),0 18px 34px -24px rgba(17,24,39,.28);transition:transform .35s cubic-bezier(.2,.7,.2,1),box-shadow .35s,border-color .35s}
.q-section:not(.lf-dark) .pv-grid .q-card:hover{transform:translateY(-6px);box-shadow:0 2px 4px rgba(17,24,39,.06),0 34px 54px -26px rgba(17,24,39,.38);border-color:var(--q-gold)}
.pv-res a{transition:transform .35s cubic-bezier(.2,.7,.2,1),box-shadow .35s,border-color .35s}
.pv-res a:hover{transform:translateY(-5px);box-shadow:0 30px 50px -26px rgba(17,24,39,.34);border-color:var(--q-gold)}
.lf-dark .pv-res a{background:linear-gradient(180deg,rgba(255,255,255,.08),rgba(255,255,255,.03));border:1px solid rgba(255,255,255,.14)}

/* numbered feature cards: big outlined numeral, accent rule that draws on hover */
.lf-num .pv-grid{counter-reset:lfn}
.lf-num .q-card{counter-increment:lfn;position:relative;overflow:hidden;padding:36px 30px 32px}
.lf-num .q-card::before{content:counter(lfn,decimal-leading-zero);position:absolute;right:18px;top:6px;font-family:var(--q-display,var(--q-sans));font-weight:800;font-size:76px;line-height:1;letter-spacing:-.04em;color:transparent;-webkit-text-stroke:1.5px color-mix(in srgb,var(--q-gold) 70%,transparent);opacity:.55;pointer-events:none}
.lf-num .q-card::after{content:"";position:absolute;left:0;bottom:0;height:3px;width:34%;background:linear-gradient(90deg,var(--q-gold),transparent);transition:width .5s cubic-bezier(.2,.7,.2,1)}
.lf-num .q-card:hover::after{width:100%}
.lf-num .q-card h3{font-size:22px;margin:0 0 12px;max-width:80%}
.lf-docs .pv-grid{gap:14px}
.lf-docs .q-card{display:flex;flex-direction:column;justify-content:center;padding:20px 22px 20px 74px;position:relative;min-height:84px}
.lf-docs .q-card::before{content:"";position:absolute;left:22px;top:50%;width:30px;height:38px;margin-top:-19px;border:2px solid var(--q-gold);border-radius:4px 10px 4px 4px;background:linear-gradient(var(--q-gold),var(--q-gold)) 6px 14px/14px 2px no-repeat,linear-gradient(var(--q-gold),var(--q-gold)) 6px 21px/14px 2px no-repeat,linear-gradient(var(--q-gold),var(--q-gold)) 6px 28px/9px 2px no-repeat}
.lf-docs .q-card h3{font-size:18px;margin:0 0 4px}.lf-docs .q-card p{margin:0;font-size:14.5px}

/* ===== product stage hero ===== */
.lf-ps{padding:0!important}
.lf-ps-wrap{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.08fr);gap:40px;align-items:center;padding-top:56px;padding-bottom:72px}
.lf-ps .q-h1{font-size:clamp(38px,4.4vw,66px);line-height:1.03;margin-top:20px}
.lf-ps .q-h1 em{color:var(--q-gold);font-style:normal}
.lf-ps .q-lead{margin-top:22px;max-width:520px;font-size:19px}
.lf-chips{display:flex;flex-wrap:wrap;gap:10px;margin-top:30px}
.lf-chip{display:inline-flex;flex-direction:column;gap:2px;padding:10px 16px 11px;border:1px solid rgba(255,255,255,.2);border-radius:14px;background:linear-gradient(180deg,rgba(255,255,255,.1),rgba(255,255,255,.03));backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px);min-width:104px}
.lf-chip span{font-size:13px;letter-spacing:.1em;text-transform:uppercase;color:var(--fg-muted);font-weight:600}
.lf-chip b{font-size:18px;line-height:1.2;color:var(--q-gold);font-weight:700}
.lf-ps-stage{position:relative;min-height:440px;display:grid;place-items:center;perspective:1100px}
.lf-ps-halo{position:absolute;inset:0;border-radius:50%;background:radial-gradient(circle,rgba(255,210,61,.26),rgba(255,210,61,0) 62%);filter:blur(4px)}
.lf-ps-ring{position:absolute;left:50%;top:50%;width:min(94%,520px);aspect-ratio:1;transform:translate(-50%,-50%);border-radius:50%;border:1px solid rgba(255,255,255,.14)}
.lf-ps-ring.r2{width:min(72%,400px);border:1px dashed rgba(255,210,61,.4);animation:lf-spin 60s linear infinite}
.lf-ps-disc{position:absolute;left:14%;right:14%;bottom:8%;height:40px;border-radius:50%;background:radial-gradient(ellipse at center,rgba(255,210,61,.6),transparent 70%);filter:blur(10px)}
.lf-ps-tilt{position:relative;z-index:2;display:grid;place-items:center;width:100%;transform-style:preserve-3d;transition:transform .25s ease-out}
.lf-ps-img{display:block;max-width:88%;max-height:420px;width:auto;height:auto;filter:drop-shadow(0 44px 44px rgba(0,0,0,.55));animation:lf-float 7s ease-in-out infinite}
.lf-ps-stage.k-light .lf-ps-img,.lf-ps-stage.k-dark .lf-ps-img{border-radius:22px;filter:none;box-shadow:0 50px 90px -30px rgba(0,0,0,.75),0 0 0 1px rgba(255,255,255,.16)}
.lf-ps-stage.k-light .lf-ps-img{background:#fff;padding:20px;box-sizing:border-box}
.lf-ps-tag{position:absolute;z-index:3;right:2%;top:6%;padding:9px 16px;border-radius:999px;background:var(--q-gold);color:#111;font-size:13px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;box-shadow:0 14px 30px -12px rgba(255,210,61,.6)}
@keyframes lf-float{0%,100%{transform:translateY(0) rotate(-.6deg)}50%{transform:translateY(-14px) rotate(.8deg)}}
@keyframes lf-spin{to{transform:translate(-50%,-50%) rotate(360deg)}}
@media(max-width:1024px){.lf-ps-wrap{grid-template-columns:1fr;gap:20px;padding-top:36px;padding-bottom:56px}.lf-ps-stage{min-height:320px;order:-1}.lf-ps-img{max-height:300px}}
@media(prefers-reduced-motion:reduce){.lf-ps-img,.lf-ps-ring.r2,.pv-lh .hero3d.lf-float::after,.pv-lh .hero3d.lf-float img.fallback{animation:none}.lf-ps-tilt{transition:none}}

.lf-fine{margin:14px 0 0;font-size:14.5px;color:var(--fg-muted);max-width:520px}.lf-fine a{color:var(--q-gold);text-decoration:underline;text-underline-offset:3px}
.lf-badge{display:inline-block;margin-top:20px;padding:9px 16px;border-radius:999px;background:var(--q-gold);color:#111;font-size:13px;font-weight:800;letter-spacing:.1em;text-transform:uppercase}
.lf-ps .pv-btns{flex-wrap:wrap;gap:10px 14px}.lf-ps .pv-btns .q-btn-ghost{border:1px solid rgba(255,255,255,.35);border-radius:6px;padding:0 18px;min-height:48px}.lf-ps .pv-btns .q-btn-ghost:hover{border-color:var(--q-gold);color:var(--q-gold)}
.lf-doclist{list-style:none;margin:0 auto;padding:0;max-width:860px;border-top:1px solid var(--border)}
.lf-doclist li{display:grid;grid-template-columns:34px minmax(0,1fr) auto;gap:16px;align-items:center;padding:16px 4px;border-bottom:1px solid var(--border)}
.lf-doclist .ic{width:22px;height:28px;border:2px solid var(--fg-muted);border-radius:3px 8px 3px 3px;opacity:.7}
.lf-doclist b{display:block;font-size:17px;color:var(--fg)}.lf-doclist span{font-size:14.5px;color:var(--fg-muted)}
.lf-doclist em{font-style:normal;font-size:13px;color:var(--fg-muted);border:1px dashed var(--border);border-radius:999px;padding:5px 12px;white-space:nowrap}
@media(max-width:640px){.lf-doclist li{grid-template-columns:30px minmax(0,1fr)}.lf-doclist em{grid-column:2;justify-self:start}}
/* ===== designed spec grid ===== */
.lf-spec{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:16px;margin:0}
.lf-spec-c{position:relative;overflow:hidden;padding:30px 26px 26px;border-radius:16px;background:var(--card);border:1px solid var(--border);box-shadow:0 22px 44px -32px rgba(17,24,39,.35);transition:transform .35s cubic-bezier(.2,.7,.2,1),box-shadow .35s,border-color .35s}
.lf-spec-c::before{content:"";position:absolute;left:0;top:0;right:0;height:3px;background:linear-gradient(90deg,var(--q-gold),transparent 80%)}
.lf-spec-c:hover{transform:translateY(-4px);border-color:var(--q-gold)}
.lf-spec-c dt{font-size:13px;letter-spacing:.12em;text-transform:uppercase;font-weight:700;color:var(--fg-muted);margin:0 0 14px}
.lf-spec-c dd{margin:0;font-weight:700;color:var(--fg);font-size:18px;line-height:1.35}
.lf-spec-c.num dd{font-family:var(--q-display,var(--q-sans));font-size:clamp(34px,3.4vw,50px);font-weight:800;letter-spacing:-.03em;line-height:1.05;color:var(--accent-ink)}
.lf-dark .lf-spec-c{background:linear-gradient(180deg,rgba(255,255,255,.09),rgba(255,255,255,.03))}
.lf-dark .lf-spec-c:hover{box-shadow:0 0 0 1px rgba(255,210,61,.3),0 30px 60px -30px rgba(0,0,0,.8)}
.lf-sec-head{text-align:center;margin-bottom:44px}
.lf-sec-head .q-h2{margin:22px auto 0;max-width:760px}
.lf-sec-head .q-lead{margin:16px auto 0;max-width:640px}

/* ===== image-led cards ===== */
.lf-wk{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px;list-style:none;margin:0;padding:0}
.lf-wk a{display:flex;flex-direction:column;height:100%;border-radius:20px;overflow:hidden;background:var(--card);border:1px solid var(--border);color:inherit;text-decoration:none;box-shadow:0 2px 4px rgba(17,24,39,.05),0 26px 44px -30px rgba(17,24,39,.4);transition:transform .4s cubic-bezier(.2,.7,.2,1),box-shadow .4s,border-color .4s}
.lf-wk a:hover{transform:translateY(-8px);border-color:var(--q-gold);box-shadow:0 4px 8px rgba(17,24,39,.06),0 44px 64px -30px rgba(17,24,39,.5)}
.lf-wk-img{position:relative;aspect-ratio:16/11;display:grid;place-items:center;overflow:hidden;background:radial-gradient(circle at 50% 38%,color-mix(in srgb,var(--q-gold) 26%,#fff),var(--bg-alt) 78%)}
.lf-wk-img img{max-width:78%;max-height:82%;width:auto;height:auto;object-fit:contain;filter:drop-shadow(0 22px 22px rgba(0,0,0,.28));transition:transform .6s cubic-bezier(.2,.7,.2,1)}
.lf-wk-img.cover{background:#0b1220}.lf-wk-img.cover img{position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:cover;filter:none}
.lf-wk-img.cover::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 45%,rgba(11,18,32,.6))}
.lf-wk-img img{mix-blend-mode:multiply}.lf-dark .lf-wk-img img{mix-blend-mode:normal}
.lf-wk a:hover .lf-wk-img img{transform:scale(1.07)}
.lf-wk-b{padding:22px 24px 26px;display:flex;flex-direction:column;gap:8px;flex:1}
.lf-wk-b h3{margin:0;font-size:22px;line-height:1.2;color:var(--fg)}
.lf-wk-b p{margin:0;font-size:15.5px;line-height:1.55;color:var(--fg-muted)}
.lf-wk-go{margin-top:auto;padding-top:10px;font-weight:700;font-size:14.5px;color:var(--accent-ink)}
.lf-wk-go::after{content:"\2192";margin-left:8px;display:inline-block;transition:transform .3s}
.lf-wk a:hover .lf-wk-go::after{transform:translateX(6px)}
.lf-dark .lf-wk a{background:linear-gradient(180deg,rgba(255,255,255,.08),rgba(255,255,255,.03))}
.lf-dark .lf-wk-img{background:radial-gradient(circle at 50% 38%,rgba(255,210,61,.22),rgba(255,255,255,.03) 72%)}
@media(max-width:1024px){.lf-wk{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:640px){.lf-wk{grid-template-columns:minmax(0,1fr)}}

/* ===== system page hero-layered: floating product ===== */
.pv-lh .hero3d.lf-float{height:auto;min-height:420px;margin-left:0;display:grid;place-items:center;animation:none}
.pv-lh .hero3d.lf-float img.fallback{position:relative;inset:auto;max-width:86%;max-height:430px;width:auto;height:auto;animation:lf-float 7s ease-in-out infinite;filter:drop-shadow(0 44px 44px rgba(0,0,0,.6))}
.pv-lh .hero3d.lf-float::before{content:"";position:absolute;inset:6% 4%;border-radius:50%;background:radial-gradient(circle,rgba(255,210,61,.28),transparent 64%)}
.pv-lh .hero3d.lf-float::after{content:"";position:absolute;left:50%;top:50%;width:min(92%,500px);aspect-ratio:1;transform:translate(-50%,-50%);border-radius:50%;border:1px dashed rgba(255,210,61,.35);animation:lf-spin 70s linear infinite}
.pv-lh .stack.has3d{min-height:0}
.pv-lh.lf-tight .q-container{gap:40px}
.pv-lh.lf-tight .stack{min-height:0}
.pv-lh.lf-tight .stack.has3d{display:flex;flex-direction:column;gap:14px;perspective:none}
.pv-lh.lf-tight .q-h1{font-size:clamp(38px,4.3vw,62px);line-height:1.04}
.pv-lh.lf-tight .q-lead{margin-top:18px;font-size:18px}
.pv-lh.lf-tight .q-container{padding-top:44px;padding-bottom:52px;align-items:center}
.pv-lh.lf-tight .hero3d.lf-float{min-height:330px;margin:0}
.pv-lh.lf-tight .hero3d.lf-float img.fallback{max-width:100%;max-height:330px}
.pv-lh.lf-tight .stack.has3d .fcard.a{position:static;left:auto;right:auto;bottom:auto;width:100%;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.2fr);column-gap:22px;align-items:start;padding:20px 22px;transform:none!important}
.pv-lh.lf-tight .fcard.a .k,.pv-lh.lf-tight .fcard.a .t{grid-column:1}
.pv-lh.lf-tight .fcard.a > p:not(.t){display:none}
.pv-lh.lf-tight .fcard.a ul{grid-column:2;grid-row:1 / span 3;margin:0}
.pv-lh.lf-tight .fcard.a .go{grid-column:1;justify-self:start;margin-top:6px}
.pv-lh.lf-tight .pv-hero-stats{margin-top:30px}
@media(max-width:1024px){.pv-lh.lf-tight .stack.has3d .fcard.a{display:block}.pv-lh.lf-tight .fcard.a > p:not(.t){display:block}.pv-lh.lf-tight .hero3d.lf-float{min-height:300px}.pv-lh .hero3d.lf-float{min-height:300px}.pv-lh .hero3d.lf-float img.fallback{max-height:290px}.pv-lh.lf-tight .stack{min-height:0}}

/* ===== home hero, Clean: product grid and a building finder ===== */
.lf-hg{padding:0!important;background:radial-gradient(900px 480px at 92% 0%,color-mix(in srgb,var(--q-gold) 24%,transparent),transparent 62%),linear-gradient(180deg,var(--bg),var(--bg-alt))}
.lf-hg-wrap{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.12fr);gap:56px;align-items:center;padding-top:56px;padding-bottom:64px}
.lf-hg .q-h1{font-size:clamp(40px,4.6vw,68px);line-height:1.02;margin-top:20px}
.lf-hg .q-h1 em{color:var(--accent-ink);font-style:normal}
.lf-hg .q-lead{margin-top:20px;max-width:540px;font-size:19px}
.lf-find{margin-top:30px}
.lf-find > span{display:block;font-size:13px;letter-spacing:.14em;text-transform:uppercase;font-weight:700;color:var(--fg-muted);margin-bottom:10px}
.lf-find div{display:flex;flex-wrap:wrap;gap:8px}
.lf-find a{display:inline-flex;align-items:center;min-height:44px;padding:0 16px;border-radius:999px;border:1px solid var(--border);background:var(--card);color:var(--fg);font-weight:600;font-size:15px;transition:transform .25s,border-color .25s,background .25s,box-shadow .25s}
.lf-find a:hover{border-color:var(--q-gold);background:var(--q-gold);color:var(--cta-fg);transform:translateY(-2px);box-shadow:0 12px 24px -14px rgba(17,24,39,.4)}
.lf-hg-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));grid-template-rows:repeat(2,minmax(0,1fr));gap:16px}
.lf-tile{position:relative;display:flex;flex-direction:column;justify-content:flex-end;min-height:220px;border-radius:20px;overflow:hidden;background:var(--card);border:1px solid var(--border);color:inherit;text-decoration:none;box-shadow:0 2px 4px rgba(17,24,39,.05),0 26px 44px -30px rgba(17,24,39,.4);transition:transform .4s cubic-bezier(.2,.7,.2,1),box-shadow .4s,border-color .4s}
.lf-tile:first-child{grid-row:span 2;min-height:456px;background:linear-gradient(165deg,#121c30,#0b1220);color:#fff;border-color:transparent}
.lf-tile:hover{transform:translateY(-6px);border-color:var(--q-gold);box-shadow:0 40px 60px -30px rgba(17,24,39,.5)}
.lf-tile img{position:absolute;left:50%;top:8%;width:78%;height:60%;object-fit:contain;transform:translateX(-50%);filter:drop-shadow(0 20px 20px rgba(0,0,0,.25));transition:transform .6s cubic-bezier(.2,.7,.2,1)}
.lf-tile:first-child img{top:4%;height:68%;width:100%}
.lf-tile:hover img{transform:translateX(-50%) scale(1.07)}
.lf-tile .t{position:relative;padding:16px 18px 18px;background:linear-gradient(180deg,transparent,color-mix(in srgb,var(--card) 92%,transparent) 40%)}
.lf-tile:first-child .t{background:linear-gradient(180deg,transparent,rgba(11,18,32,.92) 45%)}
.lf-tile .k{display:block;font-size:13px;letter-spacing:.12em;text-transform:uppercase;font-weight:700;color:var(--accent-ink)}
.lf-tile:first-child .k{color:#ffd23d}
.lf-tile b{display:block;font-size:19px;line-height:1.2;margin-top:3px}
@media(max-width:1024px){.lf-hg-wrap{grid-template-columns:1fr;gap:32px;padding-top:40px}.lf-tile:first-child{min-height:300px}}
@media(max-width:640px){.lf-hg-grid{grid-template-columns:repeat(2,minmax(0,1fr));grid-template-rows:none}.lf-tile{min-height:190px}.lf-tile:first-child{grid-column:span 2;grid-row:auto;min-height:260px}}

/* ===== home hero, Press: a front page ===== */
.lf-hp{padding:0!important}
.lf-hp-wrap{padding-top:28px;padding-bottom:56px}
.lf-hp-mast{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;border-top:3px double var(--fg);border-bottom:1px solid var(--fg);padding:9px 0;font-size:13px;letter-spacing:.2em;text-transform:uppercase;font-weight:600;color:var(--fg)}
.lf-hp-head{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(0,1fr);gap:48px;align-items:end;padding:36px 0 30px;border-bottom:1px solid var(--fg)}
.lf-hp-head .q-h1{font-size:clamp(40px,5.4vw,80px);line-height:.98;margin:0;max-width:14ch}
.lf-hp-head .q-h1 em{font-style:italic;color:var(--accent-ink)}
.lf-hp-head .q-lead{margin:0 0 18px}
.lf-hp-grid{display:grid;grid-template-columns:minmax(0,1.55fr) minmax(0,1fr);gap:0;border-bottom:1px solid var(--fg)}
.lf-hp-lead{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:26px;padding:28px 28px 28px 0;border-right:1px solid var(--border);color:inherit;text-decoration:none}
.lf-hp-lead .ph{aspect-ratio:4/3;overflow:hidden;border:1px solid var(--fg);padding:8px;background:var(--card)}
.lf-hp-lead img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .8s}
.lf-hp-lead:hover img{transform:scale(1.04)}
.lf-hp-lead .k,.lf-hp-side .k{font-size:13px;letter-spacing:.18em;text-transform:uppercase;font-weight:700;color:var(--accent-ink)}
.lf-hp-lead h2{font-family:var(--q-serif);font-size:clamp(24px,2.3vw,34px);line-height:1.12;margin:10px 0 12px;font-weight:600;color:var(--fg)}
.lf-hp-lead p{margin:0;font-family:var(--q-serif);font-size:17px;line-height:1.55;color:var(--fg-muted)}
.lf-hp-lead .more{display:inline-block;margin-top:14px;font-weight:700;font-size:14.5px;color:var(--accent-ink);border-bottom:1px solid currentColor}
.lf-hp-side{list-style:none;margin:0;padding:0 0 0 28px;display:flex;flex-direction:column}
.lf-hp-side li{padding:26px 0;border-bottom:1px solid var(--border)}.lf-hp-side li:last-child{border-bottom:0}
.lf-hp-side a{color:inherit;text-decoration:none;display:block}
.lf-hp-side h3{font-family:var(--q-serif);font-size:21px;line-height:1.2;margin:8px 0 0;font-weight:600;color:var(--fg)}
.lf-hp-side a:hover h3{color:var(--accent-ink)}
.lf-hp-stats{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));padding-top:26px}
.lf-hp-stats div{padding:0 20px;border-left:1px solid var(--border)}.lf-hp-stats div:first-child{border-left:0;padding-left:0}
.lf-hp-stats b{display:block;font-family:var(--q-serif);font-size:38px;font-weight:600;line-height:1}
.lf-hp-stats span{display:block;font-size:13.5px;color:var(--fg-muted);margin-top:6px}
@media(max-width:1024px){.lf-hp-head,.lf-hp-grid{grid-template-columns:1fr}.lf-hp-lead{border-right:0;padding-right:0;border-bottom:1px solid var(--border)}.lf-hp-side{padding-left:0}.lf-hp-stats{grid-template-columns:repeat(2,minmax(0,1fr));gap:20px 0}}
@media(max-width:640px){.lf-hp-lead{grid-template-columns:1fr}.lf-hp-mast span:nth-child(n+3){display:none}}
"""

_NUM = re.compile(r"^(Up to )?\d[\d,.]*( to \d[\d,.]*)?(\s?[A-Za-z%]{1,8})?$")


def _head(s, ctx):
    E = ctx["E"]
    eb = f'<div class="q-eyebrow">{E(s["eyebrow"])}</div>' if s.get("eyebrow") else ""
    h = f'<h2 class="q-h2">{E(s["heading"])}</h2>' if s.get("heading") else ""
    lead = f'<p class="q-lead">{E(s["intro"])}</p>' if s.get("intro") else ""
    return f'<div class="lf-sec-head">{eb}{h}{lead}</div>'


def _btns(s, ctx):
    E, L = ctx["E"], ctx["L"]
    out = ""
    if s.get("primary"):
        out += f'<a class="q-btn" href="{E(L(s["primary"]["href"]))}">{E(s["primary"]["label"])}</a>'
    if s.get("secondary"):
        out += f'<a class="q-btn-ghost" href="{E(L(s["secondary"]["href"]))}">{E(s["secondary"]["label"])}<span style="width:22px;height:1px;background:currentColor;display:inline-block"></span></a>'
    return f'<div class="pv-btns">{out}</div>' if out else ""


def _eyebrow(s, E):
    return f'<div class="q-eyebrow">{E(s["eyebrow"])}</div>' if s.get("eyebrow") else ""


def _prodstage(s, ctx):
    E, RAW, rel = ctx["E"], ctx["RAW"], ctx["rel"]
    sid = s.get("id", "pstage")
    chips = "".join(f'<span class="lf-chip"><span>{E(k)}</span><b>{E(v)}</b></span>' for k, v in s.get("chips", []))
    chips = f'<div class="lf-chips">{chips}</div>' if chips else ""
    kind = s.get("kind", "float")
    tag = f'<span class="lf-ps-tag">{E(s["tag"])}</span>' if s.get("tag") else ""
    extra = "".join(f'<a class="q-btn-ghost" href="{E(ctx["L"](a["href"]))}"{" target=_blank rel=noopener" if a.get("external") else ""}>{E(a["label"])}</a>' for a in s.get("actions", []))
    fine = s.get("fine")
    fine_html = f'<p class="lf-fine">{E(fine[0])}<a href="{E(ctx["L"](fine[2]))}">{E(fine[1])}</a></p>' if fine else ""
    badge = f'<div class="lf-badge">{E(s["tag"])}</div>' if s.get("tag") else ""
    js = (f'<script>(function(){{var r=document.getElementById("{sid}");if(!r||matchMedia("(prefers-reduced-motion: reduce)").matches||!matchMedia("(pointer:fine)").matches)return;'
          'var t=r.querySelector(".lf-ps-tilt");r.addEventListener("pointermove",function(e){var b=r.getBoundingClientRect(),x=(e.clientX-b.left)/b.width-.5,y=(e.clientY-b.top)/b.height-.5;'
          't.style.transform="rotateY("+(x*14).toFixed(1)+"deg) rotateX("+(-y*10).toFixed(1)+"deg)"});r.addEventListener("pointerleave",function(){t.style.transform=""})})();</script>')
    return (f'<section class="q-section lf-dark lf-ps" id="{E(sid)}"><div class="q-container lf-ps-wrap"><div>'
            f'{_eyebrow(s, E)}<h1 class="q-h1">{RAW(s["heading"])}</h1>'
            f'<div class="q-lead">{E(s.get("subhead", ""))}</div>{badge}{_btns(s, ctx).replace("</div>", extra + "</div>", 1) if s.get("primary") else ""}{fine_html}{chips}</div>'
            f'<div class="lf-ps-stage k-{E(kind)}"><div class="lf-ps-halo" aria-hidden="true"></div><div class="lf-ps-ring" aria-hidden="true"></div><div class="lf-ps-ring r2" aria-hidden="true"></div><div class="lf-ps-disc" aria-hidden="true"></div>'
            f'<div class="lf-ps-tilt"><img class="lf-ps-img" src="{E(rel(s["image"]))}"{ctx["srcset"](s["image"])} alt="{E(s.get("image_alt", ""))}" width="{s.get("image_w", 1200)}" height="{s.get("image_h", 800)}" fetchpriority="high" decoding="async"></div></div>'
            f'</div>{js}</section>')


def _doclist(s, ctx):
    E, L = ctx["E"], ctx["L"]
    rows = "".join(f'<li><span class="ic" aria-hidden="true"></span><div><b>{E(t)}</b><span>{E(d)}</span></div><em>In the DMP library</em></li>' for t, d in s["items"])
    return f'{ctx["sec_open"](s)}<div class="q-container">{_head(s, ctx)}<ul class="lf-doclist">{rows}</ul></div></section>'


def _specs(s, ctx):
    E = ctx["E"]
    cells = []
    for k, v in s["items"]:
        num = bool(_NUM.match(str(v))) and len(str(v)) <= 14
        cells.append(f'<div class="lf-spec-c{" num" if num else ""}"><dt>{E(k)}</dt><dd>{E(v)}</dd></div>')
    return f'{ctx["sec_open"](s)}<div class="q-container">{_head(s, ctx)}<dl class="lf-spec">{"".join(cells)}</dl></div></section>'


def _works(s, ctx):
    E, L, rel = ctx["E"], ctx["L"], ctx["rel"]
    cards = []
    for it in s["items"]:
        name, blurb, href, img = it[0], it[1], it[2], it[3]
        fit = it[4] if len(it) > 4 else "contain"
        cards.append(f'<li><a href="{E(L(href))}"><div class="lf-wk-img{" cover" if fit == "cover" else ""}"><img src="{E(rel(img))}"{ctx["srcset"](img)} alt="" width="600" height="450" loading="lazy" decoding="async"></div>'
                     f'<div class="lf-wk-b"><h3>{E(name)}</h3><p>{E(blurb)}</p><span class="lf-wk-go">{E(s.get("link_label", "Open"))}</span></div></a></li>')
    return f'{ctx["sec_open"](s)}<div class="q-container">{_head(s, ctx)}<ul class="lf-wk">{"".join(cards)}</ul></div></section>'


def _hero_grid(s, ctx):
    E, RAW, L, rel = ctx["E"], ctx["RAW"], ctx["L"], ctx["rel"]
    chips = "".join(f'<a href="{E(L(h))}">{E(t)}</a>' for t, h in s.get("finder", []))
    find = f'<div class="lf-find"><span>{E(s.get("finder_label", "Find your building"))}</span><div>{chips}</div></div>' if chips else ""
    tiles = "".join(f'<a class="lf-tile" href="{E(L(h))}"><img src="{E(rel(img))}" alt="" width="600" height="600" decoding="async"{" fetchpriority=high" if i == 0 else " loading=lazy"}><span class="t"><span class="k">{E(k)}</span><b>{E(n)}</b></span></a>'
                    for i, (n, img, h, k) in enumerate(s.get("tiles", [])))
    return (f'<section class="q-section lf-hg" id="{E(s.get("id", "hero"))}"><div class="q-container lf-hg-wrap"><div>'
            f'{_eyebrow(s, E)}<h1 class="q-h1">{RAW(s["heading"])}</h1>'
            f'<div class="q-lead">{E(s.get("subhead", ""))}</div>{_btns(s, ctx)}{find}</div><div class="lf-hg-grid">{tiles}</div></div></section>')


def _hero_press(s, ctx):
    E, RAW, L, rel = ctx["E"], ctx["RAW"], ctx["L"], ctx["rel"]
    ld = s.get("lead", {})
    side = "".join(f'<li><a href="{E(L(h))}"><span class="k">{E(k)}</span><h3>{E(t)}</h3></a></li>' for k, t, h in s.get("side", []))
    stats = "".join(f'<div><b>{E(v)}</b><span>{E(l)}</span></div>' for v, l in s.get("stats", []))
    mast = "".join(f"<span>{E(x)}</span>" for x in s.get("masthead", []))
    lead = (f'<a class="lf-hp-lead" href="{E(L(ld["href"]))}"><div class="ph"><img src="{E(rel(ld["image"]))}" alt="{E(ld.get("alt", ""))}" width="900" height="675" fetchpriority="high" decoding="async"></div>'
            f'<div><span class="k">{E(ld.get("kicker", ""))}</span><h2>{E(ld["title"])}</h2><p>{E(ld.get("body", ""))}</p><span class="more">{E(ld.get("label", "Read the story"))}</span></div></a>') if ld else ""
    return (f'<section class="q-section lf-hp" id="{E(s.get("id", "hero"))}"><div class="q-container lf-hp-wrap"><div class="lf-hp-mast">{mast}</div>'
            f'<div class="lf-hp-head"><h1 class="q-h1">{RAW(s["heading"])}</h1><div><div class="q-lead">{E(s.get("subhead", ""))}</div>{_btns(s, ctx)}</div></div>'
            f'<div class="lf-hp-grid">{lead}<ol class="lf-hp-side">{side}</ol></div><div class="lf-hp-stats">{stats}</div></div></section>')


RENDER_EXTRA4 = {"prodstage": _prodstage, "specs": _specs, "works": _works, "hero-grid": _hero_grid, "hero-press": _hero_press, "doclist": _doclist}
