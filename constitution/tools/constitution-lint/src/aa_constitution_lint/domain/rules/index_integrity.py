"""Index integrity rules — validate all index files are in sync with disk (v0.2.0)."""
from __future__ import annotations
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING
import yaml
from aa_constitution_lint.domain.models import EvaluationResult, LawEvaluation
from aa_constitution_lint.domain.rules.base import Rule

if TYPE_CHECKING:
    from aa_constitution_lint.infrastructure.law_registry import LawRegistry

LAW_ID_PATTERN = re.compile(r"\b[A-Z]+-\d+\.\d+\b")
METADATA_KEYS = {"version", "name", "created", "updated", "rag_config", "token_optimization"}


def _now() -> datetime:
    return datetime.now(UTC)


def _is_constitution_repo(project_path: Path) -> bool:
    return (project_path / "laws" / "index.yaml").exists() and (project_path / "avatars").is_dir()


class LawsRegistryFilesExistRule(Rule):
    """Files listed in laws/index.yaml must exist on disk."""

    @property
    def id(self) -> str:
        return "index.laws_registry_files_exist"

    @property
    def law_id(self) -> str:
        return "ENG-10.1"

    @property
    def description(self) -> str:
        return "All files listed per domain in laws/index.yaml must exist on disk"

    def evaluate(self, project_path: Path) -> list[LawEvaluation]:
        if not _is_constitution_repo(project_path):
            return []
        results = []
        index_path = project_path / "laws" / "index.yaml"
        try:
            data = yaml.safe_load(index_path.read_text(encoding="utf-8")) or {}
        except Exception as e:
            return [LawEvaluation(
                law_id=self.law_id, result=EvaluationResult.FAIL,
                evaluation_point="aa-constitution-lint", timestamp=_now(),
                context={"rule": self.id, "file_path": "laws/index.yaml", "message": f"Failed to parse laws/index.yaml: {e}"},
            )]
        domains = data.get("domains", {}) or {}
        for domain, domain_data in domains.items():
            if not isinstance(domain_data, dict):
                continue
            for filename in (domain_data.get("files") or []):
                full_path = project_path / "laws" / domain / filename
                if not full_path.exists():
                    rel = f"laws/{domain}/{filename}"
                    results.append(LawEvaluation(
                        law_id=self.law_id, result=EvaluationResult.FAIL,
                        evaluation_point="aa-constitution-lint", timestamp=_now(),
                        context={
                            "rule": self.id, "file_path": rel,
                            "message": f"laws/index.yaml references missing file: {rel}",
                        },
                    ))
        if not results:
            results.append(LawEvaluation(
                law_id=self.law_id, result=EvaluationResult.PASS,
                evaluation_point="aa-constitution-lint", timestamp=_now(),
                context={"rule": self.id, "message": "All files in laws/index.yaml exist on disk"},
            ))
        return results


class LawsRegistryCompleteRule(Rule):
    """All .md files in laws/{domain}/ must be listed in laws/index.yaml."""

    @property
    def id(self) -> str:
        return "index.laws_registry_complete"

    @property
    def law_id(self) -> str:
        return "ENG-10.1"

    @property
    def description(self) -> str:
        return "All .md files in laws/{domain}/ must be listed in laws/index.yaml (no orphans)"

    def evaluate(self, project_path: Path) -> list[LawEvaluation]:
        if not _is_constitution_repo(project_path):
            return []
        results = []
        index_path = project_path / "laws" / "index.yaml"
        try:
            data = yaml.safe_load(index_path.read_text(encoding="utf-8")) or {}
        except Exception:
            return []
        domains = data.get("domains", {}) or {}
        laws_dir = project_path / "laws"
        for domain_dir in sorted(laws_dir.iterdir()):
            if not domain_dir.is_dir():
                continue
            domain = domain_dir.name
            domain_data = domains.get(domain, {}) or {}
            indexed = set(domain_data.get("files") or [])
            for md_file in sorted(domain_dir.glob("*.md")):
                if md_file.name not in indexed:
                    rel = f"laws/{domain}/{md_file.name}"
                    results.append(LawEvaluation(
                        law_id=self.law_id, result=EvaluationResult.FAIL,
                        evaluation_point="aa-constitution-lint", timestamp=_now(),
                        context={
                            "rule": self.id, "file_path": rel,
                            "message": f"Orphan law file not listed in laws/index.yaml: {rel}",
                        },
                    ))
        if not results:
            results.append(LawEvaluation(
                law_id=self.law_id, result=EvaluationResult.PASS,
                evaluation_point="aa-constitution-lint", timestamp=_now(),
                context={"rule": self.id, "message": "All law .md files are listed in laws/index.yaml"},
            ))
        return results


class AvatarRagCompleteRule(Rule):
    """Every avatar directory must have an entry in AVATAR-RAG-INDEX.yaml."""

    @property
    def id(self) -> str:
        return "index.avatar_rag_complete"

    @property
    def law_id(self) -> str:
        return "ENG-10.1"

    @property
    def description(self) -> str:
        return "Every avatar dir in product-type/ and technology/ must appear in AVATAR-RAG-INDEX.yaml"

    def evaluate(self, project_path: Path) -> list[LawEvaluation]:
        if not _is_constitution_repo(project_path):
            return []
        results = []
        rag_path = project_path / "avatars" / "AVATAR-RAG-INDEX.yaml"
        if not rag_path.exists():
            return [LawEvaluation(
                law_id=self.law_id, result=EvaluationResult.FAIL,
                evaluation_point="aa-constitution-lint", timestamp=_now(),
                context={"rule": self.id, "file_path": "avatars/AVATAR-RAG-INDEX.yaml", "message": "AVATAR-RAG-INDEX.yaml not found"},
            )]
        try:
            data = yaml.safe_load(rag_path.read_text(encoding="utf-8")) or {}
        except Exception as e:
            return [LawEvaluation(
                law_id=self.law_id, result=EvaluationResult.FAIL,
                evaluation_point="aa-constitution-lint", timestamp=_now(),
                context={"rule": self.id, "file_path": "avatars/AVATAR-RAG-INDEX.yaml", "message": f"Failed to parse AVATAR-RAG-INDEX.yaml: {e}"},
            )]
        rag_keys: set[str] = set()
        for key, value in data.items():
            if key in METADATA_KEYS:
                continue
            section_keys = ("product_type_avatars", "technology_avatars", "product-type-avatars", "industry_avatars")
            if key in section_keys and isinstance(value, dict):
                rag_keys.update(value.keys())
            else:
                rag_keys.add(key)
        # Normalize all collected keys to hyphenated form for consistent lookup
        rag_keys_normalized = {k.replace("_", "-") for k in rag_keys}
        for category in ("product-type", "technology"):
            cat_dir = project_path / "avatars" / category
            if not cat_dir.is_dir():
                continue
            for avatar_dir in sorted(cat_dir.iterdir()):
                if not avatar_dir.is_dir():
                    continue
                # Accept both hyphenated (python-fastapi) and underscored (python_fastapi) keys
                if avatar_dir.name not in rag_keys_normalized:
                    results.append(LawEvaluation(
                        law_id=self.law_id, result=EvaluationResult.FAIL,
                        evaluation_point="aa-constitution-lint", timestamp=_now(),
                        context={
                            "rule": self.id, "avatar": avatar_dir.name,
                            "file_path": f"avatars/{category}/{avatar_dir.name}/",
                            "message": f"Avatar '{avatar_dir.name}' has no entry in AVATAR-RAG-INDEX.yaml (expected key: '{avatar_dir.name}' or '{avatar_dir.name.replace('-', '_')}')",
                        },
                    ))
        if not results:
            results.append(LawEvaluation(
                law_id=self.law_id, result=EvaluationResult.PASS,
                evaluation_point="aa-constitution-lint", timestamp=_now(),
                context={"rule": self.id, "message": "All avatar directories are in AVATAR-RAG-INDEX.yaml"},
            ))
        return results


class AvatarRagFilesExistRule(Rule):
    """All file paths in AVATAR-RAG-INDEX.yaml must exist on disk."""

    @property
    def id(self) -> str:
        return "index.avatar_rag_files_exist"

    @property
    def law_id(self) -> str:
        return "ENG-10.1"

    @property
    def description(self) -> str:
        return "All file paths referenced in AVATAR-RAG-INDEX.yaml must exist on disk"

    def _extract_file_paths(self, data: object, prefix: str) -> list[tuple[str, str]]:
        """Extract (avatar_id, file_path) tuples from nested RAG index data."""
        paths: list[tuple[str, str]] = []
        if isinstance(data, dict):
            if "files" in data:
                files_block = data["files"]
                avatar_id = data.get("id", prefix)
                if isinstance(files_block, dict):
                    for _k, v in files_block.items():
                        if isinstance(v, str) and ("." in v or "/" in v):
                            paths.append((str(avatar_id), v))
                elif isinstance(files_block, list):
                    for item in files_block:
                        if isinstance(item, str) and ("." in item or "/" in item):
                            paths.append((str(avatar_id), item))
            for k, v in data.items():
                if k != "files":
                    paths.extend(self._extract_file_paths(v, prefix))
        elif isinstance(data, list):
            for item in data:
                paths.extend(self._extract_file_paths(item, prefix))
        return paths

    def evaluate(self, project_path: Path) -> list[LawEvaluation]:
        if not _is_constitution_repo(project_path):
            return []
        results = []
        rag_path = project_path / "avatars" / "AVATAR-RAG-INDEX.yaml"
        if not rag_path.exists():
            return []
        try:
            data = yaml.safe_load(rag_path.read_text(encoding="utf-8")) or {}
        except Exception:
            return []
        for section_key, category in (("product_type_avatars", "product-type"), ("technology_avatars", "technology")):
            section = data.get(section_key, {}) or {}
            if not isinstance(section, dict):
                continue
            for avatar_id, avatar_data in section.items():
                if not isinstance(avatar_data, dict):
                    continue
                files_block = avatar_data.get("files", {}) or {}
                avatar_name = avatar_id.replace("_", "-")
                base_dir = project_path / "avatars" / category / avatar_name
                for _file_key, file_val in (files_block.items() if isinstance(files_block, dict) else []):
                    if not isinstance(file_val, str):
                        continue
                    file_val_clean = file_val.split(" (")[0].strip()
                    if not ("." in file_val_clean):
                        continue
                    # Paths starting with docs/, laws/, agent-skills/, etc. are
                    # repo-root-relative; avatar-local paths resolve from base_dir.
                    if file_val_clean.startswith(("docs/", "laws/", "agent-skills/", "avatars/", "tools/")):
                        full = project_path / file_val_clean
                        rel = file_val_clean
                    else:
                        full = base_dir / file_val_clean
                        rel = f"avatars/{category}/{avatar_name}/{file_val_clean}"
                    if not full.exists():
                        results.append(LawEvaluation(
                            law_id=self.law_id, result=EvaluationResult.FAIL,
                            evaluation_point="aa-constitution-lint", timestamp=_now(),
                            context={
                                "rule": self.id, "avatar": avatar_id,
                                "file_path": rel,
                                "message": f"AVATAR-RAG-INDEX.yaml references missing file: {rel}",
                            },
                        ))
        if not results:
            results.append(LawEvaluation(
                law_id=self.law_id, result=EvaluationResult.PASS,
                evaluation_point="aa-constitution-lint", timestamp=_now(),
                context={"rule": self.id, "message": "All files referenced in AVATAR-RAG-INDEX.yaml exist on disk"},
            ))
        return results


class AvatarRagLawsValidRule(Rule):
    """All law IDs in AVATAR-RAG-INDEX.yaml must be valid registered laws."""

    def __init__(self, registry: "LawRegistry | None" = None) -> None:
        self._registry = registry

    @property
    def id(self) -> str:
        return "index.avatar_rag_laws_valid"

    @property
    def law_id(self) -> str:
        return "ENG-10.1"

    @property
    def description(self) -> str:
        return "All law IDs in AVATAR-RAG-INDEX.yaml must be registered"

    def evaluate(self, project_path: Path) -> list[LawEvaluation]:
        if not _is_constitution_repo(project_path):
            return []
        if self._registry is None:
            return []
        results = []
        rag_path = project_path / "avatars" / "AVATAR-RAG-INDEX.yaml"
        if not rag_path.exists():
            return []
        try:
            content = rag_path.read_text(encoding="utf-8")
        except Exception:
            return []
        for match in LAW_ID_PATTERN.finditer(content):
            law_id = match.group(0)
            if not self._registry.law_exists(law_id):
                results.append(LawEvaluation(
                    law_id=self.law_id, result=EvaluationResult.FAIL,
                    evaluation_point="aa-constitution-lint", timestamp=_now(),
                    context={
                        "rule": self.id, "file_path": "avatars/AVATAR-RAG-INDEX.yaml",
                        "invalid_law": law_id,
                        "message": f"AVATAR-RAG-INDEX.yaml references unknown law ID: {law_id}",
                    },
                ))
        if not results:
            results.append(LawEvaluation(
                law_id=self.law_id, result=EvaluationResult.PASS,
                evaluation_point="aa-constitution-lint", timestamp=_now(),
                context={"rule": self.id, "message": "All law IDs in AVATAR-RAG-INDEX.yaml are valid"},
            ))
        return results


class AvatarIndexCompleteRule(Rule):
    """All avatar directories must be listed in their respective index.yaml."""

    @property
    def id(self) -> str:
        return "index.avatar_index_complete"

    @property
    def law_id(self) -> str:
        return "ENG-10.1"

    @property
    def description(self) -> str:
        return "All avatar dirs must be listed in avatars/index.yaml (tech) and avatars/product-type/index.yaml (product)"

    def evaluate(self, project_path: Path) -> list[LawEvaluation]:
        if not _is_constitution_repo(project_path):
            return []
        results = []

        tech_index = project_path / "avatars" / "index.yaml"
        if tech_index.exists():
            try:
                data = yaml.safe_load(tech_index.read_text(encoding="utf-8")) or {}
                tech_entries = data.get("technology", []) or []
                indexed_ids: set[str] = set()
                for entry in tech_entries:
                    if isinstance(entry, dict) and "id" in entry:
                        path_val = entry.get("path", "")
                        if path_val:
                            dir_name = path_val.strip("/").split("/")[-1]
                            indexed_ids.add(dir_name)
                tech_dir = project_path / "avatars" / "technology"
                if tech_dir.is_dir():
                    for avatar_dir in sorted(tech_dir.iterdir()):
                        if not avatar_dir.is_dir():
                            continue
                        if avatar_dir.name not in indexed_ids:
                            results.append(LawEvaluation(
                                law_id=self.law_id, result=EvaluationResult.FAIL,
                                evaluation_point="aa-constitution-lint", timestamp=_now(),
                                context={
                                    "rule": self.id, "avatar": avatar_dir.name,
                                    "file_path": "avatars/index.yaml",
                                    "message": f"Technology avatar '{avatar_dir.name}' not listed in avatars/index.yaml",
                                },
                            ))
            except Exception:
                pass

        pt_index = project_path / "avatars" / "product-type" / "index.yaml"
        if pt_index.exists():
            try:
                data = yaml.safe_load(pt_index.read_text(encoding="utf-8")) or {}
                avatars_list = data.get("avatars", []) or []
                indexed_ids_pt: set[str] = set()
                for entry in avatars_list:
                    if isinstance(entry, dict):
                        if "id" in entry:
                            indexed_ids_pt.add(entry["id"])
                        if "path" in entry:
                            dir_name = entry["path"].strip("/").split("/")[-1]
                            indexed_ids_pt.add(dir_name)
                pt_dir = project_path / "avatars" / "product-type"
                if pt_dir.is_dir():
                    for avatar_dir in sorted(pt_dir.iterdir()):
                        if not avatar_dir.is_dir():
                            continue
                        if avatar_dir.name not in indexed_ids_pt:
                            results.append(LawEvaluation(
                                law_id=self.law_id, result=EvaluationResult.FAIL,
                                evaluation_point="aa-constitution-lint", timestamp=_now(),
                                context={
                                    "rule": self.id, "avatar": avatar_dir.name,
                                    "file_path": "avatars/product-type/index.yaml",
                                    "message": f"Product avatar '{avatar_dir.name}' not listed in avatars/product-type/index.yaml",
                                },
                            ))
            except Exception:
                pass

        if not results:
            results.append(LawEvaluation(
                law_id=self.law_id, result=EvaluationResult.PASS,
                evaluation_point="aa-constitution-lint", timestamp=_now(),
                context={"rule": self.id, "message": "All avatar directories are listed in their index files"},
            ))
        return results


class NonnegLawsConsistentRule(Rule):
    """Non-neg IDs in laws/index.yaml must match non_negotiable: true in law file frontmatter."""

    @property
    def id(self) -> str:
        return "index.nonneg_laws_consistent"

    @property
    def law_id(self) -> str:
        return "ENG-10.1"

    @property
    def description(self) -> str:
        return "Non-negotiable law IDs in laws/index.yaml must match non_negotiable: true in law .md frontmatter"

    _FM_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)

    def _get_index_nonneg(self, project_path: Path) -> set[str]:
        """Extract non-negotiable law IDs from laws/index.yaml."""
        ids: set[str] = set()
        index_path = project_path / "laws" / "index.yaml"
        try:
            data = yaml.safe_load(index_path.read_text(encoding="utf-8")) or {}
        except Exception:
            return ids

        def _collect(node: object) -> None:
            if isinstance(node, str) and LAW_ID_PATTERN.match(node):
                ids.add(node)
            elif isinstance(node, dict):
                for v in node.values():
                    _collect(v)
            elif isinstance(node, list):
                for item in node:
                    _collect(item)

        nonneg = data.get("non_negotiable", {})
        avi_nonneg = data.get("aviation_non_negotiable", {})
        _collect(nonneg)
        _collect(avi_nonneg)
        return ids

    def _get_file_nonneg(self, project_path: Path) -> set[str]:
        """Extract law IDs with non_negotiable: true from all law .md frontmatter."""
        ids: set[str] = set()
        laws_dir = project_path / "laws"
        for md_file in laws_dir.rglob("*.md"):
            try:
                content = md_file.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            match = self._FM_RE.match(content)
            if not match:
                continue
            try:
                fm = yaml.safe_load(match.group(1)) or {}
            except yaml.YAMLError:
                continue
            for entry in (fm.get("laws") or []):
                if isinstance(entry, dict) and entry.get("non_negotiable") is True and "id" in entry:
                    ids.add(entry["id"])
        return ids

    def evaluate(self, project_path: Path) -> list[LawEvaluation]:
        if not _is_constitution_repo(project_path):
            return []
        results = []
        index_nonneg = self._get_index_nonneg(project_path)
        file_nonneg = self._get_file_nonneg(project_path)

        for law_id in sorted(index_nonneg - file_nonneg):
            results.append(LawEvaluation(
                law_id=self.law_id, result=EvaluationResult.FAIL,
                evaluation_point="aa-constitution-lint", timestamp=_now(),
                context={
                    "rule": self.id, "law": law_id,
                    "file_path": "laws/index.yaml",
                    "message": f"Law {law_id} in laws/index.yaml non_negotiable but no non_negotiable: true in law file",
                },
            ))
        for law_id in sorted(file_nonneg - index_nonneg):
            results.append(LawEvaluation(
                law_id=self.law_id, result=EvaluationResult.FAIL,
                evaluation_point="aa-constitution-lint", timestamp=_now(),
                context={
                    "rule": self.id, "law": law_id,
                    "file_path": "laws/",
                    "message": f"Law {law_id} has non_negotiable: true in law file but not listed in laws/index.yaml non_negotiable",
                },
            ))
        if not results:
            results.append(LawEvaluation(
                law_id=self.law_id, result=EvaluationResult.PASS,
                evaluation_point="aa-constitution-lint", timestamp=_now(),
                context={"rule": self.id, "message": "Non-negotiable law sets are consistent"},
            ))
        return results
