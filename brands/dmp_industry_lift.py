"""Per-industry data for the creative-director industry pages (used by industry_page in digital-monitoring-products.content.py).
Hero clip, three proof numbers (each from DMP's own wording on dmp.com/products/industries), the heading of the
"what this building needs" spotlight and the products shown in the dark lineup (names, images and blurbs come from PRODUCTS)."""
IND_CLIP = {"commercial": "hero-loop-hq", "financial-institutions": "hero-signal-2", "retail": "hero-loop-campus", "government": "hero-signal-1",
            "industrial-manufacturing": "hero-loop-plant", "education": "hero-loop-campus", "healthcare-wellness": "hero-signal-1",
            "multi-tenant": "hero-loop-hq", "religious-institutions": "hero-signal-2", "storage-units": "hero-loop-plant", "residential": "hero-signal-2"}
IND_STATS = {"commercial": [["8", "Communication paths on the XR550"], ["3", "Paths on board the XT Series: network, cellular, dial-up"], ["5", "Systems from one manufacturer"]],
             "financial-institutions": [["256-bit", "AES available for alarm communications"], ["VAULT", "Panels never touch the public internet"], ["No servers", "To buy or maintain with Security Command"]],
             "retail": [["1 screen", "For enterprise-wide system and user management"], ["1", "Database for access and intrusion credentials"], ["1100", "Series wireless, with a compatibility guide"]],
             "government": [["256-bit", "AES built into the XR550E"], ["UL 634", "Level 2 sensors for SCIFs, sold through DMP"], ["USA", "Designed and built in the U.S.A."]],
             "industrial-manufacturing": [["0", "Extra wires between XR panels and X1 access"], ["1", "Unified solution for intrusion and access"], ["Real time", "AlarmVision camera analytics trigger alarms"]],
             "education": [["1 action", "Locks every public door"], ["3", "Ways to start a lockdown: app, keypad or any PC running Entré"], ["4", "Systems in one XR550 panel"]],
             "healthcare-wellness": [["4", "Systems in one XR550: access, intrusion, fire and video"], ["3", "Paths: network, digital dialer and LTE cellular"], ["FirstNet", "Approved communicators"]],
             "multi-tenant": [["Wallet", "Mobile credentials for residents and staff"], ["Access Only", "A Virtual Keypad level for amenities"], ["3", "Amenities named: pools, fitness centers, community rooms"]],
             "religious-institutions": [["100%", "Of DMP products are tested before shipping"], ["3", "Systems in the XT75: intrusion, access, AlarmVision"], ["1975", "Making security systems in Springfield"]],
             "storage-units": [["1", "Command for many panels on a site"], ["0", "Added wiring for site-wide lockdowns"], ["XR to XR", "Panels on one network work together"]],
             "residential": [["3", "Arming levels: Home, Sleep, Away"], ["All wireless", "XTLplus residential packages"], ["1 touch", "To pick the level"]]}
IND_NEED = {"commercial": "A commercial building needs more than a siren.", "financial-institutions": "A branch needs security that also runs the branch.",
            "retail": "Every store. One screen.", "government": "High-security hardware, built in the U.S.A.",
            "industrial-manufacturing": "One system for the door and the alarm.", "education": "Every public door, locked in one action.",
            "healthcare-wellness": "Secure the building and the data inside it.", "multi-tenant": "A key on the phone, and access to only what it should open.",
            "religious-institutions": "A small footprint with the full system inside.", "storage-units": "Many panels, one site, one command.",
            "residential": "Home, Sleep or Away, in one touch."}
IND_LINEUP = {"commercial": ["xr550", "xt75", "263lte", "7-inch-touchscreen-keypad", "vplus-7081-bdv", "entre-enterprise"],
              "financial-institutions": ["tmsentry", "xr550", "1142", "virtual-keypad", "263lte", "dealer-admin"],
              "retail": ["virtual-keypad", "xr150", "1100xh", "1100t", "vue-video-doorbell", "dealer-admin"],
              "government": ["xr550", "7-inch-touchscreen-keypad", "263lte-firstnet", "entre-enterprise", "734n", "vplus-7081-bdv"],
              "industrial-manufacturing": ["xr550", "x1", "xv-gateways-with-alarmvision", "vplus-7121-fe", "entre-enterprise", "263lte"],
              "education": ["xr550", "digital-key-credential", "mobile-credential", "dmp-bluetooth-reader-and-mobile-credential", "virtual-keypad", "entre-enterprise"],
              "healthcare-wellness": ["xr550", "263lte-firstnet", "7-inch-touchscreen-keypad", "entre-enterprise", "virtual-keypad", "1142"],
              "multi-tenant": ["xr550", "digital-key-credential", "mobile-credential", "dmp-bluetooth-reader-and-mobile-credential", "virtual-keypad", "x1"],
              "religious-institutions": ["xt75", "xv-gateways-with-alarmvision", "vplus-7061-fe", "graphic-touchscreen", "virtual-keypad", "1128"],
              "storage-units": ["xr550", "xr150", "xv-gateways-with-alarmvision", "x1", "vplus-7081-bdv", "virtual-keypad"],
              "residential": ["xtltouch", "xtlplus", "virtual-keypad", "265lte", "vue-video-doorbell", "1164"]}
SYSTEM_PHOTOS = {"intrusion": "tab-intrusion-1200.jpg", "access-control": "tab-access-1200.jpg", "fire": "tab-fire-1200.jpg", "video": "tab-video-1200.jpg"}
