# PROPOSAL: IOC_ALP C++ Avatar Enrichment

**Proposal ID:** alp-cpp-avatar-enrichment
**Status:** COMPLETE
**Branch:** proposal/alp-cpp-avatar-enrichment
**Stacked on:** proposal/cwr-cpp-avatar-enrichment → feature/c-plus-plus-avatar-enrichment-proposal (PR #14)
**Laws:** ENG-4.1, ENG-10.1, ENG-11.1
**Source codebase:** `AAInternal/IOC_ALP` (PCLoadPlan / Integrated Operations Control)

---

## Source Codebase Facts

| Attribute | Value |
|-----------|-------|
| App short name | PCLoadPlan |
| Squad | 100109 — Flight Execution Midrange |
| Domain | Airline Load Planning (weight/balance, cargo, MEL compliance) |
| C++ Standard | C++98/C++03 (uses nullptr, no auto/lambdas) |
| Compiler | MSVC v142/v143 (Visual Studio 2019/2022) |
| Build | `msbuild ALPGUI.sln /p:Configuration=Release` + CMake |
| Platform | Windows only (MFC/AFX, no Linux/macOS target) |
| Files | 474 headers + 427 cpp in alpsource/, ~1,200 total |
| Largest class | `Flight.h` 945 lines (god class) |
| Smart pointers | Custom `RCPtr<T>` / `RCObject` (Scott Meyers pattern, 650+ usages) |
| Threading | Custom Windows threads in `Thread Classes/` (NOT std::thread) |
| Exceptions | CALPException → CHostException → 15+ domain variants |
| CI/CD | SonarQube, CodeQL, Coverity, BlackDuck |
| Age | ~25 years in production (creation comments dated 1999) |

---

## Gap Analysis: C++ Avatar vs IOC_ALP Patterns

| Gap | Avatar current state | IOC_ALP reality |
|-----|---------------------|----------------|
| Build command | CMake only | MSVC msbuild ALPGUI.sln |
| Dependencies | Abseil/gRPC/OpenSSL | AACCSAPI.lib (Sabre), TinyXML2, culib, MFC |
| Naming conventions | PascalCase only | MFC `C` prefix (CFlight, CDataManager) + suffix patterns |
| Project archetype | No Windows/MFC archetype | alpsource/ + Thread Classes/ + AlpWindows/ + .sln |
| Smart pointers | std::unique_ptr/shared_ptr | Custom RCPtr<T>/RCObject (pre-C++11 RAII) |
| Exception examples | Generic std::exception | 15-tier CALPException/CHostException hierarchy |
| Threading | std::thread | Windows CRITICAL_SECTION wrappers, message posting |
| Test framework | GoogleTest | Custom TestRunner.lib + ActiveTest.h (37 headers) |
| Aviation domain | None specific | ZFW envelope, CG calc, MEL, 7-week history (FAA) |
| Anti-patterns | Generic catalog | MFC-specific: god class, macro abuse, mixed ownership |

---

## Task List (10 tasks — ALP-01 through ALP-10)

See [tasks.md](./tasks.md) for full task definitions.

---

## Acceptance Criteria

- [ ] manifest.yaml has `brownfield_msvc_build` commands block
- [ ] manifest.yaml has `brownfield_mfc_stack` dependencies block
- [ ] manifest.yaml has `brownfield_mfc_cpp98` conventions block
- [ ] manifest.yaml `activates.project_archetypes` has `brownfield_winforms_desktop`
- [ ] `examples/ENG-2.3-rcptr-abi-stability.md` exists (≤850 tokens)
- [ ] `examples/ENG-6.1-host-exception-safety.md` exists (≤850 tokens)
- [ ] `ENG-4.1-atomic-tdd.md` has Windows/MFC brownfield section
- [ ] `full-reference.md` has Load Planning domain section (ZFW/CG/MEL)
- [ ] `full-reference.md` has MFC Windows Brownfield Governance section
- [ ] `full-reference.md` has IOC_ALP Anti-Pattern Catalog section
- [ ] All tests pass (663+), lint 17/17
- [ ] Manifest version bumped 2.0.0 → 2.2.0 (after both CWR + ALP enrichments)
