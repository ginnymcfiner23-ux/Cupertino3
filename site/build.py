#!/usr/bin/env python3
"""Assemble the static site: site/src/*.html -> repo root (index.html + pages/).
Shared header/nav/footer; no external dependencies."""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "site" / "src"
PAGES_DIR = ROOT / "pages"

PAGES = [
    ("index.html",         "Dashboard",         "pages/index.html"),
    ("summary.html",       "Executive Summary", "pages/summary.html"),
    ("properties.html",    "Property Data",     "pages/properties.html"),
    ("estate-tax.html",    "Estate & Gift Tax", "pages/estate-tax.html"),
    ("property-tax.html",  "Property Tax",      "pages/property-tax.html"),
    ("costs.html",         "Insurance & Utilities", "pages/costs.html"),
    ("rental.html",        "Rental Rules",      "pages/rental.html"),
    ("projections.html",   "Projections",       "pages/projections.html"),
    ("analysis.html",      "Live·Rent·Sell",    "pages/analysis.html"),
    ("process.html",       "Inheritance Process", "pages/process.html"),
    ("watchlist.html",     "Law Watchlist",     "pages/watchlist.html"),
    ("flagged.html",       "Flagged",           "pages/flagged.html"),
    ("sources.html",       "Sources",           "pages/sources.html"),
]

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{title} — Household Decision Dashboard</title>
<link rel="stylesheet" href="{css}">
</head>
<body>
<header class="site">
  <h1>Cupertino ↔ SF Household Decision Dashboard</h1>
  <span class="sub">City/ZIP-level data only · every row sourced or flagged · verified 2026-11-06</span>
</header>
<nav class="top">
{nav}
</nav>
<main>
{body}
</main>
<footer class="site">
  Built by session d8a9b67c · Source data &amp; audit: <code>docs/research/</code> ·
  Not tax/legal advice — verify every figure at the linked official source before acting.
</footer>
</body>
</html>
"""

def build():
    PAGES_DIR.mkdir(exist_ok=True)
    built = []
    for fname, title, href in PAGES:
        frag = (SRC / fname).read_text(encoding="utf-8")
        on_index = href == "index.html"
        nav_lines = []
        for _, ntitle, nhref in PAGES:
            # nav hrefs are written root-relative; rebase for pages under pages/
            if on_index:
                rel = nhref
            elif nhref == "index.html":
                rel = "../index.html"
            else:
                rel = nhref.removeprefix("pages/")
            active = ' class="active"' if nhref == href else ""
            nav_lines.append(f'  <a href="{rel}"{active}>{ntitle}</a>')
        # css path relative to page location
        css = "assets/style.css" if on_index else "../assets/style.css"
        # fix internal links in body: pages/x.html works from root; from pages/ it must be x.html
        body = frag
        if href != "index.html":
            body = body.replace('href="pages/', 'href="')
            body = body.replace('src="pages/', 'src="')
        html = TEMPLATE.format(title=title, nav="\n".join(nav_lines), body=body, css=css)
        out = ROOT / href
        out.write_text(html, encoding="utf-8")
        built.append(href)
    print(f"built {len(built)} pages: {', '.join(built)}")

if __name__ == "__main__":
    sys.exit(build())
