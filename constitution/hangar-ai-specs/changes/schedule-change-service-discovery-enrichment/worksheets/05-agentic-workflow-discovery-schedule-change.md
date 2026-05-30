# Worksheet 05: Agentic Workflow Discovery - Schedule Change Self-Serve

**Purpose:** Prioritize AI-assisted workflows grounded in domain evidence and constitutional guardrails.  
**Law Anchor:** PRD-3.1, ENG-9.4, BUS-7.1  
**Status:** Draft (priority scoring pending workshops + code evidence)

---

## Candidate Workflows

| Workflow | Skill Mapping | Expected Impact | Feasibility | Priority |
|---------|---------------|-----------------|-------------|----------|
| Eligibility explanation assistant | skill-21 + skill-23 + skill-05 | Reduce escalation from ineligible traffic | Medium | Pending |
| Reason-code quality reviewer | skill-08 + skill-05 | Improve explanation quality and consistency | High | Pending |
| BFF latency bottleneck analyzer | skill-13 + skill-08 | Faster root-cause and optimization cycle | High | Pending |
| Audit completeness checker | skill-13 + skill-08 | Reduce compliance misses and audit toil | High | Pending |
| Override pattern triage assistant | skill-04 + skill-05 | Detect recurring override root causes | Medium | Pending |

---

## Guardrails (Non-Negotiable)

1. Read-only mode first for any conversational eligibility assistant.
2. No booking mutation without explicit human/passenger confirmation.
3. Every recommendation must include traceable rule grounding.
4. Session and recommendation audit logging must be enabled by default.
5. Clear fallback path to human agent for low-confidence responses.

---

## Pilot Selection Scoring

| Dimension | Weight | Definition |
|----------|--------|------------|
| Customer impact | 35% | Improvement to success, clarity, or cycle time |
| Operational impact | 30% | Reduction in manual handling or incident load |
| Feasibility | 20% | Implementable with current systems and controls |
| Risk profile | 15% | Compliance and reliability exposure |

---

## Recommended Pilot Sequence (Initial)

1. Pilot A: Eligibility explanation assistant (read-only, no mutations)
2. Pilot B: Audit completeness checker (compliance and evidence quality)

---

## Exit Criteria

- [ ] Top 2 pilots selected with quantified success metrics
- [ ] Human override + approval flow documented and approved
- [ ] Rollback criteria defined for each pilot
- [ ] Ownership assigned (product, engineering, compliance)
