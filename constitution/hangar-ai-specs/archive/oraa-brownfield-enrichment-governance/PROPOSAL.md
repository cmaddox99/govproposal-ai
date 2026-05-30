# Proposal: ORAA Brownfield Enrichment Governance (Prevent Unintended Stack Rewrites)

**Proposal ID:** oraa-brownfield-enrichment-governance  
**Submitted:** March 9, 2026  
**Status:** PROPOSED

---

## Problem

Two ORAA codebases were introduced for brownfield adoption planning:

1. `NP_RAVEN_NCBC` (Network Constructor + Binary Classifier context, with Python, notebooks, and R/H2O assets)
2. `Log_analyzer` (Python Streamlit app using Azure OpenAI)

A developer reported that prior brownfield adoption behavior rewrote R/PySpark logic into generic Python patterns. That is a constitutional risk because brownfield work must preserve intent, behavior, and operational constraints unless explicitly approved.

### Why this can happen

The current constitution has strong **general** skills and several technology avatars, but there are key domain-specific coverage gaps:

- No product avatar for ORAA-style network planning optimization workflows
- No technology avatar for Streamlit-based internal LLM analytics tools
- No technology avatar for legacy ML brownfield patterns (R + notebook + PySpark/interop) with explicit non-rewrite constraints
- Several product-type entries are adoption-only documents, not full avatar packs (manifest/guidance/use-case), which can weaken routing precision

### Impact

Without these enrichments, retrieval may over-index on generic Python/FastAPI or generic ML conventions and underrepresent legacy constraints, increasing the chance of:

- Unapproved language migration
- Behavioral regressions in model calibration/threshold logic
- Loss of lineage and reproducibility in analytics workflows
- Erosion of stakeholder trust in brownfield AI assistance

---

## Root-Cause Position on the R/PySpark Rewrite Concern

**Is that possible due to missing enrichment?** Yes, it is possible and plausible.

Missing enrichment is not the only cause, but it is a strong contributor when routing has no precise product/technology context for the repo. In that vacuum, the agent defaults to strongest nearby priors (often modern Python service patterns), which can produce inappropriate rewrites.

This proposal treats that as a governance and context-precision gap and introduces explicit controls to prevent recurrence.

---

## Taxonomy Governance Position

Product-type avatars must remain capability-based. Team or org labels (for example, ORAA or Data Engineering) are not valid product taxons and MUST be rejected as product-type proposals.

### Taxonomy Rules

1. Product-type avatars represent durable business capabilities.
2. Team/org labels are rejected as product taxons.
3. Technology concerns map to technology avatars.
4. Reusable procedures map to skills.

### Taxonomy Gates (Required)

1. Domain gate: independent business capability.
2. Journey gate: distinct user/operator journeys.
3. Boundary gate: no overlap with existing product avatars.
4. Stability gate: remains valid if org chart changes.
5. Retrieval gate: improves RAG routing precision.

---

## Solution

Create a brownfield enrichment package and enforce taxonomy + non-rewrite safeguards in Constitution artifacts.

### Phase 1: Product Avatar Enrichment (ORAA Network Planning)

Create a full product avatar for network planning optimization workflows:

- Scope: itinerary generation quality, junk-itinerary classification, calibration lifecycle, handoff boundaries
- Include: `manifest.yaml`, `guidance.md`, personas, and one operational use-case
- Law specialization focus:
  - PRD-1.1 (Discovery)
  - PRD-2.1 (Journey)
  - PRD-3.1 (Roadmap)
  - PRD-5.1 (Metrics)
  - BUS-3.1 (Data governance)
  - BUS-7.1 (Auditability)

### Phase 2: Technology Avatar Enrichment (Streamlit Internal LLM Tools)

Create a full technology avatar for Python Streamlit internal analytics tools:

- Scope: prompt-governed comparison tools, deterministic parsing, alerting UX, container runbooks
- Include: `manifest.yaml`, `guidance.md`, examples for testing and validation
- Law specialization focus:
  - ENG-4.1 (Atomic TDD)
  - ENG-6.5 (Input validation)
  - ENG-6.1 (Security/secret handling)
  - PRD-3.4 (Usability/accessibility for internal users)

### Phase 3: Technology Avatar Enrichment (Legacy ML Brownfield Interop)

Create a full technology avatar for legacy ML modernization with strict compatibility controls:

- Scope: R/notebook/PySpark coexistence, interop boundaries, migration gates
- Include explicit policy statements:
  - No language rewrite by default
  - Preserve behavior before modernization
  - Require equivalence evidence before any migration
  - Require stakeholder approval for language conversion
- Law specialization focus:
  - ENG-1.3 (Maintainability, intentional refactoring)
  - ENG-4.2 (Tests define behavior)
  - ENG-5.1 (Delivery governance)
  - BUS-6.1 (Risk management)

### Phase 4: Brownfield Guardrails in Adoption Guides

Update brownfield adoption guides to include mandatory pre-flight checks:

1. Detect source language/runtime profile (R, PySpark, notebook, Python, JVM)
2. Verify matching product + technology avatars exist
3. Apply default policy: preserve stack unless migration objective explicitly approved
4. Require a parity plan (tests/outputs/metrics) before any stack transformation

---

## Deliverables

### New Avatars

1. `avatars/product-type/network-planning-optimization/`
2. `avatars/technology/python-streamlit/`
3. `avatars/technology/legacy-ml-interop/`

Each includes at minimum:

- `manifest.yaml`
- `guidance.md`
- `examples/`

### Registry and RAG Updates

1. Update `avatars/index.yaml`
2. Update `avatars/product-type/index.yaml`
3. Update `avatars/AVATAR-RAG-INDEX.yaml`

### Governance Updates

1. Update brownfield adoption guide(s) in `docs/guides/adoption/`
2. Add non-rewrite default and migration-gate criteria
3. Add reusable taxonomy governance skill in discovery-research domain
4. Add taxonomy governance guide and enrichment workflow guide
5. Update AGENTS retrieval protocol so enrichment requests always load these assets

---

## Success Criteria

| Criteria | Target |
|---|---|
| Team/org labels accepted as product taxons | 0 |
| Product avatar coverage for ORAA network planning | 1 full avatar added |
| Tech avatar coverage for Streamlit internal tooling | 1 full avatar added |
| Tech avatar coverage for legacy ML interop (R/PySpark/notebook) | 1 full avatar added |
| Brownfield guide includes explicit no-rewrite default policy | Yes |
| Brownfield guide includes migration approval and parity gates | Yes |
| Enrichment routing loads taxonomy skill + guides | Yes |
| Pilot dry-run on `NP_RAVEN_NCBC` does not suggest language rewrite by default | Pass |

---

## Non-Goals

1. Immediate code migration for ORAA repos
2. Immediate conversion of all adoption-only product folders into full avatars
3. Introducing product-specific skills (skills remain general by model design)

---

## Dependencies

1. ORAA engineering validation on domain terminology and constraints
2. Access to representative brownfield scenarios for acceptance testing
3. Reviewer alignment on migration-gate policy language

---

## Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Overfitting avatars to one team | Keep laws and patterns reusable; keep repo specifics in examples/use-cases only |
| Governance added but not enforced | Add brownfield checklist in guides and require during adoption kickoff |
| Ambiguous migration intent from users | Require explicit migration objective and approval artifact |

---

## Open Questions

1. Should PySpark-specific conventions be first-class in `legacy-ml-interop`, or split into a dedicated technology avatar later?
2. Do we want a required migration approval template in Hangar SDD for any language conversion request?
3. Which ORAA stakeholders should co-own acceptance criteria for parity validation?

---

## References

- `NP_RAVEN_NCBC/README.md`
- `NP_RAVEN_NCBC/BC/README.md`
- `Log_analyzer/README.md`
- `Log_analyzer/app.py`
- `Log_analyzer/llm_utils.py`
- `avatars/index.yaml`
- `agent-skills/skills-by-domain/ml-ai/index.yaml`
