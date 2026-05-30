---
skill:
  id: skill-09-refactoring
  name: Refactoring
  category: quality
  version: "2.0.0"

laws:
  implements:
    - id: ENG-1.3
      title: Continuous Refactoring Law
    - id: ENG-3.1
      title: Complexity Limits
    - id: ENG-3.8
      title: Continuous Refactoring Patterns
  references:
    - id: ENG-4.1
      title: Atomic TDD Law
    - id: ENG-3.4
      title: Single Responsibility Principle

triggers:
  phrases:
    - "Refactor this code"
    - "Improve code structure"
    - "Code smells detected"
    - "Make this cleaner"

followed_by:
  - skill-08-code-review
  - skill-06-atomic-tdd
---

# Skill: Refactoring

> **Purpose:** Systematically improve code structure without changing external behavior, guided by tests and constitutional principles.
> **Workflow:** See `workflows/legacy-rescue-refactor.md` for the full 6-phase constitutional remediation sequence.

---

## Purpose

Refactoring is the disciplined practice of restructuring existing code without altering its observable behavior. This skill ensures:

1. **Continuous improvement** - Code quality improves over time, not just at creation
2. **Test-protected changes** - Every refactoring is verified by existing tests
3. **Incremental transformation** - Large improvements through small, safe steps
4. **Pattern application** - Known good patterns replace problematic structures
5. **Debt reduction** - Technical debt is systematically addressed

**Key principle:** Refactoring is NOT rewriting. It's a series of small, behavior-preserving transformations.

---

## When to Invoke

Invoke this skill when:

- Code smells are detected during review
- Adding features is harder than it should be
- Tests pass but code is difficult to understand
- Duplication exists across the codebase
- Preparing code for a new feature (make the change easy, then make the easy change)
- Technical debt items are prioritized for resolution

**Trigger phrases:**
- "This code is hard to follow"
- "Let's clean this up before adding the feature"
- "There's duplication here"
- "This class is doing too much"
- "Time to pay down some tech debt"

**Prerequisite:** Tests must exist and pass before refactoring begins.

---

## Constitutional Foundation

### Engineering Constitution
- **Article III, Section 3.1** - Simplicity: Refactor toward the simplest solution
- **Article IV, Section 4.1** - Test-First: Tests must exist before refactoring
- **Article IV, Section 4.3** - Behavior Focus: Refactoring preserves behavior
- **Article II, Section 2.1** - Code Quality: Maintainability is a requirement

### Product Constitution
- **Article IV, Section 4.1** - Incremental Delivery: Small, safe changes

### Business Constitution
- **Article II, Section 2.1** - Business Rules: Rules remain correctly implemented after refactoring

---

## Method: The Refactoring Cycle

### Step 1: Ensure Test Coverage

Before any refactoring:

**Verification:**
- [ ] Tests exist for the code being refactored
- [ ] All tests pass (GREEN)
- [ ] Coverage is sufficient to detect behavior changes

**If tests don't exist:** Write characterization tests first to capture current behavior.

```python
# Characterization test - captures current behavior
def test_existing_behavior_for_refactoring():
    """
    Characterization test: Documents current behavior before refactoring.
    If this test breaks during refactoring, behavior has changed.
    """
    result = legacy_function(known_input)
    assert result == captured_current_output
```

---

### Step 2: Identify the Smell

Recognize what needs improvement:

| Code Smell | Description | Common Refactorings |
|------------|-------------|---------------------|
| **Long Method** | Method doing too much | Extract Method |
| **Large Class** | Class with too many responsibilities | Extract Class |
| **Duplicate Code** | Same logic in multiple places | Extract Method, Pull Up Method |
| **Feature Envy** | Method uses another class's data excessively | Move Method |
| **Data Clumps** | Same group of data appears together | Extract Class, Introduce Parameter Object |
| **Primitive Obsession** | Overuse of primitives instead of objects | Replace Primitive with Object |
| **Switch Statements** | Complex conditionals on type | Replace Conditional with Polymorphism |
| **Speculative Generality** | Unused abstraction "for the future" | Collapse Hierarchy, Inline Class |
| **Dead Code** | Unreachable or unused code | Remove Dead Code |
| **Comments** | Comments explaining bad code | Refactor code to be self-documenting |

---

### Step 3: Choose the Refactoring

Select the appropriate transformation:

**Composing Methods:**
- Extract Method
- Inline Method
- Replace Temp with Query
- Introduce Explaining Variable

**Moving Features:**
- Move Method
- Move Field
- Extract Class
- Inline Class

**Organizing Data:**
- Replace Primitive with Object
- Replace Array with Object
- Introduce Parameter Object
- Replace Magic Number with Constant

**Simplifying Conditionals:**
- Decompose Conditional
- Consolidate Conditional Expression
- Replace Conditional with Polymorphism
- Replace Nested Conditional with Guard Clauses

**Simplifying Method Calls:**
- Rename Method
- Add Parameter / Remove Parameter
- Replace Parameter with Method Call
- Introduce Parameter Object

---

### Step 4: Apply in Small Steps

**The Golden Rule:** One small change at a time, test after each.

```
┌─────────────────────────────────────────┐
│         REFACTORING MICRO-CYCLE         │
├─────────────────────────────────────────┤
│ 1. Make ONE small change                │
│ 2. Run tests                            │
│ 3. If GREEN → commit (optional)         │
│ 4. If RED → revert immediately          │
│ 5. Repeat until refactoring complete    │
└─────────────────────────────────────────┘
```

**Never:**
- Make multiple changes before testing
- Refactor and add features simultaneously
- Continue if tests fail

---

### Step 5: Verify and Commit

After refactoring is complete:

- [ ] All tests pass
- [ ] Code is cleaner/simpler
- [ ] No behavior has changed
- [ ] Commit with clear message describing the refactoring

**Commit message format:**
```
refactor: [what was improved]

- Applied [refactoring pattern]
- [Brief description of change]
- No behavior changes
```

---

## Quality Checklist

Before considering refactoring complete:

### Safety
- [ ] Tests existed before refactoring began
- [ ] All tests pass after refactoring
- [ ] No new behavior was added
- [ ] No behavior was removed

### Process
- [ ] Small, incremental steps taken
- [ ] Tests run after each step
- [ ] Each step could be committed independently
- [ ] Refactoring is separate from feature work

### Improvement
- [ ] Code is simpler (lower complexity)
- [ ] Code is more readable
- [ ] Duplication is reduced
- [ ] Names are clearer

---

## Skill Interactions

### Preceded By
- **08-Code Review** - Often identifies refactoring needs
- **06-Atomic TDD** - Ensures tests exist for refactoring

### Followed By
- **06-Atomic TDD** - Feature work after refactoring
- **08-Code Review** - Verify refactoring quality

### Related Skills
- **13-Technical-Debt** - Prioritizes what to refactor
- **07-Vertical Slice Dev** - May trigger refactoring to enable slicing

> 📎 Examples: See 09-refactoring-examples.md
