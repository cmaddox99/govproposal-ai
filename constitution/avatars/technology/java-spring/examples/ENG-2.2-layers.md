# ENG-2.2 — Layered Architecture (Java/Spring, AA BFF Context)

> **AA fleet critical pattern:** ServiceLocator anti-pattern is pervasive in Mobile-Manage-Minilith. It bypasses all architectural layers — dependencies are invisible and unmockable. HARD_BLOCK in any new code.

## Required Layer Boundaries

```
Controller (@RestController)
    ↓
Service (@Service)         ← business logic lives here only
    ↓
Repository (JpaRepository) ← data access only
    ↓
Domain (POJO / record)     ← data + behavior, zero framework annotations
```

## ServiceLocator — HARD_BLOCK Pattern

```java
// ❌ HARD_BLOCK — ServiceLocator in AA Minilith (ReservationResponseBuilder.java)
boolean eligible = ServiceLocator.getCheckInEligibilityManager()
    .isCarrierConnectEligible(request, userAgent); // hidden dep, unmockable

// ✅ Constructor injection — explicit, testable
@Service
public class ReservationService {
    private final CheckInEligibilityManager eligibilityManager;

    public ReservationService(CheckInEligibilityManager eligibilityManager) {
        this.eligibilityManager = eligibilityManager;
    }
}
```

## Thread Safety — Mutable Singleton HARD_BLOCK

```java
// ❌ CRITICAL BUG — found in TravelHubResponseBuilderV2/V3/V4
@Service // Spring singleton — one instance, shared across all threads
class TravelHubResponseBuilderV2 {
    private List<TravelSegment> segments; // mutable instance field = race condition
}

// ✅ All state in method parameters or final fields
@Service
class TravelHubResponseBuilder {
    public TravelHubResponse build(TravelData data) { // data passed in, no instance state
        var segments = buildSegments(data); // local variable
    }
}
```

## `@Autowired` Field Injection — Advisory

AA BFF fleet uses field injection universally. Not a hard block but a known testability limiter — constructor injection is the migration goal for any class under active development.

> Full architecture patterns in `ENG-2.2-layers-detail.md`.
