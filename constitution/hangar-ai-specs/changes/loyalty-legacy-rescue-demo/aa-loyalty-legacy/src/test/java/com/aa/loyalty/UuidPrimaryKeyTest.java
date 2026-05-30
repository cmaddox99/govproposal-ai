package com.aa.loyalty;

import com.aa.loyalty.member.domain.Member;
import com.aa.loyalty.mileage.domain.MileageAccount;
import com.aa.loyalty.mileage.domain.MileageTransaction;
import com.aa.loyalty.redemption.domain.Redemption;
import com.aa.loyalty.partner.domain.Partner;
import org.junit.jupiter.api.Test;
import java.util.UUID;
import static org.junit.jupiter.api.Assertions.*;

/**
 * ENG-4.1 — Failing tests written BEFORE implementation.
 * ENG-3.2 — UUID assigned at construction; immutable primary key.
 */
class UuidPrimaryKeyTest {

    @Test
    void member_newInstance_hasNonNullUuidId() {
        Member m = new Member();
        assertNotNull(m.getId());
        assertTrue(m.getId() instanceof UUID);
    }

    @Test
    void member_twoInstances_haveDifferentIds() {
        Member m1 = new Member();
        Member m2 = new Member();
        assertNotEquals(m1.getId(), m2.getId());
    }

    @Test
    void mileageAccount_newInstance_hasNonNullUuidId() {
        MileageAccount a = new MileageAccount();
        assertNotNull(a.getId());
        assertTrue(a.getId() instanceof UUID);
    }

    @Test
    void mileageAccount_twoInstances_haveDifferentIds() {
        MileageAccount a1 = new MileageAccount();
        MileageAccount a2 = new MileageAccount();
        assertNotEquals(a1.getId(), a2.getId());
    }

    @Test
    void mileageTransaction_newInstance_hasNonNullUuidId() {
        MileageTransaction t = new MileageTransaction();
        assertNotNull(t.getId());
        assertTrue(t.getId() instanceof UUID);
    }

    @Test
    void mileageTransaction_twoInstances_haveDifferentIds() {
        MileageTransaction t1 = new MileageTransaction();
        MileageTransaction t2 = new MileageTransaction();
        assertNotEquals(t1.getId(), t2.getId());
    }

    @Test
    void redemption_newInstance_hasNonNullUuidId() {
        Redemption r = new Redemption();
        assertNotNull(r.getId());
        assertTrue(r.getId() instanceof UUID);
    }

    @Test
    void redemption_twoInstances_haveDifferentIds() {
        Redemption r1 = new Redemption();
        Redemption r2 = new Redemption();
        assertNotEquals(r1.getId(), r2.getId());
    }

    @Test
    void partner_newInstance_hasNonNullUuidId() {
        Partner p = new Partner();
        assertNotNull(p.getId());
        assertTrue(p.getId() instanceof UUID);
    }

    @Test
    void partner_twoInstances_haveDifferentIds() {
        Partner p1 = new Partner();
        Partner p2 = new Partner();
        assertNotEquals(p1.getId(), p2.getId());
    }

    @Test
    void member_idIsPreservedAfterFieldInitialization() {
        Member m = new Member();
        UUID firstId = m.getId();
        assertNotNull(firstId);
        assertEquals(firstId, m.getId());
    }
}
