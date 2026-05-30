---
domain: product
article: V
title: MVP & Experimentation Laws
laws:
  - id: PRD-5.1
    title: MVP Law
    non_negotiable: true
    summary: MVPs SHALL be the smallest experiment to validate learning, not a crappy first version
  - id: PRD-5.2
    title: Build-Measure-Learn Law
    summary: All product development SHALL follow the BML loop
  - id: PRD-5.3
    title: Experiment Design Law
    summary: Experiments MUST be designed rigorously with hypothesis, metrics, and success criteria
  - id: PRD-5.4
    title: Feature Flag Law
    summary: New features SHOULD be behind feature flags for gradual rollout
---

<!-- SPDX-FileCopyrightText: 2026 Click Chain AI -->
<!-- SPDX-License-Identifier: LicenseRef-ClickChain-Proprietary -->
# Article V: MVP & Experimentation Laws

## Section 5.1: Minimum Viable Product Law

**Law ID:** `PRD-5.1` | **Status:** NON-NEGOTIABLE

MVPs SHALL be the smallest experiment to validate learning.

### MVP is NOT

- A crappy first version
- A feature-poor product
- An excuse for bad quality

### MVP IS

- The smallest thing that tests our riskiest assumption
- Good enough quality to get honest feedback
- Instrumented to measure the hypothesis

### MVP Criteria

```
Hypothesis: [What we believe]
Riskiest Assumption: [What could prove us wrong]
MVP Approach: [How we'll test it]
Success Metric: [What we'll measure]
Minimum Threshold: [What success looks like]
Timeline: [How long we'll run the experiment]
```

---

## Section 5.2: Build-Measure-Learn Law

**Law ID:** `PRD-5.2`

All product development SHALL follow the BML loop:

```
     IDEAS
       │
       ▼
   ┌───────┐
   │ BUILD │ ← Minimize time through the loop
   └───┬───┘
       │
       ▼
   PRODUCT
       │
       ▼
  ┌─────────┐
  │ MEASURE │ ← Actionable metrics, not vanity
  └────┬────┘
       │
       ▼
     DATA
       │
       ▼
   ┌───────┐
   │ LEARN │ ← Validated learning, pivot or persevere
   └───┬───┘
       │
       └──────────────→ IDEAS
```

---

## Section 5.3: Experiment Design Law

**Law ID:** `PRD-5.3`

Experiments MUST be designed rigorously.

### Experiment Template

```markdown
## Experiment: [Name]

### Hypothesis
We believe [action/change]
Will result in [outcome]
For [user segment]
Because [rationale]

### Metrics
Primary: [What we'll measure]
Secondary: [Supporting metrics]
Guardrail: [What we don't want to hurt]

### Design
Type: [ ] A/B Test [ ] Fake Door [ ] Wizard of Oz [ ] Concierge [ ] Other
Sample Size: [N] users
Duration: [X] weeks
Segments: [Who's included/excluded]

### Success Criteria
Minimum detectable effect: [X]%
Statistical significance: 95%
We will ship if: [Criteria]
We will kill if: [Criteria]
We will iterate if: [Criteria]

### Results
[To be filled after experiment]
```

---

## Section 5.4: Feature Flag Law

**Law ID:** `PRD-5.4`

New features SHOULD be behind feature flags.

### Benefits

- Gradual rollout (reduce risk)
- A/B testing capability
- Quick rollback if issues
- Customer-specific enablement

### Flag Lifecycle

1. **Created** (feature in development)
2. **Testing** (internal only)
3. **Beta** (select customers)
4. **Rollout** (gradual percentage)
5. **GA** (100%, flag removed)
6. **Cleanup** (code without flag)
