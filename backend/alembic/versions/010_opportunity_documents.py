"""Add opportunity_documents table.

Revision ID: 010_opp_docs
Revises: 009_pipeline
Create Date: 2026-05-21
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision: str = "010_opp_docs"
down_revision: Union[str, None] = "009_pipeline"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "opportunity_documents",
        sa.Column("id", UUID(as_uuid=False), primary_key=True),
        sa.Column(
            "organization_id",
            UUID(as_uuid=False),
            sa.ForeignKey("organizations.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column(
            "opportunity_id",
            UUID(as_uuid=False),
            sa.ForeignKey("opportunities.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("filename", sa.String(255), nullable=False),
        sa.Column("stored_path", sa.String(500), nullable=False),
        sa.Column("content_type", sa.String(100), nullable=True),
        sa.Column("size_bytes", sa.Integer, nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column(
            "uploaded_by",
            UUID(as_uuid=False),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("uploaded_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_opp_docs_org_opportunity",
        "opportunity_documents",
        ["organization_id", "opportunity_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_opp_docs_org_opportunity", table_name="opportunity_documents")
    op.drop_table("opportunity_documents")
