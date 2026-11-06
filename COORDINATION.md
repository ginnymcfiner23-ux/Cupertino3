# COORDINATION.md — Shared Task Board

Session ID: `d8a9b67c` (branch `arena/d8a9b67c-cupertino3`)
Started: 2026-11-06

## Session/branch convention

> Platform constraint: this session runs inside Arena Agent Mode, which pins all work to
> the branch `arena/d8a9b67c-cupertino3`. Session `d8a9b67c` therefore commits and pushes
> ONLY to `arena/d8a9b67c-cupertino3` (it cannot create/push other branch names). All other
> sessions: use your own `session-<id>/<task>` branch and claim your file scope below first.
> Session `d8a9b67c` is acting as the integration session for this run.

## Privacy rules (highest priority)

- No personal information (names, street addresses, APNs, account numbers, occupant names)
  may appear in the published site. ZIP codes and city-level data are permitted.
- Any PII discovered during research is INTERNAL ONLY and must never be committed to site
  output files.

## Task board

| Task ID | Task | Status | Owner session | Files / scope | Notes |
|---|---|---|---|---|---|
| T1 | Coordination board setup | done | d8a9b67c | COORDINATION.md | Created board |
| T2 | Research: federal estate/gift tax & inheritance law (official sources) | done | d8a9b67c | docs/research/federal-tax.md | IRS/congress.gov only |
| T3 | Research: CA state inheritance/estate tax, Prop 13/19, reassessment (official sources) | done | d8a9b67c | docs/research/ca-law.md | BOE/leginfo/voterguide |
| T4 | Research: property tax & assessment data, county rates (Santa Clara, SF) | done | d8a9b67c | docs/research/property-tax.md | sccgov.org, sfgov.org |
| T5 | Research: home insurance Cupertino 95014 & SF 94122 rental (official/regulatory sources) | done | d8a9b67c | docs/research/insurance.md | CA Dept of Insurance; quotes = unverified estimates |
| T6 | Research: utilities (water/electric/solar) & recurring costs | done | d8a9b67c | docs/research/utilities.md | cityofcupertino.org, sfpuc.org, cpuc.ca.gov |
| T7 | Research: SF rent control/AB 1482 & rental income rules | done | d8a9b67c | docs/research/rental-law.md | sfrb.org, leginfo |
| T8 | Projections: value, taxes, costs, sell-vs-rent-vs-live models | done | d8a9b67c | docs/research/projections.md, site data | Model outputs flagged as projections |
| T9 | Step-by-step inheritance process guide (trust, CA steps) | done | d8a9b67c | site pages | courts.ca.gov, BOE forms |
| T10 | Pending law changes watchlist (federal + CA, 2025–2026 session) | done | d8a9b67c | site pages | congress.gov, leginfo |
| T11 | Site build: landing page, subpages, tables, navigation | done | d8a9b67c | index.html, assets/, pages/ | Dashboard-style UI |
| T12 | Verification pass: every row → official source link or flagged | done | d8a9b67c | all site data + Flagged page | No inferred values |
| T13 | Integration, line-by-line re-verify, link check, PR → main, merge, GitHub Pages deploy | in progress | d8a9b67c | whole repo | Record PR + deploy result below |

## Request log (cross-session change requests)

_(Empty)_

## Conflict log

_(Empty)_

## Completed-task records

### T1 — Coordination board setup (session d8a9b67c)
- Sources: n/a
- Verification: repo initialized with README only; board created.
- Irregularities: none.


### T2–T7 — Research (session d8a9b67c)
- Files: docs/research/{federal-tax,ca-law,property-tax,insurance,utilities,rental-law}.md + research/notes.md
- Sources: IRS (estate tax, FAQ, RP 2025-32, i706, Pub 551, Topics 409/559, Pub 530), SCO (no CA estate tax),
  BOE (LTA 25023/24053/26002, LTA 20061, Rules 460/462.520, Prop 19, NR 2025-02, Pub 30, forms),
  FTB (federal-changes summary, bill analyses), leginfo (AB 1482 text, SB-284 status, Civ. Code 1954.53),
  congress.gov (S.587, H.R.1301, H.R.25), sftreasurer.org (FY26-27 rate 1.18162182%),
  sf.gov rent increases (1.6%), files.santaclaracounty.gov tax rate book, cupertino.gov utilities + flyers,
  sfpuc.gov Prop 218 notice, sjwater.com AL-628, calwater.com tariff, insurance.ca.gov CDI workbooks
  (via fetch_page; curl TLS-blocked), courts.ca.gov living-trusts, occourts wills-trusts,
  huduser.gov FMR, fhfa.gov HPI 2025Q3, SOS memo #26138 (initiative #1994 failure), cupertino.legistar 19-2194.
- Verification: every site table row carries an official source link OR a blank+flag; 59 unique external URLs
  on the site, all fetched/confirmed this session (188 total link instances).
- Irregularities: see docs/research/notes.md §16 and site Flagged page (25 items): user tax-% mismatches (A 2017/2019,
  B 2022/2023), B implied 2.135% vs official 1.18162182%, A implied 1.335% vs TRA range, B 2021→22 AV 1.96%,
  B 2018 +18.4% jump, ZIP insurance rows not extracted, market rent blank, transferor-PR status unknown.

### T8 — Projections (session d8a9b67c)
- Files: docs/research/build_projections.py, projections.csv, projections_inheritance.csv, projections_estate.csv, projections.md
- Sources/anchors: BOE factor table (2% AV growth, law), SF TTC rate (VERIFIED), FHFA HPI 2025Q3 (CA -0.6% YoY;
  long-run ≈4.2%/yr base), IRS RP 2025-32 + i706 (estate math), SCO ($0 CA), Prop 19 cap BOE NR 2025-02.
- Verification: model re-runnable; assumptions register published on site (6%/7%/2.5% flagged as no-official-source).
- Irregularities: future Prop 19 exclusion amount unknown (held flat, flagged); no official A market rent (blank+flag).

### T9 — Inheritance process guide (session d8a9b67c)
- File: site/src/process.html → pages/process.html
- Sources: santaclara.courts.ca.gov living trusts, occourts wills/trusts, BOE prop19 (BOE-19-P 3-yr, exemption 1-yr),
  BOE forms (502-D 150-day), SF TTC (supplemental), BOE Pub 30 (appeals), IRS 706 FAQ (9-month/$15M), Pub 551, Form 1041.
- Verification: deadlines sourced; internal tasks marked as such.
- Irregularities: supplemental-appeal window is per-notice (flagged for calendar).

### T10 — Law watchlist (session d8a9b67c)
- File: site/src/watchlist.html → pages/watchlist.html
- Sources: congress.gov S.587/H.R.1301/H.R.25 (all Introduced only), leginfo SB-284 (held in Assembly committee
  since 2025-07-14), SOS memo #26138 (repeal initiative failed), RP 2025-32 (OBBBA enacted, indexing 2027+),
  AB 1482 sunset 2030-01-01, sf.gov annual CPI windows, BOE December factor letters, SFPUC July 1 rates.
- Verification: statuses fetched 2026-11-06.
- Irregularities: none beyond pending-status caveats.

### T11 — Site build (session d8a9b67c)
- Files: index.html, pages/*.html (13 pages), assets/style.css, site/src/* (fragments), site/build.py, tools/check_links.py
- Sources: n/a (build tooling).
- Verification: python3 site/build.py + python3 tools/check_links.py → PASS (13 files, 188 external links,
  0 broken internal links). PII grep scan: clean (city/ZIP only).
- Irregularities: none.

### T12 — Verification pass (session d8a9b67c)
- Files: all site data + pages/flagged.html (25 flagged items)
- Sources: per-row official links as embedded.
- Verification: 59/59 unique external URLs fetched or content-confirmed this session; internal link check PASS;
  leginfo/legistar/SOS/FHFA/IRS/BOE spot-re-fetches done after link fixes.
- Irregularities: logged on Flagged page (user-table inconsistencies, rate discrepancies, blanks by rule,
  assumption flags) — flagged items do not block merge per integration rules.

## Integration / deploy record

- PR link: _(pending)_
- Merge result: _(pending)_
- GitHub Pages deploy: _(pending)_
