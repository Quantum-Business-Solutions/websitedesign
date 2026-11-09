#!/usr/bin/env python3
"""Digital Monitoring Products (dmp.com): three website directions, version 2.

Sourcing note. Version 1 (9 Nov 2026) was written blind from sitemap slugs and the September SEO analysis, because the
apex dmp.com redirects and the first crawl could not read the pages. Version 2 was written from www.dmp.com itself,
read on 9 Nov 2026: the home, About us, Certifications, Products, Support and product pages, the sitemap, robots.txt,
the page images and the stylesheet (brand yellow, black and beige). Every name, number, date and quotation below comes
from one of those. Anything that did not is on pitch["confirm"]. DMP's own wording is used wherever a claim is
DMP's to make (the 1975 founding, the innovation list, "Manufactured in the USA with U.S. and global components").

Run:  python3 brands/digital-monitoring-products.content.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "digital-monitoring-products.content.json")

CLIENT = "Digital Monitoring Products"
SHORT = "DMP"
SITE = "https://www.dmp.com"
PHONE, PHONE_HREF = "877-757-4367", "tel:+18777574367"        # Inside Sales, as published on dmp.com/support
EMAIL = "InsideSales@DMP.com"
BUY = "https://buy.dmp.com/dmp/Shop"
DOCS = "support/documentation.html"
SUPPORT = "support.html"
FOUNDED = "1975"
IMG = "assets/"

# -------------------------------------------------------------- real product names, with their dmp.com page
def P(path):
    return SITE + "/products/" + path


# slug, nav label, short, one-line, hero image, eyebrow, heading, subhead, what-to-know [[t,b]], range bullets, faq, products [[kicker,name,desc,url]], category url, detail image, detail alt
SERVICES = [
    ["intrusion", "Intrusion Systems", "intrusion systems",
     "Control panels, detectors and cellular-jam protection for intrusion alarm systems.",
     IMG + "xt75-1200.png", "Intrusion",
     "Intrusion panels that <em>grow with the site</em>.",
     "We build intrusion around the control panel. The XT Series, XTL Series and XR Series scale from a small business to a large site, and every one reports through our own communicators.",
     [["Hybrid by design", "The XT75 is a hybrid intrusion panel for residential or small business applications. It integrates intrusion, access control and AlarmVision on one panel."],
      ["Scales up", "The XR550 supports 96 doors of access control, and the XR650 won top honors at the 2026 ESX Innovation Awards."],
      ["Built against false alarms", "Cancel/Verify false alarm prevention has been a DMP feature since 2007. Video verification and AlarmVision add a second look."]],
     ["XT30, XT50 and XT75 control panels", "XTLplus and XTLtouch residential panels", "XR150, XR550 and XR650 panels", "TMSentry compact panel for teller machine security", "Motion, glassbreak, contact and wireless detectors", "JamAlert cellular jamming detection"],
     [["Which intrusion panels does DMP make?", "The XT30, XT50, XT75, XTLplus, XTLtouch, XR150, XR550 and XR650, plus the TMSentry compact panel for teller machines. Each has its own page."],
      ["What is a hybrid intrusion panel?", "One panel that runs intrusion and access control together, so doors and alarm zones share a single system. The XT75 is one."],
      ["What is cellular jamming?", "An attempt to block the cellular signal an alarm uses to report. Our JamAlert product detects it."],
      ["Does DMP sell alarm systems to building owners?", "We sell through authorized dealers and distributors. Owners start with a DMP dealer."]],
     [["Control panel", "XT75", "Hybrid intrusion panel for residential or small business applications, with intrusion, access control and AlarmVision on one panel.", P("control-panels/xt-series/xt75")],
      ["Control panel", "XT50", "From the XT Series, the line we introduced in 2008 as the first panel with built-in wireless receiver and network, cellular and dialer communications.", P("control-panels/xt-series/xt50")],
      ["Control panel", "XR150", "XR Series panel. We introduced the XR Series in 2013, and it is 32 times faster than the generation before.", P("control-panels/xr-series/xr150")],
      ["Control panel", "XR550", "XR Series panel with 96 doors of access control, introduced in 2015.", P("control-panels/xr-series/xr550")],
      ["Control panel", "XR650", "XR Series panel and 2026 ESX Innovation Awards winner.", P("control-panels/xr-series/xr650")],
      ["Residential", "XTLplus", "Second generation residential panel, introduced in 2016.", P("control-panels/xtl-series/xtlplus")],
      ["Residential", "XTLtouch", "Enhanced all-in-one solution introduced in 2018.", P("control-panels/xtl-series/xtltouch")],
      ["Banking", "TMSentry", "Compact control panel developed for teller machine security.", P("control-panels/tmsentry/tmsentry")],
      ["Detection", "JamAlert", "Cellular jamming detection, introduced in 2025.", P("intrusion/jamalert/jamalert")]],
     SITE + "/products/intrusion", IMG + "cell-jammers-1200.jpg", "A JamAlert device shown over a cell tower and skyline"],
    ["access-control", "Access Control", "access control",
     "Access control from a stand-alone cloud system to the Entré enterprise software.",
     IMG + "x1-1200.jpg", "Access control",
     "Your doors and your alarm, <em>on one system</em>.",
     "We make the controllers, readers, credentials and software, so a door, an alarm zone and a camera can sit on one platform. The newest credential lives in a phone's wallet.",
     [["A key in the phone", "Digital Key adds a credential to an Apple or Google device's mobile wallet, so the smartphone works as a secure, contactless credential. No fob to track."],
      ["Cloud or on site", "The X1 Series, introduced in 2021, is stand-alone cloud-based access control. Entré software comes in Lite, Business and Enterprise editions, plus Entré NOC."],
      ["Open standards", "In 2020 we added OSDP, BIN code and 1100 Series wireless support to our access control modules."]],
     ["X1 Series controllers, PoE and expansion modules", "Entré Lite, Business, Enterprise and NOC software", "734, 734N and 734N PoE access modules", "Bluetooth and multi-technology readers", "Digital Key and mobile credentials, prox cards and keys"],
     [["What is an access control system?", "A system that decides who can open which door and when, and keeps a record. We make the controllers, readers, credentials and software for one."],
      ["What is Digital Key?", "A credential that sits in an Apple or Google device's mobile wallet, so a phone can open a door. It is our product."],
      ["Does access control work with the alarm?", "Yes. Our XR and XT75 panels run intrusion and access control together, and Entré software manages the doors."],
      ["Is there access control without a server?", "The X1 Series is our stand-alone, cloud-based access control solution."]],
     [["Credential", "Digital Key", "Adds a credential to an Apple or Google device's mobile wallet. Access control beyond the fob.", P("access-control/credentials/digital-key-credential")],
      ["Cloud access", "X1 Series", "Stand-alone, cloud-based access control, introduced in 2021.", P("access-control/x1/x1")],
      ["Software", "Entré Enterprise", "The top of the Entré family, built for larger access control systems.", P("entr%C3%A9-software/access-control-software/entr%C3%A9-enterprise")],
      ["Software", "Entré Lite", "The entry edition of Entré access control software.", P("entr%C3%A9-software/access-control-software/entr%C3%A9-lite")],
      ["Module", "734 and 734N", "Access control modules for DMP panels, with an encrypted version.", P("access-control/modules/734n")],
      ["Reader", "Bluetooth reader and mobile credential", "Our Bluetooth reader, built for mobile credentials.", P("access-control/readers/dmp-bluetooth-reader-and-mobile-credential")]],
     SITE + "/products/access-control", IMG + "digital-key-1200.jpg", "A hand holding a phone to a door reader"],
    ["fire", "Fire Systems", "fire systems",
     "Fire alarm control panels, detectors and communicators.",
     IMG + "xf6-installed-1200.jpg", "Fire",
     "Fire panels that <em>report the way the alarm does</em>.",
     "The XF6 fire control panel is built for single-site applications and comes with network and optional cellular communications that send all signals directly to the monitoring center.",
     [["A 24V solution", "The XF6 is a 24V solution with powerful testing and programming features, built for single-site applications."],
      ["Reports the same way", "Network and optional cellular communications are on the panel, so fire signals take the path the rest of the system uses."],
      ["Beyond one panel", "XR150FC and XR550FC fire panels, wireless smoke, heat and CO detectors, pull stations and remote annunciators sit in the same catalogue."]],
     ["XF6, XR150FC and XR550FC fire control panels", "Smoke detectors, pull stations and remote annunciators", "Wireless smoke, heat and CO detectors", "PowerCom Fire communicators, including FirstNet-ready", "Graphic remote annunciators"],
     [["Which fire control panels does DMP make?", "The XF6 fire control panel and the XR150FC and XR550FC fire panels. Our product pages list the detectors, pull stations and annunciators that go with them."],
      ["Can a fire panel report by cellular?", "The XF6 comes with network and optional cellular communications that send signals directly to the monitoring center."],
      ["What is a central station fire alarm system?", "A fire alarm that reports to a monitoring center, which then dispatches the fire service. Our panels and communicators send those signals."],
      ["Who installs DMP fire systems?", "Authorized DMP dealers do. We sell through dealers and distributors."]],
     [["Fire panel", "XF6", "A 24V fire control panel for single-site applications, with network and optional cellular communications.", P("fire/fire-control-panels/xf6")],
      ["Fire panel", "XR550FC", "Fire panel from the XR Series.", P("fire/fire-control-panels/xr550fc-2")],
      ["Fire panel", "XR150FC", "Fire panel from the XR Series.", P("fire/fire-control-panels/xr150fc-2")],
      ["Detector", "2W-BLX smoke detector", "A smoke detector for DMP fire systems.", P("fire/smoke-detectors/2w-blx")],
      ["Initiating", "850 pull station", "A manual pull station.", P("fire/pull-stations/850")],
      ["Annunciator", "630F remote annunciator", "Remote annunciator for fire systems.", P("fire/remote-annunciators/630f")]],
     SITE + "/products/fire", IMG + "firetruck-1200.jpg", "The back lights of a fire truck"],
    ["video", "Video", "video",
     "VUE Plus cameras, AlarmVision analytics and the VK VMS video management platform.",
     IMG + "vue-plus-1200.jpg", "Video",
     "Cameras that <em>trigger the alarm</em>, not just record it.",
     "Our VUE Plus cameras, XV gateways and VK VMS give video the same accounts, apps and monitoring as the alarm, with AlarmVision analytics that raise alarms into XR Series panels.",
     [["Analytics that alarm", "The XV-24 with AlarmVision, introduced in 2023, uses analytics to trigger alarms into XR Series panels."],
      ["A complete platform", "In September 2026 we launched VK VMS for 24/7 video management with AlarmVision. It makes DMP video a complete platform."],
      ["One app", "Camera drivers for AlarmVision and Virtual Keypad put cameras beside the alarm in the apps dealers already use."]],
     ["VUE Plus cameras: bullet, turret, dome and fisheye", "VUE video doorbell", "V-6000, V-5000 and V-4000 series cameras", "XV gateways with AlarmVision", "VK VMS video management"],
     [["What video products does DMP make?", "The VUE Plus camera line, the VUE video doorbell, the V-6000, V-5000 and V-4000 series cameras, XV gateways with AlarmVision and the VK VMS platform."],
      ["What is AlarmVision?", "Our video analytics. It uses analytics to trigger alarms into XR Series panels."],
      ["What is a VMS?", "Video management software: the system that records, plays back and manages many cameras. VK VMS is ours."],
      ["Where do I see live video?", "In our mobile platforms, including Virtual Keypad, which supports camera drivers."]],
     [["Camera", "VUE Plus 8MP varifocal bullet", "From the VUE Plus line we launched in 2026.", P("video/vue-cameras/vplus-7081-bdv")],
      ["Camera", "VUE Plus 12MP fisheye", "A fisheye camera in the VUE Plus line.", P("video/vue-cameras/vplus-7121-fe")],
      ["Camera", "VUE Plus 6MP fisheye", "A fisheye camera in the VUE Plus line.", P("video/vue-cameras/vplus-7061-fe")],
      ["Doorbell", "VUE video doorbell", "A video doorbell in the VUE line.", P("video/vue-cameras/vue-video-doorbell")],
      ["Gateway", "XV gateways with AlarmVision", "The hardware that brings AlarmVision analytics to the platform.", P("video/alarmvision/xv-gateways-with-alarmvision")],
      ["Camera", "V-6000 series", "Cameras for larger video installations.", P("video/v-6000-series-cameras/v-6022wc")]],
     SITE + "/products/video", IMG + "alarmvision-1200.jpg", "An AlarmVision scenario: two people highlighted in a camera frame"],
    ["communicators", "Communicators and Monitoring", "communicators and monitoring",
     "Cellular, network and universal communicators, and the monitoring center equipment that receives them.",
     IMG + "dualsim-1200.jpg", "Communicators",
     "The alarm signal gets <em>more than one way out</em>.",
     "Our communicators carry alarm signals over LTE, network and Wi-Fi paths, including the first alarm panel communicator for the AT&T FirstNet network. On the other end, we build the receiver.",
     [["First for FirstNet", "In 2020 we introduced the first alarm panel communicator for the AT&T FirstNet network."],
      ["More than one path", "The ComSeries universal LTE and LTE/network communicators arrived in 2019. Cellular, network and Wi-Fi communicators sit in one category."],
      ["Both ends of the link", "We built the first software-only central station receiver, SCS-VR, in 2009, and still offer SCS receivers and line cards."]],
     ["263LTE and 265LTE cellular communicators", "Cell Com, Dual Com and PowerCom universal communicators", "763 Wi-Fi network communicator", "SCS-VR virtual receiver software, SCS-1R receiver and line cards", "VAULT encrypted connectivity for cloud-based applications"],
     [["What does a communicator do?", "It carries the alarm signal from the panel to the monitoring center, over cellular, network or both."],
      ["What is FirstNet?", "The AT&T network built for first responders. We made the first alarm panel communicator for it, in 2020."],
      ["What is SCS-VR?", "Our virtual receiver software. We introduced it in 2009 as the first software-only central station receiver."],
      ["What is VAULT?", "Our secure, encrypted connectivity for cloud-based security applications, introduced in October 2025."]],
     [["Cellular", "263LTE", "LTE communicator for XT and XR Series panels.", P("cell-network-communicators/xt-xr-series-communicators/263lte")],
      ["Cellular", "265LTE", "LTE communicator for the XTL Series.", P("cell-network-communicators/xtl-series-communicators/265lte")],
      ["Universal", "Dual Com", "A universal communicator.", P("cell-network-communicators/universal-communicators/dualcom")],
      ["Universal", "Cell Com", "Universal LTE communicator.", P("cell-network-communicators/universal-communicators/cellcom")],
      ["Monitoring center", "SCS-VR virtual receiver", "Software-only central station receiver.", P("monitoring-center/monitoring-center-software/scs-vr-virtual-receiver-software")],
      ["Monitoring center", "SCS-1R receiver", "A hardware receiver for the monitoring center.", P("monitoring-center/receivers/scs-1r")]],
     SITE + "/products/cell-network-communicators", IMG + "vault-1200.jpg", "A glowing shield with a padlock"],
    ["wireless", "Wireless", "wireless security",
     "The 1100 Series wireless line: transmitters, detectors, receivers and translators.",
     IMG + "jamalert-1200.jpg", "Wireless",
     "Encrypted two-way wireless <em>that upgrades what is already installed</em>.",
     "We have made two-way wireless since 2004. The 1100 Series added AES encryption in 2019, and the 1100T and 1100TF translators let a dealer upgrade a competitor's wireless transmitters without rewiring.",
     [["AES encrypted", "Our 1100 Series wireless has been AES encrypted since 2019."],
      ["Upgrade without rewiring", "The 1100T and 1100TF translators, introduced in 2021, allow upgrade of competitors' wireless transmitters."],
      ["The whole zone list", "Door and window inputs, motion and glassbreak detectors, panic and holdup devices, smoke, heat and CO detectors, sounders and remote controls."]],
     ["1100 receivers and repeaters", "1100T and 1100TF wireless translators", "Door, window and zone inputs", "Motion and glassbreak detectors", "Panic and holdup devices", "Smoke, heat and CO detectors", "Sounder outputs and remote controls"],
     [["What is two-way wireless?", "Devices that both send and receive, so the panel can check them. We introduced Two-Way wireless in 2004."],
      ["Can I upgrade another manufacturer's wireless?", "The 1100T and 1100TF translators were introduced in 2021 to upgrade competitors' wireless transmitters."],
      ["Is DMP wireless encrypted?", "Yes. Our 1100 Series wireless has been AES encrypted since 2019."],
      ["Which wireless devices does DMP make?", "Zone inputs, detectors, panic devices, sounders, remote controls, receivers and translators. Each has its own page."]],
     [["Receiver", "1100XH", "An 1100 Series receiver and repeater.", P("wireless/receivers-repeaters/1100xh")],
      ["Translator", "1100T", "Lets a dealer upgrade a competitor's wireless transmitters.", P("wireless/wireless-translators/1100t")],
      ["Zone input", "1101", "A wireless door and window input.", P("wireless/door-window-zone-inputs/1101")],
      ["Detector", "1128 glassbreak", "A wireless glassbreak detector.", P("wireless/glassbreak-detectors/1128")],
      ["Panic", "1142", "A wireless panic and holdup device.", P("wireless/panic-holdup/1142")],
      ["Detector", "1164 smoke", "A wireless smoke detector.", P("wireless/smoke-heat-co-detectors/1164")]],
     SITE + "/products/wireless", IMG + "xt75-600.png", "The DMP XT75 control panel"],
    ["panels-keypads", "Panels and Keypads", "panels and keypads",
     "Control panels, keypads, modules, expanders, power supplies and enclosures.",
     IMG + "keypad-722-1200.png", "Hardware",
     "Start with the panel. <em>Finish at the keypad.</em>",
     "Control panels, keypads, modules and expanders, power supplies and enclosures are each their own category. The keypads range from a 7-inch touchscreen to the Thinline and Aqualite series.",
     [["A keypad for every wall", "7-inch and 5-inch touchscreen keypads, 9800, Thinline, Aqualite and Icon series."],
      ["Modules and expanders", "Zone, output and auxiliary modules extend a panel to the size of the building."],
      ["The rest of the cabinet", "Power supplies, transformers, batteries and enclosures complete the install."]],
     ["7-inch and graphic touchscreen keypads", "9800, Thinline, Aqualite and Icon series keypads", "Modules and expanders", "Power supplies, batteries and transformers", "Enclosures and mounting plates"],
     [["How do I choose a panel?", "Start from the building, the zones and the doors, then match the panel family. A DMP dealer does this, and our Inside Sales team supports system design."],
      ["What keypads does DMP make?", "Touchscreen keypads (a sleek 7-inch and a 5-inch graphic), and the 9800, Thinline, Aqualite and Icon series."],
      ["Where are the spec sheets?", "On each product page and in our technical documentation library."],
      ["Are there international versions?", "Yes. Our global page lists international products."]],
     [["Keypad", "7-inch touchscreen keypad", "A sleek, thin 7-inch touchscreen keypad introduced in 2023.", P("keypads/touchscreen/7-inch-touchscreen-keypad")],
      ["Keypad", "Graphic touchscreen keypad", "A 5-inch full-color touchscreen with a carousel menu, introduced in 2013.", P("keypads/touchscreen/graphic-touchscreen")],
      ["Keypad", "9800 series", "Touchscreen keypads.", P("keypads/touchscreen/9800-series")],
      ["Keypad", "Thinline 7000 series", "Thinline keypads, introduced in 2004.", P("keypads/thinline/7000-series")],
      ["Keypad", "Aqualite series", "Aqualite keypads.", P("keypads/aqualite/aqualite-series")],
      ["Keypad", "Icon series", "Icon keypads.", P("keypads/icon-series/icon-series")]],
     SITE + "/products/keypads", IMG + "xt75-600.png", "The DMP XT75 control panel"],
    ["mobile-automation", "Virtual Keypad and Software", "Virtual Keypad and software",
     "Virtual Keypad, Dealer Admin, Entré, Z-Wave automation and the cloud services behind them.",
     IMG + "vk-mock-1200.png", "Software",
     "The owner's remote. <em>The dealer's programming tool.</em>",
     "Virtual Keypad lets dealers brand a full-featured remote control for their customers. Dealer Admin programs panels in bulk. Both are hosted in a Tier 4 data center and examined annually for SOC 2 Type II.",
     [["Virtual Keypad", "Introduced in 2011 as an app dealers could brand. Rebuilt in 2018 for iOS and Android, with browser-based control at VirtualKeypad.com since 2017."],
      ["Dealer Admin", "Mass panel programming and bulk firmware update arrived in 2019, with auto-programming and pre-programming templates in 2022."],
      ["Examined every year", "We complete independent SOC 2 Type II examinations annually, by a licensed CPA firm. The SOC 3 report is public."]],
     ["Virtual Keypad for iOS, Android and the browser", "Mobile wallet credentials in Virtual Keypad", "Dealer Admin for programming and firmware", "Remote Link and Tech APP", "Z-Wave lights, locks and thermostats"],
     [["What is Virtual Keypad?", "Our remote control app: the system keypad on a phone. Dealers can brand it, and it has a browser version."],
      ["What is Dealer Admin?", "The dealer's tool for programming panels, including mass programming and bulk firmware updates."],
      ["Is our software secure?", "Dealer Admin and Virtual Keypad are hosted in a Tier 4 data center, and we complete independent SOC 2 Type II examinations every year."],
      ["Does DMP support home automation?", "Z-Wave technology has been integrated with XTL and XT Series panels since 2012."]],
     [["Mobile", "Virtual Keypad", "The remote control app, with mobile wallet credentials added in 2024.", P("mobile-platforms/end-user-apps/virtual-keypad")],
      ["Dealer tool", "Dealer Admin", "Programming, firmware and templates for dealers.", P("mobile-platforms/dealer-apps/dealer-admin")],
      ["Dealer tool", "Remote Link", "Dealer software for remote panel connection.", P("mobile-platforms/dealer-apps/remote-link")]],
     SITE + "/products/mobile-platforms", IMG + "phone-commercial-1200.jpg", "A person checking a phone as they walk out of a building"],
]

# Written from DMP's own industry pages (dmp.com/products/industries/*), read 9 Nov 2026.
# slug, name, hero image, headline, why (DMP's words, condensed), bullets, featured [[kicker, name, desc, url]], library titles, contact role, faq
IND = SITE + "/products/industries/"
IND_H1 = {"commercial": "A system that does more <em>than sound an alarm</em>.",
          "financial-institutions": "A security system that <em>also helps run the branch</em>.",
          "retail": "Run every store's system <em>with one action</em>.",
          "government": "Designed and built in the U.S.A. <em>for government customers</em>.",
          "industrial-manufacturing": "Intrusion and access, <em>one system, no extra wiring</em>.",
          "education": "Lock every public door <em>in one action</em>.",
          "healthcare-wellness": "Protect the building <em>and the records inside it</em>.",
          "multi-tenant": "A phone for a key. <em>A pool-only access level.</em>",
          "religious-institutions": "<em>100 percent</em> of DMP products are tested before shipping.",
          "storage-units": "Many panels. One site. <em>One command.</em>",
          "residential": "Home, Sleep, Away: three arming levels, <em>one touch</em>."}
INDUSTRIES = [
    ["commercial", "Commercial", IMG + "hq-exterior-2-1200.png", "Scalable, convenient solutions for commercial customers.",
     "A security system should do much more than just sound an alarm when there's an intrusion. High-functioning systems provide a blanket of security with features and functions that enable commercial customers to protect their employees, facilities and businesses more effectively. Our systems are designed with employees and service providers in mind, so keypads are easy to operate regardless of experience level.",
     ["XR550 Series: up to eight communication paths between the panel and the monitoring service", "DMP Adaptive Technology moves communication from the primary to a backup path instantly", "XT Series: network, cellular and dial-up communications all on board", "Intrusion, fire, access, wireless and video from one manufacturer"],
     [["Featured", "XR550 Series", "Create, configure and manage up to eight communication paths between the panel and the monitoring service.", P("control-panels/xr-series/xr550")],
      ["Featured", "XT Series", "A complete set of communications options in an all-on-board design for faster, easier installation.", SITE + "/products/control-panels"]],
     [], None,
     [["What does DMP offer commercial customers?", "Intrusion, fire, access, wireless and video, with the XR550 supporting up to eight communication paths and the XT Series carrying network, cellular and dial-up communications on board."]]],
    ["financial-institutions", "Financial institutions", IMG + "vault-1200.jpg", "A security system plus operational management.",
     "Our systems streamline credentialing through integrated access control and intrusion, reduce labor through automated reporting and simplified credential administration, simplify compliance audits, and reduce service calls and false alarms.",
     ["128-bit or 256-bit AES encryption secures alarm communications across the network, and from the panel to each duress and access device", "VAULT: a secure, private, encrypted site-to-site connection to the SecureCom infrastructure, so security panels never touch the public internet", "Security Command: cloud-based security, access control and video management with no servers to buy, update or maintain", "TMSentry: a compact panel developed for teller machine security"],
     [["Featured", "VAULT", "Virtual Access Using Layered Tunneling: an encrypted, site-to-site connection built for organizations where protecting data is critical.", SITE + "/resources/news-updates/dmp-introduces-vault"],
      ["Featured", "Security Command", "A cloud-based security, access control and video management platform for enterprise end users, built on our Dealer Admin and Virtual Keypad cloud products.", IND + "financial-institutions"],
      ["Featured", "TMSentry", "A compact control panel developed for teller machine security.", P("control-panels/tmsentry/tmsentry")]],
     ["Why Banks Choose DMP (white paper)", "VAULT (white paper)", "Entré NOC (white paper)", "Put the Power of a Panic Button in the Hands of All Your Employees (white paper)", "Customers Who Need the Highest Data Security (white paper)", "Great Southern Bank testimonial"], "Executive Director of Financial Solutions",
     [["How do we protect alarm communications for banks?", "We offer 128-bit or 256-bit AES encryption across the network and from the panel to duress and access devices, and VAULT, an encrypted site-to-site connection that keeps panels off the public internet."]]],
    ["retail", "Retail", IMG + "tab-mobile-1200.jpg", "A security system plus business management.",
     "Our retail systems integrate access control and intrusion so one database manages user credentials, and come with cloud-based management software to run multiple systems across a national footprint with a single action and automated enterprise reporting.",
     ["Reduce false alarms from unattended deliveries and employee turnover", "Decrease service calls for battery replacements", "Virtual Keypad: enterprise-wide system and user management from a single screen", "1100 Series wireless receivers and a published compatibility guide"],
     [["Featured", "Virtual Keypad", "Enterprise-wide system and user management from a single screen.", P("mobile-platforms/end-user-apps/virtual-keypad")],
      ["Wireless", "1100 Series wireless", "AES encrypted wireless, with receivers and a compatibility guide for retail applications.", SITE + "/products/wireless"],
      ["Video", "VUE video doorbell", "A video doorbell with its own spec sheet for retail.", P("video/vue-cameras/vue-video-doorbell")]],
     ["How to Maximize Your Security for Multiple Locations (white paper)", "National Retail Security (white paper)", "Traffic Count Systems in Retail Applications (white paper)", "XR550 and XR150 spec sheets", "Monitoring Center Integration sales sheet", "1100 Series Wireless Receivers spec sheet and Compatibility Guide"], "Director of Retail Solutions",
     [["How do retailers manage many locations with DMP?", "Our cloud-based management software lets a retailer manage multiple systems across a national footprint with a single action, and Virtual Keypad handles enterprise-wide system and user management."]]],
    ["government", "Government", IMG + "keypad-722-1200.png", "Solutions for government customers.",
     "It's increasingly difficult to find products carrying the label 'Made in the USA,' but our technology is designed and built in the U.S.A. with U.S. and global components. We have a national network for installation and service and a division dedicated to government customers.",
     ["XR550E: built-in 256-bit AES encryption, communicating by network, digital dialer and LTE cellular, including AT&T FirstNet", "High-security touchscreen keypad with randomized digit location and a privacy filter", "MAGNASPHERE L2 Series High Security Sensors meeting UL 634 Level 2 for SCIFs and other secure applications, sold to dealers through DMP", "A published white paper on NDAA, BAA and TAA compliance"],
     [["Featured", "XR550E", "Built-in 256-bit AES encryption with network, dialer and LTE cellular communications, including FirstNet.", P("control-panels/xr-series/xr550")],
      ["Featured", "MAGNASPHERE L2 Series", "High Security Sensors that meet UL 634 Level 2 standards, available to dealers through DMP.", IND + "government"],
      ["Featured", "High-security touchscreen keypad", "Randomized digit location protects user codes, and a privacy filter restricts visibility to intended users.", P("keypads/touchscreen/7-inch-touchscreen-keypad")]],
     ["NDAA, BAA and TAA Compliance (white paper)", "NISPOM 5 313 Detailed Statement of Compliance (letter)", "Encrypted Cellular Communications for SCIF Installation (sheet)", "Network Security is Serious Business (white paper)", "SCIF Install Layout", "Isolation Transformer Kit and Expansion Module spec sheets"], "Executive Director of Government Solutions",
     [["Is DMP made in the USA?", "Our technology is designed and built in the U.S.A. with U.S. and global components, and we have a division dedicated to government customers."]]],
    ["industrial-manufacturing", "Industrial and manufacturing", IMG + "x1-1200.jpg", "Robust systems for complex facilities.",
     "With an integrated system that supports intrusion, access control, commercial fire and video, you get the full benefit of multiple security features working together.",
     ["XR Series panels communicate with X1 access control units without any additional wiring", "Manage intrusion and access control together in one unified solution", "Encrypted local and cloud communications", "AlarmVision turns cameras into smart motion detectors that trigger panel responses and alarms in real time"],
     [["Featured", "XR to X1", "XR Series panels communicate with X1 access control units without any additional wiring.", P("access-control/x1/x1")],
      ["Featured", "XV gateways with AlarmVision", "Integrates cameras, analytics and XT75 or XR Series control panels in one platform.", P("video/alarmvision/xv-gateways-with-alarmvision")]],
     [], None,
     [["Can intrusion and access control run together?", "Yes. XR Series panels communicate with X1 access control units without additional wiring, so both are managed in one unified solution."]]],
    ["education", "Education", IMG + "digital-key-1200.jpg", "Monitoring for school security.",
     "We provide a broad line of security hardware and software that can be configured into a customized solution, with features tailored to protecting school facilities.",
     ["XR550: an integrated panel that combines access, intrusion, fire and video in one system", "Mobile wallet credentials: students and staff use their smartphones as access credentials", "Lockdown: authorized staff can start a lockdown from the Virtual Keypad app, a system keypad or any PC running Entré software, which locks all public doors and restricts access to authorized users"],
     [["Featured", "XR550", "An integrated panel that combines access, intrusion, fire and video security functions in a single system.", P("control-panels/xr-series/xr550")],
      ["Featured", "Mobile wallet credentials", "A convenient, powerful access control solution for campuses: the phone is the credential.", P("access-control/credentials/mobile-credential")]],
     [], None,
     [["What is the lockdown feature?", "Authorized staff can start a lockdown from the Virtual Keypad app, a system keypad or any PC connected to Entré software. It instantly locks all public doors and restricts access to authorized users."]]],
    ["healthcare-wellness", "Healthcare and wellness", IMG + "dualsim-1200.jpg", "Security for healthcare providers.",
     "Healthcare providers have the additional responsibility of securing patients' protected health information, as required by the HIPAA Privacy Rule, and every business needs to protect property from intrusion.",
     ["XR550: an integrated panel with access, intrusion, fire and video, built for environments where encrypted data is required", "Communication by network, digital dialer and LTE cellular, including AT&T FirstNet", "We offer communicators approved for use on the FirstNet public-safety network"],
     [["Featured", "XR550", "An integrated panel that communicates via network, digital dialer and LTE cellular, including FirstNet.", P("control-panels/xr-series/xr550")],
      ["Featured", "FirstNet communicators", "Communicators approved for the FirstNet public-safety broadband network.", P("cell-network-communicators/xt-xr-series-communicators/263lte-firstnet")]],
     [], None,
     [["What is FirstNet?", "The nationwide public-safety broadband network. We offer communicators approved for it, which gives alarm companies a more reliable network experience than a commercial wireless network."]]],
    ["multi-tenant", "Multi-tenant", IMG + "digital-key-1200.jpg", "Security solutions for multi-dwelling units.",
     "Systems built from our components combine intrusion with fire protection, access control and video. With the Virtual Keypad app, customers can control their systems remotely, along with locks, lights, thermostats and more.",
     ["Mobile wallet credentials for residents and staff", "Virtual Keypad's Access Only user: basic access without viewing events or video, changing door lock status or receiving push notifications", "Suited to pools, fitness centers, community rooms and other private amenities"],
     [["Featured", "XR550", "An integrated panel that combines access, intrusion, fire and video in one system.", P("control-panels/xr-series/xr550")],
      ["Featured", "Mobile wallet credentials", "Residents and staff use their smartphones as access credentials.", P("access-control/credentials/mobile-credential")]],
     [], None,
     [["What is an Access Only user?", "A Virtual Keypad user role that grants basic access without the ability to view events or video, change door lock status or receive push notifications, suited to amenities such as pools and fitness centers."]]],
    ["religious-institutions", "Religious institutions", IMG + "tab-intrusion-1200.jpg", "Rock-solid reliability.",
     "As a leading security manufacturer, we build products known for consistent reliability, and 100 percent of DMP products are quality tested before shipping.",
     ["XT75 integrates intrusion, access control and AlarmVision in a small footprint", "AlarmVision integrates cameras, analytics and XT75 or XR Series panels, creating smart motion detectors", "Complete, easy-to-manage systems that integrate intrusion, access control and video surveillance"],
     [["Featured", "XT75", "Seamlessly integrates intrusion, access control and AlarmVision for customers who need a robust system with a small footprint.", P("control-panels/xt-series/xt75")],
      ["Featured", "XV gateways with AlarmVision", "AlarmVision's technology integrates cameras, analytics and the panel in one platform.", P("video/alarmvision/xv-gateways-with-alarmvision")]],
     [], None,
     [["How reliable are DMP products?", "Our products are known for consistent reliability, and 100 percent of them are quality tested before shipping."]]],
    ["storage-units", "Storage units", IMG + "alarmvision-1200.jpg", "Designed for custom needs.",
     "Storage facilities have unique security needs, and our hardware and software are designed for flexible, scalable solutions that can be configured for any application.",
     ["XR to XR communication: panels across a single site work together over the same network", "Simultaneous arming and disarming, fire exits and site-wide lockdowns, with no additional wiring or install labor", "AlarmVision with XT75 or XR Series panels triggers responses in real time"],
     [["Featured", "XR to XR communication", "Seamless operation across multiple panels within a single site.", P("control-panels/xr-series/xr550")],
      ["Featured", "XV gateways with AlarmVision", "Cameras, analytics and panels in one platform, creating smart motion detectors.", P("video/alarmvision/xv-gateways-with-alarmvision")]],
     [], None,
     [["Can several panels work together at one site?", "Yes. XR Series panel-to-panel communication lets multiple panels operate together over the same network, with simultaneous arming, fire exits and site-wide lockdowns and no additional wiring."]]],
    ["residential", "Residential", IMG + "phone-commercial-1200.jpg", "Innovative solutions for residential customers.",
     "Systems built from our components combine intrusion with fire protection, and are surprisingly easy to use. With the Virtual Keypad app, customers can control the system remotely, along with locks, lights, thermostats and more.",
     ["Home/Sleep/Away: one-touch access to three arming levels", "False Alarm Question: silence an alarm while keeping the system armed, and cancel false alarms quickly", "XTLplus residential packages: all-wireless solutions for easy, flexible installation", "XTLtouch: the enhanced all-in-one wireless burglary panel"],
     [["Featured", "XTLtouch", "The enhanced all-in-one solution: fast installation, reliable security and ease of operation.", P("control-panels/xtl-series/xtltouch")],
      ["Featured", "XTLplus residential packages", "All-wireless solutions for easy, flexible installation.", P("control-panels/xtl-series/xtlplus")],
      ["Featured", "Virtual Keypad", "Control the system, locks, lights and thermostats from a phone.", P("mobile-platforms/end-user-apps/virtual-keypad")]],
     [], None,
     [["What residential features does DMP offer?", "Home/Sleep/Away arming levels, the False Alarm Question, all-wireless XTLplus packages and the XTLtouch panel, with Virtual Keypad for remote control."]]],
]

# 1975 to 2025, from the About us page of dmp.com. [year, title, description, image]
TIMELINE = [
    ["1975", "Atlas Security", "Rick Britton starts developing a central station product at Atlas Security. DMP begins as an R&D department.", IMG + "history-modular-600.jpg"],
    ["1979", "The first keypads", "Zone bypass, the alphanumeric keypad and the zone expansion keypad.", ""],
    ["1983", "Opening and closing", "A panel with opening and closing, and schedules stored in the panel.", ""],
    ["1993", "132 zones", "An expandable control panel with 132 zones.", IMG + "history-94-600.jpg"],
    ["1997", "Burglary, fire and access in one", "Our UL Listed combination burglary, fire and access panel.", ""],
    ["2004", "Two-Way wireless", "Two-Way wireless and the Thinline keypad series.", ""],
    ["2005", "Aqualite and Clear Touch", "Aqualite and Clear Touch keypads.", IMG + "team-2005-600.jpg"],
    ["2008", "The XT Series", "The first panel with a wireless receiver and network, cellular and dialer paths on board.", ""],
    ["2009", "SCS-VR", "The first software-only central station receiver.", ""],
    ["2011", "Virtual Keypad", "The app that lets dealers brand a full remote control.", ""],
    ["2013", "The XR Series", "XR Series panels, 32 times faster than before, and the first graphic touchscreen keypad.", ""],
    ["2021", "X1 Series", "Stand-alone, cloud-based access control.", IMG + "team-2021-600.jpg"],
    ["2024", "XT75 and TMSentry", "The XT75 bridges XT and XR, TMSentry arrives, and mobile wallet credentials join Virtual Keypad.", ""],
    ["2025", "JamAlert and the 50th", "Cellular jamming detection with JamAlert, and fifty years in business.", IMG + "fifty-600.jpg"],
]

VALUES = [
    ["Honesty and Integrity", "Tell the truth, even if it costs you something. Do what's right, especially when no one is watching."],
    ["Innovation and Initiative", "Always be learning. Creative solutions to customer needs are vital to our future."],
    ["Responsiveness", "Anticipate. Listen. Acknowledge. Deliver. Follow up. The best time to respond is yesterday. The second best time is now."],
    ["Kindness", "Think before you speak. Consider the feelings of others. Treat all with respect and courtesy."],
    ["Fun", "Work hard. Play hard. Live healthy. Share and celebrate every success."],
    ["Profit", "Profit is good. It's why we're in business. It secures jobs and fuels personal and corporate growth."],
]

LEADERS = [
    ["Rick Britton", "Chief Executive Officer"], ["Marc Mills", "Chief Operating Officer"], ["Gail Rogers", "Chief Financial Officer"],
    ["Mike Taylor", "Executive Vice President of Sales"], ["Ken Francis", "Executive Vice President of Video Solutions"],
    ["Michal Moss Early", "Executive Vice President of Corporate Strategy"], ["Brad Tucker", "Vice President of Product Management and Support"],
    ["Jeff Britton", "Vice President of Production"], ["Jody Chaffin", "Vice President of Software"], ["Dave Roberts", "Vice President of Cybersecurity"],
    ["Mark Hillenburg", "Vice President of Industry Relations"], ["Mark NeSmith", "Vice President of International Sales"],
]

ASSOCIATIONS = ["Security Industry Association", "Electronic Security Association", "The Monitoring Association", "Financial and Security Products Association",
                "Partnership for Priority Verified Alarm Response", "Z-Wave Alliance", "National Retail Federation", "NFPA", "CANASA"]

# [kicker, title, description, link label, url]: headlines and dates as posted on dmp.com
NEWS = [
    ["News, 11 Sep 2026", "DMP Launches VK VMS, Enabling 24/7 Video Management With AlarmVision", "Our video platform becomes complete, with VK VMS and the XV Plus gateways.", "Read the story", SITE + "/resources/news-updates/dmp-launches-vk-vms-enabling-24-7-video-management-with-alarmvision"],
    ["News, 1 Jul 2026", "The Next Evolution of the VUE Portfolio Is Here", "More cameras join the VUE Plus family.", "Read the story", SITE + "/resources/news-updates/the-next-evolution-of-the-vue-portfolio-is-here"],
    ["News, 6 May 2026", "JamAlert Achieves UL Certification", "JamAlert, our cellular jamming detection, earns a UL certification.", "Read the story", SITE + "/resources/news-updates/jamalert-achieves-ul-certification"],
    ["News, 27 Apr 2026", "XR650 Wins Top Honors at 2026 ESX Innovation Awards", "The XR650 control panel wins at the ESX Innovation Awards.", "Read the story", SITE + "/resources/news-updates/xr650-wins-top-honors-at-2026-esx-innovation-awards"],
    ["News, 9 Apr 2026", "DMP Launches VUE Camera Line Delivering Intelligent Video and Active Deterrence", "The VUE camera line arrives.", "Read the story", SITE + "/resources/news-updates/dmp-launches-vue-camera-line"],
    ["News, 19 Mar 2026", "Integration with System Surveyor Streamlines Intrusion and Access Control System Design for Dealers", "A design tool integration for dealers.", "Read the story", SITE + "/resources/news-updates/dmp-launches-partnership-with-system-surveyor"],
    ["Case study, 30 Oct 2026", "Customer Success Story: A Small Sensor. A Big Save.", "A customer story from our resource library.", "Read the story", SITE + "/resources/case-studies/customer-success-story-oct-2026"],
    ["News, 29 Oct 2025", "DMP Introduces VAULT: Secure, Encrypted Connectivity for Cloud-Based Security Applications", "Encrypted connectivity for cloud applications.", "Read the story", SITE + "/resources/news-updates/dmp-introduces-vault"],
]

# ------------------------------------------------------------------ helpers
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


COMMON_FAQ = {
    "who": ["Does DMP sell directly to building owners?", "We sell through authorized dealers and distributors. A building owner starts with a dealer, and our Inside Sales team helps with system design."],
    "where": ["Where is DMP based?", "Digital Monitoring Products is headquartered at 2500 N. Partnership Boulevard, Springfield, Missouri 65803, and we have made our products there since 1975."],
    "what": ["What does DMP make?", "Intrusion, access control, fire and video systems, with the communicators, keypads, wireless devices, Virtual Keypad and software that go with them."],
    "usa": ["Is DMP made in the USA?", "Our products are manufactured in the USA with U.S. and global components, in Springfield, Missouri."],
    "intl": ["Is there an international range?", "Yes. Our support and global pages list international products and a table of authorized distributors outside the U.S."],
    "person": ["How do I reach a person?", "Inside Sales is 877-757-4367, Technical Support 888-436-7832 and Customer Service 866-266-2826. The contact page lists hours and email addresses."],
    "docs": ["Where do I find datasheets and installation guides?", "In our technical documentation library, which holds spec sheets, installation and programming guides, quick start guides and technical updates."],
    "order": ["How do dealers place an order?", "At buy.DMP.com, which takes orders 24 hours a day, or through DMP Customer Service."],
    "soc": ["Is our software independently examined?", "Yes. We complete independent SOC 2 Type II examinations annually, by a licensed CPA firm, for Dealer Admin and Virtual Keypad."],
}


def cf(*keys):
    return [COMMON_FAQ[k] for k in keys]


CTA = {"label": "Contact DMP", "href": "contact.html"}
LEADFORM = {"type": "leadform", "alt": True, "id": "start", "heading": "Tell us what you are specifying",
            "body": "Say who you are, what the building is and which products you are looking at, and a person will reply.",
            "submit": "Send to DMP", "note": "Inside Sales is 877-757-4367, 8 a.m. to 5 p.m. Central."}


def itemlist(name, items):
    return {"@context": "https://schema.org", "@type": "ItemList", "name": name,
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": it[1], "url": it[3]} for i, it in enumerate(items)]}


def service_page(slug, navlabel, short, one, image, eyebrow, heading, subhead, benefits, included, faq, products, cat_url, dimg, dalt):
    secs = [
        {"type": "hero", "layout": "split", "eyebrow": eyebrow, "heading": heading, "subhead": subhead,
         "primary": CTA, "secondary": {"label": "All products", "href": "services.html"},
         "image": image, "image_alt": f"DMP {short}", "image_w": 1200, "image_h": 800},
        {"type": "cards", "alt": True, "eyebrow": "What sets it apart", "heading": f"Three things to know about {short}", "items": benefits},
        {"type": "resources", "heading": f"The {short} range", "intro": "Select a product for its full page.", "items": [[x[0], x[1], x[2], "View product", x[3]] for x in products]},
        {"type": "detail", "alt": True, "eyebrow": "In this category", "heading": f"What we build for {short}", "body": one, "bullets": included, "image": dimg, "image_alt": dalt, "flip": True},
        {"type": "services", "heading": "Works with", "intro": "Each system runs on the same platform.",
         "items": [[x[1], x[3], f"services/{x[0]}.html"] for x in SERVICES if x[0] != slug][:3]},
        {"type": "faq", "heading": f"Questions about {navlabel.lower()}", "items": list(faq) + cf("who", "person", "docs")},
        LEADFORM,
    ]
    return {"file": f"services/{slug}.html", "title": f"{navlabel} | {CLIENT}, Springfield, Missouri",
            "description": desc(f"{one} {subhead}"),
            "schema": [{"@context": "https://schema.org", "@type": "CollectionPage", "name": navlabel, "about": navlabel, "isPartOf": {"@id": f"{SITE}/#website"}}, itemlist(navlabel, products)],
            "crumbs": [["Home", "index.html"], ["Products", "services.html"], [navlabel, f"services/{slug}.html"]], "sections": secs}


def industry_page(slug, name, image, headline, why, bullets, featured, library, contact_role, faq):
    secs = [
        {"type": "hero", "layout": "split", "eyebrow": name, "heading": IND_H1.get(slug, headline),
         "subhead": headline,
         "primary": CTA, "secondary": {"label": "All industries", "href": "industries.html"}, "image": image, "image_alt": f"{name}: DMP", "image_w": 1200, "image_h": 800},
        {"type": "detail", "alt": True, "eyebrow": "Why DMP", "heading": f"Why DMP for {name.lower()}", "body": why, "bullets": bullets},
        {"type": "resources", "heading": "Featured products", "intro": "The products dealers reach for first in this market.", "items": [[x[0], x[1], x[2], "View product", x[3]] for x in featured]},
    ]
    if library:
        secs.append({"type": "cards", "alt": True, "eyebrow": "The library", "heading": f"The library for {name.lower()}", "intro": "White papers, spec sheets and guides for this market.", "items": [[t, "Available from DMP."] for t in library]})
    if contact_role:
        secs.append({"type": "detail", "eyebrow": "Talk to DMP", "heading": f"A dedicated {contact_role.lower()}", "body": f"We have a {contact_role.lower()} for this market. Inside Sales, 877-757-4367, can route the question, and our directory shows your regional sales manager.", "bullets": ["Inside Sales, 8 a.m. to 5 p.m. Central", "Regional sales manager directory"]})
    secs += [{"type": "services", "heading": "Systems that work together here", "intro": "Each has its own page.",
              "items": [[SERVICE_INDEX[x][1], SERVICE_INDEX[x][3], f"services/{x}.html"] for x in ("intrusion", "access-control", "fire", "video")]},
             {"type": "faq", "heading": f"Questions about {name.lower()} security", "items": list(faq) + cf("who", "what", "person", "docs")},
             LEADFORM]
    return {"file": f"industries/{slug}.html", "title": f"Security systems for {name.lower()} | {CLIENT}, Springfield, Missouri",
            "description": desc(f"{headline} {why}", 158),
            "crumbs": [["Home", "index.html"], ["Industries", "industries.html"], [name, f"industries/{slug}.html"]], "sections": secs}


SERVICE_INDEX = {s[0]: s for s in SERVICES}
WHEEL_ITEMS = [[s[1], brief(s[3], 140), f"services/{s[0]}.html", s[1]] for s in SERVICES]


try:
    import dmp_pages_audience as _aud
except ImportError:
    _aud = None


def build():
    brand = {
        "accent": "#FFD23D", "ink_secondary": "#111111", "chrome": "light",
        "type_from": {"Quantum Showcase": "Quantum Clean", "Quantum Press": "Quantum Clean"},
        "heading": {"weight": 800, "tracking": "-.03em"},   # the Van Ausdall HubSpot site: Open Sans 800, tight tracking
        "logo": "assets/dmp-logo.svg", "logo_alt": CLIENT, "logo_w": 100, "logo_h": 37,
        "logo_note": "DMP's real logo, from dmp.com.",
        "phone": PHONE, "phone_href": PHONE_HREF, "email": EMAIL,
        "utility": [{"label": "Order at buy.DMP.com", "href": BUY}, {"label": "Technical documentation", "href": DOCS}, {"label": "Support", "href": "support.html"}],
        "cta": CTA,
        "sticky": {"primary": "Contact DMP", "primary_href": "contact.html", "secondary": "Products", "secondary_href": "services.html"},
        "launcher": {"label": "Already a dealer?", "eyebrow": "The fast lane", "title": "What do you need today?",
                     "links": [["Order at buy.DMP.com", BUY], ["Technical documentation", DOCS], ["Support and contacts", "support.html"], ["Products", "services.html"]],
                     "note": "Technical Support 888-436-7832, 7 a.m. to 7 p.m. Central.", "phone": PHONE, "phone_href": PHONE_HREF},
        "social": {}, "tagline": "Security, fire, access control and video, made in Springfield, Missouri since 1975.",
        "footer_columns": [
            {"title": "Products", "links": [[s[1], f"services/{s[0]}.html"] for s in SERVICES]},
            {"title": "Industries", "links": [[i[1], f"industries/{i[0]}.html"] for i in INDUSTRIES]},
            {"title": "Support and training", "links": [["Contact and support", "support.html"], ["Technical support FAQs", "support/tech-faqs.html"], ["Documentation", "support/documentation.html"], ["Dealer services", "support/dealer-services.html"], ["Training", "training.html"], ["Technology partners", "partners.html"], ["Get a quote", "support/get-a-quote.html"]]},
            {"title": "Company", "links": [["About", "about.html"], ["Careers", "about/careers.html"], ["Certifications", "about/certifications.html"], ["Springfield, Missouri", "locations.html"], ["News and resources", "resources.html"], ["Events", "events.html"], ["International", "international.html"], ["Contact", "contact.html"]]},
        ],
        "legal": [["Privacy policy", "privacy-policy.html"], ["Terms of use", "terms-of-use.html"]],
    }
    schema = {"org_name": CLIENT, "org_url": SITE, "org_logo": SITE + "/static/logo-light.DC983iDA.svg",
              "org_description": "Digital Monitoring Products manufactures intrusion, access control, fire and video security systems in Springfield, Missouri, and sells them through authorized dealers and distributors. Founded in 1975.",
              "sameAs": [], "telephone": "+1-877-757-4367", "founded": FOUNDED, "slogan": "Built in Springfield since 1975"}
    schema.update({"short_name": "DMP", "title_city": "Springfield, Missouri", "cities": ["Springfield", "Springfield, Missouri", "Missouri", "MO"],
                   "area_served": [{"@type": "Country", "name": "United States"}], "service_globs": [],
                   "meta_tail": "Digital Monitoring Products, Springfield, Missouri.",
                   "local": [{"slug": "springfield-headquarters", "name": "Digital Monitoring Products headquarters", "street": "2500 N. Partnership Boulevard", "city": "Springfield",
                              "region": "MO", "postal": "65803", "country": "US", "telephone": "+1-877-757-4367"}]})
    nav = [
        {"label": "Products", "href": "services.html", "children": [[s[1], f"services/{s[0]}.html"] for s in SERVICES]},
        {"label": "Industries", "href": "industries.html", "children": [[i[1], f"industries/{i[0]}.html"] for i in INDUSTRIES]},
        {"label": "Support", "href": "support.html", "children": [["Contact and support", "support.html"], ["Technical support FAQs", "support/tech-faqs.html"], ["Documentation", "support/documentation.html"], ["Dealer services", "support/dealer-services.html"], ["Design tools", "support/design-tools.html"], ["Architect and engineer support", "support/ae-support.html"], ["Training", "training.html"], ["Get a quote", "support/get-a-quote.html"]]},
        {"label": "Partners", "href": "partners.html", "children": [["Technology partners", "partners.html"], ["Become a partner", "partners/become-a-partner.html"], ["Become a dealer", "support/become-a-dealer.html"]]},
        {"label": "Resources", "href": "blog.html", "children": [["Blog", "blog.html"], ["Find a system", "find-a-system.html"], ["For dealers", "for-dealers.html"], ["For specifiers", "for-specifiers.html"], ["For building owners", "for-building-owners.html"], ["Dealer portal preview", "dealer-portal.html"], ["Why DMP", "why-dmp.html"]]},
        {"label": "Company", "href": "about.html", "children": [["About DMP", "about.html"], ["Careers", "about/careers.html"], ["DMP Cares", "about/dmp-cares.html"], ["Certifications", "about/certifications.html"], ["Springfield, Missouri", "locations.html"], ["News and resources", "resources.html"], ["Events", "events.html"], ["International", "international.html"], ["FAQ", "faq.html"], ["Contact", "contact.html"]]},
    ]
    pages = []
    # ------------------------------------------------------------------ home
    pages.append({"file": "index.html", "title": f"{CLIENT} | Security systems built in Springfield, Missouri since 1975",
                  "description": "Digital Monitoring Products designs and builds intrusion, access control, fire and video systems in Springfield, Missouri, and sells them through authorized dealers. Since 1975.",
                  "sections": [
        {"type": "hero-layered", "id": "hero-layered", "eyebrow": "Springfield, Missouri, since 1975",
         "heading": "Four systems. <em>One platform.</em>",
         "subhead": "We manufacture the panels, keypads, communicators and software behind the systems dealers install, and sell them through authorized dealers and distributors.",
         "primary": CTA, "secondary": {"label": "See the products", "href": "services.html"},
         "image": IMG + "hero-hq-dark-2100.jpg", "image_w": 2100, "image_h": 900,
         "stats": [["1975", "Founded in Springfield"], ["14", "Product categories"], ["SOC\u00a02", "Type II examination, every year"], ["24/7", "Dealer ordering at buy.DMP.com"]],
         "card_a": {"eyebrow": "Specifying a system", "title": "Start from the product", "body": "Panels, readers, cameras and communicators, each with a page and a spec sheet.",
                    "items": ["XT75, XR550 and XR650 control panels", "Digital Key and Entré access control", "VUE Plus cameras and AlarmVision"], "label": "Browse products", "href": "services.html"},
         "card_b": {"eyebrow": "Already a DMP dealer?", "title": "The fast lane", "body": "Order, look up a document or reach a person.",
                    "links": [["Order at buy.DMP.com", BUY], ["Technical documentation", DOCS], ["Contact and support", "contact.html"]]}},
        {"type": "partners", "caption": "Industry associations and alliances", "items": ASSOCIATIONS},
        {"type": "stats3d", "id": "facts", "items": [["50", "Years making security systems"], ["SOC 2 Type II", "Examined every year"], ["14", "Product categories"], ["USA", "Made with U.S. and global components"]]},
        {"type": "tabs", "id": "systems", "eyebrow": "One manufacturer", "heading": "Four systems, and the app that runs them", "items": [
            {"label": "Intrusion", "title": "Intrusion panels from XT to XR", "body": "The XT75 is a hybrid intrusion panel for residential or small business applications. It integrates intrusion, access control and AlarmVision, bridging the gap between the XT and XR Series.",
             "bullets": ["XT30, XT50 and XT75", "XR150, XR550 and XR650", "TMSentry for teller machines"], "image": IMG + "tab-intrusion-1200.jpg", "image_alt": "The DMP XT75 control board", "href": "services/intrusion.html", "link_label": "Intrusion systems"},
            {"label": "Access control", "title": "Access control beyond the fob", "body": "Digital Key adds a credential to an Apple or Google device's mobile wallet, so the smartphone works as a secure, contactless credential.",
             "bullets": ["Digital Key and mobile credentials", "X1 Series cloud access control", "Entré Lite, Business and Enterprise"], "image": IMG + "tab-access-1200.jpg", "image_alt": "A phone held to a door reader", "href": "services/access-control.html", "link_label": "Access control"},
            {"label": "Fire", "title": "A 24V fire solution", "body": "The XF6 fire control panel is built for single-site applications and comes with network and optional cellular communications that send all signals directly to the monitoring center.",
             "bullets": ["XF6, XR150FC and XR550FC", "Smoke detectors and pull stations", "PowerCom Fire communicators"], "image": IMG + "tab-fire-1200.jpg", "image_alt": "The DMP XF6 fire control panel", "href": "services/fire.html", "link_label": "Fire systems"},
            {"label": "Video", "title": "Video that raises the alarm", "body": "DMP video became a complete platform with VK VMS and the XV Plus gateways. AlarmVision uses analytics to trigger alarms into XR Series panels.",
             "bullets": ["VUE Plus camera line", "VK VMS video management", "XV gateways with AlarmVision"], "image": IMG + "tab-video-1200.jpg", "image_alt": "A VUE Plus camera", "href": "services/video.html", "link_label": "Video"},
            {"label": "Mobile", "title": "Virtual Keypad and Dealer Admin", "body": "Virtual Keypad lets dealers brand a full-featured remote control. Dealer Admin handles mass panel programming and bulk firmware updates. Both are examined annually for SOC 2 Type II.",
             "bullets": ["Virtual Keypad for iOS, Android and the browser", "Dealer Admin programming templates", "Mobile wallet credentials"], "image": IMG + "tab-mobile-1200.jpg", "image_alt": "Virtual Keypad on a laptop, tablet and phone", "href": "services/mobile-automation.html", "link_label": "Virtual Keypad and software"}]},
        {"type": "showcase3d", "id": "flagships", "eyebrow": "The range", "heading": "Meet the products behind the platform.", "intro": "Drag, swipe or use the arrow keys. Click a product to open it.", "items": _aud.SHOWCASE},
        {"type": "flow", "id": "how", "alt": True, "eyebrow": "How a DMP system works", "heading": "Follow one alarm from the sensor to the phone",
         "intro": "Five steps, one manufacturer. Select a step to see what happens and which DMP products do the work.", "detail_eyebrow": "What happens", "receive_label": "DMP products at this step", "steps": [
            {"label": "Detect", "when": "Sensors and cameras", "summary": "Doors, windows, motion, smoke, glass and video.", "title": "Detectors and cameras see the event",
             "body": "Door and window contacts, motion and glassbreak detectors, smoke, heat and CO detectors and cameras all report to the panel, wired or over our 1100 Series wireless, which has been AES encrypted since 2019. AlarmVision analytics let cameras act like smart motion detectors.",
             "receive": ["1100 Series wireless devices", "Motion, glassbreak and contact detectors", "Smoke, heat and CO detectors", "VUE Plus cameras and XV gateways"]},
            {"label": "Decide", "when": "Control panel", "summary": "XT, XTL and XR Series; XF6 for fire.", "title": "The panel decides what the event means",
             "body": "Cancel/Verify false alarm prevention has been a DMP feature since 2007. The XT75 runs intrusion, access control and AlarmVision together, and the XR550 supports 96 doors of access control.",
             "receive": ["XT30, XT50 and XT75", "XR150, XR550 and XR650", "XF6 fire control panel", "TMSentry for teller machines"]},
            {"label": "Report", "when": "Communicators", "summary": "Cellular, network and Wi-Fi paths.", "title": "The signal goes out on more than one path",
             "body": "We offer LTE, Wi-Fi and universal communicators, including the first alarm panel communicator for the AT&T FirstNet network (2020). The XR550 supports up to eight communication paths and moves to a backup path instantly. JamAlert detects cellular jamming, and VAULT encrypts the link to our cloud.",
             "receive": ["263LTE and 265LTE", "Dual Com and Cell Com", "763 Wi-Fi", "JamAlert and VAULT"]},
            {"label": "Respond", "when": "Monitoring center", "summary": "Receivers, software and line cards.", "title": "The monitoring center receives it",
             "body": "At the central station a DMP receiver takes the signal. We introduced SCS-VR in 2009 as the first software-only central station receiver, and still offer SCS receivers and line cards.",
             "receive": ["SCS-VR virtual receiver software", "SCS-1R receiver", "SCS line cards"]},
            {"label": "Control", "when": "Dealer and owner", "summary": "Apps, credentials and cloud tools.", "title": "Owners and dealers stay in control",
             "body": "Owners use Virtual Keypad on iOS, Android or the browser, and mobile wallet credentials such as Digital Key. Dealers program panels in bulk with Dealer Admin. Both cloud services are examined annually for SOC 2 Type II.",
             "receive": ["Virtual Keypad", "Digital Key", "Dealer Admin", "Entré access control software"]}]},
        {"type": "tabs", "id": "who", "eyebrow": "Whoever you are", "heading": "Dealer, specifier or owner: start where you sit", "items": [
            {"label": "Dealers", "title": "Order, program and get support", "body": "Dealers order at buy.DMP.com 24 hours a day, program panels with Dealer Admin, and reach Technical Support from 7 a.m. to 7 p.m. Central. We also offer Dealer Services and a regional sales manager directory.",
             "bullets": ["Order at buy.DMP.com", "Dealer Admin: mass programming, bulk firmware updates, templates", "Technical documentation, training videos and tech FAQs", "Find your regional sales manager"], "image": IMG + "tab-mobile-1200.jpg", "image_alt": "Virtual Keypad and Dealer Admin on laptop, tablet and phone", "href": "contact.html", "link_label": "Contact and support"},
            {"label": "Specifiers", "title": "Design support from people who know the system", "body": "Our Inside Sales team supports system design, architects and engineers, pre-sales questions and quotes. In March 2026 we announced an integration with System Surveyor to streamline intrusion and access control system design for dealers.",
             "bullets": ["Spec sheets on every product page", "Inside Sales: 877-757-4367", "System Surveyor integration", "Industry brochures and white papers"], "image": IMG + "tab-spec-1200.jpg", "image_alt": "A tablet showing a floor plan in System Surveyor", "href": "resources.html", "link_label": "News and resources"},
            {"label": "Building owners", "title": "Start with a dealer", "body": "We sell through authorized dealers and distributors. Pick the kind of building you run, see how our systems fit it, then ask a dealer to specify the system.",
             "bullets": ["Eleven industries, each with a page", "Intrusion, access control, fire and video from one manufacturer", "Control from a phone with Virtual Keypad"], "image": IMG + "tab-owner-1200.jpg", "image_alt": "A person checking a phone as they leave a building", "href": "industries.html", "link_label": "Browse industries"}]},
        {"type": "portal", "id": "portal", "eyebrow": "For dealers", "heading": "One sign-in for everything a dealer needs.", "intro": "A preview of the dealer home we would build: documents, ordering, Marketing Central, training, support and quotes behind one login. How it connects to the Buy site and Marketing Central is a proposed design to confirm with DMP IT.",
         "tiles": [["Documentation library", "Spec sheets, guides and firmware notes.", "docs"], ["Order on the Buy site", "Place orders 24 hours a day.", "cart"], ["Marketing Central", "Brand-approved sales and marketing material.", "megaphone"], ["DMP University", "Training for your team.", "training"], ["Technical support", "Reach a person, or search the FAQs.", "support"], ["Get a quote", "Start a system design request.", "quote"]],
         "signin_label": "Sign in", "cta_label": "See the dealer portal preview", "cta_href": "dealer-portal.html"},
        {"type": "detail", "id": "made-here", "alt": True, "eyebrow": "Made in Springfield", "heading": "Making it in the U.S. keeps us close to our dealers.",
         "body": "Manufacturing in the U.S. builds a tighter partnership with our customers and our community. We are honored to employ Springfield-area residents who are dedicated to the industry and its dealers.",
         "bullets": ["Headquarters: 2500 N. Partnership Boulevard, Springfield, Missouri", "Founded in 1975 by Rick Britton", "SOC 2 Type II examined by a licensed CPA firm every year"],
         "image": IMG + "plant-1200.jpg", "image_alt": "The DMP production floor in Springfield, Missouri", "image_w": 1200, "image_h": 800},
        {"type": "timeline", "id": "story", "eyebrow": "Fifty years of firsts", "heading": "From a central station receiver to a cloud platform",
         "intro": "Milestones from our history.", "items": [TIMELINE[0], TIMELINE[3], TIMELINE[7], TIMELINE[10], TIMELINE[11], TIMELINE[13]]},
        {"type": "resources", "heading": "What we shipped and earned in 2026", "intro": "Launches, awards and customer stories.", "items": NEWS[:3]},
        {"type": "faq", "id": "faq", "heading": "Quick answers for dealers and specifiers", "items": cf("who", "where", "usa", "order", "soc")},
        {"type": "contact", "id": "contact", "heading": "Talk to a person at DMP", "body": "Tell us who you are and what you are specifying.",
         "options": ["I am a dealer", "I am specifying a building", "I own a building", "Something else"], "submit": "Send to DMP",
         "note": "Inside Sales, 8 a.m. to 5 p.m. Central."},
    ]})
    # ------------------------------------------------------------------ products hub
    pages.append({"file": "services.html", "title": f"Products | {CLIENT}, Springfield, Missouri",
                  "description": "Our catalogue by system: intrusion, access control, fire, video, communicators, wireless, panels and keypads, Virtual Keypad and software.",
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "Products", "heading": "Every part of the system. <em>One manufacturer.</em>",
         "subhead": "Start from the system you are specifying. See what we make for it and every product behind it.", "primary": CTA,
         "image": IMG + "banner-allin-1200.jpg", "image_alt": "A DMP circuit board with the shield 'All in on DMP: access control, communicators, fire, intrusion, video'", "image_w": 1200, "image_h": 495},
        {"type": "wheel", "id": "wheel", "eyebrow": "One range", "heading": "Pick a system. See every part we make for it.", "intro": "Hover a segment.",
         "items": WHEEL_ITEMS, "hub": "DMP", "hub_sub": "Since 1975", "ring": "SECURITY, FIRE, ACCESS AND VIDEO", "panel_eyebrow": "Hover a segment", "link_label": "See the product line"},
        {"type": "resources", "heading": "All eight systems", "intro": "Every system, with its products, the questions buyers ask and the documents behind them.",
         "items": [[s[5], s[1], s[3], "See the line", f"services/{s[0]}.html"] for s in SERVICES]},
        {"type": "detail", "alt": True, "eyebrow": "Buying", "heading": "Order any hour at buy.DMP.com", "body": "Dealers order at buy.DMP.com 24 hours a day. Customer Service handles products and ordering, software activations, the Buy Site, shipping and order entry questions.",
         "bullets": ["Customer Service 866-266-2826, 8 a.m. to 6 p.m. Central", "Inside Sales for system design and quotes, 877-757-4367", "International products and distributors on our global page"],
         "image": IMG + "system-surveyor-1200.jpg", "image_alt": "A hand holding a tablet showing a floor plan in System Surveyor", "flip": True},
        {"type": "faq", "heading": "Before you order", "items": cf("what", "who", "intl", "docs", "order")},
        LEADFORM]})
    for s in SERVICES:
        pages.append(service_page(*s))
    # ------------------------------------------------------------------ industries
    pages.append({"file": "industries.html", "title": f"Industries | {CLIENT}, Springfield, Missouri",
                  "description": "Eleven industries, each with its own page: commercial, financial institutions, retail, government, industrial, education, healthcare, multi-tenant, religious, storage and residential.",
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "Industries", "heading": "Eleven kinds of building. <em>One manufacturer.</em>",
         "subhead": "See what we offer for each, the products we feature and the documents behind them.", "primary": CTA,
         "image": IMG + "banner-allin-1200.jpg", "image_alt": "A DMP circuit board with the shield 'All in on DMP: access control, communicators, fire, intrusion, video'", "image_w": 1200, "image_h": 495},
        {"type": "services", "heading": "Start with the building you protect", "intro": "Choose the nearest match.",
         "items": [[i[1], i[3], f"industries/{i[0]}.html"] for i in INDUSTRIES]},
        {"type": "faq", "heading": "Questions about industries", "items": cf("what", "who", "person")},
        LEADFORM]})
    for i in INDUSTRIES:
        pages.append(industry_page(*i))
    # ------------------------------------------------------------------ about
    pages.append({"file": "about.html", "title": f"About {CLIENT} | Manufacturer in Springfield, Missouri since 1975",
                  "description": "Digital Monitoring Products has manufactured security systems in Springfield, Missouri since 1975. Our mission, values, history, leadership and independent SOC 2 Type II examinations.",
                  "sections": [
        {"type": "hero", "layout": "split", "eyebrow": "About DMP", "heading": "We build security systems <em>to create jobs</em>.",
         "subhead": "Our purpose: the security of families determines the strength of society, and a strong society reaches out to the rest of the world.", "primary": CTA,
         "image": IMG + "hq-exterior-1200.jpg", "image_alt": "The DMP headquarters in Springfield, Missouri, with the American flag in front", "image_w": 1200, "image_h": 800},
        {"type": "proof", "alt": True, "eyebrow": "Our mission", "value": "We care. We have fun. We profit.",
         "text": "We provide customer-driven products through listening, anticipating needs and responding quickly with innovative solutions that work. We insist on the integrity of our products and our people.", "source": "DMP mission statement"},
        {"type": "timeline", "id": "story", "eyebrow": "Our history", "heading": "Fifty years of firsts",
         "intro": "How we began, and what followed.", "items": TIMELINE},
        {"type": "values", "alt": True, "eyebrow": "Our values", "heading": "Six values, in our own words", "items": VALUES},
        {"type": "detail", "eyebrow": "Where we build", "heading": "Manufactured in the USA, with U.S. and global components",
         "body": "'Made in the USA' is something you rarely see today. Like other manufacturers, we rely on some components that are not indigenous to the U.S. Manufacturing in the U.S. builds a tighter partnership with customers and the community.",
         "bullets": ["2500 N. Partnership Boulevard, Springfield, Missouri 65803", "Jobs for Springfield-area residents"],
         "image": IMG + "plant-1200.jpg", "image_alt": "The DMP production floor", "image_w": 1200, "image_h": 800},
        {"type": "cards", "alt": True, "eyebrow": "Certifications", "heading": "Examined by outsiders, every year", "items": [
            ["SOC 2 Type II", "We complete independent SOC 2 Type II examinations annually, conducted by a licensed CPA firm to AICPA standards."],
            ["Tier 4 data center", "Dealer Admin and Virtual Keypad are hosted in a Tier 4 data center with fully redundant subsystems."],
            ["SOC 3 report", "The SOC 3 report is intended for public distribution. SOC 2 reports go to customers and partners under confidentiality."]]},
        {"type": "leadership", "heading": "Twelve people run DMP", "intro": "The people who lead DMP.", "people": LEADERS,
         "orgs_intro": "Industry associations and alliances", "orgs": ASSOCIATIONS},
        {"type": "faq", "id": "faq", "heading": "Questions about DMP", "items": cf("where", "usa", "what", "who", "soc", "person")},
        LEADFORM]})
    # ------------------------------------------------------------------ Springfield
    pages.append({"file": "locations.html", "title": f"Springfield, Missouri headquarters | {CLIENT}",
                  "description": "Digital Monitoring Products is headquartered and manufactures at 2500 N. Partnership Boulevard, Springfield, Missouri 65803. Phone 877-757-4367.",
                  "sections": [
        {"type": "hero", "layout": "split", "eyebrow": "Springfield, Missouri", "heading": "One headquarters. <em>Authorized distributors worldwide.</em>",
         "subhead": "2500 N. Partnership Boulevard, Springfield, Missouri 65803. Inside Sales 877-757-4367.", "primary": CTA,
         "image": IMG + "hq-exterior-2-1200.png", "image_alt": "The DMP headquarters entrance sign with the American flag", "image_w": 1200, "image_h": 675},
        {"type": "cards", "alt": True, "eyebrow": "Reach a person", "heading": "Call the right team", "items": [
            ["Inside Sales, 877-757-4367", "System design, architect and engineer support, pre-sales support, quotes and pricing, and Dealer Direct assistance. 8 a.m. to 5 p.m. Central. InsideSales@DMP.com."],
            ["Technical Support, 888-436-7832", "Installation, programming, troubleshooting and diagnostics. 7 a.m. to 7 p.m. Central. TechSupport@DMP.com."],
            ["Customer Service, 866-266-2826", "Products and ordering, software activations, the Buy Site, shipping and order entry. 8 a.m. to 6 p.m. Central. CustomerService@DMP.com."]]},
        {"type": "cards", "eyebrow": "Beyond the U.S.", "heading": "Authorized distributors worldwide", "intro": "Our authorized distributors outside the U.S.", "items": [
            ["Benelux", "Sabelco"], ["Greece and Cyprus", "GQ Tech"], ["Hungary", "Object Guard"], ["Latin America and the Caribbean", "ISTC"],
            ["Mexico", "Otwo and Tecnoseguridad"], ["South Africa, Mozambique and Zambia", "Regal"], ["United Kingdom and Ireland", "ADI EU"]]},
        {"type": "faq", "id": "faq", "heading": "Where DMP works", "items": cf("where", "usa", "intl", "who", "person")},
        LEADFORM]})
    pages.append({"file": "resources.html", "title": f"News and resources | {CLIENT}, Springfield, Missouri",
                  "description": "Recent news, case studies and product announcements from Digital Monitoring Products, with our technical documentation and training library.",
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "News and resources", "heading": "Launches, awards and <em>the library behind them</em>.",
         "subhead": "Product launches, awards and customer stories, with the technical library behind them.", "primary": {"label": "Technical documentation", "href": DOCS},
         "image": IMG + "fifty-1200.jpg", "image_alt": "All DMP employees in front of the headquarters, with the banner 'Welcome to the standard of excellence in commercial security'", "image_w": 1200, "image_h": 495},
        {"type": "resources", "heading": "Recent announcements", "intro": "Select a story to read it.", "items": NEWS[:6]},
        {"type": "cards", "alt": True, "eyebrow": "The library", "heading": "For installers and specifiers", "items": [
            ["Technical documentation", "Spec sheets, installation and programming guides, quick start guides and technical updates."],
            ["Training videos", "Webinars and training, including the System Surveyor design session."],
            ["Technical Support FAQs", "Answers to the questions Technical Support hears most."]]},
        LEADFORM]})
    pages.append({"file": "faq.html", "title": f"FAQ | {CLIENT}, Springfield, Missouri",
                  "description": "Answers about Digital Monitoring Products: who it sells to, what it makes, where it is made, how dealers order and how to reach a person.",
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "FAQ", "heading": "Straight answers for <em>dealers, specifiers and owners</em>.", "subhead": "If yours is not here, call Inside Sales at 877-757-4367."},
        {"type": "faq", "heading": "About DMP", "items": cf("what", "who", "where", "usa", "intl", "soc", "order", "person", "docs")},
        LEADFORM]})
    pages.append({"file": "contact.html", "title": f"Contact and support | {CLIENT}, Springfield, Missouri",
                  "description": "Contact Digital Monitoring Products: Inside Sales 877-757-4367, Technical Support 888-436-7832, Customer Service 866-266-2826, with hours and email.",
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "Contact and support", "heading": "Reach the <em>right person</em> the first time.",
         "subhead": "Dealers, specifiers and building owners start in the same place."},
        {"type": "contact", "id": "form", "heading": "Tell us what you need", "body": "Choose what fits best.",
         "options": ["I am a dealer", "I am specifying a building", "I own a building", "Something else"], "submit": "Send to DMP",
         "note": "Inside Sales, 8 a.m. to 5 p.m. Central."},
        {"type": "cards", "alt": True, "eyebrow": "By phone", "heading": "Call the right team", "items": [
            ["Inside Sales, 877-757-4367", "System design, quotes and pricing. 8 a.m. to 5 p.m. Central."],
            ["Technical Support, 888-436-7832", "Installation, programming and troubleshooting. 7 a.m. to 7 p.m. Central."],
            ["Customer Service, 866-266-2826", "Products and ordering, software activations, shipping. 8 a.m. to 6 p.m. Central."],
            ["SecureCom Wireless, 877-300-8030", "Activation and billing. 8 a.m. to 5 p.m. Central."]]},
        {"type": "detail", "eyebrow": "Self-service", "heading": "Before you call", "body": "Our library answers most installation questions.",
         "bullets": ["Technical documentation", "Training videos", "Technical Support FAQs", "Dealer services and the regional sales manager directory"]},
        {"type": "faq", "heading": "Before you write", "items": cf("person", "who", "where", "docs", "order")},
    ]})

    pitch = {
        "qbs_contact": {"name": "Shawn", "email": "shawn@thequantumleap.business"},
        "prepared_for": "Digital Monitoring Products",
        "heard_intro": "There is no design brief from DMP yet. This version is written from dmp.com itself, read on 9 November 2026: its history, certifications, support lines, product catalogue, news and photography, in DMP's own words wherever a claim is DMP's to make. Tell us where it is wrong; your words outrank ours.",
        "heard": ["DMP sells through authorized dealers and distributors, so the site's first job is dealers and specifiers: find the product, get the spec sheet, place the order, reach a person.",
                  "DMP is a current Quantum client with a HubSpot CRM, marketing, sales and service launch under way, so the site has to feed that: forms that create records and one place for dealers to start.",
                  "DMP's own brand is yellow, black and beige. The previews use that palette, DMP's real logo and DMP's own photography, so what you see is closer to the finished site than a mood board."],
        "found": ["Search (Semrush US database, 9 November 2026): about 23,660 organic visits a month on 7,521 keywords, but 75 percent of that is navigational, people already searching the brand. DMP is not in the top ten for any of seven national category searches such as fire alarm control panel and access control panel. An AI-answer test on national buyer questions has not been run yet.",
                  "A page-level audit of 241 public pages on www.dmp.com (9 November 2026) averages 35 out of 100, and no page scores above a D. The home page is the strongest at 52: it has a title, one H1, a canonical, a phone link and a form.",
                  "The front door and the robots file: https://dmp.com/ answers 301 to http://www.dmp.com/, which answers 307. robots.txt returns HTTP 404 although it holds rules and Sitemap lines, so crawlers ignore it. The sitemap is live (369 products, 26 categories, 197 pages), and there is no llms.txt.",
                  "Markup: Organization (address, phone, founding date) is on 226 of 241 pages. None carries Product, ItemList, FAQPage or ContactPoint markup, and there are no sameAs links.",
                  "Page content: 175 of 241 pages have under 300 words, 107 share one default description, 66 titles are under 25 characters, 226 pages have an image with no alt text, and only 36 have a question heading.",
                  "Correction to the September report: its crawl started at the redirecting apex and read one URL, so its findings about the home page's title, H1, canonical, robots.txt, sitemap and structured data were wrong for the real site. They are replaced here.",
                  "Strengths to keep: 50 years of history, a real manufacturing story, SOC 2 Type II examinations, 14 product categories, a deep library of spec sheets and guides, and 1,916 referring domains."],
        "more": [["Why build it on HubSpot", "One platform for the site, the CRM and the dealers: what the build looks like, a fair comparison with Craft CMS, the risks we would manage and the questions to ask any bidder.", "hubspot-build.html"]],
        "choose_heading": "Three directions. Your call.",
        "choose_intro": "The words and the pages are the same in all three. What differs is the register. Open each one and tell us which feels like DMP.",
        "choose_reasons": [["Showcase: image-led", "Layered photography and a sales-forward feel. It makes the most of DMP's product and facility photos."],
                           ["Clean: plain and fast", "High contrast, product names first. Built for dealers and specifiers scanning for a panel or module."],
                           ["Press: editorial", "Serif headings and a magazine feel, so a 50-year-old manufacturer reads like the established name it is."]],
        "pick_reasons": [["The audience is dealers and specifiers", "They scan a catalogue to find a panel or a module. Clean puts the product names and categories first and stays out of the way."],
                         ["DMP's own look is high contrast", "Yellow and black on white is already DMP's brand. Clean lets it read as confident rather than loud."],
                         ["The catalogue is large", "dmp.com lists hundreds of product pages and a deep library. A plain, fast layout carries that better than a showy one."]],
        "pick_change": "Confirm the yellow, replace the theme typefaces with DMP's own (Gotham is licensed) and swap in any new photography DMP has.",
        "alternatives": [["Quantum Showcase", "The image-led choice: layered and sales-forward, and the one that makes the most of DMP's product photography."],
                         ["Quantum Press", "The wildcard: serif and editorial, so a 50-year-old manufacturer reads like the established name it is."]],
        "plan": [["Days 1 to 10", "Serve the site at one canonical host with a single HTTPS 301, name the crawlers in robots.txt, publish llms.txt, and add sameAs links to the Organization markup, which keeps the headquarters address as it is."],
                 ["Days 10 to 30", "Confirm the items below, decide how the product catalogue is built (see the first item), and sign off copy for each of the eight system lines."],
                 ["Days 30 to 45", "Build the eight system pages with question headings, FAQ markup, product lists and an enquiry form on each."],
                 ["Days 45 to 60", "Build the about and proof pages, and add Product markup to the catalogue pages."],
                 ["Days 60 to 90", "Publish the first three answer posts against access control, fire alarm and video surveillance questions, and the news and resources hub."],
                 ["Day 90", "Re-run the same national keyword set, the same AI questions and the same page audit against the baseline."]],
        "search": {"heading": "Where you stand in search today, and what changes", "intro": "Measured before we touched anything.", "as_of": "9 November 2026",
                   "today_stats": [["23,660", "Organic visits a month"], ["7,521", "Organic keywords"], ["0 of 7", "National category searches in the top ten"], ["39", "Authority Score"]],
                   "today": ["23,660 organic visits a month, 75 percent of them navigational searches for the brand itself.",
                             "0 of 7 national category searches put DMP in the top ten. The AI-answer test on national buyer questions has not been run yet.",
                             "Product pages carry Organization markup but no Product or FAQ markup, and no question headings.",
                             "No llms.txt and no sameAs links."],
                   "after": ["Eight system pages written in the words buyers search, each with question headings and FAQ markup.",
                             "Category pages for panels, access control, fire and communicators, written as the answer to the dealer's or specifier's search.",
                             "Product and ItemList markup on the catalogue pages, sameAs links and an llms.txt.",
                             "One HTTPS 301 at the front door and a robots.txt that names the crawlers."],
                   "keep": [["http://dmp.com/", "https://www.dmp.com/", "One hop instead of two, and none through plain HTTP."],
                            ["/products/... part-number pages", "unchanged", "Every product page keeps its address, so the pages that earn today's traffic keep it."]],
                   "note": "Rankings or traffic. Those depend on the market and on what DMP publishes after launch. We promise the inputs, and we measure the result against the 9 November baseline at 30, 60 and 90 days."},
        "confirm": [
            "How the product catalogue is built. dmp.com has hundreds of product pages (the sitemap lists panels, keypads, modules, readers, cameras and accessories by part number). HubSpot's page limits depend on the tier, so we need DMP's tier before deciding between building every product page in HubSpot and keeping the catalogue on its current system behind the new front door.",
            "The promise line. The home page says 'Security systems, built in Springfield', which is DMP's founding story, not a confirmed tagline.",
            "Typefaces. DMP uses Gotham. The previews use the Quantum theme typefaces; Gotham needs a licence for the real site.",
            "Photography and logos. Images come from dmp.com, as does the logo. They are used here for a private preview. Confirm rights, and supply anything newer.",
            "Milestone details. The timeline repeats DMP's own history list. Photos beside 1975, 1993, 2005, 2021 and 2025 come from dmp.com's history and about pages; confirm the years against the originals.",
            "Claims taken from DMP's own announcements: the XR Series being 32 times faster, the XR650 award, JamAlert's UL certification, and the jewelry store coverage mentioned in the JamAlert graphic. Each needs DMP's approval before it goes live in a headline.",
            "Industries. All eleven pages are written from DMP's own industry pages (dmp.com/products/industries). Quotations are condensed; each featured product, white paper and compliance claim (for example UL 634 Level 2, NDAA/TAA, FirstNet approval, 256-bit AES) needs DMP's approval before it is repeated in a headline.",
            "Social profiles. None are linked on dmp.com, so none appear. We recommend adding LinkedIn, YouTube and Crunchbase to the markup.",
            "Dealer routes. A dealer locator, a become-a-dealer path and a dealer login were not found on dmp.com, so none are drawn. Confirm what dealers and specifiers need to start.",
            "The associations strip. The logos are those shown on dmp.com's About page. Confirm membership status for each before showing them as a row of badges.",
            "The apex redirect, the gforce.www.dmp.com sitemap line and the buy.dmp.com ordering site are out of scope for the front-end build but affect search and the hand-off.",
            "The audit covers 241 public pages (156 of the page sitemap, 129 of 369 products and 28 category pages, with the dealer-facing intranet pages left out), because DMP's firewall blocks our audit agent. Ask DMP IT to allow our crawler so we can audit every page and run the site checks properly; until then the site-level results come from individual requests."],
        "footer": "Prepared for Digital Monitoring Products. Nothing here is live or indexed. Logo and photographs are from dmp.com and are used in this private preview.",
    }
    return finalize({"client": CLIENT, "slug": "digital-monitoring-products", "domain_hint": "dmp.com", "brand": brand, "schema": schema, "nav": nav, "pages": pages, "pitch": pitch})


# ------------------------------------------------------------------ merge the page-family modules and keep every link on the new site
SYSTEM_BY_SEGMENT = {"control-panels": "panels-keypads", "keypads": "panels-keypads", "modules-expanders": "panels-keypads", "power-supplies": "panels-keypads",
                     "access-control": "access-control", "entr%C3%A9-software": "access-control", "fire": "fire", "video": "video",
                     "cell-network-communicators": "communicators", "monitoring-center": "communicators", "wireless": "wireless",
                     "mobile-platforms": "mobile-automation", "automation": "mobile-automation", "intrusion": "intrusion"}


def finalize(data):
    import importlib
    import sys
    sys.path.insert(0, HERE)
    mods = []
    for fam in ("products", "support", "company", "partners", "audience", "blog"):
        try:
            mods.append(importlib.import_module(f"dmp_pages_{fam}"))
        except ModuleNotFoundError as e:
            raise SystemExit(f"missing page module dmp_pages_{fam}: {e}")
    have = {pg["file"] for pg in data["pages"]}
    for m in mods:
        for pg in m.PAGES:
            if pg["file"] not in have:
                data["pages"].append(pg)
                have.add(pg["file"])
        data["pitch"]["confirm"] = data["pitch"]["confirm"] + [x for x in getattr(m, "TO_CONFIRM", []) if x not in data["pitch"]["confirm"]]
    url_map, news = {}, getattr(next((m for m in mods if hasattr(m, "NEWS")), None), "NEWS", None)
    for m in mods:
        url_map.update(getattr(m, "URL_MAP", {}))
    news_map = {old[4]: new[4] for old, new in zip(NEWS, news)} if news else {}

    def resolve(u):
        if u in url_map:
            return url_map[u], "View product"
        if u in news_map:
            return news_map[u], "Read the story"
        if u.startswith(SITE + "/products/"):
            seg = u[len(SITE + "/products/"):].split("/")[0]
            return f"services/{SYSTEM_BY_SEGMENT.get(seg, 'intrusion')}.html", "See the system"
        if "/technical-documentation" in u:
            return "support/documentation.html", "Browse the library"
        if u.rstrip("/") == SITE + "/support":
            return "support.html", "Support"
        return "resources.html", "Read more"

    def walk(x, in_schema=False):
        if isinstance(x, dict):
            return {k: walk(v, in_schema or k == "schema") for k, v in x.items()}
        if isinstance(x, list):
            if len(x) == 5 and isinstance(x[4], str) and x[4].startswith(SITE + "/") and not in_schema:
                new, label = resolve(x[4])
                return [x[0], x[1], x[2], label if "dmp.com" in str(x[3]) or x[3] in ("View product", "Read more") else x[3], new]
            return [walk(v, in_schema) for v in x]
        if isinstance(x, str) and x.startswith(SITE + "/") and not in_schema:
            return resolve(x)[0]
        return x

    data["pages"] = [walk(pg) if True else pg for pg in data["pages"]]
    return data


if __name__ == "__main__":
    data = build()
    with open(OUT, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print(f"wrote {OUT}: {len(data['pages'])} pages")
