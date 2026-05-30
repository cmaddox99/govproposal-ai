"""Constitution self-governance rules (v0.2.0)."""
from __future__ import annotations
import re
from datetime import UTC, datetime
from pathlib import Path
import yaml
from aa_constitution_lint.domain.models import EvaluationResult, LawEvaluation
from aa_constitution_lint.domain.rules.base import Rule

NONNEG_PRD_LAWS = ["PRD-1.2", "PRD-1.5", "PRD-2.5", "PRD-5.1", "PRD-6.2"]
NONNEG_ENG_LAWS = ["ENG-4.1", "ENG-6.1", "ENG-6.4", "ENG-6.7"]
NONNEG_ALL_LAWS = [
    "ENG-4.1","ENG-6.1","ENG-6.4","ENG-6.7",
    "PRD-1.2","PRD-1.5","PRD-2.5","PRD-5.1","PRD-6.2",
    "BUS-1.1","BUS-4.3","BUS-7.1","BUS-9.3",
]
LAW_ID_PATTERN = re.compile(r"\b[A-Z]+-\d+\.\d+\b")


def _now() -> datetime:
    return datetime.now(UTC)


class ProductAvatarCompletenessRule(Rule):
    """Every product avatar must have manifest.yaml, guidance.md, and examples/."""

    @property
    def id(self) -> str:
        return "constitution.product_avatar_completeness"

    @property
    def law_id(self) -> str:
        return "ENG-10.1"

    @property
    def description(self) -> str:
        return "Every product avatar directory must contain manifest.yaml, guidance.md, and examples/"

    def _is_constitution_repo(self, project_path: Path) -> bool:
        return (project_path / "laws" / "index.yaml").exists() and (project_path / "avatars").is_dir()

    def evaluate(self, project_path: Path) -> list[LawEvaluation]:
        if not self._is_constitution_repo(project_path):
            return []
        results = []
        product_dir = project_path / "avatars" / "product-type"
        if not product_dir.is_dir():
            return []
        for avatar_dir in sorted(product_dir.iterdir()):
            if not avatar_dir.is_dir():
                continue
            for required in ["manifest.yaml", "guidance.md"]:
                if not (avatar_dir / required).exists():
                    results.append(LawEvaluation(
                        law_id=self.law_id, result=EvaluationResult.FAIL,
                        evaluation_point="aa-constitution-lint", timestamp=_now(),
                        context={
                            "rule": self.id, "avatar": avatar_dir.name,
                            "file_path": f"avatars/product-type/{avatar_dir.name}/{required}",
                            "message": f"Product avatar '{avatar_dir.name}' missing required file: {required}",
                        },
                    ))
            if not (avatar_dir / "examples").is_dir():
                results.append(LawEvaluation(
                    law_id=self.law_id, result=EvaluationResult.FAIL,
                    evaluation_point="aa-constitution-lint", timestamp=_now(),
                    context={
                        "rule": self.id, "avatar": avatar_dir.name,
                        "file_path": f"avatars/product-type/{avatar_dir.name}/examples/",
                        "message": f"Product avatar '{avatar_dir.name}' missing required directory: examples/",
                    },
                ))
        if not results:
            results.append(LawEvaluation(
                law_id=self.law_id, result=EvaluationResult.PASS,
                evaluation_point="aa-constitution-lint", timestamp=_now(),
                context={"rule": self.id, "message": "All product avatars have required files"},
            ))
        return results


class TechAvatarCompletenessRule(Rule):
    """Every technology avatar must have manifest.yaml, guidance.md, and examples/."""

    @property
    def id(self) -> str:
        return "constitution.tech_avatar_completeness"

    @property
    def law_id(self) -> str:
        return "ENG-10.1"

    @property
    def description(self) -> str:
        return "Every technology avatar directory must contain manifest.yaml, guidance.md, and examples/"

    def _is_constitution_repo(self, project_path: Path) -> bool:
        return (project_path / "laws" / "index.yaml").exists() and (project_path / "avatars").is_dir()

    def evaluate(self, project_path: Path) -> list[LawEvaluation]:
        if not self._is_constitution_repo(project_path):
            return []
        results = []
        tech_dir = project_path / "avatars" / "technology"
        if not tech_dir.is_dir():
            return []
        for avatar_dir in sorted(tech_dir.iterdir()):
            if not avatar_dir.is_dir():
                continue
            for required in ["manifest.yaml", "guidance.md"]:
                if not (avatar_dir / required).exists():
                    results.append(LawEvaluation(
                        law_id=self.law_id, result=EvaluationResult.FAIL,
                        evaluation_point="aa-constitution-lint", timestamp=_now(),
                        context={
                            "rule": self.id, "avatar": avatar_dir.name,
                            "file_path": f"avatars/technology/{avatar_dir.name}/{required}",
                            "message": f"Technology avatar '{avatar_dir.name}' missing required file: {required}",
                        },
                    ))
            if not (avatar_dir / "examples").is_dir():
                results.append(LawEvaluation(
                    law_id=self.law_id, result=EvaluationResult.FAIL,
                    evaluation_point="aa-constitution-lint", timestamp=_now(),
                    context={
                        "rule": self.id, "avatar": avatar_dir.name,
                        "file_path": f"avatars/technology/{avatar_dir.name}/examples/",
                        "message": f"Technology avatar '{avatar_dir.name}' missing required directory: examples/",
                    },
                ))
        if not results:
            results.append(LawEvaluation(
                law_id=self.law_id, result=EvaluationResult.PASS,
                evaluation_point="aa-constitution-lint", timestamp=_now(),
                context={"rule": self.id, "message": "All technology avatars have required files"},
            ))
        return results


class ProductAvatarNonnegExamplesRule(Rule):
    """Product avatar examples/ must reference each non-negotiable PRD law."""

    @property
    def id(self) -> str:
        return "constitution.product_avatar_nonneg_examples"

    @property
    def law_id(self) -> str:
        return "ENG-10.1"

    @property
    def description(self) -> str:
        return "Product avatar examples/ must cover non-negotiable PRD laws: " + ", ".join(NONNEG_PRD_LAWS)

    def _is_constitution_repo(self, project_path: Path) -> bool:
        return (project_path / "laws" / "index.yaml").exists() and (project_path / "avatars").is_dir()

    def evaluate(self, project_path: Path) -> list[LawEvaluation]:
        if not self._is_constitution_repo(project_path):
            return []
        results = []
        product_dir = project_path / "avatars" / "product-type"
        if not product_dir.is_dir():
            return []
        for avatar_dir in sorted(product_dir.iterdir()):
            if not avatar_dir.is_dir():
                continue
            examples_dir = avatar_dir / "examples"
            if not examples_dir.is_dir():
                continue
            mentioned: set[str] = set()
            for f in examples_dir.rglob("*"):
                if f.is_file():
                    try:
                        content = f.read_text(encoding="utf-8")
                        mentioned.update(LAW_ID_PATTERN.findall(content))
                    except (OSError, UnicodeDecodeError):
                        pass
            for law in NONNEG_PRD_LAWS:
                if law not in mentioned:
                    results.append(LawEvaluation(
                        law_id=self.law_id, result=EvaluationResult.FAIL,
                        evaluation_point="aa-constitution-lint", timestamp=_now(),
                        context={
                            "rule": self.id, "avatar": avatar_dir.name, "missing_law": law,
                            "file_path": f"avatars/product-type/{avatar_dir.name}/examples/",
                            "message": f"Product avatar '{avatar_dir.name}' examples/ has no coverage for non-neg law {law}",
                        },
                    ))
        if not results:
            results.append(LawEvaluation(
                law_id=self.law_id, result=EvaluationResult.PASS,
                evaluation_point="aa-constitution-lint", timestamp=_now(),
                context={"rule": self.id, "message": "All product avatar examples cover required non-neg PRD laws"},
            ))
        return results


class TechAvatarNonnegExamplesRule(Rule):
    """Technology avatar examples/ must reference each non-negotiable ENG law."""

    @property
    def id(self) -> str:
        return "constitution.tech_avatar_nonneg_examples"

    @property
    def law_id(self) -> str:
        return "ENG-10.1"

    @property
    def description(self) -> str:
        return "Technology avatar examples/ must cover non-negotiable ENG laws: " + ", ".join(NONNEG_ENG_LAWS)

    def _is_constitution_repo(self, project_path: Path) -> bool:
        return (project_path / "laws" / "index.yaml").exists() and (project_path / "avatars").is_dir()

    def evaluate(self, project_path: Path) -> list[LawEvaluation]:
        if not self._is_constitution_repo(project_path):
            return []
        results = []
        tech_dir = project_path / "avatars" / "technology"
        if not tech_dir.is_dir():
            return []
        for avatar_dir in sorted(tech_dir.iterdir()):
            if not avatar_dir.is_dir():
                continue
            examples_dir = avatar_dir / "examples"
            if not examples_dir.is_dir():
                continue
            mentioned: set[str] = set()
            for f in examples_dir.rglob("*"):
                if f.is_file():
                    try:
                        content = f.read_text(encoding="utf-8")
                        mentioned.update(LAW_ID_PATTERN.findall(content))
                    except (OSError, UnicodeDecodeError):
                        pass
            for law in NONNEG_ENG_LAWS:
                if law not in mentioned:
                    results.append(LawEvaluation(
                        law_id=self.law_id, result=EvaluationResult.FAIL,
                        evaluation_point="aa-constitution-lint", timestamp=_now(),
                        context={
                            "rule": self.id, "avatar": avatar_dir.name, "missing_law": law,
                            "file_path": f"avatars/technology/{avatar_dir.name}/examples/",
                            "message": f"Technology avatar '{avatar_dir.name}' examples/ has no coverage for non-neg law {law}",
                        },
                    ))
        if not results:
            results.append(LawEvaluation(
                law_id=self.law_id, result=EvaluationResult.PASS,
                evaluation_point="aa-constitution-lint", timestamp=_now(),
                context={"rule": self.id, "message": "All technology avatar examples cover required non-neg ENG laws"},
            ))
        return results


class NoDeprecatedAdoptionRule(Rule):
    """Product and technology avatars must not contain ADOPTION.md (deprecated)."""

    @property
    def id(self) -> str:
        return "constitution.no_deprecated_adoption"

    @property
    def law_id(self) -> str:
        return "ENG-10.1"

    @property
    def description(self) -> str:
        return "ADOPTION.md is deprecated; use guidance.md instead (industry avatars exempt)"

    def _is_constitution_repo(self, project_path: Path) -> bool:
        return (project_path / "laws" / "index.yaml").exists() and (project_path / "avatars").is_dir()

    def evaluate(self, project_path: Path) -> list[LawEvaluation]:
        if not self._is_constitution_repo(project_path):
            return []
        results = []
        for category in ("product-type", "technology"):
            cat_dir = project_path / "avatars" / category
            if not cat_dir.is_dir():
                continue
            for avatar_dir in sorted(cat_dir.iterdir()):
                if not avatar_dir.is_dir():
                    continue
                if (avatar_dir / "ADOPTION.md").exists():
                    results.append(LawEvaluation(
                        law_id=self.law_id, result=EvaluationResult.FAIL,
                        evaluation_point="aa-constitution-lint", timestamp=_now(),
                        context={
                            "rule": self.id, "avatar": avatar_dir.name,
                            "file_path": f"avatars/{category}/{avatar_dir.name}/ADOPTION.md",
                            "message": f"Deprecated ADOPTION.md found in '{avatar_dir.name}'; migrate content to guidance.md and delete",
                        },
                    ))
        if not results:
            results.append(LawEvaluation(
                law_id=self.law_id, result=EvaluationResult.PASS,
                evaluation_point="aa-constitution-lint", timestamp=_now(),
                context={"rule": self.id, "message": "No deprecated ADOPTION.md files found"},
            ))
        return results


class AvatarManifestSchemaRule(Rule):
    """Avatar manifest.yaml must have required top-level keys and nested avatar fields."""

    @property
    def id(self) -> str:
        return "constitution.avatar_manifest_schema"

    @property
    def law_id(self) -> str:
        return "ENG-10.1"

    @property
    def description(self) -> str:
        return "manifest.yaml must have avatar.id, avatar.type, avatar.name, activates, specializes_laws"

    def _is_constitution_repo(self, project_path: Path) -> bool:
        return (project_path / "laws" / "index.yaml").exists() and (project_path / "avatars").is_dir()

    def _check_manifest(self, manifest_path: Path, rel_path: str) -> list[LawEvaluation]:
        results = []
        try:
            data = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
        except Exception as e:
            return [LawEvaluation(
                law_id=self.law_id, result=EvaluationResult.FAIL,
                evaluation_point="aa-constitution-lint", timestamp=_now(),
                context={
                    "rule": self.id, "file_path": rel_path,
                    "message": f"Failed to parse {rel_path}: {e}",
                },
            )]
        for key in ("activates", "specializes_laws"):
            if key not in data:
                results.append(LawEvaluation(
                    law_id=self.law_id, result=EvaluationResult.FAIL,
                    evaluation_point="aa-constitution-lint", timestamp=_now(),
                    context={
                        "rule": self.id, "file_path": rel_path,
                        "message": f"manifest.yaml missing required top-level key: '{key}'",
                    },
                ))
        avatar_block = data.get("avatar", {}) or {}
        for sub_key in ("id", "type", "name"):
            if sub_key not in avatar_block:
                results.append(LawEvaluation(
                    law_id=self.law_id, result=EvaluationResult.FAIL,
                    evaluation_point="aa-constitution-lint", timestamp=_now(),
                    context={
                        "rule": self.id, "file_path": rel_path,
                        "message": f"manifest.yaml missing required key: avatar.{sub_key}",
                    },
                ))
        return results

    def evaluate(self, project_path: Path) -> list[LawEvaluation]:
        if not self._is_constitution_repo(project_path):
            return []
        results = []
        for category in ("product-type", "technology"):
            cat_dir = project_path / "avatars" / category
            if not cat_dir.is_dir():
                continue
            for avatar_dir in sorted(cat_dir.iterdir()):
                if not avatar_dir.is_dir():
                    continue
                manifest = avatar_dir / "manifest.yaml"
                if manifest.exists():
                    rel = f"avatars/{category}/{avatar_dir.name}/manifest.yaml"
                    results.extend(self._check_manifest(manifest, rel))
        if not results:
            results.append(LawEvaluation(
                law_id=self.law_id, result=EvaluationResult.PASS,
                evaluation_point="aa-constitution-lint", timestamp=_now(),
                context={"rule": self.id, "message": "All avatar manifests have required schema"},
            ))
        return results


class AvatarManifestNonnegCitationRule(Rule):
    """Avatar manifest specializes_laws should cite at least one non-negotiable law."""

    @property
    def id(self) -> str:
        return "constitution.avatar_manifest_nonneg_citation"

    @property
    def law_id(self) -> str:
        return "ENG-10.1"

    @property
    def description(self) -> str:
        return "specializes_laws in manifest.yaml should cite at least one non-negotiable law"

    def _is_constitution_repo(self, project_path: Path) -> bool:
        return (project_path / "laws" / "index.yaml").exists() and (project_path / "avatars").is_dir()

    def _extract_law_ids(self, value: object) -> list[str]:
        """Recursively extract law IDs from a YAML value."""
        ids: list[str] = []
        if isinstance(value, str) and LAW_ID_PATTERN.match(value):
            ids.append(value)
        elif isinstance(value, dict):
            if "id" in value and isinstance(value["id"], str):
                ids.append(value["id"])
            for v in value.values():
                ids.extend(self._extract_law_ids(v))
        elif isinstance(value, list):
            for item in value:
                ids.extend(self._extract_law_ids(item))
        return ids

    def evaluate(self, project_path: Path) -> list[LawEvaluation]:
        if not self._is_constitution_repo(project_path):
            return []
        results = []
        for category in ("product-type", "technology"):
            cat_dir = project_path / "avatars" / category
            if not cat_dir.is_dir():
                continue
            for avatar_dir in sorted(cat_dir.iterdir()):
                if not avatar_dir.is_dir():
                    continue
                manifest = avatar_dir / "manifest.yaml"
                if not manifest.exists():
                    continue
                try:
                    data = yaml.safe_load(manifest.read_text(encoding="utf-8")) or {}
                except Exception:
                    continue
                specializes = data.get("specializes_laws", [])
                cited = self._extract_law_ids(specializes)
                has_nonneg = any(law in NONNEG_ALL_LAWS for law in cited)
                if not has_nonneg:
                    rel = f"avatars/{category}/{avatar_dir.name}/manifest.yaml"
                    results.append(LawEvaluation(
                        law_id=self.law_id, result=EvaluationResult.WARNING,
                        evaluation_point="aa-constitution-lint", timestamp=_now(),
                        context={
                            "rule": self.id, "avatar": avatar_dir.name,
                            "file_path": rel,
                            "message": f"Avatar '{avatar_dir.name}' specializes_laws cites no non-negotiable laws",
                        },
                    ))
        if not results:
            results.append(LawEvaluation(
                law_id=self.law_id, result=EvaluationResult.PASS,
                evaluation_point="aa-constitution-lint", timestamp=_now(),
                context={"rule": self.id, "message": "All avatar manifests cite at least one non-negotiable law"},
            ))
        return results


class LawFrontmatterCompletenessRule(Rule):
    """All law .md files must have valid YAML frontmatter with required fields."""

    @property
    def id(self) -> str:
        return "constitution.law_frontmatter_completeness"

    @property
    def law_id(self) -> str:
        return "ENG-10.1"

    @property
    def description(self) -> str:
        return "Law .md files must have frontmatter with domain, article, title, and ≥1 law entry"

    def _is_constitution_repo(self, project_path: Path) -> bool:
        return (project_path / "laws" / "index.yaml").exists() and (project_path / "avatars").is_dir()

    _FM_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)

    def _check_file(self, md_file: Path, rel: str) -> list[LawEvaluation]:
        results = []
        try:
            content = md_file.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            return []
        match = self._FM_RE.match(content)
        if not match:
            return [LawEvaluation(
                law_id=self.law_id, result=EvaluationResult.FAIL,
                evaluation_point="aa-constitution-lint", timestamp=_now(),
                context={"rule": self.id, "file_path": rel, "message": f"{rel}: missing YAML frontmatter"},
            )]
        try:
            fm = yaml.safe_load(match.group(1)) or {}
        except yaml.YAMLError as e:
            return [LawEvaluation(
                law_id=self.law_id, result=EvaluationResult.FAIL,
                evaluation_point="aa-constitution-lint", timestamp=_now(),
                context={"rule": self.id, "file_path": rel, "message": f"{rel}: invalid YAML frontmatter: {e}"},
            )]
        for key in ("domain", "article", "title"):
            if key not in fm:
                results.append(LawEvaluation(
                    law_id=self.law_id, result=EvaluationResult.FAIL,
                    evaluation_point="aa-constitution-lint", timestamp=_now(),
                    context={"rule": self.id, "file_path": rel, "message": f"{rel}: frontmatter missing '{key}'"},
                ))
        laws_list = fm.get("laws", [])
        if not isinstance(laws_list, list) or len(laws_list) < 1:
            results.append(LawEvaluation(
                law_id=self.law_id, result=EvaluationResult.FAIL,
                evaluation_point="aa-constitution-lint", timestamp=_now(),
                context={"rule": self.id, "file_path": rel, "message": f"{rel}: 'laws:' must be a list with ≥1 entry"},
            ))
        else:
            for i, entry in enumerate(laws_list):
                if not isinstance(entry, dict):
                    continue
                for field in ("id", "title"):
                    if field not in entry:
                        results.append(LawEvaluation(
                            law_id=self.law_id, result=EvaluationResult.FAIL,
                            evaluation_point="aa-constitution-lint", timestamp=_now(),
                            context={
                                "rule": self.id, "file_path": rel,
                                "message": f"{rel}: laws[{i}] missing field '{field}'",
                            },
                        ))
                # non_negotiable is optional (defaults to false); only warn if absent on laws
                # that ARE non-negotiable per laws/index.yaml (checked by nonneg_laws_consistent rule)
        return results

    def evaluate(self, project_path: Path) -> list[LawEvaluation]:
        if not self._is_constitution_repo(project_path):
            return []
        results = []
        laws_dir = project_path / "laws"
        for domain in ("engineering", "product", "business"):
            domain_dir = laws_dir / domain
            if not domain_dir.is_dir():
                continue
            for md_file in sorted(domain_dir.glob("*.md")):
                rel = str(md_file.relative_to(project_path))
                results.extend(self._check_file(md_file, rel))
        if not results:
            results.append(LawEvaluation(
                law_id=self.law_id, result=EvaluationResult.PASS,
                evaluation_point="aa-constitution-lint", timestamp=_now(),
                context={"rule": self.id, "message": "All law files have valid frontmatter"},
            ))
        return results


class SkillIndexConsistencyRule(Rule):
    """Bidirectional check: skill index.yaml refs must exist on disk and vice versa."""

    @property
    def id(self) -> str:
        return "constitution.skill_index_consistency"

    @property
    def law_id(self) -> str:
        return "ENG-10.1"

    @property
    def description(self) -> str:
        return "Skill domain index.yaml file refs must exist on disk; all .md skill files must be indexed"

    def _is_constitution_repo(self, project_path: Path) -> bool:
        return (project_path / "laws" / "index.yaml").exists() and (project_path / "avatars").is_dir()

    def evaluate(self, project_path: Path) -> list[LawEvaluation]:
        if not self._is_constitution_repo(project_path):
            return []
        results = []
        skills_root = project_path / "agent-skills" / "skills-by-domain"
        if not skills_root.is_dir():
            return []
        for domain_dir in sorted(skills_root.iterdir()):
            if not domain_dir.is_dir():
                continue
            index_file = domain_dir / "index.yaml"
            if not index_file.exists():
                continue
            try:
                data = yaml.safe_load(index_file.read_text(encoding="utf-8")) or {}
            except Exception:
                continue
            skills_list = data.get("skills", []) or []
            indexed_files: set[str] = set()
            for entry in skills_list:
                if isinstance(entry, dict) and "file" in entry:
                    fname = entry["file"]
                    indexed_files.add(fname)
                    if not (domain_dir / fname).exists():
                        rel = f"agent-skills/skills-by-domain/{domain_dir.name}/{fname}"
                        results.append(LawEvaluation(
                            law_id=self.law_id, result=EvaluationResult.FAIL,
                            evaluation_point="aa-constitution-lint", timestamp=_now(),
                            context={
                                "rule": self.id, "domain": domain_dir.name,
                                "file_path": rel,
                                "message": f"Skill index references non-existent file: {rel}",
                            },
                        ))
                    # Also register examples file if present (supplementary, not a separate skill)
                    if isinstance(entry.get("examples"), str):
                        indexed_files.add(entry["examples"])
            for md_file in sorted(domain_dir.glob("*.md")):
                if md_file.name in ("index.yaml", "README.md"):
                    continue
                if md_file.name not in indexed_files:
                    rel = f"agent-skills/skills-by-domain/{domain_dir.name}/{md_file.name}"
                    results.append(LawEvaluation(
                        law_id=self.law_id, result=EvaluationResult.FAIL,
                        evaluation_point="aa-constitution-lint", timestamp=_now(),
                        context={
                            "rule": self.id, "domain": domain_dir.name,
                            "file_path": rel,
                            "message": f"Skill file not listed in domain index.yaml: {rel}",
                        },
                    ))
        if not results:
            results.append(LawEvaluation(
                law_id=self.law_id, result=EvaluationResult.PASS,
                evaluation_point="aa-constitution-lint", timestamp=_now(),
                context={"rule": self.id, "message": "All skill indexes are consistent with disk"},
            ))
        return results


# ---------------------------------------------------------------------------
# Law integrity rules (lint-law-integrity-checks proposal)
# ---------------------------------------------------------------------------

from aa_constitution_lint.domain.law_parser import (
    ConstitutionData,
    VALID_DEFERRED_STATUSES,
    title_matches_comment,
)


class LawTitleCoherenceRule(Rule):
    """Detect title mismatches between _domain.yaml comments and .md frontmatter."""

    @property
    def id(self) -> str:
        return "constitution.law_title_coherence"

    @property
    def law_id(self) -> str:
        return "ENG-10.1"

    @property
    def description(self) -> str:
        return (
            "Every law ID's _domain.yaml comment title must match "
            "its .md frontmatter title"
        )

    def evaluate(self, project_path: Path) -> list[LawEvaluation]:
        laws_dir = project_path / "laws"
        if not laws_dir.is_dir():
            return []

        data = ConstitutionData(laws_dir)
        mismatches: list[dict[str, str]] = []
        missing_comments: list[dict[str, str]] = []

        for registry in data.registries:
            for article in registry.articles:
                for law_id in article.law_ids:
                    file_title = data.law_file_titles.get(law_id)
                    if file_title is None:
                        continue  # no .md entry; handled by LawBodyExistenceRule
                    comment = article.law_comments.get(law_id)
                    if comment is None:
                        missing_comments.append({
                            "law_id": law_id,
                            "article": f"Article {article.roman}",
                            "domain": registry.domain,
                        })
                    elif not title_matches_comment(file_title, comment):
                        mismatches.append({
                            "law_id": law_id,
                            "registry_comment": comment,
                            "law_file_title": file_title,
                            "article": f"Article {article.roman}",
                            "domain": registry.domain,
                        })

        results: list[LawEvaluation] = []

        if mismatches:
            results.append(LawEvaluation(
                law_id=self.law_id,
                result=EvaluationResult.FAIL,
                evaluation_point="aa-constitution-lint",
                timestamp=_now(),
                context={
                    "rule": self.id,
                    "message": (
                        f"{len(mismatches)} law title mismatch(es) between "
                        f"_domain.yaml comments and .md frontmatter"
                    ),
                    "mismatches": mismatches,
                },
            ))

        if missing_comments:
            results.append(LawEvaluation(
                law_id=self.law_id,
                result=EvaluationResult.WARNING,
                evaluation_point="aa-constitution-lint",
                timestamp=_now(),
                context={
                    "rule": self.id,
                    "message": (
                        f"{len(missing_comments)} law ID(s) in _domain.yaml "
                        f"have no inline # comment title"
                    ),
                    "missing_comments": missing_comments,
                },
            ))

        if not results:
            results.append(LawEvaluation(
                law_id=self.law_id,
                result=EvaluationResult.PASS,
                evaluation_point="aa-constitution-lint",
                timestamp=_now(),
                context={
                    "rule": self.id,
                    "message": "All _domain.yaml comment titles match .md frontmatter titles",
                },
            ))

        return results


class LawBodyExistenceRule(Rule):
    """Detect law IDs in _domain.yaml with no .md body and no status acknowledgement."""

    @property
    def id(self) -> str:
        return "constitution.law_body_existence"

    @property
    def law_id(self) -> str:
        return "ENG-10.1"

    @property
    def description(self) -> str:
        return (
            "Every _domain.yaml article must either have .md body content "
            "for all declared laws or carry an acknowledgement status"
        )

    def evaluate(self, project_path: Path) -> list[LawEvaluation]:
        laws_dir = project_path / "laws"
        if not laws_dir.is_dir():
            return []

        data = ConstitutionData(laws_dir)
        phantom_articles: list[dict] = []

        for registry in data.registries:
            domain_dir = registry.source_file.parent.name
            authored_ids = data.law_file_ids_by_domain_dir.get(domain_dir, set())
            for article in registry.articles:
                missing = [lid for lid in article.law_ids if lid not in authored_ids]
                if missing and article.status not in VALID_DEFERRED_STATUSES:
                    phantom_articles.append({
                        "article": f"Article {article.roman}",
                        "title": article.title,
                        "domain": registry.domain,
                        "missing_count": len(missing),
                        "missing_ids": missing,
                    })

        results: list[LawEvaluation] = []

        if phantom_articles:
            results.append(LawEvaluation(
                law_id=self.law_id,
                result=EvaluationResult.FAIL,
                evaluation_point="aa-constitution-lint",
                timestamp=_now(),
                context={
                    "rule": self.id,
                    "message": (
                        f"{len(phantom_articles)} article(s) declare law IDs "
                        f"with no .md body and no acknowledgement status"
                    ),
                    "phantom_articles": phantom_articles,
                },
            ))
        else:
            results.append(LawEvaluation(
                law_id=self.law_id,
                result=EvaluationResult.PASS,
                evaluation_point="aa-constitution-lint",
                timestamp=_now(),
                context={
                    "rule": self.id,
                    "message": (
                        "All _domain.yaml articles have .md body content "
                        "or carry an acknowledgement status"
                    ),
                },
            ))

        return results


class DomainRegistrationCompletenessRule(Rule):
    """Detect .md frontmatter law IDs not registered in any _domain.yaml article."""

    @property
    def id(self) -> str:
        return "constitution.domain_registration_completeness"

    @property
    def law_id(self) -> str:
        return "ENG-10.1"

    @property
    def description(self) -> str:
        return (
            "Every law ID in .md frontmatter must be registered "
            "in its domain's _domain.yaml"
        )

    def evaluate(self, project_path: Path) -> list[LawEvaluation]:
        laws_dir = project_path / "laws"
        if not laws_dir.is_dir():
            return []

        data = ConstitutionData(laws_dir)

        # Build set of all registered IDs per domain dir
        registered_by_domain: dict[str, set[str]] = {}
        for registry in data.registries:
            domain_dir = registry.source_file.parent.name
            ids = registered_by_domain.setdefault(domain_dir, set())
            for article in registry.articles:
                ids.update(article.law_ids)

        orphan_laws: list[dict[str, str]] = []

        for domain_dir, authored_ids in data.law_file_ids_by_domain_dir.items():
            registered = registered_by_domain.get(domain_dir, set())
            for law_id in sorted(authored_ids):
                if law_id not in registered:
                    orphan_laws.append({
                        "law_id": law_id,
                        "domain": domain_dir,
                    })

        results: list[LawEvaluation] = []

        if orphan_laws:
            results.append(LawEvaluation(
                law_id=self.law_id,
                result=EvaluationResult.FAIL,
                evaluation_point="aa-constitution-lint",
                timestamp=_now(),
                context={
                    "rule": self.id,
                    "message": (
                        f"{len(orphan_laws)} law ID(s) in .md frontmatter "
                        f"are not registered in any _domain.yaml article"
                    ),
                    "orphan_laws": orphan_laws,
                },
            ))
        else:
            results.append(LawEvaluation(
                law_id=self.law_id,
                result=EvaluationResult.PASS,
                evaluation_point="aa-constitution-lint",
                timestamp=_now(),
                context={
                    "rule": self.id,
                    "message": "All .md frontmatter law IDs are registered in _domain.yaml",
                },
            ))

        return results
