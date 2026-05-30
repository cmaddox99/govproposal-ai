# .NET Core Guidance

> **Purpose:** Stack-specific agent behaviors for .NET Core/C# applications.

---

## Overview

This guidance provides patterns for AI agents working with .NET Core and C# applications. It covers testing with xUnit, domain modeling patterns, and ASP.NET Core specifics.

---

## Testing Framework

**Primary Framework:** xUnit + Moq

### Test Structure

```csharp
public class OrderTests
{
    [Fact]
    public void NewOrder_ShouldHaveZeroTotal()
    {
        // Arrange
        var customerId = CustomerId.From("cust-123");

        // Act
        var order = Order.Create(customerId);

        // Assert
        Assert.Equal(Money.Zero, order.Total);
    }

    [Fact]
    public void AddItem_ShouldUpdateTotal()
    {
        // Arrange
        var order = Order.Create(CustomerId.From("cust-123"));
        var product = new Product("SKU-1", Money.From(100));

        // Act
        order.AddItem(product, quantity: 2);

        // Assert
        Assert.Equal(Money.From(200), order.Total);
    }

    [Theory]
    [InlineData(1, 100)]
    [InlineData(2, 200)]
    [InlineData(5, 500)]
    public void AddItem_WithVariousQuantities_ShouldCalculateCorrectTotal(
        int quantity, decimal expectedTotal)
    {
        // Arrange
        var order = Order.Create(CustomerId.From("cust-123"));
        var product = new Product("SKU-1", Money.From(100));

        // Act
        order.AddItem(product, quantity);

        // Assert
        Assert.Equal(expectedTotal, order.Total.Amount);
    }
}
```

### Testing Patterns

- Use `[Fact]` for single test cases
- Use `[Theory]` with `[InlineData]` for parameterized tests
- Use xUnit `Assert` for assertions — **DO NOT USE FluentAssertions** (unapproved dependency)
- Use Moq for mocking dependencies
- Separate unit tests from integration tests

---

## Domain Modeling

### Entity Pattern

```csharp
public class Order : Entity<OrderId>, IAggregateRoot
{
    private readonly List<OrderLine> _lines = new();

    public CustomerId CustomerId { get; private set; }
    public IReadOnlyList<OrderLine> Lines => _lines.AsReadOnly();
    public OrderStatus Status { get; private set; }
    public Money Total => CalculateTotal();

    private Order() { } // EF Core

    public static Order Create(CustomerId customerId)
    {
        return new Order
        {
            Id = OrderId.New(),
            CustomerId = customerId,
            Status = OrderStatus.Draft
        };
    }

    public void AddItem(Product product, int quantity)
    {
        EnsureModifiable();

        var existingLine = _lines.FirstOrDefault(l => l.ProductId == product.Id);
        if (existingLine is not null)
        {
            existingLine.IncreaseQuantity(quantity);
        }
        else
        {
            _lines.Add(OrderLine.Create(product, quantity));
        }

        AddDomainEvent(new ItemAddedToOrder(Id, product.Id, quantity));
    }

    public void Place()
    {
        if (!_lines.Any())
            throw new EmptyOrderException(Id);

        Status = OrderStatus.Placed;
        AddDomainEvent(new OrderPlaced(Id, Total));
    }

    private Money CalculateTotal() =>
        _lines.Aggregate(Money.Zero, (sum, line) => sum + line.Total);

    private void EnsureModifiable()
    {
        if (Status != OrderStatus.Draft)
            throw new OrderNotModifiableException(Id, Status);
    }
}
```

### Value Object Pattern

```csharp
public record Money
{
    public decimal Amount { get; }
    public string Currency { get; }

    private Money(decimal amount, string currency)
    {
        if (amount < 0)
            throw new ArgumentException("Amount cannot be negative", nameof(amount));

        Amount = amount;
        Currency = currency;
    }

    public static Money From(decimal amount, string currency = "USD") =>
        new(amount, currency);

    public static Money Zero => new(0, "USD");

    public static Money operator +(Money left, Money right)
    {
        EnsureSameCurrency(left, right);
        return new Money(left.Amount + right.Amount, left.Currency);
    }

    public static Money operator *(Money money, int multiplier) =>
        new(money.Amount * multiplier, money.Currency);

    private static void EnsureSameCurrency(Money left, Money right)
    {
        if (left.Currency != right.Currency)
            throw new CurrencyMismatchException(left.Currency, right.Currency);
    }
}
```

### Strongly-Typed IDs

```csharp
public readonly record struct OrderId
{
    public Guid Value { get; }

    private OrderId(Guid value) => Value = value;

    public static OrderId New() => new(Guid.NewGuid());
    public static OrderId From(Guid value) => new(value);
    public static OrderId From(string value) => new(Guid.Parse(value));

    public override string ToString() => Value.ToString();
}
```

---

## Common Patterns

### Constructor Injection

```csharp
public class OrderService
{
    private readonly IOrderRepository _orderRepository;
    private readonly IPaymentGateway _paymentGateway;
    private readonly ILogger<OrderService> _logger;

    public OrderService(
        IOrderRepository orderRepository,
        IPaymentGateway paymentGateway,
        ILogger<OrderService> logger)
    {
        _orderRepository = orderRepository;
        _paymentGateway = paymentGateway;
        _logger = logger;
    }

    public async Task<Order> PlaceOrderAsync(OrderId orderId, CancellationToken ct)
    {
        var order = await _orderRepository.GetByIdAsync(orderId, ct)
            ?? throw new OrderNotFoundException(orderId);

        order.Place();

        await _orderRepository.SaveAsync(order, ct);

        _logger.LogInformation("Order {OrderId} placed successfully", orderId);

        return order;
    }
}
```

### Repository Interface

```csharp
public interface IOrderRepository
{
    Task<Order?> GetByIdAsync(OrderId id, CancellationToken ct = default);
    Task<IReadOnlyList<Order>> GetByCustomerAsync(CustomerId customerId, CancellationToken ct = default);
    Task SaveAsync(Order order, CancellationToken ct = default);
}

// EF Core implementation
public class EfOrderRepository : IOrderRepository
{
    private readonly OrderDbContext _context;

    public EfOrderRepository(OrderDbContext context)
    {
        _context = context;
    }

    public async Task<Order?> GetByIdAsync(OrderId id, CancellationToken ct = default)
    {
        return await _context.Orders
            .Include(o => o.Lines)
            .FirstOrDefaultAsync(o => o.Id == id, ct);
    }

    public async Task SaveAsync(Order order, CancellationToken ct = default)
    {
        _context.Orders.Update(order);
        await _context.SaveChangesAsync(ct);
    }
}
```

### Minimal API Endpoint

```csharp
app.MapPost("/orders/{orderId}/place", async (
    OrderId orderId,
    IOrderService orderService,
    CancellationToken ct) =>
{
    var order = await orderService.PlaceOrderAsync(orderId, ct);
    return Results.Ok(OrderResponse.FromDomain(order));
})
.WithName("PlaceOrder")
.Produces<OrderResponse>(StatusCodes.Status200OK)
.ProducesProblem(StatusCodes.Status404NotFound);
```

---

## Anti-Patterns to Avoid

### Anemic Domain Model

```csharp
// BAD - No behavior, just properties
public class Order
{
    public Guid Id { get; set; }
    public decimal Total { get; set; }
    public string Status { get; set; }
    public List<OrderLine> Lines { get; set; }
}

// Service does all the work
public class OrderService
{
    public void AddItem(Order order, Product product, int quantity)
    {
        order.Lines.Add(new OrderLine { ProductId = product.Id, Quantity = quantity });
        order.Total = order.Lines.Sum(l => l.Price * l.Quantity);
    }
}
```

### Service Locator

```csharp
// BAD - Hidden dependencies
public class OrderService
{
    public void PlaceOrder(Guid orderId)
    {
        var repository = ServiceLocator.Get<IOrderRepository>(); // Hidden!
        var order = repository.GetById(orderId);
        // ...
    }
}
```

### Primitive Obsession

```csharp
// BAD - Primitives instead of domain types
public class Order
{
    public Guid Id { get; set; }
    public Guid CustomerId { get; set; } // Should be CustomerId
    public decimal Total { get; set; }   // Should be Money
    public string Status { get; set; }   // Should be OrderStatus enum
}
```

---

## ASP.NET Core Specific Guidance

### Exception Handling

```csharp
public class GlobalExceptionHandler : IExceptionHandler
{
    private readonly ILogger<GlobalExceptionHandler> _logger;

    public GlobalExceptionHandler(ILogger<GlobalExceptionHandler> logger)
    {
        _logger = logger;
    }

    public async ValueTask<bool> TryHandleAsync(
        HttpContext httpContext,
        Exception exception,
        CancellationToken cancellationToken)
    {
        var (statusCode, error) = exception switch
        {
            OrderNotFoundException e => (StatusCodes.Status404NotFound, "ORDER_NOT_FOUND"),
            OrderNotModifiableException e => (StatusCodes.Status409Conflict, "ORDER_NOT_MODIFIABLE"),
            _ => (StatusCodes.Status500InternalServerError, "INTERNAL_ERROR")
        };

        _logger.LogError(exception, "Request failed: {Error}", error);

        httpContext.Response.StatusCode = statusCode;
        await httpContext.Response.WriteAsJsonAsync(new { error }, cancellationToken);

        return true;
    }
}
```

### Dependency Injection Setup

```csharp
// Program.cs
var builder = WebApplication.CreateBuilder(args);

// Domain services
builder.Services.AddScoped<IOrderService, OrderService>();

// Infrastructure
builder.Services.AddScoped<IOrderRepository, EfOrderRepository>();
builder.Services.AddDbContext<OrderDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("Default")));

// Exception handling
builder.Services.AddExceptionHandler<GlobalExceptionHandler>();
builder.Services.AddProblemDetails();

var app = builder.Build();

app.UseExceptionHandler();
app.MapControllers();
app.Run();
```

### Integration Testing

```csharp
public class OrdersControllerTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient _client;

    public OrdersControllerTests(WebApplicationFactory<Program> factory)
    {
        _client = factory.WithWebHostBuilder(builder =>
        {
            builder.ConfigureServices(services =>
            {
                // Replace with test database
                services.RemoveAll<DbContextOptions<OrderDbContext>>();
                services.AddDbContext<OrderDbContext>(options =>
                    options.UseInMemoryDatabase("TestDb"));
            });
        }).CreateClient();
    }

    [Fact]
    public async Task PlaceOrder_WithValidOrder_ReturnsOk()
    {
        // Arrange
        var orderId = await CreateTestOrder();

        // Act
        var response = await _client.PostAsync($"/orders/{orderId}/place", null);

        // Assert
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
    }
}
```

---

## Tools and Commands

### Development

```bash
# Build solution
dotnet build

# Run application
dotnet run --project src/Orders.Api

# Watch mode (hot reload)
dotnet watch run --project src/Orders.Api

# Add package
dotnet add package <PackageName>
```

### Testing

```bash
# Run all tests
dotnet test

# Run with coverage
dotnet test --collect:"XPlat Code Coverage"

# Run specific test project
dotnet test tests/Orders.UnitTests

# Filter by test name
dotnet test --filter "Name~OrderTests"
```

### Code Quality

```bash
# Format code
dotnet format

# Analyze code
dotnet build --warnaserrors

# Run analyzers
dotnet build -p:EnforceCodeStyleInBuild=true
```
