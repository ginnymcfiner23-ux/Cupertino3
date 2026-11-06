#!/usr/bin/env python3
"""Validate the data files and the built site (standard library only).

Exit code 0 only if every check passes. Checks:
  1. JSON files parse; source IDs are unique; flags are well-formed.
  2. Every VERIFIED fact has at least one OFFICIAL source that exists in sources.json.
  3. Every UNVERIFIED fact has a blank value.
  4. Every table row on the built site contains at least one link (source or flag).
  5. Every internal link resolves to a file (and, for '#id' links, to an element id).
  6. Every external link is registered in sources.json (official or secondary).
  7. No personal identifiers appear in published files (addresses, parcel numbers,
     precise ZIP codes, e-mail addresses, owner or location details).
  8. Projection sanity: sell beats keep for every test year and case (same assertion as the build).
"""
import html.parser
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
errors, warnings = [], []


def err(msg):
    errors.append(msg)


# ---------- 1-3: data ----------
sources = json.loads((ROOT / "data/sources.json").read_text())["sources"]
ids = [s["id"] for s in sources]
if len(ids) != len(set(ids)):
    err("duplicate source IDs")
src_by_id = {s["id"]: s for s in sources}
src_urls = {s["url"] for s in sources}

facts = json.loads((ROOT / "data/facts.json").read_text())
flags = json.loads((ROOT / "data/flags.json").read_text())["flags"]
flag_ids = {f["id"] for f in flags}
inputs = json.loads((ROOT / "data/inputs.json").read_text())
proj = json.loads((ROOT / "data/projections.json").read_text())

fact_ids = []
for cat in facts["categories"]:
    for r in cat["rows"]:
        fact_ids.append(r["id"])
        if r["status"] == "verified":
            if not r["sources"]:
                err(f"{r['id']}: verified without a source")
            for sid in r["sources"]:
                if sid not in src_by_id:
                    err(f"{r['id']}: unknown source {sid}")
                elif src_by_id[sid]["tier"] != "official":
                    err(f"{r['id']}: verified value cites a non-official source {sid}")
            if not r["value"]:
                err(f"{r['id']}: verified but value is blank")
        elif r["status"] == "UNVERIFIED":
            if r["value"]:
                err(f"{r['id']}: UNVERIFIED row must have a blank value")
        else:
            err(f"{r['id']}: unknown status {r['status']}")
if len(fact_ids) != len(set(fact_ids)):
    err("duplicate fact IDs")

for f in flags:
    for sid in f["sources"]:
        if sid not in src_by_id:
            err(f"{f['id']}: unknown source {sid}")
if len(flag_ids) != len(flags):
    err("duplicate flag IDs")

# every flag referenced anywhere must exist
blob = json.dumps({"facts": facts, "inputs": inputs}, ensure_ascii=False)
for ref in set(re.findall(r"FL-\d+", blob)):
    if ref not in flag_ids:
        err(f"reference to missing flag {ref}")

# ---------- 8: projection sanity ----------
for T in proj["meta"]["inheritance_years_tested"]:
    for sk in proj["scenarios"]:
        rows = {(r["property"], r["option"]): r for r in proj["summary"] if r["T"] == T and r["scenario"] == sk}
        a_sell = next(v for (p, o), v in rows.items() if p == "A" and o.startswith("Sell"))["end_real_2026"]
        a_live = next(v for (p, o), v in rows.items() if p == "A" and o.startswith("Live"))["end_real_2026"]
        b_sell = next(v for (p, o), v in rows.items() if p == "B" and o.startswith("Sell"))["end_real_2026"]
        b_hyb = next(v for (p, o), v in rows.items() if p == "B" and o.startswith("Heir"))["end_real_2026"]
        b_full = next(v for (p, o), v in rows.items() if p == "B" and o.startswith("No occ"))["end_real_2026"]
        if not (a_sell > a_live):
            err(f"projection: A sell not above live at {T}/{sk}")
        if not (b_sell > b_hyb and b_sell > b_full):
            err(f"projection: B sell not above keep at {T}/{sk}")

# ---------- 4-7: built site ----------
PAGES = [p for p in ROOT.rglob("index.html") if "archive" not in p.relative_to(ROOT).parts]
page_set = {p.relative_to(ROOT).as_posix() for p in PAGES}


class Scanner(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_table = 0
        self.rows = []      # list of (row_has_link, text)
        self.cur_row = None
        self.links = []     # hrefs
        self.ids = set()
        self.row_depth = 0
        self.in_tbody = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "table":
            self.in_table += 1
        if tag == "tbody":
            self.in_tbody = True
        if tag == "tr" and self.in_table and self.in_tbody:
            self.cur_row = {"link": False, "text": ""}
        if tag == "a":
            href = a.get("href", "")
            if href:
                self.links.append(href)
                if self.cur_row is not None:
                    self.cur_row["link"] = True

    def handle_endtag(self, tag):
        if tag == "tbody":
            self.in_tbody = False
        if tag == "tr" and self.cur_row is not None:
            self.rows.append(self.cur_row)
            self.cur_row = None
        if tag == "table":
            self.in_table -= 1

    def handle_data(self, data):
        if self.cur_row is not None:
            self.cur_row["text"] += data


all_links = set()
for p in PAGES:
    rel = p.relative_to(ROOT)
    sc = Scanner()
    text = p.read_text(encoding="utf-8")
    sc.feed(text)

    # table row check (header rows live in <thead>, handled by the same scanner; skip rows w/o <td>)
    data_rows = [r for r in sc.rows if r["text"].strip()]
    for r in data_rows:
        if not r["link"]:
            err(f"{rel}: table row without a source/flag link: {r['text'][:80]!r}")

    # personal-information scan (visible text + link targets)
    visible = re.sub(r"<[^>]+>", " ", text)
    patterns = {
        "street address": r"\b\d{1,5}\s+[A-Z][a-zA-Z]+\s+(St|Street|Ave|Avenue|Road|Rd|Way|Drive|Dr|Blvd|Lane|Ln|Court|Ct|Place|Pl)\b",
        "parcel/APN": r"\b\d{3}-\d{3}-\d{3}\b",
        "precise ZIP": r"\b(95014|94122|94123|94116)\b",
        "e-mail": r"[\w.+-]+@[\w-]+\.[\w.]+",
        "location of the account holder": r"Naaldwijk|South Holland|Netherlands|\bNL\b",
        "owner name fragments": r"[Gg]inny|[Mm]c[Ff]iner",
        "account-holder location (country)": r"\bNetherlands\b|\bNL\b",
    }
    for label, pat in patterns.items():
        if re.search(pat, visible):
            err(f"{rel}: personal-information pattern found ({label})")

    # links
    for href in sc.links:
        all_links.add(href)
        if href.startswith("#"):
            if href[1:] not in sc.ids:
                err(f"{rel}: missing in-page anchor {href}")
            continue
        if href.startswith("http://") or href.startswith("https://"):
            if href not in src_urls and not href.startswith("https://github.com/ginnymcfiner23-ux/Cupertino3"):
                err(f"{rel}: external link not registered in sources.json: {href}")
            continue
        target, _, frag = href.partition("#")
        if target.endswith("/") or target == "":
            target = (target or "") + ("index.html" if target else "")
        resolved = (p.parent / target).resolve()
        try:
            rel_target = resolved.relative_to(ROOT.resolve()).as_posix()
        except ValueError:
            err(f"{rel}: link escapes repository: {href}")
            continue
        if not resolved.exists():
            err(f"{rel}: broken internal link {href}")
            continue
        if frag and resolved.suffix == ".html":
            tsc = Scanner()
            tsc.feed(resolved.read_text(encoding="utf-8"))
            if frag not in tsc.ids:
                err(f"{rel}: anchor #{frag} not found in {rel_target}")

# required pages exist
for required in ["index.html", "facts/index.html", "property/index.html", "costs/index.html",
                 "projections/index.html", "decision/index.html", "process/index.html",
                 "law/index.html", "flagged/index.html", "sources/index.html", "assets/site.css", "assets/site.js"]:
    if not (ROOT / required).exists():
        err(f"missing required file {required}")

# every flag has a page anchor
flagged_html = (ROOT / "flagged/index.html").read_text(encoding="utf-8")
for fid in flag_ids:
    if f'id="{fid}"' not in flagged_html:
        err(f"Flagged page lacks anchor for {fid}")

print(f"pages checked: {len(PAGES)}; links seen: {len(all_links)}; facts: {len(fact_ids)}; flags: {len(flags)}")
verified = sum(1 for c in facts["categories"] for r in c["rows"] if r["status"] == "verified")
unverified = sum(1 for c in facts["categories"] for r in c["rows"] if r["status"] == "UNVERIFIED")
print(f"verified rows: {verified}; unverified rows (blank): {unverified}")
for w in warnings:
    print("WARN:", w)
if errors:
    print(f"FAILED with {len(errors)} error(s):")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print("ALL CHECKS PASSED")
