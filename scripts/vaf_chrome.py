#!/usr/bin/env python3
"""Generate the VAF header, footer and quick-action modules, the base layout and the partials
into themes/vaf/ (committed output), with defaults taken from brands/vanausdall.content.json."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from vaf_common import ROOT, A, href, link, image

C = json.load(open(os.path.join(ROOT, "brands/vanausdall.content.json"), encoding="utf-8"))
B = C["brand"]
OUT = os.path.join(ROOT, "themes/vaf")
HOST = ["PAGE"]


def f(id, label, type, default=None, **kw):
    d = {"id": id, "name": id, "label": label, "type": type}
    if default is not None:
        d["default"] = default
    d.update(kw)
    return d


def lk(id, label, h=""):
    return f(id, label, "link", link(h), supported_types=["EXTERNAL", "CONTENT", "BLOG", "EMAIL_ADDRESS"])


def group(id, label, children, default, mn=0, mx=30):
    return f(id, label, "group", default, children=children, occurrence={"min": mn, "max": mx, "default": len(default)})


def logo(id):
    return f(id, "Logo", "image", {"src": A(B["logo"]), "alt": B["logo_alt"], "loading": "eager",
                                    "width": B["logo_w"], "height": B["logo_h"]}, responsive=False)


def write(rel, text):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(text)


def module(name, label, fields, html, css="", js=""):
    base = f"modules/{name}.module/"
    write(base + "fields.json", json.dumps(fields, indent=2, ensure_ascii=False))
    write(base + "meta.json", json.dumps({"label": label, "host_template_types": HOST, "is_available_for_new_content": False,
                                          "global": True, "content_types": ["SITE_PAGE", "LANDING_PAGE", "BLOG_LISTING", "BLOG_POST"]}, indent=2))
    write(base + "module.html", html)
    if css:
        write(base + "module.css", css)
    if js:
        write(base + "module.js", js)


# ------------------------------------------------------------------ header
def nav_default():
    out = []
    for n in C["nav"]:
        kids = []
        if n.get("mega"):
            for g in n["groups"]:
                kids.append({"sub_label": g["title"], "sub_to": link(""), "sub_kind": "heading"})
                kids += [{"sub_label": a, "sub_to": link(b), "sub_kind": "link"} for a, b in g["items"]]
            ft = n.get("featured") or {}
            out.append({"item_label": n["label"], "to": link(n["href"]), "mega": True,
                        "feat_eyebrow": ft.get("eyebrow", ""), "feat_title": ft.get("title", ""), "feat_copy": ft.get("body", ""),
                        "feat_cta": ft.get("label", ""), "feat_to": link(ft.get("href", "")), "foot_label": "All solutions",
                        "children": kids})
        else:
            kids = [{"sub_label": a, "sub_to": link(b), "sub_kind": "link"} for a, b in n.get("children", [])]
            out.append({"item_label": n["label"], "to": link(n["href"]), "mega": False, "feat_eyebrow": "", "feat_title": "",
                        "feat_copy": "", "feat_cta": "", "feat_to": link(""), "foot_label": "", "children": kids})
    return out


HEADER = """{#- VAF header: utility bar, logo, two-level navigation with a mega menu, primary button, mobile drawer. All fields. -#}
{% set b = module %}
<header class="q-header">
<a class="q-skip" href="#q-content">Skip to content</a>
{% if b.util|length or b.phone %}<div class="pv-util"><div class="q-container">{% for u in b.util %}<a href="{{ u.util_to.url.href }}">{{ u.util_label }}</a>{% endfor %}{% if b.phone %}<a class="pv-phone" href="tel:{{ b.phone|regex_replace('[^0-9+]','') }}">{{ b.phone }}</a>{% endif %}</div></div>{% endif %}
<div class="q-container q-header-in">
<a href="/" class="q-header-logo" aria-label="{{ b.company_name }} home"><img src="{{ b.logo.src }}" alt="{{ b.logo.alt or b.company_name }}" width="202" height="40" loading="eager"></a>
<nav class="q-nav" aria-label="Main navigation">
{% for n in b.nav %}{% if n.children|length %}
<div class="q-nav-item{% if n.mega %} pv-has-mega{% endif %}">
<a href="{{ n.to.url.href }}" aria-haspopup="true">{{ n.item_label }}<span class="q-caret" aria-hidden="true"></span></a>
{% if n.mega %}
<div class="q-subnav pv-mega"><div class="pv-mega-in">
{% for c in n.children %}{% if c.sub_kind == 'heading' %}{% if not loop.first %}</div>{% endif %}<div class="col"><div class="gt">{{ c.sub_label }}</div>{% else %}<a href="{{ c.sub_to.url.href }}">{{ c.sub_label }}</a>{% endif %}{% if loop.last %}</div>{% endif %}{% endfor %}
{% if n.feat_title %}<a class="feat" href="{{ n.feat_to.url.href }}"><span class="q-eyebrow">{{ n.feat_eyebrow }}</span><b>{{ n.feat_title }}</b><p>{{ n.feat_copy }}</p><span class="more">{{ n.feat_cta }}</span></a>{% endif %}
</div>{% if n.foot_label %}<div class="pv-mega-foot"><a href="{{ n.to.url.href }}">{{ n.foot_label }}</a></div>{% endif %}</div>
{% else %}
<div class="q-subnav">{% for c in n.children %}<a href="{{ c.sub_to.url.href }}">{{ c.sub_label }}</a>{% endfor %}</div>
{% endif %}
</div>
{% else %}<a href="{{ n.to.url.href }}">{{ n.item_label }}</a>{% endif %}{% endfor %}
{% if b.cta_label %}<a class="q-booknow" href="{{ b.cta.url.href }}">{{ b.cta_label }}</a>{% endif %}
</nav>
<details class="q-mnav">
<summary aria-label="Open menu"><span></span><span></span><span></span></summary>
<div class="q-mnav-panel">
{% for n in b.nav %}{% if n.children|length %}
<details class="q-msub"><summary>{{ n.item_label }}<span class="q-caret" aria-hidden="true"></span></summary>
<div class="q-msub-links">{% for c in n.children %}{% if c.sub_kind == 'heading' %}<div class="pv-mgt">{{ c.sub_label }}</div>{% else %}<a href="{{ c.sub_to.url.href }}">{{ c.sub_label }}</a>{% endif %}{% endfor %}{% if n.mega and n.foot_label %}<a href="{{ n.to.url.href }}" class="pv-mall">{{ n.foot_label }}</a>{% endif %}</div></details>
{% else %}<a href="{{ n.to.url.href }}">{{ n.item_label }}</a>{% endif %}{% endfor %}
{% if b.cta_label %}<a class="q-mnav-cta" href="{{ b.cta.url.href }}">{{ b.cta_label }}</a>{% endif %}
</div>
</details>
</div>
</header>
"""


def gen_header():
    nav = nav_default()
    fields = [
        f("company_name", "Company name", "text", "Van Ausdall & Farrar, Inc."), logo("logo"),
        group("util", "Utility bar links", [f("util_label", "Label", "text", ""), lk("util_to", "Link")],
              [{"util_label": u["label"], "util_to": link(u["href"])} for u in B["utility"]], 0, 6),
        f("phone", "Phone number (utility bar)", "text", B["phone"]),
        group("nav", "Navigation", [
            f("item_label", "Label", "text", ""), lk("to", "Link (the label itself)"),
            f("mega", "Open as a wide mega menu (heading rows become columns)", "boolean", False),
            f("feat_eyebrow", "Mega menu feature card: eyebrow", "text", ""), f("feat_title", "Feature card: title", "text", ""),
            f("feat_copy", "Feature card: text", "text", ""), f("feat_cta", "Feature card: link text", "text", ""),
            lk("feat_to", "Feature card: link"), f("foot_label", "Mega menu footer link text", "text", ""),
            group("children", "Drop-down items", [
                f("sub_label", "Label", "text", ""), lk("sub_to", "Link"),
                f("sub_kind", "Kind", "choice", "link", display="select", choices=[["link", "Link"], ["heading", "Column heading (no link)"]])],
                [], 0, 40)], nav, 1, 9),
        f("cta_label", "Button text", "text", B["cta"]["label"]), lk("cta", "Button link", B["cta"]["href"]),
    ]
    module("vaf-header", "VAF header (global)", fields, HEADER)


# ------------------------------------------------------------------ footer + quick actions
FOOTER = """{% set b = module %}
<footer class="q-footer">
<div class="q-container q-footer-grid pv-fcols-4">
<div><img src="{{ b.logo.src }}" alt="{{ b.logo.alt or b.company_name }}" width="182" height="36" loading="lazy"><p class="q-footer-tag">{{ b.tagline }}</p>
<p class="q-footer-contact">{% if b.phone %}<a class="q-footer-phone" href="tel:{{ b.phone|regex_replace('[^0-9+]','') }}">{{ b.phone }}</a>{% endif %}{% if b.email %}<br><a href="mailto:{{ b.email }}">{{ b.email }}</a>{% endif %}</p>
<div class="q-footer-social vaf-social">{% for s in b.social %}{% set k = s.social_label|lower %}<a href="{{ s.social_to.url.href }}" aria-label="{{ s.social_label }}" rel="noopener" target="_blank">{% if 'linkedin' in k %}<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.42v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.07 2.07 0 1 1 0-4.14 2.07 2.07 0 0 1 0 4.14zm1.78 13.02H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.73C24 .77 23.2 0 22.22 0z"/></svg>{% elif 'facebook' in k %}<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M22 12a10 10 0 1 0-11.6 9.9v-7H7.9V12h2.5V9.8c0-2.5 1.5-3.9 3.8-3.9 1.1 0 2.2.2 2.2.2v2.5h-1.2c-1.2 0-1.6.75-1.6 1.5V12h2.7l-.43 2.9h-2.3v7A10 10 0 0 0 22 12z"/></svg>{% elif 'instagram' in k %}<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg>{% elif 'youtube' in k %}<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M23 7.2a3 3 0 0 0-2.1-2.1C19 4.6 12 4.6 12 4.6s-7 0-8.9.5A3 3 0 0 0 1 7.2C.5 9 .5 12 .5 12s0 3 .5 4.8a3 3 0 0 0 2.1 2.1c1.9.5 8.9.5 8.9.5s7 0 8.9-.5a3 3 0 0 0 2.1-2.1c.5-1.8.5-4.8.5-4.8s0-3-.5-4.8zM9.7 15.5v-7l6 3.5-6 3.5z"/></svg>{% else %}{{ s.social_label }}{% endif %}</a>{% endfor %}</div></div>
{% for col in b.columns %}<div{% if col.wide %} class="pv-fwide"{% endif %}><div class="q-footer-head">{{ col.col_title }}</div>
<nav class="q-footer-links{% if col.wide %} pv-two{% endif %}" aria-label="{{ col.col_title }}">{% for l in col.links %}<a href="{{ l.to.url.href }}">{{ l.link_label }}</a>{% endfor %}</nav></div>{% endfor %}
</div>
<div class="q-container q-footer-legal"><span class="pv-legal-item">Copyright &copy; {{ year }} {{ b.company_name }}</span>{% for l in b.legal %}<span class="pv-legal-item"><a href="{{ l.legal_to.url.href }}">{{ l.legal_label }}</a></span>{% endfor %}</div>
</footer>
"""

QUICK = """{% set b = module %}
<nav class="pv-sticky" aria-label="Quick actions"><a class="a" href="{{ b.primary.url.href }}">{{ b.primary_label }}</a><a class="b" href="{{ b.secondary.url.href }}">{{ b.secondary_label }}</a></nav>
{% if b.drawer_links|length %}<div class="pv-sl">
<button type="button" aria-expanded="false" aria-controls="pv-sl-d"><i aria-hidden="true"></i>{{ b.launcher_label }}</button>
<div class="drawer" id="pv-sl-d" hidden>
<div class="k">{{ b.drawer_eyebrow }}</div><h3>{{ b.drawer_title }}</h3>
<div class="grid">{% for l in b.drawer_links %}<a href="{{ l.dl_to.url.href }}">{{ l.dl_label }}</a>{% endfor %}<a class="call" href="{{ b.secondary.url.href }}">Call {{ b.drawer_phone }}</a></div>
<p>{{ b.drawer_note }}</p></div></div>{% endif %}
"""


def gen_footer():
    soc = [{"social_label": k.capitalize() if k != "linkedin" else "LinkedIn", "social_to": link(v)} for k, v in B["social"].items()]
    cols = [{"col_title": c["title"], "wide": c["title"] == "Solutions",
             "links": [{"link_label": a, "to": link(b)} for a, b in c["links"]]} for c in B["footer_columns"]]
    fields = [
        f("company_name", "Company name", "text", "Van Ausdall & Farrar, Inc."), logo("logo"),
        f("tagline", "Tagline", "text", B["tagline"]), f("phone", "Phone", "text", B["phone"]), f("email", "Email", "text", B["email"]),
        group("social", "Social links", [f("social_label", "Label", "text", ""), lk("social_to", "Link")], soc, 0, 8),
        group("columns", "Link columns", [
            f("col_title", "Column title", "text", ""), f("wide", "Wide column (two link columns)", "boolean", False),
            group("links", "Links", [f("link_label", "Label", "text", ""), lk("to", "Link")], [], 0, 24)], cols, 1, 6),
        group("legal", "Legal links", [f("legal_label", "Label", "text", ""), lk("legal_to", "Link")],
              [{"legal_label": a, "legal_to": link(b)} for a, b in B["legal"]], 0, 6),
    ]
    module("vaf-footer", "VAF footer (global)", fields, FOOTER)
    L, S = B["launcher"], B["sticky"]
    q = [
        f("primary_label", "Bar button 1", "text", S["primary"]), lk("primary", "Bar button 1 link", S["primary_href"]),
        f("secondary_label", "Bar button 2", "text", S["secondary"]), lk("secondary", "Bar button 2 link (phone)", S["secondary_href"]),
        f("launcher_label", "Support launcher text", "text", L["label"]), f("drawer_eyebrow", "Drawer eyebrow", "text", L["eyebrow"]),
        f("drawer_title", "Drawer title", "text", L["title"]),
        group("drawer_links", "Drawer links", [f("dl_label", "Label", "text", ""), lk("dl_to", "Link")],
              [{"dl_label": a, "dl_to": link(b)} for a, b in L["links"]], 0, 8),
        f("drawer_phone", "Drawer phone", "text", B["phone"]), f("drawer_note", "Drawer note", "text", L["note"]),
    ]
    module("vaf-quickbar", "VAF quick actions and support drawer (global)", q, QUICK)


# ------------------------------------------------------------------ layout + partials
LAYOUT = """<!--
  templateType: none
  isAvailableForNewContent: false
-->
<!doctype html>
<html lang="{{ html_lang }}" {{ html_lang_dir }}>
<head>
  <meta charset="utf-8">
  <title>{{ page_meta.html_title }}</title>
  <meta name="description" content="{{ page_meta.meta_description }}">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  {% if brand_settings.favicon.src %}<link rel="shortcut icon" href="{{ brand_settings.favicon.src }}">{% endif %}
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700;800&family=Inter:wght@400;500;600;700&display=swap">
  {{ require_css(get_asset_url('../../css/vaf.css')) }}
  {{ require_js(get_asset_url('../../js/vaf.js'), 'footer') }}
  {% block head_extra %}{% endblock %}
  {{ standard_header_includes }}
</head>
<body class="{{ builtin_body_classes }}" data-qdir="showcase">
  <div class="body-wrapper">
    {% block header %}{% global_partial path='../partials/vaf-header.html' %}{% endblock %}
    <div id="q-content" tabindex="-1">{% block body %}{% endblock %}</div>
    {% block footer %}{% global_partial path='../partials/vaf-footer.html' %}{% endblock %}
  </div>
  {{ standard_footer_includes }}
</body>
</html>
"""


def gen_layout():
    write("templates/layouts/vaf-base.html", LAYOUT)
    hdr = "<!--\n  templateType: global_partial\n  label: VAF Header\n  isAvailableForNewContent: false\n-->\n"
    write("templates/partials/vaf-header.html", hdr + '{% module "quantum_org_schema" path="../../modules/quantum-org-schema" %}\n{% module "vaf_header" path="../../modules/vaf-header" %}\n')
    ftr = hdr.replace("VAF Header", "VAF Footer")
    write("templates/partials/vaf-footer.html", ftr + '{% module "vaf_footer" path="../../modules/vaf-footer" %}\n{% module "vaf_quickbar" path="../../modules/vaf-quickbar" %}\n')


if __name__ == "__main__":
    gen_header(); gen_footer(); gen_layout()
    print("chrome written to themes/vaf")
