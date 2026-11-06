"""Validate the built guide site (guide/) and the data behind it (data/guide/).

Checks:
  1. Every <tbody> row in every table contains at least one link.
  2. Every internal link resolves to a file in guide/.
  3. No external CDN / remote resources (stylesheets, scripts, images, fonts, @import).
  4. Every VERIFIED data row cites source IDs that exist; UNVERIFIED rows have blank values.
  5. Privacy scan: flags ZIP-like numbers, APN-like patterns, and personal location words.
Exit code 1 on any failure.
"""
import glob, json, os, re, sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "guide")
fail = []


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_tbody = False
        self.row_has_link = None
        self.rows = []          # (has_link)
        self.links = []
        self.remote = []
        self.in_row = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "tbody":
            self.in_tbody = True
        if tag == "tr" and self.in_tbody:
            self.in_row = True
            self.row_has_link = False
        if tag == "a" and "href" in a:
            self.links.append(a["href"])
            if self.in_row:
                self.row_has_link = True
        if tag == "link" and a.get("rel", "").lower() == "stylesheet":
            self.remote.append(("link", a.get("href")))
        if tag in ("script", "img", "iframe", "source", "video", "audio") and a.get("src", "").startswith(("http", "//")):
            self.remote.append((tag, a.get("src")))
        if tag == "script" and "src" in a:
            self.remote.append(("script", a["src"]))

    def handle_endtag(self, tag):
        if tag == "tbody":
            self.in_tbody = False
        if tag == "tr" and self.in_row:
            self.rows.append(self.row_has_link)
            self.in_row = False


pages = sorted(glob.glob(os.path.join(DOCS, "*.html")))
if not pages:
    fail.append("no pages in guide/")
for pg in pages:
    name = os.path.basename(pg)
    text = open(pg, encoding="utf-8").read()
    p = P()
    p.feed(text)
    bad_rows = [i for i, ok in enumerate(p.rows) if not ok]
    if bad_rows:
        fail.append(f"{name}: {len(bad_rows)} table body rows without any link (first index {bad_rows[0]})")
    for href in p.links:
        if href.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target = os.path.join(DOCS, href.split("#")[0])
        if href and not os.path.exists(target):
            fail.append(f"{name}: broken internal link {href}")
    for kind, val in p.remote:
        fail.append(f"{name}: external resource <{kind}> {val}")
    if re.search(r"@import|url\(\s*['\"]?https?:", text):
        fail.append(f"{name}: remote CSS import/url")
    # privacy scan
    for pat, label in [(r"\b9[0-9]{4}\b(?!\d)", "ZIP-like number"), (r"\b\d{3}-\d{3}-\d{3}\b", "APN-like pattern"),
                       (r"Naaldwijk|Netherlands|\bNL\b", "location of client"), (r"\bAPN\b", "APN mention")]:
        for m in re.finditer(pat, re.sub(r"<[^>]+>", " ", text)):
            ctx = text[max(0, m.start() - 40): m.end() + 40].replace("\n", " ")
            # ignore pure currency amounts like $95,000 and sources text containing years/versions
            if label == "ZIP-like number" and re.search(r"\$|\d,\d", ctx):
                continue
            if label == "ZIP-like number" and re.search(r"VersionId|Rate Book|tax-rate|rp-25|\.pdf|\.htm|%|/\d", ctx):
                continue
            fail.append(f"{name}: privacy scan {label}: '{m.group(0)}' in ...{ctx}...")

# data checks
sources = {s["id"] for s in json.load(open(os.path.join(ROOT, "data/guide/sources.json")))["sources"]}
facts = json.load(open(os.path.join(ROOT, "data/guide/facts.json")))["rows"]
for r in facts:
    if r["status"] == "VERIFIED":
        if not r["sources"]:
            fail.append(f"fact {r['id']} VERIFIED without source")
        if not r["value"]:
            fail.append(f"fact {r['id']} VERIFIED but value blank")
    else:
        if r["value"]:
            fail.append(f"fact {r['id']} UNVERIFIED but has a value (must be blank)")
    for s in r["sources"]:
        if s not in sources:
            fail.append(f"fact {r['id']} cites unknown source {s}")
for f in glob.glob(os.path.join(ROOT, "data/guide/*.json")):
    for s in re.findall(r'"S\d\d"', open(f).read()):
        if s.strip('"') not in sources:
            fail.append(f"{os.path.basename(f)} cites unknown source {s}")

if fail:
    print("FAIL:")
    for x in fail[:200]:
        print(" -", x)
    print(f"{len(fail)} problems")
    sys.exit(1)
print(f"OK: {len(pages)} pages, {len(facts)} facts, {len(sources)} sources; no problems found")
