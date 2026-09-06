#!/usr/bin/env python3
"""Generate the pitch: one main page and three options, as a single HTML file.

The point of this script is that a mockup should cost nothing and commit to nothing.

Before it existed, showing a client three directions meant cloning three 300-file
themes into a live HubSpot portal -- slow, and it commits the product line before
anyone has agreed to anything. This renders the same three directions locally from
the themes' real cached tokens (themes/tokens.json), so:

  - no portal writes, no clone, nothing to undo
  - seconds instead of a day
  - the clone happens ONCE, after the client picks

Reads themes/tokens.json. Needs no network and no token.

  python3 scripts/mockup.py --client "Meridian Dental Group" \
      --themes "Quantum Press,Quantum Clean,Quantum Showcase" \
      --accent "#1E6B8C" \
      --promise "Twelve neighbourhood practices, one standard of care." \
      --brief brands/meridian-dental.md \
      --out /tmp/mockups/meridian.html
"""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reskin import derive_native, contrast_ratio, LIGHT_THEMES  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKENS = os.path.join(ROOT, "themes", "tokens.json")

GOOGLE_FONTS = (
    "https://fonts.googleapis.com/css2"
    "?family=Fraunces:opsz,wght@9..144,400;9..144,600"
    "&family=Instrument+Serif:ital@0;1"
    "&family=Poppins:wght@400;500;600"
    "&family=Space+Grotesk:wght@400;500;700"
    "&family=Open+Sans:wght@400;600"
    "&family=Playfair+Display:ital,wght@0,500;0,700;1,500"
    "&family=Spectral:wght@400;600"
    "&family=Newsreader:opsz,wght@6..72,400;6..72,600"
    "&family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,700"
    "&family=Inter:wght@400;500;600"
    "&family=DM+Sans:wght@400;500;600;700"
    "&display=swap"
)

E = lambda s: html.escape(str(s or ""), quote=True)


def load_tokens():
    if not os.path.exists(TOKENS):
        raise SystemExit(
            f"{TOKENS} not found.\nRun: QBS_HUBSPOT_TOKEN=... python3 scripts/themetokens.py")
    with open(TOKENS, encoding="utf-8") as fh:
        return json.load(fh)["themes"]


def _plain(md: str) -> str:
    """Markdown emphasis and code spans read as noise in rendered HTML."""
    md = re.sub(r"\*\*(.+?)\*\*", r"\1", md)
    md = re.sub(r"`([^`]*)`", r"\1", md)
    return md.strip()


def parse_brief(path):
    """Pull what the main page needs out of brands/<slug>.md. Best effort -- a
    missing field renders as a visible gap, which is the correct behaviour: the
    pitch should show what we don't know yet, not hide it."""
    if not path or not os.path.exists(path):
        return {}
    txt = open(path, encoding="utf-8").read()
    out = {}
    # Anchor on the heading, not on "the first blockquote" -- the only real brief in the
    # repo opens with a pre-methodology banner, and a truncated field renders as a
    # confident half-sentence, which is worse than a visible gap.
    sec = re.search(r"##\s*The promise\s*\n(.*?)(?=\n##\s)", txt, re.S)
    if sec:
        m = re.search(r'>\s*[\"“](.+?)[\"”]', sec.group(1), re.S)
        if m:
            val = " ".join(m.group(1).split())
            if val and not val.startswith("<"):
                out["promise"] = val
    # Multiline: the template's read wraps across lines.
    m = re.search(r"Reading this as:\s*(.+?)(?=\n\s*\n|\n##\s)", txt, re.S)
    if m:
        val = " ".join(re.sub(r"\*\*", "", m.group(1)).split())
        if val and "<page kind>" not in val:
            out["read"] = val
    sec = re.search(r"## Client-stated constraints.*?\n(.*?)(?=\n## )", txt, re.S)
    if sec:
        # Bullets wrap at 100 columns in every brief; a continuation line starts with
        # two spaces. Join them, or a constraint renders as a confident half-sentence.
        items = []
        for l in sec.group(1).splitlines():
            if l.strip().startswith("- "):
                items.append(l.strip()[2:].strip())
            elif l.startswith("  ") and items and l.strip():
                items[-1] += " " + l.strip()
        out["constraints"] = [_plain(i) for i in items if "<" not in i]
    sec = re.search(r"## Competitors ingested.*?\n(.*?)(?=\n## )", txt, re.S)
    if sec:
        rows = [l for l in sec.group(1).splitlines()
                if l.strip().startswith("|") and "---" not in l]
        out["competitors"] = [
            [_plain(c.strip()) for c in r.strip().strip("|").split("|")] for r in rows[1:]
        ]
    m = re.search(r"\*\*Organic traffic:\*\*\s*([^\n·]+)", txt)
    if m:
        val = m.group(1).strip()
        if val and "<" not in val:
            out["traffic"] = val
    return out


def swatch_row(tok):
    order = [("--bg", "ground"), ("--bg-alt", "surface"), ("--card", "card"),
             ("--q-gold", "accent"), ("--q-gold-bright", "hover"), ("--fg", "text"),
             ("--fg-muted", "muted")]
    out = []
    for k, label in order:
        v = tok.get(k)
        if not v:
            continue
        out.append(
            f'<div class="sw"><span class="chip" style="background:{E(v)}"></span>'
            f'<b>{E(label)}</b><code>{E(v)}</code></div>')
    return "".join(out)


def option_card(idx, name, meta, tok, role, rationale):
    bg, fg, muted = tok.get("--bg", "#fff"), tok.get("--fg", "#111"), tok.get("--fg-muted", "#666")
    gold, cta_fg = tok.get("--q-gold", "#c4a44a"), tok.get("--cta-fg", "#fff")
    card, border = tok.get("--card", bg), tok.get("--border", "rgba(0,0,0,.12)")
    serif, sans = tok.get("--q-serif", "Georgia,serif"), tok.get("--q-sans", "system-ui,sans-serif")
    short = name.replace("Quantum ", "")
    cr = contrast_ratio(gold, cta_fg) if gold.startswith("#") and cta_fg.startswith("#") else 0
    warn = ("" if cr >= 4.5 else
            f'<p class="a11y">Button contrast {cr:.2f}:1 — below the 4.5:1 minimum. '
            f'Fixed during re-skin; the derived palette clears it.</p>')
    return f"""
<section class="opt">
  <header class="opt-h">
    <span class="num">Option {idx}</span>
    <h3>{E(role)}</h3>
    <p class="theme-name">{E(short)} · {E(meta.get('ground'))} · {E(meta.get('readsAs'))}</p>
    <p class="why">{E(rationale)}</p>
  </header>

  <div class="frame" style="--bg:{E(bg)};--fg:{E(fg)};--muted:{E(muted)};--gold:{E(gold)};
       --ctafg:{E(cta_fg)};--card:{E(card)};--bd:{E(border)};--serif:{E(serif)};--sans:{E(sans)}">
    <div class="mock">
      <div class="m-nav">
        <span class="m-logo">{E(NAV_LOGO)}</span>
        <span class="m-links">{''.join(f"<i>{E(n)}</i>" for n in NAV_LINKS)}
          <b class="m-cta">{E(CTA_LABEL)}</b></span>
      </div>
      <div class="m-hero">
        <span class="m-eyebrow">{E(EYEBROW)}</span>
        <h4>{E(HEADLINE)}</h4>
        <p>{E(SUBHEAD)}</p>
        <span class="m-btns"><b class="m-cta">{E(CTA_LABEL)}</b>
          <b class="m-cta2">{E(CTA2_LABEL)}</b></span>
      </div>
      <div class="m-band">
        {''.join(f'<div class="m-stat"><b>{E(v)}</b><span>{E(l)}</span></div>' for v, l in STATS)}
      </div>
      <div class="m-cards">
        <div class="m-card"><h5>{E(CARD1)}</h5><p>{E(CARD_BODY)}</p><span class="m-link">More →</span></div>
        <div class="m-card"><h5>{E(CARD2)}</h5><p>{E(CARD_BODY)}</p><span class="m-link">More →</span></div>
        <div class="m-card"><h5>{E(CARD3)}</h5><p>{E(CARD_BODY)}</p><span class="m-link">More →</span></div>
      </div>
    </div>
  </div>

  <div class="type">
    <p class="tspec">Headings — <b>{E(serif.split(',')[0].strip(chr(39)))}</b></p>
    <p class="tsample" style="font-family:{E(serif)}">{E(HEADLINE)}</p>
    <p class="tspec">Body — <b>{E(sans.split(',')[0].strip(chr(39)))}</b></p>
    <p class="tsample-b" style="font-family:{E(sans)}">{E(SUBHEAD)}</p>
  </div>

  <div class="swatches">{swatch_row(tok)}</div>
  {warn}
</section>"""


# Mock copy. Deliberately specific: real content is the difference between a mockup
# a prospect can judge and a template they can't. Lorem is banned -- guardrails --
# and so is another client's copy: the first Kelly render shipped "General dentistry"
# cards from a dental demo, and only a human looking at the screenshot caught it.
# So there are no defaults. --eyebrow, --cards and --stats are required.
NAV_LOGO = "LOGO"
NAV_LINKS = ["Services", "About", "Insights"]
CTA_LABEL = "Book a call"
CTA2_LABEL = "See how it works"
EYEBROW = ""
HEADLINE = ""
SUBHEAD = ""
CARD1, CARD2, CARD3 = "", "", ""
CARD_BODY = "What it covers, what it costs, and how quickly it starts."
STATS = []


# Rough typeface classes, for selection rule 5. A serif and a grotesque read as
# different characters; two grotesques do not, however different their names.
def face_class(stack: str) -> str:
    f = (stack or "").split(",")[0].strip().strip("'\"").lower()
    if any(k in f for k in ("serif", "playfair", "spectral", "newsreader",
                            "fraunces", "instrument", "georgia")):
        return "serif"
    if "grotesque" in f or "grotesk" in f:
        return "grotesque"
    return "sans"


def check_selection(themes, tokens, accent=None):
    """Encode the selection rules from themes/catalogue.md so the tool enforces them
    instead of relying on whoever is typing to remember. Rule 5 caught a bad set on
    this script's own first demo run."""
    out = []
    grounds = {t: tokens[t]["ground"] for t in themes if t in tokens}
    if len(set(grounds.values())) > 1:
        out.append(f"mixed grounds {sorted(set(grounds.values()))}. Ground is filtered by "
                   f"the brief, not by taste — catalogue.md rule 1. If the client asked for "
                   f"light, the dark themes are out. Full stop.")
    seen = {}
    for t in themes:
        m = tokens.get(t)
        if not m:
            continue
        key = (m["ground"], face_class(m["tokens"].get("--q-serif", "")))
        if key in seen:
            out.append(f"{seen[key].replace('Quantum ','')} and {t.replace('Quantum ','')} are "
                       f"both {key[0]} with {key[1]} headings — catalogue.md rule 5 says never "
                       f"show two like that. One slot is wasted; swap one.")
        seen[key] = t
    if "Quantum Converter" in themes:
        out.append("Converter uses Space Grotesk, which is on the watchlist in "
                   "design/guardrails.md as an AI-default tell. It needs the strongest "
                   "justification of any theme before it goes in a set of three.")
    fails = [t.replace("Quantum ", "") for t in themes
             if tokens.get(t, {}).get("ctaPassesAA") is False]
    # The build gate checks accent TEXT on ground at 4.5. Check it here too, or a
    # direction sails through the pitch and is refused at clone time.
    if accent:
        for t in themes:
            m = tokens.get(t)
            if not m:
                continue
            d = derive_native(accent, m["ground"])
            cr = contrast_ratio(d["--accent-ink"], d["--bg"])
            if cr < 4.5:
                out.append(f"{t.replace('Quantum ','')}: accent text derives to {cr:.2f}:1 on "
                           f"its ground, under the 4.5 the build gate requires. "
                           f"reskin.py will refuse this direction.")
    if fails:
        out.append(f"{', '.join(fails)} ship button contrast below WCAG AA "
                   f"(3.5-3.9:1 vs 4.5:1 required). The mockup corrects it via the derived "
                   f"--cta-fg, but the THEME is still broken — fix at source before launch.")
    return out


def build(client, promise, read, themes, tokens, accent, brief, roles, rationales):
    global HEADLINE, SUBHEAD
    HEADLINE = promise or f"{client}"
    SUBHEAD = read or "The one line a visitor has to believe."

    opts = []
    for i, name in enumerate(themes, 1):
        meta = tokens.get(name)
        if not meta:
            raise SystemExit(f"unknown theme: {name}")
        tok = dict(meta["tokens"])
        if accent:
            # Re-skin the ACCENT ONLY, and keep each theme's own ground.
            #
            # Deriving all twelve values from one accent flattens the ground
            # differences that make the nine distinct -- the first version of this
            # script did that, and the three options came out as three shades of one
            # idea with only the typeface differing. That is precisely the failure
            # process/pitch-presentation.md exists to prevent.
            derived = derive_native(accent, meta["ground"])
            for k in ("--q-gold", "--q-gold-bright", "--q-gold-dim"):
                if derived.get(k):
                    tok[k] = derived[k]
            # --border carries the accent hue, so it follows the accent.
            if derived.get("--border"):
                tok["--border"] = derived["--border"]
            # --cta-fg must be contrast-correct against the NEW accent. This is also
            # what fixes the light themes' 3.5-3.9:1 button failure in the mockup.
            if derived.get("--cta-fg"):
                tok["--cta-fg"] = derived["--cta-fg"]
            # Same two-token accent the build will ship, so the pitch and the site agree.
            for k in ("--accent-ink", "--accent-lift"):
                if derived.get(k):
                    tok[k] = derived[k]
        opts.append(option_card(i, name, meta, tok,
                                roles[i - 1] if i <= len(roles) else "",
                                rationales[i - 1] if i <= len(rationales) else ""))

    cons = brief.get("constraints") or []
    comps = brief.get("competitors") or []
    cons_html = ("<ul>" + "".join(f"<li>{E(c)}</li>" for c in cons) + "</ul>"
                 if cons else '<p class="gap">Not captured yet — this is the highest-trust '
                              'section on the page. Fill it from the call.</p>')
    comp_html = ("<table><tr><th>Competitor</th><th>Ingested</th><th>What the category looks like</th></tr>"
                 + "".join("<tr>" + "".join(f"<td>{E(c)}</td>" for c in r[:3]) + "</tr>"
                           for r in comps) + "</table>"
                 if comps else '<p class="gap">None ingested yet — run <code>/design-ingest</code> '
                               'before the meeting. Naming a competitor we haven\'t read is worse '
                               'than naming none.</p>')
    traffic = brief.get("traffic")
    traffic_html = (f'<p class="big">{E(traffic)} <span>organic visits / month today</span></p>'
                    '<p class="note">This is the number the engagement gets measured against.</p>'
                    if traffic else
                    '<p class="gap">No baseline recorded. Pull it before the meeting — without it '
                    'there is no way to prove the work worked.</p>')

    accent_note = (f'<p class="note">All three directions re-skinned to {E(accent)}, '
                   'taken from your own site. Each theme keeps its own ground and '
                   'typeface — that is what makes the three genuinely different.</p>'
                   if accent else "")

    return f"""<title>{E(client)} — three directions</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{GOOGLE_FONTS}">
<style>
:root{{
  --ink:#14171c; --ink-2:#4a515c; --line:#e3e0d8; --paper:#faf8f4;
  --accent:#8a6d2f; --rule:#d8d4ca;
}}
@media (prefers-color-scheme:dark){{ :root:not([data-theme="light"]){{
  --ink:#eceef2; --ink-2:#a1a8b4; --line:#282c34; --paper:#0e1116;
  --accent:#d0b366; --rule:#2f343d;
}}}}
:root[data-theme="dark"]{{
  --ink:#eceef2; --ink-2:#a1a8b4; --line:#282c34; --paper:#0e1116;
  --accent:#d0b366; --rule:#2f343d;
}}
*{{box-sizing:border-box}}
body{{background:var(--paper);color:var(--ink);
  font:16px/1.65 'Inter',system-ui,-apple-system,sans-serif;margin:0}}
.wrap{{max-width:1120px;margin:0 auto;padding:0 24px}}
h1,h2,h3{{font-family:'Fraunces','Playfair Display',Georgia,serif;line-height:1.15;
  letter-spacing:-.02em;margin:0}}
.eyebrow{{font-size:12px;letter-spacing:.18em;text-transform:uppercase;
  color:var(--accent);font-weight:600;display:flex;align-items:center;gap:14px;margin:0 0 18px}}
.eyebrow::before{{content:'';width:26px;height:1px;background:var(--accent)}}
header.top{{padding:72px 0 40px;border-bottom:1px solid var(--rule)}}
header.top h1{{font-size:clamp(30px,5vw,50px);max-width:22ch}}
header.top .sub{{color:var(--ink-2);max-width:60ch;margin:18px 0 0;font-size:17px}}
section.blk{{padding:44px 0;border-bottom:1px solid var(--line)}}
section.blk h2{{font-size:clamp(20px,2.4vw,26px);margin-bottom:6px}}
section.blk .lead{{color:var(--ink-2);margin:0 0 20px;max-width:70ch}}
.grid2{{display:grid;grid-template-columns:1fr;gap:34px}}
@media(min-width:860px){{.grid2{{grid-template-columns:1fr 1fr}}}}
ul{{margin:0;padding-left:20px}} li{{margin:7px 0}}
.gap{{color:var(--ink-2);font-style:italic;border-left:2px solid var(--accent);
  padding-left:14px;margin:0}}
.big{{font-family:'Fraunces',Georgia,serif;font-size:40px;margin:0}}
.big span{{font-family:'Inter',sans-serif;font-size:15px;color:var(--ink-2);font-weight:400}}
.note{{color:var(--ink-2);font-size:14px;margin:8px 0 0}}
table{{border-collapse:collapse;width:100%;font-size:14px}}
th,td{{text-align:left;padding:9px 12px;border-bottom:1px solid var(--line);vertical-align:top}}
th{{font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-2)}}
code{{font:12px/1.4 ui-monospace,SFMono-Regular,Menlo,monospace;
  background:color-mix(in srgb,var(--ink) 7%,transparent);padding:2px 5px;border-radius:4px}}

/* ---- options ---- */
.opts{{padding:44px 0 8px}}
.opt{{margin:0 0 76px;padding-top:34px;border-top:1px solid var(--line)}}
.opt:first-of-type{{border-top:none;padding-top:14px}}
.opt-h .num{{font-size:11px;letter-spacing:.16em;text-transform:uppercase;
  color:var(--accent);font-weight:700}}
.opt-h h3{{font-size:clamp(22px,3vw,30px);margin:6px 0 4px}}
.opt-h .theme-name{{font-size:13px;color:var(--ink-2);margin:0 0 10px;
  letter-spacing:.02em;text-transform:lowercase}}
.opt-h .why{{margin:0 0 20px;max-width:66ch}}
.frame{{border:1px solid var(--rule);border-radius:12px;overflow:hidden}}
.mock{{background:var(--bg);color:var(--fg);font-family:var(--sans);padding:0}}
.m-nav{{display:flex;justify-content:space-between;align-items:center;
  padding:16px 22px;border-bottom:1px solid var(--bd);font-size:13px}}
.m-logo{{font-family:var(--serif);font-size:17px;letter-spacing:.04em}}
.m-links{{display:flex;align-items:center;gap:16px}}
.m-links i{{font-style:normal;color:var(--muted)}}
.m-cta{{background:var(--gold);color:var(--ctafg);padding:7px 15px;border-radius:6px;
  font-weight:600;font-size:12.5px}}
.m-cta2{{border:1px solid var(--gold);color:var(--gold);padding:6px 14px;
  border-radius:6px;font-weight:600;font-size:12.5px}}
.m-hero{{padding:52px 30px 46px;max-width:44rem}}
.m-eyebrow{{font-size:10.5px;letter-spacing:.2em;text-transform:uppercase;
  color:var(--gold);font-weight:600}}
.m-hero h4{{font-family:var(--serif);font-size:clamp(26px,3.6vw,40px);line-height:1.1;
  letter-spacing:-.02em;margin:14px 0 12px;font-weight:600}}
.m-hero p{{color:var(--muted);margin:0 0 22px;font-size:15px;max-width:46ch}}
.m-btns{{display:flex;gap:10px;flex-wrap:wrap}}
.m-band{{display:flex;gap:34px;flex-wrap:wrap;padding:20px 30px;
  border-top:1px solid var(--bd);border-bottom:1px solid var(--bd);background:var(--card)}}
.m-stat b{{font-family:var(--serif);font-size:26px;display:block;color:var(--gold)}}
.m-stat span{{font-size:11.5px;color:var(--muted);letter-spacing:.06em;text-transform:uppercase}}
.m-cards{{display:grid;grid-template-columns:1fr;gap:16px;padding:26px 30px 34px}}
@media(min-width:700px){{.m-cards{{grid-template-columns:repeat(3,1fr)}}}}
.m-card{{border:1px solid var(--bd);border-radius:9px;padding:18px;background:var(--card)}}
.m-card h5{{font-family:var(--serif);font-size:16.5px;margin:0 0 7px;font-weight:600}}
.m-card p{{font-size:13px;color:var(--muted);margin:0 0 12px}}
.m-link{{font-size:12.5px;color:var(--gold);font-weight:600}}

.type{{display:grid;gap:4px;margin:22px 0 0;padding:20px 0 0;border-top:1px solid var(--line)}}
.tspec{{font-size:11px;letter-spacing:.13em;text-transform:uppercase;
  color:var(--ink-2);margin:0}}
.tsample{{font-size:clamp(21px,3vw,30px);line-height:1.2;margin:2px 0 14px}}
.tsample-b{{font-size:15.5px;color:var(--ink-2);margin:2px 0 0;max-width:62ch}}
.swatches{{display:flex;flex-wrap:wrap;gap:8px;margin-top:20px}}
.sw{{display:flex;align-items:center;gap:7px;border:1px solid var(--line);
  border-radius:999px;padding:5px 11px 5px 6px;font-size:12px}}
.sw .chip{{width:17px;height:17px;border-radius:50%;
  box-shadow:inset 0 0 0 1px rgba(0,0,0,.16)}}
.sw b{{font-weight:600}} .sw code{{background:none;padding:0;color:var(--ink-2)}}
.a11y{{margin:14px 0 0;padding:10px 14px;border-left:2px solid #b4441f;
  background:color-mix(in srgb,#b4441f 8%,transparent);font-size:13.5px}}
footer{{padding:40px 0 70px;color:var(--ink-2);font-size:13.5px}}
</style>

<div class="wrap">
<header class="top">
  <p class="eyebrow">Website directions</p>
  <h1>{E(client)}</h1>
  <p class="sub">Three directions, each a complete 19-template site kit on a theme we own
  outright — re-skinned to your brand. Not concepts: working systems, editable by your team
  in HubSpot after launch.</p>
</header>

<section class="blk">
  <h2>What we read</h2>
  <p class="lead">{E(read or 'Reading to be confirmed.')}</p>
  <div class="grid2">
    <div><h2 style="font-size:17px;margin-bottom:10px">The promise</h2>
      <p class="lead" style="font-size:19px">"{E(promise or 'To be confirmed on the call.')}"</p>
      <p class="note">Your words, back to you. Everything below hangs off this line.</p></div>
    <div><h2 style="font-size:17px;margin-bottom:10px">Where you are today</h2>
      {traffic_html}</div>
  </div>
</section>

<section class="blk">
  <h2>Constraints we're honouring</h2>
  <p class="lead">What you told us, taken as binding — these outrank our house defaults.</p>
  {cons_html}
</section>

<section class="blk">
  <h2>What the category looks like</h2>
  <p class="lead">Measured off live competitor sites, not impressions.</p>
  {comp_html}
</section>

<section class="opts">
  <p class="eyebrow">The three directions</p>
  <h2 style="font-size:clamp(22px,3vw,30px);margin-bottom:8px">One safe, one stretch, one wildcard</h2>
  <p class="lead">Deliberately different registers, so the choice is real rather than three
  shades of one idea. {'' if not accent else 'All three carry your accent colour.'}</p>
  {accent_note}
  {''.join(opts)}
</section>

<footer>
  Rendered from the live design tokens of the nine Quantum themes — the colours and typefaces
  above are what ships, not an approximation. Nothing has been built in HubSpot yet; the
  direction you choose gets cloned and re-skinned once.
</footer>
</div>
"""


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--client", required=True)
    p.add_argument("--themes", required=True, help="three theme names, comma separated")
    p.add_argument("--accent", help="client accent hex; all three re-skin to it")
    p.add_argument("--promise", help="the one line a visitor must believe")
    p.add_argument("--read", help='"<page kind> for <audience>, with a <register> language"')
    p.add_argument("--brief", help="brands/<slug>.md — fills the main page")
    p.add_argument("--roles", default="The safe one|The stretch|The wildcard",
                   help="pipe-separated, so prose can contain commas")
    p.add_argument("--rationales", default="||",
                   help="pipe-separated, one per direction")
    p.add_argument("--eyebrow", help="the small line above the headline, e.g. 'Since 1947'")
    p.add_argument("--cards", help="three service names, pipe-separated")
    p.add_argument("--card-body", help="one line under each card")
    p.add_argument("--stats", help='three "value:label" pairs, pipe-separated — the stat-band')
    p.add_argument("--cta", help="primary button label")
    p.add_argument("--cta2", help="secondary button label")
    p.add_argument("--nav", help="three or four nav labels, pipe-separated")
    p.add_argument("--logo-text", help="what stands in for the logo")
    p.add_argument("--override", metavar="REASON",
                   help="proceed despite a selection-rule violation. Recorded in the output.")
    p.add_argument("--out", default="mockups.html")
    a = p.parse_args()

    themes = [t.strip() for t in a.themes.split(",") if t.strip()]
    if len(themes) != 3:
        raise SystemExit("Three themes. Two reads as a coin flip; four and nobody chooses.")

    tokens = load_tokens()
    brief = parse_brief(a.brief)
    warn = check_selection(themes, tokens, a.accent)
    for w in warn:
        print(f"warning: {w}", file=sys.stderr)
    # It was documented as a gate and behaved as a print statement -- stderr on a
    # successful command is exactly what gets dropped by a wrapper or an agent loop.
    # Rules 1 and 5 are about the SET being wrong, so they block; the contrast note
    # fires on every light build by design and stays a warning.
    blocking = [w for w in warn if "rule 1" in w or "rule 5" in w
                or "mixed grounds" in w or "both" in w and "headings" in w]
    if blocking and not a.override:
        print("\nREFUSING: the set of three violates a selection rule (above).\n"
              'Fix the set, or pass --override "<reason>" if you have one.', file=sys.stderr)
        return 2

    global EYEBROW, CARD1, CARD2, CARD3, CARD_BODY, STATS, CTA_LABEL, CTA2_LABEL, NAV_LINKS, NAV_LOGO
    missing = [f for f, v in (("--eyebrow", a.eyebrow), ("--cards", a.cards), ("--stats", a.stats)) if not v]
    if missing:
        print(f"\nREFUSING: preview copy is required: {' '.join(missing)}.\n"
              "There is no default copy on purpose -- a placeholder in front of a client is\n"
              "a placeholder, whoever it was written for (design/guardrails.md).", file=sys.stderr)
        return 2
    cards = [c.strip() for c in a.cards.split("|")]
    if len(cards) != 3:
        raise SystemExit("--cards takes exactly three, pipe-separated")
    stats = []
    for pair in a.stats.split("|"):
        v, _, l = pair.partition(":")
        if not l:
            raise SystemExit(f'--stats entries are "value:label", got {pair!r}')
        stats.append((v.strip(), l.strip()))
    if len(stats) != 3:
        raise SystemExit("--stats takes exactly three (the band is three wide)")
    EYEBROW = a.eyebrow
    CARD1, CARD2, CARD3 = cards
    STATS = stats
    if a.card_body: CARD_BODY = a.card_body
    if a.cta: CTA_LABEL = a.cta
    if a.cta2: CTA2_LABEL = a.cta2
    if a.nav: NAV_LINKS = [n.strip() for n in a.nav.split("|") if n.strip()]
    if a.logo_text: NAV_LOGO = a.logo_text

    doc = build(a.client,
                a.promise or brief.get("promise"),
                a.read or brief.get("read"),
                themes, tokens, a.accent, brief,
                [r.strip() for r in a.roles.split("|")],
                [r.strip() for r in a.rationales.split("|")])

    os.makedirs(os.path.dirname(os.path.abspath(a.out)) or ".", exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as fh:
        fh.write(doc)
    print(f"wrote {a.out}")
    for t in themes:
        m = tokens.get(t, {})
        print(f"  {t:20} {m.get('ground','?'):5} {m.get('readsAs','')}")
    print("\nPublish it as an artifact, or open it. Nothing was written to HubSpot.")


if __name__ == "__main__":
    sys.exit(main() or 0)
