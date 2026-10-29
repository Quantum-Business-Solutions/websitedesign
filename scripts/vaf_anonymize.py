#!/usr/bin/env python3
"""Customer anonymity on the case studies: replaces the eighteen named customers with a plain description everywhere they appear
(page copy, titles, meta, schema, alt text, links and the case study addresses), and drops their logos.

    python3 scripts/vaf_anonymize.py review     # print every changed sentence once, for reading
Switched on by default in scripts/vaf_build.py; set VAF_NAMED_CUSTOMERS=1 to build with the real names again.
The name-to-description table is brands/vanausdall.customers.json.
"""
import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABLE = json.load(open(os.path.join(ROOT, "brands/vanausdall.customers.json"), encoding="utf-8"))
APOS = "['’]"
SENT = re.compile(r"(^|[.!?:]\s+|[\"“(]\s*)$")


def _rx(names):
    return re.compile(r"(?:\b[Tt]he )?(?:" + "|".join(re.escape(n).replace("'", APOS).replace("\\ ", r"\s+") for n in sorted(names, key=len, reverse=True)) + r")(?:" + APOS + r"s)?(?![A-Za-z])")


for c in TABLE["customers"]:
    c["full_rx"] = _rx(c["full"])
    c["short_rx"] = _rx(c.get("short", []))
    c["label_set"] = {x.lower() for x in c["full"] + c.get("short", [])}


def _cap(s, before):
    return s[:1].upper() + s[1:] if SENT.search(before) else s


def _sub(text, c, rx, label=False):
    seen = []
    def r(m):
        poss = m.group(0).endswith(("'s", "’s"))
        first = not seen
        seen.append(1)
        base = c["label"] if label else (c["indef"] if first else c["definite"])
        out = _cap(base, text[:m.start()])
        return out + ("'s" if poss else "")
    return rx.sub(r, text)


def text(s, case_page=False, label=False):
    for x in TABLE.get("strip", []):
        s = s.replace(x, "")
    t = s.strip()
    for c in TABLE["customers"]:
        if t.lower() in c["label_set"]:
            return s.replace(t, c["label"])
    for k, v in TABLE["labels"].items():
        if t == k:
            return s.replace(t, v)
    for c in TABLE["customers"]:
        s = _sub(s, c, c["full_rx"], label)
        if case_page and c.get("short"):
            s = _sub(s, c, c["short_rx"], label)
    for old, new in TABLE["slugs"].items():
        s = s.replace("case-studies/" + old, "case-studies/" + new)
    return re.sub(r"^(?:An?|The) [^.]*? case study, vanausdall\.com$", "VAF customer case study, vanausdall.com", s)


def walk(x, case_page=False, key="", label=False):
    if isinstance(x, str):
        return x if key in ("type", "id", "layout", "module") else text(x, case_page, label)
    if isinstance(x, list):
        return [walk(i, case_page, key, label) for i in x]
    if isinstance(x, dict):
        out = {}
        for k, v in x.items():
            if isinstance(v, str) and ("case/logo-" in v or "case-assets/" in v):   # a customer's logo file; the partner logos are untouched
                continue
            out[k] = walk(v, case_page, k, label)
        return out
    return x


def apply(content):
    """Rewrite content["pages"] in place, case study files included."""
    for pg in content["pages"]:
        f = pg["file"]
        is_case = f.startswith("case-studies/") and f != "case-studies.html"
        case_page = is_case
        short_ok = not f.startswith(("locations", "policies"))
        for k in ("title", "description", "sections", "crumbs", "schema", "compose"):
            if k in pg and k != "compose":
                pg[k] = walk(pg[k], short_ok, "", label=(k == "title"))
        if is_case:
            old = re.sub(r"^case-studies/|\.html$", "", f)
            if old in TABLE["slugs"]:
                new = TABLE["slugs"][old]
                pg["file"] = f"case-studies/{new}.html"
                if new in TABLE.get("titles", {}): pg["title"] = TABLE["titles"][new]
    return content


def review():
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    os.environ["VAF_NAMED_CUSTOMERS"] = "1"
    import glob
    c = json.load(open(os.path.join(ROOT, "brands/vanausdall.content.json"), encoding="utf-8"))
    for _o in sorted(glob.glob(os.path.join(ROOT, "brands/vanausdall.overrides.*.json"))):
        for _file, _ov in json.load(open(_o, encoding="utf-8")).items():
            for _pg in c["pages"]:
                if _pg["file"] == _file:
                    _pg.update({k: v for k, v in _ov.items() if k in ("title", "description", "sections", "crumbs", "schema")})
    seen = set()
    def strs(x, out, key=""):
        if isinstance(x, str): out.append((key, x))
        elif isinstance(x, list): [strs(i, out, key) for i in x]
        elif isinstance(x, dict): [strs(v, out, k) for k, v in x.items()]
    for pg in c["pages"]:
        is_case = pg["file"].startswith("case-studies/")
        out = []; strs({k: pg[k] for k in ("title", "description", "sections", "crumbs", "schema") if k in pg}, out)
        for k, s in out:
            n = text(s, not pg["file"].startswith(("locations", "policies")))
            if n != s and (s, n) not in seen:
                seen.add((s, n)); print(f"[{pg['file']}]\n  - {s[:230]}\n  + {n[:230]}")
    print(len(seen), "changed strings")


if __name__ == "__main__":
    if sys.argv[1:] == ["review"]: review()
