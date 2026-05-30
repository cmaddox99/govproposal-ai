---
laws: [ENG-6.1, ENG-6.4, ENG-6.7]
avatar: [opentelemetry-python]
title: Security Laws — OpenTelemetry Python
---

# Security Laws: ENG-6.1, ENG-6.4, ENG-6.7 — OpenTelemetry Python

## ENG-6.1: Security by Design

OTEL configuration comes entirely from environment variables. Never set customer PII as span attributes. Never log OTEL auth headers.

```python
import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

def configure_otel() -> None:
    # ✅ OTLP endpoint and auth token from env vars
    exporter = OTLPSpanExporter(
        endpoint=os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"],
        # Auth header set via OTEL_EXPORTER_OTLP_HEADERS env var (managed by platform)
        # ❌ NEVER: headers={"Authorization": "Api-Token " + DYNATRACE_TOKEN}
    )
    provider = TracerProvider()
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)

# ✅ Correct env vars (set in deployment manifest, not application code)
# OTEL_EXPORTER_OTLP_ENDPOINT=https://abc123.live.dynatrace.com/api/v2/otlp
# OTEL_EXPORTER_OTLP_HEADERS=Authorization=Api-Token dt0c01.XXXX
# OTEL_SERVICE_NAME=hangar-ai-demand-service
```

Span attributes — only safe identifiers:

```python
tracer = trace.get_tracer("llm_service")

def generate_response(prompt: str, correlation_id: str, deployment: str) -> str:
    with tracer.start_as_current_span("llm.generate") as span:
        # ✅ Safe attributes: technical identifiers only
        span.set_attribute("correlation_id",    correlation_id)
        span.set_attribute("model_deployment",  deployment)
        span.set_attribute("operation",         "generate")

        # ❌ NEVER — PII as span attributes
        # span.set_attribute("customer_name",  customer_name)
        # span.set_attribute("pnr",            pnr)
        # span.set_attribute("passenger_email", email)

        response = _client.chat.completions.create(model=deployment, messages=[...])
        span.set_attribute("token_count", response.usage.total_tokens)
        return response.choices[0].message.content
```

The `opentelemetry-instrument` auto-instrumentation command must be used in production to enable Dynatrace correlation:

```bash
# ✅ Dynatrace OneAgent integration requires this wrapper
opentelemetry-instrument uvicorn app.main:app --host 0.0.0.0 --port 8080

# ❌ Bypasses OTEL auto-instrumentation — breaks Dynatrace trace correlation
# uvicorn app.main:app --host 0.0.0.0 --port 8080
```

## ENG-6.4: Data Protection

Span attributes must not contain PII. Use a `SpanProcessor` to strip accidental PII before export.

```python
from opentelemetry.sdk.trace import SpanProcessor, ReadableSpan
from opentelemetry.sdk.trace.export import SpanExporter

PII_ATTRIBUTE_KEYS = {
    "customer_name", "passenger_name", "email", "pnr",
    "loyalty_number", "phone_number", "date_of_birth",
    "credit_card", "ssn",
}

class PiiStrippingSpanProcessor(SpanProcessor):
    """Defence-in-depth: strip accidental PII attributes before export to Dynatrace."""

    def on_start(self, span, parent_context=None):
        for key in list(getattr(span, "attributes", {}).keys()):
            if key in PII_ATTRIBUTE_KEYS:
                del span.attributes[key]

    def on_end(self, span: ReadableSpan):
        pass  # spans are immutable at export time — prevention via on_start

# Register as the FIRST processor so PII is stripped before BatchSpanProcessor
provider = TracerProvider()
provider.add_span_processor(PiiStrippingSpanProcessor())
provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
```

structlog configuration — inject trace ID, no PII values:

```python
import structlog
from opentelemetry import trace as otel_trace

def add_trace_context(logger, method, event_dict):
    """Inject W3C TraceContext trace/span IDs into every log line."""
    span = otel_trace.get_current_span()
    if span.is_recording():
        ctx = span.get_span_context()
        event_dict["trace_id"] = format(ctx.trace_id,  "032x")
        event_dict["span_id"]  = format(ctx.span_id,   "016x")
    return event_dict

structlog.configure(
    processors=[
        add_trace_context,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ]
)

log = structlog.get_logger()

# ✅ Safe log line — technical identifiers only
log.info("Processing request",
         correlation_id=correlation_id,
         operation="generate",
         model_deployment=deployment)
# ❌ NEVER: log.info("Processing request", customer_name=name, pnr=pnr)
```

## ENG-6.7: Audit Trail

Each OTEL span IS an audit record. Require spans for every stage of the pipeline: PII redaction, LLM generate, compliance validation, audit write. Correlation ID propagated via W3C TraceContext.

```python
from opentelemetry.propagate import extract, inject
from opentelemetry import trace, context as otel_context

tracer = trace.get_tracer("hangar_ai")

async def handle_booking_assist(request: BookingAssistRequest,
                                 incoming_headers: dict) -> str:
    # Extract W3C TraceContext from upstream caller (API gateway)
    ctx = extract(incoming_headers)

    with tracer.start_as_current_span("pii_redaction", context=ctx) as span:
        span.set_attribute("correlation_id", request.correlation_id)
        safe_prompt = redact_pii(request.prompt)

    with tracer.start_as_current_span("llm.generate") as span:
        span.set_attribute("correlation_id",   request.correlation_id)
        span.set_attribute("model_deployment", os.environ["AZURE_OPENAI_DEPLOYMENT"])
        response_text = await call_llm(safe_prompt)

    with tracer.start_as_current_span("compliance_validation") as span:
        span.set_attribute("correlation_id", request.correlation_id)
        validate_compliance(response_text)

    with tracer.start_as_current_span("audit_write") as span:
        span.set_attribute("correlation_id", request.correlation_id)
        await write_audit_record(request.correlation_id, response_text)

    return response_text
```

Correlation ID (TID) as structlog context variable:

```python
import structlog
_log_ctx = structlog.contextvars

def set_correlation_context(correlation_id: str) -> None:
    _log_ctx.clear_contextvars()
    _log_ctx.bind_contextvars(correlation_id=correlation_id)

# Every subsequent log.info() automatically includes correlation_id
```

Spans exported to Dynatrace via OTLP are immutable — never attempt retroactive modification:

```
Note: Once a span is exported to Dynatrace, it cannot be modified or deleted.
Do NOT attempt to "patch" span attributes after export. If sensitive data
accidentally reaches a span, rotate affected credentials and file a security event.
```

## Anti-Patterns

1. **Removing `opentelemetry-instrument` from the start command** — Dynatrace OneAgent requires auto-instrumentation to correlate traces with infrastructure metrics; omitting it silently breaks distributed tracing and violates BUS-7.1 observability requirements.
2. **Setting `customer_name` or `pnr` as span attributes** — all span attributes are exported to Dynatrace and accessible to anyone with DT access; PII in span attributes violates AA data classification policy.
3. **Hardcoding the OTLP endpoint** — `endpoint="https://abc123.live.dynatrace.com/..."` in application code exposes the DT tenant URL and is not rotatable without a code change; use `OTEL_EXPORTER_OTLP_ENDPOINT`.
4. **Skipping the `llm.generate` span** — the LLM call is a required audit point per BUS-7.1; a pipeline that calls Azure OpenAI without an enclosing span has no audit trail for model invocations in Dynatrace.
5. **Logging OTLP auth headers for debugging** — `logger.debug("OTEL headers: %s", headers)` writes the Dynatrace API token to log aggregators; treat OTLP auth headers as credentials.
