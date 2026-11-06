#!/usr/bin/env python3
"""Build the static GitHub Pages site from data/ia/*.json (standard library only).

Writes (relative to repo root):
  index.html, facts/, property/, costs/, projections/, decision/, process/, law/,
  flagged/, sources/, assets/site.css, assets/site.js

All numbers come from data/ia/projections.json (scripts/model.py) or the register files.
Every table row carries a source link: an official URL from data/ia/sources.json, or a link
to the matching Flagged-for-Review entry when the value is UNVERIFIED.
"""
import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
D = ROOT / "data" / "ia"
BUILD_DATE = "2026-11-06"

SOURCES = {s["id"]: s for s in json.loads((D / "sources.json").read_text())["sources"]}
FACTS = json.loads((D / "facts.json").read_text())
INPUTS = json.loads((D / "inputs.json").read_text())
FLAGS = json.loads((D / "flags.json").read_text())["flags"]
PROJ = json.loads((D / "projections.json").read_text())
FLAG_IDS = {f["id"] for f in FLAGS}

NAV = [
    ("Overview", "", "index.html"),
    ("Facts", "facts/", "facts/index.html"),
    ("Property", "property/", "property/index.html"),
    ("Costs", "costs/", "costs/index.html"),
    ("Projections", "projections/", "projections/index.html"),
    ("Decision", "decision/", "decision/index.html"),
    ("Process", "process/", "process/index.html"),
    ("Law", "law/", "law/index.html"),
    ("Flagged", "flagged/", "flagged/index.html"),
    ("Sources", "sources/", "sources/index.html"),
]


# ---------- helpers ----------
def esc(x):
    return html.escape(str(x), quote=True)


def money(x, dec=0):
    return f"${x:,.{dec}f}"


def pct(x, dec=2):
    return f"{x*100:.{dec}f}%"


def src_link(sid, prefix):
    s = SOURCES.get(sid)
    if not s:
        return esc(sid)
    tag = "official" if s["tier"] == "official" else "secondary"
    return (f'<a class="src {tag}" href="{esc(s["url"])}" target="_blank" rel="noopener" '
            f'title="{esc(s["title"])}">{esc(s["publisher"].split(" (")[0])} <span class="sid">{sid}</span></a>')


def flag_link(fid, prefix):
    return f'<a class="flagref" href="{prefix}flagged/#{fid}">{fid}</a>'


def srcs_cell(ids, prefix, flags=None):
    parts = [src_link(i, prefix) for i in ids]
    parts += [flag_link(f, prefix) for f in (flags or [])]
    return " ".join(parts) if parts else '<span class="muted">none</span>'


def status_badge(status):
    s = status.lower()
    if s.startswith("verified"):
        return '<span class="badge ok">VERIFIED</span>'
    if "unverified" in s:
        return '<span class="badge warn">UNVERIFIED</span>'
    if "assumption" in s or "planning" in s:
        return '<span class="badge mute">ASSUMPTION</span>'
    if "client" in s:
        return '<span class="badge client">CLIENT INPUT</span>'
    return f'<span class="badge mute">{esc(status)}</span>'


def table(headers, rows, cls="", filterable=True):
    head = "".join(f"<th>{esc(h)}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    f = ' data-filter="1"' if filterable else ""
    return (f'<div class="tablewrap"><table class="{cls}"{f}><thead><tr>{head}</tr></thead>'
            f"<tbody>{body}</tbody></table></div>")


def page(title, depth, active, body, desc=""):
    prefix = "../" * depth
    nav = "".join(
        f'<a href="{prefix}{href}"{" class=active" if label == active else ""}>{esc(label)}</a>'
        for label, _, href in NAV
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{esc(desc or 'Source-linked decision analysis for inherited California property.')}">
<title>{esc(title)} · Inheritance Decision Analysis</title>
<link rel="stylesheet" href="{prefix}assets/site.css">
</head><body>
<header class="top">
  <div class="brand"><span class="mark">IDA</span><span>Inheritance Decision Analysis<small>Two California properties · source-linked · anonymized</small></span></div>
  <span class="asof">Data as of {BUILD_DATE}</span>
</header>
<nav class="nav">{nav}</nav>
<main>
{body}
</main>
<footer>
  <p>Anonymized planning dashboard. No names, addresses, parcel numbers or precise ZIP codes are published. Client figures are labeled as client inputs and are unverified. Projections are modeled outcomes, not forecasts. Not legal, tax, insurance or investment advice; confirm with qualified professionals.</p>
  <p>Other analyses in this repository (separate sessions, different assumptions, not reconciled): <a href="{prefix}docs/index.html">/docs/ analysis</a> · <a href="{prefix}guide/index.html">guide analysis</a>.</p>
  <p>Built from <code>data/ia/*.json</code> by <code>scripts/build_site.py</code>. Model: <code>scripts/model.py</code>. Checks: <code>scripts/validate.py</code>.</p>
</footer>
<script src="{prefix}assets/site.js"></script>
</body></html>
"""


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


# ---------- numbers pulled from the model ----------
def summary(prop, T, scen, option_prefix):
    for r in PROJ["summary"]:
        if r["property"] == prop and r["T"] == T and r["scenario"] == scen and r["option"].startswith(option_prefix):
            return r
    raise KeyError((prop, T, scen, option_prefix))


def be_rent(T, scen):
    for r in PROJ["breakeven_rent_A"]:
        if r["T"] == T and r["scenario"] == scen:
            return r
    raise KeyError((T, scen))


def sens(label_prefix):
    for r in PROJ["sensitivities"]:
        if r["label"].startswith(label_prefix):
            return r["end_real_2026"]
    raise KeyError(label_prefix)


BASE = "base"
BT = PROJ["meta"]["base_illustration_year"]
RATE_A = PROJ["meta"]["effective_tax_rates"]["A_implied"]
RATE_B = PROJ["meta"]["effective_tax_rates"]["B_implied"]
ECON = PROJ["economic_cost_A"]
A_LIVE = summary("A", BT, BASE, "Live")["end_real_2026"]
A_SELL = summary("A", BT, BASE, "Sell")["end_real_2026"]
A_PROCEEDS = summary("A", BT, BASE, "Sell")["net_proceeds_at_T"]
B_HYB = summary("B", BT, BASE, "Heir lives")["end_real_2026"]
B_FULL = summary("B", BT, BASE, "No occupancy")["end_real_2026"]
B_SELL = summary("B", BT, BASE, "Sell")["end_real_2026"]
B_BEST_KEEP = sens("B hybrid BEST CASE")
PROP19_B_VALUE = B_HYB - B_FULL
BE = be_rent(BT, BASE)

# verify the recommendation is consistent with the model before writing it
for T in PROJ["meta"]["inheritance_years_tested"]:
    for sk in PROJ["scenarios"]:
        assert summary("A", T, sk, "Sell")["end_real_2026"] > summary("A", T, sk, "Live")["end_real_2026"], ("A", T, sk)
        assert summary("B", T, sk, "Sell")["end_real_2026"] > summary("B", T, sk, "Heir lives")["end_real_2026"], ("B-hyb", T, sk)
        assert summary("B", T, sk, "Sell")["end_real_2026"] > summary("B", T, sk, "No occupancy")["end_real_2026"], ("B-full", T, sk)


# ---------- pages ----------
def page_overview():
    fr = FACTS["categories"]
    verified = sum(1 for c in fr for r in c["rows"] if r["status"] == "verified")
    unverified = sum(1 for c in fr for r in c["rows"] if r["status"] == "UNVERIFIED")
    flags_high = sum(1 for f in FLAGS if f["severity"] == "high")
    body = f"""
<section class="hero">
  <p class="eyebrow">Executive summary</p>
  <h1>Sell at inheritance is the strongest modeled plan for both properties</h1>
  <p class="lede">Two California properties may pass through a trust around 2040–2050. Under current law the
  state takes no inheritance tax, and federal estate tax applies only above a large threshold. The main choices are
  to sell, keep and rent, or keep and live in the home. In the base case, selling and investing the proceeds beats
  keeping either property in every inheritance year and stress case tested. The gap is wide for Property A and narrower for Property B in the low-growth case.</p>
  <div class="cta">
    <a class="btn" href="decision/">See the decision analysis</a>
    <a class="btn ghost" href="flagged/">Flagged for review ({len(FLAGS)} items)</a>
  </div>
</section>

<section class="stats">
  <article><small>Federal estate and gift exclusion (2026)</small><strong>$15,000,000</strong><span class="src-line">{src_link('S01','')} {src_link('S02','')}</span></article>
  <article><small>California inheritance or estate tax</small><strong>None</strong><span class="src-line">{src_link('S09','')}</span></article>
  <article><small>Prop 19 value limit (family-home transfers)</small><strong>$1,044,586</strong><span class="src-line">{src_link('S04','')}</span></article>
  <article><small>Prop 19 repeal initiative (May 2026)</small><strong>Failed to qualify</strong><span class="src-line">{src_link('S07','')}</span></article>
</section>

<section class="panel">
  <h2>Base-case result (inheritance in {BT}, end value in 2026 dollars at 2060)</h2>
  {table(["Property", "Option", "End value (real 2026 $)", "Note", "Source"], [
     ["A · Cupertino", "Sell and invest net proceeds", money(A_SELL), f"Net proceeds at {BT}: {money(A_PROCEEDS)}", srcs_cell(["S25"], "", ["FL-15", "FL-13"])],
     ["A · Cupertino", "Live in the home (Prop 19 path)", money(A_LIVE), f"Net annual economic cost of living there: {money(ECON['net_annual_economic_cost'])} (base, {ECON['year']})", srcs_cell(["S04", "S06", "S13"], "", ["FL-01", "FL-02", "FL-05"])],
     ["B · San Francisco", "Sell and invest net proceeds", money(B_SELL), "Modeled wealth from net proceeds", srcs_cell(["S25"], "", ["FL-01", "FL-13"])],
     ["B · San Francisco", "Heir lives in 1 unit; rent 2 units", money(B_HYB), f"Prop 19 on one unit is worth about {money(PROP19_B_VALUE)} vs. no occupancy", srcs_cell(["S06", "S15"], "", ["FL-03", "FL-16", "FL-17"])],
     ["B · San Francisco", "Keep renting 2 units; no occupancy", money(B_FULL), "Full reassessment of the whole property", srcs_cell(["S06"], "", ["FL-17"])],
  ], filterable=False)}
  <p class="muted">Client figures (market values, tax history, water, electricity, insurance, rent) are unverified inputs. Assumptions are labeled on the Projections page. See the <a href="flagged/">Flagged for Review</a> list before relying on any number.</p>
</section>

<section class="panel">
  <h2>Where to look</h2>
  <div class="cards">
    <a class="card" href="facts/"><b>Facts register</b><span>{verified} verified rows, {unverified} unverified rows. Each row links to its official source.</span></a>
    <a class="card" href="property/"><b>Property data</b><span>Anonymized profiles, tax history, and what Prop 19 does to each property.</span></a>
    <a class="card" href="costs/"><b>Carrying costs</b><span>Property tax, water, electricity, insurance, upkeep, with utility sources.</span></a>
    <a class="card" href="projections/"><b>Projections 2026–2050</b><span>Inflation, appreciation, and tax-law assumptions with three stress cases.</span></a>
    <a class="card" href="decision/"><b>Decision</b><span>Live, rent, or sell at 2040, 2045 and 2050, with break-even rent and recommendation.</span></a>
    <a class="card" href="process/"><b>Inheritance process</b><span>Step-by-step trust administration, filings and deadlines with sources.</span></a>
    <a class="card" href="law/"><b>Law changes</b><span>Enacted, pending and failed measures that could change the answer.</span></a>
    <a class="card warn" href="flagged/"><b>Flagged for review</b><span>{len(FLAGS)} items, {flags_high} high severity: irregularities, unverified values, and what would resolve them.</span></a>
  </div>
</section>
"""
    return page("Overview", 0, "Overview", body,
                desc="Inheritance decision analysis for two anonymized California properties: sources, projections, and recommendation.")


def page_facts():
    prefix = "../"
    body = [f'<section class="panel"><p class="eyebrow">Facts register</p><h1>Facts with official sources</h1>'
            f'<p class="muted">{esc(FACTS["rule"])}</p>'
            f'<div class="filterbar"><input type="search" placeholder="Filter rows (e.g. Prop 19, UNVERIFIED, 2026)" aria-label="Filter"></div></section>']
    for c in FACTS["categories"]:
        rows = []
        for r in c["rows"]:
            flags = re.findall(r"FL-\d+", r.get("note", ""))
            if r["status"] == "UNVERIFIED":
                value = '<span class="muted">blank (unverified)</span>'
                srcs = srcs_cell([], prefix, flags or ["FL-21"])
            else:
                value = esc(r["value"])
                srcs = srcs_cell(r["sources"], prefix)
            rows.append([
                f'<code>{esc(r["id"])}</code>', esc(r["item"]), value, status_badge(r["status"]),
                esc(r.get("as_of", "")), srcs, esc(r.get("note", "")),
            ])
        body.append(f'<section class="panel" id="{esc(c["id"])}"><h2>{esc(c["title"])}</h2>'
                    + table(["ID", "Item", "Value", "Status", "As of", "Official source", "Note"], rows) + "</section>")
    return page("Facts", 1, "Facts", "\n".join(body),
                desc="Verified facts register for federal, California, Prop 13/19, deadlines, rent, utilities, insurance, macro, and pending law.")


def page_property():
    prefix = "../"
    A, B = INPUTS["properties"]["A"], INPUTS["properties"]["B"]

    def val(x):
        return esc(x)

    rowsA = [
        ["Location", "Cupertino, Santa Clara County, CA (ZIP omitted)", "client", "", "FL-01"],
        ["Estimated market value (Nov 2026)", money(A["market_value_2026"]["value"]), "client input", "UNVERIFIED", "FL-01"],
        ["Assessed value, 2025 roll", money(A["assessed_value_2025"]["value"]), "client input", "UNVERIFIED", "FL-02"],
        ["Property tax, 2025", money(A["tax_2025"]["value"]), "client input", "UNVERIFIED", "FL-02"],
        ["Effective tax rate (computed from the above)", pct(RATE_A, 3), "derived from client input", "UNVERIFIED", "FL-02"],
        ["Assessed value, 2026 (+2% projection)", money(A["assessed_value_2026_projection"]["value"]), "client projection", "UNVERIFIED", "FL-02, FL-22"],
        ["Occupancy / units", "1 home; solar installed (client)", "client input", "UNVERIFIED", "FL-05"],
    ]
    rowsB = [
        ["Location", "San Francisco, CA (ZIP omitted)", "client", "", "FL-01"],
        ["Estimated market value (Nov 2026)", money(B["market_value_2026"]["value"]), "client input", "UNVERIFIED", "FL-01"],
        ["Assessed value, 2025 roll", money(B["assessed_value_2025"]["value"]), "client input", "UNVERIFIED", "FL-03"],
        ["Property tax, 2025", money(B["tax_2025"]["value"]), "client input", "UNVERIFIED", "FL-03"],
        ["Effective tax rate (computed from the above)", pct(RATE_B, 3), "derived from client input", "UNVERIFIED", "FL-03"],
        ["Livable units", "3 (2 rented; 1 usable by the owner)", "client input", "UNVERIFIED", "FL-16, FL-17"],
        ["Rent, two rented units (total per month)", money(B["rent_monthly_total_two_units"]["value"]), "client input", "UNVERIFIED", "FL-16"],
    ]

    def tbl(rows):
        out = []
        for item, value, kind, status, fl in rows:
            ids = [x.strip() for x in fl.split(",")]
            out.append([esc(item), esc(value), esc(kind), '<span class="badge warn">UNVERIFIED</span>' if status else '<span class="muted">n/a</span>',
                        " ".join(flag_link(i, prefix) for i in ids), srcs_cell([], prefix, ids)])
        return table(["Item", "Value", "Basis", "Status", "Flag", "Official source"], out)

    prop19 = [
        ["Parent-child exclusion applies only if the transferee makes the property a principal residence within 1 year", "Property A: yes if occupied. Property B: only the unit occupied qualifies.", ["S03", "S06"]],
        ["Rented or unoccupied units are fully reassessed at full cash value on transfer", "Property B: 2 rented units reassessed; allocation is decided by the assessor (FL-17).", ["S06"]],
        ["Limit: value above factored base-year value plus $1,044,586 is reassessed", "Model: Property A live case uses the limit; values above it are reassessed.", ["S04", "S06"]],
        ["Trust holding is looked through; LLC transfer disqualifies", "Plan to transfer title directly from the trust, not via an LLC.", ["S06"]],
        ["Homeowners' exemption: $7,000 reduction; file BOE-266 by February 15", "Included as a reduction in the living-case tax.", ["S13"]],
        ["Assessment inflation factor 2026-27 is 1.02", "Prop 13 growth in the no-transfer path (2% per year).", ["S11"]],
    ]
    prop19_rows = [[esc(a), esc(b), srcs_cell(ids, prefix)] for a, b, ids in prop19]

    body = f"""
<section class="panel">
  <p class="eyebrow">Property data</p>
  <h1>Two anonymized properties</h1>
  <p class="muted">Identities, addresses, parcel numbers and owner details are omitted by design. Figures are client inputs, not verified values. They appear only as modeling inputs and are flagged UNVERIFIED.</p>
</section>
<section class="panel"><h2>Property A · Cupertino (Santa Clara County)</h2>{tbl(rowsA)}</section>
<section class="panel"><h2>Property B · San Francisco (3 livable units)</h2>{tbl(rowsB)}</section>
<section class="panel"><h2>What Prop 19 does to each property</h2>
  {table(["Rule", "How it applies here", "Source"], prop19_rows)}
  <p class="muted">Model formula: after a qualifying transfer, assessed value = min(full cash value, base-year value + max(0, full cash value − base-year value − limit)). Without qualification, assessed value = full cash value at transfer.</p>
</section>
"""
    return page("Property", 1, "Property", body, desc="Anonymized property profiles, client tax history, and Prop 19 mechanics.")


def page_costs():
    prefix = "../"
    A, B = INPUTS["properties"]["A"], INPUTS["properties"]["B"]
    rows = [
        ["Property tax (effective rate × assessed value)", pct(RATE_A, 3) + " (client-derived)", pct(RATE_B, 3) + " (client-derived)", "UNVERIFIED", srcs_cell(["S11", "S13"], prefix, ["FL-02", "FL-03"])],
        ["Homeowners' exemption (living case)", "$7,000 reduction", "$7,000 reduction (owner-occupied unit)", "verified rule", srcs_cell(["S13"], prefix)],
        ["Water and sewer, per month", f'{money(A["water_monthly"]["mid"])} (client range $100–$150)', f'{money(B["water_sewer_monthly"]["mid"])} (client range $330–$400)', "UNVERIFIED", srcs_cell(["S14", "S29"], prefix, ["FL-11", "FL-12"])],
        ["Water reference (official, as filed)", "$141.73 per month at 10 CCF (July 1, 2026, as filed)", "$171 per month average single-family, FY26 (SFPUC)", "verified (filed / proposed)", srcs_cell(["S14", "S29"], prefix)],
        ["Electricity, per month", f'Fixed charge {money(A["fixed_charge_monthly"]["value"], 2)} less client credit $15 = {money(9.15, 2)} net (base case)', f'{money(B["electricity_monthly"]["mid"])} (client range $30–$70)', "UNVERIFIED", srcs_cell(["S28"], prefix, ["FL-05", "FL-11"])],
        ["Homeowners / landlord insurance, per year", money(A["insurance_annual"]["value"]) + " (client estimate)", money(B["insurance_annual"]["value"]) + " (client estimate; landlord policy may differ)", "UNVERIFIED", srcs_cell(["S16", "S34"], prefix, ["FL-04"])],
        ["Upkeep and maintenance, share of value per year", pct(A["maintenance_pct_of_value"]["value"], 1) + " (assumption)", pct(B["maintenance_pct_of_value"]["value"], 1) + " (assumption)", "ASSUMPTION", srcs_cell([], prefix, ["FL-15"])],
        ["Rent cap (rent-controlled units, 2026-27)", "Not applicable (no rent figure); statewide AB 1482 cap 5% + CPI, max 10%", "1.6% for March 1, 2026 to February 28, 2027", "verified", srcs_cell(["S27", "S15"], prefix, ["FL-16"])],
        ["Sale transfer tax (county)", "$1.10 per $1,000 (0.11%)", "$1.10 per $1,000 (0.11%)", "verified; city tax UNVERIFIED", srcs_cell(["S25"], prefix, ["FL-13"])],
        ["Santa Clara first installment (2026-27)", "Due Nov 1; paid or postmarked by Dec 10, 2026", "—", "verified (Santa Clara)", srcs_cell(["S12"], prefix)],
        ["San Francisco installments (2026-27)", "—", "Nov 1 / Dec 10 and Feb 1 / Apr 10 are secondary only", "UNVERIFIED", srcs_cell([], prefix, ["FL-09"])],
    ]
    body = f"""
<section class="panel"><p class="eyebrow">Carrying costs</p><h1>What it costs to hold each property</h1>
  <p class="muted">Official values appear only when a source confirms them. Other values are client inputs or labeled assumptions, and each is flagged.</p></section>
<section class="panel"><h2>Operating cost lines</h2>
  {table(["Cost line", "Property A · Cupertino", "Property B · San Francisco", "Status", "Source"], rows)}
</section>
<section class="panel"><h2>Solar: what the official rule says versus the client claim</h2>
  <p>The CPUC states the residential fixed charge is about $24.15 per month for the standard rate. Solar credits are reported not to offset it. The client reports a net credit of $10–$20 per month, which is consistent only if the credit is on energy charges alone, or if the fixed charge is not on the bill. Both cases are modeled, and the base case uses the stricter one ({money(9.15, 2)} net monthly cost).</p>
  <p class="muted">Resolve with 12 months of bills and the interconnection date (see <a href="../flagged/#FL-05">FL-05</a>).</p>
</section>
"""
    return page("Costs", 1, "Costs", body, desc="Property tax, water, electricity, insurance, and upkeep with sources and flags.")


def yearly_tables():
    base = PROJ["yearly"]
    prefix = "../"
    A_rows, B_rows = [], []
    for r in base["A"]:
        if r["year"] > 2050:
            continue
        post = "live_annual_cost" in r
        src = srcs_cell(["S11", "S04", "S06"], prefix, ["FL-01", "FL-02", "FL-15"])
        A_rows.append([
            str(r["year"]), money(r["fcv"]), money(r["av_no_transfer"]), money(r["tax_no_transfer"]),
            money(r["av_live_after_transfer"]) if post else "—",
            money(r["tax_live"]) if post else "—",
            money(r["water"]) if post else "—",
            money(r["electricity"]) if post else "—",
            money(r["insurance"]) if post else "—",
            money(r["maintenance"]) if post else "—",
            money(r["live_annual_cost"]) if post else "—",
            src,
        ])
    for r in base["B"]:
        if r["year"] > 2050:
            continue
        post = "av_hybrid" in r
        src = srcs_cell(["S11", "S06", "S15"], prefix, ["FL-01", "FL-03", "FL-16", "FL-17"])
        B_rows.append([
            str(r["year"]), money(r["fcv"]), money(r["av_no_transfer"]), money(r["tax_no_transfer"]),
            money(r["av_hybrid"]) if post else "—",
            money(r["tax_hybrid"]) if post else "—",
            money(r["rent"]) if post else "—",
            money(r["hybrid_net_cash"]) if post else "—",
            money(r["av_full"]) if post else "—",
            money(r["tax_full"]) if post else "—",
            money(r["full_net_cash"]) if post else "—",
            src,
        ])
    return A_rows, B_rows


def page_projections():
    prefix = "../"
    scen = PROJ["scenarios"]
    srows = []
    for k in ["low", "base", "high"]:
        s = scen[k]
        srows.append([esc(s["label"]), pct(s["inflation"], 1), pct(s["appreciation"], 1), pct(s["investment_return"], 1),
                      pct(s["rent_growth_sf"], 1), '<span class="badge mute">ASSUMPTION</span>', srcs_cell(["S17", "S18"], prefix, ["FL-15"])])
    A_rows, B_rows = yearly_tables()
    arows = [[esc(x) for x in r[:-1]] + [r[-1]] for r in A_rows]
    brows = [[esc(x) for x in r[:-1]] + [r[-1]] for r in B_rows]
    # highlight the base year rows for the decision year
    A_head = ["Year", "Market value", "Assessed (no transfer)", "Tax (no transfer)", f"Assessed after {BT} (live)",
              "Tax live", "Water", "Electricity (net)", "Insurance", "Upkeep", "Live annual cash cost", "Source"]
    B_head = ["Year", "Market value", "Assessed (no transfer)", "Tax (no transfer)", f"Assessed after {BT} (1 unit lived in)",
              "Tax (hybrid)", "Rent (2 units)", "Net cash (hybrid)", "Assessed (no occupancy)", "Tax (no occupancy)",
              "Net cash (no occupancy)", "Source"]
    def sens_src(label):
        if "Prop 19 limit" in label:
            return srcs_cell(["S04"], prefix, ["FL-18"])
        if "electricity" in label:
            return srcs_cell(["S28"], prefix, ["FL-05"])
        if "1% levy" in label or "2.13%" in label:
            return srcs_cell(["S24"], prefix, ["FL-03"])
        if "rent grows" in label or "BEST" in label and "rent" in label:
            return srcs_cell(["S15"], prefix, ["FL-16"])
        if "BEST CASE" in label:
            return srcs_cell(["S15"], prefix, ["FL-15", "FL-03"])
        return srcs_cell(["S25"], prefix, ["FL-13", "FL-15"])
    sens_rows = [[esc(s["label"]), money(s["end_real_2026"]), sens_src(s["label"])] for s in PROJ["sensitivities"]]
    body = f"""
<section class="panel"><p class="eyebrow">Projections</p><h1>Assumptions, scenarios and year-by-year results</h1>
<p class="muted">Client inputs are used as given and are unverified. Growth rates are labeled assumptions. Three stress cases move inflation, appreciation and returns together; they are not probabilities. Projections run 2026–2050 in the table; the decision compares every option at a common end date of {PROJ['meta']['horizon_end']}.</p>
</section>
<section class="panel"><h2>Scenarios</h2>
{table(["Case", "Inflation", "Home appreciation", "Investment return (nominal)", "SF rent growth", "Status", "Source"], srows)}
<p class="muted">Inflation anchors: CPI-U was 3.7% for the 12 months ending Sept 2026 ({src_link('S17', prefix)}); the Fed's longer-run goal is 2% ({src_link('S18', prefix)}). Prop 13 growth is capped at 2% per year ({src_link('S11', prefix)}).</p>
</section>
<section class="panel"><h2>Sensitivities (base case, inheritance in {BT}, real 2026 $ at {PROJ['meta']['horizon_end']})</h2>
{table(["Sensitivity", "End value (real 2026 $)", "Source"], sens_rows)}
</section>
<section class="panel"><h2>Property A · Cupertino, year by year (base case, inheritance in {BT})</h2>
{table(A_head, arows)}
<p class="muted">Live case after transfer: assessed value = min(full cash value, base-year value + max(0, FCV − base-year value − limit)), then 2% per year. Homeowners' exemption reduces tax by $7,000 × rate. Upkeep = {pct(INPUTS['properties']['A']['maintenance_pct_of_value']['value'],1)} of value (assumption).</p>
</section>
<section class="panel"><h2>Property B · San Francisco, year by year (base case, inheritance in {BT})</h2>
{table(B_head, brows)}
<p class="muted">Hybrid: one unit occupied (one-third of value under Prop 19 limit rules), two rented units reassessed at two-thirds of value. No occupancy: whole property reassessed. Rent starts at the client figure and grows at {pct(scen['base']['rent_growth_sf'],1)} (1.6% cap; assumption beyond 2026-27). Net cash is after property tax, costs, and income tax on rent.</p>
</section>
"""
    return page("Projections", 1, "Projections", body, desc="Inflation, appreciation, and tax-law projections for two properties, 2026–2050, with sensitivities.")


def page_decision():
    prefix = "../"
    rows = []
    for T in PROJ["meta"]["inheritance_years_tested"]:
        for sk in ["low", "base", "high"]:
            a_live = summary("A", T, sk, "Live")["end_real_2026"]
            a_sell = summary("A", T, sk, "Sell")["end_real_2026"]
            b_h = summary("B", T, sk, "Heir lives")["end_real_2026"]
            b_f = summary("B", T, sk, "No occupancy")["end_real_2026"]
            b_s = summary("B", T, sk, "Sell")["end_real_2026"]
            rb = be_rent(T, sk)
            rows.append([
                str(T), PROJ["scenarios"][sk]["label"],
                f"{money(a_live)} vs {money(a_sell)}", "Sell",
                f"{money(rb['monthly_rent_2026_dollars'])} / mo (2026 $)",
                f"{money(b_h)} / {money(b_f)} vs {money(b_s)}", "Sell",
                srcs_cell(["S06", "S25"], prefix, ["FL-15", "FL-17"]),
            ])
    best_rows = [[esc(r[0]), esc(r[1]), esc(r[2]), esc(r[3]), esc(r[4]), esc(r[5]), esc(r[6]), r[7]] for r in rows]
    econ = ECON
    rec = f"""
<section class="panel hero-small">
  <p class="eyebrow">Recommendation</p>
  <h2>Sell both properties promptly after inheritance, unless the checks below change the answer</h2>
  <ol class="reasons">
    <li><b>Wealth comes out ahead in every case tested.</b> In all three inheritance years and all three stress cases, selling and investing the net proceeds beat living in Property A and keeping either property in Property B (table above). This holds at the base-case end date of {PROJ['meta']['horizon_end']}.</li>
    <li><b>Property A has little net yield once carrying costs are counted.</b> In {econ['year']} (base), cash costs are about {money(econ['cash_costs_nominal'])} per year, while the after-tax return forgone on about {money(A_PROCEEDS)} of sale proceeds is about {money(econ['forgone_after_tax_return_on_sale_proceeds'])}. Expected appreciation offsets about {money(econ['expected_appreciation'])}, leaving a net annual economic cost of about {money(econ['net_annual_economic_cost'])}. Living value is not counted; compare it with a market rent for a comparable home.</li>
    <li><b>Property A rent only works above break-even.</b> To rent instead of sell, rent must reach about {money(BE['monthly_rent_2026_dollars'])} per month in 2026 dollars (base case, {BT}; about {money(BE['monthly_rent_at_T_nominal'])} per month in {BT} dollars). Verified market rent data were not available, so this is a threshold to test, not a result.</li>
    <li><b>Property B keeps the rent but loses to selling.</b> Keeping the two rented units and having the heir live in one (Prop 19) is worth about {money(PROP19_B_VALUE)} in real terms compared with no occupancy. Even the best case for keeping (1% levy only, 0.5% upkeep, rent growing with inflation) reaches about {money(B_BEST_KEEP)}, against {money(B_SELL)} for selling.</li>
    <li><b>Sale right after inheritance should carry little capital-gain tax.</b> Inherited property generally takes a basis equal to its value at death (IRC 1014). Confirm the rule with Publication 551 (see <a href="../flagged/#FL-07">FL-07</a>).</li>
    <li><b>Selling reduces exposure to law changes and to unverified inputs.</b> It removes annual rent-cap and Prop 19 indexing risk, the unresolved SF tax-rate question (<a href="../flagged/#FL-03">FL-03</a>), the unverified solar and insurance figures, and the risk of a future change to Prop 19 (the 2026 repeal initiative failed, but rules can change again).</li>
  </ol>
  <h3>Checks that would change the answer (verify before acting)</h3>
  <ul>
    <li>Property A: if an heir wants to live there, complete the Prop 19 steps (occupy within one year; BOE-266; BOE-19-P) and compare the net annual cost with comparable market rent (<a href="../flagged/#FL-01">FL-01</a>).</li>
    <li>Property B: keep only if the SF bill shows the 2.13% rate is mostly a 1% levy, upkeep is well below 1%, rents track the cap, and the occupied unit is confirmed as qualifying (<a href="../flagged/#FL-03">FL-03</a>, <a href="../flagged/#FL-16">FL-16</a>, <a href="../flagged/#FL-17">FL-17</a>).</li>
    <li>Replace client figures with appraisals, 12 months of bills, and written insurance quotes, then re-run <code>scripts/model.py</code>.</li>
  </ul>
</section>
"""
    body = f"""
<section class="panel"><p class="eyebrow">Decision analysis</p><h1>Live, rent, or sell</h1>
<p class="muted">Each option is valued as end wealth at {PROJ['meta']['horizon_end']}, in real 2026 dollars. The sell option invests the net proceeds at an after-tax return; the keep options include net cash flows and the property value at the end date. Property A's rent option is shown as a break-even rent, because no verified rent is available.</p>
</section>
<section class="panel"><h2>Results by inheritance year and stress case</h2>
{table(["Inheritance year", "Stress case", "A · Live vs sell (end value)", "A · Best", "A · Break-even rent (rent option)", "B · Hybrid / no-occupancy vs sell", "B · Best", "Source"], best_rows)}
<p class="muted">A "Best" column reads "Sell" in every row. Ranking uses real end value at {PROJ['meta']['horizon_end']}. Rents are quoted per month in 2026 dollars.</p>
</section>
{rec}
"""
    return page("Decision", 1, "Decision", body, desc="Live, rent, or sell decision for two properties, with break-even rent and recommendation.")


def page_process():
    prefix = "../"
    steps = [
        ["1", "Trust becomes irrevocable at the settlor's death: trustee sends notice to beneficiaries and heirs.", "Within 60 days of the event (Probate Code 16061.7).", ["S26"], []],
        ["2", "Identify and inventory trust assets; secure both properties; check that insurance matches the actual use (occupied or rented).", "Immediately after death.", [], ["FL-04"]],
        ["3", "Obtain date-of-death appraisals for each property (basis and estate values).", "As of death date; keep records for the sale and for Form 8971.", ["S30"], ["FL-01", "FL-07"]],
        ["4", "Decide whether the estate must file Form 706 (gross estate plus adjusted taxable gifts above $15M in 2026). If it does, report property values to beneficiaries on Form 8971.", "Form 706 filing date is not stated here; check the IRS instructions (not verified in this build).", ["S01", "S02", "S22"], ["FL-20"]],
        ["5", "If a child will live in a property, make it their principal residence and file for the Prop 19 exclusion.", "Move in within 1 year; BOE-266 within 1 year; BOE-19-P within 3 years or before a third-party transfer.", ["S03", "S05", "S06"], ["FL-17"]],
        ["6", "Transfer title from the trust directly to the qualifying beneficiary. Do not use an LLC.", "Trust is looked through; LLC disqualifies.", ["S06"], []],
        ["7", "Watch the property-tax calendar: Santa Clara 2026-27 first installment by Dec 10, 2026 (postmark counts); SF dates need confirmation.", "Santa Clara verified; SF unverified.", ["S12"], ["FL-09", "FL-10"]],
        ["8", "Trust files its income tax return and reports net investment income; check the NIIT rules for trusts.", "Form 1041; NIIT 3.8% above the trust threshold.", ["S23"], ["FL-19"]],
        ["9", "If selling: confirm the county transfer tax and any city tax at closing; check basis documentation.", "County tax $1.10 per $1,000; city tax unverified.", ["S25"], ["FL-13"]],
        ["10", "If renting an SF unit: confirm rent-control coverage and use the current allowable increase.", "1.6% (March 1, 2026 to Feb 28, 2027).", ["S15", "S27"], ["FL-16"]],
        ["11", "Re-check federal and state law before each filing; review pending measures.", "Recheck at each step.", ["S07", "S08", "S19"], ["FL-14", "FL-23"]],
    ]
    rows = [[esc(a), esc(b), esc(c), srcs_cell(d, prefix, e)] for a, b, c, d, e in steps]
    body = f"""
<section class="panel"><p class="eyebrow">Inheritance process</p><h1>Step-by-step through the trust</h1>
<p class="muted">Order matters: notices and appraisals come first, and the Prop 19 filing clock starts at the transfer. Dates are as stated in the cited sources. This is a checklist, not legal advice; the trust's attorney and tax preparer must confirm each step.</p></section>
<section class="panel">{table(["Step", "Action", "Timing or rule", "Source / flags"], rows)}</section>
"""
    return page("Process", 1, "Process", body, desc="Step-by-step trust administration and Prop 19 filing sequence with sources.")


def page_law():
    prefix = "../"
    items = [
        ["Prop 19 (parent-child exclusion) in effect; $1,044,586 limit for 2/16/2025 to 2/15/2027", "In effect", "Adjusted every two years; next adjustment Feb 2027", ["S04", "S03"], ["FL-18"]],
        ["Prop 19 repeal initiative (25-0017)", "Failed to qualify", "May 18, 2026 memo", ["S07"], []],
        ["SB 974: special needs trusts eligible for the Prop 19 transfer", "Chaptered; effective Jan 1, 2027", "Effective 1/1/2027", ["S08"], []],
        ["Federal estate and gift exclusion $15,000,000 (2026)", "In effect", "Indexed for inflation from 2027 under current law", ["S01", "S02"], ["FL-20"]],
        ["Death Tax Repeal Act of 2025 (S.587; H.R.1301)", "Introduced; referred to committee; not enacted", "Feb 13, 2025 (latest snapshot)", ["S19", "S19b"], ["FL-23"]],
        ["Assessment inflation factor (Prop 13)", "In effect (1.02 for 2026-27)", "Annual; 2% cap on growth absent ownership change", ["S11"], []],
        ["SF allowable rent increase", "1.6% (March 1, 2026 to Feb 28, 2027)", "Set annually by the Rent Board", ["S15"], ["FL-16"]],
        ["Statewide rent cap (AB 1482 / Civ. Code 1947.12)", "In effect", "5% + CPI, max 10% per 12 months", ["S27"], []],
        ["CPUC residential fixed charge (Base Services Charge)", "In effect (about $24.15 standard)", "Applies to residential bills (CPUC document; roll-out dates not verified)", ["S28"], ["FL-05"]],
        ["SFPUC water and sewer increases", "Proposed FY27 and FY28; adoption reported (secondary)", "July 1, 2026 and July 1, 2027", ["S29"], ["FL-12"]],
        ["Prop 40 (billionaire tax), early returns", "Not certified; early returns only", "Nov 3, 2026 (secondary)", ["S37"], ["FL-14"]],
        ["California Mental Health Services Tax (1% over $1M)", "Unverified on an official page", "—", ["S24"], ["FL-08"]],
    ]
    rows = [[esc(a), esc(b), esc(c), srcs_cell(d, prefix, e)] for a, b, c, d, e in items]
    body = f"""
<section class="panel"><p class="eyebrow">Law and pending changes</p><h1>What could change the answer</h1>
<p class="muted">Enacted, pending and failed measures with their status as of this build. Any item marked flagged should be checked before relying on it.</p></section>
<section class="panel">{table(["Measure", "Status", "Timing", "Source / flags"], rows)}</section>
<section class="panel"><h2>How to use this page</h2>
<ul>
<li>Prop 19 is the largest swing factor for Property A if it is occupied. Track the February 2027 limit adjustment.</li>
<li>Estate-tax thresholds are high enough that the two properties alone do not trigger federal estate tax on current law; other estate assets could.</li>
<li>California has no state estate or inheritance tax under current law (R&amp;TC 13301).</li>
</ul></section>
"""
    return page("Law", 1, "Law", body, desc="Enacted, pending and failed federal and state changes relevant to inherited California property.")


def page_flagged():
    prefix = "../"
    sev_rank = {"high": 0, "medium": 1, "low": 2}
    rows = []
    for f in sorted(FLAGS, key=lambda x: (sev_rank[x["severity"]], x["id"])):
        sev = f'<span class="badge {"warn" if f["severity"]=="high" else "mute"}">{f["severity"].upper()}</span>'
        rows.append([
            f'<a id="{esc(f["id"])}"></a><code>{esc(f["id"])}</code>', sev, esc(f["topic"]), esc(f["title"]),
            esc(f["detail"]), esc(f["action"]), srcs_cell(f["sources"], prefix),
        ])
    counts = {k: sum(1 for f in FLAGS if f["severity"] == k) for k in ["high", "medium", "low"]}
    body = f"""
<section class="panel review"><p class="eyebrow">Flagged for review</p><h1>Irregularities, unverified values and open questions</h1>
<p class="muted">Flags do not block publication. Each entry says what is unverified or irregular, what the workspace shows, and what would resolve it. Totals: {counts['high']} high, {counts['medium']} medium, {counts['low']} low.</p>
</section>
<section class="panel"><div class="filterbar"><input type="search" placeholder="Filter flags (e.g. FL-03, insurance, SF)" aria-label="Filter flags"></div>
{table(["ID", "Severity", "Topic", "Issue", "Detail", "Action to resolve", "Source"], rows)}</section>
"""
    return page("Flagged for review", 1, "Flagged", body, desc="Irregularities, unverified values, and open items for review, with source links.")


def page_sources():
    prefix = "../"
    rows = []
    for s in SOURCES.values():
        tag = '<span class="badge ok">OFFICIAL</span>' if s["tier"] == "official" else '<span class="badge warn">SECONDARY</span>'
        rows.append([f'<code>{esc(s["id"])}</code>', tag, esc(s["publisher"]), esc(s["title"]),
                     f'<a href="{esc(s["url"])}" target="_blank" rel="noopener">{esc(s["url"])}</a>', esc(s["retrieval"])])
    body = f"""
<section class="panel"><p class="eyebrow">Sources</p><h1>Source register</h1>
<p class="muted">Official sources are used for verified values. Secondary sources were used only to locate items for review and are never the sole basis of a verified value. Accessed {BUILD_DATE}.</p></section>
<section class="panel"><div class="filterbar"><input type="search" placeholder="Filter sources" aria-label="Filter sources"></div>
{table(["ID", "Tier", "Publisher", "Title", "Link", "How checked"], rows)}</section>
"""
    return page("Sources", 1, "Sources", body, desc="Register of official and secondary sources with retrieval status.")


CSS = """
:root{--ink:#17202a;--muted:#5b6774;--line:#dfe5ec;--bg:#f6f8fa;--card:#fff;--brand:#0f5c8c;--ok:#1f7a4d;--warn:#a25b00;--client:#1d5fa6;--mute:#6c7782}
*{box-sizing:border-box}body{margin:0;font:15px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:var(--ink);background:var(--bg)}
a{color:var(--brand)}code{font-size:.9em;background:#eef2f6;padding:0 .25em;border-radius:3px}
.top{display:flex;justify-content:space-between;align-items:center;padding:14px 24px;background:#0f2a3d;color:#fff;flex-wrap:wrap;gap:8px}
.brand{display:flex;gap:12px;align-items:center}.mark{display:inline-grid;place-items:center;width:38px;height:38px;border-radius:8px;background:#2b8bc4;font-weight:700}
.brand small{display:block;color:#b8cbd9;font-size:12px}.asof{color:#b8cbd9;font-size:13px}
.nav{display:flex;gap:4px;flex-wrap:wrap;padding:8px 16px;background:#fff;border-bottom:1px solid var(--line);position:sticky;top:0;z-index:5}
.nav a{padding:6px 10px;border-radius:6px;text-decoration:none;color:var(--ink);font-size:14px}.nav a:hover{background:#eef4f9}.nav a.active{background:var(--brand);color:#fff}
main{max-width:1200px;margin:0 auto;padding:18px 16px}
.panel{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:18px 20px;margin:0 0 16px}
.panel h2{margin:0 0 10px;font-size:19px}.panel h1{margin:4px 0 8px;font-size:26px}
.hero{background:linear-gradient(135deg,#0f2a3d,#1e5a80);color:#fff;border-radius:12px;padding:26px 26px;margin-bottom:16px}
.hero h1{font-size:30px;margin:6px 0 10px;max-width:900px}.hero .lede{max-width:860px;color:#dde8f1;font-size:16px}
.eyebrow{text-transform:uppercase;letter-spacing:.08em;font-size:12px;color:var(--muted);margin:0 0 4px}.hero .eyebrow{color:#a9c6da}
.cta{margin-top:14px;display:flex;gap:10px;flex-wrap:wrap}.btn{background:#fff;color:var(--brand);padding:9px 14px;border-radius:7px;font-weight:600;text-decoration:none}
.btn.ghost{background:transparent;color:#fff;border:1px solid #cfe0ec}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin-bottom:16px}
.stats article{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px}
.stats small{color:var(--muted);display:block}.stats strong{font-size:22px;display:block;margin:4px 0}
.src-line{font-size:12px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px}
.card{display:block;background:#fbfdfe;border:1px solid var(--line);border-radius:10px;padding:14px;text-decoration:none;color:var(--ink)}
.card b{display:block;margin-bottom:4px;color:var(--brand)}.card span{color:var(--muted);font-size:14px}.card.warn{border-color:#f0c48a;background:#fffaf2}
.tablewrap{overflow-x:auto;border:1px solid var(--line);border-radius:8px;margin:8px 0}
table{width:100%;border-collapse:collapse;font-size:13.5px}th,td{padding:8px 10px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
th{background:#f1f5f9;position:sticky;top:0;font-weight:600;color:#334}tr:nth-child(even) td{background:#fbfcfd}tr:hover td{background:#f0f7fc}
td a.src{white-space:nowrap}.sid{font-size:11px;background:#eef2f6;border-radius:3px;padding:0 3px;color:#345}
a.src.secondary{color:#8a5a00}a.flagref{background:#fff1dc;color:#7a4300;padding:0 4px;border-radius:3px;text-decoration:none;font-size:12px}
.badge{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.04em;padding:2px 7px;border-radius:999px;white-space:nowrap}
.badge.ok{background:#e4f5ec;color:var(--ok)}.badge.warn{background:#fff1dc;color:var(--warn)}.badge.client{background:#e6f0fb;color:var(--client)}.badge.mute{background:#eef1f4;color:var(--mute)}
.muted{color:var(--muted);font-size:14px}
.filterbar{margin:4px 0 8px}.filterbar input{width:100%;max-width:420px;padding:8px 10px;border:1px solid #c9d3dd;border-radius:7px;font:inherit}
.hero-small{border-color:#9cc3dc;background:#f7fbfe}
.reasons li{margin-bottom:8px}
footer{max-width:1200px;margin:24px auto;padding:0 16px 30px;color:var(--muted);font-size:12.5px}
@media (max-width:700px){.hero h1{font-size:24px}.panel h1{font-size:22px}}
"""

JS = """// Progressive enhancement: live text filter for tables and search boxes.
(function(){
  function norm(s){return (s||'').toString().toLowerCase();}
  function applyFilter(input){
    var q=norm(input.value);
    var scope=input.closest('section')||document;
    var tables=scope.querySelectorAll('table');
    tables.forEach(function(t){
      t.querySelectorAll('tbody tr').forEach(function(tr){
        tr.style.display = !q || norm(tr.textContent).indexOf(q)>-1 ? '' : 'none';
      });
    });
  }
  document.querySelectorAll('.filterbar input[type=search]').forEach(function(inp){
    inp.addEventListener('input', function(){applyFilter(inp);});
  });
})();
"""


def main():
    write(ROOT / "index.html", page_overview())
    write(ROOT / "facts/index.html", page_facts())
    write(ROOT / "property/index.html", page_property())
    write(ROOT / "costs/index.html", page_costs())
    write(ROOT / "projections/index.html", page_projections())
    write(ROOT / "decision/index.html", page_decision())
    write(ROOT / "process/index.html", page_process())
    write(ROOT / "law/index.html", page_law())
    write(ROOT / "flagged/index.html", page_flagged())
    write(ROOT / "sources/index.html", page_sources())
    write(ROOT / "assets/site.css", CSS)
    write(ROOT / "assets/site.js", JS)
    print("site written")


if __name__ == "__main__":
    main()
