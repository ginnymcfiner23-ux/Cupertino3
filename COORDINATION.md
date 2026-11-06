# COORDINATION.md — shared task board

Session ID for this work: `arena-340c906c`
Working branch (fixed for this session): `arena/340c906c-cupertino3`
(Branch-name note: the task spec suggested `session-<id>/<task>` branches. The session is bound to `arena/340c906c-cupertino3`, so all tasks are done on that branch and claims are tracked here instead.)

Statuses: `unclaimed` · `in progress` · `done` · `needs review` (published on the Flagged for Review page; does not block).

| ID | Task | Status | Owner (session) | File scope (as built) |
|----|------|--------|-----------------|------------|
| T0 | Repo review (README, git state, Pages config) | done | arena-340c906c | README.md, COORDINATION.md |
| T1 | Official-source research: CA/federal/SF/Cupertino tax, inheritance, insurance, utilities, inflation | done | arena-340c906c | data/sources.json, data/tax_law.json |
| T2 | Data tables: user-supplied property tax & assessment history (BOE-checked), cost inputs, flags, process | done | arena-340c906c | data/property_tax_history.json, data/cost_inputs.json, data/flags.json, data/process_steps.json, tools/build_data.py |
| T3 | Projection model (value, tax, insurance, utilities, maintenance, rent, live/rent/sell) | done | arena-340c906c | model/project.py, data/projections.json |
| T4 | Static GitHub Pages site (overview, category pages, Flagged for Review, sources) | done | arena-340c906c | docs/**, tools/build_site.py |
| T5 | Integration: consistency and privacy checks, PR to main, merge, Pages deploy check | in progress | arena-340c906c | tools/check_site.py, COORDINATION.md (final log) |

## Privacy rule (applies to every task)
No names, street addresses, ZIP codes, contact details, or the owner's location appear in any file in this repo. Properties are referred to as **Property A (Cupertino, Santa Clara County, CA)** and **Property B (San Francisco, CA)**. Beneficiary = "[Beneficiary]", trust = "[Trust]". `tools/check_site.py` scans every text file for these patterns.

## Log
- Claim T0–T5 by arena-340c906c. Repo reviewed: README.md only (`# Cupertino3`), single commit `2d6bbb2`, GitHub Pages already enabled, public repo, legacy build from `main` `/`.
- T1–T4 built on this branch. Rebuild order: `tools/build_data.py` → `model/project.py` → `tools/build_site.py` → `tools/check_site.py`.
- Pages source moved from `main` `/` to `main` `/docs` so the built site is served (see final log for the verified deploy).
