#!/usr/bin/env python3
"""Build Van Ausdall & Farrar pages in HubSpot on the cloned Showcase theme.

Same pattern as Revolution and Kelly Office: one generated template per page, the
theme's own modules with the page copy baked in as dnd_module defaults, so every
section is drag and drop and every field is editable in the page editor.

    env -u QBS_HUBSPOT_TOKEN -u QBS_DEV_HUBSPOT_TOKEN \
        CLIENT_HUBSPOT_TOKEN="$(cat <token file>)" \
        python3 scripts/hubspot_vaf.py chrome            # header + footer modules
        python3 scripts/hubspot_vaf.py templates <slug>... # write templates
        python3 scripts/hubspot_vaf.py pages <slug>...     # create + publish pages

Pages are published to the portal's hs-sites domain with noindex in headHtml.
Removing that noindex is a launch gate (see ClientCommand website-push-plan).
"""
import json, os, re, sys, html
sys.path.insert(0, os.path.dirname(__file__))
import reskin

PORTAL = "50498425"
THEME = "Van Ausdall and Farrar - Showcase"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = json.load(open(os.path.join(ROOT, "brands/vanausdall.content.json"), encoding="utf-8"))
ASSET_BASE = "https://van-ausdall.vercel.app"      # TEMPORARY: move to HubSpot Files before launch
FORM_ID = "e84ef7ce-04f2-4fef-b539-4351bde13b48"      # VAF | Consultation request (preview), in portal 50498425
NOINDEX = '<meta name="robots" content="noindex, nofollow">'
TOKEN = os.environ.get("CLIENT_HUBSPOT_TOKEN", "")


# ------------------------------------------------------------------ helpers
def slug_of(file):
    s = re.sub(r"\.html$", "", file)
    return "" if s == "index" else re.sub(r"/index$", "", s)


def href(h):
    """Preview-relative link -> site path."""
    if not h or h.startswith(("http", "tel:", "mailto:", "#")):
        return h or ""
    h = re.sub(r"^(\.\./)+", "", h)
    frag = ""
    if "#" in h:
        h, frag = h.split("#", 1)
        frag = "#" + frag
    return "/" + slug_of(h) + frag


def img(p):
    if not p:
        return ""
    p = re.sub(r"^(\.\./)+", "", p)
    return p if p.startswith("http") else f"{ASSET_BASE}/{p.lstrip('/')}"


def url(h):
    return {"href": href(h), "type": "EXTERNAL"}


def esc(s):
    return html.escape(s or "", quote=False)


# --------------------------------------------------------- section -> modules
def head(eb, h, intro=None):
    out = ""
    if eb:
        out += f'<div class="q-eyebrow">{esc(eb)}</div>'
    if h:
        out += f'<h2 class="q-h2" style="margin-top:22px">{h if "<" in h else esc(h)}</h2>'
    if intro:
        out += f'<p class="q-lead">{esc(intro)}</p>'
    return out


def rich_head(s):
    return ("quantum-rich-text", {"prose": head(s.get("eyebrow"), s.get("heading"), s.get("intro")),
                                  "padding": "none", "maxw": "wide"})


def cols(items, per):
    return ("quantum-columns", {"per_row": str(per), "boxed": True,
            "cols": [{"col_body": f"<h3>{esc(t)}</h3><p>{esc(b)}</p>"} for t, b, *_ in items]})


def map_section(s, page):
    """Return a list of (module, params) for one content section."""
    t = s["type"]
    P = {}
    if t in ("hero", "hero-layered"):
        has_img = bool(s.get("image"))
        P = {"layout": "split" if has_img else "centered", "eyebrow": s.get("eyebrow", ""),
             "heading": s["heading"], "subhead": s.get("subhead", ""),
             "primary_label": (s.get("primary") or {}).get("label", ""),
             "primary_url": url((s.get("primary") or {}).get("href")),
             "secondary_label": (s.get("secondary") or {}).get("label", ""),
             "secondary_url": url((s.get("secondary") or {}).get("href")),
             "image": {"src": img(s.get("image")), "alt": s.get("image_alt", "")}}
        return [("quantum-hero", P)]
    if t == "detail":
        body = f"<p>{esc(s.get('body'))}</p>"
        if s.get("bullets"):
            body += "<ul>" + "".join(f"<li>{esc(b)}</li>" for b in s["bullets"]) + "</ul>"
        return [("quantum-feature-split", {"eyebrow": s.get("eyebrow", ""), "heading": s.get("heading", ""),
                 "body_text": body, "image": {"src": img(s.get("image")), "alt": s.get("image_alt", "")},
                 "flip": bool(s.get("flip")), "cta_label": ""})]
    if t == "cards":
        n = len(s["items"]); return [rich_head(s), cols(s["items"], 4 if n % 4 == 0 else (2 if n == 2 or n == 4 else 3))]
    if t == "faq":
        return [("quantum-faq", {"heading": s.get("heading", ""),
                 "items": [{"q": q, "a": a} for q, a, *_ in s["items"]]})]
    if t == "testimonials":
        return [("quantum-testimonial-slider", {"items": [
                {"quote": q, "who": w, "role": r} for q, w, r, *_ in s["items"]]})]
    if t == "proof":
        return [("quantum-pullquote", {"quote": s["text"], "attribution": s.get("source", "")})]
    if t == "checklist":
        return [("quantum-is-this-you", {"eyebrow": s.get("eyebrow", ""), "heading": s.get("heading", ""),
                 "intro": s.get("intro", ""), "items": [{"q": q} for q in s["items"]],
                 "cta_label": s.get("cta_label") or "Schedule a consultation",
                 "cta_url": href(s.get("cta_href") or "contact.html")})]
    if t in ("flow", "timeline", "process"):
        if t == "flow":
            steps = [{"num": f"{i+1:02d}", "title": f"{x['label']}: {x['title']}", "step_body": x["body"]}
                     for i, x in enumerate(s["steps"])]
        elif t == "process":
            steps = [{"num": f"{i+1:02d}", "title": a, "step_body": b} for i, (a, b, *_) in enumerate(s["stages"])]
        else:
            steps = [{"num": a, "title": b, "step_body": c} for a, b, c, *_ in s["items"]]
        return [("quantum-timeline", {"eyebrow": s.get("eyebrow", ""), "heading": s.get("heading", ""), "steps": steps})]
    if t == "beforeafter":
        b, a = s["before"], s["after"]
        rows = [{"row_label": f"{i+1:02d}", "a": y, "b": x} for i, (x, y) in enumerate(zip(b["items"], a["items"]))]
        return [("quantum-comparison", {"heading": re.sub(r"^Drag to compare ", "Compare ", s.get("heading", "")), "col_a": a.get("title", "After"),
                 "col_b": b.get("title", "Before"), "rows": rows})]
    if t == "stats":
        return [("quantum-stats-band", {"stats": [{"v": v, "k": k} for v, k, *_ in s["items"]]})]
    if t == "casestudy":
        return [("quantum-case-study", {"eyebrow": s.get("eyebrow", ""), "heading": s.get("heading", ""),
                 "quote": s.get("quote", ""), "attribution": s.get("attribution", ""),
                 "metrics": [{"k": k, "v": v} for k, v, *_ in s.get("metrics", [])]})]
    if t == "partners":
        return [("quantum-logo-strip", {"caption": s.get("caption", ""),
                 "logos": [{"logo_label": x if isinstance(x, str) else x[0]} for x in s["items"]]})]
    if t == "cta":
        return [("quantum-cta-band", {"heading": s["heading"], "subhead": s.get("subhead", ""),
                 "cta_label": s["primary"]["label"], "url": url(s["primary"]["href"])})]
    if t in ("leadform", "contact"):
        return [("quantum-contact", {"heading": s.get("heading", ""), "body_text": s.get("body", ""),
                 "email": CONTENT["brand"]["email"], "meeting_url": url("contact.html"),
                 "form": {"form_id": FORM_ID, "portal_id": PORTAL, "form_type": "HUBSPOT", "response_type": "inline",
                          "message": "Thank you. A person from the Indianapolis office will reply to set a time."}})]
    if t == "services":
        return [("quantum-services-list", {"heading": s.get("heading", ""), "intro": s.get("intro", ""),
                 "items": [{"num": f"{i+1:02d}", "title": a, "item_body": b, "url": url(c)}
                           for i, (a, b, c, *_) in enumerate(s["items"])]})]
    if t == "wheel":
        return [("quantum-services-list", {"heading": s.get("heading", ""), "intro": s.get("intro", ""),
                 "items": [{"num": f"{i+1:02d}", "title": a, "item_body": b, "url": url(c)}
                           for i, (a, b, c, *_) in enumerate(s["items"])]})]
    if t == "tabs":
        return [("quantum-tabs", {"heading": s.get("heading", ""),
                 "tabs": [{"tab_label": x["label"], "tab_body": x["body"]} for x in s["items"]]})]
    if t == "article":
        prose = (f'<div class="q-eyebrow">{esc(s.get("category"))}</div><h1 class="q-h1" style="margin-top:22px">{esc(s["heading"])}</h1>'
                 f'<p class="q-lead">{esc(s.get("standfirst"))}</p>')
        for ch in s.get("chapters", []):
            prose += f'<h2>{esc(ch["title"])}</h2>' + "".join(f"<p>{esc(x)}</p>" for x in ch.get("paras", []))
        out = [("quantum-rich-text", {"prose": prose, "maxw": "prose"})]
        if s.get("image"):
            out.insert(0, ("quantum-image", {"image": {"src": img(s["image"]), "alt": s.get("image_alt", "")}, "width": "1000"}))
        return out
    if t in ("related", "resources", "values", "locations", "seal", "band", "fleet", "hotspots", "map", "video",
             "model3d", "calculator", "comparison", "leadership"):
        # Generic, still fully editable: heading block + columns.
        items = s.get("items") or s.get("people") or []
        norm = []
        for it in items:
            if isinstance(it, dict):
                norm.append((it.get("title") or it.get("name") or it.get("k") or "", it.get("body") or it.get("sub") or ""))
            else:
                parts = [x for x in it if isinstance(x, str) and not x.endswith((".html", ".jpg", ".png"))]
                norm.append((parts[1] if len(parts) > 2 else parts[0], parts[2] if len(parts) > 2 else (parts[1] if len(parts) > 1 else "")))
        out = [rich_head(s)]
        if norm:
            out.append(cols(norm, 3))
        return out
    return [("quantum-rich-text", {"prose": head(s.get("eyebrow"), s.get("heading"), s.get("intro"))})]


# -------------------------------------------------------------- template text
def attr(name, value):
    if isinstance(value, str):
        v = value.replace("{%", "{ %").replace("{{", "{ {")
        return f'\n        {{% module_attribute "{name}" %}}{v}{{% end_module_attribute %}}'
    return f'\n        {{% module_attribute "{name}" is_json="true" %}}{json.dumps(value, ensure_ascii=False)}{{% end_module_attribute %}}'


def dnd(mod, params, bg=None):
    blocks = "".join(attr(k, v) for k, v in params.items())
    return (f'    {{% dnd_section %}}\n      {{% dnd_module path="../../modules/{mod}", width=12 %}}{blocks}\n'
            f'      {{% end_dnd_module %}}\n    {{% end_dnd_section %}}\n')


def page_for(slug):
    for p in CONTENT["pages"]:
        if slug_of(p["file"]) == slug:
            return p
    raise SystemExit(f"no page for slug {slug!r}")


def order(page):
    comp = (page.get("compose") or {})
    comp = comp.get("showcase") if isinstance(comp, dict) else None
    secs = page["sections"]
    if not comp:
        return secs
    by = {s.get("id"): s for s in secs if s.get("id")}
    return [by[c] for c in comp if c in by] or secs


def template_for(page):
    slug = slug_of(page["file"]) or "home"
    parts = []
    for s in order(page):
        for mod, params in map_section(s, page):
            parts.append(dnd(mod, params))
    body = "".join(parts)
    jsonld = ""
    return (f"<!--\n  templateType: page\n  label: VAF - {page['title'][:60].replace('-->','')}\n  isAvailableForNewContent: false\n-->\n"
            '{% extends "../layouts/base.html" %}\n{% block body %}\n<main id="main">\n  {% dnd_area "main" label="Main content" %}\n'
            f"{body}  {{% end_dnd_area %}}\n</main>\n{{% endblock %}}\n"), f"templates/vaf/{slug.replace('/', '--') or 'home'}.html"



# ----------------------------------------------------------- header + footer
def _lnk(h):
    return {"url": {"content_id": None, "type": "EXTERNAL", "href": href(h)}, "open_in_new_tab": False, "no_follow": False}


def _f(id, label, type, default=None, **kw):
    d = {"id": id, "name": id, "label": label, "type": type}
    if default is not None:
        d["default"] = default
    d.update(kw)
    return d


def _link(id, label, h=""):
    return _f(id, label, "link", _lnk(h), supported_types=["EXTERNAL", "CONTENT", "BLOG", "EMAIL_ADDRESS"])


def _logo(id, label):
    return _f(id, label, "image", {"src": img(CONTENT["brand"]["logo"]), "alt": CONTENT["brand"]["logo_alt"],
              "loading": "eager", "width": CONTENT["brand"]["logo_w"], "height": CONTENT["brand"]["logo_h"]}, responsive=False)


def header_nav_defaults():
    out = []
    for n in CONTENT["nav"]:
        kids = []
        if n.get("mega"):
            for g in n["groups"]:
                kids.append({"sub_label": g["title"], "sub_to": _lnk(""), "sub_kind": "heading"})
                kids += [{"sub_label": a, "sub_to": _lnk(b), "sub_kind": "link"} for a, b in g["items"]]
        else:
            kids = [{"sub_label": a, "sub_to": _lnk(b), "sub_kind": "link"} for a, b in n.get("children", [])]
        out.append({"item_label": n["label"], "to": _lnk(n["href"]), "children": kids})
    return out


HEADER_HTML = """{#- VAF header. Navigation is a two-level repeater, edited once in the global content editor. -#}
{% set b = module %}
{% if b.show_topbar and b.topbar_text %}<div class="q-topbar"><a href="{{ b.topbar_url.url.href or '#' }}">{{ b.topbar_text }} <span class="q-topbar-arrow">&rarr;</span></a></div>{% endif %}
{% if b.util|length %}<div class="q-topbar" style="font-size:13px"><span>{% for u in b.util %}<a href="{{ u.util_to.url.href }}" style="margin:0 14px">{{ u.util_label }}</a>{% endfor %}</span>{% if b.phone %}<a href="tel:{{ b.phone|regex_replace('[^0-9+]','') }}" style="margin:0 14px"><b>{{ b.phone }}</b></a>{% endif %}</div>{% endif %}
<header class="q-header">
  <div class="q-container q-header-in">
    <a href="/" class="q-header-logo" aria-label="{{ b.company_name }} home">
      {% if b.logo.src %}<img src="{{ b.logo.src }}" alt="{{ b.logo.alt or b.company_name }}" height="44" loading="eager" style="height:44px;width:auto">{% else %}<span class="q-logo-text">{{ b.company_name }}</span>{% endif %}
    </a>
    <nav class="q-nav" aria-label="Main navigation">
      {% for n in b.nav %}
        {% if n.children|length %}
        <div class="q-nav-item">
          <a href="{{ n.to.url.href }}" aria-haspopup="true">{{ n.item_label }}<span class="q-caret" aria-hidden="true"></span></a>
          <div class="q-subnav">{% for c in n.children %}{% if c.sub_kind == 'heading' %}<span style="display:block;padding:10px 16px 2px;font-size:11px;letter-spacing:.12em;text-transform:uppercase;opacity:.65">{{ c.sub_label }}</span>{% else %}<a href="{{ c.sub_to.url.href }}">{{ c.sub_label }}</a>{% endif %}{% endfor %}</div>
        </div>
        {% else %}<a href="{{ n.to.url.href }}">{{ n.item_label }}</a>{% endif %}
      {% endfor %}
      {% if b.cta_label %}<a class="q-booknow" href="{{ b.cta.url.href }}">{{ b.cta_label }}</a>{% endif %}
    </nav>
    <details class="q-mnav">
      <summary aria-label="Open menu"><span></span><span></span><span></span></summary>
      <div class="q-mnav-panel">
        {% for n in b.nav %}
          {% if n.children|length %}
          <details class="q-msub"><summary>{{ n.item_label }}<span class="q-caret" aria-hidden="true"></span></summary>
            <div class="q-msub-links">{% for c in n.children %}{% if c.sub_kind == 'heading' %}<span style="display:block;padding:8px 0 2px;font-size:11px;letter-spacing:.12em;text-transform:uppercase;opacity:.65">{{ c.sub_label }}</span>{% else %}<a href="{{ c.sub_to.url.href }}">{{ c.sub_label }}</a>{% endif %}{% endfor %}</div>
          </details>
          {% else %}<a href="{{ n.to.url.href }}">{{ n.item_label }}</a>{% endif %}
        {% endfor %}
        {% if b.cta_label %}<a class="q-mnav-cta" href="{{ b.cta.url.href }}">{{ b.cta_label }}</a>{% endif %}
      </div>
    </details>
  </div>
</header>
"""

FOOTER_HTML = """{% set b = module %}
<footer class="q-footer">
  <div class="q-container q-footer-grid" style="grid-template-columns:1.4fr repeat({{ b.columns|length }},1fr)">
    <div>
      {% if b.logo.src %}<img src="{{ b.logo.src }}" alt="{{ b.logo.alt or b.company_name }}" height="40" loading="lazy" style="height:40px;width:auto">{% else %}<span class="q-logo-text">{{ b.company_name }}</span>{% endif %}
      {% if b.tagline %}<p class="q-footer-tag">{{ b.tagline }}</p>{% endif %}
      <p class="q-footer-contact">{% if b.phone %}<a class="q-footer-phone" href="tel:{{ b.phone|regex_replace('[^0-9+]','') }}">{{ b.phone }}</a>{% endif %}{% if b.phone and b.email %} &nbsp;·&nbsp; {% endif %}{% if b.email %}<a href="mailto:{{ b.email }}">{{ b.email }}</a>{% endif %}</p>
      <div class="q-footer-social">
        {% if b.facebook %}<a href="{{ b.facebook }}" aria-label="Facebook"><svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M22 12a10 10 0 1 0-11.6 9.9v-7H7.9V12h2.5V9.8c0-2.5 1.5-3.9 3.8-3.9 1.1 0 2.2.2 2.2.2v2.5h-1.2c-1.2 0-1.6.75-1.6 1.5V12h2.7l-.43 2.9h-2.3v7A10 10 0 0 0 22 12z"/></svg></a>{% endif %}
        {% if b.instagram %}<a href="{{ b.instagram }}" aria-label="Instagram"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg></a>{% endif %}
        {% if b.linkedin %}<a href="{{ b.linkedin }}" aria-label="LinkedIn"><svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.42v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.07 2.07 0 1 1 0-4.14 2.07 2.07 0 0 1 0 4.14zm1.78 13.02H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.73C24 .77 23.2 0 22.22 0z"/></svg></a>{% endif %}
      </div>
    </div>
    {% for col in b.columns %}
    <div><div class="q-footer-head">{{ col.col_title }}</div>
      <nav class="q-footer-links" aria-label="{{ col.col_title }}">{% for l in col.links %}<a href="{{ l.to.url.href }}">{{ l.link_label }}</a>{% endfor %}</nav></div>
    {% endfor %}
  </div>
  <div class="q-container q-footer-legal">
    Copyright &copy; {{ year }} {{ b.company_name }}{% for l in b.legal %} &nbsp;|&nbsp; <a href="{{ l.legal_to.url.href }}">{{ l.legal_label }}</a>{% endfor %}
  </div>
</footer>
"""


def cmd_chrome(_):
    B = CONTENT["brand"]
    nav = header_nav_defaults()
    hf = [
        _f("company_name", "Company name", "text", "Van Ausdall & Farrar, Inc."),
        _logo("logo", "Logo"),
        _f("nav", "Navigation", "group", nav, occurrence={"min": 1, "max": 9, "default": len(nav)}, children=[
            _f("item_label", "Label", "text", ""), _link("to", "Link (opens when the label is clicked)"),
            _f("children", "Drop-down items", "group", [], occurrence={"min": 0, "max": 30, "default": 0}, children=[
                _f("sub_label", "Label", "text", ""), _link("sub_to", "Link"),
                _f("sub_kind", "Kind", "choice", "link", display="select",
                   choices=[["link", "Link"], ["heading", "Small heading (no link)"]])])]),
        _f("cta_label", "Button text", "text", B["cta"]["label"]), _link("cta", "Button link", B["cta"]["href"]),
        _f("phone", "Phone number (utility bar)", "text", B["phone"]),
        _f("util", "Utility bar links", "group", [{"util_label": u["label"], "util_to": _lnk(u["href"])} for u in B["utility"]],
           occurrence={"min": 0, "max": 6, "default": len(B["utility"])},
           children=[_f("util_label", "Label", "text", ""), _link("util_to", "Link")]),
        _f("show_topbar", "Show announcement bar", "boolean", False),
        _f("topbar_text", "Announcement text", "text", ""), _link("topbar_url", "Announcement link"),
    ]
    ff = [
        _f("company_name", "Company name", "text", "Van Ausdall & Farrar, Inc."),
        _logo("logo", "Logo"),
        _f("tagline", "Tagline", "text", B["tagline"]),
        _f("phone", "Phone", "text", B["phone"]), _f("email", "Email", "text", B["email"]),
        _f("facebook", "Facebook URL", "text", B["social"].get("facebook", "")),
        _f("instagram", "Instagram URL", "text", B["social"].get("instagram", "")),
        _f("linkedin", "LinkedIn URL", "text", B["social"].get("linkedin", "")),
        _f("columns", "Link columns", "group", [
            {"col_title": c["title"], "links": [{"link_label": a, "to": _lnk(b)} for a, b in c["links"]]}
            for c in B["footer_columns"]], occurrence={"min": 1, "max": 6, "default": len(B["footer_columns"])}, children=[
            _f("col_title", "Column title", "text", ""),
            _f("links", "Links", "group", [], occurrence={"min": 0, "max": 20, "default": 0},
               children=[_f("link_label", "Label", "text", ""), _link("to", "Link")])]),
        _f("legal", "Legal links", "group", [{"legal_label": a, "legal_to": _lnk(b)} for a, b in B["legal"]],
           occurrence={"min": 0, "max": 6, "default": len(B["legal"])},
           children=[_f("legal_label", "Label", "text", ""), _link("legal_to", "Link")]),
    ]
    meta = lambda label: json.dumps({"label": label, "host_template_types": ["PAGE", "BLOG_POST", "BLOG_LISTING"],
                                     "is_available_for_new_content": False, "global": True, "content_types": ["LANDING_PAGE", "SITE_PAGE", "BLOG_LISTING", "BLOG_POST"]}, indent=2)
    for mod, fields, htm, label in (("quantum-site-header", hf, HEADER_HTML, "Site header (global)"),
                                    ("quantum-site-footer", ff, FOOTER_HTML, "Site footer (global)")):
        base = f"modules/{mod}.module/"
        # the module's nested fields need unique ids across the module
        put(base + "fields.json", json.dumps(fields, indent=2, ensure_ascii=False))
        put(base + "module.html", htm)
        put(base + "meta.json", meta(label))

# ------------------------------------------------------------------- commands
def put(path, content, env="published"):
    full = f"{THEME}/{path}"
    reskin.put_file(full, TOKEN, content, env)
    print(f"  put {env}: {full} ({len(content)} bytes)")


KNOWN_VALIDATOR_NOISE = ("Unmapped templates cannot contain drag and drop areas", "favicon_src has been deprecated")


def validate(path, content):
    """The validate endpoint reports every drag and drop area as 'unmapped' (the stock Quantum
    templates fail the same way) and flags a deprecated favicon property in base.html. Ignore
    exactly those two; anything else is a real error."""
    import subprocess, tempfile, urllib.parse
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as fh:
        fh.write(content)
    try:
        out = subprocess.run(["curl", "-s", "-X", "POST", "-H", "@-", "-F", f"file=@{fh.name};filename=x.html",
                              f"{reskin.API}/cms/v3/source-code/published/validate/" + urllib.parse.quote(path)],
                             input=f"Authorization: Bearer {TOKEN}\n".encode(), capture_output=True, timeout=120).stdout
    finally:
        os.unlink(fh.name)
    d = json.loads(out or b"{}")
    real = [e["message"] for e in d.get("errors", []) if not any(k in e["message"] for k in KNOWN_VALIDATOR_NOISE)]
    if real:
        raise SystemExit(f"template {path} failed validation:\n  " + "\n  ".join(m[:300] for m in real))


def cmd_templates(slugs):
    for sl in slugs:
        t, path = template_for(page_for("" if sl == "home" else sl))
        validate(f"{THEME}/{path}", t)
        put(path, t)


def cmd_pages(slugs):
    existing = {}
    after = None
    while True:
        r = reskin.get_json("/cms/v3/pages/site-pages?limit=100" + (f"&after={after}" if after else ""), TOKEN)
        for x in r.get("results", []):
            existing[x.get("slug", "")] = x
        after = (r.get("paging") or {}).get("next", {}).get("after")
        if not after:
            break
    for sl in slugs:
        sl = "" if sl == "home" else sl
        pg = page_for(sl)
        tpl = f"{THEME}/templates/vaf/{(sl.replace('/', '--') or 'home')}.html"
        body = {"name": f"VAF | {pg['title'].split(' | ')[0]}"[:120], "slug": sl or "home-preview", "templatePath": tpl,
                "htmlTitle": pg["title"], "metaDescription": pg.get("description", ""), "headHtml": NOINDEX,
                "language": "en", "pageExpiryEnabled": False}
        cur = existing.get(body["slug"])
        if cur:
            reskin._req("PATCH", f"/cms/v3/pages/site-pages/{cur['id']}", TOKEN, json.dumps(body).encode(), "application/json")
            pid = cur["id"]
        else:
            pid = json.loads(reskin._req("POST", "/cms/v3/pages/site-pages", TOKEN, json.dumps(body).encode(), "application/json"))["id"]
        # First publish must be scheduled: draft/push-live only updates a page that is already live.
        import datetime
        when = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=15)).strftime("%Y-%m-%dT%H:%M:%SZ")
        if cur and cur.get("state") != "DRAFT":
            reskin._req("POST", f"/cms/v3/pages/site-pages/{pid}/draft/push-live", TOKEN)
        else:
            reskin._req("POST", "/cms/v3/pages/site-pages/schedule", TOKEN, json.dumps({"id": pid, "publishDate": when}).encode(), "application/json")
        info = reskin.get_json(f"/cms/v3/pages/site-pages/{pid}", TOKEN)
        print(f"  page {pid}  /{body['slug']}  {info.get('state')}  {info.get('url')}")


def cmd_forms(_):
    """The stock {% form "form" %} tag renders nothing for a form id baked into a template default.
    Revolution's lead-form module uses the explicit form_to_use syntax, which does render."""
    base = os.path.join(ROOT, "themes/source/Quantum Showcase/modules")
    for mod in ("quantum-contact", "quantum-multistep-form"):
        h = open(f"{base}/{mod}.module/module.html", encoding="utf-8").read()
        h2 = h.replace('{% form "form" %}',
                       '{% if module.form.form_id %}{% form form_to_use="{{ module.form.form_id }}", no_title=True, '
                       'response_response_type="{{ module.form.response_type|default(\'inline\') }}", '
                       'response_message="{{ module.form.message }}" %}{% endif %}')
        if h2 == h:
            print("  no form tag in", mod); continue
        put(f"modules/{mod}.module/module.html", h2)
        # form-type fields ignore module_attribute, so the default lives in the module itself
        fields = json.load(open(f"{base}/{mod}.module/fields.json", encoding="utf-8"))
        for f in fields:
            if f["name"] == "form":
                f["default"] = {"form_id": FORM_ID, "response_type": "inline",
                                "message": "Thank you. A person from the Indianapolis office will reply to set a time."}
        put(f"modules/{mod}.module/fields.json", json.dumps(fields, indent=2, ensure_ascii=False))


def cmd_base(_):
    """Use the current favicon property in the cloned base layout."""
    src = open(os.path.join(ROOT, "themes/source/Quantum Showcase/templates/layouts/base.html"), encoding="utf-8").read()
    put("templates/layouts/base.html", src.replace("site_settings.favicon_src", "brand_settings.favicon.src"))


def main(argv):
    if not TOKEN:
        raise SystemExit("CLIENT_HUBSPOT_TOKEN not set")
    reskin.verify_portal(TOKEN, PORTAL)
    cmd, rest = argv[0], argv[1:]
    {"templates": cmd_templates, "chrome": cmd_chrome, "base": cmd_base, "forms": cmd_forms, "pages": cmd_pages}[cmd](rest)


if __name__ == "__main__":
    main(sys.argv[1:])
