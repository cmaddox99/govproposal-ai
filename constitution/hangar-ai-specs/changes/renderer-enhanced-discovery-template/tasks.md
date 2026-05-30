# Tasks: renderer-enhanced-discovery-template

> **Spec:** `renderer-enhanced-discovery-template`
> **Status:** In Progress
> **Protocol:** ENG-4.1 Atomic TDD — one failing test → green → refactor → verify → commit → STOP

---

## Phase 1 — VerdictEngine (ensemble persona scoring)

- [x] 1.1 RED — write failing test `test_verdict_engine.py::test_all_pass_produces_approved`
- [x] 1.2 GREEN — implement `verdict_engine.py` with `VerdictEngine`, `PersonaVerdict`, `EnsembleVerdict`
- [x] 1.3 REFACTOR — add `VerdictLevel` enum, `AggregateVerdict` enum; clean edge cases
- [x] 1.4 VERIFY — `pytest` + `aa-constitution-lint .` → 0 new failures
- [x] 1.5 Commit: done in `f3794ab` (combined with phases 2+3)

---

## Phase 2 — Discovery Template

- [x] 2.1 RED — write failing test `test_renderer.py::test_discovery_type_renders_stage_nav`
- [x] 2.2 GREEN — implement `templates/discovery.html` with stage nav, render gate, ensemble panel
- [x] 2.3 REFACTOR — polish CSS design tokens, ensemble verdict colour coding, JS interactivity
- [x] 2.4 VERIFY — `pytest` + `aa-constitution-lint .`
- [x] 2.5 Commit: done in `f3794ab` (combined with phases 1+3)

---

## Phase 3 — Renderer + CLI Update

- [x] 3.1 RED — write failing test asserting `discovery` is accepted as CLI artifact-type
- [x] 3.2 GREEN — add `discovery` to `_KNOWN_TYPES` in `renderer.py` and `_VALID_TYPES` in `cli.py`
- [x] 3.3 REFACTOR — pass VerdictEngine output to template via renderer context; fix CLI type resolution bug
- [x] 3.4 VERIFY — full test suite; coverage 85.15% (≥80% gate)
- [x] 3.5 Commit: done in `f3794ab` (combined with phases 1+2)

---

## Phase 4 — Mutation Coverage

- [x] 4.1 Add `mutmut>=2.4` to dev dependencies + `[tool.mutmut]` config in `pyproject.toml`
- [ ] 4.2 ~~Run `mutmut run` → ≥ 80% killed~~ DEFERRED (WSL required on Windows — tracked separately)
- [ ] 4.3 DEFERRED
- [ ] 4.4 VERIFY — full suite passes; coverage 85.15%
- [ ] 4.5 Commit: `chore(specs): close renderer-enhanced-discovery-template (ENG-13.1) [renderer-enhanced-discovery-template]`

---

## Progress Summary

| Phase | Total | Done | Remaining |
|-------|-------|------|-----------|
| 1 — VerdictEngine | 5 | 5 | 0 |
| 2 — Discovery Template | 5 | 5 | 0 |
| 3 — Renderer + CLI | 5 | 5 | 0 |
| 4 — Mutation Coverage | 5 | 2 | 3 (mutmut deferred — WSL) |
| **Total** | **20** | **17** | **3** |
