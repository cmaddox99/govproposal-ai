# ENG-3.1 — Complexity Limits · Node.js/TypeScript

**AA Fleet Hotspot:** `flightStatusBuilder.ts` in Mobile-FLIFO-BFF — 646 LOC, 25+ exported functions, ~480 branches. Single module handles delay detection, status formatting, country codes, prior-leg info, flight keys, disruption info, and list building.

## Complexity table — FLIFO-BFF

| File | LOC | Functions | Issue |
|---|---|---|---|
| `flightStatusBuilder.ts` | 646 | 25+ | God module — ENG-3.1 HARD_BLOCK |
| `liveActivitiesRequestValidation.ts` | 220 | — | Repetitive validation rules |
| `liveActivityController.ts` | 165 | — | Business logic embedded in controller |
| `flightScheduleService.ts` | 146 | — | High CC: env-switching + search-type branching |

**Max file size:** 300 LOC for a TypeScript BFF module. Above that, split by responsibility. `flightStatusBuilder.ts` should become: `delayDetector.ts`, `statusFormatter.ts`, `flightListBuilder.ts`.

## Nesting HARD_BLOCK

```typescript
// BAD — 4-level nesting in flightScheduleService.ts (AA confirmed)
buildSchedules(response) {
  if (allFieldsPresent) {            // level 1
    if (isRealTimeEligible) {        // level 2
      if (responseSuccess) {         // level 3
        forEach → forEach → push     // level 4
      }
    }
  }
}
// FIX — guard clauses + extracted functions (≤2 nesting levels)
```
