---
law_id: ENG-3.5
avatar: java-spring
---

# ENG-3.5: Naming Conventions for Java Spring

## Naming Convention Reference

| Element         | Convention            | Example                               |
|-----------------|-----------------------|---------------------------------------|
| Classes         | PascalCase            | `OrderService`, `CargoShipment`       |
| Methods         | camelCase             | `calculateTotal`, `validateEmail`     |
| Variables       | camelCase             | `customerCount`, `orderItems`         |
| Constants       | SCREAMING_SNAKE_CASE  | `MAX_RETRY_COUNT`, `DEFAULT_TIMEOUT`  |
| Interfaces      | PascalCase (no prefix)| `OrderRepository`, not `IOrderRepository` |
| Packages        | all lowercase         | `com.aa.cargo.domain`                 |
| Enums           | PascalCase (values UPPER) | `OrderStatus.PENDING`            |
| Type parameters | Single uppercase letter | `<T>`, `<K, V>`                     |
| Test classes    | Suffix with `Test`    | `OrderServiceTest`                    |

---

## COMPLIANT: Idiomatic Java/Spring Naming

```java
// Package: all lowercase, reverse domain notation
package com.aa.cargo.domain;

import java.math.BigDecimal;
import java.util.List;
import java.util.Objects;

// Constants: SCREAMING_SNAKE_CASE
public final class ShippingConstants {
    public static final int MAX_RETRY_COUNT = 3;
    public static final BigDecimal DEFAULT_TAX_RATE = new BigDecimal("0.08");
    public static final String DEFAULT_CURRENCY = "USD";

    private ShippingConstants() {
        // prevent instantiation
    }
}

// Enum: PascalCase name, UPPER_CASE values
public enum OrderStatus {
    PENDING,
    CONFIRMED,
    SHIPPED,
    DELIVERED
}

// Class: PascalCase
public record Money(BigDecimal amount, String currency) {

    public Money {
        Objects.requireNonNull(amount, "amount must not be null");
        Objects.requireNonNull(currency, "currency must not be null");
    }

    // Method: camelCase
    public Money add(Money other) {
        validateSameCurrency(other);
        return new Money(this.amount.add(other.amount), this.currency);
    }

    public Money multiply(int factor) {
        return new Money(this.amount.multiply(BigDecimal.valueOf(factor)), this.currency);
    }

    // Private method: camelCase
    private void validateSameCurrency(Money other) {
        if (!this.currency.equals(other.currency)) {
            throw new IllegalArgumentException(
                "Cannot operate on %s and %s".formatted(this.currency, other.currency)
            );
        }
    }
}

// Interface: PascalCase, NO "I" prefix
public interface OrderRepository {
    Order findById(UUID orderId);
    void save(Order order);
    List<Order> findByCustomerId(UUID customerId);
}

// Class: PascalCase
public record CargoShipment(
    UUID shipmentId,       // Variable: camelCase
    String origin,
    String destination,
    List<LineItem> items
) {}

// Service class: PascalCase
@Service
@RequiredArgsConstructor
public class OrderService {

    // Variable: camelCase
    private final OrderRepository orderRepository;
    private final TaxCalculator taxCalculator;

    // Method: camelCase, descriptive verb phrase
    public Money calculateTotal(List<LineItem> items) {
        if (items.isEmpty()) {
            return new Money(BigDecimal.ZERO, ShippingConstants.DEFAULT_CURRENCY);
        }

        var subtotal = sumLineItems(items);
        var tax = taxCalculator.calculateTax(subtotal);
        return subtotal.add(tax);
    }

    public boolean validateEmail(String email) {
        return email != null && email.contains("@");
    }

    // Private helper: camelCase
    private Money sumLineItems(List<LineItem> items) {
        return items.stream()
            .map(LineItem::lineTotal)
            .reduce(Money::add)
            .orElse(new Money(BigDecimal.ZERO, ShippingConstants.DEFAULT_CURRENCY));
    }
}
```

```java
package com.aa.cargo.domain;

// Test class: PascalCase with Test suffix
class OrderServiceTest {

    private OrderService orderService;

    @BeforeEach
    void setUp() {
        // Variable: camelCase
        var orderRepository = mock(OrderRepository.class);
        var taxCalculator = mock(TaxCalculator.class);
        orderService = new OrderService(orderRepository, taxCalculator);
    }

    @Test
    void calculateTotal_returnsZero_whenItemsEmpty() {
        var result = orderService.calculateTotal(List.of());
        assertThat(result.amount()).isEqualTo(BigDecimal.ZERO);
    }

    @Test
    void validateEmail_returnsFalse_whenMissingAtSign() {
        assertThat(orderService.validateEmail("invalid")).isFalse();
    }
}
```

**Why compliant:** Classes and interfaces use PascalCase without prefixes. Methods and variables use camelCase. Constants are SCREAMING_SNAKE_CASE. Packages are all lowercase. The interface is named `OrderRepository` rather than `IOrderRepository`. Test classes use the `Test` suffix convention.

---

## VIOLATION: Non-Idiomatic Java Naming

```java
// VIOLATION: Package should be all lowercase, not mixed case
package com.AA.Cargo.Domain;

// VIOLATION: Interface should NOT have "I" prefix (C# convention, not Java)
public interface IOrderRepository {
    Order FindById(UUID orderId);  // VIOLATION: Method should be camelCase
    void Save(Order order);        // VIOLATION: Method should be camelCase
}

// VIOLATION: Class name should be PascalCase, not snake_case
public class order_service {

    // VIOLATION: Constants should be SCREAMING_SNAKE_CASE
    private static final int maxRetryCount = 3;
    private static final String defaultCurrency = "USD";

    // VIOLATION: Field names should be camelCase, not PascalCase
    private final IOrderRepository OrderRepository;
    private final TaxCalculator TaxCalculator;

    // VIOLATION: Constructor parameter should be camelCase
    public order_service(IOrderRepository OrderRepo, TaxCalculator TaxCalc) {
        this.OrderRepository = OrderRepo;
        this.TaxCalculator = TaxCalc;
    }

    // VIOLATION: Method should be camelCase, not PascalCase
    public Money CalculateTotal(List<LineItem> Items) {
        // VIOLATION: Variable should be camelCase, not PascalCase
        BigDecimal SubTotal = BigDecimal.ZERO;

        // VIOLATION: Loop variable should be camelCase
        for (LineItem Item : Items) {
            SubTotal = SubTotal.add(Item.getPrice());
        }

        return new Money(SubTotal, defaultCurrency);
    }

    // VIOLATION: Method should be camelCase, not snake_case
    public boolean validate_email(String email_address) {
        return email_address.contains("@");
    }
}

// VIOLATION: Enum values should be UPPER_CASE
public enum OrderStatus {
    pending,
    confirmed,
    Shipped,
    delivered
}
```

**Why violates ENG-3.5:** This code uses PascalCase for methods (C# style), snake_case for class and method names (Python style), an `I` prefix on interfaces (C# convention), PascalCase for variables and parameters, camelCase for constants, and inconsistent enum value casing. These violations make the code feel foreign to Java developers and conflict with established Java community standards.

---

## Quick Reference

```text
Classes/Interfaces    PascalCase          OrderService, OrderRepository
Methods               camelCase           calculateTotal()
Variables/Fields      camelCase           customerCount, orderItems
Parameters            camelCase           orderId, customerName
Constants             SCREAMING_SNAKE     MAX_RETRY_COUNT
Enum Values           UPPER_CASE          OrderStatus.PENDING
Packages              all lowercase       com.aa.cargo.domain
Type Parameters       Single uppercase    <T>, <K, V>
Test Classes          PascalCase + Test   OrderServiceTest
Interfaces            NO "I" prefix       OrderRepository (not IOrderRepository)
```
