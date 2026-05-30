---
avatar: avatar-product-network-automation
law: PRD-1.1
title: "Customer-Centric Law"
---

# PRD-1.1 — Customer-Centric Law: Network Automation Application

## What This Law Requires
Discovery research must surface the actual pain points of network engineers, NOC operators, and IT change managers — not assumed throughput or API-capability metrics.

## Compliant Example

**Discovery Sprint: Network Change Workflow Pain Points**

Continuous discovery findings (from 8 network engineer interviews + 4 NOC operator interviews + 3 IT change manager interviews):

| Persona | Pain Point | Evidence Signal |
|---------|-----------|-----------------|
| Network Engineer | Must manually cross-reference Nautobot, ServiceNow, and device CLI to validate a change before submitting | 7/8 engineers; avg 45 min per change request |
| Network Engineer | No automated rollback — manually reverting device config takes 20–90 min post-failed change | 6/8 engineers; 3 P1 incidents cited in last quarter |
| NOC Operator | MOCCA alerts don't include the change ID that triggered the anomaly — can't correlate event to change | 4/4 NOC operators; root cause analysis slowed by 30+ min |
| IT Change Manager | Approving CAB requests requires manually validating device targets against Nautobot inventory | 3/3 change managers; 2–4 hr CAB prep per week |

**Outcome:** Discovery confirms that the #1 network engineer need is **consolidated change validation view at request time** (Nautobot inventory + change window + rollback plan in one workflow), not raw automation throughput.

**Constitutional check:** PRD-1.1 — operator pain (cross-system validation friction) drives feature priority, not API capability or throughput assumption.

## Violation Example
```
❌ "We need to reduce mean time to push network changes by 40%."
   → Metric-first without interviewing network engineers or NOC operators.
   → Violates PRD-1.1: output metric assumed, not discovered from operator behavior.
```

## Edge Cases & Warnings
- Network engineers and NOC operators have different visibility needs — discovery must interview both; do not proxy NOC needs through engineer accounts
- IT change managers are often excluded from discovery — include them; they surface change compliance gaps that cause audit failures months later
- Latent pain points surface in post-incident reviews — include post-mortem retrospectives as a discovery input alongside structured interviews
