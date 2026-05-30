---
avatar: avatar-product-network-automation
law: PRD-6.2
title: "Retention Over Acquisition Law"
---

# PRD-6.2 — Retention Over Acquisition Law: Network Automation Application

## What This Law Requires
For internal tooling, "retention" means keeping existing network engineers and NOC operators productive, engaged, and not resorting to shadow workflows. Feature depth for current users must be prioritized over expanding the tool to new teams or adding surface-area features. Fixing friction for the 8 existing network engineers is more valuable than onboarding 8 more.

## Compliant Example

**Feature Prioritization: Deepen vs. Expand**

```
Scenario: Q2 planning. Two proposals competing for sprint capacity:

Proposal A — Expand: Add PaaS subnet provisioning workflow for the Cloud team (new user group).
  - Adds 12 new users; no changes for existing network engineers.
  - No current friction data collected from Cloud team.

Proposal B — Retain: Add post-push diff verification for existing change pipeline.
  - Eliminates "silent verification failures" — the 3rd most common failure mode (5 incidents/6mo).
  - Addresses pain reported by 6/8 current users in discovery interviews.

PRD-6.2 analysis:
  - Current user NPS proxy: 4/8 engineers use the tool for ALL changes (50% adoption).
  - 4/8 engineers still use manual CLI for "high-risk" changes — citing lack of post-push verification.
  - Post-push verification (Proposal B) would close the adoption gap for existing users.
  - Expansion (Proposal A) adds new users without improving retention of current 50%.

Decision: Prioritize Proposal B (post-push verification). Proposal A moves to Q3 after
retention metric ≥80% of current engineers using the tool for all change types.
```

**Retention metric definition for network automation:**
- Primary: % of eligible network changes processed through the automation platform (vs. manual CLI bypass)
- Target: ≥80% of changes in scope before expanding to new user groups
- Secondary: Engineer-reported confidence score ("would you use this for a P1 change?")

**Constitutional check:** PRD-6.2 — retention of existing engineers prioritized over acquisition of new user groups. Expansion gated on retention threshold.

## Violation Example
```
❌ Roadmap: "Add support for Cloud, Security, and Platform teams in Q2."
   → 50% of current network engineers still bypass the tool for high-risk changes.
   → Violates PRD-6.2: acquiring new user groups while current users have unresolved
     friction compounds the friction problem across more users.
   → The post-push verification gap (known failure mode) will follow Cloud and Security
     teams into their onboarding experience.
```

## Edge Cases & Warnings
- "Retention" for an internal tool is measured by adoption depth, not login frequency — a tool used for 50% of changes has 50% retention even if users log in daily for the other 50% manually
- New user group requests are signals, not commitments — validate that current user friction is resolved first
- PRD-6.2 does not mean never expand — it means establish a retention threshold before expanding, and meet it
