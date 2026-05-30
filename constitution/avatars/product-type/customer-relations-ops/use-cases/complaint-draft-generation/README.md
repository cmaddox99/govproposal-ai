# Customer Relations Operations Use Case: Complaint Draft Generation

## Business Context

American Airlines Customer Relations Representatives handle thousands of passenger complaints per week across categories including flight operations, inflight service, airport experience, and admins club/lounge issues. Each draft must comply with strict compensation policies, prohibited language rules, and trademark requirements before it can be sent.

**Goal:** Generate a policy-compliant draft response for a CR Rep within 30 seconds and reduce the manual edit rate from ~30% to <20% by improving template selection and compliance pre-validation.

---

## User Story

**As** Alex Rivera (CR Specialist),  
**I want** to receive a policy-compliant draft for an INFLIGHT - FLIGHT ATTENDANTS complaint,  
**So that** I can review and submit it in under 2 minutes without manually correcting liability language or compensation amounts.

---

## Current Workflow (Baseline)

1. **Complaint receipt (2 min):** Alex opens the complaint record in the CR tool and reads the passenger narrative
2. **Policy lookup (3 min):** Alex manually checks the compensation matrix for the INFLIGHT category
3. **Draft composition (5 min):** Alex writes a draft from memory of policy rules, tone guidelines, and applicable template
4. **Compliance review (3 min):** Alex re-reads draft to check for prohibited phrases, apology count, trademark usage
5. **Supervisor flag (variable):** If compensation is over threshold, draft is held for Diana's review
6. **Submit (1 min):** Alex submits and closes case

**Total per case:** ~14 minutes  
**Compliance edit rate:** ~30% of cases require at least one correction after first draft

---

## Proposed Workflow (System-Assisted)

1. **Complaint record received (automatic):** Structured complaint record arrives at `ServiceRecoveryController` (ct-service-recovery-bff `com.aa.servicerecovery.bff.api.controller`)
2. **Eligibility check (automatic, <1s):** `IROPSController` calls `IROPSHubConnector` to verify disruption eligibility and recovery options
3. **PII redaction (automatic, <1s):** Customer names, PNR, contact info replaced with tokens via `pii_redact.py` before LLM call
4. **Template selection (automatic, <1s):** Category/subcategory → template map → compensation eligibility evaluated by `ServiceRecoveryServiceImpl`
5. **Silent agent pipeline (automatic, 5–15s):** Analysis Agent → Compliance Agent → Drafting Agent (orchestrated via `ServiceRecoveryServiceImpl`)
6. **Compliance validation (automatic, <1s):** Trademark check, prohibited-words scan, response structure validation
7. **PII restoration (automatic, <1s):** Tokens replaced with customer data in final draft via `ServiceRecoveryConnector`
8. **CR Rep review (2 min):** Alex reviews the pre-validated draft — no policy lookup needed
9. **Audit trace written (automatic):** LLM call, compensation decision, PII hash, outcome recorded to PostgreSQL append-only log

**Total per case:** ~3–4 minutes (78% reduction)  
**Target edit rate:** <20%

---

## Success Criteria

| Metric | Baseline | Target |
|--------|----------|--------|
| Avg case handling time | 14 min | <4 min |
| Draft edit rate (manual corrections needed) | ~30% | <20% |
| Compliance violation rate (liability language, prohibited phrases) | ~5% | 0% in delivered drafts |
| PII in LLM payload | Unknown | 0% (audited) |
| Audit trace completeness | Partial | 100% |

---

## Hangar SDD Requirements

### Epic: Compliant Complaint Draft Generation

```
BASE-001: PII is redacted before any LLM API call
BASE-002: Draft is validated for prohibited language before display to CR Rep
BASE-003: Compensation amount is validated against category policy before draft is generated
BASE-004: Audit trace record is written for every LLM call with TID, model, compensation, and outcome
BASE-005: PII is restored deterministically from the token map in the final response
BASE-006: Only the final drafted message is returned — no internal agent reasoning is surfaced
```

### Vertical Slices

| Slice | Behavior | Test |
|-------|----------|------|
| 0 | Characterization tests for all 6 BASE requirements above pass against current code | GREEN on existing behavior |
| 1 | New INFLIGHT + secondary PAX template produces higher acceptance rate | Acceptance rate test with representative case set |
| 2 | Compensation validation extended to cover INFLIGHT with prior-award deduction | Compensation rule unit tests; integration test with PostgreSQL history lookup |
| 3 | Prohibited-language scan extended with new liability phrase list | Unit test per new phrase pattern |

---

## Atomic TDD Example (ENG-4.1)

```python
# tests/unit/test_compliance_validation.py

# Step 1: RED — write failing test first
def test_draft_with_liability_language_is_flagged():
    """Liability phrase 'we are responsible for' must not appear in final draft."""
    # GIVEN
    draft_with_violation = "We are responsible for the inconvenience, John."
    
    # WHEN
    result = validate_fix_response(draft_with_violation)
    
    # THEN
    assert "we are responsible for" not in result.lower()


# Step 2: GREEN — implement minimal rule in validate_fix_response
# Step 3: REFACTOR — extract liability_phrases list to a config module
# Step 4: REPEAT for next phrase pattern
```
