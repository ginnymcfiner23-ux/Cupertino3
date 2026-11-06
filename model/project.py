"""Projection model for Property A (Cupertino) and Property B (San Francisco).

Inputs: data/assumptions.json (user inputs are UNVERIFIED and labelled as such).
Outputs: data/projections.json and CSV files in data/projections/.
All numbers are projections under stated assumptions, not facts.
Run:  python3 model/project.py
"""
import json, csv, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = {x["id"]: x["value"] for x in json.load(open(os.path.join(ROOT, "data/assumptions.json")))["inputs"]}

BASE = 2026
END = 2050
GROWTH_CAP = A["M_PT_CAP"]            # 2% Prop 13 growth on assessed value
CAP_AMT = A["M_PROP19_CAP"]           # $1,044,586 held flat (statute adjusts every 2 years)
SALE_COST = A["M_SALE_COST"]
TRANSFER = A["M_TRANSFER"]
INVEST = A["M_INVEST_RET"]
RATE_A = A["M_PT_RATE_A"]
RATE_B = A["M_PT_RATE_B"]
RENT_G = A["M_RENT_GROWTH"]
INS_G = A["M_INS_GROWTH"]
WAT_G = A["M_WATER_GROWTH"]
ELE_G = A["M_ELEC_GROWTH"]
MAINT_A = A["M_MAINT_A"]
MAINT_B = A["M_MAINT_B"]


def scenario_values(apprec):
    """Return dict of per-year series for both properties under one appreciation rate."""
    years = list(range(BASE, END + 1))
    out = {"years": years}

    # ---------- Property A ----------
    fmv_a = {t: A["U_A_FMV"] * (1 + apprec) ** (t - BASE) for t in years}
    fbyv_a = {t: A["U_A_FBYV"] * (1 + GROWTH_CAP) ** (t - BASE) for t in years}
    out["A_fmv"] = fmv_a
    out["A_assessed_parent"] = fbyv_a
    out["A_tax_parent"] = {t: fbyv_a[t] * RATE_A for t in years}
    out["A_insurance"] = {t: A["U_A_INS"] * (1 + INS_G) ** (t - BASE) for t in years}
    out["A_water"] = {t: A["U_A_WATER"] * 12 * (1 + WAT_G) ** (t - BASE) for t in years}
    out["A_solar_credit"] = {t: A["U_A_SOLAR"] * 12 * (1 + ELE_G) ** (t - BASE) for t in years}   # credit, reduces cost
    out["A_maintenance"] = {t: MAINT_A * fmv_a[t] for t in years}
    return out


def property_a_after(Y, apprec, series):
    """Post-inheritance scenarios for Property A, inheritance in year Y."""
    years = series["years"]
    fmv = series["A_fmv"]
    fbyv = series["A_assessed_parent"]
    # Prop 19 family home (heir moves in): taxable = max(FBYV, FMV - cap)
    taxable_p19 = {}
    taxable_rent = {}
    for t in years:
        if t < Y:
            continue
        base_p19 = max(fbyv[Y], fmv[Y] - CAP_AMT)
        base_rent = fmv[Y]
        taxable_p19[t] = base_p19 * (1 + GROWTH_CAP) ** (t - Y)
        taxable_rent[t] = base_rent * (1 + GROWTH_CAP) ** (t - Y)
    res = {}
    res["A_taxable_p19"] = taxable_p19
    res["A_taxable_reassessed"] = taxable_rent
    res["A_tax_p19"] = {t: taxable_p19[t] * RATE_A for t in taxable_p19}
    res["A_tax_reassessed"] = {t: taxable_rent[t] * RATE_A for t in taxable_rent}
    res["A_sale_net_at_Y"] = fmv[Y] * (1 - SALE_COST - TRANSFER)
    return res


def property_b(Y, apprec, series):
    years = series["years"]
    fmv = {t: A["U_B_FMV"] * (1 + apprec) ** (t - BASE) for t in years}
    fbyv_b_parent = {t: A["U_B_FBYV"] * (1 + GROWTH_CAP) ** (t - BASE) for t in years}
    rent = {t: A["U_B_RENT"] * 12 * (1 + RENT_G) ** (t - BASE) for t in years}
    water = {t: A["U_B_WATER"] * 12 * (1 + WAT_G) ** (t - BASE) for t in years}
    elec = {t: A["U_B_ELEC"] * 12 * (1 + ELE_G) ** (t - BASE) for t in years}
    ins = {t: A["U_B_INS"] * (1 + INS_G) ** (t - BASE) for t in years}
    maint = {t: MAINT_B * fmv[t] for t in years}
    # Parent-owned tax (informational, Prop 13)
    tax_parent = {t: fbyv_b_parent[t] * RATE_B for t in years}

    # B1: keep as rental -> full reassessment at inheritance; then 2% growth on taxable value
    tax_b1 = {}
    noi_b1 = {}
    # B3: heir occupies the owner unit (1 of 3 units; illustrative unit-count share), rents 2 units
    tax_b3 = {}
    noi_b3 = {}
    for t in years:
        if t < Y:
            continue
        taxable_b1 = fmv[Y] * (1 + GROWTH_CAP) ** (t - Y)
        tax_b1[t] = taxable_b1 * RATE_B
        # B3 (illustrative: unit share 1/3 for owner unit; the assessor allocation is not verified)
        share = 1 / 3
        occ_base = max(fbyv_b_parent[Y] * share, fmv[Y] * share - CAP_AMT)
        rented_base = fmv[Y] * (1 - share)
        taxable_b3 = (occ_base + rented_base) * (1 + GROWTH_CAP) ** (t - Y)
        tax_b3[t] = taxable_b3 * RATE_B
        noi_b1[t] = rent[t] - water[t] - elec[t] - ins[t] - maint[t] - tax_b1[t]
        noi_b3[t] = rent[t] - water[t] * 2 / 3 - elec[t] * 2 / 3 - ins[t] - maint[t] - tax_b3[t]
    sale_b = fmv[Y] * (1 - SALE_COST - TRANSFER)
    return {
        "B_fmv": fmv, "B_assessed_parent": fbyv_b_parent, "B_tax_parent": tax_parent,
        "B_rent": rent, "B_water": water, "B_elec": elec, "B_insurance": ins, "B_maintenance": maint,
        "B_tax_b1": tax_b1, "B_noi_b1": noi_b1, "B_tax_b3": tax_b3, "B_noi_b3": noi_b3,
        "B_sale_net_at_Y": sale_b,
    }


def run(Y=2045, apprec=A["M_APPREC"]):
    s = scenario_values(apprec)
    pa = property_a_after(Y, apprec, s)
    pb = property_b(Y, apprec, s)
    years = s["years"]
    # A post-inheritance annual cost (heir living in, Prop 19)
    a_cost_p19 = {}
    a_cost_rent = {}
    for t in years:
        if t < Y:
            continue
        common = s["A_insurance"][t] + s["A_water"][t] - s["A_solar_credit"][t] + s["A_maintenance"][t]
        a_cost_p19[t] = pa["A_tax_p19"][t] + common
        a_cost_rent[t] = pa["A_tax_reassessed"][t] + common
    # Parent-owned years for context
    a_cost_parent = {t: s["A_tax_parent"][t] + s["A_insurance"][t] + s["A_water"][t] - s["A_solar_credit"][t] + s["A_maintenance"][t] for t in years}

    # Comparisons at 2050 (illustrative; excludes imputed rent/use value)
    sum_a_cost_p19 = sum(a_cost_p19[t] for t in a_cost_p19)
    wealth_hold_a_2050 = s["A_fmv"][END] - sum_a_cost_p19
    wealth_sell_a_2050 = pa["A_sale_net_at_Y"] * (1 + INVEST) ** (END - Y)
    sum_noi_b1 = sum(pb["B_noi_b1"].values())
    wealth_rent_b_2050 = sum_noi_b1 + pb["B_fmv"][END]
    wealth_sell_b_2050 = pb["B_sale_net_at_Y"] * (1 + INVEST) ** (END - Y)

    # Estate exclusion vs. combined property value at Y
    excl = {t: A["M_FED_EXCL_2026"] * (1 + A["M_FED_INDEX"]) ** (t - BASE) for t in years}
    combined_fmv = {t: s["A_fmv"][t] + pb["B_fmv"][t] for t in years}

    out = {
        "inputs": {"inheritance_year": Y, "appreciation": apprec, "prop19_cap": CAP_AMT,
                   "rate_A_planning": RATE_A, "rate_B_official": RATE_B, "sale_cost": SALE_COST,
                   "transfer_tax_county": TRANSFER, "invest_return": INVEST, "growth_cap_prop13": GROWTH_CAP},
        "years": years,
        "A": {
            "fmv": s["A_fmv"], "assessed_parent_prop13": s["A_assessed_parent"], "tax_parent": s["A_tax_parent"],
            "taxable_prop19_after_Y": pa["A_taxable_p19"], "tax_prop19_after_Y": pa["A_tax_p19"],
            "taxable_reassessed_after_Y": pa["A_taxable_reassessed"], "tax_reassessed_after_Y": pa["A_tax_reassessed"],
            "insurance": s["A_insurance"], "water": s["A_water"], "solar_credit": s["A_solar_credit"], "maintenance": s["A_maintenance"],
            "annual_cost_parent": a_cost_parent, "annual_cost_heir_prop19": a_cost_p19, "annual_cost_heir_reassessed": a_cost_rent,
            "sale_net_at_Y": pa["A_sale_net_at_Y"],
        },
        "B": {k: v for k, v in pb.items() if k != "B_sale_net_at_Y"} | {"sale_net_at_Y": pb["B_sale_net_at_Y"]},
        "estate": {"exclusion": excl, "combined_fmv_A_plus_B": combined_fmv,
                   "headroom": {t: excl[t] - combined_fmv[t] for t in years}},
        "compare_2050": {
            "A_hold_live_net_wealth_excl_use_value": wealth_hold_a_2050,
            "A_sell_and_invest_value": wealth_sell_a_2050,
            "B_keep_rental_net_wealth_pretax": wealth_rent_b_2050,
            "B_sell_and_invest_value": wealth_sell_b_2050,
        },
    }
    return out


def to_str_keys(obj):
    if isinstance(obj, dict):
        return {str(k): to_str_keys(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [to_str_keys(v) for v in obj]
    return obj


def main():
    default = run(2045, A["M_APPREC"])
    sens = []
    for Y in (2040, 2045, 2050):
        for label, g in (("low_0pct", A["M_APPREC_LO"]), ("base_2.15pct", A["M_APPREC"]), ("high_4pct", A["M_APPREC_HI"])):
            r = run(Y, g)
            sens.append({"inheritance_year": Y, "scenario": label, "appreciation": g,
                         "A_fmv_at_Y": r["A"]["fmv"][Y], "A_taxable_prop19_at_Y": r["A"]["taxable_prop19_after_Y"][Y],
                         "A_tax_prop19_at_Y": r["A"]["tax_prop19_after_Y"][Y],
                         "A_tax_reassessed_at_Y": r["A"]["tax_reassessed_after_Y"][Y],
                         "B_fmv_at_Y": r["B"]["B_fmv"][Y], "B_tax_b1_at_Y": r["B"]["B_tax_b1"][Y],
                         "B_noi_b1_at_Y": r["B"]["B_noi_b1"][Y],
                         "A_sale_net_at_Y": r["A"]["sale_net_at_Y"], "B_sale_net_at_Y": r["B"]["sale_net_at_Y"],
                         "compare_2050": r["compare_2050"],
                         "exclusion_at_Y": r["estate"]["exclusion"][Y], "combined_fmv_at_Y": r["estate"]["combined_fmv_A_plus_B"][Y]})
    payload = {"generated_by": "model/project.py", "note": "Projections only. Inputs labelled UNVERIFIED are client-provided. Not facts.",
               "default_case": to_str_keys(default), "sensitivity": sens}
    os.makedirs(os.path.join(ROOT, "data/projections"), exist_ok=True)
    json.dump(payload, open(os.path.join(ROOT, "data/projections.json"), "w"), indent=2)

    # CSVs for the default case
    d = default
    ya = ["year", "A_fmv", "A_assessed_parent_prop13", "A_tax_parent", "A_tax_prop19_after_Y", "A_tax_reassessed_after_Y",
          "A_insurance", "A_water", "A_solar_credit", "A_maintenance", "A_annual_cost_parent", "A_annual_cost_heir_prop19"]
    with open(os.path.join(ROOT, "data/projections/property_A_default.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(ya)
        for t in d["years"]:
            w.writerow([t, round(d["A"]["fmv"][t]), round(d["A"]["assessed_parent_prop13"][t]), round(d["A"]["tax_parent"][t]),
                        round(d["A"]["tax_prop19_after_Y"].get(t, 0)) if t in d["A"]["tax_prop19_after_Y"] else "",
                        round(d["A"]["tax_reassessed_after_Y"].get(t, 0)) if t in d["A"]["tax_reassessed_after_Y"] else "",
                        round(d["A"]["insurance"][t]), round(d["A"]["water"][t]), round(d["A"]["solar_credit"][t]),
                        round(d["A"]["maintenance"][t]), round(d["A"]["annual_cost_parent"][t]),
                        round(d["A"]["annual_cost_heir_prop19"].get(t, 0)) if t in d["A"]["annual_cost_heir_prop19"] else ""])
    yb = ["year", "B_fmv", "B_assessed_parent_prop13", "B_tax_parent", "B_tax_b1_reassessed", "B_rent", "B_water", "B_elec", "B_insurance", "B_maintenance", "B_noi_b1_rental", "B_tax_b3_occupy_one_unit", "B_noi_b3"]
    with open(os.path.join(ROOT, "data/projections/property_B_default.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(yb)
        for t in d["years"]:
            B = d["B"]
            w.writerow([t, round(B["B_fmv"][t]), round(B["B_assessed_parent"][t]), round(B["B_tax_parent"][t]),
                        round(B["B_tax_b1"].get(t, 0)) if t in B["B_tax_b1"] else "",
                        round(B["B_rent"][t]), round(B["B_water"][t]), round(B["B_elec"][t]), round(B["B_insurance"][t]), round(B["B_maintenance"][t]),
                        round(B["B_noi_b1"].get(t, 0)) if t in B["B_noi_b1"] else "",
                        round(B["B_tax_b3"].get(t, 0)) if t in B["B_tax_b3"] else "",
                        round(B["B_noi_b3"].get(t, 0)) if t in B["B_noi_b3"] else ""])
    print("wrote data/projections.json and CSVs")
    c = default["compare_2050"]
    print({k: round(v) for k, v in c.items()})
    print("A FMV 2045", round(default["A"]["fmv"][2045]), "P19 tax 2045", round(default["A"]["tax_prop19_after_Y"][2045]),
          "reassessed tax 2045", round(default["A"]["tax_reassessed_after_Y"][2045]))
    print("B FMV 2045", round(default["B"]["B_fmv"][2045]), "B1 tax 2045", round(default["B"]["B_tax_b1"][2045]),
          "B1 NOI 2045", round(default["B"]["B_noi_b1"][2045]), "B3 tax", round(default["B"]["B_tax_b3"][2045]))
    print("Estate headroom 2045", round(default["estate"]["headroom"][2045]))


if __name__ == "__main__":
    main()
