"""Add market column to proposals and backfill from linked opportunity.

Revision ID: 014_proposal_market
Revises: 013_opp_market
Create Date: 2026-05-27
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "014_proposal_market"
down_revision: Union[str, None] = "013_opp_market"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "proposals",
        sa.Column(
            "market",
            sa.String(20),
            nullable=False,
            server_default="federal",
        ),
    )
    op.create_index("ix_proposals_market", "proposals", ["market"])

    # Backfill: for proposals linked to an opportunity, inherit the
    # opportunity's market. Proposals without opportunity_id stay 'federal'.
    op.execute(
        """
        UPDATE proposals AS p
        SET market = o.market
        FROM opportunities AS o
        WHERE p.opportunity_id IS NOT NULL
          AND p.opportunity_id = o.id
          AND o.market <> 'federal'
        """
    )


def downgrade() -> None:
    op.drop_index("ix_proposals_market", table_name="proposals")
    op.drop_column("proposals", "market")
