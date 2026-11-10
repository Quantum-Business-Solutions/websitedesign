"""Round 2b tools for the DMP preview: the system configurator, the playable keypad page, the keypad-style 404 and the
printable spec sheet. Everything is gated on the DMP content slug; the section types are only named by brands/dmp_tools.py.

  RENDER_TOOLS      tkcfg (configurator), tkplay (playable keypad), tknf (404)
  post(doc, ...)    runs after preview_panel.post: adds the tools CSS and JS to the pages that use them, and the print
                    stylesheet plus a "Print this spec sheet" button to product pages

The keypad reuses the hero keypad's parts from preview_panel.py (the shield, the sound icon, the zone colours, the blue
screen) but keeps its state on the component, so it works in all three directions; in Showcase it also drives the page
state (data-pn) the way the home keypad does.
No em or en dashes, nothing under 13px, 44px tap targets, prefers-reduced-motion respected, usable without JavaScript.
Set TK_OFF=1 to switch the pass off.
"""
from __future__ import annotations

import json
import os
import re

import preview_panel
from preview_panel import SHIELD, SND_SVG, _keep

SLUG = "digital-monitoring-products"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "brands", SLUG + ".assets")
JS_FLAG = '<script>document.documentElement.classList.add("tk-js")</script>'


def _thumb(path: str) -> str:
    """The 600px cutout when the assets folder has one (the list shows fifty thumbnails)."""
    if path.endswith(".png"):
        small = path[:-4] + "-600.png"
        if os.path.exists(os.path.join(ASSETS, small.replace("assets/", "", 1))):
            return small
    return path


def _head(s, E, RAW=None):
    return (f'<div class="tk-head"><div class="q-eyebrow">{E(s.get("eyebrow", ""))}</div>'
            f'<h1 class="q-h1">{E(s["heading"])}</h1><p class="q-lead">{E(s.get("subhead", ""))}</p></div>')


# ------------------------------------------------------------------------------------------------ configurator

def _cfg(s, ctx):
    E, L, rel = ctx["E"], ctx["L"], ctx["rel"]
    systems, addons = s["systems"], s.get("addons", [])
    label = {k: lab for k, lab, _c, _h in systems + addons}
    colour = {k: c for k, _lab, c, _h in systems + addons}

    def opt(k, lab, c, _h):
        return (f'<label class="tk-sys" style="--zc:{c}"><input type="checkbox" name="sys" value="{E(k)}">'
                f'<span class="tk-sys-b"><i aria-hidden="true"></i>{E(lab)}</span></label>')
    pick = (f'<form class="tk-pick tk-js-only" data-tk-pick onsubmit="return false">'
            f'<fieldset><legend><b>1</b> System types</legend><div class="tk-opts">{"".join(opt(*x) for x in systems)}</div></fieldset>'
            + (f'<fieldset><legend>Optional</legend><div class="tk-opts">{"".join(opt(*x) for x in addons)}</div></fieldset>' if addons else "")
            + '<button type="button" class="tk-btn tk-reset" data-tk-reset>Clear</button></form>')

    groups = ""
    idx = 0
    for kind in s["type_order"]:
        items = [p for p in s["products"] if p["kind"] == kind]
        if not items:
            continue
        lis = ""
        for p in items:
            tags = "".join(f'<span class="tk-tag" style="--zc:{colour.get(n, "#8a8f98")}"><i aria-hidden="true"></i>{E(label.get(n, n))}</span>' for n in p["needs"])
            chips = "".join(f"<div><dt>{E(k)}</dt><dd>{E(v)}</dd></div>" for k, v in p.get("chips", []))
            chips = f'<dl class="tk-chips">{chips}</dl>' if chips else ""
            if kind == "panels":
                fit = ""
            elif p.get("fit"):
                fit = f'<p class="tk-fit"><b>Stated fit:</b> {E(p["fit"])}</p>'
            else:
                fit = '<p class="tk-fit tk-ask"><b>Panel fit:</b> ask your DMP dealer</p>'
            soon = '<span class="tk-soon">Coming soon, not orderable</span>' if p.get("soon") else ""
            name = re.sub(r"\s*\(coming soon\)", "", p["name"])
            img = (f'<img src="{E(rel(_thumb(p["img"])))}" alt="" width="120" height="90" loading="lazy" decoding="async">' if p.get("img") else "")
            lis += (f'<li class="tk-p" data-tk-p data-i="{idx}" data-kind="{E(kind)}" data-needs="{E(" ".join(p["needs"]))}" data-name="{E(name)}" data-fit="{E(p.get("fit", ""))}" data-soon="{1 if p.get("soon") else 0}">'
                    f'<div class="tk-p-img">{img}</div>'
                    f'<div class="tk-p-b"><h4><a href="{E(L(p["href"]))}">{E(name)}</a>{soon}</h4><p class="tk-p-t">{E(p["blurb"])}</p>'
                    f'<p class="tk-tags"><span class="tk-tags-k">Listed under</span>{tags}</p>{chips}{fit}</div>'
                    f'<label class="tk-add tk-js-only"><input type="checkbox" data-tk-add><span>Add to summary</span></label></li>')
            idx += 1
        groups += (f'<section class="tk-grp" data-tk-grp aria-labelledby="tk-g-{E(kind)}"><h3 id="tk-g-{E(kind)}">{E(s["types"].get(kind, kind))} <span data-tk-n>{len(items)}</span></h3>'
                   f'<ul class="tk-list">{lis}</ul></section>')

    src = " and ".join(f'<a href="{E(L(h))}">{E(t)}</a>' for t, h in s.get("sources", []))
    disc = E(s["disclaimer"])
    out = f'''<section class="q-section tk-cfg" id="{E(s.get("id", "configure"))}">{JS_FLAG}
<div class="q-container">
{_head(s, E)}
<p class="tk-disc" role="note"><b>{disc}</b> It repeats what this site says about each product. A DMP dealer confirms the design.</p>
{pick}
<noscript><p class="tk-nojs">Without JavaScript the full list is shown. Every product, the systems it is listed under and its stated fit are below.</p></noscript>
<div class="tk-cols">
<div class="tk-res">
<div class="tk-cover tk-js-only" data-tk-cover role="status" aria-live="polite"></div>
<h2 class="tk-h2"><b>2</b> Products listed under your systems</h2>
<p class="tk-count" data-tk-count>All {len(s["products"])} products on this site, by type.</p>
{groups}
<p class="tk-src">Source: the product finder and product pages on this site ({src}). A product with no stated panel fit reads "ask your DMP dealer".</p>
</div>
<aside class="tk-sum tk-js-only" id="summary" aria-labelledby="tk-sum-h">
<h2 class="tk-h2" id="tk-sum-h"><b>3</b> Your summary</h2>
<p class="tk-sum-disc"><b>{disc}</b> No prices, no quantities.</p>
<div data-tk-sum><p class="tk-sum-empty">Pick system types, then tick Add to summary on the products you want.</p></div>
<p class="tk-sum-foot">Take this list to a DMP dealer, who confirms what fits the building. Specifications as listed on this site.</p>
<div class="tk-sum-act"><button type="button" class="tk-btn gold" data-tk-print>Print summary</button><a class="tk-btn" href="{E(L("find-a-dealer.html"))}">Find a dealer</a></div>
</aside>
</div>
</div></section>'''
    return _keep(out)


# ------------------------------------------------------------------------------------------------ playable keypad

def _play(s, ctx):
    E, rel = ctx["E"], ctx["rel"]
    logo = rel("assets/dmp-logo-light.svg")
    zl = "".join(f'<li data-z="{n}" style="--zc:{c}"><i aria-hidden="true"></i><b>Z{n}</b><span>{E(name)}</span><em data-tk-zs>Secure</em></li>' for n, name, c in s["zones"])
    zc = "".join(f'<div class="tk-z" data-z="{n}" data-name="{E(name)}" style="--zc:{c}" role="group" aria-label="Zone {n}, {E(name)}">'
                 f'<span class="tk-z-n"><i aria-hidden="true"></i><b>Z{n}</b> {E(name)}</span><em data-tk-zs>Secure</em>'
                 f'<button type="button" class="tk-btn" data-tk-trip aria-pressed="false">Trip</button>'
                 f'<button type="button" class="tk-btn" data-tk-byp aria-pressed="false">Bypass</button></div>' for n, name, c in s["zones"])
    keys = "".join(f'<button type="button" class="tk-key" data-tk-d="{d}">{d}</button>' for d in "123456789")
    keys += '<button type="button" class="tk-key tk-key-w" data-tk-clr>Clear</button><button type="button" class="tk-key" data-tk-d="0">0</button><span class="tk-key-x" aria-hidden="true"></span>'
    rules = "".join(f"<div><dt>{E(k)}</dt><dd>{E(v)}</dd></div>" for k, v in s.get("rules", []))
    n = len(s["zones"])
    out = f'''<section class="q-section tk-play" id="{E(s.get("id", "keypad"))}">{JS_FLAG}
<div class="q-container">
{_head(s, E)}
<div class="tk-stage" id="tk-kp" data-tk="armed">
<div class="tk-dev">
<div class="tk-kp"><div class="tk-case"><i class="tk-led" aria-hidden="true"></i>
<div class="tk-glass"><div class="tk-screen">
<div class="tk-bar"><img class="tk-logo" src="{E(logo)}" alt="" width="100" height="37"><span class="tk-clock" aria-hidden="true"><span data-tk-day>TUE</span> <span data-tk-time>5:35 PM</span></span></div>
<div class="tk-core">
<button class="tk-shield" type="button" data-tk-shield aria-label="Site armed. Key in any four digits to disarm">{SHIELD}</button>
<p class="tk-state" data-tk-label aria-hidden="true">ARMED</p>
<p class="tk-code" data-tk-code aria-hidden="true"><i></i><i></i><i></i><i></i></p>
</div>
<ul class="tk-zl" aria-hidden="true">{zl}</ul>
<p class="tk-logline" aria-hidden="true"><span>Event</span> <b data-tk-logline>All zones armed. Supervised.</b></p>
</div></div></div></div>
<p class="tk-hint" role="status" aria-live="polite" data-tk-hint>Site armed. {n} demo zones supervised. Key in any four digits to disarm.</p>
<p class="tk-demo">{E(s.get("demo", ""))}</p>
<noscript><p class="tk-nojs">The keypad needs JavaScript to play. Without it this page shows the keypad at rest, and the rules below describe what it does.</p></noscript>
</div>
<div class="tk-side tk-js-only">
<div class="tk-ctl" role="group" aria-label="Keypad controls">
<button type="button" class="tk-btn gold" data-tk-arm disabled>Arm</button>
<button type="button" class="tk-btn tk-snd" data-tk-sound aria-pressed="false">{SND_SVG}<span data-tk-sndtxt>Sound off</span></button>
</div>
<div class="tk-pad" role="group" aria-label="Number pad. Key in any four digits to disarm"><p class="tk-pad-h">Number pad <span>any four digits disarm</span></p><div class="tk-keys">{keys}</div></div>
<div class="tk-zones" role="group" aria-label="Demo zones"><p class="tk-pad-h">Demo zones <span>trip one and see</span></p>{zc}</div>
</div>
<div class="tk-log tk-js-only"><div class="tk-log-h"><h2 class="tk-h2">Event log</h2><button type="button" class="tk-btn" data-tk-clear>Clear log</button></div>
<ol data-tk-list aria-label="Events, newest first"><li><b>00:00:00</b><span>System armed</span></li></ol></div>
<div class="tk-rules"><h2 class="tk-h2">How the demo behaves</h2><dl>{rules}</dl></div>
</div>
</div></section>'''
    return _keep(out)


# ------------------------------------------------------------------------------------------------ 404

def _nf(s, ctx):
    E, L, rel = ctx["E"], ctx["L"], ctx["rel"]
    b = ctx["brand"]
    links = "".join(f'<li><a href="{E(L(h))}">{E(t)}</a></li>' for t, h in s["links"])
    lcd = s.get("lcd") or ["ZONE 404", "PAGE NOT FOUND"]
    lines = "".join(f'<p>{"" if i == 0 else "&gt; "}{E(x)}{"<i></i>" if i == len(lcd) - 1 else ""}</p>' for i, x in enumerate(lcd))
    out = f'''<section class="q-section tk-nf">{JS_FLAG}<div class="q-container tk-nf-in">
<div class="tk-nf-dev" aria-hidden="true"><div class="tk-kp"><div class="tk-case"><i class="tk-led"></i><div class="tk-glass"><div class="tk-screen tk-nf-screen">
<div class="tk-bar"><img class="tk-logo" src="{E(rel("assets/dmp-logo-light.svg"))}" alt="" width="100" height="37"><span class="tk-clock">TROUBLE</span></div>
<p class="tk-nf-num">404</p><div class="tk-nf-lcd">{lines}</div>
<p class="tk-logline"><span>Event</span> <b>Zone 404 not found. No alarm.</b></p>
</div></div></div></div></div>
<div class="tk-nf-copy"><div class="q-eyebrow">Zone 404, not found</div>
<h1 class="q-h1">{E(s["heading"])}</h1><p class="q-lead">{E(s["body"])}</p>
<div class="tk-act"><button type="button" class="tk-btn gold tk-js-only" data-pv-search>Search the site</button><a class="tk-btn" href="{E(L("index.html"))}">Go to the home page</a><a class="tk-btn" href="{E(L("keypad-demo.html"))}">Play with the keypad</a></div>
<ul class="tk-nf-links">{links}</ul>
<p class="tk-ph">Prefer a person? Inside Sales is <a href="{E(L(b["phone_href"]))}">{E(b["phone"])}</a>, 8 a.m. to 5 p.m. Central.</p></div>
</div></section>'''
    return _keep(out)


RENDER_TOOLS = {"tkcfg": _cfg, "tkplay": _play, "tknf": _nf}


# ------------------------------------------------------------------------------------------------ CSS

TOOLS_CSS = r"""
/* ===== tools pass (scripts/preview_tools.py): shared ===== */
.tk-cfg,.tk-play,.tk-nf{--tk-line:color-mix(in srgb,var(--fg) 22%,var(--bg));--tk-soft:color-mix(in srgb,var(--fg) 6%,var(--bg));--tk-r:10px;--tk-mono:'JetBrains Mono',ui-monospace,'SFMono-Regular',Menlo,Consolas,'Liberation Mono',monospace}
html[data-dir="showcase"] :is(.tk-cfg,.tk-play,.tk-nf){--tk-r:2px}
html[data-dir="clean"] :is(.tk-cfg,.tk-play,.tk-nf){--tk-r:4px}
html:not(.tk-js) .tk-js-only{display:none!important}
.tk-head{max-width:820px;margin:0 0 clamp(22px,3vw,36px)}
.tk-head .q-h1{margin:18px 0 0;font-size:clamp(38px,5.4vw,76px)}
.tk-head .q-lead{margin:16px 0 0;max-width:680px}
.tk-h2{font:800 clamp(20px,2vw,26px)/1.15 var(--q-sans,inherit);letter-spacing:-.01em;color:var(--fg);margin:0;display:flex;align-items:center;gap:12px}
html[data-dir="showcase"] .tk-h2{font-family:var(--pn-disp);text-transform:uppercase;letter-spacing:.01em;font-size:clamp(24px,2.3vw,32px)}
html[data-dir="press"] .tk-h2{font-family:'Playfair Display','Playfair Fallback',Georgia,serif;font-weight:700}
.tk-h2 b,.tk-pick legend b{display:inline-grid;place-items:center;width:30px;height:30px;border-radius:50%;background:var(--q-gold);color:#111;font:800 15px/1 var(--tk-mono)}
.tk-btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:44px;padding:0 18px;border-radius:var(--tk-r);border:1.5px solid var(--tk-line);background:transparent;color:var(--fg);font:700 14px/1 var(--q-sans,inherit);text-decoration:none;cursor:pointer;transition:border-color .2s,background .2s,transform .2s}
.tk-btn:hover{border-color:var(--fg)}
.tk-btn.gold{background:var(--q-gold);border-color:var(--q-gold);color:#111}
.tk-btn.gold:hover{transform:translateY(-1px)}
.tk-btn[disabled]{opacity:.5;cursor:not-allowed;transform:none}
.tk-btn[aria-pressed="true"]{background:var(--fg);border-color:var(--fg);color:var(--bg)}
html[data-dir="showcase"] .tk-btn{font-family:var(--pn-mono);font-size:13px;letter-spacing:.08em;text-transform:uppercase}
:is(.tk-cfg,.tk-play,.tk-nf) :is(a,button,input,summary):focus-visible{outline:3px solid var(--fg);outline-offset:3px}
.tk-nojs{margin:16px 0;padding:14px 16px;border:1.5px solid var(--tk-line);border-radius:var(--tk-r);font-size:15px;color:var(--fg)}
@media(prefers-reduced-motion:reduce){:is(.tk-cfg,.tk-play,.tk-nf) *{transition:none!important;animation:none!important}}

/* ===== the keypad device (playable page and 404) ===== */
.tk-kp{container-type:inline-size;width:100%;max-width:760px;margin:0 auto}
.tk-case{position:relative;aspect-ratio:978/660;border-radius:5.4cqw;padding:6.4cqw 6.8cqw 7.2cqw;background:linear-gradient(160deg,#fdfdfd 0%,#eceef0 38%,#d3d6da 100%);
  box-shadow:inset 0 .35cqw .2cqw #fff,inset 0 -1cqw 1.4cqw rgba(60,66,80,.35),inset .5cqw 0 .9cqw rgba(255,255,255,.7),inset -.6cqw 0 1cqw rgba(60,66,80,.22),0 0 0 1px rgba(0,0,0,.45),0 3cqw 6cqw rgba(0,0,0,.35)}
.tk-led{position:absolute;left:50%;top:2.7cqw;width:2cqw;height:1cqw;margin-left:-1cqw;border-radius:1cqw;background:#ff3b30;box-shadow:0 0 1.2cqw #ff3b30}
[data-tk="disarmed"] .tk-led{background:#c9cdd3;box-shadow:inset 0 .15cqw .3cqw rgba(0,0,0,.35)}
[data-tk="arming"] .tk-led,[data-tk="alarm"] .tk-led{animation:tk-blink 1s steps(2) infinite}
@keyframes tk-blink{50%{background:#c9cdd3;box-shadow:none}}
.tk-glass{height:100%;border-radius:1.5cqw;background:#050608;padding:.9cqw;box-shadow:0 0 0 .25cqw rgba(0,0,0,.18),inset 0 0 0 1px #222}
.tk-screen{position:relative;height:100%;border-radius:.7cqw;overflow:hidden;font-family:var(--q-sans,system-ui,sans-serif);font-size:clamp(13px,2.15cqw,18px);color:#eaf3ff;display:grid;grid-template-columns:1fr 43%;grid-template-rows:auto 1fr auto;
  background:radial-gradient(90% 110% at 36% 50%,#1d63d4 0%,#0e41a8 34%,#082873 62%,#030f36 100%);transition:filter .5s,background .5s}
[data-tk="disarmed"] .tk-screen{filter:saturate(.72) brightness(.92)}
[data-tk="alarm"] .tk-screen{background:radial-gradient(90% 110% at 36% 50%,#d3352b 0%,#9c1d16 36%,#5a0d0a 66%,#2a0504 100%)}
.tk-bar{grid-column:1/-1;display:flex;justify-content:space-between;align-items:center;padding:2cqw 2.6cqw 0}
.tk-logo{width:10.5cqw!important;min-width:44px;height:auto}
.tk-clock{font-weight:600;font-size:max(13px,.86em);letter-spacing:.04em}
.tk-core{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:.6cqw;min-width:0}
.tk-shield{position:relative;width:22cqw;min-width:72px;padding:0;border:0;background:none;border-radius:50%;cursor:pointer;transition:transform .25s}
.tk-shield svg{width:100%;display:block;overflow:visible}
.tk-js .tk-shield:hover{transform:scale(1.03)}.tk-js .tk-shield:active{transform:scale(.96)}
.tk-play .tk-shield:focus-visible{outline:3px solid #ffd23d;outline-offset:2px}
.tk-kp .sh-ring-bg{fill:rgba(3,14,52,.35);stroke:rgba(170,210,255,.18);stroke-width:1}
.tk-kp .sh-ring{fill:none;stroke:#3ddc84;stroke-width:2.6;stroke-linecap:round;stroke-dasharray:100;stroke-dashoffset:0;transform:rotate(-90deg);transform-origin:80px 85px;opacity:.9}
.tk-kp .sh-outer{fill:url(#pnShF);stroke:url(#pnShG);stroke-width:5;stroke-linejoin:round;filter:drop-shadow(0 0 5px rgba(125,255,180,.95));transition:filter .5s,fill-opacity .4s}
.tk-kp .sh-trace{fill:none;stroke:#ffd23d;stroke-width:5;stroke-linejoin:round;stroke-linecap:round;stroke-dasharray:100;stroke-dashoffset:100;opacity:0}
.tk-kp .sh-inner{fill:rgba(9,60,150,.75);stroke:rgba(190,225,255,.7);stroke-width:1.6;stroke-linejoin:round}
.tk-kp .sh-shackle{fill:none;stroke:#eaf3ff;stroke-width:5;stroke-linecap:round;transform-origin:92px 80px;transition:transform .45s}
.tk-kp .sh-body{fill:#eaf3ff}.tk-kp .sh-key{fill:#0b3496}
[data-tk="disarmed"] .sh-outer{filter:drop-shadow(0 0 6px rgba(255,157,46,.75))}
[data-tk="disarmed"] .sh-ring{opacity:0}
[data-tk="disarmed"] .sh-ring-bg{stroke:rgba(255,157,46,.6)}
[data-tk="disarmed"] .sh-shackle{transform:translateY(-5px) rotate(28deg)}
[data-tk="arming"] .sh-outer{fill-opacity:.25;stroke-opacity:.25;filter:none}
[data-tk="arming"] .sh-trace{opacity:1;animation:tk-draw var(--tk-exit,3s) linear forwards}
[data-tk="arming"] .sh-ring{stroke:#ffd23d;stroke-dashoffset:100;animation:tk-draw var(--tk-exit,3s) linear forwards}
[data-tk="alarm"] .sh-outer{filter:drop-shadow(0 0 8px rgba(255,255,255,.9))}
[data-tk="alarm"] .sh-ring{stroke:#fff}
@keyframes tk-draw{to{stroke-dashoffset:0}}
.tk-state{margin:0;font-weight:700;font-size:1.5em;line-height:1;letter-spacing:.07em;color:#eaf3ff;white-space:nowrap}
[data-tk="disarmed"] .tk-state{color:#ffc37a}[data-tk="arming"] .tk-state{color:#ffd23d}[data-tk="alarm"] .tk-state{color:#fff}
.tk-code{margin:.4cqw 0 0;display:flex;gap:1.2cqw}
.tk-code i{width:max(9px,1.5cqw);height:max(9px,1.5cqw);border-radius:50%;box-shadow:inset 0 0 0 1.5px rgba(234,243,255,.75)}
.tk-code i.on{background:#eaf3ff}
.tk-zl{list-style:none;margin:0;padding:0 2.4cqw 0 0;display:flex;flex-direction:column;justify-content:center;gap:.5cqw;min-width:0}
.tk-zl li{display:flex;align-items:center;gap:1.1cqw;padding:.7cqw 1.2cqw;border-radius:.8cqw;background:rgba(1,6,26,.34);font-size:max(13px,.8em);line-height:1.2;white-space:nowrap;min-width:0}
.tk-zl i,.tk-z-n i{flex:none;width:9px;height:9px;border-radius:50%;background:var(--zc);box-shadow:0 0 8px var(--zc)}
.tk-zl b{font-weight:700}.tk-zl span{overflow:hidden;text-overflow:ellipsis;min-width:0}
.tk-zl em{margin-left:auto;font-style:normal;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#7dffb4}
.tk-zl li[data-s="open"] em{color:#ffc37a}.tk-zl li[data-s="bypassed"] em{color:#cfd6e4}.tk-zl li[data-s="alarm"] em{color:#fff}
.tk-zl li[data-s="alarm"]{background:rgba(255,255,255,.22)}
.tk-zl li[data-s="bypassed"] i{background:#59606c;box-shadow:none}
.tk-logline{grid-column:1/-1;margin:0;display:flex;gap:1.4cqw;align-items:center;padding:1.1cqw 2.6cqw 1.3cqw;font:500 13px/1.2 var(--tk-mono);letter-spacing:.04em;text-transform:uppercase;background:rgba(1,6,26,.62);border-top:1px solid rgba(160,205,255,.2);white-space:nowrap;overflow:hidden}
.tk-logline span{color:#b9d2f7}.tk-logline b{font-weight:600;color:#fff;overflow:hidden;text-overflow:ellipsis}
@container (max-width:520px){
  .tk-case{aspect-ratio:10/9;padding:7.5cqw 5.5cqw 7.5cqw}
  .tk-screen{grid-template-columns:1fr 46%}
  .tk-zl span{display:none}
  .tk-zl{padding-right:2cqw;gap:1cqw}.tk-zl li{padding:1.2cqw 1.6cqw;gap:1.6cqw}
  .tk-shield{width:30cqw}
  .tk-state{font-size:1.25em}
}

/* ===== playable keypad page ===== */
.tk-stage{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);gap:clamp(20px,3vw,44px);align-items:start}
.tk-dev{min-width:0}
.tk-hint{margin:18px 0 0;padding:12px 16px;border-left:4px solid var(--q-gold);background:var(--tk-soft);color:var(--fg);font:600 15px/1.45 var(--q-sans,inherit);min-height:46px}
[data-tk="alarm"] .tk-hint{border-left-color:#ff5a4d}
.tk-demo{margin:10px 0 0;font-size:14px;line-height:1.5;color:var(--fg-muted)}
.tk-side{display:grid;gap:18px;min-width:0}
.tk-ctl{display:flex;flex-wrap:wrap;gap:10px}
.tk-ctl .tk-btn{flex:1 1 140px;min-height:48px}
.tk-snd .off{display:block}.tk-snd .on{display:none}
.tk-snd[aria-pressed="true"] .off{display:none}.tk-snd[aria-pressed="true"] .on{display:block}
.tk-pad,.tk-zones,.tk-log,.tk-rules{border:1.5px solid var(--tk-line);border-radius:var(--tk-r);padding:16px;background:var(--bg)}
.tk-pad-h{margin:0 0 12px;display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;font:700 13px/1.3 var(--tk-mono);letter-spacing:.08em;text-transform:uppercase;color:var(--fg)}
.tk-pad-h span{font-weight:500;color:var(--fg-muted);letter-spacing:.04em}
.tk-keys{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.tk-key{min-height:52px;border-radius:var(--tk-r);border:1.5px solid var(--tk-line);background:var(--tk-soft);color:var(--fg);font:700 20px/1 var(--tk-mono);cursor:pointer;transition:background .15s,transform .1s}
.tk-key:hover{border-color:var(--fg)}.tk-key:active{transform:scale(.96);background:var(--q-gold);color:#111}
.tk-key-w{font-size:14px;letter-spacing:.06em;text-transform:uppercase}
.tk-z{display:grid;grid-template-columns:minmax(0,1fr) auto auto auto;align-items:center;gap:8px;padding:8px 0;border-top:1px solid var(--tk-line)}
.tk-z:first-of-type{border-top:0;padding-top:0}
.tk-z-n{display:flex;align-items:center;gap:9px;font:600 15px/1.2 var(--q-sans,inherit);color:var(--fg);min-width:0}
.tk-z-n i{box-shadow:0 0 0 1.5px var(--fg)}
.tk-z em{font:700 13px/1 var(--tk-mono);font-style:normal;letter-spacing:.06em;text-transform:uppercase;color:var(--fg-muted);min-width:74px;text-align:right}
.tk-z[data-s="alarm"] em{color:var(--fg);text-decoration:underline;text-decoration-thickness:2px}
.tk-z .tk-btn{padding:0 12px;min-width:68px}
.tk-log{grid-column:1/2}
.tk-rules{grid-column:2/3}
.tk-log-h{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-bottom:12px}
.tk-log ol{list-style:none;margin:0;padding:0;max-height:300px;overflow:auto;font:500 14px/1.4 var(--tk-mono);color:var(--fg)}
.tk-log li{display:grid;grid-template-columns:78px 1fr;gap:10px;padding:7px 0;border-top:1px solid var(--tk-line)}
.tk-log li:first-child{border-top:0}
.tk-log li b{font-weight:600;color:var(--fg-muted)}
.tk-rules dl{margin:14px 0 0;display:grid;gap:12px}
.tk-rules dt{font:700 13px/1.3 var(--tk-mono);letter-spacing:.08em;text-transform:uppercase;color:var(--fg)}
.tk-rules dd{margin:4px 0 0;font-size:15px;line-height:1.55;color:var(--fg-muted)}
@media(max-width:900px){
  .tk-stage{grid-template-columns:minmax(0,1fr)}
  .tk-log,.tk-rules{grid-column:auto}
}
@media(max-width:420px){
  .tk-z{grid-template-columns:minmax(0,1fr) auto;row-gap:6px}
  .tk-z em{text-align:right}
  .tk-z .tk-btn{grid-row:2}
}

/* ===== 404 ===== */
.tk-nf-in{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,6fr);gap:clamp(24px,5vw,72px);align-items:center}
.tk-nf-dev .tk-kp{max-width:520px}
.tk-nf-screen{grid-template-columns:1fr!important;grid-template-rows:auto 1fr auto auto!important;background:radial-gradient(90% 110% at 50% 50%,#1d63d4 0%,#0e41a8 34%,#082873 62%,#030f36 100%)}
.tk-nf-num{margin:0;align-self:center;text-align:center;font:200 clamp(56px,26cqw,150px)/.9 var(--q-sans,system-ui,sans-serif);letter-spacing:-.04em;color:#eaf3ff;text-shadow:0 0 .4em rgba(255,157,46,.55)}
.tk-nf-lcd{padding:0 3cqw 2cqw;font:600 13px/1.5 var(--tk-mono);letter-spacing:.06em;color:#ffc37a;text-align:center}
.tk-nf-lcd p{margin:0}
.tk-nf-lcd i{display:inline-block;width:.6em;height:1em;margin-left:.3em;vertical-align:-.15em;background:#ffc37a;animation:tk-cur 1.1s steps(2) infinite}
@keyframes tk-cur{50%{opacity:0}}
.tk-nf .tk-led{background:#ff9d2e;box-shadow:0 0 1.2cqw #ff9d2e}
.tk-nf-copy .q-h1{margin:18px 0 0;font-size:clamp(36px,4.6vw,64px)}
.tk-nf-copy .q-lead{margin:16px 0 0}
.tk-act{display:flex;flex-wrap:wrap;gap:10px;margin:26px 0 0}
.tk-nf-links{list-style:none;margin:28px 0 0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 24px}
.tk-nf-links a{display:flex;align-items:center;min-height:44px;border-top:1px solid var(--tk-line);color:var(--fg);font-weight:600;text-decoration:none}
.tk-nf-links a:hover{text-decoration:underline;text-underline-offset:4px}
.tk-ph{margin:22px 0 0;font-size:15px;color:var(--fg-muted)}
.tk-ph a{color:var(--fg);font-weight:700;text-decoration:underline;text-underline-offset:3px;display:inline-flex;align-items:center;min-height:44px}
@media(max-width:820px){.tk-nf-in{grid-template-columns:minmax(0,1fr)}.tk-nf-dev .tk-kp{max-width:280px;margin:0}}

/* ===== configurator ===== */
.tk-disc{margin:0 0 22px;padding:14px 16px;border:1.5px solid var(--tk-line);border-left:6px solid var(--q-gold);border-radius:var(--tk-r);background:var(--tk-soft);font-size:15px;line-height:1.5;color:var(--fg)}
.tk-pick{display:flex;flex-wrap:wrap;align-items:flex-end;gap:18px 28px;padding:18px;border:1.5px solid var(--tk-line);border-radius:var(--tk-r);background:var(--bg);margin:0 0 28px}
.tk-pick fieldset{border:0;margin:0;padding:0;min-width:0}
.tk-pick legend{display:flex;align-items:center;gap:10px;padding:0;margin:0 0 12px;font:700 13px/1.2 var(--tk-mono);letter-spacing:.1em;text-transform:uppercase;color:var(--fg)}
.tk-opts{display:flex;flex-wrap:wrap;gap:8px}
.tk-sys{position:relative;display:inline-flex}
.tk-sys input{position:absolute;inset:0;width:100%;height:100%;margin:0;opacity:0;cursor:pointer}
.tk-sys-b{display:inline-flex;align-items:center;gap:10px;min-height:48px;padding:0 16px;border-radius:var(--tk-r);border:1.5px solid var(--tk-line);font:700 15px/1 var(--q-sans,inherit);color:var(--fg);background:var(--bg);transition:background .2s,border-color .2s}
.tk-sys-b i,.tk-tag i{flex:none;width:12px;height:12px;border-radius:50%;background:var(--zc);box-shadow:0 0 0 1.5px var(--fg)}
.tk-sys:hover .tk-sys-b{border-color:var(--fg)}
.tk-sys input:checked + .tk-sys-b{background:var(--fg);border-color:var(--fg);color:var(--bg)}
.tk-sys input:checked + .tk-sys-b i{box-shadow:0 0 0 1.5px var(--bg)}
.tk-sys input:focus-visible + .tk-sys-b{outline:3px solid var(--fg);outline-offset:3px}
.tk-reset{margin-left:auto}
.tk-cols{display:grid;grid-template-columns:minmax(0,1fr) minmax(300px,380px);gap:clamp(22px,3vw,44px);align-items:start}
.tk-res{min-width:0}
.tk-cover{margin:0 0 26px;padding:16px 18px;border-radius:var(--tk-r);border:1.5px solid var(--fg);background:var(--bg);font-size:15.5px;line-height:1.55;color:var(--fg)}
.tk-cover:empty{display:none}
.tk-cover p{margin:0}.tk-cover p+p{margin-top:8px}
.tk-cover a{color:var(--fg);font-weight:700;text-decoration:underline;text-underline-offset:3px}
.tk-count{margin:10px 0 0;font-size:15px;color:var(--fg-muted)}
.tk-grp{margin:26px 0 0}
.tk-grp[hidden],.tk-p[hidden]{display:none!important}
.tk-grp h3{margin:0 0 4px;display:flex;align-items:baseline;gap:10px;font:700 13px/1.3 var(--tk-mono);letter-spacing:.12em;text-transform:uppercase;color:var(--fg);padding-bottom:10px;border-bottom:2px solid var(--fg)}
.tk-grp h3 span{font-weight:500;color:var(--fg-muted)}
.tk-list{list-style:none;margin:0;padding:0}
.tk-p{display:grid;grid-template-columns:96px minmax(0,1fr) auto;gap:16px;align-items:start;padding:16px 0;border-bottom:1px solid var(--tk-line)}
.tk-p-img{width:96px;aspect-ratio:4/3;border-radius:var(--tk-r);background:#f1f1ee;display:grid;place-items:center;overflow:hidden}
.tk-p-img img{width:100%;height:100%;object-fit:contain;padding:6px}
.tk-p h4{margin:0;font:700 17px/1.3 var(--q-sans,inherit);color:var(--fg);display:flex;flex-wrap:wrap;align-items:center;gap:6px 10px}
.tk-p h4 a{display:inline-flex;align-items:center;min-height:44px;color:inherit;text-decoration:underline;text-decoration-color:var(--tk-line);text-underline-offset:4px}
.tk-p h4 a:hover{text-decoration-color:var(--fg)}
.tk-soon{display:inline-flex;align-items:center;min-height:24px;padding:0 10px;border-radius:999px;border:1.5px solid var(--fg);font:700 13px/1 var(--q-sans,inherit);letter-spacing:.02em;color:var(--fg)}
.tk-p-t{margin:6px 0 0;font-size:15px;line-height:1.5;color:var(--fg-muted)}
.tk-tags{margin:10px 0 0;display:flex;flex-wrap:wrap;align-items:center;gap:6px 8px;font-size:13px;color:var(--fg)}
.tk-tags-k{font:600 13px/1 var(--tk-mono);letter-spacing:.06em;text-transform:uppercase;color:var(--fg-muted);margin-right:2px}
.tk-tag{display:inline-flex;align-items:center;gap:7px;min-height:26px;padding:0 10px;border-radius:999px;border:1px solid var(--tk-line);font-weight:600}
.tk-tag i{width:9px;height:9px}
.tk-tag.is-on{border-color:var(--fg);background:var(--tk-soft)}
.tk-chips{margin:10px 0 0;display:flex;flex-wrap:wrap;gap:4px 18px;font-size:13.5px;color:var(--fg)}
.tk-chips div{display:flex;gap:6px}.tk-chips dt{color:var(--fg-muted)}.tk-chips dd{margin:0;font-weight:700;font-variant-numeric:tabular-nums}
.tk-fit{margin:10px 0 0;font-size:14px;line-height:1.45;color:var(--fg)}
.tk-fit.tk-ask{color:var(--fg-muted)}
.tk-add{position:relative;display:inline-flex;align-items:center;gap:9px;min-height:44px;padding:0 12px;border-radius:var(--tk-r);border:1.5px solid var(--tk-line);font:700 13.5px/1.1 var(--q-sans,inherit);color:var(--fg);cursor:pointer;white-space:nowrap}
.tk-add input{width:20px;height:20px;margin:0;accent-color:#111}
.tk-add:has(input:checked){border-color:var(--fg);background:var(--tk-soft)}
.tk-add:has(input:focus-visible){outline:3px solid var(--fg);outline-offset:3px}
.tk-src{margin:22px 0 0;font-size:14px;line-height:1.5;color:var(--fg-muted)}
.tk-src a{color:var(--fg);text-decoration:underline;text-underline-offset:3px}
.tk-sum{position:sticky;top:calc(var(--pp-hdr,81px) + 60px);padding:20px;border:1.5px solid var(--fg);border-radius:var(--tk-r);background:var(--bg);max-height:calc(100vh - var(--pp-hdr,81px) - 80px);overflow:auto}
.tk-sum-disc{margin:12px 0 0;font-size:14px;line-height:1.45;color:var(--fg)}
.tk-sum-empty{margin:16px 0 0;font-size:15px;line-height:1.5;color:var(--fg-muted)}
.tk-sum h3{margin:18px 0 6px;font:700 13px/1.3 var(--tk-mono);letter-spacing:.1em;text-transform:uppercase;color:var(--fg)}
.tk-sum ul{list-style:none;margin:0;padding:0}
.tk-sum li{padding:9px 0;border-top:1px solid var(--tk-line);font-size:15px;line-height:1.4;color:var(--fg)}
.tk-sum li small{display:block;margin-top:2px;font-size:13px;color:var(--fg-muted)}
.tk-sum-sys{display:flex;flex-wrap:wrap;gap:6px;margin:0}
.tk-sum-foot{margin:16px 0 0;font-size:14px;line-height:1.5;color:var(--fg-muted)}
.tk-sum-meta{margin:10px 0 0;font:500 13px/1.4 var(--tk-mono);color:var(--fg-muted)}
.tk-sum-act{display:flex;flex-wrap:wrap;gap:10px;margin:16px 0 0}
.tk-sum-act .tk-btn{flex:1 1 130px}
@media(max-width:1040px){.tk-cols{grid-template-columns:minmax(0,1fr)}.tk-sum{position:static;max-height:none}}
@media(max-width:600px){
  .tk-p{grid-template-columns:72px minmax(0,1fr)}.tk-p-img{width:72px}
  .tk-add{grid-column:1/-1;justify-content:center}
  .tk-opts{display:grid;grid-template-columns:1fr 1fr}.tk-sys,.tk-sys-b{width:100%}
  .tk-sys-b{padding:0 12px;font-size:14px}
  .tk-pick{padding:14px}.tk-reset{margin-left:0;width:100%}
}
@media print{
  html.tk-cfgp body > :not(#q-content):not(main),html.tk-cfgp main > :not(.tk-cfg),html.tk-cfgp .pv-crumbs,
  html.tk-cfgp .tk-cfg :is(.tk-head,.tk-disc,.tk-pick,.tk-res,.tk-sum-act){display:none!important}
  html.tk-cfgp,html.tk-cfgp body,html.tk-cfgp .tk-cfg{background:#fff!important;color:#000!important}
  html.tk-cfgp .tk-cfg{--fg:#000;--bg:#fff;--fg-muted:#333;--tk-line:#999;padding:0!important}
  html.tk-cfgp .tk-cfg::before,html.tk-cfgp .tk-cfg::after{display:none!important}
  html.tk-cfgp .tk-cols{display:block}
  html.tk-cfgp .tk-sum{position:static;max-height:none;overflow:visible;border:0;padding:0}
  html.tk-cfgp .tk-sum li{break-inside:avoid}
}
"""

# printable spec sheet: product pages only (html.tk-prod)
PRINT_CSS = r"""
/* ===== tools pass: printable spec sheet ===== */
.tk-printrow{margin:22px 0 0}
html:not(.tk-js) .tk-printrow{display:none}
.tk-printbtn{display:inline-flex;align-items:center;gap:10px;min-height:44px;padding:0 18px;border-radius:var(--radius,8px);border:1.5px solid color-mix(in srgb,var(--fg) 40%,transparent);background:transparent;color:var(--fg);font:700 14px/1 var(--q-sans,inherit);cursor:pointer}
.tk-printbtn:hover{border-color:var(--fg)}
.tk-printbtn:focus-visible{outline:3px solid var(--fg);outline-offset:3px}
html[data-dir="showcase"] .tk-printbtn{border-radius:0;font-family:var(--pn-mono);font-size:13px;letter-spacing:.08em;text-transform:uppercase}
.tk-printfoot{display:none}
@media print{
  @page{margin:14mm}
  html.tk-prod body > :not(#q-content):not(main):not(.tk-printfoot),html.tk-prod .q-header,html.tk-prod .pv-crumbs,html.tk-prod .pn-zb,html.tk-prod .pn-beat,
  html.tk-prod main > :is(.pp-con-sec,#read-next,#start,.pp-bb,.pp-cmp-sec,.dw-an),html.tk-prod main > section:has(.pv-faq,.q-form,.pp-bb),
  html.tk-prod :is(.tk-printrow,.q-btn,.q-btn-ghost,.lf-ps-act,.lf-ps-fine,video,.pv-envcap){display:none!important}
  html.tk-prod,html.tk-prod body{background:#fff!important;color:#000!important}
  html.tk-prod main *{animation:none!important;transition:none!important;opacity:1!important;transform:none!important;filter:none!important;text-shadow:none!important;box-shadow:none!important}
  html.tk-prod main > section{--fg:#000;--bg:#fff;--fg-muted:#333;--border:#999;--accent-ink:#000;background:#fff!important;background-image:none!important;color:#000!important;padding:6mm 0!important;border:0!important;min-height:0!important;break-inside:auto}
  html.tk-prod main *{background-image:none!important}
  html.tk-prod main > section::before,html.tk-prod main > section::after{display:none!important}
  html.tk-prod main :is(h1,h2,h3,h4,p,li,dt,dd,span,em,a,div){color:#000!important;-webkit-text-fill-color:#000!important;-webkit-text-stroke:0!important}
  html.tk-prod main :is(h1,.q-h1){font-size:26pt!important;line-height:1.1!important}
  html.tk-prod main :is(h2,.q-h2){font-size:16pt!important;line-height:1.2!important}
  html.tk-prod main img{max-height:70mm;width:auto!important;max-width:100%!important;object-fit:contain}
  html.tk-prod .lf-spec{display:grid!important;grid-template-columns:1fr 1fr!important;gap:0 10mm!important}
  html.tk-prod .lf-spec-c{border:0!important;border-bottom:.5pt solid #999!important;background:none!important;padding:2.5mm 0!important;break-inside:avoid;border-radius:0!important}
  html.tk-prod .lf-spec-c dd{font-size:11pt!important;font-weight:700}
  html.tk-prod .lf-spec-c dt{font-size:9pt!important}
  html.tk-prod .tk-printfoot{display:block!important;margin:6mm 0 0;padding-top:3mm;border-top:.5pt solid #999;font:9pt/1.4 Arial,sans-serif;color:#000}
}
"""

# ------------------------------------------------------------------------------------------------ JS

PRINT_JS = r"""
(function(){document.documentElement.classList.add('tk-js');
document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('[data-tk-print]');if(b){window.print()}});})();
"""

KEYPAD_JS = r"""
(function(){
'use strict';
var kp=document.getElementById('tk-kp');if(!kp)return;
var root=document.documentElement,reduce=window.matchMedia('(prefers-reduced-motion: reduce)');
function $(s,c){return (c||kp).querySelector(s)}
function $$(s,c){return Array.prototype.slice.call((c||kp).querySelectorAll(s))}
function p2(v){return (v<10?'0':'')+v}
function stamp(){var d=new Date();return p2(d.getHours())+':'+p2(d.getMinutes())+':'+p2(d.getSeconds())}
function tick(){var d=new Date(),h=d.getHours(),days=['SUN','MON','TUE','WED','THU','FRI','SAT'];
  var a=$('[data-tk-day]'),b=$('[data-tk-time]');if(a)a.textContent=days[d.getDay()];if(b)b.textContent=((h%12)||12)+':'+p2(d.getMinutes())+(h<12?' AM':' PM')}
tick();setInterval(tick,20000);

/* sound: off by default, WebAudio, no assets */
var ctx=null,soundOn=false,snd=$('[data-tk-sound]');
function beep(freq,at,dur,vol,type){
  if(!soundOn||!ctx||reduce.matches)return;
  var t=ctx.currentTime+(at||0),o=ctx.createOscillator(),g=ctx.createGain();
  o.type=type||'sine';o.frequency.value=freq;
  g.gain.setValueAtTime(0.0001,t);g.gain.exponentialRampToValueAtTime(vol||0.06,t+0.012);g.gain.exponentialRampToValueAtTime(0.0001,t+dur);
  o.connect(g);g.connect(ctx.destination);o.start(t);o.stop(t+dur+0.02);
}
if(snd)snd.addEventListener('click',function(){
  soundOn=!soundOn;
  if(soundOn&&!ctx){var AC=window.AudioContext||window.webkitAudioContext;if(AC){try{ctx=new AC()}catch(e){ctx=null}}}
  if(ctx&&ctx.state==='suspended')ctx.resume();
  snd.setAttribute('aria-pressed',String(soundOn));
  var t=$('[data-tk-sndtxt]',snd);if(t)t.textContent=soundOn?'Sound on':'Sound off';
  beep(1320,0,0.09);
});

var EXIT=3,FIRE=3,state='armed',timer=null,left=0,code='';
var zones={},order=[];
$$('.tk-z').forEach(function(el){var n=+el.getAttribute('data-z');order.push(n);
  zones[n]={n:n,name:el.getAttribute('data-name'),open:false,byp:false,alarm:false,row:el,scr:$('.tk-zl li[data-z="'+n+'"]')}});
var shield=$('[data-tk-shield]'),label=$('[data-tk-label]'),hint=$('[data-tk-hint]'),logline=$('[data-tk-logline]'),list=$('[data-tk-list]'),armBtn=$('[data-tk-arm]'),dots=$$('[data-tk-code] i');
var events=[];
function zid(z){return 'Zone '+p2(z.n)+' '+z.name}
function log(msg){
  events.unshift([stamp(),msg]);events=events.slice(0,40);
  if(logline)logline.textContent=events[0][0]+'  '+msg;
  renderLog();
}
function renderLog(){
  if(!list)return;list.textContent='';
  events.forEach(function(e){var li=document.createElement('li'),b=document.createElement('b'),s=document.createElement('span');b.textContent=e[0];s.textContent=e[1];li.appendChild(b);li.appendChild(s);list.appendChild(li)});
  if(!events.length){var li=document.createElement('li'),s=document.createElement('span');li.appendChild(document.createElement('b'));s.textContent='Log cleared';li.appendChild(s);list.appendChild(li)}
}
function say(t){if(hint)hint.textContent=t}
function zstate(z){return z.alarm?'alarm':z.byp?'bypassed':z.open?'open':'secure'}
function paintZones(){
  order.forEach(function(n){var z=zones[n],s=zstate(z),word=s==='alarm'?'Alarm':s==='bypassed'?'Bypass':s==='open'?'Open':'Secure';
    [z.row,z.scr].forEach(function(el){if(!el)return;el.setAttribute('data-s',s);var em=el.querySelector('[data-tk-zs]');if(em)em.textContent=word});
    var t=z.row.querySelector('[data-tk-trip]'),b=z.row.querySelector('[data-tk-byp]');
    t.setAttribute('aria-pressed',String(z.open));t.textContent=z.open?'Restore':'Trip';
    b.setAttribute('aria-pressed',String(z.byp));b.textContent=z.byp?'Unbypass':'Bypass';
  });
}
function paint(s){
  state=s;kp.setAttribute('data-tk',s);
  if(root.hasAttribute('data-pn'))root.setAttribute('data-pn',s==='alarm'?'armed':s);
  if(label)label.textContent=s==='armed'?'ARMED':s==='arming'?'ARMING '+left:s==='alarm'?'ALARM':'DISARMED';
  if(shield)shield.setAttribute('aria-label',s==='armed'?'Site armed. Key in any four digits to disarm':s==='arming'?'Arming. Press to cancel':s==='alarm'?'Alarm. Key in any four digits to silence and disarm':'Site disarmed. Press to arm');
  if(armBtn){armBtn.disabled=(s==='armed'||s==='alarm');armBtn.textContent=s==='arming'?'Cancel':'Arm'}
  paintZones();
}
function setCode(v){code=v;dots.forEach(function(d,i){d.classList.toggle('on',i<code.length)})}
function stopTimer(){if(timer){clearInterval(timer);timer=null}left=0}
function finishArm(){stopTimer();paint('armed');log('All zones armed. Supervised.');say('Site armed. Key in any four digits to disarm.');beep(880,0,0.1);beep(1320,0.11,0.22,0.07)}
function arm(){
  var open=order.map(function(n){return zones[n]}).filter(function(z){return z.open&&!z.byp});
  if(open.length){log('Arming refused. '+zid(open[0])+' open.');say('Cannot arm. '+zid(open[0])+' is open. Restore it or bypass it, then arm.');beep(220,0,0.25,0.05,'square');return}
  if(reduce.matches){finishArm();return}
  left=EXIT;kp.style.setProperty('--tk-exit',EXIT+'s');paint('arming');log('Exit delay. Arming.');say('Arming in '+left+'. Press Cancel to stop.');beep(990,0,0.06,0.04,'square');
  timer=setInterval(function(){left-=1;if(left<=0){finishArm()}else{if(label)label.textContent='ARMING '+left;say('Arming in '+left+'. Press Cancel to stop.');beep(990,0,0.06,0.04,'square')}},1000);
}
function disarm(why){
  var was=state;stopTimer();
  order.forEach(function(n){zones[n].alarm=false});
  paint('disarmed');
  log(was==='alarm'?'Alarm silenced. System disarmed.':was==='arming'?'Arming cancelled.':'System disarmed.');
  var open=order.map(function(n){return zones[n]}).filter(function(z){return z.open&&!z.byp});
  say((was==='alarm'?'Alarm silenced. Site disarmed.':was==='arming'?'Arming cancelled. Site disarmed.':'Site disarmed.')+(open.length?' '+zid(open[0])+' is still open.':' Press Arm, or trip a zone.'));
  beep(1320,0,0.08);beep(880,0.1,0.16);
}
function alarm(z){
  stopTimer();z.alarm=true;paint('alarm');log('ALARM. '+zid(z)+'.');say('Alarm on '+zid(z)+'. Key in any four digits to silence it.');
  for(var i=0;i<3;i++){beep(1480,i*0.36,0.16,0.07,'square');beep(1100,i*0.36+0.18,0.16,0.07,'square')}
}
function trip(n){
  var z=zones[n];z.open=!z.open;
  if(!z.open){log(zid(z)+' restored.');say(zid(z)+' restored.'+(z.alarm?' The alarm stays until you key in four digits.':''));paintZones();beep(660,0,0.07);return}
  if(z.byp){log(zid(z)+' opened while bypassed. Ignored.');say(zid(z)+' is bypassed, so nothing happens.');paintZones();return}
  if(state==='armed'||state==='alarm'||n===FIRE){alarm(z);return}
  if(state==='arming'){stopTimer();paint('disarmed');log(zid(z)+' opened during the exit delay. Arming cancelled.');say('Arming cancelled. '+zid(z)+' opened during the exit delay.');return}
  log(zid(z)+' opened. Not armed, no alarm.');say(zid(z)+' is open. The site is disarmed, so there is no alarm.');paintZones();beep(520,0,0.07);
}
function bypass(n){
  var z=zones[n];z.byp=!z.byp;if(z.byp)z.alarm=false;
  log(zid(z)+(z.byp?' bypassed.':' back in the system.'));say(zid(z)+(z.byp?' bypassed. It cannot raise an alarm.':' is back in the system.'));
  if(state==='alarm'&&!order.some(function(k){return zones[k].alarm})){paint('armed');log('No zone in alarm. Armed.')}else{paintZones()}
  if(!z.byp&&z.open&&state==='armed'){alarm(z)}
  beep(740,0,0.06);
}
function digit(d){
  setCode(code+d);beep(1900,0,0.03,0.02,'square');
  if(code.length<4)return;
  setTimeout(function(){setCode('')},260);
  if(state==='disarmed'){say('Already disarmed. Press Arm to arm the site.');return}
  disarm();
}
$$('[data-tk-d]').forEach(function(b){b.addEventListener('click',function(){digit(b.getAttribute('data-tk-d'))})});
var clr=$('[data-tk-clr]');if(clr)clr.addEventListener('click',function(){setCode('');say('Code cleared.')});
kp.addEventListener('keydown',function(e){
  if(e.ctrlKey||e.metaKey||e.altKey)return;
  if(/^[0-9]$/.test(e.key)){digit(e.key);e.preventDefault()}
});
if(shield)shield.addEventListener('click',function(){
  if(state==='disarmed')arm();else if(state==='arming')disarm();
  else say((state==='alarm'?'Alarm. ':'Site armed. ')+'Key in any four digits on the number pad to disarm.');
});
if(armBtn)armBtn.addEventListener('click',function(){if(state==='disarmed')arm();else if(state==='arming')disarm()});
order.forEach(function(n){var z=zones[n];
  z.row.querySelector('[data-tk-trip]').addEventListener('click',function(){trip(n)});
  z.row.querySelector('[data-tk-byp]').addEventListener('click',function(){bypass(n)});
});
var clear=$('[data-tk-clear]');if(clear)clear.addEventListener('click',function(){events=[];renderLog();say('Event log cleared.')});
paint('armed');log('System armed');
})();
"""

CFG_JS = r"""
(function(){
'use strict';
var sec=document.querySelector('.tk-cfg');if(!sec)return;
var D=__TK_DATA__;
function $(s,c){return (c||sec).querySelector(s)}
function $$(s,c){return Array.prototype.slice.call((c||sec).querySelectorAll(s))}
function mk(t,c,txt){var e=document.createElement(t);if(c)e.className=c;if(txt!=null)e.textContent=txt;return e}
function join(a){return a.length<2?a.join(''):a.slice(0,-1).join(', ')+' and '+a[a.length-1]}
var boxes=$$('input[name="sys"]'),items=$$('[data-tk-p]'),groups=$$('[data-tk-grp]'),cover=$('[data-tk-cover]'),count=$('[data-tk-count]'),sum=$('[data-tk-sum]');
var PANEL=['intrusion','access','fire','video'];
items.forEach(function(li,i){li._needs=li.getAttribute('data-needs').split(' ');li._o=i});
function selected(){return boxes.filter(function(b){return b.checked}).map(function(b){return b.value})}
function update(push){
  var sel=selected(),n=0;
  items.forEach(function(li){
    var hit=li._needs.filter(function(k){return sel.indexOf(k)>=0}).length;li._hit=hit;
    var show=!sel.length||hit>0;li.hidden=!show;if(show)n++;
    $$('.tk-tag',li).forEach(function(t,i){t.classList.toggle('is-on',sel.indexOf(li._needs[i])>=0)});
  });
  groups.forEach(function(g){
    var ul=$('.tk-list',g),lis=$$('[data-tk-p]',g),vis=lis.filter(function(li){return !li.hidden});
    lis.slice().sort(function(a,b){return (b._hit-a._hit)||(a._o-b._o)}).forEach(function(li){ul.appendChild(li)});
    g.hidden=!vis.length;var c=$('[data-tk-n]',g);if(c)c.textContent=vis.length;
  });
  if(count)count.textContent=sel.length?n+' of '+items.length+' products are listed under '+join(sel.map(function(k){return D.label[k]}))+'. Products listed under more of your systems come first.':'Pick at least one system type to narrow the list. Showing all '+items.length+' products.';
  /* cover: control panels listed under every panel-side system picked */
  cover.textContent='';
  var ps=sel.filter(function(k){return PANEL.indexOf(k)>=0});
  if(ps.length>=2){
    var names=join(ps.map(function(k){return D.label[k]}));
    var hit=items.filter(function(li){return li.getAttribute('data-kind')==='panels'&&ps.every(function(k){return li._needs.indexOf(k)>=0})});
    var p=mk('p');
    if(hit.length){
      p.appendChild(mk('b',null,'Control panels this site lists under '+names+': '));
      hit.forEach(function(li,i){var a=mk('a',null,li.getAttribute('data-name'));a.href=$('h4 a',li).getAttribute('href');p.appendChild(a);
        if(li.getAttribute('data-soon')==='1')p.appendChild(document.createTextNode(' (coming soon, not orderable)'));
        p.appendChild(document.createTextNode(i<hit.length-1?', ':'.'))});
      cover.appendChild(p);cover.appendChild(mk('p',null,'Listed under the same systems is not an approval that a design works. A DMP dealer confirms it.'));
    }else{
      p.appendChild(mk('b',null,'No control panel on this site is listed under all of '+names+'. '));
      p.appendChild(document.createTextNode('Whether one design can cover them: ask your DMP dealer.'));cover.appendChild(p);
    }
  }
  if(sel.indexOf('mobile')>=0&&ps.length){cover.appendChild(mk('p',null,'Which panels pair with the mobile and cloud products is not stated panel by panel on this site: ask your DMP dealer.'))}
  renderSum(sel);
  if(push&&window.history&&history.replaceState){try{history.replaceState(null,'',sel.length?'#s='+sel.join(','):location.pathname+location.search)}catch(e){}}
}
function renderSum(sel){
  sum.textContent='';
  var picked=items.filter(function(li){var c=$('[data-tk-add]',li);return c&&c.checked}).sort(function(a,b){return a._o-b._o});
  if(!sel.length&&!picked.length){sum.appendChild(mk('p','tk-sum-empty','Pick system types, then tick Add to summary on the products you want.'));return}
  sum.appendChild(mk('h3',null,'System types'));
  if(sel.length){var p=mk('p','tk-sum-sys');sel.forEach(function(k){var t=mk('span','tk-tag');t.style.setProperty('--zc',D.colour[k]);t.appendChild(mk('i'));t.appendChild(document.createTextNode(D.label[k]));p.appendChild(t)});sum.appendChild(p)}
  else sum.appendChild(mk('p','tk-sum-empty','None picked.'));
  sum.appendChild(mk('h3',null,'Shortlist ('+picked.length+')'));
  if(!picked.length){sum.appendChild(mk('p','tk-sum-empty','Nothing ticked yet. Tick Add to summary on a product.'));}
  else{
    var ul=mk('ul');
    picked.forEach(function(li){
      var row=mk('li'),kind=li.getAttribute('data-kind'),fit=li.getAttribute('data-fit');
      row.appendChild(mk('b',null,li.getAttribute('data-name')));
      if(li.getAttribute('data-soon')==='1')row.appendChild(document.createTextNode(' (coming soon, not orderable)'));
      row.appendChild(mk('small',null,D.types[kind]+'. Listed under '+join(li._needs.map(function(k){return D.label[k]||k}))+'.'));
      if(kind!=='panels')row.appendChild(mk('small',null,fit?'Stated fit: '+fit+'.':'Panel fit: ask your DMP dealer.'));
      ul.appendChild(row);
    });
    sum.appendChild(ul);
  }
  var d=new Date();
  sum.appendChild(mk('p','tk-sum-meta','Made '+d.toLocaleDateString(undefined,{year:'numeric',month:'long',day:'numeric'})+' on the DMP website preview.'));
}
boxes.forEach(function(b){b.addEventListener('change',function(){update(true)})});
$$('[data-tk-add]').forEach(function(c){c.addEventListener('change',function(){renderSum(selected())})});
var reset=$('[data-tk-reset]');if(reset)reset.addEventListener('click',function(){boxes.forEach(function(b){b.checked=false});$$('[data-tk-add]').forEach(function(c){c.checked=false});update(true)});
var m=/[#&]s=([a-z,]+)/.exec(location.hash||'');
if(m){var want=m[1].split(',');boxes.forEach(function(b){b.checked=want.indexOf(b.value)>=0})}
update(false);
})();
"""


def _cfg_data(page):
    s = next(x for x in page["sections"] if x.get("type") == "tkcfg")
    both = s["systems"] + s.get("addons", [])
    return json.dumps({"label": {k: lab for k, lab, _c, _h in both}, "colour": {k: c for k, _lab, c, _h in both}, "types": s["types"]},
                      ensure_ascii=False, separators=(",", ":"))


_SPEC_END = re.compile(r'(<dl class="lf-spec">.*?</dl>)', re.S)


def post(doc: str, content: dict, page: dict, dslug: str) -> str:
    if content.get("slug") != SLUG or os.environ.get("TK_OFF"):
        return doc
    types = {s.get("type") for s in page["sections"]}
    tool = types & set(RENDER_TOOLS)
    product = page["file"].startswith("products/") and "specs" in types
    if not tool and not product:
        return doc
    css, js, cls = "", "", []
    if tool:
        css += TOOLS_CSS
    if "tkplay" in types:
        js += KEYPAD_JS
    if "tkcfg" in types:
        js += CFG_JS.replace("__TK_DATA__", _cfg_data(page)) + PRINT_JS
        cls.append("tk-cfgp")
    if product:
        css += PRINT_CSS
        js += PRINT_JS
        cls.append("tk-prod")
        btn = ('<p class="tk-printrow"><button type="button" class="tk-printbtn" data-tk-print>'
               '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M6 9V3h12v6M6 18H4a1 1 0 0 1-1-1v-6a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v6a1 1 0 0 1-1 1h-2M6 14h12v7H6z"/></svg>'
               'Print this spec sheet</button></p>')
        doc = _SPEC_END.sub(lambda m: m.group(1) + btn, doc, count=1)
        foot = ('<p class="tk-printfoot">Printed from a preview of the DMP website. Specifications as listed on this site. '
                "Check DMP's current spec sheet and installation guide before specifying. Sold through authorized DMP dealers.</p>")
        doc = doc.replace("</main>", "</main>\n" + foot, 1)
    if cls:
        doc = re.sub(r'(<html lang="en" data-dir="[a-z]+" class=")', lambda m: m.group(1) + " ".join(cls) + " ", doc, count=1)
    i = doc.find("</style>")
    doc = doc[:i] + "\n/* ===== tools pass (scripts/preview_tools.py) ===== */\n" + css + doc[i:]
    if js:
        doc = doc.replace("</body>", "<script>" + js + "</script>\n</body>", 1)
    return doc
