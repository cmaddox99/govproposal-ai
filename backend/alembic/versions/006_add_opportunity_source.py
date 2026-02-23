"""Add source field to opportunities table.

Revision ID: 006_add_opp_source
Revises: 005_org_caps_past_perf
Create Date: 2026-02-22
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "006_add_opp_source"
down_revision: Union[str, None] = "005_org_caps_past_perf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "opportunities",
        sa.Column("source", sa.String(50), nullable=False, server_default="sam_gov"),
    )
    op.create_index("ix_opportunities_source", "opportunities", ["source"])


def downgrade() -> None:
    op.drop_index("ix_opportunities_source", table_name="opportunities")
    op.drop_column("opportunities", "source")
