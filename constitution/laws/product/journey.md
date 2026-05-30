---
domain: product
article: III
title: User Journey Laws
laws:
  - id: PRD-3.1
    title: Persona Development Law
    summary: User personas MUST be evidence-based, not fictional, based on minimum 5 interviews
  - id: PRD-3.2
    title: Journey Mapping Law
    summary: User journeys MUST be mapped before solution design with stages, actions, touchpoints, emotions
  - id: PRD-3.3
    title: User Story Law
    summary: User stories SHALL follow standard format with acceptance criteria
  - id: PRD-3.4
    title: Experience Principles Law
    summary: Products MUST define guiding experience principles
---

<!-- SPDX-FileCopyrightText: 2026 Click Chain AI -->
<!-- SPDX-License-Identifier: LicenseRef-ClickChain-Proprietary -->
# Article III: User Journey Laws

## Section 3.1: Persona Development Law

**Law ID:** `PRD-3.1`

User personas MUST be evidence-based, not fictional.

### Persona Requirements

- Based on real user interviews (minimum 5)
- Include behavioral attributes (not just demographics)
- Document goals, frustrations, and context
- Update quarterly based on new evidence

### Persona Template

```markdown
## [Persona Name]

**Who they are:**
- Role/context: [Job title, situation]
- Goals: [What they're trying to achieve]
- Frustrations: [Current pain points]

**Evidence base:**
- Interviews: [N] conducted
- Data: [Usage patterns, segments]

**Key jobs to be done:**
1. [Primary JTBD]
2. [Secondary JTBD]

**Success looks like:**
[Observable outcome when their job is done well]
```

---

## Section 3.2: Journey Mapping Law

**Law ID:** `PRD-3.2`

User journeys MUST be mapped before solution design.

### Journey Map Requirements

1. **Stages** - Phases user goes through
2. **Actions** - What user does at each stage
3. **Touchpoints** - Where user interacts with product
4. **Emotions** - How user feels (pain points, delights)
5. **Opportunities** - Where we can improve

### Journey Map Template

```
Stage:       | Awareness | Consideration | Purchase | Onboarding | Usage | Advocacy
-------------|-----------|---------------|----------|------------|-------|----------
Actions      |           |               |          |            |       |
Touchpoints  |           |               |          |            |       |
Emotions     |           |               |          |            |       |
Pain Points  |           |               |          |            |       |
Opportunities|           |               |          |            |       |
```

---

## Section 3.3: User Story Law

**Law ID:** `PRD-3.3`

User stories SHALL follow standard format with acceptance criteria.

### Format

```
As a [persona],
I want to [action],
So that [outcome].

Acceptance Criteria:
- Given [context], when [action], then [result]
- Given [context], when [action], then [result]

Definition of Done:
- [ ] Acceptance criteria met
- [ ] Tested with users (if applicable)
- [ ] Analytics instrumented
- [ ] Documentation updated
```

---

## Section 3.4: Experience Principles Law

**Law ID:** `PRD-3.4`

Products MUST define guiding experience principles.

### Example Principles

1. **Speed over features** - A fast, simple experience beats slow, complex
2. **Transparency** - Users always know what's happening and why
3. **Progressive disclosure** - Start simple, reveal complexity as needed
4. **Forgiveness** - Easy to undo, hard to break things

### Principle Application

- Reference principles in design reviews
- Use principles to resolve design debates
- Test designs against principles
