"""Creative-director layer for scripts/preview.py: dark stage sections and a few cinematic section types.

Registered in preview.py as RENDER_CD (section renderers) and CD_CSS. Pure CSS and inline SVG, no JS.
Every colour comes from the theme variables, so the three directions pick it up.

  "stage": true on any section   renders it as a dark navy stage (variables remapped, so cards, FAQs, values, leadership follow)
  spotlight   a tall photo beside a big statement and numbered needs
  tiles       photo tiles with a title over the image ("mosaic" makes the first tile large)
  callboard   phone lines with big numbers
  hqmap       a blueprint-style locator panel for one address, plus facts
  billboard   full-bleed photo with a huge statement
  badges      a labelled row of short facts

Rules: no em or en dashes (E() rewrites any that slip in), nothing under 13px, 44px tap targets, no horizontal overflow.
"""
from __future__ import annotations

import re


def _eb(E, s, center=False):
    return f'<div class="q-eyebrow"{" style=justify-content:center" if center else ""}>{E(s["eyebrow"])}</div>' if s.get("eyebrow") else ""


def _tel(n):
    return "tel:+1" + re.sub(r"\D", "", n)


def _spotlight(s, ctx):
    E, L, rel = ctx["E"], ctx["L"], ctx["rel"]
    def _need(t):
        head, sep, rest = str(t).partition(": ")
        return f'<b>{E(head)}</b><span>{E(rest)}</span>' if sep and len(head) <= 40 else E(t)
    needs = "".join(f'<li><span class="cd-n" aria-hidden="true">{i + 1:02d}</span><span class="cd-t">{_need(t)}</span></li>' for i, t in enumerate(s.get("needs", [])))
    tag = f'<span class="cd-tag">{E(s["tag"])}</span>' if s.get("tag") else ""
    cta = ""
    if s.get("cta"):
        cta = f'<a class="q-btn" href="{E(L(s["cta"]["href"]))}">{E(s["cta"]["label"])}</a>'
    img = (f'<figure class="cd-fig"><img src="{E(rel(s["image"]))}" alt="{E(s.get("image_alt", ""))}" width="1200" height="1500" loading="lazy" decoding="async">{tag}'
           f'<span class="cd-corner" aria-hidden="true"></span></figure>') if s.get("image") else ""
    return (f'{ctx["sec_open"](s, "cd-spot" + (" cd-flip" if s.get("flip") else ""))} <div class="q-container cd-grid">{img}'
            f'<div class="cd-copy">{_eb(E, s)}<h2 class="q-h2">{E(s["heading"])}</h2><p class="cd-lead">{E(s.get("body", ""))}</p>'
            f'<ol class="cd-needs">{needs}</ol>{cta}</div></div></section>')


def _tiles(s, ctx):
    E, L, rel = ctx["E"], ctx["L"], ctx["rel"]
    items = s["items"]
    n = len(items)
    mosaic = s.get("variant") == "mosaic"
    cls = [""] * n
    if mosaic and n >= 7:
        cls[0] = "big"
        left = n - 5
        if left % 4 == 2:
            cls[-1] = cls[-2] = "wide"
        elif left % 4 == 1:
            cls[-1] = "wide"
    tiles = []
    for i, it in enumerate(items):
        title, text, href, img = (list(it) + ["", "", "", ""])[:4]
        im = (f'<img src="{E(rel(img))}" alt="" width="800" height="600" loading="lazy" decoding="async">') if img else ""
        tiles.append(f'<li class="cd-tile {cls[i]}"><a href="{E(L(href))}">{im}<span class="cd-shade" aria-hidden="true"></span>'
                     f'<span class="cd-tt"><span class="cd-no" aria-hidden="true">{i + 1:02d}</span><b>{E(title)}</b><span class="cd-tx">{E(text)}</span>'
                     f'<span class="cd-go" aria-hidden="true">&#8594;</span></span></a></li>')
    head = ""
    if s.get("heading"):
        intro = f'<p class="q-lead" style="max-width:640px;margin:16px auto 0">{E(s["intro"])}</p>' if s.get("intro") else ""
        head = f'<div class="pv-center cd-head">{_eb(E, s)}<h2 class="q-h2" style="margin-top:22px;max-width:780px">{E(s["heading"])}</h2>{intro}</div>'
    return (f'{ctx["sec_open"](s, "cd-tiles")} <div class="q-container">{head}'
            f'<ul class="cd-tgrid{" cd-mosaic" if mosaic else ""}" data-n="{n}">{"".join(tiles)}</ul></div></section>')


def _callboard(s, ctx):
    E, L = ctx["E"], ctx["L"]
    cards = []
    for i, it in enumerate(s["items"]):
        mail = f'<a class="cd-mail" href="mailto:{E(it["email"])}">{E(it["email"])}</a>' if it.get("email") else ""
        cards.append(f'<li class="cd-line"><span class="cd-who">{E(it["label"])}</span><a class="cd-num" href="{E(_tel(it["number"]))}" aria-label="Call {E(it["label"])} at {E(it["number"])}">{E(it["number"])}</a>'
                     f'<p class="cd-what">{E(it["text"])}</p><span class="cd-hrs">{E(it["hours"])}</span>{mail}</li>')
    intro = f'<p class="q-lead" style="max-width:660px;margin:16px auto 0">{E(s["intro"])}</p>' if s.get("intro") else ""
    return (f'{ctx["sec_open"](s, "cd-board")} <div class="q-container"><div class="pv-center cd-head">{_eb(E, s)}'
            f'<h2 class="q-h2" style="margin-top:22px;max-width:780px">{E(s["heading"])}</h2>{intro}</div>'
            f'<ul class="cd-lines" data-n="{len(cards)}">{"".join(cards)}</ul></div></section>')


def _hqmap(s, ctx):
    E, L, rel = ctx["E"], ctx["L"], ctx["rel"]
    grid = "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="300"/>' for x in range(0, 501, 50)) + "".join(f'<line x1="0" y1="{y}" x2="500" y2="{y}"/>' for y in range(0, 301, 50))
    rings = "".join(f'<circle cx="250" cy="150" r="{r}" class="cd-ring" style="--d:{i * 0.9:.1f}s"/>' for i, r in enumerate((40, 80, 120)))
    svg = (f'<svg class="cd-radar" viewBox="0 0 500 300" role="img" aria-label="{E(s.get("map_label", "Map locator"))}" preserveAspectRatio="xMidYMid slice">'
           f'<g class="cd-gridl">{grid}</g><g>{rings}</g><line class="cd-cross" x1="250" y1="0" x2="250" y2="300"/><line class="cd-cross" x1="0" y1="150" x2="500" y2="150"/>'
           f'<circle class="cd-pin-halo" cx="250" cy="150" r="12"/><circle class="cd-pin" cx="250" cy="150" r="6"/></svg>')
    facts = "".join(f'<li><span>{E(k)}</span><b>{E(v)}</b></li>' for k, v in s.get("facts", []))
    chips = "".join(f'<span>{E(c)}</span>' for c in s.get("chips", []))
    photo = (f'<img class="cd-hqimg" src="{E(rel(s["image"]))}" alt="{E(s.get("image_alt", ""))}" width="1200" height="800" loading="lazy" decoding="async">') if s.get("image") else ""
    return (f'{ctx["sec_open"](s, "cd-hq")} <div class="q-container cd-hqgrid"><div class="cd-map">{svg}<div class="cd-coord"><span>{E(s.get("coords", ""))}</span><b>{E(s.get("place", ""))}</b></div>'
            f'<div class="cd-chips">{chips}</div></div>'
            f'<div class="cd-hqcopy">{_eb(E, s)}<h2 class="q-h2">{E(s["heading"])}</h2><p class="cd-lead">{E(s.get("body", ""))}</p>'
            f'<ul class="cd-facts">{facts}</ul>{photo}</div></div></section>')


def _billboard(s, ctx):
    E, L, rel = ctx["E"], ctx["L"], ctx["rel"]
    stats = "".join(f'<div><b>{E(v)}</b><span>{E(k)}</span></div>' for v, k in s.get("stats", []))
    stats = f'<div class="cd-bstats">{stats}</div>' if stats else ""
    src = f'<p class="cd-src">{E(s["source"])}</p>' if s.get("source") else ""
    btn = f'<a class="q-btn" href="{E(L(s["cta"]["href"]))}">{E(s["cta"]["label"])}</a>' if s.get("cta") else ""
    return (f'{ctx["sec_open"]({**s, "stage": True}, "cd-bill")}<img class="cd-bimg" src="{E(rel(s["image"]))}" alt="{E(s.get("image_alt", ""))}" width="2100" height="900" loading="lazy" decoding="async">'
            f'<span class="cd-bshade" aria-hidden="true"></span><div class="q-container cd-bcopy">{_eb(E, s)}<h2 class="cd-big">{E(s["heading"])}</h2>'
            f'<p class="cd-blead">{E(s.get("text", ""))}</p>{src}{btn}{stats}</div></section>')


def _badges(s, ctx):
    E = ctx["E"]
    cells = "".join(f'<li><b>{E(v)}</b><span>{E(k)}</span></li>' for v, k in s["items"])
    lab = f'<span class="cd-blab">{E(s["label"])}</span>' if s.get("label") else ""
    note = f'<span class="cd-bnote">{E(s["note"])}</span>' if s.get("note") else ""
    return f'{ctx["sec_open"](s, "cd-badges")} <div class="q-container"><div class="cd-brow">{lab}<ul>{cells}</ul>{note}</div></div></section>'


RENDER_CD = {"spotlight": _spotlight, "tiles": _tiles, "callboard": _callboard, "hqmap": _hqmap, "billboard": _billboard, "badges": _badges}


CD_CSS = r"""
/* ===== creative-director layer ===== */
.q-section.pv-dark{--bg:#0b1220;--bg-alt:#121c30;--fg:#f4f6fb;--fg-muted:#b7c0d3;--card:rgba(255,255,255,.06);--border:rgba(255,255,255,.14);--accent-ink:color-mix(in srgb,var(--q-gold) 78%,#fff);
  position:relative;overflow:hidden;overflow:clip;isolation:isolate;color:var(--fg);border-bottom-color:rgba(255,255,255,.08);
  background:radial-gradient(1000px 420px at 12% -6%,color-mix(in srgb,var(--q-gold) 18%,transparent),transparent 70%),radial-gradient(900px 500px at 100% 110%,rgba(80,120,255,.12),transparent 70%),linear-gradient(180deg,#0b1220,#101a2e)}
.q-section.pv-dark::before{content:"";position:absolute;inset:0;z-index:-1;pointer-events:none;background:repeating-linear-gradient(90deg,rgba(255,255,255,.035) 0 1px,transparent 1px 96px);-webkit-mask-image:linear-gradient(180deg,transparent,#000 25%,#000 75%,transparent);mask-image:linear-gradient(180deg,transparent,#000 25%,#000 75%,transparent)}
.pv-dark .q-h2,.pv-dark .q-h1,.pv-dark h3{color:#fff}
.pv-dark .q-lead,.pv-dark p{color:var(--fg-muted)}
.pv-dark .q-card,.pv-dark .pv-tilt,.pv-dark .pv-svc a{background:var(--card);border:1px solid var(--border);box-shadow:none;color:var(--fg)}
.pv-dark .q-card p,.pv-dark .pv-tilt p{color:var(--fg-muted)}
.pv-dark .q-btn-ghost{color:#fff;border-color:rgba(255,255,255,.35)}
.pv-dark .pv-faq summary,.pv-dark .pv-faq details p{color:var(--fg)}
.pv-dark a:not(.q-btn):not(.q-btn-ghost){color:inherit}
.pv-dark .pv-detail li,.pv-dark li{color:var(--fg-muted)}
.pv-dark .pv-detail img{box-shadow:0 30px 80px rgba(0,0,0,.45)}
/* values on a stage: big counted numerals */
.pv-dark .pv-values{counter-reset:cdv;gap:22px}
.pv-dark .pv-values .q-card{counter-increment:cdv;position:relative;padding:34px 30px 32px;overflow:hidden;transition:transform .3s,border-color .3s,background .3s}
.pv-dark .pv-values .q-card::before{content:counter(cdv,decimal-leading-zero);display:block;font-family:var(--q-sans);font-weight:800;font-size:64px;line-height:1;letter-spacing:-.04em;color:transparent;-webkit-text-stroke:1.5px color-mix(in srgb,var(--q-gold) 80%,#fff);margin-bottom:18px}
.pv-dark .pv-values .q-card:hover{transform:translateY(-6px);border-color:var(--q-gold);background:rgba(255,255,255,.09)}
.pv-dark .pv-values .q-card h3{font-size:24px;margin:0 0 10px}
.pv-dark .pv-values .q-card p{font-size:16px;line-height:1.6}
/* leadership on a stage: portrait tiles */
.pv-dark .pv-lead{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px}
.pv-dark .pv-lead .q-card{display:flex;flex-direction:column;align-items:flex-start;gap:26px;padding:22px 22px 24px;min-height:210px;transition:transform .3s,border-color .3s}
.pv-dark .pv-lead .q-card:hover{transform:translateY(-5px);border-color:var(--q-gold)}
.pv-dark .pv-lead .av{width:76px;height:76px;border-radius:18px;font-family:var(--q-sans);font-weight:800;font-size:26px;letter-spacing:-.02em;color:var(--cta-fg);background:linear-gradient(135deg,var(--q-gold),color-mix(in srgb,var(--q-gold) 55%,#fff));display:grid;place-items:center}
.pv-dark .pv-lead .q-card h3{font-size:20px;margin:0 0 6px}
.pv-dark .pv-lead .q-card p{font-size:14.5px;line-height:1.45;margin:0}
.pv-dark .pv-lead .q-card:last-child:nth-child(4n){grid-column:span 2}.pv-dark .pv-lead .q-card:first-child{grid-column:1/-1;flex-direction:row;align-items:center;min-height:0;gap:24px}
.pv-dark .pv-lead .q-card:first-child .av{width:104px;height:104px;font-size:36px;flex:none}
.pv-dark .pv-lead .q-card:first-child h3{font-size:28px}
.pv-dark .pv-orgs span{background:rgba(255,255,255,.06);border-color:var(--border);color:var(--fg)}
@media(max-width:1024px){.pv-dark .pv-lead{grid-template-columns:repeat(2,minmax(0,1fr))}.pv-dark .pv-lead .q-card:last-child:nth-child(4n){grid-column:auto}}
@media(max-width:600px){.pv-dark .pv-lead{grid-template-columns:1fr}.pv-dark .pv-lead .q-card:first-child{grid-column:auto}.pv-dark .pv-lead .q-card{min-height:0;flex-direction:row;align-items:center;gap:18px}.pv-dark .pv-lead .av{width:60px;height:60px;font-size:22px}.pv-dark .pv-lead .q-card:first-child .av{width:60px;height:60px;font-size:22px}.pv-dark .pv-lead .q-card:first-child h3{font-size:20px}.pv-dark .pv-values .q-card::before{font-size:48px}}

/* spotlight */
.cd-spot .cd-grid{display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr);gap:clamp(32px,5vw,80px);align-items:center}
.cd-spot.cd-flip .cd-grid{grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr)}.cd-spot.cd-flip .cd-fig{order:2}
.cd-fig{position:relative;margin:0;border-radius:calc(var(--radius) + 10px);aspect-ratio:4/5;max-height:640px;width:100%;box-shadow:0 40px 90px rgba(0,5,69,.28)}
.cd-fig img{width:100%;height:100%;object-fit:cover;display:block;border-radius:inherit}
.cd-fig::before{content:"";position:absolute;inset:-14px 14px 14px -14px;border:2px solid var(--q-gold);border-radius:inherit;z-index:-1}
.cd-fig::after{content:"";position:absolute;inset:0;border-radius:inherit;background:linear-gradient(180deg,transparent 55%,rgba(5,10,24,.55));pointer-events:none}
.cd-tag{position:absolute;left:18px;bottom:18px;z-index:2;max-width:calc(100% - 36px);padding:10px 16px;border-radius:999px;background:var(--q-gold);color:var(--cta-fg);font-weight:800;font-size:14px;letter-spacing:.04em;text-transform:uppercase}
.cd-copy{min-width:0}.cd-copy .q-h2{margin-top:22px;font-size:clamp(34px,4vw,56px);line-height:1.02}
.cd-lead{font-size:clamp(17px,1.5vw,20px);line-height:1.65;color:var(--fg-muted);margin:22px 0 28px;max-width:620px}
.cd-needs{list-style:none;margin:0 0 30px;padding:0;display:grid;gap:0;counter-reset:n}
.cd-needs li{display:grid;grid-template-columns:64px minmax(0,1fr);gap:14px;align-items:start;padding:18px 0;border-top:1px solid var(--border)}
.cd-needs li:last-child{border-bottom:1px solid var(--border)}
.cd-n{font-family:var(--q-sans);font-weight:800;font-size:34px;line-height:1;letter-spacing:-.03em;color:transparent;-webkit-text-stroke:1.4px var(--accent-ink)}
.cd-t{font-size:17px;line-height:1.5;color:var(--fg);font-weight:600;overflow-wrap:anywhere;display:grid;gap:2px}.cd-t b{font-size:19px;font-weight:800}.cd-t span{font-weight:400;color:var(--fg-muted);font-size:16px}
.pv-dark .cd-t{color:#fff}.pv-dark .cd-fig::before{border-color:color-mix(in srgb,var(--q-gold) 70%,transparent)}.pv-dark .cd-fig{box-shadow:0 40px 90px rgba(0,0,0,.5)}
@media(max-width:900px){.cd-spot .cd-grid,.cd-spot.cd-flip .cd-grid{grid-template-columns:1fr}.cd-spot.cd-flip .cd-fig{order:0}.cd-fig{aspect-ratio:16/10;max-height:none}.cd-fig::before{inset:-8px 8px 8px -8px}.cd-needs li{grid-template-columns:48px minmax(0,1fr)}.cd-n{font-size:28px}}

/* tiles */
.cd-head{margin-bottom:44px}
.cd-tgrid{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px}
.cd-tgrid[data-n="3"]{grid-template-columns:repeat(3,minmax(0,1fr))}.cd-tgrid[data-n="6"]{grid-template-columns:repeat(3,minmax(0,1fr))}.cd-tgrid[data-n="2"]{grid-template-columns:repeat(2,minmax(0,1fr))}
.cd-mosaic{grid-auto-rows:minmax(0,1fr)}
.cd-tile a{position:relative;display:block;height:100%;min-height:300px;border-radius:calc(var(--radius) + 6px);overflow:hidden;color:#fff;text-decoration:none;background:#0b1220;isolation:isolate;box-shadow:0 18px 44px rgba(0,5,69,.18);transition:transform .35s,box-shadow .35s}
.cd-tgrid[data-n="4"] .cd-tile a{min-height:400px}.cd-tile.big{grid-column:span 2;grid-row:span 2}.cd-tile.big a{min-height:620px}.cd-tile.wide{grid-column:span 2}
.cd-tile img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform .8s cubic-bezier(.2,.7,.2,1);z-index:-2}
.cd-tile a:hover{transform:translateY(-5px);box-shadow:0 28px 60px rgba(0,5,69,.3)}.cd-tile a:hover img{transform:scale(1.07)}
.cd-shade{position:absolute;inset:0;z-index:-1;background:linear-gradient(180deg,rgba(5,10,24,.05) 25%,rgba(5,10,24,.88) 100%)}
.cd-tt{position:absolute;left:0;right:0;bottom:0;padding:22px 22px 20px;display:grid;gap:6px;justify-items:start}
.cd-tt b{font-family:var(--q-sans);font-weight:800;font-size:clamp(20px,1.7vw,26px);line-height:1.12;letter-spacing:-.02em;color:#fff}.cd-tile.big .cd-tt b{font-size:clamp(28px,2.8vw,40px)}
.cd-no{font-size:13px;font-weight:800;letter-spacing:.16em;color:var(--q-gold)}
.cd-tx{font-size:14.5px;line-height:1.45;color:rgba(255,255,255,.84);display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;max-height:0;opacity:0;transition:max-height .4s,opacity .4s}
.cd-tile.big .cd-tx,.cd-tile.wide .cd-tx{max-height:5em;opacity:1}
.cd-tile a:hover .cd-tx,.cd-tile a:focus-visible .cd-tx{max-height:5em;opacity:1}
.cd-go{position:absolute;right:18px;top:-48px;width:44px;height:44px;border-radius:50%;background:var(--q-gold);color:var(--cta-fg);display:grid;place-items:center;font-weight:800;transform:translateX(8px);opacity:0;transition:.3s}
.cd-tile a:hover .cd-go,.cd-tile a:focus-visible .cd-go{opacity:1;transform:none}.cd-tile a:focus-visible{outline:3px solid var(--q-gold);outline-offset:3px}
@media(hover:none){.cd-tx{max-height:5em;opacity:1}.cd-go{opacity:1;transform:none}}
@media(max-width:1024px){.cd-tgrid,.cd-tgrid[data-n]{grid-template-columns:repeat(2,minmax(0,1fr))}.cd-tile.big a{min-height:420px}.cd-tile a{min-height:260px}}
@media(max-width:600px){.cd-tgrid,.cd-tgrid[data-n]{grid-template-columns:1fr}.cd-tile.big,.cd-tile.wide{grid-column:auto;grid-row:auto}.cd-tile.big a,.cd-tile a{min-height:240px}}

/* callboard */
.cd-lines{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}.cd-lines[data-n="3"]{grid-template-columns:repeat(3,minmax(0,1fr))}.cd-lines[data-n="3"] .cd-num{font-size:clamp(28px,3vw,42px)}
.cd-line{position:relative;display:flex;flex-direction:column;gap:10px;padding:30px 32px 28px;border:1px solid var(--border);border-radius:calc(var(--radius) + 6px);background:var(--card);box-shadow:0 14px 36px rgba(0,5,69,.08);overflow:hidden;transition:transform .3s,border-color .3s}.pv-dark .cd-line{background:linear-gradient(160deg,rgba(255,255,255,.09),rgba(255,255,255,.03));box-shadow:none}
.cd-line::before{content:"";position:absolute;left:0;top:0;bottom:0;width:5px;background:var(--q-gold)}
.cd-line:hover{transform:translateY(-4px);border-color:var(--q-gold)}
.cd-who{font-size:14px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--accent-ink)}
.cd-num{font-family:var(--q-sans);font-weight:800;font-size:clamp(34px,4.4vw,60px);line-height:1;letter-spacing:-.03em;color:var(--fg);text-decoration:none;display:inline-block;min-height:44px;overflow-wrap:anywhere}
.pv-dark .cd-num{color:#fff}.cd-num:hover,.pv-dark .cd-num:hover{color:var(--q-gold)}.cd-num:focus-visible{outline:3px solid var(--q-gold);outline-offset:4px}
.cd-what{margin:0;font-size:17px;line-height:1.55;color:var(--fg-muted);max-width:480px}
.cd-hrs{align-self:flex-start;margin-top:4px;padding:7px 14px;border-radius:999px;border:1px solid var(--border);font-size:14px;font-weight:700;color:var(--fg);background:var(--bg-alt)}.pv-dark .cd-hrs{background:rgba(255,255,255,.06)}
.cd-mail{font-size:15px;color:var(--fg-muted);text-decoration:underline;text-underline-offset:3px;overflow-wrap:anywhere;min-height:24px}
@media(max-width:1024px){.cd-lines[data-n="3"]{grid-template-columns:1fr}}
@media(max-width:800px){.cd-lines{grid-template-columns:1fr}.cd-line{padding:26px 22px 24px 26px}}

/* headquarters locator */
.cd-hqgrid{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,.95fr);gap:clamp(32px,5vw,72px);align-items:center}
.cd-map{position:relative;border-radius:calc(var(--radius) + 10px);overflow:hidden;background:#07101f;border:1px solid rgba(255,255,255,.14);box-shadow:0 40px 90px rgba(0,5,69,.35);aspect-ratio:5/4;min-height:300px}
.cd-radar{position:absolute;inset:0;width:100%;height:100%;display:block}
.cd-gridl{stroke:rgba(255,255,255,.09);stroke-width:1}.cd-cross{stroke:color-mix(in srgb,var(--q-gold) 55%,transparent);stroke-width:1;stroke-dasharray:4 6}
.cd-ring{fill:none;stroke:color-mix(in srgb,var(--q-gold) 60%,transparent);stroke-width:1.2;transform-origin:250px 150px;animation:cdring 3.6s ease-out infinite;animation-delay:var(--d)}
.cd-pin{fill:var(--q-gold)}.cd-pin-halo{fill:color-mix(in srgb,var(--q-gold) 30%,transparent);transform-origin:250px 150px;animation:cdhalo 2.2s ease-in-out infinite}
@keyframes cdring{0%{transform:scale(.4);opacity:0}25%{opacity:.9}100%{transform:scale(1.9);opacity:0}}@keyframes cdhalo{50%{transform:scale(1.8);opacity:.4}}
@media(prefers-reduced-motion:reduce){.cd-ring,.cd-pin-halo{animation:none}.cd-tile img{transition:none}}
.cd-coord{position:absolute;left:22px;top:20px;display:grid;gap:2px;font-family:ui-monospace,Menlo,Consolas,monospace}
.cd-coord span{font-size:13px;letter-spacing:.16em;color:var(--q-gold)}.cd-coord b{font-family:var(--q-sans);font-size:clamp(22px,2.4vw,32px);color:#fff;letter-spacing:-.02em}
.cd-chips{position:absolute;left:18px;right:18px;bottom:16px;display:flex;flex-wrap:wrap;gap:8px}
.cd-chips span{padding:7px 13px;border-radius:999px;border:1px solid rgba(255,255,255,.22);background:rgba(7,16,31,.7);color:#fff;font-size:13px;font-weight:700}
.cd-hqcopy .q-h2{margin-top:22px;font-size:clamp(32px,3.6vw,50px);line-height:1.04}
.cd-facts{list-style:none;margin:0 0 24px;padding:0;display:grid;gap:0}
.cd-facts li{display:grid;grid-template-columns:130px minmax(0,1fr);gap:16px;padding:14px 0;border-top:1px solid var(--border);align-items:baseline}
.cd-facts li:last-child{border-bottom:1px solid var(--border)}
.cd-facts span{font-size:13px;letter-spacing:.12em;text-transform:uppercase;font-weight:800;color:var(--accent-ink)}.cd-facts b{font-size:18px;line-height:1.4;color:var(--fg);font-weight:700;overflow-wrap:anywhere}
.pv-dark .cd-facts b{color:#fff}
.cd-hqimg{width:100%;aspect-ratio:16/8;object-fit:cover;border-radius:var(--radius);display:block}
@media(max-width:900px){.cd-hqgrid{grid-template-columns:1fr}.cd-facts li{grid-template-columns:1fr;gap:4px}.cd-map{aspect-ratio:4/3}}

/* billboard */
.cd-bill{padding:0!important;min-height:min(78vh,720px);display:flex;align-items:flex-end}
.cd-bimg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:-2}
.cd-bshade{position:absolute;inset:0;z-index:-1;background:linear-gradient(90deg,rgba(5,10,24,.88) 0%,rgba(5,10,24,.55) 55%,rgba(5,10,24,.2) 100%),linear-gradient(180deg,transparent 50%,rgba(5,10,24,.7))}
.q-section.cd-bill::before{display:none}
.cd-bcopy{width:100%;padding-top:96px;padding-bottom:84px}
.cd-big{font-family:var(--q-sans);font-weight:800;font-size:clamp(40px,7vw,104px);line-height:.98;letter-spacing:-.045em;color:#fff;margin:22px 0 0;max-width:12em;text-wrap:balance}
.cd-blead{font-size:clamp(17px,1.6vw,22px);line-height:1.6;color:rgba(255,255,255,.86)!important;max-width:640px;margin:26px 0 0}
.cd-src{font-size:14px;color:rgba(255,255,255,.7)!important;margin:12px 0 0}
.cd-bill .q-btn{margin-top:28px}
.cd-bstats{display:flex;flex-wrap:wrap;gap:0;margin-top:44px;border-top:1px solid rgba(255,255,255,.2)}
.cd-bstats div{flex:1 1 150px;padding:18px 24px 0 0;display:grid;gap:4px;align-content:start}.cd-bstats b{font-family:var(--q-sans);font-size:clamp(28px,3.2vw,46px);font-weight:800;color:var(--q-gold);letter-spacing:-.03em;line-height:1}.cd-bstats span{font-size:14px;color:rgba(255,255,255,.78)}

/* badges */
.cd-badges{padding:26px 0!important}
.cd-brow{display:flex;flex-wrap:wrap;gap:14px 28px;align-items:center}
.cd-blab{font-size:13px;letter-spacing:.16em;text-transform:uppercase;font-weight:800;color:var(--accent-ink)}
.cd-brow ul{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px;flex:1 1 100%}
.cd-brow li{display:flex;flex-direction:column;gap:2px;padding:12px 18px;border:1px solid var(--border);border-left:4px solid var(--q-gold);border-radius:10px;background:var(--card)}
.cd-brow li b{font-size:18px;font-weight:800;color:var(--fg)}.cd-brow li span{font-size:14px;color:var(--fg-muted)}
.cd-bnote{flex-basis:100%;font-size:13.5px;color:var(--fg-muted)}
[data-dir="press"] .cd-fig,[data-dir="press"] .cd-tile a,[data-dir="press"] .cd-line,[data-dir="press"] .cd-map{border-radius:2px}
"""
