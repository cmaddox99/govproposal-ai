# Panel Review Prompt — cpp-version-routing-foundation Governance

**Issued:** 2026-04-25  
**Session:** `cpp-version-sensitivity-analysis` discovery session  
**Target:** `hangar-ai-specs/changes/cpp-version-routing-foundation/governance-decision-record.md`  
**Secondary targets:** `PROPOSAL.md`, `tasks.md` (same change directory)

---

## Prompt (verbatim)

```
Conduct a multi-persona governance panel review of the schema extension decisions
in this governance decision record.

SCOPE
Review the three schema decisions (D1 frontmatter schema, D2 project.yaml declaration,
D3 routing policy block) for:
  - Correctness of the design rationale
  - Identification of risks not already documented
  - Resolution of open questions (OQ-1.1 through OQ-3.3)
  - Readiness for implementation (governance approval or conditional approval)

PERSONAS
Select 9 personas whose expertise collectively covers all of the following domains,
plus 3 personas you determine would add value. Give each a name, role title,
and 2-sentence practitioner background.

  1. C++ technical correctness — ISO C++ standards, multi-tier coverage
     (C++98 through C++23), compiler toolchain knowledge
  2. Constitution governance — schema conformance, ENG-11.x law compliance,
     proposal completeness review
  3. Legacy / brownfield C++ — C++98/03 migration, CWR relevance, herc-odyssey
     relevance, SPEClient (MSVC 6.0) relevance
  4. AI agent architecture — AVATAR-RAG-INDEX.yaml routing, token budget,
     agent-as-router pattern, guidance.md always-loaded behavior
  5. Developer experience — onboarding, project.yaml adoption friction,
     progressive disclosure for version declarations
  6. Safety-critical systems — MISRA C++, DO-178C / DO-278A aviation applicability,
     C++ version impact on certification pathways
  7. Consuming repo perspective — what a team at AA must do to adopt this,
     what's the minimum viable adoption path
  8. Information architecture — YAML schema design, naming conventions,
     field name conflicts, cross-avatar schema consistency
  9. Testing correctness — can the acceptance criteria in tasks.md actually
     validate these decisions, what is missing

PER-PERSONA OUTPUT
For each persona, produce:
  - Review scope statement (1 sentence)
  - Findings tagged 🟢 (positive), 🟡 (warning), 🔴 (blocking)
  - Verdicts on each open question (OQ-x.x) within their domain
  - Per-persona verdict: ✅ PASS | ⚠️ CONDITIONAL PASS | 🔴 BLOCKED

SYNTHESIS
Combine all findings into:
  - Overall panel verdict with rationale
  - Resolution table for OQ-1.1 through OQ-3.3 (each with recommended answer)
  - Blocking issues table (must resolve before implementation)
  - High-priority improvements (address before Phase 1 implementation begins)
  - Advisory improvements (future phases)
  - Governance verdict for each of D1, D2, D3:
    ✅ APPROVED | ⚠️ APPROVED WITH CONDITIONS | 🔴 REJECTED
```

---

## Context Provided to Panel

| File | Purpose |
|------|---------|
| `governance-decision-record.md` | Primary review target — 3 schema decisions + OQs |
| `PROPOSAL.md` | Full proposal context |
| `tasks.md` | Implementation task list |
| `avatars/technology/cpp/manifest.yaml` | Current avatar schema baseline |
| `avatars/technology/cpp/examples/ENG-3.7-error-handling.md` | Sample: high-risk file (C++23) |
| `avatars/technology/cpp/examples/ENG-6.1-thread-safety.md` | Sample: high-risk file (C++17) |
| `hangar-ai-specs/changes/cpp-version-sensitivity-analysis/production-version-survey.md` | AA production reality |
| `hangar-ai-specs/changes/cpp-version-sensitivity-analysis/rag-capability-assessment.md` | RAG architecture context |
