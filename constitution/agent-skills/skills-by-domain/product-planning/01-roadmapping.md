---
skill:
  id: skill-01-roadmapping
  name: Roadmapping
  category: planning
  version: "2.0.0"

laws:
  implements:
    - id: PRD-4.1
      title: Outcome-Based Roadmap Law
    - id: PRD-4.2
      title: Prioritization Framework Law
    - id: PRD-4.3
      title: Dependency Management Law
    - id: PRD-4.4
      title: Communication Cadence Law
  references:
    - id: PRD-1.3
      title: Outcome-Driven Law

triggers:
  phrases:
    - "Create a roadmap"
    - "Plan the product direction"
    - "Prioritize the backlog"
    - "What should we build next?"

followed_by:
  - skill-02-user-journey-mapping
  - skill-spec-governance
---

# Skill: Roadmapping

> **Purpose:** Create outcome-focused product roadmaps that guide development without over-committing to specific solutions.

---

## Purpose

Roadmapping is the practice of planning product direction at a strategic level. A good roadmap:

1. **Communicates direction** - Shows where the product is headed
2. **Aligns stakeholders** - Creates shared understanding of priorities
3. **Enables flexibility** - Focuses on outcomes, not specific features
4. **Guides decisions** - Helps teams prioritize day-to-day work

This skill follows the **Now/Next/Later** framework rather than fixed timelines, allowing adaptation to learning and change.

---

## When to Invoke

Invoke this skill when:

- Starting a new product or major initiative
- Planning quarterly or annual product direction
- Prioritizing a backlog of potential features
- Communicating strategy to stakeholders
- Aligning multiple teams on shared goals

**Trigger phrases:**
- "What should we build next?"
- "What's the product vision?"
- "Help me prioritize these features"
- "Create a roadmap for this initiative"

---

## Constitutional Foundation

### Product Constitution
- **Article IV, Section 4.1** - Roadmap Laws: "Roadmaps show direction, not promises"
- **Article IV, Section 4.2** - Outcome Focus: "Outcomes over outputs"
- **Article IV, Section 4.3** - Flexibility: "Plans adapt to learning"

### Business Constitution
- **Article I, Section 1.1** - Value Delivery: "Prioritize by business value"
- **Article III, Section 3.1** - Strategic Alignment: "Work connects to strategy"

### Engineering Constitution
- **Article I, Section 1.2** - Sustainable Pace: "Realistic capacity planning"

---

## Method

### Step 1: Clarify the Vision

Before roadmapping, establish the destination:

**Guiding Questions:**
- What does success look like in 1 year? 3 years?
- What problem are we ultimately solving?
- Who are we solving it for?
- What makes our solution unique?

**Output:** Vision statement (1-2 sentences)

### Step 2: Identify Strategic Themes

Group work into 3-5 strategic themes:

**Guiding Questions:**
- What are the major areas of investment?
- What capabilities do we need to build?
- What user problems need solving?

**Theme Format:**
```
Theme: [Name]
Objective: [What we're trying to achieve]
Key Results: [How we'll measure success]
```

### Step 3: Gather Inputs

Collect information from multiple sources:

| Source | What to Gather |
|--------|----------------|
| User Research | Pain points, unmet needs, JTBD |
| Business Goals | Revenue targets, market expansion |
| Technical Debt | Infrastructure needs, maintenance |
| Competitive Analysis | Market gaps, threats |
| Support/Sales | Common requests, blockers to deals |

### Step 4: Generate Outcome Statements

Write outcomes (not features) for each theme:

**Bad (Feature/Output):**
- "Add dark mode"
- "Build notification system"
- "Create admin dashboard"

**Good (Outcome):**
- "Users can work comfortably in any lighting condition"
- "Users never miss important updates"
- "Administrators can manage users efficiently"

### Step 5: Apply Now/Next/Later Framework

Categorize outcomes into time horizons:

| Horizon | Characteristics | Confidence |
|---------|-----------------|------------|
| **NOW** | Currently working on, well-defined | High |
| **NEXT** | Coming soon, shape is forming | Medium |
| **LATER** | Future possibilities, exploratory | Low |

**Guiding Questions for Prioritization:**
- What's most valuable to users right now?
- What reduces the biggest risk?
- What unblocks other work?
- What aligns with current strategy?

### Step 6: Add Context and Dependencies

For each outcome in NOW and NEXT:

- **Why now?** - Strategic rationale
- **Success metrics** - How we'll measure
- **Dependencies** - What needs to happen first
- **Risks** - What could go wrong

### Step 7: Review and Communicate

**Review with stakeholders:**
- Does this align with business goals?
- Is the prioritization defensible?
- Are there critical gaps?

**Communicate clearly:**
- NOW = Commitment (we're doing this)
- NEXT = Direction (we're planning this)
- LATER = Possibility (we're considering this)

---

## Quality Checklist

Before considering the roadmap complete:

- [ ] **Vision Clear:** One-sentence vision that guides all decisions
- [ ] **Themes Defined:** 3-5 strategic themes that group work
- [ ] **Outcomes Focused:** Items describe user outcomes, not features
- [ ] **Rationale Included:** Each item explains "why now"
- [ ] **Metrics Defined:** Success can be measured
- [ ] **Dependencies Mapped:** Prerequisites are identified
- [ ] **Risks Acknowledged:** Known risks are documented
- [ ] **Confidence Appropriate:** NOW is concrete, LATER is exploratory
- [ ] **Stakeholder Aligned:** Key stakeholders have reviewed

---

## Skill Interactions

### Preceded By
- **02-User Journey Mapping** - Provides user insights for prioritization

### Followed By
- **03-Executable Spec** - Defines acceptance criteria for NOW items
- **07-Vertical Slice Dev** - Breaks outcomes into implementation slices

### Related Skills
- **05-Business Rules** - Rules may drive roadmap priorities
- **04-Business Domain Modeling** - Domain understanding informs themes

> 📎 Examples: See 01-roadmapping-examples.md
