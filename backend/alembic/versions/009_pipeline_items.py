"""Add pipeline_items table.

Revision ID: 009_pipeline
Revises: 008_notifications
Create Date: 2026-05-17
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision: str = "009_pipeline"
down_revision: Union[str, None] = "008_notifications"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "pipeline_items",
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
        sa.Column(
            "proposal_id",
            UUID(as_uuid=False),
            sa.ForeignKey("proposals.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("status", sa.String(20), nullable=False, server_default="active", index=True),
        sa.Column("dollar_value_text", sa.String(100), nullable=True),
        sa.Column("questions_due_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("proposal_due_date_override", sa.DateTime(timezone=True), nullable=True),
        sa.Column("contact_name_override", sa.String(255), nullable=True),
        sa.Column("contact_email_override", sa.String(255), nullable=True),
        sa.Column("has_rfp", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("has_ppqs", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("has_resume", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("has_price", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("has_details", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("archive_status", sa.String(20), nullable=True),
        sa.Column("no_bid_reason", sa.Text, nullable=True),
        sa.Column("match_score", sa.Integer, nullable=True),
        sa.Column("match_tier", sa.String(10), nullable=True),
        sa.Column("match_breakdown", sa.Text, nullable=True),
        sa.Column(
            "created_by",
            UUID(as_uuid=False),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("notes", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_pipeline_items_org_status",
        "pipeline_items",
        ["organization_id", "status"],
    )
    op.create_unique_constraint(
        "uq_pipeline_org_opp",
        "pipeline_items",
        ["organization_id", "opportunity_id"],
    )

    # Backfill: normalize existing opportunity set_aside_type values so the
    # frontend filter (which uses canonical codes like 'sba', 'wosb') matches
    # historical SAM.gov text (e.g. 'Total Small Business Set-Aside').
    bind = op.get_bind()
    rows = bind.execute(sa.text(
        "SELECT id, set_aside_type FROM opportunities WHERE set_aside_type IS NOT NULL"
    )).fetchall()
    try:
        from govproposal.pipeline.service import normalize_set_aside
        for row in rows:
            normalized = normalize_set_aside(row[1])
            if normalized and normalized != row[1]:
                bind.execute(
                    sa.text("UPDATE opportunities SET set_aside_type = :val WHERE id = :id"),
                    {"val": normalized, "id": row[0]},
                )
    except Exception:
        # Don't block the migration if normalization import fails in some envs
        pass


def downgrade() -> None:
    op.drop_constraint("uq_pipeline_org_opp", "pipeline_items", type_="unique")
    op.drop_index("ix_pipeline_items_org_status", table_name="pipeline_items")
    op.drop_table("pipeline_items")
