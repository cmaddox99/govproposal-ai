# Progress: cpp-avatar-phase18-remediation

**Proposal ID:** cpp-avatar-phase18-remediation  
**Status:** ✅ COMPLETE  
**Phase:** 6 (Archive)  
**Depends On:** `c-plus-plus-avatar-enrichment` PR #14 — **all work executes ON PR #14** (no separate merge dependency)

---

## Phase Status

| Phase | Title | Status | Commit |
|-------|-------|--------|--------|
| 0 | SDD Artifacts + Workflow Findings | ✅ DONE | e9cd7af, 300470b |
| 1 | B-2: RAG Index Token Budget | ✅ DONE | e9cd7af |
| 2 | H-1/H-2: Missing Example Files + Manifest Routing | ✅ DONE | 35ebe06, ee8b37f, 407f4a7, e9f635a |
| 3 | H-3: ENG-6.1 Routing De-Fragmentation | ✅ DONE | b7c0928 |
| 4 | H-4: MISRA C++ / DO-278A Safety-Critical Guidance | ✅ DONE | ba2d8fb |
| 5 | A-1–A-8: Advisory Improvements | ✅ DONE (A-8 BLOCKED — domain boundary) | 6d8bcc8 |
| 6 | Archive | ✅ DONE | see below |

---

## Blocker Log

- **A-8 (BUS-7.1 citation in compliance-rating):** BLOCKED by Phase 16 guard V5
  — platform-engineering skills must only reference ENG-* laws (Safeguard 2).
  BUS-7.1 correctly excluded — the domain boundary rule is authoritative.
  Advisory finding is noted for awareness only; no action required.

---

## Test Baseline

| Snapshot | Tests Passing | Lint |
|----------|--------------|------|
| Phase 0 baseline (pre-implementation) | 653 (on PR #14 branch) | 17/17 |
| Phase 6 final (all phases complete) | 660 | 17/17 |

**Δ Tests added:** +7 new tests in `test_phase18_manifest_completeness.py`

---

## Deliverables Summary

| Finding | Resolution | File(s) |
|---------|-----------|---------|
| B-2 | `on_demand_only: true` in AVATAR-RAG-INDEX.yaml | `avatars/AVATAR-RAG-INDEX.yaml` |
| H-1 | ENG-3.7, ENG-5.5, ENG-7.1 example files + manifest pointers | `examples/ENG-3.7-*.md`, `ENG-5.5-*.md`, `ENG-7.1-*.md` |
| H-2 | ENG-4.4, ENG-7.2–7.5, ENG-5.2 added to specializes_laws | `manifest.yaml` |
| H-3 | ENG-6.1 topic router index (17 security files) | `examples/ENG-6.1-index.md` |
| H-4 | MISRA C++/DO-278A under ENG-6.x framing | `examples/ENG-6.1-misra-do278a.md` |
| W-1 | RAG evidence file with 5 canonical queries | `hangar-ai-specs/evidence/avatar-rag-cpp.md` |
| W-2 | brownfield-adoption → adoption in manifest | `manifest.yaml` |
| W-3 | 5 canonical queries documented | `avatar-rag-cpp.md` |
| W-4 | Manifest restructure tracked (deferred) | `cpp-avatar-manifest-restructure/PROPOSAL.md` |
| W-5 | Bundled with W-4 (deferred) | — |
| W-6 | skill- prefix removed from activates.skills | `manifest.yaml` |
| W-7 | Resolved by H-1 (ENG-3.7 example created) | — |
| A-1 | JNI bridge skill created | `skill-cpp-jni-bridge.md` |
| A-2 | FAR 117 traceability example | `examples/ENG-4.1-far117-traceability.md` |
| A-3 | Brownfield Entry Path in full-reference | `full-reference.md` |
| A-4 | Skill Decision Tree in full-reference | `full-reference.md` |
| A-5 | Anchor links in guidance.md | `guidance.md` |
| A-6 | Skill naming convention in index.yaml | `development-practices/index.yaml` |
| A-7 | 24 → 25 cpp skills verified | count guards updated |
| A-8 | BLOCKED — domain boundary (V5 guard) | advisory only |

---

## Governance Notes

- Sources: 7-Persona Panel Review + Avatar Workflow Validate Mode assessment (`workflows/avatar-workflow.md`)
- Panel overall verdict at time of review: 🔴 BLOCKED (B-1, B-2)
- B-1 resolved in Phase 17 of parent proposal (commit `c4ab135`)
- B-2 and H-1 through H-4 addressed in this proposal
- Phase 4 output (MISRA/DO-278A) uses ENG-6.x framing only — BUS-* BLOCKED in technology avatars (Safeguard 2)
- Governance approval: Repository owner directed this work — April 13, 2026
- W-4/W-5 (manifest 150-token restructure) deferred to separate PR — tracked in cpp-avatar-manifest-restructure stub

---

## Amendment Log

_No amendments recorded._
