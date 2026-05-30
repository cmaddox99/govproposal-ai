package com.aa.loyalty.events;

import java.util.Date;

public final class MilesAccruedEvent {
    private final String memberNumber;
    private final long miles;
    private final String transactionRef;
    private final String source;
    private final Date occurredOn;

    public MilesAccruedEvent(String memberNumber, long miles, String transactionRef, String source) {
        this.memberNumber = memberNumber;
        this.miles = miles;
        this.transactionRef = transactionRef;
        this.source = source;
        this.occurredOn = new Date();
    }

    public String getMemberNumber() { return memberNumber; }
    public long getMiles() { return miles; }
    public String getTransactionRef() { return transactionRef; }
    public String getSource() { return source; }
    public Date getOccurredOn() { return new Date(occurredOn.getTime()); }
}
