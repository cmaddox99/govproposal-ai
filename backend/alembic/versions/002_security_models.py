"""Security models - audit logs, incidents, POAM

Revision ID: 002_security_models
Revises: 001_initial_identity
Create Date: 2026-01-29

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "002_security_models"
down_revision: Union[str, None] = "001_initial_identity"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Audit logs table
    op.create_table(
        "audit_logs",
        sa.Column("id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("event_type", sa.String(50), nullable=False),
        sa.Column("event_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("actor_id", postgresql.UUID(as_uuid=False), nullable=True),
        sa.Column("actor_type", sa.String(20), nullable=False, default="user"),
        sa.Column("actor_email", sa.String(255), nullable=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=False), nullable=True),
        sa.Column("resource_type", sa.String(50), nullable=True),
        sa.Column("resource_id", postgresql.UUID(as_uuid=False), nullable=True),
        sa.Column("action", sa.String(100), nullable=False),
        sa.Column("outcome", sa.String(20), nullable=False, default="success"),
        sa.Column("ip_address", sa.String(45), nullable=True),
        sa.Column("user_agent", sa.String(500), nullable=True),
        sa.Column("details", postgresql.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_audit_logs_event_type", "audit_logs", ["event_type"])
    op.create_index("ix_audit_logs_event_time", "audit_logs", ["event_time"])
    op.create_index("ix_audit_logs_actor_id", "audit_logs", ["actor_id"])
    op.create_index("ix_audit_logs_organization_id", "audit_logs", ["organization_id"])

    # Security incidents table
    op.create_table(
        "security_incidents",
        sa.Column("id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("incident_number", sa.String(50), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("severity", sa.String(20), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, default="open"),
        sa.Column("category", sa.String(50), nullable=False),
        sa.Column("affected_systems", postgresql.JSON(), nullable=True),
        sa.Column("reported_by", postgresql.UUID(as_uuid=False), nullable=True),
        sa.Column("assigned_to", postgresql.UUID(as_uuid=False), nullable=True),
        sa.Column("detected_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("contained_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("root_cause", sa.Text(), nullable=True),
        sa.Column("remediation_steps", postgresql.JSON(), nullable=True),
        sa.Column("lessons_learned", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("incident_number"),
    )
    op.create_index("ix_security_incidents_category", "security_incidents", ["category"])

    # POAM items table
    op.create_table(
        "poam_items",
        sa.Column("id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("poam_id", sa.String(50), nullable=False),
        sa.Column("weakness_name", sa.String(255), nullable=False),
        sa.Column("weakness_description", sa.Text(), nullable=False),
        sa.Column("control_identifier", sa.String(50), nullable=False),
        sa.Column("point_of_contact", sa.String(255), nullable=True),
        sa.Column("resources_required", sa.Text(), nullable=True),
        sa.Column("scheduled_completion", sa.DateTime(timezone=True), nullable=True),
        sa.Column("milestone_changes", postgresql.JSON(), nullable=True),
        sa.Column("status", sa.String(20), nullable=False, default="open"),
        sa.Column("source_identified", sa.String(100), nullable=True),
        sa.Column("vendor_dependency", sa.Text(), nullable=True),
        sa.Column("comments", sa.Text(), nullable=True),
        sa.Column("risk_level", sa.String(20), nullable=False, default="medium"),
        sa.Column("original_detection_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("poam_id"),
    )


def downgrade() -> None:
    op.drop_table("poam_items")
    op.drop_table("security_incidents")
    op.drop_table("audit_logs")
