"""Add compliance tracking models.

Revision ID: 007_compliance
Revises: 006_add_opp_source
Create Date: 2026-02-23
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision: str = "007_compliance"
down_revision: Union[str, None] = "006_add_opp_source"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Compliance items
    op.create_table(
        "compliance_items",
        sa.Column("id", UUID(as_uuid=False), primary_key=True),
        sa.Column("organization_id", UUID(as_uuid=False), sa.ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("framework", sa.String(50), nullable=False),
        sa.Column("clause_number", sa.String(50), nullable=False),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("status", sa.String(50), nullable=False, server_default="pending_review"),
        sa.Column("evidence_notes", sa.Text, nullable=True),
        sa.Column("due_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    # Certifications
    op.create_table(
        "certifications",
        sa.Column("id", UUID(as_uuid=False), primary_key=True),
        sa.Column("organization_id", UUID(as_uuid=False), sa.ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("certification_type", sa.String(50), nullable=False),
        sa.Column("identifier", sa.String(100), nullable=True),
        sa.Column("status", sa.String(50), nullable=False, server_default="pending_review"),
        sa.Column("issued_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("expiry_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("notes", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    # CMMC assessments
    op.create_table(
        "cmmc_assessments",
        sa.Column("id", UUID(as_uuid=False), primary_key=True),
        sa.Column("organization_id", UUID(as_uuid=False), sa.ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("target_level", sa.String(20), nullable=False),
        sa.Column("total_controls", sa.Integer, nullable=False, server_default="0"),
        sa.Column("implemented_controls", sa.Integer, nullable=False, server_default="0"),
        sa.Column("partially_implemented", sa.Integer, nullable=False, server_default="0"),
        sa.Column("not_implemented", sa.Integer, nullable=False, server_default="0"),
        sa.Column("findings_count", sa.Integer, nullable=False, server_default="0"),
        sa.Column("assessment_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("notes", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("cmmc_assessments")
    op.drop_table("certifications")
    op.drop_table("compliance_items")
