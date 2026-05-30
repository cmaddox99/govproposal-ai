---
law_id: ENG-6.1
cpp_version_min: 98
cpp_version_note: >-
  C++98-safe JNI thread attachment using pthread_key_t (POSIX) or
  TlsAlloc (Win32). For C++11+ teams, thread_local RAII is simpler —
  see ENG-6.1-jni-thread-cpp11.md.
avatar: cpp
---

# [ENG-6.1](laws/engineering/eng-6-security.md): JNI Thread Safety — C++98 (pthread_key_t / TlsAlloc)

**Avatar:** C++ (Legacy C++98 — brownfield MSVC/NDK)
**Pattern:** Per-thread JVM attachment using platform TLS destructor

## Context

`JNIEnv*` is thread-local by JVM contract. Every native thread that calls
Java must obtain its own `JNIEnv*` via `AttachCurrentThread`, and must call
`DetachCurrentThread` before the thread exits — otherwise the JVM leaks the
thread peer and hangs on shutdown.

For C++98 codebases that cannot use `thread_local` (C++11), the only portable
mechanism is platform thread-local storage with a destructor callback:
POSIX `pthread_key_t` or Win32 `TlsAlloc` + `DllMain`.

Attribution: pattern derived from
[android/ndk-samples](https://github.com/android/ndk-samples),
Apache 2.0, Android Open Source Project.

## COMPLIANT — POSIX (pthread_key_t)

```cpp
// jni_thread_posix.cpp  — C++98, POSIX (Linux/Android/macOS NDK)
#include <jni.h>
#include <pthread.h>

static JavaVM*    g_jvm     = NULL;  // set once in JNI_OnLoad — safe
static pthread_key_t g_tls_key;     // per-thread JNIEnv* storage

// Destructor called by pthreads when a thread exits.
// Detaches the thread from the JVM so the JVM can reclaim the peer.
static void detach_jni_env(void* env_ptr)
{
    if (env_ptr != NULL) {
        g_jvm->DetachCurrentThread();
    }
}

jint JNI_OnLoad(JavaVM* vm, void* /*reserved*/)
{
    g_jvm = vm;
    pthread_key_create(&g_tls_key, detach_jni_env);  // register destructor
    return JNI_VERSION_1_6;
}

// Returns a valid JNIEnv* for the calling thread.
// Attaches on first call; destructor auto-detaches on thread exit.
JNIEnv* get_jni_env()
{
    JNIEnv* env = static_cast<JNIEnv*>(pthread_getspecific(g_tls_key));
    if (env == NULL) {
        g_jvm->AttachCurrentThread(&env, NULL);
        pthread_setspecific(g_tls_key, env);  // arm the destructor
    }
    return env;
}
```

**Why this is safe:** `pthread_key_create` registers `detach_jni_env` as the
destructor. When any thread that called `get_jni_env()` exits, pthreads calls
`detach_jni_env(env)` automatically — the JVM thread peer is always cleaned up
regardless of how the thread exits.

## COMPLIANT — Win32 (DllMain DLL_THREAD_DETACH)

```cpp
// jni_thread_win32.cpp  — C++98, Win32 (MSVC / Windows NDK host)
#include <jni.h>
#include <windows.h>

static JavaVM* g_jvm  = NULL;
static DWORD   g_tls  = TLS_OUT_OF_INDEXES;

BOOL WINAPI DllMain(HINSTANCE, DWORD reason, LPVOID)
{
    switch (reason) {
    case DLL_PROCESS_ATTACH:
        g_tls = TlsAlloc();
        break;
    case DLL_THREAD_DETACH:
        // Called by Windows for every thread that loaded this DLL and exits.
        if (g_jvm != NULL && TlsGetValue(g_tls) != NULL) {
            g_jvm->DetachCurrentThread();
            TlsSetValue(g_tls, NULL);
        }
        break;
    case DLL_PROCESS_DETACH:
        if (g_tls != TLS_OUT_OF_INDEXES) TlsFree(g_tls);
        break;
    }
    return TRUE;
}

JNIEnv* get_jni_env()
{
    JNIEnv* env = static_cast<JNIEnv*>(TlsGetValue(g_tls));
    if (env == NULL) {
        g_jvm->AttachCurrentThread(reinterpret_cast<void**>(&env), NULL);
        TlsSetValue(g_tls, env);
    }
    return env;
}
```

**Why this is safe:** Windows calls `DLL_THREAD_DETACH` for every thread that
exits while the DLL is loaded. `DetachCurrentThread` is guaranteed to run even
if the thread exits abnormally.

## NON-COMPLIANT

```cpp
// WRONG 1: static global JNIEnv* — shared across threads
// JNIEnv* is valid only on the thread that attached it (JVM ABI contract).
// Using it on any other thread is undefined behavior — typically a JVM crash.
static JNIEnv* g_env = NULL;  // ← thread-local value stored globally

void init_jni(JavaVM* vm)
{
    vm->AttachCurrentThread(&g_env, NULL);  // attached on THIS thread only
}

void some_other_thread_func()
{
    g_env->CallVoidMethod(...);  // UB: g_env was attached to a different thread
}

// WRONG 2: atomic<JNIEnv*> does not fix the thread-locality problem.
// The issue is not data-race visibility — it is JVM thread-affinity.
// An atomic store/load still delivers a JNIEnv* owned by another thread.
#include <atomic>
static std::atomic<JNIEnv*> g_atomic_env;  // ← wrong tool for wrong reason

void init_jni_atomic(JavaVM* vm)
{
    JNIEnv* env = NULL;
    vm->AttachCurrentThread(&env, NULL);
    g_atomic_env.store(env);   // visible to all threads — still UB to USE it
}
```

**Why these are wrong:** `JNIEnv*` encodes the thread's JNI interface table.
The JVM verifies on every call that the calling thread matches the attached
thread. Sharing `JNIEnv*` across threads causes an immediate JVM abort or
silent memory corruption.

## C++11 Upgrade Path

If your codebase has moved to C++11, replace this pattern with the simpler
`thread_local` RAII guard described in
[ENG-6.1-jni-thread-cpp11.md](ENG-6.1-jni-thread-cpp11.md).
The `thread_local` destructor eliminates the manual TLS key management.

## Edge Cases & Warnings

- **`AttachCurrentThread` on an already-attached thread:** Safe — returns
  the existing `JNIEnv*`. The matching `DetachCurrentThread` call decrements
  a reference count; only the final detach actually detaches.

- **Thread exits before `get_jni_env()` is called:** The destructor/
  `DLL_THREAD_DETACH` fires with a NULL slot — both patterns guard for NULL,
  so no spurious detach occurs.

- **`DLL_THREAD_DETACH` on threads that never called `GetJniEnv`:** Windows
  calls `DLL_THREAD_DETACH` for ALL threads, including those that never
  attached to the JVM. The `TlsGetValue(g_tls) != NULL` guard prevents a
  spurious `DetachCurrentThread`.

- **Worker pool threads recycled by the runtime:** If threads are pooled
  (Android `AsyncTask`, custom threadpools), `pthread_key_t` destructors
  fire on thread-exit — not on task-completion. The JVM attachment is
  per-thread, not per-task. Each pooled thread attaches once and detaches
  only when the thread terminates. This is correct; do not detach between
  tasks.

- **`JNI_OnLoad` timing on Win32:** `DllMain` with `DLL_PROCESS_ATTACH`
  runs under the loader lock. Keep it minimal — `TlsAlloc` is safe;
  `AttachCurrentThread` inside `DllMain` is not (risks deadlock).

Per [ENG-6.1](laws/engineering/eng-6-security.md): every native thread that
interacts with the JVM must obtain a thread-local `JNIEnv*` and register an
exit destructor. Sharing `JNIEnv*` across threads is undefined behavior.
