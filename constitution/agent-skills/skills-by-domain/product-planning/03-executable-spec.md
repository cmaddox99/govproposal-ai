---
skill:
  id: skill-03-executable-spec
  name: Executable Specification
  category: specification
  version: "2.0.0"

laws:
  implements:
    - id: PRD-3.3
      title: User Story Law
    - id: ENG-4.1
      title: Atomic TDD Law
    - id: ENG-4.4
      title: Test Structure Law
  references:
    - id: PRD-3.4
      title: Acceptance Criteria Law
    - id: ENG-4.2
      title: Test Pyramid Law

triggers:
  phrases:
    - "Write acceptance criteria"
    - "Create Gherkin specs"
    - "Define feature behavior"
    - "What are the acceptance criteria?"

followed_by:
  - skill-06-atomic-tdd
  - skill-07-vertical-slice-dev
---

# Skill: Executable Specification

> **Purpose:** Create business-readable specifications that serve as both documentation and automated tests.

---

## Purpose

Executable Specifications bridge the gap between business requirements and technical implementation. Written in Gherkin format (Given/When/Then), they serve as:

1. **Living documentation** - Always reflects current system behavior
2. **Acceptance criteria** - Clear definition of "done"
3. **Automated tests** - Verifiable through BDD frameworks
4. **Communication tool** - Shared language between business and technical teams

---

## When to Invoke

Invoke this skill when:

- Starting a new feature or user story
- Clarifying acceptance criteria with stakeholders
- Documenting expected behavior before implementation
- Creating regression tests for existing functionality
- Resolving ambiguity about what the system should do

**Trigger phrases:**
- "What are the acceptance criteria?"
- "How should this feature behave?"
- "Let's write the spec first"
- "Define the expected behavior"

---

## Constitutional Foundation

### Engineering Constitution
- **Article IV, Section 4.1** - Test-First Development: Specifications precede implementation
- **Article IV, Section 4.3** - Behavior Verification: Tests describe behavior, not implementation

### Product Constitution
- **Article III, Section 3.2** - User Story Laws: Stories have clear acceptance criteria
- **Article V, Section 5.1** - Traceability: All work traces to user value

### Business Constitution
- **Article II, Section 2.1** - Business Rules: Rules are explicit and testable
- **Article III, Section 3.3** - Compliance Verification: Requirements are auditable

---

## Method

### Step 1: Identify the Feature

Start with the user's perspective:

**Guiding Questions:**
- Who is the user performing this action?
- What are they trying to accomplish?
- What value do they receive?

**Format:**
```gherkin
Feature: [Feature Name]
  As a [role]
  I want [capability]
  So that [benefit]
```

### Step 2: Define the Happy Path

Document the primary success scenario first:

**Guiding Questions:**
- What is the most common use case?
- What does success look like?
- What state changes occur?

**Format:**
```gherkin
Scenario: [Descriptive name of happy path]
  Given [initial context]
  When [action taken]
  Then [expected outcome]
```

### Step 3: Identify Edge Cases

Systematically explore boundaries and alternatives:

**Edge Case Categories:**
- **Validation failures** - Invalid input, missing data
- **Authorization failures** - Unauthorized users, expired sessions
- **Business rule violations** - Limits exceeded, conflicts
- **State conflicts** - Concurrent modifications, stale data
- **Integration failures** - External service unavailable

### Step 4: Document Edge Cases

Write scenarios for each significant edge case:

```gherkin
Scenario: [Edge case description]
  Given [context that creates edge case]
  When [action taken]
  Then [expected handling]
```

### Step 5: Add Examples for Data Variations

Use Scenario Outlines for data-driven scenarios:

```gherkin
Scenario Outline: [Parameterized scenario]
  Given [context with <parameter>]
  When [action with <input>]
  Then [outcome with <expected>]

  Examples:
    | parameter | input | expected |
    | value1    | x     | result1  |
    | value2    | y     | result2  |
```

### Step 6: Review and Validate

Before finalizing:

- [ ] Business stakeholder can read and understand
- [ ] All acceptance criteria are covered
- [ ] Edge cases are comprehensive
- [ ] No implementation details leaked
- [ ] Scenarios are independent (no ordering dependencies)

---

## Quality Checklist

Before considering the specification complete:

- [ ] **Readable:** A business stakeholder can understand every scenario
- [ ] **Complete:** All acceptance criteria from the story are covered
- [ ] **Independent:** Each scenario can run in isolation
- [ ] **Consistent:** Terminology matches the ubiquitous language
- [ ] **Automatable:** Every step can be implemented in a test framework
- [ ] **Traced:** Specification links to user story/Hangar SDD proposal
- [ ] **Reviewed:** Validated with product owner and domain experts

---

## Skill Interactions

### Preceded By
- **02-User Journey Mapping** - Provides context for what to specify
- **05-Business Rules** - Provides rules to encode in scenarios

### Followed By
- **07-Vertical Slice Dev** - Slices implementation based on scenarios
- **06-Atomic TDD** - Implements step definitions and production code

### Related Skills
- **04-Business Domain Modeling** - Ubiquitous language alignment
- **08-Code Review** - Verifies specs match implementation

> 📎 Examples: See 03-executable-spec-examples.md
