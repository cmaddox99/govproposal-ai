---
law_id: ENG-3.3
avatar: java-spring
---

# ENG-3.3: Law of Demeter Examples for Java Spring

## VIOLATION: Train Wreck Chain (reaching through objects)

```java
public class City {
    private String name;
    private String state;

    public String getName() { return name; }
    public String getState() { return state; }
}

public class Address {
    private String street;
    private City city;
    private String zipCode;

    public String getStreet() { return street; }
    public City getCity() { return city; }
    public String getZipCode() { return zipCode; }
}

public class Customer {
    private String name;
    private Address address;

    public String getName() { return name; }
    public Address getAddress() { return address; }
}

public class Order {
    private UUID id;
    private Customer customer;
    private BigDecimal total;

    public UUID getId() { return id; }
    public Customer getCustomer() { return customer; }
    public BigDecimal getTotal() { return total; }
}

// VIOLATION: service reaches deep into the object graph
@Service
@RequiredArgsConstructor
public class ShippingLabelService {

    public String generateLabel(Order order) {
        // "Train wreck" - chaining through 3 levels of getters
        String cityName = order.getCustomer().getAddress().getCity().getName();
        String state = order.getCustomer().getAddress().getCity().getState();
        String street = order.getCustomer().getAddress().getStreet();
        String zip = order.getCustomer().getAddress().getZipCode();

        return String.format("%s\n%s\n%s, %s %s",
            order.getCustomer().getName(), street, cityName, state, zip);
    }
}
```

**Why violates ENG-3.3:** `ShippingLabelService.generateLabel` is coupled to the internal structure of `Order`, `Customer`, `Address`, and `City`. The getter chain `order.getCustomer().getAddress().getCity().getName()` means this service must know how every intermediate object is composed. If `Address` changes to embed `City` inside a `Region` object, every caller navigating this chain breaks.

---

## COMPLIANT: Encapsulated Access via Domain Methods

```java
public class City {
    private String name;
    private String state;

    public String getName() { return name; }
    public String getState() { return state; }
}

public class Address {
    private String street;
    private City city;
    private String zipCode;

    public String getCityName() {
        return city.getName();
    }

    public String getFormatted() {
        return String.format("%s\n%s, %s %s",
            street, city.getName(), city.getState(), zipCode);
    }
}

public class Customer {
    private String name;
    private Address address;

    public String getName() { return name; }

    public String getShippingAddress() {
        return String.format("%s\n%s", name, address.getFormatted());
    }
}

public class Order {
    private UUID id;
    private Customer customer;
    private BigDecimal total;

    public String getDeliveryCity() {
        return customer.getAddress().getCityName();
    }

    public String getShippingLabel() {
        return customer.getShippingAddress();
    }
}

// COMPLIANT: service only talks to its direct collaborator
@Service
@RequiredArgsConstructor
public class ShippingLabelService {

    public String generateLabel(Order order) {
        // Single method call on direct collaborator
        return order.getShippingLabel();
    }
}
```

**Why compliant:** Each class exposes behavior relevant to its callers without leaking internal structure. `ShippingLabelService` only talks to `Order`. `Order` delegates to `Customer`. `Customer` delegates to `Address`. Internal restructuring of `Address` only affects `Address` methods.

---

## Spring Service Layer Example

```java
// VIOLATION: controller reaches through service and domain objects
@RestController
@RequestMapping("/api/orders")
@RequiredArgsConstructor
public class OrderControllerBad {

    private final OrderService orderService;

    @GetMapping("/{orderId}/delivery-city")
    public ResponseEntity<Map<String, String>> getDeliveryCity(
            @PathVariable UUID orderId) {
        Order order = orderService.findById(orderId);
        // Reaching through the entire object graph from the controller
        String city = order.getCustomer().getAddress().getCity().getName();
        return ResponseEntity.ok(Map.of("city", city));
    }
}

// COMPLIANT: controller uses encapsulated domain method
@RestController
@RequestMapping("/api/orders")
@RequiredArgsConstructor
public class OrderControllerGood {

    private final OrderService orderService;

    @GetMapping("/{orderId}/delivery-city")
    public ResponseEntity<Map<String, String>> getDeliveryCity(
            @PathVariable UUID orderId) {
        Order order = orderService.findById(orderId);
        // Only talks to direct collaborator
        return ResponseEntity.ok(Map.of("city", order.getDeliveryCity()));
    }
}

// COMPLIANT: service encapsulates complex operations
@Service
@RequiredArgsConstructor
public class OrderService {

    private final OrderRepository orderRepository;

    public Order findById(UUID orderId) {
        return orderRepository.findById(orderId)
            .orElseThrow(() -> new OrderNotFoundException(orderId));
    }

    public String getDeliveryCity(UUID orderId) {
        return findById(orderId).getDeliveryCity();
    }
}
```

---

## Why It Matters

The Law of Demeter reduces **coupling between components**. When code reaches through chains like `order.getCustomer().getAddress().getCity().getName()`, it creates invisible dependencies on the internal structure of every object in that chain. This leads to:

- **Fragile code:** A structural change in any intermediate object breaks all callers
- **Hidden dependencies:** The service secretly depends on Customer, Address, and City, but only declares a dependency on Order
- **Difficult testing:** Tests must construct deep object graphs with mocks returning mocks
- **Ripple effects:** Refactoring one entity forces changes across controllers, services, and other domain objects

---

## The Rule

A method `M` of object `O` should only call methods on:

1. **`O` itself** - the object's own methods
2. **Objects passed as parameters to `M`** - direct arguments
3. **Objects created within `M`** - locally instantiated objects
4. **`O`'s direct component objects** - fields and injected dependencies

Any other access (reaching through a collaborator's return value to call a method on a stranger) violates the law and should be refactored into a method on the direct collaborator.
