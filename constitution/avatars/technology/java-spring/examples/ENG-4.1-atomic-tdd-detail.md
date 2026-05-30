---
law_id: ENG-4.1
avatar: java-spring
---

# ENG-4.1: Atomic TDD Examples for Java Spring

## COMPLIANT: Single Responsibility Test with Arrange-Act-Assert Pattern

```java
@ExtendWith(MockitoExtension.class)
class OrderServiceTest {

    @Mock
    private OrderRepository orderRepository;

    @Mock
    private InventoryService inventoryService;

    @InjectMocks
    private OrderService orderService;

    @Test
    @DisplayName("Should create order when inventory is available")
    void createOrder_WhenInventoryAvailable_ShouldReturnCreatedOrder() {
        // Arrange
        var customerId = UUID.randomUUID();
        var productId = UUID.randomUUID();
        var quantity = 5;
        var request = new CreateOrderRequest(customerId, productId, quantity);
        var expectedOrder = Order.create(customerId, productId, quantity);

        when(inventoryService.checkAvailability(productId, quantity)).thenReturn(true);
        when(orderRepository.save(any(Order.class))).thenReturn(expectedOrder);

        // Act
        var result = orderService.createOrder(request);

        // Assert
        assertThat(result).isNotNull();
        assertThat(result.getCustomerId()).isEqualTo(customerId);
        assertThat(result.getStatus()).isEqualTo(OrderStatus.CREATED);

        verify(inventoryService).checkAvailability(productId, quantity);
        verify(orderRepository).save(any(Order.class));
    }

    @Test
    @DisplayName("Should throw exception when inventory is insufficient")
    void createOrder_WhenInventoryInsufficient_ShouldThrowException() {
        // Arrange
        var request = new CreateOrderRequest(
            UUID.randomUUID(),
            UUID.randomUUID(),
            100
        );

        when(inventoryService.checkAvailability(any(), anyInt())).thenReturn(false);

        // Act & Assert
        assertThatThrownBy(() -> orderService.createOrder(request))
            .isInstanceOf(InsufficientInventoryException.class)
            .hasMessageContaining("Insufficient inventory");

        verify(orderRepository, never()).save(any());
    }
}
```

**Why compliant:** Each test method verifies exactly one behavior. Tests follow the Arrange-Act-Assert pattern with clear separation. Descriptive names explain the scenario and expected outcome. Mocks isolate the unit under test.

---

## COMPLIANT: Parameterized Test for Multiple Scenarios

```java
@ExtendWith(MockitoExtension.class)
class PriceCalculatorTest {

    @InjectMocks
    private PriceCalculator priceCalculator;

    @ParameterizedTest
    @DisplayName("Should apply correct discount tier based on quantity")
    @CsvSource({
        "1, 100.00, 100.00",    // No discount for single item
        "10, 100.00, 950.00",   // 5% discount for 10+ items
        "50, 100.00, 4500.00",  // 10% discount for 50+ items
        "100, 100.00, 8500.00"  // 15% discount for 100+ items
    })
    void calculateTotal_ShouldApplyCorrectDiscountTier(
            int quantity,
            BigDecimal unitPrice,
            BigDecimal expectedTotal) {
        // Arrange
        var lineItem = new LineItem("PROD-001", quantity, unitPrice);

        // Act
        var result = priceCalculator.calculateTotal(lineItem);

        // Assert
        assertThat(result).isEqualByComparingTo(expectedTotal);
    }

    @ParameterizedTest
    @DisplayName("Should reject invalid quantities")
    @ValueSource(ints = {0, -1, -100})
    void calculateTotal_WithInvalidQuantity_ShouldThrowException(int invalidQuantity) {
        // Arrange
        var lineItem = new LineItem("PROD-001", invalidQuantity, BigDecimal.TEN);

        // Act & Assert
        assertThatThrownBy(() -> priceCalculator.calculateTotal(lineItem))
            .isInstanceOf(IllegalArgumentException.class);
    }
}
```

**Why compliant:** Parameterized tests efficiently test multiple inputs while maintaining single-assertion focus per logical scenario. Each parameter combination tests one specific discount tier behavior.

---

## VIOLATION: Multiple Unrelated Assertions in Single Test

```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @Mock
    private EmailService emailService;

    @Mock
    private AuditService auditService;

    @InjectMocks
    private UserService userService;

    @Test
    void testUserOperations() {
        // Testing user creation
        var createRequest = new CreateUserRequest("john@example.com", "John Doe");
        var user = User.create(createRequest);
        when(userRepository.save(any())).thenReturn(user);

        var createdUser = userService.createUser(createRequest);
        assertThat(createdUser).isNotNull();
        assertThat(createdUser.getEmail()).isEqualTo("john@example.com");
        verify(emailService).sendWelcomeEmail(any());

        // Testing user update
        var updateRequest = new UpdateUserRequest(user.getId(), "Jane Doe");
        when(userRepository.findById(user.getId())).thenReturn(Optional.of(user));

        var updatedUser = userService.updateUser(updateRequest);
        assertThat(updatedUser.getName()).isEqualTo("Jane Doe");
        verify(auditService).logUpdate(any());

        // Testing user deletion
        userService.deleteUser(user.getId());
        verify(userRepository).deleteById(user.getId());
        verify(auditService).logDeletion(any());

        // Testing email validation
        assertThat(userService.isValidEmail("test@test.com")).isTrue();
        assertThat(userService.isValidEmail("invalid")).isFalse();
    }
}
```

**Why violates ENG-4.1:** This test combines four unrelated behaviors (create, update, delete, validation) into one method. When it fails, you cannot quickly identify which operation broke. Tests should be atomic - one behavior per test method. Each operation should be its own test with focused assertions.

---

## VIOLATION: Test Without Clear Arrange-Act-Assert Structure

```java
class PaymentProcessorTest {

    @Test
    void processPayment() {
        var processor = new PaymentProcessor(new MockGateway(), new MockNotifier());
        var result = processor.process(new Payment(100.00, "USD", "card_123"));
        assertTrue(result.isSuccessful());
        var refund = processor.refund(result.getTransactionId(), 50.00);
        assertTrue(refund.isSuccessful());
        assertEquals(50.00, refund.getAmount());
        var status = processor.getStatus(result.getTransactionId());
        assertEquals("PARTIALLY_REFUNDED", status);
        processor.process(new Payment(-10.00, "USD", "card_123"));
        // This should fail but we forgot to assert
    }
}
```

**Why violates ENG-4.1:** No clear AAA structure makes the test hard to read. Multiple operations are chained without separation. The test verifies process, refund, and status check in sequence - if any fails, debugging requires understanding the entire chain. The last operation has no assertion at all.

---

## COMPLIANT: Integration Test with TestContainers

```java
@SpringBootTest
@Testcontainers
@AutoConfigureTestDatabase(replace = Replace.NONE)
class OrderRepositoryIntegrationTest {

    @Container
    @ServiceConnection
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:15-alpine");

    @Autowired
    private OrderRepository orderRepository;

    @Autowired
    private TestEntityManager entityManager;

    @BeforeEach
    void setUp() {
        orderRepository.deleteAll();
    }

    @Test
    @DisplayName("Should find orders by customer ID with pagination")
    void findByCustomerId_ShouldReturnPagedResults() {
        // Arrange
        var customerId = UUID.randomUUID();
        var orders = IntStream.range(0, 25)
            .mapToObj(i -> Order.create(customerId, UUID.randomUUID(), i + 1))
            .toList();
        orderRepository.saveAll(orders);
        entityManager.flush();

        var pageable = PageRequest.of(0, 10, Sort.by("createdAt").descending());

        // Act
        var result = orderRepository.findByCustomerId(customerId, pageable);

        // Assert
        assertThat(result.getContent()).hasSize(10);
        assertThat(result.getTotalElements()).isEqualTo(25);
        assertThat(result.getTotalPages()).isEqualTo(3);
    }
}
```

**Why compliant:** Integration test focuses on one repository method behavior. Uses TestContainers for realistic database testing. Clear AAA structure with proper setup isolation via @BeforeEach.

---

## VIOLATION: Missing Edge Case Tests

```java
class DiscountServiceTest {

    private DiscountService discountService = new DiscountService();

    @Test
    void applyDiscount() {
        // Only tests happy path
        var result = discountService.applyDiscount(100.00, "SAVE10");
        assertEquals(90.00, result);
    }
}
```

**Why violates ENG-4.1:** Only tests the happy path. Missing tests for: invalid/expired codes, null inputs, zero/negative amounts, code case sensitivity, maximum discount limits. Atomic TDD requires comprehensive coverage of edge cases, each in its own focused test.

---

## TDD Cycle Commands

```bash
# RED: Run specific test, see it fail
./mvnw test -Dtest=OrderServiceTest#createOrder_WhenInventoryAvailable_ShouldReturnCreatedOrder

# GREEN: Write code, run test again
./mvnw test -Dtest=OrderServiceTest#createOrder_WhenInventoryAvailable_ShouldReturnCreatedOrder

# REFACTOR: Run all unit tests
./mvnw test

# VERIFY: Check coverage and constitutional compliance
./mvnw test jacoco:report
constitution-lint .

# Commit when green and compliant
git add -A && git commit -m "Add order creation to OrderService"
```
