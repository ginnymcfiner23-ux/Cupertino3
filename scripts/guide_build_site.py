"""Build the static site into guide/ from data/guide/*.json.

No external CDN resources. All styles are inline (<style> in each page).
Run:  python3 scripts/guide_build_site.py   (after python3 model/guide_project.py)
"""
import json, os, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = lambda p: json.load(open(os.path.join(ROOT, p)))
SRC = {s["id"]: s for s in D("data/guide/sources.json")["sources"]}
FACTS = D("data/guide/facts.json")["rows"]
HIST = D("data/guide/property_tax_history.json")
ASSUME = D("data/guide/assumptions.json")["inputs"]
A = {x["id"]: x for x in ASSUME}
IRR = D("data/guide/irregularities.json")["irregularities"]
LEG = D("data/guide/legislation.json")["items"]
STEPS = D("data/guide/inheritance_steps.json")["steps"]
PROJ = D("data/guide/projections.json")
DEF = PROJ["default_case"]
SENS = PROJ["sensitivity"]
INH = DEF["inputs"]["inheritance_year"]
GEN_DATE = "2026-11-06"

CSS = """
body{margin:0;font-family:Arial,Helvetica,sans-serif;background:#f4f6f9;color:#1d2530;line-height:1.45}
header{background:#1f3a5f;color:#fff;padding:14px 22px}
header h1{margin:0;font-size:20px;font-weight:600}
header .sub{font-size:12px;opacity:.85;margin-top:2px}
nav{background:#2a4d7a;padding:8px 22px}
nav a{color:#fff;text-decoration:none;margin-right:14px;font-size:13px;display:inline-block;padding:3px 0}
nav a:hover{text-decoration:underline}
main{padding:18px 22px;max-width:1280px}
h2{font-size:18px;color:#1f3a5f;margin:26px 0 8px;border-bottom:2px solid #d5deea;padding-bottom:4px}
h3{font-size:15px;color:#2a4d7a;margin:18px 0 6px}
.cards{display:flex;flex-wrap:wrap;gap:12px;margin:10px 0 14px}
.card{background:#fff;border:1px solid #d5deea;border-radius:6px;padding:12px 14px;min-width:200px;flex:1}
.card .k{font-size:12px;color:#55657a;text-transform:uppercase;letter-spacing:.03em}
.card .v{font-size:22px;font-weight:700;color:#1f3a5f;margin-top:4px}
.card .n{font-size:12px;color:#55657a;margin-top:4px}
table{border-collapse:collapse;width:100%;background:#fff;font-size:13px;margin:6px 0 16px}
th{background:#e7edf5;color:#1f3a5f;text-align:left;padding:7px 8px;border-bottom:1px solid #c5d1e2;vertical-align:bottom}
td{padding:6px 8px;border-bottom:1px solid #edf1f6;vertical-align:top}
tr:nth-child(even) td{background:#fafbfd}
td.num,th.num{text-align:right;white-space:nowrap}
.badge{display:inline-block;font-size:11px;padding:2px 7px;border-radius:10px;font-weight:600;white-space:nowrap}
.ver{background:#d8f0df;color:#14532d}
.unv{background:#fde9c4;color:#7a4b00}
.warn{background:#fff3cd;border:1px solid #f0d37a;border-radius:6px;padding:10px 12px;margin:10px 0;font-size:13px}
.note{background:#eef4fb;border:1px solid #c9d9ee;border-radius:6px;padding:10px 12px;margin:10px 0;font-size:13px}
.sev-high{color:#9b1c1c;font-weight:700}.sev-medium{color:#7a4b00;font-weight:700}.sev-low{color:#55657a;font-weight:700}
a{color:#1d5fa8}
small,.small{font-size:12px;color:#55657a}
footer{padding:14px 22px;font-size:12px;color:#55657a;border-top:1px solid #d5deea;margin-top:24px}
.blank{color:#9aa6b5;font-style:italic}
"""

NAV = [("index.html", "Dashboard"), ("executive-summary.html", "Executive summary"),
       ("property-tax.html", "Property tax & Prop 19"), ("federal-estate.html", "Federal estate"),
       ("california-tax.html", "California tax"), ("utilities.html", "Water & electricity"),
       ("insurance.html", "Insurance"), ("rental-sf.html", "Property B (SF rental)"),
       ("projections.html", "Projections"), ("decision-guide.html", "Decision guide"),
       ("legislation.html", "Pending law"), ("inheritance-steps.html", "Inheritance steps"),
       ("flagged.html", "Flagged for Review"), ("sources.html", "Sources")]


def esc(x):
    return html.escape("" if x is None else str(x))


def money(x, dec=0):
    if x is None or x == "":
        return '<span class="blank">—</span>'
    return f"${x:,.{dec}f}"


def pct(x, dec=2):
    return f"{x*100:.{dec}f}%"


def src_links(ids):
    out = []
    for i in ids:
        s = SRC.get(i)
        if not s:
            continue
        out.append(f'<a href="{esc(s["url"])}" target="_blank" rel="noopener" title="{esc(s["title"])}">{i}</a>')
    return ", ".join(out) if out else '<span class="small">none (unverified)</span>'


def badge(status):
    if status == "VERIFIED":
        return '<span class="badge ver">VERIFIED</span>'
    return '<span class="badge unv">UNVERIFIED</span>'


def table(headers, rows, num_cols=()):
    h = "".join(f'<th class="num">{esc(x)}</th>' if i in num_cols else f"<th>{esc(x)}</th>" for i, x in enumerate(headers))
    body = []
    for r in rows:
        cells = []
        for i, c in enumerate(r):
            cls = ' class="num"' if i in num_cols else ""
            cells.append(f"<td{cls}>{c}</td>")
        body.append("<tr>" + "".join(cells) + "</tr>")
    return f"<table><thead><tr>{h}</tr></thead><tbody>{''.join(body)}</tbody></table>"


def page(fname, title, body, active):
    links = []
    for f, t in NAV:
        style = ' style="font-weight:700"' if f == active else ""
        links.append('<a href="' + f + '"' + style + '>' + esc(t) + '</a>')
    nav = "".join(links)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} | Inheritance decision guide</title>
<style>{CSS}</style></head>
<body>
<header><h1>Inheritance decision guide: Cupertino (A) and San Francisco (B)</h1>
<div class="sub">Source-linked analysis and projections. Not legal or tax advice. Last updated {GEN_DATE}.</div></header>
<nav>{nav}</nav>
<main>
{body}
</main>
<footer>Projections use labelled assumptions and client inputs (marked UNVERIFIED). Official sources are linked in each table. Source list: <a href="sources.html">sources.html</a>. Model: <code>model/guide_project.py</code>. Generated by <code>scripts/guide_build_site.py</code>.</footer>
</body></html>"""


def facts_table(category, extra_cols=None):
    rows = []
    for r in FACTS:
        if r["category"] != category:
            continue
        val = r["value"]
        if r["status"] == "UNVERIFIED":
            val_cell = '<span class="blank">blank - unverified</span>'
        else:
            val_cell = esc(val)
        rows.append([esc(r["id"]), esc(r["item"]), val_cell, badge(r["status"]), src_links(r["sources"]), esc(r["note"])])
    return table(["ID", "Item", "Verified value", "Status", "Official source", "Note"], rows)


SRC_HIST = ["S06", "S07", "S08"]


def fmt_hist(rows):
    out = []
    for r in rows:
        out.append([str(r["year"]), money(r["assessed"]), esc(r["assessed_change"] or ""), money(r["tax"]),
                    esc(r["tax_change"] or ""), '<span class="blank">blank - unverified</span>',
                    '<span class="badge unv">UNVERIFIED (client)</span>', src_links(SRC_HIST)])
    return out


def proj_tables():
    A_ = DEF["A"]; B_ = DEF["B"]
    years = DEF["years"]
    rows_a = []
    for t in years:
        p19 = A_["tax_prop19_after_Y"].get(str(t))
        rea = A_["tax_reassessed_after_Y"].get(str(t))
        cost = A_["annual_cost_heir_prop19"].get(str(t))
        marker = " (inheritance)" if t == INH else ""
        rows_a.append([f"{t}{marker}", money(A_["fmv"][str(t)]), money(A_["assessed_parent_prop13"][str(t)]),
                       money(A_["tax_parent"][str(t)]),
                       money(p19) if p19 is not None else '<span class="blank">n/a</span>',
                       money(rea) if rea is not None else '<span class="blank">n/a</span>',
                       money(A_["insurance"][str(t)]), money(A_["water"][str(t)]),
                       money(-A_["solar_credit"][str(t)]), money(A_["maintenance"][str(t)]),
                       money(cost) if cost is not None else '<span class="blank">n/a</span>',
                       src_links(['S01','S06','S08','S20','S30'])])
    ta = table(["Year", "Market value (projection)", "Assessed value, parent (Prop 13)", "Property tax, parent (projection)",
                f"Tax if heir lives in (Prop 19, from {INH})", f"Tax if reassessed (from {INH})",
                "Insurance (client est.)", "Water (client est.)", "Solar net credit (client est.)", "Maintenance (model)",
                "Annual cost, heir lives in (Prop 19)", "Official source"],
               rows_a, num_cols=tuple(range(1, 11)))
    rows_b = []
    for t in years:
        tb1 = B_["B_tax_b1"].get(str(t)); nb1 = B_["B_noi_b1"].get(str(t))
        tb3 = B_["B_tax_b3"].get(str(t)); nb3 = B_["B_noi_b3"].get(str(t))
        marker = " (inheritance)" if t == INH else ""
        rows_b.append([f"{t}{marker}", money(B_["B_fmv"][str(t)]), money(B_["B_assessed_parent"][str(t)]),
                       money(B_["B_tax_parent"][str(t)]), money(B_["B_rent"][str(t)]), money(B_["B_water"][str(t)]),
                       money(B_["B_elec"][str(t)]), money(B_["B_insurance"][str(t)]), money(B_["B_maintenance"][str(t)]),
                       money(tb1) if tb1 is not None else '<span class="blank">n/a</span>',
                       money(nb1) if nb1 is not None else '<span class="blank">n/a</span>',
                       money(tb3) if tb3 is not None else '<span class="blank">n/a</span>',
                       money(nb3) if nb3 is not None else '<span class="blank">n/a</span>',
                       src_links(['S03','S07','S22','S25','S29'])])
    tb = table(["Year", "Market value (projection)", "Assessed, parent (Prop 13)", "Tax, parent (projection)",
                "Rent, 2 units (client; 1.6% cap)", "Water (client est.)", "Electricity (client est.)",
                "Insurance (client est.)", "Maintenance (model)",
                f"Tax if rented (reassessed, from {INH})", "Net operating income if rented (pre income tax)",
                f"Tax if heir occupies 1 unit (illustrative)", "NOI if heir occupies 1 unit (pre income tax)", "Official source"],
               rows_b, num_cols=tuple(range(1, 13)))
    return ta, tb


def sens_table():
    rows = []
    for x in SENS:
        rows.append([str(x["inheritance_year"]), x["scenario"].replace("_", " "), pct(x["appreciation"]),
                     money(x["A_fmv_at_Y"]), money(x["A_tax_prop19_at_Y"]), money(x["A_tax_reassessed_at_Y"]),
                     money(x["B_fmv_at_Y"]), money(x["B_tax_b1_at_Y"]), money(x["B_noi_b1_at_Y"]), src_links(['S01', 'S06', 'S07', 'S08'])])
    return table(["Inheritance year", "Scenario", "Appreciation / yr", "A market value at inheritance", "A tax, Prop 19",
                  "A tax, reassessed", "B market value at inheritance", "B tax if rented", "B NOI if rented (pre-tax)", "Official source"],
                 rows, num_cols=tuple(range(3, 9)))


def build():
    files = {}
    C = DEF["compare_2050"]
    ta, tb = proj_tables()
    hi = [x for x in SENS if x["inheritance_year"] == INH and x["scenario"] == "base_2.15pct"][0]
    A_fmv = DEF["A"]["fmv"][str(INH)]; B_fmv = DEF["B"]["B_fmv"][str(INH)]
    p19 = DEF["A"]["tax_prop19_after_Y"][str(INH)]; rea = DEF["A"]["tax_reassessed_after_Y"][str(INH)]
    headroom = DEF["estate"]["headroom"][str(INH)]
    counts_v = sum(1 for r in FACTS if r["status"] == "VERIFIED")
    counts_u = sum(1 for r in FACTS if r["status"] == "UNVERIFIED")
    flagged_n = len(IRR)

    # ---------- index ----------
    cards = f"""
<div class="cards">
 <div class="card"><div class="k">Property A projected value at {INH} (base)</div><div class="v">{money(A_fmv)}</div><div class="n">Projection; client estimate $3.1M in 2026 (UNVERIFIED), 2.15%/yr reference.</div></div>
 <div class="card"><div class="k">A tax at {INH} if heir lives in (Prop 19)</div><div class="v">{money(p19)}</div><div class="n">vs {money(rea)} if reassessed to market</div></div>
 <div class="card"><div class="k">Property B projected value at {INH} (base)</div><div class="v">{money(B_fmv)}</div><div class="n">Projection; client estimate $1.8M in 2026 (UNVERIFIED).</div></div>
 <div class="card"><div class="k">Federal estate headroom at {INH} (illustrative)</div><div class="v">{money(headroom)}</div><div class="n">Exclusion indexed at 2%/yr (assumption) minus A+B value.</div></div>
 <div class="card"><div class="k">Verified rows / unverified rows</div><div class="v">{counts_v} / {counts_u}</div><div class="n">Unverified values are left blank and listed on the Flagged page.</div></div>
 <div class="card"><div class="k">Flagged for review</div><div class="v">{flagged_n}</div><div class="n">Irregularities and open items.</div></div>
</div>"""
    idx = f"""<h2>Dashboard</h2>
{cards}
<div class="note"><strong>How to read this site.</strong> Verified rows link to official sources (.gov, state legislature, BOE, county, utilities, IRS). Client-provided values (labelled UNVERIFIED) are used only as inputs to projections and are never shown as verified facts. Projections are not forecasts.</div>
<h2>Start here</h2>
<div class="cards">
 <div class="card"><div class="k">Read first</div><div class="v" style="font-size:16px"><a href="executive-summary.html">Executive summary</a></div><div class="n">Key findings, the decision, and the caveats.</div></div>
 <div class="card"><div class="k">Decision</div><div class="v" style="font-size:16px"><a href="decision-guide.html">Live, rent, or sell</a></div><div class="n">Side-by-side comparison of options.</div></div>
 <div class="card"><div class="k">Projections</div><div class="v" style="font-size:16px"><a href="projections.html">Year-by-year 2026-2050</a></div><div class="n">Value, assessed value, tax, and costs.</div></div>
 <div class="card"><div class="k">Review</div><div class="v" style="font-size:16px"><a href="flagged.html">Flagged for Review</a></div><div class="n">Items that need confirmation before use.</div></div>
</div>
<h2>Categories</h2>
{table(["Category", "What it covers", "Page"], [
 ["Property tax & Prop 19", "Prop 13 / Prop 19 rules, tax rates, client tax history (unverified)", '<a href="property-tax.html">property-tax.html</a>'],
 ["Federal estate & gift", "2026 exclusion, rates, basis step-up, income-tax thresholds", '<a href="federal-estate.html">federal-estate.html</a>'],
 ["California tax", "No state estate/inheritance tax; income and capital gains rules", '<a href="california-tax.html">california-tax.html</a>'],
 ["Water & electricity", "SJW (Cupertino), SFPUC (SF), PG&E / SVCE, net billing", '<a href="utilities.html">utilities.html</a>'],
 ["Insurance", "CDI tools; premium data not verified", '<a href="insurance.html">insurance.html</a>'],
 ["Property B (SF rental)", "Rent Board, owner-occupied unit rules, rental scenarios", '<a href="rental-sf.html">rental-sf.html</a>'],
 ["Projections", "Year-by-year model 2026-2050 and sensitivity", '<a href="projections.html">projections.html</a>'],
 ["Decision guide", "Live, rent, or sell comparison", '<a href="decision-guide.html">decision-guide.html</a>'],
 ["Pending law", "Watchlist with status", '<a href="legislation.html">legislation.html</a>'],
 ["Inheritance steps", "Step-by-step process", '<a href="inheritance-steps.html">inheritance-steps.html</a>'],
 ["Flagged for Review", "Irregularities, unverified values, open questions", '<a href="flagged.html">flagged.html</a>'],
 ["Sources", "Full list with official links", '<a href="sources.html">sources.html</a>'],
], )}
<div class="warn"><strong>Privacy.</strong> This site contains no personal identifiers. Parcel numbers, owner names, addresses, and ZIP codes are not included. Property locations are given at city and county level only.</div>"""
    files["index.html"] = ("Dashboard", idx)

    # ---------- executive summary ----------
    ex = f"""<h2>Executive summary</h2>
<p>This guide compares three options for two inherited properties: keep and live in them (Prop 19 family-home treatment, where it applies), keep and rent them, or sell and invest the proceeds. It is built from official rules, client inputs, and a year-by-year model to 2050.</p>
<h3>Key findings (base case, inheritance in {INH}, appreciation 2.15%/yr)</h3>
<ul>
<li><strong>Property tax is the biggest change at inheritance.</strong> Property A's Prop 13 base is about {money(DEF['A']['assessed_parent_prop13'][str(INH)])}. If the heir lives in it (Prop 19 family-home rule), the taxable value is about {money(DEF['A']['taxable_prop19_after_Y'][str(INH)])}, giving an annual tax of about {money(p19)}. If it is reassessed to market value, the annual tax would be about {money(rea)} (<a href="property-tax.html">property-tax.html</a>).</li>
<li><strong>Property B's rented units would be reassessed.</strong> Prop 19 applies per unit (BOE LTA 2026/026). Only an owner-occupied unit can use the family-home treatment. Tax on B if fully reassessed is about {money(DEF['B']['B_tax_b1'][str(INH)])} a year (<a href="rental-sf.html">rental-sf.html</a>).</li>
<li><strong>Federal estate tax is not expected from these two properties alone.</strong> The 2026 basic exclusion is $15,000,000 (IRS Rev. Proc. 2025-32). Combined projected value at {INH} is about {money(DEF['estate']['combined_fmv_A_plus_B'][str(INH)])}. California has no estate or inheritance tax (RTC 13301).</li>
<li><strong>Heirs get a basis step-up</strong> to fair market value at death (IRC 1014). Gains are measured only from the date-of-death value.</li>
<li><strong>Financial lean (not a recommendation).</strong> Excluding use value and income tax, selling and investing beats holding Property A through {INH+5} in the base case. For Property B, keeping it as rental and selling are close in the base case, and the answer depends on income tax and rent growth (see <a href="decision-guide.html">decision-guide.html</a>).</li>
</ul>
<h3>Caveats</h3>
<ul>
<li>Client values (market values, assessed values, water, electricity, rent, insurance) are UNVERIFIED inputs. They are labelled throughout and are not verified facts.</li>
<li>Parcel-level tax rates were not confirmed. The Cupertino TRA composite is blank. The client's tax history implies rates above official sampled totals (see <a href="flagged.html">Flagged</a>).</li>
<li>Prop 19 requires that the decedent's home was their principal residence and that the heir moves in within one year. If not, the reassessed figures apply.</li>
<li>This is informational analysis, not legal or tax advice. Confirm with an estate attorney and CPA before acting.</li>
</ul>
<h3>Verification summary</h3>
<p>{counts_v} rows are VERIFIED with an official link. {counts_u} rows are UNVERIFIED and left blank. {flagged_n} irregularities or open items are on the <a href="flagged.html">Flagged for Review</a> page.</p>"""
    files["executive-summary.html"] = ("Executive summary", ex)

    # ---------- property tax ----------
    hist_a = table(["Year", "Assessed value (client)", "Change (client)", "Tax (client)", "Change (client)", "Verified tax", "Status", "Official reference"],
                   fmt_hist(HIST["property_A_cupertino"]), num_cols=(1, 3))
    hist_b = table(["Year", "Assessed value (client)", "Change (client)", "Tax (client)", "Change (client)", "Verified tax", "Status", "Official reference"],
                   fmt_hist(HIST["property_B_sf"]), num_cols=(1, 3))
    pt = f"""<h2>Property tax and Prop 13 / Prop 19</h2>
<div class="warn"><strong>Client history is UNVERIFIED.</strong> No parcel record was checked. The verified-tax column is blank on purpose. Official rates are shown in the verified table below.</div>
<h3>Verified rules and rates</h3>
{facts_table('property-tax')}
<h3>Property A (Cupertino, Santa Clara County): client-provided history</h3>
<p class="small">Official reference for the rate: <a href="https://files.santaclaracounty.gov/exjcpb1531/2025-11/tax-rate-book-2025-2026.pdf?VersionId=HHMZ1VmGwFXqVvpM36xuptkIcV2V8ctE" target="_blank" rel="noopener">SCC Tax Rate Book FY 2025-26 (S06)</a>. Implied 2025 client rate: $7,207 / $539,743 = 1.335%, above official sampled totals (1.1258%-1.2409%). See IR01.</p>
{hist_a}
<h3>Property B (San Francisco): client-provided history</h3>
<p class="small">Official reference for the rate: <a href="https://sftreasurer.org/property/secured-property-taxes" target="_blank" rel="noopener">SF Treasurer secured property taxes (S07)</a>. Implied 2025 client rate: $2,439 / $114,248 = 2.135%, versus the official 1.18162182%. See IR01.</p>
{hist_b}
<h3>Prop 19 value cap arithmetic (model method)</h3>
<p class="small">Under the family-home exclusion the new taxable value is the greater of the factored base year value and (market value minus $1,044,586). Modelled at inheritance year {INH}: taxable value about {money(DEF['A']['taxable_prop19_after_Y'][str(INH)])}; tax about {money(p19)}. Full reassessment: taxable value about {money(DEF['A']['taxable_reassessed_after_Y'][str(INH)])}, tax about {money(rea)}. Method: model/guide_project.py.</p>"""
    files["property-tax.html"] = ("Property tax & Prop 19", pt)

    # ---------- federal estate ----------
    thr_rows = []
    for yr in (2026, 2030, 2035, 2040, 2045, 2050):
        excl = DEF["estate"]["exclusion"][str(yr)]
        comb = DEF["estate"]["combined_fmv_A_plus_B"][str(yr)]
        thr_rows.append([str(yr), money(excl), money(comb), money(DEF["estate"]["headroom"][str(yr)]),
                         '<span class="badge unv">PROJECTION (indexed 2%/yr)</span>' if yr > 2026 else '<span class="badge ver">VERIFIED (2026)</span>',
                         src_links(['S10', 'S09'])])
    fed_thr = table(["Year", "Basic exclusion (per person)", "A + B projected market value", "Headroom", "Status", "Official source"], thr_rows, num_cols=(1, 2, 3))
    fe = f"""<h2>Federal estate, gift and income tax</h2>
{facts_table('federal')}
<h3>Projected exclusion vs. combined value (A + B)</h3>
<p class="small">The 2026 figure is verified (IRS). Later years are an illustrative 2%/yr indexing assumption (model input, not verified; the statute indexes annually). Combined value is the model's market value for A and B only; other estate assets would add to the total.</p>
{fed_thr}
<div class="note">Only the taxable estate above the exclusion is taxed. Headroom is shown for these two properties only.</div>"""
    files["federal-estate.html"] = ("Federal estate", fe)

    # ---------- california ----------
    ca = f"""<h2>California tax</h2>
{facts_table('california')}
<h3>Projected impact on the heir</h3>
<table><thead><tr><th>Item</th><th>Treatment</th><th>Source</th></tr></thead><tbody>
<tr><td>Inheritance of property</td><td>No state estate or inheritance tax</td><td>{src_links(['S15'])}</td></tr>
<tr><td>Rental income from B</td><td>Taxable (ordinary rates; no preferential CA capital gain rate)</td><td>{src_links(['S19','S18'])}</td></tr>
<tr><td>Sale gain above date-of-death value</td><td>Taxable as ordinary income for CA; 12.30% top rate in 2025 schedule</td><td>{src_links(['S18','S17'])}</td></tr>
<tr><td>Taxable income over $1,000,000</td><td>Additional 1% (RTC 17043)</td><td>{src_links(['S16'])}</td></tr>
</tbody></table>
<div class="note"><strong>Illustrative combined tax rate on a sale gain</strong> (not a computed liability): 15% federal long-term capital gains + 3.8% NIIT + 12.3% CA top rate = {pct(A['M_CG_RATE']['value'],1)}. The heir's actual brackets, the 20% federal rate on large gains, and the 1% surcharge over $1M are not modelled. Check with a CPA.</div>"""
    files["california-tax.html"] = ("California tax", ca)

    # ---------- utilities ----------
    water_calc_rows = [
        ["Cupertino (SJW), 5 ccf/mo", "5 x $4.9692 + $78.64 service", "$103.49/mo", "Calculated from tariff"],
        ["Cupertino (SJW), 10 ccf/mo", "6 x $4.9692 + 4 x $7.4167 + $78.64", "$138.13/mo", "Calculated from tariff"],
        ["Cupertino (SJW), 15 ccf/mo", "6 x $4.9692 + 6 x $7.4167 + 3 x $14.1659 + $78.64", "$195.45/mo", "Calculated from tariff"],
    ]
    water_calc = table(["Usage", "Calculation (tariff)", "Monthly total", "Basis"], [
        [a, b, c, '<a href="https://www.sjwater.com/media/dm3lribs/san-jose-water-company-al-628-a-approved.pdf" target="_blank" rel="noopener">S20</a>'] for a, b, c, d in water_calc_rows],
        num_cols=(2,))
    ut = f"""<h2>Water, sewer and electricity</h2>
{facts_table('utilities')}
<h3>Water cost check (Cupertino, SJW Schedule No. 1 residential tiers)</h3>
<p class="small">Client range for Property A is $100-150 per month. At 10 ccf per month the tariff gives about $138, which is inside that range. The calculation is a check, not a verified bill.</p>
{water_calc}
<div class="note"><strong>Electricity (Property A).</strong> Net billing exports are credited at Avoided Cost Calculator values (S24). Non-bypassable charges still apply to imports. The client's $10-20/mo figure is a bill credit, not guaranteed income. Electricity prices are UNVERIFIED and blank.</div>"""
    files["utilities.html"] = ("Water & electricity", ut)

    # ---------- insurance ----------
    ins_rows = [[esc(r["id"]), esc(r["item"]), '<span class="blank">blank - unverified</span>', badge(r["status"]), src_links(r["sources"]), esc(r["note"])] for r in FACTS if r["category"] == "insurance"]
    ins = f"""<h2>Home and rental insurance</h2>
<div class="warn"><strong>No verified premium averages.</strong> The California Department of Insurance publishes shop-around tools, not averages, on the page reviewed. Premium figures are left blank.</div>
{table(["ID", "Item", "Verified value", "Status", "Official source", "Note"], ins_rows)}
<h3>Client insurance estimate (UNVERIFIED input)</h3>
<p>The client estimate is $1,500 per year for each property. It is used only as a projection input. Official shop-around tools: <a href="https://www.insurance.ca.gov/01-consumers/105-type/5-residential/" target="_blank" rel="noopener">CDI residential insurance (S30)</a>.</p>
{table(["Property", "Input", "Value used", "Status", "Official reference"], [
 ["A (Cupertino)", "Homeowners insurance", money(A['U_A_INS']['value']) + " / yr", '<span class="badge unv">UNVERIFIED (client)</span>', src_links(['S30'])],
 ["B (San Francisco)", "Insurance (rental and owner unit)", money(A['U_B_INS']['value']) + " / yr", '<span class="badge unv">UNVERIFIED (client)</span>', src_links(['S30'])],
], num_cols=(2,))}"""
    files["insurance.html"] = ("Insurance", ins)

    # ---------- rental SF ----------
    rent_rows = [[esc(r["id"]), esc(r["item"]), '<span class="blank">blank - unverified</span>' if r["status"] == "UNVERIFIED" else esc(r["value"]), badge(r["status"]), src_links(r["sources"]), esc(r["note"])] for r in FACTS if r["category"] == "rental"]
    rn = f"""<h2>Property B (San Francisco): rental and owner-occupied unit</h2>
{table(["ID", "Item", "Verified value", "Status", "Official source", "Note"], rent_rows)}
<h3>Key structural rule (verified)</h3>
<p>{src_links(['S03'])}: in a multi-unit building each unit must qualify separately for the intergenerational exclusion. Only the unit the heir occupies can use Prop 19 treatment. Rented units are reassessed to market value at inheritance.</p>
<h3>Rental scenarios (projection)</h3>
<table><thead><tr><th>Scenario</th><th>Tax treatment</th><th class="num">Tax at {INH} (projection)</th><th class="num">NOI at {INH} (pre income tax)</th><th>Source</th></tr></thead><tbody>
<tr><td>Keep as rental (full reassessment)</td><td>Reassessed to market; SF secured rate</td><td class="num">{money(DEF['B']['B_tax_b1'][str(INH)])}</td><td class="num">{money(DEF['B']['B_noi_b1'][str(INH)])}</td><td>{src_links(['S07','S08','S25'])}</td></tr>
<tr><td>Heir occupies one unit, rents two (illustrative 1/3 share)</td><td>Owner unit qualifies under Prop 19 (value share approximated); rented share reassessed</td><td class="num">{money(DEF['B']['B_tax_b3'][str(INH)])}</td><td class="num">{money(DEF['B']['B_noi_b3'][str(INH)])}</td><td>{src_links(['S03','S02','S07'])}</td></tr>
<tr><td>Sell at inheritance</td><td>Net proceeds (after 5% selling cost and $1.10/$1,000 county transfer tax; SF city tax excluded)</td><td class="num">n/a</td><td class="num">{money(DEF['B']['sale_net_at_Y'])} (net proceeds)</td><td>{src_links(['S29'])}</td></tr>
</tbody></table>
<div class="note">The NOI figures are before income tax, mortgage, vacancy, and capital reserves. They are not a profit forecast. Rent-control status and the building's actual meter type are unverified.</div>"""
    files["rental-sf.html"] = ("Property B (SF rental)", rn)

    # ---------- projections ----------
    pj = f"""<h2>Projections, 2026-2050</h2>
<div class="warn"><strong>These are projections, not facts.</strong> Base assumptions: 2.15%/yr appreciation (reference: FHFA CA HPI 2024, cited in BOE LTA 2025/009), 2%/yr Prop 13 growth in assessed value, inheritance year {INH}. Client inputs are UNVERIFIED. Modelled A tax planning rate 1.18% (not parcel-verified); B tax rate is the verified SF FY 2026-27 rate.</div>
<h3>Property A (Cupertino)</h3>
<p class="small">Sources for the columns: <a href="property-tax.html">Prop 19 and tax rules (S01, S02, S06, S08)</a>; water <a href="utilities.html">SJW tariff (S20)</a>; insurance (client; <a href="insurance.html">S30</a>); maintenance is a model assumption.</p>
{ta}
<h3>Property B (San Francisco)</h3>
<p class="small">Sources for the columns: <a href="rental-sf.html">Prop 19 unit rule (S03)</a>; SF rate <a href="https://sftreasurer.org/property/secured-property-taxes" target="_blank" rel="noopener">S07</a>; rent cap <a href="https://www.sf.gov/departments--rent-board" target="_blank" rel="noopener">S25</a>; water and sewer <a href="utilities.html">S22</a>.</p>
{tb}
<h3>Sensitivity: inheritance year and appreciation</h3>
<p class="small">Inheritance year 2040, 2045, or 2050; appreciation 0%, 2.15%, or 4%. Client values as input.</p>
{sens_table()}
<h3>Comparison to 2050 (illustrative, base case)</h3>
{table(["Option", "Value to 2050 (projection, undiscounted)", "Note", "Official source"], [
 ["A: live in (Prop 19), net of costs, excluding use value", money(C['A_hold_live_net_wealth_excl_use_value']), "Market value at 2050 minus costs from inheritance; excludes living value.", src_links(['S01', 'S02'])],
 ["A: sell at inheritance and invest at 4%/yr", money(C['A_sell_and_invest_value']), "Net proceeds after 5% selling cost and county transfer tax; invested at a model return (not a forecast).", src_links(['S29'])],
 ["B: keep as rental (pre income tax)", money(C['B_keep_rental_net_wealth_pretax']), "Market value at 2050 plus NOI from inheritance. Pre income tax.", src_links(['S07', 'S25'])],
 ["B: sell at inheritance and invest at 4%/yr", money(C['B_sell_and_invest_value']), "Net proceeds invested at model return.", src_links(['S29'])],
], num_cols=(1,))}
<div class="note">The B comparison is pre-tax on the rental side and after-tax on the investment side (model input). It is not like-for-like. Treat the B result as a range.</div>"""
    files["projections.html"] = ("Projections", pj)

    # ---------- decision guide ----------
    dg = f"""<h2>Decision guide: live in, rent, or sell and reinvest</h2>
<p>The table below shows the main trade-offs for each property, using the base case. It is decision support; the personal-use value of living in the home is not priced here.</p>
{table(["Question", "Property A (Cupertino)", "Property B (San Francisco)"], [
 ["Tax at inheritance ({INH})".format(INH=INH), f"Prop 19 (if heir lives in it): about {money(p19)}/yr. Reassessed: about {money(rea)}/yr. Source: {src_links(['S01','S02','S06'])}", f"Rented units reassessed: about {money(DEF['B']['B_tax_b1'][str(INH)])}/yr. Owner unit can qualify if occupied. Source: {src_links(['S03','S07'])}"],
 ["Annual net income if kept", "None (personal use). Solar credit is a bill credit (client, UNVERIFIED).", f"NOI about {money(DEF['B']['B_noi_b1'][str(INH)])}/yr pre income tax (rent: client, UNVERIFIED). Source: {src_links(['S25'])}"],
 ["Sale net proceeds at {INH} (projection, after 5% selling cost and county transfer tax)".format(INH=INH), money(DEF['A']['sale_net_at_Y']) + " " + src_links(['S29']), money(DEF['B']['sale_net_at_Y']) + " " + src_links(['S29'])],
 ["Heir's basis", f"Date-of-death value (step-up). Source: {src_links(['S12'])}", f"Date-of-death value (step-up). Source: {src_links(['S12'])}"],
 ["Main risk", "Prop 19 eligibility (move-in, exemption filing) " + src_links(['S02']) + "; tax-rate uncertainty; ACC Plus unresolved " + src_links(['S24']), "Each rented unit reassessed " + src_links(['S03']) + "; rent-control coverage unknown " + src_links(['S25'])],
 ["Financial lean (base case)", "Selling and investing ranks ahead of holding (excludes use value). Income tax on investment returns " + src_links(['S19', 'S14']), "Close; depends on tax on rental income (" + src_links(['S19', 'S14']) + ") and rent growth (" + src_links(['S25']) + ")."],
])}
<h3>How to decide</h3>
<ol>
<li>If the heir wants to live in Property A, the Prop 19 family-home treatment is worth confirming before the move-in date. The one-year move-in and exemption filing are strict (<a href="inheritance-steps.html">steps</a>).</li>
<li>If living in A is not a goal, the base-case projections favour selling and reinvesting, since the reassessed tax and carrying cost are high relative to the income the proceeds could earn (model return, not a forecast).</li>
<li>For B, the main choice is between keeping the rental (reassessed tax, pre-tax NOI about {money(DEF['B']['B_noi_b1'][str(INH)])}/yr at {INH}) and selling. An heir who occupies one unit reduces the tax (illustrative {money(DEF['B']['B_tax_b3'][str(INH)])}/yr), but that is not verified for this building.</li>
<li>Check the figures in <a href="flagged.html">Flagged for Review</a> before deciding. The tax history does not reconcile to official rates.</li>
</ol>
<div class="warn">Not legal or tax advice. Consult an estate attorney and a CPA. Projections depend on UNVERIFIED client inputs.</div>"""
    files["decision-guide.html"] = ("Decision guide", dg)

    # ---------- legislation ----------
    leg_rows = [[esc(x["id"]), esc(x["title"]), esc(x["status"]), esc(x["effect"]), src_links(x["sources"]), '<span class="badge ver">VERIFIED</span>' if x["verified"] else '<span class="badge unv">UNVERIFIED</span>'] for x in LEG]
    lg = f"""<h2>Pending and recent law</h2>
{table(["ID", "Item", "Status", "Effect on this analysis", "Official source", "Status check"], leg_rows)}
<div class="note">Items marked UNVERIFIED have no official source linked yet. They are shown for monitoring only and are not used in projections.</div>"""
    files["legislation.html"] = ("Pending law", lg)

    # ---------- steps ----------
    st_rows = [[str(x["n"]), esc(x["title"]), esc(x["detail"]), src_links(x["sources"])] for x in STEPS]
    sp = f"""<h2>Inheritance process, step by step</h2>
{table(["Step", "Action", "Detail", "Official source"], st_rows)}
<div class="warn">These steps are a planning checklist, not legal advice. Probate or trust administration steps are not covered here and need an estate attorney.</div>"""
    files["inheritance-steps.html"] = ("Inheritance steps", sp)

    # ---------- flagged ----------
    irr_rows = [[esc(x["id"]), f'<span class="sev-{x["severity"]}">{esc(x["severity"].upper())}</span>', esc(x["property"]), esc(x["title"]), esc(x["detail"]), src_links(x["sources"])] for x in IRR]
    unv_rows = [[esc(r["id"]), esc(r["item"]), esc(r["note"]), src_links(r["sources"])] for r in FACTS if r["status"] == "UNVERIFIED"]
    fl = f"""<h2>Flagged for Review</h2>
<p>These items do not block publication. They are listed so the reader can check them before relying on the analysis.</p>
<h3>Irregularities and open questions</h3>
{table(["ID", "Severity", "Property", "Issue", "Detail", "Sources"], irr_rows)}
<h3>Unverified values (left blank in the verified tables)</h3>
{table(["ID", "Item", "Why it is blank", "Sources checked"], unv_rows)}
<h3>Client inputs used only in projections (UNVERIFIED)</h3>
{table(["Input", "Label", "Value", "Basis", "Official reference"], [
 [esc(x["id"]), esc(x["label"]), esc(str(x["value"])) + " " + esc(x["unit"]), '<span class="badge unv">UNVERIFIED (client)</span>', src_links(['S30'] if 'INS' in x['id'] else (['S20'] if 'WATER' in x['id'] else (['S23'] if 'SOLAR' in x['id'] else (['S07'] if 'PT' in x['id'] or 'FMV' in x['id'] or 'FBYV' in x['id'] else ['S25'] if 'RENT' in x['id'] else ['S07']))))]
 for x in ASSUME if x["kind"] == "user"])}
<h3>Third-party sources reviewed but not used</h3>
<p class="small">Secondary blogs, insurance aggregators, and solar sales sites were reviewed for leads. None is used for a verified value. Where they conflicted with official sources, the official source was used or the value was left blank.</p>"""
    files["flagged.html"] = ("Flagged for Review", fl)

    # ---------- sources ----------
    src_rows = [[esc(s["id"]), esc(s["publisher"]), esc(s["title"]), f'<a href="{esc(s["url"])}" target="_blank" rel="noopener">{esc(s["url"])}</a>', esc(s["tier"]), esc(s["how"])] for s in SRC.values()]
    so = f"""<h2>Sources</h2>
<p class="small">All sources were accessed {GEN_DATE}. "search excerpt" means the URL was reached through search and the excerpt is from the official domain; open the page to confirm the wording.</p>
{table(["ID", "Publisher", "Title", "URL", "Tier", "How checked"], src_rows)}"""
    files["sources.html"] = ("Sources", so)

    # write
    outdir = os.path.join(ROOT, "guide")
    os.makedirs(outdir, exist_ok=True)
    for fn, (title, body) in files.items():
        with open(os.path.join(outdir, fn), "w", encoding="utf-8") as f:
            f.write(page(fn, title, body, fn))
    open(os.path.join(outdir, ".nojekyll"), "w").write("")
    print("wrote", len(files), "pages to guide/")


if __name__ == "__main__":
    build()
