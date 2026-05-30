# ENG-3.5 — Naming Conventions (Java/Spring, AA BFF Context)

> **AA fleet finding:** "Getter-named methods that perform HTTP calls" is a confirmed MEDIUM defect in mobile-fly-checkin-bff. Names must communicate what a method does — I/O is never silent.

## Rules

| Unit | Convention | Example |
|------|-----------|---------|
| Class | PascalCase, describes a noun | `FareCalculationService`, not `FareUtil` |
| Method | camelCase, verb+noun | `calculateFareDifference()`, not `getFareDiff()` |
| I/O methods | Prefix with `fetch`, `load`, `call` | `fetchFlightStatus()`, never `getFlightStatus()` if it makes HTTP call |
| Test method | `should_expectedBehavior_givenCondition` | `should_returnEmpty_givenNoPassengers()` |
| Constants | SCREAMING_SNAKE_CASE | `MAX_SEAT_ROWS`, not `MaxSeatRows` |

## AA Fleet Anti-Patterns

```java
// ❌ AA Minilith — getter names hiding network I/O
String status = flightStatusManager.getFlightStatus(flightId);
// ^ This calls an external service. You'd never know from the name.

// ✅ Name communicates I/O
String status = flightStatusManager.fetchFlightStatus(flightId);
```

```java
// ❌ AA fleet — abbreviations and misleading names
void setVld(String v) { ... }       // what is "vld"?
void processAndUpdateAndValidate()  // three responsibilities

// ✅
void setValidationCode(String code) { ... }
void validateFareRules()
```

## Naming Red Flag: "Utils" and "Builder" Classes

`MobileUtils` (2,287 LOC, 121 methods) proves that "Utils" classes have no size limit and no conceptual boundary. Every new `*Utils` class is a god class in waiting — name it after what it actually does instead.

> Full naming catalog in `ENG-3.5-naming-detail.md`.
