#!/usr/bin/env python3
"""Authoring script for brands/tellabs.content.json.

Every fact is SOURCED from tellabs.com (fetched 19 November 2026) or from the Client Command brief.
Anything that could not be sourced is listed under pitch["confirm"]. No em dashes, no exclamation marks.

    python3 brands/tellabs.content.py
"""
import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tellabs.content.json")
CLIENT_REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "out-tellabs")

CLIENT = "Tellabs"
SHORT = "Tellabs"
LEGAL = "Tellabs Access, LLC"                      # footer of tellabs.com
PHONE, PHONE_HREF = "+1 800 690 2324", "tel:+18006902324"   # contact page: North America toll free, sales questions
HQ = ["4240 International Pkwy, Suite 105", "Carrollton, TX 75007"]  # about page
EMAIL = "ask@tellabs.com"                          # header of tellabs.com
NEXUS, DOCS, FORUMS = "https://nexus.tellabs.com/", "https://docs.tellabs.com", "https://forums.tellabs.com"
LIVE = "https://tellabs.com"
PROMISE = "Tellabs Optical LAN gives your building a simpler, more secure network that costs less to run, backed by carrier-grade engineering."

IMG_HERO, IMG_RACK, IMG_CAMPUS, IMG_PLANT, IMG_TRAIN, IMG_BUILD = (
    "assets/hero-1200.jpg", "assets/rack-1200.jpg", "assets/campus-1200.jpg", "assets/plant-1200.jpg", "assets/training-1200.jpg", "assets/building-1600.jpg")

# ------------------------------------------------------------------ helpers
def desc(text, n=158):
    if len(text) <= n:
        return text
    cut = text[:n]
    return cut[:cut.rfind(" ")].rstrip(",;:") + "."


def brief(text, n=150):
    if len(text) <= n:
        return text
    cut = text[:n]
    i = max(cut.rfind(". "), cut.rfind("? "))
    return cut[:i + 1] if i > 60 else cut[:cut.rfind(" ")].rstrip(",;:") + "."


def fit(text, lo=140, hi=160, pad=None):
    """Description between lo and hi characters: whole sentences, then padded with a tail if short."""
    t = desc(text, hi)
    if len(t) < lo and pad:
        t = desc(t.rstrip(".") + ". " + pad, hi)
    return t


# ------------------------------------------------------------------ sourced facts (tellabs.com)
TESTIMONIALS = [  # case study, Santa Fe Public Schools (Oct 2021), quote as published
    ["The Tellabs Optical LAN solution allows SFPS not only to be sustainable but also cost-effective. It allows us to reduce our costs and then apply those savings to investments in other areas of education.",
     "Elias Bernardino", "Executive Director of the SFPS Technology Department, Santa Fe Public Schools"],
]
PARTNERS = ["Connectix Cabling Systems", "Fleming Communications", "Communication Technology Services", "A/Z Corporation", "Winward Electrical Services",
            "General Dynamics Information Technology", "M.C. Dean", "ITConnect", "Vision Technologies", "VT Group", "Magellan Network Services", "Tempest Telecom Solutions"]
ASSOCIATIONS = ["APOLAN", "TIA", "BICSI", "AFCEA", "Broadband Forum", "UNH-IOL", "HTNG"]
ASSOC_FULL = [["Association for Passive Optical LAN (APOLAN)", "A non-profit of manufacturers, distributors, integrators and consultants that advocates education and global adoption of passive optical for enterprise networks."],
              ["Telecommunications Industry Association (TIA)", "The trade association for the global information and communications technology industry, through standards, policy and market intelligence."],
              ["BICSI", "A professional association supporting the information and communications technology community."],
              ["Armed Forces Communications and Electronics Association (AFCEA)", "A non-profit member association for cyber, command, control, communications and intelligence."],
              ["Broadband Forum", "A non-profit consortium accelerating broadband innovation, standards and ecosystem development."],
              ["Hospitality Technology Next Generation (HTNG)", "A not-for-profit association of hospitality professionals and technology providers."],
              ["University of New Hampshire InterOperability Laboratory", "An independent proving ground that tests networking and data communications products."]]
LEADERS = [["Rich Schroder", "President and CEO"], ["Susan Merrill", "Chief Financial Officer"], ["Karen Leos", "Vice President, Global Sales and Professional Services"], ["Tom Dobozy", "Vice President, Engineering"]]
LEADER_LINKS = {"Rich Schroder": LIVE + "/about/leadership/", "Susan Merrill": LIVE + "/about/leadership/", "Karen Leos": LIVE + "/about/leadership/", "Tom Dobozy": LIVE + "/about/leadership/"}

INDUSTRIES = [  # slug, name, image, one-line, body, bullets, faq   (all from tellabs.com/solutions/industries/*)
    ["enterprise", "Enterprise", IMG_BUILD,
     "The choice for simple, secure, scalable and stable connectivity inside buildings and across extended campuses.",
     "Enterprise network architecture is stagnant while demands on LAN services, infrastructure and operations keep rising with IoT, cloud, SDN, security and wireless. The usual fix adds complexity, human touch and cost. Optical LAN builds a modern network that is simple, flexible and secure, and costs less to buy on day one and to run year over year.",
     ["Speeds IT productivity through simplification", "Reduces network vulnerability points", "Flexible capacity and density, sized to the building", "Fiber is inherently more secure than copper", "A graceful migration path to future technologies"],
     [["Is Optical LAN a new technology?", "No. Tellabs installed its first Optical LAN networks in 2008, and its passive optical equipment was in service for Verizon FiOS from 2003."], ["Does it change what we plug in?", "No. Existing voice, video, data and Wi-Fi services keep working with no change to the core or the end devices."]]],
    ["education", "Education", IMG_CAMPUS,
     "One network across classrooms, labs, libraries and campuses, at a lower operating cost for administrators.",
     "Students, teachers and staff rely on secure, stable networks, while funding pressure makes it hard to meet demand. Optical LAN unifies and extends networks across schools, colleges and universities with fewer electronics, centralized management and fiber reach of 12 to 18 miles, so one central data center can serve a whole district.",
     ["Fewer electronics moving parts to operate and replace", "Centralized network intelligence and management", "Interconnects far-reaching campus buildings", "Reduces energy, plastics and other materials", "Matches the eRate goal of moving away from legacy interconnect in a cost-conscious manner"],
     [["Is there a school district example?", "Yes. Santa Fe Public Schools chose Tellabs Optical LAN for its K-12 campuses. The published case study reports a 10-year total cost of ownership of $433K against $2.1M for a legacy LAN."], ["Does it cover K-12 and higher education?", "Both. The education page covers K-12, higher education and eRate."]]],
    ["government", "Government", IMG_RACK,
     "A fiber-based network for civilian, defense, and state and local agencies, with a smaller attack surface.",
     "Government networks face growing cybersecurity threats while leadership, mission and budgets keep changing. Passive optical networking flattens and simplifies network design, reduces vulnerabilities, suits zero trust architecture and has centralized, software-defined management. Tellabs states Optical LAN offers 320:1 less attack surface and 6:1 fewer IT staff touches.",
     ["Civilian, defense, and state and local agencies", "Zero trust architecture with fewer points to attack", "Software-defined, centralized management", "Proven across government markets", "Published as STIG-compliant and deployed in military networks"],
     [["Has Optical LAN been certified for defense use?", "The Tellabs timeline records US Department of Defense JITC certification in 2010, followed by many DoD deployments."], ["Where do the 320:1 and 6:1 figures come from?", "They are Tellabs figures published on its Optical LAN and Government pages. Ask Tellabs for the method behind them."]]],
    ["healthcare", "Healthcare", IMG_RACK,
     "A network built for critical care, patient records and the growth of connected devices.",
     "Healthcare LANs have kept the same equipment, cabling and architecture for decades while bandwidth and availability demands rise with life-saving services and the Internet of Things. Optical LAN offers maximum reliability for clinicians, a more defensible architecture for patient electronic records, and fast connectivity for patients, families and staff.",
     ["No electromagnetic interference on fiber", "Reduces or eliminates HEPA tenting during cabling work", "Military-grade security that supports HIPAA compliance", "Removes thousands of pounds of cabling plastics", "High-performance, high-availability access for patients and staff"],
     [["Is Optical LAN used in hospitals?", "Tellabs publishes healthcare content on modernizing hospitals and on Optical LAN in healthcare ICT. Ask for the references that match your facility."], ["What about senior living?", "Tellabs covers senior living in its blog and in the Erickson Living Communities case study."]]],
    ["hospitality", "Hospitality", IMG_CAMPUS,
     "Guest connectivity across hotels and resorts, with lower capital cost on day one and lower cost to run.",
     "A guest's stay is shaped by the performance of their connection, and social media makes the result public. Optical LAN is a fiber-based hotel network that is faster, more efficient and more scalable than copper, reaches every corner of a sprawling property, and frees telecom rooms for larger rooms or suites.",
     ["Better guest experience through reliability and speed", "Reach across a sprawling resort property", "Fiber cabling increases property value", "Telecom rooms can be re-purposed as rooms or suites", "Lower capital cost on day one and lower operating cost each year"],
     [["Is there a hotel example?", "Yes. The Middletown Hotel Management mini case study reports the highest guest satisfaction rating after moving to Optical LAN."], ["Does it support cruise ships?", "Tellabs publishes an article on passive optical LANs on cruise ships and exhibits at Seatrade Cruise Global."]]],
    ["transportation", "Transportation", IMG_BUILD,
     "Networks for airports, seaports, rail stations and freight hubs that need capacity and tight security.",
     "Transportation hubs face budget limits and ageing networks that lack speed, connectivity and capacity, along with the convergence of IT and operational technology. Optical LAN has shown it meets the security, reliability and scalability requirements of airports, seaports and train stations, and it can generate revenue for hubs that serve retail outlets.",
     ["Better network performance for passengers, retail and staff", "Graceful migration to 10 gigabit speeds and beyond", "Fewer points of network vulnerability", "Greater connectivity density in a smaller footprint", "Lower operating cost with fewer moving parts"],
     [["Which airports use it?", "Tellabs publishes LaGuardia Airport and Orlando airport projects on its site. Ask Tellabs which references can be shared with you."], ["Does it cover more than airports?", "Yes. The page covers airports, seaports, rail stations and motor freight centers."]]],
    ["manufacturing", "Manufacturing", IMG_PLANT,
     "Machine and human connectivity on one passive fiber network, with fewer parts to fail.",
     "Manufacturers, distribution sites and smart warehouses are automating with the Industrial Internet of Things, machine-to-machine learning and smart devices. Optical LAN is a passive point-to-multipoint fiber infrastructure for in-building and property-wide connectivity, with centralized management, more uptime and room to scale, at a lower initial deployment cost.",
     ["Lower ongoing operational and support cost", "Graceful migration to 10 gigabit speeds and beyond", "Removes hundreds of known LAN security gaps", "No IT staff on scissor lifts at high ceilings", "No disruptive future network refreshes"],
     [["Is there a manufacturing example?", "Yes. The SK Food Group mini case study covers an Industry 4.0 rollout on Optical LAN."], ["Does it suit a large plant?", "Optical LAN is built for property-wide connectivity. Tellabs can size the design to your site."]]],
    ["service-providers", "Service Providers", IMG_RACK,
     "The first choice to collapse, converge and connect an access network, from legacy copper to PON and Ethernet.",
     "Service providers manage a large embedded base of copper that carries analog services, and want fiber-based IP services without a revenue case that pays for the upgrade. Tellabs Broadband converges legacy analog services onto systems ready for DSL, PON and Ethernet, using existing approved equipment and infrastructure. The Tellabs 1000 MSAP is described as the industry's only fiber-fed, IP-enabled digital loop carrier.",
     ["Optical and copper-based transport for every application", "PON and xDSL high-speed services for residential and business", "Support for legacy telecom services", "Class-5 switch replacement", "911 redundancy and diversity"],
     [["Which platform is this built on?", "The Tellabs 1000 MSAP, a multi-service access platform that supports PON (G-PON or 10G XGS-PON), Ethernet, DSL, TDM and ATM."], ["Can it support broadband stimulus projects?", "Tellabs states that the 1000 MSAP and the FlexSym OLT-mini minimize cost of entry by investing only when needed."]]],
]

SERVICES = [  # slug, nav label, short, one-line, image, eyebrow, heading, subhead, benefits, included, faq
    ["optical-lan", "Passive Optical LAN", "Optical LAN",
     "A building and campus LAN built on passive fiber, for enterprise, education, government, healthcare, hospitality, transportation and manufacturing.",
     IMG_HERO, "Enterprise",
     "A simpler, more secure network that <em>costs less to run</em>.",
     PROMISE,
     [["Simpler", "A flatter design with one management screen and global profiles, so IT repeats the same steps without the same errors."],
      ["More secure", "Tellabs states Optical LAN shrinks the network attack surface by 320:1 and needs 6:1 fewer IT staff touches, which suits zero trust."],
      ["Costs less", "Tellabs states 20-50% lower cost, up to 90% less material and space, and 30-40% lower energy use."],
      ["Built to last", "Single-mode fiber has no known bandwidth limit, and the path runs from gigabit to 100 gigabits without a rip and replace."]],
     ["Network Manager: one console for global profiles", "Optical Line Terminal sized for 200 to over 7,000 Ethernet connections", "Single-mode fiber and passive optical splitters from 1:2 to 1:64", "Optical Network Terminals with Power over Ethernet", "Standards-based G-PON and 10G XGS-PON", "FlexAir wireless and software-defined networking"],
     [["What is Passive Optical LAN?", "A fiber-based IT infrastructure that combines standards-based passive optical networking (G-PON and 10G XGS-PON) with advanced Ethernet. It serves buildings and campuses."],
      ["Do my devices change?", "No. Voice, video, data and Wi-Fi keep working, and the end devices stay the same."],
      ["How far can it reach?", "Tellabs states a reach of 12 to 18 miles, which allows one private LAN across a district or campus."],
      ["Where do I start?", "The Optical LAN tutorial explains the five parts. Then contact Tellabs, or a Tellabs Advantage Partner near you, for a design."]]],
    ["broadband-modernization", "Broadband Network Modernization", "Broadband modernization",
     "Tellabs 1000 MSAP converges copper and fiber services so a service provider can sustain, expand and evolve its access network.",
     IMG_RACK, "Service Providers",
     "Converge, collapse and connect <em>the access network you have</em>.",
     "Tellabs Broadband helps service providers modernize in a cost-effective manner that leverages existing approved equipment and infrastructure, with options for fiber and Ethernet upgrades.",
     [["911 redundancy", "Redundant, diverse connectivity to Public Safety Answering Points."],
      ["Class-5 switch replacement", "Supports 100 percent of Class-5 services over TDM or IP/Ethernet transport."],
      ["DSL and Ethernet", "ADSL2+ and VDSL2 service, and Ethernet transport that keeps copper-based revenue."],
      ["Transport and stimulus", "Optical options for backhaul and switch collapse, and a low cost of entry for stimulus projects."]],
     ["911 redundancy", "Broadband stimulus with the 1000 MSAP and FlexSym OLT-mini", "Broadband DSL and Ethernet", "Class-5 switch replacement", "Narrowband services", "Broadband transport", "1/0 DCS and D4 channel bank replacement"],
     [["What is the Tellabs 1000 MSAP?", "Also known as T1000, DMAX, AFC and UMC: a Broadband Digital Loop Carrier that converges legacy copper and modern fiber connectivity."],
      ["Does it support legacy services?", "Yes. It carries a range of analog special services and supports TDM and ATM next to PON, Ethernet and DSL."],
      ["Can I upgrade in stages?", "Yes. Tellabs describes investing only when needed to optimize project returns."]]],
    ["services-support-training", "Services, Support and Training", "services",
     "Technical support, professional services, training and digital credentials to plan, build and operate a Tellabs network.",
     IMG_TRAIN, "Services, Support and Training",
     "The people who plan, build and operate it, <em>trained by Tellabs</em>.",
     "The Tellabs services suite is a collection of technical support, professional services and training that is customized to your network and to the staff who run it.",
     [["Technical support", "Support agreements add to the standard hardware warranty, with remote and on-site options, updates and audits."],
      ["Professional services", "From small projects to migrations to full turnkey services: plan, design, install and operate."],
      ["Training", "Remote, on-site, classroom and free self-paced video training for planning, deployment and operations."],
      ["Digital credentials", "A digital version of your Tellabs training credential for email signatures, resumes and social profiles."]],
     ["Technical Assistance Center, staffed 24x7 on option 1 of the main number", "Standard warranty, then support agreement packages", "Planning and design, deployment and operations courses", "Tellabs Training Center, remote and on-site training", "Free self-paced Tellabs training videos", "Software license key requests"],
     [["How do I reach support?", "Call the main number and choose option 1 for Technical Support, staffed 24x7. Option 4 reaches Tellabs Nexus help."],
      ["Which courses are there?", "The catalogue includes fiber optic technician, network planning and design, and operations courses for Optical LAN."],
      ["Where are the software license keys?", "The services page has a quick start guide and a short form."]]],
]

CASES = [  # eyebrow, title, line, live path   (all published on tellabs.com)
    ["K-12 education", "Santa Fe Public Schools", "Zero telecom rooms against seven per typical school, 8 fiber drops where copper needed 120 cables, and a 10-year TCO of $433K against $2.1M.", "/top-case-study-series-optical-lan-cost-savings-applied-to-k-12-education-needs-for-santa-fe-public-schools/"],
    ["K-12 education", "White Plains City Schools", "Network simplification through automation, after a series of networking issues.", "/mini-case-study-series-olan-delivers-savings-and-efficiencies-with-network-simplification-for-k12-school/"],
    ["Hospitality", "Middletown Hotel Management", "One infrastructure in place of three, and the highest guest satisfaction rating.", "/mini-case-study-series-olan-fiber-optic-connectivity-rewards-hotelier-with-highest-guest-satisfaction/"],
    ["Manufacturing", "SK Food Group", "Optical LAN as the base for Industry 4.0 automation.", "/mini-case-study-series-sk-food-group-expands-industry-4-0-with-olan/"],
    ["Enterprise", "McGough headquarters", "An old trucking terminal turned into an open, healthy and smart office.", "/top-case-study-olan-enables-mcgough-open-healthy-and-smart-hq/"],
    ["Senior living", "Erickson Living Communities", "Wired and wireless access for staff and residents.", "/top-case-study-series-always-connected-with-olan-at-erickson-living-communities/"],
    ["Enterprise", "Kraus-Anderson headquarters", "A 100,000 square foot headquarters built as a collaborative campus.", "/mini-case-study-series-olan-helps-k-a-overcome-network-challenges-in-modern-workplace/"],
    ["Gaming", "Indian Head Casino", "Replacing multiple racks of switch-based copper in the main data center.", "/mini-case-study-series-olan-positions-indian-head-casino-at-forefront-of-technology/"],
]
PAPERS = [
    ["White paper", "Passive Optical LAN: The What, How and Why", "What Optical LAN is, how it works and why it benefits you, your company and the industry.", "/passive-optical-lan-the-what-how-and-why/"],
    ["White paper", "Tangible contributions to healthy, green and smart buildings", "How Optical LAN helps IT staff contribute to healthy, green and smart building goals.", "/contributions-passive-optical-lan-delivers-to-healthy-green-and-smart-building/"],
    ["Blog", "What Is Passive Optical LAN?", "A plain explanation of the technology, the standards behind it and where it fits.", "/what-is-passive-optical-lan/"],
    ["Blog", "What does OLT and ONT mean?", "The terms OLT and ONT, and how they are used in enterprise Optical LAN.", "/what-does-olt-and-ont-mean-in-this-alphabet-soup-called-optical-lan/"],
    ["Blog", "PON, POL, G-PON and OLAN: the key differences", "What each of the terms means and when to use it.", "/what-is-the-key-difference-between-pon-pol-gpon-and-olan/"],
    ["Blog", "What is the difference between fiber and copper networking?", "A short comparison for IT leaders weighing a network refresh.", "/"],
]
PAPERS[5][3] = "/category/blog/"

TIMELINE = [
    ["2003", "Broadband PON for Verizon FiOS", "Tellabs starts residential broadband PON as Verizon's primary PON vendor for FiOS."],
    ["2006", "IP voice and video at scale", "Millions of IP voice and IP video connections run on Tellabs broadband for homes and businesses."],
    ["2008", "Optical LAN launched", "The first federal installation is at Sandia Laboratories."],
    ["2010", "DoD certification", "US Department of Defense JITC certification, and the first of many DoD deployments."],
    ["2012", "Enterprise and hotel customers", "Millions of PON ONTs turned up, and the first commercial enterprise and hotel customers."],
    ["2016", "More industries", "Optical LAN grows in education, healthcare, retail, stadium, transportation and manufacturing."],
    ["2022", "Millions of OLAN ports", "Connecting IoT, wireless, surveillance and smart building applications."],
]

FLOW_STEPS = [  # label, when, summary, title, body, receive
    ["Network Manager", "One console", "The central intelligence of the network.", "Network Manager",
     "The PON Manager is the centralized management of the passive optical network and the powered devices attached to it. It gives one console and one screen for control, and uses global profiles to apply consistent, repeatable IT policies.", ["Global profiles for repeatable policy", "One screen for configuration and monitoring"]],
    ["Optical Line Terminal", "Main data center", "Aggregates and distributes connectivity.", "Optical Line Terminal (OLT)",
     "The OLT sits in the building's main data center and connects to the WAN and internal servers through the core router. One OLT can be sized from 200 to over 7,000 Ethernet connections from one location.", ["200 to over 7,000 Ethernet connections per OLT", "Connects to the core router and the WAN"]],
    ["Single-mode fiber", "Risers and pathways", "The cable that links every part.", "Single-mode fiber",
     "Single-mode fiber runs through the building's risers and pathways and connects the OLT, the splitters and the ONTs. There are options for multimode fiber, and for closet-based ONTs that use the last 300 feet of copper.", ["No known bandwidth capacity limit", "Options for multimode fiber and composite cable"]],
    ["Passive splitters", "Closets, walls, ceilings", "Unpowered point-to-multipoint links.", "Passive optical splitters",
     "Splitters give point-to-multipoint connectivity between the OLT and the ONTs, with ratios from 1:2 to 1:64 and 1:32 the most common. They are unmanaged and unpowered, and offer 2:X redundancy options.", ["Split ratios from 1:2 to 1:64", "Mounting in closets, wall or ceiling enclosures"]],
    ["Optical Network Terminal", "At the desk or the ceiling", "Turns light into Ethernet.", "Optical Network Terminal (ONT)",
     "ONTs convert optical to electrical and provide Ethernet for voice, video, data and Wi-Fi. They support Power over Ethernet for phones, cameras and wireless access points, and can be powered locally or from a remote DC source.", ["Power over Ethernet", "Local or remote DC power"]],
]

LEADFORM = {"type": "leadform", "alt": True, "id": "start", "heading": "Talk to a Tellabs expert", "body": "Tell us about your building, campus or network and what you want it to do. A person at Tellabs replies.", "submit": "Send to Tellabs", "note": "A person replies, not an autoresponder."}


def _flow(fid, eyebrow, heading, intro, steps, receive_label="What it does"):
    return {"type": "flow", "id": fid, "alt": True, "eyebrow": eyebrow, "heading": heading, "intro": intro, "receive_label": receive_label,
            "steps": [{"label": a, "when": b, "summary": c, "title": d, "body": e, "receive": f} for a, b, c, d, e, f in steps]}


def service_page(slug, navlabel, short, one, image, eyebrow, heading, subhead, benefits, included, faq):
    secs = [
        {"type": "hero", "layout": "split", "eyebrow": eyebrow, "heading": heading, "subhead": subhead,
         "primary": {"label": "Talk to Tellabs", "href": "contact.html"}, "secondary": {"label": "All services", "href": "services.html"},
         "image": image, "image_alt": navlabel, "image_w": 1200, "image_h": 675 if image == IMG_HERO else 800},
        {"type": "cards", "alt": True, "eyebrow": "What changes", "heading": f"What changes with Tellabs {short}", "items": benefits},
        {"type": "detail", "eyebrow": "What is included", "heading": "What you get", "body": brief(one, 200), "bullets": included, "image": image, "flip": True,
         "image_alt": navlabel + (" (generated)" if image != IMG_HERO else "")},
    ]
    if slug == "optical-lan":
        secs.insert(2, _flow("flow", "How it works", "Five parts, one network", "Click a part. Every Optical LAN is made of these five.", FLOW_STEPS))
        secs.append({"type": "testimonials", "alt": True, "heading": "What customers say", "items": [t[:3] for t in TESTIMONIALS]})
    secs.append({"type": "faq", "heading": f"Questions about {navlabel.lower()}", "items": faq})
    secs.append(LEADFORM)
    return {"file": f"services/{slug}.html", "title": f"{navlabel} | {CLIENT}", "description": fit(f"{one} {subhead}", pad="Talk to Tellabs about your network."),
            "crumbs": [["Home", "index.html"], ["Solutions", "services.html"], [navlabel, f"services/{slug}.html"]], "sections": secs}


def industry_page(slug, name, image, one, body, bullets, faq):
    secs = [
        {"type": "hero", "layout": "centered", "eyebrow": f"Industries: {name}", "heading": one, "subhead": "Talk to Tellabs about your facility, or start with the Optical LAN tutorial.",
         "primary": {"label": "Talk to Tellabs", "href": "contact.html"}, "secondary": {"label": "Optical LAN tutorial", "href": "optical-lan-tutorial.html"},
         "image": image, "image_alt": f"{name}, generated stand-in image" if image != IMG_BUILD else f"{name}, generated stand-in image", "image_w": 1200, "image_h": 800},
        {"type": "detail", "eyebrow": "Why it fits", "heading": f"A better network for {name.lower()}", "body": body, "bullets": bullets},
    ]
    secs.append({"type": "cards", "alt": True, "eyebrow": "How to start", "heading": f"Three ways to start with {name.lower()}", "items": [
        ["Read the tutorial", "The Optical LAN tutorial explains the five parts of a system, the standards behind it and why fiber."],
        ["See a case study", "The resources page lists published customer stories, by industry, in the customers' own words."],
        ["Talk to Tellabs", "Describe your facility and your goals. A person at Tellabs replies, or a Tellabs Advantage Partner near you."]]})
    if slug == "education":
        secs.append({"type": "testimonials", "alt": True, "heading": "What a school district says", "items": [t[:3] for t in TESTIMONIALS]})
    secs.append({"type": "faq", "heading": f"Questions from {name.lower()}", "items": faq})
    secs.append(LEADFORM)
    t = f"{name} Networks | {CLIENT}"
    return {"file": f"industries/{slug}.html", "title": t, "crumbs": [["Home", "index.html"], ["Industries", "industries.html"], [name, f"industries/{slug}.html"]],
            "description": fit(f"{one} {brief(body, 120)}", pad="Talk to Tellabs about your facility."), "sections": secs}


def _res(items):
    return [[e, t, d, "Read on tellabs.com", LIVE + p] for e, t, d, p in items]


def build():
    brand = {
        "accent": "#1B3D6D", "ink_secondary": "#0F2748", "chrome": "light", "chrome_bg": "#FFFFFF",
        "logo": "assets/logo.svg", "logo_alt": "Tellabs", "logo_w": 300, "logo_h": 78,
        "logo_note": "SVG from tellabs.com, navy on a light ground. Orange (#F89B2C) fails contrast against white text, so buttons are navy and orange is not used for text.",
        "phone": PHONE, "phone_href": PHONE_HREF, "email": EMAIL,
        "utility": [{"label": "Nexus", "href": NEXUS}, {"label": "Documentation", "href": DOCS}, {"label": "Forums", "href": FORUMS}, {"label": "Technical support", "href": "services.html#support"}],
        "cta": {"label": "Talk to Tellabs", "href": "contact.html"},
        "sticky": {"primary": "Talk to Tellabs", "primary_href": "contact.html", "secondary": "Call Tellabs", "secondary_href": PHONE_HREF},
        "launcher": {"label": "Already a customer?", "eyebrow": "The fast lane", "title": "What do you need today?",
                     "links": [["Technical support", "services.html#support"], ["Nexus", NEXUS], ["Documentation", DOCS], ["Forums", FORUMS], ["Training", "services.html#training"]],
                     "note": "Choose option 1 on the main number for technical support, staffed 24x7.", "phone": PHONE, "phone_href": PHONE_HREF},
        "social": {"linkedin": "https://www.linkedin.com/company/tellabs", "facebook": "https://www.facebook.com/TellabsOfficial", "x": "https://twitter.com/Tellabs",
                   "youtube": "https://www.youtube.com/channel/UCY2hL91348SM7aF7UgDxleA"},
        "tagline": "A better way to build and operate networks.",
        "footer_columns": [
            {"title": "Solutions", "links": [[s[1], f"services/{s[0]}.html"] for s in SERVICES] + [["Optical LAN tutorial", "optical-lan-tutorial.html"]]},
            {"title": "Industries", "links": [[i[1], f"industries/{i[0]}.html"] for i in INDUSTRIES[:6]] + [["All industries", "industries.html"]]},
            {"title": "Customers", "links": [["Nexus", NEXUS], ["Documentation", DOCS], ["Forums", FORUMS], ["Technical support", "services.html#support"], ["Training", "services.html#training"]]},
            {"title": "Company", "links": [["About Tellabs", "about.html"], ["Partners", "partners.html"], ["Resources", "resources.html"], ["Careers", LIVE + "/about/careers/"], ["Contact", "contact.html"]]},
        ],
        "legal": [["Privacy", LIVE + "/about/privacy/"], ["Legal", LIVE + "/about/legal/"]],
    }
    schema = {"org_name": CLIENT, "org_url": LIVE, "org_logo": LIVE + "/wp-content/uploads/2019/10/Tellabs_FullColor_Without_Tag_for_web_nobounds.svg",
              "org_description": "Tellabs builds Passive Optical LAN for enterprise, education, government, healthcare, hospitality, transportation and manufacturing, and broadband access networks for service providers.",
              "sameAs": list(brand["social"].values()), "telephone": "+1-800-690-2324", "legal_name": LEGAL, "slogan": "A better way to build and operate networks.",
              "short_name": "Tellabs", "title_city": "USA", "cities": ["Carrollton", "Dallas", "Texas", "TX", "USA"], "area_served": [{"@type": "Country", "name": "United States"}],
              "meta_tail": "Tellabs Optical LAN and broadband solutions.",
              "local": [{"slug": "carrollton", "name": "Tellabs headquarters", "street": HQ[0], "city": "Carrollton", "region": "TX", "postal": "75007", "telephone": "+1-972-588-7000"}],
              "people": [{"slug": "rich-schroder", "name": "Rich Schroder", "title": "President and CEO", "sameAs": []}]}
    nav = [
        {"label": "Solutions", "href": "services.html", "children": [[s[1], f"services/{s[0]}.html"] for s in SERVICES] + [["Optical LAN tutorial", "optical-lan-tutorial.html"]]},
        {"label": "Industries", "href": "industries.html", "children": [[i[1], f"industries/{i[0]}.html"] for i in INDUSTRIES]},
        {"label": "Services", "href": "services.html#support", "children": [["Technical support", "services.html#support"], ["Training", "services.html#training"], ["Professional services", "services.html#professional"], ["Digital credentials", "services.html#credentials"]]},
        {"label": "Resources", "href": "resources.html", "children": [["Case studies", "resources.html#cases"], ["White papers and blog", "resources.html#papers"], ["Optical LAN tutorial", "optical-lan-tutorial.html"]]},
        {"label": "Partners", "href": "partners.html"},
        {"label": "About", "href": "about.html", "children": [["About Tellabs", "about.html"], ["Leadership", "about.html#leadership"], ["Contact", "contact.html"]]},
    ]
    wheel_items = [[i[1], brief(i[3], 120), f"industries/{i[0]}.html", i[1]] for i in INDUSTRIES]
    pages = []
    home_secs = [
        {"type": "hero", "id": "hero-light", "layout": "split", "eyebrow": "Passive Optical LAN and broadband",
         "stats": [["2008", "Optical LAN launched"], ["20-50%", "Lower cost, as stated by Tellabs"], ["24x7", "Staffed technical support"], ["8", "Industries served"]],
         "ribbon": ["Optical LAN since 2008", "Staffed 24x7 technical support", "Eight industries"],
         "variants": {"journal": {"stats": None}},
         "heading": "A simpler, more secure network that <em>costs less to run</em>.", "subhead": PROMISE,
         "primary": {"label": "Talk to Tellabs", "href": "contact.html"}, "secondary": {"label": "Optical LAN tutorial", "href": "optical-lan-tutorial.html"},
         "note": "", "image": IMG_HERO, "image_alt": "Two engineers testing a network in a data center", "image_w": 1200, "image_h": 675},
        {"type": "partners", "id": "partners", "caption": "Tellabs Advantage Partners", "items": PARTNERS},
        {"type": "services", "id": "services", "heading": "Three ways Tellabs helps", "intro": "Optical LAN for the building, broadband for the operator, and the services to run both.",
         "items": [[s[1], s[3], f"services/{s[0]}.html"] for s in SERVICES]},
        {"type": "seal", "id": "seal", "eyebrow": "What Tellabs states about Optical LAN", "heading": "Six claims, from the Tellabs site", "intro": "Each line is published on tellabs.com. Ask Tellabs for the method behind a figure.",
         "items": [["320:1", "Smaller attack surface", "Tellabs states Optical LAN shrinks the network attack surface by 320:1."],
                   ["6:1", "Fewer IT staff touches", "Supports a zero trust architecture."],
                   ["20-50%", "Lower costs", "Stated against a traditional enterprise LAN."],
                   ["90%", "Less material and space", "Up to 90 percent reduction."],
                   ["30-40%", "Lower energy use", "Stated for Passive Optical LAN."],
                   ["12-18 mi", "Reach", "A private LAN across a district with one central data center."]],
         "source": "Sources: tellabs.com/solutions/pon/olan/ and tellabs.com/solutions/industries/education/."},
        {"type": "wheel", "id": "wheel", "eyebrow": "Eight industries", "heading": "Proven in every industry Tellabs serves", "intro": "Hover a segment to read it. Each industry has its own page.", "items": wheel_items, "panel_eyebrow": "Hover a segment", "link_label": "See the industry", "hub": "Tellabs", "hub_sub": "eight industries"},
        _flow("flow", "How it works", "Five parts, one network", "Click a part. Every Optical LAN is made of these five.", FLOW_STEPS),
        {"type": "beforeafter", "id": "ba", "eyebrow": "Before and after", "heading": "One school district, measured",
         "before": {"eyebrow": "A typical Santa Fe school", "title": "Copper-based LAN", "body": "Santa Fe Public Schools had the legacy design in each of 39 schools.", "items": ["Seven telecom rooms per typical school", "120 cables where Optical LAN needed 8 fiber drops", "10-year TCO of $2.1M"]},
         "after": {"eyebrow": "With Tellabs Optical LAN", "title": "One fiber network", "body": "Digitally controlled HVAC, LED lighting, sensors and more converge over one network.", "items": ["Zero telecom rooms needed", "8 fiber drops", "10-year TCO of $433K, and $60,000 lower CapEx per school"]}},
        {"type": "proof", "id": "proof", "alt": True, "eyebrow": "Measured in a case study", "value": "80%", "text": "Lower 10-year total cost of ownership for Santa Fe Public Schools: $433K against $2.1M for a legacy LAN.", "source": "Source: Tellabs case study, Santa Fe Public Schools, October 2021."},
        {"type": "timeline", "id": "story", "eyebrow": "Since 2003", "heading": "Two decades of fiber access networking", "intro": "Dates from the Tellabs timeline on its About page.", "items": TIMELINE},
        {"type": "testimonials", "id": "voices", "alt": True, "layout": "feature", "eyebrow": "What customers say", "heading": "From the Santa Fe Public Schools case study", "items": [t[:3] for t in TESTIMONIALS]},
        {"type": "faq", "id": "faq", "alt": True, "heading": "Questions we get on the first call", "items": [
            ["What is Passive Optical LAN?", "A fiber-based IT infrastructure that combines standards-based passive optical networking with advanced Ethernet, for buildings and campuses."],
            ["Does it change the devices we use?", "No. Existing voice, video, data and Wi-Fi services keep working with no change to the core or the end devices."],
            ["Is it secure?", "Tellabs publishes bidirectional encryption between OLT and ONT, ONTs that store no user or network information, and compliance with STIG, HIPAA and PCI."],
            ["How do I reach support?", "Choose option 1 on the main number for technical support, staffed 24x7."]]},
        {"type": "contact", "id": "contact", "heading": "Talk to Tellabs", "body": "Tell us about your building, campus or network. A person at Tellabs replies.",
         "options": ["Passive Optical LAN", "Broadband network modernization", "Technical support", "Training", "Becoming a partner"], "submit": "Send to Tellabs", "note": "A person replies, not an autoresponder."},
    ]
    pages.append({"file": "index.html", "title": "Tellabs | Passive Optical LAN and Broadband Network Solutions",
                  "compose": {
                      "clean": ["hero-light", "partners", "services", "seal", "flow", "proof", "voices", "faq", "contact"],
                      "journal": ["hero-light", "services", "story", "seal", "flow", "ba", "voices", "faq", "contact"],
                      "showcase": ["hero-light", "partners", "wheel", "services", "flow", "ba", "proof", "seal", "story", "voices", "faq", "contact"]},
                  "description": desc("Tellabs Optical LAN gives your building a simpler, more secure network that costs less to run. Passive optical LAN and broadband for enterprise and service providers.", 158),
                  "sections": home_secs})
    for s in SERVICES:
        pages.append(service_page(*s))
    pages.append({"file": "services.html", "title": "Services, Support and Training | Tellabs",
                  "description": "Technical support staffed 24x7, professional services, Tellabs training courses and digital credentials to plan, build and operate your Tellabs network.",
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "Services", "heading": "Support, services and training for <em>every stage of the network</em>.", "subhead": "The Tellabs services suite is customized to your network and to the people who run it.", "primary": {"label": "Talk to Tellabs", "href": "contact.html"}},
        {"type": "cards", "alt": True, "id": "areas", "eyebrow": "Four areas", "heading": "What the suite covers", "items": [
            ["Technical support", "Ongoing support to keep the network at peak performance."], ["Professional services", "Plan, design, install and operate."],
            ["Training", "Courses for the people who plan, build and run it."], ["Digital credentials", "Show what your team earned in training."]]},
        {"type": "faq", "id": "svc-faq", "heading": "Questions about services", "items": [
            ["Is support included with the equipment?", "A standard hardware repair warranty comes with every Tellabs solution. Support agreements add to it."],
            ["Can I get on-site support?", "Yes. You choose the mix of remote and on-site support, repair and replacement, updates and audits."],
            ["How is training delivered?", "Remotely with hands-on access to equipment, on site, in the Tellabs Training Center, and as free self-paced videos."],
            ["What are digital credentials?", "Digital versions of credentials earned in Tellabs training, for email signatures, resumes and social profiles."]]},
        {"type": "detail", "id": "support", "eyebrow": "Technical support", "heading": "Support agreements added to the hardware warranty", "body": "Support agreements add to the standard hardware repair warranty that comes with every Tellabs solution. You choose the mix of remote and on-site support, repair and replacement, and updates and audits. The Technical Assistance Center is staffed 24x7 on option 1 of the main number.",
         "bullets": ["Standard warranty, 8x5 next business day, and 24x7x365 support options", "On-site support and advanced on-site SLA options", "Software updates, new feature access and network audits", "Software license keys by request"], "image": IMG_RACK, "image_alt": "Network equipment rack, generated stand-in image"},
        {"type": "detail", "id": "professional", "alt": True, "eyebrow": "Professional services", "heading": "From a small project to a turnkey migration", "body": "Tellabs services help you successfully plan, design, install and operate your network, whether the work is a small project, a migration or a full turnkey service.",
         "bullets": ["Planning and design", "Installation and migration", "Operations reviews", "Mentoring for partners"], "image": IMG_BUILD, "image_alt": "An office building cutaway, generated stand-in image", "flip": True},
        {"type": "detail", "id": "training", "eyebrow": "Training", "heading": "Plan, build and operate courses", "body": "Remote training with hands-on access to equipment, on-site training, classroom training at the Tellabs Training Center, and free self-paced videos.",
         "bullets": ["Planning and design: link budgets, ONT mounting, OLT planning", "Deployment: installation, configuration, provisioning and testing", "Operations: adds, moves and changes, maintenance and troubleshooting"], "image": IMG_TRAIN, "image_alt": "A training lab, generated stand-in image"},
        {"type": "detail", "id": "credentials", "alt": True, "eyebrow": "Digital credentials", "heading": "Show the world what you earned", "body": "A digital version of a Tellabs-earned training credential for email signatures, digital resumes and social profiles.", "bullets": ["Earned in Tellabs training", "Shareable on social sites"], "image": IMG_TRAIN, "image_alt": "A training lab, generated stand-in image", "flip": True},
        LEADFORM,
    ]})
    pages.append({"file": "industries.html", "title": "Industries | Tellabs Optical LAN and Broadband",
                  "description": "Tellabs Optical LAN for enterprise, education, government, healthcare, hospitality, transportation and manufacturing, and broadband for service providers.",
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "Industries", "heading": "Eight industries, <em>one fiber network design</em>.", "subhead": "Optical LAN is proven across all industries. Find yours.", "primary": {"label": "Talk to Tellabs", "href": "contact.html"}},
        {"type": "resources", "heading": "Eight industries", "intro": "Each page covers why Optical LAN fits, and what customers ask.", "items": [["Industry", i[1], i[3], f"Networks for {i[1].lower()}", f"industries/{i[0]}.html"] for i in INDUSTRIES]},
        {"type": "faq", "alt": True, "heading": "Questions about industries", "items": [
            ["Does it work outside enterprise?", "Yes. Tellabs states Optical LAN is proven across all industries, and lists eight on its site."],
            ["Which industry is for broadband operators?", "Service Providers, which is built on the Tellabs 1000 MSAP rather than Optical LAN."],
            ["What if my industry is not listed?", "The site also has pages for retail, financial, insurance, senior living and more. Ask Tellabs about yours."],
            ["Can I see a customer from my industry?", "The resources page lists case studies by industry."]]},
        LEADFORM,
    ]})
    for i in INDUSTRIES:
        pages.append(industry_page(*i))
    pages.append({"file": "optical-lan-tutorial.html", "title": "Optical LAN Tutorial | What It Is and How It Works | Tellabs",
                  "description": "A plain tutorial on Passive Optical LAN: what it is, the five parts of a system, why fiber, and answers to common questions, from Tellabs.",
                  "crumbs": [["Home", "index.html"], ["Resources", "resources.html"], ["Optical LAN tutorial", "optical-lan-tutorial.html"]],
                  "schema": [{"@context": "https://schema.org", "@type": "Article", "headline": "Passive Optical LAN tutorial", "description": "What Passive Optical LAN is, the five parts of a system, and why fiber.", "author": {"@type": "Organization", "name": "Tellabs", "url": LIVE}, "publisher": {"@type": "Organization", "name": "Tellabs", "url": LIVE}}],
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "Tutorial", "heading": "Passive Optical LAN, <em>explained simply</em>.", "subhead": "With Passive Optical LAN gaining traction in all market verticals, now is the time to learn what it is, how it works and why it is better.", "primary": {"label": "Talk to Tellabs", "href": "contact.html"}},
        {"type": "cards", "alt": True, "eyebrow": "Quick facts", "heading": "Why fiber", "items": [
            ["Investment protection", "Fiber has a longer useful life."], ["Sustainability", "Fiber infrastructure is significantly more environmentally sustainable."],
            ["Technology independent", "Fiber in buildings and outside plant does not depend on the technology on top."], ["Graceful migration", "From gigabit to 100 gigabits."],
            ["Secure and reliable", "Greater reach than copper, with better security and reliability."], ["No known limit", "Single-mode fiber has no known bandwidth capacity limit."]]},
        _flow("flow", "How it works", "The five parts of an Optical LAN", "Click a part.", FLOW_STEPS),
        {"type": "faq", "heading": "Questions", "items": [
            ["Is fiber optic cable fragile, difficult to install and harder to test?", "No. Tellabs says single-mode fiber is smaller, lighter and stronger, with a better bend radius, higher capacity, longer reach and less interference."],
            ["Which standards are used?", "2.5G asymmetrical G-PON and 10G symmetrical XGS-PON, with standards-based Ethernet."],
            ["Where is the glossary?", "Tellabs publishes a glossary of Optical LAN terms and acronyms on its tutorial page."]]},
        LEADFORM,
    ]})
    pages.append({"file": "resources.html", "title": "Case Studies, White Papers and Blog | Tellabs Resources",
                  "description": "Tellabs case studies from schools, hotels, headquarters and plants, plus white papers and blog posts on Passive Optical LAN, on tellabs.com.",
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "Resources", "heading": "Evidence, <em>in the customers' words</em>.", "subhead": "Case studies, white papers and blog posts from tellabs.com, one click from the header.", "primary": {"label": "Optical LAN tutorial", "href": "optical-lan-tutorial.html"}},
        {"type": "resources", "id": "cases", "heading": "Case studies", "intro": "Eight published customer stories.", "items": _res(CASES)},
        {"type": "resources", "id": "papers", "alt": True, "heading": "White papers and blog", "intro": "Start with the what, how and why.", "items": _res(PAPERS)},
        {"type": "faq", "heading": "Using these resources", "items": [
            ["Where do I start if Optical LAN is new?", "Start with the Optical LAN tutorial, then the white paper on what, how and why."],
            ["Are the case studies by industry?", "Yes. They cover K-12 education, hospitality, manufacturing, enterprise headquarters, senior living and gaming."],
            ["Where is the full library?", "Every white paper, case study, video, event and news release is on tellabs.com."],
            ["Can I talk to someone about a case study?", "Yes. Use the form below and name the customer story you read."]]},
        LEADFORM,
    ]})
    pages.append({"file": "partners.html", "title": "Advantage Partner Program | Tellabs Partners",
                  "description": "The Tellabs Advantage Partner Program matches customers with resellers and integrators, and gives partners training, a demo center and support. Find or become one.",
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "Partners", "heading": "Find a partner, or <em>become one</em>.", "subhead": "The Advantage Partner Program matches our customers with the best resellers and integrators, and offers them network solutions that differentiate their business.", "primary": {"label": "Become a partner", "href": LIVE + "/partners/become/"}, "secondary": {"label": "Find a partner", "href": LIVE + "/partners/find/"}},
        {"type": "cards", "alt": True, "eyebrow": "Our pledge of support", "heading": "What partners receive", "items": [
            ["Sales support", "Help with customer interactions, proposals, configurations and on-site trials."], ["Marketing", "Lead generation, events, webinars, co-branded collateral and news releases."],
            ["Education", "Technology, product and competitive training, plus the annual Tellabs Partner Conference."], ["Dallas Demonstration Center", "Customer meetings and demos, and discounted lab equipment."]]},
        {"type": "partners", "id": "partners", "caption": "A selection of Tellabs Advantage Partners", "items": PARTNERS},
        {"type": "faq", "heading": "Partner questions", "items": [
            ["What does the program do?", "It matches customers with the best resellers and integrators, and gives partners network solutions that differentiate their business."],
            ["Is the program open to everyone?", "Tellabs describes it as highly selective, which limits channel conflict."],
            ["What support do partners get?", "Help with customers and proposals, marketing, training and certification, the Dallas Demonstration Center, an online resource center and supplemental professional services."],
            ["How do I join?", "Use Become a partner on this page, which opens the Tellabs partner application on tellabs.com."]]},
        {"type": "values", "alt": True, "eyebrow": "Industry associations", "heading": "Tellabs is an active member of seven", "items": ASSOC_FULL[:6] + [ASSOC_FULL[6]] + [["More on the site", "The About page lists each membership."]][:0]},
        LEADFORM,
    ]})
    pages.append({"file": "about.html", "title": "About Tellabs | Fiber Access Networking Since 2003",
                  "description": "Tellabs is an innovation leader in fiber-based technologies: broadband PON for service providers and Passive Optical LAN for enterprise. Leadership, history, and Carrollton, Texas.",
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "About Tellabs", "heading": "We innovate better ways to <em>build and operate networks</em>.", "subhead": "We deliver simple, secure, sustainable, stable and scalable network solutions that gain our partners and customers tangible benefits.", "primary": {"label": "Contact Tellabs", "href": "contact.html"}},
        {"type": "timeline", "id": "story", "eyebrow": "Since 2003", "heading": "The Tellabs story", "intro": "From the Tellabs timeline on its About page.", "items": TIMELINE},
        {"type": "leadership", "id": "leadership", "heading": "Leadership", "intro": "The Tellabs leadership team, from tellabs.com.", "people": LEADERS},
        {"type": "values", "alt": True, "eyebrow": "Vision and mission", "heading": "What Tellabs is working toward", "items": [
            ["Vision", "To focus our passion, expertise and social responsibility to innovate better ways to build and operate networks."],
            ["Mission", "Deliver simple, secure, sustainable, stable and scalable network solutions that gain our partners and customers tangible benefits."],
            ["How", "Work as one team, provide unparalleled customer service and build lasting customer relationships."]]},
        {"type": "locations", "heading": "Headquarters", "intro": "Carrollton, Texas.", "items": [["Carrollton", HQ[0], HQ[1], PHONE, PHONE_HREF]]},
        {"type": "faq", "heading": "Questions about Tellabs", "items": [
            ["Where is Tellabs based?", "Tellabs lists its location as 4240 International Pkwy, Suite 105, Carrollton, Texas 75007."],
            ["What does Tellabs make?", "Passive Optical LAN for enterprise, education, government, healthcare, hospitality, transportation and manufacturing, and broadband access platforms for service providers."],
            ["Who leads the company?", "Rich Schroder is President and CEO. Susan Merrill is Chief Financial Officer, Karen Leos leads Global Sales and Professional Services, and Tom Dobozy leads Engineering."],
            ["Which industry groups does Tellabs belong to?", "APOLAN, TIA, BICSI, AFCEA, the Broadband Forum, HTNG and the UNH InterOperability Laboratory."],
            ["How do I contact Tellabs?", "Call the main number, email ask@tellabs.com, or use the form on the contact page."]]},
        {"type": "cta", "heading": "Work with Tellabs", "subhead": "Visit the Tellabs careers pages to see current openings.", "primary": {"label": "See careers", "href": LIVE + "/about/careers/"}},
    ]})
    pages.append({"file": "contact.html", "title": "Contact Tellabs | Sales, Support, Training and Orders",
                  "description": "Reach Tellabs by phone, email or form: sales, technical support staffed 24x7, order management, training, Nexus help and RMA. Carrollton, Texas.",
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "Contact", "heading": "Talk to Tellabs, <em>or call</em>.", "subhead": "For pricing, availability, order status and sales questions, call the main number and choose option 5. Option 1 is technical support, staffed 24x7."},
        {"type": "contact", "id": "form", "heading": "Send a message", "body": "Tell us about your building, campus or network. A person at Tellabs replies.",
         "options": ["Passive Optical LAN", "Broadband network modernization", "Technical support", "Training", "Becoming a partner"], "submit": "Send to Tellabs", "note": "A person replies, not an autoresponder."},
        {"type": "cards", "alt": True, "eyebrow": "On the main number", "heading": "Six options", "items": [
            ["1. Technical support", "Staffed 24x7."], ["2. Order management", "Order status, invoicing, pricing and availability."], ["3. Training", "Class inquiries, scheduling and availability."],
            ["4. Tellabs Nexus", "Help with your Nexus account."], ["5. Sales", "Sales questions."], ["6. RMA", "Advanced replacements, repair and return, and warranty status."]]},
        {"type": "faq", "alt": True, "heading": "Before you call", "items": [
            ["Who do I call about an order?", "Choose option 2 on the main number for order status, invoicing, pricing and availability."],
            ["How do I get technical support?", "Choose option 1. Technical Support is staffed 24x7."],
            ["How do I sign up for training?", "Choose option 3 for class inquiries, scheduling and availability, or use the training page."],
            ["How do I send equipment back?", "Choose option 6 for advanced replacements, repair and return orders, and warranty status."],
            ["Is there a number outside North America?", "Yes. Tellabs lists numbers for Singapore, France and the United Kingdom, and an international line, on tellabs.com."]]},
        {"type": "locations", "heading": "Offices", "intro": "North America toll free " + PHONE + ". International numbers are on tellabs.com.", "items": [["Carrollton", HQ[0], HQ[1], PHONE, PHONE_HREF]]},
    ]})

    pitch = {
        "qbs_contact": {"name": "Shawn", "email": "shawn@thequantumleap.business"},
        "prepared_for": "Tellabs",
        "heard_intro": "Everything here comes from your brief and your current site. Tell us where it is wrong; your words outrank ours.",
        "heard": [
            "The promise a visitor must believe: " + PROMISE,
            "Light ground, with navy #1B3D6D for buttons. Orange #F89B2C fails contrast against white text, so it stays a small signal only.",
            "Eight industries on the live site: Enterprise, Education, Government, Healthcare, Hospitality, Transportation, Manufacturing and Service Providers.",
            "Keep the Optical LAN tutorial, white papers, case studies, technical support, training and the partner program one click from the header.",
            "Preferred set from your interview: Quantum Clean, Quantum Journal and Quantum Showcase, all light.",
            "Keep every URL with a 301 and one canonical host, tellabs.com and not www.",
            "No invented statistics: facts only from tellabs.com."],
        "found": [
            "Search baseline from your brief: 785 organic visits a month, 85 percent on the home page and almost all brand searches.",
            "The Optical LAN explainers rank 2 to 5 for what is passive optical lan and olt meaning, so their URLs are the ones to protect.",
            "823 URLs in the sitemap. The audit scores the live site 43 on average, with no page graded B or better.",
            "No page has a breadcrumb, a city or location signal, a FAQ or a self-referencing canonical on the pages we checked, and no llms.txt.",
            "Product datasheets are 121 of the 823 URLs and carry the site's long tail."],
        "pick_reasons": [], "pick_change": "",
        "alternatives": [],
        "choose_reasons": [["Quantum Clean", "Plain, fast to scan, and built for the IT leader comparing options: the promise, the proof and the five parts of Optical LAN up front."], ["Quantum Journal", "A serif, text-forward site for the buyer who reads the tutorial, white papers and case studies before calling."], ["Quantum Showcase", "Image-led and layered: the eight industries on a wheel, the before and after, and the timeline."]],
        "choice_intro": "All three are the whole site with the same words and the same proof. The difference is temperament. Open each one and tell us which feels like you.",
        "plan": [
            ["Days 1 to 15", "Settle the confirm list, name one canonical host, and write a 301 for every URL that ranks."],
            ["Days 16 to 30", "Finish the copy with your approvals, and obtain customer permission for quotes and logos."],
            ["Days 31 to 45", "Build the chosen direction with the tutorial, resources and partner pages."],
            ["Days 46 to 60", "Titles, descriptions, breadcrumbs and entity markup on the pages that earn traffic today."],
            ["Days 61 to 75", "Check every redirect, form and page on desktop and phone."],
            ["Days 76 to 90", "Go live, then compare visits and rankings against the baseline."]],
        "confirm": [
            "Which main phone number leads: +1 800 690 2324 (toll free, sales, from the contact page) or +1 972 588 7000 (the header of tellabs.com).",
            "Legal name: the footer reads Tellabs Access, LLC. A 1 October 2026 post says Zhone Technologies announced its acquisition of Tellabs Access. Confirm the legal entity and what the site should say about it.",
            "The 60 percent of North American enterprise Optical LAN deployments and 80 percent of US federal agency deployments are from a January 2017 blog post and are not used. Confirm a current figure.",
            "The 320:1, 6:1, 90 percent, 30-40 percent and 20-50 percent figures are Tellabs claims on its own Optical LAN page. Confirm the source and the method before they go live.",
            "Only one customer quote is used (Elias Bernardino, Santa Fe Public Schools, 2021). Confirm permission, and name other quotes and logos we may use.",
            "No logo files for partners or customers were collected. Partner names are shown as text.",
            "Photography: the hero image is from tellabs.com. Other images are generated stand-ins from the library, labelled generated. Supply real photographs of the product and installs.",
            "Product pages (FlexSym OLT1, OLT2, OLT6, OLT-mini, BOLT and the datasheet family) are not rebuilt in this preview. Confirm the scope.",
            "The 121 product datasheets, 59 tag pages and partner pages need a redirect decision.",
            "Case studies, white papers and blog posts link to tellabs.com in this preview. Confirm whether they move onto the new site.",
            "Orange #F89B2C is not used in the three directions. Confirm whether a small orange signal should be added.",
            "Staffed 24x7 technical support is taken from option 1 on the contact page. Confirm it is current.",
            "No team page, careers copy or leadership photos were collected; leaders are listed by name and role.",
            "Quantum Clean and Quantum Showcase are both light sans-serif directions, chosen from your interview. Confirm that is the set you want against the house rule of different typeface classes.",
            "The Semrush and AEO analysis was not available in the brief, so the search package is not included."],
        "footer": "Prepared for Tellabs. Nothing here is live or indexed. Stand-in images are generated and labelled as such.",
    }
    return {"client": CLIENT, "slug": "tellabs", "domain_hint": "tellabs.com", "brand": brand, "schema": schema, "nav": nav, "pages": pages, "pitch": pitch}


if __name__ == "__main__":
    data = build()
    with open(OUT, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print(f"wrote {OUT}: {len(data['pages'])} pages")
