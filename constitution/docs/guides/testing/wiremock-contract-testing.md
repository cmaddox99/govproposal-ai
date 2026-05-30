# WireMock Contract Testing Guide

**Purpose:** Learn how to write contract tests for external services (SOAP, REST APIs) using WireMock.

**Constitutional Reference:** Article IV, Section 4.2 (Test Pyramid Law), Article VI, Section 6.3 (Integration Resilience)
**Time to Read:** 30 minutes

---

## What Are Contract Tests?

> **Definition:** Tests that verify your code correctly interacts with external services according to their API contract (schema, protocol, behavior).

**Why Contract Tests?**
- ✅ Catch breaking changes early
- ✅ Test without hitting real external services
- ✅ Fast, reliable, repeatable tests
- ✅ Validate request/response schemas
- ✅ Document API expectations

---

## Contract Testing vs Other Tests

| Test Type | What | Speed | When |
|-----------|------|-------|------|
| **Unit Test** | Internal logic | Fastest | Always |
| **Contract Test** | API integration | Fast | External APIs |
| **Integration Test** | Full workflow | Medium | Major flows |
| **E2E Test** | Real systems | Slowest | Critical paths |

**Contract tests sit between unit and integration tests.**

---

## WireMock Setup

### Add Dependencies

```xml
<!-- pom.xml -->
<dependency>
    <groupId>org.wiremock</groupId>
    <artifactId>wiremock-standalone</artifactId>
    <version>3.3.1</version>
    <scope>test</scope>
</dependency>
```

### Create Test Base Class

```java
@ExtendWith(WireMockExtension.class)
public abstract class ExternalApiContractTestBase {

    @RegisterExtension
    static WireMockExtension wireMock = WireMockExtension.newInstance()
        .options(wireMockConfig()
            .port(8089)
            .usingFilesUnderClasspath("wiremock"))
        .build();

    @Autowired
    protected ICargoClient paymentClient;

    @BeforeEach
    public void setupClient() {
        // Point client to WireMock instead of real API
        paymentClient.setEndpointUrl("http://localhost:8089/payment");
    }
}
```

---

## Creating REST Stubs

### Step 1: Capture Real Response

Call real API once to capture response:

```bash
curl -X POST https://api.payment.com/v1/process \
  -H "Content-Type: application/json" \
  -d '{"amount": 100, "currency": "USD"}' > response.json
```

### Step 2: Save as Test Fixture

```
src/test/resources/wiremock/
  ├── mappings/           ← Stub definitions
  ├── __files/            ← Response bodies
  │   ├── payment/
  │   │   ├── payment-success.json
  │   │   ├── payment-declined.json
  │   │   ├── payment-invalid.json
  │   │   └── error-generic.json
```

**Example Response File:**

```json
// __files/payment/payment-success.json
{
  "transactionId": "TXN-12345",
  "status": "APPROVED",
  "amount": 100.00,
  "currency": "USD",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Step 3: Create Stub Mapping

```java
@Test
public void lookupCustomer_validRequest_returnsTransactionData() {
    // GIVEN - Stub iCargo service
    wireMock.stubFor(post(urlPathEqualTo("/payment/process"))
        .withHeader("Content-Type", containing("application/json"))
        .withRequestBody(matchingJsonPath("$.amount"))
        .willReturn(aResponse()
            .withStatus(200)
            .withHeader("Content-Type", "application/json")
            .withBodyFile("payment/payment-success.json")));

    // WHEN - Call our client
    ICargoResponse result = paymentClient.lookupCustomer(
        new PaymentRequest(100.00, "USD")
    );

    // THEN - Verify we parsed response correctly
    assertThat(result).isNotNull();
    assertThat(result.getTransactionId()).isEqualTo("TXN-12345");
    assertThat(result.getStatus()).isEqualTo(PaymentStatus.APPROVED);
    assertThat(result.getAmount()).isEqualByComparingTo("100.00");
}
```

---

## Testing Order Payment Integration

### iCargo Service Contract

```java
@SpringBootTest
@ExtendWith(WireMockExtension.class)
public class OrderPaymentContractTest extends ExternalApiContractTestBase {

    @Autowired
    private PalApplicationService orderService;

    @Test
    public void submitApplication_validPayment_processesPaymentSuccessfully() {
        // GIVEN - Order with payment info
        PalApplication application = createApplicationWithPaymentInfo();

        // Stub iCargo service
        wireMock.stubFor(post(urlPathEqualTo("/payment/process"))
            .withRequestBody(matchingJsonPath("$.amount"))
            .willReturn(aResponse()
                .withStatus(200)
                .withBodyFile("payment/payment-success.json")));

        // WHEN - Submit order
        PalApplication result = orderService.submitApplication(application.getId());

        // THEN - Payment processed
        assertThat(result.getPaymentStatus()).isEqualTo(PaymentStatus.APPROVED);
        assertThat(result.getTransactionId()).isNotNull();

        // Verify we called iCargo service correctly
        wireMock.verify(postRequestedFor(urlPathEqualTo("/payment/process"))
            .withHeader("Content-Type", equalTo("application/json"))
            .withRequestBody(matchingJsonPath("$.amount")));
    }

    @Test
    public void submitApplication_paymentDeclined_throwsPaymentDeclinedException() {
        // GIVEN
        PalApplication application = createApplicationWithPaymentInfo();

        // Stub declined response
        wireMock.stubFor(post(urlPathEqualTo("/payment/process"))
            .willReturn(aResponse()
                .withStatus(200)
                .withBodyFile("payment/payment-declined.json")));

        // WHEN/THEN - Expect exception
        assertThatThrownBy(() -> orderService.submitApplication(application.getId()))
            .isInstanceOf(PaymentDeclinedException.class)
            .hasMessageContaining("Payment was declined");
    }

    @Test
    public void submitApplication_invalidPaymentData_throwsValidationException() {
        // GIVEN
        PalApplication application = createApplicationWithInvalidPayment();

        // Stub validation error response
        wireMock.stubFor(post(urlPathEqualTo("/payment/process"))
            .willReturn(aResponse()
                .withStatus(400)
                .withBodyFile("payment/payment-invalid.json")));

        // WHEN/THEN
        assertThatThrownBy(() -> orderService.submitApplication(application.getId()))
            .isInstanceOf(ValidationException.class)
            .hasMessageContaining("Invalid payment data");
    }
}
```

---

## Creating SOAP Stubs

### Example SOAP Response

```xml
<!-- __files/customer/customer-lookup-success.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <CustomerResponse xmlns="http://api.example.com/customer/v1">
      <customerId>CUST-123</customerId>
      <customerName>Acme Corporation</customerName>
      <email>contact@acme.com</email>
      <status>ACTIVE</status>
      <creditLimit>100000.00</creditLimit>
    </CustomerResponse>
  </soap:Body>
</soap:Envelope>
```

### SOAP Contract Test

```java
@Test
public void lookupCustomer_validRequest_returnsCustomerData() {
    // GIVEN - Stub SOAP service
    wireMock.stubFor(post(urlPathEqualTo("/soap/customer/lookup"))
        .withHeader("Content-Type", containing("text/xml"))
        .withRequestBody(matchingXPath("//customerId[text()='CUST-123']"))
        .willReturn(aResponse()
            .withStatus(200)
            .withHeader("Content-Type", "text/xml; charset=UTF-8")
            .withBodyFile("customer/customer-lookup-success.xml")));

    // WHEN - Call our client
    Applicant applicant = customerClient.lookupCustomer("CUST-123");

    // THEN - Verify we parsed response correctly
    assertThat(customer).isNotNull();
    assertThat(applicant.getId()).isEqualTo("CUST-123");
    assertThat(applicant.getName()).isEqualTo("Acme Corporation");
    assertThat(applicant.getEmail()).isEqualTo("contact@acme.com");
    assertThat(applicant.getStatus()).isEqualTo(CustomerStatus.ACTIVE);
}
```

---

## Error Response Handling

### HTTP Errors

```java
@Test
public void lookupCustomer_http500_throwsServiceException() {
    wireMock.stubFor(post(urlPathEqualTo("/payment/process"))
        .willReturn(aResponse()
            .withStatus(500)
            .withBody("Internal Server Error")));

    assertThatThrownBy(() -> paymentClient.lookupCustomer(request))
        .isInstanceOf(ServiceException.class)
        .hasMessageContaining("HTTP 500");
}

@Test
public void lookupCustomer_http404_throwsServiceException() {
    wireMock.stubFor(post(urlPathEqualTo("/payment/process"))
        .willReturn(aResponse()
            .withStatus(404)));

    assertThatThrownBy(() -> paymentClient.lookupCustomer(request))
        .isInstanceOf(ServiceException.class)
        .hasMessageContaining("HTTP 404");
}
```

### Timeout

```java
@Test
public void lookupCustomer_timeout_throwsTimeoutException() {
    // GIVEN - Response delayed beyond client timeout
    wireMock.stubFor(post(urlPathEqualTo("/payment/process"))
        .willReturn(aResponse()
            .withStatus(200)
            .withBodyFile("payment/payment-success.json")
            .withFixedDelay(35000))); // 35 seconds (timeout is 30s)

    // WHEN/THEN
    assertThatThrownBy(() -> paymentClient.lookupCustomer(request))
        .isInstanceOf(TimeoutException.class)
        .hasMessageContaining("Payment service timed out");
}
```

---

## Advanced WireMock Features

### Request Matching

```java
// Match exact body
.withRequestBody(equalToJson("{\"amount\": 100}"))

// Match JSON path
.withRequestBody(matchingJsonPath("$.amount"))
.withRequestBody(matchingJsonPath("$[?(@.amount > 0)]"))

// Match XPath for SOAP
.withRequestBody(matchingXPath("//customerId[text()='CUST-123']"))

// Match with namespaces
.withRequestBody(matchingXPath(
    "//ns:customerId[text()='CUST-123']",
    Map.of("ns", "http://api.example.com/customer/v1")
))

// Match with regex
.withRequestBody(matching(".*CUST-\\d{3}.*"))
```

### Response Scenarios (Retry Testing)

```java
// First call fails, second succeeds
wireMock.stubFor(post(urlPathEqualTo("/payment/process"))
    .inScenario("Retry")
    .whenScenarioStateIs(Scenario.STARTED)
    .willReturn(aResponse().withStatus(503))
    .willSetStateTo("First Attempt Failed"));

wireMock.stubFor(post(urlPathEqualTo("/payment/process"))
    .inScenario("Retry")
    .whenScenarioStateIs("First Attempt Failed")
    .willReturn(aResponse()
        .withStatus(200)
        .withBodyFile("payment/payment-success.json")));

// Test retry logic
ICargoResponse result = paymentClient.lookupCustomerWithRetry(request);
assertThat(result).isNotNull(); // Succeeded on second attempt
```

### Verify Call Count

```java
// WHEN
for (int i = 0; i < 3; i++) {
    paymentClient.lookupCustomer(request);
}

// THEN
wireMock.verify(3, postRequestedFor(urlPathEqualTo("/payment/process")));
```

---

## Complete Test Suite Example

```java
@SpringBootTest
@ExtendWith(WireMockExtension.class)
public class OrderPaymentContractTest {

    @RegisterExtension
    static WireMockExtension wireMock = WireMockExtension.newInstance()
        .options(wireMockConfig().port(8089))
        .build();

    @Autowired
    private PalApplicationService orderService;

    @Autowired
    private ICargoClient paymentClient;

    @BeforeEach
    public void setup() {
        paymentClient.setEndpointUrl("http://localhost:8089/payment");
    }

    // Happy path
    @Test
    public void submitApplication_validPayment_success() {
        stubPaymentSuccess();

        PalApplication application = createApplicationWithPayment();
        PalApplication result = orderService.submitApplication(application.getId());

        assertThat(result.getStatus()).isEqualTo(SUBMITTED);
        assertThat(result.getPaymentStatus()).isEqualTo(APPROVED);
    }

    // Payment declined
    @Test
    public void submitApplication_paymentDeclined_fails() {
        stubPaymentDeclined();

        PalApplication application = createApplicationWithPayment();

        assertThatThrownBy(() -> orderService.submitApplication(application.getId()))
            .isInstanceOf(PaymentDeclinedException.class);
    }

    // Invalid payment data
    @Test
    public void submitApplication_invalidPayment_fails() {
        stubPaymentValidationError();

        PalApplication application = createApplicationWithInvalidPayment();

        assertThatThrownBy(() -> orderService.submitApplication(application.getId()))
            .isInstanceOf(ValidationException.class);
    }

    // Timeout
    @Test
    public void submitApplication_paymentTimeout_handlesGracefully() {
        stubPaymentTimeout();

        PalApplication application = createApplicationWithPayment();

        assertThatThrownBy(() -> orderService.submitApplication(application.getId()))
            .isInstanceOf(TimeoutException.class);
    }

    // Service unavailable
    @Test
    public void submitApplication_paymentServiceDown_handlesGracefully() {
        stubServiceUnavailable();

        PalApplication application = createApplicationWithPayment();

        assertThatThrownBy(() -> orderService.submitApplication(application.getId()))
            .isInstanceOf(ServiceUnavailableException.class);
    }

    // Helper methods
    private void stubPaymentSuccess() {
        wireMock.stubFor(post(urlPathEqualTo("/payment/process"))
            .willReturn(aResponse()
                .withStatus(200)
                .withBodyFile("payment/payment-success.json")));
    }

    private void stubPaymentDeclined() {
        wireMock.stubFor(post(urlPathEqualTo("/payment/process"))
            .willReturn(aResponse()
                .withStatus(200)
                .withBodyFile("payment/payment-declined.json")));
    }

    private void stubPaymentValidationError() {
        wireMock.stubFor(post(urlPathEqualTo("/payment/process"))
            .willReturn(aResponse()
                .withStatus(400)
                .withBodyFile("payment/payment-invalid.json")));
    }

    private void stubPaymentTimeout() {
        wireMock.stubFor(post(urlPathEqualTo("/payment/process"))
            .willReturn(aResponse()
                .withStatus(200)
                .withBodyFile("payment/payment-success.json")
                .withFixedDelay(35000)));
    }

    private void stubServiceUnavailable() {
        wireMock.stubFor(post(urlPathMatching("/payment/.*"))
            .willReturn(aResponse().withStatus(503)));
    }
}
```

---

## Best Practices

### 1. Use Realistic Test Data

```json
// ❌ BAD - Fake data
{"customerName": "Test", "email": "test@test.com"}

// ✅ GOOD - Realistic data
{"customerName": "Acme Corporation", "email": "billing@acme.com"}
```

### 2. Test All Response Variations

```
// Happy path
payment-success.json

// Error cases
payment-declined.json
payment-insufficient-funds.json
payment-invalid-card.json

// System errors
error-500.json
error-timeout.json
error-rate-limited.json
```

### 3. Keep Fixtures Organized

```
__files/
  payment/
    success.json
    declined.json
    invalid.json
  customer/
    found.json
    not-found.json
  shipping/
    rates.json
    unavailable.json
```

### 4. Document API Expectations

```java
/**
 * Contract test for iCargo service.
 *
 * API Contract:
 * - Endpoint: POST /payment/process
 * - Content-Type: application/json
 * - Timeout: 30 seconds
 *
 * Request Schema:
 * - amount (required, positive number)
 * - currency (required, 3-letter ISO code)
 * - cardToken (required)
 *
 * Response Schema:
 * - transactionId, status (required)
 * - amount, currency (required)
 *
 * Error Codes:
 * - DECLINED, INSUFFICIENT_FUNDS, INVALID_CARD
 */
@Test
public void lookupCustomer_contract() { }
```

---

## Troubleshooting

### WireMock Not Starting

```java
// Check port not in use
@RegisterExtension
static WireMockExtension wireMock = WireMockExtension.newInstance()
    .options(wireMockConfig()
        .port(8089) // Try different port
        .dynamicPort()) // Or use dynamic
    .build();
```

### Stub Not Matching

Enable verbose logging:
```java
// Check WireMock admin for unmatched requests
// http://localhost:8089/__admin/requests/unmatched
```

### JSON Path Not Matching

Debug by logging actual request body:
```java
wireMock.addRequestListener((request, response) -> {
    System.out.println("Request body: " + request.getBodyAsString());
});
```

---

## AI Prompt Examples

### Creating Contract Tests

```
Prompt: "Help me create a WireMock contract test for the iCargo service"

AI Response: "Following Article IV, Section 4.2 (Test Pyramid), I'll help you
             create a contract test.

             **Step 1: Capture Real Response**
             First, we need a sample response from the payment API...

             **Step 2: Create Fixture**
             Save the response to `__files/payment/payment-success.json`

             **Step 3: Write Test**
             ```java
             @Test
             void lookupCustomer_validRequest_returnsTransactionData() {
                 // Stub, call, assert...
             }
             ```

             **Step 4: Add Error Scenarios**
             - Payment declined
             - Invalid input
             - Timeout

             Shall I generate the complete test class?"
```

---

## Related Guides

- [Testing Architecture](./testing-architecture.md) - Test types and layers
- [Atomic TDD Workflow](./atomic-tdd-workflow.md) - TDD cycle
- [Test Pyramid Law](../constitution/test-pyramid-law.md) - Constitutional requirements
- [Brownfield Adoption](../adoption/brownfield-adoption.md) - Adding tests to legacy code
- [Constitution Overview](../constitution/constitution-overview.md) - All three constitutions

## AA External Service Contracts

Common external services requiring contract tests:

| Service | Product Domain | Contract Focus |
|---------|----------------|----------------|
| **iCargo** | [Cargo & Freight](../../../avatars/product-type/cargo-freight/ADOPTION.md) | AWB creation, tracking, capacity |
| **TSA Vetting** | [Cargo & Freight](../../../avatars/product-type/cargo-freight/ADOPTION.md) | Applicant vetting responses |
| **GraphMailService** | All domains | Email delivery confirmation |
| **Sabre/Amadeus** | [Passenger Booking](../../../avatars/product-type/passenger-booking/ADOPTION.md) | Flight availability, pricing |
| **AAdvantage API** | [Loyalty](../../../avatars/product-type/loyalty-aadvantage/ADOPTION.md) | Miles balance, transactions |

---

## References

**Documentation:**
- WireMock: https://wiremock.org/
- WireMock Spring Boot: https://github.com/maciejwalkowiak/wiremock-spring-boot

**Tools:**
- Postman: https://www.postman.com/ (for testing APIs manually)
- SoapUI: https://www.soapui.org/ (for SOAP testing)

---

**Your contracts = Your integration documentation!**

**Constitutional Reference:** Engineering Constitution, Article IV, Section 4.2, Article VI, Section 6.3
**Last Updated:** January 28, 2026
