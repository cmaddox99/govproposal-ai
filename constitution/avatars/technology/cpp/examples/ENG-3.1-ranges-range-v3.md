---
law_id: ENG-3.1
cpp_version_min: 14
cpp_version_note: >-
  Uses ericniebler/range-v3 (Boost Software License) for C++14 teams.
  range-v3 is the reference implementation for C++20 ranges; migration is
  mostly namespace substitution but verify const-iterator usage.
avatar: cpp
---

# [ENG-3.1](laws/engineering/eng-3-complexity.md): Ranges Pipeline — range-v3 Bridge (C++14)

**Avatar:** C++ (Transitional C++14 — CWR / IOC_ALP)
**Pattern:** Composable filter/transform/take pipelines via `ericniebler/range-v3`

## Context

Raw iterator loops with manual filter and accumulation scatter intent across
dozens of lines. Per [ENG-3.1](laws/engineering/eng-3-complexity.md), prefer
composable pipelines that express what to compute, not how to iterate.

[ericniebler/range-v3](https://github.com/ericniebler/range-v3) (Boost
Software License, Eric Niebler) is the reference implementation for C++20
`std::ranges`. It runs on C++14 and later.

⚠️ **Critical namespace warning:** range-v3 uses the `ranges::` namespace;
C++20 uses `std::ranges::`. **Do not mix headers from both** in the same
translation unit — `filter_view` const-iterability semantics differ and the
resulting ODR violations are silent.

## COMPLIANT — Filter / Transform / Take Pipeline

```cpp
// flight_query.cpp  (CWR / IOC_ALP — C++14)
#include <range/v3/view/filter.hpp>
#include <range/v3/view/transform.hpp>
#include <range/v3/view/take.hpp>
#include <range/v3/range/conversion.hpp>

struct FlightLeg {
    std::string flight_id;
    std::string origin;
    std::string dest;
    int         duration_min;
    bool        is_international;
};

// Returns the first N short domestic legs — no raw loops, intent is explicit.
std::vector<std::string>
short_domestic_flight_ids(const std::vector<FlightLeg>& legs, int max_results)
{
    using namespace ranges;

    return legs
        | views::filter([](const FlightLeg& l) {
              return !l.is_international && l.duration_min < 180;
          })
        | views::transform([](const FlightLeg& l) { return l.flight_id; })
        | views::take(max_results)
        | to<std::vector<std::string>>();
}
```

**Why this is clear:** Each stage names its purpose. The compiler proves at
compile time that the types flow correctly through the pipeline. No temporary
vectors are allocated — range-v3 views are lazy.

## COMPLIANT — ranges::sort (In-Place)

```cpp
#include <range/v3/algorithm/sort.hpp>

void sort_by_duration(std::vector<FlightLeg>& legs)
{
    // ranges::sort accepts the container directly — no begin()/end() pair.
    ranges::sort(legs, {}, &FlightLeg::duration_min);
    //                 ^     ^
    //                 |     projection: sort key extracted from member
    //                 comparator: {} means default less<>
}
```

## NON-COMPLIANT

```cpp
// WRONG: raw iterator loop — intent buried in bookkeeping
std::vector<std::string>
short_domestic_flight_ids_raw(const std::vector<FlightLeg>& legs, int max_results)
{
    std::vector<std::string> result;
    for (std::vector<FlightLeg>::const_iterator it = legs.begin();
         it != legs.end() && static_cast<int>(result.size()) < max_results;
         ++it)
    {
        if (!it->is_international && it->duration_min < 180) {
            result.push_back(it->flight_id);
        }
    }
    return result;
    // Intent: "give me the IDs of the first N short domestic legs"
    // is invisible. A reviewer must parse all four concerns simultaneously:
    // iteration, filtering, projection, and early termination.
}

// WRONG: mixing range-v3 and C++20 headers in same TU
#include <range/v3/view/filter.hpp>  // range-v3: ranges::filter_view
#include <ranges>                    // C++20: std::ranges::filter_view
// ODR violation — filter_view has two definitions; linker behavior undefined.
```

## C++20 Migration Note

range-v3 IS the reference implementation for C++20 ranges (P0896). Most code
migrates by changing namespace and headers:

```cpp
// C++14 (range-v3)                   →  C++20 (standard library)
#include <range/v3/view/filter.hpp>   →  #include <ranges>
#include <range/v3/view/transform.hpp>  (same header covers all views)
#include <range/v3/algorithm/sort.hpp> →  (included via <algorithm>)

ranges::views::filter(...)            →  std::views::filter(...)
ranges::views::transform(...)         →  std::views::transform(...)
ranges::sort(...)                     →  std::ranges::sort(...)
| ranges::to<std::vector>()           →  | std::ranges::to<std::vector>()  (C++23)
                                         or collect via std::vector(r.begin(), r.end())
```

**Before migrating, verify:** `filter_view` in range-v3 requires the predicate
to accept `const T&`; C++20 `std::ranges::filter_view` requires a
`copyable` predicate. Stateful lambdas that capture by mutable reference may
need adjustment.

## Attribution

[ericniebler/range-v3](https://github.com/ericniebler/range-v3) — Boost
Software License 1.0, © Eric Niebler. Standardized as C++20 `std::ranges`
(P0896R4).

## Edge Cases & Warnings

- **`ranges::` vs `std::ranges::` — never mix in one TU:** range-v3 and
  C++20 headers define the same names in different namespaces. Including both
  in one translation unit creates ODR violations. The `filter_view`
  const-iterability contract differs: range-v3's `filter_view` is not
  const-iterable (const member `begin()` is deleted); C++20's is — if you
  call `begin()` on a `const filter_view` today under range-v3, your code
  will silently compile differently after migration.

- **Lazy evaluation and iterator invalidation:** range-v3 views are lazy —
  they hold iterators into the source range. If the source `std::vector` is
  modified (push_back, resize, erase) while a view pipeline is alive, all
  iterators are invalidated. Materialize the result with `| to<std::vector>()`
  before mutating the source.

- **`views::take` on an empty range:** Safe — returns an empty view, not
  undefined behavior. `views::take(0)` is also safe and produces an empty view.

- **Projection syntax in `ranges::sort`:** The third argument to `ranges::sort`
  is a projection, not a comparator. Pass `{}` (default comparator) as second
  and `&T::member` as third. Passing a member pointer as second argument is
  a compile error — which is the correct behavior catching a common mistake.

- **`| to<std::vector>()` requires range-v3 ≥ 0.11:** Earlier versions used
  `ranges::to_vector`. Pin your range-v3 version in the build system.

Per [ENG-3.1](laws/engineering/eng-3-complexity.md): use composable range
pipelines to reduce cyclomatic complexity in collection-processing code. Raw
iterator loops with manual filter accumulation obscure intent and resist review.
