> Examples for: skill-08-code-review  
> Parent skill: 08-code-review.md  
> These are optional pedagogical supplements — not in governance scope.

---

## Good Examples

### Example 1: Constitutional Feedback

**Code Under Review:**
```java
public class PalApplicationController {
    @PostMapping("/orders")
    public ResponseEntity<Order> createApplication(@RequestBody OrderDTO dto) {
        // Validation in controller
        if (dto.getItems() == null || dto.getItems().isEmpty()) {
            return ResponseEntity.badRequest().build();
        }

        // Business logic in controller
        double total = 0;
        for (ItemDTO item : dto.getItems()) {
            total += item.getPrice() * item.getQuantity();
            if (total > 10000) {
                // Apply bulk discount
                total = total * 0.9;
            }
        }

        PalApplication application = new Order();
        order.setTotal(total);
        order.setStatus("PENDING");
        orderRepository.save(order);

        return ResponseEntity.ok(order);
    }
}
```

**Good Review Feedback:**

```markdown
## Review: PalApplicationController.createApplication()

### 🔴 Blocker: Business Logic in Controller
**Location:** PalApplicationController.java:8-20
**Reference:** Engineering Constitution Article II, Section 2.3

The order total calculation and bulk discount logic belongs in the domain layer, not the controller. Controllers should only handle HTTP concerns.

**Impact:** This makes the business rule untestable in isolation and violates layer separation.

**Suggestion:** Move this logic to `Order.addItem()` and let the domain model calculate totals and apply discounts.

---

### 🔴 Blocker: Missing Domain Model Behavior
**Location:** PalApplicationController.java:22-24
**Reference:** Engineering Constitution Article II, Section 2.1

`Order` appears to be an anemic model (just setters). The order should know how to calculate its own total and manage its status transitions.

**Suggestion:**
```java
PalApplication application = PalApplication.create(customerId);
for (ItemDTO item : dto.getItems()) {
    application.addItem(item.toProduct(), Quantity.of(item.getQuantity()));
}
// Total calculated internally, discount applied by domain rule
```

---

### 🟡 Concern: No Test Coverage
**Reference:** Engineering Constitution Article IV, Section 4.1

I don't see tests for the bulk discount rule. What test verifies that orders over $10,000 get 10% off?

---

### 🟢 Suggestion: Use Value Objects
**Location:** PalApplicationController.java:12
**Reference:** Engineering Constitution Article II, Section 2.1

Consider using `Money` value object instead of `double` for currency calculations to avoid floating-point precision issues.
```

### Example 2: Security-Focused Review

**Code Under Review:**
```java
public User findUser(String username) {
    String query = "SELECT * FROM users WHERE username = '" + username + "'";
    return jdbcTemplate.queryForObject(query, userMapper);
}
```

**Good Review Feedback:**

```markdown
### 🔴 Blocker: SQL Injection Vulnerability
**Location:** UserRepository.java:15
**Reference:** Business Constitution Article VII, Section 7.1

String concatenation in SQL queries allows SQL injection attacks. An attacker could input `' OR '1'='1` to bypass authentication.

**Impact:** Critical security vulnerability - could expose all user data or allow unauthorized access.

**Required Fix:**
```java
public User findUser(String username) {
    String query = "SELECT * FROM users WHERE username = ?";
    return jdbcTemplate.queryForObject(query, userMapper, username);
}
```

This uses parameterized queries which properly escape input.
```

---

## Bad Examples (Anti-Patterns)

### Anti-Pattern 1: Style Nitpicking

```markdown
# BAD - Focusing on style over substance

- Line 5: Add a blank line here
- Line 12: I prefer camelCase for this variable
- Line 18: This brace should be on the next line
- Line 24: Import statements should be alphabetized
- Line 30: I would have named this function differently
```

**Why it's wrong:**
- Style is subjective and distracting
- Doesn't catch real bugs
- Demoralizes author
- Should be automated (linters/formatters)

### Anti-Pattern 2: Vague Feedback

```markdown
# BAD - Non-actionable feedback

- This code is confusing
- Make this better
- I don't like this approach
- This needs refactoring
- Not sure about this
```

**Why it's wrong:**
- No specific location
- No explanation of why
- No suggestion for improvement
- No constitutional reference
- Doesn't help author improve

### Anti-Pattern 3: Review Without Understanding

```markdown
# BAD - Reviewing without context

I didn't read the ticket but:
- Why is this class here?
- What does this feature do?
- I assume this should work differently
```

**Why it's wrong:**
- Reviews without understanding requirements
- May suggest wrong direction
- Wastes author's time explaining basics
- Misses actual issues

---

## Artifacts & Templates

### Template: Code Review Checklist

```markdown
# Code Review: [PR Title]

## Context
- **PR:** [Link]
- **Author:** [Name]
- **Reviewer:** [Name]
- **Related:** [Issue/Spec link]

## Traceability
- [ ] Linked to issue/story
- [ ] Scope matches requirements
- [ ] No scope creep

## Test Coverage
- [ ] New behavior has tests
- [ ] Tests verify behavior, not implementation
- [ ] Edge cases covered
- [ ] Tests are independent
- [ ] All tests pass

## Constitutional Compliance

### Engineering Constitution
- [ ] Art III.3.1: Code is readable and maintainable
- [ ] Art III.3.2: Complexity is justified
- [ ] Art III.3.3: SOLID principles followed
- [ ] Art III.3.4: Law of Demeter respected
- [ ] Art II.2.1: Domain model is behavior-rich
- [ ] Art IV.4.1: Tests exist for all behavior

### Business Constitution
- [ ] Art II.2.1: Business rules correctly implemented
- [ ] Art VII.7.1: No security vulnerabilities

### Product Constitution
- [ ] Art V.5.1: Changes are traceable

## Security
- [ ] No injection vulnerabilities
- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] Access control appropriate

## Feedback Summary

### Blockers (Must Fix)
1. [Location]: [Issue] - [Reference]

### Concerns (Should Discuss)
1. [Location]: [Issue] - [Reference]

### Suggestions (Optional)
1. [Location]: [Suggestion]

## Decision
- [ ] Approved
- [ ] Approved with suggestions
- [ ] Request changes
```

### Template: Review Feedback

```markdown
### [🔴|🟡|🟢|💡] [Category]: [Brief Title]

**Location:** [File:Line]
**Reference:** [Constitution Article/Section]

[Description of the issue or observation]

**Impact:** [Why this matters]

**Suggestion:**
[How to improve, with code example if helpful]
```

---



---

## Feedback Phrase Examples

Sample feedback phrases for common review scenarios:

**Example 1:**
> "I see new functionality in `PalApplicationService.applyDiscount()` but no corresponding tests. Per Engineering Constitution Article IV, Section 4.1, all behavior needs test coverage. What test would verify this discount calculation?"

**Example 2:**
> "The discount calculation in line 47 allows discounts greater than the order total. Per BR-023, discounts cannot exceed the subtotal. The domain model should enforce this invariant."

**Example 3:**
> "Line 34 constructs a SQL query with string concatenation. Per Business Constitution Article VII, Section 7.1, this creates SQL injection risk. Please use parameterized queries."
