---
law_id: ENG-6.1
cpp_version_min: 98
avatar: cpp
context: brownfield-mfc-exception-hierarchy
---

# [ENG-6.1](laws/engineering/eng-6-security.md): Host Exception Safety (IOC_ALP / CALPException Hierarchy)

**Avatar:** C++ (Brownfield MSVC/MFC — IOC_ALP PCLoadPlan)
**Pattern:** 15-tier exception hierarchy rooted at CALPException

## Context

IOC_ALP bridges to Sabre CSAPI (GDS/reservations) through AACCSAPI.lib.
Host calls can fail with network errors, authentication failures, seat-map
corruption, or timeout. The codebase defines a 15+ type exception hierarchy:

```
std::exception
  CALPException         // base — message + error code
    CALPFileException   // file I/O failures
    CHostException      // all Sabre/GDS host errors
      CAuthException
      CTimeoutException
      CSegmentException
      ... (10+ domain types)
```

## NON-COMPLIANT: Catch-All Swallows Domain Signal

```cpp
// WRONG: swallowing domain exception loses Sabre error code + retry signal
try {
    hostConnection_->sendRequest(flightRequest_);
} catch (...) {
    // error swallowed — no logging, no FAA audit trail, no retry decision
    return false;
}
```

## COMPLIANT: Layered Catch with Audit and Retry

```cpp
// alpsource/HostRequestManager.cpp
bool CHostRequestManager::sendWithRetry(CHostRequest* req, int maxRetries) {
    for (int attempt = 0; attempt < maxRetries; ++attempt) {
        try {
            hostConnection_->sendRequest(req);
            return true;
        } catch (CTimeoutException& e) {
            // Transient — retry with backoff; log per ENG-6.7
            auditLog_.warn("TIMEOUT attempt=%d code=%d msg=%s",
                           attempt, e.getCode(), e.getMessage());
            Sleep(500 * (attempt + 1));
        } catch (CAuthException& e) {
            // Non-retryable — escalate immediately
            auditLog_.error("AUTH_FAIL code=%d msg=%s",
                            e.getCode(), e.getMessage());
            throw;
        } catch (CHostException& e) {
            auditLog_.error("HOST_ERR code=%d msg=%s",
                            e.getCode(), e.getMessage());
            return false;
        } catch (CALPException& e) {
            auditLog_.error("ALP_ERR code=%d msg=%s",
                            e.getCode(), e.getMessage());
            return false;
        }
    }
    return false;
}
```

## Safety Rules for CALPException Hierarchy

1. **Never catch `...`** without re-throw — always log domain exception type.
2. **Catch most-derived first** (CTimeoutException before CHostException).
3. **Non-retryable errors re-throw** — let caller decide escalation.
4. **Every catch writes to audit log** per
   [ENG-6.7](../../laws/engineering/eng-6-security.md).

Per [ENG-6.1](../../laws/engineering/eng-6-security.md): all host errors must
surface domain type, error code, and audit trail entry — never swallow.

## Edge Cases & Warnings

- **Catch order must be most-derived first** — `CTimeoutException` must appear before `CHostException`. If `CHostException` comes first and `CTimeoutException` derives from it, timeouts are silently caught as generic host errors, losing the timeout code in the audit log.
- **`catch (...)` without re-throw hides bugs** — A bare `catch (...)` that only logs discards the exception type, masking programming errors in development. Only use as a last-resort safety net, always with a re-throw or an explicit `UNKNOWN_ERROR` audit entry.
- **Non-retryable errors must not be swallowed** — Catching a `FATAL` `CHostException` and returning `false` without re-throwing allows the caller to retry against a permanently failed connection, causing retry storms.
