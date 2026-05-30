# Customer Relations Operations — Personas

## CR Specialist

**Name:** Alex Rivera  
**Role:** Customer Relations Representative (Front-Line)  
**Experience:** 3 years in CR Operations, handles 40–60 complaints per day across all categories  

**Primary Goals:**
- Generate a compliant draft quickly without spending time on policy lookups
- Avoid sending a draft that triggers a supervisor review or compliance flag
- Close cases within SLA without rework loops

**Pain Points:**
- Liability language slips through on INFLIGHT categories — manual editing adds 2–4 minutes per case
- Compensation amounts sometimes need manual correction when a passenger has prior awards on the same flight
- Template selection fails on edge-case subcategories (e.g., "INFLIGHT - OTHER PASSENGER BEHAVIOR" with a secondary PAX component)

**How the System Helps:**
- Draft is pre-validated against prohibited language before display — Alex sees a clean draft
- Compensation is pre-validated against the category matrix — no manual lookup
- Secondary PAX guidelines are automatically applied when the complaint references another passenger

---

## CR Supervisor

**Name:** Diana Okafor  
**Role:** CR Operations Supervisor  
**Experience:** 8 years in Customer Relations; oversees 12 specialists across two shift teams  

**Primary Goals:**
- Review high-compensation edge cases before submission (cases over $500 in travel credit)
- Audit compliance on escalated complaints to ensure no liability language is present
- Monitor draft acceptance rates to identify category coverage gaps for template updates

**Pain Points:**
- Escalated cases lack visible reasoning for why a specific compensation amount was offered
- When a draft is rejected, there is no structured audit log of what was changed manually vs. what the system generated
- New complaint category variants (social media-originated, congressional complaints) have no templates

**How the System Helps:**
- Every LLM call and compensation decision is in the audit trace with the TID chain for full review
- The audit trace captures `outcome: accepted / edited / rejected` so supervisors can track manual edits
- Template coverage gaps surface in weekly compliance reports by acceptance-rate analysis per category

---

## Compliance Reviewer

**Name:** Marcus Webb  
**Role:** CR Compliance & Quality Reviewer  
**Experience:** 5 years in legal/compliance adjoining roles; embedded in CR Operations quarterly audits  

**Primary Goals:**
- Verify no generated drafts contained liability language, prohibited phrases, or trademark errors
- Confirm PII never appeared in LLM call payloads (audit log sample check)
- Validate that compensation awards for a given period are within policy bounds per category

**Pain Points:**
- Audit logs contain raw LLM payloads but no structured way to scan for PII presence
- Trademark enforcement is inconsistent — some categories mark "AAdvantage®" correctly, others miss it
- No structured diff between the system-generated draft and the final submitted response (to quantify edit size)

**How the System Helps:**
- PII fields are hashed before storage — the audit trace allows detection of PII leakage without storing PII itself
- Trademark check runs on every draft before display via `trademark_check.py`
- `outcome` field in the audit trace, combined with a future diff field, will quantify system-generated vs. manually edited content
