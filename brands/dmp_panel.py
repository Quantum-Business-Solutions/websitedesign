"""Panel pass. Runs last in finalize(), after dmp_dw2.apply. (Showcase was dialled back after round 4: DMP's own look,
with the keypad hero and the zones kept. See scripts/preview_panel.py.)

What it adds (content only; the renderers, CSS and JS live in scripts/preview_panel.py):
  * home page: the keypad hero for Showcase (variants.showcase on the hero), six zone scenes z1..z6 and a compose order per
    direction, so Clean and Press keep their own home and Showcase walks the zones;
  * a system key on every system and product page (page["sys"]) so the three directions can colour-code by system;
  * environment backgrounds (brands/<slug>.assets/env/, AI-generated placeholders until real photography is shot) on the
    industry heroes and the eight system heroes, with video kept for Showcase and switched off for Clean and Press;
  * Press: the "fifty years of firsts" timeline becomes a feature story on the home page.

Every claim is copied from text already in the repo (product pages, the trust page, the home page). Nothing is invented here.
"""

ENV = "assets/env/env-%s-1280.jpg"
# flip: the scene's dark third is on the right, the hero copy sits on the left, so the plate is mirrored (no text in any scene)
SCENES = {
    "school":   ("01-school-corridor", True),
    "lobby":    ("02-office-lobby", False),
    "parking":  ("03-parking-lot", True),
    "hospital": ("04-hospital-entrance", False),
    "server":   ("05-server-aisle", True),
    "retail":   ("06-retail-storefront", True),
    "bank":     ("07-bank-branch", False),
    "campus":   ("08-campus-aerial", False),
    "stair":    ("09-stairwell", True),
    "dock":     ("10-warehouse-dock", False),
}
INDUSTRY_SCENE = {
    "education": "school", "commercial": "lobby", "retail": "retail", "financial-institutions": "bank",
    "healthcare-wellness": "hospital", "industrial-manufacturing": "dock", "storage-units": "dock", "government": "campus",
    "multi-tenant": "stair", "religious-institutions": "lobby", "residential": "school",
}
SYSTEM_SCENE = {
    "intrusion": "parking", "access-control": "lobby", "fire": "stair", "video": "campus", "communicators": "campus",
    "wireless": "school", "panels-keypads": "server", "mobile-automation": "lobby",
}
# page system -> colour key (communicators, wireless and panels-keypads share the intrusion yellow)
SYS_KEY = {
    "intrusion": "intrusion", "communicators": "intrusion", "wireless": "intrusion", "panels-keypads": "intrusion",
    "access-control": "access", "fire": "fire", "video": "video", "mobile-automation": "mobile",
}


def _page(data, f):
    return next((p for p in data["pages"] if p["file"] == f), None)


def _specs(data, f, n=7):
    pg = _page(data, f)
    sp = next((s for s in (pg["sections"] if pg else []) if s["type"] == "specs"), None)
    return [list(x) for x in (sp["items"][:n] if sp else [])]


def _sys(data):
    for pg in data["pages"]:
        f = pg["file"]
        seg = None
        if f.startswith("services/"):
            seg = f.split("/")[1][:-5]
        elif f.startswith("products/"):
            for c in pg.get("crumbs") or []:
                if len(c) > 1 and str(c[1]).startswith("services/"):
                    seg = c[1].split("/")[1][:-5]
        if seg in SYS_KEY:
            pg["sys"] = SYS_KEY[seg]
            pg["sys_page"] = f"services/{seg}.html"


def _env(data):
    def put(pg, scene):
        if not pg:
            return
        hero = pg["sections"][0]
        if hero.get("type") != "hero-layered":
            return
        name, flip = SCENES[scene]
        hero["bg_image"] = ENV % name
        hero["bg_flip"] = flip
        hero["bg_caption"] = "Illustrative scene"
        v = hero.setdefault("variants", {})
        for d in ("clean", "press"):
            v.setdefault(d, {})["hv"] = {}          # the photograph is the sole background in Clean and Press
    for seg, scene in INDUSTRY_SCENE.items():
        put(_page(data, f"industries/{seg}.html"), scene)
    for seg, scene in SYSTEM_SCENE.items():
        put(_page(data, f"services/{seg}.html"), scene)
    put(_page(data, "industries.html"), "campus")


def _home(data):
    home = _page(data, "index.html")
    if not home:
        return
    secs = home["sections"]
    hero = secs[0]
    for s in secs:                                   # compose needs an id on every section
        if not s.get("id"):
            s["id"] = {"partners": "assoc", "newsfeat": "news"}.get(s["type"], s["type"])
    ids = [s["id"] for s in secs]
    if len(set(ids)) != len(ids):
        raise SystemExit("dmp_panel: home page section ids are not unique: %s" % ids)

    hero.setdefault("variants", {})["showcase"] = {
        "type": "pn-hero",
        "eyebrow": ["Springfield, Missouri", "Since 1975"],
        "lines": ["Four systems.", "One platform."],
        "subhead": "Intrusion, access control, fire and video on one platform, made in Springfield, Missouri and sold only through authorized dealers and distributors.",
        "primary": {"label": "Find a dealer", "href": "find-a-dealer.html"},
        "secondary": {"label": "Become a dealer", "href": "support/become-a-dealer.html"},
        "lane": [["Walk the zones", "#z1"], ["Order at buy.DMP.com", "https://buy.dmp.com/dmp/Shop"],
                 ["Technical documentation", "support/documentation.html"], ["Dealer services", "support/dealer-services.html"]],
        "spec": [["Founded", "1975", "Springfield, Missouri"], ["Systems", "04", "Intrusion, access, fire, video"],
                 ["Catalog", "14", "Product categories"], ["Cloud", "SOC 2", "Type II, examined annually"]],
    }

    z = [
        {"type": "pn-zone", "id": "z1", "z": 1, "name": "Intrusion", "meta": "XR550 / Flagship control panel",
         "num": "574", "unit": ["Zones", "96", "Doors"],
         "heading": "The XR550 runs 96 doors and 574 zones.",
         "body": "Our flagship panel integrates intrusion and commercial fire with powerful access control.",
         "slab": {"title": "Spec sheet", "name": "XR550", "items": _specs(data, "products/xr550.html"),
                  "image": "assets/p-xr550-1200-cut.png", "alt": "The DMP XR550 control panel in its open enclosure",
                  "href": "products/xr550.html", "label": "Open the XR550"},
         "notes": [
             {"k": "Hybrid", "title": "XT75", "text": "A hybrid network panel for residential and small to medium business. Intrusion, access control and AlarmVision on one panel.", "href": "products/xt75.html"},
             {"k": "Since 2007", "title": "Cancel/Verify", "text": "False alarm prevention has been a DMP feature since 2007. Video verification and AlarmVision add a second look.", "href": "services/intrusion.html"},
             {"k": "Coming soon", "soon": True, "title": "XR650", "text": "The next XR Series panel and ESX 2026 Best of Show winner. Not yet available to order.", "href": "products/xr650.html"}],
         "more": ["Intrusion systems", "services/intrusion.html"]},
        {"type": "pn-zone", "id": "z2", "z": 2, "name": "Access control", "meta": "Controllers / Readers / Credentials / Software",
         "heading": "Access control from a single door <em>to hundreds.</em>",
         "body": "Access control runs from the cloud-based X1 to Entré software, and Digital Key puts a credential in the phone's mobile wallet.",
         "readout": ["Door 01", "Access granted"],
         "image": "assets/p-dmp-bluetooth-reader-and-mobile-credential-1200-cut.png", "alt": "The DMP SR3 Bluetooth reader",
         "calls": [
             {"title": "X1", "text": "A single-door access controller with an onboard network or Wi-Fi communicator.", "href": "products/x1.html"},
             {"title": "Entré", "text": "96 doors of access control, expandable to 400 doors and 500 panels.", "href": "products/entre-enterprise.html"},
             {"title": "Digital Key", "text": "A secure NFC credential in a smartphone's mobile wallet that works even when the phone is out of power.", "href": "products/digital-key-credential.html"},
             {"title": "SR3 reader", "text": "One reader for phones and 125 kHz prox cards, rated IP67 for harsh environments.", "href": "products/dmp-bluetooth-reader-and-mobile-credential.html"}],
         "more": ["Access control", "services/access-control.html"]},
        {"type": "pn-zone", "id": "z3", "z": 3, "name": "Fire", "meta": "XF6 / Fire control panel",
         "bg": ENV % SCENES["stair"][0], "big": ["24", "V"],
         "heading": "A 24V fire panel that reports straight to the monitoring center.",
         "lcd": ["XF6 FIRE CONTROL PANEL", "SINGLE-SITE APPLICATIONS", "NETWORK + OPTIONAL CELLULAR", "ALL SIGNALS DIRECT TO THE MONITORING CENTER"],
         "lcd_label": "Panel reading: XF6 fire control panel. Single-site applications. Network and optional cellular communications. All signals direct to the monitoring center.",
         "image": "assets/p-xf6-1200-cut.png", "alt": "The red DMP XF6 fire control panel", "href": "products/xf6.html", "label": "Open the XF6",
         "stats": [["500", "Wireless devices, up to"], ["1.7 mi", "Wireless range, up to"], ["UL 864", "10th Edition Listed for wireless"]],
         "more": ["Fire systems", "services/fire.html"]},
        {"type": "pn-zone", "id": "z4", "z": 4, "name": "Video", "meta": "VUE Plus / AlarmVision / VK VMS",
         "heading": "The camera becomes a <em>smart motion detector.</em>",
         "body": "AlarmVision integrates cameras, analytics and XT75 or XR Series control panels in one platform, creating smart motion detectors that trigger panel responses and alarms in real time.",
         "image": "assets/alarmvision-1200.jpg", "alt": "An AlarmVision scenario: two people highlighted in a camera frame",
         "cap": ["AlarmVision", "Analytics active"],
         "path_label": "Signal path",
         "path": [
             {"title": "Camera", "text": "VUE Plus bullet, turret, dome or fisheye.", "image": "assets/p-vplus-7081-bdv-1200-cut-600.png", "href": "products/vplus-7081-bdv.html"},
             {"title": "XV gateway", "text": "AlarmVision analytics read the scene.", "image": "assets/p-xv-gateways-with-alarmvision-1200-cut-600.png", "href": "products/xv-gateways-with-alarmvision.html"},
             {"title": "Panel", "text": "XT75 or XR Series takes it as an alarm.", "image": "assets/xt75-1200-cut-600.png", "href": "products/xt75.html"},
             {"title": "VK VMS", "text": "24/7 video management, with AlarmVision.", "icon": True, "href": "news/vk-vms.html"}],
         "more": ["Video", "services/video.html"]},
        {"type": "pn-zone", "id": "z5", "z": 5, "name": "Mobile", "meta": "Virtual Keypad / Digital Key / Dealer Admin",
         "heading": "The system keypad, <em>on a phone.</em>",
         "body": "Virtual Keypad runs on Android, iPhone and the web, branded with the dealer's logo. Dealer Admin handles mass panel programming and bulk firmware updates. Digital Key puts the credential in the phone's mobile wallet.",
         "image": "assets/p-virtual-keypad-1200-cut.png", "alt": "Virtual Keypad on a laptop, a tablet and a phone",
         "links": [["Virtual Keypad", "products/virtual-keypad.html"], ["Digital Key", "products/digital-key-credential.html"], ["Dealer Admin", "products/dealer-admin.html"]],
         "plate": {"k": "Independent examination", "big": ["SOC 2", "Type II"],
                   "rows": [["Examined", "Annually"], ["By", "A licensed CPA firm"], ["Covers", "Dealer Admin, Virtual Keypad"],
                            ["Hosted", "Tier 4 data center"], ["SOC 3 report", "For public distribution"]],
                   "href": "trust.html", "label": "Trust and security"},
         "more": ["Virtual Keypad and software", "services/mobile-automation.html"]},
        {"type": "pn-zone", "id": "z6", "z": 6, "name": "Dealers", "meta": "Made in Springfield, Missouri",
         "year": "1975",
         "heading": "Made in Springfield since 1975. Sold through authorized dealers.",
         "body": "We make security systems in Springfield, Missouri, with U.S. and global components, and sell them only through authorized dealers and distributors. A building owner starts with a DMP dealer.",
         "ctas": [["Find a dealer", "find-a-dealer.html"], ["Dealer portal preview", "dealer-portal.html"], ["Become a dealer", "support/become-a-dealer.html"]],
         "video": {"mp4": "assets/hero-loop-plant.mp4", "webm": "assets/hero-loop-plant.webm", "poster": "assets/hero-loop-plant-poster.jpg",
                   "label": "The DMP plant floor in Springfield, Missouri", "cap": ["Plant floor", "Springfield, Missouri"]},
         "row": [["Headquarters", "Springfield, Missouri", ""], ["Catalog", "14 product categories", "services.html"],
                 ["Dealer ordering", "buy.DMP.com, 24 hours a day", "https://buy.dmp.com/dmp/Shop"], ["Founded", "1975, by Rick Britton", "about.html"]]},
    ]
    if not z[0]["slab"]["items"]:
        raise SystemExit("dmp_panel: the XR550 specs were not found, so the Z1 spec slab would be empty")
    secs.extend(z)

    order = {s["id"]: s for s in secs}
    showcase = ["hero-layered", "assoc", "z1", "z2", "z3", "z4", "z5", "building", "how", "flagships", "z6", "who", "portal",
                "proof", "made-here", "story", "news", "guides", "faq", "contact", "ready"]
    classic = [i for i in ids]                       # Clean and Press keep the home they had
    for name in showcase:
        if name not in order:
            raise SystemExit(f"dmp_panel: the home page has no section '{name}'")
    home["compose"] = {"showcase": showcase, "clean": classic, "press": classic}

    # Press: fifty years of firsts as a feature story, under an environment cover
    story = order.get("story")
    if story and story.get("type") == "timeline":
        story.setdefault("variants", {})["press"] = {
            "type": "pn-feature", "kicker": "Feature",
            "cover": ENV % SCENES["campus"][0], "cover_caption": "Illustrative scene",
            "quote": "Rick Britton starts developing a central station product at Atlas Security. DMP begins as an R&D department.",
            "quote_by": "1975, Springfield, Missouri",
            "more": ["Read the company story", "about.html#story"]}


def _pitch(data):
    """Hub copy: the three directions now differ in more than register."""
    p = data.get("pitch")
    if not p:
        return
    p["choose_intro"] = ("The words, the pages and the facts are the same in all three. What differs is the idea. Showcase is DMP's own look with a working keypad up front, "
                         "Clean reads like a spec sheet, and Press reads like a magazine. Open each one and tell us which feels like DMP.")
    p["choose_reasons"] = [
        ["Showcase: DMP, with a keypad", "DMP's white header, yellow buttons and mixed-case headlines on light pages. The home page opens on a keypad you can arm and disarm, six colour-coded zones walk the systems, and Scenes and Night shift are the dark cinematic moments."],
        ["Clean: the spec sheet", "White ground, hairline grid, mono labels and tabular numbers. Product names and data first, for dealers and specifiers scanning for a panel or module."],
        ["Press: the magazine", "Serif headlines, full-bleed photo covers, a lead story and fifty years of firsts told as a feature, so a 50-year-old manufacturer reads like the established name it is."]]
    p["alternatives"] = [
        ["Quantum Showcase", "The familiar one: DMP's own look, with a working keypad hero and every system colour-coded."],
        ["Quantum Press", "The wildcard: serif and editorial, with photo covers and feature stories."]]
    notes = [
        "Environment backgrounds on the industry and system heroes are AI-generated placeholders, captioned 'Illustrative scene'. They are not DMP photographs. Replace them with real photography before launch, or approve them as illustrations.",
        "Showcase sets the keypad headline, the large zone numerals and the Scenes and Night shift headlines in Barlow Condensed and small labels in JetBrains Mono, Press headlines in Playfair Display, all open licence (SIL OFL) and self-hosted. Other Showcase headings and body text use the site's own faces. If DMP licenses Gotham for the web, the display face is the first thing to swap.",
        "System colours (intrusion yellow, access green, fire red, video blue, mobile violet) are our proposal, not an existing DMP standard. DMP to confirm or supply its own.",
        "The home-page keypad in Showcase is a demonstration: nothing is armed and no signal is sent. DMP to confirm it is comfortable with a keypad likeness and the wording 'Armed' and 'Disarmed' on a marketing page.",
    ]
    p["confirm"] = list(p.get("confirm", [])) + [n for n in notes if n not in p.get("confirm", [])]
    if p.get("footer"):
        p["footer"] = p["footer"].rstrip() + " Environment scenes behind some headlines are AI-generated placeholders, not DMP photographs."


def apply(data):
    if data.get("slug") != "digital-monitoring-products":
        return data
    _sys(data)
    _env(data)
    _home(data)
    _pitch(data)
    return data
