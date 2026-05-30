package com.aa.loyalty.events;

import java.util.Date;

public final class MilesExpiredEvent {
    private final String memberNumber;
    private final long expiredMiles;
    private final Date occurredOn;

    public MilesExpiredEvent(String memberNumber, long expiredMiles) {
        this.memberNumber = memberNumber;
        this.expiredMiles = expiredMiles;
        this.occurredOn = new Date();
    }

    public String getMemberNumber() { return memberNumber; }
    public long getExpiredMiles() { return expiredMiles; }
    public Date getOccurredOn() { return new Date(occurredOn.getTime()); }
}
