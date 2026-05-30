# Schedule Change Self-Serve Guidance

## Scope

Use this avatar when working on services that enable passengers to modify existing
flight reservations without agent intervention. This avatar covers the full
eligibility-to-rebooking chain: determining whether a change is allowed, presenting
actionable reason codes when it is not, executing the rebooking, and recording an
immutable audit trail.

This avatar applies to **self-serve and agentic-assisted** change scenarios. It does
not cover involuntary schedule changes initiated by AA operations (use the
service-recovery operational avatar for that).

---

## Taxonomy Note

This avatar passed all five constitution taxonomy gates (see manifest.yaml). It is
distinct from:

- `passenger-booking` — initial ticket purchase and seat selection
- `check-in-travel` — airport check-in and boarding operations
- `customer-service` — reactive agent-facing support tools

---

## Law Application

### PRD-1.1 Continuous Discovery

Discovery must prioritise these four signal sources:

1. Passengers who hit eligibility blocks — what action do they take? (abandon, call agent, retry?)
2. Airport agents — what override patterns are most common, and what's the root cause?
3. BFF and eligibility service logs — abandoned change sessions, error code frequency, latency outliers
4. Competitor benchmarks — how does an AA change compare in time, clarity, and success rate to United, Delta, Southwest?

Do not rely on support ticket volume alone. Ticket volume lags real abandonment by 24-72 hours. Instrument the BFF to capture partial sessions before they become support events.

### PRD-2.1 User Journey Mapping

Map three distinct change paths:

1. **Mobile/Web Self-Serve** — passenger initiates from AA.com or app without agent assistance
2. **Agent-Assisted via Console** — agent uses schedule-change-ui on behalf of passenger
3. **Proactive Offer (Future)** — system detects schedule disruption and proactively presents options

For each path, track:

- Entry point (booking confirmation email, app, IVR transfer)
- Eligibility check result and latency
- If ineligible: reason code clarity score (did the passenger understand why?)
- If eligible: steps to confirmation and total wall-clock time
- Post-change confirmation method (email, push, SMS)

Track exception flows explicitly:

- Group itineraries (multi-passenger PNR)
- Codeshare and partner-carrier segments
- Fare-basis conflicts (ticket rules block change)
- Loyalty seat protections (AAdvantage upgrade holds)

### PRD-3.1 Roadmap Planning

Prioritise in this order unless validated evidence suggests otherwise:

1. **Eligibility transparency** — clear, actionable reason codes when a change is blocked
2. **Self-serve rebooking success rate** — reduce errors in BFF orchestration and seat assignment
3. **Audit completeness** — every eligibility decision and outcome is retrievable
4. **Conversational assistance** — AI agent explains options and guides passenger through change
5. **Proactive disruption offers** — system-initiated change suggestions during schedule disruptions

Vertical slice delivery is required per ENG-2.3. Each slice must:

- Deliver standalone user value
- Include acceptance tests and rollback criteria before moving to next slice
- Have explicit entry and exit metrics

### PRD-4.1 MVP Validation

For each slice, define before building:

1. **Hypothesis** — which change outcome metric improves
2. **Cohort** — which traffic subset (e.g., 10% of same-day domestic)
3. **Risk controls** — what guardrails prevent booking errors in the pilot
4. **Exit criteria** — measurable threshold to declare pilot successful or failed
5. **Rollback trigger** — at what error rate will the slice be withdrawn

The eligibility reason code slice is the recommended entry point: it provides
immediate value (passengers understand why they cannot change) with zero rebooking
risk because it is read-only.

### PRD-5.1 Metrics (Experimental Baselines)

Production telemetry is incomplete in the current discovery cycle. Use these
baselines as hypotheses, not measurements. Replace by instrumenting the BFF and
eligibility service in Sprint 1.

| Tier | Metric | Experimental Baseline | 90-Day Target |
|------|--------|-----------------------|--------------|
| Customer | Self-serve change success rate | 78% (est.) | 88% |
| Customer | Agent escalation rate for eligible changes | 20% (est.) | 10% |
| Customer | Ineligibility reason code clarity score | 2.8/5 (est.) | 4.2/5 |
| Customer | Time from eligibility check to confirmation | 45s (est.) | 25s |
| Operational | BFF p95 latency | 3200ms (est.) | 1800ms |
| Operational | Eligibility service cache hit rate | 55% (est.) | 80% |
| Operational | Manual override requests per 1k changes | 18 (est.) | 8 |
| Risk | Audit trail completeness | 82% (est.) | 99% |
| Risk | Failed compliance events per 10k | 12 (est.) | 2 |

Mark all values as experimental until telemetry confirms.

---

## Engineering Expectations

1. Emit eligibility decision and rule-match reason code on every request.
2. Track BFF orchestration spans (eligibility + reservation + seat assignment) as
   separate trace segments.
3. Preserve immutable audit events for eligibility decisions and agent overrides.
4. Add contract tests whenever BFF → downstream request/response models change.
5. Define explicit fallback behaviour for each upstream dependency.
6. Human approval gate (ENG-9.4) is required before any agentic recommendation
   results in a booking mutation.

---

## Skill Pairings

Use these skills together for this domain:

1. `skill-04-business-domain-modeling` — map eligibility entities, PNR aggregates, rule ownership
2. `skill-05-business-rules` — explicit catalog of tie rules, fare rules, policy constraints
3. `skill-12-api-design` — stable, explainable BFF response contracts with reason codes
4. `skill-13-observability` — eligibility decision telemetry and BFF latency instrumentation
5. `skill-21-prompt-engineering` — conversational eligibility explanation patterns
6. `skill-23-ai-agents` — agent design for eligibility assistant and rebooking guide

---

## Agentic Workflow Guidance

When designing AI agents for this domain:

1. **Read-only first** — eligibility explanation agents must not mutate bookings directly
2. **Citation-backed answers** — every eligibility statement must link to the rule that blocked the change
3. **Human-in-the-loop gate** — any agent action that results in a PNR change requires explicit passenger confirmation and, where override authority is required, agent sign-off
4. **Audit every recommendation** — log agent reasoning chain, rule match, and outcome to the audit trail
5. **Graceful fallback** — if eligibility service is unavailable, surface degraded-mode messaging rather than failing silently

---

## ADO Discovery Document Integration

When Bhavita's ADO discovery document is received:

1. Cross-reference personas and journeys against code findings
2. Adopt any higher-confidence data from ADO (real metrics, validated personas)
3. Flag disconnects between ADO assumptions and actual service behaviour
4. Update this guidance file and relevant worksheets with reconciled data
5. Mark reconciled values distinctly from experimental baselines

Source code is the primary source of truth. ADO artifacts inform and enrich but do not override code analysis.
