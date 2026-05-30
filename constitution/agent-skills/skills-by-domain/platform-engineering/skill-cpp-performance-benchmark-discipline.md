---
skill:
  id: skill-cpp-performance-benchmark-discipline
  name: "C++ Performance Benchmark Discipline"
  category: platform-engineering
  version: "1.0.0"
  avatar: cpp

laws:
  implements:
    - id: ENG-3.1
      title: Complexity Limits Law
  references:
    - id: ENG-4.1
      title: Atomic TDD Law
    - id: ENG-6.7
      title: Audit Trail Law

triggers:
  phrases:
    - "C++ performance benchmark"
    - "C++ micro-benchmark"
    - "C++ optimization measurement"
    - "C++ latency budget"

followed_by:
  - skill-08-code-review
  - skill-27-constitution-compliance
---

# Skill: C++ Performance Benchmark Discipline

## Purpose

Ensure performance-critical C++ code has reproducible benchmarks and that optimizations are measured, not assumed. Per [ENG-3.1](laws/engineering/eng-3-code-quality.md), complexity reductions must be validated with data.

## Procedure

1. **Write benchmarks first** — before optimizing, create a Google Benchmark or Catch2 benchmark that captures the current baseline
2. **Measure before and after** — record wall time, CPU time, and allocations; commit results to the PR description
3. **Set latency budgets** — critical paths must declare a latency budget (e.g., "< 10μs p99") in the function's documentation
4. **Prevent regression** — CI should flag benchmark regressions > 10% as warnings; > 25% as blocking failures

## Governance Gate

Per [ENG-3.1](laws/engineering/eng-3-code-quality.md), any optimization PR that does not include before/after benchmark data is incomplete and should be sent back for measurement.

## C++ Specific Patterns

- Use `google/benchmark` with `BENCHMARK_MAIN()` for micro-benchmarks
- Compile benchmarks with `-O2 -DNDEBUG` (Release mode) for realistic measurements
- Use `DoNotOptimize()` and `ClobberMemory()` to prevent dead-code elimination
- Track allocations with custom allocators or ASan's allocation profiling
