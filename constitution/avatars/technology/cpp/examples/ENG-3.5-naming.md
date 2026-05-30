---
law_id: ENG-3.5
cpp_version_min: 98
avatar: cpp
---

# [ENG-3.5](laws/engineering/eng-3-code-quality.md): Naming — C++ Examples

## COMPLIANT: Intention-Revealing Names

```cpp
class FlightSearchService {
public:
    std::vector<Flight> find_available_flights(
        AirportCode origin, AirportCode destination, Date departure_date
    ) {
        auto candidates = route_repository_.find_by_route(origin, destination);
        return filter_by_availability(candidates, departure_date);
    }

private:
    std::vector<Flight> filter_by_availability(
        const std::vector<Flight>& flights, Date date
    );
    RouteRepository& route_repository_;
};
```

**Why compliant:** Class, method, and parameter names reveal intent. No abbreviations. Domain language used consistently.

## NON-COMPLIANT: Cryptic Names

```cpp
class FSS {
    std::vector<F> srch(std::string o, std::string d, int dt) {
        auto c = rr_.fb(o, d);
        return flt(c, dt);
    }
    RR& rr_;
};
```

**Why non-compliant:** Single-letter and abbreviated names. Impossible to understand without context. Violates naming conventions.

## C++ Naming Convention Table

| Element | Convention | Example |
|---------|-----------|---------|
| Types / Classes | `PascalCase` | `FlightPlan`, `BookingService` |
| Functions / Methods | `snake_case` | `find_available()`, `reserve_seat()` |
| Local variables | `snake_case` | `departure_date`, `seat_count` |
| Member variables | `snake_case_` (trailing underscore) | `pnr_`, `segments_` |
| Constants | `kPascalCase` | `kMaxRetries`, `kDefaultTimeout` |
| Namespaces | `snake_case` | `aa::crew`, `aa::booking` |
| Enum values | `kPascalCase` | `OrderStatus::kDraft` |
| Template params | `PascalCase` | `template<typename ValueType>` |
| Macros (avoid) | `ALL_CAPS` | `AA_PLATFORM_LINUX` |

**The Rule:** Names reveal intent. Abbreviations are prohibited except industry-standard terms (`pnr`, `iata`, `icao`). Domain language from the aviation ubiquitous language takes precedence over generic programming terms.

## Edge Cases & Warnings

| Scenario | Risk | Safe Approach |
|----------|------|---------------|
| Reserved identifiers: names beginning with `_` followed by an uppercase letter (e.g., `_Value`) or containing `__` anywhere | These are reserved for the implementation in all C++ scopes; using them is undefined behaviour even if your compiler currently allows it | Prefix private members with `m_` or suffix with `_`; use project-scoped macros like `AA_FEATURE_X` rather than `_AA_FEATURE_X` |
| Macro name collisions with system or third-party headers | `#define MAX 255` overrides `std::max`'s helper macros; `#define ERROR 1` collides with Windows SDK | Always namespace macros with a project prefix (`AA_MAX`, `CWR_ERROR`); include system headers before defining macros |
| Domain term that is an acronym treated as a word in PascalCase | Team disagrees: `IataCode` vs `IACode` vs `IATACode`; inconsistency across files | Establish a project glossary of approved acronym capitalisations; lint with a custom `clang-tidy` check or grep-based CI rule |
