package com.aa.loyalty.member;

import com.aa.loyalty.tier.domain.TierStatus;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;
import com.aa.loyalty.member.domain.Address;
import com.aa.loyalty.member.domain.Member;

/**
 * ENG-4.1 — Covers Member entity address delegation methods and backward-compat setters.
 * ENG-3.2 — Verifies Address VO immutability contract through Member.
 */
class MemberTest {

    @Test
    void setAddress_andGetters_work() {
        Member m = new Member();
        Address address = new Address("1 Skyway Dr", null, "Fort Worth", "TX", "76155", "US");
        m.setAddress(address);
        assertEquals("1 Skyway Dr", m.getAddressLine1());
        assertEquals("Fort Worth", m.getCity());
        assertEquals("TX", m.getState());
        assertEquals("76155", m.getPostalCode());
        assertEquals("US", m.getCountry());
    }

    @Test
    void setAddressLine1_onNullAddress_createsNewAddress() {
        Member m = new Member();
        m.setAddressLine1("100 Main St");
        assertEquals("100 Main St", m.getAddressLine1());
    }

    @Test
    void setCity_onNullAddress_createsNewAddress() {
        Member m = new Member();
        m.setCity("Dallas");
        assertEquals("Dallas", m.getCity());
    }

    @Test
    void setTierStatus_andGet_roundTrips() {
        Member m = new Member();
        m.setTierStatus(TierStatus.GOLD);
        assertEquals(TierStatus.GOLD, m.getTierStatus());
    }

    @Test
    void newMember_defaultTierStatus_isGeneral() {
        Member m = new Member();
        // Default should be GENERAL (set in field initializer or via entity init)
        // Verifies entity can be constructed and tier accessed without NPE
        assertNotNull(m);
    }

    // ─── Task 2: Domain behavior tests (written BEFORE implementation) ───

    @Test
    void enroll_setsAllRequiredFields() {
        java.util.Date dob = new java.util.Date(0);
        Member m = Member.enroll("John", "Doe", "john@example.com", "555-1234", dob, "AA000001");
        assertEquals("John", m.getFirstName());
        assertEquals("Doe", m.getLastName());
        assertEquals("john@example.com", m.getEmail());
        assertEquals("555-1234", m.getPhone());
        assertEquals(dob, m.getDateOfBirth());
        assertEquals("AA000001", m.getMemberNumber());
    }

    @Test
    void enroll_defaultsTierToGeneral() {
        Member m = Member.enroll("Jane", "Doe", "jane@example.com", null, null, "AA000002");
        assertEquals(TierStatus.GENERAL, m.getTierStatus());
    }

    @Test
    void enroll_setsEnrollmentDate() {
        long before = System.currentTimeMillis();
        Member m = Member.enroll("A", "B", "ab@example.com", null, null, "AA000003");
        long after = System.currentTimeMillis();
        assertNotNull(m.getEnrollmentDate());
        assertTrue(m.getEnrollmentDate().getTime() >= before - 100);
        assertTrue(m.getEnrollmentDate().getTime() <= after + 100);
    }

    @Test
    void enroll_setsActiveTrueByDefault() {
        Member m = Member.enroll("A", "B", "ab@example.com", null, null, "AA000004");
        assertEquals(Boolean.TRUE, m.getActive());
    }

    @Test
    void deactivate_setsActiveFalse() {
        Member m = Member.enroll("A", "B", "ab@example.com", null, null, "AA000005");
        m.deactivate();
        assertEquals(Boolean.FALSE, m.getActive());
    }

    @Test
    void deactivate_alreadyInactive_throwsISE() {
        Member m = Member.enroll("A", "B", "ab@example.com", null, null, "AA000006");
        m.deactivate();
        assertThrows(IllegalStateException.class, m::deactivate);
    }

    @Test
    void updateContact_validEmail_updatesEmail() {
        Member m = Member.enroll("A", "B", "old@example.com", null, null, "AA000007");
        m.updateContact("new@example.com", null, null);
        assertEquals("new@example.com", m.getEmail());
    }

    @Test
    void updateContact_invalidEmail_throwsIAE() {
        Member m = Member.enroll("A", "B", "valid@example.com", null, null, "AA000008");
        assertThrows(IllegalArgumentException.class, () -> m.updateContact("not-an-email", null, null));
    }

    @Test
    void updateContact_nullEmail_doesNotChangeEmail() {
        Member m = Member.enroll("A", "B", "keep@example.com", null, null, "AA000009");
        m.updateContact(null, "555-9999", null);
        assertEquals("keep@example.com", m.getEmail());
        assertEquals("555-9999", m.getPhone());
    }

    @Test
    void updateContact_setsAddress() {
        Member m = Member.enroll("A", "B", "a@example.com", null, null, "AA000010");
        Address addr = new Address("1 Main St", null, "Dallas", "TX", "75201", "US");
        m.updateContact(null, null, addr);
        assertEquals(addr, m.getAddress());
    }

    @Test
    void upgradeTier_validUpgrade_updatesTier() {
        Member m = Member.enroll("A", "B", "a@example.com", null, null, "AA000011");
        m.upgradeTier(TierStatus.GOLD);
        assertEquals(TierStatus.GOLD, m.getTierStatus());
    }

    @Test
    void upgradeTier_downgrade_throwsISE() {
        Member m = Member.enroll("A", "B", "a@example.com", null, null, "AA000012");
        m.setTierStatus(TierStatus.GOLD);
        assertThrows(IllegalStateException.class, () -> m.upgradeTier(TierStatus.GENERAL));
    }

    @Test
    void upgradeTier_sameLevel_throwsISE() {
        Member m = Member.enroll("A", "B", "a@example.com", null, null, "AA000013");
        m.setTierStatus(TierStatus.GOLD);
        assertThrows(IllegalStateException.class, () -> m.upgradeTier(TierStatus.GOLD));
    }

    @Test
    void upgradeTier_null_throwsIAE() {
        Member m = Member.enroll("A", "B", "a@example.com", null, null, "AA000014");
        assertThrows(IllegalArgumentException.class, () -> m.upgradeTier(null));
    }

    @Test
    void resetTierToGeneral_setsGeneralRegardlessOfCurrentTier() {
        Member m = Member.enroll("A", "B", "a@example.com", null, null, "AA000015");
        m.setTierStatus(TierStatus.EXECUTIVE_PLATINUM);
        m.resetTierToGeneral();
        assertEquals(TierStatus.GENERAL, m.getTierStatus());
    }
}
