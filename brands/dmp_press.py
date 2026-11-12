"""Round 3a, Press: the home page becomes a magazine. Runs last in finalize(), content only.

Renderers and CSS live in scripts/preview_press.py. Everything is attached as a Press variant or named only in the Press
compose order, so Showcase and Clean are untouched. Headlines, dates, milestones and quotations are read from the pages
already in the content (the home page, the news stories and their attributed quotes). Nothing is invented here.
"""
import os

OFF = bool(os.environ.get("DMP_R3A_OFF"))
# attributed quotations on the news stories, in the order they run on the spread (the first is the large one)
QUOTES = ["news/vue-portfolio.html", "news/vk-vms.html", "news/xr650-esx-award.html", "news/vault.html"]


def _page(data, f):
    return next((p for p in data["pages"] if p["file"] == f), None)


def _quote(data, f):
    pg = _page(data, f)
    q = next((s for s in (pg["sections"] if pg else []) if s.get("type") == "proof" and s.get("value") and "," in (s.get("source") or "")), None)
    if not q:
        return None
    name, role = q["source"].split(",", 1)
    title = ((pg.get("crumbs") or [[""]])[-1][0]) or pg.get("title", "")
    return {"value": q["value"], "text": q.get("text", ""), "name": name.strip(), "role": role.strip(), "source": q["source"],
            "href": f, "from": "Read the story: " + title if title else "Read the story"}


def apply(data):
    if OFF or data.get("slug") != "digital-monitoring-products":
        return data
    home = _page(data, "index.html")
    if not home or not home.get("compose"):
        return data
    secs = {s.get("id"): s for s in home["sections"]}
    hero, news, story, made = secs.get("hero-layered"), secs.get("news"), secs.get("story"), secs.get("made-here")
    quotes = [q for q in (_quote(data, f) for f in QUOTES) if q]
    if not (hero and news and story and made and len(quotes) >= 3):
        raise SystemExit("dmp_press: the home hero, news, story, made-here sections or the attributed news quotes were not found")

    lead = news["items"][0]
    hero.setdefault("variants", {})["press"] = {
        "type": "pr-cover", "name": data.get("client", "Digital Monitoring Products"),
        "issue": ["Springfield, Missouri", "Making security systems since 1975", "Sold through authorized dealers"],
        "kicker": "Cover story", "heading": hero["heading"], "subhead": hero.get("subhead", ""),
        "primary": {"label": "Find a dealer", "href": "find-a-dealer.html"}, "secondary": {"label": "Become a dealer", "href": "support/become-a-dealer.html"},
        "image": "assets/hero-hq-dark-2100.jpg", "alt": "The DMP headquarters building in Springfield, Missouri",
        "credit": "Photograph: DMP headquarters, Springfield, Missouri", "toc_label": "Inside",
        "lines": [["News", lead[1], "", "#news"],
                  ["Feature", story.get("eyebrow", "Fifty years of firsts"), story.get("heading", ""), "#story"],
                  ["Voices", "In their own words", "Quotations from this year's announcements.", "#voices"],
                  [made.get("eyebrow", "Made in Springfield"), made["heading"], "", "#made-here"]],
    }
    vk = next((q for q in quotes if q["href"] == lead[4]), None)
    news.setdefault("variants", {})["press"] = {"type": "pr-lead", "side_label": "Also in the news",
                                                "quote": vk, "more": ["All news", "news.html"] if _page(data, "news.html") else None}
    spread = [q for q in quotes if q is not vk] if vk else quotes
    voices = {"type": "pr-quotes", "id": "voices", "eyebrow": "Voices", "heading": "In their own words", "quotes": spread}
    home["sections"].append(voices)
    v = story.setdefault("variants", {})
    old = v.get("press") or {}
    v["press"] = {"type": "pr-feature", "kicker": old.get("kicker", "Feature"), "cover": old.get("cover", "assets/env/env-08-campus-aerial-1280.jpg"),
                  "cover_caption": old.get("cover_caption", "Illustrative scene"), "more": old.get("more", ["Read the company story", "about.html#story"])}

    cur = [i for i in home["compose"]["press"] if i not in ("facts", "flagships", "proof", "news", "story", "voices")]
    order = ["hero-layered", "news"] + [i for i in cur if i != "hero-layered"]
    at = order.index("made-here") + 1 if "made-here" in order else len(order)
    order = order[:at] + ["voices"] + order[at:]
    at = order.index("how") + 1 if "how" in order else 3
    order = order[:at] + ["story"] + order[at:]
    home["compose"]["press"] = order
    return data
