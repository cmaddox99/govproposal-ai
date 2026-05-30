"""
5-dimension scoring model for RAG evaluation.

Dimensions:
  1. law_retrieval        (weight 0.35): % of test cases where expected_laws appear in top-k results
  2. skill_routing        (weight 0.25): % of test cases where expected_skills appear in top-k results
  3. avatar_selection     (weight 0.20): % of test cases where expected_avatars appear in top-k results
  4. index_integrity      (weight 0.10): % of index entries that resolve to real files (structural)
  5. cross_ref_consistency(weight 0.10): % of law citations in skill/avatar files that are valid
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    raise SystemExit("PyYAML is required: pip install pyyaml")

from retriever import ConstitutionRetriever, _load_yaml_safe, _extract_law_ids
from law_ids import build_law_id_regex

DIMENSION_WEIGHTS = {
    "law_retrieval": 0.35,
    "skill_routing": 0.25,
    "avatar_selection": 0.20,
    "index_integrity": 0.10,
    "cross_ref_consistency": 0.10,
}


@dataclass
class DimensionScore:
    name: str
    score: float
    threshold: float
    passed: bool
    total: int
    matched: int
    failures: list[str] = field(default_factory=list)


@dataclass
class EvalReport:
    overall_score: float
    overall_passed: bool
    dimensions: list[DimensionScore]
    timestamp: str
    constitution_path: str


def _collect_registered_law_ids(constitution_path: Path, law_id_re: "re.Pattern[str]") -> set[str]:
    """Collect all law IDs from laws/**/*.md frontmatter."""
    laws_dir = constitution_path / "laws"
    registered: set[str] = set()
    if not laws_dir.exists():
        return registered
    for md_file in laws_dir.rglob("*.md"):
        text = md_file.read_text(encoding="utf-8", errors="replace")
        # parse frontmatter
        if text.startswith("---"):
            end = text.find("\n---", 3)
            if end != -1:
                fm_text = text[3:end].strip()
                try:
                    fm = yaml.safe_load(fm_text) or {}
                    for law in fm.get("laws", []):
                        if isinstance(law, dict) and law.get("id"):
                            registered.add(str(law["id"]))
                except Exception:
                    pass
        # also capture any law IDs found in body via regex as fallback
        registered.update(law_id_re.findall(text))
    return registered


class Scorer:
    def __init__(
        self,
        test_cases: list[dict[str, Any]],
        retriever: ConstitutionRetriever,
        constitution_path: Path,
        thresholds: dict[str, float],
        top_k: int = 3,
    ):
        self.test_cases = test_cases
        self.retriever = retriever
        self.constitution_path = constitution_path
        self.thresholds = thresholds
        self.top_k = top_k
        self._law_id_re = build_law_id_regex(constitution_path)

    def compute(self) -> EvalReport:
        dimensions = [
            self._score_law_retrieval(),
            self._score_skill_routing(),
            self._score_avatar_selection(),
            self._score_index_integrity(),
            self._score_cross_ref_consistency(),
        ]

        overall = sum(
            DIMENSION_WEIGHTS[d.name] * d.score for d in dimensions
        )
        overall_threshold = self.thresholds.get("overall", 0.85)
        overall_passed = overall >= overall_threshold

        return EvalReport(
            overall_score=round(overall, 4),
            overall_passed=overall_passed,
            dimensions=dimensions,
            timestamp=datetime.now(timezone.utc).isoformat(),
            constitution_path=str(self.constitution_path),
        )

    # ------------------------------------------------------------------
    # Dimension 1: law_retrieval
    # ------------------------------------------------------------------

    def _score_law_retrieval(self) -> DimensionScore:
        name = "law_retrieval"
        threshold = self.thresholds.get(name, 0.85)

        relevant = [tc for tc in self.test_cases if tc.get("expected_laws")]
        if not relevant:
            return DimensionScore(name=name, score=1.0, threshold=threshold, passed=True,
                                  total=0, matched=0)

        matched = 0
        failures: list[str] = []

        for tc in relevant:
            q = tc["question"]
            expected = set(str(l) for l in tc["expected_laws"])
            results = self.retriever.retrieve(q, top_k=self.top_k)
            # Collect all law IDs covered by retrieved documents
            retrieved_laws: set[str] = set()
            for r in results:
                retrieved_laws.update(r.matched_law_ids)
                retrieved_laws.update(r.indexed_law_ids)
                retrieved_laws.update(self._law_id_re.findall(r.file_path))
            if expected & retrieved_laws:
                matched += 1
            else:
                failures.append(
                    f"[{tc.get('id', '?')}] Q: {q!r} — expected {expected}, "
                    f"got laws {retrieved_laws or '{none}'}"
                )

        total = len(relevant)
        score = matched / total if total else 1.0
        return DimensionScore(
            name=name,
            score=round(score, 4),
            threshold=threshold,
            passed=score >= threshold,
            total=total,
            matched=matched,
            failures=failures,
        )

    # ------------------------------------------------------------------
    # Dimension 2: skill_routing
    # ------------------------------------------------------------------

    def _score_skill_routing(self) -> DimensionScore:
        name = "skill_routing"
        threshold = self.thresholds.get(name, 0.80)

        relevant = [tc for tc in self.test_cases if tc.get("expected_skills")]
        if not relevant:
            return DimensionScore(name=name, score=1.0, threshold=threshold, passed=True,
                                  total=0, matched=0)

        matched = 0
        failures: list[str] = []

        for tc in relevant:
            q = tc["question"]
            expected = set(str(s) for s in tc["expected_skills"])
            results = self.retriever.retrieve_skill_by_trigger(q, top_k=self.top_k)
            retrieved_ids = set(r.id for r in results)
            # also match by filename stem (e.g. "06-atomic-tdd" matches "06-atomic-tdd.md")
            retrieved_stems = set(r.id.replace(".md", "") for r in results)
            expected_stems = set(s.replace(".md", "") for s in expected)
            # also strip "skill-" prefix so activates.skills refs match filenames
            # e.g. "skill-06-atomic-tdd" matches "06-atomic-tdd.md" / "06-atomic-tdd"
            retrieved_bare = set(s.removeprefix("skill-") for s in retrieved_stems)
            expected_bare = set(s.removeprefix("skill-") for s in expected_stems)
            if expected_stems & (retrieved_ids | retrieved_stems) or expected_bare & (retrieved_bare | retrieved_stems):
                matched += 1
            else:
                failures.append(
                    f"[{tc.get('id', '?')}] Q: {q!r} — expected {expected}, got {retrieved_ids}"
                )

        total = len(relevant)
        score = matched / total if total else 1.0
        return DimensionScore(
            name=name,
            score=round(score, 4),
            threshold=threshold,
            passed=score >= threshold,
            total=total,
            matched=matched,
            failures=failures,
        )

    # ------------------------------------------------------------------
    # Dimension 3: avatar_selection
    # ------------------------------------------------------------------

    def _score_avatar_selection(self) -> DimensionScore:
        name = "avatar_selection"
        threshold = self.thresholds.get(name, 0.80)

        relevant = [tc for tc in self.test_cases if tc.get("expected_avatars")]
        if not relevant:
            return DimensionScore(name=name, score=1.0, threshold=threshold, passed=True,
                                  total=0, matched=0)

        matched = 0
        failures: list[str] = []

        for tc in relevant:
            q = tc["question"]
            expected = set(str(a).lower() for a in tc["expected_avatars"])
            results = self.retriever.retrieve_avatar(q, top_k=self.top_k)
            # match by avatar dir name, avatar id, or partial match
            retrieved_ids: set[str] = set()
            for r in results:
                retrieved_ids.add(r.id.lower())
                # also add dir fragment from file_path
                parts = r.file_path.replace("\\", "/").split("/")
                for p in parts:
                    retrieved_ids.add(p.lower())

            hit = False
            for exp in expected:
                for rid in retrieved_ids:
                    if exp in rid or rid in exp:
                        hit = True
                        break

            if hit:
                matched += 1
            else:
                failures.append(
                    f"[{tc.get('id', '?')}] Q: {q!r} — expected {expected}, got {retrieved_ids}"
                )

        total = len(relevant)
        score = matched / total if total else 1.0
        return DimensionScore(
            name=name,
            score=round(score, 4),
            threshold=threshold,
            passed=score >= threshold,
            total=total,
            matched=matched,
            failures=failures,
        )

    # ------------------------------------------------------------------
    # Dimension 4: index_integrity
    # ------------------------------------------------------------------

    def _score_index_integrity(self) -> DimensionScore:
        name = "index_integrity"
        threshold = self.thresholds.get(name, 0.95)

        total = 0
        matched = 0
        failures: list[str] = []

        # Check skill domain index.yaml entries
        skills_root = self.constitution_path / "agent-skills" / "skills-by-domain"
        if skills_root.exists():
            for domain_dir in sorted(skills_root.iterdir()):
                if not domain_dir.is_dir():
                    continue
                idx_path = domain_dir / "index.yaml"
                if not idx_path.exists():
                    continue
                idx = _load_yaml_safe(idx_path)
                for skill in idx.get("skills", []):
                    fname = skill.get("file", "")
                    if not fname:
                        continue
                    total += 1
                    skill_file = domain_dir / fname
                    if skill_file.exists():
                        matched += 1
                    else:
                        failures.append(f"skill index broken ref: {domain_dir.name}/{fname}")

        # Check laws/index.yaml file entries
        laws_index_path = self.constitution_path / "laws" / "index.yaml"
        if laws_index_path.exists():
            laws_idx = _load_yaml_safe(laws_index_path)
            for domain, domain_data in laws_idx.get("domains", {}).items():
                if not isinstance(domain_data, dict):
                    continue
                for fname in domain_data.get("files", []):
                    total += 1
                    f = self.constitution_path / "laws" / domain / fname
                    if f.exists():
                        matched += 1
                    else:
                        failures.append(f"laws index broken ref: laws/{domain}/{fname}")

        # Check AVATAR-RAG-INDEX.yaml file entries
        rag_index_path = self.constitution_path / "avatars" / "AVATAR-RAG-INDEX.yaml"
        if rag_index_path.exists():
            rag_idx = _load_yaml_safe(rag_index_path)
            for entry in rag_idx.get("avatars", []):
                for fpath in entry.get("files", []):
                    total += 1
                    full = self.constitution_path / "avatars" / fpath
                    if full.exists():
                        matched += 1
                    else:
                        failures.append(f"AVATAR-RAG-INDEX broken ref: {fpath}")

        score = matched / total if total else 1.0
        return DimensionScore(
            name=name,
            score=round(score, 4),
            threshold=threshold,
            passed=score >= threshold,
            total=total,
            matched=matched,
            failures=failures[:20],  # cap verbose output
        )

    # ------------------------------------------------------------------
    # Dimension 5: cross_ref_consistency
    # ------------------------------------------------------------------

    def _score_cross_ref_consistency(self) -> DimensionScore:
        name = "cross_ref_consistency"
        threshold = self.thresholds.get(name, 0.95)

        registered_law_ids = _collect_registered_law_ids(self.constitution_path, self._law_id_re)

        total = 0
        matched = 0
        failures: list[str] = []

        def _check_file(path: Path, label: str) -> None:
            nonlocal total, matched
            text = path.read_text(encoding="utf-8", errors="replace")
            ids = self._law_id_re.findall(text)
            for lid in ids:
                total += 1
                if lid in registered_law_ids:
                    matched += 1
                else:
                    failures.append(f"{label}: unknown law ID {lid!r}")

        # Check skill files
        skills_root = self.constitution_path / "agent-skills" / "skills-by-domain"
        if skills_root.exists():
            for md_file in skills_root.rglob("*.md"):
                rel = str(md_file.relative_to(self.constitution_path))
                _check_file(md_file, rel)
            for yaml_file in skills_root.rglob("index.yaml"):
                rel = str(yaml_file.relative_to(self.constitution_path))
                _check_file(yaml_file, rel)

        # Check avatar manifest and guidance files
        avatars_dir = self.constitution_path / "avatars"
        if avatars_dir.exists():
            for fpath in avatars_dir.rglob("manifest.yaml"):
                rel = str(fpath.relative_to(self.constitution_path))
                _check_file(fpath, rel)
            for fpath in avatars_dir.rglob("guidance.md"):
                rel = str(fpath.relative_to(self.constitution_path))
                _check_file(fpath, rel)

        score = matched / total if total else 1.0
        return DimensionScore(
            name=name,
            score=round(score, 4),
            threshold=threshold,
            passed=score >= threshold,
            total=total,
            matched=matched,
            failures=list(dict.fromkeys(failures))[:20],  # deduplicate + cap
        )
