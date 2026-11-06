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

# Session 41b64714 — integration board (added by final integration session)

Working branch (fixed): `arena/41b64714-cupertino3` · Session ID: `session-41b64714`

## Task board

| ID | Task | Status | Owner | Files |
|----|------|--------|-------|-------|
| T0 | Repo review + claims | done | session-41b64714 | COORDINATION.md |
| T1 | Law/tax research (federal estate tax, CA no inheritance tax, Prop 13/19) | done | session-41b64714 | data/law-tax.md, docs/analysis/tax-law.html |
| T2 | Property tax & assessment history (both properties) | done | session-41b64714 | data/properties.md, docs/analysis/properties.html |
| T3 | Utilities & insurance research | done | session-41b64714 | data/costs.md, docs/analysis/costs.html |
| T4 | Inheritance process step-by-step | done | session-41b64714 | data/inheritance.md, docs/analysis/inheritance.html |
| T5 | Projection engine + scenarios | done | session-41b64714 | scripts/analysis_projections.py, scripts/analysis_build_site.py, data/projections.analysis.json, docs/analysis/projections.html, docs/analysis/scenarios.html |
| T6 | GitHub Pages dashboard (docs/analysis/ section) | done | session-41b64714 | docs/analysis/** |
| T7 | Verification pass (line-by-line, source links on every table) | done | session-41b64714 | docs/analysis/flagged.html |
| T8 | Integration: merge branches, re-verify combined data, confirm site builds, publish Pages | done | session-41b64714 | COORDINATION.md, docs/index.html (cross-link) |

## Integration log

- PR #9 (`arena/41b64714-cupertino3` → `main`): first merge attempt not mergeable (conflict with parallel-session work on `docs/`, `data/projections.json`, `scripts/build_site.py`, `COORDINATION.md`, `README.md`). Resolved by merging `origin/main`, keeping its files unchanged, moving this session's pages to `docs/analysis/` (self-contained assets), data to `data/projections.analysis.json`, scripts to `scripts/analysis_*.py`, and appending this board. No other session's work discarded.
- Cross-link added to `docs/index.html` ("Additional analysis" tile → `analysis/index.html`).
- Re-verified: analysis section links checked (OK); `docs/index.html` cross-link OK; root site served at Pages `/`; `/docs/` and `/guide/` analyses on the same site.
- This session's findings are consistent with the other analyses: sell-at-inheritance is the strongest modeled plan; Prop 19 full reassessment of the rental is the main cost driver; stepped-up basis means $0 capital gains on immediate sale. This session additionally preserved the full 2014–2026 tax/assessment history and quantified the rate-gap irregularities (Cupertino implied 1.32–1.41% vs published ~1.15–1.22%; SF implied 1.73–2.14% vs published 1.18% secured).
- Pages deployment: root site live at `<pages-url>/Cupertino3/` (see Pages settings for the canonical URL). Legacy `pages-build-deployment` shows `errored` (known GitHub-side legacy build state, documented by session 64308d3a); deploys succeed through `.github/workflows/pages.yml`.

## Privacy

No names, addresses, parcel numbers, ZIP codes, or account handles in any file. Properties referred to as Property A (Cupertino) / Property B (San Francisco) in the other analyses; this session's pages use generic "Cupertino house" / "SF house" labels with no personal identifiers.
