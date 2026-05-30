# ENG-2.1 — DDD Aggregate Root (Java/Spring, AA BFF Context)

> **AA fleet reality:** 19 of 25 BFF repos use anemic domain models — POJOs as data bags, all logic in `*Builder` and `*Utils` classes. This is the fleet's lowest-scoring dimension (OOD: 4.2/10) and the root cause of most complexity violations.

## The Problem

```java
// ❌ Anemic — all behavior lives in ReshopBuilder, not in the domain object
class ReshopFare {
    private BigDecimal amount;
    // getters/setters only — zero behavior
}
// ReshopBuilder.java: 1,200 lines of procedural logic operating on data bags
```

## The Correct Pattern

```java
// ✅ Rich domain object — behavior lives with data
public class Fare {
    private final BigDecimal amount; // always BigDecimal(String), never BigDecimal(double)

    public Fare add(Fare other) {
        return new Fare(this.amount.add(other.amount));
    }

    public boolean exceeds(Fare threshold) {
        return this.amount.compareTo(threshold.amount) > 0;
    }
}
```

## AA BFF God-Class Evidence (ENG-3.1 cross-reference)

| File | LOC | Anti-Pattern | Consequence |
|------|-----|-------------|-------------|
| `MobileUtils.java` | 2,287 | 121 static methods — session mgmt + email + payment + encoding | Zero testability — no DI, no mocking |
| `CuratedFlightEvent.java` | 2,139 | Push notification enrichment + loyalty + CC + booking in one class | 4 `ClassCastException` risks confirmed |
| `ReservationResponseBuilder.java` | 1,654 | Builds flights + queries FLIFO + eligibility + disruption mapping | ServiceLocator calls hidden inside — untestable |
| `ConfirmationAnalyticsBuilder.java` | 1,564 | Analytics for booking + pass-by-value 12-param method | Analytics data silently lost (CRITICAL bug) |

## Rule

**One aggregate, one responsibility.** If you can describe the class with "and" you have at least two classes.

> Full DDD patterns in `ENG-2.1-aggregates-detail.md`.
