---
law_id: ENG-2.1
avatar: java-spring
---

# ENG-2.1: Aggregate Design Examples for Java Spring

## COMPLIANT: Well-Defined Aggregate Root with Encapsulated Children

```java
@Entity
@Table(name = "orders")
public class Order {

    @Id
    private UUID id;

    @Embedded
    private CustomerId customerId;

    @Enumerated(EnumType.STRING)
    private OrderStatus status;

    @OneToMany(cascade = CascadeType.ALL, orphanRemoval = true, fetch = FetchType.LAZY)
    @JoinColumn(name = "order_id")
    private List<OrderLine> orderLines = new ArrayList<>();

    @Embedded
    private Money totalAmount;

    @Version
    private Long version;

    private Instant createdAt;
    private Instant updatedAt;

    protected Order() {} // JPA requirement

    public static Order create(CustomerId customerId) {
        var order = new Order();
        order.id = UUID.randomUUID();
        order.customerId = customerId;
        order.status = OrderStatus.DRAFT;
        order.totalAmount = Money.ZERO;
        order.createdAt = Instant.now();
        return order;
    }

    public void addItem(ProductId productId, int quantity, Money unitPrice) {
        if (status != OrderStatus.DRAFT) {
            throw new IllegalStateException("Cannot modify a submitted order");
        }

        var existingLine = findLineByProduct(productId);
        if (existingLine.isPresent()) {
            existingLine.get().increaseQuantity(quantity);
        } else {
            orderLines.add(new OrderLine(productId, quantity, unitPrice));
        }

        recalculateTotal();
    }

    public void removeItem(ProductId productId) {
        if (status != OrderStatus.DRAFT) {
            throw new IllegalStateException("Cannot modify a submitted order");
        }

        orderLines.removeIf(line -> line.getProductId().equals(productId));
        recalculateTotal();
    }

    public void submit() {
        if (orderLines.isEmpty()) {
            throw new IllegalStateException("Cannot submit an empty order");
        }
        if (status != OrderStatus.DRAFT) {
            throw new IllegalStateException("Order already submitted");
        }

        this.status = OrderStatus.SUBMITTED;
        this.updatedAt = Instant.now();
    }

    public void confirm() {
        if (status != OrderStatus.SUBMITTED) {
            throw new IllegalStateException("Only submitted orders can be confirmed");
        }
        this.status = OrderStatus.CONFIRMED;
        this.updatedAt = Instant.now();
    }

    private void recalculateTotal() {
        this.totalAmount = orderLines.stream()
            .map(OrderLine::getLineTotal)
            .reduce(Money.ZERO, Money::add);
        this.updatedAt = Instant.now();
    }

    private Optional<OrderLine> findLineByProduct(ProductId productId) {
        return orderLines.stream()
            .filter(line -> line.getProductId().equals(productId))
            .findFirst();
    }

    // Read-only access to order lines
    public List<OrderLine> getOrderLines() {
        return Collections.unmodifiableList(orderLines);
    }

    // Getters for other fields...
}

@Entity
@Table(name = "order_lines")
public class OrderLine {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Embedded
    @AttributeOverride(name = "value", column = @Column(name = "product_id"))
    private ProductId productId;

    private int quantity;

    @Embedded
    private Money unitPrice;

    protected OrderLine() {}

    OrderLine(ProductId productId, int quantity, Money unitPrice) {
        if (quantity <= 0) {
            throw new IllegalArgumentException("Quantity must be positive");
        }
        this.productId = productId;
        this.quantity = quantity;
        this.unitPrice = unitPrice;
    }

    void increaseQuantity(int additionalQuantity) {
        if (additionalQuantity <= 0) {
            throw new IllegalArgumentException("Additional quantity must be positive");
        }
        this.quantity += additionalQuantity;
    }

    public Money getLineTotal() {
        return unitPrice.multiply(quantity);
    }

    // Package-private or public getters only, no setters exposed
}
```

**Why compliant:** Order is the aggregate root that controls all access to OrderLines. Business rules (status transitions, quantity validation) are enforced within the aggregate. OrderLines cannot be modified directly from outside - all changes go through Order methods. The aggregate maintains invariants (total always matches lines).

---

## COMPLIANT: Value Objects for Domain Concepts

```java
@Embeddable
public record Money(
    @Column(name = "amount") BigDecimal amount,
    @Column(name = "currency") String currency
) {
    public static final Money ZERO = new Money(BigDecimal.ZERO, "USD");

    public Money {
        Objects.requireNonNull(amount, "Amount required");
        Objects.requireNonNull(currency, "Currency required");
        if (amount.scale() > 2) {
            amount = amount.setScale(2, RoundingMode.HALF_UP);
        }
    }

    public static Money of(BigDecimal amount, String currency) {
        return new Money(amount, currency);
    }

    public static Money usd(double amount) {
        return new Money(BigDecimal.valueOf(amount), "USD");
    }

    public Money add(Money other) {
        validateSameCurrency(other);
        return new Money(this.amount.add(other.amount), this.currency);
    }

    public Money subtract(Money other) {
        validateSameCurrency(other);
        return new Money(this.amount.subtract(other.amount), this.currency);
    }

    public Money multiply(int multiplier) {
        return new Money(this.amount.multiply(BigDecimal.valueOf(multiplier)), this.currency);
    }

    public boolean isGreaterThan(Money other) {
        validateSameCurrency(other);
        return this.amount.compareTo(other.amount) > 0;
    }

    private void validateSameCurrency(Money other) {
        if (!this.currency.equals(other.currency)) {
            throw new IllegalArgumentException(
                "Cannot operate on different currencies: " + this.currency + " vs " + other.currency
            );
        }
    }
}

@Embeddable
public record CustomerId(@Column(name = "customer_id") UUID value) {
    public CustomerId {
        Objects.requireNonNull(value, "Customer ID value required");
    }

    public static CustomerId generate() {
        return new CustomerId(UUID.randomUUID());
    }

    public static CustomerId of(String value) {
        return new CustomerId(UUID.fromString(value));
    }
}

@Embeddable
public record ProductId(@Column(name = "product_id") UUID value) {
    public ProductId {
        Objects.requireNonNull(value, "Product ID value required");
    }

    public static ProductId of(String value) {
        return new ProductId(UUID.fromString(value));
    }
}
```

**Why compliant:** Value objects encapsulate domain concepts with validation and behavior. They are immutable (records) ensuring thread safety. Currency mismatch is caught at the domain level. Typed IDs prevent mixing CustomerId with ProductId accidentally.

---

## VIOLATION: Anemic Domain Model with Exposed Setters

```java
@Entity
@Data // Lombok generates setters for everything
@NoArgsConstructor
@AllArgsConstructor
public class Order {

    @Id
    @GeneratedValue
    private Long id;

    private Long customerId;

    private String status;

    @OneToMany(mappedBy = "order", cascade = CascadeType.ALL)
    private List<OrderLine> orderLines;

    private BigDecimal totalAmount;

    private LocalDateTime createdAt;
}

@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
public class OrderLine {

    @Id
    @GeneratedValue
    private Long id;

    @ManyToOne
    private Order order;

    private Long productId;

    private Integer quantity;

    private BigDecimal unitPrice;

    private BigDecimal lineTotal;
}

// Service that should be in the domain
@Service
@RequiredArgsConstructor
public class OrderService {

    private final OrderRepository orderRepository;
    private final OrderLineRepository orderLineRepository;

    public void addItemToOrder(Long orderId, Long productId, int quantity, BigDecimal price) {
        var order = orderRepository.findById(orderId).orElseThrow();

        // Business logic scattered in service
        if (!"DRAFT".equals(order.getStatus())) {
            throw new IllegalStateException("Cannot modify submitted order");
        }

        var line = new OrderLine();
        line.setOrder(order);
        line.setProductId(productId);
        line.setQuantity(quantity);
        line.setUnitPrice(price);
        line.setLineTotal(price.multiply(BigDecimal.valueOf(quantity)));

        order.getOrderLines().add(line);

        // Recalculate total in service
        var total = order.getOrderLines().stream()
            .map(OrderLine::getLineTotal)
            .reduce(BigDecimal.ZERO, BigDecimal::add);
        order.setTotalAmount(total);

        orderRepository.save(order);
    }

    public void submitOrder(Long orderId) {
        var order = orderRepository.findById(orderId).orElseThrow();

        // Validation logic in service
        if (order.getOrderLines().isEmpty()) {
            throw new IllegalStateException("Cannot submit empty order");
        }

        order.setStatus("SUBMITTED"); // String-based status, no type safety
        orderRepository.save(order);
    }
}
```

**Why violates ENG-2.1:** The domain model is anemic - entities are just data holders with getters/setters. All business logic lives in services, not the aggregate. OrderLines can be directly accessed and modified, bypassing aggregate rules. No invariants are enforced by the entities themselves. Status is a string rather than an enum, allowing invalid values.

---

## VIOLATION: Breaking Aggregate Boundaries

```java
@Service
@RequiredArgsConstructor
public class ReportingService {

    private final OrderLineRepository orderLineRepository; // Direct access to child entity!

    public List<TopSellingProduct> getTopSellingProducts(LocalDate from, LocalDate to) {
        // Directly querying and modifying order lines without going through Order
        var lines = orderLineRepository.findByCreatedAtBetween(from, to);

        // Worse: modifying child entities directly
        lines.forEach(line -> {
            line.setReportedAt(LocalDateTime.now()); // Bypasses Order aggregate
            orderLineRepository.save(line);
        });

        return lines.stream()
            .collect(Collectors.groupingBy(
                OrderLine::getProductId,
                Collectors.summingInt(OrderLine::getQuantity)
            ))
            .entrySet().stream()
            .sorted(Map.Entry.<Long, Integer>comparingByValue().reversed())
            .limit(10)
            .map(e -> new TopSellingProduct(e.getKey(), e.getValue()))
            .toList();
    }
}

// Repository that shouldn't exist for non-aggregate-roots
public interface OrderLineRepository extends JpaRepository<OrderLine, Long> {
    List<OrderLine> findByCreatedAtBetween(LocalDate from, LocalDate to);
}
```

**Why violates ENG-2.1:** OrderLineRepository allows direct access to aggregate children. Modifying OrderLines without going through the Order aggregate bypasses business rules. The aggregate root loses control over its invariants. If Order has rules about line modifications, they're easily circumvented.

---

## COMPLIANT: Repository Only for Aggregate Root

```java
public interface OrderRepository extends JpaRepository<Order, UUID> {

    Optional<Order> findByIdAndCustomerId(UUID id, CustomerId customerId);

    @Query("SELECT o FROM Order o WHERE o.status = :status AND o.createdAt < :cutoff")
    List<Order> findStaleOrders(
        @Param("status") OrderStatus status,
        @Param("cutoff") Instant cutoff
    );

    @Query("""
        SELECT new com.example.reports.OrderSummaryProjection(
            o.id, o.customerId, o.totalAmount, o.status, o.createdAt
        )
        FROM Order o
        WHERE o.createdAt BETWEEN :from AND :to
        """)
    List<OrderSummaryProjection> findOrderSummaries(
        @Param("from") Instant from,
        @Param("to") Instant to
    );
}

// Read-only projection for reporting - doesn't bypass aggregate
public record OrderSummaryProjection(
    UUID orderId,
    CustomerId customerId,
    Money totalAmount,
    OrderStatus status,
    Instant createdAt
) {}

// For complex reporting needs, use a separate read model
@Service
@RequiredArgsConstructor
public class OrderReportingService {

    private final JdbcTemplate jdbcTemplate; // Direct SQL for read-only reports

    public List<TopSellingProduct> getTopSellingProducts(Instant from, Instant to) {
        return jdbcTemplate.query("""
            SELECT ol.product_id, SUM(ol.quantity) as total_sold
            FROM order_lines ol
            JOIN orders o ON ol.order_id = o.id
            WHERE o.created_at BETWEEN ? AND ?
              AND o.status IN ('CONFIRMED', 'SHIPPED', 'DELIVERED')
            GROUP BY ol.product_id
            ORDER BY total_sold DESC
            LIMIT 10
            """,
            (rs, row) -> new TopSellingProduct(
                ProductId.of(rs.getString("product_id")),
                rs.getInt("total_sold")
            ),
            from, to
        );
    }
}
```

**Why compliant:** Only the aggregate root (Order) has a repository. Reporting uses read-only projections or direct JDBC queries that don't modify data. The aggregate boundary is respected for all write operations. Read models can query denormalized data without affecting aggregate invariants.

---

## COMPLIANT: Domain Events from Aggregate

```java
@Entity
public class Order extends AbstractAggregateRoot<Order> {

    // ... fields as before ...

    public void submit() {
        if (orderLines.isEmpty()) {
            throw new IllegalStateException("Cannot submit an empty order");
        }
        if (status != OrderStatus.DRAFT) {
            throw new IllegalStateException("Order already submitted");
        }

        this.status = OrderStatus.SUBMITTED;
        this.updatedAt = Instant.now();

        // Register domain event
        registerEvent(new OrderSubmittedEvent(
            this.id,
            this.customerId,
            this.totalAmount,
            this.orderLines.stream()
                .map(line -> new OrderLineSnapshot(
                    line.getProductId(),
                    line.getQuantity(),
                    line.getUnitPrice()
                ))
                .toList()
        ));
    }

    public void cancel(String reason) {
        if (!canBeCancelled()) {
            throw new IllegalStateException("Order cannot be cancelled in status: " + status);
        }

        this.status = OrderStatus.CANCELLED;
        this.updatedAt = Instant.now();

        registerEvent(new OrderCancelledEvent(this.id, this.customerId, reason));
    }

    private boolean canBeCancelled() {
        return status == OrderStatus.DRAFT || status == OrderStatus.SUBMITTED;
    }
}

public record OrderSubmittedEvent(
    UUID orderId,
    CustomerId customerId,
    Money totalAmount,
    List<OrderLineSnapshot> lines
) {}

public record OrderLineSnapshot(
    ProductId productId,
    int quantity,
    Money unitPrice
) {}

@Component
@RequiredArgsConstructor
public class OrderEventHandler {

    private final InventoryService inventoryService;
    private final NotificationService notificationService;

    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
    public void handleOrderSubmitted(OrderSubmittedEvent event) {
        inventoryService.reserveStock(event.lines());
        notificationService.sendOrderConfirmation(event.customerId(), event.orderId());
    }

    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
    public void handleOrderCancelled(OrderCancelledEvent event) {
        inventoryService.releaseReservation(event.orderId());
        notificationService.sendCancellationNotice(event.customerId(), event.orderId());
    }
}
```

**Why compliant:** Domain events are raised by the aggregate when significant state changes occur. Events contain immutable snapshots, not entity references. Event handlers run after the transaction commits, ensuring the aggregate is persisted first. Cross-aggregate communication happens through events, not direct calls.
