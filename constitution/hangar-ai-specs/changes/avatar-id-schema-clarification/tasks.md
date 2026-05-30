# Tasks: Avatar ID Schema Clarification

**Proposal:** avatar-id-schema-clarification
**Branch:** `feat/avatar-id-schema-clarification`

## Progress Summary
- Total tasks: 5
- Completed: 5
- In Progress: 0
- Pending: 0

---

## Phase 1 — Schema Update

- [x] **T1** Update `docs/guides/avatar-model-schema.md §3` — replace single-pattern `id: avatar-{type}-{domain-slug}` with dual-pattern allowlist table showing both `avatar-{type}-{slug}` (canonical/recommended) and `avatar-{slug}` (permitted for existing avatars) ✓ fb2ce28

- [x] **T2** Update `workflows/avatar-workflow.md §Phase 2 Step 2.1` — replace `avatar.id matches directory slug exactly` with the new validation rule: `avatar.id starts with "avatar-"` AND `contains directory slug` AND `registered in index.yaml` ✓ fb2ce28

## Phase 2 — Registry

- [x] **T3** Update `hangar-ai-specs/README.md` — add proposal to active proposals table ✓ fb2ce28

## Phase 3 — Verify

- [x] **T4** Run `aa-constitution-lint .` — confirm 17/17 pass (or equivalent with new governance tests) ✓ governance-tests green

- [x] **T5** Run full test suite — confirm no regressions in existing tests ✓ unit-tests + rag-eval green
