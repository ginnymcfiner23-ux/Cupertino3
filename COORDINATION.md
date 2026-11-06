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
5. Only the final integration step edits shared outputs (`docs/` navigation/index, combined data, PR and merge log).
6. Irregularities and unverified values go to `docs/flagged/` ("Flagged for Review") and the Irregularities register below. They never block a merge.

Standing rules for this project:
- Personal information is anonymized. No names, street addresses, parcel numbers, owner details, or precise ZIP codes appear in any file that is published.
- Every verified value needs an official source link. Values that cannot be confirmed from an official source are left blank in verified columns and marked `UNVERIFIED`.
- User-provided numbers are used only as labeled modeling inputs, never as verified facts.

Session context: session `c1b5796b`, branch `arena/c1b5796b-cupertino3` (fixed for this session; the branch name cannot be changed).

## Task Board

| ID | Task | Owner (session) | Branch | File scope | Status | Commits |
|----|------|-----------------|--------|------------|--------|---------|
| T0 | Coordination board and claims | c1b5796b | arena/c1b5796b-cupertino3 | COORDINATION.md | claimed | — |
| T1 | Official-source research and verification register | c1b5796b | arena/c1b5796b-cupertino3 | data/sources.json, data/facts.json | claimed | — |
| T2 | Projection model (inflation, tax, Prop 13/19, live/rent/sell) | c1b5796b | arena/c1b5796b-cupertino3 | scripts/model.py, data/inputs.json, data/projections.json | claimed | — |
| T3 | Static site build (Pages, `docs/`) | c1b5796b | arena/c1b5796b-cupertino3 | scripts/build_site.py, docs/** | claimed | — |
| T4 | Flagged for Review page and irregularities register | c1b5796b | arena/c1b5796b-cupertino3 | data/flags.json, docs/flagged/** | claimed | — |
| T5 | Final integration: validation, PR, merge, Pages verification | c1b5796b | arena/c1b5796b-cupertino3 | scripts/validate.py, docs/index.html, COORDINATION.md | claimed | — |

## Activity Log

- 2026-11-06 — T0 claimed by session c1b5796b (this file created).

## Irregularities & Unverified Register

Full detail is on the "Flagged for Review" page (`docs/flagged/`). Summary is filled in by T4.

## Integration Log (PR and merge)

Filled in by T5 (PR link, merge result, Pages deploy status).
