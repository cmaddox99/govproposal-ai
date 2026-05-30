# C++ Avatar Enrichment — 7-Persona Panel Review

**Branch:** `feature/c-plus-plus-avatar-enrichment-proposal`
**Artefact reviewed:** `avatars/technology/cpp/` at Phase 17 (pre-completion)
**Review scope:** Constitution conformance · technical correctness · RAG architecture · brownfield/CWR readiness · safety-critical guidance · platform skill coherence · developer experience
**Constitution guidance consulted:** `workflows/avatar-workflow.md` Mode 5 (PR Review) + Mode 2 (Assess & Correct) · `laws/` ENG-2 through ENG-7 · `PROPOSAL.md` · `PROGRESS.md`

**Automated gate results:**

| Check | Result |
|---|---|
| `aa-constitution-lint .` | ❌ 1 FAILURE — `AVATAR-RAG-INDEX.yaml` path for `full-reference.md` broken |
| `pytest tests/unit/test_cpp_avatar/ -q` | ✅ 653 tests PASSED, 0 failed |

---

## Panel Verdicts

| # | Persona | Role | Verdict |
|---|---|---|---|
| P1 | Elena Kozlov | C++ Language Expert | ⚠️ CONDITIONAL PASS |
| P2 | Marcus Webb | Constitution Governance Steward | 🔴 BLOCKED |
| P3 | Priya Ramanathan | Legacy Rescue / Brownfield Specialist | ✅ PASS |
| P4 | Dmitri Volkov | Platform Engineering Lead | ⚠️ CONDITIONAL PASS |
| P5 | Aisling O'Brien | Safety-Critical Systems Engineer | ⚠️ CONDITIONAL PASS |
| P6 | Kenji Nakamura | RAG / AI Agent Architect | 🔴 BLOCKED |
| P7 | Sofia Andrade | Developer Experience Engineer | ✅ PASS |

**Overall panel verdict: 🔴 BLOCKED — 2 blocking issues must be resolved before merge**

---

## P1 · Elena Kozlov — C++ Language Expert

> *ISO C++ committee contributor, practitioner with 15 years spanning C++98 to C++23, author of compiler porting guides for embedded and aviation stacks.*

### Positive Findings 🟢

- **Multi-tier standard coverage** — The five standard tiers (C++98/03 → C++23) with explicit tier-lock and `legacy_frozen` designations are among the most rigorously defined I have seen in any agent avatar. The compliance rating multipliers (1.00 → 0.85) appropriately penalise older standards without making them untenable.
- **ENG-4.1 example quality** — `ENG-4.1-atomic-tdd.md` includes the `ccache` tip and `--gtest_filter` workflow, which separate practitioner material from tutorial-level content. This is correct.
- **Code-smell catalog depth** — `ENG-3.1-code-smell-raii-conversion.md` covers 14 distinct smells. The decision tree from symptom → pattern → example file is the right level of specificity for a language expert consulting this avatar.
- **ENG-6.1 breadth** — 16 security example files covering smart pointer migration, move semantics, strict aliasing, void* migration, volatile-vs-atomic, thread safety, and C API wrappers collectively represent a complete ownership-first curriculum. No C++ avatar reviewed to date has matched this depth.

### Warning Findings 🟡

- **ENG-6.1 canonical routing is fragmented** — `manifest.yaml` points `example_file` to `ENG-6.1-security-by-design.md`, but 15 additional ENG-6.1 files exist with no manifest-level routing path. An agent receiving a memory safety query will only see one of 16 relevant files unless the RAG index explicitly routes by topic. Recommend an ENG-6.1 index file or section-level RAG entries.
- **ENG-5.2 dual-file conflict** — Two files cover ENG-5.2 (`ENG-5.2-cmake-governance.md` and `ENG-5.2-cmake-mixed-standard.md`). The manifest routes only to `cmake-governance.md`. A C++ developer on a multi-standard project (CWR is exactly this case) will miss the mixed-standard file entirely. The manifest entry should either point to both or specify when each is appropriate.
- **`ENG-4.4-test-structure.md` exists but ENG-4.4 is not in `specializes_laws`** — The file covers Google Test layout patterns. The law it implements is referenced in the file but not registered in the manifest. An agent will not route to it even on a "how should I structure my tests?" query. Either add ENG-4.4 to `specializes_laws` with this as `example_file`, or merge its content into `ENG-4.2-test-pyramid.md`.

### Blocking Findings 🔴

- None from this persona.

**P1 Verdict: ⚠️ CONDITIONAL PASS** — Address ENG-6.1 routing fragmentation and ENG-5.2 dual-file conflict before merge.

---

## P2 · Marcus Webb — Constitution Governance Steward

> *Maintains the Hangar AI Constitution, reviews every avatar PR against the schema, runs the `aa-constitution-lint` gate on every commit.*

### Positive Findings 🟢

- **Amendment O corrected all 8 constitutional violations** — Prior versions incorrectly included BUS-* and PRD-* laws in a technology-type avatar. Amendment O's removal of those and reconstruction of `guidance.md` around the correct 450-token law table was the right remediation. Law boundary is now clean.
- **653 tests all passing** — The 35-file test suite with 653 assertions is the most comprehensive avatar test suite in the repository. This is the governance standard other avatars should aspire to.
- **16 `specializes_laws` entries** — Breadth is appropriate for a technology avatar of this complexity; none of the 16 laws are out of boundary for a technology-type avatar.

### Warning Findings 🟡

- **`guidance.md` relative path will break after Phase 17** — The guidance file links to `../../../docs/guides/avatars/cpp/full-reference.md`. After the Phase 17 relocation to `avatars/technology/cpp/full-reference.md`, this relative path must be updated to `full-reference.md` (same directory). Failure to update this alongside the file move will cause broken links in every agent interaction that reaches the guidance footer.
- **4 `specializes_laws` entries missing `example_file`** — ENG-3.7 (Error Handling), ENG-5.5 (Observability), ENG-7.1 (Failure Handling), and ENG-5.2 (see P1 dual-file note). Per avatar schema, every `specializes_laws` entry should have an `example_file` pointer or a documented exception reason. Missing pointers degrade routing quality.
- **ENG-7.2–7.5 examples exist but laws not in `specializes_laws`** — Four resiliency pattern files (`circuit-breaker`, `retry-backoff`, `timeout-governance`, `bulkhead-isolation`) are in the `examples/` directory but their laws have no manifest entry. These examples are unreachable via the routing pipeline unless added to `specializes_laws`.

### Blocking Findings 🔴

- **🔴 BLOCKING: Linter failure — Phase 17 not executed** — The constitutional linter reports: `AVATAR-RAG-INDEX.yaml: avatars/technology/cpp/docs/guides/avatars/cpp/full-reference.md does not exist`. The file physically resides at `docs/guides/avatars/cpp/full-reference.md` but the RAG index path is constructed as `{avatar_registry_path}/{index_path}`, producing a doubled path. Phase 17 (Amendment P) resolves this by relocating the file inside the avatar directory. **This is a hard gate. The PR cannot pass `aa-constitution-lint` in its current state.**

**P2 Verdict: 🔴 BLOCKED** — Phase 17 (Amendment P relocation) is a linter-gate blocker. Must be executed before merge.

---

## P3 · Priya Ramanathan — Legacy Rescue / Brownfield Specialist

> *Led the assessment and incremental remediation of three C++98 airline operations codebases, including one with a Java/JNI boundary layer. Specialises in making legacy systems testable without full rewrites.*

### Positive Findings 🟢

- **`legacy_frozen` tier is production-ready** — The explicit `legacy_frozen` designation for C++98/03 with compile-mode compatibility, brownfield-exception flags, and characterization-first test policy is exactly what a team inheriting a C++03 codebase needs. Most avatars pretend legacy code doesn't exist.
- **Characterization test pattern is exemplary** — `ENG-4.1-characterization-test-pattern.md` implements the Michael Feathers method correctly. The seam identification table (virtual dispatch seam, link seam, preprocessor seam) maps directly to CWR's constraint solver architecture.
- **`skill-cpp-legacy-modernization` priority list** — The 8-step prioritised modernization table (NULL→nullptr, override, unique_ptr, constexpr, casts, range-for, auto, const-correctness) is correctly ordered by risk and impact. The "Do Not Touch" rules are essential guard rails for incremental adoption.
- **`skill-cpp-standard-migration`** — Presence of an explicit standard migration skill with compliance-rating tier multipliers allows a team to track and score their migration progress over time.

### Warning Findings 🟡

- **No JNI / inter-language boundary guidance** — CWR contains a C++/Java JNI bridge layer. The avatar has deep C++ coverage but no guidance on the C++ side of JNI boundaries (ownership transfer across the JNI, jobject lifetime management, JVM thread attachment). This is a specific gap for the primary CWR target project.
- **No guidance on mixing standards in a single compilation unit** — CWR's transition path will require C++03 and C++11 translation units to coexist in the same link. The avatar covers each tier in isolation but not the ABI/linkage rules governing their mixing. `ENG-5.2-cmake-mixed-standard.md` exists but is not routed by the manifest (P1 finding).
- **D10 (Regulatory Compliance) in compliance rating lacks FAR 117 test traceability** — The skill correctly identifies FAR 117 as a regulatory domain for C++ aviation projects, but it does not specify how traceability matrices should be implemented in a C++ test harness. For CWR, every constraint function needs a traceable test. An example tracing GoogleTest names to FAR 117 regulation numbers would close this gap.

### Blocking Findings 🔴

- None from this persona.

**P3 Verdict: ✅ PASS** — Avatar is brownfield-ready. Three advisory improvements would increase CWR-specific value.

---

## P4 · Dmitri Volkov — Platform Engineering Lead

> *Owns 40 C++ services across a large aviation platform. Governs the agent-skill registry. Reviews every new skill for coherence, redundancy, and coverage gaps before it enters the skill index.*

### Positive Findings 🟢

- **25 new skills is the broadest domain skill set in the registry** — The skills span TDD, security, legacy, CI/CD, compliance rating, resiliency, observability, and standard migration. Coverage is genuinely comprehensive.
- **`skill-cpp-compliance-rating` 10-dimension scoring model** — D1–D10 with veto thresholds and a standard-tier multiplier gives platform leads an objective, reproducible measure. The scoring procedure is detailed enough to be implemented as a CI gate.
- **`followed_by` chains are populated** — Skills correctly chain to related skills (e.g., `skill-cpp-legacy-modernization` → `skill-cpp-standard-migration` → `skill-27-constitution-compliance`). This enables progressive disclosure in agent interactions.

### Warning Findings 🟡

- **No `skill-cpp-jni-bridge` or inter-language skill** — This mirrors P3's finding from a platform perspective. The CWR project is the primary consumer of this avatar and has a C++/Java boundary. A platform lead would require a skill file before approving the PR as CWR-complete.
- **Skill naming inconsistency** — Some skills use domain-action form (`skill-cpp-sanitizer-hardening`), others use domain-concept form (`skill-cpp-ownership-lifetime-safety`), others use domain-output form (`skill-cpp-compliance-rating`). A naming convention in the skill index header would prevent drift across future additions.
- **Skill index registration needs verification** — PROGRESS.md lists 25 new C++ skills added in Phase 16 but I was unable to confirm all 25 appear in `agent-skills/skill-index.yaml` within this review. Any unregistered skill is unreachable by the routing pipeline. This must be verified as part of Phase 17 completion checks.

### Blocking Findings 🔴

- None from this persona.

**P4 Verdict: ⚠️ CONDITIONAL PASS** — Verify skill index registration for all 25 skills. JNI gap is advisory.

---

## P5 · Aisling O'Brien — Safety-Critical Systems Engineer

> *Certified MISRA C++ reviewer, DO-178C process engineer at a major avionics integrator. Reviews safety-critical C++ governance for ground-based and airborne systems.*

### Positive Findings 🟢

- **DO-278A and MISRA C++ references are present** — The avatar acknowledges ground-based CNS/ATM safety standards, which is the applicable standard for CWR as a ground-based crew management system. Most C++ avatars default to DO-178C (airborne) and miss DO-278A entirely.
- **ASan/UBSan mandatory in CI** — Undefined behaviour sanitizer as a non-negotiable CI gate is the correct minimum bar for safety-critical C++ development. The compliance rating D2/D6 veto thresholds (score ≥4) enforce this correctly.
- **`ENG-6.1-thread-safety.md` and `ENG-6.1-volatile-vs-atomic.md`** — These two examples cover the most common concurrency safety failures in safety-critical C++. Their presence demonstrates domain awareness beyond typical web-application avatars.

### Warning Findings 🟡

- **MISRA/DO-178C guidance is buried in `full-reference.md`** — An agent routing a safety-critical query through `guidance.md` sees only the seven laws table and the `full-reference.md` link. The safety-critical section of `full-reference.md` (MISRA, DO-178C patterns, deviations, rationales) is not surfaced at the 450-token routing layer. A safety auditor relying on this avatar will miss safety-critical constraints unless they explicitly navigate to `full-reference.md`.
- **No dedicated MISRA C++ example file** — The avatar has 44 example files with deep ENG-6.1 coverage but no `ENG-6.x-misra-compliance.md` file. MISRA compliance requires deviation records, approved-construct lists, and rule-by-rule rationale — none of which are in any current example. This is a significant gap for DO-278A-governed CWR development.
- **DO-278A (ground-based) vs DO-178C (airborne) distinction not explicit** — The avatar does not explicitly state which safety standard applies to crew management systems (CWR) vs cockpit systems. An agent advising on CWR safety posture should always cite DO-278A, not DO-178C. Adding a `cwr_standard: DO-278A` guidance note would prevent misapplication.
- **No `ENG-6.x-sanitizer-integration.md` example** — ASan/UBSan/MSan integration in a CMake project, including CI suppression files, is complex enough to warrant a dedicated example. The compliance rating references it but no step-by-step example exists.

### Blocking Findings 🔴

- None from this persona.

**P5 Verdict: ⚠️ CONDITIONAL PASS** — MISRA/DO-278A coverage is thin for a safety-critical C++ avatar. Not blocking merge but a Phase 18 safety-critical examples sprint is strongly recommended.

---

## P6 · Kenji Nakamura — RAG / AI Agent Architect

> *Designed the RAG routing pipeline for the Hangar AI platform. Responsible for token budgets, canonical query definitions, and AVATAR-RAG-INDEX.yaml schema governance.*

### Positive Findings 🟢

- **`guidance.md` at ~450 tokens is correctly sized as the routing layer** — The two-file architecture (guidance.md as 450-token entry point + full-reference.md as extended reference) is the correct design pattern for large technology avatars. Other technology avatars should adopt this pattern.
- **RAG index includes `full_reference` annotation** — The `AVATAR-RAG-INDEX.yaml` entry documents `full-reference.md` as an on-demand extended reference, distinguishing it from canonical routing files. This is good metadata practice.

### Warning Findings 🟡

- **No 5 canonical RAG query definitions for `cpp`** — The `crew-recovery-solver` avatar defines 5 explicit canonical queries in the RAG index with expected response token estimates. The `cpp` avatar entry has no equivalent. Without canonical query definitions, routing coverage cannot be validated mechanically. This is a gap relative to the current AVATAR-RAG-INDEX.yaml standard.

### Blocking Findings 🔴

- **🔴 BLOCKING: `full-reference.md` is 5,519 lines (~20,000+ tokens) with no chunking strategy** — The RAG index references `full-reference.md` as a single document. Any routing query that resolves to this file will return a response far exceeding the 3,500-token RAG context ceiling (same ceiling enforced for `crew-recovery-solver` canonical queries). Loading the full document will overflow any agent context window. This document must either: (a) be split into section-level files with individual RAG index entries, OR (b) remain as a local navigational reference with explicit routing disabled in the RAG index (flagged as `on_demand_only: true`). As currently configured, the RAG index creates an implicit promise that `full-reference.md` can be served as a query result — it cannot at this token volume.

- **🔴 BLOCKING (same root cause as P2): Linter failure** — The broken path in `AVATAR-RAG-INDEX.yaml` is confirmed from the routing architecture perspective. Phase 17 relocation is the correct fix; the RAG index path must be updated in the same commit as the file move.

**P6 Verdict: 🔴 BLOCKED** — Two blockers: (1) `full-reference.md` token overflow risk in RAG pipeline; (2) broken RAG index path. Both require resolution before the routing pipeline can reliably serve this avatar.

---

## P7 · Sofia Andrade — Developer Experience Engineer

> *Specialises in first-hour and first-week developer experience. Has onboarded 200+ engineers to C++ projects. Reviews avatars and skills from the perspective of an intermediate developer encountering C++ governance for the first time.*

### Positive Findings 🟢

- **Mental Model Transitions section is outstanding** — The 8 common C++ mental model gaps (null safety, ownership vs garbage collection, RAII vs try/finally, header files, move semantics, ODR, ADL, undefined behaviour) are exactly the concepts that trip up developers coming from Java, Python, or Go. This section has high signal and low noise.
- **Quick-Start Cheat Sheet** — Presence of a cheat sheet in `full-reference.md` demonstrates intentional progressive disclosure design. Most technology avatars require a developer to read the full spec before finding practical guidance.
- **Code smell → pattern → example file linkage** — The catalog structure (symptom → diagnosis → example file reference) allows an intermediate developer to self-navigate without requiring avatar expertise. This is good information architecture.
- **25 skills with `triggers.phrases`** — The natural language trigger lists mean an intermediate developer does not need to know the avatar schema to activate the right skill. Phrase-based routing is a significant DX improvement.

### Warning Findings 🟡

- **No brownfield quick-start path** — The quick-start guide targets greenfield C++20+ projects. A developer joining CWR (a C++03 codebase in mid-migration) will encounter guidance that does not apply to their tier until they discover the `legacy_frozen` section deep in `full-reference.md`. A "Brownfield Entry Path" section at the top of `full-reference.md` (or a dedicated `quick-start-legacy.md`) would prevent false starts.
- **No "which skill do I use?" decision tree for the 25 new skills** — 25 skills is powerful but creates a choice problem. An intermediate developer who knows they want to "improve code quality" cannot easily determine whether to invoke `skill-cpp-legacy-modernization`, `skill-cpp-compliance-rating`, `skill-cpp-sanitizer-hardening`, or `skill-cpp-ownership-lifetime-safety`. A one-page decision tree (problem statement → skill name) would reduce this friction significantly.
- **`full-reference.md` is not section-navigable from `guidance.md`** — The `guidance.md` footer link points to the full document with no section anchor. A developer clicking this link lands at the top of a 5,519-line file. Section-level anchor links from `guidance.md` (e.g., `full-reference.md#brownfield-migration`) would improve first-hour navigation.

### Blocking Findings 🔴

- None from this persona.

**P7 Verdict: ✅ PASS** — Avatar has strong DX foundations. Three advisory improvements would particularly benefit the CWR brownfield entry scenario.

---

## Consolidated Findings

### Blocking Issues (must resolve before merge)

| # | Issue | Owner | Resolution |
|---|---|---|---|
| B-1 | Linter failure — `full-reference.md` path broken in `AVATAR-RAG-INDEX.yaml` | Phase 17 (Amendment P) | Execute: `git mv docs/guides/avatars/cpp/full-reference.md avatars/technology/cpp/full-reference.md`, update RAG index path, update `guidance.md` relative link |
| B-2 | `full-reference.md` at 5,519 lines in RAG index with no token budget or chunking strategy — RAG context overflow risk | Phase 17 extension | Add `on_demand_only: true` flag to RAG index entry OR split into section-level files with individual index entries. At minimum, document the size constraint in the RAG index entry. |

### High-Priority Improvements (Phase 18 recommended)

| # | Finding | Personas | Action |
|---|---|---|---|
| H-1 | ENG-3.7, ENG-5.5, ENG-7.1 missing `example_file` in `specializes_laws` | P1, P2 | Create `ENG-3.7-error-handling.md`, `ENG-5.5-observability.md`, `ENG-7.1-failure-handling.md` examples, add `example_file` pointers |
| H-2 | ENG-4.4, ENG-7.2–7.5, ENG-5.2 (second file) unreachable from manifest routing | P1, P2 | Add ENG-4.4, ENG-7.2–7.5 to `specializes_laws`; add second `example_file` entry for ENG-5.2 (mixed-standard use case) |
| H-3 | ENG-6.1 routing — 16 files, only 1 in manifest | P1, P4 | Create `examples/ENG-6.1-index.md` as a topic router, or add section-level RAG entries for each ENG-6.1 file |
| H-4 | MISRA C++ and DO-278A guidance absent from routing layer | P5 | Add a MISRA/DO-278A example file; reference it in `specializes_laws` (ENG-6.1 or new ENG-6.x entry) |
| H-5 | `guidance.md` relative path will break at Phase 17 file move | P2 | Update `guidance.md` link from `../../../docs/guides/avatars/cpp/full-reference.md` to `full-reference.md` in same commit as file move |

### Advisory Improvements (Phase 18+)

| # | Finding | Personas | Action |
|---|---|---|---|
| A-1 | No JNI / C++–Java inter-language boundary guidance | P3, P4 | Add `skill-cpp-jni-bridge.md` for CWR's JNI layer |
| A-2 | Compliance rating D10 lacks FAR 117 GoogleTest traceability example | P3, P5 | Add traceability matrix example linking test names to FAR 117 regulation numbers |
| A-3 | No brownfield quick-start path | P7 | Add "Brownfield Entry Path" section to `full-reference.md` before existing Quick-Start Cheat Sheet |
| A-4 | No "which skill do I use?" decision tree | P7 | Add skill decision tree to `full-reference.md` and/or skill index header |
| A-5 | `full-reference.md` lacks section anchors from `guidance.md` links | P7 | Add named anchor links in `guidance.md` footer pointing to key sections of `full-reference.md` |
| A-6 | Skill naming convention not standardised | P4 | Document naming convention in skill index header; apply retroactively in Phase 18 |
| A-7 | Skill index registration for all 25 new skills needs confirmation | P4 | Audit `agent-skills/skill-index.yaml` to verify all 25 Phase 16 skills are registered |
| A-8 | `ENG-6.7` references ENG-6.7 in `skill-cpp-compliance-rating` D5 — should reference BUS-7.1 for audit trail | P2 | Update compliance rating skill to cite BUS-7.1 (the NON-NEGOTIABLE law) alongside ENG-6.7 (implementation guidance) |

---

## Phase 17 Execution Checklist

The following steps are required to clear all blocking findings. This checklist extends PROGRESS.md Phase 17 steps 17.0–17.8.

```
[ ] 17.0  Create pre-move test checkpoint: run 653 tests, record baseline
[ ] 17.1  git mv docs/guides/avatars/cpp/full-reference.md avatars/technology/cpp/full-reference.md
[ ] 17.2  Update guidance.md: change link from ../../../docs/guides/avatars/cpp/full-reference.md
                              to full-reference.md (same directory)
[ ] 17.3  Update AVATAR-RAG-INDEX.yaml cpp entry:
           full_reference path: docs/guides/avatars/cpp/full-reference.md
                          →  full_reference.md
          Add: on_demand_only: true  (B-2 mitigation)
          Add: note: "5519 lines — not suitable for direct RAG retrieval; route by section"
[ ] 17.4  Run aa-constitution-lint: expect 0 failures
[ ] 17.5  Run pytest: expect ≥653 tests pass (some fixture paths may need update)
[ ] 17.6  Push 4 unpushed commits + new Phase 17 commit
[ ] 17.7  Request PR review
[ ] 17.8  Update PROGRESS.md Phase 17 steps as complete
```

---

## Summary

The C++ avatar enrichment is the most technically comprehensive technology avatar in the repository. 17 amendment cycles and 276 tasks have produced a genuinely production-quality result — the 653 passing tests demonstrate constitutional seriousness that other avatars should emulate.

**Two issues block merge.** Both trace to the same root cause: Phase 17 (Amendment P) has not been executed. The `full-reference.md` file has not been relocated into the avatar directory, leaving the RAG index with a broken path. Fixing this requires approximately four targeted edits and one `git mv`. Once Phase 17 is complete, the linter will pass and the RAG index will correctly reference the co-located file.

**The most important post-merge work is MISRA/DO-278A coverage** (H-4). For the CWR use case, the absence of MISRA example files and DO-278A-specific guidance means safety-critical C++ engineers will not find the guidance they need through this avatar. A focused Phase 18 safety-critical sprint is recommended.

---

*Panel review conducted per `workflows/avatar-workflow.md` Mode 5 + Mode 2. Review artefact committed to branch as governance evidence.*

---

## Appendix A — Prompt Used to Generate This Review

The following is the refined prompt that produced this panel review. It was developed interactively from the user's original request ("Create 7 relevant personas to review the c-plus-plus-avatar-enrichment-proposal...") through a clarification pass, then executed with instruction to "take your time and be thorough."

---

```
Conduct a thorough 7-persona panel review of the branch
`feature/c-plus-plus-avatar-enrichment-proposal`.

SCOPE
Review all layers of the C++ avatar:
  - avatars/technology/cpp/manifest.yaml
  - avatars/technology/cpp/guidance.md
  - avatars/technology/cpp/examples/ (all 44 files)
  - docs/guides/avatars/cpp/full-reference.md
  - agent-skills/ — all 25 new C++ skills added in Phase 16
  - avatars/AVATAR-RAG-INDEX.yaml — cpp entry
  - hangar-ai-specs/changes/c-plus-plus-avatar-enrichment/PROGRESS.md
  - hangar-ai-specs/changes/c-plus-plus-avatar-enrichment/PROPOSAL.md

CONSTITUTION GUIDANCE
Before selecting personas or writing findings:
  1. Read workflows/avatar-workflow.md — apply Mode 5 (PR Review) and
     Mode 2 (Assess & Correct) guidance.
  2. Read laws/engineering/eng-2 through eng-7 for law boundary compliance.
  3. Cross-reference PROPOSAL.md stated intent against actual implementation.
  4. Run aa-constitution-lint and pytest as automated gates; record results
     at the top of the review.

PERSONAS
Select 7 personas whose expertise collectively covers all of the following
domains. Give each a name, role title, and 2-sentence practitioner background.

  1. C++ technical correctness — ISO C++ standards, multi-tier coverage
     (C++98 through C++23), code example quality
  2. Constitution governance — schema conformance, law boundary, non-negotiable
     law coverage, specializes_laws completeness
  3. Legacy / brownfield C++ — C++98/03 codebase migration, characterization
     tests, CWR relevance (the primary consumer project is C++03)
  4. Platform engineering — 25 new C++ skills, skill index coherence, coverage
     gaps, redundancy, followed_by chains
  5. Safety-critical systems — MISRA C++, DO-178C / DO-278A, aviation-domain
     safety patterns for C++
  6. RAG / AI agent architecture — token budgets, routing efficiency,
     full-reference.md architecture, AVATAR-RAG-INDEX.yaml conformance
  7. Developer experience — onboarding, progressive disclosure, mental model
     transitions, brownfield entry path

PER-PERSONA OUTPUT
For each persona, produce:
  - A brief statement of their review scope / lens
  - Findings tagged 🟢 (positive), 🟡 (warning), 🔴 (blocking)
  - A per-persona verdict: ✅ PASS | ⚠️ CONDITIONAL PASS | 🔴 BLOCKED

SYNTHESIS
Combine all findings into:
  - Overall panel verdict with clear rationale
  - Blocking issues table (must resolve before merge)
  - High-priority improvements table (Phase 18 recommended)
  - Advisory improvements table (future phases)
  - Phase 17 execution checklist if Phase 17 is identified as blocking

OUTPUT
Commit the completed review to:
  hangar-ai-specs/changes/c-plus-plus-avatar-enrichment/review/panel-review.md

Take as long as needed. Be thorough. Do not collapse personas or skip findings
to save space. This review is governance evidence and must be traceable.
```

---

*Original user request (pre-refinement):*
> "Create 7 relevant personas to review the c-plus-plus-avatar-enrichment-proposal.
> As part of this scan the constitution and the constitution-workflows for any guidance.
> If there is a workflow for creating Avatars, then consider how that should impact
> the results. Take the opinions from these personas and combine them into a list of
> recommendations. Do a thorough analysis and take as long as is needed for completion."
