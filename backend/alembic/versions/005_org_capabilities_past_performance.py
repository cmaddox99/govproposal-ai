"""Organization capabilities and past performance

Revision ID: 005_org_caps_past_perf
Revises: 004_opportunities_proposals
Create Date: 2026-02-21

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '005_org_caps_past_perf'
down_revision: Union[str, None] = '004_opportunities_proposals'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add capabilities fields to organizations table
    op.add_column('organizations', sa.Column('capabilities_summary', sa.Text(), nullable=True))
    op.add_column('organizations', sa.Column('capabilities', postgresql.JSONB(), nullable=True))

    # Create org_past_performances table
    op.create_table(
        'org_past_performances',
        sa.Column('id', postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column('organization_id', postgresql.UUID(as_uuid=False),
                  sa.ForeignKey('organizations.id', ondelete='CASCADE'),
                  nullable=False, index=True),
        sa.Column('contract_name', sa.String(500), nullable=False),
        sa.Column('agency', sa.String(255), nullable=True),
        sa.Column('contract_number', sa.String(100), nullable=True),
        sa.Column('contract_value', sa.Numeric(15, 2), nullable=True),
        sa.Column('period_of_performance_start', sa.DateTime(timezone=True), nullable=True),
        sa.Column('period_of_performance_end', sa.DateTime(timezone=True), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('relevance_tags', postgresql.JSONB(), nullable=True),
        sa.Column('contact_name', sa.String(255), nullable=True),
        sa.Column('contact_email', sa.String(255), nullable=True),
        sa.Column('contact_phone', sa.String(50), nullable=True),
        sa.Column('performance_rating', sa.String(50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('org_past_performances')
    op.drop_column('organizations', 'capabilities')
    op.drop_column('organizations', 'capabilities_summary')
