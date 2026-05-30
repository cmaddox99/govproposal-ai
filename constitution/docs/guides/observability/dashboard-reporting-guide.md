# Dashboard and Reporting Guide

**Dashboard Templates and Reporting for Leadership**

---

## Overview

This guide provides dashboard templates, report formats, and best practices for communicating constitution compliance to leadership. It includes ready-to-use Grafana dashboard JSON, report templates, and guidance on interpreting metrics.

**Audience:** Tech Leads, Engineering Managers, Directors, Compliance Officers

---

## Dashboard Hierarchy

```
Executive Summary (CxO level)
├── One-number health score
├── Trend direction
└── Risk areas

Leadership Dashboard (Director/VP level)
├── Domain breakdown
├── Team comparison
├── Trend analysis
└── Action items

Team Dashboard (Manager/Lead level)
├── Team-specific metrics
├── Law-by-law status
├── Individual contributors
└── Improvement tracking

Engineer Dashboard (IC level)
├── Personal compliance
├── Recent violations
├── Learning resources
└── Resolution queue
```

---

## Executive Summary Dashboard

**Purpose:** Give executives a 30-second view of constitution health.

**Key Metrics:**

| Metric | Target | Why It Matters |
|--------|--------|----------------|
| Health Score | > 90 | Overall governance effectiveness |
| Trend | Improving | Direction matters more than absolute |
| Risk Areas | 0-2 | Focus areas requiring attention |

**Dashboard Layout:**

```
┌─────────────────────────────────────────────────────────────────┐
│           CONSTITUTION GOVERNANCE - EXECUTIVE VIEW               │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│    ┌─────────────────────────────────────────────────────────┐  │
│    │                    HEALTH SCORE                          │  │
│    │                                                           │  │
│    │                        94.2                               │  │
│    │                    ▲ +2.1% this month                     │  │
│    │                                                           │  │
│    │    [████████████████████████████████░░░░░░]              │  │
│    │                                                           │  │
│    └─────────────────────────────────────────────────────────┘  │
│                                                                   │
│    ┌───────────────────────┐  ┌───────────────────────────────┐ │
│    │   RISK AREAS          │  │   30-DAY TREND                │ │
│    │                       │  │                                │ │
│    │   ● Testing: 88%      │  │   ▁▂▃▄▅▆▇█▇▆▇█▇█▇██▇█▇█▇██   │ │
│    │   ● Security: 91%     │  │                                │ │
│    │                       │  │   Compliance improving         │ │
│    └───────────────────────┘  └───────────────────────────────┘ │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

**Grafana JSON:**

```json
{
  "dashboard": {
    "title": "Constitution Executive Summary",
    "uid": "constitution-exec",
    "tags": ["constitution", "executive"],
    "panels": [
      {
        "id": 1,
        "title": "Health Score",
        "type": "stat",
        "gridPos": {"h": 10, "w": 24, "x": 0, "y": 0},
        "targets": [{
          "expr": "constitution:health_score",
          "refId": "A"
        }],
        "fieldConfig": {
          "defaults": {
            "thresholds": {
              "steps": [
                {"value": null, "color": "red"},
                {"value": 70, "color": "orange"},
                {"value": 85, "color": "yellow"},
                {"value": 95, "color": "green"}
              ]
            },
            "mappings": [],
            "unit": "none",
            "displayName": "Constitution Health"
          }
        },
        "options": {
          "reduceOptions": {"calcs": ["lastNotNull"]},
          "textMode": "value_and_name",
          "colorMode": "value",
          "graphMode": "area",
          "justifyMode": "center"
        }
      },
      {
        "id": 2,
        "title": "Risk Areas",
        "type": "stat",
        "gridPos": {"h": 8, "w": 8, "x": 0, "y": 10},
        "targets": [{
          "expr": "count(constitution:compliance_rate_by_domain:5m < 0.90)",
          "refId": "A"
        }],
        "fieldConfig": {
          "defaults": {
            "thresholds": {
              "steps": [
                {"value": null, "color": "green"},
                {"value": 1, "color": "yellow"},
                {"value": 3, "color": "red"}
              ]
            },
            "displayName": "Domains Below 90%"
          }
        }
      },
      {
        "id": 3,
        "title": "30-Day Trend",
        "type": "timeseries",
        "gridPos": {"h": 8, "w": 16, "x": 8, "y": 10},
        "targets": [{
          "expr": "constitution:health_score",
          "legendFormat": "Health Score",
          "refId": "A"
        }],
        "fieldConfig": {
          "defaults": {
            "custom": {
              "drawStyle": "line",
              "lineWidth": 2,
              "fillOpacity": 20
            }
          }
        }
      }
    ]
  }
}
```

---

## Leadership Dashboard

**Purpose:** Enable directors and VPs to understand constitution status across their organization and identify areas needing attention.

**Key Metrics:**

| Panel | Metrics | Insight Provided |
|-------|---------|------------------|
| Domain Health | Compliance by ENG/PRD/BUS | Which constitution areas need focus |
| Team Comparison | Compliance by team | Which teams need support |
| Top Violations | Most violated laws | Training/tooling gaps |
| MTTR | Resolution time | Process efficiency |
| Trend | 30-day history | Trajectory |

**Dashboard Layout:**

```
┌─────────────────────────────────────────────────────────────────────┐
│               CONSTITUTION GOVERNANCE - LEADERSHIP VIEW              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Health: 94.2 ▲   │  ENG: 93.8%  │  PRD: 95.1%  │  BUS: 94.0%       │
│                                                                       │
├─────────────────────────────────────────────────────────────────────┤
│  TEAM STANDINGS                     │  TOP VIOLATED LAWS             │
│                                     │                                 │
│  ● auth-team         97.1%         │  1. ENG-4.1   142  ▼ -12%      │
│  ● checkout-team     96.2%         │  2. ENG-3.1    89  → +0%       │
│  ● payments-team     94.5%         │  3. PRD-3.2    67  ▲ +5%       │
│  ● search-team       91.8%         │  4. ENG-6.5    45  ▼ -8%       │
│  ◐ inventory-team    88.3%         │  5. BUS-7.1    34  → +1%       │
│  ○ legacy-team       72.4%         │                                 │
│                                     │                                 │
├─────────────────────────────────────────────────────────────────────┤
│  RESOLUTION METRICS                 │  30-DAY COMPLIANCE TREND       │
│                                     │                                 │
│  MTTR: 2.4h (target: 4h)           │  ▁▂▃▄▅▆▇█▇▆▇█▇█▇██▇█▇█▇██     │
│  Resolution Rate: 97.2%             │                                 │
│  First-Stage Detection: 82%         │  Compliance: 94.2% (+2.1%)     │
│  Exception Rate: 3.1%               │                                 │
│                                     │                                 │
└─────────────────────────────────────────────────────────────────────┘
```

**Grafana JSON:**

```json
{
  "dashboard": {
    "title": "Constitution Leadership Dashboard",
    "uid": "constitution-leadership",
    "panels": [
      {
        "id": 1,
        "title": "Overall Health",
        "type": "gauge",
        "gridPos": {"h": 6, "w": 6, "x": 0, "y": 0},
        "targets": [{
          "expr": "constitution:health_score"
        }],
        "fieldConfig": {
          "defaults": {
            "min": 0, "max": 100,
            "thresholds": {
              "steps": [
                {"value": null, "color": "red"},
                {"value": 70, "color": "orange"},
                {"value": 85, "color": "yellow"},
                {"value": 95, "color": "green"}
              ]
            }
          }
        }
      },
      {
        "id": 2,
        "title": "Compliance by Domain",
        "type": "stat",
        "gridPos": {"h": 6, "w": 18, "x": 6, "y": 0},
        "targets": [{
          "expr": "constitution:compliance_rate_by_domain:5m * 100",
          "legendFormat": "{{law_domain}}"
        }],
        "fieldConfig": {
          "defaults": {"unit": "percent"}
        }
      },
      {
        "id": 3,
        "title": "Team Standings",
        "type": "table",
        "gridPos": {"h": 12, "w": 12, "x": 0, "y": 6},
        "targets": [{
          "expr": "sum by (team) (rate(constitution_law_evaluations_total{result='pass'}[7d])) / sum by (team) (rate(constitution_law_evaluations_total[7d])) * 100",
          "format": "table"
        }],
        "transformations": [
          {"id": "organize", "options": {"renameByName": {"Value": "Compliance %"}}}
        ]
      },
      {
        "id": 4,
        "title": "Top Violated Laws",
        "type": "table",
        "gridPos": {"h": 12, "w": 12, "x": 12, "y": 6},
        "targets": [{
          "expr": "topk(10, sum by (law_id) (increase(constitution_violations_total[7d])))",
          "format": "table"
        }]
      },
      {
        "id": 5,
        "title": "Resolution Metrics",
        "type": "stat",
        "gridPos": {"h": 6, "w": 12, "x": 0, "y": 18},
        "targets": [
          {
            "expr": "histogram_quantile(0.50, sum by (le) (rate(constitution_violation_resolution_seconds_bucket[7d]))) / 3600",
            "legendFormat": "MTTR (hours)"
          },
          {
            "expr": "sum(increase(constitution_violations_resolved_total[7d])) / sum(increase(constitution_violations_total[7d])) * 100",
            "legendFormat": "Resolution Rate"
          }
        ]
      },
      {
        "id": 6,
        "title": "Compliance Trend",
        "type": "timeseries",
        "gridPos": {"h": 6, "w": 12, "x": 12, "y": 18},
        "targets": [{
          "expr": "constitution:compliance_rate:5m * 100",
          "legendFormat": "Compliance Rate"
        }]
      }
    ]
  }
}
```

---

## Team Dashboard

**Purpose:** Give team leads detailed visibility into their team's constitution compliance.

**Key Metrics:**

| Panel | Purpose |
|-------|---------|
| Team Score | Overall team health |
| Law Compliance | Status of each relevant law |
| Recent Violations | What needs immediate attention |
| Individual Performance | Who might need support |
| Resolution Queue | Open items to address |

**Dashboard Layout:**

```
┌─────────────────────────────────────────────────────────────────────┐
│          CONSTITUTION COMPLIANCE - CHECKOUT TEAM                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Team Health: 96.2%  │  Violations (7d): 23  │  Open: 2              │
│                                                                       │
├─────────────────────────────────────────────────────────────────────┤
│  LAW COMPLIANCE STATUS                                               │
│                                                                       │
│  ● ENG-4.1  Atomic TDD             98.5%  ████████████████████░     │
│  ● ENG-3.1  Complexity Limits      94.2%  ██████████████████░░░     │
│  ● ENG-6.5  Input Validation       97.8%  ███████████████████░░     │
│  ◐ ENG-2.1  DDD                    89.1%  █████████████████░░░░     │
│  ● PRD-3.2  User Research          96.0%  ███████████████████░░     │
│                                                                       │
├─────────────────────────────────────────────────────────────────────┤
│  RECENT VIOLATIONS                  │  RESOLUTION QUEUE              │
│                                     │                                 │
│  2h ago  ENG-3.1  OrderService.java │  ⚠ ENG-4.1  Missing test       │
│  4h ago  ENG-4.1  PaymentHandler.ts │  ⚠ ENG-3.1  High complexity    │
│  1d ago  PRD-3.2  checkout-flow     │                                 │
│                                     │                                 │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Report Templates

### Weekly Summary Report

**Frequency:** Every Monday, 9 AM
**Audience:** Engineering Managers, Directors

```markdown
# Constitution Compliance Weekly Summary
**Period:** January 8-15, 2026
**Generated:** January 15, 2026 9:00 AM

## Executive Summary

| Metric | This Week | Previous Week | Trend |
|--------|-----------|---------------|-------|
| Health Score | 94.2 | 92.1 | ▲ +2.1 |
| Compliance Rate | 93.8% | 91.7% | ▲ +2.1% |
| Total Evaluations | 12,547 | 11,892 | ▲ +5.5% |
| Violations | 726 | 894 | ▼ -18.8% |
| Resolution Rate | 97.2% | 95.1% | ▲ +2.1% |

**Summary:** Constitution health improved this week. Violation count decreased by 19%
while evaluation volume increased, indicating improved compliance behavior.

## Domain Breakdown

| Domain | Compliance | Trend | Top Issue |
|--------|------------|-------|-----------|
| Engineering | 93.8% | ▲ +2.5% | ENG-4.1 (TDD) |
| Product | 95.1% | ▲ +1.2% | PRD-3.2 (Research) |
| Business | 94.0% | ▲ +2.8% | BUS-7.1 (Audit) |

## Team Standings

| Rank | Team | Compliance | Trend |
|------|------|------------|-------|
| 1 | auth-team | 97.1% | → |
| 2 | checkout-team | 96.2% | ▲ |
| 3 | payments-team | 94.5% | ▲ |
| 4 | search-team | 91.8% | → |
| 5 | inventory-team | 88.3% | ▲ |
| 6 | legacy-team | 72.4% | ▼ |

**Attention Needed:** legacy-team continues to struggle with compliance.
Recommended: Schedule compliance workshop.

## Top Violated Laws

| Law | Violations | Trend | Recommended Action |
|-----|------------|-------|-------------------|
| ENG-4.1 | 142 | ▼ -12% | Continue TDD training |
| ENG-3.1 | 89 | → 0% | Add complexity pre-commit hook |
| PRD-3.2 | 67 | ▲ +5% | Review discovery process |
| ENG-6.5 | 45 | ▼ -8% | Input validation improving |
| BUS-7.1 | 34 | → +1% | Audit trail compliance stable |

## Recommendations

1. **Schedule TDD refresher** for inventory-team and legacy-team
2. **Implement complexity pre-commit hook** to catch ENG-3.1 earlier
3. **Review discovery process** with product to address PRD-3.2 uptick
4. **Celebrate** checkout-team's improvement this week

---
Generated by Constitution Observability System
```

### Monthly Governance Report

**Frequency:** First Monday of month
**Audience:** Directors, VPs, Compliance

```markdown
# Constitution Governance Monthly Report
**Period:** January 2026
**Generated:** February 1, 2026

## Executive Summary

Constitution adoption continues to strengthen. Key highlights:
- Overall health score increased from 89.5 to 94.2 (+5.2%)
- Critical violations decreased by 34%
- All teams now above 70% compliance (up from 85% of teams)

## Monthly Metrics

| Metric | Jan 2026 | Dec 2025 | YoY |
|--------|----------|----------|-----|
| Health Score | 94.2 | 89.5 | +12.1 |
| Compliance Rate | 93.8% | 88.2% | +8.4% |
| Total Evaluations | 54,892 | 48,123 | +22.5% |
| Violation Rate | 5.8% | 11.8% | -50.8% |
| MTTR | 2.4h | 4.2h | -42.9% |

## Trend Analysis

[Include 12-month trend chart]

Key observations:
- Compliance has improved every month for 6 consecutive months
- MTTR has decreased significantly since Q3 tooling improvements
- Evaluation volume growing as more projects adopt constitution

## Risk Areas

| Area | Score | Risk Level | Mitigation |
|------|-------|------------|------------|
| Legacy Systems | 72.4% | Medium | Migration roadmap in progress |
| Testing Laws | 88.3% | Low | Training scheduled for Q1 |
| Security Laws | 91.2% | Low | Automated scanning implemented |

## Recommendations for Leadership

1. **Continue investment in tooling** - Pre-commit hooks show 3x improvement in first-stage detection
2. **Legacy modernization priority** - Legacy systems account for 45% of violations
3. **Expand training program** - Teams with training show 15% higher compliance
4. **Consider compliance KPIs** - Tie team goals to constitution health

## Appendix: Full Metrics

[Detailed metrics tables...]
```

---

## Interpreting Metrics

### Health Score Interpretation

| Score | Status | Action |
|-------|--------|--------|
| 95-100 | Excellent | Maintain current practices |
| 85-94 | Good | Minor improvements needed |
| 70-84 | Needs Attention | Review and address gaps |
| 50-69 | At Risk | Immediate intervention required |
| < 50 | Critical | Executive escalation needed |

### Trend Interpretation

| Trend | Meaning | Action |
|-------|---------|--------|
| ▲ Improving | Practices are working | Reinforce positive behaviors |
| → Stable | No change | Identify improvement opportunities |
| ▼ Declining | Problems emerging | Investigate root cause |

### Common Patterns

**Pattern: High violations, low resolution rate**
- Meaning: Teams finding issues but not fixing them
- Action: Review resolution process, add support

**Pattern: Low first-stage detection**
- Meaning: Issues caught late in pipeline
- Action: Improve pre-commit hooks, training

**Pattern: High exception rate**
- Meaning: Laws may be impractical or tooling insufficient
- Action: Review law applicability, improve tooling

---

## Automating Reports

### Slack Integration

```python
# reports/slack_weekly.py
import requests
from datetime import date

def send_weekly_to_slack(report: WeeklySummaryReport):
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"Constitution Weekly Summary - {report.period_end}"
            }
        },
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*Health Score:* {report.health_score:.1f}"},
                {"type": "mrkdwn", "text": f"*Trend:* {'▲' if report.trend > 0 else '▼'} {abs(report.trend):.1f}%"},
                {"type": "mrkdwn", "text": f"*Compliance:* {report.compliance_rate:.1f}%"},
                {"type": "mrkdwn", "text": f"*Open Violations:* {report.open_violations}"}
            ]
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Top Action:* {report.recommendations[0]}"
            }
        },
        {
            "type": "actions",
            "elements": [{
                "type": "button",
                "text": {"type": "plain_text", "text": "View Dashboard"},
                "url": "https://grafana/d/constitution-leadership"
            }]
        }
    ]

    requests.post(SLACK_WEBHOOK, json={"blocks": blocks})
```

### Email Integration

```python
# reports/email_monthly.py
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def send_monthly_email(report: MonthlyReport, recipients: list):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"Constitution Monthly Report - {report.month}"
    msg['From'] = "constitution-reports@example.com"
    msg['To'] = ", ".join(recipients)

    html = render_template('monthly_report.html', report=report)
    msg.attach(MIMEText(html, 'html'))

    with smtplib.SMTP(SMTP_SERVER) as server:
        server.send_message(msg)
```

---

## Best Practices

### For Dashboard Design

1. **Lead with the most important metric** - Health score should be prominent
2. **Show trends, not just values** - Direction matters more than absolute
3. **Enable drill-down** - Start high-level, allow exploration
4. **Use consistent colors** - Green = good, yellow = warning, red = critical
5. **Limit cognitive load** - 5-7 metrics per dashboard level

### For Reporting

1. **Start with summary** - Executives read first paragraph only
2. **Include recommendations** - Data without action is useless
3. **Compare to baseline** - Show progress over time
4. **Highlight outliers** - What needs attention?
5. **Be consistent** - Same format every time

### For Communication

1. **Celebrate improvements** - Positive reinforcement works
2. **Avoid blame** - Focus on process, not people
3. **Provide context** - Why does this metric matter?
4. **Be actionable** - What should change?
5. **Follow up** - Track if recommendations are implemented

---

## Related Guides

- [Constitution Observability Implementation](./constitution-observability-implementation.md) - Technical setup
- [Metrics Collection Guide](./metrics-collection-guide.md) - Detailed metrics definitions
