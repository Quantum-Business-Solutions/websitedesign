"""Mappers for sections faq, checklist, leadform, contact, calculator, leadership, video, article.

REGISTRY = {"<section type>": ("vaf-<module>", mapper)}; mapper(section) -> params for the module's fields.
"""
import json, math, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vaf_common import ROOT, esc, href, image, link, rt, A

BRAND = json.load(open(os.path.join(ROOT, "brands/vanausdall.content.json"), encoding="utf-8"))["brand"]


def clean(v):
    """No em or en dashes anywhere a visitor reads."""
    if isinstance(v, str):
        return v.replace("—", ", ").replace("–", "-")
    if isinstance(v, list):
        return [clean(x) for x in v]
    if isinstance(v, dict):
        return {k: clean(x) for k, x in v.items()}
    return v


def common(s):
    out = {"alt_bg": bool(s.get("alt"))}
    if s.get("id"):
        out["anchor"] = s["id"]
    return out


def _initials(name, first_last=True):
    words = [w for w in re.findall(r"[A-Za-z0-9]+", name) if w.lower() not in ("the", "and")]
    if not words:
        return ""
    if first_last:
        return (words[0][0] + (words[-1][0] if len(words) > 1 else "")).upper()
    return "".join(w[0] for w in words[:2]).upper()


# ------------------------------------------------------------------ faq
def faq(s):
    out = common(s)
    out.update({"heading": s.get("heading", ""),
                "items": [{"question": q, "answer": rt(a)} for q, a in s["items"]],
                "open_first": True, "schema": True})
    return clean(out)


# ------------------------------------------------------------------ checklist
def checklist(s):
    n = len(s["items"])
    msgs = list(s.get("messages") or [])
    msgs += [""] * (4 - len(msgs))
    # "check what you cannot answer yes to" counts gaps (1, 2, 3+); "check what is true" counts strengths (scaled to the list)
    gaps = "cannot" in (s.get("intro") or "").lower()
    mid, high = (2, 3) if gaps else (max(2, math.ceil(n * 0.4)), max(3, math.ceil(n * 0.8)))
    out = common(s)
    out.update({"eyebrow": s.get("eyebrow", "Is this you?"), "heading": s.get("heading", ""), "intro": s.get("intro", ""),
                "items": [{"item_text": t} for t in s["items"]], "score_noun": "checked",
                "msg_zero": msgs[0], "msg_low": msgs[1], "msg_mid": msgs[2], "msg_high": msgs[3],
                "band_mid": mid, "band_high": high,
                "cta_note": "Ten to fifteen minutes online, then a specialist walks it with you.",
                "cta_label": s.get("cta_label", "Take the assessment"), "cta_link": link(s.get("cta_href", "contact.html"))})
    return clean(out)


# ------------------------------------------------------------------ leadform / contact
def leadform(s):
    out = common(s)
    out.update({"heading": s.get("heading", ""), "copy": s.get("body", ""), "phone_prefix": "Or call",
                "phone_text": BRAND["phone"], "phone_link": link(BRAND["phone_href"]),
                "submit_label": s.get("submit", ""), "note": s.get("note", "")})
    return clean(out)


def contact(s):
    out = common(s)
    out.update({"heading": s.get("heading", ""), "copy": s.get("body", ""),
                "phone_label": "Call " + BRAND["phone"], "phone_link": link(BRAND["phone_href"]), "email": BRAND["email"],
                "topic_label": "What would you like to look at?",
                "topic_options": [{"topic_text": o} for o in s.get("options", [])],
                "submit_label": s.get("submit", ""), "note": s.get("note", "")})
    return clean(out)


# ------------------------------------------------------------------ calculator
def calculator(s):
    r = s.get("rates", {})
    label = re.sub(r"\s*\([^)]*\)\s*$", "", r.get("saving_label", "") or "") or "Potential saving at up to {}%".format(round(r.get("managed_saving", 0.3) * 100))
    out = common(s)
    out.update({"eyebrow": s.get("eyebrow", ""), "heading": s.get("heading", ""), "intro": s.get("intro", ""),
                "mono_cpp": r.get("mono_cpp", 0.018), "color_cpp": r.get("color_cpp", 0.09),
                "minutes_per_device_week": r.get("minutes_per_device_week", 25), "hourly": r.get("hourly", 28),
                "saving_pct": round(r.get("managed_saving", 0.3) * 100), "saving_label": label,
                "note": s.get("note", ""), "cta_label": s.get("cta_label", "Request the free print assessment"),
                "cta_link": link(s.get("cta_href", "contact.html"))})
    return clean(out)


# ------------------------------------------------------------------ leadership
def leadership(s):
    out = common(s)
    out.update({"heading": s.get("heading", ""), "intro": s.get("intro", ""),
                "people": [{"person_name": n, "person_role": r, "person_initials": _initials(n),
                            "person_photo": {"src": "", "alt": "", "loading": "lazy"}} for n, r in s["people"]],
                "orgs_intro": s.get("orgs_intro", ""), "orgs": [{"org_name": o} for o in s.get("orgs", [])]})
    return clean(out)


# ------------------------------------------------------------------ video
def video(s):
    out = common(s)
    out.update({"eyebrow": s.get("eyebrow", ""), "heading": s.get("heading", ""), "intro": s.get("intro", ""),
                "youtube_id": s.get("youtube", ""),
                "poster": image(s["poster"], s.get("alt") if isinstance(s.get("alt"), str) else "", 1280, 720) if s.get("poster") else {"src": "", "alt": "", "loading": "lazy"},
                "video_title": s.get("title", "Video"), "caption": s.get("caption", "")})
    return clean(out)


# ------------------------------------------------------------------ article
def _inline(t):
    """Plain paragraph text -> safe HTML (leave text that already carries markup alone)."""
    return t if "<" in t else esc(t)


def para_html(p):
    """Shorthand paragraph -> real HTML.
    ul:a;;b   ol:a;;b   h3:Title   quote:text   pq:text (pull quote)   callout:Title|text   anything else -> <p>."""
    m = re.match(r"^(ul|ol|h3|quote|pq|callout):(.*)$", p, re.S)
    if not m:
        return f"<p>{_inline(p)}</p>"
    kind, rest = m.group(1), m.group(2)
    if kind in ("ul", "ol"):
        return f"<{kind}>" + "".join(f"<li>{_inline(x.strip())}</li>" for x in rest.split(";;") if x.strip()) + f"</{kind}>"
    if kind == "h3":
        return f"<h3>{_inline(rest.strip())}</h3>"
    if kind == "quote":
        return f"<blockquote><p>{_inline(rest.strip())}</p></blockquote>"
    if kind == "pq":
        return f'<blockquote class="pq"><p>{_inline(rest.strip())}</p></blockquote>'
    title, _, text = rest.partition("|")
    return f'<aside class="callout"><strong>{_inline(title.strip())}</strong>' + (f"<p>{_inline(text.strip())}</p>" if text.strip() else "") + "</aside>"


def article(s):
    author = s.get("author") or {"name": "The VAF team", "role": "Indianapolis, Indiana"}
    out = {"home_label": "Home", "crumb_label": s.get("crumb_label", "Blog"), "crumb_link": link(s.get("crumb_href", "blog.html")),
           "category": s["category"], "heading": s["heading"], "standfirst": s.get("standfirst", ""),
           "author_name": author["name"], "author_role": author.get("role", ""), "author_initials": _initials(author["name"], False),
           "date_label": s.get("date_label", ""), "read_time": s.get("read", ""),
           "hero_image": image(s["image"], s.get("image_alt", ""), 1200, 675) if s.get("image") else {"src": "", "alt": "", "loading": "lazy"},
           "toc_title": "In this guide",
           "chapters": [{"chapter_anchor": c["id"], "chapter_title": c["title"], "chapter_html": "".join(para_html(p) for p in c["paras"])} for c in s["chapters"]],
           "schema": s.get("schema", True)}
    if s.get("id"):
        out["anchor"] = s["id"]
    return clean(out)


REGISTRY = {
    "faq": ("vaf-faq", faq),
    "checklist": ("vaf-checklist", checklist),
    "leadform": ("vaf-leadform", leadform),
    "contact": ("vaf-contact", contact),
    "calculator": ("vaf-calculator", calculator),
    "leadership": ("vaf-leadership", leadership),
    "video": ("vaf-video", video),
    "article": ("vaf-article", article),
}
