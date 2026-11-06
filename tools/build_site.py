#!/usr/bin/env python3
"""Builds the GitHub Pages site in docs/ from data/*.json (no hand-typed numbers).

Run order:
    python3 tools/build_data.py     # property tax history + BOE checks
    python3 model/project.py        # projections
    python3 tools/build_site.py     # HTML pages + CSV downloads
    python3 tools/check_site.py     # consistency and privacy checks
"""
import csv
import html
import json
import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
DOCS = os.path.join(ROOT, "docs")
SEL_YEARS = [2026, 2030, 2035, 2040, 2045, 2050, 2055, 2060]


def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return json.load(f)


SOURCES = {s["id"]: s for s in load("sources.json")["sources"]}
TAXHIST = load("property_tax_history.json")
PROJ = load("projections.json")
TAXLAW = load("tax_law.json")
COSTS = load("cost_inputs.json")
FLAGS = load("flags.json")["flags"]
STEPS = load("process_steps.json")["steps"]


def e(x):
    return html.escape("" if x is None else str(x))


def money(x, dp=0):
    if x is None:
        return "not computed"
    return f"${x:,.{dp}f}"


def pct(x, dp=2):
    if x is None:
        return ""
    return f"{x:.{dp}f}%"


def src_links(ids, primary_url=None):
    """Render links for source IDs; primary_url first when given."""
    out = []
    seen = set()
    if primary_url:
        out.append(f'<a href="{e(primary_url)}" rel="noopener">official source</a>')
        seen.add(primary_url)
    for sid in ids or []:
        s = SOURCES.get(sid)
        if not s or not s.get("url") or s["url"] in seen:
            continue
        seen.add(s["url"])
        out.append(f'<a href="{e(s["url"])}" rel="noopener" title="{e(s["title"])}">{e(sid)}</a>')
    if not out:
        return '<span class="flag">no link</span>'
    return " ".join(out)


def status_badge(s):
    cls = {"verified": "ok", "partially_verified": "part", "pending": "pend", "unverified": "bad",
           "derived": "part", "user-supplied": "user", "user": "user", "assumption": "assume",
           "unverified ": "bad"}.get(s, "pend")
    label = {"verified": "Verified", "partially_verified": "Partly verified", "pending": "Pending",
             "unverified": "UNVERIFIED", "derived": "Derived", "user-supplied": "User figure (unverified)",
             "user": "User figure (unverified)", "assumption": "Assumption"}.get(s, s or "")
    return f'<span class="badge {cls}">{e(label)}</span>'


def page(title, body, active, file):
    nav = [("index.html", "Overview"), ("property-tax.html", "Property tax"), ("costs.html", "Costs"),
           ("tax-law.html", "Tax law"), ("inheritance-threshold.html", "Inheritance threshold"),
           ("projections.html", "Projections"), ("decision.html", "Live / rent / sell"),
           ("process.html", "Process"), ("flagged-for-review.html", "Flagged for Review"),
           ("sources.html", "Sources")]
    navhtml = "".join(f'<a href="{h}" class="{"on" if h == active else ""}">{t}</a>' for h, t in nav)
    doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} | Inheritance analysis (Property A and B)</title>
<link rel="stylesheet" href="assets/style.css">
</head><body>
<header><div class="wrap"><h1>Inheritance analysis: Property A and Property B</h1>
<p class="sub">Anonymized. Property A = Cupertino, Santa Clara County, CA. Property B = San Francisco, CA. Beneficiary and trust shown as [Beneficiary] and [Trust].</p>
<nav>{navhtml}</nav></div></header>
<main class="wrap">
<h2>{e(title)}</h2>
{body}
</main>
<footer class="wrap"><p>Not legal, tax or investment advice. Projections are labelled assumptions, not forecasts. Figures are sourced to official pages where noted; anything not verified is blank and listed on the <a href="flagged-for-review.html">Flagged for Review</a> page. Built from data/*.json on 2026-11-06.</p></footer>
</body></html>
"""
    with open(os.path.join(DOCS, file), "w", encoding="utf-8") as f:
        f.write(doc)


def table(headers, rows, cls=""):
    th = "".join(f"<th>{e(h)}</th>" for h in headers)
    trs = []
    for r in rows:
        trs.append("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>")
    return f'<div class="tablewrap"><table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{"".join(trs)}</tbody></table></div>'


def annual_row(rows, year):
    for r in rows:
        if r["year"] == year:
            return r
    return None


def build_all():
    os.makedirs(os.path.join(DOCS, "assets"), exist_ok=True)
    os.makedirs(os.path.join(DOCS, "data"), exist_ok=True)
    with open(os.path.join(DOCS, "assets", "style.css"), "w") as f:
        f.write(CSS)
    with open(os.path.join(DOCS, ".nojekyll"), "w") as f:
        f.write("")

    pa = PROJ["property_a"]
    pb = PROJ["property_b"]
    dec = PROJ["decision_a"]
    a_base = pa["no_transfer_base"]
    a2045q = annual_row(pa["inheritance"]["2045"]["qualifies_live_in"], 2045)
    a2045n = annual_row(pa["inheritance"]["2045"]["does_not_qualify"], 2045)
    b26 = annual_row(pb["base"], 2026)
    b40 = annual_row(pb["base"], 2040)
    th = {r["year"]: r for r in PROJ["inheritance_thresholds"]}
    grid = {(g["appreciation"], g["invest_return"], g["qualifies_live_in"]): g["breakeven_monthly_rent"] for g in dec["grid"]}
    be_q = grid[("3%", "4%", True)]
    be_n = grid[("3%", "4%", False)]
    rate_a = TAXHIST["derived_effective_rates"]["A"]["rate_pct"]
    rate_b = TAXHIST["derived_effective_rates"]["B"]["rate_pct"]
    flags_by_sev = {}
    for f_ in FLAGS:
        flags_by_sev[f_["severity"]] = flags_by_sev.get(f_["severity"], 0) + 1

    # ----------------------------------------------------------- Overview
    body = f"""
<section class="card">
<h3>What this site answers</h3>
<p>Inheriting Property A (Cupertino) through [Trust] around 2040-2050, compared with holding Property B (San Francisco). It covers property tax, assessment history, insurance, water, electricity, maintenance, federal and California law, the inheritance threshold, and the live / rent / sell decision.</p>
<ul>
<li><strong>Federal estate tax:</strong> the 2026 exclusion is {money(15_000_000)} per person (verified, IRS). Projected to {money(th[2040]["federal_exemption_base"])} in 2040 and {money(th[2050]["federal_exemption_base"])} in 2050 at a {PROJ["assumptions"]["inflation_base"]*100:.0f}% inflation assumption.</li>
<li><strong>California:</strong> no estate or inheritance tax (historic sources; current confirmation pending).</li>
<li><strong>Prop 19 is the main driver for Property A.</strong> In the 2045 base case, property tax is about {money(a2045q["property_tax"])} a year if the beneficiary occupies the home as a principal residence, and about {money(a2045n["property_tax"])} a year if not.</li>
<li><strong>Live / rent / sell (base case, 2045 inheritance, 10-year horizon, 3% appreciation, 4% investment return):</strong> keeping the home beats selling only if its rent (or imputed rent) is above about {money(be_q)} a month with occupancy, or {money(be_n)} without. With a 7% return, no rent level in the search range makes keeping better.</li>
<li><strong>Property B</strong> returns about {pct(b26["noi_yield_on_value"])} net of costs in 2026 at the user's rent, before income tax and before appreciation.</li>
</ul>
<p class="note">Figures in this summary come from data/projections.json and are only as reliable as the inputs flagged on the <a href="flagged-for-review.html">Flagged for Review</a> page.</p>
</section>
<section class="grid">
<a class="tile" href="property-tax.html"><h3>Property tax and assessment history</h3><p>Both properties, year by year, with BOE factor checks.</p></a>
<a class="tile" href="costs.html"><h3>Costs</h3><p>Water, electricity and solar, insurance, maintenance and rent.</p></a>
<a class="tile" href="tax-law.html"><h3>Tax law</h3><p>Federal, California and local rules, and pending changes.</p></a>
<a class="tile" href="inheritance-threshold.html"><h3>Inheritance threshold</h3><p>Federal exemption by year, 2026-2050.</p></a>
<a class="tile" href="projections.html"><h3>Projections</h3><p>Property A and B annual projections and assumptions.</p></a>
<a class="tile" href="decision.html"><h3>Live / rent / sell</h3><p>Break-even rent and what would change the answer.</p></a>
<a class="tile" href="process.html"><h3>Inheritance process</h3><p>Steps and deadlines, with sources.</p></a>
<a class="tile warn" href="flagged-for-review.html"><h3>Flagged for Review</h3><p>{len(FLAGS)} items: {flags_by_sev.get("high",0)} high, {flags_by_sev.get("review",0)} to review, {flags_by_sev.get("info",0)} info.</p></a>
</section>
<section class="card"><h3>How to read the site</h3>
<p><span class="badge ok">Verified</span> read from an official page. <span class="badge part">Partly verified</span> official URL or partial document read; re-check before relying on it. <span class="badge pend">Pending</span> identified but not read; not used in any figure. <span class="badge user">User figure (unverified)</span> supplied by the owner; used only in labelled projections. <span class="badge assume">Assumption</span> model input, not a sourced fact. Blank = not verified.</p></section>
"""
    page("Overview", body, "index.html", "index.html")

    # ----------------------------------------------------------- Property tax
    def hist_table(prop):
        rows = []
        for r in sorted([x for x in TAXHIST["rows"] if x["property"] == prop and x["measure"] == "assessed_value"], key=lambda z: -z["year"]):
            rows.append([str(r["year"]), money(r["value"]), pct(r["stated_pct"], 1) if r["stated_pct"] is not None else "",
                         pct(r["calc_pct"]) if r["calc_pct"] is not None else "",
                         f'{r["boe_factor"]:.5f}' if r["boe_factor"] else "",
                         money(r["boe_expected_value"]) if r["boe_expected_value"] else "",
                         e(r["check"]), status_badge("user-supplied"), src_links(r["source_ids"], "https://www.boe.ca.gov/proptaxes/pdf/lta26002.pdf")])
        return table(["Roll year", "Assessed value (user)", "Stated change", "Calculated change", "BOE factor (S01)", "BOE expected value", "Check", "Status", "Source"], rows, "dense")

    def tax_table(prop):
        rows = []
        for r in sorted([x for x in TAXHIST["rows"] if x["property"] == prop and x["measure"] == "property_tax"], key=lambda z: -z["year"]):
            rows.append([str(r["year"]), money(r["value"]) if r["value"] is not None else "blank (--)",
                         pct(r["stated_pct"], 1) if r["stated_pct"] is not None else "",
                         pct(r["calc_pct"]) if r["calc_pct"] is not None else "",
                         pct(r.get("tax_to_av_pct"), 3) if r.get("tax_to_av_pct") else "",
                         e(r["check"]), status_badge("user-supplied"), src_links(r["source_ids"])])
        return table(["Tax year", "Property tax (user)", "Stated change", "Calculated change", "Tax as % of AV", "Check", "Status", "Source"], rows, "dense")

    prop19 = [x for x in TAXLAW["property_tax_california"] if x["id"] in ("PT-01", "PT-02", "PT-03", "PT-04", "PT-05", "PT-06", "PT-07", "PT-08", "PT-09", "PT-10", "PT-11", "PT-12")]
    prow = []
    for r in prop19:
        prow.append([e(r["id"]), e(r["item"]), e(r["value"]), status_badge(r["status"]), src_links(r["source_ids"], r["source_url"])])
    body = f"""
<section class="card"><h3>Assessment history (user figures, checked against BOE)</h3>
<p>Assessed values are checked against the BOE inflation factor for each roll year (LTA 2026/002). Tax amounts cannot be checked against factors. Market value is not part of the Prop 13 assessment.</p>
<h4>Property A (Cupertino, Santa Clara County)</h4>
{hist_table("A")}
<h4>Property A: property tax</h4>
{tax_table("A")}
<h4>Property B (San Francisco)</h4>
{hist_table("B")}
<h4>Property B: property tax</h4>
{tax_table("B")}
<p>Derived effective rate on assessed value (2025, tax / AV): Property A {rate_a:.3f}%; Property B {rate_b:.3f}%. These are not official rates; see flags FLAG-TAXRATIO.</p>
</section>
<section class="card"><h3>Prop 13 and Prop 19 rules used in the model</h3>
{table(["ID", "Rule", "Value / effect", "Status", "Source"], prow, "dense")}
</section>
<section class="card"><h3>Property A projection: property tax by scenario (base case)</h3>
<p>Base case: 2% inflation, 3% appreciation. The taxable value is held at the Prop 13 base until a transfer. Model estimates only; not bills.</p>
{projection_tax_table(pa)}
</section>
"""
    page("Property tax and assessment history", body, "property-tax.html", "property-tax.html")

    # ----------------------------------------------------------- Costs
    crow = []
    for c in COSTS["rows"]:
        crow.append([e(c["id"]), e(c["category"]), e(c["property"]), e(c["item"]),
                     e(c["verified_value"]) if c["verified_value"] else "<em>blank (not verified)</em>",
                     status_badge(c["verified_status"]),
                     src_links(c["source_ids"], c["source_url"]),
                     e(c["user_input"]) if c["user_input"] else "",
                     status_badge(c["user_status"]) if c["user_status"] else "",
                     e(", ".join(c["flags"])) if c["flags"] else ""])
    body = f"""
<section class="card"><h3>Water, electricity, insurance, maintenance and rent</h3>
<p>Verified values appear in the third column; blanks are not verified. User inputs are shown separately, flagged as unverified, and used only in labelled projections.</p>
{table(["ID", "Category", "Prop.", "Item", "Verified value (official)", "Status", "Source", "User input (unverified)", "Status", "Flags"], crow, "dense")}
</section>
<section class="card"><h3>Modelled annual costs, base case (2026 $ / 2026 value)</h3>
<p>Water and electricity use the user's midpoints, escalated at the base inflation assumption. Insurance uses the user's estimate (both properties). Maintenance is an assumption (A 0.5%, B 1.0% of market value). All of these are unverified.</p>
{costs_table(pa, pb)}
</section>
"""
    page("Costs", body, "costs.html", "costs.html")

    # ----------------------------------------------------------- Tax law
    def law_rows(items):
        out = []
        for r in items:
            out.append([e(r["id"]), e(r["item"]), e(r["value"]), e(r.get("effective", "")), status_badge(r["status"]),
                        src_links(r["source_ids"], r.get("source_url")), e(r.get("note", ""))])
        return table(["ID", "Item", "Value / rule", "Effective", "Status", "Source", "Note"], out, "dense")

    pending_rows = [x for x in TAXLAW["federal"] if x["id"] == "FED-11"] + \
                   [x for x in TAXLAW["property_tax_california"] if x["id"] in ("PT-11", "PT-12")] + \
                   [x for x in TAXLAW["san_francisco_local"] if x["id"] in ("SF-02", "SF-03", "SF-04")] + \
                   [x for x in TAXLAW["california"] if x["id"] == "CA-05"]
    body = f"""
<section class="card"><h3>Federal</h3>{law_rows(TAXLAW["federal"])}</section>
<section class="card"><h3>California income and estate taxes</h3>{law_rows(TAXLAW["california"])}</section>
<section class="card"><h3>California property tax (Prop 13 and Prop 19)</h3>{law_rows(TAXLAW["property_tax_california"])}</section>
<section class="card"><h3>San Francisco local rules</h3>{law_rows(TAXLAW["san_francisco_local"])}</section>
<section class="card warn-card"><h3>Pending or unverified law changes</h3>
<p>These are not in the projections. Each one is also on the Flagged for Review page.</p>
{law_rows(pending_rows)}</section>
"""
    page("Tax law", body, "tax-law.html", "tax-law.html")

    # ----------------------------------------------------------- Inheritance threshold
    trow = []
    for y in [2026, 2030, 2035, 2040, 2045, 2050]:
        r = th[y]
        trow.append([str(y), money(r["federal_exemption_base"]), money(r["federal_exemption_high_inflation"]),
                     money(r["couple_with_portability_base"]),
                     src_links(["S07", "S08"] if y == 2026 else ["S08"], "https://www.irs.gov/newsroom/irs-releases-tax-inflation-adjustments-for-tax-year-2026-including-amendments-from-the-one-big-beautiful-bill")])
    body = f"""
<section class="card"><h3>Federal estate exclusion by year</h3>
<p>2026: {money(15_000_000)} per person (verified). From 2027 the exclusion is indexed for inflation (Rev. Proc. 2025-32, s.2.14). The index method was not verified; the projection is a labelled assumption.</p>
{table(["Year", "Exclusion, base (2% inflation)", "Exclusion, high (3.7% CPI)", "Couple with portability (base)", "Source"], trow)}
<p class="note">Full annual table: <a href="data/inheritance_thresholds.csv">CSV download</a>.</p>
</section>
<section class="card"><h3>What this means for the trust</h3>
<ul>
<li>An estate with a gross value under the exclusion owes no federal estate tax. Form 706 is required above the filing threshold, and it can also be filed to elect portability of a deceased spouse's unused exclusion (IRS, verified).</li>
<li>The threshold applies to the whole estate, not to Property A alone. Property A's value ({money(a_base[0]["market_value"])} in 2026 per user estimate) is only part of the estate.</li>
<li>California has no estate or inheritance tax (historic sources; pending current confirmation). The state threshold is therefore not a constraint.</li>
<li>The top federal estate tax rate is 40% (partially verified; flagged).</li>
</ul></section>
"""
    page("Inheritance threshold", body, "inheritance-threshold.html", "inheritance-threshold.html")

    # ----------------------------------------------------------- Projections
    prow_a = []
    for y in SEL_YEARS:
        r = annual_row(a_base, y)
        q = annual_row(pa["inheritance"]["2045"]["qualifies_live_in"], y)
        n = annual_row(pa["inheritance"]["2045"]["does_not_qualify"], y)
        prow_a.append([str(y), money(r["market_value"]), money(r["taxable_value"]), money(r["property_tax"]),
                       money(r["carrying_cost"]), money(q["taxable_value"]), money(q["property_tax"]),
                       money(n["property_tax"]), src_links(["S25", "S26", "S01"], "https://www.boe.ca.gov/proptaxes/pdf/lta26002.pdf")])
    prow_b = []
    for y in SEL_YEARS:
        r = annual_row(pb["base"], y)
        prow_b.append([str(y), money(r["market_value"]), money(r["taxable_value"]), money(r["property_tax"]),
                       money(r["rent_income"]), money(r["operating_costs"]), money(r["net_operating_income"]),
                       pct(r["noi_yield_on_value"]), src_links(["S27", "S28", "S25"], "https://www.sf.gov/news--annual-rent-increase-3126-22827-announced")])
    arows = []
    for k, v in PROJ["assumptions"].items():
        if isinstance(v, (int, float)):
            arows.append([e(k), pct(v * 100, 2) if abs(v) < 1 else money(v), "assumption", "", ""])
    alist = [
        ["Inflation (base)", pct(PROJ["assumptions"]["inflation_base"] * 100, 1), "Federal Reserve 2% longer-run goal (S26)", src_links(["S26"], "https://www.federalreserve.gov/monetarypolicy/2026-07-mpr-statement.htm")],
        ["Inflation (high)", pct(PROJ["assumptions"]["inflation_high"] * 100, 1), "BLS CPI-U, 12 months to Sept 2026 (S25)", src_links(["S25"], "https://www.bls.gov/news.release/cpi.nr0.htm")],
        ["Prop 13 factor", "min(inflation, 2%)", "BOE LTA 2026/002 (S01)", src_links(["S01"], "https://www.boe.ca.gov/proptaxes/pdf/lta26002.pdf")],
        ["Value-limit add-on after 2027", "grows with inflation (ASSUMPTION)", "BOE: $1,044,586 until 2/15/2027 (S02); adjusted every two years by FHFA HPI (S06)", src_links(["S02", "S06"], "https://www.boe.ca.gov/proptaxes/pdf/lta25009.pdf")],
        ["Appreciation (base / low / high)", "3% / 2% / 5% (ASSUMPTION)", "No official source. CPI shown for context only.", src_links(["S25"], "https://www.bls.gov/news.release/cpi.nr0.htm")],
        ["Investment return (low / high)", "4% / 7% (ASSUMPTION, pre-tax)", "No official source; for comparison only", src_links(["S16"], "https://www.ftb.ca.gov/file/personal/income-types/capital-gains-and-losses.html")],
        ["Selling cost", pct(PROJ["assumptions"]["selling_cost"] * 100, 1) + " (ASSUMPTION)", "Not sourced. Transfer tax not verified (flag FLAG-TRANSFER-TAX).", src_links(["S10"], "https://www.irs.gov/publications/p551")],
        ["Maintenance (A / B)", "0.5% / 1.0% of market value (ASSUMPTION)", "Not sourced. Linked to BLS for context.", src_links(["S25"], "https://www.bls.gov/news.release/cpi.nr0.htm")],
        ["SF rent growth (rent-controlled)", "1.6% (verified)", "SF Rent Board 3/1/2026 - 2/28/2027", src_links(["S27"], "https://www.sf.gov/news--annual-rent-increase-3126-22827-announced")],
        ["Cupertino rent growth (if rented)", "3% (ASSUMPTION)", "No verified rent input; used only in break-even calculation", src_links(["S34"], "https://www.huduser.gov/portal/datasets/fmr.html")],
        ["Post-legacy solar scenario", "$50/month electricity cost (ASSUMPTION)", "Solar credit lost. Interconnection date unknown.", src_links(["S22"], "https://www.cpuc.ca.gov/industries-and-topics/electrical-energy/demand-side-management/customer-generation/net-energy-metering-and-net-billing")],
    ]
    solar_lost = pa["solar_credit_lost_base"]
    lost_2045 = annual_row(solar_lost, 2045)
    base_2045 = annual_row(a_base, 2045)
    body = f"""
<section class="card"><h3>Property A: annual projection at selected years (base case, no transfer)</h3>
<p>Market value grows at the appreciation assumption; taxable value follows the Prop 13 factor. Columns on the right show 2045 inheritance outcomes (base case). Carrying cost = property tax + insurance + water + net electricity + maintenance.</p>
{table(["Year", "Market value (assumed)", "Taxable value (no transfer)", "Property tax", "Carrying cost", "2045 transfer: taxable value (occupied)", "2045 transfer: property tax (occupied)", "2045 transfer: property tax (not occupied)", "Source"], prow_a, "dense")}
<p class="note">Full annual tables: <a href="data/property_a_annual.csv">Property A CSV</a> and <a href="data/property_b_annual.csv">Property B CSV</a>. If the solar credit is lost, the 2045 carrying cost rises from {money(base_2045["carrying_cost"])} to {money(lost_2045["carrying_cost"])}.</p>
</section>
<section class="card"><h3>Property B: annual projection at selected years (base case)</h3>
<p>Rent grows at the verified 1.6% rent-control allowance (applies only to rent-controlled units). Net operating income is before income tax and before any mortgage (none provided). Yield = NOI / assumed market value.</p>
{table(["Year", "Market value (assumed)", "Taxable value", "Property tax", "Rent income", "Operating costs", "NOI", "NOI yield", "Source"], prow_b, "dense")}
</section>
<section class="card"><h3>Assumptions and their sources</h3>
{table(["Item", "Value", "Basis", "Source"], alist)}
</section>
"""
    page("Projections", body, "projections.html", "projections.html")

    # ----------------------------------------------------------- Decision
    grid_rows = []
    for g in dec["grid"]:
        if g["appreciation"] != "3%":
            continue
        grid_rows.append([g["invest_return"], "Yes (occupied)" if g["qualifies_live_in"] else "No (not occupied)",
                          money(g["breakeven_monthly_rent"]) if g["breakeven_monthly_rent"] is not None else "not reached (above $16,667/mo search limit)",
                          src_links(["S03", "S12"], "https://www.boe.ca.gov/proptaxes/pdf/lta26026.pdf")])
    full_grid = []
    for g in dec["grid"]:
        full_grid.append([g["appreciation"], g["invest_return"], "Yes" if g["qualifies_live_in"] else "No",
                          money(g["breakeven_monthly_rent"]) if g["breakeven_monthly_rent"] is not None else "not reached",
                          src_links(["S03", "S10", "S12"], "https://www.boe.ca.gov/proptaxes/pdf/lta26026.pdf")])
    body = f"""
<section class="card"><h3>Live / rent / sell for Property A</h3>
<p>Scenario: beneficiary inherits in {dec["inherit_year"]}; comparison over {dec["horizon_years"]} years. Selling the home at inheritance gives a near-zero gain, because the basis is the date-of-death value (IRS Pub 551). Keeping the home earns rent (or imputed rent from living there) and bears the carrying cost. The table gives the monthly rent at which keeping and selling give the same value.</p>
<h4>Break-even monthly rent, 3% appreciation</h4>
{table(["Investment return (after assumed selling cost)", "Prop 19 occupancy", "Break-even rent (2045 dollars, per month)", "Source"], grid_rows)}
<p>Sell-and-invest value after {dec["horizon_years"]} years: {money(dec["sell_value_10y_at_4pct_3pct"])} at 4% return; {money(dec["sell_value_10y_at_7pct_3pct"])} at 7% return (3% appreciation).</p>
</section>
<section class="card"><h3>Full sensitivity grid</h3>
<p>Each row solves for the monthly rent that makes keeping equal to selling. "not reached" means no rent in the search range does so.</p>
{table(["Appreciation", "Investment return", "Occupied under Prop 19", "Break-even rent per month", "Source"], full_grid, "dense")}
</section>
<section class="card"><h3>What the numbers say</h3>
<ul>
<li><strong>Occupancy matters.</strong> With occupancy the break-even rent is {money(be_q)}/month; without it, {money(be_n)}/month. Reassessment without occupancy adds about {money(a2045n["property_tax"] - a2045q["property_tax"])} a year in property tax in 2045 (base case).</li>
<li><strong>The return assumption decides it.</strong> At a 7% return, selling and investing wins at any rent in the search range. At 4% (2045 inheritance, occupied), the break-even is {money(grid[("2%","4%",True)])} a month at 2% appreciation, {money(grid[("3%","4%",True)])} at 3%, and {money(grid[("5%","4%",True)])} at 5%.</li>
<li><strong>Maintenance is a large cost.</strong> The 0.5% of value assumption is about {money(base_2045["maintenance"])} a year in 2045. Replace it with the actual figure before deciding.</li>
<li><strong>Property B</strong> yields {pct(b26["noi_yield_on_value"])} in 2026 before income tax and before appreciation. With 3% appreciation the total pre-tax return is roughly {b26["noi_yield_on_value"] + 3:.1f}%, below a 7% investment return and above a 4% return. No tax or mortgage is included.</li>
</ul>
</section>
<section class="card warn-card"><h3>Recommendation (within the stated assumptions)</h3>
<p>On these assumptions, <strong>selling and investing is the default</strong> unless verified rent for Property A (or a real living benefit that the family would otherwise pay for) exceeds the break-even above. If the beneficiary will live in the home, the occupancy condition for Prop 19 must be met and documented, because it lowers the break-even by about {money(be_n - be_q)} a month in 2045 terms.</p>
<p>Before deciding, verify: the market values (appraisals), the solar interconnection date and tariff, the maintenance cost, the Cupertino rent, the beneficiary's residency, and the investment return the family can actually obtain. This is not financial or legal advice.</p>
</section>
"""
    page("Live / rent / sell", body, "decision.html", "decision.html")

    # ----------------------------------------------------------- Process
    srow = []
    for s in STEPS:
        srow.append([str(s["step"]), e(s["when"]), e(s["action"]), src_links(s["source_ids"])])
    body = f"""
<section class="card"><h3>Inheritance and transfer process</h3>
<p>Steps and deadlines are taken from the cited sources. A qualified professional should confirm each one for the specific trust and beneficiary.</p>
{table(["Step", "When", "Action", "Source"], srow)}
</section>
"""
    page("Inheritance process", body, "process.html", "process.html")

    # ----------------------------------------------------------- Flags
    frow = []
    for f_ in FLAGS:
        frow.append([e(f_["id"]), f'<span class="sev {e(f_["severity"])}">{e(f_["severity"])}</span>', e(f_["property"]),
                     e(f_["topic"]), e(f_["detail"]), e(f_["action"]), src_links(f_["source_ids"], f_.get("source_url"))])
    body = f"""
<section class="card warn-card"><h3>Flagged for Review</h3>
<p>{len(FLAGS)} items. Flagged items do not block the merge. Each needs review or an official check before any decision. High items could change the decision.</p>
{table(["ID", "Severity", "Property", "Topic", "Detail", "Action", "Source"], frow, "dense")}
</section>
"""
    page("Flagged for Review", body, "flagged-for-review.html", "flagged-for-review.html")

    # ----------------------------------------------------------- Sources
    srcr = []
    for sid, s in SOURCES.items():
        srcr.append([e(sid), e(s["publisher"]), e(s["title"]), status_badge(s["status"]),
                     f'<a href="{e(s["url"])}" rel="noopener">{e(s["url"])}</a>' if s.get("url") else "user-supplied",
                     e(s.get("used_for", ""))])
    body = f"""
<section class="card"><h3>Sources</h3>
<p>All sources were retrieved 2026-11-06. Status legend: verified, partly verified (URL or partial read), pending (not read; not used), user (site owner's figures; unverified). Non-official sources are not used in any table.</p>
{table(["ID", "Publisher", "Title", "Status", "URL", "Used for"], srcr, "dense")}
</section>
"""
    page("Sources", body, "sources.html", "sources.html")

    # ----------------------------------------------------------- CSVs
    write_csv(os.path.join(DOCS, "data", "property_a_annual.csv"), a_base, pa["inheritance"],
              ["year", "market_value", "taxable_value", "property_tax", "insurance", "water", "electricity_net", "maintenance", "carrying_cost"])
    with open(os.path.join(DOCS, "data", "property_b_annual.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(pb["base"][0].keys()))
        w.writeheader()
        w.writerows(pb["base"])
    with open(os.path.join(DOCS, "data", "inheritance_thresholds.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(PROJ["inheritance_thresholds"][0].keys()))
        w.writeheader()
        w.writerows(PROJ["inheritance_thresholds"])
    for name in ["projections.json", "property_tax_history.json", "sources.json", "flags.json", "tax_law.json", "cost_inputs.json"]:
        shutil.copy(os.path.join(DATA, name), os.path.join(DOCS, "data", name))
    print("site built in docs/")


def costs_table(pa, pb):
    rows = []
    a = pa["no_transfer_base"]
    b = pb["base"]
    for y in [2026, 2040, 2050]:
        ra = annual_row(a, y)
        rb = annual_row(b, y)
        rows.append([str(y), money(ra["insurance"]), money(ra["water"]), money(ra["electricity_net"]), money(ra["maintenance"]),
                     money(rb["insurance"]), money(rb["water"]), money(rb["electricity"]), money(rb["maintenance"])])
    for r in rows:
        r.append(src_links(["S20", "S23", "S22", "S25"], "https://www.insurance.ca.gov/01-consumers/105-type/5-residential/index.cfm"))
    return table(["Year", "A insurance", "A water", "A electricity (net)", "A maintenance", "B insurance", "B water + sewer", "B electricity", "B maintenance", "Source"], rows, "dense") + \
        '<p class="note">Insurance = user estimate $1,500/yr, escalated at base inflation. Electricity for A is a net credit (negative). Sources: see the table above.</p>'


def projection_tax_table(pa):
    rows = []
    base = pa["no_transfer_base"]
    for y in [2026, 2030, 2035, 2040, 2045, 2050]:
        r = annual_row(base, y)
        q = annual_row(pa["inheritance"]["2040"]["qualifies_live_in"], y) if y >= 2040 else None
        n = annual_row(pa["inheritance"]["2040"]["does_not_qualify"], y) if y >= 2040 else None
        rows.append([str(y), money(r["property_tax"]), money(q["property_tax"]) if q else "",
                     money(n["property_tax"]) if n else "",
                     src_links(["S01", "S04"], "https://www.boe.ca.gov/proptaxes/pdf/lta26002.pdf")])
    return table(["Year", "Property tax, no transfer", "Property tax, 2040 transfer, occupied", "Property tax, 2040 transfer, not occupied", "Source"], rows)


def write_csv(path, base, inh, cols):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["scenario"] + cols)
        for r in base:
            w.writerow(["no_transfer"] + [r[c] for c in cols])
        for y, sc in inh.items():
            for label, rows in [("occupied_" + y, sc["qualifies_live_in"]), ("not_occupied_" + y, sc["does_not_qualify"])]:
                for r in rows:
                    w.writerow([label] + [r[c] for c in cols])


CSS = """
:root{--ink:#1d2430;--mut:#5a6372;--line:#dfe3ea;--bg:#f7f8fa;--ok:#1f7a3f;--part:#9a6400;--pend:#4a5568;--bad:#b42318;--user:#5b3fa0;--assume:#0b6e8c;--warn:#fff7e6}
*{box-sizing:border-box}body{margin:0;font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:var(--ink);background:var(--bg);line-height:1.5}
.wrap{max-width:1200px;margin:0 auto;padding:0 20px}
header{background:#14213d;color:#fff;padding:20px 0 10px}header h1{margin:0;font-size:1.5rem}header .sub{color:#c9d2e3;margin:4px 0 12px;font-size:.9rem}
nav{display:flex;flex-wrap:wrap;gap:6px 14px;padding-bottom:10px}nav a{color:#dbe4f5;text-decoration:none;font-size:.9rem;padding:3px 0}nav a.on,nav a:hover{color:#fff;border-bottom:2px solid #fca311}
main{padding:20px 0}h2{margin:8px 0 14px}h3{margin:6px 0 10px}h4{margin:18px 0 8px;color:#2a3648}
.card{background:#fff;border:1px solid var(--line);border-radius:10px;padding:18px 20px;margin:0 0 18px}
.warn-card{background:var(--warn);border-color:#f2d59c}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:14px;margin-bottom:18px}
.tile{display:block;background:#fff;border:1px solid var(--line);border-radius:10px;padding:14px 16px;text-decoration:none;color:var(--ink)}
.tile:hover{border-color:#14213d;box-shadow:0 2px 8px rgba(0,0,0,.06)}.tile h3{font-size:1rem;margin:0 0 6px}.tile p{margin:0;color:var(--mut);font-size:.9rem}
.tile.warn{border-color:#f2d59c;background:var(--warn)}
.tablewrap{overflow-x:auto;margin:10px 0}table{border-collapse:collapse;width:100%;background:#fff;font-size:.9rem}
th,td{border:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}th{background:#eef2f8;font-weight:600}
table.dense td{font-size:.85rem}
.badge{display:inline-block;padding:1px 7px;border-radius:999px;font-size:.78rem;font-weight:600;color:#fff;white-space:nowrap}
.badge.ok{background:var(--ok)}.badge.part{background:var(--part)}.badge.pend{background:var(--pend)}.badge.bad{background:var(--bad)}.badge.user{background:var(--user)}.badge.assume{background:var(--assume)}
.sev{font-weight:700;text-transform:uppercase;font-size:.78rem}.sev.high{color:var(--bad)}.sev.review{color:var(--part)}.sev.info{color:var(--pend)}
.flag{color:var(--bad);font-weight:600}.note{color:var(--mut);font-size:.9rem}
footer{color:var(--mut);font-size:.85rem;padding:14px 0 30px}footer a{color:#14213d}
a{color:#14213d}
"""

if __name__ == "__main__":
    build_all()
