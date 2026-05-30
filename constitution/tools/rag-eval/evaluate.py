#!/usr/bin/env python3
"""
Constitution RAG Evaluator

Usage:
  python tools/rag-eval/evaluate.py                                         # console output
  python tools/rag-eval/evaluate.py --format json                           # JSON output
  python tools/rag-eval/evaluate.py --format github-actions                 # GitHub Actions annotations
  python tools/rag-eval/evaluate.py --threshold-check                       # Exit 1 if thresholds breached
  python tools/rag-eval/evaluate.py --constitution /path/to/constitution    # Explicit constitution path
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Bootstrap: ensure this script can import sibling modules
# ---------------------------------------------------------------------------
_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml")

from retriever import ConstitutionRetriever
from scorer import Scorer, EvalReport, DimensionScore


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _find_constitution_root(start: Path) -> Path:
    """Walk up from start looking for laws/index.yaml — that's the constitution root."""
    candidate = start
    for _ in range(10):
        if (candidate / "laws" / "index.yaml").exists():
            return candidate
        if candidate.parent == candidate:
            break
        candidate = candidate.parent
    raise SystemExit(
        f"Cannot locate constitution root from {start}. "
        "Pass --constitution /path/to/constitution explicitly."
    )


def _load_config(config_path: Path) -> dict:
    with config_path.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _load_test_cases(test_cases_dir: Path) -> list[dict]:
    cases: list[dict] = []
    for yaml_file in sorted(test_cases_dir.glob("*.yaml")):
        with yaml_file.open(encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        for tc in data.get("test_cases", []):
            cases.append(tc)
    return cases


# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------

_PASS = "PASS"
_FAIL = "FAIL"

_DIM_DISPLAY = {
    "law_retrieval": "Law Retrieval       (35%)",
    "skill_routing": "Skill Routing       (25%)",
    "avatar_selection": "Avatar Selection    (20%)",
    "index_integrity": "Index Integrity     (10%)",
    "cross_ref_consistency": "Cross-Ref Consist.  (10%)",
}


def _pct(f: float) -> str:
    return f"{f * 100:.1f}%"


def _console_output(report: EvalReport) -> None:
    """Print a human-readable table to stdout."""
    # ANSI colour helpers
    def green(s: str) -> str:
        return f"\033[32m{s}\033[0m" if sys.stdout.isatty() else s

    def red(s: str) -> str:
        return f"\033[31m{s}\033[0m" if sys.stdout.isatty() else s

    def bold(s: str) -> str:
        return f"\033[1m{s}\033[0m" if sys.stdout.isatty() else s

    print()
    print(bold("╔══════════════════════════════════════════════════════════════╗"))
    print(bold("║           Hangar AI Constitution — RAG Evaluation            ║"))
    print(bold("╚══════════════════════════════════════════════════════════════╝"))
    print(f"  Constitution : {report.constitution_path}")
    print(f"  Timestamp    : {report.timestamp}")
    print()
    print(f"  {'Dimension':<35} {'Score':>7}  {'Threshold':>9}  {'Matched':>10}  {'Status':>6}")
    print("  " + "─" * 75)

    for d in report.dimensions:
        label = _DIM_DISPLAY.get(d.name, d.name)
        status = green(_PASS) if d.passed else red(_FAIL)
        matched_str = f"{d.matched}/{d.total}" if d.total else "n/a"
        print(
            f"  {label:<35} {_pct(d.score):>7}  {_pct(d.threshold):>9}  {matched_str:>10}  {status:>6}"
        )

    print("  " + "─" * 75)
    overall_status = green(_PASS) if report.overall_passed else red(_FAIL)
    print(
        f"  {'OVERALL WEIGHTED SCORE':<35} {_pct(report.overall_score):>7}  {'85.0%':>9}  {'':>10}  {overall_status:>6}"
    )
    print()

    # Print failures for failed dimensions
    failed_dims = [d for d in report.dimensions if not d.passed and d.failures]
    if failed_dims:
        print(bold("  Failures:"))
        for d in failed_dims:
            label = _DIM_DISPLAY.get(d.name, d.name)
            print(f"\n  [{label.strip()}]")
            for f in d.failures[:10]:
                print(f"    ✗ {f}")
            if len(d.failures) > 10:
                print(f"    … and {len(d.failures) - 10} more")
        print()


def _json_output(report: EvalReport) -> None:
    """Print full report as JSON to stdout."""
    print(json.dumps(asdict(report), indent=2))


def _github_actions_output(report: EvalReport) -> None:
    """Emit GitHub Actions annotations and a job summary."""
    level_fn = {True: "notice", False: "error"}

    for d in report.dimensions:
        level = level_fn[d.passed]
        title = f"RAG {d.name}: {_pct(d.score)} (threshold {_pct(d.threshold)})"
        msg = title
        if not d.passed and d.failures:
            msg += " | " + "; ".join(d.failures[:5])
        print(f"::{level} title={title}::{msg}")

    overall_level = level_fn[report.overall_passed]
    print(
        f"::{overall_level} title=RAG Overall Score: {_pct(report.overall_score)}::"
        f"Overall: {_pct(report.overall_score)} — {'PASSED' if report.overall_passed else 'FAILED'}"
    )

    # GitHub Actions job summary (appended to $GITHUB_STEP_SUMMARY if available)
    summary_lines = [
        "## 📊 RAG Evaluation Results",
        "",
        f"**Overall Score:** `{_pct(report.overall_score)}` — "
        f"{'✅ PASSED' if report.overall_passed else '❌ FAILED'}",
        "",
        "| Dimension | Score | Threshold | Matched | Status |",
        "|-----------|-------|-----------|---------|--------|",
    ]
    for d in report.dimensions:
        matched_str = f"{d.matched}/{d.total}" if d.total else "n/a"
        status = "✅" if d.passed else "❌"
        summary_lines.append(
            f"| {d.name} | {_pct(d.score)} | {_pct(d.threshold)} | {matched_str} | {status} |"
        )

    import os
    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_file:
        with open(summary_file, "a", encoding="utf-8") as f:
            f.write("\n".join(summary_lines) + "\n")


# ---------------------------------------------------------------------------
# Report persistence
# ---------------------------------------------------------------------------

def _write_report(report: EvalReport, reports_dir: Path) -> None:
    reports_dir.mkdir(parents=True, exist_ok=True)
    out_path = reports_dir / "latest.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(asdict(report), f, indent=2)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Evaluate Hangar AI Constitution RAG quality.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--constitution",
        metavar="PATH",
        help="Path to constitution root (auto-detected if omitted)",
    )
    parser.add_argument(
        "--format",
        choices=["console", "json", "github-actions"],
        default="console",
        help="Output format (default: console)",
    )
    parser.add_argument(
        "--threshold-check",
        action="store_true",
        help="Exit with code 1 if any dimension or overall is below threshold",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=None,
        help="Override top-k from config",
    )
    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    # Resolve constitution root
    if args.constitution:
        constitution_path = Path(args.constitution).resolve()
        if not constitution_path.exists():
            parser.error(f"Constitution path does not exist: {constitution_path}")
    else:
        constitution_path = _find_constitution_root(_SCRIPT_DIR)

    # Load config
    config_path = _SCRIPT_DIR / "config.yaml"
    config = _load_config(config_path) if config_path.exists() else {}
    thresholds_cfg = config.get("thresholds", {})

    # Map config keys
    thresholds = {
        "law_retrieval": thresholds_cfg.get("law_retrieval", 0.85),
        "skill_routing": thresholds_cfg.get("skill_routing", 0.80),
        "avatar_selection": thresholds_cfg.get("avatar_selection", 0.80),
        "index_integrity": thresholds_cfg.get("index_integrity", 0.95),
        "cross_ref_consistency": thresholds_cfg.get("cross_reference_consistency", 0.95),
        "overall": thresholds_cfg.get("overall", 0.85),
    }

    eval_cfg = config.get("evaluation", {})
    top_k = args.top_k or eval_cfg.get("top_k", 3)

    output_cfg = config.get("output", {})
    reports_dir_rel = output_cfg.get("reports_dir", "tools/rag-eval/reports")
    reports_dir = constitution_path / reports_dir_rel

    # Load test cases
    test_cases_dir = _SCRIPT_DIR / "test-cases"
    if not test_cases_dir.exists():
        sys.exit(f"Test cases directory not found: {test_cases_dir}")
    test_cases = _load_test_cases(test_cases_dir)

    if not test_cases:
        sys.exit("No test cases loaded — check tools/rag-eval/test-cases/*.yaml")

    # Build retriever
    retriever = ConstitutionRetriever(constitution_path)

    # Score
    scorer = Scorer(
        test_cases=test_cases,
        retriever=retriever,
        constitution_path=constitution_path,
        thresholds=thresholds,
        top_k=top_k,
    )
    report = scorer.compute()

    # Output
    if args.format == "json":
        _json_output(report)
    elif args.format == "github-actions":
        _github_actions_output(report)
    else:
        _console_output(report)

    # Persist report
    _write_report(report, reports_dir)

    # Exit code
    if args.threshold_check:
        breached = not report.overall_passed or any(not d.passed for d in report.dimensions)
        return 1 if breached else 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
