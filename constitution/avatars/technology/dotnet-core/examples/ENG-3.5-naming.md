---
law_id: ENG-3.5
avatar: dotnet-core
---

# ENG-3.5: Naming Conventions for .NET Core (C#)

## Naming Convention Reference

| Element          | Convention            | Example                               |
|------------------|-----------------------|---------------------------------------|
| Classes          | PascalCase            | `OrderService`, `CargoShipment`       |
| Methods          | PascalCase            | `CalculateTotal`, `ValidateEmail`     |
| Properties       | PascalCase            | `CustomerCount`, `OrderItems`         |
| Public fields    | PascalCase            | `MaxValue`                            |
| Private fields   | _camelCase            | `_orderRepository`, `_taxCalculator`  |
| Parameters       | camelCase             | `orderId`, `customerName`             |
| Local variables  | camelCase             | `subtotal`, `itemCount`               |
| Constants        | SCREAMING_SNAKE_CASE  | `MAX_RETRY_COUNT`, `DEFAULT_TIMEOUT`  |
| Interfaces       | IPascalCase           | `IOrderRepository`, `ITaxCalculator`  |
| Enums            | PascalCase (values PascalCase) | `OrderStatus.Confirmed`      |
| Namespaces       | PascalCase            | `AA.Cargo.Domain`                     |
| Async methods    | PascalCase + Async    | `CalculateTotalAsync`                 |

---

## COMPLIANT: Idiomatic C#/.NET Naming

```csharp
// Namespace: PascalCase, dot-separated
namespace AA.Cargo.Domain;

using System;
using System.Collections.Generic;
using System.Linq;

// Constants: SCREAMING_SNAKE_CASE
public static class ShippingConstants
{
    public const int MAX_RETRY_COUNT = 3;
    public const decimal DEFAULT_TAX_RATE = 0.08m;
    public const string DEFAULT_CURRENCY = "USD";
}

// Enum: PascalCase name and values
public enum OrderStatus
{
    Pending,
    Confirmed,
    Shipped,
    Delivered
}

// Interface: IPascalCase (I prefix is idiomatic in C#)
public interface IOrderRepository
{
    Task<Order?> FindByIdAsync(Guid orderId);
    Task SaveAsync(Order order);
    Task<IReadOnlyList<Order>> FindByCustomerIdAsync(Guid customerId);
}

public interface ITaxCalculator
{
    Money CalculateTax(Money subtotal);
}

// Record: PascalCase, properties PascalCase
public readonly record struct Money(decimal Amount, string Currency)
{
    public static readonly Money Zero = new(0m, ShippingConstants.DEFAULT_CURRENCY);

    // Method: PascalCase
    public Money Add(Money other)
    {
        ValidateSameCurrency(other);
        return new Money(Amount + other.Amount, Currency);
    }

    public Money Multiply(int factor)
    {
        return new Money(Amount * factor, Currency);
    }

    // Private method: PascalCase
    private void ValidateSameCurrency(Money other)
    {
        if (Currency != other.Currency)
        {
            throw new InvalidOperationException(
                $"Cannot operate on {Currency} and {other.Currency}");
        }
    }
}

// Class: PascalCase
public record CargoShipment(
    Guid ShipmentId,            // Property: PascalCase
    string Origin,
    string Destination,
    IReadOnlyList<LineItem> Items
);

// Service class: PascalCase
public class OrderService
{
    // Private fields: _camelCase
    private readonly IOrderRepository _orderRepository;
    private readonly ITaxCalculator _taxCalculator;

    // Constructor parameters: camelCase
    public OrderService(
        IOrderRepository orderRepository,
        ITaxCalculator taxCalculator)
    {
        _orderRepository = orderRepository;
        _taxCalculator = taxCalculator;
    }

    // Property: PascalCase
    public int CustomerCount { get; private set; }

    // Public method: PascalCase
    public Money CalculateTotal(IReadOnlyList<LineItem> items)
    {
        if (items.Count == 0)
        {
            return Money.Zero;
        }

        // Local variables: camelCase
        var subtotal = SumLineItems(items);
        var tax = _taxCalculator.CalculateTax(subtotal);
        return subtotal.Add(tax);
    }

    // Async method: PascalCase + Async suffix
    public async Task<Order?> FindOrderAsync(Guid orderId)
    {
        return await _orderRepository.FindByIdAsync(orderId);
    }

    public bool ValidateEmail(string email)
    {
        // Local boolean: camelCase with is/has
        var isValidFormat = email.Contains('@');
        var hasDomain = email.Split('@').Last().Contains('.');
        return isValidFormat && hasDomain;
    }

    // Private method: PascalCase
    private Money SumLineItems(IReadOnlyList<LineItem> items)
    {
        return items.Aggregate(
            Money.Zero,
            (total, item) => total.Add(item.LineTotal));
    }
}
```

```csharp
namespace AA.Cargo.Domain.Tests;

// Test class: PascalCase with Tests suffix
public class OrderServiceTests
{
    // Private fields: _camelCase
    private readonly OrderService _orderService;
    private readonly Mock<IOrderRepository> _mockRepository;
    private readonly Mock<ITaxCalculator> _mockTaxCalculator;

    public OrderServiceTests()
    {
        _mockRepository = new Mock<IOrderRepository>();
        _mockTaxCalculator = new Mock<ITaxCalculator>();
        _orderService = new OrderService(
            _mockRepository.Object,
            _mockTaxCalculator.Object);
    }

    [Fact]
    public void CalculateTotal_ReturnsZero_WhenItemsEmpty()
    {
        // Local variable: camelCase
        var result = _orderService.CalculateTotal(Array.Empty<LineItem>());
        Assert.Equal(Money.Zero, result);
    }

    [Fact]
    public void ValidateEmail_ReturnsFalse_WhenMissingAtSign()
    {
        var isValid = _orderService.ValidateEmail("invalid-email");
        Assert.False(isValid);
    }

    [Fact]
    public async Task FindOrderAsync_ReturnsNull_WhenOrderNotFound()
    {
        // Parameters: camelCase
        var orderId = Guid.NewGuid();
        _mockRepository
            .Setup(r => r.FindByIdAsync(orderId))
            .ReturnsAsync((Order?)null);

        var result = await _orderService.FindOrderAsync(orderId);

        Assert.Null(result);
    }
}
```

**Why compliant:** Classes and methods use PascalCase. Interfaces have the `I` prefix (idiomatic in C#). Private fields use `_camelCase`. Parameters and local variables use camelCase. Properties use PascalCase. Async methods have the `Async` suffix. Constants use SCREAMING_SNAKE_CASE. Every name follows established .NET conventions.

---

## VIOLATION: Non-Idiomatic C# Naming

```csharp
// VIOLATION: Namespace should be PascalCase
namespace aa.cargo.domain;

// VIOLATION: Interface should have "I" prefix in C#
public interface OrderRepository
{
    // VIOLATION: Method should be PascalCase, not camelCase
    Task<Order?> findById(Guid orderId);
    Task save(Order order);
}

// VIOLATION: Class should be PascalCase, not snake_case
public class order_service
{
    // VIOLATION: Private fields should be _camelCase
    private readonly OrderRepository orderRepository;
    private readonly TaxCalculator taxcalculator;

    // VIOLATION: Constants should be SCREAMING_SNAKE_CASE
    private const int MaxRetryCount = 3;
    private const string defaultCurrency = "USD";

    // VIOLATION: Constructor parameter should be camelCase, not PascalCase
    public order_service(OrderRepository OrderRepository, TaxCalculator TC)
    {
        orderRepository = OrderRepository;
        taxcalculator = TC;
    }

    // VIOLATION: Property should be PascalCase, not camelCase
    public int customerCount { get; set; }

    // VIOLATION: Method should be PascalCase, not camelCase
    public Money calculateTotal(IReadOnlyList<LineItem> Items)
    {
        // VIOLATION: Parameter should be camelCase, not PascalCase
        decimal Sub_Total = 0m;
        // VIOLATION: Local variable should be camelCase, not mixed snake_case

        foreach (var Item in Items)
        {
            Sub_Total += Item.Price * Item.Quantity;
        }

        return new Money(Sub_Total, defaultCurrency);
    }

    // VIOLATION: Async method should have Async suffix
    public async Task<Order?> FindOrder(Guid order_id)
    {
        // VIOLATION: Parameter should be camelCase, not snake_case
        return await orderRepository.findById(order_id);
    }

    // VIOLATION: Method should be PascalCase, not snake_case
    public bool validate_email(string email_address)
    {
        return email_address.Contains("@");
    }
}

// VIOLATION: Enum values should be PascalCase, not SCREAMING_SNAKE
public enum OrderStatus
{
    PENDING,
    CONFIRMED,
    SHIPPED
}
```

**Why violates ENG-3.5:** This code uses camelCase for methods and properties (Java style), snake_case for class and method names (Python style), missing `I` prefix on interfaces (not idiomatic C#), private fields without `_` prefix, PascalCase parameters, snake_case local variables, and missing `Async` suffix on async methods. These violations conflict with established .NET conventions and make the codebase inconsistent for C# developers.

---

## Quick Reference

```text
Classes/Records       PascalCase          OrderService, CargoShipment
Interfaces            IPascalCase         IOrderRepository, ITaxCalculator
Methods               PascalCase          CalculateTotal()
Async Methods         PascalCase + Async  CalculateTotalAsync()
Properties            PascalCase          CustomerCount, OrderItems
Private Fields        _camelCase          _orderRepository, _cache
Parameters            camelCase           orderId, customerName
Local Variables       camelCase           subtotal, itemCount
Constants             SCREAMING_SNAKE     MAX_RETRY_COUNT
Enum Values           PascalCase          OrderStatus.Confirmed
Namespaces            PascalCase          AA.Cargo.Domain
```
