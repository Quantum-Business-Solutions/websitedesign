#!/usr/bin/env python3
"""The gate for a /directions build. It runs inside the Website directions workflow and by hand.

    python3 scripts/directions_qa.py <slug>            # content checks, then the rendered checks
    python3 scripts/directions_qa.py <slug> --no-render

It reads brands/<slug>.content.json, brands/<slug>.build.json and the rendered output folder, prints one line per check
(PASS / WARN / FAIL) and writes <out>/qa.json and <out>/claims-register.csv. Exit code 1 when anything FAILs.

Why this exists. The first two automated builds (IMS and DMP, 9 Nov 2026) shipped with no gate beyond build.py's SEO score:
a white headline on a white scrim, a placeholder red accent, a display face the client does not use, a home page with
six sections where the Van Ausdall home has twenty-four, and a score that read null. Each check below is a defect a
person had to find by eye on Kelly, Revolution or Van Ausdall (process/qa-findings.md, process/directions-standard.md).
FAIL means do not hand the link to a client; WARN means a person looks before it goes.
"""
from __future__ import annotations

import csv
import json
import os
import re
import subprocess
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

STARTER = ["CLIENT NAME", "START HEADING", "SUBMIT LABEL", "000-000-0000", "lorem ipsum", "<angle", "TODO", "PLACEHOLDER"]
# Words that promise more than any company can prove. A sentence that carries one must be listed in content["claims_ok"]
# with the client's own page as its source, or the build stops.
ABSOLUTES = re.compile(
    r"\b(guarantee[sd]?|unconditional(ly)?|100\s?%|zero (downtime|risk|defects)|never (miss|fail|lose|down)|"
    r"always (on|available|there)|every (single )?(customer|client|location|branch|office|time)|world[- ]class|best[- ]in[- ]class|"
    r"industry[- ]leading|cutting[- ]edge|state[- ]of[- ]the[- ]art|seamless(ly)?|number (one|1)|unmatched|unrivall?ed|second to none)\b", re.I)
COMMITMENTS = re.compile(
    r"\b(same[- ]day|next[- ]day|within (an? |one |1 |two |2 |four |4 |24 |48 )?(business )?(hour|day)s?|24/7|around the clock)\b", re.I)
SAVINGS = re.compile(r"\b(save[sd]?|saving|savings|reduce[sd]?|cut)\b[^.]{0,40}\b\d{1,3}\s?%", re.I)
FACTY = re.compile(r"(\d[\d,.]*\s?%|\$\s?\d|\b(19|20)\d{2}\b|\b\d[\d,]*\+? (years|offices|locations|technicians|employees|customers|clients|partners|awards))", re.I)
SKIP_KEYS = {"href", "src", "image", "poster", "model", "video", "id", "type", "logo", "icon", "file", "slug", "path", "alt_src",
             "quote", "quotes", "schema", "mainEntityOfPage"}   # a customer's own words and JSON-LD are not our claims


def strings(o, skip=SKIP_KEYS):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for k, v in o.items():
            if k in skip:
                continue
            yield from strings(v, skip)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v, skip)


def page_strings(pg: dict):
    """What a visitor reads on a page, leaving out testimonial sections (the customer's words, not ours)."""
    body = {k: v for k, v in pg.items() if k != "sections"}
    yield from strings(body)
    for sec in pg.get("sections", []):
        if sec.get("type") in ("testimonials",):
            continue
        yield from strings(sec)


def words(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9'’-]+", text))


def shingles(text: str, n=5):
    w = re.findall(r"[a-z0-9']+", text.lower())
    return {" ".join(w[i:i + n]) for i in range(max(0, len(w) - n + 1))}


class Gate:
    def __init__(self):
        self.rows: list[dict] = []

    def add(self, level: str, check: str, msg: str, where: str = ""):
        self.rows.append({"level": level, "check": check, "message": msg, "where": where})

    def ok(self, check, msg=""):
        self.add("PASS", check, msg)

    @property
    def failed(self):
        return any(r["level"] == "FAIL" for r in self.rows)


def write_qa_page(out: str, slug: str, client: str, rows: list) -> None:
    """<out>/qa/index.html: the gate's result beside pictures of each direction's home page at 1280 and 390, so the
    person who opens the build in Client Command judges it by eye and not from a pass or fail alone. Internal: noindex."""
    import html as _h
    qa = os.path.join(out, "qa")
    sp = os.path.join(qa, "shots.json")
    if not os.path.exists(sp):
        return
    shots = json.load(open(sp, encoding="utf-8"))
    e = _h.escape
    n = Counter(r["level"] for r in rows)
    order = {"FAIL": 0, "WARN": 1, "PASS": 2}
    trs = "".join(f'<tr class="{r["level"].lower()}"><td><b>{r["level"]}</b></td><td>{e(r["check"])}</td><td>{e(r["message"])}</td><td>{e(r.get("where", ""))}</td></tr>'
                  for r in sorted(rows, key=lambda r: order.get(r["level"], 3)))
    cols = []
    for d in dict.fromkeys(s["dir"] for s in shots):
        a = next((s for s in shots if s["dir"] == d and s["w"] == 1280), None)
        b = next((s for s in shots if s["dir"] == d and s["w"] == 390), None)
        pics = "".join(f'<a href="{e(s["file"])}"><img src="{e(s["file"])}" alt="{e(d)} home page at {s["w"]} wide" loading="lazy" style="width:{"72%" if s["w"] == 1280 else "24%"}"></a>' for s in (a, b) if s)
        cols.append(f'<section><h2>{e(d.title())}</h2><p><a href="../{e(d)}/index.html">Open the live page</a></p><div class="pics">{pics}</div></section>')
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow"><title>{e(client)}: quality check and pictures</title>
<style>body{{margin:0;font:16px/1.55 Arial,Helvetica,sans-serif;color:#14171c;background:#f3f4f6}}main{{max-width:1500px;margin:0 auto;padding:28px 20px 80px}}
h1{{font-size:28px;line-height:1.15;margin:0 0 6px}}h2{{font-size:20px;margin:0 0 4px}}p{{margin:0 0 14px;color:#4a5060}}a{{color:#0b4f9e}}
.sum{{display:flex;gap:10px;flex-wrap:wrap;margin:14px 0 22px}}.sum span{{padding:8px 14px;border-radius:999px;font-weight:700;background:#fff;border:1px solid #d9dce2}}
.sum .f{{background:#fde8e8;border-color:#e3a3a3;color:#8a1c1c}}.sum .w{{background:#fff4d6;border-color:#e0c36a;color:#6b4e00}}.sum .p{{background:#e4f5e8;border-color:#9fd0aa;color:#1d5e2c}}
.grid{{display:grid;grid-template-columns:repeat({max(1, len(cols))},minmax(0,1fr));gap:20px;align-items:start}}section{{background:#fff;border:1px solid #d9dce2;border-radius:10px;padding:16px}}
.pics{{display:flex;gap:4%;align-items:flex-start}}.pics img{{display:block;width:100%;border:1px solid #d9dce2;border-radius:4px}}.pics a{{display:contents}}
table{{width:100%;border-collapse:collapse;background:#fff;border:1px solid #d9dce2;border-radius:10px;margin-top:26px;font-size:14.5px}}td{{padding:9px 12px;border-top:1px solid #eceef2;vertical-align:top}}
tr.fail td:first-child{{color:#a11919}}tr.warn td:first-child{{color:#7a5a00}}tr.pass td:first-child{{color:#1d6b33}}
@media(max-width:900px){{.grid{{grid-template-columns:1fr}}}}</style></head><body><main>
<h1>{e(client)}: quality check and pictures</h1>
<p>The home page of each direction, whole, at 1280 and 390 wide, taken by the gate (scripts/directions_qa.py). Look before the link goes to the client: a FAIL stops it, a WARN is read by a person, and the beauty bar in process/directions-standard.md section 9 says what good looks like.</p>
<div class="sum"><span class="f">{n["FAIL"]} fail</span><span class="w">{n["WARN"]} warn</span><span class="p">{n["PASS"]} pass</span><a href="contact-sheet.jpg">One-image contact sheet</a></div>
<div class="grid">{"".join(cols)}</div>
<table><tbody>{trs}</tbody></table>
</main></body></html>"""
    open(os.path.join(qa, "index.html"), "w", encoding="utf-8").write(doc)


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        raise SystemExit(__doc__)
    slug = argv[0]
    render = "--no-render" not in argv
    g = Gate()
    content = json.load(open(os.path.join(ROOT, "brands", f"{slug}.content.json"), encoding="utf-8"))
    cfg = json.load(open(os.path.join(ROOT, "brands", f"{slug}.build.json"), encoding="utf-8"))
    out = os.path.normpath(os.path.join(ROOT, cfg.get("out", f"../out-{slug}")))
    if "--out" in argv:                       # test against another folder without touching the real output
        out = os.path.abspath(argv[argv.index("--out") + 1])
    brief = {}
    bp = os.path.join(ROOT, "brands", f"{slug}.brief.json")
    if os.path.exists(bp):
        brief = json.load(open(bp, encoding="utf-8"))
    branding = brief.get("branding") or {}
    brand = content.get("brand") or {}
    pages = content.get("pages") or []
    plist = pages if isinstance(pages, list) else list(pages.values())

    # ---- 1. starter text, em dashes, exclamation marks, in everything a visitor can read
    visible = [(pg.get("file") or pg.get("title") or "?", t) for pg in plist for t in page_strings(pg)]
    visible += [("brand", t) for t in strings({k: v for k, v in brand.items() if k in ("tagline", "legal", "footer_columns", "utility")})]
    bad = [(w, t[:60]) for w, t in visible for s in STARTER if s.lower() in t.lower()]
    g.add("FAIL", "starter-text", f"{len(bad)} starter strings left, e.g. {bad[0]}", bad[0][0]) if bad else g.ok("starter-text")
    dashes = sorted({w for w, t in visible if "—" in t or "–" in t})
    g.add("FAIL", "em-dash", f"em or en dashes on {len(dashes)} pages", ", ".join(dashes[:4])) if dashes else g.ok("em-dash")
    bangs = sorted({w for w, t in visible if "!" in t})
    g.add("WARN", "exclamation", f"exclamation marks on {len(bangs)} pages", ", ".join(bangs[:4])) if bangs else g.ok("exclamation")

    # ---- 2. claims: absolutes, commitments and savings need the client's own page as a source
    allowed = [c["text"].lower() for c in content.get("claims_ok", []) if c.get("text") and c.get("source")]
    unsourced = []
    for w, t in visible:
        for rx, kind in ((ABSOLUTES, "absolute"), (COMMITMENTS, "commitment"), (SAVINGS, "savings figure")):
            for m in rx.finditer(t):
                sentence = next((x for x in re.split(r"(?<=[.?!])\s+", t) if m.group(0) in x), t)
                if not any(a in sentence.lower() or sentence.lower() in a for a in allowed):
                    unsourced.append((kind, w, sentence[:110]))
    if unsourced:
        k = Counter(x[0] for x in unsourced)
        g.add("FAIL", "claims", f"{len(unsourced)} unsourced claims ({dict(k)}); first: [{unsourced[0][0]}] {unsourced[0][2]}",
              unsourced[0][1])
    else:
        g.ok("claims")

    # ---- 3. the claims register: every figure, year and count, by page, for the client to confirm
    reg = []
    for pg in plist:
        for t in page_strings(pg):
            for sent in re.split(r"(?<=[.?!])\s+", t):
                if FACTY.search(sent):
                    reg.append((pg.get("file") or pg.get("title") or "?", sent.strip()[:220]))
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "claims-register.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["page", "sentence", "source (fill in)", "confirmed by client"])
        w.writerows([r + ("", "") for r in reg])
    g.add("PASS", "claims-register", f"{len(reg)} figures and dates listed for the client to confirm (claims-register.csv)")

    # ---- 4. near-duplicate pages (a mirrored sitemap makes competing pages)
    texts = {pg.get("file") or pg.get("title"): " ".join(page_strings(pg)) for pg in plist}
    sh = {k: shingles(v) for k, v in texts.items() if words(v) >= 120}
    dup = []
    keys = list(sh)
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            u = len(sh[a] | sh[b])
            if u and len(sh[a] & sh[b]) / u > 0.5:
                dup.append((a, b, round(len(sh[a] & sh[b]) / u, 2)))
    g.add("FAIL" if any(d[2] > 0.8 for d in dup) else "WARN", "duplicate-pages", f"{len(dup)} page pairs overlap by more than half, e.g. {dup[0]}", dup[0][0]) if dup else g.ok("duplicate-pages")
    thin = [(k, words(v)) for k, v in texts.items() if words(v) < 200 and not str(k).endswith(("contact.html", "thanks.html"))]
    g.add("WARN", "thin-pages", f"{len(thin)} pages under 200 words, e.g. {thin[0]}", thin[0][0]) if thin else g.ok("thin-pages")

    # ---- 5. richness: the Van Ausdall home runs twenty-four sections over twenty module types; a flat home reads weak
    home = next((p for p in plist if p.get("file") in ("index.html", "home.html")), plist[0] if plist else {})
    types = [s.get("type") for s in home.get("sections", [])]
    distinct = len(set(types))
    if len(types) < 10 or distinct < 8:
        g.add("FAIL", "home-richness", f"home has {len(types)} sections over {distinct} module types; the Kelly and Van Ausdall homes have 11 and 24. See process/directions-standard.md, 'The home page kit'", "index.html")
    else:
        g.ok("home-richness", f"{len(types)} sections, {distinct} module types")
    alltypes = Counter(s.get("type") for p in plist for s in p.get("sections", []))
    g.add("WARN", "module-variety", f"only {len(alltypes)} module types across the whole site (Van Ausdall uses 36)") if len(alltypes) < 14 else g.ok("module-variety", f"{len(alltypes)} module types")
    g.add("WARN", "page-count", f"{len(plist)} pages; the build should cover every service line, industry and office the client's site names") if len(plist) < 18 else g.ok("page-count", f"{len(plist)} pages")

    # ---- 6. imagery: one picture on many pages is how the Revolution scorecard read "stock"
    use = Counter()
    for pg in plist:
        for img in set(re.findall(r"assets/[A-Za-z0-9_./-]+\.(?:png|jpe?g|webp|svg)", json.dumps(pg))):
            use[img] += 1
    over = [(k, v) for k, v in use.items() if v > 6 and "logo" not in k]
    g.add("WARN", "image-reuse", f"{len(over)} images used on more than 6 pages, e.g. {over[0]}") if over else g.ok("image-reuse")
    own = [k for k in use if "library" not in k]
    g.add("WARN", "own-imagery", "no client photography on any page; the preview is all stand-in imagery") if not own and plist else g.ok("own-imagery")

    # ---- 7. brand fidelity, against what Client Command measured at dispatch (brief.branding) when it did
    if branding.get("colors"):
        want = (branding["colors"].get("primary") or branding["colors"].get("accent") or "").lower()
        have = (brand.get("accent") or "").lower()
        if want and have and want != have:
            g.add("FAIL", "brand-accent", f"accent is {have}; the live site's measured primary is {want}")
        else:
            g.ok("brand-accent", have)
        fonts = {f.get("role"): f.get("family") for f in branding.get("fonts", [])}
        if fonts and not brand.get("fonts"):
            g.add("WARN", "brand-fonts", f"the live site sets {fonts}; brand.fonts is not set, so the house type (Open Sans) is used")
        elif fonts:
            g.ok("brand-fonts", json.dumps(brand.get("fonts")))
        if (branding.get("radius") is not None or branding.get("button_radius") is not None) and brand.get("radius") is None and brand.get("button_radius") is None:
            g.add("WARN", "brand-radius", f"the live site's corners are {branding.get('radius')}px and its buttons {branding.get('button_radius')}px; brand.radius and brand.button_radius are not set")
    elif not brand.get("accent"):
        g.add("FAIL", "brand-accent", "no accent colour at all")
    if re.search(r"placeholder (wordmark|accent|logo|colou?r)|(logo|colou?r|accent)[^.]{0,40}(is|are) (a )?placeholder", " ".join(strings(content.get("pitch", {}))), re.I) and brand.get("accent"):
        g.add("WARN", "brand-placeholder", "the pitch still says the logo or colour is a placeholder; replace it or say what is missing")
    logo = brand.get("logo")
    if logo:
        lp = os.path.join(out, logo)
        if not os.path.exists(lp):
            g.add("FAIL", "logo", f"{logo} is not in the output folder")
        elif not lp.endswith(".svg") and os.path.getsize(lp) < 4000:
            g.add("WARN", "logo", f"{logo} is a small raster; ask for the vector")
        else:
            g.ok("logo", logo)
    else:
        g.add("FAIL", "logo", "no logo")

    # ---- 8. the pitch has an opinion and an honest to-confirm list
    pitch = content.get("pitch") or {}
    g.add("FAIL", "pitch-confirm", "pitch.confirm is empty; every unsourced fact belongs there") if not pitch.get("confirm") else g.ok("pitch-confirm", f"{len(pitch['confirm'])} items")
    g.add("WARN", "pitch-recommend", "no recommended direction") if not cfg.get("recommend") else g.ok("pitch-recommend", cfg["recommend"])

    # ---- 9. rendered checks (a real browser): the typeface, the hero's legibility, overflow, the logo
    if render and os.path.isdir(out):
        r = subprocess.run(["node", os.path.join(HERE, "directions_qa.mjs"), out, json.dumps({
            "heading": (brand.get("fonts") or {}).get("heading"),
            "radius": brand.get("radius"), "button_radius": brand.get("button_radius"),
            "dirs": [t.replace("Quantum ", "").lower() for t in cfg.get("themes", [])],
        })], cwd=HERE, text=True, capture_output=True)
        try:
            for row in json.loads(r.stdout):
                g.rows.append(row)
        except Exception:  # noqa: BLE001
            g.add("WARN", "rendered", "the browser checks did not run: " + (r.stderr or r.stdout)[-200:])

    json.dump({"slug": slug, "rows": g.rows, "contact_sheet": "qa/contact-sheet.jpg" if os.path.exists(os.path.join(out, "qa", "contact-sheet.jpg")) else None,
               "pictures": "qa/index.html" if os.path.exists(os.path.join(out, "qa", "shots.json")) else None},
              open(os.path.join(out, "qa.json"), "w"), indent=1)
    write_qa_page(out, slug, content.get("client", slug), g.rows)
    width = max(len(r["check"]) for r in g.rows)
    for r in g.rows:
        print(f"  {r['level']:4}  {r['check']:<{width}}  {r['message']}" + (f"   [{r['where']}]" if r["where"] else ""))
    n = Counter(r["level"] for r in g.rows)
    print(f"\n  {n['PASS']} pass, {n['WARN']} warn, {n['FAIL']} fail")
    if os.path.exists(os.path.join(out, "qa", "index.html")):
        print(f"  pictures: {os.path.join(out, 'qa', 'index.html')} and {os.path.join(out, 'qa', 'contact-sheet.jpg')}")
    return 1 if g.failed else 0


if __name__ == "__main__":
    sys.exit(main())
