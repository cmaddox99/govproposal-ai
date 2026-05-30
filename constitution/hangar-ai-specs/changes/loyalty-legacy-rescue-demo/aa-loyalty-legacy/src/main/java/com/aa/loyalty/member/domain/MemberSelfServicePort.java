package com.aa.loyalty.member.domain;

import java.util.Date;
import java.util.List;

/**
 * ISP-compliant focused port for member self-service operations.
 * Replaces the bloated MemberManagementService interface.
 * Clients that only need self-service operations depend only on this interface.
 */
public interface MemberSelfServicePort {

    Member enroll(String firstName, String lastName, String email,
                  String phone, Date dateOfBirth);

    Member updateProfile(String memberNumber, String email, String phone, Address address);

    Member getMember(String memberNumber);

    List<Member> searchByLastName(String lastName);

    void updateTierStatus(String memberNumber, String newTier);

    List<Member> getAllEliteMembers();

    void deactivateMember(String memberNumber);
}
