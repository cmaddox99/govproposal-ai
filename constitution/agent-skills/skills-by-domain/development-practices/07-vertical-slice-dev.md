---
skill:
  id: skill-07-vertical-slice-dev
  name: Vertical Slice Development
  category: development
  version: "2.0.0"

laws:
  implements:
    - id: ENG-2.3
      title: Vertical Slice Architecture Law
    - id: ENG-1.4
      title: Incremental Improvement Law
  references:
    - id: ENG-4.2
      title: Test Pyramid Law
    - id: PRD-5.1
      title: MVP Law

triggers:
  phrases:
    - "Break down the feature"
    - "Plan vertical slices"
    - "What's the smallest deployable slice?"
    - "Slice the work"

followed_by:
  - skill-06-atomic-tdd
  - skill-08-code-review
---

# Skill: Vertical Slice Development

> **Purpose:** Implement features as thin, end-to-end slices that deliver value incrementally.
> **Workflow:** See `workflows/greenfield-development.md` for the full 8-phase governed build sequence.

---

## Purpose

Vertical Slice Development is the practice of building software in thin, complete increments that cut through all architectural layers. Each slice:

1. **Delivers user value** - Something the user can see, use, or experience
2. **Is deployable** - Can be shipped independently
3. **Is testable end-to-end** - Verifiable from UI to database
4. **Minimizes work-in-progress** - Complete one slice before starting another

This contrasts with horizontal/layer-by-layer development where you build "all the database first, then all the API, then all the UI."

---

## When to Invoke

Invoke this skill when:

- Breaking down a feature into implementation tasks
- Planning sprint or iteration work
- Deciding what to build next
- Organizing work for multiple developers
- Estimating effort for a feature

**Trigger phrases:**
- "How should we break this down?"
- "What's the smallest valuable increment?"
- "How do we parallelize this work?"
- "What should we build first?"

---

## Constitutional Foundation

### Engineering Constitution
- **Appendix A** - Vertical Slice Architecture: "Build complete features, not layers"
- **Article III, Section 3.1** - Simplicity: "The simplest thing that could work"
- **Article IV, Section 4.1** - Test-First: "Each slice is testable end-to-end"

### Product Constitution
- **Article IV, Section 4.1** - Incremental Delivery: "Deliver value early and often"
- **Article III, Section 3.3** - User Value: "Every increment provides user value"

### Business Constitution
- **Article I, Section 1.2** - Time to Value: "Minimize time to first value"

---

## Method

### Step 1: Understand the Full Feature

Before slicing, understand the complete picture:

**Guiding Questions:**
- What is the user trying to accomplish?
- What are all the acceptance criteria?
- What are the main user flows?
- What are the edge cases and error states?

**Output:** Feature overview with all scenarios listed

### Step 2: Identify the Walking Skeleton

Find the thinnest possible end-to-end path:

**Definition:** A walking skeleton is a minimal implementation that exercises all architectural layers but contains minimal functionality.

**Guiding Questions:**
- What's the happy path with hardcoded values?
- What proves all layers can communicate?
- What could we demo in the simplest form?

**Example:**
```
Feature: User can add items to shopping cart

Walking Skeleton:
- UI: Single "Add to Cart" button (no product selection)
- API: POST /cart/items (hardcoded product)
- Domain: Cart.addItem() (no validation)
- Database: Save cart item (minimal fields)

Result: Clicking button adds a hardcoded item to cart
```

### Step 3: List All Behaviors

Enumerate every behavior the feature needs:

**Categories:**
- Happy path variations
- Validation behaviors
- Error handling
- Edge cases
- Authorization checks
- Notifications/side effects

**Format each behavior as:**
```
[User action] → [Expected outcome]
```

### Step 4: Order by Value and Risk

Prioritize slices using these criteria:

**Priority Matrix:**

| Criteria | Question |
|----------|----------|
| User Value | Does this enable a user to accomplish something? |
| Risk Reduction | Does this prove something uncertain? |
| Learning | Does this teach us something we need to know? |
| Dependency | Do other slices depend on this? |

**Order:** High value + high risk/learning first

### Step 5: Define Slice Boundaries

For each slice, define:

1. **Trigger:** How the slice starts (user action, event, etc.)
2. **Layers touched:** UI, API, Domain, Database, External services
3. **Outcome:** What the user sees when complete
4. **Acceptance criteria:** How we know it works

### Step 6: Verify Slice Independence

Check that each slice:

- [ ] Can be implemented without other pending slices
- [ ] Can be deployed independently
- [ ] Can be tested in isolation
- [ ] Provides value even if other slices aren't done

### Step 7: Create Slice Specifications

For each slice, create a mini-specification:

```markdown
## Slice: [Name]

**User Story:** As a [user], I can [action] so that [benefit]

**Layers:**
- [ ] UI: [what changes]
- [ ] API: [endpoints affected]
- [ ] Domain: [business logic]
- [ ] Database: [schema/queries]
- [ ] External: [integrations]

**Acceptance Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]

**Dependencies:** [None | List dependencies]
```

---

## Quality Checklist

Before considering a slice plan complete:

- [ ] **Walking Skeleton Identified:** First slice proves end-to-end connectivity
- [ ] **User Value:** Each slice delivers something users can see/use
- [ ] **Thin Slices:** Each slice is the smallest valuable increment
- [ ] **Independence:** Slices minimize dependencies on each other
- [ ] **Testable:** Each slice can be tested end-to-end
- [ ] **Deployable:** Each slice can be shipped independently
- [ ] **Prioritized:** Slices ordered by value and risk
- [ ] **Complete Coverage:** All acceptance criteria mapped to slices

---

## Skill Interactions

### Preceded By
- **03-Executable Spec** - Provides scenarios to slice
- **02-User Journey Mapping** - Provides understanding of user flow
- **01-Roadmapping** - Provides feature priorities

### Followed By
- **06-Atomic TDD** - Implements each slice
- **08-Code Review** - Reviews completed slices

### Related Skills
- **04-Business Domain Modeling** - Slices may reveal domain boundaries
- **05-Business Rules** - Rules inform slice complexity

> 📎 Examples: See 07-vertical-slice-dev-examples.md
