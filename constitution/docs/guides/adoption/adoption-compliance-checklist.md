# Adoption Compliance Checklist

**Purpose:** Verify that your project properly adopts the hangar-ai-constitution.

**Usage:** Review this checklist at adoption milestones and during audits.

---

## Constitutional Authority

This checklist verifies compliance with the **hangar-ai-constitution**.

> **Per ENG-1.2 (AI-Engineer Pairing Law)**: Every checklist item references the specific constitutional law that requires it.

---

## 1. Governance Files

| Item | Law ID | Requirement | Path | ✓ |
|------|--------|-------------|------|---|
| Root AGENTS.md exists | **ENG-1.2** | Entry point for AI assistants | `./AGENTS.md` | ☐ |
| AGENTS.md references Constitution | **ENG-1.2** | Path to hangar-ai-constitution | — | ☐ |
| AGENTS.md defines authority hierarchy | **ENG-1.1** | Constitution > project-rules > AGENTS.md | — | ☐ |
| hangar-ai-specs/ directory exists | **ENG-11.1** | Hangar SDD structure | `./hangar-ai-specs/` | ☐ |
| hangar-ai-specs/specs/ directory exists | **ENG-11.1** | Baseline specifications | `./hangar-ai-specs/specs/` | ☐ |
| hangar-ai-specs/changes/ directory exists | **ENG-11.1** | Change proposals | `./hangar-ai-specs/changes/` | ☐ |
| Technology stack documented | **ENG-1.2** | Language, framework, versions | — | ☐ |
| Domain concepts documented | **ENG-2.1** | Ubiquitous Language defined | — | ☐ |

### Governance Files — Verification Commands

```bash
# Run these commands to verify governance files compliance

# AGENTS.md at root (NOT in subdirectory)
[ -f "./AGENTS.md" ] && echo "✓ AGENTS.md at root" || echo "✗ AGENTS.md missing or misplaced"

# AGENTS.md references Constitution
grep -q "hangar-ai-constitution" AGENTS.md && echo "✓ Constitution referenced" || echo "✗ Constitution not referenced"

# AGENTS.md has authority hierarchy
grep -q "Authority" AGENTS.md && echo "✓ Authority section present" || echo "✗ Authority section missing"

# hangar-ai-specs structure exists
[ -d "./hangar-ai-specs/specs" ] && [ -d "./hangar-ai-specs/changes" ] && echo "✓ hangar-ai-specs structure complete" || echo "✗ hangar-ai-specs structure incomplete"
```

---

## 2. Test-Driven Development

| Item | Law ID | Requirement | ✓ |
|------|--------|-------------|---|
| Tests exist before production code | **ENG-4.1** | TDD practiced in atomic cycles | ☐ |
| Tests follow RED-GREEN-REFACTOR | **ENG-4.1** | One test at a time | ☐ |
| Test names describe behavior | **ENG-4.1** | `method_condition_expectedResult` | ☐ |
| No logic in tests | **ENG-4.1** | Tests are simple assertions | ☐ |
| Characterization tests for legacy | **ENG-4.4** | Brownfield: test before changing | ☐ |

---

## 3. Coverage Requirements

| Item | Law ID | Requirement | ✓ |
|------|--------|-------------|---|
| Coverage tool configured | **ENG-4.6** | JaCoCo, pytest-cov, etc. | ☐ |
| New code ≥90% line coverage | **ENG-4.6** | Enforced in CI | ☐ |
| Critical paths 100% coverage | **ENG-4.6** | Business logic, security, money | ☐ |
| Coverage trend tracked | **ENG-4.6** | Dashboard or reports | ☐ |
| Untested code documented | **ENG-1.3** | Technical debt tracked | ☐ |

---

## 4. Code Quality

| Item | Law ID | Requirement | ✓ |
|------|--------|-------------|---|
| Cyclomatic complexity ≤10 | **ENG-3.1** | Per method | ☐ |
| Cognitive complexity ≤7 | **ENG-3.2** | Per method | ☐ |
| Method length ≤50 lines | **ENG-3.4** | Single responsibility | ☐ |
| Class length ≤500 lines | **ENG-3.4** | Single responsibility | ☐ |
| Complexity tool configured | **ENG-3.1** | PMD, SonarQube, etc. | ☐ |
| Quality gates in CI | **ENG-3.1** | Build fails on violations | ☐ |

---

## 5. Domain-Driven Design

| Item | Law ID | Requirement | ✓ |
|------|--------|-------------|---|
| Bounded contexts identified | **ENG-2.1** | Clear domain boundaries | ☐ |
| Ubiquitous language defined | **ENG-2.1** | Domain terms documented | ☐ |
| Aggregates properly defined | **ENG-2.2** | Consistency boundaries clear | ☐ |
| Value objects immutable | **ENG-2.3** | Final fields, no setters | ☐ |
| Entities have identity | **ENG-2.2** | ID-based equality | ☐ |

---

## 6. Vertical Slices

| Item | Law ID | Requirement | ✓ |
|------|--------|-------------|---|
| Features in vertical slices | **ENG-2.5** | Not horizontal layers | ☐ |
| Each slice delivers value | **ENG-2.5** | End-to-end functionality | ☐ |
| Slices are thin | **ENG-2.5** | Minimum viable increment | ☐ |
| Hangar SDD proposals use slices | **ENG-11.2** | Structured slice definitions | ☐ |

---

## 7. Security

| Item | Law ID | Requirement | ✓ |
|------|--------|-------------|---|
| Security built in from start | **ENG-6.1** | Not bolted on later | ☐ |
| Input validation present | **ENG-6.1** | All external inputs validated | ☐ |
| Output encoding applied | **ENG-6.1** | Prevent injection attacks | ☐ |
| Authentication configured | **ENG-6.2** | Identity management | ☐ |
| Authorization implemented | **ENG-6.3** | Access control | ☐ |
| Sensitive data protected | **ENG-6.4** | Encryption at rest and transit | ☐ |
| Secrets not in code | **ENG-6.5** | Environment or vault | ☐ |
| Dependencies scanned | **ENG-6.6** | CVE checking enabled | ☐ |

---

## 8. Audit Trail

| Item | Law ID | Requirement | ✓ |
|------|--------|-------------|---|
| Sensitive operations logged | **ENG-6.7** | Immutable audit records | ☐ |
| Log entries include context | **ENG-6.7** | Who, what, when, where | ☐ |
| Logs are tamper-proof | **ENG-6.7** | Cannot be modified | ☐ |
| Retention policy defined | **ENG-6.7** | Per regulatory requirements | ☐ |

---

## 9. Continuous Refactoring

| Item | Law ID | Requirement | ✓ |
|------|--------|-------------|---|
| Boy Scout Rule practiced | **ENG-1.3** | Leave code cleaner | ☐ |
| Technical debt documented | **ENG-1.3** | In project-rules.md | ☐ |
| Debt includes law violations | **ENG-1.3** | Which law it violates | ☐ |
| Remediation phases defined | **ENG-1.3** | When debt will be addressed | ☐ |

---

## 10. AI Pairing

| Item | Law ID | Requirement | ✓ |
|------|--------|-------------|---|
| AI assistants follow Constitution | **ENG-1.2** | Not generic advice | ☐ |
| AI explains WHY | **ENG-1.2** | Cites laws for decisions | ☐ |
| Human retains authority | **ENG-1.2** | AI suggests, human decides | ☐ |
| AI guides toward compliance | **ENG-1.2** | Proactive quality coaching | ☐ |

---

## Compliance Summary

| Category | Items | Checked | Compliant |
|----------|-------|---------|-----------|
| Governance Files | 8 | ___ | ☐ |
| Test-Driven Development | 5 | ___ | ☐ |
| Coverage Requirements | 5 | ___ | ☐ |
| Code Quality | 6 | ___ | ☐ |
| Domain-Driven Design | 5 | ___ | ☐ |
| Vertical Slices | 4 | ___ | ☐ |
| Security | 8 | ___ | ☐ |
| Audit Trail | 4 | ___ | ☐ |
| Continuous Refactoring | 4 | ___ | ☐ |
| AI Pairing | 4 | ___ | ☐ |
| **TOTAL** | **53** | ___ | ☐ |

---

## Adoption Levels

| Level | Threshold | Status |
|-------|-----------|--------|
| **Non-Compliant** | <50% items checked | ⚠️ |
| **Adopting** | 50-79% items checked | 🔄 |
| **Compliant** | 80-99% items checked | ✅ |
| **Exemplary** | 100% items checked | ⭐ |

---

## Audit Notes

**Auditor:** _______________

**Date:** _______________

**Compliance Level:** _______________

**Findings:**

1. _______________
2. _______________
3. _______________

**Remediation Required:**

1. _______________
2. _______________
3. _______________

---

## Common Adoption Mistakes

> **For AI Agents and Engineers:** Review these common mistakes to avoid adoption failures.

### File Placement Mistakes

| Mistake | Why It's Wrong | Fix |
|---------|----------------|-----|
| `src/AGENTS.md` | AGENTS.md must be at project root for AI agent discovery | `mv src/AGENTS.md ./AGENTS.md` |
| `app/AGENTS.md` | AGENTS.md must be at project root | `mv app/AGENTS.md ./AGENTS.md` |
| `hangar-ai-specs/AGENTS.md` | AGENTS.md must be at project root for AI agent discovery | `mv hangar-ai-specs/AGENTS.md ./AGENTS.md` |
| Missing `hangar-ai-specs/specs/` | Baseline specs have no location | `mkdir -p hangar-ai-specs/specs` |
| Missing `hangar-ai-specs/changes/` | Change proposals have no location | `mkdir -p hangar-ai-specs/changes` |

### Content Mistakes

| Mistake | Why It's Wrong | Fix |
|---------|----------------|-----|
| AGENTS.md missing Constitution reference | AI agents won't know to follow Constitution | Add `hangar-ai-constitution` path to Authority section |
| AGENTS.md missing Authority Hierarchy | Precedence rules unclear | Add authority hierarchy section per template |
| Using `PROJECT-CONSTITUTION.md` | Deprecated filename | Rename to `project-rules.md` at repo root |
| Empty `hangar-ai-specs/specs/` | No baseline documented | Generate baseline specs before changes |

### Process Mistakes

| Mistake | Why It's Wrong | Fix |
|---------|----------------|-----|
| Skipping validation checkpoint | Structure errors not caught early | Run validation commands after Step 1.1 |
| Creating change proposal before baseline | No source of truth for current behavior | Complete Step 1.3 before Step 1.4 |
| Proceeding after validation failure | Broken structure propagates | Stop and fix all validation failures |

---

## Related Resources

- [Brownfield Adoption Guide](./brownfield-adoption.md)
- [Greenfield MVP Guide](./greenfield-mvp.md)
- [AGENTS.md Template](../../templates/AGENTS.md)
- [project-rules.md Template](../../templates/project-rules.md)

---

**Last Updated:** February 12, 2026
