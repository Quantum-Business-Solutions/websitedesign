#!/usr/bin/env python3
"""Build VAF pages in HubSpot: one template per page (modules + copy baked in as dnd_module defaults), then the pages.

    CLIENT_HUBSPOT_TOKEN=... python3 scripts/vaf_build.py templates <slug>... | all
    CLIENT_HUBSPOT_TOKEN=... python3 scripts/vaf_build.py pages     <slug>... | all
    python3 scripts/vaf_build.py dry <slug>                 # print the template, write nothing

Pages publish to the portal's hs-sites domain with noindex in headHtml. Removing that noindex is a launch gate.
"""
import importlib, json, os, re, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
from vaf_common import ROOT, slug_of, href, esc

PORTAL = "50498425"
THEME = "Van Ausdall and Farrar - Showcase"
NOINDEX = '<meta name="robots" content="noindex, nofollow">'
CONTENT = json.load(open(os.path.join(ROOT, "brands/vanausdall.content.json"), encoding="utf-8"))

_EXTRA = os.path.join(ROOT, "brands/vanausdall.extra-pages.json")      # pages added after the preview (entity facts, etc.)
if os.path.exists(_EXTRA):
    CONTENT["pages"] += [x for x in json.load(open(_EXTRA, encoding="utf-8")) if x["file"] not in {p["file"] for p in CONTENT["pages"]}]

# Rewritten page copy (local uniqueness, de-duplication): brands/vanausdall.overrides.*.json = {file: {title?, description?, sections?}}
for _o in sorted(glob.glob(os.path.join(ROOT, "brands/vanausdall.overrides.*.json"))):
    for _file, _ov in json.load(open(_o, encoding="utf-8")).items():
        for _pg in CONTENT["pages"]:
            if _pg["file"] == _file:
                _pg.update({k: v for k, v in _ov.items() if k in ("title", "description", "sections", "compose", "crumbs", "schema")})

def seo_titles():
    """Titles of 30 to 60 characters that carry the brand and the place; four meta descriptions that came through the migration as one word are rewritten."""
    BR = " | Van Ausdall & Farrar"
    FIX = {"about.html": "About Van Ausdall & Farrar | Indianapolis Since 1914", "company-facts.html": "Van Ausdall & Farrar Company Facts | Indianapolis Since 1914"}
    META = {
        "index.html": "Managed IT, cybersecurity, business phones, copiers and print, and document services for Indiana businesses, locally owned in Indianapolis since 1914.",
        "about.html": "Privately owned in Indianapolis since 1914, Van Ausdall & Farrar delivers managed IT, phones, print and document services across Indiana.",
        "case-studies/city-of-anderson.html": "How VAF's on-site facilities management program saved the City of Anderson over $40,000 a year on print, billing and purchasing.",
        "services/document-conversion.html": "Document scanning and conversion in Indianapolis: paperless digital imaging, searchable archives and secure electronic storage from VAF's Document Conversion Center.",
    }
    PLACES = ("indianapolis", "indiana", "fort wayne", "evansville", "bloomington", "carmel", "fishers", "noblesville", "greenwood", "muncie", "columbus", "south bend")
    fit = lambda c: 30 <= len(c) <= 60
    for pg in CONTENT["pages"]:
        f = pg["file"]
        if f in META: pg["description"] = META[f]
        if f in FIX: pg["title"] = FIX[f]; continue
        base = pg["title"]
        while re.search(r"\|\s*(VAF|Van Ausdall & Farrar)\s*$", base): base = re.sub(r"\s*\|\s*(VAF|Van Ausdall & Farrar)\s*$", "", base)
        base = base.strip()
        if f.startswith("case-studies/") and f != "case-studies.html":
            base = re.sub(r"\s*case study\s*$", "", base.split(",")[0].split(" |")[0].strip(), flags=re.I) + " Case Study"
            cands = [base + ", Indiana" + BR, base + ", Indiana | VAF", base + BR, base + " | VAF"]
        else:
            local = any(c in base.lower() for c in PLACES)
            cands = ([] if local or f.startswith(("policies/", "blog")) or f in ("index.html", "contact.html") else [base + " in Indianapolis" + BR, base + " in Indianapolis | VAF", base + " in Indiana | VAF"]) + [base + BR, base + " | VAF", base]
        pg["title"] = next((c for c in cands if fit(c)), min(cands, key=lambda c: abs(len(c) - 55)))


seo_titles()


def tidy_faqs():
    """Drop the placeholder answer the migration wrote on case studies; a question with no specific answer is worse than no question."""
    for pg in CONTENT["pages"]:
        for s in pg["sections"]:
            if s.get("type") == "faq": s["items"] = [i for i in s.get("items", []) if not str(i[1]).startswith("Services from across")]


tidy_faqs()

REGISTRY = {}
for _f in sorted(glob.glob(os.path.join(ROOT, "scripts/vaf_map_*.py"))):
    _m = importlib.import_module(os.path.basename(_f)[:-3])
    REGISTRY.update(_m.REGISTRY)


def page_for(slug):
    for p in CONTENT["pages"]:
        if slug_of(p["file"]) == slug:
            if p["file"].startswith("policies/") and p.get("crumbs"):
                p = dict(p, crumbs=[c for c in p["crumbs"] if c[0] != "Policies"])   # the "Policies" crumb pointed at /about
            return p
    raise SystemExit(f"no page for slug {slug!r}")


def tpl_name(slug):
    return "templates/vaf/" + (slug.replace("/", "--") or "home") + ".html"


def policy_sections(secs):
    """Legal pages read as documents: no sales buttons in the hero, no empty generic FAQ, no tool promo."""
    out = []
    for s in secs:
        s = dict(s)
        if s["type"] in ("hero", "hero-layered"):
            for k in ("primary", "secondary", "stats", "note", "image", "image_alt", "poster", "video", "bg"):
                s.pop(k, None)
            s["layout"] = "centered"
        if s["type"] == "faq" and not s.get("items"):
            continue
        out.append(s)
    return out


def _with_links(page, secs):
    """Insert the related-pages and related-blog sections before the FAQ (or the lead form)."""
    try:
        import vaf_links
        extra = vaf_links.extra_sections(page, CONTENT["pages"])
    except Exception as e:           # linking must never break a build
        print("  links skipped", page["file"], e, file=sys.stderr); return secs
    have = {s.get("id") for s in secs}
    extra = [x for x in extra if x.get("id") not in have]
    if not extra: return secs
    idx = next((i for i, s in enumerate(secs) if s["type"] == "faq"), next((i for i, s in enumerate(secs) if s["type"] == "leadform"), len(secs)))
    return secs[:idx] + extra + secs[idx:]


def order(page):
    comp = page.get("compose")
    comp = comp.get("showcase") if isinstance(comp, dict) else None
    secs = page["sections"]
    if page["file"].startswith("policies/"):
        secs = policy_sections(secs)
        page = dict(page, sections=secs)
    secs = _with_links(page, secs)
    if not comp:
        return secs
    by = {s.get("id"): s for s in secs if s.get("id")}
    return [by[c] for c in comp if c in by] or secs


def attr(name, value):
    if isinstance(value, str):
        v = value.replace("{%", "{ %").replace("{{", "{ {")
        return f'\n        {{% module_attribute "{name}" %}}{v}{{% end_module_attribute %}}'
    return f'\n        {{% module_attribute "{name}" is_json="true" %}}{json.dumps(value, ensure_ascii=False)}{{% end_module_attribute %}}'


def dnd(mod, params):
    blocks = "".join(attr(k, v) for k, v in params.items())
    return (f'    {{% dnd_section %}}\n      {{% dnd_module path="../../modules/{mod}", width=12 %}}{blocks}\n'
            f'      {{% end_dnd_module %}}\n    {{% end_dnd_section %}}\n')


def schema_html(page):
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    import preview
    blocks = preview.schema_blocks(CONTENT, page, "https://www.vanausdall.com", "showcase")
    drawn = any(x["type"] == "article" for x in page["sections"])   # the article module writes its own Article block
    own = "".join(f'<script type="application/ld+json">{json.dumps(b, ensure_ascii=False)}</script>' for b in page.get("schema", []) if not (drawn and b.get("@type") == "Article"))
    if page["file"].startswith("services/") and '"Service"' not in own:
        name = page["title"].split("|")[0].strip()
        svc = {"@context": "https://schema.org", "@type": "Service", "name": name, "serviceType": name,
               "description": page.get("description", ""), "url": f"https://www.vanausdall.com/{slug_of(page['file'])}",
               "provider": {"@id": "https://www.vanausdall.com/#organization"},
               "areaServed": [{"@type": "City", "name": "Indianapolis"}, {"@type": "State", "name": "Indiana"}]}
        own += f'<script type="application/ld+json">{json.dumps(svc, ensure_ascii=False)}</script>'
    return "{% raw %}" + (blocks + own).replace("&amp;", "&") + "{% endraw %}"   # JSON-LD is read as text, so an HTML entity would show up as the literal characters


def crumbs_html(page):
    c = page.get("crumbs")
    if not c or any(x["type"] == "article" for x in page["sections"]):   # the article module draws its own breadcrumb
        return ""
    if False:
        return ""
    items = "".join(f'<li>{"<span aria-current=page>" + esc(l) + "</span>" if i == len(c) - 1 else f"<a href=" + chr(34) + href(h) + chr(34) + ">" + esc(l) + "</a>"}</li>'
                    for i, (l, h) in enumerate(c))
    return f'<nav class="pv-crumbs" aria-label="Breadcrumb"><div class="q-container"><ol>{items}</ol></div></nav>\n'


HERO_LAYOUT = (("solutions", "layered"), ("industries", "layered"), ("case-studies.html", "layered"), ("about.html", "layered"),
               ("partners.html", "layered"), ("support.html", "split"), ("services/", "split"), ("locations", "split"))


def rhythm(items, page):
    """Variety without hand-editing 168 pages: hero treatment by kind of page, alternating section grounds,
    alternating image sides. Everything stays an ordinary editable field."""
    f = page["file"]
    flips = 0
    light = 0
    for i, (mod, params) in enumerate(items):
        if mod == "vaf-hero" and f != "index.html":
            for key, lay in HERO_LAYOUT:
                if f.startswith(key):
                    if lay == "layered" and not params.get("image", {}).get("src"):
                        lay = "centered"
                    params["layout"] = lay
                    if lay == "layered":
                        params.pop("note", None)
                        # the home page carries the two floating cards; elsewhere the hero is copy, stats and the picture
                        params.update(card_a_eyebrow="", card_a_title="", card_a_body="", card_a_items=[], card_a_label="",
                                      card_b_eyebrow="", card_b_title="", card_b_body="", card_b_links=[])
                    break
        im = params.get("image")
        if isinstance(im, dict) and im.get("src") and not (im.get("alt") or "").strip():
            h = re.sub(r"<[^>]+>", "", params.get("heading") or page["title"].split("|")[0]).strip()
            im["alt"] = h[:120]          # descriptive alt for search and screen readers
        if mod == "vaf-detail":
            params["flip"] = bool(flips % 2)
            flips += 1
        if mod not in ("vaf-hero", "vaf-casestudy", "vaf-seal", "vaf-proof", "vaf-cta", "vaf-band", "vaf-partners", "vaf-stats"):
            if "alt_bg" in params or mod in ("vaf-detail", "vaf-cards", "vaf-services", "vaf-resources", "vaf-related", "vaf-faq", "vaf-tabs", "vaf-timeline", "vaf-comparison", "vaf-testimonials", "vaf-locations"):
                params["alt_bg"] = bool(light % 2)
                light += 1
    return items


def template_for(page):
    slug = slug_of(page["file"])
    parts, missing = [], set()
    for s in order(page):
        if s["type"] not in REGISTRY or not os.path.isfile(os.path.join(ROOT, "themes/vaf/modules", REGISTRY[s["type"]][0] + ".module", "module.html")):
            missing.add(s["type"]); continue
        mod, fn = REGISTRY[s["type"]]
        out = fn(s)
        for o in (out if isinstance(out, list) else [out]):
            parts.append(o if isinstance(o, tuple) else (mod, o))
    parts = "".join(dnd(m, p) for m, p in rhythm(parts, page))
    if missing and os.environ.get("VAF_ALLOW_MISSING"):
        print(f"  WARNING {page['file']}: skipped section types with no module yet: {sorted(missing)}", file=sys.stderr)
    elif missing:
        raise SystemExit(f"{page['file']}: no module registered for section types {sorted(missing)}")
    label = re.sub(r"[^A-Za-z0-9 |&,'-]", "", page["title"])[:60]
    text = (f"<!--\n  templateType: page\n  label: VAF - {label}\n  isAvailableForNewContent: false\n-->\n"
            '{% extends "../layouts/vaf-base.html" %}\n'
            f"{{% block head_extra %}}\n{schema_html(page)}\n{{% endblock %}}\n"
            "{% block body %}\n" + crumbs_html(page) + '<main id="main">\n  {% dnd_area "main" label="Main content" %}\n'
            + "".join(parts) + "  {% end_dnd_area %}\n</main>\n{% endblock %}\n")
    return text, tpl_name(slug)


def slugs_from(args):
    # /blog and everything under it belongs to the HubSpot blog, not to site pages
    if args == ["all"]:
        return [slug_of(p["file"]) for p in CONTENT["pages"] if slug_of(p["file"]) != "blog" and not slug_of(p["file"]).startswith("blog/")]
    return ["" if a == "home" else a for a in args]


# ------------------------------------------------------------------ HubSpot writes
def retrying(fn, tries=5):
    import time, reskin as _r
    for i in range(tries):
        try:
            return fn()
        except _r.HubSpotError as e:
            m = str(e)
            if i == tries - 1 or not any(k in m for k in ("000", "429", " 500", " 502", " 503", " 504", "Connection reset", "transport")):
                raise
            time.sleep(2 ** (i + 1))


def cmd_templates(args):
    import vaf_upload as U
    import reskin
    from urllib.parse import quote
    for sl in slugs_from(args):
        text, path = template_for(page_for(sl))
        U.validate(path, text.encode())
        bd, b = U.body(path, text.encode())
        retrying(lambda: reskin._req("PUT", "/cms/v3/source-code/published/content/" + quote(f"{THEME}/{path}"), U.TOKEN, bd,
                                     f"multipart/form-data; boundary={b}"))
        print("  template", path)


def page_kind(file):
    """Page type, used as the name prefix in HubSpot's page list (sortable and searchable) and as the tag on the sign-off sheet."""
    f = file
    if f == "index.html": return "Home"
    if f.startswith("solutions"): return "Pillar"
    if f.startswith("services/"): return "Service"
    if f.startswith("industries/"): return "Industry"
    if f.startswith("locations/"): return "Location"
    if f.startswith("case-studies/"): return "Case study"
    if f.startswith("policies/"): return "Policy"
    if f.startswith("blog"): return "Blog"
    if f in ("industries.html", "case-studies.html", "locations.html"): return "Hub"
    if f in ("technology-strength-assessment.html", "print-assessment.html", "cost-calculator.html", "cio-ai-playbook.html", "downloads.html", "virtualsitevisit.html"): return "Tool"
    if f in ("support.html", "contact.html"): return "Support"
    return "Company"


def meta_desc(page):
    """120 to 158 characters: a short description is topped up with the brand line, never padded with filler."""
    d = (page.get("description") or "").strip()
    if len(d) < 115:
        for tail in (" Van Ausdall & Farrar, Indianapolis office technology since 1914.", " Van Ausdall & Farrar, since 1914."):
            if 115 <= len(d + tail) <= 158:
                return d + tail
        d = d + " Van Ausdall & Farrar, Indianapolis office technology since 1914."
    return d[:158].rsplit(" ", 1)[0] if len(d) > 160 else d


def og_image(page):
    """Share image: the page's own first image, else the home hero poster (never the stock file the old site used)."""
    from vaf_common import A
    for s in page["sections"]:
        if s.get("image"):
            return A(s["image"])
    return A("assets/hero-poster")


def cmd_pages(args):
    import datetime, vaf_upload as U, reskin
    T = U.TOKEN
    existing, after = {}, None
    while True:
        r = reskin.get_json("/cms/v3/pages/site-pages?limit=100" + (f"&after={after}" if after else ""), T)
        for x in r.get("results", []):
            existing[x.get("slug", "")] = x
        after = (r.get("paging") or {}).get("next", {}).get("after")
        if not after:
            break
    for sl in slugs_from(args):
        pg = page_for(sl)
        slug = sl                       # the home page is the site root (empty slug)
        body = {"name": f"{page_kind(pg['file'])} | {pg['title'].split(' | ')[0]}"[:120], "slug": slug, "templatePath": f"{THEME}/{tpl_name(sl)}",
                "htmlTitle": pg["title"], "metaDescription": meta_desc(pg), "headHtml": NOINDEX, "language": "en",
                "featuredImage": og_image(pg), "featuredImageAltText": pg["title"].split("|")[0].strip()}
        cur = existing.get(slug)
        if cur:
            retrying(lambda: reskin._req("PATCH", f"/cms/v3/pages/site-pages/{cur['id']}", T, json.dumps(body).encode(), "application/json"))
            pid = cur["id"]
        else:
            pid = json.loads(retrying(lambda: reskin._req("POST", "/cms/v3/pages/site-pages", T, json.dumps(body).encode(), "application/json")))["id"]
        if cur and cur.get("state") != "DRAFT":
            retrying(lambda: reskin._req("POST", f"/cms/v3/pages/site-pages/{pid}/draft/push-live", T))
        else:   # first publish must be scheduled; push-live only updates a page that is already live
            when = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=15)).strftime("%Y-%m-%dT%H:%M:%SZ")
            retrying(lambda: reskin._req("POST", "/cms/v3/pages/site-pages/schedule", T, json.dumps({"id": pid, "publishDate": when}).encode(), "application/json"))
        print(f"  page {pid} /{slug}")


if __name__ == "__main__":
    cmd, rest = sys.argv[1], sys.argv[2:]
    if cmd == "dry":
        print(template_for(page_for("" if rest[0] == "home" else rest[0]))[0])
    else:
        {"templates": cmd_templates, "pages": cmd_pages}[cmd](rest)
