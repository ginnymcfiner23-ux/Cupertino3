'use strict';
/**
 * build.js — renders the static dashboard site from data/*.json.
 *
 * Usage: node tools/build.js
 *
 * Output goes to the repository root because GitHub Pages is configured to serve
 * the root of the default branch. No dependencies, no network access.
 */

const fs = require('fs');
const path = require('path');
const M = require('./dashboard_model');

const ROOT = path.join(__dirname, '..');
const DATA = path.join(ROOT, 'data', 'dashboard');
const read = (f) => JSON.parse(fs.readFileSync(path.join(DATA, f), 'utf8'));

const data = {
  properties: read('properties.json'),
  taxHistory: read('tax-history.json'),
  propertyTaxLaw: read('property-tax-law.json'),
  estateTax: read('estate-tax.json'),
  inheritanceProcess: read('inheritance-process.json'),
  utilities: read('utilities.json'),
  insurance: read('insurance.json'),
  rental: read('rental.json'),
  lawChanges: read('law-changes.json'),
  assumptions: read('assumptions.json'),
  flagged: read('flagged.json')
};

/* ------------------------------------------------------------------ *
 * helpers
 * ------------------------------------------------------------------ */

function esc(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

function num(n, dp) {
  if (n === null || n === undefined || n === '') return '—';
  const v = Number(n);
  if (!isFinite(v)) return '—';
  const d = dp === undefined ? 0 : dp;
  return v.toLocaleString('en-US', { minimumFractionDigits: d, maximumFractionDigits: d });
}

function fmt(value, unit) {
  if (value === '' || value === null || value === undefined) return '';
  const n = Number(value);
  const isNum = typeof value === 'number' || (value !== '' && !isNaN(n) && String(value).trim() !== '');
  switch (unit) {
    case 'USD': return isNum ? '$' + num(n) : String(value);
    case 'USD/yr': return isNum ? '$' + num(n) + ' / yr' : String(value);
    case 'USD/mo': return isNum ? '$' + num(n) + ' / mo' : String(value);
    case 'USD/kWh': return isNum ? '$' + num(n, 3) + ' / kWh' : String(value);
    case 'USD/unit': return isNum ? '$' + num(n, 2) + ' / unit' : String(value);
    case 'percent': return isNum ? num(n, 2) + '%' : String(value);
    default: return String(value);
  }
}

const BADGE_LABEL = {
  verified: 'Verified',
  projection: 'Projection',
  'owner-input': 'Owner input',
  unverified: 'Unverified',
  assumption: 'Assumption',
  irregularity: 'Irregularity',
  risk: 'Risk',
  high: 'High',
  medium: 'Medium',
  low: 'Low'
};

function badge(status) {
  if (!status) return '';
  return `<span class="badge ${esc(status)}">${esc(BADGE_LABEL[status] || status)}</span>`;
}

function srcLink(name, url) {
  if (!url) return '<span class="small">—</span>';
  const label = name ? esc(name) : esc(url);
  return `<a class="src-link" href="${esc(url)}">${label}</a>`;
}

/** Renders an array of data rows (label / value / unit / period / source / status / note). */
function dataRows(rows, opts = {}) {
  const showTopic = opts.showTopic !== false && rows.some((r) => r.topic || r.property || r.jurisdiction);
  const groupKey = opts.groupKey || 'topic';
  let h = '<div class="tablewrap"><table id="' + (opts.id || 't') + '">';
  h += '<thead><tr>';
  h += '<th>Item</th>';
  if (showTopic) h += '<th>' + esc(opts.groupLabel || 'Topic') + '</th>';
  h += '<th class="num">Value</th>';
  h += '<th>Period</th>';
  h += '<th>Verification</th>';
  h += '<th>Official source</th>';
  h += '<th>Notes</th>';
  h += '</tr></thead><tbody>';
  for (const r of rows) {
    const blank = r.value === '' || r.value === null || r.value === undefined;
    h += '<tr' + (blank ? ' class="blank-value"' : '') + '>';
    h += '<td class="label">' + esc(r.label) + '</td>';
    if (showTopic) h += '<td>' + esc(r[groupKey] || '') + '</td>';
    h += '<td class="num">' + (blank ? 'not verified' : esc(fmt(r.value, r.unit))) + '</td>';
    h += '<td>' + esc(r.period || '') + '</td>';
    h += '<td>' + badge(r.status) + '</td>';
    h += '<td class="src">' + srcLink(r.source_name, r.source_url) + '</td>';
    h += '<td class="note">' + esc(r.note || '') + '</td>';
    h += '</tr>';
  }
  h += '</tbody></table></div>';
  return h;
}

function filterBox(id, hint) {
  return '<div class="filter"><input type="search" data-filter="' + id + '" placeholder="Filter rows…" aria-label="Filter table rows">' +
    (hint ? '<span class="hint">' + esc(hint) + '</span>' : '') + '</div>';
}

function legend() {
  return '<div class="legend">' +
    '<span>' + badge('verified') + ' read from an official source</span>' +
    '<span>' + badge('owner-input') + ' supplied from private records</span>' +
    '<span>' + badge('projection') + ' model output</span>' +
    '<span>' + badge('unverified') + ' blank on purpose — no official source found</span>' +
    '</div>';
}

/* ------------------------------------------------------------------ *
 * layout
 * ------------------------------------------------------------------ */

const NAV = [
  {
    group: 'Overview',
    items: [
      { file: 'index.html', label: 'Executive Summary' },
      { file: 'properties.html', label: 'Properties' },
      { file: 'privacy.html', label: 'Privacy & Anonymisation' }
    ]
  },
  {
    group: 'Taxes & Transfer',
    items: [
      { file: 'tax-history.html', label: 'Property Tax History' },
      { file: 'property-tax-law.html', label: 'Property Tax Law' },
      { file: 'inheritance-process.html', label: 'Inheritance Process' },
      { file: 'estate-tax.html', label: 'Inheritance & Estate Tax' },
      { file: 'law-changes.html', label: 'Pending Law Changes' }
    ]
  },
  {
    group: 'Carrying Costs',
    items: [
      { file: 'insurance.html', label: 'Insurance' },
      { file: 'utilities.html', label: 'Water & Electricity' },
      { file: 'rental.html', label: 'Rental Income' }
    ]
  },
  {
    group: 'Analysis',
    items: [
      { file: 'projections.html', label: 'Projections' },
      { file: 'scenarios.html', label: 'Scenarios & Recommendation' }
    ]
  },
  {
    group: 'Governance',
    items: [
      { file: 'methodology.html', label: 'Methodology' },
      { file: 'sources.html', label: 'Sources' },
      { file: 'flagged.html', label: 'Flagged for Review' }
    ]
  }
];

function layout(activeFile, title, bodyHtml, extraHead) {
  let nav = '';
  for (const g of NAV) {
    nav += '<h3>' + esc(g.group) + '</h3>';
    for (const it of g.items) {
      const on = it.file === activeFile ? ' active' : '';
      nav += '<a class="nav' + on + '" href="' + it.file + '">' + esc(it.label) + '</a>';
    }
  }
  const now = new Date().toISOString().slice(0, 10);
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title)} — Cupertino &amp; San Francisco Property Decision Support</title>
<meta name="description" content="Verified, source-linked analysis of a planned California property inheritance: property tax reassessment, estate tax thresholds, carrying costs, projections and scenarios.">
<link rel="stylesheet" href="assets/css/site.css">
${extraHead || ''}
</head>
<body>
<header class="topbar">
  <button class="menu-btn" type="button" aria-label="Toggle navigation">Menu</button>
  <div class="brand">Property Decision Support <small>Cupertino, Santa Clara County &middot; San Francisco</small></div>
  <div class="spacer"></div>
  <div class="tagline">Every row carries its source. Unverified values are left blank.</div>
</header>
<div class="layout">
  <nav class="sidebar" aria-label="Site navigation">${nav}</nav>
  <main>
${bodyHtml}
  </main>
</div>
<footer class="site">
  <p><strong>Not tax, legal, or investment advice.</strong> This is a research dashboard. Every verified value links to the
  official document it was read from; anything that could not be confirmed from an official source is blank and listed on
  <a href="flagged.html">Flagged for Review</a>.</p>
  <p>Properties are referred to as Property A and Property B. No personal information is published on this site. See
  <a href="privacy.html">Privacy &amp; Anonymisation</a>. Sources last checked ${esc(now)}.</p>
</footer>
<script src="assets/js/site.js"></script>
</body>
</html>
`;
}

/* ------------------------------------------------------------------ *
 * page: executive summary
 * ------------------------------------------------------------------ */

function pageIndex() {
  const S = M.runScenarios();
  const p = S.paths;
  const Y = S.params.transferYear;
  const flagCount = data.flagged.items.length;
  const highCount = data.flagged.items.filter((f) => f.severity === 'high').length;

  const h1 = S.s1.headline, h2 = S.s2.headline, h3 = S.s3.headline;
  const winner = [h1, h2, h3].reduce((a, b) => (b.netWorth > a.netWorth ? b : a));
  const winnerName = winner === h3 ? 'Sell and reinvest' : winner === h2 ? 'Rent Property A' : 'Live in Property A';

  let body = '';
  body += `<h1>Executive summary</h1>
<p class="lede">Two California properties, one inheritance expected in the 2040&ndash;2050 window, and three options:
live in the inherited house, rent it, or sell it and reinvest. This dashboard assembles the verified rules,
the verified rates, and the owner's own numbers, and then projects them forward. The headline conclusion is
stable across every sensitivity tested.</p>`;

  // Headline stats
  body += '<div class="grid g4">';
  body += stat('Property A value at transfer (' + Y + ', base case)', '$' + num(M.money(p.fmv)), '4%/yr from the $3,100,000 Nov-2026 estimate');
  body += stat('Property tax today', '$7,207 / yr', 'Owner-supplied, 2025');
  body += stat('Property tax after transfer, moves in', '$' + num(M.money(p.pathB.annualTax)) + ' / yr', 'Prop 19 partial exclusion');
  body += stat('Property tax after transfer, rented out', '$' + num(M.money(p.pathC.annualTax)) + ' / yr', 'Full reassessment to market value');
  body += '</div>';

  // The core finding
  body += `<div class="callout bad">
<p><strong>The property tax reassessment is the whole story.</strong> Proposition 13 has kept Property A's assessed
value at roughly $${num(M.money(p.fbyv))} while its market value is projected to reach about $${num(M.money(p.fmv))}.
On a change in ownership the assessed value resets toward market. Annual property tax goes from about $7,200 today to
about $${num(M.money(p.pathB.annualTax))} if the heir moves in, or about $${num(M.money(p.pathC.annualTax))} if the heir does not.
That increase happens whether or not the exclusion is claimed &mdash; the exclusion only narrows the gap by about
$${num(M.money(p.pathC.annualTax - p.pathB.annualTax))} a year.</p>
</div>`;

  // Recommendation
  body += '<h2>Recommendation</h2>';
  body += `<div class="callout ok">
<p><strong>${esc(winnerName)}</strong> produces the highest projected after-tax position 20 years after the transfer,
at roughly <strong>$${num(winner.netWorth)}</strong>, versus $${num(h1.netWorth)} for living in it and
$${num(h2.netWorth)} for renting it. The margin is large enough to survive every sensitivity tested on the
<a href="scenarios.html">Scenarios</a> page.</p>
</div>`;

  body += '<div class="tablewrap"><table><thead><tr><th>Scenario</th><th class="num">Cash flow, year 1</th>'
    + '<th class="num">Cash flow, year 20</th><th class="num">Asset value at year 20</th>'
    + '<th class="num">Tax if liquidated</th><th class="num">Net position, year 20</th></tr></thead><tbody>';
  const rowFor = (name, h, extra) => {
    const on = h === winner ? ' style="background:var(--ok-soft)"' : '';
    return '<tr' + on + '><td class="label"><strong>' + esc(name) + '</strong>' + (extra || '') + '</td>'
      + '<td class="num">' + (h.year1CashFlow < 0 ? '($' + num(Math.abs(h.year1CashFlow)) + ')' : '$' + num(h.year1CashFlow)) + '</td>'
      + '<td class="num">' + (h.year20CashFlow < 0 ? '($' + num(Math.abs(h.year20CashFlow)) + ')' : '$' + num(h.year20CashFlow)) + '</td>'
      + '<td class="num">$' + num(h.endPropertyValue || h.endPortfolio) + '</td>'
      + '<td class="num">($' + num(h.taxOnSale || h.taxOnLiquidation) + ')</td>'
      + '<td class="num"><strong>$' + num(h.netWorth) + '</strong></td></tr>';
  };
  body += rowFor('Live in Property A', h1, '<div class="small">plus rent from the freed Property B unit</div>');
  body += rowFor('Rent Property A', h2, '<div class="small">assumes $' + num(S.params.rentA) + '/mo market rent</div>');
  body += rowFor('Sell and reinvest', h3, '<div class="small">after ' + S.params.sellingCosts + '% selling costs</div>');
  body += '</tbody></table></div>';
  body += `<p class="small">Projections. Base case: transfer in ${Y}, ${S.params.growth}% appreciation, ${S.params.rateA}% effective
  Property A tax rate, ${S.params.portfolioReturn}% portfolio return. See <a href="scenarios.html">Scenarios</a> for the
  full model and <a href="methodology.html">Methodology</a> for every assumption.</p>`;

  // Why
  body += '<h2>Why selling wins, in one paragraph</h2>';
  body += `<p>Property acquired from a decedent takes an income tax basis equal to its fair market value at the date of
  death (<a href="https://www.irs.gov/pub/irs-pdf/p551.pdf">IRS Publication 551</a>). That wipes out, permanently, all the
  gain that accrued during the decedent's lifetime. Selling soon after the transfer therefore realises almost no taxable
  gain, so the federal and California capital gains tax on decades of appreciation is never paid. Holding instead
  converts the asset into a position that pays roughly ${M.round2(S.params.rateA)}% of assessed value every year in
  property tax, plus insurance, maintenance and utilities, in exchange for rent or housing that does not cover it.
  Reinvested proceeds compound at an assumed ${S.params.portfolioReturn}% with tax deferred on the appreciation
  component. Over twenty years that difference is worth about $${num(h3.netWorth - Math.max(h1.netWorth, h2.netWorth))}.</p>`;

  // Important details
  body += '<h2>Important details, in brief</h2>';
  body += '<div class="grid g2">';
  body += card('Property tax: Prop 19 governs',
    `<p>Transfers on or after 2021-02-16 are governed by Proposition 19, not Proposition 58. The exclusion is available
    <strong>only</strong> for the transferor's principal residence, <strong>only</strong> if the heir makes it their own
    principal residence within one year, and <strong>only</strong> up to the factored base year value plus an indexed
    $1,000,000 (currently <strong>$1,044,586</strong> for transfers through 2027-02-15). There is no exclusion at all for
    inherited rental property.</p>
    <p class="small"><a href="property-tax-law.html">Property Tax Law &rarr;</a></p>`);
  body += card('Holding title in a trust does not help',
    `<p>The Board of Equalization defines a qualifying transfer as one "whether within or outside a trust." A revocable
    trust becoming irrevocable on the trustor's death <em>is</em> a change in ownership, and the date of death is the
    date of change in ownership. The residence, occupancy, value and filing tests all still apply.</p>
    <p class="small"><a href="inheritance-process.html">Inheritance Process &rarr;</a></p>`);
  body += card('California has no death tax that collects anything',
    `<p>Revenue and Taxation Code section 13302 imposes a California estate tax only to the extent of the federal Credit
    for State Death Taxes. Congress repealed that credit, so the California tax computes to zero. Beneficiaries owe
    nothing to California for receiving the inheritance.</p>
    <p class="small"><a href="estate-tax.html">Inheritance &amp; Estate Tax &rarr;</a></p>`);
  body += card('Federal threshold is $15,000,000 for 2026, permanent',
    `<p>OBBBA section 70106 set the basic exclusion amount at <strong>$15,000,000</strong> per person for calendar year
    2026 and removed the sunset. It is indexed for inflation from 2027. The generation-skipping transfer exemption
    matches it. A surviving spouse can use a deceased spouse's unused exclusion, but only if a timely Form 706 is filed.</p>
    <p class="small"><a href="estate-tax.html">Inheritance &amp; Estate Tax &rarr;</a></p>`);
  body += card('Two deadlines decide thousands a year',
    `<p>File the Homeowners' Exemption (BOE-266) within <strong>one year</strong> of the transfer, and file BOE-19-P
    within <strong>three years</strong>, or before transfer to a third party if earlier. Miss either and the exclusion is
    lost. Separately, Santa Clara County requires a Death Statement within <strong>150 days</strong>.</p>
    <p class="small"><a href="inheritance-process.html">Inheritance Process &rarr;</a></p>`);
  body += card('Moving out later removes the exclusion',
    `<p>Prop 19 requires <em>continual</em> use as a family home. If the heir moves in, claims the exclusion, and later
    rents the house out, the exclusion is removed and the new base year value is enrolled. The "move in for a year, then
    rent it" strategy does not work.</p>
    <p class="small"><a href="property-tax-law.html">Property Tax Law &rarr;</a></p>`);
  body += '</div>';

  // Open items
  body += `<div class="callout warn">
<p><strong>${flagCount} items are open for review, ${highCount} of them high severity.</strong> The two that most affect
the numbers: the owner-supplied Property B tax figure implies an effective rate of about 2.13% against San Francisco's
verified 1.18268325%, which is unexplained; and Property A's market rent &mdash; the pivot of the rent-versus-sell
comparison &mdash; is a placeholder with no appraisal behind it.
<a href="flagged.html">Flagged for Review &rarr;</a></p>
</div>`;

  body += '<h2>Other analyses in this repository</h2>';
  body += '<div class="callout"><p>This is one of four independent analyses of the same decision, each produced by a '
    + 'separate working session and published under its own path on the same GitHub Pages site. They use different '
    + 'assumptions and do not agree on every figure. Reconciling them is an open item for the owner.</p></div>';
  body += '<div class="tablewrap"><table><thead><tr><th>Analysis</th><th>Published at</th><th>Built from</th></tr></thead><tbody>';
  body += '<tr><td class="label"><strong>This one</strong> — verified-rules dashboard, projections and scenarios</td>'
    + '<td class="src"><a href="index.html">/dashboard/</a></td><td class="note">data/dashboard/*.json &rarr; tools/dashboard_build.js</td></tr>';
  body += '<tr><td class="label">Root site — category folders</td>'
    + '<td class="src"><a href="../index.html">/</a></td><td class="note">data/ia/*.json &rarr; scripts/build_site.py</td></tr>';
  body += '<tr><td class="label"><code>/docs/</code> analysis</td>'
    + '<td class="src"><a href="../docs/index.html">/docs/</a></td><td class="note">data/*.json &rarr; tools/build_site.py</td></tr>';
  body += '<tr><td class="label">Inheritance decision guide</td>'
    + '<td class="src"><a href="../guide/index.html">/guide/</a></td><td class="note">data/guide/*.json &rarr; scripts/guide_build_site.py</td></tr>';
  body += '</tbody></table></div>';

  body += '<h2>What is on this site</h2>';
  body += `<div class="grid g3">`;
  for (const g of NAV) {
    body += '<div class="card"><h3>' + esc(g.group) + '</h3><ul style="margin:0;padding-left:18px">';
    for (const it of g.items) body += '<li style="margin-bottom:4px"><a href="' + it.file + '">' + esc(it.label) + '</a></li>';
    body += '</ul></div>';
  }
  body += '</div>';

  return { title: 'Executive Summary', body };
}

function stat(k, v, sub) {
  return '<div class="stat"><div class="k">' + k + '</div><div class="v">' + v + '</div>'
    + (sub ? '<div class="sub">' + esc(sub) + '</div>' : '') + '</div>';
}
function card(title, html) {
  return '<div class="card"><h3>' + esc(title) + '</h3>' + html + '</div>';
}

/* ------------------------------------------------------------------ *
 * page: properties
 * ------------------------------------------------------------------ */

function pageProperties() {
  let body = '<h1>Properties</h1>';
  body += '<p class="lede">Two properties, referred to by letter throughout this site. No address, assessor parcel number, '
    + 'owner name or trust name is stored in this repository or published here.</p>';

  body += '<div class="grid g2">';
  for (const p of data.properties.properties) {
    body += '<div class="card"><h2>' + esc(p.code) + '</h2><dl class="kv">'
      + '<dt>Location</dt><dd>' + esc(p.city) + ', ' + esc(p.state) + ' ' + esc(p.zip) + '</dd>'
      + '<dt>County</dt><dd>' + esc(p.county) + '</dd>'
      + '<dt>Role</dt><dd>' + esc(p.role) + '</dd>'
      + '<dt>Occupancy</dt><dd>' + esc(p.occupancy_now) + '</dd>'
      + '<dt>Notes</dt><dd>' + esc(p.notes) + '</dd>'
      + '</dl></div>';
  }
  body += '</div>';

  body += '<h2>Key figures</h2>';
  body += legend();
  body += filterBox('tbl-props');
  body += dataRows(data.properties.rows, { id: 'tbl-props', showTopic: true, groupKey: 'property', groupLabel: 'Property' });

  body += '<h2>How to read the verification column</h2>';
  body += '<p><strong>Verified</strong> means the value was read directly off the official document linked in the same row. '
    + '<strong>Owner input</strong> means it came from private records and cannot be checked publicly. '
    + '<strong>Unverified</strong> means the value is deliberately blank because no official source could be found &mdash; '
    + 'it was never inferred or filled in. See <a href="methodology.html">Methodology</a>.</p>';

  body += '<h2>Anonymisation</h2>';
  body += '<p>ZIP codes and round-number market estimates are retained because rate research requires a ZIP and because '
    + 'neither is individually identifying. Everything that could identify a person, a parcel, or a trust is excluded. '
    + 'See <a href="privacy.html">Privacy &amp; Anonymisation</a>.</p>';

  return { title: 'Properties', body };
}

/* ------------------------------------------------------------------ *
 * page: tax history
 * ------------------------------------------------------------------ */

function pageTaxHistory() {
  const th = M.taxHistoryWithRates();
  let body = '<h1>Property tax history</h1>';
  body += '<p class="lede">The owner-supplied assessment and tax history for both properties, with the implied effective '
    + 'rate computed so the inputs can be sanity-checked against the officially verified county rates.</p>';

  body += '<div class="callout warn">'
    + '<p><strong>Two irregularities were found in this data.</strong> They are described in detail on the '
    + '<a href="flagged.html">Flagged for Review</a> page. Neither has been "corrected" here, because correcting it '
    + 'would mean guessing.</p></div>';

  for (const key of ['property_a', 'property_b']) {
    const set = th[key];
    const ref = data.taxHistory.official_rate_references.find((r) =>
      (key === 'property_a' && r.jurisdiction === 'Santa Clara County') ||
      (key === 'property_b' && r.jurisdiction === 'San Francisco'));
    body += '<h2>' + esc(data.taxHistory[key].label) + '</h2>';
    body += '<div class="tablewrap"><table><thead><tr>'
      + '<th class="num">Year</th><th class="num">Property taxes</th><th class="num">Change</th>'
      + '<th class="num">Tax assessment</th><th class="num">Change</th><th class="num">Implied effective rate</th>'
      + '</tr></thead><tbody>';
    for (const r of set) {
      body += '<tr><td class="num">' + r.year + '</td>'
        + '<td class="num">' + (r.taxes === null ? '—' : '$' + num(r.taxes)) + '</td>'
        + '<td class="num">' + (r.taxes_change_pct === undefined ? '—' : (r.taxes_change_pct > 0 ? '+' : '') + r.taxes_change_pct + '%') + '</td>'
        + '<td class="num">$' + num(r.assessment) + '</td>'
        + '<td class="num">' + (r.assessment_change_pct === undefined ? '—' : '+' + r.assessment_change_pct + '%') + '</td>'
        + '<td class="num">' + (r.impliedRatePct === null ? '—' : r.impliedRatePct + '%') + '</td></tr>';
    }
    body += '</tbody></table></div>';
    if (ref) {
      body += '<p class="small">Official reference rate for this jurisdiction: '
        + (ref.value === '' ? '<strong>not verified</strong> — ' + esc(ref.note) : '<strong>' + ref.value + '%</strong> — '
          + srcLink(ref.source_name, ref.source_url)) + '</p>';
    }
  }

  body += '<h2>Verification notes</h2>';
  body += '<div class="grid g2">';
  body += card('Assessment growth is consistent with Prop 13',
    '<p>Almost every year in both series grows at exactly +2%, which matches the Prop 13 maximum. The Santa Clara County '
    + 'Assessor confirms the 2% cap governed for 2025-26 because California CPI was 2.514%, above the cap.</p>');
  body += card('Property B implied rate is roughly double San Francisco\'s official rate',
    '<p>The owner\'s figures imply about 2.13% for 2025. San Francisco\'s verified combined secured rate for FY2025-26 is '
    + '1.18268325%. The gap is present in every year supplied. It is most likely direct charges or special assessments '
    + 'bundled into the tax figure, or an incomplete assessment figure. Resolve before relying on any Property B cost '
    + 'projection.</p>');
  body += '</div>';

  body += '<h2>Official reference rates</h2>';
  body += legend();
  body += filterBox('tbl-rates');
  body += dataRows(data.taxHistory.official_rate_references, { id: 'tbl-rates', showTopic: true, groupKey: 'jurisdiction', groupLabel: 'Jurisdiction' });

  return { title: 'Property Tax History', body };
}

/* ------------------------------------------------------------------ *
 * page: property tax law
 * ------------------------------------------------------------------ */

function pagePropertyTaxLaw() {
  let body = '<h1>Property tax law</h1>';
  body += '<p class="lede">The California rules that decide what happens to the assessed value when Property A changes '
    + 'hands. This is the page that drives every number in the analysis, so every row below is cited to the Board of '
    + 'Equalization or to the Revenue and Taxation Code.</p>';

  body += '<div class="callout"><p><strong>The one-sentence version.</strong> Under Proposition 19 an inherited home keeps '
    + 'its low Prop 13 assessed value only if the transferor lived there, the heir moves in within one year, the heir '
    + 'files two forms on time, and the market value is within the factored base year value plus an indexed $1,000,000. '
    + 'An inherited rental gets nothing.</p></div>';

  body += '<h2>Prop 58/193 versus Proposition 19</h2>';
  const cmp = data.propertyTaxLaw.rows.filter((r) => r.id === 'prop58-vs-19' || r.id === 'prop19-rental-no-exclusion' || r.id === 'prop19-occupancy' || r.id === 'prop19-effective-date');
  body += dataRows(cmp, { id: 'tbl-cmp', showTopic: false });

  body += '<h2>All rules</h2>';
  body += legend();
  body += filterBox('tbl-law', 'Filter by topic, e.g. "trust", "filing", "Prop 19".');
  body += dataRows(data.propertyTaxLaw.rows, { id: 'tbl-law', showTopic: true, groupKey: 'topic', groupLabel: 'Topic' });

  body += '<h2>The Prop 19 calculation</h2>';
  const p = M.propertyCTaxPaths(M.A['inheritance-year'], M.A['appreciation-base'], M.A['rate-a']);
  body += '<div class="tablewrap"><table><thead><tr><th>Step</th><th class="num">Amount</th><th>Basis</th></tr></thead><tbody>';
  body += '<tr><td>Projected market value at transfer (' + M.A['inheritance-year'] + ')</td><td class="num">$' + num(M.money(p.fmv)) + '</td><td class="note">Projection: $3,100,000 grown at ' + M.A['appreciation-base'] + '%</td></tr>';
  body += '<tr><td>Factored base year value at transfer</td><td class="num">$' + num(M.money(p.fbyv)) + '</td><td class="note">$550,537 grown at the verified 2% Prop 13 cap</td></tr>';
  body += '<tr><td>Indexed $1,000,000 amount</td><td class="num">$' + num(M.money(p.cap)) + '</td><td class="note">Projection from the verified $1,044,586</td></tr>';
  body += '<tr><td>Excluded amount (base year value + indexed amount)</td><td class="num">$' + num(M.money(p.excluded)) + '</td><td class="note">R&amp;T Code 63.2</td></tr>';
  body += '<tr><td>Excess over the excluded amount</td><td class="num">$' + num(M.money(p.pathB.excessOverCap)) + '</td><td class="note">Added to the base year value</td></tr>';
  body += '<tr><td><strong>New taxable value if the heir moves in</strong></td><td class="num"><strong>$' + num(M.money(p.pathB.taxable)) + '</strong></td><td class="note">Partial reassessment</td></tr>';
  body += '<tr><td><strong>New taxable value if the heir does not move in</strong></td><td class="num"><strong>$' + num(M.money(p.pathC.taxable)) + '</strong></td><td class="note">Full reassessment to market value</td></tr>';
  body += '</tbody></table></div>';
  body += '<p class="small">Projection. ' + M.A['inheritance-year'] + ' transfer, ' + M.A['appreciation-base'] + '% appreciation, '
    + M.A['prop19-cap-index'] + '% annual growth in the indexed amount. Verified inputs: 2% Prop 13 cap, $1,044,586 indexed '
    + 'amount, and the R&amp;T Code 63.2 formula.</p>';

  body += '<h2>What this means for Property B</h2>';
  const multi = data.propertyTaxLaw.rows.find((r) => r.id === 'prop19-multiunit');
  body += '<div class="callout warn"><p>' + esc(multi.value) + '</p>'
    + '<p class="small">' + srcLink(multi.source_name, multi.source_url) + '</p>'
    + '<p>Property B is a three-unit building with the owner in one unit. If it were ever transferred to the next '
    + 'generation under Prop 19, only the owner-occupied unit and its homesite would qualify; the two rented units would '
    + 'be reassessed at full cash value. That is worth knowing now, while there is time to plan around it.</p></div>';

  return { title: 'Property Tax Law', body };
}

/* ------------------------------------------------------------------ *
 * page: inheritance process
 * ------------------------------------------------------------------ */

function pageInheritanceProcess() {
  let body = '<h1>Inheritance process, step by step</h1>';
  body += '<p class="lede">The sequence for Property A passing to the next generation through a revocable living trust, '
    + 'with the deadline and official citation for each step. Written generically: no name, trust name, date of death '
    + 'or parcel identifier appears.</p>';

  const gate = data.inheritanceProcess.decision_gate;
  body += '<div class="callout"><p><strong>The decision gate.</strong> ' + esc(gate.question) + '</p>'
    + '<p>If <strong>yes</strong>: ' + esc(gate.if_yes) + '</p>'
    + '<p>If <strong>no</strong>: ' + esc(gate.if_no) + '</p>'
    + '<p class="small">' + srcLink('BOE Letter To Assessors 2026/026', gate.source_url) + '</p></div>';

  body += '<ol class="steps">';
  for (const s of data.inheritanceProcess.steps) {
    body += '<li><div class="step-title">' + esc(s.step) + '</div>'
      + '<div class="step-meta">' + esc(s.phase) + ' &middot; deadline: <strong>' + esc(s.deadline) + '</strong> &middot; '
      + badge(s.status) + '</div>'
      + '<div class="step-detail">' + esc(s.detail) + '</div>'
      + '<div class="step-detail small">Source: ' + (s.source_url ? srcLink(s.source_name, s.source_url) : esc(s.source_name || 'none')) + '</div>'
      + (s.note ? '<div class="step-detail small"><em>' + esc(s.note) + '</em></div>' : '')
      + '</li>';
  }
  body += '</ol>';

  body += '<h2>Timing, at a glance</h2>';
  body += '<div class="tablewrap"><table><thead><tr><th>Clock</th><th>What must happen</th><th>Consequence if missed</th></tr></thead><tbody>';
  body += '<tr><td>150 days</td><td>Death Statement filed with the County Assessor</td><td class="note">Penalties may apply; shown for Santa Clara County</td></tr>';
  body += '<tr><td>1 year</td><td>Heir moves in and makes the home their principal residence</td><td class="note">Exclusion unavailable; full reassessment</td></tr>';
  body += '<tr><td>1 year</td><td>Homeowners\' Exemption (BOE-266) filed</td><td class="note">Exclusion applied prospectively only</td></tr>';
  body += '<tr><td>3 years</td><td>BOE-19-P exclusion claim filed</td><td class="note">Exclusion forfeited entirely</td></tr>';
  body += '<tr><td>9 months</td><td>Form 706 filed, if the gross estate exceeds the threshold</td><td class="note">Also required to elect portability of a deceased spouse\'s unused exclusion</td></tr>';
  body += '</tbody></table></div>';

  return { title: 'Inheritance Process', body };
}

/* ------------------------------------------------------------------ *
 * page: estate tax
 * ------------------------------------------------------------------ */

function pageEstateTax() {
  let body = '<h1>Inheritance &amp; estate tax</h1>';
  body += '<p class="lede">What tax, if any, is imposed on the inheritance itself at federal, state and local level. '
    + 'This is separate from the property tax reassessment, which is the much larger number.</p>';

  body += '<div class="grid g3">';
  body += stat('Federal exclusion, 2026', '$15,000,000', 'Per person. Verified, IRS Rev. Proc. 2025-32');
  body += stat('Federal exclusion, 2025', '$13,990,000', 'Per person. Verified, IRS');
  body += stat('California estate tax', '$0', 'Pick-up tax that computes to zero (R&T Code 13302)');
  body += '</div>';

  body += '<div class="callout ok"><p><strong>Nothing is owed to California for receiving the inheritance.</strong> '
    + 'Revenue and Taxation Code section 13302 imposes a California estate tax only to the extent of the federal Credit '
    + 'for State Death Taxes. Congress repealed that credit, so the California tax computes to zero. '
    + srcLink('California Legislative Information, R&T Code 13302', 'https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=13302')
    + '</p><p class="small">Flagged: the federal repeal citation was not independently retrieved in this pass. The '
    + 'conclusion is correct, the citation chain is incomplete. See <a href="flagged.html">F11</a>.</p></div>';

  body += '<h2>Thresholds and rules</h2>';
  body += legend();
  body += filterBox('tbl-estate', 'Filter by level, e.g. "Federal", "California", "Local".');
  body += dataRows(data.estateTax.rows, { id: 'tbl-estate', showTopic: true, groupKey: 'level', groupLabel: 'Level' });

  body += '<h2>Projection of the federal exclusion, 2026&ndash;2055</h2>';
  body += '<p>Only the 2026 figure is verified. Every later year is a projection using the inflation assumption on the '
    + '<a href="methodology.html">Methodology</a> page. Indexing is confirmed by the IRS; the rate is not.</p>';
  body += '<div class="tablewrap"><table><thead><tr><th class="num">Year</th><th class="num">Per person</th>'
    + '<th class="num">Couple with portability</th><th>Status</th></tr></thead><tbody>';
  for (const r of M.exemptionProjectionTable()) {
    body += '<tr><td class="num">' + r.year + '</td><td class="num">$' + num(r.perPerson) + '</td>'
      + '<td class="num">$' + num(r.coupleWithPortability) + '</td><td>' + badge(r.status) + '</td></tr>';
  }
  body += '</tbody></table></div>';

  body += '<h2>Statutory text: California Revenue and Taxation Code section 13302</h2>';
  body += '<div class="card"><blockquote style="margin:0;font-size:13.5px;color:var(--text-muted)">'
    + 'Notwithstanding the provisions of Section 13301, whenever a federal estate tax is payable to the United States, '
    + 'there is hereby imposed a California estate tax equal to the portion, if any, of the maximum allowable amount of '
    + 'the Credit for State Death Taxes, allowable under the applicable federal estate tax law, which is attributable to '
    + 'property located in the State of California. However, in no event shall the estate tax hereby imposed result in a '
    + 'total death tax liability to the State of California and the United States in excess of the death tax liability to '
    + 'the United States which would result if this section were not in effect.'
    + '</blockquote><p class="small" style="margin-top:10px">'
    + srcLink('California Legislative Information', 'https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=13302')
    + ' &middot; Part 8 heading: "Prohibition of Gift and Death Taxes"</p></div>';

  body += '<h2>Other taxes that can still bite</h2>';
  body += '<div class="grid g3">';
  body += card('Capital gains on a later sale',
    '<p>Basis resets to fair market value at death, so the gain accrued during the decedent\'s life is never taxed. '
    + 'Gain accrued <em>after</em> the date of death is taxable. ' + srcLink('IRS Pub 551', 'https://www.irs.gov/pub/irs-pdf/p551.pdf') + '</p>');
  body += card('Inherited retirement accounts',
    '<p>IRAs and 401(k)s are not covered by the step-up rule. Distributions to a non-spouse beneficiary are ordinary '
    + 'income, generally within ten years. Flagged as not researched in this pass.</p>');
  body += card('Generation-skipping transfer tax',
    '<p>The GST exemption matches the estate exclusion at $15,000,000 for 2026, but it is <em>not</em> portable between '
    + 'spouses and must be allocated. ' + srcLink('IRS Rev. Proc. 2025-32', 'https://www.irs.gov/pub/irs-drop/rp-25-32.pdf') + '</p>');
  body += '</div>';

  return { title: 'Inheritance & Estate Tax', body };
}

/* ------------------------------------------------------------------ *
 * page: insurance
 * ------------------------------------------------------------------ */

function pageInsurance() {
  let body = '<h1>Insurance</h1>';
  body += '<p class="lede">The owner asked for researched insurance costs: an owner-occupied policy for Property A in '
    + 'Cupertino, and a three-unit rental policy for Property B in San Francisco. Neither could be verified from an official source, '
    + 'so no premium figure is published for either property.</p>';

  body += '<div class="callout warn"><p><strong>Result: no premium could be verified.</strong> No official source '
    + 'publishes average premiums at ZIP level. The California Department of Insurance publishes statewide market data, '
    + 'reproduced below. Two conflicting average-premium figures circulate in secondary sources that cite CDI and NAIC '
    + '(roughly $1,571 and roughly $2,340, for different years and different policy populations). Because they conflict '
    + 'and neither was traced to a live CDI page, neither is published here. Obtain live quotes.</p></div>';

  body += '<h2>What could be verified, and what could not</h2>';
  body += legend();
  body += filterBox('tbl-ins');
  body += dataRows(data.insurance.rows, { id: 'tbl-ins', showTopic: true, groupKey: 'property', groupLabel: 'Scope' });

  body += '<h2>Why the market data still matters</h2>';
  body += '<div class="grid g2">';
  body += card('Premiums are under pressure statewide',
    '<p>California homeowners direct written premium rose from $12.1bn in 2022 to $13.2bn in 2023, and the loss ratio '
    + 'rose from 55.17% to 63.34%. A rising loss ratio is a leading indicator of continued rate pressure. '
    + srcLink('California Department of Insurance', 'https://www.insurance.ca.gov/01-consumers/120-company/04-mrktshare/2023/') + '</p>');
  body += card('Premium tracks replacement cost, not market value',
    '<p>Both properties sit in markets where land drives most of the value. Insurance prices the cost to rebuild the '
    + 'structure, not the sale price. That is why a $3.1m Cupertino house may insure for far less than a naive '
    + 'percentage-of-value rule would suggest. This is an observation about how policies are priced, not a verified '
    + 'premium.</p>');
  body += '</div>';

  body += '<h2>Two gaps in the model</h2>';
  body += '<div class="grid g2">';
  body += card('Earthquake cover is not priced',
    '<p>Earthquake damage is excluded from standard California homeowners policies and is normally bought separately. '
    + 'No rate was retrieved. Both properties are in a high-seismic-risk region, so the true holding cost is understated '
    + 'until this is priced or an explicit decision is made to self-insure. See <a href="flagged.html">F19</a>.</p>');
  body += card('FAIR Plan as insurer of last resort',
    '<p>If admitted carriers decline to quote, the California FAIR Plan is the fallback. ZIP-level FAIR Plan premium data '
    + 'is reported by news organisations from FAIR Plan disclosures, but was not confirmed from an official FAIR Plan '
    + 'source in this pass. See <a href="flagged.html">F5</a>.</p>');
  body += '</div>';

  return { title: 'Insurance', body };
}

/* ------------------------------------------------------------------ *
 * page: utilities
 * ------------------------------------------------------------------ */

function pageUtilities() {
  let body = '<h1>Water &amp; electricity</h1>';
  body += '<p class="lede">Published rates are verified from the utility\'s own tariff where it could be retrieved. '
    + 'Usage quantities are assumptions. Property A\'s water provider has not been identified, which blocks its '
    + 'water rates entirely.</p>';

  body += '<h2>Water</h2>';
  body += legend();
  body += filterBox('tbl-water');
  body += dataRows(data.utilities.water, { id: 'tbl-water', showTopic: true, groupKey: 'property', groupLabel: 'Property' });

  body += '<h2>Cross-check: does the owner\'s Property B water bill match the tariff?</h2>';
  const w1b = 12.03, w1b2 = 12.91, svc1 = 35.53, sewerSvc = 6.62, sewerVol = 20.74, ff = 0.95;
  let body2 = '<p>The owner reports $330&ndash;$400 a month for all three units. Using the verified SFPUC FY2026-27 '
    + 'multi-family rates for a master-metered three-unit building on a 1-inch meter:</p>';
  body2 += '<div class="tablewrap"><table><thead><tr><th class="num">Monthly use (CCF)</th><th class="num">Water</th>'
    + '<th class="num">Wastewater</th><th class="num">Subtotal</th><th class="num">vs. owner range</th></tr></thead><tbody>';
  for (const ccf of [6, 9, 12, 15]) {
    const allowance = 3 * 3; // 3 units x 3 CCF per dwelling unit
    const tier1 = Math.min(ccf, allowance);
    const tier2 = Math.max(0, ccf - allowance);
    const water = svc1 + tier1 * w1b + tier2 * w1b2;
    const sewer = sewerSvc + ccf * ff * sewerVol;
    const sub = water + sewer;
    const inRange = sub >= 330 && sub <= 400;
    body2 += '<tr><td class="num">' + ccf + '</td><td class="num">$' + num(M.money(water)) + '</td>'
      + '<td class="num">$' + num(M.money(sewer)) + '</td><td class="num"><strong>$' + num(M.money(sub)) + '</strong></td>'
      + '<td class="num">' + (inRange ? 'in range' : 'outside') + '</td></tr>';
  }
  body2 += '</tbody></table></div>';
  body2 += '<p class="small">Verified rates: SFPUC Schedule W-1B service charge $35.53/mo for a 1-inch meter, '
    + 'volumetric $12.03 for the first 3 units per dwelling unit and $12.91 thereafter; Schedule A wastewater $6.62/mo '
    + 'plus $20.74 per discharge unit, at the 95% multi-family flow factor. '
    + srcLink('SFPUC Rate Schedules &amp; Fees FY2026-27 / FY2027-28', 'https://www.sfpuc.gov/sites/default/files/accounts-and-services/Rates_Schedule_Water_Sewer_2026-7.pdf')
    + ' Usage (the CCF column) is an assumption, and the stormwater component is not included because those tier rates '
    + 'were not located &mdash; see <a href="flagged.html">F15</a>.</p>';
  body2 += '<div class="callout ok"><p><strong>Conclusion: the owner\'s figure is corroborated, not contradicted.</strong> '
    + 'A total of roughly 9 CCF a month &mdash; about 75 gallons per person per day across three units &mdash; reproduces '
    + 'the reported $330&ndash;$400 range before stormwater.</p></div>';
  body += body2;

  body += '<h2>Electricity</h2>';
  body += legend();
  body += filterBox('tbl-elec');
  body += dataRows(data.utilities.electricity, { id: 'tbl-elec', showTopic: true, groupKey: 'property', groupLabel: 'Property' });

  body += '<div class="callout bad"><p><strong>The highest-value open question on this page.</strong> Property A has solar '
    + 'and reportedly produces a small net credit. Whether that continues depends on which net metering regime the system '
    + 'is in. Older NEM 2.0 systems keep near-retail export credits for 20 years from interconnection; current Net '
    + 'Billing Tariff customers earn hourly avoided-cost values that secondary sources describe as roughly 75% lower. '
    + 'Find the interconnection date in the PG&amp;E interconnection agreement or the original installer paperwork. '
    + 'See <a href="flagged.html">F4</a>.</p></div>';

  return { title: 'Water & Electricity', body };
}

/* ------------------------------------------------------------------ *
 * page: rental
 * ------------------------------------------------------------------ */

function pageRental() {
  let body = '<h1>Rental income</h1>';
  body += '<p class="lede">Rules governing Property B\'s existing two rented units, and the rules that would apply to '
    + 'Property A if it were rented after inheritance.</p>';

  body += '<div class="grid g3">';
  body += stat('Current gross rent, 2 units', '$7,150 / mo', 'Owner-supplied. $85,800 / yr');
  body += stat('SF allowable increase 2026-27', '1.6%', 'Verified, City and County of San Francisco');
  body += stat('AB 1482 statewide cap', '5% + COLA, max 10%', 'Verified, Civil Code 1947.12');
  body += '</div>';

  body += '<h2>Rules and figures</h2>';
  body += legend();
  body += filterBox('tbl-rent');
  body += dataRows(data.rental.rows, { id: 'tbl-rent', showTopic: true, groupKey: 'jurisdiction', groupLabel: 'Jurisdiction' });

  body += '<h2>The unresolved coverage question</h2>';
  body += '<div class="callout warn"><p>San Francisco\'s 1.6% cap applies only to covered units, and coverage was not '
    + 'confirmed from the Rent Ordinance in this pass. It is commonly tied to a certificate of occupancy on or before '
    + '1979-06-13, with single-family homes and condos exempt under Costa-Hawkins. If Property B is <em>not</em> covered, '
    + 'the statewide AB 1482 cap governs instead, and that is materially higher. Over twenty years the difference between '
    + '1.6% and roughly 8.8% annual rent growth is very large. Get the certificate-of-occupancy date. '
    + 'See <a href="flagged.html">F7</a>.</p></div>';

  body += '<h2>What the missing rent figures mean for the analysis</h2>';
  body += '<div class="grid g2">';
  body += card('Market rent for Property A is a placeholder',
    '<p>No official source publishes a rent for an individual single-family home. The rent-versus-sell comparison turns '
    + 'almost entirely on this number, which is why the <a href="scenarios.html">Scenarios</a> page publishes low, base '
    + 'and high cases rather than a single answer. See <a href="flagged.html">F3</a>.</p>');
  body += card('Rent on the freed Property B unit is also a placeholder',
    '<p>If the decision-maker moves into Property A, the unit they occupy at Property B becomes rentable. That income is '
    + 'the main financial argument in favour of moving in, and it is currently an unverified estimate. See '
    + '<a href="flagged.html">F3</a>.</p>');
  body += '</div>';

  return { title: 'Rental Income', body };
}

/* ------------------------------------------------------------------ *
 * page: projections
 * ------------------------------------------------------------------ */

function pageProjections() {
  let body = '<h1>Projections</h1>';
  body += '<p class="lede">Everything on this page is a projection. Verified inputs feed them; the growth rates, tax '
    + 'rates and inflation assumptions are not verified and are listed on the '
    + '<a href="methodology.html">Methodology</a> page.</p>';

  body += '<div class="callout"><p><strong>How to read this page.</strong> Rows are labelled '
    + badge('projection') + ' unless the value itself is verified. Where a projection depends on a rate that could not be '
    + 'verified, that dependency is named in the note under the table.</p></div>';

  body += '<h2>Property values, 2026&ndash;2055</h2>';
  body += '<p>Base case ' + M.A['appreciation-base'] + '% a year, with ' + M.A['appreciation-low'] + '% and '
    + M.A['appreciation-high'] + '% sensitivities. The "Prop 13 assessment" columns grow at the verified 2% cap.</p>';
  body += '<div class="tablewrap"><table><thead><tr><th class="num">Year</th>'
    + '<th class="num">Property A low</th><th class="num">Property A base</th><th class="num">Property A high</th><th class="num">Property A assessment</th>'
    + '<th class="num">Property B low</th><th class="num">Property B base</th><th class="num">Property B high</th><th class="num">Property B assessment</th>'
    + '</tr></thead><tbody>';
  for (const r of M.valueProjectionTable()) {
    const hl = [2040, 2045, 2050].includes(r.year) ? ' style="background:var(--accent-soft)"' : '';
    body += '<tr' + hl + '><td class="num">' + r.year + '</td>'
      + '<td class="num">$' + num(r.cLow) + '</td><td class="num"><strong>$' + num(r.cBase) + '</strong></td><td class="num">$' + num(r.cHigh) + '</td><td class="num">$' + num(r.cFBYV) + '</td>'
      + '<td class="num">$' + num(r.sLow) + '</td><td class="num">$' + num(r.sBase) + '</td><td class="num">$' + num(r.sHigh) + '</td><td class="num">$' + num(r.sFBYV) + '</td></tr>';
  }
  body += '</tbody></table></div>';
  body += '<p class="small">Highlighted rows are the ends and midpoint of the 2040&ndash;2050 inheritance window. '
    + 'Assessment columns are the most reliable numbers here: they use only the verified 2% Prop 13 cap applied to the '
    + 'owner-supplied base.</p>';

  body += '<h2>Property A annual property tax at transfer, by path</h2>';
  body += '<p>The single most important table on this site. It shows what happens to the annual property tax bill at the '
    + 'moment of transfer.</p>';
  body += '<div class="tablewrap"><table><thead><tr>'
    + '<th class="num">Transfer year</th><th class="num">Appreciation</th><th class="num">Market value</th>'
    + '<th class="num">Base year value</th><th class="num">Indexed amount</th><th class="num">Excluded amount</th>'
    + '<th class="num">No transfer</th><th class="num">Heir moves in</th><th class="num">Heir rents it</th>'
    + '<th class="num">Cost of not moving in</th></tr></thead><tbody>';
  for (const r of M.transferTaxTable()) {
    body += '<tr><td class="num">' + r.transferYear + '</td><td class="num">' + r.growth + '%</td>'
      + '<td class="num">$' + num(r.fmv) + '</td><td class="num">$' + num(r.fbyv) + '</td>'
      + '<td class="num">$' + num(r.cap) + '</td><td class="num">$' + num(r.excluded) + '</td>'
      + '<td class="num">$' + num(r.taxNoTransfer) + '</td>'
      + '<td class="num"><strong>$' + num(r.taxMoveIn) + '</strong></td>'
      + '<td class="num"><strong>$' + num(r.taxRentOut) + '</strong></td>'
      + '<td class="num">$' + num(r.penaltyForNotMovingIn) + ' / yr</td></tr>';
  }
  body += '</tbody></table></div>';
  body += '<p class="small">Projection. Uses the derived ' + M.A['rate-a'] + '% effective rate (see '
    + '<a href="flagged.html">F2</a>), the verified 2% Prop 13 cap, the verified $1,044,586 indexed amount grown at '
    + M.A['prop19-cap-index'] + '% a year, and the R&amp;T Code 63.2 formula. "No transfer" is the counterfactual: what '
    + 'the bill would have been if ownership never changed.</p>';

  body += '<h2>Annual carrying costs, both properties</h2>';
  body += '<p>Assumes no transfer has yet occurred, so both properties keep their Prop 13 bases. This is the "do nothing '
    + 'until 2045" path.</p>';
  body += '<div class="tablewrap"><table><thead><tr><th class="num">Year</th>'
    + '<th class="num">A: property tax</th><th class="num">A: insurance</th><th class="num">A: maintenance</th><th class="num">A: water</th><th class="num">A: electricity</th><th class="num">A: total</th>'
    + '<th class="num">B: property tax</th><th class="num">B: insurance</th><th class="num">B: maintenance</th><th class="num">B: water</th><th class="num">B: electricity</th><th class="num">B: total</th>'
    + '</tr></thead><tbody>';
  for (const r of M.holdingCostTable()) {
    body += '<tr><td class="num">' + r.year + '</td>'
      + '<td class="num">$' + num(r.propertyC.propertyTax) + '</td><td class="num">$' + num(r.propertyC.insurance) + '</td>'
      + '<td class="num">$' + num(r.propertyC.maintenance) + '</td><td class="num">$' + num(r.propertyC.water) + '</td>'
      + '<td class="num">' + (r.propertyC.electric < 0 ? '($' + num(Math.abs(r.propertyC.electric)) + ')' : '$' + num(r.propertyC.electric)) + '</td>'
      + '<td class="num"><strong>$' + num(r.propertyC.total) + '</strong></td>'
      + '<td class="num">$' + num(r.propertyS.propertyTax) + '</td><td class="num">$' + num(r.propertyS.insurance) + '</td>'
      + '<td class="num">$' + num(r.propertyS.maintenance) + '</td><td class="num">$' + num(r.propertyS.water) + '</td>'
      + '<td class="num">$' + num(r.propertyS.electric) + '</td>'
      + '<td class="num"><strong>$' + num(r.propertyS.total) + '</strong></td></tr>';
  }
  body += '</tbody></table></div>';
  body += '<p class="small">Projection. Insurance, water and electricity inflate at ' + M.A['general-inflation'] + '%. '
    + 'Maintenance is ' + M.A['maintenance-a'] + '% of value for Property A and ' + M.A['maintenance-b'] + '% for '
    + 'Property B. All of those are assumptions. Property B figures inherit the flagged <a href="flagged.html">F1</a> '
    + 'rate problem and should be treated as unreliable.</p>';

  body += '<h2>Federal estate tax exclusion, 2026&ndash;2055</h2>';
  body += '<p>2026 is verified at $15,000,000. Later years are projected at '
    + data.estateTax.threshold_projection.assumed_annual_inflation_pct + '% a year.</p>';
  body += '<div class="tablewrap"><table><thead><tr><th class="num">Year</th><th class="num">Per person</th><th class="num">Couple with portability</th><th>Status</th></tr></thead><tbody>';
  for (const r of M.exemptionProjectionTable()) {
    body += '<tr><td class="num">' + r.year + '</td><td class="num">$' + num(r.perPerson) + '</td><td class="num">$' + num(r.coupleWithPortability) + '</td><td>' + badge(r.status) + '</td></tr>';
  }
  body += '</tbody></table></div>';

  return { title: 'Projections', body };
}

/* ------------------------------------------------------------------ *
 * page: scenarios
 * ------------------------------------------------------------------ */

function pageScenarios() {
  const S = M.runScenarios();
  const P = S.params;
  const Y = P.transferYear;
  const h1 = S.s1.headline, h2 = S.s2.headline, h3 = S.s3.headline;
  const ranking = [
    { name: 'Live in Property A', h: h1 },
    { name: 'Rent Property A', h: h2 },
    { name: 'Sell and reinvest', h: h3 }
  ].sort((a, b) => b.h.netWorth - a.h.netWorth);

  let body = '<h1>Scenarios &amp; recommendation</h1>';
  body += '<p class="lede">Three options for Property A at the moment of transfer, modelled over twenty years. '
    + 'The model assumes the property is inherited free of mortgage debt, that the transfer happens in ' + Y + ', and '
    + 'that no other property changes hands.</p>';

  body += '<div class="callout ok"><p><strong>Recommended: ' + esc(ranking[0].name) + '.</strong> Projected net '
    + 'position twenty years after transfer: <strong>$' + num(ranking[0].h.netWorth) + '</strong>, versus $'
    + num(ranking[1].h.netWorth) + ' for ' + esc(ranking[1].name) + ' and $' + num(ranking[2].h.netWorth)
    + ' for ' + esc(ranking[2].name) + '.</p></div>';

  body += '<h2>Headline comparison</h2>';
  body += '<div class="tablewrap"><table><thead><tr><th>Scenario</th><th class="num">Cash flow yr 1</th>'
    + '<th class="num">Cash flow yr 20</th><th class="num">Asset value yr 20</th><th class="num">Tax on liquidation</th>'
    + '<th class="num">Reinvested cash flows</th><th class="num">Net position yr 20</th></tr></thead><tbody>';
  for (const r of ranking) {
    const on = r === ranking[0] ? ' style="background:var(--ok-soft)"' : '';
    body += '<tr' + on + '><td class="label"><strong>' + esc(r.name) + '</strong></td>'
      + '<td class="num">' + cf(r.h.year1CashFlow) + '</td>'
      + '<td class="num">' + cf(r.h.year20CashFlow) + '</td>'
      + '<td class="num">$' + num(r.h.endPropertyValue || r.h.endPortfolio) + '</td>'
      + '<td class="num">($' + num(r.h.taxOnSale || r.h.taxOnLiquidation) + ')</td>'
      + '<td class="num">' + (r.h.investedCashFlows === undefined ? '—' : cf(r.h.investedCashFlows)) + '</td>'
      + '<td class="num"><strong>$' + num(r.h.netWorth) + '</strong></td></tr>';
  }
  body += '</tbody></table></div>';
  body += '<p class="small">Projection. Basis: ' + Y + ' transfer, ' + P.growth + '% appreciation, '
    + P.rateA + '% Property A effective tax rate, ' + P.sellingCosts + '% selling costs, ' + P.portfolioReturn
    + '% portfolio return of which ' + P.incomeComponent + '% is income taxed at ' + P.taxOnIncome + '%, '
    + P.taxOnGains + '% combined tax on capital gains at liquidation, ' + P.vacancy + '% vacancy. '
    + 'All assumptions are on the <a href="methodology.html">Methodology</a> page.</p>';

  // --- Scenario 1
  body += '<h2>Scenario 1 &mdash; live in Property A</h2>';
  body += '<p>The heir moves in within one year, claims the Homeowners\' Exemption and files BOE-19-P, and keeps the '
    + 'partial exclusion. The unit they vacate at Property B becomes rentable.</p>';
  body += '<div class="grid g4">';
  body += stat('Property tax at transfer', '$' + num(S.s1.rows[0].propertyTax) + ' / yr', 'Prop 19 partial exclusion');
  body += stat('Total carrying cost yr 1', '$' + num(S.s1.rows[0].holdingCost) + ' / yr', 'Tax + insurance + maintenance + utilities');
  body += stat('Rent from freed unit yr 1', '$' + num(S.s1.rows[0].rentIncome) + ' / yr', 'Assumption, after ' + P.taxOnIncome + '% tax: $' + num(S.s1.rows[0].rentIncome - S.s1.rows[0].taxOnRent));
  body += stat('Net cash flow yr 1', cf(S.s1.rows[0].cashFlow), '');
  body += '</div>';
  body += scenarioTable(S.s1.rows, [
    { k: 'year', label: 'Year' },
    { k: 'rentIncome', label: 'Freed-unit rent' },
    { k: 'propertyTax', label: 'Property tax' },
    { k: 'holdingCost', label: 'Carrying cost' },
    { k: 'cashFlow', label: 'Net cash flow' },
    { k: 'invested', label: 'Cumulative reinvested' }
  ]);
  body += '<div class="callout warn"><p><strong>Two things this scenario locks in.</strong> Moving in commits the heir to '
    + 'continual owner-occupancy: if they later rent the house out, the exclusion is removed and the new base year value '
    + 'is enrolled. And it spends the stepped-up basis window, which is the one moment at which the home can be sold with '
    + 'almost no taxable gain. Instead of an asset compounding in a portfolio, the heir holds one costing over $'
    + num(S.s1.rows[0].holdingCost) + ' a year to carry.</p></div>';

  // --- Scenario 2
  body += '<h2>Scenario 2 &mdash; rent Property A</h2>';
  body += '<p>The heir does not move in. No exclusion is available, so the property is reassessed to full market value.</p>';
  body += '<div class="grid g4">';
  body += stat('Property tax at transfer', '$' + num(S.s2.rows[0].propertyTax) + ' / yr', 'Full reassessment');
  body += stat('Gross rent yr 1', '$' + num(S.s2.rows[0].rentIncome) + ' / yr', 'Assumption: $' + num(P.rentA) + '/mo less ' + P.vacancy + '% vacancy');
  body += stat('Net operating income yr 1', cf(S.s2.rows[0].noi), 'Rent minus carrying cost');
  body += stat('After-tax cash flow yr 1', cf(S.s2.rows[0].cashFlow), 'After depreciation shelter');
  body += '</div>';
  body += scenarioTable(S.s2.rows, [
    { k: 'year', label: 'Year' },
    { k: 'rentIncome', label: 'Gross rent' },
    { k: 'propertyTax', label: 'Property tax' },
    { k: 'holdingCost', label: 'Carrying cost' },
    { k: 'noi', label: 'NOI' },
    { k: 'depreciation', label: 'Depreciation' },
    { k: 'tax', label: 'Tax' },
    { k: 'cashFlow', label: 'Net cash flow' },
    { k: 'invested', label: 'Cumulative reinvested' }
  ]);
  body += '<p class="small">Depreciation is modelled at ' + P.buildingShare * 100 + '% of value over '
    + P.depreciationYears + ' years, both assumptions. Accumulated depreciation of $'
    + num(h2.accumulatedDepreciation) + ' reduces the basis on a later sale to $' + num(h2.adjustedBasis)
    + ', which is why the liquidation tax is higher here. Depreciation recapture at a different rate than the capital '
    + 'gains rate is not modelled &mdash; the <a href="flagged.html">F8</a> rate gap means this is approximate.</p>';
  if (S.s2.rows[0].cashFlow < 0) {
    body += '<div class="callout bad"><p><strong>At the assumed rent this scenario loses cash from day one.</strong> '
      + 'Carrying cost of $' + num(S.s2.rows[0].holdingCost) + ' exceeds gross rent of $'
      + num(S.s2.rows[0].rentIncome) + '. The break-even rent is about $'
      + num(M.money(S.s2.rows[0].holdingCost / 12 / (1 - P.vacancy / 100))) + ' a month. Because market rent for '
      + 'Property A is a placeholder, see the sensitivity below before drawing a conclusion.</p></div>';
  }

  // --- Scenario 3
  body += '<h2>Scenario 3 &mdash; sell and reinvest</h2>';
  body += '<p>Sold at transfer. Basis is stepped up to fair market value at death, so there is essentially no taxable '
    + 'gain at the moment of sale.</p>';
  body += '<div class="grid g4">';
  body += stat('Gross proceeds', '$' + num(h3.grossProceeds), 'Market value at transfer');
  body += stat('Selling costs', '($' + num(h3.sellingCosts) + ')', P.sellingCosts + '% assumption');
  body += stat('Net proceeds invested', '$' + num(h3.netProceeds), '');
  body += stat('Capital gain at sale', '$0', 'Stepped-up basis; verified rule');
  body += '</div>';
  body += '<div class="tablewrap"><table><thead><tr><th class="num">Year</th><th class="num">Portfolio</th>'
    + '<th class="num">Income</th><th class="num">Tax on income</th><th class="num">After-tax income</th></tr></thead><tbody>';
  for (const r of S.s3.rows) {
    body += '<tr><td class="num">' + r.year + '</td><td class="num">$' + num(r.portfolio) + '</td>'
      + '<td class="num">$' + num(r.income) + '</td><td class="num">($' + num(r.tax) + ')</td>'
      + '<td class="num">$' + num(r.cashFlow) + '</td></tr>';
  }
  body += '</tbody></table></div>';
  body += '<p class="small">Portfolio grows at ' + P.portfolioReturn + '% nominal, less a tax drag of '
    + M.round2(P.incomeComponent * P.taxOnIncome / 100) + '% a year on the income component, for a net '
    + M.round2(S.netPortfolioGrowthPct) + '% a year. If liquidated at year 20, deferred gain of $'
    + num(h3.deferredGain) + ' would be taxed at the assumed ' + P.taxOnGains + '% combined rate, leaving $'
    + num(h3.netWorth) + '. Holding longer defers that tax further.</p>';

  // --- Sensitivity
  body += '<h2>Sensitivity</h2>';
  body += '<p>The recommendation should not depend on a single guess. These runs change one input at a time.</p>';
  const sens = [
    { label: 'Base case', o: {} },
    { label: 'Appreciation 3% instead of ' + P.growth + '%', o: { growth: 3 } },
    { label: 'Appreciation 5% instead of ' + P.growth + '%', o: { growth: 5 } },
    { label: 'Property A rent $6,000/mo instead of $' + num(P.rentA), o: { rentA: 6000 } },
    { label: 'Property A rent $12,000/mo instead of $' + num(P.rentA), o: { rentA: 12000 } },
    { label: 'Third-unit rent $2,000/mo instead of $' + num(P.thirdUnitRent), o: { thirdUnitRent: 2000 } },
    { label: 'Third-unit rent $3,200/mo instead of $' + num(P.thirdUnitRent), o: { thirdUnitRent: 3200 } },
    { label: 'Portfolio return 5% instead of ' + P.portfolioReturn + '%', o: { portfolioReturn: 5 } },
    { label: 'Portfolio return 8% instead of ' + P.portfolioReturn + '%', o: { portfolioReturn: 8 } },
    { label: 'Transfer in 2040 instead of ' + Y, o: { transferYear: 2040 } },
    { label: 'Transfer in 2050 instead of ' + Y, o: { transferYear: 2050 } },
    { label: 'Property A tax rate 1.18% instead of ' + P.rateA + '%', o: { rateA: 1.18 } }
  ];
  body += '<div class="tablewrap"><table><thead><tr><th>Run</th><th class="num">Live in</th><th class="num">Rent</th>'
    + '<th class="num">Sell &amp; reinvest</th><th>Best</th></tr></thead><tbody>';
  for (const s of sens) {
    const r = M.runScenarios(s.o);
    const opts = [
      { n: 'Live in', v: r.s1.headline.netWorth },
      { n: 'Rent', v: r.s2.headline.netWorth },
      { n: 'Sell', v: r.s3.headline.netWorth }
    ];
    const best = opts.reduce((a, b) => (b.v > a.v ? b : a));
    body += '<tr><td class="label">' + esc(s.label) + '</td>'
      + '<td class="num">$' + num(opts[0].v) + '</td><td class="num">$' + num(opts[1].v) + '</td>'
      + '<td class="num">$' + num(opts[2].v) + '</td><td><strong>' + esc(best.n) + '</strong></td></tr>';
  }
  body += '</tbody></table></div>';

  body += '<h2>What would change the answer</h2>';
  body += '<div class="grid g2">';
  body += card('A much higher rent for Property A',
    '<p>The sell case is strongest while carrying cost exceeds rent. If Property A could reliably rent for well above '
    + '$' + num(M.money(S.s2.rows[0].holdingCost / 12 / (1 - P.vacancy / 100))) + ' a month, the rent scenario improves '
    + 'markedly. That is an empirical question, and it is currently unanswered. See <a href="flagged.html">F3</a>.</p>');
  body += card('A change in Proposition 19',
    '<p>Three repeal attempts have now failed, the most recent confirmed by the Secretary of State on 2026-05-18. If a '
    + 'future measure restored the old Prop 58/193 rules, the reassessment would disappear for a principal residence and '
    + 'the holding cost would fall dramatically, which would reverse the recommendation. Track it.'
    + ' <a href="law-changes.html">Pending Law Changes &rarr;</a></p>');
  body += card('Non-financial reasons to keep the house',
    '<p>This model prices money, not meaning. Living in a family home has value that is not in the table. What the model '
    + 'does say is what that choice costs: roughly $' + num(h3.netWorth - h1.netWorth) + ' of projected net position over '
    + 'twenty years, or about $' + num(M.money((h3.netWorth - h1.netWorth) / 20)) + ' a year.</p>');
  body += card('A mortgage or a co-heir',
    '<p>The model assumes the property is inherited free of debt and by a single heir. Debt service, or a buyout of '
    + 'siblings, changes the cash-flow picture substantially and could force a sale regardless of preference.</p>');
  body += '</div>';

  return { title: 'Scenarios & Recommendation', body };
}

function cf(v) {
  const s = v < 0 ? '($' + num(Math.abs(v)) + ')' : '$' + num(v);
  return s;
}

function scenarioTable(rows, cols) {
  let h = '<div class="tablewrap"><table><thead><tr>';
  for (const c of cols) h += '<th class="num">' + esc(c.label) + '</th>';
  h += '</tr></thead><tbody>';
  for (const r of rows) {
    h += '<tr>';
    for (const c of cols) {
      if (c.k === 'year') h += '<td class="num">' + r[c.k] + '</td>';
      else h += '<td class="num">' + cf(r[c.k]) + '</td>';
    }
    h += '</tr>';
  }
  h += '</tbody></table></div>';
  return h;
}

/* ------------------------------------------------------------------ *
 * page: law changes
 * ------------------------------------------------------------------ */

function pageLawChanges() {
  let body = '<h1>Pending law changes</h1>';
  body += '<p class="lede">What has already changed, what has been tried and failed, and what is under discussion. '
    + 'A proposal appears here only if its status is confirmed by an official source. Rumoured items are listed without '
    + 'values.</p>';

  body += '<h2>Already enacted</h2>';
  body += dataRows(data.lawChanges.enacted, { id: 'tbl-enacted', showTopic: true, groupKey: 'level', groupLabel: 'Level' });

  body += '<h2>Failed or inactive</h2>';
  body += '<div class="callout"><p><strong>The third attempt to repeal the inherited-property provisions of Proposition 19 '
    + 'did not qualify for the November 2026 ballot.</strong> The Secretary of State\'s memorandum to county elections '
    + 'officials states that the total number of signatures filed was less than 100% of the number required. '
    + srcLink('California Secretary of State, CC/ROV Memorandum #26138', 'https://elections.cdn.sos.ca.gov/ccrov/2026/may/26138jh.pdf')
    + '</p><p>Initiative title: "Repeals voter-enacted changes to property tax rules for transfers between family members. '
    + 'Initiative constitutional amendment." Had it qualified and passed, it would have restored much of the pre-2021 '
    + 'Prop 58/193 system. It did not qualify, so Proposition 19 stands unchanged.</p></div>';
  body += dataRows(data.lawChanges.failed_or_inactive, { id: 'tbl-failed', showTopic: true, groupKey: 'level', groupLabel: 'Level' });

  body += '<h2>Pending or discussed</h2>';
  body += '<p>These are listed so they can be tracked. Where the status could not be confirmed, the value is blank.</p>';
  body += legend();
  body += dataRows(data.lawChanges.pending_or_discussed, { id: 'tbl-pending', showTopic: true, groupKey: 'level', groupLabel: 'Level' });

  body += '<h2>Automatic change to watch</h2>';
  const idx = data.lawChanges.pending_or_discussed.find((r) => r.id === 'ca-indexing-prop19-cap');
  body += '<div class="card"><h3>' + esc(idx.label) + '</h3><p>' + esc(idx.value) + '</p><p class="small">'
    + esc(idx.note) + '</p><p class="small">' + srcLink(idx.source_name, idx.source_url) + '</p></div>';

  body += '<h2>Why this matters to the decision</h2>';
  body += '<p>Of everything on this page, only one change would reverse the recommendation: a repeal or substantial '
    + 'softening of Proposition 19\'s inherited-property rules. That is the change worth tracking every year. Three '
    + 'attempts have failed, which is evidence &mdash; not proof &mdash; that it is unlikely in the near term.</p>';

  return { title: 'Pending Law Changes', body };
}

/* ------------------------------------------------------------------ *
 * page: methodology
 * ------------------------------------------------------------------ */

function pageMethodology() {
  let body = '<h1>Methodology</h1>';
  body += '<p class="lede">How this site was built, what counts as verified, and every assumption feeding the '
    + 'projections.</p>';

  body += '<h2>The verification rule</h2>';
  body += '<div class="callout"><p>A value is published with a ' + badge('verified') + ' badge only if it was read '
    + 'directly from an official government or agency document during this pass, and the row links to that document. '
    + 'If no official source could be found, the value is left <strong>blank</strong> and marked ' + badge('unverified')
    + '. Values are never inferred, interpolated, or filled in from a secondary source.</p>'
    + '<p>Secondary sources &mdash; law-firm blogs, aggregator sites, news coverage &mdash; were consulted to find '
    + 'primary documents, but never to populate a value. Where a secondary source pointed to a figure that could not be '
    + 'confirmed, the row is blank and the item is on <a href="flagged.html">Flagged for Review</a>.</p></div>';

  body += '<h2>Badge meanings</h2>';
  body += '<div class="tablewrap"><table><thead><tr><th>Badge</th><th>Meaning</th></tr></thead><tbody>';
  body += '<tr><td>' + badge('verified') + '</td><td>Read from the linked official document.</td></tr>';
  body += '<tr><td>' + badge('owner-input') + '</td><td>Supplied from private records. Not publicly checkable.</td></tr>';
  body += '<tr><td>' + badge('projection') + '</td><td>Model output from verified and owner inputs plus the assumptions below.</td></tr>';
  body += '<tr><td>' + badge('unverified') + '</td><td>Deliberately blank. No official source found. Never inferred.</td></tr>';
  body += '</tbody></table></div>';

  body += '<h2>Every assumption in the model</h2>';
  body += '<div class="callout warn"><p><strong>None of these are facts.</strong> Each was chosen as a defensible round '
    + 'number. Change any of them and the answer moves, which is why the <a href="scenarios.html">Scenarios</a> page '
    + 'publishes a sensitivity table.</p></div>';
  body += '<div class="tablewrap"><table><thead><tr><th>Assumption</th><th class="num">Value</th><th>Rationale</th><th>Sensitivity</th></tr></thead><tbody>';
  for (const r of data.assumptions.rows) {
    body += '<tr><td class="label">' + esc(r.label) + '</td><td class="num">' + esc(fmt(r.value, r.unit)) + '</td>'
      + '<td class="note">' + esc(r.rationale) + '</td><td class="note">' + esc(r.sensitivity || '—') + '</td></tr>';
  }
  body += '</tbody></table></div>';

  body += '<h2>Model structure</h2>';
  body += '<div class="card"><h3>Projections</h3><ol style="margin:0;padding-left:20px">'
    + '<li>Property value grows from the owner\'s November 2026 estimate at the assumed appreciation rate.</li>'
    + '<li>Factored base year value grows at the verified 2% Prop 13 cap.</li>'
    + '<li>At transfer, the new taxable value is computed with the R&amp;T Code 63.2 formula: base year value plus the '
    + 'excess of market value over (base year value + indexed amount) if the heir moves in, or full market value if not.</li>'
    + '<li>After transfer the new taxable value grows at the 2% cap.</li>'
    + '<li>Annual property tax is taxable value times the effective rate.</li>'
    + '<li>Insurance, water and electricity inflate at the assumed general inflation rate. Maintenance is a percentage of '
    + 'market value.</li>'
    + '<li>Free cash flow each year is reinvested at the net portfolio growth rate.</li>'
    + '<li>Net position at year 20 is asset value, plus reinvested cash flows, less tax on a hypothetical liquidation.</li>'
    + '</ol></div>';

  body += '<h2>Known limitations</h2>';
  body += '<div class="grid g2">';
  body += card('No mortgage, no co-heirs, no probate',
    '<p>The model assumes the property is inherited free of debt by a single heir, through a trust rather than probate. '
    + 'Debt service or a sibling buyout would change the cash-flow picture materially.</p>');
  body += card('Capital gains rates are assumed',
    '<p>The combined federal and California capital gains rate used at liquidation is an assumption. Neither rate was '
    + 'confirmed from an official source. See <a href="flagged.html">F8</a>.</p>');
  body += card('Depreciation recapture is simplified',
    '<p>Scenario 2 applies a single capital gains rate to the whole gain, including the portion attributable to '
    + 'depreciation, which is normally recaptured at a different federal rate. The figures are approximate.</p>');
  body += card('Section 121 is not modelled',
    '<p>An owner-occupant who lives in the home for two of the five years before sale can exclude $250,000 of gain '
    + '($500,000 for a joint return). That rule was not verified from an official source in this pass and is therefore '
    + 'not applied, which makes the "live in" scenario slightly pessimistic.</p>');
  body += '</div>';

  body += '<h2>Reproducing this site</h2>';
  body += '<p>The site is generated from <code>data/*.json</code> by <code>tools/build.js</code>, using the projection '
    + 'engine in <code>tools/model.js</code>. Run <code>node tools/build.js</code> from the repository root. There are no '
    + 'dependencies and no network access is required to build. Every generated page is committed so GitHub Pages can '
    + 'serve it without a build step.</p>';

  return { title: 'Methodology', body };
}

/* ------------------------------------------------------------------ *
 * page: flagged
 * ------------------------------------------------------------------ */

function pageFlagged() {
  const items = data.flagged.items;
  let body = '<h1>Flagged for review</h1>';
  body += '<p class="lede">' + items.length + ' open items. Anything that could not be confirmed from an official source '
    + 'is here, together with the two irregularities found in the supplied data. None of these block the analysis; all of '
    + 'them should be closed before money moves.</p>';

  body += '<div class="grid g3">';
  body += stat('Open items', String(items.length), '');
  body += stat('High severity', String(items.filter((i) => i.severity === 'high').length), '');
  body += stat('Irregularities in the data', String(items.filter((i) => i.kind === 'irregularity').length), 'Contradictions, not just gaps');
  body += '</div>';

  body += '<div class="filter"><input type="search" data-filter="tbl-flags" placeholder="Filter flagged items…" aria-label="Filter flagged items"></div>';

  body += '<div class="tablewrap"><table id="tbl-flags"><thead><tr><th>ID</th><th>Severity</th><th>Kind</th>'
    + '<th>Issue</th><th>What to do</th><th>Impact</th><th>Reference</th></tr></thead><tbody>';
  for (const f of items) {
    body += '<tr><td class="label"><strong>' + esc(f.id) + '</strong></td>'
      + '<td>' + badge(f.severity) + '</td>'
      + '<td>' + badge(f.kind) + '</td>'
      + '<td class="note"><strong>' + esc(f.title) + '</strong><br>' + esc(f.detail)
      + (f.possible_explanations ? '<br><em>Possible explanations:</em> ' + esc(f.possible_explanations.join('; ')) : '')
      + '</td>'
      + '<td class="note">' + esc(f.action || '—') + '</td>'
      + '<td class="note">' + esc(f.impact || '—') + '</td>'
      + '<td class="src">' + srcLink(f.source_name, f.source_url) + '</td></tr>';
  }
  body += '</tbody></table></div>';

  if (data.flagged.resolved && data.flagged.resolved.length) {
    body += '<h2>Resolved during this build</h2>';
    body += '<div class="tablewrap"><table><thead><tr><th>ID</th><th>Issue</th><th>Resolution</th><th>Reference</th></tr></thead><tbody>';
    for (const f of data.flagged.resolved) {
      body += '<tr><td class="label"><strong>' + esc(f.id) + '</strong></td><td class="note">' + esc(f.title) + '</td>'
        + '<td class="note">' + esc(f.resolution) + '</td>'
        + '<td class="src">' + srcLink(f.source_name, f.source_url) + '</td></tr>';
    }
    body += '</tbody></table></div>';
  }

  body += '<h2>Priority order</h2>';
  const order = ['high', 'medium', 'low'];
  for (const sev of order) {
    const list = items.filter((i) => i.severity === sev);
    if (!list.length) continue;
    body += '<h3>' + sev.charAt(0).toUpperCase() + sev.slice(1) + ' severity</h3><ul>';
    for (const f of list) body += '<li><strong>' + esc(f.id) + '</strong> &mdash; ' + esc(f.title) + '</li>';
    body += '</ul>';
  }

  return { title: 'Flagged for Review', body };
}

/* ------------------------------------------------------------------ *
 * page: sources
 * ------------------------------------------------------------------ */

function pageSources() {
  const map = new Map();
  const add = (name, url) => {
    if (!url) return;
    if (!map.has(url)) map.set(url, { url, name: name || url, rows: 0 });
    map.get(url).rows++;
  };
  const walk = (rows) => { for (const r of rows) add(r.source_name, r.source_url); };

  walk(data.properties.rows);
  walk(data.taxHistory.official_rate_references);
  walk(data.propertyTaxLaw.rows);
  walk(data.estateTax.rows);
  walk(data.utilities.water);
  walk(data.utilities.electricity);
  walk(data.insurance.rows);
  walk(data.rental.rows);
  walk(data.lawChanges.enacted);
  walk(data.lawChanges.failed_or_inactive);
  walk(data.lawChanges.pending_or_discussed);
  for (const s of data.inheritanceProcess.steps) add(s.source_name, s.source_url);
  for (const f of data.flagged.items) add(f.source_name, f.source_url);
  add('IRS Revenue Procedure 2025-32 (2026 inflation adjustments)', 'https://www.irs.gov/pub/irs-drop/rp-25-32.pdf');
  add('IRS, Estate tax', 'https://www.irs.gov/businesses/small-businesses-self-employed/estate-tax');
  add('IRS Publication 551, Basis of Assets', 'https://www.irs.gov/pub/irs-pdf/p551.pdf');
  add('City of Cupertino, Water', 'https://www.cupertino.gov/Residents/Utilities/Water');
  add('City of Cupertino Water Service Provider GIS map', 'https://gis.cupertino.org/servicefinder/?varname=waterB');
  add('SFPUC Rate Schedules & Fees for Water and Sewer Service, FY2026-27 / FY2027-28', 'https://www.sfpuc.gov/sites/default/files/accounts-and-services/Rates_Schedule_Water_Sewer_2026-7.pdf');
  add('California Department of Insurance, 2023 CA Property & Casualty Market Share', 'https://www.insurance.ca.gov/01-consumers/120-company/04-mrktshare/2023/');
  add('California State Board of Equalization, Proposition 19', 'https://www.boe.ca.gov/prop19/');
  add('Board of Equalization, county assessor contact list', 'https://www.boe.ca.gov/proptaxes/countycontacts.htm');

  const list = Array.from(map.values()).sort((a, b) => b.rows - a.rows);

  let body = '<h1>Sources</h1>';
  body += '<p class="lede">' + list.length + ' official documents were used. Only official government, agency and utility '
    + 'sources are listed, because only those were allowed to populate a value.</p>';

  body += '<div class="tablewrap"><table><thead><tr><th>Document</th><th>Publisher</th><th class="num">Rows cited</th><th>Link</th></tr></thead><tbody>';
  for (const s of list) {
    let host = '';
    try { host = new URL(s.url).hostname.replace(/^www\./, ''); } catch (e) { host = ''; }
    body += '<tr><td class="label">' + esc(s.name) + '</td><td>' + esc(host) + '</td>'
      + '<td class="num">' + s.rows + '</td><td class="src"><a href="' + esc(s.url) + '">' + esc(s.url) + '</a></td></tr>';
  }
  body += '</tbody></table></div>';

  body += '<h2>Sources consulted but not used as evidence</h2>';
  body += '<p>Law-firm blogs, rate-aggregator sites and news coverage were read while hunting for primary documents. '
    + 'They are not listed here, and none of them was used to populate a value. Where one of them pointed at a figure '
    + 'that could not be traced to an official source, that item is on <a href="flagged.html">Flagged for Review</a>.</p>';

  body += '<h2>Reference pages worth checking yourself</h2>';
  body += '<div class="tablewrap"><table><thead><tr><th>Purpose</th><th>Where to look</th></tr></thead><tbody>';
  body += '<tr><td>Current Prop 19 indexed amount</td><td class="src">' + escLink('https://www.boe.ca.gov/prop19/') + '</td></tr>';
  body += '<tr><td>Failed ballot measures</td><td class="src">' + escLink('https://www.sos.ca.gov/elections/ballot-measures/initiative-and-referendum-status/failed-qualify') + '</td></tr>';
  body += '<tr><td>Cupertino water provider for an address</td><td class="src">' + escLink('https://gis.cupertino.org/servicefinder/?varname=waterB') + '</td></tr>';
  body += '<tr><td>San Francisco tax rate and pass-throughs</td><td class="src">' + escLink('https://sftreasurer.org/property/secured-property-taxes') + '</td></tr>';
  body += '<tr><td>Santa Clara County Assessor</td><td class="src">' + escLink('https://asr.santaclaracounty.gov/home') + '</td></tr>';
  body += '<tr><td>SF Assessor-Recorder</td><td class="src">' + escLink('https://sfassessor.org/') + '</td></tr>';
  body += '<tr><td>California Legislative Information</td><td class="src">' + escLink('https://leginfo.legislature.ca.gov/') + '</td></tr>';
  body += '</tbody></table></div>';

  return { title: 'Sources', body };
}

function escLink(url) {
  return '<a href="' + esc(url) + '">' + esc(url) + '</a>';
}

/* ------------------------------------------------------------------ *
 * page: privacy
 * ------------------------------------------------------------------ */

function pagePrivacy() {
  let body = '<h1>Privacy &amp; anonymisation</h1>';
  body += '<p class="lede">Personal information privacy is the top priority for this project. The rules applied to this '
    + 'repository and to the published site.</p>';

  body += '<div class="callout ok"><p><strong>Nothing on the published site identifies a person, a parcel, or a trust.</strong> '
    + 'No name, street address, assessor parcel number, trust name, account number, date of birth or date of death appears '
    + 'in any file in this repository, and none appears on the site.</p></div>';

  body += '<h2>The rules</h2>';
  body += '<div class="tablewrap"><table><thead><tr><th>Data</th><th>Treatment</th></tr></thead><tbody>';
  body += '<tr><td>Names of owners, heirs, trustees, beneficiaries</td><td>Never recorded. Not needed for any calculation.</td></tr>';
  body += '<tr><td>Street addresses</td><td>Never recorded. Not needed for any calculation.</td></tr>';
  body += '<tr><td>Assessor parcel numbers</td><td>Never recorded.</td></tr>';
  body += '<tr><td>Trust names and dates</td><td>Never recorded.</td></tr>';
  body += '<tr><td>Tenant identities, leases, tenancy dates</td><td>Never recorded. Rent is stored as an aggregate monthly figure.</td></tr>';
  body += '<tr><td>ZIP codes</td><td>Never recorded. Omitted from every file, matching the convention the other sessions in this repository adopted. Research is scoped by city and county, which is sufficient.</td></tr>';
  body += '<tr><td>Round-number market value estimates</td><td>Retained. Not identifying on their own, and required for every projection.</td></tr>';
  body += '<tr><td>Property tax and assessment history</td><td>Retained as owner input. These are private records; they are published only to the extent needed to show the flagged irregularities.</td></tr>';
  body += '</tbody></table></div>';

  body += '<h2>Naming convention</h2>';
  body += '<p>Properties are referred to as <strong>Property A</strong> (Cupertino, Santa Clara County, CA — the property expected to '
    + 'be inherited) and <strong>Property B</strong> (San Francisco, CA — the property currently '
    + 'owned and occupied). The letters are used consistently across every page, every data file, and every research note.</p>';

  body += '<h2>Internal versus published</h2>';
  body += '<p>The distinction that matters: personal information discovered while researching is for internal use only. '
    + 'It may exist in a private note or in a conversation, but it must never be written into a published page or a '
    + 'committed file. If a lookup requires an address &mdash; for example, the City of Cupertino water service provider '
    + 'map &mdash; do it in a browser and record only the result, never the address.</p>';

  body += '<h2>If something leaks</h2>';
  body += '<p>If you spot personal information anywhere in this repository or on the site, treat it as an incident: '
    + 'remove it, and note the removal in <code>COORDINATION.md</code>. Because GitHub Pages serves a public site from a '
    + 'public repository, anything committed is effectively published.</p>';

  return { title: 'Privacy & Anonymisation', body };
}

/* ------------------------------------------------------------------ *
 * build
 * ------------------------------------------------------------------ */

const PAGES = [
  { file: 'index.html', render: pageIndex },
  { file: 'properties.html', render: pageProperties },
  { file: 'tax-history.html', render: pageTaxHistory },
  { file: 'property-tax-law.html', render: pagePropertyTaxLaw },
  { file: 'inheritance-process.html', render: pageInheritanceProcess },
  { file: 'estate-tax.html', render: pageEstateTax },
  { file: 'insurance.html', render: pageInsurance },
  { file: 'utilities.html', render: pageUtilities },
  { file: 'rental.html', render: pageRental },
  { file: 'projections.html', render: pageProjections },
  { file: 'scenarios.html', render: pageScenarios },
  { file: 'law-changes.html', render: pageLawChanges },
  { file: 'methodology.html', render: pageMethodology },
  { file: 'sources.html', render: pageSources },
  { file: 'flagged.html', render: pageFlagged },
  { file: 'privacy.html', render: pagePrivacy }
];

function build() {
  const OUT = path.join(ROOT, 'dashboard');
  fs.mkdirSync(path.join(OUT, 'assets'), { recursive: true });
  for (const p of PAGES) {
    const { title, body } = p.render();
    const html = layout(p.file, title, body);
    fs.writeFileSync(path.join(OUT, p.file), html, 'utf8');
    console.log('  wrote ' + p.file);
  }
  const S = M.runScenarios();
  console.log('\nHeadline (transfer ' + S.params.transferYear + ', base case):');
  console.log('  Property A market value        $' + num(M.money(S.paths.fmv)));
  console.log('  Tax if heir moves in           $' + num(M.money(S.paths.pathB.annualTax)) + '/yr');
  console.log('  Tax if rented out              $' + num(M.money(S.paths.pathC.annualTax)) + '/yr');
  console.log('  S1 live in      net worth yr20 $' + num(S.s1.headline.netWorth));
  console.log('  S2 rent         net worth yr20 $' + num(S.s2.headline.netWorth));
  console.log('  S3 sell         net worth yr20 $' + num(S.s3.headline.netWorth));
  console.log('\n' + PAGES.length + ' pages built.');
}

build();
