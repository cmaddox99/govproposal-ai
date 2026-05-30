---
law_id: ENG-6.5
avatar: nodejs-typescript
---

# ENG-6.5: Input Validation Examples for Node.js TypeScript

## COMPLIANT: Zod Schema Validation with Type Inference

```typescript
import { z } from 'zod';

// Define schemas with comprehensive validation
export const CreateOrderSchema = z.object({
  customerId: z.string().uuid('Customer ID must be a valid UUID'),
  items: z
    .array(
      z.object({
        productId: z.string().uuid('Product ID must be a valid UUID'),
        quantity: z.number().int().positive('Quantity must be a positive integer'),
        unitPrice: z.number().positive('Unit price must be positive'),
      })
    )
    .min(1, 'Order must contain at least one item')
    .max(100, 'Order cannot contain more than 100 items'),
  shippingAddress: z.object({
    street: z.string().min(1, 'Street is required').max(200),
    city: z.string().min(1, 'City is required').max(100),
    state: z.string().length(2, 'State must be 2-letter code'),
    zipCode: z.string().regex(/^\d{5}(-\d{4})?$/, 'Invalid ZIP code format'),
    country: z.string().length(2, 'Country must be 2-letter ISO code'),
  }),
  notes: z.string().max(1000).optional(),
  expeditedShipping: z.boolean().default(false),
});

// Type is inferred from schema
export type CreateOrderRequest = z.infer<typeof CreateOrderSchema>;

// Validation in service layer
export class OrderService {
  async createOrder(input: unknown): Promise<Order> {
    // Parse and validate - throws ZodError on failure
    const request = CreateOrderSchema.parse(input);

    // request is now fully typed as CreateOrderRequest
    return this.processOrder(request);
  }

  async createOrderSafe(input: unknown): Promise<Result<Order, ValidationError>> {
    // Safe parse returns result object instead of throwing
    const result = CreateOrderSchema.safeParse(input);

    if (!result.success) {
      return {
        success: false,
        error: new ValidationError(formatZodError(result.error)),
      };
    }

    const order = await this.processOrder(result.data);
    return { success: true, data: order };
  }

  private async processOrder(request: CreateOrderRequest): Promise<Order> {
    // Business logic with validated, typed data
    return Order.create(request);
  }
}

// Helper to format Zod errors for API responses
function formatZodError(error: z.ZodError): string {
  return error.errors
    .map(e => `${e.path.join('.')}: ${e.message}`)
    .join('; ');
}
```

**Why compliant:** Schema defines validation rules declaratively. Type is inferred from schema, ensuring sync between validation and types. Both throwing and safe-parse patterns are shown. Error messages are user-friendly. Validation happens at the service boundary.

---

## COMPLIANT: Custom Zod Refinements for Business Rules

```typescript
import { z } from 'zod';

// Password with custom validation rules
export const PasswordSchema = z
  .string()
  .min(8, 'Password must be at least 8 characters')
  .max(128, 'Password cannot exceed 128 characters')
  .refine(
    (password) => /[A-Z]/.test(password),
    'Password must contain at least one uppercase letter'
  )
  .refine(
    (password) => /[a-z]/.test(password),
    'Password must contain at least one lowercase letter'
  )
  .refine(
    (password) => /[0-9]/.test(password),
    'Password must contain at least one number'
  )
  .refine(
    (password) => /[^A-Za-z0-9]/.test(password),
    'Password must contain at least one special character'
  );

// Date range validation with cross-field refinement
export const DateRangeSchema = z
  .object({
    startDate: z.coerce.date(),
    endDate: z.coerce.date(),
  })
  .refine(
    (data) => data.endDate > data.startDate,
    {
      message: 'End date must be after start date',
      path: ['endDate'], // Error will be attached to endDate field
    }
  );

// Credit card with Luhn algorithm validation
export const CreditCardSchema = z.object({
  number: z
    .string()
    .regex(/^\d{13,19}$/, 'Card number must be 13-19 digits')
    .refine(validateLuhn, 'Invalid card number'),
  expiryMonth: z.number().int().min(1).max(12),
  expiryYear: z.number().int().min(new Date().getFullYear()),
  cvv: z.string().regex(/^\d{3,4}$/, 'CVV must be 3-4 digits'),
  holderName: z
    .string()
    .min(2)
    .max(100)
    .regex(/^[A-Za-z\s'-]+$/, 'Name can only contain letters, spaces, hyphens, and apostrophes'),
}).refine(
  (data) => {
    const now = new Date();
    const expiryDate = new Date(data.expiryYear, data.expiryMonth - 1);
    return expiryDate > now;
  },
  {
    message: 'Card has expired',
    path: ['expiryMonth'],
  }
);

// Luhn algorithm implementation
function validateLuhn(cardNumber: string): boolean {
  let sum = 0;
  let isEven = false;

  for (let i = cardNumber.length - 1; i >= 0; i--) {
    let digit = parseInt(cardNumber[i], 10);

    if (isEven) {
      digit *= 2;
      if (digit > 9) {
        digit -= 9;
      }
    }

    sum += digit;
    isEven = !isEven;
  }

  return sum % 10 === 0;
}

export type CreditCardInput = z.infer<typeof CreditCardSchema>;
```

**Why compliant:** Custom refinements encode business rules in the schema. Cross-field validation (date range, card expiry) is handled properly. The Luhn algorithm validates card numbers at parse time. Error paths are specified for proper error attribution.

---

## COMPLIANT: class-validator with Decorators

```typescript
import {
  IsUUID,
  IsString,
  IsInt,
  IsPositive,
  IsArray,
  ValidateNested,
  ArrayMinSize,
  ArrayMaxSize,
  IsOptional,
  MaxLength,
  MinLength,
  IsEmail,
  Matches,
  IsBoolean,
  validate,
  ValidationError as ClassValidationError,
} from 'class-validator';
import { Type, plainToInstance } from 'class-transformer';

// DTO classes with validation decorators
export class OrderItemDto {
  @IsUUID('4', { message: 'Product ID must be a valid UUID' })
  productId!: string;

  @IsInt({ message: 'Quantity must be an integer' })
  @IsPositive({ message: 'Quantity must be positive' })
  quantity!: number;

  @IsPositive({ message: 'Unit price must be positive' })
  unitPrice!: number;
}

export class ShippingAddressDto {
  @IsString()
  @MinLength(1, { message: 'Street is required' })
  @MaxLength(200)
  street!: string;

  @IsString()
  @MinLength(1, { message: 'City is required' })
  @MaxLength(100)
  city!: string;

  @IsString()
  @Matches(/^[A-Z]{2}$/, { message: 'State must be 2-letter code' })
  state!: string;

  @IsString()
  @Matches(/^\d{5}(-\d{4})?$/, { message: 'Invalid ZIP code format' })
  zipCode!: string;

  @IsString()
  @Matches(/^[A-Z]{2}$/, { message: 'Country must be 2-letter ISO code' })
  country!: string;
}

export class CreateOrderDto {
  @IsUUID('4', { message: 'Customer ID must be a valid UUID' })
  customerId!: string;

  @IsArray()
  @ValidateNested({ each: true })
  @ArrayMinSize(1, { message: 'Order must contain at least one item' })
  @ArrayMaxSize(100, { message: 'Order cannot contain more than 100 items' })
  @Type(() => OrderItemDto)
  items!: OrderItemDto[];

  @ValidateNested()
  @Type(() => ShippingAddressDto)
  shippingAddress!: ShippingAddressDto;

  @IsOptional()
  @IsString()
  @MaxLength(1000)
  notes?: string;

  @IsOptional()
  @IsBoolean()
  expeditedShipping?: boolean;
}

// Validation helper
export async function validateDto<T extends object>(
  dtoClass: new () => T,
  data: unknown
): Promise<{ valid: true; data: T } | { valid: false; errors: string[] }> {
  const instance = plainToInstance(dtoClass, data);
  const errors = await validate(instance);

  if (errors.length > 0) {
    return {
      valid: false,
      errors: formatValidationErrors(errors),
    };
  }

  return { valid: true, data: instance };
}

function formatValidationErrors(errors: ClassValidationError[]): string[] {
  return errors.flatMap(error => {
    const constraints = Object.values(error.constraints ?? {});
    const nested = error.children ? formatValidationErrors(error.children) : [];
    return [...constraints, ...nested];
  });
}

// Usage in controller
export class OrderController {
  async create(req: Request, res: Response): Promise<void> {
    const result = await validateDto(CreateOrderDto, req.body);

    if (!result.valid) {
      res.status(400).json({ errors: result.errors });
      return;
    }

    const order = await this.orderService.createOrder(result.data);
    res.status(201).json(order);
  }
}
```

**Why compliant:** Decorators clearly express validation rules on properties. Nested validation handles complex objects. plainToInstance ensures proper type conversion. Validation errors are collected and formatted for API responses.

---

## VIOLATION: No Input Validation

```typescript
// Dangerous: No validation at all
export class OrderService {
  async createOrder(request: CreateOrderRequest): Promise<Order> {
    // Directly using unvalidated input
    const order = new Order();
    order.customerId = request.customerId; // Could be undefined or invalid
    order.items = request.items; // Could be empty, contain negative quantities

    for (const item of request.items) {
      // item.quantity could be negative, NaN, or undefined
      // item.productId could be invalid SQL/NoSQL injection
      await this.repository.addItem(order.id, item.productId, item.quantity);
    }

    return order;
  }
}

// Dangerous: Validation only in some places
export class UserService {
  async createUser(email: string, password: string): Promise<User> {
    // Partial validation - easy to bypass
    if (!email.includes('@')) {
      throw new Error('Invalid email');
    }

    // Password validation missing entirely
    // No length check, no complexity requirements

    return this.repository.create({ email, password });
  }
}
```

**Why violates ENG-6.5:** No schema validation allows malformed data to enter the system. Partial validation creates security gaps. Input could cause database errors, injection attacks, or business logic failures. Type safety is not enforced at runtime boundaries.

---

## VIOLATION: Validation Logic Scattered Throughout Code

```typescript
export class OrderController {
  async createOrder(req: Request, res: Response): Promise<void> {
    // Validation mixed with controller logic
    if (!req.body.customerId) {
      res.status(400).json({ error: 'Customer ID required' });
      return;
    }

    if (typeof req.body.customerId !== 'string') {
      res.status(400).json({ error: 'Customer ID must be a string' });
      return;
    }

    // More validation scattered here...
    const order = await this.orderService.createOrder(req.body);
    res.json(order);
  }
}

export class OrderService {
  async createOrder(request: any): Promise<Order> {
    // Duplicate validation in service
    if (!request.items || request.items.length === 0) {
      throw new Error('Items required');
    }

    for (const item of request.items) {
      // Even more validation scattered here
      if (item.quantity <= 0) {
        throw new Error('Invalid quantity');
      }
    }

    return this.repository.save(request);
  }
}

export class OrderRepository {
  async save(order: any): Promise<Order> {
    // Yet more validation at persistence layer
    if (!order.customerId.match(/^[0-9a-f-]{36}$/)) {
      throw new Error('Invalid customer ID format');
    }

    return this.db.insert(order);
  }
}
```

**Why violates ENG-6.5:** Validation logic is duplicated across controller, service, and repository. Inconsistent error handling makes debugging difficult. No single source of truth for validation rules. Easy to miss validation in one layer while adding in another.

---

## COMPLIANT: Express Middleware with Zod

```typescript
import { Request, Response, NextFunction, RequestHandler } from 'express';
import { z, ZodSchema, ZodError } from 'zod';

// Generic validation middleware factory
export function validateRequest<T extends ZodSchema>(schema: T): RequestHandler {
  return (req: Request, res: Response, next: NextFunction) => {
    try {
      req.body = schema.parse(req.body);
      next();
    } catch (error) {
      if (error instanceof ZodError) {
        res.status(400).json({
          error: 'Validation failed',
          details: error.errors.map(e => ({
            path: e.path.join('.'),
            message: e.message,
          })),
        });
        return;
      }
      next(error);
    }
  };
}

// Query params validation
export function validateQuery<T extends ZodSchema>(schema: T): RequestHandler {
  return (req: Request, res: Response, next: NextFunction) => {
    try {
      req.query = schema.parse(req.query) as any;
      next();
    } catch (error) {
      if (error instanceof ZodError) {
        res.status(400).json({
          error: 'Invalid query parameters',
          details: error.errors.map(e => ({
            path: e.path.join('.'),
            message: e.message,
          })),
        });
        return;
      }
      next(error);
    }
  };
}

// URL params validation
export function validateParams<T extends ZodSchema>(schema: T): RequestHandler {
  return (req: Request, res: Response, next: NextFunction) => {
    try {
      req.params = schema.parse(req.params) as any;
      next();
    } catch (error) {
      if (error instanceof ZodError) {
        res.status(400).json({
          error: 'Invalid URL parameters',
          details: error.errors.map(e => ({
            path: e.path.join('.'),
            message: e.message,
          })),
        });
        return;
      }
      next(error);
    }
  };
}

// Usage in routes
const OrderIdSchema = z.object({
  id: z.string().uuid(),
});

const ListOrdersQuerySchema = z.object({
  page: z.coerce.number().int().positive().default(1),
  pageSize: z.coerce.number().int().min(1).max(100).default(20),
  status: z.enum(['pending', 'confirmed', 'shipped', 'delivered']).optional(),
});

app.post(
  '/orders',
  validateRequest(CreateOrderSchema),
  async (req: Request, res: Response) => {
    // req.body is now typed and validated
    const order = await orderService.createOrder(req.body);
    res.status(201).json(order);
  }
);

app.get(
  '/orders/:id',
  validateParams(OrderIdSchema),
  async (req: Request, res: Response) => {
    const order = await orderService.getOrder(req.params.id);
    res.json(order);
  }
);

app.get(
  '/orders',
  validateQuery(ListOrdersQuerySchema),
  async (req: Request, res: Response) => {
    const orders = await orderService.listOrders(req.query);
    res.json(orders);
  }
);
```

**Why compliant:** Validation is centralized in middleware. Request body, query, and params are all validated. Consistent error response format across all endpoints. Route handlers receive validated, typed data. z.coerce handles string-to-number conversion from query strings.

---

## COMPLIANT: NestJS with class-validator Integration

```typescript
import {
  Controller,
  Post,
  Body,
  Get,
  Param,
  Query,
  UsePipes,
  ValidationPipe,
  ParseUUIDPipe,
} from '@nestjs/common';
import {
  IsUUID,
  IsString,
  IsInt,
  IsPositive,
  IsArray,
  ValidateNested,
  ArrayMinSize,
  IsOptional,
  IsEnum,
} from 'class-validator';
import { Type, Transform } from 'class-transformer';

// DTOs with validation
class CreateOrderItemDto {
  @IsUUID('4')
  productId!: string;

  @IsInt()
  @IsPositive()
  quantity!: number;

  @IsPositive()
  unitPrice!: number;
}

class CreateOrderDto {
  @IsUUID('4')
  customerId!: string;

  @IsArray()
  @ValidateNested({ each: true })
  @ArrayMinSize(1)
  @Type(() => CreateOrderItemDto)
  items!: CreateOrderItemDto[];
}

class ListOrdersQueryDto {
  @IsOptional()
  @IsInt()
  @IsPositive()
  @Transform(({ value }) => parseInt(value, 10))
  page?: number = 1;

  @IsOptional()
  @IsInt()
  @IsPositive()
  @Transform(({ value }) => parseInt(value, 10))
  pageSize?: number = 20;

  @IsOptional()
  @IsEnum(['pending', 'confirmed', 'shipped', 'delivered'])
  status?: string;
}

@Controller('orders')
@UsePipes(new ValidationPipe({ transform: true, whitelist: true }))
export class OrderController {
  constructor(private readonly orderService: OrderService) {}

  @Post()
  async create(@Body() dto: CreateOrderDto) {
    // dto is validated and typed
    return this.orderService.createOrder(dto);
  }

  @Get(':id')
  async findOne(@Param('id', ParseUUIDPipe) id: string) {
    // id is validated as UUID
    return this.orderService.findOne(id);
  }

  @Get()
  async findAll(@Query() query: ListOrdersQueryDto) {
    // query is validated and transformed
    return this.orderService.findAll(query);
  }
}

// Global validation pipe configuration in main.ts
app.useGlobalPipes(
  new ValidationPipe({
    transform: true,           // Auto-transform payloads to DTO instances
    whitelist: true,           // Strip properties not in DTO
    forbidNonWhitelisted: true, // Throw error for extra properties
    transformOptions: {
      enableImplicitConversion: true,
    },
  })
);
```

**Why compliant:** NestJS's ValidationPipe provides automatic validation. DTOs define validation rules with decorators. ParseUUIDPipe validates URL parameters. Transform decorator handles query string conversion. Whitelist option prevents mass assignment vulnerabilities.

---

## COMPLIANT: Validation with Discriminated Unions

```typescript
import { z } from 'zod';

// Base event schema
const BaseEventSchema = z.object({
  id: z.string().uuid(),
  timestamp: z.coerce.date(),
  correlationId: z.string().uuid().optional(),
});

// Specific event schemas
const OrderCreatedEventSchema = BaseEventSchema.extend({
  type: z.literal('order.created'),
  payload: z.object({
    orderId: z.string().uuid(),
    customerId: z.string().uuid(),
    items: z.array(z.object({
      productId: z.string().uuid(),
      quantity: z.number().int().positive(),
    })),
    totalAmount: z.number().positive(),
  }),
});

const OrderCancelledEventSchema = BaseEventSchema.extend({
  type: z.literal('order.cancelled'),
  payload: z.object({
    orderId: z.string().uuid(),
    reason: z.string().max(500),
    refundAmount: z.number().nonnegative(),
  }),
});

const PaymentProcessedEventSchema = BaseEventSchema.extend({
  type: z.literal('payment.processed'),
  payload: z.object({
    paymentId: z.string().uuid(),
    orderId: z.string().uuid(),
    amount: z.number().positive(),
    status: z.enum(['success', 'failed', 'pending']),
  }),
});

// Discriminated union of all event types
const EventSchema = z.discriminatedUnion('type', [
  OrderCreatedEventSchema,
  OrderCancelledEventSchema,
  PaymentProcessedEventSchema,
]);

export type Event = z.infer<typeof EventSchema>;
export type OrderCreatedEvent = z.infer<typeof OrderCreatedEventSchema>;
export type OrderCancelledEvent = z.infer<typeof OrderCancelledEventSchema>;
export type PaymentProcessedEvent = z.infer<typeof PaymentProcessedEventSchema>;

// Type-safe event handler
export class EventProcessor {
  async processEvent(rawEvent: unknown): Promise<void> {
    const event = EventSchema.parse(rawEvent);

    // TypeScript narrows the type based on event.type
    switch (event.type) {
      case 'order.created':
        // event.payload is typed as OrderCreatedEvent['payload']
        await this.handleOrderCreated(event.payload);
        break;
      case 'order.cancelled':
        // event.payload is typed as OrderCancelledEvent['payload']
        await this.handleOrderCancelled(event.payload);
        break;
      case 'payment.processed':
        // event.payload is typed as PaymentProcessedEvent['payload']
        await this.handlePaymentProcessed(event.payload);
        break;
    }
  }

  private async handleOrderCreated(payload: OrderCreatedEvent['payload']): Promise<void> {
    // Fully typed payload
    console.log(`Order ${payload.orderId} created with ${payload.items.length} items`);
  }

  private async handleOrderCancelled(payload: OrderCancelledEvent['payload']): Promise<void> {
    console.log(`Order ${payload.orderId} cancelled: ${payload.reason}`);
  }

  private async handlePaymentProcessed(payload: PaymentProcessedEvent['payload']): Promise<void> {
    console.log(`Payment ${payload.paymentId} ${payload.status} for order ${payload.orderId}`);
  }
}
```

**Why compliant:** Discriminated unions validate polymorphic data correctly. Each event type has its own validation rules. TypeScript narrows types based on the discriminator field. The switch statement is exhaustive - adding a new event type causes a compile error if not handled.
