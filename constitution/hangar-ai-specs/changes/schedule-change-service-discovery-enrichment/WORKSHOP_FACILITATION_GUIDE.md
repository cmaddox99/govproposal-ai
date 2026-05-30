# Workshop Facilitation Materials: Schedule Change Self-Serve Discovery

**Status:** Ready for Stakeholder Engagement  
**Prepared for:** Three facilitated workshops to validate and prioritize discovery findings  
**Duration:** ~90 minutes each (recommended scheduling: 1 week apart to allow async feedback)  
**Law Anchors:** PRD-1.1 (stakeholder validation), PRD-2.1 (journey context), ENG-2.3 (vertical slice prioritization), BUS-3.1 (fairness)

---

## How to Use These Materials

1. **Before Workshop:** Share pre-read materials (worksheets + evidence summary) with attendees 48 hours prior
2. **During Workshop:** Use agendas, decision templates, and evidence walk-throughs to guide structured discussion
3. **After Workshop:** Capture decisions and divergences in provided decision logs; feed into W1-W5 reconciliation (Task 10.4)

**Facilitator Tips:**
- Start each workshop with 5-min context setting (why discovery matters, what decisions we're making today)
- Use decision templates to make time-boxed choices (avoid open-ended debate)
- Record divergences explicitly (don't smooth over); document alongside decisions
- Close with explicit NEXT STEP and owner assignment

---

## Workshop 1: Metrics Workshop (90 minutes)

**Attendees:** Product Manager, Analytics Lead, 1-2 Business Analysts  
**Goal:** Validate KPI definitions, baseline numbers, calculation formulas, and instrumentation feasibility  
**Pre-Read Materials:** [Worksheet 01: Metrics Collection](./worksheets/01-metrics-collection-schedule-change.md)

### Agenda (90 minutes)

| Time | Activity | Owner | Materials |
|------|----------|-------|-----------|
| 0-5 min | **Welcome & Context** | Facilitator | [Context script](#context-scripts) |
| 5-20 min | **Evidence Walk-Through: Metrics Baseline** | Product | [W1 summary slide deck](#metric-slides) |
| 20-35 min | **Stakeholder Input: KPI Validation** | Analytics | [Decision Template 1.1](#decision-template-11) |
| 35-50 min | **Breakout: Instrumentation Feasibility** | Tech Lead (observer) | [Instrumentation Feasibility Matrix](#instrumentation-feasibility-matrix) |
| 50-75 min | **Workshop: Metric Targets and Baselines** | Product + Analytics | [Decision Template 1.2](#decision-template-12) |
| 75-90 min | **Capture Decisions & Next Steps** | Facilitator | [Decision Log Template](#decision-log-template) |

---

### Context Scripts

**Opening (5 min):**
```
"Today we're validating the metrics baseline for schedule change self-serve discovery. 
We've completed autonomous code analysis and public-domain benchmarking. Your role 
is to ground these metrics in operational reality: 

1. Do these KPIs capture what we should optimize for?
2. Are the baseline numbers realistic given current ops?
3. Can we instrument these metrics within our tech stack?

By end of day, we'll have signed baseline targets that gate Slice 1 execution. 
Any blockers or divergences we surface today can be mitigated in the roadmap."
```

---

### Metric Slides (Evidence Walk-Through)

**Slide 1: Discovery Scope & Source**
- 5 in-scope services (BFF, Eligibility, Reservation History, DRSS Reservation, DRSS Remarks)
- Evidence sources: (1) code analysis (event payloads, logging), (2) public benchmarking (Delta, Southwest, IATA)
- Confidence level: Low → Medium after field study; remains Medium-Low pending instrumentation baseline

**Slide 2: Proposed Customer Metrics Baseline**

| Metric | W1 Baseline | Confidence | Notes |
|--------|------------|----------|-------|
| **Satisfaction (Clarity)** | TBD (hypothesis: 3.2/5) | Low | Reason codes not yet normalized; post-explanation clarity expected 4.0-4.5/5 |
| **Escalation Rate** | TBD (hypothesis: 35% ineligible) | Low | Eligibility service shows 12 reason codes; distribution unknown |
| **Conversion (Successful Rebooking)** | TBD (hypothesis: 60% of eligible) | Medium-Low | Code path exists; high mutation-failure risk identified (Slice 2 priority) |
| **Time-to-Resolution** | TBD (hypothesis: 8 min avg) | Low | No current instrumentation; benchmark: industry 5-10 min |
| **Mobile/Desktop Parity** | TBD (hypothesis: 85% parity) | Low | BFF logs don't segment by device; UI platform assessment pending |

**Slide 3: Operational Metrics (Support & Reliability)**

| Metric | W1 Baseline | Confidence | Notes |
|--------|------------|----------|-------|
| **Escalation Deflection** | TBD (hypothesis: 65% self-serve) | Medium | Pilot A targets ≥20% reduction (new baseline: 78%+) |
| **Error Rate (API)** | TBD (hypothesis: 0.2% eligibility errors) | Medium | Service monitoring in place; accuracy vs. timeout not yet split |
| **Latency (p99)** | TBD (hypothesis: 400ms end-to-end) | Medium | BFF instrumented; downstream service latency distribution TBD |
| **Audit Completeness** | TBD (hypothesis: 60% fields populated) | Low | Pilot B targets ≥99% completeness (new baseline: 99%+) |

**Slide 4: Public Benchmark Comparisons**
- Delta Airlines (estimated): 40% self-serve eligibility, 75% conversion for eligible, 8 min avg resolution
- Southwest Airlines (estimated): 50% self-serve, 70% conversion, 6 min avg resolution
- IATA Industry Average: 45% self-serve, 65% conversion, 7.5 min avg resolution
- Industry NPS for rebooking: 4.2/5 average clarity; post-explanation improvement potential: +0.8 points

---

### Decision Template 1.1

**Workshop Decision Template: KPI Validation**

```
DECISION POINT 1.1: Which metrics should we prioritize for Slice 1?

PROPOSED METRICS (from W1):
□ Satisfaction (Clarity)               → Impact: HIGH (customer friction signal)
□ Escalation Rate (Ineligible Cohort)  → Impact: HIGH (support cost + discovery)
□ Escalation Deflection (% Self-Serve) → Impact: HIGH (Pilot A success signal)
□ Conversion Rate (Eligible Cohort)    → Impact: MEDIUM (Slice 2 priority: mutation robustness)
□ Time-to-Resolution                   → Impact: MEDIUM (SLA tracking)
□ Error Rate / Audit Completeness      → Impact: MEDIUM (Slice 2 priority: reliability + audit)

STAKEHOLDER INPUT:
- Product: [Prioritized metrics for MVP]
- Analytics: [Instrumentation feasibility notes]
- Requirements: [Any add/drop recommendations]

DECISION:
✓ Primary metrics for Slice 1 MVP: _________________________
✓ Secondary metrics to track but not gate: _________________________
✓ Defer to Slice 2: _________________________

OWNER: [Product Lead agrees to baseline measurement plan]
```

---

### Instrumentation Feasibility Matrix

**Matrix to Complete During Breakout (35-50 min)**

| Metric | Data Source (Code? Logs? New Instrumentation?) | Current Availability | Timeline to Instrument | Feasibility | Owner |
|--------|------|------|------|---|---|
| **Satisfaction (Clarity)** | Post-interaction survey or NPS API | Not current | 2 weeks (new survey SDK) | MEDIUM | Analytics |
| **Escalation Rate** | Event stream (BFF → support queue) | Partial (event topic exists) | 1 week (add PII-safe reason code to event) | HIGH | Data Eng + BFF |
| **Escalation Deflection** | Event stream (eligible self-serve vs escalation) | Partial | 1 week (event tagging) | HIGH | Data Eng |
| **Conversion Rate** | BFF + DRSS mutation success events | Partial (success log exists; failure log incomplete) | 2 weeks (add explicit mutation status event) | MEDIUM | DRSS + BFF |
| **Time-to-Resolution** | User session start/end timestamps | Partial (session logs exist) | 1 week (add step-level granularity) | HIGH | BFF + Analytics |
| **Error Rate / Audit** | Service logs + audit event stream | Partial (error logs exist; audit schema incomplete) | 3 weeks (hardened audit event schema) | MEDIUM-LOW | Engineering + Security |

---

### Decision Template 1.2

**Workshop Decision Template: Metric Targets and Baselines**

```
DECISION POINT 1.2: What are our baseline targets and instrumentation scope?

METRICS REQUIRING DECISION:

1. CLARITY (Satisfaction)
   Current Hypothesis: 3.2/5 (low due to generic "ineligible" message)
   Industry Benchmark: 4.2/5 average
   Pilot A Target: ≥1.0 point improvement (target: 4.2+/5)
   
   DECISION:
   ☐ Proceed with Pilot Target (≥4.2/5)
   ☐ Conservative Target (4.0/5 - 80% of Pilot A)
   ☐ Defer instrumentation (measure post-deploy only)
   
   Selected: ______    Owner: ______    Confidence: ____/10

2. ESCALATION RATE (Ineligible Cohort)
   Current Hypothesis: 35% of ineligible escalate to support (high - no explanation)
   Pilot A Target: ≤28% (≥20% reduction)
   
   DECISION:
   ☐ Lock Pilot A target (28%)
   ☐ Two-tier target: Sprint 1 baseline capture (no commitment); Sprint 2 ≥15% reduction
   ☐ Defer metric until Slice 2 (focus on clarity first)
   
   Selected: ______    Owner: ______    Confidence: ____/10

3. CONVERSION RATE (Eligible Cohort)
   Current Hypothesis: 60% of eligible complete self-serve rebooking
   Concern: High mutation-failure risk (W4); critical path for Slice 2, not Slice 1
   
   DECISION:
   ☐ Track but don't gate Slice 1 (Slice 2 priority)
   ☐ Set aspirational target for Slice 1+2 combined: 75% conversion
   ☐ Defer until Slice 2 (too risky pre-mutation-hardening)
   
   Selected: ______    Owner: ______    Confidence: ____/10

4. INSTRUMENTATION INVESTMENT
   Total Estimated Effort: 5-7 PTE-weeks (BFF + Data Eng + Analytics)
   Timeline: Ready for baseline in 3-4 weeks (parallel to Slice 1 prep)
   
   DECISION:
   ☐ Proceed with full instrumentation (all metrics)
   ☐ MVP instrumentation (clarity + escalation rate only; defer audit)
   ☐ Delay instrumentation; use synthetic monitoring for Slice 1 pilot
   
   Selected: ______    Owner: ______    Confidence: ____/10

CAPTURE DIVERGENCES:
If stakeholders disagree on targets or feasibility, document explicitly:
- Divergence: [What do we disagree on?]
- Why: [Reasoning from each stakeholder]
- Path Forward: [Decision rule or escalation point]

Example Divergence:
- Divergence: Analytics wants to defer escalation rate instrumentation (high effort, low signal early); Product wants it day-1 (track Pilot A progress)
- Decision Rule: Proceed with escalation rate tracking; launch with synthetic script, replace with real events by week 2
- Owner: Analytics + BFF leads to synchronize
```

---

### Decision Log Template

**To Complete at Close of Workshop 1**

```
WORKSHOP 1 DECISION LOG (Date: _______) 
Facilitator: _______ | Attendees: _______ | Decision Authority: Product Lead

PRIMARY DECISIONS MADE:
1. KPI Set Selected: [Primary, Secondary, Defer list]
2. Clarity Baseline Target: ___/5 (confidence: __/10)
3. Escalation Rate Target: ___% (confidence: __/10)
4. Conversion Rate Decision: [Track/Gate/Defer] (confidence: __/10)
5. Instrumentation Scope: [Full/MVP/Staged] (timeline: ___ weeks)

DIVERGENCES CAPTURED:
1. [Divergence type]: ___________
   Stakeholders: ____________
   Path Forward: ____________
   Owner: ____________

2. [Divergence type]: ___________
   [...]

NEXT STEPS:
☐ Analytics lead to finalize instrumentation roadmap (by: _____) 
☐ BFF lead to prep event schema updates (by: _____)
☐ Product to socialize targets with Exec team (by: _____)
☐ Metrics reviewed in W1 reconciliation (Task 10.4, by: _____)

FOLLOW-UP REQUIRED:
- [ ] Any: _____________ (Reason: _____)
- [ ] Any: _____________ (Reason: _____)
```

---

---

## Workshop 2: Persona Validation Workshop (90 minutes)

**Attendees:** Product Manager, UX Lead, 1-2 Customer Researchers  
**Goal:** Validate persona priorities, pain points, and measurement mappings  
**Pre-Read Materials:** [Worksheet 02: Persona Validation](./worksheets/02-persona-validation-schedule-change.md)

### Agenda (90 minutes)

| Time | Activity | Owner | Materials |
|------|----------|-------|-----------|
| 0-5 min | **Welcome & Context** | Facilitator | [Context script](#context-scripts-1) |
| 5-15 min | **Evidence Walk-Through: Persona Set** | Product | [W2 summary slides](#persona-slides) |
| 15-35 min | **Stakeholder Input: Persona Validation** | UX Researcher | [Decision Template 2.1](#decision-template-21) |
| 35-55 min | **Workshop: Pain Point Prioritization** | Product + UX | [Pain Point Prioritization Matrix](#pain-point-prioritization-matrix) |
| 55-75 min | **Measurement Mapping Workshop** | Analytics (observer) | [Decision Template 2.2](#decision-template-22) |
| 75-90 min | **Capture Decisions & Next Steps** | Facilitator | [Decision Log Template](#decision-log-template-1) |

---

### Context Scripts

**Opening (5 min):**
```
"Today we're validating personas and pain points for schedule change self-serve. 
We've synthesized W2 evidence (code paths, support data, industry patterns). Your role 
is to ground these personas in real customer/operator research and confirm our pain point 
prioritization aligns with your customer research:

1. Do these personas represent our actual user cohort?
2. Are pain points ranked correctly (what matters most to each persona)?
3. How should we measure success for each persona group?

By end of day, we'll have persona confidence upgraded and measurement dashboard 
requirements finalized. This gates Pilot A design and Slice 2 scope."
```

---

### Persona Slides (Evidence Walk-Through)

**Slide 1: Persona Set Overview**

| Persona | Role | Primary Goal | Confidence | Next Step |
|---------|------|-------------|------------|-----------|
| **Sam** | Customer (leisure traveler) | Self-serve rebooking during disruption | Medium-Low (code + benchmarking only; needs interview) | User interview (n=5-10) |
| **Jordan** | Customer (business traveler) | Quick rebooking + audit trail for expense | Medium-Low | User interview (n=5-10) |
| **Morgan** | Support Agent | Triage escalations + guide ineligible to resolution | Medium-Low | Support feedback sessions (n=3-5) |
| **Alex** | Operations Supervisor | Approve non-standard rebooking + fraud detection | Medium (code evidence: override paths exist) | Ops workshop (n=2-3) |
| **Taylor** | Analytics/Business Analyst | Measure rebooking success + identify problem patterns | Medium (code: audit logging present) | Analytics workshop (n=2-3) |

**Slide 2: Sam (Leisure Customer) - Detailed**

**Profile:**
- Age: 25-45
- Trip Type: Vacation (often groups or families)
- Comfort Level: Medium-tech (smartphone native, but unfamiliar with airline systems)
- Primary Pain Points:
  1. "Why am I blocked?" (ineligibility confusion)
  2. "What do I do now?" (no next-step guidance)
  3. "Will I make my connection?" (time pressure during disruption)
  4. "Do I have to call?" (preference for self-serve)

**Code Evidence Supporting Persona:**
- BFF UI shows generic "ineligible" message (no context)
- Eligibility service produces 12 reason codes but UI doesn't render
- No embedded help text or guidance links
- Support team sees high escalations from ineligible cohort (estimated 35%, W4 evidence)

**Success Criteria (Slice 1):**
- Clarity score: 4.2/5+ (up from est. 3.2)
- Escalation rate: ≤28% (20% reduction from 35%)
- Time-to-decision: ≤5 min (no external contact needed)

**Post-Slice-1 Opportunities:**
- Pilot A: "Explain eligibility" assistant (read-only)
- Slice 3: Conversational rebooking assistant (with alternatives)

---

**Slide 3: Morgan (Support Agent) - Abbreviated**

**Profile:**
- Role: Tier-1 triage + escalation handling
- Pain Points:
  1. "Same questions on repeat" (ineligible customers don't understand)
  2. "Can't resolve self-serve calls" (no reason context in notes)
  3. "Policy compliance uncertainty" (which rules apply?)

**Code Evidence:**
- Support notes (historical) lack structured reason data
- Remarks service emits rule family but SOP doesn't expose to notes
- No audit summary available for agent context

**Success Criteria (Slice 1):**
- Ineligible escalations with clear context (reason + suggested next steps)
- P50 handle time -10% (less repeat questioning)

---

**Slide 4: Confidence Upgrade Path**

```
CONFIDENCE LEVELS (W2 Assessment):

Customer Personas (Sam, Jordan):
  Current: Medium-Low ════════════════════════ (50%)
  Source: Code analysis (UI design) + public benchmark (industry personas)
  Gap: No direct customer research
  Path to Medium/High:
    → Run 5-10 customer interviews (3-week sprint)
    → Validate pain point ranking with NPS/survey (2-week survey)
    → Measure post-Pilot A (clarify score improvement)

Operator Personas (Morgan, Alex, Taylor):
  Current: Medium ════════════════════════════ (60%)
  Source: Code (override patterns, logging schema) + stakeholder feedback
  Gap: Limited ops team interviews (1-2 pilots only)
  Path to High:
    → Run ops workshop (2 hours, n=3-5 agents/supervisors)
    → Shadow one support session
    → Implement ops dashboard metrics

DECISION GATE: Proceed with Slice 1 + Pilot A at current confidence?
OR wait for higher-confidence persona research before implementation?
```

---

### Pain Point Prioritization Matrix

**Exercise (35-55 min): Rank Pain Points by Impact × Urgency**

```
PAIN POINT PRIORITIZATION MATRIX

Plot pain points on 2x2 grid:
Y-axis: Customer Impact (Low → High)
X-axis: Urgency / Frequency (Low → High)

CUSTOMER PAIN POINTS (Sam, Jordan):
1. "Why am I blocked?" (ineligibility confusion)
   → Estimated Impact: 8/10 (high frustration, escalation trigger)
   → Frequency: High (12+ reason codes, ~35% of flows)
   
2. "What do I do now?" (no next-step guidance)
   → Impact: 7/10 (delays resolution)
   → Frequency: High (all ineligibility flows)
   
3. "Will I make my connection?" (time pressure)
   → Impact: 6/10 (anxiety but not service impact)
   → Frequency: Medium (disruption-specific)
   
4. "Do I have to call?" (preference for self-serve)
   → Impact: 5/10 (friction but acceptable escalation)
   → Frequency: Medium (depends on eligibility)

OPERATOR PAIN POINTS (Morgan, Alex):
1. "Same questions on repeat" (ineligible context)
   → Impact: 8/10 (support cost + quality)
   → Frequency: High (35% of calls)
   
2. "No audit trail for compliance" (audit risk)
   → Impact: 7/10 (compliance + fraud risk)
   → Frequency: Medium (overrides only ~5%)
   
3. "Can't detect patterns" (no analytics)
   → Impact: 6/10 (process improvement blocked)
   → Frequency: Medium (analyst-driven, not urgent)

PRIORITIZATION DECISION:
   HIGH-IMPACT, HIGH-URGENCY (ATTACK NOW):
   ☐ "Why am I blocked?" → Slice 1 priority (reason normalization)
   ☐ "Same questions on repeat" → Slice 1 benefit (clarity)
   ☐ "No audit trail" → Slice 2 priority (audit completeness)
   
   MEDIUM-IMPACT (ROADMAP):
   ☐ "What do I do now?" → Pilot A (give suggestions)
   ☐ "Can't detect patterns" → Slice 2 + analytics

STAKEHOLDER DECISIONS:
Product Lead: Confirms pain point ranking? [ Y / N ]
UX Lead: Confirms customer research needed? [ Y / N ]
Support Lead: Confirms operator pain points? [ Y / N ]
```

---

### Decision Template 2.1

**Workshop Decision Template: Persona Validation**

```
DECISION POINT 2.1: Are personas valid and prioritized correctly?

PERSONA VALIDATION CHECKLIST:

☐ Sam (Leisure Customer)
   Validated by: [UX research, support data, other]
   Confidence level: [ Low / Medium-Low / Medium / High ]
   Measurement plan: [NPS survey, interview, other]
   
☐ Jordan (Business Customer)
   Validated by: [UX research, support data, other]
   Confidence level: [ Low / Medium-Low / Medium / High ]
   Measurement plan: [NPS survey, interview, other]
   
☐ Morgan (Support Agent)
   Validated by: [Ops feedback, support data, other]
   Confidence level: [ Low / Medium-Low / Medium / High ]
   Measurement plan: [Ops workshop, shadowing, feedback session]
   
☐ Alex (Operations Supervisor)
   Validated by: [Code evidence, ops feedback, other]
   Confidence level: [ Low / Medium-Low / Medium / High ]
   Measurement plan: [Ops workshop, interview]
   
☐ Taylor (Analytics)
   Validated by: [Code evidence, analytics feedback, other]
   Confidence level: [ Low / Medium-Low / Medium / High ]
   Measurement plan: [Analytics workshop, feedback session]

PRIORITY RANKING:
1st Priority: _____________ (pain point: _____________)
2nd Priority: _____________ (pain point: _____________)
3rd Priority: _____________ (pain point: _____________)
Defer: _____________ (pain point: _____________)

CONFIDENCE UPGRADES NEEDED:
☐ Customer interviews (n=10): [Timeline: ____ weeks]
☐ Support feedback session (n=5): [Timeline: ____ weeks]
☐ Ops workshop (n=3): [Timeline: ____ weeks]
☐ Post-Pilot-A measurement (real data): [Timeline: ____ weeks]

DECISION:
✓ Proceed with Slice 1 + Pilot A at current confidence? [ YES / NO / CONDITIONAL ]
✓ If conditional, what's the blocker? [ _________________ ]

Owner: _________________ | Confidence: ___/10
```

---

### Decision Template 2.2

**Workshop Decision Template: Measurement Mapping**

```
DECISION POINT 2.2: How do we measure success per persona?

MEASUREMENT MAPPING:

SAM (Leisure Customer):
  Pain Point: "Why am I blocked?"
  → Measurement: Clarity score (post-interaction survey, 5-point scale)
  → Target (Slice 1): 4.2/5 (up from 3.2)
  → Owner: Analytics
  
  Pain Point: "What do I do now?"
  → Measurement: Action conversion (% who take suggested next step)
  → Target (Slice 1): TBD (establish baseline first)
  → Owner: Product Analytics
  
  Pain Point: "Escalation avoidance"
  → Measurement: Escalation rate for ineligible cohort
  → Target (Slice 1): ≤28% (down from ~35%)
  → Owner: Support Analytics

MORGAN (Support Agent):
  Pain Point: "Same questions on repeat"
  → Measurement: Avg handle time for ineligible escalations
  → Target (Slice 1): -10% (efficiency gain from pre-fill context)
  → Owner: Support Operations
  
  Pain Point: "No audit trail"
  → Measurement: Audit field completeness (% populated)
  → Target (Slice 2): ≥99% (Pilot B target)
  → Owner: Engineering/Audit

DASHBOARD REQUIREMENTS:
  [ ] Real-time clarity score tracker (ineligible cohort)
  [ ] Escalation rate by reason code
  [ ] Support efficiency metrics (handle time by call type)
  [ ] Audit completeness by service
  [ ] A/B test variant tracking (control vs. new explanation UX)

Owner: Analytics Lead | Confidence: ___/10
```

---

### Decision Log Template

**To Complete at Close of Workshop 2**

```
WORKSHOP 2 DECISION LOG (Date: _______) 
Facilitator: _______ | Attendees: _______ | Decision Authority: Product Lead

PRIMARY DECISIONS MADE:
1. Persona Set Validated: [Sam, Jordan, Morgan, Alex, Taylor all confirmed? Y/N]
2. Priority Ranking: [1st: ___, 2nd: ___, 3rd: ___, Defer: ___]
3. Confidence Levels: [Customer: ___, Operator: ___, Analytics: ___]
4. Measurement Approval: [Dashboard scope? Y/N]

RESEARCH GAPS IDENTIFIED:
1. Customer interviews needed: n=____ (timeline: ___ weeks)
2. Ops feedback needed: n=____ (timeline: ___ weeks)
3. Post-Pilot A measurement: [Yes / No] (timeline: ___ weeks)

DIVERGENCES CAPTURED:
1. [Divergence]: _______________
   Stakeholders: ______________
   Path Forward: ______________
   Owner: ______________

NEXT STEPS:
☐ UX lead to schedule customer interview sprints (by: _____)
☐ Support lead to brief ops team on upcoming changes (by: _____)
☐ Analytics to finalize dashboard requirements (by: _____)
☐ Personas reviewed in W2 reconciliation (Task 10.4, by: _____)

FOLLOW-UP REQUIRED:
- [ ] Any: _____________ (Reason: _____)
- [ ] Any: _____________ (Reason: _____)
```

---

---

## Workshop 3: Workflow Prioritization Workshop (90 minutes)

**Attendees:** Product Manager, Tech Lead, Platform Lead, Hangar Labs representative  
**Goal:** Prioritize vertical slices and confirm top-2 agentic pilots align with roadmap  
**Pre-Read Materials:** [Worksheet 05: Agentic Workflow Discovery](./worksheets/05-agentic-workflow-discovery-schedule-change.md), [AGENTIC_EXPERIMENTATION_PLAN.md](./AGENTIC_EXPERIMENTATION_PLAN.md), [SLICE_1_PROPOSAL_DRAFT.md](./SLICE_1_PROPOSAL_DRAFT.md)

### Agenda (90 minutes)

| Time | Activity | Owner | Materials |
|------|----------|-------|-----------|
| 0-5 min | **Welcome & Context** | Facilitator | [Context script](#context-scripts-2) |
| 5-20 min | **Evidence Walk-Through: Slices and Pilots** | Product | [Slice & Pilot overview slides](#slice-pilot-slides) |
| 20-40 min | **Prioritization Workshop: Vertical Slices** | Tech Lead + Product | [Decision Template 3.1](#decision-template-31) |
| 40-60 min | **Pilot Readiness Review** | Hangar Labs + Engineering | [Pilot Readiness Matrix](#pilot-readiness-matrix) |
| 60-75 min | **Resource Alignment & Roadmap** | Platform Lead | [Decision Template 3.2](#decision-template-32) |
| 75-90 min | **Capture Decisions & Next Steps** | Facilitator | [Decision Log Template](#decision-log-template-2) |

---

### Context Scripts

**Opening (5 min):**
```
"Today we're locking the vertical-slice roadmap and validating pilot governance. 
We have 4 candidate slices and 2 agentic-pilot hypotheses. Your role is to:

1. Confirm Slice 1 (reason-code quality) is the right starting point
2. Understand resource requirements and timeline implications
3. Validate Pilot A and Pilot B governance (success metrics, rollback criteria)
4. Decide: proceed to implementation, or loop back to discovery?

By end of day, we'll have a locked roadmap for implementation planning and 
go/no-go decision criteria for each pilot. This is the final discovery gate 
before stakeholder sign-off and team assignment."
```

---

### Slice & Pilot Overview Slides

**Slide 1: Four Proposed Vertical Slices**

```
SLICE 1: Eligibility Transparency & Reason-Code Quality
├─ Problem: 12 reason codes → generic "ineligible" message → customer confusion
├─ Solution: Normalize to 4 categories, add UI explanation templates
├─ Success: ≥20% escalation reduction, ≥1.0 clarity improvement
├─ Effort: 62 FTE-weeks / 8-12 weeks elapsed
├─ Governance: Code-evidenced (W4 classification: CRITICAL exception)
└─ Gate: Pilot A readiness (≥90% explanation accuracy → unlock Pilot A)

SLICE 2: Audit Completeness & Rule Transparency
├─ Problem: Eligibility/mutation rules not explainable; audit fields 60% complete
├─ Solution: Hardened compliance field mapping, rule-to-reason contract, observability dashboard
├─ Success: ≥99% audit completeness (Pilot B target), ≥50% defect-detection speed
├─ Effort: ~40 FTE-weeks (data schema + observability)
├─ Dependency: Slice 1 complete (reason context feeds into audit schema)
└─ Gate: Pilot B readiness + compliance review

SLICE 3: Conversational Eligibility Assistant
├─ Problem: Ineligible customers want alternatives; no discovery of other options
├─ Solution: LLM-powered assistant with access approval; suggests alternatives, escalation paths
├─ Success: Pilot A target ≥20% escalation reduction extends to alternatives exploration
├─ Effort: ~50 FTE-weeks (LLM integration + safety guardrails)
├─ Dependency: Slice 1 (foundation: clear reason codes + audit)
└─ Gate: Pilot A hardening + legal review of alt suggestions

SLICE 4: Proactive Disruption Offers & Loyalty Optimization
├─ Problem: Passengers don't know about pro-active rebooking; no loyalty consideration
├─ Solution: Predictive offers during IROP window + loyalty-tier optimization
├─ Success: +15% voluntary rebooking + loyalty spend +$X per passenger
├─ Effort: ~60 FTE-weeks (ML model + offer engine + loyalty integration)
├─ Dependency: Slices 1-2 complete; requires new data contracts
└─ Gate: Data science roadmap + loyalty team alignment
```

**Slide 2: Slice Prioritization Matrix (Code-Derived)**

```
PRIORITIZATION CRITERIA:

Impact on Customer Experience (Evidence Base):
  Slice 1: ████████░░ (8/10) - Reduces frustration, enables pilots
  Slice 2: ███████░░░ (7/10) - Supports compliance + agent efficiency
  Slice 3: ██████░░░░ (6/10) - Nice-to-have for discovery
  Slice 4: ████░░░░░░ (4/10) - Strategic but not MVP

Impact on Operational Efficiency (Support/Audit):
  Slice 1: █████░░░░░ (5/10) - Some support deflection
  Slice 2: ████████░░ (8/10) - Audit automation, compliance
  Slice 3: ███░░░░░░░ (3/10) - Minimal ops impact early
  Slice 4: ██░░░░░░░░ (2/10) - Future revenue only

Implementation Risk (Code-Evidenced):
  Slice 1: ██░░░░░░░░ (2/10) - Low: reason normalization is well-scoped
  Slice 2: ███░░░░░░░ (3/10) - Low-Medium: data schema work
  Slice 3: ██████░░░░ (6/10) - Medium-High: LLM safety, hallucination risk
  Slice 4: ███████░░░ (7/10) - High: ML model complexity, data deps

Team Readiness (Capacity):
  Slice 1: ███████░░░ (7/10) - Skills available (BFF, FE, Analytics)
  Slice 2: ███████░░░ (7/10) - Skills available (data, eng)
  Slice 3: █████░░░░░ (5/10) - Requires Hangar Labs LLM expertise
  Slice 4: ████░░░░░░ (4/10) - Requires data science + product analytics

RECOMMENDATION (Code-Evidenced + ADO Alignment):
  PRIMARY PATH: Slice 1 → Slice 2 → Slice 3 (sequential, gated)
  RATIONALE: Slice 1 is lowest-risk, highest-confidence, unblocks pilots
             Slice 2 is compliance-critical (BUS-3.1/3.2)
             Slice 3 builds on pilot learnings
             Slice 4 deferred to post-pilot hardening
```

---

### Pilot Readiness Matrix

**Pilot A: Eligibility Explanation Assistant (Read-Only)**

| Criterion | Current State | Readiness | Gate |
|-----------|---|---|---|
| **Success Metrics Defined** | Escalation ≥20%, Clarity ≥1.0 point, Mutations 0 | ✅ READY | Slice 1 completion + 2-week validation |
| **Rollback Criteria Defined** | Accuracy <90%, Hallucination threshold exceeded | ✅ READY | Continuous monitoring post-deploy |
| **Governance Guardrails** | Read-only, human approval for policy recommendations, weekly review | ✅ READY | Security + compliance review required (Section 10) |
| **Data Grounding Strategy** | Reason mappings from code-evidenced eligibility rules | ✅ READY | W4 compliance field mapping approved |
| **Audit / Logging** | Full recommendation + outcome trail | ✅ READY | Pilot readiness check (PILOT_READINESS_CHECK.md) approved |
| **Safety Testing** | Pre-prod hallucination detection + accuracy QA | 🟡 PLANNED | Pre-Pilot-A approval gate (Story 4.3 in Slice 1) |
| **Team Capacity** | Hangar Labs + Engineering resources committed | 🔴 PENDING | Resource alignment required (Section 10 workshop) |
| **Legal Review** | Explanation copy liability + policy compliance | 🔴 PENDING | Legal/compliance sign-off gate (Section 10) |

**Overall Pilot A Readiness: 60% (Governance ready; Resources + Legal pending)**

---

**Pilot B: Audit Completeness Checker (Automation)**

| Criterion | Current State | Readiness | Gate |
|-----------|---|---|---|
| **Success Metrics Defined** | Completeness ≥99%, Speed ≥50% improvement | ✅ READY | Slice 2 completion + measurement |
| **Rollback Criteria Defined** | False-positive rate, overhead threshold | ✅ READY | Ops feedback required |
| **Governance Guardrails** | Produces reports (no direct mutations), human review before action | ✅ READY | Compliance + ops alignment required |
| **Design Finalized** | Audit field mapping + remediation logic | 🟡 PLANNED | W4 audit schema completion + Slice 2 design |
| **Audit / Logging** | Detection + remediation trail | 🟡 PLANNED | Slice 2 observability design |
| **Safety Testing** | Pre-prod false-positive detection | 🟡 PLANNED | Slice 2 QA plan |
| **Team Capacity** | Data + Engineering resources committed | 🔴 PENDING | Resource alignment required |
| **Compliance Review** | Audit automation liability + legal review | 🔴 PENDING | Compliance sign-off gate (Section 10) |

**Overall Pilot B Readiness: 40% (Governance started; Dependent on Slice 2 design completion)**

---

### Decision Template 3.1

**Workshop Decision Template: Slice Prioritization**

```
DECISION POINT 3.1: Slice prioritization locked?

SLICE SEQUENCING DECISION:

☐ CONFIRMED: Slice 1 → Slice 2 → Slice 3 → Slice 4 (sequential, recommended)
   Rationale: Low risk, high confidence, pilot gating strategy
   Timeline: Slice 1 (8-12w) → Slice 2 (6-8w) → Slice 3 (TBD) → Slice 4 (TBD)
   
☐ MODIFIED: Alternative sequencing?
   Alt Path: ____________________________________
   Rationale: ____________________________________
   Owners: ____________________________________

SLICE 1 GO/NO-GO DECISION:

✓ Proceed to implementation? [ GO / NO-GO / CONDITIONAL ]
   If conditional: ____________________________________
   
✓ Resource commitment confirmed? [ YES / NO ] (team: ______________)
✓ Role assignment confirmed? [ YES / NO ] (PM: __, TL: __, Analytics: __)
✓ Timeline acceptable (8-12 weeks)? [ YES / NO ]

SLICE 2 DEPENDENCY GATES:

✓ Slice 1 completion required before Slice 2 start? [ YES / NO ]
✓ Reason: ____________________________________

OWNER: Engineering Lead + Product Lead | Confidence: ___/10
```

---

### Decision Template 3.2

**Workshop Decision Template: Pilot Readiness & Roadmap**

```
DECISION POINT 3.2: Pilot readiness and roadmap alignment

PILOT A (ELIGIBILITY EXPLANATION ASSISTANT):

Readiness Assessment: ___% (60% current)
  ✅ Governance: Ready (rules-based, read-only, audit trail)
  🟡 Engineering: Planned (depends on Slice 1 completion)
  🔴 Resource: Pending (Hangar Labs + team commitment needed)
  🔴 Compliance: Pending (legal review of explanation liability)

GO/NO-GO DECISION:
  ☐ PROCEED to Slice 1 with Pilot A integration as gate (Story 5.1)
  ☐ DEFER Pilot A until post-Slice-1 validation (separate approval)
  ☐ NO-GO: Descope Pilot A; focus on core reason normalization

Contingencies:
  • If accuracy ≥90% post-Slice-1: _______________ [decision path]
  • If accuracy <90% post-Slice-1: _______________ [decision path]
  
Owner: Product + Hangar Labs | Confidence: ___/10

---

PILOT B (AUDIT COMPLETENESS CHECKER):

Readiness Assessment: ___% (40% current)
  ✅ Governance: Foundations ready (rules-based, report-only)
  🟡 Design: Planned (depends on W4 audit schema + Slice 2)
  🔴 Resource: Pending (Slice 2 team commitment needed)
  🔴 Compliance: Pending (audit automation liability review)

GO/NO-GO DECISION:
  ☐ PROCEED to Slice 2 with Pilot B design as phase 1
  ☐ DEFER Pilot B until post-Pilot-B post-Slice-2 validation
  ☐ NO-GO: Descope Pilot B; focus on audit schema hardening only

Contingencies:
  • If false-positive rate acceptable: _______________ [decision path]
  • If false-positive rate blocks ops: _______________ [decision path]
  
Owner: Engineering + Data Lead | Confidence: ___/10

---

DEPENDENCY CHAIN LOCKED:

Slice 1 → Pilot A Readiness Gate
↓
Slice 2 → Pilot B Design Phase
↓
Pilot A + B → Expanded Scope Decision (Slice 3)

Approved by: Product Lead _____, Engineering Lead _____, Hangar Labs Rep. _____
```

---

### Decision Log Template

**To Complete at Close of Workshop 3**

```
WORKSHOP 3 DECISION LOG (Date: _______) 
Facilitator: _______ | Attendees: _______ | Decision Authority: Product Lead

PRIMARY DECISIONS MADE:
1. Slice Sequencing Locked: [ Slice 1→2→3→4 / Alternative: _____]
2. Slice 1 Go/No-Go: [ GO / NO-GO / CONDITIONAL: _____]
3. Pilot A Path: [ Proceed / Defer / No-Go ]
4. Pilot B Path: [ Proceed / Defer / No-Go ]
5. Resource Commitment: [Team assigned? Y / N: ____________]

ROADMAP SUMMARY:
  Slice 1 Start Date: __________ (8-12 week duration)
  Slice 2 Start Date: __________ (contingent on Slice 1 completion)
  Pilot A Gate: __________ (Slice 1 completion + 2-week validation)
  Pilot B Gate: __________ (Slice 2 completion + compliance review)

DEPENDENCIES & GATES:
  [ ] Pilot A requires legal review (by: _____)
  [ ] Pilot B requires compliance review (by: _____)
  [ ] Slice 2 blocked until Slice 1 complete (by: _____)
  [ ] Resource contention points: _____________ (resolution: _____)

DIVERGENCES CAPTURED:
1. [Divergence]: _______________
   Stakeholders: ______________
   Resolution: ______________
   Owner: ______________

NEXT STEPS:
☐ Engineering lead to confirm team capacity (by: _____)
☐ Hangar Labs rep to schedule Pilot A governance review (by: _____)
☐ Compliance to schedule legal review (by: _____)
☐ Product to finalize resource assignments (by: _____)
☐ Roadmap reviewed in final sign-off (Task 10.5, by: _____)

FOLLOW-UP REQUIRED:
- [ ] Any: _____________ (Reason: _____)
- [ ] Any: _____________ (Reason: _____)

APPROVAL SIGN-OFF:
Product Lead: __________________ (Date: _____)
Engineering Lead: __________________ (Date: _____)
Hangar Labs Rep (if attending): __________________ (Date: _____)
```

---

---

## Post-Workshop Reconciliation (Task 10.4)

**After all three workshops are complete, reconcile findings into W1-W5:**

### W1 Metrics Reconciliation
- [ ] Update baseline numbers from Workshop 1 decisions
- [ ] Lock instrumentation roadmap and timeline
- [ ] Capture any divergences (e.g., analytics wanted different targets)
- [ ] Document rebaseline gate decision

### W2 Persona Reconciliation
- [ ] Update confidence levels based on validation
- [ ] Prioritize personas for interview/research phases
- [ ] Capture new insights from stakeholder input
- [ ] Update measurement mapping for W1 metrics

### W5 (Agentic Workflow) Reconciliation
- [ ] Confirm Pilot A success metrics from Workshop 3
- [ ] Confirm Pilot B success metrics from Workshop 3
- [ ] Update governance gates based on compliance/legal input
- [ ] Lock pilot activation sequencing

### Slice 1 Proposal Reconciliation
- [ ] Update resource plan based on team assignments (Workshop 3)
- [ ] Adjust timeline if divergences surfaced
- [ ] Incorporate measurement plans from Workshop 1
- [ ] Finalize approval gates for PO sign-off

---

## Facilitation Checklist

**Before Workshops (1 week prior):**
- [ ] Send pre-read materials to all attendees
- [ ] Confirm attendance and resolve conflicts
- [ ] Print or share decision templates
- [ ] Prepare Zoom/meeting room setup (breakout rooms for template work)

**During Workshops:**
- [ ] Start on time; set time-box expectations
- [ ] Use parking lot for out-of-scope discussions
- [ ] Capture divergences explicitly (don't gloss over)
- [ ] Take photos of whiteboard/flip charts for record
- [ ] Confirm decisions at close of each section

**After Workshops:**
- [ ] Type up decision logs day-of (while fresh)
- [ ] Send to attendees for 24-hour review/correction
- [ ] Escalate any high-priority divergences to decision owner
- [ ] Schedule Task 10.4 reconciliation meeting (1 week after final workshop)

---

**Document Status:** Ready to Use  
**Next Step:** Schedule three workshops and distribute pre-read materials (Section 10)  
**Checkpoint:** All workshop decision logs complete and reviewed within 3 days of final workshop
