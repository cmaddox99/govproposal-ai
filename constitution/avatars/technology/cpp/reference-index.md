# C++ Avatar Reference Index

> Navigation hub for the C++ avatar's extended reference documentation.
> Each file is sized to fit within a single RAG query window (≤3,500 tokens).

---

## Getting Started

| Topic | File | Description |
|-------|------|-------------|
| Glossary & Quick-Start | [ref-getting-started.md](refs/language/ref-getting-started.md) | Java-to-C++ glossary, project setup guide, version policy |

## Core Language

| Topic | File | Description |
|-------|------|-------------|
| Core Type Safety | [ref-core-type-safety.md](refs/language/ref-core-type-safety.md) | Const correctness, casts, null safety |
| Core Modern Idioms | [ref-core-modern-idioms.md](refs/language/ref-core-modern-idioms.md) | Designated initializers, variant, any, optional |
| Domain Patterns | [ref-domain-patterns.md](refs/language/ref-domain-patterns.md) | DDD patterns, dependency injection, ownership |
| Domain Quality and Anti-Patterns | [ref-domain-quality.md](refs/language/ref-domain-quality.md) | SRP refactoring, anti-patterns |
| Object Design Rehabilitation | [ref-object-design-rehabilitation.md](refs/language/ref-object-design-rehabilitation.md) | Object rehabilitation anti-patterns 1-5 |
| Object Design Patterns | [ref-object-design-patterns.md](refs/language/ref-object-design-patterns.md) | Move semantics, decision trees, design patterns, test isolation |

## Testing & Build

| Topic | File | Description |
|-------|------|-------------|
| CI Quality Toolchain Policy | [ref-testing-ci-policy.md](refs/testing/ref-testing-ci-policy.md) | CI toolchain policy, VS 2022 equivalents, clang-tidy CI gates |
| GoogleTest Core Patterns | [ref-testing-gtest-core.md](refs/testing/ref-testing-gtest-core.md) | Testing framework, TEST/TEST_F/EXPECT/ASSERT macros, exception testing |
| GoogleTest Advanced Patterns | [ref-testing-gtest-advanced.md](refs/testing/ref-testing-gtest-advanced.md) | Template test helpers, fixture deep dive, concurrency testing |
| Build Packages and Reproducible Builds | [ref-build-packages.md](refs/testing/ref-build-packages.md) | CMake, vcpkg, C++20 modules, reproducible builds ★ C++20+ |
| Build Toolchain Gap — UBSan and MSVC | [ref-build-ubsan-msvc.md](refs/testing/ref-build-ubsan-msvc.md) | UBSan/MSVC toolchain gap, sanitizer alternatives |
| Templates and Metaprogramming | [ref-templates-metaprogramming.md](refs/language/ref-templates-metaprogramming.md) | Templates, ADL, lambdas, forwarding |
| Advanced Template Techniques | [ref-templates-advanced.md](refs/language/ref-templates-advanced.md) | Type traits, tag dispatch, NTTPs, expression templates, C++20 lambdas ★ C++11-20 |
| C++20 Features Part 1 | [ref-cpp20-features-part1.md](refs/language/ref-cpp20-features-part1.md) | Modules, ranges, std::span, spaceship operator ★ C++20 |
| C++20 Features Part 2 | [ref-cpp20-features-part2.md](refs/language/ref-cpp20-features-part2.md) | Coroutine generators, aggregate improvements, calendar/timezone ★ C++20 |
| C++20 Features Part 3 | [ref-cpp20-features-part3.md](refs/language/ref-cpp20-features-part3.md) | std::format, std::bit_cast, source_location, constinit, atomic_ref ★ C++20 |
| Advanced C++ Patterns | [ref-advanced-patterns.md](refs/language/ref-advanced-patterns.md) | Preprocessor, allocators, ABI |

## Safety & Runtime

| Topic | File | Description |
|-------|------|-------------|
| Safety-Critical C++ — MISRA and DO-178C | [ref-safety-misra-do178.md](refs/safety/ref-safety-misra-do178.md) | MISRA C++, DO-178C, JSF AV rules |
| Memory Lifetime and FFI Safety | [ref-safety-memory-lifetime.md](refs/safety/ref-safety-memory-lifetime.md) | Advanced memory lifetime, FFI |
| JNI Safety and ABI Governance | [ref-safety-jni-abi.md](refs/safety/ref-safety-jni-abi.md) | JNI safety, ABI stability |
| FAR 117 Aviation Safety and CWR | [ref-safety-far117-cwr.md](refs/safety/ref-safety-far117-cwr.md) | FAR 117 compliance, CWR anti-pattern catalog (CWR/DO-278A) |
| Concurrency and Threading | [ref-concurrency-threading.md](refs/safety/ref-concurrency-threading.md) | Threads, coroutines, exception safety, termination/recovery ★ C++11+ |
| Concurrency Async and Resiliency | [ref-concurrency-async.md](refs/safety/ref-concurrency-async.md) | Resiliency patterns, circuit breakers ★ C++17+ |
| Advanced Concurrency Part 1 | [ref-concurrency-advanced-part1.md](refs/language/ref-concurrency-advanced-part1.md) | Lock-free, memory ordering, condition variables, false sharing, thread pool ★ C++11+ |
| Advanced Concurrency Part 2 | [ref-concurrency-advanced-part2.md](refs/language/ref-concurrency-advanced-part2.md) | jthread/stop_token, coroutine-concurrency safety ★ C++20 |
| Infrastructure | [ref-infrastructure.md](refs/testing/ref-infrastructure.md) | Logging, config, health checks, license compliance, tools |

## Brownfield & Legacy

> **★ = version-annotated** — content is specific to one C++ standard tier. Start with the file matching your project's `__cplusplus` value.

| Topic | File | Description |
|-------|------|-------------|
| Brownfield Adoption | [ref-brownfield-adoption.md](refs/legacy/ref-brownfield-adoption.md) | Per-tier clang-tidy, testing, code review, ABI, feature detection |
| Brownfield Project Configuration | [ref-brownfield-project-config.md](refs/legacy/ref-brownfield-project-config.md) | Compiler flags, sanitizers, IOC_ALP load planning domain, MFC brownfield |
| Brownfield Survival Patterns | [ref-brownfield-survival.md](refs/legacy/ref-brownfield-survival.md) | Rule of Three, MSVC 6.0 golden-master testing ★ C++98 |
| Coplien-Era Pattern Recognition | [ref-brownfield-coplien.md](refs/legacy/ref-brownfield-coplien.md) | Handle/Body, Counted Body, COM IUnknown — AA governance verdicts ★ C++98 |
| Migration Playbooks (Pre-C++17) | [ref-migration-pre-cpp17.md](refs/legacy/ref-migration-pre-cpp17.md) | C++98→11→14→17 step-by-step, dual-toolchain ★ C++98-C++17 |
| Migration Patterns (C++17+) | [ref-migration-cpp17-plus.md](refs/legacy/ref-migration-cpp17-plus.md) | C++17→20 survival patterns, ActiveTest.h → GoogleTest migration ★ C++17+ |
| Legacy Navigation | [ref-legacy-navigation.md](refs/legacy/ref-legacy-navigation.md) | Codebase navigation, survival patterns, priority matrix |
| Legacy Codebase Triage Playbook | [ref-legacy-triage-playbook.md](refs/legacy/ref-legacy-triage-playbook.md) | Triage playbook, ActiveTest migration strategies |
| Mental Models — Memory and Compilation | [ref-mental-models-memory.md](refs/legacy/ref-mental-models-memory.md) | Value semantics, RAII, UB — mental model gaps 1-6 |
| Mental Models — Language and Runtime | [ref-mental-models-lang.md](refs/legacy/ref-mental-models-lang.md) | Linking, templates, ODR, runtime — mental model gaps 7-13 |
| Legacy Code Smells — Structural | [ref-legacy-smells-structural.md](refs/legacy/ref-legacy-smells-structural.md) | Smell catalog smells 1-7, summary table |
| Legacy Code Smells — Patterns | [ref-legacy-smells-patterns.md](refs/legacy/ref-legacy-smells-patterns.md) | Smell catalog smells 8-14 with remediation patterns |

---

*See [guidance.md](guidance.md) for non-negotiable laws and the always-loaded RAG anchor.*
*See [split-reference-architecture guide](../../docs/guides/avatars/split-reference-architecture.md) for how this index works.*
