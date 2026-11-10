"""Round 3a, Clean direction for the DMP preview: THE SITE IS A SPEC SHEET.

Gated twice: the DMP content slug and the Clean direction. Section types registered here (cl-hero, cl-matrix, cl-finder,
cl-doors, cl-proof) are only ever named by brands/dmp_clean.py, as Clean variants, so Showcase and Press never render them.

  RENDER_CLEAN     the dimension-line hero, the product matrix, the panel finder, the audience index, the proof ledger
  post(doc, ...)   Clean pages only: the CSS for the above, the white "figure plate" treatment of the system and industry
                   heroes, and (home only) the small script that filters the matrix and drives the finder.

No-JS and reduced motion render the complete page: the matrix shows every row, the finder shows every panel.
"""
from __future__ import annotations

import os
import re

SLUG = "digital-monitoring-products"
OFF = bool(os.environ.get("DMP_R3A_OFF"))          # control builds: Round 3a switched off

SYS_COL = {"intrusion": "#ffd23d", "access": "#2fd47a", "fire": "#ff5a4d", "video": "#4aa3ff", "mobile": "#9b87ff"}


def _btns(s, ctx):
    E, L = ctx["E"], ctx["L"]
    out = ""
    if s.get("primary"):
        out += f'<a class="q-btn" href="{E(L(s["primary"]["href"]))}">{E(s["primary"]["label"])}</a>'
    if s.get("secondary"):
        out += f'<a class="q-btn-ghost" href="{E(L(s["secondary"]["href"]))}">{E(s["secondary"]["label"])}</a>'
    return out


def _hero(s, ctx):
    E, L, rel, RAW = ctx["E"], ctx["L"], ctx["rel"], ctx["RAW"]
    f = s["figure"]
    dims = "".join(f'<span class="clh-dim clh-dim-{pos}" style="--i:{i}"><b>{E(v)}</b><span>{E(k)}</span></span>' for i, (pos, v, k) in enumerate(f["dims"]))
    lane = "".join(f'<a href="{E(L(h))}">{E(t)}{" <span aria-hidden=true>&darr;</span>" if h.startswith("#") else ""}</a>' for t, h in s.get("lane", []))
    title = "".join(f'<div><dt>{E(k)}</dt><dd>{E(v)}</dd><dd class="d">{E(d)}</dd></div>' for k, v, d in s.get("title", []))
    return f'''<section class="q-section clh" id="{E(s.get("id", "hero-layered"))}" aria-labelledby="clh-h1">
<script>document.documentElement.classList.add("cl-js")</script>
<div class="q-container clh-in">
<div class="clh-copy"><p class="clh-k"><span>{E(s.get("sheet", "Sheet 01"))}</span><span>{E(s.get("eyebrow", ""))}</span></p>
<h1 class="clh-h1" id="clh-h1">{RAW(s["heading"])}</h1>
<p class="clh-lede">{E(s.get("subhead", ""))}</p>
<div class="pv-btns clh-cta">{_btns(s, ctx)}</div>
<p class="clh-lane">{lane}</p></div>
<figure class="clh-fig"><div class="clh-plate"><i class="clh-reg tl" aria-hidden="true"></i><i class="clh-reg tr" aria-hidden="true"></i><i class="clh-reg bl" aria-hidden="true"></i><i class="clh-reg br" aria-hidden="true"></i>
<a class="clh-prod" href="{E(L(f["href"]))}" aria-label="{E(f["label"])}"><img src="{E(rel(f["image"]))}" alt="{E(f["alt"])}" width="{f["w"]}" height="{f["h"]}" fetchpriority="high" decoding="async"></a>
<p class="clh-dims">{dims}</p></div>
<figcaption><span>{E(f["fig"])}</span><span>{E(f["note"])}</span><a href="{E(L(f["href"]))}">{E(f["label"])} <span aria-hidden="true">&rarr;</span></a></figcaption></figure>
</div>
<div class="q-container"><dl class="clh-title">{title}</dl></div>
</section>'''


def _head(s, ctx, cls=""):
    E, RAW = ctx["E"], ctx["RAW"]
    intro = f'<p class="cl-intro">{E(s["intro"])}</p>' if s.get("intro") else ""
    return (f'<header class="cl-head {cls}"><div><div class="q-eyebrow">{E(s.get("eyebrow", ""))}</div>'
            f'<h2 class="q-h2" id="{E(s["id"])}-h">{RAW(s["heading"])}</h2></div>{intro}</header>')


def _matrix(s, ctx):
    E, L, rel = ctx["E"], ctx["L"], ctx["rel"]
    rows = ""
    fams = []
    for i, r in enumerate(s["rows"]):
        if r["family"] not in fams:
            fams.append(r["family"])
        fk = fams.index(r["family"])
        soon = f' <span class="clm-soon">{E(r["soon"])}</span>' if r.get("soon") else ""
        data = "".join(f"<span><i>{E(k)}</i> {E(v)}</span>" for k, v in r["specs"])
        rows += (f'<tr data-f="{fk}" data-q="{E((r["name"] + " " + r["kind"] + " " + r["family"]).lower())}"{" class=clm-x" if i >= s.get("first", 12) else ""}>'
                 f'<td class="n">{i + 1:02d}</td>'
                 f'<th scope="row"><a href="{E(L(r["href"]))}"><span class="clm-th"><img src="{E(rel(r["thumb"]))}" alt="" width="96" height="72" loading="lazy" decoding="async"></span><span>{E(r["name"])}{soon}</span></a></th>'
                 f'<td class="f"><i class="clm-tick" style="background:{SYS_COL.get(r["sys"], "#0b0d10")}" aria-hidden="true"></i>{E(r["family"])}</td>'
                 f'<td class="k">{E(r["kind"])}</td><td class="d">{data}</td></tr>')
    chips = f'<button type="button" class="is-on" data-f="all" aria-pressed="true">All <b>{len(s["rows"])}</b></button>'
    for k, fam in enumerate(fams):
        n = sum(1 for r in s["rows"] if r["family"] == fam)
        chips += f'<button type="button" data-f="{k}" aria-pressed="false">{E(fam)} <b>{n}</b></button>'
    return f'''<section class="q-section clm" id="{E(s["id"])}" aria-labelledby="{E(s["id"])}-h">
<div class="q-container">{_head(s, ctx)}
<div class="clm-ctl cl-js-only" role="group" aria-label="Filter the product matrix">
<div class="clm-chips">{chips}</div>
<label class="clm-find"><span>Search</span><input type="search" data-clm-q placeholder="{E(s.get("placeholder", "Name or type"))}" autocomplete="off"></label></div>
<p class="clm-count cl-js-only" role="status" aria-live="polite" data-clm-count>{len(s["rows"])} of {len(s["rows"])} products</p>
<div class="clm-wrap"><table class="clm-t"><caption class="cl-sr">{E(s.get("caption", ""))}</caption>
<thead><tr><th scope="col" class="n">No.</th><th scope="col">Product</th><th scope="col">System</th><th scope="col">Type</th><th scope="col">Key data</th></tr></thead>
<tbody>{rows}</tbody></table>
<p class="clm-none" data-clm-none hidden>{E(s.get("none", "No product matches. Clear the search to see every product."))}</p></div>
<p class="clm-more cl-js-only"><button type="button" class="q-btn-ghost" data-clm-more aria-expanded="false">{E(s.get("more", "Show all products"))}</button></p>
<p class="cl-foot">{E(s.get("foot", ""))}</p>
</div></section>'''


def _finder(s, ctx):
    E, L = ctx["E"], ctx["L"]
    mx = s["max"]
    rows = ""
    for p in s["panels"]:
        soon = f'<span class="clm-soon">{E(p["soon"])}</span>' if p.get("soon") else ""
        rows += (f'<li class="cl-rv{" is-soon" if p.get("soon") else ""}{" is-wide" if p["zones"] / mx > 0.8 else ""}" data-z="{p["zones"]}" data-d="{p.get("doors_n", 0)}" data-name="{E(p["name"])}"{" data-soon=1" if p.get("soon") else ""}>'
                 f'<a class="clf-n" href="{E(L(p["href"]))}"><b>{E(p["name"])}</b><span>{E(p["kind"])}</span>{soon}</a>'
                 f'<div class="clf-track"><i class="clf-bar" style="--w:{p["zones"] / mx * 100:.2f}%"></i><span class="clf-v" style="--w:{p["zones"] / mx * 100:.2f}%">{E(p["zones_label"])}</span></div>'
                 f'<dl><div><dt>Doors</dt><dd>{E(p["doors"])}</dd></div><div><dt>User codes</dt><dd>{E(p["users"])}</dd></div></dl></li>')
    ticks = "".join(f'<span style="left:{t / mx * 100:.2f}%">{t}</span>' for t in s["ticks"])
    return f'''<section class="q-section clf" id="{E(s["id"])}" data-max="{mx}" aria-labelledby="{E(s["id"])}-h">
<div class="q-container">{_head(s, ctx)}
<div class="clf-ctl cl-js-only"><label for="clf-z"><span>Zones needed</span><output data-clf-out>1</output></label>
<input id="clf-z" type="range" min="1" max="{s["slider_max"]}" value="1" step="1" data-clf-z>
<p class="clf-res" role="status" aria-live="polite" data-clf-res>{E(s["all"])}</p></div>
<div class="clf-board"><div class="clf-scale" aria-hidden="true"><em>Total zones</em><div>{ticks}<i class="clf-mark" data-clf-mark></i></div></div>
<ol class="clf-rows">{rows}</ol></div>
<p class="cl-foot">{E(s.get("foot", ""))}</p>
</div></section>'''


def _doors(s, ctx):
    E, L = ctx["E"], ctx["L"]
    cols = ""
    for i, it in enumerate(s["items"]):
        bl = "".join(f"<li>{E(b)}</li>" for b in it.get("bullets", []))
        cols += (f'<li class="cl-rv"><span class="cld-n" aria-hidden="true">{i + 1:02d}</span><p class="cld-k">{E(it["kicker"])}</p>'
                 f'<h3><a href="{E(L(it["href"]))}">{E(it["title"])}</a></h3><ul>{bl}</ul>'
                 f'<span class="cld-go" aria-hidden="true">{E(it["cta"])} &rarr;</span></li>')
    return f'''<section class="q-section cld" id="{E(s["id"])}" aria-labelledby="{E(s["id"])}-h">
<div class="q-container">{_head(s, ctx)}<ol class="cld-cols">{cols}</ol></div></section>'''


def _proof(s, ctx):
    E = ctx["E"]
    cells = "".join(f'<div class="cl-rv"><dd>{E(it["n"])}</dd><dt>{E(it["label"])}</dt><dd class="s">{E(it.get("sub", ""))}</dd></div>' for it in s["items"])
    return f'''<section class="q-section clp" id="{E(s["id"])}" aria-labelledby="{E(s["id"])}-h">
<div class="q-container">{_head(s, ctx)}<dl class="clp-row">{cells}</dl><p class="cl-foot">{E(s.get("foot", ""))}</p></div></section>'''


RENDER_CLEAN = {"cl-hero": _hero, "cl-matrix": _matrix, "cl-finder": _finder, "cl-doors": _doors, "cl-proof": _proof}


# ------------------------------------------------------------------------------------------------ CSS

HERO_CSS = r"""
/* ===== round 3a, Clean: system and industry heroes as a white sheet with a figure plate ===== */
html[data-dir="clean"] .pv-lh:has(> .bg.env){background:#fff;color:var(--cl-ink);--lh-bg:#fff;border-bottom:1px solid var(--cl-ink);
  background-image:linear-gradient(var(--cl-line) 1px,transparent 1px),linear-gradient(90deg,var(--cl-line) 1px,transparent 1px);background-size:100% 96px,96px 100%}
html[data-dir="clean"] .pv-lh:has(> .bg.env) :is(.net,.glow){display:none}
html[data-dir="clean"] .pv-lh:has(> .bg.env) > .bg.env{inset:0 0 0 auto;width:46%;border-left:1px solid var(--cl-ink);overflow:hidden;background:#12151a}
html[data-dir="clean"] .pv-lh:has(> .bg.env) > .bg.env img{opacity:1;filter:grayscale(1) contrast(.96) brightness(1.75);animation:cl-plate 1.1s cubic-bezier(.2,.7,.2,1) both;transform:none}
html[data-dir="clean"] .pv-lh:has(> .bg.env) > .bg.env.flip img{transform:scaleX(-1);animation-name:cl-plate-f}
@keyframes cl-plate{from{opacity:0;transform:scale(1.06)}to{opacity:1;transform:none}}
@keyframes cl-plate-f{from{opacity:0;transform:scaleX(-1) scale(1.06)}to{opacity:1;transform:scaleX(-1)}}
html[data-dir="clean"] .pv-lh:has(> .bg.env) > .bg.env::after{background:linear-gradient(rgba(255,255,255,.16) 1px,transparent 1px) 0 0/100% 96px,linear-gradient(90deg,rgba(255,255,255,.16) 1px,transparent 1px) 0 0/96px 100%,linear-gradient(180deg,rgba(13,16,20,.04),rgba(13,16,20,.3))}
html[data-dir="clean"] .pv-lh:has(> .bg.env) > .bg.env::before{content:"";position:absolute;inset:18px;z-index:2;pointer-events:none;
  background:linear-gradient(#fff,#fff) 0 0/22px 1px,linear-gradient(#fff,#fff) 0 0/1px 22px,linear-gradient(#fff,#fff) 100% 0/22px 1px,linear-gradient(#fff,#fff) 100% 0/1px 22px,
  linear-gradient(#fff,#fff) 0 100%/22px 1px,linear-gradient(#fff,#fff) 0 100%/1px 22px,linear-gradient(#fff,#fff) 100% 100%/22px 1px,linear-gradient(#fff,#fff) 100% 100%/1px 22px;background-repeat:no-repeat}
html[data-dir="clean"] .pv-lh:has(> .bg.env) .q-container{grid-template-columns:minmax(0,1fr) minmax(0,.86fr);gap:72px;padding-top:72px;padding-bottom:80px}
html[data-dir="clean"] .pv-lh:has(> .bg.env) .q-container > div:first-child{background:#fff;padding:28px 28px 28px 0;box-shadow:-60px 0 0 #fff}
html[data-dir="clean"] .pv-lh:has(> .bg.env) .q-eyebrow{color:var(--cl-ink)}
html[data-dir="clean"] .pv-lh:has(> .bg.env) .q-eyebrow::before{color:var(--cl-ink);background:none}
html[data-dir="clean"][data-sys] .pv-lh:has(> .bg.env) .q-eyebrow::after{content:"";width:12px;height:12px;background:var(--sys);border:1px solid var(--cl-ink);margin-left:2px}
html[data-dir="clean"] .pv-lh:has(> .bg.env) .q-h1{color:var(--cl-ink);font-size:clamp(40px,4.6vw,68px);line-height:1;letter-spacing:-.04em}
html[data-dir="clean"] .pv-lh:has(> .bg.env) .q-h1 em{color:var(--cl-ink);font-style:normal;text-decoration:underline;text-decoration-color:#ffd23d;text-decoration-thickness:.11em;text-underline-offset:.07em;text-decoration-skip-ink:none}
html[data-dir="clean"] .pv-lh:has(> .bg.env) .q-lead{color:#333a46}
html[data-dir="clean"] .pv-lh:has(> .bg.env) .pv-btns .q-btn{background:var(--cl-ink);color:#fff;border-color:var(--cl-ink)}
html[data-dir="clean"] .pv-lh:has(> .bg.env) .pv-btns .q-btn:hover{background:#ffd23d;color:var(--cl-ink)}
html[data-dir="clean"] .pv-lh:has(> .bg.env) .pv-btns .q-btn-ghost{color:var(--cl-ink);border-color:var(--cl-ink)}
html[data-dir="clean"] .pv-lh:has(> .bg.env) .lane .k{color:var(--fg-muted);font-family:var(--pn-mono)}
html[data-dir="clean"] .pv-lh:has(> .bg.env) .lane a{min-height:44px;border-radius:0;border-color:var(--cl-ink);color:var(--cl-ink);background:#fff;font-family:var(--pn-mono);font-size:13px;letter-spacing:.04em}
html[data-dir="clean"] .pv-lh:has(> .bg.env) .lane a:hover{background:var(--cl-ink);color:#fff}
html[data-dir="clean"] .pv-lh:has(> .bg.env) .pv-hero-stats{border-top:1px solid var(--cl-ink)}
html[data-dir="clean"] .pv-lh:has(> .bg.env) .pv-hero-stats > div{border-left-color:var(--cl-line)}
html[data-dir="clean"] .pv-lh:has(> .bg.env) .pv-hero-stats b{color:var(--cl-ink)}
html[data-dir="clean"] .pv-lh:has(> .bg.env) .pv-hero-stats span{color:var(--fg-muted)}
html[data-dir="clean"] .pv-lh:has(> .bg.env) .fcard,html[data-dir="clean"] .pv-lh:has(> .bg.env) .fcard.b{background:#fff;color:var(--cl-ink);border:1px solid var(--cl-ink);border-radius:0;box-shadow:8px 8px 0 rgba(11,13,16,.9);backdrop-filter:none;-webkit-backdrop-filter:none}
html[data-dir="clean"] .pv-lh:has(> .bg.env) .fcard .k,html[data-dir="clean"][data-sys] .pv-lh:has(> .bg.env) .fcard .k{color:var(--fg-muted);font-family:var(--pn-mono);letter-spacing:.1em}
html[data-dir="clean"] .pv-lh:has(> .bg.env) .fcard p{color:#333a46}
html[data-dir="clean"] .pv-lh:has(> .bg.env) .fcard p.t{color:var(--cl-ink)}
html[data-dir="clean"] .pv-lh:has(> .bg.env) .fcard li::before,html[data-dir="clean"][data-sys] .pv-lh:has(> .bg.env) .fcard li::before{border-radius:0;width:10px;height:10px;margin-top:5px;background:var(--sys,#ffd23d);box-shadow:0 0 0 1px var(--cl-ink)}
html[data-dir="clean"] .pv-lh:has(> .bg.env) .fcard .go{border-radius:0;background:var(--cl-ink);color:#fff}
html[data-dir="clean"] .pv-lh:has(> .bg.env) .fcard .go:hover{background:#ffd23d;color:var(--cl-ink)}
html[data-dir="clean"] .pv-lh:has(> .bg.env) .fcard.b .links a{border-radius:0;border-color:var(--cl-ink)}
html[data-dir="clean"] .pv-lh:has(> .bg.env) .hero3d.lf-float::before{display:none}
html[data-dir="clean"] .pv-lh:has(> .bg.env) .hero3d.lf-float::after{border:1px solid rgba(255,255,255,.55);border-radius:0;animation:none;width:min(88%,460px);aspect-ratio:4/3}
html[data-dir="clean"] .pv-lh:has(> .bg.env) .hero3d.lf-float img.fallback{animation:none;filter:drop-shadow(0 26px 30px rgba(0,0,0,.55))}
html[data-dir="clean"] .pv-lh:has(> .bg.env) > .pv-envcap{right:0;bottom:0;border-radius:0;background:#fff;color:var(--cl-ink);border:1px solid var(--cl-ink);border-right:0;border-bottom:0;font:600 13px/1 var(--pn-mono);letter-spacing:.08em;text-transform:uppercase;padding:9px 12px}
html[data-dir="clean"] .pv-lh:has(> .bg.env) > .pv-envcap::before{content:"Fig. / "}
html[data-dir="clean"][data-sys] .pv-lh:has(> .bg.env){border-top:1px solid var(--cl-ink)}
@media(max-width:1024px){
  html[data-dir="clean"] .pv-lh:has(> .bg.env){padding-top:0;background-image:none}
  html[data-dir="clean"] .pv-lh:has(> .bg.env) > .bg.env{position:relative;inset:auto;width:100%;height:clamp(200px,38vw,340px);border-left:0;border-bottom:1px solid var(--cl-ink)}
  html[data-dir="clean"] .pv-lh:has(> .bg.env) > .pv-envcap{top:0;bottom:auto;border:1px solid var(--cl-ink);border-top:0;border-right:0}
  html[data-dir="clean"] .pv-lh:has(> .bg.env) .q-container{grid-template-columns:minmax(0,1fr);gap:28px;padding-top:28px;padding-bottom:56px}
  html[data-dir="clean"] .pv-lh:has(> .bg.env) .q-container > div:first-child{padding:0;box-shadow:none;background:none}
  html[data-dir="clean"] .pv-lh:has(> .bg.env) .hero3d.lf-float{background:#12151a;min-height:260px}
  html[data-dir="clean"] .pv-lh:has(> .bg.env) .fcard{box-shadow:5px 5px 0 rgba(11,13,16,.9)}
}
@media(prefers-reduced-motion:reduce){html[data-dir="clean"] .pv-lh:has(> .bg.env) > .bg.env img{animation:none!important}}
"""

HOME_CSS = r"""
/* ===== round 3a, Clean home: the spec sheet ===== */
.cl-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
html:not(.cl-js) .cl-js-only{display:none!important}
.cl-head{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);gap:48px;align-items:end;margin-bottom:40px}
.cl-head .q-h2{margin:14px 0 0;font-size:clamp(34px,4.2vw,64px);line-height:.98;letter-spacing:-.045em;max-width:16ch}
.cl-intro{margin:0;font-size:17px;line-height:1.6;color:#333a46;max-width:52ch;padding-left:20px;border-left:1px solid var(--cl-ink)}
.cl-foot{margin:22px 0 0;font:500 13px/1.5 var(--pn-mono);letter-spacing:.04em;color:var(--fg-muted)}
html.cl-js .cl-rv{opacity:0;transform:translateY(14px);transition:opacity .6s ease,transform .6s cubic-bezier(.2,.7,.2,1)}
html.cl-js .cl-rv.in{opacity:1;transform:none}
/* hero */
.clh{position:relative;padding:0!important;background:#fff;border-bottom:1px solid var(--cl-ink);
  background-image:linear-gradient(var(--cl-line) 1px,transparent 1px),linear-gradient(90deg,var(--cl-line) 1px,transparent 1px)!important;background-size:100% 96px,96px 100%!important;background-repeat:repeat!important}
.clh-in{display:grid;grid-template-columns:minmax(0,.86fr) minmax(0,1.14fr);gap:48px;align-items:center;padding-top:48px;padding-bottom:56px}
.clh-copy{background:#fff;padding:26px 26px 26px 0;box-shadow:-60px 0 0 #fff}
.clh-k{display:flex;flex-wrap:wrap;gap:0;margin:0 0 26px;font:600 13px/1 var(--pn-mono);letter-spacing:.12em;text-transform:uppercase;color:var(--cl-ink)}
.clh-k span{padding:9px 12px;border:1px solid var(--cl-ink)}
.clh-k span:first-child{background:var(--cl-ink);color:#fff}
.clh-k span + span{border-left:0}
.clh-h1{margin:0;font-family:var(--q-serif);font-weight:800;font-size:clamp(44px,5.3vw,84px);line-height:.94;letter-spacing:-.055em;color:var(--cl-ink);text-wrap:balance}
.clh-h1 em{font-style:normal;text-decoration:underline;text-decoration-color:#ffd23d;text-decoration-thickness:.11em;text-underline-offset:.07em;text-decoration-skip-ink:none}
.clh-lede{margin:22px 0 0;max-width:50ch;font-size:18px;line-height:1.55;color:#333a46}
.clh-cta{margin-top:30px;display:flex;flex-wrap:wrap;gap:12px;align-items:center}
.clh .clh-cta .q-btn{background:var(--cl-ink);color:#fff;border-color:var(--cl-ink);min-height:52px}
.clh .clh-cta .q-btn:hover{background:#ffd23d;color:var(--cl-ink)}
.clh .clh-cta .q-btn-ghost{color:var(--cl-ink);border:1px solid var(--cl-ink);border-radius:0;min-height:52px;padding:0 22px;display:inline-flex;align-items:center;text-decoration:none;font-weight:700}
.clh .clh-cta .q-btn-ghost:hover{background:var(--cl-ink);color:#fff}
.clh-lane{margin:26px 0 0;display:flex;flex-wrap:wrap;gap:6px 22px}
.clh-lane a{display:inline-flex;align-items:center;min-height:44px;font:600 13px/1 var(--pn-mono);letter-spacing:.06em;text-transform:uppercase;color:var(--cl-ink);text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:6px}
.clh-lane a:hover{text-decoration-thickness:2px;text-decoration-color:#c79a00}
.clh-fig{margin:0;min-width:0}
.clh-plate{position:relative;background:#fff;border:1px solid var(--cl-ink);padding:78px 86px 78px 96px}
.clh-reg{position:absolute;width:15px;height:15px;border:0 solid var(--cl-ink)}
.clh-reg.tl{left:10px;top:10px;border-left-width:1px;border-top-width:1px}.clh-reg.tr{right:10px;top:10px;border-right-width:1px;border-top-width:1px}
.clh-reg.bl{left:10px;bottom:10px;border-left-width:1px;border-bottom-width:1px}.clh-reg.br{right:10px;bottom:10px;border-right-width:1px;border-bottom-width:1px}
.clh-prod{display:block;position:relative}
.clh-prod img{display:block;width:100%;height:auto;filter:drop-shadow(0 22px 22px rgba(11,13,16,.2));transition:transform .5s cubic-bezier(.2,.7,.2,1)}
.clh-prod:hover img{transform:translateY(-4px)}
.clh-dims{margin:0}
.clh-dim{position:absolute;display:flex;align-items:center;justify-content:center;gap:7px;font:600 13px/1 var(--pn-mono);letter-spacing:.08em;text-transform:uppercase;color:var(--cl-blue);white-space:nowrap}
.clh-dim b{font-size:15px;font-weight:700;font-variant-numeric:tabular-nums}
.clh-dim::before{content:"";position:absolute;z-index:0}
.clh-dim > *{position:relative;z-index:1}
.clh-dim-t,.clh-dim-b{left:96px;right:86px;height:13px}
.clh-dim-t{top:38px}.clh-dim-b{bottom:38px}
.clh-dim-t::before,.clh-dim-b::before{inset:0;border-left:1px solid var(--cl-blue);border-right:1px solid var(--cl-blue);background:linear-gradient(var(--cl-blue),var(--cl-blue)) 0 50%/100% 1px no-repeat;transform-origin:0 50%}
.clh-dim-l,.clh-dim-r{top:78px;bottom:78px;width:13px;writing-mode:vertical-rl}
.clh-dim-l{left:44px;transform:rotate(180deg)}.clh-dim-r{right:36px}
.clh-dim-l::before,.clh-dim-r::before{inset:0;border-top:1px solid var(--cl-blue);border-bottom:1px solid var(--cl-blue);background:linear-gradient(var(--cl-blue),var(--cl-blue)) 50% 0/1px 100% no-repeat;transform-origin:50% 0}
.clh-dim{text-shadow:0 0 0 #fff}
.clh-dim b,.clh-dim{background:none}
.clh-dim-t,.clh-dim-b,.clh-dim-l,.clh-dim-r{isolation:isolate}
.clh-dim::after{content:"";position:absolute;z-index:0;background:#fff}
.clh-dim-t::after,.clh-dim-b::after{top:0;bottom:0;left:50%;width:calc(var(--lw,17ch) + 16px);transform:translateX(-50%)}
.clh-dim-l::after,.clh-dim-r::after{left:0;right:0;top:50%;height:calc(var(--lw,17ch) + 16px);transform:translateY(-50%)}
@media(prefers-reduced-motion:no-preference){
  html.cl-js .clh-dim-t::before,html.cl-js .clh-dim-b::before{animation:clh-x .9s cubic-bezier(.2,.7,.2,1) calc(.35s + var(--i)*.14s) both}
  html.cl-js .clh-dim-l::before,html.cl-js .clh-dim-r::before{animation:clh-y .9s cubic-bezier(.2,.7,.2,1) calc(.35s + var(--i)*.14s) both}
  html.cl-js .clh-dim > *,html.cl-js .clh-dim::after{animation:clh-f .5s ease calc(.9s + var(--i)*.14s) both}
  html.cl-js .clh-prod img{animation:clh-p .9s cubic-bezier(.2,.7,.2,1) .05s both}
  html.cl-js .clh-copy > *{animation:clh-u .7s cubic-bezier(.2,.7,.2,1) both}
  html.cl-js .clh-copy > :nth-child(2){animation-delay:.06s}html.cl-js .clh-copy > :nth-child(3){animation-delay:.14s}html.cl-js .clh-copy > :nth-child(4){animation-delay:.2s}html.cl-js .clh-copy > :nth-child(5){animation-delay:.26s}
}
@keyframes clh-x{from{transform:scaleX(0)}to{transform:none}}
@keyframes clh-y{from{transform:scaleY(0)}to{transform:none}}
@keyframes clh-f{from{opacity:0}to{opacity:1}}
@keyframes clh-p{from{opacity:0;transform:translateY(16px) scale(.97)}to{opacity:1;transform:none}}
@keyframes clh-u{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
.clh-fig figcaption{display:grid;grid-template-columns:auto minmax(0,1fr) auto;gap:0;border:1px solid var(--cl-ink);border-top:0;background:#fff;font:500 13px/1.4 var(--pn-mono);letter-spacing:.04em;color:var(--cl-ink)}
.clh-fig figcaption > *{padding:12px 14px;display:flex;align-items:center;min-height:44px}
.clh-fig figcaption > span:first-child{font-weight:700;text-transform:uppercase;letter-spacing:.1em;border-right:1px solid var(--cl-ink)}
.clh-fig figcaption > span + span{color:var(--fg-muted)}
.clh-fig figcaption a{border-left:1px solid var(--cl-ink);font-weight:700;color:var(--cl-ink);text-decoration:none;text-transform:uppercase;letter-spacing:.08em;gap:8px}
.clh-fig figcaption a:hover{background:var(--cl-ink);color:#fff}
.clh-title{margin:0;display:grid;grid-template-columns:repeat(5,minmax(0,1fr));border:1px solid var(--cl-ink);border-bottom:0;background:#fff}
.clh-title > div{padding:16px 18px 18px;border-left:1px solid var(--cl-ink);min-width:0}
.clh-title > div:first-child{border-left:0}
.clh-title dt{font:600 13px/1 var(--pn-mono);letter-spacing:.12em;text-transform:uppercase;color:var(--fg-muted)}
.clh-title dd{margin:10px 0 0;font-family:var(--q-serif);font-weight:800;font-size:clamp(26px,2.6vw,40px);line-height:1;letter-spacing:-.04em;color:var(--cl-ink);font-variant-numeric:tabular-nums}
.clh-title dd.d{margin-top:8px;font:500 13px/1.4 var(--pn-mono);letter-spacing:.02em;color:var(--fg-muted)}
/* matrix */
.clm{background-color:#fff}
.clm-ctl{display:grid;grid-template-columns:minmax(0,1fr) minmax(220px,300px);gap:20px;align-items:end;border-top:1px solid var(--cl-ink);padding-top:18px}
.clm-chips{display:flex;flex-wrap:wrap;gap:6px}
.clm-chips button{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:0 13px;border:1px solid var(--cl-line);background:#fff;color:var(--cl-ink);font:600 13px/1 var(--pn-mono);letter-spacing:.04em;cursor:pointer;transition:background .15s,color .15s,border-color .15s}
.clm-chips button b{font-weight:500;color:var(--fg-muted);font-variant-numeric:tabular-nums}
.clm-chips button:hover{border-color:var(--cl-ink)}
.clm-chips button.is-on{background:var(--cl-ink);border-color:var(--cl-ink);color:#fff}
.clm-chips button.is-on b{color:#d5d9df}
.clm-chips button:focus-visible,.clm-find input:focus-visible,.clf-ctl input:focus-visible{outline:3px solid var(--cl-blue);outline-offset:2px}
.clm-find{display:grid;gap:7px;font:600 13px/1 var(--pn-mono);letter-spacing:.12em;text-transform:uppercase;color:var(--fg-muted)}
.clm-find input{width:100%;min-height:44px;padding:0 12px;border:1px solid var(--cl-ink);border-radius:0;background:#fff;color:var(--cl-ink);font:500 15px/1 var(--pn-mono)}
.clm-count{margin:16px 0 10px;font:600 13px/1 var(--pn-mono);letter-spacing:.08em;text-transform:uppercase;color:var(--fg-muted)}
.clm-wrap{border-top:2px solid var(--cl-ink);border-bottom:1px solid var(--cl-ink)}
.clm-t{width:100%;border-collapse:collapse;table-layout:fixed}
.clm-t thead th{padding:12px 14px 12px 0;text-align:left;font:600 13px/1 var(--pn-mono);letter-spacing:.12em;text-transform:uppercase;color:var(--fg-muted);border-bottom:1px solid var(--cl-ink)}
.clm-t th.n,.clm-t td.n{width:56px}
.clm-t thead th:nth-child(2){width:31%}.clm-t thead th:nth-child(3){width:19%}.clm-t thead th:nth-child(4){width:15%}
.clm-t tbody tr{border-bottom:1px solid var(--cl-line);transition:background .15s}
.clm-t tbody tr:last-child{border-bottom:0}
.clm-t tbody tr:hover{background:#f4f5f6}
.clm-t tbody tr:hover .clm-th img{transform:scale(1.12)}
.clm-t td,.clm-t tbody th{padding:10px 14px 10px 0;vertical-align:middle;text-align:left;font-size:15px;line-height:1.35;color:var(--cl-ink);font-weight:400}
.clm-t td.n{font:500 13px/1 var(--pn-mono);color:var(--fg-muted);padding-left:6px}
.clm-t tbody th a{display:grid;grid-template-columns:64px minmax(0,1fr);gap:14px;align-items:center;min-height:52px;color:var(--cl-ink);text-decoration:none;font-weight:700;font-size:16px;letter-spacing:-.01em}
.clm-t tbody th a:hover > span:last-child{text-decoration:underline;text-underline-offset:4px}
.clm-th{display:grid;place-items:center;width:64px;height:48px;overflow:hidden}
.clm-th img{max-width:100%;max-height:100%;width:auto;height:auto;object-fit:contain;transition:transform .3s cubic-bezier(.2,.7,.2,1)}
.clm-t td.f{font:500 13px/1.35 var(--pn-mono);letter-spacing:.02em}
.clm-tick{display:inline-block;width:10px;height:10px;margin-right:9px;border:1px solid var(--cl-ink);vertical-align:-1px}
.clm-t td.k{color:#333a46}
.clm-t td.d{font:500 13px/1.5 var(--pn-mono);font-variant-numeric:tabular-nums}
.clm-t td.d span{display:inline-block;margin-right:18px;white-space:nowrap}
.clm-t td.d i{font-style:normal;color:var(--fg-muted)}
.clm-soon{display:inline-block;margin-left:8px;padding:3px 6px;border:1px dashed var(--cl-ink);font:600 13px/1.1 var(--pn-mono);letter-spacing:.04em;color:var(--cl-ink);vertical-align:1px;white-space:nowrap}
html.cl-js .clm:not(.is-open):not(.is-filter) tr.clm-x{display:none}
.clm tr[hidden]{display:none}
.clm-none{margin:0;padding:26px 0;font:500 15px/1.5 var(--pn-mono);color:var(--cl-ink)}
.clm-more{margin:18px 0 0}
.clm-more button{min-height:48px;padding:0 20px;border:1px solid var(--cl-ink);border-radius:0;background:#fff;color:var(--cl-ink);font:700 13px/1 var(--pn-mono);letter-spacing:.08em;text-transform:uppercase;cursor:pointer}
.clm-more button:hover{background:var(--cl-ink);color:#fff}
.clm.is-filter .clm-more{display:none}
/* finder */
.clf{background-color:#f4f5f6}
.clf-ctl{display:grid;grid-template-columns:230px minmax(0,1fr);gap:8px 28px;align-items:center;padding:20px 22px;border:1px solid var(--cl-ink);background:#fff}
.clf-ctl label{display:flex;align-items:baseline;justify-content:space-between;gap:12px;font:600 13px/1 var(--pn-mono);letter-spacing:.12em;text-transform:uppercase;color:var(--fg-muted)}
.clf-ctl output{font-family:var(--q-serif);font-weight:800;font-size:44px;line-height:1;letter-spacing:-.04em;color:var(--cl-ink);font-variant-numeric:tabular-nums}
.clf-ctl input[type=range]{-webkit-appearance:none;appearance:none;width:100%;height:44px;background:transparent;margin:0;cursor:pointer}
.clf-ctl input[type=range]::-webkit-slider-runnable-track{height:2px;background:var(--cl-ink)}
.clf-ctl input[type=range]::-moz-range-track{height:2px;background:var(--cl-ink)}
.clf-ctl input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:28px;height:28px;margin-top:-13px;background:#ffd23d;border:2px solid var(--cl-ink);border-radius:0}
.clf-ctl input[type=range]::-moz-range-thumb{width:24px;height:24px;background:#ffd23d;border:2px solid var(--cl-ink);border-radius:0}
.clf-res{grid-column:1/-1;margin:0;padding-top:12px;border-top:1px solid var(--cl-line);font:500 15px/1.5 var(--pn-mono);color:var(--cl-ink)}
.clf-board{margin-top:22px;background:#fff;border:1px solid var(--cl-ink);--nw:230px;--dw:300px}
.clf-scale{display:grid;grid-template-columns:var(--nw) minmax(0,1fr) var(--dw);border-bottom:1px solid var(--cl-ink);font:500 13px/1 var(--pn-mono);color:var(--fg-muted)}
.clf-scale em{font-style:normal;padding:14px 18px;text-transform:uppercase;letter-spacing:.12em;font-weight:600}
.clf-scale > div{position:relative;height:42px;margin:0 30px 0 0;background:repeating-linear-gradient(90deg,var(--cl-ink) 0 1px,transparent 1px calc(100%/60)) 0 100%/100% 7px no-repeat}
.clf-scale span{position:absolute;top:10px;transform:translateX(-50%);font-variant-numeric:tabular-nums}
.clf-scale span:first-child{transform:none}
.clf-mark{position:absolute;top:0;left:0;width:2px;height:calc(100% + var(--rows-h,0px));background:var(--cl-blue);opacity:0;z-index:2;pointer-events:none;transition:left .12s linear}
.clf.is-set .clf-mark{opacity:1}
.clf-rows{list-style:none;margin:0;padding:0}
.clf-rows li{display:grid;grid-template-columns:var(--nw) minmax(0,1fr) var(--dw);align-items:center;border-bottom:1px solid var(--cl-line);transition:opacity .25s,background .25s}
.clf-rows li:last-child{border-bottom:0}
.clf-n{display:grid;gap:4px;padding:16px 18px;min-height:44px;color:var(--cl-ink);text-decoration:none}
.clf-n b{font-family:var(--q-serif);font-weight:800;font-size:26px;line-height:1;letter-spacing:-.03em}
.clf-n span{font:500 13px/1.3 var(--pn-mono);color:var(--fg-muted)}
.clf-n .clm-soon{margin:4px 0 0;justify-self:start;color:var(--cl-ink)}
.clf-n:hover b{text-decoration:underline;text-underline-offset:4px;text-decoration-thickness:2px}
.clf-track{position:relative;height:30px;margin-right:30px;background:linear-gradient(var(--cl-line),var(--cl-line)) 0 50%/100% 1px no-repeat}
.clf-bar{position:absolute;left:0;top:5px;bottom:5px;width:var(--w);background:var(--cl-ink);transform-origin:0 50%}
.is-soon .clf-bar{background:repeating-linear-gradient(135deg,var(--cl-ink) 0 2px,transparent 2px 7px);outline:1px solid var(--cl-ink);outline-offset:-1px}
.clf-v{position:absolute;left:var(--w);top:50%;transform:translate(10px,-50%);font:700 15px/1 var(--pn-mono);color:var(--cl-ink);white-space:nowrap;font-variant-numeric:tabular-nums;background:#fff;padding:2px 4px}
.clf-rows li[style*="--flip"] .clf-v,.clf-rows li.is-wide .clf-v{left:auto;right:calc(100% - var(--w));transform:translate(-10px,-50%);background:var(--cl-ink);color:#fff}
.clf-rows li.is-soon.is-wide .clf-v{background:#fff;color:var(--cl-ink);border:1px solid var(--cl-ink)}
.clf-rows dl{margin:0;display:grid;grid-template-columns:1fr 1.25fr;border-left:1px solid var(--cl-line);align-self:stretch}
.clf-rows dl > div{padding:14px 16px;display:grid;align-content:center;gap:6px}
.clf-rows dl > div + div{border-left:1px solid var(--cl-line)}
.clf-rows dt{font:600 13px/1 var(--pn-mono);letter-spacing:.1em;text-transform:uppercase;color:var(--fg-muted)}
.clf-rows dd{margin:0;font:600 15px/1.25 var(--pn-mono);color:var(--cl-ink);font-variant-numeric:tabular-nums}
.clf-rows li.is-out{opacity:.34}
.clf-rows li.is-fit{background:linear-gradient(90deg,#ffd23d 0 5px,transparent 5px)}
@media(prefers-reduced-motion:no-preference){html.cl-js .clf-rows li .clf-bar{transform:scaleX(0);transition:transform 1s cubic-bezier(.2,.7,.2,1) .15s}html.cl-js .clf-rows li.in .clf-bar{transform:none}
  html.cl-js .clf-rows li .clf-v{opacity:0;transition:opacity .4s ease .9s}html.cl-js .clf-rows li.in .clf-v{opacity:1}}
/* audience index */
.cld{background-color:#fff}
.cld-cols{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));border:1px solid var(--cl-ink)}
.cld-cols li{position:relative;padding:26px 26px 30px;border-left:1px solid var(--cl-ink);display:flex;flex-direction:column;transition:background .2s,opacity .6s ease,transform .6s cubic-bezier(.2,.7,.2,1)}
.cld-cols li:first-child{border-left:0}
.cld-cols li:hover{background:#ffd23d}
.cld-n{font-family:var(--q-serif);font-weight:800;font-size:clamp(64px,7vw,112px);line-height:.8;letter-spacing:-.06em;color:var(--cl-ink);font-variant-numeric:tabular-nums}
.cld-k{margin:26px 0 0;font:600 13px/1 var(--pn-mono);letter-spacing:.12em;text-transform:uppercase;color:#333a46}
.cld-cols h3{margin:12px 0 0;font-size:clamp(22px,2vw,28px);line-height:1.12;letter-spacing:-.03em;font-weight:800}
.cld-cols h3 a{color:var(--cl-ink);text-decoration:none}
.cld-cols h3 a::after{content:"";position:absolute;inset:0}
.cld-cols ul{list-style:none;margin:18px 0 26px;padding:0;border-top:1px solid var(--cl-ink)}
.cld-cols ul li{display:block;padding:10px 0;border:0;border-bottom:1px solid rgba(11,13,16,.28);font-size:15px;line-height:1.45;color:#22272f;background:none!important}
.cld-go{margin-top:auto;font:700 13px/1 var(--pn-mono);letter-spacing:.08em;text-transform:uppercase;color:var(--cl-ink)}
/* proof ledger */
.clp{background-color:#fff}
.clp-row{margin:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));border-top:2px solid var(--cl-ink);border-bottom:1px solid var(--cl-ink)}
.clp-row > div{padding:26px 26px 28px 0;border-left:1px solid var(--cl-line);padding-left:26px;display:flex;flex-direction:column}
.clp-row > div:first-child{border-left:0;padding-left:0}
.clp-row dd{margin:0;font-family:var(--q-serif);font-weight:800;font-size:clamp(60px,7.2vw,116px);line-height:.86;letter-spacing:-.06em;color:var(--cl-ink);font-variant-numeric:tabular-nums;white-space:nowrap}
.clp-row dt{order:2;margin-top:22px;font-size:18px;font-weight:700;letter-spacing:-.01em;color:var(--cl-ink)}
.clp-row dd.s{order:3;margin-top:6px;font:500 13px/1.4 var(--pn-mono);letter-spacing:.04em;color:var(--fg-muted);white-space:normal}
@media(max-width:1180px){.clh-in{grid-template-columns:minmax(0,1fr);gap:36px;padding-top:44px}.clh-copy{padding:0;box-shadow:none;background:none}.clh{background-image:none!important}.clh-fig{max-width:760px}
  .clf-board{--nw:190px;--dw:240px}}
@media(max-width:900px){
  .cl-head{grid-template-columns:minmax(0,1fr);gap:18px;margin-bottom:28px}
  .clh-title{grid-template-columns:repeat(2,minmax(0,1fr))}.clh-title > div{border-top:1px solid var(--cl-ink)}.clh-title > div:nth-child(-n+2){border-top:0}.clh-title > div:nth-child(odd){border-left:0}.clh-title > div:last-child{grid-column:1/-1}
  .clm-ctl{grid-template-columns:minmax(0,1fr)}
  .clm-t,.clm-t tbody,.clm-t tbody tr,.clm-t td,.clm-t tbody th{display:block;width:auto}
  .clm-t thead{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
  .clm-t tbody tr{position:relative;padding:12px 0 14px 0}
  .clm-t td.n{position:absolute;right:0;top:16px;width:auto;padding:0}
  .clm-t td,.clm-t tbody th{padding:0}
  .clm-t tbody th a{padding-right:34px}
  .clm-t td.f,.clm-t td.k{display:block;margin:6px 0 0 78px}
  .clm-t td.k{font-size:14px}
  .clm-t td.d{margin:8px 0 0 78px}
  .clm-t td.d span{white-space:normal;display:block;margin:0}
  .clf-ctl{grid-template-columns:minmax(0,1fr)}
  .clf-board{--nw:100%;--dw:100%}
  .clf-scale{grid-template-columns:minmax(0,1fr)}.clf-scale em{padding:12px 16px 0}.clf-scale > div{margin:0 46px 0 16px}
  .clf-rows li{grid-template-columns:minmax(0,1fr)}
  .clf-n{padding:14px 16px 8px}
  .clf-track{margin:0 46px 12px 16px}
  .clf-rows dl{border-left:0;border-top:1px solid var(--cl-line)}
  .clf-mark{display:none}
  .cld-cols{grid-template-columns:minmax(0,1fr)}.cld-cols li{border-left:0;border-top:1px solid var(--cl-ink)}.cld-cols li:first-child{border-top:0}
  .clp-row{grid-template-columns:minmax(0,1fr)}.clp-row > div{border-left:0;padding-left:0;border-top:1px solid var(--cl-line)}.clp-row > div:first-child{border-top:0}
}
@media(max-width:560px){
  .clh-plate{padding:58px 46px 58px 52px}
  .clh-dim{font-size:13px;letter-spacing:.04em}.clh-dim b{font-size:13px}
  .clh-dim-t,.clh-dim-b{left:52px;right:46px}.clh-dim-t{top:24px}.clh-dim-b{bottom:24px}
  .clh-dim-l,.clh-dim-r{top:58px;bottom:58px}.clh-dim-l{left:18px}.clh-dim-r{right:14px}
  .clh-fig figcaption{grid-template-columns:minmax(0,1fr)}.clh-fig figcaption > span:first-child{border-right:0;border-bottom:1px solid var(--cl-ink)}.clh-fig figcaption a{border-left:0;border-top:1px solid var(--cl-ink)}
  .clh-cta .q-btn,.clh-cta .q-btn-ghost{width:100%;justify-content:center}
  .clh-k{flex-direction:column;align-items:flex-start}.clh-k span + span{border-left:1px solid var(--cl-ink);border-top:0}
}
@media(prefers-reduced-motion:reduce){html.cl-js .cl-rv{opacity:1;transform:none;transition:none}.clh-prod img,.clm-th img{transition:none}}
"""

HOME_JS = r"""
(function(){
  var d=document,rm=matchMedia('(prefers-reduced-motion: reduce)').matches;
  // reveal
  var rv=[].slice.call(d.querySelectorAll('.cl-rv'));
  if(!('IntersectionObserver' in window)||rm){rv.forEach(function(e){e.classList.add('in')})}
  else{var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});rv.forEach(function(e,i){e.style.transitionDelay=(i%6)*60+'ms';io.observe(e)})}
  // dimension labels: measure the label so the white gap in the line fits it
  [].forEach.call(d.querySelectorAll('.clh-dim'),function(e){var w=0;[].forEach.call(e.children,function(c){w+=(e.className.indexOf('-l')>0||e.className.indexOf('-r')>0)?c.offsetHeight:c.offsetWidth});e.style.setProperty('--lw',(w+7)+'px')});
  // matrix
  var m=d.querySelector('.clm');
  if(m){
    var rows=[].slice.call(m.querySelectorAll('tbody tr')),chips=[].slice.call(m.querySelectorAll('.clm-chips button')),q=m.querySelector('[data-clm-q]'),
        cnt=m.querySelector('[data-clm-count]'),none=m.querySelector('[data-clm-none]'),more=m.querySelector('[data-clm-more]'),f='all';
    var run=function(){
      var s=(q.value||'').trim().toLowerCase(),n=0;
      rows.forEach(function(r){var ok=(f==='all'||r.getAttribute('data-f')===f)&&(!s||r.getAttribute('data-q').indexOf(s)>=0);r.hidden=!ok;if(ok)n++});
      m.classList.toggle('is-filter',f!=='all'||!!s);
      cnt.textContent=n+' of '+rows.length+' products';none.hidden=n>0;
    };
    chips.forEach(function(b){b.addEventListener('click',function(){f=b.getAttribute('data-f');chips.forEach(function(c){var on=c===b;c.classList.toggle('is-on',on);c.setAttribute('aria-pressed',on?'true':'false')});run()})});
    q.addEventListener('input',run);
    more.addEventListener('click',function(){var o=m.classList.toggle('is-open');more.setAttribute('aria-expanded',o?'true':'false');more.textContent=o?more.getAttribute('data-less'):more.getAttribute('data-more')});
    more.setAttribute('data-more',more.textContent);more.setAttribute('data-less','Show fewer products');
  }
  // finder
  var fz=d.querySelector('.clf');
  if(fz){
    var z=fz.querySelector('[data-clf-z]'),out=fz.querySelector('[data-clf-out]'),res=fz.querySelector('[data-clf-res]'),mark=fz.querySelector('[data-clf-mark]'),
        li=[].slice.call(fz.querySelectorAll('.clf-rows li')),all=res.textContent,mx=+fz.getAttribute('data-max')||600,rowsEl=fz.querySelector('.clf-rows');
    li.forEach(function(l){if(+l.getAttribute('data-z')/mx>.62)l.classList.add('is-wide')});
    var size=function(){mark.style.setProperty('--rows-h',rowsEl.offsetHeight+'px')};size();addEventListener('resize',size);
    var upd=function(){
      var v=+z.value;out.textContent=v;
      if(v<=1){fz.classList.remove('is-set');li.forEach(function(l){l.classList.remove('is-out','is-fit')});res.textContent=all;return}
      fz.classList.add('is-set');mark.style.left=(v/mx*100)+'%';
      var fit=[],soon=[];
      li.forEach(function(l){var ok=+l.getAttribute('data-z')>=v,s=l.hasAttribute('data-soon');l.classList.toggle('is-out',!ok);l.classList.toggle('is-fit',ok&&!s);if(ok){(s?soon:fit).push(l.getAttribute('data-name'))}});
      var t=fit.length?(fit.length+(fit.length===1?' panel lists ':' panels list ')+v+' zones or more: '+fit.join(', ')+'.'):'No panel on this sheet lists '+v+' zones.';
      if(soon.length)t+=' The '+soon.join(', ')+' is coming soon and cannot be ordered yet.';
      res.textContent=t;
    };
    z.addEventListener('input',upd);
  }
})();
"""


def post(doc: str, content: dict, page: dict, dslug: str) -> str:
    if OFF or content.get("slug") != SLUG or dslug != "clean":
        return doc
    home = page["file"] == "index.html"
    i = doc.find("</style>")
    if i < 0:
        return doc
    # the hero CSS joins the main block (identical on every page, so it stays in the shared stylesheet); the home CSS is its own block
    doc = (doc[:i] + "\n/* ===== round 3a (scripts/preview_clean.py) ===== */\n" + HERO_CSS + "</style>"
           + ("\n<style>" + HOME_CSS + "</style>" if home else "") + doc[i + len("</style>"):])
    if home:
        doc = doc.replace("</body>", "<script>" + HOME_JS + "</script>\n</body>", 1)
    return doc
