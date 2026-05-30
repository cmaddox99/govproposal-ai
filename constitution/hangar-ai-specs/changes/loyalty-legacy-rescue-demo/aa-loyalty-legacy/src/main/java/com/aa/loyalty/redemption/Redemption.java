package com.aa.loyalty.redemption;

import javax.persistence.*;
import java.util.Date;

@Entity
@Table(name = "REDEMPTION")
public class Redemption {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "redemption_seq")
    @SequenceGenerator(name = "redemption_seq", sequenceName = "REDEMPTION_SEQ", allocationSize = 1)
    private Long id;

    @Column(name = "MEMBER_NUMBER", nullable = false, length = 12)
    private String memberNumber;

    @Column(name = "REDEMPTION_TYPE", length = 30)
    private String redemptionType;  // AWARD_FLIGHT, UPGRADE, GIFT_CARD, PARTNER

    @Column(name = "MILES_COST")
    private Long milesCost;

    @Column(name = "CASH_COPAY")
    private Double cashCopay;

    @Column(name = "STATUS", length = 20)
    private String status;  // PENDING, CONFIRMED, CANCELLED, EXPIRED

    @Column(name = "RESERVATION_CODE", length = 10)
    private String reservationCode;

    @Column(name = "REDEMPTION_DATE")
    @Temporal(TemporalType.TIMESTAMP)
    private Date redemptionDate;

    @Column(name = "TRAVEL_DATE")
    @Temporal(TemporalType.DATE)
    private Date travelDate;

    @Column(name = "ORIGIN", length = 3)
    private String origin;

    @Column(name = "DESTINATION", length = 3)
    private String destination;

    @Column(name = "CABIN_CLASS", length = 10)
    private String cabinClass;

    @Column(name = "NOTES", length = 1000)
    private String notes;

    public Redemption() {}

    public Long getId() { return id; }
    public String getMemberNumber() { return memberNumber; }
    public void setMemberNumber(String memberNumber) { this.memberNumber = memberNumber; }
    public String getRedemptionType() { return redemptionType; }
    public void setRedemptionType(String redemptionType) { this.redemptionType = redemptionType; }
    public Long getMilesCost() { return milesCost; }
    public void setMilesCost(Long milesCost) { this.milesCost = milesCost; }
    public Double getCashCopay() { return cashCopay; }
    public void setCashCopay(Double cashCopay) { this.cashCopay = cashCopay; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
    public String getReservationCode() { return reservationCode; }
    public void setReservationCode(String reservationCode) { this.reservationCode = reservationCode; }
    public Date getRedemptionDate() { return redemptionDate; }
    public void setRedemptionDate(Date redemptionDate) { this.redemptionDate = redemptionDate; }
    public Date getTravelDate() { return travelDate; }
    public void setTravelDate(Date travelDate) { this.travelDate = travelDate; }
    public String getOrigin() { return origin; }
    public void setOrigin(String origin) { this.origin = origin; }
    public String getDestination() { return destination; }
    public void setDestination(String destination) { this.destination = destination; }
    public String getCabinClass() { return cabinClass; }
    public void setCabinClass(String cabinClass) { this.cabinClass = cabinClass; }
    public String getNotes() { return notes; }
    public void setNotes(String notes) { this.notes = notes; }
}
