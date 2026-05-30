---
cpp_version_min: 98
cpp_version_note: >-
  Memory mental models (stack/heap, RAII) apply from C++98 onwards.
avatar: cpp
---

# C++ Avatar Reference: Legacy Mental Models - Memory and Compilation

---

## Mental Model Transitions

For developers joining C++ projects from Java, Python, or other garbage-collected languages, the following mental model gaps are the most common source of bugs and confusion. Per [ENG-3.1](laws/engineering/eng-3-code-quality.md), understanding these transitions is required before modifying legacy code.

### 1. Value Semantics vs Reference Semantics

**From GC languages:** When you write `Flight a = b;`, you get a second reference (handle) pointing to the *same* object on the heap. Mutations through `a` are visible through `b`.

**In C++:** `Flight a = b;` invokes the **copy constructor** creating an independent copy. Mutations to `a` never affect `b`. This is *value semantics*.

```cpp
// Java mental model (WRONG in C++)
Flight a = b;       // C++ copies the ENTIRE Flight object
a.setGate("B12");   // b is unchanged — a is an independent copy

// C++ reference model (explicit)
Flight& ref = b;    // ref IS b — same object
ref.setGate("B12"); // b.gate is now "B12"
```

**Parameter passing decision tree (per [ENG-3.1](laws/engineering/eng-3-code-quality.md)):**

| Intent | Syntax | When |
|--------|--------|------|
| Read only, small type | `int x` | Built-ins, enums, small structs (≤16 bytes) |
| Read only, large type | `const Flight& f` | Default for classes and containers |
| Modify caller's object | `Flight& f` | Output/in-out parameters |
| Nullable/optional input | `const Flight* f` | May be `nullptr` |
| Transfer ownership | `std::unique_ptr<Flight> f` | Sink parameter — caller gives up ownership |

> **Rule of thumb:** default to `const&` for function parameters. Only deviate when you have a specific reason.

### 2. RAII vs Garbage Collection

**From GC languages:** Memory is managed by a garbage collector. You `new` objects and forget about them. Finalizers exist but are unreliable and run at GC's discretion.

**In C++:** There is no garbage collector. Objects on the stack are destroyed **deterministically** when they leave scope — the destructor runs immediately, every time, in reverse order of construction. This is **RAII** (Resource Acquisition Is Initialization), and it is the single most important idiom in C++.

```cpp
void processReservation(const std::string& pnr) {
    DatabaseConnection db("crew-db");     // Constructor opens connection
    auto txn = db.beginTransaction();     // Constructor starts txn

    // ... do work ...

    // If an exception is thrown HERE:
    // ~Transaction() rolls back (RAII)
    // ~DatabaseConnection() closes socket (RAII)
    // No "finally" block needed. No resource leak possible.

}   // txn destroyed first, then db — reverse order, always
```

**RAII replaces:**
- Java's `try-with-resources`
- Python's `with` statement
- C#'s `using` statement

But it works for *every* resource, automatically, without programmer opt-in. `std::unique_ptr` is the canonical RAII wrapper for heap-allocated objects:

```cpp
// BAD — manual delete, exception-unsafe
Flight* f = new Flight("AA100");
process(f);
delete f;  // Skipped if process() throws!

// GOOD — RAII via unique_ptr
auto f = std::make_unique<Flight>("AA100");
process(*f);
// Destructor called automatically — no leak, even on exception
```

### 3. Compilation Model

**From GC languages:** You write `import` or `using`, the compiler/runtime resolves the module, and symbols are available. Compilation units are discovered automatically.

**In C++:** There are no modules (until C++20, and adoption is slow). Instead, there are **four separate phases**:

1. **Preprocessor** — textual substitution (`#include` pastes file contents, `#define` replaces tokens)
2. **Compiler** — each `.cpp` file is compiled independently into an object file (`.o`)
3. **Linker** — object files are combined, symbol references are resolved
4. **Loader** — dynamic libraries resolved at runtime

```
FlightService.h  ──┐
                    ├──▶ FlightService.cpp ──▶ FlightService.o ──┐
FlightService.cpp ──┘                                            │
                                                                 ├──▶ Linker ──▶ executable
CrewScheduler.h  ──┐                                             │
                    ├──▶ CrewScheduler.cpp ──▶ CrewScheduler.o ──┘
CrewScheduler.cpp──┘
```

**Key rules:**
- `#include "file.h"` literally copies and pastes `file.h` into the current file
- The **One Definition Rule (ODR)**: every entity must have exactly one definition across all translation units
- **Forward declarations** (`class Flight;`) let you reference a type without including its header — critical for breaking circular dependencies
- Include guards (`#pragma once` or `#ifndef`) prevent double-inclusion within a single translation unit

### 4. Undefined Behavior

**From GC languages:** Bad operations throw exceptions (`NullPointerException`, `IndexError`, `InvalidOperationException`). The program state remains defined; you can catch and recover.

**In C++:** **Undefined Behavior (UB)** is not an exception. It is not a crash. It means the entire program has no defined semantics — the compiler is free to do *anything*, including:
- Appearing to work correctly (until production)
- Optimizing away your safety checks
- Time-traveling (reordering code that follows UB)
- Formatting your hard drive (theoretically)

**Common sources of UB:**

| UB Source | Example | Why It's Dangerous |
|-----------|---------|-------------------|
| Signed integer overflow | `INT_MAX + 1` | Compiler assumes it never happens; removes overflow checks |
| Null pointer dereference | `Flight* f = nullptr; f->gate()` | May "work" in debug, crash in release |
| Use-after-free | `delete f; f->gate()` | Memory may be reused; reads garbage silently |
| Data race | Two threads write same `int` | Torn reads, corrupted state |
| Out-of-bounds access | `arr[arr.size()]` | Reads adjacent memory; no exception |
| Uninitialized read | `int x; if (x > 0)` | Compiler may assume any value |

**Defense per [ENG-3.1](laws/engineering/eng-3-code-quality.md):**
- Compile with `-fsanitize=address,undefined` in CI
- Use `std::vector::at()` instead of `operator[]` in non-hot paths
- Enable `-Wall -Wextra -Wpedantic`
- Treat every compiler warning as a potential UB indicator

### 5. Pointers vs References vs Values

**From GC languages:** Everything is a reference (or a value type in C#). You rarely think about pointer arithmetic, reference binding rules, or ownership.

**In C++:** There are three fundamental ways to refer to an object, each with different semantics:

| Mechanism | Nullable? | Rebindable? | Owns? | Syntax |
|-----------|-----------|-------------|-------|--------|
| Value | No | N/A (is the object) | Yes | `Flight f;` |
| Reference | No | No | No | `Flight& f = other;` |
| Pointer | Yes | Yes | Maybe | `Flight* f = &other;` |
| `unique_ptr` | Yes | Yes | Yes (exclusive) | `std::unique_ptr<Flight>` |
| `shared_ptr` | Yes | Yes | Yes (shared) | `std::shared_ptr<Flight>` |

**Decision tree:**

```
Do you need to store the object?
├── YES → Use a value (default)
│         Is it too large to copy?
│         ├── YES → std::unique_ptr (ownership) or const& (borrowing)
│         └── NO  → Value
└── NO  → Function parameter
          ├── Read-only, small → by value (int, enum)
          ├── Read-only, large → const&
          ├── Need to modify caller's copy → &
          ├── Might be null → const* or *
          └── Taking ownership → std::unique_ptr (by value, moved in)
```

> **Per [ENG-3.1](laws/engineering/eng-3-code-quality.md):** raw `new`/`delete` is prohibited in application code. Use `std::make_unique` or `std::make_shared`. Raw pointers are for non-owning observation only.

### 6. The Preprocessor

**From GC languages:** There is no preprocessor. Conditional compilation is handled by build tools or runtime checks.

**In C++:** The preprocessor is a **separate text-processing language** that runs *before* the C++ compiler sees your code. It knows nothing about C++ types, scopes, or semantics.

```cpp
// This is NOT a constant — it's text substitution
#define MAX_CREW 12
// Every occurrence of MAX_CREW is replaced with 12 BEFORE compilation

// Prefer: constexpr int MAX_CREW = 12;  // Type-safe, scoped, debuggable
```

**Key preprocessor directives:**

| Directive | Purpose | Modern Alternative |
|-----------|---------|-------------------|
| `#include "file.h"` | Paste file contents | C++20 `import` (limited adoption) |
| `#define NAME value` | Text substitution | `constexpr`, `const`, `inline` |
| `#define MACRO(x) ...` | Function-like macro | `constexpr` function, template |
| `#ifdef / #ifndef` | Conditional compilation | `if constexpr`, build-system flags |
| `#pragma once` | Include guard | (universally supported, use it) |

**Common pitfalls:**
- Macros don't respect scope — `#define max(a,b)` breaks `std::max`
- Macros evaluate arguments multiple times — `max(i++, j++)` increments twice
- Include order matters — different order can change compilation
- Missing include guards cause redefinition errors


---

## See Also

- [Legacy Mental Models - Language and Runtime](ref-mental-models-lang.md)
