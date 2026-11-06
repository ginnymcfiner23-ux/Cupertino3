# COORDINATION.md — shared task board

Session ID for this work: `arena-340c906c`
Working branch (fixed for this session): `arena/340c906c-cupertino3`
(Branch-name note: the task spec suggested `session-<id>/<task>` branches. The session is bound to `arena/340c906c-cupertino3`, so all tasks are done on that branch and claims are tracked here instead.)

Statuses: `unclaimed` · `in progress` · `done` · `needs review` (published on the Flagged for Review page; does not block).

| ID | Task | Status | Owner (session) | File scope |
|----|------|--------|-----------------|------------|
| T0 | Repo review (README, git state, Pages config) | done | arena-340c906c | README.md, COORDINATION.md |
| T1 | Official-source research: CA/federal/SF/Cupertino tax, inheritance, insurance, utilities, inflation | in progress | arena-340c906c | data/sources.json |
| T2 | Data tables: user-supplied property tax & assessment history, cost inputs, with verification status | in progress | arena-340c906c | data/properties.json, data/costs.json, data/tax_law.json |
| T3 | Projection model (property value, tax, insurance, utilities, maintenance, rent, sell-vs-hold) | in progress | arena-340c906c | model/project.py, data/projections.json |
| T4 | Static GitHub Pages site (landing + category subpages + Flagged for Review) | in progress | arena-340c906c | docs/**, tools/build_site.py |
| T5 | Integration: combined re-verification, link check, PR to main, merge, Pages deploy check | unclaimed | arena-340c906c | tools/check_site.py, COORDINATION.md (final log) |

## Privacy rule (applies to every task)
No names, street addresses, ZIP codes, contact details, or the owner's location appear in any file in this repo. Properties are referred to as **Property A (Cupertino, Santa Clara County, CA)** and **Property B (San Francisco, CA)**. Beneficiary = "[Beneficiary]", trust = "[Trust]".

## Log
- Claim T0–T5 by arena-340c906c. Repo reviewed: README.md only (`# Cupertino3`), single commit `2d6bbb2`, GitHub Pages already enabled, public repo, legacy build from `main` `/`.
