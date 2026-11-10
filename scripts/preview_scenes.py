"""Scenes: six pinned places (school corridor, office lobby, parking lot, server aisle, bank branch, campus), one DMP
product in each. Showcase home page only, and only for DMP (the section type pn-scenes is named by brands/dmp_night.py).

  RENDER_SCENES  {"pn-scenes": renderer}
  assets         brands/digital-monitoring-products.assets/scenes/scenes.css and scenes.js, linked from the section

How it differs from the prototype it came from
  * product first: each scene opens on the product, large and centred, then the product moves to its side and the copy
    arrives. At rest the product fills its own half of the screen instead of sitting above the copy.
  * the light leak is a layer above the product (screen blend), so the scene's light falls on the hardware.
  * portrait: product on top, copy underneath, and a scene whose copy does not fit the screen is simply not pinned.
  * CSS is the whole effect. scenes.js only maps scroll to one custom property per scene (transform and opacity on three
    elements), is off under reduced motion, and has a frame-time guard. The prototype's WebGL path is not shipped.
  * no counters, no fixed full-page stage: the section sits in the page like any other.

The environment plates are the AI-generated placeholders already used on the heroes (assets/env), captioned as illustrative.
"""
from __future__ import annotations

from preview_panel import MARK_A, MARK_B


def _scene(i, sc, ctx):
    E, L, rel, RAW = ctx["E"], ctx["L"], ctx["rel"], ctx["RAW"]
    n = i + 1
    env = sc["env"]                                   # assets/env/env-01-school-corridor-1280.jpg
    base = env.replace("-1280.jpg", "")
    pw, ph = sc["size"]
    img = sc["image"]
    small = img.replace(".png", "-600.png")
    stats = ""
    for st in sc.get("stats", []):
        soon = ' class="scn-soon"' if len(st) > 2 and st[2] else ""
        stats += f"<div{soon}><dt>{E(st[1])}</dt><dd>{E(st[0])}</dd></div>"
    go = "".join(f'<a href="{E(L(h))}">{E(t)} <span aria-hidden="true">&rarr;</span></a>' for t, h in sc.get("links", []))
    leak = sc.get("leak") or [18, 8]
    return f'''<article class="scn" id="scn-{n}"{f' data-zone="{int(sc["zone"])}"' if sc.get("zone") else ""} data-side="{E(sc.get("side", "r"))}" aria-labelledby="scn-{n}-h" style="--lx:{leak[0]}%;--ly:{leak[1]}%">
<div class="scn-pin">
<img class="scn-env" src="{E(rel(base + "-800.jpg"))}" srcset="{E(rel(base + "-800.jpg"))} 800w, {E(rel(env))} 1280w, {E(rel(base + "-1920.jpg"))} 1920w" sizes="100vw" alt="{E(sc["env_alt"])}" width="1920" height="1086" loading="lazy" decoding="async">
<div class="scn-scrim" aria-hidden="true"></div>
<figure class="scn-prod"><a href="{E(L(sc["href"]))}"><img src="{E(rel(img))}" srcset="{E(rel(small))} 600w, {E(rel(img))} {pw}w" sizes="(max-width: 899px) 88vw, 44vw" alt="{E(sc["alt"])}" width="{pw}" height="{ph}" loading="lazy" decoding="async"></a>
<figcaption class="scn-label"><i aria-hidden="true"></i>{E(sc["label"])}</figcaption></figure>
<div class="scn-leak" aria-hidden="true"></div>
<div class="scn-col">
<p class="scn-k"><b>{n:02d}</b> {E(sc["place"])} <span aria-hidden="true">/</span> {E(sc["system"])}</p>
<h3 id="scn-{n}-h">{RAW(sc["heading"])}</h3>
<p class="scn-body">{E(sc["body"])}</p>
<dl class="scn-stats">{stats}</dl>
<p class="scn-go">{go}</p>
<p class="scn-cap">{E(sc.get("caption", "Illustrative scene."))}</p>
</div>
</div>
</article>'''


def _scenes(s, ctx):
    E, rel, RAW = ctx["E"], ctx["rel"], ctx["RAW"]
    hid = s.get("id", "scenes")
    items = s.get("scenes", [])
    rail = "".join(f'<li><a href="#scn-{i + 1}"><b>{i + 1:02d}</b><span>{E(sc["place"])}</span></a></li>' for i, sc in enumerate(items))
    body = "".join(_scene(i, sc, ctx) for i, sc in enumerate(items))
    return (MARK_A + f'<section class="pn-scenes" id="{E(hid)}" aria-labelledby="{E(hid)}-h">'
            f'<link rel="stylesheet" href="{E(rel("assets/scenes/scenes.css"))}">'
            f'<div class="scn-intro"><p class="scn-eyebrow">{E(s.get("eyebrow", ""))}</p><h2 id="{E(hid)}-h">{RAW(s["heading"])}</h2>'
            f'<p class="scn-lede">{E(s.get("lede", ""))}</p>'
            f'<nav class="scn-rail" aria-label="Scenes"><ol>{rail}</ol></nav></div>'
            f'{body}<script src="{E(rel("assets/scenes/scenes.js"))}" defer></script></section>' + MARK_B)


RENDER_SCENES = {"pn-scenes": _scenes}
