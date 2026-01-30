"""Scoring models - proposal scores, benchmarks, readiness

Revision ID: 003_scoring_models
Revises: 002_security_models
Create Date: 2026-01-29

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "003_scoring_models"
down_revision: Union[str, None] = "002_security_models"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Proposal scores table
    op.create_table(
        "proposal_scores",
        sa.Column("id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("proposal_id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("score_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("overall_score", sa.Integer(), nullable=False),
        sa.Column("confidence_level", sa.String(20), nullable=False),
        sa.Column("ai_model_used", sa.String(100), nullable=True),
        sa.Column("created_by", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_proposal_scores_proposal_id", "proposal_scores", ["proposal_id"])

    # Score factors table
    op.create_table(
        "score_factors",
        sa.Column("id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column(
            "proposal_score_id", postgresql.UUID(as_uuid=False), nullable=False
        ),
        sa.Column("factor_type", sa.String(50), nullable=False),
        sa.Column("factor_weight", sa.Float(), nullable=False),
        sa.Column("raw_score", sa.Integer(), nullable=False),
        sa.Column("weighted_score", sa.Float(), nullable=False),
        sa.Column("evidence_summary", sa.Text(), nullable=True),
        sa.Column("improvement_suggestions", postgresql.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["proposal_score_id"], ["proposal_scores.id"], ondelete="CASCADE"
        ),
    )

    # Score explanations table
    op.create_table(
        "score_explanations",
        sa.Column("id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column(
            "proposal_score_id", postgresql.UUID(as_uuid=False), nullable=False
        ),
        sa.Column("section", sa.String(100), nullable=False),
        sa.Column("explanation_text", sa.Text(), nullable=False),
        sa.Column("supporting_evidence", postgresql.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["proposal_score_id"], ["proposal_scores.id"], ondelete="CASCADE"
        ),
    )

    # Proposal benchmarks table
    op.create_table(
        "proposal_benchmarks",
        sa.Column("id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("proposal_id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("benchmark_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("completeness_score", sa.Integer(), nullable=False),
        sa.Column("technical_depth_score", sa.Integer(), nullable=False),
        sa.Column("compliance_score", sa.Integer(), nullable=False),
        sa.Column("org_percentile", sa.Integer(), nullable=True),
        sa.Column("org_avg_at_stage", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_proposal_benchmarks_proposal_id", "proposal_benchmarks", ["proposal_id"]
    )

    # Readiness indicators table
    op.create_table(
        "readiness_indicators",
        sa.Column("id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("proposal_id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("team_type", sa.String(20), nullable=False),
        sa.Column("readiness_score", sa.Integer(), nullable=False),
        sa.Column("readiness_level", sa.String(20), nullable=False),
        sa.Column("blockers", postgresql.JSON(), nullable=True),
        sa.Column("warnings", postgresql.JSON(), nullable=True),
        sa.Column("checked_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("checked_by", postgresql.UUID(as_uuid=False), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_readiness_indicators_proposal_id", "readiness_indicators", ["proposal_id"]
    )


def downgrade() -> None:
    op.drop_table("readiness_indicators")
    op.drop_table("proposal_benchmarks")
    op.drop_table("score_explanations")
    op.drop_table("score_factors")
    op.drop_table("proposal_scores")
