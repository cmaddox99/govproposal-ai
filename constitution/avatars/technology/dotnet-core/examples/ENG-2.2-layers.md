---
law_id: ENG-2.2
avatar: dotnet-core
---

# ENG-2.2: Layered Architecture Examples for .NET Core

## COMPLIANT: Clean Architecture with Controller-Service-Repository

```csharp
// === PRESENTATION LAYER: Controllers handle HTTP only ===

// Api/Controllers/OrderController.cs
[ApiController]
[Route("api/[controller]")]
public class OrderController : ControllerBase
{
    private readonly IOrderApplicationService _orderService;

    public OrderController(IOrderApplicationService orderService)
    {
        _orderService = orderService;
    }

    [HttpPost]
    [ProducesResponseType(typeof(OrderResponse), StatusCodes.Status201Created)]
    public async Task<IActionResult> CreateOrder(
        [FromBody] CreateOrderRequest request,
        CancellationToken cancellationToken)
    {
        var order = await _orderService.CreateOrderAsync(
            new CustomerId(request.CustomerId),
            request.Items.Select(i => new LineItemCommand(
                new ProductId(i.ProductId),
                i.Quantity,
                Money.Usd(i.UnitPrice))).ToList(),
            cancellationToken);

        return CreatedAtAction(
            nameof(GetOrder),
            new { id = order.Id },
            OrderResponse.FromDomain(order));
    }

    [HttpGet("{id:guid}")]
    public async Task<IActionResult> GetOrder(Guid id, CancellationToken cancellationToken)
    {
        var order = await _orderService.GetByIdAsync(id, cancellationToken);
        return order is null ? NotFound() : Ok(OrderResponse.FromDomain(order));
    }

    [HttpPut("{id:guid}/submit")]
    public async Task<IActionResult> SubmitOrder(Guid id, CancellationToken cancellationToken)
    {
        var order = await _orderService.SubmitOrderAsync(id, cancellationToken);
        return Ok(OrderResponse.FromDomain(order));
    }
}

// Api/DTOs/CreateOrderRequest.cs
public record CreateOrderRequest(
    [Required] Guid CustomerId,
    [Required, MinLength(1)] List<LineItemRequest> Items);

public record LineItemRequest(
    [Required] Guid ProductId,
    [Range(1, int.MaxValue)] int Quantity,
    [Range(0.01, double.MaxValue)] decimal UnitPrice);

public record OrderResponse(
    Guid Id,
    Guid CustomerId,
    string Status,
    decimal TotalAmount,
    List<LineItemResponse> Items,
    DateTime CreatedAt)
{
    public static OrderResponse FromDomain(Order order) => new(
        order.Id,
        order.CustomerId.Value,
        order.Status.ToString(),
        order.TotalAmount.Amount,
        order.OrderLines.Select(l => new LineItemResponse(
            l.ProductId.Value, l.Quantity, l.UnitPrice.Amount)).ToList(),
        order.CreatedAt);
}


// === APPLICATION LAYER: Services orchestrate use cases ===

// Application/Services/OrderApplicationService.cs
public interface IOrderApplicationService
{
    Task<Order> CreateOrderAsync(
        CustomerId customerId,
        List<LineItemCommand> items,
        CancellationToken cancellationToken);
    Task<Order> SubmitOrderAsync(Guid orderId, CancellationToken cancellationToken);
    Task<Order?> GetByIdAsync(Guid orderId, CancellationToken cancellationToken);
}

public class OrderApplicationService : IOrderApplicationService
{
    private readonly IOrderRepository _repository;
    private readonly IInventoryClient _inventoryClient;
    private readonly IMediator _mediator;

    public OrderApplicationService(
        IOrderRepository repository,
        IInventoryClient inventoryClient,
        IMediator mediator)
    {
        _repository = repository;
        _inventoryClient = inventoryClient;
        _mediator = mediator;
    }

    public async Task<Order> CreateOrderAsync(
        CustomerId customerId,
        List<LineItemCommand> items,
        CancellationToken cancellationToken)
    {
        var order = Order.Create(customerId);

        foreach (var item in items)
        {
            order.AddItem(item.ProductId, item.Quantity, item.UnitPrice);
        }

        await _repository.AddAsync(order, cancellationToken);
        await _repository.SaveChangesAsync(cancellationToken);

        return order;
    }

    public async Task<Order> SubmitOrderAsync(Guid orderId, CancellationToken cancellationToken)
    {
        var order = await _repository.GetByIdAsync(orderId, cancellationToken)
            ?? throw new OrderNotFoundException(orderId);

        order.Submit();

        await _inventoryClient.ReserveStockAsync(order.OrderLines, cancellationToken);
        await _repository.SaveChangesAsync(cancellationToken);

        foreach (var domainEvent in order.DomainEvents)
        {
            await _mediator.Publish(domainEvent, cancellationToken);
        }
        order.ClearDomainEvents();

        return order;
    }

    public async Task<Order?> GetByIdAsync(Guid orderId, CancellationToken cancellationToken)
    {
        return await _repository.GetByIdAsync(orderId, cancellationToken);
    }
}


// === DOMAIN LAYER: Entities enforce business rules ===

// Domain/Models/Order.cs
public class Order : AggregateRoot
{
    private readonly List<OrderLine> _orderLines = new();

    public Guid Id { get; private set; }
    public CustomerId CustomerId { get; private set; }
    public OrderStatus Status { get; private set; }
    public Money TotalAmount { get; private set; }
    public IReadOnlyList<OrderLine> OrderLines => _orderLines.AsReadOnly();
    public DateTime CreatedAt { get; private set; }

    private Order() { }

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
            throw new InvalidOperationException("Cannot modify a submitted order");

        _orderLines.Add(new OrderLine(productId, quantity, unitPrice));
        RecalculateTotal();
    }

    public void Submit()
    {
        if (_orderLines.Count == 0)
            throw new InvalidOperationException("Cannot submit an empty order");
        if (Status != OrderStatus.Draft)
            throw new InvalidOperationException("Order already submitted");

        Status = OrderStatus.Submitted;
        AddDomainEvent(new OrderSubmittedEvent(Id, CustomerId, TotalAmount));
    }

    private void RecalculateTotal()
    {
        TotalAmount = _orderLines
            .Select(l => l.LineTotal)
            .Aggregate(Money.Zero, (acc, amount) => acc + amount);
    }
}

// Domain/Ports/IOrderRepository.cs (interface in domain)
public interface IOrderRepository
{
    Task<Order?> GetByIdAsync(Guid id, CancellationToken cancellationToken = default);
    Task AddAsync(Order order, CancellationToken cancellationToken = default);
    Task SaveChangesAsync(CancellationToken cancellationToken = default);
}


// === INFRASTRUCTURE LAYER: Implements domain ports ===

// Infrastructure/Persistence/EfOrderRepository.cs
public class EfOrderRepository : IOrderRepository
{
    private readonly OrderDbContext _context;

    public EfOrderRepository(OrderDbContext context)
    {
        _context = context;
    }

    public async Task<Order?> GetByIdAsync(Guid id, CancellationToken cancellationToken = default)
    {
        return await _context.Orders
            .Include(o => o.OrderLines)
            .FirstOrDefaultAsync(o => o.Id == id, cancellationToken);
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
```

**Why compliant:**
- Controller handles only HTTP concerns (routing, status codes, request/response DTOs)
- Application service orchestrates the use case with proper transaction boundaries
- Domain model encapsulates all business rules (status validation, total calculation)
- Repository interface is defined in domain; EF Core implementation is in infrastructure
- Dependencies point inward: Infrastructure -> Application -> Domain

---

## VIOLATION: Business Logic in Controllers

```csharp
// BAD: Controller with business logic and direct DbContext access
[ApiController]
[Route("api/orders")]
public class OrderController : ControllerBase
{
    private readonly OrderDbContext _dbContext;  // Direct infrastructure access!
    private readonly IEmailService _emailService;

    public OrderController(OrderDbContext dbContext, IEmailService emailService)
    {
        _dbContext = dbContext;
        _emailService = emailService;
    }

    [HttpPost]
    public async Task<IActionResult> CreateOrder([FromBody] Dictionary<string, object> body)
    {
        // Business logic in controller!
        var customerId = body["customerId"].ToString();
        var items = JsonSerializer.Deserialize<List<Dictionary<string, object>>>(
            body["items"].ToString()!);

        if (items == null || items.Count == 0)
            return BadRequest("Items required");

        // Direct database access in controller!
        var order = new
        {
            Id = Guid.NewGuid(),
            CustomerId = customerId,
            Status = "DRAFT",
            CreatedAt = DateTime.UtcNow
        };

        await _dbContext.Database.ExecuteSqlRawAsync(
            "INSERT INTO orders (id, customer_id, status, created_at) VALUES ({0}, {1}, {2}, {3})",
            order.Id, order.CustomerId, order.Status, order.CreatedAt);

        decimal total = 0;
        foreach (var item in items)
        {
            var quantity = int.Parse(item["quantity"].ToString()!);
            var price = decimal.Parse(item["price"].ToString()!);

            // Business rule in controller!
            if (quantity > 50)
            {
                price *= 0.85m;  // Discount logic here!
            }

            total += price * quantity;

            await _dbContext.Database.ExecuteSqlRawAsync(
                "INSERT INTO order_lines (order_id, product_id, quantity, price) VALUES ({0}, {1}, {2}, {3})",
                order.Id, item["productId"], quantity, price);
        }

        // Email sending in controller!
        await _emailService.SendAsync("customer@example.com",
            $"Order {order.Id} created for ${total}");

        return Ok(new { order.Id, Total = total });
    }

    [HttpPut("{id}/submit")]
    public async Task<IActionResult> SubmitOrder(Guid id)
    {
        // Business validation with direct SQL in controller!
        var itemCount = await _dbContext.Database
            .ExecuteSqlRawAsync("SELECT COUNT(*) FROM order_lines WHERE order_id = {0}", id);

        if (itemCount == 0)
            return BadRequest("Cannot submit empty order");

        var status = await _dbContext.Orders
            .Where(o => o.Id == id)
            .Select(o => o.Status)
            .FirstOrDefaultAsync();

        if (status != "DRAFT")
            return BadRequest("Already submitted");

        await _dbContext.Database.ExecuteSqlRawAsync(
            "UPDATE orders SET status = 'SUBMITTED' WHERE id = {0}", id);

        return Ok("Submitted");
    }
}
```

**Why violates ENG-2.2:**
- Controller contains business rules (discount calculation, status validation)
- Direct DbContext and raw SQL in the presentation layer
- Email sending mixed with HTTP handling
- No service layer or domain model; everything is raw SQL and dictionaries
- Business logic cannot be tested without a web host and database
- Adding a different entry point (message handler, CLI) requires duplicating all logic

---

## Layer Responsibilities

| Layer | Responsibility | .NET Artifacts |
|-------|----------------|----------------|
| **Presentation (API)** | HTTP, routing, DTOs, validation | Controllers, Request/Response records, `[ApiController]` |
| **Application** | Use case orchestration, transactions | Services, MediatR handlers, Commands/Queries |
| **Domain** | Business rules, entities, value objects | Entity classes, Value Objects, Domain Events |
| **Infrastructure** | Persistence, external APIs, messaging | EF Core DbContext, HttpClient, Message brokers |

---

## Dependency Injection Wiring

```csharp
// Program.cs - Wire infrastructure to domain ports
builder.Services.AddScoped<IOrderRepository, EfOrderRepository>();
builder.Services.AddScoped<IInventoryClient, HttpInventoryClient>();
builder.Services.AddScoped<IOrderApplicationService, OrderApplicationService>();
builder.Services.AddDbContext<OrderDbContext>(options =>
    options.UseNpgsql(builder.Configuration.GetConnectionString("Orders")));
```

**Key principle:** Domain defines interfaces (`IOrderRepository`), infrastructure implements them (`EfOrderRepository`), and the DI container in `Program.cs` wires them together. The domain project never references the infrastructure project.
