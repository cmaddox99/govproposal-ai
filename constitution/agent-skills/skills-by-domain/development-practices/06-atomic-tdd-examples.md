> Examples for: skill-06-atomic-tdd  
> Parent skill: 06-atomic-tdd.md  
> These are optional pedagogical supplements — not in governance scope.

---

## Good Examples

### Example 0: Working with Hangar SDD Test Tasks

**Context:** Executing TDD against pre-planned test pyramid tasks

**Hangar SDD Task File:** `hangar-ai-specs/changes/shopping-cart/tasks.md` (created in planning phase)

```markdown
## Slice: Add Item to Cart

### Unit Tests (70-80%)
- [x] UNIT: Cart.addItem() - adds new item to empty cart       ✓
- [x] UNIT: Cart.addItem() - increases quantity when item exists ✓
- [x] UNIT: Cart.addItem() - rejects negative quantities        ✓
- [ ] UNIT: CartItem.calculateSubtotal() - multiplies price by quantity  ← CURRENT
- [ ] UNIT: CartItem.calculateSubtotal() - handles decimal prices

### Integration Tests (15-25%)
- [ ] INT: POST /cart/items - creates cart item and returns 201
- [ ] INT: CartRepository.save() - persists cart to database

### E2E Tests (5-10%)
- [ ] E2E: User adds item to cart - item appears in cart

### Current Cycle
**Active:** UNIT: CartItem.calculateSubtotal() - multiplies price by quantity
**Phase:** RED
```

**TDD Workflow:**
1. Pick next uncompleted task (UNIT: CartItem.calculateSubtotal)
2. Run 8-step TDD cycle
3. Mark task complete: `- [x] UNIT: CartItem.calculateSubtotal()...`
4. Update "Current Cycle" to next task
5. Repeat until slice complete

---

### Example 1: Shopping Cart Add Item

**Context:** Implementing "add item to cart" functionality

**Cycle 1: Empty cart returns zero items**

```python
# Step 1: Identify behavior - empty cart has no items
# Step 2: Write failing test (RED)

def test_new_cart_has_zero_items():
    # Arrange
    cart = ShoppingCart()

    # Act
    count = cart.item_count()

    # Assert
    assert count == 0
```

```python
# Step 3: Verify test fails - NameError: ShoppingCart not defined
# Step 4: Write minimal code (GREEN)

class ShoppingCart:
    def item_count(self):
        return 0
```

```python
# Step 5: Test passes
# Step 6: No refactoring needed yet
# Step 7: Tests pass
# Step 8: Continue to next behavior
```

**Cycle 2: Adding one item increases count**

```python
# Step 2: Write failing test (RED)

def test_adding_item_increases_count():
    # Arrange
    cart = ShoppingCart()
    item = Item(sku="WIDGET-001", price=9.99)

    # Act
    cart.add(item)

    # Assert
    assert cart.item_count() == 1
```

```python
# Step 4: Write minimal code (GREEN)

class ShoppingCart:
    def __init__(self):
        self._items = []

    def add(self, item):
        self._items.append(item)

    def item_count(self):
        return len(self._items)
```

**Cycle 3: Adding same item twice increases quantity**

```python
# Step 2: Write failing test (RED)

def test_adding_same_item_twice_increases_quantity():
    # Arrange
    cart = ShoppingCart()
    item = Item(sku="WIDGET-001", price=9.99)

    # Act
    cart.add(item)
    cart.add(item)

    # Assert
    assert cart.item_count() == 1  # Still one line item
    assert cart.get_quantity("WIDGET-001") == 2
```

**Why it's good:**
- Each cycle tests ONE behavior
- Tests are independent
- Minimal code at each step
- Natural design emergence

### Example 2: Password Validation

**Context:** Implementing password strength validation

```python
# Cycle 1: Password must be at least 8 characters

def test_password_shorter_than_8_characters_is_invalid():
    result = validate_password("short")
    assert result.is_valid == False
    assert "at least 8 characters" in result.errors
```

```python
# Minimal implementation
def validate_password(password):
    errors = []
    if len(password) < 8:
        errors.append("Password must be at least 8 characters")
    return ValidationResult(is_valid=len(errors) == 0, errors=errors)
```

```python
# Cycle 2: Password must contain a number

def test_password_without_number_is_invalid():
    result = validate_password("longpassword")
    assert result.is_valid == False
    assert "at least one number" in result.errors
```

```python
# Cycle 3: Valid password passes all rules

def test_valid_password_passes_validation():
    result = validate_password("securepass1")
    assert result.is_valid == True
    assert result.errors == []
```

---

## Bad Examples (Anti-Patterns)

### Anti-Pattern 1: Writing Multiple Tests Before Code

```python
# BAD - Multiple tests written before any implementation

def test_cart_is_empty_initially():
    cart = ShoppingCart()
    assert cart.item_count() == 0

def test_can_add_item_to_cart():
    cart = ShoppingCart()
    cart.add(Item("SKU-1", 10.00))
    assert cart.item_count() == 1

def test_can_remove_item_from_cart():
    cart = ShoppingCart()
    cart.add(Item("SKU-1", 10.00))
    cart.remove("SKU-1")
    assert cart.item_count() == 0

def test_cart_calculates_total():
    cart = ShoppingCart()
    cart.add(Item("SKU-1", 10.00))
    cart.add(Item("SKU-2", 20.00))
    assert cart.total() == 30.00

# Then writing all the code at once...
```

**Why it's wrong:**
- Loses the design feedback from each cycle
- Temptation to over-engineer
- Harder to debug when tests fail
- Not truly test-DRIVEN

**Correct approach:** One test → one implementation → refactor → repeat

### Anti-Pattern 2: Testing Implementation Details

```python
# BAD - Testing internal implementation

def test_cart_uses_dictionary_internally():
    cart = ShoppingCart()
    cart.add(Item("SKU-1", 10.00))
    # Testing internal data structure!
    assert isinstance(cart._items, dict)
    assert "SKU-1" in cart._items

def test_cart_stores_item_with_correct_keys():
    cart = ShoppingCart()
    cart.add(Item("SKU-1", 10.00))
    # Testing internal storage format!
    assert cart._items["SKU-1"]["price"] == 10.00
```

**Why it's wrong:**
- Tests break when refactoring internals
- Couples tests to implementation
- Doesn't test actual behavior
- Leads to fragile test suites

**Correct approach:**
```python
# GOOD - Testing behavior through public interface

def test_cart_total_reflects_added_items():
    cart = ShoppingCart()
    cart.add(Item("SKU-1", 10.00))
    assert cart.total() == 10.00
```

### Anti-Pattern 3: Skipping the RED Phase

```python
# BAD - Writing test and code together, never seeing RED

def test_add_item():
    cart = ShoppingCart()  # Already implemented
    cart.add(Item("SKU-1", 10.00))  # Already implemented
    assert cart.item_count() == 1  # Passes immediately
```

**Why it's wrong:**
- No proof the test can fail
- May be testing the wrong thing
- May pass for wrong reasons
- Misses design feedback

**Correct approach:** Always run the test first and see it fail before writing implementation.

### Anti-Pattern 4: Starting TDD Without Pyramid Tasks

```markdown
# BAD - Starting TDD without categorized test tasks

Developer: "Let's just start writing tests..."

## Tests (no pyramid structure)
- [ ] Test registration works
- [ ] Test email validation
- [ ] Test full registration flow E2E
- [ ] Test registration with existing email E2E

# Result: 50% E2E tests - pyramid is inverted!
```

**Why it's wrong:**
- No visibility into test distribution
- E2E tests are slow and brittle
- Missing unit tests for edge cases
- Violates Article IV, Section 4.2 (Test Pyramid Law)

**Correct action:** Go back to planning phase and create pyramid-balanced tasks.

**Correct approach:**
```markdown
## Slice: User Registration

### Unit Tests (target: 70-80%)
- [ ] UNIT: User.validateEmail() - rejects invalid format
- [ ] UNIT: User.validateEmail() - accepts valid format
- [ ] UNIT: User.validatePassword() - enforces minimum length
- [ ] UNIT: User.validatePassword() - requires special character
- [ ] UNIT: RegistrationService.register() - creates user with hashed password
- [ ] UNIT: RegistrationService.register() - throws on duplicate email

### Integration Tests (target: 15-25%)
- [ ] INT: POST /users - creates user and returns 201
- [ ] INT: POST /users - returns 409 for duplicate email
- [ ] INT: UserRepository.save() - persists user to database

### E2E Tests (target: 5-10%)
- [ ] E2E: New user registration - complete happy path

# Result: 60% unit, 30% integration, 10% E2E - healthy pyramid
```

---

### Anti-Pattern 5: Gold Plating During GREEN Phase

```python
# BAD - Adding unrequested features to make the test pass

def test_can_add_item():
    cart = ShoppingCart()
    cart.add(Item("SKU-1", 10.00))
    assert cart.item_count() == 1

# Over-engineered implementation
class ShoppingCart:
    def __init__(self, currency="USD", tax_rate=0.0, max_items=100):
        self._items = {}
        self._currency = currency
        self._tax_rate = tax_rate
        self._max_items = max_items
        self._created_at = datetime.now()
        self._last_modified = None

    def add(self, item, quantity=1, gift_wrap=False):
        # Way more than the test requires...
```

**Why it's wrong:**
- YAGNI (You Aren't Gonna Need It)
- Untested code paths
- Increased complexity
- Harder to maintain

**Correct approach:** Write ONLY the code the test requires. No more.

---

## Artifacts & Templates

### Hangar SDD Task File

Test pyramid tasks are created during the planning phase. See the [spec-governance skill](../discovery-research/spec-governance.md) for the task file template.

**Location:** `hangar-ai-specs/changes/<feature-name>/tasks.md`

As you complete each TDD cycle, mark the corresponding task as done:
```markdown
- [x] UNIT: Cart.addItem() - adds item to empty cart  ✓ Complete
- [ ] UNIT: Cart.addItem() - increases quantity       ← Current
- [ ] INT: POST /cart/items - returns 201
```

---

### Template: Test File Structure

```python
"""
Tests for [Module/Feature Name]

These tests verify [brief description of what's being tested].
Related specification: [link to spec file]
"""

import pytest
from module_under_test import ClassUnderTest


class TestFeatureName:
    """Tests for [feature or behavior group]"""

    def test_[behavior_when_condition](self):
        """[Brief description of expected behavior]"""
        # Arrange
        sut = ClassUnderTest()

        # Act
        result = sut.method_under_test()

        # Assert
        assert result == expected_value

    def test_[another_behavior](self):
        """[Brief description]"""
        # Arrange
        # Act
        # Assert
        pass
```

### Template: TDD Cycle Checklist

```markdown
## TDD Cycle Checklist

### Cycle #[N]: [Behavior being implemented]

#### RED Phase
- [ ] Test written
- [ ] Test run
- [ ] Test fails
- [ ] Failure is for expected reason (not syntax/setup error)
- [ ] Failure message is clear

#### GREEN Phase
- [ ] Minimal code written
- [ ] New test passes
- [ ] All tests pass
- [ ] No extra code added

#### REFACTOR Phase
- [ ] Duplication removed
- [ ] Names are clear
- [ ] Code is simple
- [ ] All tests still pass

#### Completion
- [ ] Ready for next cycle OR
- [ ] Ready to commit
```

### Template: Bug Fix TDD

```markdown
## Bug Fix: [Bug Description]

### Step 1: Reproduce with Test
Write a test that fails due to the bug:

```python
def test_bug_[issue_number]_[description]():
    """
    Reproduces bug #[number]: [description]
    Expected: [what should happen]
    Actual: [what happens currently]
    """
    # Arrange - set up conditions that trigger the bug

    # Act - perform action that exposes the bug

    # Assert - verify correct behavior (will fail until fixed)
```

### Step 2: Verify Test Fails
- [ ] Test fails
- [ ] Failure matches bug description

### Step 3: Fix the Bug
- [ ] Minimal fix applied
- [ ] Test passes

### Step 4: Verify No Regressions
- [ ] All tests pass

### Step 5: Refactor if Needed
- [ ] Code improved
- [ ] Tests pass
```

---

