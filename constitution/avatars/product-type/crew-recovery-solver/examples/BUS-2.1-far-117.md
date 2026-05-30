---
avatar: avatar-product-crew-recovery-solver
law: BUS-2.1
title: "FAA Compliance Law"
---

# BUS-2.1 — FAA Compliance Law: FAR Part 117 Crew Rest in CWR

## What This Law Requires
All crew recovery options presented to schedulers must satisfy FAR Part 117 crew rest minimums. This check runs synchronously before options are scored, ranked, or displayed. No option that violates FAR Part 117 is presented under normal operating conditions.

## Compliant Example

**FAR 117 Eligibility Service**

```python
class FARPart117EligibilityService:
    """
    Hard gate: called before scoring. Result is binary.
    A False result removes the candidate from the options list.
    """

    def is_eligible(
        self,
        crew_member: CrewMember,
        proposed_assignment: FlightAssignment,
    ) -> EligibilityResult:
        last_duty_end: datetime = crew_member.last_duty_period_end
        proposed_report_time: datetime = proposed_assignment.report_time

        rest_hours = (proposed_report_time - last_duty_end).total_seconds() / 3600

        # FAR 117.25(a): minimum 10 hours rest between duty periods
        # FAR 117.25(b): reduced rest not permitted for augmented operations
        required_rest = self._compute_required_rest(crew_member, proposed_assignment)

        return EligibilityResult(
            eligible=rest_hours >= required_rest,
            actual_rest_hours=rest_hours,
            required_rest_hours=required_rest,
            regulation="FAR 117.25(a)",
        )

    def _compute_required_rest(self, crew, assignment) -> float:
        # Augmented crew: 10 hours minimum; unaugmented: varies by flight time
        # See FAR 117 Table B for full matrix
        ...
```

**Integration pattern:** `FARPart117EligibilityService.is_eligible()` is called in the `RecoveryOptionBuilder` before any scoring. Options where `eligible=False` are excluded from the result set and logged to the audit trail as `INELIGIBLE`.

## Violation Example
```
❌ FAR 117 check called after scoring; ineligible options shown with "⚠ Rest Warning" badge.
   → Regulatory violation: displaying an ineligible option implies it is a valid choice.
   → Fix: eligibility check must be a hard pre-filter, not a post-score decorator.
```

## Edge Cases & Warnings
- Flight crew and cabin crew have different FAR Part 117 tables — use `crew.role` to select the correct computation path
- International operations may also require EASA FTL compliance — check `flight.jurisdiction` and route to the correct eligibility service
- "Augmented operations" (extra crew on-board for pilot rest) changes the rest calculation — never use a flat 10-hour rule
