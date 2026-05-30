---
skill:
  id: skill-05-business-rules
  name: Business Rules
  category: modeling
  version: "2.0.0"

laws:
  implements:
    - id: ENG-2.1
      title: Domain-Driven Design Law
    - id: BUS-2.2
      title: Control Framework Law
  references:
    - id: BUS-2.1
      title: FAA Compliance Law
    - id: BUS-2.2
      title: TSA Security Compliance Law
    - id: BUS-7.1
      title: Audit Trail Law

triggers:
  phrases:
    - "Document business rules"
    - "What are the constraints?"
    - "Compliance requirements"
    - "What rules apply?"

followed_by:
  - skill-06-atomic-tdd
  - skill-10-security-review
---

# Skill: Business Rules Documentation

> **Purpose:** Capture, categorize, and document business rules that the system must enforce.

---

## Purpose

Business Rules documentation makes implicit business logic explicit. This skill ensures:

1. **Visibility** - Everyone knows what rules exist
2. **Testability** - Rules can be verified automatically
3. **Consistency** - Rules are enforced uniformly
4. **Maintainability** - Changes to rules are tracked

Business rules are the constraints, calculations, and policies that define how the business operates.

---

## When to Invoke

Invoke this skill when:

- Discovering business logic during domain modeling
- Clarifying what the system should and shouldn't allow
- Finding implicit rules buried in legacy code
- Preparing for compliance audits
- Onboarding new team members to domain knowledge

**Trigger phrases:**
- "What are the business rules for X?"
- "When should the system allow/prevent Y?"
- "What calculations apply to Z?"
- "Document the rules around..."

---

## Constitutional Foundation

### Business Constitution
- **Article II, Section 2.1** - Business Rules: "Rules are explicit, documented, and testable"
- **Article II, Section 2.2** - Rule Authority: "Business owns rule definitions"
- **Article II, Section 2.3** - Rule Verification: "Rules are verified continuously"

### Engineering Constitution
- **Article II, Section 2.4** - Domain Modeling: "Business rules live in domain layer"
- **Article IV, Section 4.2** - Test Coverage: "All business rules have tests"

### Product Constitution
- **Article III, Section 3.3** - Clarity: "Users understand what's allowed"

---

## Method

### Step 1: Discover Rules

Find business rules from multiple sources:

**Sources:**
| Source | Examples |
|--------|----------|
| Domain Experts | Verbal explanations, tribal knowledge |
| Existing Code | Conditionals, validations, calculations |
| Documents | Policy manuals, contracts, regulations |
| Support Tickets | "The system should have..." complaints |
| Edge Cases | "What happens when..." questions |

**Discovery Questions:**
- What must always be true?
- What can never happen?
- What conditions change the outcome?
- What calculations determine values?
- Who is allowed to do what?

### Step 2: Categorize Rules

Classify each rule by type:

| Category | Description | Examples |
|----------|-------------|----------|
| **Constraint** | What must/must not happen | "Order must have at least one item" |
| **Calculation** | How values are computed | "Total = sum of line items × (1 + tax rate)" |
| **Derivation** | How values are derived | "Customer tier based on annual spending" |
| **Inference** | What can be concluded | "If all items shipped, order is complete" |
| **Authorization** | Who can do what | "Only managers can approve refunds > $500" |
| **Timing** | When things happen | "Invoice generated 24h after delivery" |
| **Validation** | Input requirements | "Email must be valid format" |

### Step 3: Document Each Rule

Use consistent format for every rule:

```markdown
## Rule: [BR-XXX] [Rule Name]

**Category:** [Constraint|Calculation|etc.]
**Domain:** [Bounded Context / Aggregate]
**Priority:** [Critical|High|Medium|Low]

**Statement:**
[Clear, unambiguous statement of the rule]

**Rationale:**
[Why this rule exists - business reason]

**Source:**
[Where this rule comes from - regulation, policy, domain expert]

**Examples:**
- When [condition], then [outcome]
- When [condition], then [outcome]

**Exceptions:**
[Any exceptions or overrides]

**Related Rules:**
[Other rules that interact with this one]
```

### Step 4: Validate with Domain Experts

Confirm each rule:

**Validation Questions:**
- Is this statement accurate?
- Are there any exceptions?
- When did this rule take effect?
- Who can override this rule?
- What happens if the rule is violated?

### Step 5: Map to Implementation

Connect rules to code:

| Rule | Implementation Location | Test Coverage |
|------|------------------------|---------------|
| [BR-001] | `Order.addItem()` | `OrderTest.testMinimumOneItem()` |
| [BR-002] | `PricingService.calculate()` | `PricingTest.testTaxCalculation()` |

### Step 6: Establish Governance

Create process for rule changes:

- Who can propose rule changes?
- Who approves changes?
- How are changes communicated?
- How are changes tested before deployment?

---

## Good Examples

### Example 1: E-commerce Business Rules

**Domain:** PAL Application Processing

```markdown
## Rule: [BR-001] Minimum Order Value

**Category:** Constraint
**Domain:** Orders
**Priority:** High

**Statement:**
Orders must have a minimum value of $10.00 before shipping costs to be placed.

**Rationale:**
Orders below $10 are unprofitable due to fixed fulfillment costs.

**Source:**
Finance team policy, effective 2024-01-01

**Examples:**
- Order with $9.99 subtotal → Cannot be placed, error shown
- Order with $10.00 subtotal → Can be placed
- Order with $15.00 subtotal → Can be placed

**Exceptions:**
- Subscription orders exempt (customer retention)
- Promotional codes may waive minimum

**Related Rules:**
- [BR-002] Free shipping threshold
- [BR-005] Subscription discounts
```

```markdown
## Rule: [BR-002] Free Shipping Threshold

**Category:** Calculation
**Domain:** Orders / Shipping
**Priority:** High

**Statement:**
Orders with subtotal ≥ $50.00 qualify for free standard shipping.

**Rationale:**
Encourages larger orders, increases average order value.

**Source:**
Marketing policy, A/B tested 2023-Q3

**Calculation:**
```
IF order.subtotal >= $50.00
THEN shipping_cost = $0.00
ELSE shipping_cost = standard_shipping_rate
```

**Examples:**
- Order subtotal $49.99 → Standard shipping rate applies
- Order subtotal $50.00 → Free shipping
- Order subtotal $100.00 → Free shipping

**Exceptions:**
- Express/overnight shipping always charged
- Oversized items have surcharge regardless
- Hawaii/Alaska have different thresholds ($75)

**Related Rules:**
- [BR-001] Minimum order value
- [BR-010] Oversized item surcharge
```

```markdown
## Rule: [BR-003] Inventory Reservation

**Category:** Constraint
**Domain:** Inventory / Orders
**Priority:** Critical

**Statement:**
Inventory is reserved when item is added to cart and held for 30 minutes. Reservation released if not purchased.

**Rationale:**
Prevents overselling while allowing abandoned carts to free inventory.

**Source:**
Operations policy, after overselling incident 2023-06

**State Diagram:**
```
Available → Reserved (add to cart)
Reserved → Available (cart timeout or removal)
Reserved → Committed (order placed)
Committed → Shipped (fulfillment)
```

**Examples:**
- Add item to cart → Inventory reserved, available count decreases
- 30 min timeout → Reservation released, available count increases
- Place order → Reservation converted to commitment

**Exceptions:**
- VIP customers get 60-minute reservation
- Pre-vetting answers not reserved until ship date

**Related Rules:**
- [BR-004] Backorder handling
- [BR-012] VIP customer privileges
```

### Example 2: Authorization Rules

```markdown
## Rule: [BR-020] Refund Authorization Limits

**Category:** Authorization
**Domain:** Returns / Refunds
**Priority:** Critical

**Statement:**
Refund authorization requires approval based on amount:
- ≤ $100: Any support agent
- $101 - $500: Senior support or Team Lead
- $501 - $2000: Manager
- > $2000: Director + Finance review

**Rationale:**
Fraud prevention and financial controls. Higher amounts need more scrutiny.

**Source:**
Finance policy, SOX compliance requirement

**Authorization Matrix:**
| Amount | Role Required | Additional Requirements |
|--------|--------------|------------------------|
| ≤ $100 | Support Agent | None |
| $101-$500 | Senior Support | Reason documented |
| $501-$2000 | Manager | Reason + original order review |
| > $2000 | Director | Finance approval, audit trail |

**Examples:**
- $50 refund by Agent Jane → Approved automatically
- $300 refund by Agent Jane → Escalated to Team Lead
- $1500 refund by Team Lead → Escalated to Manager
- $3000 refund → Requires Director + Finance sign-off

**Exceptions:**
- Shipping damage claims follow separate process
- Subscription cancellation refunds use prorated calculation

**Audit Requirements:**
- All refunds logged with actor, timestamp, reason
- Refunds > $500 require documented justification
- Monthly review of refund patterns by Finance
```

---

## Bad Examples (Anti-Patterns)

### Anti-Pattern 1: Implicit Rules in Code

```java
// BAD - Rule hidden in implementation without documentation

public class PalApplicationService {
    public void placeOrder(PalApplication application) {
        // Magic numbers, no explanation
        if (application.getTotal().compareTo(new BigDecimal("10")) < 0) {
            throw new OrderException("Order too small");
        }

        // Why 30? Nobody knows.
        if (application.getItems().size() > 30) {
            throw new OrderException("Too many items");
        }

        // Unclear condition
        if (applicant.getStatus().equals("B")) {
            throw new OrderException("Cannot place order");
        }
    }
}
```

**Why it's wrong:**
- Rules not documented anywhere
- Magic numbers without explanation
- No business rationale captured
- Hard to test comprehensively
- No traceability to business requirements

**Correct approach:** Document rules explicitly, then implement with clear references.

### Anti-Pattern 2: Vague Rule Documentation

```markdown
# BAD - Vague and untestable

## Rule: Good Customer Service

Orders should be handled in a timely manner with good customer service.

## Rule: Fair Pricing

Prices should be fair and competitive.

## Rule: Secure Transactions

All transactions should be secure.
```

**Why it's wrong:**
- Not specific enough to implement
- "Timely," "fair," "secure" are subjective
- Cannot be tested automatically
- Different people will interpret differently

**Correct approach:** Make rules specific and measurable:
```markdown
## Rule: PAL Application Processing SLA

Orders placed before 2:00 PM local time ship same day.
Orders placed after 2:00 PM ship next business day.
```

### Anti-Pattern 3: Rules Without Traceability

```markdown
# BAD - No source, no governance

## Rule: 20% Discount for New Customers

New customers get 20% off their first order.
```

**Why it's wrong:**
- Who decided this?
- When does it expire?
- What defines "new customer"?
- Can it be changed? By whom?
- How do we know it's still valid?

**Correct approach:** Include complete metadata:
```markdown
## Rule: [BR-050] New Customer Discount

**Statement:** Customers placing their first order receive 20% discount on subtotal.

**Source:** Marketing campaign, approved by CMO 2024-03-01
**Effective:** 2024-03-15 to 2024-06-15
**Owner:** Marketing team

**Definition - New Customer:**
- No prior completed orders (cancelled doesn't count)
- Account created within last 90 days
```

---

## Artifacts & Templates

### Template: Business Rules Catalog

```markdown
# Business Rules Catalog: [Domain/System Name]

## Overview
This document catalogs all business rules for [domain].

**Last Updated:** [Date]
**Owner:** [Team/Person]
**Review Cadence:** [Quarterly/etc.]

---

## Rules by Category

### Constraints
| ID | Name | Priority | Domain |
|----|------|----------|--------|
| BR-001 | [Name] | Critical | [Domain] |

### Calculations
| ID | Name | Priority | Domain |
|----|------|----------|--------|
| BR-010 | [Name] | High | [Domain] |

### Authorization
| ID | Name | Priority | Domain |
|----|------|----------|--------|
| BR-020 | [Name] | Critical | [Domain] |

---

## Rule Details

[Individual rule documentation follows...]

---

## Change Log

| Date | Rule ID | Change | Author | Approved By |
|------|---------|--------|--------|-------------|
| [Date] | [ID] | [Description] | [Name] | [Name] |

---

## Governance

### Rule Change Process
1. Change requested via [process]
2. Impact assessment by [role]
3. Approval by [role]
4. Implementation and testing
5. Documentation update
6. Stakeholder communication

### Review Schedule
- [Frequency]: Full catalog review
- [Trigger]: Review after any rule change
- [Audit]: Annual compliance audit
```

### Template: Individual Rule

```markdown
## Rule: [BR-XXX] [Rule Name]

**Category:** [Constraint|Calculation|Authorization|Validation|Timing|Derivation|Inference]
**Domain:** [Bounded Context / Aggregate]
**Priority:** [Critical|High|Medium|Low]
**Status:** [Active|Deprecated|Pending]

### Statement
[Clear, unambiguous statement of the rule. Use precise language.]

### Rationale
[Why this rule exists. Business reason, not technical reason.]

### Source
[Where this rule comes from]
- **Origin:** [Regulation|Policy|Domain Expert|etc.]
- **Reference:** [Document name, section, date]
- **Effective Date:** [When rule took effect]
- **Expiration:** [If applicable]

### Specification

#### Conditions
```
IF [condition]
AND [condition]
THEN [outcome]
ELSE [alternative outcome]
```

#### Examples
| Scenario | Input | Expected Result |
|----------|-------|-----------------|
| [Scenario 1] | [Input] | [Result] |
| [Scenario 2] | [Input] | [Result] |

### Exceptions
[List any exceptions or override conditions]
- [Exception 1]: [When it applies]
- [Exception 2]: [When it applies]

### Implementation

**Location:** [Code path / module]
**Tests:** [Test file / test names]
**Monitoring:** [How violations are detected]

### Related Rules
- [BR-XXX]: [Relationship description]
- [BR-YYY]: [Relationship description]

### Change History
| Date | Change | Author |
|------|--------|--------|
| [Date] | Initial creation | [Name] |
```

---

## Quality Checklist

Before considering business rules documentation complete:

- [ ] **Discovered:** All known rules captured from code, experts, documents
- [ ] **Categorized:** Each rule has a clear category
- [ ] **Specific:** Rules are measurable and testable
- [ ] **Sourced:** Origin and authority documented
- [ ] **Exampled:** Concrete examples for each rule
- [ ] **Mapped:** Rules linked to implementation code
- [ ] **Tested:** Each rule has corresponding test coverage
- [ ] **Governed:** Change process established
- [ ] **Reviewed:** Domain experts have validated

---

## Skill Interactions

### Preceded By
- **02-User Journey Mapping** - Reveals rules through user friction
- **04-Business Domain Modeling** - Rules become invariants

### Followed By
- **03-Executable Spec** - Rules become scenario criteria
- **06-Atomic TDD** - Rules implemented test-first

### Related Skills
- **08-Code Review** - Reviews check rule implementation
- **01-Roadmapping** - Rule changes may require roadmap items
