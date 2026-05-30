package com.aa.loyalty.events;

import java.util.Date;

public final class MilesRedeemedEvent {
    private final String memberNumber;
    private final long miles;
    private final String awardCategory;
    private final Date occurredOn;

    public MilesRedeemedEvent(String memberNumber, long miles, String awardCategory) {
        this.memberNumber = memberNumber;
        this.miles = miles;
        this.awardCategory = awardCategory;
        this.occurredOn = new Date();
    }

    public String getMemberNumber() { return memberNumber; }
    public long getMiles() { return miles; }
    public String getAwardCategory() { return awardCategory; }
    public Date getOccurredOn() { return new Date(occurredOn.getTime()); }
}
