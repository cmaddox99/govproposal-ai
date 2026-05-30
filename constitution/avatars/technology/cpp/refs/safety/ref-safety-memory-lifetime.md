---
cpp_version_min: 11
cpp_version_note: >-
  Strict aliasing and placement new apply to all versions; PMR allocators require C++17.
avatar: cpp
---

# C++ Avatar Reference: Memory Lifetime and FFI Safety

---

## Advanced Memory and Object Lifetime

> ⚠️ **Complexity Warning:** The patterns in this section are for advanced use cases. Prefer smart pointers, containers, and PMR allocators for all new code. Only use placement new, custom allocators, or `std::launder` when profiling proves a standard approach is insufficient, or when interfacing with hardware/OS APIs that require manual memory control.

Per [ENG-6.1](laws/engineering/eng-6-security.md) (Security by Design) and [ENG-3.1](laws/engineering/eng-3-code-quality.md) (Complexity Limits), manual memory management introduces undefined behavior risks that compilers may silently exploit. Every pattern here must be accompanied by a justification comment and sanitizer validation.

### Strict Aliasing

The strict aliasing rule (C++ standard §6.7.2) allows the compiler to assume that pointers of different types do not alias the same memory. Violating this causes **silent UB** — code that works in debug builds but breaks with `-O2`.

```cpp
// NON-COMPLIANT — strict aliasing violation (UB!)
float fast_inverse_sqrt(float x) {
    int i = *(int*)&x;         // ❌ type punning through cast — UB
    i = 0x5f3759df - (i >> 1);
    return *(float*)&i;        // ❌ compiler may optimize this away at -O2
}

// COMPLIANT — use memcpy for safe type punning
float fast_inverse_sqrt(float x) {
    static_assert(sizeof(float) == sizeof(int32_t));
    int32_t i;
    std::memcpy(&i, &x, sizeof(i));   // ✅ defined behavior
    i = 0x5f3759df - (i >> 1);
    std::memcpy(&x, &i, sizeof(x));   // ✅ compiler optimizes to register move
    return x;
}

// COMPLIANT (C++20) — std::bit_cast for trivially-copyable types
float fast_inverse_sqrt(float x) {
    auto i = std::bit_cast<int32_t>(x);  // ✅ constexpr-friendly, safe
    i = 0x5f3759df - (i >> 1);
    return std::bit_cast<float>(i);
}
```

**Governance rules:**
- **Never** cast between unrelated pointer types to access memory — use `std::memcpy` or `std::bit_cast`
- Never use `-fno-strict-aliasing` as a workaround — it masks the bug and disables optimizations
- `reinterpret_cast` is only safe for pointer↔integer round-trips and `char*`/`std::byte*` access
- Validate with `-fsanitize=undefined` (UBSan catches misaligned access but not all aliasing violations)

### Placement New and Object Lifetime

Placement new constructs objects in pre-allocated storage. It requires manual destructor calls, correct alignment, and awareness of object lifetime rules.

```cpp
// COMPLIANT — placement new with proper alignment and lifetime
alignas(FlightPlan) std::byte buffer[sizeof(FlightPlan)];
auto* plan = new (buffer) FlightPlan{origin, dest, date};
// ... use plan ...
plan->~FlightPlan();  // ✅ explicit destructor call required

// COMPLIANT (C++17) — std::optional avoids manual lifetime management
std::optional<FlightPlan> plan;
plan.emplace(origin, dest, date);  // ✅ simpler alternative
plan.reset();                       // ✅ automatic destructor call
```

**Simpler alternative:** Prefer `std::optional`, `std::variant`, or pool allocators (PMR) over raw placement new. Only use placement new when:
- Implementing a custom allocator or memory pool
- Working with memory-mapped I/O or shared memory
- Interfacing with hardware registers at fixed addresses

### `std::launder` and Storage Reuse

When reusing storage for a different object (or after placement new into `const`-qualified or reference-member storage), `std::launder` is required to inform the compiler that the old object is gone.

```cpp
// COMPLIANT — std::launder after storage reuse
struct CacheEntry {
    const std::string key;  // const member — can't assign
    int value;
};

alignas(CacheEntry) std::byte storage[sizeof(CacheEntry)];
auto* entry = new (storage) CacheEntry{"AADFW", 42};
entry->~CacheEntry();
auto* entry2 = new (storage) CacheEntry{"AAORD", 99};
// ✅ Must launder — compiler may cache old "AADFW" value
auto* safe = std::launder(entry2);
```

**When you need `std::launder`:** Only when a type has `const` or reference members AND you reuse the same storage. For most code, this never arises — prefer `std::optional` or containers.

### Custom Allocators — When Standard Allocators Are Insufficient

Per [ENG-3.1](laws/engineering/eng-3-code-quality.md), prefer PMR allocators over custom `operator new` overrides. Custom allocators are justified only when:
- **Arena allocation** — zero-fragmentation for request-scoped memory in high-frequency trading or real-time flight data processing
- **GPU/shared memory** — `unique_ptr` with custom deleter for non-heap memory
- **Debug/profiling** — tracking allocation patterns in production

```cpp
// COMPLIANT — custom deleter for shared memory (not heap)
struct ShmDeleter {
    size_t size;
    void operator()(void* ptr) const noexcept {
        munmap(ptr, size);
    }
};

auto shared_buffer = std::unique_ptr<FlightData, ShmDeleter>{
    static_cast<FlightData*>(mmap(nullptr, sizeof(FlightData),
                                   PROT_READ | PROT_WRITE,
                                   MAP_SHARED, fd, 0)),
    ShmDeleter{sizeof(FlightData)}
};
```

---

## C/C++ Interop and FFI Error Propagation

Per [ENG-6.1](laws/engineering/eng-6-security.md) (Security by Design), all C library calls must be wrapped with error checking. Silent failure at C/C++ boundaries is a critical risk — a `send()` returning `ECONNRESET` that goes unchecked means a gate agent never receives a notification.

### Custom Deleters for C Handles

Wrap all C library handles with `std::unique_ptr` and a custom deleter:

```cpp
// COMPLIANT — RAII for C file handle
auto file = std::unique_ptr<FILE, decltype(&fclose)>(
    fopen("manifest.dat", "r"), &fclose);
if (!file) throw std::runtime_error{"Cannot open manifest"};

// COMPLIANT — RAII for OpenSSL context
auto ssl_ctx = std::unique_ptr<SSL_CTX, decltype(&SSL_CTX_free)>(
    SSL_CTX_new(TLS_client_method()), &SSL_CTX_free);

// COMPLIANT — RAII for POSIX socket; stores fd directly as member (no heap alloc)
struct SocketHandle {
    int fd_ = -1;
    explicit SocketHandle(int fd) : fd_(fd) {}
    ~SocketHandle() { if (fd_ >= 0) close(fd_); }
    SocketHandle(const SocketHandle&) = delete;
    SocketHandle& operator=(const SocketHandle&) = delete;
    SocketHandle(SocketHandle&& o) noexcept : fd_(std::exchange(o.fd_, -1)) {}
    int get() const noexcept { return fd_; }
};
auto sock = SocketHandle{socket(AF_INET, SOCK_STREAM, 0)};
```

### Error Code Translation Pattern

Wrap every C library call in a checked helper that translates `errno` / return codes to C++ error types.
For C++23+ codebases, `std::expected` (C++23) gives the cleanest spelling. For C++17/20 projects,
use `std::error_code` + exceptions, or an open-source `tl::expected`:

```cpp
// C++23: std::expected
// (for C++17/20, substitute tl::expected<T, std::error_code>)
template<typename T>
std::expected<T, std::error_code> checked_posix(T result) {
    if (result == -1)
        return std::unexpected(std::error_code(errno, std::system_category()));
    return result;
}

// Usage
auto bytes = checked_posix(send(sock, data, len, 0));
if (!bytes) {
    spdlog::error("Send failed: {}", bytes.error().message());
    return std::unexpected(bytes.error());
}
```

### FFI Boundary Rules

1. Never let C++ exceptions propagate across `extern "C"` boundaries — catch at the boundary and translate to error codes
2. Use `noexcept` on all `extern "C"` callback functions
3. Document ownership transfer for every pointer crossing the boundary (who allocates, who frees)
4. Validate all data received from C libraries before using in C++ domain logic

---



---

## C-Style Programming (CPL.xx)

Per [ENG-3.1](laws/engineering/eng-3-code-quality.md), follow Core Guidelines
CPL.1/CPL.2 — use C++ over C except where a C API is unavoidable; wrap C
idioms in C++ RAII to prevent resource leaks.

| Rule | Guidance |
|------|---------|
| CPL.1 | Prefer C++ — namespaces, RAII, templates, exceptions over global state |
| CPL.2 | Use C only when a C-only API/ABI exists (OS calls, embedded HAL, third-party C libs) |
| CPL.3 | Use `extern "C"` for interoperability; never let C++ name-mangling surprise callers |

```cpp
// extern "C" linkage: disables name mangling for cross-language interop
extern "C" {
    int aa_flight_status(int flight_number, char* out_buf, size_t buf_len);
}

// C struct → RAII C++ class (CPL.2 pattern)
struct CConfig { /* raw C struct from legacy lib */ };
class Config {           // C++ wrapper; owns CConfig lifetime
    CConfig raw_;
public:
    explicit Config(const char* path) { init_config(&raw_, path); }
    ~Config() noexcept   { destroy_config(&raw_); }
    Config(const Config&) = delete;
    const CConfig* get() const noexcept { return &raw_; }
};

// C array → std::span (CPL.1 — zero-cost view, no copy)
void process_waypoints(std::span<const Waypoint> pts) {
    process_waypoints_c(pts.data(), pts.size());  // bridge to C
}
```

## GSL Profiles (Pro.xx)

Per [ENG-6.1](laws/engineering/eng-6-security.md), apply GSL safety profiles
incrementally to eliminate whole classes of undefined behavior.

| Profile | Eliminates | Key rule |
|---------|-----------|---------|
| Type (Pro.1) | `reinterpret_cast`, unions, varargs | Use `std::bit_cast`, `std::variant` |
| Bounds (Pro.2) | Raw array access without size | Use `std::span`, `at()`, range-for |
| Lifetime (Pro.3) | Dangling pointers, use-after-free | Owner smart pointers; no `T&` to local |

```cpp
#include <gsl/gsl>  // vcpkg install ms-gsl

// Bounds-safe span (Pro.2)
void print_flights(gsl::span<const Flight> flights) {
    for (const auto& f : flights) std::cout << f.id() << '\n';
}

// not_null to document and enforce non-null at compile time
void book_seat(gsl::not_null<Passenger*> p, FlightId id);

// [[gsl::suppress]] for justified exceptions (rare)
[[gsl::suppress("bounds")]]
void memcpy_wrapper(void* dst, const void* src, size_t n) {
    std::memcpy(dst, src, n);  // known-safe, isolated
}
```

**Adoption path:** enable per file with `-DGSL_UNENFORCED_ON_CONTRACT_VIOLATION`;
graduate warnings → errors across sprints.

## See Also

- [Core Language Patterns](ref-core-language.md)
- [Concurrency & Resiliency](ref-concurrency.md)
- [Aviation & JNI Safety](ref-safety-aviation.md)


---

## See Also

- [Safety-Critical C++ - MISRA and DO-178C](ref-safety-misra-do178.md)
