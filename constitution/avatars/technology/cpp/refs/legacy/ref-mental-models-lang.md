---
cpp_version_min: 98
cpp_version_note: >-
  Language mental models (linkage, ODR, ADL) apply from C++98 onwards.
avatar: cpp
---

# C++ Avatar Reference: Legacy Mental Models - Language and Runtime

---

### 7. Linking

**From GC languages:** The runtime/compiler resolves symbols automatically. "ClassNotFoundException" is the closest analogy and is a runtime error.

**In C++:** "Undefined reference to `Flight::getGate()`" is a **linker** error, not a compiler error. Your code compiled fine — the compiler saw the *declaration* in the header. But the linker could not find the *definition* (the actual function body) in any object file or library.

**The mental model:**

```
COMPILE TIME (per .cpp file):
  "I trust that Flight::getGate() exists because I saw the declaration in Flight.h"
  → Produces Flight.o with a PLACEHOLDER for getGate()

LINK TIME (all .o files together):
  "Now I need to fill in all placeholders with actual addresses"
  → If Flight.cpp wasn't compiled or linked: UNDEFINED REFERENCE
```

**Common causes of linker errors:**
1. Forgot to add `.cpp` file to build system (CMakeLists.txt)
2. Defined function in header without `inline` → multiple definitions (ODR violation)
3. Template defined in `.cpp` file instead of header → not instantiated
4. Mismatched function signature between declaration and definition
5. Missing library in linker flags (`-lsqlite3`, `target_link_libraries()`)

**Diagnosis per [ENG-3.1](laws/engineering/eng-3-code-quality.md):**
- `nm -C object.o` — list symbols (C++ demangled)
- `ldd executable` — list dynamic library dependencies
- `c++filt` — demangle symbol names

### 8. const Correctness

**From GC languages:** `final` (Java/C#) prevents reassignment of a variable. It does not make the object immutable. Python has no built-in immutability.

**In C++:** `const` is a **deep, transitive contract** enforced by the compiler. It propagates through references, pointers, and member functions:

```cpp
class Flight {
public:
    // const member function — promises not to modify *this
    std::string getGate() const { return gate_; }

    // non-const — may modify *this
    void setGate(const std::string& g) { gate_ = g; }

private:
    std::string gate_;
};

void printFlight(const Flight& f) {
    f.getGate();     // OK — getGate() is const
    f.setGate("C4"); // COMPILE ERROR — f is const, setGate() is not
}
```

**The rules:**
- `const Flight& f` — cannot modify the Flight through `f`
- `const std::string& gate` — cannot modify the string
- `std::string getGate() const` — this member function will not modify the object
- `const` member functions can only call other `const` member functions on `*this`

**Per [ENG-3.1](laws/engineering/eng-3-code-quality.md):** Mark every parameter, return value, and member function `const` unless mutation is specifically required. `const` correctness is self-documenting code — it tells readers "this path does not change state."

> **East const vs West const:**
> - West const: `const int* p` — "pointer to const int" (traditional, most common)
> - East const: `int const* p` — same meaning, reads left-to-right consistently
> - Either is fine; be consistent within a codebase.

### 9. `volatile` — It Does NOT Mean What You Think

**From Java:** `volatile` guarantees visibility across threads and provides acquire/release memory ordering. You use it for safe lock-free communication.

**In C++:** `volatile` does **none of that**. It only tells the compiler "don't optimize away reads/writes to this variable." It provides **no atomicity and no memory ordering**. Using `volatile` for thread synchronization is undefined behavior.

| Feature | Java `volatile` | C++ `volatile` | C++ `std::atomic` |
|---------|----------------|----------------|-------------------|
| Prevents optimization | ✅ | ✅ | ✅ |
| Atomic read/write | ✅ | ❌ | ✅ |
| Memory ordering | Acquire/Release | ❌ None | Configurable |
| Thread-safe | ✅ | ❌ **UB** | ✅ |

```cpp
// ❌ UB: volatile does NOT make this thread-safe
volatile bool stop_flag = false;  // Java habit — WRONG in C++

// ✅ Correct: use std::atomic
std::atomic<bool> stop_flag{false};
```

**The rule per [ENG-6.1](laws/engineering/eng-6-security.md):** Never use `volatile` for inter-thread communication. Use `std::atomic` for lock-free variables and `std::mutex` for complex shared state. The only valid uses of `volatile` in modern C++ are memory-mapped I/O and signal handlers.

### 10. Generics vs Templates — Compile-Time Code Generation

**From Java:** Generics use type erasure — `List<String>` and `List<Integer>` share the same bytecode at runtime. The compiler inserts casts automatically.

**In C++:** Templates are compile-time code generators. `vector<string>` and `vector<int>` produce **completely separate compiled code**. This means:

| Aspect | Java Generics | C++ Templates |
|--------|---------------|---------------|
| Implementation | Type erasure (single bytecode) | Code generation (separate binary per type) |
| Runtime type info | Erased (`List<String>` → `List` at runtime) | Full type info preserved |
| Constraints | `<T extends Comparable<T>>` | `requires` clauses (C++20 concepts) |
| Compilation | Fast (no duplication) | Slower (instantiated per type) |
| Error messages | Clear (bounded type parameters) | Historically terrible; concepts help |

```cpp
// Java mental model:  <T extends Comparable<T>>
// C++20 equivalent:
template<typename T>
    requires std::totally_ordered<T>
void sort(std::vector<T>& v);

// Without concepts (C++17): errors appear at instantiation — deeply nested, confusing
// With concepts (C++20): errors appear at call site — "T does not satisfy totally_ordered"
```

**The rule per [ENG-3.1](laws/engineering/eng-3-code-quality.md):** Always constrain templates with C++20 concepts. Unconstrained templates produce incomprehensible error messages that waste hours of developer time.

### 11. Exception Handling — No Checked Exceptions, No `finally`, No `synchronized`

**In C++:** None of Java's exception constructs exist:

| Java | C++ Equivalent | Key Difference |
|------|---------------|----------------|
| Checked exceptions | *(nothing)* | All exceptions are unchecked |
| `finally { cleanup(); }` | RAII destructor | No `finally` keyword |
| `try-with-resources` | RAII `{ std::lock_guard lock{m}; }` | Scope-based cleanup |
| `synchronized` | `std::mutex` + `std::lock_guard` | Must be explicit |
| `throws IOException` | `noexcept` (opt-in for no-throw) | Default is may-throw |

```cpp
// ❌ Java habit — delete in finally-equivalent:
auto* conn = new Connection(url);
conn->execute(query);  // throws? conn leaks
delete conn;

// ✅ RAII — destructor runs even on exception:
auto conn = std::make_unique<Connection>(url);
conn->execute(query);
// conn destroyed here automatically
```

**Per [ENG-7.1](laws/engineering/eng-7-reliability.md):** Never write `finally`-style cleanup. RAII replaces it entirely.

### 12. Lambda Captures — There Is No Garbage Collector

**From Java:** Lambdas capture references; the GC keeps objects alive.

**In C++:** Captures are **raw copies or raw references** — no GC. Capturing a reference to a local variable that outlives the lambda's scope is **undefined behavior**.

```cpp
// ❌ UB: captured reference dangles after function returns
auto make_callback(const std::string& name) {
    return [&name]() { return name; };  // name is destroyed when function returns
}

// ✅ Safe: capture by value
auto make_callback(std::string name) {
    return [name]() { return name; };  // copied into lambda
}

// ✅ Safe: shared ownership extends lifetime
auto make_callback(std::shared_ptr<std::string> name) {
    return [name]() { return *name; };
}
```

**Rules per [ENG-6.1](laws/engineering/eng-6-security.md):**
- **`[&]`:** Only safe when lambda does not outlive current scope (e.g., `std::sort`).
- **`[=]`:** Safer default for lambdas stored in data structures or returned.
- **Coroutines:** After `co_await`, `[&]` captures bound to caller's stack are dangling — always capture by value.

### 13. `static` — Four Meanings in One Keyword

**From Java:** `static` means "belongs to the class, not the instance." One meaning.

**In C++:** `static` has **four different meanings** depending on context:

| Context | Meaning | Java Equivalent |
|---------|---------|-----------------|
| `static` member variable | Shared across all instances (like Java) | `static` field |
| `static` member function | No `this` pointer (like Java) | `static` method |
| `static` local variable | Initialized once, persists across calls | No equivalent (singleton pattern) |
| `static` at file/namespace scope | Internal linkage — invisible outside this file | `private` class (roughly) |

```cpp
// Meaning 1 & 2: Same as Java
class FlightCounter {
    static int count;                    // shared across instances
    static int getCount() { return count; }  // no this pointer
};

// Meaning 3: Thread-safe since C++11 (Meyers singleton)
Connection& getConnection() {
    static Connection conn("db://prod");  // initialized once, on first call
    return conn;                          // persists for program lifetime
}

// Meaning 4: Internal linkage — only visible in this .cpp file
static void helper() { /* ... */ }  // prefer anonymous namespace instead:
namespace { void helper() { /* ... */ } }  // modern C++ equivalent
```

**The rule per [ENG-3.1](laws/engineering/eng-3-code-quality.md):** Prefer `namespace { }` (anonymous namespace) over `static` for file-scope functions and variables. It's clearer in intent and works for types (not just functions/variables). Use `static` for class members and Meyers singletons only.

---


---

## See Also

- [Legacy Mental Models - Memory and Compilation](ref-mental-models-memory.md)
