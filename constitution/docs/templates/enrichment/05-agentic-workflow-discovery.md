# Enrichment Worksheet 5: Agentic Workflow Discovery

**Purpose:** Identify where AI agents can accelerate the team's development, testing, and operational workflows.  
**Session:** 2 hours with Hangar Labs + Product Team (Tech Lead, Product Owner, Senior Engineers)  
**Prerequisite:** Worksheets 1-4 completed. The enriched avatar must reflect reality before discovering workflows.  
**Output:** Prioritized list of agentic workflows to build, grounded in real domain context

---

## Instructions

This worksheet is collaborative. Hangar Labs brings the constitution's capabilities (skills, laws, TDD cycles, compliance checks). The product team brings their reality (pain points, time sinks, error-prone processes). Together you identify the intersection — where AI agents can deliver the most value.

### Evidence Source Taxonomy (Required)

For each candidate workflow and pilot claim, tag evidence as:
- `code-evidenced`
- `field-study`
- `public-benchmark`
- `stakeholder-reported`
- `hypothesis-only`

Confidence levels: `high`, `medium`, `low`

---

## Section 0: Workflow Evidence Ledger (Fill First)

| Workflow / Claim | Source Tag | Confidence | Citation / Evidence Link |
|------------------|------------|------------|--------------------------|
| [ ] | [ ] | [ ] | [ ] |
| [ ] | [ ] | [ ] | [ ] |
| [ ] | [ ] | [ ] | [ ] |

---

## Section 1: Engineering Time Audit

> Where does your team spend the most engineering hours today?

| Activity | Hours/Week (Approx) | Repetitive? | Error-Prone? | Could AI Help? |
|----------|-------------------|------------|-------------|---------------|
| Writing new features | [ ] | Low | [ ] | [ ] |
| Writing tests | [ ] | Med / High | [ ] | [ ] |
| Code review | [ ] | Med | [ ] | [ ] |
| Bug fixing | [ ] | Low | [ ] | [ ] |
| Debugging production issues | [ ] | Low | [ ] | [ ] |
| Documentation | [ ] | High | [ ] | [ ] |
| Dependency updates | [ ] | High | [ ] | [ ] |
| Data migration / schema changes | [ ] | Med | [ ] | [ ] |
| On-call / incident response | [ ] | Low | [ ] | [ ] |
| Manual testing / QA | [ ] | High | [ ] | [ ] |
| [ ] | [ ] | [ ] | [ ] | [ ] |
| [ ] | [ ] | [ ] | [ ] | [ ] |

---

## Section 2: Most Common Code Changes

> What types of PRs does your team submit most frequently?

| Change Type | Frequency | Typical Size | Pattern? | Example |
|------------|-----------|-------------|----------|---------|
| [ ] | Daily / Weekly / Monthly | S / M / L | Yes / No | [ ] |
| [ ] | [ ] | [ ] | [ ] | [ ] |
| [ ] | [ ] | [ ] | [ ] | [ ] |
| [ ] | [ ] | [ ] | [ ] | [ ] |
| [ ] | [ ] | [ ] | [ ] | [ ] |

---

## Section 3: Error Hotspots

> Where do production bugs originate most often?

| Error Category | Frequency | Root Cause | Could Tests Prevent? | Could AI Detect? |
|---------------|-----------|-----------|---------------------|-----------------|
| [ ] | [ ] | [ ] | Yes / Partially / No | Yes / No |
| [ ] | [ ] | [ ] | [ ] | [ ] |
| [ ] | [ ] | [ ] | [ ] | [ ] |
| [ ] | [ ] | [ ] | [ ] | [ ] |

---

## Section 4: Candidate Agentic Workflows

> Based on Sections 1-3, identify where AI agents can help. Rate each.

| Workflow | Constitutional Skill | Impact | Feasibility | Priority |
|----------|---------------------|--------|------------|----------|
| [ AI-assisted TDD for new endpoints ] | skill-06-atomic-tdd | [ ] | [ ] | [ ] |
| [ Auto-generate contract tests ] | skill-12-api-design | [ ] | [ ] | [ ] |
| [ Code review with law compliance ] | skill-08-code-review + skill-27 | [ ] | [ ] | [ ] |
| [ Domain model documentation ] | skill-04-business-domain-modeling | [ ] | [ ] | [ ] |
| [ Incident response runbooks ] | skill-11-incident-response | [ ] | [ ] | [ ] |
| [ ] | [ ] | [ ] | [ ] | [ ] |
| [ ] | [ ] | [ ] | [ ] | [ ] |
| [ ] | [ ] | [ ] | [ ] | [ ] |

**Scoring:**
- **Impact:** How many hours/week saved? How much quality improved? (High / Med / Low)
- **Feasibility:** Can we do this with current AI tools + constitution? (High / Med / Low)
- **Priority:** Impact × Feasibility (1 = do first, 2 = do second, etc.)

---

## Section 5: Pilot Selection

> Pick the TOP 1-2 workflows to pilot. Define success criteria.

### Pilot 1: [ Workflow Name ]

**What the agent does:** [ ]  
**What the human does:** [ ]  
**Constitutional skills used:** [ ]  
**Codebase / repo it runs against:** [ ]  
**Success metric:** [ ]  
**Duration:** [ 2 weeks / 1 month ]  
**Who evaluates:** [ ]

**Evidence Tag:** [ code-evidenced / field-study / public-benchmark / stakeholder-reported / hypothesis-only ]  
**Confidence:** [ high / medium / low ]  
**Citation:** [ ]

### Pilot 2: [ Workflow Name ]

**What the agent does:** [ ]  
**What the human does:** [ ]  
**Constitutional skills used:** [ ]  
**Codebase / repo it runs against:** [ ]  
**Success metric:** [ ]  
**Duration:** [ ]  
**Who evaluates:** [ ]

**Evidence Tag:** [ code-evidenced / field-study / public-benchmark / stakeholder-reported / hypothesis-only ]  
**Confidence:** [ high / medium / low ]  
**Citation:** [ ]

---

## Section 6: Prerequisites & Blockers

> What needs to be true before agents can work on your codebase?

| Prerequisite | Status | Blocker? | Owner |
|-------------|--------|----------|-------|
| Repo accessible to AI tools | [ ] | [ ] | [ ] |
| AGENTS.md in project repo | [ ] | [ ] | [ ] |
| Test framework configured | [ ] | [ ] | [ ] |
| CI/CD pipeline running | [ ] | [ ] | [ ] |
| Team trained on constitution | [ ] | [ ] | [ ] |
| [ ] | [ ] | [ ] | [ ] |

---

## Validation Checklist

- [ ] Engineering time audit completed honestly
- [ ] Common code change patterns identified
- [ ] Error hotspots mapped to preventable causes
- [ ] At least 5 candidate agentic workflows identified with skills
- [ ] Top 1-2 pilots selected with measurable success criteria
- [ ] Prerequisites and blockers documented with owners
- [ ] Workflow and pilot claims are source-tagged with confidence levels
- [ ] Any public benchmark references include citation metadata and directional disclaimer
