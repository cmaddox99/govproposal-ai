---
avatar: avatar-customer-relations-ops
domain: AI-Assisted Complaint Response, Compensation Decision, CR Rep Tooling
laws: [PRD-1.2, PRD-1.5, PRD-2.5, PRD-5.1, PRD-6.2, BUS-1.1, BUS-4.3, BUS-7.1, ENG-6.4, ENG-6.7]
skills: [21-prompt-engineering, 23-ai-agents, 05-business-rules, 13-observability, 10-security-review]
---

# Customer Relations Operations — Agent Guidance

AI-assisted complaint response drafting for CR Reps. A structured complaint record enters a silent 3-stage pipeline (Analysis → Compliance → Drafting), PII is redacted before every LLM call, a policy-compliant draft is returned. CR Rep never touches the LLM directly.

## Core Laws (one-liner)

| Law | Rule |
|-----|------|
| BUS-1.1 | Company policy outranks tone/style — compliance check runs before every draft is surfaced |
| BUS-4.3 | PII redacted at ingestion before every LLM call; restored only in deterministic output |
| BUS-7.1 | Every LLM call and compensation decision traced to append-only audit table |
| PRD-1.2 | Problem-first: validate draft rejection rate by category before changing prompt templates |
| PRD-5.1 | MVP = domestic flight complaints, direct AA segments only; partner carriers out of scope |
| ENG-6.4 | Customer PII (name, contact, flight PNR) encrypted at rest and in transit |
| ENG-6.7 | Supervisor override and compensation approval immutably audited with agent ID |

## Key Patterns

- **Silent orchestration** — only the final compliant draft surfaces to the CR Rep; reasoning suppressed.
- **Prohibited-word scan** — liability phrase detection runs as a final Drafting Agent pass.
- **Compensation guardrail** — dollar amounts validated against policy table before draft is released.
- **Human approval gate** — high-compensation and escalation categories require supervisor sign-off.

## Anti-Patterns

- ❌ Surfacing LLM reasoning chains to CR Reps — internal pipeline details create audit liability.
- ❌ Compensation amounts determined solely by LLM without policy table validation.
- ❌ PII present in any LLM prompt or log output.
- ❌ Draft templates that override compliance rules for tone preference.

See `guidance-detail.md` for full law applications, journey maps, and agentic pipeline design.
