package com.aa.loyalty.redemption;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.aa.loyalty.redemption.domain.Redemption;
import com.aa.loyalty.redemption.domain.RedemptionStatus;

/**
 * ENG-4.1 — Tests written BEFORE implementation of Redemption state machine.
 * ENG-2.1 — Redemption state transitions are domain behavior.
 */
class RedemptionTest {

    @Test
    void book_setsAllFields() {
        Redemption r = Redemption.book("AA000001", "AWARD_FLIGHT", 25000L, "ABC123");
        assertEquals("AA000001", r.getMemberNumber());
        assertEquals("AWARD_FLIGHT", r.getRedemptionType());
        assertEquals(25000L, r.getMilesCost());
        assertEquals("ABC123", r.getReservationCode());
        assertNotNull(r.getRedemptionDate());
    }

    @Test
    void book_defaultsStatusToPending() {
        Redemption r = Redemption.book("AA000002", "UPGRADE", 5000L, "XYZ789");
        assertEquals(RedemptionStatus.PENDING, r.getStatus());
    }

    @Test
    void confirm_pendingRedemption_setsConfirmed() {
        Redemption r = Redemption.book("AA000003", "AWARD_FLIGHT", 25000L, "DEF456");
        r.confirm();
        assertEquals(RedemptionStatus.CONFIRMED, r.getStatus());
    }

    @Test
    void confirm_alreadyConfirmed_throwsISE() {
        Redemption r = Redemption.book("AA000004", "AWARD_FLIGHT", 25000L, "GHI789");
        r.confirm();
        assertThrows(IllegalStateException.class, r::confirm);
    }

    @Test
    void confirm_cancelledRedemption_throwsISE() {
        Redemption r = Redemption.book("AA000005", "AWARD_FLIGHT", 25000L, "JKL012");
        r.cancel();
        assertThrows(IllegalStateException.class, r::confirm);
    }

    @Test
    void cancel_confirmedRedemption_setsCancelled() {
        Redemption r = Redemption.book("AA000006", "AWARD_FLIGHT", 25000L, "MNO345");
        r.confirm();
        r.cancel();
        assertEquals(RedemptionStatus.CANCELLED, r.getStatus());
    }

    @Test
    void cancel_pendingRedemption_setsCancelled() {
        Redemption r = Redemption.book("AA000007", "AWARD_FLIGHT", 25000L, "PQR678");
        r.cancel();
        assertEquals(RedemptionStatus.CANCELLED, r.getStatus());
    }

    @Test
    void cancel_alreadyCancelled_throwsISE() {
        Redemption r = Redemption.book("AA000008", "AWARD_FLIGHT", 25000L, "STU901");
        r.cancel();
        assertThrows(IllegalStateException.class, r::cancel);
    }

    @Test
    void book_newInstance_hasNonNullId() {
        Redemption r = Redemption.book("AA000009", "GIFT_CARD", 10000L, "VWX234");
        assertNotNull(r.getId());
    }
}
