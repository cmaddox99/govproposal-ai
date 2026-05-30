# ENG-4.1 — Atomic TDD (Java/Spring, AA BFF Context)

> **AA fleet baseline:** 5 repos score ≤3.0 on test coverage. God classes are the primary cause — untestable by design. `./mvnw test` must pass with coverage report before merge.

## The Atomic TDD Cycle

```
1. Write ONE failing test
2. Write ONLY enough code to make it pass
3. Refactor — keep green
4. Repeat
```

**Coverage floor:** ≥90% line, ≥70% branch. `./mvnw test jacoco:report` enforces it.

## AA BFF Pattern — Service Layer Test

```java
// ✅ Test first, one behavior at a time
@ExtendWith(MockitoExtension.class)
class FareServiceTest {

    @Mock CheckInManager checkInManager;
    @InjectMocks FareService fareService;

    @Test
    void calculateFareDifference_usesBigDecimalStringNotDouble() {
        // BigDecimal(String) — not BigDecimal(double) which loses precision
        // CRITICAL: mobile-change-bff ReshopBuilder bug — BigDecimal(0.1) != 0.1 exactly
        Fare base  = new Fare(new BigDecimal("299.99"));
        Fare newF  = new Fare(new BigDecimal("349.99"));

        Money diff = fareService.calculateDifference(base, newF);

        assertThat(diff.amount()).isEqualByComparingTo("50.00");
    }
}
```

## HARD_BLOCK — What Kills Test Coverage

| Pattern | Impact | AA Example |
|---------|--------|-----------|
| ServiceLocator deps | Cannot mock without PowerMock hacks | Minilith `ReservationResponseBuilder` |
| Static utility methods | Cannot mock | `MobileUtils` 121 static methods |
| O(n³) loops | Combinatorial test explosion | `SeatsBuilder` triple-nested |
| God class (>300 LOC) | Too many branches to cover | Every Red-tier repo |

> Full TDD patterns in `ENG-4.1-atomic-tdd-detail.md`.
