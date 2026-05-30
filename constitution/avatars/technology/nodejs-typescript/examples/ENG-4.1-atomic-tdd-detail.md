---
law_id: ENG-4.1
avatar: nodejs-typescript
---

# ENG-4.1: Atomic TDD Examples for Node.js TypeScript

## COMPLIANT: Single Responsibility Test with Arrange-Act-Assert Pattern

```typescript
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { OrderService } from './order.service';
import { OrderRepository } from './order.repository';
import { InventoryService } from './inventory.service';
import { Order, OrderStatus } from './order.entity';
import { InsufficientInventoryError } from './errors';

describe('OrderService', () => {
  let orderService: OrderService;
  let orderRepository: jest.Mocked<OrderRepository>;
  let inventoryService: jest.Mocked<InventoryService>;

  beforeEach(() => {
    orderRepository = {
      save: vi.fn(),
      findById: vi.fn(),
    } as jest.Mocked<OrderRepository>;

    inventoryService = {
      checkAvailability: vi.fn(),
    } as jest.Mocked<InventoryService>;

    orderService = new OrderService(orderRepository, inventoryService);
  });

  describe('createOrder', () => {
    it('should create order when inventory is available', async () => {
      // Arrange
      const customerId = 'cust-123';
      const productId = 'prod-456';
      const quantity = 5;
      const request = { customerId, productId, quantity };
      const expectedOrder = Order.create(customerId, productId, quantity);

      inventoryService.checkAvailability.mockResolvedValue(true);
      orderRepository.save.mockResolvedValue(expectedOrder);

      // Act
      const result = await orderService.createOrder(request);

      // Assert
      expect(result).toBeDefined();
      expect(result.customerId).toBe(customerId);
      expect(result.status).toBe(OrderStatus.Created);
      expect(inventoryService.checkAvailability).toHaveBeenCalledWith(productId, quantity);
      expect(orderRepository.save).toHaveBeenCalledTimes(1);
    });

    it('should throw error when inventory is insufficient', async () => {
      // Arrange
      const request = {
        customerId: 'cust-123',
        productId: 'prod-456',
        quantity: 100,
      };

      inventoryService.checkAvailability.mockResolvedValue(false);

      // Act & Assert
      await expect(orderService.createOrder(request)).rejects.toThrow(
        InsufficientInventoryError
      );
      expect(orderRepository.save).not.toHaveBeenCalled();
    });
  });
});
```

**Why compliant:** Each test method verifies exactly one behavior. Tests follow the Arrange-Act-Assert pattern with clear separation. Descriptive names explain the scenario and expected outcome. Mocks isolate the unit under test.

---

## COMPLIANT: Parameterized Tests with test.each

```typescript
import { describe, it, expect } from 'vitest';
import { PriceCalculator } from './price-calculator';
import { LineItem } from './line-item';

describe('PriceCalculator', () => {
  const calculator = new PriceCalculator();

  describe('calculateTotal', () => {
    it.each([
      { quantity: 1, unitPrice: 100, expected: 100, description: 'no discount for single item' },
      { quantity: 10, unitPrice: 100, expected: 950, description: '5% discount for 10+ items' },
      { quantity: 50, unitPrice: 100, expected: 4500, description: '10% discount for 50+ items' },
      { quantity: 100, unitPrice: 100, expected: 8500, description: '15% discount for 100+ items' },
    ])(
      'should apply $description (quantity: $quantity)',
      ({ quantity, unitPrice, expected }) => {
        // Arrange
        const lineItem: LineItem = {
          productId: 'PROD-001',
          quantity,
          unitPrice,
        };

        // Act
        const result = calculator.calculateTotal(lineItem);

        // Assert
        expect(result).toBe(expected);
      }
    );

    it.each([0, -1, -100])(
      'should throw error for invalid quantity: %i',
      (invalidQuantity) => {
        // Arrange
        const lineItem: LineItem = {
          productId: 'PROD-001',
          quantity: invalidQuantity,
          unitPrice: 10,
        };

        // Act & Assert
        expect(() => calculator.calculateTotal(lineItem)).toThrow('Quantity must be positive');
      }
    );
  });
});
```

**Why compliant:** Parameterized tests efficiently test multiple inputs while maintaining single-assertion focus per logical scenario. Each test.each combination tests one specific discount tier behavior. Descriptions make test output readable.

---

## VIOLATION: Multiple Unrelated Assertions in Single Test

```typescript
import { describe, it, expect, vi } from 'vitest';
import { UserService } from './user.service';

describe('UserService', () => {
  it('should handle all user operations', async () => {
    const userRepository = { save: vi.fn(), findById: vi.fn(), delete: vi.fn() };
    const emailService = { sendWelcomeEmail: vi.fn() };
    const auditService = { logUpdate: vi.fn(), logDeletion: vi.fn() };

    const userService = new UserService(userRepository, emailService, auditService);

    // Testing user creation
    const createRequest = { email: 'john@example.com', name: 'John Doe' };
    userRepository.save.mockResolvedValue({ id: '1', ...createRequest });

    const createdUser = await userService.createUser(createRequest);
    expect(createdUser).toBeDefined();
    expect(createdUser.email).toBe('john@example.com');
    expect(emailService.sendWelcomeEmail).toHaveBeenCalled();

    // Testing user update
    const updateRequest = { id: '1', name: 'Jane Doe' };
    userRepository.findById.mockResolvedValue(createdUser);

    const updatedUser = await userService.updateUser(updateRequest);
    expect(updatedUser.name).toBe('Jane Doe');
    expect(auditService.logUpdate).toHaveBeenCalled();

    // Testing user deletion
    await userService.deleteUser('1');
    expect(userRepository.delete).toHaveBeenCalledWith('1');
    expect(auditService.logDeletion).toHaveBeenCalled();

    // Testing email validation
    expect(userService.isValidEmail('test@test.com')).toBe(true);
    expect(userService.isValidEmail('invalid')).toBe(false);
  });
});
```

**Why violates ENG-4.1:** This test combines four unrelated behaviors (create, update, delete, validation) into one method. When it fails, you cannot quickly identify which operation broke. Tests should be atomic - one behavior per test method. Each operation should be its own test with focused assertions.

---

## VIOLATION: Test Without Clear Arrange-Act-Assert Structure

```typescript
import { describe, it, expect } from 'vitest';
import { PaymentProcessor } from './payment-processor';

describe('PaymentProcessor', () => {
  it('should process payment', async () => {
    const processor = new PaymentProcessor(new MockGateway(), new MockNotifier());
    const result = await processor.process({ amount: 100, currency: 'USD', cardId: 'card_123' });
    expect(result.isSuccessful).toBe(true);
    const refund = await processor.refund(result.transactionId, 50);
    expect(refund.isSuccessful).toBe(true);
    expect(refund.amount).toBe(50);
    const status = await processor.getStatus(result.transactionId);
    expect(status).toBe('PARTIALLY_REFUNDED');
    await processor.process({ amount: -10, currency: 'USD', cardId: 'card_123' });
    // This should fail but we forgot to assert
  });
});
```

**Why violates ENG-4.1:** No clear AAA structure makes the test hard to read. Multiple operations are chained without separation. The test verifies process, refund, and status check in sequence - if any fails, debugging requires understanding the entire chain. The last operation has no assertion at all.

---

## COMPLIANT: Integration Test with Testcontainers

```typescript
import { describe, it, expect, beforeAll, afterAll, beforeEach } from 'vitest';
import { PostgreSqlContainer, StartedPostgreSqlContainer } from '@testcontainers/postgresql';
import { PrismaClient } from '@prisma/client';
import { OrderRepository } from './order.repository';
import { Order } from './order.entity';

describe('OrderRepository Integration', () => {
  let container: StartedPostgreSqlContainer;
  let prisma: PrismaClient;
  let repository: OrderRepository;

  beforeAll(async () => {
    container = await new PostgreSqlContainer('postgres:15-alpine').start();

    prisma = new PrismaClient({
      datasources: {
        db: { url: container.getConnectionUri() },
      },
    });

    await prisma.$executeRaw`
      CREATE TABLE orders (
        id UUID PRIMARY KEY,
        customer_id UUID NOT NULL,
        status VARCHAR(50) NOT NULL,
        total_amount DECIMAL(10,2) NOT NULL,
        created_at TIMESTAMP NOT NULL
      )
    `;

    repository = new OrderRepository(prisma);
  }, 60000);

  afterAll(async () => {
    await prisma.$disconnect();
    await container.stop();
  });

  beforeEach(async () => {
    await prisma.order.deleteMany();
  });

  it('should find orders by customer ID with pagination', async () => {
    // Arrange
    const customerId = crypto.randomUUID();
    const orders = Array.from({ length: 25 }, (_, i) =>
      Order.create(customerId, crypto.randomUUID(), i + 1)
    );

    for (const order of orders) {
      await repository.save(order);
    }

    // Act
    const result = await repository.findByCustomerId(customerId, {
      page: 1,
      pageSize: 10,
    });

    // Assert
    expect(result.items).toHaveLength(10);
    expect(result.totalCount).toBe(25);
    expect(result.totalPages).toBe(3);
  });
});
```

**Why compliant:** Integration test focuses on one repository method behavior. Uses Testcontainers for realistic database testing. Clear AAA structure with proper setup isolation via beforeEach.

---

## VIOLATION: Missing Edge Case Tests

```typescript
import { describe, it, expect } from 'vitest';
import { DiscountService } from './discount.service';

describe('DiscountService', () => {
  it('should apply discount', () => {
    const service = new DiscountService();

    // Only tests happy path
    const result = service.applyDiscount(100, 'SAVE10');
    expect(result).toBe(90);
  });
});
```

**Why violates ENG-4.1:** Only tests the happy path. Missing tests for: invalid/expired codes, null inputs, zero/negative amounts, code case sensitivity, maximum discount limits. Atomic TDD requires comprehensive coverage of edge cases, each in its own focused test.

---

## COMPLIANT: Comprehensive Edge Case Coverage

```typescript
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { DiscountService } from './discount.service';
import { DiscountCodeRepository } from './discount-code.repository';
import { DiscountCode, DiscountType } from './discount-code.entity';
import { DiscountExpiredError } from './errors';

describe('DiscountService', () => {
  let service: DiscountService;
  let repository: jest.Mocked<DiscountCodeRepository>;

  beforeEach(() => {
    repository = {
      findByCode: vi.fn(),
    } as jest.Mocked<DiscountCodeRepository>;

    service = new DiscountService(repository);
  });

  describe('applyDiscount', () => {
    it('should apply percentage discount with valid code', async () => {
      // Arrange
      const code: DiscountCode = {
        code: 'SAVE10',
        type: DiscountType.Percentage,
        value: 10,
        expiresAt: new Date(Date.now() + 86400000), // Tomorrow
      };
      repository.findByCode.mockResolvedValue(code);

      // Act
      const result = await service.applyDiscount(100, 'SAVE10');

      // Assert
      expect(result).toBe(90);
    });

    it('should throw error for null discount code', async () => {
      // Act & Assert
      await expect(service.applyDiscount(100, null as any)).rejects.toThrow(
        'Discount code is required'
      );
    });

    it('should throw error for undefined discount code', async () => {
      // Act & Assert
      await expect(service.applyDiscount(100, undefined as any)).rejects.toThrow(
        'Discount code is required'
      );
    });

    it('should throw error for expired discount code', async () => {
      // Arrange
      const expiredCode: DiscountCode = {
        code: 'EXPIRED',
        type: DiscountType.Percentage,
        value: 10,
        expiresAt: new Date(Date.now() - 86400000), // Yesterday
      };
      repository.findByCode.mockResolvedValue(expiredCode);

      // Act & Assert
      await expect(service.applyDiscount(100, 'EXPIRED')).rejects.toThrow(
        DiscountExpiredError
      );
    });

    it.each([0, -1, -100.5])(
      'should throw error for invalid amount: %d',
      async (invalidAmount) => {
        // Act & Assert
        await expect(service.applyDiscount(invalidAmount, 'SAVE10')).rejects.toThrow(
          'Amount must be positive'
        );
      }
    );

    it.each(['save10', 'SAVE10', 'Save10'])(
      'should be case insensitive for code: %s',
      async (codeVariant) => {
        // Arrange
        const code: DiscountCode = {
          code: 'SAVE10',
          type: DiscountType.Percentage,
          value: 10,
          expiresAt: new Date(Date.now() + 86400000),
        };
        repository.findByCode.mockResolvedValue(code);

        // Act
        const result = await service.applyDiscount(100, codeVariant);

        // Assert
        expect(result).toBe(90);
      }
    );

    it('should cap discount at maximum when percentage exceeds limit', async () => {
      // Arrange
      const code: DiscountCode = {
        code: 'MEGA50',
        type: DiscountType.Percentage,
        value: 50,
        maxDiscount: 25,
        expiresAt: new Date(Date.now() + 86400000),
      };
      repository.findByCode.mockResolvedValue(code);

      // Act
      const result = await service.applyDiscount(100, 'MEGA50');

      // Assert
      expect(result).toBe(75); // 50% would be 50, but capped at 25
    });

    it('should throw error for non-existent discount code', async () => {
      // Arrange
      repository.findByCode.mockResolvedValue(null);

      // Act & Assert
      await expect(service.applyDiscount(100, 'INVALID')).rejects.toThrow(
        'Discount code not found'
      );
    });
  });
});
```

**Why compliant:** Each edge case has its own focused test. Test names clearly describe the scenario and expected behavior. Comprehensive coverage of null inputs, expired codes, invalid amounts, case sensitivity, and maximum discount limits.

---

## COMPLIANT: Testing Async Error Handling

```typescript
import { describe, it, expect, vi } from 'vitest';
import { PaymentService } from './payment.service';
import { PaymentGateway } from './payment.gateway';
import { PaymentError, NetworkError, ValidationError } from './errors';

describe('PaymentService error handling', () => {
  const mockGateway: jest.Mocked<PaymentGateway> = {
    charge: vi.fn(),
    refund: vi.fn(),
  };

  const service = new PaymentService(mockGateway);

  it('should wrap gateway errors in PaymentError', async () => {
    // Arrange
    mockGateway.charge.mockRejectedValue(new Error('Card declined'));

    // Act & Assert
    await expect(
      service.processPayment({ amount: 100, cardId: 'card_123' })
    ).rejects.toThrow(PaymentError);
  });

  it('should preserve original error message in PaymentError', async () => {
    // Arrange
    mockGateway.charge.mockRejectedValue(new Error('Card declined'));

    // Act & Assert
    await expect(
      service.processPayment({ amount: 100, cardId: 'card_123' })
    ).rejects.toThrow('Card declined');
  });

  it('should throw NetworkError on timeout', async () => {
    // Arrange
    mockGateway.charge.mockRejectedValue(new Error('ETIMEDOUT'));

    // Act & Assert
    await expect(
      service.processPayment({ amount: 100, cardId: 'card_123' })
    ).rejects.toThrow(NetworkError);
  });

  it('should throw ValidationError for invalid card format', async () => {
    // Act & Assert
    await expect(
      service.processPayment({ amount: 100, cardId: 'invalid' })
    ).rejects.toThrow(ValidationError);
  });
});
```

**Why compliant:** Each test focuses on one specific error scenario. Error types and messages are tested separately when both matter. The tests document the error handling contract of the service.

---

## TDD Cycle Commands

```bash
# RED: Run specific test, see it fail
npm test -- --testNamePattern="should create order when inventory is available"

# GREEN: Write code, run test again
npm test -- --testNamePattern="should create order when inventory is available"

# REFACTOR: Run all unit tests
npm test

# VERIFY: Check coverage and constitutional compliance
npm test -- --coverage
constitution-lint .

# Commit when green and compliant
git add -A && git commit -m "Add order creation to OrderService"
```
