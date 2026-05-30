package com.aa.loyalty.mileage.domain;

import javax.persistence.*;
import java.util.Date;
import java.util.List;
import java.util.ArrayList;
import java.util.UUID;

@Entity
@Table(name = "MILEAGE_ACCOUNT")
public class MileageAccount {

    @Id
    @Column(updatable = false, nullable = false)
    private UUID id = UUID.randomUUID();

    @Column(name = "MEMBER_NUMBER", nullable = false, unique = true, length = 12)
    private String memberNumber;

    @Column(name = "TOTAL_MILES")
    private Long totalMiles = 0L;

    @Column(name = "QUALIFYING_MILES")
    private Long qualifyingMiles = 0L;

    @Column(name = "ELITE_QUALIFYING_MILES")
    private Long eliteQualifyingMiles = 0L;

    @Column(name = "ELITE_QUALIFYING_SEGMENTS")
    private Integer eliteQualifyingSegments = 0;

    @Column(name = "MILES_EXPIRY_DATE")
    @Temporal(TemporalType.DATE)
    private Date milesExpiryDate;

    @Column(name = "LAST_ACTIVITY_DATE")
    @Temporal(TemporalType.TIMESTAMP)
    private Date lastActivityDate;

    @Column(name = "CREATED_DATE")
    @Temporal(TemporalType.TIMESTAMP)
    private Date createdDate;

    @Enumerated(EnumType.STRING)
    @Column(name = "STATUS", length = 20)
    private AccountStatus status = AccountStatus.ACTIVE;

    @Column(name = "FROZEN")
    private boolean frozen = false;

    @Column(name = "FREEZE_REASON", length = 255)
    private String freezeReason;

    @OneToMany(mappedBy = "account", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<MileageTransaction> transactions = new ArrayList<>();

    // VIOLATION: no-arg constructor leaks - status not validated on set
    public MileageAccount() {}

    public MileageAccount(String memberNumber) {
        this.memberNumber = memberNumber;
        this.createdDate = new Date();
        this.milesExpiryDate = new Date(System.currentTimeMillis() + (365L * 24 * 60 * 60 * 1000 * 2));
    }

    // VIOLATION: mutable Date returned directly — exposes internal state
    public UUID getId() { return id; }
    public String getMemberNumber() { return memberNumber; }
    public void setMemberNumber(String memberNumber) { this.memberNumber = memberNumber; }
    public Long getTotalMiles() { return totalMiles; }
    public void setTotalMiles(Long totalMiles) { this.totalMiles = totalMiles; }
    public Long getQualifyingMiles() { return qualifyingMiles; }
    public void setQualifyingMiles(Long qualifyingMiles) { this.qualifyingMiles = qualifyingMiles; }
    public Long getEliteQualifyingMiles() { return eliteQualifyingMiles; }
    public void setEliteQualifyingMiles(Long eliteQualifyingMiles) { this.eliteQualifyingMiles = eliteQualifyingMiles; }
    public Integer getEliteQualifyingSegments() { return eliteQualifyingSegments; }
    public void setEliteQualifyingSegments(Integer eliteQualifyingSegments) { this.eliteQualifyingSegments = eliteQualifyingSegments; }
    public Date getMilesExpiryDate() { return milesExpiryDate; }
    public void setMilesExpiryDate(Date milesExpiryDate) { this.milesExpiryDate = milesExpiryDate; }
    public Date getLastActivityDate() { return lastActivityDate; }
    public void setLastActivityDate(Date lastActivityDate) { this.lastActivityDate = lastActivityDate; }
    public Date getCreatedDate() { return createdDate; }
    public AccountStatus getStatus() { return status; }
    public void setStatus(AccountStatus status) { this.status = status; }
    public List<MileageTransaction> getTransactions() { return transactions; }
    public void setTransactions(List<MileageTransaction> transactions) { this.transactions = transactions; }

    public boolean isFrozen() { return frozen; }
    public String getFreezeReason() { return freezeReason; }

    public void freeze(String reason) {
        if (this.status != AccountStatus.ACTIVE) {
            throw new IllegalStateException("Can only freeze an ACTIVE account; current: " + this.status);
        }
        this.frozen = true;
        this.freezeReason = reason;
        this.status = AccountStatus.FROZEN;
    }

    /**
     * ENG-2.1 — Closed state is terminal; no further transitions allowed.
     */
    public void close() {
        if (this.status == AccountStatus.CLOSED) {
            throw new IllegalStateException("Account is already closed");
        }
        this.status = AccountStatus.CLOSED;
        this.frozen = false;
    }

    /**
     * Domain method that AccrualService uses to credit miles (ENG-2.1).
     * Preserves the invariant that all three mile counters move together on accrual.
     */
    public void addMiles(long amount) {
        if (this.status != AccountStatus.ACTIVE) {
            throw new IllegalStateException("Cannot add miles to account with status: " + this.status);
        }
        if (amount < 0) throw new IllegalArgumentException("Use deductMiles for negative amounts");
        this.totalMiles = (this.totalMiles == null ? 0L : this.totalMiles) + amount;
        this.eliteQualifyingMiles = (this.eliteQualifyingMiles == null ? 0L : this.eliteQualifyingMiles) + amount;
        this.qualifyingMiles = (this.qualifyingMiles == null ? 0L : this.qualifyingMiles) + amount;
    }

    /**
     * Domain method for mile deductions (e.g., redemptions, adjustments).
     */
    public void deductMiles(long amount) {
        if (this.status != AccountStatus.ACTIVE) {
            throw new IllegalStateException("Cannot deduct miles from account with status: " + this.status);
        }
        if (amount < 0) throw new IllegalArgumentException("Amount must be positive");
        if (amount > this.totalMiles) throw new IllegalStateException("Insufficient miles: " + totalMiles + " < " + amount);
        this.totalMiles = this.totalMiles - amount;
    }
}
