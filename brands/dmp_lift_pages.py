"""Creative-director pass over the hub pages (support, partners, audience, blog, products hub).

apply(data) is called from finalize() in digital-monitoring-products.content.py, after every page module has been merged.
It swaps split heroes for the layered video hero and replaces flat card grids with the richer section types
(callboard, tiles, stage sections). Facts, headings and links stay as the page modules wrote them.
"""
IMG = "assets/"
CLIPS = ["hero-signal-1", "hero-signal-2", "hero-loop-hq", "hero-loop-plant", "hero-loop-campus"]


def hl(h, clip, stats=None, card_a=None, card_b=None):
    out = {"type": "hero-layered", "id": "hero-layered", "eyebrow": h.get("eyebrow", ""), "heading": h["heading"], "subhead": h.get("subhead", ""),
           "image": f"{IMG}{clip}-poster.jpg", "image_w": 1600, "image_h": 900,
           "hv": {"src": f"{IMG}{clip}.mp4", "webm": f"{IMG}{clip}.webm", "poster": f"{IMG}{clip}-poster.jpg"}}
    if not card_a and not card_b:
        card_b = {"eyebrow": "Need a person?", "title": "Call Inside Sales", "body": "877-757-4367, 8 a.m. to 5 p.m. Central.", "links": [["Contact DMP", "contact.html"], ["Find a system", "find-a-system.html"]]}
    for k in ("primary", "secondary", "note"):
        if h.get(k):
            out[k] = h[k]
    if stats:
        out["stats"] = stats
    if card_a:
        out["card_a"] = card_a
    if card_b:
        out["card_b"] = card_b
    return out


def _find(page, typ, head=None, nth=0):
    hits = [i for i, s in enumerate(page["sections"]) if s.get("type") == typ and (head is None or (s.get("heading") or "").startswith(head))]
    return hits[nth] if len(hits) > nth else None


def _page(data, f):
    return next((p for p in data["pages"] if p["file"] == f), None)


def _hero(page, clip, stats=None, card_a=None, card_b=None):
    i = _find(page, "hero")
    if i is not None:
        page["sections"][i] = hl(page["sections"][i], clip, stats, card_a, card_b)


def _stage(page, typ, head, on=True, nth=0):
    i = _find(page, typ, head, nth)
    if i is not None:
        page["sections"][i] = {**page["sections"][i], "stage": on, "alt": False}


def apply(data):
    P = lambda f: _page(data, f)
    # ---- support hub
    p = P("support.html")
    if p:
        _hero(p, "hero-signal-1", [["7 to 7", "Technical Support hours, Central"], ["4", "Phone lines, each with its own hours"], ["8", "Days closed in 2026"]])
        i = _find(p, "cards", "Who to call for what")
        if i is not None:
            p["sections"][i] = {"type": "callboard", "alt": True, "eyebrow": "Pick the right line", "heading": "Who to call for what, with hours and email", "items": [
                {"label": "Quotes and system design", "number": "877-757-4367", "text": "Inside Sales: system design, architect and engineer support, pre-sales support, quotes and pricing, and Dealer Direct assistance.", "hours": "8 a.m. to 5 p.m. Central", "email": "InsideSales@DMP.com"},
                {"label": "Installation and programming", "number": "888-436-7832", "text": "Technical Support: installation, programming, troubleshooting and diagnostic issues.", "hours": "7 a.m. to 7 p.m. Central", "email": "TechSupport@DMP.com"},
                {"label": "Orders and shipping", "number": "866-266-2826", "text": "Customer Service: products and ordering, software activations, the Buy Site, shipping and order entry questions.", "hours": "8 a.m. to 6 p.m. Central", "email": "CustomerService@DMP.com"},
                {"label": "Cellular activation", "number": "877-300-8030", "text": "SecureCom Wireless: activation or billing questions. SecureComWireless.com.", "hours": "8 a.m. to 5 p.m. Central", "email": "CustomerService@SecureComWireless.com"}]}
        i = _find(p, "resources", "Fixing something")
        if i is not None:
            s = p["sections"][i]
            imgs = ["tab-intrusion-1200.jpg", "tab-spec-1200.jpg", "team-2021-1200.jpg", "dualsim-1200.jpg"]
            p["sections"][i] = {"type": "tiles", "stage": True, "eyebrow": "Start here", "heading": s["heading"], "intro": s.get("intro", ""),
                                "items": [[it[1], it[2], it[4], IMG + imgs[k]] for k, it in enumerate(s["items"])]}
        _stage(p, "cards", "We are closed on eight days")
    # ---- technical FAQ hub
    p = P("support/tech-faqs.html")
    if p:
        _hero(p, "hero-signal-2", [["8", "Categories of answers"], ["7 to 7", "Technical Support hours, Central"], ["888-436-7832", "Technical Support"]])
        i = _find(p, "resources", "Pick the product family")
        if i is not None:
            s = p["sections"][i]
            im = {"access-control": "tab-access-1200.jpg", "cellular-network-communication": "dualsim-1200.jpg", "control-panel": "xr650-esx-1200.jpg", "keypads": "keypad-722-1200.png",
                  "mobile-platforms": "tab-mobile-1200.jpg", "monitoring-center": "p-scs-1r-1200.png", "video": "tab-video-1200.jpg", "wireless": "sensor-1112-1200.jpg"}
            items = []
            for it in s["items"]:
                slug = it[4].rsplit("/", 1)[-1].replace(".html", "")
                items.append([it[1], it[2], it[4], IMG + im.get(slug, "tab-intrusion-1200.jpg")])
            p["sections"][i] = {"type": "tiles", "eyebrow": "Eight categories", "heading": s["heading"], "intro": s.get("intro", ""), "items": items}
    # ---- documentation
    p = P("support/documentation.html")
    if p:
        _hero(p, "hero-signal-1", [["900+", "Documents in the library"], ["16", "Product categories"], ["1", "Place to look"]])
        _stage(p, "cards", "Which document answers which question")
    # ---- partners
    p = P("partners.html")
    if p:
        _hero(p, "hero-loop-campus", [["6", "Partners with verified integrations"], ["1", "Dealer Admin to connect them"]])
        _stage(p, "cards", "Find it, connect it")
    # ---- audience pages
    p = P("why-dmp.html")
    if p:
        _hero(p, "hero-loop-plant", [["1975", "Founded in Springfield"], ["50", "Years making security systems"], ["SOC 2", "Type II, examined every year"]])
        i = _find(p, "cards", "Four phone lines")
        if i is not None:
            s = p["sections"][i]
            p["sections"][i] = {"type": "callboard", "alt": True, "eyebrow": "Real people", "heading": s["heading"], "items": [
                {"label": "Inside Sales", "number": "877-757-4367", "text": "System design, quotes and pricing.", "hours": "8 a.m. to 5 p.m. Central"},
                {"label": "Technical Support", "number": "888-436-7832", "text": "Installation, programming and troubleshooting.", "hours": "7 a.m. to 7 p.m. Central"},
                {"label": "Customer Service", "number": "866-266-2826", "text": "Products and ordering, software activations, shipping.", "hours": "8 a.m. to 6 p.m. Central"},
                {"label": "SecureCom Wireless", "number": "877-300-8030", "text": "Activation and billing.", "hours": "8 a.m. to 5 p.m. Central"}]}
        _stage(p, "detail", "We started in 1975")
        _stage(p, "detail", "A licensed CPA firm")
    p = P("for-dealers.html")
    if p:
        _hero(p, "hero-loop-hq", [["24/7", "Ordering at buy.DMP.com"], ["3 years", "Warranty on DMP products"], ["7 to 7", "Technical Support hours, Central"]])
        _stage(p, "cards", "What opens when you sign in")
    p = P("for-specifiers.html")
    if p:
        _hero(p, "hero-signal-2", [["7", "Written specs"], ["73", "CAD drawings"], ["900+", "Documents"]])
        _stage(p, "cards", "Four places a specification begins")
    p = P("find-a-dealer.html")
    if p:
        _hero(p, "hero-loop-campus", [["1", "Call to reach a person: 877-757-4367"], ["Only", "Sold through authorized dealers and distributors"]])
    p = P("for-building-owners.html")
    if p:
        _hero(p, "hero-loop-campus", [["4", "Steps from first call to a system you control"], ["6", "Questions that separate a good proposal"], ["11", "Industry pages"]])
        _stage(p, "cards", "Four steps")
    # ---- blog hub
    p = P("blog.html")
    if p:
        _hero(p, "hero-signal-2", [["6", "Questions answered"], ["6", "Articles for review"], ["1", "Short answer at the top of every article"]])
        i = _find(p, "resources", "The articles")
        if i is not None:
            s = p["sections"][i]
            pics = {}
            for q in data["pages"]:
                if q["file"].startswith("blog/") and q["sections"] and q["sections"][0].get("image"):
                    pics[q["file"]] = q["sections"][0]["image"]
            p["sections"][i] = {"type": "tiles", "stage": True, "variant": "mosaic", "eyebrow": "The articles", "heading": s["heading"], "intro": s.get("intro", ""),
                                "items": [[it[1], it[2], it[4], pics.get(it[4], IMG + "tab-spec-1200.jpg")] for it in s["items"]]}
        _stage(p, "cards", "Written for the people")
    # ---- products hub (hero and rhythm only; the wheel and the cards stay as they are)
    p = P("services.html")
    if p:
        _hero(p, "hero-loop-plant", [["8", "Systems, each with its own page"], ["14", "Product categories"], ["24/7", "Dealer ordering at buy.DMP.com"]])
        _stage(p, "detail", "Order any hour")
    return data
