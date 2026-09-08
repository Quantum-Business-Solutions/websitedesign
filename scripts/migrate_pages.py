"""Page-for-page migration and on-page normalisation for a preview build.

fix_title / fix_desc make every title 30 to 60 characters with the city in it and every meta
description 70 to 160 characters. build_migrated turns the copy extracted from a client's
current site (brands/<slug>.pages.json, from the whole-site crawl) into pages in the new
templates, so the preview has a counterpart for every URL the client has today, each with an
FAQ, the right schema type and a form. link_sections returns the index lists that keep the
migrated pages linked from the pillar pages.
"""
import re

# Defaults are Van Ausdall & Farrar's. Call configure(...) from the content file before using anything else.
CITY_WORDS = ("indianapolis", "indiana", "fort wayne", "evansville", "bloomington", "carmel", "fishers", "noblesville", "greenwood", "muncie", "columbus", "south bend")
CITY_SLUGS = {"indianapolis": "Indianapolis", "fort-wayne": "Fort Wayne", "evansville": "Evansville", "bloomington": "Bloomington", "carmel": "Carmel", "fishers": "Fishers", "noblesville": "Noblesville", "greenwood": "Greenwood", "muncie": "Muncie", "columbus": "Columbus", "south-bend": "South Bend"}
BRAND = {"name": "Van Ausdall & Farrar", "legal": "Van Ausdall & Farrar, Inc.", "short": "VAF", "state": "Indiana", "hq_city": "Indianapolis", "site": "https://www.vanausdall.com",
         "tail": "From Van Ausdall & Farrar, Indiana's largest office technology provider since 1914.", "hq_address": "6430 E 75th Street, Indianapolis, IN 46250",
         "proof": ["Serving Indiana since 1914", "NPS 93.4, audited by CEO Juice", "SOC 2 certified", "250+ years of IT experience on staff"],
         "proof_body": "Indiana's largest full-service office technology provider, privately owned in Indianapolis since 1914. A Net Promoter Score of 93.4, collected and audited by CEO Juice, an independent company, against a US average of 10. SOC 2 certification for the way we protect customer data. Mitel Gold partner seven years running, in the telecom business since 1983 with more than 4,000 systems deployed. Technology advisors whose average tenure with the company is fifteen years, so the person who sold the system is still here when it needs attention.",
         "service_line": "One Customer Care Center, answered within 24 hours", "assessment": "Technology Strength Assessment",
         "audience": "Businesses, schools, hospitals and municipalities across Indiana and the Midwest", "coverage": "Indianapolis, Fort Wayne, Evansville and every town between; the service fleet covers all of Indiana and customers throughout the Midwest are served from Indianapolis."}


def configure(brand=None, city_words=None, city_slugs=None):
    """Set the client. brand: keys as in BRAND (partial ok). city_words: lowercase words that count as a city in a title. city_slugs: {url-slug: City Name} for city pages."""
    global CITY_WORDS, CITY_SLUGS
    if brand:
        BRAND.update(brand)
    if city_words:
        CITY_WORDS = tuple(w.lower() for w in city_words)
    if city_slugs:
        CITY_SLUGS = dict(city_slugs)


def _brand_rx():
    n = re.escape(BRAND["name"]).replace(r"\&", r"(&|and)").replace(r"\ ", r"\s+")
    return rf"\b({n}|{re.escape(BRAND['short'])})('s)?\b[:,]?\s*"


def has_city(s):
    return any(c in s.lower() for c in CITY_WORDS)


def fix_title(title, brand=None, short=None, city_default=None):
    brand = brand or BRAND["name"]; short = short or BRAND["short"]; city_default = city_default or f", {BRAND['state']}"
    t = re.sub(r"\s+", " ", title).strip()
    if 30 <= len(t) <= 60 and has_city(t):
        return t
    base = re.sub(r"\s*\|.*$", "", t).strip()
    if brand.lower() in base.lower():
        if not has_city(base):
            base = base.rstrip(".") + f", {BRAND['hq_city']}"
        if 30 <= len(base) <= 60:
            return base
        base = re.sub(_brand_rx(), "", base).strip(" ,-:") or base
    base = re.sub(r"\s+", " ", base)
    base = re.sub(r"\b(for|and|of|at|by|with|to|the)\s+(for|and|of|at|by|with|to|the)\b", r"\1", base)
    base = re.sub(r"\s+(for|and|of|at|by|with|to|the)$", "", base.strip())
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


def fix_desc(text, tail=None, lo=70, hi=160):
    tail = tail or BRAND["tail"]
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
    t = re.sub(r"\s*[\"\u201c]?opens in a new window[\"\u201d]?\s*", " ", t, flags=re.I)
    t = re.sub(r"(?<=[a-z?!.])(?=[A-Z][a-z])", " ", t)
    return re.sub(r"\s+", " ", t).strip()


PLACEHOLDER = "Please wait while the policy is loaded"


def templated_meta(m):
    """The client's CMS pastes the title into the meta and truncates it; those are not descriptions."""
    m = m or ""
    return (not m) or (" | " in m) or ("and IT services from" in m) or re.search(r"\b[A-Za-z]{3,}i\b and IT", m) is not None


def sanitise(o):
    o = dict(o)
    if any(PLACEHOLDER in p for b in o.get("blocks", []) for p in b.get("paras", [])):
        name = (o.get("h1") or o.get("title") or "This policy").split("|")[0].strip()
        o["blocks"] = [{"heading": "", "paras": [f"{name} is published through Termageddon and embedded on this page at launch, so it stays current when the policy text changes. Until then, the policy in force is the one on the current site, linked below, and requests about personal information go to the headquarters address in the questions section."], "bullets": []}]
        o["placeholder"] = True
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
    base = re.sub(_brand_rx(), "", base).strip(" ,-:")
    base = re.sub(r"^(KnowBe4)\s*[\u2013-]\s*", "", base)
    base = re.sub(r"\b(for|and|of|at|by|with|to|the)\s+(for|and|of|at|by|with|to|the)\b", r"\1", base)
    base = re.sub(r"\s+(for|and|of|at|by|with|to|the|services|solutions)$", "", base.strip(), flags=re.I) if len(base.split()) > 2 else base
    return base.strip(" ,-:") or (o.get("h1") or "").strip() or "Page"


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
            qs.append([b["heading"].strip(), cut(b["paras"][0], 400)])
    paras = [p for b in o["blocks"] for p in b["paras"]]
    first = paras[0] if paras else ""
    second = next((p for p in paras[1:] if len(p) > 60), "")
    if not second:
        second = f"{name} is one of {BRAND['name']}'s {(pillar.lower() + ' ') if pillar else ''}services, delivered under one agreement with {BRAND['service_line'][0].lower() + BRAND['service_line'][1:]}. " + (" ".join(x.rstrip('.') + '.' for x in next((b['bullets'] for b in o['blocks'] if b['bullets']), [])[:3]))
    subject = name
    if ptype == "city":
        c = city or BRAND["state"]
        pool = [[f"Does {BRAND['name']} serve {c}?", f"Yes. {c} is served from the nearest {BRAND['short']} office with the same service desk and response commitments as {BRAND['hq_city']}. The service fleet covers the entire state."],
                [f"What does {BRAND['name']} provide in {c}?", cut(second or first or f"The full {BRAND['name']} service line for organizations in {c}.", 400)],
                [f"How do we get started in {c}?", f"Call {phone} or schedule a consultation. Most engagements begin with the free {BRAND['assessment']}, then a specialist walks the results with you."],
                ["Who supports us after installation?", f"{BRAND['service_line']}, with certified technicians dispatched locally."]]
    elif ptype == "case study":
        pool = [[f"What did {subject} achieve with {BRAND['name']}?", cut(first or "The results are described in the case study above.", 400)],
                [f"Which services did {subject} use?", (pillar and f"{pillar} services from {BRAND['name']}, delivered under one agreement.") or f"Services from across {BRAND['name']}, under one agreement."],
                ["Can we get results like these?", f"Every engagement starts with the free {BRAND['assessment']}. A specialist maps your devices, contracts and workflows and shows where the savings are before you commit."]]
    elif ptype == "policy":
        pool = ([["Where is the current policy text?", f"On the current site at {BRAND['site']}{o.get('url', '')}. It is embedded here at launch so the two never differ."]] if o.get("placeholder") else [["Which version of this policy governs?", f"The one published on the current site at {BRAND['site']}{o.get('url', '')} until the new site goes live. This page mirrors it and is re-synced from the policy provider at launch."]]) + [["Who do I contact about this policy?", f"{BRAND['legal']}, {BRAND['hq_address']}, {phone}. Write to the same address for any request about your personal information."],
                ["Does this policy apply to the Customer Care app?", "The Customer Care app has its own privacy policy, linked from this site. Where the two differ, the app policy governs data collected in the app."],
                ["When was this policy last updated?", f"The policy text on this page is carried over from the current site; a dated revision line is added when the new site goes live."]]
    else:
        pool = [[f"What is {subject}?", cut(second or first or f"{subject} from {BRAND['name']}.", 400)],
                [f"Who is {subject} for?", f"{BRAND['audience']} that want {pillar.lower() + ' technology' if pillar else 'technology'} from one local partner rather than several vendors."],
                [f"How much does {subject} cost?", f"It depends on scope, so we do not publish a single price. The free {BRAND['assessment']} produces a written recommendation and a quote with no obligation."],
                [f"Where is {subject} available?", f"{BRAND['coverage']} Call {phone}."]]
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
        if len(h1) < 12 and len(name) >= 12 and ptype != "case study":
            h1 = name
        second = next((p for p in paras_all[1:] if len(p) > 60), "")
        img = images.get(pillar) or images.get(ptype) or images.get("default")
        eyebrow = f"{label}: {pillar}" if pillar else label
        secs = [{"type": "hero", "layout": "centered", "eyebrow": eyebrow, "heading": h1, "subhead": sub,
                 "primary": {"label": "Schedule a consultation", "href": "contact.html"}, "secondary": {"label": "Take the assessment", "href": BRAND.get("assessment_href", "technology-strength-assessment.html")},
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
                     "author": {"name": BRAND["name"], "role": f"Published case study, {BRAND['site'].split('//')[-1].replace('www.', '')}"}}]
        else:
            n = 0
            for b in o["blocks"]:
                if not b["paras"] and not b["bullets"]:
                    continue
                if n >= 6:
                    break
                paras = b["paras"][:4]
                if n == 0 and len(paras) > 1 and paras[0] == paras_all[0]:
                    paras = paras[1:]
                body = " ".join(paras)
                if not body and b["bullets"]:
                    body = f"What {name.lower() if not name.isupper() else name} covers, in VAF's words."
                secs.append({"type": "detail", "alt": bool(n % 2), "eyebrow": pillar or label, "heading": b["heading"] or (f"About {name}" if n == 0 else "In practice"), "body": cut(body, 1400), "bullets": b["bullets"][:6]})
                n += 1
            if o["words"] < 200 and ptype != "policy":
                secs.append({"type": "detail", "alt": bool(n % 2), "eyebrow": "Why VAF", "heading": f"What every {BRAND['name']} customer gets", "body": BRAND["proof_body"], "bullets": BRAND["proof"]})
                n += 1
            if o["words"] < 320 and ptype != "policy":
                blurb = pillar_blurbs.get(pillar) or pillar_blurbs.get("default")
                secs.append({"type": "detail", "alt": bool(n % 2), "eyebrow": "One agreement", "heading": f"How it fits with the rest of {BRAND['name']}", "body": blurb, "bullets": [BRAND["service_line"]] + BRAND["proof"][:3]})
        faq = _faq_for(o, name, ptype, pillar, city, phone)
        if faq:
            secs.append({"type": "faq", "alt": True, "heading": f"Questions about {name}" if ptype != "city" else f"Questions we get in {city or BRAND['state']}", "items": faq})
        if ptype != "policy":
            secs.append({"type": "leadform", "id": "consult", "heading": f"Start with the {BRAND['assessment']}", "body": "Ten to fifteen minutes, then a specialist walks it with you.", "submit": "Schedule my consultation", "note": f"A person from the {BRAND['hq_city']} office replies, not an autoresponder. Or call {phone}."})
        crumbs = [["Home", "index.html"], [label, section_index.get(label, "index.html")], [name, file]]
        schema = []
        site = BRAND["site"]
        if ptype in ("service", "city"):
            schema.append({"@context": "https://schema.org", "@type": "Service", "name": name, "serviceType": name, "provider": {"@type": "Organization", "name": BRAND["legal"], "url": site},
                           "areaServed": [{"@type": "City", "name": city}] if city else {"@type": "State", "name": BRAND["state"]}, "description": sub or name})
        if ptype == "case study":
            schema.append({"@context": "https://schema.org", "@type": "Article", "headline": h1, "description": sub or name, "author": {"@type": "Organization", "name": BRAND["legal"]}, "publisher": {"@type": "Organization", "name": BRAND["legal"]}, "about": name})
        title_base = f"{name} in {city}, IN" if (city and not has_city(name)) else name
        meta_src = sub if templated_meta(o.get("meta")) else o.get("meta")
        pages.append({"file": file, "title": fix_title(title_base), "description": fix_desc(meta_src or sub or name), "crumbs": crumbs, "sections": secs, "schema": schema, "migrated_from": url, "ptype": ptype, "pillar": pillar, "name": name, "one": cut(sub or name, 140)})
    return pages, redirects


def link_sections(migrated):
    """Index lists so nothing is orphaned: by pillar for solutions, by city for locations, the rest for about."""
    out = {}
    sol = [[p["pillar"] or "Solutions", p["name"], p["one"], "Open the page", p["file"]] for p in migrated if p["ptype"] == "service"]
    if sol:
        out["solutions.html"] = {"type": "resources", "alt": True, "heading": "Every solution page, by pillar", "intro": "Each page from the current site, rebuilt in the new templates with its FAQ and schema.", "items": sorted(sol, key=lambda x: (x[0], x[1]))}
    cit = [[p["file"].split("/")[-1].split("-")[0].title(), p["name"], p["one"], "Open the page", p["file"]] for p in migrated if p["ptype"] == "city"]
    if cit:
        out["locations.html"] = {"type": "resources", "alt": True, "heading": "Every city page", "intro": "One page per city and per service in that city, each with LocalBusiness and Service schema.", "items": sorted(cit, key=lambda x: (x[0], x[1]))}
    cs = [["Case study", p["name"], p["one"], "Read the case study", p["file"]] for p in migrated if p["ptype"] == "case study"]
    if cs:
        out["case-studies.html"] = {"type": "resources", "alt": True, "heading": "More case studies, in full", "intro": "Migrated from the PDFs and pages on the current site.", "items": sorted(cs, key=lambda x: x[1])}
    co = [["About", p["name"], p["one"], "Open the page", p["file"]] for p in migrated if p["ptype"] in ("company", "policy")]
    if co:
        out["about.html"] = {"type": "resources", "alt": True, "heading": f"More from {BRAND['name']}", "intro": "Every remaining page on the current site, kept and rebuilt.", "items": sorted(co, key=lambda x: x[1])}
    return out
