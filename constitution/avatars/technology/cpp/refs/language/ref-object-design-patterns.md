---
cpp_version_min: 11
cpp_version_note: >-
  Design patterns using modern C++; move semantics (C++11+).
avatar: cpp
---

# C++ Avatar Reference: Object Design Patterns

---

### 6. Missing Move Semantics on Large Objects

**Recognition:**
- Classes written before C++11 with expensive copy constructors
- User-defined destructor but no move constructor or move assignment
- `std::vector` of these classes shows excessive copy constructor calls during reallocation
- Profiler shows copy constructors in hot paths

**Why it exists:** Move semantics were introduced in C++11. Classes designed before that only have copy semantics. Many were never updated.

**Fix:** For every class with a user-defined destructor:
1. If all members are moveable and the class manages no raw resources: `= default` the move operations
2. If the class manages raw resources: implement move constructor and move assignment manually, both `noexcept`
3. Leave the moved-from object in a valid but unspecified state

```cpp
// BEFORE — pre-C++11 class, copy-only
class CrewRoster {
    std::vector<CrewMember> members_;
    std::map<std::string, Assignment> assignments_;
    DatabaseConnection* db_;  // raw pointer — non-owning

public:
    ~CrewRoster() { /* doesn't delete db_ — it's borrowed */ }
    // No copy or move defined — compiler generates copy, deletes move
    // (because destructor is user-defined)
};

// AFTER — Rule of 5 with move semantics
class CrewRoster {
    std::vector<CrewMember> members_;
    std::map<std::string, Assignment> assignments_;
    DatabaseConnection* db_;  // raw pointer — non-owning

public:
    ~CrewRoster() = default;  // Explicit but defaulted

    // Copy
    CrewRoster(const CrewRoster&) = default;
    CrewRoster& operator=(const CrewRoster&) = default;

    // Move — noexcept is critical for vector reallocation
    CrewRoster(CrewRoster&& other) noexcept = default;
    CrewRoster& operator=(CrewRoster&& other) noexcept = default;
};
```

> **Tip:** If you can refactor to Rule of 0 (replace `DatabaseConnection*` with a non-owning wrapper or reference), the compiler generates correct move operations automatically.

**Commit strategy per [ENG-4.1](laws/engineering/eng-4-testing.md):**
- Commit 1: Add test verifying object can be moved (compile + runtime)
- Commit 2: Add move constructor and move assignment (`noexcept`)
- Commit 3: Update container usage to leverage move semantics

### Decision Tree: Inheritance, Composition, or Templates?

Use this decision tree when designing or rehabilitating object relationships:

```
START: Does type B need to reuse behavior from type A?
│
├── YES
│   ├── Is the relationship truly "B is a kind of A"?
│   │   ├── YES
│   │   │   ├── Will B be used polymorphically (via A* or A&)?
│   │   │   │   ├── YES → Public inheritance (virtual methods)
│   │   │   │   └── NO
│   │   │   │       ├── Is this a hot path (>100K calls/sec)?
│   │   │   │       │   ├── YES → CRTP (compile-time polymorphism)
│   │   │   │       │   └── NO  → Public inheritance is fine
│   │   │   └── Are there data members in the base?
│   │   │       ├── YES → Prefer composition (HAS-A) to avoid diamond
│   │   │       └── NO  → Interface inheritance (pure virtual) is OK
│   │   └── NO (it's "B uses A" or "B contains A")
│   │       └── Composition: B has a member of type A
│   └── Does B need A's interface but different implementation?
│       └── Composition + forwarding, or Strategy pattern
│
├── Does the behavior need to work with multiple types?
│   ├── Types known at compile time → Template
│   ├── Types known at link time → Link seam (different .o)
│   └── Types determined at runtime → Virtual interface
│
└── NO → Value type, no relationship needed
```

> **Per [ENG-2.1](laws/engineering/eng-2-architecture.md):** Default to composition. Use inheritance only when polymorphism is required. Use templates when types are known at compile time and performance matters.

### Protected and Private Inheritance

> ⚠️ **Complexity Warning:** Protected and private inheritance are rarely the right choice. They are "implementation inheritance" — the derived class gets the base's implementation but not its interface.

```cpp
// Private inheritance — "implemented-in-terms-of"
class TimerBasedScheduler : private Timer {
    // Timer's interface is NOT exposed to clients
    // Use Timer's protected/public methods internally
    using Timer::start;  // selectively expose if needed
};

// SIMPLIFICATION — prefer composition (achieves the same thing)
class TimerBasedScheduler {
    Timer timer_;  // ✅ same capability, no inheritance complexity
};
```

**When protected/private inheritance is justified:**
- Need to override virtual methods of the base class (composition can't do this)
- Need access to protected members (composition gives only public access)
- Empty Base Optimization (EBO) when deriving from stateless policy classes

**`dynamic_cast` interaction:** `dynamic_cast` cannot cast to a private or protected base from outside the class. This is by design but frequently surprises developers. If you need runtime polymorphism, use public inheritance.

### Mixin and Policy-Based Design

For combining behaviors without multiple inheritance, use the policy-based design pattern (Alexandrescu-style):

```cpp
// COMPLIANT — policy-based design (no MI diamonds)
template <typename LogPolicy, typename RetryPolicy>
class FlightClient : private LogPolicy, private RetryPolicy {
public:
    FlightResult search(const SearchCriteria& criteria) {
        this->log("Starting search");
        return this->retry([&] { return do_search(criteria); });
    }
};

// Usage — compose behaviors at compile time
using ProductionClient = FlightClient<FileLogger, ExponentialRetry>;
using TestClient = FlightClient<NullLogger, NoRetry>;
```

**Migration from multiple inheritance to policies:**
1. Identify the independent behaviors being inherited (logging, retry, serialization)
2. Extract each into a template parameter (policy class)
3. Use private inheritance or composition for each policy
4. Define concept constraints for each policy type

---

## Test Isolation and Mock Boundaries

Per [ENG-4.7](laws/engineering/eng-4-testing.md) (Test Isolation) and [ENG-4.8](laws/engineering/eng-4-testing.md) (Mock Boundaries), C++ tests must be independent, repeatable, and only test one unit at a time. C++ presents unique isolation challenges compared to JVM or CLR languages.

### Link-Time Isolation

C++ has no reflection — mocking requires compile-time or link-time seams.

| Technique | When to Use | Overhead |
|-----------|-------------|----------|
| **Virtual interface + gmock** | Runtime polymorphism exists | vtable indirection |
| **Template injection** | Hot paths, no virtual allowed | Zero — fully inlined |
| **Link seam** (different `.o` for test) | C/legacy code, free functions | Zero — resolved at link time |
| **`#ifdef TESTING`** | Last resort only | Conditional compilation |

```cpp
// COMPLIANT — Template injection for zero-overhead test isolation
template <typename HttpClient = ProductionHttpClient>
class FlightService {
    HttpClient client_;
public:
    FlightResult search(const SearchCriteria& c) {
        auto response = client_.get("/flights", c.to_params());
        return FlightResult::from_response(response);
    }
};

// Test — inject mock via template parameter
struct MockHttp {
    HttpResponse get(std::string_view, const Params&) {
        return HttpResponse{200, R"({"flights": []})"};
    }
};
TEST(FlightServiceTest, ReturnsEmptyOnNoFlights) {
    FlightService<MockHttp> svc;
    auto result = svc.search(SearchCriteria{"DFW", "ORD"});
    EXPECT_TRUE(result.flights().empty());
}
```

### Mock Boundary Rules

Per [ENG-4.8](laws/engineering/eng-4-testing.md), define clear boundaries for what gets mocked:

- **Mock:** External services (HTTP, gRPC, database), system clock, file I/O
- **Don't mock:** Value types, algorithms, data structures, pure functions
- **Limit:** No more than 3 mocks per test — if more are needed, the unit under test has too many dependencies (violates [ENG-3.4](laws/engineering/eng-3-code-quality.md) SRP)

### Static State in Tests

Global/static state causes flaky tests. Per [ENG-4.7](laws/engineering/eng-4-testing.md):
- Never use global singletons in testable code — inject dependencies
- Use `TEST_F` fixtures with `SetUp()/TearDown()` for test-local state
- For thread-local caches, reset between tests using `testing::Environment`

---

## See Also

- [Domain Modeling & Safety](ref-domain-modeling.md)
- [Core Language Patterns](ref-core-language.md)


---

## See Also

- [Object Design Rehabilitation](ref-object-design-rehabilitation.md)
