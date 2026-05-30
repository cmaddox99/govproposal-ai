> Examples for: skill-09-refactoring  
> Parent skill: 09-refactoring.md  
> These are optional pedagogical supplements — not in governance scope.

---

## Refactoring Catalog

### Extract Method

**When:** A code fragment can be grouped together.

**Before:**
```python
def print_order(order):
    print("Order Details:")
    print(f"  Customer: {order.customer_name}")
    print(f"  Address: {order.shipping_address}")
    print(f"  City: {order.city}, {order.state} {order.zip}")

    total = 0
    for item in order.items:
        total += item.price * item.quantity
    print(f"  Total: ${total:.2f}")
```

**After:**
```python
def print_order(order):
    print("Order Details:")
    print_customer_info(order)
    print_order_total(order)

def print_customer_info(order):
    print(f"  Customer: {order.customer_name}")
    print(f"  Address: {order.shipping_address}")
    print(f"  City: {order.city}, {order.state} {order.zip}")

def print_order_total(order):
    total = calculate_total(order)
    print(f"  Total: ${total:.2f}")

def calculate_total(order):
    return sum(item.price * item.quantity for item in order.items)
```

---

### Replace Conditional with Polymorphism

**When:** Conditionals choose behavior based on type.

**Before:**
```python
def calculate_shipping(order):
    if order.shipping_type == "standard":
        return order.weight * 0.5
    elif order.shipping_type == "express":
        return order.weight * 1.5 + 10
    elif order.shipping_type == "overnight":
        return order.weight * 3.0 + 25
    else:
        raise ValueError(f"Unknown shipping type: {order.shipping_type}")
```

**After:**
```python
class ShippingStrategy(ABC):
    @abstractmethod
    def calculate(self, weight: float) -> float:
        pass

class StandardShipping(ShippingStrategy):
    def calculate(self, weight: float) -> float:
        return weight * 0.5

class ExpressShipping(ShippingStrategy):
    def calculate(self, weight: float) -> float:
        return weight * 1.5 + 10

class OvernightShipping(ShippingStrategy):
    def calculate(self, weight: float) -> float:
        return weight * 3.0 + 25

def calculate_shipping(order):
    return order.shipping_strategy.calculate(order.weight)
```

---

### Introduce Parameter Object

**When:** Same parameters always travel together.

**Before:**
```python
def search_flights(origin, destination, departure_date, return_date,
                   passengers, cabin_class, flexible_dates):
    ...

def validate_flight_search(origin, destination, departure_date, return_date,
                          passengers, cabin_class, flexible_dates):
    ...
```

**After:**
```python
@dataclass
class FlightSearchCriteria:
    origin: str
    destination: str
    departure_date: date
    return_date: Optional[date]
    passengers: int
    cabin_class: CabinClass
    flexible_dates: bool = False

def search_flights(criteria: FlightSearchCriteria):
    ...

def validate_flight_search(criteria: FlightSearchCriteria):
    ...
```

---

### Strangler Fig Pattern (Large-Scale)

**When:** Replacing a legacy system incrementally.

```
┌─────────────────────────────────────────────────────┐
│                   STRANGLER FIG                      │
├─────────────────────────────────────────────────────┤
│                                                      │
│   ┌─────────┐         ┌─────────────┐               │
│   │ Request │────────▶│   Router    │               │
│   └─────────┘         └──────┬──────┘               │
│                              │                       │
│              ┌───────────────┼───────────────┐      │
│              ▼               ▼               ▼      │
│      ┌──────────────┐ ┌──────────────┐ ┌──────────┐│
│      │ New Service  │ │ New Service  │ │  Legacy  ││
│      │  (Feature A) │ │  (Feature B) │ │  System  ││
│      └──────────────┘ └──────────────┘ └──────────┘│
│                                                      │
│   Over time, legacy shrinks as new services grow    │
└─────────────────────────────────────────────────────┘
```

**Steps:**
1. Create routing layer in front of legacy
2. Implement new feature in new service
3. Route traffic to new service
4. Repeat until legacy is empty
5. Remove legacy system

---

## Good Examples

### Example 1: Refactoring During Feature Work

**Context:** Need to add cargo weight limits, but the code is tangled.

```markdown
## Approach: Make the change easy, then make the easy change

### Step 1: Refactor First (separate commit)
- Extract CargoValidator class from CargoService
- Move weight-related logic to validator
- All tests still pass
- Commit: "refactor: extract CargoValidator for weight validation"

### Step 2: Add Feature (separate commit)
- Add weight limit check to CargoValidator
- Add new tests for weight limits
- Commit: "feat: add cargo weight limits per aircraft type"
```

**Why it's good:**
- Refactoring is isolated from feature work
- Each commit is single-purpose
- If feature is reverted, refactoring remains

---

### Example 2: Systematic Debt Reduction

**Context:** Hangar SDD change for tech debt sprint

```markdown
# Change: reduce-cargo-service-complexity

## Proposal
Reduce cyclomatic complexity of CargoService from 47 to <10
by extracting focused classes.

## Tasks
- [ ] 1.1 Extract CargoValidator (validation logic)
- [ ] 1.2 Extract CargoPricer (pricing logic)
- [ ] 1.3 Extract CargoRouter (routing logic)
- [ ] 1.4 Inline remaining simple methods
- [ ] 1.5 Update documentation

## Constraints
- All existing tests must pass
- No behavior changes
- Each extraction is a separate commit
```

---

## Bad Examples (Anti-Patterns)

### Anti-Pattern 1: Refactoring Without Tests

```python
# BAD - No tests exist, refactoring anyway

def legacy_calculate_fare(flight_data):
    # 200 lines of complex logic
    # No tests
    # "I'll just clean this up..."
```

**Why it's wrong:**
- No safety net
- Can't verify behavior preserved
- Bugs will be introduced silently

**Correct approach:** Write characterization tests first, then refactor.

---

### Anti-Pattern 2: Big Bang Refactoring

```markdown
# BAD - Massive refactoring PR

PR: "Refactor entire booking module"
- Changed 47 files
- 3,000 lines modified
- "All tests pass"
- Reviewer: 😱
```

**Why it's wrong:**
- Impossible to review effectively
- High risk of hidden behavior changes
- If something breaks, hard to identify cause

**Correct approach:** Small, incremental PRs. One refactoring pattern at a time.

---

### Anti-Pattern 3: Refactoring + Features Together

```python
# BAD - Refactoring and feature in same change

def calculate_shipping(order):
    # Refactored: extracted shipping strategies
    # AND added new "drone delivery" option
    # AND fixed a bug in express shipping
    # All in one commit
```

**Why it's wrong:**
- Can't isolate issues
- Can't revert feature without losing refactoring
- Violates single responsibility of commits

**Correct approach:** Separate commits. Refactor first, then add feature.

---

## Artifacts & Templates

### Template: Refactoring Proposal

```markdown
# Refactoring: [Target Code]

## Current State
**Location:** [file path]
**Smell:** [identified code smell]
**Complexity:** [current metrics]

## Target State
**Pattern:** [refactoring pattern to apply]
**Expected improvement:** [what gets better]

## Approach
1. [ ] Ensure test coverage exists
2. [ ] [Step 1 of refactoring]
3. [ ] [Step 2 of refactoring]
4. [ ] Verify all tests pass
5. [ ] Update documentation if needed

## Constraints
- [ ] No behavior changes
- [ ] All tests must pass at each step
- [ ] Each step is independently committable
```

### Template: Characterization Test

```python
"""
Characterization tests for [module/function]

These tests capture CURRENT behavior before refactoring.
They are not assertions of CORRECT behavior.
If a test fails during refactoring, behavior has changed unintentionally.
"""

class TestCharacterization:
    """Captures current behavior of legacy_function."""

    def test_known_input_produces_known_output(self):
        """Captured on [date] before refactoring."""
        result = legacy_function(known_input)
        assert result == captured_output

    def test_edge_case_behavior(self):
        """Documents current edge case handling."""
        result = legacy_function(edge_case_input)
        assert result == captured_edge_case_output
```

---

