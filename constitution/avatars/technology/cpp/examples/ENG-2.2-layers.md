---
law_id: ENG-2.2
cpp_version_min: 11
avatar: cpp
---

# [ENG-2.2](laws/engineering/eng-2-architecture.md): Layered Architecture — C++ Examples

## The Rule

Layers separate concerns: each layer has a single responsibility and depends only on the layer directly below it. Dependencies always point inward (infrastructure → domain, never domain → infrastructure).

## Layer Ownership in C++

| Layer | Owns | C++ Constructs |
|-------|------|----------------|
| **Domain** | Business rules, entities, value objects | Pure headers/classes in `namespace domain`, no `#include` of infra headers |
| **Application** | Use-case orchestration | Classes in `namespace app`, depends on domain interfaces |
| **Infrastructure** | DB, HTTP, messaging | Concrete classes in `namespace infra`, implements domain interfaces via `override` |
| **Presentation** | API surface | Controllers/handlers, thin — delegates immediately to application layer |

## COMPLIANT: Clear Layer Separation

```cpp
// Domain layer — no infrastructure dependencies
class PricingService {
public:
    explicit PricingService(FareRepository& repo) : repo_(repo) {}
    Money calculate(FlightId id) {
        auto fare = repo_.find(id);
        return fare.base() + fare.taxes();
    }
private:
    FareRepository& repo_;  // Interface, not implementation
};

// Infrastructure layer — implements domain interfaces
class SqlFareRepository : public FareRepository {
public:
    Fare find(FlightId id) override { /* SQL query */ }
};

// Application layer — orchestrates use cases
class GetFareUseCase {
public:
    FareResponse execute(FlightId id) {
        auto amount = pricing_.calculate(id);
        return FareResponse{amount};
    }
private:
    PricingService& pricing_;
};
```

**Why compliant:** Domain depends on abstractions. Infrastructure implements interfaces. Application orchestrates.

## NON-COMPLIANT: Mixed Layers

```cpp
class PricingService {
    sqlite3* db_;  // Domain directly depends on infrastructure
    Money calculate(FlightId id) {
        sqlite3_exec(db_, "SELECT ...", ...);  // SQL in domain
    }
};
```

**Why non-compliant:** Domain layer contains SQL. Impossible to test without a database. Violates dependency inversion.

## Edge Cases & Warnings

| Scenario | Risk | Safe Approach |
|----------|------|---------------|
| Layer skip — application code calls `SqlFareRepository` directly | Bypasses the domain layer; breaks testability and makes future refactoring painful | Enforce with `#include` discipline: domain headers must never `#include` infrastructure headers; use a dependency rule linter (`include-what-you-use` or custom CI check) |
| "Utility" namespace every layer includes | Becomes a layer-violation dumping ground over time | Keep utilities stateless and side-effect-free; assign each utility to a specific layer; reject PRs that add infrastructure code to `utils/` |
| Circular include between layers (domain includes infrastructure to handle an exception type) | Destroys testability; the domain can no longer be tested without the full infrastructure stack | Define shared value types and error codes in a separate `domain-types/` library that all layers can include without violating the dependency rule |
