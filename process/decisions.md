# Decision rules

The judgement calls in the runbook, written as rules with a worked example — so they can be handed
over. **A rule you can delegate is worth more than a judgement you can exercise.**

Fifteen of the 37 runbook steps are 🏢 QBS, and most of that is judgement living in one head. At any
real volume, that is the ceiling. The selection rules in `themes/catalogue.md`, the card-grid table
and the contrast floors are already written as rules and are genuinely delegable; these are the ones
that weren't.

Each rule: **the question · the rule · the test · a worked example · when to escalate.**

---

## Is the wildcard good, or is it padding?

**Rule:** A wildcard is a direction we would ship if they chose it. If we would talk them out of it,
it isn't a wildcard — it's a decoy, and prospects can feel a decoy.

**Test:** run `verify.mjs` on the wildcard mockup exactly as hard as on the safe one. Then ask:
*"If they pick this, do I have a client I'm proud of, or a problem?"* Anything but the first answer
means swap it.

**Example:** Dealer, light ground. Safe = Clean, stretch = Showcase. Wildcard = Press — a serif in
a category that is entirely sans. **Good wildcard**, because Revolution's client kept Fraunces in
the set and it would ship fine. Wildcard = Void (dark) — **padding**, because the brief said light
and we would never ship it. Rule 1 of theme selection already forbids it; this rule catches the ones
rule 1 doesn't.

**Escalate:** never. This one is fully delegable.

## Fix the theme at source, or live with it?

**Rule:** Fix at source when the defect will hit the **next** client too. Live with it when it is
specific to this client's content.

**Test:** *"Would this be wrong on a different client's site using the same theme?"* Yes → source.
No → per-client, in the clone.

**Example:** Light-theme button contrast at 3.5:1 → **source**, every light client hits it. A
client's logo that clips in the header at 390px → **clone**, it's their logo. Header hardcoding
QBS's nav → **source**, and it already has a ticket.

**Escalate:** a source fix is a write to the nine, so it always goes through the named approver from
step 6. The *decision* is delegable; the *write* is not.

## Does this build need Phase 4 at all?

**Rule:** Phase 4 is needed when the section list from step 16 asks for something the 57 modules
(plus the vertical kit) don't have. Not before, and not because the client "wants something
custom".

**Test:** map every section in step 16 to a module name. Any section with no module → Phase 4, and
a change order if the tier didn't include it.

**Example:** Dealer wants a cost-per-page calculator → `cost-calculator` exists in Revolution's kit →
**port, not Phase 4**. Dealer wants a fleet map with live device status → nothing exists → **Phase
4, and a change order**.

**Escalate:** when Phase 4 would exceed ~40 hours. Above that it's a custom build, priced as one.

## Could this copy belong to any company in the category?

**Rule:** Copy is done when it contains at least three things a competitor **could not truthfully
say**.

**Test:** highlight every claim on the page. Strike the ones any dealer could make ("responsive
service", "trusted partner", "cutting-edge technology"). If fewer than three survive above the fold,
it's generic.

**Example:** *"78 years in Winston-Salem"* survives — nobody else can say it. *"Same-day service
across four NC locations"* survives. *"We put customers first"* does not. Kelly's real homepage has
the first two; a generic draft would have only the third.

**Escalate:** never. But **every surviving number goes through step 19** before it ships.

## Is this a change order?

**Rule:** Anything that changes the page count, adds a module that doesn't exist, adds a location,
adds a language, or changes the platform is a change order. Everything else is revisions within
scope, capped at two rounds per page.

**Test:** *"Does this change what we're building, or how it looks?"* What → change order. How →
revision.

**Example:** "Can the hero be blue instead of green?" → revision. "Can we add pages for our three new
branches?" → change order, and it also trips the multi-location gap. "Can the calculator email me
the result?" → change order (new module behaviour).

**Escalate:** the price. The *classification* is delegable; the *number* is the approver's.

## Which direction gets the Higgsfield render?

**Rule:** One direction, and it's the one we'd recommend if asked — before the pitch. After the
pitch, the one they chose, if different.

**Test:** *"If the client said 'you pick', which would I pick?"* That one.

**Example:** Three dealer directions; we'd recommend Clean. Render Clean's hero, use the theme's own
hero treatment for the other two. If they pick Showcase, render Showcase after the call. Never three
renders before a choice — two get discarded.

**Escalate:** never. Credits are the only cost, and the rule already minimises them.

## Should we walk away?

**Rule:** Walk when any of these is true at step 4–6: the platform cannot hold the build and they
won't upgrade · they have no traffic and no budget for content and expect traffic · they want a
copy of a competitor's site · they refuse named approvers · the number they want us to publish can't
be sourced.

**Test:** count them. One is a conversation. Two is a walk.

**Example:** Dealer on free HubSpot, wants 40 pages, won't upgrade, wants it in 30 days. That's two
(platform, and a schedule the process can't honour). Walk, or re-scope to 8 pages on Launch.

**Escalate:** always — walking is a 🏢 decision. But the *recommendation* is delegable, and it should
arrive with the count.

## When is the gate "clean enough"?

**Rule:** `verify.mjs` exit 0 **and** score ≥ 80 **and** a human has scrolled every page on a real
phone. All three. A score of 79 does not ship because it's close.

**Test:** the three are binary. If any is no, it's not done.

**Example:** Exit 0, score 84, nobody has opened it on a phone → **not done**. Exit 0, score 78,
phone-reviewed → **not done**; find the 2 points.

**Escalate:** never. This is the rule that protects everyone else's judgement.
