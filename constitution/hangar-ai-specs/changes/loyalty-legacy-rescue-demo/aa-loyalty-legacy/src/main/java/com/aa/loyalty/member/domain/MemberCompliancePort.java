package com.aa.loyalty.member.domain;

/**
 * ISP-compliant port for compliance operations (GDPR, data retention).
 * Implemented by ComplianceMemberService (separate bounded context).
 * MemberService does NOT implement this interface.
 */
public interface MemberCompliancePort {
    void archiveMemberForCompliance(String memberNumber, String retentionPolicyId);
}
