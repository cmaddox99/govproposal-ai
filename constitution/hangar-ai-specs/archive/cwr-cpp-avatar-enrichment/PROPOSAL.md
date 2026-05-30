# Proposal: CWR C++ Avatar Enrichment

> **Workflow Mode:** Avatar Workflow — Mode 4 (Enrich)
> **Source Codebase:** `projects/AgenticAI/CWR/CrewRecoveryFAR117`
> **Target Avatar:** `avatars/technology/cpp/` (v2.0.0)
> **Law:** ENG-11.1 (Hangar SDD), ENG-10.1 (Constitution Integrity)
> **Status:** COMPLETE

---

## 1. Problem Statement

The C++ avatar (v2.0.0) was built with greenfield, CMake-based, C++20 patterns. The CWR (CrewWatch Recovery) codebase — a safety-critical, FAA FAR Part 117 crew recovery optimizer — is a **C++98 legacy system** with a JNI interface, NetBeans Makefile build system, and a fundamentally different library stack.

Running the avatar-workflow Mode 4 (Enrich) against CWR reveals 10 grounding gaps. Without these enrichments, an AI agent using the C++ avatar to assist with CWR would:
- Suggest CMake when the project uses NetBeans Makefiles
- Recommend Abseil/gRPC/OpenSSL when the stack uses Xpress MP/jsoncpp/TinyXML
- Apply C++20 patterns to a C++98 codebase with no migration plan
- Miss JNI memory safety obligations entirely
- Have no FAR 117 / aviation safety-critical guidance

---

## 2. Codebase Discovery Summary (Phase 4, Step 4.1)

| Dimension | CWR Finding |
|-----------|-------------|
| **C++ Standard** | C++98/C++03 (no `-std=c++11` or higher) |
| **Build System** | NetBeans Makefiles (`nbproject/Makefile-CI-Release.mk`) |
| **Compiler** | `g++` (Linux CI), `clang++` (macOS dev) |
| **Output Artifact** | Shared library (`libSolver.so` / `libSolver.dylib`) |
| **Primary Dependency** | FICO Xpress MP solver (integer programming) |
| **Supporting Deps** | libcurl, jsoncpp, restclient-cpp, TinyXML (embedded) |
| **Java Integration** | JNI — single entry point `runSolverJNI(String) → String` |
| **Java Version** | JDK 1.7.0_80 |
| **Testing** | None (no active test framework; gtest present in `.vendor/` but unintegrated) |
| **CI/CD** | Manual shell scripts (no GitHub Actions) |
| **Error Handling** | Return codes + NULL checks; no RAII |
| **FAA Compliance** | FAR Part 117 crew rest/duty limits enforced in solver |
| **Largest File** | `Solver/Crew.cpp` — 947 KB (god class anti-pattern) |
| **Naming Patterns** | `Node` suffix (data containers), `Inf` suffix (collections), `XL_` typedef prefix |

---

## 3. Gap Analysis (Phase 2 + Phase 4 synthesis)

| ID | Gap | Severity | Avatar File Affected |
|----|-----|----------|----------------------|
| G-01 | `commands` block references CMake — CWR uses NetBeans make | 🟡 WARNING | `manifest.yaml` |
| G-02 | `dependencies` lists generic Abseil/gRPC/OpenSSL — CWR uses Xpress/jsoncpp/TinyXML/JNI | 🟡 WARNING | `manifest.yaml` |
| G-03 | `conventions` missing `Node`/`Inf` suffix and `XL_` typedef prefix patterns | 🟡 WARNING | `manifest.yaml` |
| G-04 | `project_structure` reflects greenfield DDD layout — CWR has Solver/PopulateSolver/XMLInput | 🟡 WARNING | `manifest.yaml` |
| G-05 | No JNI ABI stability example — C++/Java boundary memory obligations not documented | 🔴 BLOCKING | `examples/` (missing file) |
| G-06 | No safety-critical JNI pattern — FAR 117 correctness constraints unspecified | 🔴 BLOCKING | `examples/` (missing file) |
| G-07 | `ENG-4.1` example is greenfield only — no characterization test strategy for C++98 brownfield | 🟡 WARNING | `examples/ENG-4.1-atomic-tdd.md` |
| G-08 | `full-reference.md` has no JNI safety section | 🟡 WARNING | `docs/guides/avatars/cpp/full-reference.md` |
| G-09 | `full-reference.md` has no FAR 117 / aviation safety-critical section | 🟡 WARNING | `docs/guides/avatars/cpp/full-reference.md` |
| G-10 | `full-reference.md` has no CWR-specific anti-pattern catalog (10 identified) | 🟡 WARNING | `docs/guides/avatars/cpp/full-reference.md` |

**BLOCKING gaps:** 2 (G-05, G-06) — missing required example files for laws in `specializes_laws`
**WARNING gaps:** 8 (G-01 through G-04, G-07 through G-10)

---

## 4. Proposed Changes

### 4.1 Manifest Grounding (G-01 through G-04)

Update `avatars/technology/cpp/manifest.yaml`:

**`commands` block** — add `brownfield_makefile` commands alongside existing CMake:
```yaml
brownfield_makefile:
  build: "make -f nbproject/Makefile-CI-Release.mk ./CI-Release/libSolver.so"
  build_debug: "make CONF=Debug"
  build_all: "make all"
  clean: "make clean"
  run: "./runSolver/runSolver.sh <solver-request.xml>"
```

**`dependencies` block** — add `brownfield_jni_stack`:
```yaml
brownfield_jni_stack:
  solver: "FICO Xpress MP (libxprb, libxprs, libxprl)"
  http: "libcurl (bundled)"
  json: "jsoncpp (bundled)"
  xml: "TinyXML 2.6.1 (embedded)"
  rest: "restclient-cpp (vendored)"
  java_bridge: "JNI — JDK 1.7+ (libSolver.so loaded via System.loadLibrary)"
```

**`conventions` block** — add `brownfield_cpp98` naming:
```yaml
brownfield_cpp98:
  class_data_container: "PascalCaseNode (e.g., CrewNode, FlightNode, DutyPeriodNode)"
  class_collection: "PascalCaseInf (e.g., CrewInf, FlightInf)"
  typedef_prefix: "XL_ (e.g., XL_SET_INT, XL_MAP_INT, XL_MAPMAPPAIRLIST_INT)"
  file_naming: "PascalCase for classes, snake_case for utility functions"
  global_extern: "extern declarations at translation unit boundary (legacy pattern)"
```

**`project_structure` block** — add `brownfield_jni_solver` archetype:
```yaml
brownfield_jni_solver:
  Solver/: "Core optimization logic + JNI entry point"
  PopulateSolver/: "Data population from REST/XML → solver model"
  XMLInput/: "TinyXML-based XML request parsing"
  ConnectLookAheadOCCI/: "Database connectivity"
  libs/: "Bundled dependencies (curl, jsoncpp, restclient)"
  runSolver/: "JNI JAR + shell scripts"
  nbproject/: "NetBeans build configurations"
```

### 4.2 New Example Files (G-05, G-06)

**`examples/ENG-2.3-jni-abi-stability.md`** — JNI ABI stability and memory management:
- Never use Java objects across JNI calls without global refs
- `GetStringUTFChars` requires `ReleaseStringUTFChars`
- Exception propagation across the JNI boundary
- RAII wrapper for `JNIEnv*` local frames
- CWR pattern: `runSolverJNI(String) → String` boundary contract

**`examples/ENG-6.1-safety-critical-jni.md`** — FAR 117 + safety-critical C++ patterns:
- Correctness obligations for safety-critical solvers
- Input validation for duty/rest constraint parameters
- `MinRestAndEight()` contract preservation under refactoring
- `FAR117FLtTimeTable()` regression testing with characterization tests
- No undefined behavior in constraint matrix construction

### 4.3 Example Updates (G-07)

**Update `examples/ENG-4.1-atomic-tdd.md`** — add brownfield section:
- Characterization test pattern for legacy C++98 code with no existing tests
- `ApprovalTests` / `GoogleTest` characterization setup
- Sprout Method pattern in `Crew.cpp`-style god classes
- Seam injection around global `extern` state

### 4.4 Full-Reference Sections (G-08, G-09, G-10)

Add three new sections to `docs/guides/avatars/cpp/full-reference.md`:

**§ JNI Safety and ABI Governance** (~600 tokens)
- Local vs global references
- Exception propagation
- Memory ownership across the boundary
- Version-stable JNI method signatures

**§ Aviation Safety-Critical C++ Patterns** (~800 tokens)
- FAR 117 constraint enforcement
- Correctness before performance
- No undefined behavior in safety path
- Characterization tests as safety regression net

**§ CWR Anti-Pattern Catalog** (~1,000 tokens)
10 documented anti-patterns from CWR codebase with before/after:
1. Raw `malloc` → RAII `std::vector`
2. C-style casts → `static_cast`/`reinterpret_cast`
3. Global `extern` state → dependency injection
4. `throw -1` → typed exception hierarchy
5. `FILE*` manual close → `std::ifstream` RAII
6. 947 KB god class (`Crew.cpp`) → decomposition strategy
7. 470-inline-method header → `.cpp` implementation split
8. Nested `typedef` chains → named type aliases
9. Mixed `printf`/`cout` → unified structured logging
10. Uninitialized `atoi` → validated `strtol`

---

## 5. RAG Validation Plan (Phase 5)

After implementation, validate 5 canonical queries:

| Query | Expected Load | Max Tokens |
|-------|--------------|-----------|
| "C++ JNI memory safety boundary" | `guidance.md` + `ENG-2.3-jni-abi-stability.md` | ≤1,800 |
| "FAR 117 crew rest C++ characterization test" | `guidance.md` + `ENG-6.1-safety-critical-jni.md` + `ENG-4.1-atomic-tdd.md` | ≤2,400 |
| "C++98 brownfield makefile build" | `guidance.md` + manifest commands section | ≤1,200 |
| "CWR god class decomposition strategy" | `full-reference.md § anti-pattern catalog` | ≤1,800 |
| "JNI ABI stability naming convention" | `ENG-2.3-jni-abi-stability.md` + manifest conventions | ≤1,500 |

Threshold: Recall ≥ 5/5, max query load ≤ 3,500 tokens, 0 BLOCKING violations.

---

## 6. Versioning

Per avatar-workflow Phase 6 versioning protocol:
- Mode 4 (Enrich) = **MINOR bump**
- Current version: `2.0.0` → target: **`2.1.0`**

---

## 7. Acceptance Criteria

```gherkin
Scenario: CWR brownfield build commands are grounded
  Given the C++ avatar manifest.yaml
  When a brownfield NetBeans project agent reads the commands block
  Then it finds "make -f nbproject/Makefile-CI-Release.mk" in brownfield_makefile

Scenario: JNI ABI example exists for ENG-2.3
  Given the C++ avatar examples/ directory
  When the avatar is loaded for a JNI boundary question
  Then ENG-2.3-jni-abi-stability.md is present and within 850 token budget

Scenario: Safety-critical JNI example exists for ENG-6.1
  Given the C++ avatar examples/ directory
  When the avatar is loaded for a FAR 117 safety question
  Then ENG-6.1-safety-critical-jni.md is present and within 850 token budget

Scenario: full-reference.md contains JNI safety section
  Given docs/guides/avatars/cpp/full-reference.md
  When an agent queries "JNI safety"
  Then a "JNI Safety and ABI Governance" section is present

Scenario: full-reference.md contains FAR 117 section
  Given docs/guides/avatars/cpp/full-reference.md
  When an agent queries "aviation safety-critical C++"
  Then an "Aviation Safety-Critical C++ Patterns" section is present

Scenario: full-reference.md contains CWR anti-pattern catalog
  Given docs/guides/avatars/cpp/full-reference.md
  When an agent queries "C++ anti-patterns brownfield"
  Then a "CWR Anti-Pattern Catalog" section with ≥10 entries is present

Scenario: Avatar version bumped to 2.1.0 on completion
  Given the C++ avatar manifest.yaml
  When enrichment is complete
  Then avatar.version is "2.1.0"
```

---

## 8. Out of Scope

- Rewriting CWR source code (enrichment is avatar-only)
- Adding CI/CD to CWR (separate proposal needed)
- Adding GoogleTest to CWR (separate proposal needed)
- Product-type or industry avatar changes (BUS/PRD domain boundary respected)
