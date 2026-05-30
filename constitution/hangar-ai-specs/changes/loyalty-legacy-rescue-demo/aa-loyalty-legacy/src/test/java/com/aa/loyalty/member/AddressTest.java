package com.aa.loyalty.member;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.aa.loyalty.member.domain.Address;

class AddressTest {

    @Test
    void constructor_setsAllFields() {
        Address address = new Address("100 Oak St", "Apt 2", "Dallas", "TX", "75201", "US");
        assertEquals("100 Oak St", address.getLine1());
        assertEquals("Apt 2", address.getLine2());
        assertEquals("Dallas", address.getCity());
        assertEquals("TX", address.getState());
        assertEquals("75201", address.getPostalCode());
        assertEquals("US", address.getCountry());
    }

    @Test
    void equals_sameValues_returnsTrue() {
        Address a1 = new Address("100 Oak St", null, "Dallas", "TX", "75201", "US");
        Address a2 = new Address("100 Oak St", null, "Dallas", "TX", "75201", "US");
        assertEquals(a1, a2);
    }

    @Test
    void equals_differentLine1_returnsFalse() {
        Address a1 = new Address("100 Oak St", null, "Dallas", "TX", "75201", "US");
        Address a2 = new Address("200 Elm St", null, "Dallas", "TX", "75201", "US");
        assertNotEquals(a1, a2);
    }

    @Test
    void equals_nullFields_returnsTrueWhenBothNull() {
        Address a1 = new Address(null, null, null, null, null, null);
        Address a2 = new Address(null, null, null, null, null, null);
        assertEquals(a1, a2);
    }

    @Test
    void hashCode_sameValues_sameHash() {
        Address a1 = new Address("100 Oak St", null, "Dallas", "TX", "75201", "US");
        Address a2 = new Address("100 Oak St", null, "Dallas", "TX", "75201", "US");
        assertEquals(a1.hashCode(), a2.hashCode());
    }

    @Test
    void equals_null_returnsFalse() {
        Address a = new Address("100 Oak St", null, "Dallas", "TX", "75201", "US");
        assertNotEquals(null, a);
    }

    @Test
    void equals_differentType_returnsFalse() {
        Address a = new Address("100 Oak St", null, "Dallas", "TX", "75201", "US");
        assertNotEquals("not an address", a);
    }

    @Test
    void equals_sameInstance_returnsTrue() {
        Address a = new Address("100 Oak St", null, "Dallas", "TX", "75201", "US");
        assertEquals(a, a);
    }

    // ENG-4.1 — covering each && branch in equals() for full branch coverage
    @Test
    void equals_differentCity_returnsFalse() {
        Address a1 = new Address("100 Oak St", null, "Dallas", "TX", "75201", "US");
        Address a2 = new Address("100 Oak St", null, "Austin", "TX", "75201", "US");
        assertNotEquals(a1, a2);
    }

    @Test
    void equals_differentState_returnsFalse() {
        Address a1 = new Address("100 Oak St", null, "Dallas", "TX", "75201", "US");
        Address a2 = new Address("100 Oak St", null, "Dallas", "CA", "75201", "US");
        assertNotEquals(a1, a2);
    }

    @Test
    void equals_differentPostalCode_returnsFalse() {
        Address a1 = new Address("100 Oak St", null, "Dallas", "TX", "75201", "US");
        Address a2 = new Address("100 Oak St", null, "Dallas", "TX", "90210", "US");
        assertNotEquals(a1, a2);
    }

    @Test
    void equals_differentCountry_returnsFalse() {
        Address a1 = new Address("100 Oak St", null, "Dallas", "TX", "75201", "US");
        Address a2 = new Address("100 Oak St", null, "Dallas", "TX", "75201", "MX");
        assertNotEquals(a1, a2);
    }

    @Test
    void equals_differentLine2_returnsFalse() {
        Address a1 = new Address("100 Oak St", "Apt 1", "Dallas", "TX", "75201", "US");
        Address a2 = new Address("100 Oak St", "Apt 2", "Dallas", "TX", "75201", "US");
        assertNotEquals(a1, a2);
    }
}
