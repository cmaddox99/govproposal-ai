---
cpp_version_min: 11
cpp_version_note: >-
  JNI boundary safety; ABI stability patterns available from C++11.
avatar: cpp
---

# C++ Avatar Reference: JNI Safety and ABI Governance

---

> **Governing laws:** [ENG-2.3](laws/engineering/eng-2-architecture.md) (ABI Stability),
> [ENG-6.1](laws/engineering/eng-6-security.md) (Security by Design),
> [ENG-4.1](laws/engineering/eng-4-testing.md) (Atomic TDD — FAR 117 traceability)

---
## JNI Safety and ABI Governance

> **Context:** Applies to any C++ shared library exposed to Java via JNI.
> Canonical reference: CWR `CrewRecoveryFAR117` — `libSolver.so` loaded via
> `System.loadLibrary` from a Java crew-scheduling host (JDK 1.7+).
>
> **Governing laws:** [ENG-2.3](laws/engineering/eng-2-architecture.md) (ABI stability),
> [ENG-6.1](laws/engineering/eng-6-security.md) (security by design)

JNI is a **hard ABI boundary**. Mistakes are silent at compile time but cause
`UnsatisfiedLinkError`, `SIGSEGV`, or silent wrong results at runtime — all
unacceptable in safety-critical crew scheduling.

### Rule 1: Every JNI entry point must use `extern "C"` + `JNIEXPORT` + `JNICALL`

```cpp
// COMPLIANT — symbol visible and unmangled for Java linker
extern "C" {
JNIEXPORT jstring JNICALL
Java_com_aa_lookahead_crewwatchsolver_core_solution_CrewWatchSolverJNI_runSolverJNI(
    JNIEnv* env, jobject /* unused */, jstring input_json)
{
    // ...
}
} // extern "C"
```

- `extern "C"` prevents C++ name mangling — without it, `System.loadLibrary` throws
  `UnsatisfiedLinkError` at runtime with no compile warning
- `JNIEXPORT` controls symbol visibility (required on all platforms)
- `JNICALL` sets the calling convention (critical on Windows, harmless on Linux/macOS)

Verify the symbol is exported: `nm -D libSolver.so | grep runSolverJNI`

### Rule 2: C++ exceptions must NOT cross the JNI boundary

The JVM does not understand C++ exceptions. An uncaught `std::exception` crossing
the JNI boundary causes **undefined behaviour** — typically a JVM crash.

```cpp
// COMPLIANT — catch-all barrier at every entry point
JNIEXPORT jstring JNICALL Java_..._runSolverJNI(JNIEnv* env, jobject, jstring input) {
    try {
        std::string result = SolverFacade::run(raw);
        return env->NewStringUTF(result.c_str());
    } catch (const std::exception& ex) {
        return env->NewStringUTF((std::string("{\"error\":\"") + ex.what() + "\"}").c_str());
    } catch (...) {
        return env->NewStringUTF("{\"error\":\"unknown solver fault\"}");
    }
}

// NON-COMPLIANT — exception escapes into JVM undefined behaviour
JNIEXPORT jstring JNICALL Java_..._runSolverJNI(JNIEnv* env, jobject, jstring input) {
    return env->NewStringUTF(SolverFacade::run(raw).c_str()); // may throw!
}
```

### Rule 3: Always pair `GetStringUTFChars` / `ReleaseStringUTFChars`

```cpp
// COMPLIANT
const char* raw = env->GetStringUTFChars(input_json, nullptr);
if (!raw) return nullptr;                        // OOM guard
std::string result = SolverFacade::run(raw);
env->ReleaseStringUTFChars(input_json, raw);     // paired — no leak
return env->NewStringUTF(result.c_str());

// NON-COMPLIANT — early return leaks raw
const char* raw = env->GetStringUTFChars(input_json, nullptr);
if (validate(raw) != 0) return env->NewStringUTF("ERROR"); // raw never released
env->ReleaseStringUTFChars(input_json, raw);
```

### Rule 4: Clear pending JNI exceptions before returning

```cpp
if (env->ExceptionCheck()) {
    env->ExceptionDescribe();  // logs to stderr for diagnostics
    env->ExceptionClear();     // must ExceptionClear before making further JNI calls
}
```

### ABI Governance Checklist

| Rule | Verification |
|------|-------------|
| `extern "C"` wraps all entry points | `nm -D libSolver.so` — must show unmangled name |
| `JNIEXPORT` + `JNICALL` on every entry | Code review; grep for `JNIEXPORT` |
| `catch (...)` barrier at every entry point | Code review; no uncaught propagation |
| All `GetStringUTFChars` paired with `Release` | Static analysis / ASan |
| `ExceptionClear()` before return when needed | Code review |
| Java package path matches mangled symbol | `javap -s ClassName` vs `nm` output |
| No `exit()` / `abort()` inside solver | grep; caller (Java host) must decide |

---

---


---

## See Also

- [FAR 117 Aviation Safety and CWR](ref-safety-far117-cwr.md)
