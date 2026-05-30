# Tasks: cpp-ref-file-rightsizing

**Laws governing this work:** `ENG-11.1`, `ENG-11.2`, `ENG-10.1`, `ENG-4.1`, `ENG-6.7`

**Prerequisite for:** `cpp-version-sensitivity-analysis` options A–E

## Progress Summary

- Completed: 130 / 130
- In Progress: 0
- Blocked: 0

---

## Phase 0: Governance

> **Goal:** Establish governed execution tracking.

- [x] 0.1 Create `PROPOSAL.md` ✓ (done — this change)
- [x] 0.2 Create `tasks.md` ✓ (done — this file)
- [ ] 0.3 Open PR targeting main; description links to PROPOSAL.md and version-sensitivity analysis

---

## Phase 1: Pre-Flight Verification

> **Goal:** Confirm all source file token measurements before splitting. Re-measure any file
> marked `~` (estimated) in the split plan.

- [x] 1.1 Re-measure `ref-object-design.md` sections — confirm H3 split (after item 6) at ~3,443 / ~1,548 tokens
- [x] 1.2 Re-measure `ref-legacy-smells.md` sections — confirm H3 split at ~2,405 / ~2,404 tokens
- [x] 1.3 Re-measure `ref-legacy-mental-models.md` sections — confirm H3 split at ~2,353 / ~2,353 tokens
- [x] 1.4 Re-measure `ref-legacy-navigation.md` — confirm H2 split at `## Legacy Codebase Triage Playbook` boundary: ~1,694 / ~2,464 tokens
- [x] 1.5 Search repo for all references to the 14 files being renamed — explicit scope: `docs/`, `tools/`, `tests/`, `.github/workflows/`, `hangar-ai-specs/changes/` (other proposals), `avatars/AVATAR-RAG-INDEX.yaml`; record impacted files here and confirm the list matches PROPOSAL.md Cross-Avatar Impact table

---

## Phase 2: Split `ref-testing-ci.md` (3-way, 6,975 tokens)

> Boundary: H2 sections. Output: `ref-testing-ci-policy.md`, `ref-testing-gtest-core.md`,
> `ref-testing-gtest-advanced.md`.

- [x] 2.1 RED: write test asserting `ref-testing-ci-policy.md` exists and is ≤3,500 tokens; run test suite — confirm FAILED
- [x] 2.2 GREEN: create `ref-testing-ci-policy.md` from CI policy sections of `ref-testing-ci.md`; run test suite — confirm PASSED
- [x] 2.3 RED: write test asserting `ref-testing-gtest-core.md` exists and is ≤3,500 tokens; run test suite — confirm FAILED
- [x] 2.4 GREEN: create `ref-testing-gtest-core.md` from core GTest sections; run test suite — confirm PASSED
- [x] 2.5 RED: write test asserting `ref-testing-gtest-advanced.md` exists and is ≤3,500 tokens; run test suite — confirm FAILED
- [x] 2.6 GREEN: create `ref-testing-gtest-advanced.md` from advanced GTest sections; run test suite — confirm PASSED
- [x] 2.7 VERIFY: token sum of three output files = source file tokens ± 50; confirm no content loss
- [x] 2.8 Remove `ref-testing-ci.md`
- [x] 2.9 Update `tests/unit/test_cpp_avatar/test_rag_index.py` — replace assertion that reference-index.md has exactly 1 row for `ref-testing-ci.md` with assertions for `ref-testing-ci-policy.md`, `ref-testing-gtest-core.md`, and `ref-testing-gtest-advanced.md`

---

## Phase 3: Split `ref-brownfield-config.md` (2-way, 6,203 tokens)

> Boundary: H2. Output: `ref-brownfield-adoption.md`, `ref-brownfield-project-config.md`.
> Note: Part A is named `ref-brownfield-adoption.md` (not `ref-brownfield-migration.md`) to avoid
> confusion with `ref-migration-playbooks.md`.

- [x] 3.1 RED: write test asserting `ref-brownfield-adoption.md` exists and is ≤3,500 tokens; run test suite — confirm FAILED
- [x] 3.2 GREEN: create `ref-brownfield-adoption.md` (~2,996 tokens) from H2 migration/adoption sections of `ref-brownfield-config.md`; run test suite — confirm PASSED
- [x] 3.3 RED: write test asserting `ref-brownfield-project-config.md` exists and is ≤3,500 tokens; run test suite — confirm FAILED
- [x] 3.4 GREEN: create `ref-brownfield-project-config.md` (~3,183 tokens) from H2 project-config sections; run test suite — confirm PASSED
- [x] 3.5 VERIFY: token sum of output files = source file tokens ± 50; confirm no content loss
- [x] 3.6 Remove `ref-brownfield-config.md`
- [x] 3.7 Update `tests/unit/test_cpp_avatar/test_phase10_standard_tiers.py` — replace hard-coded `ref-brownfield-config.md` path with `ref-brownfield-adoption.md`

---

## Phase 4: Split `ref-migration-playbooks.md` ★ VERSION (2-way, 5,483 tokens)

> Boundary: C++17 version boundary. Output: `ref-migration-pre-cpp17.md`,
> `ref-migration-cpp17-plus.md`. This split provides version routing benefit.

- [x] 4.1 RED: write test asserting `ref-migration-pre-cpp17.md` exists and is ≤3,500 tokens; run test suite — confirm FAILED
- [x] 4.2 GREEN: create `ref-migration-pre-cpp17.md` (~2,162 tokens) — C++98→17 migrations; run test suite — confirm PASSED
- [x] 4.3 RED: write test asserting `ref-migration-cpp17-plus.md` exists and is ≤3,500 tokens; run test suite — confirm FAILED
- [x] 4.4 GREEN: create `ref-migration-cpp17-plus.md` (~3,321 tokens) — C++17→20, ActiveTest; run test suite — confirm PASSED
- [x] 4.5 VERIFY: token sum of output files = source file tokens ± 50; confirm no content loss
- [x] 4.6 Remove `ref-migration-playbooks.md`
- [x] 4.7 Update `tests/unit/test_cpp_avatar/test_phase11_migration_playbooks.py` — replace hard-coded `ref-migration-playbooks.md` path with assertions for both `ref-migration-pre-cpp17.md` and `ref-migration-cpp17-plus.md`

---

## Phase 5: Split `ref-concurrency.md` ★ VERSION (2-way, 5,261 tokens)

> Boundary: C++20 version boundary. Output: `ref-concurrency-threading.md`,
> `ref-concurrency-async.md`. This split provides version routing benefit.

- [x] 5.1 RED: write test asserting `ref-concurrency-threading.md` exists and is ≤3,500 tokens; run test suite — confirm FAILED
- [x] 5.2 GREEN: create `ref-concurrency-threading.md` (~1,858 tokens) — thread/mutex/atomic; run test suite — confirm PASSED
- [x] 5.3 RED: write test asserting `ref-concurrency-async.md` exists and is ≤3,500 tokens; run test suite — confirm FAILED
- [x] 5.4 GREEN: create `ref-concurrency-async.md` (~3,412 tokens) — coroutines, stop_token; run test suite — confirm PASSED
- [x] 5.5 VERIFY: token sum of output files = source file tokens ± 50; confirm no content loss
- [x] 5.6 Remove `ref-concurrency.md`

---

## Phase 6: Split `ref-object-design.md` (2-way, 5,112 tokens)

> Boundary: H3. Output: `ref-object-design-rehabilitation.md`, `ref-object-design-patterns.md`.

- [x] 6.1 RED: write test asserting `ref-object-design-rehabilitation.md` exists and is ≤3,500 tokens; run test suite — confirm FAILED
- [x] 6.2 GREEN: create `ref-object-design-rehabilitation.md` (~3,443 tokens) from items 1–6 of "Object Design Rehabilitation" section; run test suite — confirm PASSED
- [x] 6.3 RED: write test asserting `ref-object-design-patterns.md` exists and is ≤3,500 tokens; run test suite — confirm FAILED
- [x] 6.4 GREEN: create `ref-object-design-patterns.md` (~1,548 tokens) from Decision Tree, Protected/Private Inheritance, Mixin/Policy design, Test Isolation and Mock Boundaries sections; run test suite — confirm PASSED
- [x] 6.5 VERIFY: token sum of output files = source file tokens ± 50; confirm no content loss
- [x] 6.6 Remove `ref-object-design.md`

---

## Phase 7: Split `ref-advanced-cpp.md` (2-way, 5,100 tokens)

- [x] 7.1 RED: write test asserting `ref-templates-metaprogramming.md` exists and is ≤3,500 tokens; run test suite — confirm FAILED
- [x] 7.2 GREEN: create `ref-templates-metaprogramming.md` (~2,351 tokens); run test suite — confirm PASSED
- [x] 7.3 RED: write test asserting `ref-advanced-patterns.md` exists and is ≤3,500 tokens; run test suite — confirm FAILED
- [x] 7.4 GREEN: create `ref-advanced-patterns.md` (~2,730 tokens); run test suite — confirm PASSED
- [x] 7.5 VERIFY: token sum of output files = source file tokens ± 50; confirm no content loss
- [x] 7.6 Remove `ref-advanced-cpp.md`

---

## Phase 8: Split `ref-core-language.md` ★ VERSION (2-way, 4,830 tokens)

> Boundary: C++17/20 version boundary. Output: `ref-core-type-safety.md`,
> `ref-core-modern-idioms.md`. This split provides version routing benefit.

- [x] 8.1 RED: write test asserting `ref-core-type-safety.md` exists and is ≤3,500 tokens; run test suite — confirm FAILED
- [x] 8.2 GREEN: create `ref-core-type-safety.md` (~2,701 tokens) — const, casts, nulls (all versions); run test suite — confirm PASSED
- [x] 8.3 RED: write test asserting `ref-core-modern-idioms.md` exists and is ≤3,500 tokens; run test suite — confirm FAILED
- [x] 8.4 GREEN: create `ref-core-modern-idioms.md` (~2,108 tokens) — C++17/20 idioms; run test suite — confirm PASSED
- [x] 8.5 VERIFY: token sum of output files = source file tokens ± 50; confirm no content loss
- [x] 8.6 Remove `ref-core-language.md`

---

## Phase 9: Split `ref-domain-modeling.md` (2-way, 4,766 tokens)

- [x] 9.1 RED: write test asserting `ref-domain-patterns.md` exists and is ≤3,500 tokens; run test suite — confirm FAILED
- [x] 9.2 GREEN: create `ref-domain-patterns.md` (~2,207 tokens); run test suite — confirm PASSED
- [x] 9.3 RED: write test asserting `ref-domain-quality.md` exists and is ≤3,500 tokens; run test suite — confirm FAILED
- [x] 9.4 GREEN: create `ref-domain-quality.md` (~2,530 tokens); run test suite — confirm PASSED
- [x] 9.5 VERIFY: token sum of output files = source file tokens ± 50; confirm no content loss
- [x] 9.6 Remove `ref-domain-modeling.md`

---

## Phase 10: Split `ref-legacy-smells.md` (2-way, 4,809 tokens)

- [x] 10.1 RED: write test asserting `ref-legacy-smells-structural.md` exists and is ≤3,500 tokens; run test suite — confirm FAILED
- [x] 10.2 GREEN: create `ref-legacy-smells-structural.md` (re-measure before creating); run test suite — confirm PASSED
- [x] 10.3 RED: write test asserting `ref-legacy-smells-patterns.md` exists and is ≤3,500 tokens; run test suite — confirm FAILED
- [x] 10.4 GREEN: create `ref-legacy-smells-patterns.md` (re-measure before creating); run test suite — confirm PASSED
- [x] 10.5 VERIFY: token sum of output files = source file tokens ± 50; confirm no content loss
- [x] 10.6 Remove `ref-legacy-smells.md`

---

## Phase 11: Split `ref-legacy-mental-models.md` (2-way, 4,706 tokens)

- [x] 11.1 RED: write test asserting `ref-mental-models-memory.md` exists and is ≤3,500 tokens; run test suite — confirm FAILED
- [x] 11.2 GREEN: create `ref-mental-models-memory.md` (re-measure before creating); run test suite — confirm PASSED
- [x] 11.3 RED: write test asserting `ref-mental-models-lang.md` exists and is ≤3,500 tokens; run test suite — confirm FAILED
- [x] 11.4 GREEN: create `ref-mental-models-lang.md` (re-measure before creating); run test suite — confirm PASSED
- [x] 11.5 VERIFY: token sum of output files = source file tokens ± 50; confirm no content loss
- [x] 11.6 Remove `ref-legacy-mental-models.md`

---

## Phase 12: Split `ref-build-toolchain.md` ★ VERSION (2-way, 4,736 tokens)

> Boundary: C++20 version boundary. Output: `ref-build-packages.md`, `ref-build-ubsan-msvc.md`.
> This split provides version routing benefit.

- [x] 12.1 RED: write test asserting `ref-build-packages.md` exists and is ≤3,500 tokens; run test suite — confirm FAILED
- [x] 12.2 GREEN: create `ref-build-packages.md` (~1,441 tokens) — vcpkg, CMake, all versions; run test suite — confirm PASSED
- [x] 12.3 RED: write test asserting `ref-build-ubsan-msvc.md` exists and is ≤3,500 tokens; run test suite — confirm FAILED
- [x] 12.4 GREEN: create `ref-build-ubsan-msvc.md` (~3,277 tokens) — C++20 modules, UBSan/MSVC; run test suite — confirm PASSED
- [x] 12.5 VERIFY: token sum of output files = source file tokens ± 50; confirm no content loss
- [x] 12.6 Remove `ref-build-toolchain.md`

---

## Phase 13: Split `ref-safety-aviation.md` (2-way, 4,274 tokens)

- [x] 13.1 RED: write test asserting `ref-safety-jni-abi.md` exists and is ≤3,500 tokens; run test suite — confirm FAILED
- [x] 13.2 GREEN: create `ref-safety-jni-abi.md` (~1,035 tokens); run test suite — confirm PASSED
- [x] 13.3 RED: write test asserting `ref-safety-far117-cwr.md` exists and is ≤3,500 tokens; run test suite — confirm FAILED
- [x] 13.4 GREEN: create `ref-safety-far117-cwr.md` (~3,174 tokens); run test suite — confirm PASSED
- [x] 13.5 VERIFY: token sum of output files = source file tokens ± 50; confirm no content loss
- [x] 13.6 Remove `ref-safety-aviation.md`

---

## Phase 14: Split `ref-safety-memory.md` (2-way, 4,251 tokens)

- [x] 14.1 RED: write test asserting `ref-safety-misra-do178.md` exists and is ≤3,500 tokens; run test suite — confirm FAILED
- [x] 14.2 GREEN: create `ref-safety-misra-do178.md` (~2,401 tokens); run test suite — confirm PASSED
- [x] 14.3 RED: write test asserting `ref-safety-memory-lifetime.md` exists and is ≤3,500 tokens; run test suite — confirm FAILED
- [x] 14.4 GREEN: create `ref-safety-memory-lifetime.md` (~1,873 tokens); run test suite — confirm PASSED
- [x] 14.5 VERIFY: token sum of output files = source file tokens ± 50; confirm no content loss
- [x] 14.6 Remove `ref-safety-memory.md`

---

## Phase 15: Split `ref-legacy-navigation.md` (2-way, 4,247 tokens)

> Boundary: H2 at line 90. `ref-legacy-navigation.md` keeps its name and is truncated to lines 1–89
> (~1,694 tokens ✓). `ref-legacy-triage-playbook.md` is created from the
> `## Legacy Codebase Triage Playbook` section (lines 90–352, ~2,464 tokens ✓).

- [x] 15.1 RED: write test asserting `ref-legacy-navigation.md` is ≤3,500 tokens; run test suite — confirm FAILED
- [x] 15.2 GREEN: truncate `ref-legacy-navigation.md` to lines 1–89 (remove `## Legacy Codebase Triage Playbook` section and below); run test suite — confirm PASSED
- [x] 15.3 RED: write test asserting `ref-legacy-triage-playbook.md` exists and is ≤3,500 tokens; run test suite — confirm FAILED
- [x] 15.4 GREEN: create `ref-legacy-triage-playbook.md` from `## Legacy Codebase Triage Playbook` section (lines 90–352 of original `ref-legacy-navigation.md`); run test suite — confirm PASSED
- [x] 15.5 VERIFY: token sum of `ref-legacy-navigation.md` + `ref-legacy-triage-playbook.md` = 4,247 ± 50; confirm no content loss

---

## Phase 16: Update `reference-index.md`

> Rewrite the index to list all 31 files. Annotate the 4 ★ version-split file pairs with
> their version boundaries. Verify the index itself remains ≤1,500 tokens.

- [ ] 16.1 Rewrite `reference-index.md` — 31 file entries, ★ version annotations
- [ ] 16.2 Verify `reference-index.md` ≤1,500 tokens
- [ ] 16.3 Update `docs/guides/avatars/split-reference-architecture.md` — replace the 14-file "File Structure" listing with the 31-file post-split listing; update all old file names
- [ ] 16.4 Update token budget math in `docs/guides/avatars/split-reference-architecture.md` "Token Budget Design" section with post-split figures (16 → 31 files; avg ~2,456t)

---

## Phase 17: Update `avatars/AVATAR-RAG-INDEX.yaml` (Required Co-Change)

> This is a hard dependency — constitution-lint `index_integrity` will fail if this is skipped.
> All 40+ query routing examples must be re-pointed to the new file names.
> The routing update has four distinct sub-scopes (one per version-split file pair) plus general cleanup.

- [ ] 17.1 Update token counts for all 31 split files in the cpp avatar section (remove 14 old entries, add 31 new entries with measured token counts)
- [ ] 17.2 Re-point concurrency routing examples: `→ ref-concurrency.md` → `→ ref-concurrency-threading.md` (thread/mutex/atomic queries) or `→ ref-concurrency-async.md` (coroutine/stop_token/C++20 async queries)
- [ ] 17.3 Re-point testing routing examples: `→ ref-testing-ci.md` → `→ ref-testing-ci-policy.md` (policy/gate queries) or `→ ref-testing-gtest-core.md` / `→ ref-testing-gtest-advanced.md` (GTest pattern queries)
- [ ] 17.4 Re-point migration routing examples: `→ ref-migration-playbooks.md` → `→ ref-migration-pre-cpp17.md` (C++98/03/11/14 migration queries) or `→ ref-migration-cpp17-plus.md` (C++17/20 migration queries)
- [ ] 17.5 Re-point brownfield routing examples: `→ ref-brownfield-config.md` → `→ ref-brownfield-adoption.md` (adoption/onboarding queries) or `→ ref-brownfield-project-config.md` (per-tier config queries)
- [ ] 17.6 Re-point all remaining 9 source-file routing examples to their new split pair names (advanced-cpp, core-language, domain-modeling, legacy-navigation, legacy-smells, legacy-mental-models, build-toolchain, safety-aviation, safety-memory, object-design)
- [ ] 17.7 Run `aa-constitution-lint .` — confirm `index_integrity` passes with 0 failures

---

## Phase 18: Final Verification

- [ ] 18.1 Verify all 31 reference files ≤3,500 tokens (automated check)
- [ ] 18.2 Verify total reference corpus tokens = 76,152 ± 200
- [ ] 18.3 Verify zero broken internal links in `reference-index.md`
- [ ] 18.4 Search repo for any remaining references to the 14 renamed source files (from task 1.5 list) — confirm all updated or confirmed acceptable
- [ ] 18.5 Run full test suite — confirm green
- [ ] 18.6 Run `aa-constitution-lint .` — confirm 0 failures
- [ ] 18.7 Spot-check each split file against its source for missing H2/H3 sections — confirm all sections present in exactly one output file (no section dropped, no section duplicated)
- [ ] 18.8 Verify `reference-index.md` routing descriptions match the actual section titles in each split file — no stale names
- [ ] 18.9 Verify `docs/guides/avatars/split-reference-architecture.md` File Structure listing matches actual directory contents (31 files)

---

## Phase 19: Reorganize into `refs/` Subdirectories

> **Goal:** Move all 31 flat reference files into four topic subdirectories for human
> navigation. Finalize all link paths in `reference-index.md` and `AVATAR-RAG-INDEX.yaml`.
> Runs after Phase 18 confirms all content is correct at flat paths.

- [ ] 19.1 Create four subdirectories: `avatars/technology/cpp/refs/language/`, `refs/safety/`, `refs/testing/`, `refs/legacy/`
- [ ] 19.2 Move 9 language files into `refs/language/`: `ref-getting-started.md`, `ref-core-type-safety.md`, `ref-core-modern-idioms.md`, `ref-templates-metaprogramming.md`, `ref-advanced-patterns.md`, `ref-domain-patterns.md`, `ref-domain-quality.md`, `ref-object-design-rehabilitation.md`, `ref-object-design-patterns.md`
- [ ] 19.3 Move 6 safety files into `refs/safety/`: `ref-safety-misra-do178.md`, `ref-safety-memory-lifetime.md`, `ref-safety-jni-abi.md`, `ref-safety-far117-cwr.md`, `ref-concurrency-threading.md`, `ref-concurrency-async.md`
- [ ] 19.4 Move 6 testing files into `refs/testing/`: `ref-testing-ci-policy.md`, `ref-testing-gtest-core.md`, `ref-testing-gtest-advanced.md`, `ref-build-packages.md`, `ref-build-ubsan-msvc.md`, `ref-infrastructure.md`
- [ ] 19.5 Move 10 legacy files into `refs/legacy/`: `ref-legacy-navigation.md`, `ref-legacy-triage-playbook.md`, `ref-legacy-smells-structural.md`, `ref-legacy-smells-patterns.md`, `ref-mental-models-memory.md`, `ref-mental-models-lang.md`, `ref-brownfield-adoption.md`, `ref-brownfield-project-config.md`, `ref-migration-pre-cpp17.md`, `ref-migration-cpp17-plus.md`
- [ ] 19.6 Update `reference-index.md` — replace all flat `ref-*.md` links with `refs/<group>/ref-*.md` paths
- [ ] 19.7 Update `avatars/AVATAR-RAG-INDEX.yaml` — replace all flat cpp ref paths with `refs/<group>/ref-*.md` subdirectory paths
- [ ] 19.8 Update `docs/guides/avatars/split-reference-architecture.md` File Structure tree to show the final `refs/` subdirectory layout
- [ ] 19.9 Update any test files that assert file existence at flat paths — redirect to subdirectory paths (check 2.9, 3.7, 4.7 test updates)
- [ ] 19.10 Run `aa-constitution-lint .` — confirm `index_integrity` passes with 0 failures at subdirectory paths
- [ ] 19.11 Run full test suite — confirm green at final path layout

---

## Phase 20: Merge and Archive

- [ ] 20.1 Merge PR to main
- [ ] 20.2 Archive this change directory: `mv hangar-ai-specs/changes/cpp-ref-file-rightsizing hangar-ai-specs/archive/$(date +%Y-%m-%d)-cpp-ref-file-rightsizing`
- [ ] 20.3 Update `PROGRESS.md` status to `COMPLETE`
