---
law_id: ENG-11.1
avatar: ios-swift
---

# ENG-11.1: Spec-Driven Development — iOS

> **Law:** Every new feature starts with a spec entry before code is written. The spec declares the governing avatar, the applicable laws, and the acceptance criteria. A PR without a spec reference is not ready for review.

---

## Spec Entry Format

```
hangar-ai-specs/
  changes/
    FareMapRedesign/
      spec.yaml
      acceptance-criteria.md
```

```yaml
# hangar-ai-specs/changes/FareMapRedesign/spec.yaml
feature: Fare Map Redesign
avatar: ios-swift
product_avatar: passenger-booking
laws:
  - ENG-4.1   # TDD mandate — tests written before FareMapSearchViewModel changes
  - ENG-3.1   # Complexity — FareMapSearchViewModel currently 470 lines; must not grow
  # Note: JTBD and product laws (PRD-*) are governed by the product avatar
  # (e.g., passenger-booking). Reference the product avatar here; do not
  # list PRD-* laws in a technology avatar spec entry.
acceptance_criteria_file: acceptance-criteria.md
pr_gate: spec.yaml must be committed and referenced in the PR description
```

## Acceptance Criteria Example

```markdown
# Fare Map Redesign — Acceptance Criteria

GIVEN a passenger has entered origin, destination, and date range  
WHEN the fare map loads  
THEN the lowest fare per date is visible without scrolling (mobile viewport)  
AND the selected date is visually distinguished  
AND a date with no availability shows a clear indicator (not blank)

GIVEN the fare matrix fetch fails  
WHEN the view loads  
THEN a retry button is shown  
AND no stale data is displayed
```

## PR Gate

The PR description must include:
```
Spec: hangar-ai-specs/changes/FareMapRedesign/spec.yaml
Laws verified: ENG-4.1 (tests written first), ENG-3.1 (FareMapSearchViewModel not grown)
```

A reviewer must confirm the spec reference is present before approving. This is a hard gate, not a courtesy check.
