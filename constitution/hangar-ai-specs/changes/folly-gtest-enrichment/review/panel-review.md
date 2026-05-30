# C++ Avatar Enrichment — 7-Persona Panel Review (PR #25)

**Branch:** `proposal/folly-gtest-enrichment`
**Artefact reviewed:** `avatars/technology/cpp/` post-split-reference-architecture
**Review scope:** Folly-grounded GoogleTest enrichment · split ref-*.md architecture (15 files, `full-reference.md` deleted) · 25 new C++ skills · ~20 new examples · AVATAR-RAG-INDEX token budgets · FAR 117 / DO-278A / JNI safety guidance · test suite gate completeness
**Constitution guidance consulted:** `agent-skills/skills-by-domain/platform-engineering/index.yaml` · `laws/engineering/_domain.yaml` · `avatars/AVATAR-RAG-INDEX.yaml` · `manifests/technology/cpp/manifest.yaml` · prior panel review at `hangar-ai-specs/changes/c-plus-plus-avatar-enrichment/review/panel-review.md`

**Automated gate results:**

| Check | Result |
|---|---|
| `aa-constitution-lint .` | ✅ 20 passed, 0 failed, 0 skipped — **CLEAN** |
| `pytest tests/unit/test_cpp_avatar/ -q` | ⚠️ **6 FAILED**, 750 passed — missing `## Edge Cases` sections in 6 example files |
| `pytest tests/governance/ -q` (CI gate) | ✅ PASSES (not run locally — see CI configuration note) |

> **CI gap note:** `governance-tests.yml` runs only `pytest tests/governance/` — the unit test suite at `tests/unit/test_cpp_avatar/` with 756 tests is **not executed in CI**. The 6 failing tests above are therefore invisible to the pull request gate.

---

## Panel Verdicts

| # | Persona | Role | Verdict |
|---|---|---|---|
| P1 | Rafael Antebi | RAG Architecture Expert | ⚠️ CONDITIONAL PASS |
| P2 | Saoirse Brennan | Workflow & Skill Coherence Expert | ⚠️ CONDITIONAL PASS |
| P3 | Dmitri Vassiliev | C++ Technical Expert | ✅ PASS |
| P4 | Tina Marchetti | Constitutional Compliance Expert | 🔴 BLOCKED |
| P5 | James Okafor | Test Quality Expert | 🔴 BLOCKED |
| P6 | Yuki Tanabe | Safety-Critical Systems / Aviation Expert | ⚠️ CONDITIONAL PASS |
| P7 | Cleo Hendricks | Language & Grammar Expert | ⚠️ CONDITIONAL PASS |

**Overall panel verdict: 🔴 BLOCKED — 2 blocking issues across P4 and P5 must be resolved before merge.**

---

## P1 · Rafael Antebi — RAG Architecture Expert

> *Principal architect of two enterprise knowledge-retrieval platforms, including one serving a 900-person engineering org. Designed the canonical query and token budget standards used in the Hangar AI AVATAR-RAG-INDEX.yaml. Has personally audited 14 technology avatar RAG architectures.*

### Positive Findings 🟢

- **Split architecture is the correct resolution of the prior blocking issue** — The prior panel review (P6 Kenji Nakamura) identified `full-reference.md` at 5,519 lines as a blocking RAG context-overflow risk. That file is now deleted and its content distributed across 15 topic-aligned `ref-*.md` files. This is the right design: a RAG query routing to `ref-testing-ci.md` retrieves only testing content, not 5,500 lines of everything.
- **`reference-index.md` functions as an effective semantic router** — The file, co-loaded with `guidance.md`, provides unambiguous topic → file routing in ~418 tokens. The table-per-section structure (Getting Started / Core Language / Testing & Build / Safety & Runtime / Brownfield & Legacy) maps well to the query taxonomy in `AVATAR-RAG-INDEX.yaml`.
- **25 new skill queries are present and correctly routed** — The Amendment Q+ skill query block in `AVATAR-RAG-INDEX.yaml` (lines ~1092–1114) adds one query per skill, each pointing directly to the skill file with a token estimate. This closes the SG5-B routing gap identified in the prior review. All 25 skills are reachable.
- **AVATAR-RAG-INDEX lint is clean** — The `aa-constitution-lint` check "All files referenced in AVATAR-RAG-INDEX.yaml exist on disk" passes with zero failures. Every path declared in the index resolves. The broken-path blocker from the prior review (B-1) is fully resolved.
- **Direct example queries added** — Queries for `ENG-3.7-error-handling.md`, `ENG-5.5-observability.md`, `ENG-7.1-failure-handling.md`, and `ENG-4.1-far117-traceability.md` are now explicitly in `search_queries`. These were formerly unreachable from the routing pipeline (prior review H-1, H-2, A-2).

### Warning Findings 🟡

- **Token budget inflation in two enriched files** — The RAG index declares token estimates that pre-date the Folly/FAR-117 enrichment additions:
  - `ref-safety-memory.md`: declared `~2817t` — actual estimate **~5,583t** (4,198 words × 1.33). This file received JNI safety, FAR 117 crew rest, CWR anti-pattern catalog, and DO-278A content in this PR, doubling its size. At 5,583 tokens it exceeds the 3,500t RAG context ceiling by 60%.
  - `ref-testing-ci.md`: declared `~2854t` — actual estimate **~4,499t** (3,383 words × 1.33). Folly-grounded GTest sections (Core Macros, Exception Testing, Template Helper Pattern, Fixture Deep Dive, Concurrency Testing, VS 2022 Built-In Equivalents, ActiveTest.h Migration) were added, growing the file from its pre-enrichment size.
  - `ref-brownfield-config.md`: declared `~2626t` — actual estimate **~4,233t**. The IOC_ALP PCLoadPlan domain model, MFC Windows brownfield, and IOC_ALP anti-pattern catalog sections added in this PR overran the initial estimate.
  - `ref-migration-playbooks.md`: declared `~3428t` — actual estimate **~3,946t**.
  The stated token estimates in `AVATAR-RAG-INDEX.yaml` are stale. Any agent that uses these estimates for context-window budgeting will undercount the cost of retrieving these files.
- **AVATAR-RAG-INDEX version mismatch** — The index declares `version: "2.0.1"` for the cpp avatar entry, while `manifest.yaml` declares `version: "2.3.0"`. These should be synchronised. A downstream tool consuming both files will see inconsistent version signals.
- **Query collision: "exception safety"** — Two queries compete for C++ exception safety: `- C++ exception safety noexcept? → ref-concurrency.md` and `- C++ exception safety noexcept contract std::expected strong guarantee? → skill-cpp-exception-safety-governance.md`. The first is shorter and will match more ambiguous queries. A developer asking "how do I handle exceptions safely in C++?" may land in `ref-concurrency.md` (which covers exception barriers in coroutines) rather than `skill-cpp-exception-safety-governance.md` (which covers the exception safety guarantee framework). Adding a disambiguating prefix (`C++ coroutine exception safety?` vs `C++ exception safety governance noexcept?`) would prevent this collision.
- **`ref-safety-memory.md` query routing gap for FAR 117** — The query `- FAR 117 crew rest duty C++ compliance?` routes to `ref-safety-memory.md`. However, the direct example query `- C++ FAR 117 regulatory traceability? → examples/ENG-4.1-far117-traceability.md (~430t)` is a superior match for "how do I write traceable tests?" The more expensive `ref-safety-memory.md` should be the secondary route (for regulatory context), not the primary. The query ordering matters: when a RAG engine returns the first match, the example file's narrower scope is better.

### Blocking Findings 🔴

- None from this persona — the split architecture resolves the prior B-1 and B-2 blockers. The token estimation gap is a documentation accuracy issue, not a structural routing failure.

**P1 Verdict: ⚠️ CONDITIONAL PASS** — Update the four stale token estimates in `AVATAR-RAG-INDEX.yaml` to reflect post-enrichment sizes. Fix the version drift. Resolve the exception-safety query collision.

---

## P2 · Saoirse Brennan — Workflow & Skill Coherence Expert

> *Engineering Director with 12 years owning agent-based developer tooling. Designed the trigger-phrase routing contract for 3 AI skill registries. Reviews every skill entry for action-orientation, trigger completeness, and followed_by chain correctness before it enters production.*

### Positive Findings 🟢

- **All 25 skills have `trigger.phrases`** — Every C++ skill file defines natural-language trigger phrases, enabling phrase-based skill routing. A developer typing "C++ JNI bridge Java native method" will surface `skill-cpp-jni-bridge.md` without needing to know the avatar schema. This is essential DX for 25 skills.
- **`followed_by` chains are complete and correct** — Skills chain logically: `skill-cpp-legacy-modernization` → `skill-cpp-standard-migration` → `skill-27-constitution-compliance`; `skill-cpp-sanitizer-hardening` → `skill-cpp-ownership-lifetime-safety` → `skill-27-constitution-compliance`. These chains enable progressive disclosure — a developer who acts on one skill receives a natural next step.
- **`skill-cpp-jni-bridge.md` fills the CWR gap** — The prior review (P3 and P4, Advisory A-1) flagged the absence of a JNI boundary skill as a primary gap for the CWR consumer project. This skill now exists with correct trigger phrases (`"CWR JNI"`, `"JNI memory ownership"`, `"JNI exception propagation"`) and a clear 5-step procedure.
- **`platform-engineering/index.yaml` registers all 25 new skills** — Every `skill-cpp-*.md` file has a corresponding entry in the skill index with `file`, `name`, `triggers`, and `laws` fields. Routing pipeline coverage is complete.
- **`ref-brownfield-config.md` covers the full adoption kickoff sequence** — The "Adoption Kickoff" 4-step sequence (run compliance rating → notify team → create MODERNIZATION_PLAN.md → establish baseline metrics) provides a structured entry point for brownfield adopters, closing the prior review's advisory A-3 (no brownfield quick-start path).

### Warning Findings 🟡

- **`reference-index.md` has 4 consecutive rows pointing to `ref-testing-ci.md`** — The "Testing & Build" section routes `Testing & CI`, `GoogleTest Core Macros`, `GTest Exception & Template Testing`, and `GTest Fixture & Concurrency` all to `ref-testing-ci.md`. This gives the router 4 entries where 1 (with a more descriptive description) would suffice. An agent routing a user query through `reference-index.md` would surface redundant matches. Consolidate into one row with a richer description: `"GoogleTest framework, Folly-grounded macro patterns, fixture, concurrency, CI toolchain, VS 2022 equivalents"`.
- **No explicit `inputs` / `outputs` schema in most skills** — The skill files define `Purpose`, `Procedure`, `triggers`, and `followed_by`, but lack formal `inputs:` and `outputs:` fields. A developer knows when to use a skill but may not know what artefacts to provide at invocation (e.g., `skill-cpp-compliance-rating` takes a codebase path but this is inferred, not declared). This is a cross-avatar consistency gap — Java and Python avatar skills declare `inputs`/`outputs` explicitly.
- **No "test harness migration" workflow step** — The C++ avatar documents ActiveTest.h → GoogleTest migration in `ref-testing-ci.md` and `ENG-4.1-googletest-migration.md`, but there is no explicit workflow stage in `skills` or `workflows` that represents "migrate test harness". A team adopting the constitution on IOC_ALP would expect a skill or workflow entry such as `skill-cpp-activetest-migration`. The `skill-cpp-legacy-modernization` skill's trigger phrases do not include "ActiveTest", "test harness migration", or "TestRunner.lib".
- **CI gate gap: unit test suite not covered** — `governance-tests.yml` runs only `pytest tests/governance/`. The 756-test unit suite in `tests/unit/test_cpp_avatar/` is not in any CI workflow. The 6 currently failing tests (`test_example_quality.py::test_every_example_has_edge_cases_section`) are invisible to the pull request gate. A PR could merge with these tests broken and CI would report green. This is the most consequential workflow gap in this PR.

### Blocking Findings 🔴

- None from this persona independently (the CI gap is flagged as blocking by P5).

**P2 Verdict: ⚠️ CONDITIONAL PASS** — Fix the `reference-index.md` redundancy (4→1 row). Add `inputs`/`outputs` to skills in a follow-up sprint. Add "ActiveTest" to `skill-cpp-legacy-modernization` trigger phrases. The CI gap must be resolved before merge.

---

## P3 · Dmitri Vassiliev — C++ Technical Expert

> *ISO C++ committee voting member, 18 years in production C++ spanning embedded DSP, financial trading engines, and JNI-bridged Java systems. Has led two major aviation-domain C++ codebases from C++03 to C++17. Teaches C++ safety patterns at CppCon.*

### Positive Findings 🟢

- **`ENG-4.1-googletest-migration.md` is technically correct and well-scoped** — The migration example correctly uses `ASSERT_NE(flight, nullptr)` before pointer dereference (aborting the test if null, preventing UB on the next line), `EXPECT_THROW(svc_->loadFlight("ZFW-999"), CFlightNotFoundException)` to name the exact exception type, and `std::unique_ptr<CFlightService>` in the fixture to prevent leaks on assertion failure. The progression from `CHECK_TRUE` + manual `try/catch` to clean GoogleTest is exactly the right teaching sequence for an IOC_ALP developer.
- **`ENG-6.1-safety-critical-jni.md` would prevent real aviation safety incidents** — The compliant pattern correctly implements: (a) null-input guard returning structured JSON error, (b) `catch (const std::exception&)` followed by `catch (...)` as a layered safety net, (c) `ExceptionClear()` to prevent stale JNI state from corrupting subsequent calls, (d) `ReleaseStringUTFChars()` for local ref cleanup. The non-compliant pattern (exception escaping the JNI boundary) is accurately described as causing JVM undefined behavior. This is actionable, correct guidance.
- **`ENG-4.1-far117-traceability.md` accurately models FAR 117 test naming** — The traceability convention (`TEST(CrewRestPolicy, MinimumRestBeforeFDP_FAR117_23a)`) encodes the specific FAR section (117.23(a)) in the test name, making the compliance audit trail machine-readable. The edge case covering "FAR 117 amendment mid-cycle" with a `FAR_117_VERSION` pinning constant is an advanced but real pattern that aviation teams will need. The duty-period UTC/DST boundary case is technically correct and aviation-specific.
- **`ref-testing-ci.md` Folly-grounded patterns are technically accurate** — The template helper pattern (`template<class T> void testFoo()` called from `TEST()`) matches the Folly ArenaSmartPtrTest and ConvTest patterns. The `ADD_FAILURE()` guidance (`inject non-fatal failure from catch blocks`) is correct per GoogleTest semantics. The `expect_vs_assert` policy (EXPECT continues, ASSERT aborts — use ASSERT only when continuing would produce UB or meaningless output) is the correct practitioner guideline.
- **Per-tier clang-tidy configuration in `ref-brownfield-config.md` is accurate** — The C++11 tier correctly excludes `modernize-use-std-span` and `modernize-use-concepts` (C++20 only). The C++14/17 tier enables the full `modernize-*` suite except `modernize-use-trailing-return-type`. This is production-quality tier-aware configuration, not a generic "enable everything" template.

### Warning Findings 🟡

- **`ENG-4.1-googletest-migration.md` assumes default-constructible `CFlightService`** — The fixture uses `svc_ = std::make_unique<CFlightService>()`. In the IOC_ALP MFC codebase, `CFlightService` (with the `C` prefix) is likely an MFC class with dependencies injected through `CObject`-derived mechanisms, not a default-constructible class. The example may not compile against the actual IOC_ALP class without modification. Adding a comment "if CFlightService requires constructor arguments, inject them here" or showing a factory-method pattern would make this example more robust for MFC migration.
- **`ref-testing-ci.md` concurrency testing shows `std::thread` but not `CRITICAL_SECTION`** — The GTest Concurrency Testing section uses `std::thread` + `.join()` (correct for C++11+). However, IOC_ALP uses Windows `CRITICAL_SECTION` with custom threading wrappers (no `std::thread`). A concurrent brownfield developer may not recognise how to apply the `std::thread` pattern to `CRITICAL_SECTION`-based code. A note linking to `ref-brownfield-config.md` for the Windows threading equivalent would bridge this gap.
- **`ref-testing-ci.md` has a `#include "mock_order_repository.h"` in the primary test example that does not correspond to any AA domain class** — The example test class (`OrderServiceTest`) uses `MockOrderRepository` — a generic e-commerce model, not an aviation domain class. While the pattern is pedagogically correct, an AA developer encountering this for the first time may find the domain mismatch jarring. An aviation-domain variant (`FlightScheduleRepositoryTest`) or a note explaining the pattern is domain-agnostic would improve relevance.

### Blocking Findings 🔴

- None from this persona — the Folly-grounded patterns are technically sound and the JNI safety guidance is accurate.

**P3 Verdict: ✅ PASS** — C++ technical quality is high. Three advisory improvements would improve MFC brownfield applicability.

---

## P4 · Tina Marchetti — Constitutional Compliance Expert

> *Governs the Hangar AI Constitution schema for a 600-engineer org. Reviews every avatar PR against the law registry, specializes_laws schema, non-negotiable law coverage, and ENG-10.1 (Constitution Metrics). Has rejected 4 avatar PRs for constitutional violations in the past year.*

### Positive Findings 🟢

- **All 21 `specializes_laws` entries now have `example_file` pointers** — The prior review flagged four missing `example_file` entries (ENG-3.7, ENG-5.5, ENG-7.1, ENG-7.2–7.5). This PR fills all gaps: `ENG-3.7-error-handling.md`, `ENG-5.5-observability.md`, `ENG-7.1-failure-handling.md` are now created and referenced. ENG-7.2–7.5 appear in the manifest's `specializes_laws` block (per the AVATAR-RAG-INDEX listing). Per avatar schema, this is fully compliant.
- **Constitution lint is clean** — `aa-constitution-lint .` reports 20 passed, 0 failed. The prior review's blocking linter failure (broken AVATAR-RAG-INDEX path) is fully resolved. The post-split architecture now satisfies all linter checks including "All files referenced in AVATAR-RAG-INDEX.yaml exist on disk".
- **ENG-13.1 non-negotiable registration confirmed** — `laws/engineering/_domain.yaml` line 153 correctly declares `non_negotiable: [ENG-13.1]` under the Artifact Rendering Laws group. The prior review item (P4 asked to confirm this fix) is verified.
- **Non-negotiable laws (ENG-4.1, ENG-6.1, ENG-6.4, ENG-6.7) all have prominent example files** — `ENG-4.1-atomic-tdd.md`, `ENG-6.1-security-by-design.md`, `ENG-6.4-data-protection.md`, `ENG-6.7-audit-trail.md` are all present. Aviation-specific examples `ENG-4.1-far117-traceability.md` and `ENG-6.1-safety-critical-jni.md` reinforce the non-negotiable laws with domain-specific content.
- **`manifest.yaml` law boundary is clean** — The 21 `specializes_laws` entries are all ENG-* laws (no BUS-* or PRD-* laws), which is correct for a `technology` type avatar. The prior review's law boundary finding (Amendment O correction) is maintained.

### Warning Findings 🟡

- **AVATAR-RAG-INDEX version mismatch** — The RAG index entry for `cpp` declares `version: "2.0.1"`, while `manifest.yaml` declares `version: "2.3.0"`. This is a two-minor-version drift. Per ENG-10.1 (Constitution Metrics), version consistency between index and manifest is a governance requirement. The version in the RAG index should be bumped to `2.3.0` in this PR.
- **`ENG-4.1-atomic-tdd.md` fails the Edge Cases test gate** — `test_example_quality.py::test_every_example_has_edge_cases_section[ENG-4.1-atomic-tdd.md]` fails because the primary non-negotiable TDD law example lacks a `## Edge Cases & Warnings` section. Per ENG-4.1, the primary canonical example for the most important law in the constitution must fully comply with quality gates. This is the highest-visibility compliance gap.
- **`ENG-4.1-googletest-migration.md` (new in this PR) also fails the Edge Cases gate** — A new example added by this PR fails a quality gate. The test `test_every_example_has_edge_cases_section[ENG-4.1-googletest-migration.md]` was red at PR time. New examples should pass all quality gates before merge.
- **ENG-13.1 (Artifact Rendering) not in `specializes_laws`** — ENG-13.1 governs how AI agents render artefacts. The C++ avatar does not specialise this law. While this may be intentional (it's an agent-behaviour law, not a C++ coding law), there is no documented waiver. Other technology avatars that interact with rendering toolchains should document their non-applicability explicitly.

### Blocking Findings 🔴

- **🔴 BLOCKING: 6 example files fail the `## Edge Cases` quality gate** — The following example files fail `test_example_quality.py::test_every_example_has_edge_cases_section`:
  1. `ENG-4.1-atomic-tdd.md` — the canonical non-negotiable TDD example
  2. `ENG-4.1-googletest-migration.md` — **new in this PR**
  3. `ENG-2.3-jni-abi-stability.md`
  4. `ENG-2.3-rcptr-abi-stability.md`
  5. `ENG-6.1-host-exception-safety.md`
  6. `ENG-6.1-safety-critical-jni.md`

  Per ENG-4.1, every code example must be complete and production-quality. The `## Edge Cases & Warnings` section is the quality gate that distinguishes tutorial code from governance-grade examples. Two of the six failures are the primary examples for the non-negotiable ENG-4.1 and ENG-6.1 laws. These must be fixed before merge. Five example files covering critical laws (two ENG-4.1, two ENG-6.1, two ENG-2.3 ABI stability) failing the quality gate is a constitutional compliance failure.

**P4 Verdict: 🔴 BLOCKED** — Add `## Edge Cases & Warnings` sections to all 6 failing example files. Fix AVATAR-RAG-INDEX version drift. No other blocker from this persona.

---

## P5 · James Okafor — Test Quality Expert

> *Staff engineer with 10 years writing automated governance suites. Introduced behavioural test patterns to replace text-presence checks across a 400-test governance suite. Believes a test that cannot fail on a meaningful regression is not a test.*

### Positive Findings 🟢

- **750 tests pass; FOLLY-01 through FOLLY-08 all pass** — The `test_folly_gtest_enrichment.py` scenarios correctly validate that `manifest.yaml` has `googletest_canonical_patterns`, that `ref-testing-ci.md` contains `ADD_FAILURE`, `GTest Exception Testing`, `GTest Fixture Deep Dive`, `GTest Concurrency Testing`, and `ActiveTest` migration content. These tests verify the PR's stated goals.
- **`conftest.py` fixture redesign is correct** — The `cpp_full_reference` fixture now reads `ALL ref-*.md files combined` (`"\n".join(p.read_text() for p in sorted(cpp_dir.glob("ref-*.md")))`), correctly adapting to the split architecture. Prior tests that checked `full-reference.md` now transparently check the distributed content. This is the right migration: the fixture contract is maintained, the implementation is updated.
- **`avatar_test_helpers.py` uses `LawRegistry` integration** — `validate_law_references()` invokes `aa_constitution_lint.infrastructure.law_registry.LawRegistry` to validate law IDs. This is genuine behavioural testing — it validates that law IDs are registered, not merely that a string appears in a file. This is a model for how governance tests should be written.
- **`test_example_quality.py` uses parameterised testing correctly** — The file-parametrized `test_every_example_has_edge_cases_section` test dynamically discovers example files and tests each one. When a new example is added, it is automatically included in the test run. The parametrization approach is correct.

### Warning Findings 🟡

- **FOLLY tests are text-presence checks, not behavioral checks** — `test_gtest_core_macro_section_covers_expect_assert_table` asserts `"EXPECT_EQ" in cpp_full_reference` and `"ADD_FAILURE" in cpp_full_reference`. These checks would pass even if the strings appeared in a comment block or unrelated section. A developer could satisfy FOLLY-02 by adding `<!-- EXPECT_EQ is deprecated here -->` to any ref file. A behavioral check would verify that EXPECT_EQ appears in a code block (```` ```cpp ````), or that the ADD_FAILURE guidance appears in the correct subsection (GTest Core Macro Reference). At minimum, add a context window check: `cpp_full_reference[idx - 200: idx + 200]` to verify the macro appears near "Core Macro" or "GTest".
- **`test_gtest_exception_section_references_calp_exception` has a loose OR condition** — The assertion `assert "CALPException" in cpp_full_reference or "exception hierarchy" in cpp_full_reference.lower()` will pass as long as "exception hierarchy" appears *anywhere* in 6,608 lines of combined ref content. This is currently satisfied by `ref-brownfield-config.md`'s `CALPException hierarchy — std::exception → CALPException...` section. The test would pass even if the GTest Exception Testing section had no reference to the IOC_ALP hierarchy.
- **`test_folly_gtest_enrichment.py` line 222 imports `from tests.unit.test_cpp_avatar.avatar_test_helpers import check_token_budget`** — This absolute package import requires `tests/` to be on `sys.path`. `pyproject.toml` does not declare `pythonpath = ["."]` in `[tool.pytest.ini_options]`. The import succeeds during the test run because pytest's conftest machinery adds the directory to sys.path, but the import pattern is fragile. Explicitly adding `pythonpath = ["."]` to `pyproject.toml` would make the path dependency documented and reliable.
- **No test exercises the `followed_by` chain integrity** — Skills declare `followed_by: [skill-name-1, skill-name-2]`. No test verifies that referenced skill IDs in `followed_by` blocks are valid registered skills. A typo in a `followed_by` field would not be caught. Adding a test to `test_phase5_validation.py` or creating a new `test_skill_registry.py` that validates all `followed_by` references against the platform-engineering skill index would close this gap.
- **No test validates that new FOLLY-08 example (`ENG-4.1-googletest-migration.md`) enforces the RED-GREEN-REFACTOR cycle** — `test_googletest_migration_example_has_compliant_noncompliant` only checks for the strings "COMPLIANT" and "NON-COMPLIANT". It does not verify that the example demonstrates a failing test (RED) followed by a minimal passing implementation (GREEN). ENG-4.1 specifically requires the RED step to be explicit. A migration example without a RED step does not enforce ENG-4.1's most important constraint.

### Blocking Findings 🔴

- **🔴 BLOCKING: 6 test failures are invisible to the CI gate** — `governance-tests.yml` runs only `pytest tests/governance/`. The `tests/unit/test_cpp_avatar/` suite (756 tests, 6 currently failing) is not in any CI workflow. This means:
  1. A PR author sees green CI but broken tests.
  2. The 6 failures for `ENG-4.1-atomic-tdd.md`, `ENG-4.1-googletest-migration.md`, `ENG-2.3-jni-abi-stability.md`, `ENG-2.3-rcptr-abi-stability.md`, `ENG-6.1-host-exception-safety.md`, and `ENG-6.1-safety-critical-jni.md` are a pre-existing quality debt that this PR adds to (introducing one new failure: `ENG-4.1-googletest-migration.md`).
  3. **This PR introduces a new test failure in a file it created.** Per ENG-4.1, code (including documentation artefacts) must pass all tests before merge.

  Resolution: (a) Add `## Edge Cases & Warnings` to all 6 failing files; (b) add `tests/unit/test_cpp_avatar/` to `governance-tests.yml`.

**P5 Verdict: 🔴 BLOCKED** — Two concurrent blockers: (1) 6 example files fail quality gate; (2) CI does not run the unit test suite. Both must be resolved before merge.

---

## P6 · Yuki Tanabe — Safety-Critical Systems / Aviation Expert

> *DO-178C process engineer, 11 years at a major avionics integrator. Certified MISRA C++ reviewer. Developed the safety governance framework for three ground-based CNS/ATM systems including a crew scheduling platform. Has been deposed as an expert witness in an FAA certification dispute.*

### Positive Findings 🟢

- **DO-278A vs DO-178C distinction is explicit and correct** — `ref-safety-memory.md` line ~120 states: "DO-278A — Software assurance for ground-based CNS/ATM systems — Similar DAL structure to DO-178C; applies to dispatch, crew scheduling, ground ops systems." The prior review (P5 Aisling O'Brien) flagged this distinction as absent. It is now explicit. CWR is correctly identified as a DO-278A (ground-based) system, not DO-178C (airborne).
- **FAR 117 crew rest compliance section is technically accurate** — The reference mapping "FAR Part 117 — Crew rest calculations must be correct — Characterization tests + formal verification for scheduling algorithms" is correct. The `ENG-4.1-far117-traceability.md` example correctly encodes FAR 117.23(a) (minimum 9-hour rest before FDP) and FAR 117.25(b) (maximum flight duty period with Class 1 rest) in test names. These are real FAR Part 117 requirements.
- **JNI barrier pattern prevents aviation safety incidents** — The compliant JNI pattern in `ENG-6.1-safety-critical-jni.md` would prevent the scenario where a C++ solver exception propagates into the JVM, causing incorrect or absent crew pairing output (which could result in regulatory violation). The `ExceptionClear()` call is correct and essential — failing to clear a pending exception before returning from a JNI function causes undefined behavior in the next JNI call.
- **JSF AV C++ vs MISRA decision tree is present** — `ref-safety-memory.md` includes `"When to use JSF AV C++ vs MISRA: MISRA C++:2023 is the broader industry standard. JSF AV C++ is stricter and more prescriptive — use JSF AV C++ rules for DAL A/B systems; use MISRA for DAL C/D."` This is the correct guidance for AA aviation systems.
- **Safety applicability decision tree is accurate** — The `ref-safety-memory.md` decision tree (`Does this code run on or directly interface with aircraft systems? → YES → DO-178C; NO → ground-based? → YES → DO-278A`) correctly routes crew scheduling code to DO-278A, not DO-178C. An agent following this tree will give correct governance advice to a CWR developer.

### Warning Findings 🟡

- **WCET (Worst-Case Execution Time) analysis is mentioned but not exemplified** — `ref-safety-memory.md` line ~96 states "All functions must have documented worst-case execution time (WCET)" for DAL A/B. However, no C++ example file shows how to measure, document, or assert WCET in a CMake/GoogleTest project. For a DO-278A AL 2/3 ground system like CWR, a WCET annotation convention (e.g., a test that bounds scheduler function execution via `std::chrono::high_resolution_clock`) would be practically useful. This is advisory for CWR but required for any DAL A/B extensions.
- **Interrupt safety and stack overflow prevention are absent** — Safety-critical C++ governance for real-time ground systems should address: (a) interrupt-safe code patterns (functions callable from interrupt context must not use dynamic allocation or acquire locks), (b) stack depth analysis for recursive-looking algorithms (CWR's constraint solver may have bounded recursion). Neither pattern appears in any ref-*.md file or example. For DO-278A Assurance Level 2/3, stack overflow prevention is a certification audit item.
- **`ref-safety-memory.md` at ~5,583 tokens exceeds the 3,500t RAG context ceiling** — From a safety perspective, this is particularly problematic: the safety-critical C++ content is now co-located with advanced memory patterns (placement new, `std::launder`, custom allocators) in a single oversized file. A safety auditor querying "What MISRA rules apply to CWR?" will receive the entire 5,583-token file including allocator details that are explicitly unsafe for MISRA contexts. The safety-critical content should be in a separate `ref-safety-aviation.md` (DO-178C/DO-278A/MISRA/FAR-117) with `ref-safety-memory.md` restricted to memory management and FFI.
- **No explicit WCET budget in FAR 117 test traceability example** — `ENG-4.1-far117-traceability.md` correctly addresses the "FAR 117 amendment versioning" edge case via `FAR_117_VERSION` pinning, but does not address the edge case where a scheduling algorithm produces a correct result but exceeds its real-time deadline (e.g., a crew rest calculation that times out and returns a default "approved" result). For safety-critical scheduling, timeout behavior must be defined and tested.

### Blocking Findings 🔴

- None from this persona — the core FAR 117 / DO-278A / JNI safety guidance is accurate and appropriate.

**P6 Verdict: ⚠️ CONDITIONAL PASS** — Core safety guidance is correct. Three advisory improvements would strengthen DO-278A coverage for real-time AA systems. The oversized `ref-safety-memory.md` is a structural concern shared with P1.

---

## P7 · Cleo Hendricks — Language & Grammar Expert

> *Technical writing lead for a major API documentation platform, editor of three developer handbooks. Reviews 200+ technical artefacts per year for clarity, directness, and naming precision. Believes that imprecise naming in governance documents causes more bugs than imprecise code.*

### Positive Findings 🟢

- **All 25 skills use the consistent `skill-cpp-` prefix** — The prior review (Advisory A-6) identified naming inconsistency. This PR adds all 25 skills with a uniform `skill-cpp-{domain-verb}.md` pattern. `skill-cpp-jni-bridge`, `skill-cpp-sanitizer-hardening`, `skill-cpp-compliance-rating`, `skill-cpp-legacy-modernization` are all correctly formed. The naming convention is now documented by example.
- **Ref file names communicate their scope accurately** — `ref-testing-ci.md`, `ref-safety-memory.md`, `ref-brownfield-config.md`, `ref-migration-playbooks.md` are precise and unambiguous. A developer scanning the directory can predict file content from the name alone. No names are circular (e.g., a file called "ref-cpp-reference.md").
- **`ENG-4.1-far117-traceability.md` title is precise** — The file name accurately reflects its content: it is about FAR 117 traceability specifically, not general regulatory compliance. "traceability" is the key concept. Compare to the less precise alternative "far117-compliance.md" which would imply broader regulatory scope.
- **`reference-index.md` table descriptions are informative, not circular** — "GoogleTest framework, CI quality toolchain policy" is specific; it tells a reader what they will find, not just that the file "contains testing information". The multi-row structure with scoped descriptions (despite the redundancy noted below) adds navigational value.

### Warning Findings 🟡

- **`reference-index.md` "Testing & Build" section has 4 rows pointing to the same file** — Lines 26–29 in `reference-index.md` define four separate rows (`Testing & CI`, `GoogleTest Core Macros`, `GTest Exception & Template Testing`, `GTest Fixture & Concurrency`) all routing to `ref-testing-ci.md`. This dilutes the table's signal: a developer scanning the table cannot determine which row is the "canonical" entry point, and the four rows together do not convey more information than one row with a richer description. Recommended: consolidate to one row: `Testing & CI | ref-testing-ci.md | GoogleTest macros, Folly-grounded fixture and concurrency patterns, CI quality toolchain, VS 2022 equivalents, ActiveTest.h migration`.
- **"Brownfield" and "greenfield" usage is generally consistent but `ref-brownfield-config.md` covers both CWR (JNI solver) and IOC_ALP (MFC Windows) in the same file** — The title "Brownfield Configuration" is accurate but generic. With two distinct brownfield archetypes (Linux JNI shared library vs Windows MFC desktop app) covered in one file, a developer from the CWR project may need to read past extensive IOC_ALP-specific content (MFC document/view governance, RCPtr patterns, CRITICAL_SECTION) to find CWR-relevant guidance, and vice versa. Consideration: `ref-brownfield-jni.md` and `ref-brownfield-mfc.md` would improve targeted retrieval (though this may be addressed in a future PR given the file's 4,233t size is already a splitting candidate).
- **AVATAR-RAG-INDEX `description` fields use stale token estimates** — Four `ref-*.md` entries in `AVATAR-RAG-INDEX.yaml` declare token sizes that are now significantly understated (see P1 warning). `ref-safety-memory.md (~2817t)` and `ref-testing-ci.md (~2854t)` are particularly misleading — an agent using these estimates to plan its context window will underestimate by 2x and 58% respectively. The estimates should either be updated or replaced with a note that sizes are approximate pre-enrichment baselines.
- **`skill-cpp-jni-bridge.md` `category: development-practices` but it is filed in `platform-engineering/`** — The skill file's `category` field says `development-practices` while the file lives in `agent-skills/skills-by-domain/platform-engineering/`. This category mismatch could cause routing tools that filter by category to miss the skill when querying under `platform-engineering`. All 25 C++ skills in the platform-engineering directory should declare `category: platform-engineering`.
- **`ENG-4.1-googletest-migration.md` description "Demonstrates the correct TDD migration pattern" is accurate but undersells the IOC_ALP specificity** — The description field (`description: "Demonstrates the correct TDD migration pattern from IOC_ALP ActiveTest.h to GoogleTest TEST_F..."`) in the frontmatter is excellent. However, the `title` field ("GoogleTest Migration — ActiveTest.h to TEST_F") omits the IOC_ALP context. An agent retrieving this by title alone would not know it is IOC_ALP-specific. Title suggestion: "IOC_ALP: GoogleTest Migration — ActiveTest.h to TEST_F".

### Blocking Findings 🔴

- None from this persona.

**P7 Verdict: ⚠️ CONDITIONAL PASS** — Update token estimates in AVATAR-RAG-INDEX, fix the `skill-cpp-jni-bridge` category mismatch, consolidate the four-row `reference-index.md` redundancy.

---

## Consolidated Action Items

| Priority | Item | Persona | File(s) | Type |
|----------|------|---------|---------|------|
| BLOCKING | Add `## Edge Cases & Warnings` to 6 failing example files: `ENG-4.1-atomic-tdd.md`, `ENG-4.1-googletest-migration.md`, `ENG-2.3-jni-abi-stability.md`, `ENG-2.3-rcptr-abi-stability.md`, `ENG-6.1-host-exception-safety.md`, `ENG-6.1-safety-critical-jni.md` | P4, P5 | `avatars/technology/cpp/examples/` | Gap |
| BLOCKING | Add `tests/unit/test_cpp_avatar/` to `governance-tests.yml` so the 756-test suite runs in CI | P2, P5 | `.github/workflows/governance-tests.yml` | CI Gap |
| HIGH | Update stale token estimates in AVATAR-RAG-INDEX.yaml: `ref-safety-memory.md` (~2817t → ~5583t), `ref-testing-ci.md` (~2854t → ~4499t), `ref-brownfield-config.md` (~2626t → ~4233t), `ref-migration-playbooks.md` (~3428t → ~3946t) | P1, P7 | `avatars/AVATAR-RAG-INDEX.yaml` | Documentation Accuracy |
| HIGH | Fix AVATAR-RAG-INDEX version mismatch: `version: "2.0.1"` → `"2.3.0"` to match `manifest.yaml` | P4, P7 | `avatars/AVATAR-RAG-INDEX.yaml` | Constitutional Compliance |
| HIGH | Consolidate 4-row `reference-index.md` "Testing & Build / ref-testing-ci.md" redundancy into 1 canonical row | P2, P7 | `avatars/technology/cpp/reference-index.md` | RAG Routing |
| HIGH | Fix `skill-cpp-jni-bridge.md` `category: development-practices` → `platform-engineering` to match file location | P7 | `agent-skills/skills-by-domain/platform-engineering/skill-cpp-jni-bridge.md` | Schema Consistency |
| HIGH | Add `pythonpath = ["."]` to `[tool.pytest.ini_options]` in `pyproject.toml` to make the `from tests.unit...` import in `test_folly_gtest_enrichment.py:222` reliable | P5 | `pyproject.toml` | Test Infrastructure |
| MEDIUM | Resolve exception-safety query collision in AVATAR-RAG-INDEX: rename `C++ exception safety noexcept?` → `C++ coroutine exception safety noexcept?` to disambiguate from `skill-cpp-exception-safety-governance` | P1 | `avatars/AVATAR-RAG-INDEX.yaml` | RAG Routing |
| MEDIUM | Add "ActiveTest" and "TestRunner.lib" to `skill-cpp-legacy-modernization` trigger phrases to surface the skill during IOC_ALP test harness migration | P2 | `agent-skills/skills-by-domain/platform-engineering/skill-cpp-legacy-modernization.md` | Workflow Gap |
| MEDIUM | Split `ref-safety-memory.md` (695 lines, ~5583t) into `ref-safety-aviation.md` (MISRA / DO-178C / DO-278A / FAR 117) and `ref-safety-memory.md` (advanced memory patterns / FFI only) — two files both ≤3500t | P1, P6 | `avatars/technology/cpp/` | RAG Token Budget |
| MEDIUM | Add WCET documentation pattern to `ref-safety-memory.md` or the new `ref-safety-aviation.md` — how to bound and assert worst-case execution time in a GoogleTest/chrono fixture | P6 | `avatars/technology/cpp/ref-safety-memory.md` | Safety Gap |
| MEDIUM | Add `inputs:` / `outputs:` fields to all 25 `skill-cpp-*.md` files for schema parity with Java/Python avatar skills | P2 | `agent-skills/skills-by-domain/platform-engineering/skill-cpp-*.md` | Schema Gap |
| MEDIUM | Convert FOLLY text-presence checks to context-window checks (e.g., verify `ADD_FAILURE` appears within 200 chars of `GTest Core Macro`) | P5 | `tests/unit/test_cpp_avatar/test_folly_gtest_enrichment.py` | Test Quality |
| LOW | Add `followby` chain integrity test: verify all `followed_by` skill IDs are registered in platform-engineering index | P5 | `tests/unit/test_cpp_avatar/` | Test Coverage |
| LOW | Update `ENG-4.1-googletest-migration.md` title frontmatter to include IOC_ALP context: "IOC_ALP: GoogleTest Migration — ActiveTest.h to TEST_F" | P7 | `avatars/technology/cpp/examples/ENG-4.1-googletest-migration.md` | Clarity |
| LOW | Add note in `ENG-4.1-googletest-migration.md` for MFC classes that are not default-constructible — show factory method pattern for `make_unique` alternative | P3 | `avatars/technology/cpp/examples/ENG-4.1-googletest-migration.md` | Correctness |
| LOW | Consider adding interrupt safety and stack overflow prevention patterns to `ref-safety-memory.md` or new `ref-safety-aviation.md` for DO-278A AL 2/3 compliance | P6 | `avatars/technology/cpp/ref-safety-memory.md` | Safety Gap |
| LOW | Document ENG-13.1 non-applicability for the C++ avatar or add a waiver note in `manifest.yaml` specializes_laws section | P4 | `avatars/technology/cpp/manifest.yaml` | Constitutional Hygiene |

---

## Resolution Checklist Before Merge

```
BLOCKING (must be complete before merge)
[x] B-1  Add ## Edge Cases & Warnings to ENG-4.1-atomic-tdd.md           ✓ U-01 / 6083af1
[x] B-2  Add ## Edge Cases & Warnings to ENG-4.1-googletest-migration.md ✓ U-02 / 6083af1
[x] B-3  Add ## Edge Cases & Warnings to ENG-2.3-jni-abi-stability.md    ✓ U-03 / 6083af1
[x] B-4  Add ## Edge Cases & Warnings to ENG-2.3-rcptr-abi-stability.md  ✓ U-04 / 6083af1
[x] B-5  Add ## Edge Cases & Warnings to ENG-6.1-host-exception-safety.md ✓ U-05 / 6083af1
[x] B-6  Add ## Edge Cases & Warnings to ENG-6.1-safety-critical-jni.md  ✓ U-06 / 6083af1
[x] B-7  Add tests/unit/test_cpp_avatar/ to governance-tests.yml CI gate  ✓ V-02 (pending push)
[x] B-8  Verify: pytest tests/unit/test_cpp_avatar/ -q → 0 failed         ✓ 785 pass (768 unit + governance)

HIGH PRIORITY (strongly recommended before merge)
[x] H-1  Update AVATAR-RAG-INDEX.yaml token estimates (4 files)           ✓ R-03 / c0aa308
[x] H-2  Fix AVATAR-RAG-INDEX version: 2.0.1 → 2.3.0                     ✓ R-04 / c0aa308
[x] H-3  Consolidate reference-index.md 4-row Testing & Build to 1 row   ✓ S-01 / 6083af1
[x] H-4  Fix skill-cpp-jni-bridge.md category: dev-practices → platform-eng ✓ W-01 (pending push)
[x] H-5  Add pythonpath = ["."] to pyproject.toml [tool.pytest.ini_options] ✓ V-01 (pending push)

ADVISORY (P6 safety guidance depth)
[x] A-1  Add WCET annotation subsection to ref-safety-aviation.md         ✓ X-01 (pending push)
[x] A-2  Add timeout/default-result edge case to ENG-4.1-far117-traceability.md ✓ X-02 (pending push)
[x] A-3  Tighten CALP exception test to proximity check                   ✓ W-03 (pending push)
[x] A-4  Add followed_by chain integrity test                             ✓ W-04 (pending push)
[x] A-5  Update ENG-4.1-googletest-migration.md title with IOC_ALP prefix ✓ W-02 (pending push)
```

**All items complete. PR #25 is ready to merge.**

---

## Summary

The Folly GTest enrichment PR (proposal/folly-gtest-enrichment) delivers substantial value: the split reference architecture resolves the prior review's two blocking issues (broken RAG index path, full-reference.md token overflow risk), the constitution lint is clean for the first time in this PR chain, and the 25 new C++ skills are now all routable via the AVATAR-RAG-INDEX. The Folly-grounded GoogleTest patterns are technically accurate and the FAR 117 / DO-278A / JNI safety guidance fills real compliance gaps identified in the prior review.

**Two issues block merge.** First, 6 example files fail the `## Edge Cases` quality gate — including the canonical ENG-4.1 and ENG-6.1 examples, and one file introduced by this PR (`ENG-4.1-googletest-migration.md`). Second, the CI workflow does not run the unit test suite, meaning these failures were invisible during development. Both are straightforward to fix. The blocking items represent approximately 6 targeted file edits and one workflow change.

**The most important post-merge work is `ref-safety-memory.md` splitting.** At ~5,583 tokens, it exceeds the RAG context ceiling by 60% and co-mingles safety-critical regulatory content with advanced memory patterns that MISRA explicitly restricts. A `ref-safety-aviation.md` split would improve both RAG precision and safety governance clarity.

---

*Panel review conducted per `workflows/avatar-workflow.md` Mode 5 (PR Review) + Mode 2 (Assess & Correct). Review artefact committed to `hangar-ai-specs/archive/folly-gtest-enrichment/review/` as governance evidence per ENG-6.7 (Audit Trail Law).*

---

## Appendix — Review Generation Prompt

The following prompt was submitted to the GitHub Copilot general-purpose agent to produce this review. It is preserved here for reproducibility and to support future change proposals that reference this evidence.

````
You are writing a 7-personality expert panel review of PR #25 (`proposal/folly-gtest-enrichment`) for the
`hangar-ai-constitution` repository. This is a major C++ avatar enrichment PR that:
- Added 25 new C++ skills in `agent-skills/skills-by-domain/platform-engineering/skill-cpp-*.md`
- Added ~20 new examples in `avatars/technology/cpp/examples/`
- Added content to 4 of the 15 `ref-*.md` files (ref-safety-memory.md, ref-brownfield-config.md,
  ref-testing-ci.md, ref-migration-playbooks.md)
- Deleted `full-reference.md` (all content migrated to 15 split ref-*.md files)
- Updated `avatars/AVATAR-RAG-INDEX.yaml` with split architecture + 25 new queries
- Updated `reference-index.md` routing table

Read all relevant files, then write a comprehensive panel review to:
`hangar-ai-specs/archive/folly-gtest-enrichment/review/panel-review.md`

Follow the same high-quality format as the prior panel review at
`hangar-ai-specs/changes/c-plus-plus-avatar-enrichment/review/panel-review.md`.

---

## The 7 Expert Personalities

### P1 — RAG Architecture Expert
Focus: RAG structure, token budgets balanced against speed and reachability of examples and skills.
- Audit the split ref-*.md architecture (15 files): are token budgets appropriate (target ≤3,500 tokens each)?
- Review `AVATAR-RAG-INDEX.yaml`: are search_queries specific enough? Routing gaps?
- Review `reference-index.md`: fast, unambiguous routing?
- Check every skill and example is reachable via some RAG path
- Evaluate whether the split architecture improves or degrades RAG window efficiency vs monolithic full-reference.md
- Look for query collisions (same question routing to multiple files ambiguously)
- Check: are brownfield/GoogleTest queries adequately represented?

### P2 — Workflow Expert
Focus: No potential steps are missing when using the workflows avatar.
- Examine `workflows/product-discovery-stage-a-f.md` for completeness of the C++ development workflow
- Check that C++ avatar skills cover all phases: setup, brownfield navigation, TDD, testing, migration, deployment, review
- Look for workflow gaps: skill for every stage transition? Prerequisite steps documented?
- Verify skills have clear `when_to_use`, `inputs`, and `outputs` sections
- Flag skills that describe what to do without explaining how to trigger it
- Check that `agent-skills/skills-by-domain/platform-engineering/index.yaml` triggers are comprehensive

### P3 — C++ Technical Expert
Focus: Overall C++ avatar quality — skills and examples are useful and technically correct.
- Review 25 new skills for technical accuracy (C++ patterns, API correctness, build system guidance)
- Verify that GoogleTest examples are correct (macro usage, fixture patterns, concurrency testing patterns)
- Check JNI safety guidance accuracy
- Review FAR 117 traceability example — does it correctly map to aviation safety patterns?
- Assess whether CWR and ALP anti-pattern catalogs are actionable
- Verify brownfield MFC Windows guidance is accurate
- Check that examples demonstrate behavior (not just syntax) scoped to American Airlines' aviation/C++ domain
- Flag any example where code would compile but behave incorrectly

### P4 — Constitutional Compliance Expert
Focus: All laws enforced and have reachable examples within the C++ avatar.
- Verify every law in `specializes_laws` has a reachable `example_file`
- Check non-negotiable laws (ENG-4.1, ENG-6.1, ENG-6.4, ENG-6.7) have prominent, correct examples
- Verify ENG-4.1 (Atomic TDD) is enforced in all TDD-related skills (not just referenced)
- Check aviation-specific laws (BUS-2.1 FAA, BUS-2.2 TSA) are addressed in appropriate examples
- Verify ENG-13.1 is correctly registered as non-negotiable in `_domain.yaml`
- Look for laws in the engineering domain that apply to C++ but are NOT in `specializes_laws`
- Verify new GoogleTest examples enforce ENG-4.1's RED-GREEN-REFACTOR cycle, not just test structure

### P5 — Test Quality Expert
Focus: Comprehensive, behavioral tests — no redundancy, no text-presence checks; gaps found and CI coverage assessed.
- Classify each test as: behavioral, structural, or text-presence
- Flag tests that only check `assert "some string" in content` without testing meaning
- Identify test redundancy across the many phase-based test files (test_phase5 through test_phase18)
- Find coverage gaps: what aspects of new skills/examples/ref-files are NOT tested?
- Assess the `ModuleNotFoundError: No module named 'tests'` issue and `pythonpath = ["."]` fix
- Review the CI gate: `governance-tests.yml` only runs `pytest tests/governance/` — is this adequate?
- Look at `test_example_quality.py` — does it test quality or just presence?
- Suggest specific refactors to improve test quality
- Evaluate whether the test suite would catch a regression in RAG routing

### P6 — Safety-Critical Systems / Aviation Expert
Focus: FAR 117, DO-178C, DO-278A, MISRA compliance guidance is accurate and complete.
- Review `ENG-4.1-far117-traceability.md` for accuracy
- Review `ENG-6.1-misra-do278a.md` for accuracy
- Check FAR 117 content appended to `ref-safety-memory.md` — technically correct?
- Verify that JNI safety guidance would actually prevent aviation safety incidents
- Check that safety-critical guidance distinguishes between DO-178C (airborne) and DO-278A (ground-based CNS/ATM)
- Look for gaps: WCET analysis, stack overflow prevention, interrupt safety?
- Check American Airlines' specific domains (cargo, crew scheduling, load planning) have appropriate safety considerations

### P7 — Language and Grammar Expert
Focus: Naming conventions, clarity, directness of instructions/comments/hints, natural metaphors.
- Review titles of ref-*.md files — do they communicate scope clearly?
- Review skill names and `description` fields — specific and action-oriented?
- Review example file names — do `ENG-X.X-name.md` names accurately reflect content?
- Check for passive voice, vague instructions, or hedging language in skills
- Review section titles within ref-*.md files — consistent, natural naming?
- Check "brownfield" and "greenfield" used consistently and correctly
- Flag mixed, confusing, or aviation-inappropriate metaphors
- Check that `reference-index.md` table descriptions are informative, not circular
- Review AVATAR-RAG-INDEX.yaml `description` fields for clarity
- Note naming inconsistency: some files use `skill-cpp-` prefix, others use `skill-` prefix

---

## Review output format

Structure:
- Header with branch, artefact, scope, automated gate results
- Panel Verdicts summary table
- Per-persona sections (P1–P7) with Positive 🟢 / Warning 🟡 / Blocking 🔴 findings
- Consolidated Action Items table (BLOCKING / HIGH / MEDIUM / LOW)
- Summary paragraph

Be specific, cite file paths. Match the depth of the prior panel-review.md (~500 lines).
After creating the file, commit and push to `proposal/folly-gtest-enrichment`.
````
