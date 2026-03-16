"""Compliance domain models."""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from govproposal.db.base import Base


def _utc_now() -> datetime:
    """Return current UTC datetime."""
    return datetime.now(timezone.utc)


class ComplianceStatus(str, Enum):
    """Status of a compliance item."""
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    PARTIAL = "partial"
    NOT_APPLICABLE = "not_applicable"
    PENDING_REVIEW = "pending_review"


class ComplianceFramework(str, Enum):
    """Regulatory framework."""
    FAR = "far"
    DFARS = "dfars"
    NIST_800_171 = "nist_800_171"
    CMMC = "cmmc"
    ITAR = "itar"
    EAR = "ear"
    OTHER = "other"


class CertificationType(str, Enum):
    """Types of organizational certifications."""
    SAM = "sam"
    CAGE = "cage"
    UEI = "uei"
    GSA = "gsa"
    CMMC = "cmmc"
    SBA_8A = "sba_8a"
    HUBZONE = "hubzone"
    SDVOSB = "sdvosb"
    WOSB = "wosb"


class CMMCLevel(str, Enum):
    """CMMC maturity levels."""
    LEVEL_1 = "level_1"
    LEVEL_2 = "level_2"
    LEVEL_3 = "level_3"


class ComplianceItem(Base):
    """FAR/DFARS clause tracking."""

    __tablename__ = "compliance_items"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    organization_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    framework: Mapped[str] = mapped_column(String(50), nullable=False)
    clause_number: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    status: Mapped[str] = mapped_column(
        String(50), default=ComplianceStatus.PENDING_REVIEW.value, nullable=False
    )
    evidence_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    due_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utc_now, onupdate=_utc_now, nullable=False
    )


class Certification(Base):
    """Organizational registration/certification tracking."""

    __tablename__ = "certifications"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    organization_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    certification_type: Mapped[str] = mapped_column(String(50), nullable=False)
    identifier: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    status: Mapped[str] = mapped_column(
        String(50), default=ComplianceStatus.PENDING_REVIEW.value, nullable=False
    )
    issued_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    expiry_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utc_now, onupdate=_utc_now, nullable=False
    )


class CMMCAssessment(Base):
    """CMMC self-assessment tracking."""

    __tablename__ = "cmmc_assessments"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    organization_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    target_level: Mapped[str] = mapped_column(String(20), nullable=False)
    total_controls: Mapped[int] = mapped_column(default=0, nullable=False)
    implemented_controls: Mapped[int] = mapped_column(default=0, nullable=False)
    partially_implemented: Mapped[int] = mapped_column(default=0, nullable=False)
    not_implemented: Mapped[int] = mapped_column(default=0, nullable=False)
    findings_count: Mapped[int] = mapped_column(default=0, nullable=False)
    assessment_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utc_now, onupdate=_utc_now, nullable=False
    )
