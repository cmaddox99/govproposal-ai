# PRD-3.1: Roadmap Planning — Schedule Change Self-Serve

**Law Reference:** [PRD-3.1: Roadmap Planning](../../../../laws/product/roadmap.md)  
**Avatar:** schedule-change-self-serve  
**ENG-2.3:** Vertical Slice Development — each slice delivers standalone user value  
**Status:** Experimental — priorities require validation with product owner and analytics evidence

---

## Roadmap Principle

Source code is the current source of truth. Every roadmap item is grounded in
findings from repo analysis (Phase 2b) or validated discovery data. Competitor
benchmarks and architectural constraints inform priority until production telemetry
replaces experimental baselines.

---

## Vertical Slice Delivery Sequence

### Slice 1 — Eligibility Transparency (NOW)

**Hypothesis:** If passengers receive a clear, actionable reason code when ineligible,
escalation-to-agent rate drops by 20% and abandonment drops by 15%.

**Scope:**
- Add structured reason codes to eligibility service response
- BFF surfaces reason code with plain-language explanation in UI
- Agent console shows rule match detail alongside override prompt

**Acceptance Criteria:**
- 100% of ineligibility responses include a reason code (no empty/generic blocks)
- Reason code clarity score improves from 2.8/5 to ≥3.8/5 in passenger survey
- Agent investigation time per override request drops from estimated 4 min to 2 min

**Rollback Trigger:** >2% increase in booking errors or >5% increase in escalation rate

---

### Slice 2 — Rebooking Success and Audit Completeness (NEXT)

**Hypothesis:** Reducing BFF orchestration errors and filling audit gaps improves
self-serve success rate and unblocks compliance.

**Scope:**
- Instrument BFF with per-span tracing (eligibility + seat assignment + reservation)
- Add immutable audit event per eligibility decision and override
- Fix seat assignment race condition on same-day changes (identified in code review)

**Acceptance Criteria:**
- BFF p95 latency ≤1800ms
- Audit trail completeness ≥99% on all change requests
- Self-serve success rate improves from 78% to ≥84%

**Rollback Trigger:** Increase in booking errors >1% or audit completeness drops

---

### Slice 3 — Conversational Eligibility Assistant (NEXT)

**Hypothesis:** An AI agent that explains eligibility rules in plain language and
surfaces alternative flights reduces phone escalation by 30% for ineligible requests.

**Scope:**
- Eligibility explanation agent (read-only — cannot mutate bookings)
- Agent is citation-backed: every statement links to the rule that blocked the change
- Human-in-the-loop gate: agent cannot initiate rebooking without passenger confirmation

**Acceptance Criteria:**
- Agent clause precision ≥90% (validated against rule catalog)
- Escalation-to-phone rate drops ≥25% for ineligible change traffic
- Zero booking mutations without explicit passenger confirmation

**Rollback Trigger:** >0.5% incorrect eligibility explanation rate or any unauthorized booking mutation

---

### Slice 4 — Proactive Disruption and Loyalty-Aware Change (LATER)

**Hypothesis:** Proactive change offers during schedule disruptions and loyalty-aware
seat preservation increase overall change completion and reduce IDB risk.

**Scope:**
- IRROPs detection hook triggers proactive change eligibility evaluation
- Loyalty upgrade hold detection before change confirmation
- One-tap reconfirmation for pre-evaluated alternatives

**Acceptance Criteria:**
- Proactive offer acceptance rate ≥40% for disrupted itineraries
- Upgrade hold preserved in ≥95% of eligible rebookings
- IDB contributions from failed changes reduced by 30%

**Rollback Trigger:** Proactive offer accuracy <80% or IDB rate increases

---

## Prioritization Matrix

| Item | Customer Impact | Operational Impact | Feasibility | Priority |
|------|----------------|-------------------|-------------|----------|
| Reason code enrichment (Slice 1) | High | High | High | 1 |
| BFF instrumentation + audit fix (Slice 2) | Medium | High | High | 2 |
| Conversational eligibility agent (Slice 3) | High | High | Medium | 3 |
| Proactive disruption offer (Slice 4) | High | High | Low | 4 |
| Group PNR atomic change | Medium | Medium | Low | 5 |
| Loyalty upgrade preservation | High | Medium | Medium | 6 |
