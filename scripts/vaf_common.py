"""Shared helpers for the VAF section mappers (scripts/vaf_map_*.py) and the page builder."""
import html, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORTAL = "50498425"
_AMAP = json.load(open(os.path.join(ROOT, "brands/vanausdall.asset-map.json")))
FALLBACK_HOST = "https://van-ausdall.vercel.app"


def slug_of(file):
    s = re.sub(r"\.html$", "", file)
    return "" if s == "index" else re.sub(r"/index$", "", s)


def href(h):
    """Preview-relative link (contact.html, ../services/x.html#a) -> site path (/contact, /services/x#a)."""
    if not h or h.startswith(("http", "tel:", "mailto:", "#")):
        return h or ""
    h = re.sub(r"^(\.\./)+", "", h)
    frag = ""
    if "#" in h:
        h, frag = h.split("#", 1)
        frag = "#" + frag
    return "/" + slug_of(h) + frag


def A(path):
    """Preview asset path (assets/x-1200.jpg, ../assets/x.jpg) -> HubSpot Files URL ('' if falsy)."""
    if not path:
        return ""
    if path.startswith("http"):
        return path
    p = re.sub(r"^(\.\./)+", "", path).lstrip("/")
    return _AMAP.get(p) or f"{FALLBACK_HOST}/{p}"


def partner_logo(name):
    """'Canon' -> Files URL of the logo VAF already uses on vanausdall.com, or ''."""
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    for k in (s, s + "-logo", {"ricoh": "ricoh", "arctic-wolf": "artic-wolf-logo", "hp": "hp", "microsoft": "microsoft-patner",
                               "mitel": "mitel-logo", "sophos": "sophos-logo", "autotask": "autotask", "datto": "datto"}.get(s, s)):
        if f"partners/{k}" in _AMAP:
            return _AMAP[f"partners/{k}"]
    return ""


def esc(s):
    return html.escape(s or "", quote=False)


def link(h):
    """HubSpot `link` field value."""
    return {"url": {"content_id": None, "type": "EXTERNAL", "href": href(h)}, "open_in_new_tab": False, "no_follow": False}


def image(path, alt="", w=None, h=None):
    """HubSpot `image` field value."""
    d = {"src": A(path), "alt": alt or "", "loading": "lazy"}
    if w:
        d["width"] = w
    if h:
        d["height"] = h
    return d


def rt(s):
    """Plain text -> rich text paragraph (idempotent if it already contains markup)."""
    return s if (not s or "<" in s) else f"<p>{esc(s)}</p>"
