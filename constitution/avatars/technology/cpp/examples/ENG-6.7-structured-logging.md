---
law_id: ENG-6.7
cpp_version_min: 17
cpp_version_note: >-
  Uses C++17 string_view for zero-copy log field names. Transitional teams: use const char* or const std::string&; no semantic difference in output.
avatar: cpp
---

# [ENG-6.7](laws/engineering/eng-6-security.md): Audit Trail — Structured Logging

## The Rule

Logs must be **structured** (JSON or key-value), not free-text. Every log entry must include event type, trace ID, and timestamp. PII must be **redacted before logging** — never rely on downstream filtering.

## When to Use

Apply to **all production services**. Structured logs are a prerequisite for log aggregation (Splunk, ELK, Datadog), alerting, and audit trail compliance.

## COMPLIANT: Structured JSON with PII Masking

```cpp
#include <spdlog/spdlog.h>
#include <string>

// why: mask PII BEFORE it reaches any log sink — defense in depth
std::string mask_pnr(std::string_view pnr) {
    if (pnr.size() < 4) return "***";
    return std::string(pnr.size() - 3, '*') + std::string(pnr.substr(pnr.size() - 3));
}

std::string mask_email(std::string_view email) {
    auto at = email.find('@');
    if (at == std::string_view::npos || at < 2) return "***";
    return std::string(at - 1, '*') + std::string(email.substr(at - 1));  // why: preserve domain for debugging
}

void log_booking_confirmed(std::string_view trace_id,
                           std::string_view pnr,
                           std::string_view flight) {
    // why: structured JSON — machine-parseable, queryable in Splunk/ELK
    spdlog::info(R"({{"event":"booking_confirmed","trace_id":"{}","pnr":"{}","flight":"{}"}})",
                 trace_id,
                 mask_pnr(pnr),   // why: PII redacted at source, not downstream
                 flight);
}
// Output: {"event":"booking_confirmed","trace_id":"abc-123","pnr":"***XYZ","flight":"AA1234"}
```

## NON-COMPLIANT: Unstructured Plaintext with PII

```cpp
void log_booking(const std::string& passenger_name, const std::string& pnr) {
    std::cout << "Booking confirmed for " << passenger_name  // ❌ raw PII — GDPR/CCPA violation
              << " PNR: " << pnr << std::endl;               // ❌ unstructured — can't query or aggregate
    // ❌ No trace ID — impossible to correlate across services
    // ❌ std::cout is not thread-safe — interleaved output in concurrent services
}
```

## Edge Cases & Warnings

| Scenario | Guidance |
|----------|----------|
| PII in structured log fields | Redact **at the call site**, not in a log sink filter. Sink filters can be misconfigured or bypassed. |
| Exception messages containing PII | Catch, redact, then log. Never log `e.what()` directly if it may contain user input. |
| Log levels in production | Use `info` for business events, `warn` for recoverable issues, `error` for failures. Never use `debug`/`trace` in production — they may log unredacted data. |
| Thread safety | Use `spdlog` or another thread-safe logger. Raw `std::cout` interleaves output from concurrent threads. |
