---
law_id: ENG-3.3
cpp_version_min: 98
avatar: cpp
---

# [ENG-3.3](laws/engineering/eng-3-code-quality.md): Law of Demeter — C++ Examples

## COMPLIANT: Tell, Don't Ask

```cpp
class BookingService {
public:
    void confirm(BookingId id) {
        auto booking = repository_.find(id);
        booking.confirm();  // Tell the object what to do
        repository_.save(booking);
    }
private:
    BookingRepository& repository_;
};
```

**Why compliant:** `BookingService` tells `Booking` to confirm itself. Doesn't reach into internal state.

## NON-COMPLIANT: Train Wreck Chain

```cpp
void confirm(BookingId id) {
    auto booking = repository_.find(id);
    booking.get_status_manager().get_state().set_confirmed(true);
    booking.get_payment().get_processor().charge(booking.get_total());
}
```

**Why non-compliant:** Deep chain of getters violates Demeter. Tightly couples service to internal structure of Booking.

## Why It Matters in C++

In Java or Python, violating Demeter increases coupling but has limited compile-time impact. In C++, every `.get_foo()` in a header forces `#include` of Foo's definition, creating **transitive header dependencies** that:

- Increase compile times exponentially (every change to a deep dependency triggers rebuilds)
- Force implementation details into public headers (breaking encapsulation)
- Create ODR (One Definition Rule) risks in large codebases

## The Rule

1. **Tell, Don't Ask** — call methods on your direct collaborators only
2. Use **forward declarations** and **Pimpl idiom** to break header chains
3. If you see `a.get_b().get_c().do_thing()`, refactor: `a` should expose `do_thing_via_c()` or accept an interface
4. In templates, prefer passing the exact type needed rather than navigating through associated types

## Edge Cases & Warnings

| Scenario | Risk | Safe Approach |
|----------|------|---------------|
| Chain hidden behind a `const` getter on the same class | `this->config().database().host()` looks local but is still a train-wreck chain; LoD violation through self | Flatten: expose `database_host()` directly on the root object; or extract a `DatabaseConfig` value object |
| Friend class used to bypass encapsulation, defeating LoD enforcement | `friend class Scheduler` allows `Scheduler` to access `FlightLeg` internals directly; the coupling is invisible to static tools | Prefer passing the minimal interface the friend needs as a parameter; `friend` is a last resort only for unit-test helpers |
| Intermediate forwarding method on every class creates boilerplate without decoupling | `FlightLeg::get_departure_airport()` just returns `segment_.get_departure().airport()` — same knowledge, more lines | Introduce a domain value object (`DepartureInfo`) that carries the needed data; pass it directly rather than delegating through the chain |
