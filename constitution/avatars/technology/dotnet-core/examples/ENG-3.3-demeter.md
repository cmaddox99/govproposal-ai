---
law_id: ENG-3.3
avatar: dotnet-core
---

# ENG-3.3: Law of Demeter Examples for .NET Core

## VIOLATION: Train Wreck Chain (reaching through objects)

```csharp
public class City
{
    public string Name { get; init; }
    public string State { get; init; }
}

public class Address
{
    public string Street { get; init; }
    public City City { get; init; }
    public string ZipCode { get; init; }
}

public class Customer
{
    public string Name { get; init; }
    public Address Address { get; init; }
}

public class Order
{
    public Guid Id { get; init; }
    public Customer Customer { get; init; }
    public decimal Total { get; init; }
}

// VIOLATION: service reaches deep into the object graph
public class ShippingLabelService
{
    public string GenerateLabel(Order order)
    {
        // "Train wreck" - chaining through 3 levels of properties
        var cityName = order.Customer.Address.City.Name;
        var state = order.Customer.Address.City.State;
        var street = order.Customer.Address.Street;
        var zip = order.Customer.Address.ZipCode;

        return $"{order.Customer.Name}\n{street}\n{cityName}, {state} {zip}";
    }
}
```

**Why violates ENG-3.3:** `ShippingLabelService.GenerateLabel` is coupled to the internal structure of `Order`, `Customer`, `Address`, and `City`. The property chain `order.Customer.Address.City.Name` means this service must know how every intermediate object is composed. If `Address` changes to wrap `City` inside a `Region`, every caller navigating this chain breaks.

---

## COMPLIANT: Encapsulated Access via Properties and Methods

```csharp
public class City
{
    public string Name { get; init; }
    public string State { get; init; }
}

public class Address
{
    private City City { get; init; }
    public string Street { get; init; }
    public string ZipCode { get; init; }

    public string CityName => City.Name;

    public string Formatted =>
        $"{Street}\n{City.Name}, {City.State} {ZipCode}";
}

public class Customer
{
    public string Name { get; init; }
    private Address Address { get; init; }

    public string ShippingAddress =>
        $"{Name}\n{Address.Formatted}";

    public string DeliveryCity => Address.CityName;
}

public class Order
{
    public Guid Id { get; init; }
    private Customer Customer { get; init; }
    public decimal Total { get; init; }

    public string DeliveryCity => Customer.DeliveryCity;

    public string ShippingLabel => Customer.ShippingAddress;
}

// COMPLIANT: service only talks to its direct collaborator
public class ShippingLabelService
{
    public string GenerateLabel(Order order)
    {
        // Single property access on direct collaborator
        return order.ShippingLabel;
    }
}
```

**Why compliant:** Each class exposes computed properties that encapsulate internal structure. `ShippingLabelService` only talks to `Order`. `Order` delegates to `Customer`. `Customer` delegates to `Address`. Callers are shielded from internal restructuring.

---

## ASP.NET Core Controller Example

```csharp
// VIOLATION: controller reaches through service and domain objects
[ApiController]
[Route("api/orders")]
public class OrderControllerBad : ControllerBase
{
    private readonly IOrderService _orderService;

    public OrderControllerBad(IOrderService orderService)
    {
        _orderService = orderService;
    }

    [HttpGet("{orderId}/delivery-city")]
    public async Task<IActionResult> GetDeliveryCity(Guid orderId)
    {
        var order = await _orderService.FindByIdAsync(orderId);
        // Reaching through the entire object graph from the controller
        var city = order.Customer.Address.City.Name;
        return Ok(new { city });
    }
}

// COMPLIANT: controller uses encapsulated domain property
[ApiController]
[Route("api/orders")]
public class OrderControllerGood : ControllerBase
{
    private readonly IOrderService _orderService;

    public OrderControllerGood(IOrderService orderService)
    {
        _orderService = orderService;
    }

    [HttpGet("{orderId}/delivery-city")]
    public async Task<IActionResult> GetDeliveryCity(Guid orderId)
    {
        var order = await _orderService.FindByIdAsync(orderId);
        // Only talks to direct collaborator
        return Ok(new { city = order.DeliveryCity });
    }
}

// COMPLIANT: service encapsulates domain access
public interface IOrderService
{
    Task<Order> FindByIdAsync(Guid orderId);
    Task<string> GetDeliveryCityAsync(Guid orderId);
}

public class OrderService : IOrderService
{
    private readonly IOrderRepository _orderRepository;

    public OrderService(IOrderRepository orderRepository)
    {
        _orderRepository = orderRepository;
    }

    public async Task<Order> FindByIdAsync(Guid orderId)
    {
        return await _orderRepository.GetByIdAsync(orderId)
            ?? throw new OrderNotFoundException(orderId);
    }

    public async Task<string> GetDeliveryCityAsync(Guid orderId)
    {
        var order = await FindByIdAsync(orderId);
        return order.DeliveryCity;
    }
}
```

---

## Why It Matters

The Law of Demeter reduces **coupling between components**. When code reaches through chains like `order.Customer.Address.City.Name`, it creates invisible dependencies on the internal structure of every object in that chain. This leads to:

- **Fragile code:** A structural change in any intermediate object breaks all callers
- **Hidden dependencies:** The service secretly depends on Customer, Address, and City, but only declares a dependency on Order
- **Difficult testing:** Tests must construct deep object graphs with nested mocks
- **Ripple effects:** Refactoring one entity forces changes across controllers, services, and other domain objects

---

## The Rule

A method `M` of object `O` should only call methods on:

1. **`O` itself** - the object's own methods and properties
2. **Objects passed as parameters to `M`** - direct arguments
3. **Objects created within `M`** - locally instantiated objects
4. **`O`'s direct component objects** - fields and injected dependencies

Any other access (reaching through a property to access a stranger's property) violates the law and should be refactored into a property or method on the direct collaborator.
