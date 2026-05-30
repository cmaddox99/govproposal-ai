# Panel Review Prompt

**Issued:** April 25, 2026  
**Session:** `cpp-version-sensitivity-analysis` discovery session  
**Target:** `hangar-ai-specs/changes/cpp-ref-file-rightsizing/PROPOSAL.md` + `tasks.md`  
**Branch:** `analysis/cpp-version-sensitivity` @ `7179d10`

---

## Prompt (verbatim)

```
Conduct a multi persona review of this proposal

PERSONAS
Select 9 personas whose expertise collectively covers all of the following
domains, and 3 personas that you determine would add valuable reviews. Give
each a name, role title, and 2-sentence practitioner background.

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
  8. Testing that the results are correct, useful, and accurate from the
     constitution, particularly when getting results for different version
     of C++;

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
```

---

## Context provided to the panel

The following files were read prior to the review:

| File | Purpose |
|------|---------|
| `hangar-ai-specs/changes/cpp-ref-file-rightsizing/PROPOSAL.md` | Primary review target |
| `hangar-ai-specs/changes/cpp-ref-file-rightsizing/tasks.md` | Secondary review target |
| `avatars/AVATAR-RAG-INDEX.yaml` (cpp section) | RAG routing baseline |
| `avatars/technology/cpp/manifest.yaml` | Avatar configuration |
| `avatars/technology/cpp/reference-index.md` | Current routing index |
| `avatars/technology/cpp/ref-legacy-navigation.md` (first 40 lines) | Content sample |
| `hangar-ai-specs/changes/cpp-version-sensitivity-analysis/restructuring-options.md` (lines 1–80) | Source analysis document |

---

## Personas selected

### Assigned (Domains 1–8)

| # | Name | Role | Domain |
|---|------|------|--------|
| 1 | Dr. Anjali Mehta | Principal C++ Language Engineer, ISO C++ WG observer | C++ Technical Correctness |
| 2 | Marcus Webb | Hangar AI Constitution Governance Lead | Constitution Governance |
| 3 | Dmitri Volkov | Senior Staff Engineer — C++98 Legacy Systems / CWR Project | Legacy/Brownfield C++ |
| 4 | Elena Nakamura | Platform Engineering Lead — AI Agent Skills Platform | Platform Engineering |
| 5 | Col. James Okonkwo (ret.) | DO-178C / MISRA C++ Safety Systems Consultant | Safety-Critical Systems |
| 6 | Dr. Priya Sundaram | AI Agent Architecture & RAG Systems Researcher | RAG / AI Agent Architecture |
| 7 | Sofia Chen | Developer Experience Lead — C++ Onboarding | Developer Experience |
| 8 | Dr. Thomas Hart | Testing Correctness Lead — AI-Assisted Code Review | Testing Correctness (Version Accuracy) |
| 9 | Rachel Torres | Cross-Avatar Impact & Constitutional Compliance Auditor | Cross-Avatar Impact |

### Copilot-selected additional personas (Domain 9–11)

| # | Name | Role | Domain |
|---|------|------|--------|
| 10 | Owen Bradley | Test Automation Engineering Lead — Constitution TDD Compliance | TDD Compliance |
| 11 | Dr. Yuki Tanaka | Information Architecture & Technical Writing | Information Architecture |
| 12 | Patricia Osei | Change Management & Organizational Risk | Change Management / Risk |
