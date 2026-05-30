package com.aa.loyalty.member.application;

import java.util.Date;
import java.util.List;
import com.aa.loyalty.member.domain.Address;
import com.aa.loyalty.member.domain.EnrollmentRequest;
import com.aa.loyalty.member.domain.Member;

/**
 * ISP VIOLATION: This interface bundles FOUR separate client concerns into one fat contract:
 *   1. Member self-service  (enroll, updateProfile, getMember, searchByLastName)
 *   2. Tier management      (updateTierStatus, getAllEliteMembers)
 *   3. Admin / compliance   (deactivateMember, bulkImportMembers, exportMemberDataForRegulator)
 *   4. Fraud operations     (freezeAccountForFraud, archiveMemberForCompliance)
 *
 * MemberService implements ALL of these even though it should only own self-service
 * and tier concerns. Fraud-team clients get enroll(). Compliance clients get
 * freezeAccountForFraud(). Every implementor is polluted with methods that belong
 * to a completely different bounded context.
 *
 * Constitutional fix: split into four focused ports —
 *   MemberSelfServicePort, MemberTierPort, MemberAdminPort, MemberCompliancePort.
 * Each client depends only on the interface it actually uses (ISP).
 * @deprecated Use {@link MemberSelfServicePort} and focused ports instead.
 */
@Deprecated
@SuppressWarnings("java:S1133")
public interface MemberManagementService {

    // --- Self-service operations ---
    Member enroll(String firstName, String lastName, String email,
                  String phone, Date dateOfBirth);

    Member updateProfile(String memberNumber, String email, String phone, Address address);

    Member getMember(String memberNumber);

    List<Member> searchByLastName(String lastName);

    // --- Tier management ---
    void updateTierStatus(String memberNumber, String newTier);

    List<Member> getAllEliteMembers();

    // --- Admin operations (should be a separate interface) ---
    void deactivateMember(String memberNumber);

    // ISP VIOLATION: admin-only — self-service clients have no use for this method
    void bulkImportMembers(List<EnrollmentRequest> requests);

    // ISP VIOLATION: compliance-only — forces ALL implementors to know about regulatory export
    byte[] exportMemberDataForRegulator(Date fromDate, Date toDate);

    // --- Fraud operations (should be a completely separate bounded context) ---

    // ISP VIOLATION: fraud-team operation leaked into the general member interface
    void freezeAccountForFraud(String memberNumber, String fraudCaseId);

    // ISP VIOLATION: compliance-only — data retention has nothing to do with enrollment
    void archiveMemberForCompliance(String memberNumber, String retentionPolicyId);
}
