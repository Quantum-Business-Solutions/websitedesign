"""The house finish: one scale for type, space, numerals, states and motion, laid over every module.

preview.py puts POLISH_CSS after the page grammar and before each direction's own system, so a direction still owns its
geometry and its character (Showcase floats, Clean rules, Press sets in serif) but none of them can fall below this
floor. FINISH_CSS goes last, after the direction system, for the few rules a direction must not undo (motion restraint,
focus rings, the type floor). The bar this implements is written down in process/directions-standard.md, section 9,
and measured by scripts/directions_qa.py.

Nothing here invents content. A module with no data is still left out by its renderer.
"""

POLISH_CSS = r"""
/* ===== house finish: scales ===== */
:root{
  --s-1:4px;--s-2:8px;--s-3:12px;--s-4:16px;--s-5:24px;--s-6:32px;--s-7:48px;--s-8:64px;--s-9:96px;
  --sec-y:clamp(72px,8.5vw,112px);
  --t-micro:13px;--t-small:14.5px;--t-body:16px;--t-card:15.5px;--t-lead:clamp(18px,1.4vw,20px);
  --t-h3:clamp(20px,1.55vw,22px);--t-h2:clamp(30px,3.3vw,44px);--t-h1:clamp(40px,4.9vw,66px);
  --ease:cubic-bezier(.2,.7,.2,1);
  --lift:0 18px 40px -18px rgb(var(--shade,16 23 37) / .28),0 2px 6px rgb(var(--shade,16 23 37) / .06);
  --rest:0 1px 2px rgb(var(--shade,16 23 37) / .06);
}
html{-webkit-text-size-adjust:100%}
body{font-size:var(--t-body);line-height:1.6;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;text-rendering:optimizeLegibility;font-kerning:normal}
button,input,select,textarea{font-family:inherit}
p,li,dd,figcaption,blockquote{text-wrap:pretty}
::selection{background:var(--q-gold);color:var(--cta-fg)}

/* ===== type: a real scale, one hierarchy ===== */
.q-h1{font-size:var(--t-h1);line-height:1.05;letter-spacing:-.025em;max-width:17ch}
.q-h1.is-long{font-size:clamp(36px,4vw,54px);line-height:1.08;max-width:20ch}
.q-h1.is-xlong{font-size:clamp(32px,3.3vw,46px);line-height:1.12;max-width:24ch}
.q-h2{font-size:var(--t-h2);line-height:1.12;letter-spacing:-.02em;font-weight:700;max-width:24ch}
.pv-center .q-h2,.q-h2[style*="center"],.pv-cta .q-h2{margin-left:auto;margin-right:auto}
.q-lead{font-size:var(--t-lead);line-height:1.6;max-width:62ch}
.pv-center .q-lead{margin-left:auto;margin-right:auto}
.q-eyebrow{font-size:var(--t-micro);letter-spacing:.14em;font-weight:700;line-height:1.3}
h3{letter-spacing:-.01em;line-height:1.25}
.pv-grid .q-card h3,.pv-svc h3,.pv-loc .q-card h3,.pv-values .q-card h3,.pv-res h3,.pv-lead h3,.pv-post h2{font-size:var(--t-h3);font-weight:700;line-height:1.25}
.pv-grid .q-card p,.pv-values .q-card p,.pv-svc p,.pv-post p{font-size:var(--t-card);line-height:1.65}
.pv-stage p,.pv-tl p,.pv-seal p,.pv-flow .node p,.pv-loc .q-card p,.pv-res p,.pv-lead p,.pv-lh .fcard p,.pv-lh .fcard li,.pv-wheel ol a,.pv-map-list small,.pv-tst figcaption,.pv-video-cap,.pv-attr,.pv-metric .d,.pv-band .q-card .d{font-size:var(--t-small);line-height:1.55}
.pv-stage h3,.pv-tl h3,.pv-flow .node h3,.pv-seal h3{font-size:17.5px;line-height:1.3;font-weight:700}
.pv-tst-letters blockquote{font-size:16px;line-height:1.6}
.pv-tst-letters footer,.pv-proof .src,.pv-hero-note,.pv-lh .note,.pv-form-note,.pv-seal .src,.pv-cmp-hint,.pv-work-foot{font-size:14px;line-height:1.5}
.pv-hero-stats span,.pv-badge span,.pv-stat span{font-size:14px;line-height:1.4}
.pv-work .chip{font-size:13px}.pv-awards .a span{font-size:13.5px;line-height:1.45}.pv-lh-cap{font-size:13px}
.pv-split p{font-size:var(--t-body);max-width:44ch}
.pv-faq summary{font-size:19px;line-height:1.35;font-weight:600}
.pv-faq p{font-size:16px;line-height:1.7;max-width:68ch}

/* ===== numerals and their labels ===== */
.pv-stat b,.pv-hero-stats b,.pv-proof b,.pv-badge b,.pv-metric .v,.pv-tl .y,.pv-calc .v,.pv-flow .dot,.pv-seal .badge b,.q-stagenum,.pv-wheel .bignum{font-variant-numeric:lining-nums tabular-nums;font-feature-settings:"lnum" 1,"tnum" 1}
.pv-stat b{font-size:clamp(44px,4.6vw,64px);letter-spacing:-.03em;font-weight:700}
.pv-stat span{max-width:22ch;margin-left:auto;margin-right:auto;text-wrap:balance}
.pv-stat{padding:4px 24px}
.pv-hero-stats{margin-top:48px}
.pv-hero-stats b{font-size:clamp(32px,3vw,40px);font-weight:700}
.pv-hero-stats span{max-width:20ch;text-wrap:balance}
.pv-proof b{font-size:clamp(88px,13vw,184px);font-weight:700}
.pv-metric .k,.pv-cap,.pv-mega .gt,.pv-post .tag,.pv-res .k,.pv-flow .node .when,.pv-flow .detail .k,.pv-ba .k,.pv-lh .fcard .k,.pv-story .step .k{font-size:var(--t-micro);letter-spacing:.12em;line-height:1.35}

/* ===== space: one section rhythm, one heading stack ===== */
.q-section{padding:var(--sec-y) 0}
.q-eyebrow + .q-h2,.q-eyebrow + h2{margin-top:14px}
.q-h2 + .q-lead{margin-top:16px}
.pv-split{margin-bottom:var(--s-7);gap:var(--s-5) var(--s-7)}
.pv-grid{gap:var(--s-5)}
.pv-partners{padding:0 0 var(--s-8)}
.pv-partners .q-container{padding-top:var(--s-6)}
.pv-cap{margin-bottom:var(--s-5)}
.pv-ribbon .q-container{gap:10px 32px}
.pv-seal,.pv-ba{margin-top:var(--s-7)}
.pv-flow .track{margin-top:var(--s-7)}
.pv-cs,.pv-contact{gap:var(--s-8)}
.pv-cta .q-lead{margin-top:16px}

/* ===== surfaces: cards and bands ===== */
.q-card{padding:28px;transition:translate .25s var(--ease),box-shadow .25s var(--ease),border-color .2s}
a.q-card,.pv-res a,.pv-post,.pv-check label{transition:translate .25s var(--ease),box-shadow .25s var(--ease),border-color .2s}
a.q-card:hover,.pv-res a:hover{translate:0 -3px;border-color:color-mix(in srgb,var(--accent-ink) 55%,transparent);box-shadow:var(--lift)}
.pv-grid .q-card a,.pv-loc .q-card p a{color:var(--accent-ink)}
.pv-grid .q-card a::after{content:"";width:18px;height:1px;background:currentColor;margin-left:8px;transition:width .2s var(--ease)}
.pv-grid .q-card a:hover::after{width:28px}
.q-bg-alt{background:var(--bg-alt);box-shadow:inset 0 1px 0 var(--border),inset 0 -1px 0 var(--border)}
.pv-seal .item{padding:24px;gap:18px;background:var(--card);box-shadow:var(--rest)}
.pv-seal .badge::before{background:var(--card)}
/* four across leaves each commitment about 170px of text beside its badge: stack the badge above instead */
.pv-seal[style*="--cols:4"] .item{grid-template-columns:1fr;gap:14px;align-content:start}
.pv-seal[style*="--cols:4"] .badge{width:56px;height:56px}
@media(max-width:1024px){.pv-seal[style*="--cols:4"]{grid-template-columns:repeat(2,1fr)}}
@media(max-width:480px){.pv-seal[style*="--cols:4"]{grid-template-columns:1fr}.pv-seal[style*="--cols:4"] .item{grid-template-columns:56px 1fr}}
.pv-flow .detail{box-shadow:var(--rest)}
.pv-check label{align-items:center;transition:border-color .2s,background .2s}
.pv-check label:hover{border-color:color-mix(in srgb,var(--accent-ink) 55%,transparent)}
.pv-check label:has(input:checked){border-color:var(--accent-ink);background:color-mix(in srgb,var(--q-gold) 9%,var(--card))}
.pv-tst figure{padding:32px;box-shadow:var(--rest)}
.pv-tst blockquote{font-size:19px;line-height:1.55}
.pv-tst-feature{gap:var(--s-8)}
.pv-tst-feature figure.lead{box-shadow:none}
.pv-tst-feature figure.lead blockquote{font-size:clamp(22px,2.1vw,28px);line-height:1.4}
.pv-tabs [role=tablist]{gap:var(--s-5);margin-bottom:var(--s-6)}
.pv-tabs [role=tab]{font-size:16px;padding:12px 2px;transition:color .2s,border-color .2s}
.pv-tabs [role=tab]:hover{color:var(--fg)}
.pv-tabs [role=tab][aria-selected="true"]{color:var(--fg);border-bottom-color:var(--accent-ink)}
.pv-tabs h3{font-size:clamp(22px,2vw,28px);line-height:1.2}
.pv-tl .y{font-size:clamp(28px,2.4vw,34px);font-weight:700;letter-spacing:-.02em}
.pv-map-list li{padding:16px 0}
.pv-map-list b{font-size:16px}
.pv-quote{font-size:clamp(20px,1.8vw,24px);line-height:1.45}
.pv-cs .h{font-size:clamp(28px,2.8vw,38px);letter-spacing:-.02em}
.pv-metric .v{font-size:clamp(28px,2.4vw,34px);letter-spacing:-.02em}
.pv-wheel .panel .bignum{opacity:.09;top:-34px;font-size:104px;z-index:0}
.pv-wheel .panel > :not(.bignum){position:relative;z-index:1}
.pv-wheel .panel .bignum::after{content:attr(data-ghost)}
.pv-wheel .panel h3{font-size:clamp(24px,2.1vw,28px)}
.pv-wheel ol a{font-size:15px}
.pv-hero-img,.pv-detail-img,.pv-tabs .img,.pv-video,.pv-hero-wide{border-color:var(--border)}
.pv-hero-img img,.pv-detail-img img,.pv-tabs .img img{transition:scale .6s var(--ease)}
.pv-badge{padding:14px 18px}
.pv-badge b{font-size:28px;font-weight:700;letter-spacing:-.02em}
/* partner names with no logo file: a calm row of wordmarks, not a ticker of body text */
.pv-logos span{font-family:var(--q-sans);font-size:17px;font-weight:600;letter-spacing:-.005em;color:var(--fg-muted);white-space:nowrap}
.pv-logos.pv-logos-text{display:block;max-width:1040px;margin:0 auto;padding:0 20px;mask-image:none;-webkit-mask-image:none;overflow:visible}
.pv-logos.pv-logos-text .pv-logos-track{display:block;text-align:center;text-wrap:balance;line-height:2.3;animation:none}
.pv-logos.pv-logos-text span{display:inline-block;margin:0 20px;line-height:1.3}

/* ===== buttons, links, forms ===== */
.q-btn{font-size:16px;font-weight:600;line-height:1.2;padding:14px 26px;gap:8px;transition:background .18s,translate .18s var(--ease),box-shadow .18s}
.q-btn:hover{translate:0 -1px;box-shadow:0 10px 22px -10px rgb(var(--shade,16 23 37) / .45)}
.q-btn:active{translate:0 0;box-shadow:none}
.q-btn-ghost{font-weight:600;gap:10px}
.q-btn-ghost span{transition:width .2s var(--ease)}
.q-btn-ghost:hover span{width:32px!important}
.q-form{padding:32px;box-shadow:var(--rest)}
.q-form label{font-size:14px;font-weight:600;color:var(--fg);margin:0 0 6px}
.q-form input[type=text],.q-form input[type=email],.q-form input[type=tel],.q-form input[type=url],.q-form select,.q-form textarea{width:100%;padding:11px 14px;margin:0 0 18px;background:var(--bg);color:var(--fg);border:1px solid color-mix(in srgb,var(--fg) 46%,transparent);transition:border-color .15s,box-shadow .15s}
.q-form input:hover,.q-form select:hover,.q-form textarea:hover{border-color:color-mix(in srgb,var(--fg) 70%,transparent)}
.q-form input[type=text]:focus,.q-form input[type=email]:focus,.q-form input[type=tel]:focus,.q-form input[type=url]:focus,.q-form select:focus,.q-form textarea:focus{outline:0;border-color:var(--accent-ink);box-shadow:0 0 0 3px color-mix(in srgb,var(--accent-ink) 24%,transparent)}
.q-form .hs-button,.q-form input[type=submit]{margin-top:6px;font-weight:600;cursor:pointer;transition:background .18s,translate .18s var(--ease)}
.q-form .hs-button:hover,.q-form input[type=submit]:hover{translate:0 -1px}
.pv-form-note{font-size:14px;margin-top:14px}

/* ===== chrome ===== */
.q-header .q-nav > a,.q-header .q-nav-item > a{transition:color .15s}
.q-subnav{box-shadow:0 24px 60px -12px rgb(var(--shade,0 0 0) / .28),0 2px 8px rgb(var(--shade,0 0 0) / .08);border:1px solid var(--border)}
.q-subnav a{transition:background .15s,color .15s}
.pv-mega .col{padding:28px 24px 24px}
.pv-mega .col a{padding:9px 0;line-height:1.35}
.pv-mega .feat{padding:28px}
.pv-crumbs ol{font-size:14px}
.q-footer{padding-top:var(--s-8)}
.q-footer-head{font-size:var(--t-micro);letter-spacing:.14em;margin-bottom:6px}
.q-footer-links a{font-size:15px;transition:color .15s}
.q-footer-tag{font-size:15px;line-height:1.6;max-width:34ch}
.q-footer-legal{font-size:14px;margin-top:var(--s-7)}

/* ===== phones ===== */
@media(max-width:1024px){.pv-cs,.pv-contact{gap:var(--s-6)}}
@media(max-width:767px){
  :root{--sec-y:64px}
  .q-h1,.q-h1.is-long{font-size:clamp(34px,9.4vw,42px);line-height:1.08;max-width:none}
  .q-h1.is-xlong{font-size:clamp(30px,8vw,36px);max-width:none}
  .q-h2{font-size:clamp(27px,7.4vw,32px);line-height:1.15}
  .q-lead{font-size:17px;line-height:1.6}
  .q-card{padding:22px}
  .q-form{padding:22px}
  .pv-stat{padding:4px 12px}
  .pv-stat b{font-size:40px}
  .pv-hero-stats{grid-template-columns:1fr 1fr;margin-top:36px}
  .pv-hero-stats > div{padding:18px 16px 0 0;border-left:0;padding-left:0}
  .pv-split{margin-bottom:var(--s-6)}
  .pv-wheel .panel .bignum{display:none}
  .pv-faq summary{font-size:17.5px}
  .pv-tst figure{padding:22px}
  .pv-logos.pv-logos-text span{margin:0 12px}.pv-logos span{font-size:16px}.pv-logos.pv-logos-text .pv-logos-track{line-height:2.1}
  .pv-partners{padding-bottom:var(--s-7)}
}
"""

# After the direction system: what no direction may undo.
FINISH_CSS = r"""
/* ===== house finish: per-direction weight, so the hierarchy holds in each voice ===== */
[data-dir="clean"] .q-h2{font-weight:700}
[data-dir="clean"] .q-h1{font-weight:700;font-size:var(--t-h1)}
[data-dir="showcase"] .q-h1{font-size:var(--t-h1);line-height:1.03}
[data-dir="showcase"] .q-h2{font-weight:800;letter-spacing:-.028em}
[data-dir="showcase"] .q-card{box-shadow:var(--lift)}
[data-dir="showcase"] .pv-band .q-card{box-shadow:none}
[data-dir="showcase"] .pv-stat{box-shadow:var(--lift);padding:28px 20px}
[data-dir="showcase"] .pv-stat b{font-size:clamp(48px,5vw,72px);font-weight:800}
[data-dir="showcase"] .pv-svc a{box-shadow:var(--rest);transition:translate .25s var(--ease),box-shadow .25s var(--ease)}
[data-dir="showcase"] .pv-svc a:hover{translate:0 -2px;box-shadow:var(--lift)}
[data-dir="showcase"] main .q-bg-alt{box-shadow:inset 0 1px 0 var(--border),inset 0 -1px 0 var(--border)}
[data-dir="showcase"] .pv-quote{font-size:clamp(22px,2vw,27px);font-weight:600}
[data-dir="press"] .q-h1{font-weight:500;letter-spacing:-.015em;line-height:1.08}
[data-dir="press"] .q-h2{font-weight:500;letter-spacing:-.012em;line-height:1.15}
[data-dir="press"] .pv-grid .q-card h3,[data-dir="press"] .pv-svc h3,[data-dir="press"] .pv-loc .q-card h3,[data-dir="press"] .pv-post h2,[data-dir="press"] .pv-faq summary,[data-dir="press"] .pv-stage h3,[data-dir="press"] .pv-tl h3{font-weight:500;letter-spacing:0}
[data-dir="press"] .pv-stat b,[data-dir="press"] .pv-hero-stats b,[data-dir="press"] .pv-proof b,[data-dir="press"] .pv-tl .y,[data-dir="press"] .pv-badge b{font-weight:500;letter-spacing:-.01em}
[data-dir="press"] .q-lead{font-size:clamp(19px,1.5vw,21px);line-height:1.55}
[data-dir="press"] .q-bg-alt{box-shadow:none}
[data-dir="press"] .pv-logos span{font-family:var(--q-serif);font-weight:500;font-size:19px}
[data-dir="press"] .q-form input[type=text],[data-dir="press"] .q-form input[type=email],[data-dir="press"] .q-form input[type=tel],[data-dir="press"] .q-form select,[data-dir="press"] .q-form textarea{background:var(--card)}
@media(max-width:767px){
  [data-dir] .q-h1,[data-dir] .q-h1.is-long{font-size:clamp(34px,9.4vw,42px);line-height:1.08}
  [data-dir] .q-h1.is-xlong{font-size:clamp(30px,8vw,36px)}
  [data-dir] .q-h2{font-size:clamp(27px,7.4vw,32px);line-height:1.15}
  [data-dir="showcase"] .pv-stat b,[data-dir] .pv-stat b{font-size:40px}
  [data-dir="showcase"] .pv-stat{padding:20px 12px}
}

.q-eyebrow + .q-h2,.q-eyebrow + .q-h1{margin-top:16px!important}
.pv-lh .q-eyebrow + .q-h1{margin-top:20px!important}

/* ===== motion: one thing moves at a time, and nothing loops for decoration ===== */
html.pv-js .pv-rv{transform:translateY(12px)}
html.pv-js .pv-rv.in{transition:opacity .5s var(--ease),transform .5s var(--ease);transition-delay:calc(min(var(--i,0),4)*50ms)}
.pv-tilt{transform:none!important}
.pv-tilt::after{display:none}
.pv-logos-track{animation-duration:80s}
.pv-wheel .orbit,.pv-wheel .pulse,.pv-stage::before,.pv-fleet .dev .img img{animation:none}
.pv-wheel .pulse{opacity:0}
.pv-stage::before{opacity:.4}
.pv-lh .hero3d{animation:none}
html.pv-js [data-dir="showcase"] .pv-lh .hero3d{animation:pv-in3d .9s var(--ease) both}
.pv-lh .bg img{animation-duration:60s}
.pv-flow .node[aria-expanded="true"] .dot,.pv-flow .node:hover .dot{transform:none}
.pv-play:hover{transform:scale(1.04)}

/* ===== focus: every interactive thing shows where the keyboard is ===== */
:where(a,button,summary,input,select,textarea,[role=tab],[tabindex]):focus-visible{outline:2px solid var(--accent-ink);outline-offset:3px;border-radius:4px}
:where(.pv-lh,.pv-hero-video,.pv-band,.pv-work-sec,.pv-ba .after,.pv-calc .big,.pv-switch,.pv-switch-m) :where(a,button,summary):focus-visible{outline-color:#fff}
:where(.q-header,.q-footer,.pv-util,.pv-ribbon) :where(a,button,summary):focus-visible{outline-color:var(--chrome-fg)}
.q-btn:focus-visible,.q-form .hs-button:focus-visible{outline-offset:3px;box-shadow:0 0 0 5px color-mix(in srgb,var(--accent-ink) 22%,transparent)}

@media(prefers-reduced-motion:reduce){
  *,*::before,*::after{scroll-behavior:auto!important}
  .q-btn,.q-card,a.q-card,.pv-res a,.pv-svc a{transition:none}
  a.q-card:hover,.pv-res a:hover,.q-btn:hover,[data-dir="showcase"] .pv-svc a:hover{translate:none}
}
"""
