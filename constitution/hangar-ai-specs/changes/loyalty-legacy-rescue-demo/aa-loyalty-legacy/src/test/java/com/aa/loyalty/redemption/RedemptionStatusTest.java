package com.aa.loyalty.redemption;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.aa.loyalty.redemption.domain.RedemptionStatus;

class RedemptionStatusTest {

    @Test
    void allFourValuesExist() {
        assertEquals(4, RedemptionStatus.values().length);
    }

    @Test
    void valueOf_pending_returnsPending() {
        assertEquals(RedemptionStatus.PENDING, RedemptionStatus.valueOf("PENDING"));
    }

    @Test
    void valueOf_confirmed_returnsConfirmed() {
        assertEquals(RedemptionStatus.CONFIRMED, RedemptionStatus.valueOf("CONFIRMED"));
    }

    @Test
    void valueOf_cancelled_returnsCancelled() {
        assertEquals(RedemptionStatus.CANCELLED, RedemptionStatus.valueOf("CANCELLED"));
    }

    @Test
    void valueOf_expired_returnsExpired() {
        assertEquals(RedemptionStatus.EXPIRED, RedemptionStatus.valueOf("EXPIRED"));
    }

    @Test
    void name_pending_matchesDbString() {
        assertEquals("PENDING", RedemptionStatus.PENDING.name());
    }

    @Test
    void name_confirmed_matchesDbString() {
        assertEquals("CONFIRMED", RedemptionStatus.CONFIRMED.name());
    }

    @Test
    void name_cancelled_matchesDbString() {
        assertEquals("CANCELLED", RedemptionStatus.CANCELLED.name());
    }

    @Test
    void name_expired_matchesDbString() {
        assertEquals("EXPIRED", RedemptionStatus.EXPIRED.name());
    }
}
