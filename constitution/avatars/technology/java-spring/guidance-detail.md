# Java/Spring Boot Guidance

> **Purpose:** Stack-specific agent behaviors for Java/Spring Boot applications.

---

## Overview

This guidance provides patterns for AI agents working with Java and Spring Boot applications. It covers testing with JUnit 5, domain modeling patterns, and Spring-specific conventions.

---

## Testing Framework

**Primary Framework:** JUnit 5 + Mockito + AssertJ

### Test Structure

```java
@ExtendWith(MockitoExtension.class)
class OrderServiceTest {

    @Mock
    private OrderRepository orderRepository;

    @InjectMocks
    private OrderService orderService;

    @Test
    void createOrder_shouldReturnNewOrder() {
        // Arrange
        var customerId = CustomerId.of("cust-123");

        // Act
        var order = orderService.createOrder(customerId);

        // Assert
        assertThat(order.getCustomerId()).isEqualTo(customerId);
        assertThat(order.getStatus()).isEqualTo(OrderStatus.DRAFT);
        assertThat(order.getTotal()).isEqualTo(Money.ZERO);
    }

    @Test
    void addItem_shouldUpdateTotal() {
        // Arrange
        var order = Order.create(CustomerId.of("cust-123"));
        var product = new Product("SKU-1", Money.of(100));

        // Act
        order.addItem(product, 2);

        // Assert
        assertThat(order.getTotal()).isEqualTo(Money.of(200));
    }

    @ParameterizedTest
    @CsvSource({
        "1, 100",
        "2, 200",
        "5, 500"
    })
    void addItem_withVariousQuantities_shouldCalculateCorrectTotal(
            int quantity, int expectedTotal) {
        // Arrange
        var order = Order.create(CustomerId.of("cust-123"));
        var product = new Product("SKU-1", Money.of(100));

        // Act
        order.addItem(product, quantity);

        // Assert
        assertThat(order.getTotal().getAmount()).isEqualTo(expectedTotal);
    }
}
```

### Testing Patterns

- Use `@ExtendWith(MockitoExtension.class)` for mock injection
- Use `@ParameterizedTest` with `@CsvSource` for data-driven tests
- Use AssertJ for fluent assertions
- Separate unit tests from integration tests with `@SpringBootTest`
- Use `@DataJpaTest` for repository tests

---

## Domain Modeling

### Entity Pattern

```java
@Entity
@Table(name = "orders")
public class Order {

    @Id
    private OrderId id;

    @Embedded
    private CustomerId customerId;

    @OneToMany(cascade = CascadeType.ALL, orphanRemoval = true)
    private List<OrderLine> lines = new ArrayList<>();

    @Enumerated(EnumType.STRING)
    private OrderStatus status = OrderStatus.DRAFT;

    protected Order() {} // JPA

    public static Order create(CustomerId customerId) {
        var order = new Order();
        order.id = OrderId.generate();
        order.customerId = customerId;
        return order;
    }

    public void addItem(Product product, int quantity) {
        ensureModifiable();
        lines.add(new OrderLine(product.getId(), quantity, product.getPrice()));
    }

    public Money getTotal() {
        return lines.stream()
            .map(OrderLine::getSubtotal)
            .reduce(Money.ZERO, Money::add);
    }

    private void ensureModifiable() {
        if (status != OrderStatus.DRAFT) {
            throw new OrderNotModifiableException(id, status);
        }
    }
}
```

### Value Object Pattern

```java
@Embeddable
public record Money(BigDecimal amount, String currency) {

    public static final Money ZERO = new Money(BigDecimal.ZERO, "USD");

    public Money {
        if (amount.compareTo(BigDecimal.ZERO) < 0) {
            throw new IllegalArgumentException("Amount cannot be negative");
        }
    }

    public static Money of(int amount) {
        return new Money(BigDecimal.valueOf(amount), "USD");
    }

    public Money add(Money other) {
        validateSameCurrency(other);
        return new Money(amount.add(other.amount), currency);
    }

    public Money multiply(int quantity) {
        return new Money(amount.multiply(BigDecimal.valueOf(quantity)), currency);
    }

    private void validateSameCurrency(Money other) {
        if (!currency.equals(other.currency)) {
            throw new CurrencyMismatchException(currency, other.currency);
        }
    }
}
```

---

## Common Patterns

### Dependency Injection

```java
@Service
@RequiredArgsConstructor
public class OrderService {

    private final OrderRepository orderRepository;
    private final InventoryClient inventoryClient;
    private final EventPublisher eventPublisher;

    @Transactional
    public Order createOrder(CustomerId customerId, List<LineItemCommand> items) {
        var order = Order.create(customerId);

        items.forEach(item ->
            order.addItem(item.productId(), item.quantity(), item.price())
        );

        inventoryClient.reserve(order.getLines());
        orderRepository.save(order);
        eventPublisher.publishAll(order.collectEvents());

        return order;
    }
}
```

### Repository Pattern

```java
public interface OrderRepository extends JpaRepository<Order, OrderId> {

    Optional<Order> findByIdAndCustomerId(OrderId id, CustomerId customerId);

    @Query("SELECT o FROM Order o WHERE o.status = :status")
    List<Order> findByStatus(@Param("status") OrderStatus status);
}
```

---

## Anti-Patterns to Avoid

### Anemic Domain Model

```java
// BAD - Entity is just a data bag
@Entity
public class Order {
    @Id private Long id;
    private String customerId;
    private List<OrderLine> lines;
    private String status;
    // Only getters/setters, no behavior
}

// Business logic in service
@Service
public class OrderService {
    public void addItem(Long orderId, Product product) {
        Order order = repository.findById(orderId);
        if (!order.getStatus().equals("DRAFT")) { // Logic should be in Order
            throw new RuntimeException("Cannot modify");
        }
        order.getLines().add(new OrderLine(...)); // Direct manipulation
    }
}
```

### Not Using Records for Value Objects

```java
// BAD - Mutable class for what should be a value object
public class Money {
    private BigDecimal amount;

    public void setAmount(BigDecimal amount) { // Mutation!
        this.amount = amount;
    }
}

// GOOD - Use Java records
public record Money(BigDecimal amount, String currency) {
    // Immutable by default
}
```

---

## Tools and Commands

### Development

```bash
# Start application
./mvnw spring-boot:run

# Start with debug
./mvnw spring-boot:run -Dspring-boot.run.jvmArguments="-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=5005"

# Build
./mvnw clean package
```

### Testing

```bash
# Run all tests
./mvnw test

# Run single test class
./mvnw test -Dtest=OrderServiceTest

# Run with coverage
./mvnw test jacoco:report

# Integration tests only
./mvnw verify -Pfailsafe
```

### Code Quality

```bash
# Format code
./mvnw spotless:apply

# Check style
./mvnw checkstyle:check

# Static analysis
./mvnw pmd:check spotbugs:check
```
