'use strict';
/**
 * check.js — pre-publish verification.
 *
 * 1. every internal link in a generated page resolves to a file that exists
 * 2. every row marked `verified` carries a source_url
 * 3. every row marked `unverified` has an EMPTY value (the rule: never infer)
 * 4. no page contains a leftover template artefact
 * 5. external links are https
 */

const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const SITE = path.join(ROOT, 'dashboard');
const DATA = path.join(ROOT, 'data', 'dashboard');

const errors = [];
const warnings = [];

function fail(msg) { errors.push(msg); }
function warn(msg) { warnings.push(msg); }

/* ---- 1. internal links ---- */
const pages = fs.readdirSync(SITE).filter((f) => f.endsWith('.html'));
for (const p of pages) {
  const html = fs.readFileSync(path.join(SITE, p), 'utf8');
  const re = /href="([^"#][^"]*)"/g;
  let m;
  while ((m = re.exec(html)) !== null) {
    const href = m[1];
    if (/^(https?:|mailto:|tel:)/i.test(href)) continue;
    const target = href.split('#')[0];
    if (!target) continue;
    const resolved = path.join(SITE, target);
    if (!fs.existsSync(resolved)) fail(`${p}: broken link -> ${href}`);
  }
  // template artefacts
  for (const bad of ['undefined', 'NaN', '[object Object]', '${']) {
    if (html.includes(bad)) fail(`${p}: page contains template artefact "${bad}"`);
  }
}

/* ---- 2 & 3. row-level rules ---- */
const files = fs.readdirSync(DATA).filter((f) => f.endsWith('.json') && f !== '_schema.md');
let rowCount = 0, verifiedCount = 0, unverifiedCount = 0, projectionCount = 0, ownerCount = 0;

function checkRows(rows, file) {
  for (const r of rows) {
    // Only rows that carry a `value` field are subject to the value rules.
    // Step objects in the inheritance-process file have `step`/`detail`, not `value`.
    if (!r.status || !('value' in r)) continue;
    rowCount++;
    if (r.status === 'verified') {
      verifiedCount++;
      if (!r.source_url) fail(`${file}: row "${r.id}" is verified but has no source_url`);
      if (!r.source_name) warn(`${file}: row "${r.id}" is verified but has no source_name`);
      if (r.value === '' || r.value === null || r.value === undefined) {
        fail(`${file}: row "${r.id}" is verified but the value is blank`);
      }
    } else if (r.status === 'unverified') {
      unverifiedCount++;
      if (r.value !== '' && r.value !== null && r.value !== undefined) {
        fail(`${file}: row "${r.id}" is marked unverified but has a value (${r.value}) — the rule is never to infer`);
      }
    } else if (r.status === 'projection') {
      projectionCount++;
    } else if (r.status === 'owner-input') {
      ownerCount++;
    }
  }
}

for (const f of files) {
  const j = JSON.parse(fs.readFileSync(path.join(DATA, f), 'utf8'));
  if (Array.isArray(j.rows)) checkRows(j.rows, f);
  for (const key of Object.keys(j)) {
    const v = j[key];
    if (Array.isArray(v) && v.length && v[0] && typeof v[0] === 'object' && 'status' in v[0]) checkRows(v, f);
  }
}

/* ---- 4. external links are https ---- */
for (const p of pages) {
  const html = fs.readFileSync(path.join(SITE, p), 'utf8');
  const re = /href="(http:\/\/[^"]*)"/g;
  let m;
  while ((m = re.exec(html)) !== null) warn(`${p}: insecure external link ${m[1]}`);
}

/* ---- 5. privacy scan ---- */
const privacyPatterns = [
  /\b\d{1,5}\s+[NSEW]\.?\s+\w+\s+(St|Ave|Street|Avenue|Blvd|Road|Rd|Drive|Dr|Court|Ct|Lane|Ln|Way|Place|Pl)\b/i,
  /\bAPN\b/i,
  /\b\d{3}-\d{2}-\d{4}\b/
];
for (const p of pages) {
  const html = fs.readFileSync(path.join(SITE, p), 'utf8');
  const text = html.replace(/<[^>]*>/g, ' ');
  for (const re of privacyPatterns) {
    if (re.test(text)) fail(`${p}: possible personal data matched ${re}`);
  }
}

/* ---- report ---- */
console.log('Pages checked:            ' + pages.length);
console.log('Data rows checked:        ' + rowCount);
console.log('  verified:               ' + verifiedCount);
console.log('  owner-input:            ' + ownerCount);
console.log('  projection:             ' + projectionCount);
console.log('  unverified (blank):     ' + unverifiedCount);
console.log('');
if (warnings.length) {
  console.log('Warnings (' + warnings.length + '):');
  for (const w of warnings) console.log('  ! ' + w);
  console.log('');
}
if (errors.length) {
  console.log('ERRORS (' + errors.length + '):');
  for (const e of errors) console.log('  x ' + e);
  process.exit(1);
}
console.log('All checks passed.');
