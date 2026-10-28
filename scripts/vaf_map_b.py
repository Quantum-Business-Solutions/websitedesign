"""Section mappers, set B: flow, process, timeline, beforeafter, wheel, hotspots, map, tabs, fleet, model3d.

Each mapper takes one content section dict and returns the params for the matching vaf-* module.
"""
import html, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vaf_common import A, esc, href, image, link, partner_logo, rt  # noqa: E402


def nd(s):
    """No em or en dashes anywhere a visitor reads."""
    return (s or "").replace(" — ", ", ").replace(" – ", ", ").replace("—", ", ").replace("–", "-")


def _ul(items):
    return "<ul>" + "".join(f"<li>{esc(nd(i))}</li>" for i in (items or [])) + "</ul>" if items else ""


def _base(s, **extra):
    """Keys every section shares: id -> anchor, alt (background flag) -> alt_bg."""
    d = {"anchor": s.get("id", ""), "alt_bg": s.get("alt") is True}
    d.update(extra)
    return d


def _head(s):
    return {"eyebrow": nd(s.get("eyebrow", "")), "heading": nd(s.get("heading", "")), "intro": nd(s.get("intro", ""))}


# ---------------------------------------------------------------- flow
def m_flow(s):
    out = _base(s, **_head(s))
    if s.get("receive_label"):
        out["receive_label"] = nd(s["receive_label"])
    out["steps"] = [{
        "step_label": nd(st["label"]), "step_when": nd(st.get("when", "")), "step_summary": nd(st.get("summary", "")),
        "step_title": nd(st.get("title", st["label"])), "step_copy": rt(esc(nd(st.get("body", "")))),
        "step_receive": _ul(st.get("receive")),
        "step_produces": nd((st.get("receive") or [""])[0]),
    } for st in s["steps"]]
    # The chart draws a return arrow when the last stage is ongoing: the cycle starts again.
    if "ongoing" in (s["steps"][-1].get("when", "").lower()):
        out["loop_label"] = "Then the cycle begins again"
    return out


# ---------------------------------------------------------------- process
def m_process(s):
    out = _base(s, **_head(s))
    steps = []
    for t, b in s["stages"]:
        b = nd(b)
        m = re.match(r"^Produces:\s*(.*)$", b, re.S)
        if m:
            prod = m.group(1).strip()
            prod = prod[:1].upper() + prod[1:]
            steps.append({"step_title": nd(t), "step_copy": "", "step_produces": prod})
        else:
            steps.append({"step_title": nd(t), "step_copy": rt(esc(b)), "step_produces": ""})
    out["steps"] = steps
    return out


# ---------------------------------------------------------------- timeline
def m_timeline(s):
    out = _base(s, **_head(s))
    out["entries"] = [{"item_year": nd(y), "item_title": nd(t), "item_copy": rt(esc(nd(d)))} for y, t, d in s["items"]]
    return out


# ---------------------------------------------------------------- beforeafter
def m_beforeafter(s):
    b, a = s["before"], s["after"]
    out = _base(s, eyebrow=nd(s.get("eyebrow", "")), heading=nd(s.get("heading", "")))
    out["after_bg"] = {"color": s.get("bg") or "#0f1e33", "opacity": 100}
    out.update({
        "before_eyebrow": nd(b.get("eyebrow", "Before")), "before_title": nd(b["title"]), "before_copy": nd(b.get("body", "")), "before_items": _ul(b.get("items")),
        "after_eyebrow": nd(a.get("eyebrow", "After")), "after_title": nd(a["title"]), "after_copy": nd(a.get("body", "")), "after_items": _ul(a.get("items")),
    })
    if s.get("hint"):
        out["hint"] = nd(s["hint"])
    if s.get("range_label"):
        out["range_label"] = nd(s["range_label"])
    return out


# ---------------------------------------------------------------- wheel
def m_wheel(s):
    out = _base(s, **_head(s))
    out.update({"hub": nd(s.get("hub", "")), "hub_sub": nd(s.get("hub_sub", "")), "ring": nd(s.get("ring", ""))})
    out["pillars"] = [{"pillar_title": nd(it[0]), "pillar_copy": nd(it[1]), "pillar_link": link(it[2]),
                       "pillar_short": nd(it[3] if len(it) > 3 else it[0]),
                       "pillar_chips": nd(it[4]) if len(it) > 4 else "", "pillar_proof": nd(it[5]) if len(it) > 5 else ""} for it in s["items"]]
    return out


# ---------------------------------------------------------------- hotspots
def m_hotspots(s):
    out = _base(s, **_head(s))
    out["image"] = image(s["image"], nd(s.get("alt") if isinstance(s.get("alt"), str) else ""), s.get("image_w"), s.get("image_h"))
    out["pins"] = [{"pin_x": it["x"], "pin_y": it["y"], "pin_kicker": nd(it.get("k", "")), "pin_title": nd(it["title"]),
                    "pin_copy": nd(it.get("body", "")), "pin_link": link(it["href"]), "pin_link_label": nd(it.get("label", "See it"))}
                   for it in s["items"]]
    return out


# ---------------------------------------------------------------- map
def m_map(s):
    out = _base(s, heading=nd(s.get("heading", "")), intro=nd(s.get("intro", "")))
    out["map_alt"] = nd(s["alt"]) if isinstance(s.get("alt"), str) else "Map of Indiana with office locations"
    if s.get("ring") is not None:
        out["ring"] = s["ring"]
    out["offices"] = [{"office_name": nd(it["name"]), "office_sub": nd(it.get("sub", "")), "office_hq": bool(it.get("hq", False)),
                       "office_lon": it["lon"], "office_lat": it["lat"], "office_link": link(it["href"]),
                       "label_dx": it.get("label_dx", 10), "label_dy": it.get("label_dy", 4)} for it in s["items"]]
    return out


# ---------------------------------------------------------------- tabs
def m_tabs(s):
    out = _base(s, **_head(s))
    out["tabs"] = [{"tab_label": nd(it["label"]), "tab_title": nd(it.get("title", it["label"])), "tab_copy": rt(esc(nd(it.get("body", "")))),
                    "tab_bullets": _ul(it.get("bullets")), "tab_image": image(it.get("image"), nd(it.get("image_alt", "")), 800, 600),
                    "tab_link": link(it["href"]) if it.get("href") else link(""), "tab_link_label": nd(it.get("link_label", "Learn more"))}
                   for it in s["items"]]
    return out


# ---------------------------------------------------------------- fleet
def _brands(text):
    """'Canon, Ricoh, EFI Fiery' -> logo images where VAF has a partner logo, plain names where it does not."""
    parts = []
    for b in [x.strip() for x in (text or "").split(",") if x.strip()]:
        logo = partner_logo(b)
        parts.append(f'<img src="{esc(logo)}" alt="{esc(b)}" height="22">' if logo else f"<span>{esc(nd(b))}</span>")
    return "<p>" + " ".join(parts) + "</p>" if parts else ""


def m_fleet(s):
    out = _base(s, heading=nd(s.get("heading", "")), intro=nd(s.get("intro", "")))
    out["devices"] = [{"dev_title": nd(it["title"]), "dev_band": nd(it.get("band", "")), "dev_brands": _brands(it.get("brands")),
                       "dev_image": image(it.get("image"), nd(it.get("alt") if isinstance(it.get("alt"), str) else it["title"]), 600, 600),
                       "dev_bullets": _ul(it.get("bullets")), "dev_link": link(it["href"]), "dev_link_label": nd(it.get("label", "See the product"))}
                      for it in s["items"]]
    return out


# ---------------------------------------------------------------- model3d
# The preview only loads a <model-viewer> when a GLB exists; none does, so this is poster plus link.
_POSTER_ALT = "A white and charcoal multifunction copier on a cabinet"


def m_model3d(s):
    alt = s.get("alt") if isinstance(s.get("alt"), str) else _POSTER_ALT
    out = _base(s, **_head(s))
    out["poster"] = image(s["poster"], nd(alt), 1200, 1200)
    cta = s.get("cta") or {}
    out["cta_label"] = nd(cta.get("label", ""))
    out["cta_link"] = link(cta.get("href", ""))
    if s.get("hint"):
        out["hint"] = nd(s["hint"])
    return out


REGISTRY = {"flow": ("vaf-flow", m_flow), "process": ("vaf-process", m_process), "timeline": ("vaf-timeline", m_timeline),
            "beforeafter": ("vaf-beforeafter", m_beforeafter), "wheel": ("vaf-wheel", m_wheel), "hotspots": ("vaf-hotspots", m_hotspots), "map": ("vaf-map", m_map), "tabs": ("vaf-tabs", m_tabs), "fleet": ("vaf-fleet", m_fleet), "model3d": ("vaf-model3d", m_model3d)}
