---
law_id: ENG-7.1
cpp_version_min: 11
avatar: cpp
title: Failure Handling Law — C++ Patterns
tokens: ~460
---

# ENG-7.1 Failure Handling Law — C++ Patterns

**Law:** ENG-7.1 (Failure Handling Law)  
**Avatar:** `avatars/technology/cpp/`

---

## Core Rule

Every failure mode MUST be handled explicitly — no silent swallows, no unhandled
exceptions crossing module boundaries, no unset-flag surprises.
The system must always be in a *known* state after a failure, even if that state is "degraded."

---

## COMPLIANT Patterns

### 1. Explicit Degraded-State Signalling

```cpp
enum class ServiceState { Healthy, Degraded, Failed };

class CrewScheduler {
    ServiceState state_ = ServiceState::Healthy;
    std::string  failure_reason_;
public:
    ServiceState state()          const noexcept { return state_; }
    std::string  failure_reason() const noexcept { return failure_reason_; }

    CrewError assign(FlightId f, CrewId c) noexcept {
        if (state_ == ServiceState::Failed) {
            return CrewError::ServiceUnavailable;
        }
        auto result = roster_.assign(f, c);
        if (result != CrewError::None) {
            state_          = ServiceState::Degraded;
            failure_reason_ = "roster assign failed";
        }
        return result;
    }
};
```

### 2. Circuit Breaker (half-open retry pattern)

```cpp
class CircuitBreaker {
    int  failure_count_ = 0;
    bool open_          = false;
    static constexpr int kThreshold = 5;
public:
    bool allow_request() noexcept {
        return !open_;
    }
    void record_failure() noexcept {
        if (++failure_count_ >= kThreshold) open_ = true;
    }
    void record_success() noexcept {
        failure_count_ = 0;
        open_          = false;
    }
};
```

### 3. Exception Boundary at Integration Layer

```cpp
// noexcept boundary — converts exceptions from third-party to error codes
CrewError call_legacy_api(FlightId f) noexcept {
    try {
        legacy::assign(f.value());
        return CrewError::None;
    } catch (const legacy::ApiException& e) {
        spdlog::error("legacy_api_failed", spdlog::arg("msg", e.what()));
        return CrewError::ExternalFailure;
    } catch (...) {
        spdlog::error("legacy_api_unknown_failure");
        return CrewError::ExternalFailure;
    }
}
```

---

## NON-COMPLIANT Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| `catch (...) {}` — empty catch | Failure silently lost | Log + return error code |
| Unhandled exception crossing module boundary | Undefined behaviour at caller | Wrap with `noexcept` boundary |
| Boolean flag returned without checking | Caller may ignore silently | Use `[[nodiscard]]` or `enum class` |
| Service continues after unrecoverable failure | Corrupt state served to callers | Transition to `Failed` state |

---

## CWR Brownfield Path

CWR C++03/11 constraints:
- `[[nodiscard]]` requires C++17 — use wrapper macro for C++03:
  `#define NODISCARD __attribute__((warn_unused_result))`
- State machine pattern above compiles in C++03 (no lambdas, no `auto`)
- Add `ServiceState` enum to all long-lived domain objects as a first step

## Edge Cases & Warnings

| Scenario | Risk | Safe Approach |
|----------|------|---------------|
| Cascading partial degradation triggers full shutdown | Service enters `DEGRADED` on the first error, then a second unrelated error causes full `SHUTDOWN` before the first issue self-heals; over-triggers downtime | Use a per-dependency health flag rather than a single global state; only escalate to `SHUTDOWN` when the primary data path is fully unavailable |
| Health-check endpoint returns 200 under load spike despite internal queue saturation | External load balancer routes traffic to a saturated node; degradation is invisible to the orchestrator | Include queue depth and thread pool utilisation in the health-check response body; use a `/readiness` vs `/liveness` split |
| Degraded-mode state persists after underlying dependency recovers | Service stays in `DEGRADED` indefinitely because the recovery path is not exercised; silent capacity loss | Add a scheduled recovery probe (e.g., every 30 s) that attempts the downstream call and transitions back to `HEALTHY` on success |
