package com.aa.loyalty.mileage;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.aa.loyalty.mileage.domain.TransactionType;

class TransactionTypeTest {

    @Test
    void allFourValuesExist() {
        assertEquals(4, TransactionType.values().length);
    }

    @Test
    void valueOf_accrual_returnsAccrual() {
        assertEquals(TransactionType.ACCRUAL, TransactionType.valueOf("ACCRUAL"));
    }

    @Test
    void valueOf_redemption_returnsRedemption() {
        assertEquals(TransactionType.REDEMPTION, TransactionType.valueOf("REDEMPTION"));
    }

    @Test
    void valueOf_adjustment_returnsAdjustment() {
        assertEquals(TransactionType.ADJUSTMENT, TransactionType.valueOf("ADJUSTMENT"));
    }

    @Test
    void valueOf_expiry_returnsExpiry() {
        assertEquals(TransactionType.EXPIRY, TransactionType.valueOf("EXPIRY"));
    }

    @Test
    void name_accrual_matchesDbString() {
        assertEquals("ACCRUAL", TransactionType.ACCRUAL.name());
    }

    @Test
    void name_redemption_matchesDbString() {
        assertEquals("REDEMPTION", TransactionType.REDEMPTION.name());
    }

    @Test
    void name_adjustment_matchesDbString() {
        assertEquals("ADJUSTMENT", TransactionType.ADJUSTMENT.name());
    }

    @Test
    void name_expiry_matchesDbString() {
        assertEquals("EXPIRY", TransactionType.EXPIRY.name());
    }
}
