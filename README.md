# Cupertino3 — Cupertino & San Francisco House Inheritance Decision

Decision-support project for inheriting two California houses (Cupertino 95014 and
San Francisco 94122) through a trust around 2040–2050, with a live GitHub Pages
dashboard.

## What's here

- `docs/` — the live dashboard site (GitHub Pages, deployed from `/docs` on `main`)
  - `index.html` — Executive Summary
  - `properties.html` — property & tax data with irregularities
  - `tax-law.html` — verified law & tax research with official sources
  - `inheritance.html` — step-by-step inheritance process
  - `projections.html` — 2026–2055 projections (values, taxes, estate exemption)
  - `costs.html` — utilities, insurance, maintenance
  - `scenarios.html` — live / rent / sell decision analysis + recommendation
  - `flagged.html` — unverified values and irregularities for review
  - `sources.html` — full source list
- `data/` — verified research notes and `projections.json` (projection engine output)
- `scripts/` — `projections.py` (engine) and `build_site.py` (site builder)
- `COORDINATION.md` — task board and verification log

## Rebuild the site

```bash
python3 scripts/projections.py   # writes data/projections.json
python3 scripts/build_site.py    # writes docs/*.html
```

## Privacy

No personal information appears in this product. All user-provided figures are
anonymized placeholders and are flagged for verification on the Flagged for Review
page.
