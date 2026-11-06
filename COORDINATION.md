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

## Deployment / integration result

- PR #1: https://github.com/ginnymcfiner23-ux/Cupertino3/pull/1
- Merged to `main` with a merge commit on 2026-11-06.
- GitHub Pages workflow run: https://github.com/ginnymcfiner23-ux/Cupertino3/actions/runs/42223506923 — queued when checked; successful deployment is not yet confirmed.
- No PR checks were reported before merge. Static HTML navigation was checked locally; data claims remain limited to the cited official-source statements. GitHub Pages must be enabled for the repository if workflow deployment does not proceed.
