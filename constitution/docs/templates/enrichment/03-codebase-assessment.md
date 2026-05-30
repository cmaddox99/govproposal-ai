# Enrichment Worksheet 3: Codebase Assessment

**Purpose:** Map the real technology landscape so the avatar reflects actual services, APIs, and integrations.  
**Session:** 1-2 hours with Tech Lead, Architect, or Senior Engineers  
**Output:** Informs `manifest.yaml` (dependencies, tech stack), `guidance.md` (architecture context), and use-case enrichment

---

## Instructions

Document what actually exists in production today. This is NOT aspirational — it's the current state. Include legacy systems, tech debt, and "we know this is bad" items. AI agents need the real picture to give useful guidance.

### Evidence Source Taxonomy (Required)

Tag each major finding using:
- `code-evidenced`
- `field-study`
- `public-benchmark`
- `stakeholder-reported`
- `hypothesis-only`

Confidence levels: `high`, `medium`, `low`

Public benchmark references are optional in this worksheet, but if used for directional comparison (for example reliability/SLO benchmarks), they must include citation metadata.

---

## Section 0: Technical Evidence Ledger (Fill First)

| Finding / Constraint | Source Tag | Confidence | Citation / Evidence Link |
|----------------------|------------|------------|--------------------------|
| [ ] | [ ] | [ ] | [ ] |
| [ ] | [ ] | [ ] | [ ] |
| [ ] | [ ] | [ ] | [ ] |

---

## Section 1: Service Inventory

> List every service/application your team owns or heavily depends on.

| Service Name | Language / Framework | Repo URL | Type | Status |
|-------------|---------------------|----------|------|--------|
| [ ] | [ ] | [ ] | API / UI / Worker / DB | Active / Legacy / Deprecated |
| [ ] | [ ] | [ ] | [ ] | [ ] |
| [ ] | [ ] | [ ] | [ ] | [ ] |
| [ ] | [ ] | [ ] | [ ] | [ ] |
| [ ] | [ ] | [ ] | [ ] | [ ] |
| [ ] | [ ] | [ ] | [ ] | [ ] |

---

## Section 2: API Surface

> What APIs does your team expose? What do consumers call?

| Endpoint / API | Method | Purpose | Consumers | Auth |
|---------------|--------|---------|-----------|------|
| [ ] | [ ] | [ ] | [ ] | [ ] |
| [ ] | [ ] | [ ] | [ ] | [ ] |
| [ ] | [ ] | [ ] | [ ] | [ ] |
| [ ] | [ ] | [ ] | [ ] | [ ] |

---

## Section 3: External Integrations

> What systems does your product depend on that your team does NOT own?

| System | Owner Team | Protocol | What You Use It For | Reliability |
|--------|-----------|----------|--------------------|----|
| [ ] | [ ] | REST / SOAP / MQ / gRPC / File | [ ] | Stable / Flaky / Unknown |
| [ ] | [ ] | [ ] | [ ] | [ ] |
| [ ] | [ ] | [ ] | [ ] | [ ] |
| [ ] | [ ] | [ ] | [ ] | [ ] |
| [ ] | [ ] | [ ] | [ ] | [ ] |

---

## Section 4: Data Stores

> What databases, caches, queues does your product use?

| Data Store | Type | What It Holds | Owned By | Shared? |
|-----------|------|--------------|----------|---------|
| [ ] | SQL / NoSQL / Cache / Queue / File | [ ] | [ ] | Yes / No |
| [ ] | [ ] | [ ] | [ ] | [ ] |
| [ ] | [ ] | [ ] | [ ] | [ ] |

---

## Section 5: Test Coverage

> Current state of testing — be honest, this drives improvement planning.

| Service | Unit Test % | Integration Test % | E2E? | Test Framework | CI/CD |
|---------|------------|-------------------|------|----------------|-------|
| [ ] | [ ] | [ ] | Yes / No | [ ] | [ ] |
| [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |

**Test Pyramid Assessment:**
- Current distribution: [ ]% unit / [ ]% integration / [ ]% E2E
- Constitutional target (ENG-4.2): 70-80% unit / 15-25% integration / 5-10% E2E
- Gap: [ ]

---

## Section 6: Tech Stack Summary

> Which technology avatar(s) apply to this product?

| Layer | Technology | Version | Constitution Avatar |
|-------|-----------|---------|-------------------|
| Backend | [ ] | [ ] | java-spring / python-fastapi / nodejs-typescript / dotnet-core / other |
| Frontend | [ ] | [ ] | react-typescript / angular / mobile-native / other |
| Database | [ ] | [ ] | N/A |
| Messaging | [ ] | [ ] | N/A |
| Infra | [ ] | [ ] | N/A |
| CI/CD | [ ] | [ ] | N/A |

---

## Section 7: Architecture Pain Points

> Where does the architecture hurt today?

| Pain Point | Severity | Impact | Known For How Long? |
|-----------|----------|--------|-------------------|
| [ ] | High / Med / Low | [ ] | [ ] |
| [ ] | [ ] | [ ] | [ ] |
| [ ] | [ ] | [ ] | [ ] |

---

## Validation Checklist

- [ ] Every service the team owns is listed with language and repo
- [ ] API surface documented (at least key endpoints)
- [ ] External integrations identified with reliability assessment
- [ ] Test coverage numbers are real (from CI/CD, not guesses)
- [ ] Technology avatar(s) identified for agent configuration
- [ ] Architecture pain points captured honestly
- [ ] Major findings are source-tagged with confidence levels
- [ ] Any external benchmarks include citations and directional disclaimer
