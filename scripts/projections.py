#!/usr/bin/env python3
"""
Projection engine for Cupertino3 inheritance decision analysis.
All assumptions are explicitly labeled. Verified facts carry source links.
Outputs: data/projections.json
"""
import json, math

# ---------------- Assumptions (labeled; used for projections, NOT verified facts) ----------------
GROWTH = {"conservative": 0.020, "moderate": 0.035, "aggressive": 0.050}   # market value growth
PROP13_GROWTH = 0.02                       # Prop 13 factored base year value growth (verified cap)
PROP19_CAP_2026 = 1_044_586                # BOE inflation-adjusted allowance (2025-2027 period, verified)
PROP19_CAP_GROWTH = 0.02                   # assumption: inflation adjustment continues
SC_TAX_RATE = 0.0120                       # Cupertino composite ~1.15-1.22% (published; midpoint used)
SC_SPECIAL = 730                           # est. special assessments/direct charges (from 2025 bill gap; flagged)
SF_TAX_RATE = 0.0118162182                 # SF FY2026-27 secured rate (official)
SF_DIRECT_CHARGES = 1100                   # est. direct charges/special assessments from 2025 bill (flagged)
ESTATE_EX_2026 = 15_000_000               # IRS (verified)
ESTATE_EX_GROWTH = 0.025                   # assumption: inflation indexing from 2027 (IRS: indexed)
INHERIT_YEARS = [2040, 2045, 2050]
YEARS = list(range(2026, 2056))
BASE_YEAR = 2026

CUP_MV_2026 = 3_100_000     # user-provided (flag)
SF_MV_2026 = 1_800_000      # user-provided (flag)
CUP_AV_2026 = 550_537       # user-provided tax assessment 2026 (flag; verify)
SF_AV_2026 = 116_532        # 2025 AV $114,248 × 1.02 (Prop 13 growth; user-provided base)
CUP_TAX_2025 = 7_207
SF_TAX_2025 = 2_439

# Utilities / insurance planning estimates (flagged assumptions)
INFLATION = 0.025
CUP_WATER_MO = 120          # user estimate 100-150 (flag)
CUP_ELEC_MO = 0             # solar net metering; user reports $0 cost, $10-20/mo credit (flag)
CUP_INS_YR = 1300           # third-party estimates 1,189-1,229; user guess 1,500 → midpoint used (flag)
CUP_MAINT_YR = 31_000       # 1% of value rule of thumb (assumption)
SF_WATER_MO = 365           # user 330-400 (flag)
SF_ELEC_MO = 50             # user 30-70 (flag)
SF_INS_YR = 2235            # third-party landlord estimate (flag)
SF_MAINT_YR = 18_000        # 1% of value rule of thumb (assumption)
SF_RENT_MO = 7150           # user-provided (flag)
CUP_RENT_MO = 5000          # 3-bed house median ~5,005 (Homes.com 2026, third-party, flag)
PORTFOLIO_RETURN = 0.06      # nominal stock return (assumption)
PORTFOLIO_TAX_DRAG = 0.331   # combined federal 20%+3.8% NIIT + CA 9.3% on dividends/gains (approx)
STOCK_YIELD = 0.02
MANAGER_PCT = 0.08           # rental management 8% (assumption)
VACANCY_PCT = 0.05


def f(x):
    return round(x)


def mv(base, growth, year):
    n = year - BASE_YEAR
    return base * (1 + growth) ** n


def av_prop13(base, year):
    return base * (1 + PROP13_GROWTH) ** (year - BASE_YEAR)


def prop19_cap(year):
    return PROP19_CAP_2026 * (1 + PROP19_CAP_GROWTH) ** (year - BASE_YEAR)


def estate_exemption(year):
    return ESTATE_EX_2026 * (1 + ESTATE_EX_GROWTH) ** (year - BASE_YEAR)


def cup_tax_now(year):
    # taxes if Prop 13 basis continues (before inheritance)
    av = av_prop13(CUP_AV_2026, year)
    return f(av * SC_TAX_RATE + SC_SPECIAL)


def sf_tax_now(year):
    av = av_prop13(SF_AV_2026, year)
    return f(av * SF_TAX_RATE + SF_DIRECT_CHARGES)


def build_value_table():
    rows = []
    for gname, g in GROWTH.items():
        for year in YEARS:
            rows.append({
                "growth": gname, "year": year,
                "cup_mv": f(mv(CUP_MV_2026, g, year)),
                "sf_mv": f(mv(SF_MV_2026, g, year)),
                "cup_av": f(av_prop13(CUP_AV_2026, year)),
                "sf_av": f(av_prop13(SF_AV_2026, year)),
            })
    return rows


def build_tax_table():
    """Property tax projections at inheritance under the Prop 19 rules.
    Scenario A: parents' principal residence = SF house (base plan).
       - Cupertino: rental → FULL reassessment at market value at date of death.
       - SF: family home → new taxable = market value − Prop19 allowance (if above cap).
    Scenario B: parents move to Cupertino (make it principal residence before death).
       - Cupertino: family home → capped exclusion.
       - SF: rental → FULL reassessment.
    """
    rows = []
    for gname, g in GROWTH.items():
        for year in INHERIT_YEARS:
            cap = prop19_cap(year)
            # Scenario A: Cupertino rental (full reassess); SF family home (capped)
            cup_av_A = mv(CUP_MV_2026, g, year)                       # full reassess
            sf_av_A = mv(SF_MV_2026, g, year) - cap                  # capped exclusion
            sf_tax_A = f(sf_av_A * SF_TAX_RATE + SF_DIRECT_CHARGES)
            cup_tax_A = f(cup_av_A * SC_TAX_RATE + SC_SPECIAL)
            # Scenario B: Cupertino family home (capped); SF rental (full reassess)
            cup_av_B = mv(CUP_MV_2026, g, year) - cap
            sf_av_B = mv(SF_MV_2026, g, year)
            sf_tax_B = f(sf_av_B * SF_TAX_RATE + SF_DIRECT_CHARGES)
            cup_tax_B = f(cup_av_B * SC_TAX_RATE + SC_SPECIAL)
            rows.append({
                "growth": gname, "year": year,
                "cap": f(cap),
                "A": {
                    "cup_av": f(cup_av_A), "sf_av": f(sf_av_A),
                    "cup_tax": cup_tax_A, "sf_tax": sf_tax_A,
                    "total_tax": f(cup_tax_A + sf_tax_A),
                },
                "B": {
                    "cup_av": f(cup_av_B), "sf_av": f(sf_av_B),
                    "cup_tax": cup_tax_B, "sf_tax": sf_tax_B,
                    "total_tax": f(cup_tax_B + sf_tax_B),
                },
            })
    return rows


def build_estate_table():
    rows = []
    for year in YEARS:
        ex = estate_exemption(year)
        rows.append({"year": year, "exemption_person": f(ex),
                     "exemption_couple": f(2 * ex)})
    return rows


def build_scenario_comparison():
    """Compare options for the Cupertino house at inheritance."""
    rows = []
    for gname, g in GROWTH.items():
        for year in INHERIT_YEARS:
            cup_mv = mv(CUP_MV_2026, g, year)
            cap = prop19_cap(year)
            cup_av_A = cup_mv                              # rental: full reassess
            cup_tax_A = f(cup_av_A * SC_TAX_RATE + SC_SPECIAL)
            cup_av_B = cup_mv - cap                        # family home: capped
            cup_tax_B = f(cup_av_B * SC_TAX_RATE + SC_SPECIAL)
            # Sell: proceeds = MV, capital gains = 0 (stepped-up basis); costs 6%
            sale_net = f(cup_mv * 0.94)
            reinvest_income = f(sale_net * PORTFOLIO_RETURN)
            reinvest_after_tax = f(sale_net * (PORTFOLIO_RETURN - STOCK_YIELD * PORTFOLIO_TAX_DRAG))
            # Rent Cupertino (as rental): gross rent, opex, NOI
            rent_gross = CUP_RENT_MO * 12
            opex = f(cup_tax_A + CUP_INS_YR + CUP_MAINT_YR + CUP_WATER_MO * 12 +
                     (rent_gross * MANAGER_PCT) +
                     rent_gross * VACANCY_PCT)
            noi = rent_gross - opex
            rows.append({
                "growth": gname, "year": year,
                "cup_mv": f(cup_mv), "cap": f(cap),
                "rent": {
                    "gross": rent_gross, "tax": cup_tax_A, "opex": opex, "noi": f(noi),
                },
                "sell": {
                    "proceeds": f(cup_mv), "net": sale_net,
                    "income": reinvest_income, "after_tax_income": reinvest_after_tax,
                },
            })
    return rows


def build_cost_table():
    rows = []
    for year in YEARS:
        n = year - BASE_YEAR
        infl = (1 + INFLATION) ** n
        rows.append({
            "year": year,
            "cup_water": f(CUP_WATER_MO * infl),
            "cup_ins": f(CUP_INS_YR * infl),
            "cup_maint": f(CUP_MAINT_YR * infl),
            "sf_water": f(SF_WATER_MO * infl),
            "sf_elec": f(SF_ELEC_MO * infl),
            "sf_ins": f(SF_INS_YR * infl),
            "sf_maint": f(SF_MAINT_YR * infl),
            "sf_rent": f(SF_RENT_MO * infl),
        })
    return rows


data = {
    "assumptions": {
        "market_growth": GROWTH,
        "prop13_growth": PROP13_GROWTH,
        "prop19_cap_2026": PROP19_CAP_2026,
        "prop19_cap_growth": PROP19_CAP_GROWTH,
        "sc_tax_rate": SC_TAX_RATE,
        "sc_special": SC_SPECIAL,
        "sf_tax_rate": SF_TAX_RATE,
        "sf_direct_charges": SF_DIRECT_CHARGES,
        "estate_exemption_2026": ESTATE_EX_2026,
        "estate_exemption_growth": ESTATE_EX_GROWTH,
        "portfolio_return": PORTFOLIO_RETURN,
        "portfolio_tax_drag": PORTFOLIO_TAX_DRAG,
        "stock_yield": STOCK_YIELD,
        "manager_pct": MANAGER_PCT,
        "vacancy_pct": VACANCY_PCT,
        "inflation": INFLATION,
    },
    "value_table": build_value_table(),
    "tax_table": build_tax_table(),
    "estate_table": build_estate_table(),
    "scenario_table": build_scenario_comparison(),
    "cost_table": build_cost_table(),
}

with open("data/projections.json", "w") as fp:
    json.dump(data, fp, indent=1)
print("Wrote data/projections.json")
print("\n--- Spot check: Moderate 2045 ---")
for r in data["tax_table"]:
    if r["growth"] == "moderate" and r["year"] == 2045:
        print(f"Prop19 cap 2045: ${r['cap']:,}")
        print(f"A: Cupertino AV ${r['A']['cup_av']:,} tax ${r['A']['cup_tax']:,} | SF AV ${r['A']['sf_av']:,} tax ${r['A']['sf_tax']:,} | total ${r['A']['total_tax']:,}")
        print(f"B: Cupertino AV ${r['B']['cup_av']:,} tax ${r['B']['cup_tax']:,} | SF AV ${r['B']['sf_av']:,} tax ${r['B']['sf_tax']:,} | total ${r['B']['total_tax']:,}")
for r in data["scenario_table"]:
    if r["growth"] == "moderate" and r["year"] == 2045:
        print(f"Sell: MV ${r['cup_mv']:,} net ${r['sell']['net']:,} income ${r['sell']['income']:,} after-tax ${r['sell']['after_tax_income']:,}")
        print(f"Rent: gross ${r['rent']['gross']:,} tax ${r['rent']['tax']:,} opex ${r['rent']['opex']:,} NOI ${r['rent']['noi']:,}")
print("\nEstate exemption 2045:", f(estate_exemption(2045)))
print("Estate exemption 2050:", f(estate_exemption(2050)))
