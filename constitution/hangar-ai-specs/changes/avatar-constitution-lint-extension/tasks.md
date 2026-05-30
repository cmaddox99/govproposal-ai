# Tasks: avatar-constitution-lint-extension

**Laws governing this work:** `ENG-11.1`, `ENG-11.2`, `ENG-4.1`, `ENG-4.2`, `ENG-10.1`

## Progress Summary

- Completed: 3 / 20
- In Progress: 0
- Blocked: 0

---

## Phase 0: Hangar SDD Execution Artifacts

> **Goal:** Establish governed execution tracking.

- [x] 0.1 Create `PROPOSAL.md`
- [x] 0.2 Create `tasks.md`
- [x] 0.3 Create `PROGRESS.md`

## Phase 1: Rule Infrastructure

> **Goal:** Set up the avatar rules module and test scaffolding.

- [ ] 1.1 Create `tools/constitution-lint/src/aa_constitution_lint/domain/rules/avatars.py` with avatar discovery logic
- [ ] 1.2 Register avatar rules in lint engine (`application/lint_engine.py`)
- [ ] 1.3 Create test scaffolding `tools/constitution-lint/tests/test_avatar_rules.py`
- [ ] 1.4 Implement avatar discovery (scan `avatars/technology/*/manifest.yaml`)

## Phase 2: Core Validation Rules

> **Goal:** Implement the 7 avatar validation rules.

- [ ] 2.1 Implement `AvatarManifestSchemaRule` — required sections validation
- [ ] 2.2 Implement `AvatarLawReferenceRule` — law ID validity via `LawRegistry`
- [ ] 2.3 Implement `AvatarExampleFileRule` — example file existence checks
- [ ] 2.4 Implement `AvatarTokenBudgetRule` — 600-token budget enforcement
- [ ] 2.5 Implement `AvatarCitationFormatRule` — hyperlink citation format validation
- [ ] 2.6 Implement `AvatarParityRule` — structural parity with reference avatars
- [ ] 2.7 Implement `AvatarNonNegotiableCoverageRule` — 18 non-negotiable law coverage

## Phase 3: Integration and Documentation

> **Goal:** Wire rules into CI and document usage.

- [ ] 3.1 Verify all rules pass on java-spring and python-fastapi avatars (no false positives)
- [ ] 3.2 Verify all rules pass on C++ avatar (once enrichment is complete)
- [ ] 3.3 Verify `--format json` output includes avatar evaluations
- [ ] 3.4 Update `tools/constitution-lint/README.md` with avatar checks documentation
- [ ] 3.5 Update `AGENTS.md` to reference avatar lint checks in VERIFY step
- [ ] 3.6 Final governance review and PROGRESS.md sign-off
