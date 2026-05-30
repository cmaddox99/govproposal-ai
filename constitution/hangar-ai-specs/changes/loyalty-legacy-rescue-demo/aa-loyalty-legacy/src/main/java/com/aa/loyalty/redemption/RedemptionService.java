package com.aa.loyalty.redemption;

import com.aa.loyalty.mileage.MileageService;
import com.aa.loyalty.notification.NotificationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Date;
import java.util.List;
import java.util.UUID;
import java.util.logging.Logger;

/**
 * VIOLATIONS:
 * - Resource leak: FileWriter not closed if exception occurs mid-method
 * - Circular dependency risk: calls MileageService which also has redemption logic
 * - No idempotency protection on bookAwardFlight
 */
@Service
public class RedemptionService {

    private static final Logger LOG = Logger.getLogger(RedemptionService.class.getName());

    // VIOLATION: hardcoded miles cost table — should be in DB/config
    private static final long COACH_DFW_LAX = 12500;
    private static final long COACH_DFW_LHR = 30000;
    private static final long BUSINESS_DFW_LHR = 57500;
    private static final long FIRST_DFW_LHR = 70000;

    @Autowired
    private RedemptionRepository redemptionRepository;

    @Autowired
    private MileageService mileageService;  // VIOLATION: cross-context coupling

    @Autowired
    private NotificationService notificationService;

    @Transactional
    public Redemption bookAwardFlight(String memberNumber, String origin, String destination,
                                      Date travelDate, String cabinClass) {
        // VIOLATION: no idempotency check — double submission creates duplicate redemptions
        long milesCost = calculateAwardCost(origin, destination, cabinClass);

        boolean success = mileageService.redeemMiles(memberNumber, milesCost, "AWARD_FLIGHT",
            "Award flight " + origin + "-" + destination);
        if (!success) {
            throw new RuntimeException("Insufficient miles for award flight");
        }

        Redemption redemption = new Redemption();
        redemption.setMemberNumber(memberNumber);
        redemption.setRedemptionType("AWARD_FLIGHT");
        redemption.setMilesCost(milesCost);
        redemption.setStatus("CONFIRMED");
        redemption.setReservationCode(generateReservationCode());
        redemption.setRedemptionDate(new Date());
        redemption.setTravelDate(travelDate);
        redemption.setOrigin(origin);
        redemption.setDestination(destination);
        redemption.setCabinClass(cabinClass);

        Redemption saved = redemptionRepository.save(redemption);

        // VIOLATION: resource leak — FileWriter not in try-with-resources
        FileWriter fw = null;
        try {
            fw = new FileWriter("/var/log/loyalty/redemptions.log", true);
            fw.write(new Date() + " | " + memberNumber + " | AWARD_FLIGHT | " + milesCost + " miles\n");
            fw.flush();
        } catch (IOException e) {
            LOG.warning("Could not write redemption audit log: " + e.getMessage()); // swallowed
        } finally {
            if (fw != null) {
                try { fw.close(); } catch (IOException ignored) {}
            }
        }

        try {
            notificationService.sendRedemptionConfirmationEmail(memberNumber, milesCost, "AWARD_FLIGHT");
        } catch (Exception e) {
            LOG.warning("Notification failed: " + e.getMessage());
        }

        return saved;
    }

    // VIOLATION: hardcoded route-to-miles mapping, duplicates values from MileageCalculator
    private long calculateAwardCost(String origin, String destination, String cabinClass) {
        String route = origin + "-" + destination;
        if (cabinClass == null) cabinClass = "COACH";

        if (route.equals("DFW-LAX") || route.equals("LAX-DFW")) {
            return cabinClass.equals("BUSINESS") ? 25000 : COACH_DFW_LAX;
        } else if (route.equals("DFW-LHR") || route.equals("LHR-DFW")) {
            if (cabinClass.equals("FIRST")) return FIRST_DFW_LHR;
            if (cabinClass.equals("BUSINESS")) return BUSINESS_DFW_LHR;
            return COACH_DFW_LHR;
        } else {
            return 25000; // VIOLATION: default with magic number, no logging
        }
    }

    private String generateReservationCode() {
        return UUID.randomUUID().toString().substring(0, 6).toUpperCase();
    }

    public List<Redemption> getRedemptionHistory(String memberNumber) {
        return redemptionRepository.findByMemberNumber(memberNumber);
    }

    @Transactional
    public boolean cancelRedemption(String reservationCode) {
        List<Redemption> all = redemptionRepository.findAll();
        for (Redemption r : all) {
            if (reservationCode.equals(r.getReservationCode())) {
                if ("CONFIRMED".equals(r.getStatus())) {
                    r.setStatus("CANCELLED");
                    redemptionRepository.save(r);
                    // Phase 5 bug fix: refund miles on cancellation
                    mileageService.redeemMiles(r.getMemberNumber(), -r.getMilesCost(),
                        "CANCELLATION_REFUND", "Refund for cancelled reservation " + reservationCode);
                    return true;
                }
            }
        }
        return false;
    }
}
