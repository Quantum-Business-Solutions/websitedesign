"""Round 3a, Press direction for the DMP preview: THE SITE IS A MAGAZINE.

Gated twice: the DMP content slug and the Press direction. Section types registered here (pr-cover, pr-lead, pr-quotes,
pr-feature) are only ever named by brands/dmp_press.py, as Press variants, so Showcase and Clean never render them.

  RENDER_PRESS     the cover with its masthead and contents strip, the lead story, the pull-quote spread, the timeline feature
  post(doc, ...)   Press pages only: the CSS for the above, the "paper card on a full-bleed photograph" treatment of the
                   system and industry heroes, numbered section openers on the home page, and a small reveal script.

No-JS and reduced motion render the complete page.
"""
from __future__ import annotations

import os

SLUG = "digital-monitoring-products"
OFF = bool(os.environ.get("DMP_R3A_OFF"))


def _cover(s, ctx):
    E, L, rel, RAW = ctx["E"], ctx["L"], ctx["rel"], ctx["RAW"]
    issue = "".join(f"<span>{E(x)}</span>" for x in s.get("issue", []))
    btns = ""
    if s.get("primary"):
        btns += f'<a class="q-btn" href="{E(L(s["primary"]["href"]))}">{E(s["primary"]["label"])}</a>'
    if s.get("secondary"):
        btns += f'<a class="q-btn-ghost" href="{E(L(s["secondary"]["href"]))}">{E(s["secondary"]["label"])}</a>'
    lines = "".join(f'<li><a href="{E(L(h))}"><span class="n" aria-hidden="true">{i + 1:02d}</span><span class="k">{E(k)}</span><b>{E(t)}</b><span class="d">{E(d)}</span></a></li>'
                    for i, (k, t, d, h) in enumerate(s.get("lines", [])))
    img = s["image"]
    return f'''<section class="q-section prc" id="{E(s.get("id", "hero-layered"))}" aria-labelledby="prc-h1">
<script>document.documentElement.classList.add("pr-js")</script>
<div class="q-container prc-mast"><div class="prc-mast-in"><p class="prc-name" aria-hidden="true">{E(s["name"])}</p><p class="prc-issue">{issue}</p></div></div>
<div class="prc-photo"><img src="{E(rel(img))}" srcset="{E(rel(img.replace("-2100", "-1200")))} 1200w, {E(rel(img))} 2100w" sizes="100vw" alt="{E(s["alt"])}" width="2100" height="900" fetchpriority="high" decoding="async">
<div class="q-container prc-over"><p class="prc-k">{E(s.get("kicker", "Cover story"))}</p>
<h1 class="prc-h1" id="prc-h1">{RAW(s["heading"])}</h1>
<p class="prc-stand">{E(s.get("subhead", ""))}</p>
<div class="pv-btns prc-cta">{btns}</div></div></div>
<div class="q-container"><p class="prc-credit">{E(s.get("credit", ""))}</p>
<nav class="prc-toc" aria-label="In this issue"><p class="prc-toc-h">{E(s.get("toc_label", "Inside"))}</p><ol>{lines}</ol></nav></div>
</section>'''


def _opener(s, ctx, n=""):
    E, RAW = ctx["E"], ctx["RAW"]
    intro = f'<p class="pr-intro">{E(s["intro"])}</p>' if s.get("intro") else ""
    return (f'<header class="pr-open"><p class="pr-kicker">{E(s.get("eyebrow", ""))}</p>'
            f'<h2 class="q-h2" id="{E(s["id"])}-h">{RAW(s["heading"])}</h2>{intro}</header>')


def _lead(s, ctx):
    E, L, rel = ctx["E"], ctx["L"], ctx["rel"]
    items = s["items"]
    thumbs = s.get("thumbs") or []
    k, t, d, lab, h = items[0]
    fig = ""
    if thumbs:
        src, fit = thumbs[0][0], (thumbs[0][1] if len(thumbs[0]) > 1 else "cover")
        fig = (f'<a class="prl-fig prl-{E(fit)}" href="{E(L(h))}" tabindex="-1" aria-hidden="true"><img src="{E(rel(src))}" alt="" width="1200" height="800" loading="lazy" decoding="async"></a>')
    q = s.get("quote")
    quote = (f'<blockquote class="prl-q"><p>{E(q["value"])}</p><p class="prl-qt">{E(q.get("text", ""))}</p><footer>{E(q["source"])}</footer></blockquote>') if q else ""
    side = ""
    for i, (k2, t2, d2, lab2, h2) in enumerate(items[1:]):
        th = ""
        if len(thumbs) > i + 1:
            th = f'<span class="prl-th prl-{E(thumbs[i + 1][1] if len(thumbs[i + 1]) > 1 else "cover")}"><img src="{E(rel(thumbs[i + 1][0].replace("-1200.", "-600.")))}" alt="" width="600" height="400" loading="lazy" decoding="async"></span>'
        side += (f'<li class="pr-rv"><a href="{E(L(h2))}">{th}<span><span class="prl-date">{E(k2)}</span><b>{E(t2)}</b><span class="d">{E(d2)}</span></span></a></li>')
    more = f'<p class="pr-more"><a href="{E(L(s["more"][1]))}">{E(s["more"][0])}</a></p>' if s.get("more") else ""
    return f'''<section class="q-section prl" id="{E(s["id"])}" aria-labelledby="{E(s["id"])}-h">
<div class="q-container">{_opener(s, ctx)}
<div class="prl-grid"><article class="prl-main pr-rv">{fig}
<div class="prl-body"><p class="prl-date">{E(k)}</p><h3><a href="{E(L(h))}">{E(t)}</a></h3>
<p class="prl-stand">{E(s.get("lead_text") or d)}</p>{quote}
<p class="pr-more"><a href="{E(L(h))}">{E(lab)}</a></p></div></article>
<aside class="prl-side" aria-label="{E(s.get("side_label", "Also in the news"))}"><p class="pr-label">{E(s.get("side_label", "Also in the news"))}</p><ol>{side}</ol>{more}</aside></div>
</div></section>'''


def _quotes(s, ctx):
    E, L = ctx["E"], ctx["L"]
    qs = s["quotes"]
    first = qs[0]
    rest = "".join(f'<li class="pr-rv"><blockquote><p>{E(q["value"])}</p><footer><b>{E(q["name"])}</b><span>{E(q["role"])}</span>'
                   f'<a href="{E(L(q["href"]))}">{E(q["from"])}</a></footer></blockquote></li>' for q in qs[1:])
    return f'''<section class="q-section prq" id="{E(s["id"])}" aria-labelledby="{E(s["id"])}-h">
<div class="q-container"><header class="prq-head"><p class="pr-kicker">{E(s.get("eyebrow", ""))}</p><h2 class="prq-h" id="{E(s["id"])}-h">{E(s["heading"])}</h2></header>
<div class="prq-grid"><figure class="prq-main pr-rv"><span class="prq-mark" aria-hidden="true">&ldquo;</span>
<blockquote><p>{E(first["value"])}</p><p class="prq-more">{E(first.get("text", ""))}</p></blockquote>
<figcaption><b>{E(first["name"])}</b><span>{E(first["role"])}</span><a href="{E(L(first["href"]))}">{E(first["from"])}</a></figcaption></figure>
<ol class="prq-side">{rest}</ol></div>
</div></section>'''


def _feature(s, ctx):
    E, L, rel = ctx["E"], ctx["L"], ctx["rel"]
    items = s.get("items", [])
    lis = ""
    for i, it in enumerate(items):
        img = it[3] if len(it) > 3 else ""
        pic = f'<span class="prf-pic"><img src="{E(rel(img))}" alt="" width="600" height="360" loading="lazy" decoding="async"></span>' if img else ""
        lis += (f'<li class="pr-rv{" has-pic" if img else ""}"><span class="prf-y">{E(it[0])}</span><i class="prf-dot" aria-hidden="true"></i>{pic}'
                f'<h3>{E(it[1])}</h3><p>{E(it[2])}</p></li>')
    more = f'<p class="pr-more"><a href="{E(L(s["more"][1]))}">{E(s["more"][0])}</a></p>' if s.get("more") else ""
    base = s["cover"].replace("-1280.jpg", "")
    return f'''<section class="q-section pnf prf" id="{E(s.get("id", "story"))}" aria-labelledby="prf-h">
<div class="pnf-cover"><img src="{E(rel(s["cover"]))}" srcset="{E(rel(base + "-800.jpg"))} 800w, {E(rel(s["cover"]))} 1280w, {E(rel(base + "-1920.jpg"))} 1920w" sizes="100vw" alt="" width="1920" height="1086" loading="lazy" decoding="async">
<div class="pnf-over"><div class="q-container"><p class="pnf-k">{E(s.get("kicker", "Feature"))} <span>{E(s.get("eyebrow", ""))}</span></p>
<h2 class="q-h2 pnf-h" id="prf-h">{E(s["heading"])}</h2>
<p class="prf-span" aria-hidden="true"><span>{E(items[0][0])}</span><i></i><span>{E(items[-1][0])}</span></p></div></div>
<p class="pv-envcap">{E(s.get("cover_caption", "Illustrative scene"))}</p></div>
<div class="q-container"><p class="pnf-intro">{E(s.get("intro", ""))}</p>
<ol class="prf-line">{lis}</ol>{more}</div></section>'''


RENDER_PRESS = {"pr-cover": _cover, "pr-lead": _lead, "pr-quotes": _quotes, "pr-feature": _feature}


HERO_CSS = r"""
/* ===== round 3a, Press: system and industry heroes as a section opener, a paper card on a full-bleed photograph ===== */
html[data-dir="press"] .pv-lh:has(> .bg.env){--lh-bg:#14110c;border-top:0;border-bottom:1px solid var(--pr-ink)}
html[data-dir="press"] .pv-lh:has(> .bg.env) :is(.net,.glow){display:none}
html[data-dir="press"] .pv-lh:has(> .bg.env) > .bg.env img{opacity:1;filter:sepia(.18) saturate(.92) contrast(1.02)}
html[data-dir="press"] .pv-lh:has(> .bg.env) > .bg.env::after{background:linear-gradient(180deg,rgba(20,17,12,.28) 0%,rgba(20,17,12,.06) 30%,rgba(20,17,12,.5) 100%)}
html[data-dir="press"] .pv-lh:has(> .bg.env) .q-container{grid-template-columns:minmax(0,1.08fr) minmax(0,.92fr);gap:64px;align-items:end;padding-top:56px;padding-bottom:0}
html[data-dir="press"] .pv-lh:has(> .bg.env) .q-container > div:first-child{position:relative;background:#f7f4ec;color:var(--pr-ink);padding:40px 48px 44px;border-top:6px solid var(--pr-ink);box-shadow:0 -1px 0 #f7f4ec,0 30px 80px rgba(0,0,0,.35)}
html[data-dir="press"] .pv-lh:has(> .bg.env) .q-container > div:first-child::before{content:"";position:absolute;left:48px;right:48px;top:8px;border-top:1px solid var(--pr-ink)}
html[data-dir="press"] .pv-lh:has(> .bg.env) .q-eyebrow{color:var(--pr-ink);border-top:0;padding-top:10px}
html[data-dir="press"] .pv-lh:has(> .bg.env) .q-eyebrow::before{background:var(--sys,#ffd23d);width:12px;height:12px;border-radius:50%;box-shadow:0 0 0 1px var(--pr-ink)}
html[data-dir="press"] .pv-lh:has(> .bg.env) .q-h1{color:var(--pr-ink);margin-top:16px;font-size:clamp(38px,4.2vw,64px);line-height:1.03}
html[data-dir="press"] .pv-lh:has(> .bg.env) .q-h1 em{color:var(--accent-ink);font-style:italic}
html[data-dir="press"] .pv-lh:has(> .bg.env) .q-lead{color:#3a342a;font-family:var(--q-serif);font-size:19px;line-height:1.6;max-width:none}
html[data-dir="press"] .pv-lh:has(> .bg.env) .q-lead::first-letter{font-family:var(--q-serif);float:left;font-size:3.5em;line-height:.8;padding:.07em .1em 0 0;font-weight:700;color:var(--pr-ink)}
html[data-dir="press"] .pv-lh:has(> .bg.env) .pv-btns .q-btn{background:var(--pr-ink);color:#fff;border-color:var(--pr-ink)}
html[data-dir="press"] .pv-lh:has(> .bg.env) .pv-btns .q-btn:hover{background:#ffd23d;color:var(--pr-ink);border-color:var(--pr-ink)}
html[data-dir="press"] .pv-lh:has(> .bg.env) .pv-btns .q-btn-ghost{color:var(--pr-ink);border-color:var(--pr-ink)}
html[data-dir="press"] .pv-lh:has(> .bg.env) .lane .k{color:#5a5245}
html[data-dir="press"] .pv-lh:has(> .bg.env) .lane a{min-height:44px;color:var(--pr-ink);border-color:rgba(23,20,15,.5);background:transparent}
html[data-dir="press"] .pv-lh:has(> .bg.env) .lane a:hover{background:var(--pr-ink);color:#fff;border-color:var(--pr-ink)}
html[data-dir="press"] .pv-lh:has(> .bg.env) .pv-hero-stats{border-top:3px double var(--pr-ink);margin-top:34px}
html[data-dir="press"] .pv-lh:has(> .bg.env) .pv-hero-stats > div{border-left-color:rgba(23,20,15,.3)}
html[data-dir="press"] .pv-lh:has(> .bg.env) .pv-hero-stats b{color:var(--pr-ink);font-family:var(--q-serif);font-style:italic;font-weight:600}
html[data-dir="press"] .pv-lh:has(> .bg.env) .pv-hero-stats span{color:#5a5245}
html[data-dir="press"] .pv-lh:has(> .bg.env) .stack{align-self:end;padding-bottom:56px}
html[data-dir="press"] .pv-lh:has(> .bg.env) .fcard,html[data-dir="press"] .pv-lh:has(> .bg.env) .fcard.b{background:#f7f4ec;color:var(--pr-ink);border:0;border-top:3px double var(--pr-ink);border-radius:0;backdrop-filter:none;-webkit-backdrop-filter:none;box-shadow:0 24px 60px rgba(0,0,0,.4)}
html[data-dir="press"] .pv-lh:has(> .bg.env) .fcard .k,html[data-dir="press"][data-sys] .pv-lh:has(> .bg.env) .fcard .k{color:#5a5245}
html[data-dir="press"] .pv-lh:has(> .bg.env) .fcard p{color:#3a342a}
html[data-dir="press"] .pv-lh:has(> .bg.env) .fcard p.t{color:var(--pr-ink);font-family:var(--q-serif);font-size:24px;font-weight:600}
html[data-dir="press"] .pv-lh:has(> .bg.env) .fcard li::before,html[data-dir="press"][data-sys] .pv-lh:has(> .bg.env) .fcard li::before{width:9px;height:9px;margin-top:6px;background:var(--pr-ink);box-shadow:none}
html[data-dir="press"] .pv-lh:has(> .bg.env) .fcard .go{background:var(--pr-ink);color:#fff}
html[data-dir="press"] .pv-lh:has(> .bg.env) .fcard .go:hover{background:#ffd23d;color:var(--pr-ink)}
html[data-dir="press"] .pv-lh:has(> .bg.env) .hero3d.lf-float::before,html[data-dir="press"] .pv-lh:has(> .bg.env) .hero3d.lf-float::after{display:none}
html[data-dir="press"] .pv-lh:has(> .bg.env) > .pv-envcap{right:20px;bottom:14px;background:none;color:#fff;font:italic 500 14px/1.2 var(--q-serif);letter-spacing:.01em;text-shadow:0 1px 8px rgba(0,0,0,.9),0 0 2px rgba(0,0,0,.9)}
@media(prefers-reduced-motion:no-preference){html[data-dir="press"] .pv-lh:has(> .bg.env) .q-container > div:first-child{animation:pr-rise .9s cubic-bezier(.2,.7,.2,1) both}}
@keyframes pr-rise{from{opacity:0;transform:translateY(28px)}to{opacity:1;transform:none}}
@media(max-width:1024px){
  html[data-dir="press"] .pv-lh:has(> .bg.env) .q-container{grid-template-columns:minmax(0,1fr);gap:24px;padding-top:150px;padding-bottom:40px}
  html[data-dir="press"] .pv-lh:has(> .bg.env) > .bg.env::after{background:linear-gradient(180deg,rgba(20,17,12,.2) 0%,rgba(20,17,12,.2) 160px,rgba(20,17,12,.88) 520px,#14110c 100%)}
  html[data-dir="press"] .pv-lh:has(> .bg.env) > .bg.env img{opacity:1;object-position:50% 0}
  html[data-dir="press"] .pv-lh:has(> .bg.env) .stack{padding-bottom:0}
  html[data-dir="press"] .pv-lh:has(> .bg.env) > .pv-envcap{top:14px;bottom:auto}
}
@media(max-width:767px){
  html[data-dir="press"] .pv-lh:has(> .bg.env) .q-container{padding-top:120px}
  html[data-dir="press"] .pv-lh:has(> .bg.env) .q-container > div:first-child{padding:30px 22px 30px}
  html[data-dir="press"] .pv-lh:has(> .bg.env) .q-container > div:first-child::before{left:22px;right:22px}
}
"""

HOME_CSS = r"""
/* ===== round 3a, Press home: the magazine ===== */
html:not(.pr-js) .pr-js-only{display:none!important}
html.pr-js .pr-rv{opacity:0;transform:translateY(18px);transition:opacity .8s ease,transform .8s cubic-bezier(.2,.7,.2,1)}
html.pr-js .pr-rv.in{opacity:1;transform:none}
.pr-kicker{margin:0;font:700 13px/1 var(--q-sans);letter-spacing:.24em;text-transform:uppercase;color:var(--fg)}
.pr-label{margin:0 0 6px;padding-bottom:12px;border-bottom:1px solid var(--fg);font:700 13px/1 var(--q-sans);letter-spacing:.22em;text-transform:uppercase;color:var(--fg)}
.pr-more{margin:20px 0 0}
.pr-more a{display:inline-flex;align-items:center;min-height:44px;font:700 15px/1 var(--q-sans);color:var(--fg);text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:6px}
.pr-more a:hover{text-decoration-thickness:2px;text-decoration-color:#b88d00}
.pr-open{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:14px 56px;align-items:end;margin-bottom:38px}
.pr-open .pr-kicker{grid-column:1/-1}
.pr-open .q-h2{margin:0;font-size:clamp(36px,4.4vw,68px);line-height:1}
.pr-intro{margin:0;font-family:var(--q-serif);font-style:italic;font-size:20px;line-height:1.5;color:var(--fg-muted)}
/* numbered openers on the existing bands */
html[data-dir="press"].pn-home main{counter-reset:prsec}
html[data-dir="press"].pn-home main > .q-section:not(.prc){counter-increment:prsec}
html[data-dir="press"].pn-home main > .q-section:not(.pv-lh) :is(.q-eyebrow,.pr-kicker,.pnf-k)::before{content:counter(prsec,decimal-leading-zero);display:inline-block;width:auto;height:auto;background:none;border-radius:0;margin-right:14px;
  font:italic 500 30px/1 var(--q-serif);letter-spacing:0;color:inherit;vertical-align:-5px;text-transform:none}
html[data-dir="press"].pn-home main > .q-section .q-eyebrow{align-items:baseline}
/* cover */
.prc{padding:0!important;background:var(--bg)}
.prc-mast{padding-top:26px;padding-bottom:0}.prc-mast-in{container-type:inline-size}
.prc-name{margin:0;padding:0 0 14px;border-bottom:1px solid var(--fg);font-family:var(--q-serif);font-weight:900;font-size:clamp(15px,4.4vw,104px);font-size:clamp(15px,5.7cqw,130px);line-height:.9;letter-spacing:-.02em;text-transform:uppercase;color:var(--fg);white-space:nowrap;text-align:center}
.prc-issue{margin:0;padding:11px 0;border-bottom:3px double var(--fg);display:flex;justify-content:space-between;gap:8px 24px;flex-wrap:wrap;font:700 13px/1.3 var(--q-sans);letter-spacing:.2em;text-transform:uppercase;color:var(--fg)}
.prc-photo{position:relative;margin-top:22px;min-height:min(66vh,680px);display:flex;align-items:flex-end;overflow:hidden;background:#14110c;color:#fff}
.prc-photo > img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:62% 50%;filter:sepia(.14) saturate(.95)}
.prc-photo::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(14,12,8,.86) 0%,rgba(14,12,8,.62) 36%,rgba(14,12,8,.08) 68%),linear-gradient(180deg,rgba(14,12,8,0) 40%,rgba(14,12,8,.66) 100%)}
@media(prefers-reduced-motion:no-preference){.prc-photo > img{animation:prc-kb 26s ease-out both}
  html.pr-js .prc-over > *{animation:pr-rise .9s cubic-bezier(.2,.7,.2,1) both}html.pr-js .prc-over > :nth-child(2){animation-delay:.1s}html.pr-js .prc-over > :nth-child(3){animation-delay:.22s}html.pr-js .prc-over > :nth-child(4){animation-delay:.32s}
  html.pr-js .prc-name{animation:prc-name 1.1s cubic-bezier(.2,.7,.2,1) both}}
@keyframes prc-kb{from{transform:scale(1.08)}to{transform:none}}
@keyframes prc-name{from{opacity:0;letter-spacing:.06em}to{opacity:1;letter-spacing:-.02em}}
@keyframes pr-rise{from{opacity:0;transform:translateY(28px)}to{opacity:1;transform:none}}
.prc-over{position:relative;z-index:1;width:100%;padding-top:84px;padding-bottom:52px}
.prc-k{display:inline-block;margin:0 0 22px;padding:8px 12px;background:#ffd23d;color:#17140f;font:800 13px/1 var(--q-sans);letter-spacing:.22em;text-transform:uppercase}
.prc-h1{margin:0;max-width:13ch;font-family:var(--q-serif);font-weight:600;font-size:clamp(46px,6.6vw,112px);line-height:.96;letter-spacing:-.02em;color:#fff;text-wrap:balance}
.prc-h1 em{font-style:italic;font-weight:500;color:#ffd23d}
.prc-stand{margin:26px 0 0;max-width:46ch;font-family:var(--q-serif);font-size:clamp(18px,1.5vw,22px);line-height:1.5;color:#f3eee2}
.prc-cta{margin-top:28px;display:flex;flex-wrap:wrap;gap:12px}
.prc .prc-cta .q-btn{background:#ffd23d;color:#17140f;border-color:#ffd23d;min-height:52px}
.prc .prc-cta .q-btn:hover{background:#fff;border-color:#fff}
.prc .prc-cta .q-btn-ghost{color:#fff;border:1px solid rgba(255,255,255,.7);min-height:52px;padding:0 22px;display:inline-flex;align-items:center;text-decoration:none;font-weight:700}
.prc .prc-cta .q-btn-ghost:hover{background:#fff;color:#17140f}
.prc-credit{margin:10px 0 0;text-align:right;font:italic 400 14px/1.3 var(--q-serif);color:var(--fg-muted)}
.prc-toc{margin-top:18px;padding-bottom:64px;border-top:3px double var(--fg);padding-top:18px}
.prc-toc-h{margin:0 0 20px;font:700 13px/1 var(--q-sans);letter-spacing:.24em;text-transform:uppercase;color:var(--fg)}
.prc-toc ol{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:0}
.prc-toc li{min-width:0}.prc-toc li:first-child a{padding-left:0}
.prc-toc a{display:grid;grid-template-columns:minmax(0,1fr);gap:6px;padding:2px 22px 6px;min-height:44px;color:var(--fg);text-decoration:none;height:100%;align-content:start}
.prc-toc .n{font:italic 500 clamp(52px,5vw,80px)/.9 var(--q-serif);transform-origin:0 100%;color:var(--fg);transition:color .25s,transform .35s cubic-bezier(.2,.7,.2,1)}
.prc-toc a:hover .n{color:#a67f00;transform:translateY(-4px)}
.prc-toc .k{font:700 13px/1.2 var(--q-sans);letter-spacing:.18em;text-transform:uppercase;color:var(--fg-muted);padding-top:12px;border-top:1px solid var(--fg);margin-top:8px}
.prc-toc b{font-family:var(--q-serif);font-weight:600;font-size:20px;line-height:1.2}
.prc-toc a:hover b{text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:4px}
.prc-toc .d{font-size:14.5px;line-height:1.45;color:var(--fg-muted)}
/* lead story */
.prl-grid{display:grid;grid-template-columns:minmax(0,1.75fr) minmax(0,1fr);gap:48px;border-top:1px solid var(--fg);padding-top:30px}
.prl-main{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.05fr);gap:36px;align-items:start}
.prl-fig{display:block;background:#ece6d6;aspect-ratio:4/5;overflow:hidden}
.prl-fig img{width:100%;height:100%;object-fit:cover;transition:transform 1.2s cubic-bezier(.2,.7,.2,1)}
.prl-fig.prl-contain{display:grid;place-items:center;padding:12%;background:radial-gradient(circle at 50% 42%,#fbf8f0,#e6dfcc)}
.prl-fig.prl-contain img{object-fit:contain;height:auto;filter:drop-shadow(0 24px 26px rgba(23,20,15,.28))}
.prl-main:hover .prl-fig img{transform:scale(1.04)}
.prl-date{display:block;margin:0;font:700 13px/1.2 var(--q-sans);letter-spacing:.18em;text-transform:uppercase;color:var(--fg-muted)}
.prl-body h3{margin:14px 0 0;font-family:var(--q-serif);font-weight:600;font-size:clamp(28px,2.9vw,46px);line-height:1.06;letter-spacing:-.012em}
.prl-body h3 a{color:var(--fg);text-decoration:none}
.prl-body h3 a:hover{text-decoration:underline;text-decoration-thickness:2px;text-underline-offset:6px}
.prl-stand{margin:20px 0 0;font-family:var(--q-serif);font-size:19px;line-height:1.62;color:#3a342a}
.prl-stand::first-letter{font-family:var(--q-serif);float:left;font-size:4.1em;line-height:.78;padding:.08em .1em 0 0;font-weight:700;color:var(--fg)}
.prl-q{margin:26px 0 0;padding:16px 0 0;border-top:3px double var(--fg)}
.prl-q p{margin:0;font:italic 500 clamp(22px,2vw,28px)/1.25 var(--q-serif);color:var(--fg)}
.prl-q p.prl-qt{margin-top:10px;font:400 17px/1.6 var(--q-serif);font-style:normal;color:#3a342a}.prl-q footer{margin-top:10px;font:600 13px/1.4 var(--q-sans);letter-spacing:.08em;text-transform:uppercase;color:var(--fg-muted)}
.prl-side ol{list-style:none;margin:0;padding:0}
.prl-side li{border-bottom:1px solid var(--border)}
.prl-side li a{display:grid;grid-template-columns:96px minmax(0,1fr);gap:16px;padding:18px 0;color:var(--fg);text-decoration:none;align-items:start}
.prl-th{display:block;width:96px;height:96px;background:#ece6d6;overflow:hidden}
.prl-th img{width:100%;height:100%;object-fit:cover;transition:transform .8s cubic-bezier(.2,.7,.2,1)}
.prl-side li a:hover .prl-th img{transform:scale(1.07)}
.prl-side b{display:block;margin-top:8px;font-family:var(--q-serif);font-weight:600;font-size:21px;line-height:1.2}
.prl-side li a:hover b{text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:4px}
.prl-side .d{display:block;margin-top:6px;font-size:15px;line-height:1.5;color:var(--fg-muted)}
/* pull-quote spread */
.prq{background:#17140f!important;color:#f7f4ec;padding-top:104px!important;padding-bottom:104px!important;position:relative;overflow:hidden}
.prq-head{display:flex;align-items:baseline;justify-content:space-between;gap:20px;flex-wrap:wrap;padding-bottom:16px;border-bottom:3px double rgba(247,244,236,.75)}
.prq .pr-kicker{color:#ffd23d}
.prq-h{margin:0;font:italic 500 clamp(22px,2vw,28px)/1.2 var(--q-serif);color:#f7f4ec}
.prq-grid{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(0,1fr);gap:72px;margin-top:54px;align-items:start}
.prq-main{position:relative;margin:0;padding-left:0}
.prq-mark{display:block;height:.5em;font:italic 700 clamp(160px,17vw,280px)/1 var(--q-serif);color:#ffd23d;margin:0 0 26px -.04em}
.prq-main blockquote{margin:0}
.prq-main blockquote p:first-child{margin:0;font:italic 500 clamp(30px,3.7vw,60px)/1.12 var(--q-serif);letter-spacing:-.012em;color:#fff;text-wrap:balance}
.prq-more{margin:26px 0 0;max-width:54ch;font-family:var(--q-serif);font-size:19px;line-height:1.6;color:#d9d2c2}
.prq-main figcaption,.prq-side footer{display:grid;gap:5px;margin-top:26px;padding-top:16px;border-top:1px solid rgba(247,244,236,.4)}
.prq-main figcaption b,.prq-side footer b{font:700 15px/1.2 var(--q-sans);letter-spacing:.14em;text-transform:uppercase;color:#fff}
.prq-main figcaption span,.prq-side footer span{font:italic 400 16px/1.35 var(--q-serif);color:#d9d2c2}
.prq-main figcaption a,.prq-side footer a{justify-self:start;display:inline-flex;align-items:center;min-height:44px;font:600 14.5px/1.3 var(--q-sans);color:#ffd23d;text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:5px}
.prq-main figcaption a:hover,.prq-side footer a:hover{color:#fff}
.prq-side{list-style:none;margin:0;padding:0;display:grid;gap:40px}
.prq-side blockquote{margin:0}
.prq-side blockquote p{margin:0;font:italic 500 clamp(21px,1.75vw,26px)/1.3 var(--q-serif);color:#f7f4ec}
.prq-side footer{margin-top:16px;padding-top:12px}
/* timeline feature */
.prf .pnf-h{max-width:18ch}
.prf-span{margin:34px 0 0;display:flex;align-items:center;gap:20px;max-width:560px;font:italic 500 clamp(30px,3vw,46px)/1 var(--q-serif);color:#ffd23d}
.prf-span i{flex:1;height:1px;background:rgba(255,255,255,.7)}
.prf-line{list-style:none;margin:0;padding:54px 0 0;display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:0;position:relative}
.prf-line::before{content:"";position:absolute;left:0;right:0;top:calc(54px + clamp(40px,4.1vw,62px) + 22px);border-top:1px solid var(--fg)}
.prf-line li{position:relative;padding:0 22px 0 0;min-width:0}
.prf-line li:nth-child(even){padding-top:0}
.prf-y{display:block;white-space:nowrap;font:italic 500 clamp(40px,4.1vw,62px)/1 var(--q-serif);letter-spacing:-.03em;color:var(--fg);transition:color .3s}
.prf-line li:hover .prf-y{color:#a67f00}
.prf-dot{display:block;width:11px;height:11px;border-radius:50%;background:#ffd23d;box-shadow:0 0 0 1px var(--fg);margin:17px 0 22px}
.prf-pic{display:block;aspect-ratio:5/3;overflow:hidden;margin:0 0 16px;background:#ece6d6}
.prf-pic img{width:100%;height:100%;object-fit:cover;filter:sepia(.3) saturate(.8);transition:filter .5s,transform .9s cubic-bezier(.2,.7,.2,1)}
.prf-line li:hover .prf-pic img{filter:none;transform:scale(1.05)}
.prf-line h3{margin:0 0 8px;font-family:var(--q-serif);font-weight:600;font-size:22px;line-height:1.2;color:var(--fg)}
.prf-line p{margin:0;font-size:15.5px;line-height:1.6;color:var(--fg-muted)}
.prf .pr-more{margin-top:34px}
@media(max-width:1100px){
  .prc-toc ol{grid-template-columns:repeat(2,minmax(0,1fr));gap:26px 0}.prc-toc li:nth-child(odd) a{padding-left:0}
  .prl-grid{grid-template-columns:minmax(0,1fr);gap:40px}
  .prq-grid{grid-template-columns:minmax(0,1fr);gap:48px}
  .prf-line{grid-template-columns:repeat(3,minmax(0,1fr));gap:44px 0}.prf-line::before{display:none}.prf-line li{border-top:1px solid var(--fg);padding-top:18px}
}
@media(max-width:767px){
  .pr-open{grid-template-columns:minmax(0,1fr);margin-bottom:26px}
  .prc-mast{padding-top:16px}.prc-issue{letter-spacing:.12em;justify-content:flex-start}.prc-issue span:nth-child(n+2){display:none}
  .prc-photo{margin-top:14px;min-height:600px}.prc-photo > img{object-position:70% 50%}
  .prc-photo::after{background:linear-gradient(180deg,rgba(14,12,8,.3) 0%,rgba(14,12,8,.55) 38%,rgba(14,12,8,.93) 100%)}
  .prc-over{padding-top:150px;padding-bottom:36px}
  .prc-cta .q-btn,.prc-cta .q-btn-ghost{width:100%;justify-content:center}
  .prc-credit{text-align:left}
  .prc-toc{padding-bottom:44px}.prc-toc ol{grid-template-columns:minmax(0,1fr);gap:0}.prc-toc a{padding:14px 0;grid-template-columns:64px minmax(0,1fr);gap:2px 14px}.prc-toc .n{grid-row:1/4;font-size:48px}.prc-toc .k{margin-top:0}
  .prl-main{grid-template-columns:minmax(0,1fr);gap:22px}.prl-fig{aspect-ratio:4/3}
  .prq{padding-top:64px!important;padding-bottom:64px!important}.prq-grid{margin-top:34px}
  .prf-line{grid-template-columns:minmax(0,1fr);gap:30px;padding-top:34px}
  .prf-line li{display:grid;grid-template-columns:auto minmax(0,1fr);gap:0 18px;padding-right:0}
  .prf-y{grid-row:1/4;font-size:44px;min-width:2.4ch}.prf-dot{display:none}.prf-pic{grid-column:2}.prf-line h3,.prf-line p{grid-column:2}
}
@media(prefers-reduced-motion:reduce){html.pr-js .pr-rv{opacity:1;transform:none;transition:none}.prl-fig img,.prl-th img,.prf-pic img,.prc-toc .n{transition:none}}
"""

HOME_JS = r"""
(function(){
  var d=document,rm=matchMedia('(prefers-reduced-motion: reduce)').matches,rv=[].slice.call(d.querySelectorAll('.pr-rv'));
  if(!('IntersectionObserver' in window)||rm){rv.forEach(function(e){e.classList.add('in')});return}
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});
  rv.forEach(function(e,i){e.style.transitionDelay=(i%6)*70+'ms';io.observe(e)});
})();
"""


def post(doc: str, content: dict, page: dict, dslug: str) -> str:
    if OFF or content.get("slug") != SLUG or dslug != "press":
        return doc
    home = page["file"] == "index.html"
    i = doc.find("</style>")
    if i < 0:
        return doc
    # the hero CSS joins the main block (identical on every page, so it stays in the shared stylesheet); the home CSS is its own block
    doc = (doc[:i] + "\n/* ===== round 3a (scripts/preview_press.py) ===== */\n" + HERO_CSS + "</style>"
           + ("\n<style>" + HOME_CSS + "</style>" if home else "") + doc[i + len("</style>"):])
    if home:
        doc = doc.replace("</body>", "<script>" + HOME_JS + "</script>\n</body>", 1)
    return doc
