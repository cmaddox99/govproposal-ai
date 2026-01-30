"""Repository layer for scoring models."""

from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from govproposal.scoring.models import (
    ProposalBenchmark,
    ProposalScore,
    ReadinessIndicator,
    ScoreExplanation,
    ScoreFactor,
)


class ScoringRepository:
    """Repository for proposal score operations."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_score(self, score: ProposalScore) -> ProposalScore:
        """Create a new proposal score with factors."""
        self._session.add(score)
        await self._session.flush()
        await self._session.refresh(score, ["factors", "explanations"])
        return score

    async def get_score_by_id(self, score_id: str) -> ProposalScore | None:
        """Get score by ID with factors."""
        result = await self._session.execute(
            select(ProposalScore)
            .where(ProposalScore.id == score_id)
            .options(selectinload(ProposalScore.factors))
            .options(selectinload(ProposalScore.explanations))
        )
        return result.scalar_one_or_none()

    async def get_latest_score(self, proposal_id: str) -> ProposalScore | None:
        """Get the most recent score for a proposal."""
        result = await self._session.execute(
            select(ProposalScore)
            .where(ProposalScore.proposal_id == proposal_id)
            .order_by(ProposalScore.score_date.desc())
            .limit(1)
            .options(selectinload(ProposalScore.factors))
            .options(selectinload(ProposalScore.explanations))
        )
        return result.scalar_one_or_none()

    async def get_score_history(
        self, proposal_id: str, limit: int = 10
    ) -> list[ProposalScore]:
        """Get score history for a proposal."""
        result = await self._session.execute(
            select(ProposalScore)
            .where(ProposalScore.proposal_id == proposal_id)
            .order_by(ProposalScore.score_date.desc())
            .limit(limit)
            .options(selectinload(ProposalScore.factors))
        )
        return list(result.scalars().all())

    async def add_explanation(
        self, score_id: str, section: str, text: str, evidence: dict | None = None
    ) -> ScoreExplanation:
        """Add an explanation to a score."""
        explanation = ScoreExplanation(
            proposal_score_id=score_id,
            section=section,
            explanation_text=text,
            supporting_evidence=evidence,
        )
        self._session.add(explanation)
        await self._session.flush()
        await self._session.refresh(explanation)
        return explanation

    async def get_org_score_stats(
        self, organization_id: str, proposal_ids: list[str]
    ) -> dict:
        """Get aggregate score statistics for an organization's proposals."""
        if not proposal_ids:
            return {"avg_score": 0, "min_score": 0, "max_score": 0, "count": 0}

        # Get latest score for each proposal
        subquery = (
            select(
                ProposalScore.proposal_id,
                func.max(ProposalScore.score_date).label("max_date"),
            )
            .where(ProposalScore.proposal_id.in_(proposal_ids))
            .group_by(ProposalScore.proposal_id)
            .subquery()
        )

        result = await self._session.execute(
            select(
                func.avg(ProposalScore.overall_score).label("avg_score"),
                func.min(ProposalScore.overall_score).label("min_score"),
                func.max(ProposalScore.overall_score).label("max_score"),
                func.count(ProposalScore.id).label("count"),
            )
            .join(
                subquery,
                (ProposalScore.proposal_id == subquery.c.proposal_id)
                & (ProposalScore.score_date == subquery.c.max_date),
            )
        )
        row = result.one()

        return {
            "avg_score": int(row.avg_score or 0),
            "min_score": int(row.min_score or 0),
            "max_score": int(row.max_score or 0),
            "count": row.count,
        }


class BenchmarkRepository:
    """Repository for benchmark operations."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_benchmark(self, benchmark: ProposalBenchmark) -> ProposalBenchmark:
        """Create a new benchmark."""
        self._session.add(benchmark)
        await self._session.flush()
        await self._session.refresh(benchmark)
        return benchmark

    async def get_latest_benchmark(self, proposal_id: str) -> ProposalBenchmark | None:
        """Get the most recent benchmark for a proposal."""
        result = await self._session.execute(
            select(ProposalBenchmark)
            .where(ProposalBenchmark.proposal_id == proposal_id)
            .order_by(ProposalBenchmark.benchmark_date.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def get_benchmark_history(
        self, proposal_id: str, limit: int = 10
    ) -> list[ProposalBenchmark]:
        """Get benchmark history for a proposal."""
        result = await self._session.execute(
            select(ProposalBenchmark)
            .where(ProposalBenchmark.proposal_id == proposal_id)
            .order_by(ProposalBenchmark.benchmark_date.desc())
            .limit(limit)
        )
        return list(result.scalars().all())


class ReadinessRepository:
    """Repository for readiness indicator operations."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_indicator(
        self, indicator: ReadinessIndicator
    ) -> ReadinessIndicator:
        """Create a new readiness indicator."""
        self._session.add(indicator)
        await self._session.flush()
        await self._session.refresh(indicator)
        return indicator

    async def get_latest_by_team_type(
        self, proposal_id: str, team_type: str
    ) -> ReadinessIndicator | None:
        """Get the most recent readiness indicator for a proposal and team type."""
        result = await self._session.execute(
            select(ReadinessIndicator)
            .where(
                ReadinessIndicator.proposal_id == proposal_id,
                ReadinessIndicator.team_type == team_type,
            )
            .order_by(ReadinessIndicator.checked_at.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def get_all_for_proposal(
        self, proposal_id: str
    ) -> list[ReadinessIndicator]:
        """Get all readiness indicators for a proposal (latest per team type)."""
        # Get latest for each team type
        subquery = (
            select(
                ReadinessIndicator.proposal_id,
                ReadinessIndicator.team_type,
                func.max(ReadinessIndicator.checked_at).label("max_date"),
            )
            .where(ReadinessIndicator.proposal_id == proposal_id)
            .group_by(ReadinessIndicator.proposal_id, ReadinessIndicator.team_type)
            .subquery()
        )

        result = await self._session.execute(
            select(ReadinessIndicator).join(
                subquery,
                (ReadinessIndicator.proposal_id == subquery.c.proposal_id)
                & (ReadinessIndicator.team_type == subquery.c.team_type)
                & (ReadinessIndicator.checked_at == subquery.c.max_date),
            )
        )
        return list(result.scalars().all())
