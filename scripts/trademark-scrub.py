#!/usr/bin/env python3
"""
Trademark banlist scrub.
Fails CI if banned words appear in any committed file.

Carve-outs: bare functional terms ("messaging bridge"), upstream OSS names (Evolution API),
Hostinger incident quote, existing package names, technical HTML terms.

Detection: word-boundary regex, not substring. `meta` does NOT match `metadata`.
"""
import os
import re
import sys

# Banned patterns with word boundaries (case-insensitive).
# These are trademarks that triggered the Hostinger suspension.
BANNED_PATTERNS = [
    r"\bwhatsapp business\b",
    r"\bwhatsapp-business\b",
    r"\bfacebook\b",
    r"\bmeta\s+platforms\b",     # Meta Platforms (the company)
    r"\bmeta\s+inc\b",            # Meta Inc
    r"\binstagram\b",
    r"\bobscura\b",                # Obscura VPN (was Meta product)
    r"\bmessenger\b",              # FB Messenger
    r"\boculus\b",
    r"\bpaypal\b",
    r"\bstripe\b",
    r"\bgmail\b",
    r"\byoutube\b",
    r"\btiktok\b",
    r"\btwitter\b",
    r"\bdiscord\b",
    r"\bslack\b",
    r"\bmicrosoft\s+365\b",
    r"\boffice\s+365\b",
    r"\bapple\s+icloud\b",
    r"\bicloud\b",
    r"\bamazon\s+aws\b",
    r"\bopenai\b",
    r"\bchatgpt\b",
    r"\banthropic\b",
    r"\bclaude\b",
]

# Compile
BANNED_RE = [re.compile(p, re.IGNORECASE) for p in BANNED_PATTERNS]

# Files that are EXEMPT (carve-outs)
EXEMPT_FILES = {
    "scripts/trademark-scrub.py",
    "PLAN-DE-PREPARACION.md",
    "README.md",
    "DEPLOY.md",
    "intake/",  # questionnaire may ask about these platforms
    "propuesta/PROPUESTA-COMERCIAL.md",
    "legales/01-EAS-Paraguay-Complete-Guide.md",
    "legales/02-EAS-Formation-Checklist.md",
    "legales/03-EAS-Constitution-Template.md",
    "legales/04-EAS-Formation-Plan.md",
    "legales/05-Paraguay-Corporate-Forms-Comparison.md",
    "legales/06-Master-Service-Agreement-Template.md",
    "legales/07-Independent-Contractor-Agreement.md",
    "legales/08-NDA-Template.md",
    "legales/09-Privacy-Policy-Template.md",
    "legales/10-Code-of-Conduct-Template.md",
    "legales/11-Information-Security-Policy.md",
    "legales/12-Data-Protection-Policy.md",
    "legales/13-Seven-Flag-Business-Model.md",
    "legales/practice-legal/",
    "legales/patient-legal/",
    "legales/research/",
    "legales/whatsapp-bot/",
    "legales/quick-replies/",
}

# Patterns that, when found, absorb the violation (legitimate contexts)
LEGITIMATE_CONTEXTS = [
    re.compile(r"\bai-whisperers-", re.IGNORECASE),  # our package names
    re.compile(r"\bevolution-api\b", re.IGNORECASE),  # upstream OSS
    re.compile(r"\bmessaging bridge\b", re.IGNORECASE),  # functional term
    re.compile(r"\bhostinger\b", re.IGNORECASE),  # incident context
    re.compile(r"meta_description", re.IGNORECASE),  # SEO field
    re.compile(r"meta_title", re.IGNORECASE),
    re.compile(r"meta\s+name=", re.IGNORECASE),  # HTML meta tags
    re.compile(r"meta\s+property=", re.IGNORECASE),
    re.compile(r"<meta\b", re.IGNORECASE),  # HTML meta tag
    re.compile(r"\bmetadata\b", re.IGNORECASE),  # general term
    re.compile(r"\binstagram-style\b", re.IGNORECASE),  # generic
    re.compile(r"\bcookies?\b", re.IGNORECASE),  # not banned
]

errors = []

# Walk all text files
for root, dirs, files in os.walk("."):
    # Skip hidden and node_modules
    dirs[:] = [d for d in dirs if not d.startswith(".") and d != "node_modules"]
    for f in files:
        # Skip binary
        if any(f.endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".webp", ".gif", ".ico", ".woff", ".woff2", ".ttf", ".svg", ".pdf"]):
            continue
        path = os.path.join(root, f)
        rel = os.path.relpath(path, ".")

        # Apply exempt carve-outs
        skip = False
        for carve in EXEMPT_FILES:
            if carve.endswith("/"):
                if rel.startswith(carve):
                    skip = True
                    break
            elif rel == carve:
                skip = True
                break
        if skip:
            continue

        try:
            with open(path, errors="ignore") as fh:
                content = fh.read()
        except:
            continue

        # Check each banned pattern
        for pattern in BANNED_RE:
            matches = pattern.findall(content)
            if not matches:
                continue
            # Skip if there's a legitimate context
            has_legitimate = False
            for ctx in LEGITIMATE_CONTEXTS:
                if ctx.search(content):
                    has_legitimate = True
                    break
            if has_legitimate:
                continue
            errors.append(f"{rel}: matches '{pattern.pattern}' ({len(matches)}x)")

if errors:
    print(f"❌ Trademark banlist violations: {len(errors)}")
    for err in errors[:20]:
        print(f"  - {err}")
    if len(errors) > 20:
        print(f"  ... and {len(errors) - 20} more")
    sys.exit(1)
else:
    print(f"✅ Trademark banlist clean (word-boundary regex applied)")
    sys.exit(0)
