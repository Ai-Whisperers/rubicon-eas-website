---
name: Brief response
about: Submit intake answers for a specific section
title: '[Brief] NN · <section-name>'
labels: ['client-brief', 'intake']
assignees: []
---

## Section being answered

**File:** `intake/NN-<section-name>.json`
**Section title:** <paste from the JSON `section` field>

## Status

- [ ] I have read `PLAN-DE-PREPARACION.md` (recommended)
- [ ] I have read the **related questions** in the original JSON file
- [ ] I have my answers ready in the same JSON structure

## Answers

> Each question has an `id` (e.g. `IC-01`), a `question`, and an `answer` field.
>
> **Default behaviour:** placeholder answers are kept. To override, add an `answer` field with the client's response.

### IC-01
> *(copy the original question text here)*

```json
{
  "id": "IC-01",
  "answer": "...",
  "answered_by": "Dr. Pérez",
  "answer_date": "2026-08-15"
}
```

### IC-02
...

(repeat for each question in this section)

## Files attached

- [ ] Logo file (SVG/PNG)
- [ ] Profile photo
- [ ] Diploma / credentials
- [ ] Other documents referenced

## Notes / risks

Any concerns, ambiguities, or things you want to flag for Erebus.

---

✅ When done, Erebus will:
1. Validate the JSON structure (`scripts/validate-intake.py`)
2. Check the required fields are all answered (`scripts/check-required.py`)
3. Update the project tracker (`tracker/STATUS.md`)
4. Move that section from "00% real" to "100% real"
