# C++ Avatar — External Source Curation Guide

> **Purpose:** Explains the intellectual provenance of the C++ avatar — which external sources
> shaped its content, how derivation decisions were made, what copyright frameworks apply, and
> how future maintainers should handle new sources.
>
> **Audience:** Avatar maintainers, constitution contributors, legal reviewers, AI agents
>
> **Laws:** [ENG-10.1](../../laws/engineering/eng-10-constitution.md) (Documentation),
> [ENG-6.7](../../laws/engineering/eng-6-security.md) (Audit Trail),
> [ENG-11.1](../../laws/engineering/eng-11-hangar-sdd.md) (Hangar SDD)
>
> **Quick reference:** [`avatars/technology/cpp/SOURCES.md`](../../../avatars/technology/cpp/SOURCES.md)
> — the per-source table that agents use at the keyboard.

---

## Why This Document Exists

A C++ governance avatar must be authoritative. To be authoritative, it must stand on credible
shoulders. Those shoulders are specific books, open-source repositories, ISO standard papers,
and free web resources written by the people who designed the language and its idioms.

But "standing on" carries legal and ethical weight. The decisions about *which* sources to use,
*how much* to derive from them, and *how to attribute* them were reviewed by seven expert
reviewers across four rounds of formal evaluation before any content was committed. This guide
captures those decisions permanently, so that future maintainers — human or AI — can extend the
avatar without accidentally recreating risks that were already analyzed and resolved.

**What this guide does not replace:** The [`SOURCES.md`](../../../avatars/technology/cpp/SOURCES.md)
file in the avatar root is the working quick-reference. This guide is the narrative rationale
behind it.

---

## The Evolution of the Source Strategy

### Round 1 — Original Proposal (Four Commercial Books)

The initial `cpp-external-sources-enrichment` proposal cited four sources as its derivation
foundation:

1. **C++ Core Guidelines** — mistakenly labeled "MIT"; actually Standard C++ Foundation License
2. **C++ Concurrency in Action, 2nd Ed.** (Anthony Williams, Manning 2019)
3. **C++ Templates: The Complete Guide, 2nd Ed.** (Vandevoorde/Josuttis/Gregor, 2017)
4. **C++20: The Complete Guide** (Nicolai M. Josuttis, 2022)

The review panel identified three blocking problems with this approach:
- The Core Guidelines license was misidentified — it restricts external publication
- Manning and Pearson EULAs may prohibit derivative internal corporate works
- Structural copying risk under *Computer Associates v. Altai* for chapters 5, 7, 9 of Williams

The original proposal was blocked. No content was derived from commercial sources.

### Round 2 — OSS Source Analysis

An open-source discovery analysis across 22 repositories identified permissively-licensed
alternatives for every commercial source's concept domain:

| Commercial Source | OSS Replacement Found | License |
|---|---|---|
| Williams Ch. 5 (memory ordering) | C++ Core Guidelines CP.xx + `std::atomic` cppreference | Public domain |
| Williams Ch. 7 (lock-free) | `boostorg/lockfree` (2008, pre-publication) | Boost Software License |
| Williams Ch. 9 (thread pools) | `bshoshany/thread-pool`, Abseil | Apache 2.0 / MIT |
| Vandevoorde template metaprogramming | Loki Library (Alexandrescu, pre-book) | Modified BSD |
| Josuttis ranges / concepts | `ericniebler/range-v3`, cppreference | BSL-1.0 / public |
| Josuttis `std::format` | `fmtlib/fmt` (the actual reference implementation) | MIT |

The OSS analysis reduced the structural copying risk from four tasks to one (hazard pointer
section in the lock-free example), and eliminated the EULA breach risk entirely.

### Round 3 — Version Sensitivity Review

A third review round identified that even with OSS sources, the proposal was **systematically
skewed toward C++20/23** — serving 0% of AA's current production LOC — while the 95% of LOC
at legacy/brownfield/transitional tiers had critical unaddressed gaps:

- JNI thread safety at C++98 (`CrewWatchSolverJNI.cpp` in CWR)
- FAR 117 timezone arithmetic at C++14 (IOC_ALP, upcoming CWR modernization)
- Rule of Three for C++98 codebases
- `const char*` lifetime traps for pre-C++17 teams
- MSVC 6.0 characterization test patterns without GoogleTest

These gaps were addressed in a separate prerequisite proposal: `cpp-brownfield-first` (CBF,
PR #49 merged April 2026). CBF became the bridge between the original modern-only ESE scope
and AA's actual production reality.

### Round 4 — Historical Source Library Expansion

With CBF complete and ESE resuming, the review panel recommended a fourth evolution: broadening
the external source library to include **the classical C++ canon** that AA's legacy codebases
were written against. SPEClient, herc-odyssey-linux, and CWR contain idioms from Coplien
(1992), Meyers (1996–2005), and Sutter (1999–2004) that developers encounter but may not
recognize by name. Giving those patterns their names — and citing the authoritative sources —
is itself a form of governance.

The Round 4 expansion adds 12 historical sources to the avatar's source library, all under the
clean-room protocol described below.

---

## The Three-Tier Derivation Framework

All C++ avatar content falls into one of three derivation tiers. The tier determines how
content may be authored, what attribution is required, and what maintainers may do.

### Tier 1 — Freely Derivable

OSS or public domain sources. Code examples in avatar files may be directly based on these
sources provided an attribution comment is included. No clean-room process required.

**Canonical Tier 1 sources:**
- C++ Core Guidelines (Standard C++ Foundation License — internal use only; attribution block required)
- Howard Hinnant `date` library (MIT)
- fmtlib/fmt (MIT)
- range-v3 (BSL-1.0)
- GSL / microsoft/GSL (MIT)
- Loki Library (Modified BSD)
- boostorg/lockfree, boostorg/thread (BSL-1.0)
- Android NDK samples (Apache 2.0)
- Jason Turner cpp-best-practices GitHub (MIT)
- ISO C++ standard papers via open-std.org (public domain)
- POSIX standard, IANA timezone database (open standards / public domain)
- cppreference.com (CC-BY-SA 3.0)

**Attribution format for Tier 1:**
Every file that derives content from a Tier 1 source must include an HTML comment in the
front matter naming the source, its license, and a link:

```markdown
<!-- Derived from fmtlib/fmt (MIT). https://github.com/fmtlib/fmt -->
```

For the C++ Core Guidelines specifically, the fuller block is required by the license terms:

```markdown
<!-- Portions adapted from C++ Core Guidelines.
     Copyright (c) Standard C++ Foundation and its contributors.
     Licensed for internal business use only.
     https://github.com/isocpp/CppCoreGuidelines/blob/master/LICENSE -->
```

### Tier 2 — Cite and Link

Free web resources where the author has granted educational use, but content should not be
reproduced in bulk. Up to ~50 words of prose may be quoted with a URL citation. Code examples
from these sources should be independently re-authored.

**Canonical Tier 2 sources:**
- Herb Sutter's GOTW articles (herbsutter.com) — exception safety, copy-and-swap, naming
- Bjarne Stroustrup's C++ FAQ (stroustrup.com) — language design rationale
- Bartlomiej Filipek's cppstories.com articles — `std::variant`, `std::optional`, PMR

**Attribution format for Tier 2:**

```markdown
> See also: Sutter, GOTW #64 "Exception-Safe Function Calls" — https://herbsutter.com/gotw/_064/
```

### Tier 3 — Clean-Room Only

Commercial books and self-published works under copyright. These sources may be used for
*concept identification* (knowing what to cover) and *"Further Reading" attribution* only.
Code examples and prose structure must be independently authored.

**Clean-room protocol:**

1. **Concept identification phase:** A maintainer reads the source material and writes a
   concept outline — what the section should demonstrate — using bullet points only. No
   code, no borrowed prose, no structural mirrors of the chapter.

2. **Implementation phase:** The implementer authors code and explanatory prose from the
   ISO C++ standard text, cppreference.com, and Tier 1 OSS sources only. The book is closed.
   The concept outline is the only permitted reference.

3. **Structural comparison:** After drafting, compare the file's organizational structure
   against the source chapter. If section sequence mirrors the book's chapter ordering,
   restructure before committing.

4. **Attribution:** Add a visible "Further Reading" block at the bottom of the section:
   ```markdown
   > **Further reading:** This section covers [topic]. For comprehensive depth,
   > see [Author, *Title* (Year)] — the authoritative reference for this subject.
   ```

**Canonical Tier 3 sources:** Coplien (1992), Meyers (1992–2014), Sutter *Exceptional C++*
series (1999–2004), Sutter & Alexandrescu *C++ Coding Standards* (2004), Alexandrescu *Modern
C++ Design* (2001), Feathers *Working Effectively with Legacy Code* (2004), Josuttis STL
reference (2012), Josuttis C++17/C++20 guides, Stroustrup *TC++PL* and *D&E*, Filipek *C++
in Detail*, Turner *C++ Best Practices* (Leanpub edition).

---

## The Bridge Concept

A **bridge example** is an AA-domain code file that provides a Tier 1 OSS library as a safe,
version-compatible alternative to a C++20+ standard library feature. Bridges exist because
AA's transitional-tier codebase (C++14, ~60% of LOC) cannot adopt C++20 but deserves the
same safety patterns as modern-tier developers.

| C++20 Standard Feature | Bridge Example File | Bridge Library | License |
|---|---|---|---|
| `std::format` | `ENG-6.1-fmtlib-format.md` | fmtlib/fmt | MIT |
| `std::ranges` pipelines | `ENG-3.1-ranges-range-v3.md` | range-v3 | BSL-1.0 |
| `std::span` | `ENG-6.1-gsl-span-cpp14.md` | GSL `gsl::span` | MIT |
| `std::jthread` stop pattern | `ENG-6.1-thread-stop-flag.md` | Standard C++11 | N/A |
| Lock-free via `atomic<T*>` | `ENG-6.1-lock-free-cpp14.md` | C++11 `std::atomic` | N/A |
| `std::chrono::zoned_time` | `ENG-6.1-timezone-cpp14.md` | howardhinnant/date | MIT |

**Why bridges matter for sourcing decisions:** Bridge files are Tier 1 (the OSS library is the
derivation source), but they also benefit from Tier 3 conceptual framing. For example, the
`ENG-6.1-lock-free-cpp14.md` file's ABA prevention pattern is conceptually documented in
Sutter's GOTW articles and the *Exceptional C++* series. The *concept* comes from Tier 3; the
*code* is derived from Tier 1 (boostorg/lockfree and `std::atomic` cppreference). This
two-source pattern is intentional and correct.

---

## The Historical Source Library

The historical source library addresses a specific gap: AA's legacy and brownfield C++ code
was written in the 1990s and early 2000s by engineers who had read Coplien, Meyers, Sutter,
and Alexandrescu. Those books established the *vocabulary* of the code — idiom names, design
decisions, pattern structures. A developer reading CWR or herc-odyssey-linux without knowing
this vocabulary will recognize the code as C++ but not understand why it's structured the way
it is.

The historical library adds that vocabulary to the avatar under clean-room derivation. The
goal is not to reproduce the books — it is to give the patterns their names.

### Key Historical Source Roles

**Coplien (1992) — Idiom Vocabulary**
Coplien coined or popularized: CRTP ("Curiously Recurring Template Pattern"), Handle/Body
(the Pimpl idiom), Envelope/Letter (value-semantic wrapper around a polymorphic implementation),
Counted Body (reference-counted handle), Functor Callbacks (objects that behave as functions).
All of these appear in C++98 AA code. Coplien's vocabulary gives them their names.

**Meyers (1992–2014) — Correctness Checklist**
Meyers' three books collectively define ~130 correctness items that C++ developers internalized
as a vocabulary: "Item 3" (const), "Item 14" (resource handle copy), "Item 17" (exception safety
in smart pointer initialization), "Item 26" (avoid overloading on universal references). In
technical discussions at AA, "Per Meyers Item N" is a recognized citation form. The avatar
supports this by cross-referencing item numbers in the relevant ref file sections.

**Sutter (1999–2004) — Exception Safety**
Exception safety guarantee levels — basic guarantee (no resource leak), strong guarantee
(commit-or-rollback), nothrow guarantee — are Sutter's conceptual framework, popularized through
the GOTW series and *Exceptional C++*. The copy-and-swap idiom for exception-safe `operator=`
appears in Rule of Three implementations throughout AA's C++98 code. The avatar's
`ref-brownfield-survival.md` names these guarantees, with GOTW citations by URL (Tier 2).

**Alexandrescu (2001) + Loki — Policy-Based Design**
Policy-based design (using template parameters as behavioral policies rather than virtual
dispatch) is the C++98 technique for static polymorphism in performance-sensitive code. SPEClient
and herc-odyssey-linux almost certainly contain policy-based classes. Alexandrescu named and
documented the technique; the Loki library (BSD-licensed) demonstrates it in code that can be
freely derived from. The avatar's template metaprogramming section uses Loki code (Tier 1) with
Alexandrescu concept attribution (Tier 3).

**Feathers (2004) — Characterization Test Vocabulary**
The seam concept, characterization testing, Sprout Method, and Wrap Class are Feathers' patterns
for making untestable C++98 code testable. R8 Amendment R8-2 (C++98 characterization test without
GoogleTest) was implemented in `ref-brownfield-survival.md` §"MSVC 6.0 Golden-Master Testing"
using clean-room derivation from the seam concept with Feathers (2004) cited in "Further Reading."

**Jason Turner (MIT GitHub) — Modern Discipline**
Turner's `cpp-best-practices` GitHub repository is MIT-licensed and covers const-correctness
discipline, sanitizer integration, CMake best practices, and C++14/17 idioms for transitional-
tier developers. Unlike the other historical sources, Turner's GitHub is Tier 1 — code may be
directly derived. His YouTube *C++ Weekly* episodes are cited by episode number with links.

---

## Maintainer Protocol: Adding a New Source

When ESE or a future proposal wants to incorporate a new external source:

1. **Classify the source** using the tier definitions above. If uncertain, default to Tier 3.

2. **Add a row to `SOURCES.md`** in the appropriate tier section before writing any content
   that derives from it. This is the audit trail requirement (ENG-6.7).

3. **For Tier 1:** Add an attribution comment to every file that derives from the source.
   Use the format specified in the Tier 1 section above.

4. **For Tier 2:** Use URL citations only. Do not reproduce more than ~50 words.

5. **For Tier 3:** Follow the clean-room protocol (concept outline → independent implementation
   → structural comparison → Further Reading block). Document the derivation decision in the
   commit message: `chore: add [topic] via clean-room derivation (Tier 3 — [Source Title])`.

6. **For commercial books not yet in the library:** Before using them for concept identification,
   check whether an OSS alternative exists (search GitHub for the repo name + `awesome-cpp`).
   If a Tier 1 alternative exists, prefer it. Commercial books as Tier 3 sources are acceptable
   but Tier 1 is always preferred.

7. **Do not add a source** that is restricted to a specific individual's O'Reilly Safari or
   Manning subscription. Enterprise license verification is required before using commercially
   licensed books for AA governance purposes (ESE-00.4 prerequisite).

---

## Per-File Attribution Quick Reference

| File location | Attribution requirement |
|---|---|
| `avatars/technology/cpp/refs/**/*.md` | HTML comment in front matter for Tier 1 sources; "Further Reading" block for Tier 3 |
| `avatars/technology/cpp/examples/**/*.md` | HTML comment citing OSS derivation source + commit hash |
| `docs/guides/avatars/**/*.md` | In-text citation with hyperlink to source |
| `hangar-ai-specs/changes/**/*.md` | Proposal front matter `sources:` field listing all Tier 1–3 sources used |

---

## Relationship to Review Panel Findings

This guide consolidates the provenance decisions made across four formal review rounds:

| Review Round | Key Provenance Decision | Document |
|---|---|---|
| Round 1 (Original panel) | Core Guidelines license misidentified; commercial books blocked | `REVIEW-PANEL.md` §R1 |
| Round 2 (OSS analysis) | Tier 1 OSS alternatives found for all commercial sources | `OSS-SOURCE-ANALYSIS.md` |
| Round 3 (Version sensitivity) | Bridge concept introduced; FAR 117 C++98 gap identified | `R8-VERSION-REVIEW.md` §6.1 |
| Round 4 (Post-CBF) | Historical source library added; clean-room protocol formalized | `PANEL-UPDATE-ROUND-4.md` §4 |

---

*Last updated: 2026-04-27. Per ENG-10.1, this guide must be updated when any new external
source is added to the C++ avatar or when the derivation policy changes.*
