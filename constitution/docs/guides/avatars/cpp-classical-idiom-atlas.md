# C++ Classical Idiom Atlas

> **Purpose:** A vocabulary bridge for engineers reading pre-modern C++ code in AA's legacy
> and brownfield codebases. Maps 1990s and early-2000s C++ idiom vocabulary — Coplien patterns,
> GoF in C++, pre-STL techniques, CORBA-era structures, and early template metaprogramming —
> to their modern C++ equivalents and their governance status in the AA avatar.
>
> **Audience:** Engineers working in legacy tier (SPEClient), brownfield tier (herc-odyssey-linux),
> or transitional tier (CWR, IOC_ALP) who encounter patterns they recognise but cannot name.
>
> **Laws:** [ENG-10.1](../../laws/engineering/eng-10-constitution.md),
> [ENG-3.1](../../laws/engineering/eng-3-code-quality.md) (Complexity)
>
> **How to use:** Find the pattern name or code shape you're looking at. The atlas gives you
> the classical name, the modern equivalent, governance status, and where to find examples.

---

## Part I — Coplien Idioms (C++98-era, *Advanced C++ Programming Styles and Idioms*, 1992)

These patterns were named and systematised by James O. Coplien. They are the vocabulary of
C++98 object design. AA engineers encounter them in SPEClient, herc-odyssey-linux, and in
older sections of CWR.

### Handle/Body (Pimpl Idiom)

**What it looks like in legacy code:**
```cpp
// Header — only a pointer to the "body"
class FlightPlan {
public:
    explicit FlightPlan(int waypoints);
    ~FlightPlan();
    void addWaypoint(const char* name);
private:
    struct Impl;          // forward declaration — body is hidden
    Impl* impl_;          // raw pointer to implementation
};
```

**Classical name:** Handle/Body — the "handle" (`FlightPlan`) holds a pointer to the "body"
(`Impl`) which carries all the state. Also called "Compilation Firewall" because the body's
details are hidden from the header, preventing recompilation cascades.

**Modern equivalent:** The same pattern, modernized with `std::unique_ptr<Impl>`:
```cpp
#include <memory>
class FlightPlan {
public:
    explicit FlightPlan(int waypoints);
    ~FlightPlan();                        // must be out-of-line (unique_ptr requires complete Impl)
    void addWaypoint(std::string_view name);
private:
    struct Impl;
    std::unique_ptr<Impl> impl_;          // ★ C++11
};
```

**Governance status:** ✅ RECOMMENDED. Per Core Guidelines I.22 (avoid complex initialisation
of global objects) and I.26 (prefer value-like APIs). The Pimpl idiom is the AA-preferred
technique for hiding platform-specific or third-party headers from public API surfaces.

**Reference:** `ref-advanced-patterns.md` §Pimpl

---

### Envelope/Letter

**What it looks like in legacy code:**
```cpp
// Envelope — value-type wrapper that delegates to a letter via pointer
class Animal {
public:
    Animal(const char* type);
    void speak() const;       // delegates to letter_->speak()
    Animal(const Animal&);    // copies the letter
    Animal& operator=(const Animal&);
    ~Animal();
private:
    AnimalImpl* letter_;      // polymorphic "letter" — heap-allocated
};
```

**Classical name:** Envelope/Letter. The "envelope" (`Animal`) is a concrete value type with
regular copy semantics. The "letter" (`AnimalImpl*`) is a polymorphic base class on the heap.
The envelope hides the pointer entirely — callers see a value, not a pointer.

**Modern equivalent:** Combine Handle/Body with `std::shared_ptr` (for shared ownership) or
`std::unique_ptr` (for unique ownership). For true polymorphic value semantics in C++17+, use
`std::any` or a discriminated union via `std::variant`. For performance-critical C++20, use
`std::unique_ptr<Base>` with explicit `clone()` for copy semantics.

**Governance status:** ⚠️ LEGACY PATTERN — recognise and preserve. Avoid creating new
Envelope/Letter classes; prefer `std::unique_ptr<Base>` with explicit ownership. If you must
copy-construct an Envelope, be certain the Letter's copy semantics are correct.

---

### Curiously Recurring Template Pattern (CRTP)

**What it looks like in legacy code:**
```cpp
// Base class is templated on the derived class — backwards!
template <typename Derived>
class Comparable {
public:
    bool operator<(const Derived& rhs) const {
        return static_cast<const Derived*>(this)->lessThan(rhs);
    }
    bool operator>(const Derived& rhs) const { return rhs < *static_cast<const Derived*>(this); }
};

class FlightId : public Comparable<FlightId> {
public:
    bool lessThan(const FlightId& rhs) const { return number_ < rhs.number_; }
private:
    int number_;
};
```

**Classical name:** Curiously Recurring Template Pattern (CRTP), coined by Coplien (1995) in
the *C++ Report*. Provides static (compile-time) polymorphism without virtual dispatch. Used
in SPEClient for zero-overhead "mixin" behaviour in performance-critical scheduling loops.

**Modern equivalent:** C++20 Concepts allow the same static polymorphism more transparently:
```cpp
// ★ C++20
template <typename T>
concept Orderable = requires(T a, T b) { { a < b } -> std::same_as<bool>; };
```
For C++11/14 transitional tier, CRTP remains the canonical approach.

**Governance status:** ✅ ACTIVE PATTERN — still the correct technique for C++98/11/14 static
polymorphism. Route to legacy and brownfield tiers via `AVATAR-RAG-INDEX.yaml` `prefer` list
(required when `ENG-3.1-crtp.md` is created, ESE R8-6).

---

### Counted Body (Reference-Counted Handle)

**What it looks like in legacy code:**
```cpp
class RouteData {
public:
    RouteData();
    RouteData(const RouteData&);      // increments count_
    ~RouteData();                     // decrements; deletes when 0
    RouteData& operator=(const RouteData&);
private:
    int* count_;    // heap-allocated reference count
    Impl* body_;    // shared heap-allocated body
};
```

**Classical name:** Counted Body. A Handle/Body where multiple handles share the same body via
a reference count. This is a manual implementation of shared ownership — predating
`std::shared_ptr` by more than a decade.

**Modern equivalent:** `std::shared_ptr<Impl>` — strictly superior; use it. The Counted Body
pattern carries the same risks as manual `new`/`delete` with added complexity. Any legacy
Counted Body should be considered a candidate for `shared_ptr` migration during the next
brownfield modernization pass.

**Governance status:** ⚠️ LEGACY — recognise and flag for migration. Per Core Guidelines R.22
(use `make_shared` to construct shared_ptrs). Do not write new Counted Body classes.

---

### Functor Callbacks (Function Objects)

**What it looks like in legacy code:**
```cpp
struct ByDepartureTime {
    bool operator()(const Flight& a, const Flight& b) const {
        return a.departureTime() < b.departureTime();
    }
};

std::sort(flights.begin(), flights.end(), ByDepartureTime());
```

**Classical name:** Functor / Function Object. A struct or class with `operator()` used as a
callable. Predates lambdas. In 1990s C++, functors were the only way to pass parameterised
behaviour to STL algorithms.

**Modern equivalent:** Lambda expressions (★ C++11):
```cpp
std::sort(flights.begin(), flights.end(),
    [](const Flight& a, const Flight& b) { return a.departureTime() < b.departureTime(); });
```

**Governance status:** ✅ BOTH VALID — functors are still correct C++; lambdas are preferred
for new code. Named functors (like `ByDepartureTime`) can be advantageous for re-use and
readability. When reading legacy code, a struct with `operator()` is always a functor — not a
bug, not a code smell.

---

## Part II — Pre-STL and Early STL Patterns

Patterns from the era before the C++ Standard Library was universally available or reliably
implemented (pre-MSVC 6.0 / pre-GCC 3.x).

### Manual String Management (`char*` + `new[]`)

**What it looks like:**
```cpp
class Airport {
public:
    explicit Airport(const char* iata) : code_(new char[strlen(iata) + 1]) {
        strcpy(code_, iata);
    }
    ~Airport() { delete[] code_; }
private:
    char* code_;          // manually heap-managed string
};
```

**Why it exists:** Pre-MSVC 6.0 `std::string` had inconsistent exception guarantees and ABI
instability across DLL boundaries. Enterprise shops often avoided it in API signatures.

**Modern equivalent:** `std::string` (C++98/03, once reliable implementations shipped) or
`std::string_view` for non-owning references (★ C++17).

**Governance status:** 🔴 DANGEROUS LEGACY — every class doing manual `char*` management
without a complete Rule of Three is a use-after-free or double-free waiting to happen. Flag
for Rule of Three audit. Migrate to `std::string` in the next modernization pass.

**See:** `ref-brownfield-survival.md` §Rule of Three, `ENG-6.1-const-char-lifetime.md`

---

### Output-Parameter Returns

**What it looks like:**
```cpp
// Return value is an error code; result returned via pointer
int getFlightStatus(int flightId, FlightStatus* out_status);
```

**Why it exists:** C99/C++98 conventions from COM, POSIX, and Win32 APIs. Predates
`std::optional`, `std::expected`, and multi-return idioms. Still dominant in JNI and OS-layer
APIs that AA code calls.

**Modern equivalent:** `std::optional<FlightStatus>` (★ C++17) or `std::expected<FlightStatus,
Error>` (★ C++23). For transitional tier (C++14): `std::pair<bool, FlightStatus>` or a
`Result<T, E>` alias wrapping `std::pair`.

**Governance status:** ⚠️ AT API BOUNDARY — preserve output-parameter APIs when the function
is an existing external contract (JNI, OS call, legacy ABI). Use modern return types for new
internal functions.

---

### Sentinel / Magic-Value Returns

**What it looks like:**
```cpp
int findSeat(int flightId, const char* pnr);
// Returns -1 if not found; ≥0 if found
```

**Modern equivalent:** `std::optional<int>` communicates intent explicitly.

**Governance status:** ⚠️ LEGACY — recognise and document the sentinel value at the call
site. Migrate to `std::optional` when touching the function.

---

## Part III — Pre-C++11 Template Metaprogramming Vocabulary

These techniques are in templates-heavy C++98/03 libraries in AA's codebase. They are the
predecessors of C++11 `<type_traits>`, C++14 `std::enable_if_t`, and C++20 Concepts.

### Type Lists (Loki `TypeList`)

**What it looks like:**
```cpp
// Loki-style TypeList
struct NullType {};
template <class T, class U> struct Typelist { typedef T Head; typedef U Tail; };

// A list of three types:
typedef Typelist<int, Typelist<double, Typelist<char, NullType>>> MyTypes;
```

**Classical name:** TypeList, from Alexandrescu *Modern C++ Design* (2001), implemented in
the Loki library.

**Modern equivalent:** Variadic templates and `std::tuple<int, double, char>` (★ C++11).
`std::variant<int, double, char>` for discriminated unions (★ C++17).

**Governance status:** ⚠️ LEGACY — if you encounter a `Typelist` in AA code, it is Loki or
Loki-derived. Do not extend TypeList-based code; migrate to `std::tuple` / `std::variant`.

---

### Enable-If via Specialization (Pre-`std::enable_if`)

**What it looks like:**
```cpp
// Compile-time dispatch by type property — manual specialization guard
template <bool, class T = void> struct EnableIf {};
template <class T> struct EnableIf<true, T> { typedef T type; };

// Usage: "this function only exists for integral types"
template <class T>
typename EnableIf<IsIntegral<T>::value, T>::type
safeAdd(T a, T b);
```

**Classical name:** Enable-if via partial specialization. Predates `std::enable_if` (C++11) and
Concepts (C++20). The same technique, with different syntax.

**Modern equivalent:** `std::enable_if_t<std::is_integral_v<T>, T>` (★ C++14) or a Concept
constraint (★ C++20).

**Governance status:** ✅ RECOGNISE AND MAP — when modernizing C++98 template code, map old
`EnableIf` to `std::enable_if_t` first (same semantics, standard vocabulary), then migrate to
Concepts if moving to C++20.

---

### Tag Dispatching

**What it looks like:**
```cpp
struct random_access_tag {};
struct forward_tag {};

template <class Iter>
void advanceImpl(Iter& it, int n, random_access_tag) { it += n; }
template <class Iter>
void advanceImpl(Iter& it, int n, forward_tag) { while (n--) ++it; }

template <class Iter>
void advance(Iter& it, int n) {
    advanceImpl(it, n, typename IterTraits<Iter>::category());
}
```

**Classical name:** Tag dispatching. Selects a function overload at compile time by passing
a *type-encoding tag* as a parameter. Used extensively in STL iterator implementations.

**Modern equivalent:** `if constexpr` (★ C++17) or Concept constraints (★ C++20) express the
same compile-time selection more readably.

**Governance status:** ✅ VALID LEGACY PATTERN — understand it when reading; prefer `if
constexpr` or Concepts in new code. Do not refactor working tag-dispatch code unless the
surrounding function is being substantially rewritten.

---

## Part IV — CORBA / COM-Era Patterns

AA aviation systems were often built against CORBA or COM middleware in the 1990s–2000s.
These patterns survive in legacy codebases and in JNI boundary code.

### Reference-Counted COM-Style Interfaces

**What it looks like:**
```cpp
class IFlightDataSource {
public:
    virtual void AddRef() = 0;
    virtual void Release() = 0;
    virtual HRESULT GetFlightStatus(int flightId, FlightStatus* pStatus) = 0;
};
```

**Why it exists:** COM's `IUnknown` requires `AddRef`/`Release` for reference counting across
DLL boundaries, and `HRESULT` as the universal error return.

**Governance status:** ⚠️ PRESERVE AT ABI BOUNDARY — do not remove `AddRef`/`Release` from
COM interfaces; they are contractual. In implementation classes, wrap with a smart pointer
adapter. `HRESULT`-returning functions should be wrapped in helpers that translate to
`std::expected` or `std::optional` at the AA code boundary.

---

### `volatile` for Threading (Pre-C++11)

**What it looks like:**
```cpp
volatile bool g_shutdown = false;      // thread A sets; thread B polls

void workerThread() {
    while (!g_shutdown) { /* work */ }
}
```

**Why it exists:** Before C++11's memory model, `volatile` was (incorrectly) used as a
threading signal because it prevented compiler optimisation of the variable read. On some
compilers/platforms it happened to work.

**Modern equivalent:** `std::atomic<bool> g_shutdown{false}` (★ C++11) with
`memory_order_relaxed` for the poll load. The `volatile`-for-threading pattern is undefined
behaviour under the C++11 memory model.

**Governance status:** 🔴 NON-COMPLIANT — any `volatile` flag used for inter-thread
communication is a defect. Replace with `std::atomic<bool>` or, for C++20 teams, `std::stop_token`.

**See:** `ENG-6.1-thread-stop-flag.md`

---

## Part V — Exception Safety Vocabulary (Sutter)

These terms appear in code comments and design documents written by engineers who read
Herb Sutter's *Exceptional C++* (1999). Knowing the vocabulary unlocks the intent.

| Term | Meaning | Code Signal |
|------|---------|-------------|
| **Basic guarantee** | If the operation throws, no resources leak and all invariants are preserved. State may be different but valid. | Destructor + RAII; no guarantee of previous state |
| **Strong guarantee** | If the operation throws, state is *unchanged* — as if the operation never happened. Commit-or-rollback. | Copy-and-swap in `operator=`; `std::vector::push_back`-style |
| **Nothrow guarantee** | The operation never throws. | `noexcept` specifier (★ C++11); `throw()` in C++98 (deprecated) |
| **Copy-and-swap** | Implement `operator=` by constructing a copy in a local, then swapping. Strong guarantee at the cost of one extra allocation. | `void swap(T&, T&) noexcept; T& operator=(T rhs) { swap(*this, rhs); return *this; }` |
| **Exception-neutral** | A template or utility class propagates exceptions from its type parameter without modifying them. | `std::vector<T>` is exception-neutral w.r.t. `T::T(T&&)` |

**Governance status:** These vocabulary terms should appear in comments when writing resource-
owning classes. The avatar's `ref-brownfield-survival.md` Rule of Three section and future
`ref-core-type-safety.md` exception safety section use this vocabulary.

---

## Quick Lookup — "I See This Shape, What Is It?"

| Code shape you see | Classical name | Modern equivalent | Governance |
|---|---|---|---|
| `struct Impl; Impl* impl_` | Handle/Body (Pimpl) | `unique_ptr<Impl>` | ✅ Preferred with smart ptr |
| Class with `operator()` | Functor | Lambda | ✅ Both valid |
| `Base<Derived> : Base<Derived>` | CRTP | Concepts (C++20) | ✅ Valid for C++98/14 |
| `class Foo { Foo(const Foo&); ~Foo(); }` with explicit copy + dtor | Rule of Three | Rule of Five + smart ptrs | ✅ Correct for C++98 |
| `Foo* body_; int* count_` | Counted Body | `shared_ptr<Body>` | ⚠️ Migrate |
| `struct TypeList<T, TypeList<U, NullType>>` | Loki TypeList | `std::tuple<T,U>` | ⚠️ Migrate |
| `template<bool,class T> EnableIf {}` | Pre-C++11 enable_if | `std::enable_if_t` / Concepts | ✅ Map to standard |
| `typename IterTraits<I>::tag{}` parameter | Tag dispatching | `if constexpr` / Concepts | ✅ Preserve in working code |
| `volatile bool flag` used between threads | Volatile-for-threading anti-pattern | `std::atomic<bool>` | 🔴 Defect — fix |
| `AddRef() / Release()` methods | COM `IUnknown` | Smart pointer adapter | ⚠️ Preserve at ABI |
| `int func(T* out)` returns error code | Output-parameter return | `std::optional<T>` | ⚠️ Migrate on touch |

---

*Last updated: 2026-04-27. Per ENG-10.1, extend this atlas when ESE adds new legacy tier
reference content or when R8's CRTP routing task (ESE R8-6) is completed.*
