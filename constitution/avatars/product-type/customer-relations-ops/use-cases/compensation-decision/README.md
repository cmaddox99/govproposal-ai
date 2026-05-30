# Use Case: Add a Compensation Decision
# Avatar: avatar-customer-relations-ops | Laws: BUS-7.1, BUS-3.6, BUS-2.3, BUS-4.1

use_case:
  id: uc-cro-compensation-decision
  name: Log a Compensation Decision
  jtbd: "When a passenger is harmed by a disruption, I need to record what we're offering so it's auditable and the passenger can be made whole."
  actor: Customer Relations Agent
  laws: [BUS-7.1, BUS-3.6, BUS-2.3, BUS-4.1]

---

## Pre-conditions

- Complaint is in `REVIEWED` state
- Agent has confirmed disruption is AA-caused or qualifies under DOT rules

## Main Flow

1. Agent selects compensation type: miles, travel voucher, or refund
2. Amount entered; system validates against compensation matrix
3. Monetary amounts use `Decimal` arithmetic — no floating-point (BUS-3.6)
4. Decision confirmed by agent (human in the loop — no auto-compensation)
5. Audit record created: timestamp, agent ID, complaint ID, compensation type, amount, authorisation level (BUS-7.1)
6. Compensation dispatched to `mobile-aadvantage-bff` (miles) or payments (voucher/refund)
7. Audit record updated with dispatch confirmation and correlation ID

## Immutability Rule (BUS-7.1)

Once a compensation record is written, it must not be updated in place. If a correction is needed, a new record is created with a `corrects:` reference to the original record ID. The original record is never deleted or modified.

## Refund Path (BUS-2.3)

For DOT-qualifying involuntary disruptions, the refund option must be offered first — before miles or voucher alternatives. The UI flow must surface refund as the primary option, not a secondary path.
