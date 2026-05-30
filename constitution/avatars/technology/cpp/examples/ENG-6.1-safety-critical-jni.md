---
law_id: ENG-6.1
cpp_version_min: 11
avatar: cpp
context: brownfield-jni-solver
---

# [ENG-6.1](laws/engineering/eng-6-security.md): Safety-Critical JNI — C++ Examples

> **Context:** CWR `CrewRecoveryFAR117` enforces FAR Part 117 crew rest/duty limits.
> A crash or silent wrong answer in `libSolver.so` can produce illegal crew pairings.
> C++ exceptions **must not** cross the JNI boundary — they cause undefined behavior in the JVM.

## COMPLIANT: Catch-all barrier with structured error response

```cpp
// runSolver/CrewWatchSolverJNI.cpp
extern "C" {

JNIEXPORT jstring JNICALL
Java_com_aa_lookahead_crewwatchsolver_core_solution_CrewWatchSolverJNI_runSolverJNI(
    JNIEnv* env, jobject /* unused */, jstring input_json)
{
    if (!input_json) {
        return env->NewStringUTF("{\"error\":\"null input — FAR 117 solver aborted\"}");
    }

    const char* raw = env->GetStringUTFChars(input_json, nullptr);
    if (!raw) return nullptr;

    std::string result;
    try {
        result = SolverFacade::run(raw);          // FAR 117 crew rest logic
    } catch (const std::exception& ex) {
        result = std::string("{\"error\":\"") + ex.what() + "\"}";
    } catch (...) {
        result = "{\"error\":\"unknown solver fault — FAR 117 result invalid\"}";
    }

    env->ReleaseStringUTFChars(input_json, raw);

    // Discard any pending Java exception before returning
    if (env->ExceptionCheck()) {
        env->ExceptionClear();
    }
    return env->NewStringUTF(result.c_str());
}

} // extern "C"
```

**Why compliant (per ENG-6.1):**
- `catch (...)` barrier ensures no C++ exception escapes into the JVM
- Null input guard returns a structured error — Java host can detect and log
- `ExceptionClear()` prevents stale JNI exceptions from corrupting subsequent calls
- Error payload includes FAR 117 context so ops teams know result is invalid

---

## NON-COMPLIANT: Exception escapes JNI boundary

```cpp
// BAD — std::runtime_error propagates into JVM → undefined behavior / JVM crash
JNIEXPORT jstring JNICALL
Java_..._runSolverJNI(JNIEnv* env, jobject, jstring input) {
    std::string result = SolverFacade::run(/* ... */);  // may throw
    return env->NewStringUTF(result.c_str());
}
```

---

## Safety-Critical JNI Checklist (FAR 117 context)

| Rule | Check |
|------|-------|
| All JNI entry points have `catch (...)` barrier | ✅ |
| Null input returns structured error, not crash | ✅ |
| `ExceptionClear()` called before return if needed | ✅ |
| Error responses include FAR/domain context string | ✅ |
| No `exit()` / `abort()` inside solver — caller decides | ✅ |

## Edge Cases & Warnings

- **`ExceptionClear()` must precede further JNI calls after a pending exception** — If the JVM has a pending exception and you call `NewStringUTF` without clearing it, the JVM raises `IllegalStateException`. Call `env->ExceptionClear()` before additional JNI operations if a prior call may have left one pending.
- **FAR 117 errors must include regulatory context** — In safety-critical JNI bridges, the structured error response (`{"error": "...", "context": "FAR117"}`) is not optional. A bare `"ERROR"` return bypasses the FAR 117 audit requirement.
- **`catch (...)` must not swallow hardware exceptions on Windows** — On MSVC, `catch (...)` intercepts SEH exceptions (access violations, stack overflows), masking memory corruption. Use `/EHsc` and restrict `catch (...)` to portable exception boundaries in safety-critical JNI bridges.

