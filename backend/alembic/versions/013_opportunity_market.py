"""Add market column to opportunities (federal vs sled).

Revision ID: 013_opp_market
Revises: 012_opp_source_doc
Create Date: 2026-05-25
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "013_opp_market"
down_revision: Union[str, None] = "012_opp_source_doc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "opportunities",
        sa.Column(
            "market",
            sa.String(20),
            nullable=False,
            server_default="federal",
        ),
    )
    op.create_index("ix_opportunities_market", "opportunities", ["market"])


def downgrade() -> None:
    op.drop_index("ix_opportunities_market", table_name="opportunities")
    op.drop_column("opportunities", "market")
