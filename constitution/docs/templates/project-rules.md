# Project Rules - {{PROJECT_NAME}}

> Project-specific adaptations within Constitutional law boundaries.
> Per **ENG-1.2 (AI-Engineer Pairing Law)**: Every decision references the constitutional principle behind it.

---

## Constitution Reference

- **Source:** `{{PATH_TO_CONSTITUTION}}`
- **Compliance Status:** {{STATUS}} (e.g., ADOPTING, COMPLIANT, PARTIAL)
- **Adoption Date:** {{DATE}}

---

## Technology Decisions

Document each technology constraint and its constitutional impact.

### {{TECHNOLOGY_1}} Version: {{VERSION}}

- **Constraint:** {{CONSTRAINT_DESCRIPTION}}
- **Impact per {{LAW_ID}}:** {{IMPACT_DESCRIPTION}}
- **Adaptation:** {{ADAPTATION_DESCRIPTION}}

### {{TECHNOLOGY_2}} Version: {{VERSION}}

- **Constraint:** {{CONSTRAINT_DESCRIPTION}}
- **Impact per {{LAW_ID}}:** {{IMPACT_DESCRIPTION}}
- **Adaptation:** {{ADAPTATION_DESCRIPTION}}

---

## Law Adaptations

Document how specific laws are adapted for this project's constraints.

### ENG-4.1 (Atomic TDD Law) — NON-NEGOTIABLE

| Standard Requirement | Project Adaptation | Rationale |
|---------------------|-------------------|-----------|
| One test per TDD cycle | One test per TDD cycle — no exceptions | ENG-4.1 is non-negotiable; batching violates atomicity |
| One test per cycle — same rule applies to characterization tests | ENG-4.1 is NON-NEGOTIABLE regardless of test type | Characterization tests are not exempt from Atomic TDD |

> **Citation:** Per ENG-4.1: "TDD SHALL be practiced in atomic cycles — ONE test at a time."

### {{LAW_ID}} ({{LAW_NAME}}) - ADAPTED

| Standard Requirement | Project Adaptation | Rationale |
|---------------------|-------------------|-----------|
| {{STANDARD_1}} | {{ADAPTATION_1}} | {{RATIONALE_1}} |
| {{STANDARD_2}} | {{ADAPTATION_2}} | {{RATIONALE_2}} |

> **Citation:** Per {{RELATED_LAW}}: "{{QUOTE_FROM_LAW}}"

---

## Domain Rules (Business Critical)

Per **ENG-1.1 (Priority Hierarchy)** - Correctness is #2 priority after Security.

### {{DOMAIN_RULE_1}}

{{DESCRIPTION}}

```
{{RULE_DETAILS_OR_THRESHOLDS}}
```

> **Critical:** Per **ENG-4.6 (Coverage Requirements)**: Business-critical calculations require 100% test coverage.

### {{DOMAIN_RULE_2}}

{{DESCRIPTION}}

---

## Known Technical Debt

Per **ENG-3.4 (Single Responsibility Principle)** and **ENG-1.3 (Continuous Refactoring Law)** - documented for future remediation:

| Debt Item | Violates | Impact | Remediation Phase |
|-----------|----------|--------|-------------------|
| {{DEBT_1}} | {{LAW_1}} | {{IMPACT_1}} | Phase {{N}} |
| {{DEBT_2}} | {{LAW_2}} | {{IMPACT_2}} | Phase {{N}} |

---

## Adoption Phases

### Phase 1: {{PHASE_1_NAME}} ({{STATUS}})

Per **{{LAW_ID}}**: {{RATIONALE}}

- [ ] {{TASK_1}} ({{LAW_ID}})
- [ ] {{TASK_2}} ({{LAW_ID}})
- [ ] {{TASK_3}} ({{LAW_ID}})

### Phase 2: {{PHASE_2_NAME}} ({{STATUS}})

Per **{{LAW_ID}}**: {{RATIONALE}}

- [ ] {{TASK_1}} ({{LAW_ID}})
- [ ] {{TASK_2}} ({{LAW_ID}})

### Phase 3: {{PHASE_3_NAME}} ({{STATUS}})

Per **{{LAW_ID}}**: {{RATIONALE}}

- [ ] {{TASK_1}} ({{LAW_ID}})
- [ ] {{TASK_2}} ({{LAW_ID}})

---

## Template Instructions

Replace all `{{PLACEHOLDER}}` values with your project-specific information:

**Header:**
- `{{PROJECT_NAME}}` - Your project name
- `{{PATH_TO_CONSTITUTION}}` - Relative path to hangar-ai-constitution
- `{{STATUS}}` - ADOPTING, COMPLIANT, or PARTIAL
- `{{DATE}}` - Adoption date

**Technology Decisions:**
- `{{TECHNOLOGY_1}}` - e.g., "Java", "Python", "Spring Boot"
- `{{VERSION}}` - e.g., "11", "3.11", "2.7.18"
- `{{CONSTRAINT_DESCRIPTION}}` - Why this version (e.g., "Legacy system, cannot upgrade")
- `{{LAW_ID}}` - Impacted law (e.g., "ENG-4.4")
- `{{IMPACT_DESCRIPTION}}` - How the constraint affects compliance
- `{{ADAPTATION_DESCRIPTION}}` - How you're adapting

**Law Adaptations:**
- `{{LAW_ID}}` - e.g., "ENG-4.1"
- `{{LAW_NAME}}` - e.g., "Atomic TDD Law"
- `{{STANDARD_1}}` - The standard requirement from the law
- `{{ADAPTATION_1}}` - Your project's adaptation
- `{{RATIONALE_1}}` - Why this adaptation is valid

**Domain Rules:**
- `{{DOMAIN_RULE_1}}` - e.g., "Tier Calculation"
- `{{DESCRIPTION}}` - What the rule does
- `{{RULE_DETAILS_OR_THRESHOLDS}}` - Specific values or thresholds

**Technical Debt:**
- `{{DEBT_1}}` - e.g., "All logic in Controller"
- `{{LAW_1}}` - Which law it violates (e.g., "ENG-3.4")
- `{{IMPACT_1}}` - Business/technical impact
- `{{PHASE}}` - When you plan to fix it

**Adoption Phases:**
- `{{PHASE_1_NAME}}` - e.g., "Safety Net", "Foundation", "MVP"
- `{{TASK_1}}` - Specific task
- `{{LAW_ID}}` - Law that requires this task
