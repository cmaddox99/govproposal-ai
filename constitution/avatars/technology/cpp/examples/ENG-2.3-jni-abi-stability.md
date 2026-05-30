---
law_id: ENG-2.3
cpp_version_min: 11
avatar: cpp
context: brownfield-jni-solver
---

# [ENG-2.3](laws/engineering/eng-2-architecture.md): JNI ABI Stability — C++ Examples

> **Context:** CWR `CrewRecoveryFAR117` exposes `libSolver.so` to Java via JNI.
> ABI stability is safety-critical: a broken signature silently returns null to the Java host.

## COMPLIANT: Stable JNI Entry Point with Explicit Types

```cpp
// runSolver/CrewWatchSolverJNI.cpp
#include <jni.h>
#include "Solver/SolverFacade.h"

extern "C" {

JNIEXPORT jstring JNICALL
Java_com_aa_lookahead_crewwatchsolver_core_solution_CrewWatchSolverJNI_runSolverJNI(
    JNIEnv* env,
    jobject /* unused */,
    jstring input_json)
{
    const char* raw = env->GetStringUTFChars(input_json, nullptr);
    if (!raw) return nullptr;                   // OOM guard

    std::string result = SolverFacade::run(raw);
    env->ReleaseStringUTFChars(input_json, raw); // release before return

    return env->NewStringUTF(result.c_str());
}

} // extern "C"
```

**Why compliant:**
- `extern "C"` prevents C++ name mangling — Java `System.loadLibrary` can resolve the symbol
- `JNIEXPORT` / `JNICALL` ensure correct visibility and calling convention on all platforms
- Explicit `GetStringUTFChars` / `ReleaseStringUTFChars` pairing prevents memory leak
- Null guard on `raw` prevents crash on JVM OOM

---

## NON-COMPLIANT: Missing `extern "C"` — silent link failure

```cpp
// BAD — C++ mangling breaks Java symbol lookup at runtime
JNIEXPORT jstring JNICALL
Java_com_aa_lookahead_crewwatchsolver_core_solution_CrewWatchSolverJNI_runSolverJNI(
    JNIEnv* env, jobject obj, jstring input)
{
    // UnsatisfiedLinkError thrown in Java at runtime — no compile warning
}
```

---

## NON-COMPLIANT: Leaking JNI local reference

```cpp
// BAD — GetStringUTFChars not released on early return
const char* raw = env->GetStringUTFChars(input_json, nullptr);
if (validate(raw) != 0) {
    return env->NewStringUTF("ERROR");  // raw is never released
}
env->ReleaseStringUTFChars(input_json, raw);
```

**Fix:** Always pair in RAII wrapper or release before every return path.

---

## ABI Stability Checklist (per ENG-2.3)

| Rule | Check |
|------|-------|
| `extern "C"` wraps all JNI functions | ✅ |
| `JNIEXPORT` + `JNICALL` on every entry point | ✅ |
| JNI string/array refs released on all paths | ✅ |
| No C++ exceptions crossing JNI boundary | ✅ — catch and convert to `jstring` error |
| Java package path matches mangled symbol | ✅ — verify with `javap -s` or `nm libSolver.so` |

## Edge Cases & Warnings

- **Renaming a Java class breaks JNI symbol mangling** — JNI names encode the full Java package path (`Java_com_aa_cwr_Solver_runSolverJNI`). Moving the Java class silently breaks native lookup at runtime. Verify with `javap -s` + `nm libSolver.so` after any Java-side rename.
- **JDK upgrade can change `jstring` encoding** — The CWR system targets JDK 1.7. Upgrading the JVM may change `GetStringUTFChars` behavior for supplementary Unicode code points. Pin JDK version in CI and test UTF-8 round-trips explicitly.
- **Missing `JNIEXPORT` is invisible at compile time** — On Windows/MSVC, an omitted `JNIEXPORT` hides the symbol from `LoadLibrary`. The Java side throws `UnsatisfiedLinkError` only at runtime. Verify every new entry point against the ABI checklist.
