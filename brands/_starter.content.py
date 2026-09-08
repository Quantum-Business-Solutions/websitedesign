#!/usr/bin/env python3
"""STARTER content file for a new client. Copy to brands/<slug>.content.py and fill the CAPITALISED constants.

The signature set is placed by default (runbook version two). Removing a module is a decision; adding one is not.
Every fact must be sourced: the client's site, their call notes, awards listings, the trade press. Mark anything
that is only in a proposal with a PROPOSAL comment and list it under pitch["confirm"].
No em dashes anywhere. No exclamation marks. No response-time or pricing promises the client has not published.

Run:
    python3 brands/<slug>.content.py
    python3 scripts/preview.py --content brands/<slug>.content.json --themes "Quantum Showcase,Quantum Clean,Quantum Press" \
        --roles "Showcase: ...|Clean: ...|Press: ..." --base-url https://<slug>.vercel.app --out ../<client-repo>
Pass --recommend only when we are recommending a direction. Showcase goes first.
"""
import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SLUG.content.json")
CLIENT_REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "CLIENT_REPO_FOLDER")

CLIENT = "CLIENT NAME"
SHORT = "CLIENT"                       # one word, used in the wheel hub and voice rules
PHONE, PHONE_HREF = "000-000-0000", "tel:0000000000"
FOUNDED = "YEAR"                       # sourced, or leave "" and add to confirm
REGION = "nc"                          # map region: "nc", "west", or add one in preview_sections.REGIONS

# ------------------------------------------------------------------ sourced facts
TESTIMONIALS = [  # [quote, name, company], only ones published by the client
]
LOCATIONS = [  # slug, city, address 1, address 2, phone, phone href, region label, lon, lat
]
PARTNERS = []  # manufacturer and software partners, primary line FIRST
SEAL_ITEMS = [  # [mark, title, body] and every line must be on the client's site or in an agreement
]
TEAM = []      # [name, role, bio]
SERVICES = [   # slug, nav label, short, one-line, image, eyebrow, heading (<em> allowed), subhead, benefits [[t,b]], included [..], faq [[q,a]]
]
INDUSTRIES = []  # slug, name, image, one-line, body, bullets, faq

# ------------------------------------------------------------------ helpers (do not edit)
def desc(text, n=155):
    if len(text) <= n:
        return text
    cut = text[:n]
    return cut[:cut.rfind(" ")].rstrip(",;:") + "."


def brief(text, n=150):
    if len(text) <= n:
        return text
    cut = text[:n]
    i = max(cut.rfind(". "), cut.rfind("! "), cut.rfind("? "))
    return cut[:i + 1] if i > 60 else cut[:cut.rfind(" ")].rstrip(",;:") + "."


def _flow(fid, eyebrow, heading, intro, steps, receive_label="What you receive"):
    return {"type": "flow", "id": fid, "alt": True, "eyebrow": eyebrow, "heading": heading, "intro": intro, "receive_label": receive_label,
            "steps": [{"label": a, "when": b, "summary": c, "title": d, "body": e, "receive": f} for a, b, c, d, e, f in steps]}


def _ba(bid, heading, b_title, b_body, b_items, a_title, a_body, a_items, b_eyebrow="Today", a_eyebrow=f"With {SHORT}"):
    return {"type": "beforeafter", "id": bid, "eyebrow": "Before and after", "heading": heading,
            "before": {"eyebrow": b_eyebrow, "title": b_title, "body": b_body, "items": b_items},
            "after": {"eyebrow": a_eyebrow, "title": a_title, "body": a_body, "items": a_items}}


LEADFORM = {"type": "leadform", "alt": True, "id": "start", "heading": "START HEADING", "body": "BODY", "submit": "SUBMIT LABEL", "note": "A person replies, not an autoresponder."}

# Per-service signature modules: one process chart and one before/after per line, sourced copy only.
SERVICE_MODULES = {
    # "slug": [_ba(...), _flow(...)],
}


def service_page(slug, navlabel, short, one, image, eyebrow, heading, subhead, benefits, included, faq):
    secs = [
        {"type": "hero", "layout": "split", "eyebrow": eyebrow, "heading": heading, "subhead": subhead,
         "primary": {"label": "PRIMARY CTA", "href": "contact.html"}, "secondary": {"label": "All services", "href": "services.html"},
         "image": image, "image_alt": navlabel, "image_w": 1200, "image_h": 800},
        {"type": "cards", "alt": True, "eyebrow": "What changes", "heading": f"What changes with {SHORT} {short}", "items": benefits},
    ]
    secs += SERVICE_MODULES.get(slug, [])
    secs.append({"type": "detail", "eyebrow": "What is included", "heading": "What you get", "body": "INCLUDED INTRO", "bullets": included, "image": image, "flip": True})
    if TESTIMONIALS:
        secs.append({"type": "testimonials", "alt": True, "heading": "What customers say", "items": [t[:3] for t in TESTIMONIALS[:3]]})
    secs.append({"type": "faq", "heading": f"Questions about {navlabel.lower()}", "items": faq})
    secs.append(LEADFORM)
    return {"file": f"services/{slug}.html", "title": f"{navlabel} | {CLIENT}", "description": desc(f"{one} {subhead}"),
            "crumbs": [["Home", "index.html"], ["Services", "services.html"], [navlabel, f"services/{slug}.html"]], "sections": secs}


MODEL = "assets/fleet/MODEL.glb" if os.path.exists(os.path.join(CLIENT_REPO, "assets", "fleet", "MODEL.glb")) else None
WHEEL_ITEMS = [[s[1], brief(s[3], 140), f"services/{s[0]}.html", s[1]] for s in SERVICES]

# ---- signature set. Fill the copy; keep the structure.
FLOW_ENGAGEMENT = {"type": "flow", "id": "flow", "eyebrow": "How an engagement runs", "heading": "HEADING", "intro": "Click a stage.",
    "steps": [  # {"label","when","summary","title","body","receive":[...]}
    ]}
FLEET = {"type": "fleet", "id": "fleet", "heading": "HEADING", "intro": "Generated product renders for the preview; the client's imagery replaces them.",
    "items": [  # {"title","band","brands","image":"assets/fleet/x.png","bullets":[..],"href"}
    ]}
SEAL = {"type": "seal", "id": "seal", "eyebrow": f"What every {SHORT} customer gets", "heading": "Not a slogan. A list you can check.", "intro": "Each line is published by the client or in an agreement.", "items": SEAL_ITEMS, "source": "Sources: ..."}
BEFORE_AFTER = _ba("ba", "HEADING", "BEFORE TITLE", "BEFORE BODY", [], "AFTER TITLE", "AFTER BODY", [])
HOTSPOTS = {"type": "hotspots", "id": "office", "eyebrow": "The whole place", "heading": "HEADING", "intro": "Click a number.",
    "image": "assets/office-iso-1600.jpg", "image_w": 1600, "image_h": 893, "alt": "ALT",
    "items": [  # {"x","y","k","title","body","href","label"} in percent, measured on the render
    ]}
HERO_LAYERED = {"type": "hero-layered", "id": "hero", "eyebrow": "EYEBROW", "heading": "HEADING with <em>emphasis</em>.", "subhead": "SUBHEAD",
    "primary": {"label": "PRIMARY CTA", "href": "contact.html"}, "secondary": {"label": "SECONDARY", "href": "why.html"},
    "image": "assets/hero-plate-2100.jpg", "image_w": 2100, "image_h": 900,
    **({"model": MODEL, "poster": "assets/fleet/MODEL.png", "model_alt": "ALT"} if MODEL else {}),
    "stats": [],  # [[value, label]] sourced
    "card_a": {"eyebrow": "Start here", "title": "TITLE", "body": "BODY", "items": [], "href": "contact.html", "label": "CTA"},
    "card_b": {"eyebrow": "Already a customer?", "title": "The fast lane", "body": "Under a minute each.", "links": []},
    "note": "Preview photography, renders and the 3D device are generated and labelled as such; the client's own imagery replaces them."}
STORY3D = {"type": "story3d", "id": "device", "eyebrow": "Take a closer look", "heading": "HEADING", "intro": "Scroll, and the device turns to the part being described. A generated stand-in for the preview.",
    "poster": "assets/fleet/MODEL.png", "alt": "ALT", "hint": "Drag to turn", "cta": {"label": "CTA", "href": "services/x.html"},
    "steps": [],  # {"k","title","body","orbit":"30deg 72deg 100%","points":[..]}
    **({"model": MODEL} if MODEL else {})}
HISTORY = {"type": "timeline", "id": "story", "eyebrow": f"Since {FOUNDED}", "heading": "HEADING", "intro": "The dates we could source are here; the rest are on the To confirm list.",
    "items": []}  # [year, title, body, optional image]
MAP = {"type": "map", "id": "map", "heading": "HEADING", "intro": "INTRO", "region": REGION, "ring": 40,
       "items": [{"name": L[1], "lon": L[7], "lat": L[8], "href": f"locations/{L[0]}.html", "sub": L[2], "hq": i == 0} for i, L in enumerate(LOCATIONS)]}


def build():
    brand = {
        "accent": "#000000", "ink_secondary": "#000000", "chrome": "dark", "chrome_bg": "#000000",
        # "type_from": {"Quantum Showcase": "Quantum Clean"},   # borrow a direction's typefaces when the client asks
        "logo": "assets/LOGO", "logo_alt": CLIENT, "logo_w": 300, "logo_h": 100, "logo_note": "",
        "phone": PHONE, "phone_href": PHONE_HREF, "email": "",
        "utility": [], "cta": {"label": "PRIMARY CTA", "href": "contact.html"},
        "sticky": {"primary": "PRIMARY CTA", "primary_href": "contact.html", "secondary": f"Call {SHORT}", "secondary_href": PHONE_HREF},
        "launcher": {"label": "Already a customer?", "eyebrow": "The fast lane", "title": "What do you need today?", "links": [], "note": "", "phone": PHONE, "phone_href": PHONE_HREF},
        "social": {}, "tagline": "TAGLINE", "footer_columns": [], "legal": [],
    }
    schema = {"org_name": CLIENT, "org_url": "https://", "org_logo": "https://", "org_description": "", "sameAs": [], "telephone": ""}
    nav = [
        {"label": "Services", "href": "services.html", "children": [[s[1], f"services/{s[0]}.html"] for s in SERVICES]},
        {"label": "Industries", "href": "industries.html", "children": [[i[1], f"industries/{i[0]}.html"] for i in INDUSTRIES]},
        {"label": "About", "href": "about.html", "children": [["About", "about.html"], ["Locations", "locations.html"], ["Contact", "contact.html"]]},
    ]
    pages = []
    pages.append({"file": "index.html", "title": f"{CLIENT} | TITLE",
                  "compose": {
                      "showcase": ["hero", "partners", "wheel", "fleet", "ba", "flow", "office", "device", "proof", "story", "map", "voices", "faq", "contact"],
                      "clean": ["hero-light", "partners", "seal", "wheel", "is-this-you", "flow", "story", "map", "voices", "faq", "contact"],
                      "press": ["hero-light", "story", "services", "seal", "voices", "flow", "map", "faq", "contact"]},
                  "description": "DESCRIPTION",
                  "sections": [
        {"type": "hero", "id": "hero-light", "layout": "split", "eyebrow": "EYEBROW", "stats": [], "ribbon": [], "heading": "HEADING", "subhead": "SUBHEAD",
         "primary": {"label": "PRIMARY CTA", "href": "contact.html"}, "secondary": {"label": "SECONDARY", "href": "why.html"},
         "note": "Generated preview imagery, labelled as such", "image": "assets/hero-1200.jpg", "image_alt": "ALT", "image_w": 1200, "image_h": 800},
        HERO_LAYERED,
        {"type": "partners", "id": "partners", "caption": "Partners", "items": PARTNERS},
        SEAL,
        {"type": "wheel", "id": "wheel", "eyebrow": "One partner", "heading": "HEADING", "intro": "Hover a segment.", "items": WHEEL_ITEMS, "panel_eyebrow": "Hover a segment", "link_label": "See the service"},
        {"type": "checklist", "id": "is-this-you", "alt": True, "eyebrow": "Is this you?", "heading": "HEADING", "intro": "Check what sounds familiar.", "items": [], "messages": ["Check what sounds familiar.", "One is normal.", "Two is worth a conversation.", "Three or more, and it is time."], "cta_label": "PRIMARY CTA", "cta_href": "contact.html"},
        {"type": "services", "id": "services", "heading": "HEADING", "intro": "INTRO", "items": [[s[1], s[3], f"services/{s[0]}.html"] for s in SERVICES]},
        FLEET, BEFORE_AFTER, FLOW_ENGAGEMENT, HOTSPOTS, STORY3D,
        {"type": "proof", "id": "proof", "alt": True, "eyebrow": "Measured, not claimed", "value": "N", "text": "TEXT", "source": "SOURCE"},
        HISTORY, MAP,
        {"type": "testimonials", "id": "voices", "alt": True, "layout": "feature", "eyebrow": "What customers say", "heading": "HEADING", "items": [t[:3] for t in TESTIMONIALS]},
        {"type": "faq", "id": "faq", "alt": True, "heading": "Questions we get on the first call", "items": []},
        {"type": "contact", "id": "contact", "heading": "HEADING", "body": "BODY", "options": [], "submit": "SUBMIT", "note": "A person replies, not an autoresponder."},
    ]})
    for s in SERVICES:
        pages.append(service_page(*s))
    # add: services index, industries and industry pages, locations and location pages, about, faq, contact, customer support.
    pitch = {
        "qbs_contact": {"name": "Shawn Peterson", "email": "shawn@thequantumleap.business", "phone": "(712) 389-4639"},
        "prepared_for": "NAMES", "heard_intro": "Everything here comes from your site and our conversations. Tell us where it is wrong; your words outrank ours.",
        "heard": [], "found": [], "pick_reasons": [], "pick_change": "", "alternatives": [],
        "choice_intro": "All three are the whole site with the same words and the same proof. The difference is temperament. Open each one and tell us which feels like you.",
        "plan": [], "search": {"heading": "Where you stand in search today, and what changes", "intro": "Measured before we touched anything.", "as_of": "", "today_stats": [], "today": [], "after": [], "keep": [], "note": ""},
        "confirm": [], "footer": "Prepared for NAMES. Nothing here is live or indexed. Photographs, renders and the 3D device are generated and labelled as such.",
    }
    return {"client": CLIENT, "slug": "SLUG", "domain_hint": "DOMAIN", "brand": brand, "schema": schema, "nav": nav, "pages": pages, "pitch": pitch}


if __name__ == "__main__":
    data = build()
    with open(OUT, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print(f"wrote {OUT}: {len(data['pages'])} pages")
