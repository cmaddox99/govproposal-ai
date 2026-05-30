---
law_id: ENG-2.1
avatar: dotnet-core
---

# ENG-2.1: Aggregate Design Examples for .NET Core

## COMPLIANT: Well-Defined Aggregate Root with Encapsulated Children

```csharp
public class Order : AggregateRoot
{
    private readonly List<OrderLine> _orderLines = new();

    public Guid Id { get; private set; }
    public CustomerId CustomerId { get; private set; }
    public OrderStatus Status { get; private set; }
    public Money TotalAmount { get; private set; }
    public DateTime CreatedAt { get; private set; }
    public DateTime? UpdatedAt { get; private set; }

    public IReadOnlyList<OrderLine> OrderLines => _orderLines.AsReadOnly();

    private Order() { } // EF Core requirement

    public static Order Create(CustomerId customerId)
    {
        return new Order
        {
            Id = Guid.NewGuid(),
            CustomerId = customerId,
            Status = OrderStatus.Draft,
            TotalAmount = Money.Zero,
            CreatedAt = DateTime.UtcNow
        };
    }

    public void AddItem(ProductId productId, int quantity, Money unitPrice)
    {
        if (Status != OrderStatus.Draft)
        {
            throw new InvalidOperationException("Cannot modify a submitted order");
        }

        var existingLine = _orderLines.FirstOrDefault(l => l.ProductId == productId);
        if (existingLine != null)
        {
            existingLine.IncreaseQuantity(quantity);
        }
        else
        {
            _orderLines.Add(new OrderLine(productId, quantity, unitPrice));
        }

        RecalculateTotal();
    }

    public void RemoveItem(ProductId productId)
    {
        if (Status != OrderStatus.Draft)
        {
            throw new InvalidOperationException("Cannot modify a submitted order");
        }

        var line = _orderLines.FirstOrDefault(l => l.ProductId == productId);
        if (line != null)
        {
            _orderLines.Remove(line);
            RecalculateTotal();
        }
    }

    public void Submit()
    {
        if (_orderLines.Count == 0)
        {
            throw new InvalidOperationException("Cannot submit an empty order");
        }
        if (Status != OrderStatus.Draft)
        {
            throw new InvalidOperationException("Order already submitted");
        }

        Status = OrderStatus.Submitted;
        UpdatedAt = DateTime.UtcNow;

        AddDomainEvent(new OrderSubmittedEvent(
            Id,
            CustomerId,
            TotalAmount,
            _orderLines.Select(l => new OrderLineSnapshot(l.ProductId, l.Quantity, l.UnitPrice)).ToList()));
    }

    public void Confirm()
    {
        if (Status != OrderStatus.Submitted)
        {
            throw new InvalidOperationException("Only submitted orders can be confirmed");
        }

        Status = OrderStatus.Confirmed;
        UpdatedAt = DateTime.UtcNow;
    }

    private void RecalculateTotal()
    {
        TotalAmount = _orderLines
            .Select(l => l.LineTotal)
            .Aggregate(Money.Zero, (acc, amount) => acc + amount);
        UpdatedAt = DateTime.UtcNow;
    }
}

public class OrderLine
{
    public Guid Id { get; private set; }
    public ProductId ProductId { get; private set; }
    public int Quantity { get; private set; }
    public Money UnitPrice { get; private set; }
    public Money LineTotal => UnitPrice * Quantity;

    private OrderLine() { } // EF Core requirement

    internal OrderLine(ProductId productId, int quantity, Money unitPrice)
    {
        if (quantity <= 0)
        {
            throw new ArgumentException("Quantity must be positive", nameof(quantity));
        }

        Id = Guid.NewGuid();
        ProductId = productId;
        Quantity = quantity;
        UnitPrice = unitPrice;
    }

    internal void IncreaseQuantity(int additionalQuantity)
    {
        if (additionalQuantity <= 0)
        {
            throw new ArgumentException("Additional quantity must be positive", nameof(additionalQuantity));
        }

        Quantity += additionalQuantity;
    }
}
```

**Why compliant:** Order is the aggregate root that controls all access to OrderLines. Business rules (status transitions, quantity validation) are enforced within the aggregate. OrderLines cannot be modified directly from outside - all changes go through Order methods. The aggregate maintains invariants (total always matches lines). The `internal` access modifier on OrderLine constructors and methods enforces the boundary.

---

## COMPLIANT: Value Objects for Domain Concepts

```csharp
public readonly record struct Money
{
    public decimal Amount { get; }
    public string Currency { get; }

    public static readonly Money Zero = new(0m, "USD");

    public Money(decimal amount, string currency)
    {
        Amount = decimal.Round(amount, 2, MidpointRounding.AwayFromZero);
        Currency = currency ?? throw new ArgumentNullException(nameof(currency));
    }

    public static Money Usd(decimal amount) => new(amount, "USD");

    public static Money operator +(Money left, Money right)
    {
        ValidateSameCurrency(left, right);
        return new Money(left.Amount + right.Amount, left.Currency);
    }

    public static Money operator -(Money left, Money right)
    {
        ValidateSameCurrency(left, right);
        return new Money(left.Amount - right.Amount, left.Currency);
    }

    public static Money operator *(Money money, int multiplier)
    {
        return new Money(money.Amount * multiplier, money.Currency);
    }

    public static bool operator >(Money left, Money right)
    {
        ValidateSameCurrency(left, right);
        return left.Amount > right.Amount;
    }

    public static bool operator <(Money left, Money right)
    {
        ValidateSameCurrency(left, right);
        return left.Amount < right.Amount;
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

public readonly record struct CustomerId
{
    public Guid Value { get; }

    public CustomerId(Guid value)
    {
        if (value == Guid.Empty)
        {
            throw new ArgumentException("Customer ID cannot be empty", nameof(value));
        }
        Value = value;
    }

    public static CustomerId New() => new(Guid.NewGuid());
    public static CustomerId From(string value) => new(Guid.Parse(value));

    public override string ToString() => Value.ToString();
}

public readonly record struct ProductId
{
    public Guid Value { get; }

    public ProductId(Guid value)
    {
        if (value == Guid.Empty)
        {
            throw new ArgumentException("Product ID cannot be empty", nameof(value));
        }
        Value = value;
    }

    public static ProductId From(string value) => new(Guid.Parse(value));

    public override string ToString() => Value.ToString();
}
```

**Why compliant:** Value objects encapsulate domain concepts with validation and behavior. They are immutable (record struct) ensuring thread safety and value semantics. Currency mismatch is caught at the domain level. Typed IDs prevent mixing CustomerId with ProductId accidentally. Using `record struct` minimizes heap allocations.

---

## VIOLATION: Anemic Domain Model with Exposed Setters

```csharp
public class Order
{
    public long Id { get; set; }
    public long CustomerId { get; set; }
    public string Status { get; set; } = "DRAFT";
    public List<OrderLine> OrderLines { get; set; } = new();
    public decimal TotalAmount { get; set; }
    public DateTime CreatedAt { get; set; }
}

public class OrderLine
{
    public long Id { get; set; }
    public Order Order { get; set; } = null!;
    public long ProductId { get; set; }
    public int Quantity { get; set; }
    public decimal UnitPrice { get; set; }
    public decimal LineTotal { get; set; }
}

// Service that should be in the domain
public class OrderService
{
    private readonly IOrderRepository _orderRepository;
    private readonly IOrderLineRepository _orderLineRepository;

    public OrderService(IOrderRepository orderRepository, IOrderLineRepository orderLineRepository)
    {
        _orderRepository = orderRepository;
        _orderLineRepository = orderLineRepository;
    }

    public async Task AddItemToOrderAsync(long orderId, long productId, int quantity, decimal price)
    {
        var order = await _orderRepository.GetByIdAsync(orderId)
            ?? throw new NotFoundException();

        // Business logic scattered in service
        if (order.Status != "DRAFT")
        {
            throw new InvalidOperationException("Cannot modify submitted order");
        }

        var line = new OrderLine
        {
            Order = order,
            ProductId = productId,
            Quantity = quantity,
            UnitPrice = price,
            LineTotal = price * quantity
        };

        order.OrderLines.Add(line);

        // Recalculate total in service
        order.TotalAmount = order.OrderLines.Sum(l => l.LineTotal);

        await _orderRepository.SaveAsync(order);
    }

    public async Task SubmitOrderAsync(long orderId)
    {
        var order = await _orderRepository.GetByIdAsync(orderId)
            ?? throw new NotFoundException();

        // Validation logic in service
        if (order.OrderLines.Count == 0)
        {
            throw new InvalidOperationException("Cannot submit empty order");
        }

        order.Status = "SUBMITTED"; // String-based status, no type safety
        await _orderRepository.SaveAsync(order);
    }
}
```

**Why violates ENG-2.1:** The domain model is anemic - entities are just data holders with public setters. All business logic lives in services, not the aggregate. OrderLines can be directly accessed and modified, bypassing aggregate rules. No invariants are enforced by the entities themselves. Status is a string rather than an enum, allowing invalid values.

---

## VIOLATION: Breaking Aggregate Boundaries

```csharp
public class ReportingService
{
    private readonly IOrderLineRepository _orderLineRepository; // Direct access to child entity!

    public ReportingService(IOrderLineRepository orderLineRepository)
    {
        _orderLineRepository = orderLineRepository;
    }

    public async Task<List<TopSellingProduct>> GetTopSellingProductsAsync(DateTime from, DateTime to)
    {
        // Directly querying and modifying order lines without going through Order
        var lines = await _orderLineRepository.GetByDateRangeAsync(from, to);

        // Worse: modifying child entities directly
        foreach (var line in lines)
        {
            line.ReportedAt = DateTime.UtcNow; // Bypasses Order aggregate
            await _orderLineRepository.SaveAsync(line);
        }

        return lines
            .GroupBy(l => l.ProductId)
            .Select(g => new TopSellingProduct(g.Key, g.Sum(l => l.Quantity)))
            .OrderByDescending(p => p.TotalSold)
            .Take(10)
            .ToList();
    }
}

// Repository that shouldn't exist for non-aggregate-roots
public interface IOrderLineRepository
{
    Task<List<OrderLine>> GetByDateRangeAsync(DateTime from, DateTime to);
    Task SaveAsync(OrderLine orderLine);
}
```

**Why violates ENG-2.1:** IOrderLineRepository allows direct access to aggregate children. Modifying OrderLines without going through the Order aggregate bypasses business rules. The aggregate root loses control over its invariants. If Order has rules about line modifications, they are easily circumvented.

---

## COMPLIANT: Repository Only for Aggregate Root

```csharp
public interface IOrderRepository
{
    Task<Order?> GetByIdAsync(Guid id, CancellationToken cancellationToken = default);
    Task<Order?> GetByIdAndCustomerAsync(Guid id, CustomerId customerId, CancellationToken cancellationToken = default);
    Task<PagedResult<Order>> GetByCustomerIdAsync(CustomerId customerId, int pageNumber, int pageSize, CancellationToken cancellationToken = default);
    Task AddAsync(Order order, CancellationToken cancellationToken = default);
    Task SaveChangesAsync(CancellationToken cancellationToken = default);
}

public class OrderRepository : IOrderRepository
{
    private readonly OrderDbContext _context;

    public OrderRepository(OrderDbContext context)
    {
        _context = context;
    }

    public async Task<Order?> GetByIdAsync(Guid id, CancellationToken cancellationToken = default)
    {
        return await _context.Orders
            .Include(o => o.OrderLines) // Load children with aggregate
            .FirstOrDefaultAsync(o => o.Id == id, cancellationToken);
    }

    public async Task<Order?> GetByIdAndCustomerAsync(Guid id, CustomerId customerId, CancellationToken cancellationToken = default)
    {
        return await _context.Orders
            .Include(o => o.OrderLines)
            .FirstOrDefaultAsync(o => o.Id == id && o.CustomerId == customerId, cancellationToken);
    }

    public async Task<PagedResult<Order>> GetByCustomerIdAsync(CustomerId customerId, int pageNumber, int pageSize, CancellationToken cancellationToken = default)
    {
        var query = _context.Orders
            .Include(o => o.OrderLines)
            .Where(o => o.CustomerId == customerId)
            .OrderByDescending(o => o.CreatedAt);

        return await query.ToPagedResultAsync(pageNumber, pageSize, cancellationToken);
    }

    public async Task AddAsync(Order order, CancellationToken cancellationToken = default)
    {
        await _context.Orders.AddAsync(order, cancellationToken);
    }

    public async Task SaveChangesAsync(CancellationToken cancellationToken = default)
    {
        await _context.SaveChangesAsync(cancellationToken);
    }
}

// For complex reporting needs, use a separate read model with raw SQL
public class OrderReportingService
{
    private readonly IDbConnection _connection;

    public OrderReportingService(IDbConnection connection)
    {
        _connection = connection;
    }

    public async Task<List<TopSellingProduct>> GetTopSellingProductsAsync(DateTime from, DateTime to)
    {
        const string sql = """
            SELECT ol.product_id AS ProductId, SUM(ol.quantity) AS TotalSold
            FROM order_lines ol
            INNER JOIN orders o ON ol.order_id = o.id
            WHERE o.created_at BETWEEN @From AND @To
              AND o.status IN ('Confirmed', 'Shipped', 'Delivered')
            GROUP BY ol.product_id
            ORDER BY TotalSold DESC
            LIMIT 10
            """;

        var results = await _connection.QueryAsync<TopSellingProduct>(sql, new { From = from, To = to });
        return results.ToList();
    }
}
```

**Why compliant:** Only the aggregate root (Order) has a repository. Reporting uses direct SQL queries that do not modify data. The aggregate boundary is respected for all write operations. Read models can query denormalized data without affecting aggregate invariants.

---

## COMPLIANT: Domain Events from Aggregate

```csharp
public abstract class AggregateRoot
{
    private readonly List<IDomainEvent> _domainEvents = new();
    public IReadOnlyList<IDomainEvent> DomainEvents => _domainEvents.AsReadOnly();

    protected void AddDomainEvent(IDomainEvent domainEvent)
    {
        _domainEvents.Add(domainEvent);
    }

    public void ClearDomainEvents()
    {
        _domainEvents.Clear();
    }
}

public class Order : AggregateRoot
{
    // ... fields and methods as before ...

    public void Submit()
    {
        if (_orderLines.Count == 0)
        {
            throw new InvalidOperationException("Cannot submit an empty order");
        }
        if (Status != OrderStatus.Draft)
        {
            throw new InvalidOperationException("Order already submitted");
        }

        Status = OrderStatus.Submitted;
        UpdatedAt = DateTime.UtcNow;

        // Register domain event
        AddDomainEvent(new OrderSubmittedEvent(
            Id,
            CustomerId,
            TotalAmount,
            _orderLines.Select(l => new OrderLineSnapshot(l.ProductId, l.Quantity, l.UnitPrice)).ToList()));
    }

    public void Cancel(string reason)
    {
        if (!CanBeCancelled())
        {
            throw new InvalidOperationException($"Order cannot be cancelled in status: {Status}");
        }

        Status = OrderStatus.Cancelled;
        UpdatedAt = DateTime.UtcNow;

        AddDomainEvent(new OrderCancelledEvent(Id, CustomerId, reason));
    }

    private bool CanBeCancelled() => Status is OrderStatus.Draft or OrderStatus.Submitted;
}

public record OrderSubmittedEvent(
    Guid OrderId,
    CustomerId CustomerId,
    Money TotalAmount,
    IReadOnlyList<OrderLineSnapshot> Lines) : IDomainEvent;

public record OrderLineSnapshot(ProductId ProductId, int Quantity, Money UnitPrice);

public record OrderCancelledEvent(Guid OrderId, CustomerId CustomerId, string Reason) : IDomainEvent;

// Event dispatcher that publishes events after SaveChanges
public class DomainEventDispatcher
{
    private readonly IMediator _mediator;

    public DomainEventDispatcher(IMediator mediator)
    {
        _mediator = mediator;
    }

    public async Task DispatchEventsAsync(OrderDbContext context)
    {
        var aggregatesWithEvents = context.ChangeTracker
            .Entries<AggregateRoot>()
            .Where(e => e.Entity.DomainEvents.Any())
            .Select(e => e.Entity)
            .ToList();

        var domainEvents = aggregatesWithEvents
            .SelectMany(a => a.DomainEvents)
            .ToList();

        aggregatesWithEvents.ForEach(a => a.ClearDomainEvents());

        foreach (var domainEvent in domainEvents)
        {
            await _mediator.Publish(domainEvent);
        }
    }
}

// Event handlers
public class OrderSubmittedEventHandler : INotificationHandler<OrderSubmittedEvent>
{
    private readonly IInventoryService _inventoryService;
    private readonly INotificationService _notificationService;

    public OrderSubmittedEventHandler(
        IInventoryService inventoryService,
        INotificationService notificationService)
    {
        _inventoryService = inventoryService;
        _notificationService = notificationService;
    }

    public async Task Handle(OrderSubmittedEvent notification, CancellationToken cancellationToken)
    {
        await _inventoryService.ReserveStockAsync(notification.Lines);
        await _notificationService.SendOrderConfirmationAsync(notification.CustomerId, notification.OrderId);
    }
}
```

**Why compliant:** Domain events are raised by the aggregate when significant state changes occur. Events contain immutable snapshots, not entity references. Event handlers run after the aggregate is persisted. Cross-aggregate communication happens through events, not direct calls. MediatR provides clean publish/subscribe pattern.

---

## COMPLIANT: EF Core Configuration for Aggregates

```csharp
public class OrderConfiguration : IEntityTypeConfiguration<Order>
{
    public void Configure(EntityTypeBuilder<Order> builder)
    {
        builder.ToTable("orders");

        builder.HasKey(o => o.Id);

        builder.Property(o => o.Id)
            .HasColumnName("id")
            .ValueGeneratedNever();

        builder.Property(o => o.CustomerId)
            .HasColumnName("customer_id")
            .HasConversion(
                v => v.Value,
                v => new CustomerId(v));

        builder.Property(o => o.Status)
            .HasColumnName("status")
            .HasConversion<string>();

        builder.OwnsOne(o => o.TotalAmount, money =>
        {
            money.Property(m => m.Amount).HasColumnName("total_amount");
            money.Property(m => m.Currency).HasColumnName("currency");
        });

        builder.Property(o => o.CreatedAt).HasColumnName("created_at");
        builder.Property(o => o.UpdatedAt).HasColumnName("updated_at");

        // Configure owned collection - OrderLines are part of Order aggregate
        builder.OwnsMany(o => o.OrderLines, line =>
        {
            line.ToTable("order_lines");

            line.WithOwner().HasForeignKey("order_id");

            line.HasKey(l => l.Id);
            line.Property(l => l.Id).HasColumnName("id").ValueGeneratedNever();

            line.Property(l => l.ProductId)
                .HasColumnName("product_id")
                .HasConversion(v => v.Value, v => new ProductId(v));

            line.Property(l => l.Quantity).HasColumnName("quantity");

            line.OwnsOne(l => l.UnitPrice, money =>
            {
                money.Property(m => m.Amount).HasColumnName("unit_price");
                money.Property(m => m.Currency).HasColumnName("currency");
            });
        });

        // Ignore domain events - they're not persisted
        builder.Ignore(o => o.DomainEvents);
    }
}
```

**Why compliant:** EF Core configuration enforces aggregate boundaries at the persistence level. `OwnsMany` ensures OrderLines are always loaded and saved with their parent Order. Value objects (Money, CustomerId, ProductId) are properly converted. The configuration keeps persistence concerns out of domain entities.
