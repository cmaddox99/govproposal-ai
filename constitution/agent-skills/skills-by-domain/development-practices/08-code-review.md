---
skill:
  id: skill-08-code-review
  name: Code Review
  category: quality
  version: "2.0.0"

laws:
  implements:
    - id: ENG-3.1
      title: Complexity Limits
    - id: ENG-3.2
      title: Immutability Law
    - id: ENG-3.3
      title: Law of Demeter
    - id: ENG-3.4
      title: Single Responsibility Principle
    - id: ENG-6.5
      title: Input Validation Law
  references:
    - id: ENG-4.1
      title: Atomic TDD Law
    - id: ENG-6.1
      title: Security by Design Law

triggers:
  phrases:
    - "Review this code"
    - "Check for compliance"
    - "PR review"
    - "Is this code ready?"

followed_by:
  - skill-09-refactoring
  - skill-27-constitution-compliance
---

# Skill: Code Review

> **Purpose:** Ensure code quality and constitutional compliance through systematic review.

---

## Purpose

Code Review is the practice of systematically examining code changes to ensure they meet quality standards and constitutional requirements. This skill:

1. **Prevents defects** - Catches issues before they reach production
2. **Ensures compliance** - Verifies adherence to constitutional laws
3. **Shares knowledge** - Spreads understanding across the team
4. **Improves design** - Identifies opportunities for better solutions

Reviews focus on **behavior correctness**, **constitutional compliance**, and **maintainability** - not style preferences.

---

## When to Invoke

Invoke this skill when:

- Reviewing pull requests or merge requests
- Conducting code inspections
- Evaluating refactoring proposals
- Assessing code from an AI agent
- Self-reviewing before committing

**Trigger phrases:**
- "Review this code"
- "Check this implementation"
- "Is this code quality acceptable?"
- "What feedback do you have on this PR?"

---

## Constitutional Foundation

### Engineering Constitution
- **Article III, Section 3.1** - Code Quality: "Code is readable, maintainable, and correct"
- **Article III, Section 3.2** - Complexity Management: "Complexity is justified and contained"
- **Article III, Section 3.3** - SOLID Principles: "Design follows established principles"
- **Article III, Section 3.4** - Law of Demeter: "Objects talk only to friends"
- **Article IV, Section 4.2** - Test Quality: "Tests are comprehensive and meaningful"

### Product Constitution
- **Article V, Section 5.1** - Traceability: "Changes connect to requirements"

### Business Constitution
- **Article II, Section 2.1** - Business Rules: "Rules are correctly implemented"
- **Article VII, Section 7.1** - Security: "Security vulnerabilities are prevented"

---

## Method

### Step 1: Understand the Context

Before reviewing code, understand what it's meant to do:

**Questions to Answer:**
- What feature/fix does this implement?
- What are the acceptance criteria?
- What's the scope of the change?
- Are there related specifications or designs?

**Find context in:**
- Pull request description
- Linked issues/tickets
- Hangar SDD proposals
- Executable specifications

### Step 2: Verify Traceability

Confirm the change connects to tracked work:

**Checklist:**
- [ ] PR links to issue/story
- [ ] Changes align with acceptance criteria
- [ ] Scope matches what was planned
- [ ] No unrelated changes mixed in

**If traceability is missing:**
> "Per Product Constitution Article V, Section 5.1, all changes must be traceable to requirements. Could you link this PR to the relevant Hangar SDD proposal or user story?"

### Step 3: Review Test Coverage

Verify tests exist and are meaningful:

**Test Quality Checklist:**
- [ ] New behavior has tests
- [ ] Tests follow Arrange-Act-Assert
- [ ] Tests verify behavior, not implementation
- [ ] Edge cases are covered
- [ ] Tests are independent
- [ ] Test names describe expected behavior

**Red Flags:**
- No new tests for new behavior
- Tests that test implementation details
- Tests with multiple assertions testing different behaviors
- Tests that depend on other tests

### Step 4: Check Constitutional Compliance

Review against specific constitutional articles:

#### 4a. Code Quality (Article III)

| Check | Question |
|-------|----------|
| Readability | Can another developer understand this quickly? |
| Naming | Do names reveal intent? |
| Functions | Are they small and focused? |
| Comments | Are they explaining WHY, not WHAT? |

#### 4b. Complexity (Article III, Section 3.2)

| Metric | Threshold | Check |
|--------|-----------|-------|
| Method length | < 20 lines | Long methods? |
| Cyclomatic complexity | < 10 | Deep nesting? |
| Parameters | < 4 | Too many params? |
| Dependencies | Minimal | Excessive coupling? |

#### 4c. SOLID Principles (Article III, Section 3.3)

| Principle | Violation Signs |
|-----------|-----------------|
| Single Responsibility | Class doing multiple things |
| Open/Closed | Modifying existing code for new features |
| Liskov Substitution | Subtypes changing parent behavior |
| Interface Segregation | Clients depending on unused methods |
| Dependency Inversion | High-level depending on low-level |

#### 4d. Law of Demeter (Article III, Section 3.4)

Avoid method chaining through objects (e.g. `a.getB().getC()`) — use delegation instead.

### Step 5: Verify Business Rules

Confirm business rules are correctly implemented:

**Checklist:**
- [ ] Business rules match documented specifications
- [ ] Rules enforced in domain layer (not scattered)
- [ ] Invariants protected
- [ ] Edge cases handled per rules

### Step 6: Security Review

Check for security vulnerabilities:

**OWASP Top 10 Checklist:**
- [ ] Injection (SQL, Command, XSS)
- [ ] Authentication/Session management
- [ ] Sensitive data exposure
- [ ] Access control
- [ ] Security misconfiguration
- [ ] Input validation

**Red Flags:**
- String concatenation in queries
- Hardcoded credentials
- Missing input validation
- Overly permissive access
- Logging sensitive data

### Step 7: Provide Feedback

Give specific, actionable, constitutional feedback:

**Feedback Structure:**
1. **Location** - Specific file and line
2. **Observation** - What you notice
3. **Constitutional Reference** - Which article applies
4. **Impact** - Why it matters
5. **Suggestion** - How to improve

**Feedback Types:**

| Type | Meaning | Action Required |
|------|---------|-----------------|
| 🔴 **Blocker** | Must fix before merge | Yes |
| 🟡 **Concern** | Should fix, discuss if not | Discuss |
| 🟢 **Suggestion** | Nice to have | Optional |
| 💡 **Question** | Need clarification | Respond |

### Step 8: Verify Resolution

Before approving:

- [ ] All blockers addressed
- [ ] Concerns discussed and resolved
- [ ] Tests pass
- [ ] No new issues introduced

---

## Quality Checklist

For a complete code review:

- [ ] **Context Understood:** Read ticket/spec before reviewing
- [ ] **Traceability Verified:** Changes link to requirements
- [ ] **Tests Reviewed:** Coverage and quality checked
- [ ] **Constitution Checked:** Compliance with relevant articles
- [ ] **Security Examined:** OWASP concerns addressed
- [ ] **Feedback Specific:** All feedback has location and rationale
- [ ] **Feedback Actionable:** Suggestions provided, not just criticism
- [ ] **Feedback Constitutional:** References to articles included
- [ ] **Tone Constructive:** Teaching approach, not gatekeeping

---

## Skill Interactions

### Preceded By
- **06-Atomic TDD** - Code being reviewed was developed test-first
- **07-Vertical Slice Dev** - Understanding the slice being reviewed

### Followed By
- Code merge and deployment
- Knowledge sharing with team

### Related Skills
- **03-Executable Spec** - Verify implementation matches specs
- **04-Business Domain Modeling** - Review domain model quality
- **05-Business Rules** - Verify rules are correctly implemented

> 📎 Examples: See 08-code-review-examples.md
