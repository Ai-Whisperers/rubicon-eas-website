#!/usr/bin/env python3
"""
Smoke test live preview URL.
Hits each page and verifies HTTP 200 with correct title.
"""
import urllib.request
import urllib.error
import re
import sys

URL = sys.argv[1] if len(sys.argv) > 1 else "https://rubiconeas.paragu-ai.com"

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

PAGES = [
    ("/", "Rubicón EAS"),
    ("/derecho-civil.html", "Derecho Civil"),
    ("/derecho-penal.html", "Derecho Penal"),
    ("/derecho-ambiental.html", "Derecho Ambiental"),
    ("/nosotros.html", "Nosotros"),
    ("/casos.html", "Casos"),
    ("/contacto.html", "Contacto"),
    ("/blog.html", "Artículos"),
    ("/assets/styles.css", None),
    ("/assets/main.js", None),
]

errors = []
ok = 0

for path, expected_keyword in PAGES:
    url = URL.rstrip("/") + path
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Cache-Control": "no-cache"})
        r = urllib.request.urlopen(req, timeout=10)
        body = r.read().decode("utf-8", errors="replace")
        if r.status != 200:
            errors.append(f"{url}: HTTP {r.status}")
            continue
        if expected_keyword and expected_keyword not in body:
            errors.append(f"{url}: missing '{expected_keyword}' in body")
            continue
        ok += 1
    except urllib.error.HTTPError as e:
        errors.append(f"{url}: HTTP {e.code}")
    except Exception as e:
        errors.append(f"{url}: {e}")

print(f"🩺 Smoke test {URL}")
print(f"  OK: {ok}/{len(PAGES)}")
if errors:
    print(f"  ❌ Errors:")
    for err in errors:
        print(f"    - {err}")
    sys.exit(1)
print(f"  ✅ All pages serve")
