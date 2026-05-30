package com.aa.loyalty.member.domain;

import java.util.Locale;
import java.util.Objects;
import java.util.regex.Pattern;

public final class EmailAddress {

    // Bounded quantifiers prevent ReDoS; RFC 5321: local part ≤64, domain ≤253 chars with required dot.
    private static final Pattern PATTERN =
        Pattern.compile("^[^@\\s]{1,64}@[^@\\s.]{1,63}(\\.[^@\\s.]{1,63}){1,4}$");

    private final String value;

    public EmailAddress(String value) {
        if (value == null || !PATTERN.matcher(value).matches()) {
            throw new IllegalArgumentException("Invalid email: " + value);
        }
        this.value = value.toLowerCase(Locale.ROOT);
    }

    public String getValue() { return value; }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof EmailAddress)) return false;
        return Objects.equals(value, ((EmailAddress) o).value);
    }

    @Override
    public int hashCode() { return Objects.hash(value); }

    @Override
    public String toString() { return value; }
}
