# MASTER_SPEC: Schedule Change Self-Serve Discovery Handoff

**Audience:** Product leadership, engineering leads, compliance stakeholders  
**Status:** Draft for review

---

## Executive Summary

The discovery package establishes a constitutional, evidence-driven foundation for Schedule Change Self-Serve modernization. The domain now has structured artifacts for metrics, personas, code/system analysis, domain model framing, and agentic workflow prioritization.

---

## Constitutional Law References

### Product

1. [PRD-1.1: Continuous Discovery](../../../laws/product/discovery.md)
2. [PRD-2.1: Problem Validation and Journey Framing](../../../laws/product/discovery.md)
3. [PRD-3.1: Roadmap Planning](../../../laws/product/roadmap.md)
4. [PRD-4.1: MVP Definition](../../../laws/product/roadmap.md)
5. [PRD-5.1: Metrics and Success Definition](../../../laws/product/metrics.md)

### Engineering

1. [ENG-2.3: Vertical Slice Development](../../../laws/engineering/foundations.md)
2. [ENG-6.7: Observability](../../../laws/engineering/security.md)
3. [ENG-9.4: Human Override Governance](../../../laws/engineering/governance.md)
4. [ENG-10.1: Quality Gates](../../../laws/engineering/quality.md)

### Business

1. [BUS-3.1: Regulatory Compliance](../../../laws/business/compliance.md)
2. [BUS-3.2: Audit Trail Law](../../../laws/business/compliance.md)
3. [BUS-7.1: Risk Stratification](../../../laws/business/risk.md)

---

## What Is Ready

1. Taxonomy-aligned product avatar with law-mapped guidance
2. Full PRD example set (PRD-1.1 through PRD-5.1)
3. Three core use-case definitions (reason codes, rebooking, conversational assistant)
4. Five worksheet artifacts to capture and validate discovery evidence
5. Live execution tracking via `TASKS.md` and `PROGRESS.md`

---

## Key Product Opportunities

1. Improve ineligibility explanation quality to reduce avoidable escalations
2. Improve orchestration reliability and latency to increase self-serve completion
3. Improve audit event completeness for compliance confidence
4. Introduce conversational guidance only after reliability/compliance preconditions are met

---

## PO Brief: How Baselines and Personas Were Derived

### Metric Baseline Method

Experimental KPI baselines were derived through evidence triangulation, not arbitrary guessing:

1. Code evidence from W3 (service call graph, error/fallback paths, observability maturity).
2. Domain-rule complexity from W4 (eligibility gates, remarks stop-rules, exception pathways).
3. Directional external benchmarks (Delta/Southwest/IATA/JD Power) to calibrate ambition only.
4. Stakeholder operating assumptions where telemetry is not yet instrumented.

Numeric KPI values were intentionally left unchanged after code analysis; only source tags and confidence improved.

### Persona Validation Method

Persona set was validated in a pre-workshop pass using:

1. Avatar-defined persona hypotheses.
2. Code evidence linking personas to actual decision/risk paths (for example, override and audit personas).
3. Exception-flow mapping from W4 to identify who experiences failure or recovery burden.
4. Planned workshop/interview gates for final validation.

Current confidence is strongest for operator personas and provisional for customer personas pending interviews.

---

## Recommended Near-Term Decisions

1. Approve metrics instrumentation scope for immediate implementation planning
2. Confirm stakeholder participation for persona and metrics workshops
3. Approve Pilot A (eligibility explanation assistant, read-only) as first agentic candidate
4. Defer mutation-capable agent behaviors until override and audit controls are validated

---

## Handoff Checklist

- [ ] Product owner sign-off on persona and KPI priorities
- [ ] Tech lead sign-off on service call-graph assumptions
- [ ] Compliance sign-off on audit and override constraints
- [ ] Pilot selection sign-off with success/rollback criteria
