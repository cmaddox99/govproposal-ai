---
avatar: avatar-customer-service
domain: DOT Refund Timelines, Denied Boarding Compensation, IROP Rebooking, Complaint Handling
laws:
  - BUS-2.3
  - BUS-7.1
  - PRD-1.2
  - PRD-5.1
  - PRD-6.2
skills:
  - 22-decision-support
  - 28-content-transformation
  - 06-atomic-tdd
---

# Customer Service — Implementation Guidance

## Overview

Customer Service tools support stranded passengers, voluntary changers, and frustrated customers across flight changes, IROP rebooking, refunds, and complaint resolution. The dominant failure mode is **call volume surge during IROP events**: 67% of agent calls during major disruptions are rebooking requests. Automation must target this specific scenario before expanding to general inquiry handling.

---

## Core Journeys

| Journey | Persona | Success Metric |
|---------|---------|----------------|
| IROP Rebooking (self-serve) | Stranded Passenger | Call deflection rate ≥ 15% |
| Flight Change | Voluntary Changer | Self-service completion rate > 50% |
| Refund Request | Voluntary/Involuntary | Refund processed within DOT SLA |
| Complaint Resolution | Frustrated Customer | Response within 30 days (14 CFR Part 259) |
| General Inquiry | Information Seeker | First-contact resolution > 70% |

**Key personas:** Stranded Passenger, Voluntary Changer, Frustrated Customer, Information Seeker, Service Agent, Customer Advocate, Operations Lead.

---

## Non-Negotiable Laws

### BUS-2.3 — DOT Passenger Protections

**24-hour cancellation rule:** Customers who book ≥ 7 days before departure and cancel within 24 hours are entitled to a full refund. System must enforce this without agent intervention; no "are you sure?" friction.

**Refund timelines:**
- Credit card refunds: **7 business days** (14 CFR Part 260).
- Cash/check refunds: **20 business days**.
- Refund status must be surfaced to the customer without requiring a call.

**Involuntary denied boarding (IDB) compensation** (14 CFR Part 250):
- Domestic: 200% of one-way fare (max $775) if delay 1–4 hours; 400% (max $1,550) if > 4 hours.
- Compensation must be offered in cash or cash equivalent; voucher-only is non-compliant.
- System must calculate and present IDB compensation at the gate before the customer requests it.

**Tarmac delay:** 3-hour domestic, 4-hour international limits apply. Customer service tools must surface tarmac timer status when handling active flight inquiries.

### PRD-1.2 — Problem-First
- Validate what % of call volume is IROP rebooking vs. general inquiry before any AI chatbot investment.
- Research: `post_interaction_surveys`, `complaint_sentiment_analysis`, `call_recording_analysis`, `handle_time_studies`.
- A general AI chatbot will not solve a 67% IROP rebooking problem — target the validated bottleneck.

### PRD-6.2 — Retention
- Customers who successfully self-rebook after IROP are 2× more likely to rebook vs. those who call.
- Track 90-day rebook rate post-IROP by channel (self-serve vs. agent). This is the north-star retention metric.

### PRD-5.1 — MVP
- MVP scope: simple same-day IROP rebooking (domestic, single-segment, no codeshare, no group).
- Out of scope for MVP: refunds, IDB compensation, multi-city, codeshare partners.

---

## Key Patterns

- **IDB compensation proactive:** Surface at gate before customer asks; agent should never be in a position of withholding legally-required compensation.
- **DOT refund timer visible to customer:** Refund status should be self-serviceable; no call required to check status.
- **IROP self-serve before agent escalation:** Flow must attempt self-serve rebooking before routing to live agent; not optional, not a "try it" button.
- **Complaint SLA tracking:** 14 CFR Part 259 requires 30-day response; system must track complaint age and alert when approaching deadline.

---

## Anti-Patterns

- ❌ Building AI chatbot for "all queries" without validating the IROP rebooking bottleneck first (PRD-1.2 violation).
- ❌ Offering only vouchers as IDB compensation — cash equivalent is legally required.
- ❌ Hiding refund status behind an agent call — DOT requires transparency without friction.
- ❌ IROP rebooking MVP that includes codeshare, multi-city, and group — scope creep before baseline is proven.
- ❌ Measuring call deflection without tracking 90-day rebook rate (activity metric vs. retention outcome).
