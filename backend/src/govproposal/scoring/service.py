"""Service layer for scoring operations."""

import json
from dataclasses import dataclass
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

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
        """Calculate comprehensive relevance score for a proposal.

        Args:
            proposal_id: ID of the proposal to score
            user_id: ID of the user requesting the score
            proposal_data: Optional proposal data (sections, content) for scoring

        Returns:
            ProposalScoreResponse with overall score and factor breakdown
        """
        # Calculate each factor
        factors: list[ScoreFactor] = []

        for factor_type, weight in DEFAULT_SCORE_WEIGHTS.items():
            factor_result = await self._calculate_factor(
                proposal_id, factor_type, proposal_data
            )
            factors.append(
                ScoreFactor(
                    factor_type=factor_type.value,
                    factor_weight=weight,
                    raw_score=factor_result.raw_score,
                    weighted_score=factor_result.raw_score * weight,
                    evidence_summary=factor_result.evidence,
                    improvement_suggestions=factor_result.improvements,
                )
            )

        # Calculate overall score
        overall = sum(f.weighted_score for f in factors)

        # Determine confidence based on data completeness
        confidence = self._determine_confidence(proposal_data, factors)

        # Create and save score
        score = ProposalScore(
            proposal_id=proposal_id,
            overall_score=int(overall),
            confidence_level=confidence,
            ai_model_used=settings.anthropic_model,
            created_by=user_id,
            factors=factors,
        )

        saved_score = await self._repo.create_score(score)

        # Convert to response
        return ProposalScoreResponse(
            id=saved_score.id,
            proposal_id=saved_score.proposal_id,
            score_date=saved_score.score_date,
            overall_score=saved_score.overall_score,
            confidence_level=saved_score.confidence_level,
            ai_model_used=saved_score.ai_model_used,
            created_by=saved_score.created_by,
            created_at=saved_score.created_at,
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
                for f in saved_score.factors
            ],
        )

    async def _calculate_factor(
        self,
        proposal_id: str,
        factor_type: ScoreFactorType,
        proposal_data: dict | None,
    ) -> FactorResult:
        """Calculate individual factor score.

        In production, this would call AI service. For now, returns placeholder.
        """
        # Placeholder scoring logic - in production, would call AI
        if factor_type == ScoreFactorType.COMPLETENESS:
            return await self._score_completeness(proposal_data)
        elif factor_type == ScoreFactorType.TECHNICAL_DEPTH:
            return await self._score_technical_depth(proposal_data)
        elif factor_type == ScoreFactorType.SECTION_L_COMPLIANCE:
            return await self._score_compliance(proposal_data)
        elif factor_type == ScoreFactorType.SECTION_M_ALIGNMENT:
            return await self._score_section_m(proposal_data)
        else:
            return FactorResult(
                raw_score=70,
                evidence="Default scoring - factor not implemented",
                improvements=[],
            )

    async def _score_completeness(self, proposal_data: dict | None) -> FactorResult:
        """Score proposal completeness."""
        # Placeholder - would analyze sections for completeness
        if not proposal_data:
            return FactorResult(
                raw_score=50,
                evidence="No proposal data provided for analysis",
                improvements=[
                    {
                        "action": "Provide proposal content",
                        "details": "Submit proposal sections for scoring",
                        "priority": "high",
                    }
                ],
            )

        # Check for required sections
        sections = proposal_data.get("sections", [])
        required = [
            "executive_summary",
            "technical_approach",
            "management_approach",
            "past_performance",
        ]
        present = [s.get("type") for s in sections if s.get("content")]

        missing = [r for r in required if r not in present]
        completeness = ((len(required) - len(missing)) / len(required)) * 100

        improvements = []
        for section in missing:
            improvements.append(
                {
                    "action": f"Add {section.replace('_', ' ').title()}",
                    "details": f"This required section is missing",
                    "priority": "high",
                }
            )

        return FactorResult(
            raw_score=int(completeness),
            evidence=f"Found {len(present)} of {len(required)} required sections",
            improvements=improvements,
        )

    async def _score_technical_depth(self, proposal_data: dict | None) -> FactorResult:
        """Score technical depth using content analysis."""
        if not proposal_data:
            return FactorResult(
                raw_score=50,
                evidence="No proposal data provided",
                improvements=[],
            )

        # Placeholder technical depth scoring
        return FactorResult(
            raw_score=70,
            evidence="Technical content present but could be more specific",
            improvements=[
                {
                    "action": "Add specific methodologies",
                    "details": "Replace generic statements with concrete approaches",
                    "priority": "medium",
                },
                {
                    "action": "Include technical details",
                    "details": "Add tool names, version numbers, and technical specifications",
                    "priority": "medium",
                },
            ],
        )

    async def _score_compliance(self, proposal_data: dict | None) -> FactorResult:
        """Score Section L compliance."""
        # Placeholder compliance scoring
        return FactorResult(
            raw_score=75,
            evidence="Most format requirements appear to be met",
            improvements=[
                {
                    "action": "Verify page limits",
                    "details": "Confirm all sections are within specified page limits",
                    "priority": "high",
                }
            ],
        )

    async def _score_section_m(self, proposal_data: dict | None) -> FactorResult:
        """Score Section M alignment."""
        # Placeholder Section M scoring
        return FactorResult(
            raw_score=65,
            evidence="Some evaluation factors addressed, others need strengthening",
            improvements=[
                {
                    "action": "Align with evaluation criteria",
                    "details": "Reorganize content to directly address each evaluation factor",
                    "priority": "high",
                }
            ],
        )

    def _determine_confidence(
        self, proposal_data: dict | None, factors: list[ScoreFactor]
    ) -> str:
        """Determine confidence level based on data quality."""
        if not proposal_data:
            return "low"

        sections = proposal_data.get("sections", [])
        if len(sections) >= 4:
            return "high"
        elif len(sections) >= 2:
            return "medium"
        return "low"

    async def get_latest_score(self, proposal_id: str) -> ProposalScoreResponse | None:
        """Get the most recent score for a proposal."""
        score = await self._repo.get_latest_score(proposal_id)
        if not score:
            return None

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

    async def calculate_benchmark(
        self, proposal_id: str, organization_proposal_ids: list[str] | None = None
    ) -> BenchmarkResponse:
        """Calculate benchmark metrics for proposal."""
        # Get latest score
        score = await self._scoring_repo.get_latest_score(proposal_id)

        # Extract factor scores
        completeness = 70
        technical_depth = 70
        compliance = 70

        if score:
            for factor in score.factors:
                if factor.factor_type == ScoreFactorType.COMPLETENESS.value:
                    completeness = factor.raw_score
                elif factor.factor_type == ScoreFactorType.TECHNICAL_DEPTH.value:
                    technical_depth = factor.raw_score
                elif factor.factor_type == ScoreFactorType.SECTION_L_COMPLIANCE.value:
                    compliance = factor.raw_score

        # Calculate org comparison if we have other proposals
        org_percentile = None
        org_avg = None

        if organization_proposal_ids and score:
            stats = await self._scoring_repo.get_org_score_stats(
                "", organization_proposal_ids
            )
            if stats["count"] > 0:
                org_avg = stats["avg_score"]
                # Simple percentile calculation
                if score.overall_score >= stats["max_score"]:
                    org_percentile = 100
                elif score.overall_score <= stats["min_score"]:
                    org_percentile = 0
                else:
                    range_size = stats["max_score"] - stats["min_score"]
                    if range_size > 0:
                        org_percentile = int(
                            (
                                (score.overall_score - stats["min_score"])
                                / range_size
                            )
                            * 100
                        )

        # Create benchmark
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
            id=saved.id,
            proposal_id=saved.proposal_id,
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

    async def get_go_nogo_summary(self, proposal_id: str) -> GoNoGoSummary:
        """Generate go/no-go decision summary."""
        # Get score
        score = await self._scoring_repo.get_latest_score(proposal_id)

        # Get readiness indicators
        indicators = await self._readiness_repo.get_all_for_proposal(proposal_id)

        # Determine overall readiness
        overall_score = score.overall_score if score else 0
        readiness_level = "not_ready"
        all_blockers: list[str] = []
        all_warnings: list[str] = []

        for indicator in indicators:
            if indicator.blockers:
                for b in indicator.blockers:
                    all_blockers.append(b.get("description", ""))
            if indicator.warnings:
                for w in indicator.warnings:
                    all_warnings.append(w.get("description", ""))

        if indicators:
            # Use the most restrictive readiness level
            levels = [i.readiness_level for i in indicators]
            if "not_ready" in levels:
                readiness_level = "not_ready"
            elif "needs_work" in levels:
                readiness_level = "needs_work"
            else:
                readiness_level = "ready"

        # Determine recommendation
        if overall_score >= 70 and readiness_level == "ready":
            recommendation = "Proceed"
        elif overall_score >= 50 and readiness_level != "not_ready":
            recommendation = "Proceed with caution"
        else:
            recommendation = "Do not proceed"

        # Generate key points
        strengths: list[str] = []
        risks: list[str] = []
        next_steps: list[str] = []

        if score:
            for factor in score.factors:
                if factor.raw_score >= 80:
                    strengths.append(
                        f"Strong {factor.factor_type.replace('_', ' ')}: {factor.raw_score}/100"
                    )
                elif factor.raw_score < 60:
                    risks.append(
                        f"Weak {factor.factor_type.replace('_', ' ')}: {factor.raw_score}/100"
                    )

        if all_blockers:
            risks.extend(all_blockers[:3])
            next_steps.append("Address all blocking issues before proceeding")

        if all_warnings:
            next_steps.append(f"Review and address {len(all_warnings)} warnings")

        if not next_steps:
            if recommendation == "Proceed":
                next_steps.append("Submit proposal as planned")
            else:
                next_steps.append("Review detailed scoring report for improvements")

        return GoNoGoSummary(
            proposal_id=proposal_id,
            overall_score=overall_score,
            readiness_level=readiness_level,
            recommendation=recommendation,
            key_strengths=strengths[:5],
            key_risks=risks[:5],
            next_steps=next_steps[:5],
        )
