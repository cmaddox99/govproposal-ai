---
cpp_version_min: 11
cpp_version_note: >-
  SRP, cohesion, and refactoring patterns using C++11+ features.
avatar: cpp
---

# C++ Avatar Reference: Domain Quality and Anti-Patterns

---

## SRP and C++ Refactoring Patterns

Per [ENG-3.4](laws/engineering/eng-3-code-quality.md) (Single Responsibility Principle) and [ENG-3.8](laws/engineering/eng-3-code-quality.md) (Refactoring Patterns), C++ classes should have one reason to change. C++-specific refactoring tools and patterns help enforce SRP.

### C++ SRP Indicators

| Sign of SRP Violation | Metric |
|----------------------|--------|
| Header file > 500 LOC | Class does too much |
| > 10 `#include` directives | Too many dependencies |
| `friend` declarations | Broken encapsulation |
| > 5 public methods unrelated to core purpose | Mixed responsibilities |
| `.cpp` file > 1000 LOC | Needs decomposition |

### PIMPL — Extract Implementation

PIMPL separates interface from implementation, reducing compilation coupling:

```cpp
// flight_service.h — minimal header, fast compile
class FlightService {
public:
    FlightService();
    ~FlightService();
    FlightResult search(const SearchCriteria& c);
private:
    struct Impl;
    std::unique_ptr<Impl> impl_;  // ✅ hides all dependencies
};

// flight_service.cpp — implementation details hidden
struct FlightService::Impl {
    HttpClient http_;       // ← not in header
    CacheService cache_;    // ← not in header
    MetricsCollector metrics_;
    FlightResult do_search(const SearchCriteria& c);
};
```

### Extract Interface — Virtual Boundary

Per [ENG-2.5](laws/engineering/eng-2-architecture.md) (Dependency Inversion), depend on abstractions:

```cpp
// BEFORE — concrete dependency (untestable)
class BookingService {
    SabreClient sabre_;  // concrete type — can't mock in tests
};

// AFTER — interface extraction
class IGdsClient {
public:
    virtual ~IGdsClient() = default;
    virtual FlightResult search(const SearchCriteria&) = 0;
};

class BookingService {
    std::unique_ptr<IGdsClient> gds_;  // ✅ injectable, mockable
};
```

### C++ Refactoring Safety Checklist

Per [ENG-3.8](laws/engineering/eng-3-code-quality.md):
1. **Characterize first** — write tests that capture current behavior before refactoring
2. **Move in small steps** — each commit should compile, pass tests, and be revertable
3. **Use compiler as safety net** — rename methods (not just fields) to find all call sites
4. **Check ABI** — if refactoring a shared library, verify ABI compatibility with `abidiff`

---

## Anti-Patterns to Avoid

### Raw Owning Pointers

Per [ENG-6.1](laws/engineering/eng-6-security.md) (Security by Design), raw owning pointers are prohibited — they leak on exception paths and create use-after-free vulnerabilities.

```cpp
// BAD — raw owning pointer leaks on exception
Widget* create_widget() {
    auto* w = new Widget();
    configure(w);  // if this throws, w leaks
    return w;
}

// GOOD — unique_ptr with RAII ownership
std::unique_ptr<Widget> create_widget() {
    auto w = std::make_unique<Widget>();
    configure(*w);
    return w;
}
```

### Unbounded Buffer Access

Per [ENG-6.5](laws/engineering/eng-6-security.md) (Input Validation Law), all buffer access must be bounds-checked. Use `std::span` (C++20) to enforce bounds safety at the API level.

```cpp
// BAD — raw pointer + size, no bounds checking
void process(const int* data, size_t len) {
    for (size_t i = 0; i <= len; ++i) { /* off-by-one */ }
}

// GOOD — std::span with implicit bounds
void process(std::span<const int> data) {
    for (auto val : data) { /* safe iteration */ }
}
```

### Anemic Domain Model

Per [ENG-2.1](laws/engineering/eng-2-architecture.md) (DDD Law), domain logic must be encapsulated within aggregate roots, not scattered across free functions.

```cpp
// BAD — struct with only data, logic scattered in free functions
struct Order {
    std::string customer_id;
    std::vector<OrderLine> lines;
    std::string status;
};
void add_item(Order& order, Product product) { /* logic outside class */ }

// GOOD — behavior encapsulated per DDD aggregate pattern
class Order {
public:
    void add_item(const Product& product, int quantity);
    Money total() const;
private:
    void ensure_modifiable() const;
};
```

### Object Slicing

```cpp
// BAD — passing derived object by value silently truncates it
class Base { public: virtual std::string name() const { return "Base"; } int x = 1; };
class Derived : public Base { public: std::string name() const override { return "Derived"; } int y = 2; };

void process(Base b) {        // ← copies only the Base part; y is lost
    std::cout << b.name();    // prints "Base", not "Derived" — SILENTLY WRONG
}
Derived d;
process(d);  // object slicing — no compiler warning, no runtime error

// GOOD — pass polymorphic objects by reference or pointer, never by value
void process(const Base& b) {  // ← no copy, no slicing
    std::cout << b.name();     // prints "Derived" — correct
}
```

> **Why this matters:** Java, Python, and C# developers never encounter object slicing because those languages use reference semantics by default. In C++, `Base b = derived;` is a valid copy that silently discards the derived portion. This is one of the most common sources of silent bugs when developers from other languages write C++. Per [ENG-3.1](laws/engineering/eng-3-code-quality.md), prefer `const&` for polymorphic parameters. Mark base classes with a deleted copy constructor if slicing would be dangerous.

### Safe Observer Pattern

```cpp
// BAD — observer stores raw pointer; crashes if subject is destroyed first
class BadSubject {
    std::vector<Observer*> observers_;  // dangling pointers after observer destruction
};

// GOOD — weak_ptr-based observer with automatic deregistration
class Subject {
public:
    using Callback = std::function<void(const Event&)>;

    // Returns a shared_ptr token — observer lives as long as the token is held
    [[nodiscard]] std::shared_ptr<void> subscribe(Callback cb) {
        auto token = std::make_shared<Callback>(std::move(cb));
        std::lock_guard lock{mutex_};
        observers_.push_back(token);
        return token;
    }

    void notify(const Event& event) {
        std::lock_guard lock{mutex_};
        // Automatically prune expired observers
        observers_.erase(
            std::remove_if(observers_.begin(), observers_.end(),
                [](const auto& wp) { return wp.expired(); }),
            observers_.end());
        for (auto& wp : observers_) {
            if (auto sp = wp.lock()) { (*sp)(event); }
        }
    }
private:
    std::mutex mutex_;
    std::vector<std::weak_ptr<Callback>> observers_;  // no dangling — auto-expires
};
```

> **Governance:** Per [ENG-6.1](laws/engineering/eng-6-security.md), never store raw observer pointers. Use `weak_ptr` + token pattern to prevent dangling callbacks. When the observer drops its token (`shared_ptr`), the subscription is automatically cleaned up on next `notify()`.

---

## See Also

- [Core Language Patterns](ref-core-language.md)
- [Object Design Rehabilitation](ref-object-design.md)


---

## See Also

- [Domain Patterns](ref-domain-patterns.md)
