---
id: KI-012
title: "Vendored binary SDKs force __llvm_profile_raw_version = 8, blocking coverage on Xcode 26.4.1"
severity: critical
avatar: ios-build-infrastructure
discovered: 2026-05-08
law: ENG-4.2
---

## Symptom

After successfully running tests (14 tests pass), `llvm-profdata merge` warns:

```
warning: *.profraw: raw profile version mismatch: Profile uses raw
profile format version = 8; expected version = 10
```

`xcrun xccov view --report` fails with "Failed to load coverage archive".
`xcrun llvm-cov report` produces 0.00% for all sources.

## Root Cause

Two vendored binary SDKs define `___llvm_profile_raw_version` at the old v8 value:

| Binary | Symbol type | Source |
|--------|-------------|--------|
| `AmericanTestCore.framework` | `d` (local data) | testcore-ios Carthage checkout |
| `ASAPPSDK.framework` | `D` (global data) | chat-ios Carthage checkout |

When these frameworks are loaded in the test host process, their v8 version value
can win the dynamic symbol resolution race against the debug.dylib's v10 definition.
The result: the entire process writes a v8-format profraw.

`llvm-profdata merge --failure-mode=warn` (Xcode 26.4.1 / LLVM 19) produces a
6.1MB profdata output BUT with all function counters zeroed, because it cannot
interpret v8 counter encoding. The profdata is structurally valid but valueless.

Verified: `llvm-profdata show --all-functions` on the raw profraw shows **1,540 of
20,551 functions executed** — the data IS there in the raw file, but the merge
tool cannot convert it.

## What This Means

- Line coverage cannot be obtained on this codebase with the current toolchain
- `xccov view --report` will always fail (coverage archive not created)
- `llvm-cov` will always report 0.00%
- CI coverage measurement is likely also broken unless the CI image:
  - Excludes AmericanTestCore and ASAPPSDK from the test build, OR
  - Uses a pre-baked profdata from a previous clean build

## Confirmation Method

```bash
nm Carthage/Build/AmericanTestCore.xcframework/ios-arm64_x86_64-simulator/\
   AmericanTestCore.framework/AmericanTestCore | grep profile_raw_version
# → 00000000000449d8 d ___llvm_profile_raw_version

nm Carthage/Build/ASAPPSDK.xcframework/.../ASAPPSDK.framework/ASAPPSDK \
   | grep profile_raw_version
# → 00000000003e9948 D ___llvm_profile_raw_version
```

## Fix

**Option 1 (preferred):** Rebuild both SDKs from source with Xcode 26.4.1.
`AmericanTestCore` is a local Carthage checkout (testcore-ios) — buildable.
`ASAPPSDK` may be binary-only — contact ASAPP for updated xcframework.

**Option 2 (workaround):** Strip coverage instrumentation from vendored SDKs
before linking. Use `EXCLUDED_SOURCE_FILE_NAMES` or an xcconfig to exclude
these frameworks from the coverage-instrumented build.

**Option 3 (workaround):** Post-build: delete profraw files written by old
binaries before Xcode's profdata merge step runs. Requires Xcode build phase hook.

## Impact on Stage C

Coverage for `americanmobileapp-ios` remains **Unknown/Blocked** until one of the
above fixes is applied. The test infrastructure (14 of 66 test classes run successfully)
confirms the test suite CAN run — the blocker is coverage measurement only.

Function coverage proxy (from raw profraw): **7.5%** (1,540 / 20,551 functions
executed across all instrumented code). App-source-only function coverage cannot
be isolated without additional tooling due to file path stripping in profraw format.
