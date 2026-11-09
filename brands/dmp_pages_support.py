"""DMP support family: support hub, technical FAQs (hub plus eight categories), documentation, dealer services,
design tools, A&E support, get a quote, become a dealer, sales directory, marketing, private label.
Written from the current dmp.com pages. Data only."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dmp_common import *

TECH = "Technical Support 888-436-7832, 7 a.m. to 7 p.m. Central"
TECH_HREF = "tel:+18884367832"
SUP = ["Home", "index.html"], ["Support", "support.html"]


def crumbs(*rest):
    return [["Home", "index.html"], ["Support", "support.html"]] + [list(r) for r in rest]


def steps(intro, items):
    return (intro + " " if intro else "") + " ".join(f"({i}) {s.rstrip('.')}." for i, s in enumerate(items, 1))


def parts(*pairs):
    return " ".join(f"{k}: {v.rstrip('.')}." for k, v in pairs)


# ------------------------------------------------------------------------------------------------ FAQ library
Q_CODES = ["What is the code to get into Programming, Diagnostics and Keypad Options?",
    "Programming: reset the panel by placing the reset jumper across the reset pins for two seconds, then removing it to one pin. At a keypad, press 6653 (PROG). XR Series panels need 6653 + CMD. If the keypad says ENTER CODE after you press PROG, enter the lockout code that the original installing company programmed. "
    "Diagnostics: reset the panel the same way, then at a keypad press 2313 (DIAG). XR Series panels need 2313 + CMD. The keypad screen displays DIAGNOSTICS. "
    "Keypad Options: on a 7800 Series keypad, scroll through the carousel menu and select Options, tap the wrench icon, press 3577 (INST) + CMD, then select KPD OPT to enter the keypad options menu."]
Q_DEFCODE = ["What is the default user code?",
    "Prior to 2020, the default user code for all panels was 99. As of 2020, the default user code is generated at DMP and printed on the box. Initializing user codes reverts the default code to 99. We strongly encourage every DMP dealer to change the user code once the installation is finished."]
Q_PROFILE = ["What profile number is the default user code assigned to?",
    "XR Series panels use profile numbers. The default user code is assigned to profile 99, the default master profile. XT Series and XTL Series panels use authority levels, and the default user code is assigned to the Master authority level."]
Q_FWVER = ["Where do I find the panel firmware version?",
    "The sticker on the panel shows the firmware it shipped with. For panels already installed, check XR Series panels under User Menu, System Status, and XT Series panels under Diagnostics, Panel Settings."]
FW_PANELS = " ".join([
    "XTLplus/XTLtouch: update in Dealer Admin individually or with a Bulk Update over network or cell, or update directly with a 399 cable or 401 module. In Remote Link, set the Connection Type to Direct with a Baud Rate of 38400.",
    "XT30/XT50: update in Dealer Admin individually or with a Bulk Update over network or cell; the panel must be at Hardware Level M or higher to use Dealer Admin. You can also update directly with a 399 cable or 401 module, with Remote Link set to Direct at 38400.",
    "XT75: can only be updated in Dealer Admin, individually or with a Bulk Update.",
    "XR100/XR500: can be updated over network or serial. Serial connections can be made on the J22 header or the J21 DB9 connector with the J23 jumper set to R.",
    "XR350: serial connections can be made on the LX500 header. To enable the header, open the Diagnostics Menu by pressing 2313 (DIAG) + CMD, select PC Programmer and connect within 60 seconds.",
    "XR150/XR550: update in Dealer Admin individually or with a Bulk Update over network or cell. Serial connections can be made on the LX500 header, enabled the same way as on the XR350.",
    "XF6: can only be updated in Dealer Admin, individually or with a Bulk Update.",
    "iCom: update directly with a 399 cable or 401 module, with Remote Link set to Direct at 38400.",
    "CellCom/DualCom: update in Dealer Admin individually or with a Bulk Update over network or cell, or directly with a 399 cable or 401 module, with Remote Link set to Direct at 38400."])
Q_FWUPDATE = ["How do I update the firmware in my panel?", FW_PANELS]
Q_COMMPATH = ["How do I program a Communication Path in my XR500 or XR150/350/550?",
    steps("Program it in the Communication section of the panel programming menu.", [
        "Set the panel Account Number and press CMD until prompted to enter the Path Number",
        "Enter the Path Number and press CMD",
        "Use a top row select key or area to choose a Communication Type (None, DD for Digital Dialer, NET, CID for Contact ID, or press CMD to move on to CELL or WiFi)",
        "Continue to configure the other settings for the path",
        "Enter the Phone Number (DD or CID) or IP Address (Net or Cell) of the Monitoring Center receiver",
        "Press CMD until STOP displays, then press a top row select key or area to save programming"])]
Q_ASSIST = ["Will DMP assist me with programming a panel?",
    "DMP Technical Support is happy to answer your programming questions, but no DMP employee is permitted to change your programming."]
Q_REPEATERS = ["How many 1100R wireless repeaters do DMP panels support?", "DMP panels support up to 8 repeaters."]
Q_DEALERCONN = ["I am unable to connect to my system from Dealer Admin or Virtual Keypad. What should I check?",
    "For systems connected over network, make sure the appropriate App Key is populated in Remote Options."]
Q_WTROUBLE = ["What does \"Wireless Trouble\" mean?",
    "Wireless Trouble means the panel and wireless receiver are not transmitting data back and forth. The on-board LEDs on the receiver verify power and communication (Power, RXD and TXD). On XR Series panels, the X-Bus Status option in the Diagnostics Menu (2313 + CMD) tests communication with the receiver. If a software version appears on the screen, the panel is communicating with the receiver. "
    "It is also possible that the tampers are not being depressed on the wireless receiver. The 1100X-W and 1100XH-W wireless receivers, which are compatible with any XR Series panel, have a case tamper and a wall tamper. Make sure both are depressed before you continue to troubleshoot. Note: Wireless Trouble does not show up for an issue with a wireless zone."]
Q_CELLFW = ["What firmware version do I need to install a cellular modem?",
    parts(("XT30/XT50 Control Panels", "version 213 (4/12/22) and higher"), ("XT75 Control Panels", "all versions"),
          ("XR150/550 Control Panels", "version 213 (4/8/22) and higher"), ("XF6 Series Fire Control Panels", "all versions"))]
Q_PUSH = ["How do push notifications work?",
    "Push notifications are enabled on the user's mobile device with the Virtual Keypad app. In Settings, the user chooses whether to receive push notifications for Alarms, Troubles and Arms/Disarms. Additional push notifications can be sent for Sensor Activity. That option only appears if it is enabled on the system in Dealer Admin, and users can receive sensor activity notifications from up to 50 different zones programmed into the panel. "
    "Push notifications follow the primary communication type set in Dealer Admin. If the system uses EasyConnect in Dealer Admin, the panel's main communication must be Network or WiFi and port 7001 TCP outbound must be open. If the system uses Cell in Dealer Admin, the panel's communication must be Cellular."]
Q_EASY = ["What do I need to program in my panel for EASYconnect App Connections?",
    "Program the App Key in the Remote Options menu during panel programming. To find the App Key, each dealer can look at their Dealer Settings in Dealer Admin. EASYconnect connections are available on network XT Series panels with version 112 (10/5/2012), on XR150/550 panels and on XTLplus/XTLTouch panels. Port 4001 TCP must be open outbound. The App Key is not needed for cellular-only panels."]
Q_CARD = ["How do I program the panel to disarm and gain access on a card swipe?",
    "The 734 or module that controls the door must have the area the user wants to access and disarm programmed as the access area for the device in Device Setup. Users who swipe at the reader must also have a profile that can access and disarm that same area or areas."]
Q_WLZONES = ["Where do wireless zone numbers start on XR panels?",
    parts(("XR100/XR150", "zones 500-599"), ("XR500/XR550", "zones 500-999")) + " Note: watch for existing hardwired zones or hardwired outputs already programmed on the LX expansion bus."]
Q_KEYFOB = ["Where do I program key fobs into the panel?",
    parts(("XT30/XT50", "zone numbers 31-34 and 41-44"), ("XTLplus/XTLTouch", "zone numbers 51-54 and 61-64"), ("XR100/XR500 and XR150/XR350/XR550", "zone numbers 400-449"))]
Q_KPADDR = ["How do I address a keypad?",
    "Thinline keypads: " + steps("", ["Hold down the Back Arrow and CMD keys for two seconds", "At Set Brightness, enter 3577 + CMD",
        "Press the top row select key under KPD OPT to select Keypad Options", "Press any top row select key to clear the default keypad address, which is 01",
        "Enter the new keypad address and press CMD", "Program the keypad device number in Device Setup to match the new address"]) +
    " Touchscreen keypads: " + steps("", ["Press Options in the carousel menu", "Press the Installer Options wrench icon", "Enter 3577 + CMD",
        "Press the top row select area under KPD OPT to select Keypad Options", "Press any top row select area to clear the default keypad address, which is 01",
        "Enter the new keypad address and press CMD", "Program the keypad device number in Device Setup to match the new address"])]
Q_REMOTELINK = ["How do I connect to my panel with Remote Link?", " ".join([
    "XT30/50, XTL, XTLplus and XTLtouch: in Remote Link, set the Connection Type to Direct with a Baud Rate of 38400. These panels connect and program over network or cell, or by dialer on the XT30/50D, and a 399 cable or 401 module can update firmware directly.",
    "XR100/500: set the Connection Type to Direct with a Baud Rate of 9600. These panels connect over network, dialer, cell or serial. Serial connections must use the J22 header or the J21 DB9 connector with the J23 jumper set to R.",
    "XR150/350/550: set the Connection Type to Direct with a Baud Rate of 38400. These panels connect over network, dialer, cell or serial. Serial connections use the LX500 header with a 399 cable or 401 module; to enable the header, open diagnostics (2313 + CMD), select PC Programmer and connect within 60 seconds.",
    "CellCom/iCom/DualCom: set the Connection Type to Direct with a Baud Rate of 38400. These connect over cellular or network, and a 399 cable or 401 module can update firmware directly."])]
Q_RLDOWNLOAD = ["Where do I download Remote Link software and updates?", "Remote Link software is available for download in Dealer Admin under Resources, then Downloads."]
Q_ANTENNA = ["Where do I install the wireless antenna on the XT50?",
    "The XT50 wireless antenna terminal block is in the top right corner of the circuit board. The antenna installs through a small opening in the top of the enclosure and attaches to the panel at the right terminal. The left terminal is not used."]
Q_LOWBAT = ["How do I clear a low battery message for wireless devices?",
    "Replace the battery and perform a sensor reset by pressing Reset on a Touchscreen keypad or by pressing and holding the 2 key on a Thinline keypad."]
Q_RECEIVERS = ["What are the compatible wireless receivers for each DMP control panel?",
    parts(("XT30/XT50", "1100DH"), ("XT75", "1100XH"), ("XR150/XR550", "1100XH"))]
Q_AUTOARM = ["I want the panel to auto arm but not auto disarm. Do I need an opening time on the schedule?",
    "Yes. You need an Open Time even if you are not automatically disarming. If you do not want the panel to disarm automatically, do not enable Auto Disarm."]
Q_WLTEST = ["How do I test my wireless zones?",
    "There are two ways to test DMP wireless communication. Option 1, the wireless test: " + steps("", [
        "Reset the control panel by shorting the RESET header or pressing the RESET button, depending on the panel",
        "At a keypad, press 8144 (WALK), then CMD on XR panels",
        "Press CMD until the WLS option displays and select it"]) +
    " This starts a wireless check-in test that runs for five minutes and checks the consistency of your signals. Zones that fail need to be relocated, or a repeater should be added. The panel shows how many transmitters are checking in, and when the test ends it shows which transmitters failed, if any. You can also run it in Dealer Admin under System Tests, Wireless Test. "
    "Option 2, the transmitter LED, built into all 1100 Series wireless products: with the cover removed, hold the transmitter in the desired location and press the tamper switch to send data to the panel. If communication is confirmed, the LED blinks immediately on and immediately off for each press or release of the tamper switch; repeat the test until you see five consecutive blinks. If communication is faulty, the LED stays on for about 8 seconds or flashes several times in quick succession. Relocate the transmitter or the wireless receiver until the LED confirms clear communication."]
Q_REPEATERSETUP = ["Do I program my wireless repeater as a device in Device Setup programming?",
    "No. Repeaters are programmed as zones in the control panel. If several repeaters go on the same system, they must be programmed with sequential zone numbers. Program repeaters as Auxiliary Type zones, with the Disarmed Open and Disarmed Short messages set to Trouble and the Armed Open and Armed Short messages set to Alarm in Advanced Zone Programming."]
Q_KPSTOP = ["Why has the keypad stopped working after exiting Programming?",
    "The most common cause is an address conflict with wireless zones that occupy the same address as the keypad. For example, the keypad is set at address 1 and wireless zones 11-14 were just added. Either change the keypad address or reprogram the zones at the next available address."]
Q_GUIDES = ["Where can I find installation, programming and user's guides?",
    "In the documentation library, which also holds the General Troubleshooting Guide. Spec sheets, quick start guides, technical updates and more are there too."]
Q_GLOSSARY = ["How can I learn more about DMP and industry terminology?",
    "DMP publishes a glossary of terms and definitions relevant to DMP and the security industry. Ask Technical Support at 888-436-7832 for the current link."]

CATS = {
 "access-control": {
    "label": "Access control", "short": "Access Control",
    "heading": "Why the door will not open: six denied messages and what each one means.",
    "sub": "Card swipes that disarm, key fobs by panel and the access denied messages in the panel event history.",
    "image": IMG + "tab-access-1200.jpg", "alt": "A phone held to a door reader", "w": 1200, "h": 900,
    "blurb": "Card swipe programming, key fob zones and what each access denied message means.",
    "sections": [("Programming doors, credentials and key fobs", [Q_CARD, Q_KEYFOB]),
                 ("Reading the access denied messages", [["Why is the door not unlocking after presenting a credential to the reader?",
                    "These access denied messages appear in the panel event history. " + " ".join([
                    "Invalid Code: the code read from the card does not match any user code in the panel.",
                    "Invalid Time: access was attempted outside the schedule assigned to the user's profile.",
                    "Invalid Area: the user attempted to access an area that is not defined in their profile.",
                    "Invalid Level: door access is not enabled in the user's profile, or the system is in lockdown.",
                    "Armed Area: the user attempted to access an armed area they do not have the authority to disarm.",
                    "Inactive User: the user is marked as inactive in User Codes."])]])],
    "related": [("Control panel FAQs", "Codes, firmware and Remote Link for the panel behind the door.", "support/tech-faqs/control-panel.html"),
                ("Access control products", "Readers, credentials, door modules and Entré.", "services/access-control.html"),
                ("Documentation library", "Installation and programming guides for door modules.", "support/documentation.html")]},
 "cellular-network-communication": {
    "label": "Cellular and network communication", "short": "Cellular and Network",
    "heading": "Where the cellular status failure chart lives, and which firmware each modem needs.",
    "sub": "Diagnostics errors on a cellular communicator and the panel firmware that has to be in place before a cellular modem goes in.",
    "image": IMG + "p-263lte-1200.png", "alt": "The DMP 263LTE cellular communicator", "w": 1200, "h": 995,
    "blurb": "Cell diagnostics errors and the firmware version each cellular modem needs.",
    "sections": [("Diagnostics errors on a cellular communicator", [["Cellular communication is not working and when I run a diagnostics test, I get an error. What does it mean?",
                    "The Cell Status Failure Identification Chart is on page 30 of the DMP Troubleshooting Guide. It summarizes the possible error messages, what they mean and the steps to troubleshoot each one."]]),
                 ("Firmware needed before you install a cellular modem", [Q_CELLFW,
                    ["Which firmware do older cellular modems need?",
                     parts(("463C", "XR100/500 version 211 (9/21/12)"), ("464-263C and 464-263H", "XR100/500 version 212 (3/15/13)"),
                           ("263H and 263C (Enfora chipset)", "XT30/50 version 112 and XR150/350/550"),
                           ("263C (Telit chipset)", "XT30/50 version 124 (1/21/16) and XR150/350/550 version 109 (8/18/2015)"),
                           ("263LTE-V", "XT30/50 version 212 (1/10/19) and XR150/350/550 version 212 (12/20/18)"),
                           ("263LTE-A", "XT30/50 version 192 (8/23/18) and XR150/350/550 version 193 (12/19/19)"),
                           ("263LTE-V5", "XR500 version 213 (11/21/18)"),
                           ("265LTE-V", "XTLPlus/XTLTouch version 212 (1/10/19)"),
                           ("265LTE-A", "XTLPlus/XTLTouch version 192 (8/23/18)"))]])],
    "related": [("Control panel FAQs", "Firmware updates, Communication Paths and Remote Link.", "support/tech-faqs/control-panel.html"),
                ("Communicator products", "Cellular and network communicators.", "services/communicators.html"),
                ("Documentation library", "The DMP Troubleshooting Guide and technical updates.", "support/documentation.html")]},
 "control-panel": {
    "label": "Control panels", "short": "Control Panels",
    "heading": "Programming codes, firmware and Remote Link settings for XT, XTL and XR panels.",
    "sub": "The codes that open Programming and Diagnostics, where the default user code comes from, and every firmware update path by panel.",
    "image": IMG + "tab-intrusion-1200.jpg", "alt": "The DMP XT75 control board", "w": 1200, "h": 900,
    "blurb": "Programming and diagnostics codes, firmware updates, Remote Link, wireless and keypad setup by panel.",
    "sections": [("Codes, default users and who can change programming", [Q_CODES, Q_DEFCODE, Q_PROFILE, Q_ASSIST, Q_FWVER]),
                 ("Firmware, Remote Link and communication paths", [Q_FWUPDATE, Q_REMOTELINK, Q_COMMPATH, Q_CELLFW, Q_DEALERCONN]),
                 ("Wireless devices on the panel", [Q_RECEIVERS, Q_WTROUBLE, Q_REPEATERS, Q_WLZONES, Q_KEYFOB, Q_ANTENNA, Q_LOWBAT]),
                 ("Keypads, schedules, access and app connections", [Q_KPADDR, Q_AUTOARM, Q_CARD, Q_PUSH, Q_EASY])],
    "related": [("Keypad FAQs", "Address a keypad and update its firmware.", "support/tech-faqs/keypads.html"),
                ("Wireless FAQs", "Testing zones, repeaters and receivers.", "support/tech-faqs/wireless.html"),
                ("Panel and keypad products", "Control panels, keypads, modules and expanders.", "services/panels-keypads.html")]},
 "keypads": {
    "label": "Keypads", "short": "Keypads",
    "heading": "Address a keypad, update its firmware and get into installer options.",
    "sub": "Firmware updates for the 5-Inch (7800/9800) and 7-Inch (8860) touchscreen keypads, keypad addressing and the installer code.",
    "image": IMG + "p-9800-series-1200.png", "alt": "A DMP 9800 Series touchscreen keypad", "w": 1200, "h": 800,
    "blurb": "Firmware updates for 5-Inch and 7-Inch touchscreen keypads, addressing and installer options.",
    "sections": [("Updating keypad firmware", [
                    ["How do I update the firmware in my 5-Inch Graphic Touchscreen Keypad (7800/9800)?",
                     "Version 107 or later: " + steps("", ["Download the firmware update from DMP's Product Software Downloads page", "Unzip the file onto a FAT32 formatted Micro-SD card",
                        "Insert the card into the slot on the right of the keypad", "Power cycle the keypad or select Restart from the Keypad Options Menu"]) +
                     " Version 106 or earlier: " + steps("", ["Contact the Customer Repair Center", "Request an update to the latest firmware version", "Send the keypad in to DMP to be updated"])],
                    ["How do I update the firmware in my 7-Inch Touchscreen Keypad (8860)?",
                     "Update from Dealer Admin: " + steps("", ["Make sure the keypad is connected to the Wi-Fi network", "Go to Dealer Admin", "Select the user and system", "Next to the keypad name, select Update"]) +
                     " Update in Installer Options: " + steps("", ["Make sure the keypad is connected to the Wi-Fi network", "Select Options from the carousel menu, then Installer Options", "Enter 3577 and press CMD", "Select Check for Updates and follow the on-screen prompts"])]]),
                 ("Addressing keypads and getting in", [Q_KPADDR, Q_KPSTOP, Q_CODES])],
    "related": [("Control panel FAQs", "Codes, firmware and Remote Link by panel.", "support/tech-faqs/control-panel.html"),
                ("Panel and keypad products", "Thinline, touchscreen and Aqualite keypads.", "services/panels-keypads.html"),
                ("End-user training", "Keypad how-to videos for customers.", "training/end-user-training.html")]},
 "mobile-platforms": {
    "label": "Mobile platforms", "short": "Mobile Platforms",
    "heading": "Virtual Keypad help files, App Keys and push notifications, answered.",
    "sub": "Where the Virtual Keypad and Panel to Panel help files are, what to check when an app will not connect and how push notifications are enabled.",
    "image": IMG + "tab-mobile-1200.jpg", "alt": "Virtual Keypad and Dealer Admin on laptop, tablet and phone", "w": 1200, "h": 900,
    "blurb": "Help files, App Keys, EASYconnect, push notifications and Remote Link downloads.",
    "sections": [("Help files for Virtual Keypad and Panel to Panel", [
                    ["How do I find the Virtual Keypad App Help File?", "The Virtual Keypad App Help File is at virtualkeypadapp.dmp.support/vka."],
                    ["How do I find the Virtual Keypad Browser Help File?", "The Virtual Keypad Browser Help File is at virtualkeypaddesktop.dmp.support/vh."],
                    ["How do I find the Panel to Panel Communication Help File?", "The Panel to Panel Communication Help File is at paneltopanel.dmp.support/ptp."]]),
                 ("Connecting the app and sending notifications", [Q_DEALERCONN, Q_PUSH, Q_EASY]),
                 ("Schedules, Remote Link and default codes", [Q_AUTOARM, Q_RLDOWNLOAD, Q_DEFCODE])],
    "related": [("Control panel FAQs", "App Keys, Remote Options and communication paths.", "support/tech-faqs/control-panel.html"),
                ("Mobile and automation products", "Virtual Keypad and automation.", "services/mobile-automation.html"),
                ("End-user training", "How-to videos for Virtual Keypad.", "training/end-user-training.html")]},
 "monitoring-center": {
    "label": "Monitoring center", "short": "Monitoring Center",
    "heading": "Digital Key privacy, panel firmware updates and receiving signals on an SCS-1R or SCS-VR.",
    "sub": "What the Digital Key does and does not track, every panel firmware update path, Remote Link settings and the network traffic a receiver needs.",
    "image": IMG + "p-scs-1r-1200.png", "alt": "The DMP SCS-1R receiver", "w": 1200, "h": 800,
    "blurb": "Digital Key privacy, panel firmware updates, Remote Link and SCS-1R or SCS-VR signal handling.",
    "sections": [("Digital Key privacy and revoking credentials", [
                    ["Will the DMP Digital Key track my personal data during the install or operations?",
                     "No. Adding and using the Digital Key in an Apple or Android Wallet requires a valid email address for wallet login validation and to email credential notifications. If credentials are distributed by SMS text, a mobile phone number is required."],
                    ["Will the DMP Digital Key track my phone location?", "No. DMP does not use or require location services to use the Digital Key."],
                    ["Can the Digital Key be set up so that I do not have to unlock my phone?", "Yes, by enabling the Mobile Wallet Express mode for the Digital Key credential."],
                    ["How do I get the Digital Key back from a user that leaves the company?", "Digital Keys are revoked and expired remotely in Virtual Keypad, without needing anything from the user."]]),
                 ("Panel firmware and Remote Link", [Q_FWUPDATE, Q_RLDOWNLOAD,
                    ["How do I connect to my panel with Remote Link?", Q_REMOTELINK[1]]]),
                 ("Receiving and acknowledging signals", [["What do I need to receive signals and acknowledge them with my SCS-1R or SCS-VR?",
                    "Your public IP address should receive signals on the port you choose in Communication programming, and those signals should route into your network to the correct SCS-1R Line Card or SCS-VR Group. The same ports should be open outbound for TCP so the receiver can respond to Network signals, and ALL UDP should be open outbound to acknowledge cellular signals, because of the way cellular communicates. "
                    "Your SCS-1R or SCS-VR receiver also needs automation software so your Monitoring Center operator knows what signal came in, which system and who to contact. Direct automation questions to your automation company."]])],
    "related": [("Control panel FAQs", "Codes, firmware versions and communication paths.", "support/tech-faqs/control-panel.html"),
                ("Access control products", "Digital Key and mobile credentials.", "services/access-control.html"),
                ("Communicator products", "Cellular and network communicators.", "services/communicators.html")]},
 "video": {
    "label": "Video", "short": "Video",
    "heading": "Camera will not add to Dealer Admin? Reset 4000, 5000 and 6000 Series cameras this way.",
    "sub": "Which ports to open outbound for video, and the factory reset for each camera series.",
    "image": IMG + "tab-video-1200.jpg", "alt": "A VUE Plus camera", "w": 1200, "h": 900,
    "blurb": "Outbound ports for video and the factory reset for 4000, 5000 and 6000 Series cameras.",
    "sections": [("Network ports and camera resets", [
                    ["What ports need to be open to allow video?", "Document LT-2048 lists the ports to open outbound for each video product. Find your product in that document to see which ports apply."],
                    ["What do I do if the camera will not add to Dealer Admin?",
                     "Try resetting the camera. 4000/5000 Series cameras: " + steps("", ["Hold the reset button", "Unplug the camera and plug it back in while continuing to hold reset for 30 seconds, which factory resets the device"]) +
                     " 6000 Series cameras: " + steps("", ["Unplug the camera", "Wait one minute after it is powered up, but not more than 10 minutes, and hold the reset button for 30 seconds, which factory resets the device"])]])],
    "related": [("Video products", "VUE and VUE Plus cameras, XV Plus gateways and AlarmVision.", "services/video.html"),
                ("Documentation library", "Spec sheets and quick start guides for cameras.", "support/documentation.html"),
                ("Control panel FAQs", "Dealer Admin connections and App Keys.", "support/tech-faqs/control-panel.html")]},
 "wireless": {
    "label": "Wireless", "short": "Wireless",
    "heading": "Wireless Trouble, zone numbers and 1100R repeaters, explained.",
    "sub": "What Wireless Trouble means, how to test every wireless zone, where zone numbers start on XR panels and which receiver goes with which panel.",
    "image": IMG + "p-1100xh-1200.png", "alt": "The DMP 1100XH wireless receiver", "w": 1200, "h": 823,
    "blurb": "Wireless Trouble, zone tests, repeaters, receivers and low battery messages.",
    "sections": [("Receivers, repeaters and zone numbers", [Q_RECEIVERS, Q_REPEATERS, Q_REPEATERSETUP, Q_WLZONES, Q_ANTENNA]),
                 ("Troubleshooting and testing wireless", [Q_WTROUBLE, Q_WLTEST, Q_LOWBAT])],
    "related": [("Control panel FAQs", "Wireless receivers and key fobs by panel.", "support/tech-faqs/control-panel.html"),
                ("Wireless products", "1100 Series transmitters, receivers and repeaters.", "services/wireless.html"),
                ("Documentation library", "Installation guides for wireless devices.", "support/documentation.html")]},
}
ORDER = ["access-control", "cellular-network-communication", "control-panel", "keypads", "mobile-platforms", "monitoring-center", "video", "wireless"]


def qcount(c):
    return sum(len(items) for _, items in CATS[c]["sections"])


def faq_url(c): return f"support/tech-faqs/{c}.html"


def still_stuck(topic):
    return {"type": "detail", "alt": True, "eyebrow": "Still stuck?", "heading": f"Not answered here? Call Technical Support on 888-436-7832.",
            "body": f"Technical Support helps with installation, programming, troubleshooting and diagnostic issues, including {topic}. It is open from 7 a.m. to 7 p.m. Central, and TechSupport@DMP.com is the email address. DMP Technical Support is glad to answer programming questions, but no DMP employee is permitted to change your programming.",
            "bullets": ["Technical Support: 888-436-7832, 7 a.m. to 7 p.m. Central", "Email TechSupport@DMP.com", "Dealers order at buy.DMP.com, 24 hours a day", "Customer Service for orders: 866-266-2826, 8 a.m. to 6 p.m. Central"]}


def cat_page(c):
    d = CATS[c]
    secs = [{"type": "hero", "layout": "split", "eyebrow": f"Technical FAQs: {d['label'].lower()}", "heading": d["heading"], "subhead": d["sub"],
             "primary": {"label": "Call Technical Support", "href": TECH_HREF}, "secondary": {"label": "All technical FAQs", "href": "support/tech-faqs.html"},
             "image": d["image"], "image_alt": d["alt"], "image_w": d["w"], "image_h": d["h"]}]
    for head, items in d["sections"]:
        secs.append({"type": "faq", "heading": head, "items": [list(i) for i in items]})
    secs.append({"type": "services", "heading": "Related answers and products", "intro": "Keep going from here.", "items": [list(r) for r in d["related"]]})
    secs.append(still_stuck(d["label"].lower()))
    secs.append(LEADFORM)
    allq = [i for _, items in d["sections"] for i in items]
    return {"file": faq_url(c), "title": title(f"{d['label']} technical FAQs"),
            "description": desc(f"{d['label']} technical FAQs from DMP Technical Support: {d['blurb']}"),
            "crumbs": crumbs(["Technical support FAQs", "support/tech-faqs.html"], [d["label"], faq_url(c)]),
            "schema": [itemlist(f"{d['label']} technical FAQs", [[q, faq_url(c)] for q, _ in allq])],
            "sections": secs}


PAGES = []

# ------------------------------------------------------------------------------------------------ support hub
HOLIDAYS = [["New Year's Day", "Thursday, January 1"], ["Memorial Day", "Monday, May 25"], ["Independence Day", "Friday, July 3"],
            ["Labor Day", "Monday, September 7"], ["Thanksgiving", "Thursday, November 26"], ["Day After Thanksgiving", "Friday, November 27"],
            ["Christmas Eve", "Thursday, December 24"], ["Christmas Day", "Friday, December 25"]]
PAGES.append({"file": "support.html", "title": title("Support and contacts"),
    "description": desc("Four phone lines with hours: Inside Sales, Technical Support, Customer Service and SecureCom Wireless. Plus FAQs, documentation, dealer services and 2026 closures."),
    "crumbs": [["Home", "index.html"], ["Support", "support.html"]],
    "schema": [{"@context": "https://schema.org", "@type": "ContactPage", "name": "DMP support and contacts", "mainEntity": {
        "@type": "Organization", "name": CLIENT, "contactPoint": [
            {"@type": "ContactPoint", "contactType": "sales", "telephone": "+1-877-757-4367", "email": "InsideSales@DMP.com", "hoursAvailable": "Mo-Fr 08:00-17:00"},
            {"@type": "ContactPoint", "contactType": "technical support", "telephone": "+1-888-436-7832", "email": "TechSupport@DMP.com", "hoursAvailable": "Mo-Fr 07:00-19:00"},
            {"@type": "ContactPoint", "contactType": "customer service", "telephone": "+1-866-266-2826", "email": "CustomerService@DMP.com", "hoursAvailable": "Mo-Fr 08:00-18:00"}]}}],
    "sections": [
        {"type": "hero", "layout": "split", "eyebrow": "Support and contacts", "heading": "Technical Support picks up from 7 a.m. to 7 p.m. Central.",
         "subhead": "Four phone lines, each run by the team that owns the answer: Inside Sales, Technical Support, Customer Service and SecureCom Wireless. Times below are Central.",
         "primary": {"label": "Call Technical Support 888-436-7832", "href": TECH_HREF}, "secondary": {"label": "Technical FAQs", "href": "support/tech-faqs.html"},
         "image": IMG + "hq-exterior-1200.jpg", "image_alt": "The DMP headquarters in Springfield, Missouri, with the American flag in front", "image_w": 1200, "image_h": 800},
        {"type": "cards", "alt": True, "eyebrow": "Pick the right line", "heading": "Who to call for what, with hours and email",
         "items": [["Inside Sales: 877-757-4367", "System design, architect and engineer support, pre-sales support, quotes and pricing, and Dealer Direct assistance. 8 a.m. to 5 p.m. Central. InsideSales@DMP.com."],
                   ["Technical Support: 888-436-7832", "Installation, programming, troubleshooting and diagnostic issues. 7 a.m. to 7 p.m. Central. TechSupport@DMP.com."],
                   ["Customer Service: 866-266-2826", "Products and ordering, software activations, the Buy Site, shipping and order entry questions. 8 a.m. to 6 p.m. Central. CustomerService@DMP.com."],
                   ["SecureCom Wireless: 877-300-8030", "Activation or billing questions. 8 a.m. to 5 p.m. Central. CustomerService@SecureComWireless.com. Website: SecureComWireless.com."]]},
        {"type": "resources", "heading": "Fixing something or learning a product? Start with one of these four.", "intro": "Answers, documents, courses and wireless service.",
         "items": [["Answers", "Technical FAQs", "Codes, firmware, Remote Link, wireless zones and more, in eight categories.", "Open the FAQs", "support/tech-faqs.html"],
                   ["Documents", "Documentation library", "Spec sheets, installation and programming guides, quick start guides and technical updates.", "Open the library", "support/documentation.html"],
                   ["Courses", "Training", "DMP University, technical, sales and end-user training.", "See training", "training.html"],
                   ["Service", "SecureCom Wireless", "Activation and billing for cellular service on SecureComWireless.com.", "Go to SecureComWireless.com", "https://securecomwireless.com/"]]},
        {"type": "resources", "heading": "Specifying, selling or signing up as a dealer? These eight pages cover it.", "intro": "Tools for designers and dealers, and how to become one.",
         "items": [["Design", "Design tools", "Design DMP systems on a digital floor plan and generate a bill of materials.", "Open design tools", "support/design-tools.html"],
                   ["Specifications", "A&E support", "A&E specs and CAD drawings for panels, enclosures, modules, keypads and wireless.", "Open A&E support", "support/ae-support.html"],
                   ["Quotes", "Get a quote", "Tell us what you are specifying and where. A person will reply.", "Get a quote", "support/get-a-quote.html"],
                   ["Partners", "Integration partners", "Technology partners whose products work with DMP systems.", "See partners", "partners.html"],
                   ["Dealers", "Dealer services", "Dealer Admin, Dealer Account, firmware, the Customer Return Center and the warranty.", "See dealer services", "support/dealer-services.html"],
                   ["Join", "Become a dealer", "How the application works and what we look for in a dealer.", "Apply", "support/become-a-dealer.html"],
                   ["Marketing", "Marketing support", "Marketing Central assets, custom videos and print at our cost.", "See marketing support", "support/marketing.html"],
                   ["Branding", "Private label", "Custom keypads, Digital Keys, branded readers and credentials.", "See private label", "support/private-label.html"]]},
        {"type": "services", "alt": True, "heading": "Find your regional sales manager, or a distributor outside the U.S.",
         "intro": "The directory lists titles and territories, and Inside Sales routes the call.",
         "items": [["Sales regions and regional sales managers", "From the Carolinas and New England to Four Corners and Los Angeles, each region has a regional sales manager.", "support/sales-directory.html"],
                   ["International distributors", "DMP products are available through authorized dealers and distributors outside the United States.", "international.html"],
                   ["Not sure who to call?", "Inside Sales at 877-757-4367 will point you to the right person.", "contact.html"]]},
        {"type": "cards", "eyebrow": "2026 holiday closures", "heading": "We are closed on eight days in 2026, from New Year's Day to Christmas Day.",
         "items": [list(h) for h in HOLIDAYS]},
        LEADFORM]})

# ------------------------------------------------------------------------------------------------ technical FAQ hub
hub_faq = [Q_GUIDES, Q_GLOSSARY, Q_CODES, Q_DEFCODE, Q_FWUPDATE]
PAGES.append({"file": "support/tech-faqs.html", "title": title("Technical support FAQs"),
    "description": desc(f"Technical FAQs from DMP Technical Support in eight categories, {sum(qcount(c) for c in ORDER)} answers on codes, firmware, Remote Link, wireless, keypads and more."),
    "crumbs": crumbs(["Technical support FAQs", "support/tech-faqs.html"]),
    "schema": [itemlist("DMP technical FAQ categories", [[CATS[c]["label"], faq_url(c)] for c in ORDER])],
    "sections": [
        {"type": "hero", "layout": "split", "eyebrow": "Technical FAQs", "heading": "Panel codes, firmware versions and wireless zone numbers, answered in one place.",
         "subhead": "Eight categories of answers from DMP Technical Support, written for the dealer standing at the panel.",
         "primary": {"label": "Call Technical Support", "href": TECH_HREF}, "secondary": {"label": "Documentation library", "href": "support/documentation.html"},
         "image": IMG + "tab-intrusion-1200.jpg", "image_alt": "The DMP XT75 control board", "image_w": 1200, "image_h": 900},
        {"type": "resources", "heading": "Pick the product family you are working on.", "intro": "Each category lists every question and answer.",
         "items": [[f"{qcount(c)} questions", CATS[c]["label"], CATS[c]["blurb"], f"Open {CATS[c]['label'].lower()} FAQs", faq_url(c)] for c in ORDER]},
        {"type": "faq", "heading": "Five answers dealers look up most: guides, glossary, codes and firmware", "items": [list(q) for q in hub_faq]},
        {"type": "services", "alt": True, "heading": "Also useful at the panel", "intro": "Documents, courses and the phone.",
         "items": [["Documentation library", "Installation and programming guides, quick start guides, spec sheets and technical updates.", "support/documentation.html"],
                   ["Technical training", "Courses for the people installing and programming DMP systems.", "training/technical-training.html"],
                   ["Support hub", "Every phone line with hours and email.", "support.html"]]},
        still_stuck("any question not covered in these eight categories"),
        LEADFORM]})
for c in ORDER:
    PAGES.append(cat_page(c))

# ------------------------------------------------------------------------------------------------ documentation
DOC_TYPES = [
    ["Spec sheets", "One product, its specifications and ordering details: what you need to specify it.",
     "Examples: XV Plus Gateway Series Spec Sheet; XR550 Spec Sheet; VUE 5MP Cameras Spec Sheet; Virtual Keypad Spec Sheet."],
    ["Installation and programming guides", "Step by step wiring, mounting and programming for installers.",
     "Examples: 734A Access Control Wireless Lock Integration Module Installation and Programming Guide; 1140INT Wireless Horn Strobe Installation Guide; XT75 Installation and Programming Guide."],
    ["Quick start guides", "The short version for getting a device running.",
     "Examples: 8863 7-Inch Touchscreen Keypad Quick Start Guide; 8862 7-Inch Touchscreen Keypad Quick Start Guide."],
    ["Technical updates", "What changed in a release of firmware, software or hardware.",
     "Examples: SCS-VR Version 1.5.3 (10/8/26) Technical Update; VUE Video Doorbell Version 142 (10/22/26) Technical Update; 8862/8863 Keypads Version 347.1.0.1707 Technical Update; 714-8/16 and 715-8/16 Zone Expansion Module Hardware Update."],
    ["Marketing literature", "Sales sheets and brochures to put in front of a customer or specifier.",
     "Examples: 8800 Series Sales Sheet: More of What You Need; XV Plus Gateway Feature Matrix; VUE and VUE Plus Camera Comparison; International Security Applications Guide."],
    ["White papers", "Longer reading on a security problem and how DMP systems address it.",
     "Examples: How to Maximize Your Security for Multiple Locations White Paper; National Retail Security White Paper; Traffic Count Systems in Retail Applications White Paper; DMP Control Panels."],
    ["Case studies", "Customer stories that show a system doing its job.",
     "Examples: Transforming Reactive Security into Proactive Protection Case Study; Customer Success Story: A Small Sensor. A Big Save."],
    ["Training videos", "Short videos that show how to use a product or sell it.",
     "Examples: Virtual Keypad How-To; 7-Inch Keypad How-To; Replacing Batteries How-To; AlarmVision; VUE Video Doorbell."]]
SYS = [("intrusion", "Intrusion"), ("access-control", "Access control"), ("fire", "Fire"), ("video", "Video"), ("communicators", "Communicators"),
       ("wireless", "Wireless"), ("panels-keypads", "Panels and keypads"), ("mobile-automation", "Mobile and automation")]
PAGES.append({"file": "support/documentation.html", "title": title("Technical documentation library"),
    "description": desc("The DMP document library: spec sheets, installation and programming guides, quick start guides, technical updates, white papers, case studies and videos."),
    "crumbs": crumbs(["Documentation", "support/documentation.html"]),
    "sections": [
        {"type": "hero", "layout": "split", "eyebrow": "Documentation library", "heading": "More than 900 documents, from XR550 spec sheets to VUE Video Doorbell updates.",
         "subhead": "Every document type we publish, what each one is for and real titles to look for. Filter the library by product category, document type and file type.",
         "primary": {"label": "Ask Technical Support", "href": TECH_HREF}, "secondary": {"label": "Technical FAQs", "href": "support/tech-faqs.html"},
         "image": IMG + "tab-spec-1200.jpg", "image_alt": "A tablet showing a floor plan in System Surveyor", "image_w": 1200, "image_h": 900},
        {"type": "cards", "alt": True, "eyebrow": "Eight document types", "heading": "Which document answers which question", "items": [[f"{t}", f"{w} {ex}"] for t, w, ex in DOC_TYPES]},
        {"type": "detail", "eyebrow": "And more in the library", "heading": "Many more types, from battery calculators to CAD drawings",
         "body": "The library holds more than the eight headline types. Filter by resource type to reach any of these, and by file type (PDF, XLSX, PPTX or ZIP).",
         "bullets": ["A&E specs and CAD drawings (see A&E support)", "Application notes, tech tips and how-to guides", "Battery calculators and compatibility guides", "Compliance guides, compliance notes and compliance statements",
                     "Help files, user guides and quick reference cards", "Programming sheets and installation sheets", "System design guides and lab guides", "Training presentations and sales training notes", "Dealer Digest issues"]},
        {"type": "detail", "alt": True, "eyebrow": "Filter by product category", "heading": "Sixteen product categories, plus international variants",
         "body": "Start from the part of the system you are working on: Access Control, Automation, Cell and Network Communicators, Control Panels, Dealer Admin, Entré Software, Fire, Intrusion, Keypads, Software Platforms, Modules and Expanders, Monitoring Center, Power Supplies, Video, Virtual Keypad and Wireless. International versions of communicators, control panels, keypads, modules and expanders, power supplies and wireless have their own categories.",
         "bullets": ["Search by model number, for example XT75 or 1100", "Narrow to one document type, such as Technical Updates", "Open the PDF, spreadsheet, presentation or archive you need"]},
        {"type": "resources", "heading": "Browse the product lines whose documents you need", "intro": "Each system page links to its products and their documents.",
         "items": [[n, f"{n} documents", f"Spec sheets, guides and updates for {n.lower()} products.", f"See {n.lower()} products", f"services/{s}.html"] for s, n in SYS]},
        {"type": "faq", "heading": "Finding the right document", "items": [
            ["Where is the General Troubleshooting Guide?", "In the documentation library. The Cell Status Failure Identification Chart, which explains cellular diagnostics errors, is on page 30 of the DMP Troubleshooting Guide."],
            ["What does a technical update tell me?", "Each one covers a specific release, for example SCS-VR Version 1.5.3 (10/8/26) or the VUE Video Doorbell Version 142 (10/22/26), and says what changed."],
            Q_GUIDES, Q_GLOSSARY],},
        LEADFORM]})

# ------------------------------------------------------------------------------------------------ dealer services
PAGES.append({"file": "support/dealer-services.html", "title": title("Dealer services"),
    "description": desc("Dealer services from DMP: Dealer Admin, Dealer Account, free firmware, the Customer Return Center, marketing support and a three year warranty."),
    "crumbs": crumbs(["Dealer services", "support/dealer-services.html"]),
    "sections": [
        {"type": "hero", "layout": "split", "eyebrow": "Dealer services", "heading": "Firmware updates are free, and every product carries a three year warranty.",
         "subhead": "Since 1975, our sole purpose has been to create customer-driven products for professional security dealers. While others have made security a piece of their business, we have made it the entirety of ours.",
         "primary": {"label": "Become a dealer", "href": "support/become-a-dealer.html"}, "secondary": {"label": "Marketing support", "href": "support/marketing.html"},
         "image": IMG + "plant-1200.jpg", "image_alt": "The DMP production floor in Springfield, Missouri", "image_w": 1200, "image_h": 800},
        {"type": "cards", "alt": True, "eyebrow": "Six services", "heading": "What every authorized dealer gets",
         "items": [["Dealer Admin", "Your one stop shop for managing your business and your customers' systems. See an overview of your customers' systems and their status, view analytics, perform mass programming and bulk remote updates, and more."],
                   ["Dealer Account (accounting)", "Securely pay invoices, schedule payments and review the status of software licenses and more."],
                   ["Marketing support", "Your brand is the one that should be promoted, not ours. Custom brand your keypads and customize professional materials with your logo and your staff's contact information."],
                   ["Product firmware updates", "Software and firmware updates are available from DMP free of charge."],
                   ["Customer Return Center", "Our goal is to turn around every request for product updates or repairs in one business day, which is possible because of our online Customer Return Center."],
                   ["Three year warranty", "DMP warrants that the products it manufactures are without defects for three years from the purchase date, in accordance with our Terms and Conditions."]]},
        {"type": "detail", "eyebrow": "Dealer Admin", "heading": "One cloud portal for every customer's panel, with unlimited Global Holiday Dates.",
         "body": "Dealer Admin is a cloud-based portal for managing your business and your customers' DMP panels, including universal communicators. Create, add and delete customers; see location, system type, version and connection method on the customer dashboard; and manage Virtual Keypad app users from one place.",
         "bullets": ["Map and weather view, with filters by panel, system, carrier, technology and status", "Bulk Remote Update, even across thousands of panels that support remote updates", "Mass Programming dashboard with a status check on every change",
                     "Global Holiday Dates: unlimited in Dealer Admin, 40 holidays per panel, and edits update every panel with that date", "Dealer Analytics with daily, weekly or monthly email reports",
                     "Custom Roles that give staff only the authority they need", "Customer referral program you can put in your customers' hands", "Customer list export as CSV"]},
        {"type": "detail", "alt": True, "flip": True, "eyebrow": "Product firmware", "heading": "XT30/XT50 and XTLplus/XTLtouch are on version 261; XR150/XR550 on 263.",
         "body": "Current panel firmware, free to dealers. Version 261 (August 6, 2026) fixes zones on the keypad bus that could stop reporting after remotely programming Device Setup. XR150/XR550 version 263 and XF6-100/XF6-500 version 256 (both August 6, 2026) correct how Supervisory zones are treated during a Sensor Reset. XT75 version 255 is dated June 17, 2026.",
         "bullets": ["XR150/XR550: version 263, August 6, 2026", "XF6-100 and XF6-500: version 256, August 6, 2026", "XT75: version 255, June 17, 2026", "XT30/XT50 and XTLplus/XTLtouch: version 261, August 6, 2026", "XR100 and XR500: version 213, November 21, 2018, adds the 263LTE-V5 module", "International XR150 and XR550 firmware is separate and for international panel use only"],
         "image": IMG + "tab-intrusion-1200.jpg", "image_alt": "The DMP XT75 control board", "image_w": 1200, "image_h": 900},
        {"type": "detail", "eyebrow": "Security Dealer Digest", "heading": "A printed quarterly for dealers: 19 numbered issues since March 2022.",
         "body": "Many dealers told us they do not love the move of industry publications to digital, so we jumped into the publishing game. Security Dealer Digest does not compete with the trade press; it is a printed resource for all things DMP. Issue 19 is September 2026, and there is a 50th Anniversary Edition.",
         "bullets": ["Issue 19, September 2026", "Issue 18, June 2026 and Issue 17, March 2026", "50th Anniversary Edition", "Issue 1 was March 2022"]},
        {"type": "faq", "heading": "Dealer Account and monthly Entré/SCS-VR support billing", "items": [
            ["How does monthly support billing work?", "Effective August 1, 2022, all Entré and SCS-VR support is billed monthly. On the first day of each month, one invoice containing all active licenses is emailed to the dealer, the same way all other invoices are delivered. Each license has its own billing record on the invoice. Support is billed in advance, so August's invoice is for August support, and the monthly amount is the annual amount divided by twelve, rounded."],
            ["When does monthly support begin?", "For new Entré or SCS-VR licenses, monthly support billing begins on the first day of the month after purchase. The first invoice contains a prorated amount from the purchase date to the end of that month, plus the current month. For example, for an Entré license bought July 20, no support is charged on the purchase invoice, and the August 1 invoice includes prorated support for July 21 to 31 plus the full month of August."],
            ["How is prepaid annual support shown?", "Prepaid licenses show their billing details and support expiration date on each monthly invoice, with no monthly charge until support expires. In the month support expires, the amount billed is prorated from the expiration date to the end of the month."],
            ["Can dealers auto pay monthly invoices?", "Yes. The email containing the monthly invoice has a link to sign up for and manage autopay by ACH or credit card, and it can be cancelled any time through the same link. Autopay applies only to software support invoices. Dealers on EFT terms should not use autopay for software support."],
            ["What are the payment terms, and who gets past due notices?", "Payment terms for monthly support invoices are net 30. The only exception is EFT customers, whose terms are 15 days from the invoice date. All interested parties at the dealer receive past due notices, and dealer admin users or DMP accounts receivable can add interested parties under Users, then License Contacts, in Dealer Account."],
            ["How does a dealer cancel a software license?", "Use the Software License Cancellation Acknowledgement form on the License tab in Dealer Account, or contact DMP accounts receivable at acctsrec@dmp.com. Once the form is signed, the license no longer receives support or software updates. A dealer who later needs support or updates must buy a new license."],
            ["Does free freight apply to my orders?", "Enrolling in the Electronic Funds Transfer (EFT) program makes all of your orders qualify for free freight. Orders larger than $1,500 qualify when the account is paid within 30 days, and column 4, 5 or 6 dealers qualify when the account is paid within 30 days. None of this applies to credit card terms."]]},
        LEADFORM]})

# ------------------------------------------------------------------------------------------------ design tools
PAGES.append({"file": "support/design-tools.html", "title": title("Design tools: System Surveyor"),
    "description": desc("Design DMP intrusion, access control, fire and video systems on a digital floor plan in System Surveyor, with an automatic bill of materials and DMP catalog files."),
    "crumbs": crumbs(["Design tools", "support/design-tools.html"]),
    "sections": [
        {"type": "hero", "layout": "split", "eyebrow": "Design tools", "heading": "Place DMP panels, keypads and readers on a floor plan, and get the bill of materials instantly.",
         "subhead": "System Surveyor lets security professionals design DMP systems, intrusion, access control, fire and video, on a digital floor plan, placing devices and capturing project requirements in real time.",
         "primary": {"label": "About System Surveyor", "href": "partners/system-surveyor.html"}, "secondary": {"label": "Get a quote", "href": "support/get-a-quote.html"},
         "image": IMG + "system-surveyor-1200.jpg", "image_alt": "A hand holding a tablet showing a floor plan in System Surveyor", "image_w": 1200, "image_h": 732},
        {"type": "cards", "alt": True, "eyebrow": "Why design this way", "heading": "From concept to proposal faster, with accurate, well-scoped installations",
         "items": [["Design visually and professionally", "Drag and drop panels, keypads and readers onto digital floor plans for clear, precise layouts."],
                   ["Automate documentation", "Generate accurate bills of materials instantly, reducing errors and speeding approvals."],
                   ["Accelerate sales cycles", "Deliver polished proposals faster, save hours on design and win more business."],
                   ["Simplify service and upgrades", "Keep digital as-builts for easy maintenance and expansions."]]},
        {"type": "detail", "eyebrow": "Get started", "heading": "Three steps from a free account to a DMP-ready design.",
         "body": "The generated bill of materials can be shared with customers and teams. See how System Surveyor helps you design DMP intrusion and access control systems faster, collaborate with customers in real time and generate accurate system documentation instantly.",
         "bullets": ["Sign up for a free System Surveyor account", "Download the DMP product catalog files below", "Follow the System Surveyor tutorial to import DMP products into the platform"],
         "image": IMG + "tab-spec-1200.jpg", "image_alt": "A tablet showing a floor plan in System Surveyor", "image_w": 1200, "image_h": 900},
        {"type": "cards", "alt": True, "eyebrow": "Product catalog files", "heading": "Five DMP catalog files to import into System Surveyor",
         "items": [["IDS Product Catalog", "Intrusion products."], ["Fire Alarm Product Catalog", "Fire alarm products."], ["ACS Product Catalog", "Access control products."],
                   ["Video Surveillance Product Catalog", "Video products."], ["X1 ACS Product Catalog", "X1 access control products."]]},
        {"type": "services", "heading": "Keep designing", "intro": "What to do with a finished layout.",
         "items": [["System Surveyor at DMP", "Our partnership with System Surveyor and what it covers.", "partners/system-surveyor.html"],
                   ["A&E specs and CAD drawings", "Specification text and drawings for panels, enclosures, modules and doors.", "support/ae-support.html"],
                   ["Get a quote", "Send us the project and a person will reply.", "support/get-a-quote.html"]]},
        LEADFORM]})

# ------------------------------------------------------------------------------------------------ A&E support
AE_SPECS = ["XF6 A&E Spec", "DualComNF A&E Spec", "SCS-1R A&E Spec", "XT30/XT50 A&E Spec", "XR150/XR550 A&E Spec", "CX-702 A&E Spec", "XTL Series A&E Spec"]
CAD = [
 ("Control panels", ["XR150N PCB", "XR550N PCB", "XR550 Burg Access Application Example", "XR550D with Cell Wi Fi Communications", "XR550DN with Cellular Communications", "XT30 PCB", "XT50 PCB", "XT50CDN"]),
 ("Enclosures", ["340 Panel Enclosure", "341 Panel Enclosure", "350 Large Panel Enclosure", "350A Large Grade A Panel Enclosure", "350C Conduit Backbox", "352P Extra Large Panel Enclosure", "352S Extra Large Battery Enclosure", "353 Wire Pull Box", "354A-G Mounting Plate", "354-G Retrofit Plate"]),
 ("Modules and expanders", ["370 Lightning Suppressor", "572 Indicator LED (Typical Wiring Detail)", "630F-R Remote Annunciator Module (Back Box Dimensions)", "708 Bus Extender Module", "710 Bus Splitter Repeater", "711 Door Contact", "712-8 Expansion Module",
    "714 Zone Expansion Module", "714-8/714-16 Zone Expansion Module", "715-8/715-16 Zone Expansion Module", "716 Output Module", "734 Interface Module", "734N Wi Fi Interface Module", "738A Expansion Module", "763 Wi Fi Module",
    "865 Style W/X Notification Module (Panel Wiring)", "866 Style W Notification Module (Panel Wiring)", "867 Notification Module", "869 Initiating Module", "893A Dual Phone Line Module",
    "RS485 to S710D XR500 Fiber Application", "RS485 to S710D XR500 Keypad Application", "RS485 to S710D XR500 LX Bus Application", "RS485 to S710 D XR550 Fiber Application", "RS485 to S710 D XR550 Keypad Fiber Application", "RS485 to S710 D XR550 LX Bus Fiber Application"]),
 ("Keypads", ["7000 Series Thinline LCD Keypads", "7060 Thinline LCD Keypad", "7070 Thinline LCD Keypad with 4 Zones", "7073 Thinline LCD Keypad with 4 Zones, Prox Reader, and Door Access Relay"]),
 ("Wireless", ["1100D Wireless Receiver", "1100X Wireless Receiver", "1100R Wireless Repeater", "1101 Wireless Universal Transmitter", "1102 Wireless Universal Transmitter", "1103 Wireless Universal Transmitter", "1106 Wireless Universal Transmitter",
    "1114 Wireless Zone Expander", "1116 Wireless Relay", "1117 Wireless LED Annunciator", "1118 Wireless Remote Indicator Light", "1119 Wireless Door Sounder", "1129 Wireless Glassbreak", "1139 Wireless Bill Trap", "1142 Wireless Two Button Hold Up", "1183 Wireless Fixed Heat Detector"]),
 ("Single and multi-door", ["15 Door Access System Example CAD Drawings", "Double Door with Single 733 or 734 Module CAD Drawings", "Single Door Access CAD Drawings", "Single Door Access with Single 733 or 734 Module CAD Drawings", "Single Door with Two 734 Modules CAD Drawings",
    "Single Switch Lockdown method for XR550N Application CAD Drawings", "DMP Mantrap Application Door Maglock CAD Drawings", "DMP Mantrap Application Door Strike CAD Drawings", "DMP Mantrap Application CAD Drawings"])]
PAGES.append({"file": "support/ae-support.html", "title": title("A&E support: specs and CAD drawings"),
    "description": desc(f"A&E specs for {len(AE_SPECS)} DMP products and CAD drawings for {sum(len(x) for _, x in CAD)} panels, enclosures, modules, keypads, wireless devices and door applications."),
    "crumbs": crumbs(["A&E support", "support/ae-support.html"]),
    "sections": [
        {"type": "hero", "layout": "split", "eyebrow": "Architect and engineer support", "heading": f"{sum(len(x) for _, x in CAD)} CAD drawings, from the XR550N board to a three-door mantrap.",
         "subhead": f"Specification text for {len(AE_SPECS)} DMP products and drawings in six groups, so architects and engineers can put DMP systems into plans and specifications.",
         "primary": {"label": "Talk to Inside Sales", "href": "contact.html"}, "secondary": {"label": "Design tools", "href": "support/design-tools.html"},
         "image": IMG + "p-xr550-1200.png", "image_alt": "The DMP XR550 control panel", "image_w": 1200, "image_h": 818},
        {"type": "cards", "alt": True, "eyebrow": "A&E specs", "heading": f"{len(AE_SPECS)} written specifications for control panels, communicators and receivers",
         "items": [[s, "Architect and engineer specification."] for s in AE_SPECS]},
        {"type": "cards", "eyebrow": "CAD drawings", "heading": "Six groups of drawings, from control panels to single and multi-door applications",
         "items": [[f"{g} ({len(x)})", "; ".join(x) + "."] for g, x in CAD]},
        {"type": "detail", "alt": True, "eyebrow": "Support for architects and engineers", "heading": "Inside Sales supports architects and engineers on system design.",
         "body": "Inside Sales handles system design, architect and engineer support, pre-sales support and quotes. Call 877-757-4367, 8 a.m. to 5 p.m. Central, or email InsideSales@DMP.com.",
         "bullets": ["Drawings and specs are listed as plain titles; ask Inside Sales for the files", "Dealers order at buy.DMP.com, 24 hours a day", "Regional sales managers are listed in the sales directory"]},
        {"type": "services", "heading": "Related tools", "intro": "Design, document, quote.",
         "items": [["Design tools", "Lay out a DMP system on a floor plan and generate a bill of materials.", "support/design-tools.html"],
                   ["Documentation library", "Spec sheets, installation guides and technical updates.", "support/documentation.html"],
                   ["Sales directory", "Regional sales managers by territory.", "support/sales-directory.html"]]},
        LEADFORM]})

# ------------------------------------------------------------------------------------------------ get a quote
PAGES.append({"file": "support/get-a-quote.html", "title": title("Get a quote"),
    "description": desc("Request a quote from DMP: tell us your company, location and product interest, and an authorized dealer network and DMP security professionals will help."),
    "crumbs": crumbs(["Get a quote", "support/get-a-quote.html"]),
    "sections": [
        {"type": "hero", "layout": "split", "eyebrow": "Get a quote", "heading": "One location or thousands of sites: intrusion, fire, access, video and cellular, quoted together.",
         "subhead": "Complete the form to discuss project requirements or learn more about DMP products and services.",
         "primary": {"label": "Start the quote form", "href": "support/get-a-quote.html#quote"}, "secondary": {"label": "Call Inside Sales", "href": "tel:+18777574367"},
         "image": IMG + "tab-owner-1200.jpg", "image_alt": "A person checking a phone as they leave a building", "image_w": 1200, "image_h": 900},
        {"type": "detail", "alt": True, "eyebrow": "Integrated security for every scale", "heading": "Reliable, scalable and easy to use, from a single location to an enterprise.",
         "body": "Whether you are securing a single location or an enterprise with thousands of sites, DMP delivers integrated security designed for reliability, scalability and ease of use. From intrusion and fire to access control, video and cellular communications, every solution is built to meet the unique needs of the application. Through a nationwide network of authorized DMP dealers and a team of experienced security professionals, organizations receive guidance on selecting the right products, designing a complete solution and planning for future growth.",
         "bullets": ["Nationwide network of authorized DMP dealers", "Guidance on selecting the right products", "Help designing a complete solution", "Planning for future growth"]},
        {"type": "detail", "eyebrow": "What we ask for", "heading": "Eleven questions, from your dealer relationship to the product type.",
         "body": "The quote form asks:",
         "bullets": ["Are you already working with an authorized DMP dealer? (and who, if yes)", "First name and last name", "Job title", "Work email and phone number", "Company name", "ZIP code and country",
                     "What product type are you interested in? Intrusion, Access, Fire, Video, Communicators or JamAlert", "How did you hear about DMP? Social media, email, referral, publications, events or search engine, among other answers"]},
        {"type": "contact", "id": "quote", "heading": "Request your quote", "body": "Tell us who you are, where the project is and which product type you are looking at. A person will reply.",
         "options": ["Intrusion", "Access", "Fire", "Video", "Communicators", "JamAlert"], "submit": "Request a quote", "note": "Inside Sales is 877-757-4367, 8 a.m. to 5 p.m. Central."},
        {"type": "services", "alt": True, "heading": "While you wait for the quote", "intro": "Design and find people.",
         "items": [["Design tools", "Lay out the system on a floor plan and see the bill of materials.", "support/design-tools.html"],
                   ["Sales directory", "Find the regional sales manager for your territory.", "support/sales-directory.html"],
                   ["Products by system", "Intrusion, access control, fire, video and more.", "services.html"]]},
        {"type": "faq", "heading": "Before you request a quote", "items": cf("who", "person", "order")},
        LEADFORM]})

# ------------------------------------------------------------------------------------------------ become a dealer
PAGES.append({"file": "support/become-a-dealer.html", "title": title("Become a DMP dealer"),
    "description": desc("Apply to become an authorized DMP dealer. We look for $5,000 to $10,000 of equipment purchases a month, and approval typically takes a few days."),
    "crumbs": crumbs(["Become a dealer", "support/become-a-dealer.html"]),
    "sections": [
        {"type": "hero", "layout": "split", "eyebrow": "Become a dealer", "heading": "Approval to become an authorized DMP dealer should take just a few days.",
         "subhead": "DMP is a privately held independent manufacturer of intrusion, fire, access control and cellular alarm products, available exclusively through our authorized dealer network.",
         "primary": {"label": "Apply now", "href": "support/become-a-dealer.html#apply"}, "secondary": {"label": "Dealer services", "href": "support/dealer-services.html"},
         "image": IMG + "hq-exterior-1200.jpg", "image_alt": "The DMP headquarters in Springfield, Missouri, with the American flag in front", "image_w": 1200, "image_h": 800},
        {"type": "detail", "alt": True, "eyebrow": "Who we partner with", "heading": "The best security company in your city, buying $5,000 to $10,000 of equipment a month.",
         "body": "Our ideal dealer is the best security company in its market, growth-minded and actively building its intrusion, access control, commercial fire or video business, consistently installing and selling systems month after month. We generally look for dealers purchasing at least $5,000 to $10,000 in equipment per month. Founded in 1975, we are a partner you can trust.",
         "bullets": ["Privately held, independent manufacturer", "Products available exclusively through authorized dealers", "Intrusion, fire, access control and cellular alarm products"]},
        {"type": "detail", "eyebrow": "What we ask for", "heading": "Application: company, five contacts, your project and your tax details.",
         "body": "The new dealer application asks for:",
         "bullets": ["Company name, DBA name, website, address, company phone", "Primary contact name, title, work phone and email, and your role in the decision process",
                     "Owner or president, sales leader, operations, installation and service contact, and accounts payable contact, each with an email",
                     "Whether you are working on a project or bid involving DMP product, and its name", "What has created your interest in becoming a dealer, and how many years you have been in business",
                     "Your primary business activity, business type, major markets and total company annual revenue", "Tax exempt status, Federal Tax ID number, and NAICS and SIC codes"]},
        {"type": "cards", "alt": True, "eyebrow": "After you apply", "heading": "The dealer agreement form: four documents and a team list",
         "items": [["W-9 forms", "The DMP W-9 and the SecureCom W-9, so we can set you up as a vendor."],
                   ["DMP Terms and Conditions", "Download, sign and upload the signed copy. Any additional information goes to InsideSales@DMP.com."],
                   ["SecureCom Wireless Network Services Agreement", "Download, sign and upload the signed copy."],
                   ["Tax exempt certificates", "Upload certificates for all states in which you are tax exempt, up to 10 files. Without them, appropriate tax is charged on your orders."],
                   ["Owner, president, general manager and sales leader", "Company, address, website, and each person's name, email and cell phone, so your whole team can get the training and support they need."],
                   ["Your team's contact information", "Give us as many team members as possible; the more we know about your organization, the faster everyone gets moving."]]},
        {"type": "contact", "id": "apply", "heading": "Start your dealer application", "body": "Tell us about your company and a member of our team will be in touch.",
         "options": ["Intrusion", "Access control", "Commercial fire", "Video", "Several of these"], "submit": "Send application", "note": "Inside Sales is 877-757-4367, 8 a.m. to 5 p.m. Central."},
        {"type": "faq", "heading": "Dealer questions answered", "items": [
            ["Does DMP sell directly to building owners?", COMMON_FAQ["who"][1]],
            ["How do dealers place an order?", "At buy.DMP.com, which takes orders 24 hours a day, or through DMP Customer Service."],
            ["What does a dealer get?", "Dealer Admin, Dealer Account, free firmware updates, the Customer Return Center, marketing support and a three year warranty. See dealer services for details."]]},
        LEADFORM]})

# ------------------------------------------------------------------------------------------------ sales directory
RSM = ["Mid-Atlantic", "New York Metro", "Los Angeles", "The Carolinas", "New England", "Central States", "Illinois", "Oklahoma", "North Texas", "Georgia", "Indiana", "Mountain West", "Mid-South", "Michigan", "Ozarks", "South Texas", "Upper Midwest", "Ohio", "Four Corners"]
PAGES.append({"file": "support/sales-directory.html", "title": title("Sales directory: regions and regional sales managers"),
    "description": desc("DMP's sales team by role and territory: 19 regional sales managers, directors of sales, national accounts, financial, government, retail and international."),
    "crumbs": crumbs(["Sales directory", "support/sales-directory.html"]),
    "sections": [
        {"type": "hero", "layout": "split", "eyebrow": "Sales directory", "heading": f"{len(RSM)} regional sales managers, from New England to Four Corners and Los Angeles.",
         "subhead": "Our sales team is organized by region, by market and by account type. Inside Sales connects you with the right person for your territory.",
         "primary": {"label": "Call Inside Sales 877-757-4367", "href": "tel:+18777574367"}, "secondary": {"label": "International distributors", "href": "international.html"},
         "image": IMG + "hq-exterior-1200.jpg", "image_alt": "The DMP headquarters in Springfield, Missouri, with the American flag in front", "image_w": 1200, "image_h": 800},
        {"type": "cards", "alt": True, "eyebrow": "Who is on the team", "heading": "Eight kinds of sales role, from regional managers to international sales",
         "items": [[f"Regional sales managers ({len(RSM)})", "One for each of these territories: " + ", ".join(RSM) + "."],
                   ["Directors of sales (4)", "North Central (which includes Ohio), Northeast, Southeast and South Central (which includes South Texas)."],
                   ["Executive vice president of sales", "North America, Canada and Northeast."],
                   ["National accounts (6)", "Four national account directors, an executive director of national accounts and a sales engineer."],
                   ["Financial Solutions (2)", "Two executive directors of financial solutions."],
                   ["Government Solutions", "An executive director of government solutions."],
                   ["Retail Solutions", "A director of retail solutions covering North America, Canada, North Central, Mid-South, National Accounts, West Sales, Southern California and Central California."],
                   ["International sales (2)", "A vice president of international sales and an account executive for international sales."]]},
        {"type": "detail", "eyebrow": "How to reach them", "heading": "Contact goes through Inside Sales, 8 a.m. to 5 p.m. Central.",
         "body": "We do not publish individual phone numbers or email addresses here. Call Inside Sales at 877-757-4367 or email InsideSales@DMP.com with your city or state, and we will connect you with the regional sales manager for your territory.",
         "bullets": ["Inside Sales: system design, pre-sales support, quotes and pricing", "Technical questions: Technical Support 888-436-7832, 7 a.m. to 7 p.m. Central", "Orders: buy.DMP.com or Customer Service 866-266-2826"]},
        {"type": "cards", "alt": True, "eyebrow": "Outside the United States", "heading": "Eight distributor listings cover Benelux to South Africa, plus Mexico and Latin America.",
         "items": [["Benelux (Belgium, Netherlands, Luxembourg)", "Sabelco"], ["Greece and Cyprus", "GQ Tech"], ["Hungary", "Object Guard"], ["Latin America and Caribbean", "ISTC"],
                   ["Mexico", "Otwo"], ["Mexico", "Tecnoseguridad"], ["South Africa, Mozambique and Zambia", "Regal"], ["United Kingdom and Ireland", "ADI EU"]]},
        {"type": "services", "heading": "Other ways to reach us", "intro": "Quotes, distributors and contacts.",
         "items": [["Get a quote", "Tell us the project and the product type.", "support/get-a-quote.html"], ["International distributors", "How to buy DMP products outside the United States.", "international.html"], ["Support and contacts", "Every phone line, with hours.", "support.html"]]},
        LEADFORM]})

# ------------------------------------------------------------------------------------------------ marketing
VIDEOS = ["VUE Video Doorbell", "AlarmVision", "Animated Tutorials", "Virtual Keypad for Your Business", "Virtual Keypad How-To", "7-Inch Keypad How-To", "5-Inch Keypad How-To", "Thinline Keypad How-To", "Replacing Batteries How-To", "Residential Market", "Small Business Market", "Door to Door Sales"]
PAGES.append({"file": "support/marketing.html", "title": title("Marketing support for dealers"),
    "description": desc("Marketing Central for DMP dealers: free account, hundreds of assets with your logo, 75+ custom videos, and print at our cost with no markup."),
    "crumbs": crumbs(["Marketing support", "support/marketing.html"]),
    "sections": [
        {"type": "hero", "layout": "split", "eyebrow": "Marketing support", "heading": "We print and ship brochures and sell sheets at our cost, with no markup.",
         "subhead": "Customize marketing materials with your logo and contact information. Your account is free, and so are most assets.",
         "primary": {"label": "Sign up for Marketing Central", "href": "support/marketing.html#signup"}, "secondary": {"label": "Private label", "href": "support/private-label.html"},
         "image": IMG + "tab-spec-1200.jpg", "image_alt": "A tablet showing a floor plan in System Surveyor", "image_w": 1200, "image_h": 900},
        {"type": "cards", "alt": True, "eyebrow": "Three ways to carry your brand", "heading": "Assets, videos and branded keypads and credentials",
         "items": [["Marketing assets", "Choose from hundreds of high quality assets: product and lifestyle photography, ready-to-go social media and email content, and digital and print literature that can be customized with your logo and contact information."],
                   ["Custom videos", "Choose from over 75 professional videos to use on your website, social media accounts, presentations or anything else you like. Customization is free and fast."],
                   ["Keypads and credentials", "Put your brand in front of your customers, and in their pockets, with custom keypads and credentials. Choose from a variety of products and options."]]},
        {"type": "detail", "eyebrow": "Marketing Central", "heading": "A free account, free assets and an in-house print shop.",
         "body": "Log in or sign up to get started. Your account is free, and so are most assets. We will even print and ship brochures, sell sheets and more in our in-house print shop, at our cost.",
         "bullets": ["Product and lifestyle photography", "Social media and email content, ready to go", "Digital and print literature with your logo and contact information", "In-house printing at our cost, no markup"]},
        {"type": "detail", "alt": True, "flip": True, "eyebrow": "Custom videos", "heading": "Twelve video series you can brand with your logo and contact details.",
         "body": "Videos are free to customize. Choose a series, email PrivateLabel@DMP.com to start, and you receive links optimized for email and links optimized for social media. Series: " + "; ".join(VIDEOS) + ".",
         "bullets": ["Free, and fast", "Use them for training, advertising, website content and more", "Email-optimized and social-optimized links"],
         "image": IMG + "tab-mobile-1200.jpg", "image_alt": "Virtual Keypad on a laptop, tablet and phone", "image_w": 1200, "image_h": 900},
        {"type": "services", "heading": "Take branding further", "intro": "Private label and dealer services.",
         "items": [["Private label", "Custom Digital Keys, branded readers and credentials, and custom keypads.", "support/private-label.html"],
                   ["Dealer services", "Dealer Admin, Dealer Account, firmware and warranty.", "support/dealer-services.html"],
                   ["Become a dealer", "Apply for an authorized DMP dealer account.", "support/become-a-dealer.html"]]},
        {"type": "contact", "id": "signup", "heading": "Sign up for Marketing Central", "body": "By providing your contact information you authorize Digital Monitoring Products, Inc and SecureCom Wireless, LLC to contact you by email, text or phone call.",
         "options": ["Marketing assets", "Custom videos", "Keypads and credentials with my logo", "Something else"], "submit": "Sign up", "note": "Questions about DMP marketing support? Email PrivateLabel@DMP.com."},
        LEADFORM]})

# ------------------------------------------------------------------------------------------------ private label
PAGES.append({"file": "support/private-label.html", "title": title("Private label: custom keypads, Digital Keys and credentials"),
    "description": desc("Private label from DMP: custom Digital Key credentials, branded Wavelynx readers, Farpointe credentials, custom keypads and free custom videos."),
    "crumbs": crumbs(["Marketing support", "support/marketing.html"], ["Private label", "support/private-label.html"]),
    "sections": [
        {"type": "hero", "layout": "split", "eyebrow": "Private label", "heading": "Your name on the Digital Key in your customer's pocket.",
         "subhead": "Keep your brand in front of your customers with custom Digital Keys, branded readers and credentials, and custom keypads.",
         "primary": {"label": "Get started", "href": "support/private-label.html#start"}, "secondary": {"label": "Marketing support", "href": "support/marketing.html"},
         "image": IMG + "digital-key-1200.jpg", "image_alt": "A hand holding a phone to a door reader", "image_w": 1200, "image_h": 501},
        {"type": "cards", "alt": True, "eyebrow": "Five private label options", "heading": "Digital Keys, Wavelynx readers, Farpointe credentials, keypads and videos",
         "items": [["Custom Digital Key credentials", "Choose Basic Custom Branded or Full Custom Branded Digital Keys, with options for colors, logo placement, images and more."],
                   ["Branded Wavelynx readers and credentials", "Add your logo to Wavelynx Multi-Technology readers and credentials, with options for custom numbering and encryption."],
                   ["Branded Farpointe credentials", "Add your logo to Farpointe credential cards and fobs, with the option for custom numbering."],
                   ["Custom keypad options", "Basic and fully customized 5-inch and 7-inch touchscreen keypads, and branded silicone inserts for Thinline keypads."],
                   ["Custom video packages", "End-user videos you can customize with your logo and contact information for free, for training, advertising, website content and more."],
                   ["Marketing materials with your logo", "Sign up for Marketing Central to customize materials with your logo and contact information."]]},
        {"type": "detail", "eyebrow": "Lead times", "heading": "Wavelynx production runs 5 to 6 weeks; Farpointe lead time is 4 to 5 weeks.",
         "body": "Plan branded credential orders around these averages.",
         "bullets": ["Branded Wavelynx readers and credentials: production time is 5 to 6 weeks on average", "Branded Farpointe credentials: lead time is 4 to 5 weeks on average"]},
        {"type": "faq", "heading": "Custom video questions", "items": [
            ["How can I use our customized videos?", "However you like. When you choose a series to customize, you receive links for videos optimized for email and links for videos optimized for social media. Send them to your customers by email or post them to social media."],
            ["How do I order our videos?", "Select the series you want customized and email PrivateLabel@DMP.com to begin the customization process."],
            ["How much does it cost?", "It is free."]]},
        {"type": "contact", "id": "start", "heading": "Start a private label order", "body": "Tell us which items you want branded. Email PrivateLabel@DMP.com or send the form.",
         "options": ["Custom Digital Key credentials", "Branded Wavelynx readers or credentials", "Branded Farpointe credentials", "Custom keypads", "Custom videos"], "submit": "Send to private label",
         "note": "PrivateLabel@DMP.com"},
        LEADFORM]})

TO_CONFIRM = [
    "All forms (quote request, dealer application, Marketing Central sign-up, private label, lead form) are placeholders until the HubSpot forms are wired. The field lists on get-a-quote and become-a-dealer come from the fields on the current dmp.com forms; the option lists for business type, major markets and annual revenue were not reproduced.",
    "Technical FAQs: the hub page of the current site holds an older, overlapping list of 25 questions. They were merged into the category pages (and five of them kept on the hub). Where the two disagreed the newer category page was used: key fobs on XR panels use zones 400-449 (older page said 401-449); the wireless transmitter LED test follows the category page (five consecutive blinks, LED on about 8 seconds when faulty) rather than the older 'more than one second' wording; keypad firmware downloads are on the Product Software Downloads page (older page said Dealer Direct Software Downloads). Please have Technical Support confirm.",
    "Older cellular modem firmware table (463C, 464-263, 263H/C, 263LTE, 265LTE) was kept as a separate question on the cellular page because the newer page only lists XT30/XT50, XT75, XR150/550 and XF6. Confirm it is still current.",
    "FAQ answers name the three help-file addresses (virtualkeypadapp.dmp.support, virtualkeypaddesktop.dmp.support, paneltopanel.dmp.support) as plain text because outside links are not allowed in the preview. Decide whether to link them live. The glossary and the General Troubleshooting Guide are documents/pages outside the preview; the glossary answer points visitors to Technical Support for the link.",
    "The monitoring center FAQ page on the current site mixes Digital Key, panel firmware, Remote Link and SCS-1R/SCS-VR questions. It was kept as is. Confirm the Digital Key questions belong there.",
    "Video FAQ cites document LT-2048 for the ports to open; confirm the document number is still current.",
    "Support hub: the live 'current Technical Support hold time' figure was deliberately not printed. The sales engineering map image was not used because it may carry individual names.",
    "Sales directory: counts (36 entries; 19 regional sales managers, 4 directors of sales, 6 national accounts roles, 2 financial solutions, 1 government, 1 retail, 2 international, 1 executive vice president) were read from the directory pages as of November 2026 and will change. Names, phone numbers and emails were deliberately left out. The distributor list (Sabelco, GQ Tech, Object Guard, ISTC, Otwo, Tecnoseguridad, Regal, ADI EU) repeats what the international page will carry; DMP contact names were dropped.",
    "Dealer services: firmware versions and dates (version 261, 263, 256, 255, 213) are as listed in November 2026 and will go stale; consider linking to a live source. Free freight wording on the Dealer Account page was ambiguous (EFT, orders over $1,500 paid in 30 days, column 4, 5 or 6 dealers); the summary needs DMP review. Accounts Receivable specialist phone numbers and names were not reproduced; only acctsrec@dmp.com is used.",
    "Documentation page: the library is script-driven. Example titles were taken from the first results of the library and the marketing literature and retail pages; the total is stated as 'more than 900' (963 when read). Training video titles are the end-user video series. Confirm the one-line descriptions of what each document type is for, which are written for the new site.",
    "Design tools: the System Surveyor sign-up and tutorial links live on systemsurveyor.com and are mentioned as steps without links; the partner page should carry them. The five product catalog files (IDS, Fire Alarm, ACS, Video Surveillance, X1 ACS) are listed by name only because documents cannot be linked.",
    "A&E support: A&E spec descriptions ('Architect and engineer specification') are generic because the source lists titles only. CAD drawing titles keep DMP's own spelling, including 'Wi Fi'.",
    "Private label: the old private label address (/support/private_label) returns 404; the content comes from /support/marketing/private_label. The Marketing Central login portal and sign-up form fields could not be read, so the sign-up form is generic.",
    "Become a dealer: current site has two forms (new dealer application and dealer agreement form). Both are summarised on one page. Confirm that 'typically within just a few days' is still the promise.",
]
