"""Opportunity models for SAM.gov integration."""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, String, Text, Integer, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from govproposal.db.base import Base


def _utc_now() -> datetime:
    """Return current UTC datetime."""
    return datetime.now(timezone.utc)


class NoticeType(str, Enum):
    """SAM.gov notice types."""
    PRESOLICITATION = "presolicitation"
    SOLICITATION = "solicitation"
    COMBINED_SYNOPSIS = "combined_synopsis"
    AWARD_NOTICE = "award_notice"
    SOURCES_SOUGHT = "sources_sought"
    SPECIAL_NOTICE = "special_notice"
    SALE_OF_SURPLUS = "sale_of_surplus"
    INTENT_TO_BUNDLE = "intent_to_bundle"
    FAIR_OPPORTUNITY = "fair_opportunity"


class SetAsideType(str, Enum):
    """Set-aside types for small business programs."""
    NONE = "none"
    SBA = "sba"  # Small Business
    SBSA = "sbsa"  # Small Business Set-Aside
    WOSB = "wosb"  # Women-Owned Small Business
    EDWOSB = "edwosb"  # Economically Disadvantaged WOSB
    SDVOSB = "sdvosb"  # Service-Disabled Veteran-Owned
    HUBZONE = "hubzone"  # HUBZone
    EIGHT_A = "8a"  # 8(a) Program


class Opportunity(Base):
    """SAM.gov opportunity model."""

    __tablename__ = "opportunities"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )

    # SAM.gov identifiers
    notice_id: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    solicitation_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)

    # Basic info
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Agency info
    department: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    agency: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    office: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Classification
    notice_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    naics_code: Mapped[Optional[str]] = mapped_column(String(10), nullable=True, index=True)
    naics_description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    psc_code: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)

    # Set-aside info
    set_aside_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    set_aside_description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Dates
    posted_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    response_deadline: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
    archive_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Location
    place_of_performance_city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    place_of_performance_state: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    place_of_performance_country: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Value
    estimated_value: Mapped[Optional[float]] = mapped_column(Numeric(15, 2), nullable=True)

    # Contact info
    primary_contact_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    primary_contact_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    primary_contact_phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # URLs
    sam_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Source tracking
    source: Mapped[str] = mapped_column(
        String(50), nullable=False, default="sam_gov", server_default="sam_gov", index=True
    )

    # Raw data from SAM.gov
    raw_data: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    # Sync tracking
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    last_synced_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utc_now, nullable=False
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utc_now, onupdate=_utc_now, nullable=False
    )
