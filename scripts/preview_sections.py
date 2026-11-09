"""Additional section types for scripts/preview.py, mirroring the Quantum modules a client site
would use in HubSpot: video, testimonial slider, heritage timeline, tabs, a print-cost estimator,
a lease/rent/buy comparison, an "is this you" checklist, values, leadership, sticky mobile CTA,
resource cards, and the anatomy of a long-form post (header, table of contents, chapters, pull
quote, related posts). Each renderer takes (section, ctx) and returns HTML; ctx carries E, RAW,
rel (asset path), L (internal link path), brand, and sec_open.

Rules (design/guardrails.md): no em dashes, nothing under 13px, tap targets 44px, no opacity on
text, grids that balance, real content only.
"""
from __future__ import annotations

import json

EXTRA_CSS = r'''
/* ===== video ===== */
.pv-video{position:relative;aspect-ratio:16/9;border-radius:calc(var(--radius) + 6px);overflow:hidden;border:1px solid var(--border);background:#000}
.pv-video iframe,.pv-video video{position:absolute;inset:0;width:100%;height:100%;border:0;display:block}
.pv-video-wrap{max-width:1000px;margin:0 auto}
.pv-video > img{width:100%;height:100%;object-fit:cover;display:block;filter:brightness(.82)}
.pv-play{position:absolute;inset:0;margin:auto;width:84px;height:84px;border-radius:50%;border:0;background:var(--q-gold);color:var(--cta-fg);cursor:pointer;display:grid;place-items:center;box-shadow:0 18px 40px rgba(0,0,0,.35);transition:transform .2s}.pv-play:hover{transform:scale(1.06)}.pv-play span{display:block;width:0;height:0;border-style:solid;border-width:14px 0 14px 24px;border-color:transparent transparent transparent currentColor;margin-left:6px}.pv-play:focus-visible{outline:3px solid #fff;outline-offset:3px}
.pv-video-cap{font-size:14px;color:var(--fg-muted);text-align:center;margin:14px 0 0}
.pv-hero-video{position:relative;overflow:hidden;background:var(--stage);color:#fff}
.pv-hero-video video,.pv-hero-video .pv-poster{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.9}
.pv-hero-video .q-container{position:relative;z-index:1;padding-top:96px;padding-bottom:96px}
.pv-hero-video .q-h1,.pv-hero-video .q-lead{color:#fff}
.pv-hero-video::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(6,12,22,.82) 0%,rgba(6,12,22,.55) 55%,rgba(6,12,22,.2) 100%);pointer-events:none}
.pv-hero-video .q-h1 em{color:var(--stage-accent,var(--q-gold));font-style:normal}
.pv-hero-video .q-eyebrow{color:var(--stage-accent,var(--q-gold))}.pv-hero-video .q-eyebrow::before{background:var(--stage-accent,var(--q-gold))}
.pv-hero-video .q-btn-ghost{color:#fff}
.pv-hero-video .pv-hero-note{color:rgba(255,255,255,.78)}
/* ===== testimonials ===== */
.pv-tst{display:grid;grid-template-columns:repeat(2,1fr);gap:20px}
.pv-tst figure{margin:0;background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:28px;display:flex;flex-direction:column;gap:16px}
.pv-tst blockquote{margin:0;font-family:var(--q-serif);font-size:19px;line-height:1.5;color:var(--fg)}
.pv-tst figcaption{font-size:14px;color:var(--fg-muted)}.pv-tst figcaption b{display:block;color:var(--fg);font-weight:600}
.pv-tst-feature{grid-template-columns:1.25fr 1fr;align-items:start}
.pv-tst-feature figure.lead{background:none;border:0;padding:0}.pv-tst-feature figure.lead blockquote{font-size:clamp(24px,2.4vw,32px);line-height:1.35;letter-spacing:-.01em}
.pv-tst-feature figure.lead blockquote::before{content:"\201C";display:block;color:var(--accent-ink);font-size:72px;line-height:.5;margin-bottom:18px}
.pv-tst-letters{list-style:none;margin:0;padding:0}.pv-tst-letters li{padding:18px 0;border-top:1px solid var(--border)}.pv-tst-letters li:last-child{border-bottom:1px solid var(--border)}
.pv-tst-letters blockquote{margin:0;font-size:15.5px;line-height:1.55;color:var(--fg)}.pv-tst-letters footer{margin-top:8px;font-size:13.5px;color:var(--fg-muted)}.pv-tst-letters footer b{color:var(--fg);font-weight:600}
@media(max-width:1024px){.pv-tst-feature{grid-template-columns:1fr}}
/* ===== timeline ===== */
.pv-tl{display:grid;grid-template-columns:repeat(4,1fr);gap:28px;position:relative;margin-top:48px}
.pv-tl::before{content:"";position:absolute;left:0;right:0;top:9px;height:1px;background:var(--border)}
.pv-tl > div{position:relative;padding-top:30px}
.pv-tl > div::before{content:"";position:absolute;left:0;top:2px;width:15px;height:15px;border-radius:50%;background:var(--q-gold);border:3px solid var(--bg)}
.pv-tl .y{font-family:var(--q-serif);font-size:30px;color:var(--accent-ink);line-height:1}
.pv-tl h3{font-size:17px;font-weight:600;margin:10px 0 6px;color:var(--fg)}
.pv-tl p{font-size:14.5px;line-height:1.6;color:var(--fg-muted);margin:0}
/* ===== tabs ===== */
.pv-tabs [role=tablist]{display:flex;gap:12px;flex-wrap:wrap;border-bottom:1px solid var(--border);margin-bottom:28px}
.pv-tabs [role=tab]{min-height:44px;font-size:15px}
.pv-tabs [role=tabpanel]{display:grid;grid-template-columns:1.1fr .9fr;gap:40px;align-items:start}
.pv-tabs [role=tabpanel][hidden]{display:none}
.pv-tabs h3{font-family:var(--q-serif);font-size:28px;margin:0 0 12px;color:var(--fg)}
.pv-tabs p{font-size:16px;line-height:1.7;color:var(--fg-muted);margin:0 0 14px}
.pv-tabs ul{margin:0;padding-left:20px;color:var(--fg);line-height:1.8}.pv-tabs ul li::marker{color:var(--accent-ink)}
.pv-tabs .img{aspect-ratio:4/3;border-radius:var(--radius);overflow:hidden;border:1px solid var(--border);background:var(--bg-alt)}.pv-tabs .img img{width:100%;height:100%;object-fit:cover;display:block}
/* ===== calculator ===== */
.pv-calc{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:start}
.pv-calc .in{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:28px;display:grid;gap:18px}
.pv-calc label{display:block;font-size:14px;color:var(--fg);font-weight:600;margin-bottom:8px}
.pv-calc .row{display:flex;align-items:center;gap:14px}
.pv-calc input[type=range]{flex:1;accent-color:var(--q-gold);min-height:44px;font-size:16px}
.pv-calc output{font-variant-numeric:tabular-nums;min-width:90px;text-align:right;font-weight:600;color:var(--fg)}
.pv-calc .out{display:grid;gap:14px}
.pv-calc .big{background:var(--stage);color:#fff;border-radius:var(--radius);padding:28px}
.pv-calc .big .k{font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:rgba(255,255,255,.72)}
.pv-calc .big .v{font-family:var(--q-serif);font-size:52px;line-height:1.05;margin-top:8px;font-variant-numeric:tabular-nums}
.pv-calc .big .d{font-size:14px;color:rgba(255,255,255,.78);margin-top:8px}
.pv-calc .small{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.pv-calc .small > div{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:18px}
.pv-calc .small .k{font-size:13px;color:var(--fg-muted)}.pv-calc .small .v{font-family:var(--q-serif);font-size:28px;color:var(--accent-ink);margin-top:6px;font-variant-numeric:tabular-nums}
.pv-calc .note{font-size:13px;color:var(--fg-muted);margin:0}
/* ===== comparison ===== */
.pv-cmp{overflow-x:auto}.pv-cmp:focus-visible{outline:2px solid var(--accent-ink);outline-offset:4px}
.pv-cmp table{width:100%;border-collapse:collapse;font-size:15px;min-width:640px}
.pv-cmp th,.pv-cmp td{padding:16px 14px;border-bottom:1px solid var(--border);text-align:left;vertical-align:top}
.pv-cmp th{font-family:var(--q-serif);font-size:18px;color:var(--fg);font-weight:600}
.pv-cmp td:first-child{font-weight:600;color:var(--fg)}
.pv-cmp td{color:var(--fg-muted)}
.pv-cmp .rec th{color:var(--accent-ink)}
.pv-cmp .tag{display:inline-block;font-size:13px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--accent-ink);margin-left:8px}
/* ===== checklist ===== */
.pv-check{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}
.pv-check label{display:flex;gap:14px;align-items:flex-start;background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:18px 20px;cursor:pointer;min-height:44px;font-size:15.5px;line-height:1.5;color:var(--fg)}
.pv-check input{width:24px;height:24px;font-size:16px;margin-top:1px;accent-color:var(--q-gold);flex:0 0 auto}
.pv-check-out{margin-top:22px;font-size:16px;color:var(--fg)}
.pv-check-out b{color:var(--accent-ink)}
/* ===== values / leadership ===== */
.pv-values{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.pv-values .q-card h3{font-family:var(--q-serif);font-size:20px;margin:0 0 8px;color:var(--fg)}
.pv-values .q-card p{font-size:15px;line-height:1.7;color:var(--fg-muted);margin:0}
.pv-lead{display:grid;grid-template-columns:repeat(var(--cols,2),1fr);gap:20px}
.pv-lead[style*="--cols:3"] .q-card{grid-template-columns:64px 1fr}.pv-lead[style*="--cols:3"] .av{width:64px;height:64px;font-size:20px}
@media(max-width:1024px){.pv-lead{grid-template-columns:repeat(2,1fr)}}@media(max-width:600px){.pv-lead{grid-template-columns:1fr}}
.pv-lead .q-card{display:grid;grid-template-columns:96px 1fr;gap:20px;align-items:center}
.pv-lead .av{width:96px;height:96px;border-radius:50%;background:linear-gradient(135deg,var(--bg-alt),var(--border));display:flex;align-items:center;justify-content:center;font-family:var(--q-serif);font-size:30px;color:var(--accent-ink)}
.pv-lead h3{font-family:var(--q-serif);font-size:20px;margin:0 0 4px;color:var(--fg)}.pv-lead p{font-size:14.5px;color:var(--fg-muted);margin:0;line-height:1.6}
.pv-orgs{display:flex;flex-wrap:wrap;gap:10px;margin-top:22px}
.pv-orgs span{border:1px solid var(--border);border-radius:999px;padding:8px 14px;font-size:14px;color:var(--fg);min-height:36px;display:inline-flex;align-items:center}
/* ===== sticky mobile cta ===== */
.pv-sticky{display:none}
@media(max-width:767px){.pv-sticky{display:grid;grid-template-columns:1fr 1fr;gap:8px;position:fixed;left:10px;right:10px;bottom:10px;z-index:85}.pv-sticky a{min-height:48px;display:flex;align-items:center;justify-content:center;border-radius:999px;font-weight:600;font-size:15px;white-space:nowrap;padding:0 12px;text-decoration:none;box-shadow:0 10px 30px rgba(0,0,0,.18)}.pv-sticky .a{background:var(--q-gold);color:var(--cta-fg)}.pv-sticky .b{background:var(--stage);color:#fff}
  body{padding-bottom:130px}}
/* ===== resources ===== */
.pv-res{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.pv-res a{display:flex;flex-direction:column;gap:10px;text-decoration:none;color:inherit;background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:24px}
.pv-res a:hover{border-color:var(--q-gold)}
.pv-res .k{font-size:13px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--accent-ink)}
.pv-res h3{font-family:var(--q-serif);font-size:20px;margin:0;color:var(--fg)}.pv-res p{font-size:14.5px;color:var(--fg-muted);margin:0;line-height:1.6}
.pv-res span{font-weight:600;color:var(--accent-ink);font-size:14px;margin-top:auto;min-height:44px;display:inline-flex;align-items:center}
/* ===== article ===== */
.pv-art-head{max-width:820px;margin:0 auto;text-align:center}.pv-art-head .q-h1{max-width:none;font-size:clamp(34px,4.2vw,56px)}
.pv-art-meta{display:flex;gap:16px;justify-content:center;flex-wrap:wrap;font-size:14px;color:var(--fg-muted);margin-top:18px}
.pv-art-meta b{color:var(--fg);font-weight:600}
.pv-art-hero{max-width:1000px;margin:40px auto 0;aspect-ratio:16/9;border-radius:calc(var(--radius) + 6px);overflow:hidden;border:1px solid var(--border);background:var(--bg-alt)}.pv-art-hero img{width:100%;height:100%;object-fit:cover;display:block}
.pv-art{display:grid;grid-template-columns:260px 1fr;gap:56px;align-items:start}
.pv-toc{position:sticky;top:110px;border-left:2px solid var(--border);padding-left:18px}
.pv-toc .k{font-size:13px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--fg-muted);margin-bottom:10px}
.pv-toc a{display:flex;align-items:center;min-height:40px;font-size:14.5px;color:var(--fg-muted);text-decoration:none}
.pv-toc a:hover{color:var(--accent-ink)}
.pv-prose{max-width:720px}
.pv-prose h2{font-family:var(--q-serif);font-size:30px;line-height:1.15;margin:44px 0 14px;color:var(--fg)}
.pv-prose h2:first-child{margin-top:0}
.pv-prose p{font-size:17px;line-height:1.75;color:var(--fg);margin:0 0 18px}
.pv-prose ul,.pv-prose ol{font-size:17px;line-height:1.75;color:var(--fg);padding-left:22px;margin:0 0 18px}.pv-prose li{margin-bottom:8px}.pv-prose li::marker{color:var(--accent-ink)}
.pv-prose .pq{border-left:3px solid var(--q-gold);padding:6px 0 6px 22px;margin:28px 0;font-family:var(--q-serif);font-size:23px;line-height:1.45;color:var(--fg)}
.pv-prose .callout{background:var(--bg-alt);border:1px solid var(--border);border-radius:var(--radius);padding:20px 22px;margin:28px 0;font-size:16px}
.pv-prose .callout b{display:block;margin-bottom:6px;color:var(--fg)}
.pv-prose a{color:var(--accent-ink)}
.pv-author{display:flex;gap:16px;align-items:center;margin-top:40px;padding-top:24px;border-top:1px solid var(--border)}
.pv-author .av{width:56px;height:56px;border-radius:50%;background:var(--stage);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700}
.pv-author p{margin:0;font-size:14.5px;color:var(--fg-muted)}.pv-author b{display:block;color:var(--fg);font-weight:600}
.pv-bc{font-size:13.5px;color:var(--fg-muted);padding:18px 0 0}
.pv-bc a{color:var(--fg-muted);text-decoration:none;display:inline-flex;align-items:center;min-height:32px}.pv-bc a:hover{color:var(--accent-ink)}
.pv-bc span{margin:0 8px}
@media(max-width:1024px){.pv-art{grid-template-columns:1fr}.pv-toc{position:static;border-left:0;padding-left:0}.pv-toc a{min-height:36px}.pv-tl{grid-template-columns:repeat(2,1fr)}.pv-tabs [role=tabpanel]{grid-template-columns:1fr}.pv-calc{grid-template-columns:1fr}}
@media(max-width:767px){.pv-tst,.pv-tl,.pv-check,.pv-values,.pv-lead,.pv-res{grid-template-columns:1fr}.pv-lead .q-card{grid-template-columns:72px 1fr}.pv-lead .av{width:72px;height:72px}.pv-calc .small{grid-template-columns:1fr 1fr}.pv-calc .big .v{font-size:40px}.pv-prose h2{font-size:25px}}
'''


def _hero_video(s, ctx):
    E, RAW = ctx["E"], ctx["RAW"]
    btns = ""
    if s.get("primary"):
        btns += f'<a class="q-btn" href="{E(ctx["L"](s["primary"]["href"]))}">{E(s["primary"]["label"])}</a>'
    if s.get("secondary"):
        btns += f'<a class="q-btn-ghost" href="{E(ctx["L"](s["secondary"]["href"]))}">{E(s["secondary"]["label"])}<span style="width:22px;height:1px;background:currentColor;display:inline-block"></span></a>'
    media = ""
    if s.get("video"):
        poster = f' poster="{E(ctx["rel"](s["poster"]))}"' if s.get("poster") else ""
        media = f'<video autoplay muted loop playsinline preload="metadata"{poster} aria-hidden="true"><source src="{E(ctx["rel"](s["video"]))}" type="video/mp4"></video>'
    elif s.get("poster"):
        media = f'<img class="pv-poster" src="{E(ctx["rel"](s["poster"]))}" alt="" aria-hidden="true">'
    note = f'<div class="pv-hero-note">{E(s["note"])}</div>' if s.get("note") else ""
    return f'''<section class="pv-hero-video">{media}<div class="q-container"><div style="max-width:760px">
<div class="q-eyebrow">{E(s.get("eyebrow"))}</div><h1 class="q-h1" style="margin-top:22px">{RAW(s["heading"])}</h1>
<div class="q-lead" style="max-width:600px;margin:24px 0 0">{E(s.get("subhead"))}</div><div class="pv-btns">{btns}</div>{note}</div></div></section>'''


def _video(s, ctx):
    E = ctx["E"]
    embed = ""
    if s.get("vimeo"):
        src = f'https://player.vimeo.com/video/{E(s["vimeo"])}?title=0&byline=0&portrait=0&dnt=1&autoplay=1'
        if s.get("poster"):
            inner = f'<img src="{E(ctx["rel"](s["poster"]))}" alt="" width="1280" height="720" loading="lazy"><button type="button" class="pv-play" aria-label="Play: {E(s.get("title", "Video"))}"><span></span></button>'
            embed = f' data-embed="{src}"'
        else:
            inner = f'<iframe src="{src.replace("&autoplay=1", "")}" title="{E(s.get("title", "Video"))}" loading="lazy" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe>'
    else:
        embed = ""
        poster = f' poster="{E(ctx["rel"](s["poster"]))}"' if s.get("poster") else ""
        inner = f'<video controls preload="metadata" playsinline{poster}><source src="{E(ctx["rel"](s["video"]))}" type="video/mp4">Your browser does not play video. <a href="{E(ctx["rel"](s["video"]))}">Download the film</a>.</video>'
    head = ""
    if s.get("heading"):
        head = f'<div class="pv-center" style="margin-bottom:36px">{f"<div class=q-eyebrow>{E(s.get(chr(101)+chr(121)+chr(101)+chr(98)+chr(114)+chr(111)+chr(119)))}</div>" if s.get("eyebrow") else ""}<h2 class="q-h2" style="margin-top:22px;max-width:720px">{E(s["heading"])}</h2>{f"<p class=q-lead style=max-width:620px;margin-top:14px>{E(s[chr(105)+chr(110)+chr(116)+chr(114)+chr(111)])}</p>" if s.get("intro") else ""}</div>'
    cap = f'<p class="pv-video-cap">{E(s["caption"])}</p>' if s.get("caption") else ""
    return f'{ctx["sec_open"](s)} <div class="q-container">{head}<div class="pv-video-wrap"><div class="pv-video"{embed}>{inner}</div>{cap}</div></div></section>'


def _testimonials(s, ctx):
    E = ctx["E"]
    if s.get("layout") == "feature":
        q, who, org = s["items"][0]
        rest = "".join(f'<li><blockquote>{E(x[0])}</blockquote><footer><b>{E(x[1])}</b> {E(x[2])}</footer></li>' for x in s["items"][1:])
        items = f'<figure class="lead"><blockquote>{E(q.strip().strip(chr(34)))}</blockquote><figcaption><b>{E(who)}</b>{E(org)}</figcaption></figure><ol class="pv-tst-letters">{rest}</ol>'
        return f'{ctx["sec_open"](s)} <div class="q-container"><div class="pv-center" style="margin-bottom:40px"><div class="q-eyebrow">{E(s.get("eyebrow", "What customers say"))}</div><h2 class="q-h2" style="margin-top:22px;max-width:720px">{E(s["heading"])}</h2></div><div class="pv-tst pv-tst-feature">{items}</div></div></section>'
    items = "".join(
        f'<figure><blockquote>{E(q.strip().strip(chr(34)))}</blockquote><figcaption><b>{E(who)}</b>{E(org)}</figcaption></figure>'
        for q, who, org in s["items"])
    return f'{ctx["sec_open"](s)} <div class="q-container"><div class="pv-center" style="margin-bottom:40px"><div class="q-eyebrow">{E(s.get("eyebrow", "What customers say"))}</div><h2 class="q-h2" style="margin-top:22px;max-width:720px">{E(s["heading"])}</h2></div><div class="pv-tst">{items}</div></div></section>'


def _timeline(s, ctx):
    """History rail: a line across the years, one card per milestone, optional image, vertical on phones."""
    E = ctx["E"]
    tid = s.get("id", "story")
    cards = []
    for i, it in enumerate(s["items"]):
        y, t, d = it[0], it[1], it[2]
        img = f'<div class="img"><img src="{E(ctx["rel"](it[3]))}" alt="" width="600" height="400" loading="lazy"></div>' if len(it) > 3 and it[3] else ""
        cards.append(f'<li style="--i:{i}"><span class="dot" aria-hidden="true"></span><div class="y">{E(y)}</div>{img}<h3>{E(t)}</h3><p>{E(d)}</p></li>')
    n = len(cards)
    head = f'<div class="pv-center"><div class="q-eyebrow">{E(s.get("eyebrow", ""))}</div><h2 class="q-h2" style="margin-top:22px;max-width:760px">{E(s["heading"])}</h2>{f"<p class=q-lead style=max-width:640px;margin:16px_auto_0>{E(s[chr(105)+chr(110)+chr(116)+chr(114)+chr(111)])}</p>".replace("_", " ") if s.get("intro") else ""}</div>'
    nav = f'<div class="pv-tl2-nav"><button type="button" data-d="-1" aria-label="Earlier">&larr;</button><button type="button" data-d="1" aria-label="Later">&rarr;</button></div>' if n > 3 else ""
    js = f"""<script>(function(){{var w=document.getElementById("{tid}-tl");if(!w)return;var r=w.querySelector('ol');w.querySelectorAll('.pv-tl2-nav button').forEach(function(b){{b.addEventListener('click',function(){{r.scrollBy({{left:(+b.getAttribute('data-d'))*Math.min(r.clientWidth*.8,720),behavior:'smooth'}})}})}});
if('IntersectionObserver' in window){{new IntersectionObserver(function(es){{es.forEach(function(e){{if(e.isIntersecting)w.classList.add('in')}})}},{{threshold:.2}}).observe(w)}}else{{w.classList.add('in')}}}})();</script>"""
    return f'{ctx["sec_open"](s)} <div class="q-container">{head}<div class="pv-tl2" id="{E(tid)}-tl" data-n="{n}">{nav}<div class="line" aria-hidden="true"><i></i></div><ol tabindex="0" aria-label="{E(s["heading"])}">{"".join(cards)}</ol></div></div>{js}</section>'


def _tabs(s, ctx):
    E = ctx["E"]
    tid = s.get("id", "tabs")
    tabs = "".join(f'<button role="tab" id="{tid}-t{i}" aria-selected="{"true" if i == 0 else "false"}" aria-controls="{tid}-p{i}" tabindex="{0 if i == 0 else -1}">{E(t["label"])}</button>' for i, t in enumerate(s["items"]))
    panels = ""
    for i, t in enumerate(s["items"]):
        bullets = "".join(f"<li>{E(b)}</li>" for b in t.get("bullets", []))
        img = f'<div class="img"><img src="{E(ctx["rel"](t["image"]))}" alt="{E(t.get("image_alt", ""))}" width="800" height="600" loading="lazy"></div>' if t.get("image") else ""
        link = f'<p><a class="q-btn-ghost" href="{E(ctx["L"](t["href"]))}">{E(t.get("link_label", "Learn more"))}<span style="width:22px;height:1px;background:currentColor;display:inline-block"></span></a></p>' if t.get("href") else ""
        panels += f'<div role="tabpanel" tabindex="0" id="{tid}-p{i}" aria-labelledby="{tid}-t{i}"{"" if i == 0 else " hidden"}><div><h3>{E(t["title"])}</h3><p>{E(t["body"])}</p>{f"<ul>{bullets}</ul>" if bullets else ""}{link}</div>{img}</div>'
    js = f'''<script>(function(){{var r=document.getElementById("{tid}");if(!r)return;var tabs=r.querySelectorAll("[role=tab]"),panels=r.querySelectorAll("[role=tabpanel]");tabs.forEach(function(t,i){{t.addEventListener("click",function(){{tabs.forEach(function(x,j){{x.setAttribute("aria-selected",j===i?"true":"false");x.tabIndex=j===i?0:-1;panels[j].hidden=j!==i}})}});t.addEventListener("keydown",function(e){{var k=e.key==="ArrowRight"?1:e.key==="ArrowLeft"?-1:0;var n;if(e.key==="Home")n=0;else if(e.key==="End")n=tabs.length-1;else{{if(!k)return;n=(i+k+tabs.length)%tabs.length}}e.preventDefault();tabs[n].click();tabs[n].focus()}})}})}})();</script>'''
    return f'{ctx["sec_open"](s)} <div class="q-container pv-tabs" id="{tid}"><div class="pv-center" style="margin-bottom:36px"><div class="q-eyebrow">{E(s.get("eyebrow"))}</div><h2 class="q-h2" style="margin-top:22px;max-width:760px">{E(s["heading"])}</h2></div><div role="tablist" aria-label="{E(s["heading"])}">{tabs}</div>{panels}</div>{js}</section>'


def _calculator(s, ctx):
    """A print-cost estimator. Defaults and rates are DRAFT ranges; the page says so."""
    E = ctx["E"]
    cid = s.get("id", "calc")
    r = s.get("rates", {})
    mono = r.get("mono_cpp", 0.018); color = r.get("color_cpp", 0.09); labor_min = r.get("minutes_per_device_week", 25); labor_rate = r.get("hourly", 28)
    saving = r.get("managed_saving", 0.22)
    return f'''{ctx["sec_open"](s)} <div class="q-container"><div class="pv-center" style="margin-bottom:40px"><div class="q-eyebrow">{E(s.get("eyebrow"))}</div><h2 class="q-h2" style="margin-top:22px;max-width:760px">{E(s["heading"])}</h2><p class="q-lead" style="max-width:620px;margin-top:14px">{E(s.get("intro"))}</p></div>
<div class="pv-calc" id="{cid}">
<div class="in">
<div><label for="{cid}-d">Devices (printers and copiers)</label><div class="row"><input id="{cid}-d" type="range" min="1" max="60" value="8"><output for="{cid}-d">8</output></div></div>
<div><label for="{cid}-m">Mono pages a month</label><div class="row"><input id="{cid}-m" type="range" min="0" max="200000" step="500" value="25000"><output for="{cid}-m">25,000</output></div></div>
<div><label for="{cid}-c">Color pages a month</label><div class="row"><input id="{cid}-c" type="range" min="0" max="60000" step="250" value="6000"><output for="{cid}-c">6,000</output></div></div>
<p class="note">{E(s.get("note", "Estimates use typical North Carolina rates and are for orientation only. The assessment replaces them with your real numbers."))}</p>
</div>
<div class="out">
<div class="big"><div class="k">Estimated print spend today</div><div class="v" data-out="total">$0</div><div class="d">Toner and service per page, plus the staff time spent ordering supplies and chasing repairs.</div></div>
<div class="small"><div><div class="k">Per page, blended</div><div class="v" data-out="cpp">$0.00</div></div><div><div class="k">Staff hours a year on print</div><div class="v" data-out="hours">0</div></div><div><div class="k">Typical managed saving</div><div class="v" data-out="save">$0</div></div><div><div class="k">Toner orders a year, today</div><div class="v" data-out="orders">0</div></div></div>
<p style="margin:6px 0 0"><a class="q-btn" href="{E(ctx["L"](s.get("cta_href", "contact.html")))}">{E(s.get("cta_label", "Get the real number: request an assessment"))}</a></p>
</div></div></div>
<script>(function(){{var r=document.getElementById("{cid}");if(!r)return;var d=r.querySelector("#{cid}-d"),m=r.querySelector("#{cid}-m"),c=r.querySelector("#{cid}-c");var f=function(n){{return n.toLocaleString("en-US")}};var $=function(n){{return "$"+Math.round(n).toLocaleString("en-US")}};function u(){{var dv=+d.value,mv=+m.value,cv=+c.value;r.querySelector('output[for="{cid}-d"]').textContent=f(dv);r.querySelector('output[for="{cid}-m"]').textContent=f(mv);r.querySelector('output[for="{cid}-c"]').textContent=f(cv);var pages=(mv*{mono})+(cv*{color});var hours=dv*{labor_min}/60*52;var labor=hours*{labor_rate};var year=pages*12+labor;r.querySelector('[data-out=total]').textContent=$(year)+" / yr";r.querySelector('[data-out=cpp]').textContent="$"+((mv+cv)?(pages/(mv+cv)):0).toFixed(3);r.querySelector('[data-out=hours]').textContent=f(Math.round(hours));r.querySelector('[data-out=save]').textContent=$(year*{saving})+" / yr";r.querySelector('[data-out=orders]').textContent=f(Math.round(dv*6))}}[d,m,c].forEach(function(i){{i.addEventListener("input",u)}});u()}})();</script></section>'''


def _capex_calc(s, ctx):
    """Buy the rooms or subscribe to them. Rate factors are illustrative; the page says so."""
    E = ctx["E"]
    cid = s.get("id", "capex")
    f36, f60 = s.get("factors", [0.032, 0.021])
    hr = s.get("hourly", 65)
    return f'''{ctx["sec_open"](s)} <div class="q-container"><div class="pv-center" style="margin-bottom:40px"><div class="q-eyebrow">{E(s.get("eyebrow"))}</div><h2 class="q-h2" style="margin-top:22px;max-width:760px">{E(s["heading"])}</h2><p class="q-lead" style="max-width:620px;margin-top:14px">{E(s.get("intro"))}</p></div>
<div class="pv-calc" id="{cid}">
<div class="in">
<div><label for="{cid}-r">Rooms</label><div class="row"><input id="{cid}-r" type="range" min="1" max="100" value="{s.get("rooms", 12)}"><output for="{cid}-r"></output></div></div>
<div><label for="{cid}-c">Equipment and installation per room</label><div class="row"><input id="{cid}-c" type="range" min="5000" max="150000" step="2500" value="{s.get("per_room", 35000)}"><output for="{cid}-c"></output></div></div>
<div><label for="{cid}-h">Hours your team spends on each room a month</label><div class="row"><input id="{cid}-h" type="range" min="0" max="10" step="0.5" value="{s.get("hours", 2)}"><output for="{cid}-h"></output></div></div>
<div><label for="{cid}-t">Term</label><div class="row"><select id="{cid}-t" style="flex:1;min-height:44px;font:inherit;padding:8px 10px;border:1px solid var(--border);border-radius:var(--radius);background:var(--card);color:var(--fg)"><option value="36">36 months</option><option value="60" selected>60 months</option></select></div></div>
<p class="note">{E(s.get("note", "Illustrative only. The monthly figure uses a typical rate for the term you choose and includes support, monitoring and planned upgrades. Your account manager quotes the real number."))}</p>
</div>
<div class="out">
<div class="big"><div class="k">Capital kept in the business on day one</div><div class="v" data-out="cap">$0</div><div class="d">What buying the rooms outright would cost before the first meeting is held.</div></div>
<div class="small"><div><div class="k">As a service, a month</div><div class="v" data-out="mo">$0</div></div><div><div class="k">Per room, a month</div><div class="v" data-out="room">$0</div></div><div><div class="k">Support hours back a year</div><div class="v" data-out="hrs">0</div></div><div><div class="k">Value of that time a year</div><div class="v" data-out="val">$0</div></div></div>
<p style="margin:6px 0 0"><a class="q-btn" href="{E(ctx["L"](s.get("cta_href", "contact.html")))}">{E(s.get("cta_label", "Get the real number"))}</a></p>
</div></div></div>
<script>(function(){{var r=document.getElementById("{cid}");if(!r)return;var R=r.querySelector("#{cid}-r"),C=r.querySelector("#{cid}-c"),H=r.querySelector("#{cid}-h"),T=r.querySelector("#{cid}-t");var f=function(n){{return Math.round(n).toLocaleString("en-US")}};var $=function(n){{return "$"+f(n)}};function u(){{var rv=+R.value,cv=+C.value,hv=+H.value,fac=T.value==="36"?{f36}:{f60};r.querySelector('output[for="{cid}-r"]').textContent=rv;r.querySelector('output[for="{cid}-c"]').textContent=$(cv);r.querySelector('output[for="{cid}-h"]').textContent=hv;var cap=rv*cv,mo=cap*fac,hrs=rv*hv*12;r.querySelector("[data-out=cap]").textContent=$(cap);r.querySelector("[data-out=mo]").textContent=$(mo);r.querySelector("[data-out=room]").textContent=$(mo/rv);r.querySelector("[data-out=hrs]").textContent=f(hrs);r.querySelector("[data-out=val]").textContent=$(hrs*{hr})}}[R,C,H,T].forEach(function(i){{i.addEventListener("input",u)}});u()}})();</script></section>'''


def _comparison(s, ctx):
    E = ctx["E"]
    cols = s["columns"]
    head = "".join(f'<th{" class=rec" if c.get("recommended") else ""}>{E(c["label"])}{"<span class=tag>Most common</span>" if c.get("recommended") else ""}</th>' for c in cols)
    rows = "".join("<tr>" + f"<td>{E(row[0])}</td>" + "".join(f"<td>{E(v)}</td>" for v in row[1:]) + "</tr>" for row in s["rows"])
    return f'{ctx["sec_open"](s)} <div class="q-container"><div class="pv-split"><h2 class="q-h2">{E(s["heading"])}</h2><p>{E(s.get("intro"))}</p></div><div class="pv-cmp" tabindex="0" role="region" aria-label="{E(s["heading"])}"><table><thead><tr><th scope="row">Option</th>{head}</tr></thead><tbody>{rows}</tbody></table></div><p class="pv-cmp-hint">Swipe sideways to compare all three.</p>{f"<p style=font-size:14px;color:var(--fg-muted);margin-top:14px>{E(s[chr(110)+chr(111)+chr(116)+chr(101)])}</p>" if s.get("note") else ""}</div></section>'


def _checklist(s, ctx):
    E = ctx["E"]
    cid = s.get("id", "check")
    items = "".join(f'<label><input type="checkbox">{E(t)}</label>' for t in s["items"])
    return f'''{ctx["sec_open"](s)} <div class="q-container" id="{cid}"><div class="pv-center" style="margin-bottom:36px"><div class="q-eyebrow">{E(s.get("eyebrow", "Is this you?"))}</div><h2 class="q-h2" style="margin-top:22px;max-width:760px">{E(s["heading"])}</h2><p class="q-lead" style="max-width:600px;margin-top:14px">{E(s.get("intro"))}</p></div><div class="pv-check">{items}</div><p class="pv-check-out" data-out>{E(s.get("zero", "Check what sounds familiar."))}</p><p style="margin-top:18px"><a class="q-btn-ghost" data-cta data-label="{E(s.get("cta_label", "See what the assessment finds"))}" href="{E(ctx["L"](s.get("cta_href", "contact.html")))}">{E(s.get("cta_label", "See what the assessment finds"))}<span style="width:22px;height:1px;background:currentColor;display:inline-block"></span></a></p></div>
<script>(function(){{var r=document.getElementById("{cid}");if(!r)return;var o=r.querySelector("[data-out]"),bs=r.querySelectorAll("input");var msgs={json.dumps(s.get("messages", ["Tick what sounds familiar.", "One is normal.", "Two is a pattern.", "Three or more is money leaving the building every month. The assessment finds how much."]))};var cta=r.querySelector("[data-cta]");function u(){{var n=0;bs.forEach(function(b){{if(b.checked)n++}});o.innerHTML=(n?"<b>"+n+" of "+bs.length+"</b> ":"")+(msgs[Math.min(n,msgs.length-1)]);if(cta){{if(n>=3){{cta.className="q-btn";cta.textContent="Request an assessment"}}else{{cta.className="q-btn-ghost";cta.innerHTML=cta.getAttribute("data-label")+'<span style="width:22px;height:1px;background:currentColor;display:inline-block"></span>'}}}}}}bs.forEach(function(b){{b.addEventListener("change",u)}});u()}})();</script></section>'''


def _proof(s, ctx):
    E = ctx["E"]
    src = f'<p class="src">{E(s["source"])}</p>' if s.get("source") else ""
    return f'{ctx["sec_open"](s)} <div class="q-container pv-proof"><div class="q-eyebrow" style="justify-content:center">{E(s.get("eyebrow", ""))}</div><b>{E(s["value"])}</b><p class="q-lead">{E(s["text"])}</p>{src}</div></section>'


# North Carolina outline, lon/lat, simplified. Drawn once, projected in _map.
NC_OUTLINE = [(-84.32, 34.99), (-84.29, 35.22), (-84.02, 35.41), (-83.62, 35.57), (-83.11, 35.77), (-82.78, 35.95), (-82.60, 36.06), (-82.22, 36.16), (-81.91, 36.30), (-81.70, 36.58),
              (-80.30, 36.55), (-78.50, 36.54), (-76.92, 36.55), (-75.87, 36.55), (-75.72, 36.23), (-75.55, 35.82), (-75.47, 35.43), (-75.53, 35.23), (-75.90, 35.10), (-76.20, 34.95),
              (-76.50, 34.62), (-76.95, 34.68), (-77.35, 34.52), (-77.75, 34.30), (-77.92, 33.95), (-78.02, 33.86), (-78.55, 33.86), (-79.07, 34.30), (-79.68, 34.80), (-80.32, 34.82),
              (-80.78, 34.82), (-80.93, 35.10), (-81.05, 35.15), (-81.38, 35.17), (-82.29, 35.20), (-82.78, 35.08), (-83.11, 35.00), (-84.32, 34.99)]


# Simplified state outlines, lon/lat. "nc" is the default; add a region here and reference it with "region" on the map section.
CA_OUTLINE = [(-124.4, 42.0), (-120.0, 42.0), (-120.0, 39.0), (-114.63, 35.0), (-114.63, 34.87), (-114.13, 34.3), (-114.72, 33.4), (-114.72, 32.72), (-117.13, 32.53), (-117.3, 33.0),
              (-118.4, 33.75), (-118.5, 34.03), (-119.2, 34.15), (-120.5, 34.5), (-120.65, 35.2), (-121.9, 36.6), (-122.4, 37.2), (-122.5, 37.8), (-123.0, 38.3), (-123.7, 38.95),
              (-123.85, 39.8), (-124.2, 40.4), (-124.4, 41.0), (-124.2, 41.8), (-124.4, 42.0)]
NV_OUTLINE = [(-120.0, 42.0), (-114.05, 42.0), (-114.05, 36.2), (-114.63, 35.0), (-120.0, 39.0), (-120.0, 42.0)]
# The contiguous United States, from the US Census cartographic boundary via us-atlas 3.0.1 (nation-10m, public
# domain), Douglas-Peucker simplified to 0.08 degrees. For clients whose offices span the country.
US_OUTLINE = [[-124.73,48.17],[-124.65,48.39],[-123.98,48.16],[-123.13,48.18],[-122.87,48.0],[-122.76,48.14],[-122.61,47.89],[-122.78,47.7],[-122.81,47.81],[-123.15,47.36],[-122.91,47.39],[-123.12,47.39],[-122.53,47.91],[-122.55,47.29],[-122.73,47.33],[-122.71,47.13],[-122.8,47.34],[-122.86,47.27],[-122.68,47.1],[-122.53,47.32],[-122.33,47.35],[-122.43,47.66],[-122.23,47.97],[-122.4,48.23],[-122.48,48.19],[-122.38,48.06],[-122.51,48.13],[-122.41,48.33],[-122.71,48.46],[-122.47,48.47],[-122.43,48.6],[-122.54,48.78],[-122.67,48.73],[-122.76,49.0],[-95.15,49.0],[-95.15,49.38],[-94.96,49.37],[-94.82,49.29],[-94.64,48.74],[-93.83,48.63],[-93.79,48.52],[-92.99,48.62],[-92.63,48.54],[-92.71,48.46],[-92.51,48.45],[-92.37,48.22],[-92.06,48.36],[-91.57,48.04],[-90.89,48.25],[-90.76,48.1],[-89.49,48.01],[-90.87,47.56],[-92.06,46.81],[-91.94,46.68],[-90.87,46.96],[-90.75,46.89],[-90.95,46.6],[-90.74,46.69],[-90.44,46.56],[-88.96,47.01],[-88.39,47.38],[-87.98,47.48],[-87.71,47.4],[-88.23,47.2],[-88.5,46.76],[-88.14,46.97],[-88.28,46.83],[-87.82,46.89],[-87.35,46.5],[-86.88,46.44],[-86.14,46.67],[-85.17,46.76],[-84.95,46.77],[-85.03,46.48],[-84.59,46.41],[-84.13,46.53],[-84.12,46.23],[-84.25,46.18],[-83.87,45.99],[-83.77,46.02],[-83.82,46.1],[-83.58,46.09],[-83.51,45.93],[-84.38,45.93],[-84.66,46.05],[-84.75,45.84],[-85.01,46.01],[-85.51,46.09],[-85.7,45.96],[-86.28,45.94],[-86.62,45.61],[-86.72,45.67],[-86.54,45.89],[-86.78,45.85],[-86.96,45.67],[-87.02,45.84],[-87.63,44.98],[-87.84,44.93],[-88.04,44.57],[-87.93,44.54],[-87.61,44.84],[-87.38,44.87],[-87.24,45.17],[-86.98,45.29],[-87.47,44.55],[-87.52,44.18],[-87.74,43.88],[-87.71,43.68],[-87.91,43.24],[-87.77,42.78],[-87.84,42.3],[-87.42,41.64],[-87.12,41.65],[-86.62,41.89],[-86.3,42.36],[-86.21,42.72],[-86.54,43.62],[-86.44,43.79],[-86.51,44.05],[-86.27,44.35],[-86.26,44.69],[-85.54,45.21],[-85.65,44.85],[-85.6,44.77],[-85.47,44.99],[-85.53,44.75],[-85.37,45.27],[-84.92,45.39],[-85.12,45.57],[-84.94,45.71],[-85.01,45.76],[-84.77,45.79],[-83.5,45.36],[-83.27,45.02],[-83.45,45.04],[-83.27,44.71],[-83.33,44.34],[-83.54,44.25],[-83.58,44.06],[-83.88,43.96],[-83.91,43.67],[-83.65,43.6],[-83.41,43.92],[-82.91,44.07],[-82.64,43.85],[-82.42,42.97],[-82.52,42.61],[-82.69,42.52],[-82.62,42.67],[-82.8,42.65],[-83.45,41.71],[-82.93,41.51],[-82.84,41.59],[-82.48,41.38],[-81.74,41.49],[-79.15,42.55],[-78.85,42.78],[-79.07,43.08],[-79.07,43.26],[-78.37,43.38],[-76.95,43.27],[-76.24,43.53],[-76.3,43.84],[-76.13,43.9],[-76.38,44.03],[-76.31,44.2],[-74.97,44.98],[-71.5,45.01],[-71.44,45.23],[-71.29,45.3],[-71.13,45.25],[-71.01,45.35],[-70.86,45.23],[-70.78,45.43],[-70.64,45.38],[-70.72,45.52],[-70.64,45.61],[-70.26,45.89],[-70.29,46.19],[-70.06,46.42],[-70.0,46.69],[-69.23,47.46],[-69.04,47.43],[-69.05,47.26],[-68.9,47.18],[-68.23,47.35],[-67.79,47.07],[-67.8,45.68],[-67.45,45.6],[-67.49,45.28],[-67.34,45.13],[-67.16,45.16],[-66.98,44.81],[-67.26,44.6],[-67.41,44.68],[-67.59,44.45],[-67.77,44.55],[-68.05,44.33],[-68.18,44.38],[-68.19,44.24],[-68.4,44.25],[-68.46,44.34],[-68.36,44.39],[-68.48,44.43],[-68.6,44.01],[-68.68,44.26],[-68.83,44.31],[-68.78,44.49],[-69.0,44.43],[-69.08,43.97],[-70.17,43.68],[-70.55,43.32],[-70.82,42.85],[-70.78,42.69],[-70.6,42.66],[-70.87,42.55],[-71.01,42.28],[-70.72,42.21],[-70.7,41.99],[-70.41,41.74],[-70.03,41.79],[-70.09,42.03],[-70.24,42.07],[-70.03,42.02],[-69.99,41.54],[-70.0,41.67],[-70.35,41.64],[-70.95,41.41],[-70.66,41.54],[-70.63,41.71],[-70.72,41.74],[-71.19,41.46],[-71.24,41.62],[-71.34,41.45],[-71.2,41.68],[-71.39,41.78],[-71.48,41.37],[-72.91,41.29],[-73.64,41.0],[-73.78,40.79],[-73.49,40.95],[-72.64,40.98],[-72.28,41.16],[-72.1,40.99],[-71.86,41.07],[-73.21,40.63],[-73.94,40.54],[-74.06,40.68],[-74.27,40.49],[-73.98,40.45],[-74.1,39.76],[-74.86,38.94],[-74.97,38.94],[-74.89,39.16],[-75.14,39.18],[-75.54,39.46],[-75.53,39.69],[-75.59,39.46],[-75.31,38.92],[-75.1,38.8],[-75.05,38.41],[-75.94,37.09],[-76.02,37.32],[-75.66,37.96],[-75.89,37.92],[-75.83,38.13],[-75.96,38.14],[-75.86,38.36],[-75.97,38.25],[-76.0,38.37],[-76.06,38.23],[-76.26,38.33],[-76.28,38.61],[-76.03,38.57],[-76.35,38.69],[-76.2,38.93],[-76.38,38.85],[-76.3,39.03],[-76.16,39.0],[-76.28,39.15],[-76.0,39.37],[-75.97,39.56],[-76.22,39.35],[-76.25,39.45],[-76.28,39.3],[-76.36,39.39],[-76.44,39.2],[-76.58,39.26],[-76.39,39.01],[-76.56,38.77],[-76.32,38.04],[-76.83,38.35],[-76.92,38.29],[-77.02,38.45],[-77.25,38.38],[-77.11,38.63],[-77.25,38.64],[-77.27,38.33],[-77.04,38.4],[-76.96,38.21],[-76.62,38.15],[-76.24,37.89],[-76.36,37.61],[-76.91,37.97],[-76.54,37.62],[-76.3,37.56],[-76.27,37.31],[-76.41,37.4],[-76.35,37.27],[-76.49,37.25],[-76.29,37.13],[-76.3,37.0],[-76.43,36.97],[-76.65,37.22],[-76.95,37.23],[-76.69,37.2],[-76.48,36.9],[-75.99,36.92],[-75.53,35.79],[-75.99,36.53],[-75.8,36.07],[-75.92,36.24],[-76.18,36.3],[-76.06,36.16],[-76.46,36.18],[-76.3,36.1],[-76.58,36.01],[-76.69,36.28],[-76.67,35.94],[-76.06,35.99],[-76.04,35.67],[-75.95,35.96],[-75.81,35.96],[-75.73,35.63],[-76.14,35.33],[-76.49,35.37],[-76.59,35.51],[-76.46,35.55],[-76.63,35.51],[-76.58,35.39],[-77.02,35.52],[-76.47,35.26],[-76.8,34.96],[-76.98,35.0],[-76.76,34.92],[-76.48,35.07],[-76.29,35.01],[-76.53,34.68],[-76.62,34.78],[-76.67,34.71],[-76.52,34.65],[-76.04,35.06],[-76.54,34.59],[-76.68,34.69],[-77.03,34.66],[-77.56,34.42],[-77.96,33.85],[-78.28,33.91],[-78.72,33.8],[-79.09,33.48],[-79.36,33.01],[-79.58,33.01],[-80.0,32.61],[-80.47,32.5],[-80.46,32.33],[-80.75,32.31],[-80.67,32.22],[-81.2,31.72],[-81.13,31.62],[-81.26,31.55],[-81.18,31.52],[-81.29,31.21],[-81.49,30.98],[-81.41,30.98],[-81.45,30.5],[-81.26,29.81],[-80.57,28.59],[-80.57,28.1],[-80.03,26.8],[-80.13,25.77],[-80.36,25.33],[-80.18,25.49],[-80.66,24.9],[-80.44,25.19],[-81.14,25.16],[-81.29,25.69],[-81.69,25.85],[-81.87,26.38],[-82.11,26.48],[-82.18,26.68],[-82.09,26.67],[-82.07,26.96],[-82.27,26.72],[-82.74,27.54],[-82.57,27.61],[-82.41,27.9],[-82.55,27.85],[-82.69,28.03],[-82.59,27.82],[-82.73,27.61],[-82.85,27.86],[-82.86,28.22],[-82.78,28.06],[-82.67,28.44],[-82.69,28.91],[-82.8,29.15],[-83.05,29.13],[-83.64,29.89],[-84.02,30.1],[-84.27,30.1],[-84.34,29.9],[-85.12,29.72],[-85.01,29.62],[-84.69,29.76],[-85.05,29.59],[-85.35,29.66],[-85.42,29.84],[-85.34,29.69],[-85.3,29.81],[-85.43,29.95],[-86.3,30.36],[-88.0,30.23],[-87.76,30.29],[-88.01,30.68],[-88.14,30.32],[-89.31,30.38],[-89.45,30.19],[-89.86,30.0],[-89.66,29.86],[-89.48,30.08],[-89.37,29.91],[-89.22,29.97],[-89.43,29.66],[-89.53,29.73],[-89.49,29.62],[-89.68,29.62],[-89.51,29.39],[-89.2,29.35],[-89.0,29.18],[-89.14,28.99],[-89.25,29.08],[-89.42,28.93],[-89.28,29.18],[-89.39,29.12],[-89.84,29.32],[-90.22,29.09],[-90.43,29.35],[-90.58,29.31],[-90.87,29.06],[-91.34,29.3],[-91.12,29.25],[-91.13,29.34],[-91.46,29.47],[-91.62,29.74],[-91.86,29.71],[-91.83,29.83],[-92.2,29.75],[-92.02,29.62],[-92.25,29.54],[-93.47,29.77],[-94.13,29.65],[-94.73,29.37],[-94.49,29.52],[-94.77,29.55],[-94.76,29.78],[-94.94,29.7],[-95.02,29.56],[-94.89,29.31],[-95.17,29.11],[-94.73,29.33],[-96.72,28.16],[-97.21,27.6],[-97.38,27.06],[-97.16,26.08],[-97.37,26.56],[-97.36,27.35],[-97.08,27.91],[-96.42,28.4],[-96.68,28.31],[-96.77,28.41],[-96.93,28.12],[-97.15,28.13],[-97.21,28.08],[-97.02,28.04],[-97.19,27.83],[-97.52,27.85],[-97.25,27.7],[-97.41,27.32],[-97.64,27.27],[-97.42,27.26],[-97.44,26.61],[-97.15,25.95],[-97.44,25.85],[-97.65,26.02],[-98.2,26.06],[-99.08,26.4],[-99.45,27.02],[-99.51,27.56],[-100.29,28.28],[-100.8,29.25],[-101.26,29.52],[-101.41,29.76],[-102.3,29.88],[-102.67,29.74],[-102.89,29.21],[-103.28,28.98],[-104.51,29.64],[-104.92,30.6],[-106.21,31.47],[-106.45,31.76],[-108.21,31.78],[-108.21,31.33],[-111.08,31.33],[-114.81,32.49],[-114.72,32.72],[-117.12,32.53],[-117.5,33.33],[-118.09,33.73],[-118.41,33.74],[-118.54,34.04],[-119.13,34.1],[-119.56,34.41],[-120.47,34.45],[-120.62,34.55],[-120.63,35.12],[-120.86,35.21],[-120.91,35.45],[-121.88,36.29],[-121.97,36.57],[-121.82,36.68],[-121.86,36.93],[-122.11,36.96],[-122.4,37.2],[-122.52,37.78],[-122.41,37.81],[-122.36,37.59],[-122.05,37.46],[-122.43,37.96],[-122.3,38.11],[-122.49,38.11],[-122.44,37.88],[-122.53,37.82],[-123.01,38.0],[-122.97,38.25],[-123.74,38.95],[-123.85,39.83],[-124.36,40.26],[-124.41,40.44],[-124.14,40.93],[-124.06,41.44],[-124.55,42.84],[-124.15,43.91],[-123.96,45.28],[-124.0,46.24],[-123.85,46.16],[-123.55,46.27],[-124.08,46.27],[-124.07,46.63],[-123.95,46.38],[-123.96,46.64],[-123.83,46.72],[-124.09,46.75],[-124.14,46.91],[-123.86,46.95],[-124.12,47.04],[-124.18,46.93],[-124.42,47.74],[-124.73,48.17]]

REGIONS = {"nc": {"name": "North Carolina", "outlines": [NC_OUTLINE], "scale": 100},
           "us": {"name": "the United States", "outlines": [US_OUTLINE], "scale": 12},
           "west": {"name": "California and Nevada", "outlines": [CA_OUTLINE, NV_OUTLINE], "scale": 72}}


def _map(s, ctx):
    """Service-area map: the NC outline with a pin per branch, and the branch list beside it."""
    E = ctx["E"]
    import math
    region = REGIONS.get(s.get("region", "nc"), REGIONS["nc"])
    outlines = region["outlines"]
    all_pts = [p for o in outlines for p in o]
    lat0 = (max(p[1] for p in all_pts) + min(p[1] for p in all_pts)) / 2
    lon_w, lat_n = min(p[0] for p in all_pts), max(p[1] for p in all_pts)
    kx = math.cos(math.radians(lat0))
    scale = region.get("scale", 100)
    def proj(lon, lat):
        return ((lon - lon_w) * kx * scale, (lat_n - lat) * scale)
    pts = [proj(*p) for p in all_pts]
    xs = [x for x, _ in pts]; ys = [y for _, y in pts]
    w, h = max(xs) - min(xs) + 40, max(ys) - min(ys) + 40
    ox, oy = min(xs) - 20, min(ys) - 20
    path = " ".join("M" + " L".join(f"{x - ox:.1f},{y - oy:.1f}" for x, y in [proj(*p) for p in o]) + " Z" for o in outlines)
    pins, rows = [], []
    for it in s["items"]:
        name, lon, lat, href, sub, hq = it["name"], it["lon"], it["lat"], it["href"], it.get("sub", ""), it.get("hq", False)
        x, y = proj(lon, lat); x -= ox; y -= oy
        dx, dy = it.get("label_dx", 10), it.get("label_dy", 4)
        ring = f'<circle class="ring" cx="{x:.1f}" cy="{y:.1f}" r="{s.get("ring", 42)}"/>' if it.get("ring", True) else ""
        pins.append(f'{ring}<circle class="pin{" hq" if hq else ""}" cx="{x:.1f}" cy="{y:.1f}" r="5.5"/><text x="{x + dx:.1f}" y="{y + dy:.1f}">{E(name)}</text>')
        rows.append(f'<li><div><b>{E(name)}{" (headquarters)" if hq else ""}</b><small>{E(sub)}</small></div><a href="{E(ctx["L"](href))}">{E(it.get("link", "Branch page"))}</a></li>')
    svg = f'<svg class="pv-map-svg" viewBox="0 0 {w:.0f} {h:.0f}" role="img" aria-label="{E(s.get("alt", f"Map of {region.get(chr(110)+chr(97)+chr(109)+chr(101), chr(78)+chr(67))} with {ctx.get(chr(99)+chr(108)+chr(105)+chr(101)+chr(110)+chr(116)+chr(95)+chr(115)+chr(104)+chr(111)+chr(114)+chr(116), chr(111)+chr(117)+chr(114))} locations"))}"><path class="land" d="{path}"/>{"".join(pins)}</svg>'
    head = f'<div class="pv-split" style="margin-bottom:40px"><h2 class="q-h2">{E(s["heading"])}</h2><p>{E(s.get("intro", ""))}</p></div>'
    return f'{ctx["sec_open"](s)} <div class="q-container">{head}<div class="pv-map-wrap">{svg}<ul class="pv-map-list">{"".join(rows)}</ul></div></div></section>'


def _values(s, ctx):
    E = ctx["E"]
    cards = "".join(f'<div class="q-card"><h3>{E(t)}</h3><p>{E(d)}</p></div>' for t, d in s["items"])
    return f'{ctx["sec_open"](s)} <div class="q-container"><div class="pv-center" style="margin-bottom:40px"><div class="q-eyebrow">{E(s.get("eyebrow"))}</div><h2 class="q-h2" style="margin-top:22px;max-width:760px">{E(s["heading"])}</h2></div><div class="pv-values" style="grid-template-columns:repeat({min(len(s["items"]), 3)},1fr)">{cards}</div></div></section>'


def _leadership(s, ctx):
    E = ctx["E"]
    people = "".join(f'<div class="q-card"><div class="av" aria-hidden="true">{E("".join(w[0] for w in n.split()[:2]))}</div><div><h3>{E(n)}</h3><p>{E(r)}</p></div></div>' for n, r in s["people"])
    orgs = "".join(f"<span>{E(o)}</span>" for o in s.get("orgs", []))
    orgs_html = f'<p style="margin:34px 0 0;font-size:15px;color:var(--fg-muted)">{E(s.get("orgs_intro", ""))}</p><div class="pv-orgs">{orgs}</div>' if orgs else ""
    return f'{ctx["sec_open"](s)} <div class="q-container"><div class="pv-split"><h2 class="q-h2">{E(s["heading"])}</h2><p>{E(s.get("intro"))}</p></div><div class="pv-lead" style="--cols:{3 if len(s['people']) % 3 == 0 and len(s['people']) % 2 else 2}">{people}</div>{orgs_html}</div></section>'


def _sticky(s, ctx):
    E = ctx["E"]
    return f'<nav class="pv-sticky" aria-label="Quick actions"><a class="a" href="{E(ctx["L"](s.get("primary_href", "contact.html")))}">{E(s.get("primary", "Request an assessment"))}</a><a class="b" href="{E(s.get("secondary_href", ctx["brand"].get("phone_href", "#")))}">{E(s.get("secondary", "Call"))}</a></nav>'


def _resources(s, ctx):
    E = ctx["E"]
    cards = "".join(f'<a class="pv-tilt" href="{E(ctx["L"](h))}"><span class="k">{E(k)}</span><h3>{E(t)}</h3><p>{E(d)}</p><span>{E(l)}</span></a>' for k, t, d, l, h in s["items"])
    return f'{ctx["sec_open"](s)} <div class="q-container"><div class="pv-split"><h2 class="q-h2">{E(s["heading"])}</h2><p>{E(s.get("intro"))}</p></div><div class="pv-res{" pv-res-5" if len(s["items"]) == 5 else ""}" style="grid-template-columns:repeat({min(len(s["items"]), 3)},1fr)">{cards}</div></div></section>'


def _article(s, ctx):
    """A long-form post: header, hero image, TOC, chapters (h2 + paragraphs), pull quote, callout, author."""
    E, RAW = ctx["E"], ctx["RAW"]
    chapters = s["chapters"]
    toc = "".join(f'<a href="#{E(c["id"])}">{E(c["title"])}</a>' for c in chapters)
    body = ""
    for c in chapters:
        body += f'<h2 id="{E(c["id"])}">{E(c["title"])}</h2>' + "".join(
            (f'<p class="pq">{E(p[3:])}</p>' if p.startswith("pq:") else
             f'<div class="callout"><b>{E(p[8:].split("|")[0])}</b>{E(p[8:].split("|", 1)[1]) if "|" in p[8:] else ""}</div>' if p.startswith("callout:") else
             f'<ul>{"".join(f"<li>{E(x.strip())}</li>" for x in p[3:].split(";;"))}</ul>' if p.startswith("ul:") else
             f'<p>{RAW(p)}</p>') for p in c["paras"])
    author = s.get("author", {"name": ("The " + ctx.get("client_short", "") + " team").replace("The  team", "The team"), "role": "North Carolina"})
    hero = f'<div class="pv-art-hero"><img src="{E(ctx["rel"](s["image"]))}"{ctx["srcset"](s["image"])} alt="{E(s.get("image_alt", ""))}" width="1200" height="800" fetchpriority="high"></div>' if s.get("image") else ""
    bc = f'<nav class="pv-bc" aria-label="Breadcrumb"><a href="{E(ctx["L"]("index.html"))}">Home</a><span>/</span><a href="{E(ctx["L"]("blog.html"))}">Blog</a><span>/</span>{E(s["category"])}</nav>'
    return f'''<section class="q-section" style="padding-top:28px"><div class="q-container">{bc}<div class="pv-art-head" style="margin-top:34px"><div class="q-eyebrow" style="justify-content:center">{E(s["category"])}</div><h1 class="q-h1" style="font-size:clamp(34px,4vw,56px);margin-top:20px">{RAW(s["heading"])}</h1><p class="q-lead" style="margin:20px auto 0;max-width:640px">{E(s.get("standfirst"))}</p><div class="pv-art-meta"><span><b>{E(author["name"])}</b></span><span>{E(s.get("date_label", ""))}</span><span>{E(s.get("read", ""))}</span></div></div>{hero}</div></section>
<section class="q-section" style="padding-top:0"><div class="q-container pv-art"><aside class="pv-toc"><div class="k">In this guide</div>{toc}</aside><article class="pv-prose">{body}<div class="pv-author"><div class="av" aria-hidden="true">{E("".join(w[0] for w in author["name"].split()[:2]))}</div><p><b>{E(author["name"])}</b>{E(author.get("role", ""))}</p></div></article></div></section>'''


def _related(s, ctx):
    E = ctx["E"]
    cards = "".join(f'<a class="pv-post" href="{E(ctx["L"](h))}"><div class="ph"{f" style=background-image:url({E(ctx[chr(114)+chr(101)+chr(108)](img))});background-size:cover" if img else ""}></div><span class="tag">{E(tag)}</span><h2>{E(t)}</h2><p>{E(d)}</p></a>' for tag, t, d, h, img in s["items"])
    return f'{ctx["sec_open"](s)} <div class="q-container"><div class="pv-split"><h2 class="q-h2">{E(s.get("heading", "Keep reading"))}</h2><p>{E(s.get("intro", ""))}</p></div><div class="pv-grid pv-grid-{min(len(s["items"]), 3)}">{cards}</div></div></section>'


RENDER_EXTRA = {"hero-video": _hero_video, "video": _video, "testimonials": _testimonials, "timeline": _timeline,
                "tabs": _tabs, "calculator": _calculator, "capex-calc": _capex_calc, "comparison": _comparison, "checklist": _checklist,
                "values": _values, "proof": _proof, "map": _map, "leadership": _leadership, "sticky": _sticky, "resources": _resources,
                "article": _article, "related": _related}
