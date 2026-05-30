# Amendment D Confirmation Panel Review
## C++ Avatar External Sources Enrichment (PR #51)

**Branch:** `feat/cpp-external-sources-enrichment`
**Reviewed commit:** `b7008bd` — Amendment D implementation (ESE-D1 through ESE-D5)
**Reviewers:** R1–R8 (full panel — same personas as Round 5 missing-reviewer panel)
**Review date:** 2026-04-28
**Review type:** Amendment D close-out confirmation — triple-pass (dual independent + tiebreaker)

---

## Context

Amendment D was documented in Round 5 close-out (commit `c4f6aae`) and implemented in commit
`b7008bd`. This panel confirms whether each D-1 through D-5 implementation adequately resolves
the original Round 5 findings, under the stated priority:

> **Correctness > Understandability > Token Budget**

---

## Amendment D Implementation Summary

| Task | What Was Done |
|------|---------------|
| **D-1** | `ref-safety-far117-cwr.md` frontmatter: qualified `cpp_version_note` to say governance patterns are version-agnostic but code examples use C++11+; C++98 teams directed to "the platform team" |
| **D-2** | CRTP wired as routing hint in AVATAR-RAG-INDEX.yaml; stale "route here until crtp.md ships" note removed from `ref-templates-metaprogramming.md`; `examples/` entries removed from tier prefer lists (CI test constraint) |
| **D-3** | `## Further Reading` sections added to `ref-cpp20-features-part1.md`, `ref-concurrency-advanced-part1.md`, `ref-templates-advanced.md`, `ref-core-modern-idioms.md` per SOURCES.md Tier 3 citation format |
| **D-4** | ESE-00.5 Copilot Enterprise indemnification governance note appended to `PROGRESS.md` |
| **D-5** | `rag_exclude: true` removed from `ENG-6.1-jni-thread-cpp98.md` (194 lines) and `ENG-6.1-timezone-cpp14.md` (160 lines); both already in AVATAR-RAG-INDEX.yaml routing hints |

---

## Pass 1 Findings (Independent)

### R1 — Senior Copyright Counsel

| ID | Severity | File | Summary |
|----|----------|------|---------|
| A-D1-R1-01 | ✅ RESOLVED | `ref-cpp20-features-part1.md` lines 368–377 | D-3 Further Reading uses proper Tier 3 clean-room format |
| A-D1-R1-02 | ✅ RESOLVED | `ENG-6.1-jni-thread-cpp98.md` lines 27–29 | Apache 2.0 attribution maintained; activation does not change IP exposure |
| A-D1-R1-03 | ✅ RESOLVED | `ENG-6.1-timezone-cpp14.md` lines 120–124 | MIT HowardHinnant/date attribution maintained |
| A-D1-R1-04 | 🔵 MINOR | `ref-templates-advanced.md` lines 207–216 | Coplien (1992) citation lacks full title per SOURCES.md format |

**R1 Pass 1 Verdict:** ✅ All copyright findings resolved. D-3 citations are compliant.

---

### R2 — Senior Software Application Lawyer

| ID | Severity | File | Summary |
|----|----------|------|---------|
| A-D2-R2-01 | ✅ RESOLVED | `PROGRESS.md` lines 77–99 | ESE-00.5 governance adequately documents gap with remediation path |
| A-D2-R2-02 | 🟡 IMPORTANT | `ref-safety-far117-cwr.md` lines 3–8 | "Platform team" redirect creates documented gap acknowledgment; defensibility depends on redirect leading to real resource |
| A-D2-R2-03 | ✅ RESOLVED | `ENG-6.1-jni-thread-cpp98.md` | D-5 activation does not create new liability — content is accurate |

**R2 Pass 1 Verdict:** ⚠️ PARTIAL — D-4 fully resolved. D-1 creates honest disclosure record but redirect destination is undefined.

---

### R3 — AI & Software Ethics Expert

| ID | Severity | File | Summary |
|----|----------|------|---------|
| A-D3-R3-01 | ✅ RESOLVED | `ref-cpp20-features-part1.md` | Josuttis, Stroustrup, ISO draft are correct authoritative sources |
| A-D3-R3-02 | ✅ RESOLVED | `ref-concurrency-advanced-part1.md` | Williams and Boehm & Adve are definitive for concurrency content |
| A-D3-R3-03 | 🔵 MINOR | `ref-templates-advanced.md` | Missing Vandevoorde/Josuttis *C++ Templates: The Complete Guide* (2017) — definitive templates reference |
| A-D3-R3-04 | ✅ RESOLVED | `ref-core-modern-idioms.md` | Meyers, Sutter/Alexandrescu, Turner appropriately cited |

**R3 Pass 1 Verdict:** ✅ D-3 substantially resolved. E3 from Round 4 closed. Minor citation gap for templates.

---

### R4 — Constitutional AI RAG Expert

| ID | Severity | File | Summary |
|----|----------|------|---------|
| A-D4-R4-01 | 🟡 IMPORTANT | `AVATAR-RAG-INDEX.yaml` line 1241 | CRTP routing hint too specific — requires CRTP keyword; "avoid virtual?" queries miss it |
| A-D4-R4-02 | 🟡 IMPORTANT | `AVATAR-RAG-INDEX.yaml` lines 1322–1349 | `cpp_version_min: 11` creates fundamental version conflict blocking brownfield prefer-list inclusion |
| A-D4-R4-03 | ✅ RESOLVED | `AVATAR-RAG-INDEX.yaml` lines 1248–1250 | D-5 stubs already wired in routing hints; no index update needed |
| A-D4-R4-04 | 🔵 MINOR | `ref-templates-metaprogramming.md` line 342 | CRTP note updated but provides no direct link to CRTP example file |

**R4 Pass 1 Verdict:** ⚠️ PARTIAL — D-5 wiring resolved. D-2 CRTP routing insufficient for general polymorphism queries.

---

### R5 — C++ Master Technical Review

| ID | Severity | File | Summary |
|----|----------|------|---------|
| A-D5-R5-01 | ✅ RESOLVED | `ENG-6.1-jni-thread-cpp98.md` | `pthread_key_t` / `TlsAlloc` patterns technically correct; edge cases covered |
| A-D5-R5-02 | ✅ RESOLVED | `ENG-6.1-timezone-cpp14.md` | HowardHinnant/date usage correct for FAR 117 DST/UTC boundary calculations |
| A-D5-R5-03 | 🔵 MINOR | `ENG-6.1-timezone-cpp14.md` frontmatter | `cpp_version_min: 11` while note says "C++11/14" — minor clarity issue |
| A-D5-R5-04 | ✅ RESOLVED | `ref-templates-advanced.md` | Further Reading citation editions and descriptions accurate |

**R5 Pass 1 Verdict:** ✅ D-5 content is technically correct. Both files ready for activation.

---

### R6 — Senior AA Engineer

| ID | Severity | File | Summary |
|----|----------|------|---------|
| A-D6-R6-01 | 🟡 IMPORTANT | `ref-safety-far117-cwr.md` lines 3–8 | "Platform team" redirect not actionable — which team, what channel, what contact? |
| A-D6-R6-02 | ✅ RESOLVED | `ENG-6.1-jni-thread-cpp98.md` | JNI file has sufficient content for CWR `pthread_key_t` threading problems |
| A-D6-R6-03 | ✅ RESOLVED | `ENG-6.1-timezone-cpp14.md` | Timezone file sufficient for C++11/14 FAR 117 DST calculations |
| A-D6-R6-04 | 🟡 IMPORTANT | `ref-safety-far117-cwr.md` | Every code example uses `std::chrono` (C++11+); C++98 CWR developer cannot use any code in the file |

**R6 Pass 1 Verdict:** ⚠️ PARTIAL — D-5 fully resolved and actionable. D-1 "platform team" is unactionable; C++98 timezone gap persists.

---

### R7 — Adversarial Plaintiff's Litigation Attorney

| ID | Severity | File | Summary |
|----|----------|------|---------|
| A-D7-R7-01 | 🟡 IMPORTANT | `ref-safety-far117-cwr.md` lines 3–8 | New frontmatter creates "known gap with redirect" record; defensibility depends on redirect destination existing |
| A-D7-R7-02 | ✅ RESOLVED | `PROGRESS.md` ESE-00.5 section | "Unverified" with action items is due-diligence documentation, not admission |
| A-D7-R7-03 | 🔵 MINOR | `ENG-6.1-jni-thread-cpp98.md`, `ENG-6.1-timezone-cpp14.md` | Activating files elevates to "published guidance" liability standard — content accurate, review cadence recommended |

**R7 Pass 1 Verdict:** ⚠️ PARTIAL — D-4 and D-5 resolved. D-1 creates honest disclosure record; platform team redirect must lead to real resource.

---

### R8 — Cross-Version Completeness Auditor

| ID | Severity | File | Summary |
|----|----------|------|---------|
| A-D8-R8-01 | 🔴 BLOCKING (Pass 1) | `AVATAR-RAG-INDEX.yaml` lines 1322–1349 | R8-6 not satisfied — CRTP routing hint requires CRTP-keyword query; C++98 polymorphism gap persists |
| A-D8-R8-02 | 🟡 IMPORTANT | `ref-safety-far117-cwr.md` lines 3–8 | C++98 FAR 117 timezone gap persists; frontmatter acknowledges but does not fill gap |
| A-D8-R8-03 | 🔵 MINOR | Cross-tier analysis | Brownfield underserved; CRTP and timezone gaps remain as Amendment E candidates |
| A-D8-R8-04 | ✅ RESOLVED | `AVATAR-RAG-INDEX.yaml` lines 1315–1370 | Tier prefer/avoid structure is version-safe; tier architecture sound |

**R8 Pass 1 Verdict:** ⚠️ PARTIAL — Tier structure resolved. R8-6 (CRTP wiring) and R8-NEW-1 (C++98 timezone) remain open.

---

## Pass 2 Findings (Independent)

Pass 2 confirmed the same file-level findings as Pass 1. Key convergences and divergences:

| Finding Area | Pass 1 | Pass 2 | Status |
|---|---|---|---|
| D-1 "platform team" unactionable | 🟡 IMPORTANT | ⚠️ PARTIAL | ✅ Confirmed |
| D-1 C++98 FAR 117 timezone gap | 🟡 IMPORTANT | ⚠️ PARTIAL | ✅ Confirmed |
| D-2 CRTP routing hint insufficient | 🟡 IMPORTANT | ⚠️ PARTIAL | ✅ Confirmed |
| D-2 CRTP `cpp_version_min` conflict | 🟡 IMPORTANT | 🟡 IMPORTANT | ✅ Confirmed |
| D-3 Further Reading citations correct | ✅ RESOLVED | ✅ RESOLVED | ✅ Confirmed |
| D-4 ESE-00.5 governance note | ✅ RESOLVED | ✅ RESOLVED | ✅ Confirmed |
| D-5 JNI/timezone activation | ✅ RESOLVED | ✅ RESOLVED | ✅ Confirmed |
| R8-01 CRTP routing severity | 🔴 BLOCKING | 🟡 IMPORTANT | ⚠️ **Severity divergence → Pass 3** |
| R7-03 D-5 publication liability severity | 🔵 MINOR | 🟡 IMPORTANT | ⚠️ **Severity divergence → Pass 3** |

**Pass 2 Merge Recommendation:** MERGE WITH NOTED ITEMS (HIGH — ≥85% agreement on findings)

---

## Pass 3 — Tiebreaker Adjudication

### Finding 1: R8-01 — CRTP Routing Sufficiency

**Question:** Is the C++98 polymorphism routing gap BLOCKING (prevents merge) or IMPORTANT (Amendment E)?

**Evidence examined:**
- `AVATAR-RAG-INDEX.yaml` brownfield tier prefer list: contains `refs/legacy/ref-legacy-navigation.md`
- `refs/legacy/ref-legacy-navigation.md` line 55: Contains idiom table entry `CRTP | ✅ Preserve C++98/14 | Do not refactor to virtual; add to brownfield routing when crtp.md ships`
- `ref-brownfield-survival.md`: NO CRTP or polymorphism guidance found
- `ref-templates-metaprogramming.md` line 342: Has CRTP note but `cpp_version_min: 11` — not delivered to C++98 brownfield developers

**Verdict: 🟡 IMPORTANT (not BLOCKING)**

`ref-legacy-navigation.md` — which IS in the C++98 brownfield prefer list and has `cpp_version_min: 98` — contains a one-line CRTP idiom entry directing developers away from virtual dispatch. This provides a minimal but functional guidance path. The gap is suboptimal (no detailed C++98 CRTP examples), not a correctness failure (no guidance at all). Creating a C++98-safe CRTP file is appropriate Amendment E scope and does not require blocking this merge.

---

### Finding 2: R7-03 — D-5 Publication Liability Standard

**Question:** Must a formal review cadence be established BEFORE activating files, or is it post-merge?

**Evidence examined:**
- Both `ENG-6.1-jni-thread-cpp98.md` and `ENG-6.1-timezone-cpp14.md` confirmed technically correct by R5 in both Pass 1 and Pass 2
- `ENG-6.1-timezone-cpp14.md` line 21 explicitly documents FAR 117 liability context
- No existing review cadence policy for C++ avatar example files anywhere
- R5 technical review in dual-pass constitutes pre-activation expert review

**Verdict: 🔵 MINOR (not IMPORTANT)**

Content is demonstrably correct per expert C++ review in two independent passes. Review cadence is a systemic process improvement for the entire C++ avatar — not a D-5-specific gate. Both files were technically reviewed by an expert reviewer (R5) before activation; formal cadence is a good-practice post-merge quality item.

---

## Consolidated Final Findings

### D-Task Resolution Summary

| Task | Final Status | Remaining Concern |
|------|-------------|-------------------|
| **D-1** — FAR 117 frontmatter | ⚠️ PARTIAL | "Platform team" redirect undefined; C++98 timezone arithmetic gap unfilled |
| **D-2** — CRTP routing | ⚠️ PARTIAL | Routing hint added; `ref-legacy-navigation.md` provides minimal fallback path; R8-6 not fully met |
| **D-3** — Further Reading | ✅ RESOLVED | 4 files cite correct Tier 3 sources; R3 E3 from Round 4 closed |
| **D-4** — ESE-00.5 governance | ✅ RESOLVED | Due-diligence record defensible; action items documented with owner |
| **D-5** — Stub activation | ✅ RESOLVED | Both files technically correct; activated; routing pre-wired |

---

### BLOCKING Findings: 0

None. No findings prevent merge.

---

### IMPORTANT Findings: 4

**I-1** (R2, R6, R7, R8) — `ref-safety-far117-cwr.md` frontmatter
- "Platform team" redirect is undefined — no team name, contact, or wiki link
- C++98 CWR developers have governance prose but zero usable code patterns for timezone arithmetic
- **Amendment E action:** Add actual resource identifier OR create `examples/ENG-6.1-timezone-cpp98.md` with `gmtime_r`/`mktime`/`difftime` patterns

**I-2** (R4, R8) — `AVATAR-RAG-INDEX.yaml` CRTP routing hint scope
- Routing hint requires CRTP-specific keywords; "avoid virtual overhead?" queries do not match
- `ref-legacy-navigation.md` provides one-line fallback in brownfield prefer list
- **Amendment E action:** Add broader alias routing hints ("avoid virtual dispatch", "polymorphism without vtable") OR create `refs/legacy/ref-static-polymorphism.md` for brownfield prefer list

**I-3** (R4, R8) — `ENG-3.1-crtp.md` version conflict with brownfield tier
- `cpp_version_min: 11` cannot enter C++98 brownfield prefer list per CI test
- CRTP is a C++98 pattern but the example file uses C++11+ syntax
- **Amendment E action:** Create `ENG-3.1-crtp-cpp98.md` with `cpp_version_min: 98` using pure C++98 template syntax, or restructure `ENG-3.1-crtp.md` with version-gated sections

**I-4** (R7) — D-5 activated files carry higher "published guidance" liability standard
- Content is correct; future edits to these files must maintain accuracy standard
- **Amendment E action:** Establish review cadence for safety-critical example files (`ENG-6.1-jni-thread-cpp98.md`, `ENG-6.1-timezone-cpp14.md`)

---

### MINOR Findings: 4

| ID | Reviewer | Finding |
|----|----------|---------|
| M-1 | R1 | Coplien (1992) citation in `ref-templates-advanced.md` lacks full title *Advanced C++ Programming Styles and Idioms* |
| M-2 | R3 | `ref-templates-advanced.md` missing Vandevoorde/Josuttis *C++ Templates: The Complete Guide* (2017) |
| M-3 | R4 | CRTP note in `ref-templates-metaprogramming.md` line 342 has no direct link to CRTP example file |
| M-4 | R8 | `ENG-6.1-timezone-cpp14.md` title/routing says "C++14" but `cpp_version_min: 11` — naming inconsistency |

---

### Confirmed Resolved from Round 5 / Amendment D

| Reviewer | Items Confirmed Closed |
|----------|----------------------|
| R1 | Apache 2.0 attribution (D-5), MIT attribution (D-5), Further Reading Tier 3 format (D-3) |
| R2 | ESE-00.5 governance record (D-4), D-5 activation liability |
| R3 | E3 Further Reading for substantive ref files (D-3) — ALL 4 files now have Further Reading |
| R4 | D-5 stub routing pre-wired in AVATAR-RAG-INDEX.yaml |
| R5 | `pthread_key_t`/`TlsAlloc` correctness (D-5), HowardHinnant/date correctness (D-5), citation editions (D-3) |
| R6 | JNI threading file actionable for CWR (D-5), timezone C++14 file actionable (D-5) |
| R7 | ESE-00.5 "Unverified" documentation is due-diligence, not admission (D-4), D-5 content correct |
| R8 | Tier prefer/avoid structure version-safe; tier architecture sound |

---

## Reviewer Agreement

| Metric | Value |
|--------|-------|
| Pass 1 / Pass 2 finding convergence | 100% — all findings identified in both passes |
| Severity disagreements | 2 (R8-01 BLOCKING→IMPORTANT; R7-03 MINOR→IMPORTANT) |
| Pass 3 required | YES — R8-01 had merge-consequence severity divergence |
| Post-Pass-3 confidence | **HIGH** |

---

## Merge Recommendation

### ✅ CLEAR TO MERGE

**D-3, D-4, and D-5 are fully resolved.** D-1 and D-2 are partially resolved with documented limitations — honest disclosure of scope (D-1) and test-constrained routing alternative (D-2). No findings prevent merge. Four IMPORTANT findings are tracked as Amendment E backlog items.

### Amendment E Backlog (post-merge, in priority order)

| Priority | Item | Owner | Rationale |
|----------|------|-------|-----------|
| P1 | Add actual resource identifier or C++98 POSIX timezone content to `ref-safety-far117-cwr.md` | Engineering | R6/R7 — unactionable redirect for CWR developers |
| P1 | Add broad CRTP routing aliases ("avoid virtual dispatch overhead") | Engineering | R4 — current hint requires CRTP keyword |
| P2 | Create `ENG-3.1-crtp-cpp98.md` with `cpp_version_min: 98` and C++98-safe examples | Engineering | R8 — R8-6 full satisfaction |
| P2 | Establish review cadence for activated safety-critical example files | Legal/Engineering | R7 — elevated published guidance standard |
| P3 | Add Vandevoorde/Josuttis *C++ Templates: The Complete Guide* (2017) to `ref-templates-advanced.md` | Engineering | R3 — completeness |
| P3 | Standardize Coplien citation to include full title | Engineering | R1 — citation consistency |

---

*Review conducted: 2026-04-28 — Amendment D commit `b7008bd`. Three-pass independent panel: Passes 1 and 2 independent (claude-opus-4.5, ~190s each); Pass 3 tiebreaker (claude-opus-4.5, 84s). Final confidence: HIGH.*
