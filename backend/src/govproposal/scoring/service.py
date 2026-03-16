"""Service layer for scoring operations."""

import json
import logging
from dataclasses import dataclass
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from govproposal.ai.service import score_with_claude
from govproposal.config import settings
from govproposal.scoring.models import (
    ColorTeamType,
    DEFAULT_SCORE_WEIGHTS,
    ProposalBenchmark,
    ProposalScore,
    ReadinessIndicator,
    ReadinessLevel,
    ScoreExplanation,
    ScoreFactor,
    ScoreFactorType,
)
from govproposal.scoring.repository import (
    BenchmarkRepository,
    ReadinessRepository,
    ScoringRepository,
)
from govproposal.scoring.schemas import (
    BlockerItem,
    BenchmarkResponse,
    GoNoGoSummary,
    ImprovementListResponse,
    ProposalScoreResponse,
    ReadinessResponse,
    ScoreFactorResponse,
    ScoreHistoryResponse,
    ScoreImprovementResponse,
    WarningItem,
)
from govproposal.scoring.templates import format_template, get_template

logger = logging.getLogger(__name__)


@dataclass
class FactorResult:
    """Result from scoring a single factor."""

    raw_score: int
    evidence: str
    improvements: list[dict]
    strengths: list[str] | None = None
    weaknesses: list[str] | None = None


# Readiness criteria per color team
READINESS_CRITERIA: dict[ColorTeamType, list[dict]] = {
    ColorTeamType.PINK_TEAM: [
        {
            "name": "outline_complete",
            "description": "All sections have outlines",
            "category": "structure",
        },
        {
            "name": "win_themes_defined",
            "description": "Win themes documented",
            "category": "strategy",
        },
        {
            "name": "compliance_matrix_started",
            "description": "Compliance matrix initiated",
            "category": "compliance",
        },
    ],
    ColorTeamType.RED_TEAM: [
        {
            "name": "all_sections_drafted",
            "description": "All sections have full drafts",
            "category": "content",
        },
        {
            "name": "compliance_checked",
            "description": "Compliance checklist reviewed",
            "category": "compliance",
        },
        {
            "name": "graphics_placed",
            "description": "Key graphics included",
            "category": "visuals",
        },
        {
            "name": "past_performance_included",
            "description": "Past performance examples documented",
            "category": "content",
        },
    ],
    ColorTeamType.GOLD_TEAM: [
        {
            "name": "all_sections_final",
            "description": "All sections marked final",
            "category": "content",
        },
        {
            "name": "compliance_complete",
            "description": "100% compliance verified",
            "category": "compliance",
        },
        {
            "name": "pricing_complete",
            "description": "Pricing volume complete",
            "category": "pricing",
        },
        {
            "name": "all_reviews_addressed",
            "description": "All review comments addressed",
            "category": "quality",
        },
    ],
    ColorTeamType.SUBMISSION: [
        {
            "name": "all_gold_criteria",
            "description": "All Gold Team criteria met",
            "category": "prerequisite",
        },
        {
            "name": "format_verified",
            "description": "Format requirements verified",
            "category": "compliance",
        },
        {
            "name": "signatures_obtained",
            "description": "Required signatures obtained",
            "category": "administrative",
        },
        {
            "name": "submission_package_ready",
            "description": "Submission package assembled",
            "category": "administrative",
        },
    ],
}


def _score_to_response(score: ProposalScore) -> ProposalScoreResponse:
    """Convert a ProposalScore model to its API response schema."""
    return ProposalScoreResponse(
        id=score.id,
        proposal_id=score.proposal_id,
        score_date=score.score_date,
        overall_score=score.overall_score,
        confidence_level=score.confidence_level,
        ai_model_used=score.ai_model_used,
        created_by=score.created_by,
        created_at=score.created_at,
        factors=[
            ScoreFactorResponse(
                id=f.id,
                factor_type=f.factor_type,
                factor_weight=f.factor_weight,
                raw_score=f.raw_score,
                weighted_score=f.weighted_score,
                evidence_summary=f.evidence_summary,
                improvement_suggestions=f.improvement_suggestions,
            )
            for f in score.factors
        ],
    )


class ScoringService:
    """Multi-factor proposal scoring service."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._repo = ScoringRepository(session)

    async def calculate_score(
        self,
        proposal_id: str,
        user_id: str,
        proposal_data: dict | None = None,
    ) -> ProposalScoreResponse:
        """Calculate comprehensive relevance score for a proposal."""
        factors = await self._score_all_factors(proposal_data, proposal_id)
        overall = sum(f.weighted_score for f in factors)
        confidence = self._determine_confidence(proposal_data, factors)

        score = ProposalScore(
            proposal_id=proposal_id,
            overall_score=int(overall),
            confidence_level=confidence,
            ai_model_used=settings.anthropic_model,
            created_by=user_id,
            factors=factors,
        )
        saved = await self._repo.create_score(score)
        return _score_to_response(saved)

    async def _score_all_factors(
        self, proposal_data: dict | None, proposal_id: str,
    ) -> list[ScoreFactor]:
        """Calculate all scoring factors and return ScoreFactor list."""
        factors: list[ScoreFactor] = []
        for factor_type, weight in DEFAULT_SCORE_WEIGHTS.items():
            result = await self._calculate_factor(
                proposal_id, factor_type, proposal_data
            )
            factors.append(ScoreFactor(
                factor_type=factor_type.value,
                factor_weight=weight,
                raw_score=result.raw_score,
                weighted_score=result.raw_score * weight,
                evidence_summary=result.evidence,
                improvement_suggestions=result.improvements,
            ))
        return factors

    async def _calculate_factor(
        self,
        proposal_id: str,
        factor_type: ScoreFactorType,
        proposal_data: dict | None,
    ) -> FactorResult:
        """Calculate individual factor score using Claude AI with fallback."""
        template_map = {
            ScoreFactorType.COMPLETENESS: "completeness_scorer",
            ScoreFactorType.TECHNICAL_DEPTH: "technical_depth_scorer",
            ScoreFactorType.SECTION_L_COMPLIANCE: "compliance_scorer",
            ScoreFactorType.SECTION_M_ALIGNMENT: "section_m_scorer",
        }

        template_name = template_map.get(factor_type)
        if not template_name:
            return self._fallback_score(factor_type, proposal_data)

        template = get_template(template_name)
        if not template or not proposal_data:
            return self._fallback_score(factor_type, proposal_data)

        # Build template variables from proposal data
        template_vars = self._build_template_vars(factor_type, proposal_data)

        try:
            system_prompt, user_prompt = format_template(template, **template_vars)
        except KeyError as e:
            logger.warning(f"Missing template variable {e} for {factor_type}")
            return self._fallback_score(factor_type, proposal_data)

        # Call Claude
        result = await score_with_claude(system_prompt, user_prompt)
        if result:
            return FactorResult(
                raw_score=max(0, min(100, int(result.get("score", 50)))),
                evidence=result.get("evidence", "AI analysis complete"),
                improvements=result.get("improvements", []),
                strengths=result.get("strengths") or result.get("well_aligned_factors"),
                weaknesses=result.get("weaknesses") or result.get("poorly_aligned_factors"),
            )

        # Fallback to basic scoring if Claude unavailable
        return self._fallback_score(factor_type, proposal_data)

    def _build_template_vars(
        self, factor_type: ScoreFactorType, proposal_data: dict
    ) -> dict:
        """Build template variables from proposal data for a given factor."""
        title = proposal_data.get("title", "Untitled Proposal")
        description = proposal_data.get("description", "")

        # Build sections summary
        section_names = ["executive_summary", "technical_approach", "management_approach",
                         "past_performance", "pricing_summary"]
        sections_parts = []
        for name in section_names:
            content = proposal_data.get(name, "")
            label = name.replace("_", " ").title()
            if content:
                preview = content[:500] + ("..." if len(content) > 500 else "")
                sections_parts.append(f"### {label}\n{preview}")
            else:
                sections_parts.append(f"### {label}\n[Not provided]")
        sections_summary = "\n\n".join(sections_parts)

        # All proposal content combined
        all_content = "\n\n".join(
            f"## {name.replace('_', ' ').title()}\n{proposal_data.get(name, '[Not provided]')}"
            for name in section_names
        )

        if factor_type == ScoreFactorType.COMPLETENESS:
            return {
                "title": title,
                "sections_summary": sections_summary,
            }
        elif factor_type == ScoreFactorType.TECHNICAL_DEPTH:
            return {
                "technical_content": proposal_data.get("technical_approach", "") or all_content,
                "requirements_summary": description or f"Proposal for: {title}",
            }
        elif factor_type == ScoreFactorType.SECTION_L_COMPLIANCE:
            return {
                "section_l": description or "No specific Section L instructions available. Evaluate based on standard government proposal requirements.",
                "proposal_structure": sections_summary,
            }
        elif factor_type == ScoreFactorType.SECTION_M_ALIGNMENT:
            return {
                "section_m": description or "No specific Section M criteria available. Evaluate based on standard evaluation factors: technical capability, past performance, price, and management approach.",
                "proposal_content": all_content,
            }
        return {}

    def _fallback_score(
        self, factor_type: ScoreFactorType, proposal_data: dict | None
    ) -> FactorResult:
        """Basic scoring fallback when Claude is not available."""
        if not proposal_data:
            return FactorResult(
                raw_score=50,
                evidence="No proposal content available for analysis.",
                improvements=[{"action": "Add proposal content", "details": "Fill in proposal sections for AI-powered scoring", "priority": "high"}],
            )

        section_fields = ["executive_summary", "technical_approach", "management_approach",
                          "past_performance", "pricing_summary"]
        present = [f for f in section_fields if proposal_data.get(f)]
        missing = [f for f in section_fields if not proposal_data.get(f)]

        dispatch = {
            ScoreFactorType.COMPLETENESS: self._fb_completeness,
            ScoreFactorType.TECHNICAL_DEPTH: self._fb_technical_depth,
            ScoreFactorType.SECTION_L_COMPLIANCE: self._fb_compliance,
            ScoreFactorType.SECTION_M_ALIGNMENT: self._fb_alignment,
        }
        handler = dispatch.get(factor_type, self._fb_alignment)
        return handler(proposal_data, present, missing)

    def _fb_completeness(self, data: dict, present: list, missing: list) -> FactorResult:
        total = len(present) + len(missing)
        score = int((len(present) / total) * 100)
        improvements = [
            {"action": f"Add {s.replace('_', ' ').title()}", "details": "This section is missing", "priority": "high"}
            for s in missing
        ]
        return FactorResult(raw_score=score, evidence=f"{len(present)} of {total} sections completed", improvements=improvements)

    def _fb_technical_depth(self, data: dict, present: list, missing: list) -> FactorResult:
        tech = data.get("technical_approach", "")
        score = min(85, 40 + len(tech) // 50) if tech else 30
        evidence = f"Technical approach has {len(tech)} characters" if tech else "No technical approach provided"
        improvements = [{"action": "Add specific methodologies", "details": "Include concrete tools, processes, and technical details", "priority": "medium"}] if score < 80 else []
        return FactorResult(raw_score=score, evidence=evidence, improvements=improvements)

    def _fb_compliance(self, data: dict, present: list, missing: list) -> FactorResult:
        score = min(90, 60 + len(present) * 6)
        improvements = [{"action": "Verify format requirements", "details": "Confirm page limits, fonts, and margins", "priority": "high"}] if score < 80 else []
        return FactorResult(raw_score=score, evidence=f"Basic compliance check: {len(present)} sections present", improvements=improvements)

    def _fb_alignment(self, data: dict, present: list, missing: list) -> FactorResult:
        score = min(85, 55 + len(present) * 7)
        improvements = [{"action": "Align content with evaluation criteria", "details": "Reorganize to directly address each evaluation factor", "priority": "high"}] if score < 80 else []
        return FactorResult(raw_score=score, evidence=f"Alignment check: {len(present)} sections available", improvements=improvements)

    def _determine_confidence(
        self, proposal_data: dict | None, factors: list[ScoreFactor]
    ) -> str:
        """Determine confidence level based on data quality."""
        if not proposal_data:
            return "low"

        # Count how many content sections have actual content
        section_fields = ["executive_summary", "technical_approach", "management_approach",
                          "past_performance", "pricing_summary"]
        filled = sum(1 for f in section_fields if proposal_data.get(f))

        if filled >= 4:
            return "high"
        elif filled >= 2:
            return "medium"
        return "low"

    async def get_latest_score(self, proposal_id: str) -> ProposalScoreResponse | None:
        """Get the most recent score for a proposal."""
        score = await self._repo.get_latest_score(proposal_id)
        if not score:
            return None
        return _score_to_response(score)

    async def get_score_history(
        self, proposal_id: str, limit: int = 10
    ) -> ScoreHistoryResponse:
        """Get score history for a proposal."""
        scores = await self._repo.get_score_history(proposal_id, limit)

        # Determine trend
        if len(scores) < 2:
            trend = "stable"
        else:
            recent = scores[0].overall_score
            previous = scores[1].overall_score
            if recent > previous + 5:
                trend = "improving"
            elif recent < previous - 5:
                trend = "declining"
            else:
                trend = "stable"

        return ScoreHistoryResponse(
            proposal_id=proposal_id,
            scores=[
                {
                    "id": s.id,
                    "proposal_id": s.proposal_id,
                    "score_date": s.score_date,
                    "overall_score": s.overall_score,
                    "confidence_level": s.confidence_level,
                }
                for s in scores
            ],
            trend=trend,
        )

    async def get_improvements(
        self, proposal_id: str
    ) -> ImprovementListResponse:
        """Get prioritized improvements to increase score."""
        score = await self._repo.get_latest_score(proposal_id)
        if not score:
            return ImprovementListResponse(
                proposal_id=proposal_id,
                current_score=0,
                improvements=[],
            )

        improvements: list[ScoreImprovementResponse] = []
        priority = 1

        # Sort factors by raw_score (lowest first for biggest improvement opportunity)
        sorted_factors = sorted(score.factors, key=lambda f: f.raw_score)

        for factor in sorted_factors:
            if factor.raw_score < 80 and factor.improvement_suggestions:
                potential_gain = int((100 - factor.raw_score) * factor.factor_weight)

                suggestions = factor.improvement_suggestions
                if isinstance(suggestions, list):
                    for suggestion in suggestions[:3]:  # Top 3 per factor
                        improvements.append(
                            ScoreImprovementResponse(
                                priority=priority,
                                factor=factor.factor_type,
                                current_score=factor.raw_score,
                                potential_gain=potential_gain,
                                action=suggestion.get("action", ""),
                                details=suggestion.get("details", ""),
                            )
                        )
                        priority += 1

        return ImprovementListResponse(
            proposal_id=proposal_id,
            current_score=score.overall_score,
            improvements=improvements[:10],  # Top 10 improvements
        )


class BenchmarkService:
    """Benchmark and readiness assessment service."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._benchmark_repo = BenchmarkRepository(session)
        self._readiness_repo = ReadinessRepository(session)
        self._scoring_repo = ScoringRepository(session)

    def _extract_factor_scores(self, score: ProposalScore | None) -> tuple[int, int, int]:
        """Extract completeness, technical_depth, compliance from score factors."""
        completeness, technical_depth, compliance = 70, 70, 70
        if not score:
            return completeness, technical_depth, compliance
        for f in score.factors:
            if f.factor_type == ScoreFactorType.COMPLETENESS.value:
                completeness = f.raw_score
            elif f.factor_type == ScoreFactorType.TECHNICAL_DEPTH.value:
                technical_depth = f.raw_score
            elif f.factor_type == ScoreFactorType.SECTION_L_COMPLIANCE.value:
                compliance = f.raw_score
        return completeness, technical_depth, compliance

    async def _calc_org_percentile(
        self, score: ProposalScore, proposal_ids: list[str],
    ) -> tuple[int | None, float | None]:
        """Calculate org percentile and average from peer proposals."""
        stats = await self._scoring_repo.get_org_score_stats("", proposal_ids)
        if stats["count"] == 0:
            return None, None
        avg = stats["avg_score"]
        if score.overall_score >= stats["max_score"]:
            return 100, avg
        if score.overall_score <= stats["min_score"]:
            return 0, avg
        rng = stats["max_score"] - stats["min_score"]
        pct = int(((score.overall_score - stats["min_score"]) / rng) * 100) if rng > 0 else 50
        return pct, avg

    async def calculate_benchmark(
        self, proposal_id: str, organization_proposal_ids: list[str] | None = None
    ) -> BenchmarkResponse:
        """Calculate benchmark metrics for proposal."""
        score = await self._scoring_repo.get_latest_score(proposal_id)
        completeness, technical_depth, compliance = self._extract_factor_scores(score)

        org_percentile, org_avg = None, None
        if organization_proposal_ids and score:
            org_percentile, org_avg = await self._calc_org_percentile(
                score, organization_proposal_ids,
            )

        benchmark = ProposalBenchmark(
            proposal_id=proposal_id,
            completeness_score=completeness,
            technical_depth_score=technical_depth,
            compliance_score=compliance,
            org_percentile=org_percentile,
            org_avg_at_stage=org_avg,
        )
        saved = await self._benchmark_repo.create_benchmark(benchmark)
        return BenchmarkResponse(
            id=saved.id, proposal_id=saved.proposal_id,
            benchmark_date=saved.benchmark_date,
            completeness_score=saved.completeness_score,
            technical_depth_score=saved.technical_depth_score,
            compliance_score=saved.compliance_score,
            org_percentile=saved.org_percentile,
            org_avg_at_stage=saved.org_avg_at_stage,
        )

    async def check_readiness(
        self,
        proposal_id: str,
        team_type: ColorTeamType,
        user_id: str,
        proposal_data: dict | None = None,
    ) -> ReadinessResponse:
        """Check readiness for specific color team review."""
        criteria = READINESS_CRITERIA.get(team_type, [])

        blockers: list[BlockerItem] = []
        warnings: list[WarningItem] = []

        # Check each criterion (placeholder logic)
        for criterion in criteria:
            # In production, would check actual proposal state
            # For now, simulate some results
            is_met = True  # Placeholder

            if not is_met:
                if criterion.get("category") in ("content", "compliance", "prerequisite"):
                    blockers.append(
                        BlockerItem(
                            category=criterion["category"],
                            description=criterion["description"],
                            section=None,
                        )
                    )
                else:
                    warnings.append(
                        WarningItem(
                            category=criterion["category"],
                            description=criterion["description"],
                            recommendation=f"Complete: {criterion['description']}",
                        )
                    )

        # Calculate readiness
        if blockers:
            level = ReadinessLevel.NOT_READY
            readiness_score = max(0, 50 - len(blockers) * 10)
        elif warnings:
            level = ReadinessLevel.NEEDS_WORK
            readiness_score = max(50, 80 - len(warnings) * 5)
        else:
            level = ReadinessLevel.READY
            readiness_score = 90

        # Save indicator
        indicator = ReadinessIndicator(
            proposal_id=proposal_id,
            team_type=team_type.value,
            readiness_score=readiness_score,
            readiness_level=level.value,
            blockers=[b.model_dump() for b in blockers],
            warnings=[w.model_dump() for w in warnings],
            checked_by=user_id,
        )

        saved = await self._readiness_repo.create_indicator(indicator)

        return ReadinessResponse(
            id=saved.id,
            proposal_id=saved.proposal_id,
            team_type=saved.team_type,
            readiness_score=saved.readiness_score,
            readiness_level=saved.readiness_level,
            blockers=blockers,
            warnings=warnings,
            checked_at=saved.checked_at,
            checked_by=saved.checked_by,
        )

    async def get_readiness(
        self, proposal_id: str, team_type: ColorTeamType
    ) -> ReadinessResponse | None:
        """Get latest readiness for a proposal and team type."""
        indicator = await self._readiness_repo.get_latest_by_team_type(
            proposal_id, team_type.value
        )
        if not indicator:
            return None

        return ReadinessResponse(
            id=indicator.id,
            proposal_id=indicator.proposal_id,
            team_type=indicator.team_type,
            readiness_score=indicator.readiness_score,
            readiness_level=indicator.readiness_level,
            blockers=[BlockerItem(**b) for b in (indicator.blockers or [])],
            warnings=[WarningItem(**w) for w in (indicator.warnings or [])],
            checked_at=indicator.checked_at,
            checked_by=indicator.checked_by,
        )

    def _aggregate_indicators(
        self, indicators: list[ReadinessIndicator],
    ) -> tuple[str, list[str], list[str]]:
        """Aggregate readiness level, blockers, and warnings from indicators."""
        blockers: list[str] = []
        warnings: list[str] = []
        for ind in indicators:
            blockers.extend(b.get("description", "") for b in (ind.blockers or []))
            warnings.extend(w.get("description", "") for w in (ind.warnings or []))

        if not indicators:
            return "not_ready", blockers, warnings

        levels = [i.readiness_level for i in indicators]
        if "not_ready" in levels:
            level = "not_ready"
        elif "needs_work" in levels:
            level = "needs_work"
        else:
            level = "ready"
        return level, blockers, warnings

    def _build_go_nogo_points(
        self, score: ProposalScore | None, blockers: list[str],
        warnings: list[str], recommendation: str,
    ) -> tuple[list[str], list[str], list[str]]:
        """Build strengths, risks, and next steps lists."""
        strengths: list[str] = []
        risks: list[str] = []
        next_steps: list[str] = []

        if score:
            for f in score.factors:
                label = f.factor_type.replace("_", " ")
                if f.raw_score >= 80:
                    strengths.append(f"Strong {label}: {f.raw_score}/100")
                elif f.raw_score < 60:
                    risks.append(f"Weak {label}: {f.raw_score}/100")

        if blockers:
            risks.extend(blockers[:3])
            next_steps.append("Address all blocking issues before proceeding")
        if warnings:
            next_steps.append(f"Review and address {len(warnings)} warnings")
        if not next_steps:
            if recommendation == "Proceed":
                next_steps.append("Submit proposal as planned")
            else:
                next_steps.append("Review detailed scoring report for improvements")
        return strengths[:5], risks[:5], next_steps[:5]

    async def get_go_nogo_summary(self, proposal_id: str) -> GoNoGoSummary:
        """Generate go/no-go decision summary."""
        score = await self._scoring_repo.get_latest_score(proposal_id)
        indicators = await self._readiness_repo.get_all_for_proposal(proposal_id)

        overall_score = score.overall_score if score else 0
        readiness_level, blockers, warnings = self._aggregate_indicators(indicators)

        if overall_score >= 70 and readiness_level == "ready":
            recommendation = "Proceed"
        elif overall_score >= 50 and readiness_level != "not_ready":
            recommendation = "Proceed with caution"
        else:
            recommendation = "Do not proceed"

        strengths, risks, next_steps = self._build_go_nogo_points(
            score, blockers, warnings, recommendation,
        )

        return GoNoGoSummary(
            proposal_id=proposal_id, overall_score=overall_score,
            readiness_level=readiness_level, recommendation=recommendation,
            key_strengths=strengths, key_risks=risks, next_steps=next_steps,
        )
