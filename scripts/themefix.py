#!/usr/bin/env python3
"""Bring the nine Quantum themes to the reference implementation, at source.

themes/architecture.md lists five changes proven on the Revolution build. This applies
them to the exported theme source under themes/source/ -- locally, as a diff you can
read -- and then `reskin.py upload` pushes the changed files to portal 20682069.

    python3 scripts/themefix.py --theme "Quantum Clean"        # patch one, locally
    python3 scripts/themefix.py --all --write-manifest m.json  # all nine + upload manifest

What it does, per theme:

  1. Accent split.  --accent-ink (accent text on the ground, darkened to 4.5:1) and
     --accent-lift join the native block; every `color:var(--q-gold)` (the property
     `color`, not `border-color`) becomes `color:var(--accent-ink)`. Fills and borders
     keep --q-gold. On dark themes the ink resolves to the same gold, so nothing moves;
     on the five light themes accent text finally passes WCAG AA. --cta-fg is recomputed
     to whichever of near-black / near-white clears 4.5 on the accent.
  2. Geometry tokens.  --maxw --sec-y --radius --hero-size --display-2, wired into
     .q-container .q-section .q-card .q-h1 .q-h2, distinct per direction.
  3. Header/footer as MODULES (eight themes).  HubSpot theme fields.json only accepts
     boolean/choice/color/font/number/spacing -- not text, image or menu -- so the brand
     fields live in modules/quantum-site-header.module and quantum-site-footer.module,
     and the global partials just include them. Their content is edited once in the
     global content editor. Defaults are QBS's current values, so an un-touched theme
     renders exactly as today. Quantum Void keeps its own header/footer: it is QBS's live
     theme with QBS-specific menu logic; clients clone from the other eight.
  4. Fail-safe Organization schema as a module (eight themes).  modules/quantum-org-schema
     emits Organization + WebSite on the home page and BreadcrumbList elsewhere, from its
     own fields. org_name empty (the default) = no block. Absent markup is safe, wrong
     markup is not. Void keeps its richer hardcoded QBS block untouched.
  5. Skip link + a focusable content landmark.  <a class="q-skip" href="#q-content"> and
     <div id="q-content" tabindex="-1"> around the body block, so it works on every
     template including the four that have no <main>. Templates with <main> also get
     id="main".

Nothing here touches the portal. Read the diff (`git diff themes/source`), then upload.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reskin  # noqa: E402  (contrast helpers, NINE, SOURCE_DIR)

SRC = reskin.SOURCE_DIR
LIVE_QBS_THEME = "Quantum Void"

# Distinct geometry per direction. Values are px. Void keeps today's numbers exactly.
GEOMETRY = {
    "Quantum Flagship":  dict(maxw=1240, sec_y=120, radius=6,  hero=84, d2=52),
    "Quantum Void":      dict(maxw=1240, sec_y=110, radius=8,  hero=82, d2=50),
    "Quantum Signal":    dict(maxw=1240, sec_y=100, radius=12, hero=80, d2=48),
    "Quantum Converter": dict(maxw=1240, sec_y=96,  radius=6,  hero=76, d2=46),
    "Quantum Clean":     dict(maxw=1240, sec_y=96,  radius=10, hero=76, d2=46),
    "Quantum Press":     dict(maxw=1120, sec_y=120, radius=2,  hero=72, d2=48),
    "Quantum Paper":     dict(maxw=1040, sec_y=104, radius=4,  hero=68, d2=44),
    "Quantum Journal":   dict(maxw=1080, sec_y=96,  radius=2,  hero=64, d2=42),
    "Quantum Showcase":  dict(maxw=1320, sec_y=110, radius=16, hero=88, d2=54),
}

# QBS's current identity, verbatim from the live partials: the module DEFAULTS on the eight.
QBS_BRAND = {
    "company_name": "Quantum Business Solutions",
    "logo_dark": "https://www.thequantumleap.business/hubfs/quantum_new.png",
    "logo_light": "https://20682069.fs1.hubspotusercontent-na1.net/hubfs/20682069/quantum-theme/brand/quantum-light.png",
    "tagline": "Quickly understand your business and what technology you are using.",
    "header_menu": 184144186499,
    "cta_label": "Book Now",
    "cta_url": "https://meetings.hubspot.com/shawn-peterson",
    "show_topbar": False,
    "topbar_text": "Are AI engines citing your company? Get your free AEO score",
    "topbar_url": "/en/aeo-health-check",
    "facebook": "https://www.facebook.com/profile.php?id=100075560065925",
    "instagram": "https://www.instagram.com/the.quantum.leap/",
    "linkedin": "https://www.linkedin.com/company/quantum-business-solutions",
    "x": "",
    "phone": "",
    "email": "",
    "privacy_url": "/privacy-policy",
    "terms_url": "",
}

CONTENT_TYPES = ["LANDING_PAGE", "SITE_PAGE", "BLOG_LISTING", "BLOG_POST"]
HOST_TYPES = ["PAGE", "BLOG_POST", "BLOG_LISTING"]


# ------------------------------------------------------------------ module field defs

def _f(id_, label, type_="text", default="", **extra):
    d = {"id": id_, "name": id_, "label": label, "type": type_, "default": default,
         "required": False, "locked": False}
    d.update(extra)
    return d


def _img(src, alt):
    return {"src": src, "alt": alt if src else "", "loading": "disabled"} if src else {"src": "", "alt": "", "loading": "disabled"}


def _link(href):
    return {"url": {"href": href, "type": "EXTERNAL" if href.startswith("http") else "CONTENT"} if href else {"href": "", "type": "EXTERNAL"},
            "open_in_new_tab": False, "no_follow": False}


def header_fields(d: dict) -> list:
    return [
        _f("company_name", "Company name", default=d["company_name"]),
        _f("logo_dark", "Logo for dark ground", "image", default=_img(d["logo_dark"], d["company_name"]),
           responsive=False, resizable=False, show_loading=False),
        _f("logo_light", "Logo for light ground", "image", default=_img(d["logo_light"], d["company_name"]),
           responsive=False, resizable=False, show_loading=False),
        _f("header_menu", "Navigation menu", "menu", default=d["header_menu"]),
        _f("cta_label", "CTA button label", default=d["cta_label"]),
        _f("cta_url", "CTA button URL (blank hides the button)", default=d["cta_url"]),
        _f("show_topbar", "Show announcement bar", "boolean", default=d["show_topbar"], display="toggle"),
        _f("topbar_text", "Announcement text", default=d["topbar_text"]),
        _f("topbar_url", "Announcement URL", default=d["topbar_url"]),
    ]


def footer_fields(d: dict) -> list:
    return [
        _f("company_name", "Company name", default=d["company_name"]),
        _f("logo_dark", "Logo for dark ground", "image", default=_img(d["logo_dark"], d["company_name"]),
           responsive=False, resizable=False, show_loading=False),
        _f("logo_light", "Logo for light ground", "image", default=_img(d["logo_light"], d["company_name"]),
           responsive=False, resizable=False, show_loading=False),
        _f("tagline", "Tagline", default=d["tagline"]),
        _f("phone", "Phone (blank hides)", default=d["phone"]),
        _f("email", "Email (blank hides)", default=d["email"]),
        _f("facebook", "Facebook URL", default=d["facebook"]),
        _f("instagram", "Instagram URL", default=d["instagram"]),
        _f("linkedin", "LinkedIn company URL", default=d["linkedin"]),
        _f("x", "X URL", default=d["x"]),
        _f("show_menu_1", "Show link column 1", "boolean", default=False, display="toggle"),
        _f("menu_1_title", "Column 1 title", default="Solutions"),
        _f("menu_1", "Column 1 menu", "menu", default=None),
        _f("show_menu_2", "Show link column 2", "boolean", default=False, display="toggle"),
        _f("menu_2_title", "Column 2 title", default="Resources"),
        _f("menu_2", "Column 2 menu", "menu", default=None),
        _f("privacy_url", "Privacy policy URL", default=d["privacy_url"]),
        _f("terms_url", "Terms URL (blank hides)", default=d["terms_url"]),
    ]


def schema_fields() -> list:
    # All empty by default: a theme that nobody configured emits NO Organization block.
    return [
        _f("org_name", "Organization legal name (empty = no schema emitted)", default=""),
        _f("org_alt_name", "Short / alternate name", default=""),
        _f("org_url", "Canonical URL (https://…, no trailing slash)", default=""),
        _f("org_description", "One-line description", default=""),
        _f("org_logo", "Logo (≥112px)", "image", default=_img("", ""), responsive=False, resizable=False, show_loading=False),
        _f("org_sameas", "sameAs profile URL (LinkedIn company page first)", default="",
           occurrence={"min": 0, "max": 12, "default": 1}),
        _f("contact_email", "Sales contact email (optional)", default=""),
        _f("contact_phone", "Sales phone, E.164 e.g. +1-800-345-3559 (optional)", default=""),
        _f("founder_name", "Founder name (optional)", default=""),
        _f("founder_title", "Founder title", default=""),
        _f("founder_url", "Founder page URL", default=""),
        _f("founder_sameas", "Founder LinkedIn", default=""),
        _f("knows_about", "knowsAbout, comma-separated", default=""),
        _f("search_path", "Site search path for a WebSite SearchAction (blank = none)", default=""),
    ]


def meta(label: str) -> dict:
    return {"global": False, "content_types": CONTENT_TYPES, "host_template_types": HOST_TYPES,
            "label": label, "is_available_for_new_content": False}


# ------------------------------------------------------------------------- templates

HEADER_MODULE = r'''{#- Quantum site header. Every visible value is a module field, edited once in the
    global content editor. reskin.py sets the defaults for a client clone. -#}
{% set b = module %}
{% if b.show_topbar and b.topbar_text %}
<div class="q-topbar">
  <a href="{{ b.topbar_url or '#' }}">{{ b.topbar_text }} <span class="q-topbar-arrow">&rarr;</span></a>
</div>
{% endif %}
<header class="q-header">
  <div class="q-container q-header-in">
    <a href="/" class="q-header-logo" aria-label="{{ b.company_name }} home">
      {% if b.logo_dark.src or b.logo_light.src %}
        <img class="only-dark" src="{{ b.logo_dark.src or b.logo_light.src }}" alt="{{ b.company_name }}" height="40" loading="eager">
        <img class="only-light" src="{{ b.logo_light.src or b.logo_dark.src }}" alt="{{ b.company_name }}" height="40" loading="eager">
      {% else %}
        <span class="q-logo-text">{{ b.company_name }}</span>
      {% endif %}
    </a>
    <nav class="q-nav" aria-label="Main navigation">
      {% if b.header_menu %}
      {% set main_nav = menu(b.header_menu) %}
      {% for item in main_nav.children %}
        {% if item.children %}
          <div class="q-nav-item">
            <a href="{{ item.url or '#' }}" aria-haspopup="true">{{ item.label }}<span class="q-caret" aria-hidden="true"></span></a>
            <div class="q-subnav">
              {% for sub in item.children %}<a href="{{ sub.url }}">{{ sub.label }}</a>{% endfor %}
            </div>
          </div>
        {% else %}
          <a href="{{ item.url }}">{{ item.label }}</a>
        {% endif %}
      {% endfor %}
      {% endif %}
      {% if b.cta_url %}<a class="q-booknow" href="{{ b.cta_url }}">{{ b.cta_label or 'Contact' }}</a>{% endif %}
    </nav>
    <details class="q-mnav">
      <summary aria-label="Open menu"><span></span><span></span><span></span></summary>
      <div class="q-mnav-panel">
        {% if b.header_menu %}
        {% set m_nav = menu(b.header_menu) %}
        {% for item in m_nav.children %}
          {% if item.children %}
            <details class="q-msub">
              <summary>{{ item.label }}<span class="q-caret" aria-hidden="true"></span></summary>
              <div class="q-msub-links">
                {% for sub in item.children %}<a href="{{ sub.url }}">{{ sub.label }}</a>{% endfor %}
              </div>
            </details>
          {% else %}
            <a href="{{ item.url }}">{{ item.label }}</a>
          {% endif %}
        {% endfor %}
        {% endif %}
        {% if b.cta_url %}<a class="q-mnav-cta" href="{{ b.cta_url }}">{{ b.cta_label or 'Contact' }}</a>{% endif %}
      </div>
    </details>
  </div>
</header>
'''

HEADER_CSS = r'''.q-topbar{background:linear-gradient(90deg,rgba(196,164,74,.12),rgba(196,164,74,.04));border-bottom:1px solid rgba(196,164,74,.18);text-align:center;padding:9px 16px;font-size:13.5px;}
.q-topbar a{color:var(--fg);text-decoration:none;letter-spacing:.01em;}
.q-topbar a:hover{text-decoration:underline;}
.q-topbar-arrow{color:var(--accent-ink);}
.q-header{border-bottom:1px solid var(--border);background:var(--bg);position:sticky;top:0;z-index:50;}
.q-header-in{height:80px;display:flex;align-items:center;justify-content:space-between;gap:32px;}
.q-header-logo{display:flex;align-items:center;flex:0 0 auto;text-decoration:none;}
.q-header-logo img{height:40px;width:auto;}
.q-logo-text{font-family:var(--q-serif);font-size:22px;font-weight:600;color:var(--fg);letter-spacing:-0.01em;}
.q-nav{display:flex;align-items:center;gap:28px;font-size:14.5px;font-weight:500;}
.q-nav > a, .q-nav-item > a{color:var(--fg);text-decoration:none;display:inline-flex;align-items:center;gap:6px;padding:28px 0;}
.q-nav > a:hover, .q-nav-item > a:hover{color:var(--accent-ink);}
.q-nav-item{position:relative;}
.q-nav-item .q-caret{width:8px;height:8px;border-right:1.5px solid currentColor;border-bottom:1.5px solid currentColor;transform:rotate(45deg) translateY(-2px);}
.q-subnav{visibility:hidden;opacity:0;transition:opacity .18s ease,transform .18s ease;transform:translate(-50%,6px);position:absolute;top:100%;left:50%;min-width:250px;background:var(--bg);border:1px solid var(--border);border-radius:var(--radius);padding:8px 0;box-shadow:0 14px 40px rgba(0,0,0,0.18);z-index:60;}
.q-nav-item:hover .q-subnav, .q-nav-item:focus-within .q-subnav{visibility:visible;opacity:1;transform:translate(-50%,0);}
.q-subnav a{display:block;padding:9px 22px;color:var(--fg);text-decoration:none;font-size:14px;white-space:nowrap;}
.q-subnav a:hover{color:var(--accent-ink);background:var(--bg-alt);}
.q-booknow{border:1px solid var(--q-gold);color:var(--accent-ink)!important;padding:11px 26px!important;border-radius:999px;font-weight:600;letter-spacing:0.01em;}
.q-booknow:hover{background:var(--q-gold);color:var(--cta-fg)!important;}
.q-mnav{display:none;}
@media(max-width:1024px){
  .q-nav{display:none;}
  .q-mnav{display:block;}
  .q-mnav > summary{list-style:none;cursor:pointer;width:46px;height:46px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:5px;border:1px solid var(--border);border-radius:10px;}
  .q-mnav > summary::-webkit-details-marker{display:none;}
  .q-mnav > summary span{display:block;width:20px;height:2px;background:var(--accent-ink);border-radius:2px;transition:transform .2s ease,opacity .2s ease;}
  .q-mnav[open] > summary span:nth-child(1){transform:translateY(7px) rotate(45deg);}
  .q-mnav[open] > summary span:nth-child(2){opacity:0;}
  .q-mnav[open] > summary span:nth-child(3){transform:translateY(-7px) rotate(-45deg);}
  .q-mnav-panel{position:absolute;top:100%;left:0;right:0;max-height:calc(100vh - 80px);overflow:auto;-webkit-overflow-scrolling:touch;background:var(--bg);border-top:1px solid var(--border);box-shadow:0 30px 60px rgba(0,0,0,.25);padding:10px 22px 34px;z-index:70;}
  .q-mnav-panel > a, .q-msub > summary{display:flex;align-items:center;justify-content:space-between;padding:15px 2px;color:var(--fg);text-decoration:none;font-size:16px;font-weight:500;border-bottom:1px solid var(--border);min-height:44px;box-sizing:border-box;}
  .q-msub{border-bottom:1px solid var(--border);}
  .q-msub > summary{border-bottom:none;list-style:none;cursor:pointer;}
  .q-msub > summary::-webkit-details-marker{display:none;}
  .q-msub .q-caret{width:8px;height:8px;border-right:1.5px solid var(--accent-ink);border-bottom:1.5px solid var(--accent-ink);transform:rotate(45deg);transition:transform .18s ease;}
  .q-msub[open] > summary .q-caret{transform:rotate(-135deg);}
  .q-msub-links{padding:2px 0 12px;}
  .q-msub-links a{display:block;padding:12px 14px;color:var(--fg-muted);text-decoration:none;font-size:15px;min-height:44px;box-sizing:border-box;}
  .q-msub-links a:active, .q-msub-links a:hover{color:var(--accent-ink);}
  .q-mnav-cta{display:block;text-align:center;margin-top:22px;border:1px solid var(--q-gold);color:var(--accent-ink);padding:13px 26px;border-radius:999px;font-weight:600;text-decoration:none;font-size:16px;}
  .q-mnav-panel > a.q-mnav-cta{justify-content:center;border-bottom:none;}
}
'''

FOOTER_MODULE = r'''{% set b = module %}
<footer class="q-footer">
  <div class="q-container q-footer-grid">
    <div>
      {% if b.logo_dark.src or b.logo_light.src %}
        <img class="only-dark" src="{{ b.logo_dark.src or b.logo_light.src }}" alt="{{ b.company_name }}" height="38" loading="lazy">
        <img class="only-light" src="{{ b.logo_light.src or b.logo_dark.src }}" alt="{{ b.company_name }}" height="38" loading="lazy">
      {% else %}
        <span class="q-logo-text">{{ b.company_name }}</span>
      {% endif %}
      {% if b.tagline %}<p class="q-footer-tag">{{ b.tagline }}</p>{% endif %}
      {% if b.phone or b.email %}
      <p class="q-footer-contact">
        {% if b.phone %}<a class="q-footer-phone" href="tel:{{ b.phone|regex_replace('[^0-9+]','') }}">{{ b.phone }}</a>{% endif %}
        {% if b.phone and b.email %} &nbsp;·&nbsp; {% endif %}
        {% if b.email %}<a href="mailto:{{ b.email }}">{{ b.email }}</a>{% endif %}
      </p>
      {% endif %}
      <div class="q-footer-social">
        {% if b.facebook %}<a href="{{ b.facebook }}" aria-label="Facebook"><svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M22 12a10 10 0 1 0-11.6 9.9v-7H7.9V12h2.5V9.8c0-2.5 1.5-3.9 3.8-3.9 1.1 0 2.2.2 2.2.2v2.5h-1.2c-1.2 0-1.6.75-1.6 1.5V12h2.7l-.43 2.9h-2.3v7A10 10 0 0 0 22 12z"/></svg></a>{% endif %}
        {% if b.instagram %}<a href="{{ b.instagram }}" aria-label="Instagram"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg></a>{% endif %}
        {% if b.linkedin %}<a href="{{ b.linkedin }}" aria-label="LinkedIn"><svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.42v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.07 2.07 0 1 1 0-4.14 2.07 2.07 0 0 1 0 4.14zm1.78 13.02H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.73C24 .77 23.2 0 22.22 0z"/></svg></a>{% endif %}
        {% if b.x %}<a href="{{ b.x }}" aria-label="X"><svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M18.9 2H22l-7.4 8.5L23 22h-6.8l-5.3-6.9L4.8 22H1.7l7.9-9L1 2h7l4.8 6.3L18.9 2zm-1.2 18h1.9L7.2 3.9H5.2L17.7 20z"/></svg></a>{% endif %}
      </div>
    </div>
    <div>
      {% if b.show_menu_1 and b.menu_1 %}
        {% set fm1 = menu(b.menu_1) %}
        {% if b.menu_1_title %}<div class="q-footer-head">{{ b.menu_1_title }}</div>{% endif %}
        <nav class="q-footer-links" aria-label="{{ b.menu_1_title or 'Footer' }}">{% for item in fm1.children %}<a href="{{ item.url }}">{{ item.label }}</a>{% endfor %}</nav>
      {% endif %}
    </div>
    <div>
      {% if b.show_menu_2 and b.menu_2 %}
        {% set fm2 = menu(b.menu_2) %}
        {% if b.menu_2_title %}<div class="q-footer-head">{{ b.menu_2_title }}</div>{% endif %}
        <nav class="q-footer-links" aria-label="{{ b.menu_2_title or 'Footer' }}">{% for item in fm2.children %}<a href="{{ item.url }}">{{ item.label }}</a>{% endfor %}</nav>
      {% endif %}
    </div>
  </div>
  <div class="q-container q-footer-legal">
    Copyright &copy; {{ year }} {{ b.company_name }}
    {% if b.privacy_url %} &nbsp;|&nbsp; <a href="{{ b.privacy_url }}">Privacy Policy</a>{% endif %}
    {% if b.terms_url %} &nbsp;|&nbsp; <a href="{{ b.terms_url }}">Terms of Service</a>{% endif %}
  </div>
</footer>
'''

FOOTER_CSS = r'''.q-footer{background:var(--bg);border-top:1px solid var(--border);padding:76px 0 44px;}
.q-footer-grid{display:grid;grid-template-columns:1.6fr 1fr 1fr;gap:56px;align-items:start;}
.q-footer-grid img{height:38px;width:auto;}
.q-footer-tag{font-size:15px;line-height:1.6;color:var(--fg-muted);margin:22px 0 24px;max-width:300px;}
.q-footer-contact{font-size:15px;color:var(--fg-muted);margin:0 0 20px;line-height:1.8;}
.q-footer-contact a{color:var(--fg-muted);text-decoration:none;}
.q-footer-contact .q-footer-phone{color:var(--fg);font-weight:600;}
.q-footer-social{display:flex;gap:18px;align-items:center;}
.q-footer-social a{color:var(--fg-muted);display:inline-flex;width:44px;height:44px;align-items:center;justify-content:center;margin:-12px;}
.q-footer-social a:hover{color:var(--accent-ink);}
.q-footer-head{font-size:13px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:var(--fg);margin-bottom:18px;}
.q-footer-links{display:flex;flex-direction:column;gap:6px;font-size:15px;}
.q-footer-links a{color:var(--fg-muted);text-decoration:none;display:block;padding:4px 0;}
.q-footer-links a:hover{color:var(--accent-ink);}
.q-footer-legal{margin-top:56px;padding-top:26px;border-top:1px solid var(--border);text-align:center;font-size:14px;color:var(--fg-muted);}
.q-footer-legal a{color:var(--fg-muted);text-decoration:underline;}
@media(max-width:600px){.q-footer-grid{grid-template-columns:1fr;gap:34px;}}
'''

SCHEMA_MODULE = r'''{#- Structured data, fail-safe. No org_name, no output. Organization + WebSite on the home
    page only (Google: "you don't need to include it on every page of your site");
    BreadcrumbList everywhere but home. JSON-LD in <body> is valid. process/structured-data.md -#}
{% set s = module %}
{% if s.org_name %}
{% set _home = (request.path == '/' or request.path == '') %}
{% set _site = (s.org_url or ('https://' ~ request.domain))|regex_replace('/$','') %}
{% if _home %}
{% set _sa = [] %}{% for _u in s.org_sameas %}{% if _u %}{% set _sa = _sa + [_u] %}{% endif %}{% endfor %}
<script type="application/ld+json">{"@context":"https://schema.org","@type":"Organization","@id":"{{ _site }}/#organization","name":{{ s.org_name|tojson }}{% if s.org_alt_name %},"alternateName":{{ s.org_alt_name|tojson }}{% endif %},"url":"{{ _site }}"{% if s.org_logo.src %},"logo":{"@type":"ImageObject","url":{{ s.org_logo.src|tojson }}}{% endif %}{% if s.org_description %},"description":{{ s.org_description|tojson }}{% endif %}{% if _sa %},"sameAs":{{ _sa|tojson }}{% endif %}{% if s.founder_name %},"founder":{"@type":"Person"{% if s.founder_url %},"@id":{{ s.founder_url|tojson }}{% endif %},"name":{{ s.founder_name|tojson }}{% if s.founder_title %},"jobTitle":{{ s.founder_title|tojson }}{% endif %}{% if s.founder_sameas %},"sameAs":[{{ s.founder_sameas|tojson }}]{% endif %}}{% endif %}{% if s.contact_email or s.contact_phone %},"contactPoint":{"@type":"ContactPoint","contactType":"Sales"{% if s.contact_email %},"email":{{ s.contact_email|tojson }}{% endif %}{% if s.contact_phone %},"telephone":{{ s.contact_phone|tojson }}{% endif %},"areaServed":"US","availableLanguage":"English"}{% endif %}{% if s.knows_about %},"knowsAbout":{{ s.knows_about|split(',')|map('trim')|list|tojson }}{% endif %}}</script>
<script type="application/ld+json">{"@context":"https://schema.org","@type":"WebSite","@id":"{{ _site }}/#website","url":"{{ _site }}","name":{{ s.org_name|tojson }},"publisher":{"@id":"{{ _site }}/#organization"},"inLanguage":"{{ html_lang or 'en-US' }}"{% if s.search_path %},"potentialAction":{"@type":"SearchAction","target":"{{ _site }}{{ s.search_path }}?q={search_term_string}","query-input":"required name=search_term_string"}{% endif %}}</script>
{% elif request.path %}
{% set _bcns = namespace(url=_site, pos=1, items='{"@type":"ListItem","position":1,"name":"Home","item":' ~ ((_site ~ '/')|tojson) ~ '}') %}
{% for _seg in request.path|split('/') %}{% if _seg %}{% set _bcns.url = _bcns.url ~ '/' ~ _seg %}{% set _bcns.pos = _bcns.pos + 1 %}{% set _bcns.items = _bcns.items ~ ',{"@type":"ListItem","position":' ~ _bcns.pos ~ ',"name":' ~ ((_seg|replace('-',' ')|title)|tojson) ~ ',"item":' ~ (_bcns.url|tojson) ~ '}' %}{% endif %}{% endfor %}
<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{ _bcns.items }}]}</script>
{% endif %}
{% endif %}
'''

HEADER_PARTIAL = r'''<!--
  templateType: global_partial
  label: Quantum Header
  isAvailableForNewContent: false
-->
{% module "quantum_org_schema" path="../../modules/quantum-org-schema" %}
{% module "quantum_site_header" path="../../modules/quantum-site-header" %}
'''

FOOTER_PARTIAL = r'''<!--
  templateType: global_partial
  label: Quantum Footer
  isAvailableForNewContent: false
-->
{% module "quantum_site_footer" path="../../modules/quantum-site-footer" %}
'''

SKIP_CSS = ("/* skip link (themefix) */\n"
            ".q-skip{position:absolute;top:-200px;left:8px;z-index:100;background:var(--q-gold);color:var(--cta-fg);"
            "padding:10px 16px;border-radius:6px;font-weight:600;}\n"
            ".q-skip:focus{top:8px;outline:2px solid var(--fg);outline-offset:2px;}\n"
            "#q-content:focus{outline:none;}\n")

# Anchored: `color:` as a property, not the tail of border-color / border-left-color.
COLOR_GOLD_RE = re.compile(r"(?<![\w-])color:\s*var\(--q-gold\)")
ORG_BLOCK_RE = re.compile(r'\s*<script type="application/ld\+json">\{"@context":"https://schema\.org","@type":"Organization"[^\n]*</script>')


# --------------------------------------------------------------------------- patching

def patch_css(css: str, theme: str) -> tuple[str, dict]:
    native = reskin.parse_native(css)
    if not native:
        raise SystemExit(f"{theme}: no NATIVE DIRECTION block in css/quantum.css")
    gold, bg = native["--q-gold"], native["--bg"]
    ink = reskin.darken_until(gold, bg)
    lift = gold if reskin.relative_luminance(bg) < 0.18 else reskin.darken_until(gold, native.get("--bg-alt", bg))
    cta_fg = native.get("--cta-fg", "")
    if reskin.contrast_ratio(cta_fg, gold) < 4.5:
        cta_fg = reskin.best_on(gold)
    g = GEOMETRY[theme]
    add = {
        "--accent": "var(--q-gold)", "--accent-ink": ink, "--accent-lift": lift, "--cta-fg": cta_fg,
        "--maxw": f"{g['maxw']}px", "--sec-y": f"{g['sec_y']}px", "--radius": f"{g['radius']}px",
        "--hero-size": f"{g['hero']}px", "--display-2": f"{g['d2']}px",
    }
    m = reskin.NATIVE_RE.search(css)
    head, body, tail = css[:m.start(2)], m.group(2), css[m.end(2):]
    for k, v in add.items():
        if re.search(rf"{re.escape(k)}\s*:", body):
            body = re.sub(rf"{re.escape(k)}\s*:[^;]+;", f"{k}:{v};", body)
        else:
            body = body.rstrip() + f"\n  {k}:{v};\n"
    css = head + body + tail
    css = css.replace(".q-container{max-width:1240px;", ".q-container{max-width:var(--maxw);", 1)
    css = css.replace(".q-section{padding:110px 0;}", ".q-section{padding:var(--sec-y) 0;}", 1)
    css = re.sub(r"(\.q-card\{[^}]*?)border-radius:8px;", r"\1border-radius:var(--radius);", css, count=1)
    css = css.replace(".q-h1{font-family:var(--q-serif);font-size:82px;", ".q-h1{font-family:var(--q-serif);font-size:var(--hero-size);", 1)
    css = css.replace(".q-h2{font-family:var(--q-serif);font-size:50px;", ".q-h2{font-family:var(--q-serif);font-size:var(--display-2);", 1)
    # Five stages in two columns is 2+2+1: an orphan, on every theme's own framework section.
    # Stay five across on a tablet (the stage text is capped at 180px) and stack on a phone.
    css = css.replace("@media(max-width:1024px){.q-h1{font-size:56px;}.q-h2{font-size:38px;}.q-grid-5{grid-template-columns:1fr 1fr;}}",
                      "@media(max-width:1024px){.q-h1{font-size:56px;}.q-h2{font-size:38px;}.q-grid-5{grid-template-columns:repeat(5,1fr);gap:16px;}}", 1)
    css, n = COLOR_GOLD_RE.subn("color:var(--accent-ink)", css)
    # Idempotent against an earlier run: replace the skip-link rules if present, else append.
    css = re.sub(r"/\* skip link \(themefix\) \*/\n(\.q-skip\{[^}]*\}\n\.q-skip:focus\{[^}]*\}\n(#q-content:focus\{[^}]*\}\n)?)", "", css)
    css = css.rstrip() + "\n" + SKIP_CSS
    return css, {"ink": ink, "lift": lift, "cta_fg": cta_fg, "ink_ratio": round(reskin.contrast_ratio(ink, bg), 2),
                 "cta_ratio": round(reskin.contrast_ratio(cta_fg, gold), 2), "color_rewrites": n}


def patch_base(html: str, theme: str) -> str:
    """Eight: drop the hardcoded QBS Organization block (the module is fail-safe now), add
    preconnects, skip link and content landmark. Void: landmark + skip link only."""
    if theme != LIVE_QBS_THEME:
        html = ORG_BLOCK_RE.sub("", html, count=1)
        if "fonts.gstatic.com" not in html:
            html = html.replace("  {{ require_css(", '  <link rel="preconnect" href="https://fonts.googleapis.com">\n'
                                '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n  {{ require_css(', 1)
    if 'class="q-skip"' not in html:
        html = html.replace('<div class="body-wrapper">', '<a class="q-skip" href="#q-content">Skip to content</a>\n  <div class="body-wrapper">', 1)
    if 'id="q-content"' not in html:
        html = html.replace("{% block body %}{% endblock %}", '<div id="q-content" tabindex="-1">{% block body %}{% endblock %}</div>', 1)
    return html


def apply(theme: str, write: bool = True) -> list[str]:
    root = os.path.join(SRC, theme)
    if not os.path.isdir(root):
        raise SystemExit(f"{root} missing -- run reskin.py export --theme '{theme}' first")
    changed = []

    def put(rel, content):
        p = os.path.join(root, rel)
        old = open(p, encoding="utf-8").read() if os.path.exists(p) else None
        if old != content:
            changed.append(rel)
            if write:
                os.makedirs(os.path.dirname(p), exist_ok=True)
                open(p, "w", encoding="utf-8").write(content)

    def putjson(rel, obj):
        put(rel, json.dumps(obj, indent=2, ensure_ascii=False) + "\n")

    css, info = patch_css(open(os.path.join(root, "css/quantum.css"), encoding="utf-8").read(), theme)
    put("css/quantum.css", css)
    put("templates/layouts/base.html", patch_base(open(os.path.join(root, "templates/layouts/base.html"), encoding="utf-8").read(), theme))

    if theme != LIVE_QBS_THEME:
        put("templates/partials/header.html", HEADER_PARTIAL)
        put("templates/partials/footer.html", FOOTER_PARTIAL)
        put("modules/quantum-site-header.module/module.html", HEADER_MODULE)
        put("modules/quantum-site-header.module/module.css", HEADER_CSS)
        put("modules/quantum-site-header.module/module.js", "")
        putjson("modules/quantum-site-header.module/fields.json", header_fields(QBS_BRAND))
        putjson("modules/quantum-site-header.module/meta.json", meta("Quantum Site Header"))
        put("modules/quantum-site-footer.module/module.html", FOOTER_MODULE)
        put("modules/quantum-site-footer.module/module.css", FOOTER_CSS)
        put("modules/quantum-site-footer.module/module.js", "")
        putjson("modules/quantum-site-footer.module/fields.json", footer_fields(QBS_BRAND))
        putjson("modules/quantum-site-footer.module/meta.json", meta("Quantum Site Footer"))
        put("modules/quantum-org-schema.module/module.html", SCHEMA_MODULE)
        put("modules/quantum-org-schema.module/module.css", "")
        put("modules/quantum-org-schema.module/module.js", "")
        putjson("modules/quantum-org-schema.module/fields.json", schema_fields())
        putjson("modules/quantum-org-schema.module/meta.json", meta("Quantum Organization Schema"))

    skip = {"css/quantum.css", "templates/layouts/base.html"}
    if theme != LIVE_QBS_THEME:
        skip |= {"templates/partials/header.html", "templates/partials/footer.html"}
    for dirpath, _, files in os.walk(root):
        for fn in files:
            rel = os.path.relpath(os.path.join(dirpath, fn), root)
            if rel in skip or rel.startswith("modules/quantum-site-") or rel.startswith("modules/quantum-org-schema"):
                continue
            if not fn.endswith((".html", ".css")):
                continue
            txt = open(os.path.join(root, rel), encoding="utf-8").read()
            new = COLOR_GOLD_RE.sub("color:var(--accent-ink)", txt)
            if rel.startswith("templates/") and "<main>" in new:
                new = new.replace("<main>", '<main id="main">')
            if new != txt:
                put(rel, new)
    print(f"{theme:20} ink {info['ink']} ({info['ink_ratio']}:1)  cta-fg {info['cta_fg']} ({info['cta_ratio']}:1)  "
          f"css color rewrites {info['color_rewrites']}  files changed {len(changed)}")
    return changed


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--theme")
    p.add_argument("--all", action="store_true")
    p.add_argument("--dry-run", action="store_true", help="report, write nothing")
    p.add_argument("--write-manifest", help="path: write {theme: [changed files]} JSON for reskin.py upload")
    a = p.parse_args(argv)
    themes = reskin.NINE if a.all else [a.theme]
    if not themes or themes == [None]:
        p.error("--theme or --all")
    manifest = {t: apply(t, write=not a.dry_run) for t in themes}
    if a.write_manifest:
        json.dump(manifest, open(a.write_manifest, "w"), indent=1)
        print(f"manifest -> {a.write_manifest}")
    print("\nNothing touched the portal. Read `git diff themes/source`, then:\n"
          "  python3 scripts/reskin.py upload --manifest <file> --fix-at-source --approved-by <name> --reason \"...\"")


if __name__ == "__main__":
    main()
