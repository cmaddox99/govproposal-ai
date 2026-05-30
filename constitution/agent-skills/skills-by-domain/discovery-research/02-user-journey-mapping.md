---
skill:
  id: skill-02-user-journey-mapping
  name: User Journey Mapping
  category: discovery
  version: "2.0.0"

laws:
  implements:
    - id: PRD-3.1
      title: Journey Mapping Law
    - id: PRD-3.2
      title: Pain Point Documentation Law
    - id: PRD-2.3
      title: Opportunity Sizing Law
  references:
    - id: PRD-1.2
      title: Problem-First Law
    - id: PRD-2.1
      title: User Research Law

triggers:
  phrases:
    - "Map the user journey"
    - "Understand user pain points"
    - "What problems do users face?"
    - "Discovery for new feature"

followed_by:
  - skill-03-executable-spec
  - skill-04-business-domain-modeling
---

# Skill: User Journey Mapping

> **Purpose:** Understand user problems and opportunities by mapping their complete experience.

---

## Purpose

User Journey Mapping is the practice of visualizing a user's complete experience as they try to accomplish a goal. This skill:

1. **Reveals pain points** - Shows where users struggle
2. **Identifies opportunities** - Highlights where we can add value
3. **Builds empathy** - Connects teams to real user experiences
4. **Guides prioritization** - Focuses effort on highest-impact areas

Journey maps focus on the **problem space** (what users experience) before jumping to the **solution space** (what we build).

---

## When to Invoke

Invoke this skill when:

- Starting discovery for a new feature or product
- Trying to understand user pain points
- Prioritizing what to build next
- Onboarding new team members to user context
- Validating that proposed solutions address real problems

**Trigger phrases:**
- "What problems do users have?"
- "Why are users struggling with X?"
- "Help me understand the user experience"
- "Map the user journey for this feature"

---

## Constitutional Foundation

### Product Constitution
- **Article III, Section 3.1** - User Journey Laws: "Understand the journey before building the solution"
- **Article III, Section 3.2** - Pain Point Priority: "Prioritize reducing friction"
- **Article II, Section 2.1** - User Research: "Decisions based on evidence, not assumptions"

### Business Constitution
- **Article I, Section 1.1** - Value Creation: "Value comes from solving real problems"
- **Article IV, Section 4.1** - Customer Understanding: "Know thy customer"

### Engineering Constitution
- **Article I, Section 1.1** - Purpose: "Software exists to solve user problems"

---

## Method

### Step 1: Define the Scope

Establish boundaries for the journey:

**Guiding Questions:**
- Who is the user? (persona or segment)
- What are they trying to accomplish? (goal)
- Where does the journey start and end?
- What touchpoints are included?

**Output:**
```
Persona: [User type]
Goal: [What they're trying to achieve]
Scope: From [starting point] to [ending point]
Touchpoints: [Channels/products involved]
```

### Step 2: Identify Journey Stages

Break the journey into distinct phases:

**Common Stage Patterns:**
- Awareness → Consideration → Decision → Use → Advocacy
- Discover → Evaluate → Purchase → Onboard → Use → Renew
- Trigger → Search → Compare → Choose → Act → Review

**For each stage:**
- What is the user trying to do?
- What signals they've moved to this stage?
- What does success look like?

### Step 3: Map Actions and Touchpoints

For each stage, document:

| Element | Description |
|---------|-------------|
| **Actions** | What the user does (verbs) |
| **Touchpoints** | Where they interact (channels, products) |
| **Questions** | What they're wondering |
| **Tools Used** | Systems, devices, resources |

### Step 4: Capture Emotional Experience

Map the emotional arc:

**Emotional States:**
- Confident / Uncertain
- Frustrated / Delighted
- Confused / Clear
- Anxious / Calm
- Empowered / Helpless

**Guiding Questions:**
- How does the user feel at this stage?
- What causes positive emotions?
- What causes negative emotions?
- Where are the emotional peaks and valleys?

### Step 5: Identify Pain Points

Document where users struggle:

**Pain Point Categories:**
- **Process Pain:** Too many steps, too slow
- **Information Pain:** Can't find what they need
- **Trust Pain:** Uncertainty, lack of confidence
- **Support Pain:** Can't get help when needed
- **Technical Pain:** Errors, bugs, poor performance

**Rate severity:** Critical / High / Medium / Low

### Step 6: Identify Opportunities

Find where you can add value:

**Opportunity Types:**
- **Remove friction:** Eliminate unnecessary steps
- **Add clarity:** Provide better information
- **Build confidence:** Reduce uncertainty
- **Anticipate needs:** Proactive assistance
- **Create delight:** Exceed expectations

### Step 7: Connect to Jobs-to-be-Done

Frame insights in JTBD format:

```
When [situation/trigger]
I want to [motivation/action]
So I can [expected outcome]
```

**Example:**
```
When I'm checking out with a full cart
I want to see the total including shipping
So I can decide if the purchase fits my budget
```

### Step 8: Synthesize and Prioritize

Create actionable summary:

- Top 3-5 pain points to address
- Top 3-5 opportunities to explore
- Quick wins vs. strategic investments
- Areas needing more research

---

## Quality Checklist

Before considering the journey map complete:

- [ ] **Scoped:** Clear persona, goal, and boundaries defined
- [ ] **Complete:** All stages from trigger to outcome covered
- [ ] **User-Centered:** Written from user perspective, not product perspective
- [ ] **Evidence-Based:** Pain points backed by research data
- [ ] **Emotional:** Emotional journey captured throughout
- [ ] **Actionable:** Clear pain points and opportunities identified
- [ ] **Prioritized:** Pain points ranked by severity and impact
- [ ] **Connected:** JTBD statements link to product decisions

---

## Skill Interactions

### Preceded By
- User research activities (interviews, surveys, analytics)

### Followed By
- **01-Roadmapping** - Journey insights inform roadmap priorities
- **03-Executable Spec** - Pain points become acceptance criteria
- **05-Business Rules** - Journey reveals business rule needs

### Related Skills
- **04-Business Domain Modeling** - Journey context informs domain boundaries
- **07-Vertical Slice Dev** - Slices organized around journey stages

> 📎 Examples: See 02-user-journey-mapping-examples.md
