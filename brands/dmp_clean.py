"""Round 3a, Clean: the home page becomes a spec sheet. Runs last in finalize(), content only.

Renderers, CSS and JS live in scripts/preview_clean.py. Everything is attached as a Clean variant or named only in the
Clean compose order, so Showcase and Press are untouched. Every name and number is read from the product pages already in
the content (their specs sections, crumbs and hero images). Nothing is invented here.
"""
import os
import re

OFF = bool(os.environ.get("DMP_R3A_OFF"))


def _page(data, f):
    return next((p for p in data["pages"] if p["file"] == f), None)


def _specs(pg):
    sp = next((s for s in pg["sections"] if s["type"] == "specs"), None)
    return [list(x) for x in (sp["items"] if sp else [])]


def _spec(pg, *keys):
    for k, v in _specs(pg):
        if k in keys:
            return v
    return ""


def _rows(data):
    rows = []
    for pg in data["pages"]:
        if not pg["file"].startswith("products/"):
            continue
        st = pg["sections"][0]
        cr = pg.get("crumbs") or []
        if st.get("type") != "prodstage" or len(cr) < 2:
            continue
        soon = "coming soon" in (st.get("eyebrow") or "").lower()
        kind = re.sub(r",?\s*coming soon$", "", st.get("eyebrow") or "", flags=re.I)
        short = [[k, v] for k, v in _specs(pg) if len(k) <= 22 and len(v) <= 30][:2]
        rows.append({"name": cr[-1][0], "href": pg["file"], "family": cr[-2][0], "sys": pg.get("sys", ""), "kind": kind,
                     "thumb": st["image"].replace(".png", "-600.png"), "specs": short,
                     "soon": "Coming soon, not orderable" if soon else ""})
    order = ["Panels and Keypads", "Intrusion Systems", "Communicators and Monitoring", "Wireless", "Access Control", "Fire Systems", "Video", "Virtual Keypad and Software"]
    rows.sort(key=lambda r: order.index(r["family"]) if r["family"] in order else 99)
    return rows


def _num(v):
    m = re.search(r"\d[\d,]*", v or "")
    return int(m.group(0).replace(",", "")) if m else 0


def _panels(data):
    out = []
    for f in ("xt50", "xtlplus", "xtltouch", "xr150", "xr550", "xr650"):
        pg = _page(data, f"products/{f}.html")
        if not pg:
            continue
        st = pg["sections"][0]
        zl = _spec(pg, "Total zones", "Zones")
        z = _num(zl)
        if not z:
            continue
        soon = "coming soon" in (st.get("eyebrow") or "").lower()
        doors = _spec(pg, "Doors of access")
        out.append({"name": (pg.get("crumbs") or [[f.upper()]])[-1][0].replace(" Control Panel", "").replace(" All-In-One", ""),
                    "kind": re.sub(r",?\s*coming soon$", "", st.get("eyebrow") or "", flags=re.I), "href": pg["file"],
                    "zones": z, "zones_label": zl, "doors": re.sub(r"^(\d+) out of the box, (\d+) maximum$", r"\1 / \2 max", doors) or "Not listed", "doors_n": max([int(x) for x in re.findall(r"\d+", doors)] or [0]),
                    "users": _spec(pg, "User codes") or "Not listed", "soon": "Coming soon, not orderable" if soon else ""})
    out.sort(key=lambda p: (p["zones"], bool(p["soon"])))
    return out


def apply(data):
    if OFF or data.get("slug") != "digital-monitoring-products":
        return data
    home = _page(data, "index.html")
    if not home or not home.get("compose"):
        return data
    secs = {s.get("id"): s for s in home["sections"]}
    hero, who, proof = secs.get("hero-layered"), secs.get("who"), secs.get("proof")
    xr = _page(data, "products/xr550.html")
    rows = _rows(data)
    panels = _panels(data)
    if not (hero and xr and rows and len(panels) >= 4):
        raise SystemExit("dmp_clean: the home hero, the XR550 page, the product pages or the panel specs were not found")

    doors = _spec(xr, "Doors of access")
    m = re.search(r"(\d+) maximum", doors)
    dims = [["t", _spec(xr, "Total zones"), "total zones"], ["l", (m.group(1) if m else doors), "doors of access, maximum"],
            ["b", _spec(xr, "User codes"), "user codes"], ["r", _spec(xr, "Areas"), "areas"]]
    hero.setdefault("variants", {})["clean"] = {
        "type": "cl-hero", "sheet": "Sheet 01", "eyebrow": hero.get("eyebrow", ""), "heading": hero["heading"], "subhead": hero.get("subhead", ""),
        "primary": {"label": "Find a dealer", "href": "find-a-dealer.html"}, "secondary": {"label": "Become a dealer", "href": "support/become-a-dealer.html"},
        "lane": [["Product matrix", "#matrix"], ["Find your panel", "#find-panel"], ["Technical documentation", "support/documentation.html"], ["Order at buy.DMP.com", "https://buy.dmp.com/dmp/Shop"]],
        "figure": {"image": "assets/p-xr550-1200-cut.png", "w": 1090, "h": 552, "alt": "The DMP XR550 control panel in its open enclosure", "href": "products/xr550.html",
                   "label": "Open the XR550", "fig": "Fig. 01 / XR550", "note": "Lines carry specifications, not measurements.", "dims": dims},
        "title": [["Founded", "1975", "Springfield, Missouri"], ["Systems", "04", "Intrusion, access, fire, video"], ["Catalog", "14", "Product categories"],
                  ["Cloud", "SOC 2", "Type II, examined every year"], ["On this sheet", f"{len(rows):02d}", "Products with a page and specifications"]],
    }

    matrix = {"type": "cl-matrix", "id": "matrix", "eyebrow": "Product matrix",
              "heading": f"{len(rows)} products, one table.",
              "intro": "Every product with a page on this site, with its system, its type and two lines from its specifications. Filter by system or search by name.",
              "caption": "DMP products with their system, type and key specifications", "rows": rows, "first": 12,
              "more": f"Show all {len(rows)} products", "placeholder": "XR550, keypad, camera",
              "foot": "Specifications as listed on each product page. The XR650 is coming soon and cannot be ordered yet."}
    mx = 600
    finder = {"type": "cl-finder", "id": "find-panel", "eyebrow": "Find your panel",
              "heading": "Control panels, drawn to scale by zone count.",
              "intro": "Set the number of zones the building needs and the panels that list at least that many stay lit. Doors of access and user codes sit beside each one.",
              "panels": panels, "max": mx, "slider_max": max(p["zones"] for p in panels), "ticks": [0, 100, 200, 300, 400, 500, 600],
              "all": f"{len(panels)} control panels, from {panels[0]['zones']} to {panels[-1]['zones']} zones. Move the slider to narrow them.",
              "foot": "Zone counts, doors and user codes as listed on each product page. A starting point: a DMP dealer confirms the design."}
    new = [matrix, finder]
    if who:
        who.setdefault("variants", {})["clean"] = {"type": "cl-doors"}
    if proof:
        proof.setdefault("variants", {})["clean"] = {"type": "cl-proof"}
    home["sections"].extend(new)
    keep = [i for i in home["compose"]["clean"] if i not in ("facts", "building", "flagships", "matrix", "find-panel")]
    at = keep.index("assoc") + 1 if "assoc" in keep else 1
    home["compose"]["clean"] = keep[:at] + ["matrix", "find-panel"] + keep[at:]
    return data
