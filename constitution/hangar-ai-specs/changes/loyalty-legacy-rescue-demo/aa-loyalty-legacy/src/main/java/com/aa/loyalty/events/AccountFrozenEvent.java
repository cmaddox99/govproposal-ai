package com.aa.loyalty.events;

import java.util.Date;

public final class AccountFrozenEvent {
    private final String memberNumber;
    private final String reason;
    private final Date occurredOn;

    public AccountFrozenEvent(String memberNumber, String reason) {
        this.memberNumber = memberNumber;
        this.reason = reason;
        this.occurredOn = new Date();
    }

    public String getMemberNumber() { return memberNumber; }
    public String getReason() { return reason; }
    public Date getOccurredOn() { return new Date(occurredOn.getTime()); }
}
