# Node.js/TypeScript Guidance

> **Purpose:** Stack-specific agent behaviors for Node.js/TypeScript backend applications.

---

## Overview

This guidance provides patterns for AI agents working with Node.js and TypeScript backend applications. It covers testing with Jest/Vitest, Express/Fastify patterns, and domain modeling in TypeScript.

---

## Testing Framework

**Primary Framework:** Vitest (or Jest) + Supertest

### Test Structure

```typescript
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { Order, OrderLine } from './order';
import { Money, CustomerId, ProductId } from './value-objects';

describe('Order', () => {
  describe('create', () => {
    it('should create order with zero total', () => {
      // Arrange
      const customerId = CustomerId.from('cust-123');

      // Act
      const order = Order.create(customerId);

      // Assert
      expect(order.total).toEqual(Money.zero());
      expect(order.status).toBe('draft');
    });
  });

  describe('addItem', () => {
    it('should update total when adding item', () => {
      // Arrange
      const order = Order.create(CustomerId.from('cust-123'));
      const productId = ProductId.from('prod-1');

      // Act
      order.addItem(productId, Money.from(100), 2);

      // Assert
      expect(order.total).toEqual(Money.from(200));
      expect(order.lines).toHaveLength(1);
    });

    it('should throw when order is not draft', () => {
      // Arrange
      const order = Order.create(CustomerId.from('cust-123'));
      order.addItem(ProductId.from('prod-1'), Money.from(100), 1);
      order.place();

      // Act & Assert
      expect(() => {
        order.addItem(ProductId.from('prod-2'), Money.from(50), 1);
      }).toThrow('Order is not modifiable');
    });
  });
});
```

### Integration Test with Supertest

```typescript
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import request from 'supertest';
import { app } from '../app';
import { setupTestDatabase, teardownTestDatabase } from './helpers';

describe('Orders API', () => {
  beforeAll(async () => {
    await setupTestDatabase();
  });

  afterAll(async () => {
    await teardownTestDatabase();
  });

  describe('POST /orders', () => {
    it('should create a new order', async () => {
      // Act
      const response = await request(app)
        .post('/orders')
        .send({ customerId: 'cust-123' })
        .expect(201);

      // Assert
      expect(response.body).toMatchObject({
        id: expect.any(String),
        customerId: 'cust-123',
        status: 'draft',
      });
    });
  });
});
```

---

## Domain Modeling

### Entity Pattern

```typescript
import { v4 as uuid } from 'uuid';
import { OrderId, CustomerId, ProductId, Money } from './value-objects';
import { DomainEvent, OrderPlaced, ItemAddedToOrder } from './events';

export type OrderStatus = 'draft' | 'placed' | 'shipped' | 'delivered';

export class Order {
  private readonly _id: OrderId;
  private readonly _customerId: CustomerId;
  private readonly _lines: OrderLine[] = [];
  private _status: OrderStatus = 'draft';
  private readonly _events: DomainEvent[] = [];

  private constructor(id: OrderId, customerId: CustomerId) {
    this._id = id;
    this._customerId = customerId;
  }

  static create(customerId: CustomerId): Order {
    return new Order(OrderId.from(uuid()), customerId);
  }

  get id(): OrderId {
    return this._id;
  }

  get customerId(): CustomerId {
    return this._customerId;
  }

  get lines(): readonly OrderLine[] {
    return [...this._lines];
  }

  get status(): OrderStatus {
    return this._status;
  }

  get total(): Money {
    return this._lines.reduce(
      (sum, line) => sum.add(line.total),
      Money.zero()
    );
  }

  get domainEvents(): readonly DomainEvent[] {
    return [...this._events];
  }

  addItem(productId: ProductId, price: Money, quantity: number): void {
    this.ensureModifiable();

    const existingLine = this._lines.find((l) => l.productId.equals(productId));
    if (existingLine) {
      existingLine.increaseQuantity(quantity);
    } else {
      this._lines.push(new OrderLine(productId, price, quantity));
    }

    this._events.push(new ItemAddedToOrder(this._id, productId, quantity));
  }

  place(): void {
    if (this._lines.length === 0) {
      throw new Error('Cannot place empty order');
    }

    this._status = 'placed';
    this._events.push(new OrderPlaced(this._id, this.total));
  }

  clearEvents(): void {
    this._events.length = 0;
  }

  private ensureModifiable(): void {
    if (this._status !== 'draft') {
      throw new Error('Order is not modifiable');
    }
  }
}
```

### Value Object Pattern

```typescript
export class Money {
  private constructor(
    public readonly amount: number,
    public readonly currency: string
  ) {
    if (amount < 0) {
      throw new Error('Amount cannot be negative');
    }
  }

  static from(amount: number, currency = 'USD'): Money {
    return new Money(amount, currency);
  }

  static zero(currency = 'USD'): Money {
    return new Money(0, currency);
  }

  add(other: Money): Money {
    this.ensureSameCurrency(other);
    return new Money(this.amount + other.amount, this.currency);
  }

  multiply(factor: number): Money {
    return new Money(this.amount * factor, this.currency);
  }

  equals(other: Money): boolean {
    return this.amount === other.amount && this.currency === other.currency;
  }

  private ensureSameCurrency(other: Money): void {
    if (this.currency !== other.currency) {
      throw new Error(`Currency mismatch: ${this.currency} vs ${other.currency}`);
    }
  }
}

export class OrderId {
  private constructor(public readonly value: string) {}

  static from(value: string): OrderId {
    if (!value || value.trim() === '') {
      throw new Error('OrderId cannot be empty');
    }
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

---

## Common Patterns

### Repository Pattern

```typescript
export interface OrderRepository {
  findById(id: OrderId): Promise<Order | null>;
  findByCustomer(customerId: CustomerId): Promise<Order[]>;
  save(order: Order): Promise<void>;
}

export class PostgresOrderRepository implements OrderRepository {
  constructor(private readonly db: Database) {}

  async findById(id: OrderId): Promise<Order | null> {
    const row = await this.db.query(
      'SELECT * FROM orders WHERE id = $1',
      [id.value]
    );
    return row ? this.toDomain(row) : null;
  }

  async save(order: Order): Promise<void> {
    await this.db.transaction(async (tx) => {
      await tx.query(
        `INSERT INTO orders (id, customer_id, status)
         VALUES ($1, $2, $3)
         ON CONFLICT (id) DO UPDATE SET status = $3`,
        [order.id.value, order.customerId.value, order.status]
      );
      // Save lines...
    });
  }

  private toDomain(row: any): Order {
    // Reconstitute domain object from database row
  }
}
```

### Service Layer

```typescript
export class OrderService {
  constructor(
    private readonly orderRepository: OrderRepository,
    private readonly eventPublisher: EventPublisher
  ) {}

  async placeOrder(orderId: string): Promise<Order> {
    const order = await this.orderRepository.findById(OrderId.from(orderId));
    if (!order) {
      throw new OrderNotFoundError(orderId);
    }

    order.place();

    await this.orderRepository.save(order);

    // Publish domain events
    for (const event of order.domainEvents) {
      await this.eventPublisher.publish(event);
    }
    order.clearEvents();

    return order;
  }
}
```

### Express Router with Dependency Injection

```typescript
import { Router } from 'express';
import { OrderService } from '../application/order-service';

export function createOrdersRouter(orderService: OrderService): Router {
  const router = Router();

  router.post('/', async (req, res, next) => {
    try {
      const order = await orderService.createOrder(req.body.customerId);
      res.status(201).json(toResponse(order));
    } catch (error) {
      next(error);
    }
  });

  router.post('/:id/place', async (req, res, next) => {
    try {
      const order = await orderService.placeOrder(req.params.id);
      res.json(toResponse(order));
    } catch (error) {
      next(error);
    }
  });

  return router;
}
```

---

## Anti-Patterns to Avoid

### Business Logic in Routes

```typescript
// BAD - Logic in route handler
router.post('/:id/discount', async (req, res) => {
  const order = await orderRepository.findById(req.params.id);

  // Business logic in route!
  const discount = req.body.percentage / 100;
  const newTotal = order.total * (1 - discount);
  order.total = newTotal;

  await orderRepository.save(order);
  res.json(order);
});
```

### Mutable Value Objects

```typescript
// BAD - Value object should be immutable
class Money {
  amount: number;
  currency: string;

  add(other: Money): void {
    this.amount += other.amount; // Mutation!
  }
}
```

### Any Types

```typescript
// BAD - Losing type safety
function processOrder(order: any) {
  return order.total * 1.1; // No type checking
}

// GOOD - Explicit types
function processOrder(order: Order): Money {
  return order.total.multiply(1.1);
}
```

---

## Node.js Specific Guidance

### Error Handling

```typescript
// Custom error classes
export class DomainError extends Error {
  constructor(message: string) {
    super(message);
    this.name = this.constructor.name;
  }
}

export class OrderNotFoundError extends DomainError {
  constructor(public readonly orderId: string) {
    super(`Order ${orderId} not found`);
  }
}

// Error handling middleware
export function errorHandler(
  err: Error,
  req: Request,
  res: Response,
  next: NextFunction
): void {
  if (err instanceof OrderNotFoundError) {
    res.status(404).json({
      error: 'ORDER_NOT_FOUND',
      message: err.message,
    });
    return;
  }

  console.error('Unhandled error:', err);
  res.status(500).json({
    error: 'INTERNAL_ERROR',
    message: 'An unexpected error occurred',
  });
}
```

### Async/Await Patterns

```typescript
// Always handle promise rejections
router.get('/:id', async (req, res, next) => {
  try {
    const order = await orderService.getOrder(req.params.id);
    res.json(order);
  } catch (error) {
    next(error); // Forward to error handler
  }
});

// Or use a wrapper
const asyncHandler = (fn: RequestHandler): RequestHandler => {
  return (req, res, next) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
};

router.get('/:id', asyncHandler(async (req, res) => {
  const order = await orderService.getOrder(req.params.id);
  res.json(order);
}));
```

### Configuration

```typescript
// config.ts
import { z } from 'zod';

const configSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
  PORT: z.coerce.number().default(3000),
  DATABASE_URL: z.string().url(),
  LOG_LEVEL: z.enum(['debug', 'info', 'warn', 'error']).default('info'),
});

export const config = configSchema.parse(process.env);
```

---

## Tools and Commands

### Development

```bash
# Start development server (with ts-node-dev or tsx)
npm run dev

# Build TypeScript
npm run build

# Start production
npm start

# Type check without building
npm run typecheck
```

### Testing

```bash
# Run tests
npm test

# Watch mode
npm test -- --watch

# Coverage
npm test -- --coverage

# Run specific file
npm test -- order.test.ts
```

### Code Quality

```bash
# ESLint
npm run lint
npm run lint -- --fix

# Prettier
npm run format

# Type check
npm run typecheck

# All checks
npm run lint && npm run typecheck && npm test
```
