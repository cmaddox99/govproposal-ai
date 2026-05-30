# Tasks: Folly GTest Enrichment

## Progress: 34 / 34 complete

- [x] FOLLY-01 — Add `googletest_canonical_patterns` conventions to manifest.yaml ✓ b9a328e
- [x] FOLLY-02 — GTest Core Macro Reference section (TEST, EXPECT/ASSERT decision table, ADD_FAILURE, static_assert) ✓ 7df37dc
- [x] FOLLY-03 — GTest Exception Testing section (EXPECT_THROW, EXPECT_ANY_THROW, EXPECT_NO_THROW) ✓ 2604cb4
- [x] FOLLY-04 — GTest Template Test Helper Pattern section (Folly template helper → TEST()) ✓ 3fdf3d7
- [x] FOLLY-05 — GTest Fixture Deep Dive section (minimal fixture, SetUp/TearDown, RAII teardown) ✓ 3fdf3d7
- [x] FOLLY-06 — GTest Concurrency Testing section (std::thread, atomic, mutex from Folly) ✓ 3fdf3d7
- [x] FOLLY-07 — ActiveTest.h → GoogleTest Migration Playbook section ✓ 3fdf3d7
- [x] FOLLY-08 — New example `ENG-4.1-googletest-migration.md` (≤600 tokens) ✓ pending

## Amendment R — RAG Token Budget Correction & ref-safety-memory Split

- [x] R-01 — Create `ref-safety-aviation.md` — extract JNI safety, FAR 117, CWR anti-patterns, DO-278A from `ref-safety-memory.md` ✓ c0aa308
- [x] R-02 — Trim `ref-safety-memory.md` — remove extracted sections; verify ≤3,500t ✓ c0aa308
- [x] R-03 — Add `ref-safety-aviation.md` row to `reference-index.md` ✓ c0aa308
- [x] R-04 — Update `AVATAR-RAG-INDEX.yaml` — reroute queries, fix all stale token estimates, sync version to 2.3.0, disambiguate exception-safety collision, reorder FAR 117 query ✓ c0aa308
- [x] R-05 — Update tests referencing sections moved from `ref-safety-memory.md` to `ref-safety-aviation.md` ✓ c0aa308
- [x] R-06 — Verify: `aa-constitution-lint .` passes; all token estimates confirmed accurate ✓ c0aa308

## Amendment S — Workflow & Skill Coherence Fixes

- [x] S-01 — Consolidate 4 `ref-testing-ci.md` rows in `reference-index.md` → 1 descriptive row
- [x] S-02 — Add ActiveTest/TestRunner.lib trigger phrases to `skill-cpp-legacy-modernization.md`

## Amendment T — C++ Technical Clarity Improvements (Advisory)

- [x] T-01 — Add MFC constructor injection comment to `ENG-4.1-googletest-migration.md` fixture
- [x] T-02 — Expand CRITICAL_SECTION cross-reference note in `ref-testing-ci.md` concurrency section
- [x] T-03 — Replace `OrderService`/`MockOrderRepository` with aviation-domain equivalent in `ENG-4.1-atomic-tdd.md`

## Amendment U — Constitutional Compliance: Edge Cases Quality Gate (🔴 BLOCKING)

- [x] U-01 — Add `## Edge Cases & Warnings` to `ENG-4.1-atomic-tdd.md`
- [x] U-02 — Add `## Edge Cases & Warnings` to `ENG-4.1-googletest-migration.md`
- [x] U-03 — Add `## Edge Cases & Warnings` to `ENG-2.3-jni-abi-stability.md`
- [x] U-04 — Add `## Edge Cases & Warnings` to `ENG-2.3-rcptr-abi-stability.md`
- [x] U-05 — Add `## Edge Cases & Warnings` to `ENG-6.1-host-exception-safety.md`
- [x] U-06 — Add `## Edge Cases & Warnings` to `ENG-6.1-safety-critical-jni.md`
- [x] U-07 — Add ENG-13.1 non-applicability comment to `manifest.yaml`

## Amendment V — BLOCKING: CI Unit Test Gate (P2, P5)

- [x] V-01 — Add `pythonpath = ["."]` to `pyproject.toml` `[tool.pytest.ini_options]`
- [x] V-02 — Add `unit-tests` job to `.github/workflows/governance-tests.yml` running `pytest tests/unit/ -v`

## Amendment W — Test Quality & Metadata Fixes (P5, P7)

- [x] W-01 — Fix `skill-cpp-jni-bridge.md` `category: development-practices` to `category: platform-engineering`
- [x] W-02 — Update `ENG-4.1-googletest-migration.md` title to include `IOC_ALP:` prefix
- [x] W-03 — Tighten `test_gtest_exception_section_references_calp_exception` to proximity check
- [x] W-04 — Add `test_followed_by_references_are_valid` to `test_rag_index.py`

## Amendment X — Advisory: Safety Guidance Depth (P6)

- [x] X-01 — Add WCET annotation subsection to `ref-safety-aviation.md` (200 tokens max)
- [x] X-02 — Add timeout/default-result edge case to `ENG-4.1-far117-traceability.md` Edge Cases
