# Cupertino3

Anonymized analysis and GitHub Pages site comparing two ways of holding a home over 2040–2050:

- **Property A** — Cupertino, Santa Clara County, CA (to be inherited through [Trust] by [Beneficiary]).
- **Property B** — San Francisco, CA (held).

Covers property tax and assessment history (checked against BOE factors), insurance, water, electricity and solar, maintenance, federal / California / local law, the inheritance threshold, pending law changes, the live / rent / sell decision, and an inheritance process checklist.

**Published site:** this analysis is served by GitHub Pages at the `/docs/` path of the Pages site (the repository root hosts a separate dashboard from another session, which is left unchanged).

## Layout

| Path | What it is |
|------|-----------|
| `docs/` | The published site (static HTML, CSS, and downloadable CSV/JSON). |
| `data/` | Source register, user-supplied figures, law rows, cost rows, flags, process steps, projections. |
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
```

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
| `scripts/build_site.py` | Builds `guide/` from `data/guide/`. |
| `scripts/check_site.py` | Checks internal links, rows with official links, no external resources, verified rows have sources, privacy patterns. |

Rebuild:

```bash
python3 model/guide_project.py
python3 scripts/build_site.py
python3 scripts/check_site.py
```

Standard library only. Privacy rule: no personal information in the repo or site. Properties are referred to by city and county only. This is informational analysis, not legal or tax advice.
