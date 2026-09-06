# The QA process

**Internal.** How we produce the evidence behind `process/quality-standard.md`, in what order, by
whom, and what happens when something fails. The standard is what the client is promised; this is
how the promise is kept.

Version 1.0, 2026-09-06. Owner: Shawn Peterson.

---

## The rule

**Nothing reaches a client without evidence that a check ran.** Not "we looked", not "it should be
fine". A report file, a screenshot, a score. If a check cannot run (a draft page that cannot be
rendered anonymously, a form with no recipient yet), the page is not done, whatever the ticket says.

## Four stations, in order

Each station has an owner, a tool, an output, and a station to send failures back to. A failure
never goes back to step 1; it goes to the station that caused it.

### Station A: the automated gate (AI, every page, every time)

```bash
node scripts/verify.mjs <staging-url> --env staging --expect-org "<Client legal name>" --out verify-out
```

Runs at 390, 768 and 1440. Produces `verify-out/report.json`, three screenshots per page, a
`SCORE n/100` line and a row in `verify-out/scores.jsonl`. **Exit 1 or a score under 80 means the
page is not done.**

| Standard item | Checks that prove it |
|---|---|
| 1 Yours, not ours | `no QBS branding left`, `Organization names the client`, `Organization entity`, `Organization sameAs` |
| 2 Phone first | `no horizontal scroll (mobile)`, `body text >= 13px`, `inputs >= 16px`, `tap targets >= 24px`, `tap targets >= 44px`, `tap targets not crowded`, `sticky chrome <= 25%`, `nav reachable on touch`, `hero type sized for a phone`, `viewport meta` |
| 3 Readable by everyone | axe-core at three widths (`a11y@…`), `exactly one h1`, `heading order`, `images have alt` |
| 4 Fast | `images lazy below fold`, `images have width/height`, `hero fetchpriority`, `font preconnect`, `responsive images`, `CLS (mobile)`, `LCP (mobile)` |
| 5 Found | `canonical`, `meta description`, `og:title`, `og:image`, `twitter:card`, `JSON-LD parses`, `structured data present`, `noindex check` (staging must have it, production must not) |
| 6 Converts | `hard conversion path (in main)`, `soft conversion path`, `on-page form (in main)`, `no broken internal links` |
| 7 Written like a person | `no placeholder text`, `no em dashes in copy` |
| 8 Balanced and finished | card-grid balance at every width (`grid: …`), the page score |

Failures route: contrast to the re-skin (RUNBOOK 22/23); placeholder or em dash to copy (18);
card orphan to layout (16); QBS branding to the de-brand (24); noindex to the staging publish (30).

### Station B: the agents that read what a script cannot (AI, reviewed by QBS)

Five agents from `process/agents.md`, run against the staging URL and the brief, each returning a
list of findings with a location and a proposed fix. Nothing ships with an open finding marked
correctness.

| Agent | Reads for | Standard item |
|---|---|---|
| Copy critic | Generic claims (the "could a competitor say this" test), filler, em dashes, stacked adjectives, promise drift from the brief | 7 |
| Fact checker | Every number, date, name and claim against the brief's proof points and the client's sources. Anything unsourced is flagged, not softened | 7 |
| AEO/SEO reviewer | Schema types against page types, entity facts, sameAs, title and description quality, internal linking, redirect map coverage | 5 |
| Mobile reviewer | Reads the 390 screenshots as a phone user: what is hidden, what is cramped, what is above the fold | 2 |
| Adversarial verifier | Tries to make every other reviewer wrong. Reruns the gate, opens the page cold, follows every CTA | all |

Output: one findings file per page under `verify-out/agents/`, and the critic score per page written
to `data/pages.jsonl` at step 37.

### Station C: a person looks (QBS, every page, on a phone)

The step that gets skipped, so it is a station with a checklist:

- [ ] Open every page on a real phone, not a simulator. Scroll the whole thing.
- [ ] Read the hero out loud. If it sounds like a website, rewrite it.
- [ ] Tap every CTA. Submit the form. Confirm the named recipient received it, and write down who
      and when (this is the form test record).
- [ ] Look at every card grid for an orphan.
- [ ] Look at every image and ask whether it is honest.
- [ ] Open the page in a private window and search the source for "Quantum".
- [ ] Sign the gate: name and date in the ClientCommand page record.

### Station D: the launch checks (QBS, once, at go-live)

- [ ] 301s in place and tested for every URL in the brief's migration map. Record the status codes.
- [ ] Rich Results Test and schema.org validator on home, one blog post, one case study, one
      interior page, the pricing or services page. Save the results.
- [ ] `noindex` removed; production run of the gate passes with `--env production`.
- [ ] GA4, Search Console and HubSpot tracking confirmed firing on the live domain.
- [ ] Sitemap submitted. Old sitemap URLs redirecting.
- [ ] The recorded walkthrough delivered.
- [ ] The evidence bundle assembled and sent (table in `quality-standard.md`).

## The evidence bundle

One folder per client per launch, delivered through ClientCommand:

```
<client>/launch-<date>/
  report.json            gate results, every page
  scores.jsonl           the score line per page
  screenshots/           390 / 768 / 1440 per page
  agents/                findings per page, with resolution
  redirects.csv          old, new, tested status
  schema-validation/     Rich Results + validator captures
  form-test.md           recipient, timestamp, screenshot
  baseline.md            the Semrush baseline from day one
  walkthrough.mp4        editing the site
```

## Who signs what

| Station | Runs it | Signs it |
|---|---|---|
| A Gate | AI | The build owner, by reading the score line |
| B Agents | AI | The build owner, by closing every correctness finding |
| C Person | QBS build owner | Named, dated, in ClientCommand |
| D Launch | QBS build owner | Shawn Peterson, or whoever holds go-live approval (RUNBOOK 35) |

## When it fails after launch

The standard promises a free fix for 30 days on anything in it. The process for that:

1. The report comes in (client, monitor, or our own 30-day read).
2. Rerun Station A on the page. The report is the diagnosis.
3. Fix at the station that caused it. Rerun. Send the new report to the client with the fix.
4. Write the cause into `process/qa-findings.md` if it is one the process should have caught.

## What changes when the standard changes

The standard and this process carry the same version. A check added to `verify.mjs` that the
client would care about gets a line in the standard; a line in the standard that has no check gets
one written, or the line comes out. Reviewed on the RUNBOOK's monthly cadence.
