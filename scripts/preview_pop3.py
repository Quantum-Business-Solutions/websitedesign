"""Pop pass 3: conversion tools and trust pages for the DMP preview.

Section types (all read the theme variables, so Showcase, Clean and Press pick them up):
  p3assess   one-question-at-a-time yes / not sure / no assessment with progress, back, score ring and three
             'where to look' links. Server HTML is a plain checklist of every question (no JS needed).
  p3calc     the service-call savings estimator: the visitor types their own numbers, nothing is pre-filled.
  p3stories  dealer story hub cards (placeholder cards plus published stories)
  p3story    the dealer story template page layout, every value marked as a placeholder
  p3gate     gated lead magnet: cover mock, gate form, thank-you state, delivery email mock
  p3tiles    labelled fact tiles ('stated by DMP', 'to confirm', 'done', 'to do') with optional links
  p3nf       the 404 page body

Also: a site-wide consent banner (CSS and JS here, injected by JS so no page HTML changes).
Registered in preview.py as RENDER_POP3, POP3_CSS and POP3_JS.
No em or en dashes, nothing under 13px, 44px tap targets, prefers-reduced-motion respected.
"""
from __future__ import annotations

import json

POP3_CSS = r"""
/* ===== pop3: shared ===== */
:root{--pp3-line:color-mix(in srgb,var(--fg) 22%,var(--bg))}
.pp3-sec{padding:clamp(56px,7vw,96px) 0}
.pp3-wrap{max-width:var(--maxw,1200px);margin:0 auto;padding:0 clamp(16px,4vw,32px)}
.pp3-hd{max-width:760px;margin:0 0 clamp(28px,3.4vw,44px)}
.pp3-hd .q-h2{margin:18px 0 0}.pp3-hd .q-lead{margin:14px 0 0}
.pp3-btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;min-height:48px;padding:0 24px;border-radius:999px;font:700 15.5px/1 var(--q-sans,inherit);text-decoration:none;border:2px solid transparent;cursor:pointer;transition:transform .25s,box-shadow .25s,background .25s}
.pp3-btn.gold{background:var(--q-gold);color:#111}.pp3-btn.gold:hover{transform:translateY(-2px);box-shadow:0 14px 28px -14px rgba(0,0,0,.5)}
.pp3-btn.ghost{background:transparent;color:var(--fg);border-color:var(--pp3-line)}.pp3-btn.ghost:hover{border-color:var(--fg)}
.pp3-btn[disabled]{opacity:.45;cursor:not-allowed;transform:none;box-shadow:none}
.pp3-btn:focus-visible,.pp3-opt:focus-visible,.pp3-cc button:focus-visible,.pp3-cc a:focus-visible,.pp3-in:focus-visible{outline:3px solid var(--fg);outline-offset:3px}
.pp3-tag{display:inline-flex;align-items:center;min-height:26px;padding:0 12px;border-radius:999px;border:1.5px solid var(--pp3-line);font-size:13px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;color:var(--fg);background:var(--bg)}
.pp3-scard .pp3-tag{align-self:flex-start}
.pp3-tag.confirm{border-color:var(--q-gold);background:color-mix(in srgb,var(--q-gold) 24%,var(--bg))}
.pp3-tag.done{border-color:var(--fg)}
.pp3-note{margin:18px 0 0;font-size:14px;line-height:1.5;color:var(--fg-muted)}
.pp3-note b{color:var(--fg)}
.pp3-sub a,.pp3-note a{text-decoration:underline;text-underline-offset:3px}
@media(prefers-reduced-motion:reduce){.pp3-btn,.pp3-opt,.pp3-ring-c,.pp3-prog i,.pp3-cc{transition:none!important;animation:none!important}}

.pp3-gform[hidden],.pp3-thanks[hidden],.pp3-as-js[hidden],.pp3-as-nojs[hidden],.pp3-card[hidden],.pp3-prefs[hidden],.pp3-out [hidden]{display:none!important}
/* ===== assessment ===== */
.pp3-as{max-width:900px}
.pp3-card{background:var(--card,var(--bg-alt));border:1px solid var(--pp3-line);border-radius:calc(var(--radius,14px) + 8px);padding:clamp(22px,3.4vw,44px);box-shadow:0 30px 70px -48px rgba(0,0,0,.5)}
.pp3-prog{height:10px;border-radius:99px;background:var(--pp3-line);overflow:hidden}
.pp3-prog i{display:block;height:100%;width:0;background:var(--q-gold);border-radius:99px;transition:width .35s cubic-bezier(.2,.7,.2,1)}
.pp3-prog-row{display:flex;justify-content:space-between;gap:12px;margin:0 0 10px;font-size:14px;font-weight:600;color:var(--fg-muted)}
.pp3-qarea{margin:30px 0 8px;font-size:13px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--fg-muted)}
.pp3-qtext{margin:0;font-size:clamp(22px,2.8vw,32px);line-height:1.2;letter-spacing:-.02em;font-weight:700;outline:0}
.pp3-hint{margin:12px 0 0;font-size:16px;line-height:1.5;color:var(--fg-muted)}
.pp3-opts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin:28px 0 0}
.pp3-opt{display:flex;align-items:center;justify-content:center;min-height:68px;padding:0 16px;border-radius:calc(var(--radius,14px) + 4px);border:2px solid var(--pp3-line);background:var(--bg);color:var(--fg);font:700 19px/1 var(--q-sans,inherit);cursor:pointer;transition:transform .2s,border-color .2s,background .2s}
.pp3-opt:hover{border-color:var(--fg);transform:translateY(-2px)}
.pp3-opt[aria-pressed=true]{background:var(--q-gold);border-color:var(--q-gold);color:#111}
.pp3-nav{display:flex;justify-content:space-between;align-items:center;gap:12px;margin:26px 0 0}
.pp3-back{background:none;border:0;color:var(--fg);font:600 15px/1 var(--q-sans,inherit);min-height:44px;padding:0 4px;cursor:pointer;text-decoration:underline;text-underline-offset:4px}
.pp3-back[disabled]{opacity:.35;cursor:default;text-decoration:none}
.pp3-back:focus-visible{outline:3px solid var(--fg);outline-offset:3px;border-radius:6px}
.pp3-res-top{display:grid;grid-template-columns:auto 1fr;gap:clamp(20px,4vw,48px);align-items:center}
.pp3-ring{position:relative;width:190px;height:190px}
.pp3-ring svg{width:100%;height:100%;transform:rotate(-90deg)}
.pp3-ring-t{stroke:var(--pp3-line)}.pp3-ring-c{stroke:var(--q-gold);transition:stroke-dashoffset 1s cubic-bezier(.2,.7,.2,1)}
.pp3-ring b{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:46px;line-height:1;letter-spacing:-.03em}
.pp3-ring b small{margin-top:6px;font-size:13px;font-weight:600;letter-spacing:.04em;color:var(--fg-muted)}
.pp3-res-top h3{margin:0;font-size:clamp(24px,3vw,34px);letter-spacing:-.02em;line-height:1.15;outline:0}
.pp3-res-top p{margin:12px 0 0;color:var(--fg-muted);font-size:16.5px;line-height:1.5}
.pp3-areas{list-style:none;margin:30px 0 0;padding:0;display:grid;gap:12px}
.pp3-areas li{display:grid;grid-template-columns:minmax(120px,210px) 1fr auto;gap:14px;align-items:center;font-size:15px}
.pp3-areas .bar{height:8px;border-radius:99px;background:var(--pp3-line);overflow:hidden}.pp3-areas .bar i{display:block;height:100%;background:var(--fg);border-radius:99px}
.pp3-areas .v{font-weight:700;min-width:44px;text-align:right}
.pp3-h4{margin:38px 0 6px;font-size:13px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--fg-muted)}
.pp3-recs{list-style:none;margin:14px 0 0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
.pp3-rec{display:flex;flex-direction:column;gap:10px;height:100%;padding:22px;border-radius:calc(var(--radius,14px) + 4px);border:1px solid var(--pp3-line);background:var(--bg)}
.pp3-rec .n{width:34px;height:34px;border-radius:50%;background:var(--q-gold);color:#111;font-weight:800;display:grid;place-items:center}
.pp3-rec h4{margin:0;font-size:18px;line-height:1.25}.pp3-rec p{margin:0;font-size:15px;line-height:1.5;color:var(--fg-muted)}
.pp3-rec a{color:var(--fg);font-weight:700;text-decoration:underline;min-height:44px;display:inline-flex;align-items:center;text-underline-offset:4px}
.pp3-rec .links{margin-top:auto;display:flex;flex-direction:column}
.pp3-save{margin-top:34px;padding-top:28px;border-top:1px solid var(--pp3-line)}
.pp3-save h4{margin:0 0 6px;font-size:20px}
.pp3-save .q-form{max-width:460px;margin-top:14px}
.pp3-as-nojs ol{margin:0;padding:0 0 0 22px;display:grid;gap:14px}
.pp3-as-nojs li{font-size:17px;line-height:1.45}.pp3-as-nojs li span{display:block;font-size:13px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--fg-muted);margin-bottom:2px}
.pp3-as-nojs li a{color:var(--fg);font-weight:600}
@media(max-width:900px){.pp3-recs{grid-template-columns:minmax(0,1fr)}}
@media(max-width:640px){.pp3-opts{grid-template-columns:minmax(0,1fr)}.pp3-opt{min-height:60px}.pp3-res-top{grid-template-columns:minmax(0,1fr);justify-items:start}.pp3-ring{width:160px;height:160px}.pp3-areas li{grid-template-columns:1fr auto}.pp3-areas .bar{grid-column:1/-1;order:3}}

/* ===== estimator ===== */
.pp3-calc{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,.95fr);gap:clamp(20px,3vw,40px);align-items:start}
.pp3-fields{display:grid;gap:18px}
.pp3-fld label{display:block;font-weight:700;font-size:16px;margin:0 0 6px}
.pp3-fld small{display:block;font-size:14px;line-height:1.4;color:var(--fg-muted);margin:0 0 8px}
.pp3-inw{position:relative}
.pp3-inw span{position:absolute;left:16px;top:50%;transform:translateY(-50%);font-weight:700;color:var(--fg-muted);pointer-events:none}
.pp3-inw.suf span{left:auto;right:16px}
.pp3-in{width:100%;min-height:54px;padding:0 16px 0 34px;border-radius:12px;border:2px solid var(--pp3-line);background:var(--bg);color:var(--fg);font:600 18px/1 var(--q-sans,inherit)}
.pp3-inw.plain .pp3-in{padding-left:16px}.pp3-inw.suf .pp3-in{padding:0 40px 0 16px}
.pp3-in::placeholder{color:var(--fg-muted);font-weight:500;opacity:1}
.pp3-in[aria-invalid=true]{border-color:#c8392b}
.pp3-err{margin:6px 0 0;font-size:14px;color:#a3271a;min-height:0}
.pp3-out{position:sticky;top:96px;background:var(--bg-alt);border:1px solid var(--pp3-line);border-radius:calc(var(--radius,14px) + 8px);padding:clamp(22px,3vw,34px)}
.pp3-out .lbl{display:block;font-size:13px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--fg-muted)}
.pp3-empty{margin:6px 0 0;font-size:22px;font-weight:700;line-height:1.25;letter-spacing:-.01em}
.pp3-big{display:block;margin:6px 0 0;font-size:clamp(38px,5vw,60px);line-height:1;letter-spacing:-.035em;font-weight:800}
.pp3-big.yr{font-size:clamp(28px,3.4vw,38px);color:var(--fg)}
.pp3-rows{margin:22px 0 0;padding:18px 0 0;border-top:1px solid var(--pp3-line);display:grid;gap:10px;font-size:15px}
.pp3-rows div{display:flex;justify-content:space-between;gap:14px}.pp3-rows dt{color:var(--fg-muted)}.pp3-rows dd{margin:0;font-weight:700;text-align:right}
.pp3-formula{margin:18px 0 0;padding:14px 16px;border-radius:12px;background:var(--bg);border:1px dashed var(--pp3-line);font-size:14.5px;line-height:1.55;color:var(--fg-muted)}
.pp3-formula b{color:var(--fg)}
.pp3-banner{display:inline-flex;margin:0 0 22px;padding:10px 16px;border-radius:12px;background:var(--q-gold);color:#111;font-weight:800;font-size:16px}
.pp3-copy{margin-top:20px;display:flex;gap:12px;align-items:center;flex-wrap:wrap}
.pp3-copied{font-size:14px;font-weight:600}
@media(max-width:900px){.pp3-calc{grid-template-columns:minmax(0,1fr)}.pp3-out{position:static}}

/* ===== tiles ===== */
.pp3-tiles{display:grid;gap:18px;grid-template-columns:repeat(var(--cols,3),minmax(0,1fr));list-style:none;margin:0;padding:0}
.pp3-tile{display:flex;flex-direction:column;gap:12px;height:100%;padding:26px;border-radius:calc(var(--radius,14px) + 4px);border:1px solid var(--pp3-line);background:var(--card,var(--bg-alt))}
.pp3-tile h3{margin:0;font-size:20px;line-height:1.25;letter-spacing:-.01em}
.pp3-tile p{margin:0;font-size:16px;line-height:1.55;color:var(--fg-muted)}
.pp3-tile .lnk{margin-top:auto;color:var(--fg);font-weight:700;min-height:44px;display:inline-flex;align-items:center;text-underline-offset:4px}
.pp3-tile .tags{display:flex;gap:8px;flex-wrap:wrap}
@media(max-width:1024px){.pp3-tiles{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:640px){.pp3-tiles{grid-template-columns:minmax(0,1fr)}}

/* ===== stories ===== */
.pp3-sgrid{display:grid;gap:22px;grid-template-columns:repeat(2,minmax(0,1fr));list-style:none;margin:0;padding:0}
.pp3-scard{position:relative;display:flex;flex-direction:column;gap:14px;height:100%;padding:28px;border-radius:calc(var(--radius,14px) + 8px);border:1px solid var(--pp3-line);background:var(--card,var(--bg-alt));overflow:hidden}
.pp3-scard.real{background:var(--bg);border:2px solid var(--fg)}
.pp3-scard.ph{border-style:dashed}
.pp3-scard h3{margin:0;font-size:clamp(22px,2.4vw,28px);line-height:1.15;letter-spacing:-.02em}
.pp3-scard p{margin:0;font-size:16px;line-height:1.55;color:var(--fg-muted)}
.pp3-scard .mt{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin:4px 0 0}
.pp3-scard .mt span{display:block;padding:12px;border-radius:10px;border:1px dashed var(--pp3-line);font-size:13px;color:var(--fg-muted);text-align:center}
.pp3-scard .mt span b{display:block;font-size:22px;color:var(--pp3-line);line-height:1.1}
.pp3-scard .go{margin-top:auto;color:var(--fg);font-weight:700;min-height:44px;display:inline-flex;align-items:center;text-underline-offset:4px}
.pp3-scard .go.stretch::after{content:"";position:absolute;inset:0}
.pp3-metrics{display:grid;gap:0;grid-template-columns:repeat(3,minmax(0,1fr));border-radius:calc(var(--radius,14px) + 8px);overflow:hidden;background:#111;color:#fff}
.pp3-metrics div{padding:clamp(22px,3vw,40px);border-left:1px solid rgba(255,255,255,.14)}.pp3-metrics div:first-child{border-left:0}
.pp3-metrics b{display:block;font-size:clamp(34px,4.4vw,56px);line-height:1;letter-spacing:-.03em;color:transparent;-webkit-text-stroke:1.5px var(--q-gold)}
.pp3-metrics span{display:block;margin-top:10px;font-size:15px;color:#d6d6d6}
.pp3-quote{margin:0;padding:clamp(26px,4vw,48px);border-radius:calc(var(--radius,14px) + 8px);background:var(--bg-alt);border:1px solid var(--pp3-line);border-left:8px solid var(--q-gold)}
.pp3-quote p{margin:0;font-size:clamp(20px,2.4vw,28px);line-height:1.4;letter-spacing:-.01em;font-weight:600}
.pp3-quote footer{margin-top:18px;font-size:15px;color:var(--fg-muted)}
.pp3-csr{display:grid;gap:20px;grid-template-columns:repeat(3,minmax(0,1fr))}
.pp3-csr article{padding:28px;border-radius:calc(var(--radius,14px) + 4px);border:1px solid var(--pp3-line);background:var(--card,var(--bg-alt))}
.pp3-csr .k{display:inline-grid;place-items:center;width:38px;height:38px;border-radius:50%;background:var(--q-gold);color:#111;font-weight:800;margin-bottom:14px}
.pp3-csr h3{margin:0 0 10px;font-size:22px}.pp3-csr p{margin:0;color:var(--fg-muted);line-height:1.55;font-size:16px}
.pp3-chips{display:flex;flex-wrap:wrap;gap:10px;list-style:none;margin:0;padding:0}
.pp3-chips a{display:inline-flex;align-items:center;min-height:44px;padding:0 18px;border-radius:999px;border:1.5px solid var(--pp3-line);color:var(--fg);font-weight:600;text-decoration:none;background:var(--bg)}
.pp3-chips a:hover{border-color:var(--fg)}
.pp3-ribbon{display:inline-flex;margin:0 0 18px;padding:8px 14px;border-radius:8px;background:var(--q-gold);color:#111;font-weight:800;font-size:14px;letter-spacing:.04em}
@media(max-width:900px){.pp3-sgrid,.pp3-csr{grid-template-columns:minmax(0,1fr)}.pp3-metrics{grid-template-columns:minmax(0,1fr)}.pp3-metrics div{border-left:0;border-top:1px solid rgba(255,255,255,.14)}.pp3-metrics div:first-child{border-top:0}}

/* ===== gate ===== */
.pp3-gate{display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr);gap:clamp(28px,5vw,72px);align-items:center}
.pp3-cover{position:relative;aspect-ratio:3/4;max-width:380px;width:100%;margin:0 auto;border-radius:6px 16px 16px 6px;background:#111;color:#fff;padding:34px 30px;display:flex;flex-direction:column;justify-content:space-between;box-shadow:-12px 0 0 -2px #000 inset,0 40px 60px -30px rgba(0,0,0,.6);overflow:hidden;transform:rotate(-2deg)}
.pp3-cover::before{content:"";position:absolute;right:-60px;top:-60px;width:220px;height:220px;border-radius:50%;background:var(--q-gold)}
.pp3-cover::after{content:"";position:absolute;left:30px;right:30px;bottom:90px;height:6px;background:var(--q-gold)}
.pp3-cover small{position:relative;z-index:1;font-size:13px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#d6d6d6}
.pp3-cover strong{position:relative;z-index:1;font-size:clamp(30px,3.4vw,42px);line-height:1.05;letter-spacing:-.03em}
.pp3-cover span{position:relative;z-index:1;font-size:15px;color:var(--q-gold);font-weight:700}
.pp3-gform{display:grid;gap:14px;margin-top:22px;max-width:520px}
.pp3-gform label{font-weight:700;font-size:15px;display:block;margin:0 0 6px}
.pp3-gform .pp3-in{padding:0 16px;font-size:17px}
.pp3-thanks{margin-top:22px;max-width:520px;padding:22px;border-radius:16px;border:2px solid var(--fg);background:var(--bg)}
.pp3-thanks h3{margin:0 0 8px;font-size:24px}.pp3-thanks p{margin:0 0 14px;color:var(--fg-muted);line-height:1.5}
.pp3-inside{display:grid;gap:14px;grid-template-columns:repeat(2,minmax(0,1fr));list-style:none;margin:0;padding:0;counter-reset:ch}
.pp3-inside li{counter-increment:ch;display:grid;grid-template-columns:auto 1fr;gap:16px;padding:20px;border-radius:14px;border:1px dashed var(--pp3-line);background:var(--card,var(--bg-alt))}
.pp3-inside li::before{content:counter(ch);width:40px;height:40px;border-radius:50%;background:var(--q-gold);color:#111;font-weight:800;display:grid;place-items:center}
.pp3-inside b{display:block;font-size:18px}.pp3-inside span{display:block;font-size:15px;color:var(--fg-muted);margin-top:4px;line-height:1.45}
.pp3-mail{max-width:640px;border-radius:14px;border:1px solid var(--pp3-line);background:var(--bg);overflow:hidden;box-shadow:0 30px 60px -44px rgba(0,0,0,.55)}
.pp3-mail .bar{display:flex;gap:8px;align-items:center;padding:12px 18px;background:var(--bg-alt);border-bottom:1px solid var(--pp3-line);font-size:13px;color:var(--fg-muted)}
.pp3-mail .bar i{width:10px;height:10px;border-radius:50%;background:var(--pp3-line)}
.pp3-mail dl{margin:0;padding:16px 22px 0;display:grid;grid-template-columns:70px 1fr;gap:6px 10px;font-size:14.5px}.pp3-mail dt{color:var(--fg-muted)}.pp3-mail dd{margin:0;overflow-wrap:anywhere}
.pp3-mail .body{padding:12px 22px 26px;font-size:15.5px;line-height:1.6}
.pp3-mail .body .pp3-btn{margin-top:10px}
.pp3-mail.sent{outline:3px solid var(--q-gold);outline-offset:4px}
@media(max-width:900px){.pp3-gate{grid-template-columns:minmax(0,1fr)}.pp3-cover{max-width:300px}.pp3-inside{grid-template-columns:minmax(0,1fr)}}

/* ===== 404 ===== */
.pp3-nf{text-align:center}
.pp3-nf .num::before{content:"404"}
.pp3-nf .num{display:block;font-size:clamp(96px,18vw,220px);line-height:.9;font-weight:800;letter-spacing:-.06em;color:transparent;-webkit-text-stroke:3px var(--q-gold)}
.pp3-nf .q-h1{margin:10px auto 0;max-width:760px}
.pp3-nf .q-lead{margin:18px auto 0;max-width:560px}
.pp3-nf .act{display:flex;flex-wrap:wrap;gap:12px;justify-content:center;margin-top:28px}
.pp3-nf ul{list-style:none;margin:40px auto 0;padding:0;max-width:820px;display:grid;gap:12px;grid-template-columns:repeat(4,minmax(0,1fr))}
.pp3-nf ul a{display:flex;align-items:center;justify-content:center;min-height:56px;padding:8px 14px;border-radius:14px;border:1px solid var(--pp3-line);background:var(--card,var(--bg-alt));color:var(--fg);font-weight:700;text-decoration:none;text-align:center}
.pp3-nf ul a:hover{border-color:var(--fg)}
.pp3-nf .ph{margin-top:26px;color:var(--fg-muted)}.pp3-nf .ph a{color:var(--fg);font-weight:700}
@media(max-width:900px){.pp3-nf ul{grid-template-columns:repeat(2,minmax(0,1fr))}}

/* ===== consent banner (preview) ===== */
.pp3-cc{position:fixed;z-index:86;right:64px;bottom:18px;width:min(430px,calc(100vw - 300px));background:var(--bg);color:var(--fg);border:1px solid var(--pp3-line);border-radius:18px;padding:18px 20px 20px;box-shadow:0 24px 70px -20px rgba(0,0,0,.55);font:15px/1.5 var(--q-sans,system-ui);animation:pp3in .35s ease-out}
@keyframes pp3in{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
.pp3-cc .pre{margin:0 0 10px;padding:6px 10px;border-radius:8px;background:var(--bg-alt);border:1px dashed var(--pp3-line);font-size:13px;line-height:1.4;color:var(--fg-muted)}
.pp3-cc h2{margin:0 0 6px;font-size:18px;line-height:1.25}
.pp3-cc p{margin:0 0 12px;font-size:14.5px;color:var(--fg-muted)}
.pp3-cc .row{display:flex;flex-wrap:wrap;gap:8px}
.pp3-cc button{min-height:44px;padding:0 16px;border-radius:999px;border:2px solid var(--fg);background:transparent;color:var(--fg);font:700 14.5px/1 var(--q-sans,inherit);cursor:pointer}
.pp3-cc button.pri{background:var(--q-gold);border-color:var(--q-gold);color:#111}
.pp3-cc button:hover{filter:brightness(.96)}
.pp3-cc fieldset{border:0;margin:0 0 12px;padding:0;display:grid;gap:8px}
.pp3-cc label{display:flex;gap:10px;align-items:center;min-height:44px;font-size:14.5px}
.pp3-cc input[type=checkbox]{width:22px;height:22px;accent-color:#111}
.embedded .pp3-cc{display:none}
@media(max-width:1100px){.pp3-cc{width:min(430px,calc(100vw - 100px))}}
@media(max-width:767px){.pp3-cc{left:10px;right:10px;width:auto;bottom:126px;max-height:calc(100vh - 200px);overflow:auto;padding:14px 16px 16px}.pp3-cc p.txt{display:none}.pp3-cc.open p.txt{display:block}}
@media(prefers-reduced-motion:reduce){.pp3-cc{animation:none}}
"""


# ----------------------------------------------------------------------------- renderers

def _hd(s, ctx):
    E = ctx["E"]
    eb = f'<div class="q-eyebrow">{E(s["eyebrow"])}</div>' if s.get("eyebrow") else ""
    h = f'<h2 class="q-h2">{E(s["heading"])}</h2>' if s.get("heading") else ""
    lead = f'<p class="q-lead">{E(s["intro"])}</p>' if s.get("intro") else ""
    return f'<div class="pp3-hd">{eb}{h}{lead}</div>'


def _json(o):
    return json.dumps(o, ensure_ascii=False).replace("</", "<\\/")


def _assess(s, ctx):
    E, L = ctx["E"], ctx["L"]
    areas = {k: {"title": v["title"], "text": v["text"], "links": [[a, L(b)] for a, b in v["links"]]} for k, v in s["areas"].items()}
    qs = [{"area": q[0], "q": q[1], "hint": q[2]} for q in s["questions"]]
    cfg = _json({"questions": qs, "areas": areas})
    lis = "".join(
        f'<li><span>{E(areas[q["area"]]["title"])}</span>{E(q["q"])} <a href="{E(areas[q["area"]]["links"][0][1])}">{E(areas[q["area"]]["links"][0][0])}</a></li>' for q in qs)
    return f'''{ctx["sec_open"](s)}<div class="pp3-wrap">{_hd(s, ctx)}<div class="pp3-as" data-pp3-assess>
<script type="application/json">{cfg}</script>
<div class="pp3-as-nojs pp3-card"><p class="pp3-note" style="margin:0 0 18px"><b>The scored version needs JavaScript.</b> Here is every question as a plain checklist. Answer yes, not sure or no for each, in a conversation with your team or with Inside Sales.</p><ol>{lis}</ol></div>
<div class="pp3-as-js" hidden>
 <div class="pp3-card pp3-step">
  <div class="pp3-prog-row"><span class="pp3-ptxt">Question 1 of {len(qs)}</span><span class="pp3-ppct">0% done</span></div>
  <div class="pp3-prog" role="progressbar" aria-label="Assessment progress" aria-valuemin="0" aria-valuemax="{len(qs)}" aria-valuenow="0"><i></i></div>
  <p class="pp3-qarea"></p><h3 class="pp3-qtext" tabindex="-1"></h3><p class="pp3-hint"></p>
  <div class="pp3-opts" role="group" aria-label="Your answer"><button type="button" class="pp3-opt" data-v="2" aria-pressed="false">Yes</button><button type="button" class="pp3-opt" data-v="1" aria-pressed="false">Not sure</button><button type="button" class="pp3-opt" data-v="0" aria-pressed="false">No</button></div>
  <div class="pp3-nav"><button type="button" class="pp3-back" disabled>Back</button><span class="pp3-note" style="margin:0">Your answers stay in this tab and are not stored.</span></div>
 </div>
 <div class="pp3-card pp3-res" hidden aria-live="polite">
  <div class="pp3-res-top"><div class="pp3-ring" aria-hidden="true"><svg viewBox="0 0 200 200"><circle class="pp3-ring-t" cx="100" cy="100" r="86" fill="none" stroke-width="16"/><circle class="pp3-ring-c" cx="100" cy="100" r="86" fill="none" stroke-width="16" stroke-linecap="round" stroke-dasharray="540.35" stroke-dashoffset="540.35"/></svg><b><span class="pp3-pct">0%</span><small>illustrative</small></b></div>
  <div><h3 class="pp3-rt" tabindex="-1"></h3><p class="pp3-rp"></p></div></div>
  <ul class="pp3-areas"></ul>
  <p class="pp3-h4">Where to look</p><ol class="pp3-recs"></ol>
  <p class="pp3-note"><b>Illustrative scoring, DMP to confirm.</b> Yes counts 2, not sure 1 and no 0, shown as a share of the possible points. It is a conversation starter, not a rating of your business or a DMP assessment.</p>
  <div class="pp3-save"><h4>Save my results</h4><p class="pp3-note" style="margin:0">Add your details to keep a copy. In this preview the form does not send anything.</p>
   <form class="q-form" onsubmit="return false"><label for="as-n">Name</label><input id="as-n" type="text" autocomplete="name"><label for="as-e">Work email</label><input id="as-e" type="email" autocomplete="email"><input type="submit" class="hs-button" value="Save my results"></form></div>
  <div class="pp3-nav"><button type="button" class="pp3-btn ghost pp3-redo">Start again</button><button type="button" class="pp3-back pp3-edit">Change my last answer</button></div>
 </div>
</div></div></div></section>'''


def _calc(s, ctx):
    E, L = ctx["E"], ctx["L"]
    def fld(i, label, hint, ph, pre="", suf="", step="any"):
        cls = "pp3-inw" + (" suf" if suf else "") + ("" if pre or suf else " plain")
        return (f'<div class="pp3-fld"><label for="{i}">{E(label)}</label><small id="{i}-h">{E(hint)}</small><div class="{cls}">'
                f'{f"<span aria-hidden=true>{pre}</span>" if pre else ""}<input class="pp3-in" id="{i}" type="text" inputmode="decimal" autocomplete="off" placeholder="{E(ph)}" aria-describedby="{i}-h {i}-e">'
                f'{f"<span aria-hidden=true>{suf}</span>" if suf else ""}</div><p class="pp3-err" id="{i}-e" role="alert"></p></div>')
    fields = (fld("pc-calls", "Service calls per month", "Count the calls your company makes in a typical month.", "your number")
              + fld("pc-cost", "Average cost per call", "Vehicle, fuel, parts and anything else a call costs, not counting technician time.", "your number", pre="$")
              + fld("pc-share", "Share that could be handled remotely", "Your own judgement of the calls that need no visit, as a percent from 0 to 100.", "your number", suf="%")
              + fld("pc-rate", "Technician hourly cost", "What an hour of technician time costs you.", "your number", pre="$")
              + fld("pc-hrs", "Technician hours per call (travel plus on site)", "Needed to value technician time. Leave empty to leave labor out.", "your number"))
    caps = "".join(f'<li><b>{E(t)}</b> {E(b)} <a href="{E(L(h))}">{E(lb)}</a></li>' for t, b, lb, h in s["caps"])
    return f'''{ctx["sec_open"](s)}<div class="pp3-wrap">{_hd(s, ctx)}<div class="pp3-calc" data-pp3-calc>
<div><p class="pp3-banner">Your numbers, your math. Not a DMP guarantee.</p><form class="pp3-fields" onsubmit="return false" novalidate aria-label="Your numbers">{fields}</form>
<noscript><p class="pp3-note">The calculator needs JavaScript. The formula is written out on the right, so you can work it by hand.</p></noscript></div>
<div class="pp3-out" aria-live="polite">
 <span class="lbl">Your estimate</span>
 <p class="pp3-empty" data-empty>Enter your numbers to see your estimate</p>
 <div data-result hidden>
  <span class="lbl" style="margin-top:6px">Per month</span><b class="pp3-big" data-month>$0</b>
  <span class="lbl" style="margin-top:18px">Per year</span><b class="pp3-big yr" data-year>$0</b>
  <dl class="pp3-rows"><div><dt>Calls handled remotely each month</dt><dd data-rc>0</dd></div><div><dt>Call costs avoided each month</dt><dd data-cc>$0</dd></div><div><dt>Technician hours freed each month</dt><dd data-hf>0</dd></div><div><dt>Technician time freed each month</dt><dd data-tc>$0</dd></div></dl>
  <div class="pp3-copy"><button type="button" class="pp3-btn gold" data-copy>Copy summary</button><span class="pp3-copied" data-copied role="status"></span></div>
 </div>
 <p class="pp3-formula"><b>The formula.</b> Calls handled remotely = calls per month x share. Monthly savings = calls handled remotely x (cost per call + hours per call x hourly cost). Yearly = monthly x 12. Nothing here is a DMP figure; every input is yours.</p>
</div></div>
<ul class="pp3-notes pp3-sub" style="list-style:none;margin:40px 0 0;padding:0;display:grid;gap:12px;max-width:860px">{caps}</ul>
</div></section>'''


def _tiles(s, ctx):
    E, L = ctx["E"], ctx["L"]
    items = []
    for it in s["items"]:
        tags = "".join(f'<span class="pp3-tag {E(k)}">{E(t)}</span>' for k, t in it.get("tags", []))
        link = f'<a class="lnk" href="{E(L(it["link"][1]))}">{E(it["link"][0])}</a>' if it.get("link") else ""
        items.append(f'<li class="pp3-tile">{f"<div class=tags>{tags}</div>" if tags else ""}<h3>{E(it["title"])}</h3><p>{E(it["text"])}</p>{link}</li>')
    note = f'<p class="pp3-note">{E(s["note"])}</p>' if s.get("note") else ""
    return f'{ctx["sec_open"](s)}<div class="pp3-wrap">{_hd(s, ctx)}<ul class="pp3-tiles" style="--cols:{s.get("cols", 3)}">{"".join(items)}</ul>{note}</div></section>'


def _stories(s, ctx):
    E, L = ctx["E"], ctx["L"]
    out = []
    for it in s["items"]:
        if it.get("real"):
            out.append(f'<li><article class="pp3-scard real"><span class="pp3-tag done">Published story</span><h3>{E(it["title"])}</h3><p>{E(it["text"])}</p><a class="go stretch" href="{E(L(it["href"]))}">Read the story</a></article></li>')
        else:
            out.append(f'<li><article class="pp3-scard ph"><span class="pp3-tag confirm">Placeholder</span><h3>Your dealer story here</h3><p>Story to be supplied by a DMP dealer. The layout holds a headline, three results, a quote and the products used.</p>'
                       f'<div class="mt" aria-hidden="true"><span><b>--</b>result</span><span><b>--</b>result</span><span><b>--</b>result</span></div>'
                       f'<a class="go stretch" href="{E(L(s["template"]))}">See the story layout</a></article></li>')
    return f'{ctx["sec_open"](s)}<div class="pp3-wrap">{_hd(s, ctx)}<ul class="pp3-sgrid">{"".join(out)}</ul></div></section>'


def _story(s, ctx):
    E, L = ctx["E"], ctx["L"]
    m = "".join(f'<div><b>--</b><span>{E(t)}</span></div>' for t in s["metrics"])
    csr = "".join(f'<article><span class="k" aria-hidden="true">{i}</span><h3>{E(t)}</h3><p>{E(b)}</p></article>' for i, (t, b) in enumerate(s["csr"], 1))
    chips = "".join(f'<li><a href="{E(L(h))}">{E(t)}</a></li>' for t, h in s["products"])
    return f'''<section class="q-section"><div class="pp3-wrap"><span class="pp3-ribbon">Placeholder layout. Story to be supplied by a DMP dealer.</span>
<div class="pp3-metrics" role="group" aria-label="Metric band (placeholders)">{m}</div><p class="pp3-note">Metrics are left empty on purpose. Each one would be a number the dealer supplies and DMP confirms.</p></div></section>
<section class="q-section q-bg-alt"><div class="pp3-wrap"><blockquote class="pp3-quote"><p>{E(s["quote"])}</p><footer>{E(s["by"])}</footer></blockquote></div></section>
<section class="q-section"><div class="pp3-wrap">{_hd(s, ctx)}<div class="pp3-csr">{csr}</div></div></section>
<section class="q-section q-bg-alt"><div class="pp3-wrap"><div class="pp3-hd"><div class="q-eyebrow">Products in the story</div><h2 class="q-h2">Links to the products the dealer used.</h2><p class="q-lead">These are examples of where the links would point. The dealer's own list replaces them.</p></div><ul class="pp3-chips">{chips}</ul></div></section>'''


def _gate(s, ctx):
    E, L = ctx["E"], ctx["L"]
    ch = "".join(f'<li><div><b>{E(t)}</b><span>{E(b)}</span></div></li>' for t, b in s["chapters"])
    return f'''{ctx["sec_open"](s)}<div class="pp3-wrap"><div class="pp3-gate" data-pp3-gate>
<div><div class="pp3-cover" role="img" aria-label="Mock cover of the dealer playbook, title to be confirmed"><small>Dealer playbook</small><strong>Title to be confirmed</strong><span>Placeholder cover</span></div></div>
<div><div class="q-eyebrow">{E(s["eyebrow"])}</div><h2 class="q-h2" style="margin-top:18px">{E(s["heading"])}</h2><p class="q-lead" style="margin-top:14px">{E(s["intro"])}</p>
<form class="pp3-gform" novalidate data-gate-form><div><label for="pg-n">Name</label><input class="pp3-in" id="pg-n" type="text" autocomplete="name"></div><div><label for="pg-e">Work email</label><input class="pp3-in" id="pg-e" type="email" autocomplete="email"></div><div><label for="pg-c">Company</label><input class="pp3-in" id="pg-c" type="text" autocomplete="organization"></div>
<p class="pp3-err" data-gate-err role="alert"></p><div><button type="submit" class="pp3-btn gold">Get the playbook</button></div></form>
<div class="pp3-thanks" data-gate-thanks hidden tabindex="-1" role="status"><h3>Thank you. Check your email.</h3><p data-gate-msg></p><button type="button" class="pp3-btn ghost" data-gate-reset>Use a different email</button></div>
<p class="pp3-note"><b>Preview only.</b> Nothing is sent. On the live site the form would go to DMP and the playbook would arrive by email. Gate fields and consent wording are to be confirmed.</p></div></div></div></section>
<section class="q-section q-bg-alt"><div class="pp3-wrap">{_hd({"eyebrow": "What is inside", "heading": s["inside_heading"], "intro": s["inside_intro"]}, ctx)}<ol class="pp3-inside">{ch}</ol></div></section>
<section class="q-section"><div class="pp3-wrap">{_hd({"eyebrow": "After you submit", "heading": "The delivery email", "intro": "A mock of the email the gate would send. Submit the form above and this one lights up."}, ctx)}
<div class="pp3-mail" data-gate-mail><div class="bar"><i></i><i></i><i></i><span>Mock email</span></div><dl><dt>From</dt><dd>DMP (sender to be confirmed)</dd><dt>To</dt><dd data-gate-to>your work email</dd><dt>Subject</dt><dd>Your dealer playbook (title to be confirmed)</dd></dl>
<div class="body"><p>Hello,</p><p>Here is the dealer playbook you asked for. The link below opens the download.</p><p><span class="pp3-btn gold" aria-disabled="true">Download the playbook (link to be supplied)</span></p><p>Questions about your dealer account? Inside Sales is {E(ctx["brand"]["phone"])}, 8 a.m. to 5 p.m. Central.</p></div></div></div></section>'''


def _nf(s, ctx):
    E, L = ctx["E"], ctx["L"]
    links = "".join(f'<li><a href="{E(L(h))}">{E(t)}</a></li>' for t, h in s["links"])
    b = ctx["brand"]
    return f'''{ctx["sec_open"](s)}<div class="pp3-wrap pp3-nf"><span class="num" aria-hidden="true"></span><h1 class="q-h1">{E(s["heading"])}</h1><p class="q-lead">{E(s["body"])}</p>
<div class="act"><button type="button" class="pp3-btn gold" data-pv-search>Search the site</button><a class="pp3-btn ghost" href="{E(L("index.html"))}">Go to the home page</a></div>
<ul>{links}</ul><p class="ph">Prefer a person? Inside Sales is <a href="{E(L(b["phone_href"]))}">{E(b["phone"])}</a>, 8 a.m. to 5 p.m. Central.</p></div></section>'''


RENDER_POP3 = {"p3assess": _assess, "p3calc": _calc, "p3tiles": _tiles, "p3stories": _stories, "p3story": _story, "p3gate": _gate, "p3nf": _nf}


# ----------------------------------------------------------------------------- JS

POP3_JS = r"""
(function(){
var d=document,RM=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
function $(s,r){return (r||d).querySelector(s)}
function mk(t,c,h){var e=d.createElement(t);if(c)e.className=c;if(h!=null)e.innerHTML=h;return e}
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}

/* ---------- assessment ---------- */
var as=$('[data-pp3-assess]');
if(as){try{(function(){
var cfg=JSON.parse($('script[type="application/json"]',as).textContent),Q=cfg.questions,A=cfg.areas,n=Q.length,i=0,ans=[];
var js=$('.pp3-as-js',as),nojs=$('.pp3-as-nojs',as);js.hidden=false;nojs.hidden=true;
var step=$('.pp3-step',as),res=$('.pp3-res',as),bar=$('.pp3-prog i',as),pb=$('.pp3-prog',as),ptxt=$('.pp3-ptxt',as),ppct=$('.pp3-ppct',as),qa=$('.pp3-qarea',as),qt=$('.pp3-qtext',as),hint=$('.pp3-hint',as),back=$('.pp3-back',step),opts=[].slice.call(step.querySelectorAll('.pp3-opt'));
function show(foc){
 qa.textContent=A[Q[i].area].title;qt.textContent=Q[i].q;hint.textContent=Q[i].hint;
 ptxt.textContent='Question '+(i+1)+' of '+n;var done=Math.round(i/n*100);ppct.textContent=done+'% done';bar.style.width=(i/n*100)+'%';pb.setAttribute('aria-valuenow',i);
 opts.forEach(function(o){o.setAttribute('aria-pressed',String(ans[i]!=null&&String(ans[i])===o.getAttribute('data-v')))});
 back.disabled=i===0;if(foc)qt.focus();
}
opts.forEach(function(o){o.addEventListener('click',function(){ans[i]=+o.getAttribute('data-v');
 opts.forEach(function(x){x.setAttribute('aria-pressed',String(x===o))});
 if(i<n-1){i++;show(true)}else{bar.style.width='100%';results()}})});
back.addEventListener('click',function(){if(i>0){i--;show(true)}});
function results(){
 step.hidden=true;res.hidden=false;
 var tot=0,per={};Q.forEach(function(q,k){tot+=ans[k];var p=per[q.area]||(per[q.area]={s:0,m:0});p.s+=ans[k];p.m+=2});
 var pct=Math.round(tot/(2*n)*100);
 var band=pct>=75?'Broad coverage':pct>=40?'Some gaps worth a look':'Plenty of room to look';
 $('.pp3-rt',res).textContent=band;
 $('.pp3-rp',res).textContent='You answered yes to '+ans.filter(function(a){return a===2}).length+' of '+n+' questions, not sure to '+ans.filter(function(a){return a===1}).length+' and no to '+ans.filter(function(a){return a===0}).length+'. The three areas below scored lowest, so they are the best places to start.';
 var keys=Object.keys(A);keys.sort(function(a,b){var x=per[a]?per[a].s/per[a].m:2,y=per[b]?per[b].s/per[b].m:2;return x-y});
 $('.pp3-areas',res).innerHTML=Object.keys(per).map(function(k){var v=Math.round(per[k].s/per[k].m*100);return '<li><span>'+esc(A[k].title)+'</span><span class="bar"><i style="width:'+v+'%"></i></span><span class="v">'+v+'%</span></li>'}).join('');
 $('.pp3-recs',res).innerHTML=keys.filter(function(k){return per[k]}).slice(0,3).map(function(k,j){var a=A[k];return '<li class="pp3-rec"><span class="n" aria-hidden="true">'+(j+1)+'</span><h4>'+esc(a.title)+'</h4><p>'+esc(a.text)+'</p><span class="links">'+a.links.map(function(l){return '<a href="'+esc(l[1])+'">'+esc(l[0])+'</a>'}).join('')+'</span></li>'}).join('');
 var c=$('.pp3-ring-c',res),pe=$('.pp3-pct',res),C=540.35;
 if(RM){c.style.strokeDashoffset=String(C*(1-pct/100));pe.textContent=pct+'%'}
 else{c.getBoundingClientRect();c.style.strokeDashoffset=String(C*(1-pct/100));var t0=null;(function f(t){if(t0==null)t0=t;var p=Math.min(1,(t-t0)/1000);pe.textContent=Math.round(pct*(1-Math.pow(1-p,3)))+'%';if(p<1)requestAnimationFrame(f)})(performance.now())}
 var rt=$('.pp3-rt',res);rt.focus();res.scrollIntoView({block:'nearest'});
}
function back2(){res.hidden=true;step.hidden=false;show(true)}
$('.pp3-redo',res).addEventListener('click',function(){ans=[];i=0;$('.pp3-ring-c',res).style.strokeDashoffset='540.35';back2()});
$('.pp3-edit',res).addEventListener('click',function(){i=n-1;back2()});
show(false);
})()}catch(e){}}

/* ---------- estimator ---------- */
var cc=$('[data-pp3-calc]');
if(cc){(function(){
var f={calls:$('#pc-calls'),cost:$('#pc-cost'),share:$('#pc-share'),rate:$('#pc-rate'),hrs:$('#pc-hrs')};
var out={empty:$('[data-empty]',cc),res:$('[data-result]',cc),month:$('[data-month]',cc),year:$('[data-year]',cc),rc:$('[data-rc]',cc),cc:$('[data-cc]',cc),hf:$('[data-hf]',cc),tc:$('[data-tc]',cc)};
var shown={month:0,year:0},last=null;
function num(v){v=String(v).replace(/[$,%\s]/g,'');if(v==='')return null;var x=Number(v);return isFinite(x)?x:NaN}
var usd=function(x){return '$'+Math.round(x).toLocaleString('en-US')};
function setErr(k,m){var e=$('#pc-'+k+'-e');e.textContent=m||'';f[k].setAttribute('aria-invalid',m?'true':'false')}
function anim(el,key,to,fmt){var from=shown[key];shown[key]=to;if(RM||from===to){el.textContent=fmt(to);return}
 var t0=null;(function s(t){if(t0==null)t0=t;var p=Math.min(1,(t-t0)/700),e=1-Math.pow(1-p,3);el.textContent=fmt(from+(to-from)*e);if(p<1&&shown[key]===to)requestAnimationFrame(s);else if(shown[key]===to)el.textContent=fmt(to)})(performance.now())}
function calc(){
 var v={},bad=false;
 ['calls','cost','share','rate','hrs'].forEach(function(k){var x=num(f[k].value);v[k]=x;var m='';if(x!==null&&(isNaN(x)||x<0))m='Enter a number, zero or more.';else if(k==='share'&&x!==null&&x>100)m='Enter a percent from 0 to 100.';setErr(k,m);if(m)bad=true});
 var hasCost=(v.cost||0)>0||((v.rate||0)>0&&(v.hrs||0)>0);
 if(bad||v.calls===null||v.share===null||!hasCost){out.res.hidden=true;out.empty.hidden=false;last=null;shown.month=0;shown.year=0;return}
 var rc=v.calls*v.share/100,cs=rc*(v.cost||0),hf=rc*(v.hrs||0),tc=hf*(v.rate||0),m=cs+tc;
 out.empty.hidden=true;out.res.hidden=false;
 anim(out.month,'month',m,usd);anim(out.year,'year',m*12,usd);
 out.rc.textContent=(Math.round(rc*10)/10).toLocaleString('en-US');out.cc.textContent=usd(cs);out.hf.textContent=(Math.round(hf*10)/10).toLocaleString('en-US');out.tc.textContent=usd(tc);
 last={v:v,rc:rc,cs:cs,hf:hf,tc:tc,m:m};
}
Object.keys(f).forEach(function(k){f[k].addEventListener('input',calc)});
var cb=$('[data-copy]',cc),cm=$('[data-copied]',cc);
cb.addEventListener('click',function(){if(!last)return;var v=last.v;
 var t=['Service-call savings estimate (my own numbers)','Service calls per month: '+v.calls,'Average cost per call: '+usd(v.cost||0),'Share handled remotely: '+v.share+'%','Technician hourly cost: '+usd(v.rate||0),'Technician hours per call: '+(v.hrs||0),'',
 'Calls handled remotely per month: '+(Math.round(last.rc*10)/10),'Estimated monthly savings: '+usd(last.m),'Estimated yearly savings: '+usd(last.m*12),'',
 'Formula: calls x share x (cost per call + hours per call x hourly cost); yearly = monthly x 12.','Your numbers, your math. Not a DMP guarantee.'].join('\n');
 function ok(){cm.textContent='Copied to your clipboard.'}
 function fb(){var ta=d.createElement('textarea');ta.value=t;ta.setAttribute('readonly','');ta.style.cssText='position:fixed;left:-9999px';d.body.appendChild(ta);ta.select();try{d.execCommand('copy')?ok():cm.textContent='Select and copy the numbers above.'}catch(e){cm.textContent='Select and copy the numbers above.'}ta.remove()}
 if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(ok,fb)}else fb();
});
})()}

/* ---------- gate ---------- */
var g=$('[data-pp3-gate]');
if(g){(function(){
var form=$('[data-gate-form]',g),th=$('[data-gate-thanks]',g),er=$('[data-gate-err]',g),mail=d.querySelector('[data-gate-mail]'),to=d.querySelector('[data-gate-to]');
form.addEventListener('submit',function(e){e.preventDefault();var n=$('#pg-n').value.trim(),m=$('#pg-e').value.trim();
 if(!n||!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(m)){er.textContent='Please add your name and a valid work email.';(n?$('#pg-e'):$('#pg-n')).focus();return}
 er.textContent='';form.hidden=true;th.hidden=false;$('[data-gate-msg]',g).textContent='Preview only: nothing was sent. On the live site the playbook would be emailed to '+m+'. The mock email further down shows what it would look like.';
 if(to)to.textContent=m;if(mail)mail.classList.add('sent');th.focus()});
$('[data-gate-reset]',g).addEventListener('click',function(){th.hidden=true;form.hidden=false;if(mail)mail.classList.remove('sent');if(to)to.textContent='your work email';$('#pg-e').focus()});
})()}

/* ---------- consent banner (preview) ---------- */
(function(){
if(top!==self)return;var KEY='pp3-consent',v=null;
try{v=localStorage.getItem(KEY)}catch(e){}
if(v)return;
var b=mk('div','pp3-cc');b.setAttribute('role','region');b.setAttribute('aria-label','Cookie consent (preview)');
b.innerHTML='<p class="pre">Preview of the consent banner; the live site uses HubSpot’s consent tool.</p><h2>Cookies on this site</h2><p class="txt">Essential cookies keep the site working. Optional analytics and marketing cookies are only used if you allow them. Wording to be confirmed.</p><div class="pp3-prefs" hidden><fieldset><legend class="sr-only" style="position:absolute;left:-9999px">Cookie preferences</legend><label><input type="checkbox" checked disabled> Essential, always on</label><label><input type="checkbox" data-k="analytics"> Analytics</label><label><input type="checkbox" data-k="marketing"> Marketing</label></fieldset><div class="row"><button type="button" class="pri" data-a="save">Save preferences</button></div></div><div class="row pp3-main"><button type="button" class="pri" data-a="all">Accept all</button><button type="button" data-a="none">Reject non-essential</button><button type="button" data-a="prefs" aria-expanded="false">Preferences</button></div>';
function done(c){var o={v:1,choice:c.choice,analytics:!!c.analytics,marketing:!!c.marketing};try{localStorage.setItem(KEY,JSON.stringify(o))}catch(e){}b.remove()}
b.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('button[data-a]');if(!a)return;var k=a.getAttribute('data-a');
 if(k==='all')done({choice:'all',analytics:1,marketing:1});
 else if(k==='none')done({choice:'essential'});
 else if(k==='prefs'){var p=$('.pp3-prefs',b);p.hidden=!p.hidden;a.setAttribute('aria-expanded',String(!p.hidden));b.classList.toggle('open',!p.hidden);if(!p.hidden)$('input[data-k]',b).focus()}
 else if(k==='save')done({choice:'custom',analytics:$('input[data-k=analytics]',b).checked,marketing:$('input[data-k=marketing]',b).checked})});
d.body.appendChild(b);
})();
})();
"""
