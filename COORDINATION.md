# Coordination board

This checkout has a single active Arena session on the fixed branch `arena/aed145d8-cupertino3`. No parallel-agent claims or commits existed at start. Arena requires this fixed branch; the requested alternate session branch/worktree cannot be used.

| Task | Status | Owner | Files |
|---|---|---|---|
| Privacy-first research dashboard and integration | done | arena/aed145d8-cupertino3 | `index.html`, `styles.css`, `app.js`, `COORDINATION.md`, `.github/workflows/pages.yml` |
| Specific property, operating-cost and 2040–2050 projection verification | needs review | arena/aed145d8-cupertino3 | Published on Flagged for Review section; amounts left blank |

## Sources checked

- California BOE, Prop 13 assessment limits and Prop 8 lower-value treatment: https://boe.ca.gov/proptaxes/pdf/lta25023.pdf
- California BOE, basic rate and assessed property system: https://boe.ca.gov/pdf/pub800-5.pdf
- BOE 2025 Proposition 19 exclusion adjustment ($1,044,586 applicable Feb. 16, 2025–Feb. 15, 2027): https://www.boe.ca.gov/news/2025/nr-25-02.htm
- San Francisco Assessor, parent-child Proposition 19 exclusion: https://www.sfassessor.org/tax-savings/exclusions/reappraisal-exclusion-between-parent-child
- IRS estate tax filing threshold, 2026: https://www.irs.gov/businesses/small-businesses-self-employed/estate-tax
- IRS inherited basis and estate tax FAQ: https://www.irs.gov/businesses/small-businesses-self-employed/frequently-asked-questions-on-estate-taxes
- IRS 2026 Form 709 instructions: https://www.irs.gov/pub/irs-dft/i709--dft.pdf
- California DOI homeowner premium comparison (official tool; not a property-specific quote): https://interactive.web.insurance.ca.gov/apex_extprd/f?p=111:21:::NO:::
- California DOI residential insurance guidance: https://www.insurance.ca.gov/01-consumers/105-type/5-residential/
- Santa Clara County Assessor: https://www.sccassessor.org/ ; San Francisco Assessor: https://www.sfassessor.org/
- California FTB: https://www.ftb.ca.gov/ ; CPUC: https://www.cpuc.ca.gov/ ; CSLB: https://www.cslb.ca.gov/

## Verification and privacy

Checked source content against official BOE, county assessor, IRS and California agency pages returned by search. The published dashboard has links on every populated factual table row; unsourced figures are blank. User-supplied property figures, rents, expenses, locations beyond generic city-area context, and personal data have been excluded from the public site. The user’s property-value and bill histories were not independently verified. No point forecast was fabricated for 2040–2050. Individual trust, title, ownership, multi-unit Prop 19 treatment and California inheritance-tax questions remain flagged for professional/official confirmation.

## Deployment / integration note

Static GitHub Pages workflow added. It deploys on push to `main`; this session may not push to `main`, create another branch, or claim an untracked integration branch. No PR/merge/deployment success is claimed. Current session branch must be pushed and reviewed/merged through the repository’s normal integration process before Pages can deploy.

---

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
- Merged `origin/main` (PR #1 from another session: root dashboard, `.github/workflows/pages.yml`) into this branch. Both coordination boards are kept. The root dashboard is unchanged.
- This analysis is published under `/docs/` of the same Pages site. The Pages source (legacy, `main` `/`) is unchanged, so the root dashboard keeps working.


---

<!-- Session 64308d3a (branch arena/64308d3a-cupertino3) board below -->

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
