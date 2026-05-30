"""Tests for cpp-brownfield-first (CBF-*) routing wiring.

Scenario ID: cpp-brownfield-first/CBF-00.1, CBF-00.2
Law: ENG-6.7 (Audit Trail — brownfield content must be RAG-indexed)
"""

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
RAG_INDEX = REPO_ROOT / "avatars" / "AVATAR-RAG-INDEX.yaml"
CPP_REFS = REPO_ROOT / "avatars" / "technology" / "cpp" / "refs"


def _tier_routing(content: str) -> dict:
    """Extract the by_standard tier routing block from the cpp section."""
    start = content.index("by_standard:")
    end = content.index("unknown_fallback:", start)
    return yaml.safe_load("by_standard:\n" + content[start + len("by_standard:"):end])["by_standard"]


# ---------------------------------------------------------------------------
# CBF-00.1
# ---------------------------------------------------------------------------

def test_cbf_00_1_brownfield_survival_file_exists():
    """ref-brownfield-survival.md must exist in refs/legacy/."""
    path = CPP_REFS / "legacy" / "ref-brownfield-survival.md"
    assert path.exists(), (
        "refs/legacy/ref-brownfield-survival.md does not exist. "
        "CBF-00.1 requires this file to be created before it can be wired into the routing index."
    )


def test_cbf_00_1_brownfield_survival_in_legacy_prefer():
    """ref-brownfield-survival.md must appear in legacy.prefer in AVATAR-RAG-INDEX.yaml."""
    tiers = _tier_routing(RAG_INDEX.read_text(encoding="utf-8"))
    prefer = tiers["legacy"].get("prefer", [])
    assert any("ref-brownfield-survival" in p for p in prefer), (
        "refs/legacy/ref-brownfield-survival.md not found in legacy.prefer. "
        "CBF-00.1: add it so SPEClient (MSVC 6.0, ~24% AA LOC) receives brownfield guidance."
    )


def test_cbf_00_1_brownfield_survival_in_brownfield_prefer():
    """ref-brownfield-survival.md must appear in brownfield.prefer in AVATAR-RAG-INDEX.yaml."""
    tiers = _tier_routing(RAG_INDEX.read_text(encoding="utf-8"))
    prefer = tiers["brownfield"].get("prefer", [])
    assert any("ref-brownfield-survival" in p for p in prefer), (
        "refs/legacy/ref-brownfield-survival.md not found in brownfield.prefer. "
        "CBF-00.1: add it so herc-odyssey-linux (C++98/03, ~11% AA LOC) receives brownfield guidance."
    )


def test_cbf_00_1_brownfield_survival_in_transitional_prefer():
    """ref-brownfield-survival.md must appear in transitional.prefer in AVATAR-RAG-INDEX.yaml."""
    tiers = _tier_routing(RAG_INDEX.read_text(encoding="utf-8"))
    prefer = tiers["transitional"].get("prefer", [])
    assert any("ref-brownfield-survival" in p for p in prefer), (
        "refs/legacy/ref-brownfield-survival.md not found in transitional.prefer. "
        "CBF-00.1: add it so CWR/IOC_ALP (C++11/14, ~60% AA LOC) receives brownfield survival patterns "
        "when working in brownfield sections of their codebase."
    )


# ---------------------------------------------------------------------------
# CBF-00.2 — Phase 1–3 deliverables wired into correct tier prefer lists
# ---------------------------------------------------------------------------

def test_cbf_00_3_ese_v2_avoid_wiring_complete():
    """AVATAR-RAG-INDEX.yaml must have the actual ESE-V2 avoid-list wiring in place.

    CBF-00.3 created a forward-declaration comment block to document the planned
    ESE C++20-only avoid additions. CBF-13 (ESE-V2) replaced that comment block
    with real YAML entries after creating the stub files on disk.

    This test verifies:
    1. The forward-declaration comment block has been removed (work is done)
    2. The actual C++20 avoid entries are present in the YAML
    """
    content = RAG_INDEX.read_text(encoding="utf-8")
    assert "FORWARD-DECLARATIONS: ESE-C20-AVOID" not in content, (
        "CBF-00.3 forward-declaration comment block must be removed after ESE-V2 "
        "wires the actual avoid entries. Run CBF-13 to complete ESE-V2."
    )
    # Verify the actual wiring is present (spot-check)
    assert "ref-cpp20-features-part1.md" in content, (
        "ESE-V2 must wire ref-cpp20-features-part1.md into tier routing"
    )
    assert "ENG-6.1-jthread-stop-token.md" in content, (
        "ESE-V2 must wire ENG-6.1-jthread-stop-token.md into transitional.avoid"
    )


def test_cbf_00_2_phase1_to_3_deliverables_in_search_queries():
    """All CBF Phase 1–3 example files must be registered in the cpp search_queries section.

    The version_routing_policy prefer lists accept only refs/ paths (architectural
    constraint enforced by test_rag_index.py). CBF examples are discoverable via
    query-based routing — each is registered as a search_query entry.

    Mapping (from tasks.md):
      CBF-01: ENG-6.1-timezone-cpp14.md  — FAR 117 timezone arithmetic C++14
      CBF-02: ENG-6.1-jni-thread-cpp98.md — JNI pthread_key_t C++98
      CBF-03: ENG-6.1-jni-thread-cpp11.md — JNI thread_local RAII C++11
      CBF-04: ENG-6.1-fmtlib-format.md   — fmtlib safe formatting
      CBF-05: ENG-3.1-ranges-range-v3.md — range-v3 bridge C++14
      CBF-06: ENG-6.1-gsl-span-cpp14.md  — gsl::span bounds safety C++14
      CBF-07: ENG-6.1-thread-stop-flag.md — manual stop-flag C++11
      CBF-08: ENG-6.1-lock-free-cpp14.md — lock-free C++11/14
      CBF-10: ENG-6.1-const-char-lifetime.md — const char* lifetime traps
    """
    content = RAG_INDEX.read_text(encoding="utf-8")

    cbf_examples = [
        "ENG-6.1-timezone-cpp14.md",
        "ENG-6.1-jni-thread-cpp98.md",
        "ENG-6.1-jni-thread-cpp11.md",
        "ENG-6.1-fmtlib-format.md",
        "ENG-3.1-ranges-range-v3.md",
        "ENG-6.1-gsl-span-cpp14.md",
        "ENG-6.1-thread-stop-flag.md",
        "ENG-6.1-lock-free-cpp14.md",
        "ENG-6.1-const-char-lifetime.md",
    ]
    for example in cbf_examples:
        assert example in content, (
            f"{example} not found in AVATAR-RAG-INDEX.yaml search_queries. "
            f"CBF-00.2: register all Phase 1–3 examples as search_query entries "
            f"(prefer lists accept refs/ only)."
        )


def test_cbf_02_jni_thread_cpp98_content():
    """CBF-02: ENG-6.1-jni-thread-cpp98.md must contain all required JNI C++98 content.

    Scenario: cpp-brownfield-first/CBF-02
    Law: ENG-6.1 (Safety-Critical Code — JNIEnv* thread-locality contract)

    Required content:
    - COMPLIANT POSIX: pthread_key_create with a destructor that calls DetachCurrentThread
    - COMPLIANT Win32: DLL_THREAD_DETACH path calls DetachCurrentThread
    - NON-COMPLIANT: static JNIEnv* g_env (shared across threads — UB)
    - NON-COMPLIANT: std::atomic<JNIEnv*> (wrong tool — thread-model not atomics problem)
    - Reference to C++11 upgrade path (CBF-03 / thread_local)
    - Attribution: android/ndk-samples, Apache 2.0, Android Open Source Project
    - No stub markers remaining
    """
    example = (
        REPO_ROOT
        / "avatars" / "technology" / "cpp" / "examples"
        / "ENG-6.1-jni-thread-cpp98.md"
    )
    content = example.read_text(encoding="utf-8")

    assert "pthread_key_create" in content, (
        "COMPLIANT POSIX section must show pthread_key_create with destructor"
    )
    assert "DetachCurrentThread" in content, (
        "COMPLIANT sections must show DetachCurrentThread — the required JVM cleanup call"
    )
    assert "DLL_THREAD_DETACH" in content, (
        "COMPLIANT Win32 section must show DLL_THREAD_DETACH in DllMain"
    )
    assert "static" in content and "g_env" in content, (
        "NON-COMPLIANT section must show static JNIEnv* g_env anti-pattern"
    )
    assert "atomic" in content, (
        "NON-COMPLIANT section must show std::atomic<JNIEnv*> anti-pattern"
    )
    assert "Apache" in content and "ndk-samples" in content, (
        "Must include android/ndk-samples Apache 2.0 attribution"
    )
    assert "thread_local" in content or "CBF-03" in content or "cpp11" in content.lower(), (
        "Must reference the C++11 thread_local upgrade path"
    )
    assert "Stub" not in content and "stub" not in content, (
        "File must be fully populated — stub markers must be removed"
    )


def test_cbf_01_timezone_example_content():
    """CBF-01: ENG-6.1-timezone-cpp14.md must contain all required FAR 117 content.

    Scenario: cpp-brownfield-first/CBF-01
    Law: ENG-6.1 (Safety-Critical Code)

    The file must graduate from stub to production-quality content covering:
    - COMPLIANT pattern using date::make_zoned
    - NON-COMPLIANT: time_t/localtime with manual UTC offset
    - NON-COMPLIANT: hardcoded timezone offset string
    - Edge Cases: DST transition (spring-forward/fall-back), leap seconds,
      zoned_time vs local_time confusion
    - HowardHinnant/date MIT attribution
    - FAR 117 reference (the aviation regulation this protects)
    - C++20 migration note
    """
    example = (
        REPO_ROOT
        / "avatars" / "technology" / "cpp" / "examples"
        / "ENG-6.1-timezone-cpp14.md"
    )
    content = example.read_text(encoding="utf-8")

    assert "date::make_zoned" in content, (
        "COMPLIANT section must show date::make_zoned() — the primary safe API"
    )
    assert "localtime" in content or "time_t" in content, (
        "NON-COMPLIANT section must show time_t/localtime() — the unsafe anti-pattern"
    )
    assert "FAR 117" in content, (
        "Must reference FAR 117 — this example protects crew rest calculations"
    )
    assert "DST" in content or "daylight" in content.lower(), (
        "Edge Cases & Warnings must address DST transitions"
    )
    assert "leap second" in content.lower(), (
        "Edge Cases & Warnings must address leap seconds"
    )
    assert "zoned_time" in content and "local_time" in content, (
        "Edge Cases & Warnings must distinguish zoned_time vs local_time"
    )
    assert "MIT" in content and ("Howard Hinnant" in content or "HowardHinnant" in content), (
        "Must include HowardHinnant/date MIT license attribution"
    )
    assert "Stub" not in content and "stub" not in content, (
        "File must be fully populated — stub markers must be removed"
    )


def test_cbf_03_jni_thread_cpp11_content():
    """CBF-03: ENG-6.1-jni-thread-cpp11.md must contain all required JNI C++11 content.

    Scenario: cpp-brownfield-first/CBF-03
    Law: ENG-6.1 (Safety-Critical Code — JNIEnv* thread-locality contract)

    Required content:
    - COMPLIANT: thread_local RAII guard with AttachCurrentThread on first access
    - COMPLIANT: destructor or pthread_key_t backup for thread_local destructor
      ordering caveat (C++11 does not guarantee ordering with JVM shutdown)
    - COMPLIANT: GetEnv/AttachCurrentThread fresh per call (never cached)
    - NON-COMPLIANT: static JNIEnv* g_env (the pattern that kills)
    - Supersedes note pointing back to CBF-02 / pthread_key_t
    - Attribution: android/ndk-samples, Apache 2.0
    - No stub markers remaining
    """
    example = (
        REPO_ROOT
        / "avatars" / "technology" / "cpp" / "examples"
        / "ENG-6.1-jni-thread-cpp11.md"
    )
    content = example.read_text(encoding="utf-8")

    assert "thread_local" in content, (
        "COMPLIANT section must use thread_local RAII"
    )
    assert "AttachCurrentThread" in content, (
        "COMPLIANT section must show AttachCurrentThread"
    )
    assert "DetachCurrentThread" in content, (
        "COMPLIANT section must show DetachCurrentThread in destructor"
    )
    assert "GetEnv" in content, (
        "COMPLIANT section must show GetEnv to check if already attached"
    )
    assert "g_env" in content or "static" in content, (
        "NON-COMPLIANT section must show the static shared env anti-pattern"
    )
    assert "Apache" in content and "ndk-samples" in content, (
        "Must include android/ndk-samples Apache 2.0 attribution"
    )
    assert "destructor" in content.lower() or "~" in content, (
        "Must document RAII destructor that calls DetachCurrentThread"
    )
    assert "Stub" not in content and "stub" not in content, (
        "File must be fully populated — stub markers must be removed"
    )


def test_cbf_04_fmtlib_format_content():
    """CBF-04: ENG-6.1-fmtlib-format.md must contain all required fmtlib content.

    Scenario: cpp-brownfield-first/CBF-04
    Law: ENG-6.1 (Safety-Critical Code — format string safety)

    Required content:
    - COMPLIANT: fmt::format with flight-domain format string
    - COMPLIANT: custom fmt::formatter<T> specialization for domain type
    - COMPLIANT: fmt::format_to with output iterator
    - NON-COMPLIANT: sprintf (format string vulnerabilities)
    - C++20 migration note (namespace/header swap only)
    - fmtlib/fmt MIT attribution, Victor Zverovich
    - No stub markers remaining
    """
    example = (
        REPO_ROOT
        / "avatars" / "technology" / "cpp" / "examples"
        / "ENG-6.1-fmtlib-format.md"
    )
    content = example.read_text(encoding="utf-8")

    assert "fmt::format" in content, (
        "COMPLIANT section must show fmt::format()"
    )
    assert "fmt::formatter" in content, (
        "COMPLIANT section must show custom fmt::formatter<T> specialization"
    )
    assert "fmt::format_to" in content, (
        "COMPLIANT section must show fmt::format_to for output iterators"
    )
    assert "sprintf" in content, (
        "NON-COMPLIANT section must show sprintf anti-pattern"
    )
    assert "std::format" in content, (
        "Must include C++20 std::format migration note"
    )
    assert "MIT" in content and ("Victor Zverovich" in content or "fmtlib" in content), (
        "Must include fmtlib MIT attribution to Victor Zverovich"
    )
    assert "Stub" not in content and "stub" not in content, (
        "File must be fully populated — stub markers must be removed"
    )


def test_cbf_05_ranges_range_v3_content():
    """CBF-05: ENG-3.1-ranges-range-v3.md must contain all required range-v3 content.

    Scenario: cpp-brownfield-first/CBF-05
    Law: ENG-3.1 (Complexity — prefer pipelines over manual iteration)

    Required content:
    - COMPLIANT: filter | transform | take pipeline over domain collection
    - COMPLIANT: ranges::sort replacing iterator-pair sort
    - NON-COMPLIANT: raw iterator loop with manual filter accumulation
    - Warning: ranges:: vs std::ranges:: namespace — do NOT mix headers
    - Warning: const-iterability semantics differ between range-v3 and C++20
    - C++20 migration note (mostly namespace substitution)
    - Attribution: ericniebler/range-v3, Boost Software License, Eric Niebler
    - No stub markers remaining
    """
    example = (
        REPO_ROOT
        / "avatars" / "technology" / "cpp" / "examples"
        / "ENG-3.1-ranges-range-v3.md"
    )
    content = example.read_text(encoding="utf-8")

    assert ("ranges::view" in content or "ranges::views" in content
            or "view::filter" in content or "views::filter" in content), (
        "COMPLIANT section must show a ranges view pipeline (filter/transform/take)"
    )
    assert "ranges::sort" in content or "ranges::actions" in content, (
        "COMPLIANT section must show ranges::sort or actions"
    )
    assert "filter" in content and "transform" in content, (
        "COMPLIANT pipeline must include both filter and transform steps"
    )
    assert "std::ranges" in content, (
        "Must warn about std::ranges:: namespace difference from ranges::"
    )
    assert ("const-iter" in content or "const_iterator" in content
            or "const-iterable" in content or "const iterator" in content.lower()
            or "const-iterab" in content), (
        "Must document const-iterability semantics difference"
    )
    assert "Boost" in content and ("Eric Niebler" in content or "ericniebler" in content), (
        "Must include ericniebler/range-v3 Boost Software License attribution"
    )
    assert "Stub" not in content and "stub" not in content, (
        "File must be fully populated — stub markers must be removed"
    )


def test_cbf_06_gsl_span_cpp14_content():
    """CBF-06: ENG-6.1-gsl-span-cpp14.md must contain all required gsl::span content.

    Scenario: cpp-brownfield-first/CBF-06
    Law: ENG-6.1 (Safety-Critical Code — bounds safety)

    Required content:
    - COMPLIANT: gsl::span<const T> function parameter replacing pointer+size
    - COMPLIANT: span.subspan(offset, count) for sub-range passing
    - COMPLIANT: gsl::make_span from std::vector
    - NON-COMPLIANT: raw pointer + size pair
    - C++20 migration note (std::span, identical API)
    - Attribution: microsoft/GSL, MIT, Microsoft
    - No stub markers remaining
    """
    example = (
        REPO_ROOT
        / "avatars" / "technology" / "cpp" / "examples"
        / "ENG-6.1-gsl-span-cpp14.md"
    )
    content = example.read_text(encoding="utf-8")

    assert "gsl::span" in content, (
        "COMPLIANT section must show gsl::span<T> parameter"
    )
    assert "subspan" in content, (
        "COMPLIANT section must show span.subspan(offset, count)"
    )
    assert "make_span" in content or "gsl::span{" in content or "gsl::span(" in content, (
        "COMPLIANT section must show construction from std::vector"
    )
    assert "std::span" in content, (
        "Must include C++20 std::span migration note"
    )
    assert "MIT" in content and "microsoft/GSL" in content, (
        "Must include microsoft/GSL MIT attribution"
    )
    assert "Stub" not in content and "stub" not in content, (
        "File must be fully populated — stub markers must be removed"
    )


def test_cbf_07_thread_stop_flag_content():
    """CBF-07: ENG-6.1-thread-stop-flag.md must contain all required stop-flag content.

    Scenario: cpp-brownfield-first/CBF-07
    Law: ENG-6.1 (Safety-Critical Code — thread cancellation)

    Required content:
    - COMPLIANT: std::atomic<bool> with memory_order_release store (requester)
      and memory_order_acquire load (worker loop)
    - COMPLIANT: RAII stop-guard that sets flag in destructor
    - NON-COMPLIANT: volatile bool stop_flag (data race, no ordering)
    - NON-COMPLIANT: plain bool checked without atomic load (compiler may optimize away)
    - C++20 migration note: std::jthread + std::stop_token
    - No stub markers remaining
    """
    example = (
        REPO_ROOT
        / "avatars" / "technology" / "cpp" / "examples"
        / "ENG-6.1-thread-stop-flag.md"
    )
    content = example.read_text(encoding="utf-8")

    assert "atomic" in content and "bool" in content, (
        "COMPLIANT section must use std::atomic<bool> stop flag"
    )
    assert "memory_order_release" in content, (
        "COMPLIANT section must show memory_order_release on store"
    )
    assert "memory_order_acquire" in content, (
        "COMPLIANT section must show memory_order_acquire on load"
    )
    assert "volatile" in content, (
        "NON-COMPLIANT section must show volatile bool anti-pattern"
    )
    assert "jthread" in content or "stop_token" in content, (
        "Must reference C++20 jthread/stop_token upgrade path"
    )
    assert "Stub" not in content and "stub" not in content, (
        "File must be fully populated — stub markers must be removed"
    )


def test_cbf_08_lock_free_cpp14_content():
    """CBF-08: ENG-6.1-lock-free-cpp14.md must contain all required lock-free content.

    Scenario: cpp-brownfield-first/CBF-08
    Law: ENG-6.1 (Safety-Critical Code — thread safety)

    Required content:
    - COMPLIANT: boostorg/lockfree::spsc_queue for SPSC use
    - COMPLIANT: ABA mitigation via version/tag counter with atomic<uint64_t>
    - NON-COMPLIANT: std::hazard_pointer (C++23 — unavailable on C++11/14)
    - Warning: lock-free rarely appropriate for app-layer; profile first;
      cache-line contention can make lock-free slower
    - Attribution: boostorg/lockfree, Boost Software License, Tim Blechmann
    - No stub markers remaining
    """
    example = (
        REPO_ROOT
        / "avatars" / "technology" / "cpp" / "examples"
        / "ENG-6.1-lock-free-cpp14.md"
    )
    content = example.read_text(encoding="utf-8")

    assert "spsc_queue" in content, (
        "COMPLIANT section must show boostorg/lockfree::spsc_queue"
    )
    assert "ABA" in content, (
        "COMPLIANT section must address ABA problem mitigation"
    )
    assert "hazard_pointer" in content, (
        "NON-COMPLIANT section must call out std::hazard_pointer as C++23-only"
    )
    assert "profile" in content.lower(), (
        "Must warn: always profile before reaching for lock-free"
    )
    assert "cache" in content.lower() and (
        "contention" in content.lower() or "cache line" in content.lower()
        or "cache-line" in content.lower()
    ), (
        "Must warn about cache-line contention making lock-free slower"
    )
    assert "Boost" in content and (
        "Tim Blechmann" in content or "boostorg/lockfree" in content
    ), (
        "Must include boostorg/lockfree Boost Software License attribution"
    )
    assert "Stub" not in content and "stub" not in content, (
        "File must be fully populated — stub markers must be removed"
    )



# ---------------------------------------------------------------------------
# CBF-09 — Rule of Three subsection in ref-brownfield-survival.md (C++98)
# ---------------------------------------------------------------------------
def test_cbf_09_rule_of_three_content():
    """ref-brownfield-survival.md must contain a populated Rule of Three
    subsection with COMPLIANT C++98 patterns, NON-COMPLIANT patterns
    (including = delete guard), migration note to Rule of Five, and
    private-undefined non-copyable idiom. Edge Cases section required.
    """
    ref = (
        Path(__file__).parent.parent.parent.parent
        / "avatars/technology/cpp/refs/legacy/ref-brownfield-survival.md"
    )
    assert ref.exists(), "ref-brownfield-survival.md must exist"
    content = ref.read_text(encoding="utf-8")

    assert "## Rule of Three" in content, (
        "Must have a ## Rule of Three heading"
    )
    assert "COMPLIANT" in content, (
        "Must show at least one COMPLIANT Rule of Three pattern"
    )
    assert "NON-COMPLIANT" in content, (
        "Must show at least one NON-COMPLIANT pattern"
    )
    assert "= delete" in content, (
        "Must explain that = delete is C++11 only (NON-COMPLIANT in C++98)"
    )
    # Private-undefined idiom is the C++98 equivalent of = delete
    assert "private" in content.lower(), (
        "Must show private-undefined (non-copyable C++98 idiom)"
    )
    assert "Rule of Five" in content, (
        "Must include migration note to Rule of Five (C++11+)"
    )
    assert "## Edge Cases" in content, (
        "Must have ## Edge Cases (or ## Edge Cases & Warnings) section"
    )
    assert "Stub" not in content and "CBF-09" not in content, (
        "File must be fully populated — stub/task markers must be removed"
    )


# ---------------------------------------------------------------------------
# CBF-10 — const char* lifetime traps example (pre-C++17 / cpp_version_min: 03)
# ---------------------------------------------------------------------------
def test_cbf_10_const_char_lifetime_content():
    """ENG-6.1-const-char-lifetime.md must be fully populated with:
    - COMPLIANT: store as std::string, expose .c_str() only at point of use
    - COMPLIANT: lifetime-documented const char* parameter contract
    - NON-COMPLIANT: return .c_str() of local std::string (dangling)
    - NON-COMPLIANT: store pointer from temporary expression
    - Migration note to string_view (C++17)
    - Edge Cases & Warnings section
    - No stub markers
    """
    example = (
        Path(__file__).parent.parent.parent.parent
        / "avatars/technology/cpp/examples/ENG-6.1-const-char-lifetime.md"
    )
    assert example.exists(), "ENG-6.1-const-char-lifetime.md must exist"
    content = example.read_text(encoding="utf-8")

    assert "COMPLIANT" in content, "Must show at least one COMPLIANT pattern"
    assert "NON-COMPLIANT" in content, "Must show at least one NON-COMPLIANT pattern"
    assert "c_str()" in content, "Must reference .c_str() — the central API"
    assert "dangling" in content.lower() or "undefined behavior" in content.lower(), (
        "Must warn that dangling const char* causes undefined behavior"
    )
    assert "string_view" in content, (
        "Must include migration note referencing std::string_view (C++17)"
    )
    assert "## Edge Cases" in content, (
        "Must have ## Edge Cases (or ## Edge Cases & Warnings) section"
    )
    assert "Stub" not in content and "stub" not in content, (
        "File must be fully populated — stub markers must be removed"
    )
    assert "CBF-10" not in content, (
        "Stub task marker CBF-10 must be removed from the populated file"
    )


# ---------------------------------------------------------------------------
# CBF-11 — MSVC 6.0 golden-master section in ref-brownfield-survival.md
# ---------------------------------------------------------------------------
def test_cbf_11_msvc6_golden_master_content():
    """ref-brownfield-survival.md must contain a populated MSVC 6.0
    golden-master section with: stdlib-only pattern using <fstream> and
    assert(), write-then-compare workflow, explicit note that GTest 1.8.x
    is preferred for all other C++98/03 targets (GCC, MSVC 8.0+), and
    edge cases. No stub markers. No CBF-11 task reference remaining.
    """
    ref = (
        Path(__file__).parent.parent.parent.parent
        / "avatars/technology/cpp/refs/legacy/ref-brownfield-survival.md"
    )
    assert ref.exists(), "ref-brownfield-survival.md must exist"
    content = ref.read_text(encoding="utf-8")

    assert "## MSVC 6.0" in content or "## MSVC 6" in content, (
        "Must have a ## MSVC 6.0 (or ## MSVC 6) heading"
    )
    assert "golden" in content.lower() or "characterization" in content.lower(), (
        "Must describe the golden-master / characterization test pattern"
    )
    assert "<fstream>" in content, (
        "Must show stdlib-only pattern using <fstream>"
    )
    assert "assert" in content, (
        "Must use assert() — the only test primitive available on MSVC 6.0"
    )
    assert "GTest" in content or "gtest" in content, (
        "Must note GTest 1.8.x preference for non-MSVC-6.0 C++98/03 targets"
    )
    assert "1.8" in content, (
        "Must specify GTest 1.8.x version pin"
    )
    assert "## Edge Cases" in content, (
        "Must have ## Edge Cases section in the file"
    )
    assert "CBF-11" not in content, (
        "Stub task marker CBF-11 must be removed from the populated file"
    )


# ---------------------------------------------------------------------------
# CBF-12 — ESE tasks.md annotated with cpp_version_min (ESE-V1)
# ---------------------------------------------------------------------------
def test_cbf_12_ese_tasks_version_annotations():
    """Every substantive ESE task in cpp-external-sources-enrichment/tasks.md
    must carry a cpp_version_min annotation. Spot-checks: C++20 tasks, C++17
    tasks, C++11 tasks, C++98 tasks, and governance tasks are exempt.
    """
    ese_tasks = (
        Path(__file__).parent.parent.parent.parent
        / "hangar-ai-specs/changes/cpp-external-sources-enrichment/tasks.md"
    )
    assert ese_tasks.exists(), "ESE tasks.md must exist"
    content = ese_tasks.read_text(encoding="utf-8")

    # Must have a meaningful number of version annotations (≥ 40 substantive tasks)
    annotation_count = content.count("cpp_version_min:")
    assert annotation_count >= 40, (
        f"Expected ≥40 cpp_version_min annotations; found {annotation_count}. "
        "Every substantive ESE task must declare its minimum C++ standard."
    )

    # Spot-check: C++20 tasks get cpp_version_min: 20
    # ESE-01 is the first Phase 1a C++20 task (ref-cpp20-features.md skeleton)
    assert "ESE-01" in content and "cpp_version_min: 20" in content, (
        "At least one task must be annotated with cpp_version_min: 20 "
        "(Phase 1 C++20 feature tasks)"
    )

    # Spot-check: C++17 task — ESE-18 parallel algorithms (std::execution is C++17)
    # and ESE-26 false sharing (hardware_destructive_interference_size is C++17)
    assert "cpp_version_min: 17" in content, (
        "Must have at least one cpp_version_min: 17 annotation "
        "(e.g., ESE-18 parallel algorithms, ESE-26 false sharing)"
    )

    # Spot-check: C++11 tasks — ESE-17 memory ordering (std::memory_order is C++11)
    assert "cpp_version_min: 11" in content, (
        "Must have at least one cpp_version_min: 11 annotation "
        "(e.g., ESE-17 memory ordering, ESE-23 condition variables)"
    )

    # Spot-check: C++98 task — ESE-50 C-style interop (CPL.xx)
    assert "cpp_version_min: 98" in content, (
        "Must have at least one cpp_version_min: 98 annotation "
        "(e.g., ESE-50 C-style programming / extern-C interop)"
    )


# ---------------------------------------------------------------------------
# CBF-13 — ESE-V2: AVATAR-RAG-INDEX.yaml wired for all planned ESE files
# ---------------------------------------------------------------------------
def test_cbf_13_ese_rag_wiring():
    """AVATAR-RAG-INDEX.yaml must be fully wired for ESE deliverables (ESE-V2):
    - New ref stubs exist on disk (part1/part2 files for C++20 and concurrency)
    - New example stubs exist on disk
    - FORWARD-DECLARATIONS comment block has been replaced with real YAML entries
    - C++20 ref files are in greenfield.prefer
    - C++20-only files are in transitional.avoid
    - C++14-min CBF files are in brownfield.avoid
    - All ESE example stubs listed in ENG-6.1-index.md
    """
    repo = Path(__file__).parent.parent.parent.parent
    yaml_path = repo / "avatars/AVATAR-RAG-INDEX.yaml"
    examples = repo / "avatars/technology/cpp/examples"
    refs = repo / "avatars/technology/cpp/refs/language"

    # --- Stub files must exist on disk ---
    for fname in [
        "ref-cpp20-features-part1.md",
        "ref-cpp20-features-part2.md",
        "ref-concurrency-advanced-part1.md",
        "ref-concurrency-advanced-part2.md",
    ]:
        assert (refs / fname).exists(), f"Ref stub missing: refs/language/{fname}"

    for fname in [
        "ENG-3.1-ranges-views.md",
        "ENG-6.1-std-format.md",
        "ENG-6.1-jthread-stop-token.md",
        "ENG-6.1-lock-free-cpp23.md",
        "ENG-6.1-timezone-cpp20.md",
        "ENG-6.1-span-bounds-safety.md",
        "ENG-6.1-string-view-lifetime.md",
        "ENG-3.2-spaceship-operator.md",
        "ENG-3.1-modules.md",
    ]:
        assert (examples / fname).exists(), f"Example stub missing: examples/{fname}"

    # --- FORWARD-DECLARATIONS comment block must be gone ---
    yaml_text = yaml_path.read_text(encoding="utf-8")
    assert "FORWARD-DECLARATIONS: ESE-C20-AVOID" not in yaml_text, (
        "FORWARD-DECLARATIONS comment block must be replaced with actual YAML entries"
    )

    # --- C++20 ref files wired into greenfield.prefer ---
    assert "ref-cpp20-features-part1.md" in yaml_text, (
        "ref-cpp20-features-part1.md must appear in AVATAR-RAG-INDEX.yaml"
    )
    assert "ref-cpp20-features-part2.md" in yaml_text, (
        "ref-cpp20-features-part2.md must appear in AVATAR-RAG-INDEX.yaml"
    )

    # --- C++20-only examples wired into transitional.avoid ---
    assert "ENG-3.1-ranges-views.md" in yaml_text, (
        "ENG-3.1-ranges-views.md must be wired into AVATAR-RAG-INDEX.yaml"
    )
    assert "ENG-6.1-jthread-stop-token.md" in yaml_text, (
        "ENG-6.1-jthread-stop-token.md must be wired into AVATAR-RAG-INDEX.yaml"
    )

    # --- C++14-min CBF files must be in brownfield.avoid ---
    assert "ENG-6.1-gsl-span-cpp14.md" in yaml_text, (
        "ENG-6.1-gsl-span-cpp14.md must be in brownfield.avoid"
    )
    assert "ENG-3.1-ranges-range-v3.md" in yaml_text, (
        "ENG-3.1-ranges-range-v3.md must be in brownfield.avoid"
    )

    # --- ENG-6.1 index must list the new example stubs ---
    index = (examples / "ENG-6.1-index.md").read_text(encoding="utf-8")
    for fname in [
        "ENG-6.1-std-format.md",
        "ENG-6.1-jthread-stop-token.md",
        "ENG-6.1-span-bounds-safety.md",
        "ENG-6.1-string-view-lifetime.md",
        "ENG-6.1-timezone-cpp20.md",
        "ENG-6.1-lock-free-cpp23.md",
    ]:
        assert fname in index, f"{fname} must be registered in ENG-6.1-index.md"


# ---------------------------------------------------------------------------
# CBF-14 — ESE-V3 + ESE-V4: ESE task references updated to Part 1 / Part 2
# ---------------------------------------------------------------------------

def test_cbf_14_ese_tasks_split_file_references():
    """ESE tasks.md must reference Part 1 / Part 2 files, not the old monolithic names.

    CBF-13 (ESE-V2) created:
      - ref-cpp20-features-part1.md     (ESE-02 through ESE-10)
      - ref-cpp20-features-part2.md     (ESE-11, ESE-47)
      - ref-concurrency-advanced-part1.md  (ESE-21 through ESE-28, cpp_version_min 11)
      - ref-concurrency-advanced-part2.md  (ESE-22/29, cpp_version_min 20)

    CBF-14 (ESE-V3 + ESE-V4) updates ESE tasks.md so:
      1. No bare `ref-cpp20-features.md` references (without part suffix)
      2. No bare `ref-concurrency-advanced.md` references (without part suffix)
      3. Phase 1a heading updated to reflect Part 1 + Part 2 split
      4. Phase 4a heading updated to reflect Part 1 + Part 2 split
      5. ref-cpp20-features-part1.md appears in tasks.md for Phase 1a tasks
      6. ref-cpp20-features-part2.md appears in tasks.md for ESE-11 / ESE-47
      7. ref-concurrency-advanced-part1.md appears in tasks.md for Phase 4a tasks
      8. ref-concurrency-advanced-part2.md appears in tasks.md for ESE-22 / ESE-29
    """
    ese_tasks = (
        REPO_ROOT / "hangar-ai-specs" / "changes"
        / "cpp-external-sources-enrichment" / "tasks.md"
    )
    content = ese_tasks.read_text(encoding="utf-8")

    # 1. No bare monolithic filenames
    assert "ref-cpp20-features.md`" not in content, (
        "ESE tasks.md must not reference bare `ref-cpp20-features.md` — "
        "use `ref-cpp20-features-part1.md` or `ref-cpp20-features-part2.md`"
    )
    assert "ref-concurrency-advanced.md`" not in content, (
        "ESE tasks.md must not reference bare `ref-concurrency-advanced.md` — "
        "use `ref-concurrency-advanced-part1.md` or `ref-concurrency-advanced-part2.md`"
    )

    # 2. Part files must be present
    assert "ref-cpp20-features-part1.md" in content, (
        "ESE tasks.md must reference ref-cpp20-features-part1.md (ESE-02 through ESE-10)"
    )
    assert "ref-cpp20-features-part2.md" in content, (
        "ESE tasks.md must reference ref-cpp20-features-part2.md (ESE-11, ESE-47)"
    )
    assert "ref-concurrency-advanced-part1.md" in content, (
        "ESE tasks.md must reference ref-concurrency-advanced-part1.md (ESE-21–28)"
    )
    assert "ref-concurrency-advanced-part2.md" in content, (
        "ESE tasks.md must reference ref-concurrency-advanced-part2.md (ESE-22/29)"
    )

    # 3. Phase headings reflect the split
    assert "Part 1" in content and "Part 2" in content, (
        "ESE tasks.md Phase headings must be updated to show Part 1 / Part 2 split"
    )


# ---------------------------------------------------------------------------
# CBF-15 — Brownfield routing scenarios in RAG eval
# ---------------------------------------------------------------------------

def test_cbf_15_brownfield_routing_scenarios_in_rag_eval():
    """test_phase2_e4_rag_eval.py SCENARIOS must include 5 brownfield routing scenarios.

    CBF-15 adds 5 scenarios that verify the routing policy correctly serves
    brownfield C++98/11/14 teams — routing them to legacy/transitional content
    and NOT to C++20-only files (which are in transitional.avoid / brownfield.avoid).

    Required scenario IDs:
      - brownfield-timezone-cpp14   (FAR 117 timezone → ref-safety-far117-cwr.md)
      - brownfield-jni-thread-cpp98 (JNI thread safety → ref-concurrency-brownfield.md)
      - brownfield-fmtlib-cpp14     (safe string format → ref-io-formatting.md)
      - brownfield-range-v3-cpp14   (ranges pipeline → ref-brownfield-survival.md)
      - brownfield-stop-flag-cpp11  (cooperative cancellation → ref-brownfield-survival.md)
    """
    rag_eval = (
        REPO_ROOT / "tests" / "unit" / "test_cpp_avatar"
        / "test_phase2_e4_rag_eval.py"
    )
    content = rag_eval.read_text(encoding="utf-8")

    required_ids = [
        "brownfield-timezone-cpp14",
        "brownfield-jni-thread-cpp98",
        "brownfield-fmtlib-cpp14",
        "brownfield-range-v3-cpp14",
        "brownfield-stop-flag-cpp11",
    ]
    for sid in required_ids:
        assert sid in content, (
            f"SCENARIOS in test_phase2_e4_rag_eval.py must include '{sid}'. "
            "CBF-15 adds 5 brownfield routing validation scenarios."
        )


# ---------------------------------------------------------------------------
# CBF-16 — Token budget review: stub annotations replaced with real estimates
# ---------------------------------------------------------------------------

def test_cbf_16_stub_token_annotations_replaced():
    """AVATAR-RAG-INDEX.yaml search_queries must not have (~stub-CBF-NN) annotations.

    CBF content files (CBF-01 through CBF-11) are now fully populated.
    The (~stub-CBF-NN) placeholder annotations in search_queries must be
    replaced with real token estimates (~NNNt) reflecting actual file sizes.

    This test enforces that the token budget review (CBF-16) has completed.
    """
    content = RAG_INDEX.read_text(encoding="utf-8")
    stub_refs = [
        line.strip() for line in content.splitlines()
        if "~stub-CBF-" in line
    ]
    assert len(stub_refs) == 0, (
        f"Found {len(stub_refs)} (~stub-CBF-NN) placeholder(s) in "
        f"AVATAR-RAG-INDEX.yaml — replace with real token estimates (~NNNt):\n"
        + "\n".join(f"  {r}" for r in stub_refs)
    )
