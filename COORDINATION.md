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

- PR and merge details: see the entry below once the PR is open.
