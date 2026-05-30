---
law_id: ENG-3.1
cpp_version_min: 14
avatar: cpp
---

# [ENG-3.1](laws/engineering/eng-3-code-quality.md): Code Smell — RAII Conversion

## The Rule

Convert raw resource management patterns (`fopen`/`fclose`, `malloc`/`free`, `new`/`delete`) to RAII wrappers. Destructors guarantee cleanup on every exit path — including exceptions — eliminating an entire class of resource leaks.

## Before / After Summary

| Before (manual cleanup) | After (RAII) |
|--------------------------|--------------|
| `FILE* f = fopen(...)` + manual `fclose` on each path | `std::unique_ptr<FILE, FileCloser>` — auto-closes |
| `char* buf = malloc(...)` + manual `free` | `std::vector<char>` — auto-frees |
| `new FlightData()` + manual `delete` | `std::make_unique<FlightData>()` — auto-deletes |

## Context

Legacy C++ code often has functions with multiple `return` statements, each preceded by manual cleanup. Some paths forget cleanup, causing resource leaks. RAII conversion is the highest-value refactoring.

## NON-COMPLIANT: Manual Cleanup with Multiple Returns

```cpp
int processFlightManifest(const char* path, FlightData** out) {
    FILE* file = fopen(path, "r");
    if (!file) return -1;

    char* buffer = (char*)malloc(4096);
    if (!buffer) { fclose(file); return -2; }

    FlightData* data = new FlightData();
    if (!data->parse(file, buffer)) {
        free(buffer); fclose(file); delete data; return -3;
    }
    if (!data->validate()) {
        fclose(file); delete data; return -4; // BUG: buffer leaked!
    }
    *out = data; free(buffer); fclose(file); return 0;
}
```

## COMPLIANT: RAII Guards Eliminate All Leak Paths

```cpp
#include <memory>
#include <cstdio>
#include <vector>

struct FileCloser {
    void operator()(FILE* f) const { if (f) fclose(f); }
};
using FileGuard = std::unique_ptr<FILE, FileCloser>;

int processFlightManifest(const char* path, std::unique_ptr<FlightData>& out) {
    FileGuard file(fopen(path, "r"));
    if (!file) return -1;

    std::vector<char> buffer(4096);
    auto data = std::make_unique<FlightData>();
    if (!data->parse(file.get(), buffer.data())) return -3;
    if (!data->validate()) return -4; // ALL resources safe
    out = std::move(data);
    return 0;
}
```

Per [ENG-4.1](laws/engineering/eng-4-testing.md), convert one resource per PR with characterization tests.

## Edge Cases & Warnings

| Scenario | Risk | Safe Approach |
|----------|------|---------------|
| Intentional leaks at shutdown (shared caches, singleton loggers) | Wrapping in RAII causes destructor ordering issues or slows shutdown | Mark explicitly with `// INTENTIONAL: no cleanup at shutdown`; do not force-wrap in RAII |
| C API callback that takes a raw pointer the library will `free()` | Wrapping in `unique_ptr` causes a double-free when the library releases and the destructor also releases | Use `unique_ptr::release()` to hand off ownership; document the ownership transfer at the call site |
| RAII wrapper introduced around a non-owning handle alias | Destructor frees a resource still in use elsewhere; use-after-free in the other holder | Use a non-owning view struct (raw handle, no destructor) for aliases; RAII wrappers only for owning handles |
