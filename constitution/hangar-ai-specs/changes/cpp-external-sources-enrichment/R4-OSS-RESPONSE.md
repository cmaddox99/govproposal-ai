## R4 — Constitutional AI RAG Expert: Response to OSS Source Analysis

**Response Date:** 2026-04-24  
**Responding To:** [OSS-SOURCE-ANALYSIS.md](./OSS-SOURCE-ANALYSIS.md)  
**Original Verdict:** ⚠️ NEEDS MODIFICATIONS — 4 blocking issues  
**Updated Verdict:** ⚠️ NEEDS MODIFICATIONS — 4 blocking issues (2 escalated in severity) + 4 new RAG concerns introduced by the OSS approach itself

---

### OSS Analysis Assessment — RAG Perspective

The OSS analysis is an excellent legal and provenance exercise. It does not touch R4's jurisdiction. The four original blocking issues remain fully open because the OSS substitution addresses *derivation provenance* — it says nothing about file sizes, dispatch routing, index maintenance, or test coverage. What the OSS approach DOES do is introduce four new RAG-specific failure modes that were not present in the original proposal. Two of those are introduced directly by the structural changes the OSS approach mandates (derivation comment blocks + Further Reading footers), and two are introduced by the addition of `oss-reference-registry.yaml` as a new RAG artifact.

**Net RAG verdict:** The OSS approach makes the token budget situation materially worse, introduces a new embedding contamination risk through Further Reading footers, and creates a new disambiguation failure mode (registry vs. example routing). These are all solvable — but they require additional required actions on top of the original four blocking issues, not instead of them.

> ⚠️ **Critical pre-existing finding:** During token budget verification for this response, the current avatar ref files were measured at: `ref-testing-ci.md` ≈ 6,852t, `ref-concurrency.md` ≈ 5,176t, `ref-advanced-cpp.md` ≈ 5,040t, `ref-core-language.md` ≈ 4,769t. **Every one of these files already exceeds the 3,500t RAG query window before any ESE content is added.** Silent truncation is happening in production today. BLOCKING Issue 1 is not a future projection — it is a current active defect. The ESE proposal makes it worse; it did not create it.

---

### Original Blocking Issues — Status Update

| Issue | Original Severity | Updated Severity | What Changed |
|-------|------------------|-----------------|-------------|
| BLOCKING 1 — Token Budget | 🔴 | 🔴🔴 **ESCALATED** | OSS derivation comments add 500–700t per dense ref file (not the 150–300t estimated in OSS analysis). Current files are ALREADY over the 3,500t limit before any ESE additions. Split calculus must be revised to target ≤2,800t ceilings to leave headroom for citation overhead. |
| BLOCKING 2 — Zero RAG Test Cases | 🔴 | 🔴 **UNCHANGED + EXPANDED** | Still fully open. OSS approach introduces two new required disambiguation test classes (OSS query vs. programming query; registry routing vs. example routing). The ≥15 test case floor must be revised upward to ≥20. |
| BLOCKING 3 — ENG-3.1 No Router | 🔴 | 🔴 **UNCHANGED** | OSS analysis has no effect on dispatch index absence. 9 ENG-3.1 files exist today with no index; ESE would add 8 more. Top_k:3 precision degrades proportionally to file count. Still blocking. |
| BLOCKING 4 — ENG-6.1-index.md | 🔴 | 🔴 **UNCHANGED** | OSS analysis has no effect. The 7 new ENG-6.1 files added by ESE still bypass the topic-routing mechanism until the index is updated. Still blocking. |

---

### New RAG Concerns from OSS Approach

#### New Concern 1 — Further Reading Blocks and Embedding Contamination

**Severity: 🔴 New blocking concern**

The OSS approach mandates a "Further Reading" block at the bottom of every example file. These blocks will contain author names and book titles: `Williams, C++ Concurrency in Action (Manning 2019)`, `Vandevoorde, C++ Templates (Addison-Wesley 2017)`, `Josuttis, C++20 (2022)`.

The embedding contamination problem:

1. The Further Reading section in ESE-17, ESE-24, and ESE-25 will all mention Williams. A query like `"How does Williams explain the happens-before relationship?"` will produce high cosine similarity to ALL three files — they are now semantically equivalent to the embedding model on that query surface.

2. `"What does Williams say about lock-free data structures?"` will match ESE-24, but also ESE-17 and ESE-25, and anything else with a Williams footer. With `top_k: 3`, one or two of those slots are wasted on the wrong files.

3. `"Josuttis C++20 ranges explanation"` will match the ranges files (ESE-03, ESE-19), the format files (ESE-06), and potentially any other file with a Josuttis footer — not because the content is about ranges, but because all of them share the same footer vocabulary.

**The author-name vocabulary in footers has near-zero disambiguation power within the C++ avatar because it is intentionally uniform across files.**

**Required fix (new action):** All Further Reading blocks MUST be wrapped in an embedding-exclusion annotation. The RAG pipeline must be configured to skip sections wrapped with this annotation when computing embeddings. Two acceptable implementations:

Option A (HTML comment marker — preferred for Markdown files):
```markdown
<!-- no-embed -->
### Further Reading
- Williams, *C++ Concurrency in Action* (Manning 2019) Ch. 7 — deeper treatment of the same patterns
- Boost.Lockfree documentation: https://www.boost.org/doc/libs/1_84_0/doc/html/lockfree.html
<!-- /no-embed -->
```

Option B (YAML frontmatter exclusion list — preferred for indexed files):
```yaml
embed_exclude_sections:
  - further-reading
  - oss-derivation-metadata
```

Without this fix, every file that gains a Further Reading footer becomes a **false positive trap** for author-name queries. This is a net regression in retrieval precision introduced entirely by the OSS approach's mandate.

**Add ESE-00.6-RAG (new task):** Define and implement the `<!-- no-embed -->` / `<!-- /no-embed -->` annotation convention and update the RAG pipeline configuration to skip marked blocks during embedding computation. Specify in ESE-01 that all Further Reading sections and OSS derivation headers MUST use this annotation.

---

#### New Concern 2 — OSS Citation Metadata in Code Comments and Embedding Noise

**Severity: 🟠 Significant concern — manageable with guidance**

The mandated derivation comment block:
```cpp
// Pattern: Michael-Scott lock-free queue.
// Ref: boostorg/lockfree/include/boost/lockfree/queue.hpp (Boost Software License, 2008)
// Algorithm: Michael & Scott, "Simple, Fast, and Practical..." PODC 1996.
// Further reading: Williams, C++ Concurrency in Action (Manning 2019) Ch. 7
```

This block is placed in C++ code within Markdown fenced code blocks (` ```cpp ... ``` `). Whether it contributes to the embedding depends entirely on the RAG chunker configuration.

**If chunker strips fenced code blocks before embedding (common):** The citation content is invisible to the embedding model. The annotations do not help or hurt retrieval. The `<!-- triggers: -->` heading convention becomes even more important as the only structured routing metadata.

**If chunker includes fenced code block content (also common):** The `boostorg/lockfree/include/boost/lockfree/queue.hpp` path string contributes ~10 tokens of path vocabulary to every function-level embedding chunk. Across 5-8 functions in an ESE-24 file, that's 50-80 tokens of highly specific path noise. This does not meaningfully hurt semantic retrieval — C++ queries don't mention file paths. But license names (`Apache 2.0`, `MIT`, `Boost Software License`) appearing in every file have near-zero discrimination power and dilute the embedding toward a generic "C++ licensed code" vector.

**What IS useful in the comment block (keep regardless):**
- `Michael & Scott` — unique proper noun, will correctly anchor "Michael-Scott queue" queries
- `Treiber` — unique; anchors "Treiber stack" queries  
- `PODC 1996` — uncommon vocabulary, won't cause false positives
- `ABA problem` (if present) — useful technical discriminator

**What is NOT useful as embedding content and should use `<!-- no-embed -->` treatment:**
- License names: `Apache 2.0`, `MIT`, `Boost Software License` — appear across ~15 files, zero disambiguation value
- Repo org prefixes: `boostorg/`, `facebook/`, `abseil/` — high frequency, low semantic specificity
- File paths: `boostorg/lockfree/include/boost/lockfree/queue.hpp` — useful for verbatim path lookups (nobody does this in governance queries)

**Recommendation:** OSS citation comment blocks should be placed between `<!-- no-embed -->` markers at the top of each `##` section, separate from the code block. The algorithm name and academic citation (`Michael & Scott 1996`) should remain in the heading or trigger comment where the embedding can use it for routing. The license/repo/path data serves legal provenance only — it should live in `oss-reference-registry.yaml`, not embedded in every file's vector.

**This changes the derivation comment format from the OSS analysis proposal:**
```cpp
// KEEP in code (algorithmic identity for routing):
// Pattern: Michael-Scott lock-free queue (PODC 1996).

// MOVE to <!-- no-embed --> block above the section:
// OSS derivation: boostorg/lockfree/queue.hpp (Boost Software License, 2008)
// Full provenance: oss-reference-registry.yaml#lockfree-queue
```

---

#### New Concern 3 — OSS Registry Indexing Strategy

**Severity: 🟠 Significant concern — requires scoping decision**

`oss-reference-registry.yaml` (ESE-00.3) will contain all 15 repository names, all license types, all relevant task IDs, and all academic citation strings. This makes it a very broad-match document. Without explicit scoping, it will score high cosine similarity to almost any C++ query that mentions algorithms, patterns, or libraries — which is every C++ query.

**Failure mode without scoping:**
- Query: `"How do I implement a lock-free queue in C++?"` 
- Expected: ESE-24 example file
- Failure: `oss-reference-registry.yaml` appears in top_k:3 because it contains "lock-free queue", "boostorg/lockfree", "ESE-24", "Michael-Scott" — more matching vocabulary than any single example file

**Required scoping for `oss-reference-registry.yaml`:**

1. **Set `document_type: metadata`** in the YAML frontmatter — the RAG pipeline must be configured to de-boost metadata documents in top_k ranking for non-attribution queries.

2. **Add restrictive trigger set:** This file should only surface for license and attribution queries:
   ```yaml
   triggers:
     - "what license is the C++ avatar content"
     - "which OSS repositories are cited"
     - "can I use this content commercially"
     - "what is the derivation chain for"
     - "oss-reference-registry"
   ```

3. **Add `must_not_retrieve` test cases** in `cpp-c++20.yaml` covering the exact failure mode above: programming queries must NOT return the registry in top_k.

4. **Add `must_retrieve` test cases** for the queries above: attribution queries MUST return the registry.

Without this scoping, the registry becomes a precision-destroying document that competes with every example file for top_k slots.

---

#### New Concern 4 — Token Budget Recalculation

**Severity: 🔴 Escalation of BLOCKING Issue 1**

The OSS analysis estimates "~150-300 tokens per file" of additional citation overhead. This estimate is correct for a small reference file with 1-2 example sections. It is not correct for the dense reference files targeted by ESE.

**Revised estimate for a typical dense reference file (8 major sections):**

| Content Type | Lines | Tokens (×0.75 words/token est.) |
|---|---|---|
| Per-section OSS citation block (4 lines × 8 sections) | 32 | ~480t |
| "Further Reading" footer | 8 lines | ~120t |
| **Total additional overhead** | **40 lines** | **~600t** |

This is 2× to 4× the 150–300t estimate in the OSS analysis.

**Revised token budget projections for proposed new/expanded files:**

| File | Pre-ESE (projected) | After ESE content | After OSS citations | vs. 3,500t limit |
|---|---|---|---|---|
| `ref-cpp20-features.md` (new) | — | ~5,700t | ~6,300t | **+80% over** |
| `ref-advanced-cpp.md` | ~5,040t (today) | ~6,506t | ~7,100t | **+103% over** |
| `ref-core-language.md` | ~4,769t (today) | ~6,937t | ~7,540t | **+115% over** |
| `ref-testing-ci.md` | ~6,852t (today) | unchanged | +~300t | **Already +96% over** |
| `ref-concurrency.md` | ~5,176t (today) | +ESE-17/24/25 | +~600t | **+170%+ over** |

**Revised split calculus:** The original BLOCKING Issue 1 required splitting `ref-cpp20-features.md` into `ref-cpp20-core.md` + `ref-cpp20-runtime.md`. With the OSS overhead now accounted for, the correct ceiling for any split target is **≤2,800t**, not ≤3,500t. The 700t citation overhead budget must be reserved.

**Additional required actions from this recalculation:**

1. The split of `ref-cpp20-features.md` into `ref-cpp20-core.md` + `ref-cpp20-runtime.md` remains required — and each split file must target ≤2,800t, not ≤3,500t.

2. `ref-concurrency.md` MUST be audited for retroactive splitting BEFORE ESE-17/24/25 content is added. At 5,176t today, adding 3 major concurrency sections + 600t of citation overhead will bring it to ~7,400t+.

3. `ref-testing-ci.md` (6,852t today) has ZERO ESE additions but is already the worst offender. It must be flagged for an immediate split audit independent of ESE.

4. A **pre-commit token ceiling check** must be added to constitution-lint (or the ESE-01 acceptance criteria) — any ref file commit that would push a file over 2,800t should fail the check.

---

### Trigger Phrase Recommendations

The OSS comment format introduces new vocabulary (repo names, license names, academic author names) that must be evaluated for trigger phrase utility. The principle: a trigger phrase is useful only if it discriminates between files — it should route to exactly one file, not many.

**Vocabulary evaluation table:**

| Term | Source | Discriminates? | Recommendation |
|---|---|---|---|
| `Apache 2.0` | License name | ❌ No — appears in 7+ files | **Do NOT add as trigger** |
| `MIT` | License name | ❌ No — appears in 9+ files | **Do NOT add as trigger** |
| `Boost Software License` | License name | ❌ No — appears in 6+ files | **Do NOT add as trigger** |
| `boostorg` | Repo org | ❌ No — appears in lockfree, iterator, 2+ files | **Do NOT add as trigger** |
| `facebook/folly` | Repo name | 🟡 Partial — maps to ESE-17 + ESE-24 only | Use in both those files, not as a discriminator between them |
| `Michael-Scott queue` | Algorithm | ✅ Yes — maps uniquely to ESE-24 | **Add to ESE-24 trigger block** |
| `Treiber stack` | Algorithm | ✅ Yes — maps uniquely to ESE-24 | **Add to ESE-24 trigger block** |
| `ABA problem` | Algorithm concept | ✅ Yes — maps uniquely to ESE-24 | **Add to ESE-24 trigger block** |
| `tagged pointer` | Algorithm concept | ✅ Yes — maps uniquely to ESE-24 | **Add to ESE-24 trigger block** |
| `hazard pointer` | Algorithm concept | ✅ Yes — maps uniquely to ESE-24 | **Add to ESE-24 trigger block** |
| `happens-before` | Memory model term | ✅ Yes — maps uniquely to ESE-17 | **Add to ESE-17 trigger block** |
| `Boehm-Adve` | Academic author | ✅ Yes — maps uniquely to ESE-17 | **Add to ESE-17 trigger block** |
| `acquire-release` | Memory ordering term | 🟡 Partial — ESE-17 primary, ESE-24 secondary | Add to ESE-17 only |
| `Chase-Lev` | Algorithm | ✅ Yes — maps uniquely to ESE-25 | **Add to ESE-25 trigger block** |
| `work-stealing` | Algorithm concept | ✅ Yes — maps uniquely to ESE-25 | **Add to ESE-25 trigger block** |
| `range-v3` | Library name | ✅ Yes — maps uniquely to ESE-03 | **Add to ESE-03 trigger block** |
| `fmtlib` | Library name | ✅ Yes — maps uniquely to ESE-06 | **Add to ESE-06 trigger block** |
| `Zverovich` | Author (fmtlib creator) | ✅ Yes — maps uniquely to ESE-06 | **Add to ESE-06 trigger block** |
| `iterator_facade` | Boost type | ✅ Yes — maps uniquely to ESE-19 | **Add to ESE-19 trigger block** |
| `Blumofe Leiserson` | Academic authors | ✅ Yes — maps uniquely to ESE-25 | **Add to ESE-25 trigger block** |

**Resulting trigger blocks per file (examples):**

ESE-24 (lock-free):
```markdown
<!-- triggers: lock-free queue, Michael-Scott queue, ABA problem, Treiber stack,
     tagged pointer, hazard pointer, atomic queue, lock-free data structure -->
```

ESE-17 (memory ordering):
```markdown
<!-- triggers: memory ordering, happens-before, acquire-release, seq_cst,
     relaxed ordering, release fence, Boehm-Adve, memory model -->
```

ESE-25 (thread pool / work-stealing):
```markdown
<!-- triggers: thread pool, work-stealing queue, Chase-Lev, Blumofe Leiserson,
     work queue, task scheduler, executor pattern -->
```

ESE-06 (std::format):
```markdown
<!-- triggers: std::format, custom formatter, fmtlib, formatter specialization,
     Zverovich, format spec, user-defined format -->
```

ESE-03 (ranges):
```markdown
<!-- triggers: std::ranges, ranges pipeline, range-v3, views::filter,
     views::transform, lazy evaluation, ranges adaptor -->
```

**The license name vocabulary (Apache 2.0, MIT, Boost) must NOT appear in any `<!-- triggers: -->` block. It has zero disambiguation power and will cause every file with that license to compete for the same query slots.**

---

### Updated Test Case Scope for cpp-c++20.yaml

The original requirement was ≥15 test cases with ≥3 `must_not_retrieve` disambiguation tests. With the OSS approach, the following test case categories are required. Minimum count is revised to **≥20 test cases** with **≥6 `must_not_retrieve` tests**.

**Category A — Algorithm routing (original requirement, now enriched with OSS vocabulary):**

```yaml
- id: tc-cpp20-001
  question: "How do I implement a lock-free queue in C++?"
  expected_laws: [ENG-3.1, ENG-6.1]
  expected_avatars: [cpp/examples/ENG-6.1-lock-free-intro.md, cpp/examples/ESE-24-lockfree-queue.md]
  must_not_retrieve: [cpp/oss-reference-registry.yaml, cpp/ref-concurrency.md]
  note: "Programming query must route to example, not to registry"

- id: tc-cpp20-002
  question: "What is the ABA problem and how do I prevent it?"
  expected_laws: [ENG-6.1]
  expected_avatars: [cpp/examples/ESE-24-lockfree-queue.md]
  must_not_retrieve: [cpp/oss-reference-registry.yaml]

- id: tc-cpp20-003
  question: "How does work-stealing improve thread pool throughput?"
  expected_laws: [ENG-3.1]
  expected_avatars: [cpp/examples/ESE-25-thread-pool.md]
  must_not_retrieve: [cpp/oss-reference-registry.yaml]

- id: tc-cpp20-004
  question: "What is the difference between acquire and release memory ordering?"
  expected_laws: [ENG-6.1]
  expected_avatars: [cpp/examples/ESE-17-memory-ordering.md]
  must_not_retrieve: [cpp/oss-reference-registry.yaml, cpp/ref-advanced-cpp.md]
```

**Category B — OSS registry routing (NEW — tests that the registry surfaces for attribution queries but NOT for programming queries):**

```yaml
- id: tc-cpp20-010
  question: "Which OSS repositories is the C++ avatar content derived from?"
  expected_avatars: [cpp/oss-reference-registry.yaml]
  must_not_retrieve: [cpp/examples/ESE-24-lockfree-queue.md, cpp/examples/ESE-17-memory-ordering.md]
  note: "Attribution query must route to registry only"

- id: tc-cpp20-011
  question: "What license is the lock-free queue example content under?"
  expected_avatars: [cpp/oss-reference-registry.yaml]
  must_not_retrieve: [cpp/examples/ESE-24-lockfree-queue.md]

- id: tc-cpp20-012
  question: "Can I use the C++ avatar examples in a commercial product?"
  expected_avatars: [cpp/oss-reference-registry.yaml]
```

**Category C — Author/book false positive prevention (NEW — prevents Further Reading footer contamination):**

```yaml
- id: tc-cpp20-020
  question: "How does Williams explain the happens-before relationship?"
  expected_avatars: [cpp/examples/ESE-17-memory-ordering.md]
  must_not_retrieve: [cpp/examples/ESE-24-lockfree-queue.md, cpp/examples/ESE-25-thread-pool.md]
  note: "Williams is in the footer of ALL concurrency files — the correct file must win on content, not footer"

- id: tc-cpp20-021
  question: "What does Josuttis say about C++20 ranges?"
  expected_avatars: [cpp/examples/ESE-03-ranges.md]
  must_not_retrieve: [cpp/examples/ESE-06-format.md, cpp/oss-reference-registry.yaml]
  note: "Josuttis mentioned in multiple footers — content wins"
```

**Category D — Disambiguation within ENG-3.1 (original requirement, now confirms router function):**

```yaml
- id: tc-cpp20-030
  question: "How do I write a C++ ranges pipeline to filter flight records?"
  expected_laws: [ENG-3.1]
  expected_avatars: [cpp/examples/ENG-3.1-ranges-views.md]
  must_not_retrieve: [cpp/examples/ENG-6.1-thread-safety.md, cpp/examples/ENG-3.1-coroutines.md]
  note: "Confirms ENG-3.1 dispatch router routes to ranges, not coroutines"

- id: tc-cpp20-031
  question: "How do I implement a C++20 coroutine generator?"
  expected_laws: [ENG-3.1]
  expected_avatars: [cpp/examples/ENG-3.1-coroutines.md]
  must_not_retrieve: [cpp/examples/ENG-3.1-ranges-views.md, cpp/examples/ENG-6.1-memory-ordering.md]

- id: tc-cpp20-032
  question: "How do I enforce thread safety in C++?"
  expected_laws: [ENG-6.1]
  expected_avatars: [cpp/examples/ENG-6.1-thread-safety.md]
  must_not_retrieve: [cpp/examples/ENG-3.1-ranges-views.md, cpp/examples/ENG-3.1-coroutines.md]
```

**Category E — Cross-contamination regression (tests that OSS citation terms don't bleed across files):**

```yaml
- id: tc-cpp20-040
  question: "How do I use fmtlib to format custom types?"
  expected_avatars: [cpp/examples/ESE-06-format.md]
  must_not_retrieve: [cpp/oss-reference-registry.yaml, cpp/examples/ESE-03-ranges.md]

- id: tc-cpp20-041
  question: "How does range-v3 implement filter and transform?"
  expected_avatars: [cpp/examples/ESE-03-ranges.md]
  must_not_retrieve: [cpp/oss-reference-registry.yaml, cpp/examples/ESE-44-expression-templates.md]
```

---

### Updated Required Actions

| # | Action | Priority | Reviewer | Status |
|---|--------|----------|----------|--------|
| R4-01 | Split `ref-cpp20-features.md` into `ref-cpp20-core.md` + `ref-cpp20-runtime.md`. Each split target: **≤2,800t** (revised from ≤3,500t to leave 700t citation overhead budget). | 🔴 Blocking | R4 | Open |
| R4-02 | Audit `ref-concurrency.md` (5,176t today) for immediate retroactive split before ESE-17/24/25 adds content. Post-ESE projection: ~7,400t — unacceptable. | 🔴 Blocking (NEW) | R4 | Open |
| R4-03 | Audit `ref-testing-ci.md` (6,852t today) for immediate split, independent of ESE scope. Already the largest file in the avatar by a wide margin. | 🔴 Blocking (NEW) | R4 | Open |
| R4-04 | Create `tools/rag-eval/test-cases/cpp-c++20.yaml` with **≥20** test cases (revised from ≥15) including ≥6 `must_not_retrieve` tests covering: OSS registry routing, Further Reading author contamination, and ENG-3.1 dispatcher validation. | 🔴 Blocking | R4 | Open |
| R4-05 | Create `examples/ENG-3.1-index.md` dispatch router (ESE-56). | 🔴 Blocking | R4 | Open |
| R4-06 | Update ESE-55 to require `ENG-6.1-index.md` update for all 7 new ENG-6.1 files. Add missing lock-free-intro task. | 🔴 Blocking | R4 | Open |
| R4-07 | **NEW — Further Reading embedding exclusion:** Define `<!-- no-embed -->` / `<!-- /no-embed -->` annotation convention. Update RAG pipeline config to skip marked sections during embedding computation. All Further Reading sections and OSS derivation headers MUST use this annotation. Add to ESE-01 acceptance criteria. | 🔴 Blocking (NEW) | R4 | Open |
| R4-08 | **NEW — OSS Registry scoping:** Set `document_type: metadata` in `oss-reference-registry.yaml` frontmatter. Define restrictive trigger set (license/attribution queries only). Add pre-commit test that registry does NOT appear in top_k for any programming query in cpp-c++20.yaml. | 🔴 Blocking (NEW) | R4 | Open |
| R4-09 | **NEW — OSS comment format revision:** Move license/repo/path metadata to `<!-- no-embed -->` block; keep algorithm name and academic citation in heading/trigger comment where embedding can use it. Revise the derivation comment format spec in PROPOSAL.md accordingly. | 🟠 High | R4 | Open |
| R4-10 | Add algorithm-specific trigger phrases to each new ESE file's `<!-- triggers: -->` block per the table above. Add `<!-- triggers: -->` convention to ESE-01. | 🟠 High | R4 | Open |
| R4-11 | Add pre-commit token ceiling check to constitution-lint: any ref file commit that pushes a file over **2,800t** should fail the check with a message directing the author to split the file. | 🟠 High | R4 | Open |
| R4-12 | Move governance wiring checkpoint (`reference-index.md` + `AVATAR-RAG-INDEX.yaml` updates) to the end of each phase, not only Phase 8. | 🟠 High | R4 | Open |
| R4-13 | Add law citations to PROPOSAL.md header: ENG-3.2, ENG-5.5, ENG-6.5, ENG-6.7. | 🟡 Medium | R4 | Open |

---

### Summary

The OSS source analysis is sound provenance engineering that resolves R1, R2, and R3 concerns. It has no effect on R4's blocking issues because those issues are structural, not derivational. More importantly, the structural changes the OSS approach mandates introduce four new RAG concerns that must be addressed alongside the original four blocking issues.

**The eight items that must be resolved before any ESE file is committed:**

1. Token split of `ref-cpp20-features.md` to ≤2,800t per split file (R4-01)
2. Emergency retroactive split of `ref-concurrency.md` (R4-02)
3. Emergency retroactive split of `ref-testing-ci.md` (R4-03)  
4. RAG test cases in `cpp-c++20.yaml` ≥20 with ≥6 `must_not_retrieve` (R4-04)
5. ENG-3.1 dispatch router created (R4-05)
6. ENG-6.1-index.md update in ESE-55 scope (R4-06)
7. `<!-- no-embed -->` annotation for Further Reading blocks with pipeline enforcement (R4-07)
8. `oss-reference-registry.yaml` scoped as metadata document with restricted trigger set (R4-08)

Items 7 and 8 are new. Items 1–6 were always present but Items 1–3 are now more urgent given the confirmed pre-existing token overrun in production ref files.

---

*R4 response compiled in response to OSS-SOURCE-ANALYSIS.md (2026-04-24). RAG pipeline configuration findings are based on `tools/rag-eval/config.yaml` (`top_k: 3`, `law_retrieval threshold: 0.85`). Token estimates use 4 chars/token approximation consistent with prior BLOCKING Issue 1 analysis; verified against measured byte counts of current avatar ref files.*
