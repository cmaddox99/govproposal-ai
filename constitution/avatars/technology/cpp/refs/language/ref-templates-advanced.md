---
id: ref-templates-advanced
cpp_version_min: 11
cpp_version_note: >-
  Type traits/tag dispatch (C++11); if constexpr (C++17); NTTPs class-type/
  float (C++20); template lambda / consteval lambda (C++20).
  Overflow from ref-templates-metaprogramming.md (at capacity).
avatar: cpp
---

# Advanced Templates and Metaprogramming (Overflow)

Per [ENG-3.1](laws/engineering/eng-3-code-quality.md), all template
metaprogramming must be justified by measurable benefit over simpler
alternatives. Prefer concepts (C++20) over SFINAE for all new code.

---

## Type Traits Reference (C++11)

Per [ENG-3.1](laws/engineering/eng-3-code-quality.md), prefer concepts (C++20)
for new code; use type traits for `constexpr if` branches and C++11/14 compat.

| Trait | Purpose |
|---|---|
| `std::is_integral_v<T>` | True for int, char, bool, etc. |
| `std::remove_cv_t<T>` | Strip const/volatile |
| `std::remove_reference_t<T>` | Strip & or && |
| `std::decay_t<T>` | Array→pointer, function→ptr, remove cv-ref |
| `std::conditional_t<B,T,F>` | Ternary type selection |
| `std::enable_if_t<B,T>` | SFINAE gate (prefer concepts in C++20) |

Custom trait pattern:

```cpp
// has_serialize_v<T> — true if T has a .serialize() member
template<typename T, typename = void>
struct has_serialize : std::false_type {};

template<typename T>
struct has_serialize<T, std::void_t<decltype(std::declval<T>().serialize())>>
    : std::true_type {};

template<typename T>
inline constexpr bool has_serialize_v = has_serialize<T>::value;
```

Trait composition (C++17):

```cpp
// ✅ All conditions must hold
template<typename T>
using IsSerializableInt = std::conjunction<std::is_integral<T>, has_serialize<T>>;
// ✅ negation, disjunction available similarly
```

Governance: prefer `if constexpr` or concepts for new code; use `enable_if`
only in brownfield C++11/14 compatibility layers.

---

## Tag Dispatching (C++11)

Per [ENG-3.1](laws/engineering/eng-3-code-quality.md), use tag dispatch only
in brownfield C++11/14 code; migrate to `if constexpr` (C++17) or concepts (C++20).

Dispatch on `true_type`/`false_type` for brownfield code without C++17/20:

```cpp
template<typename T>
void encode_impl(T val, std::true_type  /* integral */) { encode_int(val); }
template<typename T>
void encode_impl(T val, std::false_type /* other    */) { encode_generic(val); }

template<typename T>
void encode(T val) {
    encode_impl(val, std::is_integral<T>{});  // ✅ zero-overhead dispatch
}
```

Migration path: tag dispatch → `if constexpr` (C++17) → concept overloads (C++20).

---

## Advanced Concepts (C++20)

Per [ENG-3.1](laws/engineering/eng-3-code-quality.md), concepts replace
SFINAE — they produce readable diagnostics and support subsumption-based overload resolution.

Compound `requires`-expression:

```cpp
template<typename T>
concept Serializable = requires(T t) {
    { t.serialize() } -> std::convertible_to<std::string>;
    { T::version()  } -> std::same_as<int>;
};
```

**Subsumption**: the compiler selects the most constrained overload.
To subsume `std::copyable`, define `Serializable` in terms of it with `&&`:

```cpp
template<typename T>
concept Serializable = std::copyable<T> && requires(T t) {
    { t.serialize() } -> std::convertible_to<std::string>;
    { T::version()  } -> std::same_as<int>;
};

void write(std::copyable auto x);      // less constrained
void write(Serializable auto x);       // ✅ subsumes copyable — preferred overload
```

Without the `std::copyable<T> &&` prefix, both overloads are unordered and
calling `write` with a `Serializable` argument would be **ambiguous**. The `&&`
conjunction means `Serializable` _includes_ the copyable constraint, making it
strictly more constrained and preferred by overload resolution per [temp.constr.order].

Auto-concept parameters: `void f(std::integral auto x)` — concise and
equivalent to `template<std::integral T> void f(T x)`.

Concept debugging:

```cpp
static_assert(Serializable<FlightId>,  // ✅ human-readable failure message
    "FlightId must satisfy Serializable — add serialize() and version()");
```

---

## Nontype Template Parameters — NTTPs (C++17/20)

Per [ENG-3.1](laws/engineering/eng-3-code-quality.md), NTTPs encode
compile-time configuration without macros or global constants.

```cpp
// C++17: integral, enum, pointer-to-member NTTPs
template<std::size_t N>
std::array<Seat, N> make_seats();

// C++20: template<auto N> — deduces type automatically
template<auto N>
struct Config { static constexpr auto value = N; };

// C++20: class-type NTTP (must be structural type)
struct Tag { int id; };
template<Tag T>
void process();  // process<Tag{42}>() — compile-time config
```

---

## Expression Templates (C++11)

Per [ENG-3.1](laws/engineering/eng-3-code-quality.md), expression templates
implement **lazy evaluation** to eliminate temporaries in chained arithmetic. Example: unit-safe altitude arithmetic:

```cpp
template<typename L, typename R>
struct AddExpr {
    const L& lhs; const R& rhs;
    double eval() const { return lhs.eval() + rhs.eval(); }
};

struct Altitude { double m;  double eval() const { return m; } };

template<typename L, typename R>
AddExpr<L,R> operator+(const L& l, const R& r) { return {l, r}; }

// ✅ No temporaries: a+b+c builds a tree, eval() computes once
auto result = (a + b + c).eval();
```

Use when: hot numeric paths with ≥3 operands, proven by profiler.
Prefer `constexpr` for compile-time computation; expression templates for
runtime lazy chains (Eigen/Blaze motivation).

---

## C++20 Lambda Improvements

Per [ENG-3.1](laws/engineering/eng-3-code-quality.md), C++20 lambda
improvements enable generic, compile-time, and structured-binding captures.

```cpp
// Template lambda (C++20): explicit type parameter
auto sum = []<typename T>(std::vector<T> const& v) {
    return std::accumulate(v.begin(), v.end(), T{});
};

// consteval lambda: compile-time only
auto square = [](int n) consteval { return n * n; };
static_assert(square(5) == 25);

// Capturing structured bindings (C++20)
auto [id, name] = get_flight();
auto log = [id, name]{ audit_log(id, name); };  // ✅ C++20 — was ill-formed before

// [[nodiscard]] lambda (C++20)
auto make_id = [][[nodiscard]]() -> FlightId { return generate(); };
```

## See Also

- `ref-templates-metaprogramming.md` — SFINAE→concepts progression, ADL, lambdas (C++11/17)

## Further Reading

> Further reading: Josuttis, *The C++ Standard Library* 2nd Ed. (2012) — STL algorithm complexity,
> iterator categories, and template library design patterns.

> Further reading: Alexandrescu, *Modern C++ Design* (2001) — policy-based design, TypeList,
> factory via type traits. *(Use Loki BSD source for code examples.)*

> Further reading: Coplien (1992) — foundational vocabulary for C++98-era idioms including CRTP
> naming, Handle/Body, and Counted Body patterns.
