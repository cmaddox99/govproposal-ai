# Slice 1 Implementation Proposal (Draft): Eligibility Transparency and Reason-Code Quality

**Status:** Draft (awaiting workshop validation and PO sign-off)  
**Change Reference:** schedule-change-service-discovery-enrichment  
**Slice Priority:** 1 of 4 vertical slices  
**Planning Horizon:** 8-12 weeks (10-week nominal)

**Law Anchors:** PRD-1.1 (discovery), PRD-5.1 (metrics), ENG-2.3 (vertical slices), ENG-6.7 (observability), ENG-9.4 (human governance), ENG-10.1 (quality gates), BUS-3.1 (fairness), BUS-7.1 (risk stratification)

---

## 1. Problem Statement

### Context
Currently, when a passenger is ineligible for self-serve schedule change, the eligibility service returns one of 12 distinct reason codes (e.g., `UNCONFIRMED_SEGMENTS`, `HL_SEGMENT`, `ACTIVE_IROP_RULE_VIOLATION`, etc.), but:
- The UI displays a generic "ineligible for self-serve rebooking" message without explanation
- Customers don't understand *why* they're blocked or what to do next
- Support team receives avoidable escalations from confused customers
- No guidance on how to resolve the situation (e.g., "confirm segments" vs. "contact agent")

### Evidence Base
- **W2 (Persona Validation):** Sam (customer), Jordan (support agent) persona studies show high confusion during ineligibility flows
- **W3 (Code Assessment):** Service call graph shows eligibility service produces detailed reason enums; UI consumes but doesn't render them
- **W4 (Domain Model):** Exception inventory classified as CRITICAL: "Missing/Invalid Itinerary or Impacted Slice" - reason codes not normalized to user-facing explanations
- **Discovery ADO:** Bhavita's team flagged "reason code quality and transparency" as top customer pain point (alignment with W2/W4 evidence)
- **Pilot A (Experimentation Plan):** Eligibility Explanation Assistant targets ≥20% escalation reduction and ≥1.0 clarity improvement in ineligible cohort

### Success Impact
- Reduce avoidable support escalations by ≥20% in ineligible-flow cohort
- Improve customer clarity score by ≥1.0 point (measured via post-interaction NPS delta)
- Enable Pilot A (read-only conversational assistant) with safe explanation grounding
- Establish foundation for Slice 2 (audit completeness + rule transparency)

---

## 2. Proposed Solution

### Solution Design: Two-Track Approach

**Track A: Reason-Code Normalization and UI Enhancement (Autonomous)**
- Consolidate 12 distinct eligibility reason codes into 4 human-readable explanation categories:
  1. **"Booking Not Confirmed"** (maps to: `UNCONFIRMED_SEGMENTS`, `SLICE_HAS_UNCONFIRMED_SEGMENTS`)
  2. **"Schedule Already Fixed"** (maps to: `ACTIVE_IROP_RULE_VIOLATION`, `HL_SEGMENT`, `AA20_MARKED`)
  3. **"Booking Not Eligible"** (maps to: `NON_AA_PRIME_CARRIER`, `O_D_MISMATCH`, rule-based disqualifications)
  4. **"System Issue"** (maps to: `MISSING_ITINERARY`, `INVALID_IMPACTED_SLICE`, service errors)
  
- Create explanation templates for each category:
  - "Your booking isn't confirmed yet. Please check your email for confirmation details and try again after confirmation."
  - "Your flight is already part of an active disruption recovery. An agent will contact you with rebooking options."
  - "Your booking doesn't qualify for self-serve rebooking. Please contact reservations for assistance."
  - "We're having trouble checking eligibility. Please try again or contact reservations."

- Implement UI enhancement in BFF to:
  - Receive normalized reason code from eligibility service
  - Render user-facing explanation + suggested next action
  - (Optional) Add link to agent escalation with context pre-filled

**Track B: Pilot A Integration (Gated Post-MVP)**
- Optionally integrate Eligibility Explanation Assistant for ineligible customers:
  - Powered by approved reason-explanation mappings (no hallucinations)
  - Read-only mode: provides context and alternatives, does not mutate state
  - Activation gate: Only after Track A achieves ≥90% explanation accuracy in production monitoring

### Architecture Impact (Minimal)
- **Eligibility Service:** No code change (reason codes already emitted; just add mapping metadata file)
- **BFF:** Add reason-code normalization layer + template renderer (1-2 service methods, no new dependencies)
- **UI:** Replace generic message with templated explanation (component enhancement)
- **No API contract breaking changes** (reason codes preserved for internal use; only UI rendering changes)

### Rollback Strategy
- Reason code mapping and UI rendering are self-contained features; can be feature-flagged and disabled independently
- Rollback criteria: If explanation accuracy drops below 90% OR support escalation rate increases instead of decreasing (window: 2-week measurement post-deploy)

---

## 3. Success Metrics and Acceptance Criteria

### Primary Metrics (Pilot A Success Criteria)

| Metric | Target | Measurement | Owner |
|--------|--------|-------------|-------|
| **Escalation Reduction** | ≥20% decrease | Ineligible flow → agent escalation rate (baseline: establish in week 1) | Product Analytics |
| **Clarity Improvement** | ≥1.0 point increase | Post-interaction NPS delta for ineligible customers (5-point scale) | Customer Insight |
| **Unauthorized Mutations** | 0 events | Audit log: eligible-with-error or false-positive eligibility outcomes | Security/Audit |
| **Explanation Accuracy** | ≥90% | Manual spot-check + telemetry: explanation matches actual reason (weekly sample n=20) | Product/Engineering |

### Secondary Metrics (Operational Health)

| Metric | Target | Measurement |
|--------|--------|-------------|
| Reason-code coverage | 100% | % of eligibility responses mapped to normalized category |
| Pilot A activation rate (if enabled) | ≥10% | % of ineligible cohort engaging with explanation assistant |
| Pilot A feedback sentiment | ≥3.5/5 | Customer feedback on explanation helpfulness (post-interaction survey) |
| Support deflection (post-Pilot A) | TBD post-workshop | Escalations fully resolved via assistant (no callback necessary) |

### Exit Criteria
- [ ] Track A (UI + reason normalization) deployed to production
- [ ] All reason codes mapped and tested with ≥90% accuracy for 1 week
- [ ] Escalation rate baseline established and tracked for 2+ weeks
- [ ] PO sign-off obtained (not in autonomy of Slice 1; gate in Section 10)
- [ ] Readiness review passed (legal/compliance, security, operations)

---

## 4. Backlog Scaffolding

### Phase 1: Design & Specification (2 weeks)

#### Story 1.1: Define Reason-Code Normalization Mapping
- **Owner:** Product Manager + Engineering Lead
- **AC:**
  - Reason code mapping document finalized and approved by eligibility service owner
  - All 12 reason codes mapped to one of 4 categories with clear decision logic
  - Fallback behavior defined for unknown reason codes
  - Mapping published as config file in eligibility service repo (JSON/YAML)
- **Dependencies:** None
- **Effort:** 8 story points

#### Story 1.2: Design UI Explanation Components and Copy
- **Owner:** Product Manager + UX/Design
- **AC:**
  - 4 user-facing explanation templates finalized with copy edit and legal/compliance review
  - Call-to-action buttons designed for each template (e.g., "Contact Reservations", "Check Email", "Try Again")
  - A/B test design defined (2-variant comparison: current vs. new explanation)
  - Accessibility review passed (WCAG 2.1 AA standard)
- **Dependencies:** Story 1.1
- **Effort:** 5 story points

#### Story 1.3: Define Explanation Accuracy Measurement Protocol
- **Owner:** Analytics + Engineering
- **AC:**
  - Manual QA checklist created (sample n=20 weekly spot-checks)
  - Automated telemetry added to track reason-code-to-explanation mapping events
  - Alert defined for accuracy drop below 90% (threshold)
  - Dashboard sketch created (mock-up for weekly review)
- **Dependencies:** Story 1.1
- **Effort:** 3 story points

---

### Phase 2: Implementation - Backend (3 weeks)

#### Story 2.1: Add Reason-Code Normalization Service to BFF
- **Owner:** Backend Engineer (BFF team)
- **AC:**
  - New service method `normalizeEligibilityReason(reasonCode): NormalizedReason` created
  - Reason code mapping loaded from config file and cached at startup
  - All 12 codes have explicit mapping; unknown codes default to category 4 ("System Issue")
  - Unit tests: 100% coverage of mapping logic + fallback paths
  - Integration test: eligibility service → BFF → normalized reason (end-to-end)
- **Dependencies:** Story 1.1
- **Effort:** 8 story points

#### Story 2.2: Implement Explanation Template Renderer in BFF
- **Owner:** Backend Engineer (BFF team)
- **AC:**
  - Service method `getExplanationTemplate(normalizedReason, locale): ExplanationResponse` implemented
  - Template retrieves localized explanation text + suggested actions + escalation link
  - Response schema includes: `explanation`, `nextActions[]`, `escalationLink`, `learnMoreUrl`
  - Supports i18n for future locales (at least English, Spanish)
  - Unit tests: 20+ scenarios (all normalized categories + edge cases)
- **Dependencies:** Story 1.1, Story 1.2
- **Effort:** 8 story points

#### Story 2.3: Add Explanation Telemetry and Observability
- **Owner:** Backend Engineer (Platform/Observability team)
- **AC:**
  - Structured logging added: `eligibility_reason_normalized` event with reason code, normalized category, timestamp
  - Metrics emitted: `eligibility_explanation_rendered_total` (counter by category)
  - Metrics emitted: `eligibility_escalation_rate` (gauge by category for alerting)
  - Traces added for slow normalization queries (SLO: p99 < 50ms)
  - Dashboard created: daily reason-category breakdown and escalation tracking
- **Dependencies:** Stories 2.1, 2.2
- **Effort:** 5 story points

---

### Phase 3: Implementation - Frontend (3 weeks)

#### Story 3.1: Update Eligibility Response Component with Explanation Rendering
- **Owner:** Frontend Engineer
- **AC:**
  - New React component `<EligibilityExplanation explanation={explanation} actions={actions} />` created
  - Component renders: explanation heading (category), explanation text, action buttons, optional escalation link
  - Responsive design: mobile (stacked), tablet/desktop (side-by-side with booking details)
  - No additional API calls; explanation provided by BFF in single response
  - Unit tests: rendering, actions, accessibility (axe-core checks)
- **Dependencies:** Story 1.2, Story 2.2
- **Effort:** 8 story points

#### Story 3.2: Implement A/B Test Variant Selection and Tracking
- **Owner:** Frontend Engineer + Analytics
- **AC:**
  - Feature flag created: `show_eligibility_explanation` (default: off during soft launch)
  - Variant allocation logic: 50/50 control (current UX) vs. treatment (new explanation UX)
  - Variant assigned consistently per user session (sticky)
  - A/B test tracking events: `eligibility_screen_viewed`, `explanation_variant_assigned`, `action_clicked`, `escalation_initiated`
  - Analytics dashboard created for variant comparison (escalation rate, clarity NPS, action conversion)
- **Dependencies:** Story 3.1
- **Effort:** 5 story points

#### Story 3.3: Implement Pilot A Integration Hook (Optional/Gated)
- **Owner:** Frontend Engineer (Hangar Labs collaboration)
- **AC:**
  - Conditional rendering: if `enable_pilot_a_assistant` flag is true AND ineligible AND user opts in, show "Get AI Explanation" button
  - Button opens side panel with Pilot A assistant (pre-loaded with reason context)
  - Pilot A assistant response feeds into analytics tracking
  - Feature flag: default off; requires explicit PO/engineering approval to enable
  - Documentation: integration API for Pilot A service (request/response contract)
- **Dependencies:** Story 3.1, Pilot A implementation complete (post-MVP)
- **Effort:** 5 story points (placeholder; defer until Pilot A ready)

---

### Phase 4: Testing & Quality (2 weeks)

#### Story 4.1: End-to-End Testing and QA
- **Owner:** QA Engineer
- **AC:**
  - Integration test suite: 50+ scenarios covering all reason codes → normalized categories → UI rendering
  - Browser compatibility: Chrome, Safari, Firefox (latest 2 versions)
  - Mobile testing: iOS Safari, Android Chrome (manual + automated)
  - Accessibility audit passed (WCAG 2.1 AA, axe-core, manual screen-reader testing)
  - Performance testing: P99 response time < 200ms end-to-end (BFF normalization + rendering)
  - Test results: all green with documented edge cases and known limitations
- **Dependencies:** Stories 2.1, 2.2, 3.1, 3.2
- **Effort:** 8 story points

#### Story 4.2: Canary Deploy and Monitoring
- **Owner:** DevOps + Engineering Lead
- **AC:**
  - Canary deployment: 5% of traffic → 25% → 100% over 3 days
  - Canary alerts configured: error rate > 0.1%, explanation accuracy < 90%, p99 latency > 200ms
  - On-call runbook created: rollback procedures, common issues, escalation path
  - Manual spot-checks: first 10 hours, then 24 hours, then daily for 1 week
  - Success criteria for canary pass: 0 errors, accuracy ≥90%, p99 latency < 200ms
- **Dependencies:** Story 4.1
- **Effort:** 5 story points

#### Story 4.3: Production Validation & Metrics Baseline
- **Owner:** Product Analytics + Engineering
- **AC:**
  - Metrics baseline established: escalation rate, clarity score, explanation accuracy (week 1, n=1000+ ineligible customers)
  - Dashboards operational and reviewed daily by product/engineering lead for 2 weeks
  - Alert threshold set: if escalation rate increases >5% OR accuracy drops <90%, auto-page on-call
  - Weekly review meeting: metrics review + customer feedback + issue log (gating decision for Pilot A activation)
- **Dependencies:** Story 4.2
- **Effort:** 3 story points

---

### Phase 5: Pilot A Readiness (Optional, Post-MVP)

#### Story 5.1: Pilot A Integration and Governance Review (Gated)
- **Owner:** Hangar Labs + Product + Security
- **Pre-requisite:** Slice 1 MVP achieves ≥90% explanation accuracy for 2+ weeks in production
- **AC:**
  - Pilot A interface contract finalized (reason explanation as context input)
  - Human approval gates defined for Pilot A recommendations (if any policy-modifying suggestions)
  - Logging and audit trail for all Pilot A interactions finalized
  - Weekly review schedule established (Product + Eng + Compliance)
  - Go/no-go decision gate executed (separate change proposal or amendment)
- **Dependencies:** Slice 1 MVP production success + Pilot A implementation complete
- **Effort:** (Deferred; separate storyboard for Pilot A enablement)

---

## 5. Resource Plan

### Team Composition (Estimated Full-Time Equivalent)

| Role | Count | Duration | Responsibility |
|------|-------|----------|-----------------|
| **Product Manager** | 1.0 | 10 weeks | Discovery documentation, metrics definition, stakeholder coordination, PO interface |
| **Backend Engineer (BFF)** | 1.5 | 10 weeks | Reason normalization, explanation service, API integration, observability |
| **Frontend Engineer** | 1.5 | 10 weeks | UI component, A/B test harness, Pilot A integration hook, live demo |
| **QA Engineer** | 1.0 | 6 weeks | Test strategy, scenarios, regression suite, canary validation |
| **Analytics Engineer** | 0.5 | 10 weeks | Metrics definition, dashboard, A/B test tracking, week 1 baseline |
| **DevOps / SRE** | 0.5 | 2 weeks | Canary deploy, monitoring, runbooks, on-call support |
| **UX/Design** (optional) | 0.5 | 2 weeks | Explanation template design, A/B variant design, accessibility review |
| **Security/Compliance** (optional) | 0.25 | 2 weeks | Legal review (explanation copy), data handling audit, Pilot A readiness gate |
| **Hangar Labs** (optional) | 0.25 | 4 weeks | Pilot A integration consultation, governance advice |

**Total Effort:** ~62 FTE-weeks (~8-12 weeks elapsed with 1.5-2 team capacity)

### Timeline Estimate

- **Phase 1 (Design & Spec):** Weeks 1-2 (concurrent: PM + UX + Eng leads)
- **Phase 2 (Backend):** Weeks 2-5 (concurrent: normalization + template + observability)
- **Phase 3 (Frontend):** Weeks 3-6 (concurrent: component + A/B test + Pilot A hook)
- **Phase 4 (Testing & Deploy):** Weeks 6-8 (concurrent: E2E testing + canary)
- **Production Validation:** Weeks 9-10 (monitoring, metrics baseline, Pilot A readiness decision)

**Critical Path:** Design → Backend Normalization + Frontend Component → Integration Testing → Canary Deploy → Validation

**Slack:** UX/Design can be compressed to parallel streams; Pilot A integration deferred post-MVP

---

## 6. Dependencies and Risks

### External Dependencies
- **Eligibility Service:** Must expose reason-code mapping endpoint or config file (minimal change, already emits codes)
- **Analytics Infrastructure:** Dashboard and A/B test tracking setup (assumed available; backlog if not)
- **Pilot A Implementation:** Story 5.1 depends on Hangar Labs completing Pilot A service (not in Slice 1 scope, gated post-MVP)
- **Workshop Outputs:** Final metrics targets (clarify score baseline, escalation rate baseline) from stakeholder workshops (Section 10)

### Internal Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| **Reason-code mapping ambiguity** | Medium | Design rework, delayed QA | Completed in Stories 1.1 with cross-team approval; documented decision rationale |
| **Explanation accuracy misses target (< 90%)** | Medium | Rollback required, Pilot A blocked | Weekly spot-checks (Story 1.3); escalation SLA: < 24 hours to resolution |
| **A/B test shows no improvement** | Low | Scope reduction; defer to v2 | Baseline metrics allow for confident statistical testing; decision gate at week 2 |
| **Performance regression (p99 > 200ms)** | Low | Rollback required | Profiling included in Story 2.3; cached mappings reduce latency |
| **Cross-service integration delay** | Medium | Timeline slip (1-2 weeks) | Design finalized pre-implementation (Story 1.1 blocker); early integration testing (Story 2.2) |

### Mitigation Strategy
- **Weekly steering:** Product + Eng lead sync on metrics, blockers, resource constraints
- **Early canary validation:** Metrics visible within hours of deploy, not days
- **Feature flags:** Ability to disable at component level without full rollback
- **Runbooks:** On-call escalation paths and known-issue resolutions

---

## 7. Governance and Approval Gates

### Pre-Slice-1-Start Gates (Section 10)
- [ ] **PO Sign-Off (Task 10.5):** Discovery package approved; Slice 1 prioritization confirmed by stakeholders
- [ ] **Compliance Review:** Legal review of explanation copy for policy compliance (non-discrimination, fairness)
- [ ] **Security Review:** Pilot A integration architecture vetted (no unauthorized mutations, audit trail complete)

### In-Flight Gates (Slice 1 Execution)
- [ ] **Design Approval (Post Story 1.2):** UI templates and reason mapping approved by product and design leads
- [ ] **Feature Flags Operational:** Canary deploy tooling tested and approved by DevOps
- [ ] **Metrics Dashboard Live (Post Story 2.3):** Analytics team confirms baseline tracking and alert thresholds configured

### Post-Prod Gates (Slice 1 Exit)
- [ ] **Accuracy Threshold Met (≥90% for 1 week):** Production spot-checks confirm explanation quality
- [ ] **Escalation Rate Measured (2+ weeks data):** Baseline and improvement trajectory visible
- [ ] **A/B Test Results Reviewed:** Clarity NPS delta ≥1.0 point or documented decision to proceed/iterate
- [ ] **Pilot A Readiness Gate (Story 5.1):** If accuracy ≥90%, decide on Pilot A integration (separate approval)

### Judicial Review Gate (Slice 1 → Slice 2 Progression)
- [ ] **Judicial Review #9 (Autonomous Completion Audit):** W4 domain model complete, Slice 1 proposal validated for governance, resource plan realistic, risks understood
- [ ] **Judicial Review #10 (Workshop Reconciliation):** Stakeholder input incorporated; metrics targets confirmed; legal/compliance gates scheduled

---

## 8. Alternative Approaches (Considered and Rejected)

### Alternative 1: Defer UI Rendering Until Data Infrastructure Ready
- **Rationale:** Wait for full audit event schema and analytics pipeline before shipping explanations
- **Rejection:** Too slow; W2 persona evidence shows immediate customer pain; 12+ weeks delay unacceptable; risk adoption delay for Pilots A/B
- **Selected Approach:** Ship UI rendering now (low-risk); data infrastructure upgraded in Slice 2

### Alternative 2: Implement Reason-Code Normalization in Eligibility Service Instead of BFF
- **Rationale:** Centralize logic, avoid duplication if multiple consumers
- **Rejection:** Eligibility service is non-AA maintained (downstream dependency); API contract change slow; BFF layer is flexible and safe for experiments
- **Selected Approach:** Normalization in BFF; can be refactored to eligibility service post-validation

### Alternative 3: Skip A/B Test; Roll Out 100% Immediately
- **Rationale:** Faster to value; lower operational overhead
- **Rejection:** Violates ENG-10.1 (quality gates) and BUS-7.1 (risk stratification); cannot confidently commit to ≥20% escalation reduction without evidence; could increase escalations if explanations are incorrect
- **Selected Approach:** Canary → A/B test → gradual rollout; measurement gates for Pilot A progression

---

## 9. Success Criteria Summary and Handoff

### Definition of Ready (Pre-Start)
- [x] Discovery evidence consolidated (W1-W5, SPEC, ADO reconciliation complete)
- [x] Problem statement grounded in customer pain and code evidence
- [ ] Reason-code mapping finalized through workshop validation (pending Section 10)
- [ ] UI explanation templates approved by product + design + legal (pending Section 10)
- [ ] Metrics targets confirmed: escalation baseline, clarity baseline (pending Section 10)
- [ ] Resource team assigned and committed (pending PO sign-off)

### Definition of Done (Post-Production)
- [ ] Slice 1 MVP deployed to production
- [ ] Metrics baseline established: escalation rate, clarity score, explanation accuracy (1+ week data)
- [ ] All accuracy threshold gates ≥90% for 1+ week consecutive
- [ ] No critical escalations or audit findings
- [ ] Handoff documentation completed (runbooks, next-phase recommendations, tech debt)
- [ ] Pilot A readiness gate or defer decision documented
- [ ] Go/no-go decision for Slice 2 progression made by PO + engineering lead

### Transition to Slice 2
- Upon completion, Slice 2 (Audit Completeness + Rule Transparency) can begin in parallel
- Slice 2 depends on Slice 1 metrics and exception patterns to prioritize audit fields and rule explanation depth
- Pilot A integration (Story 5.1) may run parallel to Slice 2 if accuracy targets maintained

---

## 10. References and Evidence Trail

### Discovery Worksheets
- [Worksheet 01: Metrics Collection](./worksheets/01-metrics-collection-schedule-change.md) - Baseline KPIs and measurement approach
- [Worksheet 02: Persona Validation](./worksheets/02-persona-validation-schedule-change.md) - Sam/Jordan personas and pain points
- [Worksheet 03: Codebase Assessment](./worksheets/03-codebase-assessment-schedule-change.md) - Service architecture and test inventory
- [Worksheet 04: Domain Model Inventory](./worksheets/04-domain-model-inventory-schedule-change.md) - Domain events, compliance fields, exception severity
- [Worksheet 05: Agentic Workflow Discovery](./worksheets/05-agentic-workflow-discovery-schedule-change.md) - Pilot A and Pilot B specifications

### Consolidation Artifacts
- [SPEC.md](./SPEC.md) - Discovery consolidation and vertical-slice recommendations
- [MASTER_SPEC.md](./MASTER_SPEC.md) - Executive handoff summary
- [AGENTIC_EXPERIMENTATION_PLAN.md](./AGENTIC_EXPERIMENTATION_PLAN.md) - Pilot A/B governance and success criteria

### Supporting Evidence
- [ADO Reconciliation Notes](./ado-input/ADO_RECONCILIATION_NOTES.md) - Alignment with ADO discovery findings
- [Law Citation Audit](./LAW_CITATION_AUDIT.md) - Constitutional law grounding (PRD/ENG/BUS references)
- [Pilot Readiness Check](./PILOT_READINESS_CHECK.md) - Pilot A/B governance validation

### Law References
- **PRD-1.1:** Continuous Discovery (problem validation and evidence collection)
- **PRD-5.1:** Metrics and Success Definition (KPI targets, measurement)
- **ENG-2.3:** Vertical Slice Development (incremental delivery, prioritization)
- **ENG-6.7:** Observability (instrumentation, telemetry, monitoring)
- **ENG-9.4:** Human Override Governance (approval gates, audit trail)
- **ENG-10.1:** Quality Gates (testing, validation, rollback criteria)
- **BUS-3.1:** Regulatory Compliance and Fairness (non-discrimination, audit trails)
- **BUS-7.1:** Risk Stratification (phased rollout, canary deployment)

---

## Appendix A: Reason-Code Mapping Reference (Normalization Table)

| Original Reason Code | Normalized Category | Explanation Text | Next Actions |
|---|---|---|---|
| `UNCONFIRMED_SEGMENTS` | 1: Booking Not Confirmed | "Your booking isn't confirmed yet. Please check your email for confirmation details and try again after confirmation." | [Check Email] [Contact Reservations] |
| `SLICE_HAS_UNCONFIRMED_SEGMENTS` | 1: Booking Not Confirmed | "Your booking isn't confirmed yet. Please check your email for confirmation details and try again after confirmation." | [Check Email] [Contact Reservations] |
| `ACTIVE_IROP_RULE_VIOLATION` | 2: Schedule Already Fixed | "Your flight is already part of an active disruption recovery. An agent will contact you with rebooking options." | [Contact Reservations] [View Status] |
| `HL_SEGMENT` | 2: Schedule Already Fixed | "Your flight is already part of an active disruption recovery. An agent will contact you with rebooking options." | [Contact Reservations] [View Status] |
| `AA20_MARKED` | 2: Schedule Already Fixed | "Your flight is already part of an active disruption recovery. An agent will contact you with rebooking options." | [Contact Reservations] [View Status] |
| `NON_AA_PRIME_CARRIER` | 3: Booking Not Eligible | "Your booking doesn't qualify for self-serve rebooking. Please contact reservations for assistance." | [Contact Reservations] |
| `O_D_MISMATCH` | 3: Booking Not Eligible | "Your booking doesn't qualify for self-serve rebooking. Please contact reservations for assistance." | [Contact Reservations] |
| `TIME_DELTA_INSUFFICIENT` | 3: Booking Not Eligible | "Your booking doesn't qualify for self-serve rebooking. Please contact reservations for assistance." | [Contact Reservations] |
| `RULE_VIOLATION_OTHER` | 3: Booking Not Eligible | "Your booking doesn't qualify for self-serve rebooking. Please contact reservations for assistance." | [Contact Reservations] |
| `MISSING_ITINERARY` | 4: System Issue | "We're having trouble checking eligibility. Please try again or contact reservations." | [Try Again] [Contact Reservations] |
| `INVALID_IMPACTED_SLICE` | 4: System Issue | "We're having trouble checking eligibility. Please try again or contact reservations." | [Try Again] [Contact Reservations] |
| `ELIGIBILITY_SERVICE_ERROR` | 4: System Issue | "We're having trouble checking eligibility. Please try again or contact reservations." | [Try Again] [Contact Reservations] |
| *(Unknown code)* | 4: System Issue | "We're having trouble checking eligibility. Please try again or contact reservations." | [Try Again] [Contact Reservations] |

---

**Document Status:** Draft (Pre-Workshop, Pre-PO Sign-Off)  
**Next Review:** Post-workshop validation (Task 10.4)  
**Expected Approval:** Within 1 week of PO sign-off gate (Task 10.5)
