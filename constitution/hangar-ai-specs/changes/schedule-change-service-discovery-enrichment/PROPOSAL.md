# Proposal: Schedule Change Self-Serve Discovery and Agentic Modernization

**Proposal ID:** schedule-change-service-discovery-enrichment  
**Submitted:** March 11, 2026  
**Status:** In Execution (Constitutional Discovery Track)  
**Scope:** Multi-repo codebase spanning 6+ services across UI, BFF, eligibility, history, and reservation layers  
**Complexity Level:** High (distributed system, multiple service boundaries, complex booking state machine)

---

## Executive Summary

Schedule Change Self-Serve is a multi-service platform that enables customers to modify flight reservations without agent intervention. It spans customer-facing UI, backend federation (BFF), eligibility determination, reservation history, and booking execution across multiple systems.

**Current State:**
- 6 active repositories with distributed service ownership
- Eligibility rules deeply coupled with reservation state
- Limited observability and metrics instrumentation
- Manual intervention required for complex change scenarios
- No consolidated product discovery package

**Proposed Outcome:**
Create a **constitutional discovery package** that:
1. Maps current service architecture against Hangar AI constitution
2. Identifies feature gaps and agentic intervention opportunities
3. Provides experimental baselines for product metrics (time-to-change, success rate, manual override frequency)
4. Delivers phased modernization roadmap with vertical-slice delivery
5. Surfaces governance and compliance requirements (passenger communication, audit trails, fraud prevention)

**Deliverables:**
- Constitution-aligned product avatar for Schedule Change
- 5 completed discovery worksheets (metrics, personas, codebase, domain model, agentic workflows)
- Comprehensive discovery spec with gap analysis
- Executive handoff document for Bhavita's product team
- Agentic experimentation plan with 3-month pilot roadmap
- Implementation tracking artifacts (`TASKS.md`, `PROGRESS.md`) for transparent execution

---

## Constitutional Guides and Workflow Assets

This change executes using the Constitution's artifact-driven workflow and templates:

**Hangar SDD Workflow Sequence:**
1. `PROPOSAL.md` (intent, scope, law alignment)
2. `TASKS.md` (implementation plan with checkable execution steps)
3. `PROGRESS.md` (live phase status and evidence trail)
4. `SPEC.md` and `MASTER_SPEC.md` (consolidated outputs)
5. `worksheets/` artifacts (evidence inputs)

**Guides and Templates Applied:**
- `docs/guides/avatars/product-taxonomy-governance.md` (5-gate taxonomy validation)
- `docs/guides/avatars/product-avatar-guide.md` (avatar structure quality)
- `docs/guides/avatars/law-citation-guide.md` (law traceability)
- `docs/templates/enrichment/01-metrics-collection.md` (metrics evidence worksheet)
- `docs/templates/enrichment/02-persona-validation.md` (persona evidence worksheet)
- `docs/templates/enrichment/03-codebase-assessment.md` (service/code evidence worksheet)
- `docs/templates/enrichment/04-domain-model-inventory.md` (domain model evidence worksheet)
- `docs/templates/enrichment/05-agentic-workflow-discovery.md` (agentic pilot selection workflow)

### Evidence Triangulation Protocol (Required)

All discovery claims in worksheets and roadmap artifacts must carry an evidence source tag and confidence level.

**Evidence tags:**
- `code-evidenced`: verified from repository code, contracts, or telemetry implementation
- `field-study`: validated from interviews, observations, call logs, or user research artifacts
- `public-benchmark`: sourced from publicly available competitor or industry material
- `stakeholder-reported`: reported by product/engineering/support stakeholders, not yet independently verified
- `hypothesis-only`: informed assumption pending validation

**Confidence levels:** `high`, `medium`, `low`

**Public domain field study requirement:**
- Collect directional competitor and industry evidence (public sources only)
- Record source URL/title/date and clearly mark it as directional, not authoritative internal telemetry
- Use benchmark data to augment prioritization, not to replace internal measurement

**Roadmap proposal carry-forward rule:**
Every discovery roadmap proposal must include:
1. Evidence ledger summary (counts by source tag)
2. List of hypothesis-only metrics that require instrumentation
3. Public benchmark appendix with citations

### End-to-End Execution Loop (Required)

This change follows a stage-gate loop so discovery outputs can be continuously tightened from hypothesis to measured truth:

1. **Stage A: Initialize**
  - Set experimental baselines and source tags in worksheets
  - Define confidence level per metric/claim

2. **Stage B: Public Field Study**
  - Add competitor and industry directional references
  - Do not convert directional references into internal KPI truth

3. **Stage C: Code Evidence Pass**
  - Validate service path, contracts, retries, and observability points from repositories
  - Reclassify claims to `code-evidenced` where proof exists

4. **Stage D: Internal Field Validation**
  - Validate with product, analytics, UX, support, and operations workshops
  - Reclassify claims to `field-study` or `stakeholder-reported` as applicable

5. **Stage E: Metric Rebaseline Gate**
  - Update numeric baselines only when internal telemetry or validated field evidence exists
  - Keep values unchanged if evidence remains directional only

6. **Stage F: Roadmap Lock**
  - Publish SPEC and MASTER_SPEC with evidence ledger and confidence profile
  - Freeze Slice 1 priorities based on highest-confidence signals

---

## Problem Statement

Schedule Change Self-Serve operates under several constraints:

1. **Complex eligibility logic** - Tie rules, fare basis, PNR state, airline policies all factor into what changes are allowed
2. **Multi-system orchestration** - Changes must be validated against reservations, pricing, inventory, and compliance systems
3. **Limited customer visibility** - Reasons for ineligibility are opaque; manual agent involvement often required
4. **Slow change execution** - From eligibility check to rebooking completion can take 30-90 seconds
5. **High manual intervention** - Estimated 15-25% of attempted changes require agent assistance
6. **No agentic layer** - Customers can't have conversational help understanding eligibility or exploring alternatives

**Why This Matters:**
- Each manual intervention removes 30-50 customers/hour capacity from check-in agents
- Abandoned change requests contribute to involuntary denied boardings (DOC) incidents
- Competitor platforms offer immediate, transparent, conversational change guidance
- Service Recovery org wants to eliminate step-by-step wizards and enable natural interaction

---

## Solution Approach

Four-phase engagement following Hangar AI Constitution patterns:

### Phase 1: Constitution Enrichment - Avatars & Skills ✅ (Concurrent with Team Intake)

Create/enrich Schedule Change domain structures in the constitution:

**Product Avatar Creation:**
- `avatars/product-type/schedule-change-self-serve/`
  - Manifest with service inventory, personas, business metrics
  - Guidance document with eligibility rules, system constraints
  - Use cases (mobile change, agent-assisted escalation, group rebooking)
  - Law mapping (PRD-1.1 through PRD-5.1, ENG-6.1 through ENG-10.1, BUS-3.1 through BUS-4.3)

**Skill Activation:**
- skill-spec-governance (orchestration)
- skill-02-user-journey-mapping (customer flows)
- skill-04-business-domain-modeling (eligibility rules)
- skill-05-business-rules (tie rules, fare rules, policy rules)
- skill-12-api-design (current API surface)
- skill-13-observability (instrumentation plan)
- skill-21-prompt-engineering (agentic conversational patterns)
- skill-23-ai-agents (agent design for eligibility and rebooking)

**Technology Avatar Association:**
- technology-java-21-spring-boot (backend services)
- technology-react-typescript (Schedule Change UI)
- technology-azure-cosmos-db (reservation state store)
- technology-apigee-api-gateway (partner APIs)
- technology-event-streaming (audit trail)

### Phase 2a: Team-Led Workshops - People Knowledge (3 sessions, ~4 hours)

**Pre-fill Worksheets** with service architecture diagrams, current personas, and sample metrics from SD/UR interviews or product roadmap. Team validates/corrects.

| Session | Worksheet | Duration | Attendees | Output |
|---------|-----------|----------|-----------|--------|
| 1 | Metrics Collection | 1.5 hr | Product Owner + Analytics Lead | Real KPIs by tier (customer satisfaction, change success rate, time-to-change, manual override frequency) |
| 2 | Persona Validation | 1 hr | Product Owner + UX Researcher | Validated personas: leisure traveler, busy professional, group/team lead, loyalty member |
| 3 | Agentic Workflow Discovery (Pilot Selection) | 1.5 hr | Full team (PM, tech lead, Hangar Labs) | Prioritized pilots, success criteria, blockers |

**What's Pre-Filled (Hangar Labs Prep):**
- Metrics worksheet: Templated KPIs with experimental baselines from architecture constraints and similar platforms
- Persona worksheet: Initial segmentation based on product roadmap/UR insights
- Codebase/domain worksheets: Filled autonomously via repo analysis

### Phase 2b: Autonomous Analysis - Code Knowledge (2-3 days, No Team Time)

Hangar Labs scans 6 core Schedule Change repositories:

| Repo | Analysis | Output |
|------|----------|--------|
| schedule-change-ui | UI framework, component patterns, feature flags | UX flow diagrams, tech debt inventory |
| schedule-change-bff | Federation layer, orchestration logic, error handling | Service call graph, latency breakdown, failure modes |
| schedule-change-eligibility-service | Eligibility rules engine, tie/fare logic | Business rule inventory, decision tree, constraint model |
| schedule-change-reservation-history-service | Change history and audit trail | Data model, audit completeness, compliance coverage |
| drss-schedule-change-reservation-service | Rebooking and seat assignment | Booking state machine, conflict resolution patterns |
| ServiceRecovery-Product-Wiki + architecture docs | Current design decisions, known constraints | Architecture validation (what's real vs. aspirational) |

**Worksheets Filled:**
- W3: Codebase Assessment (service inventory, dependencies, test coverage, deployment topology)
- W4: Domain Model Inventory (entities, aggregates, events, business rules in code)
- W5 (Partial): Agentic Workflow Discovery (code change patterns, error hotspots, integration points)

**Stage C Task Definition (Code Evidence Pass):**
- C1. Verify local availability/access for all in-scope repositories
- C2. Build end-to-end service call graph (UI -> BFF -> eligibility -> reservation -> history/remarks)
- C3. Extract API contracts and key DTO/request-response boundaries
- C4. Identify retry/idempotency/fallback paths and failure amplification points
- C5. Extract current observability instrumentation points and telemetry gaps
- C6. Map audit event emission points and compliance-critical fields
- C7. Reclassify worksheet claims from `hypothesis-only` to `code-evidenced` where proof exists
- C8. Publish Stage C judicial review with findings, confidence, and rulings

### Phase 3: Discovery Package Consolidation (1 day)

Create 5 worksheets + 2 comprehensive specs:

**Worksheets** (in `worksheets/`):
1. `01-metrics-collection-schedule-change.md`
2. `02-persona-validation-schedule-change.md`
3. `03-codebase-assessment-schedule-change.md`
4. `04-domain-model-inventory-schedule-change.md`
5. `05-agentic-workflow-discovery-schedule-change.md`

**Specs**:
- `SPEC.md` - Technical consolidation, current-state metrics baselines, candidate agentic workflows
- `MASTER_SPEC.md` - Product team handoff (gaps, feature proposals, targets)
- `AGENTIC_EXPERIMENTATION_PLAN.md` - 3-month pilot charters with success criteria

### Phase 4: ADO Discovery Document Validation (Upon Receipt)

When Bhavita's team shares the ADO discovery doc:
1. Cross-check against code findings for disconnects
2. Identify if ADO contains better requirements, personas, or metrics
3. Merge or override source code findings with higher-confidence ADO data (if present)
4. Report alignment and gaps in a reconciliation document

---

## Constitutional Alignment

### Laws Referenced

**Product Laws (PRD):**
- [PRD-1.1](../../../laws/product/discovery.md) Continuous Discovery — Multi-method research across personas
- [PRD-2.1](../../../laws/product/discovery.md) Problem Validation — Validate ineligibility pain points with passengers
- [PRD-2.2](../../../laws/product/discovery.md) Assumption Mapping — Document tie rules, fare rules, policy constraints
- [PRD-2.3](../../../laws/product/discovery.md) Jobs-to-be-Done — Frame as "I need to change my flight" not "I need to re-input details"
- [PRD-2.4](../../../laws/product/discovery.md) Competitive Analysis — Compare to United, Delta, Southwest, Expedia self-serve capabilities
- [PRD-3.1](../../../laws/product/roadmap.md) Roadmap Planning — Vertical-slice delivery of eligibility → rebooking → conversational agent
- [PRD-4.1](../../../laws/product/roadmap.md) MVP Definition — First slice: real-time eligibility with clear reason codes
- [PRD-5.1](../../../laws/product/metrics.md) Success Metrics — Time-to-change, success rate, manual override frequency, NPS delta

**Engineering Laws (ENG):**
- [ENG-2.3](../../../laws/engineering/foundations.md) Vertical Slice Development — Four slices: eligibility → history → rebooking → conversational agent
- [ENG-4.1](../../../laws/engineering/testing.md) Atomic TDD — Test-first for eligibility rule changes
- [ENG-6.1](../../../laws/engineering/security.md) Security by Design — PII handling in change requests, audit trail, fraud detection
- [ENG-6.4](../../../laws/engineering/security.md) Compliance and Audit Trail — Record all eligibility decisions, human overrides
- [ENG-6.7](../../../laws/engineering/security.md) Observability — Instrument eligibility decision points, rule execution time
- [ENG-9.4](../../../laws/engineering/governance.md) Human Override Law — Agent approval gate for high-risk conversational recommendations
- [ENG-10.1](../../../laws/engineering/quality.md) Quality Gates — Per-slice acceptance tests, rollback criteria

**Business Laws (BUS):**
- [BUS-2.6](../../../laws/business/incident.md) Control Framework Law — Who can approve changes, fraud thresholds
- [BUS-3.1](../../../laws/business/compliance.md) Regulatory Compliance — DOT rules on reservation modification
- [BUS-3.2](../../../laws/business/compliance.md) Audit Trail Law — Log all eligibility checks, customer communications
- [BUS-4.1](../../../laws/business/data-governance.md) Data Retention — How long to store failed change attempts, audit logs
- [BUS-4.3](../../../laws/business/data-governance.md) Data Subject Rights — Passenger right to retrieve their change history
- [BUS-7.1](../../../laws/business/risk.md) Risk Stratification — Identify high-risk change scenarios requiring agent review

---

## Success Criteria

1. ✅ Discovery worksheets are completed and review-ready for Schedule Change product owner
2. ✅ Current-state metrics baselines are explicit and marked as experimental
3. ✅ At least 5 agentic workflow candidates are prioritized with impact/feasibility scores
4. ✅ Three pilot opportunities are defined with measurable 30-day outcomes
5. ✅ All constitutional laws are cited with specific example application points
6. ✅ Product team receives executive handoff document + detailed spec + experimentation plan
7. ✅ ADO discovery document (when received) is validated against code findings with gap report
8. ✅ Discovery claims are source-tagged (`code-evidenced`/`field-study`/`public-benchmark`/`stakeholder-reported`/`hypothesis-only`) with confidence levels
9. ✅ Public domain field-study references are captured for competitor/industry directional baselines

---

## Key Risks and Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|-----------|
| Multi-service scope requires deep repo scanning | Phase 2b takes 4+ days; delays discovery | Medium | Parallelize repo clones + pre-stage analysis queries; prioritize BFF + eligibility services first |
| Experimental baselines differ from actual telemetry | Wrong confidence in KPI targets | High | Mark all as "experimental" with explicit instrumentation plan for first sprint; validate in pilot |
| Service Recovery architecture docs conflict with actual code | Misleading recommendations | Medium | Code is source of truth; document all disconnects in validation report |
| ADO discovery doc arrives late | Delays alignment report | Medium | Proceed with code-based discovery; layer in ADO reconciliation asynchronously |
| Agentic workflow pilots require new Azure OpenAI capacity | Blocks pilot execution | Low | Pre-arrange quota with platform team; include in blocker assessment (task 3.1) |
| Customer communication (eligibility explanations) requires legal/compliance review | Delays conversational agent rollout | Medium | Engage Legal + Compliance in workshop 3; draft guidance upfront |

---

## Experimental Baseline Policy

All quantitative values in discovery worksheets are marked as **experimental** because:
- Schedule Change prod telemetry is incomplete or unavailable
- Baselines are estimated from architecture constraints, similar platforms, or SD/UR insights
- Values MUST be replaced by instrumented telemetry in first implementation sprint

**Example baseline approach:**
```
Metric: Average time from eligibility check to rebooking completion
Experimental Baseline: 45 seconds (est. from BFF latency + seat assignment overhead)
Instrumentation Required: Add tracing spans to BFF → eligibility → rebooking services
Validation Cadence: Week 1-2 measure, Week 3-4 compare to baseline, Week 5+ revise targets
```

### Current Rebaseline Decision (2026-03-11)

After initial public-domain field study, numeric KPI baselines are **not** being changed yet.

Reason:
- Public competitor/industry data is directional and confirms prioritization
- It does not provide AA-internal denominator definitions, telemetry fidelity, or cohort equivalence

Action:
- Preserve current experimental values
- Upgrade evidence tags and confidence as code and workshop evidence is collected
- Rebaseline numeric values at Stage E only

---

## Governance Model

**Phase 1 (Avatar Enrichment):** Hangar Labs autonomous, no blocker  
**Phase 2a (Team Workshops):** Async prep by Labs, sync validation with Schedule Change PO, tech lead, UX research  
**Phase 2b (Code Analysis):** Hangar Labs autonomous, no blocker  
**Phase 3 (Consolidation):** Hangar Labs → review draft with Bhavita before finalization  
**Phase 4 (ADO Validation):** Upon receipt, Labs reconciles with code findings, reports to Bhavita  

**Decision Gate:**
- Bhavita approves discovery findings → proceed to Hangar SDD vertical-slice execution (Slice 1: Real-time eligibility)
- If ADO doc conflicts with code findings: escalate to PO + tech lead for alignment before proceeding

### Judicial Review Cadence

To ensure constitutional rigor, execute a judicial review checkpoint:
- After each Stage C milestone (C2, C5, C7)
- At any blocker that prevents evidence collection
- Before updating any numeric KPI baseline

Each judicial review must capture:
1. Question under review
2. Evidence considered
3. Ruling (approved / deferred / blocked)
4. Required corrective action and owner

---

## Timeline

| Phase | Duration | Blocker? | Notes |
|-------|----------|----------|-------|
| Phase 1: Avatar Enrichment | 1 day | No | Hangar Labs creates constitution structures |
| Phase 2a: Team Workshops | 4 hours (async prep + 3 sync sessions) | Yes | Requires 3 team members, 1.5-2 hour windows |
| Phase 2b: Code Analysis | 2-3 days | No | Parallel with Phase 2a; Hangar Labs only |
| Phase 3: Consolidation | 1 day | No | Hangar Labs writes worksheets + specs |
| Phase 4: ADO Validation | 1-2 days (upon receipt) | No | Hangar Labs compares ADO to code findings |
| **Total** | **~5-6 days (3 blocker hours)** | — | Can start today; workshops can be scheduled next week |

---

## Next Actions

1. **Immediate:** Use `TASKS.md` as the authoritative execution checklist for this change
2. **Immediate:** Use `PROGRESS.md` as the live phase dashboard and evidence log
3. **This week:** Schedule 3 team workshops (60 min slots, 1-2 days apart)
4. **Parallel:** Hangar Labs performs autonomous code analysis for W3/W4/W5-partial
5. **Week 2:** Consolidate worksheets and publish `SPEC.md`, `MASTER_SPEC.md`, `AGENTIC_EXPERIMENTATION_PLAN.md`
6. **Upon receipt:** Reconcile ADO discovery doc against code findings (Phase 4)
7. **Approval gate:** Bhavita green-lights findings -> proceed to Slice 1 Hangar SDD vertical-slice execution

---

## Appendix: Scope and Service Inventory (Pre-Filled)

**Schedule Change Core Services:**

| Service | URL | Language | Purpose |
|---------|-----|----------|---------|
| schedule-change-ui | https://github.com/AAInternal/schedule-change-ui | React/TS | Customer-facing wizard + agent console |
| schedule-change-bff | https://github.com/AAInternal/schedule-change-bff | Java 21 / Spring | Backend federation, orchestration, resilience |
| schedule-change-eligibility-service | https://github.com/AAInternal/schedule-change-eligibility-service | Java 21 / Spring | Eligibility rule engine, tie/fare validation |
| schedule-change-reservation-history-service | https://github.com/AAInternal/schedule-change-reservation-history-service | Java 21 / Spring | Change history, audit trail, compliance log |
| drss-schedule-change-reservation-service | https://github.com/AAInternal/drss-schedule-change-reservation-service | Java 21 / Spring | Rebooking execution, seat assignment |
| drss-remarks-service | (Co-owned by Service Recovery) | — | Supports marking passenger remarks during change |

**Supporting References:**
- Architecture Docs: https://github.com/AAInternal/ServiceRecovery-Product-Wiki/tree/main/schedule-change-self-serve/docs/architecture
- Apigee Proxy: schedule-change-eligibility-service-apigee, apigee-schedule-change-history-service

**Out of Scope (AVP/Auction/ACE):**
- Auction suite (pre-removal phase)
- AVP-Ace (agent-based tool, separate modernization)
- service-recovery-reservation (no direct admin access)
