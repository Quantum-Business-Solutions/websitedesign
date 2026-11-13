"""Opt-in signature sections for the preview generator: the promise hero, the two-track build
timeline, the building-type explorer, the route guide and the planning request.

Nothing here reaches a client whose content file does not name one of these section types:
preview.py adds WOW_CSS and WOW_JS to a page only when the page uses one (see uses()).

Every renderer degrades to readable static HTML with no JS, gates motion on
prefers-reduced-motion, and takes all of its words from the content file. No facts live here.
Each direction styles the same markup its own way ([data-dir] rules at the end of WOW_CSS).
"""
from __future__ import annotations

TYPES = ("rxhero", "tracks", "explorer", "routes", "plan")


def uses(sections) -> bool:
    return any(s.get("type") in TYPES for s in sections)


WOW_CSS = r"""
/* ===== opt-in signature sections (preview_wow.py) ===== */
.rx-vh{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);clip-path:inset(50%);white-space:nowrap}
.rx-js .rx-rv{opacity:0;transform:translateY(18px);transition:opacity .6s ease,transform .7s cubic-bezier(.2,.7,.2,1);transition-delay:var(--d,0ms)}
.rx-js .rx-rv.rx-in{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){.rx-js .rx-rv{opacity:1;transform:none;transition:none}}
.rx-head{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr);gap:28px 64px;align-items:end;margin-bottom:44px}
.rx-head .q-h2{margin:20px 0 0;text-wrap:balance}
.rx-head p{margin:0;font-size:18px;line-height:1.6;color:var(--fg-muted);max-width:52ch}
.rx-head-c{display:flex;flex-direction:column;align-items:center;text-align:center;margin-bottom:36px}
.rx-head-c .q-h2{margin:20px 0 0;max-width:760px;text-wrap:balance}
.rx-head-c p{margin:16px 0 0;font-size:18px;line-height:1.6;color:var(--fg-muted);max-width:58ch}
.rx-src{margin:22px 0 0;font-size:13px;line-height:1.5;color:var(--fg-muted)}
.rx-link{display:inline-flex;align-items:center;gap:10px;min-height:44px;font-weight:600;font-size:16px;color:var(--accent-ink)}
.rx-link::after{content:"";width:22px;height:1px;background:currentColor;transition:width .2s ease}
.rx-link:hover::after{width:34px}

/* ---- hero ---- */
.rx-hero{padding-top:52px;padding-bottom:56px}
.rx-hero .rx-h1{max-width:none;font-size:clamp(34px,3.85vw,56px);line-height:1.05;letter-spacing:-.025em;margin:20px 0 0;text-wrap:balance}
.rx-hero .q-lead{font-size:18px;line-height:1.6;margin:0}
.rx-hero .pv-btns{margin-top:26px}
.rx-hero .pv-hero-note{margin-top:18px}
.rx-fig{position:relative;margin:0}
.rx-fig .rx-frame{position:relative;overflow:hidden;background:var(--bg-alt)}
.rx-fig img{display:block;width:100%;height:100%;object-fit:cover}
.rx-fig figcaption{margin-top:12px;font-size:13px;line-height:1.5;color:var(--fg-muted)}
.rx-stats{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));margin:0;padding:0;list-style:none}
.rx-stats li{padding:22px 24px;border-left:1px solid var(--border)}
.rx-stats li:first-child{border-left:0}
.rx-stats b{display:block;font-family:var(--q-serif);font-size:34px;line-height:1;font-weight:800;letter-spacing:-.03em;color:var(--accent-ink);white-space:nowrap}
.rx-stats span{display:block;margin-top:8px;font-size:13px;line-height:1.45;color:var(--fg-muted)}
.rx-affil{margin-top:40px;display:flex;flex-direction:column;align-items:center;text-align:center;gap:12px}
.rx-affil p{margin:0;font-size:13px;letter-spacing:.16em;text-transform:uppercase;font-weight:700;color:var(--fg-muted)}
.rx-affil ul{display:flex;flex-wrap:wrap;justify-content:center;gap:8px 34px;margin:0;padding:0;list-style:none;font-size:15px;font-weight:600;color:var(--fg)}
.rx-affil li{display:inline-flex;align-items:center;gap:10px}
.rx-affil li::before{content:"";width:7px;height:7px;border-radius:50%;background:var(--q-gold);flex:none}
/* the small "both at once" card that sits on the hero photograph */
.rx-now{background:var(--bg);border-radius:16px;padding:16px 18px 18px;width:292px;box-shadow:0 14px 40px rgba(16,23,37,.16)}
.rx-now .k{font-size:13px;letter-spacing:.14em;text-transform:uppercase;font-weight:700;color:var(--accent-ink)}
.rx-now dl{margin:10px 0 0;display:grid;gap:10px}
.rx-now dt{font-size:13.5px;font-weight:600;color:var(--fg);line-height:1.3}
.rx-now dd{margin:6px 0 0;height:8px;border-radius:99px;background:color-mix(in srgb,var(--q-gold) 16%,var(--bg));overflow:hidden}
.rx-now dd i{display:block;height:100%;border-radius:99px;background:var(--q-gold);transform-origin:0 50%;animation:rx-now 7s cubic-bezier(.45,0,.2,1) infinite}
.rx-now dd.b i{background:var(--fg)}
@keyframes rx-now{0%{transform:scaleX(.04)}62%,88%{transform:scaleX(1)}100%{transform:scaleX(.04)}}
@media(prefers-reduced-motion:reduce){.rx-now dd i{animation:none}}
/* home, photo-led */
.rx-hero-photo .rx-h1{max-width:23em}
.rx-hero-photo .rx-hero-top{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:24px 64px;align-items:center;margin-top:26px}
.rx-hero-photo .rx-hero-top .q-lead{max-width:62ch}
.rx-hero-photo .rx-hero-top .pv-btns{margin-top:0;justify-content:flex-end}
.rx-hero-photo .rx-fig{margin-top:44px}
.rx-hero-photo .rx-frame{aspect-ratio:21/9;border-radius:28px;box-shadow:0 30px 70px rgba(16,23,37,.16)}
.rx-hero-photo .rx-frame img{object-position:50% 58%}
.rx-hero-photo .rx-now{position:absolute;left:28px;top:28px}
.rx-hero-photo .rx-stats{position:relative;margin:-54px 40px 0;background:var(--bg);border-radius:20px;box-shadow:0 18px 50px rgba(16,23,37,.12)}
.rx-hero-photo .rx-stats li{padding:26px 28px}
/* home, ledger */
.rx-hero-ledger .rx-hero-top{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,.8fr);gap:40px 64px;align-items:center}
.rx-hero-ledger .rx-h1{font-size:clamp(34px,3.4vw,48px);line-height:1.07}
.rx-hero-ledger .q-lead{margin-top:22px;max-width:56ch}
.rx-hero-ledger .rx-frame{aspect-ratio:16/10;border-radius:var(--radius);border:1px solid var(--border)}
.rx-hero-ledger .rx-frame img{object-position:38% 60%}
.rx-get{margin:-36px 20px 0;position:relative;background:var(--bg);border:1px solid var(--border);border-radius:var(--radius);padding:18px 20px 16px;box-shadow:0 10px 30px rgba(16,23,37,.07)}
.rx-get .k{font-size:13px;letter-spacing:.14em;text-transform:uppercase;font-weight:700;color:var(--accent-ink)}
.rx-get ul{margin:12px 0 0;padding:0;list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:8px 18px;font-size:14.5px;line-height:1.35;color:var(--fg)}
.rx-get li{display:grid;grid-template-columns:18px 1fr;gap:8px;align-items:start}
.rx-get li::before{content:"";width:9px;height:5px;margin-top:5px;border-left:2px solid var(--q-gold);border-bottom:2px solid var(--q-gold);transform:rotate(-45deg)}
.rx-hero-ledger .rx-stats{margin-top:52px;border-top:1px solid var(--border)}
.rx-hero-ledger .rx-stats li{padding:22px 24px 0}.rx-hero-ledger .rx-stats li:first-child{padding-left:0}
/* home, plate */
.rx-hero-plate .rx-h1{font-size:clamp(36px,4.3vw,62px);line-height:1.08;max-width:21em;font-weight:500;letter-spacing:-.015em}
.rx-hero-plate .rx-hero-top{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(0,1fr);gap:36px 56px;align-items:start;margin-top:40px;padding-top:36px;border-top:1px solid var(--fg)}
.rx-hero-plate .rx-frame{aspect-ratio:16/9;border:1px solid var(--fg);padding:10px;background:var(--card)}
.rx-hero-plate .rx-frame img{object-position:50% 60%}
.rx-hero-plate figcaption{font-family:var(--q-serif);font-style:italic;font-size:14.5px}
.rx-hero-plate .q-lead{font-size:20px;line-height:1.55}
.rx-hero-plate .pv-btns{display:inline-flex;flex-direction:column;align-items:flex-start;gap:8px}
/* inner pages */
.rx-hero-page{padding-top:48px}
.rx-hero-page .rx-hero-top{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,600px);gap:40px 64px;align-items:center}
.rx-hero-page .rx-h1{font-size:clamp(34px,3.6vw,52px)}
.rx-hero-page .q-lead{margin-top:22px;max-width:52ch}
.rx-hero-page .rx-fig{max-width:600px;width:100%;justify-self:end}
.rx-hero-page .rx-frame{aspect-ratio:2/1;border-radius:var(--radius);border:1px solid var(--border)}
.rx-facts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));margin:0;padding:0;list-style:none;border-bottom:1px solid var(--border)}
.rx-facts li{padding:16px 16px 16px 0;border-left:1px solid var(--border);padding-left:16px}
.rx-facts li:first-child{border-left:0;padding-left:0}
.rx-facts b{display:block;font-family:var(--q-serif);font-size:20px;line-height:1.15;font-weight:800;letter-spacing:-.02em;color:var(--fg)}
.rx-facts span{display:block;margin-top:6px;font-size:13px;line-height:1.4;color:var(--fg-muted)}

/* ---- two tracks ---- */
.rx-figs{display:grid;grid-template-columns:1fr 1fr;gap:0;margin:0;padding:0;list-style:none}
.rx-figs li{padding:0 0 0 24px;border-left:2px solid var(--q-gold)}
.rx-figs li + li{margin-left:24px}
.rx-figs b{display:block;font-family:var(--q-serif);font-size:clamp(26px,2.6vw,36px);line-height:1;font-weight:800;letter-spacing:-.03em;color:var(--fg);white-space:nowrap}
.rx-figs span{display:block;margin-top:8px;font-size:13.5px;line-height:1.4;color:var(--fg-muted)}
[data-rx-tracks]{--p:1}
.rx-tl{--k:168px;position:relative;background:var(--card);border:1px solid var(--border);border-radius:calc(var(--radius) + 6px);padding:30px 32px 26px}
.rx-tl-in{position:relative}
.rx-zone{position:absolute;top:36px;bottom:0;left:calc(var(--k) + (100% - var(--k))*.6);width:calc((100% - var(--k))*.15);background:repeating-linear-gradient(135deg,color-mix(in srgb,var(--q-gold) 13%,transparent) 0 6px,color-mix(in srgb,var(--q-gold) 5%,transparent) 6px 12px);border-left:1px dashed color-mix(in srgb,var(--q-gold) 60%,transparent);border-right:1px dashed color-mix(in srgb,var(--q-gold) 60%,transparent);pointer-events:none}
.rx-ph{position:absolute;top:-8px;bottom:-8px;left:calc(var(--k) + (100% - var(--k))*var(--p));width:2px;margin-left:-1px;background:var(--fg);pointer-events:none;display:none}
.rx-ph::before{content:"";position:absolute;left:-4px;top:-5px;width:10px;height:10px;border-radius:50%;background:var(--fg)}
.rx-live .rx-ph{display:block;transition:opacity .5s ease .3s}.rx-live.rx-done .rx-ph{opacity:0}
.rx-grp{position:relative}
.rx-grp + .rx-grp{margin-top:22px;padding-top:22px;border-top:1px solid var(--border)}
.rx-grp-t{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 12px;margin:0 0 14px;font-size:17px;font-weight:700;color:var(--fg);line-height:1.3}
.rx-grp-t span{font-size:13.5px;font-weight:500;color:var(--fg-muted)}
.rx-lane{display:grid;grid-template-columns:var(--k) minmax(0,1fr);align-items:end}
.rx-lane + .rx-lane{margin-top:12px}
.rx-lane-k{font-size:13px;letter-spacing:.12em;text-transform:uppercase;font-weight:700;color:var(--fg-muted);padding:0 14px 1px 0;line-height:1.2}
.rx-rail{position:relative;height:44px}
.rx-rail::after{content:"";position:absolute;left:0;right:0;bottom:0;height:14px;border-radius:99px;background:color-mix(in srgb,var(--fg) 7%,transparent)}
.rx-bar{position:absolute;bottom:0;top:0;left:calc(var(--s)*100%);width:calc((var(--e) - var(--s))*100%);display:flex;flex-direction:column;justify-content:flex-end;--f:clamp(0,calc((var(--p) - var(--s))/(var(--e) - var(--s))),1);z-index:1}
.rx-bar span{font-size:13px;line-height:1.2;font-weight:600;color:var(--fg);padding:0 2px 6px 2px;white-space:nowrap}
.rx-bar u{display:block;height:14px;border-radius:99px;background:color-mix(in srgb,var(--q-gold) 20%,var(--card));overflow:hidden;text-decoration:none;box-shadow:inset 0 0 0 1px color-mix(in srgb,var(--q-gold) 30%,transparent);margin-right:3px}
.rx-bar u i{display:block;height:100%;background:var(--q-gold);transform:scaleX(var(--f));transform-origin:0 50%;will-change:transform}
.rx-b .rx-bar u{background:color-mix(in srgb,var(--fg) 10%,var(--card));box-shadow:inset 0 0 0 1px color-mix(in srgb,var(--fg) 18%,transparent)}
.rx-b .rx-bar u i{background:color-mix(in srgb,var(--fg) 62%,var(--card))}
.rx-seg u i{background:repeating-linear-gradient(90deg,var(--q-gold) 0 calc(25% - 2px),color-mix(in srgb,var(--q-gold) 20%,var(--card)) calc(25% - 2px) 25%)}
.rx-flag{display:grid;grid-template-columns:var(--k) minmax(0,1fr);margin-top:8px}
.rx-flag div{grid-column:2;position:relative;height:24px}
.rx-flag b{position:absolute;top:0;left:calc(var(--at)*100%);display:inline-flex;align-items:center;gap:7px;font-size:13px;font-weight:700;color:var(--accent-ink);white-space:nowrap;transition:color .3s ease}
.rx-flag b::before{content:"";width:9px;height:9px;border-radius:50%;background:var(--q-gold);margin-left:-5px;transition:background .3s ease,transform .3s ease}
.rx-flag b.end{left:auto;right:0;flex-direction:row-reverse}
.rx-flag b.end::before{margin:0 -4px 0 0}
.rx-b .rx-flag b{color:var(--fg)}.rx-b .rx-flag b::before{background:var(--fg)}
.rx-live .rx-flag b:not(.rx-on){color:var(--fg-muted)}
.rx-live .rx-flag b:not(.rx-on)::before{background:color-mix(in srgb,var(--fg) 22%,var(--card));transform:scale(.8)}
.rx-key{display:flex;align-items:center;gap:12px;margin:22px 0 0;font-size:13.5px;line-height:1.45;color:var(--fg-muted)}
.rx-key i{flex:none;width:30px;height:16px;border-radius:3px;background:repeating-linear-gradient(135deg,color-mix(in srgb,var(--q-gold) 26%,transparent) 0 4px,color-mix(in srgb,var(--q-gold) 9%,transparent) 4px 8px);border:1px dashed color-mix(in srgb,var(--q-gold) 60%,transparent)}
.rx-steps{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:0;margin:28px 0 0;padding:0;list-style:none;counter-reset:rx}
.rx-steps li{counter-increment:rx;padding:18px 22px 0 0;border-top:2px solid var(--q-gold);margin-right:14px;transition:border-color .35s ease}
.rx-steps li:last-child{margin-right:0}
.rx-steps h3{margin:0;font-size:16.5px;line-height:1.3;font-weight:700;color:var(--fg);display:flex;gap:10px;align-items:baseline}
.rx-steps h3::before{content:counter(rx);font-size:13px;font-weight:700;color:var(--accent-ink);transition:color .35s ease}
.rx-steps p{margin:8px 0 0;font-size:14.5px;line-height:1.55;color:var(--fg-muted)}
.rx-live .rx-steps li:not(.rx-on){border-top-color:var(--border)}
.rx-live .rx-steps li:not(.rx-on) h3::before{color:var(--fg-muted)}
.rx-tracks-photo .rx-head{align-items:center}
.rx-tk-fig{margin:0;max-width:520px;justify-self:end;width:100%}
.rx-tk-fig .rx-frame{aspect-ratio:3/2;border-radius:var(--radius);overflow:hidden;background:var(--bg-alt)}
.rx-tk-fig img{display:block;width:100%;height:100%;object-fit:cover}
.rx-tk-fig figcaption{margin-top:10px;font-size:13px;color:var(--fg-muted)}
.rx-tracks-photo .rx-figs{margin-top:28px}

/* ---- explorer ---- */
.rx-ex-tabs{display:none;gap:6px;justify-content:center;flex-wrap:wrap;margin:0 auto 32px;padding:6px;width:fit-content;max-width:100%;background:color-mix(in srgb,var(--fg) 5%,transparent);border-radius:999px}
.rx-js .rx-ex-tabs{display:flex}
.rx-ex-tabs [role=tab]{appearance:none;border:0;background:none;cursor:pointer;font:600 15.5px/1 var(--q-sans);color:var(--fg);padding:0 22px;min-height:46px;border-radius:999px;transition:background .2s ease,color .2s ease}
.rx-ex-tabs [role=tab]:hover{background:color-mix(in srgb,var(--fg) 7%,transparent)}
.rx-ex-tabs [role=tab][aria-selected=true]{background:var(--q-gold);color:var(--cta-fg)}
.rx-ex-tabs [role=tab]:focus-visible{outline:2px solid var(--fg);outline-offset:2px}
.rx-pan{display:grid;grid-template-columns:minmax(0,600px) minmax(0,1fr);gap:36px 56px;align-items:start}
.rx-pan + .rx-pan{margin-top:56px}.rx-js .rx-pan + .rx-pan{margin-top:0}
.rx-pan[hidden]{display:none}
.rx-js .rx-pan:not([hidden]) .rx-pan-fig{animation:rx-pan-a .5s cubic-bezier(.2,.7,.2,1) both}
.rx-js .rx-pan:not([hidden]) .rx-pan-copy{animation:rx-pan-b .5s .06s cubic-bezier(.2,.7,.2,1) both}
@keyframes rx-pan-a{from{opacity:0;transform:translateX(-14px)}to{opacity:1;transform:none}}
@keyframes rx-pan-b{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}
@media(prefers-reduced-motion:reduce){.rx-js .rx-pan:not([hidden]) .rx-pan-fig,.rx-js .rx-pan:not([hidden]) .rx-pan-copy{animation:none}}
.rx-pan-fig{position:relative;margin:0;max-width:600px;width:100%}
.rx-pan-fig .rx-frame{position:relative;aspect-ratio:2/1;overflow:hidden;border-radius:var(--radius);background:var(--bg-alt)}
.rx-pan-fig img{display:block;width:100%;height:100%;object-fit:cover}
.rx-pan-copy h3{margin:0;font-family:var(--q-serif);font-size:clamp(24px,2.3vw,32px);line-height:1.15;letter-spacing:-.02em;color:var(--fg);text-wrap:balance}
.rx-pan-copy > p{margin:14px 0 0;font-size:17px;line-height:1.6;color:var(--fg-muted);max-width:54ch}
.rx-pan-cols{display:grid;grid-template-columns:1fr 1fr;gap:20px 32px;margin-top:24px;padding-top:22px;border-top:1px solid var(--border)}
.rx-pan-cols h4{margin:0 0 10px;font-size:13px;letter-spacing:.14em;text-transform:uppercase;font-weight:700;color:var(--accent-ink)}
.rx-pan-cols ul{margin:0;padding:0;list-style:none;display:grid;gap:8px;font-size:14.5px;line-height:1.45;color:var(--fg)}
.rx-pan-cols li span{display:block;color:var(--fg-muted);font-size:13.5px}
.rx-pan-cols .b li{display:grid;grid-template-columns:14px 1fr;gap:8px}
.rx-pan-cols .b li::before{content:"";width:6px;height:6px;border-radius:50%;background:var(--q-gold);margin-top:8px}
.rx-pan-copy .rx-link{margin-top:18px}

/* ---- route guide ---- */
.rx-rt{border:1px solid var(--border);border-radius:calc(var(--radius) + 4px);background:var(--card);overflow:hidden}
.rx-rt-q{display:none;grid-template-columns:1.6fr 1fr;gap:0;border-bottom:1px solid var(--border)}
.rx-js .rx-rt-q{display:grid}
.rx-rt-q fieldset{margin:0;border:0;padding:24px 28px;min-width:0}
.rx-rt-q fieldset + fieldset{border-left:1px solid var(--border)}
.rx-rt-q legend{float:left;width:100%;padding:0;margin:0 0 14px;font-size:13px;letter-spacing:.14em;text-transform:uppercase;font-weight:700;color:var(--fg-muted)}
.rx-opts{clear:both;display:flex;flex-wrap:wrap;gap:8px}
.rx-opts label{position:relative;cursor:pointer}
.rx-opts input{position:absolute;opacity:0;inset:0;width:100%;height:100%;margin:0;cursor:pointer}
.rx-opts span{display:inline-flex;align-items:center;min-height:44px;padding:0 16px;border:1px solid var(--border);border-radius:8px;background:var(--bg);font-size:15px;font-weight:600;color:var(--fg);transition:border-color .15s ease,background .15s ease,color .15s ease}
.rx-opts label:hover span{border-color:var(--fg)}
.rx-opts input:checked + span{background:var(--fg);border-color:var(--fg);color:var(--bg)}
.rx-opts input:focus-visible + span{outline:2px solid var(--q-gold);outline-offset:2px}
.rx-res{padding:28px}
.rx-res + .rx-res{border-top:1px solid var(--border)}
.rx-res[hidden]{display:none}
.rx-res > h3{margin:0 0 20px;font-family:var(--q-serif);font-size:22px;line-height:1.25;letter-spacing:-.01em;color:var(--fg)}
.rx-js .rx-res:not([hidden]) .rx-res-g{animation:rx-pan-b .4s cubic-bezier(.2,.7,.2,1) both}
@media(prefers-reduced-motion:reduce){.rx-js .rx-res:not([hidden]) .rx-res-g{animation:none}}
.rx-res-g{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:0}
.rx-res-g > div{padding:0 28px;border-left:1px solid var(--border)}
.rx-res-g > div:first-child{padding-left:0;border-left:0}.rx-res-g > div:last-child{padding-right:0}
.rx-res-g h4{margin:0 0 10px;font-size:13px;letter-spacing:.14em;text-transform:uppercase;font-weight:700;color:var(--accent-ink)}
.rx-res-g strong{display:block;font-size:17px;line-height:1.3;color:var(--fg);font-weight:700}
.rx-res-g p{margin:8px 0 0;font-size:14.5px;line-height:1.55;color:var(--fg-muted)}
.rx-res-g ul{margin:0;padding:0;list-style:none;display:grid;gap:12px}
.rx-res-g .q-btn{margin-top:16px;padding:13px 22px;font-size:15px}

/* ---- planning request ---- */
.rx-plan-g{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,480px);gap:48px 64px;align-items:start}
.rx-plan .q-h2{margin:20px 0 0;text-wrap:balance}
.rx-plan .q-lead{margin-top:16px;font-size:18px;line-height:1.6;max-width:56ch}
.rx-sheets{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px;margin:30px 0 0;padding:0;list-style:none}
.rx-sheets li{background:var(--bg);border:1px solid var(--border);border-radius:10px;padding:14px 12px 14px;display:flex;flex-direction:column;gap:12px;box-shadow:0 6px 18px rgba(16,23,37,.05);transition:transform .25s ease,box-shadow .25s ease}
.rx-sheets li:hover{transform:translateY(-4px);box-shadow:0 14px 30px rgba(16,23,37,.1)}
.rx-sheets svg{width:100%;height:auto;aspect-ratio:4/3;color:var(--fg);display:block}
.rx-sheets svg .a{stroke:var(--q-gold)}
.rx-sheets b{font-size:13.5px;line-height:1.25;font-weight:700;color:var(--fg)}
.rx-next{margin:30px 0 0;padding:0;list-style:none;counter-reset:rxn;display:grid;gap:0;border-top:1px solid var(--border)}
.rx-next li{counter-increment:rxn;display:grid;grid-template-columns:34px 1fr;gap:6px;padding:14px 0;border-bottom:1px solid var(--border);font-size:15px;line-height:1.5;color:var(--fg-muted)}
.rx-next li::before{content:counter(rxn);font-weight:700;color:var(--accent-ink);font-size:14px;line-height:1.6}
.rx-next b{color:var(--fg);font-weight:700}
.rx-call{margin:22px 0 0;font-size:15px;color:var(--fg-muted)}
.rx-call a{color:var(--fg);font-weight:700;min-height:44px;display:inline-flex;align-items:center}
.rx-plan .q-form{display:grid;grid-template-columns:1fr 1fr;gap:0 14px;box-shadow:0 20px 50px rgba(16,23,37,.08)}
.rx-plan .q-form .f{min-width:0}.rx-plan .q-form .w{grid-column:1/-1}
.rx-plan .q-form .hs-button{white-space:normal;padding-left:12px;padding-right:12px}
.rx-plan .q-form .ft{grid-column:1/-1;margin:0 0 16px;font-family:var(--q-serif);font-size:20px;line-height:1.25;font-weight:700;color:var(--fg)}

/* ---- fixes to shared sections on pages that carry these (same content, tidier grid) ---- */
.pv-seal{grid-template-columns:repeat(3,1fr)}
.pv-seal .badge b{font-size:13px;max-width:46px;line-height:1.05}
@media(max-width:1024px){.pv-seal{grid-template-columns:repeat(2,1fr)}}
@media(max-width:560px){.pv-seal{grid-template-columns:1fr}}

/* ---- responsive ---- */
@media(max-width:1024px){
  .rx-head{grid-template-columns:1fr;align-items:start}
  .rx-hero-photo .rx-hero-top .pv-btns{justify-content:flex-start}
  .rx-hero-photo .rx-hero-top,.rx-hero-ledger .rx-hero-top,.rx-hero-plate .rx-hero-top,.rx-hero-page .rx-hero-top{grid-template-columns:1fr}
  .rx-hero-page .rx-fig,.rx-tk-fig{justify-self:start}
  .rx-pan{grid-template-columns:1fr}
  .rx-plan-g{grid-template-columns:1fr}
  .rx-res-g{grid-template-columns:1fr;gap:22px}.rx-res-g > div{padding:22px 0 0;border-left:0;border-top:1px solid var(--border)}.rx-res-g > div:first-child{padding-top:0;border-top:0}
  .rx-rt-q{grid-template-columns:1fr}.rx-rt-q fieldset + fieldset{border-left:0;border-top:1px solid var(--border)}
  .rx-steps{grid-template-columns:1fr 1fr;gap:22px 0}
}
@media(max-width:767px){
  .rx-hero{padding-top:36px;padding-bottom:44px}
  .rx-hero .rx-h1,.rx-hero-ledger .rx-h1,.rx-hero-plate .rx-h1,.rx-hero-page .rx-h1{font-size:clamp(30px,8.4vw,38px);line-height:1.08}
  .rx-hero .q-lead,.rx-hero-plate .q-lead{font-size:17px}
  .rx-hero-photo .rx-fig{margin-top:32px}
  .rx-hero-photo .rx-frame{aspect-ratio:4/3;border-radius:20px}
  .rx-hero-photo .rx-frame img{object-position:40% 60%}
  .rx-hero-photo .rx-now{position:relative;left:auto;top:auto;width:auto;margin:-28px 14px 0;box-shadow:0 12px 30px rgba(16,23,37,.14)}
  .rx-hero-photo .rx-stats{margin:16px 0 0;border-radius:16px;box-shadow:none;border:1px solid var(--border)}
  .rx-stats{grid-template-columns:1fr 1fr}
  .rx-stats li,.rx-hero-photo .rx-stats li,.rx-hero-ledger .rx-stats li{padding:18px 16px;border-left:0;border-top:1px solid var(--border)}
  .rx-stats li:nth-child(even){border-left:1px solid var(--border)}
  .rx-stats li:nth-child(-n+2){border-top:0}
  .rx-hero-ledger .rx-stats{margin-top:36px;border:1px solid var(--border);border-radius:var(--radius)}
  .rx-hero-ledger .rx-stats li:first-child{padding-left:16px}
  .rx-stats b{font-size:28px}
  .rx-get{margin:-24px 12px 0}.rx-get ul{grid-template-columns:1fr}
  .rx-hero-plate .rx-hero-top{margin-top:28px;padding-top:28px}
  .rx-facts b{font-size:17px}.rx-facts li{padding:14px 10px 14px 10px}
  .rx-affil ul{gap:8px 22px;font-size:14.5px}
  .rx-head{margin-bottom:30px}.rx-head p,.rx-head-c p{font-size:17px}
  .rx-figs b{font-size:26px}.rx-figs li{padding-left:14px}.rx-figs li + li{margin-left:14px}
  .rx-tl{--k:0px;padding:20px 16px 18px;border-radius:var(--radius)}
  .rx-lane{grid-template-columns:1fr}.rx-lane-k{padding:0 0 2px}
  .rx-lane + .rx-lane{margin-top:14px}
  .rx-rail{height:40px}
  .rx-bar span{font-size:13px;white-space:normal;line-height:1.15;padding-bottom:5px}
  .rx-flag{grid-template-columns:1fr}.rx-flag div{grid-column:1}
  .rx-steps{grid-template-columns:1fr;gap:18px}.rx-steps li{margin-right:0;padding-right:0}
  .rx-ex-tabs{display:none;grid-template-columns:1fr 1fr;width:100%;border-radius:18px;margin-bottom:24px}
  .rx-js .rx-ex-tabs{display:grid}
  .rx-ex-tabs [role=tab]{border-radius:14px;padding:0 8px;font-size:15px}
  .rx-pan-cols{grid-template-columns:1fr}
  .rx-rt-q fieldset{padding:18px 16px}.rx-res{padding:22px 16px}
  .rx-opts span{padding:0 13px;font-size:14.5px}
  .rx-sheets{grid-template-columns:repeat(2,minmax(0,1fr))}
  .rx-sheets li:last-child{grid-column:1/-1;flex-direction:row;align-items:center}.rx-sheets li:last-child svg{width:46%}
  .rx-plan .q-form{grid-template-columns:1fr}
}

/* ===== direction voices ===== */
/* Showcase: photo-led, rounded, soft lift */
[data-dir="showcase"] .rx-hero .rx-h1,[data-dir="showcase"] .rx-pan-copy h3{font-weight:800;letter-spacing:-.03em}
[data-dir="showcase"] .rx-hero-page .rx-hero-top{grid-template-columns:minmax(0,600px) minmax(0,1fr)}
[data-dir="showcase"] .rx-hero-page .rx-hero-top > div:first-child{order:2}
[data-dir="showcase"] .rx-hero-page .rx-fig{justify-self:start}
[data-dir="showcase"] .rx-hero-page .rx-frame,[data-dir="showcase"] .rx-pan-fig .rx-frame,[data-dir="showcase"] .rx-tk-fig .rx-frame{border:0;border-radius:24px;box-shadow:0 24px 56px rgba(16,23,37,.16)}
[data-dir="showcase"] .rx-hero-page .rx-fig::before,[data-dir="showcase"] .rx-pan-fig::before{content:"";position:absolute;left:-16px;top:18px;right:34px;aspect-ratio:2/1;border-radius:24px;background:color-mix(in srgb,var(--q-gold) 9%,var(--bg))}
[data-dir="showcase"] .rx-hero-page .rx-facts{margin-top:8px}
[data-dir="showcase"] .rx-tl{border:0;box-shadow:0 18px 50px rgba(16,23,37,.09);background:var(--bg)}
[data-dir="showcase"] .q-bg-alt .rx-tl{background:var(--bg)}
[data-dir="showcase"] .rx-rt{border:0;box-shadow:0 18px 50px rgba(16,23,37,.09);background:var(--bg)}
[data-dir="showcase"] .rx-opts span{border-radius:999px}
[data-dir="showcase"] .rx-sheets li{border:0;border-radius:16px;box-shadow:0 10px 26px rgba(16,23,37,.08)}
@media(max-width:1024px){[data-dir="showcase"] .rx-hero-page .rx-hero-top{grid-template-columns:1fr}[data-dir="showcase"] .rx-hero-page .rx-hero-top > div:first-child{order:0}}
/* Clean: procedural, square, hairlines */
[data-dir="clean"] .rx-hero .rx-h1{font-weight:700}
[data-dir="clean"] .rx-ex-tabs{background:none;border-radius:0;padding:0;gap:0;border-bottom:1px solid var(--border);width:100%;justify-content:flex-start}
[data-dir="clean"] .rx-ex-tabs [role=tab]{border-radius:0;padding:0 22px 0 0;margin-right:22px;min-height:48px;border-bottom:2px solid transparent;margin-bottom:-1px;font-size:16.5px}
[data-dir="clean"] .rx-ex-tabs [role=tab]:hover{background:none;color:var(--accent-ink)}
[data-dir="clean"] .rx-ex-tabs [role=tab][aria-selected=true]{background:none;color:var(--accent-ink);border-bottom-color:var(--q-gold)}
[data-dir="clean"] .rx-head-c{display:block;text-align:left}
[data-dir="clean"] .rx-pan-fig .rx-frame,[data-dir="clean"] .rx-hero-page .rx-frame{border:1px solid var(--border);border-radius:6px}
[data-dir="clean"] .rx-tl{border-radius:var(--radius);background:var(--bg)}
[data-dir="clean"] .rx-rail::after,[data-dir="clean"] .rx-bar u,[data-dir="clean"] .rx-bar u i{border-radius:2px}
[data-dir="clean"] .rx-tl-in{background-image:linear-gradient(90deg,var(--border) 1px,transparent 1px);background-size:calc((100% - var(--k))/10) 100%;background-position:var(--k) 0;background-repeat:repeat-x}
[data-dir="clean"] .rx-rt{background:var(--bg);border-radius:var(--radius)}
@media(max-width:767px){[data-dir="clean"] .rx-ex-tabs{display:none;grid-template-columns:1fr 1fr;border-bottom:0;gap:0 16px}.rx-js[data-dir="clean"] .rx-ex-tabs{display:grid}[data-dir="clean"] .rx-ex-tabs [role=tab]{margin:0;padding:0;text-align:left;border-bottom:2px solid var(--border)}}
/* Press: editorial serif on warm paper, rules and plates */
[data-dir="press"] .rx-hero .rx-h1{font-weight:500;letter-spacing:-.015em}
[data-dir="press"] .rx-hero .q-lead,[data-dir="press"] .rx-head p,[data-dir="press"] .rx-head-c p,[data-dir="press"] .rx-pan-copy > p,[data-dir="press"] .rx-plan .q-lead{font-family:var(--q-serif)}
[data-dir="press"] .rx-stats b,[data-dir="press"] .rx-facts b,[data-dir="press"] .rx-figs b,[data-dir="press"] .rx-pan-copy h3,[data-dir="press"] .rx-res > h3{font-weight:500}
[data-dir="press"] .rx-frame{border-radius:0}
[data-dir="press"] .rx-hero-page .rx-frame,[data-dir="press"] .rx-pan-fig .rx-frame,[data-dir="press"] .rx-tk-fig .rx-frame{border:1px solid var(--fg);padding:8px;background:var(--card);border-radius:0}
[data-dir="press"] .rx-fig figcaption,[data-dir="press"] .rx-tk-fig figcaption{font-family:var(--q-serif);font-style:italic;font-size:14.5px}
[data-dir="press"] .rx-tl{border-radius:2px;border:0;border-top:2px solid var(--fg);border-bottom:1px solid var(--fg);background:transparent;padding-left:0;padding-right:0}
[data-dir="press"] .rx-rail::after,[data-dir="press"] .rx-bar u,[data-dir="press"] .rx-bar u i{border-radius:0}
[data-dir="press"] .rx-rail::after{height:10px;bottom:2px;background:none;border-bottom:1px solid var(--border)}
[data-dir="press"] .rx-bar u{background:transparent;box-shadow:inset 0 0 0 1px var(--fg)}
[data-dir="press"] .rx-bar u i,[data-dir="press"] .rx-seg u i{background:var(--fg)}
[data-dir="press"] .rx-seg u i{background:repeating-linear-gradient(90deg,var(--fg) 0 calc(25% - 2px),transparent calc(25% - 2px) 25%)}
[data-dir="press"] .rx-b .rx-bar u i{background:color-mix(in srgb,var(--fg) 45%,var(--bg))}
[data-dir="press"] .rx-grp-t{font-family:var(--q-serif);font-size:21px;font-weight:500}
[data-dir="press"] .rx-grp-t span{font-style:italic;font-size:15.5px}
[data-dir="press"] .rx-steps li{border-top:1px solid var(--fg)}
[data-dir="press"] .rx-steps h3{font-family:var(--q-serif);font-size:19px;font-weight:500}
[data-dir="press"] .rx-steps h3::before{font-style:italic;font-size:16px}
[data-dir="press"] .rx-figs li{border-left:1px solid var(--fg)}
[data-dir="press"] .rx-ex-tabs{background:none;border-radius:0;padding:0;border-top:1px solid var(--fg);border-bottom:1px solid var(--fg);width:100%;gap:0}
[data-dir="press"] .rx-ex-tabs [role=tab]{border-radius:0;font:500 19px/1 var(--q-serif);padding:0 26px;min-height:52px}
[data-dir="press"] .rx-ex-tabs [role=tab][aria-selected=true]{background:none;color:var(--accent-ink);font-style:italic;box-shadow:inset 0 -2px 0 var(--q-gold)}
[data-dir="press"] .rx-rt,[data-dir="press"] .rx-sheets li,[data-dir="press"] .rx-opts span{border-radius:2px}
[data-dir="press"] .rx-sheets li{box-shadow:none;border-color:var(--fg)}
[data-dir="press"] .rx-plan .q-form{box-shadow:none}
"""

WOW_JS = r"""(function(){var d=document.documentElement,rm=matchMedia('(prefers-reduced-motion: reduce)').matches;d.classList.add('rx-js');
var rv=[].slice.call(document.querySelectorAll('.rx-rv'));
if(rm||!('IntersectionObserver' in window)){rv.forEach(function(e){e.classList.add('rx-in')})}
else{var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('rx-in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});rv.forEach(function(e){io.observe(e)})}
/* two tracks: the scroll position is the clock. One way, so a section never empties again. */
var tr=[].slice.call(document.querySelectorAll('[data-rx-tracks]'));
function mark(el,p){[].forEach.call(el.querySelectorAll('[data-at]'),function(x){x.classList.toggle('rx-on',p>=parseFloat(x.getAttribute('data-at')))})}
if(tr.length&&!rm){tr.forEach(function(el){el._p=0;el.classList.add('rx-live');el.style.setProperty('--p','0');mark(el,0)});
var q=0;function tick(){q=0;tr.forEach(function(el){var c=el.querySelector('.rx-tl')||el,r=c.getBoundingClientRect(),vh=innerHeight,p=(vh*.86-r.top)/(vh*.62);p=Math.max(0,Math.min(1,p));if(p>el._p){el._p=p;el.style.setProperty('--p',p.toFixed(3));mark(el,p);if(p>=1)el.classList.add('rx-done')}})}
addEventListener('scroll',function(){if(!q)q=requestAnimationFrame(tick)},{passive:true});addEventListener('resize',tick);tick()}
/* explorer: tabs */
[].forEach.call(document.querySelectorAll('[data-rx-ex]'),function(w){var tabs=[].slice.call(w.querySelectorAll('[role=tab]')),pans=[].slice.call(w.querySelectorAll('[role=tabpanel]'));
function go(i,f){tabs.forEach(function(t,j){t.setAttribute('aria-selected',j===i?'true':'false');t.tabIndex=j===i?0:-1});pans.forEach(function(p,j){p.hidden=j!==i});if(f)tabs[i].focus()}
tabs.forEach(function(t,i){t.addEventListener('click',function(){go(i)});t.addEventListener('keydown',function(e){var k=e.key,n=tabs.length;if(k==='ArrowRight'||k==='ArrowDown'){e.preventDefault();go((i+1)%n,1)}else if(k==='ArrowLeft'||k==='ArrowUp'){e.preventDefault();go((i+n-1)%n,1)}else if(k==='Home'){e.preventDefault();go(0,1)}else if(k==='End'){e.preventDefault();go(n-1,1)}})});go(0)});
/* route guide: two answers pick one of the prepared results */
[].forEach.call(document.querySelectorAll('[data-rx-routes]'),function(w){var res=[].slice.call(w.querySelectorAll('[data-k]'));
function upd(){var b=w.querySelector('input[data-q="b"]:checked'),n=w.querySelector('input[data-q="n"]:checked'),k=(b?b.value:'')+'-'+(n?n.value:'');res.forEach(function(r){r.hidden=r.getAttribute('data-k')!==k})}
w.addEventListener('change',upd);upd()});
})();"""


# ------------------------------------------------------------------------------ helpers

def _img(ctx, src, alt, w, h, eager=False, focus=None):
    E = ctx["E"]
    style = f' style="object-position:{E(focus)}"' if focus else ""
    # "plain": no lazy loading and no priority hint, for images in panels that start hidden (a lazy one pops in on the tab change)
    load = "" if eager == "plain" else ' fetchpriority="high"' if eager else ' loading="lazy"'
    return f'<img src="{E(ctx["rel"](src))}"{ctx["srcset"](src)} alt="{E(alt)}" width="{w}" height="{h}"{load} decoding="async"{style}>'


def _btns(s, ctx):
    E, L = ctx["E"], ctx["L"]
    out = ""
    if s.get("primary"):
        out += f'<a class="q-btn" href="{E(L(s["primary"]["href"]))}">{E(s["primary"]["label"])}</a>'
    if s.get("secondary"):
        out += f'<a class="q-btn-ghost" href="{E(L(s["secondary"]["href"]))}">{E(s["secondary"]["label"])}<span style="width:22px;height:1px;background:currentColor;display:inline-block"></span></a>'
    return f'<div class="pv-btns">{out}</div>' if out else ""


# ------------------------------------------------------------------------------ hero

def _rxhero(s, ctx):
    """The promise hero. look: photo (photo-led band), ledger (text and what the first step returns),
    plate (editorial), page (inner pages: a cropped frame and three sourced facts)."""
    E, RAW = ctx["E"], ctx["RAW"]
    look = s.get("look", "photo")
    eyebrow = f'<div class="q-eyebrow">{E(s["eyebrow"])}</div>' if s.get("eyebrow") else ""
    h1 = f'<h1 class="q-h1 rx-h1">{RAW(s["heading"])}</h1>'
    lead = f'<div class="q-lead">{E(s.get("subhead", ""))}</div>'
    btns = _btns(s, ctx)
    note = f'<div class="pv-hero-note">{E(s["note"])}</div>' if s.get("note") else ""
    img = _img(ctx, s["image"], s.get("image_alt", ""), s.get("image_w", 1200), s.get("image_h", 800), eager=True, focus=s.get("focus"))
    stats = ""
    if s.get("stats"):
        stats = '<ul class="rx-stats">' + "".join(f"<li><b>{E(v)}</b><span>{E(l)}</span></li>" for v, l in s["stats"]) + "</ul>"
    affil = ""
    if s.get("affiliations"):
        a = s["affiliations"]
        affil = f'<div class="rx-affil"><p>{E(a.get("caption", ""))}</p><ul>' + "".join(f"<li>{E(x)}</li>" for x in a["items"]) + "</ul></div>"
    now = ""
    if s.get("now"):
        n = s["now"]
        now = (f'<div class="rx-now"><div class="k">{E(n["label"])}</div><dl>'
               f'<div><dt>{E(n["a"])}</dt><dd><i></i></dd></div><div><dt>{E(n["b"])}</dt><dd class="b"><i></i></dd></div></dl></div>')
    get = ""
    if s.get("receive"):
        r = s["receive"]
        get = f'<div class="rx-get"><div class="k">{E(r["label"])}</div><ul>' + "".join(f"<li>{E(x)}</li>" for x in r["items"]) + "</ul></div>"
    cap = f'<figcaption>{E(s["caption"])}</figcaption>' if s.get("caption") else ""
    sec = ctx["sec_open"](s, f"rx-hero rx-hero-{E(look)}")
    if look == "photo":
        return (f'{sec} <div class="q-container">{eyebrow}{h1}<div class="rx-hero-top">{lead}{btns}</div>'
                f'<figure class="rx-fig"><div class="rx-frame">{img}</div>{now}</figure>{stats}{note and f"<div style=text-align:center>{note}</div>"}{affil}</div></section>')
    if look == "ledger":
        return (f'{sec} <div class="q-container"><div class="rx-hero-top"><div>{eyebrow}{h1}{lead}{btns}{note}</div>'
                f'<figure class="rx-fig"><div class="rx-frame">{img}</div>{get}</figure></div>{stats}{affil}</div></section>')
    if look == "plate":
        return (f'{sec} <div class="q-container">{eyebrow}{h1}<div class="rx-hero-top"><figure class="rx-fig"><div class="rx-frame">{img}</div>{cap}</figure>'
                f'<div>{lead}{btns}{note}</div></div>{affil}</div></section>')
    facts = ""
    if s.get("facts"):
        facts = '<ul class="rx-facts">' + "".join(f"<li><b>{E(v)}</b><span>{E(l)}</span></li>" for v, l in s["facts"]) + "</ul>"
    return (f'{sec} <div class="q-container"><div class="rx-hero-top"><div>{eyebrow}{h1}{lead}{btns}{note}</div>'
            f'<figure class="rx-fig"><div class="rx-frame">{img}</div>{facts}</figure></div></div></section>')


# ------------------------------------------------------------------------------ two tracks

def _lane(E, key, bars, seg=False):
    out = ""
    for i, (label, a, b) in enumerate(bars):
        cls = "rx-bar rx-seg" if seg and i == 0 else "rx-bar"
        out += f'<div class="{cls}" style="--s:{a};--e:{b}"><span>{E(label)}</span><u><i></i></u></div>'
    return f'<div class="rx-lane"><div class="rx-lane-k">{E(key)}</div><div class="rx-rail">{out}</div></div>'


def _tracks(s, ctx):
    """Two-track build timeline. The scroll position is the clock: the plant and the site run together,
    the building is set and finished, and the site-built sequence is still going. All copy and every
    position on the axis come from the content file; with no JS the chart renders complete."""
    E = ctx["E"]
    a, b = s["modular"], s["sitebuilt"]
    figs = ""
    if s.get("figures"):
        figs = '<ul class="rx-figs">' + "".join(f"<li><b>{E(v)}</b><span>{E(l)}</span></li>" for v, l in s["figures"]) + "</ul>"
    intro = f'<p style="margin-top:16px">{E(s["intro"])}</p>' if s.get("intro") else ""
    left = f'<div><div class="q-eyebrow">{E(s.get("eyebrow", ""))}</div><h2 class="q-h2">{E(s["heading"])}</h2>{intro}{figs if s.get("image") else ""}</div>'
    if s.get("image"):
        cap = f'<figcaption>{E(s["caption"])}</figcaption>' if s.get("caption") else ""
        right = f'<figure class="rx-tk-fig rx-rv"><div class="rx-frame">{_img(ctx, s["image"], s.get("image_alt", ""), s.get("image_w", 600), s.get("image_h", 400))}</div>{cap}</figure>'
    else:
        right = figs
    head = f'<div class="rx-head">{left}{right}</div>'
    ga = (f'<div class="rx-grp rx-a"><p class="rx-grp-t">{E(a["title"])} <span>{E(a.get("sub", ""))}</span></p>'
          + _lane(E, a["lanes"][0]["key"], a["lanes"][0]["bars"], seg=True) + _lane(E, a["lanes"][1]["key"], a["lanes"][1]["bars"])
          + f'<div class="rx-flag"><div><b data-at="{a["end"]}" style="--at:{a["end"]}">{E(a["flag"])}</b></div></div></div>')
    gb = (f'<div class="rx-grp rx-b"><p class="rx-grp-t">{E(b["title"])} <span>{E(b.get("sub", ""))}</span></p>'
          + _lane(E, b["lanes"][0]["key"], b["lanes"][0]["bars"])
          + f'<div class="rx-flag"><div><b class="end" data-at="0.995">{E(b["flag"])}</b></div></div></div>')
    key = f'<p class="rx-key"><i aria-hidden="true"></i><span>{E(s["zone"])}</span></p>' if s.get("zone") else ""
    steps = "".join(f'<li data-at="{at}"><h3>{E(t)}</h3><p>{E(d)}</p></li>' for t, d, at in s.get("steps", []))
    steps = f'<ol class="rx-steps">{steps}</ol>' if steps else ""
    src = f'<p class="rx-src">{E(s["source"])}</p>' if s.get("source") else ""
    cls = "rx-tracks" + (" rx-tracks-photo" if s.get("image") else "")
    return (f'{ctx["sec_open"](s, cls)} <div class="q-container">{head}<div data-rx-tracks>'
            f'<div class="rx-tl" role="group" aria-label="{E(s.get("aria", s["heading"]))}"><div class="rx-tl-in"><div class="rx-zone" aria-hidden="true"></div>{ga}{gb}<div class="rx-ph" aria-hidden="true"></div></div>{key}</div>'
            f'{steps}</div>{src}</div></section>')


# ------------------------------------------------------------------------------ explorer

def _explorer(s, ctx):
    """Building-type explorer: one tab per market, each swapping the photograph, the copy, what is built
    and the ways to buy. With no JS every panel is shown in order under its own heading."""
    E, L = ctx["E"], ctx["L"]
    xid = E(s.get("id", "explorer"))
    tabs, pans = "", ""
    for i, it in enumerate(s["items"]):
        tabs += f'<button type="button" role="tab" id="{xid}-t{i}" aria-controls="{xid}-p{i}" aria-selected="{"true" if i == 0 else "false"}">{E(it["label"])}</button>'
        builds = "".join(f"<li>{E(x)}</li>" for x in it.get("builds", []))
        routes = "".join(f"<li>{E(t)}<span>{E(d)}</span></li>" for t, d in it.get("routes", []))
        pans += (f'<div class="rx-pan" role="tabpanel" id="{xid}-p{i}" aria-labelledby="{xid}-t{i}">'
                 f'<figure class="rx-pan-fig"><div class="rx-frame">{_img(ctx, it["image"], it.get("alt", ""), it.get("image_w", 600), it.get("image_h", 400), eager="plain", focus=it.get("focus"))}</div></figure>'
                 f'<div class="rx-pan-copy"><h3>{E(it["title"])}</h3><p>{E(it["body"])}</p>'
                 f'<div class="rx-pan-cols"><div class="b"><h4>{E(s.get("builds_label", "What is built"))}</h4><ul>{builds}</ul></div>'
                 f'<div><h4>{E(s.get("routes_label", "Ways to buy"))}</h4><ul>{routes}</ul></div></div>'
                 f'<a class="rx-link" href="{E(L(it["href"]))}">{E(it.get("link", "See more"))}</a></div></div>')
    intro = f'<p>{E(s["intro"])}</p>' if s.get("intro") else ""
    head = f'<div class="rx-head-c"><div class="q-eyebrow">{E(s.get("eyebrow", ""))}</div><h2 class="q-h2">{E(s["heading"])}</h2>{intro}</div>'
    return (f'{ctx["sec_open"](s, "rx-ex")} <div class="q-container">{head}<div data-rx-ex>'
            f'<div class="rx-ex-tabs" role="tablist" aria-label="{E(s.get("tabs_label", s["heading"]))}">{tabs}</div>{pans}</div></div></section>')


# ------------------------------------------------------------------------------ route guide

def _routes(s, ctx):
    """Two questions, one prepared answer. Every answer is written out in the content file; the script
    only chooses which one is visible. With no JS all of them are listed."""
    E, L = ctx["E"], ctx["L"]
    rid = E(s.get("id", "routes"))

    def opts(q, items, legend):
        o = "".join(f'<label><input type="radio" name="{rid}-{q}" data-q="{q}" value="{E(k)}"{" checked" if i == 0 else ""}><span>{E(lbl)}</span></label>' for i, (k, lbl) in enumerate(items))
        return f'<fieldset><legend>{E(legend)}</legend><div class="rx-opts">{o}</div></fieldset>'

    qs = f'<div class="rx-rt-q">{opts("b", s["buyers"], s["buyer_legend"])}{opts("n", s["needs"], s["need_legend"])}</div>'
    res = ""
    for r in s["results"]:
        buy = "".join(f"<li><strong>{E(t)}</strong><p>{E(d)}</p></li>" for t, d in r["buy"])
        res += (f'<div class="rx-res" data-k="{E(r["key"])}"><h3>{E(r["title"])}</h3><div class="rx-res-g">'
                f'<div><h4>{E(s["labels"][0])}</h4><strong>{E(r["build"][0])}</strong><p>{E(r["build"][1])}</p></div>'
                f'<div><h4>{E(s["labels"][1])}</h4><ul>{buy}</ul></div>'
                f'<div><h4>{E(s["labels"][2])}</h4><strong>{E(s["first"][0])}</strong><p>{E(s["first"][1])}</p>'
                f'<a class="q-btn" href="{E(L(s["cta"]["href"]))}">{E(s["cta"]["label"])}</a></div></div></div>')
    intro = f'<p>{E(s["intro"])}</p>' if s.get("intro") else ""
    head = f'<div class="rx-head"><div><div class="q-eyebrow">{E(s.get("eyebrow", ""))}</div><h2 class="q-h2">{E(s["heading"])}</h2></div>{intro}</div>'
    src = f'<p class="rx-src">{E(s["source"])}</p>' if s.get("source") else ""
    return f'{ctx["sec_open"](s, "rx-routes")} <div class="q-container">{head}<div class="rx-rt rx-rv" data-rx-routes>{qs}<div aria-live="polite">{res}</div></div>{src}</div></section>'


# ------------------------------------------------------------------------------ planning request

_SHEET = {
    "floor": '<rect x="6" y="8" width="52" height="32"/><path d="M26 8v14M26 30v10M6 24h12M40 40V24h18"/><path class="a" d="M26 22a8 8 0 0 1 8 8"/>',
    "site": '<path d="M5 12 54 6l5 30-50 6z"/><rect class="a" x="20" y="16" width="22" height="13"/><path d="M5 12l4 30" stroke-dasharray="3 3"/>',
    "render": '<path d="M4 40h56M10 40V20l22-10 22 10v20"/><path class="a" d="M6 21 32 9l26 12"/><path d="M18 26h8v8h-8zM38 26h8v8h-8zM28 40V30h8v10"/>',
    "spec": '<rect x="12" y="5" width="40" height="38"/><path d="M19 14h26M19 21h26M19 28h18"/><path class="a" d="M19 35h10"/>',
    "budget": '<rect x="10" y="5" width="44" height="38"/><path d="M17 14h14M17 21h14M17 28h14M40 14h8M40 21h8M40 28h8"/><path class="a" d="M17 36h31"/>',
}


def _plan(s, ctx):
    """The no cost planning request: what comes back, what happens next, and the form."""
    E, L = ctx["E"], ctx["L"]
    brand = ctx["brand"]
    fid = E(s.get("id", "plan"))
    sheets = "".join(f'<li><svg viewBox="0 0 64 48" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round" aria-hidden="true">{_SHEET.get(k, _SHEET["spec"])}</svg><b>{E(t)}</b></li>' for k, t in s.get("sheets", []))
    sheets = f'<ul class="rx-sheets" aria-label="{E(s.get("sheets_label", "What you receive"))}">{sheets}</ul>' if sheets else ""
    nxt = "".join(f"<li><span><b>{E(t)}</b> {E(d)}</span></li>" for t, d in s.get("next", []))
    nxt = f'<ol class="rx-next">{nxt}</ol>' if nxt else ""
    fields = ""
    for i, f in enumerate(s["fields"]):
        label, kind, auto, wide = f[0], f[1], f[2], (len(f) > 3 and f[3])
        cls = "f w" if wide else "f"
        if kind == "select":
            o = "".join(f"<option>{E(x)}</option>" for x in s.get("options", []))
            fields += f'<div class="{cls}"><label for="{fid}-{i}">{E(label)}</label><select id="{fid}-{i}">{o}</select></div>'
        else:
            fields += f'<div class="{cls}"><label for="{fid}-{i}">{E(label)}</label><input id="{fid}-{i}" type="{E(kind)}"{f" autocomplete={E(auto)}" if auto else ""}></div>'
    ft = f'<p class="ft">{E(s["form_title"])}</p>' if s.get("form_title") else ""
    form = (f'<form class="q-form rx-rv" onsubmit="return false">{ft}{fields}<div class="f w"><input type="submit" class="hs-button" value="{E(s.get("submit", "Send"))}">'
            f'<p class="pv-form-note">{E(s.get("note", ""))}</p></div></form>')
    call = f'<p class="rx-call">{E(s.get("call_label", "Or call"))} <a href="{E(L(brand["phone_href"]))}">{E(brand["phone"])}</a></p>'
    return (f'{ctx["sec_open"](s, "rx-plan")} <div class="q-container rx-plan-g"><div><div class="q-eyebrow">{E(s.get("eyebrow", ""))}</div>'
            f'<h2 class="q-h2">{E(s["heading"])}</h2><div class="q-lead">{E(s.get("body", ""))}</div>{sheets}{nxt}{call}</div>{form}</div></section>')


RENDER_WOW = {"rxhero": _rxhero, "tracks": _tracks, "explorer": _explorer, "routes": _routes, "plan": _plan}
