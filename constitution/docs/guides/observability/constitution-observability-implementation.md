# Constitution Observability Implementation Guide

**End-to-End Setup Guide for DevOps and Tech Leads**

---

## Overview

This guide provides step-by-step instructions for implementing constitution observability in your organization. By the end of this guide, you will have:

- Metrics collection at all evaluation points
- Enforcement event logging
- Real-time health dashboards
- Automated compliance reporting
- Alerting for compliance degradation

**Time to Complete:** 2-4 hours (depending on existing infrastructure)

**Prerequisites:**
- Observability platform (Prometheus/Grafana, Datadog, or equivalent)
- CI/CD pipeline (GitHub Actions, GitLab CI, Jenkins, etc.)
- Access to create dashboards and alert rules

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Constitution Observability Stack                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Evaluation Points                 Collection Layer                   │
│  ┌─────────────┐                  ┌────────────────┐                │
│  │  Pre-commit │──────────────────│   Metrics      │                │
│  │   Hooks     │                  │   Exporter     │                │
│  └─────────────┘                  └───────┬────────┘                │
│                                           │                          │
│  ┌─────────────┐                  ┌───────▼────────┐                │
│  │  CI/CD      │──────────────────│   Push         │                │
│  │  Pipeline   │                  │   Gateway      │                │
│  └─────────────┘                  └───────┬────────┘                │
│                                           │                          │
│  ┌─────────────┐                  ┌───────▼────────┐                │
│  │  AI Agent   │──────────────────│   Prometheus   │                │
│  │  Sessions   │                  │   (or equiv)   │                │
│  └─────────────┘                  └───────┬────────┘                │
│                                           │                          │
│  ┌─────────────┐                  ┌───────▼────────┐   ┌──────────┐│
│  │  Code       │──────────────────│   Grafana      │───│  Alerts  ││
│  │  Reviews    │                  │   Dashboards   │   │          ││
│  └─────────────┘                  └───────┬────────┘   └──────────┘│
│                                           │                          │
│                                   ┌───────▼────────┐                │
│                                   │   Reports      │                │
│                                   │   Generator    │                │
│                                   └────────────────┘                │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Step 1: Install Constitution Metrics Library

### Python Projects

```bash
pip install constitution-metrics
```

```python
# constitution_setup.py
from constitution_metrics import ConstitutionCollector, setup_exporter

# Initialize collector
collector = ConstitutionCollector(
    project="order-service",
    team="checkout-team"
)

# Start metrics exporter (for long-running services)
setup_exporter(port=9090)
```

### Node.js Projects

```bash
npm install @constitution/metrics
```

```javascript
// constitution-setup.js
const { ConstitutionCollector, setupExporter } = require('@constitution/metrics');

const collector = new ConstitutionCollector({
  project: 'order-service',
  team: 'checkout-team'
});

setupExporter({ port: 9090 });
```

### For CI/CD (Stateless)

Use the push gateway approach:

```python
# ci_metrics.py
from constitution_metrics import ConstitutionCollector

collector = ConstitutionCollector(
    project="order-service",
    team="checkout-team",
    push_gateway="http://pushgateway:9091"
)

# Metrics will be pushed to gateway on each evaluation
```

---

## Step 2: Instrument Evaluation Points

### Pre-commit Hook

Create a pre-commit hook that evaluates constitution laws:

```bash
# .git/hooks/pre-commit (or use pre-commit framework)
#!/bin/bash

# Run constitution linter
constitution-lint --staged --format json > /tmp/constitution-results.json

# Push metrics
python -c "
from constitution_metrics import ConstitutionCollector
import json

with open('/tmp/constitution-results.json') as f:
    results = json.load(f)

collector = ConstitutionCollector(
    project='$PROJECT_NAME',
    team='$TEAM_NAME',
    push_gateway='$PUSH_GATEWAY_URL'
)

for result in results['evaluations']:
    collector.record_evaluation(
        law_id=result['law_id'],
        result=result['result'],
        evaluation_point='pre_commit'
    )
"

# Block commit on critical violations
if grep -q '"severity": "critical"' /tmp/constitution-results.json; then
    echo "Critical constitution violations detected. Commit blocked."
    exit 1
fi
```

### CI/CD Pipeline (GitHub Actions)

```yaml
# .github/workflows/constitution-check.yml
name: Constitution Compliance

on:
  pull_request:
    branches: [main, develop]

jobs:
  constitution-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install constitution-lint constitution-metrics

      - name: Run Constitution Check
        env:
          PUSH_GATEWAY: ${{ secrets.METRICS_PUSH_GATEWAY }}
          PROJECT: ${{ github.repository }}
          TEAM: ${{ github.repository_owner }}
        run: |
          # Run linter
          constitution-lint . --format json > results.json

          # Push metrics
          python scripts/push_ci_metrics.py \
            --results results.json \
            --gateway $PUSH_GATEWAY \
            --project $PROJECT \
            --team $TEAM \
            --evaluation-point ci_pipeline

      - name: Check for Critical Violations
        run: |
          if jq -e '.evaluations[] | select(.result == "fail" and .severity == "critical")' results.json > /dev/null; then
            echo "::error::Critical constitution violations found"
            jq '.evaluations[] | select(.result == "fail")' results.json
            exit 1
          fi

      - name: Upload Results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: constitution-results
          path: results.json
```

### AI Agent Integration

For AI coding assistants (GitHub Copilot, Claude, etc.):

```python
# agent_constitution_middleware.py
from constitution_metrics import ConstitutionCollector, EnforcementLogger

logger = EnforcementLogger()
collector = ConstitutionCollector(
    project=os.environ.get('PROJECT'),
    team=os.environ.get('TEAM')
)

def evaluate_agent_output(code_change: str, context: dict) -> EvaluationResult:
    """Evaluate AI-generated code for constitution compliance."""
    evaluations = run_constitution_checks(code_change)

    for eval in evaluations:
        # Record metric
        collector.record_evaluation(
            law_id=eval.law_id,
            result=eval.result,
            evaluation_point='ai_agent'
        )

        # Log enforcement event if violation
        if eval.result == 'fail':
            logger.log_enforcement(
                law_id=eval.law_id,
                law_title=eval.law_title,
                action='warned',
                description=eval.description,
                severity=eval.severity,
                detection_stage='ai_agent'
            )

    return EvaluationResult(
        passed=all(e.result == 'pass' for e in evaluations),
        evaluations=evaluations
    )
```

---

## Step 3: Configure Enforcement Logging

Set up structured logging for all enforcement events:

```python
# enforcement_logging.py
import structlog
from datetime import datetime

# Configure structlog for JSON output
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
)

logger = structlog.get_logger("constitution.enforcement")

class EnforcementLogger:
    def __init__(self, project: str, team: str):
        self.project = project
        self.team = team

    def log_violation(
        self,
        law_id: str,
        law_title: str,
        description: str,
        severity: str,
        detection_stage: str,
        action: str,
        file_path: str = None,
        line_number: int = None,
        exception_reason: str = None
    ):
        logger.info(
            "constitution_enforcement",
            event_type="violation",
            law_id=law_id,
            law_title=law_title,
            violation_description=description,
            severity=severity,
            detection_stage=detection_stage,
            action=action,
            file_path=file_path,
            line_number=line_number,
            exception_reason=exception_reason,
            project=self.project,
            team=self.team
        )

    def log_resolution(
        self,
        violation_id: str,
        law_id: str,
        resolution_method: str,
        resolved_by: str
    ):
        logger.info(
            "constitution_enforcement",
            event_type="resolution",
            violation_id=violation_id,
            law_id=law_id,
            resolution_method=resolution_method,
            resolved_by=resolved_by,
            project=self.project,
            team=self.team
        )
```

### Log Aggregation Configuration

For Elasticsearch/Kibana:

```yaml
# filebeat.yml
filebeat.inputs:
  - type: container
    paths:
      - '/var/lib/docker/containers/*/*.log'
    processors:
      - decode_json_fields:
          fields: ["message"]
          target: ""
          overwrite_keys: true

output.elasticsearch:
  hosts: ["elasticsearch:9200"]
  indices:
    - index: "constitution-enforcement-%{+yyyy.MM.dd}"
      when.contains:
        event: "constitution_enforcement"
```

---

## Step 4: Set Up Dashboards

### Prometheus Recording Rules

Create recording rules for efficient dashboard queries:

```yaml
# prometheus-rules.yaml
groups:
  - name: constitution-compliance
    interval: 1m
    rules:
      # Compliance rate (5m window)
      - record: constitution:compliance_rate:5m
        expr: |
          sum(rate(constitution_law_evaluations_total{result="pass"}[5m]))
          /
          sum(rate(constitution_law_evaluations_total[5m]))

      # Compliance rate by domain (5m window)
      - record: constitution:compliance_rate_by_domain:5m
        expr: |
          sum by (law_domain) (rate(constitution_law_evaluations_total{result="pass"}[5m]))
          /
          sum by (law_domain) (rate(constitution_law_evaluations_total[5m]))

      # Violation rate (5m window)
      - record: constitution:violation_rate:5m
        expr: sum(rate(constitution_violations_total[5m]))

      # Health score (calculated)
      - record: constitution:health_score
        expr: |
          clamp_max(
            (constitution:compliance_rate:5m * 40) +
            (clamp_max(sum(rate(constitution_violations_resolved_total[24h])) / sum(rate(constitution_violations_total[24h])), 1) * 25) +
            (sum(rate(constitution_violations_total{detection_stage="pre_commit"}[24h])) / sum(rate(constitution_violations_total[24h])) * 20) +
            ((1 - clamp_max(sum(rate(constitution_violations_total{action="exception"}[24h])) / sum(rate(constitution_violations_total[24h])), 1)) * 15)
          , 100)
```

### Grafana Dashboard JSON

Import this dashboard into Grafana:

```json
{
  "dashboard": {
    "id": null,
    "uid": "constitution-health",
    "title": "Constitution Health Dashboard",
    "tags": ["constitution", "compliance", "governance"],
    "timezone": "browser",
    "refresh": "1m",
    "panels": [
      {
        "id": 1,
        "title": "Overall Health Score",
        "type": "gauge",
        "gridPos": {"h": 8, "w": 6, "x": 0, "y": 0},
        "targets": [{
          "expr": "constitution:health_score",
          "refId": "A"
        }],
        "fieldConfig": {
          "defaults": {
            "min": 0,
            "max": 100,
            "thresholds": {
              "mode": "absolute",
              "steps": [
                {"value": null, "color": "red"},
                {"value": 60, "color": "orange"},
                {"value": 80, "color": "yellow"},
                {"value": 90, "color": "green"}
              ]
            }
          }
        }
      },
      {
        "id": 2,
        "title": "Compliance by Domain",
        "type": "stat",
        "gridPos": {"h": 8, "w": 6, "x": 6, "y": 0},
        "targets": [{
          "expr": "constitution:compliance_rate_by_domain:5m * 100",
          "legendFormat": "{{law_domain}}",
          "refId": "A"
        }],
        "fieldConfig": {
          "defaults": {
            "unit": "percent"
          }
        }
      },
      {
        "id": 3,
        "title": "Compliance Trend (7 days)",
        "type": "timeseries",
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0},
        "targets": [{
          "expr": "constitution:compliance_rate:5m * 100",
          "legendFormat": "Compliance Rate",
          "refId": "A"
        }]
      },
      {
        "id": 4,
        "title": "Top Violated Laws",
        "type": "table",
        "gridPos": {"h": 10, "w": 12, "x": 0, "y": 8},
        "targets": [{
          "expr": "topk(10, sum by (law_id) (increase(constitution_violations_total[7d])))",
          "format": "table",
          "refId": "A"
        }]
      },
      {
        "id": 5,
        "title": "Violations by Severity",
        "type": "piechart",
        "gridPos": {"h": 10, "w": 6, "x": 12, "y": 8},
        "targets": [{
          "expr": "sum by (severity) (constitution_violations_total)",
          "legendFormat": "{{severity}}",
          "refId": "A"
        }]
      },
      {
        "id": 6,
        "title": "Detection Stage Distribution",
        "type": "piechart",
        "gridPos": {"h": 10, "w": 6, "x": 18, "y": 8},
        "targets": [{
          "expr": "sum by (detection_stage) (increase(constitution_violations_total[7d]))",
          "legendFormat": "{{detection_stage}}",
          "refId": "A"
        }]
      }
    ]
  }
}
```

---

## Step 5: Configure Alerting

### Prometheus Alert Rules

```yaml
# alerting-rules.yaml
groups:
  - name: constitution-alerts
    rules:
      - alert: ConstitutionHealthCritical
        expr: constitution:health_score < 70
        for: 30m
        labels:
          severity: critical
        annotations:
          summary: "Constitution health critically low ({{ $value | printf \"%.1f\" }})"
          description: "The organization's constitution health score has dropped below 70."
          runbook_url: "https://wiki/runbooks/constitution-health"

      - alert: ConstitutionHealthWarning
        expr: constitution:health_score >= 70 and constitution:health_score < 85
        for: 1h
        labels:
          severity: warning
        annotations:
          summary: "Constitution health needs attention ({{ $value | printf \"%.1f\" }})"

      - alert: HighViolationRate
        expr: constitution:violation_rate:5m > 0.1
        for: 15m
        labels:
          severity: warning
        annotations:
          summary: "High constitution violation rate"
          description: "Violation rate is {{ $value | printf \"%.3f\" }} per second"

      - alert: CriticalViolationUnresolved
        expr: |
          sum(constitution_violations_total{severity="critical"})
          - sum(constitution_violations_resolved_total{severity="critical"})
          > 3
        for: 2h
        labels:
          severity: critical
        annotations:
          summary: "Unresolved critical violations"
          description: "{{ $value }} critical violations remain unresolved for over 2 hours"
```

### Alertmanager Configuration

```yaml
# alertmanager.yaml
global:
  resolve_timeout: 5m

route:
  receiver: 'default'
  group_by: ['alertname', 'severity']
  routes:
    - match:
        severity: critical
      receiver: 'constitution-critical'
    - match:
        severity: warning
      receiver: 'constitution-warning'

receivers:
  - name: 'default'
    slack_configs:
      - api_url: 'https://hooks.slack.com/services/xxx'
        channel: '#engineering'

  - name: 'constitution-critical'
    slack_configs:
      - api_url: 'https://hooks.slack.com/services/xxx'
        channel: '#constitution-critical'
    pagerduty_configs:
      - service_key: 'your-pagerduty-key'

  - name: 'constitution-warning'
    slack_configs:
      - api_url: 'https://hooks.slack.com/services/xxx'
        channel: '#constitution-alerts'
```

---

## Step 6: Set Up Reporting

### Weekly Report Generator

```python
# reports/weekly.py
from datetime import date, timedelta
from dataclasses import dataclass
from typing import List
import requests

@dataclass
class WeeklyReport:
    period: str
    overall_compliance: float
    compliance_delta: float
    total_evaluations: int
    total_violations: int
    resolved: int
    open: int
    top_violated: List[dict]
    recommendations: List[str]

def generate_weekly_report() -> WeeklyReport:
    end = date.today()
    start = end - timedelta(days=7)

    # Query Prometheus
    compliance = query_prometheus(
        'avg_over_time(constitution:compliance_rate:5m[7d])'
    )
    prev_compliance = query_prometheus(
        'avg_over_time(constitution:compliance_rate:5m[7d] offset 7d)'
    )

    violations = query_prometheus(
        'sum(increase(constitution_violations_total[7d]))'
    )

    top_violated = query_prometheus(
        'topk(5, sum by (law_id) (increase(constitution_violations_total[7d])))'
    )

    return WeeklyReport(
        period=f"{start} to {end}",
        overall_compliance=compliance * 100,
        compliance_delta=(compliance - prev_compliance) * 100,
        total_evaluations=query_prometheus('sum(increase(constitution_law_evaluations_total[7d]))'),
        total_violations=violations,
        resolved=query_prometheus('sum(increase(constitution_violations_resolved_total[7d]))'),
        open=violations - query_prometheus('sum(increase(constitution_violations_resolved_total[7d]))'),
        top_violated=top_violated,
        recommendations=generate_recommendations()
    )

def send_report(report: WeeklyReport):
    # Send to Slack
    slack_message = format_slack(report)
    requests.post(SLACK_WEBHOOK, json=slack_message)

    # Send email
    email_body = format_email(report)
    send_email(RECIPIENTS, "Weekly Constitution Report", email_body)
```

### Cron Schedule

```yaml
# kubernetes CronJob
apiVersion: batch/v1
kind: CronJob
metadata:
  name: constitution-weekly-report
spec:
  schedule: "0 9 * * 1"  # Monday 9 AM
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: reporter
            image: constitution-reports:latest
            command: ["python", "-m", "reports.weekly"]
            env:
            - name: PROMETHEUS_URL
              value: "http://prometheus:9090"
            - name: SLACK_WEBHOOK
              valueFrom:
                secretKeyRef:
                  name: reporting
                  key: slack-webhook
```

---

## Verification Checklist

After completing this guide, verify:

- [ ] Metrics are being collected from all evaluation points
- [ ] `constitution_law_evaluations_total` counter is incrementing
- [ ] `constitution_violations_total` counter tracks violations
- [ ] Enforcement events appear in logs with full context
- [ ] Health score is calculating correctly (check with manual calculation)
- [ ] Dashboard loads and displays real data
- [ ] Test alert fires when threshold is breached
- [ ] Weekly report generates and delivers successfully

---

## Troubleshooting

### Metrics Not Appearing

1. Check push gateway connectivity: `curl -X GET http://pushgateway:9091/metrics`
2. Verify scrape config in Prometheus: `curl http://prometheus:9090/api/v1/targets`
3. Check for errors in collector logs

### Health Score Incorrect

1. Verify all component metrics exist
2. Check recording rules are evaluating: `curl http://prometheus:9090/api/v1/rules`
3. Manual calculation check against dashboard

### Alerts Not Firing

1. Verify alert rules are loaded: `curl http://prometheus:9090/api/v1/rules`
2. Check Alertmanager is receiving: `curl http://alertmanager:9093/api/v2/alerts`
3. Test with manual alert push

---

## Next Steps

1. **Train teams** on interpreting dashboards
2. **Iterate on thresholds** based on baseline data
3. **Add project-specific dashboards** for drill-down
4. **Implement ENG-10.5** for law effectiveness measurement
5. **Review monthly** and adjust as needed

---

## Related Guides

- [Metrics Collection Guide](./metrics-collection-guide.md) - Detailed metrics definitions
- [Dashboard Reporting Guide](./dashboard-reporting-guide.md) - Dashboard templates for leadership
- [Observability Skill](../../../agent-skills/skills-by-domain/platform-engineering/13-observability.md)
