"""Design wave B content: pinned stories on the four system pages, the distributor map on the international page,
icon keys for the audience cards and the three doors, and the page rhythm fixes (section flags).

apply(data) runs last in finalize(). Everything shown is read from text already on the page: the steps are the page's
"What you get" cards plus its "Start from the product" card, the pins are the eight distributors listed on the page.
"""
import re

STORY_PAGES = ("services/intrusion.html", "services/fire.html", "services/video.html", "services/panels-keypads.html")

# approximate region centres (latitude, longitude). Mexico has two distributors, so the pins sit apart inside the country.
GEO = {
    "Benelux": (51.2, 5.2),
    "Greece and Cyprus": (36.6, 27.0),
    "Hungary": (47.2, 19.4),
    "Latin America and the Caribbean": (13.0, -72.0),
    "Otwo": (25.5, -104.5),
    "Tecnoseguridad": (17.8, -96.5),
    "South Africa, Mozambique and Zambia": (-24.5, 29.5),
    "United Kingdom and Ireland": (53.4, -5.8),
}
SPRINGFIELD = (37.2, -93.3)


def _page(data, f):
    return next((p for p in data["pages"] if p["file"] == f), None)


def _story(data):
    for f in STORY_PAGES:
        pg = _page(data, f)
        if not pg:
            continue
        secs = pg["sections"]
        hero = secs[0]
        i = next((k for k, s in enumerate(secs) if s["type"] == "cards" and s.get("id") == "overview"), None)
        if i is None or not hero.get("float"):
            continue
        cards = secs[i]
        steps = [{"title": t, "text": b} for t, b in cards["items"]]
        a, bb = hero.get("card_a"), hero.get("card_b")
        if a:
            steps.append({"title": a["title"], "text": a["body"], "links": [tuple(x) for x in (bb or {}).get("links", [])],
                          "cta": (a["label"], a["href"])})
        secs[i] = {"type": "dw2-story", "id": "overview", "eyebrow": cards.get("eyebrow"), "heading": cards["heading"],
                   "image": hero["float"], "alt": hero.get("float_alt", ""), "steps": steps}


def _map(data):
    pg = _page(data, "international.html")
    if not pg:
        return
    secs = pg["sections"]
    j = next((k for k, s in enumerate(secs) if s.get("id") == "find-your-distributor"), None)
    if j is None:
        return
    items = []
    for region, company, text, label, url in secs[j]["items"]:
        m = re.search(r"contact for this region is ([^.]+)\.", text)
        key = company if region == "Mexico" else region
        if key not in GEO:
            key = next((k for k in GEO if region.startswith(k)), None)
        if key is None:
            continue
        lat, lon = GEO[key]
        items.append({"region": region, "company": company, "contact": m.group(1) if m else "", "label": label, "url": url, "lat": lat, "lon": lon})
    secs.insert(j, {"type": "dw2-map", "id": "map", "dark": True, "eyebrow": "Worldwide", "heading": "Eight authorized distributors on one map",
                    "intro": "Each distributor with its website and the DMP contact for the region.", "hint": "Hover, focus or tap a pin.",
                    "hq": SPRINGFIELD, "hq_label": "Springfield, Missouri", "items": items,
                    "aria": "World map of the eight authorized DMP distributors"})


def _icons(data):
    def cards(f, idx_heading, keys):
        pg = _page(data, f)
        if not pg:
            return
        for s in pg["sections"]:
            if s["type"] == "cards" and s.get("heading", "").startswith(idx_heading) and len(s["items"]) == len(keys):
                s["icons"] = keys
    cards("for-dealers.html", "What opens when you sign in", ["docs", "cloud", "partner", "training", "support", "docs"])
    cards("for-dealers.html", "Free firmware", ["cloud", "partner", "communicator", "support", "intrusion", "partner"])
    cards("for-specifiers.html", "Four places", ["docs", "partner", "cloud", "support"])
    cards("for-building-owners.html", "Four steps", ["access", "support", "docs", "mobile"])
    cards("for-building-owners.html", "Six questions", ["keypad", "communicator", "access", "mobile", "support", "partner"])
    home = _page(data, "index.html")
    if home:
        for s in home["sections"]:
            if s["type"] == "doors":
                for it, k in zip(s["items"], ("partner", "docs", "intrusion")):
                    it["icon"] = k


def _rhythm(data):
    """Section flags so no two neighbouring sections share a background. Flags are read on the pre-augment page (preview_pop2.augment
    inserts its own day, outcomes, numbers and router sections at render time); the checks below are by type so a changed page is skipped."""
    def flag(f, typ, sid=None, **kw):
        pg = _page(data, f)
        for sec in (pg["sections"] if pg else []):
            if sec["type"] == typ and (sid is None or sec.get("id") == sid):
                sec.update(kw)
                return
    flag("index.html", "stats3d", alt=True)                    # partners, facts and systems were three white bands in a row
    flag("index.html", "faq", alt=True)                        # guides and faq were both white
    flag("contact.html", "tiles", "selfservice", alt=True)     # form and self-service tiles were both white
    flag("find-a-system.html", "showcase3d", "flagships", dark=True)   # hero, flagships, finder, facts, resources and faq were all white
    flag("find-a-system.html", "stats3d", alt=True)
    flag("find-a-system.html", "faq", dark=True)
    flag("dealer-portal.html", "portal", alt=True)             # hero, portal and network were all white
    flag("dealer-portal.html", "network", dark=True)
    flag("dealer-portal.html", "faq", dark=True)
    flag("blog.html", "faq", alt=False)                        # faq and the subscribe form were both alt
    for pg in data["pages"]:
        if pg["file"].startswith("industries/") and pg["file"] != "industries.html":
            for s in pg["sections"]:
                if s["type"] == "stats3d" and not s.get("dark") and not s.get("alt"):
                    s["alt"] = True                             # tiles and the facts band were both white


def apply(data):
    _story(data)
    _map(data)
    _icons(data)
    _rhythm(data)
    return data
