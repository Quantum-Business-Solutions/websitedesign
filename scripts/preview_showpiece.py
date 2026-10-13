"""Showpiece sections for scripts/preview.py: the layer that makes a product page feel like a technology company.

Section types registered in RENDER_EXTRA3:
  product3d    dark stage hero with a turnable 3D model, floating spec tags, glow and grid
  countband    dark band of numbers that count up once on scroll
  ticker       a slow marquee of capabilities (static when motion is reduced)
  pulseflow    the monitoring pipeline: five nodes, travelling pulses, an example live feed
  itdirector   before / after slider, the stressed IT director to the relieved one, real logo in a thought bubble
  photoband    a photograph with drifting steam and a few honest lines beside it
  savingstease a one-slider teaser that sends the visitor to the Office Overview
  overview     the Full Office Overview and Analysis: seven service lines, live savings, a written result

Rules held from design/guardrails.md: no em dashes, nothing under 13px, tap targets 44px, no opacity on text,
motion respects prefers-reduced-motion, every number shown as an estimate says so. The Overview rates are DRAFT
ranges for Kelly to confirm; the page says so and the assessment replaces them with measured figures.
"""
from __future__ import annotations

import json

MV_SRC = "https://ajax.googleapis.com/ajax/libs/model-viewer/3.5.0/model-viewer.min.js"

CSS3 = r'''
/* ===== showpiece layer ===== */
@property --p{syntax:"<number>";inherits:true;initial-value:100}
.pv-progress{position:fixed;left:0;top:0;height:3px;width:100%;z-index:120;transform-origin:0 50%;transform:scaleX(0);background:linear-gradient(90deg,var(--q-gold),var(--q-gold-bright,var(--q-gold)));pointer-events:none}
.pv-dark{background:var(--chrome-bg);color:#fff;position:relative;overflow:hidden;isolation:isolate}
.pv-dark .q-h2,.pv-dark h2,.pv-dark h3{color:#fff}
.pv-dark .q-eyebrow{color:var(--q-gold)}.pv-dark .q-eyebrow::before{background:var(--q-gold)}
.pv-grid-bg{position:absolute;inset:0;z-index:-2;background-image:linear-gradient(rgba(255,255,255,.055) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.055) 1px,transparent 1px);background-size:56px 56px;mask-image:radial-gradient(80% 90% at 70% 40%,#000,transparent 80%);-webkit-mask-image:radial-gradient(80% 90% at 70% 40%,#000,transparent 80%);animation:pv-gridmove 24s linear infinite}
@keyframes pv-gridmove{to{background-position:56px 56px,56px 56px}}
.pv-orb{position:absolute;border-radius:50%;filter:blur(70px);z-index:-1;opacity:.55;animation:pv-orb 16s ease-in-out infinite}
.pv-orb.a{width:480px;height:480px;right:-80px;top:-120px;background:color-mix(in srgb,var(--q-gold) 70%,transparent)}
.pv-orb.b{width:380px;height:380px;left:-120px;bottom:-140px;background:rgba(60,110,255,.38);animation-delay:-8s}
@keyframes pv-orb{50%{transform:translate(40px,-30px) scale(1.12)}}

/* video hero: the film sits in its own frame, no words over the footage */
.pv-lh.vid .q-container{grid-template-columns:minmax(0,1.08fr) minmax(0,1fr);gap:clamp(28px,3.4vw,56px);padding-top:72px;padding-bottom:72px;align-items:center}
.pv-lh.vid{padding:0}
.pv-lh.vbg{min-height:min(88vh,820px);display:flex;align-items:center}
.pv-lh.vbg .bg video{opacity:1;object-position:62% 50%}
.pv-lh.vbg .bg::after{background:linear-gradient(90deg,rgba(0,5,45,.94) 0%,rgba(0,5,45,.82) 34%,rgba(0,5,45,.34) 62%,rgba(0,5,45,.08) 100%),linear-gradient(180deg,rgba(0,5,45,.5) 0%,transparent 22%,transparent 78%,rgba(0,5,45,.7) 100%)}
.pv-lh.vbg .q-container{grid-template-columns:minmax(0,700px);justify-content:start;padding-top:88px;padding-bottom:88px}
.pv-lh.vbg .q-h1{font-size:clamp(36px,4.1vw,56px);line-height:1.06;margin-top:20px;letter-spacing:-.02em}
.pv-lh.vbg .q-lead{margin-top:22px;max-width:560px;line-height:1.55}
.pv-lh.vbg .pv-btns{margin-top:30px}
.pv-lh.vbg .lane{margin-top:22px;gap:10px}
.pv-lh.vbg .pv-hero-stats{margin-top:38px;max-width:640px}
.pv-lh.vbg .bg video{object-position:72% 50%}
.pv-lh.vbg .net{opacity:.35}
.pv-lh.vbg .lane{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;max-width:640px;margin-top:26px;align-items:stretch}
.pv-lh.vbg .lane .k{grid-column:1/-1;margin:0 0 2px}
.pv-lh.vbg .lane a{justify-content:center;text-align:center;min-height:46px;padding:0 10px;white-space:nowrap;background:rgba(255,255,255,.08);border-color:rgba(255,255,255,.3);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);transition:background .2s,border-color .2s,transform .2s}
.pv-lh.vbg .lane a:hover{background:rgba(255,255,255,.16);transform:translateY(-2px)}
@media(max-width:640px){.pv-lh.vbg .lane{grid-template-columns:repeat(2,minmax(0,1fr))}}

.pv-lh.vbg .q-container,.pv-p3d:has(.pv-p3d-stage.photo) > .q-container{width:100%}
@media(max-width:820px){.pv-lh.vbg .bg::after{background:linear-gradient(180deg,rgba(0,5,45,.9),rgba(0,5,45,.72))}}

.pv-lh.vid .q-h1{font-size:clamp(34px,3.6vw,54px);line-height:1.05;margin-top:16px;max-width:none}
.pv-lh.vid .q-lead{max-width:560px;margin-top:18px;font-size:clamp(16px,1.25vw,18px)}
.pv-lh.vid .lane{margin-top:18px}
.pv-lh.vid .pv-hero-stats{margin-top:26px}
.pv-lh.vid .pv-hero-stats b{font-size:clamp(22px,2vw,30px)}
.vframe{position:relative;border-radius:28px;overflow:hidden;aspect-ratio:16/9;border:1px solid rgba(255,255,255,.22);box-shadow:0 60px 130px rgba(0,0,0,.6),0 0 0 10px rgba(255,255,255,.04),0 0 90px color-mix(in srgb,var(--q-gold) 28%,transparent);background:#050a24}
.vframe video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}
.vframe::after{content:"";position:absolute;inset:0;border-radius:inherit;pointer-events:none;background:linear-gradient(180deg,rgba(0,5,69,.0) 62%,rgba(0,5,69,.55) 100%);box-shadow:inset 0 0 0 1px rgba(255,255,255,.1)}
.vtag{position:absolute;left:16px;bottom:16px;z-index:2;display:inline-flex;align-items:center;gap:10px;background:rgba(8,14,40,.72);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border:1px solid rgba(255,255,255,.22);color:#fff;border-radius:999px;padding:9px 16px 9px 12px;font-size:13.5px;font-weight:600}
.vtag i{width:10px;height:10px;border-radius:50%;background:var(--q-gold);animation:pv-pulse 2.2s ease-out infinite}
@media(max-width:1024px){.pv-lh.vid .q-container{grid-template-columns:1fr}.vframe{max-width:640px}}
.pv-wheel .hub-orb{animation:pv-orbfloat 6s ease-in-out infinite;filter:drop-shadow(0 0 14px rgba(99,210,58,.55))}
@keyframes pv-orbfloat{50%{transform:scale(1.045)}}
@media(prefers-reduced-motion:reduce){.pv-wheel .hub-orb{animation:none}}
/* product3d */
.pv-p3d{padding:clamp(56px,7vw,104px) 0}
.pv-p3d-grid{display:grid;grid-template-columns:1fr 1.05fr;gap:clamp(24px,4vw,64px);align-items:center}
.pv-p3d .q-h1{color:#fff;margin:18px 0 0}.pv-p3d .q-h1 em{color:var(--q-gold);font-style:normal}
.pv-p3d .q-lead{color:rgba(255,255,255,.86);margin-top:20px;max-width:520px}
.pv-p3d-btns{display:flex;gap:14px;flex-wrap:wrap;align-items:center;margin-top:30px}
.pv-p3d .q-btn-ghost{color:#fff}
.pv-p3d-facts{list-style:none;padding:0;margin:34px 0 0;display:grid;grid-template-columns:repeat(3,1fr);gap:14px;max-width:560px}
.pv-p3d-facts li{border:1px solid rgba(255,255,255,.16);background:rgba(255,255,255,.06);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);border-radius:var(--radius);padding:14px 16px}
.pv-p3d-facts b{display:block;font-family:var(--q-serif);font-size:26px;line-height:1.1;color:#fff;font-variant-numeric:tabular-nums}
.pv-p3d-facts span{display:block;font-size:13.5px;color:rgba(255,255,255,.78);margin-top:4px;line-height:1.35}
.pv-p3d-stage{position:relative;aspect-ratio:1/1;max-height:640px;width:100%}
.pv-p3d-stage model-viewer,.pv-p3d-stage > img.fb{width:100%;height:100%;display:block;--poster-color:transparent;position:relative;z-index:2}
.pv-p3d-stage > img.fb{object-fit:contain;animation:pv-float 8s ease-in-out infinite}
.pv-p3d-stage model-viewer:defined ~ img.fb{display:none}
.pv-p3d-ring{position:absolute;left:8%;right:8%;bottom:6%;height:16%;border-radius:50%;z-index:1;background:radial-gradient(ellipse at center,color-mix(in srgb,var(--q-gold) 55%,transparent),transparent 68%);filter:blur(10px);animation:pv-ring 6s ease-in-out infinite}
.pv-p3d-ring::before,.pv-p3d-ring::after{content:"";position:absolute;inset:-10%;border-radius:50%;border:1px solid rgba(255,255,255,.22);transform:scaleY(.32)}
.pv-p3d-ring::after{inset:-30%;border-color:rgba(255,255,255,.1)}
@keyframes pv-ring{50%{opacity:.7;transform:scale(1.06)}}
.pv-p3d-tag{position:absolute;z-index:3;display:flex;align-items:center;gap:10px;background:rgba(8,14,40,.72);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border:1px solid rgba(255,255,255,.2);border-radius:999px;padding:8px 16px 8px 12px;box-shadow:0 14px 34px rgba(0,0,0,.4);animation:pv-float 7s ease-in-out infinite;white-space:nowrap}
.pv-p3d-tag i{width:10px;height:10px;border-radius:50%;background:var(--q-gold);box-shadow:0 0 0 0 color-mix(in srgb,var(--q-gold) 70%,transparent);animation:pv-pulse 2.2s ease-out infinite;flex:0 0 auto}
.pv-p3d-tag b{font-size:13.5px;font-weight:600;color:#fff}.pv-p3d-tag em{font-style:normal;font-size:13.5px;color:var(--q-gold);font-weight:700}
.pv-p3d-tag:nth-of-type(2){animation-delay:-1.7s}.pv-p3d-tag:nth-of-type(3){animation-delay:-3.1s}.pv-p3d-tag:nth-of-type(4){animation-delay:-4.4s}
@keyframes pv-pulse{70%{box-shadow:0 0 0 12px transparent}100%{box-shadow:0 0 0 0 transparent}}
.pv-p3d-stage.photo{aspect-ratio:4/3}.pv-p3d-stage.photo.vid{aspect-ratio:16/9}.pv-p3d-stage.photo.vid .pv-p3d-tag{display:none}.pv-p3d-stage.photo > video.fb{object-fit:cover;border-radius:28px;border:1px solid rgba(255,255,255,.2);box-shadow:0 40px 90px rgba(0,0,0,.5);width:100%;height:100%}
.pv-p3d-stage.photo > img.fb{object-fit:cover;border-radius:28px;border:1px solid rgba(255,255,255,.2);box-shadow:0 40px 90px rgba(0,0,0,.5);animation:none}.pv-p3d-stage.photo .pv-p3d-ring{display:none}.pv-p3d-stage.photo .pv-p3d-hint{display:none}
.pv-p3d:has(.pv-p3d-stage.photo){position:relative;overflow:hidden;isolation:isolate;min-height:min(84vh,780px);display:flex;align-items:center;padding:clamp(64px,7vw,96px) 0}
.pv-p3d:has(.pv-p3d-stage.photo) .pv-p3d-grid{grid-template-columns:minmax(0,680px)}
.pv-p3d-stage.photo{position:absolute;inset:0;aspect-ratio:auto;max-height:none;z-index:-1}
.pv-p3d-stage.photo.vid{aspect-ratio:auto}
.pv-p3d-stage.photo > img.fb,.pv-p3d-stage.photo > video.fb{position:absolute;inset:0;width:100%;height:100%;border-radius:0;border:0;box-shadow:none;object-fit:cover;object-position:70% 50%}
.pv-p3d-stage.photo::after{content:"";position:absolute;inset:0;z-index:3;pointer-events:none;background:linear-gradient(90deg,rgba(0,5,45,.94) 0%,rgba(0,5,45,.82) 36%,rgba(0,5,45,.3) 66%,rgba(0,5,45,.06) 100%),linear-gradient(180deg,rgba(0,5,45,.5) 0%,transparent 24%,transparent 76%,rgba(0,5,45,.7) 100%)}
.pv-p3d:has(.pv-p3d-stage.photo) .q-h1{font-size:clamp(34px,3.8vw,54px);line-height:1.07;letter-spacing:-.02em}
.pv-p3d:has(.pv-p3d-stage.photo) .q-lead{font-size:clamp(16px,1.3vw,19px);line-height:1.55;max-width:560px}
.pv-p3d:has(.pv-p3d-stage.photo) .pv-p3d-hint{display:none}
@media(max-width:820px){.pv-p3d-stage.photo::after{background:linear-gradient(180deg,rgba(0,5,45,.9),rgba(0,5,45,.74))}}
.pv-hascut{position:relative;overflow:hidden;min-height:min(80vh,720px);display:flex;align-items:center}
.pv-hascut .pv-p3d-grid{grid-template-columns:minmax(0,600px)}
.pv-hascut > .q-container{width:100%;position:relative;z-index:2}
.pv-cx{position:absolute;z-index:4;right:max(1vw,0px);top:50%;width:min(54vw,720px);aspect-ratio:var(--cw)/var(--ch);transform:translate(130%,-50%) rotate(14deg);opacity:0;pointer-events:none}
.pv-cx video,.pv-cx img.still{position:absolute;inset:0;width:100%;height:100%;display:block}
.pv-cx img.still{display:none}
.pv-hascut.in .pv-cx{animation:pv-cx-in 1.5s cubic-bezier(.2,.85,.25,1) .1s forwards}
@keyframes pv-cx-in{0%{transform:translate(130%,-50%) rotate(14deg);opacity:0}25%{opacity:1}100%{transform:translate(0,-50%) rotate(0);opacity:1}}
.pv-cx .steam{position:absolute;width:22%;height:32%;opacity:0;pointer-events:none}
.pv-hascut.in .pv-cx .steam{animation:pv-cx-fade .8s 1.8s forwards}
@keyframes pv-cx-fade{to{opacity:1}}
.pv-cx .steam i{position:absolute;bottom:0;left:calc(var(--x)*1%);width:16%;height:100%;border-radius:50%;background:radial-gradient(ellipse at 50% 80%,rgba(255,255,255,.55),rgba(255,255,255,0) 68%);filter:blur(9px);opacity:0;animation:pv-steam 4.2s var(--d) infinite ease-out}
@keyframes pv-steam{0%{transform:translateY(25%) scaleX(.7);opacity:0}25%{opacity:.7}100%{transform:translateY(-70%) translateX(var(--dx)) scaleX(1.5);opacity:0}}
@media(max-width:820px){.pv-hascut{align-items:flex-start;min-height:780px}.pv-cx{top:auto;bottom:6px;right:50%;width:min(88vw,440px);transform:translate(50%,40%) rotate(10deg)}@keyframes pv-cx-in{0%{transform:translate(50%,60%) rotate(10deg);opacity:0}25%{opacity:1}100%{transform:translate(50%,0) rotate(0);opacity:1}}}
@media(prefers-reduced-motion:reduce){.pv-cx{opacity:1;transform:translate(0,-50%);animation:none!important}.pv-hascut.in .pv-cx{animation:none}.pv-cx video{display:none}.pv-cx img.still{display:block}.pv-cx .steam{opacity:1}.pv-cx .steam i{animation:none;opacity:.35}}
.pv-cx img.still.static{display:block;object-fit:contain;filter:drop-shadow(0 40px 50px rgba(0,0,0,.55));animation:pv-float 8s ease-in-out infinite}
@media(prefers-reduced-motion:reduce){.pv-cx img.still.static{animation:none}}
.pv-ice{position:absolute;inset:0;z-index:5;pointer-events:none;perspective:900px;overflow:hidden}
@media(prefers-reduced-motion:reduce){.pv-ice{display:none}}
.pv-cx.tall{width:auto;height:min(84%,600px);right:max(8vw,0px)}
@media(max-width:820px){.pv-cx.tall{height:58%;width:auto}}
.pv-p3d-hint{position:absolute;right:4px;bottom:0;z-index:3;font-size:13px;color:rgba(255,255,255,.8);letter-spacing:.08em;text-transform:uppercase}

/* countband */
.pv-cnt{padding:clamp(48px,6vw,80px) 0}
.pv-cnt-grid{display:grid;grid-template-columns:repeat(var(--n,4),1fr);gap:28px;text-align:center}
.pv-cnt-grid > div{position:relative;padding:8px 0}
.pv-cnt-grid > div + div::before{content:"";position:absolute;left:-14px;top:12%;bottom:12%;width:1px;background:rgba(255,255,255,.16)}
.pv-cnt-grid b{display:block;font-family:var(--q-serif);font-size:clamp(40px,5.2vw,72px);line-height:1;color:#fff;font-variant-numeric:tabular-nums;letter-spacing:-.02em}
.pv-cnt-grid b small{font-size:.5em;color:var(--q-gold);margin-left:2px}
.pv-cnt-grid span{display:block;margin-top:10px;font-size:15px;color:rgba(255,255,255,.82);line-height:1.4}

/* ticker */
.pv-tick{background:var(--bg-alt);border-block:1px solid var(--border);overflow:hidden;padding:18px 0}
.pv-tick-track{display:flex;width:max-content;animation:pv-tick 46s linear infinite}
.pv-tick:hover .pv-tick-track{animation-play-state:paused}
.pv-tick ul{list-style:none;margin:0;padding:0 0 0 0;display:flex;gap:0;flex:0 0 auto}
.pv-tick li{display:inline-flex;align-items:center;gap:22px;padding-right:22px;font-size:15px;font-weight:600;color:var(--fg);white-space:nowrap}
.pv-tick li::after{content:"";width:8px;height:8px;border-radius:50%;background:var(--q-gold);flex:0 0 auto}
@keyframes pv-tick{to{transform:translateX(-50%)}}

/* pulseflow */
.pv-pf{padding:clamp(56px,7vw,104px) 0}
.pv-pf-head{max-width:760px;margin:0 auto 48px;text-align:center}
.pv-pf-head p{color:rgba(255,255,255,.84);font-size:18px;line-height:1.6;margin:16px auto 0}
.pv-pf-rail{display:grid;grid-template-columns:repeat(5,1fr);gap:0;position:relative;margin:0 0 34px;padding:0;list-style:none}
.pv-pf-rail::before{content:"";position:absolute;left:10%;right:10%;top:40px;height:2px;background:rgba(255,255,255,.14)}
.pv-pf-rail::after{content:"";position:absolute;left:10%;top:38px;width:90px;height:6px;border-radius:6px;background:linear-gradient(90deg,transparent,var(--q-gold),transparent);filter:blur(1px);animation:pv-travel 4.2s linear infinite}
@keyframes pv-travel{from{transform:translateX(0);opacity:0}10%{opacity:1}90%{opacity:1}to{transform:translateX(calc(var(--w,900px) - 90px));opacity:0}}
.pv-pf-rail li{position:relative;text-align:center;padding:0 10px}
.pv-pf-rail button{all:unset;cursor:pointer;display:block;width:100%;text-align:center;min-height:44px}
.pv-pf-rail button:focus-visible{outline:3px solid #fff;outline-offset:6px;border-radius:12px}
.pv-pf-ico{width:80px;height:80px;border-radius:24px;margin:0 auto;display:grid;place-items:center;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.2);color:#fff;transition:transform .35s,background .35s,border-color .35s,box-shadow .35s}
.pv-pf-ico svg{width:34px;height:34px;stroke:currentColor;fill:none;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}
.pv-pf-rail li.on .pv-pf-ico{transform:translateY(-6px) scale(1.06);background:var(--q-gold);border-color:var(--q-gold);color:var(--cta-fg);box-shadow:0 18px 40px color-mix(in srgb,var(--q-gold) 45%,transparent)}
.pv-pf-rail h3{font-size:17px;margin:16px 0 4px;color:#fff}.pv-pf-rail p{font-size:14.5px;line-height:1.5;color:rgba(255,255,255,.8);margin:0}
.pv-pf-feed{max-width:860px;margin:0 auto;border-radius:var(--radius);border:1px solid rgba(255,255,255,.18);background:rgba(4,8,24,.7);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);overflow:hidden;box-shadow:0 30px 70px rgba(0,0,0,.45)}
.pv-pf-bar{display:flex;align-items:center;gap:8px;padding:12px 16px;border-bottom:1px solid rgba(255,255,255,.12);font-size:13px;color:rgba(255,255,255,.8);letter-spacing:.06em;text-transform:uppercase}
.pv-pf-bar i{width:10px;height:10px;border-radius:50%;background:#ff5f57}.pv-pf-bar i+i{background:#febc2e}.pv-pf-bar i+i+i{background:#28c840}.pv-pf-bar span{margin-left:auto}
.pv-pf-log{list-style:none;margin:0;padding:16px 18px;min-height:228px;font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:14px;line-height:1.75;color:#d9e4ff}
.pv-pf-log li{display:flex;gap:12px;opacity:1;animation:pv-in .5s ease both}
.pv-pf-log time{color:rgba(255,255,255,.62);flex:0 0 auto}.pv-pf-log b{color:var(--q-gold);font-weight:600}
.pv-pf-log .ok{color:#7ff0a8}
@keyframes pv-in{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.pv-pf-note{max-width:860px;margin:14px auto 0;font-size:13.5px;color:rgba(255,255,255,.72);text-align:center}

/* itdirector */
.pv-ita{max-width:1120px;margin:0 auto}
.pv-ita-frame{position:relative;aspect-ratio:16/9;border-radius:calc(var(--radius) + 8px);overflow:hidden;background:#05070f;border:1px solid var(--border);box-shadow:0 40px 90px rgba(0,5,69,.28);--p:100;transition:--p 1.1s cubic-bezier(.65,0,.25,1);user-select:none;-webkit-user-select:none;touch-action:pan-y}
.pv-ita-frame img.im{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}
.pv-ita-frame img.before{clip-path:inset(0 calc(100% - var(--p) * 1%) 0 0)}
.pv-ita-split{position:absolute;top:0;bottom:0;left:calc(var(--p) * 1%);width:3px;margin-left:-1.5px;background:#fff;box-shadow:0 0 0 1px rgba(0,0,0,.2),0 0 24px rgba(255,255,255,.7);z-index:4;pointer-events:none}
.pv-ita-split::after{content:"";position:absolute;top:50%;left:50%;width:48px;height:48px;margin:-24px 0 0 -24px;border-radius:50%;background:#fff;box-shadow:0 8px 24px rgba(0,0,0,.4);background-image:linear-gradient(90deg,transparent 14px,#06124a 14px 17px,transparent 17px 31px,#06124a 31px 34px,transparent 34px)}
.pv-ita-range{position:absolute;inset:0;width:100%;height:100%;opacity:0;cursor:ew-resize;z-index:5;margin:0}
.pv-ita-label{position:absolute;top:16px;z-index:3;font-size:13.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;padding:9px 16px;border-radius:999px;backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px)}
.pv-ita-label.b{left:16px;background:rgba(160,20,20,.82);color:#fff}.pv-ita-label.a{right:16px;background:rgba(10,120,60,.88);color:#fff}
.pv-ita-bubble{position:absolute;z-index:3;left:27%;top:2.5%;width:min(27%,300px);aspect-ratio:2.1/1;display:grid;place-items:center;background:var(--chrome-bg);border:3px solid #fff;box-sizing:border-box;border-radius:50%/56%;box-shadow:0 22px 50px rgba(0,0,0,.45);transform:scale(.2);transform-origin:18% 100%;opacity:0;transition:transform .7s cubic-bezier(.3,1.6,.5,1),opacity .35s;pointer-events:none}
.pv-ita-bubble img{width:68%;height:auto;display:block}
.pv-ita-dot{position:absolute;z-index:3;background:var(--chrome-bg);border:2px solid #fff;box-sizing:border-box;border-radius:50%;box-shadow:0 8px 20px rgba(0,0,0,.4);transform:scale(0);opacity:0;transition:transform .45s cubic-bezier(.3,1.6,.5,1),opacity .3s;pointer-events:none}
.pv-ita-dot.d1{left:31.4%;top:22.6%;width:2.2%;aspect-ratio:1}.pv-ita-dot.d2{left:30%;top:27%;width:1.3%;aspect-ratio:1}
.pv-ita-frame.relieved .pv-ita-bubble{transform:scale(1);opacity:1}.pv-ita-frame.relieved .pv-ita-dot{transform:scale(1);opacity:1}.pv-ita-frame.relieved .pv-ita-dot.d1{transition-delay:.1s}.pv-ita-frame.relieved .pv-ita-bubble{transition-delay:.3s}
.pv-ita-chips{list-style:none;margin:0;padding:0;position:absolute;left:16px;right:16px;bottom:16px;display:flex;gap:10px;flex-wrap:wrap;z-index:3;pointer-events:none;transition:opacity .45s,transform .45s}
.pv-ita-chips li{background:rgba(8,14,40,.8);border:1px solid rgba(255,255,255,.28);color:#fff;border-radius:999px;padding:9px 16px;font-size:14px;font-weight:600;backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px)}
.pv-ita-chips.b li{border-color:rgba(255,125,125,.85)}.pv-ita-chips.a li{border-color:rgba(125,240,175,.9)}
.pv-ita-frame:not(.relieved) .pv-ita-chips.a,.pv-ita-frame.relieved .pv-ita-chips.b{opacity:0;transform:translateY(10px)}
.pv-ita-ctl{display:flex;justify-content:center;gap:12px;margin-top:22px;flex-wrap:wrap}
.pv-ita-ctl button{min-height:48px;padding:0 24px;border-radius:999px;border:1px solid var(--border);background:var(--card);color:var(--fg);font:inherit;font-weight:600;font-size:15px;cursor:pointer}
.pv-ita-ctl button[aria-pressed=true]{background:var(--chrome-bg);color:#fff;border-color:var(--chrome-bg)}
.pv-ita-cap{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:26px}
.pv-ita-cap > div{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:22px 24px}
.pv-ita-cap h3{font-family:var(--q-serif);font-size:20px;margin:0 0 8px;color:var(--fg)}.pv-ita-cap p{margin:0;font-size:15.5px;line-height:1.65;color:var(--fg-muted)}
.pv-ita-note{font-size:13.5px;color:var(--fg-muted);text-align:center;margin-top:16px}

/* photoband */
.pv-pb{display:grid;grid-template-columns:5fr 7fr;gap:clamp(24px,4vw,60px);align-items:center}
.pv-pb-img{position:relative;border-radius:calc(var(--radius) + 8px);overflow:hidden;aspect-ratio:16/9;border:1px solid var(--border);box-shadow:0 40px 90px rgba(0,5,69,.22);order:2}
.pv-pb-img video{width:100%;height:100%;object-fit:cover;display:block}
.pv-pb-img img{width:100%;height:100%;object-fit:cover;display:block;transform:scale(1.04);transition:transform 1.6s cubic-bezier(.2,.7,.2,1)}
.pv-pb-img:hover img{transform:scale(1.09)}
.pv-steam{position:absolute;width:5.5%;aspect-ratio:1/2;pointer-events:none}
.pv-steam i{position:absolute;left:50%;bottom:0;width:70%;height:55%;margin-left:-35%;border-radius:50%;background:radial-gradient(ellipse at center,rgba(255,255,255,.55),transparent 70%);filter:blur(7px);opacity:0;animation:pv-steam 4.6s ease-in infinite}
.pv-steam i:nth-child(2){animation-delay:-1.5s;margin-left:-10%}.pv-steam i:nth-child(3){animation-delay:-3s;margin-left:-55%}
@keyframes pv-steam{0%{transform:translateY(0) scale(.6);opacity:0}25%{opacity:.7}100%{transform:translateY(-190%) scale(1.5);opacity:0}}
.pv-pb ul{list-style:none;padding:0;margin:24px 0 0;display:grid;gap:12px}
.pv-pb li{display:flex;gap:14px;align-items:flex-start;font-size:16.5px;line-height:1.55;color:var(--fg)}
.pv-pb li::before{content:"";flex:0 0 22px;height:22px;margin-top:2px;border-radius:50%;background:var(--q-gold);background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23fff' stroke-width='3.2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M6 12.5l4 4 8-9'/%3E%3C/svg%3E");background-size:70%;background-position:center;background-repeat:no-repeat}

/* savings teaser */
.pv-st{display:grid;grid-template-columns:1.1fr 1fr;gap:clamp(24px,4vw,60px);align-items:center;padding:clamp(34px,4vw,56px);border-radius:calc(var(--radius) + 10px);background:linear-gradient(135deg,var(--chrome-bg),color-mix(in srgb,var(--chrome-bg) 70%,var(--q-gold)));color:#fff;position:relative;overflow:hidden}
.pv-st::after{content:"";position:absolute;right:-90px;top:-90px;width:300px;height:300px;border-radius:50%;background:color-mix(in srgb,var(--q-gold) 55%,transparent);filter:blur(60px)}
.pv-st > *{position:relative;z-index:1}
.pv-st h2{color:#fff;margin:0}.pv-st p{color:rgba(255,255,255,.86);font-size:17px;line-height:1.6;margin:14px 0 0}
.pv-st label{display:block;font-size:14px;font-weight:600;margin-bottom:10px;color:#fff}
.pv-st .row{display:flex;align-items:center;gap:14px}.pv-st input[type=range]{flex:1;accent-color:var(--q-gold);min-height:44px}
.pv-st output{min-width:96px;text-align:right;font-weight:700;font-variant-numeric:tabular-nums}
.pv-st .res{margin-top:20px;padding:20px 22px;border-radius:var(--radius);background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.22)}
.pv-st .res .k{font-size:13px;letter-spacing:.1em;text-transform:uppercase;color:rgba(255,255,255,.8)}
.pv-st .res .v{font-family:var(--q-serif);font-size:clamp(34px,4.4vw,52px);line-height:1.05;margin-top:6px;font-variant-numeric:tabular-nums}
.pv-st .res .d{font-size:14px;color:rgba(255,255,255,.82);margin-top:6px}
.pv-st .q-btn{margin-top:18px}

/* overview */
.pv-ov-hero{padding:clamp(60px,8vw,120px) 0 clamp(36px,5vw,60px)}
.pv-ov-hero .q-h1{color:#fff;max-width:900px;margin:18px 0 0}.pv-ov-hero .q-h1 em{font-style:normal;color:var(--q-gold)}
.pv-ov-hero .q-lead{color:rgba(255,255,255,.88);max-width:680px;margin-top:22px}
.pv-ov-hero .badges{display:flex;gap:12px;flex-wrap:wrap;margin-top:30px}
.pv-ov-hero .badges span{border:1px solid rgba(255,255,255,.28);border-radius:999px;padding:9px 18px;font-size:14.5px;color:#fff;background:rgba(255,255,255,.07);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px)}
.pv-ov{padding:clamp(40px,5vw,72px) 0 clamp(60px,7vw,100px)}
.pv-ov-app{display:grid;grid-template-columns:260px 1fr;gap:28px;align-items:start}
.pv-ov-rail{list-style:none;margin:0;padding:0;display:grid;gap:6px;position:sticky;top:110px}
.pv-ov-rail button{all:unset;box-sizing:border-box;width:100%;min-height:52px;display:flex;align-items:center;gap:14px;padding:8px 14px;border-radius:14px;cursor:pointer;color:var(--fg-muted);font-size:15px;font-weight:600;border:1px solid transparent;transition:background .25s,color .25s,border-color .25s}
.pv-ov-rail button:hover{background:var(--bg-alt)}
.pv-ov-rail button:focus-visible{outline:3px solid var(--accent-ink);outline-offset:2px}
.pv-ov-rail .ic{width:36px;height:36px;border-radius:11px;display:grid;place-items:center;background:var(--bg-alt);border:1px solid var(--border);flex:0 0 auto;color:var(--fg)}
.pv-ov-rail .ic svg{width:19px;height:19px;stroke:currentColor;fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.pv-ov-rail li.on button{background:var(--card);border-color:var(--border);color:var(--fg);box-shadow:0 10px 28px rgba(0,5,69,.1)}
.pv-ov-rail li.on .ic{background:var(--q-gold);border-color:var(--q-gold);color:var(--cta-fg)}
.pv-ov-rail li.off button{text-decoration:line-through;text-decoration-thickness:1.5px}
.pv-ov-rail li.done .ic::after{content:"";position:absolute}
.pv-ov-rail .amt{margin-left:auto;font-size:13.5px;color:var(--accent-ink);font-variant-numeric:tabular-nums}
.pv-ov-app > *,.pv-ov-stage > *{min-width:0}
.pv-ov-stage{display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:24px;align-items:start}
.pv-ov-tw{overflow-x:auto;-webkit-overflow-scrolling:touch}
.pv-ov-tw:focus-visible{outline:3px solid var(--accent-ink);outline-offset:3px}
.pv-ov-panel{background:var(--card);border:1px solid var(--border);border-radius:calc(var(--radius) + 6px);padding:clamp(24px,3vw,40px);box-shadow:0 24px 60px rgba(0,5,69,.08);animation:pv-in .5s ease both}
.pv-ov-panel[hidden]{display:none}
.pv-ov-panel [tabindex='-1']:focus{outline:none}
.pv-ov-panel .k{font-size:13px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--accent-ink)}
.pv-ov-panel h2,.pv-ov-panel h3.t{font-family:var(--q-serif);font-size:clamp(26px,3vw,36px);line-height:1.12;margin:10px 0 10px;color:var(--fg)}
.pv-ov-panel .b{font-size:16.5px;line-height:1.65;color:var(--fg-muted);margin:0 0 24px;max-width:640px}
.pv-ov-tog{display:flex;align-items:center;gap:12px;padding:14px 16px;border-radius:14px;background:var(--bg-alt);border:1px solid var(--border);margin-bottom:22px;font-size:15.5px;font-weight:600;color:var(--fg);cursor:pointer;min-height:52px}
.pv-ov-tog input{width:24px;height:24px;accent-color:var(--q-gold);flex:0 0 auto}
.pv-ov-fields{display:grid;gap:22px}
.pv-ov-fields.dim{opacity:.38;pointer-events:none}
.pv-ov-f label{display:flex;justify-content:space-between;gap:12px;font-size:15px;font-weight:600;color:var(--fg);margin-bottom:8px}
.pv-ov-f output{font-variant-numeric:tabular-nums;color:var(--accent-ink);font-weight:700}
.pv-ov-f input[type=range]{width:100%;accent-color:var(--q-gold);min-height:44px;margin:0}
.pv-ov-f .hint{font-size:13.5px;color:var(--fg-muted);margin-top:2px}
.pv-ov-f select,.pv-ov-f input[type=text],.pv-ov-f input[type=email],.pv-ov-f input[type=tel]{width:100%;min-height:48px;font-size:16px;padding:0 14px;border:1px solid var(--border);border-radius:12px;background:var(--bg);color:var(--fg);font-family:inherit}
.pv-ov-read{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:26px}
.pv-ov-read > div{border:1px solid var(--border);border-radius:14px;padding:14px 16px;background:var(--bg-alt)}
.pv-ov-read .kk{font-size:13px;color:var(--fg-muted)}.pv-ov-read .vv{font-family:var(--q-serif);font-size:24px;color:var(--fg);margin-top:4px;font-variant-numeric:tabular-nums}
.pv-ov-read .vv.g{color:var(--accent-ink)}
.pv-ov-nav{display:flex;justify-content:space-between;gap:12px;margin-top:28px;flex-wrap:wrap}
.pv-ov-nav button{min-height:48px;padding:0 26px;border-radius:999px;font:inherit;font-weight:700;font-size:15.5px;cursor:pointer;border:1px solid var(--border);background:var(--card);color:var(--fg)}
.pv-ov-nav button.go{background:var(--q-gold);border-color:var(--q-gold);color:var(--cta-fg)}
.pv-ov-nav button:focus-visible{outline:3px solid var(--accent-ink);outline-offset:3px}
.pv-ov-live{position:sticky;top:110px;border-radius:calc(var(--radius) + 6px);background:var(--chrome-bg);color:#fff;padding:26px;overflow:hidden;isolation:isolate}
.pv-ov-live::before{content:"";position:absolute;right:-70px;top:-70px;width:220px;height:220px;border-radius:50%;background:color-mix(in srgb,var(--q-gold) 60%,transparent);filter:blur(50px);z-index:-1}
.pv-ov-live .k{font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:rgba(255,255,255,.8)}
.pv-ov-live .v{font-family:var(--q-serif);font-size:44px;line-height:1.05;margin-top:8px;font-variant-numeric:tabular-nums}
.pv-ov-live .r{font-size:14px;color:rgba(255,255,255,.82);margin-top:6px}
.pv-ov-gauge{position:relative;width:170px;height:170px;margin:20px auto 6px}
.pv-ov-gauge svg{width:100%;height:100%;transform:rotate(-90deg)}
.pv-ov-gauge circle{fill:none;stroke-width:14;stroke-linecap:round}
.pv-ov-gauge .bg{stroke:rgba(255,255,255,.14)}.pv-ov-gauge .fg{stroke:var(--q-gold);transition:stroke-dashoffset .9s cubic-bezier(.2,.7,.2,1)}
.pv-ov-gauge .tick{stroke:#fff;stroke-width:3;stroke-linecap:butt}
.pv-ov-gauge .c{position:absolute;inset:0;display:grid;place-content:center;text-align:center}
.pv-ov-gauge .c b{font-family:var(--q-serif);font-size:38px;line-height:1;font-variant-numeric:tabular-nums}.pv-ov-gauge .c span{font-size:13px;color:rgba(255,255,255,.8);margin-top:4px}
.pv-ov-live .lines{list-style:none;padding:0;margin:14px 0 0;display:grid;gap:10px}
.pv-ov-live .lines li{display:grid;grid-template-columns:1fr auto;gap:4px 10px;font-size:13.5px;color:rgba(255,255,255,.86)}
.pv-ov-live .lines .bar{grid-column:1/-1;height:6px;border-radius:6px;background:rgba(255,255,255,.14);overflow:hidden}
.pv-ov-live .lines .bar i{display:block;height:100%;width:0;border-radius:6px;background:var(--q-gold);transition:width .8s cubic-bezier(.2,.7,.2,1)}
.pv-ov-live .mark{margin-top:16px;padding:12px 14px;border-radius:12px;font-size:14px;line-height:1.45;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2)}
.pv-ov-live .mark.ok{background:rgba(40,200,120,.18);border-color:rgba(120,240,170,.5)}
.pv-ov-res .big{font-family:var(--q-serif);font-size:clamp(46px,7vw,92px);line-height:1;color:var(--fg);font-variant-numeric:tabular-nums;letter-spacing:-.02em}
.pv-ov-res .big small{font-size:.4em;color:var(--fg-muted);letter-spacing:0}
.pv-ov-res .rng{font-size:16px;color:var(--fg-muted);margin-top:8px}
.pv-ov-table{width:100%;border-collapse:collapse;margin-top:26px;font-size:15px}
.pv-ov-table th,.pv-ov-table td{padding:12px 10px;border-bottom:1px solid var(--border);text-align:left;vertical-align:middle}
.pv-ov-table th{font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:var(--fg-muted)}
.pv-ov-table td.n{font-variant-numeric:tabular-nums;white-space:nowrap}.pv-ov-table td.g{color:var(--accent-ink);font-weight:700}
.pv-ov-table .meter{height:8px;border-radius:8px;background:var(--bg-alt);overflow:hidden;min-width:90px}.pv-ov-table .meter i{display:block;height:100%;border-radius:8px;background:var(--q-gold);width:0;transition:width 1s cubic-bezier(.2,.7,.2,1)}
.pv-ov-asm{margin-top:22px;border:1px solid var(--border);border-radius:14px;padding:4px 18px;background:var(--bg-alt)}
.pv-ov-asm summary{cursor:pointer;min-height:48px;display:flex;align-items:center;font-weight:600;font-size:15px;color:var(--fg)}
.pv-ov-asm ul{margin:4px 0 14px;padding-left:20px;font-size:14.5px;line-height:1.7;color:var(--fg-muted)}
.pv-ov-cta{margin-top:30px;display:grid;grid-template-columns:1fr 1fr;gap:14px 18px}
.pv-ov-cta h3{grid-column:1/-1;font-family:var(--q-serif);font-size:26px;margin:0;color:var(--fg)}.pv-ov-cta p.n{grid-column:1/-1;margin:-4px 0 6px;font-size:15.5px;line-height:1.6;color:var(--fg-muted)}
.pv-ov-cta .full{grid-column:1/-1}
.pv-ov-cta .q-btn{border:0;cursor:pointer;min-height:52px;font:inherit;font-weight:700}
.pv-ov-thanks{display:none;grid-column:1/-1;padding:18px 20px;border-radius:14px;background:color-mix(in srgb,var(--q-gold) 18%,var(--card));border:1px solid var(--q-gold);font-size:16px;line-height:1.55;color:var(--fg)}
.pv-ov-fine{margin-top:18px;font-size:13.5px;line-height:1.6;color:var(--fg-muted)}

@media(max-width:1100px){.pv-ov-stage{grid-template-columns:minmax(0,1fr)}.pv-ov-live{position:relative;top:auto}}
@media(max-width:1024px){.pv-p3d-grid{grid-template-columns:1fr}.pv-p3d-stage{max-height:520px;margin:0 auto}.pv-pb{grid-template-columns:1fr}.pv-pb-img{order:0}.pv-st{grid-template-columns:1fr}.pv-ov-app{grid-template-columns:minmax(0,1fr)}.pv-ov-rail{position:static;max-width:100%;grid-auto-flow:column;grid-auto-columns:minmax(150px,1fr);overflow-x:auto;padding-bottom:6px;scroll-snap-type:x proximity}.pv-ov-rail li{scroll-snap-align:start}.pv-ov-rail .amt{display:none}}
@media(max-width:767px){.pv-p3d-facts{grid-template-columns:1fr}.pv-p3d-tag{display:none}.pv-cnt-grid{grid-template-columns:1fr 1fr}.pv-cnt-grid > div + div::before{display:none}.pv-pf-rail{grid-template-columns:1fr;gap:18px}.pv-pf-rail::before,.pv-pf-rail::after{display:none}.pv-pf-rail li{display:grid;grid-template-columns:64px 1fr;gap:4px 16px;text-align:left;align-items:center}.pv-pf-rail button{display:contents}.pv-pf-ico{width:60px;height:60px;margin:0;grid-row:1/3}.pv-pf-rail h3{margin:0;align-self:end}.pv-pf-rail p{align-self:start}.pv-ita-cap{grid-template-columns:1fr}.pv-ita-bubble{width:34%}.pv-ov-read{grid-template-columns:1fr}.pv-ov-cta{grid-template-columns:1fr}.pv-ita-label{font-size:13px;padding:7px 12px}}
@media(prefers-reduced-motion:reduce){.pv-grid-bg,.pv-orb,.pv-p3d-ring,.pv-p3d-tag,.pv-p3d-tag i,.pv-p3d-stage > img.fb,.pv-steam i,.pv-pf-rail::after,.pv-tick-track{animation:none!important}.pv-tick-track{flex-wrap:wrap;width:auto}.pv-tick ul[aria-hidden]{display:none}.pv-ita-frame{transition:none}.pv-ita-bubble,.pv-ita-dot{transition:none}.pv-ov-live .lines .bar i,.pv-ov-gauge .fg,.pv-ov-table .meter i{transition:none}}
'''

ICONS = {
    "printer": '<path d="M7 9V3h10v6"/><rect x="3" y="9" width="18" height="9" rx="2"/><path d="M7 14h10v7H7z"/>',
    "docs": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h4"/>',
    "press": '<rect x="3" y="8" width="18" height="10" rx="2"/><path d="M6 8V4h12v4M7 18v3M17 18v3M8 13h8"/>',
    "it": '<rect x="3" y="4" width="18" height="6" rx="1.5"/><rect x="3" y="14" width="18" height="6" rx="1.5"/><path d="M7 7h.01M7 17h.01M11 7h6M11 17h6"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
    "cup": '<path d="M5 8h11v6a5 5 0 0 1-5 5h-1a5 5 0 0 1-5-5z"/><path d="M16 10h2a2.5 2.5 0 0 1 0 5h-2M8 3v2M12 3v2"/>',
    "profile": '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-7 8-7s8 2.6 8 7"/>',
    "chart": '<path d="M4 20V4M4 20h16"/><path d="M8 16l4-5 3 3 5-7"/>',
    "device": '<rect x="5" y="3" width="14" height="18" rx="3"/><path d="M9 7h6M9 11h6M9 15h3"/>',
    "meter": '<path d="M4 18a8 8 0 1 1 16 0"/><path d="M12 18l4-6"/>',
    "dash": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 15l3-4 3 2 4-5"/>',
    "truck": '<path d="M3 6h11v10H3zM14 9h4l3 3v4h-7"/><circle cx="7" cy="18" r="2"/><circle cx="17" cy="18" r="2"/>',
    "smile": '<circle cx="12" cy="12" r="9"/><path d="M8 14c1 1.6 2.4 2.4 4 2.4s3-.8 4-2.4M9 9.5h.01M15 9.5h.01"/>',
}


def _svg(name: str) -> str:
    return f'<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">{ICONS[name]}</svg>'


# ------------------------------------------------------------------------------ product3d

def _product3d(s, ctx):
    E, RAW, L = ctx["E"], ctx["RAW"], ctx["L"]
    rel = ctx["rel"]
    btns = ""
    if s.get("primary"):
        btns += f'<a class="q-btn" href="{E(L(s["primary"]["href"]))}">{E(s["primary"]["label"])}</a>'
    if s.get("secondary"):
        btns += f'<a class="q-btn-ghost" href="{E(L(s["secondary"]["href"]))}">{E(s["secondary"]["label"])}<span style="width:22px;height:1px;background:currentColor;display:inline-block"></span></a>'
    facts = "".join(f"<li><b>{E(v)}</b><span>{E(l)}</span></li>" for v, l in s.get("facts", []))
    tags = "".join(
        f'<span class="pv-p3d-tag" style="left:{x}%;top:{y}%"><i></i><b>{E(lab)}</b><em>{E(val)}</em></span>'
        for lab, val, x, y in s.get("tags", []))
    poster = rel(s["poster"])
    if s.get("model"):
        orbit = s.get("orbit", "28deg 74deg 105%")
        stage = (f'<model-viewer src="{E(rel(s["model"]))}" poster="{E(poster)}" alt="{E(s.get("alt", "A 3D model you can turn"))}" camera-controls disable-zoom auto-rotate rotation-per-second="16deg" '
                 f'shadow-intensity="0" exposure="1.1" interaction-prompt="none" camera-orbit="{E(orbit)}" loading="eager" reveal="auto"></model-viewer>'
                 f'<img class="fb" src="{E(poster)}" alt="" width="1200" height="1200">'
                 f'<script type="module" src="{MV_SRC}"></script>')
    elif s.get("video"):
        webm = f'<source src="{E(rel(s["video_webm"]))}" type="video/webm">' if s.get("video_webm") else ""
        stage = (f'<video class="fb" autoplay muted loop playsinline preload="auto" poster="{E(poster)}" aria-label="{E(s.get("alt_text", ""))}" width="1280" height="720">{webm}<source src="{E(rel(s["video"]))}" type="video/mp4"></video>')
    else:
        stage = f'<img class="fb" src="{E(poster)}" alt="{E(s.get("alt_text", ""))}" width="1200" height="900">'
    photo = (" photo" + (" vid" if s.get("video") else "")) if not s.get("model") and s.get("photo") else ""
    cut = s.get("cutout")
    if cut:
        steam = "".join(f'<i style="--x:{x};--d:{d}s;--dx:{dx}px"></i>' for x, d, dx in ((8, 0, -14), (34, 1.1, 10), (58, 2.2, -8)))
        cutter = (f'<div class="pv-cx{" tall" if cut.get("h", 592) > cut.get("w", 720) * 1.1 else ""}" aria-hidden="true" style="--cw:{cut.get("w", 720)};--ch:{cut.get("h", 592)}">{("<video muted playsinline preload=auto width=" + str(cut.get("w", 720)) + " height=" + str(cut.get("h", 592)) + "><source src=" + chr(34) + E(rel(cut["webm"])) + chr(34) + " type=video/webm></video>") if cut.get("webm") else ""}'
                  f'<img class="still{" static" if not cut.get("webm") else ""}" alt="" src="{E(rel(cut["still"]))}" width="{cut.get("w", 720)}" height="{cut.get("h", 592)}">'
                  f'<div class="steam" style="left:{cut.get("steam_x", 12)}%;top:{cut.get("steam_y", 20)}%">{steam}</div></div>')
        sid = f' id="{E(s["id"])}"' if s.get("id") else ""
        if cut.get("tumble"):
            import json as _j
            cutter += '<div class="pv-ice" aria-hidden="true" data-ice=' + chr(39) + _j.dumps([rel(x) for x in cut["tumble"]]) + chr(39) + '></div>'
        return (f'<section class="q-section pv-dark pv-p3d pv-hascut"{sid}><div class="pv-grid-bg" aria-hidden="true"></div><div class="pv-orb a" aria-hidden="true"></div><div class="pv-orb b" aria-hidden="true"></div>'
                f'<div class="q-container pv-p3d-grid"><div><div class="q-eyebrow">{E(s.get("eyebrow", ""))}</div>'
                f'<h1 class="q-h1">{RAW(s["heading"])}</h1><p class="q-lead">{E(s.get("subhead", ""))}</p>'
                f'<div class="pv-p3d-btns">{btns}</div>{f"<ul class=pv-p3d-facts>{facts}</ul>" if facts else ""}</div></div>{cutter}'
                '<script>(function(){var h=document.querySelector(".pv-hascut");if(!h)return;var v=h.querySelector(".pv-cx video"),rm=matchMedia("(prefers-reduced-motion: reduce)").matches;if(rm)return;'
                'var ice=function(){var c=h.querySelector(".pv-ice");if(!c||!c.animate)return;var src=JSON.parse(c.getAttribute("data-ice")),W=c.clientWidth,H=c.clientHeight,N=W<700?9:15;for(var i=0;i<N;i++){(function(i){var im=new Image();im.src=src[i%src.length];im.alt="";var settle=i<5,sz=settle?60+Math.random()*40:90+Math.random()*90,sx=W*(.62+Math.random()*.2),sy=H*(.32+Math.random()*.14),ex=settle?W*(.55+Math.random()*.4):W*(Math.random()*1.0),ey=settle?H*(.78+Math.random()*.14):H*(.15+Math.random()*.9),rz=(Math.random()-.5)*720,rx=360+Math.random()*360,ry=360+Math.random()*360;im.style.cssText="position:absolute;left:0;top:0;width:"+sz+"px;height:auto;opacity:0;will-change:transform,opacity;filter:drop-shadow(0 20px 24px rgba(0,0,0,.45))";c.appendChild(im);var es=settle?.7+Math.random()*.5:1.6+Math.random()*1.6;var a=im.animate([{transform:"translate("+sx+"px,"+sy+"px) translateZ(-500px) rotateX(0) rotateY(0) rotateZ(0) scale(.2)",opacity:0,offset:0},{opacity:1,offset:.14},{transform:"translate("+ex+"px,"+ey+"px) translateZ("+(settle?0:260)+"px) rotateX("+rx+"deg) rotateY("+ry+"deg) rotateZ("+rz+"deg) scale("+es+")",opacity:settle?1:.0,offset:1}],{duration:1700+Math.random()*900,delay:350+i*110,easing:"cubic-bezier(.2,.7,.25,1)",fill:"forwards"})})(i)}};'
                'var go=function(){h.classList.add("in");ice();if(v){var p=v.play();if(p&&p.catch)p.catch(function(){})}};if(v)v.addEventListener("ended",function(){try{v.currentTime=Math.max(0,v.duration-.05)}catch(e){}});'
                'if("IntersectionObserver" in window){new IntersectionObserver(function(es,o){if(es[0].isIntersecting){go();o.disconnect()}},{threshold:.25}).observe(h)}else go()})();</script></section>')
    return (f'<section class="q-section pv-dark pv-p3d"{f" id={chr(34)}{E(s[chr(105)+chr(100)])}{chr(34)}" if s.get("id") else ""}>'
            f'<div class="pv-grid-bg" aria-hidden="true"></div><div class="pv-orb a" aria-hidden="true"></div><div class="pv-orb b" aria-hidden="true"></div>'
            f'<div class="q-container pv-p3d-grid"><div><div class="q-eyebrow">{E(s.get("eyebrow", ""))}</div>'
            f'<h1 class="q-h1">{RAW(s["heading"])}</h1><p class="q-lead">{E(s.get("subhead", ""))}</p>'
            f'<div class="pv-p3d-btns">{btns}</div>{f"<ul class=pv-p3d-facts>{facts}</ul>" if facts else ""}</div>'
            f'<div class="pv-p3d-stage{photo}"><div class="pv-p3d-ring" aria-hidden="true"></div>{stage}{tags}<div class="pv-p3d-hint">{E(s.get("hint", "Drag to turn"))}</div></div></div></section>')


# ------------------------------------------------------------------------------ countband

def _countband(s, ctx):
    E = ctx["E"]
    cells = ""
    for it in s["items"]:
        val, label = it[0], it[1]
        suffix = it[2] if len(it) > 2 else ""
        dec = 1 if "." in str(val) else 0
        cells += (f'<div><b data-count="{E(str(val).replace(",", ""))}" data-dec="{dec}" data-suffix="{E(suffix)}">{E(val)}{f"<small>{E(suffix)}</small>" if suffix else ""}</b><span>{E(label)}</span></div>')
    head = f'<div class="pv-center" style="margin-bottom:36px"><div class="q-eyebrow">{E(s["eyebrow"])}</div></div>' if s.get("eyebrow") else ""
    return (f'<section class="q-section pv-dark pv-cnt"><div class="pv-grid-bg" aria-hidden="true"></div><div class="q-container">{head}'
            f'<div class="pv-cnt-grid" style="--n:{len(s["items"])}">{cells}</div></div></section>')


# ------------------------------------------------------------------------------ ticker

def _ticker(s, ctx):
    E = ctx["E"]
    lis = "".join(f"<li>{E(t)}</li>" for t in s["items"])
    return (f'<div class="pv-tick" role="region" aria-label="{E(s.get("label", "What every Kelly agreement includes"))}"><div class="pv-tick-track">'
            f'<ul>{lis}</ul><ul aria-hidden="true">{lis}</ul></div></div>')


# ------------------------------------------------------------------------------ pulseflow

def _pulseflow(s, ctx):
    E, RAW = ctx["E"], ctx["RAW"]
    nodes = s["nodes"]  # [icon, title, text]
    lis = "".join(
        f'<li class="{"on" if i == 0 else ""}"><button type="button" data-i="{i}"><span class="pv-pf-ico">{_svg(n[0])}</span><h3>{E(n[1])}</h3><p>{E(n[2])}</p></button></li>'
        for i, n in enumerate(nodes))
    feed = json.dumps(s["feed"], ensure_ascii=False)
    sid = s.get("id", "pf")
    js = ("<script>(function(){var r=document.getElementById('" + sid + "');if(!r)return;var rail=r.querySelector('.pv-pf-rail'),lis=r.querySelectorAll('.pv-pf-rail li'),log=r.querySelector('.pv-pf-log');"
          "var feed=" + feed + ",n=0,idx=0,t,rm=matchMedia('(prefers-reduced-motion: reduce)').matches;"
          "function w(){rail.style.setProperty('--w',(rail.getBoundingClientRect().width*.8)+'px')}w();addEventListener('resize',w);"
          "function on(i){lis.forEach(function(l,k){l.classList.toggle('on',k===i)})}"
          "function add(){var f=feed[n%feed.length];var li=document.createElement('li');var d=new Date();var hh=String(8+((n*7)%9)).padStart(2,'0'),mm=String((n*13)%60).padStart(2,'0');"
          "li.innerHTML='<time>'+hh+':'+mm+'</time><span>'+f[1]+'</span>';log.appendChild(li);while(log.children.length>6)log.removeChild(log.firstChild);on(f[0]);n++}"
          "function start(){if(t)return;add();t=setInterval(add,rm?4200:2300)}"
          "if('IntersectionObserver' in window){new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting)start();else{clearInterval(t);t=0}})},{threshold:.25}).observe(r)}else{start()}"
          "lis.forEach(function(l,k){l.querySelector('button').addEventListener('click',function(){on(k)})});"
          "})();</script>")
    return (f'<section class="q-section pv-dark pv-pf" id="{E(sid)}"><div class="pv-grid-bg" aria-hidden="true"></div><div class="pv-orb b" aria-hidden="true"></div><div class="q-container">'
            f'<div class="pv-pf-head"><div class="q-eyebrow">{E(s.get("eyebrow", ""))}</div><h2 class="q-h2" style="margin-top:18px">{E(s["heading"])}</h2><p>{E(s.get("intro", ""))}</p></div>'
            f'<ol class="pv-pf-rail">{lis}</ol>'
            f'<div class="pv-pf-feed"><div class="pv-pf-bar"><i></i><i></i><i></i><span>Kelly monitoring, example feed</span></div><ul class="pv-pf-log" aria-live="off"></ul></div>'
            f'<p class="pv-pf-note">{E(s.get("note", "Illustrative. A real feed shows your devices, your meters and your supply orders."))}</p></div>{js}</section>')


# ------------------------------------------------------------------------------ itdirector

def _itdirector(s, ctx):
    E, rel = ctx["E"], ctx["rel"]
    sid = s.get("id", "ita")
    logo = rel(s.get("logo", "assets/kelly-logo.png"))
    bubble = (f'<span class="pv-ita-dot d2"></span><span class="pv-ita-dot d1"></span><div class="pv-ita-bubble" role="img" aria-label="Thinking: Kelly Office Solutions"><img src="{E(logo)}" alt="" width="300" height="109"></div>') if s.get("bubble", True) else ""
    chips = "".join(f'<ul class="pv-ita-chips {side}">' + "".join(f"<li>{E(c)}</li>" for c in s[key]) + "</ul>" for side, key in (("b", "before_chips"), ("a", "after_chips")) if s.get(key))
    js = ("<script>(function(){var r=document.getElementById('" + sid + "');if(!r)return;var f=r.querySelector('.pv-ita-frame'),rg=r.querySelector('.pv-ita-range'),bs=r.querySelectorAll('.pv-ita-ctl button'),rm=matchMedia('(prefers-reduced-motion: reduce)').matches;"
          "function set(p,smooth){if(!smooth){f.style.transition='none'}f.style.setProperty('--p',p);rg.value=p;f.classList.toggle('relieved',p<=34);bs[0].setAttribute('aria-pressed',p>66);bs[1].setAttribute('aria-pressed',p<=34);if(!smooth){void f.offsetWidth;f.style.transition=''}}"
          "rg.addEventListener('input',function(){set(+rg.value,false)});"
          "bs[0].addEventListener('click',function(){set(100,true)});bs[1].addEventListener('click',function(){set(0,true)});"
          "set(100,false);var done=0;if('IntersectionObserver' in window&&!rm){new IntersectionObserver(function(es,o){es.forEach(function(e){if(e.isIntersecting&&!done){done=1;setTimeout(function(){set(0,true)},1100);o.disconnect()}})},{threshold:.55}).observe(f)}"
          "})();</script>")
    return (f'{ctx["sec_open"](s)} <div class="q-container"><div class="pv-center" style="margin-bottom:40px"><div class="q-eyebrow">{E(s.get("eyebrow", ""))}</div>'
            f'<h2 class="q-h2" style="margin-top:22px;max-width:780px">{E(s["heading"])}</h2><p class="q-lead" style="max-width:640px;margin:16px auto 0">{E(s.get("intro", ""))}</p></div>'
            f'<div class="pv-ita" id="{E(sid)}"><div class="pv-ita-frame"><img class="im after" src="{E(rel(s["after"]))}" alt="{E(s.get("after_alt", "The same IT director, relaxed, with calm dashboards behind them"))}" width="1600" height="900" loading="lazy">'
            f'<img class="im before" src="{E(rel(s["before"]))}" alt="{E(s.get("before_alt", "An IT director with their head in their hands, surrounded by red alerts"))}" width="1600" height="900" loading="lazy">'
            f'<span class="pv-ita-label b">{E(s.get("before_label", "Before"))}</span><span class="pv-ita-label a">{E(s.get("after_label", "With Kelly"))}</span>'
            f'{bubble}{chips}'
            f'<div class="pv-ita-split" aria-hidden="true"></div><input class="pv-ita-range" type="range" min="0" max="100" value="100" aria-label="Drag to compare before and after"></div>'
            f'<div class="pv-ita-ctl"><button type="button" aria-pressed="true">{E(s.get("before_btn", "Before"))}</button><button type="button" aria-pressed="false">{E(s.get("after_btn", "After"))}</button></div>'
            f'<div class="pv-ita-cap"><div><h3>{E(s["before_title"])}</h3><p>{E(s["before_body"])}</p></div><div><h3>{E(s["after_title"])}</h3><p>{E(s["after_body"])}</p></div></div>'
            f'<p class="pv-ita-note">{E(s.get("note", "Generated images for the preview. Your own customers and technicians replace them once photography exists."))}</p></div></div>{js}</section>')


# ------------------------------------------------------------------------------ photoband

def _photoband(s, ctx):
    E, rel, L = ctx["E"], ctx["rel"], ctx["L"]
    if s.get("video"):
        webm = f'<source src="{E(rel(s["video_webm"]))}" type="video/webm">' if s.get("video_webm") else ""
        media = f'<video autoplay muted loop playsinline preload="metadata" poster="{E(rel(s["image"]))}" aria-label="{E(s.get("alt_text", ""))}" width="1280" height="720">{webm}<source src="{E(rel(s["video"]))}" type="video/mp4"></video>'
    else:
        media = f'<img src="{E(rel(s["image"]))}" alt="{E(s.get("alt_text", ""))}" width="1600" height="900" loading="lazy">'
    steam = "".join(f'<span class="pv-steam" style="left:{x}%;top:{y}%"><i></i><i></i><i></i></span>' for x, y in s.get("steam", []))
    lis = "".join(f"<li>{E(t)}</li>" for t in s.get("points", []))
    cta = f'<p style="margin-top:28px"><a class="q-btn" href="{E(L(s["cta"]["href"]))}">{E(s["cta"]["label"])}</a></p>' if s.get("cta") else ""
    return (f'{ctx["sec_open"](s)} <div class="q-container pv-pb"><div><div class="q-eyebrow">{E(s.get("eyebrow", ""))}</div><h2 class="q-h2" style="margin-top:20px">{E(s["heading"])}</h2>'
            f'<p class="q-lead" style="margin-top:16px;max-width:520px">{E(s.get("intro", ""))}</p><ul>{lis}</ul>{cta}</div>'
            f'<div class="pv-pb-img">{media}{"" if s.get("video") else steam}</div></div></section>')


# ------------------------------------------------------------------------------ savings teaser

def _savingstease(s, ctx):
    E, L = ctx["E"], ctx["L"]
    sid = s.get("id", "st")
    rate = s.get("rate", 0.12)
    js = ("<script>(function(){var r=document.getElementById('" + sid + "');if(!r)return;var i=r.querySelector('input'),o=r.querySelector('output'),v=r.querySelector('[data-v]');"
          "var f=function(n){return '$'+Math.round(n).toLocaleString('en-US')};"
          "function u(){var m=+i.value;o.textContent=f(m)+' a month';v.textContent=f(m*12*" + str(rate) + ")+' a year'}i.addEventListener('input',u);u()})();</script>")
    return (f'<section class="q-section"><div class="q-container"><div class="pv-st" id="{E(sid)}"><div><div class="q-eyebrow" style="color:#fff">{E(s.get("eyebrow", "Full Office Overview"))}</div>'
            f'<h2 class="q-h2" style="margin-top:18px">{E(s["heading"])}</h2><p>{E(s["body"])}</p></div>'
            f'<div><label for="{E(sid)}-r">{E(s.get("label", "Roughly what does your office spend a month on print, IT, mail and the break room?"))}</label>'
            f'<div class="row"><input id="{E(sid)}-r" type="range" min="2000" max="80000" step="500" value="18000"><output>$18,000 a month</output></div>'
            f'<div class="res"><div class="k">A typical result</div><div class="v" data-v>$0 a year</div><div class="d">{E(s.get("fine", "A rough orientation at 12 percent. The Overview uses your real inputs and shows a range."))}</div></div>'
            f'<a class="q-btn" href="{E(L(s["href"]))}">{E(s.get("cta", "Run my Full Office Overview"))}</a></div></div></div>{js}</section>')


# ------------------------------------------------------------------------------ overview

OV_LINES = [
    {"id": "print", "icon": "printer", "name": "Copiers and managed print", "short": "Print",
     "blurb": "Every device, every page, and the staff time nobody counts. Managed print puts toner, service and meter reads under one agreement.",
     "fields": [
         {"k": "devices", "label": "Printers and copiers", "min": 1, "max": 80, "step": 1, "def": 8, "fmt": "n"},
         {"k": "mono", "label": "Mono pages a month", "min": 0, "max": 200000, "step": 500, "def": 25000, "fmt": "n"},
         {"k": "color", "label": "Color pages a month", "min": 0, "max": 60000, "step": 250, "def": 6000, "fmt": "n"}]},
    {"id": "docs", "icon": "docs", "name": "Document management", "short": "Documents",
     "blurb": "Hours spent filing, searching, re-keying and walking paper between desks. Scan to DocuWare turns it into indexed workflows.",
     "fields": [{"k": "hours", "label": "Staff hours a week on paper handling", "min": 0, "max": 120, "step": 1, "def": 12, "fmt": "n", "hint": "Filing, finding, re-keying, scanning, routing approvals."}]},
    {"id": "press", "icon": "press", "name": "Production print", "short": "Production",
     "blurb": "Booklets, forms, plans and mailings sent to an outside print shop. In-house production print with inline finishing brings them home.",
     "fields": [{"k": "spend", "label": "Spent outside on printing, a month", "min": 0, "max": 25000, "step": 100, "def": 1500, "fmt": "$"}]},
    {"id": "it", "icon": "it", "name": "IT services", "short": "IT",
     "blurb": "KellyWay managed IT: monitoring, backup, security and Microsoft 365 for a fixed monthly invoice, from the team that already services your copiers.",
     "fields": [
         {"k": "users", "label": "People who use a computer", "min": 1, "max": 300, "step": 1, "def": 40, "fmt": "n"},
         {"k": "spend", "label": "IT spend a month, all vendors", "min": 0, "max": 60000, "step": 250, "def": 5000, "fmt": "$", "hint": "Support, licences, backup, hardware refresh, break-fix."}]},
    {"id": "mail", "icon": "mail", "name": "Mailing", "short": "Mailing",
     "blurb": "FP postage meters at commercial rates, folder inserters and mailroom printers that cost less per piece than the office copier.",
     "fields": [
         {"k": "postage", "label": "Postage a month", "min": 0, "max": 15000, "step": 50, "def": 1200, "fmt": "$"},
         {"k": "hours", "label": "Staff hours a week in the mailroom", "min": 0, "max": 40, "step": 1, "def": 4, "fmt": "n"}]},
    {"id": "cup", "icon": "cup", "name": "Water, ice and coffee", "short": "Break room",
     "blurb": "Bottleless water, ice and coffee serviced on the same visit as the copier. One fewer delivery company, one fewer invoice.",
     "fields": [{"k": "spend", "label": "Spent on water, ice and coffee, a month", "min": 0, "max": 6000, "step": 25, "def": 360, "fmt": "$"}]},
]

OV_RATES = {
    "labor_rate": 28, "vendor_admin_hours_month": 3,
    "print": {"mono_cpp": 0.018, "color_cpp": 0.09, "min_per_device_week": 25, "low": 0.12, "mid": 0.18, "high": 0.28},
    "docs": {"low": 0.20, "mid": 0.30, "high": 0.45},
    "press": {"low": 0.10, "mid": 0.15, "high": 0.28},
    "it": {"low": 0.05, "mid": 0.10, "high": 0.18},
    "mail": {"postage_low": 0.04, "postage_mid": 0.07, "postage_high": 0.11, "labor_low": 0.18, "labor_mid": 0.30, "labor_high": 0.45},
    "cup": {"low": 0.06, "mid": 0.10, "high": 0.18},
    "consolidation_factor": {"low": 0.5, "mid": 0.8, "high": 1.2},
    "goal": 0.10,
}


def _field_html(lid, f):
    fid = f"ov-{lid}-{f['k']}"
    hint = f'<div class="hint">{f["hint"]}</div>' if f.get("hint") else ""
    return (f'<div class="pv-ov-f"><label for="{fid}"><span>{f["label"]}</span><output for="{fid}" data-out="{lid}.{f["k"]}" data-fmt="{f.get("fmt", "n")}"></output></label>'
            f'<input id="{fid}" type="range" data-line="{lid}" data-k="{f["k"]}" min="{f["min"]}" max="{f["max"]}" step="{f["step"]}" value="{f["def"]}">{hint}</div>')


OV_JS = r"""
(function(){
var root=document.getElementById('__ID__');if(!root)return;
var CFG=__CFG__,R=CFG.rates,LINES=CFG.lines;
var rm=matchMedia('(prefers-reduced-motion: reduce)').matches;
var st={step:0,inc:{},v:{}};
LINES.forEach(function(l){st.inc[l.id]=true;st.v[l.id]={};l.fields.forEach(function(f){st.v[l.id][f.k]=f.def})});
var panels=[].slice.call(root.querySelectorAll('.pv-ov-panel')),railLi=[].slice.call(root.querySelectorAll('.pv-ov-rail li'));
var money=function(n){return '$'+Math.round(n).toLocaleString('en-US')};
var num=function(n){return Math.round(n).toLocaleString('en-US')};
function fmt(v,t){return t==='$'?money(v):num(v)}
function calc(id){var v=st.v[id],lab=R.labor_rate,cur=0,lo=0,mi=0,hi=0;
 if(id==='print'){var p=R.print,pages=(v.mono*p.mono_cpp+v.color*p.color_cpp)*12,labor=v.devices*p.min_per_device_week/60*52*lab;cur=pages+labor;lo=cur*p.low;mi=cur*p.mid;hi=cur*p.high}
 else if(id==='docs'){cur=v.hours*52*lab;lo=cur*R.docs.low;mi=cur*R.docs.mid;hi=cur*R.docs.high}
 else if(id==='press'){cur=v.spend*12;lo=cur*R.press.low;mi=cur*R.press.mid;hi=cur*R.press.high}
 else if(id==='it'){cur=v.spend*12;lo=cur*R.it.low;mi=cur*R.it.mid;hi=cur*R.it.high}
 else if(id==='mail'){var po=v.postage*12,la=v.hours*52*lab,m=R.mail;cur=po+la;lo=po*m.postage_low+la*m.labor_low;mi=po*m.postage_mid+la*m.labor_mid;hi=po*m.postage_high+la*m.labor_high}
 else if(id==='cup'){cur=v.spend*12;lo=cur*R.cup.low;mi=cur*R.cup.mid;hi=cur*R.cup.high}
 return {cur:cur,lo:lo,mi:mi,hi:hi}}
function total(){var cur=0,lo=0,mi=0,hi=0,n=0,per={};
 LINES.forEach(function(l){if(!st.inc[l.id]){per[l.id]=null;return}var c=calc(l.id);per[l.id]=c;cur+=c.cur;lo+=c.lo;mi+=c.mi;hi+=c.hi;n++});
 var vend=Math.max(0,n-1),per1=R.vendor_admin_hours_month*12*R.labor_rate,cf=R.consolidation_factor;
 var cons={cur:0,lo:vend*per1*cf.low,mi:vend*per1*cf.mid,hi:vend*per1*cf.high,vend:vend};
 lo+=cons.lo;mi+=cons.mi;hi+=cons.hi;
 return {cur:cur,lo:lo,mi:mi,hi:hi,n:n,per:per,cons:cons,pct:cur>0?mi/cur:0,pctlo:cur>0?lo/cur:0,pcthi:cur>0?hi/cur:0}}
var tw={};
function tween(el,to,f,ms){if(!el)return;var from=el.__v||0;el.__v=to;if(rm||ms===0){el.textContent=f(to);return}var t0=performance.now();cancelAnimationFrame(tw[el.__k||(el.__k=Math.random())]);
 (function s(t){var p=Math.min(1,(t-t0)/(ms||700)),e=1-Math.pow(1-p,3);el.textContent=f(from+(to-from)*e);if(p<1)tw[el.__k]=requestAnimationFrame(s)})(t0)}
var $=function(s,c){return (c||root).querySelector(s)};
var CIRC=2*Math.PI*66;
function render(){
 var T=total();
 // field outputs
 root.querySelectorAll('[data-out]').forEach(function(o){var p=o.getAttribute('data-out').split('.'),v=st.v[p[0]][p[1]];o.textContent=fmt(v,o.getAttribute('data-fmt'))});
 // per-line readouts and rail amounts
 LINES.forEach(function(l,i){var c=T.per[l.id],pan=root.querySelector('.pv-ov-panel[data-line="'+l.id+'"]');
  var amt=railLi[i+1].querySelector('.amt');
  if(c){pan.querySelector('[data-r=cur]').textContent=money(c.cur)+' a year';pan.querySelector('[data-r=mi]').textContent=money(c.mi)+' a year';pan.querySelector('[data-r=rng]').textContent=money(c.lo)+' to '+money(c.hi);amt.textContent=money(c.mi)}
  else{pan.querySelector('[data-r=cur]').textContent='Not included';pan.querySelector('[data-r=mi]').textContent='$0';pan.querySelector('[data-r=rng]').textContent='$0';amt.textContent=''}
  railLi[i+1].classList.toggle('off',!c)});
 // live aside
 var live=$('.pv-ov-live');if(live){tween($('[data-live=total]',live),T.mi,money,600);$('[data-live=range]',live).textContent='Range '+money(T.lo)+' to '+money(T.hi);
  var pct=T.pct*100;tween($('[data-live=pct]',live),pct,function(x){return x.toFixed(1)+'%'},600);
  var fg=$('.fg',live);fg.style.strokeDasharray=CIRC;fg.style.strokeDashoffset=CIRC*(1-Math.min(1,T.pct/0.3));
  var mk=$('.mark',live),goal=R.goal*100;
  if(T.n===0){mk.className='mark';mk.textContent='Turn on at least one line to see an estimate.'}
  else if(T.pct>=R.goal){mk.className='mark ok';mk.textContent='Clears the '+goal.toFixed(0)+'% mark. Even the low case is '+(T.pctlo*100).toFixed(1)+'%.'}
  else{mk.className='mark';mk.textContent='Below the '+goal.toFixed(0)+'% mark so far. Turn on more lines: the saving grows with each one Kelly takes over.'}
  var max=0;LINES.forEach(function(l){var c=T.per[l.id];if(c&&c.mi>max)max=c.mi});if(T.cons.mi>max)max=T.cons.mi;
  LINES.forEach(function(l){var c=T.per[l.id],li=live.querySelector('[data-bar="'+l.id+'"]');li.querySelector('.a').textContent=c?money(c.mi):'off';li.querySelector('.bar i').style.width=c&&max?Math.max(3,c.mi/max*100)+'%':'0'});
  var cl=live.querySelector('[data-bar="cons"]');cl.querySelector('.a').textContent=T.cons.mi?money(T.cons.mi):'$0';cl.querySelector('.bar i').style.width=T.cons.mi&&max?Math.max(3,T.cons.mi/max*100)+'%':'0'}
 // results panel
 var rp=$('.pv-ov-res');if(rp&&!rp.hidden){fillResult(T)}
 return T}
function fillResult(T){
 var res=$('.pv-ov-res');
 tween($('[data-res=total]',res),T.mi,money,1100);
 $('[data-res=range]',res).textContent='Likely range '+money(T.lo)+' to '+money(T.hi)+' a year';
 tween($('[data-res=pct]',res),T.pct*100,function(x){return x.toFixed(1)+'%'},1100);
 var pr=$('[data-res=pctrange]',res);if(pr)pr.textContent=(T.pctlo*100).toFixed(1)+'% to '+(T.pcthi*100).toFixed(1)+'%';
 $('[data-res=cur]',res).textContent=money(T.cur);
 $('[data-res=head]',res).textContent=T.pct>=R.goal?'Your estimated saving clears '+(R.goal*100).toFixed(0)+'%':'Your estimated saving, with room to grow';
 $('[data-res=sub]',res).textContent=T.pct>=R.goal?'Low case '+(T.pctlo*100).toFixed(1)+'%, high case '+(T.pcthi*100).toFixed(1)+'% of what these lines cost you today.':'Today this lands under '+(R.goal*100).toFixed(0)+'%. Adding lines raises it: each one Kelly takes over removes a vendor and an invoice.';
 var tb=$('tbody',res);tb.innerHTML='';var mx=0;
 LINES.forEach(function(l){var c=T.per[l.id];if(c&&c.mi>mx)mx=c.mi});if(T.cons.mi>mx)mx=T.cons.mi;
 LINES.forEach(function(l){var c=T.per[l.id];if(!c)return;var tr=document.createElement('tr');tr.innerHTML='<td>'+l.name+'</td><td class="n">'+money(c.cur)+'</td><td class="n g">'+money(c.mi)+'</td><td class="n">'+money(c.lo)+' to '+money(c.hi)+'</td><td><div class="meter"><i></i></div></td>';tb.appendChild(tr);requestAnimationFrame(function(){tr.querySelector('i').style.width=(mx?c.mi/mx*100:0)+'%'})});
 if(T.cons.vend>0){var tr=document.createElement('tr');tr.innerHTML='<td>Vendor consolidation ('+T.cons.vend+' fewer '+(T.cons.vend===1?'vendor':'vendors')+', one agreement)</td><td class="n">Admin time</td><td class="n g">'+money(T.cons.mi)+'</td><td class="n">'+money(T.cons.lo)+' to '+money(T.cons.hi)+'</td><td><div class="meter"><i></i></div></td>';tb.appendChild(tr);requestAnimationFrame(function(){tr.querySelector('i').style.width=(mx?T.cons.mi/mx*100:0)+'%'})}
 var hid=$('[name=summary]',res);if(hid){hid.value=JSON.stringify({inputs:st.v,included:st.inc,estimate:{current:Math.round(T.cur),saving_low:Math.round(T.lo),saving_mid:Math.round(T.mi),saving_high:Math.round(T.hi),percent:+(T.pct*100).toFixed(1)}})}
 var g=$('.fg',res);if(g){g.style.strokeDasharray=CIRC;g.style.strokeDashoffset=CIRC;requestAnimationFrame(function(){requestAnimationFrame(function(){g.style.strokeDashoffset=CIRC*(1-Math.min(1,T.pct/0.3))})})}
}
function go(n,quiet){st.step=Math.max(0,Math.min(panels.length-1,n));panels.forEach(function(p,i){p.hidden=i!==st.step});
 railLi.forEach(function(l,i){l.classList.toggle('on',i===st.step)});
 var live=$('.pv-ov-live');if(live)live.hidden=false;
 render();if(quiet)return;var top=root.getBoundingClientRect().top+scrollY-90;if(scrollY>top)scrollTo({top:top,behavior:rm?'auto':'smooth'});
 var h=panels[st.step].querySelector('h2,h3.t');if(h){h.setAttribute('tabindex','-1');h.focus({preventScroll:true})}}
root.addEventListener('input',function(e){var t=e.target;if(t.matches('input[type=range][data-line]')){st.v[t.getAttribute('data-line')][t.getAttribute('data-k')]=+t.value;render()}
 else if(t.matches('input[data-inc]')){var id=t.getAttribute('data-inc');st.inc[id]=t.checked;var f=t.closest('.pv-ov-panel').querySelector('.pv-ov-fields');f.classList.toggle('dim',!t.checked);render()}});
root.addEventListener('click',function(e){var b=e.target.closest('[data-go]');if(b){var a=b.getAttribute('data-go');if(a==='next')go(st.step+1);else if(a==='back')go(st.step-1);else if(a==='start')go(1);else if(a==='res')go(panels.length-1);else go(+a);return}
 var r=e.target.closest('.pv-ov-rail button');if(r){go(+r.getAttribute('data-i'))}
 if(e.target.closest('[data-print]')){window.print()}});
var form=$('.pv-ov-cta form');if(form){form.addEventListener('submit',function(e){e.preventDefault();var th=$('.pv-ov-thanks');th.style.display='block';th.focus&&th.setAttribute('tabindex','-1');th.focus();form.querySelector('button').disabled=true})}
go(0,true);
})();
"""


def _overview(s, ctx):
    E, RAW, L = ctx["E"], ctx["RAW"], ctx["L"]
    sid = s.get("id", "overview")
    rates = json.loads(json.dumps(OV_RATES))
    for k, v in (s.get("rates") or {}).items():
        if isinstance(v, dict) and isinstance(rates.get(k), dict):
            rates[k].update(v)
        else:
            rates[k] = v
    lines = OV_LINES
    # rail: profile intro + 6 lines + results
    rail = '<li class="on"><button type="button" data-i="0"><span class="ic">' + _svg("profile") + '</span><span>Start</span></button></li>'
    for i, l in enumerate(lines, start=1):
        rail += f'<li><button type="button" data-i="{i}"><span class="ic">{_svg(l["icon"])}</span><span>{E(l["short"])}</span><span class="amt"></span></button></li>'
    rail += f'<li><button type="button" data-i="{len(lines) + 1}"><span class="ic">{_svg("chart")}</span><span>Your result</span></button></li>'

    intro = (f'<section class="pv-ov-panel" data-step="0"><div class="k">Step 1 of {len(lines) + 2}</div><h2>{E(s.get("intro_title", "Six service lines. One honest number."))}</h2>'
             f'<p class="b">{E(s.get("intro_body", "Walk through the lines your office pays for today. Leave out any that Kelly would not take over. The estimate updates as you move, and the last page gives you a range, not a promise."))}</p>'
             f'<div class="pv-ov-read" style="margin-top:0"><div><div class="kk">Takes about</div><div class="vv">3 minutes</div></div><div><div class="kk">You need</div><div class="vv">Rough numbers</div></div><div><div class="kk">You get</div><div class="vv g">A written analysis</div></div></div>'
             f'<div class="pv-ov-nav"><span></span><button type="button" class="go" data-go="start">Start the Overview</button></div></section>')

    panels = ""
    for i, l in enumerate(lines, start=1):
        fields = "".join(_field_html(l["id"], f) for f in l["fields"])
        last = i == len(lines)
        panels += (f'<section class="pv-ov-panel" data-step="{i}" data-line="{l["id"]}" hidden><div class="k">Step {i + 1} of {len(lines) + 2}</div><h3 class="t">{E(l["name"])}</h3>'
                   f'<p class="b">{E(l["blurb"])}</p>'
                   f'<label class="pv-ov-tog"><input type="checkbox" data-inc="{l["id"]}" checked><span>Include {E(l["name"].lower())} in my Overview</span></label>'
                   f'<div class="pv-ov-fields">{fields}</div>'
                   f'<div class="pv-ov-read"><div><div class="kk">Costs you today</div><div class="vv" data-r="cur">$0</div></div><div><div class="kk">Estimated saving</div><div class="vv g" data-r="mi">$0</div></div><div><div class="kk">Likely range</div><div class="vv" data-r="rng">$0</div></div></div>'
                   f'<div class="pv-ov-nav"><button type="button" data-go="back">Back</button><button type="button" class="go" data-go="{"res" if last else "next"}">{"See my result" if last else "Next line"}</button></div></section>')

    asm = "".join(f"<li>{E(t)}</li>" for t in s.get("assumptions", [
        "Print: 1.8 cents per mono page, 9 cents per color page, and 25 minutes a week per device for ordering supplies and chasing repairs, at $28 an hour. Managed print saves 12 to 28 percent of that, 18 percent typical.",
        "Documents: staff hours on paper handling at $28 an hour. Scan to DocuWare workflows save 20 to 45 percent of them, 30 percent typical.",
        "Production print: 10 to 28 percent against outside print shop spend, 15 percent typical, net of the equipment.",
        "IT: 5 to 18 percent against what the office pays for support, backup, licences and break-fix, 10 percent typical.",
        "Mailing: 4 to 11 percent on postage through FP commercial rates, and 18 to 45 percent of mailroom hours with inserters and a mailroom printer.",
        "Water, ice and coffee: 6 to 18 percent, 10 percent typical.",
        "Consolidation: three hours a month of admin per vendor you stop managing, at $28 an hour, scaled 0.5 to 1.2 times.",
        "These are DRAFT planning ranges for Kelly to confirm. They are not a quote or a guarantee. The assessment replaces every one with your meters and your invoices."]))

    result = (f'<section class="pv-ov-panel pv-ov-res" data-step="{len(lines) + 1}" hidden><div class="k">Your Full Office Overview</div>'
              f'<h2 data-res="head">Your estimated saving</h2><p class="b" data-res="sub"></p>'
              f'<div class="big"><span data-res="total">$0</span><small> a year</small></div><div class="rng" data-res="range"></div>'
              f'<div class="pv-ov-read"><div><div class="kk">Share of today\'s cost</div><div class="vv g" data-res="pct">0%</div></div><div><div class="kk">Cost of these lines today</div><div class="vv" data-res="cur">$0</div></div><div><div class="kk">Low case to high case</div><div class="vv" data-res="pctrange">0%</div></div></div>'
              f'<div class="pv-ov-tw" tabindex="0" role="region" aria-label="Savings by line"><table class="pv-ov-table"><thead><tr><th>Line</th><th>Today</th><th>Saving</th><th>Range</th><th></th></tr></thead><tbody></tbody></table></div>'
              f'<details class="pv-ov-asm"><summary>What this estimate is built on</summary><ul>{asm}</ul></details>'
              f'<div class="pv-ov-cta"><h3>{E(s.get("cta_title", "Get the written Office Analysis"))}</h3><p class="n">{E(s.get("cta_body", "A Kelly specialist reviews these numbers, walks your office and replaces every estimate with a measured figure. You keep the report whether or not you buy."))}</p>'
              f'<form class="full" style="display:contents" autocomplete="on"><div class="pv-ov-f"><label for="{sid}-n"><span>Name</span></label><input id="{sid}-n" type="text" autocomplete="name" required></div>'
              f'<div class="pv-ov-f"><label for="{sid}-c"><span>Company</span></label><input id="{sid}-c" type="text" autocomplete="organization"></div>'
              f'<div class="pv-ov-f"><label for="{sid}-e"><span>Work email</span></label><input id="{sid}-e" type="email" autocomplete="email" required></div>'
              f'<div class="pv-ov-f"><label for="{sid}-p"><span>Phone</span></label><input id="{sid}-p" type="tel" autocomplete="tel"></div>'
              f'<input type="hidden" name="summary"><button class="q-btn full" type="submit">{E(s.get("submit", "Send me the analysis"))}</button></form>'
              f'<div class="pv-ov-thanks" role="status">Thank you. A person from your nearest Kelly branch replies, not an autoresponder. Or call 1-800-34-KELLY.</div></div>'
              f'<div class="pv-ov-nav"><button type="button" data-go="back">Adjust my numbers</button><button type="button" data-print>Save or print this page</button></div>'
              f'<p class="pv-ov-fine">{E(s.get("fine", "Estimates only, from typical planning ranges that Kelly will confirm. Nothing here is a quote, a guarantee or a promise of a specific saving."))}</p></section>')

    live_lines = "".join(f'<li data-bar="{l["id"]}"><span>{E(l["short"])}</span><span class="a">$0</span><div class="bar"><i></i></div></li>' for l in lines)
    live_lines += '<li data-bar="cons"><span>Fewer vendors</span><span class="a">$0</span><div class="bar"><i></i></div></li>'
    live = (f'<aside class="pv-ov-live" aria-live="polite"><div class="k">Estimated saving so far</div><div class="v" data-live="total">$0</div><div class="r" data-live="range"></div>'
            f'<div class="pv-ov-gauge"><svg viewBox="0 0 160 160" aria-hidden="true"><circle class="bg" cx="80" cy="80" r="66"/><circle class="fg" cx="80" cy="80" r="66"/>'
            f'<line class="tick" x1="80" y1="6" x2="80" y2="22" transform="rotate({round(0.10 / 0.30 * 360)} 80 80)"/></svg><div class="c"><b data-live="pct">0%</b><span>of what you spend</span></div></div>'
            f'<ul class="lines">{live_lines}</ul><div class="mark"></div></aside>')

    cfg = json.dumps({"rates": rates, "lines": [{"id": l["id"], "name": l["name"], "fields": [{"k": f["k"], "def": f["def"]} for f in l["fields"]]} for l in lines]})
    js = "<script>" + OV_JS.replace("__ID__", sid).replace("__CFG__", cfg) + "</script>"
    hero = (f'<section class="q-section pv-dark pv-ov-hero"><div class="pv-grid-bg" aria-hidden="true"></div><div class="pv-orb a" aria-hidden="true"></div><div class="q-container">'
            f'<div class="q-eyebrow">{E(s.get("eyebrow", "Full Office Overview and Analysis"))}</div><h1 class="q-h1">{RAW(s["heading"])}</h1>'
            f'<p class="q-lead">{E(s.get("subhead", ""))}</p><div class="badges">{"".join(f"<span>{E(b)}</span>" for b in s.get("badges", []))}</div></div></section>')
    return (f'{hero}<section class="q-section pv-ov" id="{E(sid)}"><div class="q-container"><div class="pv-ov-app"><ol class="pv-ov-rail" aria-label="Overview steps">{rail}</ol>'
            f'<div class="pv-ov-stage"><div>{intro}{panels}{result}</div>{live}</div></div></div>{js}</section>')


# ------------------------------------------------------------------------------ global JS

JS3 = r"""(function(){var rm=matchMedia('(prefers-reduced-motion: reduce)').matches;
/* reading progress */
var bar=document.createElement('div');bar.className='pv-progress';bar.setAttribute('aria-hidden','true');document.body.appendChild(bar);
function pr(){var h=document.documentElement.scrollHeight-innerHeight;bar.style.transform='scaleX('+(h>0?Math.min(1,scrollY/h):0)+')'}
addEventListener('scroll',pr,{passive:true});pr();
/* counters */
var cs=[].slice.call(document.querySelectorAll('[data-count]'));
function fin(b){var v=+b.getAttribute('data-count'),d=+b.getAttribute('data-dec')||0,s=b.getAttribute('data-suffix')||'';b.innerHTML=v.toLocaleString('en-US',{minimumFractionDigits:d,maximumFractionDigits:d})+(s?'<small>'+s+'</small>':'')}
if(cs.length&&'IntersectionObserver' in window&&!rm){cs.forEach(function(b){var v=+b.getAttribute('data-count'),d=+b.getAttribute('data-dec')||0,s=b.getAttribute('data-suffix')||'';b.innerHTML=(0).toFixed(d)+(s?'<small>'+s+'</small>':'')});
 var io=new IntersectionObserver(function(es){es.forEach(function(e){if(!e.isIntersecting)return;io.unobserve(e.target);var b=e.target,v=+b.getAttribute('data-count'),d=+b.getAttribute('data-dec')||0,s=b.getAttribute('data-suffix')||'',t0=performance.now();
  (function f(t){var p=Math.min(1,(t-t0)/1600),k=1-Math.pow(1-p,4),x=v*k;b.innerHTML=x.toLocaleString('en-US',{minimumFractionDigits:d,maximumFractionDigits:d})+(s?'<small>'+s+'</small>':'');if(p<1)requestAnimationFrame(f)})(t0)})},{threshold:.4});
 cs.forEach(function(b){io.observe(b)});setTimeout(function(){cs.forEach(function(b){if(b.getBoundingClientRect().top<innerHeight*0.9&&b.textContent.trim().charAt(0)==='0'&&+b.getAttribute('data-count')!==0)fin(b)})},4000)}
/* spotlight follows the pointer on dark showpiece sections */
if(!rm&&matchMedia('(pointer:fine) and (min-width:1025px)').matches){document.querySelectorAll('.pv-dark').forEach(function(s){s.addEventListener('pointermove',function(e){var r=s.getBoundingClientRect();var o=s.querySelector('.pv-orb.a');if(o){o.style.transform='translate('+((e.clientX-r.left)/r.width-.5)*60+'px,'+((e.clientY-r.top)/r.height-.5)*40+'px)'}})})}
})();"""

RENDER_EXTRA3 = {
    "product3d": _product3d, "countband": _countband, "ticker": _ticker, "pulseflow": _pulseflow,
    "itdirector": _itdirector, "photoband": _photoband, "savingstease": _savingstease, "overview": _overview,
}
