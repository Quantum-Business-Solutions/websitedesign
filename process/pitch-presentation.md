# The pitch: one main page, three options

How website options get shown to a prospect. The shape matters as much as the work, because the shape
is what communicates effort.

## Why this shape

A prospect shown one design evaluates *you*. A prospect shown three evaluates *the designs* — and
the question silently changes from "should we hire them" to "which one do we like." That is a much
better question to be answered in the room.

The main page in front of the three options does something the options can't: it proves the work
started before the meeting. A prospect who sees their own colours, their own competitors named, and
their own promise written back at them concludes we already put real effort in — because we did.

Three is the number. Two reads as a coin flip; four or more and nobody chooses.

## The structure

**One main page, then three option pages.** Four artifacts, one URL each, or one artifact with four
views — either is fine, but the main page always comes first and is always shown first.

### The main page

Not a design. The evidence and the reasoning, in this order:

1. **The read.** One line: *"Reading this as: <page kind> for <audience>, with a <register>
   language."* From `/website` step 1. This is the sentence that tells them we understood the brief.
2. **What we found.** Their measured tokens — real hexes off their live site, not swatches we
   invented — and the two or three competitors we ingested, with one line each on what the category
   looks like. Firecrawl `branding` output, so every value is defensible.
3. **The promise.** Their answer to interview question 4, written back to them verbatim. If it looks
   different in their own words than it sounded in the call, that's a useful thing to surface here.
4. **The constraints we're honouring.** Pulled from `brands/<slug>.md`. Naming a client's stated
   constraint back to them — *"you said no heavy black backgrounds, so all three directions are
   light"* — is the single highest-trust move on the page.
5. **Why these three.** One line per direction on why it's in the set. Then the three options.

### The three options

One per direction, from the selection rules in `themes/catalogue.md`: **safe / stretch / wildcard**,
ground filtered by the brief.

Each option page carries:

- The theme name and what it reads as
- Real palette swatches at the re-skinned values, from the themes' live tokens
- The type pairing **set in the actual faces**, not named in a caption
- A representative hero block, live
- One line of rationale — why this direction, for them

Label them by character, not by number: *"Signature — the safe one"*, *"Ink — the stretch"*. A
prospect can hold three names; they can't hold three numbers.

## Rules

1. **Never show a direction that trips a guardrail.** Run `process/checklist.md` and
   `/impeccable audit` on all three before the meeting. The wildcard is the one most likely to fail
   contrast — check it hardest.
2. **The wildcard has to be genuinely different, and genuinely good.** A deliberately weak third
   option to make the middle look better is a trick prospects can feel. If you wouldn't ship it,
   it's not an option, it's padding — replace it.
3. **Never show two themes with the same ground and a similar typeface class.** Press and Journal are
   both light serifs; showing both wastes a slot and makes the set look like one idea.
4. **Hero imagery only for the chosen direction.** Higgsfield credits on two discarded heroes is
   waste. Use the theme's existing hero treatment for the other two — they're already good.
5. **Real content, never Lorem.** Their company name, their promise, their sector's language. Lorem
   in a pitch reads as a template, which is exactly the impression the three-option shape exists to
   avoid.
6. **Mobile before the meeting.** Prospects open the link on their phone during the call. Load all
   four at phone width and scroll every one.

## Publishing

The four pages publish as artifacts — private by default, and the prospect gets a link when we
choose. The one live check that matters: open each link cold, on a phone, before sending.

## After they choose

1. Record the choice in `brands/<slug>.md` — **and why**, in their words. The rejected directions
   and the reason are worth as much as the winner.
2. The chosen direction becomes the clone. `process/reskin.md`, then Phase 05 of
   `process/website-design-process.md`.
3. A direction rejected for a reason that generalises past this client → `design/guardrails.md`.

The rejected two cost almost nothing — a mockup each, and no clone, and knowing what the client turned down —
and why — is what makes the next presentation sharper.
