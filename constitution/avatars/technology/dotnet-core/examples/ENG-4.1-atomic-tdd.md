---
law_id: ENG-4.1
avatar: dotnet-core
---

# ENG-4.1: Atomic TDD Examples for .NET Core

## COMPLIANT: Single Responsibility Test with Arrange-Act-Assert Pattern

```csharp
public class OrderServiceTests
{
    private readonly Mock<IOrderRepository> _orderRepositoryMock;
    private readonly Mock<IInventoryService> _inventoryServiceMock;
    private readonly OrderService _sut;

    public OrderServiceTests()
    {
        _orderRepositoryMock = new Mock<IOrderRepository>();
        _inventoryServiceMock = new Mock<IInventoryService>();
        _sut = new OrderService(_orderRepositoryMock.Object, _inventoryServiceMock.Object);
    }

    [Fact]
    public async Task CreateOrder_WhenInventoryAvailable_ShouldReturnCreatedOrder()
    {
        // Arrange
        var customerId = Guid.NewGuid();
        var productId = Guid.NewGuid();
        var quantity = 5;
        var request = new CreateOrderRequest(customerId, productId, quantity);
        var expectedOrder = Order.Create(customerId, productId, quantity);

        _inventoryServiceMock
            .Setup(x => x.CheckAvailabilityAsync(productId, quantity))
            .ReturnsAsync(true);
        _orderRepositoryMock
            .Setup(x => x.AddAsync(It.IsAny<Order>()))
            .ReturnsAsync(expectedOrder);

        // Act
        var result = await _sut.CreateOrderAsync(request);

        // Assert
        Assert.NotNull(result);
        Assert.Equal(customerId, result.CustomerId);
        Assert.Equal(OrderStatus.Created, result.Status);

        _inventoryServiceMock.Verify(x => x.CheckAvailabilityAsync(productId, quantity), Times.Once);
        _orderRepositoryMock.Verify(x => x.AddAsync(It.IsAny<Order>()), Times.Once);
    }

    [Fact]
    public async Task CreateOrder_WhenInventoryInsufficient_ShouldThrowException()
    {
        // Arrange
        var request = new CreateOrderRequest(Guid.NewGuid(), Guid.NewGuid(), 100);

        _inventoryServiceMock
            .Setup(x => x.CheckAvailabilityAsync(It.IsAny<Guid>(), It.IsAny<int>()))
            .ReturnsAsync(false);

        // Act
        var act = () => _sut.CreateOrderAsync(request);

        // Assert
        var ex = await Assert.ThrowsAsync<InsufficientInventoryException>(act);
        Assert.Contains("Insufficient inventory", ex.Message);

        _orderRepositoryMock.Verify(x => x.AddAsync(It.IsAny<Order>()), Times.Never);
    }
}
```

**Why compliant:** Each test method verifies exactly one behavior. Tests follow the Arrange-Act-Assert pattern with clear separation. Descriptive names explain the scenario and expected outcome using the Given-When-Then naming convention. Mocks isolate the system under test (SUT).

---

## COMPLIANT: Theory Tests for Multiple Scenarios

```csharp
public class PriceCalculatorTests
{
    private readonly PriceCalculator _sut = new();

    [Theory]
    [InlineData(1, 100.00, 100.00)]    // No discount for single item
    [InlineData(10, 100.00, 950.00)]   // 5% discount for 10+ items
    [InlineData(50, 100.00, 4500.00)]  // 10% discount for 50+ items
    [InlineData(100, 100.00, 8500.00)] // 15% discount for 100+ items
    public void CalculateTotal_ShouldApplyCorrectDiscountTier(
        int quantity,
        decimal unitPrice,
        decimal expectedTotal)
    {
        // Arrange
        var lineItem = new LineItem("PROD-001", quantity, unitPrice);

        // Act
        var result = _sut.CalculateTotal(lineItem);

        // Assert
        Assert.Equal(expectedTotal, result);
    }

    [Theory]
    [InlineData(0)]
    [InlineData(-1)]
    [InlineData(-100)]
    public void CalculateTotal_WithInvalidQuantity_ShouldThrowArgumentException(int invalidQuantity)
    {
        // Arrange
        var lineItem = new LineItem("PROD-001", invalidQuantity, 10.00m);

        // Act
        var act = () => _sut.CalculateTotal(lineItem);

        // Assert
        Assert.Throws<ArgumentException>(act);
    }
}
```

**Why compliant:** Theory tests efficiently test multiple inputs while maintaining single-assertion focus per logical scenario. Each InlineData combination tests one specific discount tier behavior.

---

## VIOLATION: Multiple Unrelated Assertions in Single Test

```csharp
public class UserServiceTests
{
    private readonly Mock<IUserRepository> _userRepositoryMock = new();
    private readonly Mock<IEmailService> _emailServiceMock = new();
    private readonly Mock<IAuditService> _auditServiceMock = new();
    private readonly UserService _sut;

    public UserServiceTests()
    {
        _sut = new UserService(
            _userRepositoryMock.Object,
            _emailServiceMock.Object,
            _auditServiceMock.Object);
    }

    [Fact]
    public async Task TestUserOperations()
    {
        // Testing user creation
        var createRequest = new CreateUserRequest("john@example.com", "John Doe");
        var user = User.Create(createRequest);
        _userRepositoryMock.Setup(x => x.AddAsync(It.IsAny<User>())).ReturnsAsync(user);

        var createdUser = await _sut.CreateUserAsync(createRequest);
        Assert.NotNull(createdUser);
        Assert.Equal("john@example.com", createdUser.Email);
        _emailServiceMock.Verify(x => x.SendWelcomeEmailAsync(It.IsAny<User>()), Times.Once);

        // Testing user update
        var updateRequest = new UpdateUserRequest(user.Id, "Jane Doe");
        _userRepositoryMock.Setup(x => x.GetByIdAsync(user.Id)).ReturnsAsync(user);

        var updatedUser = await _sut.UpdateUserAsync(updateRequest);
        Assert.Equal("Jane Doe", updatedUser.Name);
        _auditServiceMock.Verify(x => x.LogUpdateAsync(It.IsAny<User>()), Times.Once);

        // Testing user deletion
        await _sut.DeleteUserAsync(user.Id);
        _userRepositoryMock.Verify(x => x.DeleteAsync(user.Id), Times.Once);
        _auditServiceMock.Verify(x => x.LogDeletionAsync(It.IsAny<Guid>()), Times.Once);

        // Testing email validation
        Assert.True(_sut.IsValidEmail("test@test.com"));
        Assert.False(_sut.IsValidEmail("invalid"));
    }
}
```

**Why violates ENG-4.1:** This test combines four unrelated behaviors (create, update, delete, validation) into one method. When it fails, you cannot quickly identify which operation broke. Tests should be atomic - one behavior per test method. Each operation should be its own test with focused assertions.

---

## VIOLATION: Test Without Clear Arrange-Act-Assert Structure

```csharp
public class PaymentProcessorTests
{
    [Fact]
    public async Task ProcessPayment()
    {
        var processor = new PaymentProcessor(new MockGateway(), new MockNotifier());
        var result = await processor.ProcessAsync(new Payment(100.00m, "USD", "card_123"));
        Assert.True(result.IsSuccessful);
        var refund = await processor.RefundAsync(result.TransactionId, 50.00m);
        Assert.True(refund.IsSuccessful);
        Assert.Equal(50.00m, refund.Amount);
        var status = await processor.GetStatusAsync(result.TransactionId);
        Assert.Equal("PARTIALLY_REFUNDED", status);
        await processor.ProcessAsync(new Payment(-10.00m, "USD", "card_123"));
        // This should fail but we forgot to assert
    }
}
```

**Why violates ENG-4.1:** No clear AAA structure makes the test hard to read. Multiple operations are chained without separation. The test verifies process, refund, and status check in sequence - if any fails, debugging requires understanding the entire chain. The last operation has no assertion at all.

---

## COMPLIANT: Integration Test with TestContainers

```csharp
public class OrderRepositoryIntegrationTests : IAsyncLifetime
{
    private readonly PostgreSqlContainer _postgres = new PostgreSqlBuilder()
        .WithImage("postgres:15-alpine")
        .Build();

    private OrderDbContext _context = null!;
    private OrderRepository _sut = null!;

    public async Task InitializeAsync()
    {
        await _postgres.StartAsync();

        var options = new DbContextOptionsBuilder<OrderDbContext>()
            .UseNpgsql(_postgres.GetConnectionString())
            .Options;

        _context = new OrderDbContext(options);
        await _context.Database.EnsureCreatedAsync();

        _sut = new OrderRepository(_context);
    }

    public async Task DisposeAsync()
    {
        await _context.DisposeAsync();
        await _postgres.DisposeAsync();
    }

    [Fact]
    public async Task FindByCustomerId_ShouldReturnPagedResults()
    {
        // Arrange
        var customerId = Guid.NewGuid();
        var orders = Enumerable.Range(0, 25)
            .Select(i => Order.Create(customerId, Guid.NewGuid(), i + 1))
            .ToList();

        await _context.Orders.AddRangeAsync(orders);
        await _context.SaveChangesAsync();

        // Act
        var result = await _sut.FindByCustomerIdAsync(
            customerId,
            pageNumber: 1,
            pageSize: 10);

        // Assert
        Assert.Equal(10, result.Items.Count);
        Assert.Equal(25, result.TotalCount);
        Assert.Equal(3, result.TotalPages);
    }
}
```

**Why compliant:** Integration test focuses on one repository method behavior. Uses TestContainers for realistic database testing. Clear AAA structure with proper setup isolation via IAsyncLifetime.

---

## VIOLATION: Missing Edge Case Tests

```csharp
public class DiscountServiceTests
{
    private readonly DiscountService _sut = new();

    [Fact]
    public void ApplyDiscount_ShouldApplyDiscount()
    {
        // Only tests happy path
        var result = _sut.ApplyDiscount(100.00m, "SAVE10");
        Assert.Equal(90.00m, result);
    }
}
```

**Why violates ENG-4.1:** Only tests the happy path. Missing tests for: invalid/expired codes, null inputs, zero/negative amounts, code case sensitivity, maximum discount limits. Atomic TDD requires comprehensive coverage of edge cases, each in its own focused test.

---

## COMPLIANT: Comprehensive Edge Case Coverage

```csharp
public class DiscountServiceTests
{
    private readonly Mock<IDiscountCodeRepository> _repositoryMock = new();
    private readonly DiscountService _sut;

    public DiscountServiceTests()
    {
        _sut = new DiscountService(_repositoryMock.Object);
    }

    [Fact]
    public async Task ApplyDiscount_WithValidCode_ShouldApplyPercentageDiscount()
    {
        // Arrange
        var code = new DiscountCode("SAVE10", DiscountType.Percentage, 10, DateTime.UtcNow.AddDays(1));
        _repositoryMock.Setup(x => x.GetByCodeAsync("SAVE10")).ReturnsAsync(code);

        // Act
        var result = await _sut.ApplyDiscountAsync(100.00m, "SAVE10");

        // Assert
        Assert.Equal(90.00m, result);
    }

    [Fact]
    public async Task ApplyDiscount_WithNullCode_ShouldThrowArgumentNullException()
    {
        // Act
        var act = () => _sut.ApplyDiscountAsync(100.00m, null!);

        // Assert
        var ex = await Assert.ThrowsAsync<ArgumentNullException>(act);
        Assert.Equal("discountCode", ex.ParamName);
    }

    [Fact]
    public async Task ApplyDiscount_WithExpiredCode_ShouldThrowDiscountExpiredException()
    {
        // Arrange
        var expiredCode = new DiscountCode("EXPIRED", DiscountType.Percentage, 10, DateTime.UtcNow.AddDays(-1));
        _repositoryMock.Setup(x => x.GetByCodeAsync("EXPIRED")).ReturnsAsync(expiredCode);

        // Act
        var act = () => _sut.ApplyDiscountAsync(100.00m, "EXPIRED");

        // Assert
        await Assert.ThrowsAsync<DiscountExpiredException>(act);
    }

    [Theory]
    [InlineData(0)]
    [InlineData(-1)]
    [InlineData(-100.50)]
    public async Task ApplyDiscount_WithInvalidAmount_ShouldThrowArgumentException(decimal invalidAmount)
    {
        // Act
        var act = () => _sut.ApplyDiscountAsync(invalidAmount, "SAVE10");

        // Assert
        var ex = await Assert.ThrowsAsync<ArgumentException>(act);
        Assert.Contains("Amount must be positive", ex.Message);
    }

    [Theory]
    [InlineData("save10")]
    [InlineData("SAVE10")]
    [InlineData("Save10")]
    public async Task ApplyDiscount_ShouldBeCaseInsensitive(string codeVariant)
    {
        // Arrange
        var code = new DiscountCode("SAVE10", DiscountType.Percentage, 10, DateTime.UtcNow.AddDays(1));
        _repositoryMock.Setup(x => x.GetByCodeAsync(It.IsAny<string>())).ReturnsAsync(code);

        // Act
        var result = await _sut.ApplyDiscountAsync(100.00m, codeVariant);

        // Assert
        Assert.Equal(90.00m, result);
    }

    [Fact]
    public async Task ApplyDiscount_WhenDiscountExceedsMaximum_ShouldCapAtMaximum()
    {
        // Arrange
        var code = new DiscountCode("MEGA50", DiscountType.Percentage, 50, DateTime.UtcNow.AddDays(1), maxDiscount: 25.00m);
        _repositoryMock.Setup(x => x.GetByCodeAsync("MEGA50")).ReturnsAsync(code);

        // Act
        var result = await _sut.ApplyDiscountAsync(100.00m, "MEGA50");

        // Assert
        Assert.Equal(75.00m, result); // 50% would be 50.00, but capped at 25.00
    }
}
```

**Why compliant:** Each edge case has its own focused test. Test names clearly describe the scenario and expected behavior. Comprehensive coverage of null inputs, expired codes, invalid amounts, case sensitivity, and maximum discount limits.

---

## TDD Cycle Commands

```bash
# RED: Run specific test, see it fail
dotnet test --filter "FullyQualifiedName~OrderServiceTests.CreateOrder_WhenInventoryAvailable"

# GREEN: Write code, run test again
dotnet test --filter "FullyQualifiedName~OrderServiceTests.CreateOrder_WhenInventoryAvailable"

# REFACTOR: Run all unit tests
dotnet test

# VERIFY: Check coverage and constitutional compliance
dotnet test --collect:"XPlat Code Coverage"
constitution-lint .

# Commit when green and compliant
git add -A && git commit -m "Add order creation to OrderService"
```
