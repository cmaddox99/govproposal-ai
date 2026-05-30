# Tasks: cpp-governance-tooling-enhancements

**Laws governing this work:** `ENG-11.1`, `ENG-11.2`, `ENG-10.1`, `ENG-4.1`, `ENG-6.7`

**Proposal:** `PROPOSAL.md` in this directory
**Predecessor:** `hangar-ai-specs/changes/cpp-version-routing-foundation/` (PR #47, merge-ready)

## Progress Summary

- Completed: 0 / 0
- In Progress: 0
- Blocked: 0

**Status:** 🟡 DRAFT — not yet in implementation

---

## Phase 0: Pre-Work Investigation

> **Goal:** Resolve open questions before writing tests or code.

- [ ] 0.1 Locate canonical adoption guide — find where per-language onboarding checklists live (`docs/guides/adoption/` or elsewhere)
- [ ] 0.2 Audit `tools/constitution-lint/` plugin architecture — determine how to register a new lint rule
- [ ] 0.3 Assess guidance.md token budget relief — identify prose that can be trimmed to create ≥10 token headroom for mixed-migration note (current: 344 words, ~447t after N3/ENG-2.1 fix)
- [ ] 0.4 Open PR targeting main; link to PROPOSAL.md

---

## Phase 1: `schema_version` Enforcement Lint Rule

> **Goal:** Lint rule that catches `.copilot/project.yaml` missing `schema_version`.

- [ ] 1.1 RED: write `test_schema_version_lint_rule_catches_missing_key` — assert lint FAILS when `cpp:` block present but `schema_version` absent; run → confirm FAILED
- [ ] 1.2 RED: write `test_schema_version_lint_rule_passes_when_present` — assert lint PASSES when `schema_version: "1"` present; run → confirm FAILED
- [ ] 1.3 GREEN: implement `cpp_project_yaml_schema_version` lint rule in `tools/constitution-lint/`
- [ ] 1.4 REFACTOR: ensure rule integrates cleanly with existing rule registration pattern
- [ ] 1.5 VERIFY: run full test suite + constitution-lint → all green; run lint against repo → 21/21+ pass

---

## Phase 2: D3 Ref-File Existence Lint Rule

> **Goal:** Lint rule that verifies all prefer/avoid paths in version_routing_policy exist on disk.

- [ ] 2.1 RED: write `test_avatar_rag_index_ref_files_exist_rule_catches_missing_file` — assert lint FAILS when prefer list references non-existent file; run → confirm FAILED
- [ ] 2.2 RED: write `test_avatar_rag_index_ref_files_exist_rule_passes_when_all_present` — assert lint PASSES when all prefer/avoid files exist; run → confirm FAILED
- [ ] 2.3 GREEN: implement `avatar_rag_index_ref_files_exist` lint rule
- [ ] 2.4 REFACTOR: generalize rule to work for any technology avatar with `version_routing_policy`
- [ ] 2.5 VERIFY: run full test suite + constitution-lint → all green

---

## Phase 3: guidance.md Mixed-Migration Note

> **Pre-condition:** guidance.md word count × 1.3 must be ≤ 440 after any trim (need 10 token headroom).
> **Status:** BLOCKED on Phase 0.3 token budget assessment

- [ ] 3.1 UNBLOCK: trim guidance.md to free ≥10 token headroom; verify budget tests still pass
- [ ] 3.2 RED: write `test_guidance_addresses_mixed_migration` — assert guidance.md contains mixed-migration note; run → confirm FAILED
- [ ] 3.3 GREEN: add mixed-migration footnote to detection order step 5 in guidance.md
- [ ] 3.4 VERIFY: run full suite + lint; check both token budget tests pass

---

## Phase 4: Adoption Workflow — C++ Version Declaration Step

> **Pre-condition:** Phase 0.1 must identify the adoption guide location.
> **Status:** BLOCKED on Phase 0.1

- [ ] 4.1 UNBLOCK: confirm adoption guide path and per-language checklist pattern
- [ ] 4.2 RED: write test asserting adoption guide references `cpp-project.yaml` template
- [ ] 4.3 GREEN: add mandatory C++ version declaration step to adoption guide
        Step text: "Declare your C++ standard: copy `avatars/technology/cpp/templates/cpp-project.yaml`
        to `.copilot/project.yaml` and set `cpp.standard` to your project's actual C++ version."
- [ ] 4.4 VERIFY: run full suite + lint → all green

---

## Phase 5: Full Verification and PR

- [ ] 5.1 Run full test suite → all green (expect 830+ tests)
- [ ] 5.2 Run constitution-lint → clean
- [ ] 5.3 Manual walkthrough: adopt C++ avatar without project.yaml → confirm lint warns
- [ ] 5.4 Manual walkthrough: delete a refs file → confirm lint fails
- [ ] 5.5 Update progress summary
- [ ] 5.6 Commit and push; update PR #47 successor link
