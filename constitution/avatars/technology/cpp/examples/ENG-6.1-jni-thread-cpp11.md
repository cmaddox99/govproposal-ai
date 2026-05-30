---
law_id: ENG-6.1
cpp_version_min: 11
cpp_version_note: >-
  C++11 JNI thread safety using thread_local RAII. Supersedes the
  pthread_key_t pattern in ENG-6.1-jni-thread-cpp98.md for C++11+ teams.
avatar: cpp
rag_exclude: true  # placeholder — content pending CBF adoption; excluded from RAG routing
---

# [ENG-6.1](laws/engineering/eng-6-security.md): JNI Thread Safety — C++11 (thread_local RAII)

**Avatar:** C++ (Transitional C++11/14 — CWR / IOC_ALP)
**Pattern:** Per-thread JVM attachment via `thread_local` RAII guard

## Context

`JNIEnv*` is thread-local by JVM contract. For C++11+ codebases, `thread_local`
RAII is simpler than the `pthread_key_t` approach in
[ENG-6.1-jni-thread-cpp98.md](ENG-6.1-jni-thread-cpp98.md) — the compiler
handles the per-thread lifetime automatically.

**Important caveat:** The C++11 standard does not specify the ordering between
`thread_local` destructors and JVM shutdown. On Android NDK and some host JVMs,
the JVM may have already detached the thread by the time the `thread_local`
destructor fires. The pattern below guards against this with a `GetEnv` check
before calling `DetachCurrentThread`.

Attribution: pattern derived from
[android/ndk-samples](https://github.com/android/ndk-samples),
Apache 2.0, Android Open Source Project.

## COMPLIANT — thread_local RAII Guard

```cpp
// jni_thread_cpp11.cpp  — C++11, cross-platform
#include <jni.h>

static JavaVM* g_jvm = nullptr;  // set once in JNI_OnLoad — safe

// RAII guard: attaches on first use, detaches on thread exit.
struct JniEnvGuard {
    JNIEnv* env = nullptr;
    bool    attached = false;

    JniEnvGuard()
    {
        jint rc = g_jvm->GetEnv(reinterpret_cast<void**>(&env), JNI_VERSION_1_6);
        if (rc == JNI_EDETACHED) {
            // Thread not yet attached — attach now.
            rc = g_jvm->AttachCurrentThread(&env, nullptr);
            attached = (rc == JNI_OK);
        }
        // rc == JNI_OK means already attached on this thread — use env as-is.
    }

    ~JniEnvGuard()
    {
        if (!attached) return;  // we did not attach — do not detach
        // Guard against JVM already gone (e.g., during process shutdown).
        JNIEnv* check = nullptr;
        jint rc = g_jvm->GetEnv(reinterpret_cast<void**>(&check), JNI_VERSION_1_6);
        if (rc != JNI_EDETACHED) {
            g_jvm->DetachCurrentThread();
        }
    }

    // Non-copyable — each thread owns its own guard.
    JniEnvGuard(const JniEnvGuard&) = delete;
    JniEnvGuard& operator=(const JniEnvGuard&) = delete;
};

// One guard per thread; destructor fires when the thread exits.
thread_local JniEnvGuard tl_jni_guard;

// Returns the calling thread's JNIEnv*.
// First call on a thread attaches; subsequent calls reuse the attached env.
JNIEnv* get_jni_env()
{
    return tl_jni_guard.env;
}

jint JNI_OnLoad(JavaVM* vm, void* /*reserved*/)
{
    g_jvm = vm;
    return JNI_VERSION_1_6;
}
```

**Why this is safe:** `thread_local JniEnvGuard` is constructed the first time
`tl_jni_guard` is accessed on a given thread. Its destructor is called when
that thread exits. The `attached` flag ensures we only call `DetachCurrentThread`
if we called `AttachCurrentThread` — threads that were already attached (e.g.,
the main JVM thread) are left alone.

## COMPLIANT — GetEnv / AttachCurrentThread per call (no caching)

For short-lived helper functions where storing a guard is inconvenient:

```cpp
// Obtain a fresh JNIEnv* for the current call only.
// Safe to call from any thread at any time.
JNIEnv* get_env_for_call(bool* did_attach_out)
{
    JNIEnv* env = nullptr;
    *did_attach_out = false;
    jint rc = g_jvm->GetEnv(reinterpret_cast<void**>(&env), JNI_VERSION_1_6);
    if (rc == JNI_EDETACHED) {
        g_jvm->AttachCurrentThread(&env, nullptr);
        *did_attach_out = true;
    }
    return env;
}

void call_java_method()
{
    bool did_attach = false;
    JNIEnv* env = get_env_for_call(&did_attach);
    env->CallVoidMethod(/* ... */);
    if (did_attach) g_jvm->DetachCurrentThread();
}
```

## NON-COMPLIANT

```cpp
// WRONG: static global JNIEnv* — shared across threads.
// JNIEnv* is valid only on the thread that attached it.
// Using it on any other thread is undefined behavior.
static JNIEnv* g_env = nullptr;  // ← kills the JVM on first cross-thread use

void init_jni(JavaVM* vm)
{
    vm->AttachCurrentThread(&g_env, nullptr);
}

void worker_thread_func()
{
    // g_env was attached to a different thread — immediate JVM crash or
    // silent memory corruption.
    g_env->CallVoidMethod(/* ... */);
}
```

## Supersedes

This pattern supersedes the `pthread_key_t` approach for C++11+ codebases:
- `thread_local` is part of the C++11 standard — no POSIX/Win32 ifdefs needed.
- Destructor is compiler-managed — no manual `pthread_key_create` / `TlsAlloc`.
- For C++98 codebases still on MSVC 2005–2010, see
  [ENG-6.1-jni-thread-cpp98.md](ENG-6.1-jni-thread-cpp98.md).

## Edge Cases & Warnings

- **`thread_local` destructor ordering with JVM shutdown:** The C++11 standard
  does not guarantee that `thread_local` destructors fire before JVM teardown.
  On Android NDK the JVM typically detaches threads before calling
  `thread_local` destructors. The `GetEnv` check in `~JniEnvGuard` handles this:
  if `GetEnv` returns `JNI_EDETACHED`, the JVM has already cleaned up — skip
  `DetachCurrentThread`.

- **`attached` flag semantics:** Only detach if *we* attached. A thread that
  was already attached before the first `get_jni_env()` call (e.g., threads
  created by the JVM itself) must not be detached by our destructor — that
  would corrupt the JVM thread state.

- **Worker-pool threads (Android AsyncTask, custom pools):** `thread_local`
  variables live for the thread lifetime, not the task lifetime. The guard
  attaches on the thread's first use and detaches only when the thread
  terminates. Do not call `DetachCurrentThread` between tasks — it will break
  subsequent calls on the same pooled thread.

- **`AttachCurrentThread` on already-attached thread:** Returns the existing
  `JNIEnv*` and is safe. The `GetEnv` pre-check avoids the redundant call and
  correctly sets `attached = false` so we do not issue a spurious detach.

- **MSVC 2013 and earlier:** `thread_local` was not fully supported until
  MSVC 2015. For MSVC 2013, use `__declspec(thread)` with care — it does not
  call destructors for non-trivial types in DLLs loaded with `LoadLibrary`.
  For those compilers, fall back to the `pthread_key_t` / `TlsAlloc` pattern
  in [ENG-6.1-jni-thread-cpp98.md](ENG-6.1-jni-thread-cpp98.md).

Per [ENG-6.1](laws/engineering/eng-6-security.md): every native thread
interacting with the JVM must obtain a thread-local `JNIEnv*` and ensure
`DetachCurrentThread` is called on exit. `thread_local` RAII is the
preferred C++11 mechanism.
