---
avatar: avatar-product-ballot-trading
law: PRD-1.5
title: "Evidence-Based Decision Law"
---

# PRD-1.5 — Evidence-Based Decision Law: Ballot Trading Application

## What This Law Requires

Trade eligibility decisions, ballot award rankings, and roadmap prioritization must
be grounded in evidence — CBA rules, telemetry, and validated pilot feedback — not
arbitrary system order or PM intuition. Each decision must surface its scoring
rationale to pilots and schedulers.

## Compliant Example

**Ballot Award Ranking Model (Evidence-Surfaced)**

```python
@dataclass
class TradeAwardCandidate:
    pilot_id: str
    pairing_id: str
    award_score: float  # 0.0–1.0, visible to pilot and scheduler

    # Factor breakdown (written to audit trail)
    cba_seniority_rank: int           # weight: 0.60 (CBA Article 8 — seniority governs)
    conflict_free: bool               # HARD GATE — False removes candidate entirely
    days_since_last_award: int        # weight: 0.25 (CBA Article 9.2 — equity distribution)
    domicile_match_score: float       # weight: 0.15 (operational preference)

    cba_article_applied: str          # e.g., "Article 8.1 — Seniority-Based Award Order"
    override_justification: str | None  # Required if scheduler deviates from top-ranked
```

**UI requirement:** Ballot award list displays rank, seniority position, and the
primary CBA article that governs the award order. A scheduler who selects a
lower-ranked candidate must enter a justification (logged to audit trail under
BUS-7.1).

**Constitutional check:** PRD-1.5 — award decision is grounded in CBA-specified
evidence (seniority rank, conflict status). Scheduler judgment is preserved but
every deviation is logged with justification.

## Violation Example

```
❌ Trade awards processed in submission-timestamp order (first submitted, first awarded).
   → No CBA seniority evaluation; submission speed becomes a de-facto eligibility factor.
   → Pilots without fast internet connections are systematically disadvantaged.
   → Violates PRD-1.5: decision basis is not CBA-evidence-grounded.
```

## Edge Cases & Warnings

- `conflict_free: False` removes the candidate from the award list — it is not
  shown as a waivable option under any normal circumstance (BUS-2.2).
- CBA seniority rank must be sourced from the authoritative seniority file at
  ballot-open time; cached values from a prior ballot period are not acceptable.
- Evidence basis for each award must be logged in the audit trail before the
  award notification is sent — retroactive logging violates BUS-7.1.
