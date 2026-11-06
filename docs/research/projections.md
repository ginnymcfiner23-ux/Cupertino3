# T8 — Projections: Value, Taxes, Costs, Sell-vs-Rent-vs-Live (MODEL OUTPUTS)

> **ALL FIGURES ON THIS PAGE ARE MODEL PROJECTIONS, NOT VERIFIED FACTS.**
> Built by `docs/research/build_projections.py` (deterministic; re-runnable).
> Input assumptions are flagged; verified legal anchors are cited.

## Assumptions register

| Assumption | Value | Status | Anchor/source |
|---|---|---|---|
| Property A value Nov 2026 | $3,100,000 | USER-PROVIDED | internal |
| Property B value Nov 2026 | $1,800,000 | USER-PROVIDED | internal |
| Property A 2026 assessed value | $550,537 | USER-PROVIDED (matches BOE 1.02 factor — VERIFIED consistency) | BOE LTA 2026/002 |
| Home value CAGR — low/base/high | 2.5% / 4.2% / 6.0% | ASSUMPTION | base = FHFA CA HPI since-1991Q1 ≈ +320% ≈ 4.2%/yr (VERIFIED report figure); low/high are scenario spreads |
| Assessed-value growth | 2.0%/yr | VERIFIED LAW (Prop 13 cap) | BOE LTA 2024/053 |
| Property A tax rate (model) | 1.335% | USER-IMPLIED (2025 tax ÷ 2025 AV) — FLAG (above county TRA range; direct charges suspected) | SCC tax rate book |
| Property B tax rate (model) | 1.18162182% | VERIFIED (SF FY2026-27 rate) | sftreasurer.org |
| Prop 19 adjusted exclusion | $1,044,586 | VERIFIED for transfers 2025-02-16→2027-02-15; **held flat beyond 2027 in model — FLAG** (biennial FHFA indexation) | BOE NR 2025-02 |
| Selling costs | 6% of price | ASSUMPTION — no official source (commission norms) — FLAG | — |
| Nominal investment return | 7%/yr | ASSUMPTION — no official source — FLAG | — |
| Long-run inflation | 2.5%/yr | ASSUMPTION — FLAG | — |
| Rent growth beyond current window | 2.5%/yr | ASSUMPTION (current SF window is 1.6% — VERIFIED) | sf.gov |
| Inheritance year modeled | 2040 and 2050 (user said ~2040–2050) | USER-PROVIDED window | — |
| Property A market rent (if let) | — | **NOT ESTIMATED — blank + FLAG** (no official market-rent source; HUD FMR ≠ market rent) | — |

## 1. Property A value projections (from $3.1M, Nov 2026)

| Year | Low 2.5% | Base 4.2% | High 6.0% |
|---|---|---|---|
| 2030 | $3,421,820 | $3,654,539 | $3,913,679 |
| 2036 | $3,968,262 | $4,677,770 | $5,551,628 |
| 2040 | $4,380,219 | $5,514,546 | $7,008,802 |
| 2045 | $4,955,816 | $6,774,049 | $9,379,358 |
| 2050 | $5,607,050 | $8,321,219 | $12,551,697 |

(Property B same scenarios from $1.8M — see projections.csv.)

## 2. Status-quo property tax projections (no transfer; 2% AV cap; model rate)

**Property A** (AV $550,537 → 2% growth; tax at user-implied 1.335%):

| Year | Assessed value | Projected tax |
|---|---|---|
| 2026 | $550,537 | $7,350 |
| 2030 | $595,919 | $7,956 |
| 2040 | $726,422 | $9,698 |
| 2050 | $885,504 | $11,821 |

**Property B** (AV $114,248 (2025) → 2% growth; tax at official SF 1.18162182%):

| Year | Assessed value | Projected tax |
|---|---|---|
| 2026 | $116,533 | $1,377 |
| 2040 | $153,908 | $1,819 |
| 2050 | $187,546 | $2,216 |

## 3. Inheritance-year reassessment scenarios (THE decision lever; base 4.2% CAGR)

| Year | Projected FMV | Status-quo tax (if it existed) | Prop 19 EXCLUSION (heir occupies) new BV → tax | NO EXCLUSION (heir doesn't occupy / not transferor PR) new BV → tax |
|---|---|---|---|---|
| 2040 | $5,514,546 | $9,698 | $4,469,960 → **$59,674/yr** | $5,514,546 → **$73,619/yr** |
| 2050 | $8,321,219 | $11,821 | $7,276,633 → **$97,143/yr** | $8,321,219 → **$111,088/yr** |

Model math: exclusion new BV = FMV − $1,044,586 (flat; future adjusted amount unknown → FLAG). Even with the exclusion, tax jumps ~6–8× vs status quo; without it, ~7.6–9.4×. **If Property A is not the transferor's principal residence at death, exclusion is unavailable regardless of heir behavior (FLAG — occupancy unknown).**

## 4. Federal estate tax scenarios (verified rates; CA = $0 VERIFIED)

Simplified formula: tax = $5,945,800 + 40% × (estate − $15,000,000), for estates > $15M (credit = tax on $15M under §2001 schedule; ignores deductions → FLAG as simplified).

| Taxable estate | Federal tax | Effective rate | CA estate/inheritance tax |
|---|---|---|---|
| $10,000,000 | $0 | 0% | $0 |
| $15,000,000 | $0 | 0% | $0 |
| $20,000,000 | $7,945,800 | 39.7% | $0 |
| $30,000,000 | $11,945,800 | 39.8% | $0 |
| $40,000,000 | $15,945,800 | 39.9% | $0 |

Watchlist: S.587/H.R.1301 would repeal federal estate/GST tax entirely (pending). OBBBA indexed the $15M threshold from 2027 — future thresholds grow with CPI (model not extended → FLAG).

## 5. Live vs Rent vs Sell — Property A at inheritance (framework)

Stepped-up basis (VERIFIED IRC §1014): sale soon after death → **gain ≈ post-death appreciation only**; federal LTCG 0/15/20% + NIIT 3.8% + CA ordinary rates to 13.3% apply only to that slice.

| Option | Key economics (model) | Key risks/flags |
|---|---|---|
| **Live in A** (Prop 19) | Keep AV path if FMV ≤ cap — but FMV ≫ cap → new BV = FMV − $1.04M; 2040 tax ≈ $59.7k/yr vs status-quo $9.7k. Utility costs user-estimated $100–150 water, ~$0 electric. Gives up nothing on B (B continues:2 units rented ≈ $7,150/mo + live in 3rd) | Requires transferor PR + heir occupancy + BOE-19-P within 3 yrs + homeowner's exemption within 1 yr. Opportunity cost: A's equity (≈$5.5M in 2040) stays in housing |
| **Rent A** (heir stays in B) | **No Prop 19 exclusion** (heir doesn't occupy) → full FMV reassessment: 2040 tax ≈ $73.6k/yr. Rental income: **no official market-rent figure → blank/FLAG**. AB 1482 + Cupertino Ord. 19-2194 cap increases (5%+CPI ≤10%); vacancy decontrol at turnover (Costa-Hawkins) | Highest property-tax drag; rent must clear $73.6k tax + water/sewer/insurance/maintenance before profit — cannot compute without market rent (FLAG) |
| **Sell A** | Net after 6% costs at 2040 base CAGR: ≈ $5.18M; invested 7% → ≈ $10.2M in 10 yrs (ASSUMPTIONS). Tax hit ≈ LTCG only on post-death appreciation (stepped-up basis) | Selling costs/return are assumptions (FLAG); loses the asset + Prop 13 base forever; market-timing risk |
| **Hold B unchanged** (common to all) | B continues ≈ $7,150/mo rent (user), SF 1.6% cap on occupied units (VERIFIED), vacancy decontrol at turnover; B status-quo tax ≈ $1.4k/yr (official rate) | SF irregularity: user's implied 2.135% effective rate vs official 1.1827% → FLAG (reconcile against actual bill) |

**Ranking on purely modelled cash economics at 2040 (base case):** cannot be completed to a single ranking because Property A's market rent is deliberately left blank (no official source) — the site shows the cost side of each option and the verified decision levers, with the rent column flagged. This follows the no-inference rule.

## 6. Files

- `docs/research/projections.csv` — 25 years × 3 scenarios, both properties
- `docs/research/projections_inheritance.csv` — 2040/2050 reassessment scenarios
- `docs/research/projections_estate.csv` — estate-tax table
- `docs/research/build_projections.py` — source of truth (re-run to regenerate)
