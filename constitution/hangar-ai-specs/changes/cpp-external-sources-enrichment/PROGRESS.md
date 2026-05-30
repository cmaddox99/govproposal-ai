# PROGRESS: cpp-external-sources-enrichment (ESE)

**Proposal:** `hangar-ai-specs/changes/cpp-external-sources-enrichment/PROPOSAL.md`
**Status:** CLEAR TO MERGE — All 88 tasks complete (73 core + 10 Amendment A + 5 Amendment D); Amendment E (8 items) is post-merge backlog; 1894 tests passing
**Branch:** `feat/cpp-external-sources-enrichment`

---

## Governance Sign-Off

| Checkpoint | Status | Notes |
|---|---|---|
| ENG-4.1 Atomic TDD compliance | ✅ Confirmed | All production code preceded by failing test; RED→GREEN→REFACTOR cycle enforced each commit |
| ENG-6.7 Audit Trail | ✅ Confirmed | All commits reference scenario IDs; tasks.md tracks completion with commit hashes |
| ENG-11.1 Hangar SDD artifacts | ✅ Confirmed | PROPOSAL.md + tasks.md + PROGRESS.md (this file) present |
| ENG-10.1 Law reference validity | ✅ Confirmed | `test_no_bare_law_references` passing; all ENG-*/PRD-*/BUS-* refs are hyperlinked |
| Prerequisite CBF merged | ✅ Confirmed | `cpp-brownfield-first` (PR #49) merged to main; ESE branch rebased on main post-merge |

---

## CBF Prerequisite Summary

The `cpp-brownfield-first` (CBF) proposal was a prerequisite for ESE. It was developed on
`feat/cpp-brownfield-first` and merged via PR #49. CBF delivered the following ESE-blocked
tasks ahead of schedule:

| ESE Task | CBF Deliverable |
|---|---|
| ESE-V1/V2 | Version routing wired; AVATAR-RAG-INDEX.yaml updated |
| ESE-V3/V4 | cpp20-features and concurrency-advanced ref files split (Part 1 / Part 2) |
| ESE-V5 | ESE-56–65 bridge deliverables pre-created |
| ESE-01 | ref-cpp20-features-part1/2 skeletons created |
| ESE-21 | ref-concurrency-advanced-part1/2 skeletons created |
| ESE-56–65 | JNI, brownfield, thread-local, FAR117, const-char-lifetime files created |

---

## Version Annotation Summary

All 48 substantive ESE tasks carry `cpp_version_min` annotations per ESE-V1 / CBF-12:

| Version | Count | Representative tasks |
|---|---|---|
| C++20 | 22 | ESE-02–16, ESE-34–36, ESE-42–43 |
| C++17 | 4 | ESE-17–18, ESE-40–41 |
| C++14 | 2 | ESE-50–51 |
| C++11 | 18 | ESE-19–20, ESE-22–33, ESE-37–39 |
| C++98 | 2 | ESE-55 (gmtime_r), ESE-63 (MSVC 6.0 golden-master) |

---

## Round 4 Review Panel — Outstanding Items

See `PANEL-UPDATE-ROUND-4.md` for full verdicts. Key open items:

| ID | Description | Owner |
|---|---|---|
| R8-4 | FAR 117 C++98 `gmtime_r`/`mktime` timezone arithmetic — partial | ESE-00.3a (proposed) |
| R8-6 | CRTP example file wiring into AVATAR-RAG-INDEX.yaml | ESE (deferred to CRTP task) |
| R8-7 | Pre-modern library equivalence table in brownfield-survival.md | ESE (deferred) |
| R5 | ESE-06 spec: remove CVE-2024 hallucination; ESE-24: remove "lock-free" claim | Fix before those tasks execute |

---

## External Source Library

Historical sources incorporated per `avatars/technology/cpp/SOURCES.md`:

- **Tier 1 (freely derivable):** Core Guidelines, Howard Hinnant date, fmtlib, range-v3, GSL, Loki, Jason Turner GitHub, ISO papers
- **Tier 2 (cite/link only):** Sutter GOTW, Stroustrup FAQ, Filipek cppstories.com, cppreference
- **Tier 3 (clean-room only):** Coplien AC++PSI, Meyers EC++/EMC++, Sutter Exceptional C++, Alexandrescu MCD, Feathers WELC, Josuttis STL/C++17/C++20

Full curation rationale: `docs/guides/avatars/cpp-source-curation-guide.md`

---

## ESE-00.5 — Copilot Enterprise Indemnification Governance (R2-F2)

**Status:** Open — governance record only, no code change required.

This entry documents the R2 (IP/Copyright Counsel) open finding from PANEL-UPDATE-ROUND-4.md
(R2-F2 ❌ OPEN) and serves as the tracking record per Amendment D (ESE-D4).

| Governance Item | Status | Notes |
|---|---|---|
| AA Copilot Enterprise agreement | **Unverified** | Must be confirmed with IT Procurement / Legal. A qualifying Copilot Enterprise license is prerequisite for Microsoft Copyright Shield coverage on Copilot-assisted output. |
| Microsoft Copyright Shield scope | **Unverified** | Shield applies to Copilot Enterprise subscribers. Confirm with Microsoft TAM that ESE avatar repositories are within scope. |
| Duplication filter (output screening) | **Unverified** | Copilot Enterprise enables duplication detection that screens suggestions matching public code. Confirm this filter is active for developers working in this repository. |

**Action required before production deployment of ESE avatar files:**
1. IT Procurement to confirm active Copilot Enterprise agreement (not Copilot Business or Individual)
2. Legal to confirm Copyright Shield covers AA's use of Copilot output in this repository
3. Copilot Enterprise admin to confirm duplication filter is enabled for affected developer accounts

**If any of the above cannot be confirmed**, consult R2 (IP/Copyright Counsel) guidance in
`PANEL-UPDATE-ROUND-4.md` lines ~50–70 for fallback posture (standard Tier 1/2/3 clean-room
protocol already implemented in `avatars/technology/cpp/SOURCES.md` provides baseline protection).

*Recorded: 2026-04-28 — Amendment D close-out (ESE-D4). Owner: Legal / IT Procurement.*
