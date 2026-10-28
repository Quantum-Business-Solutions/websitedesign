# Building a custom HubSpot theme page for page (the VAF runbook)

What worked on the 155 page `vanausdall` build (portal 50498425), written so the next one starts at step 3, not step 0.

## Pipeline
1. **Assets** `scripts/vaf_assets.py`: upload logos, photos, video to HubSpot Files; writes `brands/<slug>.asset-map.json`. Every module and mapper resolves URLs through `A()` in `vaf_common.py`.
2. **Modules** `themes/<theme>/modules/*.module`: one per section type. Port in parallel with sub-agents, one agent per 8 to 10 modules, each running `scripts/vaf_check.py` before it reports.
3. **Mappers** `scripts/vaf_map_a..d.py`: each exports `REGISTRY = {section type: (module, mapper)}`. The mapper turns a content.json section into module field values.
4. **Templates** `scripts/vaf_build.py templates all`: one template per page extending `layouts/vaf-base.html`, fields baked in as `module_attribute` defaults. `rhythm()` applies hero layout by page kind, alternating background and flip, and alt text fallback.
5. **Pages** `scripts/vaf_build.py pages all`: first publish uses `/cms/v3/pages/site-pages/schedule`; later updates use `draft/push-live`. Page `name` is `"{Kind} | {Title}"` so the dashboard sorts by type.
6. **Overrides** `brands/<slug>.overrides.*.json`: rewrite a page's sections without touching the scraped content. Used for the 11 suburb pages (duplicate content), the pillar pages, the services dedupe and the home page.

## HubSpot gotchas (all hit for real)
- Forbidden module field ids: body, label, value, name, type, id, default, content. Ids must be unique module-wide, including nested.
- Form fields ignore `module_attribute`: the default form id lives in `fields.json`; render with `{% form form_to_use=... %}`.
- New module fields (`file`-type, `bg_video_webm`, `card_logo`) show on live pages only after HubSpot's module cache refreshes, usually a few minutes. Add a comment revision to `module.html` to nudge it.
- The validate endpoint reports "Unmapped templates cannot contain drag and drop areas" for stock templates too. Known noise, ignore.
- The public API cannot create a blog. Create it in the UI, then `PUT /content/api/v2/blogs/{id}` to set slug and templates (archive any static `/blog` page first or you get PAGE_EXISTS). Per-post `templatePath` is refused; the blog's own setting applies. HubSpot collapses double dashes in slugs, so map redirects from the originals.
- Pages built from a CDN-cached template show stale in screenshots: add a cache-busting query and wait.
- Transient resets happen on long runs: every API call goes through `retrying()`; reruns are idempotent.
- Shell: never `pkill` or `ps | grep | kill` with a pattern that matches your own command line; it kills your shell.

## QA tools (all in `scripts/`)
- `qa_pages.js` Playwright desktop and mobile, with scroll to trigger reveals, overflow and console checks.
- `vaf_seo_audit.py` per page title, description, H1, canonical, og:image, schema, alt coverage.
- `vaf_coverage.py` old site versus new page text coverage, to prove nothing was lost.
- `vaf_page_scorecard.py` the 10/10 gate, combines the three above plus the guardrails.

## Launch gates
Remove staging `noindex` from every page (a tracked blocker in the sign-off sheet), publish redirects from `brands/<slug>.redirects.json`, submit the sitemap, confirm the blog templates are assigned, rotate the temporary token.
