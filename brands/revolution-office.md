# Revolution Office

> **Pre-methodology.** This brief was written before `themes/catalogue.md` existed. Its three
> directions use Sora, Archivo and Fraunces — and only Fraunces is one of the nine (it's Flagship,
> not Press). "Signature" and "Ink" are not theme names. Read it as the argument for brief-first
> working, which it proves well; do **not** copy its naming into a new build. New directions are
> `<Company> — <ThemeName>` using a real theme name.

- **slug:** revolution-office
- **brand_profile_id:** `d8a54316-97b9-48ce-a7e2-482b491763a6`
- **current site:** https://revolutionoffice.com
- **contact:** Tom Menton
- **commercials:** two options discussed — HubSpot Content Starter (~$15/mo hosting) with a
  $7,500–$10,000 build on a 30-day timeline, and a $50,000 full redesign pitch
- **prior build:** `Quantum-Business-Solutions/Revolution`, branch
  `claude/revolutions-github-connection-0lvyx7` (Next.js)
- **why QBS is pitching:** the client is dissatisfied with a competitor agency's Figma concept

## The design read

Reading this as: **managed-print / management-services site** for **business buyers evaluating a
national-scope vendor**, with a **modern, technology-driven but light and approachable** language,
leaning toward **tiled-layout editorial with a warm amber accent on light ground**.

## Client-stated constraints — these outrank house defaults

From meetings 2026-08-27 / 2026-08-30 (Tom Menton ↔ Shawn Peterson):

- **Lighter colour scheme — orange, white, grey.**
- **Avoid heavy black backgrounds.** Stated explicitly.
- **Straightforward, less whimsical font.** Called out twice as a required change.
- **Tiled layout**, matching the referenced Figma site.
- Aesthetic should read **modern, technology-driven, national in scope**.

## ⚠️ Conflict to resolve before showing the client

**Direction 2 "Ink" contradicts a stated constraint.** It is amber on near-black
(`background: #1A1A1A`, `dark: #101010`) — and Tom explicitly asked to *avoid heavy black
backgrounds* and use a lighter scheme.

Under the methodology the brief wins over house taste, so Ink either gets re-grounded onto a light
surface or is dropped from the set shown to him. Presenting it as-is invites the rejection that
already stalled this project once.

This is exactly what a written brief is for — the constraint was captured in a meeting weeks before
the directions were built, and nothing was checking one against the other.

## Competitor benchmarks — client-specified

Tom wants brand perception benchmarked against **Ricoh** and **Canon** managed-print-services
pages. Ingest both via `/design-ingest` before designing: the target is to read as credible in that
category while not looking like either.

## Delivery shape

- **Phased launch** — a functional basic site first, not a complete build up front.
- **Replicable landing pages for association partnerships.** Treat this as a template requirement,
  not a one-off page: it changes how the section system has to be built.

## Brand assets

- **Logo:** https://www.revolutionoffice.com/wp-content/themes/ro_theme/assets/img/logo.png
- **Figma:** client-supplied draft, originally produced by an outside marketing firm. The previous
  engagement stalled on communication/language barriers — so the Figma is a *reference for layout
  and feel* (tiling, font register), not an inherited spec to implement faithfully.
- **Authorized client logos** for a social-proof wall: Armanino LLP, Center Theatre Group,
  Media-Providence Friends School, San Francisco Friends School, The Carey School, Trinity School,
  Union City Apostolic Church.

## Planned structure

About · Management Services · Products & Services (managed print prominent) · Who We Serve ·
Associations · Success Stories / Case Studies · Learning Center · Blog · Contact.

Priority is a **functional basic site launched quickly**, not a complete build up front.

## Directions produced

| Name | Rationale | Status |
|---|---|---|
| Revolution Office — Signature | Direction 1 of 3. Confident and current, closest to the brand today. Amber `#F5A622` on white, Sora headings. | draft — **best fit for the brief** |
| Revolution Office — Ink | Direction 2 of 3. Dark, high-contrast, editorial. Amber on near-black `#1A1A1A`, Archivo. | draft — **conflicts with the brief, see above** |
| Revolution Office — Press | Direction 3 of 3. Warm paper stock `#F7F5F2`, deeper amber `#C87F1B`, Fraunces headings. | draft — light ground fits; check Fraunces against "less whimsical" |

## Guardrails specific to this client

Not for promotion to `design/guardrails.md` — these are Revolution's, not the house's.

- No dark or black-ground designs. Light backgrounds only.
- Type must read plain and businesslike. Fraunces is a display serif with personality — verify it
  against "straightforward, less whimsical" before committing to Press.
- Tiled/card layout is a stated preference, not just an option.

## Build lessons from the prior attempt

Already paid for once — don't rediscover them.

- **Never composite text with `opacity`** — it failed WCAG contrast measurement. Use `color-mix()`.
  Now promoted to the house guardrails.
- **Next.js can serve stale builds** after a rebuild, causing 500s and ChunkLoadErrors. Run
  `pkill -f next-server` before QA.
- **Lovable auto-commits to `main`** — fetch and rebase before pushing local changes.
- Claude's Vercel token returned 403 on deployments; Shawn has to supply URLs or update the
  integration role.
