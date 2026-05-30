---
cpp_version_min: 11
cpp_version_note: >-
  Type safety and const-correctness; C++11 baseline with C++17 std::string_view noted.
avatar: cpp
---

# C++ Avatar Reference: Core Type Safety

---

## Const Correctness Philosophy

Per [ENG-3.1](laws/engineering/eng-3-code-quality.md), const correctness is not just a rule — it is a **design philosophy**. In a const-correct codebase, the type system enforces at compile time which code paths can modify state and which cannot. This is the C++ equivalent of Java's "defensive immutability" principle, but enforced by the compiler, not by convention.

> **For Java developers:** Think of `const` as a compiler-enforced version of `@Immutable` or `@ReadOnly` annotations. The difference is that C++ enforces `const` at compile time — if you mark a parameter `const&`, the compiler will not let you accidentally modify it.

### The Const-by-Default Rule

**Every declaration starts as `const` unless mutation is required:**

```cpp
// PARAMETERS — const reference is the default
void displayFlight(const Flight& flight);           // why: read-only access
void updateGate(Flight& flight, std::string gate);  // mutation needed — non-const ref

// MEMBER FUNCTIONS — const unless they modify state
class FlightService {
public:
    Flight find(FlightId id) const;                 // why: does not modify service state
    std::vector<Flight> search(const Query& q) const; // why: query is read-only
    void cancel(FlightId id);                       // modifies state — non-const

    // why: const overloads let const and non-const callers both work
    const Seat& getSeat(SeatId id) const;
    Seat& getSeat(SeatId id);
};

// LOCAL VARIABLES — const unless reassigned
const auto flight = service.find(id);               // why: not reassigned after init
const auto& passengers = flight.passengers();       // why: read-only reference
auto gate = flight.gate();                          // non-const — will be reassigned
gate = selectNewGate(flight);

// RETURN TYPES — return by value (const-by-default after move)
Flight FlightService::find(FlightId id) const {
    return repository_.load(id);                    // why: return by value, caller decides mutability
}
```

### Const Propagation Through Layers

Const correctness propagates from parameters through function calls. A `const` reference at the API boundary guarantees that no called function can modify the object:

```cpp
// API layer — const reference guarantees no mutation
void printBoardingPass(const Reservation& res) {
    // All of these are safe because res is const:
    auto name = res.passengerName();     // calls const member function
    auto seat = res.seatAssignment();    // calls const member function
    // res.cancel();                     // COMPILE ERROR — cancel() is non-const
}
```

### Const Correctness Checklist

| Location | Default | Exception |
|----------|---------|-----------|
| Function parameters (large types) | `const T&` | `T&` only if mutation is the function's purpose |
| Function parameters (small types) | `T` (by value) | `const T&` if you want to avoid copies of large small-types |
| Member functions | `const` | Non-const only if the function modifies `*this` |
| Local variables | `const auto` | `auto` only if the variable is reassigned |
| Pointers | `const T*` | `T*` only if the pointee is modified |
| Return types | By value (let caller decide) | `const T&` for accessor returning member reference |
| Loop variables | `const auto&` | `auto&` only if modifying elements in-place |
| Lambda captures | `[x]` (const copy by default) | `[&x]` only if the lambda needs to modify or observe changes |

### Common Const Mistakes (Java Developer Traps)

```cpp
// MISTAKE 1: Forgetting const on parameters
void printFlight(Flight& f);          // ❌ Why non-const? Implies mutation.
void printFlight(const Flight& f);    // ✅ Clearly read-only

// MISTAKE 2: Forgetting const on member functions
class FlightService {
    Flight find(FlightId id);          // ❌ Can't call on a const FlightService
    Flight find(FlightId id) const;    // ✅ Works for both const and non-const
};

// MISTAKE 3: Using non-const local when value doesn't change
auto flight = service.find(id);        // ❌ Accidentally allows flight = otherFlight;
const auto flight = service.find(id);  // ✅ Compiler prevents accidental reassignment

// MISTAKE 4: Returning non-const reference to internals
class Reservation {
    std::string& name() { return name_; }         // ❌ Exposes mutable internal state
    const std::string& name() const { return name_; } // ✅ Read-only access
};
```

> **Const-correctness is viral** — once you make one function `const`, the compiler forces every function it calls to also be `const`-correct. This is a feature, not a bug. It means adding `const` to a codebase reveals hidden mutation paths that were invisible before.

---

## Implicit Conversions and Type Safety

Per [ENG-3.1](laws/engineering/eng-3-code-quality.md) (Complexity Limits) and [ENG-6.1](laws/engineering/eng-6-security.md) (Security by Design), implicit conversions are a major source of silent bugs in C++.

### `explicit` Governance

```cpp
// NON-COMPLIANT — implicit conversion from int to FlightId
class FlightId {
    int value_;
public:
    FlightId(int v) : value_{v} {}  // ❌ implicit — allows FlightId f = 42;
};

void book(FlightId id);
book(42);  // ❌ compiles — is 42 a flight ID? A seat count? A gate number?

// COMPLIANT — explicit prevents accidental conversion
class FlightId {
    int value_;
public:
    explicit FlightId(int v) : value_{v} {}  // ✅ requires FlightId{42}
};

book(FlightId{42});  // ✅ intent is clear
```

**Rules:**
- **All** single-argument constructors must be `explicit` unless implicit conversion is intentionally designed (document why)
- All conversion operators (`operator bool()`, `operator int()`) must be `explicit`
- Enable `-Wconversion` and `-Wsign-conversion` in CI — treat as errors

### Copy Elision and Return Value Optimization

Per [ENG-3.1](laws/engineering/eng-3-code-quality.md), understand when the compiler eliminates copies:

```cpp
// Guaranteed copy elision (C++17) — no copy/move constructor needed
FlightPlan create_plan() {
    return FlightPlan{origin, dest};  // ✅ always elided since C++17
}

// NRVO (Named Return Value Optimization) — likely but NOT guaranteed
FlightPlan create_plan(bool domestic) {
    FlightPlan plan;
    if (domestic) {
        plan = make_domestic();
    } else {
        plan = make_international();
    }
    return plan;  // ⚠️ NRVO applies when there is ONE local variable returned
}

// DON'T std::move a local return — it PREVENTS elision!
FlightPlan create_plan() {
    FlightPlan plan{origin, dest};
    return std::move(plan);  // ❌ prevents NRVO — compiler can't elide a moved-from
}
```

**Rules:**
- Return local variables by name — do NOT `std::move` them (the compiler applies NRVO or implicit move)
- For prvalue returns (`return FlightPlan{...}`), elision is guaranteed since C++17
- `std::move` on return is only correct when returning a function parameter (not a local)

---

## Cast Governance

Per [ENG-6.1](laws/engineering/eng-6-security.md) and [ENG-3.1](laws/engineering/eng-3-code-quality.md), every type cast must use a named C++ cast — never a C-style cast. **Java developers:** In Java, `(Flight) obj` either succeeds or throws `ClassCastException` — it is always safe. In C++, a C-style cast can silently perform a `reinterpret_cast` which is **undefined behavior**. There is no safety net.

### Cast Decision Table

| Cast | Purpose | Safety | Java Equivalent |
|------|---------|--------|-----------------|
| `static_cast<T>(expr)` | Convert between related types (numeric, up/downcast in hierarchy) | **Safe** — compile-time checked | `(Type) expr` (safe part) |
| `dynamic_cast<T*>(ptr)` | Runtime-checked downcast in polymorphic hierarchy | **Safe** — returns `nullptr` on failure | `instanceof` + cast |
| `const_cast<T>(expr)` | Add or remove `const`/`volatile` qualifier | **Dangerous** — modifying a truly `const` object is UB | No equivalent — Java `final` cannot be cast away |
| `reinterpret_cast<T>(expr)` | Bit reinterpretation between unrelated types | **Very dangerous** — almost always UB unless casting to/from `char*`/`std::byte*` | No equivalent |
| `(Type) expr` (C-style) | **BANNED** — performs the first cast that compiles from: `const_cast`, `static_cast`, `reinterpret_cast` | **Unpredictable** — may silently do `reinterpret_cast` | Looks like Java cast but is NOT safe |

### Rules

1. **NEVER use C-style casts in C++ code.** Enable `-Wold-style-cast` to flag them. In legacy code, migrate C-style casts to named casts on each file touch (Boy Scout Rule per [ENG-1.4](laws/engineering/eng-1-core-principles.md)).

2. **Prefer `static_cast`** for numeric conversions, enum conversions, and upcasts/downcasts when the type is known at compile time.

3. **Use `dynamic_cast` sparingly** — it requires RTTI and indicates a design that may benefit from the Visitor pattern or `std::variant`. If you find yourself writing chains of `dynamic_cast`, the design needs refactoring per [ENG-3.1](laws/engineering/eng-3-code-quality.md).

4. **`const_cast` is a last resort.** The only acceptable use is calling a legacy C API that takes a non-const pointer but does not modify the data:

```cpp
// ACCEPTABLE — legacy C API that should be const but isn't
extern "C" int legacy_validate(char* data, size_t len);  // C API, doesn't modify

void validate(const std::string& input) {
    // why: const_cast to call a legacy API that lacks const-correctness
    legacy_validate(const_cast<char*>(input.c_str()), input.size());
}
```

```cpp
// ❌ NEVER DO THIS — modifying a truly const object is UB
const Flight flight{"AA100"};
const_cast<Flight&>(flight).setGate("B12");  // ❌ UB — flight is genuinely const
```

5. **`reinterpret_cast` must be confined to unsafe boundary modules** per the Safety and Ownership governance. It is only safe for pointer↔integer round-trips and accessing object representations via `char*`/`std::byte*`.

### C-Style Cast Migration Example

```cpp
// BEFORE — C-style cast (banned)
double altitude_ft = (double)altitude_m * 3.281;      // ❌ C-style
FlightBase* base = (FlightBase*)derived;               // ❌ C-style — could reinterpret
const char* raw = (const char*)&data;                  // ❌ C-style — could reinterpret

// AFTER — named casts (compliant)
double altitude_ft = static_cast<double>(altitude_m) * 3.281;   // why: numeric conversion
FlightBase* base = static_cast<FlightBase*>(derived);            // why: upcast in known hierarchy
const char* raw = reinterpret_cast<const char*>(&data);          // why: object representation access — explicit intent
```

---


---

## Interface Design Rules (Core Guidelines I.xx)

<!-- Adapted from C++ Core Guidelines. Copyright Standard C++ Foundation. Internal use only. https://github.com/isocpp/CppCoreGuidelines -->

Per [ENG-6.1](laws/engineering/eng-6-security.md) and [ENG-3.1](laws/engineering/eng-3-code-quality.md),
well-designed interfaces prevent ownership confusion, null-dereference, and
parameter-count complexity.

### I.1 — Make Interfaces Explicit

State preconditions in code with `Expects()` from the GSL so violations fail
fast in debug builds rather than producing silent UB:

```cpp
#include <gsl/gsl>

// COMPLIANT — machine-checked contract
Booking create_booking(const PNR& pnr, const FlightId& id) {
    Expects(!pnr.value.empty());  // ✅ asserts in debug; documents invariant
    Expects(id.value > 0);
    return Booking{pnr, id};
}

// NON-COMPLIANT — caller has no signal on invalid input
Booking create_booking(const PNR& pnr, const FlightId& id) {
    return Booking{pnr, id};  // ❌ silent misbehaviour
}
```

Use `Ensures()` for postconditions on return values.

### I.3 — Avoid Singletons — Avoid Singletons

Singletons create hidden global state, prevent testing, and cause
static-initialisation-order fiasco. Prefer dependency injection:

```cpp
// NON-COMPLIANT — hidden state, SIOF risk, untestable
static FlightCache& instance() { static FlightCache c; return c; } // ❌

// COMPLIANT — injected; mockable in tests
class BookingService {
    const FlightCache& cache_;
public:
    explicit BookingService(const FlightCache& c) : cache_(c) {} // ✅
};
```

### I.11 — Never Transfer Ownership by Raw Pointer

Raw pointer parameters imply non-ownership. Transfer ownership via
`std::unique_ptr<T>`; pass non-owning views via `std::span<T>`:

```cpp
FlightRecord* load(int id);                     // ❌ ambiguous
std::unique_ptr<FlightRecord> load(int id);     // ✅ caller owns
std::span<const FlightRecord>  view(int id);    // ✅ non-owning
```

### I.12 — Use `not_null<T*>` for Never-Null Pointers

`gsl::not_null<T*>` enforces the invariant at construction, eliminating
null-check boilerplate at every call site:

```cpp
// COMPLIANT — null caught at construction, not scattered at every use
void process(gsl::not_null<const FlightRecord*> rec) {
    rec->validate();  // ✅ no null check needed
}

// NON-COMPLIANT — defensive check duplicated across all callers
void process(const FlightRecord* rec) {
    if (!rec) return;  // ❌ repeated at every call site
    rec->validate();
}
```

### I.23 — Keep Parameter Count Low (Use Aggregates)

Functions with more than four parameters are error-prone. Group related
parameters into a named aggregate:

```cpp
// NON-COMPLIANT — 6 positional args; adjacent swaps are silent bugs
Booking book(int flight_id, int row, char col,
             int pax, bool premium, bool meal); // ❌

// COMPLIANT — aggregate makes names explicit at the call site
struct BookingRequest {
    FlightId flight_id;  SeatLocation seat;
    int  pax_count   = 1;
    bool is_premium  = false;
    bool needs_meal  = false;
};
Booking book(const BookingRequest& req);  // ✅
```

---


---

## See Also

- [Core Modern Idioms](ref-core-modern-idioms.md)
