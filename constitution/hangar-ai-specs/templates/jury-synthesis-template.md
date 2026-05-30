---
schema_version: 1
workflow: legacy-rescue-refactor
spec_id: <spec-id>
phase: <N>
subject: "<brief description of what is being reviewed>"
artifact_under_review: phase-N-<name>.html
timestamp: <ISO-8601>

juror_count: 5
distinct_models_required: true
jurors:
  - id: J1
    role: <role title>
    model: <model-id>
  - id: J2
    role: <role title>
    model: <model-id>
  - id: J3
    role: <role title>
    model: <model-id>
  - id: J4
    role: <role title>
    model: <model-id>
  - id: J5
    role: <role title>
    model: <model-id>

rounds:
  r1_completed: true
  r2_completed: true

verdict: APPROVED   # APPROVED | NEEDS_REVISION
---

# Multi-Cognition Jury Synthesis — Phase <N>

> **Workflow:** legacy-rescue-refactor  
> **Phase:** <N> — <Phase Name>  
> **Subject:** <brief description>  
> **Timestamp:** <ISO-8601>

---

## Round 1 — Individual Juror Deliberations

### J1 — <Role Title> (<Model>)

**Analysis:**
<!-- Juror's independent assessment of the artifact. What does this juror see through their
     specialist lens? What constitutional articles are relevant? -->

**Key finding:**
<!-- The single most important observation from this juror's perspective -->

**Proposed changes / concerns:**
<!-- Specific, actionable recommendations -->

**Confidence:** <HIGH | MEDIUM | LOW> — <brief rationale>

---

### J2 — <Role Title> (<Model>)

**Analysis:**
<!-- ... -->

**Key finding:**
<!-- ... -->

**Proposed changes / concerns:**
<!-- ... -->

**Confidence:** <HIGH | MEDIUM | LOW> — <brief rationale>

---

### J3 — <Role Title> (<Model>)

**Analysis:**
<!-- ... -->

**Key finding:**
<!-- ... -->

**Proposed changes / concerns:**
<!-- ... -->

**Confidence:** <HIGH | MEDIUM | LOW> — <brief rationale>

---

### J4 — <Role Title> (<Model>)

**Analysis:**
<!-- ... -->

**Key finding:**
<!-- ... -->

**Proposed changes / concerns:**
<!-- ... -->

**Confidence:** <HIGH | MEDIUM | LOW> — <brief rationale>

---

### J5 — <Role Title> (<Model>)

**Analysis:**
<!-- ... -->

**Key finding:**
<!-- ... -->

**Proposed changes / concerns:**
<!-- ... -->

**Confidence:** <HIGH | MEDIUM | LOW> — <brief rationale>

---

## Round 2 — Cross-Juror Synthesis

### Converging Themes

<!-- List the findings or recommendations that multiple jurors arrived at independently.
     These carry the most weight — unanimous convergence = high confidence. -->

1. **<Theme 1>** — Identified by J1, J2, J3 (or all): <summary>
2. **<Theme 2>** — ...
3. **<Theme 3>** — ...

### Points of Divergence

| Point | J1/J2 position | J3/J4 position | J5 position |
|-------|----------------|----------------|-------------|
| <point> | <view> | <view> | <view> |

**Resolution:** <How divergence was resolved — e.g. approaches are additive, prioritise by urgency>

### Integrated Assessment

<!-- Unified evaluation drawing from all 5 deliberations. This is the R2 synthesis —
     it should be more than a summary; it should add insight from the cross-juror dialogue. -->

<Integrated assessment text>

---

## Judicial Synthesis Verdict

### Required Changes / Conditions

<!-- If APPROVED with conditions, list them here. If NEEDS_REVISION, list blocking issues. -->

1. <Required change or condition>
2. <Required change or condition>

### Ruling

**VERDICT: APPROVED**
<!-- or: VERDICT: NEEDS_REVISION — <blocking reason> -->

<Rationale: why this verdict, referencing constitutional articles>

---
*Judicial synthesis produced by: <synthesizer model>*  
*Jurors: J1 <model> · J2 <model> · J3 <model> · J4 <model> · J5 <model>*  
*Timestamp: <ISO-8601>*
