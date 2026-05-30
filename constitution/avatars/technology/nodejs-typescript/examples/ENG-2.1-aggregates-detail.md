---
law_id: ENG-2.1
avatar: nodejs-typescript
---

# ENG-2.1: DDD Aggregate Root Examples for Node.js TypeScript

## COMPLIANT: Order Aggregate Root with Proper Encapsulation

```typescript
// domain/aggregates/Order.ts
import { DomainEvent } from '../events/DomainEvent';

export type OrderStatus = 'draft' | 'submitted' | 'confirmed' | 'cancelled';

export interface LineItem {
  readonly productId: string;
  readonly quantity: number;
  readonly unitPrice: number;
}

export class Order {
  private readonly _items: LineItem[] = [];
  private readonly _events: DomainEvent[] = [];

  private constructor(
    readonly id: string,
    readonly customerId: string,
    private _status: OrderStatus,
    readonly createdAt: Date,
    items: LineItem[] = []
  ) {
    this._items = [...items];
  }

  static create(customerId: string): Order {
    const id = crypto.randomUUID();
    const order = new Order(id, customerId, 'draft', new Date());
    order._events.push({
      type: 'OrderCreated',
      aggregateId: id,
      payload: { customerId },
      occurredAt: new Date(),
    });
    return order;
  }

  static reconstitute(
    id: string,
    customerId: string,
    status: OrderStatus,
    createdAt: Date,
    items: LineItem[]
  ): Order {
    return new Order(id, customerId, status, createdAt, items);
  }

  get status(): OrderStatus {
    return this._status;
  }

  get items(): readonly LineItem[] {
    return Object.freeze([...this._items]);
  }

  get total(): number {
    return this._items.reduce(
      (sum, item) => sum + item.quantity * item.unitPrice,
      0
    );
  }

  addItem(productId: string, quantity: number, unitPrice: number): void {
    this.ensureCanModify();

    if (quantity <= 0) {
      throw new Error('Quantity must be positive');
    }
    if (unitPrice < 0) {
      throw new Error('Unit price cannot be negative');
    }

    const existingIndex = this._items.findIndex(i => i.productId === productId);
    if (existingIndex >= 0) {
      const existing = this._items[existingIndex];
      this._items[existingIndex] = {
        ...existing,
        quantity: existing.quantity + quantity,
      };
    } else {
      this._items.push(Object.freeze({ productId, quantity, unitPrice }));
    }
  }

  removeItem(productId: string): void {
    this.ensureCanModify();

    const index = this._items.findIndex(i => i.productId === productId);
    if (index < 0) {
      throw new Error(`Product ${productId} not found in order`);
    }
    this._items.splice(index, 1);
  }

  submit(): void {
    if (this._items.length === 0) {
      throw new Error('Cannot submit an empty order');
    }
    if (this._status !== 'draft') {
      throw new Error(`Cannot submit order in status: ${this._status}`);
    }

    this._status = 'submitted';
    this._events.push({
      type: 'OrderSubmitted',
      aggregateId: this.id,
      payload: {
        customerId: this.customerId,
        total: this.total,
        itemCount: this._items.length,
      },
      occurredAt: new Date(),
    });
  }

  confirm(): void {
    if (this._status !== 'submitted') {
      throw new Error('Only submitted orders can be confirmed');
    }
    this._status = 'confirmed';
  }

  cancel(reason: string): void {
    if (this._status === 'confirmed') {
      throw new Error('Cannot cancel a confirmed order');
    }
    if (this._status === 'cancelled') {
      throw new Error('Order is already cancelled');
    }

    this._status = 'cancelled';
    this._events.push({
      type: 'OrderCancelled',
      aggregateId: this.id,
      payload: { reason },
      occurredAt: new Date(),
    });
  }

  collectEvents(): DomainEvent[] {
    const events = [...this._events];
    this._events.length = 0;
    return events;
  }

  private ensureCanModify(): void {
    if (this._status !== 'draft') {
      throw new Error(`Cannot modify order in status: ${this._status}`);
    }
  }
}
```

```typescript
// domain/events/DomainEvent.ts
export interface DomainEvent {
  readonly type: string;
  readonly aggregateId: string;
  readonly payload: Record<string, unknown>;
  readonly occurredAt: Date;
}
```

**Why compliant:**
- Order is the aggregate root controlling all access to line items
- All mutations go through aggregate root methods that enforce invariants
- Items are returned as readonly frozen copies, preventing external mutation
- State transitions are validated (draft -> submitted -> confirmed)
- Domain events capture significant state changes
- Private constructor forces use of factory methods (`create`, `reconstitute`)

---

## COMPLIANT: Value Objects for Domain Concepts

```typescript
// domain/value-objects/Money.ts
export class Money {
  static readonly ZERO = new Money(0, 'USD');

  private constructor(
    readonly amount: number,
    readonly currency: string
  ) {
    if (!Number.isFinite(amount)) {
      throw new Error('Amount must be a finite number');
    }
    this.amount = Math.round(amount * 100) / 100;
  }

  static usd(amount: number): Money {
    return new Money(amount, 'USD');
  }

  static of(amount: number, currency: string): Money {
    return new Money(amount, currency);
  }

  add(other: Money): Money {
    this.validateSameCurrency(other);
    return new Money(this.amount + other.amount, this.currency);
  }

  subtract(other: Money): Money {
    this.validateSameCurrency(other);
    return new Money(this.amount - other.amount, this.currency);
  }

  multiply(factor: number): Money {
    return new Money(this.amount * factor, this.currency);
  }

  isGreaterThan(other: Money): boolean {
    this.validateSameCurrency(other);
    return this.amount > other.amount;
  }

  equals(other: Money): boolean {
    return this.amount === other.amount && this.currency === other.currency;
  }

  private validateSameCurrency(other: Money): void {
    if (this.currency !== other.currency) {
      throw new Error(`Cannot operate on ${this.currency} and ${other.currency}`);
    }
  }
}


// domain/value-objects/OrderId.ts
export class OrderId {
  private constructor(readonly value: string) {
    if (!value || value.trim().length === 0) {
      throw new Error('OrderId cannot be empty');
    }
  }

  static generate(): OrderId {
    return new OrderId(crypto.randomUUID());
  }

  static from(value: string): OrderId {
    return new OrderId(value);
  }

  equals(other: OrderId): boolean {
    return this.value === other.value;
  }

  toString(): string {
    return this.value;
  }
}
```

**Why compliant:** Value objects are immutable (all operations return new instances). They encapsulate validation and business logic. Typed IDs prevent mixing OrderId with CustomerId. Currency mismatches are caught at the domain level.

---

## VIOLATION: Anemic Domain Model with No Behavior

```typescript
// BAD: Entity is just a data container
interface Order {
  id: string;
  customerId: string;
  items: LineItem[];
  status: string;        // String instead of union type
  total: number;
  createdAt: Date;
}

interface LineItem {
  productId: string;
  quantity: number;
  unitPrice: number;
}

// BAD: All business logic in the service
class OrderService {
  constructor(
    private readonly db: Database,
    private readonly inventoryClient: InventoryClient
  ) {}

  async addItem(orderId: string, productId: string, quantity: number, price: number): Promise<void> {
    const order = await this.db.orders.findOne({ id: orderId });

    // Business logic scattered in service!
    if (order.status !== 'draft') {
      throw new Error('Cannot modify');
    }

    if (quantity <= 0) {
      throw new Error('Bad quantity');
    }

    // Directly mutating the entity!
    order.items.push({ productId, quantity, unitPrice: price });

    // Recalculating total in service!
    order.total = order.items.reduce(
      (sum: number, item: LineItem) => sum + item.quantity * item.unitPrice,
      0
    );

    await this.db.orders.updateOne({ id: orderId }, order);
  }

  async submitOrder(orderId: string): Promise<void> {
    const order = await this.db.orders.findOne({ id: orderId });

    // Validation in service instead of domain!
    if (order.items.length === 0) {
      throw new Error('Cannot submit empty order');
    }

    if (order.status !== 'draft') {
      throw new Error('Already submitted');
    }

    // Direct mutation of status!
    order.status = 'submitted';

    await this.db.orders.updateOne({ id: orderId }, order);
  }

  async cancelOrder(orderId: string, reason: string): Promise<void> {
    const order = await this.db.orders.findOne({ id: orderId });

    // More scattered validation
    if (order.status === 'confirmed') {
      throw new Error('Cannot cancel');
    }

    order.status = 'cancelled';
    await this.db.orders.updateOne({ id: orderId }, order);

    // No domain events, just direct side effects
    console.log(`Order ${orderId} cancelled: ${reason}`);
  }
}
```

**Why violates ENG-2.1:**
- Order is an anemic data container (plain interface with no behavior)
- All business rules are scattered in the service layer
- Items can be directly pushed onto the array, bypassing validation
- Status is a raw string with no type safety for valid transitions
- No encapsulation: any code with a reference can mutate order properties
- No domain events to capture what happened
- Total is manually recalculated in the service instead of being derived

---

## VIOLATION: Breaking Aggregate Boundaries

```typescript
// BAD: Accessing child entities directly
class LineItemRepository {
  constructor(private readonly db: Database) {}

  // Should not exist! LineItems should only be accessed through Order
  async findByProductId(productId: string): Promise<LineItem[]> {
    return this.db.lineItems.find({ productId });
  }

  // Modifying child entities outside the aggregate!
  async updateQuantity(lineItemId: string, newQuantity: number): Promise<void> {
    await this.db.lineItems.updateOne(
      { id: lineItemId },
      { quantity: newQuantity }
    );
    // Order.total is now stale! Invariant broken!
  }
}
```

**Why violates ENG-2.1:** Direct access to LineItems bypasses the Order aggregate. Modifying quantities without going through Order breaks the total invariant. The aggregate root loses control over consistency rules.

---

## Aggregate Boundaries

```typescript
// Order aggregate contains:
// - Order (root) - the only entry point
// - LineItem (entity within aggregate) - accessed only through Order
// - Money (value object) - immutable, shared safely

// Customer is a SEPARATE aggregate - referenced by ID only
class Order {
  readonly customerId: string;  // Reference by ID, not object
  // NOT: readonly customer: Customer;  // This would cross aggregate boundary
}
```

**Key principle:** Aggregates reference other aggregates by ID only. All mutations go through the aggregate root. Only the aggregate root has a repository.
