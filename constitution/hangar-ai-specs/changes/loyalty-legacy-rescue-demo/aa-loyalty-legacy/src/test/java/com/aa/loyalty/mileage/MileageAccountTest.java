package com.aa.loyalty.mileage;

// CHARACTERIZATION TEST — ENG-4.10
import org.junit.jupiter.api.Test;
import java.util.Date;
import static org.junit.jupiter.api.Assertions.*;

class MileageAccountTest {

    @Test
    void defaultConstructor_setsDefaultValues() {
        MileageAccount account = new MileageAccount();
        assertNull(account.getMemberNumber());
        assertEquals(0L, account.getTotalMiles());
        assertEquals(0L, account.getQualifyingMiles());
        assertEquals(0L, account.getEliteQualifyingMiles());
        assertEquals(0, account.getEliteQualifyingSegments());
        assertEquals("ACTIVE", account.getStatus());
        assertNotNull(account.getTransactions());
        assertTrue(account.getTransactions().isEmpty());
    }

    @Test
    void paramConstructor_setsMemberNumberAndDates() {
        MileageAccount account = new MileageAccount("AA123456");
        assertEquals("AA123456", account.getMemberNumber());
        assertNotNull(account.getCreatedDate());
        assertNotNull(account.getMilesExpiryDate());
    }

    @Test
    void paramConstructor_setsExpiryTwoYearsOut() {
        long before = System.currentTimeMillis();
        MileageAccount account = new MileageAccount("AA123456");
        long after = System.currentTimeMillis();
        long twoYearsMs = 365L * 24 * 60 * 60 * 1000 * 2;
        assertTrue(account.getMilesExpiryDate().getTime() >= before + twoYearsMs - 1000);
        assertTrue(account.getMilesExpiryDate().getTime() <= after + twoYearsMs + 1000);
    }

    @Test
    void setTotalMiles_updatesValue() {
        MileageAccount account = new MileageAccount("AA001");
        account.setTotalMiles(5000L);
        assertEquals(5000L, account.getTotalMiles());
    }

    @Test
    void setStatus_updatesStatus() {
        MileageAccount account = new MileageAccount("AA001");
        account.setStatus("MILES_EXPIRED");
        assertEquals("MILES_EXPIRED", account.getStatus());
    }

    @Test
    void setLastActivityDate_updatesDate() {
        MileageAccount account = new MileageAccount("AA001");
        Date now = new Date();
        account.setLastActivityDate(now);
        assertEquals(now, account.getLastActivityDate());
    }

    @Test
    void setEliteQualifyingMiles_updatesValue() {
        MileageAccount account = new MileageAccount("AA001");
        account.setEliteQualifyingMiles(25000L);
        assertEquals(25000L, account.getEliteQualifyingMiles());
    }

    @Test
    void setEliteQualifyingSegments_updatesValue() {
        MileageAccount account = new MileageAccount("AA001");
        account.setEliteQualifyingSegments(30);
        assertEquals(30, account.getEliteQualifyingSegments());
    }

    @Test
    void setMemberNumber_updatesValue() {
        MileageAccount account = new MileageAccount("AA001");
        account.setMemberNumber("AA999");
        assertEquals("AA999", account.getMemberNumber());
    }

    @Test
    void setMilesExpiryDate_updatesValue() {
        MileageAccount account = new MileageAccount("AA001");
        java.util.Date d = new java.util.Date();
        account.setMilesExpiryDate(d);
        assertEquals(d, account.getMilesExpiryDate());
    }

    @Test
    void setTransactions_updatesValue() {
        MileageAccount account = new MileageAccount("AA001");
        java.util.List<com.aa.loyalty.mileage.MileageTransaction> txns = new java.util.ArrayList<>();
        account.setTransactions(txns);
        assertSame(txns, account.getTransactions());
    }
}
