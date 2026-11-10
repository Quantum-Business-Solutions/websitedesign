"""DMP page module: tools, trust center, stories, lead magnet. Data only: PAGES and TO_CONFIRM.
Pages: assessment (dealer system-fit check), savings-estimator, stories, stories/template-dealer-story, resources/dealer-playbook,
trust, accessibility, 404. Section types p3* are rendered by scripts/preview_pop3.py.
Facts come from pages already written for this site (communicators, wireless, Dealer Admin, certifications, SOC 2 article);
the tools score and calculate only what the visitor types, and no figure is presented as a DMP claim."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dmp_common import *

PAGES = []
TO_CONFIRM = []


def _hero(eyebrow, heading, subhead, primary, secondary, image, alt, w=1200, h=900):
    return {"type": "hero", "layout": "split", "eyebrow": eyebrow, "heading": heading, "subhead": subhead,
            "primary": primary, "secondary": secondary, "image": image, "image_alt": alt, "image_w": w, "image_h": h}


def _lead(heading, body, note=None):
    d = dict(LEADFORM)
    d["heading"], d["body"] = heading, body
    if note:
        d["note"] = note
    return d


# ================================================================================================ assessment
AREAS = {
    "panels": {"title": "Panels and growth", "text": "The XT, XTL and XR panels scale from a small business to a large site. The XR550 handles 96 doors, 574 zones and 10,000 user codes.",
               "links": [["Panels and keypads", "services/panels-keypads.html"], ["Which commercial intrusion panel fits which building", "blog/which-commercial-intrusion-panel.html"]]},
    "comms": {"title": "Communicators and encryption", "text": "DMP communicators carry alarm signals over LTE, network and Wi-Fi paths, with AES encrypted options on communicators and receivers.",
              "links": [["Communicators and monitoring", "services/communicators.html"], ["How cellular alarm communication works", "blog/cellular-alarm-communication-options.html"]]},
    "wireless": {"title": "Wireless devices", "text": "Two-way, supervised 900 MHz devices add zones without new wire, and the 1100 Series has been AES encrypted since 2019.",
                 "links": [["Wireless", "services/wireless.html"], ["What to know before a wireless retrofit", "blog/wireless-security-devices-retrofit.html"]]},
    "remote": {"title": "Remote service and Dealer Admin", "text": "Dealer Admin performs bulk remote updates and mass programming changes, with system health status on one dashboard. Virtual Keypad gives customers remote control under the dealer's brand.",
               "links": [["Dealer Admin", "products/dealer-admin.html"], ["Virtual Keypad and software", "services/mobile-automation.html"]]},
    "access": {"title": "Access control", "text": "Access control runs from the cloud-based X1 to Entré software, and Digital Key puts a credential in the phone's mobile wallet.",
               "links": [["Access control", "services/access-control.html"], ["Cloud-based access control: a dealer guide", "blog/cloud-based-access-control-dealer-guide.html"]]},
    "video": {"title": "Video verification", "text": "VUE Plus cameras, an XV gateway with AlarmVision and the panel turn a motion alarm into something a person can see and confirm.",
              "links": [["Video", "services/video.html"], ["How to add video verification to an alarm system", "blog/add-video-verification-to-alarm-system.html"]]},
    "trust": {"title": "Cloud trust", "text": "Dealer Admin and Virtual Keypad are examined for SOC 2 Type II every year by a licensed CPA firm, to AICPA standards.",
              "links": [["What SOC 2 Type II means for a security platform", "blog/soc-2-type-ii-security-platform.html"], ["Trust center", "trust.html"]]},
}
QUESTIONS = [
    ["panels", "Can the panels you install most often grow in zones, doors and users without a panel swap?", "Think about the panel line you sell into small sites and into large ones."],
    ["comms", "Can your panels send alarm signals over both network and cellular paths?", "Network, Wi-Fi and LTE are the common options."],
    ["comms", "Do your alarm signals travel over a supervised communication path?", "Supervised means the path itself is checked, not only the alarm."],
    ["comms", "Do you have a way to detect cellular jamming at sites where it matters?", "For example a dedicated jamming detector."],
    ["comms", "Is alarm communication encrypted on the paths you use, for example with AES?", "Think about communicators, receivers and the panel connection."],
    ["wireless", "Is the wireless device line you sell two-way, supervised and encrypted?", "Think about transmitters, detectors and receivers."],
    ["remote", "Can you update panel firmware and programming remotely, without a visit?", "Think about your usual service call."],
    ["remote", "Can you push the same programming change or firmware update to many customer systems at once?", "Bulk or mass changes rather than one panel at a time."],
    ["remote", "Can you give each member of staff only the access they need, and offer single sign-on?", "Custom roles and single sign-on in your management portal."],
    ["remote", "Can customers manage their system from a phone or browser, under your brand?", "A branded remote control app."],
    ["access", "Can your access control offer phone-based credentials, such as a mobile wallet or Bluetooth credential?", "A credential on the phone instead of a card."],
    ["access", "Can one platform family cover both a single-door site and a multi-door, multi-site customer?", "From a stand-alone controller to enterprise software."],
    ["video", "Can you add camera verification to an intrusion alarm so a person can see and confirm it?", "Cameras linked to the panel, with video at the time of the alarm."],
    ["trust", "Do the cloud services you rely on have an independent SOC 2 Type II examination every year that you can talk about with customers?", "Ask what it covers and who examines it."],
]
PAGES.append({
    "file": "assessment.html",
    "title": "Dealer system-fit check | Digital Monitoring Products",
    "description": desc("Fourteen yes, not sure or no questions on panels, communicators, remote service, access and video, with three places to look next. Illustrative scoring."),
    "crumbs": [["Home", "index.html"], ["Dealer system-fit check", "assessment.html"]],
    "schema": [],
    "sections": [
        _hero("Dealer system-fit check", "How well does your setup <em>support growth?</em>",
              "Fourteen yes, not sure or no questions on your panel line, communicators, remote service, access control and video. You get a score and three places to look next.",
              {"label": "Start the check", "href": "#check"}, {"label": "Find a system instead", "href": "find-a-system.html"},
              IMG + "tab-mobile-1200.jpg", "Dealer Admin and Virtual Keypad on a laptop, tablet and phone"),
        {"type": "p3assess", "id": "check", "eyebrow": "The check", "heading": "One question at a time.",
         "intro": "Answer for the setup you use today. The questions ask about capabilities DMP describes on its own pages, and they are neutral: not sure is a fine answer.",
         "areas": AREAS, "questions": QUESTIONS},
        {"type": "resources", "alt": True, "eyebrow": "Keep going", "heading": "Other ways to find your fit.",
         "items": [["Tool", "Savings estimator", "Type your own service-call numbers and see the math.", "Open the estimator", "savings-estimator.html"],
                   ["Tool", "Find a system", "Choose a product type, then a system, and see every matching product.", "Find a system", "find-a-system.html"],
                   ["Trust", "Trust center", "What DMP says about SOC 2 Type II, certifications and contacts.", "Open the trust center", "trust.html"]]},
        _lead("Talk through your results", "Say what you sell today and where the gaps are, and Inside Sales will reply."),
    ]})
TO_CONFIRM.append("Dealer system-fit check: scoring is illustrative (yes 2, not sure 1, no 0, as a share of possible points) and the three score bands are our own. DMP to confirm the questions, the bands and whether results should feed a CRM. Every question and recommendation draws only on capabilities stated on DMP's own pages.")

# ================================================================================================ savings estimator
PAGES.append({
    "file": "savings-estimator.html",
    "title": title("Service-call savings estimator"),
    "description": desc("Type your own service-call numbers and see a monthly and yearly estimate, with the formula written out. Your numbers, your math. Not a DMP guarantee."),
    "crumbs": [["Home", "index.html"], ["Service-call savings estimator", "savings-estimator.html"]],
    "schema": [],
    "sections": [
        _hero("Savings estimator", "What could fewer visits <em>be worth to you?</em>",
              "A calculator that starts empty. You type your own service-call numbers and it shows a monthly and yearly figure, with the formula in plain sight.",
              {"label": "Enter your numbers", "href": "#estimate"}, {"label": "Dealer Admin", "href": "products/dealer-admin.html"},
              IMG + "tab-spec-1200.jpg", "A DMP spec sheet and a control panel on a desk"),
        {"type": "p3calc", "id": "estimate", "eyebrow": "The estimator", "heading": "Your numbers, your math.",
         "intro": "Nothing is pre-filled and no figure here comes from DMP. The share that could be handled remotely is your own judgment.",
         "caps": [["Remote programming.", "Remote Link updates firmware and programming from a laptop.", "Remote Link", "products/remote-link.html"],
                  ["Bulk updates.", "Dealer Admin performs bulk remote updates and mass programming changes, with system health status on a single dashboard.", "Dealer Admin", "products/dealer-admin.html"],
                  ["What can be remote.", "DMP does not say how many calls these remove, and neither does this page. Technical Support can talk through a specific call.", "Technical support FAQs", "support/tech-faqs.html"]]},
        {"type": "resources", "alt": True, "eyebrow": "Next", "heading": "Read how the remote tools work.",
         "items": [["Software", "Dealer Admin", "The cloud portal for status, mass programming and bulk remote updates.", "See Dealer Admin", "products/dealer-admin.html"],
                   ["Software", "Remote Link", "Panel management software to update firmware and programming from a laptop.", "See Remote Link", "products/remote-link.html"],
                   ["Tool", "Dealer system-fit check", "Fourteen questions on how your setup supports growth.", "Take the check", "assessment.html"]]},
        _lead("Want to talk through your own numbers?", "Tell Inside Sales what your service calls look like and a person will reply."),
    ]})
TO_CONFIRM.append("Savings estimator: inputs start empty and the formula is ours (calls x share x (cost per call + hours per call x hourly cost)). No default, benchmark or DMP claim is shown. DMP to confirm the wording 'Your numbers, your math. Not a DMP guarantee.' and whether legal wants a longer disclaimer.")

# ================================================================================================ stories
PH_METRICS = ["First result, to be supplied", "Second result, to be supplied", "Third result, to be supplied"]
PAGES.append({
    "file": "stories.html",
    "title": "Dealer stories | Digital Monitoring Products",
    "description": desc("Dealer stories: what an installer did, with which DMP products, and what happened. One published story today, and room for yours."),
    "crumbs": [["Home", "index.html"], ["Dealer stories", "stories.html"]],
    "schema": [],
    "sections": [
        _hero("Dealer stories", "What dealers <em>did with it.</em>",
              "A place for real installs: the problem, the products, the result. One story is published today. The rest are placeholders waiting for a DMP dealer.",
              {"label": "Read the published story", "href": "news/small-sensor-big-save.html"}, {"label": "See the story layout", "href": "stories/template-dealer-story.html"},
              IMG + "sensor-1112-1200.jpg", "A DMP 1112 wireless water and temperature detector", 1200, 800),
        {"type": "p3stories", "id": "stories", "eyebrow": "The stories", "heading": "One published. Three waiting.",
         "intro": "The three placeholder cards show where dealer stories will sit. No name, number or quote on them is real.",
         "template": "stories/template-dealer-story.html",
         "items": [{"real": True, "title": "A small sensor. A big save.",
                    "text": "A 1112 Wireless Water and Temperature Detector under a water heater, connected to an XT75. A week later the heater burst and the alarm sounded while the installer was out of town.",
                    "href": "news/small-sensor-big-save.html"}, {}, {}, {}]},
        {"type": "cards", "alt": True, "eyebrow": "How a story reads", "heading": "Every story follows the same four steps.",
         "items": [["Challenge", "What the customer or the dealer needed, in the dealer's words."],
                   ["Solution", "Which DMP products the dealer chose, linked to their pages."],
                   ["Result", "What happened. Numbers appear only when the dealer supplies them and DMP confirms them."],
                   ["Quote", "A line from the dealer or the customer, used with permission."]]},
        _lead("Have a story to share?", "If you are an authorized DMP dealer with a result you can talk about, tell Inside Sales."),
    ]})
PAGES.append({
    "file": "stories/template-dealer-story.html",
    "title": "Dealer story template | Digital Monitoring Products",
    "description": desc("The layout of a DMP dealer story: metric band, quote card, challenge, solution, result and the products used. Every value is a placeholder."),
    "crumbs": [["Home", "index.html"], ["Dealer stories", "stories.html"], ["Story template", "stories/template-dealer-story.html"]],
    "schema": [],
    "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "Dealer story template", "heading": "[Dealer name]: <em>the headline states the result</em>",
         "subhead": "Story to be supplied by a DMP dealer. This page shows the layout only; nothing on it is a real story."},
        {"type": "p3story", "metrics": PH_METRICS, "quote": "Quote to be supplied by the dealer. It would sit here, in the dealer's own words, used with permission.",
         "by": "[Name], [title], [dealer company]. Placeholder: no quote has been written.",
         "eyebrow": "Challenge, solution, result", "heading": "The story in three parts.",
         "csr": [["Challenge", "Placeholder. What the customer or the dealer needed, described in a few sentences."],
                 ["Solution", "Placeholder. Which DMP products the dealer chose and how they were installed."],
                 ["Result", "Placeholder. What happened afterwards. Any number is supplied by the dealer and confirmed by DMP."]],
         "products": [["Dealer Admin", "products/dealer-admin.html"], ["Virtual Keypad", "products/virtual-keypad.html"], ["XT75 control panel", "products/xt75.html"],
                      ["XR550 control panel", "products/xr550.html"], ["Communicators", "services/communicators.html"], ["VUE Plus video", "services/video.html"]]},
        _lead("Want your dealer story here?", "Tell Inside Sales about an install you are proud of."),
    ]})
TO_CONFIRM += [
    "Dealer stories: the hub shows one real published story (the 1112 water-sensor story at news/small-sensor-big-save.html) and three placeholder cards. DMP to confirm who collects, approves and publishes dealer stories, and whether customer permission wording is needed. The template page contains no invented names, numbers or quotes.",
]

# ================================================================================================ dealer playbook (gated lead magnet)
PAGES.append({
    "file": "resources/dealer-playbook.html",
    "title": title("Dealer playbook: title to be confirmed"),
    "description": desc("A gated dealer playbook: the gate form, a thank-you state, a cover mock, the chapters inside and the delivery email. Title and chapters are placeholders."),
    "crumbs": [["Home", "index.html"], ["News and resources", "resources.html"], ["Dealer playbook", "resources/dealer-playbook.html"]],
    "schema": [],
    "sections": [
        {"type": "p3gate", "id": "gate", "eyebrow": "Free for dealers (to be confirmed)", "heading": "Dealer playbook: title to be confirmed",
         "intro": "A guide for security dealers. The title and the chapters are placeholders until DMP confirms them.",
         "inside_heading": "Six chapters, all placeholders.", "inside_intro": "Generic chapter ideas that stand in for the real contents. Each one is marked to confirm.",
         "chapters": [["Choosing a platform to grow on", "Placeholder chapter, to confirm."], ["Reliable alarm communication", "Placeholder chapter, to confirm."],
                      ["Service without the truck roll", "Placeholder chapter, to confirm."], ["Adding access control and video", "Placeholder chapter, to confirm."],
                      ["Training your team", "Placeholder chapter, to confirm."], ["Working with DMP as an authorized dealer", "Placeholder chapter, to confirm."]]},
        {"type": "cta", "alt": True, "heading": "Not a dealer yet?", "subhead": "Approval to become an authorized DMP dealer should take just a few days.", "primary": {"label": "Become a dealer", "href": "support/become-a-dealer.html"}},
    ]})
TO_CONFIRM += [
    "Dealer playbook: title, chapters, cover, gate fields, consent wording, sender address and download link are all placeholders. DMP to decide whether a playbook exists, who writes it and where the file is hosted. The thank-you state is implemented locally on the page and nothing is sent.",
]

# ================================================================================================ trust center
STATED = [["done", "Stated by DMP"]]
CONF = [["confirm", "To confirm"]]
PAGES.append({
    "file": "trust.html",
    "title": "Trust center | Digital Monitoring Products",
    "description": desc("SOC 2 Type II, certifications, security and privacy contacts and a security FAQ, using only what DMP's pages state. Items not yet confirmed are marked."),
    "crumbs": [["Home", "index.html"], ["Trust center", "trust.html"]],
    "schema": [],
    "sections": [
        _hero("Trust center", "Security and privacy, <em>stated plainly.</em>",
              "What DMP says about its SOC 2 Type II examinations, certifications and contacts, in one place. Anything DMP has not yet confirmed is marked.",
              {"label": "Ask about the SOC reports", "href": "#start"}, {"label": "Our certifications", "href": "about/certifications.html"},
              IMG + "hq-exterior-2-1200.png", "The DMP headquarters entrance in Springfield, Missouri", 1200, 800),
        {"type": "p3tiles", "eyebrow": "SOC 2 Type II", "heading": "Independent examination, every year.", "cols": 3,
         "items": [{"tags": STATED, "title": "Examined every year", "text": "DMP completes independent SOC 2 Type II examinations annually, conducted by a licensed CPA firm in accordance with AICPA standards. They cover Dealer Admin and Virtual Keypad."},
                   {"tags": STATED, "title": "A SOC 3 report for everyone", "text": "The SOC 3 report is intended for public distribution."},
                   {"tags": CONF, "title": "Where to download the SOC 3", "text": "A public link to the SOC 3 report is not on the pages we read. DMP to supply it."},
                   {"tags": STATED, "title": "SOC 2 reports under confidentiality", "text": "SOC 2 reports are available to customers and partners under appropriate confidentiality arrangements. Inside Sales can route the question.", "link": ["Contact Inside Sales", "contact.html"]},
                   {"tags": STATED, "title": "Tier 4 data center", "text": "Dealer Admin and Virtual Keypad are hosted within a Tier 4 data center, designed for fully redundant subsystems and compartmentalized security zones."},
                   {"tags": STATED, "title": "Staff roles and single sign-on", "text": "Dealer Admin has a Single Sign-On option and Custom Roles that give staff only the authority they need.", "link": ["Dealer Admin", "products/dealer-admin.html"]}]},
        {"type": "p3tiles", "alt": True, "eyebrow": "Encryption and equipment", "heading": "What the product pages say.", "cols": 3,
         "intro": "Each statement below is made on the linked product page. This is not a complete security specification.",
         "items": [{"tags": STATED, "title": "263LTE communicators", "text": "NIST AES certification, #2350 for 128-bit and #2595 for 256-bit.", "link": ["263LTE", "products/263lte.html"]},
                   {"tags": STATED, "title": "SCS-1R and SCS-VR receivers", "text": "Both carry NIST AES certification.", "link": ["SCS-1R", "products/scs-1r.html"]},
                   {"tags": STATED, "title": "1100 Series wireless", "text": "AES encrypted since 2019, with two-way, supervised 900 MHz communication.", "link": ["Wireless", "services/wireless.html"]},
                   {"tags": STATED, "title": "XR550 control panel", "text": "AES encrypted communication options, including encrypted 10/100 network or Wi-Fi.", "link": ["XR550", "products/xr550.html"]},
                   {"tags": STATED, "title": "VAULT", "text": "A private, encrypted tunnel between a customer's network and SecureCom Wireless infrastructure, so systems stay off the public internet.", "link": ["Read about VAULT", "news/vault.html"]},
                   {"tags": STATED, "title": "JamAlert", "text": "Cellular jamming detection that has achieved UL 2610 certification.", "link": ["JamAlert", "products/jamalert.html"]}]},
        {"type": "p3tiles", "eyebrow": "Listings and approvals", "heading": "What DMP can state.", "cols": 2,
         "items": [{"tags": STATED, "title": "UL Listed combination panel since 1997", "text": "In 1997 DMP introduced a UL Listed combination burglary, fire and access control panel."},
                   {"tags": STATED, "title": "FirstNet", "text": "DMP offers communicators approved for the FirstNet mobile broadband public-safety network, and made the first alarm panel communicator for the AT&T FirstNet network."},
                   {"tags": STATED, "title": "Manufactured in the USA", "text": "Products are manufactured in Springfield, Missouri, with U.S. and global components."},
                   {"tags": STATED, "title": "The full list", "text": "Every certification DMP states is on one page, with the stories behind them.", "link": ["Certifications", "about/certifications.html"]}]},
        {"type": "p3tiles", "alt": True, "eyebrow": "Data handling", "heading": "Marked to confirm.", "cols": 3,
         "intro": "These are the questions a security reviewer asks. DMP's pages do not answer them yet, so we have not.",
         "items": [{"tags": CONF, "title": "Data retention", "text": "How long customer and dealer data is kept, and how it is deleted."},
                   {"tags": CONF, "title": "Where data is stored", "text": "The hosting location of the Tier 4 data center and any other regions."},
                   {"tags": CONF, "title": "Service providers", "text": "Which third parties process data for Dealer Admin and Virtual Keypad."},
                   {"tags": CONF, "title": "Incident response", "text": "How and when DMP tells customers about a security incident."},
                   {"tags": CONF, "title": "Reporting a vulnerability", "text": "A dedicated security contact and a disclosure process."},
                   {"tags": STATED, "title": "Website privacy", "text": "How dmp.com collects, uses and protects personal information is in the privacy policy, last updated January 2021.", "link": ["Privacy policy", "privacy-policy.html"]}]},
        {"type": "p3tiles", "eyebrow": "Contacts", "heading": "Who to ask.", "cols": 2,
         "items": [{"tags": STATED, "title": "Privacy questions", "text": "The privacy policy names info@dmp.com for questions about it.", "link": ["Email info@dmp.com", "mailto:info@dmp.com"]},
                   {"tags": STATED, "title": "SOC reports and sales", "text": "Inside Sales, 877-757-4367, 8 a.m. to 5 p.m. Central, InsideSales@DMP.com.", "link": ["Call 877-757-4367", "tel:+18777574367"]},
                   {"tags": STATED, "title": "Technical questions", "text": "Technical Support, 888-436-7832, 7 a.m. to 7 p.m. Central, TechSupport@DMP.com.", "link": ["Call 888-436-7832", "tel:+18884367832"]},
                   {"tags": CONF, "title": "Security contact", "text": "A dedicated security email address is not on the pages we read. DMP to supply one, or to say that Inside Sales handles it."}]},
        {"type": "resources", "alt": True, "eyebrow": "Policies", "heading": "The legal pages.",
         "items": [["Policy", "Privacy policy", "How we collect, use, disclose and protect personal information.", "Read the privacy policy", "privacy-policy.html"],
                   ["Policy", "Terms of use", "The terms that apply to your use of the website.", "Read the terms", "terms-of-use.html"],
                   ["Accessibility", "Accessibility statement", "Our target, the evidence so far and how to tell us about a problem.", "Read the statement", "accessibility.html"]]},
        {"type": "faq", "heading": "Security questions, answered from DMP's pages", "items": [
            ["What does the SOC 2 Type II examination cover?", "Dealer Admin and Virtual Keypad, DMP's SaaS applications, which are hosted within a Tier 4 data center."],
            ["Who examines it, and how often?", "A licensed CPA firm, in accordance with AICPA standards, every year."],
            ["Can I see the report?", "The SOC 3 report is intended for public distribution. SOC 2 reports are available to customers and partners under appropriate confidentiality arrangements. Inside Sales can route the request."],
            ["Is alarm communication encrypted?", "Where the product pages say so. For example the 263LTE communicators and the SCS-1R and SCS-VR receivers carry NIST AES certification, and the 1100 Series wireless line has been AES encrypted since 2019."],
            ["Is this a complete security statement?", "No. It repeats what DMP's own pages already state. Anything marked to confirm is not yet published."]]},
        _lead("Ask about the SOC reports", "Say who you are and what the project needs, and Inside Sales will reply about the SOC 2 and SOC 3 reports."),
    ]})
TO_CONFIRM += [
    "Trust center: every statement repeats existing DMP page data (certifications page, SOC 2 article, product pages). Marked to confirm: a public SOC 3 download link, a dedicated security or vulnerability-disclosure contact (only info@dmp.com for privacy, Inside Sales and Technical Support exist), data retention, hosting location, service providers and incident notification. The privacy policy shown was last updated January 2021 on dmp.com.",
]

# ================================================================================================ accessibility statement
PAGES.append({
    "file": "accessibility.html",
    "title": "Accessibility statement | Digital Monitoring Products",
    "description": desc("Our target is WCAG 2.2 AA. What has been checked so far, what is still to be done and how to tell us about a problem. No claim of full conformance."),
    "crumbs": [["Home", "index.html"], ["Accessibility statement", "accessibility.html"]],
    "schema": [],
    "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "Draft for the preview, 9 November 2026", "heading": "Accessibility statement",
         "subhead": "We are working toward WCAG 2.2 level AA. We do not claim full conformance."},
        {"type": "p3tiles", "eyebrow": "Evidence so far", "heading": "What has been checked, and what has not.", "cols": 2,
         "items": [{"tags": [["done", "Done in the preview"]], "title": "Automated checks", "text": "axe-core run on the preview at 390 and 1440 wide with zero color-contrast or critical violations on the sampled pages."},
                   {"tags": [["confirm", "To be completed before launch"]], "title": "Manual testing", "text": "Manual testing with a keyboard and assistive technology is to be completed before launch. Until it is done, this page claims nothing more."}],
         "note": "Automated checks find only part of the problems that exist. They do not replace manual testing."},
        {"type": "cards", "alt": True, "eyebrow": "Built in so far", "heading": "What the new tools already do.",
         "items": [["Keyboard and focus", "The system-fit check, the savings estimator, the playbook form and the consent banner can be used with a keyboard and show a visible focus ring."],
                   ["Reduced motion", "Count-ups, the score ring and the banner entrance switch off when your device asks for reduced motion."],
                   ["No script", "The system-fit check lists all of its questions as a plain checklist when JavaScript is off."]]},
        {"type": "detail", "eyebrow": "Feedback", "heading": "Tell us if something does not work.",
         "body": "If a page or a tool is hard to use, contact Inside Sales on 877-757-4367, 8 a.m. to 5 p.m. Central, or at InsideSales@DMP.com, or use the contact page. Say which page and what got in the way.",
         "bullets": ["Inside Sales: 877-757-4367", "InsideSales@DMP.com", "The contact page"], "cta": {"label": "Contact DMP", "href": "contact.html"},
         "image": IMG + "phone-commercial-1200.jpg", "image_alt": "A person checking a phone as they walk out of a building", "image_w": 1200, "image_h": 800},
        {"type": "faq", "alt": True, "heading": "Questions about accessibility", "items": [
            ["Is the site fully WCAG 2.2 AA conformant?", "We have not claimed that. WCAG 2.2 AA is the target. The evidence so far is the automated check described above, and manual testing is still to come."],
            ["Does this cover buy.DMP.com?", "No. The dealer ordering site is a separate system and is not described on this page."],
            ["Where does the legal side sit?", "The privacy policy and terms of use are linked in the footer and in the trust center."]]},
        _lead("Report an accessibility problem", "Say which page you were on and what got in the way, and a person will reply.", "Inside Sales is 877-757-4367, 8 a.m. to 5 p.m. Central."),
    ]})
TO_CONFIRM += [
    "Accessibility statement: target WCAG 2.2 AA with no conformance claim. Automated evidence is our own axe-core run on the preview (390 and 1440 wide); manual testing is to be completed before launch. DMP to confirm the feedback contact (we used Inside Sales and the contact page), a response-time commitment and any legal review of the wording.",
]

# ================================================================================================ 404 and consent banner
PAGES.append({
    "file": "404.html",
    "title": "Page not found | Digital Monitoring Products",
    "description": "The page was not found. Search the site, try a top link or call Inside Sales.",
    "crumbs": [["Home", "index.html"], ["Page not found", "404.html"]],
    "schema": [],
    "sections": [
        {"type": "p3nf", "heading": "That page was not found.", "body": "The link may be old, or the page may have moved. Search the site, try one of these, or call a person.",
         "links": [["Products", "services.html"], ["Find a system", "find-a-system.html"], ["Dealer system-fit check", "assessment.html"], ["Find a dealer", "find-a-dealer.html"],
                   ["Support", "support.html"], ["For dealers", "for-dealers.html"], ["Blog", "blog.html"], ["Contact", "contact.html"]]},
        {"type": "cta", "alt": True, "heading": "Tell us what you were looking for.", "subhead": "A person at DMP can point you to the right page.", "primary": {"label": "Contact DMP", "href": "contact.html"}},
    ]})
TO_CONFIRM += [
    "404 page: links are relative to the page's folder in this preview. On the live site the server returns this page for any missing URL, so its links and assets must be root-relative.",
    "Consent banner: a preview-only mock (Accept all, Reject non-essential, Preferences, choice kept in the browser's localStorage). The live site is to use HubSpot's consent tool, so the real categories, wording and region rules are DMP's to confirm. The preview labels itself as such on the banner.",
]
