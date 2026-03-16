"""Seed script — creates test organizations, users, proposals, opportunities, and compliance data.

Usage: cd backend && python -m scripts.seed
"""

import asyncio
import sys
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from sqlalchemy import select

# Ensure govproposal is importable
sys.path.insert(0, "src")

from govproposal.db.base import async_session_maker, engine, Base
from govproposal.identity.models import Organization, OrganizationMember, User
from govproposal.identity.security import hash_password
from govproposal.opportunities.models import Opportunity
from govproposal.proposals.models import Proposal, ProposalStatus
from govproposal.compliance.models import (
    CMMCAssessment,
    Certification,
    ComplianceItem,
    ComplianceStatus,
)

PASSWORD_HASH = hash_password("TestPassword123!")

now = datetime.now(timezone.utc)


def _id() -> str:
    return str(uuid4())


# --- Orgs ---
org1_id = _id()
org2_id = _id()

ORGS = [
    Organization(id=org1_id, name="Acme Government Solutions", slug="acme-gov", contact_email="admin@acme-gov.com", uei_number="ACME12345678", cage_code="1A2B3"),
    Organization(id=org2_id, name="Federal Tech Partners", slug="fed-tech", contact_email="admin@fedtech.com", uei_number="FEDT98765432", cage_code="9X8Y7"),
]

# --- Users ---
user1_id, user2_id, user3_id, user4_id = _id(), _id(), _id(), _id()

USERS = [
    User(id=user1_id, email="admin@acme-gov.com", password_hash=PASSWORD_HASH, is_active=True, is_verified=True, mfa_required=False),
    User(id=user2_id, email="member@acme-gov.com", password_hash=PASSWORD_HASH, is_active=True, is_verified=True, mfa_required=False),
    User(id=user3_id, email="admin@fedtech.com", password_hash=PASSWORD_HASH, is_active=True, is_verified=True, mfa_required=False),
    User(id=user4_id, email="member@fedtech.com", password_hash=PASSWORD_HASH, is_active=True, is_verified=True, mfa_required=False),
]

MEMBERS = [
    OrganizationMember(id=_id(), user_id=user1_id, organization_id=org1_id, role="owner"),
    OrganizationMember(id=_id(), user_id=user2_id, organization_id=org1_id, role="member"),
    OrganizationMember(id=_id(), user_id=user3_id, organization_id=org2_id, role="owner"),
    OrganizationMember(id=_id(), user_id=user4_id, organization_id=org2_id, role="member"),
]

# --- Opportunities ---
OPPORTUNITIES = [
    Opportunity(
        id=_id(), notice_id=f"SAM-{uuid4().hex[:8].upper()}", solicitation_number="W911QY-26-R-0001",
        title="Army Cybersecurity Infrastructure Modernization", description="Modernize cybersecurity infrastructure across CONUS installations.",
        department="Department of Defense", agency="U.S. Army", notice_type="solicitation",
        naics_code="541512", set_aside_type="none", response_deadline=now + timedelta(days=30),
        estimated_value=5000000.00, source="sam_gov",
    ),
    Opportunity(
        id=_id(), notice_id=f"SAM-{uuid4().hex[:8].upper()}", solicitation_number="75A50126-R-0045",
        title="VA Electronic Health Records Integration", description="Integrate EHR systems across VA medical centers.",
        department="Department of Veterans Affairs", agency="Veterans Health Administration", notice_type="combined_synopsis",
        naics_code="541511", set_aside_type="sdvosb", response_deadline=now + timedelta(days=45),
        estimated_value=3200000.00, source="sam_gov",
    ),
    Opportunity(
        id=_id(), notice_id=f"SAM-{uuid4().hex[:8].upper()}", solicitation_number="NNG26-R-0012",
        title="NASA Data Analytics Platform Development", description="Cloud-based analytics platform for mission data.",
        department="NASA", agency="NASA", notice_type="presolicitation",
        naics_code="541519", set_aside_type="sba", response_deadline=now + timedelta(days=60),
        estimated_value=950000.00, source="sam_gov",
    ),
]


def _make_proposals(org_id: str, user_id: str) -> list:
    return [
        Proposal(id=_id(), organization_id=org_id, title="DOD Cybersecurity Enhancement", status=ProposalStatus.IN_PROGRESS.value,
                 agency="Department of Defense", solicitation_number="W911QY-26-R-0001", naics_code="541512",
                 due_date=now + timedelta(days=14), estimated_value=2400000, created_by=user_id,
                 executive_summary="Our proposal addresses DoD cybersecurity modernization requirements."),
        Proposal(id=_id(), organization_id=org_id, title="VA Healthcare IT Modernization", status=ProposalStatus.REVIEW.value,
                 agency="Veterans Affairs", solicitation_number="75A50126-R-0045", naics_code="541511",
                 due_date=now + timedelta(days=20), estimated_value=1800000, created_by=user_id,
                 executive_summary="Comprehensive EHR integration solution for VA medical centers."),
        Proposal(id=_id(), organization_id=org_id, title="GSA Cloud Infrastructure", status=ProposalStatus.DRAFT.value,
                 agency="General Services Administration", naics_code="541519",
                 due_date=now + timedelta(days=45), estimated_value=3200000, created_by=user_id),
        Proposal(id=_id(), organization_id=org_id, title="NASA Data Analytics Platform", status=ProposalStatus.SUBMITTED.value,
                 agency="NASA", solicitation_number="NNG26-R-0012", naics_code="541519",
                 due_date=now - timedelta(days=5), estimated_value=950000, created_by=user_id,
                 submitted_at=now - timedelta(days=5),
                 executive_summary="Cloud-native analytics platform for NASA mission data."),
        Proposal(id=_id(), organization_id=org_id, title="USDA Rural Broadband Mapping", status=ProposalStatus.AWARDED.value,
                 agency="USDA", naics_code="541512",
                 estimated_value=750000, awarded_value=720000, created_by=user_id,
                 submitted_at=now - timedelta(days=60)),
    ]


PROPOSALS = _make_proposals(org1_id, user1_id) + _make_proposals(org2_id, user3_id)

# --- Compliance ---
COMPLIANCE_ITEMS = [
    ComplianceItem(id=_id(), organization_id=org1_id, framework="far", clause_number="52.204-7", title="SAM.gov Registration", status=ComplianceStatus.COMPLIANT.value, evidence_notes="Active registration verified"),
    ComplianceItem(id=_id(), organization_id=org1_id, framework="far", clause_number="52.204-13", title="CAGE Code Maintenance", status=ComplianceStatus.COMPLIANT.value, evidence_notes="Valid CAGE code on file"),
    ComplianceItem(id=_id(), organization_id=org1_id, framework="far", clause_number="52.219-1", title="Small Business Program Representation", status=ComplianceStatus.COMPLIANT.value, evidence_notes="UEI number verified"),
    ComplianceItem(id=_id(), organization_id=org1_id, framework="dfars", clause_number="252.204-7012", title="DFARS Cybersecurity Requirements", status=ComplianceStatus.PARTIAL.value, evidence_notes="SSP in development"),
    ComplianceItem(id=_id(), organization_id=org1_id, framework="nist_800_171", clause_number="3.1.1", title="Access Control", status=ComplianceStatus.NON_COMPLIANT.value, evidence_notes="Facility clearance pending", due_date=now + timedelta(days=90)),
]

CERTIFICATIONS = [
    Certification(id=_id(), organization_id=org1_id, certification_type="sam", identifier="ACME12345678", status=ComplianceStatus.COMPLIANT.value, expiry_date=now + timedelta(days=365)),
    Certification(id=_id(), organization_id=org1_id, certification_type="cage", identifier="1A2B3", status=ComplianceStatus.COMPLIANT.value),
    Certification(id=_id(), organization_id=org1_id, certification_type="gsa", identifier="GS-35F-0001A", status=ComplianceStatus.COMPLIANT.value, expiry_date=now + timedelta(days=45), notes="Expires in 45 days"),
    Certification(id=_id(), organization_id=org1_id, certification_type="sdvosb", status=ComplianceStatus.PENDING_REVIEW.value, notes="Application submitted"),
]

CMMC_ASSESSMENTS = [
    CMMCAssessment(id=_id(), organization_id=org1_id, target_level="level_2", total_controls=110,
                   implemented_controls=78, partially_implemented=20, not_implemented=12,
                   findings_count=5, assessment_date=now - timedelta(days=30)),
]


async def seed() -> None:
    print("Seeding database...")

    async with async_session_maker() as session:
        # Check if already seeded
        existing = (await session.execute(
            select(Organization).where(Organization.slug == "acme-gov")
        )).scalar_one_or_none()
        if existing:
            print("Database already seeded (acme-gov org exists). Skipping.")
            return

        for obj_list in [ORGS, USERS, MEMBERS, OPPORTUNITIES, PROPOSALS, COMPLIANCE_ITEMS, CERTIFICATIONS, CMMC_ASSESSMENTS]:
            for obj in obj_list:
                session.add(obj)

        await session.commit()
        print(f"Seeded: 2 orgs, 4 users, {len(PROPOSALS)} proposals, {len(OPPORTUNITIES)} opportunities")
        print(f"Seeded: {len(COMPLIANCE_ITEMS)} compliance items, {len(CERTIFICATIONS)} certifications, {len(CMMC_ASSESSMENTS)} CMMC assessments")
        print("Login credentials: any user email above with password 'TestPassword123!'")


if __name__ == "__main__":
    asyncio.run(seed())
