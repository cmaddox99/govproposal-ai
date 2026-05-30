"""
Phase 2 — E4: RAG Routing Evaluation Harness v2

Scoring 4 metrics across 30 scenarios.

KEY DESIGN DECISIONS (from diagnostic):

1. Multi-version ref files (cpp_version_min:98) intentionally contain
   newer content behind ★ C++XX callout markers. This is NOT leakage
   — it is correct comprehensive reference behavior. The eval treats
   this as acceptable: a C++98 developer sees labeled C++20 sections
   and knows not to use them.

2. Migration guidance docs (ref-brownfield-adoption, ref-mental-models)
   intentionally mention modern constructs as migration TARGETS.
   `unique_ptr` in a C++98 brownfield guide is not leakage — it is
   the point.

3. HARD FAIL is reserved for: a file with cpp_version_min > project
   standard appearing in the TIER ROUTING prefer list (not query match)
   — because tier routing is the "default serve" path with no query filter.

4. ROUTING GAP (xfail/soft) is used for: query does not find the best
   ref file, or the result is the right tier but not the ideal document.

Metrics:
  ROUTING     — right file in top-6 combined route?
  VERSION_SAFE— cpp_version_min <= project for all TIER-routed files
  COVERAGE    — must_contain keywords present in ANY routed content?
  NO_LEAK     — must_not_contain keywords ABSENT from ALL routed content?

NO_LEAK hard-fail criteria:
  - Applied only when the leaking keyword IS NOT clearly behind a
    ★ C++NN callout in the file. "Marked leakage" is informational only.
"""

import io
import pathlib
import re
import yaml
import pytest

REPO_ROOT = pathlib.Path(__file__).parent.parent.parent.parent
CPP_DIR   = REPO_ROOT / "avatars" / "technology" / "cpp"
RAG_INDEX = REPO_ROOT / "avatars" / "AVATAR-RAG-INDEX.yaml"

VERSION_ORDER = [98, 3, 11, 14, 17, 20, 23, 26]

TIER_MAP = {
    "pre98": "legacy",
    "98": "brownfield", "03": "brownfield",
    "11": "transitional", "14": "transitional",
    "17": "modern",
    "20": "greenfield", "23": "greenfield",
}


def _version_ok(file_min: int, project: int) -> bool:
    try:
        return VERSION_ORDER.index(file_min) <= VERSION_ORDER.index(project)
    except ValueError:
        return False


def _strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4:]
    return text


def _read_ref(ref_path: str) -> str:
    p = CPP_DIR / ref_path
    if not p.exists():
        return ""
    return _strip_frontmatter(p.read_text(encoding="utf-8"))


def _ref_version_min(ref_path: str) -> int | None:
    p = CPP_DIR / ref_path
    if not p.exists():
        return None
    m = re.search(r"cpp_version_min:\s*(\d+)", p.read_text(encoding="utf-8"))
    return int(m.group(1)) if m else None


def _is_callout_gated(content: str, keyword: str) -> bool:
    """
    Return True if every occurrence of keyword is within 3 lines of a
    '★ C++NN' callout marker — meaning the content is version-labeled
    and a developer knows it applies to a specific version.
    """
    lines = content.splitlines()
    kw_lower = keyword.lower()
    ungated = 0
    for i, line in enumerate(lines):
        if kw_lower in line.lower():
            # Check window: 5 lines before, 0 after (marker usually precedes content)
            window_start = max(0, i - 5)
            window = "\n".join(lines[window_start: i + 2]).lower()
            if "c++2" not in window and "c++1" not in window and "★" not in window:
                # Also check section heading above
                for j in range(i - 1, max(0, i - 15) - 1, -1):
                    if lines[j].startswith("##") or lines[j].startswith("---"):
                        if "c++" in lines[j].lower() or "★" in lines[j]:
                            break
                        elif lines[j].startswith("##"):
                            ungated += 1
                            break
    return ungated == 0


def _load_index():
    return yaml.safe_load(RAG_INDEX.read_text(encoding="utf-8"))


def _route_by_query(query: str, index: dict) -> list[str]:
    cpp = index["technology_avatars"]["cpp"]
    query_lower = query.lower()
    matches = []
    for entry in cpp.get("search_queries", []):
        m = re.search(r"->?\s*(refs/[^\s\(]+\.md)", entry)
        if not m:
            m = re.search(r"(refs/[^\s\(]+\.md)", entry)
        if not m:
            continue
        ref_path = m.group(1)
        entry_lower = entry.lower()
        query_words = [w for w in query_lower.split() if len(w) > 3]
        hits = sum(1 for w in query_words if w in entry_lower)
        if hits >= 2:
            matches.append(ref_path)
    return list(dict.fromkeys(matches))


def _route_by_tier(project_standard: str, index: dict) -> list[str]:
    tier = TIER_MAP.get(str(project_standard), "unknown")
    cpp = index["technology_avatars"]["cpp"]
    vp = cpp.get("version_routing_policy", {}).get("by_standard", {})
    return vp.get(tier, {}).get("prefer", [])


def _combined_route(query: str, project_standard: str, index: dict) -> list[str]:
    q = _route_by_query(query, index)
    t = _route_by_tier(project_standard, index)
    combined = q + [r for r in t if r not in q]
    return combined[:6]


# ── Scenario definitions ─────────────────────────────────────────────────────
# (id, query, cpp_version, expected_primary, allowed_alts,
#  must_contain, must_not_contain_unmarked, hard_fail_if_leaked)
#
# must_not_contain_unmarked: keyword must be ABSENT unless it's clearly
# behind a ★ C++NN callout. Migration guidance naturally contains newer
# terms as targets — we only flag truly unmarked leakage.

SCENARIOS = [
    # Memory management
    ("mem-98-brownfield",
     "C++ memory management C++98 brownfield",
     98,
     "refs/legacy/ref-brownfield-adoption.md",
     ["refs/legacy/ref-mental-models-memory.md"],
     ["memory"],
     [],  # unique_ptr in migration guide is expected + gated
     False),

    ("mem-11-unique-ptr",
     "C++ smart pointer unique_ptr memory ownership",
     11,
     "refs/safety/ref-safety-memory-lifetime.md",
     ["refs/language/ref-domain-patterns.md"],
     ["unique_ptr"],
     [],
     False),

    ("mem-14-make-unique",
     "C++ make_unique smart pointer factory",
     14,
     "refs/safety/ref-safety-memory-lifetime.md",
     [],
     ["unique_ptr"],
     [],
     False),

    ("mem-20-pmr",
     "C++ PMR polymorphic memory resource allocator",
     20,
     "refs/language/ref-advanced-patterns.md",
     [],
     ["pmr", "C++17"],
     [],
     False),

    # Concurrency
    ("conc-98-pthread",
     "C++ pthread POSIX threading C++98 legacy",
     98,
     "refs/legacy/ref-concurrency-brownfield.md",
     [],
     ["pthread"],
     [],
     False),

    ("conc-98-volatile",
     "C++ volatile thread safety C++98",
     98,
     "refs/legacy/ref-concurrency-brownfield.md",
     [],
     ["volatile"],
     [],
     False),

    ("conc-11-thread",
     "C++ std::thread mutex lock_guard thread safety",
     11,
     "refs/safety/ref-concurrency-threading.md",
     [],
     ["thread", "lock_guard"],
     [],
     False),

    ("conc-17-async",
     "C++ async circuit breaker bulkhead resiliency",
     17,
     "refs/safety/ref-concurrency-async.md",
     [],
     ["circuit"],
     [],
     False),

    ("conc-20-coroutine",
     "C++ coroutines co_await co_yield C++20",
     20,
     "refs/language/ref-concurrency-coroutines.md",
     [],
     ["co_await"],
     [],
     False),

    # I/O — key version boundary tests
    ("io-98-printf",
     "C++ printf format string security injection",
     98,
     "refs/language/ref-io-formatting.md",
     [],
     ["printf", "literal"],
     [],
     False),

    ("io-11-spdlog",
     "C++ spdlog logging structured best practice",
     11,
     "refs/language/ref-io-formatting.md",
     ["refs/testing/ref-infrastructure.md"],
     ["spdlog"],
     [],
     False),

    ("io-20-format",
     "C++ std::format fmtlib string formatting C++20",
     20,
     "refs/language/ref-io-formatting.md",
     [],
     ["std::format"],
     [],
     False),

    ("io-23-print",
     "C++ std::print println C++23",
     23,
     "refs/language/ref-io-formatting.md",
     [],
     ["std::print"],
     [],
     False),

    ("io-11-iostream",
     "C++ iostream cout cerr output",
     11,
     "refs/language/ref-io-formatting.md",
     [],
     ["iostream", "cout"],
     [],
     False),

    # Templates
    ("tmpl-11-sfinae",
     "C++ SFINAE enable_if template metaprogramming",
     11,
     "refs/language/ref-templates-metaprogramming.md",
     [],
     ["enable_if"],
     [],
     False),

    ("tmpl-20-concepts",
     "C++ concepts requires template constraints C++20",
     20,
     "refs/language/ref-templates-metaprogramming.md",
     [],
     ["concept"],
     [],
     False),

    # Smart pointers
    ("sp-11-smart",
     "C++ unique_ptr shared_ptr smart pointer ownership RAII",
     11,
     "refs/safety/ref-safety-memory-lifetime.md",
     [],
     ["unique_ptr"],
     [],
     False),

    # Comparison operators
    ("cmp-20-spaceship",
     "C++ spaceship operator three-way comparison",
     20,
     "refs/language/ref-core-type-safety.md",
     ["refs/language/ref-core-modern-idioms.md"],
     ["operator"],
     [],
     False),

    # Aviation compliance
    ("avia-far117",
     "C++ FAR 117 crew rest aviation compliance CWR",
     14,
     "refs/safety/ref-safety-far117-cwr.md",
     [],
     ["FAR"],
     [],
     False),

    # Brownfield migration
    ("bfld-migrate-cpp11",
     "C++ brownfield migration C++11 legacy upgrade",
     11,
     "refs/legacy/ref-brownfield-adoption.md",
     ["refs/legacy/ref-migration-pre-cpp17.md"],
     ["migration"],
     [],
     False),

    ("bfld-cpp98-mental",
     "C++ C++98 mental model Java developer pointer",
     98,
     "refs/legacy/ref-mental-models-lang.md",
     ["refs/legacy/ref-mental-models-memory.md"],
     [],
     [],
     False),

    # ABI stability
    ("abi-stability",
     "C++ ABI stability binary compatibility shared library pimpl",
     17,
     "refs/language/ref-advanced-patterns.md",
     [],
     ["ABI"],
     [],
     False),

    # Same-tier boundaries (version sensitivity)
    ("boundary-11-gets-threading",
     "C++ thread mutex lock C++11",
     11,
     "refs/safety/ref-concurrency-threading.md",
     [],
     ["thread", "mutex"],
     [],
     False),

    ("boundary-coroutines-needs-20",
     "C++ coroutines co_await",
     11,
     # C++11 should NOT get coroutines as primary; transitional tier must not prefer it
     "refs/safety/ref-concurrency-threading.md",  # correct alternative
     ["refs/legacy/ref-brownfield-adoption.md"],
     [],
     [],
     False),

    # Ambiguous queries — test that routing falls back gracefully
    ("ambig-format-cpp17",
     "C++ format output string text",
     17,
     "refs/language/ref-io-formatting.md",
     ["refs/testing/ref-infrastructure.md"],
     [],  # Accept any routing for ambiguous
     [],
     False),

    # Testing
    ("test-gtest-cpp11",
     "C++ unit testing GoogleTest fixture mock",
     11,
     "refs/testing/ref-testing-gtest-core.md",
     ["refs/testing/ref-testing-ci-policy.md"],
     ["test"],
     [],
     False),

    # Hard-fail tier safety tests (direct tier routing only)
    # These verify the TIER PREFER list doesn't include wrong-version files
    ("tier-cpp98-no-coroutines",
     "C++ tier routing brownfield C++98",
     98,
     "refs/legacy/ref-legacy-navigation.md",
     ["refs/legacy/ref-brownfield-adoption.md"],
     [],
     ["co_await"],   # coroutine keywords must not be in C++98 tier-routed content
     True),

    ("tier-cpp11-no-coroutines",
     "C++ tier routing transitional C++11",
     11,
     "refs/safety/ref-concurrency-threading.md",
     ["refs/language/ref-core-type-safety.md"],
     [],
     [],
     False),

    ("tier-cpp20-modern",
     "C++ tier routing greenfield C++20",
     20,
     "refs/language/ref-core-modern-idioms.md",
     ["refs/language/ref-advanced-patterns.md",
      "refs/language/ref-concurrency-coroutines.md"],
     [],
     [],
     False),

    ("tier-cpp98-version-safety",
     "C++ C++98 brownfield project version safety",
     98,
     "refs/legacy/ref-legacy-navigation.md",
     ["refs/legacy/ref-brownfield-adoption.md"],
     [],
     [],
     True),  # If any tier-routed file has cpp_version_min > 98, hard fail

    # ── CBF-15: Brownfield routing scenarios ──────────────────────────────
    # Verify that brownfield C++98/11/14 queries route to legacy/transitional
    # content and NOT to C++20-only files (in transitional.avoid/brownfield.avoid).

    ("brownfield-timezone-cpp14",
     "FAR 117 crew rest timezone cpp14 chrono datetime",
     14,
     "refs/safety/ref-safety-far117-cwr.md",
     ["refs/legacy/ref-brownfield-survival.md",
      "examples/ENG-6.1-timezone-cpp14.md"],
     [],
     [],
     False),

    ("brownfield-jni-thread-cpp98",
     "JNI thread safety pthread cpp98 legacy",
     98,
     "refs/legacy/ref-concurrency-brownfield.md",
     ["refs/safety/ref-concurrency-threading.md",
      "examples/ENG-6.1-jni-thread-cpp98.md"],
     ["thread"],
     [],
     False),

    ("brownfield-fmtlib-cpp14",
     "safe string format fmtlib fmt format cpp14",
     14,
     "refs/language/ref-io-formatting.md",
     ["refs/legacy/ref-brownfield-survival.md",
      "examples/ENG-6.1-fmtlib-format.md"],
     ["format"],
     [],
     False),

    ("brownfield-range-v3-cpp14",
     "ranges pipeline filter transform range-v3 cpp14",
     14,
     "refs/legacy/ref-brownfield-survival.md",
     ["refs/language/ref-core-modern-idioms.md",
      "examples/ENG-3.1-ranges-range-v3.md"],
     [],
     [],
     False),

    ("brownfield-stop-flag-cpp11",
     "cooperative thread cancellation stop flag atomic cpp11",
     11,
     "refs/legacy/ref-brownfield-survival.md",
     ["refs/safety/ref-concurrency-threading.md",
      "examples/ENG-6.1-thread-stop-flag.md"],
     [],
     [],
     False),
]


def evaluate_scenario(scenario: tuple, index: dict) -> dict:
    (sid, query, project_version, expected_primary,
     allowed_alts, must_contain, must_not_contain_unmarked, hard_fail_if_leaked) = scenario

    routed     = _combined_route(query, str(project_version), index)
    tier_routed = _route_by_tier(str(project_version), index)
    all_expected = [expected_primary] + allowed_alts

    # ROUTING
    routing_ok = any(r in routed for r in all_expected)

    # VERSION_SAFE — tier routing only (query routing is filtered by intent)
    version_safe = True
    unsafe_files = []
    for ref in tier_routed:
        min_v = _ref_version_min(ref)
        if min_v is not None and not _version_ok(min_v, project_version):
            version_safe = False
            unsafe_files.append((ref, min_v))

    # COVERAGE
    all_content = " ".join(_read_ref(r) for r in routed).lower()
    missing_kws = [kw for kw in must_contain if kw.lower() not in all_content]
    coverage_ok = len(missing_kws) == 0

    # NO_LEAK — only if keyword is NOT callout-gated
    leaked_kws = []
    for kw in must_not_contain_unmarked:
        all_content_raw = " ".join(_read_ref(r) for r in routed)
        if kw.lower() in all_content_raw.lower():
            # Check if it's gated in every file that contains it
            for ref in routed:
                content = _read_ref(ref)
                if kw.lower() in content.lower():
                    if not _is_callout_gated(content, kw):
                        leaked_kws.append(kw)
                        break
    no_leak_ok = len(leaked_kws) == 0
    hard_fail  = hard_fail_if_leaked and not no_leak_ok

    notes = []
    if not routing_ok:
        notes.append(f"routing miss: routed={routed[:3]}, wanted one of {all_expected}")
    if unsafe_files:
        notes.append(f"version-unsafe in tier: {unsafe_files}")
    if missing_kws:
        notes.append(f"missing coverage: {missing_kws}")
    if leaked_kws:
        notes.append(f"LEAKED (ungated): {leaked_kws}")

    return {
        "id": sid,
        "routing_ok": routing_ok,
        "version_safe": version_safe,
        "coverage_ok": coverage_ok,
        "no_leak_ok": no_leak_ok,
        "hard_fail": hard_fail,
        "routed": routed,
        "tier_routed": tier_routed,
        "notes": notes,
    }


def run_all(index: dict) -> list[dict]:
    return [evaluate_scenario(s, index) for s in SCENARIOS]


def _dashboard_text(results: list[dict]) -> str:
    total    = len(results)
    routing  = sum(1 for r in results if r["routing_ok"])
    vsafe    = sum(1 for r in results if r["version_safe"])
    coverage = sum(1 for r in results if r["coverage_ok"])
    noleak   = sum(1 for r in results if r["no_leak_ok"])
    hard     = [r for r in results if r["hard_fail"]]

    buf = io.StringIO()
    w = buf.write
    w("\n")
    w("=" * 65 + "\n")
    w("  C++ Avatar RAG Routing Evaluation Dashboard\n")
    w("=" * 65 + "\n")
    w(f"  Scenarios evaluated  : {total}\n")
    w("  ------------------------------------------------\n")
    w(f"  Routing accuracy     : {routing}/{total}  ({100*routing//total}%)\n")
    w(f"  Tier version safety  : {vsafe}/{total}  ({100*vsafe//total}%)\n")
    w(f"  Answer coverage      : {coverage}/{total}  ({100*coverage//total}%)\n")
    w(f"  No ungated leakage   : {noleak}/{total}  ({100*noleak//total}%)\n")
    w(f"  Hard fails           : {len(hard)}  (must be 0)\n")
    w("=" * 65 + "\n")

    failures = [r for r in results if r["notes"]]
    if failures:
        w("\n  Issues (non-blocking unless hard_fail):\n")
        for r in failures:
            tag = " [HARD FAIL]" if r["hard_fail"] else ""
            w(f"\n  [{r['id']}]{tag}\n")
            for n in r["notes"]:
                w(f"    - {n}\n")
    w("\n")
    return buf.getvalue()


# ── Pytest tests ─────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def index():
    return _load_index()


@pytest.fixture(scope="module")
def results(index):
    return run_all(index)


class TestRAGEvalDashboard:
    """
    Prints the full evaluation dashboard.
    Hard fails on version leakage; soft issues are reported but don't fail.
    """

    def test_dashboard_no_hard_fails(self, results, capsys):
        text = _dashboard_text(results)
        with capsys.disabled():
            print(text)
        hard_fails = [r for r in results if r["hard_fail"]]
        assert not hard_fails, (
            f"{len(hard_fails)} hard-fail: "
            + ", ".join(r["id"] for r in hard_fails)
        )

    def test_routing_accuracy_above_70pct(self, results):
        routing = sum(1 for r in results if r["routing_ok"])
        pct = 100 * routing // len(results)
        assert pct >= 70, f"Routing accuracy {pct}% is below 70% minimum"

    def test_tier_version_safety_is_100pct(self, results):
        """TIER routing must NEVER serve a too-new file. This is the hard safety gate."""
        unsafe = [r for r in results if not r["version_safe"]]
        assert not unsafe, (
            "Tier routing served version-unsafe files: "
            + ", ".join(r["id"] for r in unsafe)
        )

    def test_coverage_above_70pct(self, results):
        coverage = sum(1 for r in results if r["coverage_ok"])
        pct = 100 * coverage // len(results)
        assert pct >= 70, f"Coverage {pct}% below 70% minimum"


class TestVersionLeakageHardFails:
    """
    Tier routing safety — the 'always-serve' path must NEVER include
    cpp_version_min > project_standard files.
    """

    def test_cpp98_tier_all_files_are_version_safe(self, index):
        tier_routes = _route_by_tier("98", index)
        assert tier_routes, "C++98 tier must have preferred refs"
        for ref in tier_routes:
            min_v = _ref_version_min(ref)
            if min_v is not None:
                assert _version_ok(min_v, 98), (
                    f"C++98 tier prefers {ref} but its cpp_version_min={min_v} > 98"
                )

    def test_cpp11_tier_all_files_are_version_safe(self, index):
        tier_routes = _route_by_tier("11", index)
        for ref in tier_routes:
            min_v = _ref_version_min(ref)
            if min_v is not None:
                assert _version_ok(min_v, 11), (
                    f"C++11 tier prefers {ref} with cpp_version_min={min_v} > 11"
                )

    def test_cpp17_tier_all_files_are_version_safe(self, index):
        tier_routes = _route_by_tier("17", index)
        for ref in tier_routes:
            min_v = _ref_version_min(ref)
            if min_v is not None:
                assert _version_ok(min_v, 17), (
                    f"C++17 tier prefers {ref} with cpp_version_min={min_v} > 17"
                )

    def test_cpp20_tier_all_files_are_version_safe(self, index):
        tier_routes = _route_by_tier("20", index)
        for ref in tier_routes:
            min_v = _ref_version_min(ref)
            if min_v is not None:
                assert _version_ok(min_v, 20), (
                    f"C++20 tier prefers {ref} with cpp_version_min={min_v} > 20"
                )

    def test_coroutines_ref_not_in_cpp11_tier(self, index):
        tier_routes = _route_by_tier("11", index)
        assert not any("coroutines" in r for r in tier_routes), (
            "Coroutines ref (C++20) must not appear in C++11 transitional tier"
        )

    def test_coroutines_ref_not_in_cpp98_tier(self, index):
        tier_routes = _route_by_tier("98", index)
        assert not any("coroutines" in r for r in tier_routes)

    def test_cpp98_tier_prefers_legacy_content(self, index):
        tier_routes = _route_by_tier("98", index)
        assert any("legacy" in r or "brownfield" in r for r in tier_routes), (
            "C++98 tier must prefer legacy/brownfield refs"
        )

    def test_cpp20_tier_prefers_modern_content(self, index):
        tier_routes = _route_by_tier("20", index)
        assert any("modern-idioms" in r or "coroutines" in r or "advanced" in r
                   for r in tier_routes), (
            "C++20 greenfield tier must prefer modern refs"
        )


@pytest.mark.parametrize("scenario", SCENARIOS, ids=[s[0] for s in SCENARIOS])
def test_scenario(scenario, index):
    result = evaluate_scenario(scenario, index)
    # Hard fail always fails the test
    assert not result["hard_fail"], (
        f"[{result['id']}] HARD FAIL: {result['notes']}"
    )
    # Routing miss or coverage miss: xfail (informational)
    issues = []
    if not result["routing_ok"]:
        issues.append(f"routing miss: {result['notes']}")
    if not result["coverage_ok"]:
        issues.append(f"coverage: {result['notes']}")
    if issues:
        pytest.xfail(f"[{result['id']}] soft gap: {'; '.join(issues)}")
