---
# Discovery Package Index — Tier 1 and Tier 2 Manifests
# Governed by: ENG-11.1, PRD-2.5
# Usage: Copy the appropriate tier manifest into hangar-ai-specs/changes/[discovery-id]/package-index.md
#        Mark each artifact as Required / Optional / Deferred at Stage A.
---

# Discovery Package Index — disc-YYYY-NNN

> **Discovery ID:** disc-YYYY-NNN
> **Tier:** <Tier 1 / Tier 2>
> **Declared at:** Stage A

---

## Tier Selection — Complexity Rubric

Answer the 5 questions below. If ≥3 answers are "Yes", select Tier 2. Otherwise Tier 1.

| # | Question | Answer |
|---|----------|:------:|
| 1 | Does the discovery span 3+ services or bounded contexts? | Yes / No |
| 2 | Are there 3+ stakeholder groups with distinct needs? | Yes / No |
| 3 | Does the domain involve regulatory or compliance constraints? | Yes / No |
| 4 | Is the expected implementation timeline > 1 quarter? | Yes / No |
| 5 | Does the discovery require cross-team coordination (2+ teams)? | Yes / No |

**Result:** <Tier 1 / Tier 2>

---

## Tier 1 Manifest (Simple, ≤1 service)

| # | Artifact | Status | Stage Produced |
|---|----------|:------:|:--------------:|
| 1 | discovery-guide | Required | F |
| 2 | worksheet-01-metrics-collection | Required | E |
| 3 | worksheet-02-persona-validation | Required | B |
| 4 | worksheet-03-codebase-assessment | Required | C |
| 5 | forward-roadmap | Required | F |
| 6 | slice-1-ready-brief | Required | F |

---

## Tier 2 Manifest (Complex, 3+ services)

| # | Artifact | Status | Stage Produced |
|---|----------|:------:|:--------------:|
| 1 | discovery-guide | Required | F |
| 2 | worksheet-01-metrics-collection | Required | E |
| 3 | worksheet-02-persona-validation | Required | B |
| 4 | worksheet-03-codebase-assessment | Required | C |
| 5 | worksheet-04-domain-model-inventory | Required | C |
| 6 | worksheet-05-agentic-workflow-discovery | Required | D |
| 7 | executive-briefing-deck | Required | F |
| 8 | forward-roadmap | Required | F |
| 9 | slice-1-ready-brief | Required | F |
| 10 | ado-gap-analysis-brief | Optional | D |
| 11 | discovery-prompt-guide | Optional | B |

---

## Reference Package (Tier 2)

> Worked example for all 6 stages (`.md` + rendered `.html`):

```
tools/templates/product-discovery/examples/partner-miles-reference/
```

> Extended Tier 2 reference (AA Hangar Labs):

```
/aa-hangar-labs/discovery-packages/service-recovery/complex-disruption-scenarios/
```
