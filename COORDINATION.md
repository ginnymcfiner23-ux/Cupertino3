# COORDINATION.md — Shared Task Board

Repo: `ginnymcfiner23-ux/Cupertino3`
Live site (after integration): https://ginnymcfiner23-ux.github.io/Cupertino3/

## How this session handles branch scope

Arena pins this session to the branch **`arena/56e7a5a3-cupertino3`** and forbids creating/switching to
other branches. The coordination protocol asks for per-task branches named `session-<id>/<task>`.
To satisfy both, this session uses **directory-level file scopes inside the single session branch**
instead of separate branches. No other session branch exists in the remote (`git branch -a` shows only
`main` and this branch), so there is no live contention. If a second session appears, it must append its
claims below and respect the listed scopes — do not edit files inside another session's scope.

| Session ID | Branch | Scope |
|---|---|---|
| `arena/56e7a5a3-cupertino3` (session A, integration session) | `arena/56e7a5a3-cupertino3` | entire repo (sole session; integration done by same session) |

---

## Tasks

Status values: `unclaimed` · `in progress` · `needs review` · `done`

| # | Task | Status | Owner session | Files touched |
|---|---|---|---|---|
| T1 | Coordination file, repo scaffold, privacy policy, build tooling | done | A | `COORDINATION.md`, `README.md`, `tools/`, `data/_schema.md` |
| T2 | Property profiles + property-tax history verification (Cupertino 95014 / SF 94122) | in progress | A | `research/01-property-profiles.md`, `data/cupertino-tax-history.json`, `data/sf-tax-history.json` |
| T3 | California property tax law: Prop 13 / 19 / 58, trust transfers, parent–child exclusion | in progress | A | `research/02-property-tax-law.md`, `data/property-tax-law.json` |
| T4 | Insurance cost research (Cupertino owner-occupied, SF 94122 rental/3-unit) | in progress | A | `research/03-insurance.md`, `data/insurance.json` |
| T5 | Utilities: water (Cupertino / SFPUC) + electricity (PG&E, solar NEM) | in progress | A | `research/04-utilities.md`, `data/utilities.json` |
| T6 | Inheritance & estate tax: federal (IRS/OBBBA), California, local; step-up basis; GST | in progress | A | `research/05-estate-tax.md`, `data/estate-tax.json` |
| T7 | Inherited-property process, step by step (trust administration → reassessment) | in progress | A | `research/06-inheritance-process.md`, `data/inheritance-process.json` |
| T8 | Rental income: SF rent control + AB 1482, net operating income | in progress | A | `research/07-rental.md`, `data/rental.json` |
| T9 | Projections engine: values, taxes, costs, inflation (2026→2055) | in progress | A | `research/08-projections.md`, `data/projections.json`, `data/assumptions.json` |
| T10 | Scenario model: live-in / rent / sell-and-reinvest (after tax) | in progress | A | `research/09-scenarios.md`, `data/scenarios.json` |
| T11 | Pending & proposed law changes (federal + California + local) | in progress | A | `research/10-law-changes.md`, `data/law-changes.json` |
| T12 | Site build: landing dashboard + subpages by category | in progress | A | `site/`, generated `*.html`, `assets/` |
| T13 | Verification pass: every table row has an official source link, else blank + flagged | in progress | A | `data/flagged.json`, `site/flagged-for-review.html` |
| T14 | Integration, PR #, merge, GitHub Pages deploy confirmation | unclaimed | A | — |

## Handoff log

| Timestamp (UTC) | Session | Note |
|---|---|---|
| 2026-11-06 | A | Repo contained only `README.md`. Pages already enabled, `main` / root, legacy build. Created this file, claimed T1–T13. |

## Privacy rule (applies to every file in this repo)

No personal data (names, street addresses, APNs, trust names, account numbers, exact assessed
values tied to an owner) may appear in the published site. Properties are referred to as
**Property C** (Cupertino, ZIP 95014) and **Property S** (San Francisco, ZIP 94122). ZIP codes and
round-number market estimates are retained because they are required for rate research and are not
individually identifying. Any personal data discovered during research stays in internal notes only
and is never written into `site/` output.
