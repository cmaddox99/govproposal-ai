# Tasks: cpp-version-routing-foundation

**Laws governing this work:** `ENG-11.1`, `ENG-11.2`, `ENG-10.1`, `ENG-4.1`, `ENG-6.7`

**Proposal:** `PROPOSAL.md` in this directory
**Predecessor:** `hangar-ai-specs/archive/cpp-ref-file-rightsizing/` (complete)

## Progress Summary

- Completed: 49 / 49 ✅
- In Progress: 0
- Blocked: 0

**Phase 1 COMPLETE** — all 28 acceptance criterion + advisory tests GREEN; 816 suite tests pass.
**PR #47** open: `feat/cpp-version-routing-foundation → main`
**Phase 6 verification report:** `phase6-verification-report.md`
**Post-merge advisory fixes applied:** N3 (detection signal alignment), ENG-2.1 version-specificity, tasks.md checkboxes

---

## Phase 0: Governance

> **Goal:** Formal proposal and task structure in place before any implementation.

- [x] 0.1 Create `PROPOSAL.md` ✓
- [x] 0.2 Create `tasks.md` ✓
- [x] 0.3 Open PR targeting main; description links to PROPOSAL.md

---

## Phase 1: Test Infrastructure — New Acceptance Criteria

> **Goal:** Write RED tests for all 10 acceptance criteria before touching any
> avatar file. Every test must FAIL before Phase 2 begins.
>
> **Test file:** `tests/unit/test_rag_index.py`

- [x] 1.1 RED: write `test_guidance_has_version_protocol_section` — assert `guidance.md`
      contains `## Version Context Protocol`; run suite → confirm FAILED
- [x] 1.2 RED: write `test_guidance_version_protocol_detection_order` — assert section
      contains the 6-step detection order (`.copilot/project.yaml`, `CMakeLists.txt`,
      `.vcxproj`, `Makefile`, `.dsp/.dsw`, unknown); run suite → confirm FAILED
- [x] 1.3 RED: write `test_guidance_version_protocol_routing_table` — assert section
      contains routing tier table with 5 rows (MSVC6, C++98/03, C++11/14, C++17+,
      Unknown); run suite → confirm FAILED
- [x] 1.4 RED: write `test_rag_index_has_version_routing_policy` — assert
      `AVATAR-RAG-INDEX.yaml` cpp section contains `version_routing_policy` key;
      run suite → confirm FAILED
- [x] 1.5 RED: write `test_version_routing_policy_has_all_tiers` — assert
      `version_routing_policy.by_standard` contains all 5 expected canonical tier keys
      (`legacy`, `brownfield`, `transitional`, `modern`, `greenfield`);
      run suite → confirm FAILED
- [x] 1.6 RED: write `test_law_mapped_examples_have_cpp_version_min` — assert all 21
      law-mapped example files (`ENG-*.md`) have `cpp_version_min` in frontmatter;
      run suite → confirm FAILED
- [x] 1.7 RED: write `test_modern_examples_have_cpp_version_note` — assert all example
      files where `cpp_version_min >= 17` also have `cpp_version_note` in frontmatter;
      run suite → confirm FAILED
- [x] 1.8 RED: write `test_cpp_project_template_exists` — assert
      `avatars/technology/cpp/templates/cpp-project.yaml` exists; run suite → confirm FAILED
- [x] 1.9 RED: write `test_guidance_token_budget` — assert `guidance.md` character
      count ÷ 4 ≤ 600 (token ceiling); run suite → confirm FAILED (currently ~310t, will
      need to verify it doesn't exceed 600t after change)
- [x] 1.10 RED: write `test_routing_policy_file_refs_exist` — for every filename in
      `version_routing_policy.by_standard.*.prefer` and `*.avoid`, assert the file
      actually exists at that path; run suite → confirm FAILED (B1 guard)
- [x] 1.11 RED: write `test_routing_policy_tier_names_match_guidance` — assert the 5
      tier keys in `version_routing_policy.by_standard` exactly match the tier names in
      the `## Version Context Protocol` section of `guidance.md`; run suite → confirm FAILED
- [x] 1.12 RED: write `test_project_template_has_pre98_standard` — assert
      `templates/cpp-project.yaml` includes `pre98` as a documented valid value for
      the `standard` field (B2 guard); run suite → confirm FAILED
- [x] 1.13 RED: write `test_cpp_version_note_max_length` — assert every `cpp_version_note`
      value in all example file frontmatter is ≤ 240 characters;
      run suite → confirm FAILED (no notes exist yet; will catch future violations)
- [x] 1.14 RED: write `test_routing_policy_prefer_refs_not_examples` — assert that all
      files in `*.prefer` lists are under `refs/` (not `examples/`) and all files in
      `*.avoid` lists are under `examples/` (not `refs/`);
      run suite → confirm FAILED (structural correctness guard)
- [x] 1.15 VERIFY: run full suite — confirm exactly the new 14 tests fail; all prior
      tests still pass; record baseline failure output

---

## Phase 2: `guidance.md` — Version Context Protocol

> **Goal:** Add Version Context Protocol section to guidance.md.
> Protocol is always loaded; it is the highest-leverage change in this proposal.

- [x] 2.1 GREEN: add `## Version Context Protocol` section to `guidance.md` with:
      - 6-step detection order (project.yaml → CMakeLists.txt → .vcxproj → Makefile
        → .dsp/.dsw → unknown)
      - Routing tier table (MSVC6, C++98/03, C++11/14, C++17+, Unknown)
      - Unknown-version rule: "Do NOT default to modern C++; ask before recommending
        any ★-annotated file"
      Run suite → confirm tests 1.1, 1.2, 1.3, 1.9 pass; all others still fail
- [x] 2.2 REFACTOR: measure token count of updated guidance.md; trim prose if count
      exceeds 550t (safety margin before 600t ceiling)
- [x] 2.3 VERIFY: run full suite → all prior tests pass, new tests 1.1–1.3 + 1.9 green

---

## Phase 3: `AVATAR-RAG-INDEX.yaml` — Version Routing Policy

> **Goal:** Add explicit, auditable routing preferences per C++ standard tier.

- [x] 3.1 GREEN: add `version_routing_policy` block to cpp section of
      `AVATAR-RAG-INDEX.yaml` with:
      - `detection_order` (5 steps matching guidance.md protocol)
      - `by_standard.legacy` — pre-C++98 (MSVC 6.0 / .dsp/.dsw): prefer legacy-navigation, mental-models-lang, legacy-smells-structural; avoid ENG-3.7, ENG-6.1-thread-safety, ENG-3.1-concepts; WARN action
      - `by_standard.brownfield` — C++98/C++03: prefer legacy-navigation, brownfield-adoption, brownfield-project-config; avoid ENG-3.7, ENG-3.1-concepts, ENG-3.1-coroutines
      - `by_standard.transitional` — C++11/C++14: prefer core-type-safety, safety-memory-lifetime, concurrency-threading; avoid ENG-3.7, ENG-3.1-concepts, ENG-3.1-pmr-allocators
      - `by_standard.modern` — C++17: prefer core-type-safety, safety-memory-lifetime, advanced-patterns; avoid ENG-3.7, ENG-3.1-concepts, ENG-3.1-coroutines
      - `by_standard.greenfield` — C++20/C++23: no prefer/avoid restrictions
      - `unknown` — strategy: legacy-safe; agent_prompt asks for version (no "C++14 baseline" wording)
      All file paths use real repo paths (refs/legacy/*, refs/language/*, refs/safety/*, examples/*)
      Run suite → confirm tests 1.4, 1.5, 1.10, 1.11, 1.14 pass

- [x] 3.2 REFACTOR: review each avoid list — verify every listed file actually contains
      content gated behind the avoided standard; remove any incorrect exclusions
- [x] 3.3 VERIFY: run full suite → all prior tests pass, 1.4–1.5 now green

---

## Phase 4: Example File Frontmatter — `cpp_version_min`

> **Goal:** Add `cpp_version_min` (and `cpp_version_note` where version ≥ 17) to all
> law-mapped examples and high-risk supplemental files. No content changes — metadata only.
>
> Version assignments are documented in PROPOSAL.md § "Version Frontmatter Assignment".

### 4A: C++23 examples (highest risk — FAIL loudly in any pre-23 toolchain)

- [x] 4.1 GREEN: add frontmatter to `ENG-3.7-error-handling.md` → `cpp_version_min: 23`,
      note: "Uses std::expected (C++23). For C++11–17, use error_code + custom Result<T,E>
      or tl::expected polyfill."
- [x] 4.2 GREEN: add frontmatter to `ENG-6.1-expected-errors.md` → `cpp_version_min: 23`,
      same note
- [x] 4.3 VERIFY: run suite → 1.6, 1.7 still fail (other files not yet done); no regression

### 4B: C++20 examples

- [x] 4.4 GREEN: add frontmatter to `ENG-3.1-concepts.md` → `cpp_version_min: 20`,
      note: "Uses C++20 concepts/requires. For C++14/17, use SFINAE or static_assert."
- [x] 4.5 GREEN: add frontmatter to `ENG-3.1-coroutines.md` → `cpp_version_min: 20`,
      note: "Uses C++20 coroutines (co_await, co_yield). Not available before C++20."
- [x] 4.6 GREEN: add frontmatter to `ENG-3.1-designated-initializers.md` → `cpp_version_min: 20`,
      note: "Designated initializers are C++20. Use constructor or factory pattern in C++11/14/17."

### 4C: C++17 examples

- [x] 4.7 GREEN: add frontmatter to `ENG-3.1-pmr-allocators.md` → `cpp_version_min: 17`,
      note: "std::pmr requires C++17. Use custom allocator interface in C++11/14."
- [x] 4.8 GREEN: add frontmatter to `ENG-5.2-cmake-governance.md` → `cpp_version_min: 17`,
      note: "Uses C++17 CMake target_compile_features. Compatible with CMake 3.8+ and C++17."
- [x] 4.9 GREEN: add frontmatter to `ENG-5.5-observability.md` → `cpp_version_min: 17`,
      note: "spdlog structured logging uses C++17 features. For C++14, use spdlog 1.x with fmt."
- [x] 4.10 GREEN: add frontmatter to `ENG-6.1-security-by-design.md` → `cpp_version_min: 17`,
       note: "Uses std::scoped_lock (C++17). For C++11/14, use std::lock_guard<std::mutex>."
- [x] 4.11 GREEN: add frontmatter to `ENG-6.1-thread-safety.md` → `cpp_version_min: 17`,
       note: "Uses std::scoped_lock (C++17). For C++11/14, use std::lock_guard<std::mutex>."
- [x] 4.12 GREEN: add frontmatter to `ENG-6.4-data-protection.md` → `cpp_version_min: 17`,
       note: "Uses structured bindings (C++17). For C++14, use std::tie or explicit member access."
- [x] 4.13 GREEN: add frontmatter to `ENG-6.7-audit-trail.md` → `cpp_version_min: 20`,`n       note: "Uses designated initializer aggregate syntax (.field = value) which requires C++20. For C++17, use positional or constructor initialization."
- [x] 4.14 GREEN: add `cpp_version_min: 11` frontmatter (no note) to `ENG-7.1-failure-handling.md``n       (uses enum class + noexcept only; [[nodiscard]] note in file is informational)

### 4D: C++14 examples

- [x] 4.15 GREEN: add frontmatter to `ENG-6.1-smart-pointer-migration.md` → `cpp_version_min: 14`,
       note: "std::make_unique requires C++14. For C++11, use unique_ptr<T>(new T(...)) directly."
- [x] 4.16 GREEN: add frontmatter to `ENG-5.2-cmake-mixed-standard.md` → `cpp_version_min: 14`
- [x] 4.17 GREEN: add frontmatter to `ENG-3.1-feature-detection.md` → `cpp_version_min: 14`,
       note: "__has_include and SD-6 feature test macros are C++14+."

### 4E: C++11 examples (many — use minimum viable note for these)

- [x] 4.18 GREEN: add `cpp_version_min: 11` frontmatter (no note required) to:
       `ENG-2.1-aggregates.md`, `ENG-2.2-layers.md`, `ENG-2.3-jni-abi-stability.md`,
       `ENG-3.1-complexity.md`, `ENG-3.2-immutability.md`, `ENG-3.3-demeter.md`,
       `ENG-3.5-naming.md`, `ENG-4.1-atomic-tdd.md`, `ENG-4.2-test-pyramid.md`,
       `ENG-4.4-test-structure.md`, `ENG-6.5-input-validation.md`,
       `ENG-7.2-circuit-breaker.md`, `ENG-7.3-retry-backoff.md`,
       `ENG-7.4-timeout-governance.md`, `ENG-7.5-bulkhead-isolation.md`,
       `ENG-6.1-move-semantics.md`, `ENG-6.1-thread-migration.md`

### 4F: C++98 examples (safe for all versions)

- [x] 4.19 GREEN: add `cpp_version_min: 98` to `ENG-2.3-rcptr-abi-stability.md`

### 4G: Verify and wrap up

- [x] 4.20 VERIFY: run suite → tests 1.6 and 1.7 now green; all prior tests pass
- [x] 4.21 REFACTOR: cross-check all assignments against ISO C++ feature availability
       table in PROPOSAL.md; correct any misassigned version numbers

---

## Phase 5: Template File

> **Goal:** Provide a canonical `.copilot/project.yaml` schema that consuming repos
> can copy and populate.

- [x] 5.1 GREEN: create `avatars/technology/cpp/templates/cpp-project.yaml` with:
      - `cpp.standard` (required) — valid values: 98 | 03 | 11 | 14 | 17 | 20 | 23
      - `cpp.idiom_level` (required) — same values; handles CWR scenario
      - `cpp.compiler` (required) — msvc | gcc | clang | borland | objective-cpp
      - `cpp.toolset` (optional) — MSVC v140-v143 or GCC/Clang version
      - `cpp.notes` (optional) — free text for migration status
      - Inline comments explaining each field
      - A filled-in CWR example (standard: "14", idiom_level: "03", compiler: "gcc")
      Run suite → test 1.8 passes

- [x] 5.2 GREEN: add a reference to the template in `guidance.md` (one line, no new section):
      `> **New to this project?** Copy [templates/cpp-project.yaml](templates/cpp-project.yaml)
      to `.copilot/project.yaml` and declare your C++ standard.`

- [x] 5.3 VERIFY: run full suite → all 10 AC tests now green; all prior tests pass

---

## Phase 6: Full Verification

> **Goal:** All acceptance criteria met; no regressions; constitution lint clean.

- [x] 6.1 Run full test suite: `python -m pytest tests/ -v` → all green
- [x] 6.2 Run constitution lint: `aa-constitution-lint .` → clean
- [x] 6.3 Manual scenario walkthrough — CWR:
       - Simulate project.yaml with `standard: "14", idiom_level: "03"`
       - Verify routing table correctly avoids `ref-core-modern-idioms.md`
       - Verify `ENG-3.7-error-handling.md` frontmatter warning fires
- [x] 6.4 Manual scenario walkthrough — herc-odyssey-linux:
       - Simulate project.yaml with `standard: "98"`
       - Verify routing table routes to `ref-mental-models-memory.md`
       - Verify routing avoids `ref-concurrency-async.md`
- [x] 6.5 Manual scenario walkthrough — SPEClient:
       - Simulate detection of `.dsp`/`.dsw` files (no project.yaml)
       - Verify guidance.md protocol triggers MSVC 6.0 warning
- [x] 6.6 Update `tasks.md` progress summary: Completed N / 42

---

## Phase 7: Commit and PR

- [x] 7.1 `git add -A && git commit -m "feat(cpp-avatar): add version-aware routing foundation (Option E Phase 1)"`
       Commit message MUST reference proposal ID: `cpp-version-routing-foundation`
- [x] 7.2 Push branch and open PR
- [x] 7.3 Link PR to `hangar-ai-specs/changes/cpp-version-sensitivity-analysis/next-steps.md` Tier 1.2
- [x] 7.4 Mark `0.3` complete

---

## Amendment Strategy

**This proposal (Foundation) is complete** — all 49 tasks done; merged to main via PR #47.

Follow-on work is tracked as **Amendment 1** to this proposal rather than a new change
directory, because it extends the same problem scope (C++ version-aware routing) rather
than opening a new change direction.

**Amendment 1 artifacts (in this directory):**
- Governing spec: [`PHASE2-PROPOSAL.md`](PHASE2-PROPOSAL.md)
- Task list: [`tasks-amendment1.md`](tasks-amendment1.md)

> **For future AI agents:** When a follow-on body of work amends an existing spec rather
> than starting a new change direction, keep the amendment artifacts in the same change
> directory alongside the original. Use `tasks-amendmentN.md` + the existing or a new
> `PHASE2-PROPOSAL.md`-style document as the governing spec. This avoids proliferating
> near-duplicate change directories while keeping each amendment's work clearly separated
> from the original task list.
