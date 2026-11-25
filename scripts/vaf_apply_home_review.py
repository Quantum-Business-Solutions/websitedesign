#!/usr/bin/env python3
"""Apply Brian Courtney's home page review (VAF Homepage Review Change List.xlsx, 25 Nov 2026, rows HOME-01 to HOME-40).

    python3 scripts/vaf_apply_home_review.py            # apply (idempotent: a second run changes nothing)
    python3 scripts/vaf_apply_home_review.py --check    # report what is still left to change

Decision (Shawn, 25 Nov): where a change is sweeping, make it everywhere the same text appears. Text rules run on the source files
(content, overrides, extra pages, customer labels, module defaults, theme code), so the real customer names stay in the source and the
anonymiser keeps describing them at build time. Blog posts are never touched.
HOME-05 (a replacement stat, "wording to come") is not applied: no wording was given."""
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECK = "--check" in sys.argv

TEXT_FILES = (["brands/vanausdall.content.json", "brands/vanausdall.extra-pages.json", "brands/vanausdall.customers.json"]
              + sorted(os.path.relpath(p, ROOT) for p in glob.glob(os.path.join(ROOT, "brands/vanausdall.overrides.*.json")))
              + sorted(os.path.relpath(p, ROOT) for p in glob.glob(os.path.join(ROOT, "themes/vaf/modules/*/fields.json")))
              + sorted(os.path.relpath(p, ROOT) for p in glob.glob(os.path.join(ROOT, "themes/vaf/modules/*/module.html")))
              + ["themes/vaf/js/vaf-assess.js", "scripts/vaf_map_d.py"])

# (id, regex, replacement, rows). Applied to the raw text of every file above. Order matters.
RULES = [
    # HOME-01, 07, 39: Client Service Center -> Customer Care Center
    ("name-ccc", r"Client Service Center", "Customer Care Center", "HOME-01/07/39"),
    # HOME-10: Ricoh out of the brands VAF sells (support resources for existing Ricoh customers stay)
    ("ricoh-1", r"Canon, Ricoh, Kyocera and HP", "Canon, Kyocera and HP", "HOME-10"),
    ("ricoh-2", r"Canon, Ricoh, Kyocera, and HP", "Canon, Kyocera, and HP", "HOME-10"),
    ("ricoh-3", r"Canon, Ricoh, Kyocera, HP", "Canon, Kyocera, HP", "HOME-10"),
    ("ricoh-4", r"Canon, Ricoh, Kyocera or HP", "Canon, Kyocera or HP", "HOME-10"),
    ("ricoh-5", r"Canon, Ricoh, Kyocera", "Canon, Kyocera", "HOME-10"),
    # HOME-09: Process pillar wording (the service pages and the 'Document Conversion Center' name are not renamed)
    ("docscan-1", r"Document management, document conversion, business process and AI", "Document management, document scanning, business process and AI", "HOME-09"),
    ("docscan-2", r"Document management\|Document conversion\|Business process\|AI consulting", "Document management|Document scanning|Business process|AI consulting", "HOME-09"),
    # HOME-11: Elevate in the Communication vendor list
    ("elevate-1", r"\|Mitel, RingCentral, 8x8\"", "|Mitel, RingCentral, 8x8, Elevate\"", "HOME-11"),
    ("elevate-2", r"\"Mitel, RingCentral, 8x8\"", "\"Mitel, RingCentral, 8x8, Elevate\"", "HOME-11"),
    # HOME-12: AI governance in the Information pillar list
    ("aigov-1", r"Managed IT\|Cybersecurity\|Cloud and backup\|vCIO\"", "Managed IT|Cybersecurity|Cloud and backup|vCIO|AI governance\"", "HOME-12"),
    # HOME-27: the named-customers sentence on the Engineering and construction tab
    ("eng-sentence", r" Shiel Sexton, Bowen Engineering and Echo Engineering are on the record\.", "", "HOME-27"),
    # HOME-28: the utility sentence
    ("util", r"Bloomington's utility department and the Town of Bargersville run on VAF content management", "A large utility department and an Indiana town run on VAF content management", "HOME-28"),
    # HOME-32: AI playbook copy
    ("playbook", r"written for Indiana businesses", "written for your business", "HOME-32"),
    # HOME-34: video caption on the home page
    ("video-caption", r"\"intro\": \"Filmed with VAF people at the 75th Street headquarters\.\"", "\"intro\": \"\"", "HOME-34"),
    # HOME-35, 36: response time
    ("response", r"Same-day service for most Indianapolis metro copier calls\.", "Our average response time for copier calls anywhere in Indiana is under 4 hours.", "HOME-35/36"),
    # HOME-37: contact intro
    ("contact-intro", r"Tell us what you run and what is not working\. A person from the Indianapolis office replies to set a time\. Or start with the ten-minute assessment\.",
     "Tell us what you run and what is not working. One of our technology advisors will set up a time to review your situation. Or start with our complimentary assessment.", "HOME-37"),
    # HOME-02, 06, 14, 15, 16, 17, 20, 21 and every other copy of the same time claims
    ("t-sentence-a", r"Ten to fifteen minutes\. (?=Information, print, process and communication, scored)", "", "HOME-02/06"),
    ("t-sentence-b", r"(Three or more is the reason the assessment exists\.) Ten to fifteen minutes gives you the full score\.", r"\1", "HOME-16"),
    ("t-sentence-c", r"Ten to fifteen minutes\. Complimentary\.", "Complimentary.", "HOME-06"),
    ("t-sentence-d", r"Ten to fifteen minutes online\. You can save for later and finish another day\.", "Eighty yes or no questions in eight short steps of ten. Go at your own pace.", "assessment FAQ"),
    ("t-minute-adj", r"the ten to fifteen minute (Technology Strength Assessment|assessment)", r"the \1", "locations"),
    ("t-takes2", r" and takes ten to fifteen minutes, covering", ", covering", "locations"),
    ("t-online-ten", r", ten to fifteen minutes, and a specialist", ", and a specialist", "locations"),
    ("t-comma-then", r", ten to fifteen minutes online, then a specialist", ", then a specialist", "locations"),
    ("t-about", r", about ten to fifteen minutes online\. A specialist", ". A specialist", "services"),
    ("t-default", r"Ten to fifteen minutes\. A person walks", "A person walks", "module default"),
    ("t-start-1", r"Ten to fifteen minutes(?: online)?, then a specialist", "A specialist", "HOME-17/21"),
    ("t-start-2", r"([\.\"]) ten to fifteen minutes(?: online)?, then a specialist", r"\1 A specialist", "HOME-17/21"),
    ("t-colon", r": ten to fifteen minutes(?: online)?, then a specialist", ", then a specialist", "HOME-17/21"),
    ("t-comma-call", r", ten to fifteen minutes online, or call", ", or call", "locations"),
    ("t-on-your", r": ten to fifteen minutes on your devices", ": your devices", "flow"),
    ("t-assess-sentence", r"Ten to fifteen minutes across ", "A free assessment across ", "meta"),
    ("t-in", r" in ten to fifteen minutes(?: online)?(?=[,\. ])", "", "assessment"),
    ("t-takes", r" and takes ten to fifteen minutes to complete", "", "assessment"),
    ("t-when", r"10 to 15 minutes, then a visit", "Then a visit", "HOME-20"),
    ("t-five-about", r" in about five minutes", "", "HOME-14"),
    ("t-five-link", r"Take the five-minute assessment", "Take the assessment", "HOME-15"),
    ("t-ten-min", r"the ten-minute assessment", "the assessment", "contact"),
    ("t-js-lead", r"About 10 to 15 minutes\. ", "", "assessment script"),
    ("t-js-pace", r" &middot; about ' \+ left \+ ' minute' \+ \(left === 1 \? '' : 's'\) \+ ' left", "", "assessment script"),
]

changed_files = {}
counts = {}


def apply_text():
    for f in TEXT_FILES:
        p = os.path.join(ROOT, f)
        if not os.path.exists(p):
            continue
        s = open(p, encoding="utf-8").read()
        o = s
        for rid, rx, rep, _ in RULES:
            s, n = re.subn(rx, rep, s)
            if n:
                counts[rid] = counts.get(rid, 0) + n
        if s != o:
            changed_files[f] = s


def load(f):
    p = os.path.join(ROOT, f)
    raw = changed_files.get(f) or open(p, encoding="utf-8").read()
    d = json.loads(raw)
    for ind in (1, 2, 3, 4):
        for ea in (False, True):
            if json.dumps(json.loads(open(p, encoding="utf-8").read()), indent=ind, ensure_ascii=ea).strip() == open(p, encoding="utf-8").read().strip():
                return d, ind, ea
    raise SystemExit("cannot round-trip " + f)


def save(f, d, ind, ea):
    raw = open(os.path.join(ROOT, f), encoding="utf-8").read()
    changed_files[f] = json.dumps(d, indent=ind, ensure_ascii=ea) + ("\n" if raw.endswith("\n") else "")


STAT = ("Phone systems deployed since 1983",)


def strip_structural(o):
    """Structural edits: HOME-04 stat, HOME-10 Ricoh cards and list items, HOME-12 bullets, HOME-23/24/25 timeline. Returns number of edits."""
    n = 0
    if isinstance(o, list):
        keep = []
        for e in o:
            if isinstance(e, list) and len(e) == 2 and e[1] in STAT and str(e[0]).startswith("4,000"):
                n += 1; continue
            if isinstance(e, dict) and e.get("stat_caption") in STAT:
                n += 1; continue
            if e == "Ricoh" or (isinstance(e, list) and e[:1] == ["Ricoh"] and len(e) == 2):
                n += 1; continue
            keep.append(e)
        if len(keep) != len(o):
            o[:] = keep
        if o == ["Help desk", "Cybersecurity", "Cloud and backup", "vCIO"]:
            o.append("AI governance"); n += 1
        # timeline: [year, title, text] lists
        if o and all(isinstance(e, list) and len(e) == 3 and isinstance(e[0], str) for e in o) and any(e[:2] == ["1983", "Telecom"] for e in o) and not any(e[0] == "1987" for e in o):
            new = {"1987": ["1987", "Copiers", "VAF enters the copier business."],
                   "2015": ["2015", "Document Conversion Center", "VAF opens the Document Conversion Center."],
                   "2016": ["2016", "Print Fulfillment Center", "VAF opens the Print Fulfillment Center."]}
            items = o + list(new.values())
            order = lambda e: (9999 if e[0] == "Today" else int(e[0]))
            o[:] = sorted(items, key=order); n += 3
        for e in o:
            n += strip_structural(e)
    elif isinstance(o, dict):
        if o.get("stat") == "4,000+" and o.get("stat_label") in STAT:
            o["stat"] = ""; o["stat_label"] = ""; n += 1
        if o.get("stat_figure") == "4,000+" and o.get("stat_caption") in STAT:
            pass
        for v in list(o.values()):
            n += strip_structural(v)
    return n


def apply_structural():
    total = 0
    for f in TEXT_FILES:
        if not f.endswith(".json"):
            continue
        d, ind, ea = load(f)
        n = strip_structural(d)
        if n:
            save(f, d, ind, ea); total += n
            counts["structural:" + os.path.basename(f)] = n
    return total


def customers():
    f = "brands/vanausdall.customers.json"
    d, ind, ea = load(f)
    n = 0
    for c in d["customers"]:
        if c.get("label") == "Community Hospital":
            c["label"] = "Regional Hospital"; n += 1
        if c.get("indef") == "a community hospital":
            c["indef"] = "a regional hospital"; n += 1
    if n:
        save(f, d, ind, ea); counts["customers"] = n


def home_map():
    f = "brands/vanausdall.overrides.home.json"
    d, ind, ea = load(f)
    n = 0

    def walk(o):
        nonlocal n
        if isinstance(o, dict):
            if o.get("name") == "Fort Wayne" and o.get("sub") == "1241 N Wells Street":
                o["sub"] = "(260) 432-1547"; n += 1
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(d)
    if n:
        save(f, d, ind, ea); counts["home-map-fort-wayne"] = n


apply_text()
apply_structural()
customers()
home_map()
if CHECK:
    print("still to change:", counts or "nothing")
    sys.exit(0)
for f, s in changed_files.items():
    open(os.path.join(ROOT, f), "w", encoding="utf-8").write(s)
print("files changed:", len(changed_files))
for k, v in sorted(counts.items()):
    print(f"  {k:<42} {v}")
