#!/usr/bin/env python3
"""Lightweight checks for the public static site and its source-link policy."""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
PAGES = [ROOT / "index.html", *sorted((ROOT / "pages").glob("*.html"))]
OFFICIAL_HOSTS = (
    "irs.gov",
    "boe.ca.gov",
    "ca.gov",
    "leginfo.legislature.ca.gov",
    "insurance.ca.gov",
    "sfpuc.gov",
    "sf.gov",
    "sfbos.archive.sf.gov",
    "asr.santaclaracounty.gov",
    "lao.ca.gov",
    "cpuc.ca.gov",
)
ERRORS: list[str] = []


class Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "a":
            self.hrefs.append(dict(attrs).get("href") or "")


def check_page(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    parser = Links()
    parser.feed(text)

    for href in parser.hrefs:
        parsed = urlparse(href)
        if parsed.scheme in ("http", "https"):
            if parsed.scheme != "https":
                ERRORS.append(f"{path.relative_to(ROOT)}: non-HTTPS link: {href}")
            if not any(parsed.hostname == host or (parsed.hostname or "").endswith("." + host) for host in OFFICIAL_HOSTS):
                ERRORS.append(f"{path.relative_to(ROOT)}: external link is not on the approved official-source list: {href}")
        elif parsed.scheme == "mailto":
            continue
        else:
            local = (path.parent / parsed.path).resolve() if parsed.path else path
            if not local.exists():
                ERRORS.append(f"{path.relative_to(ROOT)}: broken internal link: {href}")

    rows = re.findall(r"<tr>(.*?)</tr>", text, flags=re.DOTALL)
    data_rows = [row for row in rows if "<th" not in row]
    for index, row in enumerate(data_rows, start=1):
        sources = re.findall(r'<a\s+[^>]*href="(https://[^"]+)"', row, flags=re.IGNORECASE)
        if not sources:
            ERRORS.append(f"{path.relative_to(ROOT)}: data table row {index} has no HTTPS source link")
        for source in sources:
            hostname = urlparse(source).hostname or ""
            if not any(hostname == host or hostname.endswith("." + host) for host in OFFICIAL_HOSTS):
                ERRORS.append(f"{path.relative_to(ROOT)}: table source is not an approved official host: {source}")

    for tag in ("html", "head", "body", "nav", "main", "footer"):
        if f"<{tag}" not in text or f"</{tag}>" not in text:
            ERRORS.append(f"{path.relative_to(ROOT)}: missing {tag} document structure")
    print(f"checked {path.relative_to(ROOT)} ({len(data_rows)} table data rows, {len(parser.hrefs)} links)")


def main() -> int:
    if not PAGES or not (ROOT / "pages").is_dir():
        print("site pages are missing", file=sys.stderr)
        return 1
    for page in PAGES:
        check_page(page)
    if ERRORS:
        for error in ERRORS:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Site validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
