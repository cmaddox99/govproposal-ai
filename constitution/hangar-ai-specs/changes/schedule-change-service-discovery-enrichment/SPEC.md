# SPEC: Schedule Change Self-Serve Discovery Consolidation

**Change ID:** schedule-change-service-discovery-enrichment  
**Status:** Draft (worksheet-backed, evidence enrichment in progress)

---

## 1. Objective

Produce a code-and-workshop grounded discovery baseline for Schedule Change Self-Serve that can be used to drive vertical-slice delivery decisions.

---

## 2. Scope

In scope:
- Schedule-change customer and agent journeys
- Eligibility, orchestration, rebooking, and audit service boundaries
- Metrics baseline and instrumentation plan
- Candidate agentic workflow pilots with governance guardrails

Out of scope:
- Production code implementation for Slice 1+
- Non-schedule-change service recovery domains

---

## 3. Discovery Inputs

Primary artifacts:
- `worksheets/01-metrics-collection-schedule-change.md`
- `worksheets/02-persona-validation-schedule-change.md`
- `worksheets/03-codebase-assessment-schedule-change.md`
- `worksheets/04-domain-model-inventory-schedule-change.md`
- `worksheets/05-agentic-workflow-discovery-schedule-change.md`

Supporting artifacts:
- Product avatar files under `avatars/product-type/schedule-change-self-serve/`
- Index and RAG routing updates in product avatar registries

---

## 4. Current Findings (Draft)

1. Metrics are directionally useful but mostly experimental, requiring instrumentation before target commitments.
2. Persona set is clear enough for initial prioritization, but evidence confidence remains low pending stakeholder validation.
3. System architecture appears concentrated around BFF orchestration and eligibility rules as the highest leverage points.
4. Audit completeness and explanation quality are key constraints for any future conversational capability.

---

## 5. Vertical-Slice Recommendation

1. Slice 1: Eligibility transparency and reason-code quality
2. Slice 2: Rebooking reliability and audit completeness
3. Slice 3: Conversational eligibility assistant (read-only first)
4. Slice 4: Proactive disruption offers and loyalty-aware optimization

---

## 6. Risks

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Baseline uncertainty | Mis-prioritized roadmap | Instrumentation-first sprint |
| Distributed service complexity | Slow discovery closure | Prioritize BFF + eligibility evidence |
| Compliance uncertainty | Pilot delays | Early Legal/Compliance review gate |

---

## 7. Exit Criteria

- [ ] Worksheet evidence upgraded from hypotheses to measured observations where possible
- [ ] Product and technical stakeholders review findings and priorities
- [ ] Slice 1 backlog candidates defined with measurable acceptance criteria
- [ ] Discovery package approved for implementation planning

---

## 8. Law Citation Matrix

This consolidation spec is grounded in the following constitutional laws:

### Product Laws

1. [PRD-1.1: Continuous Discovery](../../../laws/product/discovery.md)
2. [PRD-2.1: Problem Validation / Journey Context](../../../laws/product/discovery.md)
3. [PRD-3.1: Roadmap Planning](../../../laws/product/roadmap.md)
4. [PRD-5.1: Metrics and Success Definition](../../../laws/product/metrics.md)

### Engineering Laws

1. [ENG-2.3: Vertical Slice Development](../../../laws/engineering/foundations.md)
2. [ENG-6.7: Observability](../../../laws/engineering/security.md)
3. [ENG-9.4: Human Override Governance](../../../laws/engineering/governance.md)
4. [ENG-10.1: Quality Gates](../../../laws/engineering/quality.md)

### Business Laws

1. [BUS-3.1: Regulatory Compliance](../../../laws/business/compliance.md)
2. [BUS-3.2: Audit Trail Requirements](../../../laws/business/compliance.md)
3. [BUS-7.1: Risk Stratification](../../../laws/business/risk.md)
