package com.aa.loyalty.mileage;

import org.junit.jupiter.api.Test;
import com.aa.loyalty.mileage.domain.AccountStatus;
import static org.junit.jupiter.api.Assertions.*;
import com.aa.loyalty.mileage.domain.FrozenMileageAccount;
import com.aa.loyalty.mileage.domain.MileageAccount;

/**
 * CHARACTERIZATION TEST (ENG-4.10) — LSP violation documented here.
 * 
 * ORIGINAL VIOLATION: FrozenMileageAccount extends MileageAccount and throws
 * IllegalStateException from addMiles()/deductMiles(), breaking the base class contract.
 * 
 * POST-FIX (Phase 5): FrozenMileageAccount is removed. Frozen state is modeled
 * as a boolean flag + freeze() method on MileageAccount itself. AccrualService
 * checks isFrozen() before calling addMiles(). No subtype surprises at runtime.
 */
class FrozenMileageAccountTest {

    @Test
    void frozenAccount_addMiles_throwsIllegalStateException() {
        MileageAccount account = new MileageAccount("AA-FROZEN-001");
        account.freeze("Fraud investigation");
        assertThrows(IllegalStateException.class, () -> account.addMiles(1000L));
    }

    @Test
    void frozenAccount_deductMiles_throwsIllegalStateException() {
        MileageAccount account = new MileageAccount("AA-FROZEN-002");
        account.freeze("Compliance hold");
        assertThrows(IllegalStateException.class, () -> account.deductMiles(500L));
    }

    @Test
    void frozenAccount_getTotalMiles_stillWorks() {
        MileageAccount account = new MileageAccount("AA-FROZEN-003");
        account.setTotalMiles(5000L);
        account.freeze("Disputed transaction");
        assertEquals(5000L, account.getTotalMiles());
    }

    @Test
    void frozenAccount_isFrozen_returnsTrue() {
        MileageAccount account = new MileageAccount("AA-FROZEN-004");
        assertFalse(account.isFrozen());
        account.freeze("Test freeze");
        assertTrue(account.isFrozen());
    }

    @Test
    void frozenAccount_statusSetToFrozen() {
        MileageAccount account = new MileageAccount("AA-FROZEN-005");
        assertEquals(AccountStatus.ACTIVE, account.getStatus());
        account.freeze("Security hold");
        assertEquals(AccountStatus.FROZEN, account.getStatus());
    }

    @Test
    void frozenAccount_getFreezeReason_returnsReason() {
        MileageAccount account = new MileageAccount("AA-FROZEN-006");
        account.freeze("Fraud case #1234");
        assertEquals("Fraud case #1234", account.getFreezeReason());
    }

    @Test
    void activeAccount_addMiles_succeeds() {
        MileageAccount account = new MileageAccount("AA-ACTIVE-001");
        account.addMiles(1000L);
        assertEquals(1000L, account.getTotalMiles());
    }

    @Test
    void activeAccount_deductMiles_succeeds() {
        MileageAccount account = new MileageAccount("AA-ACTIVE-002");
        account.setTotalMiles(5000L);
        account.deductMiles(1000L);
        assertEquals(4000L, account.getTotalMiles());
    }
}
