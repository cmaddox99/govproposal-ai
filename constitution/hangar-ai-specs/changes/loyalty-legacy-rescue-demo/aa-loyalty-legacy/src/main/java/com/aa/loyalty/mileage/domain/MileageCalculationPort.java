package com.aa.loyalty.mileage.domain;

/**
 * DIP abstraction for mileage calculation.
 * High-level modules (PartnerService) depend on this interface.
 * Low-level modules (MileageCalculator) implement it.
 * Both depend on the abstraction — neither on the concrete implementation.
 */
public interface MileageCalculationPort {
    long calculatePartnerMiles(String partnerCode, double spendAmount, String memberTier);
    long calculateAccruedMiles(String origin, String destination, String bookingClass,
                               String memberTier, String partnerCode, boolean isPromo,
                               int flightSegments);
}
