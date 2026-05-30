---
law_id: ENG-6.1
cpp_version_min: 03
cpp_version_note: >-
  const char* lifetime traps apply from C++98/03 onwards — std::string and
  .c_str() are both C++98 features. These traps parallel std::string_view
  lifetime traps exactly; see ENG-6.1-string-view-lifetime.md when C++17
  is available.
avatar: cpp
---

# [ENG-6.1](laws/engineering/eng-6-security.md): `const char*` Lifetime Traps

`const char*` obtained from `std::string::c_str()` is valid **only as long as
the string object it came from is alive and unmodified**. Storing or returning
that pointer past the string's lifetime causes **undefined behavior** — typically
a read of freed memory that produces garbage or a crash at an unpredictable
distance from the root cause.

Per [ENG-6.1](laws/engineering/eng-6-security.md) (Security by Design Law),
lifetime-unsafe code is a resource-management defect.

## COMPLIANT

### Store ownership; expose `.c_str()` only at the point of use

```cpp
// C++03 — flight number is stored as std::string; .c_str() produced inline
class FlightLeg {
public:
    explicit FlightLeg(const std::string& flight_num)
        : flight_num_(flight_num) {}       // string owns the buffer

    // COMPLIANT: .c_str() lives only as long as the call expression
    void log() const {
        ::fprintf(stderr, "leg: %s\n", flight_num_.c_str());
    }

    // COMPLIANT: return std::string, not const char*
    const std::string& flight_num() const { return flight_num_; }

private:
    std::string flight_num_;               // owner
};
```

### Lifetime-documented `const char*` parameter contract

Sometimes a C API requires `const char*`. Document the lifetime contract
explicitly so callers cannot accidentally pass a dangling pointer:

```cpp
// COMPLIANT: caller guarantees 'path' outlives write_log_entry()
// — documented contract; function does not store the pointer
void write_log_entry(const char* path, int level) {
    // 'path' used and discarded within this call — never stored
    ::syslog(level, "aa-ground: %s", path);
}

// Correct call site — string outlives the function call
void schedule_update(const std::string& config_path) {
    write_log_entry(config_path.c_str(), LOG_INFO);
}
```

## NON-COMPLIANT

### Returning `.c_str()` of a local `std::string`

```cpp
// DANGLING — local string destroyed at return; pointer is immediately invalid
const char* get_route_code(int flight_id) {
    std::string code = build_route_code(flight_id);  // local string
    return code.c_str();   // NON-COMPLIANT: pointer outlives 'code'
}

// Caller reads undefined memory
const char* route = get_route_code(4820);
::printf("%s\n", route);   // undefined behavior — 'code' is gone
```

**Fix:** return `std::string` by value; let the caller manage lifetime.

```cpp
std::string get_route_code(int flight_id) {
    return build_route_code(flight_id);   // COMPLIANT
}
```

### Storing a pointer from a temporary `std::string` expression

```cpp
// DANGLING — temporary destroyed at the semicolon
const char* label = std::string("AA" + std::to_string(gate)).c_str();
// NON-COMPLIANT: 'label' is a dangling pointer on the very next line
::puts(label);   // undefined behavior
```

```cpp
// Also DANGLING — make_label() returns by value; temporary destroyed at ';'
const char* p = make_label(flight).c_str();   // NON-COMPLIANT
```

**Fix:** store the `std::string` in a named variable; take `.c_str()` inline:

```cpp
std::string label = "AA" + std::to_string(gate);   // COMPLIANT
::puts(label.c_str());
```

### Storing `.c_str()` across a `std::string` mutation

```cpp
const char* name = airline_name.c_str();   // valid here
airline_name += " International";           // reallocation may occur
::printf("%s\n", name);   // NON-COMPLIANT: name may be dangling after append
```

Any operation that may reallocate the string's internal buffer (`+=`, `append`,
`resize`, `reserve`, `assign`, …) invalidates all outstanding `const char*`
pointers from that string.

## Migration Note — `std::string_view` (C++17)

`std::string_view` shares **exactly the same lifetime rules** as `const char*`.
The traps above apply equally: do not store a `string_view` into a string that
may be destroyed or mutated. When C++17 is available, prefer `std::string_view`
for read-only string parameters — it avoids copies and works with both `char*`
and `std::string` callers — but always respect its lifetime contract.

See [`ENG-6.1-string-view-lifetime.md`](ENG-6.1-string-view-lifetime.md) for
the C++17 `string_view` version of these traps.

## Edge Cases & Warnings

Per [ENG-6.1](laws/engineering/eng-6-security.md) (Security by Design Law),
all edge cases below are undefined behavior — not implementation-defined.

- **`std::string` small-string optimisation (SSO)** — Many implementations store
  short strings inline in the `std::string` object without heap allocation. SSO
  makes dangling-pointer bugs *harder to detect*: the dangling pointer may appear
  to work in tests because the on-stack bytes are not immediately overwritten.
  Never rely on this; sanitizers (ASan, MSan) catch it.
- **Reallocation on any mutation** — `operator+=`, `append()`, `resize()`,
  `push_back()`, `reserve()`, and `assign()` may all reallocate. Treat any
  `const char*` from `.c_str()` as invalidated after any mutation of the source
  string, even if you believe the new content fits within the old capacity.
- **Returning via output parameter** — passing `const char**` as an output param
  and writing `*out = local_string.c_str()` is the same dangling-pointer bug.
- **`std::ostringstream` intermediary** — `oss.str().c_str()` is a common trap:
  `oss.str()` returns a temporary `std::string`; taking `.c_str()` of that
  temporary is undefined behavior at the semicolon.
- **Thread safety** — a `const char*` obtained from one thread becomes invalid
  if another thread mutates the owning `std::string` concurrently, even before
  the string goes out of scope.

