"""Mappers for set C: detail, cards, services, resources, related, locations, comparison, casestudy, testimonials.

REGISTRY = {"<section type>": ("vaf-<module>", mapper)}; mapper(section) -> params dict (keys = module field names).
Every field is always supplied so a page never inherits example copy from fields.json defaults.
"""
import os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vaf_common import image, link, rt  # noqa: E402

_DASH = re.compile(r"\s*[—–]\s*")


def clean(v):
    """No em or en dashes anywhere a visitor reads (recursive)."""
    if isinstance(v, str):
        return _DASH.sub(", ", v)
    if isinstance(v, list):
        return [clean(x) for x in v]
    if isinstance(v, dict):
        return {k: clean(x) for k, x in v.items()}
    return v


def _lnk(h):
    l = link(h or "")
    if (h or "").startswith("http"):
        l["open_in_new_tab"] = True
    return l


def _common(s):
    return {"anchor": s.get("id", ""), "alt_bg": bool(s.get("alt")), "padding": "normal"}


def detail(s):
    form = s.get("form")
    out = {
        **_common(s),
        "eyebrow": s.get("eyebrow", ""),
        "heading": s.get("heading", ""),
        "copy": rt(s.get("body", "")),
        "bullets": [{"bullet_text": b} for b in s.get("bullets", [])],
        "image": image(s.get("image", ""), s.get("image_alt", ""), 1200, 800),
        "flip": bool(s.get("flip")),
        "show_form": bool(form),
        "form_heading": (form or {}).get("submit", ""),
    }
    return clean(out)


def _card_logo(title):
    """A card named for a partner or brand gets that partner's logo (files already in HubSpot Files)."""
    import re as _re
    from vaf_common import partner_logo
    cands = [title, title.replace(" ", "")] + [x.strip() for x in _re.split(r"\s*[,/&]\s*|\s+by\s+", title)] + [_re.split(r"\s+", title)[0]]
    for cand in cands:
        u = partner_logo(cand)
        if u:
            return {"card_logo": {"src": u, "alt": title + " logo", "loading": "lazy"}}
    return {}


def cards(s):
    return clean({**_common(s), "eyebrow": s.get("eyebrow", ""), "heading": s.get("heading", ""), "markers": "none",
                  "items": [{"card_title": t, "card_copy": b, **_card_logo(t)} for t, b in s.get("items", [])]})


def services(s):
    return clean({**_common(s), "heading": s.get("heading", ""), "intro": s.get("intro", ""), "link_label": "Learn more", "markers": "none",
                  "items": [{"svc_title": t, "svc_copy": b, "svc_link": _lnk(h)} for t, b, h in s.get("items", [])]})


def resources(s):
    return clean({**_common(s), "heading": s.get("heading", ""), "intro": s.get("intro", ""),
                  "items": [{"res_kind": k, "res_title": t, "res_copy": d, "res_cta": lab, "res_link": _lnk(h), "res_image": image("")}
                            for k, t, d, lab, h in s.get("items", [])]})


def related(s):
    return clean({**_common(s), "heading": s.get("heading", "Keep reading"), "intro": s.get("intro", ""), "link_label": "Read more",
                  "items": [{"rel_tag": tag, "rel_title": t, "rel_copy": d, "rel_link": _lnk(h), "rel_image": image(img or "", "", 1200, 675)}
                            for tag, t, d, h, img in s.get("items", [])]})


def showcase(s):
    """Sticky-scroll service panels. Items: dicts with tag, title, copy, bullets (list), stat, stat_label, href, image."""
    return clean({**_common(s), "eyebrow": s.get("eyebrow", ""), "heading": s.get("heading", ""), "intro": s.get("intro", ""), "link_label": s.get("link_label", "Explore the service"),
                  "items": [{"sv_tag": i.get("tag", ""), "sv_title": i["title"], "sv_copy": i.get("copy", ""), "sv_bullets": " | ".join(i.get("bullets", [])),
                             "sv_stat": i.get("stat", ""), "sv_stat_label": i.get("stat_label", ""), "sv_link": _lnk(i.get("href", "")), "sv_image": image(i.get("image", ""), i.get("alt", ""), 1200, 800)}
                            for i in s.get("items", [])]})


def picker(s):
    """Problem router. Items: dicts with problem, service, copy, bullets (list), href."""
    return clean({**_common(s), "eyebrow": s.get("eyebrow", ""), "heading": s.get("heading", ""), "intro": s.get("intro", ""), "link_label": s.get("link_label", "See how we fix it"),
                  "foot_label": s.get("foot_label", ""), "foot_link": _lnk(s.get("foot_href", "")),
                  "items": [{"pk_problem": i["problem"], "pk_service": i["service"], "pk_copy": i.get("copy", ""), "pk_bullets": " | ".join(i.get("bullets", [])), "pk_link": _lnk(i.get("href", ""))} for i in s.get("items", [])]})


def locations(s):
    return clean({**_common(s), "heading": s.get("heading", ""), "intro": s.get("intro", ""), "detailed": bool(s.get("detailed")),
                  "items": [{"loc_name": n, "loc_line1": a1, "loc_line2": a2, "loc_phone": ph, "loc_link": _lnk(h)}
                            for n, a1, a2, ph, h in s.get("items", [])]})


def comparison(s):
    cols = s.get("columns", [])
    rows = []
    for r in s.get("rows", []):
        cells = list(r[1:5]) + [""] * (4 - len(r[1:5]))
        rows.append({"row_title": r[0], "cell_1": cells[0], "cell_2": cells[1], "cell_3": cells[2], "cell_4": cells[3]})
    return clean({**_common(s), "heading": s.get("heading", ""), "intro": s.get("intro", ""), "corner_label": "What to compare",
                  "columns": [{"col_title": c["label"], "col_recommended": bool(c.get("recommended"))} for c in cols],
                  "rec_tag": "Most common", "rows": rows, "note": s.get("note", "")})


def casestudy(s):
    return clean({**_common(s), "eyebrow": s.get("eyebrow", ""), "heading": s.get("heading", ""),
                  "quote_text": s.get("quote", "").strip().strip('"'), "attribution": s.get("attribution", ""),
                  "metrics": [{"m_label": k, "m_value": v, "m_desc": d} for k, v, d in s.get("metrics", [])],
                  "cta_label": "", "cta_link": link(""), "tone": "dark"})


def testimonials(s):
    return clean({**_common(s), "eyebrow": s.get("eyebrow", "What customers say"), "heading": s.get("heading", ""),
                  "layout": "feature" if s.get("layout") == "feature" else "grid",
                  "items": [{"t_quote": q.strip().strip('"'), "t_name": who, "t_org": org} for q, who, org in s.get("items", [])]})


REGISTRY = {
    "picker": ("vaf-picker", picker),
    "showcase": ("vaf-showcase", showcase),
    "detail": ("vaf-detail", detail),
    "cards": ("vaf-cards", cards),
    "services": ("vaf-services", services),
    "resources": ("vaf-resources", resources),
    "related": ("vaf-related", related),
    "locations": ("vaf-locations", locations),
    "comparison": ("vaf-comparison", comparison),
    "casestudy": ("vaf-casestudy", casestudy),
    "testimonials": ("vaf-testimonials", testimonials),
}
