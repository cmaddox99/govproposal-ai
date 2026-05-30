# Use Case: God Module Split

**Laws:** ENG-3.1 (Complexity Limits), ENG-2.2 (Layered Architecture)
**Repo:** Mobile-FLIFO-BFF — `flightStatusBuilder.ts` (646 LOC, 25+ functions, ~480 branches)

## Problem

`flightStatusBuilder.ts` handles: delay detection, arrival/departure status, country codes, flight keys, prior-leg info, disruption info, list building. A change to delay logic risks breaking list building — no isolation. Functions `isDepartureDelayed` and `isArrivalDelayed` are 33-LOC near-duplicates; `formatDateWithTimeZone` and `formatDateWithoutTimezone` are 90% identical.

## Split Target

```
flightStatusBuilder.ts (646 LOC)
  → delayDetector.ts         (≤80 LOC)  isDepartureDelayed, isArrivalDelayed
  → flightStatusFormatter.ts (≤120 LOC) buildFlightStatusObject, status strings
  → flightListBuilder.ts     (≤100 LOC) buildFlightStatusList, pagination
  → priorLegResolver.ts      (≤60 LOC)  prior leg info, flight keys
  → countryCodeMap.ts        (≤20 LOC)  data-driven lookup, not if-else chains
```

## Migration Steps

1. Create `delayDetector.ts` — move `isDepartureDelayed` + `isArrivalDelayed`, consolidate into single `isLegDelayed(leg, direction)` (eliminates duplication).
2. Create `countryCodeMap.ts` — replace 3-branch if-else with `Record<string, string>` lookup.
3. Move remaining functions to named files ≤150 LOC.
4. Delete original `flightStatusBuilder.ts` barrel — `index.ts` re-exports.
5. Tests: each new file must reach 90%+ branch coverage before deletion of original.

## Reference

`mobile-platform-bff`: 13 route modules, largest file 381 LOC (includes versioned endpoints). No utility god-module. Each module owns one concern.
