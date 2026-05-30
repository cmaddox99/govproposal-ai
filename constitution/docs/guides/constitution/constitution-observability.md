# Constitution Observability Guide

> **Guide ID:** constitution-observability  
> **Laws:** ENG-10.1, ENG-10.2, ENG-10.3, ENG-10.4, ENG-10.5  
> **Source law file:** laws/engineering/governance.md  
> This guide contains implementation detail extracted from ENG-10.x law bodies. The SHALL requirements remain in governance.md.

---

## ENG-10.1 — Metrics Collection: Implementation

### Metric Schema

```yaml
constitution_metrics:
  compliance:
    law_id: "ENG-4.1"
    result: "pass" | "fail" | "skip"
    timestamp: "2026-01-15T10:30:00Z"
    context:
      project: "order-service"
      team: "checkout-team"
      evaluation_point: "pre-commit" | "ci-pipeline" | "ai-agent" | "code-review"

  dimensions:
    - law_id
    - project
    - team
    - evaluation_point
    - result
```

### Metric Categories

| Category | Metrics | Collection Frequency |
|----------|---------|---------------------|
| Compliance Rate | Laws passed / Laws evaluated | Per commit, per PR |
| Violation Count | Total violations by law ID | Real-time |
| Violation Severity | Critical, Warning, Info breakdown | Real-time |
| Law Coverage | Laws evaluated / Total applicable laws | Daily |
| Evaluation Latency | Time to evaluate compliance | Per evaluation |

---

## ENG-10.2 — Enforcement Tracking: Event Schema

```yaml
enforcement_event:
  event_id: "evt_abc123"
  timestamp: "2026-01-15T10:30:00Z"
  law_id: "ENG-4.1"
  law_title: "Atomic TDD Law"

  violation:
    severity: "critical" | "warning" | "info"
    description: "Implementation code written without failing test"
    file_path: "src/services/OrderService.java"
    line_number: 47

  detection:
    stage: "pre-commit" | "ci-pipeline" | "code-review" | "ai-agent"
    tool: "constitutional-linter" | "ai-reviewer" | "human-reviewer"

  enforcement:
    action: "blocked" | "warned" | "exception-granted"
    exception_reason: null | "legacy-code-exemption"
    exception_approver: null | "tech-lead@example.com"

  resolution:
    status: "pending" | "resolved" | "wont-fix"
    resolved_at: null | "2026-01-15T11:00:00Z"
    resolved_by: null | "engineer@example.com"
    resolution_method: null | "test-added" | "code-reverted" | "exception-documented"
```

### Key Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| Mean Time to Resolution (MTTR) | avg(resolved_at - timestamp) | < 4 hours |
| First-Stage Detection Rate | pre-commit detections / total detections | > 80% |
| Exception Rate | exceptions / total violations | < 5% |
| Resolution Rate | resolved / (resolved + pending) | > 95% |

---

## ENG-10.3 — Compliance Reporting: Report Schema and Types

### Report Types

| Report | Frequency | Audience | Key Contents |
|--------|-----------|----------|--------------|
| Daily Digest | Daily | Engineers, Tech Leads | Violations by law, unresolved issues |
| Weekly Summary | Weekly | Engineering Managers | Compliance trends, team comparisons |
| Monthly Governance | Monthly | Leadership, Compliance | Overall health, risk areas, recommendations |
| Quarterly Review | Quarterly | Executive, Audit | YoY trends, strategic recommendations |

### Report Schema

```yaml
compliance_report:
  metadata:
    report_type: "weekly-summary"
    period_start: "2026-01-08"
    period_end: "2026-01-15"
    generated_at: "2026-01-15T06:00:00Z"

  summary:
    overall_compliance_rate: 94.2
    total_evaluations: 12547
    total_violations: 726
    violations_resolved: 689
    open_violations: 37

  by_domain:
    engineering:
      compliance_rate: 93.8
      top_violated_laws:
        - law_id: "ENG-4.1"
          violations: 142
          trend: "improving"

  trends:
    compliance_rate_delta: +2.1
    mttr_delta: -1.2

  recommendations:
    - area: "Testing Laws"
      priority: "high"
      action: "Schedule TDD refresher training for checkout team"
```

---

## ENG-10.4 — Health Dashboard: Specifications

### Dashboard Hierarchy

```
Level 1: Organization Health
├── Overall Compliance Score: 94.2/100
├── Active Violations: 37
├── Teams in Good Standing: 12/15
└── Risk Areas: 2 (Testing, Security)

Level 2: Team Dashboard
├── Team Compliance Score
├── Violation Breakdown by Law
├── MTTR Trend
└── Top Improvement Opportunities

Level 3: Project Dashboard
├── Project Compliance Score
├── Recent Violations (last 7 days)
├── Law-by-Law Status
└── Historical Trend (30 days)
```

### Health Score Calculation

```python
def calculate_health_score(metrics: ComplianceMetrics) -> float:
    """
    Calculate overall constitution health score (0-100).
    Weights: Compliance Rate 40%, Resolution Rate 25%,
    First-Stage Detection 20%, Exception Rate 15% (inverse).
    """
    return round((
        metrics.compliance_rate * 0.40 +
        metrics.resolution_rate * 0.25 +
        metrics.first_stage_detection_rate * 0.20 +
        (1 - metrics.exception_rate) * 0.15
    ) * 100, 1)
```

### Dashboard Panels

| Panel | Metrics | Refresh Rate |
|-------|---------|--------------|
| Health Score | Overall score, trend arrow | 5 min |
| Compliance by Domain | ENG, PRD, BUS breakdown | 5 min |
| Violation Heatmap | Violations by law and team | 15 min |
| MTTR Gauge | Current vs target MTTR | 5 min |
| Trend Graph | 30-day compliance trend | 1 hour |
| Alert Feed | Recent critical violations | Real-time |

---

## ENG-10.5 — Law Effectiveness: Framework and Card Schema

### Effectiveness Framework

| Law Category | Leading Indicators | Lagging Indicators |
|--------------|-------------------|-------------------|
| Testing Laws | Test coverage %, TDD cycle time | Defect escape rate, production bugs |
| Security Laws | Security review completion | Security incidents, CVEs |
| Quality Laws | Complexity scores, review feedback | Technical debt, rework rate |
| Architecture Laws | Layer violation count | System coupling, change impact |

### Law Effectiveness Card Schema

```yaml
law_effectiveness:
  law_id: "ENG-4.1"
  law_title: "Atomic TDD Law"

  intended_outcomes:
    - "Reduce defect escape rate"
    - "Improve code design through test-first thinking"
    - "Enable safe refactoring"

  success_metrics:
    - metric: "defect_escape_rate"
      baseline: 12.5
      target: 5.0
      current: 6.2
      trend: "improving"
    - metric: "test_coverage"
      baseline: 45
      target: 80
      current: 78
      trend: "stable"

  effectiveness_score: 87
  review:
    last_reviewed: "2025-12-15"
    next_review: "2026-03-15"
    reviewer: "engineering-governance@example.com"
```

### Effectiveness Dashboard Metrics

| Metric | Formula | Purpose |
|--------|---------|---------|
| Defect Delta | (post_adoption - baseline) / baseline | Measure defect reduction |
| Velocity Impact | post_adoption_velocity / baseline_velocity | Ensure laws don't slow teams |
| Adoption Depth | teams_fully_compliant / total_teams | Track organizational adoption |
| Developer Sentiment | Survey NPS for law | Ensure laws are practical |

---

## Implementation Priority

| Phase | Laws | Focus |
|-------|------|-------|
| 1 — Foundation | ENG-10.1, ENG-10.2 | Establish collection and tracking |
| 2 — Visibility | ENG-10.4 | Enable real-time monitoring |
| 3 — Governance | ENG-10.3 | Formalize reporting processes |
| 4 — Optimization | ENG-10.5 | Enable continuous improvement |

---

## Cross-References

| Law | Related Laws | Relationship |
|-----|--------------|--------------|
| ENG-10.1 | ENG-5.5, BUS-7.1 | Extends observability to constitution compliance |
| ENG-10.2 | ENG-6.7, BUS-7.1 | Applies audit trail principles to enforcement |
| ENG-10.3 | BUS-7.2, PRD-8.1 | Aligns with audit and analytics requirements |
| ENG-10.4 | ENG-5.5, ENG-7.7 | Leverages observability infrastructure |
| ENG-10.5 | PRD-5.3, PRD-6.1 | Applies experimentation principles to laws |
