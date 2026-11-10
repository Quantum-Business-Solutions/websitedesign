"""Round 2b: tools and new pages. Runs last in finalize(), after the panel pass.

What it adds (content only; the renderers, CSS and JS live in scripts/preview_tools.py):
  * configurator.html   the system configurator: pick system types, see which products on this site are listed under each,
                        tick a shortlist and print a summary. A preview tool: not a quote or an engineering approval.
  * keypad-demo.html    a full page keypad to play with: arm, disarm, trip and bypass demo zones, read the event log.
  * 404.html            the keypad-style not-found page (same heading, links and phone line as before).
  * links to the two new pages from the Products mega menu foot, the footer, the finder, the fit check and the 404.

Where the configurator's facts come from. Nothing is written here:
  * the product list, the system tags and the one-line descriptions are the finder section of find-a-system.html, as built;
  * the three spec chips per product are the chips on that product's own page (prodstage);
  * "stated fit" is cut out of the one-line description with a regular expression ("for all DMP panels",
    "for XT75 and XR panels"). Where the description does not name panels, the tool says "ask your DMP dealer".
Set TK_OFF=1 to switch the whole pass off (used to prove the other pages are unchanged).
"""
import os
import re

SLUG = "digital-monitoring-products"
DISCLAIMER = "Preview tool: not a quote or an engineering approval."

# key, label, colour (the Round 1 system colours), system page
SYSTEMS = [
    ("intrusion", "Intrusion", "#ffd23d", "services/intrusion.html"),
    ("access", "Access control", "#2fd47a", "services/access-control.html"),
    ("fire", "Fire", "#ff5a4d", "services/fire.html"),
    ("video", "Video", "#4aa3ff", "services/video.html"),
    ("mobile", "Mobile and cloud", "#9b87ff", "services/mobile-automation.html"),
]
ADDONS = [
    ("comm", "Communicators", "#8a8f98", "services/communicators.html"),
    ("wireless", "Wireless", "#8a8f98", "services/wireless.html"),
]
FIT = re.compile(r"\b(?:for|to|with) ((?:all DMP|XR|XT\w*|DMP and non-DMP)[\w ,&-]*? panels)\b")


def _page(data, file):
    return next((p for p in data["pages"] if p["file"] == file), None)


def _catalog(data):
    finder_page = _page(data, "find-a-system.html")
    finder = next((s for s in (finder_page or {}).get("sections", []) if s.get("type") == "finder"), None)
    if not finder or not finder.get("products"):
        raise SystemExit("dmp_tools: the finder on find-a-system.html was not found, so the configurator would be empty")
    types = {b["key"]: b["label"] for b in finder["buildings"]}
    out = []
    for pr in finder["products"]:
        pg = _page(data, pr["href"])
        stage = next((s for s in (pg or {}).get("sections", []) if s.get("type") == "prodstage"), {})
        soon = "coming soon" in (pr["name"] + " " + pr["blurb"]).lower()
        m = FIT.search(pr["blurb"])
        kind = pr["buildings"][0]
        out.append({"name": pr["name"], "href": pr["href"], "img": pr.get("img", ""), "blurb": pr["blurb"],
                    "kind": kind, "needs": list(pr["needs"]), "soon": soon,
                    "fit": m.group(1) if m else "", "chips": [list(c) for c in (stage.get("chips") or [])][:3]})
    return types, out


def _configurator(data):
    types, products = _catalog(data)
    xr650 = [p for p in products if "XR650" in p["name"]]
    if any(not p["soon"] for p in xr650):
        raise SystemExit("dmp_tools: the XR650 must be marked coming soon")
    return {
        "file": "configurator.html",
        "title": "System configurator: which DMP products fit | DMP",
        "description": "Pick intrusion, access, fire, video or mobile and see which DMP products on this site are listed under each, with a printable summary. A preview tool, not a quote.",
        "crumbs": [["Home", "index.html"], ["System configurator", "configurator.html"]],
        "schema": [],
        "sections": [
            {"type": "tkcfg", "id": "configure", "eyebrow": "System configurator",
             "heading": "Pick the systems. See what fits.",
             "subhead": "Choose the system types a building needs and the list narrows to the DMP products this site lists under each one. Tick the ones you want and print a one-page summary to take to a DMP dealer.",
             "disclaimer": DISCLAIMER,
             "systems": [list(s) for s in SYSTEMS], "addons": [list(s) for s in ADDONS],
             "types": types, "type_order": ["panels", "keypads", "access", "sensors", "cameras", "comm", "software"],
             "products": products,
             "sources": [["Find a system", "find-a-system.html"], ["All products", "services.html"]]},
            {"type": "faq", "alt": True, "heading": "About this tool",
             "items": [
                 ["Where does the list come from?", "From this site. Each product is shown under the systems the product finder lists it under, with the one-line description and the specifications from its own page. The tool does not add anything of its own."],
                 ["Does a match mean two products work together?", "No. A match means both products are listed under the systems you picked. Where a product description names the panels it is for, the tool repeats it as the stated fit. Where it does not, the tool says to ask your DMP dealer."],
                 ["Is the summary a quote?", "No. It has no prices and no quantities, and it is not an engineering approval. It is a shortlist to take to a DMP dealer, who confirms the design."],
                 ["Can I order the XR650?", "Not yet. The XR650 is coming soon and is not orderable, so the tool lists it for reference only."],
                 ["Who do I talk to next?", "DMP sells through authorized dealers and distributors. A building owner starts with a dealer, and DMP's Inside Sales team helps with system design."]]},
            {"type": "resources", "eyebrow": "Keep going", "heading": "Other ways to find your fit.",
             "items": [["Tool", "Find a system", "Choose a product type, then a system, and see every matching product.", "Find a system", "find-a-system.html"],
                       ["Tool", "Dealer system-fit check", "Fourteen questions on how your setup supports growth.", "Take the check", "assessment.html"],
                       ["Demo", "Keypad demo", "Arm, disarm and trip demo zones on a keypad in the browser. No signal is sent.", "Play with the keypad", "keypad-demo.html"]]},
            {"type": "cta", "alt": True, "heading": "Take the shortlist to a dealer.", "subhead": "A DMP dealer confirms what fits the building and designs the system.",
             "primary": {"label": "Find a dealer", "href": "find-a-dealer.html"}},
        ]}


def _keypad(data):
    names = {p["file"]: p for p in data["pages"]}
    items = []
    for kicker, name, text, label, href in [
            ["Keypad", "7-Inch Touchscreen Keypad", "A 7-inch touchscreen keypad with a proximity reader and a 5MP camera, for all DMP panels.", "See the 7-inch keypad", "products/7-inch-touchscreen-keypad.html"],
            ["Keypad", "5-Inch Touchscreen Keypad", "A 5-inch resistive touchscreen keypad with an interactive arming shield, for all DMP panels.", "See the 5-inch keypad", "products/graphic-touchscreen.html"],
            ["App", "Virtual Keypad", "The customer app for remote arming, alarm verification, schedules, geofences and device control.", "See Virtual Keypad", "products/virtual-keypad.html"]]:
        if href in names:
            items.append([kicker, name, text, label, href])
    return {
        "file": "keypad-demo.html",
        "title": "Keypad demo: arm, disarm and trip a zone | DMP",
        "description": "A keypad to play with in the browser: arm it, disarm it, trip and bypass demo zones and read the event log. A demonstration. No signal is sent.",
        "crumbs": [["Home", "index.html"], ["Keypad demo", "keypad-demo.html"]],
        "schema": [],
        "sections": [
            {"type": "tkplay", "id": "keypad", "eyebrow": "Keypad demo",
             "heading": "Go on. Disarm it.",
             "subhead": "A keypad you can play with. Key in any four digits to disarm, trip a zone, arm it again and watch the event log fill.",
             "demo": "Demo keypad. No signal is sent, and nothing here shows how a real DMP keypad is programmed.",
             "zones": [[1, "Intrusion", "#ffd23d"], [2, "Access", "#2fd47a"], [3, "Fire", "#ff5a4d"], [4, "Video", "#4aa3ff"], [5, "Mobile", "#9b87ff"]],
             "rules": [["Arm", "Press the shield or Arm. A three second exit delay runs, then the site is armed. An open zone stops arming until you restore or bypass it."],
                       ["Trip a zone", "Press Trip on a zone. Armed, it raises an alarm. Disarmed, it only shows as open. In this demo the fire zone raises an alarm at any time."],
                       ["Disarm", "Key in any four digits on the number pad. That disarms the site and silences an alarm."],
                       ["Bypass", "Bypass takes a zone out of the system until you bring it back. A bypassed zone cannot raise an alarm."]]},
            {"type": "resources", "alt": True, "eyebrow": "The real ones", "heading": "The keypads this demo borrows from.", "items": items},
            {"type": "cta", "heading": "Want the real thing on a wall?", "subhead": "DMP keypads are sold and installed by authorized dealers.",
             "primary": {"label": "Find a dealer", "href": "find-a-dealer.html"}},
        ]}


def _nf(data):
    pg = _page(data, "404.html")
    if not pg:
        return
    for i, s in enumerate(pg["sections"]):
        if s.get("type") == "p3nf":
            s = dict(s)
            s["type"] = "tknf"
            s["lcd"] = ["ZONE 404", "PAGE NOT FOUND", "CHECK THE ADDRESS"]
            s["links"] = list(s["links"]) + [["System configurator", "configurator.html"], ["Keypad demo", "keypad-demo.html"]]
            pg["sections"][i] = s


def _links(data):
    for it in data.get("nav", []):
        foot = (it.get("dw_mega") or {}).get("foot")
        if foot and it.get("href") == "services.html" and not any(h == "configurator.html" for _t, h in foot):
            foot.append(["System configurator", "configurator.html"])
    for col in data["brand"].get("footer_columns", []):
        if col.get("title") == "Support and training":
            have = {h for _t, h in col["links"]}
            for t, h in (["System configurator", "configurator.html"], ["Keypad demo", "keypad-demo.html"]):
                if h not in have:
                    col["links"].append([t, h])
    fs = _page(data, "find-a-system.html")
    if fs and not any(s.get("id") == "configurator" for s in fs["sections"]):
        i = next((n for n, s in enumerate(fs["sections"]) if s.get("type") == "finder"), None)
        if i is not None:
            fs["sections"].insert(i + 1, {
                "type": "cta", "alt": True, "id": "configurator", "heading": "Specifying more than one system?",
                "subhead": "Pick intrusion, access, fire, video or mobile together and print a shortlist. " + DISCLAIMER,
                "primary": {"label": "Open the system configurator", "href": "configurator.html"}})
    for file, item in (("assessment.html", ["Tool", "System configurator", "Pick the system types and print a shortlist of the products listed under each.", "Open the configurator", "configurator.html"]),
                       ("services/panels-keypads.html", ["Demo", "Keypad demo", "Arm, disarm and trip demo zones on a keypad in the browser. No signal is sent.", "Play with the keypad", "keypad-demo.html"])):
        pg = _page(data, file)
        res = [s for s in (pg or {}).get("sections", []) if s.get("type") == "resources"]
        if res and not any(x[4] == item[4] for x in res[-1]["items"]):
            res[-1]["items"].append(item)


def _wall(data):
    """Round 4b: the product wall on the Showcase catalogue (services.html). Existing data only: one tile per product page,
    its name from the page's own breadcrumb, its cutout from its own stage, its system from the Round 1 colour key."""
    svc = _page(data, "services.html")
    if not svc or any(s.get("id") == "wall" for s in svc["sections"]):
        return
    labels = {k: (lab, c) for k, lab, c, _h in SYSTEMS}
    items = []
    for pg in data["pages"]:
        if not pg["file"].startswith("products/") or pg.get("sys") not in labels:
            continue
        stage = next((s for s in pg["sections"] if s.get("type") == "prodstage"), None)
        if not stage or not stage.get("image"):
            continue
        soon = "coming soon" in (stage.get("eyebrow", "") + " " + " ".join(map(str, stage.get("fine", [])))).lower() or "not yet orderable" in " ".join(map(str, stage.get("fine", []))).lower()
        items.append({"name": pg["crumbs"][-1][0], "href": pg["file"], "img": stage["image"], "w": stage.get("image_w", 600), "h": stage.get("image_h", 450),
                      "sys": pg["sys"], "soon": soon})
    if not items:
        return
    if any("xr650" in i["href"] and not i["soon"] for i in items):
        raise SystemExit("dmp_tools: the XR650 must be marked coming soon on the product wall")
    order = [k for k, _l, _c, _h in SYSTEMS]
    items.sort(key=lambda i: order.index(i["sys"]))   # stable: keeps the catalogue order inside each system
    used = [k for k in order if any(i["sys"] == k for i in items)]
    wall = {"type": "tkwall", "id": "wall", "eyebrow": "The product wall",
            "heading": f"{len(items)} products, {len(used)} system colours.",
            "intro": "Every product page on this site, ringed in the colour of the system it belongs to. Filter by system, then select a product to open its page.",
            "systems": [[k, labels[k][0], labels[k][1]] for k in used], "items": items}
    at = next((n + 1 for n, s in enumerate(svc["sections"]) if s.get("type") == "wheel"), 1)
    svc["sections"].insert(at, {"type": "pn-none", "id": "wall", "variants": {"showcase": wall}})


def _pitch(data):
    p = data.get("pitch")
    if not p:
        return
    notes = [
        "System configurator: a client-side preview of the custom tool. It only repeats what this site already says: the systems each product is listed under in the finder, its one-line description and its specifications. 'Stated fit' is the panel wording in that description; anything else reads 'ask your DMP dealer'. DMP to supply a real compatibility matrix before this becomes a specifying tool, and to approve the label 'Preview tool: not a quote or an engineering approval'.",
        "Keypad demo page: a demonstration with invented demo rules (a three second exit delay, any four digits disarm, the fire zone alarms at any time). It does not show how a DMP keypad is programmed and no signal is sent. DMP to confirm it is comfortable with a playable keypad likeness.",
        "Printable spec sheets: product pages print as a one-column sheet with the specifications as listed on this site. DMP's own PDF spec sheets remain the reference.",
    ]
    p["confirm"] = list(p.get("confirm", [])) + [n for n in notes if n not in p.get("confirm", [])]


def apply(data):
    if data.get("slug") != SLUG or os.environ.get("TK_OFF"):
        return data
    have = {p["file"] for p in data["pages"]}
    for pg in (_configurator(data), _keypad(data)):
        if pg["file"] not in have:
            data["pages"].append(pg)
    _nf(data)
    _wall(data)
    _links(data)
    _pitch(data)
    return data
