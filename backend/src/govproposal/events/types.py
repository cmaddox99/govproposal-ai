"""Event type constants."""


class EventTypes:
    PROPOSAL_CREATED = "proposal.created"
    PROPOSAL_UPDATED = "proposal.updated"
    PROPOSAL_SCORED = "proposal.scored"
    PROPOSAL_SUBMITTED = "proposal.submitted"
    PROPOSAL_DELETED = "proposal.deleted"

    OPPORTUNITY_SYNCED = "opportunity.synced"
    OPPORTUNITY_MATCHED = "opportunity.matched"

    COMPLIANCE_ITEM_CREATED = "compliance.item_created"
    COMPLIANCE_EXPIRING = "compliance.expiring"

    USER_REGISTERED = "user.registered"
    USER_LOGIN = "user.login"
