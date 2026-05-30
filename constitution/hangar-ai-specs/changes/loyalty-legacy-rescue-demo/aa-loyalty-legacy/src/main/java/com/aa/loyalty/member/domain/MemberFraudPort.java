package com.aa.loyalty.member.domain;

/**
 * ISP-compliant port for fraud management operations.
 * Implemented by FraudManagementService (separate bounded context).
 * MemberService does NOT implement this interface.
 */
public interface MemberFraudPort {
    void freezeAccountForFraud(String memberNumber, String fraudCaseId);
}
