---
id: cpp-sources
avatar: cpp
purpose: Source inventory — lists every external reference that influenced C++ avatar content.
  Agents load this file when generating citations. Maintainers consult this before adding
  new content derived from any external source.
audience: AI agents, avatar maintainers, legal reviewers
related: docs/guides/avatars/cpp-source-curation-guide.md
---

# C++ Avatar — External Source Inventory

> **How to use this file:**
> - **Agents:** When citing a pattern, look up the source here to get the correct attribution form.
> - **Maintainers:** Before writing new content, find the source in this table and follow the "Derive?" policy.
> - **Legal:** Each row identifies the license and derivation decision rationale.
>
> Full rationale for each decision: [`docs/guides/avatars/cpp-source-curation-guide.md`](../../docs/guides/avatars/cpp-source-curation-guide.md)

---

## Tier 1 — Freely Derivable (OSS / Public Domain)

Content in avatar files may be directly based on these sources. Attribution comment required.

| Source | License | Key Avatar Files Influenced | Cite As |
|--------|---------|----------------------------|---------|
| **C++ Core Guidelines** (Stroustrup/Sutter) | Standard C++ Foundation (internal business use only) | All ref files — law IDs `[ENG-N.N]`, Core Guidelines rule IDs `[I.11]` etc. | `<!-- Adapted from C++ Core Guidelines. Copyright Standard C++ Foundation. Internal use only. https://github.com/isocpp/CppCoreGuidelines/blob/master/LICENSE -->` |
| **Howard Hinnant `date` library** | MIT | `ENG-6.1-timezone-cpp14.md`, `ref-safety-far117-cwr.md` | `<!-- Derived from howardhinnant/date (MIT). -->` |
| **fmtlib/fmt** | MIT | `ENG-6.1-fmtlib-format.md`, `ref-io-formatting.md` | `<!-- Derived from fmtlib/fmt (MIT). -->` |
| **range-v3** (Niebler) | Boost Software License | `ENG-3.1-ranges-range-v3.md` | `<!-- Derived from ericniebler/range-v3 (BSL-1.0). -->` |
| **GSL — C++ Core Guidelines Support Library** | MIT | `ENG-6.1-gsl-span-cpp14.md` | `<!-- Derived from microsoft/GSL (MIT). -->` |
| **Loki Library** (Alexandrescu) | BSD-like (Modified BSD) | `ref-templates-metaprogramming.md` policy-based design section | `<!-- Derived from loki-lib/Loki (Modified BSD). -->` |
| **Boost.Lockfree** | Boost Software License | `ENG-6.1-lock-free-cpp14.md` | `<!-- Derived from boostorg/lockfree (BSL-1.0). -->` |
| **Android NDK samples** | Apache 2.0 | `ENG-6.1-jni-thread-cpp98.md`, `ENG-6.1-jni-thread-cpp11.md` | `<!-- Pattern from Android NDK JNI tips (Apache 2.0). -->` |
| **Jason Turner — `cpp-best-practices` GitHub** | MIT | `ref-core-modern-idioms.md` const-correctness, sanitizer sections | `<!-- Derived from lefticus/cppbestpractices (MIT). -->` |
| **ISO C++ Standard Papers** (open-std.org) | Public domain | Any section citing standardization rationale | `<!-- Source: ISO/IEC open-std.org paper P-XXXX. Public domain. -->` |
| **Barry Revzin ISO Papers** | Public domain | `ref-cpp20-features-part2.md` future-watch section | `<!-- Source: Revzin PXXXXRn, open-std.org. Public domain. -->` |
| **POSIX Standard** | Open standard | `ENG-6.1-jni-thread-cpp98.md`, `ref-safety-far117-cwr.md` POSIX time functions | `<!-- Source: POSIX standard / The Open Group. Open standard. -->` |
| **IANA Timezone Database** | Public domain | `ref-safety-far117-cwr.md` | `<!-- Source: IANA tz database. Public domain. -->` |

---

## Tier 2 — Cite and Link (Free Web Resources)

May be cited by URL; do not reproduce more than ~50 words of prose.

| Source | Policy | Key Avatar Files Influenced | Cite As |
|--------|--------|----------------------------|---------|
| **Herb Sutter — GOTW articles** (herbsutter.com) | URL citation + ≤50 words | `ref-core-type-safety.md` exception safety, `ref-brownfield-survival.md` | `> See also: Sutter, GOTW #64 "Exception-Safe Function Calls" — https://herbsutter.com/gotw/_064/` |
| **Bjarne Stroustrup — C++ FAQ** (stroustrup.com) | URL citation + ≤50 words | `ref-getting-started.md`, `ref-core-type-safety.md` | `> See also: Stroustrup FAQ — https://www.stroustrup.com/bs_faq2.html` |
| **Bartlomiej Filipek — cppstories.com** | URL citation + ≤50 words | `ref-core-modern-idioms.md` variant/optional sections | `> Further reading: Filipek, "std::variant Tricks" — https://www.cppstories.com/...` |
| **cppreference.com** | URL citation; content is freely reusable under CC-BY-SA 3.0 | Any section describing standard library semantics | `<!-- Standard library semantics from cppreference.com (CC-BY-SA 3.0). -->` |

---

## Tier 3 — Clean-Room (Concept Domain Only)

These commercial works may be cited by title and used for concept identification. **No structural
copying. No example reproduction.** Code must be independently authored from ISO standard,
cppreference.com, and Tier 1 OSS sources. See clean-room protocol in
[`cpp-source-curation-guide.md`](../../docs/guides/avatars/cpp-source-curation-guide.md#the-clean-room-protocol).

| Source | Publisher | Key Concept Domains | Avatar "Further Reading" Citation Form |
|--------|-----------|--------------------|-----------------------------------------|
| Coplien, *Advanced C++ Programming Styles and Idioms* (1992) | Addison-Wesley | CRTP naming, Handle/Body, Envelope/Letter, Counted Body, Functor Callbacks | `> Further reading: Coplien (1992) — foundational vocabulary for C++98-era idioms.` |
| Meyers, *Effective C++* 3rd Ed. (2005) | Addison-Wesley | Resource handle copy, const correctness, exception safety in assignments | `> Per Meyers, *Effective C++* Item 17 — ...` |
| Meyers, *Effective Modern C++* (2014) | O'Reilly | Move semantics, perfect forwarding, `auto`, concurrency idioms | `> Per Meyers, *Effective Modern C++* Item 26 — ...` |
| Sutter, *Exceptional C++* (1999); *More Exceptional C++* (2001) | Addison-Wesley | Exception safety guarantees, copy-and-swap, RAII contracts | `> Further reading: Sutter (1999) Chapter N — ...` |
| Sutter & Alexandrescu, *C++ Coding Standards* (2004) | Addison-Wesley | 101-item correctness checklist | `> Per Sutter & Alexandrescu Item N — ...` |
| Alexandrescu, *Modern C++ Design* (2001) | Addison-Wesley | Policy-based design, TypeList, factory via type traits | `> Further reading: Alexandrescu (2001) Chapter 1.` *(use Loki BSD code for examples)* |
| Feathers, *Working Effectively with Legacy Code* (2004) | Addison-Wesley | Seam points, characterization tests, Sprout Method, Wrap Class | `> Per Feathers (2004) — seam vocabulary for dependency-breaking in legacy C++.` |
| Josuttis, *The C++ Standard Library*, 2nd Ed. (2012) | Addison-Wesley | STL iterator categories, algorithm complexity, container guarantees | `> Further reading: Josuttis (2012) §N — ...` |
| Josuttis, *C++17 — The Complete Guide* (2019) | Self-published | `std::variant`, `std::optional`, structured bindings, PMR allocators | `> Further reading: Josuttis, *C++17 — The Complete Guide* (2019).` |
| Josuttis, *C++20 — The Complete Guide* (2022) | Self-published | Ranges, concepts, coroutines, `std::format`, `std::span` | `> Further reading: Josuttis, *C++20 — The Complete Guide* (2022).` |
| Stroustrup, *The C++ Programming Language*, 4th Ed. (2013) | Addison-Wesley | Language design rationale, type system, exception model | `> Further reading: Stroustrup, *TC++PL* 4th Ed. (2013) §N.` |
| Stroustrup, *The Design and Evolution of C++* (1994) | Addison-Wesley | Design rationale for RAII, templates, exceptions | `> Further reading: Stroustrup, *D&E* (1994) §N.` |
| Filipek, *C++ in Detail* (Leanpub) | Self-published | C++17 practical patterns in depth | `> Further reading: Filipek, *C++ in Detail* — https://leanpub.com/cppin-detail` |
| Turner, *C++ Best Practices* (2022) | Leanpub / GitHub | Sanitizer workflow, const-correctness discipline, CMake best practices | `> Further reading: Turner, *C++ Best Practices* — https://github.com/cpp-best-practices` *(GitHub repo is MIT)* |

---

## Revision Log

| Date | Change | Author |
|------|--------|--------|
| 2026-04-27 | Initial — covers CBF deliverables + ESE source library expansion (Round 4 panel) | Copilot |
