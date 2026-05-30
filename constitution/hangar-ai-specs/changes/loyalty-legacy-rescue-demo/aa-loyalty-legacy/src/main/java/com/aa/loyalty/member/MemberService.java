package com.aa.loyalty.member;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.Date;
import java.util.List;
import java.util.logging.Logger;

/**
 * VIOLATIONS:
 * - Enrollment logic mixed with profile update and search
 * - No domain events emitted on status change
 * - Tier update logic duplicated from TierService
 */
@Service
public class MemberService {

    private static final Logger LOG = Logger.getLogger(MemberService.class.getName());

    @Autowired
    private MemberRepository memberRepository;

    @Transactional
    public Member enroll(String firstName, String lastName, String email,
                         String phone, Date dateOfBirth) {
        // VIOLATION: no duplicate email check
        Member existing = memberRepository.findByEmail(email);
        if (existing != null) {
            LOG.warning("Duplicate enrollment attempt for email: " + email);
            return existing; // VIOLATION: silently returns existing — no error
        }

        Member member = new Member();
        member.setFirstName(firstName);
        member.setLastName(lastName);
        member.setEmail(email);
        member.setPhone(phone);
        member.setDateOfBirth(dateOfBirth);
        member.setEnrollmentDate(new Date());
        member.setLastUpdated(new Date());
        // VIOLATION: member number generation is inline magic
        member.setMemberNumber("AA" + System.currentTimeMillis());
        return memberRepository.save(member);
    }

    @Transactional
    public Member updateProfile(String memberNumber, String email, String phone,
                                String addressLine1, String city, String state,
                                String postalCode, String country) {
        Member member = memberRepository.findByMemberNumber(memberNumber);
        if (member == null) throw new RuntimeException("Member not found");

        // VIOLATION: no email format validation
        if (email != null) member.setEmail(email);
        if (phone != null) member.setPhone(phone);
        if (addressLine1 != null) member.setAddressLine1(addressLine1);
        if (city != null) member.setCity(city);
        if (state != null) member.setState(state);
        if (postalCode != null) member.setPostalCode(postalCode);
        if (country != null) member.setCountry(country);
        member.setLastUpdated(new Date());

        return memberRepository.save(member);
    }

    // VIOLATION: tier update logic should only live in TierService
    @Transactional
    public void updateTierStatus(String memberNumber, String newTier) {
        Member member = memberRepository.findByMemberNumber(memberNumber);
        if (member == null) return;
        String oldTier = member.getTierStatus();
        member.setTierStatus(newTier);
        member.setLastUpdated(new Date());
        memberRepository.save(member);
        LOG.info("Tier changed for " + memberNumber + ": " + oldTier + " -> " + newTier);
        // VIOLATION: no event emitted, downstream consumers unaware of tier change
    }

    public Member getMember(String memberNumber) {
        return memberRepository.findByMemberNumber(memberNumber);
    }

    public List<Member> searchByLastName(String lastName) {
        // VIOLATION: no rate limiting, no result cap
        return memberRepository.searchByLastName(lastName);
    }

    public List<Member> getAllEliteMembers() {
        return memberRepository.findAllEliteMembers();
    }

    @Transactional
    public void deactivateMember(String memberNumber) {
        Member member = memberRepository.findByMemberNumber(memberNumber);
        if (member != null) {
            member.setActive(false);
            member.setLastUpdated(new Date());
            memberRepository.save(member);
        }
    }
}
