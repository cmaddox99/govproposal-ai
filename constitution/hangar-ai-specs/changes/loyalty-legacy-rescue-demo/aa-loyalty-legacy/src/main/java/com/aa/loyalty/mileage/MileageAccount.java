package com.aa.loyalty.mileage;

import javax.persistence.*;
import java.util.Date;
import java.util.List;
import java.util.ArrayList;

@Entity
@Table(name = "MILEAGE_ACCOUNT")
public class MileageAccount {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "mileage_seq")
    @SequenceGenerator(name = "mileage_seq", sequenceName = "MILEAGE_SEQ", allocationSize = 1)
    private Long id;

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

    @Column(name = "STATUS", length = 20)
    private String status = "ACTIVE";  // VIOLATION: magic string, no enum

    @OneToMany(mappedBy = "account", cascade = CascadeType.ALL, fetch = FetchType.EAGER) // VIOLATION: EAGER fetch on collection
    private List<MileageTransaction> transactions = new ArrayList<>();

    // VIOLATION: no-arg constructor leaks - status not validated on set
    public MileageAccount() {}

    public MileageAccount(String memberNumber) {
        this.memberNumber = memberNumber;
        this.createdDate = new Date();
        this.milesExpiryDate = new Date(System.currentTimeMillis() + (365L * 24 * 60 * 60 * 1000 * 2));
    }

    // VIOLATION: mutable Date returned directly — exposes internal state
    public Long getId() { return id; }
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
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
    public List<MileageTransaction> getTransactions() { return transactions; }
    public void setTransactions(List<MileageTransaction> transactions) { this.transactions = transactions; }
}
