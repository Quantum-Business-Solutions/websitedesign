"""Round 2a, Showcase home page only: two scroll pieces after the zones.

  scenes   six pinned places, one product in each (renderer: scripts/preview_scenes.py)
  night    one illustrated building after dark, eight products on duty, a test alarm to run (scripts/preview_night.py)

Runs after dmp_panel.apply in finalize(). Clean and Press are not touched: their compose lists were fixed by dmp_panel
before these two sections existed, so neither direction renders them.

Every product fact below is copied from text already in the repo (product cards and spec tables in
digital-monitoring-products.content.py and dmp_pages_*.py, and the zone scenes in dmp_panel.py). The places are
illustrations and say so. The test alarm has no time, address, zone number, person or cause: it only shows which
product category does which job. XR650 appears once, as coming soon and not orderable.
"""

ENV = "assets/env/env-%s-1280.jpg"

SCENES = [
    {"place": "School corridor", "system": "Intrusion, fire and access", "side": "r", "leak": [16, 6],
     "env": ENV % "01-school-corridor", "env_alt": "Illustrative scene: an empty school corridor at dusk, lockers lit by amber ceiling lights",
     "image": "assets/p-xr550-1200-cut.png", "size": [1090, 552], "alt": "The DMP XR550 control panel with its enclosure door open",
     "label": "XR550 control panel", "href": "products/xr550.html",
     "heading": "<em>96</em> doors and <em>574</em> zones on one panel.",
     "body": "Our flagship panel integrates intrusion and commercial fire with powerful access control.",
     "stats": [["10,000", "User codes"], ["AES", "Encrypted communication options"], ["XR650", "Coming soon, not orderable", True]],
     "links": [["Open the XR550", "products/xr550.html"]],
     "caption": "Illustrative scene. XR550 shown with its enclosure door open."},
    {"place": "Office lobby", "system": "Access control", "side": "l", "leak": [78, 4],
     "env": ENV % "02-office-lobby", "env_alt": "Illustrative scene: an office lobby at night with glass doors and amber pendant lights",
     "image": "assets/p-x1-1200-cut.png", "size": [562, 612], "alt": "The DMP X1 single-door access controller with its enclosure open",
     "label": "X1 access controller", "href": "products/x1.html",
     "heading": "One door, run <em>from the cloud.</em>",
     "body": "The X1 Series is our stand-alone, cloud-based access control solution. The X1 is a single-door access controller with an onboard network or Wi-Fi communicator.",
     "stats": [["2021", "X1 Series introduced"], ["2", "Reader inputs, in and out"], ["OSDP", "And Wiegand reader protocols"]],
     "links": [["Open the X1", "products/x1.html"]],
     "caption": "Illustrative scene. X1 shown with its enclosure open."},
    {"place": "Parking lot", "system": "Video", "side": "r", "leak": [10, 30],
     "env": ENV % "03-parking-lot", "env_alt": "Illustrative scene: a rain-wet parking lot at night under amber lamp posts",
     "image": "assets/p-vplus-7081-bdv-1200-cut.png", "size": [665, 379], "alt": "The DMP VUE Plus 8MP Varifocal Bullet camera",
     "label": "VUE Plus 8MP Varifocal Bullet", "href": "products/vplus-7081-bdv.html",
     "heading": "A camera that works as a <em>smart motion detector.</em>",
     "body": "A motorized varifocal lens, two-way audio and red and blue deterrence lights. AlarmVision integrates cameras, analytics and XT75 or XR Series control panels in one platform.",
     "stats": [["8MP", "Resolution"], ["70 m", "IR distance"], ["3.6 to 11", "Millimeter focal length"]],
     "links": [["Open the camera", "products/vplus-7081-bdv.html"]],
     "caption": "Illustrative scene. Not a customer installation."},
    {"place": "Server aisle", "system": "Communication and cloud", "side": "r", "leak": [24, 0],
     "env": ENV % "05-server-aisle", "env_alt": "Illustrative scene: a dark server room aisle with blue and amber status lights",
     "image": "assets/p-263lte-1200-cut.png", "size": [570, 799], "alt": "The DMP 263LTE cellular communicator board with its antenna",
     "label": "263LTE, component view", "href": "products/263lte.html",
     "heading": "Straight to the receiver. <em>No NOC between.</em>",
     "body": "The 263LTE is an AT&T and Verizon cellular communicator for XT and XR Series panels. Dealer Admin and Virtual Keypad are hosted within a Tier 4 data center.",
     "stats": [["SOC 2", "Type II, examined annually"], ["Tier 4", "Data center"], ["LTE", "AT&T and Verizon"]],
     "links": [["Open the 263LTE", "products/263lte.html"], ["Trust and security", "trust.html"]],
     "caption": "Illustrative scene. Component view, not rack hardware."},
    {"place": "Bank branch", "system": "Fire", "side": "l", "leak": [70, 10],
     "env": ENV % "07-bank-branch", "env_alt": "Illustrative scene: a bank branch after hours with brass desk lamps and wood counters",
     "image": "assets/p-xf6-1200-cut.png", "size": [1016, 920], "alt": "The red DMP XF6 fire control panel",
     "label": "XF6 fire control panel", "href": "products/xf6.html",
     "heading": "A <em>24V fire panel,</em> listed for wireless.",
     "body": "An addressable 24V fire panel for single-site applications, with network and optional cellular communications that send all signals direct to the monitoring center.",
     "stats": [["500", "Wireless devices, up to"], ["1.7 mi", "Wireless range, up to"], ["UL 864", "10th Edition Listed for wireless"]],
     "links": [["Open the XF6", "products/xf6.html"]],
     "caption": "Illustrative scene. Not a customer installation."},
    {"place": "Campus", "system": "Virtual Keypad and software", "side": "l", "leak": [82, 20],
     "env": ENV % "08-campus-aerial", "env_alt": "Illustrative scene: an aerial view of a business campus at dusk with lit windows",
     "image": "assets/p-virtual-keypad-1200-cut.png", "size": [1200, 682], "alt": "Virtual Keypad on a laptop, a tablet and a phone",
     "label": "Virtual Keypad", "href": "products/virtual-keypad.html",
     "heading": "The system, lights, locks and cameras <em>in one app.</em>",
     "body": "Virtual Keypad runs on Android, iPhone and the web, branded with the dealer's logo. We sell only through authorized dealers and distributors.",
     "stats": [["1975", "Founded in Springfield, Missouri"], ["2011", "Virtual Keypad introduced"], ["2018", "Rebuilt for iOS and Android"]],
     "links": [["Open Virtual Keypad", "products/virtual-keypad.html"], ["Find a dealer", "find-a-dealer.html"]],
     "caption": "Illustrative scene. Devices shown for illustration."},
]

P = "assets/p-%s-1200-cut-600.png"
POINTS = [
    {"k": "roof", "chip": "Roof", "where": "Roof", "name": "263LTE", "kind": "LTE cellular communicator", "image": P % "263lte", "alt": "The DMP 263LTE cellular communicator",
     "fact": "AT&T and Verizon cellular communicator for XT and XR Series panels.", "href": "products/263lte.html"},
    {"k": "stair", "chip": "Stairwell", "where": "Stairwell", "name": "XF6", "kind": "Fire control panel", "image": P % "xf6", "alt": "The DMP XF6 fire control panel",
     "fact": "An addressable 24V fire panel with network or optional cellular reporting.", "href": "products/xf6.html"},
    {"k": "win", "chip": "Windows", "where": "Windows", "name": "1128", "kind": "Wireless glassbreak detector", "image": P % "1128", "alt": "The DMP 1128 wireless glassbreak detector",
     "fact": "Detects glassbreak up to 20 feet from framed glass in an outside wall.", "href": "products/1128.html"},
    {"k": "door", "chip": "Main door", "where": "Main door", "name": "X1", "kind": "Single-door access controller", "image": P % "x1", "alt": "The DMP X1 access controller",
     "fact": "A single-door access controller with an onboard network or Wi-Fi communicator.", "href": "products/x1.html"},
    {"k": "panel", "chip": "Panel room", "where": "Panel room", "name": "XR550", "kind": "Flagship control panel", "image": P % "xr550", "alt": "The DMP XR550 control panel",
     "fact": "96 doors, 574 zones and 10,000 user codes, with encrypted communication options.", "href": "products/xr550.html"},
    {"k": "side", "chip": "Side entrance", "where": "Side entrance", "name": "Digital Key", "kind": "Mobile credential", "image": P % "digital-key-credential", "alt": "A Digital Key credential on a phone",
     "fact": "A secure NFC credential in a smartphone's mobile wallet that works even when the phone is out of power.", "href": "products/digital-key-credential.html"},
    {"k": "gate", "chip": "Parking gate", "where": "Parking gate", "name": "VUE Plus 8MP Varifocal Bullet", "kind": "Bullet camera", "image": P % "vplus-7081-bdv", "alt": "The DMP VUE Plus bullet camera",
     "fact": "A motorized varifocal lens, two-way audio and red and blue deterrence lights.", "href": "products/vplus-7081-bdv.html"},
    {"k": "phone", "chip": "Phone", "where": "On a phone", "name": "Virtual Keypad", "kind": "App for the system's users", "image": P % "virtual-keypad", "alt": "Virtual Keypad on a laptop, a tablet and a phone",
     "fact": "Live camera footage and Real Alarm or False Alarm confirmation on a phone, tablet or computer.", "href": "products/virtual-keypad.html"},
]

NIGHT = {
    "type": "pn-night", "id": "night",
    "eyebrow": "Protect the whole building", "heading": ["Night", "shift"],
    "lede": "Eight products on duty in one building. Pick a glowing point to see what works there, then run a test alarm.",
    "caption": "Run a test alarm to follow one signal from a window to a phone.",
    "steps": [
        ["Trip", "The demonstration trips a glassbreak detector."],
        ["Detect", "The 1128 detects glassbreak up to 20 feet from framed glass in an outside wall."],
        ["Decide", "The panel decides what the event means."],
        ["Send", "The 263LTE carries the alarm over LTE to the monitoring center receiver, with no NOC between."],
        ["Verify", "Virtual Keypad asks \"Is This A False Alarm?\" and, if cameras are on the system, shows live footage."],
        ["Resolve", "Cancel/Verify false alarm prevention has been a DMP feature since 2007."]],
    "points": POINTS,
    "note": "Illustrative scene. Demonstration only, no signal is sent.",
}

SCENES_SECTION = {
    "type": "pn-scenes", "id": "scenes",
    "eyebrow": "Scenes", "heading": "Six places <em>our products work.</em>",
    "lede": "A school corridor, an office lobby, a parking lot, a server aisle, a bank branch and a campus, each with the DMP product that belongs there.",
    "scenes": SCENES,
}

AFTER = "z6"          # the last zone: the two pieces follow the walk through the zones


def apply(data):
    if data.get("slug") != "digital-monitoring-products":
        return data
    home = next((p for p in data["pages"] if p["file"] == "index.html"), None)
    comp = (home or {}).get("compose") or {}
    order = comp.get("showcase")
    if not home or not order or AFTER not in order:
        raise SystemExit("dmp_night: the Showcase home page has no compose order with '%s' (dmp_panel must run first)" % AFTER)
    have = {s.get("id") for s in home["sections"]}
    files = {p["file"] for p in data["pages"]}
    for sec in (SCENES_SECTION, NIGHT):
        if sec["id"] in have:
            raise SystemExit("dmp_night: the home page already has a section '%s'" % sec["id"])
        for it in sec.get("scenes", []) + sec.get("points", []):
            for h in [it["href"]] + [l[1] for l in it.get("links", [])]:
                if h not in files:
                    raise SystemExit("dmp_night: '%s' links to a page that does not exist: %s" % (sec["id"], h))
        home["sections"].append(sec)
    i = order.index(AFTER) + 1
    comp["showcase"] = order[:i] + ["scenes", "night"] + order[i:]
    p = data.get("pitch")
    if p:
        note = ("Showcase home page: the six 'Scenes' and the 'Night shift' building are illustrations, captioned as such, and the test alarm is a "
                "demonstration with no real event behind it. DMP to confirm it is comfortable with an alarm walk-through on a marketing page.")
        if note not in p.get("confirm", []):
            p["confirm"] = list(p.get("confirm", [])) + [note]
    return data
