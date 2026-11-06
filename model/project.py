#!/usr/bin/env python3
"""Projection model for the inheritance decision (Property A = Cupertino, Property B = San Francisco).

Writes data/projections.json. Every number is either:
  * a verified input (cited in data/sources.json and tagged "verified"), or
  * a user-supplied input (tagged "user-supplied" / "unverified"), or
  * a model assumption (tagged "assumption"; change it in ASSUMPTIONS below).

Nothing here is personal information. Properties are referred to only as A and B.
Run:  python3 model/project.py
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "projections.json")

START_YEAR = 2026
END_YEAR = 2060
INHERIT_YEARS = [2040, 2045, 2050]   # user's stated window: 2040-2050

# ---------------------------------------------------------------- verified constants
PROP13_CAP = 0.02                      # BOE LTA 2026/002: factor not to exceed 2%; 2026-27 factor = 1.02
PROP19_CAP_2025 = 1_044_586            # BOE LTA 2025/009: value cap add-on for transfers 2/16/2025-2/15/2027
HOMEOWNERS_EXEMPTION = 7_000           # BOE Homeowners' Exemption page
FED_EXEMPTION_2026 = 15_000_000        # IRS IR-2025-103 / Rev. Proc. 2025-32 s.2.14
FED_TOP_ESTATE_RATE = 0.40             # secondary-verified only (see flags)
FED_LTCG_0_MAX_SINGLE_2026 = 49_450    # Rev. Proc. 2025-32 s.4.03 (All other individuals)
FED_LTCG_15_MAX_SINGLE_2026 = 545_500  # Rev. Proc. 2025-32 s.4.03
NIIT_RATE = 0.038                      # IRS Topic 559
NIIT_THRESH_SINGLE = 200_000           # IRS Topic 559
FED_GIFT_ANNUAL_EXCL_2026 = 19_000     # IRS IR-2025-103
SF_RENT_ALLOWABLE_2026 = 0.016         # SF Rent Board 3/1/2026-2/28/2027
CPI_FED_TARGET = 0.02                  # Federal Reserve MPR July 2026 (PCE 2% goal)
CPI_LATEST_BLS = 0.037                 # BLS CPI-U Sept 2026, 12-month (all items, NSA)
ELEC_CPI_BLS = 0.044                   # BLS CPI electricity, 12-month to Sept 2026

# ---------------------------------------------------------------- user-supplied inputs
A = {
    "market_value_2026": 3_100_000,    # user estimate Nov 2026 (UNVERIFIED)
    "av_2026": 550_537,                # user table (2026 roll); matches BOE factor 1.02 x 2025 AV
    "av_2025": 539_743,
    "tax_2025": 7_207,                 # user table
    "water_month": 125,                # user range $100-150 (midpoint)
    "elec_month_net": -15,             # user: solar credit $10-20/mo (midpoint); negative = credit
    "insurance_year": 1_500,           # user estimate (UNVERIFIED)
}
B = {
    "market_value_2026": 1_800_000,    # user estimate Nov 2026 (UNVERIFIED)
    "av_2025": 114_248,                # user table
    "tax_2025": 2_439,                 # user table
    "rent_month": 7_150,               # user: two rented units
    "water_month": 365,                # user range $330-400 for 3 units (midpoint)
    "elec_month": 50,                  # user range $30-70 (midpoint)
    "insurance_year": 1_500,           # user estimate (UNVERIFIED)
}

# ---------------------------------------------------------------- model assumptions
ASSUMPTIONS = {
    "inflation_base": CPI_FED_TARGET,        # base case = Fed 2% goal (verified target)
    "inflation_high": CPI_LATEST_BLS,        # stress case = latest BLS 12-month CPI (verified value)
    "appreciation_base": 0.03,               # ASSUMPTION
    "appreciation_low": 0.02,                # ASSUMPTION
    "appreciation_high": 0.05,               # ASSUMPTION
    "invest_return_low": 0.04,               # ASSUMPTION (pre-tax)
    "invest_return_high": 0.07,              # ASSUMPTION (pre-tax)
    "selling_cost": 0.06,                    # ASSUMPTION (commission + closing; not verified)
    "maint_pct_A": 0.005,                    # ASSUMPTION: 0.5% of market value per year
    "maint_pct_B": 0.010,                    # ASSUMPTION: 1.0% of market value per year
    "rent_growth_B": SF_RENT_ALLOWABLE_2026, # verified rent-control allowance applied to B's rents
    "rent_growth_A_market": 0.03,            # ASSUMPTION for any Cupertino rent (no verified rent input)
    "solar_credit_lost_cost_month": 50,      # ASSUMPTION scenario: solar credit lost -> bill of $50/mo
    "legacy_solar_expiry_note": "Interconnection date unknown; NEM 2.0 terms run 20 years from interconnection (CPUC).",
}

def prop13_factor(inflation):
    """Prop 13 inflation factor: CCPI change, capped at 2% (BOE LTA 2026/002)."""
    return min(inflation, PROP13_CAP)

def cap_amount(year, inflation):
    """Value-cap add-on for a transfer in `year`. Verified for 2025-2027 only; later years are an ASSUMPTION
    that the add-on grows with inflation (statute adjusts it by FHFA HPI every two years)."""
    if year <= 2026:
        return PROP19_CAP_2025
    return PROP19_CAP_2025 * (1 + inflation) ** (year - 2026)

def run_property_a(inflation=ASSUMPTIONS["inflation_base"],
                   appreciation=ASSUMPTIONS["appreciation_base"],
                   inherit_year=None, qualifies=True, solar_lost=False):
    """Year-by-year projection for Property A. If inherit_year is None: no transfer (current owner)."""
    rate = A["tax_2025"] / A["av_2025"]           # observed effective rate on assessed value (derived)
    f13 = prop13_factor(inflation)
    rows = []
    av = A["av_2026"]          # factored value, current owner (no transfer)
    tv = None                  # taxable value after transfer (if any)
    fmv0 = A["market_value_2026"]
    for y in range(START_YEAR, END_YEAR + 1):
        t = y - START_YEAR
        fmv = fmv0 * (1 + appreciation) ** t
        if inherit_year is not None and y == inherit_year:
            cap = cap_amount(y, inflation)
            if qualifies:
                tv = max(av, fmv - cap)        # BOE LTA 2026/026 value-cap rule
            else:
                tv = fmv                        # full reassessment to market
        if inherit_year is not None and y > inherit_year:
            tv = tv * (1 + f13)
        if inherit_year is not None and y >= inherit_year:
            taxable = tv
        else:
            taxable = av
        if y > START_YEAR and (inherit_year is None or y < inherit_year):
            av = av * (1 + f13)
        prop_tax = rate * taxable
        infl_idx = (1 + inflation) ** t
        insurance = A["insurance_year"] * infl_idx
        water = A["water_month"] * 12 * infl_idx
        if solar_lost:
            elec = ASSUMPTIONS["solar_credit_lost_cost_month"] * 12 * infl_idx
        else:
            elec = A["elec_month_net"] * 12 * infl_idx
        maint = ASSUMPTIONS["maint_pct_A"] * fmv
        total = prop_tax + insurance + water + elec + maint
        rows.append({
            "year": y,
            "market_value": round(fmv),
            "taxable_value": round(taxable),
            "property_tax": round(prop_tax),
            "insurance": round(insurance),
            "water": round(water),
            "electricity_net": round(elec),
            "maintenance": round(maint),
            "carrying_cost": round(total),
        })
        if inherit_year is not None and y < inherit_year:
            pass
    return rows

def run_property_b(inflation=ASSUMPTIONS["inflation_base"], appreciation=ASSUMPTIONS["appreciation_base"]):
    rate = B["tax_2025"] / B["av_2025"]
    f13 = prop13_factor(inflation)
    av = B["av_2025"] * (1 + f13)      # 2026-27 roll: 2025 AV x BOE factor (DERIVED, see flags)
    rows = []
    for y in range(START_YEAR, END_YEAR + 1):
        t = y - START_YEAR
        fmv = B["market_value_2026"] * (1 + appreciation) ** t
        if y > START_YEAR:
            av *= (1 + f13)
        infl_idx = (1 + inflation) ** t
        rent = B["rent_month"] * 12 * (1 + ASSUMPTIONS["rent_growth_B"]) ** t
        prop_tax = rate * av
        insurance = B["insurance_year"] * infl_idx
        water = B["water_month"] * 12 * infl_idx
        elec = B["elec_month"] * 12 * infl_idx
        maint = ASSUMPTIONS["maint_pct_B"] * fmv
        costs = prop_tax + insurance + water + elec + maint
        rows.append({
            "year": y,
            "market_value": round(fmv),
            "taxable_value": round(av),
            "property_tax": round(prop_tax),
            "rent_income": round(rent),
            "insurance": round(insurance),
            "water": round(water),
            "electricity": round(elec),
            "maintenance": round(maint),
            "operating_costs": round(costs),
            "net_operating_income": round(rent - costs),
            "noi_yield_on_value": round((rent - costs) / fmv * 100, 2),
        })
    return rows

def keep_value(rent0, inherit_year, horizon, r, appreciation, inflation, qualifies, rent_growth):
    """Value (in future dollars) at inherit_year+horizon of KEEPING the house, rent-or-live equivalent.
    rent0 = annual rent (or imputed rent) in inherit_year. Cash flows reinvested at r."""
    rows = run_property_a(inflation, appreciation, inherit_year, qualifies)
    by_year = {x["year"]: x for x in rows}
    end = inherit_year + horizon
    fv = 0.0
    for k in range(horizon):
        y = inherit_year + k
        rent = rent0 * (1 + rent_growth) ** k
        cost = by_year[y]["carrying_cost"]
        fv += (rent - cost) * (1 + r) ** (horizon - 1 - k)
    fmv_end = by_year[end]["market_value"]
    s = ASSUMPTIONS["selling_cost"]
    return fmv_end * (1 - s) + fv

def sell_value(inherit_year, horizon, r, appreciation):
    rows = run_property_a(ASSUMPTIONS["inflation_base"], appreciation, inherit_year, True)
    by_year = {x["year"]: x for x in rows}
    fmv = by_year[inherit_year]["market_value"]
    proceeds = fmv * (1 - ASSUMPTIONS["selling_cost"])
    # Stepped-up basis = FMV at death (IRS Pub 551), so a sale on the transfer date has ~zero gain.
    return proceeds * (1 + r) ** horizon

def breakeven_rent(inherit_year, horizon, r, appreciation, inflation, qualifies):
    """Monthly rent (grows with ASSUMPTION rent_growth_A_market) that makes keeping = selling."""
    target = sell_value(inherit_year, horizon, r, appreciation)
    lo, hi = 0.0, 200_000.0
    g = ASSUMPTIONS["rent_growth_A_market"]
    # If even the top of the search range cannot match selling, report None (not reached).
    if keep_value(hi, inherit_year, horizon, r, appreciation, inflation, qualifies, g) < target:
        return None
    for _ in range(100):
        mid = (lo + hi) / 2
        v = keep_value(mid, inherit_year, horizon, r, appreciation, inflation, qualifies, g)
        if v < target:
            lo = mid
        else:
            hi = mid
    return round((lo + hi) / 2 / 12)  # monthly rent, USD

def inheritance_thresholds():
    rows = []
    for y in range(2026, 2051):
        if y == 2026:
            amt = FED_EXEMPTION_2026
        else:
            amt = FED_EXEMPTION_2026 * (1 + ASSUMPTIONS["inflation_base"]) ** (y - 2026)
        amt_hi = FED_EXEMPTION_2026 * (1 + ASSUMPTIONS["inflation_high"]) ** (y - 2026) if y > 2026 else FED_EXEMPTION_2026
        rows.append({
            "year": y,
            "federal_exemption_base": round(amt),
            "federal_exemption_high_inflation": round(amt_hi),
            "couple_with_portability_base": round(2 * amt),
        })
    return rows

def main():
    out = {"meta": {
        "generated_for": "Property A (Cupertino, Santa Clara County, CA) and Property B (San Francisco, CA)",
        "start_year": START_YEAR, "end_year": END_YEAR, "inherit_years": INHERIT_YEARS,
        "note": "Projections, not forecasts. Assumption values are labelled and can be changed in model/project.py.",
    }, "inputs": {"A": A, "B": B}, "assumptions": ASSUMPTIONS, "constants": {
        "prop13_cap": PROP13_CAP, "prop19_cap_2025_2027": PROP19_CAP_2025,
        "homeowners_exemption": HOMEOWNERS_EXEMPTION, "fed_exemption_2026": FED_EXEMPTION_2026,
        "fed_ltcg_0_max_single_2026": FED_LTCG_0_MAX_SINGLE_2026,
        "fed_ltcg_15_max_single_2026": FED_LTCG_15_MAX_SINGLE_2026,
        "niit_rate": NIIT_RATE, "niit_threshold_single": NIIT_THRESH_SINGLE,
    }}
    # Property A: no-transfer baseline and three inheritance-year scenarios
    base_a = run_property_a()
    out["property_a"] = {"no_transfer_base": base_a, "inheritance": {}}
    for y in INHERIT_YEARS:
        out["property_a"]["inheritance"][str(y)] = {
            "qualifies_live_in": run_property_a(inherit_year=y, qualifies=True),
            "does_not_qualify": run_property_a(inherit_year=y, qualifies=False),
        }
    out["property_a"]["solar_credit_lost_base"] = run_property_a(solar_lost=True)

    # Property B: current hold economics
    out["property_b"] = {"base": run_property_b(),
                         "low_appreciation": run_property_b(appreciation=ASSUMPTIONS["appreciation_low"]),
                         "high_inflation": run_property_b(inflation=ASSUMPTIONS["inflation_high"])}

    # Decision analysis for Property A (inheritance in 2045, 10-year horizon)
    dec = {"inherit_year": 2045, "horizon_years": 10, "selling_cost": ASSUMPTIONS["selling_cost"], "grid": []}
    for app_label, app in [("2%", 0.02), ("3%", 0.03), ("5%", 0.05)]:
        for r_label, r in [("4%", 0.04), ("7%", 0.07)]:
            for q in (True, False):
                be = breakeven_rent(2045, 10, r, app, ASSUMPTIONS["inflation_base"], q)
                dec["grid"].append({
                    "appreciation": app_label, "invest_return": r_label,
                    "qualifies_live_in": q,
                    "breakeven_monthly_rent": be,
                })
    dec["sell_value_10y_at_4pct_3pct"] = round(sell_value(2045, 10, 0.04, 0.03))
    dec["sell_value_10y_at_7pct_3pct"] = round(sell_value(2045, 10, 0.07, 0.03))
    out["decision_a"] = dec
    out["inheritance_thresholds"] = inheritance_thresholds()

    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)
    print("wrote", OUT)

if __name__ == "__main__":
    main()
