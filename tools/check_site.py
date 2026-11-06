#!/usr/bin/env python3
"""Consistency and privacy checks for the site and data.

Checks:
  1. Every JSON file parses.
  2. Every table body row in docs/*.html has at least one link to an official domain.
  3. Every internal link in docs/*.html resolves to a file.
  4. Every flag and every cost/tax-law row cites a source ID that exists and has a URL.
  5. Privacy: no street addresses, ZIP codes, names, or the owner's location in repo text files.
Exit code 0 = pass, 1 = fail.
"""
import glob
import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
DATA = os.path.join(ROOT, "data")

OFFICIAL = ("boe.ca.gov", "irs.gov", "ftb.ca.gov", "lao.ca.gov", "arev.assembly.ca.gov", "insurance.ca.gov",
            "cfpnet.com", "cpuc.ca.gov", "sjwater.com", "sfpuc.gov", "bls.gov", "federalreserve.gov",
            "sf.gov", "santaclaracounty.gov", "sos.ca.gov", "congress.gov", "huduser.gov", "leginfo.legislature.ca.gov")

# Privacy patterns (repo-wide). Conservative: only things that would identify the owner or a property.
PRIVACY = {
    "street address": re.compile(r"\b\d{1,5}\s+(?:[NSEW]\.?\s+)?[A-Z][a-zA-Z]+\s+(?:Ave|Avenue|St|Street|Rd|Road|Blvd|Boulevard|Dr|Drive|Way|Ln|Lane|Ct|Court|Pl|Place|Terrace|Circle|Loop|Parkway|Pkwy)\b"),
    "ZIP code (CA range)": re.compile(r"(?:\bCA\b|California)[ ,]+9[0-6]\d{3}\b|\b9[0-6]\d{3}\b(?=\s*(?:<|\)|,\s*(?:CA|California)))"),
    "owner handle": re.compile(r"ginny|mcfiner", re.I),
    "owner location": re.compile(r"Naaldwijk|South Holland|Netherlands|\bNL\b|Zuid-Holland", re.I),
    "email address": re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"),
}


class TableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_tbody = False
        self.rows = []          # list of row dicts: {"links": [...], "text": ...}
        self.cur = None
        self.links_in_row = []
        self.depth_tr = 0
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "tbody":
            self.in_tbody = True
        if tag == "tr" and self.in_tbody:
            self.cur = {"links": []}
        if tag == "a" and "href" in a:
            self.hrefs.append(a["href"])
            if self.cur is not None:
                self.cur["links"].append(a["href"])

    def handle_endtag(self, tag):
        if tag == "tbody":
            self.in_tbody = False
        if tag == "tr" and self.cur is not None:
            self.rows.append(self.cur)
            self.cur = None


def domain_ok(url):
    m = re.match(r"https?://([^/]+)/", url)
    if not m:
        return False
    host = m.group(1).lower()
    return any(host == d or host.endswith("." + d) for d in OFFICIAL)


def check_json(problems):
    n = 0
    for path in glob.glob(os.path.join(DATA, "*.json")) + glob.glob(os.path.join(DOCS, "data", "*.json")):
        try:
            with open(path) as f:
                json.load(f)
            n += 1
        except Exception as exc:  # noqa: BLE001
            problems.append(f"JSON parse error {path}: {exc}")
    return n


def check_html(problems):
    files = sorted(glob.glob(os.path.join(DOCS, "*.html")))
    total_rows = 0
    for path in files:
        text = open(path, encoding="utf-8").read()
        p = TableParser()
        p.feed(text)
        for i, row in enumerate(p.rows):
            total_rows += 1
            if not any(domain_ok(u) for u in row["links"]):
                problems.append(f"{os.path.basename(path)}: table body row {i+1} has no official-domain link")
        for href in p.hrefs:
            if href.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = os.path.normpath(os.path.join(DOCS, href.split("#")[0]))
            if href.split("#")[0] and not os.path.exists(target):
                problems.append(f"{os.path.basename(path)}: broken internal link {href}")
    return len(files), total_rows


def check_sources(problems):
    srcs = {s["id"]: s for s in json.load(open(os.path.join(DATA, "sources.json")))["sources"]}
    for s in srcs.values():
        if not s.get("url"):
            problems.append(f"source {s['id']} has no URL")
    checks = [("flags.json", "flags"), ("cost_inputs.json", "rows"), ("tax_law.json", None), ("process_steps.json", "steps")]
    count = 0
    for fname, key in checks:
        data = json.load(open(os.path.join(DATA, fname)))
        items = []
        if key:
            items = data[key]
        else:
            for k, v in data.items():
                if isinstance(v, list):
                    items.extend(v)
        for it in items:
            count += 1
            ids = it.get("source_ids", [])
            url = it.get("source_url")
            if not ids and not url:
                problems.append(f"{fname}: item {it.get('id', it.get('topic', '?'))} has no source")
            for sid in ids:
                if sid not in srcs:
                    problems.append(f"{fname}: unknown source id {sid}")
            if url and not domain_ok(url):
                problems.append(f"{fname}: item {it.get('id')} source_url is not an official domain: {url}")
    return count


def check_privacy(problems):
    scanned = 0
    targets = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in (".git", "__pycache__")]
        for fn in filenames:
            if fn.endswith((".py", ".json", ".html", ".css", ".md", ".csv", ".txt")):
                targets.append(os.path.join(dirpath, fn))
    for path in targets:
        rel = os.path.relpath(path, ROOT)
        if rel == os.path.join("tools", "check_site.py"):
            continue  # this file lists the patterns
        scanned += 1
        text = open(path, encoding="utf-8", errors="ignore").read()
        for label, pat in PRIVACY.items():
            for m in pat.finditer(text):
                if label == "ZIP code (CA range)":
                    # ignore numbers that are part of currency or a larger number
                    start, end = m.span()
                    if (start > 0 and text[start - 1] in "$,.0123456789") or (end < len(text) and text[end] in ",.0123456789"):
                        continue
                problems.append(f"privacy: {label} pattern '{m.group(0)}' in {rel}")
    return scanned


def main():
    problems = []
    n_json = check_json(problems)
    n_pages, n_rows = check_html(problems)
    n_items = check_sources(problems)
    n_files = check_privacy(problems)
    print(f"JSON files parsed: {n_json}")
    print(f"HTML pages checked: {n_pages}; table body rows checked: {n_rows}")
    print(f"Data items checked for sources: {n_items}")
    print(f"Repository text files scanned for privacy: {n_files}")
    if problems:
        print(f"FAIL: {len(problems)} problem(s)")
        for p in problems[:200]:
            print(" -", p)
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
