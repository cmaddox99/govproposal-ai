# ADO Reconciliation Notes: Schedule Change Discovery

**Source Document:** `Schedule Change_Discovery.docx`  
**Source Team:** Bhavita (ADO + Microsoft Copilot discovery)  
**Reconciliation Date:** 2026-03-11

---

## Intake Confirmation

- ADO discovery document received and stored at:
  - `openspec/changes/schedule-change-service-discovery-enrichment/ado-input/Schedule Change_Discovery.docx`
- Document content was converted to text for analysis and compared against W1/W3/W4 findings.

---

## ADO Summary (Extracted)

Top hidden problem clusters identified in ADO backlog synthesis:

1. Eligible customers blocked from self-service due to misclassification.
2. Alternate-flight selection UX is unclear/incomplete and drives drop-off.
3. SC architecture fragility due to tightly coupled, error-prone services.
4. Limited analytics/observability for behavior and reliability diagnosis.
5. Complex disruption handling is inconsistent (connection/time/airport/routing/XPT scenarios).

ADO proposed method pattern:

- Understand -> Ideate -> Prototype -> Test -> Decide
- Outcome focus with KR-oriented framing
- Slicing recommendations for implementation increments

---

## Alignment With Current OpenSpec Discovery

### Strong Alignment

1. **Eligibility correctness as top priority**
   - ADO and our W4 both emphasize misclassification and rule-path correctness.
2. **Reliability and resilience focus**
   - ADO architecture fragility aligns with W3 resilience/fallback evidence and Stage C reliability findings.
3. **Observability gap**
   - ADO analytics gap aligns with W1 instrumentation plan and W3 observability evidence/gaps.
4. **Complex disruption scenarios**
   - ADO scenarios align with W4 rule categories and exception path mapping.
5. **Outcome-driven slicing**
   - ADO slicing guidance aligns with constitutional vertical-slice roadmap direction in proposal/spec artifacts.

### Partial Alignment / Refinement Needed

1. **KPI numbers in ADO narrative**
   - ADO includes directional percentage expectations; our governance requires numeric baselines to remain provisional until telemetry and field validation complete.
2. **Persona depth**
   - ADO content is heavily problem/flow focused; we maintain explicit persona validation gates in W2 before final confidence elevation.
3. **Contract and service-boundary precision**
   - ADO is stronger on product framing; W3 remains stronger on concrete endpoint/service contract evidence.

### Divergence

1. **Evidence governance rigor**
   - OpenSpec artifacts enforce source-tag/confidence taxonomy per claim; ADO doc does not consistently label source confidence.
2. **Judicial checkpoints**
   - OpenSpec execution includes judicial review gates for blockers and evidence quality; this governance pattern is not explicit in ADO narrative.

---

## Confidence Upgrade Decision

1. **Roadmap confidence:** Increased to **high** for priority direction (eligibility + reliability + observability + complex-scenario handling).
2. **Numeric KPI confidence:** Remains **provisional** pending telemetry instrumentation and workshop confirmation.
3. **Persona confidence:** Operator personas remain stronger than customer personas until interview evidence is completed.

---

## Merge Actions Applied

1. Accept ADO problem framing as validated directional input.
2. Preserve existing numeric KPI lock policy (no rebaseline yet).
3. Carry ADO opportunity framing into upcoming workshop packet (Tasks 4.1-4.3).
4. Keep W3/W4 code evidence as source of truth for technical boundary and rule precision.

---

## Recommended Next Actions

1. Run workshop sequence (metrics, persona, workflow prioritization) with ADO findings as discussion seed.
2. Complete compliance-required field mapping in W4.
3. Execute law-citation completeness sweep (Task 6.1).
4. Open Slice 1 implementation proposal after PO sign-off.
