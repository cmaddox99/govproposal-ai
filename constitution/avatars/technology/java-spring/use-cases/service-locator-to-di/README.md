# Use Case: ServiceLocator → Constructor Injection Migration

**Avatar:** avatar-java-spring  
**Laws:** ENG-2.2 (Layered Architecture), ENG-4.1 (Atomic TDD)  
**AA Evidence:** Mobile-Manage-Minilith — `ReservationResponseBuilder.java` (1,654 LOC)  
**Risk level:** High — ServiceLocator makes unit testing impossible without PowerMock

## Context

Mobile-Manage-Minilith uses ServiceLocator pervasively across its core builders:

```java
// Current state — Minilith ReservationResponseBuilder.java
boolean eligible = ServiceLocator.getCheckInEligibilityManager()
    .isCarrierConnectEligible(request, userAgent);
boolean flifoEligible = ServiceLocator.getFlightStatusManager()
    .isFlightStatusEligible(flightId);
```

**Problems:**
1. No way to mock `CheckInEligibilityManager` in unit tests without PowerMockito hacks
2. `ReservationResponseBuilder` has hidden, unbounded dependencies — each `ServiceLocator.get*()` call is an invisible coupling
3. Circular dependency risk: ServiceLocator resolves at runtime, not compile time

## Migration Strategy (Incremental — ENG-11.1 gate required)

**Step 1 — Add constructor while keeping ServiceLocator (bridge state)**

```java
@Service
public class ReservationResponseBuilder {
    private final CheckInEligibilityManager eligibilityManager;
    private final FlightStatusManager flightStatusManager;

    // New constructor — Spring will wire this
    @Autowired
    public ReservationResponseBuilder(
            CheckInEligibilityManager eligibilityManager,
            FlightStatusManager flightStatusManager) {
        this.eligibilityManager = eligibilityManager;
        this.flightStatusManager = flightStatusManager;
    }

    public ReservationResponse build(ReservationRequest request) {
        // Now use injected fields — not ServiceLocator
        boolean eligible = eligibilityManager.isCarrierConnectEligible(request, userAgent);
    }
}
```

**Step 2 — Write the test that was impossible before**

```java
@ExtendWith(MockitoExtension.class)
class ReservationResponseBuilderTest {
    @Mock CheckInEligibilityManager eligibilityManager;
    @Mock FlightStatusManager flightStatusManager;
    @InjectMocks ReservationResponseBuilder builder;

    @Test
    void build_returnsEligibleWhenCarrierConnectEnabled() {
        given(eligibilityManager.isCarrierConnectEligible(any(), any())).willReturn(true);
        ReservationResponse response = builder.build(sampleRequest());
        assertThat(response.isCarrierConnectEligible()).isTrue();
    }
}
```

**Step 3 — Delete ServiceLocator call after test is green**

Only remove the ServiceLocator call after the test proves the constructor-injected version behaves correctly. Do not delete both at once.

## Success Criteria

- Zero `ServiceLocator.get*()` calls in the migrated class
- Test coverage ≥ 90% for the migrated class
- No PowerMockito or Mockito `mockStatic()` in the test suite

## AA Scope Estimate

Minilith has 16 confirmed `ServiceLocator.get*()` call sites across 5 core builders. Full migration = ~3 weeks, 1 engineer, incremental delivery per class.
