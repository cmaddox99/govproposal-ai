---
law_id: ENG-6.1
cpp_version_min: 14
avatar: cpp
title: Security by Design — Topic Router Index
tokens: ~280
type: index
---

# ENG-6.1 Security by Design — C++ Topic Router

**Law:** ENG-6.1 (Security by Design — Non-Negotiable)  
**Avatar:** `avatars/technology/cpp/`  
**Type:** Index — route to the specific file for your security topic.

---

## How to Use This Index

Load **only the file that matches your topic** — do not load all ENG-6.1 files.
Each file is ≤ 850 tokens. Loading all ENG-6.1 files at once would exceed any context budget.

---

## COMPLIANT Routing

| Topic | File | When to Use |
|-------|------|-------------|
| General security architecture | [ENG-6.1-security-by-design.md](ENG-6.1-security-by-design.md) | Starting point — security invariants, threat modelling |
| Raw pointer / `void*` migration | [ENG-6.1-void-star-migration.md](ENG-6.1-void-star-migration.md) | Replacing `void*` with typed alternatives |
| `auto_ptr` → `unique_ptr` | [ENG-6.1-auto-ptr-migration.md](ENG-6.1-auto-ptr-migration.md) | Eliminating deprecated C++03 ownership |
| Smart pointer ownership | [ENG-6.1-smart-pointers.md](ENG-6.1-smart-pointers.md) | `unique_ptr`, `shared_ptr`, `weak_ptr` rules |
| Smart pointer migration path | [ENG-6.1-smart-pointer-migration.md](ENG-6.1-smart-pointer-migration.md) | Step-by-step brownfield upgrade |
| RAII resource management | [ENG-6.1-raii-resources.md](ENG-6.1-raii-resources.md) | File handles, sockets, locks |
| RAII wrapping C APIs | [ENG-6.1-raii-c-api-wrapper.md](ENG-6.1-raii-c-api-wrapper.md) | Wrapping OS/third-party C handles |
| Cast governance | [ENG-6.1-cast-governance.md](ENG-6.1-cast-governance.md) | `static_cast` / `reinterpret_cast` rules |
| Move semantics | [ENG-6.1-move-semantics.md](ENG-6.1-move-semantics.md) | Efficient transfer, `std::move`, `noexcept` |
| Null safety | [ENG-6.1-null-safety.md](ENG-6.1-null-safety.md) | Eliminating null dereference |
| Strict aliasing | [ENG-6.1-strict-aliasing.md](ENG-6.1-strict-aliasing.md) | Type-punning, UB from aliasing violations |
| Thread safety | [ENG-6.1-thread-safety.md](ENG-6.1-thread-safety.md) | Mutex, atomic, data race prevention — C++17 `scoped_lock` |
| Thread safety (C++11) | [ENG-6.1-thread-safety-cpp11.md](ENG-6.1-thread-safety-cpp11.md) | `lock_guard` + `std::thread` — C++11 portable threading |
| Smart pointers (C++11) | [ENG-6.1-smart-pointers-cpp11.md](ENG-6.1-smart-pointers-cpp11.md) | `unique_ptr(new T(...))` before `make_unique`; C++11 ownership |
| Format string safety | [ENG-6.1-format-string-safety.md](ENG-6.1-format-string-safety.md) | `printf` risks, iostream, fmtlib/spdlog, `std::format` (C++20) |
| Thread migration | [ENG-6.1-thread-migration.md](ENG-6.1-thread-migration.md) | POSIX threads → `std::thread` |
| `volatile` vs atomic | [ENG-6.1-volatile-vs-atomic.md](ENG-6.1-volatile-vs-atomic.md) | When `volatile` is wrong, when atomic is right |
| Expected errors / error safety | [ENG-6.1-expected-errors.md](ENG-6.1-expected-errors.md) | Exception-safe code, strong/basic guarantee |
| Legacy modernisation (before/after) | [ENG-6.1-legacy-modernization-before-after.md](ENG-6.1-legacy-modernization-before-after.md) | Side-by-side old vs new code |
| MISRA C++ / DO-278A safety-critical | [ENG-6.1-misra-do278a.md](ENG-6.1-misra-do278a.md) | DO-278A Assurance Level B/C, MISRA rules for aviation |
| JNI safety-critical boundary | [ENG-6.1-safety-critical-jni.md](ENG-6.1-safety-critical-jni.md) | Safety-critical JNI boundary — reference lifecycle, exception propagation |
| MFC/host exception safety | [ENG-6.1-host-exception-safety.md](ENG-6.1-host-exception-safety.md) | Exception safety in brownfield MFC codebases |
| FAR 117 timezone bridge (C++14) | [ENG-6.1-timezone-cpp14.md](ENG-6.1-timezone-cpp14.md) | HowardHinnant/date for C++11/14 — **[STUB — content pending CBF adoption]** |
| JNI thread safety C++98 | [ENG-6.1-jni-thread-cpp98.md](ENG-6.1-jni-thread-cpp98.md) | pthread_key_t / TlsAlloc — **[STUB — content pending CBF adoption]** |
| JNI thread safety C++11 | [ENG-6.1-jni-thread-cpp11.md](ENG-6.1-jni-thread-cpp11.md) | thread_local RAII — **[STUB — content pending CBF adoption]** |
| Safe string formatting (fmtlib) | [ENG-6.1-fmtlib-format.md](ENG-6.1-fmtlib-format.md) | fmtlib bridge for C++11/14 — **[STUB — content pending CBF adoption]** |
| Bounds-safe array view (gsl::span) | [ENG-6.1-gsl-span-cpp14.md](ENG-6.1-gsl-span-cpp14.md) | gsl::span bridge for C++14 — **[STUB — content pending CBF adoption]** |
| Cooperative thread stop-flag | [ENG-6.1-thread-stop-flag.md](ENG-6.1-thread-stop-flag.md) | std::atomic<bool> manual cancellation — **[STUB — content pending CBF adoption]** |
| Lock-free patterns C++11/14 | [ENG-6.1-lock-free-cpp14.md](ENG-6.1-lock-free-cpp14.md) | ABA + SPSC ring buffer — **[STUB — content pending CBF adoption]** |
| Memory ordering (C++11) | [ENG-6.1-memory-ordering.md](ENG-6.1-memory-ordering.md) | All 5 std::memory_order values with happens-before — ESE-17 |
| Parallel algorithms C++17 | [ENG-6.1-parallel-algorithms.md](ENG-6.1-parallel-algorithms.md) | std::execution policies seq/par/par_unseq — ESE-18 |
| const char* lifetime traps | [ENG-6.1-const-char-lifetime.md](ENG-6.1-const-char-lifetime.md) | Pre-C++17 dangling pointer traps — .c_str() lifetime rules, SSO hazard, mutation invalidation |
| string_view lifetime traps (C++17) | [ENG-6.1-string-view-lifetime.md](ENG-6.1-string-view-lifetime.md) | C++17 std::string_view lifetime hazards — **[STUB — ESE task, not yet populated]** |
| std::format safe formatting (C++20) | [ENG-6.1-std-format.md](ENG-6.1-std-format.md) | std::format bridge for C++20 — **[STUB — ESE-16, not yet populated]** |
| std::jthread + stop_token (C++20) | [ENG-6.1-jthread-stop-token.md](ENG-6.1-jthread-stop-token.md) | Cooperative cancellation, stop_callback, volatile NON-COMPLIANT — ESE-30 |
| condition_variable + predicate (C++11) | [ENG-6.1-condition-variable.md](ENG-6.1-condition-variable.md) | Bounded queue, spurious wakeup, cv_any+stop_token — ESE-31 |
| std::span bounds safety (C++20) | [ENG-6.1-span-bounds-safety.md](ENG-6.1-span-bounds-safety.md) | std::span replaces raw ptr+size — ESE-15 |
| std::chrono::zoned_time (C++20) | [ENG-6.1-timezone-cpp20.md](ENG-6.1-timezone-cpp20.md) | FAR 117 timezone arithmetic C++20 — **[STUB — ESE-47, not yet populated]** |
| std::hazard_pointer (C++23) | [ENG-6.1-lock-free-cpp23.md](ENG-6.1-lock-free-cpp23.md) | Lock-free reclamation C++23 — **[STUB — future ESE, not yet populated]** |

---

## NON-COMPLIANT Usage

Loading all ENG-6.1 files in a single RAG query exceeds token budgets and
returns irrelevant sections alongside the needed guidance. Always route by topic.

---

## Quick-Reference: RAII Ownership Pattern

The following is the security-by-design *anchor pattern* common to all ENG-6.1 topics.
For topic-specific details, route to the file above.

```cpp
// Every resource in C++ MUST be owned by an RAII type — never raw
class Connection {
    std::unique_ptr<Socket> socket_;   // owned — destructor closes on any exit
public:
    explicit Connection(std::string host)
        : socket_(std::make_unique<Socket>(std::move(host))) {}
    // No manual cleanup needed — RAII ensures release on destruction
};
```
