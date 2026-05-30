---
skill:
  id: skill-cpp-jni-bridge
  name: "C++ JNI Bridge Governance"
  category: platform-engineering
  version: "1.0.0"
  avatar: cpp

laws:
  implements:
    - id: ENG-6.1
      title: Security by Design Law (NON-NEGOTIABLE)
  references:
    - id: ENG-3.1
      title: Complexity Limits Law
    - id: ENG-6.7
      title: Audit Trail Law

triggers:
  phrases:
    - "JNI bridge"
    - "C++ JNI"
    - "Java Native Interface"
    - "jni.h"
    - "CWR JNI"
    - "C++ Java interop"
    - "JNI memory ownership"
    - "JNI exception propagation"

followed_by:
  - skill-cpp-ownership-lifetime-safety
  - skill-cpp-exception-safety-governance
---

# Skill: C++ JNI Bridge Governance

## Purpose

Enforce safe, correct JNI boundaries between C++ domain code and the Java scheduling
layer in CWR. Per [ENG-6.1](laws/engineering/eng-6-security.md), JNI boundaries are
integration boundaries — exceptions must not propagate across them, and memory ownership
must be explicit and release-safe.

## Procedure

1. **Map JNI types explicitly** — never use implicit conversions; maintain a type-map table
2. **Convert exceptions at the boundary** — catch all C++ exceptions in JNI functions; translate to Java exceptions with `env->ThrowNew()`
3. **Release local refs** — call `env->DeleteLocalRef()` for every local ref created in the JNI function; prefer `try/finally` patterns via RAII wrappers
4. **Audit JNI entry points** — per [ENG-6.7](laws/engineering/eng-6-security.md), log every JNI call that mutates shared state
5. **Test JNI boundary in isolation** — write a GoogleTest that exercises the JNI entry point directly without the Java layer

## Governance Gate

Per [ENG-6.1](laws/engineering/eng-6-security.md), a JNI function that:
- lets a C++ exception propagate across the boundary → **BLOCKING violation**
- leaks a JNI local reference → **BLOCKING violation**
- performs unprotected mutation of shared state without logging → **HIGH violation**

## C++ Specific Patterns

### Type Mapping Table (CWR convention)

| Java type | JNI type | C++ type | Notes |
|-----------|----------|----------|-------|
| `long` | `jlong` | `int64_t` | Use for IDs (FlightId, CrewId) |
| `String` | `jstring` | `std::string` | Convert via `GetStringUTFChars` + `ReleaseStringUTFChars` |
| `int[]` | `jintArray` | `std::vector<int32_t>` | Copy via `GetIntArrayElements` + `ReleaseIntArrayElements` |
| `byte[]` | `jbyteArray` | `std::vector<uint8_t>` | For binary payloads |

### Exception Boundary Pattern

```cpp
// Every JNI function MUST have this pattern:
extern "C" JNIEXPORT jlong JNICALL
Java_com_aa_cwr_CrewScheduler_assignCrew(JNIEnv* env, jobject, jlong flightId, jlong crewId) {
    try {
        CrewError err = scheduler().assign_crew(FlightId{flightId}, CrewId{crewId});
        return static_cast<jlong>(err);
    } catch (const std::exception& e) {
        env->ThrowNew(env->FindClass("java/lang/RuntimeException"), e.what());
        return -1L;
    } catch (...) {
        env->ThrowNew(env->FindClass("java/lang/RuntimeException"), "Unknown C++ error");
        return -1L;
    }
}
```

### RAII Local Ref Guard

```cpp
class JniLocalRef {
    JNIEnv* env_;
    jobject ref_;
public:
    JniLocalRef(JNIEnv* env, jobject ref) : env_(env), ref_(ref) {}
    ~JniLocalRef() { if (ref_) env_->DeleteLocalRef(ref_); }
    jobject get() const { return ref_; }
    JniLocalRef(const JniLocalRef&) = delete;
};
```

## CWR Brownfield Path

CWR uses C++03 in the solver core but JNI bridges to a Java layer:
1. All JNI functions are in a thin `jni/` directory — no domain logic in JNI layer
2. C++03 compatible: no `auto`, no lambdas — use explicit types
3. All JNI functions must compile with `-std=c++03` until the solver migrates
