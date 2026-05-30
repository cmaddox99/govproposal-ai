"""Law-ID extraction for the Hangar constitution RAG evaluator.

Valid law-ID prefixes are derived from ``laws/*/_domain.yaml`` — the
constitution's authoritative domain registry. Extracting regexes this way
keeps the evaluator in lock-step with whatever domains Hangar declares, and
prevents license identifiers (e.g. ``BSL-1.0``) or other shape-matching
tokens from being miscounted as broken law references.
"""
from __future__ import annotations

import re
from pathlib import Path

try:
    import yaml
except ImportError:
    raise SystemExit("PyYAML is required: pip install pyyaml")


def load_domain_prefixes(constitution_path: Path) -> set[str]:
    """Load valid law-ID prefixes from ``laws/*/_domain.yaml`` registries.

    Each domain directory under ``laws/`` is expected to declare a ``prefix``
    field (e.g. ``ENG``, ``PRD``, ``BUS``). Missing, unparseable, or
    non-string prefix fields are skipped silently so a partially-broken
    domain registry still yields a usable (if narrower) set.
    """
    prefixes: set[str] = set()
    laws_dir = constitution_path / "laws"
    if not laws_dir.exists():
        return prefixes
    for domain_yaml in sorted(laws_dir.glob("*/_domain.yaml")):
        try:
            data = yaml.safe_load(domain_yaml.read_text(encoding="utf-8")) or {}
        except Exception:
            continue
        prefix = data.get("prefix")
        if isinstance(prefix, str) and prefix.isalpha() and prefix.isupper():
            prefixes.add(prefix)
    return prefixes


def build_law_id_regex(constitution_path: Path) -> re.Pattern[str]:
    """Compile a law-ID regex restricted to prefixes registered in the constitution.

    The regex shape is ``\\b(<PREFIX>-<article>.<section>)\\b`` where ``<PREFIX>``
    is a domain prefix from ``_domain.yaml``. If no prefixes can be loaded
    (empty or missing ``laws/`` dir), the returned pattern matches nothing —
    callers see zero law IDs instead of accidentally accepting arbitrary
    uppercase-hyphen-number tokens as valid.
    """
    prefixes = load_domain_prefixes(constitution_path)
    if not prefixes:
        return re.compile(r"(?!x)x")  # never matches
    alt = "|".join(sorted(prefixes))
    return re.compile(rf"\b((?:{alt})-\d+\.\d+)\b")


def extract_law_ids(text: str, constitution_path: Path) -> list[str]:
    """Return every law-ID in *text* whose prefix is registered in *constitution_path*.

    Convenience wrapper over :func:`build_law_id_regex`. Callers that process
    many strings should cache the compiled pattern themselves.
    """
    return build_law_id_regex(constitution_path).findall(text)
