# Enrichment Worksheet 4: Domain Model Inventory

**Purpose:** Capture the real business entities, rules, and event flows so AI agents understand your domain.  
**Session:** 1-2 hours with Domain Expert, Senior Engineer, or Business Analyst  
**Output:** Informs `guidance.md` (domain-specific patterns), use-case enrichment, and agentic workflow design

---

## Instructions

Document your domain as it exists in code and in the team's heads. Include both — code captures what's implemented, tribal knowledge captures what should be implemented. AI agents need both to give contextual guidance per ENG-2.1 (Domain-Driven Design Law).

### Evidence Source Taxonomy (Required)

For entities, rules, and exception flows, tag evidence as:
- `code-evidenced`
- `field-study`
- `stakeholder-reported`
- `public-benchmark`
- `hypothesis-only`

Confidence levels: `high`, `medium`, `low`

---

## Section 0: Domain Evidence Ledger (Fill First)

| Domain Claim | Source Tag | Confidence | Citation / Notes |
|--------------|------------|------------|------------------|
| [ ] | [ ] | [ ] | [ ] |
| [ ] | [ ] | [ ] | [ ] |
| [ ] | [ ] | [ ] | [ ] |

---

## Section 1: Core Entities / Aggregates

> What are the main "things" in your domain? (DDD: Aggregates, Entities, Value Objects)

| Entity | Type | Key Fields | Owned By (Service) | DB Table / Collection |
|--------|------|-----------|-------------------|----------------------|
| [ ] | Aggregate / Entity / Value Object | [ ] | [ ] | [ ] |
| [ ] | [ ] | [ ] | [ ] | [ ] |
| [ ] | [ ] | [ ] | [ ] | [ ] |
| [ ] | [ ] | [ ] | [ ] | [ ] |
| [ ] | [ ] | [ ] | [ ] | [ ] |
| [ ] | [ ] | [ ] | [ ] | [ ] |

---

## Section 2: Business Rules

> What rules govern your domain? Include both coded and tribal.

| Rule | Description | Where Enforced | Coded? | Source of Truth |
|------|-----------|----------------|--------|----------------|
| [ ] | [ ] | Service / DB / UI / Manual | Yes / No / Partial | Code / Wiki / Person's head |
| [ ] | [ ] | [ ] | [ ] | [ ] |
| [ ] | [ ] | [ ] | [ ] | [ ] |
| [ ] | [ ] | [ ] | [ ] | [ ] |
| [ ] | [ ] | [ ] | [ ] | [ ] |

**Tribal Knowledge Risk:** Rules only in someone's head that would be lost if they left:
1. [ ]
2. [ ]
3. [ ]

---

## Section 3: Domain Events / Flows

> What happens when key actions occur? Map the event chains.

### Flow 1: [ Name — e.g., "Passenger Checks In" ]

```
Trigger: [ What starts this flow? ]
   │
   ├─ Step 1: [ ]
   │     └─ System: [ which service ]
   │     └─ Rule: [ which business rule applies ]
   │
   ├─ Step 2: [ ]
   │     └─ System: [ ]
   │     └─ Rule: [ ]
   │
   ├─ Step 3: [ ]
   │     └─ System: [ ]
   │     └─ Output: [ what's produced ]
   │
   └─ End State: [ ]
```

### Flow 2: [ Name ]

```
Trigger: [ ]
   │
   ├─ Step 1: [ ]
   ├─ Step 2: [ ]
   └─ End State: [ ]
```

### Flow 3: [ Name ]

```
Trigger: [ ]
   │
   ├─ Step 1: [ ]
   ├─ Step 2: [ ]
   └─ End State: [ ]
```

---

## Section 4: Exception / Error Flows

> What goes wrong? What are the edge cases that cause the most operational pain?

| Exception | Frequency | Current Handling | Impact | Automated? |
|-----------|-----------|-----------------|--------|-----------|
| [ ] | Daily / Weekly / Monthly / Rare | [ ] | High / Med / Low | Yes / No / Partial |
| [ ] | [ ] | [ ] | [ ] | [ ] |
| [ ] | [ ] | [ ] | [ ] | [ ] |
| [ ] | [ ] | [ ] | [ ] | [ ] |

---

## Section 5: Regulatory / Compliance Constraints

> What external rules constrain your domain? (FAA, TSA, DOT, IATA, PCI, GDPR, etc.)

| Regulation | Authority | What It Requires | How You Comply | Audit Frequency |
|-----------|-----------|-----------------|---------------|-----------------|
| [ ] | [ ] | [ ] | [ ] | [ ] |
| [ ] | [ ] | [ ] | [ ] | [ ] |
| [ ] | [ ] | [ ] | [ ] | [ ] |

---

## Section 6: Domain Language / Glossary

> What terms does your team use that outsiders wouldn't understand?

| Term | Definition | Used In (Service / Context) |
|------|-----------|---------------------------|
| [ ] | [ ] | [ ] |
| [ ] | [ ] | [ ] |
| [ ] | [ ] | [ ] |
| [ ] | [ ] | [ ] |
| [ ] | [ ] | [ ] |

---

## Validation Checklist

- [ ] Core entities mapped with ownership and storage
- [ ] Business rules captured — especially tribal knowledge at risk
- [ ] At least 3 key domain flows documented with step-by-step
- [ ] Exception flows identified (these are where agentic workflows add most value)
- [ ] Regulatory constraints listed
- [ ] Domain glossary started (even 5-10 terms helps agents enormously)
- [ ] Domain claims are source-tagged with confidence levels
