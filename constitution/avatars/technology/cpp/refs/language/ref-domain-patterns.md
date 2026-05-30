---
cpp_version_min: 11
cpp_version_note: >-
  DDD and domain patterns using C++11 move semantics.
avatar: cpp
---

# C++ Avatar Reference: Domain Patterns

---

## Domain Modeling

Per [ENG-2.1](laws/engineering/eng-2-architecture.md) (Domain-Driven Design Law), all projects must apply DDD tactical patterns — Entities, Value Objects, Aggregates, and Domain Events. C++ ownership semantics naturally enforce aggregate boundaries.

### Entity Pattern (Ownership-First)

```cpp
class Order {
public:
    static Order create(CustomerId customer_id) {
        return Order{OrderId::generate(), std::move(customer_id)};
    }

    void add_item(const Product& product, int quantity) {
        ensure_modifiable();
        lines_.emplace_back(product.id(), quantity, product.price());
    }

    [[nodiscard]] Money total() const {
        return std::accumulate(
            lines_.begin(), lines_.end(), Money::zero(),
            [](Money acc, const OrderLine& line) { return acc + line.subtotal(); });
    }

private:
    Order(OrderId id, CustomerId customer_id)
        : id_{std::move(id)}, customer_id_{std::move(customer_id)} {}

    void ensure_modifiable() const {
        if (status_ != OrderStatus::kDraft) {
            throw OrderNotModifiableError{id_, status_};
        }
    }

    OrderId id_;
    CustomerId customer_id_;
    std::vector<OrderLine> lines_;
    OrderStatus status_ = OrderStatus::kDraft;
};
```

### Value Object Pattern (Immutable)

Per [ENG-3.2](laws/engineering/eng-3-code-quality.md) (Immutability Law), value objects must be constructed once and never modified. In C++, make all data members `const` or make the class immutable by design (private members, no mutating methods, return new instances).

```cpp
class Money {
public:
    static Money zero() { return Money{0, "USD"}; }
    static Money of(int amount) { return Money{amount, "USD"}; }

    Money operator+(const Money& other) const {
        validate_same_currency(other);
        return Money{amount_ + other.amount_, currency_};
    }

    Money operator*(int quantity) const {
        return Money{amount_ * quantity, currency_};
    }

    bool operator==(const Money& other) const = default;

private:
    Money(int amount, std::string currency)
        : amount_{amount}, currency_{std::move(currency)} {
        if (amount_ < 0) throw std::invalid_argument{"Amount cannot be negative"};
    }

    void validate_same_currency(const Money& other) const {
        if (currency_ != other.currency_) {
            throw CurrencyMismatchError{currency_, other.currency_};
        }
    }

    int amount_;
    std::string currency_;
};
```

---

## Dependency Injection in C++

> Per [ENG-2.5](laws/engineering/eng-2-architecture.md), high-level modules must not depend on low-level modules — both depend on abstractions. In C++, this is achieved via **constructor injection** with pure virtual interfaces. No DI (Dependency Injection) framework is required.

### The C++ DI Triad

1. **Interface** — pure virtual class defining the contract
2. **Implementation** — concrete class implementing the interface
3. **Composition root** — `main()` or a factory that wires implementations to interfaces

```cpp
// 1. Interface (pure virtual — the abstraction)
class IFlightRepository {
public:
    virtual ~IFlightRepository() = default;
    virtual std::optional<Flight> find(FlightId id) const = 0;
    virtual void save(const Flight& flight) = 0;
};

// 2. Implementation (concrete — depends on infrastructure)
class PostgresFlightRepository final : public IFlightRepository {
public:
    explicit PostgresFlightRepository(pqxx::connection& db) : db_{db} {}
    std::optional<Flight> find(FlightId id) const override { /* ... */ }
    void save(const Flight& flight) override { /* ... */ }
private:
    pqxx::connection& db_;
};

// 3. Service (depends on interface, not implementation)
class FlightService {
public:
    explicit FlightService(std::unique_ptr<IFlightRepository> repo)
        : repo_{std::move(repo)} {}

    void cancelFlight(FlightId id) {
        auto flight = repo_->find(id);
        if (!flight) throw FlightNotFoundError{id};
        flight->cancel();
        repo_->save(*flight);
    }
private:
    std::unique_ptr<IFlightRepository> repo_;  // owns the dependency
};

// 4. Composition root (main.cpp — the ONLY place that knows concrete types)
int main() {
    pqxx::connection db{"postgresql://localhost/flights"};
    auto repo = std::make_unique<PostgresFlightRepository>(db);
    FlightService service{std::move(repo)};
    // ... run service
}
```

### Ownership Rules for DI

| Relationship | C++ Mechanism | When to Use |
|-------------|---------------|-------------|
| Service **owns** dependency | `std::unique_ptr<Interface>` | Default — single owner, clear lifetime |
| Service **borrows** dependency | `Interface&` (const or non-const) | Dependency outlives service (e.g., DB connection pool) |
| Service **shares** dependency | `std::shared_ptr<Interface>` | Multiple services need the same instance (rare — prefer unique) |

### Testing with DI

Constructor injection makes testing trivial — inject a mock:

```cpp
TEST(FlightServiceTest, cancel_nonexistent_throws) {
    auto mock_repo = std::make_unique<MockFlightRepository>();
    EXPECT_CALL(*mock_repo, find(_)).WillOnce(Return(std::nullopt));
    FlightService service{std::move(mock_repo)};
    EXPECT_THROW(service.cancelFlight(FlightId{"AA100"}), FlightNotFoundError);
}
```

> **Governance:** No DI framework (Boost.DI, Google Fruit) is prescribed. Manual constructor injection at the composition root is sufficient for most AA C++ services and avoids adding a compile-time or runtime dependency.

---

## Safety and Ownership

### Ownership-First API Design

Per [ENG-6.1](laws/engineering/eng-6-security.md) (Security by Design), C++ APIs must express ownership intent explicitly. Inspired by Rust's ownership model, translated to modern C++ idioms:

**Core principles:**
- Every heap resource has exactly one owner at any point in time
- Ownership transfer is explicit via `std::unique_ptr` or move semantics
- Shared ownership (`std::shared_ptr`) is permitted only when lifetime cannot be statically determined — document the rationale
- Non-owning access uses references, `std::span`, or `gsl::not_null<T*>`
- Factory functions return `std::unique_ptr` to make ownership transfer unambiguous

```cpp
// GOOD — ownership-first factory: caller owns the result
std::unique_ptr<FlightPlan> create_flight_plan(
    FlightId id, Route route, CrewAssignment crew) {
    auto plan = std::make_unique<FlightPlan>(
        std::move(id), std::move(route), std::move(crew));
    plan->validate();
    return plan;
}

// GOOD — explicit ownership transfer into a container
class FlightSchedule {
public:
    void add_plan(std::unique_ptr<FlightPlan> plan) {
        plans_.push_back(std::move(plan));
    }

    // Non-owning read access via span
    std::span<const std::unique_ptr<FlightPlan>> plans() const {
        return plans_;
    }

private:
    std::vector<std::unique_ptr<FlightPlan>> plans_;
};

// GOOD — shared_ptr only when lifetime is truly shared (document why)
// Example: cache entry accessed by multiple concurrent request handlers
auto shared_config = std::make_shared<RouteConfig>(load_config());
```

**When to use each smart pointer:**

| Pointer | Use when | Example |
|---------|----------|---------|
| `std::unique_ptr` | Single owner, transfer via move | Domain entities, factory results |
| `std::shared_ptr` | Multiple owners with shared lifetime (document rationale) | Cache entries, observer patterns |
| `raw T*` or `T&` | Non-owning observation, never delete | Function parameters, iteration |
| `gsl::not_null<T*>` | Non-owning, guaranteed non-null | Required dependency references |

### Lifetime and Bounds Safety

Per [ENG-6.1](laws/engineering/eng-6-security.md), prevent dangling references, use-after-free, and buffer overflows by defaulting to safe patterns:

**Defaults:**
- Prefer stack allocation and value semantics — heap allocation only when necessary
- Use `std::span` instead of raw pointer + size pairs for bounds-safe array access
- Use `gsl::not_null<T*>` for non-null pointer contracts
- Use `std::optional` over sentinel values or nullable raw pointers
- All RAII handles must release resources in destructors — never rely on manual cleanup

**Preventing dangling references:**
- Never return references or pointers to local variables
- Never store references to temporaries
- Use `std::string_view` only for non-owning, short-lived read access — never store across scope boundaries
- Prefer returning by value (move semantics make this efficient)

```cpp
// GOOD — bounds-safe iteration with std::span
void process_flight_segments(std::span<const FlightSegment> segments) {
    for (const auto& seg : segments) {
        validate_segment(seg);  // no index math, no off-by-one
    }
}

// GOOD — non-null contract for required dependency
void register_handler(gsl::not_null<EventHandler*> handler) {
    handlers_.push_back(handler);  // caller guarantees non-null
}

// GOOD — optional instead of nullptr sentinel
std::optional<Gate> find_available_gate(Terminal terminal) {
    for (const auto& gate : gates_) {
        if (gate.terminal() == terminal && gate.is_available()) {
            return gate;
        }
    }
    return std::nullopt;  // explicit "not found" — no dangling pointer risk
}

// GOOD — RAII file handle, no manual close needed
class AuditLogWriter {
public:
    explicit AuditLogWriter(const std::filesystem::path& path)
        : stream_{path, std::ios::app} {
        if (!stream_) throw std::runtime_error{"Cannot open audit log"};
    }
    // ~AuditLogWriter() closes stream_ automatically (RAII)

    void write(std::string_view entry) { stream_ << entry << '\n'; }

private:
    std::ofstream stream_;
};
```

### Unsafe Boundary Governance

Per [ENG-6.1](laws/engineering/eng-6-security.md) and the Q5 stakeholder decision, unsafe operations (`reinterpret_cast`, C-style casts, manual memory management, inline assembly) must be localized behind reviewed boundary modules. Each repository selects a governance mode:

| Mode | Policy | When to use |
|------|--------|-------------|
| **Strict mode (Option 1)** | Architect approval + waiver logging required for **all** unsafe boundary exceptions | Safety-critical systems (crew scheduling, dispatch, maintenance compliance) |
| **Default mode (Option 2)** *(recommended)* | Architect approval + waiver logging required only for **safety-critical paths** | Most greenfield and modernizing brownfield repos |
| **Lightweight mode (Option 3)** | Reviewer approval only (must be explicitly justified in repo governance) | Low-risk infrastructure utilities — requires architecture governance approval to select |

**Greenfield configuration:** Default mode (Option 2); cannot downgrade to Option 3 without architecture governance approval.

**Brownfield configuration:** Default mode (Option 2) with temporary phased exceptions allowed per repository implementation plan. Planned progression toward Option 2 (or Option 1 for higher-assurance repos).

**Per-repository configuration:**
- Declare policy mode in repository AGENTS.md or governance config
- Include: unsafe-boundary policy mode, safety-critical path list, waiver process owner, audit logging location
- Enforce mode in CI/policy checks where available

**What constitutes an unsafe boundary:**
- `reinterpret_cast` or C-style casts
- Manual `new`/`delete` outside of RAII wrappers
- Raw pointer arithmetic
- Inline assembly
- `#pragma` directives that disable safety checks
- Direct OS/kernel API calls that bypass type safety

---


---

## See Also

- [Domain Quality and Anti-Patterns](ref-domain-quality.md)
