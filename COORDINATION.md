# Shared task board

| Task | Status | Owner/session | File scope | Notes |
|---|---|---|---|---|
| Research, build, verify, and publish inheritance decision dashboard | in progress | `arena/715670b0-cupertino3` (Arena session) | All project files except `.git/` | Initial claim; repository had only README.md and no prior coordination board. Site/build/verification complete; PR, merge, and Pages deployment remain. |

## Activity log

- 2026-11-06 — Claimed the end-to-end dashboard task after reviewing the empty task board. No other active claims were present. Claim committed as `08ef969` and pushed to the session branch. The initial attempt to rebase before first push found no remote session branch; the claim was then pushed to establish it.
- 2026-11-06 — Built a static, multi-page privacy-first dashboard: executive summary, decision framework, projection model, inheritance process, tax/property law, operating costs, Flagged for Review, and official sources. No parcel numbers, names, addresses, household property values, rents, utility bills, insurance guesses, or other household-specific financial figures are published. Unsupported figure cells remain blank.

## Sources reviewed and verification performed

- Federal estate/gift tax: [IRS estate-tax FAQs](https://www.irs.gov/businesses/small-businesses-self-employed/frequently-asked-questions-on-estate-taxes), [IRS 2026 tax law update](https://www.irs.gov/newsroom/working-families-tax-cuts-individuals-and-workers), [IRS Rev. Proc. 2025-32](https://www.irs.gov/pub/irs-drop/rp-25-32.pdf), [IRS gift-tax FAQs](https://www.irs.gov/businesses/small-businesses-self-employed/frequently-asked-questions-on-gift-taxes), and [Form 706 instructions](https://www.irs.gov/instructions/i706). Verified the 2026 federal basic exclusion of $15,000,000, inflation indexing after 2026, 2026 annual gift exclusion of $19,000 per donee, estate return framework, portability, and general inherited basis treatment.
- California property tax / Prop. 19: [BOE Publication 29](https://www.boe.ca.gov/proptaxes/pdf/pub29.pdf), [BOE 2025 Prop. 19 exclusion notice](https://www.boe.ca.gov/news/2025/nr-25-02.htm), [BOE revised forms circular](https://www.boe.ca.gov/proptaxes/pdf/lta22025.pdf), and [Santa Clara County Assessor Prop. 19 guidance](https://asr.santaclaracounty.gov/tax-savings/transferring-your-assessed-value/parent-to-child-2). Verified the 2025–2027 indexed amount ($1,044,586), principal-residence/use and value-test framework, and Prop. 13 annual inflation cap, while flagging stale/ambiguous county wording.
- California legislation: [BOE 2026/013](https://boe.ca.gov/proptaxes/pdf/lta26013.pdf) and [SB 293 chaptered text](https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202520260SB293) reviewed for the narrow wildfire/probate claim extension. [SB 284 status](https://leginfo.legislature.ca.gov/faces/billStatusClient.xhtml?bill_id=202520260SB284) reviewed; its record showed held in committee/under submission on July 14, 2025, and it is not presented as enacted law.
- Insurance / utilities: [California DOI 2026 comparison tool](https://interactive.web.insurance.ca.gov/apex_extprd/f?p=111:20), [DOI residential insurance guide](https://www.insurance.ca.gov/01-consumers/105-type/95-guides/03-res/res-ins-guide.cfm), and [SFPUC rates](https://www.sfpuc.gov/accounts-services/water-power-and-sewer-rates). The DOI confirms tool premiums are hypothetical and exact premiums require insurer-specific quotes; no house-specific premium is asserted. SFPUC rate schedule is linked, but household bill amounts remain blank.
- Rental / sale taxation: [IRS Publication 527](https://www.irs.gov/publications/p527) and [IRS Publication 523](https://www.irs.gov/publications/p523).
- California inheritance tax background: [California Legislative Analyst’s Office](https://lao.ca.gov/BallotAnalysis/Initiative/2017-038); state-level inheritance-tax status is distinguished from federal estate tax, fiduciary income tax, capital gains, and property tax.
- Verification checks: all local website links resolve within the repository; every data row in every HTML table has at least one HTTPS official-source link; scanned public pages for supplied household values/ZIP codes and found no matches; `git diff --check` clean. Research pages inspected directly using official-source pages/PDFs. The GitHub Pages workflow copies only `index.html`, `pages/`, and `assets/` into the deployment artifact so coordination, README, and workflow files are not published. A separate GitHub Actions validator (`scripts/validate_site.py`) checks internal links, official HTTPS sources on every table row, approved official domains, and document structure on pushes and pull requests; it passes locally.

## Flagged items published on the site

- Property histories, tax bills, rents, insurance guesses, utilities/solar credits, and repair estimates are private, unverified, and withheld. ZIP/city alone does not confirm a parcel or tax-rate area; no parcel-specific tax comparison or forecast is claimed.
- Santa Clara County’s Prop. 19 explanatory page includes legacy/ambiguous wording: it says the allowance is adjusted annually while BOE’s 2025 notice says the amount is published every other year, and one sentence renders “At least of the children” without a number. Users are directed to BOE materials and to obtain assessor confirmation.
- Future 2040–2050 laws, assessed values, market values, insurance premiums, and utility costs are unknown; the numeric projection cells are blank rather than inferred.
- Official legislative note: SB 284 is presented only as a proposal with its recorded 2025 committee status; SB 293 is described as a narrow chaptered wildfire/probate exception, not general inheritance relief.

## Deployment record

- Pull request: pending.
- Merge: pending.
- GitHub Pages deployment: pending.
