"""Design wow pass 1: content for the building cutaway (home), the product anatomy module, and the rich mega menus.

apply(data) runs last in finalize(), after dmp_cutouts.apply, so every image path written here is already a cutout
path (looked up through dmp_cutouts.MAP). Section types live in scripts/preview_dw1.py.

Every fact line below is paraphrased from the product's own page text (dmp_pages_products.py) or from a page already
in the build. Nothing is invented. The XR650 is coming soon and never gets an order button.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dmp_cutouts as cut  # noqa: E402
import dmp_pages_products as pm  # noqa: E402

BY = {r["slug"]: r for r in pm.RAW}


def _img(slug):
    p = pm.PRODUCTS[slug]["image"]
    return cut.MAP.get(p, p)


def _p(slug, name, fact):
    r = BY[slug]
    return {"name": name, "kicker": r["kicker"].split(",")[0], "image": _img(slug), "href": f"products/{slug}.html", "fact": fact,
            "soon": "coming soon" in r["kicker"].lower()}


# ------------------------------------------------------------------ home: protect the whole building
SPOTS = [
    {"id": "roof", "label": "Roof", "title": "The communicator on the roof",
     "lede": "Alarms travel over LTE cellular straight to the DMP monitoring center receiver, with no network operations center in between.",
     "products": [
         _p("263lte", "263LTE", "AT&T and Verizon cellular communicator for XT and XR Series panels."),
         _p("265lte", "265LTE", "Adds LTE to an XTL panel. The panel powers it, so no extra enclosure."),
         _p("scs-vr-virtual-receiver-software", "SCS-VR", "A UL Classified virtual receiver that runs on a server, for network IP and cellular signals.")]},
    {"id": "windows", "label": "Windows", "title": "Windows and openings",
     "lede": "The 1100 Series wireless line: transmitters, detectors, receivers and translators.",
     "products": [
         _p("1128", "1128 Glassbreak Detector", "Detects glassbreak up to 20 feet from framed glass in an outside wall."),
         _p("1101", "1101 Universal Transmitter", "Two independent reporting zones from one transmitter.")],
     "more": {"label": "See the wireless line", "href": "services/wireless.html"}},
    {"id": "door", "label": "Main door", "title": "The main door",
     "lede": "Access control from a single door to hundreds.",
     "products": [
         _p("x1", "X1", "A single-door access controller with an onboard network or Wi-Fi communicator."),
         _p("entre-enterprise", "Entré Enterprise", "96 doors of access control, expandable to 400 doors and 500 panels.")]},
    {"id": "gate", "label": "Parking gate and lot", "title": "The parking gate and lot",
     "lede": "Credentials at the gate, cameras over the lot.",
     "products": [
         _p("dmp-bluetooth-reader-and-mobile-credential", "SR3 Bluetooth Reader", "One reader for phones and 125 kHz prox cards, rated IP67 for harsh environments."),
         _p("vplus-7061-fe", "VUE Plus 6MP Fisheye", "A 360 degree view with AlarmVision onboard, indoor or outdoor."),
         _p("xv-gateways-with-alarmvision", "XV Gateways with AlarmVision", "Loitering, person, vehicle and animal detection from your customers' cameras.")]},
    {"id": "panel", "label": "Panel room", "title": "The panel closet",
     "lede": "The control panel, sized from small business to very large sites.",
     "products": [
         _p("xr550", "XR550", "96 doors of access control, 574 zones and 10,000 user codes."),
         _p("xt75", "XT75", "Intrusion, access control and AlarmVision on a single network panel.")]},
    {"id": "stair", "label": "Stairwell", "title": "The stairwell",
     "lede": "Addressable fire detection tells owners and responders the exact location of an alarm.",
     "products": [
         _p("xf6", "XF6", "An addressable 24V fire panel with network or optional cellular reporting."),
         _p("2w-blx", "2W-BLX Smoke Detector", "An addressable photoelectric detector, listed to ANSI/UL 268.")]},
    {"id": "teller", "label": "Teller and vault", "title": "The teller line and vault",
     "lede": "Bank-grade protection for financial customers.",
     "products": [
         _p("xr550", "XR550", "UL bank, safe and vault listing, with Card Plus Pin and Dual Authority."),
         _p("tmsentry", "TMSentry", "Built-in encryption and six supervised zones in a slim ATM and ITM panel.")]},
    {"id": "phone", "label": "Owner's phone", "title": "The owner's phone",
     "lede": "Owners and dealers stay in control from anywhere.",
     "products": [
         _p("virtual-keypad", "Virtual Keypad", "Check status, arm and disarm, and control locks and cameras from a phone, tablet or computer."),
         _p("digital-key-credential", "Digital Key", "A secure credential in the phone's mobile wallet that works over NFC, even on a dead phone.")]},
]


def _building():
    return {"type": "dwbuilding", "id": "building", "dark": True, "eyebrow": "Protect the whole building",
            "heading": "Walk the building. See what protects each spot.",
            "intro": "Pick a spot on the building, or take the guided tour. Every stop lists the DMP products that belong there.",
            "spots": SPOTS, "note": "A starting point. A dealer confirms the design."}


# ------------------------------------------------------------------ product anatomy
SOFT = ("software", "app", "portal", "management")


def _anatomy(page):
    secs = page["sections"]
    ps = next((s for s in secs if s["type"] == "prodstage"), None)
    ci = next((i for i, s in enumerate(secs) if s["type"] == "cards" and len(s["items"]) >= 4), None)
    if ps is None or ci is None:
        return
    items = secs[ci]["items"][:6]
    kick = ps["eyebrow"]
    soft = any(w in kick.lower() for w in SOFT)
    slug = page["file"].split("/")[1][:-5]
    short = BY[slug]["short"]
    secs[ci] = {"type": "dwanatomy", "id": "anatomy", "dark": True, "soft": soft,
                "eyebrow": "Inside the app" if soft else "Anatomy",
                "heading": f"{short}, feature by feature", "name": short,
                "image": ps["image"], "image_alt": ps.get("image_alt", ""), "image_w": ps.get("image_w", 1200), "image_h": ps.get("image_h", 800),
                "items": [{"n": i + 1, "title": t, "text": b} for i, (t, b) in enumerate(items)],
                "note": "Callouts around the picture list the features on this page. They do not point to the position of a part."}


# ------------------------------------------------------------------ mega menus
def _mi(path):
    return cut.MAP.get(path, path)


PRODUCT_TILES = [
    ["Intrusion", "Control panels, detectors and cellular-jam protection for intrusion alarm systems.", "services/intrusion.html", "assets/p-xr550-1200-cut.png"],
    ["Access control", "Access control from a stand-alone cloud system to the Entré enterprise software.", "services/access-control.html", "assets/p-x1-1200-cut.png"],
    ["Fire", "Fire alarm control panels, detectors and communicators.", "services/fire.html", "assets/p-xf6-1200-cut.png"],
    ["Video", "VUE Plus cameras, AlarmVision analytics and the VK VMS video management platform.", "services/video.html", "assets/p-vplus-7061-fe-1200-cut.png"],
    ["Communicators", "Cellular, network and universal communicators, and the monitoring center equipment that receives them.", "services/communicators.html", "assets/p-263lte-1200-cut.png"],
    ["Wireless", "The 1100 Series wireless line: transmitters, detectors, receivers and translators.", "services/wireless.html", "assets/p-1100xh-1200-cut.png"],
    ["Panels and keypads", "Control panels, keypads, modules, expanders, power supplies and enclosures.", "services/panels-keypads.html", "assets/keypad-722-1200-cut.png"],
    ["Software", "Virtual Keypad, Dealer Admin, Entré, Z-Wave automation and the cloud services behind them.", "services/mobile-automation.html", "assets/p-virtual-keypad-1200-cut.png"],
]

INDUSTRY_CHIPS = [
    ["Commercial", "industries/commercial.html", "assets/hq-exterior-2-1200.png"],
    ["Financial institutions", "industries/financial-institutions.html", "assets/vault-1200.jpg"],
    ["Retail", "industries/retail.html", "assets/tab-mobile-1200.jpg"],
    ["Government", "industries/government.html", "assets/tab-access-1200.jpg"],
    ["Industrial and manufacturing", "industries/industrial-manufacturing.html", "assets/plant-1200.jpg"],
    ["Education", "industries/education.html", "assets/digital-key-1200.jpg"],
    ["Healthcare and wellness", "industries/healthcare-wellness.html", "assets/dualsim-1200.jpg"],
    ["Multi-tenant", "industries/multi-tenant.html", "assets/sensor-1112-1200.jpg"],
    ["Religious institutions", "industries/religious-institutions.html", "assets/tab-intrusion-1200.jpg"],
    ["Storage units", "industries/storage-units.html", "assets/alarmvision-1200.jpg"],
    ["Residential", "industries/residential.html", "assets/phone-commercial-1200.jpg"],
]

SUPPORT_LINES = [
    {"label": "Quotes and system design", "number": "877-757-4367", "text": "Inside Sales: system design, quotes and pricing.", "hours": "8 a.m. to 5 p.m. Central"},
    {"label": "Installation and programming", "number": "888-436-7832", "text": "Technical Support: installation, programming and troubleshooting.", "hours": "7 a.m. to 7 p.m. Central"},
    {"label": "Orders and shipping", "number": "866-266-2826", "text": "Customer Service: products and ordering, software activations, shipping.", "hours": "8 a.m. to 6 p.m. Central"},
    {"label": "Cellular activation", "number": "877-300-8030", "text": "SecureCom Wireless: activation and billing.", "hours": "8 a.m. to 5 p.m. Central"},
]


def _nav(data):
    for it in data["nav"]:
        if not isinstance(it, dict):
            continue
        lab = it["label"]
        if lab == "Products":
            xr = BY["xr550"]
            it["dw_mega"] = {"kind": "products", "tiles": [[a, b, c, _mi(d)] for a, b, c, d in PRODUCT_TILES],
                             "featured": {"eyebrow": "Flagship panel", "name": "XR550 Control Panel", "image": _img("xr550"), "href": "products/xr550.html",
                                          "body": "96 doors, 574 zones and 10,000 user codes, with encrypted communication options.", "label": "View the XR550"},
                             "foot": [["All products", "services.html"], ["Find a system", "find-a-system.html"]]}
        elif lab == "Industries":
            it["dw_mega"] = {"kind": "industries", "chips": [[a, b, _mi(c)] for a, b, c in INDUSTRY_CHIPS],
                             "foot": [["All eleven industries", "industries.html"], ["Find a system", "find-a-system.html"]]}
        elif lab == "Support":
            it["dw_mega"] = {"kind": "support", "lines": SUPPORT_LINES,
                             "links": [list(c) for c in it["children"] if c[1] not in ("support.html",)],
                             "foot": [["Contact and support", "support.html"], ["Technical documentation", "support/documentation.html"]]}


def apply(data):
    _nav(data)
    for p in data["pages"]:
        f = p["file"]
        if f == "index.html":
            secs = p["sections"]
            i = next((k for k, s in enumerate(secs) if s.get("id") == "systems"), None)
            if i is not None:
                secs.insert(i + 1, _building())
        elif f.startswith("products/"):
            _anatomy(p)
    return data
