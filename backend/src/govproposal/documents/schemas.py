"""Document schemas."""

from datetime import datetime

from pydantic import BaseModel


class OpportunityDocumentResponse(BaseModel):
    """A document attached to an opportunity."""

    id: str
    organization_id: str
    opportunity_id: str
    filename: str
    content_type: str | None = None
    size_bytes: int
    description: str | None = None
    uploaded_by: str | None = None
    uploaded_at: datetime

    model_config = {"from_attributes": True}


class OpportunityDocumentList(BaseModel):
    items: list[OpportunityDocumentResponse]
    total: int
