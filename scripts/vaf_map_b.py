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
    } for st in s["steps"]]
    return out


REGISTRY = {"flow": ("vaf-flow", m_flow)}
