package com.aa.loyalty.member.domain;

import java.util.List;

/**
 * ISP-compliant port for member admin operations.
 * Implemented by AdminMemberService (separate bounded context).
 * MemberService does NOT implement this interface.
 */
public interface MemberAdminPort {
    void bulkImportMembers(List<EnrollmentRequest> requests);
    byte[] exportMemberDataForRegulator(java.util.Date fromDate, java.util.Date toDate);
}
