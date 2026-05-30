package com.aa.loyalty.member.domain;

import javax.persistence.Column;
import javax.persistence.Embeddable;
import java.util.Objects;

@Embeddable
public final class Address {

    @Column(name = "ADDRESS_LINE1", length = 100)
    private final String line1;

    @Column(name = "ADDRESS_LINE2", length = 100)
    private final String line2;

    @Column(name = "CITY", length = 50)
    private final String city;

    @Column(name = "STATE", length = 10)
    private final String state;

    @Column(name = "POSTAL_CODE", length = 10)
    private final String postalCode;

    @Column(name = "COUNTRY", length = 3)
    private final String country;

    protected Address() {
        this.line1 = null;
        this.line2 = null;
        this.city = null;
        this.state = null;
        this.postalCode = null;
        this.country = null;
    }

    public Address(String line1, String line2, String city, String state,
                   String postalCode, String country) {
        this.line1 = line1;
        this.line2 = line2;
        this.city = city;
        this.state = state;
        this.postalCode = postalCode;
        this.country = country;
    }

    public String getLine1() { return line1; }
    public String getLine2() { return line2; }
    public String getCity() { return city; }
    public String getState() { return state; }
    public String getPostalCode() { return postalCode; }
    public String getCountry() { return country; }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Address)) return false;
        Address that = (Address) o;
        return Objects.equals(line1, that.line1)
            && Objects.equals(line2, that.line2)
            && Objects.equals(city, that.city)
            && Objects.equals(state, that.state)
            && Objects.equals(postalCode, that.postalCode)
            && Objects.equals(country, that.country);
    }

    @Override
    public int hashCode() {
        return Objects.hash(line1, line2, city, state, postalCode, country);
    }
}
