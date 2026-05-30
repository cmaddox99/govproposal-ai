---
law_id: ENG-4.1
avatar: python-fastapi
---

# ENG-4.1: Atomic TDD Examples for Python/FastAPI

## COMPLIANT: TDD Cycle with pytest

```python
# test_order_service.py

# Step 1: RED - Write failing test
def test_calculate_total_with_single_item_returns_item_price():
    # GIVEN
    order = OrderFixture.with_single_item(price=Money(Decimal("10.00")))
    service = OrderService(tax_calculator=NoOpTaxCalculator())

    # WHEN
    total = service.calculate_total(order)

    # THEN
    assert total.subtotal == Money(Decimal("10.00"))


# Step 2: GREEN - Write minimum code (in order_service.py)
class OrderService:
    def calculate_total(self, order: Order) -> OrderTotal:
        subtotal = order.items[0].total
        return OrderTotal(subtotal=subtotal, tax=Money.zero(), shipping=Money.zero())


# Step 3: REFACTOR - Improve while green
class OrderService:
    def calculate_total(self, order: Order) -> OrderTotal:
        subtotal = self._calculate_subtotal(order.items)
        return OrderTotal(subtotal=subtotal, tax=Money.zero(), shipping=Money.zero())

    def _calculate_subtotal(self, items: Sequence[LineItem]) -> Money:
        return reduce(lambda acc, item: acc.add(item.total), items, Money.zero())


# Step 4: Commit, then write NEXT test
def test_calculate_total_with_multiple_items_returns_sum():
    # Next TDD cycle...
    pass
```

**Why compliant:** One test at a time, minimal code to pass, refactor continuously.

---

## VIOLATION: Batch Testing

```python
# BAD: Multiple tests before any implementation
def test_empty_order():
    order = Order()
    assert order.total == Money.zero()

def test_single_item():
    order = Order()
    order.add_item(Item(price=Money(10)))
    assert order.total == Money(10)

def test_multiple_items():
    order = Order()
    order.add_item(Item(price=Money(10)))
    order.add_item(Item(price=Money(20)))
    assert order.total == Money(30)

def test_with_discount():
    order = Order()
    order.add_item(Item(price=Money(100)))
    order.apply_discount(Decimal("0.1"))
    assert order.total == Money(90)

# Then writing all code at once to pass all tests
```

**Why violates ENG-4.1:** Loses incremental design feedback, encourages over-engineering upfront, makes it harder to identify which requirement caused a failure.

---

## TDD Cycle Commands

```bash
# RED: Run test, see it fail
pytest tests/test_order.py::TestOrder::test_adding_item_updates_total -v

# GREEN: Write code, run test again
pytest tests/test_order.py::TestOrder::test_adding_item_updates_total -v

# REFACTOR: Run all tests after refactoring
pytest

# VERIFY: Check coverage and constitutional compliance
pytest --cov=src --cov-fail-under=80
constitution-lint .

# Commit when green and compliant
git add -A && git commit -m "Add item price calculation to Order"
```
