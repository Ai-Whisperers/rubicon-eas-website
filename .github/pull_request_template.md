## What

Brief description of the change.

## Type

- [ ] Bug fix
- [ ] New feature
- [ ] Content / copy update
- [ ] Compliance / legal
- [ ] Infra / deploy
- [ ] Refactor

## Linked

- Issue: #...
- Plan: PLAN-DE-PREPARACION.md section ...
- Branch: older → newer

## Pre-flight

- [ ] `python3 scripts/validate-intake.py` → passes
- [ ] `python3 scripts/validate-content.py` → passes
- [ ] `python3 scripts/trademark-scrub.py` → passes
- [ ] `python3 scripts/smoke-test.py https://rubiconeas.paragu-ai.com` → passes
- [ ] Local preview loads (if applicable)
- [ ] No secrets committed (CF tokens, R2 keys, etc.)
- [ ] No trademark violations

## Checklist

- [ ] `PLAN-DE-PREPARACION.md` updated (if milestones changed)
- [ ] `tracker/STATUS.md` updated (if blockers changed)
- [ ] `worker.js` re-deployed (if R2 presigned URLs changed)
- [ ] `rubicon-eas-lead` Worker re-deployed (if API changed)

## After merge

- [ ] Verify live URL still serves
- [ ] Test lead pipeline end-to-end
- [ ] Comment on related issue(s)
