#!/usr/bin/env python3
"""
Check that all required-field questions are filled in client responses.
Run after intake has been answered.
"""
import json
import glob
import sys

errors = []
total_required = 0
total_unanswered = 0

for path in sorted(glob.glob("intake/*.json")):
    if path.endswith("_totals.json"):
        continue
    with open(path) as f:
        data = json.load(f)

    for q in data.get("questions", []):
        if q.get("required"):
            total_required += 1
            # Check if "answer" or "value" field is present and non-empty
            answer = q.get("answer") or q.get("value")
            has_example = "example" in q and (q.get("answer") is None)
            if answer is None and not has_example:
                total_unanswered += 1
                errors.append(f"{path} {q['id']}: required, no answer")

print(f"📋 Required field check")
print(f"  Required: {total_required}")
print(f"  Unanswered: {total_unanswered}")

if errors:
    print(f"\n⚠️  Required questions not yet answered:")
    for err in errors[:30]:
        print(f"  - {err}")
    if len(errors) > 30:
        print(f"  ... and {len(errors) - 30} more")
    sys.exit(1 if total_unanswered == total_required else 0)
else:
    print(f"  ✅ All required answered")
    sys.exit(0)
