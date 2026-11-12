"""Pop pass 1: content for the home, system and product pages (section types live in scripts/preview_pop1.py).

apply(data) runs last in finalize(). Every fact below is read from the product data in dmp_pages_products.py
(specs, blurbs, kickers) or from text already on the page; nothing is invented. The XR650 is coming soon and
never gets an order button.
"""
import copy
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dmp_pages_products as pm  # noqa: E402

IMG = "assets/"
BUY = "https://buy.dmp.com/dmp/Shop"
NOTE = "A starting point. A dealer confirms the design."
BY = {r["slug"]: r for r in pm.RAW}


def _spec(slug, key):
    for k, v in BY[slug]["specs"]:
        if k == key:
            return v
    raise KeyError((slug, key))


def _card(slug, why="", facts=None, cta=None):
    r, p = BY[slug], pm.PRODUCTS[slug]
    soon = "coming soon" in r["kicker"].lower()
    c = {"name": r["name"], "kicker": r["kicker"].split(",")[0], "image": p["image"], "href": f"products/{slug}.html", "why": why or r["blurb"],
         "facts": facts or [], "soon": soon}
    if pm._stage_kind(p["image"]) in ("light", "dark"):
        c["light"] = True
    if cta:
        c["cta"] = cta
    return c


def _sec_index(secs, pred):
    return next((i for i, s in enumerate(secs) if pred(s)), None)


# ------------------------------------------------------------------ home
def _home(pg):
    secs = pg["sections"]
    i = _sec_index(secs, lambda s: s.get("id") == "who")
    if i is not None:
        secs[i] = {"type": "doors", "id": "who", "dark": True, "eyebrow": "Whoever you are", "heading": "Three doors in. Pick the one you came for.",
                   "intro": "Dealers, specifiers and building owners each get a front door with the answers they ask for first.",
                   "items": [
                       {"kicker": "For dealers", "title": "Order, program and get support, any hour.", "image": IMG + "p-dealer-admin-1200.png", "alt": "Dealer Admin on a laptop",
                        "bullets": ["Order at buy.DMP.com, 24 hours a day", "Dealer Admin: mass programming, bulk firmware updates, templates"], "href": "for-dealers.html", "cta": "Go to dealers"},
                       {"kicker": "For specifiers", "title": "Design support from people who know the system.", "image": IMG + "tab-spec-1200.jpg", "alt": "A tablet showing a floor plan in System Surveyor", "fit": "cover",
                        "bullets": ["Spec sheets on every product page", "System Surveyor integration for intrusion and access design"], "href": "for-specifiers.html", "cta": "Go to specifiers"},
                       {"kicker": "For building owners", "title": "Start with a dealer who can specify it.", "image": IMG + "keypad-722-1200.png", "alt": "The DMP 7-inch touchscreen keypad",
                        "bullets": ["Eleven industries, each with its own page", "Control from a phone with Virtual Keypad"], "href": "for-building-owners.html", "cta": "Go to building owners"}]}
    # proof band after "made here"
    j = _sec_index(secs, lambda s: s.get("id") == "portal")
    if j is not None:
        secs.insert(j + 1, {"type": "proofband", "id": "proof", "dark": True, "eyebrow": "Proof, not promises", "heading": "Built to last, examined every year.",
                            "items": [{"n": "50", "count": 50, "label": "Years making security systems", "sub": "Founded in 1975"},
                                      {"n": "SOC 2", "text": True, "label": "Type II, examined every year", "sub": "Dealer Admin and Virtual Keypad"},
                                      {"n": "14", "count": 14, "label": "Product categories", "sub": "One manufacturer"}],
                            "foot": "Made in Springfield, Missouri, with U.S. and global components."})
    # visual news and guides
    news_thumbs = {"VK VMS": ("p-xv-gateways-with-alarmvision-1200.png", "contain"), "VUE": ("vue-plus-1200.jpg", "contain"), "JamAlert": ("jamalert-1200.jpg", "contain"),
                   "XR650": ("p-xr650-1200.png", "contain"), "System Surveyor": ("system-surveyor-1200.jpg", "cover")}
    guide_thumbs = {"intrusion panel": ("p-xr550-1200.png", "contain"), "cellular": ("p-263lte-1200.png", "contain"), "access control": ("x1-1200.jpg", "contain")}

    def thumbs(items, table, fallback):
        out = []
        for it in items:
            hit = next((v for k, v in table.items() if k.lower() in it[1].lower()), fallback)
            out.append([IMG + hit[0], hit[1]])
        return out

    for s in secs:
        if s["type"] == "resources" and str(s.get("heading", "")).startswith("What we shipped"):
            s.update({"type": "newsfeat", "dark": False, "alt": True, "eyebrow": "News", "thumbs": thumbs(s["items"], news_thumbs, ("hq-exterior-1200.jpg", "cover"))})
        elif s["type"] == "resources" and s.get("id") == "guides":
            s.update({"type": "newsfeat", "eyebrow": "Guides", "thumbs": thumbs(s["items"], guide_thumbs, ("hq-exterior-1200.jpg", "cover"))})
    secs.append({"type": "closer", "id": "ready", "eyebrow": "Next step", "heading": "Ready to see a system that fits your building?",
                 "sub": "Talk to a dealer near you, or join the dealers who install DMP.",
                 "primary": {"label": "Find a dealer", "href": "find-a-dealer.html"}, "secondary": {"label": "Become a dealer", "href": "support/become-a-dealer.html"}})


# ------------------------------------------------------------------ system selectors and flows
def _panel_selector():
    zones = ["Up to 58", "Up to 142", "Up to 574"]
    wl = ["Up to 48", "Up to 100", "Up to 500"]
    doors = ["None", "Up to 8", "Up to 96"]

    def facts(s):
        return [["Total zones", _spec(s, "Total zones")], ["Wireless zones", _spec(s, "Wireless zones")], ["Doors of access", _spec(s, "Doors of access")]]

    cards = {
        "xt50": _card("xt50", f"{_spec('xt50', 'Total zones')} total zones, {_spec('xt50', 'Wireless zones')} wireless zones and {_spec('xt50', 'Doors of access')} doors of access, with an onboard 1100D wireless receiver.", facts("xt50"), "View the XT50"),
        "xr150": _card("xr150", f"{_spec('xr150', 'Total zones')} total zones, {_spec('xr150', 'Wireless zones')} wireless zones and {_spec('xr150', 'Doors of access')} doors of access, with {_spec('xr150', 'User codes')} user codes.", facts("xr150"), "View the XR150"),
        "xr550": _card("xr550", f"{_spec('xr550', 'Total zones')} total zones, {_spec('xr550', 'Wireless zones')} wireless zones, and access control for up to 96 doors, 32 out of the box.", facts("xr550"), "View the XR550"),
    }
    rules = [{"when": [[0], [0], [0, 1]], "res": ["xt50"]}, {"when": [[0, 1], [0, 1], [0, 1]], "res": ["xr150"]}, {"when": [None, None, None], "res": ["xr550"]}]
    return {"type": "panelpick", "id": "fit", "alt": True, "eyebrow": "Find your fit", "heading": "Which panel fits?",
            "intro": "Answer three questions about the site. Each answer maps to the panel specifications listed on its product page.",
            "note": NOTE, "out_label": "Our suggestion", "static_label": "The three panels, by size", "say": "Suggested panel: ",
            "questions": [{"q": "Zones to protect", "options": zones}, {"q": "Wireless zones", "options": wl}, {"q": "Doors of access control", "options": doors}],
            "rules": rules, "cards": cards,
            "also": [{"text": "All wireless, no doors? The XTLplus has 99 two-way wireless zones and up to 140 Z-Wave devices.", "label": "See the XTLplus", "href": "products/xtlplus.html"},
                     {"text": "Intrusion, access control and AlarmVision in one panel for residential and small to medium business?", "label": "See the XT75", "href": "products/xt75.html"},
                     {"text": "Planning past the XR550? The XR650, coming soon and not yet orderable, adds up to 100 areas and 300,000 user codes.", "label": "See the XR650", "href": "products/xr650.html"}]}


def _access_selector():
    doors = ["1 door", "Up to 16 doors", "Up to 96 doors", "Up to 400 doors, many panels"]
    cred = ["Cards or fobs", "A phone over Bluetooth", "A phone with an NFC wallet credential"]
    ctl = ["x1", "entre-lite", "entre-enterprise", "entre-enterprise"]
    cards = {
        "x1": _card("x1", "", [["Doors", "1"], ["Communication", _spec("x1", "Communication")], ["Reader protocols", _spec("x1", "Reader protocols")]], "View the X1"),
        "entre-lite": _card("entre-lite", "", [["Doors", "Up to 16"], ["Runs on", "XR Series panels"]], "View Entré Lite"),
        "entre-enterprise": _card("entre-enterprise", "", [["Doors included", _spec("entre-enterprise", "Doors included")], ["Maximum doors", "400"], ["Maximum panels", _spec("entre-enterprise", "Maximum panels")]], "View Entré Enterprise"),
        "mobile-credential": _card("mobile-credential", "", [["Phones", _spec("mobile-credential", "Phones")], ["Managed in", _spec("mobile-credential", "Managed in")]], "View the credential"),
        "dmp-bluetooth-reader-and-mobile-credential": _card("dmp-bluetooth-reader-and-mobile-credential", "", [["Credentials", _spec("dmp-bluetooth-reader-and-mobile-credential", "Credentials")], ["Ingress rating", "IP67"]], "View the SR3 reader"),
        "digital-key-credential": _card("digital-key-credential", "", [["Phones", _spec("digital-key-credential", "Phones")], ["Managed in", _spec("digital-key-credential", "Managed in")]], "View Digital Key"),
    }
    rules = []
    for di in range(4):
        for ci in range(3):
            res = [ctl[di]] + ([] if ci == 0 else (["mobile-credential", "dmp-bluetooth-reader-and-mobile-credential"] if ci == 1 else ["digital-key-credential"]))
            rules.append({"when": [[di], [ci]], "res": res})
    return {"type": "panelpick", "id": "fit", "alt": True, "eyebrow": "Find your fit", "heading": "Which access control fits?",
            "intro": "Pick the size of the job and how people will open the door. Each suggestion comes from the product pages.",
            "note": NOTE, "out_label": "Our suggestion", "static_label": "Every option", "say": "Suggested: ",
            "questions": [{"q": "How many doors?", "options": doors}, {"q": "How do people open the door?", "options": cred}],
            "rules": rules, "cards": cards,
            "also": [{"text": "Dealers: manage credentials and lock down a lost one from Dealer Admin.", "label": "See Dealer Admin", "href": "products/dealer-admin.html"}]}


def _fire_selector():
    cards = {
        "xf6": _card("xf6", "An addressable 24V fire panel with onboard Ethernet and optional cellular reporting. Supports up to 500 wireless devices.", [["Onboard zones", "Six 24V Class B"], ["Wireless range", _spec("xf6", "Wireless range")], ["Listing", "UL 864 10th Edition"]], "View the XF6"),
        "xr150fc-2": _card("xr150fc-2", "A combined access, burglary and fire panel with a built-in fire command center keyboard.", [["Doors of access", "Up to 8"], ["Keypads", "Up to 7 supervised"]], "View the XR150FC"),
        "xr550fc-2": _card("xr550fc-2", "Integrated intrusion, fire and access control with a fire command center keyboard.", [["Doors of access", _spec("xr550fc-2", "Doors of access")], ["Keypads", "Up to 15 supervised"]], "View the XR550FC"),
    }
    rules = [{"when": [[0], [0]], "res": ["xf6"]}, {"when": [None, [0, 1]], "res": ["xr150fc-2"]}, {"when": [None, None], "res": ["xr550fc-2"]}]
    return {"type": "panelpick", "id": "fit", "alt": True, "eyebrow": "Find your fit", "heading": "Which fire panel fits?",
            "intro": "Choose what the panel has to run. Each suggestion comes from the fire panel pages.", "note": NOTE, "say": "Suggested panel: ",
            "static_label": "The three fire panels",
            "questions": [{"q": "What does the panel run?", "options": ["Fire only", "Fire plus intrusion"]}, {"q": "Doors of access control", "options": ["None", "Up to 8", "Up to 96"]}],
            "rules": rules, "cards": cards,
            "also": [{"text": "Round out the system with a remote annunciator or a pull station.", "label": "See the 630F", "href": "products/630f.html"}]}


def _video_selector():
    cards = {
        "vue-video-doorbell": _card("vue-video-doorbell", "A 5MP video doorbell with AI detection and true video verification for monitoring stations.", [["Resolution", "5MP / 3K"], ["Analytics", "Person, vehicle and package"]], "View the doorbell"),
        "vplus-7061-fe": _card("vplus-7061-fe", "A 6MP fisheye with a 360 degree view, onboard AlarmVision and a microphone. Rated for indoor and outdoor.", [["Resolution", "6MP"], ["Field of view", "360 degrees"], ["Environment", "Indoor and outdoor"]], "View the fisheye"),
        "vplus-7081-bdv": _card("vplus-7081-bdv", "An 8MP varifocal bullet with deterrence lights, a microphone and speaker, and onboard AlarmVision.", [["Resolution", "8MP"], ["IR distance", _spec("vplus-7081-bdv", "IR distance")], ["Environment", "Indoor and outdoor"]], "View the bullet"),
        "v-6022wc": _card("v-6022wc", "A 2-megapixel indoor cube camera with motion event analytics, for small business and retail.", [["Resolution", "2MP"], ["Environment", "Indoor"], ["Field of view", _spec("v-6022wc", "Field of view")]], "View the cube"),
    }
    fe = "The V-6022WC cube is indoor only, so the 6MP fisheye covers the outdoor case. It is rated for indoor and outdoor."
    rules = [{"when": [[2], None], "res": ["vue-video-doorbell"]}, {"when": [None, [0]], "res": ["vplus-7061-fe"]}, {"when": [None, [1]], "res": ["vplus-7081-bdv"]},
             {"when": [[0], [2]], "res": ["v-6022wc"]}, {"when": [[1], [2]], "res": ["vplus-7061-fe"], "why": {"vplus-7061-fe": fe}}, {"when": [None, None], "res": ["v-6022wc"]}]
    return {"type": "panelpick", "id": "fit", "alt": True, "eyebrow": "Find your fit", "heading": "Which camera fits?",
            "intro": "Say where it goes and what matters most. Each suggestion comes from the camera pages.", "note": NOTE, "say": "Suggested camera: ",
            "static_label": "The cameras",
            "questions": [{"q": "Where will it go?", "options": ["Indoors", "Indoors or outdoors", "At the front door"]}, {"q": "What matters most?", "options": ["A 360 degree view", "Long range and deterrence", "A small, simple camera"]}],
            "rules": rules, "cards": cards,
            "also": [{"text": "Want the camera to raise the alarm? XV gateways turn ONVIF and RTSP cameras into smart motion detectors for XT75 and XR panels.", "label": "See the XV gateways", "href": "products/xv-gateways-with-alarmvision.html"},
                     {"text": "Need more detail from a fisheye? The VUE Plus 12MP fisheye has a 1.8 mm focal length.", "label": "See the 12MP fisheye", "href": "products/vplus-7121-fe.html"}]}


def _path(heading, intro, q, opts, say):
    """A 'pick your path' chooser of real product families: opts = [(label, [slugs])]."""
    slugs = []
    for _, ss in opts:
        for x in ss:
            if x not in slugs:
                slugs.append(x)
    return {"type": "panelpick", "id": "fit", "alt": True, "mode": "path", "eyebrow": "Pick your path", "heading": heading, "intro": intro,
            "note": NOTE, "out_label": "Where to start", "static_label": "Every product family", "say": say,
            "questions": [{"q": q, "options": [o[0] for o in opts]}],
            "rules": [{"when": [[i]], "res": ss} for i, (_, ss) in enumerate(opts)],
            "cards": {x: _card(x, "", [], "Open the page") for x in slugs}}


SELECTORS = {
    "intrusion": _panel_selector, "panels-keypads": _panel_selector, "access-control": _access_selector, "fire": _fire_selector, "video": _video_selector,
    "communicators": lambda: _path("Which path does your signal take?", "Choose what you are connecting. Each path starts with the products built for it.", "What are you connecting?",
                                   [("An XT or XR panel over LTE", ["263lte", "263lte-firstnet"]), ("An XTLplus or XTLtouch panel", ["265lte"]),
                                    ("Almost any panel", ["cellcom", "dualcom"]), ("The monitoring center", ["scs-vr-virtual-receiver-software", "scs-1r"])], "Start with: "),
    "wireless": lambda: _path("Which wireless product do you need?", "Choose the job. Each path lists the 1100 Series products that do it.", "What do you need to add?",
                              [("A receiver for the panel", ["1100xh"]), ("A detector or panic device", ["1128", "1164", "1142"]), ("A transmitter for another device", ["1101"]),
                               ("A takeover from another maker", ["1100t"])], "Start with: "),
    "mobile-automation": lambda: _path("Who is the software for?", "Choose who will use it. Each path starts with the product built for them.", "Who is it for?",
                                       [("The building owner", ["virtual-keypad"]), ("The dealer's customers and staff", ["dealer-admin"]), ("Programming panels from a laptop", ["remote-link"])], "Start with: "),
}

FLOWS = {
    "intrusion": {"heading": "From detector to monitoring center, on one platform.", "intro": "Follow the signal. Every step is a DMP product, and each one links to its page.",
                  "nodes": [
                      {"label": "Detect", "when": "Sensors", "text": "Door and window contacts, motion and glassbreak detectors, wired or on 1100 Series wireless.", "chips": [["1100XH receiver", "products/1100xh.html"]]},
                      {"label": "Decide", "when": "Control panel", "text": "The panel decides what the event means. Cancel/Verify false alarm prevention has been a DMP feature since 2007.", "chips": [["XT75", "products/xt75.html"], ["XT50", "products/xt50.html"], ["XR150", "products/xr150.html"], ["XR550", "products/xr550.html"]]},
                      {"label": "Report", "when": "Communicators", "text": "The signal goes out on more than one path. The XR550 supports up to eight communication paths.", "chips": [["263LTE", "products/263lte.html"], ["JamAlert", "products/jamalert.html"]]},
                      {"label": "Respond", "when": "Monitoring center", "text": "A DMP receiver takes the signal at the central station.", "chips": [["SCS-VR", "products/scs-vr-virtual-receiver-software.html"], ["SCS-1R", "products/scs-1r.html"]]},
                      {"label": "Control", "when": "Dealer and owner", "text": "Owners use Virtual Keypad. Dealers program in bulk with Dealer Admin.", "chips": [["Virtual Keypad", "products/virtual-keypad.html"], ["Dealer Admin", "products/dealer-admin.html"]]}]},
    "fire": {"heading": "A fire signal takes the same path as the alarm.", "intro": "Detectors, panel, annunciator and monitoring center, one maker end to end.",
             "nodes": [
                 {"label": "Detect", "when": "Smoke and pull stations", "text": "An addressable smoke detector reports the exact alarm location on the XR LX-Bus.", "chips": [["2W-BLX", "products/2w-blx.html"], ["850 pull station", "products/850.html"], ["1164 wireless", "products/1164.html"]]},
                 {"label": "Decide", "when": "Fire panel", "text": "Three fire panels to choose from, from the XF6 to the XR550FC.", "chips": [["XF6", "products/xf6.html"], ["XR150FC", "products/xr150fc-2.html"], ["XR550FC", "products/xr550fc-2.html"]]},
                 {"label": "Annunciate", "when": "At the door", "text": "A 20-key remote annunciator with a 32-character LCD.", "chips": [["630F", "products/630f.html"]]},
                 {"label": "Report", "when": "Network and cellular", "text": "The XF6 has onboard Ethernet and optional cellular communication to the monitoring center.", "chips": [["XF6", "products/xf6.html"]]},
                 {"label": "Respond", "when": "Monitoring center", "text": "Signals go straight to the monitoring center, the way the alarm does.", "chips": [["SCS-VR", "products/scs-vr-virtual-receiver-software.html"]]}]},
    "video": {"heading": "From camera to alarm to app.", "intro": "AlarmVision analytics let cameras act like smart motion detectors. Here is the path.",
              "nodes": [
                  {"label": "Capture", "when": "Cameras", "text": "VUE Plus cameras, the V-6022WC cube and the video doorbell.", "chips": [["VUE Plus fisheye", "products/vplus-7061-fe.html"], ["Bullet", "products/vplus-7081-bdv.html"], ["Doorbell", "products/vue-video-doorbell.html"]]},
                  {"label": "Analyze", "when": "XV gateways", "text": "Gateways with AlarmVision turn ONVIF and RTSP cameras into smart motion detectors.", "chips": [["XV gateways", "products/xv-gateways-with-alarmvision.html"]]},
                  {"label": "Alarm", "when": "Control panel", "text": "AlarmVision uses analytics to trigger alarms into the panel.", "chips": [["XT75", "products/xt75.html"], ["XR550", "products/xr550.html"]]},
                  {"label": "Manage", "when": "VK VMS", "text": "VK VMS gives 24/7 video management with AlarmVision.", "chips": []},
                  {"label": "View", "when": "One app", "text": "Video next to the alarm in one app.", "chips": [["Virtual Keypad", "products/virtual-keypad.html"]]}]},
    "panels-keypads": {"heading": "One cabinet, one maker, every wall.", "intro": "A keypad on every wall, a panel that fits the building, and the app that already matches.",
                       "nodes": [
                           {"label": "Keypads", "when": "At the door", "text": "From the 7-inch touchscreen to Thinline, a keypad for every wall.", "chips": [["7-inch touchscreen", "products/7-inch-touchscreen-keypad.html"], ["Graphic touchscreen", "products/graphic-touchscreen.html"], ["7000 Series", "products/7000-series.html"]]},
                           {"label": "Panel", "when": "XT, XTL and XR", "text": "Three panel families, so the panel fits the building.", "chips": [["XT50", "products/xt50.html"], ["XTLplus", "products/xtlplus.html"], ["XR550", "products/xr550.html"]]},
                           {"label": "Communicate", "when": "Reporting", "text": "LTE communicators send the signal to the receiver.", "chips": [["263LTE", "products/263lte.html"], ["265LTE", "products/265lte.html"]]},
                           {"label": "Control", "when": "Dealer and owner", "text": "Virtual Keypad for owners, Dealer Admin for dealers.", "chips": [["Virtual Keypad", "products/virtual-keypad.html"], ["Dealer Admin", "products/dealer-admin.html"]]}]},
}


def _system(pg, slug):
    secs = pg["sections"]
    title = pg["crumbs"][-1][0]
    hero = secs[0]
    short = hero["primary"]["label"].split(" for ", 1)[-1]
    cta_label = hero["primary"]["label"]
    # anchors
    ci = _sec_index(secs, lambda s: s["type"] == "cards")
    secs[ci]["id"] = "overview"
    big = _sec_index(secs, lambda s: s["type"] in ("showcase3d", "network"))
    network = secs[big]["type"] == "network"
    fi = _sec_index(secs, lambda s: s["type"] == "faq")
    secs[fi]["id"] = "faq"
    flow = FLOWS.get(slug)
    anchors = [["Overview", "overview"], ["Find your fit", "fit"], ["FAQ", "faq"]]
    if network:
        wi = _sec_index(secs[big + 1:], lambda s: s["type"] == "works")
        secs[big + 1 + wi]["id"] = "products"
        anchors += [["How it works", "range"], ["Products", "products"]]
    else:
        anchors += [["Products", "range"], ["How it works", "how"]]
    # build the middle of the page: hero, subnav, cards, [flow], picker, rest
    ins = []
    if flow and not network:
        ins.append({"type": "flowviz", "id": "how", "dark": True, "eyebrow": "How it connects", "heading": flow["heading"], "intro": flow["intro"], "nodes": flow["nodes"]})
    ins.append(SELECTORS[slug]())
    ci = _sec_index(secs, lambda s: s["type"] == "cards")
    secs[ci + 1:ci + 1] = ins
    order = {s.get("id"): n for n, s in enumerate(secs) if s.get("id")}
    items = [[t, "#" + i] for t, i in sorted(anchors, key=lambda a: order[a[1]])]
    secs.insert(1, {"type": "subnav", "title": title, "items": items, "cta": {"label": cta_label, "href": "for-specifiers.html"}})
    secs.append({"type": "closer", "id": "ready", "eyebrow": "Next step", "heading": f"Ready to design with DMP {short}?",
                 "sub": "Inside Sales supports system design, architects and engineers, pre-sales questions and quotes.",
                 "primary": {"label": hero["primary"]["label"], "href": "for-specifiers.html"}, "secondary": {"label": "Talk to Inside Sales", "href": "contact.html"}})


# ------------------------------------------------------------------ products
SKIP_KEYS = {"Models", "Firmware", "Included"}
ALIAS = {"Zones": "Total zones", "Bank listings": "Listings", "Listing": "Listings"}
OVERRIDE = {"xr550": ["xr150", "xr650"], "xr150": ["xt50", "xr550"], "xt50": ["xr150", "xr550"], "xr650": ["xr550", "xr150"],
            "xtlplus": ["xtltouch", "xt50"], "xtltouch": ["xtlplus", "xt50"], "1101": ["1142"], "1142": ["1101"]}


def _smap(slug):
    out = {}
    for k, v in BY[slug]["specs"]:
        k = ALIAS.get(k, k)
        if k not in SKIP_KEYS and k not in out and not (" " not in k and any(ch.isdigit() for ch in k)):   # model codes are not facts to compare
            out[k] = v
    return out


def _siblings(slug):
    if slug in OVERRIDE:
        return OVERRIDE[slug]
    mine = _smap(slug)
    r = BY[slug]
    kind = lambda x: BY[x]["kicker"].split(",")[0].strip().lower()
    same = lambda x: kind(x) == kind(slug) or (kind(x).split()[-1] == kind(slug).split()[-1] and BY[x]["system"] == r["system"])
    pool = [k for k in r["rel"] if k in BY and same(k)]
    pool += [k for k in BY if BY[k]["system"] == r["system"] and k not in pool and same(k)]
    scored = []
    for k in pool:
        if k == slug:
            continue
        sh = [x for x in mine if x in _smap(k)]
        if len(sh) >= 2:
            scored.append((-len(sh), pool.index(k), k))
    scored.sort()
    return [k for _, _, k in scored[:2]]


def _compare(slug):
    sibs = _siblings(slug)
    if not sibs:
        return None
    cols = [slug] + sibs
    maps = [_smap(c) for c in cols]
    order = []
    for m in maps:
        for k in m:
            if k not in order:
                order.append(k)
    scored = []
    for k in order:
        have = sum(1 for m in maps if k in m)
        if k in maps[0] and have >= 2:
            scored.append((-have, order.index(k), k))
    scored.sort()
    keys = [k for _, _, k in scored[:6]]
    if len(keys) < 2:
        return None
    # keep the table orderly: original order of appearance
    keys.sort(key=order.index)
    rows = [[k, [m.get(k) for m in maps]] for k in keys]
    colinfo = []
    for c in cols:
        r = BY[c]
        colinfo.append({"name": r["short"], "kicker": r["kicker"].split(",")[0], "image": pm.PRODUCTS[c]["image"], "href": f"products/{c}.html",
                        "here": c == slug, "soon": "coming soon" in r["kicker"].lower()})
    return {"type": "compare", "id": "compare", "eyebrow": "Compare", "heading": f"{BY[slug]['short']} next to its closest sibling{'s' if len(sibs) > 1 else ''}",
            "intro": "Specifications as listed on each product page.", "cols": colinfo, "rows": rows,
            "note": "A starting point. A dealer confirms the design." + (" The XR650 is coming soon and not yet orderable." if "xr650" in cols else "")}


def _product(pg, r):
    slug = r["slug"]
    secs = pg["sections"]
    soon = "coming soon" in r["kicker"].lower()
    cmp_ = _compare(slug)
    si = _sec_index(secs, lambda s: s["type"] == "specs")
    if cmp_ is not None:
        at = (si + 1) if si is not None else _sec_index(secs, lambda s: s["type"] == "works")
        secs.insert(at, cmp_)
    wi = _sec_index(secs, lambda s: s["type"] == "works" and s.get("heading") == "Works with")
    if wi is not None:
        w = secs[wi]
        light = pm._stage_kind(pm.PRODUCTS[slug]["image"]) in ("light", "dark")
        secs[wi] = {"type": "connect", "id": "works-with", "dark": cmp_ is not None, "eyebrow": "Works with", "heading": f"Where {'' if r['short'] in ('Entré Lite', 'Entré Enterprise', 'CellCom', 'DualCom', 'TMSentry', 'JamAlert', 'Virtual Keypad', 'Dealer Admin', 'Remote Link') else 'the '}{r['short']} connects",
                    "intro": w.get("intro", ""), "link_label": "Open", "hub": {"name": r["short"], "image": r["image"], "alt": r["alt"], "light": light}, "items": w["items"]}
    bar = {"type": "buybar", "target": "pstage", "name": r["name"], "kicker": r["kicker"], "image": r["image"],
           "spec": {"label": "Spec sheet", "href": "support/documentation.html"}, "ask": {"label": "Ask DMP", "href": "contact.html"}}
    if not soon:
        bar["order"] = {"label": "Order on buy.DMP.com (dealers)", "href": BUY}
    secs.append(bar)


def apply(data):
    by = {p["file"]: p for p in data["pages"]}
    _home(by["index.html"])
    for slug in SELECTORS:
        _system(by[f"services/{slug}.html"], slug)
    for r in pm.RAW:
        pg = by.get(f"products/{r['slug']}.html")
        if pg:
            _product(pg, r)
    return data
