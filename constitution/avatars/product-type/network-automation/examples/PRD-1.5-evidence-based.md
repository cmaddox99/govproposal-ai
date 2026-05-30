---
avatar: avatar-product-network-automation
law: PRD-1.5
title: "Evidence-Based Decision Law"
---

# PRD-1.5 — Evidence-Based Decision Law: Network Automation Application

## What This Law Requires
All network automation feature prioritization and scope decisions must be supported by evidence — interview data, incident counts, ticket analysis, or validated assumptions. Opinion-only prioritization is prohibited.

## Compliant Example

**Feature Prioritization Decision: Automated Rollback (v1.1 vs MVP)**

```
Decision: Defer automated rollback to v1.1. Ship manual rollback (snapshot-based) in MVP.

Evidence supporting deferral:
- 6/8 engineers: manual rollback is painful (20–90 min) but occurs ~2×/month
- Incident data: 3 P1s in 6 months — none caused by rollback failure, all caused by
  out-of-window push or missing audit trail
- Risk assessment: automated rollback that itself fails silently would be worse than
  manual rollback — validated in 3 incident post-mortems
- PRD-5.1 MVP gate: compliance gate and audit trail must ship first; rollback automation
  is high-value but does not address the #1 failure modes

Evidence against shipping in MVP:
- No existing rollback mechanism to automate — must build snapshot infrastructure
- Rollback failure rate unknown without production data — premature optimization risk
- Engineer interviews: "knowing I have a clean snapshot is enough for v1"

Decision logged: hangar-ai-specs/changes/netauto-v1-scope/PROPOSAL.md
```

**Constitutional check:** PRD-1.5 — feature scope decision backed by incident data and engineer interviews, not team preference or perceived engineering elegance.

## Violation Example
```
❌ "We should include automated rollback in v1 — it's a critical safety feature."
   → Opinion-only prioritization ("should", "critical" without evidence).
   → Violates PRD-1.5: what incident data supports rollback being MVP-blocking?
     If the #1 failure modes are out-of-window pushes (compliance gate) and missing
     audit trails, those must ship first per PRD-5.1.
```

## Edge Cases & Warnings
- "Best practice" is not evidence — it must be grounded in this domain's specific failure modes
- Negative evidence (data showing a feature is NOT the priority) is as valuable as positive evidence
- Decisions made without evidence must be flagged as assumptions and validated before the next planning cycle
