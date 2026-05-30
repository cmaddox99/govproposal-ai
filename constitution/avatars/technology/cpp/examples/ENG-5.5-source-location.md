---
id: ENG-5.5-source-location
law_id: ENG-5.5
avatar: cpp
title: source_location for Structured Logging
cpp_version_min: "20"
tags: [observability, logging, source_location, macros]
---

# `std::source_location` — ENG-5.5

Per [ENG-5.5](../../../laws/engineering/eng-5-devops.md), structured
log records must include call-site context (file, function, line) without macros.

## COMPLIANT

```cpp
#include <source_location>
#include <string_view>
#include <iostream>

// Zero-overhead call-site capture via default parameter
void log_info(std::string_view msg,
              std::source_location loc = std::source_location::current()) {
    std::cout << "[INFO] " << loc.file_name() << ':' << loc.line()
              << " (" << loc.function_name() << ") " << msg << '\n';
}

void process_flight(const Flight& f) {
    log_info("processing flight");  // captures call site automatically
}
```

## NON-COMPLIANT

```cpp
// Macro-based: fragile, pollutes namespace, can't be forwarded
#define LOG_INFO(msg) \
    std::cout << "[INFO] " << __FILE__ << ':' << __LINE__ << ' ' << (msg) << '\n'

void process_flight(const Flight& f) {
    LOG_INFO("processing flight");  // __FILE__/__LINE__ are textual — not type-safe
}
```

## Edge Cases & Warnings

| Scenario | Risk | Mitigation |
|----------|------|------------|
| Template instantiation | `function_name()` includes template args (long) | Truncate or strip at `<` for display |
| `consteval` context | `current()` returns compile-time location correctly | No special handling needed |
| Async continuations | Location captured at suspension point, not resume | Capture before `co_await` if caller context needed |
| Forwarding wrappers | Wrapping `log_info` copies `loc` from outer caller | Pass `loc` explicitly in wrapper's default param |
