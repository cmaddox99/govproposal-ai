---
law_id: ENG-2.2
avatar: nodejs-typescript
---

# ENG-2.2: Layered Architecture Examples for Node.js TypeScript

## COMPLIANT: Clean Route Handler-Service-Repository Separation

```typescript
// === PRESENTATION LAYER: Route handlers handle HTTP only ===

// api/routes/orders.ts
import { Router, Request, Response, NextFunction } from 'express';
import { OrderApplicationService } from '../../application/order.service';
import { CreateOrderSchema, SubmitOrderSchema } from '../schemas/order.schemas';
import { validateRequest } from '../middleware/validation';

export function createOrderRouter(orderService: OrderApplicationService): Router {
  const router = Router();

  router.post(
    '/',
    validateRequest(CreateOrderSchema),
    async (req: Request, res: Response, next: NextFunction) => {
      try {
        const order = await orderService.createOrder({
          customerId: req.body.customerId,
          items: req.body.items,
        });
        res.status(201).json(toOrderResponse(order));
      } catch (error) {
        next(error);
      }
    }
  );

  router.get(
    '/:id',
    async (req: Request, res: Response, next: NextFunction) => {
      try {
        const order = await orderService.findById(req.params.id);
        if (!order) {
          res.status(404).json({ error: 'Order not found' });
          return;
        }
        res.json(toOrderResponse(order));
      } catch (error) {
        next(error);
      }
    }
  );

  router.put(
    '/:id/submit',
    async (req: Request, res: Response, next: NextFunction) => {
      try {
        const order = await orderService.submitOrder(req.params.id);
        res.json(toOrderResponse(order));
      } catch (error) {
        next(error);
      }
    }
  );

  return router;
}

// api/mappers/order.mapper.ts
function toOrderResponse(order: Order): OrderResponse {
  return {
    id: order.id,
    customerId: order.customerId,
    status: order.status,
    items: order.items.map(item => ({
      productId: item.productId,
      quantity: item.quantity,
      unitPrice: item.unitPrice,
    })),
    total: order.total,
    createdAt: order.createdAt.toISOString(),
  };
}


// === APPLICATION LAYER: Services orchestrate use cases ===

// application/order.service.ts
import { Order } from '../domain/aggregates/Order';
import { OrderRepository } from '../domain/ports/order.repository';
import { InventoryClient } from '../domain/ports/inventory.client';
import { EventPublisher } from '../domain/ports/event.publisher';

export class OrderApplicationService {
  constructor(
    private readonly repository: OrderRepository,
    private readonly inventoryClient: InventoryClient,
    private readonly eventPublisher: EventPublisher
  ) {}

  async createOrder(command: CreateOrderCommand): Promise<Order> {
    const order = Order.create(command.customerId);

    for (const item of command.items) {
      order.addItem(item.productId, item.quantity, item.unitPrice);
    }

    await this.repository.save(order);
    await this.eventPublisher.publishAll(order.collectEvents());

    return order;
  }

  async submitOrder(orderId: string): Promise<Order> {
    const order = await this.repository.findById(orderId);
    if (!order) {
      throw new OrderNotFoundError(orderId);
    }

    order.submit();

    await this.inventoryClient.reserveStock(order.items);
    await this.repository.save(order);
    await this.eventPublisher.publishAll(order.collectEvents());

    return order;
  }

  async findById(orderId: string): Promise<Order | null> {
    return this.repository.findById(orderId);
  }
}


// === DOMAIN LAYER: Entities and interfaces, no external dependencies ===

// domain/aggregates/Order.ts
export class Order {
  // ... aggregate root with business rules (see ENG-2.1 examples)
  static create(customerId: string): Order { /* ... */ }
  addItem(productId: string, quantity: number, unitPrice: number): void { /* ... */ }
  submit(): void { /* ... */ }
}

// domain/ports/order.repository.ts (interface only - no implementation)
export interface OrderRepository {
  findById(id: string): Promise<Order | null>;
  save(order: Order): Promise<void>;
}

// domain/ports/inventory.client.ts (interface only)
export interface InventoryClient {
  reserveStock(items: readonly LineItem[]): Promise<void>;
}

// domain/ports/event.publisher.ts (interface only)
export interface EventPublisher {
  publishAll(events: DomainEvent[]): Promise<void>;
}


// === INFRASTRUCTURE LAYER: Implements domain ports ===

// infrastructure/persistence/mongo-order.repository.ts
import { Collection, Document } from 'mongodb';
import { Order } from '../../domain/aggregates/Order';
import { OrderRepository } from '../../domain/ports/order.repository';

export class MongoOrderRepository implements OrderRepository {
  constructor(private readonly collection: Collection<Document>) {}

  async findById(id: string): Promise<Order | null> {
    const doc = await this.collection.findOne({ _id: id });
    return doc ? this.toDomain(doc) : null;
  }

  async save(order: Order): Promise<void> {
    const doc = this.toDocument(order);
    await this.collection.replaceOne(
      { _id: order.id },
      doc,
      { upsert: true }
    );
  }

  private toDomain(doc: Document): Order {
    return Order.reconstitute(
      doc._id,
      doc.customerId,
      doc.status,
      new Date(doc.createdAt),
      doc.items
    );
  }

  private toDocument(order: Order): Document {
    return {
      _id: order.id,
      customerId: order.customerId,
      status: order.status,
      items: [...order.items],
      createdAt: order.createdAt,
    };
  }
}

// infrastructure/messaging/kafka-event.publisher.ts
import { Kafka, Producer } from 'kafkajs';
import { DomainEvent } from '../../domain/events/DomainEvent';
import { EventPublisher } from '../../domain/ports/event.publisher';

export class KafkaEventPublisher implements EventPublisher {
  private readonly producer: Producer;

  constructor(kafka: Kafka) {
    this.producer = kafka.producer();
  }

  async publishAll(events: DomainEvent[]): Promise<void> {
    const messages = events.map(event => ({
      key: event.aggregateId,
      value: JSON.stringify(event),
    }));

    await this.producer.send({
      topic: 'order-events',
      messages,
    });
  }
}
```

**Why compliant:**
- Route handlers handle only HTTP concerns (request parsing, response formatting, status codes)
- Application service orchestrates the use case without business logic
- Domain model defines entities with behavior and interfaces (ports) for infrastructure
- Infrastructure implements domain ports with specific technologies (MongoDB, Kafka)
- Dependencies point inward: Infrastructure -> Application -> Domain

---

## VIOLATION: Business Logic in Route Handlers

```typescript
// BAD: Route handler doing everything
import express from 'express';
import { MongoClient } from 'mongodb';
import nodemailer from 'nodemailer';

const app = express();
const client = new MongoClient(process.env.MONGO_URL!);
const db = client.db('orders');

app.post('/api/orders', async (req, res) => {
  // Validation mixed into handler
  if (!req.body.customerId) {
    return res.status(400).json({ error: 'Customer ID required' });
  }
  if (!req.body.items || req.body.items.length === 0) {
    return res.status(400).json({ error: 'Items required' });
  }

  const orderId = crypto.randomUUID();

  // Business logic in route handler!
  let total = 0;
  for (const item of req.body.items) {
    if (item.quantity <= 0) {
      return res.status(400).json({ error: 'Invalid quantity' });
    }

    // Pricing logic in handler!
    let price = item.unitPrice;
    if (item.quantity > 10) {
      price *= 0.9;  // Volume discount
    }
    total += price * item.quantity;
  }

  // Direct database access in handler!
  await db.collection('orders').insertOne({
    _id: orderId,
    customerId: req.body.customerId,
    items: req.body.items,
    status: 'draft',
    total,
    createdAt: new Date(),
  });

  // Email notification in handler!
  const transporter = nodemailer.createTransport({ host: 'smtp.example.com' });
  await transporter.sendMail({
    to: req.body.email,
    subject: `Order ${orderId} Created`,
    text: `Your order total is $${total}`,
  });

  res.status(201).json({ orderId, total });
});

app.put('/api/orders/:id/submit', async (req, res) => {
  const order = await db.collection('orders').findOne({ _id: req.params.id });

  if (!order) {
    return res.status(404).json({ error: 'Not found' });
  }

  // Business validation in handler!
  if (order.status !== 'draft') {
    return res.status(400).json({ error: 'Already submitted' });
  }
  if (order.items.length === 0) {
    return res.status(400).json({ error: 'Empty order' });
  }

  // Direct database mutation!
  await db.collection('orders').updateOne(
    { _id: req.params.id },
    { $set: { status: 'submitted' } }
  );

  // Inline HTTP call to inventory service!
  await fetch(`http://inventory-service/reserve`, {
    method: 'POST',
    body: JSON.stringify({ items: order.items }),
  });

  res.json({ message: 'Submitted' });
});
```

**Why violates ENG-2.2:**
- Route handlers contain business rules (discount calculation, status validation)
- Direct MongoDB access in the presentation layer with no repository abstraction
- Email sending and HTTP calls mixed into request handling
- No domain model; data is untyped objects from the database
- Business logic cannot be reused outside of HTTP context (e.g., message consumer)
- Testing requires mocking MongoDB, SMTP, and HTTP in every route test

---

## Layer Responsibilities

| Layer | Responsibility | Node.js TypeScript Artifacts |
|-------|----------------|-------------------------------|
| **Presentation (API)** | HTTP routing, validation, serialization | Express routers, Zod schemas, middleware |
| **Application** | Use case orchestration, transactions | Service classes, command/query objects |
| **Domain** | Business rules, entities, interfaces | Aggregate classes, value objects, port interfaces |
| **Infrastructure** | Database, messaging, external APIs | Repository implementations, HTTP/Kafka clients |

---

## Dependency Injection Wiring

```typescript
// composition-root.ts - Wire everything together at startup
import { MongoClient } from 'mongodb';
import { Kafka } from 'kafkajs';
import { MongoOrderRepository } from './infrastructure/persistence/mongo-order.repository';
import { KafkaEventPublisher } from './infrastructure/messaging/kafka-event.publisher';
import { HttpInventoryClient } from './infrastructure/http/inventory.client';
import { OrderApplicationService } from './application/order.service';
import { createOrderRouter } from './api/routes/orders';

export async function createApp() {
  const mongo = await MongoClient.connect(process.env.MONGO_URL!);
  const kafka = new Kafka({ brokers: [process.env.KAFKA_BROKER!] });

  const orderRepository = new MongoOrderRepository(mongo.db().collection('orders'));
  const eventPublisher = new KafkaEventPublisher(kafka);
  const inventoryClient = new HttpInventoryClient(process.env.INVENTORY_URL!);

  const orderService = new OrderApplicationService(
    orderRepository,
    inventoryClient,
    eventPublisher
  );

  const app = express();
  app.use('/api/orders', createOrderRouter(orderService));

  return app;
}
```

**Key principle:** Domain defines interfaces (ports), infrastructure provides implementations (adapters), and the composition root wires them together. No layer directly depends on a layer it should not know about.
