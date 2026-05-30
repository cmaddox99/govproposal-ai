---
law_id: ENG-2.2
avatar: java-spring
---

# ENG-2.2: Layered Architecture Examples for Java Spring

## COMPLIANT: Clean Controller-Service-Repository Separation

```java
// === PRESENTATION LAYER: Controllers handle HTTP only ===

// api/OrderController.java
@RestController
@RequestMapping("/api/orders")
@RequiredArgsConstructor
public class OrderController {

    private final OrderApplicationService orderService;

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public OrderResponse createOrder(@Valid @RequestBody CreateOrderRequest request) {
        Order order = orderService.createOrder(
            new CustomerId(request.customerId()),
            request.items().stream()
                .map(i -> new LineItemCommand(
                    new ProductId(i.productId()),
                    i.quantity(),
                    Money.usd(i.unitPrice())))
                .toList()
        );
        return OrderResponse.fromDomain(order);
    }

    @GetMapping("/{id}")
    public OrderResponse getOrder(@PathVariable UUID id) {
        return orderService.findById(id)
            .map(OrderResponse::fromDomain)
            .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND));
    }

    @PutMapping("/{id}/submit")
    public OrderResponse submitOrder(@PathVariable UUID id) {
        Order order = orderService.submitOrder(id);
        return OrderResponse.fromDomain(order);
    }
}

// api/dto/CreateOrderRequest.java
public record CreateOrderRequest(
    @NotNull UUID customerId,
    @NotEmpty @Valid List<LineItemRequest> items
) {}

public record LineItemRequest(
    @NotNull UUID productId,
    @Positive int quantity,
    @Positive BigDecimal unitPrice
) {}

public record OrderResponse(
    UUID id,
    UUID customerId,
    String status,
    BigDecimal totalAmount,
    List<LineItemResponse> items,
    Instant createdAt
) {
    public static OrderResponse fromDomain(Order order) {
        return new OrderResponse(
            order.getId(),
            order.getCustomerId().value(),
            order.getStatus().name(),
            order.getTotalAmount().amount(),
            order.getOrderLines().stream()
                .map(line -> new LineItemResponse(
                    line.getProductId().value(),
                    line.getQuantity(),
                    line.getUnitPrice().amount()))
                .toList(),
            order.getCreatedAt()
        );
    }
}


// === APPLICATION LAYER: Services orchestrate use cases ===

// application/OrderApplicationService.java
@Service
@RequiredArgsConstructor
@Transactional
public class OrderApplicationService {

    private final OrderRepository orderRepository;
    private final InventoryClient inventoryClient;
    private final ApplicationEventPublisher eventPublisher;

    public Order createOrder(CustomerId customerId, List<LineItemCommand> items) {
        Order order = Order.create(customerId);

        for (LineItemCommand item : items) {
            order.addItem(item.productId(), item.quantity(), item.unitPrice());
        }

        orderRepository.save(order);
        return order;
    }

    public Order submitOrder(UUID orderId) {
        Order order = orderRepository.findById(orderId)
            .orElseThrow(() -> new OrderNotFoundException(orderId));

        order.submit();
        inventoryClient.reserveStock(order.getOrderLines());
        orderRepository.save(order);

        // Publish domain events after persistence
        order.getDomainEvents().forEach(eventPublisher::publishEvent);
        order.clearDomainEvents();

        return order;
    }

    @Transactional(readOnly = true)
    public Optional<Order> findById(UUID orderId) {
        return orderRepository.findById(orderId);
    }
}


// === DOMAIN LAYER: Entities contain business rules ===

// domain/model/Order.java
@Entity
@Table(name = "orders")
public class Order {

    @Id
    private UUID id;

    @Embedded
    private CustomerId customerId;

    @Enumerated(EnumType.STRING)
    private OrderStatus status;

    @OneToMany(cascade = CascadeType.ALL, orphanRemoval = true)
    @JoinColumn(name = "order_id")
    private List<OrderLine> orderLines = new ArrayList<>();

    @Embedded
    private Money totalAmount;

    private Instant createdAt;

    protected Order() {} // JPA

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
        orderLines.add(new OrderLine(productId, quantity, unitPrice));
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
    }

    private void recalculateTotal() {
        this.totalAmount = orderLines.stream()
            .map(OrderLine::getLineTotal)
            .reduce(Money.ZERO, Money::add);
    }

    // Read-only getters...
}

// domain/ports/OrderRepository.java (interface in domain)
public interface OrderRepository {
    Optional<Order> findById(UUID id);
    void save(Order order);
}


// === INFRASTRUCTURE LAYER: Implements domain ports ===

// infrastructure/persistence/JpaOrderRepository.java
@Repository
public class JpaOrderRepository implements OrderRepository {

    private final SpringDataOrderRepository springDataRepo;

    public JpaOrderRepository(SpringDataOrderRepository springDataRepo) {
        this.springDataRepo = springDataRepo;
    }

    @Override
    public Optional<Order> findById(UUID id) {
        return springDataRepo.findById(id);
    }

    @Override
    public void save(Order order) {
        springDataRepo.save(order);
    }
}

interface SpringDataOrderRepository extends JpaRepository<Order, UUID> {}
```

**Why compliant:**
- Controller only handles HTTP request/response mapping and validation
- Application service orchestrates the use case (create, submit) without business logic
- Domain model contains all business rules (status transitions, invariants)
- Repository interface is defined in domain; infrastructure provides implementation
- Dependencies point inward: Infrastructure -> Application -> Domain

---

## VIOLATION: Business Logic in Controllers, Domain Importing Infrastructure

```java
// BAD: Controller with business logic and direct database access
@RestController
@RequestMapping("/api/orders")
public class OrderController {

    @Autowired
    private JdbcTemplate jdbcTemplate;  // Infrastructure in controller!

    @Autowired
    private JavaMailSender mailSender;  // Infrastructure in controller!

    @PostMapping
    public ResponseEntity<Map<String, Object>> createOrder(@RequestBody Map<String, Object> body) {
        // Business logic in controller!
        String customerId = (String) body.get("customerId");
        List<Map<String, Object>> items = (List<Map<String, Object>>) body.get("items");

        if (items == null || items.isEmpty()) {
            return ResponseEntity.badRequest().body(Map.of("error", "Items required"));
        }

        // Direct database access in controller!
        UUID orderId = UUID.randomUUID();
        jdbcTemplate.update(
            "INSERT INTO orders (id, customer_id, status) VALUES (?, ?, ?)",
            orderId, customerId, "DRAFT"
        );

        BigDecimal total = BigDecimal.ZERO;
        for (Map<String, Object> item : items) {
            int quantity = (int) item.get("quantity");
            BigDecimal price = new BigDecimal(item.get("price").toString());

            // Business rule in controller!
            if (quantity > 100) {
                price = price.multiply(BigDecimal.valueOf(0.9));  // Discount logic here!
            }

            total = total.add(price.multiply(BigDecimal.valueOf(quantity)));

            jdbcTemplate.update(
                "INSERT INTO order_lines (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)",
                orderId, item.get("productId"), quantity, price
            );
        }

        // Email sending in controller!
        try {
            SimpleMailMessage message = new SimpleMailMessage();
            message.setTo("customer@example.com");
            message.setSubject("Order Confirmation");
            message.setText("Order " + orderId + " created. Total: $" + total);
            mailSender.send(message);
        } catch (Exception ignored) {}

        return ResponseEntity.ok(Map.of("orderId", orderId, "total", total));
    }

    @PutMapping("/{id}/submit")
    public ResponseEntity<String> submitOrder(@PathVariable UUID id) {
        // Direct SQL with business validation in controller!
        List<Map<String, Object>> items = jdbcTemplate.queryForList(
            "SELECT * FROM order_lines WHERE order_id = ?", id
        );

        if (items.isEmpty()) {
            return ResponseEntity.badRequest().body("Cannot submit empty order");
        }

        String status = jdbcTemplate.queryForObject(
            "SELECT status FROM orders WHERE id = ?", String.class, id
        );

        if (!"DRAFT".equals(status)) {
            return ResponseEntity.badRequest().body("Order already submitted");
        }

        jdbcTemplate.update("UPDATE orders SET status = 'SUBMITTED' WHERE id = ?", id);
        return ResponseEntity.ok("Order submitted");
    }
}
```

**Why violates ENG-2.2:**
- Controller contains business rules (discount calculation, submission validation)
- Direct database access via JdbcTemplate in the presentation layer
- Email sending mixed into HTTP request handling
- No service layer or domain model; entities are raw Maps
- Untestable business logic without spinning up a full web context
- Violates dependency direction: presentation layer imports infrastructure (JdbcTemplate, JavaMailSender)

---

## Layer Responsibilities

| Layer | Responsibility | Spring Artifacts |
|-------|----------------|------------------|
| **Presentation (API)** | HTTP mapping, validation, DTOs | `@RestController`, `@Valid`, Request/Response records |
| **Application** | Use case orchestration, transactions | `@Service`, `@Transactional` |
| **Domain** | Business rules, entities, value objects | Entities, Value Objects, Domain Events |
| **Infrastructure** | Persistence, external APIs, messaging | `@Repository`, HTTP clients, Message publishers |

---

## Dependency Inversion

```java
// Domain layer defines the PORT (interface)
public interface OrderRepository {
    Optional<Order> findById(UUID id);
    void save(Order order);
}

public interface InventoryClient {
    void reserveStock(List<OrderLine> items);
}

// Infrastructure layer provides the ADAPTER (implementation)
@Repository
public class JpaOrderRepository implements OrderRepository {
    // JPA-specific implementation
}

@Component
public class HttpInventoryClient implements InventoryClient {
    private final RestClient restClient;
    // HTTP-specific implementation
}
```

**Key principle:** Domain defines interfaces, infrastructure implements them. The application layer depends on domain interfaces, never on infrastructure classes directly.
