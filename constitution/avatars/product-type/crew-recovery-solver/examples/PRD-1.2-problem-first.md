---
avatar: avatar-product-crew-recovery-solver
law: PRD-1.2
title: "Problem-First Law"
---

# PRD-1.2 — Problem-First Law: Crew Recovery Application

## What This Law Requires
No solution work for CWR may begin until the crew recovery problem is validated with evidence. Building reassignment workflows without documented scheduler pain points is prohibited.

## Compliant Example

**Problem Statement: IROP Crew Recovery (Evidence-Validated)**

```
Problem: During IROP events, SOC crew schedulers spend an average of 8 minutes
per crew member checking FAR 117 eligibility across 3 separate systems before
they can even begin evaluating recovery options. This delay compounds across
all affected crew members, causing cascading reassignment failures.

Evidence:
- 5/6 schedulers interviewed: multi-system FAR 117 lookup is the #1 time loss
- Avg IROP recovery window: 45 minutes; current per-crew assessment: 8 min
- 4-crew cancellation consumes 32 of 45 available minutes on eligibility checks alone

Validated: Yes — 6 scheduler interviews + ops data from 14 IROP events (Q1 2026)
```

**Gate:** This problem statement is filed in `hangar-ai-specs/changes/` before any feature specification work begins.

**Constitutional check:** PRD-1.2 — solution (consolidated eligibility view) defined only after problem is validated with interview evidence and operational data.

## Violation Example
```
❌ "Let's build a crew reassignment tool — it'll speed up IROP recovery."
   → Solution proposed without a validated problem statement.
   → Violates PRD-1.2: no evidence of what schedulers actually struggle with.
```

## Edge Cases & Warnings
- "We know the problem — IROP recovery is slow" is not a validated problem statement; quantified evidence of scheduler behavior is required
- Problem validation must include both schedulers AND crew members — their pain points diverge
