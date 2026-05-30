---
law_id: ENG-3.5
avatar: nodejs-typescript
---

# ENG-3.5: Naming Conventions for Node.js TypeScript

## Naming Convention Reference

| Element          | Convention            | Example                               |
|------------------|-----------------------|---------------------------------------|
| Classes          | PascalCase            | `OrderService`, `CargoManifest`       |
| Interfaces       | PascalCase            | `OrderRepository`, `ShippingRate`     |
| Types            | PascalCase            | `OrderStatus`, `PaymentResult`        |
| Functions        | camelCase             | `calculateTotal`, `validateEmail`     |
| Variables        | camelCase             | `customerCount`, `orderItems`         |
| Constants        | SCREAMING_SNAKE_CASE  | `MAX_RETRY_COUNT`, `DEFAULT_TIMEOUT`  |
| Enums            | PascalCase (values PascalCase) | `OrderStatus.Confirmed`     |
| Files            | kebab-case            | `order-service.ts`, `cargo-manifest.ts` |
| Directories      | kebab-case            | `order-processing/`, `shared-utils/`  |
| Boolean vars     | is/has/should prefix  | `isValid`, `hasPermission`            |

---

## COMPLIANT: Idiomatic TypeScript Naming

```typescript
// File: order-service.ts  (kebab-case file name)

// Constants: SCREAMING_SNAKE_CASE
const MAX_RETRY_COUNT = 3;
const DEFAULT_CURRENCY = 'USD';
const BASE_TAX_RATE = 0.08;

// Enum: PascalCase name, PascalCase values
enum OrderStatus {
  Pending = 'PENDING',
  Confirmed = 'CONFIRMED',
  Shipped = 'SHIPPED',
  Delivered = 'DELIVERED',
}

// Interface: PascalCase
interface Money {
  readonly amount: number;
  readonly currency: string;
}

// Interface: PascalCase, NO "I" prefix
interface OrderRepository {
  findById(orderId: string): Promise<Order | null>;
  save(order: Order): Promise<void>;
  findByCustomerId(customerId: string): Promise<Order[]>;
}

// Type alias: PascalCase
type PaymentResult = {
  readonly transactionId: string;
  readonly status: OrderStatus;
  readonly amount: Money;
};

// Interface: PascalCase
interface CargoManifest {
  readonly manifestId: string;
  readonly origin: string;
  readonly destination: string;
  readonly items: readonly LineItem[];
}

// Class: PascalCase
class OrderService {
  // Private fields: camelCase with no prefix
  private readonly orderRepository: OrderRepository;
  private readonly taxCalculator: TaxCalculator;

  constructor(orderRepository: OrderRepository, taxCalculator: TaxCalculator) {
    this.orderRepository = orderRepository;
    this.taxCalculator = taxCalculator;
  }

  // Methods: camelCase, descriptive verb phrase
  async calculateTotal(items: readonly LineItem[]): Promise<Money> {
    if (items.length === 0) {
      return { amount: 0, currency: DEFAULT_CURRENCY };
    }

    // Variables: camelCase
    const subtotal = this.sumLineItems(items);
    const taxAmount = this.taxCalculator.calculateTax(subtotal);
    const customerCount = await this.getActiveCustomerCount();

    return {
      amount: subtotal.amount + taxAmount.amount,
      currency: subtotal.currency,
    };
  }

  validateEmail(email: string): boolean {
    // Boolean variable: is/has prefix
    const isValidFormat = email.includes('@');
    const hasDomain = email.split('@')[1]?.includes('.') ?? false;
    return isValidFormat && hasDomain;
  }

  // Private helper: camelCase
  private sumLineItems(items: readonly LineItem[]): Money {
    return items.reduce<Money>(
      (total, item) => ({
        amount: total.amount + item.unitPrice.amount * item.quantity,
        currency: total.currency,
      }),
      { amount: 0, currency: DEFAULT_CURRENCY },
    );
  }

  private async getActiveCustomerCount(): Promise<number> {
    // implementation
    return 0;
  }
}

// Function: camelCase
function createCargoManifest(
  origin: string,
  destination: string,
  orderItems: readonly LineItem[],
): CargoManifest {
  return {
    manifestId: generateId(),
    origin,
    destination,
    items: orderItems,
  };
}

export { OrderService, createCargoManifest, OrderStatus };
export type { Money, CargoManifest, OrderRepository, PaymentResult };
```

```typescript
// File: order-service.spec.ts  (kebab-case file name)
import { OrderService } from './order-service';

describe('OrderService', () => {
  // Variables: camelCase
  let orderService: OrderService;
  let mockRepository: jest.Mocked<OrderRepository>;
  let mockTaxCalculator: jest.Mocked<TaxCalculator>;

  beforeEach(() => {
    mockRepository = createMockRepository();
    mockTaxCalculator = createMockTaxCalculator();
    orderService = new OrderService(mockRepository, mockTaxCalculator);
  });

  describe('calculateTotal', () => {
    it('should return zero for empty items', async () => {
      const result = await orderService.calculateTotal([]);
      expect(result.amount).toBe(0);
    });

    it('should include tax in the total', async () => {
      // arrange, act, assert
    });
  });

  describe('validateEmail', () => {
    it('should reject email without at sign', () => {
      const isValid = orderService.validateEmail('invalid-email');
      expect(isValid).toBe(false);
    });
  });
});
```

**Why compliant:** Classes and interfaces use PascalCase without prefixes. Functions and variables use camelCase. Constants are SCREAMING_SNAKE_CASE. Files use kebab-case. Boolean variables use descriptive `is`/`has` prefixes. Every name communicates its purpose clearly.

---

## VIOLATION: Non-Idiomatic TypeScript Naming

```typescript
// VIOLATION: File should be kebab-case, not PascalCase
// File: OrderService.ts

// VIOLATION: Constants should be SCREAMING_SNAKE_CASE
const maxRetryCount = 3;
const default_currency = 'USD';

// VIOLATION: Interface should NOT have "I" prefix (C#/.NET convention)
interface IOrderRepository {
  // VIOLATION: Method should be camelCase, not PascalCase
  FindById(orderId: string): Promise<Order | null>;
  Save(order: Order): Promise<void>;
}

// VIOLATION: Enum values should be PascalCase, not SCREAMING_SNAKE
enum OrderStatus {
  PENDING = 'PENDING',
  CONFIRMED = 'CONFIRMED',
}

// VIOLATION: Class name is fine, but internal naming is wrong
class OrderService {
  // VIOLATION: Fields should be camelCase, not PascalCase or snake_case
  private readonly Order_Repository: IOrderRepository;
  private readonly Tax_Calculator: TaxCalculator;

  constructor(OrderRepository: IOrderRepository, TaxCalculator: TaxCalculator) {
    // VIOLATION: Parameter names should be camelCase
    this.Order_Repository = OrderRepository;
    this.Tax_Calculator = TaxCalculator;
  }

  // VIOLATION: Method should be camelCase, not PascalCase
  async CalculateTotal(Items: readonly LineItem[]): Promise<Money> {
    // VIOLATION: Variable should be camelCase, not PascalCase or snake_case
    let Sub_Total = 0;
    let CustomerCount = 0;

    for (const Item of Items) {
      Sub_Total += Item.unitPrice.amount * Item.quantity;
    }

    return { amount: Sub_Total, currency: default_currency };
  }

  // VIOLATION: Method should be camelCase, not snake_case
  validate_email(email_address: string): boolean {
    return email_address.includes('@');
  }
}

// VIOLATION: Function should be camelCase, not PascalCase
function CreateCargoManifest(
  Origin: string,         // VIOLATION: Parameters should be camelCase
  Destination: string,
  order_items: string[],  // VIOLATION: Parameter should be camelCase, not snake_case
): CargoManifest {
  return {
    manifestId: generateId(),
    origin: Origin,
    destination: Destination,
    items: order_items,
  };
}
```

**Why violates ENG-3.5:** This code uses PascalCase for methods (C# style), snake_case for variable and method names (Python style), an `I` prefix on interfaces (.NET convention), PascalCase for parameters and loop variables, and a PascalCase file name. These inconsistencies make the codebase confusing for TypeScript developers and conflict with established community standards.

---

## Quick Reference

```text
Classes/Interfaces    PascalCase          OrderService, OrderRepository
Types/Enums           PascalCase          OrderStatus, PaymentResult
Enum Values           PascalCase          OrderStatus.Confirmed
Functions/Methods     camelCase           calculateTotal()
Variables/Fields      camelCase           customerCount, orderItems
Parameters            camelCase           orderId, customerName
Constants             SCREAMING_SNAKE     MAX_RETRY_COUNT
Booleans              is/has/should       isValid, hasPermission
Files                 kebab-case          order-service.ts
Directories           kebab-case          order-processing/
Interfaces            NO "I" prefix       OrderRepository (not IOrderRepository)
```
