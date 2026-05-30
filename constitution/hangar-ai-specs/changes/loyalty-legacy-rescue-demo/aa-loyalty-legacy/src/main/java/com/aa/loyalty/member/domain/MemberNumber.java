package com.aa.loyalty.member.domain;

import java.util.Objects;
import java.util.regex.Pattern;

public final class MemberNumber {

    private static final Pattern PATTERN =
        Pattern.compile("^[A-Z]{2}\\d{9}$");

    private final String value;

    public MemberNumber(String value) {
        if (value == null || !PATTERN.matcher(value).matches()) {
            throw new IllegalArgumentException("Invalid member number: " + value);
        }
        this.value = value;
    }

    public String getValue() { return value; }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof MemberNumber)) return false;
        return Objects.equals(value, ((MemberNumber) o).value);
    }

    @Override
    public int hashCode() { return Objects.hash(value); }

    @Override
    public String toString() { return value; }
}
