---
cpp_version_min: 11
cpp_version_note: >-
  Object design rehabilitation using move semantics and RAII (C++11+).
avatar: cpp
---

# C++ Avatar Reference: Object Design Rehabilitation

---

## Object Design Rehabilitation

> Per [ENG-3.1](laws/engineering/eng-3-code-quality.md) and [ENG-2.1](laws/engineering/eng-2-architecture.md), legacy C++ codebases frequently suffer from object design patterns that were considered best practice in the 1990s but are now recognized as sources of bugs, complexity, and performance problems. This section provides a systematic approach to identifying and rehabilitating these design debt vectors.

### Summary Table

| # | Design Debt Vector | Recognition | Severity | Safe First Step |
|---|-------------------|-------------|----------|----------------|
| 1 | Multiple Inheritance Diamonds | `dynamic_cast` failures, unexpected object sizes | CRITICAL | Extract pure interface for shared base |
| 2 | Operator Overloading Hiding Cost | `a + b` triggers DB lookup or deep copy | HIGH | Rename to explicit function (`merge()`) |
| 3 | Implicit Conversions | Wrong type compiles silently | HIGH | Add `explicit` to all single-arg constructors |
| 4 | Copy Semantics Performance | Excessive time in copy constructors | HIGH | Add move constructor + `noexcept` |
| 5 | Over-Reliance on Virtual Functions | 20+ overrides, `dynamic_cast` chains | MEDIUM | CRTP for hot paths, keep virtual for plugins |
| 6 | Missing Move Semantics | Pre-C++11 classes with expensive copy | HIGH | Add `= default` move ops or implement manually |

### 1. Multiple Inheritance Diamond Problems

**Recognition:**
- Class `D` inherits from `B` and `C`, which both inherit from `A`
- `dynamic_cast<A*>(d)` returns ambiguous result
- `sizeof(D)` is larger than expected (multiple copies of `A`'s data)
- Compiler warnings about ambiguous base class access

**Why it exists:** Multiple inheritance was promoted as a way to combine behaviors. Without careful design, shared ancestors create diamonds.

**Fix:** Extract a pure interface (no data members) for the shared base. Virtual inheritance only as a last resort — it adds runtime overhead and complexity.

```cpp
// BEFORE — Diamond problem
class Printable {
protected:
    std::string format_;  // DATA in base — causes diamond
public:
    virtual void print() const;
};

class FlightLog : public Printable { /* ... */ };
class CrewLog : public Printable { /* ... */ };

class CombinedLog : public FlightLog, public CrewLog {
    // TWO copies of format_! Ambiguous access.
};

// AFTER — Composition (preferred)
class IPrintable {
public:
    virtual ~IPrintable() = default;
    virtual void print() const = 0;  // Pure interface — no data
};

class PrintFormatter {
    std::string format_;
public:
    void printFormatted(const std::string& content) const;
};

class CombinedLog : public IPrintable {
    FlightLog flightLog_;         // HAS-A, not IS-A
    CrewLog crewLog_;             // HAS-A, not IS-A
    PrintFormatter formatter_;    // Shared behavior via composition

public:
    void print() const override {
        formatter_.printFormatted(flightLog_.content() + crewLog_.content());
    }
};
```

**Commit strategy per [ENG-4.1](laws/engineering/eng-4-testing.md):**
- Commit 1: Characterization tests for diamond class behavior
- Commit 2: Extract pure interface (no data) from shared base
- Commit 3: Convert one derived class to composition
- Commit 4: Convert remaining derived classes

### 2. Operator Overloading Hiding Expensive Operations

**Recognition:**
- `Flight a + b` compiles but takes 50ms (deep copies, DB lookups, network calls)
- `operator==` does deep comparison of nested containers
- `operator<<` triggers serialization of large object graphs
- Profiler shows hot spots in overloaded operators

**Why it exists:** Operator overloading makes code "look clean" — `a + b` is more readable than `a.mergeWith(b)`. But the visual simplicity hides computational cost.

**Fix:** Operators should only be overloaded when:
1. The semantics match the built-in operator (addition is commutative, comparison is reflexive)
2. The cost is proportional to what a reader expects (O(1) for `==` on IDs, O(n) is acceptable for containers)

Use named functions for expensive operations — the name communicates the cost:

```cpp
// BAD — operator+ hides expensive merge
FlightPlan operator+(const FlightPlan& a, const FlightPlan& b) {
    // Deep copies both plans, queries weather service,
    // recalculates fuel — 200ms operation
    return merge(a, b);
}
auto combined = planA + planB;  // Looks instant, takes 200ms

// GOOD — named function communicates cost
FlightPlan FlightPlan::mergeWith(const FlightPlan& other,
                                  const WeatherService& weather) const {
    // Same operation, but name + parameters make cost visible
}
auto combined = planA.mergeWith(planB, weatherService);
```

**Commit strategy per [ENG-4.1](laws/engineering/eng-4-testing.md):**
- Commit 1: Add benchmark test for operator
- Commit 2: Create named function equivalent
- Commit 3: Deprecate operator, update call sites
- Commit 4: Remove deprecated operator

### 3. Implicit Conversions Causing Silent Bugs

**Recognition:**
- Function expecting `FlightId` accepts `const char*` or `std::string` without explicit construction
- Overload resolution picks surprising candidates
- `process("AA100")` compiles when `process(FlightId)` is the signature
- Debugging shows objects constructed at unexpected call sites

**Why it exists:** C++ allows single-argument constructors to act as implicit conversion operators. This was intended for convenience (e.g., `std::string` from `const char*`) but causes bugs in domain types.

**Fix:** Mark ALL single-argument constructors `explicit`. Mark ALL conversion operators `explicit`. This is the #1 silent bug source in legacy value types.

```cpp
// BEFORE — implicit conversion trap
class FlightId {
public:
    FlightId(const std::string& raw);           // Implicit: string → FlightId
    FlightId(int numericId);                     // Implicit: int → FlightId!
    operator std::string() const;                // Implicit: FlightId → string!
};

void cancelFlight(FlightId id);

cancelFlight(42);        // Compiles! Creates FlightId from int
cancelFlight("AA100");   // Compiles! string → FlightId
std::string s = FlightId("AA100");  // Compiles! Implicit conversion back

// AFTER — explicit conversion required
class FlightId {
public:
    explicit FlightId(const std::string& raw);
    explicit FlightId(int numericId);
    explicit operator std::string() const;
};

cancelFlight(FlightId(42));                      // Must be explicit
cancelFlight(FlightId("AA100"));                 // Must be explicit
auto s = static_cast<std::string>(flightId);     // Must be explicit
```

**Commit strategy per [ENG-4.1](laws/engineering/eng-4-testing.md):**
- Commit 1: Add `explicit` to constructors of one value type
- Commit 2: Fix all resulting compile errors at call sites
- Commit 3: Add negative compile test (verify implicit conversion fails)

### 4. Copy Semantics Creating Performance Problems

**Recognition:**
- Large objects (`FlightPlan`, `Manifest`) passed by value to functions
- Profiler shows significant time in copy constructors
- `std::vector<LargeObject>` reallocation causes spikes
- Move-unaware classes in containers

**Why it exists:** Pre-C++11, copy was the only way to transfer objects. Move semantics didn't exist. Classes written before 2011 have no move constructors.

**Fix:** Add move constructor and move assignment operator (`noexcept`!) to every class with expensive copy. Then ensure callers use move semantics.

```cpp
// BEFORE — copy only, expensive
class FlightPlan {
    std::vector<Waypoint> waypoints_;   // 500+ waypoints
    std::string rawData_;               // 100KB of parsed data
    // No move constructor — vector reallocation copies everything
};

// AFTER — move-aware
class FlightPlan {
    std::vector<Waypoint> waypoints_;
    std::string rawData_;

public:
    // Move constructor — O(1), steals resources
    FlightPlan(FlightPlan&& other) noexcept
        : waypoints_(std::move(other.waypoints_))
        , rawData_(std::move(other.rawData_))
    {}

    // Move assignment — O(1)
    FlightPlan& operator=(FlightPlan&& other) noexcept {
        waypoints_ = std::move(other.waypoints_);
        rawData_ = std::move(other.rawData_);
        return *this;
    }

    // Copy operations can be defaulted or explicitly defined
    FlightPlan(const FlightPlan&) = default;
    FlightPlan& operator=(const FlightPlan&) = default;
};

// Usage — move when transferring ownership
std::vector<FlightPlan> plans;
plans.push_back(std::move(loadedPlan));     // O(1) move, not O(n) copy
plans.emplace_back(buildPlan(route));       // Constructed in-place
```

> **Critical:** Move constructors and move assignment MUST be `noexcept`. `std::vector` will only use move (instead of copy) during reallocation if the move operations are `noexcept`.

**Commit strategy per [ENG-4.1](laws/engineering/eng-4-testing.md):**
- Commit 1: Add benchmark for copy-heavy operation
- Commit 2: Add move constructor + move assignment (noexcept)
- Commit 3: Update callers to use `std::move` where appropriate
- Commit 4: Verify performance improvement with benchmark

### 5. Over-Reliance on Virtual Functions

**Recognition:**
- Class hierarchies with 20+ virtual method overrides
- `dynamic_cast` chains: `if (auto* b = dynamic_cast<Boeing*>(a)) { ... } else if (auto* a = dynamic_cast<Airbus*>(a)) { ... }`
- Virtual function calls in tight inner loops (performance-sensitive paths)
- Each new aircraft type requires modifying 15+ virtual overrides

**Why it exists:** Virtual functions are C++'s primary mechanism for runtime polymorphism. Early C++ education emphasized deep virtual hierarchies as "proper OOP."

**Fix:** Use the right polymorphism mechanism for the situation:

| Mechanism | When | Overhead |
|-----------|------|----------|
| Virtual functions | Runtime type varies (plugins, user-defined) | Indirect call per invocation |
| CRTP (Curiously Recurring Template Pattern) | Type known at compile time, hot path | Zero — fully inlined |
| C++20 Concepts / `std::variant` | Closed set of types | Zero — compile-time dispatch |
| `std::function` + lambdas | Callbacks, one-off customization | Indirect call + possible allocation |

```cpp
// BEFORE — virtual in hot loop
class Aircraft {
public:
    virtual double fuelBurn(double distance) const = 0;
};

// Called 1M times per route optimization — virtual dispatch overhead
for (const auto& segment : route) {
    total += aircraft->fuelBurn(segment.distance);  // Virtual call
}

// AFTER — CRTP for compile-time polymorphism in hot path
template <typename Derived>
class AircraftBase {
public:
    double fuelBurn(double distance) const {
        return static_cast<const Derived*>(this)->fuelBurnImpl(distance);
    }
};

class Boeing737 : public AircraftBase<Boeing737> {
public:
    double fuelBurnImpl(double distance) const {
        return distance * 0.0463;  // Fully inlined
    }
};
```

**When to keep virtual functions:**
- Plugin systems where types are loaded at runtime
- User-defined strategies passed across module boundaries
- When the set of types is open-ended and not performance-critical

**Commit strategy per [ENG-4.1](laws/engineering/eng-4-testing.md):**
- Commit 1: Profile and benchmark virtual call in hot path
- Commit 2: Implement CRTP or variant alternative
- Commit 3: A/B benchmark: virtual vs compile-time dispatch
- Commit 4: Replace in production if benchmark proves improvement


---

## See Also

- [Object Design Patterns](ref-object-design-patterns.md)
