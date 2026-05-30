---
skill:
  id: skill-13-observability
  name: Observability
  category: operations
  version: "2.0.0"

laws:
  implements:
    - id: ENG-5.5
      title: Observability Law
    - id: ENG-6.7
      title: Audit Trail Law (NON-NEGOTIABLE)
    - id: BUS-7.1
      title: Audit Trail Law (NON-NEGOTIABLE)
  references:
    - id: BUS-9.1
      title: Incident Classification Law

triggers:
  phrases:
    - "Add logging"
    - "Set up metrics"
    - "Distributed tracing"
    - "Monitor this service"

followed_by:
  - skill-11-incident-response
  - skill-27-constitution-compliance
---

# Skill: Observability

> **Purpose:** Build systems that reveal their internal state through logs, metrics, and traces, enabling rapid debugging and proactive monitoring.

---

## Purpose

Observability is the practice of instrumenting systems so their internal state can be understood from external outputs. This skill ensures:

1. **Visibility** - Know what's happening inside production systems
2. **Debuggability** - Find root causes quickly when things go wrong
3. **Proactive detection** - Catch issues before users report them
4. **Performance insight** - Understand system behavior under load
5. **Business intelligence** - Connect technical metrics to business outcomes

**Key principle:** You can't fix what you can't see. Observability is not optional.

**The Three Pillars:**
- **Logs** - Discrete events that happened
- **Metrics** - Numeric measurements over time
- **Traces** - Request flow across services

---

## When to Invoke

Invoke this skill when:

- Designing new services or features
- Debugging production issues
- Setting up monitoring and alerting
- Improving system visibility
- Establishing SLOs and SLIs
- Preparing for production readiness review

**Trigger phrases:**
- "How do we monitor this?"
- "What metrics should we track?"
- "We need better logging"
- "Set up alerting for this service"
- "I can't tell what's happening in production"

---

## Constitutional Foundation

### Engineering Constitution
- **Article VI, Section 6.1** - Observability: Systems must expose internal state
- **Article VI, Section 6.2** - Reliability: Defined SLOs with measurement
- **Article IV, Section 4.1** - Test-First: Observability tested before deploy

### Product Constitution
- **Article VI, Section 6.1** - User Experience: Detect degradation before users

### Business Constitution
- **Article IV, Section 4.1** - Continuity: Business metrics visible
- **Article III, Section 3.3** - Audit Trail: Actions are traceable

---

## The Three Pillars

### Pillar 1: Logging

**What to log:**

| Level | When to Use | Examples |
|-------|-------------|----------|
| **ERROR** | Something failed, needs attention | Exceptions, failed operations |
| **WARN** | Potential issue, degraded state | Retry succeeded, fallback used |
| **INFO** | Significant business events | User actions, state changes |
| **DEBUG** | Detailed diagnostic info | Variable values, flow decisions |

**Structured Logging:**

```python
import structlog

logger = structlog.get_logger()

# BAD - Unstructured
logger.info(f"User {user_id} placed order {order_id} for ${total}")

# GOOD - Structured
logger.info("order_placed",
    user_id=user_id,
    order_id=order_id,
    total=total,
    item_count=len(items),
    payment_method=payment_method
)
```

**Output (JSON):**
```json
{
  "timestamp": "2024-01-15T10:30:00.000Z",
  "level": "info",
  "event": "order_placed",
  "user_id": "usr_123",
  "order_id": "ord_456",
  "total": 99.99,
  "item_count": 3,
  "payment_method": "card",
  "service": "order-service",
  "environment": "production",
  "trace_id": "abc123"
}
```

**Logging Best Practices:**
- Use structured logging (JSON)
- Include correlation IDs (trace_id, request_id)
- Log at service boundaries
- Don't log sensitive data (passwords, tokens, PII)
- Include context (user_id, tenant_id, etc.)

---

### Pillar 2: Metrics

**The Four Golden Signals:**

| Signal | What it Measures | Example Metrics |
|--------|------------------|-----------------|
| **Latency** | Time to serve requests | p50, p95, p99 response time |
| **Traffic** | Demand on system | Requests per second |
| **Errors** | Rate of failures | Error rate, error count by type |
| **Saturation** | How "full" the system is | CPU %, memory %, queue depth |

**Metric Types:**

```python
from prometheus_client import Counter, Histogram, Gauge

# Counter - Only goes up
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

# Histogram - Distribution of values
http_request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint'],
    buckets=[.005, .01, .025, .05, .1, .25, .5, 1, 2.5, 5, 10]
)

# Gauge - Goes up and down
active_connections = Gauge(
    'active_connections',
    'Number of active connections'
)
```

**Using Metrics:**

```python
@app.middleware("http")
async def metrics_middleware(request, call_next):
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time

    http_requests_total.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()

    http_request_duration.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)

    return response
```

**Key Metrics to Track:**

```yaml
# Application Metrics
- http_requests_total
- http_request_duration_seconds
- http_request_size_bytes
- http_response_size_bytes

# Business Metrics
- orders_created_total
- payments_processed_total
- user_signups_total

# Dependency Metrics
- database_query_duration_seconds
- external_api_request_duration_seconds
- cache_hit_ratio

# Resource Metrics
- process_cpu_seconds_total
- process_memory_bytes
- database_connections_active
```

---

### Pillar 3: Distributed Tracing

**What is a Trace:**

```
Trace: Complete request journey
├── Span: API Gateway (50ms)
│   ├── Span: Auth Service (10ms)
│   └── Span: Order Service (35ms)
│       ├── Span: Database Query (5ms)
│       ├── Span: Inventory Check (15ms)
│       └── Span: Payment Service (10ms)
```

**Implementing Tracing:**

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Setup
provider = TracerProvider()
provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)

# Usage
async def create_order(order_request):
    with tracer.start_as_current_span("create_order") as span:
        span.set_attribute("user_id", order_request.user_id)
        span.set_attribute("item_count", len(order_request.items))

        # Child span for database
        with tracer.start_as_current_span("save_to_database"):
            order = await db.save(order_request)

        # Child span for external call
        with tracer.start_as_current_span("process_payment"):
            payment = await payment_service.charge(order)

        span.set_attribute("order_id", order.id)
        return order
```

**Trace Context Propagation:**

```python
# Inject trace context into outgoing requests
from opentelemetry.propagate import inject

headers = {}
inject(headers)
response = await http_client.post(url, headers=headers)

# Extract trace context from incoming requests
from opentelemetry.propagate import extract

context = extract(request.headers)
with tracer.start_as_current_span("handle_request", context=context):
    ...
```

---

## Alerting

### Alert Design Principles

**Alert on symptoms, not causes:**
```yaml
# BAD - Cause-based
- alert: HighCPU
  expr: cpu_usage > 80%
  # CPU might be high but system is fine

# GOOD - Symptom-based
- alert: HighLatency
  expr: http_request_duration_seconds:p99 > 1
  # Users are experiencing slow responses
```

**Alert Severity Levels:**

| Severity | Response | Examples |
|----------|----------|----------|
| **Critical** | Page immediately | Service down, data loss |
| **Warning** | Investigate soon | Degraded performance |
| **Info** | Review in morning | Capacity trending |

**Alert Template:**

```yaml
groups:
  - name: order-service
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m]))
          /
          sum(rate(http_requests_total[5m]))
          > 0.05
        for: 5m
        labels:
          severity: critical
          service: order-service
        annotations:
          summary: "High error rate in order-service"
          description: "Error rate is {{ $value | humanizePercentage }} (threshold: 5%)"
          runbook: "https://wiki/runbooks/order-service-errors"

      - alert: HighLatency
        expr: |
          histogram_quantile(0.99,
            rate(http_request_duration_seconds_bucket[5m])
          ) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High p99 latency in order-service"
          description: "p99 latency is {{ $value | humanizeDuration }}"
```

---

## SLOs and SLIs

### Definitions

| Term | Meaning | Example |
|------|---------|---------|
| **SLI** | Service Level Indicator - what we measure | 99th percentile latency |
| **SLO** | Service Level Objective - target we aim for | p99 latency < 500ms |
| **SLA** | Service Level Agreement - contractual commitment | 99.9% uptime or credits |
| **Error Budget** | Allowed failures before violating SLO | 0.1% of requests can fail |

### Defining SLOs

```yaml
# Order Service SLOs

availability:
  sli: successful_requests / total_requests
  slo: 99.9%
  window: 30 days
  error_budget: 43.2 minutes/month

latency:
  sli: requests_under_500ms / total_requests
  slo: 99%
  window: 30 days

error_rate:
  sli: non_error_requests / total_requests
  slo: 99.5%
  window: 30 days
```

### Error Budget Policy

```markdown
## Error Budget Policy

### When budget is healthy (> 50% remaining)
- Normal development velocity
- Experiment with new features
- Take calculated risks

### When budget is concerning (25-50% remaining)
- Increase review rigor
- Prioritize reliability work
- Limit risky deployments

### When budget is critical (< 25% remaining)
- Freeze non-critical deployments
- Focus on reliability fixes only
- Incident review for all issues

### When budget is exhausted (0%)
- Stop all feature deployments
- All hands on reliability
- Post-mortem required before resuming
```

---

## Dashboards

### Dashboard Hierarchy

```
Level 1: Business Dashboard
├── Revenue metrics
├── User activity
└── Conversion rates

Level 2: Service Dashboard
├── Golden signals per service
├── Dependencies health
└── Resource utilization

Level 3: Debug Dashboard
├── Detailed metrics
├── Log aggregation
└── Trace analysis
```

### Service Dashboard Template

```
┌─────────────────────────────────────────────────────────────┐
│                     ORDER SERVICE                            │
├─────────────────────────────────────────────────────────────┤
│  Request Rate          Error Rate           Latency (p99)   │
│  ████████ 150/s       ██ 0.5%              ████ 120ms       │
├─────────────────────────────────────────────────────────────┤
│  [Request Rate Graph - 24h]                                 │
│  ▁▂▃▄▅▆▇█▇▆▅▄▃▂▁▂▃▄▅▆▇█▇▆▅▄▃▂▁                           │
├─────────────────────────────────────────────────────────────┤
│  [Latency Heatmap - 24h]                                    │
│  p99: ████████████░░░░░░░░                                 │
│  p95: ██████████░░░░░░░░░░                                 │
│  p50: █████░░░░░░░░░░░░░░░                                 │
├─────────────────────────────────────────────────────────────┤
│  Dependencies          Status                               │
│  ├── Database          ● Healthy                           │
│  ├── Payment Service   ● Healthy                           │
│  ├── Inventory API     ◐ Degraded                          │
│  └── Cache             ● Healthy                           │
└─────────────────────────────────────────────────────────────┘
```

---

## Good Examples

### Example 1: Well-Instrumented Service

```python
# Comprehensive observability setup

import structlog
from prometheus_client import Counter, Histogram
from opentelemetry import trace

logger = structlog.get_logger()
tracer = trace.get_tracer(__name__)

orders_created = Counter('orders_created_total', 'Orders created', ['status'])
order_value = Histogram('order_value_dollars', 'Order value distribution')
order_processing_time = Histogram('order_processing_seconds', 'Order processing time')

async def create_order(request: CreateOrderRequest) -> Order:
    with tracer.start_as_current_span("create_order") as span:
        span.set_attribute("user_id", request.user_id)
        start_time = time.time()

        try:
            # Process order
            order = await process_order(request)

            # Record success metrics
            orders_created.labels(status="success").inc()
            order_value.observe(order.total)
            order_processing_time.observe(time.time() - start_time)

            # Log success
            logger.info("order_created",
                order_id=order.id,
                user_id=request.user_id,
                total=order.total,
                item_count=len(request.items),
                processing_time_ms=(time.time() - start_time) * 1000
            )

            span.set_attribute("order_id", order.id)
            span.set_attribute("order_total", order.total)

            return order

        except PaymentError as e:
            orders_created.labels(status="payment_failed").inc()
            logger.warning("order_payment_failed",
                user_id=request.user_id,
                error=str(e)
            )
            span.record_exception(e)
            raise

        except Exception as e:
            orders_created.labels(status="error").inc()
            logger.error("order_creation_failed",
                user_id=request.user_id,
                error=str(e),
                exc_info=True
            )
            span.record_exception(e)
            raise
```

---

## Bad Examples (Anti-Patterns)

### Anti-Pattern 1: Log and Hope

```python
# BAD - Useless logging

def process_order(order):
    print("Processing order...")  # No structure, no context
    try:
        result = do_something()
        print("Done!")  # What was done?
    except Exception as e:
        print(f"Error: {e}")  # No context, no trace
```

**Correct approach:** Structured logging with context.

---

### Anti-Pattern 2: Alert Fatigue

```yaml
# BAD - Too many noisy alerts

- alert: CPUAbove50
  expr: cpu > 50  # Fires constantly

- alert: AnyError
  expr: errors > 0  # Fires on every error

# Result: Team ignores all alerts
```

**Correct approach:** Alert on symptoms, appropriate thresholds, actionable alerts only.

---

### Anti-Pattern 3: No Correlation

```python
# BAD - Logs without trace context

logger.info("User logged in")  # Which user? Which request?
logger.info("Order created")   # Same request? Different?
logger.info("Payment processed")  # Can't connect the dots
```

**Correct approach:** Include trace_id/request_id in all logs.

---

## Quality Checklist

Before considering observability complete:

### Logging
- [ ] Structured logging implemented
- [ ] Correlation IDs propagated
- [ ] Appropriate log levels used
- [ ] Sensitive data excluded
- [ ] Logs queryable and indexed

### Metrics
- [ ] Four golden signals covered
- [ ] Business metrics defined
- [ ] Dependency health tracked
- [ ] Histograms for latencies
- [ ] Dashboards created

### Tracing
- [ ] Trace context propagated
- [ ] Key spans instrumented
- [ ] Span attributes meaningful
- [ ] Traces exported to backend

### Alerting
- [ ] SLOs defined
- [ ] Alerts symptom-based
- [ ] Runbooks linked
- [ ] Escalation path clear
- [ ] Error budget tracked

---

## Skill Interactions

### Preceded By
- **12-API Design** - APIs designed with observability in mind

### Followed By
- **11-Incident Response** - Observability enables faster response

### Related Skills
- **10-Security Review** - Security event logging
- **14-Technical Debt** - Observability gaps as debt
