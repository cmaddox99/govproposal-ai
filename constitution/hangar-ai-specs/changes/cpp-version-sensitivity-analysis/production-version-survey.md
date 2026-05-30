# Production C++ Version Survey
## Tier 1.1 — Which C++ Standard Is In Production?

**Purpose:** Panel Tier 1 required a factual baseline of which C++ standards are
actually deployed across AA's active C++ repositories before designing the Option E
version-routing scheme.

**Method:** Evidence gathered from:
- GitHub Actions workflow files (`.github/workflows/`)
- Visual Studio project files (`.vcxproj`, `.dsp`, `.dsw`, `.sln`)
- CMakeLists.txt and Makefile compiler flags
- Source file patterns (`.mm` = Objective-C++, `#include <vcl\vcl.h>` = Borland VCL)
- Committed runtime DLLs (`msvcp60.dll` = MSVC 6.0 C-runtime)
- Build tool versions (VS toolset v140–v143, GCC on Ubuntu 22.04)

---

## Survey Results

| Repo | Est. LOC | C++ Standard | Confidence | Category |
|------|----------|-------------|-----------|---------|
| IOC_ALP | ~222,000 | **C++14** (MSVC default) | ⚠️ Inferred | Windows/MSVC |
| SPEClient | ~177,000 | **Pre-C++98 (MSVC 6.0)** | ✅ High | Windows/MSVC 6 |
| hte_pm_hostconn | ~152,000 | **C++14** (MSVC default) | ⚠️ Inferred | Windows/MSVC |
| herc-odyssey-linux | ~80,600 | **C++98/03** | ⚠️ Inferred | Linux/GCC |
| CWR | ~73,700 | **C++14** (no C++14 features) | ✅ Confirmed | Windows/MSVC |
| supportATIS | ~33,600 | **Borland VCL (non-ISO)** | ✅ Confirmed | Borland/RAD Studio |
| IOC_ScreenPrinter | ~32,600 | **C++17** (explicit) | ✅ Confirmed | Windows/MSVC |
| memtier-benchmarking | ~12,800 | **C++11/14** (GCC 11) | ⚠️ Inferred | Linux/Docker |
| mobileFOS2_iOS | ~6,300 | **Objective-C++** (non-ISO) | ✅ Confirmed | iOS/Xcode |
| IOC_FosQuery2 | ~2,100 | **C++14** (MSVC default, archived) | ⚠️ Inferred | Windows/MSVC |
| app-mgmt-killapp | ~275 | **C++17** (explicit, CppWinRT) | ✅ Confirmed | Windows/MSVC |

---

## Per-Repository Evidence

### IOC_ALP (~222k LOC) — C++14 inferred
- **Build:** `msbuild ALPGUI.sln /p:Configuration=Release` (CIbuild.yml, CICD.yml)
- **Runner:** Custom runner `PCALP`, `windows-latest`
- **CMakeLists.txt:** `cmake_minimum_required(VERSION 3.16)`, MFC enabled — no `CMAKE_CXX_STANDARD` set
- **Coverity build:** `msbuild ALPGUI.sln /p:Configuration=Release` — no `/std:c++XX` flag
- **No `.vcxproj` standard tag found** in initial root scan
- **Verdict:** MSVC MSBuild with no explicit C++ standard = **C++14 default** for any v141/v142/v143 toolset
- **Risk:** If PlatformToolset is v140 or earlier, this could be C++11 or pre-11 default

### SPEClient (~177k LOC) — Pre-C++98 / MSVC 6.0  ⚠️ CRITICAL
- **Project files:** `SPECLIENT.dsp`, `SPEClient.dsw` — Visual Studio 6.0 Developer Studio format (1998)
- **Version control artifact:** `mssccprj.scc`, `vssver.scc` — Visual SourceSafe integration files
- **Committed runtime DLL:** `msvcp60.dll` — MSVC 6.0 C++ standard library runtime (definitive proof)
- **Other VS6 artifacts:** `SPECLIENT.ncb` (project browser DB), `SPECLIENT.opt` (user options)
- **No CI:** No `.github/workflows/` directory — zero automated builds in GitHub Actions
- **Source characteristics:** Multiple saved backup copies of main file (`SPECLIENTold.cpp`,
  `SPECLIENT for CorpAA reg key fix.cpp`, `SPEClient v921.cpp`) — manual version control
- **Verdict:** **Visual C++ 6.0 (ca. 1998)** — predates even the C++98 standard ratification.
  MSVC 6.0 has non-conformant template implementation, non-standard STL, and many
  ISO C++98 deviations. This is the most critical legacy finding in the portfolio.
- **Note on LOC (~177k):** This appears to be the second-largest C++ codebase and has
  ZERO CI, ZERO GitHub Actions, and ZERO automated quality gates.

### hte_pm_hostconn (~152k LOC) — C++14 inferred (VS2019)
- **Build:** `msbuild '...MasterBuild.sln'` via Coverity action
- **VS version:** `vs-version: '16.0'` in `setup-msbuild@v1` step — **Visual Studio 2019**
- **Default standard for VS2019:** C++14 (no `/std:c++17` flag observed)
- **Project name:** "VG-Host Terminal Emulator" — an emulator project; terminal emulator
  code tends to be older idioms even when compiled with a newer toolset
- **Sonar language:** `javafs` in Coverity action (unusual — suggests mixed Java/C++ codebase
  or incorrect configuration)
- **Verdict:** **C++14** by VS2019 default, but architectural patterns likely older (C++03 style)
- **Caveat:** Without vcxproj inspection, can't rule out a `<LanguageStandard>` element
  forcing a specific standard in some configurations

### herc-odyssey-linux (~80.6k LOC) — C++98/03  ⚠️ HIGH CONCERN
- **Build system:** Raw `make` with `CC = g++` in `airmax/multi_make_CC`
- **Compiler flags:** `LINUXFLAGS` contains only include paths and `-fPIC` — **no `-std=` flag at all**
- **Architecture:** Orbix 6.1 CORBA middleware (ca. 2001), Oracle Pro*C embedded SQL
- **Oracle connection:** `od_app/Ody_2014test@herctst` — test credentials in Makefile
- **Database:** Oracle 19.10 (modern), but code patterns are ODYM 5.1 (very old Oracle middleware)
- **CI status:** `codeql.yml` has C/C++ build **commented out** with note:
  `# C/Cpp builds are failing - re-enable once workflow build is fixed`
  — the CI cannot build this code; only Java/Python are scanned
- **Verdict:** **C++98/03 codebase** compiled with whatever GCC default the Linux host provides.
  No `-std=` flag means compiler-default, which on an old RHEL/CentOS system would be
  C++98. CI is broken for C++ — no automated build verification.
- **Critical concern:** The CI cannot build this code. There is no compiler-enforced
  standard check. Code may silently use GCC extensions or pre-standard patterns.

### CWR (~73.7k LOC) — C++14 (no C++14 features used yet)  ← PRIMARY FOCUS REPO
- **Status:** User confirmed — recently migrated from C++03 to C++14 compiler
- **Feature usage:** No C++14 language features are being used yet (zero delta migration)
- **Significance:** This is the primary consumer project for the constitution; the
  "brownfield C++14 that acts like C++03" scenario is the highest-priority use case
- **Verdict:** **C++14 toolset, C++03 idiom usage** — prime candidate for gradual modernization

### supportATIS (~33.6k LOC) — Borland VCL (Non-ISO C++)  ⚠️ DIFFERENT ECOSYSTEM
- **Framework:** VCL (Visual Component Library) — Embarcadero/Borland RAD Studio
- **Evidence:** `#include <vcl\vcl.h>`, `TForm`, `__fastcall` calling convention
- **Build tool:** Embarcadero RAD Studio (not MSVC, not GCC)
- **No CI:** No `.github/workflows/` directory
- **Language characteristics:** Borland C++ Builder extensions include `__closure`,
  `__fastcall`, `__published`, `_TCHAR`, `AnsiString`, `WideString` — non-standard
- **Verdict:** **Borland/Embarcadero C++ Builder** — outside the ISO C++ standard.
  The constitution's C++ avatar assumes ISO C++ (MSVC/GCC/Clang); Borland VCL is
  a different ecosystem with different rules. The avatar should NOT be applied here
  without an Embarcadero/VCL overlay.

### IOC_ScreenPrinter (~32.6k LOC) — C++17 (explicitly set)  ✅ MODERN
- **Project file:** `MessageManager.vcxproj` (ToolsVersion 15.0)
- **PlatformToolset:** `v143` (Visual Studio 2022)
- **LanguageStandard:** `stdcpp17` — **C++17 explicitly configured** in most project configurations
- **Note:** Some configurations show `Default` — mixed; primary configs are C++17
- **Verdict:** **C++17** — the most modern MSVC project in the portfolio

### memtier-benchmarking (~12.8k LOC) — C++11/14 (Docker/GCC 11)
- **Build:** `autoreconf -ivf && ./configure && make` inside Docker
- **Base image:** `ubuntu:22.04` — ships GCC 11 with C++17 default (`-std=gnu++17`)
- **CXXFLAGS:** Not overridden in configure.ac — uses GCC 11 default
- **Source:** Open-source `memtier_benchmark` v2.1.4 — internally uses C++11/14 patterns
- **Purpose:** This repo is a thin wrapper that mirrors the open-source tool to
  `packages.aa.com/docker-*` — not AA-authored C++ code
- **Verdict:** **C++11/14 source compiled under GCC 11 C++17 default** — effectively C++17
  ABI but the source code does not exploit C++17 features

### mobileFOS2_iOS (~6.3k LOC) — Objective-C++ (Non-ISO)
- **Language:** `.m` (Objective-C) and `.mm` (Objective-C++) files throughout
- **Project:** `mobileFOS.xcodeproj` — Xcode project (no CMake, no MSVC)
- **Age indicators:** `.xib` files (pre-Storyboard iOS UI), committed `.ipa` files,
  ARC-era code — suggests Xcode 4–6 era (ca. 2011–2013)
- **No CI:** No `.github/workflows/` directory
- **Verdict:** **Objective-C++** — not standard ISO C++. The `.mm` files mix
  Objective-C message syntax with C++ class instantiation. The constitution's
  C++ avatar does not apply here; an iOS/Apple avatar would be needed.

### IOC_FosQuery2 (~2.1k LOC) — C++14 (archived project)
- **Project file:** `.vcxproj` ToolsVersion 14.0 format, `PlatformToolset v142`
- **LanguageStandard:** Not set — **C++14 default for v142 toolset**
- **Status:** Appears to be an archived/legacy tool
- **Verdict:** **C++14 default** — smallest repo, archived status, low priority

### app-mgmt-killapp (~275 LOC) — C++17 (CppWinRT)
- **Project file:** `KillApp.vcxproj`, PlatformToolset `v143`
- **CppWinRT version:** 2.0.220531.1 — **requires C++17 minimum** (documented requirement)
- **Source features confirmed:** `std::chrono`, `std::unordered_map`, lambdas,
  range-based for, `std::vector<std::wstring>`, `nullptr`
- **Verdict:** **C++17** — modern utility; smallest C++ codebase in the portfolio

---

## Fleet-Wide Summary

### By C++ Standard

| Standard | Repos | Total LOC | % of LOC |
|----------|-------|-----------|---------|
| C++17 (explicit) | IOC_ScreenPrinter, app-mgmt-killapp | ~32,875 | ~5% |
| C++14 (toolset default) | IOC_ALP, hte_pm_hostconn, CWR, IOC_FosQuery2 | ~449,800 | ~60% |
| C++11/14 (GCC/Docker) | memtier-benchmarking | ~12,800 | ~2% |
| C++98/03 | herc-odyssey-linux | ~80,600 | ~11% |
| Pre-C++98 (MSVC 6.0) | SPEClient | ~177,000 | ~24% |
| Non-ISO (Borland VCL) | supportATIS | ~33,600 | — |
| Non-ISO (Objective-C++) | mobileFOS2_iOS | ~6,300 | — |

**ISO C++ total: ~752,575 LOC across 9 repos**
**Non-ISO total: ~39,900 LOC in 2 repos**

### Key Findings for Option E Design

1. **C++14 is the center of gravity** (60% of ISO C++ LOC) — the avatar must excel here,
   particularly for "C++14 toolset running C++03-era idioms" (the CWR/hte_pm_hostconn scenario)

2. **SPEClient represents a critical technical debt risk** (~177k LOC, MSVC 6.0, no CI):
   - The second-largest codebase has ZERO automated build verification
   - MSVC 6.0 is incompatible with C++11 and later — any modernization attempt
     requires a complete toolchain migration, not just a language standard bump
   - The avatar should flag MSVC 6.0 patterns explicitly and warn about migration paths

3. **herc-odyssey-linux has a broken CI build** (~80k LOC):
   - The CI cannot compile the C++ code — no automated safety net
   - Code likely uses GCC extensions and pre-standard patterns
   - `-std=c++98` or `-std=c++03` should be explicitly set in the Makefile to
     prevent accidental use of newer features that aren't tested

4. **The portfolio spans ~25 years of C++ standards** (MSVC 6.0 ca. 1998 → C++17 current):
   - No single avatar persona can address all scenarios
   - Option E (project-declaration routing) is strongly validated by this data

5. **Two repos are not ISO C++ and should be explicitly excluded from C++ avatar scope:**
   - `supportATIS` → Borland/Embarcadero C++ Builder ecosystem
   - `mobileFOS2_iOS` → Objective-C++/iOS ecosystem
   - The avatar should detect Borland and Objective-C++ patterns and redirect

6. **C++17 adoption is small but present** (~5% LOC):
   - IOC_ScreenPrinter and app-mgmt-killapp are actively using C++17
   - The avatar needs to handle C++17-specific guidance (structured bindings,
     `if constexpr`, `std::optional`, `std::variant`, fold expressions)

### Confidence Assessment

| Repo | Evidence Quality | Main Gap |
|------|-----------------|---------|
| CWR | ✅ User confirmed | None |
| app-mgmt-killapp | ✅ Source + vcxproj | None |
| IOC_ScreenPrinter | ✅ vcxproj `stdcpp17` | None |
| supportATIS | ✅ VCL headers | RAD Studio version unknown |
| mobileFOS2_iOS | ✅ .mm file structure | None |
| SPEClient | ✅ .dsp + msvcp60.dll | Can't verify if any .vcxproj exists deeper |
| herc-odyssey-linux | ⚠️ Makefile, no std flag | -std flag could exist in sub-makefiles |
| hte_pm_hostconn | ⚠️ VS2019 + msbuild | vcxproj not inspected |
| IOC_ALP | ⚠️ msbuild + cmake | vcxproj not inspected |
| IOC_FosQuery2 | ⚠️ vcxproj v142 | Archived status |
| memtier-benchmarking | ⚠️ Dockerfile | configure.ac CXXFLAGS not fully traced |

---

## Implications for Option E

This survey directly answers the core design question:

> "What C++ versions do we need the avatar to handle well?"

**Answer:**
- **MUST HANDLE WELL:** C++14 (toolset default, majority LOC), C++03-idioms-in-C++14
- **MUST HANDLE:** C++17 (two active repos, modern patterns)
- **SHOULD HANDLE:** C++98/03 (herc-odyssey-linux; recognize and warn)
- **SPECIAL CASE:** MSVC 6.0 / pre-C++98 — recognize and provide migration path warning
- **OUT OF SCOPE (document explicitly):** Borland VCL, Objective-C++

The `project.md` declaration mechanism (Option E core feature) should support:
```yaml
cpp_standard: "14"          # actual toolset standard
cpp_idiom_level: "03"       # actual feature usage level (CWR scenario)
compiler: "msvc"            # msvc | gcc | clang | borland | objective-cpp
toolset: "v143"             # for MSVC: v140-v143
```

This enables the avatar to give advice calibrated to both the *maximum available*
standard AND the *current idiom level* — critical for the CWR brownfield scenario.

---

## Next Steps

1. **SPEClient — urgent consultation:** Engage the SPEClient team to understand the
   migration roadmap. A 177k LOC codebase on MSVC 6.0 with no CI is a significant
   risk. The avatar should proactively identify MSVC 6.0 patterns.

2. **herc-odyssey-linux — CI repair:** The commented-out C++ build in CodeQL should
   be investigated. Understanding why the C++ build fails is important for
   assessing actual code health.

3. **hte_pm_hostconn / IOC_ALP — vcxproj inspection:** Fetch and inspect the actual
   `.vcxproj` files to confirm whether `<LanguageStandard>` is set in any configuration.

4. **Proceed to Tier 1.2** (RAG infrastructure capability assessment) using these
   findings to scope which standard transitions need explicit routing paths.

5. **Draft Option E project.md schema** using the `cpp_standard` / `cpp_idiom_level` /
   `compiler` / `toolset` fields identified above.

---

*Survey conducted: 2025 | Evidence from GitHub repository files and CI workflow analysis*
*Committed to: `hangar-ai-specs/changes/cpp-version-sensitivity-analysis/production-version-survey.md`*
