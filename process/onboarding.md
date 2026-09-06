# Onboarding: earning a build

`OPERATOR.md` is the checklist. This is how someone new gets to the point where handing them that
checklist is safe. Three builds, in order, and a permission that unlocks after each one.

The reason it is graduated: the expensive mistakes in this process are all one command long.
`reskin.py --apply` on the wrong portal. A staging publish without `noindex`. A go-live with the
QBS header still in the footer. None of them are hard to avoid — they are hard to avoid **the
first time**, when everything is unfamiliar and the command looks the same as the safe one.

## What "ready to build" means

Before any of the three builds, the newcomer has done all of this and can say so:

- Read `process/RUNBOOK.md` end to end, and can name the four 👤 CLIENT steps and the four 🔒
  APPROVAL steps without looking (7, 13, 17, 20 · 6, 13, 22, 35)
- Read `process/OPERATOR.md` and the **five traps** at the top of it
- Read `design/guardrails.md` and can explain the card-grid rule and why the fix is the column
  count, not the content
- Read `process/decisions.md` — all eight rules — and has been asked, on a real past build, which rule
  applied and what they would have decided
- Run `python3 scripts/mockup.py` and `node scripts/verify.mjs` on any public URL, and read the
  output back correctly (what a FAIL returns to, what the score means)
- Knows the two portals by heart: **20682069 is QBS**, owns the nine themes, `$QBS_HUBSPOT_TOKEN`.
  Everything else is a client, `$CLIENT_HUBSPOT_TOKEN`, and the OAuth MCP must never touch it

## Build one — shadow

Sit beside a build. Do not touch the portal.

**They do:** the brief (`brands/<client>.md`) from the discovery notes, then compare against what
the owner wrote. Run every read-only command themselves as the owner runs it — `inspect`, `audit`,
`plan`, `mockup.py`, `verify.mjs` — and reconcile any difference in output. Write the step-37
actuals into `data/pages.jsonl` for this build.

**They do not:** any `--apply`, any publish, any client contact.

**Done when:** their brief and the owner's agree on every field the template marks *consumed by a
later phase*, and their `pages.jsonl` lines are accepted as the build's record.

**Unlocks:** read-only access to the QBS portal token, and `mockup.py` for real prospects.

## Build two — run it, reviewed

They run the build. The owner reviews at every 🔒 and every 🚦 before anything moves.

**They do:** every 🤖 and 🤖→🏢 step. Draft every client email. Run the gate and fix what it
returns. Present the three directions in the meeting, with the owner present.

**Review points, all mandatory:** the `reskin.py plan` output before `--apply` (the owner types
`--approved-by`, not them) · the staging URL before it is shared · the `verify.mjs` run before
step 32 · the go-live checklist before step 35.

**Done when:** the build passes the gate at ≥80 on every page with no fix the owner had to make
themselves, and the client did not learn anyone new was involved.

**Unlocks:** `--apply --approved-by <their name>` on **client** portals. Not on 20682069.

## Build three — alone

They run it. The owner reads the record afterwards, not during.

**They do:** everything, including the client calls. The owner is one message away, not in the room.

**Done when:** the retrospective — written, in `process/qa-findings.md` style, what went wrong and
what the process should say differently — is accepted and at least one change lands in a process
document as a result. **A build that teaches the process nothing was not observed closely enough.**

**Unlocks:** full operator status. Still not: editing the nine themes at source. That is one
person's job (`RUNBOOK.md` → *Owner and cadence*), because the nine are shared by every client
built on them.

## Permissions, as a table

| After | Can | Still cannot |
|---|---|---|
| Ready to build | Read every doc, run every read-only script on public URLs | Touch any portal |
| Build one | Read QBS portal (`inspect`, `audit`, `themetokens.py`), render real mockups | `--apply`, publish, client contact |
| Build two | `--apply` on client portals with their own `--approved-by`, publish to staging, draft client comms | Anything on 20682069 that writes; go-live without a second pair of eyes |
| Build three | Full operator — go-live, sign off gates, own a client | Edit `themes/source/` or the nine live themes |

## The visual module catalogue

Step 13 asks a client to choose from 57 module *names*. The newcomer will be doing the same.
Every theme ships `templates/all-modules.html`; publish it once to QBS staging
(`20682069.hs-sites.com`, `noindex`), screenshot each module at 1440 and 390, and keep the images
under `themes/catalogue/`. Until that page is published, the catalogue is
`themes/catalogue.md` — read the module list there alongside the live QBS site, which uses most of them.

## Three things the owner does, not the newcomer

1. Rotates any PAT that was ever pasted into a chat.
2. Signs the first `--approved-by` on every new client portal, so the portal-ID check has been
   done by a human who has done it before.
3. Runs the monthly agenda. Onboarding does not transfer that.
