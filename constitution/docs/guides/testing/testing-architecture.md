# Testing Architecture Guide

**Purpose:** Understand how to structure tests across layers following Constitutional requirements.

**Constitutional Reference:** Article IV (Testing Laws)
**Time to Read:** 20 minutes

---

## Testing Layer Strategy

### The Core Principle

> **Integration tests should ONLY be written at the controller layer. Below the controller layer, write TRUE unit tests with minimal mocking.**

---

## Test Pyramid Distribution

```
         △              5-10%    E2E Tests (Selenium)
        ███             15-25%   Integration @ Controller (@SpringBootTest)
       █████            10-15%   Contract Tests (WireMock)
    █████████           70-80%   Unit Tests (Pure Java, minimal mocking)
```

This pyramid ensures:
- **Fast feedback** - 70-80% of tests run in milliseconds
- **High coverage** - Unit tests cover business logic thoroughly
- **Confidence** - Integration tests verify components work together
- **Cost-effective** - Expensive tests (E2E) only for critical paths

---

## Layer-by-Layer Testing Guide

### 1️⃣ Unit Tests (Service & Repository Layer)

**Location:** `src/test/java/com/example/services/`

**Characteristics:**
- ✅ **No Spring context** - Pure Java, millisecond execution
- ✅ **No mocking domain/state** - Use real domain objects, DTOs, entities
- ✅ **Mock only external edges** - Email, SOAP clients, external APIs
- ✅ **Fast** - Tests run in <100ms each
- ✅ **Focused** - Test single service method

**What to Mock:**
```java
@Mock private GraphMailService graphMailService;              // External I/O ✓
@Mock private ICargoClient paymentClient;     // External API ✓
@Mock private SpringTemplateEngine templateEngine;    // External library ✓
```

**What to Keep Real:**
```java
private PersistService persistService = new InMemoryPersistService();    // Domain logic ✓
private OrderTransformer transformer = new OrderTransformer();           // Transformer ✓
// All domain entities, DTOs, value objects - keep real!
```

**Example:**
```java
@ExtendWith(MockitoExtension.class)
public class PalApplicationServiceTest {

    @InjectMocks
    private PalApplicationService service;

    // Mock ONLY external edges
    @Mock private GraphMailService graphMailService;
    @Mock private ICargoClient paymentClient;

    // Keep these REAL
    private PersistService persistService = new InMemoryPersistService();

    @Test
    public void createApplication_validRequest_returnsSuccess() {
        // GIVEN - Real domain objects
        OrderRequest request = new OrderRequest();
        request.setItems(List.of(createValidItem()));

        // Mock external I/O only
        when(graphMailService.sendEmail(any(), any(), any(), any())).thenReturn(true);

        // WHEN - Call real service
        ApplicationResponse response = service.createApplication(request);

        // THEN - Assert behavior, NOT mock interactions
        assertThat(response.isSuccess()).isTrue();
        assertThat(response.getOrderId()).isNotNull();
    }
}
```

**❌ DON'T DO THIS:**
```java
// Wrong layer for integration tests!
@SpringBootTest
public class PalApplicationServiceIntegrationTest {
    @Autowired private PalApplicationService service; // ❌ Too heavy!
}
```

---

### 2️⃣ Integration Tests (Controller Layer ONLY)

**Location:** `src/test/java/com/example/controller/`

**Characteristics:**
- ✅ **Full Spring context** - `@SpringBootTest`
- ✅ **Test via HTTP** - `MockMvc` or `TestRestTemplate`
- ✅ **Mock external dependencies** - Third-party APIs, email, iCargo services
- ✅ **Real database** - H2 in-memory or Testcontainers
- ✅ **Complete workflows** - Test full user journeys

**Example:**
```java
@SpringBootTest(webEnvironment = RANDOM_PORT)
@AutoConfigureTestDatabase(replace = Replace.ANY)
@Transactional
public class PalApplicationControllerIntegrationTest {

    @Autowired
    private TestRestTemplate restTemplate;

    @MockBean // Mock external dependency
    private ICargoClient paymentClient;

    @MockBean // Mock external dependency
    private GraphMailService graphMailService;

    @Test
    public void submitApplication_completeJourney_viaRestApi() {
        // GIVEN
        when(graphMailService.sendEmail(any(), any(), any(), any())).thenReturn(true);

        // WHEN - Test via HTTP
        ResponseEntity<ApplicationResponse> response =
            restTemplate.postForEntity(
                "/api/orders",
                createValidRequest(),
                ApplicationResponse.class
            );

        // THEN - Verify HTTP response and side effects
        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.CREATED);
        assertThat(response.getBody().isSuccess()).isTrue();
    }
}
```

---

### 3️⃣ Contract Tests (External APIs)

**Location:** `src/test/java/com/example/contract/`

**Characteristics:**
- ✅ **WireMock** for SOAP/REST stubbing
- ✅ **Schema validation**
- ✅ **Error scenario testing**

**Example:**
```java
@ExtendWith(WireMockExtension.class)
public class ICargoServiceContractTest {

    @WireMockTest
    WireMockServer wireMock;

    @Test
    public void lookupCustomer_validRequest_matchesSchema() {
        // GIVEN - Stub iCargo service response
        wireMock.stubFor(post("/payment/process")
            .willReturn(ok()
                .withHeader("Content-Type", "application/json")
                .withBodyFile("icargo-success-response.json")));

        // WHEN - Call real client pointing to WireMock
        PaymentResponse response = client.lookupCustomer(createValidPayment());

        // THEN - Verify contract
        assertThat(response.getTransactionId()).isNotNull();
        wireMock.verify(postRequestedFor(urlEqualTo("/payment/process")));
    }
}
```

See [WireMock Contract Testing Guide](./wiremock-contract-testing.md) for detailed examples.

---

### 4️⃣ E2E Tests (Full Stack)

**Location:** `src/test/e2e/` or separate repository

**Characteristics:**
- ✅ **Real UI** - Selenium/Cypress
- ✅ **Real backend** - Staging environment
- ✅ **Critical paths only** - 5-10 tests maximum

**When to use:**
- User login/logout flow
- Happy path of core business workflows
- Payment/transaction flows

**When NOT to use:**
- Edge cases (unit tests)
- Error scenarios (unit/integration tests)
- Performance testing (separate tool)

---

## What Goes Where?

| What You're Testing | Test Type | Layer | Spring Context? | Mocking Strategy |
|---------------------|-----------|-------|-----------------|------------------|
| Service business logic | Unit | Service | ❌ No | Mock external edges only |
| Repository queries | Unit | Repository | ❌ No | In-memory DB or test doubles |
| Transformers/Mappers | Unit | Util | ❌ No | No mocking |
| REST endpoints | Integration | Controller | ✅ Yes | Mock external dependencies |
| Security/Auth | Integration | Controller | ✅ Yes | Mock user context |
| Complete workflows | Integration | Controller | ✅ Yes | Mock externals, real DB |
| External API contract | Contract | N/A | ❌ No | WireMock |
| Email service contract | Contract | N/A | ❌ No | WireMock or test doubles |
| User journeys | E2E | Full Stack | ✅ Yes | No mocking |

---

## Common Mistakes to Avoid

### ❌ Mistake #1: Integration Tests at Service Layer
```java
// WRONG - Don't do this!
@SpringBootTest
public class PalApplicationServiceTest {
    @Autowired private PalApplicationService service;
}
```
**Why wrong?** Slow, heavy, unnecessary. Service tests should be pure Java unit tests.

### ❌ Mistake #2: Mocking Domain Objects
```java
// WRONG - Don't mock domain!
@Mock private PalApplication application;
@Mock private PersistService persistService;
```
**Why wrong?** Tests implementation, not behavior. Use real domain objects.

### ❌ Mistake #3: Verify() on Mocks
```java
// WRONG - Don't verify implementation details!
verify(persistService, times(1)).save(any());
```
**Why wrong?** Tests HOW code works, not WHAT it does. Breaks on refactoring.

### ❌ Mistake #4: Testing Multiple Behaviors
```java
// WRONG - Too much in one test!
@Test
public void testEverything() {
    // Tests creation, update, submit, approval...
}
```
**Why wrong?** Hard to debug. One test = one behavior.

---

## Quick Decision Tree

```
Am I testing...
├─ Business logic in service layer?
│  └─ → Unit test (no Spring, mock external edges only)
├─ REST API endpoint?
│  └─ → Integration test (SpringBootTest, MockMvc)
├─ External API contract?
│  └─ → Contract test (WireMock)
└─ Full user journey?
   └─ → E2E test (Selenium, staging env)
```

---

## AI Prompt Examples

### Deciding Test Type

```
Prompt: "I need to test this new service method. What kind of test?"

AI Response: "Following Article IV (Testing Laws), let me analyze:

             **Is this testing business logic?**
             Yes → Unit test (no Spring context)

             **Does it need external systems?**
             - Payment gateway? → Mock with WireMock
             - Email? → Mock the service
             - Database? → Use in-memory H2

             **Is it a REST endpoint?**
             Yes → Integration test at controller layer

             Based on your code, I recommend a unit test:
             ```java
             @ExtendWith(MockitoExtension.class)
             public class YourServiceTest {
                 // ...
             }
             ```"
```

### Fixing Over-Mocking

```
Prompt: "These tests break every time I refactor. Help."

AI Response: "Per Article IV, you may be testing structure instead of behavior.

             **Signs of over-mocking:**
             - `verify()` calls everywhere
             - Mocking domain objects
             - Tests mirror implementation

             **Fix:**
             1. Remove `verify()` calls
             2. Use real domain objects
             3. Assert on outcomes, not interactions

             Let me refactor this test..."
```

---

## Key Takeaways

1. **Unit tests are fast** - No Spring context, no mocking domain/state
2. **Integration tests are at controller layer** - Test via HTTP, mock externals
3. **Mock only I/O boundaries** - Email, SOAP, external APIs
4. **Test behavior, not implementation** - Don't verify mock interactions
5. **70-80% should be unit tests** - Fast, reliable, maintainable

---

## The Three Constitutions and Testing

| Constitution | Testing Focus |
|--------------|---------------|
| [Engineering](../../../laws/engineering/) | Test pyramid, coverage, TDD cycle |
| [Product](../../../laws/product/) | User journey acceptance tests |
| [Business](../../../laws/business/) | Compliance verification tests |

### Aviation Compliance Testing

For systems governed by the [Aviation/FAA Adoption](../../../avatars/industry/aviation-faa/ADOPTION.md), additional testing requirements apply:

| Level | Aviation Requirement |
|-------|---------------------|
| **DO-178C Level A** | MC/DC coverage required |
| **DO-178C Level B** | Decision coverage required |
| **DO-178C Level C** | Statement coverage required |
| **TSA Systems** | Audit trail verification tests |
| **DOT Systems** | Timeline compliance tests (7-day refund) |

### Product Domain Testing Patterns

Each product domain has specific testing patterns:

| Domain | Testing Focus |
|--------|---------------|
| [Cargo & Freight](../../../avatars/product-type/cargo-freight/ADOPTION.md) | PAL vetting, AWB validation, dangerous goods |
| [Passenger Booking](../../../avatars/product-type/passenger-booking/ADOPTION.md) | Fare rules, ancillary pricing, PNR integrity |
| [Loyalty](../../../avatars/product-type/loyalty-aadvantage/ADOPTION.md) | Miles calculations, status qualification |
| [Airport Operations](../../../avatars/product-type/airport-operations/ADOPTION.md) | Crew legality, gate conflicts |
| [Customer Service](../../../avatars/product-type/customer-service/ADOPTION.md) | Refund timelines, compensation calculations |

---

## Related Guides

- [Atomic TDD Workflow](./atomic-tdd-workflow.md) - Test-first development
- [Characterization Testing](./characterization-testing.md) - Testing legacy code
- [WireMock Contract Testing](./wiremock-contract-testing.md) - External API testing
- [Test Pyramid Law](../constitution/test-pyramid-law.md) - Constitutional requirements
- [Aviation/FAA Adoption](../../../avatars/industry/aviation-faa/ADOPTION.md) - Aviation testing standards

---

**Remember:** The goal is fast, reliable tests that enable fearless refactoring!

**Constitutional Reference:** Engineering Constitution, Article IV (Testing Laws)
**Last Updated:** January 28, 2026
