# Cupertino3

Anonymized analysis and GitHub Pages site comparing two ways of holding a home over 2040–2050:

- **Property A** — Cupertino, Santa Clara County, CA (to be inherited through [Trust] by [Beneficiary]).
- **Property B** — San Francisco, CA (held).

Covers property tax and assessment history (checked against BOE factors), insurance, water, electricity and solar, maintenance, federal / California / local law, the inheritance threshold, pending law changes, the live / rent / sell decision, and an inheritance process checklist.

**Published sites (one GitHub Pages site, two analyses):**

- **Root site** (`index.html` and folders `facts/`, `property/`, `costs/`, `projections/`, `decision/`, `process/`, `law/`, `flagged/`, `sources/`, shared `assets/`). Built by `scripts/build_site.py` from `data/ia/*.json`. Checked by `scripts/validate.py`. Session c1b5796b.
- **`/docs/` site** (`docs/`). Built by `tools/build_site.py` from `data/*.json`. Checked by `tools/check_site.py`. Session 340c906c.

The two analyses use different assumptions and do not yet agree on every figure. Neither is verified; both are labelled as assumption-based projections. See FL-25 on the root site's Flagged for Review page and the cross-session note in `COORDINATION.md`. The earlier dashboard (session aed145d8) is archived unchanged in `archive/previous-dashboard/`.

## Layout

| Path | What it is |
|------|-----------|
| `docs/` | The published site (static HTML, CSS, and downloadable CSV/JSON). |
| `data/` | Files for the `/docs/` site (session 340c906c): sources, tax law, cost inputs, flags, process steps, projections. |
| `data/ia/` | Files for the root site (session c1b5796b): sources, facts, client inputs, history, flags, projections. |
| `scripts/model.py` | Projection model for the root site. Writes `data/ia/projections.json`. |
| `scripts/build_site.py` | Generates the root site from `data/ia/`. |
| `scripts/validate.py` | Checks the root site: sourcing, links, personal-information scan, projection sanity. |
| `index.html`, category folders | The root site (landing page and category pages). |
| `model/project.py` | Projection model. Writes `data/projections.json`. All assumptions are labelled. |
| `tools/build_data.py` | Builds the property tax history and BOE factor checks from the user tables. |
| `tools/build_site.py` | Generates `docs/` from `data/`. No numbers are typed into the HTML by hand. |
| `tools/check_site.py` | Checks: JSON parses; every table row links to an official domain; internal links resolve; every flag and row cites a source; privacy patterns absent. |
| `COORDINATION.md` | Task board and session log. |

## Rebuild

```bash
python3 tools/build_data.py
python3 model/project.py
python3 tools/build_site.py
python3 tools/check_site.py
python3 scripts/model.py
python3 scripts/build_site.py
python3 scripts/validate.py
```

Root site: `scripts/model.py` → `scripts/build_site.py` → `scripts/validate.py`.

Standard library only; no packages to install.

## Status rules

- **Verified**: read from an official page. **Partly verified**: official URL or partial read. **Pending**: identified, not read, not used. **UNVERIFIED / user figure**: supplied by the owner; blank in verified columns and used only in labelled projections. **Assumption**: a model input, not a fact.
- Anything not verified is left blank and listed on the *Flagged for Review* page. Flagged items do not block publication.

## Privacy

Only the anonymized references above are used. No names, addresses, ZIP codes or the owner's location appear in the repository, and `tools/check_site.py` enforces this. This is not legal, tax or investment advice.

---

## Inheritance decision guide (session 64308d3a)

A second, separate analysis lives in `guide/` (served at `/guide/` of the same Pages site). It covers the same two properties with a different scope: verified facts with official links (`data/guide/facts.json`), client inputs (UNVERIFIED, labelled), a 2026-2050 projection model (`model/guide_project.py`), inheritance steps, pending law, and a Flagged for Review page. Unverified values are blank.

| Path | What it is |
|---|---|
| `guide/` | Generated static site: landing page, category pages, Flagged for Review, sources. Inline styles; no external resources. |
| `data/guide/` | Facts, sources, client inputs, irregularities, legislation, inheritance steps, projections. |
| `model/guide_project.py` | Projection model. Writes `data/guide/projections.json` and CSVs. |
| `scripts/guide_build_site.py` | Builds `guide/` from `data/guide/`. |
| `scripts/guide_check_site.py` | Checks internal links, rows with official links, no external resources, verified rows have sources, privacy patterns. |

Rebuild:

```bash
python3 model/guide_project.py
python3 scripts/guide_build_site.py
python3 scripts/guide_check_site.py
```

Standard library only. Privacy rule: no personal information in the repo or site. Properties are referred to by city and county only. This is informational analysis, not legal or tax advice.

---

## Verified-rules dashboard (session `arena/56e7a5a3-cupertino3`)

A fourth, separate analysis lives in `dashboard/` (served at `/dashboard/` of the same Pages site).
It is built around a strict verification rule: **a row is published as Verified only if it was read
directly off an official government, agency or utility document, and the row links to that
document.** Anything that could not be confirmed is left blank and listed on the Flagged for Review
page. Secondary sources were used only to locate primary documents, never to populate a value.

| Path | What it is |
|---|---|
| `dashboard/` | Generated static site: 16 pages — landing dashboard, category pages, projections, scenarios, Flagged for Review, sources, methodology, privacy. |
| `data/dashboard/` | One JSON file per topic; one row per fact, each with `source_name`, `source_url` and a status of `verified` / `owner-input` / `projection` / `unverified`. |
| `research/dashboard-verification-log.md` | What was verified, from what document, with the verbatim text or table read — plus everything deliberately left blank and why. |
| `tools/dashboard_model.js` | Deterministic projection and scenario engine. |
| `tools/dashboard_build.js` | Renders `dashboard/` from `data/dashboard/`. |
| `tools/dashboard_check.js` | Pre-publish gate (links, verified rows have sources, unverified rows are blank, no template artefacts, privacy scan). |

Rebuild:

```bash
node tools/dashboard_build.js
node tools/dashboard_check.js
```

Node only, no dependencies, no network access required to build.

Result at the end of the session: **16 pages, 167 rows checked, 97 verified, 25 owner-input,
45 intentionally blank, 0 errors.** 19 items remain open on the Flagged for Review page; 1 was
resolved during the build.

**Headline: sell and reinvest**, in all twelve sensitivity runs. Property acquired from a decedent
takes a basis equal to fair market value at death (IRS Pub 551), so selling soon after transfer
realises almost no taxable gain, while holding costs roughly $105k–$122k a year to carry after
reassessment.

Privacy: no ZIP codes are recorded anywhere, matching the convention the other sessions adopted.
Properties are referred to as **Property A** (Cupertino, Santa Clara County, CA) and
**Property B** (San Francisco, CA).
