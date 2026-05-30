---
skill:
  id: skill-cpp-compliance-rating
  name: "C++ Constitution Compliance Rating"
  category: platform-engineering
  version: "1.0.0"
  avatar: cpp

laws:
  implements:
    - id: ENG-4.1
      reason: "D1 Test Governance dimension measures TDD compliance"
    - id: ENG-6.1
      reason: "D2 Security Posture and D6 Memory Safety dimensions"
    - id: ENG-6.7
      reason: "D5 Observability & Audit dimension measures audit trail compliance"
  references:
    - id: ENG-5.2
      reason: "D3 CI/CD Pipeline dimension"
    - id: ENG-2.1
      reason: "D4 Architecture & Design dimension"
    - id: ENG-3.1
      reason: "D4 Architecture & Design dimension (complexity)"
    - id: ENG-6.7
      reason: "D5 Observability & Audit dimension"
    - id: ENG-4.1
      reason: "D10 Regulatory Compliance dimension"

triggers:
  phrases:
    - "C++ compliance rating"
    - "C++ compliance score"
    - "C++ codebase rating"
    - "rate this C++ codebase"
    - "C++ constitution compliance"
    - "C++ governance score"
    - "assess C++ codebase quality"
    - "C++ deployment readiness"

followed_by:
  - skill-cpp-legacy-code-navigation
  - skill-cpp-legacy-modernization
  - skill-27-constitution-compliance
---

# C++ Constitution Compliance Rating

## Purpose

Produce a quantitative, reproducible 0–10 compliance score for any C++ codebase governed by the Hangar AI Constitution. The score enables deployment gating, remediation tracking, and cross-tier normalization.

## Assessment Procedure

### Step 1: Determine Standard Tier

Inspect `CMakeLists.txt` for `CMAKE_CXX_STANDARD` or `target_compile_features()`:
- T5 (C++23) → multiplier 1.00
- T4 (C++20) → multiplier 1.00
- T3 (C++14/17) → multiplier 0.95
- T2 (C++11) → multiplier 0.90
- T1 (C++98/03) → multiplier 0.85

### Step 2: Score Each Dimension (0–10)

| # | Dimension | Weight | Veto? | What to Inspect |
|---|-----------|--------|-------|-----------------|
| D1 | Test Governance | 15% | ≥4 | tests/ directory, CI test jobs, coverage config |
| D2 | Security Posture | 15% | ≥4 | Sanitizer flags in CMake/CI, raw pointer count |
| D3 | CI/CD Pipeline | 10% | — | CI config files, deployment automation |
| D4 | Architecture | 10% | — | Module boundaries, complexity metrics |
| D5 | Observability | 12% | ≥3 | Logging framework, audit trail, health checks |
| D6 | Memory Safety | 12% | ≥3 | Smart pointer usage, RAII patterns, ASan results |
| D7 | Dependencies | 6% | — | Package manager config, license file |
| D8 | Documentation | 6% | — | AGENTS.md, README.md, API docs |
| D9 | Modernization | 6% | — | Standard tier, compiler version, migration plan |
| D10 | Regulatory | 8% | ≥3 | Compliance artifacts, traceability matrix |

### Step 3: Calculate Composite Score

```
composite = Σ(dimension_score × weight) × tier_multiplier
```

### Step 4: Apply Veto Rules

If D1 < 4, D2 < 4, D5 < 3, D6 < 3, or D10 < 3 → cap grade at Non-Compliant.

### Step 5: Assign Grade

| Grade | Range | Action |
|-------|-------|--------|
| Exemplary | 8.0–10.0 | Production-ready |
| Compliant | 6.0–7.9 | Production-ready with monitoring |
| Remediation Required | 4.0–5.9 | 90-day remediation plan required |
| Non-Compliant | 0.0–3.9 | Production deployment blocked |

## Report Template

```
## Compliance Rating Report
- **Repository:** {repo_name}
- **Standard Tier:** T{tier} ({standard})
- **Date:** {date}

### Dimension Scores
| Dimension | Score | Notes |
|-----------|-------|-------|
| D1 Test Governance | {score} | {notes} |
| ... | ... | ... |

### Composite Score: {composite}
### Grade: {grade}
### Veto Violations: {veto_list or "None"}
### Top Remediation Priorities:
1. {priority_1}
2. {priority_2}
3. {priority_3}
```

## Governance Gate

- Rating must be performed before production deployment
- Remediation Required repositories need a documented 90-day plan
- Non-Compliant repositories are blocked from production
- Re-rating required after significant remediation work
- Full specification: [compliance-rating-system.md](../../avatars/technology/cpp/compliance-rating-system.md)
