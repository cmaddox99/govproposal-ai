package com.aa.loyalty.events;

import com.aa.loyalty.tier.domain.TierStatus;
import org.junit.jupiter.api.Test;

import java.lang.reflect.Field;
import java.lang.reflect.Modifier;
import java.util.Date;

import static org.junit.jupiter.api.Assertions.*;

/**
 * ENG-3.2 — Verifies all domain events are immutable (all fields final, no setters).
 * ENG-4.1 — Tests written before event classes created (TDD).
 */
class DomainEventsTest {

    // ── MilesAccruedEvent ─────────────────────────────────────────────

    @Test
    void milesAccruedEvent_constructorSetsAllFields() {
        MilesAccruedEvent event = new MilesAccruedEvent("AA001", 1500L, "AA100", "FLIGHT");
        assertEquals("AA001", event.getMemberNumber());
        assertEquals(1500L, event.getMiles());
        assertEquals("AA100", event.getTransactionRef());
        assertEquals("FLIGHT", event.getSource());
        assertNotNull(event.getOccurredOn());
    }

    @Test
    void milesAccruedEvent_partnerSource() {
        MilesAccruedEvent event = new MilesAccruedEvent("AA002", 200L, "TXN-REF", "PARTNER");
        assertEquals("PARTNER", event.getSource());
        assertEquals("TXN-REF", event.getTransactionRef());
    }

    @Test
    void milesAccruedEvent_occurredOn_returnsDefensiveCopy() {
        MilesAccruedEvent event = new MilesAccruedEvent("AA001", 1500L, "AA100", "FLIGHT");
        Date d1 = event.getOccurredOn();
        Date d2 = event.getOccurredOn();
        assertEquals(d1, d2);
        assertNotSame(d1, d2);
    }

    @Test
    void milesAccruedEvent_allFieldsFinal() {
        assertAllFieldsFinal(MilesAccruedEvent.class);
    }

    @Test
    void milesAccruedEvent_noSetterMethods() {
        assertNoSetters(MilesAccruedEvent.class);
    }

    // ── TierChangedEvent ─────────────────────────────────────────────

    @Test
    void tierChangedEvent_constructorSetsAllFields() {
        TierChangedEvent event = new TierChangedEvent("AA001", TierStatus.GENERAL, TierStatus.GOLD);
        assertEquals("AA001", event.getMemberNumber());
        assertEquals(TierStatus.GENERAL, event.getPreviousTier());
        assertEquals(TierStatus.GOLD, event.getNewTier());
        assertNotNull(event.getOccurredOn());
    }

    @Test
    void tierChangedEvent_occurredOn_returnsDefensiveCopy() {
        TierChangedEvent event = new TierChangedEvent("AA001", TierStatus.GENERAL, TierStatus.GOLD);
        Date d1 = event.getOccurredOn();
        Date d2 = event.getOccurredOn();
        assertNotSame(d1, d2);
    }

    @Test
    void tierChangedEvent_allFieldsFinal() {
        assertAllFieldsFinal(TierChangedEvent.class);
    }

    @Test
    void tierChangedEvent_noSetterMethods() {
        assertNoSetters(TierChangedEvent.class);
    }

    // ── MilesRedeemedEvent ───────────────────────────────────────────

    @Test
    void milesRedeemedEvent_constructorSetsAllFields() {
        MilesRedeemedEvent event = new MilesRedeemedEvent("AA001", 25000L, "AWARD_FLIGHT");
        assertEquals("AA001", event.getMemberNumber());
        assertEquals(25000L, event.getMiles());
        assertEquals("AWARD_FLIGHT", event.getAwardCategory());
        assertNotNull(event.getOccurredOn());
    }

    @Test
    void milesRedeemedEvent_occurredOn_returnsDefensiveCopy() {
        MilesRedeemedEvent event = new MilesRedeemedEvent("AA001", 25000L, "AWARD_FLIGHT");
        assertNotSame(event.getOccurredOn(), event.getOccurredOn());
    }

    @Test
    void milesRedeemedEvent_allFieldsFinal() {
        assertAllFieldsFinal(MilesRedeemedEvent.class);
    }

    @Test
    void milesRedeemedEvent_noSetterMethods() {
        assertNoSetters(MilesRedeemedEvent.class);
    }

    // ── MilesExpiredEvent ────────────────────────────────────────────

    @Test
    void milesExpiredEvent_constructorSetsAllFields() {
        MilesExpiredEvent event = new MilesExpiredEvent("AA001", 5000L);
        assertEquals("AA001", event.getMemberNumber());
        assertEquals(5000L, event.getExpiredMiles());
        assertNotNull(event.getOccurredOn());
    }

    @Test
    void milesExpiredEvent_occurredOn_returnsDefensiveCopy() {
        MilesExpiredEvent event = new MilesExpiredEvent("AA001", 5000L);
        assertNotSame(event.getOccurredOn(), event.getOccurredOn());
    }

    @Test
    void milesExpiredEvent_allFieldsFinal() {
        assertAllFieldsFinal(MilesExpiredEvent.class);
    }

    @Test
    void milesExpiredEvent_noSetterMethods() {
        assertNoSetters(MilesExpiredEvent.class);
    }

    // ── AccountFrozenEvent ───────────────────────────────────────────

    @Test
    void accountFrozenEvent_constructorSetsAllFields() {
        AccountFrozenEvent event = new AccountFrozenEvent("AA001", "fraud investigation");
        assertEquals("AA001", event.getMemberNumber());
        assertEquals("fraud investigation", event.getReason());
        assertNotNull(event.getOccurredOn());
    }

    @Test
    void accountFrozenEvent_occurredOn_returnsDefensiveCopy() {
        AccountFrozenEvent event = new AccountFrozenEvent("AA001", "fraud");
        assertNotSame(event.getOccurredOn(), event.getOccurredOn());
    }

    @Test
    void accountFrozenEvent_allFieldsFinal() {
        assertAllFieldsFinal(AccountFrozenEvent.class);
    }

    @Test
    void accountFrozenEvent_noSetterMethods() {
        assertNoSetters(AccountFrozenEvent.class);
    }

    // ── MemberEnrolledEvent ──────────────────────────────────────────

    @Test
    void memberEnrolledEvent_constructorSetsAllFields() {
        Date enrollmentDate = new Date(1000000L);
        MemberEnrolledEvent event = new MemberEnrolledEvent("AA001", "test@aa.com", enrollmentDate);
        assertEquals("AA001", event.getMemberNumber());
        assertEquals("test@aa.com", event.getEmail());
        assertEquals(enrollmentDate, event.getEnrollmentDate());
        assertNotNull(event.getOccurredOn());
    }

    @Test
    void memberEnrolledEvent_nullEnrollmentDate_handledGracefully() {
        MemberEnrolledEvent event = new MemberEnrolledEvent("AA001", "test@aa.com", null);
        assertNull(event.getEnrollmentDate());
        assertNotNull(event.getOccurredOn());
    }

    @Test
    void memberEnrolledEvent_enrollmentDate_returnsDefensiveCopy() {
        Date enrollmentDate = new Date(1000000L);
        MemberEnrolledEvent event = new MemberEnrolledEvent("AA001", "test@aa.com", enrollmentDate);
        assertNotSame(enrollmentDate, event.getEnrollmentDate());
        assertNotSame(event.getEnrollmentDate(), event.getEnrollmentDate());
    }

    @Test
    void memberEnrolledEvent_occurredOn_returnsDefensiveCopy() {
        MemberEnrolledEvent event = new MemberEnrolledEvent("AA001", "test@aa.com", new Date());
        assertNotSame(event.getOccurredOn(), event.getOccurredOn());
    }

    @Test
    void memberEnrolledEvent_allFieldsFinal() {
        assertAllFieldsFinal(MemberEnrolledEvent.class);
    }

    @Test
    void memberEnrolledEvent_noSetterMethods() {
        assertNoSetters(MemberEnrolledEvent.class);
    }

    // ── Helpers ──────────────────────────────────────────────────────

    private void assertAllFieldsFinal(Class<?> clazz) {
        for (Field field : clazz.getDeclaredFields()) {
            if (field.isSynthetic()) continue; // skip JaCoCo / compiler-generated fields
            assertTrue(Modifier.isFinal(field.getModifiers()),
                "Field '" + field.getName() + "' in " + clazz.getSimpleName() + " must be final (ENG-3.2)");
        }
    }

    private void assertNoSetters(Class<?> clazz) {
        long setterCount = java.util.Arrays.stream(clazz.getDeclaredMethods())
            .filter(m -> m.getName().startsWith("set"))
            .count();
        assertEquals(0, setterCount,
            clazz.getSimpleName() + " must have no setter methods (ENG-3.2)");
    }
}
