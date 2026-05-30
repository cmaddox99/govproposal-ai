# Progress: avatar-constitution-lint-extension

**Status:** ⬜ NOT STARTED — Proposal drafted; awaiting prioritization after C++ avatar enrichment completes.  
**Started:** 2026-04-05  
**Last Updated:** 2026-04-05

---

## Status Summary

| Phase | Status | Description |
|-------|--------|-------------|
| Phase 0: Hangar SDD Execution Artifacts | ✅ Complete | `PROPOSAL.md`, `tasks.md`, and `PROGRESS.md` created |
| Phase 1: Rule Infrastructure | ⬜ Not Started | Avatar rules module and test scaffolding |
| Phase 2: Core Validation Rules | ⬜ Not Started | 7 avatar validation rules |
| Phase 3: Integration and Documentation | ⬜ Not Started | CI integration, documentation, sign-off |

**Overall:** SDD planning artifacts established; implementation awaiting prioritization.

---

## Decision Log

No decisions made yet. Key design decisions to resolve during implementation:
- Avatar discovery mechanism (index.yaml vs. directory scan)
- Parity baseline avatars (java-spring, python-fastapi, or configurable)
- Severity levels per rule (CRITICAL vs. WARNING)
- Brownfield exemption mechanism

---

## Recent Updates

- Initial proposal created based on testing strategy review during C++ avatar enrichment session (2026-04-05)
- Proposal includes full implementation context, architecture notes, and 7 proposed rules
- Cross-referenced from c-plus-plus-avatar-enrichment PROPOSAL.md Amendment A

---

## Governance Alignment

- Laws cited per ENG-11.2
- Proposal follows Hangar SDD lifecycle (ENG-11.1)
- Extends existing constitution-lint infrastructure (ENG-10.1)

---

## Immediate Next Steps

1. Complete C++ avatar enrichment proposal first (dependency)
2. Review `avatar_test_helpers.py` output from C++ proposal task 2.7a for design input
3. Begin Phase 1 rule infrastructure when prioritized

---

## Blockers

- Soft dependency on C++ avatar enrichment completion (can develop against java-spring/python-fastapi first, but C++ avatar provides the newest validation target)
