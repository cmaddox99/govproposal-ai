---
id: ref-brownfield-survival
cpp_version_min: 98
cpp_version_note: >-
  Applies to all AA C++ tiers. Core survival patterns are C++98-safe.
  MSVC 6.0 golden-master section covers the legacy tier specifically.
  Transitional-tier (C++11/14) teams working in brownfield sections of their
  codebase should read this alongside their standard-version-specific refs.
avatar: cpp
---

# C++ Brownfield Survival Patterns

> **Status:** Fully populated (Rule of Three, MSVC 6.0 Golden-Master sections complete).
> `const char*` Lifetime Traps live in `const-char-lifetime.md` (examples/).

## Purpose

Provides survival patterns for developers working in AA C++ brownfield codebases:
- **Legacy tier** (pre-C++98 / MSVC 6.0 / SPEClient, ~24% AA LOC)
- **Brownfield tier** (C++98/03 / herc-odyssey-linux, ~11% AA LOC)
- **Transitional tier** (C++11/14 / CWR, IOC_ALP, ~60% AA LOC) — when working in
  brownfield sections of a mixed-standard codebase

Per [ENG-4.1](laws/engineering/eng-4-testing.md) (Atomic TDD Law), all code examples
use characterization-test-first patterns. Per [ENG-10.1](laws/engineering/eng-10-documentation.md)
(Documentation Law), all patterns cite their governing law.

## See Also

- `const char*` Lifetime Traps — CBF-10
- MSVC 6.0 Golden-Master Testing (stdlib-only characterization tests) — see [below](#msvc-60-golden-master-testing)

---

## Rule of Three

> **Applies to:** C++98 and C++03.  
> **C++11+ teams:** Skip to the migration note below — use Rule of Five instead.

The **Rule of Three** states: if a class needs to declare **any** of destructor,
copy constructor, or copy assignment operator, it almost certainly needs all three.
The compiler-generated versions do shallow copies and are wrong for any class that
owns a resource (raw pointer, file handle, socket, lock).

Per [ENG-6.1](laws/engineering/eng-6-security.md) (Security by Design Law), resource
ownership must be explicit and exception-safe.

### COMPLIANT — explicit Rule of Three

```cpp
// C++98/03 — owns a heap buffer; all three are declared together
class FlightPlan {
public:
    explicit FlightPlan(std::size_t waypoints)
        : size_(waypoints), data_(new int[waypoints]) {}

    ~FlightPlan() {
        delete[] data_;
    }

    FlightPlan(const FlightPlan& other)
        : size_(other.size_), data_(new int[other.size_]) {
        std::copy(other.data_, other.data_ + size_, data_);
    }

    FlightPlan& operator=(const FlightPlan& other) {
        if (this != &other) {          // self-assignment guard
            int* tmp = new int[other.size_];
            std::copy(other.data_, other.data_ + other.size_, tmp);
            delete[] data_;
            data_ = tmp;
            size_ = other.size_;
        }
        return *this;
    }

private:
    std::size_t size_;
    int*        data_;
};
```

Key points:
- Copy assignment uses the **copy-then-swap** or **copy-into-temp** idiom to keep
  the object valid if `new` throws before `delete[]` runs.
- Self-assignment guard (`if (this != &other)`) prevents deleting `data_` before
  copying from it.

### COMPLIANT — non-copyable type (private-undefined idiom)

When a resource must not be copied (mutex, file handle, connection), declare copy
constructor and copy assignment **private** without defining them. Any accidental
copy call becomes a **linker error** in C++98 — caught at build time.

```cpp
// C++98/03 — non-copyable RAII wrapper (connection owns a socket fd)
class SocketConnection {
public:
    explicit SocketConnection(int fd) : fd_(fd) {}
    ~SocketConnection() { if (fd_ >= 0) ::close(fd_); }

    int fd() const { return fd_; }

private:
    // Declared private, NOT defined — linker error if called
    SocketConnection(const SocketConnection&);
    SocketConnection& operator=(const SocketConnection&);

    int fd_;
};
```

### NON-COMPLIANT — relying on compiler-generated copy for a resource-owning class

```cpp
// BAD — double-free: compiler copies the raw pointer; both objects
// call delete[] on the same memory when they go out of scope
class FlightPlan {
public:
    explicit FlightPlan(std::size_t n) : data_(new int[n]) {}
    ~FlightPlan() { delete[] data_; }   // user-defined dtor ← triggers Rule of Three
    // copy constructor and copy assignment NOT declared → compiler generates shallow copy
private:
    int* data_;  // NON-COMPLIANT: raw pointer ownership without Rule of Three
};
```

### NON-COMPLIANT — using `= delete` in C++98

```cpp
// DOES NOT COMPILE in C++98/03 — = delete is a C++11 feature
class SocketConnection {
    SocketConnection(const SocketConnection&) = delete;      // C++11 only
    SocketConnection& operator=(const SocketConnection&) = delete;  // C++11 only
};
```

Use the **private-undefined idiom** above for C++98 non-copyable types.

### Migration note — Rule of Five (C++11+)

When the project adopts C++11:

1. Replace the private-undefined idiom with `= delete` — explicit and produces
   a clear compiler error at the call site, not a linker error.
2. Add the **move constructor** and **move assignment operator** (`= default` or
   custom) to support efficient container use.
3. Consider `= default` for the copy pair if value semantics are correct.

**Rule of Five** (C++11): destructor, copy constructor, copy assignment, move
constructor, move assignment — all five or none (using `= default`/`= delete`).

## Edge Cases & Warnings

Per [ENG-6.1](laws/engineering/eng-6-security.md) (Security by Design Law), all
edge cases below represent resource-safety hazards in C++98 codebases.

- **Self-assignment** — `if (this != &other)` is mandatory in copy assignment when
  `delete` runs before `new`. Without it, `delete[] data_` frees the memory you are
  about to copy from.
- **Exception safety in copy assignment** — allocate the new resource *before*
  releasing the old one. If `new` throws, the object remains valid (strong guarantee).
- **Order of member declaration** — destructor, copy constructor, copy assignment
  should be grouped together in the class definition so reviewers immediately
  recognise the Rule of Three pattern.
- **Inheritance** — if a base class has a virtual destructor (C++98 polymorphic
  base), each derived class that owns resources needs its own Rule of Three.
  Forgetting the copy pair in a derived class that adds a raw-pointer member is a
  common C++98 bug.
- **`boost::noncopyable`** — a widely used C++98 alternative to the
  private-undefined idiom. Inherit privately: `class Foo : private boost::noncopyable`.
  Produces a clear compile-time error and documents intent. Requires Boost; prefer
  the private-undefined idiom for code with no Boost dependency.
- **Templates** — the Rule of Three applies to class templates too. The compiler
  instantiates the generated copy members per type parameter; forgetting the Rule of
  Three in a template that stores a raw pointer is a latent double-free.


---

## MSVC 6.0 Golden-Master Testing

> **Scope:** Legacy tier only — MSVC 6.0 / Visual Studio 6.0 (VC98).  
> **For all other C++98/03 targets** (GCC ≥ 3.4, MSVC 8.0 / VS 2005 and later):
> use **GTest 1.8.x** (vcpkg pin: `gtest==1.8.1`) instead — see
> see [ENG-4.1](laws/engineering/eng-4-testing.md) (Atomic TDD Law) characterization test pattern example.

MSVC 6.0 (1998) predates every widely-available C++ testing framework. The
STL shipped in VC98 is non-conforming in ways that prevent GTest and Catch2
from compiling. The only universally available test primitives are `<fstream>`,
`<cstdlib>`, and `assert()` from `<cassert>`.

Per [ENG-4.1](laws/engineering/eng-4-testing.md) (Atomic TDD Law), characterization
tests pin **existing behaviour** as the baseline before any change. The
golden-master pattern is the MSVC 6.0-safe implementation of that requirement.

### Pattern — write-then-compare golden master

The golden-master pattern has two modes:

1. **Record mode** — run the code under test, capture its output to a reference
   file (the "golden master"). Commit the file to source control.
2. **Verify mode** — run the same code again, write output to a temp file,
   compare against the golden master. Diff = regression.
3. **Commit atomically** — golden file and any code changes that affect it must be
   committed in the same PR/changeset to preserve traceability.

```cpp
// golden_master.h — stdlib-only; compiles on MSVC 6.0
#ifndef GOLDEN_MASTER_H
#define GOLDEN_MASTER_H

#include <fstream>
#include <string>
#include <cassert>
#include <cstdlib>    // std::remove

// Write 'actual' to a temp file, compare line-by-line to 'golden_path'.
// Calls assert(false) on the first differing line.
inline void assert_matches_golden(const std::string& golden_path,
                                  const std::string& actual) {
    // Write actual output to temp file
    const std::string tmp_path = golden_path + ".tmp";
    {
        std::ofstream tmp(tmp_path.c_str());
        assert(tmp.is_open());
        tmp << actual;
    }

    // Compare golden vs actual line by line
    std::ifstream golden(golden_path.c_str());
    std::ifstream tmp(tmp_path.c_str());
    assert(golden.is_open()); // golden master must exist (record first)

    std::string g_line, t_line;
    int line_num = 0;
    while (std::getline(golden, g_line)) {
        ++line_num;
        bool got = static_cast<bool>(std::getline(tmp, t_line));
        assert(got);          // actual shorter than golden
        assert(g_line == t_line); // content mismatch
    }
    // Actual must not have extra lines
    assert(!std::getline(tmp, t_line));

    std::remove(tmp_path.c_str());
}

// Record mode: write 'actual' as the new golden master.
// Call once manually; commit the result; then switch to verify mode.
inline void record_golden(const std::string& golden_path,
                          const std::string& actual) {
    std::ofstream out(golden_path.c_str());
    assert(out.is_open());
    out << actual;
}

#endif // GOLDEN_MASTER_H
```

### Usage — characterization test for a legacy serialiser

```cpp
// test_flight_serializer_golden.cpp — MSVC 6.0 compatible
#include "golden_master.h"
#include "flight_serializer.h"  // legacy component under test
#include <cassert>

static std::string serialize_sample_flight() {
    FlightRecord rec;
    rec.flight_num = "AA4820";
    rec.origin     = "DFW";
    rec.dest       = "LAX";
    rec.dep_utc    = 1700000000;  // fixed epoch for determinism
    return FlightSerializer::to_csv(rec);
}

int main() {
    const std::string GOLDEN = "tests/golden/flight_serializer_sample.csv";
    const std::string actual = serialize_sample_flight();

    // Switch: record_golden(GOLDEN, actual);   // run once, commit, then comment out
    assert_matches_golden(GOLDEN, actual);      // normal verify mode

    return 0;   // 0 = all asserts passed
}
```

**Workflow:**

1. First run: uncomment `record_golden(...)`, comment out `assert_matches_golden(...)`.
   Build and run. Commit the generated golden file to source control.
2. Subsequent runs: uncomment `assert_matches_golden(...)`, comment out `record_golden(...)`.
   Any output change fails the assert and terminates the process with a non-zero exit code.
3. Deliberate behaviour change: delete the golden file, run in record mode again,
   review the diff in your VCS, then commit the new baseline.

### When to prefer GTest 1.8.x instead

| Compiler / toolchain | Recommended test framework |
|----------------------|---------------------------|
| MSVC 6.0 (VC98) | Golden-master (stdlib-only, above) |
| MSVC 8.0 / VS 2005+ | GTest 1.8.x (`gtest==1.8.1` via vcpkg) |
| GCC 3.4+ / MinGW | GTest 1.8.x |
| Clang (any C++98/03 mode) | GTest 1.8.x |

GTest 1.8.x is the last release that compiles cleanly against a strict C++03
toolchain. Pin to `gtest==1.8.1` in vcpkg or bundle the source directly
(two-file distribution: `gtest-all.cc` + `gtest.h`).

## Edge Cases & Warnings (MSVC 6.0)

Per [ENG-4.1](laws/engineering/eng-4-testing.md) (Atomic TDD Law), these
edge cases affect the reliability of golden-master baselines.

- **Determinism is mandatory** — any non-deterministic output (timestamps,
  pointers, thread-scheduling artefacts, locale-dependent formatting) must be
  stripped or normalised before writing to the golden file. A non-deterministic
  golden master produces a flaky test.
- **Line endings** — MSVC 6.0 writes `\r\n` by default in text mode. Open both
  golden and temp files in the same mode (text or binary) to avoid spurious
  line-ending mismatches across developer machines and CI.
- **`assert()` in release builds** — `NDEBUG` disables `assert()`. Always build
  test binaries without `NDEBUG` (remove `/DNDEBUG` from the test project's
  release config). A passing test that silently skips all assertions is worse
  than a failing test.
- **Exit code convention** — MSVC 6.0 `main()` returns `int`; the OS captures
  it. CI scripts should check `%ERRORLEVEL%` (Windows batch) or `$?` (POSIX).
  An `assert()` failure calls `abort()` which exits with a non-zero code on all
  platforms — CI sees the failure correctly.
- **Floating-point output** — `printf` / `ostream` floating-point formatting
  varied across MSVC runtime versions. If the serialiser emits floats, pin the
  precision explicitly (`std::setprecision(6)` or `%.6f`) in the recording step.
- **Upgrade path** — when the project migrates from MSVC 6.0 to MSVC 8.0+,
  convert golden-master tests to GTest 1.8.x. The golden files become `EXPECT_EQ`
  assertions. This is a mechanical translation; do it as the first task after the
  compiler upgrade.

---
