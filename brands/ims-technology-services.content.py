#!/usr/bin/env python3
"""IMS Technology Services: the three website directions, as data.

Rebuilt 9 November 2026 after the first headless build (Client Command build 7f46fbdc) uploaded the site but lost its
content file when the commit step failed. Facts come from imsts.com (every page crawled on 9 November 2026, the five
case studies, the awards pages), the Client Command brief, and the QBS SEO and AEO analysis of 13 September 2026.
Photography is IMS's own, downloaded from imsts.com at full resolution; the award badges are the ones IMS publishes.

Voice: IMS speaking to a buyer. Sourcing caveats live in pitch["confirm"], never in page copy.
No em dashes, no exclamation marks, no response-time or pricing promises IMS has not published.

Run:
    python3 brands/ims-technology-services.content.py
    python3 scripts/build.py ims-technology-services --shots
"""
import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ims-technology-services.content.json")

CLIENT = "IMS Technology Services"
SHORT = "IMS"
PHONE, PHONE_HREF = "610-361-1870", "tel:+16103611870"
FOUNDED = "1994"
REGION = "us"
SITE = "https://www.imsts.com"

# ------------------------------------------------------------------ sourced facts
TESTIMONIALS = [  # published on imsts.com
    ["Your calm, get-it-done demeanor was much appreciated during the organized chaos that is a group meeting. So what if another organization needs to get an electric car delivered and rolled through the ballroom that you're setting up? No problem. You and your entire team were always ready to pitch in and help out.", "ECOG-ACRIN Cancer Research Group", "Event staging customer"],
    ["I reviewed quite a few proposals, including the on-site AV vendor, and no other company came close to offering the service, expertise and pricing of IMS.", "Saint Joseph's University", "Event staging customer"],
    ["Your team really exceeded my expectations (and I came into this with high expectations based on your supplier presentation). Not only did you deliver a really tight and well-produced video, you did so in a way that made the featured platform look really dynamic.", "ETS", "Content creation customer"],
    ["We were confident from the early planning stages that the AV for the meeting would work exactly as we needed it to because you were on top of everything from the beginning.", "Clinical Immunology Society", "Event staging customer"],
    ["The end result is a truly phenomenal commencement video celebration, one which honors our graduates in an exceptional manner. To the IMS team, Drexel is fortunate to have such wonderful partners in each of you, thank you for your work.", "Drexel University", "Commencement video customer"],
]
LOCATIONS = [  # slug, city, address 1, address 2, phone, phone href, label, lon, lat, state
    ["garnet-valley", "Garnet Valley", "3055 McCann Farm Drive", "Garnet Valley, PA 19060", PHONE, PHONE_HREF, "Headquarters", -75.4838, 39.8565, "PA"],
    ["linwood", "Linwood", "2000 Columbia Avenue, Suite 300", "Linwood, PA 19061", PHONE, PHONE_HREF, "Event Staging", -75.4238, 39.8248, "PA"],
    ["orlando", "Orlando", "404 Sunport Lane, Suite 350", "Orlando, FL 32809", PHONE, PHONE_HREF, "Southeast", -81.3974, 28.4310, "FL"],
    ["plano", "Plano", "3001 Technology Dr., Suite 100", "Plano, TX 75009", PHONE, PHONE_HREF, "Mid-West", -96.6989, 33.0198, "TX"],
    ["westlake-village", "Westlake Village", "5321 Sterling Center Dr.", "Westlake Village, CA 91361", PHONE, PHONE_HREF, "West Coast", -118.8059, 34.1458, "CA"],
]
PARTNERS = ["Crestron", "Extron", "Biamp", "QSC", "Cisco", "Christie", "Planar", "Haivision", "Polycom", "Zoom", "Webex"]
SEAL_ITEMS = [
    ["1", "One contract, one accountable team", "Design and implementation under one contract, with a single point of accountability from the first drawing to the last cable."],
    ["PM", "A dedicated production manager", "Every event customer gets a dedicated production manager and account representative, from planning through fulfillment."],
    ["10+", "A project team with tenure", "Project manager, system engineer, lead technician and field engineer, averaging more than ten years in the industry."],
    ["ISO", "ISO/IEC 27001:2022", "Information security management that meets the international standard, for clients who cannot afford a leak."],
    ["APEx", "AVIXA APEx and InfoComm Diamond", "AVIXA AV Provider of Excellence, and InfoComm Diamond level certification."],
    ["24/7", "Rooms watched around the clock", "Managed Services monitors installed systems 24/7/365, with tiers that match coverage to what is mission-critical."],
]
TEAM = [  # as listed on imsts.com
    ["Paul Wedesky, CASE, CMP", "President, Event Staging"],
    ["Dave Fisher", "President, Systems Integration"],
    ["Austin Conner", "Chief Financial Officer"],
    ["Jay Rule", "VP, Business Development, Event Staging"],
    ["John Beaulieu", "VP, Sales and Marketing, Systems Integration"],
    ["Chris Leonard", "VP, Operations, Event Staging"],
    ["Anthony P. Grassia Jr., CTS", "VP, Production Management, Event Staging"],
    ["Danielle Byrne, PMP, CTS", "VP, Operations, Systems Integration"],
    ["Ed Easley, CTS-I, CQT", "Director of Managed Services"],
]

# The work: the five Commercial Integrator award projects (case studies on imsts.com) and two staged events.
WORK = [
    {"title": "Longwood Reimagined, Longwood Gardens", "chip": "Best Large Venue, 2025", "image": "assets/work-longwood.jpg", "href": "services/systems-integration.html",
     "line": "AV integration across a multiyear, $250 million transformation of one of the world's premier gardens, in Kennett Square, Pennsylvania.",
     "alt": "The new glass conservatory at Longwood Gardens"},
    {"title": "U.S. Squash national center, Philadelphia", "chip": "Best Large Venue, 2021", "image": "assets/work-us-squash.jpg", "href": "services/systems-integration.html",
     "line": "The 1916 33rd Street Armory, reborn as the home of U.S. Squash with Drexel University.", "alt": "Glass squash courts inside the 33rd Street Armory"},
    {"title": "Medallion Hall, Five Below headquarters", "chip": "Best Meeting Room, 2024", "image": "assets/work-five-below.jpg", "href": "services/systems-integration.html",
     "line": "A corporate conference theater in the historic Lits Brothers Building.", "alt": "Tiered colored seating facing three displays in Medallion Hall"},
    {"title": "Learning Stair video wall, West Chester University", "chip": "Best Higher Education, 2023", "image": "assets/work-wcu-video-wall.jpg", "href": "services/digital-signage-video-walls.html",
     "line": "A two-story direct-view LED wall of 264 panels, 23 by 24 feet.", "alt": "A two-story LED wall above the dining hall at West Chester University"},
    {"title": "Whitney Athletic Center", "chip": "Best Higher Education, 2022", "image": "assets/work-whitney.jpg", "href": "services/systems-integration.html",
     "line": "90,000 square feet of athletic, academic and game-day space, with a new press box.", "alt": "The West Stadium stands at the Whitney Athletic Center"},
    {"title": "A national association congress", "chip": "Event Staging", "image": "assets/hero-delegate-assembly.jpg", "href": "services/event-staging.html",
     "line": "General session staging for thousands of delegates.", "alt": "A delegate assembly hall under IMS LED screens"},
    {"title": "On the field, after dark", "chip": "Event Staging", "image": "assets/work-outdoor-event.jpg", "href": "services/event-staging.html",
     "line": "Outdoor event staging in a stadium bowl.", "alt": "Hundreds of dinner tables set on a stadium field"},
]
# Event production: for the event services and the event-led industries, where building projects would be off-topic.
EVENT_WORK = [
    {"title": "Corporate general sessions", "chip": "Event Staging", "image": "assets/event-general-session.jpg", "href": "services/event-staging.html",
     "line": "LED walls, lighting, audio and scenic for the room the whole company watches.", "alt": "A corporate general session staged by IMS"},
    {"title": "University commencements", "chip": "Commencement", "image": "assets/hero-commencement.jpg", "href": "industries/higher-education.html",
     "line": "Arena commencements, with live camera feeds and streaming.", "alt": "A university commencement in an arena, staged by IMS"},
    {"title": "Awards galas", "chip": "Gala", "image": "assets/event-awards-gala.jpg", "href": "services/event-staging.html",
     "line": "Historic venues, lit and staged for the night.", "alt": "An awards gala in a historic hall, staged by IMS"},
    {"title": "Medical and scientific meetings", "chip": "Pharma and medical", "image": "assets/ind-pharma-medical.jpg", "href": "industries/pharmaceutical-medical.html",
     "line": "Symposia and congresses that run to the minute.", "alt": "A medical conference stage set by IMS"},
    {"title": "Outdoor events", "chip": "Outdoor", "image": "assets/work-outdoor-event.jpg", "href": "services/event-staging.html",
     "line": "Stadium fields and open-air venues, after dark.", "alt": "Dinner tables on a stadium field, staged by IMS"},
]
EVENT_SERVICES = {"event-staging", "virtual-events", "streaming-services", "production-content-creation"}
SERVICE_VOICES = {"event-staging": [0, 3, 1], "virtual-events": [2, 3, 0], "streaming-services": [3, 4, 2], "production-content-creation": [2, 4, 0],
                  "systems-integration": [1, 3, 0], "managed-services": [3, 1, 0], "avaas": [1, 3, 2], "digital-signage-video-walls": [2, 1, 3]}
INDUSTRY_VOICES = {"corporate": [2, 3, 1], "higher-education": [4, 1, 2], "pharmaceutical-medical": [0, 3, 2], "associations-nonprofits": [3, 0, 1],
                   "government-politics": [1, 3, 0], "professional-financial": [3, 2, 1]}

AWARDS = [  # badge, title, who and when
    ["assets/awards/integrator-of-the-year-2025.png", "Integrator of the Year, 2025", "NSCA, Commercial Integrator and Security Sales & Integration"],
    ["assets/awards/scn-top50-2025.png", "SCN Top 50 Systems Integrators", "2023, 2024 and 2025"],
    ["assets/awards/ci-2026.png", "Best Meeting Room Project", "Commercial Integrator, 2026"],
    ["assets/awards/ci-2025.png", "Best Large Venue Project", "Commercial Integrator, 2025: Longwood Reimagined"],
    ["assets/awards/ci-2024.png", "Best Meeting Room Project", "Commercial Integrator, 2024: Five Below"],
    ["assets/awards/ci-2023.png", "Best Higher Education Project", "Commercial Integrator, 2023: West Chester University"],
    ["assets/awards/ci-2022.png", "Best Higher Education Project", "Commercial Integrator, 2022: Whitney Athletic Center"],
    ["assets/awards/ci-2021.png", "Best Large Venue Project", "Commercial Integrator, 2021: U.S. Squash"],
]

# Case studies for the five award projects. Facts from Commercial Integrator's award writeups and the imsts.com case-study pages (9 Nov 2026).
CASES = [
    {"slug": "longwood-reimagined", "w": 0, "eyebrow": "Commercial Integrator, Best Large Venue Project, 2025", "heading": "Longwood <em>Reimagined</em>",
     "place": "Longwood Gardens, Kennett Square, Pennsylvania",
     "subhead": "AV for about 30 rooms and spaces across a $250 million transformation of 17 acres, built to disappear into one of the world's great gardens.",
     "metrics": [["Project", "$250M", "Longwood Reimagined, 17 acres"], ["Labor", "4,800+", "hours on site and in the shop"], ["Cable", "100,000+ ft", "installed"], ["Commissioning", "10 to 4", "weeks, compressed"]],
     "quote": "IMS was a true partner on the Longwood Reimagined Project. Their team understood our needs and delivered a seamless AV experience that's intuitive, reliable, and beautifully integrated into our space.",
     "who": "Michael Parisi, VP of IT, Longwood Gardens",
     "challenge": "A multiyear, $250 million project to reimagine 17 acres of a garden that welcomes more than a million guests a year. The AV had to work in demanding environmental conditions, including a glass conservatory, without spoiling a single sightline.",
     "delivered": ["The West Conservatory: 32,000 square feet of glass, with paging and audio tied to the fountains and speakers in an operable ceiling",
                   "The Grove and the Potting Shed: classrooms, studios, executive offices, meeting rooms and workshops",
                   "1906 Dining and Bar: zoned audio with fountain integration; the Fountain Room: custom projector lifts in an arched ceiling",
                   "Outdoor displays and menu boards in the Beer Garden, and an interactive touch display in the Peirce-du Pont House",
                   "Redundant DSP networks and Crestron control, every rack built and tested at IMS, all programming in house"],
     "detail_img": "assets/work-longwood.jpg", "brands": ["Biamp", "Bose Professional", "Cisco", "Crestron", "Extron", "Mersive", "QSC", "Samsung", "Shure", "Sony", "Vaddio", "Yamaha"],
     "team": "With JB&B (engineering), WEISS/MANFREDI and Reed Hilderbrand (design) and Bancroft (general contractor). Commissioned in time for A Longwood Christmas, 2024.",
     "service": "services/systems-integration.html"},
    {"slug": "us-squash", "w": 1, "eyebrow": "Commercial Integrator, Best Large Venue Project, 2021", "heading": "The U.S. Squash national center, <em>live on every court</em>",
     "place": "The 33rd Street Armory, Philadelphia, with Drexel University",
     "subhead": "A 1916 armory reborn as the home of U.S. Squash, with every one of its 20 courts captured and streamed.",
     "metrics": [["Facility", "65,000 sq ft", "inside a 1916 armory"], ["Courts", "20", "captured and streamed"], ["Displays", "40+", "monitors, 43 to 100 inches"], ["Audio", "Up to 110", "speakers in 8 spectator zones"]],
     "challenge": "IMS joined after construction had started. The original technology scope would not deliver a squash-focused live event venue, and the plans had no AV control room and no central server room.",
     "delivered": ["A new third-level section designed for the head end and the control room",
                   "An SDVoE network capturing and streaming all 20 courts, more than 12 hours a day",
                   "A 64 by 64 SDI matrix, with live scoring overlaid on the video and sent to YouTube and a Haivision capture system",
                   "Dante audio on Q-SYS processing, with 68 input channels",
                   "Q-SYS touch panels and iPads, so staff run the building from anywhere in it"],
     "detail_img": "assets/room-us-squash.jpg", "brands": ["AJA", "Audinate", "Chief", "Crestron", "Kramer", "Marshall", "Planar", "Shure", "QSC", "Haivision"],
     "team": "IMS Event Staging has produced the U.S. Open Squash Championships since 2011, so the building was designed by people who know the event.",
     "service": "services/systems-integration.html"},
    {"slug": "five-below-medallion-hall", "w": 2, "eyebrow": "Commercial Integrator, Best Meeting Room Project, 2024", "heading": "Medallion Hall, <em>the most booked room</em> at Five Below",
     "place": "Five Below headquarters, the Lits Brothers Building, Philadelphia",
     "subhead": "A conference theater built to bring people back to the office, that engages every seat and broadcasts to every store.",
     "metrics": [["Projection", "3", "4K laser projectors, 7,000 lumens"], ["Cameras", "5", "PTZ, auto-tracking"], ["Video", "13 in, 8 out", "inputs and outbound routes"], ["Network", "48 ports", "AV over IP, with Dante"]],
     "challenge": "Five Below, with nearly 1,600 stores in 43 states, wanted a room for town halls, training and events, on Microsoft Teams and Zoom. The building's 125-year-old exposed brick and low timber ceilings left almost nowhere to mount anything.",
     "delivered": ["Three 4K laser projectors, three 65-inch confidence monitors and a latecomer display",
                   "Five auto-tracking PTZ cameras for town hall broadcasts",
                   "Two column arrays, nine pendant speakers and four ceiling microphone arrays",
                   "Wireless handheld, head-worn and lavalier microphones, a Teams cart and iPad control",
                   "A control room on a 48-port AV-over-IP network with Dante"],
     "outcome": "Medallion Hall is now the most booked room in the company.",
     "detail_img": "assets/work-five-below.jpg", "brands": [],
     "team": "With IA Architects (architecture and interiors), Bala Consulting Engineers (MEP, low voltage and AV design) and D'Lauro & Rodgers (construction).",
     "service": "services/systems-integration.html"},
    {"slug": "west-chester-learning-stair", "w": 3, "eyebrow": "Commercial Integrator, Best Higher Education Project, 2023", "heading": "The Learning Stair, <em>two stories of LED</em>",
     "place": "Science and Engineering Commons Center, West Chester University",
     "subhead": "A 23 by 24 foot direct-view LED wall for teaching, admissions tours, events, live streaming and recording.",
     "metrics": [["LED panels", "264", "direct view"], ["Wall", "23 x 24 ft", "two stories"], ["Building", "175,000 sq ft", "opened August 2021"], ["Control", "3", "touch panels"]],
     "challenge": "Create an impactful teaching and learning technology experience for faculty and students, at the heart of a new 175,000 square foot science and engineering building.",
     "delivered": ["264 direct-view LED panels, 23 by 24 feet, on NovaStar controllers and an Analog Way processor",
                   "Four wall-mounted column line arrays and ceiling speakers on Biamp processing",
                   "PTZ cameras and streaming encoders, so lectures and events reach beyond the stair",
                   "Wireless presentation, ADA assisted listening and three Crestron touch panels"],
     "detail_img": "assets/hero-video-wall.jpg", "brands": ["Biamp", "Crestron", "Extron", "Listen Technologies", "Matrox", "Mersive", "QSC", "Shure", "Vaddio", "Yamaha"],
     "team": "Project managed for IMS by Jack Dager, CTS.",
     "service": "services/digital-signage-video-walls.html"},
    {"slug": "whitney-athletic-center", "w": 4, "eyebrow": "Commercial Integrator, Best Higher Education Project, 2022", "heading": "The Whitney Athletic Center, <em>ready for ESPN</em>",
     "place": "University of Delaware, Newark",
     "subhead": "90,000 square feet of athletic, academic and game-day space, with a press box built to broadcast standards.",
     "metrics": [["New space", "90,000 sq ft", "athletic, academic and game day"], ["Timeline", "2018 to 2021", "completed November 2021"], ["Standard", "ESPN", "broadcast-ready cabling"], ["Opening", "On time", "for the football season"]],
     "quote": "Despite the slowdowns caused by the pandemic, IMS was still able to complete the entirety of their work in time for the opening of the University of Delaware football season.",
     "who": "Kyle Martin, Manager of Performances and Events, University of Delaware",
     "challenge": "Broadcast infrastructure that would meet or exceed the standards of national media outlets, including ESPN, delivered through pandemic supply-chain delays before the first home game.",
     "delivered": ["Single-mode fiber, CAT6, video and audio cabling from every camera position to the press box and the broadcast truck",
                   "AV for the lobby, offices, medical and treatment rooms, concourses, lounges and conference rooms",
                   "The club and bar, the President's suite, press and media suites and radio rooms",
                   "Dante audio, Clear-Com intercom, laser projection and wireless presentation"],
     "detail_img": "assets/work-whitney.jpg", "brands": ["Audinate", "Barco", "Clear-Com", "Crestron", "Epson", "Listen Technologies", "Panasonic"],
     "team": "With HOK Architects and EDiS Construction.",
     "service": "services/systems-integration.html"},
]
for _c in CASES:
    WORK[_c["w"]]["href"] = f"work/{_c['slug']}.html"


def case_page(c):
    w = WORK[c["w"]]
    others = [dict(x, href=f"work/{o['slug']}.html") for o in CASES if o is not c for x in [WORK[o["w"]]]]
    secs = [{"type": "hero-video", "eyebrow": c["eyebrow"], "heading": c["heading"], "subhead": c["subhead"], "poster": w["image"], "note": c["place"],
             "primary": {"label": "Talk to IMS about your project", "href": "contact.html"}, "secondary": {"label": "All award projects", "href": "why-ims.html#work"}}]
    if c.get("quote"):
        secs.append({"type": "casestudy", "alt": True, "eyebrow": "By the numbers", "heading": w["title"], "quote": c["quote"], "attribution": c["who"], "metrics": c["metrics"]})
    else:
        secs.append({"type": "cards", "alt": True, "eyebrow": "By the numbers", "heading": c.get("outcome") or w["title"], "items": [[f"{v}", f"{k}: {d}"] for k, v, d in c["metrics"]]})
    secs.append({"type": "cards", "eyebrow": "The project", "heading": "What had to be true, and who built it", "items": [["The brief", c["challenge"]], ["The team", c["team"]]]})
    secs.append({"type": "detail", "eyebrow": "What IMS delivered", "heading": "Designed, built, tested and handed over by one team", "body": "Every system below was designed, installed and commissioned by IMS.",
                 "bullets": c["delivered"], "image": c["detail_img"], "image_alt": w["alt"], "image_w": 1600, "image_h": 900, "flip": True, "list_with_text": True})
    if c["brands"]:
        secs.append({"type": "partners", "caption": "Technology in the project", "items": c["brands"]})
    _name = w["title"].split(",")[0]
    _faq = [[f"Who did the AV for {_name}?", f"IMS Technology Services designed, installed and commissioned the audiovisual systems at {c['place']}."],
            [f"What award did {_name} win?", f"{c['eyebrow'].replace('Commercial Integrator, ', 'Commercial Integrator Integration Awards: ')}."],
            ["What did IMS deliver?", c["delivered"][0] + "."]]
    if c["brands"]:
        _faq.append(["What technology is in the project?", "Systems from " + ", ".join(c["brands"][:-1]) + " and " + c["brands"][-1] + ", among others."])
    _faq.append(["Can IMS do a project like this for us?", "Yes. Systems Integration designs and builds it, Managed Services keeps it running, and Event Staging can run the events in it. Call 610-361-1870 or use the form below."])
    secs.append({"type": "faq", "heading": f"Questions about {_name}", "items": _faq})
    secs.append({"type": "work", "id": "work", "eyebrow": "More of the work", "heading": "Four more award projects, and the events", "intro": "Integrated, managed and staged by IMS.", "items": others + [WORK[5]]})
    secs.append(LEADFORM)
    return {"file": f"work/{c['slug']}.html", "title": f"{w['title']}: Case Study | {CLIENT}", "description": desc(f"{c['eyebrow']}. {c['subhead']}"),
            "crumbs": [["Home", "index.html"], ["Why IMS", "why-ims.html"], [w["title"].split(",")[0], f"work/{c['slug']}.html"]], "sections": secs}


# slug, nav label, short, one-line, image, eyebrow, heading (<em> allowed), subhead, benefits [[t,b]], included [..], faq [[q,a]]
SERVICES = [
    ["systems-integration", "Systems Integration", "systems integration",
     "Design and installation of presentation, collaboration and unified communication technology, under one contract.",
     "assets/svc-systems-integration.jpg", "Systems Integration",
     "Rooms that look and sound <em>the way the meeting needs</em>.",
     "IMS designs, engineers and installs video, audio, control, display and collaboration systems, from the huddle room to the national center, with one accountable team from the first drawing to the handover.",
     [["Design and consulting", "Design that fits the plans for new construction or the refurbishment of an existing space, so the technology and the building are planned together."],
      ["Integration and installation", "Project managers and engineers work with your architect, general contractor and facilities team toward on-time delivery."],
      ["Unified communications, any platform", "Teams, Zoom, Webex or all three. A platform-agnostic approach for meetings inside and outside the company."],
      ["A certified field team", "Technicians certified in Crestron, Extron, Biamp, Polycom, Cisco, Haivision, Planar and more."]],
     ["Video conferencing, web conferencing and unified communication", "Control systems, display systems and video walls",
      "Streaming and video over IP, wireless collaboration, distance learning and interactive displays", "Paging, sound masking and structured cabling",
      "Remote system management, capture systems and content management", "Digital signage and content creation"],
     [["What does design-build mean at IMS?", "Design and implementation under one contract, with a single point of accountability. The team that designs the room is the team that answers for it."],
      ["Do you work with architects and general contractors?", "Yes. Our project managers and engineers work hand in hand with architects, general contractors and facilities management on new construction and renovations."],
      ["Which spaces do you integrate?", "Boardrooms, conference centers, huddle and training rooms, multipurpose and divisible rooms, control and command centers, stadiums and event venues, amenity centers, lobbies and classrooms."],
      ["Who keeps the system running after install?", "IMS Managed Services monitors and supports what we build, and AV as a Service bundles the technology and its support into one monthly cost."]]],
    ["managed-services", "Managed Services", "managed services",
     "A managed model that monitors, supports, reports on and refreshes AV, with one accountable owner.",
     "assets/svc-ms-lobby.jpg", "Managed Services",
     "We do not install AV and leave. <em>We run it.</em>",
     "A proactive managed services model that keeps every room ready before it is needed, and accountable to leadership long after install day. IMS monitors, detects, resolves, reports, recommends and refreshes.",
     [["Service and support", "24/7/365 monitoring, with tiers that match coverage to what is mission-critical."],
      ["Reporting with 4Sight", "Our monitoring platform turns AV into usage data, health analytics and trend reports leadership can act on."],
      ["Staff augmentation", "Specialists onsite or remote, embedded or event-based, with defined scope, escalation and IMS oversight."],
      ["AV as a Service", "Hardware, installation, support, monitoring and refresh bundled into one operating cost."]],
     ["Design services and production services", "Support and maintenance, critical meeting support and remote monitoring", "Consulting and staffing solutions",
      "Digital signage", "4Sight with Automatic Issue (AI) Resolution", "CapEx, hybrid AVaaS, full AV as a Service or embedded staff"],
     [["What does a managed AV program include?", "Design and production services, support and maintenance, consulting, critical meeting support, staffing, remote monitoring and digital signage."],
      ["Is it only for large enterprises?", "No. A five-room office gets the same operating discipline as a 500-room enterprise, scoped to its budget."],
      ["What is 4Sight?", "Our proprietary monitoring platform. With Automatic Issue (AI) Resolution it pairs automated detection with an IMS service team."],
      ["Can you manage rooms another integrator installed?", "Talk to us about your estate. The scope of every agreement is written down before it starts."]]],
    ["event-staging", "Event Staging", "event staging",
     "Staging, audio visual and creative services for meetings and events of every size, with a dedicated production manager.",
     "assets/svc-event-staging.jpg", "Event Staging",
     "Events that look and sound <em>like your organization</em>.",
     "A full range of staging, audio visual and creative services for live, virtual and hybrid events, delivered by certified technicians and experienced production managers, from a training seminar to a national congress.",
     [["Audio", "From small training seminars to large-venue productions, clear sound that carries the message to the back row."],
      ["Video", "Presentation, projection, playback, mapping, blends and live recording on state-of-the-art equipment."],
      ["Lighting", "From speaker illumination to orchestrated light shows that shape the set and the mood."],
      ["Scenic design", "Hard sets, podiums, stage drape and sectional staging, designed for your venue and your brand."]],
     ["A dedicated production manager and account representative for every customer", "Audio, video, lighting and scenic design in one team",
      "Production and content creation, LED walls and digital signage", "IMS Concierge Services: content management, second screen technology and gamification",
      "Streaming services: overflow sessions, webcasting and video conferencing", "Exhibit services, and the IMS Scenic and Design Portal"],
     [["What kinds of events do you stage?", "Product launches, corporate events, inaugurations, annual meetings, commencements, symposiums, galas and training meetings, live and virtual."],
      ["Who will we work with?", "A dedicated production manager and account representative who own planning, execution and fulfillment."],
      ["Do you stage in venues across Philadelphia?", "Yes. IMS is the leading audiovisual rental and event staging company in the Philadelphia metro area and works in the major Mid-Atlantic venues."],
      ["What is the Scenic and Design Portal?", "A library of set designs with customization options to fit a venue and a budget. Ask your account representative for access."]]],
    ["avaas", "AV as a Service", "AV as a Service",
     "A subscription that bundles AV technology, support, monitoring and planned upgrades into one monthly cost.",
     "assets/svc-avaas.jpg", "AV as a Service (AVaaS)",
     "Technology as an operating cost, <em>not a capital event</em>.",
     "AVaaS ends the break-fix-replace cycle. Equipment, support and planned upgrades move from the capital budget to one predictable monthly cost, so the rooms stay current for the whole term.",
     [["Predictability", "Equipment, infrastructure and support as a monthly operating expense, with scheduled upgrades."],
      ["Innovation", "Your AV and IT people move from maintenance to client-facing, revenue-generating work."],
      ["Flexibility", "Invest in the systems that fit the business, not what this year's capital budget allows."],
      ["Reliability", "24/7 monitoring and management that catches most issues before they become downtime."],
      ["Informed decisions", "Data and reporting for fact-based decisions about the next technology."],
      ["Consistency", "Consistent expense, budgeting, technology and user experience, room to room."]],
     ["The right AV solution, with the Solution Replacement Guarantee (SRG)", "Technology support and maintenance for the entire term", "Natural disaster and Act of God protection",
      "All AV and IT technology for one monthly cost", "Planned upgrades, so you never own obsolete technology"],
     [["Who is AVaaS for?", "Organization leaders, financial decision makers, IT managers and the people who use the rooms every day."],
      ["What is the Solution Replacement Guarantee?", "A feature of the IMS AVaaS model that keeps your solution current through the term. Your account manager will walk you through the terms."],
      ["What does the monthly payment include?", "The current AV solution and future replacement solutions, with all warranties, support and services."]]],
    ["digital-signage-video-walls", "Digital Signage and Video Walls", "digital signage",
     "Video walls and digital signage designed from a needs analysis, installed, trained and kept fresh.",
     "assets/svc-digital-signage.jpg", "Digital Signage and Video Walls",
     "Messaging that <em>stops people where they stand</em>.",
     "From a 3x3 lobby wall to a two-story direct-view LED installation, IMS designs the hardware and the software, installs it, trains your team and keeps the content fresh.",
     [["A needs analysis first", "Every project starts with an in-depth analysis of what the displays have to do."],
      ["Hardware and software, designed together", "Leading sign manufacturers, the drive systems that create the content and the networks that run them."],
      ["Training for your team", "On-site or web-based, after installation."],
      ["Content that stays fresh", "A content plan with monthly and quarterly updates keeps every screen worth looking at."]],
     ["Lobby, cafe, collaboration-space and interactive video walls", "Large direct-view LED installations", "Portable units and permanent fixtures",
      "Corporate and event digital signage", "Widgets and APIs that deliver fresh content without manual work"],
     [["How big can you build?", "From a 3x3 lobby wall to the 23.94 by 24.69 foot direct-view LED wall at West Chester University's Learning Stair, which won Commercial Integrator's Best Higher Education Project in 2023."],
      ["Do you create the content?", "Yes. Our content design team develops the messaging and can run the content plan for you."],
      ["Indoor and outdoor?", "Both: indoor and outdoor displays, video walls, single screens and interactive panels."]]],
    ["virtual-events", "Virtual and Hybrid Events", "virtual events",
     "Produced virtual and hybrid events with a hosted platform, a branded environment and the team that runs your live events.",
     "assets/svc-virtual-events.jpg", "Virtual and Hybrid Events",
     "A broadcast-quality event, <em>wherever your audience is</em>.",
     "Fully produced virtual and hybrid events with secure streaming, technical direction and speaker support, branded environments and post-event editing, from the same team that stages your live events.",
     [["One link, no downloads", "A hosted platform with a single URL, landing pages and an agenda view. No apps or plugins."],
      ["Audience engagement", "Chat, polling, Q&A, whiteboarding and virtual trade show experiences."],
      ["Security and privacy", "Open or secured with flexible login. Registration data is deleted after the event, and attendee data is never shared or sold."],
      ["Content and branding", "The IMS Content Concierge manages event content, and our in-house video and design teams brand the whole environment."]],
     ["Secure, reliable streaming platforms", "Technical direction and speaker support", "Custom creative design and branded virtual environments",
      "Integration with in-person and hybrid programs", "Post-event editing for on-demand or packaged content", "A broadcast studio for recording or streaming a message"],
     [["When does a virtual event make sense?", "When funding is uncertain, attendees abroad cannot travel, in-person registration is lower than expected, or corporate travel is restricted."],
      ["Do you run hybrid events?", "Yes. We add a virtual extension to an in-person conference, or stream a town hall to other sites and to employees' devices."],
      ["What happens to attendee data?", "Registration data creates the logins, and accounts and registration data are deleted after the event."]]],
    ["streaming-services", "Streaming Services", "streaming",
     "Overflow session streaming, webcasting and video conferencing, for live and virtual attendees.",
     "assets/svc-streaming.jpg", "Streaming Services",
     "Reach the people <em>outside the room</em>.",
     "Overflow streaming, webcasting and two-way video conferencing, planned around your goals and your audience and delivered by an experienced crew.",
     [["Overflow sessions", "When a session room is full, we broadcast it into overflow rooms so no attendee is left out."],
      ["Webcasting", "HD video from one source to many viewers over an international content delivery network, with branded registration and flexible security."],
      ["Video conferencing", "Two-way HD video between locations, built into existing infrastructure or as point-to-point connections."]],
     ["Planning around your goals, audience and vision", "Custom registration workflow and page branding", "Hosting, delivery to your platform or to your social channels",
      "Integration with existing video conference infrastructure"],
     [["Which option fits my event?", "Overflow streaming when a room reaches capacity, webcasting to show video to remote attendees, video conferencing for two-way HD video between locations."],
      ["Can you stream to our own platform?", "Yes. We can host the event, stream to your platform or deliver to your social channels."],
      ["Can streaming be added to a permanent room?", "Yes. Event Staging, Systems Integration and Managed Services work together on hybrid meeting rooms."]]],
    ["production-content-creation", "Production and Content Creation", "content creation",
     "Video, animation, projection mapping and 360 photospheres, from show openers to documentaries.",
     "assets/svc-content-creation.jpg", "Production and Content Creation",
     "Content bound only by <em>your imagination</em>.",
     "Show openers, walk-up stingers, wrap-up videos, scripted documentaries and animated projection, developed, designed and delivered by the team that puts them on the screen.",
     [["Event content", "Show openers, walk-up stingers and promotional videos for galas, national sales meetings and town halls."],
      ["Projection mapping", "Content and projection for indoor and outdoor venues, using the architecture and custom scenic elements."],
      ["360 degree photospheres", "Interactive tours for real estate, galleries, laboratories, restaurants and more."],
      ["Event post-production", "Multi-angle recording, then raw footage or trimmed, segmented files for playback and distribution."]],
     ["Logo animations to full-length documentaries", "Video shoots, editing and animation", "Professional voiceover talent",
      "Digital scenic and event promotional videos", "Branded virtual meeting elements such as lower thirds"],
     [["What kinds of content do you make?", "Logo animations, scripted documentaries, show openers, walk-up stingers, wrap-up and highlight videos, animated projection and 360 photospheres."],
      ["Can you record our event?", "Yes. Working with Event Staging, the team records the proceedings from multiple angles."],
      ["Do you work with outside talent?", "Yes, professional voiceover talent on scripted projects."]]],
]

SERVICE_DETAIL_IMG = {"systems-integration": "assets/room-us-squash.jpg", "managed-services": "assets/svc-managed-services.jpg", "event-staging": "assets/event-awards-gala.jpg",
                      "avaas": "assets/room-conference.jpg", "digital-signage-video-walls": "assets/detail-signage.jpg", "virtual-events": "assets/detail-virtual.jpg",
                      "streaming-services": "assets/event-show-control.jpg", "production-content-creation": "assets/detail-content.jpg"}

# slug, name, image, one-line, body, bullets, faq
INDUSTRIES = [
    ["corporate", "Corporate", "assets/ind-corporate.jpg", "Annual meetings, product launches and town halls that put the company on stage at its best.",
     "IMS plans, produces and delivers annual meetings, product launches and tradeshows for companies from small businesses to the Fortune 500. Because Event Staging, Systems Integration and Managed Services are one company, we can build on a fixed installation too: a town hall in the main cafeteria, broadcast to every region.",
     ["Annual meetings, product launches and tradeshows", "Hybrid meetings supported at every site nationally", "Sets, lighting, video and audio at the host site", "Streaming to other locations and to employees' devices"],
     [["Can you support a national rollout?", "Yes, from a single local event to a coordinated national rollout."],
      ["Can you stream a town hall to other sites?", "Yes. Hybrid meetings that stream from the host site to other locations or to employees' computers, phones and tablets are a specialty."]]],
    ["higher-education", "Higher education", "assets/ind-higher-education.jpg", "Commencements, convocations and campus AV that carry the institution's mission and culture.",
     "IMS supports commencements and graduations, convocations, conferences, galas, capital campaigns, alumni meetings and athletic events, and builds the permanent systems behind them. Our campus work won Commercial Integrator's Best Higher Education Project in 2022, for the Whitney Athletic Center, and in 2023, for West Chester University's Learning Stair video wall.",
     ["Commencements, convocations and web streaming", "Outdoor sound systems and live camera feeds", "Digital event recording and commencement video", "Video walls and athletic center AV design and integration"],
     [["Do you produce commencement video?", "Yes. Drexel University called its commencement video celebration truly phenomenal."],
      ["Can you build permanent campus systems?", "Yes. Systems Integration designs and installs classrooms, video walls and athletic center AV, and Managed Services keeps them running."]]],
    ["pharmaceutical-medical", "Pharmaceutical and medical", "assets/ind-pharma-medical.jpg", "Meetings that demand confidentiality, an understanding of compliance and national consistency.",
     "IMS supports POA meetings, product launches, investigator meetings, training meetings, symposia, national sales meetings and continuing medical education. We provide the confidentiality these events require, understand the role compliance plays, and offer consistent equipment and labor pricing across the country.",
     ["Investigator meetings, symposia and national sales meetings", "Audience response systems and video switching", "Digital event recording and live camera feeds", "Consistent equipment and labor pricing nationwide"],
     [["Do you understand compliance requirements?", "Yes. We understand the role compliance plays in pharmaceutical and medical education events and provide the confidentiality they require."],
      ["Can you staff meetings in several cities?", "Yes, with consistent equipment and labor pricing across the country."]]],
    ["associations-nonprofits", "Associations and nonprofits", "assets/ind-associations.jpg", "Board meetings, congresses and membership meetings, planned toward the mission and the budget.",
     "IMS works with associations and nonprofits from board meetings to educational events and national congresses, and takes part in strategic planning to support the event experience. We use technology and decor to grow attendance and drive sponsorship, and we know how to work within an association budget.",
     ["Board meetings, educational events and membership meetings", "Delegate assemblies and national congresses", "Technology and decor that support attendance and sponsorship", "Exhibit services and exhibitor management"],
     [["Do you work with national associations?", "Yes. National association congresses and delegate assemblies are part of our event staging work."],
      ["Can you handle the exhibit hall?", "Yes: LED, lighting, audio and monitors, with exhibitor management and online ordering."]]],
    ["government-politics", "Government and politics", "assets/ind-government.jpg", "Press conferences, plenary sessions and campaign events, on a non-partisan basis.",
     "IMS has supported events involving Presidents and Vice Presidents, and works with both political parties and all branches of state and federal government. Set design, lighting, video projection, sound reinforcement and teleprompters support press conferences, campaigns, plenary sessions and fundraisers of any size.",
     ["Press conferences, plenary sessions and fundraisers", "Teleprompters, video recording and projection", "Set design and lighting for any number of attendees", "Non-partisan, with both political parties"],
     [["Do you work across party lines?", "Yes, with both political parties and all branches of state and federal government."],
      ["Can you support a press conference on short notice?", "Call 610-361-1870 and we will tell you honestly what we can staff and when."]]],
    ["professional-financial", "Professional and financial services", "assets/ind-professional-financial.jpg", "Annual, investor and client meetings for firms where confidentiality is the point.",
     "IMS supports accounting, finance, legal and consulting firms with service shaped by compliance, confidentiality and strict adherence to non-disclosure. Events include sales meetings, state of the company, investor and due diligence meetings and community events, with webcasting and conferencing that reach any audience.",
     ["Annual, sales and investor meetings", "Webcasting and audio visual conferencing", "Lighting and scenic design for the main stage", "Conference rooms and boardrooms integrated by the same company"],
     [["Do you sign non-disclosure agreements?", "Yes. We adhere strictly to non-disclosure requirements for professional services firms."],
      ["Can you build our conference rooms too?", "Yes. Systems Integration designs and installs boardrooms and conference rooms, and Managed Services keeps them running."]]],
]

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


def _flow(fid, eyebrow, heading, intro, steps, receive_label="What you receive", alt=True):
    return {"type": "flow", "id": fid, "alt": alt, "eyebrow": eyebrow, "heading": heading, "intro": intro, "receive_label": receive_label,
            "steps": [{"label": a, "when": b, "summary": c, "title": d, "body": e, "receive": f} for a, b, c, d, e, f in steps]}


def _ba(bid, heading, b_title, b_body, b_items, a_title, a_body, a_items, b_eyebrow="Without IMS", a_eyebrow="With IMS"):
    return {"type": "beforeafter", "id": bid, "eyebrow": "Before and after", "heading": heading,
            "before": {"eyebrow": b_eyebrow, "title": b_title, "body": b_body, "items": b_items},
            "after": {"eyebrow": a_eyebrow, "title": a_title, "body": a_body, "items": a_items}}


VOICES = [t[:3] for t in TESTIMONIALS]
LEADFORM = {"type": "leadform", "alt": True, "id": "start", "heading": "Tell us about the room, the event or the program",
            "body": "One form reaches all three business units. Say what you are planning and the right IMS team member will call you.",
            "submit": "Talk to IMS", "note": "A person replies, not an autoresponder."}

BA_MANAGED = _ba("ba", "Reactive AV, or AV that is managed",
                 "Reactive AV", "Most AV programs are built to succeed on day one, not day one thousand.",
                 ["You find out a room is down when someone walks in to use it", "Every fix starts with a ticket and a wait", "Refresh planning happens after something breaks", "Reporting is a status update, not a record"],
                 "Managed by IMS", "A closed loop: monitor, detect, resolve, report, recommend and refresh.",
                 ["Rooms are monitored continuously, before anyone walks in", "Most issues are caught and resolved before a meeting starts", "Lifecycle and budget planning are built into the model", "Reporting is data leadership can use to decide"],
                 b_eyebrow="Reactive AV", a_eyebrow="Managed by IMS")
BA_VENDORS = _ba("ba-one", "Three vendors, or one IMS",
                 "Three vendors", "An integrator for the rooms, a help desk for the problems, a rental house for the events.",
                 ["Three contracts, three account teams, three invoices", "The event crew has never seen the room it is working in", "Nobody owns the room after the install crew leaves", "Every handoff is a place for something to go wrong"],
                 "One IMS", "Systems Integration, Managed Services and Event Staging, one company and one set of account teams.",
                 ["One contract and a single point of accountability", "The team that built the room supports the event in it", "Rooms watched 24/7/365 by the people who installed them", "One account manager who knows the whole picture"],
                 b_eyebrow="Without IMS", a_eyebrow="With IMS")
FLOW_SI = _flow("flow", "How a project runs", "From the first drawing to a system your team can run",
                "Click a stage. One contract and one accountable team, from design to support.",
                [["Design", "Stage 1", "Goals first, then the design.", "Design and consulting", "Design that fits the plans for new construction or the refurbishment of an existing space, so the technology and the building are planned together.", ["A design matched to your goals", "Coordination with your architect and contractors"]],
                 ["Engineer", "Stage 2", "Drawings, systems, schedule.", "Engineering", "A system engineer documents the design and the project manager sets the schedule with your general contractor and facilities team.", ["System documentation", "A schedule tied to the building's"]],
                 ["Install", "Stage 3", "Built by certified technicians.", "Integration and installation", "Certified field technicians install, program and commission every system, toward on-time delivery.", ["A commissioned, tested system", "As-built documentation"]],
                 ["Train", "Stage 4", "Your people learn it.", "Training and handover", "Your team learns the rooms before the first important meeting in them.", ["Hands-on training", "A clear handover"]],
                 ["Run", "Stage 5", "Managed Services keeps it ready.", "Managed Services", "IMS Managed Services monitors the rooms 24/7/365 and keeps them ready, with 4Sight reporting for leadership.", ["Monitoring and support", "Usage and health reporting"]]])
FLOW_HOME = _flow("flow", "One IMS", "From the room, to the run, to the event",
                  "Click a stage. Systems Integration, Managed Services and Event Staging share customers, so each stage hands over to the same company.",
                  [["Design", "Systems Integration", "Goals first, then the design.", "Design and consulting", "Whether the project is a new facility, a refurbished space or an event, IMS starts from your goals and designs the technology, the set and the content together.", ["A design matched to your goals", "A single point of accountability"]],
                   ["Build", "Systems Integration", "Installed by the same company.", "Integration and installation", "Certified technicians install and commission the systems, working with your architect, general contractor and facilities team.", ["A commissioned system", "Training for your team"]],
                   ["Run", "Managed Services", "Rooms watched 24/7/365.", "Managed Services", "IMS monitors, detects, resolves, reports, recommends and refreshes, so the rooms are ready before anyone walks in.", ["Monitoring and support", "4Sight reporting for leadership"]],
                   ["Stage", "Event Staging", "The show, in a room we know.", "Event Staging", "When the town hall, the launch or the annual meeting comes, the event crew works in a room IMS built and monitors.", ["A dedicated production manager", "Audio, video, lighting and scenic in one team"]]],
                  alt=False)
SERVICE_MODULES = {
    "systems-integration": [FLOW_SI],
    "managed-services": [BA_MANAGED],
    "avaas": [{"type": "capex-calc", "id": "capex", "eyebrow": "Buy it, or subscribe to it", "heading": "What AV as a Service changes in your budget",
               "intro": "Rooms, what each costs to equip and install, and how much of your team's time they take today. Move the sliders.",
               "rooms": 12, "per_room": 35000, "hours": 2, "cta_label": "Get the real number for your rooms", "cta_href": "contact.html"},
              BA_MANAGED],
    "event-staging": [_flow("flow", "How an event runs", "From the first call to the last case loaded out",
                            "Click a stage. One production manager owns it from start to finish.",
                            [["Plan", "Stage 1", "Goals, venue, audience.", "Planning", "Your production manager and account representative start with the goals, the venue and the audience, then design the show around them.", ["A production plan", "A budget you can approve"]],
                             ["Design", "Stage 2", "Set, light, sound, content.", "Design", "Scenic, lighting, audio and video designed together, with content from our in-house team if you need it.", ["Renderings and a show design", "Content in production"]],
                             ["Show", "Stage 3", "Certified crew, on site.", "Execution", "Certified technicians install, rehearse and run the show, with streaming and recording when the audience is bigger than the room.", ["A rehearsed show", "Streaming and recording as needed"]],
                             ["After", "Stage 4", "Content that keeps working.", "Fulfillment", "Load-out, then edited, segmented recordings for playback and distribution.", ["Edited recordings", "A debrief for next time"]]])],
}


def service_page(slug, navlabel, short, one, image, eyebrow, heading, subhead, benefits, included, faq):
    secs = [
        {"type": "hero", "layout": "split", "eyebrow": eyebrow, "heading": heading, "subhead": subhead,
         "primary": {"label": "Talk to IMS", "href": "contact.html"}, "secondary": {"label": "All services", "href": "services.html"},
         "image": image, "image_alt": f"{navlabel} by IMS", "image_w": 1600, "image_h": 1000},
        {"type": "cards", "alt": True, "eyebrow": "What you get", "heading": f"What {short} means at IMS", "items": benefits},
    ]
    secs += SERVICE_MODULES.get(slug, [])
    secs.append({"type": "detail", "eyebrow": "What is included", "heading": "Everything in scope, written down before work starts",
                 "body": f"IMS {short}, line by line. The scope of every engagement is agreed in writing before we begin.", "bullets": included, "image": SERVICE_DETAIL_IMG.get(slug, image), "image_alt": f"{navlabel}, IMS project photography", "flip": True, "list_with_text": True})
    if slug in EVENT_SERVICES:
        secs.append({"type": "work", "id": "work", "eyebrow": "The work", "heading": "Staged by IMS", "intro": "Every photograph here is an IMS production.", "items": EVENT_WORK})
    else:
        secs.append({"type": "work", "id": "work", "eyebrow": "The work", "heading": "Award-winning, and on the record",
                     "intro": "Projects that won Commercial Integrator's Integration Awards, integrated by IMS.", "items": WORK[:5]})
    secs.append({"type": "testimonials", "alt": True, "heading": "What customers say", "items": [VOICES[i] for i in SERVICE_VOICES.get(slug, [0, 1, 2])]})
    secs.append({"type": "faq", "heading": f"Questions about {navlabel.lower() if slug != 'avaas' else 'AV as a Service'}", "items": faq})
    secs.append(LEADFORM)
    city_title = {"systems-integration": "AV Systems Integration, Philadelphia", "event-staging": "Event Staging and AV Production, Philadelphia",
                  "managed-services": "Managed AV Services", "digital-signage-video-walls": "Digital Signage and LED Video Walls"}.get(slug, navlabel)
    return {"file": f"services/{slug}.html", "title": f"{city_title} | {CLIENT}", "description": desc(f"{one} {subhead}"),
            "crumbs": [["Home", "index.html"], ["Services", "services.html"], [navlabel, f"services/{slug}.html"]], "sections": secs}


def industry_page(slug, name, image, one, body, bullets, faq):
    rel = [s for s in SERVICES if s[0] in ("event-staging", "systems-integration", "virtual-events", "managed-services")]
    return {"file": f"industries/{slug}.html", "title": f"AV and Event Staging for {name} | {CLIENT}",
            "description": desc(f"{one} Event staging, AV integration and managed services from IMS, Garnet Valley, PA, with offices nationwide."),
            "crumbs": [["Home", "index.html"], ["Industries", "industries.html"], [name, f"industries/{slug}.html"]],
            "sections": [
                {"type": "hero", "layout": "split", "eyebrow": f"Industries: {name}", "heading": f"AV and events for <em>{name.lower()}</em>.", "subhead": one,
                 "primary": {"label": "Talk to IMS", "href": "contact.html"}, "secondary": {"label": "All industries", "href": "industries.html"},
                 "image": image, "image_alt": f"An IMS event for {name.lower()}", "image_w": 1600, "image_h": 1000},
                {"type": "detail", "alt": True, "eyebrow": "What we do here", "heading": f"How IMS works with {name.lower()}", "body": body, "bullets": bullets, "image": image, "image_alt": name, "list_with_text": True},
                {"type": "services", "heading": "The services that matter most here", "intro": "Each has its own page.", "items": [[s[1], s[3], f"services/{s[0]}.html"] for s in rel]},
                ({"type": "work", "id": "work", "eyebrow": "The work", "heading": "On campus, on the record", "intro": "Two Commercial Integrator awards for higher education, and the events behind them.", "items": [WORK[3], WORK[4], EVENT_WORK[1], WORK[1], EVENT_WORK[2]]}
                 if slug == "higher-education" else
                 {"type": "work", "id": "work", "eyebrow": "The work", "heading": "Staged by IMS", "intro": "Every photograph here is an IMS production.", "items": EVENT_WORK}),
                {"type": "testimonials", "alt": True, "heading": "What customers say", "items": [VOICES[i] for i in INDUSTRY_VOICES.get(slug, [0, 1, 2])]},
                {"type": "faq", "heading": f"Questions from {name.lower()}", "items": faq},
                LEADFORM,
            ]}


def location_page(slug, city, a1, a2, phone, phone_href, label, lon, lat, st):
    hq = slug == "garnet-valley"
    eyebrow = "Headquarters" if hq else f"{city}, {label}"
    image = "assets/team-integrator-of-year.jpg" if hq else {"linwood": "assets/event-general-session.jpg", "orlando": "assets/event-awards-gala.jpg",
                                                              "plano": "assets/room-conference.jpg", "westlake-village": "assets/svc-virtual-events.jpg"}[slug]
    area = "Greater Philadelphia, the northeast and customers nationally" if slug in ("garnet-valley", "linwood") else {"orlando": "the southeast", "plano": "the middle of the country", "westlake-village": "the west coast"}[slug]
    return {"file": f"locations/{slug}.html", "title": f"AV Integration and Event Staging in {city}, {st} | {CLIENT}",
            "description": desc(f"IMS Technology Services in {city}, {st}: AV systems integration, managed services and event staging for {area}. {a1}, {a2}. Call {phone}."),
            "crumbs": [["Home", "index.html"], ["Locations", "locations.html"], [city, f"locations/{slug}.html"]],
            "schema": [{"@context": "https://schema.org", "@type": "LocalBusiness", "@id": f"{SITE}/locations/{slug}#office", "name": f"IMS Technology Services {city}",
                        "parentOrganization": {"@id": f"{SITE}/#organization"}, "telephone": "+1-610-361-1870", "url": f"{SITE}/locations/{slug}",
                        "address": {"@type": "PostalAddress", "streetAddress": a1, "addressLocality": city, "addressRegion": st, "postalCode": a2.split()[-1], "addressCountry": "US"},
                        "geo": {"@type": "GeoCoordinates", "latitude": lat, "longitude": lon}}],
            "sections": [
                {"type": "hero", "layout": "split", "eyebrow": eyebrow, "heading": f"AV, events and managed services, <em>{'from ' + city if hq else 'in ' + city}</em>.",
                 "subhead": (f"The IMS headquarters serves {area}. Systems Integration, Managed Services and Event Staging are one company, reached on one number: {phone}." if hq else
                             f"The IMS {city} office serves {area}, with the full company behind it. One number reaches all five offices: {phone}."),
                 "primary": {"label": f"Call {phone}", "href": phone_href}, "secondary": {"label": "Talk to IMS", "href": "contact.html"},
                 "image": image, "image_alt": "The IMS team" if hq else f"IMS work, {city}", "image_w": 1600, "image_h": 900},
                {"type": "cards", "alt": True, "eyebrow": f"From {city}", "heading": f"What IMS does from {city}", "items": [
                    ["Systems Integration", "Design, installation and integration of video, audio, control and collaboration systems."],
                    ["Managed Services", "Monitoring, support, 4Sight reporting and staff augmentation for installed rooms."],
                    ["Event Staging", "Audio, video, lighting, scenic and content for meetings and events of every size."]]},
                {"type": "locations", "heading": f"Visit or call {city}", "intro": f"{a1}, {a2}. {phone}.", "items": [[f"{city} ({label})", a1, a2, phone, phone_href]]},
                {"type": "work", "id": "work", "eyebrow": "The work", "heading": "Award-winning, and on the record", "intro": "Five Commercial Integrator awards since 2021.", "items": WORK[:5]},
                {"type": "faq", "heading": f"Questions we get in {city}", "items": [
                    [f"What does IMS do from {city}?", f"All three business units serve {area} from {city}, with the whole company behind the office."],
                    ["Do you work nationally?", "Yes. IMS is headquartered in Garnet Valley, Pennsylvania, with offices in Linwood, Orlando, Plano and Westlake Village, and supports customers across the country."],
                    ["What is the best number to call?", f"{phone} reaches IMS from anywhere."]]},
                LEADFORM,
            ]}


WHEEL_ITEMS = [[s[1], brief(s[3], 140), f"services/{s[0]}.html", s[1]] for s in SERVICES]
HERO_SLIDES = ["assets/hero-general-session.jpg", "assets/hero-us-squash.jpg", "assets/hero-video-wall.jpg", "assets/hero-delegate-assembly.jpg", "assets/hero-commencement.jpg"]
HERO_CAPTIONS = ["Corporate general session, staged by IMS", "U.S. Squash national center, Philadelphia", "Direct-view LED video wall, integrated by IMS",
                 "National association congress, staged by IMS", "University commencement, staged by IMS"]
HERO_STATS = [["1994", "Founded"], ["2025", "Integrator of the Year"], ["8x", "Inc. 5000"], ["5", "Offices, four states"]]

HERO_LAYERED = {"type": "hero-layered", "id": "hero", "eyebrow": "Systems Integration. Managed Services. Event Staging.",
                "heading": "The room. The run. <em>The show.</em>",
                "subhead": "Our success is defined by our clients' ability to look and sound their very best. IMS designs the room, keeps it running and stages the event, as one award-winning company.",
                "primary": {"label": "Talk to IMS", "href": "contact.html"}, "secondary": {"label": "See the work", "href": "#work"},
                "slides": HERO_SLIDES, "captions": HERO_CAPTIONS, "image_w": 1920, "image_h": 1080, "network": False,
                "stats": HERO_STATS,
                "card_a": {"eyebrow": "Start here", "title": "Planning a room or an event?", "body": "One form reaches all three business units, and a person calls you back.",
                           "items": ["Systems Integration", "Managed Services", "Event Staging"], "href": "contact.html", "label": "Talk to IMS"}}
HISTORY = {"type": "timeline", "id": "story", "eyebrow": "Since 1994", "heading": "From IMS, Inc. to One IMS",
           "intro": "Founded by Jill and John Renninger, and growing and profitable every year since.",
           "items": [["1994", "Founded as IMS, Inc.", "Jill and John Renninger start the company in the Philadelphia area. It has grown and been profitable every year since.", "assets/event-show-control.jpg"],
                     ["2012", "The first of eight Inc. 5000 listings", "Among America's fastest growing private companies: 2012 to 2017, 2019 and 2024.", "assets/event-general-session.jpg"],
                     ["2021", "Best Large Venue: U.S. Squash", "The first Commercial Integrator award of the current run. Awards follow in 2022, 2023, 2024, 2025 and 2026.", "assets/work-us-squash.jpg"],
                     ["2025", "Integrator of the Year", "Named by NSCA, Commercial Integrator and Security Sales & Integration, and an SCN Top 50 Systems Integrator for the third year running.", "assets/team-integrator-of-year.jpg"],
                     ["2026", "ISO/IEC 27001:2022, and One IMS", "Information security compliance in June, and three business units brought together as one company, one CRM and one set of account teams.", "assets/svc-managed-services.jpg"]]}
MAP = {"type": "map", "id": "map", "heading": "Five offices, one number, support nationwide",
       "intro": f"Headquartered in Garnet Valley, Pennsylvania, with Event Staging in Linwood and offices in Orlando, Plano and Westlake Village. One number reaches IMS: {PHONE}.",
       "region": REGION, "ring": 22, "alt": "Map of the United States with the five IMS offices",
       "items": [{"name": L[1], "lon": L[7], "lat": L[8], "href": f"locations/{L[0]}.html", "sub": f"{L[2]}, {L[3]}", "hq": i == 0, "link": "Office page",
                  **({"label_dx": -78, "label_dy": -8} if L[0] == "garnet-valley" else {"label_dx": 10, "label_dy": 14} if L[0] == "linwood" else {})}
                 for i, L in enumerate(LOCATIONS)]}
WORK_HOME = {"type": "work", "id": "work", "eyebrow": "The work", "heading": "Rooms and stages that won the industry's attention",
             "intro": "Five Commercial Integrator Integration Awards since 2021, and the 2025 Integrator of the Year. Every photograph here is an IMS project.",
             "items": WORK}
AWARDS_SEC = {"type": "awards", "id": "awards", "alt": True, "eyebrow": "On the record", "heading": "Recognized by the industry, judged by the room",
              "intro": "Every award named with who gave it and for what.", "items": AWARDS}
SEAL = {"type": "seal", "id": "seal", "eyebrow": "What every IMS customer gets", "heading": "Not a slogan. A list you can check.",
        "intro": "Six commitments behind every room, every program and every show.", "items": SEAL_ITEMS}
VOICES_SEC = {"type": "testimonials", "id": "voices", "alt": True, "layout": "feature", "eyebrow": "What customers say", "heading": "Customers, in their own words", "items": VOICES}
HOME_FAQ = {"type": "faq", "id": "faq", "heading": "Questions we get on the first call", "items": [
    ["What is One IMS?", "IMS is one company with three business units, Systems Integration, Managed Services and Event Staging, serving shared customers from one set of account teams."],
    ["Where is IMS based?", "Headquarters are at 3055 McCann Farm Drive in Garnet Valley, Pennsylvania. Event Staging is in Linwood, Pennsylvania, with offices in Orlando, Plano and Westlake Village."],
    ["Do you work outside the Philadelphia area?", "Yes. Many customers are in Greater Philadelphia, and IMS serves the northeast and customers nationally."],
    ["Can one company really build the room and run the event?", "That is the point of IMS. A town hall can run in a room IMS designed, installed and monitors, staged by a crew that knows it."],
    ["Which certifications does IMS hold?", "AVIXA AV Provider of Excellence (APEx), InfoComm Diamond level certification and ISO/IEC 27001:2022, with field technicians certified across the major manufacturers."]]}
CONTACT = {"type": "contact", "id": "contact", "heading": "Ready to look and sound your best?",
           "body": "Tell us about the room, the event or the program. One form reaches all three business units, and a person calls you back.",
           "options": ["Systems Integration", "Managed Services", "Event Staging", "AV as a Service", "Something else"], "submit": "Talk to IMS", "note": "A person replies, not an autoresponder."}
SERVICES_LIST = {"type": "services", "id": "services", "heading": "Everything from the install to the event", "intro": "Three business units, and the services that connect them. Each has its own page.",
                 "items": [[s[1], s[3], f"services/{s[0]}.html"] for s in SERVICES]}


def build():
    brand = {
        "accent": "#004B8D", "ink_secondary": "#FFFFFF", "chrome": "light",
        "type_from": {"Quantum Showcase": "Quantum Clean"},  # Shawn 9 Nov: the type of the Van Ausdall HubSpot site (Open Sans 800 headings, Inter body), not Bricolage
        "logo": "assets/ims-logo.png", "logo_alt": CLIENT, "logo_w": 140, "logo_h": 71,
        "logo_note": "The only logo on imsts.com is a 140 by 71 PNG. A vector is on the To confirm list.",
        "phone": PHONE, "phone_href": PHONE_HREF, "email": "",
        "utility": [{"label": "Managed Services", "href": "services/managed-services.html"}, {"label": "Locations", "href": "locations.html"}, {"label": "Careers", "href": "careers.html"}],
        "cta": {"label": "Talk to IMS", "href": "contact.html"},
        "sticky": {"primary": "Talk to IMS", "primary_href": "contact.html", "secondary": "Call IMS", "secondary_href": PHONE_HREF},
        "launcher": {"label": "Already a customer?", "eyebrow": "Reach your account team", "title": "What do you need today?",
                     "links": [["Call 610-361-1870", PHONE_HREF], ["Managed Services", "services/managed-services.html"], ["Plan an event", "services/event-staging.html"], ["Contact", "contact.html"]],
                     "note": "Your IMS account manager picks it up.", "phone": PHONE, "phone_href": PHONE_HREF},
        "social": {"linkedin": "https://www.linkedin.com/company/ims-technology-services", "youtube": "https://www.youtube.com/user/imsav", "facebook": "https://www.facebook.com/IMSESandSI", "x": "https://twitter.com/IMSEventStaging"},
        "tagline": "Award-winning systems integration, managed services and event staging since 1994. Headquartered in Garnet Valley, Pennsylvania.",
        "footer_columns": [
            {"title": "Services", "links": [[s[1], f"services/{s[0]}.html"] for s in SERVICES]},
            {"title": "Industries", "links": [[i[1], f"industries/{i[0]}.html"] for i in INDUSTRIES]},
            {"title": "Company", "links": [["Why IMS", "why-ims.html"], ["About", "about.html"], ["Locations", "locations.html"], ["Careers", "careers.html"], ["FAQ", "faq.html"], ["Contact", "contact.html"]]},
        ],
        "legal": [["Privacy policy", f"{SITE}/privacy-policy"], ["ISO/IEC 27001:2022", f"{SITE}/compliance-isoiec-270012022-standard-information-security-management"]],
    }
    schema = {"org_name": CLIENT, "org_url": SITE, "org_logo": f"{SITE}/sites/default/files/IMS_Logo.png",
              "org_description": "IMS Technology Services designs and installs AV and collaboration systems, runs them through Managed Services, and stages live, virtual and hybrid events. Founded in 1994, headquartered in Garnet Valley, Pennsylvania.",
              "sameAs": ["https://www.linkedin.com/company/ims-technology-services", "https://www.youtube.com/user/imsav", "https://www.facebook.com/IMSESandSI", "https://twitter.com/IMSEventStaging"],
              "telephone": "+1-610-361-1870", "founded": FOUNDED, "slogan": "Our success is defined by our clients' ability to look and sound their very best.",
              "short_name": SHORT, "title_city": "Philadelphia",
              "cities": ["Garnet Valley", "Philadelphia", "Linwood", "Orlando", "Plano", "Westlake Village", "Pennsylvania", "PA"],
              "area_served": [{"@type": "Country", "name": "United States"}],
              "meta_tail": "IMS Technology Services, Garnet Valley, PA, since 1994.",
              "people": [{"slug": n.split(",")[0].lower().replace(" ", "-").replace(".", ""), "name": n.split(",")[0], "title": r} for n, r in TEAM[:4]],
              "local": [{"slug": L[0], "name": f"IMS Technology Services {L[1]}", "street": L[2], "city": L[1], "region": L[9], "postal": L[3].split()[-1], "telephone": "+1-610-361-1870"} for L in LOCATIONS]}
    nav = [
        {"label": "Services", "href": "services.html", "children": [[s[1], f"services/{s[0]}.html"] for s in SERVICES]},
        {"label": "Industries", "href": "industries.html", "children": [[i[1], f"industries/{i[0]}.html"] for i in INDUSTRIES]},
        {"label": "Why IMS", "href": "why-ims.html", "children": [["Why IMS", "why-ims.html"], ["The work", "why-ims.html#work"], ["FAQ", "faq.html"]]},
        {"label": "About", "href": "about.html", "children": [["About IMS", "about.html"], ["Locations", "locations.html"], ["Careers", "careers.html"], ["Contact", "contact.html"]]},
    ]

    pages = []
    # ---------------- home
    pages.append({"file": "index.html", "title": f"AV Integration, Managed AV and Event Staging, Philadelphia | {CLIENT}",
                  "description": "IMS Technology Services: award-winning AV systems integration, managed services and event staging. 2025 Integrator of the Year, Garnet Valley, PA, since 1994.",
                  "compose": {
                      "showcase": ["hero", "partners", "work", "wheel", "ba-one", "flow", "awards", "story", "map", "voices", "faq", "contact"],
                      "clean": ["hero-light", "partners", "seal", "work", "services", "ba-one", "flow", "awards", "map", "voices", "faq", "contact"],
                      "press": ["hero-press", "work", "story", "services", "voices", "seal", "awards", "map", "faq", "contact"]},
                  "sections": [
        {"type": "hero", "id": "hero-light", "layout": "split", "eyebrow": "Systems Integration. Managed Services. Event Staging.", "stats": HERO_STATS,
         "ribbon": ["2025 Integrator of the Year", "SCN Top 50 Systems Integrators, 2023 to 2025", "ISO/IEC 27001:2022"],
         "heading": "Our success is defined by our clients' ability to look and sound <em>their very best</em>.",
         "subhead": "One company for the rooms you build, the systems that keep them running and the events you stage. Award-winning, founded in 1994, headquartered in Garnet Valley, Pennsylvania.",
         "primary": {"label": "Talk to IMS", "href": "contact.html"}, "secondary": {"label": "See the work", "href": "#work"},
         "image": "assets/hero-general-session.jpg", "image_alt": "A corporate general session staged by IMS, with IMS on the LED walls", "image_w": 1920, "image_h": 1080,
         "badge": {"value": "2025", "label": "Integrator of the Year"}},
        {"type": "hero", "id": "hero-press", "layout": "split", "eyebrow": "Since 1994", "ribbon": ["Founded in 1994", "Garnet Valley, Pennsylvania", "2025 Integrator of the Year"],
         "heading": "Thirty-two years of rooms and stages that <em>look and sound their best</em>.",
         "subhead": "IMS designs and installs the room, keeps it running and stages the event in it. Systems Integration, Managed Services and Event Staging, as one company.",
         "primary": {"label": "Talk to IMS", "href": "contact.html"}, "secondary": {"label": "Our story", "href": "#story"},
         "image": "assets/work-wcu-video-wall.jpg", "image_alt": "The Learning Stair LED wall at West Chester University, integrated by IMS", "image_w": 1600, "image_h": 633,
         "badge": {"value": "5", "label": "Commercial Integrator awards since 2021"}},
        HERO_LAYERED,
        {"type": "partners", "id": "partners", "caption": "Technology our certified field technicians design, install and support", "items": PARTNERS},
        WORK_HOME,
        SEAL,
        {"type": "wheel", "id": "wheel", "eyebrow": "One IMS", "heading": "Three business units, eight ways to work with IMS", "intro": "Hover a segment. Each service has its own page.",
         "items": WHEEL_ITEMS, "panel_eyebrow": "Hover a segment", "link_label": "See the service", "hub": "One IMS", "hub_sub": "three units", "ring": "LOOK AND SOUND YOUR VERY BEST"},
        SERVICES_LIST, BA_VENDORS, FLOW_HOME, AWARDS_SEC, HISTORY, MAP, VOICES_SEC, HOME_FAQ, CONTACT,
    ]})
    # ---------------- services
    pages.append({"file": "services.html", "title": f"AV Integration, Managed Services and Event Staging Services | {CLIENT}",
                  "description": "Systems Integration, Managed Services and Event Staging, plus AV as a Service, video walls, virtual events, streaming and content creation, all from IMS.",
                  "crumbs": [["Home", "index.html"], ["Services", "services.html"]],
                  "sections": [
        {"type": "hero", "layout": "split", "eyebrow": "Services", "heading": "Three business units, <em>one IMS</em>.",
         "subhead": "Systems Integration, Managed Services and Event Staging, with the services that connect them. One contract, one account team, one number.",
         "primary": {"label": "Talk to IMS", "href": "contact.html"}, "secondary": {"label": "Why IMS", "href": "why-ims.html"},
         "image": "assets/event-general-session.jpg", "image_alt": "An IMS-staged general session", "image_w": 1600, "image_h": 900},
        {"type": "wheel", "id": "wheel", "eyebrow": "Eight services", "heading": "Everything from the install to the event", "intro": "Hover a segment to read it.",
         "items": WHEEL_ITEMS, "panel_eyebrow": "Hover a segment", "link_label": "See the service", "hub": "One IMS", "hub_sub": "three units", "ring": "LOOK AND SOUND YOUR VERY BEST"},
        {"type": "resources", "alt": True, "heading": "Each service, in detail", "intro": "What changes, what is included and what customers ask.",
         "items": [[s[5], s[1], s[3], "See the service", f"services/{s[0]}.html"] for s in SERVICES]},
        BA_VENDORS,
        {"type": "work", "id": "work", "eyebrow": "The work", "heading": "Award-winning, and on the record", "intro": "Projects and events from all three business units.", "items": WORK},
        LEADFORM,
    ]})
    for s in SERVICES:
        pages.append(service_page(*s))
    for c in CASES:
        pages.append(case_page(c))
    # ---------------- industries
    pages.append({"file": "industries.html", "title": f"Industries: Corporate, Higher Ed, Pharma, Associations | {CLIENT}",
                  "description": "AV integration and event staging for corporate, higher education, pharmaceutical and medical, associations, government and professional services, from IMS.",
                  "crumbs": [["Home", "index.html"], ["Industries", "industries.html"]],
                  "sections": [
        {"type": "hero", "layout": "split", "eyebrow": "Industries", "heading": "Six markets, and <em>what each one needs</em>.",
         "subhead": "From a commencement in an arena to an investigator meeting behind closed doors, IMS has staged it, and builds the permanent rooms behind it.",
         "primary": {"label": "Talk to IMS", "href": "contact.html"}, "secondary": {"label": "Services", "href": "services.html"},
         "image": "assets/ind-higher-education.jpg", "image_alt": "A university commencement staged by IMS", "image_w": 1600, "image_h": 656},
        {"type": "resources", "alt": True, "heading": "Six markets", "intro": "Each page covers what we do, what customers ask and how to start.",
         "items": [["Industry", i[1], i[3], f"AV and events for {i[1].lower()}", f"industries/{i[0]}.html"] for i in INDUSTRIES]},
        {"type": "work", "id": "work", "eyebrow": "The work", "heading": "Across every market", "intro": "Corporate, campus, venue and association work.", "items": WORK},
        VOICES_SEC, LEADFORM,
    ]})
    for i in INDUSTRIES:
        pages.append(industry_page(*i))
    # ---------------- why, about, careers
    pages.append({"file": "why-ims.html", "title": f"Why IMS: Awards, Certifications and One Accountable Team | {CLIENT}",
                  "description": "2025 Integrator of the Year, SCN Top 50 three years running, five Commercial Integrator awards, AVIXA APEx and ISO/IEC 27001:2022. Why customers choose IMS.",
                  "crumbs": [["Home", "index.html"], ["Why IMS", "why-ims.html"]],
                  "sections": [
        {"type": "hero", "layout": "split", "eyebrow": "Why IMS", "heading": "Recognized by the industry. <em>Judged by the room.</em>",
         "subhead": "The 2025 Integrator of the Year, an SCN Top 50 Systems Integrator three years running, and five Commercial Integrator awards since 2021. And one accountable team behind every one.",
         "primary": {"label": "Talk to IMS", "href": "contact.html"}, "secondary": {"label": "See the work", "href": "#work"},
         "image": "assets/team-integrator-of-year.jpg", "image_alt": "The IMS team with the 2025 Integrator of the Year award", "image_w": 1920, "image_h": 781,
         "badge": {"value": "2025", "label": "Integrator of the Year"}},
        SEAL, AWARDS_SEC, BA_VENDORS,
        {"type": "work", "id": "work", "eyebrow": "The work", "heading": "The projects behind the awards", "intro": "Every photograph here is an IMS project.", "items": WORK},
        VOICES_SEC, LEADFORM,
    ]})
    pages.append({"file": "about.html", "title": f"About IMS: Founded 1994, Garnet Valley, Pennsylvania | {CLIENT}",
                  "description": "Founded in 1994 as IMS, Inc. by Jill and John Renninger, IMS Technology Services has grown and been profitable every year. Headquartered in Garnet Valley, PA.",
                  "crumbs": [["Home", "index.html"], ["About", "about.html"]],
                  "sections": [
        {"type": "hero", "layout": "split", "eyebrow": "About IMS", "heading": "All about process, performance and <em>accountability</em>.",
         "subhead": "IMS was founded in 1994 as IMS, Inc. by Jill and John Renninger, and has grown and been profitable every year since. Our goal has not changed: the best value in AV integration, event staging, project management and managed services, with an old-fashioned can-do attitude.",
         "primary": {"label": "Talk to IMS", "href": "contact.html"}, "secondary": {"label": "Careers", "href": "careers.html"},
         "image": "assets/team-kickoff-2024.jpg", "image_alt": "The IMS team at the 2024 company kickoff", "image_w": 1600, "image_h": 900},
        {"type": "stats", "alt": True, "items": [["1994", "Founded as IMS, Inc."], ["8x", "Inc. 5000 fastest growing companies"], ["5", "Offices in four states"], ["2025", "Integrator of the Year"]]},
        HISTORY,
        {"type": "leadership", "id": "leadership", "heading": "The IMS management team", "intro": "The people who run Event Staging, Systems Integration and Managed Services.", "people": TEAM},
        AWARDS_SEC, MAP, VOICES_SEC,
        {"type": "cta", "heading": "Want to join the IMS team?", "subhead": "We are looking for motivated, creative, dynamic professionals.", "primary": {"label": "See careers", "href": "careers.html"}},
    ]})
    pages.append({"file": "careers.html", "title": f"Careers at IMS Technology Services, Garnet Valley, PA | {CLIENT}",
                  "description": "Join the 2025 Integrator of the Year. IMS is looking for motivated, creative, dynamic professionals in systems integration, managed services and event staging.",
                  "crumbs": [["Home", "index.html"], ["Careers", "careers.html"]],
                  "sections": [
        {"type": "hero", "layout": "split", "eyebrow": "Careers", "heading": "Join the team that <em>looks and sounds its best</em>.",
         "subhead": "IMS is an eight-time Inc. 5000 company and the 2025 Integrator of the Year, and we are looking for motivated, creative, dynamic professionals to join us.",
         "primary": {"label": "Tell us about yourself", "href": "#apply"}, "secondary": {"label": "Talk to IMS", "href": "contact.html"},
         "image": "assets/team-integrator-of-year.jpg", "image_alt": "The IMS team", "image_w": 1920, "image_h": 781},
        {"type": "values", "alt": True, "eyebrow": "Working at IMS", "heading": "Serious work, in good company",
         "items": [["Award-winning work", "Longwood Gardens, U.S. Squash, Five Below, West Chester University: the projects people in this industry want on their resume."],
                   ["Three business units", "Systems Integration, Managed Services and Event Staging, so a career can grow in more than one direction."],
                   ["Equal opportunity", "IMS Technology Services, LLC is an Equal Opportunity Employer."]]},
        {"type": "cards", "eyebrow": "Who we hire", "heading": "Roles across the company", "items": [
            ["Field engineers and technicians", "Install, program and commission the systems, certified on the platforms we integrate."],
            ["Production crew", "Audio, video, lighting and scenic for events of every size, staff and freelance."],
            ["Project and production managers", "Own the schedule, the budget and the customer, from first call to handover."],
            ["Managed services and support", "Keep the rooms ready 24/7/365, with 4Sight and an IMS service team."]]},
        {"type": "leadform", "alt": True, "id": "apply", "heading": "Tell us about yourself", "body": "Staff or freelance, send a note with your experience and we will be in touch. A person reads every one.", "submit": "Send",
         "note": "Freelancers are always welcome.", "fields": [["Name", "text", "name"], ["Email", "email", "email"], ["Phone", "tel", "tel"], ["Role you are interested in", "text", "organization-title"], ["Link to your resume or LinkedIn", "url", "url"]]},
    ]})
    # ---------------- locations
    pages.append({"file": "locations.html", "title": f"Locations: Garnet Valley, Linwood, Orlando, Plano, Westlake Village | {CLIENT}",
                  "description": "IMS offices in Garnet Valley (headquarters) and Linwood, Pennsylvania, Orlando, Florida, Plano, Texas and Westlake Village, California. One number: 610-361-1870.",
                  "crumbs": [["Home", "index.html"], ["Locations", "locations.html"]],
                  "sections": [
        {"type": "hero", "layout": "split", "eyebrow": "Locations", "heading": "Five offices. <em>One number.</em>",
         "subhead": f"Headquartered in Garnet Valley, Pennsylvania, with offices in Linwood, Orlando, Plano and Westlake Village. Call {PHONE} to reach IMS from anywhere.",
         "primary": {"label": f"Call {PHONE}", "href": PHONE_HREF}, "secondary": {"label": "Talk to IMS", "href": "contact.html"},
         "image": "assets/team-integrator-of-year.jpg", "image_alt": "The IMS team", "image_w": 1920, "image_h": 781},
        MAP,
        {"type": "resources", "alt": True, "heading": "Office pages", "intro": "What each office does, who it serves and how to reach it.",
         "items": [[L[6], f"IMS {L[1]}", f"{L[2]}, {L[3]}.", f"About {L[1]}", f"locations/{L[0]}.html"] for L in LOCATIONS]},
        LEADFORM,
    ]})
    for L in LOCATIONS:
        pages.append(location_page(*L))
    # ---------------- faq, contact
    pages.append({"file": "faq.html", "title": f"Frequently Asked Questions | {CLIENT}",
                  "description": "What One IMS means, where IMS works, the awards and certifications, AV as a Service, and how to plan an event or a room with IMS Technology Services.",
                  "crumbs": [["Home", "index.html"], ["FAQ", "faq.html"]],
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "FAQ", "heading": "The questions people <em>ask first</em>.", "subhead": f"Not here? Call {PHONE} and ask a person.",
         "primary": {"label": "Talk to IMS", "href": "contact.html"}},
        {"type": "faq", "heading": "Common questions", "items": HOME_FAQ["items"] + [
            ["What does IMS do?", "IMS designs and installs AV and collaboration systems, keeps them running through Managed Services, and stages live, virtual and hybrid events."],
            ["What awards has IMS won?", "2025 Integrator of the Year; SCN Top 50 Systems Integrators in 2023, 2024 and 2025; Commercial Integrator Integration Awards in 2021, 2022, 2023, 2024, 2025 and 2026; and eight Inc. 5000 listings."],
            ["What is AV as a Service?", "A subscription that bundles AV technology, support, monitoring and planned upgrades into one monthly cost."],
            ["How do I plan an event with IMS?", "Use the form or call 610-361-1870. Every event customer gets a dedicated production manager and account representative."]]},
        LEADFORM,
    ]})
    pages.append({"file": "contact.html", "title": f"Contact IMS: 610-361-1870, Garnet Valley, PA | {CLIENT}",
                  "description": "Talk to IMS about a room, an event or a managed services program. One form reaches Systems Integration, Managed Services and Event Staging. 610-361-1870.",
                  "crumbs": [["Home", "index.html"], ["Contact", "contact.html"]],
                  "sections": [
        {"type": "hero", "layout": "split", "eyebrow": "Contact", "heading": "Tell us about the room, <em>the event or the program</em>.",
         "subhead": f"One form and one number reach Systems Integration, Managed Services and Event Staging. Call {PHONE}, or write, and a person calls you back.",
         "primary": {"label": f"Call {PHONE}", "href": PHONE_HREF}, "secondary": {"label": "Use the form", "href": "#form"},
         "image": "assets/team-kickoff-2024.jpg", "image_alt": "The IMS team", "image_w": 1600, "image_h": 900},
        dict(CONTACT, id="form", heading="Start here"),
        {"type": "locations", "alt": True, "detailed": True, "heading": "Offices", "intro": f"One number reaches all five offices: {PHONE}.",
         "items": [[f"{L[1]} ({L[6]})", L[2], L[3], L[4], L[5]] for L in LOCATIONS]},
    ]})

    pitch = {
        "qbs_contact": {"name": "Shawn Peterson", "email": "shawn@thequantumleap.business", "phone": "(712) 389-4639"},
        "prepared_for": "Jason Smith, IMS Technology Services",
        "heard_intro": "Everything here comes from imsts.com, your HubSpot rollout and our calls. Tell us where it is wrong; your words outrank ours.",
        "heard": [
            "One IMS: three business units, Systems Integration, Managed Services and Event Staging, with shared customers, one CRM and account managers per unit. The site should say that in the first five seconds.",
            "Managed Services lives on its own subdomain today, and the contact page and forms run on SharpSpring. Everything moves onto one site, and every form lands in HubSpot.",
            "The current site is about 95 pages on Drupal, last refreshed years ago, and the Managed Services page was rebuilt quickly and does not match the rest.",
            "You have just added two companies and a national footprint. The site has to read as a national company with deep Philadelphia roots.",
            "The promise, in your words: our success is defined by our clients' ability to look and sound their very best."],
        "found": [
            "Your best proof is invisible. Five Commercial Integrator award projects and a gallery of staged events sit in case studies that average 24 out of 100 and do not rank. Every direction now leads with the work, in your own photography.",
            "None of the 12 money pages has a form, and none of 95 pages carries structured data. Every page in these directions has a form, and schema that tells search engines and AI assistants who IMS is.",
            "For event live streaming and digital signage in Garnet Valley, imsts.com is not in the top ten. Both pages are rebuilt here to compete.",
            "Five offices, and no page for any of them. Each office now has its own page, with local business schema."],
        "pick_reasons": [
            ["Your work is the pitch", "Showcase opens on your own stages and rooms, full-bleed and moving, then puts the five award projects in front of the buyer before a single paragraph."],
            ["Three business units, one story", "Showcase's wheel, before-and-after and one-company flow explain One IMS visually, which the other two can only say in words."],
            ["An events company should feel like a show", "Showcase has the depth and motion of a stage; Clean and Press are calmer, and better suited to a buyer who reads before they look."]],
        "pick_change": "Showcase's own display face read as playful for buyers in IT and finance, so it is set here in Open Sans and Inter, plainer and more precise. The one thing we would still add is motion from your own shows: a short cut of event footage behind the hero instead of photographs.",
        "alternatives": [
            ["Quantum Clean", "If the buyer is IT and facilities first: the same work and proof, in a plainer, faster-to-scan layout with the checkable list near the top."],
            ["Quantum Press", "If heritage and the award record are the story: an editorial serif, thirty-two years told as a story, and the most magazine-like of the three."]],
        "choice_intro": "All three are the whole site, with the same words, the same photography and the same proof. The difference is temperament. Open each one on your phone and tell us which feels like IMS.",
        "plan": [
            ["Week 1", "Choose a direction. Confirm the items under To confirm. Send the logo as a vector."],
            ["Weeks 2 to 3", "Copy for every page from your three business unit leaders, in your words. Project photography gathered from your case study library."],
            ["Weeks 3 to 5", "Build in your HubSpot: theme cloned and re-skinned, every page built, Managed Services moved in from its subdomain, every form wired to a named person."],
            ["Week 6", "Quality gate on every page, on a real phone. Every old URL redirected and tested. Your team edits a page in the walkthrough."],
            ["Launch, then 90 days", "Go live. Search and AI visibility re-measured at 30, 60 and 90 days against the September baseline."]],
        "search": {
            "heading": "Where you stand in search today, and what changes",
            "intro": "Measured before we touched anything, so the work can be judged against it. QBS SEO and AEO analysis of imsts.com, 13 September 2026: a crawl of all 95 pages, Semrush, and live buyer searches from Garnet Valley.",
            "as_of": "13 September 2026",
            "today_stats": [["45/100", "Search and AI visibility score"], ["1,443", "Organic visits a month"], ["8,897", "Visits a month on the table"], ["0 of 95", "Pages with structured data"]],
            "today": [
                "Search and AI visibility scores 45 out of 100. The weakest part is structured data and the entity, at 0 out of 100.",
                "1,443 organic visits a month from 763 keywords, worth about $406 in paid clicks. 27 percent of it is people searching the name.",
                "Strong at home where it counts: imsts.com is in the top ten for 7 of 9 buyer searches from Garnet Valley, and first for av systems integration garnet valley.",
                "Absent where it should not be: 0 of 10 for event live streaming services garnet valley and for digital signage installation garnet valley.",
                "None of the 12 money pages has a form; one has a phone link. The contact page and forms run on SharpSpring.",
                "An AI assistant named IMS in 4 of 5 buyer questions, without any schema to help it."],
            "after": [
                "Organization, LocalBusiness and Service schema on every page, with sameAs links to LinkedIn, YouTube, Facebook and X.",
                "A form and a tap-to-call number on every money page, wired to HubSpot.",
                "Five office pages with local business schema, and city names in the titles that matter.",
                "The award projects rebuilt as pages that rank and get quoted, with the photography up front.",
                "Every page scored on our gate before you see it, and every old URL redirected and tested at launch."],
            "keep_heading": "Every page that earns a visitor today keeps earning it",
            "keep": [["/systems-integration", "/services/systems-integration", "av systems integration garnet valley #1"],
                     ["/event-staging", "/services/event-staging", "event staging and AV rental, Philadelphia"],
                     ["/managed-services and managedservices.imsts.com", "/services/managed-services", "managed AV services; the subdomain folds in"],
                     ["/lp/case-study-*", "the work, on every direction", "the five award projects"]],
            "note": "Rankings or traffic by a date. Those depend on the market and on what you publish after launch. What we promise is that nothing about the build is the reason they do not come, and that the same analysis is re-run at 30, 60 and 90 days."},
        "confirm": [
            "Legal name: the careers page says IMS Technology Services, LLC and the About page says the company began as IMS, Inc. Schema uses IMS Technology Services.",
            "Logo: the only file on imsts.com is a 140 by 71 PNG. Please send the vector, and a white version for dark backgrounds. The blue, #004B8D, is read from the logo.",
            "Photography is IMS's own, from imsts.com and your case studies. Confirm you hold the rights to all of it, and send originals of the case study photography if you have them.",
            "The hero captions name what is on screen in general terms (a corporate general session, a national association congress, a university commencement). Tell us the client and venue names you are happy to publish.",
            "Partner names come from your certification and project text, not from partner logos. Confirm which marks you are authorized to show.",
            "WBENC certification appears on your event staging page. Confirm it is current and we will add it to the commitments.",
            "The Best Meeting Room Project award for 2026: tell us the project and we will add it to the work.",
            "The two acquisitions: when they can be announced, and what can be said. The site is built to add them as offices.",
            "Testimonials are the ones published on imsts.com. Confirm permission to reuse them.",
            "Who receives each form, by business unit, so a person replies every time.",
            "The Scenic and Design Portal, exhibit ordering and any customer portal: send the addresses and we will link them.",
            "The five case study pages use facts from Commercial Integrator's award writeups and your own case study pages. Medallion Hall's seat count is 75-plus at Commercial Integrator and 144-plus on imsts.com, so we left it out. Tell us the right number.",
            "The AV as a Service calculator uses typical monthly rates (3.2 percent of equipment cost over 36 months, 2.1 percent over 60) and $65 an hour for staff time. Send your real AVaaS rates and we will use them.",
            "A recent event reel. The only video on your YouTube channel is ten years old. Send the 2025 event technology video from Facebook, or any recent reel, and it becomes the moving hero on Showcase."],
        "footer": "Prepared for Jason Smith, IMS Technology Services. Nothing here is live or indexed. Every photograph is IMS's own work, from imsts.com.",
    }
    _FAQ_EXTRA = {
        "about.html": ("Questions about IMS", [
            ["Who founded IMS?", "Jill and John Renninger founded the company in 1994 as IMS, Inc."],
            ["Where are the IMS offices?", "Garnet Valley (headquarters) and Linwood, Pennsylvania; Orlando, Florida; Plano, Texas; and Westlake Village, California."],
            ["Is IMS one company or three?", "One company with three business units, Systems Integration, Managed Services and Event Staging, sharing customers and account teams."]]),
        "careers.html": ("Working at IMS", [
            ["Do you hire freelancers?", "Yes. Freelance production crew are always welcome to send their information."],
            ["Where would I work?", "Garnet Valley, Linwood, Orlando, Plano or Westlake Village, with field and event roles wherever the work is."],
            ["Is IMS an equal opportunity employer?", "Yes. IMS Technology Services, LLC is an Equal Opportunity Employer."]]),
        "contact.html": ("Before you call", [
            ["Which business unit should I ask for?", "You do not need to know. One form and one number reach all three, and we route you to the right team."],
            ["I am already a customer. Who do I call?", "Your IMS account manager, or 610-361-1870."],
            ["Who replies?", "A person, during business hours. The form is not an autoresponder."]]),
        "industries.html": ("Questions from specific industries", [
            ["My industry is not listed. Can you still help?", "Yes. These six are where we stage the most events; the rooms and the managed services work the same way for everyone."],
            ["Do you have references in my industry?", "Yes. Ask your account representative for a reference in your field."]]),
        "services.html": ("How the services fit", [
            ["Do I have to buy everything from IMS?", "No. Most customers start with one business unit and add the others as the relationship earns it."],
            ["What is One IMS?", "Systems Integration, Managed Services and Event Staging as one company, with shared customers and account teams."]]),
        "why-ims.html": ("Questions about the record", [
            ["Who named IMS Integrator of the Year?", "NSCA, Commercial Integrator and Security Sales & Integration, for 2025."],
            ["Which projects won Commercial Integrator awards?", "U.S. Squash (2021), the Whitney Athletic Center (2022), West Chester University's Learning Stair video wall (2023), Five Below's Medallion Hall (2024) and Longwood Reimagined (2025), with a Best Meeting Room Project award in 2026."]]),
        "locations.html": ("Coverage questions", [
            ["Do you cover my city?", "IMS supports customers nationally from five offices. Call 610-361-1870 and we will tell you who will be on site."],
            ["Can I visit?", "Yes. Call ahead and we will set a time at the office nearest you."]]),
    }
    for _pg in pages:
        if _pg["file"] in _FAQ_EXTRA and not any(x.get("type") == "faq" for x in _pg["sections"]):
            _h, _items = _FAQ_EXTRA[_pg["file"]]
            _faq = {"type": "faq", "id": "faq", "heading": _h, "items": _items}
            _secs = _pg["sections"]
            if _secs and _secs[-1].get("type") in ("leadform", "cta", "contact", "locations"):
                _secs.insert(len(_secs) - 1, _faq)
            else:
                _secs.append(_faq)
    return {"client": CLIENT, "slug": "ims-technology-services", "domain_hint": "imsts.com",
            "brand": brand, "schema": schema, "nav": nav, "pages": pages, "pitch": pitch,
            # Sentences the gate would stop, each with the page on imsts.com that says it (checked 10 Nov 2026).
            "claims_ok": [
                {"text": "24/7", "source": f"{SITE}/managed-services"},
                {"text": "Rooms watched around the clock", "source": f"{SITE}/managed-services"},
                {"text": "Managed Services monitors installed systems 24/7/365, with tiers that match coverage to what is mission-critical.", "source": f"{SITE}/managed-services"},
                {"text": "Rooms watched 24/7/365 by the people who installed them", "source": f"{SITE}/managed-services"},
                {"text": "Rooms watched 24/7/365.", "source": f"{SITE}/managed-services"},
                {"text": "IMS Managed Services monitors the rooms 24/7/365 and keeps them ready, with 4Sight reporting for leadership.", "source": f"{SITE}/managed-services"},
                {"text": "24/7/365 monitoring, with tiers that match coverage to what is mission-critical.", "source": f"{SITE}/managed-services"},
                {"text": "Keep the rooms ready 24/7/365, with 4Sight and an IMS service team.", "source": f"{SITE}/managed-services"},
                {"text": "24/7 monitoring and management that catches most issues before they become downtime.", "source": f"{SITE}/avaas"},
                {"text": "The right AV solution, with the Solution Replacement Guarantee (SRG)", "source": f"{SITE}/avaas"},
                {"text": "What is the Solution Replacement Guarantee?", "source": f"{SITE}/avaas"},
                {"text": "Presentation, projection, playback, mapping, blends and live recording on state-of-the-art equipment.", "source": f"{SITE}/event-staging"},
                {"text": "A dedicated production manager and account representative for every customer", "source": f"{SITE}/event-staging"},
            ]}


if __name__ == "__main__":
    data = build()
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"wrote {OUT}: {len(data['pages'])} pages")
