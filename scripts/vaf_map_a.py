"""Section mappers, set A: hero, hero-layered, partners, stats, seal, proof, cta, band, values.

REGISTRY = {section type: (module name, mapper)}. mapper(section dict) -> field-name params for the module.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vaf_common import A, esc, image, link, partner_logo


def lnk(h):
    """link() that opens off-site destinations in a new tab."""
    d = link(h)
    if (h or "").startswith("http") and "vanausdall.com" not in h:
        d["open_in_new_tab"] = True
    return d


def _put(out, k, v):
    if v not in (None, "", [], {}):
        out[k] = v


# ------------------------------------------------------------------ hero (+ hero-layered)
def hero(s):
    layered = s["type"] == "hero-layered"
    out = {"layout": "layered" if layered else s.get("layout", "centered")}
    if layered:   # looping background footage (generated, see brands/vanausdall.md) with its poster as first paint
        out["bg_video"] = A("video/hero-loop")
        out["bg_video_webm"] = A("video/hero-loop-webm")
        out["poster"] = image("assets/hero-poster", "")
        out["image"] = image("assets/hero-poster", "")
    _put(out, "anchor", s.get("id"))
    for k in ("eyebrow", "heading", "subhead", "note"):
        v = s.get(k)
        if k == "note" and v and "generated for the preview" in v:
            continue        # preview-only disclaimer, never shown to the client
        _put(out, k, v)
    for k in ("primary", "secondary"):
        if s.get(k):
            out[k + "_label"] = s[k]["label"]
            out[k + "_link"] = lnk(s[k]["href"])
    if s.get("image"):
        w = s.get("image_w", 2100 if layered else 1200)
        h = s.get("image_h", 891 if layered else (800 if out["layout"] == "split" else 675))
        out["image"] = image(s["image"], s.get("image_alt", ""), w, h)
        out["image"]["loading"] = "eager"
    if s.get("poster"):
        out["poster"] = image(s["poster"], "")
    if s.get("video"):
        out["bg_video"] = A(s["video"])
    if s.get("bg"):
        out["bg_color"] = {"color": s["bg"], "opacity": 100}
    if s.get("badge"):
        out["badge_value"] = s["badge"]["value"]
        out["badge_label"] = s["badge"]["label"]
    if s.get("stats"):
        out["stats"] = [{"stat_figure": v, "stat_caption": c} for v, c in s["stats"]]
    if s.get("ribbon"):
        out["ribbon"] = [{"ribbon_text": r} for r in s["ribbon"]]
    a = s.get("card_a")
    if a:
        out.update(card_a_eyebrow=a.get("eyebrow", ""), card_a_title=a.get("title", ""), card_a_body=a.get("body", ""),
                   card_a_items=[{"card_a_item_text": x} for x in a.get("items", [])],
                   card_a_label=a.get("label", ""), card_a_link=lnk(a.get("href", "contact.html")))
    b = s.get("card_b")
    if b:
        out.update(card_b_eyebrow=b.get("eyebrow", ""), card_b_title=b.get("title", ""), card_b_body=b.get("body", ""),
                   card_b_links=[{"card_b_link_label": t, "card_b_link_url": lnk(h)} for t, h in b.get("links", [])])
    # s["variants"] (press direction only) is intentionally not ported.
    return out


# ------------------------------------------------------------------ partners
def _logo(name):
    return partner_logo(name) or partner_logo(name.replace(" ", ""))


def partners(s):
    items = []
    for n in s["items"]:
        items.append({"partner_name": n, "partner_logo": image(_logo(n), n, 150, 52)})
    with_logo = sum(1 for i in items if i["partner_logo"]["src"])
    names_only = s.get("id") == "customers" or with_logo * 2 < len(items)
    out = {"display": "names" if names_only else "logos", "caption": s.get("caption", "Partners"), "items": items}
    _put(out, "anchor", s.get("id"))
    return out


# ------------------------------------------------------------------ shared: anchor, alternate background, tone
def _frame(s, out):
    _put(out, "anchor", s.get("id"))
    if s.get("alt"):
        out["alt_bg"] = True
    if s.get("tone") == "dark":
        out["tone"] = "dark"
    return out


def stats(s):
    return _frame(s, {"items": [{"stat_figure": v, "stat_caption": c} for v, c in s["items"]]})


def seal(s):
    out = {"items": [{"seal_mark": m, "seal_title": t, "seal_text": d} for m, t, d in s["items"]]}
    for k in ("eyebrow", "heading", "intro", "source"):
        _put(out, k, s.get(k))
    return _frame(s, out)


def proof(s):
    out = {"figure": s["value"], "copy": s["text"]}
    for k in ("eyebrow", "source"):
        _put(out, k, s.get(k))
    return _frame(s, out)


def cta(s):
    out = {"heading": s["heading"]}
    _put(out, "subhead", s.get("subhead"))
    if s.get("primary"):
        out["primary_label"] = s["primary"]["label"]
        out["primary_link"] = lnk(s["primary"]["href"])
    return _frame(s, out)


def band(s):
    out = {"items": [{"card_title": t, "card_text": d, "card_link": lnk(h)} for t, d, h in s["items"]]}
    for k in ("eyebrow", "heading", "subhead"):
        _put(out, k, s.get(k))
    return _frame(s, out)


def values(s):
    out = {"items": [{"value_title": t, "value_text": d} for t, d in s["items"]]}
    for k in ("eyebrow", "heading"):
        _put(out, k, s.get(k))
    return _frame(s, out)


REGISTRY = {
    "hero": ("vaf-hero", hero),
    "hero-layered": ("vaf-hero", hero),
    "partners": ("vaf-partners", partners),
    "stats": ("vaf-stats", stats),
    "seal": ("vaf-seal", seal),
    "proof": ("vaf-proof", proof),
    "cta": ("vaf-cta", cta),
    "band": ("vaf-band", band),
    "values": ("vaf-values", values),
}
