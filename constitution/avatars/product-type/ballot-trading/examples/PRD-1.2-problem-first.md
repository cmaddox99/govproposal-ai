---
avatar: avatar-product-ballot-trading
law: PRD-1.2
title: "Problem-First Law"
---

# PRD-1.2 — Problem-First Law: Ballot Trading Application

## What This Law Requires

No solution work for the ballot trading platform may begin until the pilot trip-trading problem is validated with evidence. Proposing batch-trade engines or eligibility UI redesigns without documented pilot pain points is prohibited.

## Compliant Example

**Problem Statement: Batch Ballot Submission Friction (Evidence-Validated)**

```
Problem: During monthly ballot periods, line pilots submit up to 40 trade requests
manually, one at a time through the DOTC Portal. Pilots with seniority to win
multiple trades are forced to re-enter pairing IDs and availability windows
repeatedly, with no indication of which prior submissions conflict.

Evidence:
- 7/8 pilots interviewed: manual re-entry is the #1 source of ballot-period
  frustration (base domiciles DFW, CLT, MIA)
- Session replay analysis: average pilot revisits the submission form 6.2 times
  per ballot period; 22% of sessions end in abandonment before submission
- Scheduler call logs: 38% of pilot calls during ballot week are "did my trade go
  through?" — confirming lack of submission feedback, not CBA questions

Validated: Yes — 8 pilot interviews + 3-month session replay dataset (Q1 2026)
```

**Gate:** This problem statement is filed in `hangar-ai-specs/changes/` before any
feature specification work (bulk submission, smart conflict detection) begins.

**Constitutional check:** PRD-1.2 — solution scope (batch input, conflict preview)
defined only after the re-entry and feedback-gap problem is validated with
interview evidence and behavioral telemetry.

## Violation Example

```
❌ "Pilots need a smarter ballot experience — let's add AI-ranked trade suggestions."
   → Solution proposed without a validated problem statement.
   → No evidence of what specific step in the trade flow pilots actually struggle with.
   → Violates PRD-1.2: no quantified pilot behavior or interview data filed.
```

## Edge Cases & Warnings

- "Pilots complain about ballot trading" is not a validated problem statement;
  the complaint must be localized to a specific step, reason code, or system with
  measured frequency.
- Problem validation must include pilots across seniority quintiles and domiciles —
  senior pilots and junior pilots experience trade friction differently.
- CBA rule changes can redefine what the problem is mid-discovery; re-validate
  the problem statement if a new CBA cycle opens before spec work begins.
