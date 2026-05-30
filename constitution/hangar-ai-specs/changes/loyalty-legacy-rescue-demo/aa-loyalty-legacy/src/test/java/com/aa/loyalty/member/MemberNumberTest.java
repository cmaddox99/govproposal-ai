package com.aa.loyalty.member;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.aa.loyalty.member.domain.MemberNumber;

class MemberNumberTest {

    @Test
    void constructor_validFormat_setsValue() {
        MemberNumber mn = new MemberNumber("AA123456789");
        assertEquals("AA123456789", mn.getValue());
    }

    @Test
    void constructor_null_throwsIllegalArgumentException() {
        assertThrows(IllegalArgumentException.class, () -> new MemberNumber(null));
    }

    @Test
    void constructor_tooShort_throwsIllegalArgumentException() {
        assertThrows(IllegalArgumentException.class, () -> new MemberNumber("AA12345"));
    }

    @Test
    void constructor_lowercaseLetters_throwsIllegalArgumentException() {
        assertThrows(IllegalArgumentException.class, () -> new MemberNumber("aa123456789"));
    }

    @Test
    void constructor_allDigits_throwsIllegalArgumentException() {
        assertThrows(IllegalArgumentException.class, () -> new MemberNumber("12345678901"));
    }

    @Test
    void constructor_wrongPrefixFormat_throwsIllegalArgumentException() {
        assertThrows(IllegalArgumentException.class, () -> new MemberNumber("A1234567890"));
    }

    @Test
    void equals_sameValue_returnsTrue() {
        assertEquals(new MemberNumber("AA123456789"), new MemberNumber("AA123456789"));
    }

    @Test
    void equals_differentValue_returnsFalse() {
        assertNotEquals(new MemberNumber("AA123456789"), new MemberNumber("BB987654321"));
    }

    @Test
    void hashCode_sameValue_sameHash() {
        assertEquals(new MemberNumber("AA123456789").hashCode(), new MemberNumber("AA123456789").hashCode());
    }

    @Test
    void toString_returnsValue() {
        assertEquals("AA123456789", new MemberNumber("AA123456789").toString());
    }
}
