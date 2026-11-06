#!/usr/bin/env python3
"""Projection model for Cupertino3 decision analysis.
All outputs are MODEL PROJECTIONS with stated assumptions — not verified facts.
Writes docs/research/projections.csv and prints summary tables.
"""
import csv

# ---- Assumptions (all flagged on site) ----
A_VALUE_2026 = 3_100_000.0     # user-provided Nov 2026 estimate
B_VALUE_2026 = 1_800_000.0     # user-provided Nov 2026 estimate
A_AV_2026 = 550_537.0          # user-provided 2026 assessment (matches BOE 1.02 factor)
B_AV_2025 = 114_248.0          # user-provided 2025 assessment

G_LOW, G_BASE, G_HIGH = 0.025, 0.042, 0.060   # home value CAGR scenarios (base = FHFA since-1991 CAGR ≈4.2%)
AV_GROWTH = 0.02               # Prop 13 cap (BOE-verified law)
A_TAX_RATE = 0.01335           # user-implied 2025 effective rate (FLAGGED)
B_TAX_RATE = 0.0118162182      # SF official FY2026-27 secured rate (VERIFIED)
PROP19_ADJ = 1_044_586.0       # verified for transfers 2025-02-16..2027-02-15; future value unknown -> held flat (FLAG)
SELL_COST = 0.06               # assumption: 6% selling costs (no official source — FLAG)
INV_RETURN = 0.07              # assumption: nominal stock return — no official source (FLAG)
INFLATION = 0.025              # assumption: long-run inflation (FLAG)
B_RENT = 7_150.0 * 12          # user-provided annual rent from 2 units
RENT_GROWTH = 0.025            # assumption beyond current SF 1.6% window (FLAG)
YEARS = list(range(2026, 2051))

def av(year):  # Property A status-quo factored base year value
    return A_AV_2026 * (1 + AV_GROWTH) ** (year - 2026)

def av_b(year):
    return B_AV_2025 * (1 + AV_GROWTH) ** (year - 2025)

rows = []
for year in YEARS:
    for label, g in (("low", G_LOW), ("base", G_BASE), ("high", G_HIGH)):
        a_val = A_VALUE_2026 * (1 + g) ** (year - 2026)
        b_val = B_VALUE_2026 * (1 + g) ** (year - 2026)
        rows.append({
            "year": year, "scenario": label, "cagr": f"{g:.1%}",
            "A_value": round(a_val), "B_value": round(b_val),
            "A_statusquo_AV": round(av(year)), "B_statusquo_AV": round(av_b(year)),
            "A_statusquo_tax": round(av(year) * A_TAX_RATE),
            "B_statusquo_tax": round(av_b(year) * B_TAX_RATE),
        })

# Inheritance-year scenarios (modeled at 2040 and 2050), base CAGR
inh = []
for year in (2040, 2050):
    g = G_BASE
    fmv = A_VALUE_2026 * (1 + g) ** (year - 2026)
    fbyv = av(year)
    # Prop 19 exclusion available (principal residence both sides): new BYV = fmv - PROP19_ADJ (since fmv >> fbyv+adj)
    new_bv_excl = max(fbyv, fmv - PROP19_ADJ)
    # No exclusion: full FMV
    new_bv_full = fmv
    inh.append({
        "year": year, "fmv": round(fmv), "fbyv": round(fbyv),
        "new_bv_excl": round(new_bv_excl), "tax_excl": round(new_bv_excl * A_TAX_RATE),
        "new_bv_full": round(new_bv_full), "tax_full": round(new_bv_full * A_TAX_RATE),
        "tax_statusquo": round(fbyv * A_TAX_RATE),
    })

# Estate tax scenarios on taxable estate (arithmetic on verified rates)
est = []
for size in (10e6, 15e6, 20e6, 30e6, 40e6):
    if size <= 15e6:
        fed = 0.0
    else:
        fed = 5_945_800 + 0.40 * (size - 15e6)   # simplified: credit + 40% on excess
        fed = min(fed, 0.40 * size)              # sanity: never exceed flat 40%
    est.append({"estate": int(size), "federal_tax": round(fed), "effective": f"{fed/size:.1%}", "ca_tax": 0})

# Sell-vs-hold breakeven: sell A at inheritance year, invest net proceeds vs. hold A renting it out
# Rent-if-let for A: NO official market-rent figure -> blank/flagged; model uses placeholder only in sensitivity, not shown as fact.
print("=== Property A value scenarios (Nov 2026 = $3.1M) ===")
for y in (2030, 2036, 2040, 2045, 2050):
    r = {x["scenario"]: x for x in rows if x["year"] == y}
    print(y, {k: f"${v['A_value']:,}" for k, v in r.items()})

print("\n=== Status-quo property tax (A, 2% AV growth, user-implied rate) ===")
for y in (2026, 2030, 2040, 2050):
    r = next(x for x in rows if x["year"] == y and x["scenario"] == "base")
    print(y, f"AV ${r['A_statusquo_AV']:,}  tax ${r['A_statusquo_tax']:,}")

print("\n=== Inheritance-year reassessment scenarios (base 4.2% CAGR) ===")
for x in inh:
    print(f"{x['year']}: FMV ${x['fmv']:,} | statusquo tax ${x['tax_statusquo']:,} | "
          f"Prop19-excl new BV ${x['new_bv_excl']:,} tax ${x['tax_excl']:,} | "
          f"no-excl new BV ${x['new_bv_full']:,} tax ${x['tax_full']:,}")

print("\n=== Federal estate tax (simplified, verified rates; CA = $0) ===")
for x in est:
    print(f"${x['estate']:,}: fed ${x['federal_tax']:,} ({x['effective']}), CA $0")

print("\n=== Sell A at 2040 (base CAGR), net after 6% costs, invested 7% ===")
fmv2040 = A_VALUE_2026 * (1 + G_BASE) ** 14
net = fmv2040 * (1 - SELL_COST)
# gain over stepped-up basis = post-inheritance appreciation only; model14 yrs of holding after death not modeled — assume sold soon: gain ~0 (stepped-up basis at death)
gross_inv = net * (1 + INV_RETURN) ** 10
print(f"FMV 2040 ${fmv2040:,.0f} -> net ${net:,.0f} -> in 10y @7%: ${gross_inv:,.0f} (tax on gain flagged: fed LTCG+NIIT+CA rates apply to post-death appreciation only)")

with open("/home/user/Cupertino3/docs/research/projections.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

with open("/home/user/Cupertino3/docs/research/projections_inheritance.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(inh[0].keys()))
    w.writeheader()
    w.writerows(inh)

with open("/home/user/Cupertino3/docs/research/projections_estate.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(est[0].keys()))
    w.writeheader()
    w.writerows(est)

print("\nWrote 3 CSVs to docs/research/")
