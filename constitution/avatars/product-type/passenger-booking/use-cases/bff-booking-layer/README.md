# Use Case: BFF Booking Layer Intelligence

**Avatar:** avatar-passenger-booking  
**Laws:** PRD-1.1 (Discovery), PRD-4.1 (MVP), ENG-11.1 (SDD Gate)  
**Source:** aa-ct-mobile-booking-bff (7.4/10), mobile-airfare-search-bff (4.8/10), mobile-reservation-bff (5.0/10)  
**Evidence date:** March 2026

## BFF Quality Stratification

| Service | Score | Tier | Recommendation |
|---------|-------|------|----------------|
| `aa-ct-mobile-booking-bff` | **7.4/10** | 🟢 Green | Safe to extend — reference implementation |
| `mobile-reservation-bff` | 5.0/10 | 🟡 Yellow | Stable, but don't add complexity |
| `mobile-airfare-search-bff` | 4.8/10 | 🟡 Yellow | **Currency precision bug confirmed — CRITICAL** |

## Critical Bug: Currency Precision in Airfare Search

**Service:** `mobile-airfare-search-bff`  
**File:** `ReshopBuilder.java`  
**Bug:** `new BigDecimal(double)` used for fare calculations  
**Impact:** Fare differences shown to customers may be off by fractions of a cent due to IEEE 754 double precision. This translates to wrong prices displayed in the app for re-shop scenarios.  
**Fix:** Replace all `new BigDecimal(doubleValue)` with `new BigDecimal("string")` or `BigDecimal.valueOf(doubleValue)`.

**Product teams must audit:** Any pricing display in the booking funnel that routes through `airfare-search-bff` is affected. Regression test must verify exact cent values match backend contract.

## Reference Implementation: booking-bff (7.4/10)

`aa-ct-mobile-booking-bff` is the fleet's highest-quality service (SOLID 7.5, GRASP 7.0, OOD 7.0, Coverage 8.0). Use it as the reference pattern for:
- Constructor injection (not field injection)
- No god classes — largest file is < 300 LOC
- Test coverage ≥ 80%
- Clean layer separation (controller → service → client)

New booking features should extend `booking-bff` where possible, rather than adding complexity to lower-quality services.

## Roadmap Rules for Booking Features

1. **Airfare-search features:** Resolve currency precision bug before adding new fare display features
2. **Reservation features:** `mobile-reservation-bff` (5.0/10) is stable — PROPOSAL.md required per ENG-11.1 before any contract changes
3. **New booking flows:** Use `booking-bff` as target service — it can absorb new features without quality degradation
4. **Multi-passenger flows:** Audit `Minilith.getAllPassengers()` — confirmed bug returns only last passenger; any BFF feature relying on passenger list from Minilith is affected
