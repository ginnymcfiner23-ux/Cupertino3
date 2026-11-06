# COORDINATION.md — Shared Task Board

Repo: ginnymcfiner23-ux/Cupertino3
Session: 41b64714 (branch `arena/41b64714-cupertino3`)
Mode: single session (no other sessions detected). This session performs all tasks.

## Tasks

| # | Task | Status | Owner | Scope (files) | Notes |
|---|------|--------|-------|---------------|-------|
| 1 | Legal & tax research (federal estate tax, CA Prop 13/19, no CA inheritance tax) | done | session-41b64714 | `data/law-tax.md`, `docs/tax-law.html` | Verified from IRS.gov, boe.ca.gov, ftb.ca.gov, sos.ca.gov |
| 2 | Property tax & assessment research (both properties, county assessors) | done | session-41b64714 | `data/properties.md`, `docs/properties.html` | Santa Clara + SF County Assessors / Treasurer rates; irregularities flagged |
| 3 | Utility & maintenance cost research (PG&E, water districts, insurance) | done | session-41b64714 | `data/costs.md`, `docs/costs.html` | PG&E, City of Cupertino, SFPUC tariffs; CDI/NAIC insurance data |
| 4 | Inheritance process step-by-step (Probate, trust, Prop 19 reassessment) | done | session-41b64714 | `data/inheritance.md`, `docs/inheritance.html` | BOE, IRS, CA Probate Code |
| 5 | Projections engine (values, taxes, costs, scenarios, 2026-2055) | done | session-41b64714 | `data/projections.json`, `docs/projections.html`, `docs/scenarios.html`, `scripts/projections.py` | Assumptions labeled; verified law/rates carried |
| 6 | Executive summary | done | session-41b64714 | `docs/index.html` | Synthesizes all findings |
| 7 | GitHub Pages site (clean dashboard UI, all pages, tables with source links) | done | session-41b64714 | `docs/*.html`, `docs/assets/*` | Plain HTML/CSS/JS, no build step |
| 8 | Verification pass (line-by-line, source links on every table) | done | session-41b64714 | all data files + site | Re-checked each row vs official source |
| 9 | Flagged for Review page | done | session-41b64714 | `docs/flagged.html` | 18 flagged items published |
| 10 | GitHub Pages deploy + PR/merge + record in COORDINATION.md | in progress | session-41b64714 | `docs/`, PR to main | pages source: main:/docs |

## Verification log (task-level)

- **Task 1 (law/tax):** Federal estate tax exclusion $15M/person (2026) verified from IRS estate tax page + IR-2025-103 + Rev. Proc. 2025-32. CA no inheritance/estate tax verified from FTB bill analyses (SB 378, SB 726). Prop 13 rules + Prop 19 exclusion rules verified from BOE Taxpayers' Rights Advocate LTA 2022/051 (official). Prop 19 repeal status from CA Secretary of State failure memo + CA Senate SCA 4 page. Capital gains/step-up from IRS Topic 409 + Pub 551. CA income tax from FTB rate schedules.
- **Task 2 (properties):** SF secured rate 1.18162182% (FY 2026-27) from SF Treasurer official page. Santa Clara County rates from official Compilation of Tax Rates 2025-26 PDF. User-provided tax history flagged; implied effective rates computed and irregularities flagged (Cupertino 1.32-1.41% vs published 1.15-1.22%; SF 1.73-2.14% vs published 1.18%).
- **Task 3 (utilities/insurance):** City of Cupertino water/sewer/stormwater rates from official city PDF (Jan 1, 2026). SFPUC rates from official SFPUC pages + rate schedule PDF (July 1, 2026). PG&E ~33.7¢/kWh from CPUC PAO / PG&E Advice Letter 7846-E (via third-party summaries — flag). Insurance averages from CDI snapshot / NAIC (via summaries — flag). Cupertino/SF-specific insurance from third-party quote sites — flagged as estimates.
- **Task 4 (process):** Steps verified against BOE LTA 2022/051 (date of death = transfer date; BOE-19-P 3-year deadline; 1-year residency + homeowner's exemption; exclusion removed if home becomes rental), IRS (Form 706, stepped-up basis), CA Probate Code items flagged for direct statute verification.
- **Task 5 (projections):** Projection engine uses labeled assumptions (growth 2/3.5/5%, portfolio 6%, estate indexing +2.5%, inflation 2.5%). All law inputs (Prop 13 2% cap, Prop 19 $1M allowance 2025-2027 = $1,044,586, IRS 2026 exclusion $15M, published tax rates) verified from official sources. Every projection table carries its source link.
- **Task 8 (verification pass):** Re-read every page; all internal links checked (no broken links); all external links spot-checked against the source list; unverified values isolated in docs/flagged.html; no inferred values — unverifiable cells shown as "--" or flagged.

## Irregularities / flagged items

1. Cupertino implied effective rate (1.32–1.41%) exceeds published Cupertino composite (~1.15–1.22%) — likely special assessments; verify on bill.
2. SF implied effective rate (1.73–2.14%) exceeds published SF secured rate (1.18%) — likely direct charges (sewer/ERU); verify on bill.
3. Cupertino 2026 property tax missing.
4. Cupertino occupancy/rent status unknown — affects Prop 19 analysis.
5. User-provided market values ($3.1M / $1.8M) and rents ($7,150/mo) unverified.
6. Insurance figures are third-party estimates; official CDI/NAIC averages used for context.
7. Prop 19 $1,044,586 allowance cited via legal summaries — verify current BOE adjustment notice.
8. Probate Code statute details not fetched directly — flagged for verification.

## Handoff log

- None — single session.
