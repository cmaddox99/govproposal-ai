---
avatar: avatar-product-network-automation
law: PRD-2.5
title: "Discovery Stage-Gate Law"
---

# PRD-2.5 — Discovery Stage-Gate Law: Network Automation Application

## What This Law Requires
Network automation discovery stages must progress sequentially with documented evidence gates. No stage may begin without the prior stage's exit criteria met and evidence filed in `hangar-ai-specs/`. No build work begins until all discovery stages are complete.

## Compliant Example

**Discovery Stage Gates: Network Change Automation Feature**

| Stage | Exit Criteria | Evidence Filed | Gate |
|-------|--------------|----------------|------|
| Stage A — Problem framing | Problem statement with ≥3 operator interviews | `hangar-ai-specs/changes/netauto-change-pipeline/stage-a-problem.md` | ✅ |
| Stage B — Current state mapping | Journey map with ≥5 workflow steps and ≥2 documented failure modes | `hangar-ai-specs/changes/netauto-change-pipeline/stage-b-journey.md` | ✅ |
| Stage C — Opportunity sizing | Quantified impact: time cost, incident frequency, audit gap | `hangar-ai-specs/changes/netauto-change-pipeline/stage-c-sizing.md` | ✅ |
| Stage D — Solution hypothesis | Hypothesis statement + riskiest assumptions identified | `hangar-ai-specs/changes/netauto-change-pipeline/stage-d-hypothesis.md` | ✅ |
| Stage E — Assumption validation | Riskiest assumptions tested (prototype or interview) | `hangar-ai-specs/changes/netauto-change-pipeline/stage-e-validation.md` | ✅ |
| Stage F — Build decision | PRD-5.1 MVP scope agreed; compliance gate and audit trail in scope | `hangar-ai-specs/changes/netauto-change-pipeline/stage-f-decision.md` | ✅ |

**Stage E example — Assumption validation:**
Riskiest assumption: "Engineers will trust an automated compliance gate and not seek workarounds."
Validation method: Prototype walkthrough with 4 engineers.
Finding: 3/4 trusted the gate when shown the CAB approval check output. 1/4 wanted a manual override option — documented for v1.1 scope.
Result: Assumption VALIDATED with scope note.

**Constitutional check:** PRD-2.5 — all 6 discovery stages complete with evidence filed before specification work begins on the change automation pipeline.

## Violation Example
```
❌ Team moves from "here's the problem" directly to writing API specs.
   → Stages B through F skipped: no current-state journey map, no opportunity sizing,
     no hypothesis, no assumption validation.
   → Violates PRD-2.5: build work beginning without stage gate evidence is prohibited.
   → Result: API designed for a workflow that doesn't match how engineers actually work
     (discovered 2 sprints in during QA testing).
```

## Edge Cases & Warnings
- Stage gates are sequential — Stage C cannot begin before Stage B evidence is filed, even if the team "knows" the answer
- A stage can be completed quickly (hours, not weeks) if evidence already exists — the gate is about documentation, not cycle time
- External deadline pressure does not grant a stage gate exception — file a formal assumption log and flag the risk explicitly
