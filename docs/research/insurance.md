# T5 — Home Insurance Research (CA Department of Insurance + official sources)

Verification date: 2026-11-06.
Note: curl/python downloads from insurance.ca.gov are TLS-blocked in this sandbox — data obtained via fetch_page on official xlsx files.

## Statewide averages — CDI Part I "Written Premium by Policy Form" (VERIFIED)

Source page: https://www.insurance.ca.gov/0400-news/0200-studies-reports/0250-homeowners-study/
Data file: A-Part-I-Data-Summary.xlsx (fetched 2026-11-06)

| Policy form | Avg written premium (pooled 2008–2023) | Status |
|---|---|---|
| Homeowners Multi-Peril | $1,176 | VERIFIED (statewide pooled — understates current year; FLAG) |
| Dwelling Fire — Owner-Occupied | $798 | VERIFIED (pooled) |
| Dwelling Fire — Tenant-Occupied (landlord policy for Property B) | $601 | VERIFIED (pooled) |
| Condo | $537 | VERIFIED (pooled) |
| Renters/Tenant | $190 | VERIFIED (pooled) |
| Mobile home | $650 | VERIFIED (pooled) |

## Statewide trends — CDI SB 824 ZIP data workbook, summary sheet (VERIFIED)

File: Residential-Property-Coverage-Amounts-Wildfire-Risk-and-Losses.xlsx (fetched 2026-11-06)

| Year | Statewide earned premium | Exposures | Avg Coverage A | Avg Coverage C |
|---|---|---|---|---|
| 2018 | $8.33B | 11.38M | $230,138 | $76,762 |
| 2023 | $14.22B | 12.58M | $324,973 | $93,927 |

(Intermediate years in workbook; 2018 and 2023 endpoints recorded.)

## ZIP-level data (95014 / 94122)

| Item | Value | Status |
|---|---|---|
| ZIP 95014 avg premium / loss data | — | **NOT EXTRACTED — left blank, FLAGGED** (report page linked for manual review) |
| ZIP 94122 avg premium / loss data | — | **NOT EXTRACTED — left blank, FLAGGED** |

Manual-review link: https://www.insurance.ca.gov/0400-news/0200-studies-reports/0250-homeowners-study/

## Official comparison / quoting tools

| Tool | URL | Status |
|---|---|---|
| CDI 2026 Homeowners Insurance Comparison Tool | https://interactive.web.insurance.ca.gov/apex_extprd/f?p=111:20 | VERIFIED (official) — note: wildfire surcharges 15%–300%+ not reflected in tool premiums |
| County Coverage A averages (PDF) | linked from CDI study page (D-Average-of-Coverage-A-C_v1.pdf) | VERIFIED link exists |

## User estimates (UNVERIFIED)

| Item | Value | Status |
|---|---|---|
| Property A insurance estimate | ~$1,500/yr | USER-PROVIDED GUESS — FLAG |
| Property B insurance estimate | ~$1,500/yr | USER-PROVIDED GUESS — FLAG |

**Site treatment: user guesses shown in a clearly-marked "user estimate" column; official-verified columns left blank where ZIP data was not extracted; all flagged on Flagged for Review page.**
