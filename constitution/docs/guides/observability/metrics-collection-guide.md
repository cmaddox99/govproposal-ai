# Metrics Collection Guide

**Detailed Metrics Definitions for Engineers**

---

## Overview

This guide provides comprehensive documentation of all constitution compliance metrics, including their definitions, collection methods, and usage patterns. Use this as a reference when instrumenting your systems for constitution observability.

**Audience:** Engineers, DevOps, SREs

---

## Metric Categories

| Category | Purpose | Key Metrics |
|----------|---------|-------------|
| Compliance | Track law adherence | Evaluations, pass rate, coverage |
| Violations | Track failures | Count, severity, detection stage |
| Resolution | Track remediation | Time to resolve, resolution rate |
| Health | Track overall status | Health score, trends |
| Effectiveness | Track law success | Outcome metrics, baselines |

---

## Core Metrics

### 1. Law Evaluations

**Metric Name:** `constitution_law_evaluations_total`

**Type:** Counter

**Description:** Total number of law evaluations performed across all evaluation points.

**Labels:**

| Label | Description | Example Values |
|-------|-------------|----------------|
| `law_id` | Constitution law identifier | `ENG-4.1`, `PRD-3.2`, `BUS-7.1` |
| `law_domain` | Domain of the law | `ENG`, `PRD`, `BUS` |
| `result` | Evaluation outcome | `pass`, `fail`, `skip` |
| `evaluation_point` | Where evaluation occurred | `pre_commit`, `ci_pipeline`, `code_review`, `ai_agent` |
| `project` | Project identifier | `order-service`, `auth-api` |
| `team` | Team identifier | `checkout-team`, `platform` |

**Collection Code:**

```python
from prometheus_client import Counter

LAW_EVALUATIONS = Counter(
    'constitution_law_evaluations_total',
    'Total constitution law evaluations',
    ['law_id', 'law_domain', 'result', 'evaluation_point', 'project', 'team']
)

def record_evaluation(
    law_id: str,
    result: str,
    evaluation_point: str,
    project: str,
    team: str
):
    law_domain = law_id.split('-')[0]  # Extract ENG, PRD, BUS
    LAW_EVALUATIONS.labels(
        law_id=law_id,
        law_domain=law_domain,
        result=result,
        evaluation_point=evaluation_point,
        project=project,
        team=team
    ).inc()
```

**Example Queries:**

```promql
# Overall compliance rate (5m window)
sum(rate(constitution_law_evaluations_total{result="pass"}[5m]))
/
sum(rate(constitution_law_evaluations_total[5m]))

# Compliance by domain
sum by (law_domain) (rate(constitution_law_evaluations_total{result="pass"}[1h]))
/
sum by (law_domain) (rate(constitution_law_evaluations_total[1h]))

# Evaluations per team (24h)
sum by (team) (increase(constitution_law_evaluations_total[24h]))
```

---

### 2. Violations

**Metric Name:** `constitution_violations_total`

**Type:** Counter

**Description:** Total number of constitution law violations detected.

**Labels:**

| Label | Description | Example Values |
|-------|-------------|----------------|
| `law_id` | Constitution law identifier | `ENG-4.1`, `PRD-3.2` |
| `law_domain` | Domain of the law | `ENG`, `PRD`, `BUS` |
| `severity` | Violation severity | `critical`, `warning`, `info` |
| `detection_stage` | Where violation was detected | `pre_commit`, `ci_pipeline`, `code_review`, `ai_agent` |
| `action` | Enforcement action taken | `blocked`, `warned`, `exception` |
| `project` | Project identifier | `order-service` |
| `team` | Team identifier | `checkout-team` |

**Severity Classification:**

| Severity | Criteria | Response |
|----------|----------|----------|
| `critical` | Non-negotiable law violated | Block immediately |
| `warning` | Required law violated | Warn, track resolution |
| `info` | Best practice not followed | Log for awareness |

**Non-negotiable laws (always critical):**
- ENG-4.1, ENG-6.1, ENG-6.4, ENG-6.7
- PRD-1.2, PRD-1.5, PRD-5.1, PRD-6.2
- BUS-1.1, BUS-4.3, BUS-7.1, BUS-9.3

**Collection Code:**

```python
from prometheus_client import Counter

VIOLATIONS = Counter(
    'constitution_violations_total',
    'Total constitution violations',
    ['law_id', 'law_domain', 'severity', 'detection_stage', 'action', 'project', 'team']
)

NON_NEGOTIABLE_LAWS = {
    'ENG-4.1', 'ENG-6.1', 'ENG-6.4', 'ENG-6.7',
    'PRD-1.2', 'PRD-1.5', 'PRD-5.1', 'PRD-6.2',
    'BUS-1.1', 'BUS-4.3', 'BUS-7.1', 'BUS-9.3'
}

def record_violation(
    law_id: str,
    detection_stage: str,
    action: str,
    project: str,
    team: str
):
    severity = 'critical' if law_id in NON_NEGOTIABLE_LAWS else 'warning'
    law_domain = law_id.split('-')[0]

    VIOLATIONS.labels(
        law_id=law_id,
        law_domain=law_domain,
        severity=severity,
        detection_stage=detection_stage,
        action=action,
        project=project,
        team=team
    ).inc()
```

**Example Queries:**

```promql
# Total violations (7 days)
sum(increase(constitution_violations_total[7d]))

# Critical violations by law
sum by (law_id) (increase(constitution_violations_total{severity="critical"}[7d]))

# First-stage detection rate
sum(rate(constitution_violations_total{detection_stage="pre_commit"}[24h]))
/
sum(rate(constitution_violations_total[24h]))

# Exception rate
sum(rate(constitution_violations_total{action="exception"}[7d]))
/
sum(rate(constitution_violations_total[7d]))
```

---

### 3. Resolution Time

**Metric Name:** `constitution_violation_resolution_seconds`

**Type:** Histogram

**Description:** Time taken to resolve constitution violations.

**Labels:**

| Label | Description | Example Values |
|-------|-------------|----------------|
| `law_id` | Constitution law identifier | `ENG-4.1` |
| `severity` | Violation severity | `critical`, `warning` |
| `resolution_method` | How violation was resolved | `fixed`, `reverted`, `exception_documented` |

**Buckets:**

```python
RESOLUTION_BUCKETS = [
    300,      # 5 minutes
    900,      # 15 minutes
    3600,     # 1 hour
    14400,    # 4 hours (target for critical)
    43200,    # 12 hours
    86400,    # 24 hours
    172800,   # 48 hours
    604800    # 7 days
]
```

**Collection Code:**

```python
from prometheus_client import Histogram
from datetime import datetime

RESOLUTION_TIME = Histogram(
    'constitution_violation_resolution_seconds',
    'Time to resolve constitution violations',
    ['law_id', 'severity', 'resolution_method'],
    buckets=RESOLUTION_BUCKETS
)

def record_resolution(
    law_id: str,
    severity: str,
    resolution_method: str,
    violation_timestamp: datetime,
    resolution_timestamp: datetime
):
    duration = (resolution_timestamp - violation_timestamp).total_seconds()

    RESOLUTION_TIME.labels(
        law_id=law_id,
        severity=severity,
        resolution_method=resolution_method
    ).observe(duration)
```

**Example Queries:**

```promql
# Median resolution time (50th percentile)
histogram_quantile(0.50,
  sum by (le) (rate(constitution_violation_resolution_seconds_bucket[7d]))
)

# 90th percentile resolution time by severity
histogram_quantile(0.90,
  sum by (le, severity) (rate(constitution_violation_resolution_seconds_bucket[7d]))
)

# MTTR for critical violations
histogram_quantile(0.50,
  sum by (le) (rate(constitution_violation_resolution_seconds_bucket{severity="critical"}[7d]))
) / 3600  # Convert to hours
```

---

### 4. Violations Resolved

**Metric Name:** `constitution_violations_resolved_total`

**Type:** Counter

**Description:** Total number of violations that have been resolved.

**Labels:**

| Label | Description | Example Values |
|-------|-------------|----------------|
| `law_id` | Constitution law identifier | `ENG-4.1` |
| `severity` | Violation severity | `critical`, `warning` |
| `resolution_method` | How resolved | `fixed`, `reverted`, `exception_documented` |

**Collection Code:**

```python
from prometheus_client import Counter

VIOLATIONS_RESOLVED = Counter(
    'constitution_violations_resolved_total',
    'Total resolved constitution violations',
    ['law_id', 'severity', 'resolution_method']
)

def record_resolution(law_id: str, severity: str, method: str):
    VIOLATIONS_RESOLVED.labels(
        law_id=law_id,
        severity=severity,
        resolution_method=method
    ).inc()
```

**Example Queries:**

```promql
# Resolution rate
sum(increase(constitution_violations_resolved_total[7d]))
/
sum(increase(constitution_violations_total[7d]))

# Open violations (current)
sum(constitution_violations_total) - sum(constitution_violations_resolved_total)
```

---

### 5. Health Score

**Metric Name:** `constitution_health_score`

**Type:** Gauge

**Description:** Calculated constitution health score (0-100).

**Labels:**

| Label | Description | Example Values |
|-------|-------------|----------------|
| `scope` | Level of aggregation | `org`, `team`, `project` |
| `scope_id` | Identifier for scope | `checkout-team`, `order-service` |

**Calculation:**

```python
def calculate_health_score(
    compliance_rate: float,      # 0.0 - 1.0
    resolution_rate: float,      # 0.0 - 1.0
    first_stage_rate: float,     # 0.0 - 1.0
    exception_rate: float        # 0.0 - 1.0
) -> float:
    """
    Calculate health score (0-100).

    Weights:
    - Compliance Rate: 40%
    - Resolution Rate: 25%
    - First-Stage Detection: 20%
    - Exception Rate: 15% (inverse)
    """
    score = (
        (compliance_rate * 40) +
        (resolution_rate * 25) +
        (first_stage_rate * 20) +
        ((1 - exception_rate) * 15)
    )
    return min(score, 100)
```

**Recording Rule:**

```yaml
groups:
  - name: constitution-health
    interval: 5m
    rules:
      - record: constitution:health_score
        expr: |
          clamp_max(
            (
              (sum(rate(constitution_law_evaluations_total{result="pass"}[24h])) /
               sum(rate(constitution_law_evaluations_total[24h]))) * 40
            ) +
            (
              clamp_max(
                sum(increase(constitution_violations_resolved_total[24h])) /
                sum(increase(constitution_violations_total[24h])),
              1) * 25
            ) +
            (
              (sum(rate(constitution_violations_total{detection_stage="pre_commit"}[24h])) /
               sum(rate(constitution_violations_total[24h]))) * 20
            ) +
            (
              (1 - clamp_max(
                sum(rate(constitution_violations_total{action="exception"}[24h])) /
                sum(rate(constitution_violations_total[24h])),
              1)) * 15
            ),
          100)
```

---

### 6. Evaluation Latency

**Metric Name:** `constitution_evaluation_duration_seconds`

**Type:** Histogram

**Description:** Time taken to evaluate constitution compliance.

**Labels:**

| Label | Description | Example Values |
|-------|-------------|----------------|
| `evaluation_point` | Where evaluation occurred | `pre_commit`, `ci_pipeline` |

**Buckets:**

```python
LATENCY_BUCKETS = [
    0.01,   # 10ms
    0.025,  # 25ms
    0.05,   # 50ms
    0.1,    # 100ms
    0.25,   # 250ms
    0.5,    # 500ms
    1.0,    # 1s
    2.5,    # 2.5s
    5.0,    # 5s
    10.0    # 10s
]
```

**Collection Code:**

```python
from prometheus_client import Histogram
import time
from contextlib import contextmanager

EVALUATION_DURATION = Histogram(
    'constitution_evaluation_duration_seconds',
    'Constitution evaluation duration',
    ['evaluation_point'],
    buckets=LATENCY_BUCKETS
)

@contextmanager
def measure_evaluation(evaluation_point: str):
    start = time.time()
    try:
        yield
    finally:
        duration = time.time() - start
        EVALUATION_DURATION.labels(evaluation_point=evaluation_point).observe(duration)

# Usage
with measure_evaluation('ci_pipeline'):
    results = run_constitution_checks()
```

---

### 7. Open Violations Gauge

**Metric Name:** `constitution_open_violations`

**Type:** Gauge

**Description:** Current number of unresolved violations.

**Labels:**

| Label | Description | Example Values |
|-------|-------------|----------------|
| `severity` | Violation severity | `critical`, `warning` |
| `project` | Project identifier | `order-service` |
| `team` | Team identifier | `checkout-team` |

**Collection Code:**

```python
from prometheus_client import Gauge

OPEN_VIOLATIONS = Gauge(
    'constitution_open_violations',
    'Current open violations',
    ['severity', 'project', 'team']
)

def update_open_violations(project: str, team: str):
    """Update gauge with current open violation counts."""
    for severity in ['critical', 'warning', 'info']:
        count = query_open_violations(project, team, severity)
        OPEN_VIOLATIONS.labels(
            severity=severity,
            project=project,
            team=team
        ).set(count)
```

---

## Enforcement Event Schema

Beyond metrics, enforcement events should be logged with full context:

```json
{
  "event_type": "constitution_enforcement",
  "event_id": "evt_abc123xyz",
  "timestamp": "2026-01-15T10:30:00.000Z",

  "law": {
    "id": "ENG-4.1",
    "title": "Atomic TDD Law",
    "domain": "ENG",
    "article": "IV",
    "section": "1",
    "is_non_negotiable": true
  },

  "violation": {
    "severity": "critical",
    "description": "Implementation code written without a failing test first",
    "file_path": "src/services/OrderService.java",
    "line_number": 47,
    "code_snippet": "public void processOrder(...) {"
  },

  "detection": {
    "stage": "pre_commit",
    "tool": "constitutional-linter",
    "tool_version": "2.1.0"
  },

  "enforcement": {
    "action": "blocked",
    "exception_reason": null,
    "exception_approver": null
  },

  "context": {
    "project": "order-service",
    "team": "checkout-team",
    "engineer": "engineer@example.com",
    "commit_sha": "abc123",
    "branch": "feature/new-checkout"
  },

  "resolution": {
    "status": "pending",
    "resolved_at": null,
    "resolved_by": null,
    "resolution_method": null
  }
}
```

---

## Collection Best Practices

### 1. Label Cardinality

Keep label cardinality manageable:

```python
# GOOD - Bounded labels
labels=['law_id', 'severity', 'evaluation_point']

# BAD - Unbounded labels
labels=['file_path', 'line_number', 'engineer_email']
```

### 2. Consistent Naming

Follow Prometheus naming conventions:

```python
# GOOD
'constitution_law_evaluations_total'     # Counter with _total suffix
'constitution_violation_resolution_seconds'  # Histogram with unit suffix

# BAD
'constitution_evaluations'               # Missing _total for counter
'constitution_resolution_time'           # Missing unit
```

### 3. Atomic Updates

Update related metrics atomically:

```python
def record_evaluation_result(evaluation: LawEvaluation):
    # Record evaluation
    LAW_EVALUATIONS.labels(...).inc()

    # If violation, also record violation
    if evaluation.result == 'fail':
        VIOLATIONS.labels(...).inc()

    # Don't split across multiple calls that could fail independently
```

### 4. Default Values

Handle missing data gracefully:

```python
def record_evaluation(law_id: str, result: str, **kwargs):
    LAW_EVALUATIONS.labels(
        law_id=law_id,
        law_domain=law_id.split('-')[0],
        result=result,
        evaluation_point=kwargs.get('evaluation_point', 'unknown'),
        project=kwargs.get('project', 'unknown'),
        team=kwargs.get('team', 'unknown')
    ).inc()
```

---

## Metric Retention

| Metric Type | Retention | Rationale |
|-------------|-----------|-----------|
| Raw counters | 15 days | High cardinality, aggregate quickly |
| Recording rules | 90 days | Pre-aggregated, lower storage |
| Health scores | 1 year | Trend analysis, compliance audits |
| Enforcement logs | 2 years | Audit trail requirements |

Configure in Prometheus:

```yaml
# prometheus.yaml
global:
  scrape_interval: 15s

storage:
  tsdb:
    retention.time: 15d

# Use remote write for long-term storage
remote_write:
  - url: "http://thanos-receive:10908/api/v1/receive"
```

---

## Related Guides

- [Constitution Observability Implementation](./constitution-observability-implementation.md) - End-to-end setup
- [Dashboard Reporting Guide](./dashboard-reporting-guide.md) - Dashboard templates
