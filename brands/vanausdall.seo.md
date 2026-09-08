# Van Ausdall & Farrar: SEO Analysis of vanausdall.com

Data: Semrush (US database) and Firecrawl, pulled September 8, 2026.

## Summary

- vanausdall.com ranks for 365 organic keywords and earns about 1,081 organic visits per month, worth $1,015 per month in ad equivalent. About 80 percent of keywords are brand searches and the home page carries 85 percent of traffic.
- The four closest Indiana competitors each earn 1,555 to 2,094 visits per month from 1,058 to 2,711 keywords, roughly 1.5 to 2 times VAF's traffic and 3 to 7 times its keyword footprint.
- "managed it services indianapolis" (1,000 searches per month, KD 29, CPC $20.83) and "it support indianapolis" (880, KD 16, CPC $16.68) are the most valuable local terms. Leap Managed IT is number 1 for both. VAF is not in the top 100 for either.
- VAF's best Indianapolis IT positions are "voip phone systems indianapolis" at number 5 (50 searches) and "copiers indianapolis" at number 12 (70 searches).
- Backlinks are competitive: VAF has Authority Score 21 and 486 referring domains versus Leap at 24 and 471, Taylored at 27 and 959. Missing pages, not authority, are the gap.

## Where the traffic comes from today

The home page produces 85 percent of visits and about 80 percent of ranking keywords are "Van Ausdall" brand variants. Non-brand traffic comes from the regional pages, chiefly /fort-wayne/managed-it-solutions-fort-wayne-in (49 keywords, number 6 for "managed it services fort wayne") and /evansville/managed-it-solutions-evansville-in (number 2 for "managed it evansville").

The Indianapolis footprint is 28 keywords, none above 140 searches per month: "indianapolis network support" number 24 (140), "document management indianapolis" number 26 (140), "printers indianapolis" number 17 (90), "copiers indianapolis" number 12 (70), "voip phone systems indianapolis" number 5 (50).

## Competitors

| Domain | Organic traffic / mo | Keywords | Authority Score |
|---|---|---|---|
| taylored.com | 2,094 | 2,711 | 27 |
| theamegroup.com | 2,007 | 1,839 | not pulled |
| bradenonline.com | 1,807 | 1,595 | not pulled |
| leapmanagedit.com | 1,555 | 1,058 | 24 |
| vanausdall.com | 1,081 | 365 | 21 |

## Keyword opportunities

Volume, KD and CPC from Semrush; competitor positions from the Leap and Taylored gap report.

| Keyword | Volume / mo | KD | VAF today | Competitor |
|---|---|---|---|---|
| business phone systems | 9,900 | 44 | 25 (Fort Wayne page) | none top 100 |
| managed print services | 4,400 | 16 | not ranking | not in gap set |
| copier lease | 2,400 | 19 | not ranking | not in gap set |
| managed it services indianapolis | 1,000 | 29 | not ranking | Leap 1, Taylored 13 |
| it support indianapolis | 880 | 16 | not ranking | Leap 1, Taylored 21 |
| it consulting indianapolis | 590 | 31 | not ranking | Taylored 6, Leap 13 |
| managed it indianapolis | 480 | 31 | not ranking | Leap 3, Taylored 8 |
| cybersecurity indianapolis | 480 | 24 | not ranking | Leap 43 |
| managed print services indianapolis | 170 | 6 | not ranking | not in gap set |
| office phone systems | 2,900 | 37 | not ranking | Taylored 40 |
| healthcare it services | 2,400 | 22 | not ranking | Taylored 17 |

Semrush shows 0 volume for "copier lease indianapolis" and "document scanning services indianapolis", 20 for "copier repair indianapolis", 30 for "business phone systems indianapolis" and 40 for "voip indianapolis". Copier demand arrives through non-geo terms and Google Maps, not typed city modifiers.

## Local search: Indianapolis

Live Firecrawl results, September 8, 2026.

"managed it services indianapolis", top 10: leapmanagedit.com, cloudtango.net, gadellnet.com, mis.tech, meriplex.com, taylored.com, esi.tech, visualedgeit.com, exactitconsulting.com, corsicatech.com. VAF is absent.

"copier lease indianapolis", top 10: visualedgeit.com, werentcopiers.com, copierleaseindianapolis.com, copierleasecenter.com, gflesch.com, bbb.org, iccbusinessproducts.com, copierleaseindianapolis.com/blog, leapcopierprinter.com, then vanausdall.com/copy-print-solutions/ at 10.

Leap's new copier brand (leapcopierprinter.com) already sits above VAF for VAF's core product.

## Technical findings

Live scrape of the home page (65,846 characters of HTML) and sitemap.xml:

- Title "Copier Sales & Managed IT | Van Ausdall & Farrar" is 56 characters; meta description is 135. Both within limits, but "Indianapolis" is missing from the title.
- One H1 ("Indianapolis' Trusted Managed Technology Partner"), seven service H2s, viewport meta, lang="en", canonical set.
- One JSON-LD Organization block. No LocalBusiness, Service or FAQ schema.
- og:image is a stock file (/images/artificial-intelligence.jpg).
- 15 script tags (6 external). No GTM, HubSpot or WordPress fingerprints; custom-built site.
- 73 images, 68 lazy-loaded, all with alt text.
- The string "as5d4f65s4f564we654fw" is a hidden honeypot anti-spam field injected by the form script. Forms work, but there is no CRM integration.
- Sitemap: 586 URLs, no index. 324 (55 percent) are blog posts on the /blog?p=slug-YYMMDD query-string pattern, and 90 are PDFs.

## Backlinks

| Domain | Authority Score | Referring domains | Backlinks |
|---|---|---|---|
| vanausdall.com | 21 | 486 | 2,523 |
| leapmanagedit.com | 24 | 471 | 3,764 |
| taylored.com | 27 | 959 | 3,605 |

VAF has more referring domains than Leap yet Leap outranks it on every local IT term.

## What this means for the build

- Build a dedicated Indianapolis managed IT page: the 28 local IT terms in the gap report total roughly 11,000 searches per month and VAF ranks for none.
- Reuse the Fort Wayne (number 6) and Evansville (number 2) page template for Indianapolis; the format already ranks.
- Add standalone pages for "managed print services" (4,400 per month, KD 16) and "copier lease" (2,400, KD 19); low difficulty, zero VAF visibility.
- Move the 324 /blog?p= posts to clean /blog/slug paths with 301 redirects.
- Add LocalBusiness schema per office and Service schema per offering; only one Organization block exists today.
- Put "Indianapolis" in the home page title and replace the stock og:image; the home page is 85 percent of traffic.
- Replace the honeypot form with a HubSpot form so leads from 1,081 monthly visits are tracked.
- Defend copiers against leapcopierprinter.com, already number 9 for "copier lease indianapolis" while VAF sits at 10.
