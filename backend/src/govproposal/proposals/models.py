"""Proposal models."""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional, List
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, String, Text, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from govproposal.db.base import Base


def _utc_now() -> datetime:
    """Return current UTC datetime."""
    return datetime.now(timezone.utc)


class ProposalStatus(str, Enum):
    """Proposal status values."""
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    SUBMITTED = "submitted"
    AWARDED = "awarded"
    NOT_AWARDED = "not_awarded"
    CANCELLED = "cancelled"


class Proposal(Base):
    """Proposal model."""

    __tablename__ = "proposals"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )

    # Organization (tenant)
    organization_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Linked opportunity (optional)
    opportunity_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("opportunities.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # Basic info
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        String(50), default=ProposalStatus.DRAFT.value, nullable=False, index=True
    )

    # Solicitation info (copied from opportunity or manual entry)
    solicitation_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    agency: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    naics_code: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)

    # Dates
    due_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    submitted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Value
    estimated_value: Mapped[Optional[float]] = mapped_column(nullable=True)
    proposed_value: Mapped[Optional[float]] = mapped_column(nullable=True)
    awarded_value: Mapped[Optional[float]] = mapped_column(nullable=True)

    # Content sections (JSON for flexibility)
    executive_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    technical_approach: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    management_approach: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    past_performance: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    pricing_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Additional sections stored as JSON
    sections: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    # AI-generated content tracking
    ai_generated_content: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    # User tracking
    created_by: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    updated_by: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utc_now, onupdate=_utc_now, nullable=False
    )
