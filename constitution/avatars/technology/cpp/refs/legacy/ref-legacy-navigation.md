---
cpp_version_min: 98
cpp_version_note: >-
  Legacy C++ codebase navigation; all patterns apply from C++98/03 onwards.
avatar: cpp
---

# C++ Avatar Reference: Legacy Code Navigation


---
## Legacy Code Navigation for New Engineers

Per [ENG-1.2](laws/engineering/eng-1-core-principles.md) (AI-Engineer Pairing Law), AI assistants act as teaching partners. This section provides structured guidance for novice C++ developers assigned to existing American Airlines codebases. The goal is to accelerate time-to-proficiency while preventing accidental regressions.

### Code Archaeology Techniques

When joining an unfamiliar C++ codebase:

1. **Start with the build system** — read `CMakeLists.txt` top-down. It reveals module structure, dependencies, compiler flags, and which targets exist. This is the map of the codebase.
2. **Read headers before implementation** — public headers (`include/`) define the API contract. Understand the interface before diving into implementation details in `src/`.
3. **Trace from the entry point** — find `main()` or the service initialization function. Follow the call chain to understand how components connect.
4. **Generate documentation** — run `doxygen` (even without existing config) to produce call graphs and class hierarchies. Even undocumented code produces useful structural diagrams.
5. **Search for domain entities** — use `grep -rn "class "` to find domain classes. Map them to the business domain (flights, bookings, crew, gates).

### Understanding Legacy Patterns

Legacy C++ code often uses patterns that predate modern standards. Recognize these and understand their intent before changing them:

| Legacy Pattern | Modern Equivalent | Migration Notes |
|---------------|-------------------|-----------------|
| `auto_ptr` | `std::unique_ptr` | Drop-in replacement in most cases |
| `NULL` | `nullptr` | Type-safe; catches implicit conversion bugs |
| `typedef` | `using` alias | Identical semantics, clearer syntax |
| Raw `new`/`delete` | `std::make_unique` / `std::make_shared` | Wrap in RAII; never delete manually |
| `boost::optional` | `std::optional` (C++17+) | Direct migration for most uses |
| `boost::shared_ptr` | `std::shared_ptr` | Direct replacement |
| `#define` constants | `constexpr` variables | Type-safe, scoped, debuggable |
| Callback function pointers | `std::function` or templates | Safer, more flexible |
| Manual mutex lock/unlock | `std::scoped_lock` | Exception-safe, automatic release |
| `dynamic_cast` chains | `std::variant` + `std::visit` | Compile-time exhaustive matching |

**Coplien-era and pre-STL idioms** (C++98 and earlier — common in SPEClient, herc-odyssey-linux, older CWR sections):

| What you see | Classical name | Safe to change? | Immediate action |
|---|---|---|---|
| `struct Impl; Impl* impl_` | Handle/Body (Pimpl) | ✅ | Migrate raw `Impl*` → `unique_ptr<Impl>` when touching |
| Class: dtor + copy-ctor + copy-assign all defined | Rule of Three | ✅ Correct C++98 | Audit all three together; see `ref-brownfield-survival.md` |
| `int* count_; Body* body_` — shared heap | Counted Body | ⚠️ Migrate carefully | Replace with `shared_ptr<Body>` on next touch |
| Abstract base ptr inside value-type wrapper | Envelope/Letter | ⚠️ Preserve at ABI | Migrate ptr to `unique_ptr<Base>` + explicit `clone()` |
| `AddRef()` / `Release()` methods | COM `IUnknown` | 🔴 Do not remove | Preserve; wrap with smart-pointer adapter at AA boundary |
| `volatile bool flag` between threads | Volatile-for-threading | 🔴 Defect | Replace with `std::atomic<bool>` — per [ENG-6.1](laws/engineering/eng-6-security.md), `volatile` ≠ thread-safe under C++11 memory model |
| `struct Cmp { bool operator()(T,T) const; }` | Functor | ✅ Valid | Prefer lambda in new code; keep named functors for reuse |
| `template<class T, class U> struct Typelist` | Loki TypeList | ⚠️ Migrate | Replace with `std::tuple<T,U>` or `std::variant` |
| `template<typename D> class Base { cast<D*>(this)-> }` | CRTP | ✅ Preserve C++98/14 | Do not refactor to virtual; add to brownfield routing when `crtp.md` ships (per [ENG-3.1](laws/engineering/eng-3-code-quality.md)) |
| `void fn(Iter&, n, random_access_tag{})` | Tag dispatching | ✅ Preserve | Use `if constexpr` for new code only |

> **Full vocabulary, code examples, and rationale:** [`docs/guides/avatars/cpp-classical-idiom-atlas.md`](docs/guides/avatars/cpp-classical-idiom-atlas.md)

### Safe Modification Strategies

Per [ENG-4.1](laws/engineering/eng-4-testing.md) (Atomic TDD) and [ENG-4.10](laws/engineering/eng-4-testing.md) (Test Evolution Law), all modifications to legacy code must be covered by tests. When modifying code you don't fully understand, follow Michael Feathers' legacy code techniques:

1. **Write characterization tests first** — before changing anything, write tests that capture the current behavior. These tests prove you haven't broken anything after your change.
2. **Use the Sprout Method** — instead of modifying an existing function, write new logic in a new function and call it from the original. This minimizes risk to existing code.
3. **Use the Wrap Method** — wrap an existing function with new behavior (before/after logic) without modifying the original implementation.
4. **Never mix behavior change and refactor** — commit refactoring separately from feature changes. Each commit should do exactly one thing.
5. **Add RAII wrappers incrementally** — when you touch a function with raw resource management, wrap one resource at a time in a RAII handle. Don't rewrite the entire function.

### Debugging Legacy C++ Code

Essential tools for understanding and debugging unfamiliar code:

| Tool | When to Use | Quick Start |
|------|-------------|-------------|
| **GDB / LLDB** | Understanding control flow, inspecting state | `gdb ./binary`, then `break main`, `run`, `bt` for backtrace |
| **AddressSanitizer** | Finding memory bugs during development | Compile with `-fsanitize=address -fno-omit-frame-pointer` |
| **Valgrind** | Legacy code without sanitizer support | `valgrind --leak-check=full ./binary` |
| **strace / ltrace** | Understanding system calls and library usage | `strace -f ./binary 2>&1 \| head -100` |
| **perf** | Finding CPU hotspots | `perf record ./binary && perf report` |

### Common Legacy Pitfalls

These issues frequently catch new engineers working on existing C++ codebases:

- **Implicit conversions** — C++ silently converts between types (e.g., `int` to `bool`, `double` to `int`). Enable `-Wconversion` to surface these.
- **Undefined behavior that "works on my machine"** — UB may appear to work in debug builds but crash in release (or on different compilers). Never assume current behavior is correct if the code has UB.
- **Header inclusion order dependencies** — some legacy code only compiles if headers are included in a specific order. Add missing `#include` directives rather than relying on transitive includes.
- **Static initialization order fiasco** — globals in different files initialize in undefined order. If you see a crash on startup, check for cross-file global dependencies.
- **Build system tribal knowledge** — legacy projects often have undocumented flags, defines, or environment variables. Document anything you discover in the project's `README.md` or `AGENTS.md`.

### Modernization Entry Points

When working in legacy code, apply these incremental improvements to code you touch (but don't rewrite untouched code):

1. **Smart pointers** — replace `new`/`delete` with `std::make_unique` in functions you modify
2. **`const` correctness** — add `const` to parameters and methods as you understand const-safe paths
3. **`nullptr`** — replace `NULL` and `0` with `nullptr` in touched code
4. **`override`** — add `override` to virtual function overrides you encounter (catches signature mismatches)
5. **Range-based `for`** — replace manual iterator loops with range-based `for` when touching loop code
6. **`auto`** — use `auto` for complex iterator types and factory results (but keep explicit types for numeric variables)

### Skill Development Path

Progress from novice to proficient through these phases:

| Phase | Focus | Activities |
|-------|-------|------------|
| **Phase 1: Read & Understand** | Code archaeology, characterization tests | Read CMakeLists.txt, trace call chains, write tests for existing behavior |
| **Phase 2: Modify Safely** | Sprout/wrap methods, incremental RAII | Fix bugs and add features using safe modification techniques |
| **Phase 3: Modernize** | Smart pointers, concepts, ranges | Apply modern C++ patterns to code you own; propose modernization PRs |
| **Phase 4: Design** | Ownership-first, RAII, concepts, coroutines | Design new components following full governance guidance |


---

## See Also

- [Legacy Codebase Triage Playbook](ref-legacy-triage-playbook.md)
