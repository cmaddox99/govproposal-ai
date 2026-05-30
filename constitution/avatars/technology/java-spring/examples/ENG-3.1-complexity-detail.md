---
law_id: ENG-3.1
avatar: java-spring
---

# ENG-3.1: Complexity Management Examples for Java Spring

## COMPLIANT: Single Responsibility with Strategy Pattern

```java
@Service
@RequiredArgsConstructor
public class PaymentService {

    private final PaymentStrategyFactory strategyFactory;
    private final PaymentRepository paymentRepository;
    private final PaymentEventPublisher eventPublisher;

    public PaymentResult processPayment(PaymentRequest request) {
        var strategy = strategyFactory.getStrategy(request.getPaymentMethod());
        var result = strategy.process(request);

        if (result.isSuccessful()) {
            paymentRepository.save(result.toEntity());
            eventPublisher.publish(new PaymentCompletedEvent(result));
        }

        return result;
    }
}

public interface PaymentStrategy {
    PaymentResult process(PaymentRequest request);
    boolean supports(PaymentMethod method);
}

@Component
public class CreditCardPaymentStrategy implements PaymentStrategy {

    private final CreditCardGateway gateway;
    private final FraudDetectionService fraudService;

    @Override
    public PaymentResult process(PaymentRequest request) {
        fraudService.validateTransaction(request);
        return gateway.charge(request.getAmount(), request.getCardDetails());
    }

    @Override
    public boolean supports(PaymentMethod method) {
        return method == PaymentMethod.CREDIT_CARD;
    }
}

@Component
@RequiredArgsConstructor
public class PaymentStrategyFactory {

    private final List<PaymentStrategy> strategies;

    public PaymentStrategy getStrategy(PaymentMethod method) {
        return strategies.stream()
            .filter(s -> s.supports(method))
            .findFirst()
            .orElseThrow(() -> new UnsupportedPaymentMethodException(method));
    }
}
```

**Why compliant:** Each class has a single responsibility. PaymentService orchestrates, strategies handle specific payment types. New payment methods require only adding a new strategy class - no modification to existing code (Open/Closed Principle). Cyclomatic complexity stays low in each component.

---

## COMPLIANT: Readable Method with Early Returns

```java
@Service
public class OrderValidationService {

    public ValidationResult validateOrder(Order order) {
        if (order == null) {
            return ValidationResult.failure("Order cannot be null");
        }

        if (order.getItems().isEmpty()) {
            return ValidationResult.failure("Order must contain at least one item");
        }

        if (order.getCustomerId() == null) {
            return ValidationResult.failure("Customer ID is required");
        }

        var itemValidation = validateItems(order.getItems());
        if (itemValidation.hasErrors()) {
            return itemValidation;
        }

        var inventoryValidation = validateInventory(order.getItems());
        if (inventoryValidation.hasErrors()) {
            return inventoryValidation;
        }

        return ValidationResult.success();
    }

    private ValidationResult validateItems(List<OrderItem> items) {
        var errors = items.stream()
            .filter(item -> item.getQuantity() <= 0)
            .map(item -> "Invalid quantity for product: " + item.getProductId())
            .toList();

        return errors.isEmpty()
            ? ValidationResult.success()
            : ValidationResult.failure(errors);
    }

    private ValidationResult validateInventory(List<OrderItem> items) {
        // Delegated inventory check logic
        return inventoryService.checkAvailability(items);
    }
}
```

**Why compliant:** Early returns reduce nesting and make the validation flow clear. Each validation concern is separated into its own method. The main method reads like a checklist. Cyclomatic complexity is distributed across focused methods.

---

## VIOLATION: God Class with Mixed Responsibilities

```java
@Service
public class OrderManager {

    @Autowired private JdbcTemplate jdbcTemplate;
    @Autowired private JavaMailSender mailSender;
    @Autowired private RestTemplate restTemplate;

    public Order createOrder(OrderRequest request) {
        // Validation logic mixed in
        if (request.getItems() == null || request.getItems().isEmpty()) {
            throw new ValidationException("Items required");
        }
        for (var item : request.getItems()) {
            if (item.getQuantity() <= 0) {
                throw new ValidationException("Invalid quantity");
            }
            if (item.getPrice().compareTo(BigDecimal.ZERO) <= 0) {
                throw new ValidationException("Invalid price");
            }
        }

        // Direct database access
        var orderId = UUID.randomUUID();
        jdbcTemplate.update(
            "INSERT INTO orders (id, customer_id, status, created_at) VALUES (?, ?, ?, ?)",
            orderId, request.getCustomerId(), "CREATED", Instant.now()
        );

        for (var item : request.getItems()) {
            jdbcTemplate.update(
                "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)",
                orderId, item.getProductId(), item.getQuantity(), item.getPrice()
            );
        }

        // Inventory check via HTTP
        var inventoryResponse = restTemplate.getForObject(
            "http://inventory-service/check?productIds=" +
            request.getItems().stream()
                .map(i -> i.getProductId().toString())
                .collect(Collectors.joining(",")),
            InventoryResponse.class
        );

        if (!inventoryResponse.isAvailable()) {
            // Rollback manually
            jdbcTemplate.update("DELETE FROM order_items WHERE order_id = ?", orderId);
            jdbcTemplate.update("DELETE FROM orders WHERE id = ?", orderId);
            throw new InventoryException("Insufficient stock");
        }

        // Email sending logic
        var message = mailSender.createMimeMessage();
        try {
            var helper = new MimeMessageHelper(message, true);
            helper.setTo(request.getCustomerEmail());
            helper.setSubject("Order Confirmation #" + orderId);
            helper.setText(buildEmailBody(request, orderId), true);
            mailSender.send(message);
        } catch (MessagingException e) {
            // Swallowed exception - order continues anyway
        }

        // Logging directly
        System.out.println("Order created: " + orderId);

        // Building response with inline calculation
        var total = request.getItems().stream()
            .map(i -> i.getPrice().multiply(BigDecimal.valueOf(i.getQuantity())))
            .reduce(BigDecimal.ZERO, BigDecimal::add);

        var tax = total.multiply(new BigDecimal("0.08"));
        var shipping = total.compareTo(new BigDecimal("50")) > 0
            ? BigDecimal.ZERO
            : new BigDecimal("5.99");

        return new Order(orderId, request.getCustomerId(), total.add(tax).add(shipping));
    }

    private String buildEmailBody(OrderRequest request, UUID orderId) {
        // 200+ lines of HTML template building...
        return "<html>...</html>";
    }

    // 30+ more methods covering reporting, analytics, refunds, etc.
}
```

**Why violates ENG-3.1:** This class handles validation, persistence, HTTP calls, email sending, logging, and price calculation. It has over 30 methods and knows about too many concerns. Changes to email templates require modifying this class. Testing requires mocking 10+ dependencies. The createOrder method alone has cyclomatic complexity > 15.

---

## VIOLATION: Deeply Nested Conditionals

```java
@Service
public class ShippingCalculator {

    public ShippingQuote calculateShipping(ShippingRequest request) {
        BigDecimal cost = BigDecimal.ZERO;

        if (request != null) {
            if (request.getDestination() != null) {
                if (request.getDestination().getCountry() != null) {
                    if (request.getDestination().getCountry().equals("US")) {
                        if (request.getWeight() != null) {
                            if (request.getWeight() <= 1.0) {
                                if (request.isExpedited()) {
                                    cost = new BigDecimal("12.99");
                                } else {
                                    if (request.getDestination().isRural()) {
                                        cost = new BigDecimal("7.99");
                                    } else {
                                        cost = new BigDecimal("5.99");
                                    }
                                }
                            } else if (request.getWeight() <= 5.0) {
                                if (request.isExpedited()) {
                                    cost = new BigDecimal("24.99");
                                } else {
                                    if (request.getDestination().isRural()) {
                                        cost = new BigDecimal("14.99");
                                    } else {
                                        cost = new BigDecimal("9.99");
                                    }
                                }
                            } else {
                                // Even more nesting for heavy packages...
                            }
                        }
                    } else if (request.getDestination().getCountry().equals("CA")) {
                        // Similar deep nesting for Canada...
                    } else {
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

```java
@Service
@RequiredArgsConstructor
public class ShippingCalculator {

    private final ShippingRateRepository rateRepository;
    private final ShippingZoneResolver zoneResolver;

    public ShippingQuote calculateShipping(ShippingRequest request) {
        validateRequest(request);

        var zone = zoneResolver.resolveZone(request.getDestination());
        var weightTier = WeightTier.fromWeight(request.getWeight());
        var serviceLevel = request.isExpedited() ? ServiceLevel.EXPRESS : ServiceLevel.STANDARD;

        var rate = rateRepository.findRate(zone, weightTier, serviceLevel)
            .orElseThrow(() -> new ShippingNotAvailableException(zone, weightTier));

        return ShippingQuote.builder()
            .baseCost(rate.getBaseCost())
            .ruralSurcharge(calculateRuralSurcharge(request.getDestination(), rate))
            .estimatedDays(rate.getEstimatedDays())
            .build();
    }

    private void validateRequest(ShippingRequest request) {
        Objects.requireNonNull(request, "Shipping request required");
        Objects.requireNonNull(request.getDestination(), "Destination required");
        Objects.requireNonNull(request.getWeight(), "Weight required");
    }

    private BigDecimal calculateRuralSurcharge(Address destination, ShippingRate rate) {
        return destination.isRural() ? rate.getRuralSurcharge() : BigDecimal.ZERO;
    }
}

public enum WeightTier {
    LIGHT(0, 1.0),
    MEDIUM(1.0, 5.0),
    HEAVY(5.0, 20.0),
    FREIGHT(20.0, Double.MAX_VALUE);

    private final double minWeight;
    private final double maxWeight;

    public static WeightTier fromWeight(double weight) {
        return Arrays.stream(values())
            .filter(tier -> weight > tier.minWeight && weight <= tier.maxWeight)
            .findFirst()
            .orElse(FREIGHT);
    }
}
```

**Why compliant:** Logic is flat with minimal nesting. Rates are stored in a database rather than hardcoded conditionals. Enums encapsulate weight tier logic. Each method has a single responsibility and low cyclomatic complexity. Adding new zones or tiers requires only database entries, not code changes.

---

## COMPLIANT: Using Records for Immutable Data Transfer

```java
public record OrderSummary(
    UUID orderId,
    String customerName,
    List<LineItemSummary> items,
    MonetaryAmount subtotal,
    MonetaryAmount tax,
    MonetaryAmount total,
    OrderStatus status,
    Instant createdAt
) {
    public OrderSummary {
        Objects.requireNonNull(orderId, "Order ID required");
        Objects.requireNonNull(items, "Items required");
        items = List.copyOf(items); // Defensive copy for immutability
    }

    public static OrderSummary fromOrder(Order order, TaxCalculator taxCalc) {
        var subtotal = order.calculateSubtotal();
        var tax = taxCalc.calculate(subtotal, order.getShippingAddress());

        return new OrderSummary(
            order.getId(),
            order.getCustomer().getFullName(),
            order.getItems().stream().map(LineItemSummary::from).toList(),
            subtotal,
            tax,
            subtotal.add(tax),
            order.getStatus(),
            order.getCreatedAt()
        );
    }
}

public record LineItemSummary(
    String productName,
    int quantity,
    MonetaryAmount unitPrice,
    MonetaryAmount lineTotal
) {
    public static LineItemSummary from(OrderItem item) {
        return new LineItemSummary(
            item.getProduct().getName(),
            item.getQuantity(),
            item.getUnitPrice(),
            item.calculateLineTotal()
        );
    }
}
```

**Why compliant:** Records eliminate boilerplate (getters, equals, hashCode, toString). Immutability prevents accidental state changes. Factory methods encapsulate construction logic. Each record has a focused purpose as a data carrier.
