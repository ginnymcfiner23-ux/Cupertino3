# Data schema

Every table row in `data/*.json` uses the same shape. The site renders each row with its
source link and a verification badge.

| Field | Meaning |
|---|---|
| `id` | Stable slug, unique within the file |
| `label` | Human-readable row label |
| `value` | The value. **Empty string means "could not be verified — intentionally blank."** |
| `unit` | `USD`, `USD/yr`, `USD/mo`, `percent`, `count`, `date`, `text`, `step` |
| `period` | The year or period the value applies to |
| `source_name` | Publisher of the source (IRS, BOE, SFPUC…) |
| `source_url` | Deep link to the official document. Empty for owner-supplied or assumption rows. |
| `status` | One of the four values below |
| `note` | Caveat, method, or cross-reference |

## `status` values

| Status | Badge | Rule |
|---|---|---|
| `verified` | Verified | Value read directly off an official government/agency document linked in `source_url`. |
| `owner-input` | Owner input | Supplied by the project owner from private records. Not publicly verifiable. Never published with identifying detail. |
| `projection` | Projection | Model output. Built only from `verified` or `owner-input` inputs plus the stated assumptions on the Methodology page. Not a fact. |
| `unverified` | Unverified | **Value is intentionally blank.** No official source could be located during this pass. |

## Rule applied throughout

> If a value cannot be confirmed from an official source, leave it blank and flag it as
> unverified. Never infer or fill in values.

Secondary sources (law-firm blogs, rate-aggregator sites) are **never** used to populate a
`value`. They may appear in a `note` only as a suggestion for follow-up, with the value left
blank and the status `unverified`.

## Privacy rule

No row may contain a name, street address, assessor parcel number, trust name, or account
number. Properties are `Property C` (Cupertino, ZIP 95014) and `Property S`
(San Francisco, ZIP 94122). ZIP codes are retained because water, utility, and rate research
requires them and a ZIP is not individually identifying.
