---
cpp_version_min: 98
cpp_version_note: >-
  Migration guide for C++98/03 to C++11/14; documents C++98 patterns explicitly.
avatar: cpp
---

# C++ Avatar Reference: Migration Playbooks (Pre-C++17 Foundation)

---

## Migration Playbook: C++98/03 → C++11

Per [ENG-1.4](laws/engineering/eng-1-core-principles.md) (Incremental Improvement Law), migrations must proceed in vertical slices with test verification at each step.

The largest and most impactful upgrade in C++ history. This migration enables smart pointers, move semantics, and the C++ memory model — foundational safety improvements.

### Feature Adoption Sequence (Safety-First Priority)

| Priority | Feature | Rationale | Risk Level |
|---|---|---|---|
| 1 | `nullptr` | Eliminates NULL/0 ambiguity bugs; drop-in replacement | Low |
| 2 | `override` / `final` | Catches silent virtual function signature mismatches at compile time | Low |
| 3 | `enum class` | Prevents implicit integer conversion bugs in status codes | Low |
| 4 | `auto` (for iterators) | Reduces verbosity in `std::map<>::iterator` patterns | Low |
| 5 | Range-based `for` | Eliminates off-by-one in iterator loops | Low |
| 6 | `std::unique_ptr` / `std::shared_ptr` | Eliminates memory leaks — biggest safety win | Medium |
| 7 | Move semantics | Performance + correctness for value types | Medium |
| 8 | Lambdas | Replaces `std::bind1st`/`bind2nd` and function objects | Medium |
| 9 | `constexpr` | Replaces `#define` constants with type-safe compile-time values | Low |
| 10 | `std::thread` / `std::mutex` | Replaces POSIX/Win32 threads with portable API | High |

### Critical Pitfalls

- **`auto_ptr` → `unique_ptr`**: NOT a drop-in replacement. `auto_ptr` copies transfer ownership; `unique_ptr` requires explicit `std::move()`. Automated sed-replace is dangerous.
- **GCC 5.1 ABI break**: `std::string` and `std::list` changed ABI. Mixing GCC 4.x and GCC 5.x objects in the same binary causes silent data corruption. Set `_GLIBCXX_USE_CXX11_ABI` explicitly.
- **`throw()` → `noexcept`**: Semantically different. `throw()` calls `std::unexpected()`; `noexcept` calls `std::terminate()`.
- **Narrowing in brace init**: `int x = {3.14}` was legal in C++98, is ill-formed in C++11.
- **Thread safety**: C++11 introduces the memory model — pre-existing "working" code using `volatile` for synchronization is now officially undefined behavior.

### CI Changes
1. Add `-std=c++11` to build flags (start with one module)
2. Enable `-Wsuggest-override` (GCC) or `-Wmissing-override` (Clang)
3. Add a CI job that builds with C++11 flag alongside existing C++98 build
4. Run tests under both standards until migration is complete
5. Add `modernize-use-nullptr` and `modernize-use-override` clang-tidy checks

## Migration Playbook: C++11 → C++14

Per [ENG-1.4](laws/engineering/eng-1-core-principles.md) (Incremental Improvement Law), migrations must proceed in vertical slices.

A minor, low-risk upgrade focused on convenience and expressiveness.

### Feature Adoption Sequence

| Priority | Feature | Rationale |
|---|---|---|
| 1 | Generic lambdas (`auto` params) | Simplifies callback code, enables polymorphic lambdas |
| 2 | `[[deprecated]]` attribute | Governance tool: mark APIs for sunset |
| 3 | `std::make_unique` | Eliminates last reason for raw `new` in non-placement contexts |
| 4 | Relaxed `constexpr` | Enables loops and conditionals in constexpr functions |
| 5 | Return type deduction | Simplifies factory functions |
| 6 | Variable templates | Cleaner type traits (`is_integral_v<T>` vs `is_integral<T>::value`) |

### Pitfalls
- C++14 is a minor revision. The biggest risk is accidentally using C++17 features (structured bindings, `if constexpr`) that look syntactically similar.
- `std::make_unique` was missing from C++11 — many codebases have a custom `make_unique`. Remove custom implementations after upgrade.

### CI Changes
- Change `-std=c++11` to `-std=c++14`. No ABI implications.
- Enable `clang-tidy` check `modernize-make-unique`.

## Migration Playbook: C++14 → C++17

Per [ENG-1.4](laws/engineering/eng-1-core-principles.md) (Incremental Improvement Law), migrations must proceed in vertical slices.

A significant upgrade with major library additions. This is where Boost dependencies start becoming unnecessary.

### Feature Adoption Sequence

| Priority | Feature | Rationale |
|---|---|---|
| 1 | `std::optional` | Replaces nullable pointers and sentinel values for "maybe" semantics |
| 2 | `std::string_view` | Performance for read-only string parameters — but DANGEROUS if stored |
| 3 | Structured bindings | Cleaner tuple/pair/struct decomposition |
| 4 | `if constexpr` | Eliminates SFINAE for simple compile-time branching |
| 5 | `[[nodiscard]]` | Prevents ignoring error returns — critical for safety |
| 6 | `std::variant` + `std::visit` | Type-safe union replacement; eliminates dynamic_cast chains |
| 7 | `std::filesystem` | Replaces Boost.Filesystem and POSIX/Win32 file APIs |
| 8 | Fold expressions | Simplifies variadic template patterns |

### Critical Pitfalls
- **`std::string_view` dangling**: The #1 source of bugs in C++17 adoption. Views do not own data — storing a `string_view` from a temporary causes use-after-free.
- **`std::optional<T&>`** does NOT exist. Code using `boost::optional<T&>` cannot migrate directly — redesign with pointers or `std::reference_wrapper`.
- **Removed features**: `std::auto_ptr`, `std::random_shuffle`, `std::bind1st`/`std::bind2nd` — if these still exist, they are compile errors in C++17 mode. Remove them BEFORE upgrading the standard flag.
- **`std::result_of`** deprecated — replace with `std::invoke_result`.
- **Filesystem exceptions**: `std::filesystem::copy` throws by default; production code should use the `error_code` overloads.

### CI Changes
- Change `-std=c++14` to `-std=c++17`
- Enable clang-tidy: `modernize-use-nodiscard`, `modernize-replace-random-shuffle`
- Verify all removed features (`auto_ptr`, `random_shuffle`) are already eliminated
- Replace Boost usage: `boost::optional` → `std::optional`, `boost::variant` → `std::variant`, `boost::filesystem` → `std::filesystem`

## Migration Playbook: C++17 → C++20

Per [ENG-1.4](laws/engineering/eng-1-core-principles.md) (Incremental Improvement Law), migrations must proceed in vertical slices with test verification at each step.

The second-largest upgrade after C++11. Introduces transformative features (concepts, ranges, coroutines) but requires careful sequencing.

### Feature Adoption Sequence

| Priority | Feature | Rationale |
|---|---|---|
| 1 | `std::span` | Bounds-safe replacement for pointer+size — biggest safety win |
| 2 | Three-way comparison (`<=>`) | Eliminates boilerplate comparison operators; catches bugs |
| 3 | Concepts | Better error messages, self-documenting templates; replaces SFINAE |
| 4 | `[[likely]]` / `[[unlikely]]` | Performance hints for hot paths |
| 5 | Ranges | Composable, lazy, bounds-safe iteration — replaces raw algorithm+iterator |
| 6 | `consteval` / `constinit` | Compile-time guarantees for safety-critical constants; fixes SIOF |
| 7 | Coroutines | Async I/O — adopt only after stable executor library is chosen |
| 8 | Modules | Build speed — adopt LAST; toolchain support still maturing |

### Critical Pitfalls
- **Coroutines without a library**: C++20 provides coroutine primitives (`co_await`, `co_yield`, `co_return`) but NO standard task/generator types until C++23 `std::generator`. Choose a coroutine library (cppcoro, Asio, folly::coro) BEFORE adopting coroutines.
- **Modules**: CMake support requires 3.28+. Build system integration is still fragile across compilers. Module adoption should be LAST.
- **Ranges dangling**: Lazy evaluation can cause use-after-free if the underlying container is modified or destroyed. `views::transform` captures by reference by default.
- **Module ABI**: GCC and Clang have incompatible module ABI. Do not mix module object files from different compilers.
- **Compile time increase**: Concepts and ranges significantly increase compile times. Budget for CI pipeline time increases of 20-50%.

### CI Changes
- Change `-std=c++17` to `-std=c++20`
- Update clang-tidy to enable `modernize-use-concepts`, `modernize-use-std-span`
- Add custom coroutine-parameter-by-value check (no upstream clang-tidy check exists yet — enforce via code review or local clang-tidy plugin)
- Increase CI timeout — concepts and ranges increase compile times
- If adopting modules: upgrade CMake to 3.28+, restructure CI for module dependency scanning

## Dual-Toolchain Governance

Per [ENG-5.2](laws/engineering/eng-5-devops.md) (CI/CD Pipeline Law), all builds must go through automated pipelines. During multi-year migrations, repositories often run two compilers simultaneously. This is a steady state, not a temporary condition.

### CMake Per-Target Standards
Use `target_compile_features()` per target, NOT global `CMAKE_CXX_STANDARD`:
```cmake
target_compile_features(legacy_acars_parser PUBLIC cxx_std_11)
target_compile_features(gate_assignment_v2 PUBLIC cxx_std_17)
target_compile_features(crew_optimizer PUBLIC cxx_std_20)
```

### CI Matrix
Run the CI pipeline under BOTH compilers:
- Legacy compiler validates backward compatibility of legacy modules
- Modern compiler enables sanitizers, clang-tidy, and static analysis

### Release Build Authority
- Legacy compiler is authoritative for release builds of legacy modules until migration completes
- Modern compiler is authoritative for new modules from day one
- Document the authoritative compiler per target in CMakeLists.txt comments

### Sanitizer Allocation
- ASan/UBSan/TSan run under the modern compiler only
- Legacy modules use Valgrind if the modern compiler cannot build them
- Both paths must be green in CI before merge

## Dependency Standard Mismatch

Per [ENG-6.6](laws/engineering/eng-6-security.md) (Vulnerability Management), all dependencies must be managed — including dependencies that require a different C++ standard than the consuming module.

When a vcpkg/Conan dependency requires a higher C++ standard than the consuming module:

1. **Check dependency minimum standard** — review the package's CMakeLists.txt or documentation
2. **Isolate behind a wrapper** — create a thin adapter library compiled at the dependency's required standard. The adapter's public API uses only types compatible with the consuming module's standard.
3. **Never force-compile a C++17 library with `-std=c++11`** — this causes undefined behavior even if it appears to compile
4. **vcpkg triplet configuration** — use custom triplets for per-dependency standard:
```cmake
# triplets/x64-linux-cpp17.cmake
set(VCPKG_CXX_FLAGS "-std=c++17")
```

### Pre-vcpkg Dependency Management
For brownfield projects not yet using vcpkg:
- **Git submodules**: Acceptable for small dependency sets; version-lock in `.gitmodules`
- **Manual vendoring**: Copy source into `third_party/`; document version and license
- **System packages**: Use `find_package()` with version constraints
- **Migration to vcpkg**: Create `vcpkg.json` manifest alongside existing system; migrate one dependency at a time

## Writing New Code for Legacy Standards

Per [ENG-1.3](laws/engineering/eng-1-core-principles.md) (Boy Scout Rule), leave the code cleaner than you found it. When writing NEW code that must compile under an older standard, use these patterns to maximize forward-compatibility:

### What's Available at Each Tier

| Pattern | C++11 | C++14 | C++17 | C++20+ |
|---|---|---|---|---|
| Smart pointers | ✅ `unique_ptr`, `shared_ptr` | ✅ + `make_unique` | ✅ | ✅ |
| Move semantics | ✅ | ✅ | ✅ | ✅ |
| Lambdas | ✅ basic | ✅ generic | ✅ constexpr | ✅ template |
| `auto` | ✅ variables | ✅ return types | ✅ | ✅ |
| Error handling | exceptions | exceptions | `std::optional` | `std::expected` |
| Compile-time logic | `std::enable_if` | `std::enable_if` | `if constexpr` | Concepts |
| String views | ❌ (use `const std::string&`) | ❌ | ✅ `string_view` | ✅ |
| Bounds-safe views | ❌ (use `gsl::span`) | ❌ | ❌ (use `gsl::span`) | ✅ `std::span` |

### Polyfill Strategy
Use polyfill libraries for critical features when the standard doesn't provide them:
- `gsl::span` → backport of `std::span` for pre-C++20 (Microsoft GSL)
- `tl::optional` / `tl::expected` → backport for pre-C++17/C++23
- `fmt::format` → backport of `std::format` for pre-C++20
- `date::` library → backport of `<chrono>` calendar extensions

### Forward-Compatible Coding
Write code that can be easily upgraded:
```cpp
// Use type aliases that can be swapped later
#if __cplusplus >= 202002L
    using BufferView = std::span<const std::byte>;
#else
    using BufferView = gsl::span<const std::byte>;
#endif

// Use compatibility macros
#if __cplusplus >= 201703L
    #define AA_NODISCARD [[nodiscard]]
    #define AA_FALLTHROUGH [[fallthrough]]
#else
    #define AA_NODISCARD
    #define AA_FALLTHROUGH
#endif
```

---


---

## See Also

- [Migration Patterns (C++17+ and Survival)](ref-migration-cpp17-plus.md)
