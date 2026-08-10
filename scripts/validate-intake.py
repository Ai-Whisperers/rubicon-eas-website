#!/usr/bin/env python3
"""
Validate intake/*.json structure.
Each intake file must be a JSON object with:
  - "section": string
  - "scope": string
  - "questions": list of objects with:
      - "id": string (unique, e.g. IC-01, PR-02)
      - "category": string
      - "question": string
      - "type": one of: text, textarea, select, boolean, tags, file, url, range, date, number, email, tel
      - "required": boolean
      - optional: "example", "hint", "options", "min", "max", "default", "placeholder"
"""
import json
import glob
import sys
from pathlib import Path

VALID_TYPES = {"text", "textarea", "select", "boolean", "tags", "file", "url", "range", "date", "number", "email", "tel"}

REQUIRED_KEYS = {"id", "category", "question", "type", "required"}
OPTIONAL_KEYS = {"example", "hint", "options", "min", "max", "default", "placeholder", "accepted_formats"}

errors = []
total_questions = 0
total_files = 0

for path in sorted(glob.glob("intake/*.json")):
    if path.endswith("_totals.json"):
        continue
    total_files += 1
    with open(path) as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            errors.append(f"{path}: invalid JSON: {e}")
            continue

    if "section" not in data or not isinstance(data["section"], str):
        errors.append(f"{path}: missing or invalid 'section'")
    if "scope" not in data or not isinstance(data["scope"], str):
        errors.append(f"{path}: missing or invalid 'scope'")
    if "questions" not in data or not isinstance(data["questions"], list):
        errors.append(f"{path}: missing or invalid 'questions'")
        continue

    for i, q in enumerate(data["questions"]):
        total_questions += 1
        # Check required keys
        missing = REQUIRED_KEYS - set(q.keys())
        if missing:
            errors.append(f"{path} q{i+1}: missing keys: {missing}")
            continue

        # Check id format
        if not isinstance(q["id"], str) or not q["id"]:
            errors.append(f"{path} q{i+1}: invalid id")

        # Check type
        if q["type"] not in VALID_TYPES:
            errors.append(f"{path} q{i+1}: invalid type '{q['type']}'. Valid: {sorted(VALID_TYPES)}")

        # If select, must have options
        if q["type"] == "select" and "options" not in q:
            errors.append(f"{path} q{i+1}: 'select' type must have 'options'")

        # If range, must have min and max
        if q["type"] == "range":
            if "min" not in q or "max" not in q:
                errors.append(f"{path} q{i+1}: 'range' type must have 'min' and 'max'")

        # Check optional keys are allowed
        unknown = set(q.keys()) - REQUIRED_KEYS - OPTIONAL_KEYS
        if unknown:
            errors.append(f"{path} q{i+1}: unknown keys: {unknown}")

print(f"📋 Intake JSON validation")
print(f"  Files: {total_files}")
print(f"  Questions: {total_questions}")

if errors:
    print(f"\n❌ {len(errors)} errors:")
    for err in errors[:20]:
        print(f"  - {err}")
    if len(errors) > 20:
        print(f"  ... and {len(errors) - 20} more")
    sys.exit(1)
else:
    print(f"  ✅ All intake files valid")
    sys.exit(0)
