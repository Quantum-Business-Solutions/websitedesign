#!/usr/bin/env python3
"""Authoring script for brands/ramtech-building-systems.content.json.

Every fact is sourced from ramtechmodular.com (fetched by newclient.py, November 2026) or from the Client Command brief.
Anything that could not be sourced is listed in pitch["confirm"]. No em dashes, no exclamation marks.

    python3 brands/ramtech-building-systems.content.py
"""
import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ramtech-building-systems.content.json")
CLIENT_REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "out-ramtech-building-systems")

CLIENT = "Ramtech Building Systems"
SHORT = "Ramtech"
PHONE, PHONE_HREF = "(817) 473-9376", "tel:+18174739376"
EMAIL = "sales@ramtechmodular.com"
FOUNDED = "1982"
REGION = "tx"
SITE = "https://www.ramtechmodular.com"

TESTIMONIALS = []  # none published as text; the video narrations on the site are not reproduced as quotes
LOCATIONS = [  # slug, label, address 1, address 2, phone, phone href, region label, lon, lat
    ("mansfield", "Mansfield, Texas", "1400 US Hwy 287 South", "Mansfield, TX 76063", PHONE, PHONE_HREF, "Texas and the Southwest", -97.1417, 32.5632),
]
PARTNERS = ["Modular Building Institute", "Better Business Bureau", "BuyBoard", "TIPS"]  # affiliations shown on the home page footer band
AFFIL_NOTE = "Affiliations Ramtech shows on its own site."
SEAL_ITEMS = [
    ["Direct", "A manufacturer, not a broker", "Ramtech designs, engineers, manufactures and installs its own buildings, from a 20 acre plant in Mansfield, Texas."],
    ["One year", "Written warranty", "A full one-year written warranty on every new relocatable or permanent modular building Ramtech manufactures and installs in the continental U.S."],
    ["31", "Modular Building Institute Awards of Distinction", "Received since the program started in 1987."],
    ["No cost", "Project planning and budgeting", "A floor plan, a site plan, an exterior rendering, outlined specifications and a preliminary budget before any design fee."],
    ["Fixed", "A firm fixed price", "Ramtech states the price before any construction activity takes place."],
    ["Co-ops", "Buy through a purchasing cooperative", "For schools and government agencies, many buildings are available through the cooperatives Ramtech is a vendor for, including BuyBoard and TIPS."],
]
SEAL_SOURCE = "Sources: ramtechmodular.com warranty, awards, design-build, procurement options and relocatable purchase options pages."
TEAM = []

PRIMARY = {"label": "Start with no cost planning", "href": "contact.html"}
SECONDARY = {"label": "See what Ramtech builds", "href": "services.html"}

# slug, nav label, short, one-line, image, eyebrow, heading, subhead, benefits [[t,b]], included, faq
SERVICES = [
    ("education", "Education", "education buildings",
     "Portable classrooms to complete permanent campuses for public, private, charter and faith-based schools, colleges and vocational schools.",
     "assets/hero-education.jpg", "Education",
     "Modular school buildings, <em>from one classroom to a whole campus</em>.",
     "Since 1982 Ramtech has built relocatable and permanent modular school buildings for public, private and faith-based K-12 schools, colleges and vocational schools throughout the Southwest.",
     [["Portable classrooms and wings", "Single classrooms, and multiple classroom buildings from 4 to 16 classrooms, from standard floor plans or a custom design."],
      ["Labs, cafeterias and offices", "Computer lab classrooms, science labs, cafeterias and dining halls, administrative offices and restroom buildings."],
      ["Complete campuses", "Ramtech built 17 relocatable buildings, 69,776 square feet in all, for West ISD after the 2013 fertilizer plant explosion."],
      ["Three ways to build", "Relocatable, pier and beam permanent, or slab-on-grade permanent, chosen to fit the budget and how long the space is needed."]],
     ["Relocatable buildings for growth, interim space or leased use", "Permanent modular construction with site-applied finishes", "In-house space planning, design and engineering", "School-based health centers, content mastery and life skills classrooms", "Purchase through cooperatives such as BuyBoard and TIPS where the district is a member"],
     [["Can a school district buy through a cooperative?", "For schools and government agencies, many Ramtech relocatable buildings are available through the purchasing cooperatives Ramtech is a vendor for. Ask which cooperative your district belongs to."],
      ["Does Ramtech build more than portable classrooms?", "Yes. Ramtech builds classroom wings, labs, cafeterias, administrative offices, restroom buildings and complete permanent campuses."],
      ["Can the building be moved later?", "Relocatable buildings are designed for that. Permanent modular construction is designed to match the life expectancy of a site-built building."]]),
    ("healthcare", "Healthcare", "healthcare buildings",
     "Clinics, medical offices, imaging centers and specialty healthcare space, permanent or relocatable, in rural, remote and urban settings.",
     "assets/healthcare.jpg", "Healthcare",
     "Modular healthcare buildings, <em>permanent or relocatable</em>.",
     "Ramtech has built modular medical facilities, medical office buildings and specialty healthcare facilities for over three decades, with standard and customizable floor plans.",
     [["Clinics and medical offices", "Community health clinics, single-practitioner rural clinics and large medical office additions."],
      ["Diagnostic and specialty space", "Diagnostic imaging centers and other specialty healthcare facilities built to the technical needs of the use."],
      ["Where the need is", "Healthcare providers in remote, rural and urban locations, with a design-build team that handles the regulatory requirements."],
      ["Additions to what you have", "New facilities and additions designed to join existing structures."]],
     ["Slab-on-grade or pier and beam permanent modular construction", "Relocatable medical buildings for interim or leased space", "Standard medical floor plans and custom design", "Design, manufacturing, installation and finish-out from one company"],
     [["Do modular medical buildings meet the same codes?", "Ramtech states that its modular buildings are built to meet or exceed the same codes and standards as site-built facilities."],
      ["Can Ramtech build a small rural clinic?", "Yes. Ramtech names single-practitioner rural clinics and large urban medical office additions among the facilities it builds."]]),
    ("commercial", "Commercial", "commercial buildings",
     "Offices, industrial, retail and hospitality buildings, from small temporary facilities to large permanent ones.",
     "assets/commercial.jpg", "Commercial",
     "Commercial modular buildings <em>that fit the schedule</em>.",
     "Ramtech has worked with many of the country's largest companies, providing small and large modular buildings for industrial, office and retail use across the Southwest.",
     [["Offices and industrial", "Relocatable job-site offices and permanent commercial offices, new or as an addition to a building you have."],
      ["Repeatable designs", "A pier and beam dealership design built for Payne Automotive Group was made to be replicated across several South Texas locations."],
      ["Airport and hospitality", "Panama City-Bay County Airport selected Ramtech for a 7,168 square foot steel terminal expansion."],
      ["One team to manage", "Design-build removes the need to manage separate relationships with architects and contractors."]],
     ["No cost project planning and budgeting", "Slab-on-grade permanent modular construction for mid-size to large buildings", "Pier and beam permanent modular construction for small to medium buildings", "Relocatable buildings, purchased or leased"],
     [["How much can modular save?", "Ramtech states that its commercial approaches can save 10 to 25 percent in design and construction costs. The no cost planning step gives you a preliminary budget to check that against."],
      ["Can I lease a commercial modular building?", "Ramtech offers finance leases and relocatable leasing. A finance lease can allow 100 percent financing, and Ramtech's procurement page describes a $1 purchase at the end of the fixed term."]]),
    ("government", "Government", "government buildings",
     "Federal, regional, state and local agencies, from administrative offices and clinics to barracks and correctional facilities.",
     "assets/government.jpg", "Government",
     "Modular buildings for government, <em>built to the procurement requirements</em>.",
     "Since 1982 Ramtech has provided prefabricated building solutions to federal, regional, state and local government agencies, and has experience with their contracting requirements.",
     [["Offices, clinics and labs", "Administrative offices, medical clinics and medical labs for government agencies."],
      ["Barracks and quarters", "A 6,550 square foot temporary fire crew quarters at Vance Air Force Base in Enid, Oklahoma."],
      ["Public safety", "A 4,760 square foot police station and holding facility for the City of Clyde, Texas, and a 2,184 square foot police headquarters in Cottonwood Shores, Texas."],
      ["Secure facilities", "SCIFs, data and communication centers, built to ICD-705 requirements."]],
     ["Design-build, construction manager at risk and other delivery methods", "Purchase through cooperatives and directly from Ramtech", "Relocatable and permanent modular construction", "A one-year written warranty on every new building"],
     [["Which agencies does Ramtech work with?", "Ramtech names federal, regional, state and local agencies, including the Department of Defense and the Army Corps of Engineers, and has worked with FEMA on disaster recovery."],
      ["Can a government agency buy through a cooperative?", "In many cases yes. Ramtech is a vendor for select local, state and regional purchasing cooperatives."]]),
    ("permanent-modular-construction", "Permanent Modular Construction", "permanent modular construction",
     "Two ways to build a permanent modular building: slab-on-grade and pier and beam.",
     "assets/hero-main.jpg", "Permanent modular construction",
     "A permanent building that <em>comes off a factory floor</em>.",
     "Permanent modular construction combines the speed of prefabrication with site-applied interior and exterior finishes, at the same amenities and life expectancy as a site-built building.",
     [["Slab-on-grade", "Sections built with ceiling and walls attached but no floor, then crane set onto a concrete slab. For grade-level entries, medium to large projects and additions."],
      ["Pier and beam", "Small to medium projects with faster completion and less cost than site construction, and several forms of financing."],
      ["Two tracks at once", "The foundation is built on your site while the building sections are built in the plant."],
      ["Design-build", "Ramtech's own engineers, manufacturing and construction managers, working under one contract."]],
     ["No cost project planning and budgeting", "In-house engineering and design", "Site development and installation", "Delivery as design-build, construction manager at risk, or as a subcontractor to your prime contractor"],
     [["Is it as durable as site-built?", "Ramtech states that modular buildings use the same materials and are built to the same codes as site construction, and that they last as long as site-built structures when maintained."],
      ["What does design cost?", "After the preliminary budget is approved, Ramtech states the design fee rarely exceeds 2 percent of that budget."]]),
    ("relocatable-modular-buildings", "Relocatable Modular Buildings", "relocatable modular buildings",
     "Buildings built 60 to 80 percent complete in the plant, set on a concrete block foundation, and designed to be moved.",
     "assets/modular.jpg", "Relocatable modular buildings",
     "Relocatable buildings, <em>delivered and set where you need them</em>.",
     "From a double-wide portable classroom to a multiple-building complex, Ramtech builds relocatable modular buildings in Type V (wood) and Type II (steel) construction.",
     [["Fast", "Sections are typically built to 60 to 80 percent completion in the plant, then installed on a site-specific concrete block foundation."],
      ["Lower cost", "A less costly option for temporary or interim facilities, or space you lease for a limited period."],
      ["Less site disruption", "Final finish-out happens after the buildings are set and weathered in."],
      ["Move them later", "Designed to be reused or repurposed when the need changes."]],
     ["Needs analysis by designers, engineers and manufacturing and construction specialists", "A floor plan to fit your requirement and budget", "Delivery, set, skirting and final finish-out", "Concurrent multi-site capability"],
     [["Can I lease instead of buy?", "Yes. Ramtech's relocatable purchase options page covers purchase, leasing and financing alternatives."],
      ["Do relocatable buildings need a foundation?", "Yes, a site-specific concrete block foundation system."]]),
]

INDUSTRIES = [  # slug, name, image, one-line, body, bullets, faq
    ("multi-family-and-student-housing", "Multi-family and student housing", "assets/hero-main.jpg",
     "Apartments, student housing, hospitality, assisted living and specialty housing, built as permanent modular construction.",
     "Developers, owners and architects bring Ramtech projects with aggressive timelines, labor challenges and site constraints. Ramtech's project managers work through design, specification, engineering, construction and installation.",
     ["Student housing and university residence halls", "Workforce and employee housing", "Assisted living and senior housing", "Military and government housing", "Transitional and specialty housing"],
     [["Who is this for?", "Developers, owners, architects and investors planning multi-family apartments, student housing, hospitality, assisted living or specialty housing."]]),
    ("scif-buildings", "SCIF buildings", "assets/government.jpg",
     "Temporary and permanent modular buildings for SCIFs, data and communication centers and other secure computing facilities.",
     "Ramtech has provided these buildings for government and commercial clients for over 30 years, with experience working for the Department of Defense and the Army Corps of Engineers.",
     ["Sensitive Compartmented Information Facilities", "Data and communication centers", "Requirements of ICD-705", "Design-build delivery from one company"],
     [["Which standards apply?", "Ramtech's SCIF page names ICD-705 among the technical requirements it builds to."]]),
    ("disaster-recovery", "Disaster recovery", "assets/modular.jpg",
     "Temporary modular buildings and permanent space solutions to get a school, healthcare facility or business running again.",
     "Ramtech has worked with education, healthcare, government and commercial organizations after flooding, tornadoes, earthquakes, hurricanes and blast explosions, and with local, state and federal agencies including FEMA.",
     ["Temporary school campuses, including West ISD after the 2013 fertilizer plant explosion", "Schools destroyed by hurricane in the U.S. Virgin Islands", "A FEMA-funded temporary campus after flooding", "Navigation of the rebuilding process with local, state and federal authorities"],
     [["Does Ramtech work with FEMA?", "Ramtech states it has experience working with FEMA and with local, state and regional authorities on rebuilding."]]),
]

def desc(text, n=155):
    if len(text) <= n:
        return text
    cut = text[:n]
    return cut[:cut.rfind(" ")].rstrip(",;:") + "."


def brief(text, n=150):
    if len(text) <= n:
        return text
    cut = text[:n]
    i = max(cut.rfind(". "), cut.rfind("! "), cut.rfind("? "))
    return cut[:i + 1] if i > 60 else cut[:cut.rfind(" ")].rstrip(",;:") + "."


def _flow(fid, eyebrow, heading, intro, steps, receive_label="What you receive"):
    return {"type": "flow", "id": fid, "alt": True, "eyebrow": eyebrow, "heading": heading, "intro": intro, "receive_label": receive_label,
            "steps": [{"label": a, "when": b, "summary": c, "title": d, "body": e, "receive": f} for a, b, c, d, e, f in steps]}


def _ba(bid, heading, b_title, b_body, b_items, a_title, a_body, a_items, b_eyebrow="Site-built", a_eyebrow=f"With {SHORT}"):
    return {"type": "beforeafter", "id": bid, "eyebrow": "Before and after", "heading": heading,
            "before": {"eyebrow": b_eyebrow, "title": b_title, "body": b_body, "items": b_items},
            "after": {"eyebrow": a_eyebrow, "title": a_title, "body": a_body, "items": a_items}}


LEADFORM = {"type": "leadform", "alt": True, "id": "start", "heading": "Start with no cost project planning and budgeting",
            "body": "Tell us what you are building, where, and when you need it. Ramtech returns a floor plan, a site plan, an exterior rendering, outlined specifications and a preliminary budget.",
            "submit": "Request planning and budgeting", "note": "A person replies, not an autoresponder."}

SERVICE_INDEX = {s[0]: s for s in SERVICES}
WHEEL_ITEMS = [[s[1], brief(s[3], 140), f"services/{s[0]}.html", s[1]] for s in SERVICES]


def service_page(slug, navlabel, short, one, image, eyebrow, heading, subhead, benefits, included, faq):
    secs = [
        {"type": "hero", "layout": "split", "eyebrow": eyebrow, "heading": heading, "subhead": subhead,
         "primary": PRIMARY, "secondary": {"label": "All building types", "href": "services.html"},
         "image": image, "image_alt": f"{navlabel}: a Ramtech modular building", "image_w": 1200, "image_h": 800},
        {"type": "cards", "alt": True, "eyebrow": "What Ramtech builds", "heading": f"What {SHORT} brings to {short}", "items": benefits},
        {"type": "detail", "eyebrow": "What is included", "heading": "What you get", "body": "Everything below is published on ramtechmodular.com. The planning step comes first and carries no cost.", "bullets": included, "image": image, "image_alt": navlabel, "flip": True},
        {"type": "faq", "heading": f"Questions about {navlabel.lower()}", "items": faq},
        LEADFORM,
    ]
    return {"file": f"services/{slug}.html", "title": f"{navlabel} | {CLIENT}", "description": desc(f"{one} {subhead}".replace("<em>", "").replace("</em>", "")),
            "crumbs": [["Home", "index.html"], ["What we build", "services.html"], [navlabel, f"services/{slug}.html"]], "sections": secs}


def industry_page(slug, name, image, one, body, bullets, faq):
    return {"file": f"specialty/{slug}.html", "title": f"{name} | {CLIENT}", "description": desc(one + " " + body),
            "crumbs": [["Home", "index.html"], ["Specialty", "industries.html"], [name, f"specialty/{slug}.html"]],
            "sections": [
                {"type": "hero", "layout": "split", "eyebrow": "Specialty", "heading": f"<em>{name}</em>, built modular.", "subhead": one, "primary": PRIMARY, "secondary": SECONDARY,
                 "image": image, "image_alt": name, "image_w": 1200, "image_h": 800},
                {"type": "detail", "alt": True, "eyebrow": "What Ramtech does here", "heading": f"{name} with Ramtech", "body": body, "bullets": bullets},
                {"type": "faq", "heading": f"Questions about {name.lower()}", "items": faq},
                LEADFORM]}


def location_page(slug, label, a1, a2, phone, phone_href, region, lon, lat):
    return {"file": f"locations/{slug}.html", "title": f"Modular Buildings in Mansfield, TX | {CLIENT}",
            "description": f"Ramtech Building Systems designs, manufactures and installs modular buildings from its plant at {a1}, {a2}. Call {phone}.",
            "crumbs": [["Home", "index.html"], ["Locations", "locations.html"], [label, f"locations/{slug}.html"]],
            "schema": [{"@context": "https://schema.org", "@type": "GeneralContractor", "@id": f"{SITE}/#mansfield", "name": CLIENT,
                        "telephone": "+1-817-473-9376", "email": EMAIL, "url": SITE + "/",
                        "address": {"@type": "PostalAddress", "streetAddress": a1, "addressLocality": "Mansfield", "addressRegion": "TX", "postalCode": "76063", "addressCountry": "US"},
                        "geo": {"@type": "GeoCoordinates", "latitude": lat, "longitude": lon}}],
            "sections": [
                {"type": "hero", "layout": "split", "eyebrow": "Headquarters and plant", "heading": "Designed, built and shipped from <em>Mansfield, Texas</em>.",
                 "subhead": "Ramtech's manufacturing plant sits on a 20 acre site in Mansfield, where the company has operated since it became a direct manufacturer.",
                 "primary": {"label": f"Call {phone}", "href": phone_href}, "secondary": PRIMARY,
                 "image": "assets/hero-main.jpg", "image_alt": "A Ramtech modular building", "image_w": 1200, "image_h": 800},
                {"type": "locations", "heading": "Visit or call", "intro": f"{a1}, {a2}. Email {EMAIL}.", "items": [[label, a1, a2, phone, phone_href]]},
                {"type": "faq", "heading": "Questions about where Ramtech works", "items": [
                    ["Where does Ramtech build?", "Ramtech serves markets across the USA and has built throughout the Southwest, with projects in Texas, Oklahoma and Arkansas, among others."],
                    ["Does Ramtech work outside Texas?", "Yes. Ramtech's own project profiles include buildings in Oklahoma and Arkansas and disaster recovery work in the U.S. Virgin Islands."]]},
                LEADFORM]}


FLOW = _flow("flow", "How a project runs", "Four stages, and the first one costs nothing",
             "Ramtech describes its design-build process on its own site. Click a stage.",
             [("Plan", "Before any fee", "A programming meeting, then no cost project planning and budgeting.", "No cost project planning and budgeting",
               "After an initial programming meeting Ramtech prepares the first set of drawings and a preliminary budget.", ["A basic floor plan and site plan", "An exterior rendering", "Outlined building specifications", "A preliminary budget"]),
              ("Design", "After the budget is approved", "A more in-depth programming meeting and design review.", "Design and a firm price",
               "The design phase begins with a fee that Ramtech states rarely exceeds 2 percent of the preliminary budget.", ["Detailed design", "A firm fixed price before construction begins"]),
              ("Build", "Two tracks at once", "The foundation on your site, the building in the plant.", "Manufacturing and site work together",
               "Ramtech builds a site-specific foundation while the building sections are manufactured in Mansfield.", ["Site development", "Building sections made in the plant"]),
              ("Set and finish", "Delivery", "Sections are shipped, set, weathered in and finished out.", "Installation and finish-out",
               "The sections are set on the foundation and the final finish-out is performed by Ramtech.", ["A finished building", "A one-year written warranty from occupancy"])])
BEFORE_AFTER = _ba("ba", "Drag to compare site-built with the Ramtech sequence",
                   "One step, then the next", "On a conventional site-built project, foundation, structure and finishes follow one another in order.",
                   ["Work waits on weather", "More general conditions cost", "Multiple contractors to coordinate"],
                   "Two tracks at once", "At Ramtech the foundation is built on site while the building sections are made in the plant. Ramtech states this is typically 25 to 40 percent faster than site construction.",
                   ["Factory-controlled production", "Up to 10 to 25 percent lower design and construction costs, as Ramtech states", "Design, manufacturing and construction under one roof"])
SEAL = {"type": "seal", "id": "seal", "eyebrow": f"What every {SHORT} customer gets", "heading": "Not a slogan. A list you can check.", "intro": "Each line is published on ramtechmodular.com.", "items": SEAL_ITEMS, "source": SEAL_SOURCE}
HISTORY = {"type": "timeline", "id": "story", "eyebrow": f"Since {FOUNDED}", "heading": "From a dealership in Arlington to a 20 acre plant", "intro": "The dates Ramtech publishes. The rest are on the To confirm list.",
           "items": [["1982", "Ramtech Modular Design opens", "A small modular dealership in Arlington, Texas, in an industry then controlled by large leasing companies."],
                     ["The plant", "A direct manufacturer in Mansfield", "Frustrated by the product available for complex projects, Ramtech opened its own manufacturing plant on the 20 acre site it still occupies."],
                     ["1987", "First Awards of Distinction year", "The Modular Building Institute awards program starts. Ramtech has since received 31."],
                     ["Today", "More than 3,500 projects", "Ramtech serves on the Texas Industrial Building Code Council and holds leadership positions with the Modular Building Institute."]]}


def build():
    brand = {
        "accent": "#cd2122", "ink_secondary": "#181818", "chrome": "dark", "chrome_bg": "#181818",
        "logo": "assets/logo.png", "logo_alt": CLIENT, "logo_w": 420, "logo_h": 180,
        "logo_note": "White wordmark fetched from the live site, so the header and footer sit on a dark ground. Ask for the vector.",
        "phone": PHONE, "phone_href": PHONE_HREF, "email": EMAIL,
        "utility": [{"label": "Warranty", "href": "about.html#warranty"}, {"label": "FAQ", "href": "faq.html"}],
        "cta": PRIMARY,
        "sticky": {"primary": "Start with no cost planning", "primary_href": "contact.html", "secondary": f"Call {SHORT}", "secondary_href": PHONE_HREF},
        "launcher": {"label": "Plan a project", "eyebrow": "The fast lane", "title": "What do you need?", "links": [["Education", "services/education.html"], ["Healthcare", "services/healthcare.html"], ["Commercial", "services/commercial.html"], ["Government", "services/government.html"], ["Frequently asked questions", "faq.html"]],
                     "note": "A person at the Mansfield plant replies.", "phone": PHONE, "phone_href": PHONE_HREF},
        "social": {"facebook": "https://www.facebook.com/RamtechBuildingSystems/", "linkedin": "https://www.linkedin.com/company/ramtech-building-systems-inc-", "youtube": "https://www.youtube.com/user/RamtechGroup", "x": "https://x.com/RamtechModular"},
        "tagline": "Design-build leader in commercial modular construction since 1982. A direct manufacturer in Mansfield, Texas.",
        "footer_columns": [
            {"title": "What we build", "links": [[s[1], f"services/{s[0]}.html"] for s in SERVICES]},
            {"title": "Specialty", "links": [[i[1], f"specialty/{i[0]}.html"] for i in INDUSTRIES]},
            {"title": "Company", "links": [["About", "about.html"], ["Locations", "locations.html"], ["FAQ", "faq.html"], ["Contact", "contact.html"]]},
        ],
        "legal": [["Privacy policy", SITE + "/privacy-policy/"], ["Terms of use", SITE + "/terms-of-service/"]],
    }
    schema = {"org_name": "Ramtech Building Systems, Inc.", "org_url": SITE + "/", "org_logo": "https://y4f9m6d2.delivery.rocketcdn.me/wp-content/uploads/2017/11/Ramtech-Logo.png",
              "org_description": "Design-build leader in commercial modular construction since 1982 and a direct manufacturer of relocatable and permanent modular buildings for education, healthcare, commercial and government buyers in the Southwest, from Mansfield, Texas.",
              "sameAs": [brand["social"][k] for k in brand["social"]], "telephone": "+1-817-473-9376"}
    schema.update({"founded": FOUNDED, "short_name": SHORT, "title_city": "Texas",
                   "cities": ["Mansfield", "Texas", "TX", "Southwest"],
                   "area_served": [{"@type": "State", "name": "Texas"}, {"@type": "State", "name": "Oklahoma"}],
                   "meta_tail": "Ramtech Building Systems, a modular design-build manufacturer in Mansfield, Texas since 1982.",
                   "local": [{"slug": l[0], "name": CLIENT, "street": l[2], "city": "Mansfield", "region": "TX", "postal": "76063", "telephone": "+1-817-473-9376", "lat": l[8], "lon": l[7]} for l in LOCATIONS]})
    nav = [
        {"label": "What we build", "href": "services.html", "children": [[s[1], f"services/{s[0]}.html"] for s in SERVICES]},
        {"label": "Specialty", "href": "industries.html", "children": [[i[1], f"specialty/{i[0]}.html"] for i in INDUSTRIES]},
        {"label": "About", "href": "about.html", "children": [["About Ramtech", "about.html"], ["Locations", "locations.html"], ["FAQ", "faq.html"], ["Contact", "contact.html"]]},
    ]
    faq_home = [["How much faster is modular?", "Ramtech states that modular construction is usually 25 to 40 percent faster than site construction, because the foundation and the building are made at the same time."],
                ["Is modular as durable as site-built?", "Ramtech states that modular buildings use the same materials and are built to the same codes as site construction, and last as long when maintained."],
                ["What does the no cost planning cover?", "A floor plan, a site plan, an exterior rendering, outlined specifications and a preliminary budget, before any design fee."],
                ["Can we buy through a purchasing cooperative?", "For schools and government agencies, many buildings are available through the cooperatives Ramtech is a vendor for, including BuyBoard and TIPS."],
                ["What is the warranty?", "A full one-year written warranty from the date of occupancy on every new building Ramtech manufactures and installs in the continental U.S."]]
    pages = []
    pages.append({"file": "index.html", "title": f"{CLIENT} | Modular buildings from a Texas design-build manufacturer",
                  "compose": {
                      "showcase": ["hero-light", "partners", "wheel", "ba", "flow", "proof", "story", "faq", "contact"],
                      "clean": ["hero-light", "partners", "seal", "wheel", "is-this-you", "flow", "story", "faq", "contact"],
                      "press": ["hero-light", "story", "services", "seal", "proof", "flow", "faq", "contact"]},
                  "description": "A design-build leader in commercial modular construction since 1982. Direct manufacturer of relocatable and permanent modular buildings, Mansfield, Texas.",
                  "sections": [
        {"type": "hero", "id": "hero-light", "layout": "split", "eyebrow": "Mansfield, Texas. Modular construction since 1982.",
         "stats": [["1982", "Specializing in commercial modular since"], ["3,500+", "Projects completed"], ["31", "MBI Awards of Distinction"], ["20 acres", "Manufacturing site in Mansfield"]],
         "ribbon": ["Modular Building Institute", "BuyBoard", "TIPS", "BBB"],
         "variants": {"press": {"stats": None, "ribbon": ["Mansfield, Texas. Since 1982.", "A direct manufacturer", "31 Awards of Distinction"]}},
         "heading": "A design-build leader in <em>modular building construction</em>.",
         "subhead": "Ramtech designs, manufactures and installs relocatable and permanent modular buildings for schools, healthcare providers, government agencies and commercial buyers, with no cost project planning and budgeting to start.",
         "primary": PRIMARY, "secondary": SECONDARY,
         "note": "Photographs are Ramtech's own, from ramtechmodular.com",
         "image": "assets/hero-main.jpg", "image_alt": "A two-story Ramtech modular building with a red metal roof and brick exterior", "image_w": 1200, "image_h": 800,
         "badge": {"value": "31", "label": "Modular Building Institute Awards of Distinction"}},
        {"type": "partners", "id": "partners", "caption": AFFIL_NOTE, "items": PARTNERS},
        SEAL,
        {"type": "wheel", "id": "wheel", "eyebrow": "What Ramtech builds", "heading": "Four markets, two ways to build", "intro": "Hover a segment. Education, healthcare, commercial and government, in permanent or relocatable construction.", "items": WHEEL_ITEMS, "hub": "Ramtech", "hub_sub": "design-build", "ring": "MODULAR BUILDINGS FOR THE SOUTHWEST", "panel_eyebrow": "Hover a segment", "link_label": "See the building type"},
        {"type": "checklist", "id": "is-this-you", "alt": True, "eyebrow": "Is this you?", "heading": "Six signs modular is worth pricing",
         "intro": "Check what sounds familiar.",
         "items": ["Enrollment grew faster than the building plan", "A lease on portable buildings is ending", "The space is needed before a site-built schedule can deliver it", "A clinic is needed where there is none", "The budget has to be known before design starts", "The building may need to move someday"],
         "messages": ["Check what sounds familiar.", "One is normal.", "Two is worth a conversation.", "Three or more, and the no cost planning step is the place to start."],
         "cta_label": "Start with no cost planning", "cta_href": "contact.html"},
        {"type": "services", "id": "services", "heading": "What Ramtech builds", "intro": "Four markets and two ways to build, each with its own page.",
         "items": [[s[1], s[3], f"services/{s[0]}.html"] for s in SERVICES]},
        FLOW, BEFORE_AFTER,
        {"type": "proof", "id": "proof", "alt": True, "eyebrow": "Counted, not claimed", "value": "31", "text": "Modular Building Institute Awards of Distinction received since the program started in 1987, for excellence in design, manufacturing and construction.", "source": "Source: ramtechmodular.com/awards"},
        HISTORY,
        {"type": "faq", "id": "faq", "alt": True, "heading": "Questions we get on the first call", "items": faq_home},
        {"type": "contact", "id": "contact", "heading": "Start with no cost project planning and budgeting", "body": "Tell us what you are building, where, and when you need it. Call the plant at " + PHONE + " or send the form.",
         "options": ["Education", "Healthcare", "Commercial", "Government", "Permanent modular construction", "Relocatable modular buildings", "Multi-family or student housing", "Something else"], "submit": "Request planning and budgeting", "note": "A person replies, not an autoresponder."},
    ]})
    pages.append({"file": "services.html", "title": f"What We Build | Modular buildings | {CLIENT}",
                  "description": "Education, healthcare, commercial and government buildings, in permanent or relocatable modular construction. Ramtech designs, manufactures and installs.",
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "What we build", "heading": "Four markets, <em>two ways to build</em>.", "subhead": "Ramtech designs, manufactures and installs modular buildings for education, healthcare, commercial and government buyers, in permanent or relocatable construction.", "primary": PRIMARY},
        {"type": "wheel", "id": "wheel", "eyebrow": "What Ramtech builds", "heading": "Hover a segment", "intro": "Each line has its own page.", "items": WHEEL_ITEMS, "hub": "Ramtech", "hub_sub": "design-build", "ring": "MODULAR BUILDINGS FOR THE SOUTHWEST", "panel_eyebrow": "Hover a segment", "link_label": "See the building type"},
        {"type": "resources", "heading": "The six lines", "intro": "What Ramtech builds, what is included, and the questions people ask.", "items": [[s[1], s[1], brief(s[3], 140), f"See {s[1].lower()}", f"services/{s[0]}.html"] for s in SERVICES]},
        LEADFORM]})
    for s in SERVICES:
        pages.append(service_page(*s))
    pages.append({"file": "industries.html", "title": f"Specialty Buildings | Housing, SCIF, disaster recovery | {CLIENT}",
                  "description": "Multi-family and student housing, SCIF buildings and disaster recovery space, built as modular construction by Ramtech Building Systems in Mansfield, Texas.",
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "Specialty", "heading": "Housing, secure facilities and <em>disaster recovery</em>.", "subhead": "Three kinds of project that Ramtech builds across its markets, each with its own page.", "primary": PRIMARY},
        {"type": "resources", "heading": "Specialty buildings", "intro": "Where Ramtech's design-build team is most often asked for something particular.", "items": [[i[1], i[1], brief(i[3], 140), f"See {i[1].lower()}", f"specialty/{i[0]}.html"] for i in INDUSTRIES]},
        LEADFORM]})
    for i in INDUSTRIES:
        pages.append(industry_page(*i))
    pages.append({"file": "about.html", "title": f"About {CLIENT} | Modular design-build since 1982", "description": "Ramtech began as a small modular dealership in Arlington, Texas in 1982 and now manufactures its own buildings on a 20 acre site in Mansfield.",
                  "sections": [
        {"type": "hero", "layout": "split", "eyebrow": "About Ramtech", "heading": "Design, manufacturing and construction, <em>since 1982</em>.", "subhead": "Ramtech has provided more modular buildings to government agencies, schools, healthcare providers and commercial organizations than any other company in the Southwest, by its own account.", "primary": PRIMARY, "secondary": {"label": "Locations", "href": "locations.html"},
         "image": "assets/difference.jpg", "image_alt": "Ramtech modular building", "image_w": 1200, "image_h": 800},
        {"type": "stats", "alt": True, "items": [["1982", "Specializing in commercial modular"], ["3,500+", "Projects completed"], ["31", "MBI Awards of Distinction"], ["20 acres", "Manufacturing site in Mansfield"]]},
        {"type": "cards", "eyebrow": "The Ramtech difference", "heading": "Three capabilities", "items": [
            ["Design", "Experienced designers across every discipline produce efficient, economical building layouts and facades."],
            ["Manufacturing", "Complete in-house space planning, design, manufacturing and engineering on every project."],
            ["Construction", "A single-source solution for site development and building installation, from start to finish."]]},
        HISTORY,
        {"type": "detail", "id": "warranty", "alt": True, "eyebrow": "Warranty", "heading": "One year, in writing", "body": "Ramtech provides a full one-year written warranty on every new relocatable or permanent modular building it manufactures and installs in the continental U.S. The period runs from the date of occupancy and covers defects in materials and workmanship under normal use. Equipment Ramtech buys from recognized manufacturers, such as heating and air-conditioning equipment and water heaters, typically carries its own warranty.",
         "bullets": ["Covers defects in materials and workmanship", "Repair or replacement at no charge during the year", "Applies to relocatable and permanent buildings"]},
        {"type": "partners", "id": "affiliations", "caption": AFFIL_NOTE, "items": PARTNERS},
        LEADFORM]})
    pages.append({"file": "locations.html", "title": "Locations | Ramtech Building Systems, Mansfield, Texas", "description": "Ramtech Building Systems is at 1400 US Hwy 287 South, Mansfield, Texas 76063, with a 20 acre manufacturing site. Call (817) 473-9376 or email sales.",
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "Locations", "heading": "One plant, <em>markets across the USA</em>.", "subhead": f"Ramtech designs and manufactures in Mansfield, Texas. Call {PHONE}.", "primary": {"label": f"Call {PHONE}", "href": PHONE_HREF}},
        {"type": "locations", "detailed": True, "heading": "Where we are", "intro": "Headquarters and manufacturing site.", "items": [[l[1], l[2], l[3], l[4], l[5]] for l in LOCATIONS]},
        LEADFORM]})
    for l in LOCATIONS:
        pages.append(location_page(*l[:2], *l[2:6], l[6], l[7], l[8]))
    pages.append({"file": "faq.html", "title": f"FAQ | Modular construction questions | {CLIENT}", "description": "Straight answers on modular construction: cost, speed, durability, relocatable versus permanent, purchasing cooperatives, financing and warranty.",
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "FAQ", "heading": "Questions, <em>answered plainly</em>.", "subhead": "Answers drawn from Ramtech's own FAQ. If yours is not here, call or send the form."},
        {"type": "faq", "heading": "About modular construction", "items": faq_home + [
            ["What is modular construction?", "Controlled off-site factory production of engineered building sections, typically built 50 to 90 percent complete, then transported to the site, assembled and finished."],
            ["What is the difference between relocatable and permanent?", "Both are made in the plant with the same materials as site-built structures. Relocatable buildings sit on a concrete block foundation and can be moved. Permanent buildings use a pier and beam or slab-on-grade foundation and site-applied finishes."],
            ["Can I finance a modular building?", "Ramtech works with third-party finance companies, including finance leases, and can help you compare options."]]},
        LEADFORM]})
    pages.append({"file": "contact.html", "title": f"Contact | Start a project | {CLIENT}", "description": f"Call Ramtech at {PHONE} or send the form. 1400 US Hwy 287 South, Mansfield, TX 76063. Start with no cost project planning and budgeting.",
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "Contact", "heading": "Start a project, <em>or just call</em>.", "subhead": f"Tell us what you are building, where and when. Call {PHONE} or email {EMAIL}."},
        {"type": "contact", "id": "form", "heading": "Start with no cost planning and budgeting", "body": "Choose what you are thinking about.",
         "options": ["Education", "Healthcare", "Commercial", "Government", "Permanent modular construction", "Relocatable modular buildings", "Multi-family or student housing", "Something else"], "submit": "Request planning and budgeting", "note": "A person replies, not an autoresponder."},
        {"type": "locations", "alt": True, "heading": "Or visit the plant", "intro": "Headquarters and manufacturing.", "items": [[l[1], l[2], l[3], l[4], l[5]] for l in LOCATIONS]},
    ]})

    pitch = {
        "qbs_contact": {"name": "Shawn", "email": "shawn@thequantumleap.business", "phone": ""},
        "prepared_for": "Ramtech Building Systems",
        "heard_intro": "Ramtech is a prospect, so nothing here comes from a conversation. Everything comes from ramtechmodular.com and the brief Quantum filled in. Tell us where it is wrong; your words outrank ours.",
        "heard": ["The brief has no stated promise. The site's own headline is 'Ramtech is a design-build leader in modular building construction'; we used it, marked unconfirmed.",
                  "No likes, dislikes or ground preference were given. We chose the house light set.",
                  "Notes in the brief: design-build leader since 1982, direct manufacturer, more than 3,500 projects, the most modular buildings delivered to government, education, healthcare and commercial buyers in the Southwest.",
                  "The offer to lead with is no cost project planning and budgeting."],
        "found": ["829 URLs in the sitemap, 765 of them blog posts and image attachment pages. Average page score 44 of 100 (Quantum audit, November 2026).",
                  "No page title names a city. 517 pages are under 300 words, and only 2 carry FAQ markup.",
                  "Two figures disagree: the home page and Ramtech story say more than 3,500 projects; the Ramtech difference page says more than 4,000.",
                  "The site is open to AI crawlers (robots.txt allows them) but has no llms.txt file. The search and AI analysis for this domain has not been run, so no traffic figures appear here."],
        "choose_heading": "Three directions. Your call.",
        "choose_intro": "The words, the pages and the proof are identical in all three. What differs is the register. Open each one on your phone and tell us which feels like Ramtech.",
        "choose_reasons": [["If a plain, procedural site is the argument", "Clean: white ground, a humanist sans, hairline cards. Built for the facility manager, school business officer or procurement lead reading a page in order."],
                           ["If a contemporary, confident look is the argument", "Showcase: image-led, rounded, more sales-forward. Shows the buildings first."],
                           ["If established is the argument", "Press: warm paper and a serif. Reads like the company that has been building since 1982."]],
        "pick_reasons": [["Buyers read to compare", "School districts, agencies and healthcare administrators comparing builders want the process, the contract routes and the proof on the page. Clean puts them first."],
                         ["The proof is procedural", "No cost planning, a firm fixed price, a one-year warranty, purchasing cooperatives: Clean lets each one sit in a plain list a buyer can check."],
                         ["It will age well", "A 40-year-old builder that makes things should not look trendy. Clean is quiet enough for the buildings to be the subject."]],
        "pick_change": "The Ramtech photographs are 2017 to 2019 and several are small. We would commission a current set of finished buildings before launch; the hero carries the whole page.",
        "alternatives": [["Quantum Showcase", "The safe, sales-forward one: big building photographs, a wheel of the four markets, a drag comparison of site-built and modular sequences."],
                         ["Quantum Press", "The wildcard: serif headlines on warm paper, the 1982 story high on the page. Nobody in modular construction looks like this."]],
        "plan": [["Weeks 1 to 2", "Choose a direction. Resolve the items under To confirm, starting with the promise and the project count."],
                 ["Weeks 3 to 4", "Copy review with Ramtech: the project profiles, the floor plans library, and which blog posts are worth keeping."],
                 ["Weeks 5 to 7", "Build in HubSpot: theme, templates, every page, forms routed to the right person at the plant."],
                 ["Weeks 8 to 9", "Review rounds, a permanent redirect for every URL that exists today, QA on the same gate this preview passed."],
                 ["Week 10", "Launch with the baseline captured the day before."],
                 ["Days 60 to 90", "Measure against the baseline and decide the first articles from the questions buyers ask."]],
        "search": {"heading": "Where you stand in search today", "intro": "The search and AI analysis for this domain has not been pulled.", "as_of": "not pulled", "today_stats": [], "today": [], "after": [], "keep": [], "note": ""},
        "confirm": [
            "Who this is for. The brief says Ramtech is a prospect and lists Kelly Williams as a possible contact on our side, unconfirmed. Kelly Williams is named on Ramtech's own site as its Vice President of Business Development. Confirm who at Ramtech receives this.",
            "The promise. The brief gives none. We used the home page headline, 'a design-build leader in modular building construction'.",
            "The project count. The home page and the Ramtech story say more than 3,500; the Ramtech difference page says more than 4,000. We used 3,500.",
            "Accent and header colour. The brief gives none. #cd2122 (red) is the most frequent colour in Ramtech's child theme stylesheet and matches the roofs in the photographs; #181818 is the header ground because the logo is white. Neither was checked against brand guidelines.",
            "The logo is a white-type PNG fetched from the live site. Ask for the vector and a dark-type version.",
            "Photographs are Ramtech's own, 2017 to 2019, taken from the live site. Which project is in which photograph is not captioned on the site, so alt text is descriptive only.",
            "No written testimonials. The site features video narrations by Marty Crawford (West ISD) and Rev. John Wilke (Immanuel Lutheran Church and School), but no quoted text. Nothing is attributed to them here.",
            "Named people. Ramtech's design team page names nobody, so no team section appears.",
            "Mansfield coordinates (32.5632, -97.1417) are approximate, used only for schema markup.",
            "The map section is left out because the map module has no Texas outline and Ramtech lists one location.",
            "Financing and lease figures on the specialty pages come from Ramtech's procurement pages: confirm the $1 end-of-lease purchase and 100 percent financing still apply.",
            "The SCIF page was only partly readable in our fetch; the standards named here are ICD-705 only.",
            "The 31 Awards of Distinction, and 'since 1987', come from the awards page; confirm the current count.",
            "No search or AI analysis was run, so there is no search package on the hub.",
        ],
        "footer": "Prepared for Ramtech Building Systems. Nothing here is live or indexed. Photographs are Ramtech's own, taken from ramtechmodular.com. Facts we could not source are listed under To confirm.",
    }
    return {"client": CLIENT, "slug": "ramtech-building-systems", "domain_hint": "ramtechmodular.com", "brand": brand, "schema": schema, "nav": nav, "pages": pages, "pitch": pitch}


if __name__ == "__main__":
    data = build()
    with open(OUT, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print(f"wrote {OUT}: {len(data['pages'])} pages")
