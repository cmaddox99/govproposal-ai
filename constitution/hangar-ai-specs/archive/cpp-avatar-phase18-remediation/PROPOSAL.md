# Proposal: C++ Avatar Phase 18 — Panel Review Remediation + Workflow Compliance

**Proposal ID:** cpp-avatar-phase18-remediation  
**Submitted:** April 13, 2026  
**Status:** ACTIVE — In Progress on PR #14  
**Depends On:** Work executes ON `feature/c-plus-plus-avatar-enrichment-proposal` (PR #14), not after it merges  
**Sources:**
- 7-Persona Panel Review (`hangar-ai-specs/changes/c-plus-plus-avatar-enrichment/review/panel-review.md`)
- Avatar Workflow Validate Mode assessment (`workflows/avatar-workflow.md`) — see §Workflow vs Panel Analysis below
- Workflow Validate Report (`hangar-ai-specs/changes/c-plus-plus-avatar-enrichment/review/workflow-validate-report.md`) — 2026-04-13 Mode 3 scan
- RAG Validation Evidence (`hangar-ai-specs/evidence/avatar-rag-cpp.md`) — 5 canonical queries

---

## Laws Cited (ENG-11.2 Compliance)

Per [ENG-11.2: Proposal Completeness](laws/engineering/eng-11-hangar-sdd.md), every proposal must cite at least one law. This proposal is governed by and implements the following laws:

| Law ID | Title | Relevance |
|--------|-------|-----------|
| [ENG-11.1](laws/engineering/eng-11-hangar-sdd.md) | Hangar SDD Law (Non-Negotiable) | Governs proposal lifecycle: PROPOSE → IMPLEMENT → ARCHIVE |
| [ENG-11.2](laws/engineering/eng-11-hangar-sdd.md) | Proposal Completeness | Requires law citations, success criteria, and deliverables |
| [ENG-4.1](laws/engineering/eng-4-testing.md) | Atomic TDD Law (Non-Negotiable) | All code changes follow RED–GREEN–REFACTOR |
| [ENG-4.2](laws/engineering/eng-4-testing.md) | Test Pyramid Law | Test distribution must reflect pyramid structure |
| [ENG-6.1](laws/engineering/eng-6-security.md) | Security by Design (Non-Negotiable) | 16 security examples must be routable — not just present |
| [ENG-10.1](laws/engineering/eng-10-constitution.md) | Constitution Compliance | Manifest references must point to existing files |
| [BUS-1.1](laws/business/bus-1-compliance.md) | Priority Hierarchy (Legal First) | Aviation safety standards (DO-278A, FAR 117) take precedence |
| [BUS-2.1](laws/business/bus-2-compliance.md) | FAA Compliance | DO-278A and FAR 117 guidance must be surfaced at routing layer |
| [BUS-7.1](laws/business/bus-7-operational-governance.md) | Audit Trail Law (Non-Negotiable) | PROGRESS.md tracks all phase completions |

---

## Problem Statement (Per PRD-1.2)

The 7-persona panel review of PR #14 (`c-plus-plus-avatar-enrichment`) identified two blocking issues and fifteen advisory findings. A subsequent avatar-workflow Validate Mode assessment (`workflows/avatar-workflow.md`) surfaced three additional findings that the panel review missed entirely. Together these define the full remediation scope.

**Remaining blocker (B-2):** `full-reference.md` is referenced in `AVATAR-RAG-INDEX.yaml` with no token budget annotation. At 5,519 lines (~20,000+ tokens), loading this file in response to a RAG query will overflow any agent context window. The RAG index currently implies this file can be served as a query result — it cannot.

**Routing gaps (H-1 through H-4):** Five high-priority manifest and routing deficiencies mean agents will fail to route to correct guidance for error handling (ENG-3.7), observability (ENG-5.5), failure handling (ENG-7.1), test structure (ENG-4.4), resiliency patterns (ENG-7.2–7.5), and safety-critical standards (MISRA C++, DO-278A). The panel's H-4 recommendation is framed under ENG-6.x only — citing DO-278A as a BUS-* law in a technology avatar would violate Safeguard 2 (law domain boundary).

**Workflow findings (W-1 through W-3):** The avatar-workflow Validate Mode surfaced three issues the panel review did not: a missing RAG validation evidence file required by Phase 5/6, a broken `activates.workflows` reference (`brownfield-adoption` does not exist as a workflow file), and an undocumented 5-canonical-query contract. These are resolvable on PR #14.

**Separate-PR item (W-4):** The workflow enforces a 150-token budget for `manifest.yaml`. The current manifest is approximately 1,500 tokens — 10× over budget. Fixing this requires extracting the `stack`, `standard_tiers`, and `project_archetypes` blocks into separate companion files and restructuring the manifest to a routing-only document. This is a major breaking change that affects 16 test files and cannot be safely bundled into PR #14.

**Additional workflow findings (W-5 through W-7):** The 2026-04-13 Validate Mode assessment surfaced three further issues: (W-5) six manifest blocks (`standard_tiers`, `ci_toolchain`, `authorities`, `brownfield_adoption`, `skill_parity`, `project_archetypes`) are either not on the schema allowlist or explicitly forbidden — Amendment O removed three blocks but missed these six; (W-6) `activates.skills` references use a `skill-` prefix (`skill-06-atomic-tdd`) that does not match the actual filenames (`06-atomic-tdd.md`), creating a routing dependency on implicit prefix-stripping; (W-7) RAG validation query Q2 (error handling without exceptions) fails because ENG-3.7 has no `example_file`, dropping recall to 4/5 (80%) — below the 95% threshold. W-5 strengthens the W-4 manifest restructure case; W-6 is fixable on PR #14; W-7 is resolved by Phase 2 (H-1).

**Advisory gaps (A-1 through A-8):** Eight advisory items reduce the avatar's usability for brownfield CWR developers and leave incomplete audit citations.

---

## Workflow vs Panel Review Analysis

This section documents where the two review sources agree, diverge, or prescribe incompatible solutions.

### Agreements

| Finding | Panel | Workflow | Status in This Proposal |
|---------|-------|----------|------------------------|
| `full-reference.md` token overflow risk | B-2 | Phase 5 hard fail >3,500 tokens/query | Phase 1 — `on_demand_only: true` satisfies both |
| Missing `example_file` for ENG-3.7, ENG-5.2, ENG-5.5, ENG-7.1 | H-1 | Phase 2.1 schema scan gap + W-7 RAG recall 4/5 | Phase 2 — create files + add manifest pointers |
| 25 Phase 16 skills need index verification | A-7 | Phase 2.5 orphaned-skill check | Phase 5 — A-7 audit |

### Disagreements / Tensions

| Issue | Panel Says | Workflow Says | Resolution |
|-------|-----------|--------------|------------|
| **DO-278A citation** | Add DO-278A guidance to technology avatar (H-4) | `technology + BUS-* → BLOCKING` (Safeguard 2) | ✅ Resolved: Phase 4 creates `ENG-6.1-misra-do278a.md` using only ENG-6.x framing. DO-278A is referenced as *context* within the example, not as a `specializes_laws` BUS-* entry. |
| **ENG-6.1 routing** | Create an `ENG-6.1-index.md` topic router (H-3) | Workflow only requires one `example_file` per law — `ENG-6.1-security-by-design.md` already satisfies this | ✅ Resolved: Index file is advisory quality improvement, not a workflow blocker. Phase 3 keeps it but marks it advisory. |
| **Manifest size** | Never mentioned | 150-token hard limit — current manifest is ~1,500 tokens (BLOCKING) | ⚠️ Separate PR required — see W-4 below. Cannot safely bundle into PR #14. |
| **RAG evidence file** | Not checked | `avatar-rag-cpp.md` required before Phase 6 commit gate | ✅ Resolved: New Phase 0.6 creates this file on PR #14. |
| **`brownfield-adoption` workflow** | Not checked | Safeguard 5: referenced workflow must exist as a file in `/workflows/` | ✅ Resolved: New Phase 0.7 fixes the manifest reference. |
| **6 forbidden manifest blocks (W-5)** | Panel V4 removed 3 blocks (`anti_patterns`, `anti_patterns_by_tier`, `retrieval_triggers`) | 6 additional blocks not on allowlist: `standard_tiers`, `ci_toolchain`, `authorities` (unknown); `brownfield_adoption`, `skill_parity`, `project_archetypes` (explicitly forbidden) | ⚠️ Bundle with W-4 manifest restructure (separate PR). These contribute ~800 tokens to the manifest. |
| **Skills naming mismatch (W-6)** | Not checked | `activates.skills` uses `skill-` prefix but files don't have it — routing depends on implicit prefix-stripping | 🟡 Fixable on PR #14: update manifest to match actual filenames, or document prefix convention. |
| **RAG recall 4/5 (W-7)** | H-1 noted routing gap qualitatively | Workflow quantifies: Q2 fails, recall = 80% (below 95% threshold) | ✅ Resolved by Phase 2 (H-1) — creating `ENG-3.7-error-handling.md`. |

### What Goes on PR #14 vs Separate PR

| Item | PR #14 | Separate PR |
|------|--------|------------|
| B-2 RAG index annotation | ✅ | — |
| H-1/H-2 missing example files | ✅ | — |
| H-3 ENG-6.1 index (advisory) | ✅ | — |
| H-4 MISRA/DO-278A example (ENG-6.x only) | ✅ | — |
| A-1–A-8 advisory improvements | ✅ | — |
| W-1 RAG evidence file creation | ✅ | — |
| W-2 brownfield-adoption workflow reference fix | ✅ | — |
| W-3 5 canonical RAG queries documentation | ✅ | — |
| W-6 Skills naming convention fix (update manifest refs) | ✅ | — |
| **W-4 manifest.yaml 150-token restructure** | — | ✅ New proposal needed |
| **W-5 6 forbidden manifest blocks removal** | — | ✅ Bundle with W-4 |

---

## Solution

This proposal executes the remediation work on PR #14 in six phases, plus documents the separate-PR item for W-4.

| Phase | Scope | Priority | PR |
|-------|-------|----------|----|
| 0 (ext) | W-1/W-2/W-3/W-6: RAG evidence file, broken workflow reference, canonical queries, skills naming fix | Critical | #14 |
| 1 | B-2: Add `on_demand_only: true` + token budget annotation to RAG index | Critical | #14 |
| 2 | H-1/H-2: Create 4 missing example files; add manifest routing entries (resolves W-7 RAG recall gap) | High | #14 |
| 3 | H-3: ENG-6.1 index topic router (advisory) | Medium | #14 |
| 4 | H-4: MISRA C++ / DO-278A example under ENG-6.x | High | #14 |
| 5 | A-1–A-8: Advisory improvements | Advisory | #14 |
| W-4/W-5 | manifest.yaml 150-token restructure + 6 forbidden block removal | Workflow BLOCKING | Separate PR |

---

## Deliverables

### Phase 1 — RAG Index Token Budget (B-2)
- `avatars/AVATAR-RAG-INDEX.yaml` updated with `on_demand_only: true` and size note on `full-reference.md` entry

### Phase 2 — Missing Example Files and Manifest Routing (H-1, H-2)
- `avatars/technology/cpp/examples/ENG-3.7-error-handling.md` — C++ error handling patterns
- `avatars/technology/cpp/examples/ENG-5.5-observability.md` — OpenTelemetry C++ instrumentation
- `avatars/technology/cpp/examples/ENG-7.1-failure-handling.md` — bulkhead/fallback patterns
- `avatars/technology/cpp/examples/ENG-5.2-mixed-standard.md` — C++03/C++11/C++20 coexistence use case
- `avatars/technology/cpp/manifest.yaml` updated: `example_file` added for ENG-3.7, ENG-5.5, ENG-7.1; ENG-4.4 and ENG-7.2–7.5 added to `specializes_laws`; second ENG-5.2 entry added

### Phase 3 — ENG-6.1 Routing Index (H-3)
- `avatars/technology/cpp/examples/ENG-6.1-index.md` — topic router for all 16 ENG-6.1 example files
- `avatars/AVATAR-RAG-INDEX.yaml` updated with section-level entry for ENG-6.1 index

### Phase 4 — Safety-Critical Standards (H-4)
- `avatars/technology/cpp/examples/ENG-6.1-misra-do278a.md` — MISRA C++ rules and DO-278A compliance patterns for CWR
- `avatars/technology/cpp/manifest.yaml` updated: MISRA/DO-278A example referenced under ENG-6.1 (or new law entry)

### Phase 5 — Advisory Improvements (A-1 through A-8)
- `agent-skills/skills-by-domain/development-practices/skill-cpp-jni-bridge.md` — JNI boundary skill
- `avatars/technology/cpp/examples/ENG-4.1-far117-traceability.md` — FAR 117 test name → regulation traceability matrix example
- `avatars/technology/cpp/full-reference.md` additions: Brownfield Entry Path section, skill decision tree
- `avatars/technology/cpp/guidance.md` updated: named anchor links to key `full-reference.md` sections
- `agent-skills/skills-by-domain/development-practices/skill-index.yaml` (or equivalent): skill naming convention documented; all 25 Phase 16 skills verified present
- `agent-skills/skills-by-domain/development-practices/skill-cpp-compliance-rating.md` D5 updated: `BUS-7.1` citation added alongside `ENG-6.7`

---

## Success Criteria

| Criterion | Measurement |
|-----------|-------------|
| W-1 resolved | `hangar-ai-specs/evidence/avatar-rag-cpp.md` exists with 5 canonical queries and RAG validation results |
| W-2 resolved | `manifest.yaml` `activates.workflows` references only workflow files that exist under `workflows/` |
| W-3 resolved | RAG evidence file documents 5 canonical queries with token estimates ≤3,500 per query |
| B-2 resolved | `AVATAR-RAG-INDEX.yaml` entry for `full-reference.md` contains `on_demand_only: true` |
| H-1 resolved | `manifest.yaml` `specializes_laws` has `example_file` for ENG-3.7, ENG-5.5, ENG-7.1; files exist on disk; all new example files ≤850 tokens |
| H-2 resolved | ENG-4.4, ENG-7.2–7.5 present in `specializes_laws`; ENG-5.2 has two `example_file` entries |
| H-3 resolved | `ENG-6.1-index.md` exists; all 16 ENG-6.1 files referenced within it |
| H-4 resolved | `ENG-6.1-misra-do278a.md` exists ≤850 tokens; manifest references it under ENG-6.1; file uses only ENG-6.x law framing (no BUS-* citations in specializes_laws) |
| Advisory complete | A-1 through A-8 checked in `tasks.md` |
| W-4 documented | Separate proposal exists for manifest.yaml 150-token restructure |
| W-5 documented | 6 forbidden manifest blocks identified and tracked in W-4 manifest restructure proposal |
| W-6 resolved | `activates.skills` references match actual filenames (prefix removed or convention documented) |
| W-7 resolved | RAG recall 5/5 after ENG-3.7 `example_file` is created (H-1) |
| Tests green | `pytest` passes all existing 653+ tests |
| Linter green | `aa-constitution-lint .` passes with 0 failures |

---

## Risk Register

| Risk | Likelihood | Mitigation |
|------|-----------|-----------|
| PR #14 not yet merged when implementation starts | Medium | All Phase 18 work is on the PR #14 branch — no separate merge needed |
| New example files exceed 850-token workflow budget | Medium | Enforce word-count check (≤680 words ≈ 850 tokens) before committing each new file |
| H-4 MISRA/DO-278A file accidentally cites BUS-2.1 in specializes_laws | Low | Test explicitly checks manifest has no new BUS-* entries; file may reference DO-278A in prose only |
| Phase 5 JNI skill not yet in skill-index.yaml → orphaned skill warning | Medium | Register new skill in same commit as skill file creation |
| W-4 manifest restructure deferred indefinitely | Medium | Open W-4 proposal in same merge window as PR #14 to keep pressure on resolution |

---

## Taxonomy Gate (skill-30)

Per [skill-30: Taxonomy-Governed Avatar Enrichment](agent-skills/skills-by-domain/discovery-research/30-taxonomy-governed-avatar-enrichment.md):

| Gate | Question | Result | Rationale |
|------|----------|--------|-----------|
| Domain | Durable business capability independent of team names? | ✅ PASS | C++ avatar routing is a stable engineering capability |
| Boundary | No overlap with existing avatar? | ✅ PASS | This extends the existing cpp avatar, not a new avatar |
| Stability | Remains valid if org structure changes? | ✅ PASS | Law-based routing is org-independent |
| Retrieval | Improves RAG precision versus adding ambiguity? | ✅ PASS | Resolves routing gaps identified by panel review |
| Scope | Fits within existing `avatars/technology/cpp/` scope? | ✅ PASS | All deliverables extend the existing avatar; no new avatar needed |

---

## Archival Instructions

When all tasks are complete:

```bash
mv hangar-ai-specs/changes/cpp-avatar-phase18-remediation \
   hangar-ai-specs/archive/$(date +%Y-%m-%d)-cpp-avatar-phase18-remediation
```

Update `PROGRESS.md` status to `COMPLETE` before archiving.
