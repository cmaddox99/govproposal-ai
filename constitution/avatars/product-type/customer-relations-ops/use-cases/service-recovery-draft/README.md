# Use Case: AI-Assisted Service Recovery Draft
# Avatar: avatar-customer-relations-ops | Laws: BUS-4.1, BUS-7.1, ENG-6.4, PRD-2.3
# Grounded in: ct-service-recovery-bff, ai-inspiration-service (hangar-w4-dp-mobile)

use_case:
  id: uc-cro-service-recovery-draft
  name: AI-Assisted Service Recovery Response Draft
  jtbd: "When a passenger is waiting for a response about their disruption, I want AI to draft an empathetic reply quickly so I can focus on the decision, not the writing."
  actor: Customer Relations Agent
  laws: [BUS-4.1, BUS-7.1, ENG-6.4, PRD-2.3]
  source_evidence: ct-service-recovery-bff, ai-inspiration-service, servicerecovery-ios

---

## Pre-conditions

- Complaint is in `REVIEWED` state (agent has read the case)
- PNR and disruption type are confirmed
- PII has been stripped before being passed to the LLM (BUS-4.1 — PII Privacy by Design)

## Main Flow

1. Agent selects complaint in CRM; case loads with disruption type and flight details
2. Agent clicks "Generate draft" — system calls `ai-inspiration-service`
3. LLM receives: disruption type, compensation tier, flight route, delay duration — **no PII, no PNR**
4. Draft response returned in ~3 seconds — empathy-first, compensation amount pre-filled
5. Agent reviews draft; edits tone or specific detail if needed
6. Agent selects compensation type and confirms amount (human in the loop — no auto-compensation)
7. Agent clicks "Send" — response dispatched, audit record created (BUS-7.1)

## PII Safety Contract (BUS-4.1)

The BFF layer must enforce these before the LLM call:
```
✅ Allowed in LLM prompt: disruption_type, delay_minutes, route (DFW→LAX), compensation_tier
❌ NEVER in LLM prompt: passenger_name, PNR, email, phone, AAdvantage number, payment data
```

If PII is detected in the prompt at the BFF layer, the call is rejected and an alert is logged. No exceptions.

## What the Agent Cannot Skip

- The agent must read the complaint before generating a draft — **Generate Draft** button is disabled until the agent has been on the case view for ≥30 seconds
- The agent must confirm the compensation amount before sending — the system cannot auto-send based on the LLM draft alone
- Every sent response is logged with: agent ID, complaint ID, draft version used, edits made, compensation amount, timestamp (BUS-7.1)

## Alternate Flows

| Branch | Trigger | Resolution |
|--------|---------|------------|
| LLM service unavailable | `ai-inspiration-service` timeout | Agent writes manually; fallback template available for disruption type |
| Draft tone is wrong | Agent rejects draft | Agent edits or clicks "Regenerate" (max 2 regenerations per case) |
| Complaint requires legal review | Legal flag triggered by disruption type | Route to legal team queue; LLM draft suppressed |
| Passenger is AAdvantage elite | Detected by compensation tier | Draft pre-fills with appropriate elite-tier language and offer |

## Quality Signal

If the agent's edit distance from the LLM draft exceeds 70% (i.e., they rewrote most of it), the case is flagged for prompt quality review. This is how the `ai-inspiration-service` prompt is iteratively improved — not by building a better model, but by learning from what agents actually change.
