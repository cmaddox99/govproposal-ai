"""Repository layer for compliance models."""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from govproposal.compliance.models import CMMCAssessment, Certification, ComplianceItem


class ComplianceItemRepository:
    """Repository for compliance item operations."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, item: ComplianceItem) -> ComplianceItem:
        self._session.add(item)
        await self._session.flush()
        await self._session.refresh(item)
        return item

    async def get_by_id(self, item_id: str) -> ComplianceItem | None:
        result = await self._session.execute(
            select(ComplianceItem).where(ComplianceItem.id == item_id)
        )
        return result.scalar_one_or_none()

    async def update(self, item: ComplianceItem) -> ComplianceItem:
        await self._session.flush()
        await self._session.refresh(item)
        return item

    async def list_by_org(
        self,
        organization_id: str,
        framework: str | None = None,
        status: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[list[ComplianceItem], int]:
        query = select(ComplianceItem).where(
            ComplianceItem.organization_id == organization_id
        )
        if framework:
            query = query.where(ComplianceItem.framework == framework)
        if status:
            query = query.where(ComplianceItem.status == status)

        count_query = select(func.count()).select_from(query.subquery())
        count_result = await self._session.execute(count_query)
        total = count_result.scalar_one()

        query = query.order_by(ComplianceItem.created_at.desc()).limit(limit).offset(offset)
        result = await self._session.execute(query)
        items = list(result.scalars().all())
        return items, total


class CertificationRepository:
    """Repository for certification operations."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, cert: Certification) -> Certification:
        self._session.add(cert)
        await self._session.flush()
        await self._session.refresh(cert)
        return cert

    async def get_by_id(self, cert_id: str) -> Certification | None:
        result = await self._session.execute(
            select(Certification).where(Certification.id == cert_id)
        )
        return result.scalar_one_or_none()

    async def update(self, cert: Certification) -> Certification:
        await self._session.flush()
        await self._session.refresh(cert)
        return cert

    async def list_by_org(
        self,
        organization_id: str,
        certification_type: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[list[Certification], int]:
        query = select(Certification).where(
            Certification.organization_id == organization_id
        )
        if certification_type:
            query = query.where(Certification.certification_type == certification_type)

        count_query = select(func.count()).select_from(query.subquery())
        count_result = await self._session.execute(count_query)
        total = count_result.scalar_one()

        query = query.order_by(Certification.created_at.desc()).limit(limit).offset(offset)
        result = await self._session.execute(query)
        certs = list(result.scalars().all())
        return certs, total


class CMMCAssessmentRepository:
    """Repository for CMMC assessment operations."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, assessment: CMMCAssessment) -> CMMCAssessment:
        self._session.add(assessment)
        await self._session.flush()
        await self._session.refresh(assessment)
        return assessment

    async def get_by_id(self, assessment_id: str) -> CMMCAssessment | None:
        result = await self._session.execute(
            select(CMMCAssessment).where(CMMCAssessment.id == assessment_id)
        )
        return result.scalar_one_or_none()

    async def list_by_org(
        self,
        organization_id: str,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[list[CMMCAssessment], int]:
        query = select(CMMCAssessment).where(
            CMMCAssessment.organization_id == organization_id
        )

        count_query = select(func.count()).select_from(query.subquery())
        count_result = await self._session.execute(count_query)
        total = count_result.scalar_one()

        query = query.order_by(CMMCAssessment.created_at.desc()).limit(limit).offset(offset)
        result = await self._session.execute(query)
        assessments = list(result.scalars().all())
        return assessments, total
