package com.aa.loyalty.member.domain;

import com.aa.loyalty.tier.domain.TierStatus;
import javax.persistence.*;
import java.util.Date;
import java.util.UUID;

@Entity
@Table(name = "MEMBER")
public class Member {

    @Id
    @Column(updatable = false, nullable = false)
    private UUID id = UUID.randomUUID();

    @Column(name = "MEMBER_NUMBER", nullable = false, unique = true, length = 20)
    private String memberNumber;

    @Column(name = "FIRST_NAME", length = 50)
    private String firstName;

    @Column(name = "LAST_NAME", length = 50)
    private String lastName;

    @Column(name = "EMAIL", length = 100)
    private String email;

    @Column(name = "PHONE", length = 20)
    private String phone;

    @Column(name = "DATE_OF_BIRTH")
    @Temporal(TemporalType.DATE)
    private Date dateOfBirth;

    @Enumerated(EnumType.STRING)
    @Column(name = "TIER_STATUS", length = 20)
    private TierStatus tierStatus = TierStatus.GENERAL;

    @Column(name = "ENROLLMENT_DATE")
    @Temporal(TemporalType.TIMESTAMP)
    private Date enrollmentDate;

    @Column(name = "LAST_UPDATED")
    @Temporal(TemporalType.TIMESTAMP)
    private Date lastUpdated;

    @Column(name = "ACTIVE")
    private Boolean active = true;

    @Column(name = "PREFERRED_LANGUAGE", length = 5)
    private String preferredLanguage = "en";

    @Embedded
    private Address address = new Address(null, null, null, null, null, null);

    public Member() {
        // required by JPA
    }

    public UUID getId() { return id; }
    public String getMemberNumber() { return memberNumber; }
    public void setMemberNumber(String memberNumber) { this.memberNumber = memberNumber; }
    public String getFirstName() { return firstName; }
    public void setFirstName(String firstName) { this.firstName = firstName; }
    public String getLastName() { return lastName; }
    public void setLastName(String lastName) { this.lastName = lastName; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    public String getPhone() { return phone; }
    public void setPhone(String phone) { this.phone = phone; }
    public Date getDateOfBirth() { return dateOfBirth; }
    public void setDateOfBirth(Date dateOfBirth) { this.dateOfBirth = dateOfBirth; }
    public TierStatus getTierStatus() { return tierStatus; }
    public void setTierStatus(TierStatus tierStatus) { this.tierStatus = tierStatus; }
    public Date getEnrollmentDate() { return enrollmentDate; }
    public void setEnrollmentDate(Date enrollmentDate) { this.enrollmentDate = enrollmentDate; }
    public Date getLastUpdated() { return lastUpdated; }
    public void setLastUpdated(Date lastUpdated) { this.lastUpdated = lastUpdated; }
    public Boolean getActive() { return active; }
    public void setActive(Boolean active) { this.active = active; }
    public String getPreferredLanguage() { return preferredLanguage; }
    public void setPreferredLanguage(String preferredLanguage) { this.preferredLanguage = preferredLanguage; }

    public Address getAddress() { return address; }
    public void setAddress(Address address) { this.address = address; }

    // Backward-compatible delegation accessors for address fields
    public String getAddressLine1() { return address != null ? address.getLine1() : null; }
    public void setAddressLine1(String v) {
        this.address = new Address(v, getAddressLine2(), getCity(), getState(), getPostalCode(), getCountry());
    }
    public String getAddressLine2() { return address != null ? address.getLine2() : null; }
    public void setAddressLine2(String v) {
        this.address = new Address(getAddressLine1(), v, getCity(), getState(), getPostalCode(), getCountry());
    }
    public String getCity() { return address != null ? address.getCity() : null; }
    public void setCity(String v) {
        this.address = new Address(getAddressLine1(), getAddressLine2(), v, getState(), getPostalCode(), getCountry());
    }
    public String getState() { return address != null ? address.getState() : null; }
    public void setState(String v) {
        this.address = new Address(getAddressLine1(), getAddressLine2(), getCity(), v, getPostalCode(), getCountry());
    }
    public String getPostalCode() { return address != null ? address.getPostalCode() : null; }
    public void setPostalCode(String v) {
        this.address = new Address(getAddressLine1(), getAddressLine2(), getCity(), getState(), v, getCountry());
    }
    public String getCountry() { return address != null ? address.getCountry() : null; }
    public void setCountry(String v) {
        this.address = new Address(getAddressLine1(), getAddressLine2(), getCity(), getState(), getPostalCode(), v);
    }

    /**
     * ENG-2.1 — Factory method; ensures all required fields set at enrollment.
     */
    public static Member enroll(String firstName, String lastName, String email,
                                 String phone, Date dateOfBirth, String memberNumber) {
        Member m = new Member();
        m.firstName = firstName;
        m.lastName = lastName;
        m.email = email;
        m.phone = phone;
        m.dateOfBirth = dateOfBirth;
        m.memberNumber = memberNumber;
        m.enrollmentDate = new Date();
        m.lastUpdated = new Date();
        m.tierStatus = TierStatus.GENERAL;
        m.active = true;
        return m;
    }

    /**
     * ENG-2.1 — Deactivation is a domain operation, not a raw setter.
     */
    public void deactivate() {
        if (!Boolean.TRUE.equals(this.active)) {
            throw new IllegalStateException("Member is already deactivated: " + memberNumber);
        }
        this.active = false;
        this.lastUpdated = new Date();
    }

    /**
     * ENG-2.1 — Contact update validates email via EmailAddress VO.
     */
    public void updateContact(String email, String phone, Address address) {
        if (email != null) {
            new EmailAddress(email); // validates format — throws if invalid
            this.email = email;
        }
        if (phone != null) this.phone = phone;
        if (address != null) this.address = address;
        this.lastUpdated = new Date();
    }

    /**
     * ENG-2.1 — Tier transitions are domain behavior.
     */
    public void upgradeTier(TierStatus newTier) {
        if (newTier == null) throw new IllegalArgumentException("New tier cannot be null");
        if (newTier.ordinal() <= this.tierStatus.ordinal()) {
            throw new IllegalStateException(
                "upgradeTier() cannot downgrade: " + this.tierStatus + " -> " + newTier
            );
        }
        this.tierStatus = newTier;
        this.lastUpdated = new Date();
    }

    public void resetTierToGeneral() {
        this.tierStatus = TierStatus.GENERAL;
        this.lastUpdated = new Date();
    }
}
