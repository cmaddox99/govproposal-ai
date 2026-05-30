# OpenTelemetry Python Guidance

> **Purpose:** Stack-specific patterns for Python services using OpenTelemetry (OTEL) for distributed tracing, structured logging correlation, and OTLP export to Dynatrace or other collectors. Covers auto-instrumentation bootstrapping, manual spans, structlog correlation, and test patterns.

---

## Overview

OpenTelemetry Python provides two instrumentation modes that are used together:

| Mode | When to Use | How |
|------|------------|-----|
| **Auto-instrumentation** | FastAPI routes, httpx, logging — boilerplate spans | `opentelemetry-instrument uvicorn app.main:app` |
| **Manual spans** | Critical business operations needing named spans and attributes | `tracer.start_as_current_span("llm.generate")` |

**In `cr-genai-draft-response`**, the OTEL distro handles FastAPI request spans and logging injection automatically. Manual spans are recommended for: PII redaction, LLM call, compensation validation, and audit trace write.

---

## Bootstrapping with `opentelemetry-distro`

> **Per `ENG-1.2` (AI-Engineer Pairing):** All instrumentation decisions must be explainable. Never silently remove instrumentation — it breaks the observability audit trail required by `BUS-7.1`.

### Step 1: Install instrumentation packages

```bash
opentelemetry-bootstrap -a install
# Detects installed libraries (FastAPI, httpx, logging) and installs matching instrumentors
```

### Step 2: Configure OTEL in `app/core/otel_logger.py`

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
import structlog
import os

def configure_logger():
    """Configure OTEL TracerProvider and structlog correlation."""
    # Per BUS-7.1: OTLP export ensures every span is observable in Dynatrace
    exporter = OTLPSpanExporter(
        endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317"),
    )
    provider = TracerProvider()
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)

    # Auto-instrument logging: injects trace_id and span_id into every log record
    LoggingInstrumentor().instrument(set_logging_format=True)
```

### Step 3: Run with auto-instrumentation (production)

```bash
# Wraps uvicorn — auto-instruments FastAPI routes, httpx client, and logging
opentelemetry-instrument uvicorn app.main:app --host 0.0.0.0 --port 8100
```

---

## Manual Spans for Business Operations

> **Per `BUS-7.1` (Audit Trail):** The following operations must emit a named span so they are observable in Dynatrace regardless of whether the HTTP request span covers them.

### Operations Requiring Manual Spans

| Operation | Span Name | Required Attributes |
|-----------|-----------|-------------------|
| PII redaction | `pii.redact` | `request.tid`, `field_count` |
| LLM generate call | `llm.generate` | `request.tid`, `model.deployment_name`, `prompt_tokens`, `completion_tokens` |
| Compliance validation | `compliance.validate` | `request.tid`, `complaint.category`, `violations_found` |
| Audit trace write | `audit.write_trace` | `request.tid`, `outcome` |

### Pattern

```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

def redact_pii_with_span(complaint: dict, tid: str) -> tuple[dict, dict]:
    """Per BUS-7.1: PII redaction emits an OTEL span for observability."""
    with tracer.start_as_current_span("pii.redact") as span:
        span.set_attribute("request.tid", tid)
        # Per ENG-6.1: Never set PII values as span attributes
        redacted, token_map = redact_pii(complaint)
        span.set_attribute("field_count", len(token_map))
        return redacted, token_map

async def call_llm_with_span(tid: str, user_prompt: str, system_prompt: str) -> str:
    """Per BUS-7.1: LLM call emits an OTEL span with token usage."""
    with tracer.start_as_current_span("llm.generate") as span:
        span.set_attribute("request.tid", tid)
        span.set_attribute("model.deployment_name", settings.azure_openai_model)
        result = wrapper.generate(tid, user_prompt, system_prompt)
        # token usage would be set here from the wrapper's return metadata
        return result
```

---

## structlog + OTEL Trace Correlation

Auto-instrumenting logging with `LoggingInstrumentor` injects `otelTraceID` and `otelSpanID` into every log record. To surface these in structlog:

```python
import structlog
import logging

def configure_structlog():
    """Bind OTEL trace context into structlog records."""
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
    )
```

This produces logs like:
```json
{
  "event": "LLM call complete",
  "tid": "req-001",
  "otelTraceID": "1a2b3c4d...",
  "otelSpanID": "5e6f7a8b...",
  "model": "gpt-4o",
  "timestamp": "2026-03-18T14:22:01.234Z"
}
```

Dynatrace correlates these log records with the trace span automatically.

---

## Dynatrace-Specific Patterns

AA's observability stack exports OTEL to Dynatrace via OTLP. Key configuration:

```bash
# Environment variables for Dynatrace ingest
OTEL_EXPORTER_OTLP_ENDPOINT=https://{your-env}.live.dynatrace.com/api/v2/otlp
OTEL_EXPORTER_OTLP_HEADERS="Authorization=Api-Token dt0c01.{your-token}"
OTEL_SERVICE_NAME=cr-genai-draft-response
OTEL_RESOURCE_ATTRIBUTES=deployment.environment=prod,service.version=1.2.0
```

> **Per `ENG-6.1` (Security):** The Dynatrace API token must come from a Kubernetes Secret or environment variable — never hardcoded or committed to source.

---

## Testing OTEL Spans (ENG-4.1)

> **Per `ENG-4.1` (Atomic TDD):** Span emission must be testable without a live OTLP collector. Use `opentelemetry-sdk`'s `InMemorySpanExporter`.

```python
# tests/unit/test_otel_spans.py
import pytest
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry import trace


@pytest.fixture
def in_memory_tracer():
    """Provide a TracerProvider with InMemorySpanExporter for unit tests."""
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    trace.set_tracer_provider(provider)
    yield exporter
    exporter.clear()


def test_pii_redact_emits_span_with_tid(in_memory_tracer):
    """Per BUS-7.1: pii.redact span must be emitted with request.tid attribute."""
    # WHEN
    redact_pii_with_span(complaint={"text": "complaint"}, tid="test-001")

    # THEN
    spans = in_memory_tracer.get_finished_spans()
    pii_spans = [s for s in spans if s.name == "pii.redact"]
    assert len(pii_spans) == 1
    assert pii_spans[0].attributes["request.tid"] == "test-001"


def test_pii_span_does_not_include_customer_name(in_memory_tracer):
    """Per ENG-6.1: PII values must never appear as span attributes."""
    redact_pii_with_span(complaint={"customer_name": "Maria Torres"}, tid="test-002")

    spans = in_memory_tracer.get_finished_spans()
    for span in spans:
        for attr_value in span.attributes.values():
            assert "Maria Torres" not in str(attr_value)
```

---

## Anti-Patterns

| Anti-Pattern | Correct Pattern |
|-------------|----------------|
| Removing `opentelemetry-instrument` from the start command | Never remove — breaks Dynatrace correlation for all requests |
| Setting customer PII as span attributes | Set only non-PII attributes: `tid`, `category`, `outcome` |
| Hardcoding OTLP endpoint | Load from `OTEL_EXPORTER_OTLP_ENDPOINT` env var |
| Skipping manual spans on LLM calls | LLM calls must have named spans per `BUS-7.1` |
| Using `SimpleSpanProcessor` in production | Use `BatchSpanProcessor` in production for performance |
