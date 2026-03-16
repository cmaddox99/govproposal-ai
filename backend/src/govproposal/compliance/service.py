"""Service layer for compliance operations."""

from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from govproposal.compliance.models import ComplianceStatus
from govproposal.compliance.repository import (
    CertificationRepository,
    CMMCAssessmentRepository,
    ComplianceItemRepository,
)


class ComplianceService:
    """Service for compliance tracking operations."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._item_repo = ComplianceItemRepository(session)
        self._cert_repo = CertificationRepository(session)
        self._cmmc_repo = CMMCAssessmentRepository(session)

    async def get_compliance_summary(self, organization_id: str) -> dict:
        """Calculate compliance summary with percentages."""
        items, total_items = await self._item_repo.list_by_org(
            organization_id, limit=1000
        )
        certs, total_certs = await self._cert_repo.list_by_org(
            organization_id, limit=1000
        )

        compliant_items = sum(
            1 for i in items if i.status == ComplianceStatus.COMPLIANT.value
        )
        partial_items = sum(
            1 for i in items if i.status == ComplianceStatus.PARTIAL.value
        )
        non_compliant_items = sum(
            1 for i in items if i.status == ComplianceStatus.NON_COMPLIANT.value
        )

        active_certs = sum(
            1 for c in certs if c.status == ComplianceStatus.COMPLIANT.value
        )

        overall_pct = 0.0
        if total_items > 0:
            overall_pct = round(
                (compliant_items + partial_items * 0.5) / total_items * 100, 1
            )

        return {
            "overall_compliance_percentage": overall_pct,
            "total_items": total_items,
            "compliant_items": compliant_items,
            "partial_items": partial_items,
            "non_compliant_items": non_compliant_items,
            "action_required": non_compliant_items + (total_items - compliant_items - partial_items - non_compliant_items),
            "total_certifications": total_certs,
            "active_certifications": active_certs,
        }

    async def get_expiring_certifications(
        self, organization_id: str, days_ahead: int = 90
    ) -> list:
        """Get certifications expiring within given days."""
        certs, _ = await self._cert_repo.list_by_org(organization_id, limit=1000)
        cutoff = datetime.now(timezone.utc) + timedelta(days=days_ahead)
        return [
            c for c in certs
            if c.expiry_date and c.expiry_date <= cutoff
        ]
