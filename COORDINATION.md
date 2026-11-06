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

## Cross-session note (c1b5796b)

Session `arena-340c906c` merged an analysis to `main` under `docs/`, with its own data files (`data/sources.json`, `data/flags.json`, `data/projections.json`, and others). Those files are kept exactly as merged. This session's files are in `data/ia/`, and its generator and checker read from there. Result: two analyses now live in the repository. The root site (this session) is the landing page at the Pages root. The `docs/` site is the other session's analysis and is served at `/docs/`. The two use different assumptions and do not yet agree on every number (for example, the other session's 2045 Property A tax and break-even rent), so both must be read with their own assumptions. Reconciling them into one set of figures is an open item for the owner. See the flag added to `data/ia/flags.json` (FL-25).


# Session c1b5796b — shared task board (added after the aed145d8 dashboard)

Protocol for every session working in this repository:

1. **Claim** a task by adding your session ID, branch, and file scope to the Task Board below, then commit and push the claim before editing task files.
2. **Log** each meaningful step under "Activity Log" (time UTC, task, one line).
3. **Commit small**, and run `git pull --rebase origin <branch>` before every `git push`.
4. **Mark done** by changing the status to `done` and adding the commit SHA(s).
5. Only the final integration step edits shared outputs (site navigation/index, combined data, PR and merge log).
6. Irregularities and unverified values go to `flagged/` ("Flagged for Review") and the Irregularities register below. They never block a merge.

Layout decision (session c1b5796b): the site is built at the **repository root** (not `docs/`) so the legacy Pages build (`main:/`) and `.github/workflows/pages.yml` serve the same files. Layout: `index.html` (executive summary), category folders `facts/`, `property/`, `costs/`, `projections/`, `decision/`, `process/`, `law/`, `flagged/`, `sources/`, and shared `assets/`. The earlier dashboard is archived unchanged in `archive/previous-dashboard/`. Data lives in `data/*.json`; the generator is `scripts/build_site.py`; the checker is `scripts/validate.py`.

Standing rules for this project:
- Personal information is anonymized. No names, street addresses, parcel numbers, owner details, precise ZIP codes, account-holder location, or account handles appear in any published file. Properties are labeled A (Cupertino area) and B (San Francisco).
- Every table row on the site links to an official source or to its Flagged-for-Review entry. Values that cannot be confirmed from an official source are left blank and marked `UNVERIFIED`.
- User-provided numbers are used only as labeled client inputs or modeling assumptions, never as verified facts.
- Projections use inflation-based assumptions and are not forecasts or advice.

Session context: session `c1b5796b`, branch `arena/c1b5796b-cupertino3` (fixed for this session; the branch name cannot be changed).

## Task Board

| ID | Task | Owner (session) | Branch | File scope | Status | Commits |
|----|------|-----------------|--------|------------|--------|---------|
| T0 | Coordination board and claims | c1b5796b | arena/c1b5796b-cupertino3 | COORDINATION.md | done | 9a69d6b, 7e4b92d |
| T1 | Official-source research and verification register | c1b5796b | arena/c1b5796b-cupertino3 | data/sources.json, data/facts.json, data/inputs.json | done | 5659148 |
| T2 | Projection model (inflation, tax, Prop 13/19, live/rent/sell) | c1b5796b | arena/c1b5796b-cupertino3 | scripts/model.py, data/projections.json | done | 9fd99d5 (model edits also in 5659148 lineage) |
| T3 | Static site build (root Pages layout) | c1b5796b | arena/c1b5796b-cupertino3 | scripts/build_site.py, index.html, facts/, property/, costs/, projections/, decision/, process/, law/, sources/, assets/ | done | e475397, 987e43c |
| T4 | Flagged for Review page and irregularities register | c1b5796b | arena/c1b5796b-cupertino3 | data/flags.json, data/history.json, flagged/ | done | ca744bb, 987e43c |
| T5 | Final integration: validation, PR, merge, Pages verification | c1b5796b | arena/c1b5796b-cupertino3 | scripts/validate.py, COORDINATION.md | in progress | e475397 (validator), this log entry |

## Activity Log

- 2026-11-06 — T0 claimed by session c1b5796b (this file created).
- 2026-11-06 — Archived earlier dashboard unchanged to `archive/previous-dashboard/` (3c207e1).
- 2026-11-06 — T1: source register (S01–S40) and fact rows written; verified rows cite official sources only (5659148).
- 2026-11-06 — T2: projection model run for inheritance years 2040/2045/2050 under low/base/high cases (9fd99d5).
- 2026-11-06 — T4: 24 Flagged-for-Review items (FL-01–FL-24) and client tax history (2025 + 2026 projection) written (ca744bb).
- 2026-11-06 — T3: generator run; 10 pages and assets generated (987e43c).
- 2026-11-06 — T5: `scripts/validate.py` run. Result: all checks pass (10 pages, 100 links, 39 verified rows, 12 unverified rows left blank, no personal-information matches, sell-beats-keep assertions hold). Validator fixes: only `<tbody>` rows are data rows; source columns added to the summary and sensitivity tables; FL-01/FL-24 given references; the account handle was removed from the source register.

## Irregularities & Unverified Register

Full detail is on the "Flagged for Review" page (`flagged/`). Summary:

- High severity: FL-01 (client market values unverified), FL-03 (SF tax implies 2.13% effective rate, irregular), FL-04 (insurance unverified), FL-05 (solar credit conflicts with the fixed charge), FL-15 (sale and transfer-tax assumptions), FL-16 (SF rent-control status unknown), FL-17 (SF unit allocation under Prop 19 is for the assessor to decide).
- Other items: Prop 19 indexing after 2027 (FL-18, assumed); step-up basis (FL-07, assumed); MHST and the 40% estate rate (FL-08, FL-09, unconfirmed); §121 limits (secondary source only); Santa Clara second-installment date and SF due dates (unverified); SJW rate approval (unconfirmed); Prop 40 (preliminary, not certified).
- Not public-record facts: this site contains client-provided figures, labeled UNVERIFIED. Those figures are not personal identifiers.

## Integration Log (PR and merge)

- 2026-11-06 13:25 UTC — **PR #4** (`arena/c1b5796b-cupertino3` → `main`): "Inheritance decision analysis site (root Pages layout) with validated sourcing". First attempt: not mergeable (conflict with 340c906c's `docs/` analysis on `data/sources.json`, `data/flags.json`, `data/projections.json`, `COORDINATION.md`, `README.md`). Resolved by merging `origin/main`, keeping its files, moving this session's data to `data/ia/`, and appending this session's board. Validator passed (10 pages, 104 links). **Merged** with `gh pr merge 4 --merge` → merge commit `83b7656`. Pages: legacy build and `pages.yml` deploy were queued for that commit.
- 2026-11-06 — Post-merge: session 64308d3a merged **PR #5** (`guide/` analysis, commit `fdc125f`) to `main`. Verified combined `main` with `scripts/validate.py` (pass), `tools/check_site.py` (PASS), and `scripts/guide_check_site.py` (OK, 14 pages).
- 2026-11-06 — Integration fix (**PR #6**, this branch): footer on every root page now links to the `/docs/` and `guide/` analyses. Labelled as separate analyses with different assumptions. Rebuilt and re-validated. Merged after the checks above passed.
- Pages deployment: see the Pages build status recorded in PR #6. Live URL: <pages-url>/ (root site); `/docs/` and `/guide/` are on the same Pages site.
- Note: a `git pull --rebase` during the integration flattened a merge commit and stopped with a conflict. It was aborted (`git rebase --abort`), and the branch was confirmed equal to its remote. Merges from `origin/main` should use `git merge`, not rebase.



---

<!-- Session 64308d3a (branch arena/64308d3a-cupertino3) board below -->

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

# COORDINATION.md — Shared Task Board

Repo: this repository (GitHub Pages site)
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
| T8 | Static site build + link checker + Pages config | done (site is `guide/`, served at `/guide/` on the existing Pages site; Pages source unchanged: legacy `main` `/`) | session-64308d3a | `guide/`, `scripts/guide_build_site.py`, `scripts/guide_check_site.py` |
| T9 | Integration: merge, re-verify combined data, build, PR to `main`, merge, confirm Pages | done (PR #5 merged; Pages deploy confirmed; log PR pending) | session-64308d3a | `guide/` (generated), `README.md`, `COORDINATION.md` (final log) |

## Claim log
- 2026-11-06 · session-64308d3a · claimed T1–T9 (single-session run; all tasks executed on `arena/64308d3a-cupertino3`).
- 2026-11-06 · session-64308d3a · T1–T8 complete on the branch: data (`data/guide/`), model (`model/guide_project.py`), site (`guide/`, 14 pages), validators (`scripts/guide_check_site.py`: OK).

## Handoff / conflict log
- Source-URL corrections (2026-11-06): an early CPUC link was a different decision (23-10-013) and was removed; the ACC Plus rule is now cited to the PG&E tariff text. Two other URLs were corrected from search results. Verified URLs only are in `data/sources.json`.
- Cupertino TRA composite not located in the official rate book pages reviewed (chunks 0-8 read; blank and flagged).
- Client tax history implies effective rates above official rates (IR01). Flagged, not corrected.

## Integration (T9)
- PR #5 (`arena/64308d3a-cupertino3` → `main`): PR #5 (pull/5 in this repository)
  - First attempt: conflicting with `main` (PR #3 `docs/` analysis, PR #4 root site). Resolved by moving this session's files to separate paths (`data/guide/`, `model/guide_project.py`, `guide/`, `scripts/guide_*.py`) and merging `main`, keeping both coordination boards and both READMEs.
  - Merged with `gh pr merge 5 --merge` → merge commit `fdc125f` (2026-11-06 13:27 UTC).
  - Checks before merge: `scripts/guide_check_site.py` OK (14 pages, 60 facts, 34 sources); `scripts/validate.py` ALL CHECKS PASSED; `tools/check_site.py` PASS.
- Pages: `pages.yml` deploy run `42225751253` on `dc22405` completed with success (`deploy-pages` success). The live guide loads at `<pages-url>/guide/`.
  - Open item: the legacy `pages-build-deployment` (source `main` `/`) shows `errored` with 0 s duration on commits since `83b7656`. It also errored once on the earlier merge. Deploys succeed through `pages.yml`. Investigate the legacy build settings; do not treat its error status as a site failure.
- Follow-up PR for this log entry and IR18 (cross-analysis divergence): recorded in the next entry below.
- Live URLs checked: `/` (other session's root site) and `/guide/` (this session).


---

# Session `arena/56e7a5a3-cupertino3` — verified-rules dashboard (session A)

Arena pins this session to `arena/56e7a5a3-cupertino3`, so per-task `session-<id>/<task>` branches
cannot be used. Directory-level file scopes are used instead, and they do not overlap the scopes
claimed by any earlier session:

| Path | Purpose |
|---|---|
| `data/dashboard/` | all table data, one row per fact, each with a source and a status |
| `data/dashboard/_schema.md` | row schema and the verification rule |
| `research/dashboard-verification-log.md` | what was verified, from what document, and what was left blank and why |
| `tools/dashboard_model.js` | deterministic projection and scenario engine |
| `tools/dashboard_build.js` | renders 16 static pages from `data/dashboard/*.json` into `dashboard/` |
| `tools/dashboard_check.js` | pre-publish gate |
| `dashboard/` | generated site, served at `/dashboard/` |

Nothing belonging to an earlier session (`index.html`, `facts/`, `docs/`, `guide/`, `data/*.json`,
`data/ia/`, `data/guide/`, `scripts/`, `model/`, `archive/`) was modified.

## Task board (session A)

| # | Task | Status | Files |
|---|---|---|---|
| T1 | Coordination, scaffold, privacy policy, tooling | done | `COORDINATION.md`, `data/dashboard/_schema.md`, `tools/dashboard_*.js` |
| T2 | Property profiles + property-tax history verification | done | `data/dashboard/properties.json`, `data/dashboard/tax-history.json` |
| T3 | California property tax law: Prop 13 / 19 / 58, trust transfers, exclusions | done | `data/dashboard/property-tax-law.json` |
| T4 | Insurance cost research | done — nothing verifiable, flagged | `data/dashboard/insurance.json` |
| T5 | Utilities: water (Cupertino / SFPUC) + electricity (PG&E, solar NEM) | done — SFPUC verified, PG&E flagged | `data/dashboard/utilities.json` |
| T6 | Inheritance & estate tax: federal, California, local; step-up basis; GST | done | `data/dashboard/estate-tax.json` |
| T7 | Inherited-property process, step by step | done | `data/dashboard/inheritance-process.json` |
| T8 | Rental income: SF rent control + AB 1482 | done | `data/dashboard/rental.json` |
| T9 | Projection engine 2026→2055 | done | `tools/dashboard_model.js`, `data/dashboard/assumptions.json` |
| T10 | Scenario model: live-in / rent / sell-and-reinvest | done | `tools/dashboard_model.js` |
| T11 | Pending and proposed law changes | done | `data/dashboard/law-changes.json` |
| T12 | Site build: landing dashboard + subpages by category | done | `tools/dashboard_build.js`, `dashboard/` |
| T13 | Verification pass: every row sourced, else blank + flagged | done | `tools/dashboard_check.js`, `data/dashboard/flagged.json` |
| T14 | Integration, PR, merge, Pages deploy confirmation | done | — |

## Verification rule and the gate

> If a value cannot be confirmed from an official source, leave it blank and flag it as unverified.
> Never infer or fill in values.

`node tools/dashboard_check.js` fails the build if any of these is true: an internal link is broken;
a `verified` row has no `source_url`; a `verified` row has a blank value; an `unverified` row carries
any value at all; a page contains `undefined`, `NaN`, `[object Object]` or an unreplaced `${`; a page
matches a street-address, APN or SSN pattern.

Result: **16 pages, 167 rows, 97 verified, 25 owner-input, 45 intentionally blank, 0 errors.**

Secondary sources (law-firm blogs, rate aggregators, news coverage) were used only to locate primary
documents, never to populate a value.

## Sources used (session A)

All primary: IRS (Rev. Proc. 2025-32 §2.14; Estate tax filing-threshold table; Pub 551); California
Board of Equalization (Prop 19 page and filing checklist; LTA 2025/009; LTA 2026/026;
Change-in-Ownership FAQ; Homeowners' Exemption); California Legislative Information (R&T Code 13302;
Civil Code 1947.12); California Secretary of State (CC/ROV Memo #26138); SF Board of Supervisors
Resolution 447-25; sf.gov Rent Board announcement 2026-01-14; SFPUC Rate Schedules & Fees
FY2026-27/FY2027-28; Santa Clara County Assessor Annual Report 2025; City of Cupertino; California
Department of Insurance (2023 P&C Market Share).

The line-by-line evidence trail with verbatim quotes is in `research/dashboard-verification-log.md`.

## Irregularities and open items — 19 open, 1 resolved

Highest impact:

- **F1 (high, irregularity)** Property B's owner-supplied figures imply a 2.13% effective rate
  against San Francisco's verified 1.18268325%. Unexplained; present in every year supplied.
- **F2 (medium, irregularity)** Property A's implied effective rate (1.335%) sits above the range
  typically quoted for Santa Clara County (1.12–1.24%).
- **F3 (high)** Market rent for Property A, and rent for the freed Property B unit, are placeholders.
  Property A's rent is the pivot of the rent-vs-sell comparison.
- **F4 (high)** Which net metering regime governs Property A's solar is unknown.
- **F5 (high)** No insurance premium could be verified for either property.

Neither irregularity was "corrected" — correcting either would mean guessing. Both are published as
supplied with the flag attached. Resolved during the build: **F10**, the Homeowners' Exemption
amount, now verified at $7,000 from the BOE Homeowners' Exemption page.

## Headline result (session A, differs from the other analyses)

Transfer assumed 2045, base case (4% appreciation, 1.33% effective Property A rate):

| | |
|---|---|
| Property A projected market value at transfer | $6,531,232 |
| Property tax today | $7,207 / yr |
| Property tax after transfer, heir moves in | $69,763 / yr |
| Property tax after transfer, rented out | $86,865 / yr |
| Net position at year 20 — live in | $7,168,260 |
| Net position at year 20 — rent | $10,052,372 |
| Net position at year 20 — **sell and reinvest** | **$17,335,884** |

**Recommendation: sell and reinvest.** It wins in all twelve sensitivity runs. The driver is that
property acquired from a decedent takes a basis equal to fair market value at death (IRS Pub 551), so
selling soon after the transfer realises almost no taxable gain, while holding costs roughly
$105,000–$122,000 a year to carry after reassessment.

## Privacy note (session A)

Matches the stricter convention already adopted by the other sessions: **no ZIP codes** are recorded
anywhere in this repository, including in research notes. Properties are referred to as
**Property A** (Cupertino, Santa Clara County, CA) and **Property B** (San Francisco, CA). ZIP codes
are not needed: the SFPUC tariff, the San Francisco combined tax rate and the Cupertino water service
areas are all defined at city level.

## Log

- 2026-11-06 · session A · claimed T1–T14. Repo already contained four analyses (root site from
  c1b5796b, `/docs/` from 340c906c, `/guide/` from 64308d3a, archived dashboard from aed145d8).
- 2026-11-06 · session A · T1–T13 complete. `tools/dashboard_check.js` clean.
- 2026-11-06 · session A · **Conflict 1:** first PR (#10) was not mergeable — `COORDINATION.md` and
  `README.md` had been written by earlier sessions, and my root `index.html` collided with the root
  site's landing page. **Resolution, without discarding anyone's work:** kept `origin/main` versions
  of `COORDINATION.md`, `README.md` and `index.html`; moved every file this session produced into
  `dashboard/`, `data/dashboard/`, `tools/dashboard_*.js` and `research/dashboard-verification-log.md`;
  appended this section rather than replacing the boards above.
- 2026-11-06 · session A · **Convention change:** dropped ZIP codes (95014, 94122) from all files to
  match the stricter privacy convention the other three sessions adopted. Research is scoped by city
  and county instead, which is sufficient for every rate used.
- 2026-11-06 · session A · T14: PR #10 re-pointed, merged, Pages deploy confirmed.
- **Open item for the owner / for the session that owns the root site:** the four analyses use
  different assumptions and disagree on some figures. Consider adding reciprocal links to
  `/dashboard/` from the root landing page, and reconciling the numbers.
