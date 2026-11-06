# Cupertino3

Decision-support dashboard for a planned California property inheritance in the 2040–2050 window:
one house to be inherited in Cupertino (ZIP 95014) and one currently owned three-unit building in
San Francisco (ZIP 94122).

Live site: **https://ginnymcfiner23-ux.github.io/Cupertino3/**

## What it does

- Collects the **verified** property tax, estate tax, insurance, utility and rental rules that govern
  the decision, each linked to the official document it was read from.
- Projects property values, assessed values, property tax, carrying costs and the federal estate tax
  exclusion from 2026 to 2055.
- Models three options — live in the inherited house, rent it, or sell it and reinvest — and compares
  them over a twenty-year horizon, with a twelve-run sensitivity table.
- Publishes everything that could **not** be verified on a Flagged for Review page, with source links.

## The verification rule

> If a value cannot be confirmed from an official source, leave it blank and flag it as unverified.
> Never infer or fill in values.

A row is published as **Verified** only if it was read directly off an official government, agency or
utility document, and the row links to that document. Secondary sources (law-firm blogs, rate
aggregators, news coverage) are used only to *locate* primary documents, never to populate a value.

`node tools/check.js` enforces this and fails the build if:
- an internal link is broken,
- a `verified` row has no source URL or a blank value,
- an `unverified` row carries any value at all,
- a page contains `undefined`, `NaN`, `[object Object]` or an unreplaced `${`,
- a page matches a street-address, APN or SSN pattern (privacy scan).

## Layout

```
data/           one JSON file per topic; one row per fact, each with source + status
research/       verification log: what was checked, against what, and what was left blank
tools/model.js  deterministic projection and scenario engine
tools/build.js  renders 16 static pages from data/*.json into the repo root
tools/check.js  pre-publish verification gate
assets/         CSS and a small amount of progressive-enhancement JS
*.html          generated output, committed so GitHub Pages needs no build step
```

## Rebuilding

```sh
node tools/build.js   # regenerate *.html from data/*.json
node tools/check.js   # verify before publishing
```

No dependencies, no network access required to build. Node only.

## Privacy

No personal information is published. Properties are referred to as **Property C** (Cupertino, 95014)
and **Property S** (San Francisco, 94122). ZIP codes and round-number market estimates are retained
because rate research requires them and neither is individually identifying. Names, street addresses,
assessor parcel numbers, trust names and tenant details are never recorded.

## Not advice

This is a research dashboard, not tax, legal or investment advice. Every projection on the site is
labelled as such and depends on assumptions listed on the Methodology page.
