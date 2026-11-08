# Build lessons: a HubSpot site build, start to finish

What the Van Ausdall & Farrar (VAF) build taught us, written as rules for the next build. Each rule
says what happened, so you can judge whether it applies. Read with `process/RUNBOOK.md` (the order of
work) and `process/OPERATOR.md` (the exact commands and traps).

## Week 1: settle these before any build work

1. **Test access with a real write.** VAF's token could not create a contact property, and the token
   was not in the build environment, so the theme publish waited on another session. List the scopes
   (CMS pages and source code, Files, blog, forms, URL redirects, contacts schema), put the token in
   the environment, and run one test write of each kind. Always call a client's HubSpot through
   ClientCommand with the global fallback turned off: one write landed in Quantum's own portal
   because the client token lacked a scope (removed within a minute, but avoidable).
2. **Decide how customers are named, and get permission.** VAF decided late to describe case study
   customers instead of naming them, which meant rewriting 18 pages, their titles, markup, logos
   and addresses. Settle named versus described at kickoff.
3. **Start the claims register on day one.** Surprises came after the build: "SOC 2 certified"
   wording, an unsourced "largest" superlative, an out-of-date NPS (93.4 against the audited 92.8)
   and an office with no public address. Collect every office's address, hours and phone early,
   because the local business markup needs them.
4. **Get DNS, host and Search Console access in week 1.** At VAF these still block the launch gates.
5. **Set the launch date at kickoff** and give every client dependency an owner and a date. VAF's plan
   carried 29 overdue tasks because the launch gates held placeholder dates. Count weeks from the
   real kickoff, not from the first design conversation, and re-baseline weekly.

## Build rules that worked

- **Structured data.** Organization on the home and about pages only. LocalBusiness on home, about,
  contact and the office pages. Every other reference to the company carries its name, because Google
  does not follow an ID to another page. Use `sameAs` to separate the company from similarly named
  firms. Run `scripts/vaf_schema_check.py` (or the client's equivalent) after every publish.
- **One form per purpose, with a hidden source field.** Create the contact property first, as a
  text property: HubSpot does not keep a default value on a hidden dropdown. Lead source is then
  known on every submission.
- **Quality gates weekly, not once at the end.** Page scorecard on desktop and phone, accessibility
  scan, link and image crawl, schema check, blog sweep. Expect one momentary CDN error per full run;
  re-test that page alone.
- **Redirect map early, cleaned and checked.** VAF's first map had 25 bad rows out of 228
  (self-redirects and conflicting duplicates). Check every target loads on staging and publish the
  map as a client page for approval.
- **Blog.** Make the import safe to repeat (VAF ended up with 58 accidental duplicates). HubSpot
  collapses double hyphens in slugs, so those posts need redirects. Never link a page to a
  future-dated post: VAF's pillar cards returned 404 until the posts were published. Plan the TL;DR
  and FAQ for every post from the start; the client wanted every post and the first pass skipped
  98. A batch writer with a validator plus an idempotent apply script worked well.
- **Blog listing template** is a HubSpot setting (Settings, Website, Blog, Templates) and the API
  ignores it. Give it an owner and check by loading `/blog`.

## Editing and handover: build it in, do not tack it on

- **Self-service editing is a feature.** VAF's modules had no picker groups and almost no help text
  until the last week, and its page templates were generated one per page and not available for new
  pages. Group the modules, give every image, link and toggle help text, hide the global modules,
  and ship a generic "drag and drop page" template from the first publish. Body copy should be rich
  text. Set the expectation that custom module fields edit in the left panel, not on the page.
- **Write the editing guide and test it with the client's real editor** before training. Five jobs:
  change a headline, swap an image, add a section, move a section, clone a page.
- **Keep the hero simple.** VAF's hero has 30-plus fields because it switches between three layouts;
  it is the module most likely to confuse an editor.

## Client process

- **Sign-off sheet.** Build the page rows from HubSpot, add change requests as rows, and keep
  customer names out of it. `update_signoff_sheet` replaces any rows and notes you do not pass, and
  posted notes cannot be resolved without their IDs. Use `add_signoff_rows` for increments and back
  up the rows before any replace. We lost and restored rows once.
- **Track pages on the sheet, not in the plan.** Wave-level plan tasks stay readable in meetings.
- **A weekly report page from kickoff:** results, change log, what we need from the client, what is
  coming up, and links to everything. It worked as the meeting agenda.
- **Feedback with an AI assistant.** Give the client a short "how to give us feedback" guide and link
  it from the report.
- **Before-and-after SEO page.** Publish a scorecard against the baseline analysis as soon as the
  first wave is staged (needs the old-to-new URL map).
- **Link new tickets to the plan as soon as they sync.** ClientCommand's HubSpot sync can lag; check
  that a new ticket has arrived before linking it, and do not run the all-clients link sweep.

## Mistakes to avoid

- Creating a property or record without checking which portal the call will hit.
- Passing partial rows to a replace-style update.
- Describing "drag and drop" to a client before testing it with someone who is not us.
- Leaving launch gates on placeholder dates.
