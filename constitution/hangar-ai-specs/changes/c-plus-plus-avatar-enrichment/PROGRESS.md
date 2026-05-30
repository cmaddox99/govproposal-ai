# Progress: c-plus-plus-avatar-enrichment

**Status:** 🟡 READY FOR RE-REVIEW — Amendment Q Complete (All 36 Edge-Case Sections Added)
**Started:** 2026-04-05
**Last Updated:** 2026-04-14

---

## Governance Review — PR #14 (2026-04-10)

**Reviewer:** adeel-ali-aa | **Review ID:** #4086806910 | **Verdict:** 🔴 BLOCKED — Do Not Merge

The governance panel ran an Assess & Correct + Validate review against the Avatar Workflow
Proposal and found **8 constitutional violations** requiring correction before merge.
Amendment O addresses all violations. Three companion proposals filed as separate PRs.

| Violation | Description | Status |
|-----------|-------------|--------|
| V1 | 9 BUS-* examples in technology avatar | ✅ Resolved (Step 16.1) |
| V2 | 5 PRD-* examples in technology avatar | ✅ Resolved (Step 16.1) |
| V3 | `governance_overrides` self-approval in manifest.yaml | ✅ Resolved (Step 16.2) |
| V4 | `anti_patterns`/`retrieval_triggers` blocks in manifest.yaml | ✅ Resolved (Step 16.3) |
| V5 | BUS-* law refs in `skill-cpp-compliance-rating.md` | ✅ Resolved (Step 16.4) |
| V6 | `compliance-rating-system.md` embedded as shadow governance | ✅ Resolved (Step 16.5) |
| V7 | `guidance.md` ~66,500 tokens (limit: 450) | ✅ Resolved (Step 16.6) |
| V8 | Companion proposals not filed | ✅ Resolved (Step 16.7) |

---

## Status Summary

| Phase | Status | Description |
|-------|--------|-------------|
| Phase 0: Hangar SDD Execution Artifacts | ✅ Complete | `PROPOSAL.md`, `tasks.md`, and `PROGRESS.md` created; all 12 governance compliance gaps patched |
| Phase 1: Avatar Foundation | ✅ Complete | `manifest.yaml` and `guidance.md` created with full cross-avatar parity |
| Phase 2: Safety and Toolchain Policies | ✅ Complete | All 20 policy sections documented with brownfield exceptions |
| Phase 3: Non-Negotiable Law Examples | ✅ Complete | 18/18 law-mapped example files created |
| Phase 3a: Supplemental Engineering-Law Examples | ✅ Complete | 9/9 parity examples created |
| Phase 4: Registry, RAG, and Governance Wiring | ✅ Complete | Indexing and routing updates |
| Phase 5: Validation and Review | ✅ Complete | All acceptance criteria validated |
| Phase 6: Advanced C++20+ Governance | ✅ Complete | Exception safety, coroutines, logging, modules, allocators |
| Phase 7: Critical Fixes (Amendment C) | ✅ Complete | Law ID bug fixes, compiler warning policy |
| Phase 8: P0 Governance Gaps (Amendment D) | ✅ Complete | Concurrency, resiliency, ABI, deploy, debug skills |
| Phase 9: Examples & Novice Guidance (Amendment E) | ✅ Complete | 10 C++20+ examples, legacy code navigation |
| Phase 10: Standard-Tier Foundation (Amendment F) | ✅ Complete | 5 standard tiers, tiered compilers, per-tier governance |
| Phase 11: Migration Playbooks (Amendment G) | ✅ Complete | 4 migration playbooks, 7 examples, dual-toolchain |
| Phase 12: Legacy Anti-Patterns & Skills (Amendment H) | ✅ Complete | 13 anti-patterns, 4 new skills, 4 skill updates, RAG |

**Overall:** Phases 0–17 complete. 653 tests passing. 276 tasks tracked (276 done). aa-constitution-lint 17/17 passing. Avatar v2.0.0 ready for merge.

---

## Decision Log

Resolved stakeholder decisions reflected in `PROPOSAL.md`:

- Q1: `laws/index.yaml` is authoritative for law labeling and non-negotiable scope
- Q2: `manifest.yaml` remains engineering-focused; cross-domain non-negotiables live in `examples/`
- Q3: C++20 minimum for greenfield; C++23 recommended where supported; brownfield older standards permitted with modernization plan
- Q4: Mandatory CI gates are `clang-tidy`, ASan, UBSan; recommended gates include TSan, clang static analyzer, and Mull mutation testing where LLVM/Clang is available, with documented brownfield exceptions when Mull is not yet practical
- Q5: Unsafe-boundary governance uses repository-configurable policy with Option 2 default
- Q6: GoogleTest + GoogleMock default; brownfield repos without frameworks adopt immediately
- Q7: Supplemental engineering-law examples apply to C++ for this change only
- Q8: Support both `vcpkg` and `Conan`; recommend `vcpkg` by default
- Q9: `skill-04-business-domain-modeling` mandatory by default, with documented exception for low-domain-complexity infrastructure repos

---

## Recent Updates

- **Amendment B: Advanced C++20+ Governance (2026-04-06)** — Senior architect review identified critical gaps in exception safety, coroutines, logging, modules, and allocator governance. Adds 5 new guidance sections, 3 new skill modules, and registry updates. Total task count 91 → 109 (18 new tasks in Phase 6).
- **Amendment A: Testing Strategy Upgrade (2026-04-05)** — Added to PROPOSAL.md. Introduces three testing improvements: (A.1) reusable `avatar_test_helpers.py` module with governance validators using `LawRegistry`, (A.2) upgraded test approach for tasks 2.7+ using schema/compliance checks, (A.3) comprehensive `test_constitution_compliance.py` suite in Phase 5. Two new tasks added (2.7a, 5.6a); total count 89 → 91. Deferred `constitution-lint` extension to separate proposal `avatar-constitution-lint-extension`.
- Updated execution checklist in `tasks.md` to reflect the Mull mutation-testing decision in Phase 2 policy work.
- Added an explicit Phase 2 task for Mull policy text (LLVM/Clang prerequisite + phased brownfield exception handling), and renumbered subsequent Phase 2 tasks accordingly.
- Updated `PROPOSAL.md` to replace generic security/DevOps tool wording with a short cross-language alignment matrix for C++, including per-tool selection rationale.
- Expanded `tasks.md` for audit traceability to cover matrix/rationale implementation work (added Phase 2 items 2.18 and 2.19; total task count updated to 72).
- Validated proposal references/cross-links and checklist counts for consistency (`tasks.md` remains 3 completed out of 72 total).
- Updated `PROPOSAL.md` to require Markdown hyperlinks for constitution law/rule references in implementation documents.
- Expanded `tasks.md` to include explicit hyperlink-validation in Phase 5 (added item 5.7, final review moved to 5.8; total task count updated to 73).
- **(Final Review — 12-Gap Compliance Patch)** Audited proposal against all enrichment governance rules (skill-30, enrichment workflow, spec-governance, law-citation-guide, enrichment templates). Identified and patched 12 gaps:
  - **HIGH:** (1) Added formal Laws Cited section with 13 hyperlinked law references per ENG-11.2. (2) Added explicit 5 taxonomy gate pass/fail results per skill-30. (3) Added anti-pattern alias canonical mapping per skill-30 output #2. (4) Added cross-reference to mutation-testing-governance proposal and ENG-4.11 coordination note. (5) Added evidence source taxonomy tags to key claims per enrichment template conventions.
  - **MEDIUM:** (6) Added risk register with 7 risks and mitigations. (7) Added draft YAML for index.yaml and AVATAR-RAG-INDEX.yaml entries. (8) Added token impact assessment for 37 new files. (9) Added enrichment intake details (target repos, brownfield constraints) per workflow Step 1. (10) Added archival instructions per ENG-11.1 lifecycle.
  - **LOW:** (11) Added rollback/deprecation plan. (12) Noted optional design.md/SPEC.md artifacts per spec-governance.md.
- Updated `tasks.md` with 12 new Phase 0 completed items (0.5–0.16) and 4 new Phase 5 validation items (5.8–5.11, final review renumbered to 5.12); total task count updated from 73 to 89; completed count updated from 3 to 15.
- Converted all References in `PROPOSAL.md` to Markdown hyperlinks per law-citation-guide.md.
- Added mutation-testing-governance proposal and 5 additional governance source files to References section.

---

## Governance Alignment

- Taxonomy classification recorded: technology/runtime capability enrichment
- Five taxonomy gates explicitly documented with pass/fail results (skill-30 method)
- Anti-pattern alias canonical mapping documented (skill-30 required output #2)
- Canonical mapping recorded in proposal
- Brownfield non-rewrite safeguards recorded in proposal
- Minimum review/sign-off roles recorded in proposal
- Laws Cited section added with hyperlink citations (ENG-11.2 compliance)
- Evidence source taxonomy tags applied to key claims (enrichment template convention)
- Cross-reference to mutation-testing-governance proposal documented (ENG-4.11 dependency)
- Risk register with mitigations documented
- Token impact assessment documented
- Enrichment intake details documented (workflow Step 1)
- Archival and rollback plans documented (ENG-11.1 lifecycle)

---

## Immediate Next Steps

1. Human governance review by Constitution Steward, Platform Engineering Lead, Security Reviewer
2. Update PR #14 with Amendments C/D/E deliverables
3. Archive proposal to `hangar-ai-specs/archive/` per ENG-11.1 lifecycle after merge

---

## Governance Sign-Off Checklist

| Law | Requirement | Status | Evidence |
|-----|-------------|--------|----------|
| ENG-4.1 | Atomic TDD — every task follows RED-GREEN-REFACTOR | ✅ Met | 70+ tests, each committed after TDD cycle |
| ENG-6.1 | Security by Design — ownership-first API, unsafe boundary governance | ✅ Met | guidance.md §Ownership-First API, §Unsafe Boundary Governance |
| ENG-6.4 | Data Protection — RAII-based encryption, PII lifetime scope | ✅ Met | examples/ENG-6.4-data-protection.md |
| ENG-6.7 | Audit Trail — structured logging, governance decisions recorded | ✅ Met | PROGRESS.md decision log, examples/ENG-6.7-audit-trail.md |
| ENG-10.1 | Law References Valid — all citations resolve to known laws | ✅ Met | test_law_citations.py validates via LawRegistry |
| ENG-11.1 | Hangar SDD — PROPOSAL.md, tasks.md, PROGRESS.md in hangar-ai-specs/ | ✅ Met | hangar-ai-specs/changes/c-plus-plus-avatar-enrichment/ |
| ENG-2.2 | Layered Architecture — domain/application/infrastructure separation | ✅ Met | manifest.yaml project_structure, examples/ENG-2.2-layers.md |
| ENG-3.1 | Complexity Limits — cyclomatic ≤ 7 enforced by clang-tidy | ✅ Met | guidance.md §CI Quality Toolchain Policy |
| BUS-2.1 | FAA Compliance — aviation regulatory references documented | ✅ Met | examples/BUS-2.1-faa-compliance.md |

**Minimum sign-off roles:** Constitution Steward, Platform Engineering Lead, Security Reviewer.  
**Status:** Awaiting human review after Phase 5 validation completes.

---

## Blockers

None currently.

## Phase 13: Novice C++ Developer Guidance (Amendment I) ✅ Complete

| Deliverable | Status | Tests |
|---|---|---|
| Mental Model Transitions section (8 gaps) | ✅ | 12 |
| Legacy Code Smell Catalog section (14 smells) | ✅ | 17 |
| Legacy Codebase Triage Playbook section | ✅ | 10 |
| Survival Patterns section (week-1 → month-6) | ✅ | 12 |
| Object Design Rehabilitation section (6 vectors) | ✅ | 9 |
| Expanded skill-cpp-legacy-code-navigation.md | ✅ | 3 |
| New skill-cpp-legacy-survival-patterns.md | ✅ | 3 |
| 14 code smell anti-patterns in manifest | ✅ | 14 |
| 8 retrieval triggers in manifest | ✅ | 8 |
| RAG index entries | ✅ | 1 |
| 2 new examples (RAII conversion, characterization test) | ✅ | 4 |
| Phase 5 validation counts updated | ✅ | - |

**Total new tests:** 88 | **Running total:** 496

## Phase 14: Constitution Compliance Rating System (Amendment J) ✅ Complete

| Deliverable | Status | Tests |
|---|---|---|
| Compliance Rating overview in guidance.md | ✅ | 16 |
| 3 example scorecards (greenfield/brownfield/legacy) | ✅ | 1 |
| skill-cpp-compliance-rating.md | ✅ | 6 |
| Compliance rating retrieval triggers | ✅ | 3 |
| Compliance rating RAG entries | ✅ | 1 |
| compliance-rating-system.md reference doc | ✅ | 3 |
| Phase 5 validation counts updated | ✅ | - |

**Total new tests:** 31 | **Running total:** 527

## Phase 15: High-Value Additions (Amendment K) ✅ Complete

| Deliverable | Status | Tests |
|---|---|---|
| Quick-Start Cheat Sheet in guidance | ✅ | 6 |
| MISRA/DO-178C Safety-Critical Section | ✅ | 9 |
| Periodic Re-Rating Schedule | ✅ | 5 |

**Total new tests:** 20 | **Running total:** 547

---

## Phase 16: Constitutional Compliance Corrections (Amendment O) ✅ Complete

| Deliverable | Status | Tests |
|---|---|---|
| 14 BUS-*/PRD-* example files removed | ✅ | 3 |
| manifest.yaml governance_overrides block removed | ✅ | 1 |
| manifest.yaml anti_patterns/retrieval_triggers removed | ✅ | 2 |
| skill-cpp-compliance-rating.md law refs corrected | ✅ | 1 |
| compliance-rating-system.md removed from avatar dir | ✅ | 1 |
| guidance.md rebuilt to ≤450 tokens (two-file architecture) | ✅ | 1 |
| full-reference.md created (docs/guides/avatars/cpp/) | ✅ | — |
| test_phase16_compliance_corrections.py created | ✅ | 8 |
| Companion proposals filed (3) | ✅ | — |
| Test suite: 653 passed, 0 skipped, 0 failed | ✅ | 649 |

**Running total after completion:** 653 tests

---

## Phase 17: File Relocation — Amendment P ✅ Complete

| Milestone | Status | Tests |
|-----------|--------|-------|
| Merge main into PR #14 branch (17.0) | ✅ | — (main at same commit, no-op) |
| git mv full-reference.md to avatars/technology/cpp/ (17.1) | ✅ | — |
| AVATAR-RAG-INDEX.yaml path corrected to `full-reference.md` (17.2) | ✅ | — |
| guidance.md link fixed to `full-reference.md` (17.3) | ✅ | — |
| conftest.py + 14 test files fixture paths fixed (17.4) | ✅ | — |
| Full test suite passes 653 (17.5) | ✅ | 653 |
| aa-constitution-lint passes 17/17 (17.6) | ✅ | — |
| docs/guides/avatars/cpp/ cleaned up (17.7) | ✅ | — |
| Committed [Amendment-P] (17.8) | ✅ | — |

**Running total after completion:** 653 tests passing, 0 failed, 17/17 linter checks passing

---

## Final Summary

| Phase | Description | Tasks | Tests |
|-------|-------------|-------|-------|
| 0 | SDD Artifacts | 16 | 0 |
| 1 | Core Manifest & Guidance | 8 | 12 |
| 2 | Safety Policies & CI | 20 | 28 |
| 3 | Law Examples | 18 | 27 |
| 3a | Supplemental Examples | 9 | 9 |
| 4 | Registry & RAG | 7 | 15 |
| 5 | Validation & Review | 13 | 33 |
| 6 | Expert Review (Amendment B) | 18 | 0 |
| 7 | Critical Fixes (Amendment C) | 7 | 10 |
| 8 | P0 Governance (Amendment D) | 27 | 62 |
| 9 | Examples & Novice (Amendment E) | 15 | 50 |
| 10 | Standard Tiers (Amendment F) | 15 | 51 |
| 11 | Migration Playbooks (Amendment G) | 19 | 56 |
| 12 | Legacy Skills & RAG (Amendment H) | 20 | 55 |
| 13 | Novice Guidance (Amendment I) | 19 | 88 |
| 14 | Compliance Rating (Amendment J) | 13 | 31 |
| 15 | High-Value Additions (Amendment K) | 7 | 20 |
| 16 | Constitutional Corrections (Amendment O) | 17 | 122 |
| 17 | File Relocation — Amendment P | 8 | 0 |
| 18 | Edge Cases & Warnings (Amendment Q) | 37 | 61 |
| **Total** | | **323** | **710** |

---

## Phase 18 — Edge Cases & Warnings (Amendment Q)

Added `## Edge Cases & Warnings` tables to all 36 example files that were missing this section.
One index/router file (`ENG-6.1-index.md`) was excluded as a non-example router. Four Phase 9 files
required additional trimming after edge-case addition to stay within the 600t limit.

| Metric | Value |
|--------|-------|
| Files fixed | 36 / 36 |
| Files excluded (router) | 1 |
| Phase 9 files re-trimmed | 4 |
| New passing tests | +50 (parametrized) |
| Linter checks | 17/17 |

### Key Commits

| Commit | Description |
|--------|-------------|
| `6853d73` | RED: parametrized edge-case test (35 failing params) |
| `d4f02a5`–`8fb2d60` | P1+P2: 10 safety/security files |
| `f086b44` | P3a: 6 standard files (batch) |
| `0c14297` | P3b: 11 files — emoji headers renamed, missing sections added |
| `0f6f5b8` | P3c: trim-to-fit ENG-5.2-project-structure.md (803t → 767t) |
| `e9c792d` | P3d: 8 remaining files (batch) |
| `d24dbc3` | FIX: trim 4 Phase 9 files to 600t budget |

**Running total:** 710 passed, 0 failed, 17/17 linter checks
