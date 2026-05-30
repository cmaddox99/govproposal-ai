---
id: ref-brownfield-coplien
cpp_version_min: 98
cpp_version_note: >-
  Applies to all AA C++ legacy-tier and brownfield-tier codebases.
  These patterns appear in CWR, herc-odyssey-linux, and SPEClient.
  Governance verdicts are AA-specific — general LLM training data
  does not include the AA migration rulings.
avatar: cpp
---

# C++ Coplien-Era Pattern Recognition ★ C++98

Patterns from the Coplien / early GoF era appear extensively in AA's C++98 legacy
codebase. General LLMs know these patterns abstractly. This file adds the
**AA governance verdict**: what to do when you encounter them in CWR,
herc-odyssey-linux, or SPEClient.

> **Full vocabulary:** See [`docs/guides/avatars/cpp-classical-idiom-atlas.md`](docs/guides/avatars/cpp-classical-idiom-atlas.md)

## Pattern Recognition Table

| What you see in code | Pattern name | Governance verdict | Action |
|---|---|---|---|
| `struct Impl; Impl* impl_` in a class header | **Handle/Body (Pimpl)** | ✅ PRESERVE — good design | Migrate `impl_` from raw `Impl*` to `std::unique_ptr<Impl>` when touching the class. **Note:** unique_ptr makes the class move-only; if copy semantics are required, add explicit deep-copying copy ctor/assign that clones the Impl. Evaluate ABI impact before migrating. |
| Class with both `~Foo()` dtor and `Foo(const Foo&)` copy ctor | **Rule of Three** | ✅ CORRECT for C++98 | Audit all three: dtor, copy-ctor, copy-assign. See `ref-brownfield-survival.md §Rule of Three`. |
| Class with `int* count_; Body* body_` — shared heap body | **Counted Body** | ⚠️ MIGRATE | Replace with `std::shared_ptr<Body>` on next touch; do not extend this pattern |
| Class with abstract base ptr; outer class has copy semantics | **Envelope/Letter** | ⚠️ PRESERVE / MIGRATE | Preserve at ABI. Migrate outer ptr to `std::unique_ptr<Base>` with explicit `clone()` |
| `virtual void AddRef() = 0; virtual void Release() = 0;` | **COM IUnknown** | ⚠️ PRESERVE AT ABI BOUNDARY | Do not remove. Wrap with smart-pointer adapter at the AA code boundary. |
| `volatile bool g_shutdown` used between threads | **Volatile-for-threading** | 🔴 NON-COMPLIANT — defect | Replace with `std::atomic<bool>` (C++11). Per [ENG-6.1](laws/engineering/eng-6-security.md), `volatile` provides no memory ordering guarantee under the C++11 memory model. See `thread-stop-flag.md`. |
| `bool operator()(const T& a, const T& b) const` struct | **Functor / Function Object** | ✅ VALID | Prefer lambda in new code; named functors are still correct and readable for reused comparators |

## Exception Safety Vocabulary

Code comments in C++98 codebases often use Sutter's guarantee levels. When you see
these terms, the author was explicitly communicating the exception contract:

| Term | Meaning | What to preserve |
|---|---|---|
| **basic guarantee** | If throws: no leak, invariants hold, state valid but unspecified | RAII in destructors |
| **strong guarantee** | If throws: state is completely unchanged (commit-or-rollback) | Copy-and-swap pattern in `operator=` |
| **nothrow / no-throw** | Operation never throws | `throw()` in C++98 → `noexcept` in C++11+ |
| **copy-and-swap** | `operator=` makes a copy locally, then swaps — gives strong guarantee | The swap must be `noexcept` |

Per [ENG-6.1](laws/engineering/eng-6-security.md), resource-owning classes must honour at
minimum the basic guarantee. Copy-and-swap gives the strong guarantee at the cost of one
extra allocation — use it in `operator=` for any class that owns a heap resource.

> **Further reading:** Sutter, *Exceptional C++* (1999); GOTW #64 — https://herbsutter.com/gotw/_064/

## See Also

- `ref-brownfield-survival.md` — Rule of Three, MSVC 6.0 golden-master testing
- `ref-legacy-smells-patterns.md` — broader legacy smell catalogue
- `docs/guides/avatars/cpp-classical-idiom-atlas.md` — full idiom vocabulary
