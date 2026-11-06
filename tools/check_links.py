#!/usr/bin/env python3
"""Link checker: internal links must resolve to real files; external links must be
present with scheme http(s). Prints a report; exits non-zero on internal breakage."""
import pathlib, re, sys, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
html_files = [ROOT / "index.html"] + sorted((ROOT / "pages").glob("*.html"))

internal_bad, external, anchors_missing = [], [], []
link_re = re.compile(r'href="([^"]+)"')
id_re = re.compile(r'id="([^"]+)"')

ids_by_file = {}
for f in html_files:
    ids_by_file[f] = set(id_re.findall(f.read_text(encoding="utf-8")))

for f in html_files:
    text = f.read_text(encoding="utf-8")
    for href in link_re.findall(text):
        if href.startswith(("http://", "https://")):
            external.append((f.name, href))
            continue
        if href.startswith("mailto:"):
            continue
        # split anchor
        if "#" in href:
            path, frag = href.split("#", 1)
        else:
            path, frag = href, None
        target = (f.parent / path).resolve() if path else f.resolve()
        if path and target.is_dir():
            target = target / "index.html"  # directory links resolve to their index
        if path and not target.exists():
            internal_bad.append((str(f.relative_to(ROOT)), href))
        elif frag:
            if target not in ids_by_file:
                ids_by_file[target] = set(id_re.findall(target.read_text(encoding="utf-8")))
            if frag not in ids_by_file[target]:
                anchors_missing.append((str(f.relative_to(ROOT)), href))

print(f"Checked {len(html_files)} HTML files")
print(f"External links: {len(external)}")
ext_hosts = {}
for _, u in external:
    host = urllib.parse.urlparse(u).netloc
    ext_hosts[host] = ext_hosts.get(host, 0) + 1
for h, c in sorted(ext_hosts.items(), key=lambda x: -x[1]):
    print(f"  {h}: {c}")

if internal_bad:
    print("\nBROKEN INTERNAL LINKS:")
    for f, h in internal_bad:
        print(f"  {f}: {h}")
if anchors_missing:
    print("\nMISSING ANCHORS:")
    for f, h in anchors_missing:
        print(f"  {f}: {h}")

ok = not internal_bad and not anchors_missing
print("\nRESULT:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
