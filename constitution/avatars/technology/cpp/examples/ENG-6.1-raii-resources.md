---
law_id: ENG-6.1
cpp_version_min: 11
avatar: cpp
---

# [ENG-6.1](laws/engineering/eng-6-security.md): Security by Design — RAII Resources

## The Rule

Every resource (memory, file handles, sockets, database connections, GPU memory) **must be owned by an RAII type**. Constructors acquire, destructors release — no exceptions.

## When to Use

Apply to **all** resource types: file handles, socket descriptors, database connections, GPU memory, mutex locks, temporary files. If it needs cleanup, it needs an RAII wrapper.

## COMPLIANT: Custom Deleters for System Resources

```cpp
#include <memory>
#include <cstdio>
#include <unistd.h>
#include <stdexcept>

// FILE* with RAII
auto open_manifest(const char* path) {
    auto deleter = [](FILE* f) { if (f) std::fclose(f); };  // why: custom deleter pairs with fopen
    std::unique_ptr<FILE, decltype(deleter)> file(std::fopen(path, "r"), deleter);
    if (!file) throw std::runtime_error("cannot open manifest");  // why: fail fast, no partial state
    return file;  // why: caller owns the handle, cleanup is automatic
}

// Socket fd with RAII
struct SocketCloser {
    void operator()(int* fd) const { if (fd && *fd >= 0) ::close(*fd); delete fd; }
};
using SocketHandle = std::unique_ptr<int, SocketCloser>;

SocketHandle connect_to_gate_service(int fd) {
    return SocketHandle(new int(fd));  // why: auto-closes on scope exit, exception, or early return
}
```

## NON-COMPLIANT: Raw File Handle

```cpp
void process_manifest(const char* path) {
    FILE* f = std::fopen(path, "r");  // ❌ raw handle — no automatic cleanup
    parse(f);    // ❌ if parse() throws, f leaks
    std::fclose(f);  // ❌ never reached on exception
}
```

## Edge Cases & Warnings

| Scenario | Guidance |
|----------|----------|
| Moved-from objects | A moved-from RAII object **must be in a valid state** — typically null/empty. Destructor must handle it safely (no double-free). |
| Database connections | Wrap in RAII with a pool-return deleter: `unique_ptr<Connection, PoolReturner>`. Don't close — return to pool. |
| GPU memory (`cudaFree`) | Use `unique_ptr<void, CudaDeleter>` — GPU leaks are invisible to OS memory tools. |
| Multiple resources in one constructor | Acquire in order, use member RAII types. If second acquisition fails, first member's destructor cleans up automatically. |
| `fopen` returns `NULL` | Always check before wrapping — `unique_ptr` with a null pointer still calls the deleter on some implementations. Guard with `if (!file)`. |
