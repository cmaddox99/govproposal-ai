"""Platform admin API router for super users."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from govproposal.identity.dependencies import DbSession, SuperUser
from govproposal.identity.repository import OrganizationRepository
from govproposal.identity.schemas import (
    FeatureToggleRequest,
    FeatureToggleResponse,
    FeatureTogglesResponse,
    MessageResponse,
    TenantResponse,
    TenantStatusRequest,
)

router = APIRouter(prefix="/api/v1/platform", tags=["platform-admin"])

# Feature toggles storage (in production, use database or config service)
_feature_toggles: dict[str, bool] = {
    "scoring": True,
    "benchmarks": True,
    "ai_analysis": True,
    "export": True,
    "api_access": True,
}

_feature_descriptions: dict[str, str] = {
    "scoring": "Proposal relevance scoring",
    "benchmarks": "Competitive benchmarks and readiness indicators",
    "ai_analysis": "AI-powered proposal analysis",
    "export": "Export proposals and reports",
    "api_access": "External API access for integrations",
}


@router.get("/tenants", response_model=list[TenantResponse])
async def list_tenants(
    super_user: SuperUser,
    session: DbSession,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[TenantResponse]:
    """List all organizations (tenants). Requires super user role."""
    org_repo = OrganizationRepository(session)
    orgs, _ = await org_repo.list_all(limit, offset)

    tenants = []
    for org in orgs:
        member_count = await org_repo.get_member_count(org.id)
        tenants.append(
            TenantResponse(
                id=org.id,
                name=org.name,
                slug=org.slug,
                is_active=org.is_active,
                member_count=member_count,
                created_at=org.created_at,
            )
        )

    return tenants


@router.get("/tenants/{org_id}", response_model=TenantResponse)
async def get_tenant(
    org_id: str,
    super_user: SuperUser,
    session: DbSession,
) -> TenantResponse:
    """Get tenant details. Requires super user role."""
    org_repo = OrganizationRepository(session)
    org = await org_repo.get_by_id(org_id)

    if not org:
        from govproposal.identity.exceptions import OrganizationNotFoundError

        raise OrganizationNotFoundError()

    member_count = await org_repo.get_member_count(org.id)

    return TenantResponse(
        id=org.id,
        name=org.name,
        slug=org.slug,
        is_active=org.is_active,
        member_count=member_count,
        created_at=org.created_at,
    )


@router.put("/tenants/{org_id}/status", response_model=TenantResponse)
async def update_tenant_status(
    org_id: str,
    data: TenantStatusRequest,
    super_user: SuperUser,
    session: DbSession,
) -> TenantResponse:
    """Enable/disable organization. Requires super user role."""
    org_repo = OrganizationRepository(session)
    org = await org_repo.get_by_id(org_id)

    if not org:
        from govproposal.identity.exceptions import OrganizationNotFoundError

        raise OrganizationNotFoundError()

    org.is_active = data.is_active
    await org_repo.update(org)

    member_count = await org_repo.get_member_count(org.id)

    return TenantResponse(
        id=org.id,
        name=org.name,
        slug=org.slug,
        is_active=org.is_active,
        member_count=member_count,
        created_at=org.created_at,
    )


@router.get("/features", response_model=FeatureTogglesResponse)
async def get_feature_toggles(
    super_user: SuperUser,
) -> FeatureTogglesResponse:
    """Get all feature toggle states. Requires super user role."""
    features = [
        FeatureToggleResponse(
            feature=name,
            enabled=enabled,
            description=_feature_descriptions.get(name),
        )
        for name, enabled in _feature_toggles.items()
    ]
    return FeatureTogglesResponse(features=features)


@router.get("/features/{feature}", response_model=FeatureToggleResponse)
async def get_feature_toggle(
    feature: str,
    super_user: SuperUser,
) -> FeatureToggleResponse:
    """Get feature toggle state. Requires super user role."""
    if feature not in _feature_toggles:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="Feature not found")

    return FeatureToggleResponse(
        feature=feature,
        enabled=_feature_toggles[feature],
        description=_feature_descriptions.get(feature),
    )


@router.put("/features/{feature}", response_model=FeatureToggleResponse)
async def update_feature_toggle(
    feature: str,
    data: FeatureToggleRequest,
    super_user: SuperUser,
) -> FeatureToggleResponse:
    """Update feature toggle. Requires super user role."""
    if feature not in _feature_toggles:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="Feature not found")

    _feature_toggles[feature] = data.enabled

    return FeatureToggleResponse(
        feature=feature,
        enabled=_feature_toggles[feature],
        description=_feature_descriptions.get(feature),
    )
