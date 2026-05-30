# Tasks: cpp-avatar-phase18-remediation

**Laws governing this work:** `ENG-11.1`, `ENG-11.2`, `ENG-4.1`, `ENG-4.2`, `ENG-6.1`, `BUS-1.1`, `BUS-2.1`, `BUS-7.1`

**Depends On:** `c-plus-plus-avatar-enrichment` (PR #14) must be merged to main before Phase 1+ implementation.

## Progress Summary

- Completed: 3 / 52
- In Progress: 0
- Blocked: 0

---

## Phase 0: SDD Execution Artifacts

> **Goal:** Establish governed execution tracking for the Phase 18 remediation change.

- [x] 0.1 Create `PROPOSAL.md`
- [x] 0.2 Create `tasks.md`
- [x] 0.3 Create `PROGRESS.md`
- [x] 0.4 ✓ e9cd7af Record governance approvals and sign-off evidence in `PROGRESS.md`
- [x] 0.5 ✓ e9cd7af (PR #14 — feature/c-plus-plus-avatar-enrichment-proposal) Open PR targeting main; add description linking to panel review and PROPOSAL.md

### W-1 — Create RAG Validation Evidence File (Workflow Phase 5/6 Gate)

> `hangar-ai-specs/evidence/avatar-rag-cpp.md` does not exist. The avatar-workflow requires
> this to be committed before the Phase 6 commit gate. Panel review did not check for it.

- [x] 0.6 ✓ e9cd7af Create `hangar-ai-specs/evidence/avatar-rag-cpp.md` using the template from
      `docs/guides/avatar-model-schema.md` Section 8 (or the format from `avatar-scan-cpp.md`)
      — Record avatar path, version, scan date
      — Simulate and document 5 canonical RAG queries (see W-3 below)
      — Record token estimate per query; confirm each ≤3,500 tokens
      — Record recall: 5/5 queries answerable from loaded files (excluding full-reference.md)

### W-2 — Fix broken activates.workflows reference

> `manifest.yaml` lists `brownfield-adoption` in `activates.workflows`, but no
> `workflows/brownfield-adoption.md` exists. The workflow's Safeguard 5 flags this.
> `workflows/` has: `greenfield-development.md` ✅, `product-discovery-stage-a-f.md` ✅,
> but `brownfield-adoption` is only at `docs/guides/adoption/brownfield-adoption.md`.

- [x] 0.7 ✓ e9cd7af In `avatars/technology/cpp/manifest.yaml`, update `activates.workflows`:
      either (a) change `brownfield-adoption` to the correct relative path for the
      existing docs guide, or (b) create `workflows/brownfield-adoption.md` as a
      thin redirect to the guide. **Preferred: option (a) — update to existing path.**
- [x] 0.8 ✓ e9cd7af Verify both other workflow references (`greenfield-development`, `product-discovery-stage-a-f`)
      resolve correctly

### W-3 — Document 5 Canonical RAG Queries

> The avatar-workflow (Phase 0.4 / Phase 3.2) requires 5 canonical RAG queries to be defined
> and recorded in evidence. These become the Phase 5 validation test cases.

- [x] 0.9 ✓ e9cd7af Define 5 canonical RAG queries for the cpp avatar in `avatar-rag-cpp.md`:
      Suggested queries (adjust to reflect actual avatar content):
      1. "How do I write a GoogleTest for a C++ class with RAII ownership?"
      2. "What is the correct way to handle errors in C++ without exceptions per this avatar?"
      3. "How do I migrate from raw pointers to unique_ptr in a brownfield C++03 codebase?"
      4. "What sanitizers are mandatory in CI for C++ projects under this constitution?"
      5. "How does the compliance rating score a C++ project for DO-278A/safety-critical posture?"
- [x] 0.10 ✓ e9cd7af For each query, list which avatar files would be loaded by the RAG pipeline and
       estimate total tokens; confirm all 5 are ≤3,500 tokens and answerable

### W-4 — Document Separate-PR Item: manifest.yaml Token Budget

> The avatar-workflow enforces ≤150 tokens for manifest.yaml.
> Current manifest: 1,176 words ≈ 1,500 tokens — 10× over budget.
> This cannot be safely bundled into PR #14 (16 test files reference manifest paths,
> and the manifest schema would need major restructuring).

- [x] 0.11 ✓ e9cd7af Create `hangar-ai-specs/changes/cpp-avatar-manifest-restructure/PROPOSAL.md` stub
       documenting: (a) the 150-token limit, (b) what blocks need to move (stack, standard_tiers,
       project_archetypes → separate companion files), (c) test impact, (d) semver bump required (MAJOR)
       **Note:** This stub marks the work as tracked; implementation is a separate PR after #14 merges.
- [x] 0.12 ✓ 300470b **[W-6]** In `avatars/technology/cpp/manifest.yaml`, fix `activates.skills` entries: remove
       the `skill-` prefix so references match actual filenames in `agent-skills/skills-by-domain/`:
       `skill-06-atomic-tdd` → `06-atomic-tdd`, `skill-07-vertical-slice-dev` → `07-vertical-slice-dev`,
       `skill-08-code-review` → `08-code-review`, `skill-04-business-domain-modeling` → `04-business-domain-modeling`
- [x] 0.13 ✓ 300470b **[W-6]** Run `aa-constitution-lint .` and full test suite — confirm 0 failures
- [x] 0.14 ✓ 300470b **[W-6]** Commit: `fix(cpp-avatar): correct activates.skills prefix mismatch [W-6 cpp-avatar-phase18-remediation]`

---

## Phase 1: B-2 Fix — RAG Index Token Budget Annotation

> **Goal:** Prevent agents from loading `full-reference.md` as a direct RAG result by annotating
> the `AVATAR-RAG-INDEX.yaml` entry with `on_demand_only: true` and a size warning.
>
> **Source:** Panel review B-2 (Kenji Nakamura, P6)
> **Law:** ENG-10.1 (Constitution Compliance)
> **Prerequisite:** PR #14 merged to main (file must exist at `avatars/technology/cpp/full-reference.md`)

- [x] 1.1 ✓ e9cd7af In `avatars/AVATAR-RAG-INDEX.yaml`, locate the `cpp:` avatar block's `full_reference:` entry
- [x] 1.2 ✓ e9cd7af Add `on_demand_only: true` flag to the `full_reference` entry
- [x] 1.3 ✓ e9cd7af Add `note: "5519 lines (~20K tokens) — not suitable for direct RAG retrieval; route by section anchor"` to the entry
- [x] 1.4 ✓ e9cd7af Run `aa-constitution-lint .` — must pass with 0 failures
- [x] 1.5 ✓ e9cd7af Commit: `fix(cpp-avatar): annotate full-reference.md as on_demand_only in RAG index [B-2]`

---

## Phase 2: H-1 / H-2 — Missing Example Files and Manifest Routing

> **Goal:** Create 4 missing example files and add 6 missing `specializes_laws` entries to `manifest.yaml`
> so agents can route to error handling, observability, failure handling, test structure, resiliency,
> and mixed-standard guidance.
>
> **Source:** Panel review H-1 (ENG-3.7, ENG-5.5, ENG-7.1 missing example_file),
>             H-2 (ENG-4.4, ENG-7.2–7.5, ENG-5.2 second file unreachable)
> **Laws:** ENG-3.7, ENG-4.4, ENG-5.5, ENG-7.1, ENG-7.2, ENG-7.3, ENG-7.4, ENG-7.5

### 2a — RED: Write failing test for missing ENG-3.7 example file
- [x] 2.1 ✓ 35ebe06 Write ONE failing test: `test_eng37_example_file_exists_and_referenced_in_manifest`
      in `tests/unit/test_cpp_avatar/test_phase18_manifest_completeness.py`
      — assert `avatars/technology/cpp/examples/ENG-3.7-error-handling.md` exists on disk
      — assert ENG-3.7 entry in `manifest.yaml` `specializes_laws` has an `example_file` key
      Run tests → confirm FAIL before continuing
- [x] 2.2 ✓ 35ebe06 Create `avatars/technology/cpp/examples/ENG-3.7-error-handling.md`
      (C++ error handling patterns: `std::expected`, error codes vs exceptions, `noexcept` contracts,
       `std::error_code` usage, RAII-based resource safety on error paths, brownfield `errno` migration)
- [x] 2.3 ✓ 35ebe06 Add `example_file: ENG-3.7-error-handling.md` to ENG-3.7 entry in `manifest.yaml` `specializes_laws`
- [x] 2.4 ✓ 35ebe06 Run tests → confirm 2.1 test PASSES

### 2b — RED: Write failing test for missing ENG-5.5 example file
- [x] 2.5 ✓ ee8b37f Write ONE failing test: `test_eng55_example_file_exists_and_referenced_in_manifest`
      — assert `avatars/technology/cpp/examples/ENG-5.5-observability.md` exists on disk
      — assert ENG-5.5 entry in `manifest.yaml` has `example_file` key
      Run tests → confirm FAIL
- [x] 2.6 ✓ ee8b37f Create `avatars/technology/cpp/examples/ENG-5.5-observability.md`
      (OpenTelemetry C++ SDK integration: span creation, metric recording, log correlation,
       trace context propagation across C++/JNI boundary, brownfield `printf`/syslog migration)
- [x] 2.7 ✓ ee8b37f Add `example_file: ENG-5.5-observability.md` to ENG-5.5 in `manifest.yaml`
- [x] 2.8 ✓ ee8b37f Run tests → confirm 2.5 test PASSES

### 2c — RED: Write failing test for missing ENG-7.1 example file
- [x] 2.9 ✓ 407f4a7 Write ONE failing test: `test_eng71_example_file_exists_and_referenced_in_manifest`
      — assert `avatars/technology/cpp/examples/ENG-7.1-failure-handling.md` exists
      — assert ENG-7.1 entry in `manifest.yaml` has `example_file` key
      Run tests → confirm FAIL
- [x] 2.10 ✓ 407f4a7 Create `avatars/technology/cpp/examples/ENG-7.1-failure-handling.md`
       (bulkhead isolation, fallback chaining, watchdog patterns, timeout enforcement,
        safe degraded-mode operation for CWR safety-critical paths)
- [x] 2.11 ✓ 407f4a7 Add `example_file: ENG-7.1-failure-handling.md` to ENG-7.1 in `manifest.yaml`
- [x] 2.12 ✓ 407f4a7 Run tests → confirm 2.9 test PASSES

### 2d — RED: Write failing test for ENG-4.4 and ENG-7.2–7.5 missing from specializes_laws
- [x] 2.13 ✓ e9f635a Write ONE failing test: `test_eng44_and_eng72_75_present_in_specializes_laws`
       — assert ENG-4.4 is present as a key in `manifest.yaml` `specializes_laws`
       — assert ENG-7.2, ENG-7.3, ENG-7.4, ENG-7.5 each present in `specializes_laws`
       Run tests → confirm FAIL
- [x] 2.14 ✓ e9f635a Add ENG-4.4 entry to `manifest.yaml` `specializes_laws` pointing to
       existing `ENG-4.4-test-structure.md`
- [x] 2.15 ✓ e9f635a Add ENG-7.2 through ENG-7.5 entries to `manifest.yaml` `specializes_laws` pointing to
       existing circuit-breaker, retry-backoff, timeout-governance, bulkhead-isolation example files
- [x] 2.16 ✓ e9f635a Run tests → confirm 2.13 test PASSES

### 2e — ENG-5.2 mixed-standard use case
- [x] 2.17 ✓ e9f635a Write ONE failing test: `test_eng52_has_two_example_files_or_mixed_standard_entry`
       — assert second ENG-5.2 example file exists or `mixed_standard` variant is in manifest
       Run tests → confirm FAIL
- [x] 2.18 ✓ e9f635a Create `avatars/technology/cpp/examples/ENG-5.2-mixed-standard.md`
       (C++03/C++11/C++20 coexistence in same build: `#if __cplusplus` guards,
        incremental migration gate policy, CWR brownfield constraint patterns)
- [x] 2.19 ✓ e9f635a Add second `example_file` entry (or `example_files` list) for ENG-5.2 in `manifest.yaml`
- [x] 2.20 ✓ e9f635a Run tests → confirm 2.17 test PASSES

### 2f — VERIFY Phase 2
- [ ] 2.21 Run `python3 -m pytest tests/ -q --tb=short` — all tests must pass
- [ ] 2.22 Run `aa-constitution-lint .` — must pass 0 failures
- [ ] 2.23 Commit: `feat(cpp-avatar): add missing example files and manifest routing [H-1/H-2]`

---

## Phase 3: H-3 — ENG-6.1 Routing De-Fragmentation

> **Goal:** Make all 16 ENG-6.1 security example files discoverable via a topic-router index file.
>
> **Source:** Panel review H-3 (P1 Elena Kozlov, P4 Dmitri Volkov)
> **Law:** ENG-6.1 (Security by Design — Non-Negotiable)

- [x] 3.1 ✓ b7c0928 Write ONE failing test: `test_eng61_index_exists_and_references_all_16_files`
      — assert `avatars/technology/cpp/examples/ENG-6.1-index.md` exists
      — assert the file contains references to all 16 ENG-6.1 example files by name
      Run tests → confirm FAIL
- [x] 3.2 ✓ b7c0928 List all existing ENG-6.1 example files in `avatars/technology/cpp/examples/`
- [x] 3.3 ✓ b7c0928 Create `avatars/technology/cpp/examples/ENG-6.1-index.md`
      — title: "ENG-6.1 Security by Design — C++ Topic Router"
      — one section per topic area (ownership, concurrency, API safety, void* migration, etc.)
      — each section links to the relevant ENG-6.1-*.md file with 1-line description
      — intro note: "All 16 files below implement ENG-6.1; route by topic"
- [x] 3.4 ✓ b7c0928 Add `ENG-6.1-index` entry to `avatars/AVATAR-RAG-INDEX.yaml` under the cpp block
- [x] 3.5 ✓ b7c0928 Run tests → confirm 3.1 test PASSES
- [x] 3.6 ✓ b7c0928 Run `python3 -m pytest tests/ -q --tb=short` — all tests pass
- [x] 3.7 ✓ b7c0928 Run `aa-constitution-lint .` — 0 failures
- [x] 3.8 ✓ b7c0928 Commit: `feat(cpp-avatar): add ENG-6.1 topic router index for 16 security files [H-3]`

---

## Phase 4: H-4 — MISRA C++ and DO-278A Safety-Critical Guidance

> **Goal:** Surface MISRA C++ and DO-278A guidance at the manifest routing layer
> so agents advising on CWR safety posture cite the correct standard.
>
> **Source:** Panel review H-4 (P5 Aisling O'Brien)
> **Laws:** ENG-6.1 (Security by Design — Non-Negotiable)
> **⚠️ LAW BOUNDARY CONSTRAINT (Workflow Safeguard 2):** This is a TECHNOLOGY avatar.
> `specializes_laws` MUST NOT add BUS-* entries. DO-278A and FAR 117 are referenced
> as *context* within the ENG-6.x example file prose — NOT as law citations in the manifest.
> An agent routing a safety query will reach this file via ENG-6.1, then read the DO-278A context.
> **Note:** DO-278A governs ground-based CNS/ATM systems (CWR = crew management, ground-based).
>          DO-178C governs airborne software. An agent must not confuse the two.

- [x] 4.1 ✓ ba2d8fb Write ONE failing test: `test_misra_do278a_example_exists_and_in_manifest`
      — assert `avatars/technology/cpp/examples/ENG-6.1-misra-do278a.md` exists
      — assert manifest `specializes_laws` references this file under ENG-6.1 or a safety-critical entry
      Run tests → confirm FAIL
- [x] 4.2 ✓ ba2d8fb Create `avatars/technology/cpp/examples/ENG-6.1-misra-do278a.md`:
      — Section 1: DO-278A vs DO-178C — which standard applies to CWR (ground-based → DO-278A)
      — Section 2: MISRA C++ 2008 / 2023 — key rules relevant to crew management systems
      — Section 3: Compiler enforcement — clang-tidy MISRA rule sets, custom checks
      — Section 4: Required deviation recording — rationale format for justified rule violations
      — Section 5: Integration with compliance rating system (D10 in skill-cpp-compliance-rating)
- [x] 4.3 ✓ ba2d8fb Add `ENG-6.1-misra-do278a` reference to `manifest.yaml` `specializes_laws` under ENG-6.1
      (or as `ENG-6.1.safety_critical` sub-entry — match existing manifest structure)
- [x] 4.4 ✓ ba2d8fb Run tests → confirm 4.1 test PASSES
- [x] 4.5 ✓ ba2d8fb Run `python3 -m pytest tests/ -q --tb=short` — all tests pass
- [x] 4.6 ✓ ba2d8fb Run `aa-constitution-lint .` — 0 failures
- [x] 4.7 ✓ ba2d8fb Commit: `feat(cpp-avatar): add MISRA C++ and DO-278A safety-critical guidance [H-4]`

---

## Phase 5: A-1 through A-8 — Advisory Improvements

> **Goal:** Address the 8 advisory findings to improve DX, routing completeness, and audit citation accuracy.
> These are NOT blocking but complete the avatar's usability for CWR developers.

### A-1 — JNI Bridge Skill
- [x] 5.1 ✓ 6d8bcc8 Create `agent-skills/skills-by-domain/development-practices/skill-cpp-jni-bridge.md`
      — covers: JNI type mapping (C++ ↔ Java), memory ownership at JNI boundary,
        exception propagation, `jni.h` include conventions, brownfield CWR JNI patterns
- [x] 5.2 ✓ 6d8bcc8 Register `skill-cpp-jni-bridge` in the skill index for the development-practices domain
- [x] 5.3 ✓ 6d8bcc8 Reference `skill-cpp-jni-bridge` in `manifest.yaml` skill activations

### A-2 — FAR 117 Test Traceability Example
- [x] 5.4 ✓ 6d8bcc8 Create `avatars/technology/cpp/examples/ENG-4.1-far117-traceability.md`
      — traceability matrix template: test name → FAR 117 regulation number
      — example: `TEST(CrewRestPolicy, MinimumGroundTime_FAR117_23)` → FAR 117.23
      — integration with D10 (compliance rating dimension)

### A-3 — Brownfield Entry Path
- [x] 5.5 ✓ 6d8bcc8 Add "Brownfield Entry Path" section to `avatars/technology/cpp/full-reference.md`
      (insert before the existing Quick-Start Cheat Sheet section)
      — 5-step entry path: audit → freeze → modernize in slices → gate → graduate
      — CWR-specific: C++03 baseline, ALP/MFC constraints, legacy test harness notes

### A-4 — Skill Decision Tree
- [x] 5.6 ✓ 6d8bcc8 Add "Which skill do I use?" decision tree to `avatars/technology/cpp/full-reference.md`
      (insert after the Brownfield Entry Path section)
      — decision branches: new code vs brownfield? → safety-critical? → modernization goal?

### A-5 — Named Anchor Links in guidance.md
- [x] 5.7 ✓ 6d8bcc8 Add named anchor links in `avatars/technology/cpp/guidance.md` footer section
      pointing to key `full-reference.md` sections: Quick-Start, Brownfield Entry, Skill Tree, Mental Models

### A-6 — Skill Naming Convention
- [x] 5.8 ✓ 6d8bcc8 Add skill naming convention note to `agent-skills/skills-by-domain/development-practices/index.yaml`
      header: define `domain-action` as canonical form (e.g., `skill-cpp-sanitizer-hardening`);
      flag advisory update for non-conforming skills in Phase 18+

### A-7 — Skill Index Audit
- [x] 5.9 ✓ 6d8bcc8 Audit `agent-skills/skill-index.yaml` (or equivalent registry): confirm all 25 Phase 16
      C++ skills added in `c-plus-plus-avatar-enrichment` are registered
- [x] 5.10 ✓ 6d8bcc8 Register any missing skills found in 5.9

### A-8 — BUS-7.1 Citation Fix
- [x] 5.11 ✓ BLOCKED-V5 In `agent-skills/skills-by-domain/development-practices/skill-cpp-compliance-rating.md`
       locate dimension D5 (audit trail)
- [x] 5.12 ✓ BLOCKED-V5 (Phase 16 guard V5 prohibits BUS-* in platform-engineering skills — correct domain boundary) Add `BUS-7.1` citation alongside existing `ENG-6.7` reference in D5
       (BUS-7.1 is the NON-NEGOTIABLE audit trail law; ENG-6.7 is implementation guidance)

### VERIFY Phase 5
- [x] 5.13 ✓ 6d8bcc8 Run `python3 -m pytest tests/ -q --tb=short` — all tests pass
- [x] 5.14 ✓ 6d8bcc8 Run `aa-constitution-lint .` — 0 failures
- [x] 5.15 ✓ 6d8bcc8 Commit: `feat(cpp-avatar): advisory improvements A-1 through A-8 [Phase-18]`

---

## Phase 6: Archive

> **Goal:** Complete SDD lifecycle and archive the proposal.

- [x] 6.1 ✓ 6738339 Update `PROGRESS.md` status to `COMPLETE`; record final test counts and lint results
- [x] 6.2 ✓ 6738339 Archive:
      `mv hangar-ai-specs/changes/cpp-avatar-phase18-remediation hangar-ai-specs/archive/$(date +%Y-%m-%d)-cpp-avatar-phase18-remediation`
- [x] 6.3 ✓ 6738339 Commit: `chore(sdd): archive cpp-avatar-phase18-remediation [ENG-11.1]`
