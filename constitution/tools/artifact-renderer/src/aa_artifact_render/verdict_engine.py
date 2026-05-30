"""
verdict_engine.py — Ensemble agent persona scoring for constitutional build verdicts.

Evaluates a list of persona verdicts (each carrying PASS | WARN | FAIL) and
produces an aggregate constitutional verdict:

  - ALL PASS            → APPROVED
  - any WARN, no FAIL   → APPROVED_WITH_CONDITIONS
  - any FAIL            → BLOCKED

Usage (from Jinja2 template rendering pipeline)::

    from aa_artifact_render.verdict_engine import VerdictEngine

    engine = VerdictEngine()
    ensemble = engine.evaluate(frontmatter.get("ensemble_verdict", {}).get("verdicts", []))
    # ensemble.aggregate → AggregateVerdict
    # ensemble.personas  → list[PersonaVerdict]
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class VerdictLevel(str, Enum):
    """Possible verdict for a single persona."""

    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"


class AggregateVerdict(str, Enum):
    """Constitutional build verdict computed across all persona verdicts."""

    APPROVED = "APPROVED"
    APPROVED_WITH_CONDITIONS = "APPROVED_WITH_CONDITIONS"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class PersonaVerdict:
    """A single agent persona's verdict on the build."""

    persona: str
    law: str
    verdict: VerdictLevel
    note: str


@dataclass(frozen=True)
class EnsembleVerdict:
    """The full ensemble result: individual persona verdicts + aggregate."""

    personas: tuple[PersonaVerdict, ...]
    aggregate: AggregateVerdict


class VerdictEngine:
    """
    Evaluates a list of persona verdict dicts into a structured EnsembleVerdict.

    Each dict must have keys: ``persona``, ``law``, ``verdict``, ``note``.
    The ``verdict`` value must be one of the :class:`VerdictLevel` members
    (case-sensitive: ``PASS``, ``WARN``, ``FAIL``). An unrecognised value raises
    :class:`ValueError`.

    Missing required keys raise :class:`KeyError`.
    """

    def evaluate(self, verdicts: list[dict[str, Any]]) -> EnsembleVerdict:
        """
        Evaluate a list of raw verdict dicts.

        Args:
            verdicts: List of dicts from frontmatter ``ensemble_verdict.verdicts``.

        Returns:
            :class:`EnsembleVerdict` with individual :class:`PersonaVerdict` objects
            and the computed :class:`AggregateVerdict`.

        Raises:
            ValueError: If a verdict string is not a valid :class:`VerdictLevel`.
            KeyError:   If a required key is missing from a verdict dict.
        """
        persona_verdicts = [self._parse(v) for v in verdicts]
        aggregate = self._aggregate(persona_verdicts)
        return EnsembleVerdict(personas=tuple(persona_verdicts), aggregate=aggregate)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _parse(raw: dict[str, Any]) -> PersonaVerdict:
        verdict_str: str = raw["verdict"]
        try:
            level = VerdictLevel(verdict_str)
        except ValueError:
            raise ValueError(
                f"Invalid verdict value {verdict_str!r}. "
                f"Expected one of: {[v.value for v in VerdictLevel]}"
            )
        return PersonaVerdict(
            persona=str(raw["persona"]),
            law=str(raw["law"]),
            verdict=level,
            note=str(raw["note"]),
        )

    @staticmethod
    def _aggregate(personas: list[PersonaVerdict]) -> AggregateVerdict:
        if not personas:
            return AggregateVerdict.APPROVED
        levels = {pv.verdict for pv in personas}
        if VerdictLevel.FAIL in levels:
            return AggregateVerdict.BLOCKED
        if VerdictLevel.WARN in levels:
            return AggregateVerdict.APPROVED_WITH_CONDITIONS
        return AggregateVerdict.APPROVED
