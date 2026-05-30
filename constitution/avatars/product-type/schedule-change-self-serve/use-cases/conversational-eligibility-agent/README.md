# Use Case: Conversational Eligibility Assistant (Agentic)

**Avatar:** schedule-change-self-serve  
**Law:** PRD-3.1 Roadmap Planning, ENG-9.4 Human Override Law  
**Slice:** 3 — Conversational Eligibility Assistance  
**Skill:** skill-23-ai-agents, skill-21-prompt-engineering  
**Status:** Discovery — requires Slice 1 + 2 acceptance criteria met before building

---

## Overview

A passenger blocked from changing their flight interacts with an AI agent that
explains the eligibility rules in plain language, surfaces alternative options,
and guides them step-by-step — without ever mutating a booking directly.

The agent is citation-backed: every claim links to the specific rule that blocked
the change. A human-in-the-loop gate (ENG-9.4) requires explicit passenger
confirmation before any action is taken.

---

## Actors

- **Passenger** — chat interface embedded in schedule-change-ui or app
- **Eligibility Assistant Agent** — reads-only; explains rules and alternatives
- **schedule-change-eligibility-service** — provides structured rule data to agent
- **schedule-change-bff** — executes any passenger-confirmed actions
- **Human Agent (override path)** — required when escalation is requested

---

## Agentic Interaction Flow

```
Passenger: "Why can't I change to the 3pm flight?"
  │
  ▼
Agent queries eligibility service for rule match on PNR + target flight
  │
  ▼
Agent: "Your ticket (fare class Q) requires 7-day advance purchase.
       The 3pm flight departs in 4 hours, which falls within that window.
       [Rule: FARE_BASIS_ADVANCE_PURCHASE — AA fare rules §4.2]"
  │
  ▼
Passenger: "What are my options?"
  │
  ▼
Agent: "Three options:
  1. Change to a flight departing tomorrow or later (your fare allows this).
  2. Purchase a flexible fare — difference is approximately $95.
  3. Speak with an agent — some exceptions apply at the airport."
  │
  ▼
Passenger selects option 1 → Agent surfaces available flights
  │
  ▼
Agent: "You've selected the 9am tomorrow flight. Ready to confirm?"
  │
  └── Passenger confirms → BFF executes change (human-in-the-loop gate cleared)
  └── Passenger declines → Session ends, no booking mutation
```

---

## Guard Rails (ENG-9.4, BUS-7.1)

- Agent is **read-only** until passenger gives explicit confirmation
- Agent cannot override ineligibility rules — can only explain and surface options
- Every agent recommendation is logged to audit trail with reasoning chain
- Escalation to human agent is always offered as an option
- Agent must surface uncertainty: if rule is ambiguous, say so and escalate

---

## Acceptance Criteria (Slice 3)

- Agent eligibility explanation accuracy ≥90% (validated against rule catalog)
- Escalation-to-phone rate drops ≥25% for ineligible traffic in pilot cohort
- Zero booking mutations without explicit passenger confirmation
- Every agent session logged to audit trail with full reasoning chain
- Average session resolution time ≤3 minutes (vs. 8 minute phone average, est.)

---

## Decision Gate (Pre-Build Checklist)

- [ ] Slice 1 reason code enrichment is live and accuracy ≥90%
- [ ] Slice 2 BFF latency ≤2000ms p95
- [ ] Slice 2 audit trail completeness ≥99%
- [ ] Human-in-the-loop gate design reviewed and approved by Legal/Compliance
- [ ] Azure OpenAI capacity confirmed for conversation volume
- [ ] Prompt engineering reviewed for hallucination guardrails (skill-21)
