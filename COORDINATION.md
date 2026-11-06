# COORDINATION.md — Shared Task Board

Repo: `ginnymcfiner23-ux/Cupertino3`
Working branch for this session: `arena/64308d3a-cupertino3` (branch name is fixed by the session; per-task `session-<id>/<task>` sub-branches are not used because all work must stay on this branch).
Session ID: `session-64308d3a`

Status key: `unclaimed` · `in progress` · `done` · `needs review` (published on the Flagged for Review page; does not block)

## Privacy rule (applies to every task)
- No names, addresses, parcel numbers (APN), ZIP codes, or the user's personal location appear in any file in this repo or on the site.
- Properties are referred to only as **Property A (Cupertino, Santa Clara County, CA)** and **Property B (San Francisco, CA — rental/primary-residence property)**.
- Any personal detail seen during research is kept out of git and out of the site.

## Task board

| ID | Task | Status | Owner | Files in scope |
|----|------|--------|-------|----------------|
| T1 | Repo review & irregularities log | done | session-64308d3a | `COORDINATION.md`, `data/irregularities.json` |
| T2 | California property tax & Prop 13 / Prop 19 rules (trust transfers) | done | session-64308d3a | `data/facts.json` (category property-tax), `data/property_tax_history.json` |
| T3 | Federal & state estate, gift, income, and capital-gains tax thresholds (2026 + projections) | done | session-64308d3a | `data/facts.json` (federal, california), `data/assumptions.json` |
| T4 | Utilities: water (Cupertino / SF), electricity & solar (Cupertino), SF rental costs | done (partial: unverified rows blank) | session-64308d3a | `data/facts.json` (utilities, rental) |
| T5 | Insurance research: primary residence (Cupertino) and rental/landlord (SF) | done (no verified premium averages; blank) | session-64308d3a | `data/facts.json` (insurance) |
| T6 | Legislative watchlist (proposed changes to tax, property, inheritance law) | done (`needs review` items flagged) | session-64308d3a | `data/legislation.json` |
| T7 | Projection model (property value, assessed value, tax, costs, hold/rent/sell scenarios) | done | session-64308d3a | `data/assumptions.json`, `model/project.py`, `data/projections.json` |
| T8 | Static site build + link checker + Pages config | done (site is `docs/`; Pages source set to `main` `/docs` after merge) | session-64308d3a | `docs/`, `scripts/build_site.py`, `scripts/check_site.py` |
| T9 | Integration: merge, re-verify combined data, build, PR to `main`, merge, confirm Pages | in progress | session-64308d3a | `docs/` (generated), `README.md`, `COORDINATION.md` (final log) |

## Claim log
- 2026-11-06 · session-64308d3a · claimed T1–T9 (single-session run; all tasks executed on `arena/64308d3a-cupertino3`).
- 2026-11-06 · session-64308d3a · T1–T8 complete on the branch: data (`data/`), model (`model/project.py`), site (`docs/`, 14 pages), validators (`scripts/check_site.py`: OK). T9 integration started.

## Handoff / conflict log
- Source-URL corrections (2026-11-06): an early CPUC link was a different decision (23-10-013) and was removed; the ACC Plus rule is now cited to the PG&E tariff text. Two other URLs were corrected from search results. Verified URLs only are in `data/sources.json`.
- Cupertino TRA composite not located in the official rate book pages reviewed (chunks 0-8 read; blank and flagged).
- Client tax history implies effective rates above official rates (IR01). Flagged, not corrected.

## Integration (T9)
- Target: PR from `arena/64308d3a-cupertino3` to `main`. PR link and merge result to be recorded below after merge.
- PR: pending
- Merge: pending
- Pages: pending
