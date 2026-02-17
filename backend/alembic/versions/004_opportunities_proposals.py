"""Opportunities and Proposals models

Revision ID: 004_opportunities_proposals
Revises: 003_scoring_models
Create Date: 2026-02-08

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '004_opportunities_proposals'
down_revision: Union[str, None] = '003_scoring_models'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add new columns to organizations table
    op.add_column('organizations', sa.Column('contact_email', sa.String(255), nullable=True))
    op.add_column('organizations', sa.Column('phone', sa.String(50), nullable=True))
    op.add_column('organizations', sa.Column('address', sa.Text(), nullable=True))
    op.add_column('organizations', sa.Column('uei_number', sa.String(20), nullable=True))
    op.add_column('organizations', sa.Column('cage_code', sa.String(10), nullable=True))
    op.add_column('organizations', sa.Column('duns_number', sa.String(20), nullable=True))
    op.add_column('organizations', sa.Column('naics_codes', sa.Text(), nullable=True))

    # Create opportunities table
    op.create_table(
        'opportunities',
        sa.Column('id', postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column('notice_id', sa.String(100), nullable=False, unique=True, index=True),
        sa.Column('solicitation_number', sa.String(100), nullable=True, index=True),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('department', sa.String(255), nullable=True),
        sa.Column('agency', sa.String(255), nullable=True),
        sa.Column('office', sa.String(255), nullable=True),
        sa.Column('notice_type', sa.String(50), nullable=False, index=True),
        sa.Column('naics_code', sa.String(10), nullable=True, index=True),
        sa.Column('naics_description', sa.String(255), nullable=True),
        sa.Column('psc_code', sa.String(10), nullable=True),
        sa.Column('set_aside_type', sa.String(50), nullable=True),
        sa.Column('set_aside_description', sa.String(255), nullable=True),
        sa.Column('posted_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('response_deadline', sa.DateTime(timezone=True), nullable=True, index=True),
        sa.Column('archive_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('place_of_performance_city', sa.String(100), nullable=True),
        sa.Column('place_of_performance_state', sa.String(50), nullable=True),
        sa.Column('place_of_performance_country', sa.String(100), nullable=True),
        sa.Column('estimated_value', sa.Numeric(15, 2), nullable=True),
        sa.Column('primary_contact_name', sa.String(255), nullable=True),
        sa.Column('primary_contact_email', sa.String(255), nullable=True),
        sa.Column('primary_contact_phone', sa.String(50), nullable=True),
        sa.Column('sam_url', sa.String(500), nullable=True),
        sa.Column('raw_data', postgresql.JSONB(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('last_synced_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )

    # Create proposals table
    op.create_table(
        'proposals',
        sa.Column('id', postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column('organization_id', postgresql.UUID(as_uuid=False), sa.ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('opportunity_id', postgresql.UUID(as_uuid=False), sa.ForeignKey('opportunities.id', ondelete='SET NULL'), nullable=True, index=True),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.String(50), nullable=False, default='draft', index=True),
        sa.Column('solicitation_number', sa.String(100), nullable=True),
        sa.Column('agency', sa.String(255), nullable=True),
        sa.Column('naics_code', sa.String(10), nullable=True),
        sa.Column('due_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('submitted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('estimated_value', sa.Float(), nullable=True),
        sa.Column('proposed_value', sa.Float(), nullable=True),
        sa.Column('awarded_value', sa.Float(), nullable=True),
        sa.Column('executive_summary', sa.Text(), nullable=True),
        sa.Column('technical_approach', sa.Text(), nullable=True),
        sa.Column('management_approach', sa.Text(), nullable=True),
        sa.Column('past_performance', sa.Text(), nullable=True),
        sa.Column('pricing_summary', sa.Text(), nullable=True),
        sa.Column('sections', postgresql.JSONB(), nullable=True),
        sa.Column('ai_generated_content', postgresql.JSONB(), nullable=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=False), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('updated_by', postgresql.UUID(as_uuid=False), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('proposals')
    op.drop_table('opportunities')

    op.drop_column('organizations', 'naics_codes')
    op.drop_column('organizations', 'duns_number')
    op.drop_column('organizations', 'cage_code')
    op.drop_column('organizations', 'uei_number')
    op.drop_column('organizations', 'address')
    op.drop_column('organizations', 'phone')
    op.drop_column('organizations', 'contact_email')
