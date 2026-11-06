# T4 — Property Tax & Assessment Data (official sources)

Verification date: 2026-11-06.

## County secured tax rates

| Item | Value | Status | Official source |
|---|---|---|---|
| San Francisco secured rate FY 2026-27 | **1.18162182%** | VERIFIED (fetched 2026-11-06) | [SF TTC — Secured Property Taxes](https://sftreasurer.org/property/secured-property-taxes) |
| SF secured rate FY 2025-26 | 1.18268325% | VERIFIED (page history) | same |
| SF 1st installment delinquent | Dec 10 (10% penalty); 2nd: Apr 10 | VERIFIED | same |
| SF supplemental after change of ownership | Assessor reappraises; supplemental bill on difference | VERIFIED | same |
| Santa Clara County tax rate book 2025-26 | Composite TRA rates ≈ **1.039%–1.241%** (examples: 1.03880%, 1.14200%, 1.15600%, 1.17860%, 1.24090%) | VERIFIED (sampled) | [SCC Tax Rate Book 2025-2026](https://files.santaclaracounty.gov/exjcpb1531/2025-11/tax-rate-book-2025-2026.pdf) |
| SCC bill example (TRA 017-025) | AV $616,984 − $7,000 homeowner exemption → tax $7,194.92 (2025-26) | VERIFIED (sample) | SCC tax bill sample |
| SCC "Where My Taxes Go" lookup | per-TRA breakdown | VERIFIED (tool exists) | [payments.sccgov.org/PropertyTaxAllocation](https://payments.sccgov.org/PropertyTaxAllocation/Home) |
| Property A exact TRA rate | — | **UNVERIFIED — parcel ID withheld; cannot resolve TRA** | use SCC tool with own APN (internal) |
| Property A implied effective rate (2025: $7,207 ÷ $539,743) | 1.335% (user data) | USER-PROVIDED; above TRA base range → likely includes direct/parcel assessments | FLAG |
| Property B implied effective rate (2025: $2,439 ÷ $114,248) | 2.135% (user data) | USER-PROVIDED; ≈1.8× official SF rate → **IRREGULARITY, FLAG** | FLAG |

## Assessment histories (user-provided) — consistency audit vs official BOE factors

### Property A — Cupertino 95014 (USER-PROVIDED; year-over-year changes VERIFIED against BOE factor table)

| Year | Tax (user) | Δ tax | Assessment (user) | Δ AV | Official BOE factor | Match? |
|---|---|---|---|---|---|---|
| 2014 | $5,965 | — | $440,305 | — | — (base) | — |
| 2015 | $6,130 | +2.8% ✓ | $449,101 | +2.0% | 1.01998 | ✓ |
| 2016 | $6,414 | +4.6% ✓ | $455,949 | +1.5% | 1.01525 | ✓ |
| 2017 | $6,383 | **printed +2%, computed −0.5% → FLAG** | $465,067 | +2.0% | 1.02 | ✓ |
| 2018 | $6,540 | +2.5% ✓ | $474,368 | +2.0% | 1.02 | ✓ |
| 2019 | $6,565 | **printed +2.8%, computed +0.4% → FLAG** | $483,854 | +2.0% | 1.02 | ✓ |
| 2020 | $6,565 | +0.0% ✓ | $493,530 | +2.0% | 1.02 | ✓ |
| 2021 | $6,662 | +1.5% ✓ | $498,642 | +1.0% | 1.01036 | ✓ |
| 2022 | $6,755 | +1.4% ✓ | $508,614 | +2.0% | 1.02 | ✓ |
| 2023 | $6,917 | +2.4% ✓ | $518,786 | +2.0% | 1.02 | ✓ |
| 2024 | $7,003 | +1.2% ✓ | $529,161 | +2.0% | 1.02 | ✓ |
| 2025 | $7,207 | +2.9% ✓ | $539,743 | +2.0% | 1.02 | ✓ |
| 2026 | — (blank) | **FLAG** | $550,537 | +2.0% | 1.02 | ✓ |

Assessment column: **all 11 YoY changes match official BOE inflation factors exactly** (±$1 rounding) — VERIFIED consistency.

### Property B — SF 94122 (USER-PROVIDED)

| Year | Tax (user) | Δ tax | Assessment (user) | Δ AV | BOE factor | Match? |
|---|---|---|---|---|---|---|
| 2016 | $1,675 | — | $96,557 | — | — | — |
| 2017 | $1,740 | +3.9% ✓ | $98,488 | +2.0% | 1.02 | ✓ |
| 2018 | $2,061 | +18.4% ✓ (jump — FLAG: unexplained) | $100,456 | +2.0% | 1.02 | ✓ |
| 2019 | $2,134 | +3.5% ✓ | $102,465 | +2.0% | 1.02 | ✓ |
| 2020 | $2,197 | +3.0% ✓ | $104,513 | +2.0% | 1.02 | ✓ |
| 2021 | $2,247 | +2.3% ✓ | $105,595 | +1.0% | 1.01036 | ✓ |
| 2022 | $2,107 | **printed +2%, computed −6.2% → FLAG** | $107,662 | **+1.96% (vs 2.0%; ≈$45 off) → minor FLAG** | 1.02 | ~ |
| 2023 | $2,179 | **printed +1%, computed +3.4% → FLAG** | $109,814 | +2.0% | 1.02 | ✓ |
| 2024 | $2,315 | +6.2% ✓ | $112,008 | +2.0% | 1.02 | ✓ |
| 2025 | $2,439 | +5.3% ✓ | $114,248 | +2.0% | 1.02 | ✓ |

Sources for audit: BOE LTA 2024/053 factor table (VERIFIED), user-provided tables (internal).

## Value data (user-provided, unverifiable without parcel ID)

| Item | Value | Status |
|---|---|---|
| Property A estimated value Nov 2026 | $3,100,000 | USER-PROVIDED (AVM-type estimate; not an official assessment) |
| Property B estimated value Nov 2026 | $1,800,000 | USER-PROVIDED |
| Property B units / rent | 3 units; ~$7,150/mo from 2 units; 3rd owner-occupied | USER-PROVIDED |
