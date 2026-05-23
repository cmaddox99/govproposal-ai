"""Pipeline item models.

Represents an opportunity that has been promoted into the pursuit pipeline.
Mirrors the DKW Pipeline Tracker spreadsheet: Active / Archive / No Bid.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, Integer, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from govproposal.db.base import Base


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class PipelineStatus(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    NO_BID = "no_bid"


class MatchTier(str, Enum):
    RED = "red"
    YELLOW = "yellow"
    GREEN = "green"


class ArchiveStatus(str, Enum):
    SUBMITTED = "submitted"
    AWARDED = "awarded"
    LOST = "lost"
    WITHDRAWN = "withdrawn"


class PipelineItem(Base):
    """An opportunity in the active pursuit pipeline."""

    __tablename__ = "pipeline_items"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )

    organization_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    opportunity_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("opportunities.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    proposal_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("proposals.id", ondelete="SET NULL"),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default=PipelineStatus.ACTIVE.value, index=True
    )

    # Spreadsheet text overrides
    dollar_value_text: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    questions_due_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    proposal_due_date_override: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    contact_name_override: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    contact_email_override: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Pipeline Details checkmarks
    has_rfp: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")
    has_ppqs: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")
    has_resume: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")
    has_price: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")
    has_details: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")

    # Archive
    archive_status: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    no_bid_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Match score (0-100) and tier (red/yellow/green)
    match_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    match_tier: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    match_breakdown: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # User tracking
    created_by: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utc_now, onupdate=_utc_now, nullable=False
    )
