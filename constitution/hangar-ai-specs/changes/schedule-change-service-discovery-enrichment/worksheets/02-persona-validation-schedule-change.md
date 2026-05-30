# Worksheet 02: Persona Validation - Schedule Change Self-Serve

**Purpose:** Validate discovery personas and connect them to measurable outcomes.  
**Law Anchor:** PRD-1.1, PRD-2.1  
**Status:** In Progress (pre-workshop evidence pass complete; workshop validation pending)

---

## Persona Validation Method (PO Explainability)

Personas were not invented from scratch. They were derived and stress-tested using four methods:

1. Product-avatar seed personas from constitutional artifact set (role hypotheses).
2. Code-path role evidence from W3/W4 (who is impacted by rule outcomes, overrides, and audit responsibilities).
3. Exception-pattern alignment (which user/operator absorbs failures in eligibility, remarks, or update flows).
4. Stakeholder signal alignment from operations/compliance assumptions pending workshop confirmation.

Validation scoring model:

$$
	ext{Persona Confidence} = f(\text{Journey Evidence}, \text{Code Evidence}, \text{Operational Signal}, \text{Research Completeness})
$$

Current stage: pre-validation. Final confidence requires workshop and interview artifacts.

---

## Persona Set Under Validation

1. Sam - Leisure Traveler
2. Jordan - Business Traveler (Loyalty-heavy)
3. Morgan - Group Lead / Corporate Coordinator
4. Alex - Airport Agent (override authority)
5. Taylor - Compliance Analyst

---

## Validation Grid

| Persona | Primary Need | Top Pain Point | Evidence Source | Confidence | Validation Needed |
|--------|--------------|----------------|-----------------|------------|-------------------|
| Sam | Fast change options | Ineligibility not explained clearly | Journey hypothesis + reason-code evidence | Medium-Low | 5+ interviews |
| Jordan | Speed + loyalty protection | Upgrade/seat continuity concerns | Journey hypothesis + orchestration complexity evidence | Medium-Low | Frequent traveler interviews |
| Morgan | Atomic group changes | Group splits and repeated manual handling | Journey hypothesis + exception-path evidence | Medium-Low | Corporate travel coordinator interviews |
| Alex | Faster, explainable overrides | Missing rule-context in console | Agent signal + remarks/eligibility rule evidence | Medium | 1-2 observational sessions |
| Taylor | Complete, queryable audit trail | Distributed logging gaps | Compliance signal + history/audit touchpoint evidence | Medium | Compliance review |

---

## What Changed After Code Analysis

1. Persona confidence is now method-backed (not pure hypothesis) for operator personas.
2. Alex and Taylor moved to stronger confidence because override and audit-relevant flows are visible in service code.
3. Customer personas remain Medium-Low until direct interview evidence is captured.

---

## Decision Questions for Workshop

1. Which persona currently drives the highest business risk if ignored?
2. Which persona should define MVP success criteria first?
3. Which assumptions are least reliable and must be validated in the next sprint?
4. Which journeys differ materially between domestic and international traffic?

---

## Acceptance Criteria for Persona Validation

- [ ] At least 5 external or internal user interviews completed
- [ ] At least 1 airport-agent observation session completed
- [ ] Persona priority ranking approved by Product Owner
- [ ] Persona-to-metric mapping agreed for MVP dashboard
