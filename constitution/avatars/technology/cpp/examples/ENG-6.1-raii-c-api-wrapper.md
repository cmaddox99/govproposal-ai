---
law_id: ENG-6.1
cpp_version_min: 14
avatar: cpp
---

# [ENG-6.1](laws/engineering/eng-6-security.md) — RAII Wrappers for C API Resources

**The Rule:** Every C resource (FILE*, socket fd, OpenSSL context, database handle) must be wrapped in RAII so that cleanup happens automatically on scope exit — including when exceptions are thrown. Raw C resource management is the #1 source of resource leaks in C++ services.

**When to use which approach:**
- **Simple resources** (file, socket): `std::unique_ptr` with custom deleter — one line, no new class needed
- **Complex lifecycle** (open/read/write/close, connect/send/recv/disconnect): Dedicated RAII class with move semantics
- **Shared ownership** (rare): `std::shared_ptr` with custom deleter

## NON-COMPLIANT: Manual Resource Management

```cpp
FILE* f = fopen("manifest.dat", "r");
process(f);   // ❌ if process() throws, f is never closed → leak
fclose(f);

int sock = socket(AF_INET, SOCK_STREAM, 0);
connect(sock, &addr, sizeof(addr));
send_data(sock);  // ❌ if send_data() throws, socket leaks → fd exhaustion
close(sock);
```

## COMPLIANT: RAII with unique_ptr Custom Deleter

```cpp
// Simple resource — unique_ptr with custom deleter (one line)
auto file = std::unique_ptr<FILE, decltype(&fclose)>(
    fopen("manifest.dat", "r"), &fclose);
if (!file) throw std::runtime_error{"cannot open manifest"};
process(file.get());  // closed automatically on scope exit or exception

// Complex resource — dedicated RAII class with move semantics
class Socket {
    int fd_;
public:
    explicit Socket(int fd) : fd_(fd) {}
    ~Socket() { if (fd_ >= 0) ::close(fd_); }
    Socket(Socket&& o) noexcept : fd_(std::exchange(o.fd_, -1)) {}
    Socket& operator=(Socket&&) noexcept;
    int get() const { return fd_; }
    // Non-copyable — socket ownership is exclusive
    Socket(const Socket&) = delete;
    Socket& operator=(const Socket&) = delete;
};
```

**⚠️ Edge case:** Using a function pointer as `unique_ptr` deleter (like `&fclose`) adds 8 bytes to the pointer's size. A stateless lambda `[](FILE* f) { fclose(f); }` is optimized to zero overhead via Empty Base Optimization. For performance-critical code with many resource handles, prefer the lambda form.

## Edge Cases & Warnings

| Scenario | Risk | Safe Approach |
|----------|------|---------------|
| Move constructor throws mid-way through acquiring the wrapped resource | RAII invariant broken — destructor runs on a partially-constructed object and attempts to free a null handle | Mark move constructor `noexcept` when the resource transfer cannot fail; initialize the moved-from handle to a sentinel (e.g., `INVALID_SOCKET = -1`) the destructor can skip |
| RAII wrapper exported from a shared library; ABI changes when wrapper gains a member | Library consumer holds a pointer to the old size; destructor called on wrong bytes | Use the PImpl idiom or an opaque handle type at DLL boundaries; never export RAII wrapper types directly |
| Wrapping a C resource handle that is not uniquely owned (non-owning alias) | Destructor frees a handle still in use by the caller; double-free or use-after-free | Use a non-owning view type (raw handle with no destructor) at non-owning sites; ownership transfer through `unique_ptr` only |
