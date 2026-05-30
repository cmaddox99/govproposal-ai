---
skill:
  id: skill-14-technical-debt
  name: Technical Debt Management
  category: quality
  version: "2.0.0"

laws:
  implements:
    - id: ENG-1.3
      title: Continuous Refactoring Law
  references:
    - id: ENG-3.1
      title: Complexity Limits

triggers:
  phrases:
    - "Track technical debt"
    - "Debt inventory"
    - "Pay down debt"
    - "Code quality declining"

followed_by:
  - skill-09-refactoring
  - skill-01-roadmapping
---

# Skill: Technical Debt Management

> **Purpose:** Systematically identify, catalog, prioritize, and pay down technical debt to maintain sustainable development velocity.
> **Workflow:** See `workflows/legacy-rescue-decision-track.md` for the full per-bounded-context refactor/rewrite decision sequence.

---

## Purpose

Technical Debt Management is the practice of treating code and architecture shortcuts as financial debt that accrues interest. This skill ensures:

1. **Visibility** - Debt is identified and tracked, not hidden
2. **Prioritization** - Highest-impact debt addressed first
3. **Balance** - Features and debt repayment in healthy proportion
4. **Prevention** - New debt is conscious and documented
5. **Sustainability** - Codebase remains maintainable long-term

**Key principle:** All debt is not equal. Some debt enables speed; some debt cripples it. Know the difference.

---

## When to Invoke

Invoke this skill when:

- Code review identifies shortcuts or "TODO" items
- Velocity is slowing despite consistent effort
- Bugs cluster in certain areas of the codebase
- Onboarding new team members takes longer
- Refactoring feels impossible due to entanglement
- Planning technical debt sprints

**Trigger phrases:**
- "We'll fix this later"
- "This is a temporary solution"
- "Why does this take so long?"
- "Don't touch that code"
- "Let's do a debt sprint"

---

## Constitutional Foundation

### Engineering Constitution
- **Article III, Section 3.1** - Simplicity: Complexity is debt
- **Article II, Section 2.1** - Code Quality: Maintainability required
- **Article IV, Section 4.1** - Test-First: Missing tests are debt

### Product Constitution
- **Article IV, Section 4.1** - Velocity: Debt slows delivery

### Business Constitution
- **Article IV, Section 4.1** - Sustainability: Long-term viability
- **Article III, Section 3.3** - Audit: Debt is documented

---

## Method: Debt Management Lifecycle

### Step 1: Identify Debt

**Sources of Debt Discovery:**

```markdown
## Debt Discovery Sources

### Code Analysis
- Static analysis warnings
- Complexity metrics (cyclomatic > 10)
- Duplication reports
- Code coverage gaps

### Team Signals
- "Scary" code areas
- Frequently broken tests
- Long code review cycles
- Slow feature delivery

### Incident Analysis
- Root causes from postmortems
- Bug clustering patterns
- Performance bottlenecks

### Architecture Review
- Coupling analysis
- Dependency graphs
- Service boundaries
```

**Code Smell Indicators:**

```python
# Debt indicators in code

# TODO/FIXME/HACK comments
# TODO: This should be refactored (created 2 years ago)
# HACK: Temporary workaround for payment bug
# FIXME: Race condition here

# Suppressed warnings
# pylint: disable=all
# @SuppressWarnings("unchecked")
# // eslint-disable-next-line

# Magic numbers and strings
if status == 47:  # What is 47?
    timeout = 86400  # Why this number?

# Duplicated logic
# Same 50 lines in 4 different files
```

---

### Step 2: Catalog Debt

**Debt Registry Template:**

```markdown
# Technical Debt Registry

## PR Checklist - Debt Section

### New Debt Introduced?
- [ ] No new debt
- [ ] Yes - DEBT ticket created: DEBT-XXX
- [ ] Yes - Approved by tech lead

### Existing Debt Addressed?
- [ ] No opportunity in this PR
- [ ] Yes - DEBT-XXX partially addressed
- [ ] Yes - DEBT-XXX fully resolved

### Boy Scout Rule
- [ ] Code left cleaner than found
- [ ] Or: No changes to surrounding code
```

---

## Quality Checklist

Before considering debt management mature:

### Process
- [ ] Debt registry exists and is maintained
- [ ] Debt discussed in sprint planning
- [ ] Budget allocated (e.g., 20% rule)
- [ ] Definition of Done includes debt awareness

### Visibility
- [ ] Dashboard shows debt metrics
- [ ] Team knows top debt items
- [ ] Stakeholders understand trade-offs

### Prevention
- [ ] Code review checks for new debt
- [ ] Approved shortcuts are documented
- [ ] TODOs linked to tickets

### Measurement
- [ ] Debt trend tracked over time
- [ ] Interest (cost) quantified
- [ ] ROI of repayment measured

---

## Skill Interactions

### Preceded By
- **08-Code Review** - Identifies debt in reviews
- **11-Incident Response** - Postmortems reveal debt

### Followed By
- **09-Refactoring** - Debt repayment via refactoring

### Related Skills
- **13-Observability** - Missing observability is debt
- **10-Security Review** - Security gaps are debt

> 📎 Examples: See 14-technical-debt-examples.md