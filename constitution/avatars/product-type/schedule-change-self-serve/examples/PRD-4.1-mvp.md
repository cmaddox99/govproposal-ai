# PRD-4.1: MVP & Product-Market Fit — Schedule Change Self-Serve

**Law Reference:** [PRD-4.1: MVP & Product-Market Fit](../../../../laws/product/roadmap.md)  
**Avatar:** schedule-change-self-serve  
**Status:** Experimental — pilot criteria require validation with product owner before Sprint 1

---

## MVP Principle for Schedule Change

The smallest useful slice is the one that gives passengers a clear answer — even
if the answer is "no, you can't change." Transparent eligibility is lower-risk
than conversational rebooking and delivers immediate measurable value.

---

## Pilot 1: Eligibility Reason Code Enrichment

**Hypothesis:** Structured reason codes with plain-language explanation reduce
agent escalation rate by 20% and abandonment rate by 15% within 30 days.

### Scope
- Eligibility service emits structured reason codes (not just `INELIGIBLE: true`)
- BFF maps reason code to plain-language explanation string
- Schedule Change UI displays explanation with a suggested next step

### Risk Controls
- Change is additive (no existing data removed)
- Reason codes are read-only — no booking mutation
- Rollback: revert to generic ineligibility message if reason code accuracy <90%

### Cohort
- 25% of ineligible change attempts on domestic itineraries
- Exclude codeshare and group PNRs in first cohort (more complex rule surfaces)

### Success Criteria (30 days)
- Reason code coverage: 100% of ineligible responses include a code
- Agent escalation rate: drops from 20% to ≤16% for ineligible traffic
- Passenger clarity score: ≥3.5/5 in in-app survey (5-question, post-result)
- Zero increase in booking errors or re-check attempts

### Rollback Trigger
- Reason code accuracy <90% (determined by agent audit of 100 samples)
- Booking error rate increases >1% in cohort vs. control

---

## Pilot 2: BFF Observability Spike

**Hypothesis:** Adding per-span tracing to the BFF reveals the top latency
contributor within the orchestration chain, enabling a targeted fix to reduce
p95 from 3200ms to <2000ms in 30 days.

### Scope
- Add OpenTelemetry spans: BFF → eligibility call + seat query + reservation write
- Deploy to 100% of traffic (observability-only, no logic change)
- Dashboard in existing monitoring platform

### Risk Controls
- Tracing is side-effect-free — no logic changes
- Sampling rate adjustable if tracing overhead exceeds 2% CPU

### Success Criteria (14 days)
- Full span coverage on all BFF change requests
- Top 3 latency contributors identified with evidence
- Actionable sprint ticket created for each contributor

---

## Decision Gate (Before Slice 3 — Agentic Layer)

Before building the conversational eligibility agent, validate:

1. Reason code enrichment (Pilot 1) has shipped and acceptance criteria met
2. BFF latency is ≤2000ms p95 (agent on top of slow BFF amplifies latency problems)
3. Audit trail completeness ≥99% (agent recommendations must be auditable)
4. Human-in-the-loop override gate design approved by Legal/Compliance
