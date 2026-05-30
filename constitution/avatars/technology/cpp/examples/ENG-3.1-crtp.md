---
law_id: ENG-3.1
cpp_version_min: 11
avatar: cpp
---

# [ENG-3.1](laws/engineering/eng-3-code-quality.md): CRTP — Curiously Recurring Template Pattern (C++11)

Per [ENG-3.1](laws/engineering/eng-3-code-quality.md), CRTP achieves static
polymorphism — zero virtual dispatch overhead, inlined by the compiler.

## CRTP vs. Virtual Trade-Off

| | CRTP | `virtual` |
|---|---|---|
| Dispatch cost | Zero (inlined) | vptr indirection |
| Runtime polymorphism | ❌ No | ✅ Yes |
| Heterogeneous container | ❌ No | ✅ Yes |
| Use when | Hot path, mixin | Plugins, type-erased |

## COMPLIANT: Static Polymorphism via `Serializable<Derived>`

```cpp
template<typename Derived>
class Serializable {
protected:
    Derived& derived() { return static_cast<Derived&>(*this); }
    // available for mixins needing non-const access

public:
    std::string to_string() const {
        return static_cast<const Derived&>(*this).serialize(); // ✅ static dispatch
    }
};

struct FlightRecord : Serializable<FlightRecord> {
    FlightId id;
    std::string serialize() const {
        return "FL-" + std::to_string(id.value);
    }
};

FlightRecord r{FlightId{42}};
auto s = r.to_string();  // ✅ inlined — no vptr, no heap
```

## COMPLIANT: CRTP Mixin for Audit Logging

```cpp
template<typename Derived>
class AuditLogged {
public:
    template<typename Fn>
    auto with_audit(std::string_view op, Fn&& fn) {
        log_entry(op, "BEGIN");
        auto result = fn(static_cast<Derived&>(*this));  // ✅ zero overhead
        log_entry(op, "END");
        return result;
    }
};

struct BookingService : AuditLogged<BookingService> {
    Booking create(const PNR& pnr) {
        return with_audit("create", [&](BookingService& s) {
            return s.do_create(pnr);
        });
    }
};
```

## NON-COMPLIANT: RTTI `dynamic_cast` Chain

```cpp
// ❌ RTTI dispatch — O(n) vtable walk, throws on mismatch, non-inlinable
void serialize(Serializable* obj) {
    if (auto* fr = dynamic_cast<FlightRecord*>(obj))
        fr->serialize();
    else if (auto* br = dynamic_cast<BookingRecord*>(obj))  // ❌ grows with types
        br->serialize();
    // ... every new type requires editing this function
}
```

## Edge Cases

### Inheritance Depth

CRTP does not support deep hierarchies. `Derived` cannot itself be a CRTP
base for a further subclass without explicit re-templating. Limit to one
or two levels.

### C++20 Replacement: Concepts

C++20 concepts replace many CRTP uses without the template machinery:

```cpp
// C++20 — concept constrains directly; no base class required
template<typename T>
concept Serialisable = requires(const T& t) { { t.serialize() } -> std::convertible_to<std::string>; };

template<Serialisable T>
std::string to_string(const T& obj) { return obj.serialize(); }  // ✅ cleaner
```
