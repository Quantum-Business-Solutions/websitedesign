"""Page-for-page migration and on-page normalisation for a preview build.

fix_title / fix_desc make every title 30 to 60 characters with the city in it and every meta
description 70 to 160 characters. build_migrated turns the copy extracted from a client's
current site (brands/<slug>.pages.json, from the whole-site crawl) into pages in the new
templates, so the preview has a counterpart for every URL the client has today, each with an
FAQ, the right schema type and a form. link_sections returns the index lists that keep the
migrated pages linked from the pillar pages.
"""
import re

CITY_WORDS = ("indianapolis", "indiana", "fort wayne", "evansville", "bloomington", "carmel", "fishers", "noblesville", "greenwood", "muncie", "columbus", "south bend")
CITY_SLUGS = {"indianapolis": "Indianapolis", "fort-wayne": "Fort Wayne", "evansville": "Evansville", "bloomington": "Bloomington", "carmel": "Carmel", "fishers": "Fishers", "noblesville": "Noblesville", "greenwood": "Greenwood", "muncie": "Muncie", "columbus": "Columbus", "south-bend": "South Bend"}


def has_city(s):
    return any(c in s.lower() for c in CITY_WORDS)


def fix_title(title, brand="Van Ausdall & Farrar", short="VAF", city_default=", Indiana"):
    t = re.sub(r"\s+", " ", title).strip()
    if 30 <= len(t) <= 60 and has_city(t):
        return t
    base = re.sub(r"\s*\|.*$", "", t).strip()
    if brand.lower() in base.lower():
        if not has_city(base):
            base = base.rstrip(".") + ", Indianapolis"
        if 30 <= len(base) <= 60:
            return base
        base = re.sub(r"\b(Van Ausdall (&|and) Farrar|VA&F|VAF)('s)?\b[:,]?\s*", "", base).strip(" ,-:") or base
    base = re.sub(r"\s+", " ", base)
    if not has_city(base):
        base = base.rstrip(".") + city_default
    for suf in (f" | {brand}", f" | {short}"):
        if 30 <= len(base) + len(suf) <= 60:
            return base + suf
    lim = 60 - len(f" | {short}")
    stop = ("for", "and", "in", "of", "the", "with", "to", "a", "an", "&", "or", "your", "solutions", "systems")
    core = re.sub(re.escape(city_default) + r"$", "", base).strip()
    room = lim - len(city_default)
    cut = core if len(core) <= room else core[:room].rsplit(" ", 1)[0]
    words = cut.rstrip(" ,:-").split(" ")
    while len(words) > 2 and words[-1].lower().strip(",") in stop:
        words.pop()
    cut = " ".join(words).rstrip(" ,:-")
    return cut + city_default + f" | {short}"


def fix_desc(text, tail="From Van Ausdall & Farrar, Indiana's largest office technology provider since 1914.", lo=70, hi=160):
    t = re.sub(r"\s+", " ", (text or "")).strip()
    if len(t) > hi:
        out = ""
        for sent in re.split(r"(?<=[.!?])\s+", t):
            cand = (out + " " + sent).strip()
            if len(cand) > hi - 2:
                break
            out = cand
        t = out if len(out) >= lo else (t[:hi - 3].rsplit(" ", 1)[0].rstrip(" ,;:") + ".")
    if len(t) < lo:
        t = (t + " " + tail).strip()
        if len(t) > hi:
            t = t[:hi - 1].rsplit(" ", 1)[0].rstrip(" ,;:") + "."
    return t


def tidy(t):
    """Client-facing text rule: no em or en dashes. Replace with a comma or colon, keep the sentence readable."""
    t = re.sub(r"\s*[\u2014\u2013]\s*", ", ", t or "")
    t = re.sub(r"\s*--\s*", ", ", t)
    t = re.sub(r",\s*,", ",", t)
    return re.sub(r"\s+", " ", t).strip()


def sanitise(o):
    o = dict(o)
    o["title"] = tidy(o.get("title")); o["meta"] = tidy(o.get("meta")); o["h1"] = tidy(o.get("h1"))
    o["blocks"] = [{"heading": tidy(b.get("heading")), "paras": [re.sub(r"\s*Explore [A-Z][^.]*$", "", tidy(p)).strip() for p in b.get("paras", []) if not is_junk(tidy(p))], "bullets": [tidy(x) for x in b.get("bullets", []) if not is_junk(tidy(x))]} for b in o.get("blocks", [])]
    return o


def cut(text, n):
    """Cut at a sentence end at or before n characters, else at a word boundary."""
    t = (text or "").strip()
    if len(t) <= n:
        return t
    best = ""
    for sent in re.split(r"(?<=[.!?])\s+", t):
        cand = (best + " " + sent).strip()
        if len(cand) > n:
            break
        best = cand
    return best if len(best) >= n // 3 else t[:n].rsplit(" ", 1)[0].rstrip(" ,;:") + "."


def is_junk(p):
    return p.count(" | ") >= 2 or p.lower().startswith(("explore ", "read full story", "click here"))


def clean_name(o):
    base = re.sub(r"\s*\|.*$", "", o.get("title") or "").strip()
    base = re.sub(r"\b(Van Ausdall (&|and) Farrar|VA&F|VAF)('s)?\b[:,]?\s*", "", base).strip(" ,-:")
    base = re.sub(r"^(KnowBe4)\s*[–-]\s*", "", base)
    return base or (o.get("h1") or "").strip() or "Page"


PILLAR_OF = {"information": "Information", "communication": "Communication", "print": "Print", "process": "Process", "knowbe4": "Information"}
KEYS = [("Information", ("security", "cloud", "network", "it-", "managed-it", "proactive", "project", "backup", "continuity", "knowbe4", "phish", "ransom", "password", "spoof", "auto-support")),
        ("Communication", ("voice", "phone", "telecom", "carrier", "circuit", "sd-wan", "communication", "dictation", "transcription", "recognition", "switch-to-cloud", "conference", "mobility", "unified", "call-")),
        ("Print", ("print", "copier", "copy-", "wids", "wide", "production")),
        ("Process", ("document", "forms", "scanning", "iphone", "content", "workflow", "mail", "fulfillment", "receptionist", "facilities", "process"))]


def guess_pillar(path):
    p = path.lower()
    for pillar, keys in KEYS:
        if any(k in p for k in keys):
            return pillar
    return ""


def map_url(url):
    """Return (file, ptype, pillar, section_label) for a client URL, or None when the page is not migrated."""
    segs = [s for s in url.strip("/").split("/") if s]
    if not segs:
        return None
    s0 = segs[0]
    if s0 in PILLAR_OF:
        if len(segs) == 1:
            return (f"solutions-{s0}.html", "service", PILLAR_OF[s0], "Solutions")
        slug = segs[1] if s0 != "knowbe4" else f"knowbe4-{segs[1]}"
        return (f"services/{slug}.html", "service", PILLAR_OF[s0], "Solutions")
    if s0 == "case-studies" and len(segs) > 1:
        return (f"case-studies/{segs[1]}.html", "case study", "", "Case studies")
    if s0 in CITY_SLUGS:
        city = CITY_SLUGS[s0]
        if len(segs) == 1:
            return (f"locations/{s0}.html", "city", "", "Locations")
        short = re.sub(rf"(-in)?-{s0}(-in)?$", "", segs[1]); short = re.sub(rf"-{s0}$", "", short)
        return (f"locations/{s0}-{short}.html", "city", guess_pillar(segs[1]), "Locations")
    if s0 == "policies":
        return (f"policies/{segs[1]}.html", "policy", "", "Policies")
    if s0 == "about" and len(segs) > 1:
        return (f"about/{segs[1]}.html", "company", "", "About")
    if s0 == "contact" and len(segs) > 1:
        return (f"{segs[1]}.html", "company", "", "About")
    if s0 == "industries" and len(segs) > 1:
        return (f"industries/{segs[1]}.html", "service", "", "Industries")
    pillar = guess_pillar(s0)
    if "privacy" in s0 or "policy" in s0:
        return (f"policies/{s0}.html", "policy", "", "Policies")
    return (f"{'services/' if pillar else ''}{s0}.html", "service" if pillar else "company", pillar, "Solutions" if pillar else "About")


def _faq_for(o, name, ptype, pillar, city, phone):
    qs = []
    for b in o["blocks"]:
        if b["heading"].rstrip().endswith("?") and b["paras"]:
            qs.append([b["heading"].strip(), b["paras"][0][:400]])
    first = next((p for b in o["blocks"] for p in b["paras"]), "")
    subject = name
    if ptype == "city":
        c = city or "Indiana"
        pool = [[f"Does Van Ausdall & Farrar serve {c}?", f"Yes. {c} is served from the nearest VAF office with the same Customer Care Center, 25-point service inspections and 24-hour response as Indianapolis. The service fleet covers the entire state."],
                [f"What does Van Ausdall & Farrar provide in {c}?", (first or f"Managed IT and cybersecurity, business phone systems, copiers and managed print, and document services for organizations in {c}.")[:400]],
                [f"How do we get started in {c}?", f"Call {phone} or schedule a consultation. Most engagements begin with the free Technology Strength Assessment, then a specialist walks the results with you."],
                ["Who supports us after installation?", "The Customer Care Center in Indianapolis, Monday through Friday, 7:00am to 5:00pm, with requests answered within 24 hours and certified technicians dispatched locally."]]
    elif ptype == "case study":
        pool = [[f"What did {subject} achieve with Van Ausdall & Farrar?", (first or "The results are described in the case study above.")[:400]],
                [f"Which services did {subject} use?", (pillar and f"{pillar} services from Van Ausdall & Farrar, delivered under one agreement.") or "Services from across VAF's four pillars: information, communication, print and process, under one agreement."],
                ["Can we get results like these?", "Every engagement starts with the free Technology Strength Assessment. A specialist maps your devices, contracts and workflows and shows where the savings are before you commit."]]
    elif ptype == "policy":
        pool = [["Who do I contact about this policy?", f"Van Ausdall & Farrar, Inc., 6430 E 75th Street, Indianapolis, IN 46250, {phone}. Write to the same address for any request about your personal information."],
                ["Does this policy apply to the Customer Care app?", "The Customer Care app has its own privacy policy, linked from this site. Where the two differ, the app policy governs data collected in the app."],
                ["When was this policy last updated?", "The policy text on this page is carried over from vanausdall.com as of September 2026; a dated revision line is added when the new site goes live."]]
    else:
        pool = [[f"What is {subject.lower() if subject[:1].isupper() and not subject.isupper() else subject}?", (first or f"{subject} from Van Ausdall & Farrar, Indiana's largest office technology provider.")[:400]],
                [f"Who is {subject.lower() if not subject.isupper() else subject} for?", f"Businesses, schools, hospitals and municipalities across Indiana and the Midwest that want {pillar.lower() + ' technology' if pillar else 'technology'} from one local partner rather than several vendors."],
                [f"How much does {subject.lower() if not subject.isupper() else subject} cost?", "It depends on scope, so we do not publish a single price. The free Technology Strength Assessment produces a written recommendation and a quote with no obligation."],
                [f"Where is {subject.lower() if not subject.isupper() else subject} available?", f"Indianapolis, Fort Wayne, Evansville and every town between; the service fleet covers all of Indiana and customers throughout the Midwest are served from Indianapolis. Call {phone}."]]
    for q in pool:
        if len(qs) >= 5:
            break
        if q[0] not in [x[0] for x in qs]:
            qs.append(q)
    return qs


def build_migrated(extract, existing_files, covered, retire, images, phone, pillar_blurbs, section_index):
    """extract: list from <slug>.pages.json; existing_files: set of build files already present;
    covered: {client url: build file}; retire: set of client urls not migrated; images: {pillar or type: asset};
    pillar_blurbs: {pillar: paragraph}; section_index: {'Solutions': 'solutions.html', ...}."""
    pages, redirects, taken = [], {}, set(existing_files)
    for o in sorted(extract, key=lambda o: o["url"]):
        url = o["url"]
        if url in covered:
            redirects[url] = covered[url]; continue
        if url in retire or url == "/":
            continue
        m = map_url(url)
        if not m:
            continue
        file, ptype, pillar, label = m
        o = sanitise(o)
        if file in taken:
            redirects[url] = file; continue
        taken.add(file); redirects[url] = file
        name = clean_name(o)
        h1 = (o.get("h1") or name).strip()
        if ptype == "case study" and h1:
            name = h1
        city = next((CITY_SLUGS[c] for c in CITY_SLUGS if url.strip("/").split("/")[0] == c), "")
        paras_all = [p for b in o["blocks"] for p in b["paras"]]
        sub = cut(paras_all[0] if paras_all else (o.get("meta") or ""), 280)
        img = images.get(pillar) or images.get(ptype) or images.get("default")
        eyebrow = f"{label}: {pillar}" if pillar else label
        secs = [{"type": "hero", "layout": "centered", "eyebrow": eyebrow, "heading": h1, "subhead": sub,
                 "primary": {"label": "Schedule a consultation", "href": "contact.html"}, "secondary": {"label": "Take the assessment", "href": "technology-strength-assessment.html"},
                 "image": img, "image_alt": f"{name}", "image_w": 1200, "image_h": 800}]
        if ptype == "case study":
            chapters = []
            for i, b in enumerate(o["blocks"]):
                if not b["paras"] and not b["bullets"]:
                    continue
                paras = b["paras"] or [" ".join(b["bullets"])]
                chapters.append({"id": f"c{i}", "title": b["heading"] or ("Overview" if i == 0 else "Results"), "paras": paras[:5]})
            if not chapters:
                chapters = [{"id": "c0", "title": "Overview", "paras": [sub or name]}]
            secs = [{"type": "article", "category": "Case study", "crumb_label": "Case studies", "crumb_href": "case-studies.html", "heading": h1, "standfirst": sub, "image": img, "image_alt": f"{name} case study", "date_label": "Case study", "read": f"{max(2, o['words'] // 220)} min read", "chapters": chapters,
                     "author": {"name": "Van Ausdall & Farrar", "role": "Published case study, vanausdall.com"}}]
        else:
            n = 0
            for b in o["blocks"]:
                if not b["paras"] and not b["bullets"]:
                    continue
                if n >= 6:
                    break
                body = " ".join(b["paras"][:4])
                if not body and b["bullets"]:
                    body = f"What {name.lower() if not name.isupper() else name} covers, in VAF's words."
                secs.append({"type": "detail", "alt": bool(n % 2), "eyebrow": pillar or label, "heading": b["heading"] or (f"About {name}" if n == 0 else "In practice"), "body": cut(body, 1400), "bullets": b["bullets"][:6]})
                n += 1
            if o["words"] < 200 and ptype != "policy":
                secs.append({"type": "detail", "alt": bool(n % 2), "eyebrow": "Why VAF", "heading": "What every Van Ausdall & Farrar customer gets", "body": "Indiana's largest full-service office technology provider, privately owned in Indianapolis since 1914. A Net Promoter Score of 93.4, collected and audited by CEO Juice, an independent company, against a US average of 10. SOC 2 certification for the way we protect customer data. Mitel Gold partner seven years running, in the telecom business since 1983 with more than 4,000 systems deployed. Technology advisors whose average tenure with the company is fifteen years, so the person who sold the system is still here when it needs attention.", "bullets": ["Serving Indiana since 1914", "NPS 93.4, audited by CEO Juice", "SOC 2 certified", "250+ years of IT experience on staff"]})
                n += 1
            if o["words"] < 320 and ptype != "policy":
                blurb = pillar_blurbs.get(pillar) or pillar_blurbs.get("default")
                secs.append({"type": "detail", "alt": bool(n % 2), "eyebrow": "One agreement", "heading": "How it fits with the rest of Van Ausdall & Farrar", "body": blurb,
                             "bullets": ["One Customer Care Center, answered within 24 hours", "25-point inspection on every service call", "Net Promoter Score 93.4, audited by CEO Juice", "Privately owned in Indianapolis since 1914"]})
        faq = _faq_for(o, name, ptype, pillar, city, phone)
        if faq:
            secs.append({"type": "faq", "alt": True, "heading": f"Questions about {name}" if ptype != "city" else f"Questions we get in {city or 'Indiana'}", "items": faq})
        if ptype != "policy":
            secs.append({"type": "leadform", "id": "consult", "heading": "Start with the Technology Strength Assessment", "body": "Ten to fifteen minutes, then a specialist walks it with you.", "submit": "Schedule my consultation", "note": f"A person from the Indianapolis office replies, not an autoresponder. Or call {phone}."})
        crumbs = [["Home", "index.html"], [label, section_index.get(label, "index.html")], [name, file]]
        schema = []
        site = "https://www.vanausdall.com"
        if ptype in ("service", "city"):
            schema.append({"@context": "https://schema.org", "@type": "Service", "name": name, "serviceType": name, "provider": {"@type": "Organization", "name": "Van Ausdall & Farrar, Inc.", "url": site},
                           "areaServed": [{"@type": "City", "name": city}] if city else {"@type": "State", "name": "Indiana"}, "description": sub or name})
        if ptype == "case study":
            schema.append({"@context": "https://schema.org", "@type": "Article", "headline": h1, "description": sub or name, "author": {"@type": "Organization", "name": "Van Ausdall & Farrar, Inc."}, "publisher": {"@type": "Organization", "name": "Van Ausdall & Farrar, Inc."}, "about": name})
        title_base = f"{name} in {city}, IN" if (city and not has_city(name)) else name
        pages.append({"file": file, "title": fix_title(title_base), "description": fix_desc(o.get("meta") or sub or name), "crumbs": crumbs, "sections": secs, "schema": schema, "migrated_from": url, "ptype": ptype, "pillar": pillar, "name": name, "one": (sub or name)[:140]})
    return pages, redirects


def link_sections(migrated):
    """Index lists so nothing is orphaned: by pillar for solutions, by city for locations, the rest for about."""
    out = {}
    sol = [[p["pillar"] or "Solutions", p["name"], p["one"], "Open the page", p["file"]] for p in migrated if p["ptype"] == "service"]
    if sol:
        out["solutions.html"] = {"type": "resources", "alt": True, "heading": "Every solution page, by pillar", "intro": "Each page from vanausdall.com today, rebuilt in the new templates with its FAQ and schema.", "items": sorted(sol, key=lambda x: (x[0], x[1]))}
    cit = [[p["file"].split("/")[-1].split("-")[0].title(), p["name"], p["one"], "Open the page", p["file"]] for p in migrated if p["ptype"] == "city"]
    if cit:
        out["locations.html"] = {"type": "resources", "alt": True, "heading": "Every city page", "intro": "One page per city and per service in that city, each with LocalBusiness and Service schema.", "items": sorted(cit, key=lambda x: (x[0], x[1]))}
    cs = [["Case study", p["name"], p["one"], "Read the case study", p["file"]] for p in migrated if p["ptype"] == "case study"]
    if cs:
        out["case-studies.html"] = {"type": "resources", "alt": True, "heading": "More case studies, in full", "intro": "Migrated from the PDFs and pages on vanausdall.com.", "items": sorted(cs, key=lambda x: x[1])}
    co = [["About", p["name"], p["one"], "Open the page", p["file"]] for p in migrated if p["ptype"] in ("company", "policy")]
    if co:
        out["about.html"] = {"type": "resources", "alt": True, "heading": "More from Van Ausdall & Farrar", "intro": "Every remaining page on vanausdall.com, kept and rebuilt.", "items": sorted(co, key=lambda x: x[1])}
    return out
