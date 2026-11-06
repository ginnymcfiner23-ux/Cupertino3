#!/usr/bin/env python3
"""Projection model for the two anonymized properties (standard library only).

Reads  data/ia/inputs.json   (client inputs are UNVERIFIED; assumptions are labeled)
Writes data/ia/projections.json

Method (every step is a modeling choice unless an official source is cited in inputs.json):
  * Prop 13 path (no transfer): assessed value grows 2%/yr (BOE factor 1.02, S11).
  * Prop 19 path (parent-child transfer at year T):
      occupied qualifying home  -> AV = min(FCV, FBYV + max(0, FCV - FBYV - cap)), then +2%/yr
      rented / not qualifying   -> AV = FCV at T, then +2%/yr (full reassessment)
    cap = $1,044,586 (2026 value), indexed by inflation from 2027 (assumption, FL-18).
  * Property B (3 units): the occupied unit gets the Prop 19 treatment on 1/3 of value;
    the two rented units (2/3) are fully reassessed (assessor determines the split, FL-17).
  * Tax = assessed value x effective rate from client tax bills (client-derived, FL-02/FL-03).
  * Living option: homeowners' exemption reduces tax by $7,000 x rate.
  * Rent option (Property A): rent is unknown, so the model solves the break-even rent
    that equalizes end-of-horizon wealth with selling.
  * Sale: stepped-up basis (IRC 1014) => no gain at sale; costs = brokerage (assumption)
    + county transfer tax (S25). City transfer taxes are excluded (FL-13).
  * Cash flows and sale proceeds are compounded at an after-tax return:
      return x (1 - yield_share x (fed LTCG + NIIT + CA rate)).
  * End-value is reported in nominal and real (2026) dollars at the horizon year.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
INP = json.loads((ROOT / "data/ia/inputs.json").read_text())

V0 = INP["valuation_year"]              # 2026 valuation date
END = INP["horizon_end"]                # 2060 common end date for comparisons
TESTS = INP["inheritance_years"]        # [2040, 2045, 2050]
BASE_T = INP["base_illustration_year"]  # 2045 for the year-by-year table
A = INP["properties"]["A"]
B = INP["properties"]["B"]
AS = INP["assumptions"]
SCEN = INP["scenarios"]

P13 = 0.02
CAP_2026 = AS["prop19_value_limit_2025"]["value"]   # 1,044,586 applies Feb 16 2025 - Feb 15 2027
HOX = AS["homeowners_exemption"]["value"]
SELL_COST = AS["sale_brokerage_pct"]["value"] + AS["county_transfer_tax_rate"]["value"]
YIELD_SHARE = AS["investment_yield_taxable_share"]["value"]
TAX_DRAG = (AS["federal_ltcg_rate"]["value"] + AS["niit_rate"]["value"]
            + AS["ca_marginal_rate_for_heir"]["value"])
RENT_TAX = AS["rental_marginal_tax_rate"]["value"]
BLD = AS["depreciation_building_share"]["value"]
LIFE = AS["depreciation_years"]["value"]
OCC = AS["unit_share_occupied_when_one_unit_lived_in"]["value"]   # occupied share (B)
RENT_SHARE_B = 1 - OCC

RATE_A = A["tax_2025"]["value"] / A["assessed_value_2025"]["value"]
RATE_B = B["tax_2025"]["value"] / B["assessed_value_2025"]["value"]
RATE_B_FLOOR = 0.01   # Prop 13 1% general levy only (lower-bound sensitivity)

MV_A = A["market_value_2026"]["value"]
AV25_A = A["assessed_value_2025"]["value"]
INS_A = A["insurance_annual"]["value"]
WATER_A_M = A["water_monthly"]["mid"]
ELEC_OFFICIAL_M = A["fixed_charge_monthly"]["value"] - A["electricity_solar_credit_monthly"]["mid"]
ELEC_CLIENT_M = -A["electricity_solar_credit_monthly"]["mid"]
MAINT_A = A["maintenance_pct_of_value"]["value"]

MV_B = B["market_value_2026"]["value"]
AV25_B = B["assessed_value_2025"]["value"]
INS_B = B["insurance_annual"]["value"]
WATER_B_M = B["water_sewer_monthly"]["mid"]
ELEC_B_M = B["electricity_monthly"]["mid"]
RENT_B_M = B["rent_monthly_total_two_units"]["value"]
MAINT_B = B["maintenance_pct_of_value"]["value"]


def fcv(mv, g, t):
    """Full cash (market) value in year t."""
    return mv * (1 + g) ** (t - V0)


def fbyv(av25, t):
    """Prop 13 factored base-year value (no transfer) in year t."""
    return av25 * (1 + P13) ** (t - 2025)


def cap(t, infl, indexed=True):
    """Prop 19 value limit in year t."""
    if not indexed:
        return CAP_2026
    return CAP_2026 * (1 + infl) ** max(0, t - V0)


def av_prop19(f_t, base_t, cap_t):
    """Assessed value of a qualifying home after transfer at year T."""
    return min(f_t, base_t + max(0.0, f_t - base_t - cap_t))


def infl_factor(s, t):
    return (1 + s["inflation"]) ** (t - V0)


def run_keep_or_sell(cashflows, proceeds_T, T, end_asset, r_after, sell_at_end=True):
    """Return end-of-horizon wealth.

    cashflows: dict year -> cash (positive = inflow, negative = outflow), for T <= t < END.
    proceeds_T: lump-sum wealth placed at year T (sell option), else 0.
    end_asset: asset value at END (keep option) that is realized net of sale costs.
    """
    w = proceeds_T
    for t in range(T, END):
        w = w * (1 + r_after) + cashflows.get(t, 0.0)
    if end_asset is not None:
        w += end_asset * (1 - SELL_COST)
    return w


def r_after(s):
    return s["investment_return"] - YIELD_SHARE * TAX_DRAG


# ---------- Property A: Cupertino ----------
def a_tax(t, T, option, s, indexed=True):
    if option == "live":
        fT, bT, cT = fcv(MV_A, s["appreciation"], T), fbyv(AV25_A, T), cap(T, s["inflation"], indexed)
        av = av_prop19(fT, bT, cT) * (1 + P13) ** (t - T)
        return av, av * RATE_A - HOX * RATE_A
    fT = fcv(MV_A, s["appreciation"], T)
    av = fT * (1 + P13) ** (t - T)
    return av, av * RATE_A


def a_costs(t, s, elec_m):
    f = infl_factor(s, t)
    water = WATER_A_M * 12 * f
    elec = elec_m * 12 * f
    ins = INS_A * f
    maint = MAINT_A * fcv(MV_A, s["appreciation"], t)
    return water, elec, ins, maint


def a_live(T, s, elec_m=ELEC_OFFICIAL_M, indexed=True):
    cash = {}
    rows = {}
    for t in range(T, END):
        av, tax = a_tax(t, T, "live", s, indexed)
        w, e, i, m = a_costs(t, s, elec_m)
        cash[t] = -(tax + w + e + i + m)
        rows[t] = dict(av=av, tax=tax, water=w, elec=e, ins=i, maint=m, cash=cash[t])
    end_asset = fcv(MV_A, s["appreciation"], END)
    w_end = run_keep_or_sell(cash, 0.0, T, end_asset, r_after(s))
    return w_end, rows


def a_sell_end(T, s):
    proceeds = fcv(MV_A, s["appreciation"], T) * (1 - SELL_COST)
    return proceeds * (1 + r_after(s)) ** (END - T), proceeds


def a_rent_breakeven(T, s, elec_m=ELEC_OFFICIAL_M, indexed=True):
    """Annual rent in 2026 dollars (grown at inflation) at which keep-and-rent equals selling."""
    target, _ = a_sell_end(T, s)
    dep = BLD * fcv(MV_A, s["appreciation"], T) / LIFE

    def keep_wealth(r0):
        cash = {}
        for t in range(T, END):
            av, tax = a_tax(t, T, "rent", s, indexed)
            w, e, i, m = a_costs(t, s, elec_m)
            rent = r0 * infl_factor(s, t)
            taxable = rent - (w + e + i + m + tax) - dep
            tax_rent = max(0.0, taxable) * RENT_TAX
            cash[t] = rent - (tax + w + e + i + m) - tax_rent
        return run_keep_or_sell(cash, 0.0, T, fcv(MV_A, s["appreciation"], END), r_after(s))

    lo, hi = 0.0, 500000.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if keep_wealth(mid) < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


# ---------- Property B: San Francisco (3 units; 1 occupied, 2 rented) ----------
def b_av(t, T, option, s):
    fT = fcv(MV_B, s["appreciation"], T)
    if option == "hybrid":   # heir occupies one unit; two rented units reassessed
        occ_f, occ_b = fT * OCC, fbyv(AV25_B, T) * OCC
        occ_av = av_prop19(occ_f, occ_b, cap(T, s["inflation"]))   # full Prop 19 limit applies to the one qualifying unit
        av_T = occ_av + fT * RENT_SHARE_B
    else:                    # no occupancy: whole property reassessed
        av_T = fT
    return av_T * (1 + P13) ** (t - T)


def b_tax(t, T, option, s, rate=RATE_B):
    av = b_av(t, T, option, s)
    if option == "hybrid":
        return av, av * rate - HOX * rate
    return av, av * rate


def b_keep(T, s, option, rate=RATE_B, rent_growth=None, maint_pct=None):
    rg = s["rent_growth_sf"] if rent_growth is None else rent_growth
    mp = MAINT_B if maint_pct is None else maint_pct
    cash, rows = {}, {}
    dep = BLD * fcv(MV_B, s["appreciation"], T) * RENT_SHARE_B / LIFE
    for t in range(T, END):
        f = infl_factor(s, t)
        av, tax = b_tax(t, T, option, s, rate)
        water = WATER_B_M * 12 * f
        elec = ELEC_B_M * 12 * f
        ins = INS_B * f
        maint = mp * fcv(MV_B, s["appreciation"], t)
        rent = RENT_B_M * 12 * (1 + rg) ** (t - V0)
        taxable = rent - RENT_SHARE_B * (water + elec + ins + maint + tax) - dep
        tax_rent = max(0.0, taxable) * RENT_TAX
        cash[t] = rent - (tax + water + elec + ins + maint) - tax_rent
        rows[t] = dict(av=av, tax=tax, water=water, elec=elec, ins=ins, maint=maint,
                       rent=rent, tax_rent=tax_rent, cash=cash[t])
    end_asset = fcv(MV_B, s["appreciation"], END)
    w_end = run_keep_or_sell(cash, 0.0, T, end_asset, r_after(s))
    return w_end, rows


def b_sell_end(T, s):
    proceeds = fcv(MV_B, s["appreciation"], T) * (1 - SELL_COST)
    return proceeds * (1 + r_after(s)) ** (END - T), proceeds


# ---------- assemble outputs ----------
def real(value, s):
    return value / (1 + s["inflation"]) ** (END - V0)


def build():
    out = {
        "meta": {
            "valuation_year": V0,
            "horizon_end": END,
            "inheritance_years_tested": TESTS,
            "base_illustration_year": BASE_T,
            "effective_tax_rates": {"A_implied": RATE_A, "B_implied": RATE_B, "B_floor_1pct": RATE_B_FLOOR},
            "sale_costs": SELL_COST,
            "after_tax_return_drag": YIELD_SHARE * TAX_DRAG,
            "note": "Client inputs are UNVERIFIED. Values are modeled outcomes, not forecasts or advice.",
        },
        "scenarios": SCEN,
        "summary": [],
        "breakeven_rent_A": [],
        "sensitivities": [],
        "yearly": {},
        "pre_transfer": {},
    }

    for sk, s in SCEN.items():
        for T in TESTS:
            live_w, _ = a_live(T, s)
            sell_w, proceeds = a_sell_end(T, s)
            be = a_rent_breakeven(T, s)
            out["summary"].append({
                "property": "A", "T": T, "scenario": sk,
                "option": "Live in the home (Prop 19 path)",
                "end_nominal": round(live_w), "end_real_2026": round(real(live_w, s)),
            })
            out["summary"].append({
                "property": "A", "T": T, "scenario": sk,
                "option": "Sell at inheritance, invest net proceeds",
                "end_nominal": round(sell_w), "end_real_2026": round(real(sell_w, s)),
                "net_proceeds_at_T": round(proceeds),
            })
            out["breakeven_rent_A"].append({
                "T": T, "scenario": sk,
                "annual_rent_2026_dollars": round(be),
                "monthly_rent_at_T_nominal": round(be * infl_factor(s, T) / 12),
                "monthly_rent_2026_dollars": round(be / 12),
            })

            keepH, _ = b_keep(T, s, "hybrid")
            keepF, _ = b_keep(T, s, "full")
            sellB, proceedsB = b_sell_end(T, s)
            out["summary"].append({
                "property": "B", "T": T, "scenario": sk,
                "option": "Heir lives in 1 unit, rent 2 units (Prop 19 on 1 unit)",
                "end_nominal": round(keepH), "end_real_2026": round(real(keepH, s)),
            })
            out["summary"].append({
                "property": "B", "T": T, "scenario": sk,
                "option": "No occupancy, keep renting 2 units (full reassessment)",
                "end_nominal": round(keepF), "end_real_2026": round(real(keepF, s)),
            })
            out["summary"].append({
                "property": "B", "T": T, "scenario": sk,
                "option": "Sell at inheritance, invest net proceeds",
                "end_nominal": round(sellB), "end_real_2026": round(real(sellB, s)),
                "net_proceeds_at_T": round(proceedsB),
            })

    # Sensitivities at base case, T = BASE_T
    s = SCEN["base"]
    w_idx, _ = a_live(BASE_T, s, indexed=True)
    w_noidx, _ = a_live(BASE_T, s, indexed=False)
    out["sensitivities"].append({"label": "A live: Prop 19 limit indexed with inflation (base)", "end_real_2026": round(real(w_idx, s))})
    out["sensitivities"].append({"label": "A live: Prop 19 limit NOT indexed (stays $1,044,586)", "end_real_2026": round(real(w_noidx, s))})
    w_elec_client, _ = a_live(BASE_T, s, elec_m=ELEC_CLIENT_M)
    out["sensitivities"].append({"label": "A live: electricity at client claim (net credit $15/mo, no fixed charge)", "end_real_2026": round(real(w_elec_client, s))})
    hyb_floor, _ = b_keep(BASE_T, s, "hybrid", rate=RATE_B_FLOOR)
    out["sensitivities"].append({"label": "B hybrid: tax at 1% levy only (lower bound)", "end_real_2026": round(real(hyb_floor, s))})
    hyb_base, _ = b_keep(BASE_T, s, "hybrid")
    out["sensitivities"].append({"label": "B hybrid: tax at implied 2.13% rate (base)", "end_real_2026": round(real(hyb_base, s))})
    rent_hi, _ = b_keep(BASE_T, s, "hybrid", rent_growth=s["inflation"])
    out["sensitivities"].append({"label": "B hybrid: rent grows with inflation instead of 1.6% cap", "end_real_2026": round(real(rent_hi, s))})


    # Best case for keeping B: 1% levy only, 0.5% upkeep, rent grows with inflation
    best_keep, _ = b_keep(BASE_T, s, "hybrid", rate=RATE_B_FLOOR, rent_growth=s["inflation"], maint_pct=0.005)
    out["sensitivities"].append({"label": "B hybrid BEST CASE for keeping (1% levy only, 0.5% upkeep, rent grows with inflation)", "end_real_2026": round(real(best_keep, s))})
    best_full, _ = b_keep(BASE_T, s, "full", rate=RATE_B_FLOOR, rent_growth=s["inflation"], maint_pct=0.005)
    out["sensitivities"].append({"label": "B full-reassessment BEST CASE for keeping (no occupancy)", "end_real_2026": round(real(best_full, s))})
    sell_B_base, _ = b_sell_end(BASE_T, s)
    out["sensitivities"].append({"label": "B sell at inheritance (base, for comparison)", "end_real_2026": round(real(sell_B_base, s))})

    # Economic cost of living in A at BASE_T (base case): cash costs + forgone return on proceeds - expected appreciation
    _, a_rows_T = a_live(BASE_T, s)
    proceeds_A = fcv(MV_A, s["appreciation"], BASE_T) * (1 - SELL_COST)
    yr = BASE_T
    r0 = a_rows_T[yr]
    cash_cost = -r0["cash"]
    forgone = proceeds_A * r_after(s)
    appreciation = fcv(MV_A, s["appreciation"], yr) * s["appreciation"]
    out["economic_cost_A"] = {
        "year": yr, "scenario": "base",
        "cash_costs_nominal": round(cash_cost),
        "forgone_after_tax_return_on_sale_proceeds": round(forgone),
        "expected_appreciation": round(appreciation),
        "net_annual_economic_cost": round(cash_cost + forgone - appreciation),
        "note": "Living value is not counted. Compare the net figure with the market rent for a comparable home (not verified here)."
    }

    # Year-by-year, base case, T = BASE_T
    ya, yb, pa, pb = [], [], [], []
    _, a_rows = a_live(BASE_T, s)
    _, b_hyb_rows = b_keep(BASE_T, s, "hybrid")
    _, b_full_rows = b_keep(BASE_T, s, "full")
    for t in range(V0, END + 1):
        f_t = fcv(MV_A, s["appreciation"], t)
        av_np = fbyv(AV25_A, t)
        ar = a_rows.get(t)
        pa.append({"year": t, "fcv": round(f_t), "av_no_transfer": round(av_np), "tax_no_transfer": round(av_np * RATE_A)})
        if ar:
            ya.append({"year": t, "fcv": round(f_t), "av_no_transfer": round(av_np),
                       "tax_no_transfer": round(av_np * RATE_A),
                       "av_live_after_transfer": round(ar["av"]), "tax_live": round(ar["tax"]),
                       "water": round(ar["water"]), "electricity": round(ar["elec"]),
                       "insurance": round(ar["ins"]), "maintenance": round(ar["maint"]),
                       "live_annual_cost": round(-ar["cash"])})
        else:
            ya.append({"year": t, "fcv": round(f_t), "av_no_transfer": round(av_np),
                       "tax_no_transfer": round(av_np * RATE_A)})
        f_b = fcv(MV_B, s["appreciation"], t)
        av_np_b = fbyv(AV25_B, t)
        pb.append({"year": t, "fcv": round(f_b), "av_no_transfer": round(av_np_b), "tax_no_transfer": round(av_np_b * RATE_B)})
        hr = b_hyb_rows.get(t)
        fr = b_full_rows.get(t)
        row = {"year": t, "fcv": round(f_b), "av_no_transfer": round(av_np_b), "tax_no_transfer": round(av_np_b * RATE_B)}
        if hr:
            row.update({"av_hybrid": round(hr["av"]), "tax_hybrid": round(hr["tax"]),
                        "rent": round(hr["rent"]), "water": round(hr["water"]), "electricity": round(hr["elec"]),
                        "insurance": round(hr["ins"]), "maintenance": round(hr["maint"]),
                        "hybrid_net_cash": round(hr["cash"]),
                        "av_full": round(fr["av"]), "tax_full": round(fr["tax"]),
                        "full_net_cash": round(fr["cash"])})
        yb.append(row)
    out["yearly"]["A"] = ya
    out["yearly"]["B"] = yb
    out["pre_transfer"]["A"] = pa
    out["pre_transfer"]["B"] = pb
    out["yearly_meta"] = {"T": BASE_T, "scenario": "base",
                          "note": "Post-transfer columns start in the inheritance year; earlier years show the status-quo Prop 13 path only."}
    return out


if __name__ == "__main__":
    result = build()
    path = ROOT / "data/ia/projections.json"
    path.write_text(json.dumps(result, indent=2) + "\n")
    print("wrote", path)
