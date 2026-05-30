# R1 — Copyright Counsel: Version-Sensitivity Review of ESE Proposal

**Reviewer:** Senior copyright counsel, 20+ years US copyright and IP law  
**Review Date:** 2026-07-14  
**Scope:** Focused re-review — does the 5-tier version-sensitive routing system introduce new copyright
or licensing complications not present in the original review or the OSS response?  
**Documents reviewed:**
- `PROPOSAL.md` (including OSS Governing Principle)
- `docs/guides/avatars/cpp-version-sensitive-routing.md`
- `REVIEW-PANEL.md` (original R1 section + R1 Formal Response to OSS Source Analysis)

**Prior verdicts:**
- Original: ⚠️ PROCEED WITH MODIFICATIONS — DO NOT EXECUTE AS-IS
- Post-OSS: ✅ PROCEED — SUBJECT TO THREE REMAINING PREREQUISITES

---

## Executive Finding

**The 5-tier version-sensitive routing system does NOT materially change the copyright analysis.**

The routing system is an architectural dispatch mechanism — it maps project signals (`cpp.standard`,
`idiom_level`) to pre-existing reference files. It does not create content, does not alter the license
terms of OSS sources, and does not change the character of AA's use of Core Guidelines-adapted content
from internal to external. The three remaining prerequisites from the post-OSS verdict (Core Guidelines
license fix, OSS Reference Registry, derivation language amendment) are independent of routing
architecture and remain controlling.

**However**, the version routing system introduces **three ancillary concerns** that did not exist in
either prior review round. None are independently blocking, but two require documented resolution before
content deployment:

1. **Linear attribution scaling** — creating N version-specific derivative files from the same OSS
   source multiplies per-file attribution obligations in a predictable and manageable way. Requires
   ESE-00.3 tracking.
2. **Copyright notice propagation in section-level RAG retrieval** — if Content Filtering (Step 4 of
   the routing flow) operates at sub-file granularity, attribution comments may not travel with the
   extracted section. Requires specification of retrieval granularity.
3. **`bshoshany/thread-pool` C++14 backport derivation scope** — the C++14 variant of a C++17-minimum
   OSS source is a lawful derivative under MIT but that conclusion needs formal documentation.

The remaining four items below either confirm settled findings or identify non-issues. Each is addressed
explicitly.

---

## Section 1: Version-Specific OSS Source Licensing

**Question:** Do the OSS derivation sources have version-dependent licensing that changes the analysis
when AA derives content for a specific C++ tier?

### 1.1 `boostorg/lockfree` — Boost Software License across C++11 and C++20 tiers

**Finding: No material legal difference between C++11-era and C++20-era use. Settled.**

The Boost Software License 1.0 is a single, version-neutral text. It imposes one condition: for
source-code distributions, the license text must not be removed or altered. It imposes no condition on
binary distributions. The license contains no C++ standard version restriction, no era-specific clause,
and no provision that would treat a C++11 example differently from a C++20 example. Tim Blechmann's
copyright in `boost/lockfree/queue.hpp` is the same copyright whether the file is compiled under
`-std=c++11` or `-std=c++20`. The version routing system's decision to serve Boost-derived content to
the `transitional` or `greenfield` tier changes nothing about BSL compliance obligations.

**One factual note for the record:** REVIEW-PANEL.md describes Boost.Lockfree as "predating Williams
by 4 years." R5 correctly flagged this as imprecise — official Boost release was February 2013,
contemporaneous with Williams 2012. The copyright independence argument rests on the derivation chain
running through Treiber 1986 and Michael & Scott 1996 PODC (both pre-dating Williams), not on
Boost.Lockfree's release date alone. This has no version-routing implication but the ESE-00.3 registry
should state the argument accurately.

### 1.2 `bshoshany/thread-pool` — MIT, C++17 minimum, C++14 backport scenario

**Finding: A C++14 variant derived from this source is clearly within the MIT license. New documentation
item required in ESE-00.3.**

MIT grants AA "the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software." There is no C++ standard version restriction in MIT. The C++17 minimum in
`bshoshany/thread-pool` is a compiler requirement for the original source, not a license restriction on
derivatives. AA may lawfully write a C++14 adaptation that replaces `std::jthread`/`std::stop_token`
with `std::thread` + a cooperative-stop flag.

Two conditions attach under MIT:
1. The copyright notice and permission notice must be preserved in all copies or **substantial
   portions** of the Software. A C++14 backport that retains structural derivation from the original
   is a "substantial portion" and requires the copyright notice in the file header.
2. If the C++14 variant is sufficiently transformed that no structural element of the original remains
   (Use Mode A — reference only), it may be an independent work and no attribution obligation attaches
   under MIT. Given the semantic and syntactic gap between a `std::jthread` implementation and a
   `std::thread` + manual stop-flag implementation, this is plausible — but it requires a per-file
   judgment at creation time, not a categorical rule.

**Required documentation in ESE-00.3:** Add a "C++14 backport" entry for `bshoshany/thread-pool`
noting: (a) the backport is within MIT license permissions; (b) if the backport retains structural
derivation, the copyright notice must be in the file header; (c) if the backport is independently
implemented using the thread-pool architecture as reference only, it is Use Mode A and no attribution
obligation attaches to the derived file (though the derivation comment citing the OSS source should
still appear for provenance documentation).

### 1.3 `fmtlib/fmt` — MIT; Victor Zverovich's dual role as author and ISO proposer

**Finding: No patent concern and no implied endorsement problem. Non-issue.**

Victor Zverovich is both the author of `fmtlib/fmt` (MIT, 2012) and a co-author of WG21 P0645
(the proposal that became `std::format` in C++20). Teaching fmtlib as "the C++11 path to std::format"
is not legally problematic on either the patent or endorsement theory:

**Patent concern:** The MIT license does not include an explicit patent grant (unlike Apache 2.0 §3).
However, `std::format` was standardized by ISO — the standardization process inherently requires
contributors to ISO/IEC JTC1 SC22 WG21 to license their contributions under the ISOC++ patent
policy, which includes a royalty-free commitment for standard-conforming implementations. To the extent
Zverovich holds any patent claims on the formatting approach (none currently identified in the public
record), those claims would be encumbered by both the MIT license grant (which implicitly licenses
necessary patent claims under the *implied patent license* doctrine, *TransCore, L.P. v. Electronic
Transaction Consultants Corp.*, 563 F.3d 1271 (Fed. Cir. 2009)) and the WG21 patent policy. No
actionable patent concern exists.

**Implied endorsement concern:** None. Zverovich's fmtlib README actively and explicitly markets the
library as the reference implementation that became `std::format`. The connection is documented by the
author himself — there is nothing "implied" about it. Teaching this connection to AA engineers is
factually accurate, and accurate statement of fact does not constitute a false endorsement claim under
the Lanham Act.

**`★ C++20` routing note:** The routing system correctly serves fmtlib guidance to `transitional` and
`brownfield` tiers (C++11/14 codebase teams who cannot use `std::format` directly) and routes them
away from the `★ C++20` `std::format` section. This is technically accurate guidance and has no
copyright implication.

### 1.4 `ericniebler/range-v3` — Boost Software License; C++14 mode vs C++20 mode

**Finding: No license difference between modes. Settled.**

The BSL text in `ericniebler/range-v3` is identical to any other BSL repository and contains no
mode-dependent clauses. The library supports both a C++14 compatibility mode and a C++20 mode as a
compile-time configuration choice by the end user — it is a single codebase under a single license.
The version routing system's decision to serve `range-v3`-derived examples to the `transitional` tier
using C++14-compatible patterns (avoiding `std::ranges::views` which requires C++20 and instead using
the range-v3 equivalents) does not alter the BSL obligations in any way.

---

## Section 2: Multi-Version Derivative Works — Compliance Burden

**Question:** Does creating multiple version-specific derivatives (e.g., both a C++11 and C++20 file
from `boostorg/lockfree`) create additional license compliance burden beyond what was identified in the
original OSS review?

**Finding: The compliance burden scales linearly. It is manageable but must be tracked. New ESE-00.3
requirement.**

The original OSS review identified per-file attribution obligations: for BSL sources, each file
containing adapted code must preserve the copyright notice; for MIT sources, each file must preserve
the copyright notice and permission notice; for Apache 2.0 sources with NOTICE files, each derived
file's repository must include the NOTICE attribution.

When the version routing system causes AA to create two files from the same OSS source — one for the
`transitional` tier (C++11/14 patterns) and one for the `greenfield` tier (C++20 patterns) — each
file independently triggers the per-file attribution obligation. The obligation is the same in character
but applies twice. This is linear scaling, not a new category of obligation.

**The practical concern is traceability, not legal novelty.** As the routing system proliferates
tier-specific files, the number of files requiring attribution tracking grows. ESE-00.3
(`oss-reference-registry.yaml`) must include a "derived files" inventory that lists every AA file
derived from each OSS source, organized by tier. Without this inventory, a future compliance audit
cannot confirm that attribution was applied consistently across all version-specific variants.

**One structural risk worth noting:** If a developer creates the `greenfield` (C++20) file first
(from `boostorg/lockfree`), correctly applies the BSL attribution header, and later creates the
`transitional` (C++11) variant treating it as a "downgrade" rather than a fresh derivation, the
attribution obligation for the `transitional` file may be overlooked. The version routing architecture
should document a creation-time checklist: each new tier-specific file is a new derivation event
requiring its own attribution review, not a copy-and-downgrade of an existing file.

**Required addition to ESE-00.3:** A "derived files by tier" table mapping OSS source → AA file
→ tier, with a per-row "attribution applied" confirmation status.

---

## Section 3: Template Distribution and License Traceability

**Question:** Does distributing the `.copilot/project.yaml` template across AA repositories create
any license traceability burden?

**Finding: No license traceability burden from the template itself. Non-issue.**

The `cpp-project.yaml` template (at `avatars/technology/cpp/templates/cpp-project.yaml`) is a YAML
configuration file declaring routing parameters: `cpp.standard`, `idiom_level`, `compiler`, `toolset`,
and `notes`. Examining its content:

```yaml
cpp:
  schema_version: "1"
  standard: "14"
  idiom_level: "03"
  compiler: "gcc"
  toolset: "gcc-9"
  notes: "CWR migration..."
```

This template is AA's own original authorship. It derives from no OSS source, copies no third-party
expression, and contains no third-party copyright notices. Distributing it to AA's internal
repositories — including repositories that adopt the C++ avatar — does not create any OSS attribution
obligation, NOTICE file requirement, or copyright notice propagation burden on the template itself.

**The downstream activation effect is what matters, not the template.** When a team copies this
template and declares `standard: "14"`, they activate the routing system that will serve them
`transitional`-tier content. The license obligations attach to the content files that are served, not
to the template that triggers the routing. Those content-file obligations are already documented in the
original OSS review.

**One administrative note:** The template's `notes` field (free-text) could in theory contain
developer-authored content that references commercial books (e.g., a developer writes `notes: "See
Williams Ch. 9 for threading model"`). This is an edge case — the notes field is a comment for human
reference, not a derivation record — but the developer guidance document (Action 12 from the post-OSS
review) should include a one-line note that project.yaml notes fields are not to be used as OSS or
commercial-book attribution records.

---

## Section 4: `idiom_level` Backport Derivation Scope

**Question:** If AA creates C++03-idiom variants of content originally derived from C++11+ OSS sources,
is the backported derivative work clearly within the OSS license? Is there a "scope of derivation"
concern?

**Finding: C++03-idiom variants are within the OSS licenses, but the Use Mode A/B determination must
be made at creation time. Settled as a legal matter; requires per-file authorship judgment.**

The CWR scenario (`standard: "14"`, `idiom_level: "03"`) causes the avatar to serve C++03-idiom
examples to a C++14 codebase. If those C++03-idiom examples are derived from C++11+ OSS sources, the
derivation chain runs: C++11 OSS source → C++03-idiom AA example → CWR developer's context.

**Legal analysis under the applicable licenses:**

MIT, BSL, and Apache 2.0 all expressly permit "modification" without any language-version restriction.
A C++03-idiom adaptation is a modification in the ordinary sense. There is no "derivation scope"
doctrine in US copyright that would limit the permissible degree of transformation — either the work
is a derivative (subject to the license conditions) or it is an independent work (not subject to any
license conditions). The question is which category applies.

**The degree of transformation matters for the Use Mode A/B determination.** A C++03-idiom variant of
a C++11 thread-pool implementation involves substituting:
- `std::jthread` → POSIX `pthread_t` or `std::thread` (where available in partial C++11)
- `std::stop_token` → manual `volatile bool stop_flag` with `std::atomic` where unavailable
- Lambda captures → named functor classes
- `std::unique_ptr` → raw pointer with manual `delete`

This transformation is architecturally deep. After this degree of modification, the resulting C++03
file may retain no copied expression from the C++11+ OSS original — only the *idea* of a thread pool
with a work queue. Under *Baker v. Selden*, 101 U.S. 99 (1879), ideas are not protected by copyright.
Under *Feist*, only original expression is protected. If the C++03 file contains no copied code
structure, it is an independent work (Use Mode A) and carries no attribution obligation under any of
the applicable licenses.

**The key point for ESE-00.3:** A C++03 backport should be documented at creation time as either:
- Use Mode A (reference only): author consulted C++11 OSS for architectural understanding; C++03
  file is independently written; no attribution obligation under the OSS license (but derivation
  comment for provenance is still recommended practice)
- Use Mode B (code adapted): C++03 file retains structural derivation from the C++11 OSS source;
  attribution obligation attaches; file header must include the applicable copyright notice

The distinction is a per-file judgment, not a policy rule. This is not a new legal concern introduced
by the routing system — it is the same Use Mode A/B framework established in the post-OSS review
(New Concern 1, Required Action 7). The routing system creates the *occasion* to apply the framework
to a new category of files (C++03-idiom variants), but the framework itself is already in place.

---

## Section 5: Core Guidelines License — Tier-Routing Implications

**Question:** The version routing system serves Core Guidelines-adapted content to ALL tiers, including
`legacy` (pre-C++98) and `brownfield` (C++98/03) teams. Does this change the legal exposure under the
Standard C++ Foundation License's "internal use only" restriction?

**Finding: Tier-routing does not change the legal exposure. The finding is settled.**

The Standard C++ Foundation License's operative restriction is:

> "...for your **personal or internal business use only**..."

The restriction is keyed to the character of the USE (internal vs. external), not to the characteristics
of the USE'S RECIPIENT (which version of C++ they compile against). Routing Core Guidelines-adapted
content to a C++98 team at AA is the same legal act as routing it to a C++20 team at AA — both are
internal to the organization. The internal/external boundary is the legal threshold. The standard/tier
boundary is irrelevant.

**One technically-grounded observation, not a new legal finding:** Some Core Guidelines rules are
inherently version-specific (e.g., rules governing `std::span`, `std::format`, `constexpr` improvements,
Concepts). When the routing system delivers these rules to a `legacy` or `brownfield` tier team, the
developer cannot apply them. This is a technical/RAG quality concern (R4's domain), not a copyright
concern. The Standard C++ Foundation License does not require that adapted content be *usable* by the
recipient — only that it be used internally and that the file-header copyright block is present.

**The pre-existing Critical Finding 1 remains unchanged and blocking:** Every Core Guidelines-adapted
file must carry the Standard C++ Foundation file-header copyright block:

```markdown
<!-- Portions adapted from C++ Core Guidelines.
     Copyright (c) Standard C++ Foundation and its contributors.
     Licensed for internal business use only.
     License: https://github.com/isocpp/CppCoreGuidelines/blob/master/LICENSE -->
```

The tier a file is routed to does not change this requirement.

---

## Section 6: Copyright Notice Propagation in RAG Context

**Question:** Does the version routing system create any scenario where a copyright notice is stripped
or not surfaced when content is served to a developer?

**Finding: There is a latent risk in section-level RAG retrieval that requires architectural
specification. This is the most novel copyright concern introduced by the version routing system.**

The routing guide describes a Content Filtering step (Step 4 in the version-aware RAG query flow):

> `ref-concurrency-threading.md` loaded; `★ C++17` `scoped_lock` section is NOT served (project is
> C++14). Primary GOOD example uses `std::lock_guard` (C++11) ✓

This filtering is described as behavioral: the agent answers with C++11/14-compatible patterns only.
The ambiguity is whether "NOT served" means:

**Interpretation A — Behavioral filtering (whole-file load):** The agent loads the complete reference
file, including all copyright headers and attribution comments, into its context window. The agent
then chooses not to *respond* with the C++17 content. Under this interpretation, the copyright notices
for all sections of the file are present in the agent's context for every retrieval event, regardless
of which tier content the agent ultimately responds with.

**Interpretation B — Architectural filtering (section-level extraction):** The RAG pipeline extracts
only the C++11-relevant sections of the file and passes those sections to the agent's context window.
The C++17 and C++20 sections (and potentially their associated attribution comments) are not loaded.
Under this interpretation, if a multi-version file has section-specific attribution comments:

```cpp
// Adapted from: boostorg/lockfree/queue.hpp (BSL) — C++11 lock-free pattern
std::atomic<T*> head{nullptr};
```

...those comments travel with their sections and the copyright notice propagates correctly under
section-level retrieval. **But if the file header carries the copyright notice (which is the
documented requirement from the original OSS review) and section-level extraction excludes the file
header**, then the attribution obligation is technically satisfied (the notice exists in the file) but
is not surfaced to the developer or auditor in the retrieval context.

**The `★ C++NN` section-level callout design introduces this ambiguity.** A reference file with
`cpp_version_min: 11` and a `## Advanced Patterns ★ C++20` section has:
- A single file-header copyright block covering the entire file
- Section-specific attribution comments at the code-block level

If the routing system operates under Interpretation A (behavioral, whole-file load), copyright notices
propagate correctly and this concern evaporates. If it operates under Interpretation B (architectural,
section-level extraction), the file-header copyright block is the only location not reliably reaching
the developer's context.

**Required action:** The routing guide
(`docs/guides/avatars/cpp-version-sensitive-routing.md`) must specify which interpretation is
operative. If Interpretation B is used, the attribution comment format must be strengthened: **every
code section with a `★ C++NN` marker that has distinct OSS provenance must carry its own inline
attribution comment** within the section, not only in the file header. The derivation comment format
already supports this (the `// Ref:` and `// Adapted from:` conventions), but it must be documented
as mandatory for version-gated sections, not merely conventional.

**Severity:** 🟡 MEDIUM — not blocking because the file-header copyright notice always exists in the
file, satisfying the OSS license's formal requirement. The concern is auditability and developer
awareness, not technical breach. Resolving it costs one sentence in the routing guide and a reminder
in the content creation checklist.

---

## Updated Verdict

**Prior verdict (post-OSS):** ✅ PROCEED — SUBJECT TO THREE REMAINING PREREQUISITES  
**Version routing re-review verdict:** ✅ PROCEED — prior verdict UNCHANGED — three additional
documentation items added (non-blocking)

The version-sensitive routing system introduces no new blocking copyright concerns. The three
remaining prerequisites from the post-OSS verdict govern independent concerns and retain their
priority and blocking status:

1. **Core Guidelines license fix** (Actions 1–4 from post-OSS review) — unchanged, blocking, not
   affected by routing.
2. **OSS Reference Registry + Governing Principle amendment** (Actions 5–7) — unchanged, blocking,
   not affected by routing.
3. **Developer guidance on Further Reading discipline and Copilot prompt hygiene** (Actions 12–13)
   — unchanged, blocking, not affected by routing.

**Three additional documentation items from this review (non-blocking, required before content
deployment):**

| # | Item | Priority | Basis |
|---|------|----------|-------|
| V1 | Add "derived files by tier" table to ESE-00.3, mapping each OSS source to each AA tier-specific derivative file with per-row attribution confirmation | 🟡 | Section 2 — linear attribution scaling |
| V2 | Specify in the routing guide whether Content Filtering operates at whole-file load (Interpretation A) or section-level extraction (Interpretation B); if B, mandate inline attribution comments in all `★ C++NN`-gated sections with distinct OSS provenance | 🟡 | Section 6 — copyright notice propagation |
| V3 | Add C++14 backport entry for `bshoshany/thread-pool` in ESE-00.3, documenting the Use Mode A/B determination framework for C++03-idiom and C++14 tier-specific variants | 🟢 | Section 1.2 and Section 4 |

**Items confirmed as non-issues by this review (explicitly settled):**

| Topic | Section | Conclusion |
|-------|---------|------------|
| BSL version-neutrality for `boostorg/lockfree` | 1.1 | No version-dependent clauses in BSL |
| `fmtlib` dual-role patent/endorsement concern | 1.3 | No actionable patent claim; no implied endorsement problem |
| `range-v3` BSL mode difference (C++14 vs C++20) | 1.4 | Single license text; no mode-dependent clauses |
| `.copilot/project.yaml` template distribution | 3 | Template is AA-authored YAML; creates no OSS attribution obligations |
| Core Guidelines internal-use restriction across tiers | 5 | Restriction is use-character-based (internal/external), not recipient-based |

---

*R1 version-sensitivity review submitted 2026-07-14. This review supplements the original R1 section
(lines 24–81 of REVIEW-PANEL.md) and the R1 Formal Response to OSS Source Analysis (lines 1229–1508
of REVIEW-PANEL.md). The updated verdict of ✅ PROCEED is unchanged. Three prior prerequisite actions
retain their blocking status. Three new non-blocking documentation items (V1, V2, V3) are added for
resolution before content deployment.*
