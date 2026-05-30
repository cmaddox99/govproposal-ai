# Aviation / FAA Constitution Adoption

**Base Constitution:** [BUSINESS-CONSTITUTION.md](../../../laws/business/)
**Regulations:** FAA Part 25/121/135, DO-178C, DO-254, AS9100
**Last Updated:** January 2026

> This document shows how the Base Business Constitution laws apply specifically to aviation software and aerospace organizations.

---

## Regulatory Overview

### Key Standards

| Standard | Scope | Focus |
|----------|-------|-------|
| **DO-178C** | Airborne software | Software assurance levels |
| **DO-254** | Airborne hardware | Hardware assurance levels |
| **DO-326A** | Airborne security | Cybersecurity for aircraft |
| **AS9100** | Aerospace QMS | Quality management |

### Software Levels (DO-178C)

| Level | Failure Condition | Examples |
|-------|-------------------|----------|
| **A** | Catastrophic | Flight control, autopilot |
| **B** | Hazardous | Engine control |
| **C** | Major | Navigation display |
| **D** | Minor | Entertainment system |
| **E** | No effect | Cabin lighting |

---

## DO-178C Laws

### Section A.1: Development Assurance Law

**Software MUST meet assurance level requirements:**

```yaml
# DO-178C Objectives by Level
objectives:
  level_a:  # 71 objectives, all must be met with independence
    planning: 7
    development: 26
    verification: 28
    configuration: 6
    quality_assurance: 4
    independence_required: true

  level_b:  # 69 objectives
    independence_required: true
    reduced_from_a:
      - some_structural_coverage_objectives

  level_c:  # 62 objectives
    independence_required: false

  level_d:  # 26 objectives
    independence_required: false
```

### Section A.2: Requirements Traceability Law

**All requirements MUST be traceable:**

```
REQUIREMENTS TRACEABILITY

System Requirements
       ↓ (traced to)
High-Level Software Requirements
       ↓ (traced to)
Low-Level Software Requirements
       ↓ (traced to)
Source Code
       ↓ (traced to)
Test Cases
       ↓ (verified by)
Test Results

Every requirement must trace DOWN to implementation
Every test must trace UP to requirements
No orphan code (all code traced to requirements)
```

### Section A.3: Structural Coverage Law

**Code coverage requirements by level:**

| Level | Statement | Decision | MC/DC |
|-------|-----------|----------|-------|
| **A** | Required | Required | Required |
| **B** | Required | Required | - |
| **C** | Required | - | - |
| **D** | - | - | - |

```python
# ✅ COMPLIANT - Full MC/DC coverage for Level A
def calculate_altitude_alert(
    current_altitude: int,
    target_altitude: int,
    rate_of_climb: int
) -> AlertLevel:
    """
    DO-178C Level A function - MC/DC coverage required.

    Test cases for MC/DC:
    | current | target | rate | expected | covers |
    |---------|--------|------|----------|--------|
    | 10000 | 12000 | 500 | NOMINAL | baseline |
    | 11500 | 12000 | 500 | CAUTION | condition 1 true |
    | 10000 | 12000 | -500 | WARNING | condition 2 true |
    | 11800 | 12000 | 1000 | WARNING | compound true |
    """
    approaching = (target_altitude - current_altitude) < 1000

    if approaching and rate_of_climb > 0:  # Decision 1
        if (target_altitude - current_altitude) < 200:  # Decision 2
            return AlertLevel.WARNING
        return AlertLevel.CAUTION

    if rate_of_climb < 0 and current_altitude < target_altitude:  # Decision 3
        return AlertLevel.WARNING

    return AlertLevel.NOMINAL
```

---

## Configuration Management

### Section A.4: Configuration Identification Law

**All items MUST be under configuration control:**

```yaml
configuration_items:
  software:
    - requirements_documents
    - design_documents
    - source_code
    - object_code
    - executable_code
    - test_cases
    - test_procedures
    - test_results

  environment:
    - compilers_version
    - linkers_version
    - test_tools_version
    - qualified_tools

  data:
    - parameter_data_files
    - configuration_tables

control_requirements:
  identification: "Unique identifier + version"
  change_control: "CCB approval required"
  baseline: "Established at each life cycle milestone"
  audit: "Regular audits for compliance"
```

### Section A.5: Problem Reporting Law

**All problems MUST be tracked to closure:**

```python
@dataclass
class ProblemReport:
    """DO-178C compliant problem report."""
    pr_id: str  # Unique identifier
    title: str
    severity: Severity  # 1-4
    detected_in_phase: LifecyclePhase
    affected_items: list[str]  # Configuration items
    description: str
    root_cause: str | None
    correction: str | None
    verification_method: str | None
    status: PRStatus
    closed_date: datetime | None

    # Traceability
    related_requirements: list[str]
    related_test_cases: list[str]

    # For Level A/B - independence
    verified_by: str  # Different from author
```

---

## Testing Laws

### Section A.6: Requirements-Based Testing Law

**All requirements MUST have tests:**

```python
# ✅ COMPLIANT - Requirements-based test
class TestAltitudeAlert:
    """
    Tests for calculate_altitude_alert

    Requirement Coverage:
    - REQ-ALT-001: Alert when within 1000ft of target
    - REQ-ALT-002: Warning when within 200ft
    - REQ-ALT-003: Warning on descent below target
    """

    @requirement("REQ-ALT-001")
    def test_caution_when_approaching_target(self):
        """Verify caution alert when within 1000ft."""
        result = calculate_altitude_alert(
            current_altitude=11500,
            target_altitude=12000,
            rate_of_climb=500
        )
        assert result == AlertLevel.CAUTION

    @requirement("REQ-ALT-002")
    def test_warning_when_very_close_to_target(self):
        """Verify warning alert when within 200ft."""
        result = calculate_altitude_alert(
            current_altitude=11850,
            target_altitude=12000,
            rate_of_climb=500
        )
        assert result == AlertLevel.WARNING
```

---

## Quality Assurance

### Section A.7: Software Quality Assurance Law

**SQA MUST verify compliance:**

```markdown
## SQA Audit Checklist (DO-178C)

### Planning Phase
- [ ] Plans complete and approved
- [ ] Standards defined
- [ ] Transition criteria defined

### Development Phase
- [ ] Requirements traceable to system
- [ ] Design traceable to requirements
- [ ] Code traceable to design
- [ ] Coding standards followed

### Verification Phase
- [ ] Test cases trace to requirements
- [ ] Coverage analysis complete
- [ ] All tests passed or PRs opened
- [ ] Review records complete

### Configuration
- [ ] All items identified
- [ ] Change control followed
- [ ] Baselines established

### Documentation
- [ ] SAS (Software Accomplishment Summary) complete
- [ ] SCI (Software Configuration Index) complete
- [ ] All life cycle data archived
```

---

## Quick Reference

### DO-178C Life Cycle Data

| Document | Level A | Level B | Level C | Level D |
|----------|---------|---------|---------|---------|
| Plan for Software Aspects | ✓ | ✓ | ✓ | ✓ |
| Software Development Plan | ✓ | ✓ | ✓ | ✓ |
| Software Verification Plan | ✓ | ✓ | ✓ | ✓ |
| Software Requirements Data | ✓ | ✓ | ✓ | ✓ |
| Software Design Description | ✓ | ✓ | ✓ | - |
| Source Code | ✓ | ✓ | ✓ | ✓ |
| Test Cases/Procedures | ✓ | ✓ | ✓ | ✓ |
| Test Results | ✓ | ✓ | ✓ | ✓ |
| SAS | ✓ | ✓ | ✓ | ✓ |
| SCI | ✓ | ✓ | ✓ | ✓ |

### Certification Checklist

```markdown
## Before Certification Audit

- [ ] All plans approved by DER/DAR
- [ ] Requirements 100% traced and tested
- [ ] Structural coverage met for level
- [ ] All problem reports closed or deferred
- [ ] Tool qualification complete (if applicable)
- [ ] SQA audits complete
- [ ] Life cycle data archived
- [ ] SAS signed by SQA
```
