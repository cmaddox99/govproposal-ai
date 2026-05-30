package com.aa.loyalty.member;

import javax.persistence.*;
import java.util.Date;

@Entity
@Table(name = "MEMBER")
public class Member {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "member_seq")
    @SequenceGenerator(name = "member_seq", sequenceName = "MEMBER_SEQ", allocationSize = 1)
    private Long id;

    @Column(name = "MEMBER_NUMBER", nullable = false, unique = true, length = 12)
    private String memberNumber;

    @Column(name = "FIRST_NAME", length = 50)
    private String firstName;

    @Column(name = "LAST_NAME", length = 50)
    private String lastName;

    @Column(name = "EMAIL", length = 100)
    private String email;  // VIOLATION: no @Email validation

    @Column(name = "PHONE", length = 20)
    private String phone;

    @Column(name = "DATE_OF_BIRTH")
    @Temporal(TemporalType.DATE)
    private Date dateOfBirth;

    @Column(name = "TIER_STATUS", length = 20)
    private String tierStatus = "GENERAL";

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

    @Column(name = "ADDRESS_LINE1", length = 100)
    private String addressLine1;

    @Column(name = "ADDRESS_LINE2", length = 100)
    private String addressLine2;

    @Column(name = "CITY", length = 50)
    private String city;

    @Column(name = "STATE", length = 10)
    private String state;

    @Column(name = "POSTAL_CODE", length = 10)
    private String postalCode;

    @Column(name = "COUNTRY", length = 3)
    private String country;

    public Member() {}

    public Long getId() { return id; }
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
    public String getTierStatus() { return tierStatus; }
    public void setTierStatus(String tierStatus) { this.tierStatus = tierStatus; }
    public Date getEnrollmentDate() { return enrollmentDate; }
    public void setEnrollmentDate(Date enrollmentDate) { this.enrollmentDate = enrollmentDate; }
    public Date getLastUpdated() { return lastUpdated; }
    public void setLastUpdated(Date lastUpdated) { this.lastUpdated = lastUpdated; }
    public Boolean getActive() { return active; }
    public void setActive(Boolean active) { this.active = active; }
    public String getPreferredLanguage() { return preferredLanguage; }
    public void setPreferredLanguage(String preferredLanguage) { this.preferredLanguage = preferredLanguage; }
    public String getAddressLine1() { return addressLine1; }
    public void setAddressLine1(String addressLine1) { this.addressLine1 = addressLine1; }
    public String getAddressLine2() { return addressLine2; }
    public void setAddressLine2(String addressLine2) { this.addressLine2 = addressLine2; }
    public String getCity() { return city; }
    public void setCity(String city) { this.city = city; }
    public String getState() { return state; }
    public void setState(String state) { this.state = state; }
    public String getPostalCode() { return postalCode; }
    public void setPostalCode(String postalCode) { this.postalCode = postalCode; }
    public String getCountry() { return country; }
    public void setCountry(String country) { this.country = country; }
}
