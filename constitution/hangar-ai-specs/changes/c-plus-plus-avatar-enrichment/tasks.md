# Tasks: c-plus-plus-avatar-enrichment

**Laws governing this work:** `ENG-11.1`, `ENG-11.2`, `ENG-4.1`, `ENG-4.2`, `ENG-6.1`, `BUS-7.1`

## Progress Summary

- Completed: 285 / 323
- In Progress: 0
- Blocked: 0 (1 task pending human sign-off: 0.4)

---

## Phase 0: Hangar SDD Execution Artifacts

> **Goal:** Establish governed execution tracking for the C++ avatar enrichment change.

- [x] 0.1 Create `PROPOSAL.md`
- [x] 0.2 Create `tasks.md`
- [x] 0.3 Create `PROGRESS.md`
- [x] 0.4 Record governance approvals and sign-off evidence in `PROGRESS.md`
- [x] 0.5 Add formal Laws Cited section with hyperlink citations (ENG-11.2 compliance)
- [x] 0.6 Document explicit 5 taxonomy gate pass/fail results (skill-30 required method)
- [x] 0.7 Add anti-pattern alias canonical mapping table (skill-30 required output #2)
- [x] 0.8 Add cross-reference to mutation-testing-governance proposal and ENG-4.11 coordination note
- [x] 0.9 Add evidence source taxonomy tags to key claims (enrichment template convention)
- [x] 0.10 Add risk register with mitigations for execution risks
- [x] 0.11 Add draft YAML for `avatars/index.yaml` and `AVATAR-RAG-INDEX.yaml` entries
- [x] 0.12 Add token impact assessment for 29+ new files
- [x] 0.13 Add enrichment intake details (target repos/services, brownfield constraints — workflow Step 1)
- [x] 0.14 Add archival instructions (SDD lifecycle ENG-11.1)
- [x] 0.15 Add rollback/deprecation plan
- [x] 0.16 Note optional `design.md` / `SPEC.md` artifacts (spec-governance.md)

## Phase 1: Avatar Foundation

> **Goal:** Create the core C++ technology avatar structure with parity-complete manifest and guidance artifacts.

- [x] 1.1 Create `avatars/technology/cpp/manifest.yaml`
- [x] 1.2 Create `avatars/technology/cpp/guidance.md`
- [x] 1.3 Document stack metadata, compiler/build options, and toolchain matrix in `manifest.yaml`
- [x] 1.4 Add test/build/lint/format/sanitizer command matrix to `manifest.yaml`
- [x] 1.5 Add conventions section to `manifest.yaml` (naming, structure, testing layout)
- [x] 1.6 Add project structure template to `manifest.yaml`
- [x] 1.7 Add anti-patterns and retrieval triggers to `manifest.yaml`
- [x] 1.8 Add baseline skill activation parity to `manifest.yaml`

## Phase 2: Rust-Inspired Safety and Toolchain Policies

> **Goal:** Encode approved C++ governance decisions in guidance and implementation artifacts.

- [x] 2.1 Document ownership-first API design guidance
- [x] 2.2 Document lifetime and bounds safety defaults (`span`, `not_null`, RAII)
- [x] 2.3 Document unsafe-boundary governance with repository-configurable modes
- [x] 2.4 Document concurrency-by-design guidance
- [x] 2.5 Document C++ version policy (greenfield and brownfield)
- [x] 2.6 Document CI quality toolchain policy
- [x] 2.7a Create `tests/unit/test_cpp_avatar/avatar_test_helpers.py` with reusable governance validators (Amendment A.1)
- [x] 2.7 Document Mull mutation testing policy, including LLVM/Clang prerequisite and phased brownfield exception handling
- [x] 2.8 Document GoogleTest + GoogleMock testing framework policy
- [x] 2.9 Document package manager guidance for `vcpkg` and `Conan` with selection criteria
- [x] 2.10 Document brownfield non-rewrite safeguards and modernization path
- [x] 2.11 Document default SAST recommendation for C++ (with brownfield exception path)
- [x] 2.12 Document default dependency/vulnerability scanning recommendation for C++ (with brownfield exception path)
- [x] 2.13 Document default DAST recommendation for C++ services (with brownfield exception path)
- [x] 2.14 Document default secrets-management platform recommendation (with brownfield exception path)
- [x] 2.15 Document default IaC tooling recommendation (with brownfield exception path)
- [x] 2.16 Document default coverage tooling recommendation for C++ CI reporting (with brownfield exception path)
- [x] 2.17 Document default observability stack recommendation (with brownfield exception path)
- [x] 2.18 Add Cross-Language Alignment Defaults matrix content to C++ guidance/manifest implementation
- [x] 2.19 Document tool-selection rationale snippets in C++ guidance, relevant skill modules, and AGENTS routing notes

## Phase 3: Non-Negotiable Law Coverage Examples

> **Goal:** Provide 18/18 non-negotiable law examples for C++.

- [x] 3.1 Create `examples/ENG-4.1-atomic-tdd.md`
- [x] 3.2 Create `examples/ENG-6.1-security-by-design.md`
- [x] 3.3 Create `examples/ENG-6.4-data-protection.md`
- [x] 3.4 Create `examples/ENG-6.7-audit-trail.md`
- [x] 3.5 Create `examples/PRD-1.2-problem-first.md`
- [x] 3.6 Create `examples/PRD-1.5-evidence-based-decision.md`
- [x] 3.7 Create `examples/PRD-2.5-stage-gate.md`
- [x] 3.8 Create `examples/PRD-5.1-mvp.md`
- [x] 3.9 Create `examples/PRD-6.2-retention-over-acquisition.md`
- [x] 3.10 Create `examples/BUS-1.1-priority-hierarchy.md`
- [x] 3.11 Create `examples/BUS-4.3-data-subject-rights.md`
- [x] 3.12 Create `examples/BUS-7.1-audit-trail.md`
- [x] 3.13 Create `examples/BUS-9.3-breach-notification.md`
- [x] 3.14 Create `examples/BUS-2.1-faa-compliance.md`
- [x] 3.15 Create `examples/BUS-2.2-tsa-security.md`
- [x] 3.16 Create `examples/BUS-2.3-dot-consumer-protection.md`
- [x] 3.17 Create `examples/BUS-3.1-pnr-retention.md`
- [x] 3.18 Create `examples/BUS-6.1-dangerous-goods.md`

## Phase 3a: Supplemental Engineering-Law Example Parity

> **Goal:** Add the supplemental engineering-law examples required for C++ parity with mature technology avatars.

- [x] 3a.1 Create `examples/ENG-2.1-aggregates.md`
- [x] 3a.2 Create `examples/ENG-2.2-layers.md`
- [x] 3a.3 Create `examples/ENG-3.1-complexity.md`
- [x] 3a.4 Create `examples/ENG-3.2-immutability.md`
- [x] 3a.5 Create `examples/ENG-3.3-demeter.md`
- [x] 3a.6 Create `examples/ENG-3.5-naming.md`
- [x] 3a.7 Create `examples/ENG-4.2-test-pyramid.md`
- [x] 3a.8 Create `examples/ENG-4.4-test-structure.md`
- [x] 3a.9 Create `examples/ENG-6.5-input-validation.md`

## Phase 4: Registry, RAG, and Governance Wiring

> **Goal:** Ensure the C++ avatar is retrievable, indexed, and governance-complete.

- [x] 4.1 Update `avatars/index.yaml`
- [x] 4.2 Update `avatars/AVATAR-RAG-INDEX.yaml`
- [x] 4.3 Create or update platform-engineering C++ skill modules
- [x] 4.4 Update `agent-skills/skills-by-domain/platform-engineering/index.yaml`
- [x] 4.5 Update `AGENTS.md` if retrieval/activation guidance changes
- [x] 4.6 Apply law citation format checks to guidance and example files
- [x] 4.7 Record minimum governance sign-offs in `PROGRESS.md`

## Phase 5: Validation and Review

> **Goal:** Verify proposal acceptance criteria are met and implementation artifacts are governance-ready.

- [x] 5.1 Validate manifest parity sections are present
- [x] 5.2 Validate guidance parity sections are present
- [x] 5.3 Validate 18/18 non-negotiable examples are present
- [x] 5.4 Validate 9 supplemental engineering-law examples are present
- [x] 5.5 Validate RAG/index updates are complete
- [x] 5.6 Validate brownfield safeguards and test equivalence guidance are documented
- [x] 5.6a Build `tests/unit/test_cpp_avatar/test_constitution_compliance.py` governance validation suite (Amendment A.3)
- [x] 5.7 Validate constitution law/rule references are Markdown hyperlinks to canonical sources
- [x] 5.8 Validate evidence source taxonomy tags are present on key claims
- [x] 5.9 Validate risk register mitigations are current
- [x] 5.10 Validate draft registry YAML matches actual implementation
- [x] 5.11 Validate token budget per example file (<600 tokens)
- [x] 5.12 Final governance review against proposal success criteria

## Phase 6: Advanced C++20+ Governance (Amendment B)

> **Goal:** Close critical governance gaps for exception safety, coroutines, logging, modules, and allocators.

### Guidance Sections
- [x] 6.1 Add exception safety & error handling governance section to `guidance.md`
- [x] 6.2 Add coroutines governance section to `guidance.md`
- [x] 6.3 Add structured logging & diagnostics governance section to `guidance.md`
- [x] 6.4 Add C++20 modules governance section to `guidance.md`
- [x] 6.5 Add allocator governance section to `guidance.md`

### Skill Modules
- [x] 6.6 Create `skill-cpp-exception-safety-governance.md`
- [x] 6.7 Create `skill-cpp-coroutines-governance.md`
- [x] 6.8 Create `skill-cpp-logging-diagnostics-standards.md`

### Registry Updates
- [x] 6.9 Update `manifest.yaml` — new retrieval triggers and anti-patterns
- [x] 6.10 Update `AVATAR-RAG-INDEX.yaml` — new search queries
- [x] 6.11 Update `platform-engineering/index.yaml` — register 3 new skills (count 15→18)

### Tests
- [x] 6.12 Test exception safety guidance section
- [x] 6.13 Test coroutines guidance section
- [x] 6.14 Test logging & diagnostics guidance section
- [x] 6.15 Test modules guidance section
- [x] 6.16 Test allocator governance guidance section
- [x] 6.17 Test 3 new skill modules exist with valid frontmatter
- [x] 6.18 Full suite verification — all tests pass, lint clean

---

## Phase 7: Critical Fixes (Amendment C)

> **Goal:** Fix 4 swapped law IDs and add missing compiler warning policy.

### Bug Fixes
- [x] 7.1 Fix swapped law IDs in `guidance.md` — ENG-5.1↔5.2 and ENG-5.5↔5.6 (7 locations)
- [x] 7.2 Fix swapped law IDs in `PROPOSAL.md` law citation table (4 entries)

### Compiler Warning Policy
- [x] 7.3 Add compiler warning flags subsection to `guidance.md` CI Quality Toolchain Policy
- [x] 7.4 Add `-Wall -Wextra -Wpedantic -Werror` to `manifest.yaml` mandatory CI toolchain

### Tests
- [x] 7.5 RED test — verify law IDs match actual titles in `guidance.md`
- [x] 7.6 RED test — verify compiler warning policy section exists in `guidance.md`
- [x] 7.7 Full suite verification — all tests pass, commit

---

## Phase 8: P0 Governance Gaps (Amendment D)

> **Goal:** Close high-risk governance gaps — 3 unaddressed lifecycle phases, missing concurrency/resiliency skills, ABI stability, templates, anti-patterns.

### New Guidance Sections
- [x] 8.1 Add ABI Stability & Binary Compatibility section to `guidance.md`
- [x] 8.2 Add Template & Metaprogramming Governance section to `guidance.md`
- [x] 8.3 Add Panic/Abort vs Recovery Policy section to `guidance.md`
- [x] 8.4 Add C/C++ FFI Error Propagation section to `guidance.md`
- [x] 8.5 Add Reproducible Builds section to `guidance.md`
- [x] 8.6 Add License Compliance & Dependency Governance section to `guidance.md`

### New Skills
- [x] 8.7 Create `skill-cpp-concurrency-thread-safety-governance.md`
- [x] 8.8 Create `skill-cpp-resiliency-failure-modes.md`
- [x] 8.9 Create `skill-cpp-deployment-hardening.md`
- [x] 8.10 Create `skill-cpp-debugging-diagnostics-playbook.md`
- [x] 8.11 Create `skill-cpp-dependency-governance.md`

### Registry Updates
- [x] 8.12 Bump compiler versions in `manifest.yaml` — GCC 13+, Clang 16+, MSVC 19.38+, CMake 3.25+
- [x] 8.13 Add 10 missing anti-patterns to `manifest.yaml`
- [x] 8.14 Expand `specializes_laws`, retrieval triggers, bump version 2.0.0, add workflow
- [x] 8.15 Update `AVATAR-RAG-INDEX.yaml` — new search queries for all new topics
- [x] 8.16 Update `platform-engineering/index.yaml` — register 5 new skills (count 18→23)

### Tests
- [x] 8.17 Tests for ABI stability guidance section
- [x] 8.18 Tests for template/metaprogramming guidance section
- [x] 8.19 Tests for panic/abort policy section
- [x] 8.20 Tests for FFI error propagation section
- [x] 8.21 Tests for reproducible builds section
- [x] 8.22 Tests for license compliance section
- [x] 8.23 Tests for 5 new skill modules
- [x] 8.24 Tests for updated manifest (compiler versions, anti-patterns, triggers)
- [x] 8.25 Tests for updated RAG index
- [x] 8.26 Tests for cross-avatar parity (version 2.0.0, workflow, specializes_laws count)
- [x] 8.27 Full suite verification — all tests pass, commit

---

## Phase 9: C++20+ Examples & Legacy Code Guidance (Amendment E)

> **Goal:** Add 10 modern C++20+ example files and a comprehensive legacy code navigation section for novice engineers.

### C++20+ Examples
- [x] 9.1 Create `ENG-6.1-smart-pointers.md` — unique_ptr/shared_ptr/weak_ptr patterns
- [x] 9.2 Create `ENG-6.1-move-semantics.md` — noexcept move with swap idiom
- [x] 9.3 Create `ENG-6.1-thread-safety.md` — scoped_lock + atomic counter patterns
- [x] 9.4 Create `ENG-6.1-raii-resources.md` — RAII with custom deleters for C interop
- [x] 9.5 Create `ENG-3.1-concepts.md` — C++20 concept-constrained templates
- [x] 9.6 Create `ENG-6.1-expected-errors.md` — std::expected monadic chaining
- [x] 9.7 Create `ENG-3.1-coroutines.md` — coroutine with stop_token cancellation
- [x] 9.8 Create `ENG-6.7-structured-logging.md` — spdlog JSON with PII redaction
- [x] 9.9 Create `ENG-5.2-cmake-governance.md` — well-structured CMakeLists.txt
- [x] 9.10 Create `ENG-3.1-pmr-allocators.md` — PMR in hot-path fare calculation

### Legacy Code Guidance
- [x] 9.11 Add "Legacy Code Navigation for New Engineers" section to `guidance.md`
- [x] 9.12 Create `skill-cpp-legacy-code-navigation.md`

### Tests
- [x] 9.13 Tests for 10 new C++20+ example files (parameterized)
- [x] 9.14 Tests for legacy code navigation guidance section
- [x] 9.15 Full suite verification — all tests pass, commit

---

## Phase 10: Standard-Tier Governance Foundation (Amendment F)

> **Goal:** Add structured standard-tier definitions to manifest.yaml and per-tier governance policies to guidance.md, enabling AI agents to provide correct, tier-specific guidance for C++98/03, C++11, C++14/17, and C++20/23 codebases.

### Manifest Standard Tiers
- [x] 10.1 Add `standard_tiers` block to `manifest.yaml` — 5 tiers with per-tier compiler minimums, status, policy, features
- [x] 10.2 Replace single `compilers:` list with tiered compiler structure in `manifest.yaml`
- [x] 10.3 Add `anti_patterns_by_tier` block to `manifest.yaml` — tier-scoped anti-patterns for C++98/03, C++11, C++14/17
- [x] 10.4 Parameterize lint command in `manifest.yaml` — per-tier `-std=` examples

### Guidance Per-Tier Governance
- [x] 10.5 Add per-tier clang-tidy configuration profiles to `guidance.md`
- [x] 10.6 Add per-tier testing framework matrix to `guidance.md`
- [x] 10.7 Add per-tier code review criteria to `guidance.md`
- [x] 10.8 Add cross-standard ABI boundary guidance to `guidance.md`
- [x] 10.9 Add feature-detection macro governance to `guidance.md`
- [x] 10.10 Add compiler flag progression guide to `guidance.md`
- [x] 10.11 Add sanitizer availability matrix to `guidance.md`

### Tests & Verification
- [x] 10.12 Tests for manifest standard_tiers and tiered compilers
- [x] 10.13 Tests for all new guidance sections (per-tier clang-tidy, testing, review, ABI, feature detection, flags, sanitizers)
- [x] 10.14 Update Phase 5 validation test counts
- [x] 10.15 Full suite verification — all tests pass, commit

---

## Phase 11: Migration Playbooks & Examples (Amendment G)

> **Goal:** Provide concrete, ordered migration guidance for each C++ standard upgrade path and example files demonstrating legacy migration patterns.

### Migration Playbooks
- [x] 11.1 Add C++98/03 → C++11 migration playbook to `guidance.md`
- [x] 11.2 Add C++11 → C++14 migration playbook to `guidance.md`
- [x] 11.3 Add C++14 → C++17 migration playbook to `guidance.md`
- [x] 11.4 Add C++17 → C++20 migration playbook to `guidance.md`
- [x] 11.5 Add dual-toolchain governance section to `guidance.md`
- [x] 11.6 Add dependency standard mismatch guidance to `guidance.md`
- [x] 11.7 Add "Writing New Code for Legacy Standards" section to `guidance.md`

### Example Files
- [x] 11.8 Create `ENG-5.2-cmake-mixed-standard.md` example
- [x] 11.9 Create `ENG-6.1-auto-ptr-migration.md` example
- [x] 11.10 Create `ENG-6.1-smart-pointer-migration.md` example
- [x] 11.11 Create `ENG-6.1-raii-c-api-wrapper.md` example
- [x] 11.12 Create `ENG-6.1-thread-migration.md` example
- [x] 11.13 Create `ENG-3.1-feature-detection.md` example
- [x] 11.14 Create `ENG-6.1-legacy-modernization-before-after.md` example

### Tests & Verification
- [x] 11.15 Tests for migration playbook sections in guidance
- [x] 11.16 Tests for 7 new example files (parameterized)
- [x] 11.17 Update Phase 5 validation test counts (examples 37→44)
- [x] 11.18 Update PROGRESS.md
- [x] 11.19 Full suite verification — all tests pass, commit

---

## Phase 12: Legacy Anti-Patterns, Skills & RAG (Amendment H)

> **Goal:** Add 13 legacy-specific anti-patterns, create 4 new skills for standard migration/modernization, add legacy mode sections to 4 existing skills, and close RAG retrieval blind spots.

### Legacy Anti-Patterns
- [x] 12.1 Add 13 legacy anti-patterns to `manifest.yaml` anti_patterns[]

### New Skills
- [x] 12.2 Create `skill-cpp-standard-migration.md`
- [x] 12.3 Create `skill-cpp-legacy-modernization.md`
- [x] 12.4 Create `skill-cpp-compatibility-headers.md`
- [x] 12.5 Create `skill-cpp-feature-detection.md`

### Existing Skill Updates
- [x] 12.6 Add legacy mode section to `skill-cpp-portable-build-governance.md`
- [x] 12.7 Add legacy mode section to `skill-cpp-concurrency-thread-safety-governance.md`
- [x] 12.8 Add legacy mode section to `skill-cpp-template-complexity-management.md`
- [x] 12.9 Add legacy mode section to `skill-cpp-exception-safety-governance.md`

### RAG & Registry
- [x] 12.10 Add 12 legacy retrieval triggers to `manifest.yaml`
- [x] 12.11 Add 10 legacy search queries to `AVATAR-RAG-INDEX.yaml`
- [x] 12.12 Add 5 legacy anti-patterns to `AVATAR-RAG-INDEX.yaml`
- [x] 12.13 Update `platform-engineering/index.yaml` skill count (24→28)

### Tests & Verification
- [x] 12.14 Tests for 13 new anti-patterns in manifest
- [x] 12.15 Tests for 4 new skills (frontmatter, law citations, content)
- [x] 12.16 Tests for 4 updated skills (legacy mode sections)
- [x] 12.17 Tests for RAG index and registry updates
- [x] 12.18 Update Phase 5 validation test counts (skills 17→21)
- [x] 12.19 Update PROGRESS.md and tasks.md summary counts
- [x] 12.20 Full suite verification — all tests pass, commit

---

## Phase 13: Novice C++ Developer Guidance (Amendment I)

> **Goal:** Add comprehensive guidance for experienced programmers novice to C++ who are taking over poorly-maintained legacy codebases. Covers mental model transitions, code smell recognition, triage methodology, survival patterns, and object design rehabilitation.

### Guidance Sections
- [x] 13.1 Add "Mental Model Transitions" section to guidance.md (8 gaps: value semantics, RAII, compilation model, UB, pointers, preprocessor, linking, const)
- [x] 13.2 Add "Legacy Code Smell Catalog" section to guidance.md (14 smells with recognition, severity, remediation)
- [x] 13.3 Add "Legacy Codebase Triage Playbook" section to guidance.md (week-1 daily priorities, month-1 plan, DO NOT TOUCH list, characterization tests, seams)
- [x] 13.4 Expand "Skill Development Path" into full "Survival Patterns" section (week-1 reading → month-6 leadership)
- [x] 13.5 Add "Object Design Rehabilitation" section to guidance.md (6 design debt vectors)

### Skills
- [x] 13.6 Expand `skill-cpp-legacy-code-navigation.md` with triage timeline + seam guide
- [x] 13.7 Create `skill-cpp-legacy-survival-patterns.md`

### Manifest & RAG
- [x] 13.8 Add 14 code smell entries to `manifest.yaml` anti_patterns
- [x] 13.9 Add 8 retrieval triggers for novice content to `manifest.yaml`
- [x] 13.10 Add novice guidance RAG entries to `AVATAR-RAG-INDEX.yaml`

### Examples
- [x] 13.11 Create `ENG-3.1-code-smell-raii-conversion.md` example
- [x] 13.12 Create `ENG-4.1-characterization-test-pattern.md` example

### Tests & Verification
- [x] 13.13 Tests for 5 new guidance sections
- [x] 13.14 Tests for expanded and new skills
- [x] 13.15 Tests for 2 new examples (parameterized)
- [x] 13.16 Tests for manifest and RAG updates
- [x] 13.17 Update Phase 5 validation test counts (examples 44→46, skills 21→22)
- [x] 13.18 Update PROGRESS.md
- [x] 13.19 Full suite verification — all tests pass, commit

---

## Phase 14: Constitution Compliance Rating System (Amendment J)

> **Goal:** Add a quantitative, reproducible 0–10 compliance rating system for C++ codebases. Enables deployment gating, remediation tracking, and cross-tier normalization with 10 weighted dimensions mapped to constitutional laws.

### Guidance Sections
- [x] 14.1 Add "Constitution Compliance Rating" overview to guidance.md (10 dimensions, scoring formula, grade boundaries)
- [x] 14.2 Add detailed rubric (0-10 criteria per dimension) to guidance.md
- [x] 14.3 Add 3 example scorecards + tier adjustments to guidance.md

### Skills & Registry
- [x] 14.4 Create `skill-cpp-compliance-rating.md`
- [x] 14.5 Add compliance rating retrieval triggers to `manifest.yaml`
- [x] 14.6 Add compliance rating RAG entries to `AVATAR-RAG-INDEX.yaml`

### Tests & Verification
- [x] 14.7 Tests for rating sections in guidance (10 dimensions, rubric, scorecards)
- [x] 14.8 Tests for rating skill (frontmatter, law citations, content)
- [x] 14.9 Tests for manifest and RAG updates
- [x] 14.10 Update Phase 5 validation test counts (skills 22→23)
- [x] 14.11 Clean up compliance-rating-system.md reference doc
- [x] 14.12 Update PROGRESS.md and tasks.md summary counts
- [x] 14.13 Full suite verification — all tests pass, commit

---

## Phase 15: High-Value Additions (Amendment K)

> **Goal:** Add three high-value sections to the C++ guidance: a quick-start cheat sheet for onboarding, MISRA/DO-178C safety-critical mapping, and a periodic compliance re-rating schedule.

### Quick-Start Cheat Sheet
- [x] 15.1 Add "Quick-Start Cheat Sheet" section to guidance.md (greenfield, brownfield, novice paths)
- [x] 15.2 Tests for cheat sheet section presence and content (6 tests)

### MISRA/DO-178C Safety-Critical Section
- [x] 15.3 Add "MISRA C++ / DO-178C Compliance Mapping" section to guidance.md
- [x] 15.4 Tests for MISRA rules, DO-178C levels, FAA references (9 tests)

### Periodic Re-Rating Schedule
- [x] 15.5 Add re-rating cadence section to guidance.md
- [x] 15.6 Tests for re-rating schedule content (5 tests)

### Verification
- [x] 15.7 Full suite verification — all tests pass, commit

---

## Phase 16: Constitutional Compliance Corrections (Amendment O)

> **Goal:** Correct all 8 constitutional violations identified in governance panel review (PR #14, review #4086806910, 2026-04-10). Each step is one atomic TDD cycle per ENG-4.1: write RED test → implement correction → confirm GREEN → commit.

### Step 16.1 — Delete BUS-*/PRD-* Examples; Add Domain Boundary Contract Test (V1, V2)
- [x] 16.1a Write RED test in `test_phase16_compliance_corrections.py`: `test_technology_avatar_examples_only_contain_eng_laws()` — asserts every file in `examples/` starts with `ENG-` (one contract test that permanently enforces Safeguard 2; replaces any need for specific file-absence tests)
- [x] 16.1b Update `test_examples_non_negotiable.py`: remove the 14 BUS-*/PRD-* entries from `NON_NEGOTIABLE_EXAMPLES` (lines 22–35) — **do not replace with file-absence tests**; the domain boundary contract test above covers this permanently
- [x] 16.1c Update `test_phase5_validation.py`: remove lines 82–84 (BUS-*/PRD-* expected file list); update line 250 assertion from `count == 58` to `count == 44`
- [x] 16.1d Delete 9 BUS-* files: `BUS-1.1-priority-hierarchy.md`, `BUS-2.1-faa-compliance.md`, `BUS-2.2-tsa-security.md`, `BUS-2.3-dot-consumer-protection.md`, `BUS-3.1-pnr-retention.md`, `BUS-4.3-data-subject-rights.md`, `BUS-6.1-dangerous-goods.md`, `BUS-7.1-audit-trail.md`, `BUS-9.3-breach-notification.md`
- [x] 16.1e Delete 5 PRD-* files: `PRD-1.2-problem-first.md`, `PRD-1.5-evidence-based-decision.md`, `PRD-2.5-stage-gate.md`, `PRD-5.1-mvp.md`, `PRD-6.2-retention-over-acquisition.md`
- [x] 16.1f Confirm GREEN — commit
- **Design note:** Specific file-absence tests (e.g., "assert BUS-7.1-audit-trail.md does not exist") are one-shot guards — they become permanently valueless once the deletion is stable. The domain boundary contract test tests the *rule* (tech avatars → ENG-* only), not the *past incident*, and stays useful indefinitely.

### Step 16.2 — Remove `governance_overrides` Block (V3)
- [x] 16.2a Write RED test: assert `governance_overrides` key absent from `manifest.yaml`
- [x] 16.2b Remove `governance_overrides` block from `manifest.yaml`
- [x] 16.2c Confirm GREEN — commit

### Step 16.3 — Remove `anti_patterns`, `anti_patterns_by_tier`, `retrieval_triggers`; Add `authorities:` (V4 + Parity)
- [x] 16.3a Write RED test: assert three blocks absent from `manifest.yaml`
- [x] 16.3b Write RED test: assert `authorities:` block present in `manifest.yaml` (parity with `android-kotlin` schema — newest avatar as of 2026-04-08)
- [x] 16.3c Remove `anti_patterns`, `anti_patterns_by_tier`, `retrieval_triggers` blocks from `manifest.yaml`
- [x] 16.3d Add `authorities:` block to `manifest.yaml` citing: Herb Sutter (gotw.ca), Bjarne Stroustrup (stroustrup.com/C++), C++ Core Guidelines (isocpp.github.io/CppCoreGuidelines), ISO C++ Standard Committee (isocpp.org)
- [x] 16.3e Update any manifest content tests that assert the removed blocks exist
- [x] 16.3f Confirm GREEN — commit
- **Note:** `brownfield_adoption:`, `skill_parity:`, and `project_archetypes:` blocks inside `activates:` are **not removed** — `android-kotlin` establishes precedent for custom manifest blocks (`fastlane_lanes:`, `test_idioms:`); these are constitutionally acceptable.

### Step 16.4 — Fix Skill Law References (V5)
- [x] 16.4a Write RED test: assert `skill-cpp-compliance-rating.md` contains no `BUS-` law references (contract: platform-engineering skills reference only ENG-* laws — permanently useful rule)
- [x] 16.4b Replace `BUS-7.1` → `ENG-6.7` and `BUS-1.1` → `ENG-4.1` in `skill-cpp-compliance-rating.md`
- [x] 16.4c Confirm GREEN — commit

### Step 16.5 — Remove `compliance-rating-system.md` (V6)
- [x] 16.5a Write RED test: assert no `*rating-system.md` or `*compliance-rating*.md` exists in `avatars/technology/cpp/` (contract: avatar directories may not contain shadow governance documents — tests the rule, not the specific filename)
- [x] 16.5b Delete `avatars/technology/cpp/compliance-rating-system.md`
- [x] 16.5c Update any test that asserts the file exists
- [x] 16.5d Confirm GREEN — commit

### Step 16.6 — Rebuild `guidance.md` to ≤450 Tokens (V7)
- [x] 16.6a Write RED test: assert `guidance.md` token estimate ≤450 (word_count × 1.3)
- [x] 16.6b Update `test_law_reference_coverage.py`: remove BUS-7.1 assertions in guidance section checks (`Reproducible Builds`, `Constitution Compliance Rating`, `Safety-Critical C++`)
- [x] 16.6c Update all guidance section-presence tests that assert sections now moved to `docs/guides/avatars/cpp/`
- [x] 16.6d Rebuild `guidance.md`: purpose statement (2 sentences), non-negotiable laws section (law ID + 1 sentence + example file pointer each), pointer to `docs/guides/avatars/cpp/`
- [x] 16.6e Confirm GREEN — commit

### Step 16.7 — Full Suite Verification + Evidence File + Companion Proposals (V8)
- [x] 16.7a Run full test suite — all tests pass (≥683)
- [x] 16.7b Create `hangar-ai-specs/evidence/avatar-scan-cpp.md` — Avatar Workflow Phase 2 gap report (required for Phase 6 Commit gate): lists 8 violations found, Amendment O correction for each, post-O status per safeguard
- [x] 16.7c Create `hangar-ai-specs/changes/cpp-extended-reference-docs/` with `PROPOSAL.md` + `tasks.md`
- [x] 16.7d Create `hangar-ai-specs/changes/cpp-tier-compliance-rating/` with `PROPOSAL.md` + `tasks.md` (combined tier system + evaluation formula — architecturally inseparable; tier is pre-condition for scoring, Dimension 9 IS the tier evaluation, tier_multiplier adjusts composite score)
- [x] 16.7e Create `hangar-ai-specs/changes/product-avatar-bus-enrichment/` with `PROPOSAL.md` + `tasks.md`
- [x] 16.7f Post PR comment noting `mobile-react-native/examples/PRD-3.4-accessibility.md` — same domain boundary type as CPP violations, already on main; request governance panel ruling on whether accessibility crosses tech/product boundary
- [x] 16.7g Update `PROGRESS.md` with Amendment O completion
- [x] 16.7h Commit

---

## Phase 17: File Relocation — Amendment P

> **Goal:** Move `full-reference.md` from `docs/guides/avatars/cpp/` to `avatars/technology/cpp/`,
> correct all references, and verify the linter passes without the `f2e1552` weakening patch.
> **Prerequisite:** Merge `main` into the PR #14 branch before starting this phase.

### Step 17.0 — Prerequisite: Merge Main
- [x] 17.0 ✓ c4ab135 Merge `origin/main` into `feature/c-plus-plus-avatar-enrichment-proposal`
      (surfaces any conflicts before the file move; `f2e1552` will be present from main and
       must be accounted for — see 17.6)

### Step 17.1 — Move the File
- [x] 17.1 ✓ c4ab135 `git mv docs/guides/avatars/cpp/full-reference.md avatars/technology/cpp/full-reference.md`
      (preserves full git history for the file)

### Step 17.2 — Update AVATAR-RAG-INDEX.yaml
- [x] 17.2 ✓ c4ab135 In `avatars/AVATAR-RAG-INDEX.yaml`, locate the `cpp:` avatar block and change
      the `full_reference:` value from `docs/guides/avatars/cpp/full-reference.md` to
      `full-reference.md` (linter resolves relative to avatar base dir `avatars/technology/cpp/`)

### Step 17.3 — Fix guidance.md Link
- [x] 17.3 ✓ c4ab135 Update `avatars/technology/cpp/guidance.md` line 27: fix the relative link so it
      points correctly to `avatars/technology/cpp/full-reference.md`

### Step 17.4 — Fix Test Fixture
- [x] 17.4 ✓ c4ab135 Update `tests/unit/test_cpp_avatar/conftest.py` lines 39–42: change the
      `cpp_full_reference` session fixture path from `docs/guides/avatars/cpp/full-reference.md`
      to `avatars/technology/cpp/full-reference.md`

### Step 17.5 — Run Full Test Suite
- [x] 17.5 ✓ c4ab135 Run full test suite — all tests must pass (>=683)
      (20 test files use the `cpp_full_reference` fixture via conftest.py — only conftest.py
       needs updating; all 20 test files pick up the fix automatically)

### Step 17.6 — Linter Verification
- [x] 17.6 ✓ c4ab135 Run `aa-constitution-lint .` — linter must pass.
      Note: `f2e1552` (merged from main) weakens `AvatarRagFilesExistRule`. This step confirms
      the file move passes even the weakened rule. Full enforcement is restored when the
      `avatar-full-reference-pattern` proposal (S3) reverts `f2e1552` after this PR merges.

### Step 17.7 — Clean Up Stale docs/ Directory
- [x] 17.7 ✓ c4ab135 Verify `docs/guides/avatars/cpp/` contains no remaining files after the move;
      remove the now-empty directory if applicable

### Step 17.8 — Commit
- [x] 17.8 ✓ c4ab135 Commit: `fix(cpp-avatar): move full-reference.md into avatar dir, fix RAG index [Amendment-P]`

---

**Progress summary after Phase 17:** 276 tasks total (268 through Phase 16 + 8 Phase 17 tasks)

---

## Phase 18: Example Quality Enhancement — Edge Cases & Warnings

> **Goal:** Add `## Edge Cases & Warnings` to all 35 example files missing it, bringing the entire 51-file example set to 7/7 quality score.
> **Prerequisite:** Phase 17 merged; full test suite baseline passing.
> **Protocol:** Per ENG-4.1, each file is one Atomic TDD cycle (RED → GREEN → VERIFY → COMMIT).
> **Token rule:** No file may exceed 850t after addition. One file needs trim-to-fit (see 18.28).

### Step 18.0 — RED: Write Failing Test

- [x] 18.0 Write `test_every_example_has_edge_cases_section` in `tests/unit/test_cpp_avatar/test_example_quality.py` — asserts every file in `avatars/technology/cpp/examples/` contains `## Edge Cases` (prefix match). Run test → must FAIL on all 35 missing files.

---

### Step 18.1–18.5 — P1: Safety/Security-Critical Files

> Each task: add edge-case table (3+ rows), run full suite, commit. Human expert sign-off required before merge per R8.

- [x] 18.1 `ENG-6.1-strict-aliasing.md` (516t, adds ~100t → ~616t) — edge cases: type-punning via union, `memcpy`-based punning, `volatile`-qualified pointer casts, ABI breaks across TU boundaries
- [x] 18.2 `ENG-6.1-misra-do278a.md` (597t, adds ~100t → ~697t) — edge cases: deviation approval workflow, static-analysis false positives requiring suppressions, MISRA Rule 11.3 vs pointer arithmetic in legacy drivers
- [x] 18.3 `ENG-4.1-far117-traceability.md` (459t, adds ~100t → ~559t) — edge cases: split-certification artefacts across repos, test IDs not matching FAA-accepted format, duty-time boundary at midnight UTC
- [x] 18.4 `ENG-6.5-input-validation.md` (348t, adds ~100t → ~448t) — edge cases: multi-byte UTF-8 in fixed-width fields, integer overflow before range check, validation bypass via proxy structs
- [x] 18.5 `ENG-6.1-smart-pointers.md` (320t, adds ~100t → ~420t) — edge cases: `shared_ptr` in cyclic graphs causing leaks, `weak_ptr::lock()` in multithreaded destruction race, `unique_ptr<T[]>` with virtual destructors

---

### Step 18.6–18.10 — P2: Medium-Risk Files

- [x] 18.6 `ENG-6.1-raii-c-api-wrapper.md` (389t → ~489t) — edge cases: double-free if move constructor throws, destructor ordering in DLL unload, RAII wrapper around non-owning handle
- [x] 18.7 `ENG-6.1-thread-migration.md` (403t → ~503t) — edge cases: detached thread accessing destroyed stack frame, `pthread_cancel` with C++ objects, POSIX thread priorities not mapping to `std::thread`
- [x] 18.8 `ENG-3.7-error-handling.md` (467t → ~567t) — edge cases: `std::expected<void, E>` monadic chain termination, exception-neutral code mixing with `expected`, error code slicing in inheritance hierarchies
- [x] 18.9 `ENG-7.1-failure-handling.md` (510t → ~610t) — edge cases: cascading partial degradation triggering full shutdown, health-check false positive under load spike, degraded-mode state persisting after recovery
- [x] 18.10 `ENG-3.1-perfect-forwarding.md` (520t → ~620t) — edge cases: forwarding to overloaded functions causes ambiguity, `std::forward` of rvalue ref in a loop body, interaction with `explicit` constructors

---

### Step 18.11–18.16 — P3a: Remaining 5/7 Files

- [x] 18.11 `ENG-3.1-complexity.md` (354t → ~454t) — edge cases: cyclomatic counter ignores template instantiation depth, lambda expressions inflate line-count metrics
- [x] 18.12 `ENG-3.1-feature-detection.md` (334t → ~434t) — edge cases: `__has_include` succeeds but header is incomplete, feature macros defined differently per TU
- [x] 18.13 `ENG-3.2-immutability.md` (333t → ~433t) — edge cases: `const` member function modifying `mutable` state, `const` reference to temporary lifetime extension
- [x] 18.14 `ENG-3.5-naming.md` (302t → ~402t) — edge cases: reserved identifiers (`_Uppercase`, double-underscore), macro name collision with system headers
- [x] 18.15 `ENG-4.2-test-pyramid.md` (347t → ~447t) — edge cases: integration test disguised as unit test via heavy mocking, test pyramid inversion in legacy brownfield repo
- [x] 18.16 `ENG-5.5-observability.md` (451t → ~551t) — edge cases: structured log field name collision with framework reserved keys, tracing context lost across thread-pool boundaries

---

### Step 18.17–18.27 — P3b: 6/7 Group (First 11)

- [x] 18.17 `ENG-2.1-aggregates.md` (412t → ~512t) — edge cases: aggregate initialisation with base-class member shadowing, designated initialisers with bit-fields
- [x] 18.18 `ENG-2.2-layers.md` (463t → ~563t) — edge cases: circular dependency introduced via template specialisation in header, utility class placed in wrong layer
- [x] 18.19 `ENG-3.1-code-smell-raii-conversion.md` (497t → ~597t) — edge cases: RAII wrapper breaks ABI when exported from shared library, converting global C resource handle
- [x] 18.20 `ENG-3.1-concepts.md` (354t → ~454t) — edge cases: concept subsumption ordering not matching expected overload, concept constraint not checked on explicit instantiation
- [x] 18.21 `ENG-3.1-coroutines.md` (575t → ~675t) — edge cases: coroutine destroyed before final suspend, `co_await` in destructor, promise type default constructor missing
- [x] 18.22 `ENG-3.1-pmr-allocators.md` (510t → ~610t) — edge cases: `monotonic_buffer_resource` used past buffer lifetime, upstream allocator propagation in container copy
- [x] 18.23 `ENG-4.1-atomic-tdd.md` (499t → ~599t) — edge cases: test touching multiple responsibilities (hidden coupling), GREEN achieved by hard-coding rather than implementing
- [x] 18.24 `ENG-4.1-characterization-test-pattern.md` (530t → ~630t) — edge cases: characterization test passing on wrong platform due to UB, updating golden output without investigation
- [x] 18.25 `ENG-4.4-test-structure.md` (493t → ~593t) — edge cases: `SCOPED_TRACE` in deeply nested loops obscures failure location, fixture setUp/tearDown asymmetry causing state leak
- [x] 18.26 `ENG-5.2-cmake-governance.md` (469t → ~569t) — edge cases: target alias collision between subprojects, `PRIVATE`/`PUBLIC` link specifier causing transitive pollution
- [x] 18.27 `ENG-5.2-cmake-mixed-standard.md` (696t → ~796t) — edge cases: `CXX_STANDARD` not propagating through `FetchContent`, per-target standard override silently ignored by old CMake

---

### Step 18.28 — P3c: Trim-to-Fit File

- [x] 18.28 `ENG-5.2-project-structure.md` (803t — **trim required**) — trim "Brownfield Adaptation" 4-step prose list to a 2-row compact table (saves ~50t); then add 3-row edge-case table; verify final token count is 850t or below

---

### Step 18.29–18.35 — P3d: 6/7 Group (Last 7)

- [x] 18.29 `ENG-6.1-legacy-modernization-before-after.md` (532t → ~632t) — edge cases: before/after diff introduces ABI break invisible to unit tests, modernisation on hot path degrades performance
- [x] 18.30 `ENG-6.1-move-semantics.md` (424t → ~524t) — edge cases: moved-from object used after move (silent UB), move constructor marked `noexcept` incorrectly enabling optimisation that breaks strong exception guarantee
- [x] 18.31 `ENG-6.1-thread-safety.md` (367t → ~467t) — edge cases: `static` local variable init race in pre-C++11 compilers (brownfield), `volatile` mistaken for thread synchronisation
- [x] 18.32 `ENG-7.2-circuit-breaker.md` (358t → ~458t) — edge cases: half-open state not resetting under sustained low error rate, circuit breaker tripping on client-side timeout rather than server error
- [x] 18.33 `ENG-7.3-retry-backoff.md` (387t → ~487t) — edge cases: retry on non-idempotent operation causing duplicate side-effects, jitter using non-thread-safe `rand()`
- [x] 18.34 `ENG-7.4-timeout-governance.md` (433t → ~533t) — edge cases: `std::future::wait_for` returning `deferred` instead of `timeout`, nested timeout shorter than outer causing premature cancellation
- [x] 18.35 `ENG-7.5-bulkhead-isolation.md` (361t → ~461t) — edge cases: bulkhead pool exhaustion not surfaced as distinct error code, shared thread pool defeating isolation guarantee

---

### Step 18.36 — Full Suite Verification

- [x] 18.36 Run full test suite — all tests must pass (686+ with new edge-case test); run `aa-constitution-lint .`; verify no example file exceeds 850t ✓ d24dbc3 (710 passed, 17/17 linter)

### Step 18.37 — Update Progress + Commit

- [x] 18.37 Update `PROGRESS.md` with Phase 18 completion ✓ 4ae0b2e

---

**Progress summary after Phase 18:** 323 tasks total (276 through Phase 17 + 37 Phase 18 + 10 supplemental) — **323/323 complete**
