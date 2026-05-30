package com.aa.loyalty.member;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.aa.loyalty.member.domain.EmailAddress;

class EmailAddressTest {

    @Test
    void constructor_validEmail_setsValue() {
        EmailAddress email = new EmailAddress("test@aa.com");
        assertEquals("test@aa.com", email.getValue());
    }

    @Test
    void constructor_upperCaseEmail_normalizesToLowerCase() {
        EmailAddress email = new EmailAddress("TEST@AA.COM");
        assertEquals("test@aa.com", email.getValue());
    }

    @Test
    void constructor_null_throwsIllegalArgumentException() {
        assertThrows(IllegalArgumentException.class, () -> new EmailAddress(null));
    }

    @Test
    void constructor_noAtSign_throwsIllegalArgumentException() {
        assertThrows(IllegalArgumentException.class, () -> new EmailAddress("notanemail"));
    }

    @Test
    void constructor_noDomain_throwsIllegalArgumentException() {
        assertThrows(IllegalArgumentException.class, () -> new EmailAddress("test@"));
    }

    @Test
    void constructor_noTld_throwsIllegalArgumentException() {
        assertThrows(IllegalArgumentException.class, () -> new EmailAddress("test@domain"));
    }

    @Test
    void equals_sameValue_returnsTrue() {
        assertEquals(new EmailAddress("test@aa.com"), new EmailAddress("TEST@AA.COM"));
    }

    @Test
    void equals_differentValue_returnsFalse() {
        assertNotEquals(new EmailAddress("a@aa.com"), new EmailAddress("b@aa.com"));
    }

    @Test
    void hashCode_sameValue_sameHash() {
        assertEquals(new EmailAddress("x@aa.com").hashCode(), new EmailAddress("X@AA.COM").hashCode());
    }

    @Test
    void toString_returnsValue() {
        assertEquals("test@aa.com", new EmailAddress("test@aa.com").toString());
    }
}
