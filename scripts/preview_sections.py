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
.pv-hero-video{position:relative;overflow:hidden;background:var(--chrome-bg);color:#fff}
.pv-hero-video video,.pv-hero-video .pv-poster{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.42}
.pv-hero-video .q-container{position:relative;z-index:1;padding-top:96px;padding-bottom:96px}
.pv-hero-video .q-h1,.pv-hero-video .q-lead{color:#fff}
.pv-hero-video .q-eyebrow{color:var(--q-gold)}.pv-hero-video .q-eyebrow::before{background:var(--q-gold)}
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
.pv-tl2{position:relative;margin:52px auto 0;max-width:1040px;display:grid;gap:28px}
.pv-tl2 .line{position:absolute;left:50%;top:10px;bottom:10px;width:2px;background:var(--border);transform:translateX(-1px)}
.pv-tl2 .ev{display:grid;grid-template-columns:1fr 1fr;align-items:center;position:relative}
.pv-tl2 .dot{position:absolute;left:50%;top:50%;width:18px;height:18px;border-radius:50%;background:var(--q-gold);border:4px solid var(--bg);transform:translate(-50%,-50%);z-index:2;box-shadow:0 0 0 2px var(--border)}
.pv-tl2 .card{background:var(--card,var(--bg));border:1px solid var(--border);border-radius:calc(var(--radius) + 4px);padding:22px 26px;box-shadow:0 14px 34px rgba(0,0,0,.07);position:relative}
.pv-tl2 .ev.l .card{grid-column:1;margin-right:48px}.pv-tl2 .ev.r .card{grid-column:2;margin-left:48px}
.pv-tl2 .ev.l .card::after,.pv-tl2 .ev.r .card::after{content:"";position:absolute;top:50%;width:48px;height:2px;background:var(--border);transform:translateY(-1px)}.pv-tl2 .ev.l .card::after{right:-48px}.pv-tl2 .ev.r .card::after{left:-48px}
.pv-tl2 .y{font-family:var(--q-serif);font-size:34px;line-height:1;color:var(--accent-ink);font-weight:700}
.pv-tl2 h3{font-size:18px;font-weight:700;margin:10px 0 6px;color:var(--fg)}.pv-tl2 p{font-size:15px;line-height:1.6;color:var(--fg-muted);margin:0}
@media(max-width:767px){.pv-tl2 .line{left:14px}.pv-tl2 .ev{grid-template-columns:1fr}.pv-tl2 .ev.l .card,.pv-tl2 .ev.r .card{grid-column:1;margin:0 0 0 40px}.pv-tl2 .ev.l .card::after,.pv-tl2 .ev.r .card::after{left:-26px;width:26px}.pv-tl2 .dot{left:14px}}
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
.pv-calc .big{background:var(--chrome-bg);color:#fff;border-radius:var(--radius);padding:28px}
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
.pv-lead{display:grid;grid-template-columns:repeat(2,1fr);gap:20px}
.pv-lead .q-card{display:grid;grid-template-columns:96px 1fr;gap:20px;align-items:center}
.pv-lead .av{width:96px;height:96px;border-radius:50%;background:linear-gradient(135deg,var(--bg-alt),var(--border));display:flex;align-items:center;justify-content:center;font-family:var(--q-serif);font-size:30px;color:var(--accent-ink)}
.pv-lead h3{font-family:var(--q-serif);font-size:20px;margin:0 0 4px;color:var(--fg)}.pv-lead p{font-size:14.5px;color:var(--fg-muted);margin:0;line-height:1.6}
.pv-orgs{display:flex;flex-wrap:wrap;gap:10px;margin-top:22px}
.pv-orgs span{border:1px solid var(--border);border-radius:999px;padding:8px 14px;font-size:14px;color:var(--fg);min-height:36px;display:inline-flex;align-items:center}
/* ===== sticky mobile cta ===== */
.pv-sticky{display:none}
@media(max-width:767px){.pv-sticky{display:grid;grid-template-columns:1fr 1fr;gap:8px;position:fixed;left:10px;right:10px;bottom:10px;z-index:85}.pv-sticky a{min-height:48px;display:flex;align-items:center;justify-content:center;border-radius:999px;font-weight:600;font-size:15px;white-space:nowrap;padding:0 12px;text-decoration:none;box-shadow:0 10px 30px rgba(0,0,0,.18)}.pv-sticky .a{background:var(--q-gold);color:var(--cta-fg)}.pv-sticky .b{background:var(--chrome-bg);color:#fff}
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
.pv-author .av{width:56px;height:56px;border-radius:50%;background:var(--chrome-bg);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700}
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
    if s.get("vimeo") or s.get("youtube"):
        if s.get("vimeo"):
            src = f'https://player.vimeo.com/video/{E(s["vimeo"])}?title=0&byline=0&portrait=0&dnt=1&autoplay=1'
        else:
            src = f'https://www.youtube-nocookie.com/embed/{E(s["youtube"])}?rel=0&modestbranding=1&autoplay=1'
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
    E = ctx["E"]
    items = "".join(f'<div class="ev {"l" if i % 2 == 0 else "r"}"><div class="dot" aria-hidden="true"></div><div class="card"><div class="y">{E(y)}</div><h3>{E(tt)}</h3><p>{E(d)}</p></div></div>' for i, (y, tt, d) in enumerate(s["items"]))
    return f'{ctx["sec_open"](s)} <div class="q-container"><div class="pv-center"><div class="q-eyebrow">{E(s.get("eyebrow"))}</div><h2 class="q-h2" style="margin-top:22px;max-width:760px">{E(s["heading"])}</h2></div><div class="pv-tl2"><div class="line" aria-hidden="true"></div>{items}</div></div></section>'


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


# Indiana outline, lon/lat, simplified. Selected with "outline": "IN" on the map section.
IN_OUTLINE = [(-87.53, 41.71), (-87.52, 41.30), (-87.53, 40.49), (-87.53, 39.35), (-87.60, 39.10), (-87.58, 38.87), (-87.50, 38.74), (-87.65, 38.57),
              (-87.75, 38.42), (-87.93, 38.26), (-88.03, 37.80), (-87.90, 37.92), (-87.62, 37.90), (-87.40, 37.94), (-87.13, 37.78), (-86.80, 37.99),
              (-86.52, 37.92), (-86.33, 38.19), (-86.07, 37.96), (-85.90, 38.02), (-85.65, 38.33), (-85.42, 38.73), (-85.20, 38.69), (-84.79, 38.79),
              (-84.81, 39.10), (-84.82, 40.00), (-84.80, 41.00), (-84.81, 41.70), (-85.50, 41.76), (-86.50, 41.76), (-87.53, 41.71)]
OUTLINES = {"NC": (None, 35.5, 84.4, 36.65), "IN": (None, 39.8, 88.1, 41.85)}


def _map(s, ctx):
    """Service-area map: a state outline with a pin per branch, and the branch list beside it."""
    E = ctx["E"]
    import math
    state = s.get("outline", "NC")
    _, lat0, lon_off, lat_top = OUTLINES[state]
    kx = math.cos(math.radians(lat0))
    def proj(lon, lat):
        return ((lon + lon_off) * kx * 100, (lat_top - lat) * 100)
    pts = [proj(*p) for p in (IN_OUTLINE if state == "IN" else NC_OUTLINE)]
    xs = [x for x, _ in pts]; ys = [y for _, y in pts]
    w, h = max(xs) - min(xs) + 40, max(ys) - min(ys) + 40
    ox, oy = min(xs) - 20, min(ys) - 20
    path = "M" + " L".join(f"{x - ox:.1f},{y - oy:.1f}" for x, y in pts) + " Z"
    pins, rows = [], []
    for it in s["items"]:
        name, lon, lat, href, sub, hq = it["name"], it["lon"], it["lat"], it["href"], it.get("sub", ""), it.get("hq", False)
        x, y = proj(lon, lat); x -= ox; y -= oy
        dx, dy = it.get("label_dx", 10), it.get("label_dy", 4)
        pins.append(f'<circle class="ring" cx="{x:.1f}" cy="{y:.1f}" r="{s.get("ring", 42)}"/><circle class="pin{" hq" if hq else ""}" cx="{x:.1f}" cy="{y:.1f}" r="5.5"/><text x="{x + dx:.1f}" y="{y + dy:.1f}">{E(name)}</text>')
        rows.append(f'<li><div><b>{E(name)}{" (headquarters)" if hq else ""}</b><small>{E(sub)}</small></div><a href="{E(ctx["L"](href))}">{E(it.get("link", "Branch page"))}</a></li>')
    svg = f'<svg class="pv-map-svg" viewBox="0 0 {w:.0f} {h:.0f}" role="img" aria-label="{E(s.get("alt", "Map of " + ("Indiana" if state == "IN" else "North Carolina") + " with " + ctx["brand"].get("short", "branch") + " locations"))}"><path class="land" d="{path}"/>{"".join(pins)}</svg>'
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
    return f'{ctx["sec_open"](s)} <div class="q-container"><div class="pv-split"><h2 class="q-h2">{E(s["heading"])}</h2><p>{E(s.get("intro"))}</p></div><div class="pv-lead">{people}</div>{orgs_html}</div></section>'


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
    author = s.get("author", {"name": "The Kelly team", "role": "Service and sales, North Carolina"})
    hero = f'<div class="pv-art-hero"><img src="{E(ctx["rel"](s["image"]))}"{ctx["srcset"](s["image"])} alt="{E(s.get("image_alt", ""))}" width="1200" height="800" fetchpriority="high"></div>' if s.get("image") else ""
    bc = f'<nav class="pv-bc" aria-label="Breadcrumb"><a href="{E(ctx["L"]("index.html"))}">Home</a><span>/</span><a href="{E(ctx["L"]("blog.html"))}">Blog</a><span>/</span>{E(s["category"])}</nav>'
    return f'''<section class="q-section" style="padding-top:28px"><div class="q-container">{bc}<div class="pv-art-head" style="margin-top:34px"><div class="q-eyebrow" style="justify-content:center">{E(s["category"])}</div><h1 class="q-h1" style="font-size:clamp(34px,4vw,56px);margin-top:20px">{RAW(s["heading"])}</h1><p class="q-lead" style="margin:20px auto 0;max-width:640px">{E(s.get("standfirst"))}</p><div class="pv-art-meta"><span><b>{E(author["name"])}</b></span><span>{E(s.get("date_label", ""))}</span><span>{E(s.get("read", ""))}</span></div></div>{hero}</div></section>
<section class="q-section" style="padding-top:0"><div class="q-container pv-art"><aside class="pv-toc"><div class="k">In this guide</div>{toc}</aside><article class="pv-prose">{body}<div class="pv-author"><div class="av" aria-hidden="true">{E("".join(w[0] for w in author["name"].split()[:2]))}</div><p><b>{E(author["name"])}</b>{E(author.get("role", ""))}</p></div></article></div></section>'''


def _related(s, ctx):
    E = ctx["E"]
    cards = "".join(f'<a class="pv-post" href="{E(ctx["L"](h))}"><div class="ph"{f" style=background-image:url({E(ctx[chr(114)+chr(101)+chr(108)](img))});background-size:cover" if img else ""}></div><span class="tag">{E(tag)}</span><h2>{E(t)}</h2><p>{E(d)}</p></a>' for tag, t, d, h, img in s["items"])
    return f'{ctx["sec_open"](s)} <div class="q-container"><div class="pv-split"><h2 class="q-h2">{E(s.get("heading", "Keep reading"))}</h2><p>{E(s.get("intro", ""))}</p></div><div class="pv-grid pv-grid-{min(len(s["items"]), 3)}">{cards}</div></div></section>'


RENDER_EXTRA = {"hero-video": _hero_video, "video": _video, "testimonials": _testimonials, "timeline": _timeline,
                "tabs": _tabs, "calculator": _calculator, "comparison": _comparison, "checklist": _checklist,
                "values": _values, "proof": _proof, "map": _map, "leadership": _leadership, "sticky": _sticky, "resources": _resources,
                "article": _article, "related": _related}
