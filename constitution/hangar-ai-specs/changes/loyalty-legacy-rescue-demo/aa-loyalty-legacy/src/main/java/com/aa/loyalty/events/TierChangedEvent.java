package com.aa.loyalty.events;

import com.aa.loyalty.tier.domain.TierStatus;
import java.util.Date;

public final class TierChangedEvent {
    private final String memberNumber;
    private final TierStatus previousTier;
    private final TierStatus newTier;
    private final Date occurredOn;

    public TierChangedEvent(String memberNumber, TierStatus previousTier, TierStatus newTier) {
        this.memberNumber = memberNumber;
        this.previousTier = previousTier;
        this.newTier = newTier;
        this.occurredOn = new Date();
    }

    public String getMemberNumber() { return memberNumber; }
    public TierStatus getPreviousTier() { return previousTier; }
    public TierStatus getNewTier() { return newTier; }
    public Date getOccurredOn() { return new Date(occurredOn.getTime()); }
}
