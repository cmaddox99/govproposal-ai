"""Law reference coverage tests for C++ avatar guidance.md.

Ensures every governance section in guidance.md cites the constitutional
law(s) that govern it.  This catches accidental deletion of law references
during editing — the exact bug that removed the ENG-6.1 citation from the
Concurrency section.

Each test case maps a section heading to the law ID(s) that MUST appear
(as markdown hyperlinks) within that section's text.
"""

import pathlib
import re
from typing import Dict, List

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[3]
_CPP_DIR = ROOT / "avatars" / "technology" / "cpp"


# ── Helpers ─────────────────────────────────────────────────────────────


def _load_sections(text: str) -> Dict[str, str]:
    """Split guidance.md into {heading: body} for ## headings.

    The body of each section includes all text (and sub-headings) up to
    the next ## heading or end-of-file.
    """
    pattern = re.compile(r"^(## .+)$", re.MULTILINE)
    splits = pattern.split(text)
    sections: Dict[str, str] = {}
    # splits alternates: [preamble, heading1, body1, heading2, body2, ...]
    for i in range(1, len(splits) - 1, 2):
        heading = splits[i].strip().lstrip("# ").strip()
        body = splits[i + 1]
        sections[heading] = body
    return sections


def _law_hyperlinks_in(text: str) -> set:
    """Return set of law IDs found as markdown hyperlinks [LAW-ID](...)."""
    return set(re.findall(r"\[(ENG-\d+\.\d+|BUS-\d+\.\d+|PRD-\d+\.\d+)\]\(", text))


@pytest.fixture(scope="module")
def guidance_text():
    return "\n".join(p.read_text(encoding="utf-8") for p in sorted(_CPP_DIR.rglob("ref-*.md")))


@pytest.fixture(scope="module")
def sections(guidance_text):
    return _load_sections(guidance_text)


# ── Sections explicitly exempt from law references ──────────────────────
#
# These sections are informational, navigational, or purely technical
# reference material that do not govern behavior under a specific law.
# Any NEW ## section must either:
#   (a) appear in SECTION_LAW_REQUIREMENTS with its governing law(s), OR
#   (b) appear in SECTIONS_EXEMPT_FROM_LAWS with a justification, OR
#   (c) contain at least one hyperlinked law reference in its body.
# Failing all three causes test_new_sections_have_law_references to fail.

SECTIONS_EXEMPT_FROM_LAWS = {
    # Preamble / navigation — no governance content
    "Overview",
    "Table of Contents",
    "Quick-Start Guide",
    "Glossary for Java Developers",  # reference table, not governance
    "C++ Version Policy",        # governed by stakeholder decision, not a law
    "Testing Framework",         # subsections carry the law refs (ENG-4.1, ENG-4.2)
    "Anti-Patterns to Avoid",    # umbrella heading; each anti-pattern subsection has refs
    "Tools and Commands",        # pure CLI reference
    "Priority Matrix",           # informational table only
    # Operational reference — routed from manifest per schema §3
    "Skill Parity",              # parity metadata, not governance content
    "Project Archetypes",        # project type selection guide, not law governance
    "Authorities and References",  # external reference links, not governance content
    "See Also",                  # cross-reference navigation, not governance content
    "Further Reading",           # bibliographic citations (SOURCES.md Tier 3); no governance content
}

# ── Section → Required Law(s) Mapping ──────────────────────────────────
#
# Format: (section_heading, [list_of_required_law_ids])
#
# IMPORTANT: When adding a new governance section to guidance.md, add the
# corresponding entry here.  This is the canonical registry of which laws
# govern which sections.

SECTION_LAW_REQUIREMENTS = [
    # -- Core governance sections --
    ("Package Management", ["ENG-6.6"]),
    ("Domain Modeling", ["ENG-2.1"]),
    ("Dependency Injection in C++", ["ENG-2.5"]),
    ("Safety and Ownership", ["ENG-6.1"]),
    ("Concurrency", ["ENG-6.1"]),
    ("CI Quality Toolchain Policy", ["ENG-5.2"]),
    ("Exception Safety and Error Handling", ["ENG-6.1", "ENG-3.7"]),
    ("Coroutines", ["ENG-3.1"]),
    ("Structured Logging and Diagnostics", ["ENG-6.7"]),
    ("Health Check and Readiness Probes", ["ENG-7.1", "ENG-7.7"]),
    ("C++20 Modules", ["ENG-2.2"]),
    ("Allocator Governance", ["ENG-3.1"]),
    ("ABI Stability and Binary Compatibility", ["ENG-2.3"]),
    ("Template and Metaprogramming Governance", ["ENG-3.1"]),
    ("Termination and Recovery Policy", ["ENG-7.1"]),
    ("C/C++ Interop and FFI Error Propagation", ["ENG-6.1"]),
    ("Reproducible Builds", ["ENG-5.1"]),
    ("License Compliance and Dependency Governance", ["ENG-6.6"]),
    ("Configuration Management", ["ENG-6.1"]),

    # -- Brownfield / migration sections --
    ("Brownfield Migration", ["ENG-1.4"]),
    ("Legacy Code Navigation for New Engineers", ["ENG-1.2"]),
    ("Per-Tier clang-tidy Configuration", ["ENG-3.1", "ENG-5.2"]),
    ("Per-Tier Testing Framework Matrix", ["ENG-4.2"]),
    ("Per-Tier Code Review Criteria", ["ENG-3.1"]),
    ("Cross-Standard ABI Boundaries", ["ENG-2.4"]),
    ("Feature-Detection Macro Governance", ["ENG-5.3"]),
    ("Compiler Flag Progression During Migration", ["ENG-5.2"]),
    ("Sanitizer Availability by Compiler Version", ["ENG-6.1"]),
    ("Dual-Toolchain Governance", ["ENG-5.2"]),
    ("Dependency Standard Mismatch", ["ENG-6.6"]),
    ("Writing New Code for Legacy Standards", ["ENG-1.3"]),

    # -- Migration playbooks --
    ("Migration Playbook: C++98/03 → C++11", ["ENG-1.4"]),
    ("Migration Playbook: C++11 → C++14", ["ENG-1.4"]),
    ("Migration Playbook: C++14 → C++17", ["ENG-1.4"]),
    ("Migration Playbook: C++17 → C++20", ["ENG-1.4"]),

    # -- Novice guidance sections --
    ("Mental Model Transitions", ["ENG-3.1"]),
    ("Legacy Code Smell Catalog", ["ENG-3.1"]),
    ("Legacy Codebase Triage Playbook", ["ENG-4.1", "ENG-6.1"]),
    ("Survival Patterns", ["ENG-4.1", "ENG-3.1"]),
    ("Object Design Rehabilitation", ["ENG-3.1", "ENG-2.1"]),

    # -- Resiliency patterns --
    ("Resiliency Patterns", ["ENG-7.1", "ENG-7.2", "ENG-7.3", "ENG-7.4", "ENG-7.5", "ENG-7.6"]),

    # -- Advanced governance (Phase 15b) --
    ("Advanced Memory and Object Lifetime", ["ENG-6.1", "ENG-3.1"]),
    ("Forwarding, ADL, and Template Safety", ["ENG-3.1", "ENG-6.1"]),
    ("Lambda and Functional Pattern Governance", ["ENG-6.1"]),

    # -- P1 patterns (Phase 15c) --
    ("Test Isolation and Mock Boundaries", ["ENG-4.7", "ENG-4.8"]),
    ("Implicit Conversions and Type Safety", ["ENG-3.1", "ENG-6.1"]),
    ("Cast Governance", ["ENG-6.1", "ENG-3.1"]),
    ("Const Correctness Philosophy", ["ENG-3.1"]),
    ("SRP and C++ Refactoring Patterns", ["ENG-3.4", "ENG-3.8"]),

    # -- Preprocessor and macro governance (Amendment L) --
    ("Preprocessor and Macro Governance", ["ENG-3.1"]),

    # -- Compliance and safety sections --
    ("Safety-Critical C++ (MISRA C++ / DO-178C / JSF AV C++)", ["ENG-6.1"]),
    # -- P2 additions: designated init, null safety, void* migration --
    ("Designated Initializers ★ C++20", ["ENG-3.1"]),
    ("Null Safety and Pointer Contracts", ["ENG-6.1", "ENG-3.1"]),
    ("Type-Safe Unions: `void*` → `std::variant` / `std::any` ★ C++17", ["ENG-6.1", "ENG-3.1"]),
]


# ── Parametrized Tests ──────────────────────────────────────────────────


@pytest.mark.parametrize(
    "section_heading, required_laws",
    SECTION_LAW_REQUIREMENTS,
    ids=[f"{h}→{','.join(laws)}" for h, laws in SECTION_LAW_REQUIREMENTS],
)
class TestSectionLawReferences:
    """Each governance section must cite its governing law(s) as hyperlinks."""

    def test_section_exists(self, sections, section_heading, required_laws):
        assert section_heading in sections, (
            f"Section '## {section_heading}' not found in guidance.md. "
            f"If renamed, update SECTION_LAW_REQUIREMENTS in this test."
        )

    def test_required_laws_present(self, sections, section_heading, required_laws):
        if section_heading not in sections:
            pytest.skip(f"Section '{section_heading}' not found")
        body = sections[section_heading]
        found = _law_hyperlinks_in(body)
        for law_id in required_laws:
            assert law_id in found, (
                f"Section '## {section_heading}' is missing a hyperlinked "
                f"reference to [{law_id}]. Found: {sorted(found) or 'none'}. "
                f"Every governance section must cite its governing law(s)."
            )


# ── Global invariants ───────────────────────────────────────────────────


class TestLawReferenceInvariants:
    """Global checks across all of guidance.md."""

    def test_no_bare_law_references(self, guidance_text):
        """Every individual ENG-*/BUS-* mention must be a markdown hyperlink.

        Checks each occurrence, not just unique IDs.  This catches the case
        where ENG-6.1 is properly hyperlinked in section A but appears as
        bare text in a new section B.
        """
        bare_refs = []
        for i, line in enumerate(guidance_text.splitlines(), 1):
            # Find all law-like patterns on this line
            for match in re.finditer(r"(?:ENG|BUS|PRD)-\d+\.\d+", line):
                law_id = match.group()
                start = match.start()
                # Check if this occurrence is inside a markdown hyperlink [LAW](
                # Look for '[' before and '](laws/' after
                prefix = line[:start]
                suffix = line[start + len(law_id):]
                if prefix.endswith("[") and suffix.startswith("](laws/"):
                    continue  # properly hyperlinked
                bare_refs.append(f"  line {i}: {law_id}  →  {line.strip()[:100]}")
        assert not bare_refs, (
            f"Found {len(bare_refs)} bare (non-hyperlinked) law reference(s):\n"
            + "\n".join(bare_refs[:20])
            + ("\n  ... and more" if len(bare_refs) > 20 else "")
            + "\n\nAll law references must use [LAW-ID](laws/...) format."
        )

    def test_hyperlinks_point_to_correct_paths(self, guidance_text):
        """Law hyperlinks must point to the correct law file."""
        law_path_map = {
            "ENG-1": "laws/engineering/eng-1-core-principles.md",
            "ENG-2": "laws/engineering/eng-2-architecture.md",
            "ENG-3": "laws/engineering/eng-3-code-quality.md",
            "ENG-4": "laws/engineering/eng-4-testing.md",
            "ENG-5": "laws/engineering/eng-5-devops.md",
            "ENG-6": "laws/engineering/eng-6-security.md",
            "ENG-7": "laws/engineering/eng-7-reliability.md",
            "ENG-9": "laws/engineering/eng-9-data-engineering.md",
            "ENG-10": "laws/engineering/eng-10-documentation.md",
            "ENG-11": "laws/engineering/eng-11-sdd.md",
            "BUS-1": "laws/business/bus-1-strategic-alignment.md",
            "BUS-2": "laws/business/bus-2-compliance.md",
            "BUS-3": "laws/business/bus-3-data-governance.md",
            "BUS-5": "laws/business/bus-5-vendor-management.md",
            "BUS-7": "laws/business/bus-7-operational-governance.md",
            "BUS-8": "laws/business/bus-8-intellectual-property.md",
            "BUS-9": "laws/business/bus-9-incident-management.md",
        }
        # Extract all [LAW-ID](path) pairs
        refs = re.findall(
            r"\[((?:ENG|BUS|PRD)-(\d+)\.\d+)\]\((laws/[^)]+)\)", guidance_text
        )
        errors = []
        for law_id, article_num, path in refs:
            prefix = law_id.split(".")[0]  # e.g. "ENG-6"
            expected_path = law_path_map.get(prefix)
            if expected_path and path != expected_path:
                errors.append(
                    f"[{law_id}]({path}) should point to {expected_path}"
                )
        assert not errors, (
            f"Misrouted law hyperlinks:\n" + "\n".join(errors)
        )

    def test_minimum_law_coverage(self, guidance_text):
        """guidance.md must reference a minimum set of critical laws."""
        critical_laws = {
            "ENG-2.1",  # DDD
            "ENG-3.1",  # Complexity Limits
            "ENG-4.1",  # Atomic TDD
            "ENG-4.2",  # Test Pyramid
            "ENG-5.2",  # CI/CD Pipeline
            "ENG-6.1",  # Security by Design
            "ENG-6.7",  # Audit Trail
            "ENG-7.1",  # Failure Handling
        }
        found = _law_hyperlinks_in(guidance_text)
        missing = critical_laws - found
        assert not missing, (
            f"guidance.md is missing references to critical laws: {sorted(missing)}"
        )

    def test_total_law_reference_count_not_regressed(self, guidance_text):
        """Guard against bulk deletion of law references."""
        count = len(re.findall(
            r"\[(?:ENG|BUS|PRD)-\d+\.\d+\]\(laws/", guidance_text
        ))
        # Current count is ~150+ after removing BUS-* domain boundary violations (Amendment O)
        assert count >= 130, (
            f"Law reference count ({count}) dropped below 130. "
            f"Expected ~150+. Check for accidental deletions."
        )

    def test_new_sections_have_law_references(self, sections):
        """Any new ## section must be registered or contain a law reference.

        This catches the case where someone adds a new governance section
        to guidance.md but forgets to cite the governing law.  To fix a
        failure here, do ONE of:
          1. Add the section + its law(s) to SECTION_LAW_REQUIREMENTS
          2. Add the section to SECTIONS_EXEMPT_FROM_LAWS (with justification)
          3. Add a law hyperlink [ENG-x.y](laws/...) to the section body
        """
        registered = {h for h, _ in SECTION_LAW_REQUIREMENTS}
        unregistered_without_laws = []
        for heading, body in sections.items():
            if heading in registered or heading in SECTIONS_EXEMPT_FROM_LAWS:
                continue
            # Section is not registered and not exempt — it must self-document
            found = _law_hyperlinks_in(body)
            if not found:
                unregistered_without_laws.append(heading)
        assert not unregistered_without_laws, (
            f"The following ## sections are not in SECTION_LAW_REQUIREMENTS, "
            f"not in SECTIONS_EXEMPT_FROM_LAWS, and contain no law hyperlinks:\n"
            + "\n".join(f"  - ## {h}" for h in unregistered_without_laws)
            + "\n\nEither add governing law references to the section, "
            "register it in SECTION_LAW_REQUIREMENTS, or exempt it in "
            "SECTIONS_EXEMPT_FROM_LAWS."
        )
