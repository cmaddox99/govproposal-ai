---
skill:
  id: skill-04-business-domain-modeling
  name: Business Domain Modeling
  category: modeling
  version: "2.0.0"

laws:
  implements:
    - id: ENG-2.1
      title: Domain-Driven Design Law
    - id: ENG-2.4
      title: Bounded Context Law
    - id: ENG-3.4
      title: Single Responsibility Principle
  references:
    - id: ENG-2.2
      title: Layered Architecture Law
    - id: ENG-3.2
      title: Immutability Law
    - id: PRD-2.2
      title: Assumption Mapping Law

triggers:
  phrases:
    - "Design the domain model"
    - "Identify aggregates"
    - "Define bounded contexts"
    - "Where should this logic go?"

followed_by:
  - skill-05-business-rules
  - skill-06-atomic-tdd
---

# Skill: Business Domain Modeling

> **Purpose:** Design rich domain models that capture business behavior and enforce invariants.

---

## Purpose

Business Domain Modeling applies Domain-Driven Design (DDD) to create software models that reflect the business domain. This skill ensures:

1. **Business alignment** - Code speaks the language of the business
2. **Behavior encapsulation** - Domain logic lives in domain objects
3. **Invariant protection** - Business rules are enforced at the model level
4. **Bounded contexts** - Clear boundaries prevent model pollution

The goal is to create models that are **behavior-rich**, not anemic data containers.

---

## When to Invoke

Invoke this skill when:

- Designing a new feature's domain layer
- Refactoring existing code to improve domain modeling
- Identifying aggregate boundaries
- Establishing ubiquitous language with stakeholders
- Resolving confusion about where logic belongs

**Trigger phrases:**
- "Where should this business logic live?"
- "What's the aggregate root here?"
- "Is this an entity or value object?"
- "Let's model this domain"

---

## Constitutional Foundation

### Engineering Constitution
- **Article II, Section 2.1** - Domain-Driven Design: "Model the domain, not the database"
- **Article II, Section 2.2** - Ubiquitous Language: "Code uses business terminology"
- **Article II, Section 2.3** - Bounded Contexts: "Explicit boundaries between models"
- **Article II, Section 2.4** - Aggregates: "Consistency boundaries around invariants"

### Product Constitution
- **Article III, Section 3.1** - User Language: "Product speaks user's language"

### Business Constitution
- **Article II, Section 2.1** - Business Rules: "Rules are explicit and enforced"

---

## Method

### Step 1: Event Storm the Domain

Discover domain events through collaborative modeling:

**Domain Events:**
- Things that happen in the business (past tense)
- Important enough that the business cares
- Examples: OrderPlaced, PaymentReceived, ItemShipped

**Process:**
1. List all events that occur in this domain
2. Sequence them on a timeline
3. Identify commands that trigger events
4. Find the actors who issue commands

### Step 2: Identify Bounded Contexts

Draw boundaries around distinct models:

**Guiding Questions:**
- Where does the language change meaning?
- Which teams own which concepts?
- Where do we need different models of the same thing?

**Example:**
- **Sales Context:** Customer has payment info, purchase history
- **Support Context:** Customer has tickets, satisfaction score
- **Shipping Context:** Customer has address, delivery preferences

Each context has its own Customer model with different attributes.

### Step 3: Define Ubiquitous Language

Create a glossary of domain terms:

**Format:**
```
Term: [Business term]
Context: [Which bounded context]
Definition: [Clear, unambiguous definition]
Examples: [Concrete examples]
Not to be confused with: [Similar terms]
```

**Rules:**
- Same term should have same meaning everywhere in a context
- Different contexts may have different definitions
- Code must use these exact terms

### Step 4: Classify Building Blocks

Categorize domain concepts:

| Type | Characteristics | Examples |
|------|-----------------|----------|
| **Entity** | Has identity, changes over time | Order, Customer, Product |
| **Value Object** | No identity, immutable, equality by value | Money, Address, DateRange |
| **Aggregate** | Cluster of entities with a root | Order (with OrderLines) |
| **Domain Service** | Stateless operations across entities | PricingService, TaxCalculator |
| **Domain Event** | Something that happened | OrderPlaced, PaymentFailed |

### Step 5: Design Aggregates

Define consistency boundaries:

**Aggregate Design Rules:**
1. Each aggregate has exactly one root entity
2. External references only to the root
3. All changes go through the root
4. Invariants enforced within aggregate boundary
5. Keep aggregates small

**Guiding Questions:**
- What must be consistent together?
- What can be eventually consistent?
- What's the transactional boundary?

### Step 6: Model Behavior, Not Data

Create behavior-rich objects:

**Bad (Anemic):**
```java
class Order {
    private List<OrderLine> lines;

    public List<OrderLine> getLines() { return lines; }
    public void setLines(List<OrderLine> lines) { this.lines = lines; }
}

// Logic scattered in services
class PalApplicationService {
    public void addLine(PalApplication application, Product product, int quantity) {
        OrderLine line = new OrderLine(product, quantity);
        application.getLines().add(line);
    }
}
```

**Good (Behavior-Rich):**
```java
class Order {
    private List<OrderLine> lines;

    public void addItem(Product product, Quantity quantity) {
        if (this.isFinalized()) {
            throw new OrderAlreadyFinalizedException();
        }
        OrderLine existing = findLineFor(product);
        if (existing != null) {
            existing.increaseQuantity(quantity);
        } else {
            lines.add(new OrderLine(product, quantity));
        }
    }
}
```

### Step 7: Enforce Invariants

Business rules enforced in the model:

**Types of Invariants:**
- **Creation invariants:** Valid state on construction
- **Transition invariants:** Valid state changes
- **Aggregate invariants:** Consistency across members

**Implementation:**
- Validate in constructors
- Validate in mutation methods
- Never expose internal collections directly
- Use factory methods for complex creation

### Step 8: Document the Model

Create visual and written documentation:

- Context map showing bounded contexts
- Aggregate diagrams showing roots and members
- Ubiquitous language glossary
- Invariant specifications

---

## Quality Checklist

Before considering the domain model complete:

- [ ] **Behavior-Rich:** Domain objects have methods, not just getters/setters
- [ ] **Invariants Protected:** Business rules enforced in domain layer
- [ ] **Ubiquitous Language:** Code uses business terms consistently
- [ ] **Proper Classification:** Entities vs Value Objects correctly identified
- [ ] **Small Aggregates:** Each aggregate has clear, minimal scope
- [ ] **Factory Methods:** Complex creation uses factories
- [ ] **Domain Events:** Significant state changes raise events
- [ ] **No Primitives:** Domain concepts wrapped in value objects

---

## Skill Interactions

### Preceded By
- **02-User Journey Mapping** - Provides domain context
- **05-Business Rules** - Rules become invariants

### Followed By
- **06-Atomic TDD** - Implements domain model test-first
- **03-Executable Spec** - Specs use domain language

### Related Skills
- **07-Vertical Slice Dev** - Slices respect aggregate boundaries
- **08-Code Review** - Reviews check domain model integrity

> 📎 Examples: See 04-business-domain-modeling-examples.md
