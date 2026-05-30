---
law_id: ENG-3.2
avatar: nodejs-typescript
---

# ENG-3.2: Immutability Law Examples for Node.js/TypeScript

## COMPLIANT: Immutable Value Object (readonly Properties)

```typescript
// Immutable value object using readonly properties
type Money = {
  readonly amount: number;
  readonly currency: string;
};

function createMoney(amount: number, currency: string): Money {
  if (amount < 0) {
    throw new Error("Amount cannot be negative");
  }
  if (!currency) {
    throw new Error("Currency is required");
  }
  return Object.freeze({ amount, currency });
}

function addMoney(a: Money, b: Money): Money {
  if (a.currency !== b.currency) {
    throw new CurrencyMismatchError(a.currency, b.currency);
  }
  return createMoney(a.amount + b.amount, a.currency);
}

function multiplyMoney(money: Money, factor: number): Money {
  return createMoney(money.amount * factor, money.currency);
}

const zero: Money = Object.freeze({ amount: 0, currency: "USD" });
```

### Using `as const` for Literal Types

```typescript
// as const makes values deeply readonly
const ORDER_STATUSES = ["draft", "submitted", "confirmed", "shipped"] as const;
type OrderStatus = (typeof ORDER_STATUSES)[number];

const DEFAULT_CONFIG = {
  maxRetries: 3,
  timeoutMs: 5000,
  baseUrl: "https://api.example.com",
} as const;
// DEFAULT_CONFIG.maxRetries = 10; // Compile error: Cannot assign to readonly property
```

### Immutable Domain Object with Object.freeze

```typescript
type Order = {
  readonly id: string;
  readonly items: readonly LineItem[];
  readonly status: OrderStatus;
};

function createOrder(id: string): Order {
  return Object.freeze({ id, items: Object.freeze([]), status: "draft" as const });
}

function addItem(order: Order, item: LineItem): Order {
  return Object.freeze({
    ...order,
    items: Object.freeze([...order.items, item]),
  });
}

function withStatus(order: Order, newStatus: OrderStatus): Order {
  return Object.freeze({ ...order, status: newStatus });
}

function totalOf(order: Order): Money {
  return order.items.reduce(
    (sum, item) => addMoney(sum, item.total),
    zero
  );
}
```

**Why compliant:** `readonly` properties prevent compile-time mutation. `Object.freeze()` prevents runtime mutation. `as const` infers the narrowest possible types and marks all properties as readonly. All operations return new objects instead of modifying existing ones.

---

## VIOLATION: Mutable Class with Settable Properties

```typescript
// BAD: Mutable class
class Money {
  // VIOLATION: Public mutable properties
  public amount: number;
  public currency: string;

  constructor(amount: number, currency: string) {
    this.amount = amount;
    this.currency = currency;
  }

  // VIOLATION: Mutates internal state
  add(other: Money): void {
    this.amount += other.amount;
  }
}

// Usage showing problems with mutability
const price = new Money(10, "USD");
const tax = new Money(1, "USD");
price.add(tax); // price is now mutated -- other references see the change
price.amount = -999; // No protection against invalid state

// BAD: Mutable order with exposed array
class Order {
  // VIOLATION: Mutable array
  public items: LineItem[] = [];
  public status: string = "draft";

  addItem(item: LineItem): void {
    this.items.push(item); // Mutating internal array
  }
}

const order = new Order();
order.items.push(hackedItem); // Bypasses addItem validation
order.items.length = 0; // Clears items without going through business logic
order.status = "anything"; // No type safety, no validation
```

**Why violates ENG-3.2:** Mutable classes with public properties allow unrestricted state changes. Array mutation (`.push()`, `.splice()`) modifies shared references. Without `readonly`, TypeScript cannot catch accidental mutations at compile time. Shared mutable state leads to subtle, hard-to-reproduce bugs.

---

## Quick Reference

| Pattern | Mutable (Avoid) | Immutable (Prefer) |
|---------|-----------------|---------------------|
| Object type | `class` with public properties | `type` with `readonly` properties |
| Array | `T[]` with `.push()` | `readonly T[]` with spread `[...arr, item]` |
| Constants | `const obj = { ... }` | `const obj = { ... } as const` |
| Runtime freeze | none | `Object.freeze()` |
| State change | `obj.prop = val` | `{ ...obj, prop: val }` (spread) |
