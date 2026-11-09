"""DMP page module: audience pages and the finder. Data only: PAGES and TO_CONFIRM.
Pages: for-dealers, for-specifiers, for-building-owners, dealer-portal, find-a-system, why-dmp.
Facts come from pages already written in the other dmp_pages_* modules and the content module (all read from dmp.com)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dmp_common import *
import dmp_pages_products as _prod

PAGES = []
TO_CONFIRM = []


def _hero(eyebrow, heading, subhead, primary, secondary, image, alt, w, h):
    return {"type": "hero", "layout": "split", "eyebrow": eyebrow, "heading": heading, "subhead": subhead,
            "primary": primary, "secondary": secondary, "image": image, "image_alt": alt, "image_w": w, "image_h": h}


SYSTEM_RES = [
    ["Intrusion", "Intrusion Systems", "Control panels, detectors and cellular jamming protection.", "See intrusion", "services/intrusion.html"],
    ["Access control", "Access Control", "Credentials, readers, modules and software, from one door to hundreds.", "See access control", "services/access-control.html"],
    ["Fire", "Fire Systems", "Fire control panels, detectors, pull stations and annunciators.", "See fire", "services/fire.html"],
    ["Video", "Video", "VUE Plus cameras, AlarmVision gateways and the video doorbell.", "See video", "services/video.html"],
    ["Communicators", "Communicators and Monitoring", "Cellular and network communicators, plus the receivers that take their signals.", "See communicators", "services/communicators.html"],
    ["Wireless", "Wireless", "Two-way, supervised 900 MHz transmitters, receivers and detectors.", "See wireless", "services/wireless.html"],
    ["Hardware", "Panels and Keypads", "The XT, XTL and XR panels and every keypad that runs on them.", "See panels and keypads", "services/panels-keypads.html"],
    ["Software", "Virtual Keypad and Software", "Virtual Keypad for customers, Dealer Admin and Remote Link for dealers.", "See software", "services/mobile-automation.html"],
]

# ================================================================================================ for-dealers
PAGES.append({
    "file": "for-dealers.html",
    "title": title("For dealers"),
    "description": desc("One sign-in for documents, ordering, Marketing Central, training, quotes and support. What authorized DMP dealers get and how to apply."),
    "crumbs": [["Home", "index.html"], ["For dealers", "for-dealers.html"]],
    "schema": [],
    "sections": [
        _hero("For dealers",
              "Six dealer jobs. <em>One sign-in.</em>",
              "Documents, ordering, Marketing Central, DMP University, Technical Support and quotes. We sell only through authorized dealers, and we have spent fifty years building products for them.",
              {"label": "Order at buy.DMP.com", "href": BUY}, {"label": "See the dealer portal", "href": "dealer-portal.html"},
              IMG + "tab-mobile-1200.jpg", "Virtual Keypad and Dealer Admin on a laptop, tablet and phone", 1200, 900),
        {"type": "cards", "alt": True, "eyebrow": "One sign-in", "heading": "What opens when you sign in",
         "intro": "Each of these has a home today. The plan is to reach all of them from a single account.",
         "items": [
             ["Documentation library", "More than 900 documents: spec sheets, installation and programming guides, quick start guides and technical updates."],
             ["Ordering", "Orders go through the Buy site, which takes orders 24 hours a day, or through Customer Service at 866-266-2826."],
             ["Marketing Central", "Hundreds of marketing assets with your logo and contact details. Your account is free, and so are most assets."],
             ["DMP University", "Dozens of free, on-demand courses, plus 200 sales training videos."],
             ["Technical support", "Technical Support picks up from 7 a.m. to 7 p.m. Central at 888-436-7832."],
             ["Quotes", "Send us the project and the product type, and Inside Sales replies. Inside Sales is 877-757-4367, 8 a.m. to 5 p.m. Central."]]},
        {"type": "detail", "eyebrow": "Ordering", "heading": "The Buy site takes orders 24 hours a day.",
         "body": "Ordering stays on the Buy site, our separate dealer ordering system. Customer Service handles products and ordering, software activations, the Buy site, shipping and order entry questions at 866-266-2826, 8 a.m. to 6 p.m. Central.",
         "bullets": ["Orders at buy.DMP.com, 24 hours a day", "Customer Service: products, ordering, activations and shipping", "Dealer Account: pay invoices, schedule payments and review the status of software licenses"],
         "image": IMG + "tab-mobile-1200.jpg", "image_alt": "Dealer Admin shown on a laptop beside a phone", "image_w": 1200, "image_h": 900},
        {"type": "detail", "alt": True, "flip": True, "eyebrow": "Marketing Central", "heading": "We print and ship brochures and sell sheets at our cost, with no markup.",
         "body": "Your brand is the one that should be promoted, not ours. Choose from hundreds of high quality assets, including product and lifestyle photography, social media and email content, and literature you can customize with your logo and contact information. Customization of more than 75 professional videos is free and fast.",
         "bullets": ["A free account, and free assets", "In-house print shop, at our cost", "Custom keypads and credentials with your logo"],
         "image": IMG + "phone-commercial-1200.jpg", "image_alt": "A person checking a phone as they walk out of a building", "image_w": 1200, "image_h": 800},
        {"type": "detail", "eyebrow": "Training", "heading": "Free courses online, four-day bootcamps at our headquarters.",
         "body": "DMP University is our learning management system for dealers. A DMP University administrator can add, edit and remove employees, assign courses and run reports. For hands-on time, Technician Bootcamps run four days at our headquarters, taught by our Regional Training Managers.",
         "bullets": ["Fewer service calls, faster installs and happier customers", "200 sales training videos through DMP University", "Tech Training Tours and classes at your location"],
         "image": IMG + "tab-spec-1200.jpg", "image_alt": "A DMP spec sheet and a control panel on a desk", "image_w": 1200, "image_h": 900},
        {"type": "cards", "alt": True, "eyebrow": "A dealer account", "heading": "Free firmware, a three year warranty and a return turned around in one business day.",
         "items": [
             ["Dealer Admin", "Your one stop shop for managing your business and your customers' systems: status, analytics, mass programming and bulk remote updates."],
             ["Dealer Account", "Securely pay invoices, schedule payments and review the status of software licenses."],
             ["Free firmware updates", "Software and firmware updates are available from DMP free of charge."],
             ["Customer Return Center", "Our goal is for every request for a product update or repair to be turned around in one business day."],
             ["Three year warranty", "We warrant that the products we manufacture are without defects for three years from the purchase date, under our Terms and Conditions."],
             ["Regional sales managers", "Each territory has a regional sales manager. Inside Sales connects you with the right one."]]},
        {"type": "resources", "eyebrow": "Next", "heading": "Apply, look up a manager or read the full list of dealer services.",
         "items": [
             ["Join", "Become a dealer", "Approval to become an authorized DMP dealer should take just a few days.", "Apply", "support/become-a-dealer.html"],
             ["Services", "Dealer services", "Dealer Admin, Dealer Account, firmware, the Customer Return Center and the warranty.", "See dealer services", "support/dealer-services.html"],
             ["People", "Sales directory", "Regional sales managers by territory, and international distributors.", "Find your manager", "support/sales-directory.html"]]},
        {"type": "faq", "heading": "Questions from dealers", "items": [
            ["Does DMP publish dealer tiers or prices?", "No. Our dealer pages do not list tiers, discounts or prices. Inside Sales can talk through your account at 877-757-4367."],
            ["What kind of dealer do we look for?", "The best security company in its market, growth-minded and consistently installing and selling systems. We generally look for dealers buying at least $5,000 to $10,000 of equipment a month."],
            ["Where do I find spec sheets and guides?", "In the documentation library, which you can filter by product category and document type."],
            ["How do I get training for a new technician?", "Start with the free courses in DMP University. For hands-on labs, register for a Technician Bootcamp, or contact your regional training manager to schedule a class at your location."]] + cf("order")},
        LEADFORM,
    ]})

# ================================================================================================ for-specifiers
PAGES.append({
    "file": "for-specifiers.html",
    "title": title("For architects, engineers and consultants"),
    "description": desc("Spec sheets, A&E specifications, 73 CAD drawings, System Surveyor design tools and UL listings for architects, engineers and consultants."),
    "crumbs": [["Home", "index.html"], ["For specifiers", "for-specifiers.html"]],
    "schema": [],
    "sections": [
        _hero("For architects, engineers and consultants",
              "Spec DMP in minutes: <em>written specs, CAD and a bill of materials.</em>",
              "Everything needed to put a DMP system into a specification: spec sheets for each product, design on a digital floor plan, and Inside Sales to help with system design.",
              {"label": "Open A&E support", "href": "support/ae-support.html"}, {"label": "Find a system", "href": "find-a-system.html"},
              IMG + "tab-spec-1200.jpg", "A DMP product specification and a control panel", 1200, 900),
        {"type": "badges", "label": "Listings", "items": [["UL 2610", "JamAlert, commercial premises security alarm units and systems"], ["UL 864 10th Edition", "XF6 fire panel, Listed for wireless"], ["UL Classified", "SCS-VR virtual receiver software"], ["SOC 2 Type II", "Dealer Admin and Virtual Keypad, every year"]],
         "note": "Listings as stated on DMP product pages. DMP compliance to confirm they are current before publishing."},
        {"type": "cards", "alt": True, "eyebrow": "What you can start from", "heading": "Four places a specification begins",
         "items": [
             ["Spec sheets", "One product, its specifications and ordering details, for example the XR550 Spec Sheet or the VUE 5MP Cameras Spec Sheet."],
             ["A&E specifications", "Written specifications for the XF6, XT30/XT50, XR150/XR550 and XTL Series panels, the DualComNF communicator, the SCS-1R receiver and the CX-702."],
             ["CAD drawings", "73 drawings in six groups, including control panels, enclosures, modules and expanders, and door applications."],
             ["Inside Sales", "System design, architect and engineer support and pre-sales support at 877-757-4367, 8 a.m. to 5 p.m. Central."]]},
        {"type": "detail", "eyebrow": "Design tools", "heading": "Place panels, keypads and readers on a floor plan and get the bill of materials.",
         "body": "System Surveyor lets you design DMP intrusion, access control, fire and video systems on a digital floor plan, capturing project requirements as you go. Five DMP product catalogs import into it, and the generated bill of materials can be shared with customers and teams.",
         "bullets": ["IDS, fire alarm, ACS, video surveillance and X1 ACS catalogs", "Digital as-builts for later maintenance and expansion", "A free dealer tier, with no certification required"],
         "image": IMG + "system-surveyor-1200.jpg", "image_alt": "A designer placing DMP devices on a digital floor plan on a tablet", "image_w": 1200, "image_h": 732},
        {"type": "detail", "alt": True, "flip": True, "eyebrow": "UL and compliance", "heading": "JamAlert is UL 2610 certified, and the XF6 is UL 864 10th Edition Listed for wireless.",
         "body": "We have made a UL Listed combination burglary, fire and access control panel since 1997. The SCS-VR virtual receiver is UL Classified software. Communicators approved for the FirstNet public-safety network are in the catalog, and our government page lists a white paper on NDAA, BAA and TAA compliance.",
         "bullets": ["UL 2610 for JamAlert, the standard for commercial premises security alarm units and systems", "SOC 2 Type II examination every year for Dealer Admin and Virtual Keypad", "Manufactured in the USA with U.S. and global components"],
         "image": IMG + "tab-fire-1200.jpg", "image_alt": "The DMP XF6 fire control panel", "image_w": 1200, "image_h": 900},
        {"type": "detail", "eyebrow": "The library", "heading": "More than 900 documents, filtered by product category and document type.",
         "body": "Spec sheets, installation and programming guides, quick start guides, technical updates, battery calculators and CAD drawings are in one library. Inside Sales can point you to the right one if you are not sure which you need.",
         "bullets": ["Sixteen product categories, plus international variants", "File types: PDF, XLSX, PPTX and ZIP", "Documents are listed on each product page"],
         "image": IMG + "tab-intrusion-1200.jpg", "image_alt": "A DMP control panel circuit board", "image_w": 1200, "image_h": 900},
        {"type": "detail", "stage": True, "eyebrow": "The spec pack", "heading": "Download the spec pack from the library.",
         "body": "Spec sheets, A&E specifications, installation guides and CAD drawings sit in one documentation library, filtered by product category and document type.",
         "bullets": ["Written specs for the XF6, DualComNF, SCS-1R, XT30/XT50, XR150/XR550, CX-702 and XTL Series", "73 CAD drawings in six groups", "Inside Sales can point you to the right document"],
         "image": IMG + "tab-spec-1200.jpg", "image_alt": "A tablet showing a floor plan with DMP devices", "image_w": 1200, "image_h": 900,
         "cta": {"label": "Download the spec pack", "href": "support/documentation.html"}},
        {"type": "services", "heading": "Start from the system or the building",
         "intro": "Each opens a page with the products, specifications and documents for that part of a system.",
         "items": [["Product finder", "Choose a product type and a system, and see matching products.", "find-a-system.html"],
                   ["Products by system", "Intrusion, access control, fire, video, communicators, wireless, panels and software.", "services.html"],
                   ["Technology partners", "Six partners with verified DMP integrations.", "partners.html"]]},
        {"type": "faq", "heading": "Questions from specifiers", "items": [
            ["Can I specify DMP equipment directly?", "We sell through authorized dealers and distributors, so a project is bought through a dealer. Inside Sales helps with system design and can connect you with the right dealer or regional sales manager."],
            ["Which products have written A&E specifications?", "The XF6, DualComNF, SCS-1R, XT30/XT50, XR150/XR550, CX-702 and XTL Series."],
            ["Where are the CAD drawings?", "On the A&E support page, in six groups from control panels and enclosures to single and multi-door applications."]] + cf("person")},
        LEADFORM,
    ]})

# ================================================================================================ for-building-owners
PAGES.append({
    "file": "for-building-owners.html",
    "title": title("For building owners"),
    "description": desc("How to buy a DMP security system through an authorized dealer, what to ask before you sign, and how to reach DMP to find a dealer near you."),
    "crumbs": [["Home", "index.html"], ["For building owners", "for-building-owners.html"]],
    "schema": [],
    "sections": [
        _hero("For building owners and managers",
              "Buy through a dealer. <em>Choose a good one.</em>",
              "We make the panels, keypads, communicators and software, and authorized dealers design, install and service them. Start with the building and a short list of questions.",
              {"label": "Find a dealer", "href": "find-a-dealer.html"}, {"label": "Find a system", "href": "find-a-system.html"},
              IMG + "tab-owner-1200.jpg", "A person checking a phone as they leave a building", 1200, 900),
        {"type": "cards", "alt": True, "eyebrow": "How it works", "heading": "Four steps from the first call to a system you control",
         "items": [
             ["1. Describe the building", "Tell us or a dealer what you need to protect: doors, alarm zones, cameras, fire. Our systems run intrusion, access control, fire and video."],
             ["2. Talk to a dealer", "We sell through authorized dealers and distributors. A dealer designs the system and installs it. Our Inside Sales team supports system design."],
             ["3. Review the design", "Dealers can lay out a system on a digital floor plan and produce a bill of materials, so you see what is going where."],
             ["4. Control it from a phone", "Virtual Keypad runs on iOS and Android and in a browser. It arms and disarms the system and controls locks, lights and thermostats."]]},
        {"type": "cards", "eyebrow": "What to ask", "heading": "Six questions that separate a good proposal from a vague one",
         "items": [
             ["Which panel, and how many doors and zones does it support?", "The XR550 supports 96 doors and 574 zones. The dealer should say which panel fits your building and why."],
             ["How does the system report an alarm?", "Ask for the paths: network, cellular or both, and what happens when one fails."],
             ["Can my doors and my alarm be one system?", "Intrusion and access control can share a panel, and one database manages credentials."],
             ["Can I use my phone as a key?", "Digital Key puts a credential in a phone's mobile wallet, and it works even when the phone is out of power."],
             ["Who monitors it, and who do I call at night?", "Ask who answers an alarm and who answers a service call, and at what hours."],
             ["What happens if I change dealers?", "Ask who holds the programming and the customer account, and how it would be handed over."]]},
        {"type": "services", "heading": "Industries we have written for", "intro": "Each page says which DMP products fit that kind of building.",
         "items": [["Commercial", "Intrusion, fire, access, wireless and video from one manufacturer.", "industries/commercial.html"],
                   ["Education", "Campus security with a lockdown, and a phone for a key.", "industries/education.html"],
                   ["Healthcare and wellness", "Protect the building and the patient records inside it.", "industries/healthcare-wellness.html"],
                   ["Multi-tenant", "A phone for a key, and an access level just for the pool.", "industries/multi-tenant.html"],
                   ["Retail", "One system across every store.", "industries/retail.html"],
                   ["All eleven industries", "From financial institutions to storage units.", "industries.html"]]},
        {"type": "detail", "alt": True, "flip": True, "eyebrow": "Control", "heading": "Home, Sleep, Away: three arming levels, one touch.",
         "body": "Virtual Keypad is the customer app for remote arming, alarm verification, schedules, geofences and device control. Dealers can brand it with their name and logo.",
         "bullets": ["Access Only users get basic access without seeing events or video", "False Alarm Question silences an alarm while the system stays armed", "Lockdown can start from the app, a keypad or any PC running Entré software"],
         "image": IMG + "vk-mock-1200.png", "image_alt": "Virtual Keypad on a laptop, tablet and phone", "image_w": 1200, "image_h": 800},
        {"type": "detail", "eyebrow": "Finding a dealer", "heading": "Call Inside Sales at 877-757-4367 with your city or state.",
         "body": "Tell us where the building is, or send the form below, and Inside Sales will connect you with the regional sales manager for your territory, who can point you to an authorized dealer. Our regional sales managers cover territories from New England to Los Angeles.",
         "bullets": ["Inside Sales is open 8 a.m. to 5 p.m. Central", "Outside the United States, see our international distributors", "Dealers can apply to join if you already have an installer in mind"],
         "image": IMG + "hq-exterior-1200.jpg", "image_alt": "The DMP headquarters building", "image_w": 1200, "image_h": 800},
        {"type": "resources", "eyebrow": "Also useful", "heading": "Where to go next",
         "items": [["Contact", "Contact us", "Inside Sales, Technical Support and Customer Service, with hours.", "Contact DMP", "contact.html"],
                   ["People", "Sales directory", "How regional sales managers are organized by territory.", "See the directory", "support/sales-directory.html"],
                   ["Outside the U.S.", "International distributors", "Authorized distributors from Benelux to South Africa, plus Mexico and Latin America.", "Find a distributor", "international.html"],
                   ["Quotes", "Get a quote", "Tell us about the project and a person will reply.", "Get a quote", "support/get-a-quote.html"]]},
        {"type": "faq", "heading": "Questions from building owners", "items": cf("who", "person", "usa") + [
            ["Does the system need a monitoring contract?", "Alarm signals can report to a monitoring center, which is arranged through your dealer. Ask the dealer how monitoring is set up and billed."]]},
        LEADFORM,
    ]})

# ================================================================================================ dealer-portal
PAGES.append({
    "file": "dealer-portal.html",
    "title": title("Dealer portal"),
    "description": desc("One sign-in for the documentation library, the Buy site, Marketing Central, DMP University, Technical Support and quotes. A proposed design."),
    "crumbs": [["Home", "index.html"], ["For dealers", "for-dealers.html"], ["Dealer portal", "dealer-portal.html"]],
    "schema": [],
    "sections": [
        _hero("Dealer portal",
              "One account, six places a dealer <em>already works</em>.",
              "Today a dealer moves between the documentation library, the Buy site, Marketing Central, DMP University and Technical Support. The portal puts a single sign-in in front of all of them.",
              {"label": "What dealers get", "href": "for-dealers.html"}, {"label": "Become a dealer", "href": "support/become-a-dealer.html"},
              IMG + "tab-mobile-1200.jpg", "Dealer Admin and Virtual Keypad on a laptop, tablet and phone", 1200, 900),
        {"type": "portal", "id": "portal", "eyebrow": "Single sign-in", "heading": "Sign in once, then go where the job is.",
         "intro": "A design for the dealer sign-in. Every tile leads to something we run today.",
         "tiles": [
             ["Documentation library", "More than 900 spec sheets, guides, quick start guides and technical updates.", "docs"],
             ["Order on the Buy site", "Orders 24 hours a day on the Buy site, our separate dealer ordering system.", "cart"],
             ["Marketing Central", "Brochures, videos, photography and branded keypads, with your logo and contact details.", "megaphone"],
             ["DMP University training", "Free on-demand courses and 200 sales training videos.", "training"],
             ["Technical support", "888-436-7832, 7 a.m. to 7 p.m. Central, plus the technical FAQs.", "support"],
             ["Get a quote", "Send the project to Inside Sales and a person replies.", "quote"]],
         "cta_label": "Order on the Buy site", "cta_href": BUY, "signin_label": "Dealer sign-in"},
        {"type": "network", "id": "network", "eyebrow": "Proposed design, to confirm with DMP IT",
         "heading": "One dealer record, connected to the systems the dealer already uses.",
         "intro": "This diagram is a proposal. How Marketing Central and the Buy site connect today has not been confirmed, so every link below is to be validated with DMP IT before anything is built.",
         "hub": "Dealer portal sign-in",
         "nodes": [
             ["Dealer CRM record", "One record for the dealer company and its people, the source for who may sign in and what they see."],
             ["Buy site", "Stays a separate ordering system. The portal sends the signed-in dealer there."],
             ["Marketing Central", "Hundreds of assets and custom videos. The portal would pass the dealer's logo and contacts through."],
             ["DMP University", "Courses and sales videos, with administrators who manage their own team."],
             ["Documentation library", "Spec sheets, guides and updates."],
             ["Dealer Admin and Dealer Account", "Programming, customers, invoices and licenses, which dealers already use."]]},
        {"type": "cards", "alt": True, "eyebrow": "What we would confirm first", "heading": "Four questions come before any build",
         "items": [
             ["How do Marketing Central and the Buy site sign in today?", "Each has its own login. We need to know whether either can accept a shared identity."],
             ["Which record is the source of truth for a dealer?", "The CRM record would decide who can sign in, and which staff roles see which tiles."],
             ["Which tiles are visible to which people?", "A dealer owner, a technician and a sales lead may need different views."],
             ["What happens at sign-out and when an employee leaves?", "Access should end in one place, across every connected system."]]},
        {"type": "detail", "eyebrow": "What stays the same", "heading": "Dealer Admin, the Buy site and Marketing Central keep doing their own jobs.",
         "body": "The portal does not replace them. It is the front door: one sign-in, one set of staff, and a route to each tool. Dealer Admin still programs panels and manages Virtual Keypad users, and orders are still placed on the Buy site.",
         "bullets": ["Orders stay on the Buy site", "Dealer Admin keeps programming, customers and invoices", "Marketing Central keeps the asset library and print shop"],
         "image": IMG + "vk-mock-1200.png", "image_alt": "Virtual Keypad on a laptop, tablet and phone", "image_w": 1200, "image_h": 800},
        {"type": "faq", "heading": "Questions about the dealer portal", "items": [
            ["Is the dealer portal live?", "Not yet. It is a proposed design that needs confirmation with DMP IT."],
            ["Where do I order today?", "At buy.DMP.com, which takes orders 24 hours a day."],
            ["How do I sign up for Marketing Central?", "Sign up for a free account on the marketing support page. Most assets are free."],
            ["How do I become a dealer?", "Apply on the become a dealer page. Approval to become an authorized DMP dealer should take just a few days."]]},
        LEADFORM,
    ]})

# ================================================================================================ find-a-system
# The building-type filter was removed: nearly every product tags every building, so it narrowed nothing. The first filter is now the product type.
TYPES = [("panels", "Control panels"), ("keypads", "Keypads"), ("access", "Credentials and access"), ("comm", "Communicators and receivers"),
         ("sensors", "Detectors and wireless devices"), ("cameras", "Cameras and gateways"), ("software", "Apps and software")]
PRODUCT_TYPE = {}
for _k, _ss in {"panels": "xt75 xt50 xtlplus xtltouch xr150 xr550 xr650 tmsentry xf6 xr150fc-2 xr550fc-2", "keypads": "7-inch-touchscreen-keypad graphic-touchscreen 9800-series 7000-series aqualite-series icon-series",
                "access": "digital-key-credential mobile-credential dmp-bluetooth-reader-and-mobile-credential 734n x1 entre-lite entre-enterprise",
                "comm": "cellcom dualcom 263lte 263lte-firstnet 265lte scs-vr-virtual-receiver-software scs-1r jamalert", "sensors": "850 630f 2w-blx 1100xh 1101 1128 1142 1164 1100t",
                "cameras": "xv-gateways-with-alarmvision v-6022wc vplus-7061-fe vplus-7121-fe vplus-7081-bdv vue-video-doorbell", "software": "virtual-keypad dealer-admin remote-link"}.items():
    for _s in _ss.split():
        PRODUCT_TYPE[_s] = _k
NEEDS = [("intrusion", "Intrusion"), ("access", "Access control"), ("fire", "Fire"), ("video", "Video"), ("wireless", "Wireless"),
         ("mobile", "Mobile and cloud"), ("comm", "Communicators")]
# Needs follow each product's own page text: category, blurb and the system line in services. Conservative on purpose.
PRODUCT_NEEDS = {
    "digital-key-credential": ["access", "mobile"], "mobile-credential": ["access", "mobile"],
    "dmp-bluetooth-reader-and-mobile-credential": ["access"], "734n": ["access"], "x1": ["access", "mobile"],
    "entre-lite": ["access"], "entre-enterprise": ["access"],
    "cellcom": ["comm"], "dualcom": ["comm"], "263lte": ["comm"], "263lte-firstnet": ["comm"], "265lte": ["comm"],
    "scs-vr-virtual-receiver-software": ["comm"], "scs-1r": ["comm"],
    "xt75": ["intrusion", "access", "video"], "xt50": ["intrusion"], "xtlplus": ["intrusion", "wireless"], "xtltouch": ["intrusion", "wireless"],
    "xr150": ["intrusion", "access"], "xr550": ["intrusion", "access", "fire", "video"], "xr650": ["intrusion"], "tmsentry": ["intrusion"],
    "7-inch-touchscreen-keypad": ["intrusion"], "graphic-touchscreen": ["intrusion"], "9800-series": ["intrusion", "wireless"],
    "7000-series": ["intrusion"], "aqualite-series": ["intrusion"], "icon-series": ["intrusion"],
    "xf6": ["fire"], "xr150fc-2": ["fire", "intrusion", "access"], "xr550fc-2": ["fire", "intrusion", "access"],
    "850": ["fire"], "630f": ["fire"], "2w-blx": ["fire"], "jamalert": ["intrusion"],
    "virtual-keypad": ["mobile"], "dealer-admin": ["mobile"], "remote-link": ["mobile"],
    "xv-gateways-with-alarmvision": ["video", "intrusion"], "v-6022wc": ["video"], "vplus-7061-fe": ["video"], "vplus-7121-fe": ["video"],
    "vplus-7081-bdv": ["video"], "vue-video-doorbell": ["video"],
    "1100xh": ["wireless"], "1101": ["wireless"], "1128": ["wireless", "intrusion"], "1142": ["wireless", "intrusion"], "1164": ["wireless", "fire"], "1100t": ["wireless"],
}
_missing = [s for s in _prod.PRODUCTS if s not in PRODUCT_NEEDS or s not in PRODUCT_TYPE]
assert not _missing, _missing
FINDER_PRODUCTS = [{"name": p["name"] + (" (coming soon)" if s == "xr650" else ""), "img": p["image"], "href": f"products/{s}.html", "blurb": p["blurb"],
                    "buildings": [PRODUCT_TYPE[s]], "needs": PRODUCT_NEEDS[s]} for s, p in _prod.PRODUCTS.items()]
FLAGSHIP = ["xr550", "xt75", "x1", "digital-key-credential", "vplus-7081-bdv", "virtual-keypad", "dealer-admin", "xf6"]
SHOWCASE = [[_prod.PRODUCTS[s]["name"], _prod.PRODUCTS[s]["image"], f"products/{s}.html", _prod.PRODUCTS[s]["blurb"]] for s in FLAGSHIP]

PAGES.append({
    "file": "find-a-system.html",
    "title": title("Find a system"),
    "description": desc("Pick a product type and a system, and see matching DMP products: intrusion, access control, fire, video, wireless, mobile and communicators."),
    "crumbs": [["Home", "index.html"], ["Find a system", "find-a-system.html"]],
    "schema": [itemlist("DMP products", [[f["name"], f["href"]] for f in FINDER_PRODUCTS])],
    "sections": [
        _hero("Find a system",
              "Find the right DMP product <em>in two clicks.</em>",
              "Intrusion, access control, fire, video, wireless, mobile and communicators from one manufacturer. Choose a product type, choose a system, and open the product page.",
              {"label": "Jump to the finder", "href": "#finder"}, {"label": "Products by system", "href": "services.html"},
              IMG + "tab-intrusion-1200.jpg", "A DMP control panel circuit board", 1200, 900),
        {"type": "showcase3d", "id": "flagships", "eyebrow": "Flagship products", "heading": "Eight products that show what one platform does.",
         "intro": "From the XR550 with 96 doors to a credential that lives in a phone's wallet.", "items": SHOWCASE},
        {"type": "finder", "id": "finder", "eyebrow": "Product finder", "heading": "Choose a product type, then a system.",
         "building_label": "Product type", "need_label": "System",
         "intro": "Each filter narrows the list. The industry pages say which products we feature for each kind of building.",
         "buildings": [{"key": k, "label": l} for k, l in TYPES], "needs": [{"key": k, "label": l} for k, l in NEEDS],
         "products": FINDER_PRODUCTS},
        {"type": "stats3d", "id": "facts", "items": [["50", "Years making security systems"], ["SOC 2 Type II", "Examined every year"], ["14", "Product categories"], ["USA", "Manufactured with U.S. and global components"]]},
        {"type": "resources", "eyebrow": "By system", "heading": "Prefer to browse a whole system?", "items": SYSTEM_RES},
        {"type": "faq", "heading": "Questions about choosing a system", "items": [
            ["How do I choose a panel?", "Start from the building, the zones and the doors, then match the panel family. A DMP dealer does this, and our Inside Sales team supports system design."],
            ["Why does every product show for every building?", "Our products are not made for one type of building. The industry pages say which products we feature for each."],
            ["Where are the spec sheets?", "On each product page and in the technical documentation library."]] + cf("who")},
        LEADFORM,
    ]})

# ================================================================================================ why-dmp
PAGES.append({
    "file": "why-dmp.html",
    "title": title("Why DMP"),
    "description": desc("Made in the USA, 50 years in business, open integrations, one platform across intrusion, access, fire and video, SOC 2 Type II, phone support and training."),
    "crumbs": [["Home", "index.html"], ["Why DMP", "why-dmp.html"]],
    "schema": [],
    "sections": [
        _hero("Why DMP",
              "Security is all we make. <em>Fifty years of it.</em>",
              "While others have made security a piece of their business, we have made it the entirety of ours. We build the panels, keypads, communicators and software, and sell them through authorized dealers.",
              {"label": "Contact DMP", "href": "contact.html"}, {"label": "Find a system", "href": "find-a-system.html"},
              IMG + "hq-exterior-1200.jpg", "The DMP headquarters building", 1200, 800),
        {"type": "detail", "alt": True, "eyebrow": "Made in the USA", "heading": "Every DMP product is quality tested before it ships.",
         "body": "We manufacture our products in the USA with U.S. and global components. Made in the USA is something you rarely see today, and building here keeps us close to our customers and our community.",
         "bullets": ["100 percent of products are quality tested before shipping", "Designed and built in the U.S.A. for federal, state and local government", "Three year warranty, and a Customer Return Center aiming for one business day"],
         "image": IMG + "plant-1200.jpg", "image_alt": "The DMP production floor", "image_w": 1200, "image_h": 800},
        {"type": "detail", "flip": True, "eyebrow": "Fifty years", "heading": "We started in 1975, and the first XR Series was 32 times faster than before.",
         "body": "We began as an R&D department building a central station product. Along the way came Two-Way wireless in 2004, the XT Series in 2008, the first software-only central station receiver in 2009, Virtual Keypad in 2011 and the XR Series in 2013.",
         "bullets": ["A UL Listed combination burglary, fire and access panel in 1997", "X1 Series, stand-alone cloud-based access control, in 2021", "Fifty years in business in 2025"],
         "image": IMG + "fifty-1200.jpg", "image_alt": "The DMP fiftieth anniversary mark", "image_w": 1200, "image_h": 495},
        {"type": "cards", "alt": True, "eyebrow": "One platform", "heading": "Intrusion, access, fire and video share one panel, one app and one set of accounts.",
         "items": [
             ["Intrusion", "XT and XR Series panels scale from a small business to a large site."],
             ["Access control", "The XR550 supports 96 doors, and Digital Key puts the credential in a phone's wallet."],
             ["Fire", "The XR550FC combines intrusion, fire and access control with a fire command center keyboard."],
             ["Video", "AlarmVision analytics raise alarms into XT75 and XR Series panels."]]},
        {"type": "detail", "eyebrow": "Open integrations", "heading": "Six partners have verified integrations, and our access modules speak OSDP.",
         "body": "Evolon, System Surveyor, SureView, Genetec, HavenLock and ASSA ABLOY Aperio each have a verified integration with DMP. The 1100T translator learns in up to 128 zones of other makers' transmitters, so a dealer can take over a site without rewiring.",
         "bullets": ["Most integrations are configured in Dealer Admin with DMP API credentials", "OSDP, BIN code and 1100 Series wireless support in access modules since 2020", "A technology partner program for software and hardware makers"],
         "image": IMG + "system-surveyor-1200.jpg", "image_alt": "A designer placing DMP devices on a digital floor plan", "image_w": 1200, "image_h": 732},
        {"type": "detail", "alt": True, "flip": True, "eyebrow": "SOC 2 Type II", "heading": "A licensed CPA firm examines Dealer Admin and Virtual Keypad every year.",
         "body": "Both are hosted in a Tier 4 data center and examined in line with AICPA standards. The SOC 3 report is intended for public distribution, and SOC 2 reports go to customers and partners under confidentiality.",
         "bullets": ["Independent examination every year", "A public SOC 3 report", "Encrypted site-to-site connections with VAULT"],
         "image": IMG + "vault-1200.jpg", "image_alt": "A glowing shield with a padlock", "image_w": 1200, "image_h": 800},
        {"type": "cards", "eyebrow": "Support", "heading": "Four phone lines, each run by the team that owns the answer.",
         "items": [
             ["Inside Sales: 877-757-4367", "System design, architect and engineer support, quotes and pricing. 8 a.m. to 5 p.m. Central."],
             ["Technical Support: 888-436-7832", "Installation, programming, troubleshooting and diagnostics. 7 a.m. to 7 p.m. Central."],
             ["Customer Service: 866-266-2826", "Products and ordering, software activations, shipping. 8 a.m. to 6 p.m. Central."],
             ["SecureCom Wireless: 877-300-8030", "Activation or billing questions. 8 a.m. to 5 p.m. Central."]]},
        {"type": "detail", "alt": True, "eyebrow": "Training", "heading": "Dozens of free courses, 200 sales videos and four-day bootcamps.",
         "body": "Trained technicians mean fewer service calls, faster installs and happier customers. DMP University is free and on demand. Bootcamps teach hands-on labs at our headquarters, and Tech Training Tours visit regional cities.",
         "bullets": ["DMP University for dealers", "Technician and Advanced Technician Bootcamps", "A one-hour live Virtual Keypad webinar for your customer"],
         "image": IMG + "tab-spec-1200.jpg", "image_alt": "A DMP spec sheet and a control panel", "image_w": 1200, "image_h": 900},
        LEADFORM,
    ]})

# ================================================================================================ find-a-dealer
PAGES.append({
    "file": "find-a-dealer.html",
    "title": title("Find an authorized dealer"),
    "description": desc("DMP sells only through authorized dealers. Tell us where the building is and what kind of building it is, and a person at DMP will reply."),
    "crumbs": [["Home", "index.html"], ["For building owners", "for-building-owners.html"], ["Find a dealer", "find-a-dealer.html"]],
    "schema": [],
    "sections": [
        _hero("Find a dealer",
              "Find an authorized DMP dealer <em>near you</em>.",
              "DMP sells only through authorized dealers and distributors. Tell us where the building is and what it needs, and a person at DMP will reply.",
              {"label": "Call Inside Sales 877-757-4367", "href": "tel:+18777574367"}, {"label": "Sales directory", "href": "support/sales-directory.html"},
              IMG + "tab-owner-1200.jpg", "A person checking a phone as they leave a building", 1200, 900),
        {"type": "spotlight", "id": "how", "eyebrow": "How it works", "heading": "From your address to an authorized dealer.",
         "body": "We make the panels, keypads, communicators and software. Authorized dealers design, install and service the systems, so the right first step is a conversation with DMP about where you are.",
         "needs": ["Tell us: where the building is, and what kind of building it is", "A person replies: Inside Sales connects you with the regional sales manager for your territory", "Meet a dealer: an authorized dealer designs, installs and services the system"],
         "image": IMG + "tab-owner-1200.jpg", "image_alt": "A person checking a phone as they leave a building", "tag": "Buy through a dealer", "cta": {"label": "Tell us your location", "href": "#start"}},
        {"type": "tiles", "id": "paths", "eyebrow": "Prefer to look it up yourself?", "heading": "Three other ways in.", "items": [
            ["Sales directory", "Regional sales managers by territory, with titles and regions.", "support/sales-directory.html", IMG + "hq-exterior-1200.jpg"],
            ["Call Inside Sales", "877-757-4367, 8 a.m. to 5 p.m. Central. A person will point you to the right dealer.", "contact.html", IMG + "tab-mobile-1200.jpg"],
            ["Outside the U.S.", "Authorized distributors in the United Kingdom, Mexico, South Africa and more.", "international.html", IMG + "banner-allin-1200.jpg"]]},
        {**LEADFORM, "id": "start", "heading": "Tell us your location and building",
         "body": "Say where the building is and what kind of building it is, and a person at DMP will reply."},
        {"type": "faq", "heading": "Questions about finding a dealer", "items": cf("who", "person", "where")},
    ]})

TO_CONFIRM += [
    "Dealer tiers and pricing: the dealer pages we read do not describe tiers, discounts or prices, so none are written. DMP to confirm whether tiers exist and whether any can be shown.",
    "The single sign-in is a proposal. How Marketing Central (portal.assets.site) and the Buy site (buy.dmp.com) authenticate today is unconfirmed; the network diagram on the dealer portal page is labelled as a proposed design for DMP IT to validate.",
    "Dealer CRM record: which system is the source of truth for dealers, and whether DMP wants role-based tiles, is unconfirmed.",
    "Only the Order button links to the Buy site. Marketing Central login and sign-up are external to the preview and are not linked.",
    "Product finder tags: systems were inferred conservatively from each product's own page text, and the product type (panel, keypad, credential, communicator, detector, camera, software) from its name and category. The building-type filter was removed because every product fits every building. DMP to confirm the tags.",
    "The 8 flagship products in the showcase (XR550, XT75, X1, Digital Key, VUE Plus 8MP bullet, Virtual Keypad, Dealer Admin, XF6) are our selection. DMP to confirm the lineup. The XR650 is left out because it is marked coming soon.",
    "Stats: 50 years (founded 1975; fifty years in business reported for 2025), SOC 2 Type II, 14 product categories and 'manufactured in the USA with U.S. and global components' come from existing site copy. Confirm the 14 count against the current product catalog.",
    "Find a dealer: the page and its form are a placeholder for a real dealer locator. No window for a reply is stated because DMP's pages state none. DMP to confirm who answers the form, how fast, and whether a locator is wanted.",
    "Specifier page: the new headline says 'in minutes'. DMP to confirm that claim, and DMP compliance to sign off the Listings strip (UL 2610, UL 864 10th Edition, UL Classified) before publishing.",
    "Finding a dealer: no public dealer locator exists on the pages we read. The page routes owners to Inside Sales and the contact form. DMP to confirm that is how owners should be handled, and whether a locator is wanted.",
    "Specifier page: the free System Surveyor dealer tier and 'no certification required' are taken from the partner page. UL 864 10th Edition and UL Classified claims are taken from the XF6 and SCS-VR product pages. DMP to confirm they are current.",
    "The building owner questions to ask a dealer are general buying advice, not DMP claims. DMP to approve the wording, especially the questions on monitoring and changing dealers.",
    "'Home, Sleep, Away' and 'False Alarm Question' are from the residential page, and 'Access Only user' from the multi-tenant page.",
    "Images reuse existing files in the assets folder. Several are product shots shared across pages, and DMP should supply fresh photography for the audience pages.",
]
