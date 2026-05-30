---
domain: engineering
article: III
title: Code Quality Laws
laws:
  - id: ENG-3.1
    title: Complexity Limits
    summary: Functions/methods SHALL have cyclomatic complexity ≤10, cognitive complexity ≤7
  - id: ENG-3.2
    title: Immutability Law
    summary: State representations SHALL be constructed once and never modified
  - id: ENG-3.3
    title: Law of Demeter
    summary: Components SHALL only interact with immediate collaborators, never navigating through intermediaries
  - id: ENG-3.4
    title: Single Responsibility Principle
    summary: Every module/class/function SHALL have ONE reason to change
  - id: ENG-3.5
    title: Naming Conventions Law
    summary: Names SHALL reveal intent using consistent conventions
  - id: ENG-3.6
    title: Documentation Law
    summary: Public APIs and complex algorithms MUST be documented
  - id: ENG-3.7
    title: Error Handling Law
    summary: Errors SHALL be represented with specific types and handled explicitly
  - id: ENG-3.8
    title: Continuous Refactoring Patterns
    summary: Apply standard refactoring patterns during refactoring phase
  - id: ENG-3.9
    title: Open/Closed Principle
    summary: Software entities SHALL be open for extension but closed for modification
  - id: ENG-3.10
    title: Liskov Substitution Principle
    summary: Subtypes SHALL be substitutable for their base types without breaking correctness
  - id: ENG-3.11
    title: Interface Segregation Principle
    summary: Clients SHALL NOT be forced to depend on interfaces they do not use
---

<!-- SPDX-FileCopyrightText: 2026 Click Chain AI -->
<!-- SPDX-License-Identifier: LicenseRef-ClickChain-Proprietary -->
# Article III: Code Quality Laws

## Section 3.1: Complexity Limits

**Law ID:** `ENG-3.1` | **Status:** STRICTLY ENFORCED

| Metric | Limit | Enforcement |
|--------|-------|-------------|
| **Cyclomatic Complexity** | ≤ 10 per function/method | Build fails |
| **Cognitive Complexity** | ≤ 7 per function/method | Build fails |
| **Function/Method Length** | ≤ 50 lines | Warning → Fail |
| **Class/Module Length** | ≤ 300 lines | Warning |
| **Function Parameters** | ≤ 4 (use objects for more) | Warning |
| **Nesting Depth** | ≤ 3 levels | Warning |
| **File Size** | ≤ 500 lines | Warning |

### When Limits Exceeded

Refactor immediately:
- Decompose large operations into focused sub-operations
- Handle edge cases early to flatten the main path
- Replace conditional type-checking with type-directed behavior

---

## Section 3.2: Immutability Law

**Law ID:** `ENG-3.2`

Facts don't change — new facts replace old facts.

State representations SHALL be constructed once and never modified:

- **Construct once** — Representations are created complete and valid; partial or incremental assembly that exposes intermediate invalid states is prohibited
- **Transform by replacement** — Operations that derive new state produce new representations; they never alter the original
- **Read-only exposure** — Composite state (collections, nested structures) is exposed for reading only; structural changes produce new composites
- **Identity by value** — Two representations with the same attributes are equal, regardless of when or where they were created

### Benefits

- Thread safety without synchronization
- Predictable behavior
- Easier testing and debugging

### Avatar Guidance

Each technology avatar provides idiomatic patterns:
- Python: `@dataclass(frozen=True)`, `NamedTuple`
- Java: `record`, `@Embeddable` with no setters
- TypeScript: `readonly` properties, `as const`
- .NET: `record`, `init`-only properties
- Swift/Kotlin: `let`/`val`, value types
- React Native: `readonly`, Redux immutable patterns

---

## Section 3.3: Law of Demeter (Tell, Don't Ask)

**Law ID:** `ENG-3.3`

A component SHALL only interact with its immediate collaborators — never navigate through an intermediary to reach a third party.

```
❌ VIOLATION (Transitive Navigation)
destination = order → customer → address → city → name

✅ COMPLIANT (Direct Collaboration)
destination = order.deliveryCity()
```

### Rule

A component may only interact with:
- Itself
- Its direct dependencies (injected or composed)
- Objects it receives as arguments
- Objects it creates internally

### Avatar Guidance

Each technology avatar provides idiomatic examples of encapsulating traversals behind direct collaborator methods.

---

## Section 3.4: Single Responsibility Principle

**Law ID:** `ENG-3.4`

Every module/class/function SHALL have ONE reason to change:

- Classes named for what they ARE (noun)
- Functions named for what they DO (verb)
- If you can't name it clearly, it does too much
- "And" in a name suggests violation

---

## Section 3.5: Naming Conventions Law

**Law ID:** `ENG-3.5`

Names SHALL reveal intent and follow the idiomatic conventions of the technology in use.

### Universal Principles

- **Types/Concepts** — Named as nouns describing what they represent
- **Actions/Operations** — Named as verbs describing what they do
- **Predicates** — Prefixed to indicate boolean nature (is/has/can/should)
- **Constants** — Visually distinct from variables (convention varies by language)
- **Consistency** — One convention per project, enforced by tooling

### PROHIBITED (Universal)

- Single-letter names (except short-lived loop indices)
- Abbreviations (unless universally understood: `id`, `url`, `http`)
- Generic names without context: `data`, `info`, `manager`, `processor`
- Encoding type in name (Hungarian notation)

### Avatar Guidance

See technology avatar for language-idiomatic casing conventions (PascalCase, camelCase, snake_case, etc.).

---

## Section 3.6: Documentation Law

**Law ID:** `ENG-3.6`

### Required Documentation

- All public APIs: Purpose, parameters, return values, exceptions
- Complex algorithms: Inline comments explaining WHY (not WHAT)
- Configuration: Purpose of each setting
- Architecture decisions: ADRs for significant choices

### PROHIBITED

- Commented-out code (delete it, Git has history)
- TODO without linked issue/ticket
- Obvious comments (`// increment counter` before `counter++`)
- Outdated comments (worse than no comments)

---

## Section 3.7: Error Handling Law

**Law ID:** `ENG-3.7`

Errors SHALL be represented with specific, descriptive types and handled explicitly:

- Represent errors with specific types that describe what went wrong (not generic "something failed")
- Handle errors at the appropriate level — where recovery is possible
- Never silently discard errors
- Fail fast on programming errors; recover gracefully from operational errors
- Log errors with context (what was being attempted, with what inputs)

---

## Section 3.8: Continuous Refactoring Patterns

**Law ID:** `ENG-3.8`

Apply these patterns during refactoring:

| Problem | Action | Application |
|---------|--------|-------------|
| Large operation | Decompose | Break into focused sub-operations |
| Many related parameters | Group | Consolidate into a cohesive structure |
| Deep nesting | Simplify | Handle edge cases early to flatten the main path |
| Conditional type-checking | Dispatch | Replace with type-directed behavior |
| Duplicated logic | Consolidate | Unify into a single reusable definition |
| Misplaced logic | Co-locate | Place logic with the data it operates on |
| Raw primitives for domain concepts | Elevate | Replace with domain-meaningful types |

---

## Section 3.9: Open/Closed Principle

**Law ID:** `ENG-3.9`

Software entities (classes, modules, functions) SHALL be **open for extension but closed for modification**. Adding new behavior should not require editing existing, tested code.

### Requirements

- Design extension points (interfaces, hooks, plugins) for anticipated variations
- Use strategy patterns over conditionals for varying behavior
- Employ plugin architectures for new features
- Maintain backward compatibility and stable interfaces
- Extend functionality through composition or inheritance

### Violations

- Adding if/switch branches for new types (should use polymorphism)
- Modifying existing methods to support new cases (should extend)
- Breaking existing callers when adding features
- Hardcoding dependencies instead of injecting abstractions

### Avatar Guidance

**Java/Kotlin:**
- Use interfaces and abstract classes for extension points
- Prefer `sealed interface` (Kotlin) for known variations
- Apply Strategy, Template Method, and Visitor patterns

**Python:**
- Use abstract base classes (`abc.ABC`)
- Duck typing enables easy extension
- Prefer Protocol types for structural subtyping

**TypeScript/JavaScript:**
- Use interfaces and abstract classes
- Function composition over class hierarchies
- Higher-order functions for behavioral extension

**Go:**
- Use interfaces for polymorphism
- Functional options pattern for configuration
- Table-driven tests for extensibility validation

**.NET:**
- Use interfaces and abstract classes
- Prefer composition via dependency injection
- Apply decorator and adapter patterns

### Example

**❌ VIOLATION (switch statement requires modification for new payment types):**

```typescript
class PaymentProcessor {
  processPayment(type: string, amount: number): void {
    switch (type) {
      case 'credit_card':
        this.chargeCreditCard(amount);
        break;
      case 'paypal':
        this.chargePayPal(amount);
        break;
      // Adding 'crypto' requires modifying this switch
      default:
        throw new Error('Unknown payment type');
    }
  }
}
```

**✅ COMPLIANT (Strategy pattern allows extension without modification):**

```typescript
interface PaymentMethod {
  charge(amount: number): void;
}

class CreditCardPayment implements PaymentMethod {
  charge(amount: number): void {
    // Credit card logic
  }
}

class PayPalPayment implements PaymentMethod {
  charge(amount: number): void {
    // PayPal logic
  }
}

// NEW: CryptoPayment added without modifying existing code
class CryptoPayment implements PaymentMethod {
  charge(amount: number): void {
    // Crypto logic
  }
}

class PaymentProcessor {
  constructor(private method: PaymentMethod) {}
  
  processPayment(amount: number): void {
    this.method.charge(amount);
  }
}
```

---

## Section 3.10: Liskov Substitution Principle

**Law ID:** `ENG-3.10`

Subtypes SHALL be **substitutable for their base types without altering the correctness** of the program. A subclass should strengthen postconditions (what it guarantees) and weaken preconditions (what it requires), never the reverse.

### Requirements

- Subtypes preserve invariants of the base type
- Override methods maintain or strengthen postconditions (cannot weaken)
- Override methods maintain or weaken preconditions (cannot strengthen)
- Exceptions thrown by overrides must be same or more specific than base
- Behavioral contracts must be honored (not just syntactic signatures)

### Violations

- Subtype throws exceptions not thrown by base type
- Subtype requires stricter preconditions than base (e.g., narrower input range)
- Subtype provides weaker postconditions than base (e.g., returns null when base never does)
- Subtype changes expected side effects or state transitions
- Inheritance for code reuse when IS-A relationship doesn't hold

### Avatar Guidance

**Java/Kotlin:**
- Use `@Override` annotation to catch signature mismatches
- Prefer composition over inheritance when behavioral contracts differ
- Use `sealed` classes (Kotlin) to constrain inheritance

**Python:**
- Override `__eq__`, `__hash__` consistently in subclasses
- Use `abc.ABC` to define behavioral contracts
- Type hints help document expected behavior

**TypeScript:**
- Structural typing catches many LSP violations at compile time
- Use `implements` over `extends` when behavior diverges
- Document behavioral contracts with JSDoc

**Go:**
- Interfaces define behavioral contracts
- Embedding should preserve parent behavior
- Test substitutability explicitly

**.NET:**
- Use `virtual`/`override` keywords intentionally
- Covariant return types (C# 9+) help maintain LSP
- Analyzer warnings catch many violations

### Example

**❌ VIOLATION (Square breaks Rectangle's width/height independence):**

```python
class Rectangle:
    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height
    
    def set_width(self, width: int):
        self._width = width
    
    def set_height(self, height: int):
        self._height = height
    
    def area(self) -> int:
        return self._width * self._height

class Square(Rectangle):  # VIOLATION: Square IS-NOT-A Rectangle behaviorally
    def set_width(self, width: int):
        self._width = width
        self._height = width  # Breaks independence assumption
    
    def set_height(self, height: int):
        self._width = height
        self._height = height

# This code expects Rectangle behavior but breaks with Square:
def test_resize(rect: Rectangle):
    rect.set_width(5)
    rect.set_height(4)
    assert rect.area() == 20  # FAILS for Square (area = 16)
```

**✅ COMPLIANT (Separate abstractions for different contracts):**

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> int:
        pass

class Rectangle(Shape):
    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height
    
    def set_width(self, width: int):
        self._width = width
    
    def set_height(self, height: int):
        self._height = height
    
    def area(self) -> int:
        return self._width * self._height

class Square(Shape):  # No longer inherits Rectangle
    def __init__(self, side: int):
        self._side = side
    
    def set_side(self, side: int):
        self._side = side
    
    def area(self) -> int:
        return self._side * self._side

# Code operates on the Shape abstraction:
def print_area(shape: Shape):
    print(f"Area: {shape.area()}")  # Works for both Rectangle and Square
```

---

## Section 3.11: Interface Segregation Principle

**Law ID:** `ENG-3.11`

Clients SHALL NOT be forced to depend on interfaces they do not use. Prefer many **specific, cohesive interfaces** over one large, general-purpose interface.

### Requirements

- Interfaces should be client-focused (role interfaces)
- Split large interfaces into cohesive subsets
- Clients implement/depend only on methods they actually use
- Avoid "fat" interfaces with unrelated operations
- Use composition to combine capabilities when needed

### Violations

- Interface with methods only some implementations use (forces no-op stubs)
- Clients forced to implement methods they'll never call
- Single interface serving multiple unrelated use cases
- Interface pollution (adding methods for one client that breaks others)

### Avatar Guidance

**Java/Kotlin:**
- Use small, focused interfaces
- Apply `default` methods (Java 8+) sparingly (can hide ISP violations)
- Kotlin: Use delegation to compose interfaces without boilerplate

**Python:**
- Use Protocol types (`typing.Protocol`) for structural contracts
- Duck typing naturally enforces ISP (no forced dependencies)
- Abstract base classes should be minimal

**TypeScript:**
- Interfaces are free — create many small ones
- Use intersection types to combine interfaces
- Structural typing makes ISP violations obvious

**Go:**
- Embrace small interfaces (idiomatic Go: 1-3 methods)
- Consumers define interfaces, not producers
- Use embedding to compose interfaces

**.NET:**
- Use small interfaces (e.g., `IDisposable`, `IEquatable<T>`)
- Avoid marker interfaces (use attributes instead)
- C# 8+: Use default interface methods cautiously

### Example

**❌ VIOLATION (fat interface forces unused methods on clients):**

```java
interface Worker {
    void work();
    void eat();
    void sleep();
    void receiveSalary();
}

class HumanWorker implements Worker {
    public void work() { /* ... */ }
    public void eat() { /* ... */ }
    public void sleep() { /* ... */ }
    public void receiveSalary() { /* ... */ }
}

class RobotWorker implements Worker {
    public void work() { /* ... */ }
    public void eat() { /* NO-OP stub — robots don't eat */ }
    public void sleep() { /* NO-OP stub — robots don't sleep */ }
    public void receiveSalary() { /* NO-OP stub — robots aren't paid */ }
}
```

**✅ COMPLIANT (segregated interfaces per client need):**

```java
interface Workable {
    void work();
}

interface Feedable {
    void eat();
}

interface Restable {
    void sleep();
}

interface Payable {
    void receiveSalary();
}

class HumanWorker implements Workable, Feedable, Restable, Payable {
    public void work() { /* ... */ }
    public void eat() { /* ... */ }
    public void sleep() { /* ... */ }
    public void receiveSalary() { /* ... */ }
}

class RobotWorker implements Workable {
    public void work() { /* ... */ }
    // Only implements what it needs — no forced stubs
}

// Clients depend only on what they need:
class WorkManager {
    void manage(Workable worker) {
        worker.work();  // Doesn't care about eating, sleeping, or salary
    }
}
```

