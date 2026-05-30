---
law_id: ENG-3.1
cpp_version_min: 98
avatar: cpp
---

# [ENG-3.1](laws/engineering/eng-3-code-quality.md): Complexity Limits — C++ Examples

**The Rule:** Functions must have cyclomatic complexity ≤10. Nesting depth must not exceed 3 levels. Decompose complex logic into focused, testable functions.

**Why this matters:** High-complexity functions are exponentially harder to test — a function with cyclomatic complexity 15 needs at minimum 15 test paths. In aviation systems, untested paths can mean missed fare calculations or incorrect crew scheduling.

## COMPLIANT: Low Cyclomatic Complexity

```cpp
// Each function has ONE responsibility, low complexity
Money calculate_discount(const Customer& customer, Money amount) {
    auto tier = customer.loyalty_tier();
    auto rate = discount_rate_for(tier);  // delegation, not nesting
    return amount * rate;
}

double discount_rate_for(LoyaltyTier tier) {
    switch (tier) {
        case LoyaltyTier::kGold:     return 0.15;
        case LoyaltyTier::kSilver:   return 0.10;
        case LoyaltyTier::kBronze:   return 0.05;
        default:                      return 0.0;
    }
    // Cyclomatic complexity: 4 — each case is trivial
}
```

## NON-COMPLIANT: Deeply Nested Conditionals

```cpp
// ❌ Cyclomatic complexity: 8+, nesting depth: 4
Money calculate_discount(const Customer& c, Money amount, bool promo, int day) {
    if (c.is_active()) {
        if (c.loyalty_tier() == kGold) {
            if (promo) {
                if (day == 1) { return amount * 0.3; }
                else { return amount * 0.2; }
            } else { return amount * 0.15; }
        } else { /* more nesting... */ }
    }
    return Money::zero();
}
```

**Edge case:** A `switch` with 20 enum values (e.g., aircraft types) is acceptable IF each case is trivial (one-liner). Complexity tools measure structure, not intent — use `// NOLINT(readability-function-cognitive-complexity)` with justification comment for legitimate large switches.

**Fix pattern:** Replace nested `if` chains with early returns (guard clauses), lookup tables (`std::map<LoyaltyTier, double>`), or strategy pattern.

## Edge Cases & Warnings

| Scenario | Risk | Safe Approach |
|----------|------|---------------|
| Cyclomatic complexity counter ignores template instantiation depth | A function at complexity 5 instantiated with 10 type arguments can have the equivalent of 50 logic paths; static analysis misses the combinatorial explosion | Apply complexity limits to template function bodies as if the most complex instantiation were the only one; add a static assert on the number of accepted template arguments |
| `constexpr if` branches counted as complexity even when dead at compile time | Tool reports high complexity for a function that at runtime has only one active branch | Check whether your tool supports `constexpr if` branch elision; if not, suppress for `constexpr if` blocks with a justification comment |
| Lambda expressions embedded in a function inflate its line-count metric | Cognitive complexity of a 10-line function with a 20-line lambda registers as 30 lines; extraction looks unnecessary | Extract large lambdas into named helper functions or static member functions; lambdas should be ≤5 lines |

## See Also

- [ENG-3.1-comparison-operators.md](ENG-3.1-comparison-operators.md) — Manual 6-operator (C++98/11/14), `std::tie`, and C++20 spaceship operator
- [ENG-3.1-sfinae-cpp11.md](ENG-3.1-sfinae-cpp11.md) — `enable_if` SFINAE patterns (C++11/14); concepts migration path to C++20
