#!/usr/bin/env python3
"""Claims register: every figure on the rebuilt pages, checked against what the old site and its blog already said.

    python3 scripts/vaf_claims_audit.py [base-url]
Writes brands/vanausdall.claims-register.json and .md. "Supported" means every number in the sentence appears in the old
site's own text; "New" means at least one number does not, so a person has to confirm it before launch. Nothing here
certifies a claim against the outside world: external checks are recorded by hand in brands/vanausdall.claims-verified.json.
"""
import concurrent.futures as cf, html, json, os, re, subprocess, sys, time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = (sys.argv[1] if len(sys.argv) > 1 else "https://50498425.hs-sites.com").rstrip("/")
red = json.load(open(os.path.join(ROOT, "brands/vanausdall.redirects.json"), encoding="utf-8"))
paths = sorted({r["to"].rstrip("/") or "/" for r in red})

old = json.dumps(json.load(open(os.path.join(ROOT, "brands/vanausdall.pages.json"), encoding="utf-8"))) + json.dumps(json.load(open(os.path.join(ROOT, "brands/vanausdall.blog.json"), encoding="utf-8")))
old = html.unescape(old).replace("\\u2019", "'").replace(",", "").lower()
NUM = re.compile(r"\$?\d[\d,]*(?:\.\d+)?\s?(?:%|\+|k\b|m\b|million|billion|hours?|years?|days?|minutes?|sq ft|-point)?", re.I)
SKIP = re.compile(r"\(\d{3}\)|\d{3}-\d{4}|\b\d{5}\b|\b(?:19|20)\d\d\b(?!\s?(?:%|\+))|copyright|©|utm_|px|rem\b", re.I)


def fetch(p):
    h = subprocess.run(["curl", "-s", "-L", "--max-time", "40", f"{BASE}{p}?cb={int(time.time())}"], capture_output=True).stdout.decode("utf-8", "replace")
    return p, h


def text(h):
    m = re.search(r"<main[^>]*>(.*?)</main>", h, re.S | re.I)
    b = m.group(1) if m else h
    b = re.sub(r"<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", b, flags=re.S | re.I)
    b = re.sub(r"</(p|li|h\d|div|section|dd|dt|blockquote|td|tr)>", "\n", b, flags=re.I)
    return html.unescape(re.sub(r"<[^>]+>", " ", b))


def main():
    with cf.ThreadPoolExecutor(8) as ex: pages = dict(ex.map(fetch, paths))
    reg = {}
    for p, h in pages.items():
        if "<title" not in h.lower(): continue
        for line in text(h).split("\n"):
            for s in re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", line).strip()):
                if len(s) < 12 or len(s) > 420 or SKIP.search(s): continue
                nums = [n.strip() for n in NUM.findall(s) if re.search(r"\d", n)]
                nums = [n for n in nums if not re.fullmatch(r"\d{1,2}", n) or re.search(r"[%+$]|hour|year|day|min", n, re.I)]
                if not nums: continue
                key = re.sub(r"\W+", " ", s.lower()).strip()
                e = reg.setdefault(key, dict(claim=s, numbers=nums, pages=[]))
                if p not in e["pages"]: e["pages"].append(p)
    rows = []
    for e in reg.values():
        miss = []
        for n in e["numbers"]:
            core = re.sub(r"[^\d.]", "", n)
            if core and core not in old: miss.append(n)
        e["status"] = "supported" if not miss else "new"; e["unmatched"] = miss; rows.append(e)
    rows.sort(key=lambda r: (r["status"], -len(r["pages"])))
    json.dump(rows, open(os.path.join(ROOT, "brands/vanausdall.claims-register.json"), "w"), indent=1)
    new = [r for r in rows if r["status"] == "new"]
    L = ["# Van Ausdall & Farrar: claims register", "", f"{len(rows)} sentences with figures on {len(pages)} pages. {len(rows) - len(new)} use only numbers the old site already stated; {len(new)} contain a number the old site did not, so VAF confirms them before launch.", "",
         "## Needs confirmation", "", "| Claim | Numbers not on the old site | Pages |", "|---|---|---|"]
    for r in new: L.append(f"| {r['claim'].replace('|', '/')} | {', '.join(r['unmatched'])} | {', '.join(r['pages'][:3])}{' +' + str(len(r['pages']) - 3) if len(r['pages']) > 3 else ''} |")
    L += ["", "## Supported by the old site", "", "| Claim | Pages |", "|---|---|"]
    for r in rows:
        if r["status"] == "supported": L.append(f"| {r['claim'].replace('|', '/')} | {len(r['pages'])} |")
    open(os.path.join(ROOT, "brands/vanausdall.claims-register.md"), "w").write("\n".join(L) + "\n")
    print(f"{len(rows)} claim sentences; supported {len(rows) - len(new)}; need confirmation {len(new)}")


if __name__ == "__main__":
    main()
