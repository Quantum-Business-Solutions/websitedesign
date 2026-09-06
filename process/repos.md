# Where client work lives

**Not a branch per client.** One shared method repo, and a client repo only when a client build
produces code. Most won't.

---

## Why a branch per client is the wrong tool

A branch is for a divergent version of the same thing that will eventually **converge**. A client
site never converges back into the methodology. Using branches that way breaks in five specific
ways:

1. **Improvements stop reaching clients.** Every fix to the process, the guardrails or the scripts
   lands on `main`. Twenty client branches means twenty stale copies, each needing a merge nobody
   will do. Six months in, the newest client has the best tooling and the oldest has none.
2. **You can only see one client at a time.** Checking out Kelly hides Revolution. Cross-client work
   becomes impossible — and cross-client work is where the value is. `verticals/office-technology.md`
   only exists because six clients' briefs were readable side by side in one working tree.
3. **History becomes unreadable.** Either `main` carries client commits or the branches diverge
   permanently. Neither gives you a usable `git log`.
4. **The scripts have no home.** If `reskin.py` improves on a client branch, which branch is
   canonical? The answer is always `main`, which means client branches can never contribute.
5. **It is the fork mistake, one level up.** `process/reskin.md` forbids forking the nine themes per
   client because nine maintainable themes become forty unmaintainable ones. A branch per client is
   the same error applied to the repo.

## The boundary that actually works

Four layers, each with one job:

| Layer | Holds | Source of truth for |
|---|---|---|
| **`websitedesign`** — `main` only | The method, the guardrails, the patterns, the scripts, **and every client brief** | How we work, and what we know about each client |
| **`<client>` repo** — *only when needed* | Custom theme source, client-specific modules, review previews, upload tooling | The client's build source |
| **HubSpot** | The live site | **The site itself.** Always |
| **BrandCommand / ClientCommand** | Project, plan, pages, assets, hours | The engagement |

The scripts here already assume this shape. They take the client as an **argument**, not as a
checkout:

```bash
python3 scripts/reskin.py plan --client "Kelly Office Solutions" …
python3 scripts/mockup.py --client "Kelly Office Solutions" --brief brands/kelly-office-solutions.md …
node scripts/verify.mjs <url> --expect-org "Kelly Office Solutions"
```

**`websitedesign` is a tool that operates on clients, not a template you copy per client.** That
distinction is the whole answer.

## The decision rule: a client gets a repo when Phase 4 happens

Phase 4 of `process/RUNBOOK.md` is *build theme, templates, modules*. If a build produces **code**,
it needs a repo. If it doesn't, a repo would be empty.

| Situation | Repo? |
|---|---|
| **Launch tier** — three-of-nine re-skinned, no custom modules | **No.** HubSpot is the artifact; the brief is the record |
| **Growth** — re-skin plus a handful of existing modules | **No**, usually |
| **Growth/Transform with custom modules** | **Yes** — Revolution needed 29 modules, 7 sections, 10 templates |
| Custom app, calculator, or an interactive preview | **Yes** |

`Quantum-Business-Solutions/revolution` is the existing precedent and it was the right call: a
Next.js preview app, the HubSpot theme as a record, and `gen-tokens.mjs` / `upload.sh` /
`build-site.mjs`. None of that would fit here, and none of it belongs on a branch.

## Briefs stay here, all of them, together

`brands/<slug>.md` lives in `websitedesign` even for clients with their own repo. This is the one
place a per-client split would do real damage:

- Reading across briefs is how the **vertical layer** got built. Six dealer briefs in one tree
  produced a measured category palette, a keyword profile and a module kit. Split across six repos,
  that never happens.
- Briefs are **tiny text files.** There is no storage argument.
- They are the **institutional memory** — the Revolution "Ink" conflict was caught weeks later only
  because a constraint was written down somewhere findable.

> ⚠️ **They also contain client-confidential material** — pricing, stated constraints, contacts,
> traffic numbers. `websitedesign` must stay **private**, and if it is ever shared or opened up, the
> `brands/` directory moves first. No credentials in briefs, ever — reference where a token lives,
> never its value.

## The drift risk, named

Revolution's repo carries tooling that does not exist here: `gen-tokens.mjs`, `gen-chrome.mjs`,
`upload.sh`, `build-site.mjs`, `tools/reg.mjs`. **The tooling has already forked once.** That is the
real cost of client repos, and the mitigation is a rule:

**Tooling that would help a second client belongs in `websitedesign`, not in a client repo.**

By that rule, at least three of Revolution's five scripts should be here:

- `upload.sh` — syncing a theme folder to a portal with HubL validation is universal
- `build-site.mjs` — building pages from a content definition is universal
- `gen-tokens.mjs` — generating tokens from one source is the principle `designsystem.py` already
  follows

Only `gen-chrome.mjs` (defaults from Revolution's own nav) and the Next.js resolve hook are
genuinely client-specific.

## Public preview URLs: the client repo is the front end

A pitch needs a URL a buyer can open on a phone without a login. The client repo gives you one for
free: connect it to Vercel once (Add New Project, import the repo, no framework, no build command)
and every push to `main` redeploys to `https://<client-slug>.vercel.app`. Nothing to run, nothing to
maintain, and the repo stays the record.

What goes in the repo root so the URL is worth sharing (Kelly is the reference,
`Quantum-Business-Solutions/kelly-office-solutions`):

| File | What it is |
|---|---|
| `index.html` | A hub in the client's colours: the directions, the home render, the Quantum Website Standard |
| `directions.html` | The pitch page from `mockup.py`, wrapped in a full HTML document |
| `home-clean.html` (one per rendered direction) | The high-fidelity render, self-contained, images inlined |
| `standard.html` | The client-facing guarantee |
| `vercel.json` | `cleanUrls: true` and an `X-Robots-Tag: noindex, nofollow` header on every path |

Rules: **noindex everywhere** (a preview that gets indexed is a duplicate of the client's future
site); no forms that submit anywhere; no analytics; the dated files under `directions/` and
`renders/` stay as the record and the root files are the served copies. The gate runs against the
preview URL with `--env staging`, which requires the noindex.

This replaces nothing in HubSpot. The preview is a picture of the site; the site is the clone.

## Naming

| Thing | Convention |
|---|---|
| Client repo | `Quantum-Business-Solutions/<client-slug>` — lowercase, hyphenated |
| Brief | `brands/<client-slug>.md`, same slug |
| Theme clone in HubSpot | `<Company> — <ThemeName>` |
| BrandCommand project | `<Company> — <ThemeName>`, per direction |
| Semrush project | the client's name |

One slug per client, used everywhere. Chasing a client across four systems with three spellings is
a real cost at ten clients.

## Branches inside a client repo

Normal software branching — `main` is what's deployed, feature branches for work in progress. That
is branches used for what branches are for. The rule is only about **never using a branch to mean a
client.**

## What this means at ten clients

- One `websitedesign`, one `main`, ten briefs in one directory, one set of scripts everyone benefits
  from.
- Two or three client repos, for the builds that genuinely produced code.
- Ten live sites in HubSpot, ten projects in ClientCommand.
- A vertical layer that gets better every time a brief is added — which is the compounding property
  none of the alternatives have.

---

## Do we need Supabase and Vercel per client?

**Supabase: no. Not for any client.** Nothing in a website build needs a database. There is one
Supabase — BrandCommand's — and it is already brand-scoped by `brand_profile_id`. A second instance
per client would hold nothing.

**Vercel: almost never, and the reason is `mockup.py`.** It emits a single self-contained HTML file.
That publishes as an **Artifact** — private by default, a shareable link, no build step, no hosting,
no cost, seconds. That is what the three-option pitch needs, and it is what replaced the previous
approach.

Revolution used Next.js on a host because it predates `mockup.py` **and** because its preview does
something a static file can't: a live direction switcher and a client edit mode. That is the
threshold.

| What you're publishing | Where | Cost |
|---|---|---|
| Three-option pitch | **Artifact** | none |
| Interactive preview — direction switcher, live edit | Vercel project in the client repo | a project |
| A calculator or tool that outlives the pitch | Vercel, or a HubSpot module | — |
| **The actual site** | **HubSpot, client portal** | their subscription |

One thing worth knowing: the QBS Vercel team (`quantum-business-solutions1`, Pro) currently shows
**zero projects** via the API. If previews have been deployed, they are on a personal scope the
integration can't see — which is itself a reason to standardise: a client preview on someone's
personal account is not a company asset.

## What Claude can do, and where you have to be involved

**End to end without you:**

- The diagnosis, the four Semrush pulls, the brand measurement
- Mockups → published artifact
- Clone, re-skin, client `Organization` schema — *proposed*; see below
- Page build, asset generation, the gate, the agent loop
- Vercel: creating a git project and deploying, when a preview needs one (the integration is
  connected and authorised)

**Needs you, and always will:**

1. **DNS at cutover.** Only the domain owner can point a domain. This is the one genuinely
   unavoidable human step in the whole process, and it belongs on the plan with a date — Revolution's
   own plan asked for "access to DNS and the current host by Week 5."
2. **Approving portal writes.** `reskin.py plan` prints the change table; a person says yes. That is
   the protocol and it does not get automated.
3. **Creating a new GitHub repo.** This session's GitHub access is scoped to attached repositories,
   so a brand-new client repo is created by you (or attached after you create it).
4. **Anything that spends money** — a HubSpot tier upgrade, Higgsfield credits, a domain.
5. **The four questions.** Ground, register, the promise, the lane. The promise especially: it is the
   one input that cannot be measured or inferred.
6. **Client-facing claims about the client.** Any figure on their site — response times, technician
   counts, devices under management — is theirs to confirm. An agent that cannot find a number will
   write a plausible one, and no gate catches that.

The honest summary: **Claude can do the build; you own the approvals, the domain, and the truth of
anything the site claims.**
