---
law_id: ENG-6.4
cpp_version_min: 17
cpp_version_note: >-
  Uses C++17 string_view and structured bindings for PII-safe APIs. Transitional teams: use const std::string&; brownfield: explicit null-checks before access.
avatar: cpp
---

# [ENG-6.4](laws/engineering/eng-6-security.md): Data Protection — C++ Examples

## The Rule

PII (personally identifiable information) **must be encrypted at rest** and **scrubbed from memory** after use. Access to raw PII requires audited accessors — no public fields.

**Note:** The `volatile` cast in `secure_zero` prevents the compiler from optimizing away the memset. In Java, the GC handles memory — in C++, you must explicitly scrub sensitive data. Prefer `memset_s` (C11) or platform APIs (`SecureZeroMemory` on Windows) when available.

## When to Use

Apply to **any data** containing passenger names, email addresses, passport numbers, payment card details, frequent flyer IDs, or other PII. This includes in-memory representations, not just database storage.

## COMPLIANT: PII Encapsulation with Access Control

```cpp
#include <cstring>

class PassengerRecord {
public:
    static PassengerRecord create(std::string name, std::string passport) {
        return PassengerRecord{std::move(name), std::move(passport)};
    }

    std::string_view name() const { return name_; }

    // why: passport only accessible via audited accessor — masked by default
    std::string masked_passport() const {
        return std::string(passport_.size() - 4, '*') + passport_.substr(passport_.size() - 4);
    }

    // why: scrub PII from memory when no longer needed
    ~PassengerRecord() {
        secure_zero(passport_);
        secure_zero(name_);
    }

private:
    PassengerRecord(std::string n, std::string p) : name_(std::move(n)), passport_(std::move(p)) {}
    std::string name_;
    std::string passport_;

    // why: volatile prevents compiler from optimizing away the memset
    static void secure_zero(std::string& s) {
        volatile char* p = s.data();
        std::memset(const_cast<char*>(static_cast<const volatile char*>(p)), 0, s.size());
        s.clear();
    }
};
```

## NON-COMPLIANT: Exposed PII

```cpp
struct PassengerRecord {
    std::string name;              // ❌ public — logged, serialized, leaked without audit
    std::string passport_number;   // ❌ directly accessible — no masking, no scrubbing
};
// ❌ PII persists in memory after object is destroyed — core dump exposes data
```

## Edge Cases & Warnings

| Scenario | Guidance |
|----------|----------|
| Compiler optimizes away `memset` | Standard `memset` on a buffer that is never read again **may be optimized away**. Use `volatile` pointer cast, `SecureZeroMemory` (Windows), or C11 `memset_s`. |
| `std::string` SSO (Small String Optimization) | Short strings may live on the stack, not heap. `secure_zero` must handle both — `s.data()` returns the correct pointer regardless. |
| PII in logs | Never log raw PII. Always pass through masking functions before any log call (see ENG-6.7-structured-logging). |
| Moved-from PII strings | After `std::move`, the source string may retain data in SSO buffer. Explicitly scrub the source after move. |
