"""DMP page module: company family (careers, DMP Cares, certifications, events, international, legal pages, news articles).
Written from the current dmp.com pages. Data only: PAGES, TO_CONFIRM, NEWS."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dmp_common import *

PRIV_UPDATED = 'Last Updated: January 2021'
PRIV = [['Introduction',
  'Digital Monitoring Products (herein referred to as “Digital Monitoring Products”) appreciates that '
  'privacy is important to you and is committed to protecting the confidentiality of Personal Information '
  'and handling Personal Information with integrity and with an understanding of its sensitive nature. As '
  'such, Digital Monitoring Products has created this Privacy Policy (the “Privacy Policy” or the “Policy”), '
  'and all employees of Digital Monitoring Products are expected and required to abide by this Privacy '
  'Policy. This Privacy Policy applies solely to information collected by this website, except where stated '
  'otherwise.\n'
  '\n'
  'For the purposes of this Policy, Personal Information is information that can be used to directly or '
  'indirectly to identify a living individual. Personal Information may include, but is not limited to, '
  'sensitive categories of information, herein referred to as Sensitive Personal Information, such as '
  'information that reveals racial or ethnic origin, political opinions, religious beliefs, trade union '
  'membership, health, sexual or gender orientation.\n'
  '\n'
  'This Policy is designed to protect Personal Information under applicable law as it exists. Digital '
  'Monitoring Products understands that laws and circumstances may change quicker than the Policy can be '
  'adjusted to fit and that this Privacy Policy cannot address every possible issue and circumstance. As '
  'such, this Privacy Policy is subject in all respects to local legal and regulatory requirements, as well '
  'as existing agreements, and Digital Monitoring Products confirms that the company will comply with any '
  'such requirements and existing agreements.\n'
  '\n'
  'The Digital Monitoring Products web site at www.dmp.com (the “Site”) provides you with information about '
  'Digital Monitoring Products, its products and services, and in certain circumstances, allows you to '
  'purchase products or services or sign up to receive further information about Digital Monitoring '
  'Products. In order to provide you with access to this information about Digital Monitoring Products, and '
  'the ability to purchase products and services offered by or through the Site, certain Personal '
  'Information is collected from visitors to the Site. This Privacy Policy is designed to inform you about '
  'the types of information that are collected, as well as our use of such Personal Information, and sets '
  'forth the guidelines Digital Monitoring Products uses in protecting your privacy. This Privacy Policy '
  'applies to your use of the Site, any other Digital Monitoring Products site that is linked from '
  'www.dmp.com, as well as your use of Digital Monitoring Products’s social media web sites and pages, '
  'including without limitation, YouTube™, Facebook® , LinkedIn ® , Twitter® , Instagram® , and Google+™, '
  'which are all included in the definition of “Site”. This Privacy Policy shall also be deemed part of the '
  'Digital Monitoring Products Site Terms of Use.\n'
  '\n'
  'This Privacy Policy describes the types of Personal Information that Digital Monitoring Products collects '
  'in connection with this Site. Digital Monitoring Products gathers Personal Information and will '
  'distribute this information only within Digital Monitoring Products in an effort to meet your needs and '
  'respond to your information requests.\n'
  '\n'
  'We note that if you are a Digital Monitoring Products employee, contractor, supplier, customer or other '
  'partner, the use and protection of Personal Information may be subject to additional contractual '
  'obligations between us, including without limitation, additional Digital Monitoring Products policies.',
  []],
 ['Personal vs. Non-personal Information',
  'Personal Information\n'
  '\n'
  'Personal Information may be collected from you as you use the Site. Personal Information generally is '
  'information that personally identifies you in some way(s). Examples include your name, address, birth '
  'date, email address, phone number, other data collected when purchasing our products or services, '
  'education, employment, credit card, or other credit information. Additional examples include information '
  'submitted through our call centers, by joining a mailing list, by participating in social media events, '
  'contests or surveys, and signing up for email alerts or distributions. If during your visit to the this '
  'website you submit Personal Information to us, you are choosing to provide us with your Personal '
  'Information and you agree that it will be used to provide the information, products or services that you '
  'request (including information on additional products and or services which Digital Monitoring Products '
  'reasonably thinks may be of interest to you) and you consent to Digital Monitoring Products’s use of your '
  'personal information to improve or market Digital Monitoring Products’s products or services. Digital '
  'Monitoring Products does not knowingly request or collect Personal Information from any person under the '
  'age of 13 and we ask that any individual who is under the age of 13 to refrain from using our Site or '
  'submitting any Personal Information.\n'
  '\n'
  'Non-Personal Information\n'
  '\n'
  'Non-personal information includes general information about your visit to the Site that is not personal '
  'information or does not personally identify you. Digital Monitoring Products’s web server will recognize '
  'your domain name, which will be collected to monitor general use of the Site and for improvements to the '
  'Site, our products, and services. Similarly, cookies provide non-personal information which allows us to '
  'track the anonymous use of our Site, including use and traffic statistics each time you visit by placing '
  'small data files placed on your hard drive by the Site. Cookies also make the Site more convenient and '
  'easier to navigate for you, but they do not collect personal information. Cookies can be ‘session '
  'cookies’ (which are deleted when you close your browser) and/or ‘persistent cookies’ which remain on your '
  'computer for a longer period of time. Further detail on cookies is discussed below. You can disable or '
  'reject the use of cookies, by modifying the appropriate settings on your browser. Note that by doing so, '
  'however, you will likely not enjoy the full functionality of the Site.',
  []],
 ['Use, Disclosure and Protection of Personal Information',
  'It is Digital Monitoring Products’s intention to obtain Personal Information only by fair and lawful '
  'means, and to use the Personal Information to service your needs and requests. Digital Monitoring '
  'Products will not process Personal Information in a manner incompatible with the purposes for which it '
  'was originally collected unless later authorized by the individual from whom the information was '
  'collection or unless allowed by law. We will not keep Personal Information longer than is necessary for '
  'the purposes for which it was originally gathered.\n'
  '\n'
  'When do collect and process Personal Information about individuals, we will disclose certain information '
  'to those particular individuals on a reasonable and timely basis upon written request of the individuals '
  'from whom the Personal Information was collected. The disclosed information will include what Personal '
  'Information is being collected, who is collecting it, how and for what purposes it is being collected, '
  'how it is being us and to whom it is being disclosed. We will allow individuals reasonable access to '
  'their Personal Information to verify, correct or delete their data, where inaccurate.\n'
  '\n'
  'We may also use Personal Information to process an order made through the Site, including shipping and '
  'returns of such order, and for organizing and submitting customer satisfaction reviews. We may also use '
  'such Personal Information to support marketing for our products and services and to enhance the content '
  'and use of our Site.\n'
  '\n'
  'In order for Digital Monitoring Products to provide our products and services, we may need to share your '
  'Personal Information with other companies, agencies or contractors affiliated with Digital Monitoring '
  'Products. We will always seek to ensure that it is kept secure and only used in accordance with your '
  'instructions and agreed purpose.\n'
  '\n'
  'Further, we may use and disclose Personal Information to the extent necessary to comply with laws, '
  'regulations, court orders, government agencies or investigations and similar legal instructions, to '
  'resolve disputes, and to protect Digital Monitoring Products rights and property.\n'
  '\n'
  'Additionally, we may also contract with other third-parties to provide services, such as shipping, '
  'payment processing, contact verification, market research, and organization of promotions, or other '
  'subcontractors; however, we will provide these contractual parties only with the Personal Information '
  'necessary to perform the work for which they were contracted.\n'
  '\n'
  'Digital Monitoring Products and its third-party providers may use cloud-based tools, and in such event, '
  'data might be processed in countries outside the United States. In such cases, Digital Monitoring '
  'Products and any such provider will agree to the necessary terms as required by law to protect Personal '
  'Information.\n'
  '\n'
  'Digital Monitoring Products will process Personal Information only with consent and when such processing '
  'is permitted by applicable law. If Digital Monitoring Products needs to process Sensitive Personal Data, '
  'which is very rare, Digital Monitoring Products will obtain explicit consent for such processing, unless '
  'such processing is permitted by applicable law.\n'
  '\n'
  'Digital Monitoring Products will not sell Personal Information to any third party and we will take '
  'commercially reasonable efforts to maintain the confidentiality of such information, in accordance with '
  'our contractual obligations as well as in compliance with those laws applicable in the states and '
  'countries in which we conduct business (and you should be aware that laws in all jurisdictions are not '
  'the same, and that some may have stricter requirements than others). Further, to protect your Personal '
  'Information from unauthorized access and use, Digital Monitoring Products maintains physical, electronic, '
  'and procedural safeguards, and requires those to whom we disclose Personal Information to do the same. We '
  'are committed to making sure that your Personal Information is accurate and up to date but it is your '
  'responsibility to let us know if your Personal Information is inaccurate or out of date and we can only '
  'make changes to your personal information if you notify us.\n'
  '\n'
  'Digital Monitoring Products will retain your Personal Information only for so long as it is helpful to '
  'support the overall purpose for which we collected the information.\n'
  '\n'
  'Digital Monitoring Products may use third party service providers, such as Google Analytics, to help '
  'analyze how users use the Site. By visiting this web site you are agreeing to our use of cookies for '
  'these purposes. For example, services like Google Analytics collect information anonymously and reports '
  'website trends without identifying individual visitors. Google Analytics collects only the IP address '
  'assigned to you on the date you visit the Site, rather than your name or other personally identifying '
  'information. Google Analytics uses cookies to collect information such as how often users visit the Site, '
  'what pages are visited, and what other sites are used prior to coming to the Site. Although Google '
  'Analytics plants a persistent cookie on your web browser to identify you as a unique user the next time '
  'you visit the Site, the cookie cannot be used by anyone but Google ® . Digital Monitoring Products does '
  'not combine the information collected through the use of Google Analytics with other personally '
  'identifiable information. Digital Monitoring Products uses the information we get from Google Analytics '
  'only to improve our Site and Services. Google’s ability to use and share information collected by Google '
  'Analytics about your visits to the Site is restricted by the Google Analytics Terms of Use, '
  'http://www.google.com/analytic... and the Google Privacy Policy, https://policies.google.com/privacy. If '
  'you are interested in learning about opting out of Google Analytics, visit: '
  'https://tools.google.com/dlpage/gaoptout.',
  []],
 ['Opting Out of Marketing Communications',
  'Your Personal Information may be used to provide you with information regarding additional opportunities '
  'and information about Digital Monitoring Products products and services; and accordingly, by using the '
  'Site and providing such Personal Information, you consent to such use. However, to the extent required by '
  'law, we will provide mechanisms for opting out of mass marketing communications targeted by Personal '
  'Information we have collected or otherwise obtain consent in the manner required by applicable law. These '
  'mechanisms will normally be available on the relevant email or web site, but you may always notify us at '
  'the address specified below under “Contact Us”. Requests to opt out of communications based on data '
  'controlled by third parties must be made through the third party. Notwithstanding the foregoing, there '
  'may be some jurisdictions requiring stricter opt-in versus opt-out mechanisms relating to these types of '
  'communications and we will comply with the applicable laws in such locations.',
  []],
 ['External Links; Public Social Media',
  'This Site may provide links to other third party websites, including social media sites. These links are '
  'provided to you for your convenience only, and you access them at your own risk. Even if the third party '
  'is affiliated with Digital Monitoring Products, if you choose to use these links, Digital Monitoring '
  'Products is not responsible for the conditions or results of use, privacy policies or practices, or the '
  'content of such external links or the person or entity responsible for them. You should review the '
  'applicable terms of use and privacy policy provisions of such third party websites before using them.\n'
  '\n'
  'Furthermore, any information you submit in a public forum or social marketing site that is publicly '
  'available (such as a chat room, public posting or blog, whether or not sponsored by Digital Monitoring '
  'Products) can be read, collected, or used by us as well as others, and could be used to personalize your '
  'experience. You are responsible for the information you choose to submit through these media, and '
  'although we attempt to monitor user-posted content, such user-posted material is not subject to this '
  'privacy statement. Use of any Digital Monitoring Products-related social media or marketing site may also '
  'be subject to additional policies and terms of use, which you should review before posting any such '
  'public information.',
  []],
 ['Other Digital Monitoring Products Sites',
  'This Privacy Policy is applicable to this Site, as specified above. However, other Digital Monitoring '
  'Products websites may have their own respective privacy policy or other privacy-related terms posted. '
  'Those other privacy terms and conditions shall apply to privacy-related issues regarding that other site '
  'and the use of any services, functionalities or other offerings made in connection with that other site, '
  'and this Privacy Policy shall not apply in such circumstances.',
  []],
 ['Amendments to this Privacy Policy',
  'Digital Monitoring Products may amend this Policy at any time by posting a revised version on this Site, '
  'without providing prior notice to you. Any such amendment will be effective at the time it is posted '
  'unless a delayed effective date is expressly stated in the revised version. Your continued use of this '
  'Site after such changes have been posted will constitute your acceptance of the changes.',
  []],
 ['Enforceability',
  'In the event any of the provisions of this Privacy Policy shall be held to be unenforceable, the '
  'remaining provisions shall be unimpaired, and the unenforceable provision shall be replaced by such '
  'enforceable term or provision as comes closest to the intention underlying the unenforceable term or '
  'provision. This Privacy Policy shall be subject to and do not alter any other agreements you have entered '
  'into with Digital Monitoring Products.',
  []],
 ['Applicable Law',
  'This Site (excluding linked sites) is controlled by Digital Monitoring Products from its offices within '
  'the State of Missouri, United States of America. By accessing this Site, you agree that all matters '
  'relating to your use of this Site and the terms of this Privacy Policy shall be governed by the statutes '
  'and laws of the State of Missouri, and the federal laws of the U.S.A., without regard to the conflicts of '
  'laws principles thereof. The application of the United Nations Convention of Contracts for the '
  'International Sale of Goods, and the model Uniform Computer Information Transactions Act approved by the '
  'National Conference of Commissioners on Uniform State Laws (as enacted and/or modified into any state law '
  'in the U.S.A.), are expressly excluded and shall not apply.',
  []],
 ['Contact Us',
  'If you have any questions about this Privacy Policy, please contact us at info@dmp.com.',
  []]]
TERMS_UPDATED = 'Last Updated: January 2021'
TERMS = [['Introduction',
  'Digital Monitoring Products, on behalf of itself and its subsidiaries and affiliates (“Digital Monitoring '
  'Products”) maintains its website at www.dmp.com (the “Site”) for informational, general promotional, '
  'public information, as well as investor relations purposes. The following Terms of Use apply to your use '
  'of this Site, including any other Digital Monitoring Products-sponsored web logs, forums and social media '
  'sites and forums accessible from the Site and/or maintained by Digital Monitoring Products. By accessing, '
  'browsing, posting comments to, or otherwise using this Site, you agree to be bound by these Terms of Use, '
  'as they may be modified from time to time.',
  []],
 ['Intellectual Property',
  'Digital Monitoring Products retains all copyrights in any text, graphic images, and software owned by '
  'Digital Monitoring Products and hereby authorizes you to electronically copy documents published herein '
  'solely for the purpose of viewing the information for your own individual and/or internal purpose. You '
  'may not otherwise copy, modify, distribute, transmit, display, publish, sell, license, create derivative '
  'works, link to, or use any information on this Site without written permission from Digital Monitoring '
  'Products. Except as expressly provided above, nothing contained herein shall be construed as conferring '
  'any license or right under any Digital Monitoring Products copyright, patent or trademark.\n'
  '\n'
  'Digital Monitoring Products, the Digital Monitoring Products logo, and the other Digital Monitoring '
  'Products names or products referenced herein are trade names, trademarks or service marks of Digital '
  'Monitoring Products, Incorporated or its subsidiaries and affiliates and may not be used without '
  'permission. Digital Monitoring Products® is a registered trademark of Digital Monitoring Products.\n'
  '\n'
  'Other product or company names mentioned herein may be the trade names, trademarks, or service marks of '
  'their respective owners.',
  []],
 ['Disclaimer',
  'The information and materials available on or through this Site, including text, images, and links, are '
  'PROVIDED "AS IS" BY Digital Monitoring Products, SOLELY AS A CONVENIENCE TO VISITORS OF THIS SITE WITHOUT '
  'WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED. Digital Monitoring Products DOES NOT WARRANT THE '
  'ACCURACY, ADEQUACY OR COMPLETENESS OF THIS INFORMATION AND MATERIALS, AND Digital Monitoring Products '
  'EXPRESSLY DISCLAIMS LIABILITY FOR ERRORS OR OMISSIONS IN THIS INFORMATION AND MATERIALS. THERE IS NO '
  'WARRANTY THAT ANY INFORMATION, SERVICE, PRODUCTS, MATERIALS OR OTHER CONTENT OR DATA AVAILABLE ON OR '
  "THROUGH THIS SITE, OR Digital Monitoring Products'S SOFTWARE OR HARDWARE SYSTEMS WILL FULFILL ANY OF YOUR "
  'PARTICULAR PURPOSES OR NEEDS.\n'
  '\n'
  'Digital Monitoring Products DISCLAIMS A WARRANTY OF ANY KIND, IMPLIED, EXPRESSED OR STATUTORY, INCLUDING '
  'THE WARRANTIES OF NON-INFRINGEMENT OF THIRD PARTY RIGHTS, TITLE, MERCHANTABILITY OR QUALITY, FITNESS FOR '
  'A PARTICULAR PURPOSE, ACCURACY OF INFORMATION CONTENT OR DATA, INFORMATION ACCESS AND ORDER EXECUTION, '
  'FREEDOM FROM COMPUTER VIRUS, IN CONNECTION WITH THIS SITE OR AVAILABLE INFORMATION AND MATERIALS, EVEN IF '
  'Digital Monitoring Products HAS BEEN ADVISED OR IS OTHERWISE AWARE OF THE POSSIBILITY OF SUCH DAMAGES.',
  []],
 ['Limited Liability',
  'IN NO EVENT SHALL Digital Monitoring Products (OR ANY OF ITS SUBSIDIARIES OR AFFILIATES) BE LIABLE FOR '
  'ANY DAMAGES, INCLUDING ANY INCIDENTAL, CONSEQUENTIAL, SPECIAL, DIRECT OR INDIRECT DAMAGES, LOSSES, OR '
  'EXPENSES, INCLUDING LOST PROFITS OR BUSINESS OPPORTUNITIES, ARISING IN CONNECTION WITH THE SITE OR ANY '
  'LINKED WEBSITE, OR USE THEREOF OR INABILITY TO USE, BY ANY PARTY OR IN CONNECTION WITH ANY FAILURE OF '
  'PERFORMANCE, ERROR, OMISSION, INTERRUPTION, DEFECT, DELAY IN OPERATION OR TRANSMISSION, COMPUTER VIRUS OR '
  'LINE OR SYSTEM FAILURE, EVEN IF Digital Monitoring Products, OR ITS REPRESENTATIVE THEREOF, IS ADVISED OF '
  'THE POSSIBILITY OF SUCH DAMAGES, LOSSES OR EXPENSES, EXCEPT AS LIMITED BY APPLICABLE LAW. SOME STATES DO '
  'NOT ALLOW THE EXCLUSION OR LIMITATION OF INCIDENTAL OR CONSEQUENTIAL DAMAGES, SO THE ABOVE MAY NOT APPLY '
  'TO YOU.\n'
  '\n'
  'Only those terms and conditions set forth in any definitive agreement duly executed by Digital Monitoring '
  'Products, or any of its affiliates or subsidiaries, shall govern the purchase, use, distribution or other '
  'relationship with Digital Monitoring Products or its products or services. This Site and those that link '
  'into and out of this Site could include technical or other inaccuracies, and not all products or services '
  'referenced herein are available in all areas. Digital Monitoring Products reserves the right to change '
  'the products or services described on this Site at any time. Contact Digital Monitoring Products for '
  'further information before relying on any information contained herein.',
  []],
 ['Data Submitted by You to this Site',
  'You agree that you are solely responsible for the text, graphic images, or other information that you '
  'create, submit, post, or display on or through this Site (collectively, the “Data”) and for the '
  'consequences of your actions. Subject to the terms the Digital Monitoring Products Privacy Policy, you '
  'further agree that you are solely responsible for your Data, and Digital Monitoring Products assumes no '
  'responsibility or liability for any Data posted by you or any third party user of this Site.\n'
  '\n'
  'Digital Monitoring Products reserves the right, but shall have no obligation, to pre-vh, review, flag, '
  'filter, modify, refuse or remove from this Site any Data or any other text, graphic images, or other '
  'information, including without limitation, comments posted to web logs, social media sites or forums '
  'accessible from www.dmp.com or maintained by Digital Monitoring Products. You agree that your Data does '
  'not and will not violate or infringe any copyright, trademark, right of privacy or publicity or other '
  'proprietary rights of any person or entity or constitute libelous, obscene, threatening, abusive or '
  'unlawful matter. Your Data will not include any computer viruses or any commercial messages or '
  'solicitations that have not been approved by Digital Monitoring Products in advance.',
  []],
 ['License from You',
  'By submitting, posting, or displaying your Data on or through this Site, you grant, and represent that '
  'you have the right to grant, to Digital Monitoring Products a perpetual, irrevocable, worldwide, '
  'royalty-free, non-exclusive and sublicensable license to use, reproduce, adapt, modify, create derivative '
  'works from, translate, publish, publicly perform, publicly display, and distribute such Data. Digital '
  'Monitoring Products and its licensees shall also have the right to use your name in connection with their '
  'use of any such Data. You further agree that Digital Monitoring Products has no obligation to respond to '
  'any inquiries, your Data is not provided to Digital Monitoring Products in confidence, and that your Data '
  'is created, submitted, posted or displayed gratuitously and without expectation of compensation. Without '
  'limiting any of Digital Monitoring Products’s rights in the Data, you agree that Digital Monitoring '
  'Products will be free to consider, reproduce, use, disclose and distribute the Data to others, and to use '
  'the Data for any purpose including without limitation, developing, manufacturing, and marketing products '
  'incorporating such Data.',
  []],
 ['Indemnity',
  'You agree to indemnify, defend and hold Digital Monitoring Products and its suppliers or other applicable '
  'related parties, harmless from and against all claims, losses, liability, cost, and expenses (including '
  "attorneys' fees) arising from your violation of these Terms of Use or use or misuse of this Site, or from "
  'the use of any Data or any service, product, information or materials provided through this Site. Your '
  'obligations under this paragraph will survive your termination of access to or use of the Site.',
  []],
 ['Fraudulent, Illegal or Improper Activity',
  'You agree that you will not use this Site for any illegal, fraudulent, unauthorized, or improper activity '
  '(a "Prohibited Use"). If we suspect that you may be engaging in any Prohibited Use, including any '
  'violation of any terms or conditions relating to this Site or any service or product by Digital '
  'Monitoring Products, your access to this Site and any service or product may be suspended or terminated '
  'without notice.',
  []],
 ['Copyright Notices',
  'Digital Monitoring Products respects the rights of all copyright holders. If you believe your copyright '
  'has been infringed, you may notify Digital Monitoring Products by email at info@dmp.com.\n'
  '\n'
  'To be effective, your notice must include substantially the following, as provided for under the Online '
  'Copyright Infringement Liability Limitation Act of the Digital Millennium Copyright Act, 17 U.S.C. '
  '512(c)(3):\n'
  '\n'
  'Digital Monitoring Products has adopted and reasonably implemented a policy that provides for the '
  'termination in appropriate circumstances of subscribers and account holders of Digital Monitoring '
  'Products’s system or network who are repeat infringers.',
  ['Identification of the copyright work claimed to have been infringed, or, if multiple copyrighted works '
   'at a single online site are covered by a single notification, a representative list of such works at '
   'that site',
   'A physical or electronic signature of a person authorized to act on behalf of the owner of an exclusive '
   'right that is allegedly infringed;',
   'Identification of the material that is claimed to be infringing or to be the subject of infringing '
   'activity and that is to be removed or access to which is to be disabled, and information reasonably '
   'sufficient to permit us to locate the material;',
   'Information reasonably sufficient to permit us to contact the complaining party, such as an address, '
   'telephone number, and, if available, an electronic mail address at which the complaining party may be '
   'contacted;',
   'A statement that the complaining party has a good faith belief that use of the material in the manner '
   'complained of is not authorized by the copyright owner, its agent, or the law; and',
   'A statement that the information in the notification is accurate, and under penalty of perjury, that the '
   'complaining party is authorized to act on behalf of the owner of an exclusive right that is allegedly '
   'infringed.']],
 ['Links from this Web Site',
  'This Site contains links to other websites and resources maintained by third parties. The linked sites '
  'may not be under the control of Digital Monitoring Products, and Digital Monitoring Products shall not be '
  'responsible for the content of any linked site or link contained in a linked site. These links are '
  'provided as a convenience only, and the inclusion of any link does not imply an endorsement, affiliation, '
  'or sponsorship by Digital Monitoring Products of that site. Any use of or reliance on any such '
  'information, content, and materials is at your own risk, and may be subject to additional policies or '
  'terms of use provided by the provider thereof.',
  []],
 ['Submissions',
  'You agree to provide true, accurate, current and complete information about yourself when you elect to '
  'provide personal information to Digital Monitoring Products via this Site, including in connection with '
  'registering or creating an account at this Site. You also agree to maintain and promptly update any such '
  'information to keep it accurate. Without limiting the generality of the foregoing, you will not submit '
  'any false or misleading information (including without limitation names or other contact information) or '
  'impersonate any person. To protect your account, you shall keep your password confidential and take full '
  'responsibility for your own and third party activities that occur under or in connection with your '
  'account.',
  []],
 ['Privacy and Security',
  'We understand the need to safeguard certain of your information and records from unauthorized use and '
  'disclosure. Please see Digital Monitoring Products Privacy Policy, which is deemed a part of these Terms '
  'of Use.',
  []],
 ['Cross-border Transmission of Data',
  'Subject to the Digital Monitoring Products Privacy Policy, you acknowledge and agree that by providing '
  'Digital Monitoring Products with your personal or proprietary information in any application or '
  'transaction request through this Site, you hereby consent to the transmission of such personal or '
  'proprietary information to or by Digital Monitoring Products, and its service providers or marketers, '
  'over state and international borders as necessary for handling your application or transaction request in '
  "accordance with Digital Monitoring Products's standard business practices.",
  []],
 ['Enforceability',
  'In the event any of the provisions of these Terms of Use shall be held to be unenforceable, the remaining '
  'provisions shall be unimpaired, and the unenforceable provision shall be replaced by such enforceable '
  'term or provision as comes closest to the intention underlying the unenforceable term or provision. These '
  'Terms of Use shall be subject to and do not alter any other agreements you have entered into with Digital '
  'Monitoring Products.',
  []],
 ['Applicable Law',
  'This Site (excluding linked sites) is controlled by Digital Monitoring Products from its offices within '
  'the State of Missouri, United States of America. By accessing this Site, you agree that all matters '
  'relating to your use of this Site shall be governed by the statutes and laws of the State of Missouri, '
  'and the federal laws of the United States of America without regard to the conflicts of laws principles '
  'thereof. The application of the United Nations Convention of Contracts for the International Sale of '
  'Goods, and the model Uniform Computer Information Transactions Act approved by the National Conference of '
  'Commissioners on Uniform State Laws (as enacted and/or modified into any state law in the U.S.A.), are '
  'expressly excluded and shall not apply.',
  []],
 ['Amendments',
  'We may change, amend or discontinue this Site (or any portion thereof) at any time without prior notice '
  'or obligation to you. We may also change these Terms of Use at any time without prior notice, and your '
  'continued use of this Site after such changes have been posted will constitute your acceptance of the '
  'changes.',
  []]]

def legal_page(file, name, updated, secs, crumb, descr, intro):
    sections = [{"type": "hero", "layout": "centered", "eyebrow": updated.replace("Last Updated:", "Last updated"), "heading": name, "subhead": intro}]
    for h, body, bullets in secs:
        d = {"type": "detail", "heading": h, "body": body}
        if bullets: d["bullets"] = bullets
        sections.append(d)
    return {"file": file, "title": title(name), "description": desc(descr),
            "crumbs": [["Home", "index.html"], [crumb, file]], "sections": sections}


def news_page(slug, date_label, ttl, descr, hero, body_sections, tags=None):
    return {"file": f"news/{slug}.html", "title": title(ttl), "description": desc(descr),
            "crumbs": [["Home", "index.html"], ["Resources", "resources.html"], [ttl, f"news/{slug}.html"]],
            "sections": [hero] + body_sections + [LEADFORM]}


def hero_news(eyebrow, heading, subhead, image, alt, secondary=None):
    h = {"type": "hero", "layout": "split", "eyebrow": eyebrow, "heading": heading, "subhead": subhead,
         "primary": CTA, "image": image, "image_alt": alt, "image_w": 1200, "image_h": 800}
    if secondary: h["secondary"] = secondary
    return h


PAGES = []

# ----------------------------------------------------------------------------------------------- careers
PAGES.append({
    "file": "about/careers.html", "title": title("Careers in Springfield, Missouri"),
    "description": desc("Work at a family-owned tech company in the Ozarks: manufacturing, sales, tech support and software engineering jobs, an on-site medical clinic and a free home security system."),
    "crumbs": [["Home", "index.html"], ["About", "about.html"], ["Careers", "about/careers.html"]],
    "sections": [
        hero_news("Careers", "A family-owned tech company <em>in the Ozarks</em>",
                  "We design, engineer and manufacture security systems for commercial and residential applications, in Springfield, Missouri. Joining us means joining a team committed to its mission and values, including giving back to the community and pursuing excellence every day.",
                  IMG + "hq-exterior-1200.jpg", "The DMP headquarters in Springfield, Missouri",
                  {"label": "How we give back", "href": "about/dmp-cares.html"}),
        {"type": "cards", "alt": True, "eyebrow": "Benefits", "heading": "A medical clinic on site and a security system at home",
         "items": [["Care close to your desk", "An on-site family medical clinic, plus medical, dental and vision insurance."],
                   ["Savings with a company match", "Health savings accounts with a company match, a 401k and Roth IRA savings plan with a company match, and flexible savings and dependent care savings accounts."],
                   ["Time away", "Paid time off and 8 paid holidays."],
                   ["Learning and rewards", "Tuition reimbursement and a bonus program."],
                   ["Coverage beyond the basics", "Life insurance, supplemental benefits and voluntary coverages."],
                   ["Our product, in your home", "A free home security system for every employee."]]},
        {"type": "detail", "eyebrow": "Where you could work", "heading": "Jobs in manufacturing, sales, tech support and software engineering",
         "body": "Discover work worth doing at DMP. Open positions are listed in our careers portal, where you can search manufacturing, sales, tech support, software engineering jobs and more.",
         "bullets": ["Manufacturing", "Sales", "Tech support", "Software engineering"],
         "image": IMG + "plant-1200.jpg", "image_alt": "The DMP manufacturing floor in Springfield, Missouri", "flip": True},
        {"type": "proof", "alt": True, "eyebrow": "Mission and values", "value": "Our mission and values are not just generic words. We live by our mission and values every day.",
         "text": "It's a combination of our products and people that defines the integrity we're known for. I don't think you can find a mission statement that fits our company better.",
         "source": "A DMP team member"},
        {"type": "cta", "heading": "Giving is one of our company values", "subhead": "We create opportunities for our employees and their families to give money, time and talent.",
         "primary": {"label": "Read about DMP Cares", "href": "about/dmp-cares.html"}},
        LEADFORM]})

# ----------------------------------------------------------------------------------------------- DMP Cares
PAGES.append({
    "file": "about/dmp-cares.html", "title": title("DMP Cares"),
    "description": desc("Generosity is one of our company values. We support worthy causes and give our people the chance to give money, time and talent, with a goal of 50,000 volunteer hours."),
    "crumbs": [["Home", "index.html"], ["About", "about.html"], ["DMP Cares", "about/dmp-cares.html"]],
    "sections": [
        hero_news("DMP Cares", "Giving is one of our <em>company values</em>",
                  "We believe the blessings of generosity extend well beyond the recipient. DMP Cares is the sum of our efforts, and of each person's commitment to a lifestyle of generosity.",
                  IMG + "team-2021-1200.jpg", "The DMP team at the Springfield, Missouri headquarters"),
        {"type": "cards", "alt": True, "eyebrow": "How we give", "heading": "Money, time and talent: three ways our people give",
         "items": [["We support worthy causes", "As a company, we support a number of worthy causes."],
                   ["We make room for families", "We create opportunities for our employees and their families to contribute."],
                   ["Hands-on giving counts", "Contributions are sometimes financial, but we also encourage personal, hands-on donations of time and talent."]]},
        {"type": "proof", "eyebrow": "Why it matters", "value": "We want our people to be generous people.",
         "text": "Giving serves others in need and reminds us to be thankful for our many blessings.", "source": "Our company value of generosity"},
        {"type": "detail", "alt": True, "eyebrow": "Volunteer hours", "heading": "Our team is working toward 50,000 volunteer hours",
         "body": "We are excited to work together toward 50,000 volunteer hours. Team members log their volunteer time in our HR system under the 2025 BHAG, Track to 50,000 Volunteer Hours.",
         "bullets": ["Volunteer time is self-reported by each team member", "The goal is shared across the whole company"]},
        {"type": "values", "eyebrow": "Our value", "heading": "Generosity, in our own words",
         "items": [["Serve with your time", "Serve others with your time."], ["Serve with your money", "Serve others with your money."], ["Personal fulfillment", "Giving to others leads to personal fulfillment and happiness."]]},
        {"type": "cta", "heading": "Want to work somewhere that gives back?", "subhead": "See what it is like to work at a family-owned company in the Ozarks.",
         "primary": {"label": "Careers at DMP", "href": "about/careers.html"}},
        LEADFORM]})

# ----------------------------------------------------------------------------------------------- certifications
PAGES.append({
    "file": "about/certifications.html", "title": title("Certifications"),
    "description": desc("DMP completes an independent SOC 2 Type II examination every year for Dealer Admin and Virtual Keypad, hosted in a Tier 4 data center. A SOC 3 report is public."),
    "crumbs": [["Home", "index.html"], ["About", "about.html"], ["Certifications", "about/certifications.html"]],
    "schema": [{"@context": "https://schema.org", "@type": "WebPage", "name": "Certifications", "about": "SOC 2 Type II"}],
    "sections": [
        hero_news("Certifications", "Our SOC 2 Type II controls, <em>examined every year</em>",
                  "Dealer Admin and Virtual Keypad, our SaaS applications, are hosted in a Tier 4 data center and examined independently each year in line with AICPA standards.",
                  IMG + "tab-mobile-1200.jpg", "Virtual Keypad on a phone"),
        {"type": "detail", "alt": True, "eyebrow": "Where it runs", "heading": "Dealer Admin and Virtual Keypad are hosted in a Tier 4 data center",
         "body": "In today's digital world, security is paramount. Tier 4 is designed to host mission-critical servers with fully redundant subsystems and compartmentalized security zones.",
         "bullets": ["Fully redundant cooling, power, network links and storage", "Compartmentalized security zones", "Hosts the Dealer Admin and Virtual Keypad SaaS applications"]},
        {"type": "cards", "eyebrow": "SOC 2 Type II", "heading": "Independent examination, a public SOC 3 report and SOC 2 reports under confidentiality",
         "items": [["Examined every year", "We complete independent SOC 2 Type II examinations annually, conducted by a licensed CPA firm in accordance with standards established by the American Institute of Certified Public Accountants (AICPA)."],
                   ["A SOC 3 report for everyone", "The SOC 3 report is intended for public distribution."],
                   ["SOC 2 reports for customers and partners", "SOC 2 reports are available to customers and partners under appropriate confidentiality arrangements."]]},
        {"type": "cards", "alt": True, "eyebrow": "Beyond SOC 2", "heading": "Listings and approvals: UL 2610, UL Listed panels and FirstNet",
         "items": [["JamAlert is UL 2610 certified", "Our cellular jamming detection technology has achieved UL 2610 certification, the standard for commercial premises security alarm units and systems."],
                   ["A UL Listed combination panel since 1997", "In 1997 we introduced a UL Listed combination burglary, fire and access control panel."],
                   ["Communicators approved for FirstNet", "We offer communicators approved for use on the FirstNet mobile broadband public-safety network, and made the first alarm panel communicator for the AT&T FirstNet network."],
                   ["Manufactured in the USA", "Our products are manufactured in Springfield, Missouri, with U.S. and global components."]]},
        {"type": "resources", "heading": "Read more", "intro": "The stories and product pages behind these listings.",
         "items": [["News, 6 May 2026", "JamAlert achieves UL certification", "How UL 2610 certification lets dealers specify JamAlert where UL Listed equipment is required.", "Read the story", "news/jamalert-ul.html"],
                   ["Product", "JamAlert", "Cellular jamming detection that works with DMP and other alarm systems.", "View product", "products/jamalert.html"],
                   ["Software", "Virtual Keypad", "The mobile and web platform covered by our SOC 2 Type II examination.", "See mobile and automation", "services/mobile-automation.html"]]},
        {"type": "faq", "heading": "Questions about our SOC reports",
         "items": [["Which applications are covered?", "The Dealer Admin and Virtual Keypad SaaS applications, which are hosted within a Tier 4 data center."],
                   ["How often is the examination done?", "Annually, by a licensed CPA firm, in accordance with AICPA standards."],
                   ["Who can see the SOC 2 report?", "Customers and partners, under appropriate confidentiality arrangements. The SOC 3 report is intended for public distribution."]]},
        LEADFORM]})

# ----------------------------------------------------------------------------------------------- events
PAGES.append({
    "file": "events.html", "title": title("Dealer events and technician training"),
    "description": desc("Technician Bootcamps, an Advanced Bootcamp, a Detroit Tech Training Tour, two Dealer Roundtables and Owners Forum 2027: events for dealer executives, technicians, sales and marketing."),
    "crumbs": [["Home", "index.html"], ["Events", "events.html"]],
    "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "Events",
         "heading": "Owner or technician, <em>there is an event for you</em>",
         "subhead": "Whether you are a DMP dealer executive, technician, salesperson or marketing professional, we have an event for you and your team.",
         "primary": CTA, "secondary": {"label": "Training programs", "href": "training.html"}},
        {"type": "cards", "alt": True, "eyebrow": "Technician training", "heading": "Six hands-on training events for dealer technicians",
         "items": [["Technician Bootcamp, December", "3 1/2 days of instruction and hands-on training labs for dealer technicians with basic alarm installation experience, basic computer skills and mobile app exposure. Covers XTLtouch, 1100 Series Wireless, XT Series, XR Series, Dealer Admin, Virtual Keypad, the AlarmVision demo and X1 Series. Includes the XTLtouch package, a bootcamp bag, shirt and hat."],
                   ["Technician Bootcamp, January", "The same 3 1/2 day agenda, taught by a Regional Training Manager, with the XTLtouch package. Times are listed in Central time."],
                   ["Tech Training Tour, January, Detroit, Michigan", "3 days of instruction and hands-on labs, brought to Detroit with Axis Communications. Led by Field Sales Engineer, North Central, Brian Butterfield. The preliminary agenda covers XR and XT75 access control, 1100 Series Wireless, XV with AlarmVision and cameras, the VUE Video Doorbell, Virtual Keypad and XF6. Times are Eastern. Includes a Tech Training Tour hat."],
                   ["Technician Bootcamp, February", "3 1/2 days with the same agenda, from the product tour and DMP Foundations to the final test and closing ceremony. Includes the XTLtouch package."],
                   ["Advanced Technician Bootcamp, March", "For experienced technicians who have completed our base Technician Bootcamp. Covers IP networking, the Dealer Admin and Tech apps, the Virtual Keypad app, the XR550 system, XR550 access control, wireless and fire, DMP camera technology and troubleshooting. Includes an XR550 training kit, a bootcamp tool bag, shirt, wire cutters, flashlight, DMP decal, an Advanced Master Tech Pocket Coin, an online certificate, a workbook and catered lunches and breaks."],
                   ["Technician Bootcamp, March", "3 1/2 days of instruction and hands-on labs, finishing with a final test and survey and a lunch and closing ceremony. Includes the XTLtouch package."]]},
        {"type": "timeline", "id": "dealer-events", "eyebrow": "For owners and executives", "heading": "Dealer Roundtables in San Diego and Hilton Head, and Owners Forum 2027 in Las Vegas",
         "intro": "Space is limited at each event. Register before the date shown.",
         "items": [["8 and 9 February 2027", "Dealer Roundtable, San Diego", "At the San Diego Mission Bay Resort, 1775 E Mission Bay Dr. We have secured a group rate of $239. Register before Tuesday, 12 January 2027."],
                   ["Register by 15 March 2027", "Owners Forum 2027, Las Vegas", "At Resorts World Las Vegas, with a free shuttle between Resorts World and ISC West for guests in the DMP room block. Includes the annual DMP Dealer Recognition Awards."],
                   ["4 and 5 October 2027", "Dealer Roundtable, Hilton Head", "At the Hilton Beachfront Resort and Spa, Hilton Head Island. We have secured a group rate of $269, available first come, first served. Register before Friday, 17 September 2027."]]},
        {"type": "detail", "alt": True, "eyebrow": "Dealer Roundtable", "heading": "One and a half days of dealers teaching dealers",
         "body": "The Dealer Roundtable is hosted by members of the DMP Executive Management Group, including Owner and President Rick Britton. It gives DMP dealers and security personnel from around the country a chance to discuss best practices. Each topic runs about 30 minutes, followed by 15 minutes of discussion or a tabletop exercise, and most topics are presented or facilitated by other dealers.",
         "bullets": ["For owners and executive leadership, senior management, operations management and sales and marketing management",
                     "San Diego topics include the common-sense use of AI for sales and selling, a dealer panel, how DMP Sales Engineers can help you grow your sales, new things coming to the DMP Dealer Program, and the power of VK VMS as a unified platform",
                     "Hilton Head includes a session on navigating insurance claims as a dealer"]},
        {"type": "detail", "eyebrow": "Owners Forum 2027", "heading": "Connect with peers, learn to scale, and celebrate the Dealer Recognition Awards",
         "body": "Owners Forum is an exclusive opportunity to connect with industry peers, engage in meaningful collaboration and discover the keys to scaling your business. Please register by Monday, 15 March 2027.",
         "bullets": ["Speakers include a former LA Chargers Gameday host, a CEO who multiplied revenue for Tesla and Lyft, a TEDx speaker and top expert in business scaling, and an organizational psychologist who has sold millions of books",
                     "A dealer panel and the annual DMP Dealer Recognition Awards",
                     "High-level agenda: registration and breakfast at 8:00 a.m., opening remarks at 9:00 a.m., dealer awards at 10:00 a.m., lunch at 12:00 p.m., adjourn at 3:30 p.m.",
                     "Hosted at Resorts World Las Vegas, 3000 S Las Vegas Blvd"], "flip": True},
        {"type": "proof", "alt": True, "eyebrow": "From our dealers", "value": "I find the direct personal interaction with the DMP management team to be unique in our industry.",
         "text": "Each member of the team is eager to discuss questions and concerns of their dealer network. They truly have an interest in my company.", "source": "A DMP dealer"},
        LEADFORM]})

# ----------------------------------------------------------------------------------------------- international
DIST = [("Benelux (Belgium, Netherlands, Luxembourg)", "Sabelco", "https://sabelco.com", "Mark NeSmith"),
        ("Greece and Cyprus", "GQ Tech", "https://gqt.gr/el", "Mark NeSmith"),
        ("Hungary", "Object Guard", "https://www.objekt-or.hu/", "Mark NeSmith"),
        ("Latin America and the Caribbean", "ISTC", "https://istccorp.com/", "Mark NeSmith"),
        ("Mexico", "Otwo", "https://otwo.com.mx/", "Mark NeSmith"),
        ("Mexico", "Tecnoseguridad", "https://tecnoseguridad.mx/", "Mark NeSmith"),
        ("South Africa, Mozambique and Zambia", "Regal", "https://regalsecurity.co.za/", "Mark NeSmith"),
        ("United Kingdom and Ireland", "ADI EU", "https://www.adiglobal.com/", "Doug Dacre")]
PAGES.append({
    "file": "international.html", "title": title("International distributors and products"),
    "description": desc("Eight authorized DMP distributors serve Benelux, Greece and Cyprus, Hungary, Latin America, Mexico, South Africa and the UK and Ireland, with international panels and technical support."),
    "crumbs": [["Home", "index.html"], ["International", "international.html"]],
    "schema": [itemlist("Authorized DMP international distributors", [[d[1], d[2]] for d in DIST])],
    "sections": [
        hero_news("International", "Tested before it ships, <em>wherever it ships</em>",
                  "DMP products are built to meet real security needs with powerful features and dependable performance. They are available through authorized dealers and distributors internationally.",
                  IMG + "plant-1200.jpg", "DMP products being built in Springfield, Missouri",
                  {"label": "Browse our systems", "href": "services.html"}),
        {"type": "resources", "id": "find-your-distributor", "heading": "Find your distributor: eight authorized partners, from Benelux to South Africa",
         "intro": "To locate DMP products in your region, start with the authorized distributor for your country.",
         "items": [[d[0], d[1], f"Authorized DMP distributor. Our contact for this region is {d[3]}.", f"Visit {d[1]}", d[2]] for d in DIST]},
        {"type": "cards", "alt": True, "eyebrow": "International products", "heading": "International versions of our panels, keypads, wireless, communicators and video",
         "items": [["Control panels", "XR550, XR150, XT30, XTLplus and XTLtouch international control panels (the XTLtouch is the all-in-one), plus the International Panel Pack."],
                   ["Keypads", "The International Thinline Series Keypad and the International 5-Inch Touchscreen Keypad."],
                   ["Wireless", "1100D and 1100X international wireless receivers, the 1100R repeater, the 1122 PIR, 1128 glassbreak detector, 1135 siren, 1142 two-button panic, 1144 key fobs and 1103 transmitter."],
                   ["Cell and network communicators", "The 263LTE International Cellular Communicator, the 383 International Cellular Antenna LTE and the 386 International Antenna Mounting Bracket."],
                   ["Video", "International XV Gateways with AlarmVision."],
                   ["Power supplies, modules and expanders", "The 503 power supply, 324 wire-in transformer, 318T, 318EXT and 318R battery harnesses, 381-25 and 381-12 SMA extension cables and 381-2 coax cable, plus the 712-8, 714-16, 714-8, 714-8PCB zone expansion modules, the 716 output expansion module and the 860 relay output module."]]},
        {"type": "detail", "eyebrow": "International team", "heading": "Reach our international team in Springfield",
         "body": "For more information on locating authorized dealers or distributors around the world, contact DMP Customer Service at +1-866-266-2826 or CustomerService@DMP.com.",
         "bullets": ["International Sales: Mark NeSmith, MNeSmith@dmp.com, 417-839-2547",
                     "International Sales: Doug Dacre, DDacre@dmp.com, (417) 447-9629",
                     "Mark NeSmith is our contact for every region except the United Kingdom and Ireland, which is Doug Dacre"]},
        {"type": "detail", "alt": True, "eyebrow": "Technical support", "heading": "International technical support runs from 11:00 a.m. to 12:00 a.m. GMT",
         "body": "Representatives are available from 11:00 a.m. to 12:00 a.m. GMT (6:00 a.m. to 7:00 p.m. Central). For support outside business hours, email InternationalSupport@dmp.com and we will schedule a call.",
         "bullets": ["Toll-free numbers for eight countries are listed below", "Email InternationalSupport@dmp.com for after-hours calls"], "flip": True},
        {"type": "cards", "eyebrow": "Toll-free numbers", "heading": "Toll-free technical support in Belgium, France, Germany, Greece, Ireland, Mexico, South Africa and the United Kingdom",
         "items": [["Belgium", "+32080054707"], ["France", "+330805089291"], ["Germany", "+4908001825459"], ["Greece", "+308008481019"],
                   ["Ireland", "+3531800816836"], ["Mexico", "+52018003511041"], ["South Africa", "+270800014664"], ["United Kingdom", "+4408081349543"]]},
        {"type": "detail", "alt": True, "eyebrow": "Customs and tariffs", "heading": "Every physical DMP product carries a six-digit Harmonized System code",
         "body": "The Harmonized System (HS) code is part of the international Harmonized Tariff System and is used to establish any tariff rates due when a DMP customer imports DMP goods into another country, or when we are the importer. Because future exports may not be known when a product is released, every physical product is assigned a code, as are sales literature and marketing giveaways. Software and other products delivered electronically do not need one. For example, DMP is the importer in Canada when a dealer buys products and their account is set to pay in Canadian dollars.",
         "bullets": ["Burglar or fire alarms and similar apparatus, including keypads, door contacts and monitoring hardware: 8531.10",
                     "Parts and accessories for alarm systems, and access control readers and hardware: 8531.90",
                     "Access credentials such as proximity and smart cards: 8523.51",
                     "Cellular antennas: 8529.10, and coaxial cable: 8544.70"]},
        LEADFORM]})

# ----------------------------------------------------------------------------------------------- legal
PAGES.append(legal_page("privacy-policy.html", "Privacy Policy", PRIV_UPDATED, PRIV, "Privacy Policy",
                        "How Digital Monitoring Products collects, uses, discloses and protects personal information, and how to opt out of marketing communications.",
                        "How we collect, use, disclose and protect Personal Information."))
PAGES.append(legal_page("terms-of-use.html", "Terms of Use", TERMS_UPDATED, TERMS, "Terms of Use",
                        "The terms that govern use of the Digital Monitoring Products website, including intellectual property, disclaimers, liability and applicable law.",
                        "The terms that apply to your use of our website."))

# ----------------------------------------------------------------------------------------------- news
NEWS = []
NEWS.append(["News, 11 Sep 2026", "DMP launches VK VMS, enabling 24/7 video management with AlarmVision", "A cloud video management system inside Virtual Keypad, with new XV Plus Gateways.", "Read the story", "news/vk-vms.html"])
PAGES.append(news_page("vk-vms", "", "DMP launches VK VMS, enabling 24/7 video management with AlarmVision",
  "VK VMS adds live video viewing and on-site device management to Virtual Keypad, with AlarmVision Plus and Pro subscriptions and new XV Plus Gateways.",
  hero_news("News, 11 September 2026", "VK VMS: <em>24/7 video management</em> with AlarmVision",
            "Launch expands our Gateway family with new XV Plus Gateways.", IMG + "xv-plus-gateway-1200.jpg", "A DMP XV Plus Gateway", {"label": "See video systems", "href": "services/video.html"}),
  [{"type": "detail", "alt": True, "eyebrow": "SPRINGFIELD, Mo.", "heading": "A cloud video management solution built into Virtual Keypad",
    "body": "VK VMS is a new cloud-based, integrated video management solution that delivers live video viewing and on-site device management to our flagship Virtual Keypad platform. The launch introduces AlarmVision subscription tiers and XV Plus Gateways, enabling professional monitoring in our growing video platform.",
    "bullets": ["Activated through the new XV Plus Gateway hardware", "Dealers can offer VK VMS independently of our patented AlarmVision technology, which is now a suite of analytic subscriptions",
                "Announced availability: September 29", "Shown at the DMP booth (#3205) at GSX, September 14 to 16"]},
   {"type": "cards", "heading": "Dealers can sell VK VMS, AlarmVision, or both together",
    "items": [["VK VMS for surveillance", "Video management and surveillance, with live viewing and on-site device management."],
              ["AlarmVision for intelligent detection", "Analytics that detect and classify activity."],
              ["Both, for continuous recording on events", "Combine them to add continuous recording to zone-linked events, so users can detect and classify activity, review footage and preserve video for future investigation."]]},
   {"type": "cards", "alt": True, "eyebrow": "AlarmVision subscriptions", "heading": "Our previous AlarmVision subscription is now two options: Plus and Pro",
    "items": [["AlarmVision Plus", "The natural next evolution of the award-winning AlarmVision technology. Designed with VUE Plus Cameras in mind, it lets cameras serve as zones within the alarm system, enabling smart detection and scene awareness."],
              ["AlarmVision Pro", "Builds on those capabilities with AI that understands activity in context, generates detailed event descriptions and lets users search recorded video using natural language and specific attributes."],
              ["Search by what you remember", "Users can search for a person based on clothing, appearance, activity or location rather than manually reviewing hours of footage."],
              ["Dynamic Slicing", "Preserves full-resolution image detail for earlier, more accurate detection at greater distances."]]},
   {"type": "proof", "eyebrow": "Why we built it", "value": "We heard our dealers clearly.",
    "text": "They want more video management functionality and flexibility in how they deploy and quote AlarmVision. VK VMS and the new AlarmVision options are a direct response to that feedback.", "source": "Ken Francis, Executive Vice President of Video Solutions"},
   {"type": "cards", "alt": True, "eyebrow": "XV Plus Gateways", "heading": "Three XV Plus Gateways: 20 rated megapixels with 1 TB, or 80 with 4 TB",
    "items": [["XV Plus-20", "Supports up to 20 rated camera megapixels and includes 1 TB of video storage."],
              ["XV Plus-80", "Supports up to 80 rated camera megapixels and includes 4 TB of storage, as a desktop unit."],
              ["XV Plus-80R", "The rackmounted version: up to 80 rated camera megapixels and 4 TB of storage."],
              ["Simpler installation", "All models eliminate the need for inbound ports, port forwarding or a separate VPN appliance."]]},
   {"type": "resources", "heading": "Related products and systems", "intro": "Where the VK VMS launch fits in our video platform.",
    "items": [["Product", "XV Plus Gateways with AlarmVision", "The gateway hardware that activates VK VMS.", "View product", "products/xv-gateways-with-alarmvision.html"],
              ["Product", "VUE Plus 8MP Varifocal Bullet Camera", "VUE Plus cameras are designed to work with AlarmVision Plus.", "View product", "products/vplus-7081-bdv.html"],
              ["System", "Video", "Our video systems, from cameras to monitoring.", "See video systems", "services/video.html"]]}]))

NEWS.append(["News, 1 Jul 2026", "The next evolution of the VUE portfolio is here", "VUE Plus cameras add varifocal, panoramic and fisheye models with onboard AlarmVision.", "Read the story", "news/vue-portfolio.html"])
PAGES.append(news_page("vue-portfolio", "", "The next evolution of the VUE portfolio is here",
  "VUE Plus cameras add varifocal, panoramic and fisheye models in 6MP, 8MP and 12MP, with onboard AlarmVision, ONVIF compliance and direct XR and XT panel integration.",
  hero_news("News, 1 July 2026", "VUE Plus cameras bring <em>AlarmVision to the edge</em>",
            "A new line of professional-grade cameras built to help you deliver specialty lenses, optimized performance and enhanced capabilities to your customers.",
            IMG + "vue-plus-1200.jpg", "A VUE Plus camera", {"label": "See video systems", "href": "services/video.html"}),
  [{"type": "detail", "alt": True, "eyebrow": "Introducing VUE Plus", "heading": "Smarter optics, built-in intelligence and alarm panel integration",
    "body": "We are building on an established professional-grade video portfolio with the launch of VUE Plus cameras. New varifocal, panoramic and fisheye models join the existing VUE line, with higher resolution, direct panel integration, lower light use and onboard analytics built for the demands of professional alarm monitoring.",
    "bullets": ["Available now through authorized DMP dealers worldwide", "Backed by our support, training and warranty programs"]},
   {"type": "cards", "heading": "A camera that knows when the panel is armed and which events are real",
    "items": [["Direct panel connection", "VUE Plus cameras connect directly to our XR and XT Series intrusion control panels, so the camera understands when a system is armed and responds accordingly."],
              ["Onboard analytics", "The cameras distinguish meaningful threats from routine activity, helping ensure only true alarm events are communicated to the panel."],
              ["Fewer nuisance alarms", "Intelligent analytics and intrusion detection work together to reduce nuisance alarms and improve response confidence."],
              ["Resolutions and zones", "Available in 6MP, 8MP and 12MP, with up to four areas of interest or boundary boxes per camera for precise, zone-level alarm verification."],
              ["Deterrence and two-way audio", "Select models add red and blue or white deterrence lighting and two-way audio, for real-time response to suspicious activity directly from the camera."],
              ["Open architecture", "VUE Plus cameras are ONVIF-compliant, giving dealers and end users greater control over how video systems are deployed, integrated and expanded."]], "alt": True},
   {"type": "proof", "eyebrow": "On the launch", "value": "By bringing AlarmVision directly to the edge, your cameras will know when your panel is armed without additional hardware or complex integrations.",
    "text": "The security industry is being asked to verify alarms faster, respond smarter and reduce false dispatches. VUE Plus cameras do exactly that by combining onboard intelligence with direct panel integration.", "source": "Rick Britton, CEO"},
   {"type": "resources", "heading": "Eight VUE Plus models: varifocal, panoramic, mini dome and fisheye",
    "intro": "Each model has its own product page.",
    "items": [["8MP bullet", "VUE Plus 8MP Varifocal Bullet Camera", "VPLUS-7081-BDV", "View product", "products/vplus-7081-bdv.html"],
              ["8MP bullet", "VUE Plus 8MP Panoramic Bullet Camera", "VPLUS-7081-BDP", "View product", "services/video.html"],
              ["8MP dome", "VUE Plus 8MP Mini Dome Camera", "VPLUS-7081-MD", "View product", "services/video.html"],
              ["8MP dome", "VUE Plus 8MP Varifocal Dome Camera", "VPLUS-7081-DV", "View product", "services/video.html"],
              ["6MP fisheye", "VUE Plus 6MP Fisheye Camera", "VPLUS-7061-FE", "View product", "products/vplus-7061-fe.html"],
              ["12MP fisheye", "VUE Plus 12MP Fisheye Camera", "VPLUS-7121-FE", "View product", "products/vplus-7121-fe.html"],
              ["8MP turret", "VUE Plus 8MP Varifocal Turret Camera", "VPLUS-7081-TDV", "View product", "services/video.html"],
              ["8MP turret", "VUE Plus 8MP Panoramic Turret Camera", "VPLUS-7081-TDP", "View product", "services/video.html"]]},
   {"type": "detail", "alt": True, "eyebrow": "Documents", "heading": "A sales sheet, a video booklet and a spec sheet for every VUE Plus model",
    "body": "Literature that goes with the VUE Plus launch, available from DMP.",
    "bullets": ["LT-3199 VUE Plus Cameras Sales Sheet", "LT-3110 Video Solutions Booklet", "LT-3195 VUE Plus 8MP Varifocal Bullet Camera Spec Sheet", "LT-3193 VUE Plus 8 MP Panoramic Bullet Camera Spec Sheet",
                "LT-3192 VUE Plus 8MP Mini Dome Camera Spec Sheet", "LT-3196 VUE Plus 8MP Varifocal Dome Camera Spec Sheet", "LT-3191 VUE Plus 6MP Fisheye Camera Spec Sheet",
                "LT-3198 VUE Plus 12MP Fisheye Camera Spec Sheet", "LT-3197 VUE Plus 8MP Varifocal Turret Camera Spec Sheet", "LT-3194 VUE Plus 8MP Panoramic Turret Camera Spec Sheet"]}]))

NEWS.append(["News, 6 May 2026", "JamAlert achieves UL certification", "UL 2610 certification for JamAlert in commercial burglary applications.", "Read the story", "news/jamalert-ul.html"])
PAGES.append(news_page("jamalert-ul", "", "JamAlert achieves UL certification for commercial burglary applications",
  "JamAlert cellular jamming detection has achieved UL 2610 certification, the standard for commercial premises security alarm units and systems.",
  hero_news("News, 6 May 2026", "JamAlert earns <em>UL certification</em> for commercial burglary applications",
            "Our cellular jamming detection technology has achieved UL 2610 certification.", IMG + "jamalert-1200.jpg", "A JamAlert cellular jamming detector", {"label": "Our certifications", "href": "about/certifications.html"}),
  [{"type": "detail", "alt": True, "eyebrow": "Springfield, MO", "heading": "UL 2610 is the standard for commercial premises security alarm units and systems",
    "body": "UL 2610 defines requirements for how commercial intrusion and holdup alarm systems must be designed, built, tested and perform. The certification marks a significant milestone for JamAlert, providing independent validation of its performance and reliability while expanding its applicability in regulated and compliance-driven environments.",
    "bullets": ["Standard: UL 2610", "Applies to: commercial burglary applications", "Product: JamAlert cellular jamming detection technology"]},
   {"type": "cards", "heading": "Cellular jamming is hard to test in the field, so UL tested it for you",
    "items": [["Field testing is impractical", "Cellular jamming remains a growing concern, but because the use of jamming devices is restricted, real-world testing is not practical for dealers or end users."],
              ["Controlled conditions", "JamAlert was evaluated under controlled conditions to meet established UL standards, so it performs as intended when it matters most."],
              ["Specify it where UL Listed is required", "Dealers can more easily specify JamAlert in projects with strict compliance, insurance or AHJ requirements, helping streamline approvals."]]},
   {"type": "proof", "alt": True, "eyebrow": "On the certification", "value": "Achieving UL certification for JamAlert is an important step forward for both our dealers and their customers.",
    "text": "It provides the third-party validation the industry has been looking for, while also enabling deployment in applications where UL Listed components are required.", "source": "Brad Tucker, Vice President of Product Management and Support"},
   {"type": "detail", "eyebrow": "Compatibility", "heading": "JamAlert works with DMP and other alarm systems",
    "body": "JamAlert integrates with DMP or other alarm systems to detect and alert on potential cellular jamming activity, helping ensure uninterrupted alarm communication."},
   {"type": "resources", "alt": True, "heading": "Related products and systems", "intro": "Where JamAlert fits.",
    "items": [["Product", "JamAlert", "Cellular jamming detection technology.", "View product", "products/jamalert.html"],
              ["System", "Communicators", "Cellular and network communicators for DMP panels.", "See communicators", "services/communicators.html"],
              ["System", "Intrusion", "Burglary and holdup systems for commercial buildings.", "See intrusion", "services/intrusion.html"]]}]))

NEWS.append(["News, 27 Apr 2026", "XR650 wins top honors at 2026 ESX Innovation Awards", "The XR650 takes the Intrusion Innovation Award and Best of Show.", "Read the story", "news/xr650-esx-award.html"])
PAGES.append(news_page("xr650-esx-award", "", "XR650 wins Intrusion Innovation Award and Best of Show at 2026 ESX",
  "The XR650 enterprise control panel won the Intrusion Detection category and Best of Show at the 2026 Electronic Security Expo Innovation Awards in Irving, Texas.",
  hero_news("News, 27 April 2026", "XR650 wins <em>Best of Show</em> at ESX 2026",
            "Our category-winning enterprise control panel earns the event's highest overall honor.", IMG + "xr650-esx-1200.jpg", "DMP team members on stage at ESX with the XR650 display beside them", {"label": "Intrusion systems", "href": "services/intrusion.html"}),
  [{"type": "detail", "alt": True, "eyebrow": "Irving, Texas", "heading": "The XR650 was named Best of Show at the 2026 Electronic Security Expo",
    "body": "The ESX Innovation Awards recognize products that advance the security industry across a variety of technology categories. The XR650 was first named the winner of the Intrusion Detection category.",
    "bullets": ["Category winner: Intrusion Detection", "Overall honor: Best of Show", "Event: 2026 Electronic Security Expo (ESX), Irving, Texas"]},
   {"type": "cards", "heading": "From category winner to Best of Show in a live presentation",
    "items": [["Intrusion Detection winner", "The XR650 was named winner of the Intrusion Detection category."],
              ["The TechVision Challenge", "As one of the highest-scoring Innovation Award recipients across all categories, we were invited to compete, with finalists presenting live to a panel of distinguished integrator judges."],
              ["Best of Show", "Mark Hillenburg, Vice President of Industry Relations, Ken Francis, Vice President of Video Solutions, and Meg DiVito, Director of Marketing, represented DMP in the challenge."]]},
   {"type": "detail", "alt": True, "eyebrow": "Built for enterprise", "heading": "More total users, areas and zones than any other panel in its class",
    "body": "For enterprise environments with large and growing user populations, the XR650 gives systems room to grow over time without redesign. It supports multisite operations and adds bank-grade cybersecurity built for modern IT networks.",
    "bullets": ["Simplified installation and management", "Works with the DMP ecosystem", "Suited to financial institutions, government facilities and more"], "flip": True},
   {"type": "proof", "eyebrow": "On the award", "value": "The XR650 was built for organizations operating at the highest level, where scale, security and growth cannot be compromised.",
    "text": "Enterprise security and cybersecurity expectations are evolving, and the intrusion detection system infrastructure must rise to the occasion.", "source": "Mark Hillenburg, Vice President of Industry Relations"},
   {"type": "resources", "alt": True, "heading": "Where the XR650 is used", "intro": "The panel and the markets named in the announcement.",
    "items": [["Product", "XR650 control panel", "The enterprise control panel that won Best of Show.", "View product", "products/xr650.html"],
              ["Industry", "Financial institutions", "Security for banks and credit unions.", "See the industry", "industries/financial-institutions.html"],
              ["Industry", "Government", "Security for government facilities.", "See the industry", "industries/government.html"]]}]))

NEWS.append(["News, 9 Apr 2026", "DMP launches VUE camera line delivering intelligent video and active deterrence", "Three 5MP VUE cameras with analytics and active deterrence.", "Read the story", "news/vue-camera-line.html"])
PAGES.append(news_page("vue-camera-line", "", "DMP launches VUE camera line delivering intelligent video and active deterrence",
  "Three new 5MP VUE cameras, bullet, turret and dome, add person and vehicle detection, active deterrence lighting, two-way audio and Virtual Keypad integration.",
  hero_news("News, 9 April 2026", "VUE launches with <em>three 5MP cameras</em> and active deterrence",
            "New 5MP cameras advance our video portfolio with advanced analytics, integrated deterrence and commercial-grade performance.", IMG + "vue-cameras-5mp-1200.jpg", "The VUE dome, turret and bullet cameras", {"label": "See video systems", "href": "services/video.html"}),
  [{"type": "detail", "alt": True, "eyebrow": "SPRINGFIELD, Mo.", "heading": "A trio of 5MP cameras for retail, QSR and medium to large commercial installations",
    "body": "The VUE lineup includes bullet, turret and dome form factors. Building on the recent introduction of the VUE Video Doorbell, this release strengthens the VUE portfolio with professional-grade cameras that offer improved performance, expanded capabilities and integration across the DMP ecosystem.",
    "bullets": ["Bullet, turret and dome models", "Available now through authorized DMP dealers"]},
   {"type": "cards", "heading": "Sharper detail, smarter detection and a way to intervene",
    "items": [["5MP on every model", "Sharper detail, and faster, more confident alarm verification."],
              ["Person and vehicle detection", "Advanced analytics identify relevant activity, helping reduce unnecessary footage and improve response accuracy."],
              ["Power and standards", "All models support PoE or 12VDC power, are ONVIF compliant and include built-in microphones."],
              ["Active deterrence", "Bullet and turret models feature integrated deterrence lighting, red and blue or white, along with two-way audio, so users can intervene in real time."],
              ["Virtual Keypad integration", "Users can view video, review events and verify alarms from anywhere."],
              ["Better than the last generation", "Compared to our previous generation: improved performance, sharper image quality and more capable analytics."]], "alt": True},
   {"type": "proof", "eyebrow": "On the launch", "value": "The launch of VUE Cameras marks a significant advancement for our video lineup.",
    "text": "Compared to our previous generation, these cameras deliver improved performance, sharper image quality and more capable analytics, helping dealers provide faster, more reliable and more proactive security.", "source": "Ken Francis, Executive Vice President of Video Solutions"},
   {"type": "resources", "heading": "The three VUE cameras", "intro": "Each form factor has its own product page.",
    "items": [["Bullet", "VUE Bullet camera", "5MP, with deterrence lighting and two-way audio.", "View product", "services/video.html"],
              ["Turret", "VUE Turret camera", "5MP, with deterrence lighting and two-way audio.", "View product", "services/video.html"],
              ["Dome", "VUE Dome camera", "5MP with person and vehicle detection.", "View product", "services/video.html"]]}]))

NEWS.append(["News, 19 Mar 2026", "Integration with System Surveyor streamlines intrusion and access control system design for dealers", "Design DMP systems on digital floor plans with System Surveyor.", "Read the story", "news/system-surveyor.html"])
PAGES.append(news_page("system-surveyor", "", "DMP launches partnership with System Surveyor",
  "Our integration with System Surveyor lets dealers design intrusion, access control, fire and video systems on digital floor plans, with a bill of materials generated automatically.",
  hero_news("News, 19 March 2026", "System Surveyor partnership <em>streamlines system design</em> for dealers",
            "Integration streamlines intrusion and access control system design for dealers.", IMG + "system-surveyor-1200.jpg", "A hand holding a tablet showing a floor plan in System Surveyor", {"label": "About the partner", "href": "partners/system-surveyor.html"}),
  [{"type": "detail", "alt": True, "eyebrow": "Springfield, Mo.", "heading": "Dealers get a mobile, collaborative system design platform",
    "body": "We announced a partnership with System Surveyor, a digital system design platform for security and technology integrators. The collaboration gives DMP dealers advanced tools to simplify system planning, automate documentation and accelerate the sales process.",
    "bullets": ["DMP system components are built into the platform", "Dealers design intrusion, access control, fire and video systems directly on digital floor plans"]},
   {"type": "cards", "heading": "From site survey to proposal in up to 50% less design time",
    "items": [["Design on digital floor plans", "Place DMP intrusion, access control, fire and video components directly on the plan."],
              ["Documentation generated for you", "A bill of materials and project documentation and requirements are created automatically."],
              ["Proposals produced swiftly", "Dealers move with greater efficiency from site survey to system proposal, reducing system design time up to 50%."]]},
   {"type": "proof", "alt": True, "eyebrow": "From DMP", "value": "In partnering with System Surveyor, our dealers gain an improved way of designing DMP systems and communicating with their teams, customers and project stakeholders.",
    "text": "At DMP, we are always looking for ways to help our dealers optimize productivity and acquire more business.", "source": "Mark Hillenburg, Vice President of Industry Relations"},
   {"type": "proof", "eyebrow": "From System Surveyor", "value": "Working with DMP allows dealers to design intrusion and access control deployments with greater clarity.",
    "text": "System Surveyor is focused on helping integrators simplify system design and collaborate more effectively. The partnership helps generate accurate documentation and accelerate the entire proposal process.", "source": "Chris Hugman, co-founder and CEO of System Surveyor"},
   {"type": "resources", "alt": True, "heading": "Design tools and the partnership", "intro": "Where to go next.",
    "items": [["Partner", "System Surveyor", "Our partner page for the design platform.", "See the partner", "partners/system-surveyor.html"],
              ["Dealer support", "Design tools", "The tools we offer dealers for system design.", "See design tools", "support/design-tools.html"],
              ["System", "Access control", "Access control systems you can design on a floor plan.", "See access control", "services/access-control.html"]]}]))

NEWS.append(["Case study, 30 Oct 2026", "Customer Success Story: A Small Sensor. A Big Save.", "A water heater burst a week after a 1112 sensor went in beneath it.", "Read the story", "news/small-sensor-big-save.html"])
PAGES.append(news_page("small-sensor-big-save", "", "Customer success story: a small sensor, a big save",
  "A 1112 Wireless Water and Temperature Detector under a water heater, wired to an XT75, raised the alarm a week later when the heater burst.",
  hero_news("Case study, 30 October 2026", "A small sensor. A big <em>save.</em>",
            "Charles Pilchard of Washington Alarm installed a 1112 under his own water heater. A week later, it burst while he was out of town.", IMG + "sensor-1112-1200.jpg", "Two white 1112 wireless water and temperature detectors beside a small puddle on a wood floor",
            {"label": "Buy the 1112 at buy.DMP.com", "href": BUY}),
  [{"type": "detail", "alt": True, "eyebrow": "The install", "heading": "A 1112 beneath the water heater, connected to an XT75",
    "body": "Charles Pilchard, project manager at Washington Alarm, experienced the value of proactive water detection firsthand after installing a DMP 1112 Wireless Water and Temperature Detector beneath his home's water heater and connecting it to an XT75 control panel.",
    "bullets": ["Sensor: 1112 Wireless Water and Temperature Detector", "Panel: XT75", "Place: beneath the home's water heater"]},
   {"type": "cards", "heading": "One week later, the heater burst and the alarm sounded",
    "items": [["The alarm", "While Charles was out of town, the water heater burst, triggering an alarm and prompting a call from his central monitoring station."],
              ["The early warning", "It alerted him to the issue while he was away, helping minimize potential water damage and saving valuable time and costly repairs."],
              ["What changed", "A simple installation became a powerful personal success story, giving Charles greater confidence in recommending and installing 1100 Series Wireless Environmental Sensors to customers before disaster strikes."]]},
   {"type": "proof", "alt": True, "eyebrow": "The result", "value": "The early warning helped minimize potential water damage, saving valuable time and costly repairs.",
    "text": "Catch leaks and temperature changes early with the 1112 Wireless Water and Temperature Detector.", "source": "Customer success story, October 2026"},
   {"type": "resources", "heading": "The products in this story", "intro": "Dealers order the 1112 at buy.DMP.com.",
    "items": [["Sensor", "1112 Wireless Water and Temperature Detector", "Features and specifications.", "View product", "services/wireless.html"],
              ["Panel", "XT75", "The control panel the sensor was connected to.", "View product", "products/xt75.html"],
              ["System", "Wireless", "The 1100 Series Wireless environmental sensors.", "See wireless", "services/wireless.html"]]}]))

NEWS.append(["News, 29 Oct 2025", "DMP introduces VAULT: secure, encrypted connectivity for cloud-based security applications", "Cloud access for Virtual Keypad and Dealer Admin, with systems kept off the public internet.", "Read the story", "news/vault.html"])
PAGES.append(news_page("vault", "", "DMP introduces VAULT: secure, encrypted connectivity for cloud-based security applications",
  "VAULT, Virtual Access Using Layered Tunneling, lets dealers and enterprises use Virtual Keypad and Dealer Admin while keeping security systems off the public internet.",
  hero_news("News, 29 October 2025", "VAULT: <em>encrypted connectivity</em>, no public internet exposure",
            "Secure access to cloud applications without exposing systems to the public internet.", IMG + "vault-1200.jpg", "The VAULT secure connectivity appliance graphic", {"label": "Our certifications", "href": "about/certifications.html"}),
  [{"type": "detail", "alt": True, "eyebrow": "Springfield, Mo.", "heading": "A private, encrypted tunnel to SecureCom Wireless infrastructure",
    "body": "Virtual Access Using Layered Tunneling (VAULT) is a secure communication platform that allows dealers and enterprise customers to use our cloud applications while keeping their security systems off the public internet. Organizations can use Virtual Keypad and Dealer Admin without exposing systems directly. VAULT creates a private, encrypted tunnel between a customer's corporate network and the SecureCom Wireless infrastructure, so systems reach our cloud services through a controlled and isolated connection.",
    "bullets": ["Made for banks, financial institutions, government agencies and other organizations handling sensitive information", "Keeps strict network boundaries in place"]},
   {"type": "cards", "heading": "Six things VAULT does for an enterprise security network",
    "items": [["Encrypted panel communication", "Intrusion panels maintain encrypted communication with SecureCom servers."],
              ["Isolated from the public internet", "Security systems remain isolated from the public internet."],
              ["Central management", "Centralized management through Virtual Keypad."],
              ["Unlimited business panels", "Unlimited business panels managed through Dealer Admin."],
              ["Replay and tamper protection", "Integrity checks and sequence numbering detect and block replay attacks or tampered packets in real time."],
              ["Cut the tunnel at once", "If a threat, breach or policy violation is detected, administrators can immediately terminate the VPN tunnel, isolating affected systems and preventing further access."]], "alt": True},
   {"type": "detail", "eyebrow": "How it works", "heading": "A point-to-point VPN built on AES, SHA and IKEv2",
    "body": "VAULT operates as a point-to-point Virtual Private Network that secures IP communications using government-grade authentication and encryption. It supports established standards including the Advanced Encryption Standard (AES) and Secure Hash Algorithm (SHA), while Internet Key Exchange (IKEv2) authenticates both endpoints and establishes the encrypted tunnel.",
    "bullets": ["We provide a preconfigured VAULT appliance that streamlines deployment and integration", "A VAULT spec sheet is available from DMP"], "flip": True},
   {"type": "proof", "alt": True, "eyebrow": "Why we built it", "value": "Our enterprise customers asked us for the highest grade of security for their businesses.",
    "text": "VAULT gives them the ability to use powerful cloud applications while keeping their systems isolated from the public internet.", "source": "Brad Tucker, Vice President of Product Management and Support"},
   {"type": "resources", "heading": "Related products and markets", "intro": "Where VAULT is used.",
    "items": [["Product", "VAULT", "The secure connectivity platform and appliance.", "View product", "services/communicators.html"],
              ["Software", "Virtual Keypad and mobile", "Centralized management through Virtual Keypad.", "See mobile and automation", "services/mobile-automation.html"],
              ["Industry", "Financial institutions", "Banks and credit unions that keep strict network boundaries.", "See the industry", "industries/financial-institutions.html"],
              ["Industry", "Government", "Government agencies handling sensitive information.", "See the industry", "industries/government.html"]]}]))

TO_CONFIRM = [
    "Legal text (privacy-policy.html, terms-of-use.html) is reproduced from the current pages, last updated January 2021, and must be reviewed and approved by DMP counsel before it goes live. It still names www.dmp.com, Google+ and Twitter, and refers to 'this website'; counsel should confirm the wording for the new site.",
    "The legal pages hold several paragraphs per section, separated by blank lines inside each detail 'body'. The renderer must keep paragraph breaks (for example white-space: pre-line) or the paragraphs will run together. Both pages also exceed 9 sections because every legal heading is kept.",
    "Careers: open positions live in a separate careers portal (a third-party HR site). No link is shown because only internal links are allowed; DMP should provide the portal address for the new site. No job listings were invented.",
    "Careers quote is unattributed on the source page; confirm who it may be credited to (currently 'A DMP team member').",
    "DMP Cares: the source page links to about 30 charities and organizations, but their names are not in the text. The preview names none. DMP should supply the list of supported causes and approve linking to them.",
    "DMP Cares: the volunteer-hours instruction (50,000 hours, 2025 BHAG, logged under HR Actions in the HR system) comes from an internal employee kiosk page. Confirm it is meant to be public and whether the 2025 goal is still current. /dmp-cares-4u returned no content and was not used.",
    "Certifications: the SOC 3 report is a PDF download on the current page and cannot be linked in the preview. DMP should supply the file. Other listings stated (JamAlert UL 2610, 1997 UL Listed combination panel, FirstNet-approved communicators) come from the news, About and DualSIM pages; confirm each is current.",
    "Events: dates are shown only where the source gives them. The Technician Bootcamps (December, January, February, March), the Advanced Technician Bootcamp (March) and the Detroit Tech Training Tour (January) list a month and no day or year. The Advanced Technician Bootcamp page still carries an old August 17 to 20 agenda, so only its topics are used. Owners Forum 2027 gives a register-by date (March 15, 2027) but no event date.",
    "Events: registration forms (with attendee type, sponsorship level and payment) and hotel booking links live on the source event pages. The new site needs its own registration path; the page currently sends visitors to the Contact DMP form.",
    "Events: the two dealer quotes (events page and Dealer Roundtable pages) are unattributed on the source pages; confirm credit lines. Speaker names for the Roundtables were left out.",
    "International: the source gives Inside Sales as +1-866-266-2826, which elsewhere is Customer Service (Inside Sales is 877-757-4367). Confirm the number.",
    "International: the team list shows four people (Mark, Shaun, Diego, Doug) with only Mark NeSmith and Doug Dacre named in full and phone numbers that are not clearly tied to a person. Only those two are shown, with the numbers as listed; confirm numbers, and supply surnames and roles for Shaun and Diego if they should appear.",
    "International: the page lists 'Latin America & Caribbean' ISTC and two Mexico distributors; the DMP contact column names Mark NeSmith for all except ADI EU (Doug Dacre). Confirm. Distributor websites are as shown on the source page and are external links.",
    "International: individual international products are listed as text because their product pages (slugs such as xr550int) belong to another family; link them once those pages exist.",
    "International: the Harmonized Tariff Schedule page reads as an internal reference (it mentions the CMS system and long classification discussions). The page uses a short summary and five example codes. Confirm DMP wants these public and that they are current for customs use.",
    "News dates are taken from the publication metadata on each article. VK VMS: 'available 9/29' has no year on the source; shown as September 29. The article's GSX booth and dates (#3205, September 14 to 16) are past and may be dropped.",
    "News: related product links use best-guess slugs (vplus-7081-bdv, xv-plus-gateways-with-alarmvision, vue-bullet, vue-turret, vue-dome, xr650, jamalert, vault, 1112, xt75); a VK VMS product page was not found, so none is linked. The VUE camera line article calls its cameras 'a trio of 5MP cameras'; the VUE Dome product description mentions no deterrence lighting, which the article reserves for bullet and turret models.",
    "News: documents (VAULT spec sheet, VUE Plus sales sheet and spec sheets, the customer success story download) are named as plain text; PDFs need hosting before they can be linked.",
    "News: Ken Francis is titled Executive Vice President of Video Solutions in two releases and Vice President of Video Solutions in the ESX release; titles are reproduced as each article gives them.",
    "Images: the ESX story uses a photo from the source page that shows people; confirm photo permission. The VUE camera line image is the launch email header; confirm it is usable without its 'See More. Know More. Do More.' text.",
]
