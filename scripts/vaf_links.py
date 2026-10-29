"""Internal linking for the VAF build: related-link directories and blog tag modules added to pages as they are built.

extra_sections(page, pages) -> list of section dicts (types "linkcloud" and "blogrel") to insert before the FAQ.
The graph comes from the site itself: pillar membership from the solutions page, industry and case study categories from the pages."""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PILLAR_PAGES = {"Information": "solutions-information.html", "Communication": "solutions-communication.html",
                "Print": "services/copy-print-solutions.html", "Process": "solutions-process.html"}
INDUSTRY_PAGES = {"Education": "industries/education.html", "Engineering and Construction": "industries/engineering-construction.html",
                  "Financial Services": "industries/financial-services.html", "Healthcare": "industries/healthcare.html",
                  "Insurance": "industries/insurance.html", "Manufacturing and Logistics": "industries/manufacturing-logistics.html",
                  "Real Estate": "industries/real-estate.html", "State and Local Government": "industries/government.html"}
TOP_SERVICES = [("Managed IT services", "services/managed-it.html"), ("Cybersecurity", "services/cybersecurity.html"),
                ("Business phone systems", "services/business-phone-systems.html"), ("Copiers and printers", "services/copiers.html"),
                ("Managed print services", "services/managed-print.html"), ("Document conversion", "services/document-conversion.html")]
TAG_RULES = [  # first match wins: (regex on the page file, blog tag slug, heading topic)
    (r"cyber|security|knowbe4|phish|network-sec|firewall", "cybersecurity", "security"),
    (r"managed-it|proactive-it|help-desk|it-services|infrastructure|network", "managed-it", "managed IT"),
    (r"cloud|backup|continuity|disaster", "cloud-solutions", "cloud and backup"),
    (r"phone|voice|communicat|ucaas|contact|call|carrier|video-conf|collab", "business-phone-systems", "business phones"),
    (r"managed-print|print|copier|mfp|follow-me|production", "managed-print-services", "print"),
    (r"document|scanning|records|conversion|content|workflow|process", "document-conversion", "documents and process"),
    (r"\bai\b|ai-|artificial|playbook", "ai-consulting", "AI"),
    (r"physical|surveillance|camera|intrusion", "physical-security", "physical security"),
]
CASE_PILLAR = {"Print": ["tippecanoe-school-corporation", "star-financial-bank", "shiel-sexton"], "Process": ["johnson-memorial-hospital", "tippecanoe-school-corporation-digital-document", "city-of-anderson"],
               "Information": ["echo-engineering", "gailey-eye-clinic", "aspire"], "Communication": ["mid-city", "berry-global", "bowen-engineering"]}


def _load():
    ov = json.load(open(os.path.join(ROOT, "brands/vanausdall.overrides.pillars.json"), encoding="utf-8"))
    groups = {}
    secs = ov.get("solutions.html", {}).get("sections", [])
    for s in secs:                       # the main services of each pillar come first
        if s["type"] == "services":
            groups.setdefault(s["heading"], []).extend((it[0], it[2]) for it in s["items"])
    for s in secs:
        if s["type"] == "linkcloud":
            for g in s["groups"]:
                have = {h for _, h in groups.get(g["title"], [])}
                groups.setdefault(g["title"], []).extend((l, h) for l, h in g["links"] if h not in have)
    return groups


GROUPS = _load()
FILE2PILLAR = {h.replace("/", "/"): p for p, links in GROUPS.items() for _, h in links}


def _tag_for(file):
    for rx, tag, topic in TAG_RULES:
        if re.search(rx, file):
            return tag, topic
    return None, None


def _label(pages, f):
    for p in pages:
        if p["file"] == f:
            return re.split(r"\s*[|,]\s*", p["title"])[0].replace(" in Indiana", "").replace(", Indiana", "").strip()
    return f


def _cases(pages):
    out = {}
    for p in pages:
        if p["file"].startswith("case-studies/"):
            cat = ""
            for s in p["sections"]:
                if s["type"] == "article":
                    cat = s.get("category", "")
            out[p["file"]] = (cat, re.split(r"\s+case study", p["title"])[0])
    return out


def extra_sections(page, pages):
    f = page["file"]
    cases = _cases(pages)
    groups, blog = [], None
    if f.startswith("services/") and f in FILE2PILLAR or f in PILLAR_PAGES.values() and False:
        pillar = FILE2PILLAR[f]
        sib = [(l, h) for l, h in GROUPS[pillar] if h != f][:9]
        groups.append({"title": f"More in {pillar.lower()}", "links": sib})
        groups.append({"title": "Keep exploring", "links": [[f"The {pillar.lower()} pillar", PILLAR_PAGES[pillar]], ["Industries we serve", "industries.html"], ["Case studies", "case-studies.html"],
                                                          ["Technology Strength Assessment", "technology-strength-assessment.html"], ["Talk to a solutions expert", "contact.html"]]})
    elif f in PILLAR_PAGES.values():
        pillar = [k for k, v in PILLAR_PAGES.items() if v == f][0]
        groups.append({"title": "Industries we serve", "links": [[k, v] for k, v in INDUSTRY_PAGES.items()]})
        cs = [[cases[c][1], c] for c in cases if any(c.endswith(x + ".html") for x in CASE_PILLAR[pillar])]
        if cs: groups.append({"title": "Results from this pillar", "links": cs})
        groups.append({"title": "Other pillars", "links": [[f"{k}", v] for k, v in PILLAR_PAGES.items() if v != f] + [["Technology Strength Assessment", "technology-strength-assessment.html"]]})
    elif f.startswith("industries/") and f != "industries.html":
        cat = [k for k, v in INDUSTRY_PAGES.items() if v == f]
        if cat:
            same = [[cases[c][1], c] for c in cases if cases[c][0].lower() == cat[0].lower()]
            groups.append({"title": "Popular services", "links": [list(x) for x in TOP_SERVICES]})
            if same: groups.append({"title": f"{cat[0]} case studies", "links": same})
            groups.append({"title": "Other industries", "links": [[k, v] for k, v in INDUSTRY_PAGES.items() if v != f]})
    elif f.startswith("case-studies/") and f in cases:
        cat = cases[f][0]
        more = [[cases[c][1], c] for c in cases if c != f and cases[c][0].lower() == cat.lower()][:5]
        groups.append({"title": f"More in {cat.lower()}" if more else "More case studies", "links": more or [["All case studies", "case-studies.html"]]})
        groups.append({"title": "Related", "links": ([[f"{cat} industry page", INDUSTRY_PAGES[cat]]] if cat in INDUSTRY_PAGES else []) + [["Managed print services", "services/managed-print.html"], ["Managed IT services", "services/managed-it.html"], ["Technology Strength Assessment", "technology-strength-assessment.html"]]})
    elif f.startswith("locations/") and f not in ("locations.html",):
        city = f.split("/")[1].split("-")[0]
        groups.append({"title": "Explore our services", "links": [list(x) for x in TOP_SERVICES]})
        groups.append({"title": "Other offices", "links": [["Indianapolis", "locations/indianapolis.html"], ["Fort Wayne", "locations/fort-wayne.html"], ["Evansville", "locations/evansville.html"], ["All locations", "locations.html"]]})
    out = []
    if groups:
        out.append({"type": "linkcloud", "id": "related", "alt": True, "eyebrow": "Keep exploring", "heading": "Related pages", "intro": "", "groups": groups})
    if f.startswith(("services/", "industries/", "solutions")) or f in PILLAR_PAGES.values():
        tag, topic = _tag_for(f)
        if tag:
            out.append({"type": "blogrel", "id": "from-the-blog", "alt": False, "eyebrow": "From the blog", "heading": f"Guides on {topic}", "tag": tag, "count": "3", "link_label": "Read all VAF guides"})
    return out
