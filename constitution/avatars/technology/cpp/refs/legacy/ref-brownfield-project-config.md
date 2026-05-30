---
cpp_version_min: 98
cpp_version_note: >-
  Brownfield project configuration starting from C++98/03 build systems.
avatar: cpp
---

# C++ Avatar Reference: Brownfield Project Configuration

---

## Compiler Flag Progression During Migration

Per [ENG-5.2](laws/engineering/eng-5-devops.md) (CI/CD Pipeline Law), compiler warning enforcement must be automated in CI. Adopt warning flags incrementally — do not enable `-Werror` on a legacy codebase with thousands of warnings. Each phase must reach zero warnings before the next phase is enabled.

| Phase | Flags | Purpose |
|---|---|---|
| 1. Baseline | `-Wall` (no `-Werror`) | Measure warning count without breaking the build |
| 2. Tighten | `-Wall -Wextra` (no `-Werror`) | Surface more issues; still non-blocking |
| 3. Enforce core | `-Wall -Wextra -Werror` | Core warnings are now build errors |
| 4. Pedantic | Add `-Wpedantic` | ISO compliance; catches GCC/Clang extensions |
| 5. Conversion safety | Add `-Wconversion -Wsign-conversion` | Critical for fare/weight/distance calculations |
| 6. Full governance | Full flag set per this guidance | All warnings as errors; matches greenfield standard |

**Rules:**
- Track warning count in CI — trend must be monotonically decreasing
- Each phase gate is: zero warnings at the current phase level
- New code in a brownfield repo MUST compile clean at Phase 6 even if the legacy code is at Phase 2
- Use per-target compile options in CMake to enforce different flag levels:
```cmake
target_compile_options(legacy_module PRIVATE -Wall -Wextra)           # Phase 2
target_compile_options(new_module PRIVATE -Wall -Wextra -Wpedantic -Werror -Wconversion)  # Phase 6
```

## Sanitizer Availability by Compiler Version

Per [ENG-6.1](laws/engineering/eng-6-security.md) (Security by Design), runtime sanitizers must be used in CI where available. The following matrix shows sanitizer availability by compiler:

| Sanitizer | GCC min | Clang min | MSVC |
|---|---|---|---|
| AddressSanitizer (ASan) | 4.8 | 3.1 | 19.28 (VS 2019 16.9, partial) |
| UndefinedBehaviorSanitizer (UBSan) | 4.9 | 3.3 | 19.28 (partial) |
| ThreadSanitizer (TSan) | 5.1 | 3.2 | Not supported |
| MemorySanitizer (MSan) | Not supported | 3.3 | Not supported |

### Fallback Policies for Legacy Toolchains
- **ASan/UBSan unavailable** (GCC < 4.9, older MSVC): Use Valgrind memcheck + UBSan manual review
- **TSan unavailable** (MSVC, GCC < 5.1): Document data race risk; use `-Wthread-safety` (Clang) where possible; prioritize code review for concurrency
- **All sanitizers unavailable** (very old toolchains): Mandatory Valgrind CI gate + static analysis (cppcheck as clang-tidy fallback)

**Rule:** Brownfield projects MUST document which sanitizers are active and which have approved fallbacks in their `MODERNIZATION_PLAN.md`.


---


---

## Load Planning Domain — IOC_ALP (PCLoadPlan)

> Per [ENG-6.7](laws/engineering/eng-6-security.md) (Audit Trail Law) and
> [ENG-6.1](laws/engineering/eng-6-security.md) (Security by Design), all
> airline load planning computations must be auditable, envelope-validated,
> and compliant with FAA MEL/weight-and-balance regulations.

IOC_ALP (PCLoadPlan) is a ~25-year-old MFC Windows desktop application
used by the Integrated Operations Center (IOC) to manage aircraft weight,
balance, and cargo loading for American Airlines flights.

### Domain Concepts

| Concept | Description |
|---------|-------------|
| **ZFW (Zero Fuel Weight)** | Total aircraft weight minus fuel load; must stay within manufacturer envelope for each aircraft type |
| **CG (Center of Gravity)** | Longitudinal balance point; must stay within forward/aft limits throughout flight |
| **MEL (Minimum Equipment List)** | FAA-approved list of inoperative systems that allow dispatch; IOC_ALP tracks MEL items per flight |
| **Belly Cargo** | Revenue cargo loaded in lower deck; ZFW envelope includes belly load |
| **CSAPI (Sabre)** | GDS integration via `AACCSAPI.lib` — fetches seat maps, reservations, and passenger weights |
| **FlightPhase** | State machine tracking flight lifecycle: PRE_DEPARTURE → BOARDING → CLOSED → IN_FLIGHT → ARRIVED |
| **FAA 7-Week History** | Regulatory requirement: retain load planning records for 7 weeks per FAA Order 8900.1 |

### ZFW / CG Compliance Pattern

```cpp
// alpsource/CFlight.cpp
bool CFlight::isValidZFW() const {
    // ZFW envelope loaded from aircraft type table at startup
    return zfw_ >= envelope_.minZFW() && zfw_ <= envelope_.maxZFW();
}

double CFlight::computeCG() const {
    // CG = (sum of moment arms * weights) / total weight
    double totalMoment = cargoMoment_ + paxMoment_ + crewMoment_;
    double totalWeight = zfw_;
    return (totalWeight > 0.0) ? totalMoment / totalWeight : 0.0;
}
```

### MEL Compliance Governance

Per [ENG-6.1](laws/engineering/eng-6-security.md): every MEL item must be
validated against the current dispatch release before boarding is closed.
IOC_ALP calls `AACCSAPI.lib` to retrieve MEL status from Sabre before
allowing `FlightPhase::CLOSED` transition.

### FAA Audit Retention

Per [ENG-6.7](laws/engineering/eng-6-security.md): load planning records
(ZFW, CG, MEL items, CSAPI transaction IDs) must be persisted for ≥7 weeks.
`CDataManager` writes to an append-only audit file on `FlightPhase::CLOSED`.

### Sabre CSAPI Integration Pattern

```cpp
// alpsource/CHostRequestManager.cpp
// CSAPI calls go through CHostException hierarchy (see host-exception-safety example)
RCPtr<CFlightData> CDataManager::fetchFlightData(const std::string& flightId) {
    CFlightDataRequest req(flightId);
    try {
        hostConnection_->sendRequest(&req);       // AACCSAPI.lib call
        return req.getFlightData();               // returns RCPtr<CFlightData>
    } catch (CHostException& e) {
        auditLog_.error("CSAPI_ERR flt=%s code=%d", flightId.c_str(), e.getCode());
        throw;
    }
}
```

---

---

## MFC Windows Brownfield Governance (IOC_ALP)

> Per [ENG-1.4](laws/engineering/eng-1-core-principles.md) (Brownfield
> Migration Law) and [ENG-2.3](laws/engineering/eng-2-architecture.md) (Vertical
> Slice Architecture), modernizing MFC C++98 code requires explicit ownership
> boundaries and characterization tests before any structural change.

IOC_ALP uses three custom infrastructure patterns that predate C++11 and must
be respected as ownership contracts at every vertical slice boundary.

### RCPtr / RCObject — Reference-Counted Ownership

`RCPtr<T>` is the primary ownership primitive (~650 usages). Any new code
that receives an `RCPtr<T>` must copy the value into a plain struct at the
slice boundary — never store or return `RCPtr<T>` from new-slice code.

```cpp
// CORRECT: copy at boundary, new slice holds plain value
struct FlightSnapshot {
    std::string flightNumber;
    double zfw;
};
FlightSnapshot snapshotFrom(RCPtr<CFlight> f) {
    return { f->getFlightNumber(), f->getZFW() };
}
```

### Observer / Observable — Event Propagation

`CObserver` / `CObservable` is the primary event bus. New code must not
introduce `std::function` callbacks alongside `CObserver` — creates two
notification paths and silent fan-out bugs.

```cpp
// CORRECT: extend CObserver for new listeners
class CLoadStatusObserver : public CObserver {
public:
    void update(CObservable* src, void* hint) override {
        CFlightPhase* phase = static_cast<CFlightPhase*>(hint);
        if (phase->isClosed()) notifyLoadComplete();
    }
};
```

### Command / Parser / Record / Request Quad

Every Sabre CSAPI data operation uses a four-class quad:
- `*Command` — orchestrates the operation
- `*Parser`  — transforms raw CSAPI response into domain objects
- `*Record`  — value-object holding parsed fields
- `*Request` — encapsulates CSAPI request parameters and lifecycle

New operations **must** follow this quad or document a divergence in the
vertical slice spec. Partial quads (e.g., Command without Parser) create
untestable parsing logic inside the Command.

### MFC Threading Constraints

Per [ENG-6.1](laws/engineering/eng-6-security.md): all UI updates must
occur on the main MFC thread. Background worker threads (in `Thread Classes/`)
must post results via `PostMessage` — direct MFC control access from a worker
thread causes heap corruption in the MFC document/view architecture.

```cpp
// CORRECT: post result to UI thread
workerThread_->PostThreadMessage(WM_LOAD_COMPLETE, (WPARAM)&result, 0);
// WRONG: touching UI from worker thread — silent heap corruption
// flightGrid_->SetItemText(row, col, value.c_str());
```

---

---

## IOC_ALP Anti-Pattern Catalog

> Per [ENG-3.1](laws/engineering/eng-3-code-quality.md) (Complexity Law) and
> [ENG-6.1](laws/engineering/eng-6-security.md) (Security by Design), the
> following anti-patterns observed in IOC_ALP must be triaged before modernizing
> any vertical slice that touches the affected code.

### ALP-AP-1: Flight.h God Class (945 Lines)

`CFlight` accumulates ZFW, CG, MEL, cargo, pax, phase, and Sabre data —
945 lines with no cohesion boundary. New code must not add methods to it.
**Remedy:** Strangler Fig — extract `FlightWeight`, `FlightCargo`, `FlightPhase`
as separate collaborators; each new slice gets its own class.

### ALP-AP-2: Macro Abuse in Globals.h

`Globals.h` defines 80+ `#define` macros for domain constants and string
literals. Macros bypass namespaces and type checking.
**Remedy:** Replace with `constexpr` / typed `enum class` in a proper namespace.
See [ENG-3.1](laws/engineering/eng-3-code-quality.md) for complexity governance.

### ALP-AP-3: Mixed Ownership (RCPtr + raw pointer)

Some files hold `RCPtr<CFlight>` in one field and a raw `CFlight*` in another
for the same object — ownership is ambiguous and double-free-prone.
**Remedy:** Per [ENG-6.1](laws/engineering/eng-6-security.md): pick one
ownership model per class. In new slices, always copy to value at RCPtr boundary.

### ALP-AP-4: #pragma warning(disable:4786)

`#pragma warning(disable:4786)` suppresses "identifier too long" (MSVC < VS2005
debug info limit). Masking warnings hides symbol table truncation.
**Remedy:** Remove pragma; shorten template-heavy type aliases to under 256 chars.

### ALP-AP-5: CObservable::notify Without Null Guard

Several `notify()` call sites dereference `hint` directly without checking
whether the observer list has stale (already-deleted) pointers.
**Remedy:** Observer list must use `RCPtr<CObserver>` not raw pointer, or use
a weak-reference sentinel. Characterization test before touching.

### ALP-AP-6: CRITICAL_SECTION Without RAII Wrapper

Windows `CRITICAL_SECTION` lock/unlock is manual — missed `LeaveCriticalSection`
on early return paths causes deadlocks in the load planning UI.
**Remedy:** Wrap in an RAII guard:

```cpp
struct CSLock {
    explicit CSLock(CRITICAL_SECTION& cs) : cs_(cs) { EnterCriticalSection(&cs_); }
    ~CSLock() { LeaveCriticalSection(&cs_); }
private:
    CRITICAL_SECTION& cs_;
};
```

### Anti-Pattern Triage Priority

| Anti-Pattern | Risk Level | Effort | Recommended Phase |
|-------------|-----------|--------|------------------|
| ALP-AP-3: Mixed ownership | 🔴 Critical | Medium | Phase 1 — before adding any new slice |
| ALP-AP-6: CRITICAL_SECTION without RAII | 🔴 Critical | Low | Phase 1 — deadlock risk |
| ALP-AP-5: Null observer dereference | 🟠 High | Low | Phase 1 — RAII observer list |
| ALP-AP-2: Macro abuse | 🟠 High | Medium | Phase 2 — constexpr migration |
| ALP-AP-4: #pragma warning disable | 🟡 Medium | Low | Phase 2 — fix identifiers |
| ALP-AP-1: God class CFlight | 🟡 Medium | Very High | Phase 3 — Strangler Fig |

---
## See Also

- [Migration Playbooks](ref-migration-playbooks.md)
- [Legacy Code Navigation](ref-legacy-navigation.md)


---

## See Also

- [Brownfield Adoption](ref-brownfield-adoption.md)
