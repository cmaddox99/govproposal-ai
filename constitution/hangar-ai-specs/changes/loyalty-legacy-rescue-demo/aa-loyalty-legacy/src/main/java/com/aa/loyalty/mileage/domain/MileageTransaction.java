package com.aa.loyalty.mileage.domain;

import javax.persistence.*;
import java.util.Date;
import java.util.UUID;

@Entity
@Table(name = "MILEAGE_TRANSACTION")
public class MileageTransaction {

    @Id
    @Column(updatable = false, nullable = false)
    private UUID id = UUID.randomUUID();

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "ACCOUNT_ID", nullable = false)
    private MileageAccount account;

    @Enumerated(EnumType.STRING)
    @Column(name = "TRANSACTION_TYPE", length = 20)
    private TransactionType transactionType;

    @Column(name = "MILES_AMOUNT")
    private Long milesAmount;

    @Column(name = "QUALIFYING")
    private Boolean qualifying = false;

    @Column(name = "FLIGHT_NUMBER", length = 10)
    private String flightNumber;

    @Column(name = "ORIGIN", length = 3)
    private String origin;

    @Column(name = "DESTINATION", length = 3)
    private String destination;

    @Column(name = "FLIGHT_DATE")
    @Temporal(TemporalType.DATE)
    private Date flightDate;

    @Column(name = "PARTNER_CODE", length = 10)
    private String partnerCode;

    @Column(name = "BOOKING_CLASS", length = 2)
    private String bookingClass;

    @Column(name = "FARE_BASIS", length = 20)
    private String fareBasis;

    @Column(name = "TICKET_NUMBER", length = 20)
    private String ticketNumber;

    @Column(name = "TRANSACTION_DATE")
    @Temporal(TemporalType.TIMESTAMP)
    private Date transactionDate;

    @Column(name = "DESCRIPTION", length = 500)
    private String description;

    @Column(name = "REVERSAL_FLAG")
    private Boolean reversalFlag = false;

    @Column(name = "ORIGINAL_TXN_ID")
    private Long originalTransactionId;

    public MileageTransaction() {
        // required by JPA
    }

    public UUID getId() { return id; }
    public MileageAccount getAccount() { return account; }
    public void setAccount(MileageAccount account) { this.account = account; }
    public TransactionType getTransactionType() { return transactionType; }
    public void setTransactionType(TransactionType transactionType) { this.transactionType = transactionType; }
    public Long getMilesAmount() { return milesAmount; }
    public void setMilesAmount(Long milesAmount) { this.milesAmount = milesAmount; }
    public Boolean getQualifying() { return qualifying; }
    public void setQualifying(Boolean qualifying) { this.qualifying = qualifying; }
    public String getFlightNumber() { return flightNumber; }
    public void setFlightNumber(String flightNumber) { this.flightNumber = flightNumber; }
    public String getOrigin() { return origin; }
    public void setOrigin(String origin) { this.origin = origin; }
    public String getDestination() { return destination; }
    public void setDestination(String destination) { this.destination = destination; }
    public Date getFlightDate() { return flightDate; }
    public void setFlightDate(Date flightDate) { this.flightDate = flightDate; }
    public String getPartnerCode() { return partnerCode; }
    public void setPartnerCode(String partnerCode) { this.partnerCode = partnerCode; }
    public String getBookingClass() { return bookingClass; }
    public void setBookingClass(String bookingClass) { this.bookingClass = bookingClass; }
    public String getFareBasis() { return fareBasis; }
    public void setFareBasis(String fareBasis) { this.fareBasis = fareBasis; }
    public String getTicketNumber() { return ticketNumber; }
    public void setTicketNumber(String ticketNumber) { this.ticketNumber = ticketNumber; }
    public Date getTransactionDate() { return transactionDate; }
    public void setTransactionDate(Date transactionDate) { this.transactionDate = transactionDate; }
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    public Boolean getReversalFlag() { return reversalFlag; }
    public void setReversalFlag(Boolean reversalFlag) { this.reversalFlag = reversalFlag; }
    public Long getOriginalTransactionId() { return originalTransactionId; }
    public void setOriginalTransactionId(Long originalTransactionId) { this.originalTransactionId = originalTransactionId; }
}
