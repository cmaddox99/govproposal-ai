"""Analytics service — read-only aggregate queries."""

from datetime import datetime, timedelta, timezone

from sqlalchemy import extract, func, select, case, cast, String
from sqlalchemy.ext.asyncio import AsyncSession

from govproposal.opportunities.models import Opportunity
from govproposal.proposals.models import Proposal, ProposalStatus
from govproposal.scoring.models import ProposalScore


class AnalyticsService:
    """Read-only analytics over existing tables."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_dashboard_metrics(self, organization_id: str) -> dict:
        """Active proposals, new opportunities (30d), win rate, pending deadlines."""
        now = datetime.now(timezone.utc)
        thirty_days_ago = now - timedelta(days=30)

        # Active proposals (not submitted/awarded/not_awarded/cancelled)
        active_statuses = [
            ProposalStatus.DRAFT.value,
            ProposalStatus.IN_PROGRESS.value,
            ProposalStatus.REVIEW.value,
        ]
        active_q = select(func.count()).select_from(Proposal).where(
            Proposal.organization_id == organization_id,
            Proposal.status.in_(active_statuses),
        )
        active_count = (await self._session.execute(active_q)).scalar_one()

        # New opportunities in last 30 days
        opp_q = select(func.count()).select_from(Opportunity).where(
            Opportunity.created_at >= thirty_days_ago,
            Opportunity.is_active.is_(True),
        )
        new_opportunities = (await self._session.execute(opp_q)).scalar_one()

        # Win rate
        awarded_q = select(func.count()).select_from(Proposal).where(
            Proposal.organization_id == organization_id,
            Proposal.status == ProposalStatus.AWARDED.value,
        )
        awarded_count = (await self._session.execute(awarded_q)).scalar_one()

        decided_q = select(func.count()).select_from(Proposal).where(
            Proposal.organization_id == organization_id,
            Proposal.status.in_([ProposalStatus.AWARDED.value, ProposalStatus.NOT_AWARDED.value]),
        )
        decided_count = (await self._session.execute(decided_q)).scalar_one()

        win_rate = round((awarded_count / decided_count * 100), 1) if decided_count > 0 else 0.0

        # Pending deadlines (proposals with due_date in next 14 days)
        deadline_cutoff = now + timedelta(days=14)
        deadline_q = select(func.count()).select_from(Proposal).where(
            Proposal.organization_id == organization_id,
            Proposal.status.in_(active_statuses),
            Proposal.due_date.isnot(None),
            Proposal.due_date <= deadline_cutoff,
            Proposal.due_date >= now,
        )
        pending_deadlines = (await self._session.execute(deadline_q)).scalar_one()

        return {
            "active_proposals": active_count,
            "new_opportunities": new_opportunities,
            "win_rate": win_rate,
            "pending_deadlines": pending_deadlines,
        }

    async def get_pipeline_breakdown(self, organization_id: str) -> list[dict]:
        """Proposals grouped by status."""
        q = (
            select(Proposal.status, func.count().label("count"))
            .where(Proposal.organization_id == organization_id)
            .group_by(Proposal.status)
        )
        result = await self._session.execute(q)
        return [{"status": row.status, "count": row.count} for row in result.all()]

    async def get_recent_proposals(self, organization_id: str, limit: int = 5) -> list[dict]:
        """Last N updated proposals."""
        q = (
            select(Proposal)
            .where(Proposal.organization_id == organization_id)
            .order_by(Proposal.updated_at.desc())
            .limit(limit)
        )
        result = await self._session.execute(q)
        proposals = result.scalars().all()
        return [
            {
                "id": p.id,
                "title": p.title,
                "agency": p.agency,
                "status": p.status,
                "estimated_value": p.estimated_value,
                "due_date": p.due_date.isoformat() if p.due_date else None,
                "updated_at": p.updated_at.isoformat(),
            }
            for p in proposals
        ]

    async def get_analytics_overview(self, organization_id: str) -> dict:
        """Full analytics overview."""
        metrics = await self.get_dashboard_metrics(organization_id)
        pipeline = await self.get_pipeline_breakdown(organization_id)
        recent = await self.get_recent_proposals(organization_id)

        # Total contract value (awarded proposals)
        value_q = select(func.coalesce(func.sum(Proposal.awarded_value), 0.0)).where(
            Proposal.organization_id == organization_id,
            Proposal.status == ProposalStatus.AWARDED.value,
        )
        total_value = float((await self._session.execute(value_q)).scalar_one())

        # Total submitted
        submitted_q = select(func.count()).select_from(Proposal).where(
            Proposal.organization_id == organization_id,
            Proposal.status.in_([
                ProposalStatus.SUBMITTED.value,
                ProposalStatus.AWARDED.value,
                ProposalStatus.NOT_AWARDED.value,
            ]),
        )
        total_submitted = (await self._session.execute(submitted_q)).scalar_one()

        # Average score
        score_q = (
            select(func.avg(ProposalScore.overall_score))
            .join(Proposal, ProposalScore.proposal_id == Proposal.id)
            .where(Proposal.organization_id == organization_id)
        )
        avg_score = (await self._session.execute(score_q)).scalar_one()
        avg_score = round(float(avg_score), 1) if avg_score else 0.0

        return {
            **metrics,
            "pipeline": pipeline,
            "recent_proposals": recent,
            "total_contract_value": total_value,
            "total_submitted": total_submitted,
            "average_score": avg_score,
        }

    async def get_monthly_activity(self, organization_id: str, months: int = 6) -> list[dict]:
        """Proposal activity by month for the last N months."""
        now = datetime.now(timezone.utc)
        cutoff = now - timedelta(days=months * 30)

        # Get proposals created in date range
        q = (
            select(
                extract("year", Proposal.created_at).label("year"),
                extract("month", Proposal.created_at).label("month"),
                func.count().label("created"),
                func.count(case(
                    (Proposal.status.in_([
                        ProposalStatus.SUBMITTED.value,
                        ProposalStatus.AWARDED.value,
                        ProposalStatus.NOT_AWARDED.value,
                    ]), 1),
                )).label("submitted"),
                func.count(case(
                    (Proposal.status == ProposalStatus.AWARDED.value, 1),
                )).label("awarded"),
            )
            .where(
                Proposal.organization_id == organization_id,
                Proposal.created_at >= cutoff,
            )
            .group_by(
                extract("year", Proposal.created_at),
                extract("month", Proposal.created_at),
            )
            .order_by(
                extract("year", Proposal.created_at),
                extract("month", Proposal.created_at),
            )
        )
        result = await self._session.execute(q)
        rows = result.all()

        # Also get average scores per month
        score_q = (
            select(
                extract("year", ProposalScore.created_at).label("year"),
                extract("month", ProposalScore.created_at).label("month"),
                func.avg(ProposalScore.overall_score).label("avg_score"),
            )
            .join(Proposal, ProposalScore.proposal_id == Proposal.id)
            .where(
                Proposal.organization_id == organization_id,
                ProposalScore.created_at >= cutoff,
            )
            .group_by(
                extract("year", ProposalScore.created_at),
                extract("month", ProposalScore.created_at),
            )
        )
        score_result = await self._session.execute(score_q)
        score_map = {
            (int(r.year), int(r.month)): round(float(r.avg_score), 1)
            for r in score_result.all()
        }

        month_names = [
            "Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
        ]

        return [
            {
                "month": f"{month_names[int(r.month) - 1]} {int(r.year)}",
                "proposals_created": r.created,
                "proposals_submitted": r.submitted,
                "proposals_awarded": r.awarded,
                "avg_score": score_map.get((int(r.year), int(r.month))),
            }
            for r in rows
        ]

    async def get_top_agencies(self, organization_id: str, limit: int = 5) -> list[dict]:
        """Top agencies by proposal count."""
        q = (
            select(
                Proposal.agency,
                func.count().label("count"),
                func.count(case(
                    (Proposal.status == ProposalStatus.AWARDED.value, 1),
                )).label("awarded"),
            )
            .where(
                Proposal.organization_id == organization_id,
                Proposal.agency.isnot(None),
            )
            .group_by(Proposal.agency)
            .order_by(func.count().desc())
            .limit(limit)
        )
        result = await self._session.execute(q)
        return [
            {"agency": r.agency, "count": r.count, "awarded": r.awarded}
            for r in result.all()
        ]

    async def get_score_trends(self, organization_id: str, limit: int = 5) -> list[dict]:
        """Score history for recently scored proposals."""
        # Get proposals with multiple scores
        proposals_q = (
            select(Proposal.id, Proposal.title)
            .where(Proposal.organization_id == organization_id)
            .order_by(Proposal.updated_at.desc())
            .limit(limit)
        )
        proposals = (await self._session.execute(proposals_q)).all()

        trends = []
        for p in proposals:
            scores_q = (
                select(
                    ProposalScore.overall_score,
                    ProposalScore.created_at,
                )
                .where(ProposalScore.proposal_id == p.id)
                .order_by(ProposalScore.created_at.asc())
            )
            scores = (await self._session.execute(scores_q)).all()
            if scores:
                trends.append({
                    "proposal_id": p.id,
                    "title": p.title,
                    "scores": [
                        {
                            "score": s.overall_score,
                            "date": s.created_at.isoformat(),
                        }
                        for s in scores
                    ],
                })
        return trends

    async def get_trends(self, organization_id: str) -> dict:
        """Full trends data."""
        monthly = await self.get_monthly_activity(organization_id)
        score_trends = await self.get_score_trends(organization_id)
        top_agencies = await self.get_top_agencies(organization_id)
        return {
            "monthly_activity": monthly,
            "score_trends": score_trends,
            "top_agencies": top_agencies,
        }
