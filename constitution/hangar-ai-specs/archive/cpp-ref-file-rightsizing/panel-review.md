# Multi-Persona Panel Review: cpp-ref-file-rightsizing PROPOSAL.md

**Panel convened:** April 25, 2026  
**Proposal reviewed:** `hangar-ai-specs/changes/cpp-ref-file-rightsizing/PROPOSAL.md` + `tasks.md`  
**Branch:** `analysis/cpp-version-sensitivity` @ `7179d10`  
**Prompt:** See [review-prompt.md](review-prompt.md)

---

## PANEL ROSTER

### Assigned Personas (Domains 1–8)

**Persona 1 — Dr. Anjali Mehta**  
*Principal C++ Language Engineer, ISO C++ Working Group observer*  
Anjali has spent 18 years working on standards-conforming C++ for embedded and systems software, including reviewing ISO committee papers for C++17/20/23. She specializes in how language evolution changes idioms — const-correctness in C++03 vs. structured bindings in C++17, SFINAE vs. concepts — and has strong opinions about what "correct" looks like at each standard level.

**Persona 2 — Marcus Webb**  
*Hangar AI Constitution Governance Lead*  
Marcus spent a decade at a large airline as a principal architect before transitioning to AI governance. He wrote the internal governance checklist for ENG-11.1/11.2 proposals and has rejected three proposals for incomplete law citation or missing success criteria. His lens: does the proposal document say what it needs to say, are the law links traceable, are success criteria measurable and complete?

**Persona 3 — Dmitri Volkov**  
*Senior Staff Engineer — C++98 Legacy Systems / CWR Project*  
Dmitri has maintained C++98/03 codebases professionally since 2001, including the CWR (Crew Watch Replacement) solver that is the primary consumer of this avatar. He knows exactly what happens when AI advice that assumes C++14+ idioms is applied to C++03 codebases: it introduces undefined behavior, compilation errors, or link-time failures that take days to diagnose. He cares deeply about characterization tests and brownfield migration safety.

**Persona 4 — Elena Nakamura**  
*Platform Engineering Lead — AI Agent Skills Platform*  
Elena owns the skills infrastructure: the `agent-skills/` directory, skill index files, `followed_by` chain design, and skill coverage gap analysis. She reviews proposals for completeness of skill routing, redundant skill paths, and whether the platform correctly activates the right skill for a given intent.

**Persona 5 — Col. James Okonkwo (ret.)**  
*DO-178C / MISRA C++ Safety Systems Consultant*  
James spent 22 years as a safety systems engineer for avionics software, with direct experience on DO-178C Level A certification audits and MISRA C++ 2023 rule set analysis. He reviews proposals involving safety-critical content for traceability, completeness, and whether safety rules are correctly attributed to the right C++ standards levels.

**Persona 6 — Dr. Priya Sundaram**  
*AI Agent Architecture & RAG Systems Researcher*  
Priya studies retrieval-augmented generation at the intersection of token budget constraints, routing precision, and context window optimization. She has published on RAG precision degradation from oversized document chunks and is a harsh critic of token count estimates that lack empirical grounding.

**Persona 7 — Sofia Chen**  
*Developer Experience Lead — C++ Onboarding*  
Sofia designs onboarding experiences for engineers joining C++ codebases from Java/Python backgrounds, specifically in large aviation enterprises where C++ expertise is declining. She cares about progressive disclosure, navigation coherence, file naming that surfaces intent, and whether split files feel like coherent standalone documents or orphaned fragments.

**Persona 8 — Dr. Thomas Hart**  
*Testing Correctness Lead — AI-Assisted Code Review*  
Thomas specializes in validating that AI-generated C++ code examples and guidance are version-correct — i.e., that advice presented for C++03 doesn't silently assume C++11 features, that C++20 examples compile cleanly under GCC 12 without deprecated constructs. His role is ensuring the constitution's advice actually works for the version it claims to target.

**Persona 9 — Rachel Torres**  
*Cross-Avatar Impact & Constitutional Compliance Auditor*  
Rachel reviews proposals that touch files outside their primary avatar directory. She specializes in blast-radius analysis — mapping all downstream files, tests, lint rules, and indexes affected by a structural change. She caught the `AVATAR-RAG-INDEX.yaml` issue in the `cpp-split-reference-architecture` proposal and confirmed it was a constitution-lint hard gate.

### Copilot-Selected Additional Personas

**Persona 10 — Owen Bradley**  
*Test Automation Engineering Lead — Constitution TDD Compliance*  
Owen reviews whether the TDD tasks in a proposal actually implement the ENG-4.1 Atomic TDD Law correctly — not just whether tests exist, but whether the RED step is atomic, the GREEN step is minimal, and the test assertions provide genuine quality gates rather than superficial file-existence checks. He catches "theater TDD" where tests technically exist but provide no real signal.

**Persona 11 — Dr. Yuki Tanaka**  
*Information Architecture & Technical Writing*  
Yuki reviews file naming conventions, navigational coherence, and whether split documents function as coherent standalone reference artifacts. She applies the test: "if I receive only this one file with no other context, does its name and content tell me what I need to know?" She is particularly sensitive to naming that encodes opaque sequencing (`-a`, `-b` suffixes) rather than semantic intent.

**Persona 12 — Patricia Osei**  
*Change Management & Organizational Risk*  
Patricia evaluates change proposals for migration risk, rollback readiness, blast radius on production systems, and whether the risk register is realistic or optimistic. She has specific experience with large-scale file restructuring in repositories where other teams may have external links or scripts pointing to the old file paths.

---

## PER-PERSONA REVIEWS

---

### Persona 1 — Dr. Anjali Mehta | C++ Technical Correctness

**Scope:** Verify that the proposed file split plan preserves technical correctness of content grouping. Assess whether version-natural split boundaries are correctly identified and whether split names accurately reflect ISO C++ standard coverage.

**Findings:**

🟢 **Version boundary identification for ★ splits is technically sound.** The four ★ splits align correctly with actual ISO language evolution: `std::thread`/`std::mutex` are C++11 (not C++17/20), coroutines are C++20, `std::variant` is C++17, `co_await` is C++20, `std::stop_token` is C++20. These boundaries are technically defensible.

🟢 **`ref-templates-metaprogramming.md` vs `ref-advanced-patterns.md` split captures a real semantic boundary** — the template/concept/ADL half vs. the lambda/allocator/preprocessor half. These are genuinely different skills and a developer asking about SFINAE doesn't necessarily need to read about PMR allocators.

🟡 **`ref-concurrency-threading.md` at 1,858 tokens is suspiciously small for a file describing thread safety.** If `std::thread`, `std::mutex`, `std::atomic`, and `std::lock_guard` all live in this file, that's 4 major facility families in ~7,400 characters. Either the content is thin (incomplete coverage) or the token estimate is incorrect. This should be re-measured at Phase 1 pre-flight, not assumed.

🟡 **`ref-core-type-safety.md` boundary claim "all versions" is technically imprecise.** The `const` correctness rules differ meaningfully between C++03 (no `constexpr`) and C++11+ (full `constexpr` propagation). Describing this file as "all versions" understates the complexity. The file header should clarify that C++03 and C++11+ `constexpr` semantics are both covered and distinguished.

🔴 **`ref-legacy-orientation.md` at 3,918 tokens exceeds the ≤3,500-token target.** The risk register explicitly states "Content is already measured and within target; no further split required" — this is factually incorrect. 3,918 > 3,500 by 418 tokens (+12%). After the split, `ref-legacy-orientation.md` will still violate the target. The proposal's primary success criterion ("All 31 reference files ≤ 3,500 tokens") will not be met for this file. This is a blocking defect.

**Verdict: 🔴 BLOCKED** — The `ref-legacy-orientation.md` arithmetic error is a hard factual defect. Proposal cannot close its own success criterion as written.

---

### Persona 2 — Marcus Webb | Constitution Governance

**Scope:** Law citations, schema conformance, success criteria measurability, ENG-11.1/11.2 compliance, non-negotiable law coverage.

**Findings:**

🟢 **Law citation table is complete and relevant.** ENG-11.1, ENG-11.2, ENG-10.1, ENG-4.1, ENG-6.7 are correctly cited and the "Relevance" column correctly characterizes each law's applicability. This is well-formed.

🟢 **Success criteria table is measurable and verifiable.** Each criterion has a concrete measurement method. The "Zero content loss" criterion is notable — it's behavioral, not structural. The "token sum ± 100" for total corpus is a reasonable tolerance.

🟢 **Taxonomy Gate (skill-30) table is correctly populated** and all five gate questions are addressed. The "Scope" answer correctly flags the AVATAR-RAG-INDEX.yaml as an out-of-scope co-change.

🟡 **Phase 0 tasks in `tasks.md` are checked-off in the task text itself** (`✓ (done — this change)`) rather than being marked with `[x]`. This is inconsistent with the progress tracking convention used in other proposals in this repository. When automation counts completed tasks, the `[ ]` / `[x]` pattern matters.

🟡 **The proposal cites ENG-6.7 (Audit Trail Law) as relevant because "index files are audit records."** This is a stretch — ENG-6.7 primarily governs logging and traceability in production code, not file index maintenance. The more applicable law for index integrity is ENG-10.1 (Constitution Compliance) which is already cited. The ENG-6.7 citation is harmless but potentially misleading in a future audit.

🟡 **`PROGRESS.md` update is listed as task 18.3 but there is no mention of updating `reference-index.md`'s claim** that "each file is sized to fit within a single RAG query window (≤3,500 tokens)" — that claim is currently false and the proposal should explicitly address correcting it as part of D30.

🟢 **Archival instructions are present and follow the established pattern** from other proposals. The `mv` command is syntactically correct.

**Verdict: ✅ PASS** — The governance documentation is well-formed. The findings are improvements, not blockers.

---

### Persona 3 — Dmitri Volkov | Legacy/Brownfield C++ (CWR)

**Scope:** How does this split affect the primary consumer of the brownfield C++ guidance? CWR is a C++03 codebase — does the post-split file structure make it harder or easier to get C++03-appropriate advice?

**Findings:**

🟢 **`ref-migration-pre-cpp17.md` is a highly beneficial split for CWR.** The pre-C++17 migration content (C++98→11, C++11→14, C++14→17) is precisely what a CWR engineer needs. Splitting it away from the C++17→20 content means a CWR engineer's query budget is not consumed by C++20 guidance that is inapplicable to their context.

🟢 **`ref-brownfield-migration.md` and `ref-brownfield-project-config.md` split makes sense** — migration strategies and per-project configuration are two distinct concerns. A CWR engineer writing new tests doesn't need to load all the project configuration content for IOC_ALP.

🔴 **The proposed split of `ref-legacy-navigation.md` is structurally unsound for the CWR use case.** The split creates `ref-legacy-priorities.md` at only 312 tokens. This file is so small it cannot function as a meaningful standalone reference document for a CWR engineer trying to understand survival patterns. More critically, the main body (`ref-legacy-orientation.md`) at 3,918 tokens still exceeds the target. The split does not improve retrievability for the CWR consumer at all — it creates a micro-fragment and leaves the main body over budget.

🟡 **`ref-brownfield-config.md` split names are confusing.** `ref-brownfield-migration.md` vs. `ref-migration-playbooks.md` will create a naming collision problem — both files have "migration" in the name but cover different things. A developer searching for migration guidance will not know from the name alone which file to load. Consider `ref-brownfield-tier-configs.md` for the per-tier configuration half.

🟡 **No explicit tracking of which files are "CWR-primary" in the post-split `reference-index.md`.** The CWR project is explicitly called out in the manifest as the primary brownfield consumer. The reference index should provide a CWR-specific entry path or annotation so that CWR engineers don't have to know the full file taxonomy.

**Verdict: ⚠️ CONDITIONAL PASS** — The `ref-legacy-navigation.md` split issue is the same blocking defect found by Persona 1. Other findings are improvements. The naming collision concern is a high-priority fix before implementation.

---

### Persona 4 — Elena Nakamura | Platform Engineering

**Scope:** Skill index coherence, skill routing, coverage gaps, and whether the split creates any skill-to-reference routing breakage.

**Findings:**

🟢 **Skills reference the cpp avatar directory, not individual ref files.** As confirmed in the cross-avatar impact analysis, skill files activate the avatar as a whole. No skill files will require updates from this split.

🟢 **The `search_queries` entries in AVATAR-RAG-INDEX.yaml that route to reference files are correctly identified as requiring updates.** The proposal calls this out explicitly.

🟡 **Phase 16 tasks (3 subtasks for 40+ routing decisions) are critically underspecified.** The work required to re-point 40+ routing examples is substantial. Each routing example needs a judgment call: "Does this query about concurrency go to `ref-concurrency-threading.md` or `ref-concurrency-async.md`?" For the 4 ★ version-split files, this routing decision is the entire value of the split — getting it wrong negates the version-routing benefit. Task 16.2 should be decomposed into per-★-file routing decision tasks with explicit routing decision rationale documented.

🟡 **AVATAR-RAG-INDEX.yaml has pre-existing stale token counts.** The YAML currently lists `ref-testing-ci.md (~4499t)` but the actual measured value is 6,975 tokens. Similarly `ref-object-design.md (~3500t)` vs. actual 5,112. These counts were wrong before this proposal and Phase 16 must correct all of them, not just the split files. This adds scope that isn't acknowledged in the task count.

🟡 **No task to add routing examples for the 15 NEW files.** Phase 16 re-points old examples to new names, but the 15 new files (the outputs of splits) may introduce query patterns that weren't served by the original 14 files. For example, a developer specifically asking about `co_await` exception safety would now benefit from a direct routing entry to `ref-concurrency-async.md`. The proposal should add at least 1–2 routing examples per new file.

**Verdict: ⚠️ CONDITIONAL PASS** — Phase 16 needs task decomposition. Pre-existing count staleness must be acknowledged.

---

### Persona 5 — Col. James Okonkwo | Safety-Critical Systems

**Scope:** DO-178C / DO-278A / MISRA C++ content placement, safety-rule traceability, correctness of safety file splits.

**Findings:**

🟢 **`ref-safety-misra-do178.md` and `ref-safety-memory-lifetime.md` split is technically correct.** MISRA C++ / DO-178C certification rules are categorically distinct from memory lifetime and FFI safety patterns. These belong in separate files from a traceability standpoint — in a certification audit, you trace code to MISRA rules, not to FFI patterns.

🟢 **`ref-safety-far117-cwr.md` correctly places FAR 117 and CWR anti-patterns together.** FAR 117 (crew rest regulations) and the CWR anti-pattern catalog are both aviation-domain operational safety concerns. Their co-location in a single file is semantically correct.

🟡 **`ref-safety-jni-abi.md` at ~1,035 tokens is very small.** A 1,035-token file covering JNI safety and ABI stability is thin for a safety-critical context. In DO-178C Level B/C software, JNI boundary safety is a significant concern (data type marshalling, exception propagation, memory ownership). The proposal should verify that this file actually contains sufficient content for its claimed coverage, or consider merging JNI/ABI content into another safety file.

🟡 **The `ref-safety-aviation.md` split separates JNI/ABI from FAR 117/CWR.** This is technically defensible but creates a potential traceability gap: a DO-278A audit reviewing the CWR solver (which uses JNI) would need both `ref-safety-jni-abi.md` and `ref-safety-far117-cwr.md`. The `reference-index.md` should annotate these two files as a paired set for CWR/DO-278A context.

🟢 **DO-178C and DO-278A are correctly separated across different files.** DO-178C governs airborne software; DO-278A governs ground-based CNS/ATM systems like CWR. Keeping them in distinct sub-sections (which this split preserves) is correct for certification traceability.

**Verdict: ✅ PASS** — Safety content splits are technically sound. Size concerns are advisory.

---

### Persona 6 — Dr. Priya Sundaram | RAG / AI Agent Architecture

**Scope:** Token budget accuracy, retrieval window improvement math, routing efficiency of the post-split corpus, AVATAR-RAG-INDEX.yaml conformance.

**Findings:**

🟢 **The +94% RAG window improvement calculation is correct.** Before: 6,483 usable tokens ÷ 4,760 avg = 1.36 files. After: 6,483 ÷ 2,456 avg = 2.64 files. The arithmetic is verified.

🟢 **The ÷4 character-to-token approximation is appropriately disclosed** as an approximation, and is consistent with GPT-4/Claude tokenization behavior for mixed C++ prose and code.

🔴 **`ref-legacy-orientation.md` at 3,918 tokens violates the stated target.** After the split, 1 of the 31 files still exceeds ≤3,500 tokens. The success criterion "All 31 reference files ≤ 3,500 tokens" will fail. From a RAG architecture standpoint, this file at 3,918 tokens occupies 60% of a post-split 8K retrieval slot, which is materially worse than the 48% average post-split target. This is a blocking defect in the retrieval architecture.

🔴 **`reference-index.md` token count in AVATAR-RAG-INDEX.yaml will be stale after D30 rewrite.** The YAML states `reference-index.md` is `~418` tokens; after the rewrite from 16 to 31 files, the index will be approximately 836 tokens (proportional estimate). The YAML also has a `note: "not counted against per-query 3,500t budget"` for this file. The post-split index token count must be updated and re-verified against this "not counted" policy.

🟡 **The AVATAR-RAG-INDEX.yaml token counts for reference files are systematically wrong** (stale from the original estimates before the split proposal's measurements). The Phase 16 task should explicitly require re-measuring all reference files at the time of YAML update, not just re-pointing names.

🟡 **The "version-routing benefit gained at no extra cost" claim for ★ splits is only valid if the AVATAR-RAG-INDEX.yaml routing examples are updated correctly.** Simply having two files named `ref-concurrency-threading.md` and `ref-concurrency-async.md` provides no version routing benefit unless the routing examples distinguish between them by version context. The value of the ★ splits is entirely realized in Phase 16, not in the file splits themselves.

🟡 **`ref-legacy-priorities.md` at 312 tokens is too small for effective RAG retrieval.** At 312 tokens, loading this file costs ~1,248 characters of retrieval budget for minimal content return. RAG systems typically show diminishing returns below ~500 tokens per chunk. Either this content should be included in the preceding orientation file (if the split creates a target violation anyway) or a different section boundary should be found.

**Verdict: 🔴 BLOCKED** — The `ref-legacy-orientation.md` target violation is a hard blocker. The success criterion cannot be satisfied as written. The Phase 16 scope underestimation is a high-priority concern.

---

### Persona 7 — Sofia Chen | Developer Experience

**Scope:** File naming coherence, progressive disclosure, navigational quality of post-split reference-index.md, onboarding experience for a Java developer arriving at a C++03 codebase.

**Findings:**

🟢 **Most split file names improve discoverability.** `ref-concurrency-threading.md` vs `ref-concurrency-async.md`, `ref-templates-metaprogramming.md` vs `ref-advanced-patterns.md`, `ref-safety-misra-do178.md` vs `ref-safety-memory-lifetime.md` — all of these communicate content at a glance.

🔴 **`ref-object-design-vectors-a.md` and `ref-object-design-vectors-b.md` names are semantically opaque.** "Vectors" appears nowhere in the original `ref-object-design.md` description ("Object rehabilitation patterns, test isolation boundaries"). A developer reading the `reference-index.md` entry for "vectors-a" will have no idea what this file contains. Better names based on the actual split content (e.g., `ref-object-design-rehabilitation.md` and `ref-object-design-isolation.md`) would provide immediate navigational value. This is a blocking UX defect — opaque names in the routing layer degrade RAG routing quality.

🔴 **`ref-legacy-priorities.md` at 312 tokens makes no sense as a standalone file.** A human developer discovering 31 reference files in a directory listing would find a 312-token file confusing and suspect it's a stub or error. At minimum the file needs a clear opening statement explaining why it exists as a standalone artifact. More fundamentally, if the `ref-legacy-navigation.md` split is being revisited (which it should be, given the 3,918-token issue), this pathologically small file should not exist.

🟡 **The post-split `reference-index.md` will have 31 files but no grouping of related pairs.** A developer navigating 31 files needs visual cues that `ref-concurrency-threading.md` and `ref-concurrency-async.md` are a related pair. The rewrite task (D30) should specify a "Related files" annotation or sub-grouping within the existing H2 section structure.

🟡 **No progressive disclosure path for the CWR/brownfield entry.** The current `reference-index.md` has a single "Brownfield & Legacy" section. After the split, that section will have 8+ entries. A "CWR Quick Start" subsection that surfaces the 3–4 most critical files for a CWR engineer would dramatically improve onboarding for the primary consumer.

**Verdict: 🔴 BLOCKED** — `ref-object-design-vectors-a/b.md` naming is a blocking UX defect that would degrade RAG routing quality. The file names propagate into AVATAR-RAG-INDEX.yaml routing examples and human navigation.

---

### Persona 8 — Dr. Thomas Hart | Testing Correctness (Version Accuracy)

**Scope:** Do the reference file split boundaries preserve version-correctness of the content? Does the split introduce any risk of version-inappropriate advice being retrieved for a given C++ version query?

**Findings:**

🟢 **The ★ version-natural splits are the most valuable correctness improvement.** Splitting `ref-concurrency.md` at the C++20 boundary means a query about `std::thread` safety will not have its retrieval window consumed by coroutine content that is inapplicable to C++14. This directly reduces the risk of version-inappropriate advice reaching a C++14 codebase developer.

🟢 **`ref-migration-pre-cpp17.md` and `ref-migration-cpp17-plus.md` correctly scope their version coverage.** A developer at C++03 asking about migration paths needs only `ref-migration-pre-cpp17.md`. The post-split routing will naturally provide this precision.

🟡 **`ref-core-type-safety.md` covers "all versions" including both C++03 `const` and C++20 `consteval`.** This is a deliberate choice but creates a risk: advice labeled "all versions" may present C++11 `constexpr` as if it applies to C++03. The split boundary at C++17/20 for `ref-core-modern-idioms.md` is correct, but the "all versions" file still needs internal version annotations to prevent cross-version confusion.

🟡 **No test in `tasks.md` validates version correctness of split content** — only token count and file existence. A content correctness check (e.g., "does `ref-concurrency-threading.md` contain no `co_await` or `std::stop_token`?") would provide a meaningful quality gate. These are implementable as regex-based negative assertions in the test suite.

🟢 **The proposal correctly identifies that `ref-concurrency-threading.md` covers `std::thread`, `std::mutex`, `std::atomic`, `std::lock_guard`** — all of which are C++11 facilities, not "pre-C++20" per se. The file name and description are accurate for what they cover.

**Verdict: ⚠️ CONDITIONAL PASS** — The split strategy is version-correct but tests should validate content placement, not just token counts and file existence.

---

### Persona 9 — Rachel Torres | Cross-Avatar Impact & Compliance Audit

**Scope:** Complete blast-radius analysis for all files outside `avatars/technology/cpp/`, including test files, lint rules, other proposals, and the AVATAR-RAG-INDEX.yaml.

**Findings:**

🟢 **Cross-avatar impact section is present and identifies the AVATAR-RAG-INDEX.yaml hard dependency.** This is the critical finding from the prior session and the proposal correctly handles it.

🟢 **Constitution-lint `index_integrity` enforcement is correctly characterized as a hard gate.** Making the AVATAR-RAG-INDEX.yaml update a blocking task (task 16.3 runs lint before Phase 17) is the right sequencing.

🟡 **`docs/guides/avatars/split-reference-architecture.md` is not in the impact analysis.** This guide document describes the reference architecture and likely mentions "16 reference files" as the target state. After the split produces 31 files, this guide will be stale. Task 1.5 (search for old file references) should include a search of `docs/` as well as the avatar directory.

🟡 **The test suite files in `tests/unit/test_cpp_avatar/` are not mentioned in the impact analysis.** Based on the prior `cpp-avatar-phase18-remediation` tasks.md, there are existing tests like `test_cpp_avatar/test_phase5_validation.py::TestTokenBudget` and `test_example_eng_4_1.py`. These tests may check for specific file names or counts. If they do, they will fail after the split until updated. The proposal should include a task to audit and update existing test files.

🟡 **The `reference-index.md` heading states "Each file is sized to fit within a single RAG query window (≤3,500 tokens)"** — this claim is currently false (14 of 16 files exceed it). The proposal correctly flags D30 as updating this document, but doesn't explicitly require correcting this false header claim.

🟢 **`avatars/index.yaml` correctly identified as unaffected.** Confirmed — it only holds a path to `technology/cpp/`, not individual file names.

**Verdict: ⚠️ CONDITIONAL PASS** — The guide doc and test suite gaps are significant omissions in the impact analysis.

---

### Persona 10 — Owen Bradley | Test Automation & TDD Compliance

**Scope:** Are the tasks.md TDD cycles ENG-4.1 compliant? Do the test assertions provide genuine quality gates?

**Findings:**

🟢 **Phase 2 correctly separates RED and GREEN steps for each of the three output files.** Tasks 2.1, 2.3, 2.5 are RED; 2.2, 2.4, 2.6 are GREEN. This is genuinely atomic — one test, one file creation.

🔴 **Phases 3–14 collapse RED and GREEN into a single "RED/GREEN:" combined step.** "3.1 RED/GREEN: create `ref-brownfield-migration.md` (~2,996 tokens) ≤3,500 verified" is not atomic TDD. Per ENG-4.1, the RED step (write the test, observe it fail) is a separate observable event from the GREEN step (write the minimum code). The abbreviated format hides this and creates a checkbox that can be marked complete without ever running a failing test. This is "theater TDD" — the form is present but the substance is absent.

🔴 **The test assertions are insufficient for the "zero content loss" success criterion.** Every test in Phases 2–14 asserts only: file exists AND token_count ≤ 3,500. This passes even if the file is empty or contains random text. The proposal's success criterion "Every section from all 14 source files present in exactly one output file" cannot be verified by these tests. The tests should additionally assert: (1) at least N H2 sections exist (matching the source file's section count for that half), and (2) no section from the other half is present.

🟡 **The ±20 token tolerance in per-split VERIFY tasks (e.g., 2.7) is unnecessarily strict.** When splitting a file, shared frontmatter (title, separator lines) legitimately adds 10–30 tokens per output file. A ±50 tolerance per split file would catch genuine content loss while allowing for structural overhead.

🟢 **Phase 17 final verification is comprehensive.** Tasks 17.1–17.6 cover token validation, corpus total, broken links, reference audit, test suite, and lint. The sequencing is correct.

🟡 **Phase 16.3 runs `aa-constitution-lint` as a gating step before Phase 17.** This is correct sequencing — lint should gate Phase 17, not be part of it. However, the lint also needs to be re-run in Phase 17 (17.6) to catch any regressions introduced in Phase 15 (reference-index.md rewrite). Both lint runs are justified.

**Verdict: 🔴 BLOCKED** — Phases 3–14 violate ENG-4.1 Atomic TDD Law. A proposal that mandates ENG-4.1 in its own laws citation cannot have TDD tasks that collapse RED and GREEN into a single step.

---

### Persona 11 — Dr. Yuki Tanaka | Information Architecture

**Scope:** File naming coherence, whether split files function as coherent standalone reference artifacts, navigational quality.

**Findings:**

🔴 **`ref-object-design-vectors-a.md` and `-vectors-b.md` names encode no semantic content.** The word "vectors" appears neither in the source file name, description, nor the referenced content ("object rehabilitation," "test isolation"). The `-a`/`-b` suffix convention implies arbitrary halves of a whole, not distinct conceptual units. If a developer receives only the filename, they learn nothing. Required fix: rename to semantically meaningful names before this proposal can be implemented.

🟡 **`ref-brownfield-migration.md` creates a naming collision with `ref-migration-playbooks.md`.** Both files will contain "migration" content. A developer scanning the directory listing will not be able to distinguish them. Consider `ref-brownfield-tier-configs.md` and `ref-brownfield-cwr-patterns.md` as alternatives.

🟡 **`ref-mental-models-memory.md` and `ref-mental-models-lang.md` naming is somewhat thin.** A developer unfamiliar with the split would not know that "memory" means "GC→C++ mental model transitions for memory management" specifically. The `reference-index.md` description mitigates this but the filename alone is not self-explanatory.

🟢 **Most other split names are well-formed.** `ref-testing-ci-policy.md`, `ref-testing-gtest-core.md`, `ref-testing-gtest-advanced.md`, `ref-migration-pre-cpp17.md`, `ref-migration-cpp17-plus.md`, `ref-core-type-safety.md`, `ref-core-modern-idioms.md`, `ref-concurrency-threading.md`, `ref-concurrency-async.md` — all of these communicate their content at a glance.

🟡 **31 files in a flat directory is approaching the upper cognitive limit for navigation.** Without the `reference-index.md` as a routing layer, a developer `ls`-ing the directory would see 31 `ref-*.md` files with no obvious grouping. Consider whether subdirectories (e.g., `reference/core/`, `reference/legacy/`) would improve navigability. This is an advisory finding — not a blocker given that `reference-index.md` exists as a routing layer.

**Verdict: 🔴 BLOCKED** — The `ref-object-design-vectors-a/b.md` names are incoherent. The naming issue will propagate into AVATAR-RAG-INDEX.yaml routing examples and into the `reference-index.md`. It must be resolved before implementation.

---

### Persona 12 — Patricia Osei | Change Management & Organizational Risk

**Scope:** Risk register quality, migration blast radius, rollback readiness, external dependencies.

**Findings:**

🟢 **Risk register covers the most critical risks.** Section-boundary content sharing, the AVATAR-RAG-INDEX.yaml co-change risk, and token estimate overage risks are all present.

🔴 **Risk register contains a factual error: `ref-legacy-orientation.md` is listed as "within target."** The risk register states: "Content is already measured and within target; no further split required." The measured value is 3,918 tokens, which exceeds the 3,500-token target. This mischaracterizes the actual risk level. This is a Low/Low risk entry for something that is actually a blocker for the primary success criterion.

🟡 **No rollback plan is documented.** The proposal creates 15 new files and removes 14 existing files in the same set of commits. If a post-merge regression is discovered, rolling back requires recreating all 14 original files from git history. For a 14-file deletion operation, a rollback procedure should be explicit: the PR should not use `--squash` merge, and the archival instructions should note that reverting the merge commit restores all 14 source files.

🟡 **"Other proposals referencing old ref file names break" risk is rated Medium/Medium** but the mitigation ("search repo for references before closing the PR") is task 1.5 and 17.4 which are far apart in the task sequence. If old references are found at Phase 17, fixing them requires re-doing the AVATAR-RAG-INDEX.yaml update (Phase 16). The mitigation should be moved entirely to Phase 1 (pre-flight) and confirmed before any splitting begins.

🟡 **No mention of external tooling risk.** If any CI scripts, Makefile targets, or pre-commit hooks reference the 14 old filenames directly (not through constitution-lint), those would fail silently after the rename. Task 1.5 should explicitly check scripts in `.github/workflows/`, `tools/`, and `Makefile` (if present).

🟢 **Relationship to Other Proposals table is accurate and complete.** All four related proposals are correctly characterized and none are listed as conflicting.

**Verdict: ⚠️ CONDITIONAL PASS** — The rollback gap and the reference search timing issue are significant process risks. The factual error in the risk register is the same blocker found by other personas.

---

## SYNTHESIS

### Overall Panel Verdict: 🔴 BLOCKED

The proposal has four independent blocking issues that must be resolved before it can proceed to implementation. None of these blockers are architectural — they are all correctable defects in the proposal document and task plan.

---

### Blocking Issues Table (Must Resolve Before Merge)

| # | Blocking Issue | Finding Origin | Location in Proposal | Required Fix |
|---|----------------|---------------|---------------------|-------------|
| B1 | **`ref-legacy-orientation.md` at 3,918 tokens violates the ≤3,500-token target.** The risk register incorrectly states it is "within target." The proposal's own success criterion will fail as written. | P1, P6, P9, P12 | Risk Register; Split Plan table | Either: (a) find a second split point within `ref-legacy-orientation.md` to bring it to ≤3,500t, or (b) redesign the `ref-legacy-navigation.md` split strategy entirely. Since `ref-legacy-priorities.md` would be only 312 tokens, a 3-way or different boundary split is the better option. |
| B2 | **`ref-object-design-vectors-a.md` and `ref-object-design-vectors-b.md` are semantically opaque names.** They encode no content meaning and will degrade RAG routing quality when propagated into AVATAR-RAG-INDEX.yaml. | P7, P11 | Split Plan table; Deliverables D8, D9 | Rename to semantically meaningful names based on actual content (e.g., `ref-object-design-rehabilitation.md` and `ref-object-design-isolation.md`). Update all downstream references (PROPOSAL.md, tasks.md, Deliverables table). |
| B3 | **Tasks.md Phases 3–14 collapse RED and GREEN into a single combined step, violating ENG-4.1 Atomic TDD Law.** A proposal citing ENG-4.1 cannot have task phases that elide the RED step. | P10 | tasks.md Phases 3–14 | Expand each "RED/GREEN:" combined task into separate RED task (write failing test) and GREEN task (write minimum code). This changes approximately 24 tasks into 48 tasks but honors the law the proposal cites. |
| B4 | **`ref-legacy-priorities.md` at 312 tokens is a pathologically small file** that cannot function as a standalone RAG reference artifact, fails the progressive disclosure quality bar, and exists as a direct consequence of the B1 split error. | P3, P6, P7 | Split Plan table; Deliverable D29 | Resolved by fixing B1 — redesign the `ref-legacy-navigation.md` split strategy to produce two files that are both meaningfully sized (ideally 1,500–3,500 tokens each). |

> ⚠️ Note: B1 and B4 are coupled — fixing B1 (the 3,918-token violation) by redesigning the split strategy will naturally resolve B4 (the 312-token micro-file). They should be fixed together.

---

### High-Priority Improvements Table (Resolve Before or During Phase 1)

| # | Issue | Personas | Recommended Action |
|---|-------|---------|-------------------|
| H1 | **Phase 16 tasks severely underestimate the AVATAR-RAG-INDEX.yaml update scope.** 3 subtasks for 40+ routing decisions + pre-existing stale counts. | P4, P6 | Decompose task 16.2 into per-★-file routing decision tasks. Add a task to correct all pre-existing stale token counts. Add a task to write new routing entries for the 15 new files (1–2 per new file). |
| H2 | **`ref-brownfield-migration.md` naming collision with `ref-migration-playbooks.md`.** Both contain "migration" and will be confusing in directory listing and index. | P3, P11 | Rename `ref-brownfield-migration.md` to `ref-brownfield-tier-configs.md` (or similar) before implementation. Update PROPOSAL.md, tasks.md, deliverables, and AVATAR-RAG-INDEX.yaml references. |
| H3 | **Existing test suite (`tests/unit/test_cpp_avatar/`) not in cross-avatar impact analysis.** Tests may check specific file names or the count of 16 reference files, and will fail silently after the split. | P9 | Add task to Phase 1 pre-flight: audit all test files for hard-coded references to the 14 renamed files or to the count 16. Update affected tests before Phase 2 splitting begins. |
| H4 | **Task 1.5 (search for old file references) is too late and too narrow.** It is currently positioned as pre-flight but does not explicitly cover `docs/`, `.github/workflows/`, `tools/`, or the test suite. | P9, P12 | Expand task 1.5 scope to cover the full repository: `docs/`, `tools/`, `tests/`, `.github/`. Move the reconciliation gate to Phase 1 exit criteria — do not begin Phase 2 until all cross-references are inventoried. |
| H5 | **No test validates content correctness of splits** — only file existence and token count. "Zero content loss" is a success criterion but no test enforces it. | P8, P10 | Add content-presence assertions to tests: (1) expected H2 section titles from source appear in exactly one output file, (2) for ★ version splits, no C++20 constructs (`co_await`, `std::stop_token`) appear in the pre-C++20 output file. |
| H6 | **`docs/guides/avatars/split-reference-architecture.md` is not in cross-avatar impact analysis.** This guide likely references "16 reference files" and will be stale. | P9 | Add `split-reference-architecture.md` to the cross-avatar impact analysis table. Add a task (Phase 15 or 16) to update this guide to reflect 31 files. |
| H7 | **`ref-legacy-orientation.md` risk register entry is factually wrong** (claims 3,918t is "within target"). | P1, P12 | Correct the risk register. After redesigning the B1 split, update the risk register to accurately reflect the actual post-split file sizes. |

---

### Advisory Improvements Table (Future Phases / Nice-to-Have)

| # | Issue | Personas | Suggested Action |
|---|-------|---------|-----------------|
| A1 | `ref-concurrency-threading.md` at 1,858 tokens warrants re-measurement at Phase 1 — if only 4 major facility families are described in 1,858 tokens, content may be thin. | P1 | Add to Phase 1 pre-flight checklist. |
| A2 | `reference-index.md` should include a "CWR Quick Start" subsection surfacing the 3–4 most critical files for the primary brownfield consumer. | P3, P7 | Add to D30 description in PROPOSAL.md. |
| A3 | Phase 0 tasks.md checkboxes are annotated with `✓ (done)` in text rather than `[x]`. Progress automation may not count these as complete. | P2 | Change `[ ] 0.1 ... ✓ (done)` to `[x] 0.1 ...` format. |
| A4 | `ref-safety-jni-abi.md` at 1,035 tokens should be verified that it contains substantive content, not just headers. | P5 | Add content-adequacy check to Phase 1 pre-flight. |
| A5 | ±20 token tolerance in per-split VERIFY tasks (Phase 2.7 etc.) may be too strict. Recommend ±50 per split file to account for structural headers. | P10 | Update VERIFY task tolerances in tasks.md. |
| A6 | Post-split `reference-index.md` (31 files) should group related split pairs visually (e.g., ★ version pairs annotated as paired alternatives). | P7 | Add to D30 specification: "annotate ★ split pairs as related pair; include 'See Also: [partner file]' annotation." |
| A7 | No rollback procedure documented. After merge, reverting requires git history replay. | P12 | Add note to archival instructions: "Do not squash-merge — preserve individual split commits for rollback capability." |
| A8 | ENG-6.7 citation may be a stretch — ENG-10.1 already covers index integrity. | P2 | Consider replacing ENG-6.7 with ENG-11.1's subsidiary requirement for change traceability, or drop it. Advisory only. |

---

### Phase 17 Execution Checklist (Blocking Gate — Do Not Skip)

Phase 17 as written in tasks.md is structurally correct. The following additions are required before Phase 17 can serve as a reliable gate:

| # | Check | Current Status | Required Addition |
|---|-------|---------------|------------------|
| ✅ | All 31 reference files ≤ 3,500 tokens | Present (17.1) | None — but B1 must be fixed for this to pass |
| ✅ | Total corpus tokens = 76,152 ± 200 | Present (17.2) | Tighten tolerance to ±100 per success criterion |
| ✅ | Zero broken internal links in reference-index.md | Present (17.3) | None |
| ✅ | All references to 14 renamed files updated | Present (17.4) | Must include `docs/`, `tools/`, `tests/`, `.github/` scope |
| ✅ | Full test suite green | Present (17.5) | None |
| ✅ | `aa-constitution-lint .` — 0 failures | Present (17.6) | None |
| ❌ | **MISSING: Content completeness check** | Absent | Add 17.7: Verify all H2 section titles from each source file appear in exactly one output file |
| ❌ | **MISSING: Version correctness check** | Absent | Add 17.8: Verify ★ pre-C++20 output files contain no C++20-specific constructs (`co_await`, `std::stop_token`, `std::jthread`) |
| ❌ | **MISSING: AVATAR-RAG-INDEX.yaml token count accuracy** | Absent | Add 17.9: Verify all token counts in AVATAR-RAG-INDEX.yaml cpp section match measured values ± 10% |

---

### Summary Scorecard

| Persona | Domain | Verdict |
|---------|--------|---------|
| Dr. Anjali Mehta | C++ Technical Correctness | 🔴 BLOCKED |
| Marcus Webb | Constitution Governance | ✅ PASS |
| Dmitri Volkov | Legacy/Brownfield C++ | ⚠️ CONDITIONAL PASS |
| Elena Nakamura | Platform Engineering | ⚠️ CONDITIONAL PASS |
| Col. James Okonkwo | Safety-Critical Systems | ✅ PASS |
| Dr. Priya Sundaram | RAG Architecture | 🔴 BLOCKED |
| Sofia Chen | Developer Experience | 🔴 BLOCKED |
| Dr. Thomas Hart | Testing Correctness | ⚠️ CONDITIONAL PASS |
| Rachel Torres | Cross-Avatar Impact | ⚠️ CONDITIONAL PASS |
| Owen Bradley | TDD Compliance | 🔴 BLOCKED |
| Dr. Yuki Tanaka | Information Architecture | 🔴 BLOCKED |
| Patricia Osei | Change Management | ⚠️ CONDITIONAL PASS |

**5 BLOCKED · 5 CONDITIONAL PASS · 2 PASS**

**Overall Verdict: 🔴 BLOCKED — 4 blocking issues must be resolved before the proposal can proceed to implementation. All blockers are correctable defects; the architecture is sound.**
