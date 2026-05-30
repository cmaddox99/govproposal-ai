---
id: ENG-3.1-policy-based-design
law_id: ENG-3.1
avatar: cpp
title: Policy-Based Design
cpp_version_min: "11"
tags: [templates, policy, strategy, compile-time]
---

# Policy-Based Design — ENG-3.1

Per [ENG-3.1](../../../laws/engineering/eng-3-code-quality.md), prefer
compile-time policy composition over runtime virtual dispatch when the
policies are known at compile time.

## COMPLIANT

```cpp
// StoragePolicy: InMemoryStorage or SqliteStorage
// LogPolicy:     SilentLog or AuditLog
template<typename StoragePolicy, typename LogPolicy>
class FlightRepository {
    StoragePolicy storage_;
    LogPolicy     log_;
public:
    void save(const Flight& f) {
        log_.record("save", f.id());
        storage_.persist(f);
    }
    std::optional<Flight> find(FlightId id) {
        return storage_.fetch(id);
    }
};

// Concept constraints on policies (C++20)
// Assumes Flight and FlightId are defined as in the FlightRepository class above
template<typename T>
concept StorageConcept = requires(T t, Flight f, FlightId id) {
    t.persist(f);
    { t.fetch(id) } -> std::same_as<std::optional<Flight>>;
};

template<StorageConcept S, typename L>
class FlightRepo2 { /* ... */ };
```

## NON-COMPLIANT

```cpp
// virtual dispatch for strategies known at compile time
struct IStorage { virtual void persist(const Flight&) = 0; virtual ~IStorage() = default; };
struct ILog    { virtual void record(std::string_view, FlightId) = 0; virtual ~ILog() = default; };

class FlightRepository {
    IStorage* storage_; // heap allocation + virtual call overhead
    ILog*     log_;
public:
    FlightRepository(IStorage* s, ILog* l) : storage_(s), log_(l) {}
    void save(const Flight& f) { log_->record("save", f.id()); storage_->persist(f); }
};
```

## Edge Cases & Warnings

| Scenario | Risk | Mitigation |
|----------|------|------------|
| Policy defaults | Missing default causes opaque compile errors | Use `= DefaultStorage` in template parameters |
| Policy interaction | Two policies that share state race | Keep policies stateless or use a context type |
| Over-engineering | Single-use repo needs no policies | Apply only when ≥2 strategies are production-real |
| Concept constraints missing | Substitution failure produces 50-line errors | Add `static_assert(StorageConcept<S>)` for early errors |
