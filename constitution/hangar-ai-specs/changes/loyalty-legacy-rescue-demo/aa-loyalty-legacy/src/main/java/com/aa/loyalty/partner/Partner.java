package com.aa.loyalty.partner;

import javax.persistence.*;

@Entity
@Table(name = "PARTNER")
public class Partner {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "partner_seq")
    @SequenceGenerator(name = "partner_seq", sequenceName = "PARTNER_SEQ", allocationSize = 1)
    private Long id;

    @Column(name = "PARTNER_CODE", nullable = false, unique = true, length = 20)
    private String partnerCode;

    @Column(name = "PARTNER_NAME", length = 100)
    private String partnerName;

    @Column(name = "PARTNER_TYPE", length = 30)
    private String partnerType;  // AIRLINE, HOTEL, CAR_RENTAL, RETAIL, FINANCIAL

    @Column(name = "BASE_EARN_RATE")
    private Double baseEarnRate = 1.0;

    @Column(name = "ACTIVE")
    private Boolean active = true;

    @Column(name = "API_ENDPOINT", length = 200)
    private String apiEndpoint;

    @Column(name = "API_KEY", length = 100)
    private String apiKey;  // SECURITY VIOLATION: API key stored in DB column, logged by JPA

    public Partner() {}

    public Long getId() { return id; }
    public String getPartnerCode() { return partnerCode; }
    public void setPartnerCode(String partnerCode) { this.partnerCode = partnerCode; }
    public String getPartnerName() { return partnerName; }
    public void setPartnerName(String partnerName) { this.partnerName = partnerName; }
    public String getPartnerType() { return partnerType; }
    public void setPartnerType(String partnerType) { this.partnerType = partnerType; }
    public Double getBaseEarnRate() { return baseEarnRate; }
    public void setBaseEarnRate(Double baseEarnRate) { this.baseEarnRate = baseEarnRate; }
    public Boolean getActive() { return active; }
    public void setActive(Boolean active) { this.active = active; }
    public String getApiEndpoint() { return apiEndpoint; }
    public void setApiEndpoint(String apiEndpoint) { this.apiEndpoint = apiEndpoint; }
    public String getApiKey() { return apiKey; }
    public void setApiKey(String apiKey) { this.apiKey = apiKey; }
}
