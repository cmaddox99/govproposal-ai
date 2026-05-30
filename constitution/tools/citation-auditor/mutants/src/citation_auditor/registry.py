"""Registry loader for aa-citation-audit.

Architecture: Infrastructure layer (Phase 3 §2.3 / Phase 4 §4.1).
Responsibility: Load and parse laws/index.yaml + scan all domain law files
for title/summary (ADR-002: no per-law title/summary in index.yaml — must
scan individual law .md files).
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from citation_auditor.exceptions import RegistryLoadError
from typing import Annotated
from typing import Callable
from typing import ClassVar

MutantDict = Annotated[dict[str, Callable], "Mutant"] # type: ignore


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None): # type: ignore
    """Forward call to original or mutated function, depending on the environment"""
    import os # type: ignore
    mutant_under_test = os.environ['MUTANT_UNDER_TEST'] # type: ignore
    if mutant_under_test == 'fail': # type: ignore
        from mutmut.__main__ import MutmutProgrammaticFailException # type: ignore
        raise MutmutProgrammaticFailException('Failed programmatically')       # type: ignore
    elif mutant_under_test == 'stats': # type: ignore
        from mutmut.__main__ import record_trampoline_hit # type: ignore
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__) # type: ignore
        # (for class methods, orig is bound and thus does not need the explicit self argument)
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_' # type: ignore
    if not mutant_under_test.startswith(prefix): # type: ignore
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    mutant_name = mutant_under_test.rpartition('.')[-1] # type: ignore
    if self_arg is not None: # type: ignore
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs) # type: ignore
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs) # type: ignore
    return result # type: ignore


@dataclass(frozen=True)
class RegistryEntry:
    law_id: str
    domain: str
    non_negotiable: bool
    title: str | None
    summary: str | None


def load_registry(laws_dir: Path) -> dict[str, RegistryEntry]:
    args = [laws_dir]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_load_registry__mutmut_orig, x_load_registry__mutmut_mutants, args, kwargs, None)


def x_load_registry__mutmut_orig(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_1(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = None

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_2(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(None)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_3(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() and not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_4(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_5(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_6(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(None)

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_7(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = None
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_8(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir * "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_9(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "XXindex.yamlXX"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_10(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "INDEX.YAML"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_11(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_12(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(None)

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_13(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding=None) as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_14(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="XXutf-8XX") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_15(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="UTF-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_16(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = None
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_17(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(None)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_18(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(None) from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_19(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_20(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError(None)

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_21(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("XXRegistry load failed: index.yaml must be a YAML mappingXX")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_22(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("registry load failed: index.yaml must be a yaml mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_23(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("REGISTRY LOAD FAILED: INDEX.YAML MUST BE A YAML MAPPING")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_24(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = None
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_25(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") and {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_26(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get(None) or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_27(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("XXnon_negotiableXX") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_28(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("NON_NEGOTIABLE") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_29(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(None)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_30(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = None
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_31(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") and {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_32(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get(None) or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_33(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("XXlaw_idsXX") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_34(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("LAW_IDS") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_35(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = None

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_36(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = None
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_37(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = None
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_38(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = None
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_39(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") and {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_40(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get(None) or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_41(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("XXdomainsXX") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_42(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("DOMAINS") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_43(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_44(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            break
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_45(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") and []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_46(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get(None) or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_47(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("XXfilesXX") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_48(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("FILES") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_49(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = None
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_50(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir * rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_51(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_52(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                break
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_53(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(None, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_54(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, None, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_55(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, None)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_56(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_57(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_58(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, )

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_59(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = None
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_60(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = None

    return registry


def x_load_registry__mutmut_61(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=None,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_62(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=None,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_63(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=None,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_64(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=None,
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_65(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=None,
        )

    return registry


def x_load_registry__mutmut_66(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_67(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_68(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_69(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_70(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            )

    return registry


def x_load_registry__mutmut_71(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id not in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_72(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(None),
            summary=summary_map.get(law_id),
        )

    return registry


def x_load_registry__mutmut_73(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(None),
        )

    return registry

x_load_registry__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_load_registry__mutmut_1': x_load_registry__mutmut_1, 
    'x_load_registry__mutmut_2': x_load_registry__mutmut_2, 
    'x_load_registry__mutmut_3': x_load_registry__mutmut_3, 
    'x_load_registry__mutmut_4': x_load_registry__mutmut_4, 
    'x_load_registry__mutmut_5': x_load_registry__mutmut_5, 
    'x_load_registry__mutmut_6': x_load_registry__mutmut_6, 
    'x_load_registry__mutmut_7': x_load_registry__mutmut_7, 
    'x_load_registry__mutmut_8': x_load_registry__mutmut_8, 
    'x_load_registry__mutmut_9': x_load_registry__mutmut_9, 
    'x_load_registry__mutmut_10': x_load_registry__mutmut_10, 
    'x_load_registry__mutmut_11': x_load_registry__mutmut_11, 
    'x_load_registry__mutmut_12': x_load_registry__mutmut_12, 
    'x_load_registry__mutmut_13': x_load_registry__mutmut_13, 
    'x_load_registry__mutmut_14': x_load_registry__mutmut_14, 
    'x_load_registry__mutmut_15': x_load_registry__mutmut_15, 
    'x_load_registry__mutmut_16': x_load_registry__mutmut_16, 
    'x_load_registry__mutmut_17': x_load_registry__mutmut_17, 
    'x_load_registry__mutmut_18': x_load_registry__mutmut_18, 
    'x_load_registry__mutmut_19': x_load_registry__mutmut_19, 
    'x_load_registry__mutmut_20': x_load_registry__mutmut_20, 
    'x_load_registry__mutmut_21': x_load_registry__mutmut_21, 
    'x_load_registry__mutmut_22': x_load_registry__mutmut_22, 
    'x_load_registry__mutmut_23': x_load_registry__mutmut_23, 
    'x_load_registry__mutmut_24': x_load_registry__mutmut_24, 
    'x_load_registry__mutmut_25': x_load_registry__mutmut_25, 
    'x_load_registry__mutmut_26': x_load_registry__mutmut_26, 
    'x_load_registry__mutmut_27': x_load_registry__mutmut_27, 
    'x_load_registry__mutmut_28': x_load_registry__mutmut_28, 
    'x_load_registry__mutmut_29': x_load_registry__mutmut_29, 
    'x_load_registry__mutmut_30': x_load_registry__mutmut_30, 
    'x_load_registry__mutmut_31': x_load_registry__mutmut_31, 
    'x_load_registry__mutmut_32': x_load_registry__mutmut_32, 
    'x_load_registry__mutmut_33': x_load_registry__mutmut_33, 
    'x_load_registry__mutmut_34': x_load_registry__mutmut_34, 
    'x_load_registry__mutmut_35': x_load_registry__mutmut_35, 
    'x_load_registry__mutmut_36': x_load_registry__mutmut_36, 
    'x_load_registry__mutmut_37': x_load_registry__mutmut_37, 
    'x_load_registry__mutmut_38': x_load_registry__mutmut_38, 
    'x_load_registry__mutmut_39': x_load_registry__mutmut_39, 
    'x_load_registry__mutmut_40': x_load_registry__mutmut_40, 
    'x_load_registry__mutmut_41': x_load_registry__mutmut_41, 
    'x_load_registry__mutmut_42': x_load_registry__mutmut_42, 
    'x_load_registry__mutmut_43': x_load_registry__mutmut_43, 
    'x_load_registry__mutmut_44': x_load_registry__mutmut_44, 
    'x_load_registry__mutmut_45': x_load_registry__mutmut_45, 
    'x_load_registry__mutmut_46': x_load_registry__mutmut_46, 
    'x_load_registry__mutmut_47': x_load_registry__mutmut_47, 
    'x_load_registry__mutmut_48': x_load_registry__mutmut_48, 
    'x_load_registry__mutmut_49': x_load_registry__mutmut_49, 
    'x_load_registry__mutmut_50': x_load_registry__mutmut_50, 
    'x_load_registry__mutmut_51': x_load_registry__mutmut_51, 
    'x_load_registry__mutmut_52': x_load_registry__mutmut_52, 
    'x_load_registry__mutmut_53': x_load_registry__mutmut_53, 
    'x_load_registry__mutmut_54': x_load_registry__mutmut_54, 
    'x_load_registry__mutmut_55': x_load_registry__mutmut_55, 
    'x_load_registry__mutmut_56': x_load_registry__mutmut_56, 
    'x_load_registry__mutmut_57': x_load_registry__mutmut_57, 
    'x_load_registry__mutmut_58': x_load_registry__mutmut_58, 
    'x_load_registry__mutmut_59': x_load_registry__mutmut_59, 
    'x_load_registry__mutmut_60': x_load_registry__mutmut_60, 
    'x_load_registry__mutmut_61': x_load_registry__mutmut_61, 
    'x_load_registry__mutmut_62': x_load_registry__mutmut_62, 
    'x_load_registry__mutmut_63': x_load_registry__mutmut_63, 
    'x_load_registry__mutmut_64': x_load_registry__mutmut_64, 
    'x_load_registry__mutmut_65': x_load_registry__mutmut_65, 
    'x_load_registry__mutmut_66': x_load_registry__mutmut_66, 
    'x_load_registry__mutmut_67': x_load_registry__mutmut_67, 
    'x_load_registry__mutmut_68': x_load_registry__mutmut_68, 
    'x_load_registry__mutmut_69': x_load_registry__mutmut_69, 
    'x_load_registry__mutmut_70': x_load_registry__mutmut_70, 
    'x_load_registry__mutmut_71': x_load_registry__mutmut_71, 
    'x_load_registry__mutmut_72': x_load_registry__mutmut_72, 
    'x_load_registry__mutmut_73': x_load_registry__mutmut_73
}
x_load_registry__mutmut_orig.__name__ = 'x_load_registry'


def _parse_law_file(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    args = [law_file, title_map, summary_map]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__parse_law_file__mutmut_orig, x__parse_law_file__mutmut_mutants, args, kwargs, None)


def x__parse_law_file__mutmut_orig(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding="utf-8")
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith("---"):
        return
    end = content.find("\n---", 3)
    if end == -1:
        return
    frontmatter_text = content[3:end]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("laws") or []:
        if not isinstance(law_entry, dict):
            continue
        law_id = law_entry.get("id")
        if not law_id:
            continue
        if "title" in law_entry:
            title_map[law_id] = law_entry["title"]
        if "summary" in law_entry:
            summary_map[law_id] = law_entry["summary"]


def x__parse_law_file__mutmut_1(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = None
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith("---"):
        return
    end = content.find("\n---", 3)
    if end == -1:
        return
    frontmatter_text = content[3:end]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("laws") or []:
        if not isinstance(law_entry, dict):
            continue
        law_id = law_entry.get("id")
        if not law_id:
            continue
        if "title" in law_entry:
            title_map[law_id] = law_entry["title"]
        if "summary" in law_entry:
            summary_map[law_id] = law_entry["summary"]


def x__parse_law_file__mutmut_2(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding=None)
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith("---"):
        return
    end = content.find("\n---", 3)
    if end == -1:
        return
    frontmatter_text = content[3:end]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("laws") or []:
        if not isinstance(law_entry, dict):
            continue
        law_id = law_entry.get("id")
        if not law_id:
            continue
        if "title" in law_entry:
            title_map[law_id] = law_entry["title"]
        if "summary" in law_entry:
            summary_map[law_id] = law_entry["summary"]


def x__parse_law_file__mutmut_3(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding="XXutf-8XX")
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith("---"):
        return
    end = content.find("\n---", 3)
    if end == -1:
        return
    frontmatter_text = content[3:end]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("laws") or []:
        if not isinstance(law_entry, dict):
            continue
        law_id = law_entry.get("id")
        if not law_id:
            continue
        if "title" in law_entry:
            title_map[law_id] = law_entry["title"]
        if "summary" in law_entry:
            summary_map[law_id] = law_entry["summary"]


def x__parse_law_file__mutmut_4(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding="UTF-8")
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith("---"):
        return
    end = content.find("\n---", 3)
    if end == -1:
        return
    frontmatter_text = content[3:end]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("laws") or []:
        if not isinstance(law_entry, dict):
            continue
        law_id = law_entry.get("id")
        if not law_id:
            continue
        if "title" in law_entry:
            title_map[law_id] = law_entry["title"]
        if "summary" in law_entry:
            summary_map[law_id] = law_entry["summary"]


def x__parse_law_file__mutmut_5(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding="utf-8")
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if content.startswith("---"):
        return
    end = content.find("\n---", 3)
    if end == -1:
        return
    frontmatter_text = content[3:end]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("laws") or []:
        if not isinstance(law_entry, dict):
            continue
        law_id = law_entry.get("id")
        if not law_id:
            continue
        if "title" in law_entry:
            title_map[law_id] = law_entry["title"]
        if "summary" in law_entry:
            summary_map[law_id] = law_entry["summary"]


def x__parse_law_file__mutmut_6(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding="utf-8")
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith(None):
        return
    end = content.find("\n---", 3)
    if end == -1:
        return
    frontmatter_text = content[3:end]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("laws") or []:
        if not isinstance(law_entry, dict):
            continue
        law_id = law_entry.get("id")
        if not law_id:
            continue
        if "title" in law_entry:
            title_map[law_id] = law_entry["title"]
        if "summary" in law_entry:
            summary_map[law_id] = law_entry["summary"]


def x__parse_law_file__mutmut_7(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding="utf-8")
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith("XX---XX"):
        return
    end = content.find("\n---", 3)
    if end == -1:
        return
    frontmatter_text = content[3:end]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("laws") or []:
        if not isinstance(law_entry, dict):
            continue
        law_id = law_entry.get("id")
        if not law_id:
            continue
        if "title" in law_entry:
            title_map[law_id] = law_entry["title"]
        if "summary" in law_entry:
            summary_map[law_id] = law_entry["summary"]


def x__parse_law_file__mutmut_8(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding="utf-8")
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith("---"):
        return
    end = None
    if end == -1:
        return
    frontmatter_text = content[3:end]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("laws") or []:
        if not isinstance(law_entry, dict):
            continue
        law_id = law_entry.get("id")
        if not law_id:
            continue
        if "title" in law_entry:
            title_map[law_id] = law_entry["title"]
        if "summary" in law_entry:
            summary_map[law_id] = law_entry["summary"]


def x__parse_law_file__mutmut_9(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding="utf-8")
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith("---"):
        return
    end = content.find(None, 3)
    if end == -1:
        return
    frontmatter_text = content[3:end]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("laws") or []:
        if not isinstance(law_entry, dict):
            continue
        law_id = law_entry.get("id")
        if not law_id:
            continue
        if "title" in law_entry:
            title_map[law_id] = law_entry["title"]
        if "summary" in law_entry:
            summary_map[law_id] = law_entry["summary"]


def x__parse_law_file__mutmut_10(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding="utf-8")
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith("---"):
        return
    end = content.find("\n---", None)
    if end == -1:
        return
    frontmatter_text = content[3:end]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("laws") or []:
        if not isinstance(law_entry, dict):
            continue
        law_id = law_entry.get("id")
        if not law_id:
            continue
        if "title" in law_entry:
            title_map[law_id] = law_entry["title"]
        if "summary" in law_entry:
            summary_map[law_id] = law_entry["summary"]


def x__parse_law_file__mutmut_11(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding="utf-8")
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith("---"):
        return
    end = content.find(3)
    if end == -1:
        return
    frontmatter_text = content[3:end]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("laws") or []:
        if not isinstance(law_entry, dict):
            continue
        law_id = law_entry.get("id")
        if not law_id:
            continue
        if "title" in law_entry:
            title_map[law_id] = law_entry["title"]
        if "summary" in law_entry:
            summary_map[law_id] = law_entry["summary"]


def x__parse_law_file__mutmut_12(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding="utf-8")
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith("---"):
        return
    end = content.find("\n---", )
    if end == -1:
        return
    frontmatter_text = content[3:end]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("laws") or []:
        if not isinstance(law_entry, dict):
            continue
        law_id = law_entry.get("id")
        if not law_id:
            continue
        if "title" in law_entry:
            title_map[law_id] = law_entry["title"]
        if "summary" in law_entry:
            summary_map[law_id] = law_entry["summary"]


def x__parse_law_file__mutmut_13(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding="utf-8")
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith("---"):
        return
    end = content.rfind("\n---", 3)
    if end == -1:
        return
    frontmatter_text = content[3:end]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("laws") or []:
        if not isinstance(law_entry, dict):
            continue
        law_id = law_entry.get("id")
        if not law_id:
            continue
        if "title" in law_entry:
            title_map[law_id] = law_entry["title"]
        if "summary" in law_entry:
            summary_map[law_id] = law_entry["summary"]


def x__parse_law_file__mutmut_14(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding="utf-8")
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith("---"):
        return
    end = content.find("XX\n---XX", 3)
    if end == -1:
        return
    frontmatter_text = content[3:end]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("laws") or []:
        if not isinstance(law_entry, dict):
            continue
        law_id = law_entry.get("id")
        if not law_id:
            continue
        if "title" in law_entry:
            title_map[law_id] = law_entry["title"]
        if "summary" in law_entry:
            summary_map[law_id] = law_entry["summary"]


def x__parse_law_file__mutmut_15(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding="utf-8")
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith("---"):
        return
    end = content.find("\n---", 4)
    if end == -1:
        return
    frontmatter_text = content[3:end]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("laws") or []:
        if not isinstance(law_entry, dict):
            continue
        law_id = law_entry.get("id")
        if not law_id:
            continue
        if "title" in law_entry:
            title_map[law_id] = law_entry["title"]
        if "summary" in law_entry:
            summary_map[law_id] = law_entry["summary"]


def x__parse_law_file__mutmut_16(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding="utf-8")
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith("---"):
        return
    end = content.find("\n---", 3)
    if end != -1:
        return
    frontmatter_text = content[3:end]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("laws") or []:
        if not isinstance(law_entry, dict):
            continue
        law_id = law_entry.get("id")
        if not law_id:
            continue
        if "title" in law_entry:
            title_map[law_id] = law_entry["title"]
        if "summary" in law_entry:
            summary_map[law_id] = law_entry["summary"]


def x__parse_law_file__mutmut_17(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding="utf-8")
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith("---"):
        return
    end = content.find("\n---", 3)
    if end == +1:
        return
    frontmatter_text = content[3:end]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("laws") or []:
        if not isinstance(law_entry, dict):
            continue
        law_id = law_entry.get("id")
        if not law_id:
            continue
        if "title" in law_entry:
            title_map[law_id] = law_entry["title"]
        if "summary" in law_entry:
            summary_map[law_id] = law_entry["summary"]


def x__parse_law_file__mutmut_18(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding="utf-8")
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith("---"):
        return
    end = content.find("\n---", 3)
    if end == -2:
        return
    frontmatter_text = content[3:end]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("laws") or []:
        if not isinstance(law_entry, dict):
            continue
        law_id = law_entry.get("id")
        if not law_id:
            continue
        if "title" in law_entry:
            title_map[law_id] = law_entry["title"]
        if "summary" in law_entry:
            summary_map[law_id] = law_entry["summary"]


def x__parse_law_file__mutmut_19(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding="utf-8")
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith("---"):
        return
    end = content.find("\n---", 3)
    if end == -1:
        return
    frontmatter_text = None

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("laws") or []:
        if not isinstance(law_entry, dict):
            continue
        law_id = law_entry.get("id")
        if not law_id:
            continue
        if "title" in law_entry:
            title_map[law_id] = law_entry["title"]
        if "summary" in law_entry:
            summary_map[law_id] = law_entry["summary"]


def x__parse_law_file__mutmut_20(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding="utf-8")
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith("---"):
        return
    end = content.find("\n---", 3)
    if end == -1:
        return
    frontmatter_text = content[4:end]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("laws") or []:
        if not isinstance(law_entry, dict):
            continue
        law_id = law_entry.get("id")
        if not law_id:
            continue
        if "title" in law_entry:
            title_map[law_id] = law_entry["title"]
        if "summary" in law_entry:
            summary_map[law_id] = law_entry["summary"]


def x__parse_law_file__mutmut_21(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding="utf-8")
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith("---"):
        return
    end = content.find("\n---", 3)
    if end == -1:
        return
    frontmatter_text = content[3:end]

    try:
        frontmatter = None
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("laws") or []:
        if not isinstance(law_entry, dict):
            continue
        law_id = law_entry.get("id")
        if not law_id:
            continue
        if "title" in law_entry:
            title_map[law_id] = law_entry["title"]
        if "summary" in law_entry:
            summary_map[law_id] = law_entry["summary"]


def x__parse_law_file__mutmut_22(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding="utf-8")
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith("---"):
        return
    end = content.find("\n---", 3)
    if end == -1:
        return
    frontmatter_text = content[3:end]

    try:
        frontmatter = yaml.safe_load(None)
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("laws") or []:
        if not isinstance(law_entry, dict):
            continue
        law_id = law_entry.get("id")
        if not law_id:
            continue
        if "title" in law_entry:
            title_map[law_id] = law_entry["title"]
        if "summary" in law_entry:
            summary_map[law_id] = law_entry["summary"]


def x__parse_law_file__mutmut_23(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding="utf-8")
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith("---"):
        return
    end = content.find("\n---", 3)
    if end == -1:
        return
    frontmatter_text = content[3:end]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return

    if isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("laws") or []:
        if not isinstance(law_entry, dict):
            continue
        law_id = law_entry.get("id")
        if not law_id:
            continue
        if "title" in law_entry:
            title_map[law_id] = law_entry["title"]
        if "summary" in law_entry:
            summary_map[law_id] = law_entry["summary"]


def x__parse_law_file__mutmut_24(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding="utf-8")
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith("---"):
        return
    end = content.find("\n---", 3)
    if end == -1:
        return
    frontmatter_text = content[3:end]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("laws") and []:
        if not isinstance(law_entry, dict):
            continue
        law_id = law_entry.get("id")
        if not law_id:
            continue
        if "title" in law_entry:
            title_map[law_id] = law_entry["title"]
        if "summary" in law_entry:
            summary_map[law_id] = law_entry["summary"]


def x__parse_law_file__mutmut_25(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding="utf-8")
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith("---"):
        return
    end = content.find("\n---", 3)
    if end == -1:
        return
    frontmatter_text = content[3:end]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get(None) or []:
        if not isinstance(law_entry, dict):
            continue
        law_id = law_entry.get("id")
        if not law_id:
            continue
        if "title" in law_entry:
            title_map[law_id] = law_entry["title"]
        if "summary" in law_entry:
            summary_map[law_id] = law_entry["summary"]


def x__parse_law_file__mutmut_26(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding="utf-8")
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith("---"):
        return
    end = content.find("\n---", 3)
    if end == -1:
        return
    frontmatter_text = content[3:end]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("XXlawsXX") or []:
        if not isinstance(law_entry, dict):
            continue
        law_id = law_entry.get("id")
        if not law_id:
            continue
        if "title" in law_entry:
            title_map[law_id] = law_entry["title"]
        if "summary" in law_entry:
            summary_map[law_id] = law_entry["summary"]


def x__parse_law_file__mutmut_27(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding="utf-8")
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith("---"):
        return
    end = content.find("\n---", 3)
    if end == -1:
        return
    frontmatter_text = content[3:end]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("LAWS") or []:
        if not isinstance(law_entry, dict):
            continue
        law_id = law_entry.get("id")
        if not law_id:
            continue
        if "title" in law_entry:
            title_map[law_id] = law_entry["title"]
        if "summary" in law_entry:
            summary_map[law_id] = law_entry["summary"]


def x__parse_law_file__mutmut_28(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding="utf-8")
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith("---"):
        return
    end = content.find("\n---", 3)
    if end == -1:
        return
    frontmatter_text = content[3:end]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("laws") or []:
        if isinstance(law_entry, dict):
            continue
        law_id = law_entry.get("id")
        if not law_id:
            continue
        if "title" in law_entry:
            title_map[law_id] = law_entry["title"]
        if "summary" in law_entry:
            summary_map[law_id] = law_entry["summary"]


def x__parse_law_file__mutmut_29(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding="utf-8")
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith("---"):
        return
    end = content.find("\n---", 3)
    if end == -1:
        return
    frontmatter_text = content[3:end]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("laws") or []:
        if not isinstance(law_entry, dict):
            break
        law_id = law_entry.get("id")
        if not law_id:
            continue
        if "title" in law_entry:
            title_map[law_id] = law_entry["title"]
        if "summary" in law_entry:
            summary_map[law_id] = law_entry["summary"]


def x__parse_law_file__mutmut_30(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding="utf-8")
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith("---"):
        return
    end = content.find("\n---", 3)
    if end == -1:
        return
    frontmatter_text = content[3:end]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("laws") or []:
        if not isinstance(law_entry, dict):
            continue
        law_id = None
        if not law_id:
            continue
        if "title" in law_entry:
            title_map[law_id] = law_entry["title"]
        if "summary" in law_entry:
            summary_map[law_id] = law_entry["summary"]


def x__parse_law_file__mutmut_31(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding="utf-8")
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith("---"):
        return
    end = content.find("\n---", 3)
    if end == -1:
        return
    frontmatter_text = content[3:end]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("laws") or []:
        if not isinstance(law_entry, dict):
            continue
        law_id = law_entry.get(None)
        if not law_id:
            continue
        if "title" in law_entry:
            title_map[law_id] = law_entry["title"]
        if "summary" in law_entry:
            summary_map[law_id] = law_entry["summary"]


def x__parse_law_file__mutmut_32(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding="utf-8")
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith("---"):
        return
    end = content.find("\n---", 3)
    if end == -1:
        return
    frontmatter_text = content[3:end]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("laws") or []:
        if not isinstance(law_entry, dict):
            continue
        law_id = law_entry.get("XXidXX")
        if not law_id:
            continue
        if "title" in law_entry:
            title_map[law_id] = law_entry["title"]
        if "summary" in law_entry:
            summary_map[law_id] = law_entry["summary"]


def x__parse_law_file__mutmut_33(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding="utf-8")
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith("---"):
        return
    end = content.find("\n---", 3)
    if end == -1:
        return
    frontmatter_text = content[3:end]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("laws") or []:
        if not isinstance(law_entry, dict):
            continue
        law_id = law_entry.get("ID")
        if not law_id:
            continue
        if "title" in law_entry:
            title_map[law_id] = law_entry["title"]
        if "summary" in law_entry:
            summary_map[law_id] = law_entry["summary"]


def x__parse_law_file__mutmut_34(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding="utf-8")
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith("---"):
        return
    end = content.find("\n---", 3)
    if end == -1:
        return
    frontmatter_text = content[3:end]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("laws") or []:
        if not isinstance(law_entry, dict):
            continue
        law_id = law_entry.get("id")
        if law_id:
            continue
        if "title" in law_entry:
            title_map[law_id] = law_entry["title"]
        if "summary" in law_entry:
            summary_map[law_id] = law_entry["summary"]


def x__parse_law_file__mutmut_35(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding="utf-8")
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith("---"):
        return
    end = content.find("\n---", 3)
    if end == -1:
        return
    frontmatter_text = content[3:end]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("laws") or []:
        if not isinstance(law_entry, dict):
            continue
        law_id = law_entry.get("id")
        if not law_id:
            break
        if "title" in law_entry:
            title_map[law_id] = law_entry["title"]
        if "summary" in law_entry:
            summary_map[law_id] = law_entry["summary"]


def x__parse_law_file__mutmut_36(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding="utf-8")
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith("---"):
        return
    end = content.find("\n---", 3)
    if end == -1:
        return
    frontmatter_text = content[3:end]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("laws") or []:
        if not isinstance(law_entry, dict):
            continue
        law_id = law_entry.get("id")
        if not law_id:
            continue
        if "XXtitleXX" in law_entry:
            title_map[law_id] = law_entry["title"]
        if "summary" in law_entry:
            summary_map[law_id] = law_entry["summary"]


def x__parse_law_file__mutmut_37(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding="utf-8")
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith("---"):
        return
    end = content.find("\n---", 3)
    if end == -1:
        return
    frontmatter_text = content[3:end]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("laws") or []:
        if not isinstance(law_entry, dict):
            continue
        law_id = law_entry.get("id")
        if not law_id:
            continue
        if "TITLE" in law_entry:
            title_map[law_id] = law_entry["title"]
        if "summary" in law_entry:
            summary_map[law_id] = law_entry["summary"]


def x__parse_law_file__mutmut_38(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding="utf-8")
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith("---"):
        return
    end = content.find("\n---", 3)
    if end == -1:
        return
    frontmatter_text = content[3:end]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("laws") or []:
        if not isinstance(law_entry, dict):
            continue
        law_id = law_entry.get("id")
        if not law_id:
            continue
        if "title" not in law_entry:
            title_map[law_id] = law_entry["title"]
        if "summary" in law_entry:
            summary_map[law_id] = law_entry["summary"]


def x__parse_law_file__mutmut_39(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding="utf-8")
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith("---"):
        return
    end = content.find("\n---", 3)
    if end == -1:
        return
    frontmatter_text = content[3:end]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("laws") or []:
        if not isinstance(law_entry, dict):
            continue
        law_id = law_entry.get("id")
        if not law_id:
            continue
        if "title" in law_entry:
            title_map[law_id] = None
        if "summary" in law_entry:
            summary_map[law_id] = law_entry["summary"]


def x__parse_law_file__mutmut_40(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding="utf-8")
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith("---"):
        return
    end = content.find("\n---", 3)
    if end == -1:
        return
    frontmatter_text = content[3:end]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("laws") or []:
        if not isinstance(law_entry, dict):
            continue
        law_id = law_entry.get("id")
        if not law_id:
            continue
        if "title" in law_entry:
            title_map[law_id] = law_entry["XXtitleXX"]
        if "summary" in law_entry:
            summary_map[law_id] = law_entry["summary"]


def x__parse_law_file__mutmut_41(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding="utf-8")
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith("---"):
        return
    end = content.find("\n---", 3)
    if end == -1:
        return
    frontmatter_text = content[3:end]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("laws") or []:
        if not isinstance(law_entry, dict):
            continue
        law_id = law_entry.get("id")
        if not law_id:
            continue
        if "title" in law_entry:
            title_map[law_id] = law_entry["TITLE"]
        if "summary" in law_entry:
            summary_map[law_id] = law_entry["summary"]


def x__parse_law_file__mutmut_42(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding="utf-8")
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith("---"):
        return
    end = content.find("\n---", 3)
    if end == -1:
        return
    frontmatter_text = content[3:end]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("laws") or []:
        if not isinstance(law_entry, dict):
            continue
        law_id = law_entry.get("id")
        if not law_id:
            continue
        if "title" in law_entry:
            title_map[law_id] = law_entry["title"]
        if "XXsummaryXX" in law_entry:
            summary_map[law_id] = law_entry["summary"]


def x__parse_law_file__mutmut_43(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding="utf-8")
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith("---"):
        return
    end = content.find("\n---", 3)
    if end == -1:
        return
    frontmatter_text = content[3:end]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("laws") or []:
        if not isinstance(law_entry, dict):
            continue
        law_id = law_entry.get("id")
        if not law_id:
            continue
        if "title" in law_entry:
            title_map[law_id] = law_entry["title"]
        if "SUMMARY" in law_entry:
            summary_map[law_id] = law_entry["summary"]


def x__parse_law_file__mutmut_44(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding="utf-8")
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith("---"):
        return
    end = content.find("\n---", 3)
    if end == -1:
        return
    frontmatter_text = content[3:end]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("laws") or []:
        if not isinstance(law_entry, dict):
            continue
        law_id = law_entry.get("id")
        if not law_id:
            continue
        if "title" in law_entry:
            title_map[law_id] = law_entry["title"]
        if "summary" not in law_entry:
            summary_map[law_id] = law_entry["summary"]


def x__parse_law_file__mutmut_45(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding="utf-8")
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith("---"):
        return
    end = content.find("\n---", 3)
    if end == -1:
        return
    frontmatter_text = content[3:end]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("laws") or []:
        if not isinstance(law_entry, dict):
            continue
        law_id = law_entry.get("id")
        if not law_id:
            continue
        if "title" in law_entry:
            title_map[law_id] = law_entry["title"]
        if "summary" in law_entry:
            summary_map[law_id] = None


def x__parse_law_file__mutmut_46(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding="utf-8")
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith("---"):
        return
    end = content.find("\n---", 3)
    if end == -1:
        return
    frontmatter_text = content[3:end]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("laws") or []:
        if not isinstance(law_entry, dict):
            continue
        law_id = law_entry.get("id")
        if not law_id:
            continue
        if "title" in law_entry:
            title_map[law_id] = law_entry["title"]
        if "summary" in law_entry:
            summary_map[law_id] = law_entry["XXsummaryXX"]


def x__parse_law_file__mutmut_47(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding="utf-8")
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith("---"):
        return
    end = content.find("\n---", 3)
    if end == -1:
        return
    frontmatter_text = content[3:end]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("laws") or []:
        if not isinstance(law_entry, dict):
            continue
        law_id = law_entry.get("id")
        if not law_id:
            continue
        if "title" in law_entry:
            title_map[law_id] = law_entry["title"]
        if "summary" in law_entry:
            summary_map[law_id] = law_entry["SUMMARY"]

x__parse_law_file__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__parse_law_file__mutmut_1': x__parse_law_file__mutmut_1, 
    'x__parse_law_file__mutmut_2': x__parse_law_file__mutmut_2, 
    'x__parse_law_file__mutmut_3': x__parse_law_file__mutmut_3, 
    'x__parse_law_file__mutmut_4': x__parse_law_file__mutmut_4, 
    'x__parse_law_file__mutmut_5': x__parse_law_file__mutmut_5, 
    'x__parse_law_file__mutmut_6': x__parse_law_file__mutmut_6, 
    'x__parse_law_file__mutmut_7': x__parse_law_file__mutmut_7, 
    'x__parse_law_file__mutmut_8': x__parse_law_file__mutmut_8, 
    'x__parse_law_file__mutmut_9': x__parse_law_file__mutmut_9, 
    'x__parse_law_file__mutmut_10': x__parse_law_file__mutmut_10, 
    'x__parse_law_file__mutmut_11': x__parse_law_file__mutmut_11, 
    'x__parse_law_file__mutmut_12': x__parse_law_file__mutmut_12, 
    'x__parse_law_file__mutmut_13': x__parse_law_file__mutmut_13, 
    'x__parse_law_file__mutmut_14': x__parse_law_file__mutmut_14, 
    'x__parse_law_file__mutmut_15': x__parse_law_file__mutmut_15, 
    'x__parse_law_file__mutmut_16': x__parse_law_file__mutmut_16, 
    'x__parse_law_file__mutmut_17': x__parse_law_file__mutmut_17, 
    'x__parse_law_file__mutmut_18': x__parse_law_file__mutmut_18, 
    'x__parse_law_file__mutmut_19': x__parse_law_file__mutmut_19, 
    'x__parse_law_file__mutmut_20': x__parse_law_file__mutmut_20, 
    'x__parse_law_file__mutmut_21': x__parse_law_file__mutmut_21, 
    'x__parse_law_file__mutmut_22': x__parse_law_file__mutmut_22, 
    'x__parse_law_file__mutmut_23': x__parse_law_file__mutmut_23, 
    'x__parse_law_file__mutmut_24': x__parse_law_file__mutmut_24, 
    'x__parse_law_file__mutmut_25': x__parse_law_file__mutmut_25, 
    'x__parse_law_file__mutmut_26': x__parse_law_file__mutmut_26, 
    'x__parse_law_file__mutmut_27': x__parse_law_file__mutmut_27, 
    'x__parse_law_file__mutmut_28': x__parse_law_file__mutmut_28, 
    'x__parse_law_file__mutmut_29': x__parse_law_file__mutmut_29, 
    'x__parse_law_file__mutmut_30': x__parse_law_file__mutmut_30, 
    'x__parse_law_file__mutmut_31': x__parse_law_file__mutmut_31, 
    'x__parse_law_file__mutmut_32': x__parse_law_file__mutmut_32, 
    'x__parse_law_file__mutmut_33': x__parse_law_file__mutmut_33, 
    'x__parse_law_file__mutmut_34': x__parse_law_file__mutmut_34, 
    'x__parse_law_file__mutmut_35': x__parse_law_file__mutmut_35, 
    'x__parse_law_file__mutmut_36': x__parse_law_file__mutmut_36, 
    'x__parse_law_file__mutmut_37': x__parse_law_file__mutmut_37, 
    'x__parse_law_file__mutmut_38': x__parse_law_file__mutmut_38, 
    'x__parse_law_file__mutmut_39': x__parse_law_file__mutmut_39, 
    'x__parse_law_file__mutmut_40': x__parse_law_file__mutmut_40, 
    'x__parse_law_file__mutmut_41': x__parse_law_file__mutmut_41, 
    'x__parse_law_file__mutmut_42': x__parse_law_file__mutmut_42, 
    'x__parse_law_file__mutmut_43': x__parse_law_file__mutmut_43, 
    'x__parse_law_file__mutmut_44': x__parse_law_file__mutmut_44, 
    'x__parse_law_file__mutmut_45': x__parse_law_file__mutmut_45, 
    'x__parse_law_file__mutmut_46': x__parse_law_file__mutmut_46, 
    'x__parse_law_file__mutmut_47': x__parse_law_file__mutmut_47
}
x__parse_law_file__mutmut_orig.__name__ = 'x__parse_law_file'
