# Test Pyramid Law

**Purpose:** Understand the testing strategy and coverage requirements that ensure reliable, maintainable test suites.

**Constitutional Reference:** Article IV, Sections 4.2-4.3, 4.10  
**Time to Read:** 20 minutes

---

## The Law

> **The test suite SHALL maintain a pyramid distribution with unit tests as the foundation.**

---

## The Test Pyramid

```
                    △                    5-10%    E2E Tests
                   ███                   
                  █████                  15-25%   Integration Tests
                 ███████                          (Controller Layer ONLY)
               ███████████               
             ███████████████             10-15%   Contract Tests
           ███████████████████                    (WireMock for external APIs)
         ███████████████████████         
       ███████████████████████████       70-80%   Unit Tests
     ███████████████████████████████              (Fast, No Spring)
```

---

## Test Types and Distribution

### 70-80% Unit Tests

**Characteristics:**
- ✅ No Spring context - Pure Java
- ✅ No mocking domain objects - Use real entities
- ✅ Mock only external I/O - Email, SOAP, REST clients
- ✅ Fast execution - <10ms per test
- ✅ Focused - Test single method/class

**Location:** `src/test/java/com/example/services/`

**Example:**
```java
@ExtendWith(MockitoExtension.class)
public class PalApplicationServiceTest {

    @InjectMocks
    private PalApplicationServiceImpl service;

    // Mock ONLY external I/O boundaries
    @Mock private GraphMailService graphMailService;
    @Mock private ICargoClient iCargoClient;

    // Use REAL domain objects
    private PalApplicationRepository repository = new InMemoryPalApplicationRepository();

    @Test
    public void createApplication_validRequest_returnsSuccess() {
        // GIVEN - Real domain objects
        CreateApplicationRequest request = PalApplicationBuilder.validRequest().build();
        when(graphMailService.sendEmail(any())).thenReturn(true);

        // WHEN - Call real service
        ApplicationResponse response = service.createApplication(request);

        // THEN - Assert behavior
        assertThat(response.isSuccess()).isTrue();
        assertThat(response.getOrderId()).isNotNull();
    }
}
```

### 15-25% Integration Tests (Controller Layer ONLY)

**Characteristics:**
- ✅ Full Spring context - `@SpringBootTest` or `@WebMvcTest`
- ✅ Test via HTTP - MockMvc or TestRestTemplate
- ✅ Mock external dependencies - iCargo service, email
- ✅ Real database - H2 or Testcontainers
- ✅ Complete workflows - Test user journeys

**Location:** `src/test/java/com/example/controller/`

**Example:**
```java
@WebMvcTest(PalApplicationController.class)
@AutoConfigureMockMvc(addFilters = false)
public class PalApplicationControllerIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private PalApplicationService orderService;

    @Test
    public void createApplication_validRequest_returns201() throws Exception {
        // GIVEN
        when(orderService.createApplication(any()))
            .thenReturn(successResponse());

        // WHEN/THEN
        mockMvc.perform(post("/api/orders")
                .contentType(MediaType.APPLICATION_JSON)
                .content(validRequestJson()))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.applicationId").exists());
    }
}
```

### 10-15% Contract Tests

**Characteristics:**
- ✅ WireMock for SOAP/REST stubbing
- ✅ Schema validation
- ✅ Error scenario testing
- ✅ No real external calls

**Location:** `src/test/java/com/example/contract/`

**Example:**
```java
@ExtendWith(WireMockExtension.class)
public class ICargoServiceContractTest {

    @RegisterExtension
    static WireMockExtension wireMock = WireMockExtension.newInstance()
        .options(wireMockConfig().dynamicPort())
        .build();

    @Test
    public void lookupCustomer_validRequest_matchesSchema() {
        // GIVEN
        wireMock.stubFor(post("/payments/process")
            .willReturn(ok()
                .withBodyFile("icargo-success-response.json")));

        // WHEN
        ICargoResponse result = client.lookupCustomer(validPaymentRequest());

        // THEN
        assertThat(result.getTransactionId()).isNotNull();
        wireMock.verify(postRequestedFor(urlEqualTo("/payments/process")));
    }
}
```

### 5-10% End-to-End Tests

**Characteristics:**
- ✅ Real UI or API calls
- ✅ Staging environment
- ✅ Critical paths only - 5-10 tests maximum
- ✅ Slow but high confidence

**Location:** `src/test/e2e/` or separate repository

---

## Coverage Requirements

### Thresholds (Strictly Enforced)

| Metric | Minimum | Target | Enforced By |
|--------|---------|--------|-------------|
| Line Coverage | 90% | 95% | Jacoco |
| Branch Coverage | 85% | 90% | Jacoco |
| New Code Coverage | 95% | 100% | PR Review |
| Critical Path Coverage | 100% | 100% | PR Review |
| Mutation Score | 70% | 80% | Pitest |

### Critical Paths (100% Required)

- Financial calculations (pricing, totals, discounts)
- Security and authentication logic
- Data validation and transformation
- External service integrations (payment, shipping)

### Verification Commands

```bash
# Run tests with coverage
./mvnw test jacoco:report

# View coverage report
open target/site/jacoco/index.html

# Run mutation testing
./mvnw org.pitest:pitest-maven:mutationCoverage

# View mutation report
open target/pit-reports/*/index.html
```

### Coverage Exclusions

Configuration in `pom.xml` excludes:
- Configuration classes (`@Configuration`)
- DTOs and entities (getters/setters)
- Main application class
- Exception classes (simple wrappers)

---

## Test Decomposition Law (Section 4.10)

### The Problem

Monolithic integration test classes cause:
- Slow test execution
- Difficult navigation
- Poor test isolation
- Limited parallelization

### The Solution

**Decompose when:**
- Test class exceeds **200 lines**
- Test class contains **more than 8 tests**
- Tests cover **multiple functional boundaries**
- Execution time exceeds **3 seconds**

**Decomposition Strategy:**
```
❌ BEFORE: Monolithic
PalApplicationControllerIntegrationTest (370 lines, 8 tests)
  - Tests for create, confirm, retrieve, cancel

✅ AFTER: Decomposed by Function
OrderCreateIntegrationTest (100 lines, 2 tests)
OrderConfirmIntegrationTest (120 lines, 4 tests)
OrderRetrieveIntegrationTest (80 lines, 2 tests)
OrderCancelIntegrationTest (70 lines, 2 tests)
```

**Shared Setup via Base Class:**
```java
@WebMvcTest(PalApplicationController.class)
@AutoConfigureMockMvc(addFilters = false)
@ActiveProfiles("test")
public abstract class PalApplicationControllerTestBase {
    @Autowired protected MockMvc mockMvc;
    @Autowired protected ObjectMapper objectMapper;
    @MockBean protected PalApplicationService orderService;

    @BeforeEach
    void baseSetUp() {
        Mockito.reset(orderService);
    }
}

public class OrderCreateIntegrationTest
    extends PalApplicationControllerTestBase {
    // Tests for create operations only
}
```

---

## What Goes Where?

| What You're Testing | Test Type | Layer | Spring? | Mocking |
|---------------------|-----------|-------|---------|---------|
| Business logic | Unit | Service | ❌ No | External I/O only |
| Repository queries | Unit | Repository | ❌ No | In-memory DB |
| Transformers/Mappers | Unit | Util | ❌ No | None |
| REST endpoints | Integration | Controller | ✅ Yes | Service layer |
| Security/Auth | Integration | Controller | ✅ Yes | User context |
| Complete workflows | Integration | Controller | ✅ Yes | External deps |
| Payment gateway contract | Contract | N/A | ❌ No | WireMock |
| Email service contract | Contract | N/A | ❌ No | WireMock |
| User journeys | E2E | Full Stack | ✅ Yes | None |

---

## Common Mistakes

### ❌ Mistake #1: Integration Tests at Service Layer

```java
// WRONG - Too heavy for service tests!
@SpringBootTest
public class PalApplicationServiceIntegrationTest {
    @Autowired private PalApplicationService service;
}
```

**Fix:** Use pure Java unit tests at service layer.

### ❌ Mistake #2: Mocking Domain Objects

```java
// WRONG - Don't mock domain!
@Mock private PalApplication application;
@Mock private PalApplicationRepository repository;
```

**Fix:** Use real domain objects, mock only external I/O.

### ❌ Mistake #3: Inverted Pyramid (Mostly Integration)

```
     █████████████████████████████████   85%   Integration Tests
       ███████████████████████████       15%   Unit Tests
```

**Fix:** Increase unit tests to 70-80%, reduce integration tests.

### ❌ Mistake #4: Testing Implementation Details

```java
// WRONG - Testing HOW, not WHAT
verify(repository).save(any());
verify(graphMailService, times(1)).send(any());
```

**Fix:** Assert on observable behavior, not mock interactions.

---

## Decision Tree

```
Am I testing...

├─ Business logic in service layer?
│  └─ → Unit test (no Spring, mock external I/O only)

├─ REST API endpoint?
│  └─ → Integration test (@WebMvcTest, MockMvc)

├─ External SOAP/REST contract?
│  └─ → Contract test (WireMock)

├─ Complete user journey?
│  └─ → E2E test (full stack, staging env)

└─ Repository query?
   └─ → Unit test (in-memory DB or test doubles)
```

---

## Prompt Examples

### Asking About Test Type

```
Prompt: "I need to test the PAL application submission. What type of test?"

AI Response: "Following the Test Pyramid Law (Article IV, Section 4.2):

             **Business Logic → Unit Test**
             - Test service method `submitApplication()`
             - No Spring context
             - Mock only external I/O (email service)

             **HTTP Endpoint → Integration Test**
             - Test POST /orders/{id}/submit
             - Use @WebMvcTest
             - Mock service layer

             **iCargo Service → Contract Test**
             - Test payment processing contract
             - Use WireMock

             Let's start with the unit test for business logic.
             Following Atomic TDD, here's a failing test..."
```

### Asking About Coverage

```
Prompt: "Current coverage is 75%. How do I get to 90%?"

AI Response: "Following the Coverage Laws (Article IV, Section 4.3):

             Current: 75% | Target: 90% | Gap: 15%

             **Step 1: Identify uncovered code**
             ```bash
             ./mvnw test jacoco:report
             open target/site/jacoco/index.html
             ```

             **Step 2: Prioritize by risk**
             - Financial calculations (must be 100%)
             - Validation logic (must be 100%)
             - Error handling paths
             - Edge cases

             **Step 3: Write characterization tests**
             For each uncovered method, write tests that:
             - Cover happy path
             - Cover error conditions
             - Cover edge cases

             Shall I help identify the specific uncovered areas?"
```

---

## Related Guides

- [Testing Architecture](../testing/testing-architecture.md) - Detailed testing patterns
- [Characterization Testing](../testing/characterization-testing.md) - Testing legacy code
- [Atomic TDD Workflow](../testing/atomic-tdd-workflow.md) - Writing tests
- [WireMock Contract Testing](../testing/wiremock-contract-testing.md) - Contract tests

---

**Constitutional Reference:** Article IV, Sections 4.2-4.3, 4.10  
**Last Updated:** January 27, 2026
