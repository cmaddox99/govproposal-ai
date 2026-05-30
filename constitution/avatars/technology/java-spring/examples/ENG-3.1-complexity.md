# ENG-3.1 — Complexity Limits (Java/Spring, AA BFF Fleet)

> **AA fleet context:** 6 of 25 BFF repos contain files exceeding 1,000 LOC. MobileUtils.java (2,287 LOC) is the fleet's largest god class. Complexity concentration is the primary driver of 30+ confirmed bugs.

## Hard Limits

| Unit | Limit | Rationale |
|------|-------|-----------|
| Class | 300 LOC | Beyond this, test coverage collapses (confirmed: God classes avg < 3.5 test coverage score) |
| Method | 30 LOC | AA's 177-line `mapFlifoResponse()` is unmaintainable — confirmed MEDIUM defect |
| Cyclomatic complexity | 10 per method | Beyond 10: branch coverage becomes impossible |

## AA BFF Fleet — Real God Class Evidence (March 2026)

| Repo | File | LOC | Confirmed Bugs |
|------|------|-----|----------------|
| Minilith | `MobileUtils.java` | 2,287 | 4 (regex split, inverted credit card check, NumberFormatException, charAt(0) on empty) |
| aa-ct-mobile-airship | `CuratedFlightEvent.java` | 2,139 | 3 (ClassCastException, NPE on FF stream, redundant collect/stream) |
| aa-ct-mobile-manage-bff | (via god pattern) | — | O(n³) triple-nested loops in SeatsBuilder |
| mobile-iu-bff | `ConfirmationAnalyticsBuilder.java` | 1,564 | 3 (pass-by-value 12-param, 3× duplicate setPnrInfo, cabinType always null) |
| Minilith | `ReservationResponseBuilder.java` | 1,654 | 2 NPEs confirmed |

**Pattern:** Every god class in the fleet has at least 2 confirmed bugs. There are no exceptions.

## Decomposition Rule

```java
// ❌ God builder — DO NOT ADD TO
class TravelHubResponseBuilderV2 { // 655 LOC
    // + V3 (653 LOC) + V4 (612 LOC) = 1,763 LOC for one concept
}

// ✅ Extract to abstract base + version-specific overrides
abstract class TravelHubResponseBuilder {
    abstract List<TravelSegment> buildSegments(TravelData data);
    // shared logic once, ~660 LOC total (62% reduction)
}
```

> Full complexity patterns in `ENG-3.1-complexity-detail.md`.
