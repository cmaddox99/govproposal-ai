---
avatar: avatar-schedule-change-self-serve
domain: Eligibility Check, Reason Codes, Self-Serve Rebooking, Audit Trail
laws: [PRD-1.1, PRD-2.1, PRD-3.1, PRD-4.1, PRD-5.1, BUS-2.1, BUS-2.2, BUS-2.4, ENG-6.4, ENG-6.7]
skills: [04-business-domain-modeling, 05-business-rules, 12-api-design, 13-observability, 21-prompt-engineering, 23-ai-agents]
---

# Schedule Change Self-Serve — Agent Guidance

Covers the full eligibility-to-rebooking chain: check if a change is allowed, surface actionable reason codes if not, execute the rebooking, record an immutable audit trail. Applies to both self-serve and agentic-assisted change scenarios.

**Not in scope:** involuntary schedule changes initiated by AA operations (use the service-recovery avatar).

## Core Laws (one-liner)

| Law | Rule |
|-----|------|
| PRD-1.1 | Discovery: prioritise eligibility-block abandonment signals over support ticket volume |
| PRD-2.1 | Map three change paths: mobile self-serve, agent-assisted console, proactive offer |
| PRD-3.1 | Roadmap order: eligibility clarity → self-serve success rate → audit completeness → AI assist |
| PRD-4.1 | Eligibility reason-code slice is the safest MVP entry point — read-only, zero rebooking risk |
| PRD-5.1 | Validate on same-day domestic cohort (10%) before full rollout |
| ENG-6.4 | PNR and ticket data encrypted at rest and in transit |
| ENG-6.7 | Every eligibility decision and agent override immutably audited |

## Key Patterns

- **Reason codes before rebooking** — passengers can't self-serve if they don't understand why a change is blocked.
- **BFF trace spans** — track eligibility + reservation + seat assignment as separate segments.
- **Human-in-the-loop gate** — any agentic action that mutates a PNR requires explicit passenger confirmation.
- **Immutable audit events** — eligibility decisions and agent overrides logged to append-only store.

## Anti-Patterns

- ❌ Relying solely on support ticket volume to measure abandonment (lags 24-72 hours).
- ❌ Agentic rebooking without explicit passenger confirmation gate.
- ❌ Eligibility service falling back silently — degrade gracefully with messaging.

See `guidance-detail.md` for full law breakdowns, skill pairings, and agentic workflow guidance.
