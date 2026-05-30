---
law_id: ENG-3.3
avatar: nodejs-typescript
---

# ENG-3.3: Law of Demeter Examples for Node.js TypeScript

## VIOLATION: Train Wreck Chain (reaching through objects)

```typescript
class City {
  constructor(
    public readonly name: string,
    public readonly state: string
  ) {}
}

class Address {
  constructor(
    public readonly street: string,
    public readonly city: City,
    public readonly zipCode: string
  ) {}
}

class Customer {
  constructor(
    public readonly name: string,
    public readonly address: Address
  ) {}
}

class Order {
  constructor(
    public readonly id: string,
    public readonly customer: Customer,
    public readonly total: number
  ) {}
}

// VIOLATION: function reaches deep into the object graph
function getShippingLabel(order: Order): string {
  // "Train wreck" - navigating through 3 levels of properties
  const cityName = order.customer.address.city.name;
  const state = order.customer.address.city.state;
  const street = order.customer.address.street;
  const zip = order.customer.address.zipCode;

  return `${order.customer.name}\n${street}\n${cityName}, ${state} ${zip}`;
}
```

**Why violates ENG-3.3:** `getShippingLabel` is tightly coupled to the internal structure of `Order`, `Customer`, `Address`, and `City`. The property chain `order.customer.address.city.name` means any restructuring of intermediate objects (e.g., wrapping `City` in a `Region`) breaks this function and every other function that navigates the same chain.

---

## COMPLIANT: Encapsulated Access via Class Methods

```typescript
class City {
  constructor(
    public readonly name: string,
    public readonly state: string
  ) {}
}

class Address {
  constructor(
    private readonly street: string,
    private readonly city: City,
    private readonly zipCode: string
  ) {}

  cityName(): string {
    return this.city.name;
  }

  formatted(): string {
    return `${this.street}\n${this.city.name}, ${this.city.state} ${this.zipCode}`;
  }
}

class Customer {
  constructor(
    private readonly name: string,
    private readonly address: Address
  ) {}

  shippingAddress(): string {
    return `${this.name}\n${this.address.formatted()}`;
  }
}

class Order {
  constructor(
    public readonly id: string,
    private readonly customer: Customer,
    public readonly total: number
  ) {}

  deliveryCity(): string {
    // Delegates to direct collaborator only
    return this.customer.deliveryCity();
  }

  shippingLabel(): string {
    return this.customer.shippingAddress();
  }
}

// Add to Customer so Order can delegate
class Customer {
  // ...existing constructor...

  deliveryCity(): string {
    return this.address.cityName();
  }
}

// COMPLIANT: only talks to direct collaborator
function getShippingLabel(order: Order): string {
  return order.shippingLabel();
}

function getDeliveryCity(order: Order): string {
  return order.deliveryCity();
}
```

**Why compliant:** Each class exposes focused methods instead of leaking its internal structure. `getShippingLabel` only talks to `Order`. `Order` delegates to `Customer`. `Customer` delegates to `Address`. Internal changes to `Address` only affect `Address` methods, not external callers.

---

## Express/NestJS Route Example

```typescript
// VIOLATION: route handler reaches deep into domain objects
router.get('/orders/:orderId/city', async (req, res) => {
  const order = await orderService.findById(req.params.orderId);
  // Reaching through the entire object graph
  const city = order.customer.address.city.name;
  res.json({ city });
});

// COMPLIANT: route handler uses encapsulated method
router.get('/orders/:orderId/city', async (req, res) => {
  const order = await orderService.findById(req.params.orderId);
  // Only talks to direct collaborator
  res.json({ city: order.deliveryCity() });
});

// COMPLIANT: NestJS controller with service encapsulation
@Controller('orders')
export class OrderController {
  constructor(private readonly orderService: OrderService) {}

  @Get(':orderId/city')
  async getDeliveryCity(@Param('orderId') orderId: string) {
    // Service method encapsulates the domain call
    return { city: await this.orderService.getDeliveryCity(orderId) };
  }
}

@Injectable()
export class OrderService {
  constructor(private readonly orderRepository: OrderRepository) {}

  async getDeliveryCity(orderId: string): Promise<string> {
    const order = await this.orderRepository.findById(orderId);
    return order.deliveryCity();
  }
}
```

---

## Why It Matters

The Law of Demeter reduces **coupling between components**. When code reaches through chains like `order.customer.address.city.name`, it creates invisible dependencies on the internal structure of every object in that chain. This leads to:

- **Fragile code:** A structural change in any intermediate object breaks all callers
- **Hidden dependencies:** The function secretly depends on Customer, Address, and City, but only declares a dependency on Order
- **Difficult testing:** Tests must construct deep object graphs instead of simple stubs
- **Ripple effects:** Refactoring one class forces changes across routes, services, and other modules

---

## The Rule

A method `M` of object `O` should only call methods on:

1. **`O` itself** - the object's own methods
2. **Objects passed as parameters to `M`** - direct arguments
3. **Objects created within `M`** - locally instantiated objects
4. **`O`'s direct component objects** - properties held by the object

Any other access (reaching through a property to access a stranger's property) violates the law and should be refactored into a method on the direct collaborator.
