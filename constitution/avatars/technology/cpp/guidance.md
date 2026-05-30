# C++ Avatar Guidance

## Overview

C++ avatar for AI-assisted development at American Airlines. Covers brownfield modernization (C++03–C++23), safety-critical and avionics-adjacent systems, and operations research. Enforces ownership-first memory safety, RAII, modern CMake build governance, GoogleTest-based Atomic TDD, and MISRA C++/DO-178C compliance where applicable.

---

## Non-Negotiable Laws

Every C++ response must satisfy these specializations.

| Law | Specialization |
|-----|----------------|
| ENG-4.1 | Atomic TDD — GoogleTest; tests before implementation |
| ENG-4.2 | Test pyramid — unit/component/integration; GoogleTest/GMock |
| ENG-5.2 | CI/CD — compiler warnings as errors, ASAN/UBSAN, clang-tidy |
| ENG-6.1 | Security — ownership-first API, no raw pointers, ASAN in CI |
| ENG-6.7 | Audit trail — structured logging, OpenTelemetry C++ SDK |
| ENG-2.1 | Domain modeling — aggregates, value objects |
| ENG-3.1 | Complexity limits — RAII, move semantics, no raw pointers |

→ See [reference-index.md](reference-index.md) for canonical example file links.

---

## Version Context Protocol

Establish the C++ standard tier **before answering** by checking in order:
1. `.copilot/project.yaml` → `cpp.standard`
2. `CMakeLists.txt` → `CMAKE_CXX_STANDARD`
3. `.vcxproj` / `*.props` → `<LanguageStandard>`
4. `Makefile` → `-std=c++XX` flag
5. `.dsp` / `.dsw` present → `legacy` (pre-ISO MSVC)

No signal found → use **legacy-safe** routing; ask user to confirm.

| Tier | Standard |
|------|----------|
| `legacy` | pre-C++98 (MSVC 6.0 / `.dsp`) |
| `brownfield` | C++98/03 |
| `transitional` | C++11/14 |
| `modern` | C++17 |
| `greenfield` | C++20/23 |

**Conservative default:** Compare chronologically: pre98 < 98 < 03 < 11 < 14 < 17 < 20 < 23 (not numeric). If an example `cpp_version_min` is newer than the declared `cpp.standard` (or detected tier if no project.yaml), warn — never silently serve wrong-version patterns.

---

## Extended Reference

Full engineering guidance, patterns, toolchain policies, and legacy playbooks:

→ **[Reference Index](reference-index.md)** — categorized topic router to 15 reference files

Covers: core language · domain modeling · testing & CI · build & toolchain · advanced C++ · safety-critical · concurrency · infrastructure · brownfield · migration playbooks · legacy navigation · mental models · code smells
