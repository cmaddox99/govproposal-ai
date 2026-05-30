---
cpp_version_min: 11
cpp_version_note: >-
  Runtime sanitizer configuration for C++11+ projects.
avatar: cpp
---

# C++ Avatar Reference: Build Toolchain Gap - UBSan and MSVC

---

## Toolchain Gap — UBSan Not Available on MSVC

MSVC does not support UndefinedBehaviorSanitizer. Equivalent controls:
- `/RTC1` runtime checks in Debug builds (stack corruption, uninitialized variables)
- MSVC `/analyze` with C26451 (arithmetic overflow)
- Code review checklist for integer arithmetic and pointer operations

Migration path: Add a Linux CI stage using GCC/Clang with `-fsanitize=undefined`
for full UBSan coverage. Target: [milestone date].
```

### Compiler Warning Flags Policy

Per [ENG-5.2](laws/engineering/eng-5-devops.md), all C++ builds must enable strict compiler warnings treated as errors. Without `-Werror`, warnings accumulate and mask real bugs — a `-Wsign-compare` warning in fare or fuel calculation could silently wrap a value, producing incorrect results.

**Mandatory flags (all compilers):**

```cmake
# CMakeLists.txt — apply to all targets
target_compile_options(${PROJECT_NAME} PRIVATE
    $<$<CXX_COMPILER_ID:GNU,Clang,AppleClang>:
        -Wall -Wextra -Wpedantic -Werror
        -Wconversion -Wsign-conversion
        -Wnon-virtual-dtor -Wold-style-cast
        -Woverloaded-virtual -Wnull-dereference
    >
    $<$<CXX_COMPILER_ID:MSVC>:
        /W4 /WX /permissive-
    >
)
```

| Flag | Purpose |
|------|---------|
| `-Wall` | Enable most common warnings |
| `-Wextra` | Additional warnings not covered by `-Wall` |
| `-Wpedantic` | Strict ISO C++ compliance; reject extensions |
| `-Werror` | Treat all warnings as errors — **non-negotiable** |
| `-Wconversion` | Implicit narrowing conversions (critical for fare/weight calculations) |
| `-Wsign-conversion` | Signed/unsigned mismatch (prevents silent wraparound) |
| `-Wnon-virtual-dtor` | Missing virtual destructor in polymorphic base (prevents memory leaks) |
| `-Wold-style-cast` | Flags C-style casts that should use `static_cast` etc. |

**Suppressing warnings:** Individual warnings may be suppressed **only** with an inline pragma and a comment explaining why:

```cpp
// NOLINT: third-party header triggers -Wold-style-cast; no fix available
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wold-style-cast"
#include <legacy_vendor_header.h>
#pragma GCC diagnostic pop
```

**Brownfield exception:** Repositories with extensive pre-existing warnings may adopt `-Werror` incrementally: Phase 1 — enable flags without `-Werror` to measure warning count; Phase 2 — fix warnings module-by-module; Phase 3 — enable `-Werror` once warning count is zero.

### SAST (Static Application Security Testing)

Per [ENG-6.1](laws/engineering/eng-6-security.md) (Security by Design), C++ projects must include static application security testing in CI.

**Default tools:** `clang-tidy` (compiler-adjacent diagnostics) + CodeQL C/C++ (security-focused query analysis).

- **`clang-tidy`** runs on every PR as a mandatory CI gate — catches common bugs, style violations, security anti-patterns, and modernization opportunities
- **CodeQL C/C++** provides deeper security-focused analysis with query packs for buffer overflows, injection, and memory corruption — requires GitHub Advanced Security
- Together they provide layered SAST coverage: fast compiler-level checks plus deep security scanning

**Brownfield exception:** If CodeQL is not available (e.g., no GitHub Advanced Security license), document the gap and use `clang-tidy` security checks plus the clang static analyzer as an interim equivalent. Define a migration path toward full CodeQL adoption with milestones.

### Dependency and Vulnerability Scanning

Per [ENG-6.1](laws/engineering/eng-6-security.md), C++ projects must include dependency vulnerability scanning in CI.

**Default tools:** Dependabot alerts + GitHub dependency review.

- **Dependabot** provides continuous CVE (Common Vulnerabilities and Exposures) visibility for dependencies declared in `vcpkg.json` or `conanfile.txt`, with automated pull requests for vulnerable dependency updates
- **GitHub dependency review** blocks PRs that introduce dependencies with known vulnerabilities
- For C++ libraries vendored as source (not managed via package manager), maintain a manual vulnerability tracking list and review against NVD/CVE databases on a regular cadence

**Brownfield exception:** If a repository uses a dependency management approach not supported by Dependabot (e.g., manually vendored third-party source, internal package registry), document the current approach, ensure an equivalent vulnerability scanning control exists, and define a migration path toward Dependabot-compatible tooling.

### DAST (Dynamic Application Security Testing)

Per [ENG-6.1](laws/engineering/eng-6-security.md), web-exposed C++ services must include dynamic security testing.

**Default tool:** OWASP (Open Worldwide Application Security Project) ZAP (Zed Attack Proxy) baseline scan in staging/test environments.

- Run OWASP ZAP as an automated baseline scan against HTTP/HTTPS endpoints during CI/CD pipeline staging deployments
- For C++ services without web-facing endpoints (e.g., libraries, CLI tools, embedded systems), DAST is not applicable — document the exemption
- For gRPC or non-HTTP services, use protocol-appropriate fuzzing tools as an equivalent control

**Brownfield exception:** If OWASP ZAP cannot be integrated into the current pipeline (e.g., no staging environment, non-HTTP service), document the constraint and define a phased adoption plan. Ensure an equivalent runtime security testing control exists in the interim.

### Secrets Management

Per [ENG-5.6](laws/engineering/eng-5-devops.md) (Configuration Management Law), C++ projects must not store secrets in source code or environment variables.

**Default:** HashiCorp Vault or cloud-native secret manager (AWS Secrets Manager, Azure Key Vault, GCP Secret Manager).

- All credentials, API keys, certificates, and connection strings must be retrieved at runtime from a managed secret store
- Use the platform-appropriate SDK or CLI to fetch secrets during application startup or CI/CD pipeline execution
- Rotate secrets on a defined cadence; never embed secrets in `CMakeLists.txt`, source files, or configuration committed to version control
- CI/CD pipelines should use short-lived credentials (e.g., OIDC tokens) rather than long-lived service account keys

**Brownfield exception:** If a repository currently uses environment variables or config files for secrets, document the current approach, ensure secrets are not committed to source control, and define a migration path toward a managed secret store with milestones.

### Infrastructure as Code (IaC)

Per [ENG-5.1](laws/engineering/eng-5-devops.md) (Infrastructure as Code Law), C++ project infrastructure must be defined as code with drift detection.

**Default:** Terraform with policy checks and drift detection in CI.

- Define all infrastructure (build environments, deployment targets, CI runners) in Terraform HCL
- Run `terraform plan` in CI to detect drift before apply
- Use policy-as-code tools (e.g., OPA/Rego, Sentinel) for compliance guardrails
- Store Terraform state in a remote backend (e.g., S3, Azure Blob, GCS) with state locking

**Brownfield exception:** If a repository uses an alternative IaC tool (e.g., Ansible, CloudFormation, Pulumi), document the current tool, ensure it provides equivalent reproducibility and drift detection, and define a migration path toward Terraform if cross-platform standardization is a goal.

### Coverage Tooling

Per [ENG-4.2](laws/engineering/eng-4-testing.md) (Test Pyramid Law) and [ENG-4.6](laws/engineering/eng-4-testing.md) (Coverage Requirements), C++ projects must report code coverage in CI.

**Default:** `llvm-cov` (or `gcov`-compatible output) integrated into CI gates.

- Use `llvm-cov` with Clang or `gcov` with GCC to generate coverage reports
- Integrate coverage reporting into CI — fail the build if coverage drops below the project-defined threshold
- Generate machine-readable output (LCOV, Cobertura XML) for CI dashboard integration
- Coverage thresholds are project-defined; the constitution does not mandate a specific percentage but requires that coverage is measured and tracked

```bash
# Generate coverage with llvm-cov
cmake -B build -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_FLAGS="--coverage"
cmake --build build && ctest --test-dir build
llvm-cov report ./build/tests/unit/<test_binary>
```

**Brownfield exception:** If a repository uses a different coverage tool (e.g., Bullseye, gcovr wrapper), document the current tool and ensure it provides equivalent CI-integrated coverage reporting.

### Observability

Per [ENG-5.5](laws/engineering/eng-5-devops.md) (Observability Law), C++ services must export telemetry data.

**Default:** OpenTelemetry C++ SDK with OTLP export, Prometheus metrics, and centralized structured logging.

- **Traces:** Instrument C++ services with `opentelemetry-cpp` SDK; export traces via OTLP to the organization's tracing backend
- **Metrics:** Expose Prometheus-compatible metrics endpoint for scraping; use OpenTelemetry metrics API for custom business metrics
- **Logs:** Use structured logging (JSON format) with correlation IDs linking to distributed traces; route to centralized log aggregation
- Ensure all three signals (traces, metrics, logs) share correlation context for end-to-end observability

**Brownfield exception:** If a repository uses existing observability tooling (e.g., custom logging, StatsD metrics), document the current stack, ensure it provides equivalent trace/metric/log correlation, and define a migration path toward OpenTelemetry with milestones.

### Cross-Language Alignment Defaults Summary

The following matrix summarizes C++ tool defaults aligned with existing avatar patterns across the constitution. Each default is documented in detail in its own subsection above.

| Concern | C++ Default | Cross-Language Pattern | Law |
|---------|-------------|----------------------|-----|
| SAST | `clang-tidy` + CodeQL C/C++ | Native static analyzers per language | [ENG-6.1](laws/engineering/eng-6-security.md) |
| Dependency/Vulnerability Scanning | Dependabot + GitHub dependency review | GitHub-centric CVE scanning | [ENG-6.1](laws/engineering/eng-6-security.md) |
| DAST | OWASP ZAP baseline | Baseline DAST for web services | [ENG-6.1](laws/engineering/eng-6-security.md) |
| Secrets Management | HashiCorp Vault / cloud secret manager | Managed secret storage | [ENG-5.6](laws/engineering/eng-5-devops.md) |
| IaC | Terraform + drift checks | Reproducible infrastructure | [ENG-5.1](laws/engineering/eng-5-devops.md) |
| Coverage Tooling | `llvm-cov` / `gcov` | Language-native coverage | [ENG-4.2](laws/engineering/eng-4-testing.md) |
| Observability | OpenTelemetry C++ + OTLP + Prometheus | OTEL-first across stacks | [ENG-5.5](laws/engineering/eng-5-devops.md) |

**Brownfield exception (all concerns):** If a repository cannot adopt a default, document the current tool/constraint, map an equivalent control, and treat migration as phased adoption with milestones.

### Tool Selection Rationale

Each tool default above was selected based on the following criteria. These rationale snippets are provided so that humans and AI agents can understand the intent behind each selection.

| Tool | Selection Rationale | Confidence |
|------|-------------------|------------|
| `clang-tidy` | Compiler-adjacent diagnostics with fast CI feedback; catches bugs, style, and modernization opportunities in a single pass | High — code-evidenced from existing avatar patterns |
| CodeQL | Mature security-focused query analysis with deep inter-procedural analysis; GitHub-native integration for PR gating | High — public-benchmark (CodeQL security coverage data) |
| Dependabot | GitHub-native CVE scanning with automated PR remediation; low operational overhead for `vcpkg.json` and `conanfile` dependencies | High — code-evidenced from existing GitHub workflows |
| OWASP ZAP | Widely adopted baseline DAST with practical automation; suitable for web-exposed C++ services without heavy custom setup | Medium — public-benchmark (OWASP project adoption data) |
| HashiCorp Vault | Platform-flexible managed secret storage; supports rotation, audit logging, and multi-cloud deployment patterns | High — stakeholder-reported (ops team conventions) |
| Terraform | Industry-standard multi-cloud IaC with mature policy tooling (OPA, Sentinel); strong ecosystem and drift detection | High — code-evidenced from existing repo IaC patterns |
| `llvm-cov` | Native LLVM toolchain compatibility; stable LCOV/Cobertura reporting formats for CI dashboard integration | High — public-benchmark (LLVM project tooling) |
| OpenTelemetry | Aligns with existing OTEL-first patterns across stacks; enables consistent trace/metric/log correlation | High — code-evidenced from opentelemetry-python avatar pattern |

---

## See Also

- [Testing & CI Quality](ref-testing-ci.md)
- [Advanced C++ Patterns](ref-advanced-cpp.md)


---

## See Also

- [Build Packages and Reproducible Builds](ref-build-packages.md)
