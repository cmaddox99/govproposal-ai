---
law_id: PRD-1.2
avatar: crew-training-scheduling
---

# PRD-1.2: Problem-First Law Examples for Crew Training Scheduling

> **Law:** Before building any feature, the problem it solves MUST be validated with evidence.
> Product decisions driven by speculation, not user pain, produce unused features.

---

## COMPLIANT: Feature Backed by Validated Scheduler Pain

```markdown
## Feature Request: Sequential Open Blocked Sequence Run

### Problem Statement
Mid-range schedulers report that the standard optimizer run sometimes assigns
the same open blocked sequence to multiple students in a way that conflicts with
CKP availability — leaving sequences technically "saved" but practically unusable.

### Evidence (PRD-1.2 compliance)
- Qualitative: 3 scheduler interviews confirmed CKP conflicts are the primary
  reason they override optimizer recommendations
- Quantitative: 68% of overrides in APR2025 cited "CKP not available for
  assigned sequence" as the reason (from solution acceptance rate tracking)
- Operational: 12 sequences marked FIND (needs CKP) in the last 3 runs had
  no available CKPs within the freeze window

### Validated Problem
Run the optimizer once per open blocked sequence, sequentially, so each
sequence is saved only when a complete CKP-available assignment can be made.

### Feature: runOpenBlkdSeqSequentially config flag
Validates: reduces CKP-conflict overrides by ≥ 30%
```

**Why compliant:** The config flag `runOpenBlkdSeqSequentially` exists because scheduler interviews AND quantitative override data both confirm the problem. The feature is not speculation — it traces to measured pain.

---

## COMPLIANT: Problem-First Discovery Before Adding a New Reward

```markdown
## Proposed Reward: APD Leg Reward (jose-02 invocation)

### Problem Statement
UG (Upgrade) students are completing training without APD legs because the
optimizer selects shorter options that meet hour requirements but lack the APD.
Schedulers then manually add APD legs — creating rework.

### Evidence
- 4 scheduler interviews: "The optimizer keeps picking options without APD legs
  for UG students — we have to fix it every run"
- Metrics: In MAR2025, 7 of 9 UG students in the solution had no APD leg;
  all 7 required manual correction by Flight Standards
- Root cause: No reward incentivised APD leg retention → optimizer treated
  APD and non-APD options as equal

### Decision: Add APD leg reward to scoring pipeline
Validates: ≥ 80% of UG students in solution include APD leg without manual correction
```

**Why compliant:** Per PRD-1.2, the APD leg reward was not added because "it sounds good" — it was added because scheduler interviews AND run data both proved UG students were systematically missing APD legs. The success metric is defined before implementation.

---

## VIOLATION: Feature Built Without Problem Validation

```markdown
## Feature Request (VIOLATES PRD-1.2): Add "Preferred Base" Weight

Request from OR Scientist: "Let's add a weight that penalises students being
assigned to sequences at bases other than their domicile. It feels like it
would improve solution quality."

Status: Implemented directly based on "feels like" rationale.
```

**Why violates PRD-1.2:** "Feels like it would improve" is an assumption, not validated evidence. No scheduler was interviewed. No data on base-mismatch overrides was collected. The feature may solve a non-problem while adding complexity and making the scoring model harder to tune. Per PRD-1.2, the problem must be validated BEFORE the solution is designed.

**Correct approach:**
1. Interview 3+ schedulers: "Do you override recommendations because of base mismatches?"
2. Review override logs: What % cite base mismatch?
3. If validated → define the reward; if not → park the idea

---

## COMPLIANT: JTBD Framing for Scheduler Feature

```markdown
## Jobs-to-be-Done (PRD-2.3 format)

When open blocked sequences are at risk of spoiling,
I want to see which students can fill them without disrupting existing assignments,
So I can make scheduling decisions in minutes instead of hours.

When the optimizer produces a recommendation with CKP conflicts,
I want to know immediately which sequences need a CKP found,
So I can work those first before approving other changes.
```

**Why compliant:** JTBD framing separates the user's goal (fill sequences quickly, resolve CKP gaps) from the solution (optimizer run, CKP Actions sheet). This keeps the product team focused on the outcome — not on specific UI or algorithm choices.

