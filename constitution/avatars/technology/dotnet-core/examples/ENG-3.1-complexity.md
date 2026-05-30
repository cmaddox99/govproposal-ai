---
law_id: ENG-3.1
avatar: dotnet-core
---

# ENG-3.1: Complexity Management Examples for .NET Core

## COMPLIANT: Single Responsibility with Strategy Pattern

```csharp
public interface IPaymentStrategy
{
    Task<PaymentResult> ProcessAsync(PaymentRequest request);
    bool Supports(PaymentMethod method);
}

public class CreditCardPaymentStrategy : IPaymentStrategy
{
    private readonly ICreditCardGateway _gateway;
    private readonly IFraudDetectionService _fraudService;

    public CreditCardPaymentStrategy(
        ICreditCardGateway gateway,
        IFraudDetectionService fraudService)
    {
        _gateway = gateway;
        _fraudService = fraudService;
    }

    public async Task<PaymentResult> ProcessAsync(PaymentRequest request)
    {
        await _fraudService.ValidateTransactionAsync(request);
        return await _gateway.ChargeAsync(request.Amount, request.CardDetails);
    }

    public bool Supports(PaymentMethod method) => method == PaymentMethod.CreditCard;
}

public class PayPalPaymentStrategy : IPaymentStrategy
{
    private readonly IPayPalClient _client;

    public PayPalPaymentStrategy(IPayPalClient client)
    {
        _client = client;
    }

    public async Task<PaymentResult> ProcessAsync(PaymentRequest request)
    {
        return await _client.ExecutePaymentAsync(request.PayPalPaymentId);
    }

    public bool Supports(PaymentMethod method) => method == PaymentMethod.PayPal;
}

public class PaymentService
{
    private readonly IEnumerable<IPaymentStrategy> _strategies;
    private readonly IPaymentRepository _repository;
    private readonly IEventPublisher _eventPublisher;

    public PaymentService(
        IEnumerable<IPaymentStrategy> strategies,
        IPaymentRepository repository,
        IEventPublisher eventPublisher)
    {
        _strategies = strategies;
        _repository = repository;
        _eventPublisher = eventPublisher;
    }

    public async Task<PaymentResult> ProcessPaymentAsync(PaymentRequest request)
    {
        var strategy = _strategies.FirstOrDefault(s => s.Supports(request.PaymentMethod))
            ?? throw new UnsupportedPaymentMethodException(request.PaymentMethod);

        var result = await strategy.ProcessAsync(request);

        if (result.IsSuccessful)
        {
            await _repository.SaveAsync(result.ToEntity());
            await _eventPublisher.PublishAsync(new PaymentCompletedEvent(result));
        }

        return result;
    }
}

// DI Registration in Program.cs
builder.Services.AddScoped<IPaymentStrategy, CreditCardPaymentStrategy>();
builder.Services.AddScoped<IPaymentStrategy, PayPalPaymentStrategy>();
builder.Services.AddScoped<PaymentService>();
```

**Why compliant:** Each class has a single responsibility. PaymentService orchestrates, strategies handle specific payment types. New payment methods require only adding a new strategy class - no modification to existing code (Open/Closed Principle). Cyclomatic complexity stays low in each component.

---

## COMPLIANT: Readable Method with Early Returns and Guard Clauses

```csharp
public class OrderValidationService
{
    private readonly IInventoryService _inventoryService;

    public OrderValidationService(IInventoryService inventoryService)
    {
        _inventoryService = inventoryService;
    }

    public async Task<ValidationResult> ValidateOrderAsync(Order? order)
    {
        if (order is null)
        {
            return ValidationResult.Failure("Order cannot be null");
        }

        if (order.Items.Count == 0)
        {
            return ValidationResult.Failure("Order must contain at least one item");
        }

        if (order.CustomerId == Guid.Empty)
        {
            return ValidationResult.Failure("Customer ID is required");
        }

        var itemValidation = ValidateItems(order.Items);
        if (itemValidation.HasErrors)
        {
            return itemValidation;
        }

        var inventoryValidation = await ValidateInventoryAsync(order.Items);
        if (inventoryValidation.HasErrors)
        {
            return inventoryValidation;
        }

        return ValidationResult.Success();
    }

    private ValidationResult ValidateItems(IReadOnlyList<OrderItem> items)
    {
        var errors = items
            .Where(item => item.Quantity <= 0)
            .Select(item => $"Invalid quantity for product: {item.ProductId}")
            .ToList();

        return errors.Count == 0
            ? ValidationResult.Success()
            : ValidationResult.Failure(errors);
    }

    private async Task<ValidationResult> ValidateInventoryAsync(IReadOnlyList<OrderItem> items)
    {
        return await _inventoryService.CheckAvailabilityAsync(items);
    }
}
```

**Why compliant:** Early returns reduce nesting and make the validation flow clear. Each validation concern is separated into its own method. The main method reads like a checklist. Cyclomatic complexity is distributed across focused methods.

---

## VIOLATION: God Class with Mixed Responsibilities

```csharp
public class OrderManager
{
    private readonly string _connectionString;
    private readonly SmtpClient _smtpClient;
    private readonly HttpClient _httpClient;

    public OrderManager(IConfiguration config)
    {
        _connectionString = config.GetConnectionString("Default")!;
        _smtpClient = new SmtpClient("smtp.example.com");
        _httpClient = new HttpClient();
    }

    public async Task<Order> CreateOrderAsync(OrderRequest request)
    {
        // Validation logic mixed in
        if (request.Items == null || request.Items.Count == 0)
        {
            throw new ValidationException("Items required");
        }
        foreach (var item in request.Items)
        {
            if (item.Quantity <= 0)
            {
                throw new ValidationException("Invalid quantity");
            }
            if (item.Price <= 0)
            {
                throw new ValidationException("Invalid price");
            }
        }

        // Direct database access with raw SQL
        var orderId = Guid.NewGuid();
        await using var connection = new SqlConnection(_connectionString);
        await connection.OpenAsync();

        await using var transaction = await connection.BeginTransactionAsync();

        await connection.ExecuteAsync(
            @"INSERT INTO Orders (Id, CustomerId, Status, CreatedAt)
              VALUES (@Id, @CustomerId, @Status, @CreatedAt)",
            new { Id = orderId, request.CustomerId, Status = "CREATED", CreatedAt = DateTime.UtcNow },
            transaction);

        foreach (var item in request.Items)
        {
            await connection.ExecuteAsync(
                @"INSERT INTO OrderItems (OrderId, ProductId, Quantity, Price)
                  VALUES (@OrderId, @ProductId, @Quantity, @Price)",
                new { OrderId = orderId, item.ProductId, item.Quantity, item.Price },
                transaction);
        }

        // Inventory check via HTTP
        var productIds = string.Join(",", request.Items.Select(i => i.ProductId));
        var inventoryResponse = await _httpClient.GetFromJsonAsync<InventoryResponse>(
            $"http://inventory-service/check?productIds={productIds}");

        if (inventoryResponse?.IsAvailable != true)
        {
            await transaction.RollbackAsync();
            throw new InventoryException("Insufficient stock");
        }

        await transaction.CommitAsync();

        // Email sending logic
        try
        {
            var message = new MailMessage
            {
                From = new MailAddress("orders@example.com"),
                Subject = $"Order Confirmation #{orderId}",
                Body = BuildEmailBody(request, orderId),
                IsBodyHtml = true
            };
            message.To.Add(request.CustomerEmail);
            await _smtpClient.SendMailAsync(message);
        }
        catch
        {
            // Swallowed exception - order continues anyway
        }

        // Logging directly
        Console.WriteLine($"Order created: {orderId}");

        // Building response with inline calculation
        var total = request.Items.Sum(i => i.Price * i.Quantity);
        var tax = total * 0.08m;
        var shipping = total > 50 ? 0m : 5.99m;

        return new Order(orderId, request.CustomerId, total + tax + shipping);
    }

    private string BuildEmailBody(OrderRequest request, Guid orderId)
    {
        // 200+ lines of HTML template building...
        return "<html>...</html>";
    }

    // 30+ more methods covering reporting, analytics, refunds, etc.
}
```

**Why violates ENG-3.1:** This class handles validation, persistence, HTTP calls, email sending, logging, and price calculation. It has direct dependencies on infrastructure (SqlConnection, SmtpClient, HttpClient). Changes to email templates require modifying this class. Testing requires complex setup. The CreateOrderAsync method alone has cyclomatic complexity > 15.

---

## VIOLATION: Deeply Nested Conditionals

```csharp
public class ShippingCalculator
{
    public ShippingQuote CalculateShipping(ShippingRequest? request)
    {
        decimal cost = 0m;

        if (request != null)
        {
            if (request.Destination != null)
            {
                if (request.Destination.Country != null)
                {
                    if (request.Destination.Country == "US")
                    {
                        if (request.Weight.HasValue)
                        {
                            if (request.Weight <= 1.0)
                            {
                                if (request.IsExpedited)
                                {
                                    cost = 12.99m;
                                }
                                else
                                {
                                    if (request.Destination.IsRural)
                                    {
                                        cost = 7.99m;
                                    }
                                    else
                                    {
                                        cost = 5.99m;
                                    }
                                }
                            }
                            else if (request.Weight <= 5.0)
                            {
                                if (request.IsExpedited)
                                {
                                    cost = 24.99m;
                                }
                                else
                                {
                                    if (request.Destination.IsRural)
                                    {
                                        cost = 14.99m;
                                    }
                                    else
                                    {
                                        cost = 9.99m;
                                    }
                                }
                            }
                            else
                            {
                                // Even more nesting for heavy packages...
                            }
                        }
                    }
                    else if (request.Destination.Country == "CA")
                    {
                        // Similar deep nesting for Canada...
                    }
                    else
                    {
                        // International shipping nesting...
                    }
                }
            }
        }

        return new ShippingQuote(cost);
    }
}
```

**Why violates ENG-3.1:** Seven levels of nesting make this nearly impossible to understand or maintain. The cyclomatic complexity exceeds 20. Adding a new country or weight tier requires navigating the maze. This should be decomposed using lookup tables, strategy pattern, or a rules engine.

---

## COMPLIANT: Decomposed Shipping with Lookup Tables

```csharp
public class ShippingCalculator
{
    private readonly IShippingRateRepository _rateRepository;
    private readonly IShippingZoneResolver _zoneResolver;

    public ShippingCalculator(
        IShippingRateRepository rateRepository,
        IShippingZoneResolver zoneResolver)
    {
        _rateRepository = rateRepository;
        _zoneResolver = zoneResolver;
    }

    public async Task<ShippingQuote> CalculateShippingAsync(ShippingRequest request)
    {
        ValidateRequest(request);

        var zone = _zoneResolver.ResolveZone(request.Destination);
        var weightTier = WeightTier.FromWeight(request.Weight!.Value);
        var serviceLevel = request.IsExpedited ? ServiceLevel.Express : ServiceLevel.Standard;

        var rate = await _rateRepository.GetRateAsync(zone, weightTier, serviceLevel)
            ?? throw new ShippingNotAvailableException(zone, weightTier);

        return new ShippingQuote
        {
            BaseCost = rate.BaseCost,
            RuralSurcharge = CalculateRuralSurcharge(request.Destination, rate),
            EstimatedDays = rate.EstimatedDays
        };
    }

    private static void ValidateRequest(ShippingRequest request)
    {
        ArgumentNullException.ThrowIfNull(request);
        ArgumentNullException.ThrowIfNull(request.Destination);

        if (!request.Weight.HasValue)
        {
            throw new ArgumentException("Weight is required", nameof(request));
        }
    }

    private static decimal CalculateRuralSurcharge(Address destination, ShippingRate rate)
    {
        return destination.IsRural ? rate.RuralSurcharge : 0m;
    }
}

public enum WeightTier
{
    Light,
    Medium,
    Heavy,
    Freight
}

public static class WeightTierExtensions
{
    private static readonly (double Min, double Max, WeightTier Tier)[] Tiers =
    {
        (0, 1.0, WeightTier.Light),
        (1.0, 5.0, WeightTier.Medium),
        (5.0, 20.0, WeightTier.Heavy),
        (20.0, double.MaxValue, WeightTier.Freight)
    };

    public static WeightTier FromWeight(double weight)
    {
        return Tiers
            .FirstOrDefault(t => weight > t.Min && weight <= t.Max)
            .Tier;
    }
}
```

**Why compliant:** Logic is flat with minimal nesting. Rates are stored in a repository rather than hardcoded conditionals. Extension methods encapsulate weight tier logic. Each method has a single responsibility and low cyclomatic complexity. Adding new zones or tiers requires only database entries, not code changes.

---

## COMPLIANT: Using Records for Immutable Data Transfer

```csharp
public record OrderSummary(
    Guid OrderId,
    string CustomerName,
    IReadOnlyList<LineItemSummary> Items,
    Money Subtotal,
    Money Tax,
    Money Total,
    OrderStatus Status,
    DateTime CreatedAt)
{
    public static OrderSummary FromOrder(Order order, ITaxCalculator taxCalculator)
    {
        var subtotal = order.CalculateSubtotal();
        var tax = taxCalculator.Calculate(subtotal, order.ShippingAddress);

        return new OrderSummary(
            order.Id,
            order.Customer.FullName,
            order.Items.Select(LineItemSummary.From).ToList(),
            subtotal,
            tax,
            subtotal + tax,
            order.Status,
            order.CreatedAt);
    }
}

public record LineItemSummary(
    string ProductName,
    int Quantity,
    Money UnitPrice,
    Money LineTotal)
{
    public static LineItemSummary From(OrderItem item)
    {
        return new LineItemSummary(
            item.Product.Name,
            item.Quantity,
            item.UnitPrice,
            item.CalculateLineTotal());
    }
}

public readonly record struct Money(decimal Amount, string Currency)
{
    public static readonly Money Zero = new(0m, "USD");

    public static Money Usd(decimal amount) => new(amount, "USD");

    public static Money operator +(Money left, Money right)
    {
        ValidateSameCurrency(left, right);
        return new Money(left.Amount + right.Amount, left.Currency);
    }

    public static Money operator *(Money money, int multiplier)
    {
        return new Money(money.Amount * multiplier, money.Currency);
    }

    private static void ValidateSameCurrency(Money left, Money right)
    {
        if (left.Currency != right.Currency)
        {
            throw new InvalidOperationException(
                $"Cannot operate on different currencies: {left.Currency} vs {right.Currency}");
        }
    }
}
```

**Why compliant:** Records eliminate boilerplate (equality, GetHashCode, ToString). Immutability prevents accidental state changes. Factory methods encapsulate construction logic. Each record has a focused purpose as a data carrier. The `record struct` for Money provides value semantics with minimal allocation.

---

## COMPLIANT: Extension Methods for Cross-Cutting Concerns

```csharp
public static class QueryableExtensions
{
    public static async Task<PagedResult<T>> ToPagedResultAsync<T>(
        this IQueryable<T> query,
        int pageNumber,
        int pageSize,
        CancellationToken cancellationToken = default)
    {
        var totalCount = await query.CountAsync(cancellationToken);
        var items = await query
            .Skip((pageNumber - 1) * pageSize)
            .Take(pageSize)
            .ToListAsync(cancellationToken);

        return new PagedResult<T>(items, totalCount, pageNumber, pageSize);
    }

    public static IQueryable<T> ApplySpecification<T>(
        this IQueryable<T> query,
        ISpecification<T> specification) where T : class
    {
        query = specification.Criteria.Aggregate(query, (current, criteria) => current.Where(criteria));

        query = specification.Includes.Aggregate(query, (current, include) => current.Include(include));

        if (specification.OrderBy != null)
        {
            query = query.OrderBy(specification.OrderBy);
        }
        else if (specification.OrderByDescending != null)
        {
            query = query.OrderByDescending(specification.OrderByDescending);
        }

        return query;
    }
}

public record PagedResult<T>(
    IReadOnlyList<T> Items,
    int TotalCount,
    int PageNumber,
    int PageSize)
{
    public int TotalPages => (int)Math.Ceiling(TotalCount / (double)PageSize);
    public bool HasPreviousPage => PageNumber > 1;
    public bool HasNextPage => PageNumber < TotalPages;
}
```

**Why compliant:** Extension methods provide reusable, composable functionality without cluttering domain classes. The specification pattern allows complex query composition while keeping individual components simple. PagedResult encapsulates pagination logic in a single, testable location.
