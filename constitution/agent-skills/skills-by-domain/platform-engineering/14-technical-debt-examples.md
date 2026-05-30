> Examples for: skill-14-technical-debt  
> Parent skill: 14-technical-debt.md  
> These are optional pedagogical supplements — not in governance scope.

---

## Types of Technical Debt

### Debt Quadrant

```
                    Reckless                    Prudent
              ┌─────────────────────┬─────────────────────┐
              │                     │                     │
              │  "We don't have     │  "We must ship now  │
   Deliberate │   time for tests"   │   and deal with     │
              │                     │   consequences"     │
              │  HIGH INTEREST      │  MANAGED RISK       │
              │                     │                     │
              ├─────────────────────┼─────────────────────┤
              │                     │                     │
              │  "What's a design   │  "Now we know how   │
 Inadvertent  │   pattern?"         │   we should have    │
              │                     │   done it"          │
              │  REQUIRES LEARNING  │  NATURAL EVOLUTION  │
              │                     │                     │
              └─────────────────────┴─────────────────────┘
```

### Debt Categories

| Category | Examples | Interest Rate |
|----------|----------|---------------|
| **Code Debt** | Duplication, complex methods, poor naming | Medium |
| **Architecture Debt** | Monolith, tight coupling, wrong patterns | High |
| **Test Debt** | Missing tests, flaky tests, slow tests | High |
| **Documentation Debt** | Missing docs, outdated docs | Low |
| **Dependency Debt** | Outdated libraries, security vulnerabilities | Variable |
| **Infrastructure Debt** | Manual deployments, missing monitoring | Medium |

---

## Good Examples

### Example 1: Well-Managed Debt Backlog

```markdown
# Technical Debt Dashboard

## Summary
- Total Items: 23
- High Priority: 4
- In Progress: 2
- Resolved This Quarter: 8

## High Priority Queue

| ID | Title | Impact | Effort | Age |
|----|-------|--------|--------|-----|
| DEBT-001 | Payment monolith | High | 4 weeks | 8mo |
| DEBT-007 | Missing API tests | High | 1 week | 3mo |
| DEBT-012 | N+1 queries in order list | High | 2 days | 2mo |
| DEBT-015 | Deprecated auth library | High | 1 week | 1mo |

## Recent Wins
- DEBT-003: Extracted UserValidator ✓
- DEBT-009: Added integration tests ✓
- DEBT-011: Removed dead code ✓

## Debt Budget Tracking
- Q1 Target: 20% of capacity
- Q1 Actual: 18% of capacity
- Trend: On track
```

---

### Example 2: Feature + Debt Planning

```markdown
# Feature: Add Cryptocurrency Payments

## Debt Analysis

### Blocking Debt
DEBT-001 (Payment Monolith) blocks clean implementation.
Must extract payment processor interface first.

### Plan
1. Sprint 1: Extract PaymentProcessor interface (DEBT-001 partial)
2. Sprint 2: Implement CryptoPaymentProcessor
3. Sprint 3: Add wallet integration

### Debt Paydown Benefits
- DEBT-001 partially resolved
- Future payment methods easier
- Testing improved
```

---

## Bad Examples (Anti-Patterns)

### Anti-Pattern 1: Hidden Debt

```python
# BAD - Debt without tracking

def calculate_tax(order):
    # This is wrong for international orders but whatever
    return order.total * 0.08

# No ticket, no tracking, forgotten until bug report
```

**Correct approach:** Create DEBT ticket, add TODO with reference.

---

### Anti-Pattern 2: Debt Bankruptcy

```markdown
# BAD - Ignoring debt until crisis

Year 1: "We'll fix it later"
Year 2: "We're too busy with features"
Year 3: "We need to rewrite everything"

# Result: 6-month rewrite project, team burnout
```

**Correct approach:** Continuous 20% investment prevents bankruptcy.

---

### Anti-Pattern 3: Gold Plating Debt

```markdown
# BAD - Over-engineering debt repayment

DEBT-012: Add missing tests for OrderService

Proposed solution:
- Build custom testing framework
- Add property-based testing
- Implement mutation testing
- Create visual test reports

# 2-day task becomes 2-month project
```

**Correct approach:** Minimal viable repayment. Fix the debt, nothing more.

---

## Artifacts & Templates

### Template: Debt Item

```markdown
# DEBT-XXX: [Title]

## Metadata
- **Category:** [Code/Architecture/Test/Docs/Dependency/Infrastructure]
- **Location:** [file/folder path]
- **Identified:** [date]
- **Reporter:** [@username]

## Description
[What is the debt? Be specific.]

## Impact
- **Velocity:** [How it slows development]
- **Quality:** [Bug/incident risk]
- **Team:** [Onboarding, morale impact]

## Interest (Ongoing Cost)
[Quantify the ongoing cost: time, incidents, workarounds]

## Remediation
[How to fix it - high level approach]

## Estimate
- **Effort:** [days/weeks]
- **Complexity:** [Low/Medium/High]
- **Risk:** [Low/Medium/High]

## Priority
[High/Medium/Low] - [Justification]

## Status
[Proposed/Approved/In Progress/Done]
```

### Template: Quarterly Debt Review

```markdown
# Q[N] Technical Debt Review

## Executive Summary
[High-level status of debt health]

## Metrics
- Debt items: [total] ([+/- vs last quarter])
- High priority: [count]
- Resolved: [count]
- Debt budget adherence: [%]

## Top Risks
1. [Highest risk debt item]
2. [Second highest]
3. [Third highest]

## Recommendations
1. [Priority focus for next quarter]
2. [Resource allocation]
3. [Process improvements]

## Appendix
[Full debt registry snapshot]
```

---

---

## Worked Examples: Technical Debt Registry

## DEBT-001: Payment Service Monolith

**Category:** Architecture
**Location:** /services/payment/
**Identified:** 2024-01-15
**Reporter:** @engineer

### Description
Payment service has grown to 15,000 lines with 12 responsibilities.
Adding new payment methods requires modifying 8+ files.

### Impact
- New payment method takes 2 weeks instead of 2 days
- High bug rate in payment code (3x average)
- 4 incidents in last quarter traced here

### Interest (ongoing cost)
- 3 engineer-days per sprint in workarounds
- 1 incident per month average
- Onboarding takes 2 extra weeks

### Remediation
Extract into microservices:
1. Payment Processing Service
2. Payment Method Registry
3. Payment Analytics Service

**Estimated Effort:** 4 weeks (2 engineers)
**Priority:** High
**Status:** Proposed
```

**Debt Tracking Fields:**

| Field | Purpose |
|-------|---------|
| ID | Unique identifier |
| Category | Type of debt |
| Location | Where in codebase |
| Description | What the debt is |
| Impact | How it affects the team |
| Interest | Ongoing cost if not fixed |
| Remediation | How to fix it |
| Effort | Estimated fix time |
| Priority | High/Medium/Low |
| Status | Proposed/Approved/In Progress/Done |

---

### Step 3: Prioritize Debt

**Prioritization Matrix:**

```
                    Low Effort              High Effort
              ┌─────────────────────┬─────────────────────┐
              │                     │                     │
              │     QUICK WINS      │    MAJOR PROJECT    │
  High Impact │                     │                     │
              │   Do immediately    │   Plan and schedule │
              │                     │                     │
              ├─────────────────────┼─────────────────────┤
              │                     │                     │
              │     FILL-INS        │      AVOID          │
   Low Impact │                     │                     │
              │  Do when convenient │  Don't prioritize   │
              │                     │                     │
              └─────────────────────┴─────────────────────┘
```

**Scoring Model:**

```python
def calculate_debt_priority(debt_item):
    # Impact score (1-5)
    velocity_impact = rate_velocity_impact(debt_item)  # How much it slows us
    bug_frequency = rate_bug_frequency(debt_item)      # Bugs from this area
    incident_risk = rate_incident_risk(debt_item)      # Production risk

    impact_score = (velocity_impact + bug_frequency + incident_risk) / 3

    # Effort score (1-5, inverted - lower effort = higher priority)
    effort_score = 6 - rate_effort(debt_item)

    # Compound interest factor
    age_months = get_age_months(debt_item)
    interest_multiplier = 1 + (age_months * 0.1)  # 10% increase per month

    return (impact_score * effort_score * interest_multiplier)
```

---

### Step 4: Plan Repayment

**Debt Budget Strategies:**

| Strategy | Description | When to Use |
|----------|-------------|-------------|
| **20% Rule** | 20% of each sprint for debt | Sustainable long-term |
| **Debt Sprint** | Full sprint on debt only | Debt is critical |
| **Boy Scout** | Leave code cleaner than found | Continuous improvement |
| **Alongside Features** | Bundle with related features | Natural opportunities |

**Sprint Planning with Debt:**

```markdown
## Sprint 24 Planning

### Capacity: 40 points

### Feature Work (80% = 32 points)
- USER-123: Add payment method (8 pts)
- USER-124: Order history page (13 pts)
- USER-125: Email notifications (8 pts)

### Debt Work (20% = 8 points)
- DEBT-001: Extract PaymentValidator (5 pts)
- DEBT-012: Add missing order tests (3 pts)

### Debt Selected Because:
- DEBT-001 blocks USER-123 (natural opportunity)
- DEBT-012 is quick win in same area
```

---

### Step 5: Execute Repayment

**Debt Repayment Principles:**

1. **Tests First** - Don't repay debt without test coverage
2. **Small Steps** - Break large debt into smaller pieces
3. **Verify Behavior** - Ensure nothing breaks
4. **Document Changes** - Update docs and registry

**Repayment Workflow:**

```markdown
## Repaying DEBT-001: Extract PaymentValidator

### Prerequisites
- [ ] Characterization tests for existing behavior
- [ ] Team aware of changes

### Execution
- [ ] Create new PaymentValidator class
- [ ] Move validation methods one at a time
- [ ] Update callers to use new class
- [ ] Run full test suite after each move
- [ ] Remove old code when empty

### Verification
- [ ] All tests pass
- [ ] No behavior changes
- [ ] Performance not degraded
- [ ] Team review complete

### Closeout
- [ ] Update DEBT-001 status to Done
- [ ] Update architecture docs
- [ ] Share in team retro
```

---

### Step 6: Prevent New Debt

**Debt Prevention Practices:**

```markdown
## Definition of Done - Debt Aware

### Code Quality
- [ ] No new static analysis warnings
- [ ] Cyclomatic complexity < 10
- [ ] No duplication introduced
- [ ] Tests cover new code (>90%)

### Debt Documentation
- [ ] If shortcut taken, DEBT ticket created
- [ ] Shortcut has TODO with ticket reference
- [ ] Debt reviewed and approved

### Example
```python
# Approved shortcut - see DEBT-045
# TODO(DEBT-045): Replace with proper caching layer
@lru_cache(maxsize=1000)
def get_user(user_id):
    return db.query(User).get(user_id)
```
```

**Tech Debt Review in PR:**

```markdown
