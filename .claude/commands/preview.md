---
description: Three complete clickable sites, one per direction, plus the chooser hub. Deploys via the client repo.
argument-hint: "<company name>"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Skill, mcp__Firecrawl__firecrawl_scrape, mcp__Higgsfield__generate_image, mcp__Higgsfield__jobs_wait
---

Build the preview site for `$ARGUMENTS`. **Nothing here touches HubSpot.** This is the step between
the directions and the build: the buyer clicks through every page of every direction on their phone,
then chooses.

## 1 — Inputs (see `process/INTAKE.md`)

- `brands/<slug>.md` exists and has the entity facts, proof points and directions filled.
- `brands/<slug>.content.json` exists. If not, write it from the brief and the client's current
  site, using `brands/kelly-office-solutions.content.json` as the reference. Every page, every
  section, real copy. No em dashes. No claim without a source in the brief.
- The client repo exists (`Quantum-Business-Solutions/<slug>`, per `process/repos.md`) and is
  connected to Vercel. Assets in `<repo>/assets/`: the logo, a hero image, `hero-og.jpg` at 1200
  wide, partner logos under `assets/partners/<slug>.png|jpg` named after the partner.
- **Look at the logo.** If it carries white type, the chrome must be dark (`brand.chrome: "dark"`,
  `brand.chrome_bg`). Kelly's does.

## 2 — Generate

```bash
python3 scripts/preview.py --content brands/<slug>.content.json \
    --themes "Quantum <A>,Quantum <B>,Quantum <C>" --recommend "Quantum <A>" \
    --roles "<A in one line>|<B in one line>|<C in one line>" \
    --base-url https://<slug>.vercel.app --out /path/to/<client-repo>
```

Each theme's real `css/quantum.css` (from `themes/source/`, as patched) is inlined with the client's
accent derived onto it, so the three differ in ground, type, measure and corner, not only colour.
The hub at `/` carries the specs, our pick with reasons, the alternatives, a side-by-side compare,
every page, the plan and the reply button. Every page is `noindex`.

## 3 — Look, then gate

Screenshot the hub and the recommended home page at 1440 and 390 and **look**. Then:

```bash
node scripts/verify.mjs https://<slug>.vercel.app/<dir>/ https://<slug>.vercel.app/<dir>/locations \
     https://<slug>.vercel.app/<dir>/blog --env staging --expect-org "<Client legal name>"
```

Under 80 on any page: fix the generator or the content, not the output.

## 4 — QA agents, then the link

Run the Copy critic, Fact checker and Mobile reviewer from `process/agents.md` against the hub and
the recommended home page. Close every correctness finding. Only then does the URL go to the client,
and only the hub URL: they choose from there.

## 5 — Feed it back

Their choice and their words into the brief. Anything the content file needed that the intake did
not ask for goes into `process/INTAKE.md`.
