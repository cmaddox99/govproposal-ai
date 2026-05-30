package com.aa.loyalty.mileage;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.aa.loyalty.mileage.domain.AccountStatus;

class AccountStatusTest {

    @Test
    void allFourValuesExist() {
        assertEquals(4, AccountStatus.values().length);
    }

    @Test
    void valueOf_active_returnsActive() {
        assertEquals(AccountStatus.ACTIVE, AccountStatus.valueOf("ACTIVE"));
    }

    @Test
    void valueOf_frozen_returnsFrozen() {
        assertEquals(AccountStatus.FROZEN, AccountStatus.valueOf("FROZEN"));
    }

    @Test
    void valueOf_milesExpired_returnsMilesExpired() {
        assertEquals(AccountStatus.MILES_EXPIRED, AccountStatus.valueOf("MILES_EXPIRED"));
    }

    @Test
    void valueOf_closed_returnsClosed() {
        assertEquals(AccountStatus.CLOSED, AccountStatus.valueOf("CLOSED"));
    }

    @Test
    void name_active_matchesDbString() {
        assertEquals("ACTIVE", AccountStatus.ACTIVE.name());
    }

    @Test
    void name_frozen_matchesDbString() {
        assertEquals("FROZEN", AccountStatus.FROZEN.name());
    }

    @Test
    void name_milesExpired_matchesDbString() {
        assertEquals("MILES_EXPIRED", AccountStatus.MILES_EXPIRED.name());
    }

    @Test
    void name_closed_matchesDbString() {
        assertEquals("CLOSED", AccountStatus.CLOSED.name());
    }
}
