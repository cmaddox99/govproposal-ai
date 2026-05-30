---
law: PRD-2.1
avatar: avatar-customer-relations-ops
title: "User Journey — Complaint Intake to Draft Review"
---

# PRD-2.1 User Journey — Customer Relations Ops

## Journey: CR Rep Complaint Response (Primary Path)

| Step | Actor | Action | Module | Compliance Gate |
|------|-------|--------|--------|----------------|
| 1. Intake | CRM | Structured complaint received | CRM Platform → FastAPI | Category classification triggered |
| 2. PII Redact | System | PII stripped before LLM call | `pii_redact.py` | 0% PII in LLM payload |
| 3. Analysis | AI | Silent analysis of complaint context | Stage 1: Analysis Agent | No output to Rep |
| 4. Compliance | AI | Compliance check against template rules | Stage 2: Compliance Agent | Prohibited language check |
| 5. Draft | AI | Response draft generated | Stage 3: Drafting Agent | Template governance enforced |
| 6. Review | CR Rep | Read, evaluate, accept/edit draft | FastAPI response surface | 120s target review time |
| 7. Edit | CR Rep | Adjust compensation or tone if needed | CR Rep interface | Supervisor approval for >$X compensation |
| 8. Send | CR Rep | Approved draft sent to passenger | CRM Platform outbound | Audit trace recorded |
| 9. Close | System | Case closed; audit trace finalized | PostgreSQL append-only | 7-year retention |

## Exception Flows

| Scenario | Handling |
|----------|----------|
| Compensation override needed | Escalate to supervisor for approval |
| ADA/disability complaint | Medical PII classification triggers RESTRICTED handling |
| Draft rejected entirely | CR Rep retypes; rejection reason logged in audit trace |

## Silent Pipeline (invisible to Rep)

The 3-stage AI pipeline runs silently. The Rep sees only the compliant draft output.
All 3 stages are traced in the append-only audit log per ENG-6.7 requirements.
