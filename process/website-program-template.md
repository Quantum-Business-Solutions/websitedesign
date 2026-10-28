# Website program template: one build project, then separate 24 month programs

Set up in ClientCommand on the VAF engagement (Oct 2026). Reuse for every site build so the plan, the tickets and the post-launch retainer exist before launch, not after.

## Projects (one ClientCommand plan each, never one giant plan)
1. **Website Build and Launch**: phases 1 Build and publish, 2 Blog and content, 3 SEO and AEO, 4 Forms and conversion, 5 QA and sign-off, 6 Launch. About 21 tasks, each with a due date, `owner_party` (qbs, client or both), and `client_action` where the client must decide or approve.
2. **SEO and AEO Program (24 months)**: baseline rankings and Search Console, technical fix list, AEO baseline on 20 buyer questions, monthly report. One phase per quarter.
3. **Content Program (24 months)**: 24 month calendar, two posts and one page refresh a month, TL;DR and FAQ rollout, VAF review batches.
4. **Local Search, Reviews and Conversion (24 months)**: Google Business Profile, review requests, conversion baselines and tests.

Create month 1 tasks in detail, later quarters as one task per quarter, then add month tasks at the start of each month. A 24 month wall of tickets nobody reads is worse than a rolling quarter.

## Launch blockers that must be tasks, not memory
- Remove staging `noindex` from every page and every blog post.
- DNS and 301 map live on the same day.
- Claims register approved by the client (every figure, tier, certification).
- Sign-off sheet refreshed with every live page and its type.
- Rotate the temporary build token.

## ClientCommand gotchas
- `push_plan_to_hubspot_tickets` returned "no eligible tasks" for all four new plans. Do not work around it by calling `create_ticket` per task: that creates local tickets with no HubSpot sync and no plan link. Find out why a plan is ineligible first (the master plan's tickets synced from HubSpot and were linked).
- `create_plan` after a portal's first plan always makes a project, and gives it a default "Phase 1" you should rename with `update_phase`.
- `call_hubspot_as_client` with `allow_global_fallback:false` uses the client's stored token, so reads and writes work even when no token is in the shell. Large list calls return full bodies; use `limit=1` to get counts from `total`.

## Blog TL;DR and FAQ pipeline
1. Audit: count FAQ, TL;DR, question headings in the migrated posts (VAF: 335 posts, 1 FAQ mention, 3 TL;DRs, 42 with question headings, 0 FAQ markup).
2. A sub-agent drafts `brands/<slug>.blog-enrich.json`: three bullet TL;DR and 3 to 5 FAQs per post, grounded only in that post, with a validator for word counts, dashes and duplicates. Thin posts are skipped, not padded.
3. The client reviews. Then a script inserts the TL;DR box and FAQ into the post body and generates the FAQPage JSON-LD from the same text, never hand-written.
4. Order: question-heading posts first, then top traffic, then newest.

## Schema position (do not oversell)
FAQ rich results retired in 2026, and structured data does not drive AI answers. The visible TL;DR and FAQ text does the work; markup only has to agree with it. Organization and LocalBusiness belong on the home or about page, not every page; BreadcrumbList site-wide; BlogPosting on posts; Service on service pages.

## Verify live, not from state files
`brands/<slug>.blog-import.state.json` listed 311 posts while HubSpot had 343 published, and its URLs used a stale blog prefix. Always diff the live blog (`total` from the API) against the source JSON and load a sample of posts in Playwright.
