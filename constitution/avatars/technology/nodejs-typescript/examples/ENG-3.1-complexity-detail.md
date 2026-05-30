---
law_id: ENG-3.1
avatar: nodejs-typescript
---

# ENG-3.1: Complexity Management Examples for Node.js TypeScript

## COMPLIANT: Single Responsibility with Strategy Pattern

```typescript
// payment-strategy.interface.ts
export interface PaymentStrategy {
  process(request: PaymentRequest): Promise<PaymentResult>;
  supports(method: PaymentMethod): boolean;
}

// credit-card.strategy.ts
export class CreditCardPaymentStrategy implements PaymentStrategy {
  constructor(
    private readonly gateway: CreditCardGateway,
    private readonly fraudService: FraudDetectionService
  ) {}

  async process(request: PaymentRequest): Promise<PaymentResult> {
    await this.fraudService.validateTransaction(request);
    return this.gateway.charge(request.amount, request.cardDetails);
  }

  supports(method: PaymentMethod): boolean {
    return method === PaymentMethod.CreditCard;
  }
}

// paypal.strategy.ts
export class PayPalPaymentStrategy implements PaymentStrategy {
  constructor(private readonly client: PayPalClient) {}

  async process(request: PaymentRequest): Promise<PaymentResult> {
    return this.client.executePayment(request.paypalPaymentId);
  }

  supports(method: PaymentMethod): boolean {
    return method === PaymentMethod.PayPal;
  }
}

// payment.service.ts
export class PaymentService {
  constructor(
    private readonly strategies: PaymentStrategy[],
    private readonly repository: PaymentRepository,
    private readonly eventPublisher: EventPublisher
  ) {}

  async processPayment(request: PaymentRequest): Promise<PaymentResult> {
    const strategy = this.strategies.find(s => s.supports(request.paymentMethod));

    if (!strategy) {
      throw new UnsupportedPaymentMethodError(request.paymentMethod);
    }

    const result = await strategy.process(request);

    if (result.isSuccessful) {
      await this.repository.save(result.toEntity());
      await this.eventPublisher.publish(new PaymentCompletedEvent(result));
    }

    return result;
  }
}

// Dependency injection setup (e.g., with tsyringe or inversify)
container.register<PaymentStrategy[]>('PaymentStrategies', {
  useValue: [
    new CreditCardPaymentStrategy(container.resolve(CreditCardGateway), container.resolve(FraudDetectionService)),
    new PayPalPaymentStrategy(container.resolve(PayPalClient)),
  ],
});
```

**Why compliant:** Each class has a single responsibility. PaymentService orchestrates, strategies handle specific payment types. New payment methods require only adding a new strategy class - no modification to existing code (Open/Closed Principle). Cyclomatic complexity stays low in each component.

---

## COMPLIANT: Readable Function with Early Returns and Guard Clauses

```typescript
import { ValidationResult, ValidationError } from './validation';
import { Order, OrderItem } from './order';
import { InventoryService } from './inventory.service';

export class OrderValidationService {
  constructor(private readonly inventoryService: InventoryService) {}

  async validateOrder(order: Order | null | undefined): Promise<ValidationResult> {
    if (!order) {
      return ValidationResult.failure('Order cannot be null or undefined');
    }

    if (order.items.length === 0) {
      return ValidationResult.failure('Order must contain at least one item');
    }

    if (!order.customerId) {
      return ValidationResult.failure('Customer ID is required');
    }

    const itemValidation = this.validateItems(order.items);
    if (itemValidation.hasErrors) {
      return itemValidation;
    }

    const inventoryValidation = await this.validateInventory(order.items);
    if (inventoryValidation.hasErrors) {
      return inventoryValidation;
    }

    return ValidationResult.success();
  }

  private validateItems(items: readonly OrderItem[]): ValidationResult {
    const errors = items
      .filter(item => item.quantity <= 0)
      .map(item => `Invalid quantity for product: ${item.productId}`);

    return errors.length === 0
      ? ValidationResult.success()
      : ValidationResult.failure(errors);
  }

  private async validateInventory(items: readonly OrderItem[]): Promise<ValidationResult> {
    return this.inventoryService.checkAvailability(items);
  }
}
```

**Why compliant:** Early returns reduce nesting and make the validation flow clear. Each validation concern is separated into its own method. The main method reads like a checklist. Cyclomatic complexity is distributed across focused methods.

---

## VIOLATION: God Module with Mixed Responsibilities

```typescript
import { createConnection, Connection } from 'mysql2/promise';
import nodemailer from 'nodemailer';
import axios from 'axios';

// Everything in one file with mixed concerns
export class OrderManager {
  private connection: Connection | null = null;
  private transporter = nodemailer.createTransport({ host: 'smtp.example.com' });

  async createOrder(request: OrderRequest): Promise<Order> {
    // Validation logic mixed in
    if (!request.items || request.items.length === 0) {
      throw new Error('Items required');
    }
    for (const item of request.items) {
      if (item.quantity <= 0) {
        throw new Error('Invalid quantity');
      }
      if (item.price <= 0) {
        throw new Error('Invalid price');
      }
    }

    // Direct database access
    this.connection = await createConnection({
      host: process.env.DB_HOST,
      user: process.env.DB_USER,
      password: process.env.DB_PASSWORD,
      database: process.env.DB_NAME,
    });

    const orderId = crypto.randomUUID();

    await this.connection.execute(
      'INSERT INTO orders (id, customer_id, status, created_at) VALUES (?, ?, ?, ?)',
      [orderId, request.customerId, 'CREATED', new Date()]
    );

    for (const item of request.items) {
      await this.connection.execute(
        'INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)',
        [orderId, item.productId, item.quantity, item.price]
      );
    }

    // Inventory check via HTTP
    const productIds = request.items.map(i => i.productId).join(',');
    const { data: inventoryResponse } = await axios.get(
      `http://inventory-service/check?productIds=${productIds}`
    );

    if (!inventoryResponse.isAvailable) {
      // Manual rollback
      await this.connection.execute('DELETE FROM order_items WHERE order_id = ?', [orderId]);
      await this.connection.execute('DELETE FROM orders WHERE id = ?', [orderId]);
      throw new Error('Insufficient stock');
    }

    // Email sending logic
    try {
      await this.transporter.sendMail({
        from: 'orders@example.com',
        to: request.customerEmail,
        subject: `Order Confirmation #${orderId}`,
        html: this.buildEmailBody(request, orderId),
      });
    } catch {
      // Swallowed exception - order continues anyway
    }

    // Logging directly
    console.log(`Order created: ${orderId}`);

    // Building response with inline calculation
    const total = request.items.reduce((sum, i) => sum + i.price * i.quantity, 0);
    const tax = total * 0.08;
    const shipping = total > 50 ? 0 : 5.99;

    return { orderId, customerId: request.customerId, total: total + tax + shipping };
  }

  private buildEmailBody(request: OrderRequest, orderId: string): string {
    // 200+ lines of HTML template building...
    return '<html>...</html>';
  }

  // 30+ more methods covering reporting, analytics, refunds, etc.
}
```

**Why violates ENG-3.1:** This class handles validation, persistence, HTTP calls, email sending, logging, and price calculation. It directly manages database connections and external services. Changes to email templates require modifying this class. Testing requires mocking many external services. The createOrder method alone has cyclomatic complexity > 15.

---

## VIOLATION: Deeply Nested Conditionals

```typescript
export function calculateShipping(request: ShippingRequest | null): ShippingQuote {
  let cost = 0;

  if (request !== null) {
    if (request.destination !== null) {
      if (request.destination.country !== null) {
        if (request.destination.country === 'US') {
          if (request.weight !== null) {
            if (request.weight <= 1.0) {
              if (request.isExpedited) {
                cost = 12.99;
              } else {
                if (request.destination.isRural) {
                  cost = 7.99;
                } else {
                  cost = 5.99;
                }
              }
            } else if (request.weight <= 5.0) {
              if (request.isExpedited) {
                cost = 24.99;
              } else {
                if (request.destination.isRural) {
                  cost = 14.99;
                } else {
                  cost = 9.99;
                }
              }
            } else {
              // Even more nesting for heavy packages...
            }
          }
        } else if (request.destination.country === 'CA') {
          // Similar deep nesting for Canada...
        } else {
          // International shipping nesting...
        }
      }
    }
  }

  return { cost };
}
```

**Why violates ENG-3.1:** Seven levels of nesting make this nearly impossible to understand or maintain. The cyclomatic complexity exceeds 20. Adding a new country or weight tier requires navigating the maze. This should be decomposed using lookup tables, strategy pattern, or a configuration object.

---

## COMPLIANT: Decomposed Shipping with Lookup Tables

```typescript
// shipping-calculator.ts
export class ShippingCalculator {
  constructor(
    private readonly rateRepository: ShippingRateRepository,
    private readonly zoneResolver: ShippingZoneResolver
  ) {}

  async calculateShipping(request: ShippingRequest): Promise<ShippingQuote> {
    this.validateRequest(request);

    const zone = this.zoneResolver.resolveZone(request.destination);
    const weightTier = WeightTier.fromWeight(request.weight);
    const serviceLevel = request.isExpedited ? ServiceLevel.Express : ServiceLevel.Standard;

    const rate = await this.rateRepository.findRate(zone, weightTier, serviceLevel);

    if (!rate) {
      throw new ShippingNotAvailableError(zone, weightTier);
    }

    return {
      baseCost: rate.baseCost,
      ruralSurcharge: this.calculateRuralSurcharge(request.destination, rate),
      estimatedDays: rate.estimatedDays,
    };
  }

  private validateRequest(request: ShippingRequest): void {
    if (!request) {
      throw new Error('Shipping request is required');
    }
    if (!request.destination) {
      throw new Error('Destination is required');
    }
    if (request.weight == null) {
      throw new Error('Weight is required');
    }
  }

  private calculateRuralSurcharge(destination: Address, rate: ShippingRate): number {
    return destination.isRural ? rate.ruralSurcharge : 0;
  }
}

// weight-tier.ts
export enum WeightTier {
  Light = 'LIGHT',
  Medium = 'MEDIUM',
  Heavy = 'HEAVY',
  Freight = 'FREIGHT',
}

const WEIGHT_TIERS: Array<{ min: number; max: number; tier: WeightTier }> = [
  { min: 0, max: 1.0, tier: WeightTier.Light },
  { min: 1.0, max: 5.0, tier: WeightTier.Medium },
  { min: 5.0, max: 20.0, tier: WeightTier.Heavy },
  { min: 20.0, max: Infinity, tier: WeightTier.Freight },
];

export namespace WeightTier {
  export function fromWeight(weight: number): WeightTier {
    const tier = WEIGHT_TIERS.find(t => weight > t.min && weight <= t.max);
    return tier?.tier ?? WeightTier.Freight;
  }
}
```

**Why compliant:** Logic is flat with minimal nesting. Rates are stored in a repository rather than hardcoded conditionals. Weight tier logic is encapsulated in a lookup table. Each function has a single responsibility and low cyclomatic complexity. Adding new zones or tiers requires only database entries, not code changes.

---

## COMPLIANT: Using TypeScript Interfaces and Types for Clean Contracts

```typescript
// order-summary.ts
export interface OrderSummary {
  readonly orderId: string;
  readonly customerName: string;
  readonly items: readonly LineItemSummary[];
  readonly subtotal: Money;
  readonly tax: Money;
  readonly total: Money;
  readonly status: OrderStatus;
  readonly createdAt: Date;
}

export interface LineItemSummary {
  readonly productName: string;
  readonly quantity: number;
  readonly unitPrice: Money;
  readonly lineTotal: Money;
}

export function createOrderSummary(
  order: Order,
  taxCalculator: TaxCalculator
): OrderSummary {
  const subtotal = order.calculateSubtotal();
  const tax = taxCalculator.calculate(subtotal, order.shippingAddress);

  return Object.freeze({
    orderId: order.id,
    customerName: order.customer.fullName,
    items: order.items.map(createLineItemSummary),
    subtotal,
    tax,
    total: Money.add(subtotal, tax),
    status: order.status,
    createdAt: order.createdAt,
  });
}

function createLineItemSummary(item: OrderItem): LineItemSummary {
  return Object.freeze({
    productName: item.product.name,
    quantity: item.quantity,
    unitPrice: item.unitPrice,
    lineTotal: item.calculateLineTotal(),
  });
}

// money.ts
export interface Money {
  readonly amount: number;
  readonly currency: string;
}

export namespace Money {
  export const ZERO: Money = Object.freeze({ amount: 0, currency: 'USD' });

  export function usd(amount: number): Money {
    return Object.freeze({
      amount: Math.round(amount * 100) / 100,
      currency: 'USD',
    });
  }

  export function add(left: Money, right: Money): Money {
    validateSameCurrency(left, right);
    return Object.freeze({
      amount: left.amount + right.amount,
      currency: left.currency,
    });
  }

  export function subtract(left: Money, right: Money): Money {
    validateSameCurrency(left, right);
    return Object.freeze({
      amount: left.amount - right.amount,
      currency: left.currency,
    });
  }

  export function multiply(money: Money, multiplier: number): Money {
    return Object.freeze({
      amount: Math.round(money.amount * multiplier * 100) / 100,
      currency: money.currency,
    });
  }

  function validateSameCurrency(left: Money, right: Money): void {
    if (left.currency !== right.currency) {
      throw new Error(
        `Cannot operate on different currencies: ${left.currency} vs ${right.currency}`
      );
    }
  }
}
```

**Why compliant:** Interfaces define clear contracts. Object.freeze ensures immutability at runtime. Factory functions encapsulate construction logic. Each module has a focused purpose. The namespace pattern groups related functions without class overhead.

---

## COMPLIANT: Functional Composition with Pipes

```typescript
import { pipe } from 'fp-ts/function';
import * as E from 'fp-ts/Either';
import * as TE from 'fp-ts/TaskEither';

// Pure validation functions
const validateNotEmpty = (items: OrderItem[]): E.Either<ValidationError, OrderItem[]> =>
  items.length > 0
    ? E.right(items)
    : E.left(new ValidationError('Order must contain at least one item'));

const validateQuantities = (items: OrderItem[]): E.Either<ValidationError, OrderItem[]> => {
  const invalidItems = items.filter(item => item.quantity <= 0);
  return invalidItems.length === 0
    ? E.right(items)
    : E.left(new ValidationError(`Invalid quantities for: ${invalidItems.map(i => i.productId).join(', ')}`));
};

const validatePrices = (items: OrderItem[]): E.Either<ValidationError, OrderItem[]> => {
  const invalidItems = items.filter(item => item.unitPrice.amount <= 0);
  return invalidItems.length === 0
    ? E.right(items)
    : E.left(new ValidationError(`Invalid prices for: ${invalidItems.map(i => i.productId).join(', ')}`));
};

// Compose validations
export const validateOrderItems = (items: OrderItem[]): E.Either<ValidationError, OrderItem[]> =>
  pipe(
    items,
    E.right,
    E.chain(validateNotEmpty),
    E.chain(validateQuantities),
    E.chain(validatePrices)
  );

// Async validation with external service
const checkInventory = (inventoryService: InventoryService) =>
  (items: OrderItem[]): TE.TaskEither<ValidationError, OrderItem[]> =>
    pipe(
      TE.tryCatch(
        () => inventoryService.checkAvailability(items),
        (error) => new ValidationError(`Inventory check failed: ${error}`)
      ),
      TE.chain(available =>
        available
          ? TE.right(items)
          : TE.left(new ValidationError('Insufficient inventory'))
      )
    );

// Full validation pipeline
export const validateOrder = (
  inventoryService: InventoryService
) => (order: Order): TE.TaskEither<ValidationError, Order> =>
  pipe(
    validateOrderItems(order.items),
    TE.fromEither,
    TE.chain(checkInventory(inventoryService)),
    TE.map(() => order)
  );
```

**Why compliant:** Each validation is a small, pure function. Composition is explicit through pipe. Error handling is built into the types (Either/TaskEither). Adding new validations is just adding to the pipeline. Testing individual validators is trivial.

---

## COMPLIANT: Module Pattern for Encapsulation

```typescript
// order-calculator.module.ts
interface DiscountConfig {
  readonly tiers: ReadonlyArray<{
    readonly minQuantity: number;
    readonly discountPercent: number;
  }>;
  readonly maxDiscountPercent: number;
}

interface TaxConfig {
  readonly defaultRate: number;
  readonly ratesByState: Readonly<Record<string, number>>;
}

export function createOrderCalculator(config: {
  discount: DiscountConfig;
  tax: TaxConfig;
}) {
  // Private helper functions
  const getDiscountPercent = (quantity: number): number => {
    const tier = [...config.discount.tiers]
      .sort((a, b) => b.minQuantity - a.minQuantity)
      .find(t => quantity >= t.minQuantity);

    const discount = tier?.discountPercent ?? 0;
    return Math.min(discount, config.discount.maxDiscountPercent);
  };

  const getTaxRate = (state: string): number => {
    return config.tax.ratesByState[state] ?? config.tax.defaultRate;
  };

  // Public API
  return {
    calculateSubtotal(items: readonly OrderItem[]): Money {
      return items.reduce(
        (total, item) => Money.add(total, this.calculateLineTotal(item)),
        Money.ZERO
      );
    },

    calculateLineTotal(item: OrderItem): Money {
      const discountPercent = getDiscountPercent(item.quantity);
      const grossTotal = Money.multiply(item.unitPrice, item.quantity);
      const discountAmount = Money.multiply(grossTotal, discountPercent / 100);
      return Money.subtract(grossTotal, discountAmount);
    },

    calculateTax(subtotal: Money, shippingState: string): Money {
      const rate = getTaxRate(shippingState);
      return Money.multiply(subtotal, rate);
    },

    calculateTotal(items: readonly OrderItem[], shippingState: string): Money {
      const subtotal = this.calculateSubtotal(items);
      const tax = this.calculateTax(subtotal, shippingState);
      return Money.add(subtotal, tax);
    },
  };
}

// Usage
const calculator = createOrderCalculator({
  discount: {
    tiers: [
      { minQuantity: 10, discountPercent: 5 },
      { minQuantity: 50, discountPercent: 10 },
      { minQuantity: 100, discountPercent: 15 },
    ],
    maxDiscountPercent: 20,
  },
  tax: {
    defaultRate: 0.08,
    ratesByState: {
      CA: 0.0725,
      NY: 0.08,
      TX: 0.0625,
    },
  },
});
```

**Why compliant:** Configuration is injected, making the calculator testable and reusable. Private helpers are truly private (closure scope). The public API is minimal and focused. Business rules (discount tiers, tax rates) are externalized as configuration.
