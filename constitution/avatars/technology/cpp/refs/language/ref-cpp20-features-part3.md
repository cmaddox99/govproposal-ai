---
id: ref-cpp20-features-part3
cpp_version_min: 20
cpp_version_note: >-
  C++20 features Part 3: std::format, std::bit_cast, std::source_location,
  constinit, std::atomic_ref. Requires C++20 compiler support.
  See Part 1 for modules, ranges, span, spaceship.
  See Part 2 for coroutine generators and calendar/timezone.
avatar: cpp
---

# C++20 Core Features — Part 3

Per [ENG-2.2](laws/engineering/eng-2-architecture.md) (Architecture Law), all C++20
features must be introduced with governing context and migration guidance.

---

## std::format

Per [ENG-6.1](laws/engineering/eng-6-security.md) (Security) and
[ENG-6.5](laws/engineering/eng-6-security.md) (Input Validation), `std::format` is the
type-safe, locale-independent successor to `printf`/`sprintf`/`stringstream`. It eliminates
format-string type mismatches at compile time. Core Guidelines ES.45 (no magic strings).

### std::format vs. printf / sprintf

```cpp
// COMPLIANT — type-safe; compile error if argument type mismatches format
std::string msg = std::format("Flight {}/{} departs at {:05d}",
                               flight.carrier, flight.number,
                               flight.departure_hhmm);

// NON-COMPLIANT — printf: no compile-time type check; UB on mismatch
char buf[64];
sprintf(buf, "Flight %s/%d departs at %05d",
        flight.carrier.c_str(), flight.number,
        flight.departure_hhmm);  // ❌ UB if carrier is not null-terminated C-str

// NON-COMPLIANT — stringstream: verbose; locale-sensitive by default
std::ostringstream oss;
oss << "Flight " << flight.carrier << "/" << flight.number;  // ❌ verbose
```

### std::format_to — Writing into Buffers and Output Iterators

Use `std::format_to` to avoid constructing an intermediate `std::string` on hot paths:

```cpp
// COMPLIANT — format directly into an audit log buffer
void write_audit_entry(std::span<char> buf, const FlightId& id,
                       std::string_view event) {
    if (buf.empty()) return;   // nothing to write into — guard against underflow
    auto result = std::format_to_n(buf.data(), buf.size() - 1,
                                   "[AUDIT] {}/{} — {}", id.carrier, id.number, event);
    // result.out points one past the last written char; null-terminate there
    *result.out = '\0';  // ✅ safe: reserved one byte above for this terminator
}
```

### Custom std::formatter Specialisation

```cpp
// COMPLIANT — formatter<FlightId> enables std::format("{}", flight_id)
template<>
struct std::formatter<FlightId> : std::formatter<std::string> {
    auto format(const FlightId& id, std::format_context& ctx) const {
        return std::formatter<std::string>::format(
            std::format("{}{:04d}", id.carrier, id.number), ctx);
    }
};

// Usage — FlightId now composes in any format string
std::string msg = std::format("Boarding: {} at gate {}", flight_id, gate);
// ✅ Prints e.g. "Boarding: AA0100 at gate B22"

// NON-COMPLIANT — ad-hoc to_string() scattered across callers
std::string s = flight_id.carrier + std::to_string(flight_id.number);  // ❌ no width control
```

### std::vformat — Runtime Format Strings (Avoid)

`std::vformat` accepts a runtime format string. This is unsafe in AA systems:

```cpp
// NON-COMPLIANT — runtime format string: attacker-controlled format = security risk
std::string user_input = get_user_template();          // user-supplied
std::string result = std::vformat(user_input,          // ❌ DO NOT use with external input
    std::make_format_args(flight_id, gate));

// COMPLIANT — enumerate and validate format strings explicitly
// Use a whitelist of pre-approved templates; never pass raw user input to vformat.
```

**[ENG-6.5](laws/engineering/eng-6-security.md) rule:** `std::vformat` with user-supplied
format strings must be treated as an injection vector. Pre-approve all format templates or
use fixed `std::format` call sites.

---

## std::bit_cast

Per [ENG-6.1](laws/engineering/eng-6-security.md) (Security), `std::bit_cast<To>(from)` is
the type-safe, well-defined replacement for `reinterpret_cast`-based type-punning and
`memcpy` tricks. Core Guidelines ES.49 (use named casts).

### Constraints

`std::bit_cast<To>(from)` requires:
1. `sizeof(To) == sizeof(From)` — exact size match
2. Both types are **trivially copyable** (`std::is_trivially_copyable_v<T>`)

### IEEE-754 Float Inspection

```cpp
// COMPLIANT — inspect float bits without UB
uint32_t float_bits = std::bit_cast<uint32_t>(3.14f);
bool is_negative  = (float_bits >> 31) & 1;
uint32_t exponent = (float_bits >> 23) & 0xFF;
uint32_t mantissa =  float_bits        & 0x7F'FFFF;

// NON-COMPLIANT — type-punning via pointer cast: UB (strict aliasing violation)
float f = 3.14f;
uint32_t bits = *reinterpret_cast<uint32_t*>(&f);  // ❌ strict aliasing UB

// NON-COMPLIANT — memcpy: defined but verbose
uint32_t bits2;
std::memcpy(&bits2, &f, sizeof(f));  // ⚠️ works but bit_cast is cleaner
```

### Binary Protocol Parsing (ACARS / ADS-B)

ACARS and ADS-B messages arrive as packed binary structs.
`bit_cast` provides safe extraction without `reinterpret_cast`.

> ⚠️ **Portability note:** bit-field layout is implementation-defined and
> endianness-sensitive. For true portable protocol parsing, use explicit masks
> and shifts after `bit_cast`ing to a `uint32_t`, not directly to a bit-field struct.

```cpp
// COMPLIANT — safe extraction via bit_cast to integer, then explicit masking
uint32_t raw = read_word_big_endian(buf, offset);  // handle endian before bit_cast
// Bit layout (ADS-B vel word): bits[9:0]=ew_vel, bit[10]=ew_dir, bits[20:11]=ns_vel, bit[21]=ns_dir
int ew_vel = raw & 0x3FF;
int ew_dir = (raw >> 10) & 1;
int ew_kts = ew_dir ? -ew_vel : ew_vel;

// COMPLIANT — bit_cast for IEEE-754 inspection (portable: floats are well-specified)
static_assert(std::is_trivially_copyable_v<float>);
uint32_t float_bits = std::bit_cast<uint32_t>(3.14f);  // ✅ defined; same size

// NON-COMPLIANT — reinterpret_cast on packed buffer: UB + alignment trap
auto* p = reinterpret_cast<uint32_t*>(buf + offset);  // ❌ alignment UB
```

**[ENG-6.1](laws/engineering/eng-6-security.md) rule:** `reinterpret_cast` for type-punning
is prohibited without a documented justification in the code review record. Use
`std::bit_cast` for all new type-punning needs.

---

## std::source_location

Per [ENG-6.7](laws/engineering/eng-6-security.md) (Audit Trail) and
[ENG-5.5](laws/engineering/eng-5-devops.md) (Observability), structured call-site
capture replaces `__FILE__`/`__LINE__` macros in logging and audit functions.
Core Guidelines ES.30/ES.31 (don't use macros for constants or "functions").

### Default Parameter Pattern

```cpp
// COMPLIANT — source_location::current() captures call site at the call expression
void audit_log(std::string_view event,
               std::source_location loc = std::source_location::current()) {
    // loc.file_name(), loc.line(), loc.function_name() — all thread-safe
    std::format_to(std::back_inserter(audit_buf_),
        "[AUDIT] {}:{} ({}) — {}\n",
        loc.file_name(), loc.line(), loc.function_name(), event);
}

// Caller — no macro noise; location captured automatically
audit_log("seat_assignment_changed");   // ✅ captures exact call site

// NON-COMPLIANT — __FILE__/__LINE__ macros require caller boilerplate
void audit_log_macro(std::string_view event, const char* file, int line);
audit_log_macro("seat_assignment_changed", __FILE__, __LINE__);  // ❌ caller burden
```

### Comparison: source_location vs. __FILE__/__LINE__

| | `std::source_location` | `__FILE__` / `__LINE__` |
|---|---|---|
| Syntax | Default parameter, no caller change | Explicit macro at every call site |
| Type safety | Structured type | Raw `const char*` / `int` |
| Template-friendly | ✅ Works in templates | ⚠️ Macro expansion can surprise |
| Inlineable | ✅ Captured at call expression | ✅ |
| C++ standard | C++20 | Pre-standard, all compilers |

### Audit Logging Pattern ([ENG-6.7](laws/engineering/eng-6-security.md))

```cpp
// COMPLIANT — structured audit record with call-site provenance
// per [ENG-6.7](laws/engineering/eng-6-security.md) (Audit Trail)
struct AuditEntry {
    std::string_view   event;
    std::string_view   user_id;
    std::source_location location;
    std::chrono::system_clock::time_point timestamp;
};

void record_pnr_change(std::string_view pnr, std::string_view agent,
    std::source_location loc = std::source_location::current()) {
    AuditEntry e{ "PNR_MODIFIED", agent, loc,
                  std::chrono::system_clock::now() };
    audit_sink_.write(e);  // ✅ full provenance: file, line, function, time
}
```

**Thread safety:** `std::source_location` values are value types — safe to copy across
threads. The `current()` call itself is evaluated at compile time at the call expression.

---

## constinit

Per [ENG-3.1](laws/engineering/eng-3-code-quality.md) (Complexity), `constinit` prevents
the **static initialization order fiasco** for mutable globals that must be
constant-initialized before first use. Core Guidelines Con.5 (use constexpr for values).

### constinit vs. constexpr vs. const

| Specifier | Value mutable after init? | Must init at compile time? | Use when |
|---|---|---|---|
| `constexpr` | ❌ immutable | ✅ yes | Compile-time constants |
| `constinit` | ✅ mutable | ✅ yes | Mutable globals needing safe init order |
| `const` | ❌ immutable | ❌ can be runtime | Runtime-determined constants |

### Initialization Order Fiasco Prevention

The static initialization order fiasco occurs when a global in one TU depends on a
global in another TU that may not be initialized yet:

```cpp
// NON-COMPLIANT — undefined initialization order across TUs
// counter.cpp
int g_flight_count = 0;                      // zero-initialized, fine

// stats.cpp
extern int g_flight_count;
int g_active_routes = g_flight_count + 10;   // ❌ g_flight_count may not be
                                              //    initialized yet (SIOF)
```

### constinit for Mutable Globals

```cpp
// COMPLIANT — constinit guarantees zero-initialization before any TU uses it
constinit int g_flight_count = 0;            // ✅ compile-time init guaranteed
constinit std::atomic<int> g_active_routes{0}; // ✅ atomic + constinit

// Mutated at runtime — constinit does NOT prevent this
void record_departure() { ++g_flight_count; }

// COMPLIANT — constinit constexpr: immutable compile-time constant
// (redundant but explicit)
constinit constexpr int MAX_GATES = 120;     // ✅ same as constexpr alone
```

### Compile-Time Enforcement

`constinit` is a **compile-time contract**: the compiler rejects the declaration if
the initializer cannot be evaluated at compile time:

```cpp
int runtime_value();

constinit int g_bad = runtime_value();  // ❌ compile error — not constexpr-friendly
constexpr int g_good = 42;              // ✅ fine

// NON-COMPLIANT — using a function-local static to work around SIOF
// (Meyers singleton) — valid C++11 but adds overhead; prefer constinit for globals
int& flight_count() {
    static int count = 0;               // ⚠️ thread-safe in C++11 but adds branch
    return count;
}
```

**[ENG-3.1](laws/engineering/eng-3-code-quality.md) rule:** Prefer `constinit` over
Meyers-singleton workarounds for mutable globals with constant initial values.

---

## std::atomic_ref

Per [ENG-6.1](laws/engineering/eng-6-security.md) (Security — thread safety),
`std::atomic_ref<T>` provides atomic operations on an existing non-atomic object
without changing its type or layout. Core Guidelines CP.8 (do not try to use
`volatile` for synchronization).

### Primary Use Case: ABI-Safe Brownfield Atomics

Adding `std::atomic<T>` members to a shared struct breaks ABI (different size/alignment).
`std::atomic_ref` atomises access without touching the struct definition:

```cpp
// Existing ABI-stable struct — cannot add std::atomic members without breaking ABI
struct FlightCounter {       // shared via JNI / shared memory / IPC
    int  active_flights;     // must stay plain int for ABI compatibility
    int  cancelled_flights;
};

// COMPLIANT — atomic_ref wraps the existing int; FlightCounter layout unchanged
void increment_active(FlightCounter& fc) {
    std::atomic_ref<int> ref{fc.active_flights};  // ✅ atomic access, no ABI change
    ref.fetch_add(1, std::memory_order_relaxed);
}

// NON-COMPLIANT — data race: plain increment without synchronization
void increment_active_unsafe(FlightCounter& fc) {
    ++fc.active_flights;   // ❌ data race if called from multiple threads
}
```

### Constraints

`std::atomic_ref<T>` requires:
1. `T` is **trivially copyable**
2. The referred object is **suitably aligned** (`alignof(T)` ≥ `atomic_ref<T>::required_alignment`)
3. The **underlying object must outlive every `atomic_ref` that wraps it** — dangling refs are UB
4. All concurrent accesses to the same object must go through `atomic_ref` — mixing atomic and
   non-atomic access is UB

```cpp
// COMPLIANT — alignment check; place at struct definition site, not point of use
// This catches platform-specific alignment requirements at compile time.
static_assert(alignof(int) >= std::atomic_ref<int>::required_alignment,
              "int not suitably aligned for atomic_ref on this platform");
```

### atomic_ref vs. std::atomic vs. volatile

| | `std::atomic<T>` | `std::atomic_ref<T>` | `volatile T` |
|---|---|---|---|
| Owns the value | ✅ | ❌ (references existing) | ✅ |
| ABI-compatible | ❌ changes layout | ✅ no layout change | ✅ |
| Thread-safe | ✅ | ✅ | ❌ (not for sync) |
| Memory order control | ✅ | ✅ | ❌ |
| Brownfield-safe | ❌ | ✅ | ❌ |

**[ENG-6.1](laws/engineering/eng-6-security.md) rule:** Never use `volatile` for thread
synchronization. Use `std::atomic` for new code; use `std::atomic_ref` when ABI
constraints prevent changing existing struct member types.





- `ref-cpp20-features-part1.md` — modules, ranges, std::span, spaceship operator
- `ref-cpp20-features-part2.md` — coroutine generators (`co_yield`), calendar/timezone

