---
skill:
  id: skill-27-constitution-compliance
  name: Constitution Compliance
  category: governance
  version: "2.0.0"

laws:
  implements:
    - id: ENG-10.2
      title: Compliance Monitoring Law
      relationship: primary
    - id: ENG-10.1
      title: Amendment Process Law
      relationship: primary
    - id: BUS-7.1
      title: Audit Trail Law
      relationship: primary
  references:
    - id: ENG-4.1
      title: Atomic TDD Law
      context: Verify TDD compliance in all changes
    - id: ENG-6.7
      title: Audit Trail Law
      context: Track compliance evidence

triggers:
  phrases:
    - "Check constitution compliance"
    - "Validate against laws"
    - "Compliance report"
    - "Constitution audit"
    - "Law violations"

prerequisites:
  - Constitution laws loaded in context
  - Access to codebase for analysis

followed_by:
  - skill-08-code-review

related_skills:
  - skill-06-atomic-tdd
  - skill-10-security-review
  - skill-13-observability
---

# Skill: Constitution Compliance

> **Purpose:** Validate code changes and development practices against the American Airlines AI Constitution laws.
> **Workflow:** See `workflows/legacy-rescue-refactor.md` for compliance assessment in constitutional remediation, `workflows/legacy-rescue-rewrite.md` for compliance assessment in behavioral-parity rewrites, and `workflows/legacy-rescue-decision-track.md` for regulatory scope identification in the refactor/rewrite decision.

---

## Purpose

This skill enables AI agents to:

1. **Check law compliance** - Verify code against specific constitutional laws
2. **Generate compliance reports** - Document adherence or violations
3. **Suggest remediations** - Provide fixes for violations
4. **Track compliance metrics** - Monitor compliance trends over time
5. **Support audits** - Generate evidence for compliance audits

---

## When to Invoke

Invoke this skill when:
- Reviewing code changes for constitutional compliance
- Preparing for compliance audits
- Setting up compliance monitoring
- Investigating potential violations
- Generating compliance reports

---

## Compliance Check Categories

### Engineering Law Compliance

| Law | Check | Automation |
|-----|-------|------------|
| ENG-4.1 (Atomic TDD) | Test-before-code verification | CI/CD gate |
| ENG-3.1 (Complexity) | Cyclomatic complexity ≤10 | Static analysis |
| ENG-6.1 (Security) | OWASP Top 10 validation | SAST tools |
| ENG-6.7 (Audit Trail) | Logging completeness | Log analysis |

### Product Law Compliance

| Law | Check | Automation |
|-----|-------|------------|
| PRD-3.4 (Experience Principles) | WCAG 2.1 AA compliance | a11y testing |
| PRD-5.1 (MVP) | Feature scope validation | Manual review |

### Business Law Compliance

| Law | Check | Automation |
|-----|-------|------------|
| BUS-2.1 (FAA) | Aviation regulation adherence | Manual audit |
| BUS-2.2 (TSA) | Security directive compliance | Security scan |
| BUS-7.1 (Audit Trail) | Complete audit logging | Log audit |

---

## Compliance Report Template

```markdown
# Constitution Compliance Report

**Project:** [Project Name]
**Date:** [Date]
**Reviewer:** [AI Agent + Human Reviewer]

## Summary

| Domain | Compliant | Violations | Risk Level |
|--------|-----------|------------|------------|
| Engineering | X/Y | Z | Low/Medium/High |
| Product | X/Y | Z | Low/Medium/High |
| Business | X/Y | Z | Low/Medium/High |

## Critical Violations (Non-Negotiable Laws)

### [LAW-X.X] [Law Name]
- **Status:** VIOLATION
- **Evidence:** [Description of violation]
- **Impact:** [Business/Security impact]
- **Remediation:** [Required fix]
- **Deadline:** [Based on severity]

## Recommendations

1. [Recommendation 1]
2. [Recommendation 2]

## Evidence Artifacts

- [ ] Test coverage report
- [ ] Security scan results
- [ ] Audit log samples
```

---

## Integration with CI/CD

### GitHub Actions Integration

```yaml
name: Constitution Compliance Check

on:
  pull_request:
    branches: [main, develop]

jobs:
  compliance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Check ENG-4.1 (TDD Compliance)
        run: |
          # Verify tests exist for changed files
          ./scripts/check-tdd-compliance.sh
          
      - name: Check ENG-3.1 (Complexity)
        run: |
          # Run complexity analysis
          ./scripts/check-complexity.sh
          
      - name: Check ENG-6.1 (Security)
        run: |
          # Run security scan
          ./scripts/security-scan.sh
          
      - name: Generate Compliance Report
        run: |
          ./scripts/generate-compliance-report.sh
```

---

## Compliance Monitoring Dashboard

### Key Metrics

1. **Compliance Score** - Overall % of laws being followed
2. **Critical Violations** - Count of non-negotiable law violations
3. **Trend** - Compliance improvement/degradation over time
4. **Coverage** - % of codebase under compliance monitoring

### Alerting Thresholds

| Metric | Warning | Critical |
|--------|---------|----------|
| Compliance Score | <90% | <80% |
| Critical Violations | >0 | >3 |
| Test Coverage | <80% | <70% |

---

## Aviation-Specific Compliance

### FAA Compliance (BUS-2.1)

- DO-178C traceability for safety-critical systems
- FAR Part 117 crew rest calculations validated
- All changes auditable

### TSA Compliance (BUS-2.2)

- Security directive adherence
- Vetting system integration verified
- Access controls documented

### DOT Compliance (BUS-2.3)

- Fare transparency requirements
- Refund processing timelines
- Consumer protection adherence

---

## Workflow Integration

This skill integrates with:

- **`workflows/legacy-rescue-refactor.md`** — Phase 1 (Assess): compliance assessment gate; Phase 6 (Certify): final compliance report
- **`workflows/legacy-rescue-rewrite.md`** — Phase 1 (Assess): regulatory scope identification; Phase 6 (Certify): before/after compliance evidence
- **`workflows/legacy-rescue-decision-track.md`** — Phase 1 (Archaeology): per-bounded-context regulatory mapping; Phase 3 (Deliberate): compliance risk as REFACTOR/REWRITE decision factor
- **`workflows/greenfield-development.md`** — Phase 7 (Review): constitution compliance sign-off before ship

---

## AI Tool Guidelines

When using GitHub Copilot for compliance:

1. **Always cite laws** - Reference specific law IDs (e.g., ENG-4.1)
2. **Check non-negotiables first** - Priority on critical laws
3. **Document exceptions** - Any deviation requires documented approval
4. **Generate evidence** - Create artifacts for audit trails

---

## References

- [Engineering Laws](../../../laws/engineering/)
- [Product Laws](../../../laws/product/)
- [Business Laws](../../../laws/business/)
- [Laws Index](../../../laws/index.yaml)
