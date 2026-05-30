---
cpp_version_min: 11
cpp_version_note: >-
  Sanitizer flags (ASan/UBSan) apply to all C++11+ projects.
avatar: cpp
---

# C++ Avatar Reference: CI Quality Toolchain Policy

---

## CI Quality Toolchain Policy

Per [ENG-5.2](laws/engineering/eng-5-devops.md) (CI/CD Pipeline Law) and the Q4 stakeholder decision, every C++ project must enforce quality gates in CI:

**Mandatory gates (must pass on every PR):**

| Gate | Purpose |
|------|---------|
| Compiler warning flags | `-Wall -Wextra -Wpedantic -Werror`: treat all warnings as errors |
| `clang-tidy` | Static analysis: catches common bugs, style violations, and modernization opportunities |
| AddressSanitizer (ASan) | Detects memory errors: use-after-free, buffer overflows, stack overflows |
| UndefinedBehaviorSanitizer (UBSan) | Detects undefined behavior: integer overflow, null dereference, alignment violations |

**Recommended gates (enabled where practical):**

| Gate | Purpose | Prerequisite |
|------|---------|-------------|
| ThreadSanitizer (TSan) | Detects data races in concurrent code | Cannot run simultaneously with ASan |
| clang static analyzer | Deep path-sensitive analysis | Clang toolchain |
| Mull mutation testing | Validates test effectiveness via mutation score | LLVM/Clang toolchain |
| `llvm-cov` / `gcov` | Code coverage reporting in CI | Compatible compiler |
| CodeQL C/C++ | Security-focused query analysis for PR gating | GitHub Advanced Security |
| Dependabot | Dependency vulnerability scanning | GitHub repository |

**Brownfield exception:** If a repository cannot yet adopt a mandatory gate, document the constraint and define a phased adoption plan with milestones.

### Visual Studio 2022 Built-In Equivalents

Per [ENG-5.2](laws/engineering/eng-5-devops.md), teams using **Visual Studio 2022** as their primary IDE can satisfy the majority of mandatory CI quality gates using tools that ship with Visual Studio — no separate downloads required. This section maps each mandated tool to its VS-native equivalent.

> **When to use this section:** If your team develops C++ in Visual Studio (on Windows, or targeting Windows/Linux via Remote Linux), read this section alongside the standard toolchain requirements. VS-native tools satisfy the constitution's quality gates; you do not need to install standalone clang-tidy or GoogleTest if VS is already configured correctly.

#### Static Analysis: MSVC `/analyze` + C++ Core Check (replaces `clang-tidy`)

Visual Studio ships with two built-in static analyzers that together cover the most important `clang-tidy` checks:

| Built-In Tool | What It Checks | How to Enable |
|---|---|---|
| **MSVC `/analyze`** | Buffer overflows, null dereference, uninitialized memory, integer overflow, use-after-free | Project → Properties → Code Analysis → Enable Code Analysis on Build (check ✅) |
| **C++ Core Check** | Core Guidelines enforcement: resource leaks, raw pointer misuse, type safety, lifetime | Project → Properties → Code Analysis → Ruleset → "C++ Core Check Rules" |
| **Clang-tidy integration** | Full clang-tidy ruleset inside VS IDE | Tools → Options → Text Editor → C/C++ → Code Style → Clang-Tidy; requires LLVM component (selected in VS Installer, no separate download) |

**CI integration:** Enable `/analyze` via the command line for build server runs:

```bat
:: MSBuild with code analysis enabled
msbuild MySolution.sln /p:RunCodeAnalysis=true /p:CodeAnalysisRuleSet=CppCoreCheckRules.ruleset

:: Or with cl.exe directly
cl /analyze /analyze:plugin EspXEngine.dll /W4 /WX your_file.cpp
```

**C++ Core Check ruleset file (`.ruleset`):**

```xml
<!-- CppCoreCheckRules.ruleset — place in solution root -->
<RuleSet Name="C++ Core Check" ToolsVersion="17.0">
  <Rules AnalyzerId="Microsoft.Analyzers.NativeCodeAnalysis" RuleNamespace="Microsoft.Rules.Native">
    <Rule Id="C26400" Action="Warning" />  <!-- raw pointer from new — use make_unique -->
    <Rule Id="C26401" Action="Warning" />  <!-- do not delete a raw pointer owned by smart pointer -->
    <Rule Id="C26402" Action="Warning" />  <!-- return a scoped object instead of a heap-allocated one -->
    <Rule Id="C26408" Action="Warning" />  <!-- avoid malloc/free — use new/delete or make_unique -->
    <Rule Id="C26429" Action="Warning" />  <!-- Symbol was not tested for nullness — use gsl::not_null -->
    <Rule Id="C26481" Action="Warning" />  <!-- don't use pointer arithmetic — use span<> instead -->
    <Rule Id="C26486" Action="Warning" />  <!-- don't pass a pointer that may be invalid to a function -->
  </Rules>
</RuleSet>
```

> **Java developer note:** This is equivalent to running Checkstyle or SpotBugs in your Maven/Gradle build — same concept, different tool. In VS, enabling code analysis in the project properties is analogous to adding the Checkstyle Maven plugin.

#### AddressSanitizer (ASan): Built-In Since VS 2019

MSVC ships AddressSanitizer directly — no separate LLVM toolchain required.

**Enable in project properties:**
- Project → Properties → C/C++ → General → Enable Address Sanitizer: **Yes (`/fsanitize=address`)**

**Or via command line:**

```bat
cl /fsanitize=address /Zi /DEBUG /Od your_file.cpp /link /DEBUG
```

**Or via CMake (works with VS generator):**

```cmake
# CMakeLists.txt — MSVC ASan (VS 2019 16.9+)
if(MSVC AND CMAKE_BUILD_TYPE STREQUAL "Debug")
    target_compile_options(${PROJECT_NAME} PRIVATE /fsanitize=address)
    # Do NOT add /RTC1 or /INCREMENTAL when using ASan
endif()
```

**Behavior:** Identical to GCC/Clang ASan — detects use-after-free, heap buffer overflows, stack buffer overflows, use-after-return. VS integrates ASan output directly into the IDE error list window.

> **Limitation:** `/fsanitize=address` requires x64 or x86 targets. ARM targets on Windows are not yet supported.

#### UBSan Gap — Known Limitation on MSVC

**UndefinedBehaviorSanitizer (UBSan) is not available in MSVC.** This is a known gap. Mitigations:

| MSVC Equivalent Control | What It Catches |
|---|---|
| `/analyze` + `C26451` (arithmetic overflow) | Some integer overflow scenarios |
| `/RTC1` (Runtime Checks) in Debug builds | Stack corruption, uninitialized variables |
| C++ Core Check `C26481`–`C26489` (bounds) | Out-of-bounds pointer arithmetic |
| Manual code review of arithmetic operations | Integer wrapping, sign conversion errors |

**Document as a known gap** in your project's constitution compliance rating under the toolchain section. For MSVC-only projects, use `/analyze` + `/RTC1` as the declared equivalent control, and note that a Clang CI stage should be added to a migration roadmap if full UBSan coverage is needed.

#### Unit Testing: GoogleTest Is Supported Natively in VS

Visual Studio Test Explorer discovers and runs GoogleTest, Catch2, CppUnitTest, and Boost.Test automatically — no adapter installation needed for GoogleTest since VS 2017 15.5.

**Add GoogleTest via vcpkg (VS-integrated package manager):**

```bat
:: In VS Developer Command Prompt — vcpkg ships with VS 2022
vcpkg install gtest:x64-windows
vcpkg integrate install
```

Then add to `CMakeLists.txt`:

```cmake
find_package(GTest CONFIG REQUIRED)
target_link_libraries(my_tests PRIVATE GTest::gtest_main GTest::gmock)
```

Test Explorer automatically discovers all `TEST()` and `TEST_F()` cases — run, debug, and view coverage directly in the IDE.

> **CWR note:** For the CWR repository specifically, adding GoogleTest via vcpkg is the fastest path to Test Explorer integration. No standalone install needed beyond what the VS Installer provides.

#### Code Coverage: Visual Studio Enterprise (or Free Alternative)

| Tool | Availability | How to Use |
|---|---|---|
| **VS Built-In Code Coverage** | Visual Studio Enterprise only | Test → Analyze Code Coverage for All Tests |
| **OpenCppCoverage** | Free, open-source (small install) | `opencppcoverage --sources=src -- mytest.exe`; generates HTML + Cobertura XML |
| **LLVM `llvm-cov`** | Available if LLVM component is installed in VS | `llvm-cov report` after build with `--coverage` flags |

For teams on VS Professional/Community, OpenCppCoverage is the recommended free alternative and generates CI-compatible Cobertura XML output.

#### Memory Leak Detection: CRT Debug Heap (No Install Required)

For debug builds, MSVC's CRT provides built-in leak detection without Valgrind:

```cpp
// Add to main() or a test fixture SetUpTestSuite()
#ifdef _DEBUG
    #define _CRTDBG_MAP_ALLOC
    #include <cstdlib>
    #include <crtdbg.h>
    _CrtSetDbgFlag(_CRTDBG_ALLOC_MEM_DF | _CRTDBG_LEAK_CHECK_DF);
#endif
```

At program exit, any unreleased heap memory is reported to the debug output window with file and line number (if debug info is present).

#### VS 2022 Installer Components — What to Select

When installing or modifying Visual Studio 2022, ensure these optional components are checked to enable the tools above:

| Component | Where | Enables |
|---|---|---|
| **C++ Clang tools for Windows** | Individual Components → Compilers, build tools → | clang-tidy integration, clang-cl compiler |
| **C++ Address Sanitizer** | Individual Components → Compilers, build tools → | `/fsanitize=address` support |
| **vcpkg package manager** | Individual Components → Code tools → | GoogleTest, Catch2 via vcpkg |
| **C++ CMake tools for Windows** | Desktop development with C++ workload | Open-folder CMake support |
| **C++ core desktop features** | Desktop development with C++ workload (default) | MSVC `/analyze`, C++ Core Check |

> **All of the above ship with Visual Studio 2022** — either in the default "Desktop development with C++" workload or as selectable components in the VS Installer. No third-party downloads required.

#### VS Built-In vs. Standard Toolchain — Compliance Matrix

| Constitution Requirement | Standard Tool | VS 2022 Built-In Equivalent | Compliance Status |
|---|---|---|---|
| Static analysis (mandatory) | `clang-tidy` | MSVC `/analyze` + C++ Core Check; or VS clang-tidy integration | ✅ Satisfies requirement |
| AddressSanitizer (mandatory) | `asan` (GCC/Clang) | `/fsanitize=address` (VS 2019 16.9+) | ✅ Satisfies requirement |
| UndefinedBehaviorSanitizer (mandatory) | `ubsan` (GCC/Clang) | `/RTC1` + `/analyze` (partial coverage) | ⚠️ Partial — document gap |
| Unit testing | GoogleTest | VS Test Explorer + GoogleTest via vcpkg | ✅ Satisfies requirement |
| Code coverage | `llvm-cov` / `gcov` | VS Enterprise coverage or OpenCppCoverage | ✅ Satisfies requirement (OpenCppCoverage free) |
| Memory leak detection | Valgrind / ASan | CRT Debug Heap + `/fsanitize=address` | ✅ Satisfies requirement |
| Build system | CMake | VS-native CMake (open folder or solution) | ✅ Satisfies requirement |

**For the UBSan gap:** Add the following to your project's constitution compliance notes:

```markdown

---


---


---

## See Also

- [GoogleTest Core Patterns](ref-testing-gtest-core.md)
- [GoogleTest Advanced Patterns](ref-testing-gtest-advanced.md)
