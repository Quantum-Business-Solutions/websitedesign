# data/

The evidence layer. Everything here is **measured**, appended, never edited by hand.

| File | Written by | One line per |
|---|---|---|
| `pages.jsonl` | RUNBOOK step 27, when a page ships | shipped page — client, URL, template, **section order**, vertical |
| `performance.jsonl` | `scripts/converted.py pull` | page × pull — visits, submissions, conversion |
| `learnings.jsonl` | `scripts/converted.py learn` | above-the-fold section order that cleared the **sample floor** — with a confidence that scales with sample |
| `../verify-out/scores.jsonl` | `scripts/verify.mjs` | page × run — the 0–100 critic score. The quality trendline |

**The sample floor is the whole point.** A learning is written only on ≥6 pages and ≥200 visits.
Below that it's noise with a confidence score — which is exactly the failure already sitting in
BrandCommand's `agent_learnings`, where the best variant is the one at 0%.

After ten builds this directory is the thing no competitor can copy by hiring a designer: *"on
dealer homepages this section order converts at X, n=6."*
