---
skill:
  id: skill-cpp-logging-diagnostics-standards
  name: "C++ Logging and Diagnostics Standards"
  category: platform-engineering
  version: "1.0.0"
  avatar: cpp

laws:
  implements:
    - id: ENG-6.7
      title: Audit Trail Law (NON-NEGOTIABLE)
    - id: ENG-6.4
      title: Data Protection Law (NON-NEGOTIABLE)
  references:
    - id: ENG-5.6
      title: Observability Law

triggers:
  phrases:
    - "C++ logging framework"
    - "C++ spdlog setup"
    - "C++ structured logging"
    - "C++ PII in logs"
    - "C++ audit log format"

followed_by:
  - skill-13-observability
  - skill-10-security-review
---

# Skill: C++ Logging and Diagnostics Standards

## Purpose

Enforce structured logging with PII redaction so that all C++ services produce audit-ready, machine-readable logs. Per [ENG-6.7](laws/engineering/eng-6-security.md), every significant action must be traceable; per [ENG-6.4](laws/engineering/eng-6-security.md), PII must never appear in log output.

## Procedure

1. **Use spdlog** — adopt spdlog as the structured logging framework with JSON output format for production
2. **Apply log level policy** — TRACE/DEBUG disabled in production; INFO for normal operations; WARN for recoverable issues; ERROR/CRITICAL for failures
3. **Redact PII at the logging boundary** — wrap PII fields in masking functions (`mask_name()`, `mask_pnr()`) before passing to logger
4. **Include audit fields** — every audit-relevant log entry must contain: `timestamp`, `service`, `action`, `actor`, `outcome`, `trace_id`
5. **Integrate with OpenTelemetry** — inject trace context (trace_id, span_id) into log entries for distributed trace correlation

## Governance Gate

Per [ENG-6.4](laws/engineering/eng-6-security.md), any log statement emitting unmasked PII (passenger name, PNR, credit card, SSN) is a **blocking violation**. Per [ENG-6.7](laws/engineering/eng-6-security.md), a service endpoint without structured logging is incomplete.

## C++ Specific Patterns

- Use spdlog's `fmt`-based API for type-safe structured logging (no printf)
- Configure JSON sink (`spdlog::sinks::basic_file_sink_mt`) for production; color console for development
- Create domain-specific loggers (`spdlog::get("flight-service")`) rather than using the default logger
- Use `spdlog::set_error_handler()` to catch logging failures without crashing the service
