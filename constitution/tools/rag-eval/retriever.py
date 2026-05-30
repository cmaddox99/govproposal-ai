"""
RAG retriever — simulates retrieval from constitution content.
Uses keyword matching + law ID exact matching (no embeddings — deterministic for CI).
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    raise SystemExit("PyYAML is required: pip install pyyaml")

from law_ids import build_law_id_regex


@dataclass
class RetrievalResult:
    content_type: str        # 'law', 'skill', 'avatar'
    id: str                  # law ID, skill file, or avatar id
    file_path: str
    score: float
    matched_law_ids: list[str]   # law IDs from query that matched this entry
    matched_keywords: list[str]
    indexed_law_ids: list[str] = None   # all law IDs indexed for this entry

    def __post_init__(self):
        if self.indexed_law_ids is None:
            self.indexed_law_ids = []


def _tokenize(text: str) -> list[str]:
    """Lower-case word tokens, stripping punctuation."""
    return re.findall(r'[a-z][a-z0-9]*', text.lower())


def _extract_law_ids(law_id_re: "re.Pattern[str]", text: str) -> list[str]:
    return law_id_re.findall(text)


def _normalize_law_id(law_id_re: "re.Pattern[str]", entry: Any) -> str | None:
    """Extract plain law ID string from either a string or a YAML dict entry."""
    if isinstance(entry, str):
        ids = law_id_re.findall(entry)
        return ids[0] if ids else None
    if isinstance(entry, dict):
        raw = entry.get("id", "")
        ids = law_id_re.findall(str(raw))
        return ids[0] if ids else None
    return None


def _normalize_law_ids(law_id_re: "re.Pattern[str]", entries: list[Any]) -> list[str]:
    """Convert a list of law entries (str or dict) to plain law ID strings."""
    result: list[str] = []
    for e in entries:
        lid = _normalize_law_id(law_id_re, e)
        if lid:
            result.append(lid)
    return result


def _load_yaml_safe(path: Path) -> dict[str, Any]:
    try:
        with path.open(encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except Exception:
        return {}


def _extract_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Extract YAML frontmatter (--- ... ---) and body from a markdown file."""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            fm_text = text[3:end].strip()
            body = text[end + 4:].strip()
            try:
                fm = yaml.safe_load(fm_text) or {}
            except Exception:
                fm = {}
            return fm, body
    return {}, text


class ConstitutionRetriever:
    def __init__(self, constitution_path: Path):
        self.constitution_path = constitution_path
        self._law_id_re = build_law_id_regex(constitution_path)
        self._index: list[dict] = []
        self._build_index()

    # ------------------------------------------------------------------
    # Index building
    # ------------------------------------------------------------------

    def _build_index(self) -> None:
        """Index all laws, skills, and avatars."""
        self._index_laws()
        self._index_skills()
        self._index_avatars()

    def _index_laws(self) -> None:
        """Scan laws/**/*.md, extract frontmatter law IDs and body text."""
        laws_dir = self.constitution_path / "laws"
        if not laws_dir.exists():
            return
        for md_file in sorted(laws_dir.rglob("*.md")):
            raw = md_file.read_text(encoding="utf-8", errors="replace")
            fm, body = _extract_frontmatter(raw)
            law_ids = [str(law.get("id", "")) for law in fm.get("laws", []) if law.get("id")]
            if not law_ids:
                law_ids = _extract_law_ids(self._law_id_re, raw)
            tokens = _tokenize(fm.get("title", "") + " " + body)
            trigger_phrases: list[str] = []
            # extract section headings as trigger phrases
            for heading in re.findall(r'^#{1,3}\s+(.+)$', body, re.MULTILINE):
                trigger_phrases.append(heading.lower())
            self._index.append({
                "content_type": "law",
                "id": md_file.stem,
                "file_path": str(md_file.relative_to(self.constitution_path)),
                "law_ids": law_ids,
                "tokens": set(tokens),
                "trigger_phrases": trigger_phrases,
                "domain": fm.get("domain", ""),
                "title": fm.get("title", ""),
            })

    def _index_skills(self) -> None:
        """Scan agent-skills/**/*.md, extract trigger phrases and law citations."""
        skills_root = self.constitution_path / "agent-skills" / "skills-by-domain"
        if not skills_root.exists():
            return
        for domain_dir in sorted(skills_root.iterdir()):
            if not domain_dir.is_dir():
                continue
            index_path = domain_dir / "index.yaml"
            if index_path.exists():
                idx = _load_yaml_safe(index_path)
                for skill in idx.get("skills", []):
                    fname = skill.get("file", "")
                    skill_path = domain_dir / fname
                    skill_id = fname
                    triggers: list[str] = [t.lower() for t in skill.get("triggers", [])]
                    law_ids: list[str] = [str(l) for l in skill.get("laws", [])]

                    # also load file body for extra tokens
                    body_tokens: set[str] = set()
                    if skill_path.exists():
                        body = skill_path.read_text(encoding="utf-8", errors="replace")
                        body_tokens = set(_tokenize(body))
                        law_ids += _extract_law_ids(self._law_id_re, body)

                    self._index.append({
                        "content_type": "skill",
                        "id": skill_id,
                        "file_path": str((domain_dir / fname).relative_to(self.constitution_path)),
                        "law_ids": list(set(law_ids)),
                        "tokens": body_tokens | set(_tokenize(" ".join(triggers))),
                        "trigger_phrases": triggers,
                        "name": skill.get("name", fname),
                        "domain": domain_dir.name,
                    })
            else:
                # index any md files found directly
                for md_file in sorted(domain_dir.glob("*.md")):
                    body = md_file.read_text(encoding="utf-8", errors="replace")
                    law_ids = _extract_law_ids(self._law_id_re, body)
                    self._index.append({
                        "content_type": "skill",
                        "id": md_file.name,
                        "file_path": str(md_file.relative_to(self.constitution_path)),
                        "law_ids": list(set(law_ids)),
                        "tokens": set(_tokenize(body)),
                        "trigger_phrases": [],
                        "name": md_file.stem,
                        "domain": domain_dir.name,
                    })

    def _load_rag_index_entries(self) -> dict[str, dict]:
        """
        Load AVATAR-RAG-INDEX.yaml and return a map of avatar_dir_name → {
            'search_queries': list[str],   # semantic query portion (before ' → ')
            'law_ids': list[str],          # all law IDs found in queries/laws block
        }

        The AVATAR-RAG-INDEX nests avatars under category keys:
            technology_avatars.cpp, product_type_avatars.loyalty-aadvantage, etc.
        This method flattens those into a simple avatar_dir_name → data map so
        _index_avatars() can enrich each avatar entry with its RAG index vocabulary.

        Enriching avatars with RAG search queries gives the keyword retriever access
        to sub-generic C++ vocabulary (e.g., 'std::expected', 'circuit breaker',
        'ASan UBSan') that does not appear in the slim guidance.md or manifest.yaml.
        Without this enrichment, the retriever cannot distinguish C++ avatar queries
        from generic law-file keyword overlap.
        """
        rag_index_path = self.constitution_path / "avatars" / "AVATAR-RAG-INDEX.yaml"
        if not rag_index_path.exists():
            return {}

        raw = _load_yaml_safe(rag_index_path)
        result: dict[str, dict] = {}

        # Category keys that contain avatar sub-dicts
        category_keys = [
            "technology_avatars",
            "product_type_avatars",
            "industry_avatars",
            "avatars",  # fallback flat structure
        ]

        def _extract_avatar(key: str, avatar_data: dict) -> None:
            if not isinstance(avatar_data, dict):
                return
            queries: list[str] = []
            law_ids: list[str] = []
            for q in avatar_data.get("search_queries", []):
                if not isinstance(q, str):
                    continue
                # Strip the routing suffix " → ref-*.md (~Nt)" to get the semantic query
                semantic = q.split("→")[0].strip().lower()
                if semantic:
                    queries.append(semantic)
                law_ids.extend(_extract_law_ids(self._law_id_re, q))
            # Also harvest law IDs from the specializes_laws block (dict of law→desc)
            spec = avatar_data.get("specializes_laws", {})
            if isinstance(spec, dict):
                for law_key in spec.keys():
                    ids = self._law_id_re.findall(str(law_key))
                    law_ids.extend(ids)
            result[key] = {
                "search_queries": queries,
                "law_ids": list(set(law_ids)),
            }

        for cat_key in category_keys:
            cat_block = raw.get(cat_key, {})
            if not isinstance(cat_block, dict):
                continue
            for avatar_key, avatar_data in cat_block.items():
                _extract_avatar(avatar_key, avatar_data)

        return result

    def _index_avatars(self) -> None:
        """Scan avatars/**/guidance.md and manifest.yaml, plus AVATAR-RAG-INDEX.yaml.

        The AVATAR-RAG-INDEX.yaml search queries are loaded as additional trigger
        phrases and law IDs for each avatar entry.  This enriches the keyword retriever
        so that fine-grained law/skill queries (e.g. "C++ circuit breaker ENG-7.2")
        can surface the correct avatar and its associated law IDs even when those
        terms do not appear in the slim guidance.md.
        """
        avatars_dir = self.constitution_path / "avatars"
        if not avatars_dir.exists():
            return

        # Pre-load AVATAR-RAG-INDEX enrichment data (keyed by avatar dir name)
        rag_index_data = self._load_rag_index_entries()

        # walk product-type and technology subdirs
        for category in ("product-type", "technology", "industry"):
            cat_dir = avatars_dir / category
            if not cat_dir.exists():
                continue
            for avatar_dir in sorted(cat_dir.iterdir()):
                if not avatar_dir.is_dir() or avatar_dir.name == "__pycache__":
                    continue
                if avatar_dir.name in ("index.yaml",):
                    continue

                manifest_path = avatar_dir / "manifest.yaml"
                guidance_path = avatar_dir / "guidance.yaml"
                guidance_md = avatar_dir / "guidance.md"

                manifest: dict = _load_yaml_safe(manifest_path) if manifest_path.exists() else {}
                avatar_node = manifest.get("avatar", {})
                avatar_id = avatar_node.get("id", avatar_dir.name)
                avatar_name = avatar_node.get("name", avatar_dir.name)
                law_ids: list[str] = _normalize_law_ids(self._law_id_re, manifest.get("specializes_laws", []))
                if not law_ids:
                    activates = manifest.get("activates", {})
                    if isinstance(activates, dict):
                        law_ids = _normalize_law_ids(self._law_id_re, activates.get("specializes_laws", []))

                # Trigger phrases: dir name (hyphens→spaces) and avatar name
                body_tokens: set[str] = set(_tokenize(avatar_name + " " + avatar_dir.name))
                trigger_phrases: list[str] = [
                    avatar_dir.name.lower(),
                    avatar_dir.name.lower().replace("-", " "),
                    avatar_name.lower(),
                    avatar_name.lower().replace("/", " ").replace("_", " "),
                ]

                # load guidance
                for gp in (guidance_md, guidance_path):
                    if gp.exists():
                        text = gp.read_text(encoding="utf-8", errors="replace")
                        body_tokens |= set(_tokenize(text))
                        law_ids += _extract_law_ids(self._law_id_re, text)
                        break

                # look into manifest for specializes_laws deeper
                spec_laws = _normalize_law_ids(self._law_id_re, manifest.get("specializes_laws", []))
                if not spec_laws and isinstance(manifest.get("activates"), dict):
                    spec_laws = _normalize_law_ids(self._law_id_re, manifest["activates"].get("specializes_laws", []))
                law_ids += spec_laws

                # Enrich from AVATAR-RAG-INDEX: add search query tokens + law IDs
                # Look up by both avatar_dir.name and the avatar id
                for lookup_key in (avatar_dir.name, avatar_id.replace("avatar-technology-", "")
                                   .replace("avatar-product-type-", "").replace("avatar-industry-", "")):
                    rag_data = rag_index_data.get(lookup_key, {})
                    if rag_data:
                        # Add semantic portion of each search query as tokens + trigger phrase
                        for semantic_q in rag_data.get("search_queries", []):
                            body_tokens |= set(_tokenize(semantic_q))
                            trigger_phrases.append(semantic_q)
                        # Add all law IDs found in the RAG index for this avatar
                        law_ids += rag_data.get("law_ids", [])
                        break

                self._index.append({
                    "content_type": "avatar",
                    "id": avatar_id,
                    "file_path": str(manifest_path.relative_to(self.constitution_path))
                        if manifest_path.exists()
                        else str(avatar_dir.relative_to(self.constitution_path)),
                    "law_ids": list(set(law_ids)),
                    "tokens": body_tokens,
                    "trigger_phrases": trigger_phrases,
                    "name": avatar_name,
                    "category": category,
                    "avatar_dir": avatar_dir.name,
                })

    # ------------------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------------------

    def _score_entry(
        self,
        entry: dict,
        query_tokens: set[str],
        query_law_ids: list[str],
        query_lower: str,
        weights: dict[str, float] | None = None,
    ) -> tuple[float, list[str], list[str]]:
        """Return (score, matched_law_ids, matched_keywords)."""
        if weights is None:
            weights = {"law_id": 3.0, "trigger": 2.0, "keyword": 1.0}

        entry_law_ids: list[str] = entry.get("law_ids", [])
        entry_tokens: set[str] = entry.get("tokens", set())
        entry_triggers: list[str] = entry.get("trigger_phrases", [])

        # 1. Exact law ID match
        matched_laws = [lid for lid in query_law_ids if lid in entry_law_ids]
        law_score = weights["law_id"] * len(matched_laws)

        # 2. Trigger phrase substring match
        # Normalize hyphens/slashes to spaces for fuzzy matching
        query_normalized = re.sub(r'[-/]', ' ', query_lower)
        matched_triggers: list[str] = []
        for trigger in entry_triggers:
            if not trigger:
                continue
            trigger_norm = re.sub(r'[-/]', ' ', trigger)
            if (trigger_norm in query_normalized or query_normalized in trigger_norm
                    or trigger in query_lower or query_lower in trigger):
                matched_triggers.append(trigger)
        trigger_score = weights["trigger"] * len(matched_triggers)

        # 3. Keyword overlap (TF-IDF-style: count / sqrt(vocab size))
        common_tokens = query_tokens & entry_tokens
        if entry_tokens:
            kw_score = weights["keyword"] * len(common_tokens) / (len(entry_tokens) ** 0.5)
        else:
            kw_score = 0.0

        total = law_score + trigger_score + kw_score
        matched_keywords = sorted(common_tokens)[:10]

        return total, matched_laws, matched_keywords

    def retrieve(self, query: str, top_k: int = 3) -> list[RetrievalResult]:
        """Retrieve top-k most relevant content for a query."""
        query_lower = query.lower()
        query_tokens = set(_tokenize(query))
        query_law_ids = _extract_law_ids(self._law_id_re, query)

        scored: list[tuple[float, dict, list[str], list[str]]] = []
        for entry in self._index:
            score, m_laws, m_kw = self._score_entry(
                entry, query_tokens, query_law_ids, query_lower
            )
            if score > 0:
                scored.append((score, entry, m_laws, m_kw))

        scored.sort(key=lambda x: x[0], reverse=True)

        return [
            RetrievalResult(
                content_type=e["content_type"],
                id=e["id"],
                file_path=e["file_path"],
                score=sc,
                matched_law_ids=ml,
                matched_keywords=mk,
                indexed_law_ids=e.get("law_ids", []),
            )
            for sc, e, ml, mk in scored[:top_k]
        ]

    def retrieve_skill_by_trigger(self, query: str, top_k: int = 3) -> list[RetrievalResult]:
        """Route query to skills via trigger phrase matching (skills only)."""
        query_lower = query.lower()
        query_tokens = set(_tokenize(query))
        query_law_ids = _extract_law_ids(self._law_id_re, query)

        scored: list[tuple[float, dict, list[str], list[str]]] = []
        for entry in self._index:
            if entry["content_type"] != "skill":
                continue
            score, m_laws, m_kw = self._score_entry(
                entry, query_tokens, query_law_ids, query_lower
            )
            if score > 0:
                scored.append((score, entry, m_laws, m_kw))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [
            RetrievalResult(
                content_type=e["content_type"],
                id=e["id"],
                file_path=e["file_path"],
                score=sc,
                matched_law_ids=ml,
                matched_keywords=mk,
                indexed_law_ids=e.get("law_ids", []),
            )
            for sc, e, ml, mk in scored[:top_k]
        ]

    def retrieve_avatar(self, query: str, top_k: int = 3) -> list[RetrievalResult]:
        """Retrieve most relevant avatar for a query."""
        query_lower = query.lower()
        query_tokens = set(_tokenize(query))
        query_law_ids = _extract_law_ids(self._law_id_re, query)

        scored: list[tuple[float, dict, list[str], list[str]]] = []
        for entry in self._index:
            if entry["content_type"] != "avatar":
                continue
            score, m_laws, m_kw = self._score_entry(
                entry, query_tokens, query_law_ids, query_lower,
                weights={"law_id": 2.0, "trigger": 3.0, "keyword": 1.0},
            )
            if score > 0:
                scored.append((score, entry, m_laws, m_kw))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [
            RetrievalResult(
                content_type=e["content_type"],
                id=e["id"],
                file_path=e["file_path"],
                score=sc,
                matched_law_ids=ml,
                matched_keywords=mk,
                indexed_law_ids=e.get("law_ids", []),
            )
            for sc, e, ml, mk in scored[:top_k]
        ]

    def index_stats(self) -> dict:
        """Return counts of indexed items by type."""
        counts: dict[str, int] = {}
        for entry in self._index:
            ct = entry["content_type"]
            counts[ct] = counts.get(ct, 0) + 1
        return counts
