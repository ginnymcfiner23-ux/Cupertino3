#!/usr/bin/env python3
"""Builds data/property_tax_history.json from the user-supplied tables and the BOE factor table.

User figures are anonymized: Property A = Cupertino (Santa Clara County, CA); Property B = San Francisco, CA.
Each assessed-value (AV) change is checked against the BOE inflation factor for that roll year
(source: BOE LTA 2026/002, S01). Tax changes cannot be checked against BOE factors, because they
depend on bonds, direct assessments and exemptions; those rows are flagged for bill-level review.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Roll year -> BOE factor (LTA 2026/002 row "Y-(Y+1)"). Only the rows needed for the history.
BOE_FACTOR = {
    2014: 1.00454,  # 2014-15 (0.45%)
    2015: 1.01998,  # 2015-16 (2.00%)
    2016: 1.01525,  # 2016-17 (1.53%)
    2017: 1.02,     # 2017-18
    2018: 1.02,     # 2018-19
    2019: 1.02,     # 2019-20
    2020: 1.02,     # 2020-21
    2021: 1.01036,  # 2021-22 (1.04%)
    2022: 1.02,     # 2022-23
    2023: 1.02,     # 2023-24
    2024: 1.02,     # 2024-25
    2025: 1.02,     # 2025-26
    2026: 1.02,     # 2026-27
}

# User tables: year -> (value, stated % change or None)
A_TAX = {2026: (None, None), 2025: (7207, 2.9), 2024: (7003, 1.2), 2023: (6917, 2.4), 2022: (6755, 1.4),
         2021: (6662, 1.5), 2020: (6565, None), 2019: (6565, 2.8), 2018: (6383, None), 2017: (6383, -0.5),
         2016: (6414, 4.6), 2015: (6130, 2.8), 2014: (5965, None)}
A_AV = {2026: (550537, 2), 2025: (539743, 2), 2024: (529161, 2), 2023: (518786, 2), 2022: (508614, 2),
        2021: (498642, 1), 2020: (493530, 2), 2019: (483854, 2), 2018: (474368, 2), 2017: (465067, 2),
        2016: (455949, 1.5), 2015: (449101, 2), 2014: (440305, 0.5)}
B_TAX = {2025: (2439, 5.3), 2024: (2315, 6.2), 2023: (2179, 3.4), 2022: (2107, 2), 2021: (2066, -5.9),
         2020: (2197, 3), 2019: (2134, 3.5), 2018: (2061, 18.4), 2017: (1740, 3.9), 2016: (1675, 1.6)}
B_AV = {2025: (114248, 2), 2024: (112008, 2), 2023: (109814, 2), 2022: (107662, 2), 2021: (105595, 1),
        2020: (104513, 2), 2019: (102465, 2), 2018: (100456, 2), 2017: (98488, 2), 2016: (96557, 1.5)}

OFFICIAL_BOE = "S01"
OFFICIAL_A_PORTAL = "S29"
OFFICIAL_B_PORTAL = "S28"


def av_rows(prop, av_table, portal):
    rows = []
    for y in sorted(av_table):
        val, stated = av_table[y]
        prev = av_table.get(y - 1)
        row = {"property": prop, "year": y, "measure": "assessed_value", "value": val,
               "stated_pct": stated, "calc_pct": None, "boe_factor": BOE_FACTOR.get(y),
               "boe_expected_value": None, "check": "no prior year in table", "flags": [],
               "source_ids": [OFFICIAL_BOE, portal], "status": "user-supplied"}
        if prev:
            pv = prev[0]
            row["calc_pct"] = round((val / pv - 1) * 100, 2)
            f = BOE_FACTOR.get(y)
            if f:
                exp = round(pv * f)
                row["boe_expected_value"] = exp
                diff = val - exp
                if abs(diff) <= 5:
                    row["check"] = "matches BOE factor (within $5)"
                else:
                    row["check"] = f"differs from BOE factor by ${diff:+,}"
                    row["flags"].append("AV-BOE-DIFF")
                boe_pct = round((f - 1) * 100, 3)
                if stated is not None:
                    # Labels use one-decimal precision (e.g. 1.525% shown as 1.5%; 1.036% shown as 1.0%).
                    if abs(round(boe_pct, 1) - stated) <= 0.05:
                        row["check"] += f"; stated {stated}% consistent with BOE {boe_pct}% at one-decimal rounding"
                    else:
                        row["flags"].append("AV-LABEL")
                        row["check"] += f"; stated {stated}% differs from BOE {boe_pct}%"
        rows.append(row)
    return rows


def tax_rows(prop, tax_table, portal, av_table):
    rows = []
    for y in sorted(tax_table):
        val, stated = tax_table[y]
        prev = tax_table.get(y - 1)
        row = {"property": prop, "year": y, "measure": "property_tax", "value": val,
               "stated_pct": stated, "calc_pct": None, "boe_factor": None, "boe_expected_value": None,
               "check": "", "flags": [], "source_ids": [portal], "status": "user-supplied"}
        if val is None:
            row["check"] = "not yet billed (user table shows '--')"
            row["flags"].append("TAX-MISSING")
        if prev and prev[0] is not None and val is not None:
            row["calc_pct"] = round((val / prev[0] - 1) * 100, 2)
            if stated is None:
                row["check"] = f"no % given; identical to prior year" if val == prev[0] else f"no % given; calculated {row['calc_pct']}%"
                if val == prev[0]:
                    row["flags"].append("TAX-IDENTICAL")
            elif abs(stated - row["calc_pct"]) > 0.15:
                row["check"] = f"stated {stated}% vs calculated {row['calc_pct']}%"
                row["flags"].append("TAX-LABEL")
            else:
                row["check"] = "matches stated change (rounding)"
        if val is not None and y in av_table:
            row["tax_to_av_pct"] = round(val / av_table[y][0] * 100, 3)
        rows.append(row)
    return rows


def main():
    rows = []
    rows += av_rows("A", A_AV, OFFICIAL_A_PORTAL)
    rows += tax_rows("A", A_TAX, OFFICIAL_A_PORTAL, A_AV)
    rows += av_rows("B", B_AV, OFFICIAL_B_PORTAL)
    rows += tax_rows("B", B_TAX, OFFICIAL_B_PORTAL, B_AV)

    # Derived effective tax rate on assessed value (2025), used by the projection model.
    derived = {
        "A": {"year": 2025, "tax": A_TAX[2025][0], "av": A_AV[2025][0],
              "rate_pct": round(A_TAX[2025][0] / A_AV[2025][0] * 100, 3)},
        "B": {"year": 2025, "tax": B_TAX[2025][0], "av": B_AV[2025][0],
              "rate_pct": round(B_TAX[2025][0] / B_AV[2025][0] * 100, 3)},
    }
    out = {"generated_from": "tools/build_data.py (user tables; BOE LTA 2026/002 factors)",
           "boe_factors_used": {str(k): v for k, v in BOE_FACTOR.items()},
           "derived_effective_rates": derived,
           "rows": rows}
    with open(os.path.join(ROOT, "data", "property_tax_history.json"), "w") as f:
        json.dump(out, f, indent=2)
    print("wrote data/property_tax_history.json with", len(rows), "rows")


if __name__ == "__main__":
    main()
