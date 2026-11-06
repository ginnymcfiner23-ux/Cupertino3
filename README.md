# Cupertino3

Source-linked inheritance decision guide for two properties:

- **Property A** - Cupertino, Santa Clara County, CA (primary residence)
- **Property B** - San Francisco, CA (rental with an owner-occupied unit)

The site is published from `docs/` with GitHub Pages.

## Layout

| Path | Contents |
|---|---|
| `docs/` | Generated static site (HTML, inline styles, no external resources). |
| `data/facts.json` | Verified and unverified rows. Each row lists its official source IDs. |
| `data/sources.json` | Source register: publisher, URL, tier, and how it was checked. |
| `data/assumptions.json` | Client inputs (UNVERIFIED) and model assumptions (labelled). |
| `data/property_tax_history.json` | Client-provided tax history (UNVERIFIED; verified column blank). |
| `data/irregularities.json` | Flagged for Review items. |
| `data/legislation.json` | Pending and recent law watchlist. |
| `data/inheritance_steps.json` | Step-by-step inheritance process. |
| `data/projections.json`, `data/projections/*.csv` | Model output (generated). |
| `model/project.py` | Projection model (2026-2050, inheritance year sensitivity). |
| `scripts/build_site.py` | Builds `docs/` from `data/` and `model/` output. |
| `scripts/check_site.py` | Checks links, rows with sources, external resources, and privacy patterns. |
| `COORDINATION.md` | Parallel-session task board and log. |

## Rebuild

```bash
python3 model/project.py
python3 scripts/build_site.py
python3 scripts/check_site.py
```

Python 3 standard library only.

## Rules followed

- Verified values come from official sources (.gov, state legislature, BOE, county, utilities, IRS). Every verified row links to its source.
- Values that could not be confirmed are left blank and flagged UNVERIFIED.
- Client-provided numbers are used only as labelled inputs to projections.
- Projections are labelled as projections and list their assumptions.
- No personal information is stored in this repository or on the site. Properties are referred to by city and county only. No parcel numbers, names, addresses, or ZIP codes.

This is informational analysis, not legal or tax advice.
