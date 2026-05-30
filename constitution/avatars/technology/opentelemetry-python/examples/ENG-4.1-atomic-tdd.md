---
laws: [ENG-4.1]
avatar: [opentelemetry-python]
title: Atomic TDD — OpenTelemetry Python
---

# Atomic TDD: ENG-4.1 — OpenTelemetry Python

## Overview

Use `InMemorySpanExporter` to test OTEL instrumentation without a live collector. Each test is a single, self-contained assertion: one span created, one attribute present, one PII field absent.

**Pattern:** `Arrange (InMemorySpanExporter) → Act (call instrumented function) → Assert (span name / attributes / status)`

---

## Test Setup

```python
# tests/conftest.py
import pytest
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

@pytest.fixture
def span_exporter() -> InMemorySpanExporter:
    exporter  = InMemorySpanExporter()
    provider  = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    trace.set_tracer_provider(provider)
    yield exporter
    exporter.clear()
    trace.set_tracer_provider(trace.NoOpTracerProvider())
```

---

## ENG-4.1 Test Cases

### Test 1 — Named span is created with expected attributes

```python
# tests/test_llm_spans.py
from services.llm_service import generate_response

def test_llm_generate_span_created(span_exporter):
    # Arrange — exporter is wired via conftest fixture
    correlation_id = "tid-unit-test-001"

    # Act
    generate_response(
        prompt="What is the baggage policy for Basic Economy?",
        correlation_id=correlation_id,
    )

    # Assert — span created with correct name
    spans = span_exporter.get_finished_spans()
    assert len(spans) == 1
    span = spans[0]
    assert span.name == "llm.generate"
```

### Test 2 — Required safe attributes are present

```python
def test_llm_span_has_required_attributes(span_exporter):
    generate_response(prompt="Rebooking options for AA100", correlation_id="tid-002")

    span = span_exporter.get_finished_spans()[0]

    assert "model_deployment"  in span.attributes
    assert "token_count"       in span.attributes
    assert "correlation_id"    in span.attributes
    assert span.attributes["correlation_id"] == "tid-002"
```

### Test 3 — PII attributes are NOT on the span (critical security test)

```python
def test_llm_span_has_no_pii_attributes(span_exporter):
    """PII must never appear as span attributes — Dynatrace/OTLP exports are not PII-safe."""
    generate_response(
        prompt="Rebook passenger for flight AA200",
        correlation_id="tid-003",
    )

    span = span_exporter.get_finished_spans()[0]
    attr_keys = set(span.attributes.keys())

    pii_attr_names = {"customer_name", "passenger_name", "email", "pnr",
                      "loyalty_number", "phone_number", "date_of_birth"}
    leaked_pii = attr_keys & pii_attr_names
    assert leaked_pii == set(), f"PII attributes leaked to span: {leaked_pii}"
```

### Test 4 — structlog trace ID injection

```python
# tests/test_structlog_trace_injection.py
import structlog
from opentelemetry import trace as otel_trace
from services.logging_setup import configure_structlog_with_trace_id

def test_structlog_injects_trace_id(span_exporter, capsys):
    configure_structlog_with_trace_id()

    tracer = otel_trace.get_tracer("test")
    with tracer.start_as_current_span("test.operation") as span:
        log = structlog.get_logger()
        log.info("test_event", operation="unit_test")

    captured = capsys.readouterr().out
    trace_id  = format(span.get_span_context().trace_id, "032x")
    assert trace_id in captured, "structlog output must contain active trace ID"
```

### Test 5 — Span status is ERROR on exception

```python
from opentelemetry.trace import StatusCode

def test_llm_span_error_status_on_failure(span_exporter, monkeypatch):
    def failing_call(*args, **kwargs):
        raise ConnectionError("Azure OpenAI unreachable")

    monkeypatch.setattr("services.llm_service._azure_client.chat.completions.create",
                        failing_call)

    with pytest.raises(ConnectionError):
        generate_response(prompt="test", correlation_id="tid-004")

    span = span_exporter.get_finished_spans()[0]
    assert span.status.status_code == StatusCode.ERROR
    assert "Azure OpenAI unreachable" in (span.status.description or "")
```

### Test 6 — Credential attributes never on spans

```python
def test_no_credential_attributes_on_span(span_exporter):
    """OTLP endpoint, API keys, and auth headers must never be span attributes."""
    generate_response(prompt="test", correlation_id="tid-005")

    span = span_exporter.get_finished_spans()[0]
    attr_keys = set(span.attributes.keys())

    credential_attrs = {"api_key", "authorization", "bearer_token",
                        "otlp_endpoint", "azure_openai_key"}
    leaked = attr_keys & credential_attrs
    assert leaked == set(), f"Credential attributes leaked to span: {leaked}"
```

---

## Reference: Instrumented Function Shape

```python
# services/llm_service.py
from opentelemetry import trace

tracer = trace.get_tracer("llm_service")

def generate_response(prompt: str, correlation_id: str) -> str:
    with tracer.start_as_current_span("llm.generate") as span:
        span.set_attribute("correlation_id",   correlation_id)
        span.set_attribute("model_deployment", os.environ["AZURE_OPENAI_DEPLOYMENT"])
        # ❌ span.set_attribute("customer_name", customer_name) — NEVER
        # ❌ span.set_attribute("pnr", pnr) — NEVER
        response = _azure_client.chat.completions.create(...)
        span.set_attribute("token_count", response.usage.total_tokens)
        return response.choices[0].message.content
```
