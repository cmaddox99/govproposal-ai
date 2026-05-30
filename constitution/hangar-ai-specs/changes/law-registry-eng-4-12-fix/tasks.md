# Tasks — Register ENG-4.12 in Domain Registry

**Spec ID:** `law-registry-eng-4-12-fix`
**Status:** Complete

## Task List

- [x] LR412-01 — Identify failing governance tests and root cause ✓
  - 3 tests failing: missing registry entry, missing article claim, missing non_negotiable flag
  - Root cause: ENG-4.12 authored in testing.md (commit b842260) but never added to _domain.yaml
- [x] LR412-02 — Add ENG-4.12 to Article IV `laws:` list in `_domain.yaml` ✓
- [x] LR412-03 — Add ENG-4.12 to Article IV `non_negotiable:` set in `_domain.yaml` ✓
- [x] LR412-04 — Add ENG-4.12 to `non_negotiable.engineering` list in `laws/index.yaml` ✓
- [x] LR412-05 — Add ENG-4.12 to main laws list in `laws/index.yaml` ✓
- [x] LR412-06 — Verify all 5 governance tests pass locally ✓ (10 passed, 0 failed)
- [x] LR412-07 — Verify constitution lint passes for ENG-4.12 violation ✓
- [x] LR412-08 — Commit and push to PR ✓
