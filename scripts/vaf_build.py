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

REGISTRY = {}
for _f in sorted(glob.glob(os.path.join(ROOT, "scripts/vaf_map_*.py"))):
    _m = importlib.import_module(os.path.basename(_f)[:-3])
    REGISTRY.update(_m.REGISTRY)


def page_for(slug):
    for p in CONTENT["pages"]:
        if slug_of(p["file"]) == slug:
            return p
    raise SystemExit(f"no page for slug {slug!r}")


def tpl_name(slug):
    return "templates/vaf/" + (slug.replace("/", "--") or "home") + ".html"


def order(page):
    comp = page.get("compose")
    comp = comp.get("showcase") if isinstance(comp, dict) else None
    secs = page["sections"]
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
    own = "".join(f'<script type="application/ld+json">{json.dumps(b, ensure_ascii=False)}</script>' for b in page.get("schema", []))
    return "{% raw %}" + blocks + own + "{% endraw %}"


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
    if args == ["all"]:
        return [slug_of(p["file"]) for p in CONTENT["pages"]]
    return ["" if a == "home" else a for a in args]


# ------------------------------------------------------------------ HubSpot writes
def cmd_templates(args):
    import vaf_upload as U
    import reskin
    from urllib.parse import quote
    for sl in slugs_from(args):
        text, path = template_for(page_for(sl))
        U.validate(path, text.encode())
        bd, b = U.body(path, text.encode())
        reskin._req("PUT", "/cms/v3/source-code/published/content/" + quote(f"{THEME}/{path}"), U.TOKEN, bd,
                    f"multipart/form-data; boundary={b}")
        print("  template", path)


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
        body = {"name": f"VAF | {pg['title'].split(' | ')[0]}"[:120], "slug": slug, "templatePath": f"{THEME}/{tpl_name(sl)}",
                "htmlTitle": pg["title"], "metaDescription": pg.get("description", ""), "headHtml": NOINDEX, "language": "en"}
        cur = existing.get(slug)
        if cur:
            reskin._req("PATCH", f"/cms/v3/pages/site-pages/{cur['id']}", T, json.dumps(body).encode(), "application/json")
            pid = cur["id"]
        else:
            pid = json.loads(reskin._req("POST", "/cms/v3/pages/site-pages", T, json.dumps(body).encode(), "application/json"))["id"]
        if cur and cur.get("state") != "DRAFT":
            reskin._req("POST", f"/cms/v3/pages/site-pages/{pid}/draft/push-live", T)
        else:   # first publish must be scheduled; push-live only updates a page that is already live
            when = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=15)).strftime("%Y-%m-%dT%H:%M:%SZ")
            reskin._req("POST", "/cms/v3/pages/site-pages/schedule", T, json.dumps({"id": pid, "publishDate": when}).encode(), "application/json")
        print(f"  page {pid} /{slug}")


if __name__ == "__main__":
    cmd, rest = sys.argv[1], sys.argv[2:]
    if cmd == "dry":
        print(template_for(page_for("" if rest[0] == "home" else rest[0]))[0])
    else:
        {"templates": cmd_templates, "pages": cmd_pages}[cmd](rest)
