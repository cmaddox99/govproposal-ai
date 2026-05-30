package com.aa.loyalty.tier.domain;

import java.util.HashMap;
import java.util.Map;

/**
 * Value object holding the benefit configuration for a single AAdvantage tier.
 * Immutable. Created at system start and registered in TierBenefitCalculator.
 * Adding a new tier requires only instantiating a TierBenefits and registering it —
 * no modification of TierBenefitCalculator (OCP compliant).
 */
public final class TierBenefits {

    private final int upgradeCertificates;
    private final boolean loungeAccess;
    private final boolean earlyBoarding;
    private final boolean companionFare;
    private final double bonusMilesRate;
    private final boolean priorityCheckIn;
    private final int extraBaggage;
    private final String summary;

    @SuppressWarnings("java:S107") // Builder is the public API; this private constructor is intentionally full-arg
    private TierBenefits(int upgradeCertificates, boolean loungeAccess, boolean earlyBoarding,
                         boolean companionFare, double bonusMilesRate, boolean priorityCheckIn,
                         int extraBaggage, String summary) {
        this.upgradeCertificates = upgradeCertificates;
        this.loungeAccess = loungeAccess;
        this.earlyBoarding = earlyBoarding;
        this.companionFare = companionFare;
        this.bonusMilesRate = bonusMilesRate;
        this.priorityCheckIn = priorityCheckIn;
        this.extraBaggage = extraBaggage;
        this.summary = summary;
    }

    public static Builder builder() { return new Builder(); }

    public static class Builder {
        private int upgradeCertificates;
        private boolean loungeAccess;
        private boolean earlyBoarding;
        private boolean companionFare;
        private double bonusMilesRate;
        private boolean priorityCheckIn;
        private int extraBaggage;
        private String summary;

        public Builder upgradeCertificates(int v) { this.upgradeCertificates = v; return this; }
        public Builder loungeAccess(boolean v) { this.loungeAccess = v; return this; }
        public Builder earlyBoarding(boolean v) { this.earlyBoarding = v; return this; }
        public Builder companionFare(boolean v) { this.companionFare = v; return this; }
        public Builder bonusMilesRate(double v) { this.bonusMilesRate = v; return this; }
        public Builder priorityCheckIn(boolean v) { this.priorityCheckIn = v; return this; }
        public Builder extraBaggage(int v) { this.extraBaggage = v; return this; }
        public Builder summary(String v) { this.summary = v; return this; }
        public TierBenefits build() {
            return new TierBenefits(upgradeCertificates, loungeAccess, earlyBoarding,
                companionFare, bonusMilesRate, priorityCheckIn, extraBaggage, summary);
        }
    }

    public Map<String, Object> toMap() {
        Map<String, Object> m = new HashMap<>();
        m.put("upgradeCertificates", upgradeCertificates);
        m.put("loungeAccess", loungeAccess);
        m.put("earlyBoarding", earlyBoarding);
        m.put("companionFare", companionFare);
        m.put("bonusMilesRate", bonusMilesRate);
        m.put("priorityCheckIn", priorityCheckIn);
        m.put("extraBaggage", extraBaggage);
        return m;
    }

    public String getSummary() { return summary; }
    public int getUpgradeCertificates() { return upgradeCertificates; }
    public boolean isLoungeAccess() { return loungeAccess; }
    public boolean isEarlyBoarding() { return earlyBoarding; }
    public boolean isCompanionFare() { return companionFare; }
    public double getBonusMilesRate() { return bonusMilesRate; }
    public boolean isPriorityCheckIn() { return priorityCheckIn; }
    public int getExtraBaggage() { return extraBaggage; }
}
