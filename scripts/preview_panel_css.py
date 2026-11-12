"""CSS and JS strings for scripts/preview_panel.py (DMP only). Kept apart so the renderer file stays readable.

SYS_CSS       system colour-coding, all three directions (subtle in Clean and Press)
SHOWCASE_CSS  Showcase after the dial-back: DMP's own light chrome and type, plus the keypad hero, zone scenes, slim zone bar and pager
CLEAN_CSS     Swiss spec-sheet catalogue
PRESS_CSS     editorial magazine
PANEL_JS      keypad state machine, zone scroll-spy, chapter pager, optional WebAudio sound (Showcase only)

No text under 13px, tap targets 44px on phones, every animation off under prefers-reduced-motion.
"""

SYS_CSS = r"""
:root{--sys:#ffd23d;--sys-ink:#6f5500}
[data-sys="intrusion"]{--sys:#ffd23d;--sys-ink:#6f5500}
[data-sys="access"]{--sys:#2fd47a;--sys-ink:#0b6b3a}
[data-sys="fire"]{--sys:#ff5a4d;--sys-ink:#b3261a}
[data-sys="video"]{--sys:#4aa3ff;--sys-ink:#0f5bb5}
[data-sys="mobile"]{--sys:#9b87ff;--sys-ink:#5a3fd0}
/* environment plates */
.pv-lh .bg.env img{opacity:.78;object-position:50% 50%}
.pv-lh .bg.env.flip img{animation-name:pn-kb-flip;transform:scaleX(-1) scale(1.04)}
.pv-lh .bg.hv.env.flip img.hv-poster{transform:scaleX(-1)}
@keyframes pn-kb-flip{from{transform:scaleX(-1) scale(1.04) translate(0,0)}to{transform:scaleX(-1) scale(1.14) translate(-1.5%,1%)}}
.pv-lh .bg.env::after,.pv-lh .bg.hv.env::after{background:linear-gradient(90deg,color-mix(in srgb,var(--lh-bg,#0c0d0f) 94%,transparent) 0%,color-mix(in srgb,var(--lh-bg,#0c0d0f) 80%,transparent) 38%,color-mix(in srgb,var(--lh-bg,#0c0d0f) 34%,transparent) 72%,color-mix(in srgb,var(--lh-bg,#0c0d0f) 46%,transparent) 100%),linear-gradient(180deg,color-mix(in srgb,var(--lh-bg,#0c0d0f) 52%,transparent) 0%,transparent 26%,transparent 58%,var(--lh-bg,#0c0d0f) 100%)}
@media(max-width:1024px){.pv-lh .bg.env::after,.pv-lh .bg.hv.env::after{background:linear-gradient(180deg,color-mix(in srgb,var(--lh-bg,#0c0d0f) 62%,transparent) 0%,color-mix(in srgb,var(--lh-bg,#0c0d0f) 74%,transparent) 50%,var(--lh-bg,#0c0d0f) 100%)}.pv-lh .bg.env img{opacity:.7}}
@media(prefers-reduced-motion:reduce){.pv-lh .bg.env img{animation:none!important}.pv-lh .bg.env.flip img{transform:scaleX(-1)}}
html[data-dir="showcase"] .pv-lh .bg.hv.env[data-mp4*="hero-signal"] video.on{mix-blend-mode:screen;opacity:.9}
.pv-envcap{position:absolute;right:16px;bottom:12px;z-index:3;margin:0;padding:4px 9px;font:500 13px/1.2 var(--q-sans);letter-spacing:.02em;color:#fff;background:rgba(0,0,0,.62);border-radius:2px;pointer-events:none}
.pv-lh:has(.bg.hv:not([data-mp4*="hero-signal"]) video.on) .pv-envcap{display:none}
@media(max-width:767px){.pv-envcap{right:10px;bottom:8px}}
/* system colour on the system and product pages */
html[data-sys] .pv-lh{border-top:3px solid var(--sys)}
html[data-sys] .pv-lh .q-eyebrow{color:var(--sys)}
html[data-sys] .pv-lh .q-eyebrow::before{background:var(--sys)}
html[data-sys] .pv-lh .glow{background:radial-gradient(600px circle at var(--mx,70%) var(--my,40%),color-mix(in srgb,var(--sys) 24%,transparent),transparent 60%)}
html[data-sys] .pv-lh .hero3d.lf-float::before{background:radial-gradient(circle,color-mix(in srgb,var(--sys) 30%,transparent),transparent 64%)}
html[data-sys] .pv-lh .hero3d.lf-float::after{border-color:color-mix(in srgb,var(--sys) 45%,transparent)}
html[data-sys] .pv-lh .hero3d .disc{background:radial-gradient(ellipse at center,color-mix(in srgb,var(--sys) 45%,transparent),transparent 70%)}
html[data-sys] .pv-lh .fcard:not(.b) .k{color:var(--sys)}
html[data-sys] .pv-lh .fcard.b .k{color:var(--sys-ink)}
.mo-tag{font-size:13px}
html[data-dir="press"] .bignum{opacity:1!important;color:#857b5f!important}
html[data-dir="clean"] .bignum{opacity:1!important;color:#7f8690!important}
.tl-span b,.tl-span span{font-size:13px!important}
html[data-sys] .pv-lh .fcard li::before{background:var(--sys);box-shadow:inset 0 0 0 4px color-mix(in srgb,var(--sys) 35%,#000)}
html[data-sys] .lf-ps{border-top:3px solid var(--sys)}
html[data-sys] .lf-ps .q-eyebrow{color:var(--sys)}
html[data-sys] .lf-ps .q-eyebrow::before{background:var(--sys)}
html[data-sys] .lf-ps-halo{background:radial-gradient(circle,color-mix(in srgb,var(--sys) 30%,transparent),transparent 66%)}
html[data-sys] .lf-ps-ring{border-color:color-mix(in srgb,var(--sys) 42%,transparent)}
html[data-sys] .lf-ps-disc{background:radial-gradient(ellipse at center,color-mix(in srgb,var(--sys) 40%,transparent),transparent 70%)}
html[data-sys] .lf-ps .lf-chip{border-top:2px solid var(--sys)}
html[data-sys] .lf-dark .lf-spec-c.num{box-shadow:inset 0 2px 0 var(--sys)}
/* stage modules on a system page glow in the system colour (buttons stay DMP yellow) */
html[data-sys] :is(.dw2-st-stage,.dw2-st-prog,.pp-flow,.mo-c3-stage,.dw2-chips){--q-gold:var(--sys);--pn-y:var(--sys);--q-gold-bright:var(--sys)}
/* links to a system carry its colour as a thin top rule */
:is(.dw-mt,.pv-tilt,.ex-tab)[href*="services/"]{border-top:3px solid var(--sysl,#ffd23d)}
:is(.dw-mt,.pv-tilt,.ex-tab)[href*="services/access-control"]{--sysl:#2fd47a}
:is(.dw-mt,.pv-tilt,.ex-tab)[href*="services/fire"]{--sysl:#ff5a4d}
:is(.dw-mt,.pv-tilt,.ex-tab)[href*="services/video"]{--sysl:#4aa3ff}
:is(.dw-mt,.pv-tilt,.ex-tab)[href*="services/mobile-automation"]{--sysl:#9b87ff}
"""

SHOWCASE_CSS = r"""
/* ============================================================ SHOWCASE ============================================================
   Dialled back after round 4. The page is DMP's own site first: the theme's white header and footer, its mixed-case headings
   (--q-serif) and Inter body, rounded yellow buttons, cards with soft shadows, light and dark bands in the content's own rhythm.
   The panel ideas stay where they earn their place: the keypad hero (dark, Barlow Condensed headline), the slim zone bar under
   the header, the six zone scenes (big Barlow numerals only), Scenes and Night shift. Mono is for tiny labels only. */
html[data-dir="showcase"]{--pn-bk:#0a0a0b;--pn-ink:#101112;--pn-panel:#16171a;--pn-panel2:#1d1f23;--pn-line:rgba(255,255,255,.11);--pn-line2:rgba(255,255,255,.2);--pn-txt:#f3f2ed;--pn-mut:#b4b3ab;
  --pn-y:#ffd23d;--pn-amber:#ff9d2e;--pn-ok:#3ddc84;--pn-st:var(--pn-ok);--pn-ease:cubic-bezier(.2,.7,.1,1);--pn-pad:clamp(20px,4.2vw,68px);--pn-zbh:36px;--zi:var(--zc);
  --pn-disp:'Barlow Condensed','Barlow Condensed Fallback','Arial Narrow',Arial,sans-serif;--pn-mono:'JetBrains Mono',ui-monospace,'SFMono-Regular',Menlo,Consolas,'Liberation Mono',monospace;
  --pn-head:var(--q-serif)}
/* disarmed: the yellow accents (buttons, the armed word, dots) turn amber. Text inks on light grounds keep their contrast. */
html[data-dir="showcase"][data-pn="disarmed"]{--pn-st:var(--pn-amber);--pn-y:#ff9d2e;--q-gold:#ff9d2e;--q-gold-dim:#ff9d2e;--chrome-accent:#ff9d2e}
html[data-dir="showcase"][data-pn="disarmed"] :is(.lf-dark,.pv-lh,.pv-dark,.pv-band){--q-gold:#ff9d2e;--q-gold-bright:#ffb45e;--accent-ink:#ff9d2e}
html[data-dir="showcase"][data-pn="arming"]{--pn-st:var(--pn-y)}
/* anchors: fixed padding (Night shift's own scroll margin is written against these two numbers) */
html[data-dir="showcase"].pn-zbar{scroll-padding-top:172px}
@media(max-width:767px){html[data-dir="showcase"].pn-zbar{scroll-padding-top:140px}}
html[data-sys][data-dir="showcase"] .pv-lh .q-h1 em{color:var(--sys)}
/* sticky modules sit under the header plus the zone bar */
html[data-dir="showcase"].pn-zbar :is(.pp-subnav,.pp-bb){top:calc(var(--pp-hdr,81px) + var(--pn-zbh) + 2px)}
html[data-dir="showcase"].pn-zbar:has(.pp-subnav){scroll-padding-top:calc(var(--pp-hdr,81px) + 72px + var(--pn-zbh))}
/* ---- shared atoms ---- */
.pn-led{display:inline-block;width:8px;height:8px;border-radius:50%;background:#34363a;box-shadow:inset 0 0 0 1px rgba(255,255,255,.14);flex:none;transition:background .4s,box-shadow .4s}
.pn-btn{display:inline-flex;align-items:center;gap:.5em;min-height:52px;padding:0 26px;border-radius:999px;font:700 16px/1 var(--q-sans);letter-spacing:0;text-decoration:none;border:1.5px solid transparent;transition:transform .25s var(--pn-ease),background .25s,color .25s,box-shadow .25s,border-color .25s}
.pn-btn-y{background:var(--pn-y);color:#0a0a0b;box-shadow:0 10px 26px color-mix(in srgb,var(--pn-y) 28%,transparent)}
.pn-btn-y:hover{transform:translateY(-2px);box-shadow:0 16px 34px color-mix(in srgb,var(--pn-y) 38%,transparent)}
.pn-btn-o{border-color:var(--pn-line2);color:var(--pn-txt)}
.pn-btn-o:hover{background:var(--pn-txt);border-color:var(--pn-txt);color:var(--pn-bk)}
.pn-btn-k{background:#0a0a0b;color:#fff;box-shadow:0 10px 26px rgba(0,0,0,.22)}
.pn-btn-k:hover{transform:translateY(-2px);box-shadow:0 16px 34px rgba(0,0,0,.28)}
.pn-btn-ko{border-color:#0a0a0b;color:#0a0a0b}
.pn-btn-ko:hover{background:#0a0a0b;color:#fff}
html:not(.pn-js) .pn-js-only{display:none!important}
.pn-js .pn-rv{opacity:0;transform:translateY(18px);transition:opacity .8s var(--pn-ease),transform .8s var(--pn-ease)}
.pn-js .pn-rv.in{opacity:1;transform:none}
.pn-js .pn-rv:nth-child(2){transition-delay:.08s}.pn-js .pn-rv:nth-child(3){transition-delay:.16s}.pn-js .pn-rv:nth-child(4){transition-delay:.24s}
:is(.pn-hero,.pn-zone,.pn-zb,.pn-ctl) :focus-visible{outline:2px solid var(--pn-y);outline-offset:3px;border-radius:2px}
.pn-z6 :focus-visible{outline-color:#0a0a0b}
:is(.pn-hero,.pn-zone) :is(h1,h2,h3,p,dl,dd,dt,ol,ul,figure){margin:0;padding:0}
:is(.pn-hero,.pn-zone,.pn-zb) :is(ol,ul){list-style:none}
:is(.pn-hero,.pn-zone) img{display:block;max-width:100%;height:auto}
:is(.pn-hero,.pn-zone) button{font:inherit;color:inherit;background:none;border:0;padding:0;cursor:pointer}

/* ---- zone bar: a slim light strip inside the sticky header ---- */
.pn-zb{display:flex;align-items:stretch;border-top:1px solid rgba(10,12,16,.1);background:#f6f6f3;--pn-st-ink:#0b6b3a}
/* the sticky header ignores pointer events (dw-fix) and only re-enables its utility bar and nav; the zone strip must be clickable too */
.q-header.dw-fix .pn-zb,.q-header .pn-zb,.pn-zb a{pointer-events:auto}
html[data-pn="disarmed"] .pn-zb{--pn-st-ink:#9a4a00}
html[data-pn="arming"] .pn-zb{--pn-st-ink:#6f5500}
.pn-zb ol{flex:1;display:grid;grid-template-columns:repeat(6,minmax(0,1fr));margin:0;padding:0}
.pn-zb li+li{border-left:1px solid rgba(10,12,16,.08)}
.pn-zb li:nth-child(6) a{--zc:#0a0a0b!important}
.pn-zb a{position:relative;display:flex;align-items:center;gap:9px;height:var(--pn-zbh);padding:0 16px;text-decoration:none;font:600 13px/1 var(--pn-mono);letter-spacing:.06em;text-transform:uppercase;color:#4a4d54;justify-content:center;overflow:hidden;white-space:nowrap;transition:color .3s,background .3s}
.pn-zb a::after{content:"";position:absolute;left:0;right:0;bottom:0;height:3px;background:var(--zc);transform:scaleX(0);transform-origin:left;transition:transform .5s var(--pn-ease)}
.pn-zb a b{color:#0a0a0b;font-weight:700}
.pn-zb a em{margin-left:6px;font-style:normal;letter-spacing:.08em;color:#5c5f66}
.pn-zb a:hover{color:#0a0a0b;background:rgba(10,12,16,.05)}
.pn-zb a .pn-led{background:var(--zc);box-shadow:inset 0 0 0 1px rgba(0,0,0,.28)}
.pn-zb a.is-on{color:#0a0a0b;background:#fff}
.pn-zb a.is-on::after{transform:scaleX(1)}
.pn-zb a.is-on .pn-led{box-shadow:inset 0 0 0 1px rgba(0,0,0,.28),0 0 0 3px color-mix(in srgb,var(--zc) 30%,transparent)}
.pn-zb :focus-visible{outline-color:#0a0a0b!important;outline-offset:-3px!important}
html[data-pn="disarmed"] .pn-zb-home a:not(.is-on) .pn-led{background:#c9cbd0}
html[data-pn="disarmed"] .pn-zb-home a em{color:#9a4a00}
.pn-zb-r{display:none}
.pn-st{display:inline-flex;align-items:center;gap:10px;font:700 13px/1 var(--pn-mono);letter-spacing:.14em;color:var(--pn-st-ink);white-space:nowrap}
.pn-st i{width:9px;height:9px;border-radius:50%;background:var(--pn-st);box-shadow:inset 0 0 0 1px rgba(0,0,0,.25),0 0 0 3px color-mix(in srgb,var(--pn-st) 22%,transparent)}
@media(max-width:1500px){.pn-zb a em{display:none}}
@media(max-width:1024px){.pn-zb a{padding:0 10px;gap:7px}}
@media(max-width:767px){
  html[data-dir="showcase"]{--pn-zbh:44px}
  .pn-zb-home a{justify-content:center;padding:0 4px;gap:6px;letter-spacing:.04em}
  .pn-zb-home a span{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}
  .pn-zb:not(.pn-zb-home){overflow-x:auto;scrollbar-width:none;-webkit-overflow-scrolling:touch}
  .pn-zb:not(.pn-zb-home)::-webkit-scrollbar{display:none}
  .pn-zb:not(.pn-zb-home) ol{display:flex;flex:none}
  .pn-zb:not(.pn-zb-home) a{padding:0 14px}
}

/* ---- HERO: the keypad ---- */
.pn-hero{position:relative;padding:clamp(34px,5vh,64px) var(--pn-pad) 0;display:flex;flex-direction:column;overflow:hidden;isolation:isolate;background:var(--pn-bk);color:var(--pn-txt);font-family:var(--q-sans)}
@media(min-width:1025px){.pn-hero{min-height:calc(100svh - 170px)}}
.pn-hero-grid{position:absolute;inset:0;z-index:-1;background:radial-gradient(60% 55% at 72% 46%,color-mix(in srgb,var(--pn-st) 10%,transparent),transparent 70%),linear-gradient(var(--pn-line) 1px,transparent 1px) 0 0/100% 96px,linear-gradient(90deg,var(--pn-line) 1px,transparent 1px) 0 0/96px 100%;-webkit-mask:linear-gradient(#000 55%,transparent);mask:linear-gradient(#000 55%,transparent);opacity:.75}
.pn-mark{position:absolute;width:18px;height:18px;z-index:-1;opacity:.6}
.pn-mark::before,.pn-mark::after{content:"";position:absolute;background:var(--pn-y)}
.pn-mark::before{left:0;right:0;top:50%;height:1px}.pn-mark::after{top:0;bottom:0;left:50%;width:1px}
.pn-mark-tl{left:calc(var(--pn-pad) - 9px);top:14px}.pn-mark-br{right:calc(var(--pn-pad) - 9px);bottom:150px}
.pn-hero-in{flex:1;display:grid;grid-template-columns:minmax(0,46fr) minmax(0,54fr);gap:clamp(24px,4vw,72px);align-items:center;padding-bottom:clamp(28px,5vh,56px);width:100%;max-width:1640px;margin:0 auto}
.pn-eyebrow{display:flex;align-items:center;flex-wrap:wrap;gap:6px 12px;font:600 13px/1.2 var(--pn-mono);letter-spacing:.16em;text-transform:uppercase;color:var(--pn-mut);margin-bottom:clamp(18px,3vh,30px)!important}
.pn-eyebrow i{width:28px;height:1px;background:var(--pn-y)}.pn-eyebrow span{color:var(--pn-y)}
.pn-h1{font-family:var(--pn-disp);font-weight:800;font-size:clamp(60px,7.4vw,148px);line-height:.86;letter-spacing:-.005em;text-transform:uppercase;color:var(--pn-txt)}
.pn-h1-l{display:block;white-space:nowrap}
.pn-h1-state{margin-top:.1em;min-height:1.02em}
.pn-h1-word{position:relative;display:inline-block;padding:.03em .14em .05em .1em;margin-left:-.1em;color:#0a0a0b;z-index:0}
.pn-h1-word::before{content:"";position:absolute;inset:0;z-index:-1;background:var(--pn-y);transform-origin:left;transition:transform .55s var(--pn-ease)}
html[data-pn="disarmed"] .pn-h1-word,html[data-pn="arming"] .pn-h1-word{color:var(--pn-bk);-webkit-text-stroke:.035em var(--pn-st);paint-order:stroke fill}
html[data-pn="disarmed"] .pn-h1-word::before,html[data-pn="arming"] .pn-h1-word::before{transform:scaleX(0);opacity:0}
html[data-pn="arming"] .pn-h1-word{animation:pn-blinkt .5s steps(2) infinite}
.pn-lede{max-width:34em;margin-top:clamp(20px,3.2vh,34px)!important;font-size:clamp(16px,1.2vw,19px);line-height:1.55;color:#cfcec7}
.pn-lede strong{color:var(--pn-y);font-weight:700}
.pn-hero-cta{display:flex;flex-wrap:wrap;gap:14px;margin-top:clamp(20px,3.2vh,34px)}
.pn-lane{display:flex;flex-wrap:wrap;gap:0 22px;margin-top:18px!important;font:600 13px/1.2 var(--pn-mono);letter-spacing:.06em;text-transform:uppercase}
.pn-lane a{display:inline-flex;align-items:center;gap:6px;min-height:44px;color:var(--pn-mut);text-decoration:underline;text-decoration-color:var(--pn-line2);text-underline-offset:5px}
.pn-lane a:hover{color:var(--pn-y);text-decoration-color:var(--pn-y)}
.pn-hero-spec{display:grid;grid-template-columns:repeat(4,1fr);border-top:1px solid var(--pn-line2);margin:0 calc(var(--pn-pad)*-1)!important;padding:0 var(--pn-pad)!important}
.pn-hero-spec div{padding:18px 20px 22px 0;display:grid;grid-template-columns:auto 1fr;column-gap:16px;align-items:baseline}
.pn-hero-spec div+div{border-left:1px solid var(--pn-line);padding-left:20px}
.pn-hero-spec dt{grid-column:1/-1;font:600 13px/1 var(--pn-mono);letter-spacing:.16em;text-transform:uppercase;color:var(--pn-mut);margin-bottom:10px}
.pn-hero-spec dd:not(.d){font-family:var(--pn-disp);font-weight:800;font-size:clamp(34px,3.2vw,52px);line-height:.9;font-variant-numeric:tabular-nums;text-transform:uppercase}
.pn-hero-spec dd.d{font:500 13px/1.35 var(--pn-mono);letter-spacing:.03em;color:var(--pn-mut);text-transform:uppercase}

.pn-hero-kp{position:relative;min-width:0}
.pn-kp{container-type:inline-size;position:relative;width:100%;max-width:820px;margin:0 auto}
.pn-kp-case{position:relative;aspect-ratio:978/660;border-radius:5.4cqw;padding:6.4cqw 6.8cqw 7.2cqw;background:linear-gradient(160deg,#fdfdfd 0%,#eceef0 38%,#d3d6da 100%);
  box-shadow:inset 0 .35cqw .2cqw #fff,inset 0 -1cqw 1.4cqw rgba(60,66,80,.35),inset .5cqw 0 .9cqw rgba(255,255,255,.7),inset -.6cqw 0 1cqw rgba(60,66,80,.22),0 0 0 1px rgba(0,0,0,.6),0 5cqw 9cqw rgba(0,0,0,.75),0 0 16cqw color-mix(in srgb,var(--pn-st) 16%,transparent);transition:box-shadow .8s}
.pn-kp-led{position:absolute;left:50%;top:2.7cqw;width:2cqw;height:1cqw;margin-left:-1cqw;border-radius:1cqw;background:#ff3b30;box-shadow:0 0 1.2cqw #ff3b30,0 0 3cqw rgba(255,59,48,.7);transition:background .3s,box-shadow .3s}
html[data-pn="disarmed"] .pn-kp-led{background:#c9cdd3;box-shadow:inset 0 .15cqw .3cqw rgba(0,0,0,.35)}
html[data-pn="arming"] .pn-kp-led{animation:pn-blink .5s steps(2) infinite}
@keyframes pn-blink{50%{background:#c9cdd3;box-shadow:none}}
@keyframes pn-blinkt{50%{opacity:.35}}
.pn-kp-mic{position:absolute;right:3.2cqw;bottom:5.2cqw;width:.7cqw;height:.7cqw;border-radius:50%;background:#7d838c;box-shadow:inset 0 .1cqw .2cqw #222}
.pn-kp-glass{height:100%;border-radius:1.5cqw;background:#050608;padding:.9cqw;box-shadow:0 0 0 .25cqw rgba(0,0,0,.18),inset 0 0 0 1px #222,0 .3cqw .5cqw rgba(255,255,255,.9)}
.pn-kp-screen{position:relative;height:100%;border-radius:.7cqw;overflow:hidden;font-family:var(--q-sans);font-size:clamp(13px,2.15cqw,18px);color:#eaf3ff;display:grid;grid-template-columns:24% 1fr 35.5%;grid-template-rows:auto 1fr auto;
  background:radial-gradient(90% 110% at 42% 48%,#1d63d4 0%,#0e41a8 34%,#082873 62%,#030f36 100%);transition:filter .6s}
html[data-pn="disarmed"] .pn-kp-screen{filter:saturate(.72) brightness(.9)}
.pn-kp-arcs{position:absolute;inset:0;width:100%;height:100%}
.pn-kp-sheen{position:absolute;inset:0;pointer-events:none;background:linear-gradient(118deg,rgba(255,255,255,.13) 0%,rgba(255,255,255,.03) 26%,transparent 27%)}
.pn-kp-screen>*{position:relative}.pn-kp-screen>.pn-kp-arcs,.pn-kp-screen>.pn-kp-sheen,.pn-kp-screen>.pn-kp-events{position:absolute}
.pn-kp-bar{grid-column:1/-1;display:flex;justify-content:space-between;align-items:center;padding:2cqw 2.6cqw 0 2.6cqw}
.pn-kp-logo{width:10.5cqw!important;min-width:44px}
.pn-kp-clock{display:flex;align-items:center;gap:.7em;font-weight:600;font-size:max(13px,.86em);letter-spacing:.02em}
.pn-kp-clock svg{width:1.5em;height:1.05em;opacity:.9}
.pn-kp-info{padding:1cqw 0 0 2.8cqw;align-self:center}
.pn-kp-big{display:block;font-weight:200;font-size:4.2em;line-height:.9;letter-spacing:-.04em}
.pn-kp-cap{display:block;font-weight:600;font-size:max(13px,.72em);letter-spacing:.2em;text-transform:uppercase;margin-top:.3em;color:#cfe2ff}
.pn-kp-info dl{margin-top:1em!important;display:grid;gap:.4em;font-size:max(13px,.7em)}
.pn-kp-info dt{letter-spacing:.12em;text-transform:uppercase;color:#b9d2f7}
.pn-kp-info dd{font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#7dffb4;transition:color .3s}
html[data-pn="disarmed"] .pn-kp-info dd,html[data-pn="arming"] .pn-kp-info dd{color:#ffc37a}
.pn-kp-core{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:.5cqw;padding-top:.6cqw}
.pn-kp-shield{position:relative;width:25cqw;min-width:76px;border-radius:50%;transition:transform .25s var(--pn-ease)}
.pn-kp-shield svg{width:100%;overflow:visible;display:block}
.pn-js .pn-kp-shield:hover{transform:scale(1.035)}.pn-js .pn-kp-shield:active{transform:scale(.955)}
.pn-kp-shield:focus-visible{outline:max(2px,.4cqw) solid var(--pn-y)!important;outline-offset:.2cqw;border-radius:50%!important}
.pn-kp .sh-ring-bg{fill:rgba(3,14,52,.35);stroke:rgba(170,210,255,.18);stroke-width:1}
.pn-kp .sh-ring{fill:none;stroke:#3ddc84;stroke-width:2.6;stroke-linecap:round;stroke-dasharray:100;stroke-dashoffset:0;transform:rotate(-90deg);transform-origin:80px 85px;opacity:.9}
.pn-kp .sh-outer{fill:url(#pnShF);stroke:url(#pnShG);stroke-width:5;stroke-linejoin:round;filter:drop-shadow(0 0 5px rgba(125,255,180,.95)) drop-shadow(0 0 16px rgba(61,220,132,.7));transition:filter .5s,fill-opacity .4s}
.pn-kp .sh-trace{fill:none;stroke:#ffd23d;stroke-width:5;stroke-linejoin:round;stroke-linecap:round;stroke-dasharray:100;stroke-dashoffset:100;opacity:0}
.pn-kp .sh-inner{fill:rgba(9,60,150,.75);stroke:rgba(190,225,255,.7);stroke-width:1.6;stroke-linejoin:round;transition:fill .5s}
.pn-kp .sh-shackle{fill:none;stroke:#eaf3ff;stroke-width:5;stroke-linecap:round;transform-origin:92px 80px;transition:transform .45s var(--pn-ease)}
.pn-kp .sh-body{fill:#eaf3ff}.pn-kp .sh-key{fill:#0b3496}
html[data-pn="disarmed"] .pn-kp .sh-outer{filter:drop-shadow(0 0 6px rgba(255,157,46,.75))}
html[data-pn="disarmed"] .pn-kp .sh-inner{fill:rgba(4,22,80,.55)}
html[data-pn="disarmed"] .pn-kp .sh-ring{opacity:0}
html[data-pn="disarmed"] .pn-kp .sh-ring-bg{stroke:rgba(255,157,46,.55);animation:pn-invite 2.4s ease-in-out infinite}
html[data-pn="disarmed"] .pn-kp .sh-shackle{transform:translateY(-5px) rotate(28deg)}
@keyframes pn-invite{0%,100%{stroke-width:1;opacity:.5}50%{stroke-width:3.5;opacity:1}}
/* arming: the shield outline draws itself over the exit delay, the ring counts down */
html[data-pn="arming"] .pn-kp .sh-outer{fill-opacity:.25;stroke-opacity:.25;filter:none}
html[data-pn="arming"] .pn-kp .sh-trace{opacity:1;animation:pn-draw var(--pn-exit,3s) linear forwards;filter:drop-shadow(0 0 6px rgba(255,210,61,.9))}
html[data-pn="arming"] .pn-kp .sh-ring{stroke:#ffd23d;opacity:1;stroke-dashoffset:100;animation:pn-draw var(--pn-exit,3s) linear forwards}
html[data-pn="arming"] .pn-kp .sh-shackle{transform:translateY(-2px) rotate(10deg)}
@keyframes pn-draw{to{stroke-dashoffset:0}}
html.pn-thunk .pn-kp-shield{animation:pn-thunk .5s var(--pn-ease)}
@keyframes pn-thunk{0%{transform:scale(1)}35%{transform:scale(.93)}70%{transform:scale(1.045)}100%{transform:scale(1)}}
.pn-kp-state{font-weight:700;font-size:1.7em;line-height:1;letter-spacing:.07em;color:#eaf3ff;text-shadow:0 0 1em rgba(125,255,180,.9);white-space:nowrap}
html[data-pn="disarmed"] .pn-kp-state{color:#ffb866;text-shadow:0 0 1.2em rgba(255,157,46,.6)}
html[data-pn="arming"] .pn-kp-state{color:#ffd23d;text-shadow:0 0 1.2em rgba(255,210,61,.6)}
.pn-kp-arm{margin-top:1cqw;min-width:17cqw;padding:1.05cqw 2.2cqw!important;border-radius:5cqw;font-weight:700!important;font-size:max(13px,.82em)!important;letter-spacing:.16em;text-transform:uppercase;color:#eaf3ff!important;background:rgba(3,14,52,.55)!important;box-shadow:inset 0 0 0 1px rgba(190,225,255,.6);transition:transform .2s var(--pn-ease),background .3s}
html[data-pn="disarmed"] .pn-kp-arm{color:#04103a!important;background:linear-gradient(#fff,#cfe2ff)!important;box-shadow:0 .3cqw .8cqw rgba(0,0,0,.45),inset 0 -.2cqw .3cqw rgba(10,50,150,.3)}
html:not(.pn-js) .pn-kp-arm{display:none}
.pn-kp-menu{display:flex;flex-direction:column;justify-content:center;padding:0 1.6cqw 0 4.6cqw}
.pn-kp-menu a{display:flex;align-items:center;gap:1.2cqw;flex:0 1 5.6cqw;min-height:24px;padding:0 1.2cqw;text-decoration:none;font-weight:500;font-size:1.08em;letter-spacing:.01em;color:#eaf3ff;border-radius:.8cqw;white-space:nowrap;transition:background .2s,color .2s,transform .25s var(--pn-ease)}
.pn-kp-menu a i{width:max(7px,1.1cqw);height:max(7px,1.1cqw);border-radius:50%;background:var(--zc);box-shadow:0 0 1cqw var(--zc);transition:opacity .3s;flex:none}
html[data-pn="disarmed"] .pn-kp-menu a i{opacity:.4}
.pn-kp-menu a:hover{background:rgba(255,255,255,.12);color:#fff;transform:translateX(.5cqw)}
.pn-kp-menu a:focus-visible{outline:2px solid var(--pn-y)!important;outline-offset:-2px}
.pn-kp-log{grid-column:1/-1;display:flex;gap:1.4cqw;align-items:center;padding:1.1cqw 2.6cqw 1.3cqw!important;font:500 13px/1.2 var(--pn-mono);letter-spacing:.04em;text-transform:uppercase;background:rgba(1,6,26,.62);border-top:1px solid rgba(160,205,255,.2);white-space:nowrap;overflow:hidden}
.pn-kp-log span{color:#b9d2f7}.pn-kp-log b{font-weight:600;color:#fff;overflow:hidden;text-overflow:ellipsis}
.pn-kp-events{inset:0;z-index:5;display:flex;flex-direction:column;padding:2.4cqw 3cqw;background:rgba(2,8,34,.96);color:#eaf3ff}
.pn-kp-events[hidden]{display:none}
.pn-kp-events-h{display:flex;align-items:center;justify-content:space-between;gap:12px;padding-bottom:1.6cqw;border-bottom:1px solid rgba(160,205,255,.3)}
.pn-kp-events-h b{font-weight:500;font-size:1.5em}
.pn-kp-events-h button{min-height:max(32px,5cqw);padding:0 14px!important;border:1px solid rgba(190,225,255,.6)!important;border-radius:6px;font:600 13px/1 var(--pn-mono)!important;letter-spacing:.12em;text-transform:uppercase;color:#eaf3ff!important}
.pn-kp-events-h button:hover{background:rgba(255,255,255,.12)!important}
.pn-kp-events ol{margin:1.2cqw 0 0!important;display:grid;gap:.35em;overflow:auto;font:500 13px/1.5 var(--pn-mono);letter-spacing:.04em;text-transform:uppercase}
.pn-kp-events li{display:grid;grid-template-columns:6.5em 1fr;gap:10px}
.pn-kp-events li b{color:#b9d2f7;font-weight:500}
.pn-kp-floor{position:absolute;left:8%;right:8%;bottom:-5cqw;height:6cqw;background:radial-gradient(closest-side,color-mix(in srgb,var(--pn-st) 30%,transparent),transparent);filter:blur(1.4cqw);opacity:.75;z-index:-1}
.pn-ctl{display:flex;flex-wrap:wrap;justify-content:center;gap:10px;margin:clamp(26px,3.4cqw,40px) auto 0;max-width:820px}
.pn-key{display:inline-flex;align-items:center;justify-content:center;gap:9px;min-height:44px;padding:0 16px!important;border:1px solid var(--pn-line2)!important;font:700 13px/1 var(--pn-mono)!important;letter-spacing:.1em;text-transform:uppercase;color:var(--pn-txt)!important;background:rgba(255,255,255,.03)!important;transition:border-color .2s,color .2s,background .2s}
.pn-key:hover{border-color:var(--pn-y)!important;color:var(--pn-y)!important}
.pn-key-arm{border-color:var(--pn-st)!important;color:var(--pn-st)!important;min-width:132px}
.pn-key-arm::before{content:"";width:9px;height:9px;border-radius:50%;background:var(--pn-st);box-shadow:0 0 10px var(--pn-st)}
.pn-snd .on{display:none}.pn-snd[aria-pressed="true"] .on{display:block}.pn-snd[aria-pressed="true"] .off{display:none}
.pn-snd[aria-pressed="true"]{color:var(--pn-y)!important;border-color:color-mix(in srgb,var(--pn-y) 55%,transparent)!important}
.pn-kp-hint{margin-top:16px!important;text-align:center;font:600 13px/1.4 var(--pn-mono);letter-spacing:.1em;text-transform:uppercase;color:var(--pn-st);min-height:1.4em}
.pn-kp-demo{margin-top:6px!important;text-align:center;font:500 13px/1.4 var(--pn-mono);letter-spacing:.04em;color:var(--pn-mut)}
html:not(.pn-js) .pn-kp-demo{display:none}
.pn-sweep{position:fixed;left:0;right:0;top:0;height:2px;z-index:95;pointer-events:none;background:linear-gradient(90deg,transparent,var(--pn-st) 20%,var(--pn-st) 80%,transparent);box-shadow:0 0 24px 2px color-mix(in srgb,var(--pn-st) 70%,transparent);animation:pn-scan .9s var(--pn-ease) forwards}
@keyframes pn-scan{0%{transform:translateY(0);opacity:0}12%{opacity:1}100%{transform:translateY(100vh);opacity:0}}

/* ---- ZONE scaffold ---- */
.pn-zone{position:relative;padding:clamp(72px,9vw,140px) var(--pn-pad);border-top:1px solid var(--pn-line);overflow:hidden;isolation:isolate;background:var(--pn-bk);color:var(--pn-txt);font-family:var(--q-sans);font-size:17px;line-height:1.5}
.pn-zin{max-width:1560px;margin:0 auto}
.pn-zhead{display:flex;align-items:center;gap:16px;font:600 13px/1 var(--pn-mono);letter-spacing:.16em;text-transform:uppercase;color:var(--pn-mut);margin-bottom:clamp(36px,5vw,72px)}
.pn-ztag{display:inline-flex;align-items:center;gap:10px;color:var(--zc);border:1px solid color-mix(in srgb,var(--zc) 50%,transparent);padding:8px 12px;white-space:nowrap}
.pn-ztag .pn-led{background:var(--zc);box-shadow:0 0 10px var(--zc)}
.pn-zname{color:var(--pn-txt);white-space:nowrap}
.pn-zrule{flex:1;min-width:12px;height:7px;background:repeating-linear-gradient(90deg,var(--pn-line2) 0 1px,transparent 1px 8px)}
.pn-zmeta{white-space:nowrap}
.pn-zone .pn-h2{font-family:var(--pn-disp);font-weight:800;font-size:clamp(40px,4.9vw,84px);line-height:.92;letter-spacing:0;text-transform:uppercase;text-wrap:balance;color:var(--pn-txt)}
.pn-zone .pn-h2 em{font-style:normal;color:var(--zc)}
.pn-zone .pn-h2+p{margin-top:22px;max-width:36em;color:#cfcec7;font-size:clamp(16px,1.15vw,18px)}
.pn-zone h3{font-family:var(--pn-disp);font-weight:800;font-size:28px;letter-spacing:.005em;line-height:1;text-transform:uppercase}
.pn-zone h3 a{color:inherit;text-decoration:none;background:linear-gradient(currentColor,currentColor) 0 100%/0 2px no-repeat;transition:background-size .35s var(--pn-ease)}
.pn-zone h3 a:hover{background-size:100% 2px}
@media(max-width:767px){.pn-zone h3 a{display:inline-flex;align-items:center;min-height:44px;min-width:44px;background-position:0 86%}.pn-calls p,.pn-notes p,.pn-path li p{margin-top:0!important}}
/* round 4b: the same 44px rule on tablets, plus the keypad's on-screen menu, its Arm pill and the dealer facts row */
@media(min-width:768px) and (max-width:1024px){.pn-zone h3 a{display:inline-flex;align-items:center;min-height:44px;min-width:44px;background-position:0 86%}}
@media(max-width:1024px){.pn-z6-row a{display:inline-flex;align-items:center;min-height:44px}}
@media(min-width:600px) and (max-width:1024px){.pn-kp-menu a{flex:0 1 44px;min-height:44px}.pn-kp-arm{min-height:44px}}
.pn-zone{scroll-margin-top:-62px}
@media(max-width:767px){.pn-zone{scroll-margin-top:-36px}}
.pn-more{margin-top:28px!important}

/* Z1 intrusion */
.pn-z1{background:linear-gradient(180deg,#0a0a0b,#0e0e0f)}
.pn-z1-grid{display:grid;grid-template-columns:minmax(0,58fr) minmax(0,42fr);column-gap:clamp(24px,4vw,72px);align-items:start}
.pn-z1-num{grid-column:1;grid-row:1}
.pn-num{position:relative;font-family:var(--pn-disp);font-weight:800;font-size:clamp(190px,36vw,620px);line-height:.74;letter-spacing:-.02em;margin-left:-.17em!important;font-variant-numeric:tabular-nums;white-space:nowrap}
.pn-num-o,.pn-num-f{padding-right:.04em}
.pn-num-o{color:#0b0b0c;-webkit-text-stroke:3px var(--pn-y);paint-order:stroke fill}
.pn-num-f{position:absolute;left:0;top:0;color:var(--pn-y);clip-path:inset(-30% -10% -30% -10%)}
.pn-js .pn-num-f{clip-path:inset(130% -10% -30% -10%);transition:clip-path 1.6s cubic-bezier(.6,0,.1,1) .15s}
.pn-js .pn-z1.seen .pn-num-f{clip-path:inset(-30% -10% -30% -10%)}
.pn-num-unit{display:flex;align-items:baseline;gap:.6em;margin-top:clamp(18px,2.4vw,34px)!important;font:700 clamp(13px,1.3vw,18px)/1 var(--pn-mono);letter-spacing:.22em;text-transform:uppercase}
.pn-num-unit b{font:800 2.6em/1 var(--pn-disp);letter-spacing:0;color:var(--pn-y);margin-right:.15em}
.pn-num-plus{color:var(--pn-y)}
.pn-z1-copy{grid-column:1;grid-row:2;margin-top:clamp(32px,4vw,60px);max-width:700px}
.pn-slab{grid-column:2;grid-row:1/3;position:relative;background:var(--pn-y);color:#0a0a0b;padding:clamp(20px,2.2vw,32px) clamp(20px,2.2vw,32px) 0;box-shadow:12px 12px 0 color-mix(in srgb,var(--pn-y) 16%,transparent)}
.pn-slab::before{content:"";position:absolute;left:0;right:0;top:0;height:8px;background:repeating-linear-gradient(90deg,#0a0a0b 0 1px,transparent 1px 10px)}
.pn-slab-h{display:flex;justify-content:space-between;font:700 13px/1 var(--pn-mono);letter-spacing:.16em;text-transform:uppercase;padding:10px 0 14px!important;border-bottom:2px solid #0a0a0b}
.pn-slab dl div{display:flex;justify-content:space-between;align-items:baseline;gap:16px;padding:10px 0;border-bottom:1px solid rgba(10,10,11,.28)}
.pn-slab dt{font:600 13px/1.2 var(--pn-mono);letter-spacing:.08em;text-transform:uppercase}
.pn-slab dd{font-family:var(--pn-disp);font-weight:800;font-size:clamp(26px,2.4vw,36px);line-height:.95;font-variant-numeric:tabular-nums;text-align:right;white-space:nowrap}
.pn-slab-go{display:inline-flex;align-items:center;gap:8px;min-height:44px;margin-top:10px;font:700 13px/1 var(--pn-mono);letter-spacing:.1em;text-transform:uppercase;color:#0a0a0b;text-decoration:underline;text-underline-offset:5px}
.pn-slab-img{width:112%!important;max-width:none!important;margin:10px -6% -9% -6%;filter:drop-shadow(0 26px 28px rgba(0,0,0,.45))}
.pn-notes{display:grid;grid-template-columns:repeat(3,1fr);margin-top:clamp(64px,8vw,120px)!important;border-top:1px solid var(--pn-line2)}
.pn-notes li{padding:22px 24px 4px 0}
.pn-notes li+li{border-left:1px solid var(--pn-line);padding-left:24px}
.pn-nk{display:inline-flex;align-items:center;gap:8px;font:700 13px/1 var(--pn-mono);letter-spacing:.16em;text-transform:uppercase;color:var(--pn-y);margin-bottom:14px}
.pn-notes h3{font-size:clamp(36px,3.2vw,52px)}
.pn-notes p{margin-top:10px;color:var(--pn-mut);font-size:15px;max-width:30em}
.pn-soon .pn-nk{color:#0a0a0b;background:var(--pn-txt);padding:6px 9px}
.pn-soon .pn-nk i{width:6px;height:6px;border-radius:50%;background:#c2410c}
.pn-soon h3{color:#0c0c0d;-webkit-text-stroke:1.6px var(--pn-txt);paint-order:stroke fill;letter-spacing:.03em}
.pn-soon h3 a{color:var(--pn-txt);-webkit-text-fill-color:#0c0c0d}

/* Z2 access */
.pn-z2{background:radial-gradient(70% 80% at 50% 55%,color-mix(in srgb,var(--zc) 9%,transparent),transparent 70%),#0a0a0b}
.pn-z2-grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(200px,.62fr) minmax(0,1fr);gap:clamp(24px,3.5vw,64px);align-items:center}
.pn-readout{display:inline-flex;align-items:center;gap:14px;margin-top:34px!important;font:700 13px/1 var(--pn-mono);letter-spacing:.14em;text-transform:uppercase;border:1px solid color-mix(in srgb,var(--zc) 50%,transparent);padding:0 14px 0 0!important}
.pn-readout span{background:var(--zc);color:#04140a;padding:11px 12px}
.pn-readout b{color:var(--zc);font-weight:700}
.pn-z2-stage{--sh:clamp(400px,44vw,640px);position:relative;display:grid;place-items:center;height:var(--sh)}
.pn-z2-stage::before{content:"";position:absolute;inset:6% 0;background:radial-gradient(closest-side,color-mix(in srgb,var(--zc) 38%,transparent),color-mix(in srgb,var(--zc) 10%,transparent) 55%,transparent 72%);filter:blur(8px)}
.pn-z2-stage img{position:relative;height:calc(var(--sh)*.92)!important;width:auto!important;max-width:none!important;filter:hue-rotate(-105deg) saturate(1.5) drop-shadow(0 0 1px rgba(160,255,200,.8)) drop-shadow(0 30px 40px rgba(0,0,0,.8));animation:pn-float 7s ease-in-out infinite}
@keyframes pn-float{50%{transform:translateY(-10px)}}
.pn-ring{position:absolute;left:50%;top:27%;width:26%;aspect-ratio:1;border-radius:50%;border:1px solid var(--zc);transform:translate(-50%,-50%) scale(1);opacity:0;animation:pn-ping 4.5s cubic-bezier(.2,.6,.3,1) infinite}
.pn-ring.r2{animation-delay:1.5s}.pn-ring.r3{animation-delay:3s}
@keyframes pn-ping{0%{transform:translate(-50%,-50%) scale(.8);opacity:.9}100%{transform:translate(-50%,-50%) scale(5.2);opacity:0}}
.pn-calls{display:grid;gap:0;border-top:1px solid var(--pn-line2)}
.pn-calls li{position:relative;display:grid;grid-template-columns:auto 1fr;gap:18px;padding:20px 0;border-bottom:1px solid var(--pn-line2)}
.pn-calls li::before{content:"";position:absolute;right:100%;top:34px;width:clamp(20px,3vw,56px);height:1px;background:var(--zc);margin-right:6px}
.pn-calls li::after{content:"";position:absolute;right:calc(100% + clamp(20px,3vw,56px) + 3px);top:31px;width:7px;height:7px;border-radius:50%;background:var(--zc);box-shadow:0 0 10px var(--zc)}
.pn-cn{font:700 13px/1 var(--pn-mono);letter-spacing:.1em;color:var(--zc);padding-top:7px}
.pn-calls p{margin-top:8px;color:var(--pn-mut);font-size:15px}

/* Z3 fire */
.pn-z3{background:#120505}
.pn-z3-bg{position:absolute;inset:0;z-index:-1}
.pn-z3-bg img{width:100%!important;height:100%!important;object-fit:cover;object-position:30% 50%;filter:grayscale(1) contrast(1.15) brightness(.9)}
.pn-z3-bg::before{content:"";position:absolute;inset:0;background:#ff2a12;mix-blend-mode:multiply}
.pn-z3-bg::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(10,2,2,.95) 0%,rgba(14,3,3,.8) 44%,rgba(20,4,4,.4) 100%),linear-gradient(0deg,rgba(10,2,2,.95),transparent 40%,rgba(10,2,2,.7))}
.pn-z3-grid{display:grid;grid-template-columns:minmax(0,58fr) minmax(0,42fr);gap:clamp(24px,4vw,72px);align-items:center}
.pn-volt{font-family:var(--pn-disp);font-weight:800;font-size:clamp(150px,24vw,400px);line-height:.76;letter-spacing:-.02em;color:var(--zc);margin:0 0 clamp(20px,2.5vw,36px) -.03em!important;text-shadow:0 0 80px rgba(255,60,40,.45)}
.pn-volt span{color:#1c0706;-webkit-text-stroke:3px var(--zc);paint-order:stroke fill;margin-left:.04em;text-shadow:none}
.pn-z3 .pn-h2{max-width:13em}
.pn-lcd{margin-top:30px;max-width:600px;padding:16px 18px;background:rgba(8,0,0,.78);border:1px solid rgba(255,90,74,.45);border-left:4px solid var(--zc);font:600 13px/1.75 var(--pn-mono);letter-spacing:.06em;color:#ffd9d4;-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px)}
.pn-lcd p:first-child{color:#fff;border-bottom:1px dashed rgba(255,90,74,.45);padding-bottom:6px;margin-bottom:6px}
.pn-lcd i{display:inline-block;width:.6em;height:1.05em;margin-left:.4em;vertical-align:-.15em;background:var(--zc);animation:pn-blinkt 1s steps(2) infinite}
.pn-z3-prod{position:relative}
.pn-z3-prod::before{content:"";position:absolute;inset:8%;background:radial-gradient(closest-side,rgba(255,60,40,.55),transparent);filter:blur(30px)}
.pn-z3-prod a{display:block;position:relative}
.pn-z3-prod img{position:relative;width:100%;max-width:560px;margin:0 auto;filter:drop-shadow(0 40px 50px rgba(0,0,0,.75));transition:transform .5s var(--pn-ease)}
.pn-z3-prod a:hover img{transform:translateY(-6px) scale(1.02)}
.pn-z3-stats{display:grid;grid-template-columns:repeat(3,1fr);margin-top:clamp(48px,6vw,90px)!important;border-top:1px solid rgba(255,255,255,.28)}
.pn-z3-stats div{display:flex;flex-direction:column;padding:20px 20px 0 0}
.pn-z3-stats div+div{border-left:1px solid rgba(255,255,255,.2);padding-left:22px}
.pn-z3-stats dd{font-family:var(--pn-disp);font-weight:800;font-size:clamp(48px,6vw,104px);line-height:.9;text-transform:uppercase}
.pn-z3-stats dt{margin-top:10px;font:600 13px/1.4 var(--pn-mono);letter-spacing:.12em;text-transform:uppercase;color:#f0c9c4}
.pn-z3 .pv-envcap{bottom:10px}

/* Z4 video */
.pn-z4{background:linear-gradient(180deg,#07090d,#0a0d14)}
.pn-z4-top{display:grid;grid-template-columns:minmax(0,44fr) minmax(0,56fr);gap:clamp(24px,4vw,72px);align-items:center}
.pn-finder,.pn-feed{position:relative}
.pn-finder img{width:100%!important;aspect-ratio:16/10;object-fit:cover}
.pn-finder::after{content:"";position:absolute;inset:0;pointer-events:none;background:repeating-linear-gradient(0deg,rgba(0,0,0,.16) 0 1px,transparent 1px 3px);box-shadow:inset 0 0 0 1px color-mix(in srgb,var(--zc) 45%,transparent)}
.pn-fc{position:absolute;width:26px;height:26px;border:2px solid var(--zc);z-index:2}
.pn-fc.tl{left:-7px;top:-7px;border-right:0;border-bottom:0}.pn-fc.tr{right:-7px;top:-7px;border-left:0;border-bottom:0}
.pn-fc.bl{left:-7px;bottom:-7px;border-right:0;border-top:0}.pn-fc.br{right:-7px;bottom:-7px;border-left:0;border-top:0}
.pn-finder figcaption,.pn-feed figcaption{position:absolute;left:0;right:0;bottom:0;z-index:2;display:flex;justify-content:space-between;gap:12px;padding:12px 14px;font:700 13px/1 var(--pn-mono);letter-spacing:.12em;text-transform:uppercase;color:#fff;background:linear-gradient(0deg,rgba(0,0,0,.88),rgba(0,0,0,.5) 70%,transparent)}
.pn-finder figcaption span,.pn-feed figcaption span{display:inline-flex;align-items:center;gap:8px}
.pn-rec{width:8px;height:8px;border-radius:50%;background:var(--zc);box-shadow:0 0 10px var(--zc);animation:pn-blinkt 1.6s steps(2) infinite}
.pn-path{position:relative;margin-top:clamp(56px,7vw,110px)}
.pn-path-h{font:700 13px/1 var(--pn-mono);letter-spacing:.18em;text-transform:uppercase;color:var(--zc);margin-bottom:26px!important}
.pn-path ol{display:grid;grid-template-columns:repeat(4,1fr);gap:0}
.pn-path li{position:relative;padding:0 24px 0 0}
.pn-path-line{position:absolute;left:0;right:0;top:calc(39px + 150px + 14px);height:1px;background:repeating-linear-gradient(90deg,color-mix(in srgb,var(--zc) 70%,transparent) 0 6px,transparent 6px 12px)}
.pn-path-line i{position:absolute;left:0;top:-4px;width:100%;height:9px;animation:pn-travel 4.4s cubic-bezier(.5,0,.5,1) infinite}
.pn-path-line i::before{content:"";position:absolute;left:0;top:0;width:9px;height:9px;border-radius:50%;background:#fff;box-shadow:0 0 0 4px color-mix(in srgb,var(--zc) 35%,transparent),0 0 22px 6px var(--zc)}
@keyframes pn-travel{0%{transform:translateX(0);opacity:0}6%{opacity:1}92%{opacity:1}100%{transform:translateX(calc(100% - 9px));opacity:0}}
.pn-js .pn-zone:not(.pn-live) *,.pn-js .pn-hero:not(.pn-live) *{animation-play-state:paused!important}
.pn-pn{position:absolute;left:0;top:0;font:700 13px/1 var(--pn-mono);letter-spacing:.12em;color:var(--zc)}
.pn-pimg{height:150px;display:flex;align-items:center;justify-content:flex-start;padding-top:22px}
.pn-pimg img{max-height:118px!important;width:auto!important;max-width:86%!important;filter:drop-shadow(0 0 22px color-mix(in srgb,var(--zc) 40%,transparent)) drop-shadow(0 14px 16px rgba(0,0,0,.6))}
.pn-palarm{color:var(--zc)}.pn-palarm svg{height:96px;width:96px;filter:drop-shadow(0 0 16px color-mix(in srgb,var(--zc) 70%,transparent))}
.pn-path li h3{position:relative;margin-top:36px;font-size:clamp(28px,2.6vw,40px)}
.pn-path li h3::before{content:"";position:absolute;left:0;top:-27px;width:11px;height:11px;border-radius:50%;background:#0a0d14;border:2px solid var(--zc)}
.pn-path li p{margin-top:8px;color:var(--pn-mut);font-size:15px;max-width:22em}

/* Z5 mobile */
.pn-z5{background:radial-gradient(60% 70% at 26% 45%,color-mix(in srgb,var(--zc) 14%,transparent),transparent 70%),#0a0a0b}
.pn-z5-grid{display:grid;grid-template-columns:minmax(0,56fr) minmax(0,44fr);column-gap:clamp(24px,4vw,72px);row-gap:clamp(28px,3vw,48px);align-items:center}
.pn-z5-stage{grid-row:1/3;position:relative}
.pn-z5-stage::before{content:"";position:absolute;inset:4% 2%;background:radial-gradient(closest-side,color-mix(in srgb,var(--zc) 50%,transparent),transparent);filter:blur(40px)}
.pn-z5-stage img{position:relative;width:100%;filter:drop-shadow(0 40px 46px rgba(0,0,0,.7))}
.pn-chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:22px!important}
.pn-chips a{display:inline-flex;align-items:center;min-height:44px;padding:0 14px;border:1px solid color-mix(in srgb,var(--zc) 50%,transparent);font:700 13px/1 var(--pn-mono);letter-spacing:.08em;text-transform:uppercase;color:var(--zc);text-decoration:none}
.pn-chips a:hover{background:var(--zc);color:#0a0a0b}
.pn-plate{position:relative;border:1px solid color-mix(in srgb,var(--zc) 50%,transparent);background:linear-gradient(145deg,#1b1a22,#111116);padding:clamp(24px,2.4vw,36px)}
.pn-rivet{position:absolute;width:7px;height:7px;border-radius:50%;background:radial-gradient(circle at 35% 35%,#d9d0ff,#5b4f8a)}
.pn-rivet.a{left:10px;top:10px}.pn-rivet.b{right:10px;top:10px}.pn-rivet.c{left:10px;bottom:10px}.pn-rivet.d{right:10px;bottom:10px}
.pn-plate-k{font:700 13px/1 var(--pn-mono);letter-spacing:.18em;text-transform:uppercase;color:var(--zc)}
.pn-plate-big{display:flex;flex-wrap:wrap;align-items:baseline;gap:0 .22em;margin:14px 0 18px!important;font-family:var(--pn-disp);font-weight:800;font-size:clamp(60px,7vw,120px);line-height:.86;text-transform:uppercase}
.pn-plate-big span:last-child{color:#16151c;-webkit-text-stroke:2.4px var(--zc);paint-order:stroke fill;letter-spacing:.01em}
.pn-plate dl div{display:grid;grid-template-columns:9.5em 1fr;gap:12px;padding:10px 0;border-top:1px solid var(--pn-line);font:600 13px/1.35 var(--pn-mono);letter-spacing:.06em;text-transform:uppercase}
.pn-plate dt{color:var(--pn-mut)}.pn-plate dd{color:var(--pn-txt)}
.pn-plate-go{display:inline-flex;align-items:center;gap:8px;min-height:44px;margin-top:8px;font:700 13px/1 var(--pn-mono);letter-spacing:.1em;text-transform:uppercase;color:var(--zc);text-decoration:underline;text-underline-offset:5px}

/* Z6 dealers */
.pn-z6{background:var(--pn-y);color:#0a0a0b;border-top:0}
.pn-z6::before{content:"";position:absolute;left:0;right:0;top:0;height:10px;background:repeating-linear-gradient(90deg,#0a0a0b 0 1px,transparent 1px 12px)}
.pn-z6 .pn-zhead{color:#2d2400}
.pn-z6 .pn-ztag{color:#0a0a0b;border-color:#0a0a0b}
.pn-z6 .pn-ztag .pn-led{background:#0a0a0b;box-shadow:none}
.pn-z6 .pn-zname{color:#0a0a0b}
.pn-z6 .pn-zrule{background:repeating-linear-gradient(90deg,rgba(10,10,11,.6) 0 1px,transparent 1px 8px)}
.pn-z6-grid{display:grid;grid-template-columns:minmax(0,54fr) minmax(0,46fr);gap:clamp(24px,4vw,72px);align-items:end}
.pn-year{color:#0a0a0b;white-space:nowrap;font-family:var(--pn-disp);font-weight:800;font-size:clamp(150px,21vw,380px);line-height:.74;letter-spacing:-.02em;margin:0 0 clamp(24px,3vw,44px) -.03em!important;font-variant-numeric:tabular-nums}
.pn-z6 .pn-h2{color:#0a0a0b;max-width:13em}
.pn-z6 .pn-z6-copy>p:not(.pn-year){margin-top:22px;max-width:36em;color:#231c00;font-weight:500;font-size:clamp(16px,1.15vw,18px)}
.pn-z6-cta{display:flex;flex-wrap:wrap;gap:14px;margin-top:30px}
.pn-feed{background:#0a0a0b;box-shadow:14px 14px 0 #0a0a0b}
.pn-feed-v{position:relative;aspect-ratio:16/10;overflow:hidden}
.pn-feed-v :is(img,video){position:absolute;inset:0;width:100%!important;height:100%!important;object-fit:cover;filter:grayscale(1) contrast(1.12) brightness(.92)}
.pn-feed::after{content:"";position:absolute;inset:0;pointer-events:none;background:color-mix(in srgb,var(--pn-y) 22%,transparent);mix-blend-mode:multiply}
.pn-feed .pn-fc{border-color:var(--pn-y)}
.pn-feed .pn-fc.tl{left:12px;top:12px}.pn-feed .pn-fc.tr{right:12px;top:12px}.pn-feed .pn-fc.bl{left:12px;bottom:12px}.pn-feed .pn-fc.br{right:12px;bottom:12px}
.pn-feed figcaption{padding:14px 48px 20px}
.pn-z6-row{display:grid;grid-template-columns:repeat(4,1fr);margin-top:clamp(56px,7vw,100px)!important;border-top:2px solid #0a0a0b}
.pn-z6-row div{padding:18px 18px 0 0}
.pn-z6-row div+div{border-left:1px solid rgba(10,10,11,.35);padding-left:20px}
.pn-z6-row dt{font:700 13px/1 var(--pn-mono);letter-spacing:.16em;text-transform:uppercase;color:#2d2400;margin-bottom:10px}
.pn-z6-row dd{font-family:var(--pn-disp);font-weight:800;font-size:clamp(24px,2.2vw,34px);line-height:1;text-transform:uppercase}
.pn-z6-row a{color:inherit;text-decoration:underline;text-underline-offset:4px;text-decoration-thickness:2px}

/* ---- responsive ---- */
@media (max-width:1024px){
  .pn-hero-in{display:flex;flex-direction:column;align-items:stretch;padding-bottom:36px}
  .pn-hero-copy{display:contents}
  .pn-eyebrow{order:1}.pn-h1{order:2;font-size:min(15.4vw,132px)}.pn-hero-kp{order:3;margin-top:clamp(26px,5vw,44px)}.pn-hero-more{order:4;margin-top:30px}
  .pn-kp{max-width:640px}
  .pn-lede{margin-top:0!important;font-size:17px}
  .pn-hero-spec{grid-template-columns:repeat(2,1fr)}
  .pn-hero-spec div:nth-child(3){border-left:0;padding-left:0}
  .pn-hero-spec div:nth-child(n+3){border-top:1px solid var(--pn-line)}
  .pn-mark-br{display:none}
  .pn-z1-grid,.pn-z3-grid,.pn-z4-top,.pn-z5-grid,.pn-z6-grid{grid-template-columns:minmax(0,1fr)}
  .pn-num{font-size:min(56vw,520px)}
  .pn-z1-num,.pn-z1-copy,.pn-slab{grid-column:1;grid-row:auto}
  .pn-slab{margin-top:44px;max-width:620px}
  .pn-z2-grid{grid-template-columns:minmax(0,1fr) minmax(0,1.25fr);align-items:start}
  .pn-z2-copy{grid-column:1/-1}
  .pn-z2-stage{--sh:clamp(340px,60vw,520px);align-self:center}
  .pn-calls li::before,.pn-calls li::after{display:none}
  .pn-z3-bg::after{background:linear-gradient(0deg,rgba(10,2,2,.97) 0%,rgba(14,3,3,.84) 55%,rgba(20,4,4,.55) 100%)}
  .pn-z3-prod img{max-width:420px}
  .pn-z5-stage{grid-row:auto}
  .pn-year{font-size:min(40vw,400px)}
  .pn-feed{margin-right:14px}
  .pn-z6-row{grid-template-columns:repeat(2,1fr)}
  .pn-z6-row div:nth-child(3){border-left:0;padding-left:0}
  .pn-z6-row div:nth-child(n+3){margin-top:18px;border-top:1px solid rgba(10,10,11,.35)}
}
@media (max-width:719px){
  .pn-zmeta{display:none}
  .pn-notes,.pn-z3-stats{grid-template-columns:1fr}
  .pn-notes li+li,.pn-z3-stats div+div{border-left:0;padding-left:0;border-top:1px solid var(--pn-line);margin-top:18px}
  .pn-z3-stats div+div{border-top-color:rgba(255,255,255,.2)}
  .pn-notes li{padding-right:0}
  .pn-path ol{grid-template-columns:1fr}
  .pn-path li{display:grid;grid-template-columns:104px 1fr;column-gap:18px;align-items:center;padding:16px 0 16px 28px;border-top:1px solid var(--pn-line)}
  .pn-path-line{left:5px;right:auto;top:44px;bottom:8px;width:1px;height:auto;background:repeating-linear-gradient(0deg,color-mix(in srgb,var(--zc) 70%,transparent) 0 6px,transparent 6px 12px)}
  .pn-path-line i{left:-4px;top:0;width:9px;height:100%;animation-name:pn-travelv}
  .pn-pn{left:28px;top:14px}
  .pn-pimg{grid-row:1/3;height:96px;padding-top:14px}
  .pn-pimg img{max-height:74px!important;max-width:100%!important}
  .pn-palarm svg{width:64px;height:64px}
  .pn-path li h3{margin-top:0;align-self:end}
  .pn-path li h3::before{left:calc(-28px - 104px - 18px);top:8px}
  .pn-path li p{margin-top:4px;align-self:start}
}
@keyframes pn-travelv{0%{transform:translateY(0);opacity:0}6%{opacity:1}92%{opacity:1}100%{transform:translateY(calc(100% - 9px));opacity:0}}
@media (max-width:599px){
  .pn-zone{font-size:16px}
  .pn-kp{width:calc(100% + 12px);margin-left:-6px}
  .pn-kp-screen{grid-template-columns:1fr 40%}
  .pn-kp-info,.pn-kp-log,.pn-kp-arm{display:none}
  .pn-kp-menu{padding:0 1cqw 0 2cqw}
  .pn-kp-menu a{font-size:13px;flex:0 1 22px;min-height:0;gap:6px}
  .pn-kp-state{font-size:15px}
  .pn-kp-shield{width:27cqw}
  .pn-hero-cta .pn-btn{flex:1 1 auto;justify-content:center}
  .pn-ctl{gap:8px}.pn-key{flex:1 1 auto;padding:0 10px!important}
  .pn-eyebrow{letter-spacing:.1em}
  .pn-eyebrow i{width:18px}
  .pn-hero-spec div{grid-template-columns:1fr;padding-right:10px}
  .pn-hero-spec dd.d{margin-top:8px}
  .pn-zhead{flex-wrap:wrap}
  .pn-z2-grid{grid-template-columns:minmax(0,1fr)}
  .pn-z2-stage{--sh:380px;width:100%}
  .pn-lcd{letter-spacing:.02em;padding:14px}
  .pn-plate dl div{grid-template-columns:7.5em 1fr}
  .pn-feed figcaption{padding:12px 44px 18px;letter-spacing:.06em}
  .pn-z6-cta .pn-btn{flex:1 1 100%;justify-content:center}
  .pn-slab-img{width:104%!important;margin:10px -2% -6% -2%}
}
@media (prefers-reduced-motion:reduce){
  .pn-hero *,.pn-zone *,.pn-zb *,.pn-beat *{animation:none!important;transition-duration:.01ms!important;transition-delay:0s!important}
  .pn-js .pn-rv{opacity:1;transform:none}
  .pn-js .pn-num-f{clip-path:inset(-30% -10% -30% -10%)}
  .pn-beat-live{-webkit-mask:none!important;mask:none!important;opacity:.4!important}
  .pn-path-line i{transform:translateX(50%);opacity:1}
  .pn-ring{opacity:.35;transform:translate(-50%,-50%) scale(2.4)}
  .pn-ring.r2{transform:translate(-50%,-50%) scale(3.6);opacity:.22}.pn-ring.r3{display:none}
  .pn-sweep{display:none}
  .pn-snd{display:none!important}
}

/* ================= round 3b: tighter home, chapter rail, briefing, native modules ================= */
/* rhythm: every panel section on the home page breathes the same amount */
.pn-zone{padding:clamp(56px,6vw,96px) var(--pn-pad)}
.pn-zhead{margin-bottom:clamp(28px,3.4vw,52px)}

/* ---- chapter rail: the right-hand twin of the heartbeat (wide screens only) ---- */
.pn-ch{display:none}
@media(min-width:1320px){
  .pn-ch{display:block;position:fixed;right:0;top:0;bottom:0;width:30px;z-index:61;pointer-events:none;border-left:1px solid var(--pn-line);background:var(--pn-bk)}
  .pn-ch ol{position:absolute;right:0;top:50%;transform:translateY(-50%);margin:0;padding:0;list-style:none;pointer-events:auto}
  .pn-ch li{margin:0;padding:0}
  .pn-ch a{position:relative;display:flex;align-items:center;justify-content:center;width:30px;height:34px;text-decoration:none}
  .pn-ch a::before{content:"";position:absolute;left:50%;top:-1px;width:1px;height:calc(50% - 7px);background:var(--pn-line2)}
  .pn-ch a::after{content:"";position:absolute;left:50%;bottom:0;width:1px;height:calc(50% - 7px);background:var(--pn-line2)}
  .pn-ch li:first-child a::before,.pn-ch li:last-child a::after{content:none}
  .pn-ch a .pn-led{width:8px;height:8px;border-radius:1px}
  .pn-ch a:hover .pn-led{background:#8a8c90}
  .pn-ch a.is-on .pn-led{background:var(--pn-y);box-shadow:0 0 0 3px color-mix(in srgb,var(--pn-y) 22%,transparent),0 0 12px var(--pn-y)}
  .pn-ch a span{position:absolute;right:34px;top:50%;transform:translate(8px,-50%);white-space:nowrap;padding:8px 11px;background:#16171a;border:1px solid var(--pn-line2);font:600 13px/1 var(--pn-mono);letter-spacing:.1em;text-transform:uppercase;color:var(--pn-txt);opacity:0;visibility:hidden;transition:opacity .2s,transform .2s var(--pn-ease),visibility .2s}
  .pn-ch a span b{color:var(--pn-y);font-weight:700;margin-right:4px}
  .pn-ch a:hover span,.pn-ch a:focus span,.pn-ch a:focus-visible span{opacity:1;visibility:visible;transform:translate(0,-50%)}
  .pn-ch a:focus-visible{outline:2px solid var(--pn-y);outline-offset:-3px}
  .pn-ch-tag{position:absolute;left:50%;bottom:18px;transform:translateX(-50%);writing-mode:vertical-rl;font:600 13px/1 var(--pn-mono);letter-spacing:.16em;text-transform:uppercase;color:var(--pn-mut);white-space:nowrap}
  .pn-ch-tag b{color:var(--pn-y);font-weight:700}.pn-ch-tag em{font-style:normal}
}
@media(min-width:1320px) and (max-height:620px){.pn-ch-tag{display:none}}

/* ---- briefing: news and guides as one readout ---- */
.pn-brief{position:relative;padding:clamp(56px,6vw,96px) var(--pn-pad);border-top:1px solid var(--pn-line);background:var(--pn-ink);color:var(--pn-txt);font-family:var(--q-sans)}
.pn-brief :where(p,h2,h3,h4,ol){margin:0;padding:0}.pn-brief ol{list-style:none}
.pn-bin{max-width:1560px;margin:0 auto}
.pn-bhead{margin-bottom:clamp(24px,3vw,40px)}
.pn-beb{display:flex;align-items:center;gap:12px;font:600 13px/1 var(--pn-mono);letter-spacing:.16em;text-transform:uppercase;color:var(--pn-y)}
.pn-beb::before{content:"";width:28px;height:1px;background:var(--pn-y)}
.pn-brief .pn-h2{font-family:var(--pn-disp);font-weight:800;font-size:clamp(40px,4.5vw,72px);line-height:.94;text-transform:uppercase;color:var(--pn-txt)}
.pn-bgrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:clamp(28px,4vw,72px)}
.pn-bcol{border-top:2px solid var(--pn-txt);padding-top:16px}
.pn-bk{display:flex;align-items:center;gap:10px;font:600 13px/1 var(--pn-mono);letter-spacing:.16em;text-transform:uppercase;color:var(--pn-mut)}
.pn-bk .pn-led{background:var(--pn-y);box-shadow:0 0 10px var(--pn-y)}
.pn-bcol h3{margin-top:12px;font-family:var(--pn-disp);font-weight:700;font-size:clamp(24px,2.2vw,32px);line-height:1.05;text-transform:uppercase;color:var(--pn-txt)}
.pn-bcol ol{margin-top:18px}
.pn-bcol li{display:grid;grid-template-columns:44px minmax(0,1fr);gap:0 8px;padding:18px 0;border-top:1px solid var(--pn-line2)}
.pn-bn{font:700 13px/1.5 var(--pn-mono);letter-spacing:.08em;color:var(--pn-y)}
.pn-bt{font:600 13px/1.5 var(--pn-mono);letter-spacing:.1em;text-transform:uppercase;color:var(--pn-mut)}
.pn-bcol h4{margin-top:6px;font-family:var(--q-sans);font-size:19px;line-height:1.3;font-weight:700;letter-spacing:0;text-transform:none}
.pn-bcol h4 a{display:inline-block;padding:4px 0;color:var(--pn-txt);text-decoration:none;background:linear-gradient(var(--pn-y),var(--pn-y)) 0 100%/0 2px no-repeat;transition:background-size .35s var(--pn-ease),color .2s}
.pn-bcol h4 a:hover{color:var(--pn-y);background-size:100% 2px}
.pn-bcol h4 a:focus-visible{outline:2px solid var(--pn-y);outline-offset:3px}
.pn-bcol li p:last-child{margin-top:6px;font-size:15px;line-height:1.5;color:var(--pn-mut);max-width:44em}
@media(max-width:899px){.pn-bgrid{grid-template-columns:minmax(0,1fr)}.pn-bcol h4 a{padding:10px 0}}
@media(prefers-reduced-motion:reduce){.pn-ch *,.pn-brief *{transition-duration:.01ms!important}}

/* chapter links land like zone links: flush under the header and zone bar */
html.pn-home[data-dir="showcase"] :is(main > .q-section,.pn-brief,.pn-scenes,.pn-zone){scroll-margin-top:-70px}
@media(max-width:767px){html.pn-home[data-dir="showcase"] :is(main > .q-section,.pn-brief,.pn-scenes,.pn-zone){scroll-margin-top:-32px}}
html.pn-home[data-dir="showcase"] .pn-hero{scroll-margin-top:600px}
html[data-dir="showcase"] .pv-contact a.q-btn{color:#0a0a0b!important}

/* ================= dial-back: DMP's own look on the panel pieces ================= */
/* ---- hero: stays dark and cinematic; the headline keeps Barlow Condensed, everything else is the site's own type ---- */
.pn-hero-grid{background:radial-gradient(60% 55% at 72% 46%,color-mix(in srgb,var(--pn-st) 12%,transparent),transparent 70%),radial-gradient(50% 60% at 8% 0%,rgba(255,255,255,.05),transparent 70%);-webkit-mask:none;mask:none;opacity:1}
.pn-mark{display:none}
.pn-eyebrow{font:700 13px/1.2 var(--q-sans);letter-spacing:.2em;color:var(--pn-y)}
.pn-eyebrow i{width:10px;height:10px;border-radius:50%}
.pn-eyebrow span{color:rgba(255,255,255,.5)}
.pn-lane{font:600 15px/1.2 var(--q-sans);letter-spacing:0;text-transform:none}
.pn-lane a{color:#d6d5cf}
.pn-hero-spec dt{font:700 13px/1 var(--q-sans);letter-spacing:.16em}
.pn-hero-spec dd:not(.d){font-family:var(--pn-head);font-weight:800;font-size:clamp(30px,2.8vw,44px);line-height:1;letter-spacing:-.03em;text-transform:none}
.pn-hero-spec dd.d{font:500 14px/1.4 var(--q-sans);letter-spacing:0;text-transform:none;color:#c9c8c1}
.pn-key{border-radius:999px;font:600 14px/1 var(--q-sans)!important;letter-spacing:0;text-transform:none;padding:0 18px!important}
.pn-kp-hint{font:600 14px/1.4 var(--q-sans);letter-spacing:0;text-transform:none}
.pn-kp-demo{font:500 13px/1.4 var(--q-sans);letter-spacing:0}

/* ---- zones: light grounds (Z3 fire stays a dark scene, Z6 dealers stays DMP yellow) ---- */
.pn-zone:not(.pn-z3):not(.pn-z6),.pn-brief{--pn-bk:#fff;--pn-ink:#f6f6f3;--pn-txt:#0b0c0e;--pn-mut:#54575e;--pn-line:rgba(10,12,16,.1);--pn-line2:rgba(10,12,16,.2);background:#fff;color:#0b0c0e}
.pn-z1{--zi:#6f5500}.pn-z2{--zi:#0b6b3a}.pn-z4{--zi:#0f5bb5}.pn-z5{--zi:#5a3fd0}
.pn-zone.pn-z2,.pn-zone.pn-z5{--pn-bk:#f6f6f3}
.pn-zone:not(.pn-z3) :focus-visible,.pn-brief :focus-visible{outline-color:#0a0a0b}
.pn-zhead{font:700 13px/1 var(--q-sans);letter-spacing:.16em}
.pn-ztag{color:var(--zi);border-radius:999px;border-color:color-mix(in srgb,var(--zi) 40%,transparent);background:color-mix(in srgb,var(--zc) 12%,transparent);padding:8px 14px}
.pn-ztag .pn-led{box-shadow:inset 0 0 0 1px rgba(0,0,0,.25)}
.pn-z3 .pn-ztag .pn-led{box-shadow:0 0 10px var(--zc)}
.pn-zrule{height:1px;background:var(--pn-line2)}
.pn-zone .pn-h2{font-family:var(--pn-head);font-weight:800;font-size:clamp(32px,3.5vw,54px);line-height:1.06;letter-spacing:-.03em;text-transform:none}
.pn-zone .pn-h2 em{color:var(--zi)}
.pn-zone .pn-h2+p{color:color-mix(in srgb,var(--pn-txt) 80%,transparent)}
.pn-zone h3{font-family:var(--pn-head);font-weight:800;font-size:22px;letter-spacing:-.02em;line-height:1.15;text-transform:none}
/* Z1 */
.pn-zone.pn-z1{background:#fff}
.pn-num-o{color:#fff;-webkit-text-stroke:3px #0a0a0b}
.pn-num-f{color:#0a0a0b}
.pn-num-unit{font:700 clamp(13px,1.2vw,16px)/1 var(--q-sans);letter-spacing:.2em}
.pn-num-unit b{color:var(--pn-txt)}
.pn-num-plus{color:var(--zi)}
.pn-slab{border-radius:24px;box-shadow:0 30px 70px rgba(10,12,16,.16)}
.pn-slab::before{content:none}
.pn-slab-h{font:700 13px/1 var(--q-sans);padding-top:4px!important}
.pn-slab dt{font:600 14px/1.2 var(--q-sans);letter-spacing:0;text-transform:none}
.pn-slab dd{font-family:var(--pn-head);font-size:clamp(20px,1.7vw,26px);letter-spacing:-.02em;line-height:1.1}
.pn-slab-go{font:700 15px/1 var(--q-sans);letter-spacing:0;text-transform:none}
.pn-slab-img{filter:drop-shadow(0 26px 28px rgba(0,0,0,.3))}
.pn-nk{font:700 13px/1 var(--q-sans);color:var(--zi)}
.pn-notes h3{font-size:clamp(26px,2.3vw,34px)}
.pn-soon .pn-nk{color:#fff;background:#0b0c0e;border-radius:999px;padding:7px 12px}
.pn-soon .pn-nk i{background:#ff9d2e}
.pn-soon h3{color:var(--pn-txt);-webkit-text-stroke:0;letter-spacing:-.02em}
.pn-soon h3 a{-webkit-text-fill-color:currentColor}
/* Z2 */
.pn-zone.pn-z2{background:radial-gradient(70% 80% at 50% 55%,color-mix(in srgb,var(--zc) 12%,transparent),transparent 70%),#f6f6f3}
.pn-readout{border-radius:999px;overflow:hidden;font:700 13px/1 var(--q-sans);background:#fff}
.pn-readout b{color:var(--zi)}
.pn-z2-stage img{filter:hue-rotate(-105deg) saturate(1.5) drop-shadow(0 30px 34px rgba(0,0,0,.3))}
.pn-cn{color:var(--zi)}
/* Z3: the one dark zone */
.pn-z3-stats dd{font-family:var(--pn-head);font-size:clamp(38px,4.4vw,68px);line-height:1;letter-spacing:-.03em;text-transform:none}
.pn-z3-stats dt{font:600 14px/1.4 var(--q-sans);letter-spacing:0;text-transform:none}
/* Z4 */
.pn-zone.pn-z4{background:#fff}
.pn-finder{border-radius:16px}
.pn-finder img,.pn-finder::after{border-radius:16px}
.pn-finder figcaption{border-radius:0 0 16px 16px}
.pn-finder,.pn-z4 .pn-fc{--zc:#4aa3ff}
.pn-z4 .pn-fc{border-color:var(--zi)}
.pn-path-h{font:700 13px/1 var(--q-sans);color:var(--zi)}
.pn-pn{color:var(--zi)}
.pn-pimg img{filter:drop-shadow(0 14px 16px rgba(0,0,0,.22))}
.pn-palarm{color:var(--zi)}.pn-palarm svg{filter:none}
.pn-path li h3{font-size:clamp(20px,1.8vw,26px)}
.pn-path li h3::before{background:var(--pn-bk);border-color:var(--zi)}
.pn-path-line{background:repeating-linear-gradient(90deg,var(--zi) 0 6px,transparent 6px 12px);opacity:.7}
.pn-path-line i::before{background:var(--zi);box-shadow:0 0 0 4px color-mix(in srgb,var(--zc) 35%,transparent)}
/* Z5 */
.pn-zone.pn-z5{background:radial-gradient(60% 70% at 26% 45%,color-mix(in srgb,var(--zc) 16%,transparent),transparent 70%),#f6f6f3}
.pn-z5-stage img{filter:drop-shadow(0 30px 40px rgba(0,0,0,.28))}
.pn-chips a{border-radius:999px;padding:0 18px;font:600 15px/1 var(--q-sans);letter-spacing:0;text-transform:none;color:var(--zi);background:#fff;border-color:color-mix(in srgb,var(--zi) 40%,transparent)}
.pn-chips a:hover{background:var(--zi);border-color:var(--zi);color:#fff}
.pn-plate{background:#fff;border:1px solid var(--pn-line);border-radius:24px;box-shadow:0 24px 60px rgba(10,12,16,.1)}
.pn-rivet{display:none}
.pn-plate-k{font:700 13px/1 var(--q-sans);color:var(--zi)}
.pn-plate-big{font-family:var(--pn-head);font-size:clamp(40px,4.4vw,68px);line-height:1;letter-spacing:-.03em;text-transform:none}
.pn-plate-big span:last-child{color:var(--zi);-webkit-text-stroke:0;letter-spacing:-.03em}
.pn-plate dl div{font:500 15px/1.4 var(--q-sans);letter-spacing:0;text-transform:none}
.pn-plate dd{font-weight:600}
.pn-plate-go{font:700 15px/1 var(--q-sans);letter-spacing:0;text-transform:none;color:var(--zi)}
/* Z6 */
.pn-z6::before{content:none}
.pn-z6 .pn-ztag{background:transparent}
.pn-feed{border-radius:24px;overflow:hidden;box-shadow:0 30px 70px rgba(0,0,0,.3)}
.pn-z6-row dt{font:700 13px/1 var(--q-sans)}
.pn-z6-row dd{font-family:var(--pn-head);font-size:clamp(18px,1.5vw,22px);letter-spacing:-.02em;line-height:1.2;text-transform:none}
@media(max-width:719px){.pn-zone:not(.pn-z3) :is(.pn-notes li+li){border-top-color:var(--pn-line)}}
/* ---- briefing (news and guides): a light band ---- */
.pn-brief{background:#f6f6f3}
.pn-beb{font:700 13px/1.2 var(--q-sans);letter-spacing:.2em;color:#6f5500;margin-bottom:14px!important}
.pn-beb::before{width:10px;height:10px;border-radius:50%}
.pn-brief .pn-h2{font-family:var(--pn-head);font-size:clamp(32px,3.5vw,54px);line-height:1.06;letter-spacing:-.03em;text-transform:none}
.pn-bk{font:700 13px/1 var(--q-sans)}
.pn-bk .pn-led{box-shadow:inset 0 0 0 1px rgba(0,0,0,.25)}
.pn-bcol h3{font-family:var(--pn-head);font-weight:800;font-size:clamp(22px,1.9vw,28px);line-height:1.15;letter-spacing:-.02em;text-transform:none}
.pn-bn{color:#6f5500}
.pn-bt{font:700 13px/1.5 var(--q-sans)}
.pn-bcol h4 a:hover{color:var(--pn-txt)}
.pn-bcol h4 a:focus-visible{outline-color:#0a0a0b}
/* ---- chapter rail: a small floating pager on wide screens (it crosses light and dark bands, so it carries its own ground) ---- */
@media(min-width:1320px){
  .pn-ch{top:50%;bottom:auto;right:10px;width:30px;transform:translateY(-50%);padding:6px 0;border:1px solid rgba(10,12,16,.14);border-radius:999px;background:rgba(255,255,255,.94);box-shadow:0 10px 28px rgba(10,12,16,.16)}
  .pn-ch ol{position:static;transform:none}
  .pn-ch a{width:28px;height:26px}
  .pn-ch a::before,.pn-ch a::after{content:none}
  .pn-ch a .pn-led{border-radius:50%;background:#c3c5ca;box-shadow:none}
  .pn-ch a:hover .pn-led{background:#6b6e75}
  .pn-ch a.is-on .pn-led{background:#0a0a0b;box-shadow:0 0 0 3px var(--pn-y)}
  .pn-ch a span{right:36px;background:#0b0c0e;border:0;border-radius:8px;font:600 13px/1 var(--q-sans);letter-spacing:0;text-transform:none;color:#fff}
  .pn-ch a:focus-visible{outline-color:#0a0a0b;outline-offset:-2px;border-radius:50%}
  .pn-ch-tag{display:none}
}
/* ---- tools (configurator, keypad demo, product wall): the site's own type and rounding ---- */
html[data-dir="showcase"] body .tk-h2{font-family:var(--pn-head);font-weight:800;text-transform:none;letter-spacing:-.02em;font-size:clamp(22px,2vw,28px)}
html[data-dir="showcase"] body :is(.tk-btn,.tk-printbtn){border-radius:999px;font-family:var(--q-sans);font-size:15px;letter-spacing:0;text-transform:none}
html[data-dir="showcase"] body .tk-wf{border-radius:999px;font:600 14px/1 var(--q-sans);letter-spacing:0;text-transform:none}
html[data-dir="showcase"] body .tk-wsoon{border-radius:999px;padding:5px 10px}
/* modules that were tuned for the all-dark pass: decorative numerals on light bands, the eyebrow on the dark product wall */
html[data-dir="showcase"] .bignum{opacity:1!important;color:#85878d!important}
html[data-dir="showcase"] .lf-dark .bignum{color:#9a9ca1!important}
html[data-dir="showcase"] body .tk-wall .q-eyebrow{color:var(--pn-y)}
"""

CLEAN_CSS = r"""
/* ============================================================ CLEAN: SWISS SPEC SHEET ============================================================ */
html[data-dir="clean"]{--pn-mono:'JetBrains Mono',ui-monospace,'SFMono-Regular',Menlo,Consolas,'Liberation Mono',monospace;--cl-line:#d5d9df;--cl-ink:#0b0d10;--cl-blue:#1d4ed8;
  --bg:#ffffff;--bg-alt:#f4f5f6;--card:#ffffff;--border:#d5d9df;--fg:#0b0d10;--fg-muted:#4a5160;--radius:0px}
html[data-dir="clean"] body{background:#fff}
/* type: tight grotesque headings, mono micro labels, tabular numerals */
html[data-dir="clean"] :is(.q-h1,.q-h2){letter-spacing:-.035em}
html[data-dir="clean"] .q-eyebrow{font-family:var(--pn-mono);font-size:13px;font-weight:600;letter-spacing:.12em;gap:10px}
html[data-dir="clean"] main{counter-reset:clsec}
html[data-dir="clean"] main > .q-section{counter-increment:clsec}
html[data-dir="clean"] main > .q-section .q-eyebrow::before{content:counter(clsec,decimal-leading-zero);width:auto;height:auto;background:none;border-radius:0;font-weight:700;color:inherit;padding-right:10px;border-right:1px solid currentColor}
html[data-dir="clean"] :is(.pv-stat b,.pv-hero-stats b,.lf-spec-c dd,.lf-chip b,.pp-cmp-v,table td,table th){font-variant-numeric:tabular-nums}
html[data-dir="clean"] :is(.pv-hero-stats span,.lf-spec-c dt,.lf-chip span,.lf-find > span,.lf-tile .k,.pv-crumbs ol,.pv-cap,.pv-post .tag,.pv-metric .k){font-family:var(--pn-mono);letter-spacing:.08em}
/* squared, hairline components: no shadows, no pills */
html[data-dir="clean"] :is(.q-btn,.q-header .q-booknow,.q-mnav-cta,.q-form .hs-button,.pp-btn){border-radius:0}
html[data-dir="clean"] .q-btn{box-shadow:none;border:1px solid var(--cl-ink)}
html[data-dir="clean"] :is(.q-card,.lf-spec-c,.lf-tile,.q-form,.pv-detail-img){box-shadow:none;border:1px solid var(--cl-line)}
html[data-dir="clean"] .q-card:hover{border-color:var(--cl-ink)}
html[data-dir="clean"] .q-form :is(input,select,textarea){border-radius:0}
/* light bands: tick ruler along the top edge, hairline between bands */
html[data-dir="clean"] main > .q-section:not(.lf-dark):not(.pv-lh):not(.pp-closer):not(.pv-tl-stage){border-top:1px solid var(--cl-line);background-image:repeating-linear-gradient(90deg,#b9bfc8 0 1px,transparent 1px 12px);background-size:100% 6px;background-repeat:no-repeat}
html[data-dir="clean"] .q-bg-alt:not(.lf-dark){background-color:var(--bg-alt)}
/* dark plates: graphite with a blueprint grid */
html[data-dir="clean"] .lf-dark{background-color:#12151a;background-image:linear-gradient(rgba(255,255,255,.045) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.045) 1px,transparent 1px);background-size:48px 48px}
html[data-dir="clean"] .pv-lh{--lh-bg:#0d1014}
/* header: hairline, mono utility row */
html[data-dir="clean"] .q-header{border-bottom:1px solid var(--cl-ink)}
html[data-dir="clean"] .pv-util a{font-family:var(--pn-mono);letter-spacing:.02em}
html[data-dir="clean"] .pv-crumbs ol{text-transform:uppercase;font-size:13px}
/* home hero: product grid with the finder, drawn like a spec sheet */
html[data-dir="clean"] .lf-hg{background:#fff;background-image:linear-gradient(var(--cl-line) 1px,transparent 1px),linear-gradient(90deg,var(--cl-line) 1px,transparent 1px);background-size:100% 96px,96px 100%;-webkit-mask:none}
html[data-dir="clean"] .lf-hg-wrap{position:relative}
html[data-dir="clean"] .lf-hg-wrap > div:first-child{background:#fff;padding:26px 28px 28px 0;box-shadow:-40px 0 0 #fff}
html[data-dir="clean"] .lf-hg .q-h1{font-size:clamp(44px,5vw,76px);line-height:.98}
html[data-dir="clean"] .lf-find a{border-radius:0;border-color:var(--cl-ink);font-family:var(--pn-mono);font-size:13px;letter-spacing:.04em;text-transform:uppercase;font-weight:600}
html[data-dir="clean"] .lf-hg-grid{gap:0;border:1px solid var(--cl-ink);background:#fff}
html[data-dir="clean"] .lf-tile{border-radius:0;border:0;outline:1px solid var(--cl-line);outline-offset:-1px;box-shadow:none;background:#fff}
html[data-dir="clean"] .lf-tile:hover{transform:none;outline-color:var(--cl-ink);box-shadow:none;z-index:1}
html[data-dir="clean"] .lf-tile:first-child{background:#f4f5f6;color:var(--cl-ink);outline-color:var(--cl-ink)}
html[data-dir="clean"] .lf-tile:first-child .t{background:none}
html[data-dir="clean"] .lf-tile:first-child .k{color:var(--accent-ink)}
html[data-dir="clean"] .lf-tile .t{background:none;border-top:1px solid var(--cl-line)}
html[data-dir="clean"] .lf-tile img{filter:none}
/* dimension lines on the hero product */
html[data-dir="clean"] .lf-tile:first-child::before{content:"";position:absolute;left:9%;right:9%;top:22px;height:11px;border-left:1px solid var(--cl-blue);border-right:1px solid var(--cl-blue);background:linear-gradient(var(--cl-blue),var(--cl-blue)) 0 50%/100% 1px no-repeat;z-index:1}
html[data-dir="clean"] .lf-tile:first-child::after{content:"";position:absolute;left:18px;top:12%;bottom:34%;width:11px;border-top:1px solid var(--cl-blue);border-bottom:1px solid var(--cl-blue);background:linear-gradient(var(--cl-blue),var(--cl-blue)) 50% 0/1px 100% no-repeat;z-index:1}
html[data-dir="clean"] .lf-tile[href*="xr550"],html[data-dir="clean"] .lf-tile[href*="xt75"]{box-shadow:inset 0 3px 0 #ffd23d}
html[data-dir="clean"] .lf-tile[href*="digital-key"]{box-shadow:inset 0 3px 0 #2fd47a}
html[data-dir="clean"] .lf-tile[href*="xf6"]{box-shadow:inset 0 3px 0 #ff5a4d}
html[data-dir="clean"] .lf-tile[href*="virtual-keypad"]{box-shadow:inset 0 3px 0 #9b87ff}
/* stats: a ruled data row */
html[data-dir="clean"] .pv-hero-stats{border-top:1px solid var(--cl-ink)}
html[data-dir="clean"] .pv-hero-stats b{font-size:44px;letter-spacing:-.04em}
/* spec cells and chips: system colour as a thin top rule */
html[data-dir="clean"] .lf-spec-c{border-radius:0}
html[data-dir="clean"] .lf-spec-c::before{background:var(--sys)}
html[data-dir="clean"] .lf-chip{border-radius:0}
html[data-dir="clean"] .pv-faq summary{font-weight:700}
@media(max-width:1024px){html[data-dir="clean"] .lf-hg-wrap > div:first-child{padding-right:0}}
@media(max-width:767px){html[data-dir="clean"] .lf-hg{background-size:100% 64px,64px 100%}}
"""

PRESS_CSS = r"""
/* ============================================================ PRESS: EDITORIAL MAGAZINE ============================================================ */
html[data-dir="press"]{--q-serif:'Playfair Display','Playfair Fallback',Georgia,'Times New Roman',serif;--pr-ink:#17140f}
html[data-dir="press"] :is(.q-h1,.q-h2){font-family:var(--q-serif);font-weight:600;letter-spacing:-.012em;line-height:1.04}
html[data-dir="press"] .q-h1{font-size:clamp(46px,5.6vw,88px)}
html[data-dir="press"] .q-h2{font-size:clamp(34px,3.6vw,54px)}
html[data-dir="press"] :is(.q-h1,.q-h2) em{font-style:italic;font-weight:500}
html[data-dir="press"] .pv-lh.lf-tight .q-h1,html[data-dir="press"] .lf-ps .q-h1{font-size:clamp(42px,4.8vw,72px);line-height:1.04}
html[data-dir="press"] .lf-hp-head .q-h1{font-size:clamp(48px,6.4vw,104px);line-height:.96;max-width:13ch}
html[data-dir="press"] .q-lead{font-family:var(--q-serif);font-weight:400}
html[data-dir="press"] .pv-lh .q-lead{font-family:var(--q-sans);font-size:18px}
html[data-dir="press"] .q-eyebrow{letter-spacing:.24em;font-size:13px}
html[data-dir="press"] .lf-hp-mast span{font-size:13px}
/* rules: a double rule opens every light band */
html[data-dir="press"] main > .q-section:not(.lf-dark):not(.pv-lh):not(.pp-closer):not(.pv-tl-stage):not(.lf-hp):not(.pnf) > .q-container{position:relative}
html[data-dir="press"] main > .q-section:not(.lf-dark):not(.pv-lh):not(.pp-closer):not(.pv-tl-stage):not(.lf-hp):not(.pnf) > .q-container::before{content:"";position:absolute;left:40px;right:40px;top:-56px;border-top:3px double var(--fg)}
/* dark bands in warm ink, not navy */
html[data-dir="press"] .lf-dark{background:#17140f}
html[data-dir="press"] .pv-lh{--lh-bg:#14110c}
/* covers: full-bleed photograph, serif headline, the lead reads like a standfirst */
html[data-dir="press"] .pv-lh .bg.env img{opacity:.9}
html[data-dir="press"] .pv-lh .q-container{padding-top:120px;padding-bottom:110px}
html[data-dir="press"] .pv-lh .q-eyebrow{border-top:1px solid rgba(255,255,255,.6);padding-top:12px}
/* drop cap on the long-form bands */
html[data-dir="press"] .pv-detail .q-lead::first-letter{font-family:var(--q-serif);float:left;font-size:3.5em;line-height:.82;padding:.06em .1em 0 0;font-weight:600;color:var(--accent-ink)}
/* feature story */
.pnf{padding:0!important;border-bottom:1px solid var(--fg)}
.pnf-cover{position:relative;min-height:min(78vh,720px);display:flex;align-items:flex-end;overflow:hidden;background:#14110c;color:#fff}
.pnf-cover img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.pnf-cover::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(12,10,7,.5) 0%,rgba(12,10,7,.16) 34%,rgba(12,10,7,.9) 100%),linear-gradient(90deg,rgba(12,10,7,.72),rgba(12,10,7,.1) 70%)}
.pnf-over{position:relative;z-index:1;width:100%;padding:120px 0 64px}
.pnf-k{margin:0 0 18px;font:700 13px/1 var(--q-sans);letter-spacing:.24em;text-transform:uppercase;color:#ffd23d}
.pnf-k span{color:#fff;margin-left:14px;padding-left:14px;border-left:1px solid rgba(255,255,255,.6)}
.pnf .pnf-h{color:#fff;font-size:clamp(40px,5.2vw,84px);line-height:1;max-width:16ch;margin:0}
.pnf-q{margin:34px 0 0;max-width:640px;border-left:3px solid #ffd23d;padding-left:22px}
.pnf-q p{margin:0;font-family:var(--q-serif);font-style:italic;font-size:clamp(20px,2vw,28px);line-height:1.35;color:#fff}
.pnf-q footer{margin-top:12px;font:600 13px/1.3 var(--q-sans);letter-spacing:.14em;text-transform:uppercase;color:#e9e4d8}
.pnf > .q-container{padding-top:44px;padding-bottom:64px}
.pnf-intro{margin:0 0 26px;font:700 13px/1 var(--q-sans);letter-spacing:.22em;text-transform:uppercase;color:var(--fg-muted);border-top:3px double var(--fg);padding-top:14px}
.pnf-cols{list-style:none;margin:0;padding:0;columns:3;column-gap:44px;column-rule:1px solid var(--border)}
.pnf-cols li{break-inside:avoid;padding:0 0 26px}
.pnf-cols .y{display:block;font-family:var(--q-serif);font-style:italic;font-size:34px;line-height:1;color:var(--accent-ink)}
.pnf-cols h3{margin:8px 0 6px;font-family:var(--q-serif);font-size:22px;font-weight:600;line-height:1.2;color:var(--fg)}
.pnf-cols p{margin:0;font-size:16px;line-height:1.65;color:var(--fg-muted)}
.pnf-more{margin:8px 0 0}
.pnf-more a{display:inline-flex;align-items:center;min-height:44px;font-weight:700;color:var(--fg);text-decoration:underline;text-underline-offset:5px}
@media(max-width:1024px){.pnf-cols{columns:2}}
@media(max-width:767px){.pnf-cols{columns:1}.pnf-over{padding:90px 0 44px}.pnf-cover{min-height:560px}
  html[data-dir="press"] main > .q-section:not(.lf-dark):not(.pv-lh):not(.pp-closer):not(.pv-tl-stage):not(.lf-hp):not(.pnf) > .q-container::before{left:20px;right:20px;top:-34px}
  html[data-dir="press"] .pv-lh .q-container{padding-top:64px;padding-bottom:64px}}
"""

PANEL_JS = r"""
(function(){
'use strict';
var root=document.documentElement;
if(root.getAttribute('data-dir')!=='showcase')return;
var reduce=window.matchMedia('(prefers-reduced-motion: reduce)');
function $(s,c){return (c||document).querySelector(s)}
function $$(s,c){return Array.prototype.slice.call((c||document).querySelectorAll(s))}

/* heartbeat: count check-ins, pause with the tab */
var live=$('.pn-beat-live'),count=$('[data-pn-beat]'),n=1;
if(live&&count){live.addEventListener('animationiteration',function(){n+=1;count.textContent='CHECK-IN '+('000'+n).slice(-4)})}
document.addEventListener('visibilitychange',function(){root.classList.toggle('pn-hidden',document.hidden)});

/* zone bar on inner pages: bring the current system into view on phones */
var cur=$('.pn-zb:not(.pn-zb-home) a.is-on');
if(cur&&cur.scrollIntoView&&window.matchMedia('(max-width:767px)').matches){var zb=cur.closest('.pn-zb');zb.scrollLeft=Math.max(0,cur.offsetLeft-16)}

var kp=$('#pn-kp');
if(!kp)return;

/* ---------- clock ---------- */
function p2(v){return (v<10?'0':'')+v}
function stamp(){var d=new Date();return p2(d.getHours())+':'+p2(d.getMinutes())+':'+p2(d.getSeconds())}
function tick(){var d=new Date(),h=d.getHours(),m=d.getMinutes(),days=['SUN','MON','TUE','WED','THU','FRI','SAT'];
  var a=$('[data-pn-day]'),b=$('[data-pn-time]');if(a)a.textContent=days[d.getDay()];if(b)b.textContent=((h%12)||12)+':'+p2(m)+(h<12?' AM':' PM')}
tick();var clock=setInterval(tick,20000);

/* ---------- sound: off by default, WebAudio, no assets ---------- */
var ctx=null,soundOn=false,snd=$('[data-pn-sound]');
function beep(freq,at,dur,vol,type){
  if(!soundOn||!ctx||reduce.matches)return;
  var t=ctx.currentTime+(at||0),o=ctx.createOscillator(),g=ctx.createGain();
  o.type=type||'sine';o.frequency.value=freq;
  g.gain.setValueAtTime(0.0001,t);g.gain.exponentialRampToValueAtTime(vol||0.06,t+0.012);g.gain.exponentialRampToValueAtTime(0.0001,t+dur);
  o.connect(g);g.connect(ctx.destination);o.start(t);o.stop(t+dur+0.02);
}
if(snd){snd.addEventListener('click',function(){
  soundOn=!soundOn;
  if(soundOn&&!ctx){var AC=window.AudioContext||window.webkitAudioContext;if(AC){try{ctx=new AC()}catch(e){ctx=null}}}
  if(ctx&&ctx.state==='suspended'){ctx.resume()}
  snd.setAttribute('aria-pressed',String(soundOn));
  var t=$('[data-pn-sndtxt]',snd);if(t)t.textContent=soundOn?'Sound on':'Sound off';
  beep(1320,0,0.09);
})}

/* ---------- arm / disarm ---------- */
var EXIT=3,state='armed',timer=null,left=0;
var toggles=$$('[data-pn-toggle]'),shield=$('.pn-kp-shield'),labels=$$('[data-pn-label]'),armtxt=$$('[data-pn-armtxt]');
var headline=$('[data-pn-headline]'),status=$('[data-pn-status]'),zst=$$('[data-pn-zst]'),hint=$('[data-pn-hint]'),logline=$('[data-pn-logline]'),invite=$('[data-pn-invite]');
var list=$('[data-pn-events-list]'),events=[];
function log(msg){
  events.unshift([stamp(),msg]);events=events.slice(0,6);
  if(logline)logline.textContent=events[0][0]+'  '+msg;
  if(list){list.textContent='';events.forEach(function(e){var li=document.createElement('li'),b=document.createElement('b'),s=document.createElement('span');b.textContent=e[0];s.textContent=e[1];li.appendChild(b);li.appendChild(s);list.appendChild(li)})}
}
function say(t){if(hint)hint.textContent=t}
function paint(s){
  state=s;root.setAttribute('data-pn',s);
  var word=s==='armed'?'ARMED':s==='arming'?'ARMING '+left:'DISARMED';
  labels.forEach(function(el){el.textContent=word});
  if(headline)headline.textContent=s==='armed'?'Armed.':s==='arming'?'Arming.':'Disarmed.';
  if(shield){shield.setAttribute('aria-pressed',String(s==='armed'));shield.setAttribute('aria-label',s==='armed'?'Site armed. Press to disarm':s==='arming'?'Arming. Press to cancel':'Site disarmed. Press to arm')}
  armtxt.forEach(function(b){b.textContent=s==='armed'?'Disarm':s==='arming'?'Cancel':'Arm all'});
  if(status)status.textContent=s==='armed'?'Secure':s==='arming'?'Arming':'Ready';
  zst.forEach(function(el){el.textContent=s==='armed'?'Secure':s==='arming'?'Arming':'Bypassed'});
  if(invite)invite.textContent=s==='armed'?'Disarm it, then arm it again.':s==='arming'?'Exit delay running.':'Arm it.';
}
function sweep(){
  if(reduce.matches)return;
  var el=document.createElement('i');el.className='pn-sweep';el.setAttribute('aria-hidden','true');document.body.appendChild(el);
  el.addEventListener('animationend',function(){el.remove()});
}
function thunk(){if(reduce.matches)return;root.classList.remove('pn-thunk');void kp.offsetWidth;root.classList.add('pn-thunk');setTimeout(function(){root.classList.remove('pn-thunk')},600)}
function finishArm(){
  if(timer){clearInterval(timer);timer=null}left=0;
  paint('armed');log('All zones armed. Supervised.');say('Site armed. Six zones supervised.');
  beep(880,0,0.1);beep(1320,0.11,0.22,0.07);sweep();thunk();
}
function arm(){
  if(reduce.matches){finishArm();return}
  left=EXIT;root.style.setProperty('--pn-exit',EXIT+'s');
  paint('arming');log('Exit delay. Arming all zones.');say('Arming in '+left+'. Press again to cancel.');beep(990,0,0.06,0.04,'square');
  timer=setInterval(function(){
    left-=1;
    if(left<=0){finishArm()}
    else{labels.forEach(function(el){el.textContent='ARMING '+left});say('Arming in '+left+'. Press again to cancel.');beep(990,0,0.06,0.04,'square')}
  },1000);
}
function disarm(){
  var was=state;
  if(timer){clearInterval(timer);timer=null}left=0;
  paint('disarmed');log(was==='arming'?'Arming cancelled.':'System disarmed.');say(was==='arming'?'Arming cancelled. Site disarmed.':'Site disarmed. Press the shield to arm.');
  beep(1320,0,0.08);beep(880,0.1,0.16);if(was==='armed')sweep();
}
function toggle(){if(state==='disarmed')arm();else disarm()}
toggles.forEach(function(b){b.addEventListener('click',toggle)});
log('System armed');

/* events log on the keypad screen */
var evBox=$('#pn-events'),evOpen=$('[data-pn-events-open]'),evClose=$('[data-pn-events-close]');
function showEvents(open){
  if(!evBox)return;evBox.hidden=!open;if(evOpen)evOpen.setAttribute('aria-expanded',String(open));
  if(open){if(evClose)evClose.focus()}else if(evOpen){evOpen.focus()}
  beep(1900,0,0.03,0.02,'square');
}
if(evOpen)evOpen.addEventListener('click',function(){showEvents(evBox.hidden)});
if(evClose)evClose.addEventListener('click',function(){showEvents(false)});
if(evBox)evBox.addEventListener('keydown',function(e){if(e.key==='Escape'){showEvents(false)}});

/* phones: the on-screen menu is too small to tap, the zone bar carries the same six links */
var small=window.matchMedia('(max-width:599px)'),menu=$('.pn-kp-menu');
function inert(){if(!menu)return;if(small.matches){menu.setAttribute('inert','');menu.setAttribute('aria-hidden','true')}else{menu.removeAttribute('inert');menu.removeAttribute('aria-hidden')}}
inert();if(small.addEventListener)small.addEventListener('change',inert);else if(small.addListener)small.addListener(inert);

/* ---------- zones light as their scene comes into view (zone scenes, and the Scenes that belong to a zone) ---------- */
var links=$$('.pn-zb-home a[data-z]'),zones=$$('[data-zone]');
function setActive(k){
  links.forEach(function(a){var z=+a.getAttribute('data-z');a.classList.toggle('is-on',z===k);if(z===k)a.setAttribute('aria-current','true');else a.removeAttribute('aria-current')});
}
/* ---------- chapter rail: which chapter is under the middle of the screen ---------- */
var chs=$$('.pn-ch a[data-ch]'),chn=$('[data-pn-chn]'),cht=$('[data-pn-cht]');
if(chs.length){
  var chTg=chs.map(function(a){return document.getElementById(a.getAttribute('data-ch'))}),chCur=-1,chTick=false;
  var chSpy=function(){
    chTick=false;var y=window.innerHeight*0.45,k=0;
    for(var i=0;i<chTg.length;i++){if(chTg[i]&&chTg[i].getBoundingClientRect().top<=y)k=i}
    if(k===chCur)return;chCur=k;
    chs.forEach(function(a,i){a.classList.toggle('is-on',i===k);if(i===k)a.setAttribute('aria-current','true');else a.removeAttribute('aria-current')});
    if(chn)chn.textContent=('0'+(k+1)).slice(-2);if(cht)cht.textContent=chs[k].getAttribute('data-t')||'';
  };
  window.addEventListener('scroll',function(){if(!chTick){chTick=true;requestAnimationFrame(chSpy)}},{passive:true});
  window.addEventListener('resize',chSpy);chSpy();
}
if('IntersectionObserver' in window){
  var vis=[];
  var io=new IntersectionObserver(function(es){
    es.forEach(function(e){vis[zones.indexOf(e.target)]=e.isIntersecting});
    var on=0;zones.forEach(function(s,i){if(vis[i])on=+s.getAttribute('data-zone')});setActive(on);
  },{rootMargin:'-42% 0px -56% 0px'});
  zones.forEach(function(s){io.observe(s)});
  var liveIO=new IntersectionObserver(function(es){es.forEach(function(e){e.target.classList.toggle('pn-live',e.isIntersecting)})},{rootMargin:'80px 0px'});
  $$('.pn-zone,.pn-hero').forEach(function(el){liveIO.observe(el)});
  var seen=new IntersectionObserver(function(es){es.forEach(function(e){if(!e.isIntersecting)return;e.target.classList.add('in','seen');seen.unobserve(e.target)})},{rootMargin:'0px 0px -10% 0px',threshold:0.1});
  $$('.pn-rv,.pn-z1').forEach(function(el){seen.observe(el)});
}else{$$('.pn-rv,.pn-z1').forEach(function(el){el.classList.add('in','seen')});$$('.pn-zone,.pn-hero').forEach(function(el){el.classList.add('pn-live')})}

/* plant feed: load and play only in view, never with reduced motion, pause when the tab is hidden */
var holder=$('[data-pn-video]'),vid=null;
function play(){if(vid&&!document.hidden){var q=vid.play();if(q&&q.catch)q.catch(function(){})}}
if(holder&&'IntersectionObserver' in window){
  new IntersectionObserver(function(es){es.forEach(function(e){
    if(e.isIntersecting&&!reduce.matches){
      if(!vid){vid=document.createElement('video');vid.muted=true;vid.loop=true;vid.playsInline=true;vid.setAttribute('muted','');vid.setAttribute('playsinline','');vid.setAttribute('aria-hidden','true');vid.preload='metadata';
        if(holder.dataset.webm&&vid.canPlayType('video/webm; codecs="vp9"')){var w=document.createElement('source');w.src=holder.dataset.webm;w.type='video/webm';vid.appendChild(w)}
        var m=document.createElement('source');m.src=holder.dataset.mp4;m.type='video/mp4';vid.appendChild(m);holder.appendChild(vid)}
      play();
    }else if(vid){vid.pause()}
  })},{threshold:0.25}).observe(holder);
  document.addEventListener('visibilitychange',function(){if(!vid)return;if(document.hidden)vid.pause();else play()});
}
})();
"""
