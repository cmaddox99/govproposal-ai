---
cpp_version_min: 98
cpp_version_note: >-
  FAR Part 117 CWR compliance governance applies to all C++ versions including C++98/03
  codebases. Governance patterns (characterization tests, golden-file validation, structured
  error signaling) are version-agnostic. Code examples in this file use C++11+ std::chrono
  APIs. For C++98 timezone arithmetic (POSIX gmtime_r/mktime/difftime), direct legacy teams
  to the platform team for UTC offset and DST-safe time boundary calculations.
avatar: cpp
---

# C++ Avatar Reference: FAR 117 Aviation Safety and CWR

---

## FAR 117 Aviation Safety — Crew Rest and Duty Compliance in C++

> **Context:** CWR `CrewRecoveryFAR117` enforces FAA FAR Part 117 crew rest and
> flight-time limits in C++98. A wrong answer — even a transient one — can produce
> illegal crew pairings and put airlines out of FAA compliance.
>
> **Governing laws:** [ENG-4.1](laws/engineering/eng-4-testing.md) (Atomic TDD),
> [ENG-6.1](laws/engineering/eng-6-security.md) (Security by Design),
> [BUS-2.1](laws/business/bus-2-compliance.md) (FAA Compliance)

### What FAR 117 Requires from Software

FAR Part 117 governs pilot flight time, duty periods, and rest requirements.
C++ code enforcing these rules must:

1. **Be correct** — a miscalculation in minimum rest hours (§117.25) or flight-time
   limits (§117.23) is an FAA violation, not just a software bug
2. **Be auditable** — outputs must be traceable to inputs for FAA record-keeping
3. **Be stable** — the calculation logic must not silently change between deployments

### CWR Pattern: Observed FAR 117 Functions

The CWR codebase implements these key compliance calculations:

| Function | FAR 117 Reference | Purpose |
|----------|-------------------|---------|
| `FAR117FLtTimeTable()` | §117.23 — Flight Time Limits | Lookup table for max cumulative flight hours |
| `MinRestAndEight()` | §117.25 — Rest Requirements | Compute minimum rest period before next duty |
| `getDiurnalTime()` | §117.21 — Augmented crews | Calculate Window of Circadian Low (WOCL) adjustments |

### Governance Pattern 1: Characterization Tests Before Any Change

**Never modify FAR 117 calculation code without a characterization test suite.**
The cost of an incorrect change is an FAA violation; the cost of a thorough test is low.

```cpp
// tests/unit/FAR117/MinRestCharacterizationTest.cpp
#include <gtest/gtest.h>
#include "Solver/FAR117Compliance.h"

// Golden-file driven: generated from known-good solver runs, reviewed by ops team
TEST(FAR117Characterization, MinRestAndEight_DomesticDuty_Returns10Hours) {
    // Arrange — frozen fixture representing a domestic duty period
    CrewDutyNode duty = LoadFixture<CrewDutyNode>("fixtures/far117/domestic_duty.xml");

    // Act — call the real FAR 117 function, no mocking
    int rest_minutes = MinRestAndEight(duty);

    // Assert — characterize the OBSERVED output (reviewed and approved by ops)
    // If this value changes, STOP and get ops team sign-off before proceeding
    EXPECT_EQ(rest_minutes, 600)  // 10 hours = 600 minutes (§117.25 minimum)
        << "FAR 117 §117.25 minimum rest characterization failure — "
           "requires ops team review before merging";
}
```

### Governance Pattern 2: Golden-File Validation for End-to-End Outputs

For the JNI entry point, use golden-file tests to lock in the full JSON response:

```cpp
TEST(FAR117GoldenFile, SolverOutputMatchesApprovedBaseline) {
    std::string input  = ReadFile("fixtures/far117/schedule_request_001.xml");
    std::string actual = SolverFacade::run(input);

    // Golden file reviewed and signed off by crew scheduling ops team
    std::string golden = ReadFile("fixtures/far117/golden_response_001.json");

    EXPECT_EQ(actual, golden)
        << "FAR 117 golden-file mismatch — diff the output and get ops approval "
           "before updating the golden file";
}
```

**Updating a golden file** requires:
1. Diff the old and new outputs — understand every change
2. Ops team sign-off that the new output is legally correct
3. Commit the new golden file with a comment citing the FAR section validated

### Governance Pattern 3: No Silent Fallbacks on Compliance Failures

FAR 117 code must **never silently return a default value** when a constraint
cannot be evaluated. Return a structured error that the Java host can detect:

```cpp
// COMPLIANT — structured error, Java host must handle explicitly
std::string MinRestAndEight_safe(const CrewDutyNode& duty) {
    if (!duty.is_valid()) {
        return "{\"error\":\"FAR117-INVALID-DUTY\",\"section\":\"117.25\"}";
    }
    int rest = MinRestAndEight(duty);
    if (rest < 0) {
        return "{\"error\":\"FAR117-CONSTRAINT-VIOLATION\",\"section\":\"117.25\"}";
    }
    return FormatRestResult(rest);
}

// NON-COMPLIANT — returns 0 on failure; Java host may interpret as valid
int MinRestAndEight_unsafe(const CrewDutyNode& duty) {
    if (!duty.is_valid()) return 0;  // silently wrong
    return MinRestAndEight(duty);
}
```

### FAR 117 Code Review Checklist

| Check | Rationale |
|-------|-----------|
| Characterization tests exist for all `FAR117*` functions | Prevents silent regression |
| Golden-file tests cover end-to-end JNI output | Locks in legally-reviewed outputs |
| No silent fallbacks returning 0 / default on constraint failure | Failures must be explicit |
| All constraint values cite FAR section in a comment | Traceability for FAA audit |
| Any change to FAR 117 logic reviewed by ops/compliance team | Regulatory requirement |
| Outputs logged with input hash for audit trail (per [ENG-6.7](laws/engineering/eng-6-security.md)) | FAA record-keeping |

---

---

### WCET (Worst-Case Execution Time) Annotation

DO-278A AL 2/3 ground systems must document and bound WCET for scheduling functions.
Use `std::chrono::high_resolution_clock` to assert timing SLAs in GoogleTest:

```cpp
TEST(CrewRestPolicy, wcet_under_50ms_far117_23a) {
    auto start = std::chrono::high_resolution_clock::now();
    rest_policy_.approve(crew_, fdp_, hours{9});
    auto elapsed = std::chrono::high_resolution_clock::now() - start;
    EXPECT_LT(std::chrono::duration_cast<std::chrono::milliseconds>(elapsed).count(), 50)
        << "FAR 117 rest check must complete within 50 ms SLA";
}
```

Document the agreed deadline in a `WCET_SLA_MS` constant; bump version when the
hardware target changes. Timing tests are flaky on shared CI runners — gate on
a dedicated benchmark job, not the standard test suite.

---

## CWR Anti-Pattern Catalog

> **Source:** Patterns observed during codebase scan of `CrewRecoveryFAR117` (C++98).
> Each entry documents the anti-pattern as found, the risk it poses, and the
> constitutional remedy. Use this catalog when triaging brownfield C++98 codebases.
>
> **Governing laws:** [ENG-3.1](laws/engineering/eng-3-code-quality.md) (Complexity),
> [ENG-6.1](laws/engineering/eng-6-security.md) (Security by Design),
> [ENG-4.1](laws/engineering/eng-4-testing.md) (Atomic TDD)

### AP-1: God Class (947 KB implementation file)

**Observed:** `Solver/Crew.cpp` — a single 947 KB implementation file containing
hundreds of methods, global state, FAR 117 logic, data hydration, and solver
orchestration in one class.

**Risk:** Any change touches untestable, deeply coupled logic. A single PR can
silently break FAR 117 compliance in a path untouched by the change.

**Remedy (per [ENG-3.1](laws/engineering/eng-3-code-quality.md)):**
1. Write characterization tests first — lock in current behaviour before splitting
2. Extract cohesive responsibility clusters using the Strangler Fig pattern
3. Each extracted class gets its own unit tests before the god class shrinks

```cpp
// Strangler Fig: extract FAR 117 logic into a focused class
class FAR117Compliance {       // extracted from Crew.cpp
public:
    int minRestMinutes(const CrewDutyNode& duty) const;
    bool isFlightTimeExceeded(const CrewNode& crew) const;
};
```

### AP-2: Raw `malloc` / Manual Memory Management

**Observed:** `malloc`, `free`, and unguarded `new` throughout `Solver/` and
`PopulateSolver/`, with no RAII wrappers.

**Risk:** Memory leaks on exception paths (including `throw -1` — see AP-4).
Buffer overruns from manual size arithmetic. Double-free on error branches.

**Remedy (per [ENG-6.1](laws/engineering/eng-6-security.md)):**
Replace with C++98-compatible RAII where possible; use `std::vector` and
`std::string` instead of raw arrays.

```cpp
// BEFORE (C++98 anti-pattern)
char* buf = (char*)malloc(MAX_RESPONSE);
// ... many code paths, some with early return — leak risk

// AFTER (C++98-compatible RAII)
std::string buf;
buf.reserve(MAX_RESPONSE);  // no leak on any path
```

### AP-3: 14 Global `extern` Variables

**Observed:** 14 global `extern` variables shared across translation units,
including solver state and FAR 117 lookup tables.

**Risk:** Non-deterministic behaviour under concurrent JNI calls. Impossible to
unit-test in isolation. Load-order bugs between translation units.

**Remedy:** Encapsulate in a `SolverContext` struct passed explicitly, or use
a thread-local singleton pattern safe for JNI re-entrancy.

```cpp
// BEFORE
extern int g_solver_mode;          // shared, racy under concurrent JNI calls
extern FAR117Table g_far117_table; // non-const global — mutation risk

// AFTER (C++98-compatible)
struct SolverContext {
    int solver_mode;
    const FAR117Table far117_table;  // const after construction
};
```

### AP-4: `throw int` / `throw -1` Error Handling

**Observed:** Integer literals used as exception values (e.g., `throw -1`,
`throw 3`) throughout the solver. No exception hierarchy.

**Risk:** These integers escape into the JNI boundary unless caught. A
`catch (int)` clause is easily missed; `catch (...)` must be used at the JNI
entry point (see JNI Safety section). Integer codes have no diagnostic value
in production logs.

**Remedy:** Define a typed exception hierarchy, even in C++98:

```cpp
// C++98-compatible exception hierarchy
struct SolverError {
    int code;
    const char* message;
    explicit SolverError(int c, const char* m) : code(c), message(m) {}
};

// throw SolverError(-1, "FAR117: constraint violation in MinRestAndEight");
// catch (const SolverError& e) { log(e.code, e.message); }
```

### AP-5: 470-Method Header File (Inline Method Explosion)

**Observed:** A header file with 470 inline method definitions, used as a de-facto
implementation file.

**Risk:** Every translation unit that includes this header recompiles all 470
methods. Catastrophic incremental build times. Tight coupling — callers rebuild
on any private method change.

**Remedy:** Move implementations to `.cpp` files. Expose only the public interface
in the header. Incremental builds drop from minutes to seconds.

### AP-6: `FILE*` Without RAII

**Observed:** `fopen` / `fclose` pairs with manual close, including paths where
`fclose` is skipped on error returns.

**Risk:** File descriptor leaks under error paths (especially `throw -1` — see AP-4).
Can exhaust OS file descriptor limits in long-running JNI processes.

**Remedy (C++98-compatible):**
```cpp
struct FileGuard {
    FILE* fp;
    explicit FileGuard(const char* path, const char* mode) : fp(fopen(path, mode)) {}
    ~FileGuard() { if (fp) fclose(fp); }  // always closes
private:
    FileGuard(const FileGuard&);            // non-copyable (C++98)
};
```

### AP-7: C-Style Casts

**Observed:** `(char*)`, `(int*)`, `(void*)` casts used for type punning and
pointer arithmetic throughout the codebase.

**Risk:** C-style casts silently do the most dangerous thing available —
`reinterpret_cast` if `static_cast` fails. Type punning via pointer cast
violates strict aliasing ([ENG-6.1](laws/engineering/eng-6-security.md)).

**Remedy:** Replace with explicit C++ named casts:
- `static_cast<char*>` — safe numeric/pointer conversions
- `reinterpret_cast<char*>` — explicit byte-level reinterpretation (use `memcpy` for type punning)
- Never `const_cast` — redesign the const-incorrect interface instead

### Anti-Pattern Triage Priority

| Anti-Pattern | Risk Level | Effort | Recommended Phase |
|-------------|-----------|--------|------------------|
| AP-4: `throw int` crossing JNI | 🔴 Critical | Low | Phase 1 — before next release |
| AP-3: Global `extern` vars (concurrency) | 🔴 Critical | High | Phase 1 — JNI re-entrancy risk |
| AP-6: `FILE*` leaks | 🟠 High | Low | Phase 1 — RAII wrapper |
| AP-2: Raw `malloc` | 🟠 High | Medium | Phase 2 — with characterization tests |
| AP-7: C-style casts | 🟠 High | Medium | Phase 2 — static analysis guided |
| AP-1: God class | 🟡 Medium | Very High | Phase 3 — Strangler Fig |
| AP-5: 470-method header | 🟡 Medium | Medium | Phase 2 — build time relief |

---

---
## See Also

- [Safety-Critical C++ & Memory](ref-safety-memory.md)
- [Core Language Patterns](ref-core-language.md)
- [Brownfield Configuration](ref-brownfield-config.md)
- [Migration Playbooks](ref-migration-playbooks.md)


---

## See Also

- [JNI Safety and ABI Governance](ref-safety-jni-abi.md)
