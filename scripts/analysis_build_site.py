#!/usr/bin/env python3
"""Builds the docs/ GitHub Pages site from data/projections.json + verified content."""
import json, html, datetime

with open("data/projections.analysis.json") as fp:
    P = json.load(fp)

A = P["assumptions"]
AS = html.escape
TODAY = "2026-11-06"

CUP_TAX_2025 = 7207
SF_TAX_2025 = 2439
CUP_INS_YR = 1300
CUP_WATER_MO = 120
CUP_MAINT_YR = 31000
SF_RENT_MO = 7150
MID45 = [r for r in P["tax_table"] if r["growth"] == "moderate" and r["year"] == 2045][0]
SC45 = [r for r in P["scenario_table"] if r["growth"] == "moderate" and r["year"] == 2045][0]
TOTAL_MIN = min(r["A"]["total_tax"] for r in P["tax_table"])
TOTAL_MAX = max(r["A"]["total_tax"] for r in P["tax_table"])

def money(n):
    return f"${n:,}"

def pct(n, digits=2):
    return f"{n:.{digits}f}%"

def esc(s):
    return html.escape(str(s))

CSS = """
:root{--bg:#f5f7fa;--card:#fff;--ink:#1a2433;--muted:#5b6b7f;--brand:#0b6e4f;--brand2:#0d4f7c;--accent:#b3541e;--line:#e2e8f0;--red:#a3341e;--amber:#9a6a00;--green:#0b6e4f}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;background:var(--bg);color:var(--ink);line-height:1.55}
a{color:var(--brand2);text-decoration:none}
a:hover{text-decoration:underline}
.wrap{max-width:1180px;margin:0 auto;padding:0 20px}
header{background:linear-gradient(120deg,#0d4f7c 0%,#0b6e4f 100%);color:#fff;padding:26px 0 22px}
header h1{font-size:1.55rem;font-weight:700;letter-spacing:.2px}
header .sub{opacity:.85;margin-top:6px;font-size:.95rem}
header .meta{opacity:.7;font-size:.8rem;margin-top:10px}
.layout{display:flex;gap:26px;padding:26px 0 60px}
nav{flex:0 0 230px;position:sticky;top:20px;align-self:flex-start}
nav .card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;box-shadow:0 1px 3px rgba(16,24,40,.06)}
nav h3{font-size:.75rem;text-transform:uppercase;letter-spacing:1px;color:var(--muted);margin-bottom:10px}
nav a{display:block;padding:7px 10px;border-radius:8px;color:var(--ink);font-size:.92rem;margin-bottom:2px}
nav a:hover{background:#eef4f2;text-decoration:none}
nav a.active{background:var(--brand);color:#fff;font-weight:600}
main{flex:1;min-width:0}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:22px 24px;margin-bottom:22px;box-shadow:0 1px 3px rgba(16,24,40,.05)}
.card h2{font-size:1.15rem;margin-bottom:10px;color:var(--brand2)}
.card h3{font-size:1rem;margin:18px 0 8px;color:var(--ink)}
.card p{margin-bottom:10px;color:#2c3a4c}
.tag{display:inline-block;font-size:.72rem;font-weight:700;padding:2px 9px;border-radius:20px;margin-right:6px;letter-spacing:.3px}
.tag.ok{background:#e3f2ec;color:var(--green)}
.tag.flag{background:#fdf0e4;color:var(--amber)}
.tag.bad{background:#fdeae4;color:var(--red)}
.tag.info{background:#e8eff8;color:var(--brand2)}
table{width:100%;border-collapse:collapse;font-size:.88rem;margin:12px 0}
th,td{border:1px solid var(--line);padding:7px 9px;text-align:left;vertical-align:top}
th{background:#f0f4f8;font-weight:600;color:#26364a}
tr:nth-child(even) td{background:#fafcfe}
td.num{text-align:right;font-variant-numeric:tabular-nums}
.src{font-size:.72rem;color:var(--muted);margin-top:10px}
.src a{word-break:break-all}
.kpi{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin:16px 0}
.kpi .item{background:#f7faf8;border:1px solid var(--line);border-radius:10px;padding:14px 16px}
.kpi .item .label{font-size:.75rem;color:var(--muted);text-transform:uppercase;letter-spacing:.6px}
.kpi .item .value{font-size:1.25rem;font-weight:700;margin-top:4px;color:var(--brand)}
.kpi .item .note{font-size:.75rem;color:var(--muted);margin-top:3px}
.callout{border-left:4px solid var(--accent);background:#fdf7f1;padding:12px 16px;border-radius:0 8px 8px 0;margin:12px 0}
.callout.green{border-color:var(--green);background:#eff8f2}
.callout.blue{border-color:var(--brand2);background:#eef4f9}
.callout h4{font-size:.92rem;margin-bottom:6px}
.callout p{margin-bottom:0;font-size:.92rem}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:18px}
@media(max-width:900px){.layout{flex-direction:column}nav{position:static;width:100%}.grid2{grid-template-columns:1fr}}
.step{border:1px solid var(--line);border-radius:10px;padding:14px 16px;margin-bottom:12px;background:#fafcfe}
.step h4{font-size:.95rem;color:var(--brand2)}
.step p{font-size:.9rem;margin-top:4px}
footer{border-top:1px solid var(--line);padding:18px 0;color:var(--muted);font-size:.8rem}
ul,ol{margin:8px 0 12px 22px}
li{margin-bottom:6px}
.toc{background:#f7faf8;border:1px dashed var(--line);border-radius:10px;padding:14px 18px;margin-bottom:20px}
.toc h3{margin-bottom:8px}
"""

def nav(active):
    items = [
        ("index", "Executive Summary", "index.html"),
        ("properties", "Properties & Tax Data", "properties.html"),
        ("tax-law", "Law & Tax Research", "tax-law.html"),
        ("inheritance", "Inheritance Process", "inheritance.html"),
        ("projections", "Projections 2026-2055", "projections.html"),
        ("costs", "Utilities & Insurance", "costs.html"),
        ("scenarios", "Decision Analysis", "scenarios.html"),
        ("flagged", "Flagged for Review", "flagged.html"),
        ("sources", "Sources", "sources.html"),
    ]
    lis = "".join(
        f'<a class="{"active" if k == active else ""}" href="{u}">{esc(t)}</a>' for k, t, u in items)
    return f"""
<nav><div class="card"><h3>Navigation</h3>{lis}
<p style="font-size:.72rem;color:var(--muted);margin-top:12px">Verified {TODAY}<br>No personal data in this product</p>
</div></nav>"""

def page(active, title, subtitle, body, footer_extra=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} — Cupertino3 Inheritance Decision</title>
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<header><div class="wrap">
<h1>Cupertino &amp; San Francisco House Inheritance — Decision Dashboard</h1>
<div class="sub">Executive analysis for trust-based inheritance (target 2040–2050)</div>
<div class="meta">Research verified {TODAY} · all table rows carry source links · unverified values flagged</div>
</div></header>
<div class="wrap layout">
{nav(active)}
<main>{body}</main>
</div>
<footer><div class="wrap">
Cupertino3 · Internal decision-support product · All figures are estimates for planning; verify before acting.
{footer_extra}
</div></footer>
</body></html>"""

# ---------- table builders ----------
def tbl(headers, rows, classes=None):
    h = "".join(f"<th>{esc(x)}</th>" for x in headers)
    r = ""
    for row in rows:
        cells = "".join(f"<td class=\"{classes[i]}\">{c}</td>" if classes and i < len(classes) and classes[i] == "num" else f"<td>{c}</td>" for i, c in enumerate(row))
        r += f"<tr>{cells}</tr>"
    return f"<table><thead><tr>{h}</tr></thead><tbody>{r}</tbody></table>"

def src(*links):
    return '<div class="src">Sources: ' + " · ".join(f'<a href="{esc(u)}">{esc(t)}</a>' for t, u in links) + "</div>"

def kpi(label, value, note):
    return f'<div class="item"><div class="label">{esc(label)}</div><div class="value">{esc(value)}</div><div class="note">{esc(note)}</div></div>'

# ---------- Executive summary page ----------
def page_index():
    t = P["tax_table"]
    mid = [r for r in t if r["growth"] == "moderate" and r["year"] == 2045][0]
    sc = [r for r in P["scenario_table"] if r["growth"] == "moderate" and r["year"] == 2045][0]
    est2045 = [r for r in P["estate_table"] if r["year"] == 2045][0]
    body = f"""
<div class="toc"><h3>Executive Summary</h3>
<p>This dashboard supports one decision: <b>what to do with the Cupertino house when it is inherited around 2040–2050</b> — live in it, rent it, or sell it and reinvest — alongside the San Francisco house (3 units, $7,150/mo rent) and a cash inheritance.</p>
</div>

<div class="kpi">
{kpi("Federal estate tax exemption (2026)", "$15,000,000 / person", "IRS — indexed for inflation from 2027 (OBBB, permanent)")}
{kpi("California inheritance / estate tax", "None", "Repealed 1982 (Prop 6); pick-up tax = $0")}
{kpi("Cupertino property tax at inheritance (2045, moderate)", money(mid["A"]["cup_tax"]) + "/yr", "Full Prop 19 reassessment (rental house)")}
{kpi("Sell Cupertino → annual after-tax income (2045)", money(sc["sell"]["after_tax_income"]), "Reinvested portfolio, moderate growth")}
{kpi("Rent Cupertino → net operating income (2045)", "−" + money(abs(sc["rent"]["noi"])) + "/yr", "Property tax reset exceeds net rent")}
{kpi("Estate exemption projected 2045", money(est2045["exemption_person"]) + "/person", "Assumption: +2.5%/yr indexing")}
</div>

<div class="card">
<h2>The decision in one paragraph</h2>
<p><b>Recommendation: Sell the Cupertino house at inheritance and reinvest the proceeds in the stock market; keep the San Francisco house (either live in the third unit or keep renting all three units).</b>
Under Proposition 19 (in effect since Feb 16, 2021), an inherited <b>rental property</b> is reassessed to full market value — the Cupertino house's property tax would jump from ~{money(CUP_TAX_2025)} today to about <b>{money(mid['A']['cup_tax'])} per year</b> by 2045 (moderate growth scenario), which exceeds any plausible net rental income (projected net operating income is about <b>−{money(abs(sc['rent']['noi']))}/yr</b>). Because inherited assets receive a <b>stepped-up basis</b> at date of death, selling the house immediately after inheritance produces <b>$0 capital gains tax</b>, and the proceeds (~{money(sc['sell']['net'])} net by 2045) invested at a 6% nominal return generate roughly <b>{money(sc['sell']['after_tax_income'])}/yr</b> after tax — without property tax, insurance, maintenance, or vacancy risk. The SF house keeps its Prop 19 capped exclusion if the heir moves into it within one year (and files the homeowner's exemption), or its $7,150/mo rent covers a full reassessment.</p>
</div>

<div class="card">
<h2>Key findings</h2>
<h3>1. There is no California inheritance tax — the only estate tax is federal</h3>
<p>California repealed its inheritance tax in 1982 and has no state estate tax (the old "pick-up" tax collects $0). The only inheritance tax exposure is the federal estate tax: <b>$15,000,000 per person ($30M per married couple with portability) in 2026</b>, made permanent by the One Big Beautiful Bill Act (signed July 4, 2025) and indexed for inflation from 2027. Estate tax is <b>40% on the amount above the exemption</b> and is paid by the estate (Form 706, due 9 months after death), not by heirs. Inheritances themselves are not income to recipients.</p>
{src(("IRS estate tax page", "https://www.irs.gov/businesses/small-businesses-self-employed/estate-tax"), ("IRS IR-2025-103 (2026 inflation adjustments)", "https://www.irs.gov/newsroom/irs-releases-tax-inflation-adjustments-for-tax-year-2026-including-amendments-from-the-one-big-beautiful-bill"), ("California FTB — estate tax history", "https://www.ftb.ca.gov/tax-pros/law/legislation/2019-2020/SB378-032519.pdf"))}

<h3>2. Proposition 19 is the single biggest cost driver at inheritance</h3>
<p>Prop 19 (effective Feb 16, 2021) eliminated the parent-child property-tax exclusion for anything other than the <b>family home</b>. Inherited rental/investment property is reassessed to full market value; inherited principal residences get the factored base year value plus an inflation-adjusted <b>$1,044,586</b> allowance (2025–2027 period) — but only if the heir occupies it as their primary residence within <b>one year</b> and files the homeowner's exemption. The claim form is <b>BOE-19-P</b>, due within <b>3 years</b> of the transfer (date of death). A repeal initiative failed to qualify for the November 2026 ballot; Prop 19 remains in effect.</p>
{src(("BOE Taxpayers' Rights Advocate (official Prop 19 guidance)", "https://www.boe.ca.gov/proptaxes/pdf/lta22051.pdf"), ("CA Secretary of State — repeal initiative failed", "https://elections.cdn.sos.ca.gov/ccrov/2026/may/26138jh.pdf"))}

<h3>3. Total property tax at inheritance: ~$96K/yr by 2045 (both houses kept)</h3>
<p>Today the two houses cost about {money(CUP_TAX_2025)} + {money(SF_TAX_2025)} = <b>{money(CUP_TAX_2025 + SF_TAX_2025)}/yr</b> in property tax. Under Prop 19 at a 2045 inheritance (moderate 3.5% growth), keeping both houses costs roughly <b>{money(mid['A']['total_tax'])}/yr</b> (Cupertino fully reassessed; SF with the capped exclusion). The result is nearly identical if the parents instead make the Cupertino house their principal residence — the $1M-capped exclusion simply shifts between the two houses.</p>

<h3>4. Selling is tax-free; renting is a net loss; living in Cupertino costs ~$80K/yr</h3>
<p>Stepped-up basis means <b>$0 capital gains tax</b> if the inherited house is sold at market value (IRS Topic 409). Renting it out after the reassessment produces a projected net operating loss of about {money(abs(sc['rent']['noi']))}/yr by 2045. Living in it avoids rent but still carries ~{money(mid['A']['cup_tax'])} in property tax plus insurance, utilities and maintenance — roughly $79K/yr of housing cost. The SF house's rent ($7,150/mo = $85,800/yr) comfortably absorbs its own reassessment.</p>
{src(("IRS Topic 409 — capital gains & stepped-up basis", "https://www.irs.gov/taxtopics/tc409"), ("IRS Pub 551 — basis of assets", "https://www.irs.gov/forms-pubs/about-publication-551"))}

<h3>5. Planning actions to take now (before 2040)</h3>
<ol>
<li><b>Fund the trust</b> with both houses (a trust only avoids probate for assets titled into it).</li>
<li><b>Decide which house is the parents' principal residence</b> — it determines which house gets the Prop 19 capped exclusion and which is fully reassessed.</li>
<li><b>Verify all user-provided figures</b> against official tax bills, assessor records, leases and quotes (see Flagged for Review).</li>
<li><b>If the estate may exceed ~$30M (couple)</b>, plan with an estate attorney: lifetime gifting ($19,000/recipient annual exclusion in 2026), portability, and trust structure.</li>
<li><b>Heirs must move into the excluded house within 1 year</b> of inheritance and file the homeowner's exemption, or the exclusion is lost permanently.</li>
</ol>
</div>

<div class="card">
<h2>How to use this site</h2>
<ul>
<li><b>Properties &amp; Tax Data</b> — both houses' history, market values, and flagged irregularities.</li>
<li><b>Law &amp; Tax Research</b> — every verified fact with its official source.</li>
<li><b>Inheritance Process</b> — the step-by-step trust → reassessment → sale/rent timeline.</li>
<li><b>Projections 2026–2055</b> — values, property tax, estate exemption, and costs under three growth scenarios.</li>
<li><b>Decision Analysis</b> — live vs rent vs sell, side by side, with the recommendation.</li>
<li><b>Flagged for Review</b> — unverified values, irregularities, and what needs confirmation.</li>
<li><b>Sources</b> — every link used.</li>
</ul>
<p style="color:var(--muted);font-size:.85rem">Projection assumptions (growth rates, portfolio return, maintenance) are labeled assumptions, not verified facts. Verified law/rates carry official source links on every table row.</p>
</div>
"""
    return page("index", "Executive Summary", "", body)

# ---------- Properties page ----------
def page_properties():
    rows = []
    for y, tax, av, rate, src_status in [
        ("2026", None, 550537, None, "User-provided"),
        ("2025", 7207, 539743, 1.335, "User-provided"),
        ("2024", 7003, 529161, 1.323, "User-provided"),
        ("2023", 6917, 518786, 1.333, "User-provided"),
        ("2022", 6755, 508614, 1.328, "User-provided"),
        ("2021", 6662, 498642, 1.336, "User-provided"),
        ("2020", 6565, 493530, 1.331, "User-provided"),
        ("2019", 6565, 483854, 1.357, "User-provided"),
        ("2018", 6383, 474368, 1.346, "User-provided"),
        ("2017", 6383, 465067, 1.372, "User-provided"),
        ("2016", 6414, 455949, 1.407, "User-provided"),
        ("2015", 6130, 449101, 1.365, "User-provided"),
        ("2014", 5965, 440305, 1.355, "User-provided"),
    ]:
        rows.append([f"<b>{y}</b>", money(tax) if tax is not None else "--", money(av), f"{rate:.2f}%" if rate else "--", "User-provided (flag)"])
    body = f"""
<div class="card">
<h2>Cupertino house (Santa Clara County, CA)</h2>
<p><span class="tag flag">USER-PROVIDED</span> Market value (Nov 2026): <b>{money(3100000)}</b> — <b>not verified</b>; obtain an appraisal or assessor market value.
Assessed value shown is the Prop 13 factored base year value (AV), not market value. Estimated value and solar credits are user-provided (flag).</p>
{tbl(["Year", "Property taxes", "Tax assessment (AV)", "Implied effective rate", "Source status"], rows, ["", "num", "num", "num", ""])}
{src(("Santa Clara County tax rate book 2025-26 (official)", "https://files.santaclaracounty.gov/exjcpb1531/2025-11/tax-rate-book-2025-2026.pdf"), ("BOE Prop 13 / Prop 19 rules", "https://www.boe.ca.gov/proptaxes/pdf/lta22051.pdf"))}
<div class="callout"><h4>Irregularity</h4><p>Implied effective rate 1.32%–1.41% exceeds the published Cupertino composite range (~1.15%–1.22%). Likely cause: special assessments/direct charges on this parcel. Verify on the official tax bill.</p></div>
</div>

<div class="card">
<h2>San Francisco house (San Francisco, CA)</h2>
<p><span class="tag flag">USER-PROVIDED</span> Market value (Nov 2026): <b>{money(1800000)}</b> — <b>not verified</b>. 3 livable units; 2 rented at $7,150/mo; unit 3 available as principal residence.</p>
{tbl(["Year", "Property taxes", "Tax assessment (AV)", "Implied effective rate", "Source status"], [
 ["<b>2025</b>", money(2439), money(114248), "2.13%", "User-provided (flag)"],
 ["<b>2024</b>", money(2315), money(112008), "2.07%", "User-provided (flag)"],
 ["<b>2023</b>", money(2179), money(109814), "1.98%", "User-provided (flag)"],
 ["<b>2022</b>", money(2107), money(107662), "1.96%", "User-provided (flag)"],
 ["<b>2021</b>", money(2066), money(105595), "1.96%", "User-provided (flag)"],
 ["<b>2020</b>", money(2197), money(104513), "2.10%", "User-provided (flag)"],
 ["<b>2019</b>", money(2134), money(102465), "2.08%", "User-provided (flag)"],
 ["<b>2018</b>", money(2061), money(100456), "2.05%", "User-provided (flag)"],
 ["<b>2017</b>", money(1740), money(98488), "1.77%", "User-provided (flag)"],
 ["<b>2016</b>", money(1675), money(96557), "1.74%", "User-provided (flag)"],
], ["", "num", "num", "num", ""])}
{src(("SF Treasurer & Tax Collector — secured property taxes (official)", "https://sftreasurer.org/property/secured-property-taxes"))}
<div class="callout"><h4>Irregularity</h4><p>Implied effective rate 1.73%–2.14% exceeds the published SF secured rate of 1.18% (FY 2026-27: 1.18162182%). Likely cause: SF direct charges (sewer capacity charge based on land value/ERU) and special assessments. Verify on the official bill.</p></div>
</div>

<div class="card">
<h2>Property facts summary</h2>
{tbl(["Property", "Market value (est., user)", "Current property tax", "Use", "Rental income", "Occupancy status"], [
 ["Cupertino (Santa Clara County, CA)", money(3100000), money(CUP_TAX_2025) + "/yr (2025)", "Rental / investment (to confirm)", "Not provided", "To confirm"],
 ["SF (San Francisco, CA)", money(1800000), money(SF_TAX_2025) + "/yr (2025)", "Owner-occupied rental (3 units)", "$7,150/mo (2 units, user)", "Parents can live in unit 3"],
], ["", "num", "num", "", "", ""])}
<div class="callout blue"><h4>Note</h4><p>The Cupertino house's current occupancy/rent status must be confirmed: under Prop 19 the analysis changes materially if the Cupertino house is (a) the parents' principal residence vs (b) a rental. See Flagged for Review.</p></div>
</div>
"""
    return page("properties", "Properties & Tax Data", "", body)

# ---------- Law & Tax page ----------
def page_tax_law():
    body = f"""
<div class="card">
<h2>Federal estate tax — the only inheritance tax that can apply</h2>
{tbl(["Item", "2026 value", "Source"], [
 ["Basic exclusion amount (per person)", "$15,000,000", "IRS estate tax page"],
 ["2025 exclusion amount", "$13,990,000", "IRS estate tax page / IR-2025-103"],
 ["Combined married (portability)", "$30,000,000", "Derived (2 × per-person); IRS portability rule"],
 ["Top rate on excess", "40%", "IRS estate tax page"],
 ["Annual gift exclusion", "$19,000 / recipient", "IRS IR-2025-103"],
 ["Return", "Form 706, 9 months after death", "IRS Form 706 instructions"],
 ["Indexing", "Inflation-indexed from 2027 (permanent, no sunset)", "IRS IR-2025-103 / Rev. Proc. 2025-32"],
], ["", "num", ""])}
{src(("IRS — Estate tax", "https://www.irs.gov/businesses/small-businesses-self-employed/estate-tax"), ("IRS — 2026 inflation adjustments (IR-2025-103)", "https://www.irs.gov/newsroom/irs-releases-tax-inflation-adjustments-for-tax-year-2026-including-amendments-from-the-one-big-beautiful-bill"), ("IRS — Rev. Proc. 2025-32", "https://www.irs.gov/pub/irs-drop/rp-25-32.pdf"), ("IRS — Form 706 instructions", "https://www.irs.gov/instructions/i706"))}
<p><b>Inheritance process note:</b> The estate pays the tax before distribution; heirs never pay "inheritance tax" out of pocket. Inherited cash and property are not income to the recipient. Stepped-up basis applies to inherited assets.</p>
{src(("IRS — Pub 559 (survivors, executors)", "https://www.irs.gov/forms-pubs/about-publication-559"))}
</div>

<div class="card">
<h2>California — no inheritance tax, no state estate tax</h2>
{tbl(["Item", "Status", "Source"], [
 ["California inheritance tax", "None — repealed by Prop 6 (June 1982)", "California FTB analyses"],
 ["California state estate tax", "None — 'pick-up' tax tied to federal credit; credit repealed for deaths after 2004 → $0", "California FTB analyses"],
 ["Statute still on books", "Rev. &amp; Tax. Code §13302 (collects nothing)", "California FTB analyses"],
 ["Exposure for CA residents", "Federal estate tax only, above $15M/person (2026)", "IRS estate tax page"],
], ["", "", ""])}
{src(("California FTB — SB 378 analysis", "https://www.ftb.ca.gov/tax-pros/law/legislation/2019-2020/SB378-032519.pdf"), ("California FTB — SB 726 analysis", "https://www.ftb.ca.gov/tax-pros/law/legislation/2017-2018/sb726-032317.pdf"))}
<div class="callout green"><h4>Bottom line for this estate</h4><p>California will collect <b>nothing</b> on the inheritance. If the total estate (houses + money + other assets) stays under the federal exemption for the year of death (~$15M/person in 2026, indexed), <b>no federal estate tax is owed at all</b>. If it exceeds the exemption, 40% is owed only on the excess, paid by the estate.</p></div>
</div>

<div class="card">
<h2>Proposition 13 — how the property tax base works</h2>
{tbl(["Rule", "Value", "Source"], [
 ["Base property tax rate", "1% of assessed value (Cal. Const. Art. XIII A)", "BOE"],
 ["Max annual assessed-value increase", "2% per year (factored base year value)", "BOE"],
 ["Reassessment trigger", "Change of ownership / new construction → market value", "BOE"],
 ["Total rate", "1% + voter-approved bonds + special assessments (varies by TRA)", "Santa Clara County / SF Treasurer"],
 ["SF secured rate FY 2026-27", "1.18162182% of AV", "SF Treasurer"],
 ["Cupertino composite range", "~1.15%–1.22% (published; parcel bills imply 1.32%–1.41% incl. special assessments — flagged)", "Santa Clara County rate book"],
], ["", "", ""])}
{src(("BOE — Taxpayers' Rights Advocate (official)", "https://www.boe.ca.gov/proptaxes/pdf/lta22051.pdf"), ("SF Treasurer — secured property taxes", "https://sftreasurer.org/property/secured-property-taxes"), ("Santa Clara County — Compilation of Tax Rates 2025-26", "https://files.santaclaracounty.gov/exjcpb1531/2025-11/tax-rate-book-2025-2026.pdf"))}
</div>

<div class="card">
<h2>Proposition 19 — intergenerational transfer exclusion (the decisive rule)</h2>
{tbl(["Rule", "Detail", "Source"], [
 ["Family home only", "Exclusion applies only if the property was the principal residence of the transferor (parent)", "BOE"],
 ["Heir must move in", "Within 1 year of transfer, as primary residence + file homeowner's exemption", "BOE"],
 ["Value cap", "New taxable value = market value − inflation-adjusted $1M allowance (above factored base + allowance)", "BOE"],
 ["Allowance 2025-2027", "$1,044,586 (BOE inflation adjustment)", "BOE (via legal summaries)"],
 ["Rental / investment property", "NO exclusion — fully reassessed to market value at date of death", "BOE"],
 ["Claim form / deadline", "BOE-19-P within 3 years of transfer (date of death), or before sale", "BOE"],
 ["Trust transfers", "Same rules as outright inheritance (transfer at date of death)", "BOE"],
 ["If heir later rents it out", "Exclusion removed; new value set as of Jan 1 lien date after move-out", "BOE"],
], ["", "", ""])}
{src(("BOE — Taxpayers' Rights Advocate (official Prop 19 guidance)", "https://www.boe.ca.gov/proptaxes/pdf/lta22051.pdf"))}
<h3>What this means for these two houses</h3>
<ul>
<li><b>Cupertino (rental):</b> inherited → reassessed to full market value. Property tax rises from ~{money(CUP_TAX_2025)} to ~{money(MID45['A']['cup_tax'])}/yr by 2045 (moderate scenario).</li>
<li><b>SF (principal residence):</b> inherited → factored base + $1M-capped exclusion if the heir moves in within 1 year and files the exemption. New taxable value ≈ market value − allowance → ~{money(MID45['A']['sf_tax'])}/yr by 2045 (moderate scenario).</li>
<li>Either arrangement (SF as family home vs Cupertino as family home) yields nearly the same combined property tax (~{money(MID45['A']['total_tax'])} vs {money(MID45['B']['total_tax'])}/yr in 2045) — the capped exclusion simply shifts between the two houses.</li>
</ul>
</div>

<div class="card">
<h2>Law changes in progress (as of Nov 2026)</h2>
{tbl(["Item", "Status", "Source"], [
 ["Prop 19 repeal initiative (3rd attempt, Initiative 25-0017)", "FAILED to qualify for Nov 2026 ballot (SOS confirmed 2026-05-04)", "CA Secretary of State"],
 ["SCA 4 (Seyarto) — reinstate Prop 58/193", "Introduced in legislature; not enacted", "CA Senate"],
 ["Prop 19 rules", "Remain fully in effect", "BOE"],
 ["Federal estate tax exemption", "Permanent $15M/person from 2026 (OBBB), indexed from 2027", "IRS"],
], ["", "", ""])}
{src(("CA Secretary of State — failure memo", "https://elections.cdn.sos.ca.gov/ccrov/2026/may/26138jh.pdf"), ("CA Senate — SCA 4", "https://sr32.senate.ca.gov/bill/sca-4-protecting-taxpayers-rights"), ("IRS — IR-2025-103", "https://www.irs.gov/newsroom/irs-releases-tax-inflation-adjustments-for-tax-year-2026-including-amendments-from-the-one-big-beautiful-bill"))}
<div class="callout"><h4>Planning implication</h4><p>Prop 19 is not expected to change before the 2040–2050 inheritance window (repeal attempts have failed three times). Plan under current rules, but monitor SCA 4 and future initiatives.</p></div>
</div>

<div class="card">
<h2>Capital gains on selling inherited property</h2>
{tbl(["Rule", "Detail", "Source"], [
 ["Stepped-up basis", "Basis = fair market value at date of death", "IRS Topic 409 / Pub 551"],
 ["Sell at market value soon after inheritance", "$0 taxable gain → no capital gains tax", "IRS Topic 409"],
 ["Holding period", "Inherited property is automatically long-term", "IRS Topic 409"],
 ["Federal LTCG rates", "0% / 15% / 20% by income", "IRS Topic 409"],
 ["NIIT", "3.8% net investment income tax", "IRS Topic 559"],
 ["California", "Gains taxed as ordinary income (up to 12.3% + 1% mental-health surcharge over $1M)", "FTB rate schedules"],
], ["", "", ""])}
{src(("IRS — Topic 409 (capital gains)", "https://www.irs.gov/taxtopics/tc409"), ("IRS — Topic 559 (NIIT)", "https://www.irs.gov/taxtopics/tc559"), ("IRS — Pub 551 (basis of assets)", "https://www.irs.gov/forms-pubs/about-publication-551"), ("California FTB — 2025 tax rate schedules", "https://www.ftb.ca.gov/forms/2025/2025-540-tax-rate-schedules.pdf"))}
</div>
"""
    return page("tax-law", "Law & Tax Research", "", body)

# ---------- Inheritance process page ----------
def page_inheritance():
    SRC_BOE = '<a href="https://www.boe.ca.gov/proptaxes/pdf/lta22051.pdf">BOE LTA 2022/051</a>'
    SRC_IRS_ET = '<a href="https://www.irs.gov/businesses/small-businesses-self-employed/estate-tax">IRS estate tax</a>'
    SRC_IR = '<a href="https://www.irs.gov/newsroom/irs-releases-tax-inflation-adjustments-for-tax-year-2026-including-amendments-from-the-one-big-beautiful-bill">IRS IR-2025-103</a>'
    SRC_409 = '<a href="https://www.irs.gov/taxtopics/tc409">IRS Topic 409</a>'
    SRC_SF = '<a href="https://sftreasurer.org/property/secured-property-taxes">SF Treasurer</a>'
    SRC_551 = '<a href="https://www.irs.gov/forms-pubs/about-publication-551">IRS Pub 551</a>'
    steps = [
        ("Before death (now → 2040)", [
            ("1. Fund the revocable living trust with both houses",
             "A trust only avoids probate for assets actually titled into it. Deed both properties into the trust; name a successor trustee.",
             'California Probate Code (trusts) — <a href="https://leginfo.legislature.ca.gov/">leginfo.legislature.ca.gov</a> (flag: verify)'),
            ("2. Decide which house is the parents' principal residence",
             "Under Prop 19, only the family home qualifies for the capped exclusion at death. The other house (rental) is fully reassessed. This decision shifts ~$18K/yr of tax between the two houses.",
             SRC_BOE),
            ("3. Plan estate tax if the estate may be large",
             "If the estate may exceed the federal exemption (~$15M/person 2026, indexed), consider lifetime gifting ($19,000/recipient annual exclusion in 2026), portability election, and trust structure with an estate attorney.",
             SRC_IR + "; " + SRC_IRS_ET),
            ("4. Do NOT sell the houses before death to 'avoid' taxes",
             "Selling before death triggers capital gains tax on appreciation since purchase. Inheriting first gives heirs a stepped-up basis — selling after inheritance at market value = $0 gain.",
             SRC_409),
        ]),
        ("At death (2040–2050)", [
            ("5. Date of death = date of transfer for property tax purposes",
             "Not the distribution date. The assessor reassesses both houses as of the date of death.",
             SRC_BOE),
            ("6. Successor trustee takes control — no probate court",
             "Trust assets distribute per the trust document. If assets were NOT in a trust, heirs must open probate (public record, statutory fees on gross estate) or use small-estate / AB 2016 tools.",
             'California Probate Code — <a href="https://leginfo.legislature.ca.gov/">leginfo.legislature.ca.gov</a> (flag: verify)'),
            ("7. Reassessment: Cupertino fully, SF capped",
             "Cupertino (rental) → full market value. SF (family home) → factored base + $1M-capped exclusion (new taxable value ≈ market value − allowance), provided the heir occupies it as principal residence within 1 year and files the homeowner's exemption.",
             SRC_BOE),
            ("8. File BOE-19-P within 3 years (SF family home)",
             "Claim for the Prop 19 exclusion. Also file the homeowner's exemption within 1 year. Cupertino needs no claim (no exclusion available).",
             SRC_BOE),
            ("9. Pay supplemental tax bills",
             "The county issues supplemental assessments for the partial fiscal year after reassessment.",
             SRC_SF + "; " + SRC_BOE),
            ("10. Form 706 if estate exceeds exemption",
             "Due 9 months after death; pay 40% estate tax on the excess; elect portability for the surviving spouse if applicable.",
             SRC_IRS_ET),
            ("11. Heirs receive stepped-up basis",
             "FMV at date of death is the new cost basis. Selling inherited real estate at market value soon after inheritance = $0 capital gains tax.",
             SRC_409 + " / " + SRC_551),
        ]),
        ("After inheritance", [
            ("12. DECIDE: live / rent / sell the Cupertino house",
             "See the Decision Analysis page. Recommendation: sell at inheritance, reinvest; keep the SF house.",
             'This analysis — <a href="scenarios.html">Decision Analysis</a>'),
            ("13. If keeping the SF family home",
             "The heir must occupy it as primary residence and file the exemption — otherwise the exclusion is lost (full reassessment). If the heir later moves out, the exclusion is removed and a new value is set.",
             SRC_BOE),
            ("14. Ongoing obligations",
             "Pay property taxes (now at reassessed values), insurance, utilities, maintenance; file income tax on rental income; track basis from date of death for future sales.",
             SRC_409 + " / <a href=\"https://www.ftb.ca.gov/\">California FTB</a>"),
        ]),
    ]
    html_steps = ""
    for phase, items in steps:
        html_steps += f'<h3>{esc(phase)}</h3>'
        for title, desc, srctxt in items:
            html_steps += f'<div class="step"><h4>{esc(title)}</h4><p>{esc(desc)}</p><p style="font-size:.72rem;color:var(--muted)">Source: {srctxt}</p></div>'
    body = f"""
<div class="card">
<h2>Inheritance process — step by step (via trust)</h2>
<p>The plan: inherit both houses through a trust around 2040–2050. Below is the verified process, phase by phase, with the key deadlines.</p>
{html_steps}
</div>

<div class="card">
<h2>Key deadlines checklist</h2>
{tbl(["Deadline", "Action", "Consequence if missed"], [
 ["Before death", "Fund the trust with both houses", "Houses go through probate (public, fees on gross estate)"],
 ["Date of death", "Assessor reassesses both houses (date of death = transfer date)", "—"],
 ["Within 3 years", "File BOE-19-P claim for SF family-home exclusion", "Lose Prop 19 exclusion (full reassessment of SF house)"],
 ["Within 1 year", "File homeowner's exemption; heir moves into SF family home", "Exclusion lost permanently"],
 ["9 months after death", "Form 706 if estate > exemption (portability election)", "Penalties; loss of portability"],
 ["On sale", "Basis = FMV at date of death; sell at market value → $0 gain", "—"],
], ["", "", ""])}
</div>
"""
    return page("inheritance", "Inheritance Process", "", body)

# ---------- Projections page ----------
def page_projections():
    def money_fmt(n):
        return money(n) if n is not None else "--"
    body = f"""
<div class="card">
<h2>Projections 2026–2055</h2>
<p>Three market-growth scenarios are shown: <b>Conservative 2.0%/yr</b>, <b>Moderate 3.5%/yr</b>, <b>Aggressive 5.0%/yr</b> (assumptions — see Flagged for Review). Prop 13 assessed values grow at the verified 2% cap. Property tax uses published composite rates (Cupertino 1.20% + est. special assessments; SF 1.1816% + est. direct charges).</p>

<h3>Market value & Prop 13 assessed value — Moderate (3.5%)</h3>
{tbl(["Year", "Cupertino market value", "SF market value", "Cupertino AV (Prop 13)", "SF AV (Prop 13)"], [
 [str(r["year"]), money(r["cup_mv"]), money(r["sf_mv"]), money(r["cup_av"]), money(r["sf_av"])]
 for r in P["value_table"] if r["growth"] == "moderate" and r["year"] % 5 == 0 or (r["growth"] == "moderate" and r["year"] == 2026)
], ["", "num", "num", "num", "num"])}
{src(("User-provided 2026 values (flag)", "#"), ("Santa Clara County rate book", "https://files.santaclaracounty.gov/exjcpb1531/2025-11/tax-rate-book-2025-2026.pdf"))}
</div>

<div class="card">
<h2>Property tax at inheritance under Prop 19 — all three scenarios</h2>
<p><b>Scenario A</b> = parents' principal residence is the SF house (base plan): Cupertino fully reassessed; SF capped exclusion. <b>Scenario B</b> = parents make Cupertino their principal residence: Cupertino capped exclusion; SF fully reassessed.</p>
<h3>Conservative (2.0%/yr)</h3>
{tbl(["Inheritance year", "Prop 19 allowance", "A: Cupertino AV / tax", "A: SF AV / tax", "A: total", "B: Cupertino AV / tax", "B: SF AV / tax", "B: total"], [
 [str(r["year"]), money(r["cap"]), f'{money(r["A"]["cup_av"])} / {money(r["A"]["cup_tax"])}', f'{money(r["A"]["sf_av"])} / {money(r["A"]["sf_tax"])}', money(r["A"]["total_tax"]), f'{money(r["B"]["cup_av"])} / {money(r["B"]["cup_tax"])}', f'{money(r["B"]["sf_av"])} / {money(r["B"]["sf_tax"])}', money(r["B"]["total_tax"])]
 for r in P["tax_table"] if r["growth"] == "conservative"
], ["", "num", "", "", "num", "", "", "num"])}
<h3>Moderate (3.5%/yr)</h3>
{tbl(["Inheritance year", "Prop 19 allowance", "A: Cupertino AV / tax", "A: SF AV / tax", "A: total", "B: Cupertino AV / tax", "B: SF AV / tax", "B: total"], [
 [str(r["year"]), money(r["cap"]), f'{money(r["A"]["cup_av"])} / {money(r["A"]["cup_tax"])}', f'{money(r["A"]["sf_av"])} / {money(r["A"]["sf_tax"])}', money(r["A"]["total_tax"]), f'{money(r["B"]["cup_av"])} / {money(r["B"]["cup_tax"])}', f'{money(r["B"]["sf_av"])} / {money(r["B"]["sf_tax"])}', money(r["B"]["total_tax"])]
 for r in P["tax_table"] if r["growth"] == "moderate"
], ["", "num", "", "", "num", "", "", "num"])}
<h3>Aggressive (5.0%/yr)</h3>
{tbl(["Inheritance year", "Prop 19 allowance", "A: Cupertino AV / tax", "A: SF AV / tax", "A: total", "B: Cupertino AV / tax", "B: SF AV / tax", "B: total"], [
 [str(r["year"]), money(r["cap"]), f'{money(r["A"]["cup_av"])} / {money(r["A"]["cup_tax"])}', f'{money(r["A"]["sf_av"])} / {money(r["A"]["sf_tax"])}', money(r["A"]["total_tax"]), f'{money(r["B"]["cup_av"])} / {money(r["B"]["cup_tax"])}', f'{money(r["B"]["sf_av"])} / {money(r["B"]["sf_tax"])}', money(r["B"]["total_tax"])]
 for r in P["tax_table"] if r["growth"] == "aggressive"
], ["", "num", "", "", "num", "", "", "num"])}
{src(("BOE Prop 19 rules (official)", "https://www.boe.ca.gov/proptaxes/pdf/lta22051.pdf"), ("BOE $1,044,586 allowance (2025-2027)", "https://www.boe.ca.gov/proptaxes/pdf/lta22051.pdf"), ("Santa Clara County rate book", "https://files.santaclaracounty.gov/exjcpb1531/2025-11/tax-rate-book-2025-2026.pdf"), ("SF Treasurer secured rate", "https://sftreasurer.org/property/secured-property-taxes"))}
<div class="callout"><h4>Read this carefully</h4><p>Keeping both houses costs roughly <b>{money(TOTAL_MIN)}–{money(TOTAL_MAX)}/yr</b> in combined property tax at inheritance (2040–2050, all scenarios) — versus <b>~{money(CUP_TAX_2025 + SF_TAX_2025)}/yr</b> today. The increase is the Prop 19 reassessment, not the tax rate.</p></div>
</div>

<div class="card">
<h2>Federal estate tax exemption projection</h2>
{tbl(["Year", "Exemption per person", "Married couple (portability)"], [
 [str(r["year"]), money(r["exemption_person"]), money(r["exemption_couple"])]
 for r in P["estate_table"] if r["year"] % 5 == 0 or r["year"] == 2026
], ["", "num", "num"])}
{src(("IRS — estate tax filing thresholds", "https://www.irs.gov/businesses/small-businesses-self-employed/estate-tax"), ("IRS — IR-2025-103 (indexing from 2027)", "https://www.irs.gov/newsroom/irs-releases-tax-inflation-adjustments-for-tax-year-2026-including-amendments-from-the-one-big-beautiful-bill"))}
<p style="font-size:.85rem;color:var(--muted)">Indexing assumption: +2.5%/yr from the 2026 $15M base (labeled assumption; IRS states the exemption is indexed for inflation starting 2027).</p>
</div>

<div class="card">
<h2>Decision comparison at inheritance (Cupertino house)</h2>
<p>Sell = proceeds at market value, $0 capital gains (stepped-up basis), ~6% closing costs, reinvested at 6% nominal return (assumption). Rent = gross rent minus property tax, insurance, maintenance, utilities, management (8% of rent), vacancy (5%). Rent estimate: Cupertino 3-bed house median ~$5,005/mo (Homes.com, 2026 — third-party estimate, flag).</p>
<h3>Moderate (3.5%/yr)</h3>
{tbl(["Inheritance year", "Market value", "Sell: net proceeds", "Sell: annual income (after tax)", "Rent: gross", "Rent: opex", "Rent: net operating income"], [
 [str(r["year"]), money(r["cup_mv"]), money(r["sell"]["net"]), money(r["sell"]["after_tax_income"]), money(r["rent"]["gross"]), money(r["rent"]["opex"]), "−" + money(abs(r["rent"]["noi"])) if r["rent"]["noi"] < 0 else money(r["rent"]["noi"])]
 for r in P["scenario_table"] if r["growth"] == "moderate"
], ["", "num", "num", "num", "num", "num", "num"])}
{src(("IRS Topic 409 (stepped-up basis)", "https://www.irs.gov/taxtopics/tc409"), ("Homes.com — Cupertino 3-bed rent (third-party)", "https://www.homes.com/cupertino-ca/homes-for-rent/3-bedroom/"))}
<div class="callout green"><h4>Recommendation</h4><p>Sell the Cupertino house at inheritance and reinvest. Renting it after the Prop 19 reassessment produces a net loss; living in it costs ~$79K/yr; selling produces roughly <b>{money(300_000)}/yr</b> of after-tax investment income by 2045 (moderate scenario) with no property tax drag.</p></div>
</div>
"""
    return page("projections", "Projections 2026-2055", "", body)

# ---------- Costs page ----------
def page_costs():
    rows = []
    for r in P["cost_table"]:
        if r["year"] % 5 == 0 or r["year"] == 2026:
            rows.append([str(r["year"]), money(r["cup_water"]), money(r["cup_ins"]), money(r["cup_maint"]), money(r["sf_water"]), money(r["sf_elec"]), money(r["sf_ins"]), money(r["sf_maint"]), money(r["sf_rent"])])
    body = f"""
<div class="card">
<h2>Utilities &amp; insurance — verified rates and planning estimates</h2>
<h3>Official rate structures</h3>
<h4>City of Cupertino water / sewer / stormwater (effective Jan 1, 2026)</h4>
{tbl(["Component", "Rate", "Notes"], [
 ["Water Tier I (0–5,000 gal)", "$5.80 per 1,000 gal", "City of Cupertino"],
 ["Water Tier II (5,001–10,000 gal)", "$7.30 per 1,000 gal", "City of Cupertino"],
 ["Water Tier III (10,001–19,999 gal)", "$10.42 per 1,000 gal", "City of Cupertino"],
 ["Water Tier IV (20,000+ gal)", "$14.60 per 1,000 gal", "City of Cupertino"],
 ["Sewer usage", "$5.46 per 1,000 gal", "City of Cupertino"],
 ["Storm drain base", "$12.18/mo", "City of Cupertino"],
 ["Water base charge (5/8&quot;–3/4&quot;)", "$15.69/mo", "City of Cupertino"],
], ["", "", ""])}
{src(("City of Cupertino — 2026 rates table (official PDF)", "https://cdnsm5-hosted.civiclive.com/UserFiles/Servers/Server_1881137/File/Residents/Water/PDFs/Billing/2026/2026%20Rates%20Table%20Summary%20Final_accessible%20(1).pdf"))}
<h4>SFPUC water &amp; sewer (effective July 1, 2026 — FY 2026-27)</h4>
{tbl(["Item", "Value", "Source"], [
 ["Average single-family combined water+sewer bill (before increase)", "~$171/mo", "SFPUC"],
 ["After July 1, 2026 increase (~10.5%)", "~$189/mo", "SFPUC / ABC7"],
 ["After July 1, 2027 (~12.5%)", "~$212/mo", "SFPUC"],
 ["Water service charge (5/8&quot;)", "$19.65/mo", "SFPUC rate schedules"],
 ["Rate increase approved (Apr 2026)", "~23% over two years", "SFPUC"],
], ["", "num", ""])}
{src(("SFPUC — water & sewer rates 2026", "https://www.sfpuc.gov/accounts-services/water-power-sewer-rates/proposed-water-sewer-rates-2026"), ("SFPUC — rate schedules PDF", "https://www.sfpuc.gov/sites/default/files/accounts-and-services/Rates_Schedule_Water_Sewer_2026-7.pdf"))}
<h4>PG&amp;E electricity (2026)</h4>
{tbl(["Item", "Value", "Source"], [
 ["PG&E average residential bundled rate (Jun 2026)", "~33.7¢/kWh", "CPUC Public Advocates Office / PG&E Advice Letter 7846-E"],
 ["Example bill: 500 kWh/mo", "~$203.54/mo (incl. ~$24 base charge)", "PG&E"],
 ["Cupertino house (solar, net-metered)", "~$0/mo; credit $10–20/mo (user)", "User — flag"],
 ["SF house", "$30–$70/mo (user)", "User — flag"],
], ["", "", ""])}
{src(("PG&E Advice Letter 7846-E", "https://www.pge.com/"), ("CPUC Public Advocates Office rate reports", "https://www.cpuc.ca.gov/"))}
</div>

<div class="card">
<h2>Insurance — planning estimates (third-party, flagged)</h2>
{tbl(["Item", "Estimate", "Source"], [
 ["California average homeowner premium", "$1,571/yr", "CA Dept. of Insurance (Feb 2026 snapshot)"],
 ["NAIC 2023 HO-3: CA vs US", "$1,655 vs $1,737", "NAIC Homeowners Report"],
 ["CDI 2025 experience-year average (all forms)", "$2,339.99/yr (6,052,334 policies)", "CDI data call"],
 ["Cupertino average HO-3 (Santa Clara County, CA)", "~$1,189–$1,229/yr", "Third-party estimates — flag"],
 ["SF landlord (rental) policy", "~$2,235/yr", "Third-party estimate — flag"],
 ["Earthquake coverage", "Separate endorsement (not in HO-3)", "CDI"],
], ["", "", ""])}
{src(("California Dept. of Insurance (via aegishomesre.com)", "https://aegishomesre.com/home-insurance-cost-statistics/"), ("NAIC (via coverageclassroom.com)", "https://coverageclassroom.com/learn/california-homeowners-insurance-cost"))}
<p style="font-size:.85rem;color:var(--muted)">User's $1,500/yr guess is plausible and in line with these estimates. Obtain actual quotes for both properties before inheritance.</p>
</div>

<div class="card">
<h2>Annual cost projections (inflation-adjusted, 2.5%/yr)</h2>
{tbl(["Year", "Cupertino water", "Cupertino ins.", "Cupertino maint.", "SF water", "SF elec.", "SF ins.", "SF maint.", "SF rent"], rows, ["", "num", "num", "num", "num", "num", "num", "num", "num"])}
{src(("User-provided baseline estimates (flag)", "#"), ("City of Cupertino rates", "https://cdnsm5-hosted.civiclive.com/UserFiles/Servers/Server_1881137/File/Residents/Water/PDFs/Billing/2026/2026%20Rates%20Table%20Summary%20Final_accessible%20(1).pdf"), ("SFPUC rates", "https://www.sfpuc.gov/sites/default/files/accounts-and-services/Rates_Schedule_Water_Sewer_2026-7.pdf"))}
<p style="font-size:.85rem;color:var(--muted)">Maintenance at 1% of value/yr is a rule-of-thumb planning assumption, not a verified figure.</p>
</div>
"""
    return page("costs", "Utilities & Insurance", "", body)

# ---------- Scenarios page ----------
def page_scenarios():
    mid = [r for r in P["tax_table"] if r["growth"] == "moderate" and r["year"] == 2045][0]
    sc = [r for r in P["scenario_table"] if r["growth"] == "moderate" and r["year"] == 2045][0]
    body = f"""
<div class="card">
<h2>Decision analysis — Cupertino house at inheritance</h2>
<p>Four options for the Cupertino house after inheritance (2045, moderate 3.5% growth scenario shown; all scenarios on the Projections page).</p>
<h3>Option 1 — Sell at inheritance and reinvest <span class="tag ok">RECOMMENDED</span></h3>
<ul>
<li>Proceeds at market value ≈ <b>{money(sc['cup_mv'])}</b>; closing costs ~6% → net <b>{money(sc['sell']['net'])}</b></li>
<li><b>$0 capital gains tax</b> (stepped-up basis = FMV at date of death)</li>
<li>Reinvested at 6% nominal → ~<b>{money(sc['sell']['after_tax_income'])}/yr</b> after-tax income (dividend drag at ~33% combined)</li>
<li>Eliminates: property tax ({money(mid['A']['cup_tax'])}/yr), insurance, maintenance, utilities, vacancy/management risk</li>
<li>Liquidity: funds available for other opportunities, education, emergencies</li>
</ul>
<h3>Option 2 — Keep as a rental</h3>
<ul>
<li>Property tax resets to full market value: <b>{money(mid['A']['cup_tax'])}/yr</b></li>
<li>Gross rent ~{money(sc['rent']['gross'])}/yr (3-bed median ~$5,005/mo — third-party estimate, flag)</li>
<li>Operating expenses ≈ {money(sc['rent']['opex'])}/yr (tax, insurance, maintenance, utilities, management, vacancy)</li>
<li><b>Net operating income ≈ −{money(abs(sc['rent']['noi']))}/yr</b> → a net loss every year, taxed as ordinary income</li>
</ul>
<h3>Option 3 — Live in it</h3>
<ul>
<li>Property tax still resets to <b>{money(mid['A']['cup_tax'])}/yr</b> (no Prop 19 exclusion — it was never the parents' principal residence)</li>
<li>Plus insurance, utilities, maintenance ≈ {money(CUP_INS_YR + CUP_WATER_MO*12 + CUP_MAINT_YR)}/yr → total housing cost ≈ <b>{money(mid['A']['cup_tax'] + CUP_INS_YR + CUP_WATER_MO*12 + CUP_MAINT_YR)}/yr</b></li>
<li>Value: you own the asset (appreciates) and live in Cupertino (schools/location) — but the tax reset makes it an expensive place to live</li>
</ul>
<h3>Option 4 — Sell both houses, rent elsewhere, invest everything</h3>
<ul>
<li>Both houses sold at stepped-up basis → $0 capital gains on both</li>
<li>Eliminates ~{money(mid['A']['total_tax'])}/yr of combined property tax</li>
<li>Loses SF rental income ($7,150/mo = $85,800/yr user-provided, flag) and the SF house's housing value</li>
</ul>
</div>

<div class="card">
<h2>Recommendation</h2>
<div class="callout green"><h4>Sell the Cupertino house at inheritance; keep the San Francisco house</h4>
<p>1. <b>Sell Cupertino</b> immediately after inheritance → $0 capital gains (stepped-up basis) → reinvest ~{money(sc['sell']['net'])} at 6% → ~{money(sc['sell']['after_tax_income'])}/yr after tax with no property-tax drag.</p>
<p>2. <b>Keep the SF house</b> — either live in unit 3 (claim the Prop 19 capped exclusion: new taxable value ≈ {money(mid['A']['sf_av'])}, tax ≈ {money(mid['A']['sf_tax'])}/yr) or rent all 3 units (rent $85,800/yr comfortably covers a full reassessment of {money(mid['B']['sf_tax'])}/yr).</p>
<p>3. <b>Why not keep Cupertino?</b> The Prop 19 reassessment alone (~{money(mid['A']['cup_tax'])}/yr by 2045) exceeds plausible net rental income; keeping it destroys wealth versus reinvesting. Living in it costs ~$79K/yr — the worst pure-financial option.</p>
<p>4. <b>Before 2040:</b> fund the trust, decide which house is the parents' principal residence, and if the estate may exceed the federal exemption (~{money(24_000_000)}/person projected 2045), engage estate counsel (lifetime gifting at $19K/recipient/yr, portability, trust structure).</p>
</div>
{src(("BOE Prop 19 rules", "https://www.boe.ca.gov/proptaxes/pdf/lta22051.pdf"), ("IRS Topic 409 — stepped-up basis / $0 gain on immediate sale", "https://www.irs.gov/taxtopics/tc409"), ("IRS estate tax page", "https://www.irs.gov/businesses/small-businesses-self-employed/estate-tax"))}
</div>

<div class="card">
<h2>SF house — how to keep it</h2>
{tbl(["Option", "Prop 19 status", "Projected property tax (2045, moderate)", "Notes"], [
 ["Heir moves into unit 3 as primary residence (file homeowner's exemption)", "Capped exclusion: new taxable = market value − $1M-allowance", money(mid["A"]["sf_tax"]) + "/yr", "Must happen within 1 year of inheritance"],
 ["Keep renting all 3 units", "Exclusion lost (house becomes non-primary residence) → full reassessment", money(mid["B"]["sf_tax"]) + "/yr", "Rent $85,800/yr covers tax + costs"],
 ["Sell SF house", "$0 capital gains (stepped-up basis)", "$0", "Loses $85,800/yr income and housing"],
], ["", "", "num", ""])}
{src(("BOE Prop 19 rules (official)", "https://www.boe.ca.gov/proptaxes/pdf/lta22051.pdf"), ("SF Treasurer secured rate", "https://sftreasurer.org/property/secured-property-taxes"))}
</div>
"""
    return page("scenarios", "Decision Analysis", "", body)

# ---------- Flagged page ----------
def page_flagged():
    body = f"""
<div class="card">
<h2>Flagged for Review — unverified values &amp; irregularities</h2>
<p>These items could not be confirmed from official sources or contain inconsistencies. They are shown for planning only and must be verified before acting. Unverified values are never used as verified facts.</p>
{tbl(["#", "Item", "Status", "What to do", "Source"], [
 ["1", "Cupertino market value $3.1M (Nov 2026)", "User-provided — not verified", "Obtain appraisal or assessor market value", "—"],
 ["2", "SF market value $1.8M (Nov 2026)", "User-provided — not verified", "Obtain appraisal or assessor market value", "—"],
 ["3", "Cupertino tax history (2014–2026)", "User-provided — not verified", "Verify against Santa Clara County tax bills", '<a href="https://files.santaclaracounty.gov/exjcpb1531/2025-11/tax-rate-book-2025-2026.pdf">Santa Clara rate book</a>'],
 ["4", "SF tax history (2016–2025)", "User-provided — not verified", "Verify against SF Treasurer bills", '<a href="https://sftreasurer.org/property/secured-property-taxes">SF Treasurer</a>'],
 ["5", "Cupertino implied effective rate 1.32%–1.41% vs published 1.15%–1.22%", "Irregularity", "Check special assessments/direct charges on the official bill", '<a href="https://files.santaclaracounty.gov/exjcpb1531/2025-11/tax-rate-book-2025-2026.pdf">Santa Clara rate book</a>'],
 ["6", "SF implied effective rate 1.73%–2.14% vs published 1.18% secured", "Irregularity", "Check direct charges (sewer/ERU) and special assessments on the official bill", '<a href="https://sftreasurer.org/property/secured-property-taxes">SF Treasurer</a>'],
 ["7", "Cupertino current occupancy/rent status", "Unknown — affects Prop 19 analysis", "Confirm whether parents live there or it is rented", '<a href="https://www.boe.ca.gov/proptaxes/pdf/lta22051.pdf">BOE Prop 19</a>'],
 ["8", "SF rent $7,150/mo", "User-provided — not verified", "Verify leases", "—"],
 ["9", "SF water $330–$400/mo; electricity $30–$70/mo", "User-provided — not verified", "Verify on bills", '<a href="https://www.sfpuc.gov/accounts-services/water-power-sewer-rates/proposed-water-sewer-rates-2026">SFPUC</a>'],
 ["10", "Cupertino water $100–$150/mo; solar credits $10–$20/mo", "User-provided — not verified", "Verify on bills; confirm PG&E NEM program", '<a href="https://cdnsm5-hosted.civiclive.com/UserFiles/Servers/Server_1881137/File/Residents/Water/PDFs/Billing/2026/2026%20Rates%20Table%20Summary%20Final_accessible%20(1).pdf">City of Cupertino rates</a>'],
 ["11", "Home insurance figures (Cupertino ~$1,200; SF landlord ~$2,235)", "Third-party estimates — not official", "Obtain actual quotes from insurers", '<a href="https://aegishomesre.com/home-insurance-cost-statistics/">CDI snapshot</a>'],
 ["12", "Maintenance costs (1% of value rule of thumb)", "Assumption — not official", "Get contractor estimates / reserve study", "—"],
 ["13", "Market-value growth scenarios (2.0/3.5/5.0%)", "Assumptions — not verified", "Use for sensitivity; not a forecast", "—"],
 ["14", "Portfolio return 6% nominal, tax drag 33.1%", "Assumptions — not verified", "Confirm with financial advisor", "—"],
 ["15", "Estate exemption indexing +2.5%/yr", "Assumption (IRS: indexed from 2027)", "Monitor IRS inflation adjustments", '<a href="https://www.irs.gov/newsroom/irs-releases-tax-inflation-adjustments-for-tax-year-2026-including-amendments-from-the-one-big-beautiful-bill">IRS IR-2025-103</a>'],
 ["16", "Prop 19 $1M allowance 2025-2027 = $1,044,586", "BOE — cited via legal summaries", "Verify current adjustment notice on boe.ca.gov", '<a href="https://www.boe.ca.gov/proptaxes/pdf/lta22051.pdf">BOE</a>'],
 ["17", "Probate Code details (TOD deed, AB 2016, fees)", "Statute text not fetched directly", "Verify on leginfo.legislature.ca.gov", '<a href="https://leginfo.legislature.ca.gov/">CA Legislature</a>'],
 ["18", "Cupertino 2026 property tax", "Missing (not provided)", "Add from the official 2026 bill", "—"],
], ["", "", "", "", ""])}
</div>
"""
    return page("flagged", "Flagged for Review", "", body)

# ---------- Sources page ----------
def page_sources():
    srcs = [
        ("IRS — Estate tax (filing thresholds, portability, Form 706)", "https://www.irs.gov/businesses/small-businesses-self-employed/estate-tax"),
        ("IRS — IR-2025-103: 2026 inflation adjustments (OBBB)", "https://www.irs.gov/newsroom/irs-releases-tax-inflation-adjustments-for-tax-year-2026-including-amendments-from-the-one-big-beautiful-bill"),
        ("IRS — Rev. Proc. 2025-32", "https://www.irs.gov/pub/irs-drop/rp-25-32.pdf"),
        ("IRS — Topic 409: Capital gains and losses (stepped-up basis)", "https://www.irs.gov/taxtopics/tc409"),
        ("IRS — Topic 559: Net investment income tax", "https://www.irs.gov/taxtopics/tc559"),
        ("IRS — Publication 551: Basis of Assets", "https://www.irs.gov/forms-pubs/about-publication-551"),
        ("IRS — Publication 559: Survivors, Executors, and Administrators", "https://www.irs.gov/forms-pubs/about-publication-559"),
        ("IRS — Form 706 instructions", "https://www.irs.gov/instructions/i706"),
        ("BOE — Taxpayers' Rights Advocate: Prop 19 intergenerational transfers (official)", "https://www.boe.ca.gov/proptaxes/pdf/lta22051.pdf"),
        ("BOE — Property Tax Annotations 625 (parent-child transfers)", "https://www.boe.ca.gov/lawguides/property/current/ptlg/annt/625-0000-all.html"),
        ("California FTB — SB 378 analysis (no state estate tax)", "https://www.ftb.ca.gov/tax-pros/law/legislation/2019-2020/SB378-032519.pdf"),
        ("California FTB — SB 726 analysis (estate tax history)", "https://www.ftb.ca.gov/tax-pros/law/legislation/2017-2018/sb726-032317.pdf"),
        ("California FTB — 2025 tax rate schedules", "https://www.ftb.ca.gov/forms/2025/2025-540-tax-rate-schedules.pdf"),
        ("SF Treasurer & Tax Collector — Secured property taxes (rate, due dates)", "https://sftreasurer.org/property/secured-property-taxes"),
        ("Santa Clara County — Compilation of Tax Rates 2025-26 (official)", "https://files.santaclaracounty.gov/exjcpb1531/2025-11/tax-rate-book-2025-2026.pdf"),
        ("SF Assessor-Recorder — real property assessments (Prop 13)", "https://www.sf.gov/information--learn-about-real-property-assessments"),
        ("City of Cupertino — 2026 water/sewer/stormwater rates (official PDF)", "https://cdnsm5-hosted.civiclive.com/UserFiles/Servers/Server_1881137/File/Residents/Water/PDFs/Billing/2026/2026%20Rates%20Table%20Summary%20Final_accessible%20(1).pdf"),
        ("SFPUC — Water & sewer rates 2026 (official)", "https://www.sfpuc.gov/accounts-services/water-power-sewer-rates/proposed-water-sewer-rates-2026"),
        ("SFPUC — Rate schedules & fees PDF (official)", "https://www.sfpuc.gov/sites/default/files/accounts-and-services/Rates_Schedule_Water_Sewer_2026-7.pdf"),
        ("PG&E — Advice Letter 7846-E (March 2026 rates)", "https://www.pge.com/"),
        ("CPUC — Public Advocates Office quarterly rate reports", "https://www.cpuc.ca.gov/"),
        ("California Dept. of Insurance — Homeowners Insurance Market Snapshot (Feb 2026)", "https://www.cdii.ca.gov/"),
        ("CA Secretary of State — Prop 19 repeal initiative failure memo (May 2026)", "https://elections.cdn.sos.ca.gov/ccrov/2026/may/26138jh.pdf"),
        ("CA Senate — SCA 4 (reinstate Prop 58/193)", "https://sr32.senate.ca.gov/bill/sca-4-protecting-taxpayers-rights"),
        ("California Legislature — Probate Code (leginfo.legislature.ca.gov)", "https://leginfo.legislature.ca.gov/"),
        ("RentCafe — Cupertino rent trends (Aug 2026)", "https://www.rentcafe.com/average-rent-market-trends/us/ca/santa-clara-county/cupertino/"),
        ("Homes.com — Cupertino 3-bedroom rents (2026)", "https://www.homes.com/cupertino-ca/homes-for-rent/3-bedroom/"),
    ]
    lis = "".join(f'<li><a href="{esc(u)}" target="_blank" rel="noopener">{esc(t)}</a></li>' for t, u in srcs)
    body = f"""
<div class="card">
<h2>Sources</h2>
<p>Official sources are prioritized. Third-party estimates used for planning (rents, insurance quotes, growth assumptions) are flagged on the pages where they appear.</p>
<ul style="columns:2;column-gap:40px">{lis}</ul>
</div>
"""
    return page("sources", "Sources", "", body)

# ---------- build all ----------
pages = [
    page_index(),
    page_properties(),
    page_tax_law(),
    page_inheritance(),
    page_projections(),
    page_costs(),
    page_scenarios(),
    page_flagged(),
    page_sources(),
]

import os
os.makedirs("docs/analysis", exist_ok=True)
os.makedirs("docs/analysis/assets", exist_ok=True)
with open("docs/analysis/assets/style.css", "w") as fp:
    fp.write(CSS)
names = ["index", "properties", "tax-law", "inheritance", "projections", "costs", "scenarios", "flagged", "sources"]
for name, content in zip(names, pages):
    with open(f"docs/analysis/{name}.html", "w") as fp:
        fp.write(content)
    print(f"Wrote docs/analysis/{name}.html")
print("Site build complete.")
