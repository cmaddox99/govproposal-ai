---
avatar: avatar-product-network-automation
law: PRD-1.2
title: "Problem-First Law"
---

# PRD-1.2 — Problem-First Law: Network Automation Application

## What This Law Requires
No network automation solution work may begin until the operator problem is validated with evidence. Building a Nautobot change pipeline or DNS API without documented engineer pain points is prohibited.

## Compliant Example

**Problem Statement: Network Change Automation (Evidence-Validated)**

```
Problem: Network engineers at AA spend an average of 45 minutes per change
request performing manual cross-system validation (Nautobot → ServiceNow →
device CLI), with 3 P1 incidents in the last 6 months caused by out-of-window
pushes and silent verification failures.

Evidence:
- 7/8 network engineers interviewed: cross-system validation is #1 time loss
- 6/8 engineers: no automated rollback means 20–90 min manual recovery per failed change
- 3 P1 incidents (Q4 2025–Q1 2026): root cause = out-of-window push or unverified change
- Ticket data: 15% of CAB change requests rejected for missing rollback plan
- NOC interviews: avg 30+ min to correlate alert to triggering change (no correlation_id)

Validated: Yes — 8 engineer interviews + 4 NOC interviews + 6-month incident/ticket data
```

**Phase gate:** Problem statement filed in `hangar-ai-specs/changes/` before any feature specification begins. No API design, no schema design, no Nautobot job specification until this gate is filed.

**Constitutional check:** PRD-1.2 — validated problem with quantitative evidence before any solution work begins.

## Violation Example
```
❌ "Let's build an API that wraps the Nautobot change job endpoint."
   → Solution proposed with no problem statement.
   → Violates PRD-1.2: what engineer pain does this solve? What evidence supports it?
   → The Nautobot API capability does not justify building a wrapper. The operator
     problem (45 min cross-system friction) justifies it.
```

## Edge Cases & Warnings
- "Everyone agrees this is a problem" is not evidence — interview data and ticket counts are required
- The problem statement must specify the affected personas (network engineers, NOC operators) not just "users"
- A technical debt problem ("the current process is manual") is not a customer problem — validate that the manual process causes measurable operator pain before proposing automation
