"""The chooser page for scripts/preview.py, in the shape Revolution's preview proved:
the three directions with their real specs, our pick with reasons tied to what the client
said, the alternatives, a side-by-side compare, every page, the plan, and a way to answer.
Kept in its own module so the markup can be edited without touching the page renderer."""
from __future__ import annotations

import html
import re

import reskin


def _e(s) -> str:
    s = "" if s is None else str(s)
    s = re.sub(r"\s*[—–]\s*", ", ", s)
    return html.escape(s, quote=True)


def _pname(pg: dict) -> str:
    return "Home" if pg["file"] == "index.html" else pg["title"].split("|")[0].strip()


def _slug(theme: str) -> str:
    return theme.replace("Quantum ", "").lower()


def _ground(bg: str) -> str:
    lum = reskin.relative_luminance(bg)
    if lum < 0.18:
        return "Dark"
    if lum < 0.93:
        return "Warm paper"
    return "White"


def hub(content, themes, recommend, base, roles, standard, client_tokens):
    b = content["brand"]
    pitch = content.get("pitch", {})
    ink = reskin.darken_until(b["accent"], "#f6f7f6")
    n = len(themes)

    specs = []
    for i, t in enumerate(themes, 1):
        css, tok = client_tokens(t, b)
        nat = reskin.parse_native(css)
        short = t.replace("Quantum ", "")
        face = (nat.get("--q-serif") or "").split(",")[0].strip("'\"")
        rec = '<span class="rec">our recommendation</span>' if t == recommend else ""
        specs.append(
            '<article class="dir"><div class="dir-h">'
            f'<span class="n">{i} / {n}</span><h2 class="h3">{_e(short)}{rec}</h2><p>{_e(roles.get(t, ""))}</p></div>'
            '<dl class="spec">'
            f'<div><dt>Measure</dt><dd>{_e(nat.get("--maxw", "1240px"))}</dd></div>'
            f'<div><dt>Headings</dt><dd>{_e(face)}</dd></div>'
            f'<div><dt>Ground</dt><dd>{_e(_ground(nat["--bg"]))}</dd></div>'
            f'<div><dt>Corner</dt><dd>{_e(nat.get("--radius", "8px"))}</dd></div></dl>'
            f'<a class="btn" href="{_slug(t)}/index.html" target="_blank" rel="noopener">Open {_e(short)}</a></article>')

    pick = recommend or themes[0]
    pick_short, pick_slug = pick.replace("Quantum ", ""), _slug(pick)
    reasons = "".join(f'<div class="why"><h3 class="h4">{_e(h)}</h3><p>{_e(t)}</p></div>' for h, t in pitch.get("pick_reasons", []))
    alts = "".join(
        f'<a class="alt" href="{_slug(t)}/index.html" target="_blank" rel="noopener"><h3 class="h4">{_e(t.replace("Quantum ", ""))}</h3>'
        f'<p>{_e(why)}</p><span>Open {_e(t.replace("Quantum ", ""))}</span></a>'
        for t, why in pitch.get("alternatives", []))
    heard = "".join(f"<li>{_e(x)}</li>" for x in pitch.get("heard", []))
    confirm = "".join(f"<li>{_e(x)}</li>" for x in pitch.get("confirm", []))
    heard_intro = pitch.get("heard_intro", "Tell us if any of this is wrong. It outranks our house defaults.")
    found = "".join(f"<li>{_e(x)}</li>" for x in pitch.get("found", []))
    plan = "".join(f'<div class="step"><div class="when">{_e(w)}</div><p>{_e(what)}</p></div>' for w, what in pitch.get("plan", []))
    pages = content["pages"]
    page_opts = "".join(f'<option value="{_e(pg["file"])}">{_e(_pname(pg))}</option>' for pg in pages)
    frames = "".join(
        f'<figure><figcaption>{_e(t.replace("Quantum ", ""))}</figcaption>'
        f'<iframe title="{_e(t.replace("Quantum ", ""))} preview" loading="lazy" src="{_slug(t)}/index.html" data-dir="{_slug(t)}"></iframe></figure>'
        for t in themes)
    every = ""
    for t in themes:
        every += f'<div class="col"><h3 class="h4">{_e(t.replace("Quantum ", ""))}</h3>' + "".join(
            f'<a href="{_slug(t)}/{pg["file"]}" target="_blank" rel="noopener">{_e(_pname(pg))}</a>' for pg in pages) + "</div>"
    qc = pitch.get("qbs_contact", {})
    std = ('<a class="alt" href="standard.html" target="_blank" rel="noopener"><h3 class="h4">The Quantum Website Standard</h3>'
           '<p>The ten things every site we build is guaranteed to have at launch, and the evidence you receive for each.</p><span>Open</span></a>') if standard else ""
    phone_href = re.sub(r"[^0-9+]", "", qc.get("phone", ""))

    css = f"""
:root{{--bg:#ffffff;--bg-alt:#f6f7f6;--fg:#1e2420;--muted:#546358;--border:#e2e6e3;--accent:{b["accent"]};--ink:{ink};--chrome:{b.get("chrome_bg", "#111")}}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#0e1412;--bg-alt:#141b18;--fg:#e6ebe7;--muted:#9cab9f;--border:#243328;--ink:{b["accent"]}}}}}
:root[data-theme="dark"]{{--bg:#0e1412;--bg-alt:#141b18;--fg:#e6ebe7;--muted:#9cab9f;--border:#243328;--ink:{b["accent"]}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 Inter,system-ui,sans-serif}}
a{{color:var(--ink)}}
.skip{{position:absolute;top:-200px;left:8px;background:var(--accent);color:#000;padding:10px 16px;border-radius:6px}}.skip:focus{{top:8px}}
.top{{background:var(--chrome);position:sticky;top:0;z-index:20}}.top .wrap{{display:flex;align-items:center;justify-content:space-between;gap:14px;min-height:64px}}.top img{{height:36px}}
.top nav{{display:flex;gap:4px;flex-wrap:wrap}}.top nav a{{color:rgba(255,255,255,.82);text-decoration:none;font-size:13.5px;padding:10px 10px;border-radius:8px;min-height:44px;display:inline-flex;align-items:center}}.top nav a:hover{{color:#fff;background:rgba(255,255,255,.08)}}
.wrap{{max-width:1040px;margin:0 auto;padding:0 24px}}
section{{padding:64px 0;border-bottom:1px solid var(--border)}}
.eyebrow{{font-size:13px;letter-spacing:.16em;text-transform:uppercase;color:var(--ink);font-weight:600;margin:0 0 14px}}
h1{{font-size:clamp(32px,5vw,52px);line-height:1.04;letter-spacing:-.02em;margin:0 0 16px;text-wrap:balance;max-width:20ch}}
h2{{font-size:clamp(24px,3vw,34px);line-height:1.1;letter-spacing:-.02em;margin:0 0 12px;text-wrap:balance}}
h3,.h3{{font-size:22px;margin:0 0 6px;letter-spacing:-.01em}}h4,.h4{{font-size:16px;margin:0 0 6px}}.dir h2.h3{{font-size:22px;line-height:1.2}}
.confirm li{{margin:10px 0}}
.lead{{color:var(--muted);max-width:62ch;margin:0 0 28px;font-size:17px}}
.dirs{{display:grid;grid-template-columns:repeat({n},1fr);gap:18px}}
.dir{{border:1px solid var(--border);border-radius:14px;padding:24px;background:var(--bg-alt);display:flex;flex-direction:column;gap:18px}}
.dir .n{{font-size:13px;color:var(--muted);letter-spacing:.08em}}.dir p{{margin:6px 0 0;color:var(--muted);font-size:14.5px}}
.rec{{display:inline-block;margin-left:8px;font-size:12.5px;font-weight:600;letter-spacing:.04em;color:var(--ink);border:1px solid var(--accent);border-radius:999px;padding:2px 10px;vertical-align:middle}}
.spec{{display:grid;grid-template-columns:1fr 1fr;gap:10px 16px;margin:0}}.spec dt{{font-size:13px;color:var(--muted);letter-spacing:.06em;text-transform:uppercase}}.spec dd{{margin:2px 0 0;font-weight:600;font-size:14.5px}}
.btn{{display:inline-flex;align-items:center;justify-content:center;min-height:44px;padding:10px 18px;background:var(--accent);color:#000545;border-radius:8px;text-decoration:none;font-weight:600;margin-top:auto}}
.btn:hover{{filter:brightness(.95)}}
.pick{{display:grid;grid-template-columns:1.1fr .9fr;gap:40px;align-items:start}}
.why{{padding:16px 0;border-top:1px solid var(--border)}}.why:last-of-type{{border-bottom:1px solid var(--border)}}.why p{{margin:4px 0 0;color:var(--muted);font-size:15px}}
.change{{background:var(--bg-alt);border:1px solid var(--border);border-radius:12px;padding:20px 22px;margin-top:22px;font-size:15px}}
.alts{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}.alt{{display:block;border:1px solid var(--border);border-radius:12px;padding:20px 22px;text-decoration:none;color:inherit;background:var(--bg-alt)}}.alt:hover{{border-color:var(--accent)}}.alt p{{color:var(--muted);font-size:14.5px;margin:0 0 10px}}.alt span{{font-weight:600;color:var(--ink);font-size:14px}}
.cmp-bar{{display:flex;gap:14px;align-items:center;margin:0 0 18px;flex-wrap:wrap}}select{{font:inherit;font-size:16px;padding:10px 12px;border:1px solid var(--border);border-radius:8px;background:var(--bg);color:var(--fg);min-height:44px}}
.frames{{display:grid;grid-template-columns:repeat({n},1fr);gap:14px}}.frames figure{{margin:0}}.frames figcaption{{font-size:13px;color:var(--muted);margin:0 0 8px;font-weight:600}}
.frames iframe{{width:100%;aspect-ratio:9/16;border:1px solid var(--border);border-radius:12px;background:#fff}}
.every{{display:grid;grid-template-columns:repeat({n},1fr);gap:24px}}.every .col a{{display:flex;align-items:center;min-height:44px;text-decoration:none;color:var(--fg);border-top:1px solid var(--border);font-size:15px}}.every .col a:hover{{color:var(--ink)}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:40px}}ul{{margin:0;padding-left:18px}}li{{margin:8px 0;color:var(--fg)}}li::marker{{color:var(--accent)}}
.plan{{display:grid;grid-template-columns:repeat(5,1fr);gap:14px}}.step{{border-top:2px solid var(--accent);padding-top:12px}}.when{{font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:var(--ink);font-weight:700}}.step p{{margin:8px 0 0;font-size:14.5px;color:var(--muted)}}
.turn{{background:var(--bg-alt);border:1px solid var(--border);border-radius:14px;padding:28px}}.turn a.btn{{margin:0 12px 12px 0}}
footer{{padding:36px 0 80px;color:var(--muted);font-size:13.5px;max-width:66ch}}
@media(max-width:900px){{.dirs,.frames,.every,.plan{{grid-template-columns:1fr}}.pick,.alts,.two{{grid-template-columns:1fr}}.frames iframe{{aspect-ratio:3/4}}}}
"""
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{_e(content["client"])}, three website directions</title>
<meta name="description" content="Three complete website directions for {_e(content["client"])}, prepared by Quantum Business Solutions.">
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="{_e(base)}/">
<meta property="og:title" content="{_e(content["client"])}, three website directions">
<meta property="og:image" content="{_e(base)}/assets/hero-og.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap">
<style>{css}</style></head><body>
<a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="wrap"><img src="{_e(b["logo"])}" alt="{_e(content["client"])}" height="36" width="99"><nav aria-label="Sections"><a href="#three">The three</a><a href="#pick">Our pick</a><a href="#compare">Compare</a><a href="#heard">Fixed</a><a href="#confirm">To confirm</a><a href="#every">Every page</a><a href="#plan">The plan</a><a href="#turn">Your turn</a></nav></div></header>
<main id="main">
<section><div class="wrap"><p class="eyebrow">Quantum Business Solutions for {_e(content["client"])}</p><h1>Same site. Three ways to design it.</h1>
<p class="lead">Each one is the whole site, not a home page and two mockups: every page is built and live in all three. The words and the structure are identical across them on purpose, so the decision in front of you is about direction, not copy. Open any one, then use the switcher pinned to the bottom of the page to flip between all three without losing your place.</p></div></section>
<section id="three"><div class="wrap"><p class="eyebrow">The three</p><div class="dirs">{"".join(specs)}</div></div></section>
<section id="pick"><div class="wrap"><p class="eyebrow">Our recommendation</p><div class="pick"><div><h2>We would build {_e(pick_short)}</h2><p class="lead">{_e(roles.get(pick, ""))}</p>{reasons}<div class="change"><strong>The one thing we would change:</strong> {_e(pitch.get("pick_change", ""))}</div><p style="margin-top:22px"><a class="btn" href="{pick_slug}/index.html" target="_blank" rel="noopener">Open {_e(pick_short)}</a></p></div>
<div><h3 class="h3" style="font-size:18px;margin-bottom:14px">If you would rather not</h3><div class="alts" style="grid-template-columns:1fr">{alts}</div></div></div></div></section>
<section id="compare"><div class="wrap"><p class="eyebrow">Side by side</p><h2>The same page, all three at once</h2><div class="cmp-bar"><label for="cmp">Pick a page</label><select id="cmp">{page_opts}</select></div><div class="frames">{frames}</div></div></section>
<section id="heard"><div class="wrap"><div class="two"><div><p class="eyebrow">What we are treating as fixed</p><h2>What your site and brand profile already say</h2><p class="lead" style="margin-bottom:12px">{_e(heard_intro)}</p><ul>{heard}</ul></div><div><p class="eyebrow">What we found</p><h2>And what we would do about it</h2><ul>{found}</ul></div></div></div></section>
<section id="confirm"><div class="wrap"><p class="eyebrow">To confirm with you</p><h2>Ten things we wrote as a draft, not a fact</h2><p class="lead">Each of these appears on the pages. None is built until you confirm or correct it.</p><ul class="confirm">{confirm}</ul></div></section>
<section id="every"><div class="wrap"><p class="eyebrow">Every page</p><h2>Built and live in all three</h2><div class="every">{every}</div></div></section>
<section id="plan"><div class="wrap"><p class="eyebrow">The plan</p><h2>From a choice to a live site</h2><div class="plan">{plan}</div>{('<div class="alts" style="margin-top:28px;grid-template-columns:1fr 1fr">' + std + '</div>') if std else ""}</div></section>
<section id="turn"><div class="wrap"><div class="turn"><p class="eyebrow">Your turn</p><h2>Tell us which one, and what you would change</h2><p class="lead" style="margin-bottom:18px">Reply with the direction and anything on any page you would change. Nothing is locked until you say so.</p><a class="btn" href="mailto:{_e(qc.get("email", ""))}?subject={_e(content["client"])}%20website%20direction">Email {_e(qc.get("name", "us"))}</a><a class="btn" style="background:transparent;border:1px solid var(--accent);color:var(--ink)" href="tel:{_e(phone_href)}">Call {_e(qc.get("phone", ""))}</a></div></div></section>
</main>
<footer class="wrap">{_e(pitch.get("footer", "Prepared for " + pitch.get("prepared_for", content["client"]) + ". Nothing here is live or indexed."))}</footer>
<script>
document.getElementById('cmp').addEventListener('change', function (e) {{
  document.querySelectorAll('.frames iframe').forEach(function (f) {{ f.src = f.dataset.dir + '/' + e.target.value; }});
}});
</script>
</body></html>
"""
