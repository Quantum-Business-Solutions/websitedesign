# VAF blog import report

Generated 2026-10-28 20:14 UTC. Portal 50498425.

- Posts found on vanausdall.com/blog: 335 (the live listing; the plan estimated 324)
- Posts retrieved and normalised: 335 (0 unretrievable)
- Posts created in HubSpot: 0
- Failures logged: 0
- Future-dated posts (kept with their original date, so HubSpot schedules them): 4

## Status: posts NOT yet created (blocked on the blog itself)

The CMS API has no endpoint to create a blog. `POST /cms/v3/blogs/posts` fails with `PARENT_BLOG_DOES_NOT_EXIST`, `POST /cms/v3/blogs` is 404, and the legacy `POST /blogs/v3/blogs` fails with `BLOG_HS_SITE_DOMAIN_WRITE_SCOPE_MISSING` whatever domain is sent. The token's scopes (content, cms.domains.read/write, files.*, forms, automation, crm companies read) are not the cause: no public API creates or configures a blog (name, slug, templates, posts per page).

One UI step unblocks everything:
1. Settings > Website > Blog > Create a new blog. Name `VAF Blog`, URL slug `blog`, domain 50498425.hs-sites.com, language English.
2. In that blog's Templates tab: Listing page template = "VAF Blog Listing", Post template = "VAF Blog Post" (both in the "Van Ausdall and Farrar - Showcase" theme, already uploaded). In Settings set posts per page to 12 (the card grid is balanced for any count; 12 gives clean 3-column rows). Date format: month day, year.
3. Run `CLIENT_HUBSPOT_TOKEN=... python3 scripts/vaf_blog_import.py import` (finds the blog by name; idempotent; failures go to `brands/vanausdall.blog-import-failures.jsonl`, rerun with `retry`).

Already done in the portal: author "Van Ausdall & Farrar" and 103 blog tags (11 category tags with the old slugs, e.g. `managed-it`, `news`, plus 92 topic tags). All 174 images are in Files at /vaf/blog (brands/vanausdall.blog-images.json).

## Notes for review
- 335 posts, 195 with a featured image (140 have none on the live site; the templates show a neutral VAF tile).
- Categories are imported as the first tags of each post (HubSpot has no categories); the listing chips link to /blog/tag/<category slug>.
- Post author on the live site is the organisation, so one author "Van Ausdall & Farrar" is used.
- 4 posts are dated November 2026 on the live site (future); they keep their date and are scheduled.
- Body links to other site pages (/contact, /information/..., /print/...) are left as on the live site and may need mapping to the new site's URLs. 33 press-release PDF links point to /pdf/pr/... on the live domain and need those files at go-live.
- 17 posts embed YouTube iframes; kept as-is.
- Every post gets headHtml `<meta name="robots" content="noindex, nofollow">`; remove it at go-live.
