# Project Tracker

Track Rubicón EAS project status. Run from repo root:

```bash
# Live status
cat tracker/STATUS.md

# Counts
python3 scripts/check-required.py
python3 scripts/validate-intake.py
python3 scripts/validate-content.py

# Smoke test
python3 scripts/smoke-test.py https://rubiconeas.paragu-ai.com
```

## Files

- `STATUS.md` — current project state, blockers, milestones
- `README.md` — this file

## Update cycle

- `STATUS.md` updated: when client closes a milestone or when CI fails
- `check-required.py` updated: every time client sends intake responses
- `smoke-test.py` updated: after every deploy to live

## Status colors

- ✅ green / done
- 🟡 yellow / in progress, 50-90%
- ⚪ white / not started
- ❌ red / blocked or failed
