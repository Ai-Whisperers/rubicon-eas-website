#!/usr/bin/env python3
"""
Validate that content ES JSON has the canonical schema.
"""
import json
import sys
import os
from pathlib import Path

REQUIRED_TOP = {"site", "navigation", "hero", "areas", "trust_strip", "about", "cases", "testimonials", "faq", "contact", "disclaimer", "footer"}
REQUIRED_SITE = {"name", "tagline", "matricula_csj", "phone", "whatsapp", "email", "address"}

errors = []
warnings = []

# Check sample/assets/content.es.json
content_path = "sample/assets/content.es.json"
if not os.path.exists(content_path):
    print(f"❌ Missing {content_path}")
    sys.exit(1)

with open(content_path) as f:
    data = json.load(f)

# Top-level keys
missing = REQUIRED_TOP - set(data.keys())
if missing:
    errors.append(f"missing top-level keys: {missing}")

# site object
site = data.get("site", {})
missing_site = REQUIRED_SITE - set(site.keys())
if missing_site:
    errors.append(f"site.{missing_site} missing")

# Navigation
nav = data.get("navigation", [])
if not isinstance(nav, list) or len(nav) < 5:
    warnings.append(f"navigation has only {len(nav) if isinstance(nav, list) else 0} items")

# Areas
areas = data.get("areas", {}).get("items", [])
if len(areas) < 3:
    errors.append(f"need at least 3 practice areas, got {len(areas)}")

# Cases
cases = data.get("cases", {})
case_items = cases.get("items", [])
if len(case_items) < 1:
    warnings.append(f"no case studies yet")

# FAQ
faq = data.get("faq", {})
faq_sections = faq.get("sections", [])
if len(faq_sections) < 1:
    warnings.append(f"no FAQ sections")

# Disclaimer
disc = data.get("disclaimer", "")
if "no constituye asesoramiento" not in disc.lower():
    errors.append(f"disclaimer must include 'no constituye asesoramiento jurídico'")

# Footer
footer = data.get("footer", {})
if not footer.get("legal_links"):
    warnings.append("footer should have legal_links")

print(f"📋 Content schema validation")
print(f"  Site: {site.get('name', 'MISSING')}")
print(f"  Phone: {site.get('phone', 'MISSING')}")
print(f"  Areas: {len(areas)}")
print(f"  Cases: {len(case_items)}")
print(f"  FAQ sections: {len(faq_sections)}")

if errors:
    print(f"\n❌ {len(errors)} errors:")
    for err in errors:
        print(f"  - {err}")
    sys.exit(1)

if warnings:
    print(f"\n⚠️  {len(warnings)} warnings:")
    for w in warnings:
        print(f"  - {w}")

print(f"  ✅ Content valid")
sys.exit(0)
