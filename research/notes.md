# Research Notes (internal — session d8a9b67c)

PII rule: no names, street addresses, APNs, or account identifiers appear in this repo or the site.
Property references use labels "Property A" (Cupertino, CA 95014) and "Property B" (San Francisco, CA 94122).

## Verification status legend
- **VERIFIED**: value read directly from an official source fetched this session.
- **USER-PROVIDED**: figure supplied by the user; not independently confirmable without parcel identifier (withheld).
- **UNVERIFIED / FLAGGED**: cannot confirm from an official source; value left blank or clearly labeled; listed on Flagged page.

---

## 1. Federal estate / gift / GST tax (VERIFIED)

| Item | Value | Source |
|---|---|---|
| Basic exclusion, deaths in 2026 | $15,000,000 | https://www.irs.gov/businesses/small-businesses-self-employed/estate-tax |
| Basic exclusion 2026 (OBBBA §70106) | $15,000,000, indexed for inflation after 2026 | https://www.irs.gov/pub/irs-drop/rp-25-32.pdf (§2.14) |
| Filing threshold 2026 (Form 706) | $15,000,000 | https://www.irs.gov/businesses/small-businesses-self-employed/frequently-asked-questions-on-estate-taxes |
| Top estate/gift rate | 40% (IRC §2001 rate schedule) | https://www.irs.gov/instructions/i706 |
| Applicable credit (unified credit) at $15M | $5,945,800 | https://www.irs.gov/instructions/i706 (Line 9a notes) |
| Annual gift exclusion 2026 | $19,000 per donee ($38,000 per couple) | https://www.irs.gov/businesses/small-businesses-self-employed/whats-new-estate-and-gift-tax |
| GST exemption 2026 | $15,000,000 | Rev. Proc. 2025-32 §2.14 |
| Portability (DSUE) | Must file Form 706 to elect, even below threshold | IRS estate-tax FAQ (above) |
| Law change | P.L. 119-21 (OBBBA, signed 2025-07-04) made $15M permanent + indexed | Rev. Proc. 2025-32 §1 |

Simplified large-estate estimate (flagged as simplified): federal tax ≈ $5,945,800 + 40% × (taxable estate − $15,000,000), ignoring deductions/adjustments.

## 2. California estate / inheritance / gift tax (VERIFIED)

| Item | Value | Source |
|---|---|---|
| CA estate tax return required for deaths on/after 2005-01-01 | No | https://www.sco.ca.gov/ardtax_estate_tax.html |
| State death tax credit (pick-up tax) | Eliminated 2005-01-01 (EGTRRA) | same |
| CA inheritance tax | Only for deaths before 1982-06-08 (legacy) | same |
| CA gift tax | Only for gifts before 1982-06-08 (legacy) | same |
| CA top income tax rate (context) | 13.3% (12.3% + 1% MHS over $1M) | https://www.ftb.ca.gov/about-ftb/data-reports-plans/summary-of-federal-income-tax-changes/index.html |
| Local inheritance/estate tax | None in California (no local estate tax) | SCO page (state administers; no local levy) |

## 3. Property tax — Prop 13 (VERIFIED)

| Item | Value | Source |
|---|---|---|
| Base rate | 1% of assessed value + voter-approved bonded debt | https://boe.ca.gov/proptaxes/pdf/lta25023.pdf (BOE LTA 2025/023) |
| Annual assessment growth cap | 2% (Art. XIII A §2(b)) | same; https://boe.ca.gov/proptaxes/pdf/rules/Rule460.pdf |
| Reassessment triggers | Change in ownership or new construction only | same |
| Decline-in-value relief | Proposition 8 rule (assess at lower FV) | BOE LTA 2025/023 |
| 2025 roll inflation factor | 1.02 (CCPI +2.514%, capped) | https://boe.ca.gov/proptaxes/pdf/lta24053.pdf |
| 2026 roll inflation factor | 1.02 | https://boe.ca.gov/proptaxes/pdf/lta26002.pdf |
| Historical factors 2015-2026 | 1.02 except 2016: 1.01525, 2021: 1.01036 (and2015: 1.01998) | LTA 2024/053 enclosure table |

**Line-by-line verification of user-provided assessment histories vs. BOE factors:**
- Property A (Cupertino): all 11 year-over-year changes 2015→2026 match official BOE factors exactly (±$1 rounding). VERIFIED as internally consistent with Prop 13 factor schedule.
- Property B (SF): 2017→2021 and 2023→2025 match; 2021→2022 grew 1.957% vs official 2.0% (≈$45 difference) — FLAG (minor, likely source rounding/exemption change).

## 4. Property tax rates — local (VERIFIED where noted)

| Item | Value | Source |
|---|---|---|
| SF secured rate FY 2026-27 | 1.18162182% | https://sftreasurer.org/property/secured-property-taxes (fetched 2026-11-06) |
| SF secured rate FY 2025-26 | 1.18268325% | same page history / SF TTC |
| SF first installment delinquent | Dec 10 (10% penalty); second Apr 10 | same |
| Santa Clara County tax rate book 2025-26 | Composite TRA rates ≈ 1.039%–1.241% (examples incl. 1.142%, 1.156%, 1.1786%, 1.2409%) | https://files.santaclaracounty.gov/exjcpb1531/2025-11/tax-rate-book-2025-2026.pdf |
| Property A exact TRA rate | UNVERIFIED — parcel ID withheld; cannot resolve TRA | flagged |
| Property A implied effective rate (2025 tax ÷ 2025 assessment) | 1.335% (user data) — above TRA base range; consistent only if direct/parcel assessments included | FLAG |
| Property B implied effective rate (2025) | 2.135% (user data) vs official 1.1827% — ~1.8× discrepancy | FLAG (possible multi-parcel/supplemental/direct charges; unresolvable without parcel ID) |

## 5. Proposition 19 — parent-child transfer (VERIFIED)

| Item | Value | Source |
|---|---|---|
| Effective | Transfers on/after 2021-02-16 | https://www.boe.ca.gov/prop19/ |
| Family-home exclusion requires | Transferor's principal residence + transferee occupies as principal residence (within 1 yr) + claim filed | BOE; https://www.boe.ca.gov/proptaxes/pdf/lta20061.pdf |
| Exclusion amount cap (transfers 2025-02-16 → 2027-02-15) | factored BYV + $1,044,586 (biennial FHFA indexation) | https://www.boe.ca.gov/news/2025/nr-25-02.htm |
| If FMV > cap | new BYV = FMV − adjusted exclusion amount (excess added) | BOE LTA / Rule 462.520 |
| If FMV ≤ cap | BYV unchanged (stays factored base) | same |
| Non-qualifying property (rental, second home) | Full reassessment to FMV | BOE prop19 page |
| Claim form | BOE-19-P, within 3 years of death/transfer (or before 3rd-party transfer) | https://www.boe.ca.gov/prop19/ |
| Homeowners' exemption claim | Within 1 year of transfer (BOE-100-H / BOE-266) | BOE prop19 checklist |
| Worked example source | Rule 462.520 examples | https://www.boe.ca.gov/proptaxes/pdf/rules/Rule462-520.pdf |

Critical unknown (FLAG): whether Property A is/will be the transferor's principal residence at death — determines Prop 19 eligibility. User data does not state current occupancy of Property A.

## 6. Stepped-up basis (VERIFIED)

| Item | Value | Source |
|---|---|---|
| Basis at death | FMV at date of death (IRC §1014) | IRS Pub 551: https://www.irs.gov/forms-pubs/about-publication-551 |
| Community property (CA) | Full step-up of entire property at first spouse's death (§1014(b)(6)) | Pub 551 |
| Documentation if no 706 filed | Appraised value at date of death | Pub 551 |
| Alternate valuation §2032 | Only if estate files Form 706 | https://www.irs.gov/instructions/i706 |

## 7. Capital gains / income tax (VERIFIED)

| Item | 2026 value | Source |
|---|---|---|
| LTCG 0% cap, single | $49,450 | Rev. Proc. 2025-32 §4.03 |
| LTCG 0% cap, MFJ | $98,900 | same |
| LTCG 15% cap, single | $545,500 | same |
| LTCG 15% cap, MFJ | $613,700 | same |
| 20% rate above those | yes | same |
| Top ordinary brackets 2026 | 37% over $768,700 (MFJ) / $640,600 (single) | Rev. Proc. 2025-32 §4.01 |
| NIIT | 3.8% on investment income > $200k/$250k MAGI | https://www.irs.gov/taxtopics/tc559 (topic exists; 2026 page — verify at filing) |
| CA top rate | 13.3% | FTB (see §2) |
| Prior-year LTCG reference (2025) | https://www.irs.gov/taxtopics/tc409 (still shows 2025 — flag if used for 2026) |

## 8. SALT deduction (VERIFIED)

| Item | Value | Source |
|---|---|---|
| SALT cap 2025 | $40,000 ($20k MFS), floors at $10,000 above $500k MAGI | https://www.irs.gov/publications/p530 |
| SALT cap 2026 | $40,400 (Rev. Proc. 2025-32 / OBBBA §70120) | https://www.irs.gov/pub/irs-access/p6079_accessible.pdf |
| Expiration | Cap reverts after 2029 (OBBBA sunsets provision) | OBBBA text (P.L. 119-21) |

## 9. Rent control / rental law (VERIFIED)

| Item | Value | Source |
|---|---|---|
| SF allowable increase 2026-03-01 → 2027-02-28 | 1.6% (60% Bay Area CPI), once/12 months, on base rent only | https://www.sf.gov/learn-about-rent-increases-san-francisco |
| Notice | 30 days (<10% increase), 90 days (>10%), +5 days if mailed | same |
| Banked increases | Permitted (Rule 4.12) | same |
| Prior-year SF increases | 2025: 1.4%, 2024: 1.7%, 2023: 3.6%, 2022: 2.3% (NON-official mirrors — corroborating only) | relisto/trimball etc. — not cited on site |
| AB 1482 cap | 5% + local CPI, max 10%; effective until 2030-01-01 | https://leginfo.legislature.ca.gov/faces/billTextClient.xhtml?bill_id=201920200AB1482 |
| AB 1482 just cause | After 12 months occupancy (24 mo if new tenant added) | same |
| AB 1482 SFR exemption | Single-family/condo owned by individual exempt (written notice required) | same; Cupertino AB 1482 flyer: https://www.cupertino.gov/files/assets/city/v/2/departments/documents/community-development/housing/ps-flyer-ab-1482-new-ca-la.pdf |
| Costa-Hawkins vacancy decontrol | Market rent reset allowed at turnover | Civ. Code §§1954.50–1954.535 (leginfo) |
| Cupertino local ordinance | Urgency Ordinance 19-2194 (just cause + large-increase limits, adopted 2019-12-17) | https://cupertino.legistar.com/LegislationDetail.aspx?From=RSS&ID=6034821 (status: verify current text) |
| SF prior rent-license requirement | Rent Increase License (housing inventory reporting) | sf.gov rent page |

AB 1482 2026-27 caps (8.8% SF region / 8.6% Santa Clara, eff. 2026-08-01) come from NON-official mirrors → FLAG, verify against DCA/BLS before citing on site.

## 10. Utilities (VERIFIED rates; user bills USER-PROVIDED)

### Property B — San Francisco (SFPUC, official rate schedule)
Source: https://www.sfpuc.gov/sites/default/files/accounts-and-services/Rates2023/RatesProp218_0323.pdf and https://www.sfpuc.gov/accounts-services/water-power-sewer-rates/proposed-water-sewer-rates-2026/proposition-218-notice

| Item | FY2025-26 (eff. 2025-07-01) | FY2026-27 proposed (eff. 2026-07-01) |
|---|---|---|
| SFR water Tier 1 (first 4 units) | $11.40/CCF | $12.20/CCF |
| SFR water Tier 2 (additional) | $12.66/CCF | $13.05+ (per notice table) |
| Multi-family water, first 3 units/dwelling | $11.24/CCF | see notice |
| SFR wastewater volumetric | $18.72/CCF (FY26) | see notice |
| Wastewater service charge (fixed) | $5.76/mo | see notice |

- User-reported SF water bill $330–400/mo for 3 units → USER-PROVIDED, UNVERIFIED (depends on usage/flow factors); official calculator: https://sfpuc.gov/bill-calculator (verify path) — FLAG.

### Property A — Cupertino (providers depend on exact location; official tariffs fetched)
Provider map (official): https://www.cupertino.gov/Residents/Utilities — California Water Service (purple area) / San Jose Water (green area); sewer: Cupertino Sanitary District or Sunnyvale Sanitary; electric: SVCE + PG&E.

| Provider | Rate (official) | Source |
|---|---|---|
| SJW residential 0–6 CCF | $4.9692/CCF eff. 2026-07-01 (prior $4.7924) | https://www.sjwater.com/media/oycbyo3o/adv-628-web.pdf |
| SJW 6–12 CCF | $7.4167/CCF | same |
| SJW 12+ CCF | $14.1659/CCF | same |
| SJW avg bill, 10 CCF, 3/4" meter | $141.73/mo eff. 2026-07-01 | same |
| Cal Water (Los Altos/Santa Clara terr.) Tier 1 1-6 CCF | $2.7015/CCF (+ $10.7870 Tier 2) | https://www.calwater.com/wp-content/uploads/2025/12/20260101_Residential_Metered_Service_LAS.pdf |
| Cal Water 2026 surcharge note | +0.35% revenue increase eff. 2026-01-01 | same |

- User-reported Property A water $100–150/mo → consistent with SJW average bill ($141.73) — partially corroborated; final verification requires provider-by-map (FLAG).
- Sewer provider rate: Cupertino Sanitary District / Sunnyvale Sanitary — not fetched (FLAG, link-only).

### Electric / solar (USER-PROVIDED)
- User: solar produces +$10–20/mo credit; usually $0 electric cost → USER-PROVIDED, UNVERIFIED.
- Context source for NEM rules: PG&E / CPUC (link-only; not fetched → FLAG).

## 11. Insurance (partial VERIFIED; ZIP-level FLAGGED)

| Item | Value | Source |
|---|---|---|
| CA statewide avg written premium, Homeowners Multi-Peril (2008–2023 pooled) | $1,176 | CDI Part I xlsx (fetched): https://www.insurance.ca.gov/0400-news/0200-studies-reports/0250-homeowners-study/ → A-Part-I-Data-Summary.xlsx |
| Dwelling-Fire owner-occupied (pooled) | $798 | same |
| Dwelling-Fire tenant-occupied (pooled) | $601 | same |
| Condo (pooled) | $537 | same |
| Renters (pooled) | $190 | same |
| Statewide avg Coverage A (2018→2023) | $230,138 → $324,973 | SB 824 xlsx (fetched) |
| ZIP 95014 avg premium | NOT EXTRACTED — left blank + FLAGGED | report page (above) |
| ZIP 94122 avg premium | NOT EXTRACTED — left blank + FLAGGED | report page (above) |
| 2026 comparison tool | https://interactive.web.insurance.ca.gov/apex_extprd/f?p=111:20 (official quote tool; wildfire surcharges 15%–300%+ not shown) | CDI |
| User estimates | ~$1,500/yr each property → USER-PROVIDED, UNVERIFIED | — |

Note: pooled averages span 2008–2023 and understate current-year costs — flagged on site.

## 12. Market rent benchmarks (VERIFIED official; projections flagged)

| Item | Value | Source |
|---|---|---|
| HUD FY2026 FMR, Santa Clara County 2BR | $3,483/mo (eff. 2025-10-01) | https://www.huduser.gov/portal/datasets/fmr.html (Federal Register notice: 2025-16060) |
| HUD FY2026 FMR, Santa Clara County 1BR/3BR/4BR | $2,982 / $4,602 / $5,010 | HUD data mirrors (flag: confirm on huduser before final cite) |
| HUD FY2027 Santa Clara 2BR (eff. 2026-10-01) | $3,272 (−6.1% YoY) | HUD (mirror cite — FLAG verify on huduser) |
| SF FMR FY2026 2BR | NOT FETCHED — blank + FLAG | huduser.gov |
| User rent, Property B | ~$7,150/mo (2 units) + 3rd unit owner-occupied | USER-PROVIDED |

## 13. Housing value projections — anchors (VERIFIED official FHFA figures)

Source: https://www.fhfa.gov/document/d/hpi/fhfa-house-price-index-report-2025q3 (and 2025q2)

| Metric | Value |
|---|---|
| CA purchase-only HPI 1-yr (to 2025Q3) | −0.34% … +0.38% (series-dependent; report shows CA 1-yr 0.38%, 5-yr 35.29%–41.38%, since 1991Q1 +318.6%–320.1%) |
| CA CAGR since 1991Q1 (computed from FHFA +320.05%) | ≈ 4.2%/yr over ~34.75 yrs |

Projection scenarios used on site (clearly labeled ASSUMPTIONS):
- Low 2.5% / Base 4.2% (FHFA since-1991 CAGR) / High 6.0% CAGR.
- Not predictions; FHFA historical anchors cited.

## 14. Pending law changes / watchlist

| Item | Status | Source |
|---|---|---|
| Death Tax Repeal Act (S.587, Thune; H.R.1301, Feenstra) | Introduced 2025-02-13; Senate Finance / House Ways & Means; would repeal federal estate & GST tax | https://www.congress.gov/bill/119th-congress/senate-bill/587 |
| H.R.25 FairTax Act | Would also repeal estate/gift tax; introduced only | congress.gov |
| CA SB-284 (Seyarto) — Prop 19 family-transfer flexibility | Passed Senate 38-0 (2025-05-29); held in Assembly Rev&Tax/Approps since 2025-07-14; no 2026 action recorded | https://leginfo.legislature.ca.gov/faces/billStatusClient.xhtml?bill_id=202520260SB284 |
| Prop 19 repeal initiative (2025-0017) | Failed to qualify for 2026 ballot | CA SOS memo https://elections.cdn.sos.ca.gov/ccrov/2026/may/26138jh.pdf (URL from search — FLAG: fetch before citing) |
| OBBBA estate exclusion | Enacted: $15M permanent, indexed 2027+ | Rev. Proc. 2025-32 |
| SALT cap | $40,000 (2025) → $40,400 (2026), high-income phase-down to $10k floor | IRS Pub 530 / Rev. Proc. 2025-32 |
| AB 1482 sunset | Repeals 2030-01-01 (bill adds-and-repeals) | leginfo AB 1482 text |
| SF rent CPI increases | Annual (next window 2027-03-01) | sf.gov |

## 15. Inheritance process — sources (VERIFIED)

- Living trust mechanics, successor trustee duties, no-probate: https://santaclara.courts.ca.gov/self-help/self-help-topics/self-help-probate/probate-medicalfinancialend-life-issues/living-trusts
- Wills & trusts overview: https://www.occourts.org/self-help/self-help-probate/wills-trusts
- Change in ownership / assessor notification: BOE + county assessor (SCC: https://www.sccassessor.org/ — link)
- Prop 19 claim: BOE-19-P (https://www.boe.ca.gov/prop19/)
- Homeowners' exemption: BOE-100-H, within 1 year of transfer
- Death of joint tenant / affidavit: BOE-502-D within 150 days (source: BOE forms index https://www.boe.ca.gov/forms/)
- Federal: Form 706 only if > $15M or portability election (IRS)
- Step-up documentation: IRS Pub 551

## 16. User-provided data — internal consistency audit (computed this session)

### Property A (Cupertino 95014) — USER-PROVIDED
- Value Nov 2026: $3,100,000.
- Assessment history: matches BOE factors exactly every year 2015→2026 (VERIFIED consistency).
- Tax history YoY % as printed by user vs computed:
  - 2017: printed +2%, computed −0.5% ($6,414→$6,383) — **FLAG**
  - 2019: printed +2.8%, computed +0.4% ($6,540→$6,565) — **FLAG**
  - All other years match within 0.1pp.
- 2026 tax: blank ("—") — left blank, FLAG (FY26-27 bill expected; fill from bill when available).
- Implied 2025 effective rate 1.335% vs county TRA range 1.039–1.241% — FLAG (direct charges likely; exact TRA unresolvable without parcel ID).

### Property B (SF 94122) — USER-PROVIDED
- Value: $1,800,000 (Nov 2026); 3 units; ~$7,150/mo from 2 units; 3rd unit owner-occupied.
- Assessment history: matches BOE factors except 2021→2022 1.957% vs 2.0% (≈$45) — minor FLAG.
- Tax history YoY as printed vs computed:
  - 2022: printed +2%, computed −6.2% ($2,247→$2,107) — **FLAG (internal inconsistency)**
  - 2023: printed +1%, computed +3.4% ($2,107→$2,179) — **FLAG (internal inconsistency)**
  - 2018 jump +18.4% — plausible supplemental/ownership event; unverifiable — FLAG.
  - Other years match.
- Implied 2025 effective rate 2.135% vs official 1.1827% — **FLAG (major discrepancy)**.

### User operating-cost estimates (all USER-PROVIDED / UNVERIFIED)
- A: water $100–150/mo (partially corroborated by SJW avg bill $141.73); solar credit +$10–20/mo; insurance ~$1,500/yr; maintenance "lower than SF" (no figure → blank).
- B: water $330–400/mo (3 units); electric $30–70/mo; insurance ~$1,500/yr.

## 17. Decision-analysis framework (derived; all inputs sourced above)

Scenarios at inheritance (~2045 assumed year — FLAG as assumption):
1. **Keep / live in A**: Prop 19 exclusion possible ONLY if transferor's + heir's principal residence. New BYV = max(factored BYV, FMV − $1,044,586*). *future adjusted amount unknown (biennial FHFA indexation) → blank/assumption.
2. **Rent A (heir lives elsewhere)**: no exclusion → full reassessment to FMV. Property tax jumps from ~$10.7k (projected status quo) to ~$76k–90k/yr (projected) — magnitude of decision.
3. **Sell A**: stepped-up basis ≈ FMV at death → capital gains ≈ post-death appreciation only; costs ~6% (ASSUMPTION, no official source — flagged); invest proceeds.

SF (Property B) as current residence + rent engine: SF Rent Board 1.6% cap on occupied units; vacancy decontrol at turnover (Costa-Hawkins); AB 1482 backstop.

## 18. Dead ends (do not retry)
- curl/python downloads from insurance.ca.gov blocked (TLS reset) — use fetch_page.
- sfrb.org direct paths 404 — use sf.gov.
- openbook.sfgov.org rate-history PDF is download-only — use sftreasurer.org page (has current rate inline).
- IRS newsroom 2026-inflation URL 404 — use Rev. Proc. 2025-32 PDF.
- boe.ca.gov pub103.pdf 404.
- bash cannot reach non-allowed hosts (only github/npm/pypi) — external link checks must use fetch_page.
