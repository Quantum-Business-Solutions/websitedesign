"""Shared constants and helpers for the Digital Monitoring Products page modules (brands/dmp_pages_*.py).
Import with:  import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from dmp_common import *"""
import os, re, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "digital-monitoring-products.assets")
CLIENT = "Digital Monitoring Products"
SITE = "https://www.dmp.com"
IMG = "assets/"
BUY = "https://buy.dmp.com/dmp/Shop"           # the dealer ordering site is a separate system and stays external
PHONE = "877-757-4367"
CTA = {"label": "Contact DMP", "href": "contact.html"}
LEADFORM = {"type": "leadform", "alt": True, "id": "start", "heading": "Tell us what you are specifying",
            "body": "Say who you are, what the building is and which products you are looking at, and a person will reply.",
            "submit": "Send to DMP", "note": "Inside Sales is 877-757-4367, 8 a.m. to 5 p.m. Central."}
COMMON_FAQ = {
    "who": ["Does DMP sell directly to building owners?", "DMP sells through authorized dealers and distributors. A building owner starts with a dealer, and DMP's inside sales team helps with system design."],
    "where": ["Where is DMP based?", "Digital Monitoring Products is headquartered at 2500 N. Partnership Boulevard, Springfield, Missouri 65803, and has made its products there since 1975."],
    "what": ["What does DMP make?", "Intrusion, access control, fire and video systems, with the communicators, keypads, wireless devices, Virtual Keypad and software that go with them."],
    "usa": ["Is DMP made in the USA?", "DMP says its products are manufactured in the USA with U.S. and global components, in Springfield, Missouri."],
    "person": ["How do I reach a person?", "Inside Sales is 877-757-4367, Technical Support 888-436-7832 and Customer Service 866-266-2826. The support page lists hours and email addresses."],
    "order": ["How do dealers place an order?", "At buy.DMP.com, which takes orders 24 hours a day, or through DMP Customer Service."],
    "soc": ["Is DMP's software independently examined?", "Yes. DMP completes independent SOC 2 Type II examinations annually, by a licensed CPA firm, for Dealer Admin and Virtual Keypad."],
}
def cf(*keys): return [COMMON_FAQ[k] for k in keys]
def desc(text, n=155):
    if len(text) <= n: return text
    cut = text[:n]; return cut[:cut.rfind(" ")].rstrip(",;:") + "."
def brief(text, n=150):
    if len(text) <= n: return text
    cut = text[:n]; i = max(cut.rfind(". "), cut.rfind("! "), cut.rfind("? "))
    return cut[:i + 1] if i > 60 else cut[:cut.rfind(" ")].rstrip(",;:") + "."
def title(name): return f"{name} | {CLIENT}"
def itemlist(name, items):
    """items: [[name, url], ...] -> an ItemList JSON-LD block."""
    return {"@context": "https://schema.org", "@type": "ItemList", "name": name,
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "url": u} for i, (n, u) in enumerate(items)]}
def fetch_image(url, name, alpha=False):
    """Download an image once, write web sizes into the assets folder, return the path to use in a page, e.g. 'assets/xt75-1200.jpg'.
    alpha=True keeps transparency (PNG). Requires Pillow. Re-uses the file if it already exists."""
    from PIL import Image
    ext = "png" if alpha else "jpg"; out1200 = os.path.join(ASSETS, f"{name}-1200.{ext}"); out600 = os.path.join(ASSETS, f"{name}-600.{ext}")
    if not os.path.exists(out1200):
        os.makedirs(ASSETS, exist_ok=True); tmp = os.path.join("/tmp", f"dl-{name}")
        subprocess.run(["curl", "-sS", "-L", "-m", "60", "-o", tmp, url], check=True)
        im = Image.open(tmp)
        for w, o in ((1200, out1200), (600, out600)):
            t = im if im.width <= w else im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
            (t.convert("RGBA") if alpha else t.convert("RGB")).save(o, optimize=True, **({} if alpha else {"quality": 82}))
    return f"{IMG}{name}-1200.{ext}"
