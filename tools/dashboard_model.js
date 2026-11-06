'use strict';
/**
 * model.js — deterministic projection engine.
 *
 * Everything produced here is a PROJECTION built from (a) values verified against
 * official sources, (b) owner-supplied inputs, and (c) assumptions listed in
 * data/assumptions.json. Nothing computed here is a verified fact.
 */

const fs = require('fs');
const path = require('path');

const DATA = path.join(__dirname, '..', 'data', 'dashboard');
const read = (f) => JSON.parse(fs.readFileSync(path.join(DATA, f), 'utf8'));

const assumptions = read('assumptions.json');
const A = {};
for (const r of assumptions.rows) A[r.id] = r.value;

const properties = read('properties.json');
const taxHistory = read('tax-history.json');

const START_YEAR = 2026;
const END_YEAR = 2055;

const money = (n) => Math.round(n);
const round2 = (n) => Math.round(n * 100) / 100;

/** Compound growth. */
function grow(base, ratePct, years) {
  return base * Math.pow(1 + ratePct / 100, years);
}

/** Property A market value by year. */
function propertyCValue(year, growthPct) {
  return grow(3100000, growthPct, year - START_YEAR);
}

/** Property B market value by year. */
function propertySValue(year, growthPct) {
  return grow(1800000, growthPct, year - START_YEAR);
}

/** Property A factored base year value by year (Prop 13, 2% cap). */
function propertyCFBYV(year) {
  return grow(550537, A['prop13-growth'], year - START_YEAR);
}

/** Property B factored base year value by year. */
function propertySFBYV(year) {
  return grow(114248, A['prop13-growth'], year - START_YEAR);
}

/** Prop 19 indexed $1 million amount by year (assumption-driven). */
function prop19Cap(year) {
  return grow(1044586, A['prop19-cap-index'], year - START_YEAR);
}

/** Federal basic exclusion amount by year. 2026 is verified; later years are projections. */
function federalExemption(year) {
  const t = read('estate-tax.json').threshold_projection;
  if (year <= t.base_year) return t.verified_anchor.value;
  return grow(t.verified_anchor.value, t.assumed_annual_inflation_pct, year - t.base_year);
}

/* ------------------------------------------------------------------ *
 * Property A property tax under each path
 * ------------------------------------------------------------------ */

/**
 * @param {number} transferYear  year of change in ownership
 * @param {number} growthPct     market appreciation assumption
 * @param {number} ratePct       effective property tax rate
 */
function propertyCTaxPaths(transferYear, growthPct, ratePct) {
  const fbyv = propertyCFBYV(transferYear);
  const fmv = propertyCValue(transferYear, growthPct);
  const cap = prop19Cap(transferYear);
  const excluded = fbyv + cap;

  // Path A — no transfer: Prop 13 base keeps growing 2% a year.
  const pathA = {
    id: 'A',
    name: 'No transfer — base year value continues',
    taxable: fbyv,
    annualTax: (fbyv * ratePct) / 100
  };

  // Path B — transfer and the heir moves in: partial exclusion under R&T 63.2.
  const excess = Math.max(0, fmv - excluded);
  const taxableB = fbyv + excess;
  const pathB = {
    id: 'B',
    name: 'Transfer + heir moves in — Prop 19 partial exclusion',
    taxable: taxableB,
    annualTax: (taxableB * ratePct) / 100,
    excludedAmount: excluded,
    excessOverCap: excess
  };

  // Path C — transfer and the heir does not move in: full reassessment.
  const pathC = {
    id: 'C',
    name: 'Transfer + heir does not move in — full reassessment',
    taxable: fmv,
    annualTax: (fmv * ratePct) / 100
  };

  return { transferYear, growthPct, ratePct, fbyv, fmv, cap, excluded, pathA, pathB, pathC };
}

/** Property tax for a given assessment in a given year, both properties. */
function annualTax(taxableValue, ratePct) {
  return (taxableValue * ratePct) / 100;
}

/* ------------------------------------------------------------------ *
 * Holding cost model
 * ------------------------------------------------------------------ */

/**
 * Annual holding cost for a property, in nominal dollars, for a given number of
 * years after the base year.
 */
function holdingCost(opts) {
  const {
    baseYear,
    year,
    value,                 // market value in `year`
    taxableValue,          // assessed value in `year`
    ratePct,               // effective property tax rate
    insuranceBase,         // annual insurance in base year
    maintenancePct,        // annual maintenance as % of market value
    waterMonthly,
    electricMonthly,       // negative means a net credit
    inflationPct = A['general-inflation']
  } = opts;

  const n = year - baseYear;
  const inf = Math.pow(1 + inflationPct / 100, n);

  const propertyTax = annualTax(taxableValue, ratePct);
  const insurance = insuranceBase * inf;
  const maintenance = value * (maintenancePct / 100);
  const water = waterMonthly * 12 * inf;
  const electric = electricMonthly * 12 * inf;

  return {
    year,
    propertyTax: money(propertyTax),
    insurance: money(insurance),
    maintenance: money(maintenance),
    water: money(water),
    electric: money(electric),
    total: money(propertyTax + insurance + maintenance + water + electric)
  };
}

/* ------------------------------------------------------------------ *
 * Scenarios
 * ------------------------------------------------------------------ */

const SCEN = {
  transferYear: A['inheritance-year'],
  horizon: 20,
  growth: A['appreciation-base'],
  rateA: A['rate-a'],
  rateB: A['rate-b'],
  sellingCosts: A['selling-costs'],
  portfolioReturn: A['portfolio-return'],
  incomeComponent: A['reinvestment-yield'],
  taxOnIncome: A['combined-tax-on-income'],
  taxOnGains: 33.3, // ASSUMPTION, flagged (F8): combined federal + CA long-term capital gains
  vacancy: A['vacancy'],
  rentGrowthB: A['rent-growth-b'],
  thirdUnitRent: A['third-unit-rent'],
  rentA: A['rent-a'],
  insuranceA: A['insurance-a'],
  insuranceB: A['insurance-b'],
  maintenanceA: A['maintenance-a'],
  maintenanceB: A['maintenance-b'],
  waterA: A['water-a'],
  electricA: A['electric-a'],
  waterB: A['water-b'],
  electricB: A['electric-b'],
  depreciationYears: 27.5, // ASSUMPTION: MACRS residential rental
  buildingShare: 0.8       // ASSUMPTION: building share of value for depreciation
};

/**
 * Run all three scenarios.
 * Returns per-year rows plus headline comparison figures.
 */
function runScenarios(overrides = {}) {
  const S = Object.assign({}, SCEN, overrides);
  const Y = S.transferYear;
  const years = [];
  const fmvC = propertyCValue(Y, S.growth);
  const fmvS = propertySValue(Y, S.growth);

  // ---- Shared: Property B baseline (owner stays) ---------------------
  // Property B keeps its Prop 13 base because no transfer occurs.
  const sFBYV = propertySFBYV(Y);

  // ---- Shared: Property A assessed value under each path -------------
  const paths = propertyCTaxPaths(Y, S.growth, S.rateA);

  for (let i = 0; i <= S.horizon; i++) {
    const year = Y + i;
    const valueC = propertyCValue(year, S.growth);
    const valueS = propertySValue(year, S.growth);
    const inf = Math.pow(1 + A['general-inflation'] / 100, i);

    // Property A taxable value in this year under each path
    const taxableA = propertyCFBYV(year);                                  // no transfer
    const taxableB = grow(paths.pathB.taxable, A['prop13-growth'], i);     // moved in
    const taxableC = grow(paths.pathC.taxable, A['prop13-growth'], i);     // rented / not moved in

    const costFn = (taxable, insuranceBase, maintenancePct, water, electric) =>
      holdingCost({
        baseYear: Y, year, value: valueC, taxableValue: taxable,
        ratePct: S.rateA, insuranceBase, maintenancePct,
        waterMonthly: water, electricMonthly: electric
      });

    const costMoveIn = costFn(taxableB, S.insuranceA, S.maintenanceA, S.waterA, S.electricA);
    const costRentOut = costFn(taxableC, S.insuranceA, S.maintenanceA, S.waterA, S.electricA);

    // Property B holding cost (owner-occupied, two units rented)
    const costPropertyB = holdingCost({
      baseYear: Y, year, value: valueS, taxableValue: propertySFBYV(year),
      ratePct: S.rateB, insuranceBase: S.insuranceB, maintenancePct: S.maintenanceB,
      waterMonthly: S.waterB, electricMonthly: S.electricB
    });

    // Rent rolls
    const rentBTwoUnits = grow(7150, S.rentGrowthB, i) * 12;                    // two units, current tenancy
    const rentBThreeUnits = rentBTwoUnits + grow(S.thirdUnitRent, S.rentGrowthB, i) * 12; // all three units
    const rentA = grow(S.rentA, S.growth, i) * 12 * (1 - S.vacancy / 100);

    years.push({
      year, i, valueC, valueS,
      taxableA, taxableB, taxableC,
      costMoveIn, costRentOut, costPropertyB,
      rentBTwoUnits, rentBThreeUnits, rentA
    });
  }

  // ---- Scenario 1: live in Property A, rent the freed Property B unit
  const s1 = { id: 'S1', name: 'Live in Property A', rows: [] };
  {
    let invested = 0;
    for (const y of years) {
      const rentFreed = (y.rentBThreeUnits - y.rentBTwoUnits);              // third unit only
      const taxOnRent = Math.max(0, rentFreed) * (S.taxOnIncome / 100);
      const cf = rentFreed - taxOnRent - y.costMoveIn.total;
      invested = invested * (1 + netPortfolioGrowth(S) / 100) + cf;
      s1.rows.push({
        year: y.year,
        rentIncome: money(rentFreed),
        taxOnRent: money(taxOnRent),
        holdingCost: y.costMoveIn.total,
        propertyTax: y.costMoveIn.propertyTax,
        cashFlow: money(cf),
        invested: money(invested)
      });
    }
    const last = s1.rows[s1.rows.length - 1];
    const endValue = years[years.length - 1].valueC;
    // Personal residence: gain over the stepped-up basis. Section 121 exclusion is
    // noted in the narrative but NOT modelled (not verified).
    const gainOnSale = Math.max(0, endValue - fmvC);
    const taxOnSale = gainOnSale * (S.taxOnGains / 100);
    s1.headline = {
      year1CashFlow: s1.rows[0].cashFlow,
      year20CashFlow: last.cashFlow,
      endPropertyValue: money(endValue),
      investedCashFlows: last.invested,
      gainOnSale: money(gainOnSale),
      taxOnSale: money(taxOnSale),
      netWorth: money(endValue - taxOnSale + last.invested)
    };
  }

  // ---- Scenario 2: rent Property A, stay in Property B
  const s2 = { id: 'S2', name: 'Rent Property A', rows: [] };
  {
    const depreciableBasis = fmvC * S.buildingShare;
    const annualDepreciation = depreciableBasis / S.depreciationYears;
    let invested = 0;
    let accumulatedDepreciation = 0;
    for (const y of years) {
      const noi = y.rentA - y.costRentOut.total;
      accumulatedDepreciation = Math.min(depreciableBasis, accumulatedDepreciation + annualDepreciation);
      const taxable = Math.max(0, noi - annualDepreciation);
      const tax = taxable * (S.taxOnIncome / 100);
      const cf = noi - tax;
      invested = invested * (1 + netPortfolioGrowth(S) / 100) + cf;
      s2.rows.push({
        year: y.year,
        rentIncome: money(y.rentA),
        holdingCost: y.costRentOut.total,
        propertyTax: y.costRentOut.propertyTax,
        noi: money(noi),
        depreciation: money(annualDepreciation),
        tax: money(tax),
        cashFlow: money(cf),
        invested: money(invested)
      });
    }
    const last = s2.rows[s2.rows.length - 1];
    const endValue = years[years.length - 1].valueC;
    const adjustedBasis = fmvC - accumulatedDepreciation;
    const gainOnSale = Math.max(0, endValue - adjustedBasis);
    const taxOnSale = gainOnSale * (S.taxOnGains / 100);
    s2.headline = {
      year1CashFlow: s2.rows[0].cashFlow,
      year20CashFlow: last.cashFlow,
      endPropertyValue: money(endValue),
      investedCashFlows: last.invested,
      accumulatedDepreciation: money(accumulatedDepreciation),
      adjustedBasis: money(adjustedBasis),
      gainOnSale: money(gainOnSale),
      taxOnSale: money(taxOnSale),
      netWorth: money(endValue - taxOnSale + last.invested)
    };
  }

  // ---- Scenario 3: sell Property A at inheritance and reinvest
  const s3 = { id: 'S3', name: 'Sell and reinvest', rows: [] };
  {
    const grossProceeds = fmvC;
    const costs = grossProceeds * (S.sellingCosts / 100);
    const netProceeds = grossProceeds - costs;
    // Stepped-up basis equals FMV at death, so gain at sale is ~zero and there is
    // no capital gains tax at the moment of sale.
    const gainAtSale = 0;
    let portfolio = netProceeds;
    for (const y of years) {
      const incomeBefore = portfolio * (S.incomeComponent / 100);
      const tax = incomeBefore * (S.taxOnIncome / 100);
      const cf = incomeBefore - tax; // cash thrown off, reinvested
      if (y.i > 0) {
        s3.rows.push({
          year: y.year,
          portfolio: money(portfolio),
          income: money(incomeBefore),
          tax: money(tax),
          cashFlow: money(cf)
        });
      }
      portfolio = portfolio * (1 + netPortfolioGrowth(S) / 100);
    }
    // final row
    {
      const y = years[years.length - 1];
      const incomeBefore = portfolio * (S.incomeComponent / 100);
      const tax = incomeBefore * (S.taxOnIncome / 100);
      s3.rows.push({
        year: y.year,
        portfolio: money(portfolio),
        income: money(incomeBefore),
        tax: money(tax),
        cashFlow: money(incomeBefore - tax)
      });
    }
    const last = s3.rows[s3.rows.length - 1];
    const deferredGain = Math.max(0, last.portfolio - netProceeds);
    const taxOnLiquidation = deferredGain * (S.taxOnGains / 100);
    s3.headline = {
      grossProceeds: money(grossProceeds),
      sellingCosts: money(costs),
      netProceeds: money(netProceeds),
      gainAtSale: money(gainAtSale),
      year1CashFlow: s3.rows[0] ? s3.rows[0].cashFlow : 0,
      year20CashFlow: last.cashFlow,
      endPortfolio: last.portfolio,
      deferredGain: money(deferredGain),
      taxOnLiquidation: money(taxOnLiquidation),
      netWorth: money(last.portfolio - taxOnLiquidation)
    };
  }

  return {
    params: S,
    years,
    paths,
    fmvC,
    fmvS,
    s1,
    s2,
    s3,
    netPortfolioGrowthPct: netPortfolioGrowth(S)
  };
}

/** Portfolio growth net of the annual tax drag on the income component. */
function netPortfolioGrowth(S) {
  const gross = S.portfolioReturn;
  const drag = (S.incomeComponent * S.taxOnIncome) / 100;
  return gross - drag;
}

/* ------------------------------------------------------------------ *
 * Tables for the projections page
 * ------------------------------------------------------------------ */

function valueProjectionTable() {
  const rows = [];
  for (let y = START_YEAR; y <= END_YEAR; y++) {
    rows.push({
      year: y,
      cLow: money(propertyCValue(y, A['appreciation-low'])),
      cBase: money(propertyCValue(y, A['appreciation-base'])),
      cHigh: money(propertyCValue(y, A['appreciation-high'])),
      cFBYV: money(propertyCFBYV(y)),
      sLow: money(propertySValue(y, A['appreciation-low'])),
      sBase: money(propertySValue(y, A['appreciation-base'])),
      sHigh: money(propertySValue(y, A['appreciation-high'])),
      sFBYV: money(propertySFBYV(y)),
      exemption: money(federalExemption(y))
    });
  }
  return rows;
}

function transferTaxTable() {
  const rows = [];
  const growths = [A['appreciation-low'], A['appreciation-base'], A['appreciation-high']];
  for (const y of [2040, 2045, 2050]) {
    for (const g of growths) {
      const p = propertyCTaxPaths(y, g, A['rate-a']);
      rows.push({
        transferYear: y,
        growth: g,
        fmv: money(p.fmv),
        fbyv: money(p.fbyv),
        cap: money(p.cap),
        excluded: money(p.excluded),
        taxNoTransfer: money(p.pathA.annualTax),
        taxMoveIn: money(p.pathB.annualTax),
        taxableMoveIn: money(p.pathB.taxable),
        taxRentOut: money(p.pathC.annualTax),
        penaltyForNotMovingIn: money(p.pathC.annualTax - p.pathB.annualTax),
        exclusionSaves: money(p.pathC.annualTax - p.pathB.annualTax)
      });
    }
  }
  return rows;
}

function exemptionProjectionTable() {
  const rows = [];
  const t = read('estate-tax.json').threshold_projection;
  for (let y = t.base_year; y <= END_YEAR; y++) {
    rows.push({
      year: y,
      perPerson: money(federalExemption(y)),
      coupleWithPortability: money(federalExemption(y) * 2),
      status: y === t.base_year ? 'verified' : 'projection'
    });
  }
  return rows;
}

function holdingCostTable() {
  const rows = [];
  const Y = A['inheritance-year'];
  for (const y of [2030, 2035, 2040, 2045, 2050, 2055]) {
    const valueC = propertyCValue(y, A['appreciation-base']);
    const valueS = propertySValue(y, A['appreciation-base']);
    const cCurrent = holdingCost({
      baseYear: START_YEAR, year: y, value: valueC, taxableValue: propertyCFBYV(y),
      ratePct: A['rate-a'], insuranceBase: A['insurance-a'], maintenancePct: A['maintenance-a'],
      waterMonthly: A['water-a'], electricMonthly: A['electric-a']
    });
    const sCurrent = holdingCost({
      baseYear: START_YEAR, year: y, value: valueS, taxableValue: propertySFBYV(y),
      ratePct: A['rate-b'], insuranceBase: A['insurance-b'], maintenancePct: A['maintenance-b'],
      waterMonthly: A['water-b'], electricMonthly: A['electric-b']
    });
    rows.push({ year: y, propertyC: cCurrent, propertyS: sCurrent });
  }
  return rows;
}

function taxHistoryWithRates() {
  const out = {};
  for (const key of ['property_a', 'property_b']) {
    out[key] = taxHistory[key].rows.map((r) => ({
      ...r,
      impliedRatePct: r.taxes && r.assessment ? round2((r.taxes / r.assessment) * 100) : null
    }));
  }
  return out;
}

module.exports = {
  A,
  START_YEAR,
  END_YEAR,
  assumptions,
  properties,
  taxHistory,
  grow,
  propertyCValue,
  propertySValue,
  propertyCFBYV,
  propertySFBYV,
  prop19Cap,
  federalExemption,
  propertyCTaxPaths,
  annualTax,
  holdingCost,
  runScenarios,
  valueProjectionTable,
  transferTaxTable,
  exemptionProjectionTable,
  holdingCostTable,
  taxHistoryWithRates,
  money,
  round2
};
