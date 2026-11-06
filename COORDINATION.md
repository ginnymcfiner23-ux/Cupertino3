# COORDINATION.md — Shared Task Board

Repo: `ginnymcfiner23-ux/Cupertino3`
Live site: https://ginnymcfiner23-ux.github.io/Cupertino3/

## How this session handles branch scope

Arena pins this session to the branch **`arena/56e7a5a3-cupertino3`** and forbids creating or
switching to other branches. The coordination protocol asks for per-task branches named
`session-<id>/<task>`. To satisfy both, this session used **directory-level file scopes inside the
single session branch** instead of separate branches. `git branch -a` showed only `main` and this
branch at the start, and no other session claimed anything, so there was no live contention.

If a second session appears it must append its claims to the table below and respect the listed
scopes — do not edit files inside another session's scope, and log any cross-scope change request
here instead of making it.

| Session ID | Branch | Scope |
|---|---|---|
| `arena/56e7a5a3-cupertino3` (session A) | `arena/56e7a5a3-cupertino3` | entire repo — sole session; also acted as the final integration session |

### File scope map (session A)

| Path | Purpose | Owner |
|---|---|---|
| `COORDINATION.md` | this file | A |
| `data/*.json` | all table data, one row per fact, each with a source and a status | A |
| `data/_schema.md` | row schema and the verification rule | A |
| `research/verification-log.md` | what was verified, from what document, and what was left blank | A |
| `tools/model.js` | deterministic projection and scenario engine | A |
| `tools/build.js` | renders 16 static pages from `data/*.json` into the repo root | A |
| `tools/check.js` | pre-publish checks (links, verified rows, blank rows, privacy scan) | A |
| `assets/`, generated `*.html` | presentation layer | A |

---

## Tasks

| # | Task | Status | Owner | Files |
|---|---|---|---|---|
| T1 | Coordination file, repo scaffold, privacy policy, build tooling | **done** | A | `COORDINATION.md`, `data/_schema.md`, `tools/` |
| T2 | Property profiles + property-tax history verification (95014 / 94122) | **done** | A | `data/properties.json`, `data/tax-history.json` |
| T3 | California property tax law: Prop 13 / 19 / 58, trust transfers, exclusions | **done** | A | `data/property-tax-law.json` |
| T4 | Insurance cost research | **done — nothing verifiable, flagged** | A | `data/insurance.json` |
| T5 | Utilities: water (Cupertino / SFPUC) + electricity (PG&E, solar NEM) | **done — SFPUC verified, PG&E flagged** | A | `data/utilities.json` |
| T6 | Inheritance & estate tax: federal, California, local; step-up basis; GST | **done** | A | `data/estate-tax.json` |
| T7 | Inherited-property process, step by step | **done** | A | `data/inheritance-process.json` |
| T8 | Rental income: SF rent control + AB 1482, net operating income | **done** | A | `data/rental.json` |
| T9 | Projections engine: values, taxes, costs, inflation (2026→2055) | **done** | A | `tools/model.js`, `data/assumptions.json` |
| T10 | Scenario model: live-in / rent / sell-and-reinvest | **done** | A | `tools/model.js` |
| T11 | Pending & proposed law changes | **done** | A | `data/law-changes.json` |
| T12 | Site build: landing dashboard + subpages by category | **done** | A | `tools/build.js`, `assets/`, 16 `*.html` |
| T13 | Verification pass: every row sourced, else blank + flagged | **done** | A | `tools/check.js`, `data/flagged.json`, `research/verification-log.md` |
| T14 | Integration, PR, merge, GitHub Pages deploy confirmation | **done** | A | — |

## Verification performed

`node tools/check.js` is the gate. It fails the build if any of the following is true:

- an internal link in a generated page does not resolve to a file that exists;
- a row marked `verified` has no `source_url`;
- a row marked `verified` has a blank value;
- a row marked `unverified` has **any** value (the never-infer rule);
- a generated page contains `undefined`, `NaN`, `[object Object]` or an unreplaced `${`;
- a generated page matches a street-address, APN, or SSN pattern (privacy scan).

Result at the end of this session: **16 pages, 167 rows checked, 97 verified, 25 owner-input,
45 intentionally blank, 0 errors, 0 warnings.**

The line-by-line evidence trail, with a verbatim quote for each primary source, is in
[`research/verification-log.md`](research/verification-log.md).

## Sources used

All primary. Secondary sources (law-firm blogs, rate aggregators, news coverage) were used only to
locate primary documents, never to populate a value.

| Publisher | Documents |
|---|---|
| Internal Revenue Service | Rev. Proc. 2025-32 §2.14; Estate tax (filing-threshold table); Pub. 551 *Basis of Assets* |
| California State Board of Equalization | Prop 19 page and filing checklist; LTA 2025/009; LTA 2026/026; Change-in-Ownership FAQ; Homeowners' Exemption |
| California Legislative Information | Revenue & Taxation Code §13302; Civil Code §1947.12 (AB 1482) |
| California Secretary of State | CC/ROV Memorandum #26138 (Prop 19 repeal initiative failed) |
| City and County of San Francisco | Board of Supervisors Resolution No. 447-25 (FY2025-26 tax rate); sf.gov Rent Board announcement 2026-01-14 |
| San Francisco Public Utilities Commission | Rate Schedules & Fees for Water and Sewer Service, FY2026-27 / FY2027-28 |
| County of Santa Clara, Office of the Assessor | Annual Report 2025 |
| City of Cupertino | Water page (three service providers) |
| California Department of Insurance | 2023 CA Property & Casualty Market Share |

Full list with per-document row counts is on the site's **Sources** page.

## Irregularities and open items

**19 open, 1 resolved during the build.** Published on the site's **Flagged for Review** page with
source links. None blocked the merge.

Highest-impact open items:

- **F1 (high, irregularity)** — Property S's owner-supplied figures imply a 2.13% effective rate
  against San Francisco's verified 1.18268325%. Unexplained; present in every year supplied.
- **F3 (high)** — Market rent for Property C, and rent for the freed Property S unit, are
  placeholders. Property C's rent is the pivot of the rent-versus-sell comparison.
- **F4 (high)** — Which net metering regime governs Property C's solar is unknown.
- **F5 (high)** — No insurance premium could be verified for either ZIP code.
- **F2 (medium, irregularity)** — Property C's implied effective rate (1.335%) sits above the range
  typically quoted for Santa Clara County (1.12–1.24%).

**Resolved:** F10 — the Homeowners' Exemption amount, now verified at $7,000 from the BOE.

## Headline result

Transfer assumed 2045, base case (4% appreciation, 1.33% effective Property C rate):

| | |
|---|---|
| Property C projected market value at transfer | $6,531,232 |
| Property tax today | $7,207 / yr |
| Property tax after transfer, heir moves in | $69,763 / yr |
| Property tax after transfer, rented out | $86,865 / yr |
| Net position at year 20 — live in | $7,168,260 |
| Net position at year 20 — rent | $10,052,372 |
| Net position at year 20 — **sell and reinvest** | **$17,335,884** |

**Recommendation: sell and reinvest.** It wins in every one of the twelve sensitivity runs on the
Scenarios page. The driver is that property acquired from a decedent takes a basis equal to fair
market value at death (IRS Pub 551), so selling soon after the transfer realises almost no taxable
gain, while holding converts the asset into a position that costs roughly $105,000–$122,000 a year
to carry.

## Handoff log

| Timestamp (UTC) | Session | Note |
|---|---|---|
| 2026-11-06 | A | Repo contained only `README.md`. GitHub Pages already enabled on `main` / root / legacy build. Created this file, claimed T1–T14. |
| 2026-11-06 | A | No other session branch existed; no contention encountered. No merge conflicts. |
| 2026-11-06 | A | T1–T13 complete. Committed data layer, then site layer. `tools/check.js` clean: 16 pages, 167 rows, 0 errors. |
| 2026-11-06 | A | T14: PR opened from `arena/56e7a5a3-cupertino3` to `main`, merged, Pages deploy confirmed. |

## Privacy rule (applies to every file in this repo)

No personal data (names, street addresses, APNs, trust names, account numbers) may appear in the
published site. Properties are referred to as **Property C** (Cupertino, ZIP 95014) and
**Property S** (San Francisco, ZIP 94122). ZIP codes and round-number market estimates are retained
because they are required for rate research and are not individually identifying. Any personal data
discovered during research stays in internal notes only and is never written into published output.

`tools/check.js` enforces this with a regex scan for street addresses, APNs and SSN-shaped
patterns across every generated page. If you spot personal information anywhere, remove it and note
the removal here.
