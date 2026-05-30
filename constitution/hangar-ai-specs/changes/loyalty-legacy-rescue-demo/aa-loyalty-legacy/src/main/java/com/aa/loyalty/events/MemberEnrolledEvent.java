package com.aa.loyalty.events;

import java.util.Date;

public final class MemberEnrolledEvent {
    private final String memberNumber;
    private final String email;
    private final Date enrollmentDate;
    private final Date occurredOn;

    public MemberEnrolledEvent(String memberNumber, String email, Date enrollmentDate) {
        this.memberNumber = memberNumber;
        this.email = email;
        this.enrollmentDate = enrollmentDate != null ? new Date(enrollmentDate.getTime()) : null;
        this.occurredOn = new Date();
    }

    public String getMemberNumber() { return memberNumber; }
    public String getEmail() { return email; }
    public Date getEnrollmentDate() { return enrollmentDate != null ? new Date(enrollmentDate.getTime()) : null; }
    public Date getOccurredOn() { return new Date(occurredOn.getTime()); }
}
