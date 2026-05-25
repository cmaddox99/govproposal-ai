"""Add source-document columns to opportunities.

Revision ID: 012_opp_source_doc
Revises: 011_pp_source_doc
Create Date: 2026-05-23
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "012_opp_source_doc"
down_revision: Union[str, None] = "011_pp_source_doc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "opportunities",
        sa.Column("source_document_path", sa.String(500), nullable=True),
    )
    op.add_column(
        "opportunities",
        sa.Column("source_document_filename", sa.String(255), nullable=True),
    )
    op.add_column(
        "opportunities",
        sa.Column("source_document_content_type", sa.String(100), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("opportunities", "source_document_content_type")
    op.drop_column("opportunities", "source_document_filename")
    op.drop_column("opportunities", "source_document_path")
