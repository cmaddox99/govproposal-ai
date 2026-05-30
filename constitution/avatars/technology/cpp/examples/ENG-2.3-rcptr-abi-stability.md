---
law_id: ENG-2.3
cpp_version_min: 11
avatar: cpp
context: brownfield-mfc-rcptr
---

# ENG-2.3 — RCPtr ABI Stability (IOC_ALP / Brownfield MFC C++98)

**Law:** [ENG-2.3 — Vertical Slice Architecture](../../laws/engineering/eng-2-architecture.md)
**Avatar:** C++ (Brownfield MSVC/MFC — IOC_ALP PCLoadPlan)
**Pattern:** Custom reference-counted smart pointer (RCPtr<T> / RCObject)

---

## Context

IOC_ALP (PCLoadPlan) was authored ~1999 predating C++11. It uses a hand-rolled
reference-counted smart pointer — `RCPtr<T>` wrapping any class that inherits `RCObject`.

With 650+ usages across the codebase, `RCPtr<T>` is the *de facto* ownership
contract. Introducing `std::shared_ptr<T>` without a boundary creates
mixed-ownership UB at slice boundaries.

---

## NON-COMPLIANT: Mixed Ownership Across Slice Boundary

```cpp
// WRONG: mixed ownership across a vertical slice boundary
// Old code owns via RCPtr; new slice returns std::shared_ptr — double-free risk
RCPtr<CFlight> legacy = dataManager->getFlight(flightId);
std::shared_ptr<CFlight> modern = std::make_shared<CFlight>(*legacy); // copy OK
modern->update(payload);   // modifies copy, legacy ptr unchanged — silent data loss
```

---

## COMPLIANT: Adapter Boundary at Slice Edge

```cpp
// RCObject base — every reference-counted type inherits this
class RCObject {
public:
    void addReference()    { ++refCount_; }
    void removeReference() { if (--refCount_ == 0) delete this; }
    bool isShared() const  { return refCount_ > 1; }
protected:
    RCObject() : refCount_(0) {}
    virtual ~RCObject() {}
private:
    int refCount_;
};

// Slice boundary adapter: wrap RCPtr in a value copy for the new slice
class FlightSliceAdapter {
public:
    // Accept by RCPtr (legacy ownership) — copy data into value object
    explicit FlightSliceAdapter(RCPtr<CFlight> src)
        : flightNumber_(src->getFlightNumber()),
          departureTime_(src->getDepartureTime()),
          zfw_(src->getZFW()) {}

    // New slice works with plain value — no RCPtr dependency
    std::string flightNumber() const { return flightNumber_; }
    double      zfw()          const { return zfw_; }

private:
    std::string flightNumber_;
    time_t      departureTime_;
    double      zfw_;
};
```

---

## ABI Stability Rule

When adding a new vertical slice that touches `RCPtr<T>` objects:

1. **Never store `RCPtr<T>` in a new-slice struct** — copy to value at boundary.
2. **Never return `RCPtr<T>` from new-slice functions** — return value or `std::unique_ptr`.
3. **Characterization test first** — lock the `refCount_` lifecycle before touching.

---

## Characterization Test (before modernizing)

```cpp
TEST(RCPtrCharacterization, FlightRefCountLifecycle) {
    RCPtr<CFlight> a = dataManager->getFlight("AA100");
    EXPECT_FALSE(a->isShared());   // sole owner
    {
        RCPtr<CFlight> b = a;      // addReference called
        EXPECT_TRUE(a->isShared());
    }                              // removeReference — b destroyed
    EXPECT_FALSE(a->isShared());   // back to sole owner, not deleted
}
```

Per [ENG-2.3](../../laws/engineering/eng-2-architecture.md): isolate legacy
ownership at slice boundaries; never leak `RCPtr<T>` into modernized layers.

## Edge Cases & Warnings

- **`RCPtr<T>` and `std::shared_ptr<T>` must never alias the same object** — Reference counts are separate; double-free occurs when both go out of scope. At DLL boundaries, transfer ownership via a factory that wraps to `shared_ptr` with a no-op deleter.
- **`addReference`/`removeReference` are not thread-safe in CWR** — The CWR `RCPtr` uses non-atomic increment/decrement. Concurrent JNI and Java host thread access requires a mutex guard or migration to `std::shared_ptr`.
