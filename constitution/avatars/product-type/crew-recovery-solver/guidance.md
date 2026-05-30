# Crew Recovery Solver Guidance

> **Purpose:** Governs AI-assisted development of IROP crew reassignment and recovery systems.

---

## Overview
Crew Recovery Solver (CWR) reassigns crew after IROP events. FAR Part 117 crew rest minimums are a **hard safety constraint** — never a performance tradeoff. Every assignment decision must produce an immutable audit trail entry.

## Non-Negotiable Laws

### BUS-2.1 — FAA Compliance Law
- **What this law requires:** All recovery options presented must satisfy FAR Part 117 crew rest minimums before display.
- **What violates it:** Showing a crew member an assignment that violates their legal rest period, even as a "waivable" option.
- **Implementation note:** FAR 117 check runs synchronously before any option is scored or ranked.

### PRD-1.5 — Evidence-Based Decision Law
- **What this law requires:** Recovery options must be ranked by evidence-scored criteria (rest compliance, experience match, proximity), not arbitrary order.
- **What violates it:** Presenting options in FIFO or random order without scoring justification.
- **Implementation note:** Each option carries a `recovery_score` with factor breakdown visible to the scheduler.

### BUS-7.1 — Audit Trail Law
- **What this law requires:** Every crew assignment decision — accepted, rejected, or overridden — must produce an immutable audit record.
- **What violates it:** Assignment changes that update the crew roster without a corresponding audit log entry.
- **Implementation note:** Audit record includes decision timestamp, acting user, FAR 117 status at time of decision, and override justification if applicable.

### PRD-5.1 — MVP Law
- **What this law requires:** Recovery features ship only when FAR 117 enforcement and audit trail are both present.
- **What violates it:** Shipping "v1" without full audit trail or with FAR 117 check as opt-in.

## Core Journeys
| Journey | Trigger | Key Laws |
|---------|---------|----------|
| Single cancellation recovery | Flight cancelled | BUS-2.1, PRD-1.5, BUS-7.1 |
| Cascading delay reassignment | Multi-leg delay chain | BUS-2.1, BUS-7.1 |
| Manual override with justification | Scheduler judgment | BUS-7.1, ENG-6.7 |

## Anti-Patterns to Avoid
- Treating FAR Part 117 as a soft warning rather than a hard gate
- Logging assignment changes without correlation ID (breaks regulatory audit trail)
- Presenting recovery options without evidence-based scoring
