# Tasks: cpp-external-sources-enrichment

**Laws governing this work:** `ENG-11.1`, `ENG-11.2`, `ENG-4.1`, `ENG-3.1`, `ENG-6.1`, `ENG-5.2`, `ENG-10.1`

## Progress Summary

- Completed: 73 / 73 core tasks (+ 10 Amendment A panel-fix tasks + 5 Amendment D tasks)
- In Progress: 0
- Blocked: 0
- Version Annotated (ESE-V1/CBF-12): 48 / 51 substantive tasks
- **Status: CLEAR TO MERGE** — Amendment D implemented (commit `b7008bd`); Amendment D confirmation panel complete (2026-04-28); 350-scenario cross-version RAG eval added (commit `46f9c2a`)
- **Amendment D: COMPLETE** — D-3/D-4/D-5 fully resolved; D-1/D-2 partially resolved (see Phase 12 Amendment E backlog)
- **Amendment E: 8 tasks pending** — Panel follow-up items, none blocking merge. See Phase 12.

---

## Phase 0.5: Version Routing Wiring ⛔ MUST COMPLETE BEFORE PHASE 1

> **Mandate:** Per version-sensitivity review (Round 3), all ESE deliverables must be wired into the 5-tier routing system before any content task executes. Failure to complete Phase 0.5 causes CI failure (`test_phase2d_c4_ref_frontmatter.py`) and recreates the pre-PR#47 routing failures.

- [x] ESE-V1 ✓ — `cpp_version_min` annotated on all 48 substantive tasks (CBF-12). Distribution: 22×C++20, 4×C++17, 18×C++11, 2×C++14, 2×C++98.
- [x] ESE-V2 ✓ — `AVATAR-RAG-INDEX.yaml` fully wired (CBF-13): tier prefer/avoid lists updated; FORWARD-DECLARATIONS comment block replaced with real entries.
- [x] ESE-V3 ✓ — `ref-cpp20-features-part1.md` + `ref-cpp20-features-part2.md` confirmed (CBF-14). All task references updated.
- [x] ESE-V4 ✓ — `ref-concurrency-advanced-part1.md` + `ref-concurrency-advanced-part2.md` confirmed (CBF-14). All task references updated.
- [x] ESE-V5 ✓ — ESE-56–65 bridge deliverables confirmed: ESE-56/57/58/59/60/61/62/64/65 pre-created by CBF; ESE-63 pre-created by CBF-09 in ref-brownfield-survival.md. All properly sequenced.

---

## Phase 0: Hangar SDD Execution Artifacts

> **Goal:** Establish governed execution artifacts for this change.

- [x] ESE-00.1 ✓ — `PROPOSAL.md` created (this document)
- [x] ESE-00.2 ✓ — `tasks.md` created (this document)
- [x] ESE-00.3 ✓ 4cbe534 — Record governance sign-off and author review in a `PROGRESS.md` file

---

## Phase 1: P1 Critical Gaps — C++20 Features

> **Goal:** Cover the five P1 C++20 gaps that are actively missing from AA C++ development guidance. Each task produces one new file or a targeted section addition. Per ENG-4.1, each example file must contain at least one COMPLIANT and one NON-COMPLIANT code block with explicit rationale.

### Phase 1a: New C++20 Features — Part 1 (`ref-cpp20-features-part1.md`) + Part 2 (`ref-cpp20-features-part2.md`) reference files

- [x] ESE-01 ✓ (CBF-13) — Skeletons already on disk: `ref-cpp20-features-part1.md` and `ref-cpp20-features-part2.md` created by CBF-13.
- [x] ESE-02 ✓ 4046994 — `cpp_version_min: 20` — Add **C++20 Modules** section to `ref-cpp20-features-part1.md`: `export module`, `import`, module partitions (`module M:Part`), global module fragment (`module;`), header units vs. module interfaces, and CMake `target_sources(PRIVATE FILE_SET CXX_MODULES FILES ...)` wiring. Cite C++ Core Guidelines SF.xx. Copyright note: original examples only.
- [x] ESE-03 ✓ — `cpp_version_min: 20` — Add **Ranges and Views** section to `ref-cpp20-features-part1.md`: `std::ranges::sort` vs. iterator-pair sort, `std::views::filter | std::views::transform | std::views::take` pipeline, lazy evaluation semantics, `std::ranges::to<std::vector>` materialization (C++23 preview note), sentinel types, and bounded vs. unbounded ranges. AA domain example: pipeline over `std::span<const FlightLeg>`. Cite Core Guidelines ES.1 (prefer standard library) and P.3 (express intent). Copyright note: original examples only (Josuttis C++20 concept reference only).
- [x] ESE-04 ✓ — `cpp_version_min: 20` — Add **std::span governance** section to `ref-cpp20-features-part1.md`: span vs. raw array vs. vector reference; span as "non-owning view"; subspan patterns; span in function signatures (replaces pointer+count per Core Guidelines I.xx); bounds checking with `std::span::operator[]` vs. `.at()`-equivalent; `std::span<const T>` for read-only APIs. Cite Core Guidelines I.12 (use not_null), P.6 (bounds checkable at runtime). Copyright note: Core Guidelines examples adaptable with attribution; Josuttis C++20 concept reference only.
- [x] ESE-05 ✓ — `cpp_version_min: 20` — Add **Three-way comparison (spaceship operator)** section to `ref-cpp20-features-part1.md`: ordering category types (`std::strong_ordering`, `std::weak_ordering`, `std::partial_ordering`); `auto operator<=>(const T&) const = default`; custom operator<=> with heterogeneous types; interaction with operator== when spaceship is defined; migration path from manual </>/<=/>=. AA domain example: `FlightId` and `RouteKey` value types. Cite Core Guidelines C.11 (regular types) and ENG-3.2 (Immutability). Copyright note: original examples only.
- [x] ESE-06 ✓ — `cpp_version_min: 20` — Add **std::format** section to `ref-cpp20-features-part1.md`: `std::format` vs. printf/sprintf/stringstream; format string type-safety (compile-time type checks eliminate printf-style mismatch UB); `std::format_to` for output iterators; `std::formatter<T>` specialization for custom types (e.g., `FlightId`, `PNR`); `std::vformat` for runtime format strings and why to avoid it. Cite Core Guidelines ES.45 (no magic strings), ENG-6.5 (input validation). Copyright note: original examples only.
- [x] ESE-07 ✓ — `cpp_version_min: 20` — Add **std::bit_cast** section to `ref-cpp20-features-part1.md`: bit_cast as type-safe replacement for `reinterpret_cast + memcpy` type-punning; constraints (same size, trivially copyable); `std::bit_cast<uint32_t>(float_value)` for IEEE-754 inspection; binary protocol parsing for ACARS/ADS-B messages. Cite Core Guidelines ES.49 (use named casts), ENG-6.1 (no reinterpret_cast without documented justification). Copyright note: original examples only.
- [x] ESE-08 ✓ — `cpp_version_min: 20` — Add **std::source_location** section to `ref-cpp20-features-part1.md`: `std::source_location::current()` as default parameter in logging functions; comparison with `__FILE__`/`__LINE__` macros; stack-free structured location capture for ENG-6.7 audit logging; thread-safe usage. Cite Core Guidelines ES.30/31 (don't use macros), ENG-5.5 (Observability), ENG-6.7 (Audit Trail). Copyright note: original examples only.
- [x] ESE-09 ✓ — `cpp_version_min: 20` — Add **constinit** section to `ref-cpp20-features-part1.md`: `constinit` vs. `constexpr` vs. `const`; initialization order fiasco prevention; `constinit` for mutable globals that must be zero-initialized before first use (e.g., flight-count accumulators); `constinit constexpr` combination. Cite Core Guidelines Con.5 (use constexpr for values), ENG-3.1 (complexity). Copyright note: original examples only.
- [x] ESE-10 ✓ — `cpp_version_min: 20` — Add **std::atomic_ref** section to `ref-cpp20-features-part1.md`: `std::atomic_ref<T>` for atomic access to non-atomic objects (legacy structs); use case for brownfield code where adding `std::atomic<T>` members would break ABI; constraints (alignment, trivially copyable). Cite Core Guidelines CP.xx, ENG-6.1. Copyright note: original examples only.
- [x] ESE-11 ✓ — `cpp_version_min: 20` — Add **C++20 Coroutine Generators** section to `ref-cpp20-features-part2.md`: `co_yield` mechanics; custom `Generator<T>` promise_type with iteration support; lazy sequence over flight results; cancellable generator with stop_token; comparison with `std::generator` (C++23 preview). Build on ENG-3.1-coroutines.md (co_await) — this section focuses on co_yield generator pattern not covered there. Copyright note: original examples only.

### Phase 1b: New example files for P1 C++20 gaps

- [x] ESE-12 ✓ — `cpp_version_min: 20` — Create `avatars/technology/cpp/examples/ENG-3.1-ranges-views.md`: COMPLIANT example using `std::views` pipeline to replace a raw loop over flight legs (ENG-3.1 complexity — ranged algorithms reduce complexity). NON-COMPLIANT example using manual iterator loop. Edge cases: infinite ranges, owning vs. non-owning views, dangling reference from temporary range. ≤ 700 tokens.
- [x] ESE-13 ✓ — `cpp_version_min: 20` — Create `avatars/technology/cpp/examples/ENG-3.1-modules.md`: COMPLIANT `export module aa.flight` with partition `aa.flight:domain`; import in a consumer; CMake `FILE_SET CXX_MODULES` configuration. NON-COMPLIANT pattern: `#include` cycle that modules solve. Edge cases: legacy header units (`import <vector>`), mixing modules with traditional headers. ≤ 700 tokens.
- [x] ESE-14 ✓ — `cpp_version_min: 20` — Create `avatars/technology/cpp/examples/ENG-3.2-spaceship-operator.md`: COMPLIANT `FlightId` value type with `auto operator<=>() const = default`; custom partial_ordering for `FlightAltitude` (NaN handling); interaction with map/set ordering. NON-COMPLIANT: hand-rolling six comparison operators instead. Edge cases: partial_ordering with NaN-equivalent sentinel values. ≤ 700 tokens.
- [x] ESE-15 ✓ — `cpp_version_min: 20` — Create `avatars/technology/cpp/examples/ENG-6.1-span-bounds-safety.md`: COMPLIANT function accepting `std::span<const SeatData>` instead of `const SeatData* data, size_t len`; subspan for row range; `std::as_bytes` for binary serialization. NON-COMPLIANT: raw pointer + size pair. Edge cases: empty span, span to temporary (dangling), span-of-span. ≤ 700 tokens.
- [x] ESE-16 ✓ — `cpp_version_min: 20` — Create `avatars/technology/cpp/examples/ENG-6.1-std-format.md`: COMPLIANT `std::format` for audit log message vs. NON-COMPLIANT `sprintf`. Custom `std::formatter<FlightId>` specialization. Runtime format string hazard and `std::vformat` warning. ≤ 700 tokens.

---

## Phase 2: P1 Critical Gaps — Concurrency

> **Goal:** Cover two P1 concurrency gaps that directly affect safety-critical AA concurrent code.

- [x] ESE-17 ✓ — `cpp_version_min: 11` — Create `avatars/technology/cpp/examples/ENG-6.1-memory-ordering.md`: systematic treatment of all five `std::memory_order` values with happens-before reasoning. COMPLIANT: acquire/release for producer-consumer handoff; relaxed for independent counters; seq_cst cost trade-off note. NON-COMPLIANT: using `memory_order_relaxed` for dependent reads (broken happens-before). Edge cases: acq_rel for read-modify-write, release sequence through non-atomic RMW, seq_cst in multi-producer scenarios. ≤ 700 tokens. Copyright note: original examples; concept from Williams 2019 (reference only).
- [x] ESE-18 ✓ — `cpp_version_min: 17` — Create `avatars/technology/cpp/examples/ENG-6.1-parallel-algorithms.md`: COMPLIANT flight-data batch processing using `std::execution::par_unseq` with `std::transform`; `std::execution::seq` for deterministic tests; `par` for I/O-constrained work. NON-COMPLIANT: assuming order of execution with `par_unseq`. Edge cases: exception handling in parallel (first exception propagated), data race with shared mutable state, alignment requirements for SIMD (`par_unseq`). ≤ 700 tokens. Copyright note: original examples only.

---

## Phase 3: P1 Critical Gaps — Templates and Core Guidelines

> **Goal:** Cover CRTP (cited but undocumented) and Interface Design rules (Expects/Ensures).

- [x] ESE-19 ✓ — `cpp_version_min: 11` — Create `avatars/technology/cpp/examples/ENG-3.1-crtp.md`: CRTP for static polymorphism — `template<typename Derived> class Serializable` with `derived().serialize()` call; CRTP mixin pattern for logging without virtual overhead; CRTP vs. virtual trade-off table. NON-COMPLIANT: RTTI-based dispatch (`dynamic_cast` chain). Edge cases: CRTP and inheritance depth limits, CRTP with concepts (C++20 CRTP replacement pattern). ≤ 700 tokens. Copyright note: original examples; concept from Vandevoorde 2017 (reference only).
- [x] ESE-20 ✓ — `cpp_version_min: 14` — Add **Interface Design Rules (I.xx)** section to `avatars/technology/cpp/refs/language/ref-core-type-safety.md`: I.1 (explicit contract); I.3 (avoid singletons); I.11 (never transfer ownership by raw pointer — use unique_ptr or span); I.12 (use not_null<T*> for never-null pointers); Expects/Ensures macros from GSL; precondition/postcondition documentation style; I.23 (keep parameter count low, use aggregates). Cite Core Guidelines I.1, I.3, I.11, I.12, I.23 with URLs. Copyright note: Core Guidelines adaptable with MIT attribution.

---

## Phase 4: P2 High-Priority Concurrency Gaps

> **Goal:** Fill the eight remaining P2 concurrency gaps with a new advanced concurrency reference file and targeted examples.

### Phase 4a: Advanced Concurrency — Part 1 (`ref-concurrency-advanced-part1.md`) + Part 2 (`ref-concurrency-advanced-part2.md`) reference files

- [x] ESE-21 ✓ (CBF-13) — Skeletons already on disk: `ref-concurrency-advanced-part1.md` and `ref-concurrency-advanced-part2.md` created by CBF-13.
- [x] ESE-22 ✓ b62edb8 — `cpp_version_min: 20` — Add **std::jthread and std::stop_token** section to `ref-concurrency-advanced-part2.md`: `jthread` auto-join on destruction; `stop_token` cooperative cancellation; `stop_callback` for cleanup; migration from `std::thread` + `std::atomic<bool>` stop-flag pattern. AA domain example: cancellable fare-search background thread. Cite Core Guidelines CP.25 (prefer joining thread). Copyright note: original examples only.
- [x] ESE-23 ✓ 2804575 — `cpp_version_min: 11` — Add **Condition Variable Patterns** section to `ref-concurrency-advanced-part1.md`: CP.42 rule (always wait-with-predicate to prevent spurious wakeup); bounded producer-consumer queue; `notify_one` vs. `notify_all` semantics; `condition_variable_any` for stop_token integration; avoiding missed-wakeup bug. AA domain example: booking request queue with bounded backpressure. Copyright note: original examples; Core Guidelines CP.42 adaptable with attribution.
- [x] ESE-24 ✓ f4d65f1 — `cpp_version_min: 11` — Add **Lock-free Data Structures** section to `ref-concurrency-advanced-part1.md`: lock-free concepts; when lock-free is NOT faster (cache line contention); ABA problem and mitigation (version counter / hazard pointers); lock-free SPSC (single-producer single-consumer) ring buffer pattern; `std::atomic<shared_ptr<T>>` for **atomic** (not necessarily lock-free) node update (C++20) — `is_lock_free()` may return false; always check. Warnings: lock-free is rarely appropriate for application-layer code; always profile first. Copyright note: original examples; concept from Williams 2019 (reference only).
- [x] ESE-25 ✓ 14cf3e9 — `cpp_version_min: 11` — Add **Thread Pool and Work-Stealing** section to `ref-concurrency-advanced-part1.md`: producer-consumer thread pool skeleton; work-stealing deque concept for load balancing; `std::async` with thread pool executor vs. launching new threads; AA use case: parallel crew pairing feasibility checks. Cite Core Guidelines CP.41 (minimize thread creation). Copyright note: original examples; concept from Williams 2019 (reference only).
- [x] ESE-26 ✓ 5bca8c0 — `cpp_version_min: 17` — Add **False Sharing and Cache Line Alignment** section to `ref-concurrency-advanced-part1.md`: false sharing definition; cache line size (64 bytes on x86); `alignas(std::hardware_destructive_interference_size)` pattern; padding structs to separate hot counters; example: per-thread statistics accumulator. Cite Core Guidelines Per.xxx. Copyright note: original examples; concept from Williams 2019 (reference only).
- [x] ESE-27 ✓ f7159df — `cpp_version_min: 11` — Add **std::promise and std::future Patterns** section to `ref-concurrency-advanced-part1.md`: `std::promise<T>` / `std::future<T>` for async result passing; `std::packaged_task` for deferred execution; `std::shared_future` for multi-consumer results; exception propagation through `set_exception`; relationship to `std::async`. AA domain example: async fare availability check with timeout via `future::wait_for`. Copyright note: original examples only.
- [x] ESE-28 ✓ 9b6b983 — `cpp_version_min: 11` — Add **Amdahl's Law and Gustafson's Law** section to `ref-concurrency-advanced-part1.md`: Amdahl's equation; serial fraction bottleneck; practical implications (20% serial code = max 5x speedup regardless of core count); Gustafson's law for data-parallel work; measuring serial fraction; when to not parallelize. Context: crew scheduling optimizers and fare combinatorics. Copyright note: original derivation; concept from Williams 2019 (reference only).
- [x] ESE-29 ✓ 975f3b3 — `cpp_version_min: 20` — Add **CP.51/CP.52/CP.53 rules** to existing `avatars/technology/cpp/ref-concurrency.md` as a dedicated "Coroutine-Concurrency Safety" sub-section: CP.51 (no capturing lambdas as coroutines — closure goes out of scope at suspension); CP.52 (no locks held across suspension points — deadlock); CP.53 (no reference parameters to coroutines — referenced object may not survive to resumption). Cross-reference ENG-3.1-coroutines.md. Cite Core Guidelines CP.51/52/53 with URLs. Copyright note: Core Guidelines adaptable with MIT attribution.

### Phase 4b: New example files for P2 concurrency

- [x] ESE-30 ✓ 02b4784 — `cpp_version_min: 20` — Create `avatars/technology/cpp/examples/ENG-6.1-jthread-stop-token.md`: COMPLIANT jthread + stop_token for cancellable background validation task. NON-COMPLIANT: raw thread + volatile bool stop flag (data race). Edge cases: stop_callback cleanup, jthread with coroutines. ≤ 700 tokens.
- [x] ESE-31 ✓ d05e00d — `cpp_version_min: 11` — Create `avatars/technology/cpp/examples/ENG-6.1-condition-variable.md`: COMPLIANT bounded queue using condition_variable with wait(lock, predicate). NON-COMPLIANT: wait() without predicate (spurious wakeup). Edge cases: lost wakeup race condition, notify before wait, cv with stop_token. ≤ 700 tokens.
- [x] ESE-32 ✓ c1806bd — `cpp_version_min: 17` — Create `avatars/technology/cpp/examples/ENG-3.1-false-sharing.md`: COMPLIANT per-thread counter with `alignas(std::hardware_destructive_interference_size)` padding. NON-COMPLIANT: naively adjacent counters in array. Performance impact note and when to apply. ≤ 700 tokens.

---

## Phase 5: P2 High-Priority Template Gaps

> **Goal:** Enrich `ref-advanced-cpp.md` with type traits, tag dispatching, advanced concepts, and NTTP; add policy-based design example.

- [x] ESE-33 — `cpp_version_min: 11` — Add **Type Traits Reference** section to `ref-advanced-cpp.md`: systematic table of `std::is_*`, `std::remove_cv_t`, `std::remove_reference_t`, `std::decay_t`, `std::conditional_t`, `std::enable_if_t`; custom type trait pattern (`has_serialize_v<T>`); trait composition with `std::conjunction`/`std::disjunction`/`std::negation`. Governance: prefer concepts for new code; use type traits for constexpr if branches and brownfield compatibility. Copyright note: original examples; concept from Vandevoorde 2017 (reference only).
- [x] ESE-34 — `cpp_version_min: 11` — Add **Tag Dispatching** section to `ref-advanced-cpp.md`: dispatch on `std::true_type`/`std::false_type` based on `is_integral_v<T>`; tag-based algorithm selection in brownfield code without C++20 concepts; migration path from tag dispatch to `if constexpr` to concepts. Copyright note: original examples only.
- [x] ESE-35 — `cpp_version_min: 20` — Add **Advanced Concepts** section to `ref-advanced-cpp.md`: compound `requires`-expression (checking multiple operations); concept subsumption (how the compiler picks the most constrained overload); auto-concept parameters (`void f(auto x)` vs `void f(std::integral auto x)`); combining concepts with `&&` and `||`; concept debugging (static_assert for concept diagnostics). Copyright note: original examples only; Core Guidelines T.20-T.25 adaptable with attribution.
- [x] ESE-36 — `cpp_version_min: 17` — Add **Nontype Template Parameters (NTTPs)** section to `ref-advanced-cpp.md`: NTTPs for integral, enum, pointer-to-member; C++20: floating-point NTTPs and class-type NTTPs; compile-time string as NTTP (`template <auto N>` with string literal wrapper); compile-time configuration table with NTTP. Copyright note: original examples; concept from Vandevoorde 2017 (reference only).
- [x] ESE-37 — `cpp_version_min: 11` — Create `avatars/technology/cpp/examples/ENG-3.1-policy-based-design.md`: COMPLIANT: `template<typename StoragePolicy, typename LogPolicy> class FlightRepository` with separate compile-time strategies. NON-COMPLIANT: runtime strategy injection via virtual base (unnecessary overhead). Edge cases: policy type constraints with concepts, policy defaults, policy interaction. ≤ 700 tokens. Copyright note: original examples; concept from Vandevoorde 2017 (reference only).

---

## Phase 6: P2 Core Guidelines Rule Gaps

> **Goal:** Cover Core Guidelines F.xx (parameter passing), C.20/C.21/C.22 (Rule of Zero/Five), C.11 (regular types), SL.xx (container/algorithm selection), and SF.xx (source file organization).

- [x] ESE-38 — `cpp_version_min: 11` — Add **Parameter Passing Convention Table** (F.16/F.17/F.18/F.19/F.20) to `ref-core-language.md`: formal table: in (`const T&` or `T`), in-out (`T&`), will-move-from (`T&&` + `std::move`), forward (`T&&` + `std::forward`), out (return by value); when to use `unique_ptr` vs. `shared_ptr` vs. raw reference; the "sink parameter by value" pattern. Cite Core Guidelines F.15-F.20 with URLs. Copyright note: Core Guidelines adaptable with MIT attribution.
- [x] ESE-39 — `cpp_version_min: 11` — Add **Rule of Zero / Rule of Five** section to `ref-core-language.md`: the hierarchy — Rule of Zero (compiler generates all five), Rule of Five (if you declare one, declare all five), Rule of Three (pre-C++11); interaction with `= default` and `= delete`; when custom implementations are needed vs. when `= default` suffices; `[[nodiscard]]` on factory functions. Add COMPLIANT/NON-COMPLIANT examples for FlightPlan value type. Cite Core Guidelines C.20/C.21/C.22. Copyright note: Core Guidelines adaptable with MIT attribution.
- [x] ESE-40 — `cpp_version_min: 11` — Add **Regular Types and Value Semantics** section to `ref-core-language.md`: definition of regular type (default constructible, copyable, movable, equality comparable, swappable); why domain value types (`FlightId`, `PNR`, `SeatCode`) should be regular; relationship to `std::regular` concept (C++20); `friend bool operator==(const T&, const T&) = default`; value semantics vs. identity semantics. Cite Core Guidelines C.11. Copyright note: Core Guidelines adaptable with MIT attribution.
- [x] ESE-41 — `cpp_version_min: 11` — Add **Container and Algorithm Selection Guide** to `ref-core-language.md`: container decision table (vector vs. deque vs. list vs. unordered_map vs. map vs. set); prefer `std::ranges` algorithms over hand-rolled loops (ES.1); `std::string_view` governance (where safe vs. where it dangles); `std::span` vs. `std::string_view` comparison; avoid `std::string` where `std::string_view` suffices. Cite Core Guidelines SL.con.xx and ES.1/ES.2. Copyright note: original examples; Core Guidelines adaptable with attribution.
- [x] ESE-42 — `cpp_version_min: 98` — Add **Source File Organization (SF.xx)** section to `ref-build-toolchain.md`: SF.1 (use a consistent file extension); SF.3/SF.4 (use header files for interfaces, not implementations); SF.6 (use `using` directives only in small scopes); SF.7 (don't `using namespace std` in headers); SF.8 (use include guards or `#pragma once`); SF.12 (prefer `#pragma once`); SF.21 (don't mix definition styles in headers); C++20 modules as long-term migration path. Cite Core Guidelines SF.xx with URLs. Copyright note: Core Guidelines adaptable with MIT attribution.
- [x] ESE-43 — `cpp_version_min: 11` — Add **Profiling Before Optimization** section to `ref-build-toolchain.md` (Per.xx): "Don't optimize prematurely — first understand, then measure, then optimize" (Per.1); `perf`, `valgrind --callgrind`, `vtune`, `tracy` for C++; avoid unnecessary copies (Per.10 — value semantics encourages copies; use `std::move` for sinks); `[[likely]]`/`[[unlikely]]` attributes for branch prediction hints; zero-overhead abstraction check. Cite Core Guidelines Per.1/Per.3/Per.10. Copyright note: Core Guidelines adaptable with MIT attribution.

---

## Phase 7: P3 Medium-Priority Gaps

> **Goal:** Cover remaining medium-priority gaps for completeness: expression templates, NTTPs, chrono/timezone, lambda improvements, C-style programming guidance, GSL Profiles, Amdahl's Law, coroutine source_location.

- [x] ESE-44 — `cpp_version_min: 11` — Add **Expression Templates** section to `ref-advanced-cpp.md`: lazy evaluation via template expression nodes; example: unit-safe arithmetic type that defers computation; when to use vs. when `constexpr` suffices; performance benefit (avoids temporaries); Eigen/Blaze-style motivation. Copyright note: original examples; concept from Vandevoorde 2017 (reference only). ≤ 400 token section.
- [x] ESE-45 — `cpp_version_min: 20` — Add **C++20 Lambda Improvements** section to `ref-advanced-cpp.md`: template lambda syntax (`[]<typename T>(T x) { ... }`); lambda in unevaluated contexts (e.g., `sizeof` lambda); `consteval` lambda; capturing structured bindings; `[[nodiscard]]` lambda. Copyright note: original examples; concept from Josuttis C++20 (reference only).
- [x] ESE-46 — `cpp_version_min: 20` — Add **C++20 Aggregate Improvements** section to `ref-core-language.md`: parenthesis initialization for aggregates (`FlightRequest{...}` and `FlightRequest(...)`); class template argument deduction (CTAD) with aggregates; inheritance from aggregates (C++20 allows); interaction with designated initializers. Copyright note: original examples; concept from Josuttis C++20 (reference only).
- [x] ESE-47 — `cpp_version_min: 20` — Add **Calendar and Timezone** section to `ref-cpp20-features-part2.md`: `std::chrono::year_month_day`; `std::chrono::zoned_time` for FAR 117 crew rest calculations; converting between `sys_time` and `local_time`; timezone database (`std::chrono::get_tzdb()`); duration arithmetic with `std::chrono::hh_mm_ss`. Aviation context: duty period limits require timezone-aware time math. Copyright note: original examples; concept from Josuttis C++20 (reference only).
- [x] ESE-48 — `cpp_version_min: 20` — Create `avatars/technology/cpp/examples/ENG-5.5-source-location.md`: COMPLIANT logging function using `std::source_location::current()` as default parameter for zero-overhead structured location capture. NON-COMPLIANT: manual `__FILE__`/`__LINE__` macro injection. Edge cases: source_location in templates, consteval context, async code. ≤ 700 tokens.
- [x] ESE-49 — `cpp_version_min: 20` — Create `avatars/technology/cpp/examples/ENG-3.1-constinit.md`: COMPLIANT `constinit` global flight-counter to prevent static init-order fiasco. COMPLIANT `constinit std::atomic<int>` for thread-safe global. NON-COMPLIANT: plain `static int` that silently zero-initializes but has no compile-time guarantee. Edge cases: constinit with non-trivial type, constinit thread_local. ≤ 700 tokens.
- [x] ESE-50 — `cpp_version_min: 98` — Add **C-Style Programming (CPL.xx)** section to `ref-safety-memory.md`: CPL.1 (prefer C++ over C); CPL.2 (only use C when necessary); `extern "C"` linkage for FFI; C struct wrapping in RAII C++ class; C array → `std::span` migration; mixing C and C++ TUs safely (name mangling). Cite Core Guidelines CPL.1/CPL.2/CPL.3. Copyright note: Core Guidelines adaptable with MIT attribution.
- [x] ESE-51 — `cpp_version_min: 14` — Add **GSL Profiles (Pro.xx)** section to `ref-safety-memory.md`: type-safety profile (no reinterpret_cast, no unions, no varargs); bounds profile (use span, not raw arrays); lifetime profile (no dangling, no use-after-free); how to apply profiles incrementally with `[[gsl::suppress("tag")]]`; GSL library integration (`vcpkg install ms-gsl`). Cite Core Guidelines Pro.1/Pro.2/Pro.3. Copyright note: Core Guidelines adaptable with MIT attribution.

---

## Phase 8: Governance Wiring

> **Goal:** Ensure all new content is reachable via RAG routing, manifest, and reference-index.

- [x] ESE-52 — Update `avatars/technology/cpp/reference-index.md`: add rows for `ref-cpp20-features-part1.md`, `ref-cpp20-features-part2.md`, `ref-concurrency-advanced-part1.md`, and `ref-concurrency-advanced-part2.md`; update descriptions for enhanced `ref-advanced-cpp.md`, `ref-core-language.md`, `ref-concurrency.md`, `ref-build-toolchain.md`, `ref-safety-memory.md`; add entries for all 17 new example files
- [x] ESE-53 — Update `avatars/technology/cpp/manifest.yaml`: add C++20 feature list (modules, ranges, format, spaceship, span, bit_cast, source_location, constinit, atomic_ref, chrono-calendar) to language version matrix; update `anti_patterns` and `retrieval_triggers` sections; add `concurrency_advanced` and `cpp20_features` to reference file list
- [x] ESE-54 — Update `avatars/AVATAR-RAG-INDEX.yaml`: add routing entries for `ref-cpp20-features-part1.md` + `ref-cpp20-features-part2.md` (triggers: "ranges", "modules", "std::format", "spaceship", "std::span", "bit_cast", "source_location", "constinit", "atomic_ref", "coroutine generator") and `ref-concurrency-advanced-part1.md` + `ref-concurrency-advanced-part2.md` (triggers: "memory ordering", "happens-before", "lock-free", "thread pool", "false sharing", "condition variable", "jthread", "stop_token", "Amdahl"); update token estimates for all modified files
- [x] ESE-55 — Final verification: run `aa-constitution-lint .` from repository root; confirm all new files referenced in `reference-index.md`; confirm all law citations in new files use `[ENG-x.x](laws/...)` format; confirm all example files contain `## Edge Cases & Warnings` section; confirm copyright attribution header in each new file

---

## Quick Reference — Gap ID to Task Mapping

| Gap ID | Task(s) | Priority |
|--------|---------|----------|
| GAP-C1 Memory ordering | ESE-17 | P1 |
| GAP-C2 Parallel algorithms | ESE-18 | P1 |
| GAP-C3 jthread/stop_token | ESE-22, ESE-30 | P2 |
| GAP-C4 Condition variables | ESE-23, ESE-31 | P2 |
| GAP-C5 Lock-free | ESE-24 | P2 |
| GAP-C6 Thread pool | ESE-25 | P2 |
| GAP-C7 False sharing | ESE-26, ESE-32 | P2 |
| GAP-C8 promise/future | ESE-27 | P2 |
| GAP-C9 Amdahl's Law | ESE-28 | P3 |
| GAP-C10 CP.51/52/53 | ESE-29 | P2 |
| GAP-T1 CRTP | ESE-19 | P1 |
| GAP-T2 Type traits | ESE-33 | P2 |
| GAP-T3 Tag dispatching | ESE-34 | P2 |
| GAP-T4 Policy-based design | ESE-37 | P3 |
| GAP-T5 Expression templates | ESE-44 | P3 |
| GAP-T6 NTTPs | ESE-36 | P3 |
| GAP-T7 Advanced Concepts | ESE-35 | P2 |
| GAP-20-1 C++20 Modules | ESE-02, ESE-13 | P1 |
| GAP-20-2 Ranges/Views | ESE-03, ESE-12 | P1 |
| GAP-20-3 std::format | ESE-06, ESE-16 | P1 |
| GAP-20-4 Spaceship operator | ESE-05, ESE-14 | P1 |
| GAP-20-5 std::span | ESE-04, ESE-15 | P1 |
| GAP-20-6 std::bit_cast | ESE-07 | P2 |
| GAP-20-7 std::source_location | ESE-08, ESE-48 | P2 |
| GAP-20-8 constinit | ESE-09, ESE-49 | P2 |
| GAP-20-9 Coroutine generators | ESE-11 | P2 |
| GAP-20-10 std::atomic_ref | ESE-10 | P2 |
| GAP-20-11 Calendar/timezone | ESE-47 | P3 |
| GAP-20-12 Lambda improvements | ESE-45 | P3 |
| GAP-20-13 Aggregate improvements | ESE-46 | P3 |
| GAP-CG1 Interface design I.xx | ESE-20 | P1 |
| GAP-CG2 Parameter passing F.xx | ESE-38 | P2 |
| GAP-CG3 Rule of Zero/Five | ESE-39 | P2 |
| GAP-CG4 Regular types C.11 | ESE-40 | P2 |
| GAP-CG5 Performance Per.xx | ESE-43 | P2 |
| GAP-CG6 Container/SL guide | ESE-41 | P2 |
| GAP-CG7 CPL.xx C-style | ESE-50 | P3 |
| GAP-CG8 Source files SF.xx | ESE-42 | P2 |
| GAP-CG9 GSL Profiles Pro.xx | ESE-51 | P3 |
| GAP-CG10 CP.42/43/50 | ESE-23 (incorporated) | P2 |
| GAP-CG11 string_view lifetime traps | ESE-64 (`const char*`, cpp03), ESE-41 section (`string_view`, cpp17) | P1 |
| GAP-CG12 deducing this (C++23) | New section in ref-advanced-cpp.md | P2 |
| GAP-AA1 Characterization testing | `cpp_version_min` fix on existing file (11→98) + ESE-65 (MSVC 6.0 stdlib fallback only) | P1 |
| GAP-AA2 JNI thread safety | ESE-62 (C++98 pthread_key_t) + C++11 thread_local RAII section | P1 |
| GAP-AA3 MFC integration | ref-brownfield-survival.md section | P1 |
| GAP-AA4 FICO Xpress | ref-brownfield-survival.md section | P1 |
| GAP-AA5 CMake migration | ref-build-toolchain.md section | P2 |
| GAP-AA6 RCPtr migration | ref-brownfield-survival.md section | P2 |
| GAP-AA7 Resource Handle Pattern | ref-brownfield-survival.md section | P2 |
| GAP-AA8 Legacy serialization | ref-brownfield-survival.md section | P3 |
| GAP-20-2 bridge (range-v3) | ESE-58 (`cpp_version_min: 14`, transitional) | P1 |
| GAP-20-3 bridge (fmtlib) | ESE-57 (`cpp_version_min: 11`, transitional) | P1 |
| GAP-20-5 bridge (gsl::span) | ESE-59 (`cpp_version_min: 14`, transitional) | P1 |
| GAP-20-11 bridge (HH date) | ESE-56 (`cpp_version_min: 11`, transitional) | P1 |
| GAP-C3 bridge (manual stop-flag) | ESE-61 (`cpp_version_min: 11`, transitional) | P2 |
| GAP-C5 C++11/14 lock-free | ESE-60 (`cpp_version_min: 11`, transitional) | P2 |

---

## Phase 9: Version-Sensitivity Bridge Deliverables _(new — version-routing round 3)_

> **Goal:** Added by the version-sensitivity review to ensure 95% of AA's current C++ LOC receives actionable guidance. **ESE-56 and ESE-62 execute BEFORE Phase 1** (active liability gaps per R7). All other bridge tasks execute alongside their parent phase.

- [x] ESE-56 ✓ (CBF-01) — `cpp_version_min: 11` — Create `avatars/technology/cpp/examples/ENG-6.1-timezone-cpp14.md` (routes to `transitional.prefer`): FAR 117 timezone-aware arithmetic for CWR/IOC_ALP TODAY using `HowardHinnant/date` (MIT). COMPLIANT: `date::make_zoned("America/Chicago", tp)` for crew rest period start/end arithmetic. NON-COMPLIANT: `time_t`/`localtime` with manual DST offset. Migration note: HowardHinnant/date API is nearly identical to C++20 `std::chrono` — migration is mechanical. Attribution: HowardHinnant/date, MIT. ≤ 700 tokens. **Execute BEFORE Phase 7 (ESE-47). Closes R7 FAR 117 theory.**

- [x] ESE-57 ✓ (CBF-04) — `cpp_version_min: 11` — Create `avatars/technology/cpp/examples/ENG-6.1-fmtlib-format.md` (routes to `transitional.prefer`): fmtlib bridge for CWR/IOC_ALP TODAY. COMPLIANT: `fmt::format("{} flight {} departs {}", carrier, flight_num, dept_time)` replacing `sprintf`. Custom `fmt::formatter<FlightId>` specialization. NON-COMPLIANT: `sprintf` with format string. Migration note: fmtlib IS the reference implementation that became `std::format`; API identical — migration is mechanical. Attribution: fmtlib/fmt, MIT. ≤ 700 tokens. **Execute before ESE-16.**

- [x] ESE-58 ✓ (CBF-05) — `cpp_version_min: 14` — Create `avatars/technology/cpp/examples/ENG-3.1-ranges-range-v3.md` (routes to `transitional.prefer`): range-v3 bridge for CWR/IOC_ALP TODAY. COMPLIANT: `ranges::view::filter | ranges::view::transform | ranges::view::take` over `std::vector<FlightLeg>`. NON-COMPLIANT: manual iterator loop. **Warning:** range-v3 uses `ranges::` namespace; std::ranges uses `std::ranges::`; `filter_view` const-iterability semantics differ — cannot mix headers. Attribution: ericniebler/range-v3, Boost Software License. ≤ 700 tokens. **Execute before ESE-12.**

- [x] ESE-59 ✓ (CBF-06) — `cpp_version_min: 14` — Create `avatars/technology/cpp/examples/ENG-6.1-gsl-span-cpp14.md` (routes to `transitional.prefer`): `gsl::span` bridge for CWR/IOC_ALP TODAY. COMPLIANT: `gsl::span<const SeatData>` replacing `const SeatData* data, size_t len`. NON-COMPLIANT: raw pointer + size pair. Migration note: `gsl::span` API is identical to C++20 `std::span`. Attribution: microsoft/GSL, MIT. ≤ 700 tokens. **Execute before ESE-15.**

- [x] ESE-60 ✓ (CBF-08) — `cpp_version_min: 11` — Create `avatars/technology/cpp/examples/ENG-6.1-lock-free-cpp14.md` (routes to `transitional.prefer`): C++11/14 lock-free patterns. ABA problem with version counter; `boostorg/lockfree::spsc_queue` for SPSC use case; when lock-free is NOT faster. NON-COMPLIANT: `std::hazard_pointer` (C++23 — unavailable). Warning: lock-free is rarely appropriate for application-layer code; always profile first. Attribution: boostorg/lockfree, Boost Software License; algorithm: Treiber 1986. ≤ 700 tokens. **Execute before ESE-24.**

- [x] ESE-61 ✓ (CBF-07) — `cpp_version_min: 11` — Create `avatars/technology/cpp/examples/ENG-6.1-thread-stop-flag.md` (routes to `transitional.prefer`): Manual stop-flag pattern for C++11/14 teams. COMPLIANT: `std::atomic<bool>` with `memory_order_release` store / `memory_order_acquire` load. NON-COMPLIANT: `volatile bool` (data race). Migration note: when C++20 is available, replace with `std::jthread` + `std::stop_token`. ≤ 700 tokens.

- [x] ESE-62 ✓ (CBF-02) — `cpp_version_min: 98` — Create `avatars/technology/cpp/examples/ENG-6.1-jni-thread-cpp98.md` (routes to `legacy.prefer`, `brownfield.prefer`): C++98-safe JNI thread attachment using `pthread_key_t` (POSIX) / `TlsAlloc` (Win32). COMPLIANT: destructor callback on `pthread_key_create` calls `DetachCurrentThread` at thread exit. NON-COMPLIANT: `static JNIEnv* g_env` (thread-local by JVM contract — UB across threads). NON-COMPLIANT: `std::atomic<JNIEnv*>` (wrong for thread-model reasons). Attribution: android/ndk-samples, Apache 2.0. ≤ 700 tokens. **Execute IMMEDIATELY — closes R7 JNI wrongful-death theory.**

- [x] ESE-63 ✓ (CBF-09) — `cpp_version_min: 98` — Add **Rule of Three subsection** to `ref-brownfield-survival.md` (CBF-09 pre-created; `ref-core-language.md` does not exist — content placed in `legacy.prefer` file `ref-brownfield-survival.md` which satisfies same routing requirement) (routes to `legacy.prefer`, `brownfield.prefer`): Rule of Three for C++98/03 — declare destructor, copy constructor, copy assignment together; private-undefined pattern for non-copyable types (C++98); `= delete` is C++11 only. Migration note: when C++11 is available, upgrade to Rule of Five. Context: serving Rule of Five to C++98 developers produces uncompilable code — this subsection gates them correctly.

- [x] ESE-64 ✓ (CBF-10) — `cpp_version_min: 03` — Create `avatars/technology/cpp/examples/ENG-6.1-const-char-lifetime.md` (routes to `brownfield.prefer`): `const char*` lifetime traps for pre-C++17 developers. COMPLIANT: documenting expected lifetime contract on `const char*` parameters. NON-COMPLIANT: returning `const char*` to a local `std::string`'s `.c_str()` (dangling). NON-COMPLIANT: storing `const char*` from a temporary. Migration note: these patterns parallel `std::string_view` lifetime traps exactly — see ENG-6.1-string-view-lifetime.md when C++17 is available. ≤ 700 tokens.

- [x] ESE-65 ✓ (CBF-11) — `cpp_version_min: 98` — **Scope narrowed (GTest 1.8.x correction):** GoogleTest 1.8.x (final C++98 release, EOL 2018) supports C++98/03 on GCC and MSVC 8.0+ — the existing `ENG-4.1-characterization-test-pattern.md` now routes to `legacy.prefer`/`brownfield.prefer` via its corrected `cpp_version_min: 98`. This task is scoped to **MSVC 6.0 (SPEClient) and pre-MSVC-8 toolchains only** where no GTest release compiles. Add MSVC-6.0-safe golden-master section to `ref-brownfield-survival.md`: stdlib-only pattern using `<fstream>`, `<cstdlib>`, `assert()` — record known-good output; compare on re-run; diff signals regression. Explicitly document GTest 1.8.x (vcpkg pin `gtest==1.8.1`) as the preferred option for all other C++98/03 projects; this pattern is the MSVC 6.0 fallback only.

---

## Phase 10: Post-Implementation Review Panel — Amendment A _(added 2026-04-27)_

> **Goal:** Resolve all correctness and quality findings raised by the two final deep-analysis 7-reviewer panel rounds run after completion of all 73 ESE implementation tasks. All findings are documented in PROPOSAL.md §Amendment A.
> **Commits:** `72caf8e` (Round 1), `a502288` (Round 2)

### Round 1 Panel Fixes (commits `be6e551`–`72caf8e`)

- [x] ESE-P1 ✓ — Split `ref-cpp20-features-part1.md` (6225t, over budget) into Part 1 (3013t: Modules/Ranges/span/Spaceship) + new Part 3 (3346t: format/bit_cast/source_location/constinit/atomic_ref). Both within 3500t budget. Updated routing, reference-index, ESE-06–10 tests.
- [x] ESE-P2 ✓ — Fix `format_to_n` null-termination: `buf[result.size]` → `*result.out`. `result.out` is the past-last-written iterator; `result.size` is the would-have-been-written count.
- [x] ESE-P3 ✓ — Fix `std::bit_cast` constraint: removed false "To must be default-constructible" claim. Correct requirements: same size + both trivially copyable.
- [x] ESE-P4 ✓ — Replace ADS-B bit-field `bit_cast` target with endian-safe masking; added portability warning (bit-field layout is implementation-defined).
- [x] ESE-P5 ✓ — Rule of Five: "ctor" → "dtor" — the destructor (not copy ctor) triggers the double-free in Rule of Five scenarios.
- [x] ESE-P6 ✓ — `std::unique_ptr` is `std::movable`, not `std::semiregular`. `semiregular` requires default-constructible + copyable.
- [x] ESE-P7 ✓ — F.17/F.18 labels corrected: F.17 = in/out via `T&`, F.18 = will-move-from via `T&&`. Labels were previously swapped.
- [x] ESE-P8 ✓ — `ENG-6.1-condition-variable.md`: added required `## Edge Cases & Warnings` table (4 rows: spurious wakeup, predicate race, notify_all vs one, exception safety).
- [x] ESE-P9 ✓ — `if [[likely]]` invalid syntax fixed: `if [[likely]] (cond)` → `if (cond) [[likely]] { }`.
- [x] ESE-P10 ✓ — FAR 117 timezone: replaced `dep_tp + 8h` (UTC arithmetic) with `local_days{date} + 8h` → `zoned_time{tz_acc, local}` (correct acclimation-timezone local time). Updated prose to consistently say "acclimation timezone."
- [x] ESE-P11 ✓ — `std::promise` destruction: "blocks forever" → "throws `std::future_error(broken_promise)`". Destroying an unfulfilled promise marks the shared state as broken.
- [x] ESE-P12 ✓ — `std::thread` destructor: "forgetting join is UB" → "calls `std::terminate()` (defined behavior, not UB)".
- [x] ESE-P13 ✓ — `ENG-5.5-source-location.md`: added missing `#include <iostream>` to compliant example.
- [x] ESE-P14 ✓ — Removed stale "Status: In progress — ESE-02 complete" banners from Part 1 and Part 2.
- [x] ESE-P15 ✓ — AVATAR-RAG-INDEX.yaml: updated format/bit_cast/source_location/constinit/atomic_ref routing queries to point to Part 3 (not Part 1); added Part 3 to C++11 avoid lists; added inventory row and version-tier routing entries.

### Round 2 Panel Fixes (commit `a502288`)

- [x] ESE-A1 ✓ — Added missing `template<typename T>` to Serializable concept in subsumption example — required for valid C++20 concept definition.
- [x] ESE-A2 ✓ — `format_to_n`: added `if (buf.empty()) return;` guard — `buf.size() - 1` on empty span underflows (unsigned wrap → SIZE_MAX).
- [x] ESE-A3 ✓ — `std::atomic_ref` constraints: added lifetime rule — the underlying object must outlive every `atomic_ref` that wraps it.
- [x] ESE-A4 ✓ — `constinit` example: (a) removed plain `++` on `constinit int` (data race); promoted `std::atomic<int>` as canonical form. (b) Replaced `int g = 0` SIOF illustration with real cross-TU dynamic-init fiasco (`static int x = get_base_count()`). (c) Corrected edge-case wording: "literal or trivial types" → "type has a `constexpr` constructor."
- [x] ESE-A5 ✓ — `Generator<T>` made move-only: added deleted copy ctor/assign and move ctor/assign using `std::exchange`. Default copy ctor would double-destroy the coroutine handle.
- [x] ESE-A6 ✓ — `ref-safety-memory-lifetime.md`: `std::expected` is C++23, not C++11. Added version annotation and `tl::expected` note for C++17/20 teams.
- [x] ESE-A7 ✓ — AVATAR-RAG-INDEX.yaml: removed duplicate "C++ FAR 117 regulatory traceability test?" query (appeared at lines 1176 and 1216).
- [x] ESE-A8 ✓ — Part 2 `cpp_version_note` corrected: now says "See Part 3 for std::format, bit_cast, source_location, constinit, atomic_ref" instead of Part 1. Part 3 See-Also bullet fixed.
- [x] ESE-A9 ✓ — `ENG-5.5-source-location.md`: law link changed from `eng-5-observability.md` (non-existent) to `eng-5-devops.md` (consistent with all other ENG-5.5 examples).
- [x] ESE-A10 ✓ — Ranges sentinel table: `std::string_view` (bounded range) replaced with `const char*` + `std::default_sentinel_t` via `take_while` — accurate null-terminated C-string sentinel example.

### Post-Phase-10 State

- Test suite: **1388 passing** (1 test removed: legitimate removal of duplicate YAML token annotation entry)
- Amendment A appended to `PROPOSAL.md` — commit `0f07d6a`

---

## Phase 11: Amendment D — Round 5 Close-Out Panel Action Items _(added 2026-04-27)_

> **Goal:** Resolve the 5 IMPORTANT findings from the Round 5 missing-reviewer panel (R1–R8).
> These are **post-merge** improvements — none blocks PR #51 from merging to main.
> Full findings documented in PROPOSAL.md §Amendment D and ROUND5-PANEL-REVIEW.md.

- [x] ESE-D1 ✓ b7008bd — `ref-safety-far117-cwr.md`: Option (b) implemented — `cpp_version_note` qualified to scope C++98 coverage as version-agnostic governance; code examples noted as C++11+; C++98 teams directed to platform team. **Panel verdict: ⚠️ PARTIAL** — "platform team" redirect undefined; C++98 timezone content gap unfilled. → See ESE-E1, ESE-E2 below.

- [x] ESE-D2 ✓ b7008bd — `AVATAR-RAG-INDEX.yaml`: CRTP wired as routing hint (CI test forbids `examples/` in prefer lists; `cpp_version_min: 11` blocks brownfield tier). Stale routing note removed from `ref-templates-metaprogramming.md`. **Panel verdict: ⚠️ PARTIAL** — routing hint requires CRTP-keyword query; `ref-legacy-navigation.md` provides one-line fallback in brownfield prefer list. R8-6 not fully met. → See ESE-E3, ESE-E4 below.

- [x] ESE-D3 ✓ b7008bd — `## Further Reading` sections added to `ref-cpp20-features-part1.md`, `ref-concurrency-advanced-part1.md`, `ref-templates-advanced.md`, `ref-core-modern-idioms.md` per SOURCES.md Tier 3 citation format. **Panel verdict: ✅ RESOLVED** — R3 E3 from Round 4 fully closed.

- [x] ESE-D4 ✓ b7008bd — ESE-00.5 Copilot Enterprise governance note appended to `PROGRESS.md` with three action items and fallback posture. **Panel verdict: ✅ RESOLVED** — defensible due-diligence record.

- [x] ESE-D5 ✓ b7008bd — `rag_exclude: true` removed from `ENG-6.1-jni-thread-cpp98.md` and `ENG-6.1-timezone-cpp14.md`; routing pre-wired in AVATAR-RAG-INDEX.yaml. **Panel verdict: ✅ RESOLVED** — both files technically correct; R6 confirms actionable for CWR developers.

---

## Phase 12: Amendment E — Amendment D Panel Action Items _(added 2026-04-28)_

> **Goal:** Close the 4 IMPORTANT and 4 MINOR findings from the Amendment D confirmation panel
> (AMENDMENT-D-PANEL-REVIEW.md, commit `b7008bd`). None blocks merge of PR #51.
> **Panel verdict:** CLEAR TO MERGE — Amendment E is post-merge work.

- [ ] ESE-E1 — `avatars/technology/cpp/refs/safety/ref-safety-far117-cwr.md`: Add actionable resource identifier for the "platform team" redirect — either an internal wiki link, ServiceNow catalog item, or team contact. **Reviewers: R2, R6, R7 — unactionable redirect is documented gap.** Priority: P1.

- [ ] ESE-E2 — Add C++98 POSIX timezone arithmetic content: Either add `## C++98 Alternative: POSIX Time Functions` subsection to `ref-safety-far117-cwr.md` with `gmtime_r`/`mktime`/`difftime` patterns and DST hazard notes, OR create `examples/ENG-6.1-timezone-cpp98.md` with `cpp_version_min: 98`. **Reviewers: R6, R8 — C++98 CWR developers have zero usable timezone code.** Priority: P1.

- [ ] ESE-E3 — `avatars/AVATAR-RAG-INDEX.yaml`: Add broad CRTP routing aliases so "avoid virtual dispatch overhead" and "polymorphism without vtable" queries route to CRTP guidance. **Reviewer: R4 — current hint requires CRTP keyword.** Priority: P1.

- [ ] ESE-E4 — Close R8-6 fully: Either (a) create `examples/ENG-3.1-crtp-cpp98.md` with `cpp_version_min: 98` and pure C++98 template syntax (no `auto`, no lambda, no `std::string_view`), add to brownfield tier prefer list; OR (b) create `refs/legacy/ref-static-polymorphism.md` with CRTP guidance, add to brownfield prefer list. **Reviewer: R8 — brownfield tier still has no proactive CRTP example delivery.** Priority: P2.

- [ ] ESE-E5 — Establish review cadence for activated safety-critical example files: Document in PROGRESS.md that `ENG-6.1-jni-thread-cpp98.md` and `ENG-6.1-timezone-cpp14.md` require accuracy review when C++ standards or AA operational context changes. **Reviewer: R7 — "published guidance" liability standard now applies.** Priority: P2.

- [ ] ESE-E6 — `avatars/technology/cpp/refs/language/ref-templates-advanced.md`: Add Vandevoorde & Josuttis, *C++ Templates: The Complete Guide* 2nd Ed. (2017, Addison-Wesley) to `## Further Reading` section. **Reviewer: R3 — definitive templates reference missing.** Priority: P3.

- [ ] ESE-E7 — Standardize Coplien (1992) citation in `ref-templates-advanced.md` to include full title: *Advanced C++ Programming Styles and Idioms* (Addison-Wesley, 1992). **Reviewer: R1 — citation consistency with SOURCES.md format.** Priority: P3.

- [ ] ESE-E8 — `examples/ENG-6.1-timezone-cpp14.md`: Consider renaming to `ENG-6.1-timezone-cpp11.md` or updating routing hint to include "C++11 C++14" — `cpp_version_min: 11` but title/routing implies C++14 only. **Reviewer: R8 — minor tier coverage confusion.** Priority: P3.
