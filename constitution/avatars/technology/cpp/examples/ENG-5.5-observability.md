---
law_id: ENG-5.5
cpp_version_min: 11
avatar: cpp
title: Observability Law — C++ Patterns
tokens: ~480
---

# ENG-5.5 Observability Law — C++ Patterns

**Law:** ENG-5.5 (Observability Law)  
**Avatar:** `avatars/technology/cpp/`

---

## Core Rule

Every production C++ service MUST emit structured logs, metrics, and traces sufficient
to answer: *Is it working? How fast? Why did it fail?*
Observability is built in at construction time, not bolted on after incidents.

---

## COMPLIANT Patterns

### 1. Structured Logging (spdlog + JSON sink)

```cpp
#include <spdlog/spdlog.h>
#include <spdlog/fmt/ostr.h>

// Log with context — queryable by log aggregators
void assign_crew(FlightId flight, CrewId crew) {
    spdlog::info("crew_assigned",
        spdlog::arg("flight_id", flight.value()),
        spdlog::arg("crew_id",   crew.value()),
        spdlog::arg("rest_hours", rest_hours(crew)));
}

// Structured error — includes causal context, not just message
spdlog::error("crew_assignment_failed",
    spdlog::arg("flight_id", flight.value()),
    spdlog::arg("reason",    "rest_violation"),
    spdlog::arg("crew_id",   crew.value()));
```

### 2. Metrics via Prometheus Client

```cpp
#include <prometheus/counter.h>
#include <prometheus/histogram.h>

// Counters and histograms registered at startup — zero-allocation on hot path
inline auto& assignments_total() {
    static auto& c = prometheus::BuildCounter()
        .Name("crew_assignments_total")
        .Help("Total crew assignment attempts")
        .Register(*registry).Add({{"result", "success"}});
    return c;
}

inline auto& assignment_duration_ms() {
    static auto& h = prometheus::BuildHistogram()
        .Name("crew_assignment_duration_ms")
        .Buckets({1, 5, 10, 50, 100, 500})
        .Register(*registry).Add({});
    return h;
}

// Usage on hot path
assignments_total().Increment();
assignment_duration_ms().Observe(elapsed.count());
```

### 3. Distributed Tracing (OpenTelemetry)

```cpp
#include <opentelemetry/trace/provider.h>

auto tracer = opentelemetry::trace::Provider::GetTracerProvider()
    ->GetTracer("crew-scheduling");

auto span = tracer->StartSpan("assign_crew");
span->SetAttribute("flight.id", flight.value());
span->SetAttribute("crew.id",   crew.value());
// ... work ...
span->End();
```

---

## NON-COMPLIANT Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| `std::cout << "assigned crew"` | No structure, no context, not queryable | Use structured logger |
| Catch exception, print, swallow | Error lost from metrics/traces | Emit metric + re-throw or return error |
| `printf`-style debug logging left in prod | Unstructured, no level control | Replace with `spdlog::debug()` |
| No metrics on SLA-critical paths | Invisible latency degradation | Add histogram on every external call |

---

## CWR Brownfield Path

CWR C++03 constraints:
- Use `spdlog` (header-only, C++11 minimum — compile with `-std=c++11`)
- Defer OpenTelemetry to new services; instrument legacy via log correlation IDs
- Add one Prometheus counter per public domain function as a first step

## Edge Cases & Warnings

| Scenario | Risk | Safe Approach |
|----------|------|---------------|
| Structured log field name collision with framework reserved keys | spdlog or OpenTelemetry SDKs reserve fields like `level`, `timestamp`, `message`; user-defined fields with those names silently override or are dropped | Define a project field schema document; prefix all custom fields with a namespace (`cwr.crew_id`, `cwr.flight_num`); validate schema in CI |
| Tracing context lost across thread-pool boundaries | `std::thread` and most thread pools do not propagate OpenTelemetry context automatically; child spans appear disconnected from the parent trace | Explicitly capture the context at the spawn site and restore it in the worker: `auto ctx = opentelemetry::context::RuntimeContext::GetCurrent(); pool.submit([ctx]{ ... attach ctx ... });` |
| Counter metrics never reset on service restart, making rate graphs misleading | A restarted pod shows a drop to zero, then a spike; alerting fires on the apparent drop | Use gauge metrics for current values and counters with a `_total` suffix (Prometheus convention); dashboards should display rate, not raw counter value |
