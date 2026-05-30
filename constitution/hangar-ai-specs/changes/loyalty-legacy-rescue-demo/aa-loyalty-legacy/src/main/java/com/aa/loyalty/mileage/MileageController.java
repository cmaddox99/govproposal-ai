package com.aa.loyalty.mileage;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;
import java.util.logging.Logger;

/**
 * VIOLATIONS:
 * - Business logic directly in controller
 * - No input validation (memberNumber format, date format)
 * - Exception mapping handled inline with ResponseEntity
 * - Catches Exception broadly
 */
@RestController
@RequestMapping("/api/v1/mileage")
public class MileageController {

    private static final Logger LOG = Logger.getLogger(MileageController.class.getName());

    @Autowired
    private MileageService mileageService;  // VIOLATION: direct field injection, not constructor

    @GetMapping("/{memberNumber}/balance")
    public ResponseEntity<?> getBalance(@PathVariable String memberNumber) {
        // VIOLATION: no validation that memberNumber matches expected format
        try {
            Long miles = mileageService.getTotalMiles(memberNumber);
            Map<String, Object> resp = new HashMap<>();
            resp.put("memberNumber", memberNumber);
            resp.put("totalMiles", miles);
            resp.put("timestamp", new Date().toString());
            return ResponseEntity.ok(resp);
        } catch (Exception e) {  // VIOLATION: catches broad Exception
            LOG.severe("Balance lookup failed: " + e.getMessage());
            return ResponseEntity.status(500).body("Internal error");
        }
    }

    @PostMapping("/{memberNumber}/accrue/flight")
    public ResponseEntity<?> accrueFlightMiles(
            @PathVariable String memberNumber,
            @RequestParam String flightNumber,
            @RequestParam String origin,
            @RequestParam String destination,
            @RequestParam String bookingClass,
            @RequestParam String flightDate,
            @RequestParam(required = false) String ticketNumber) {

        // VIOLATION: date parsing inline in controller
        Date parsedDate;
        try {
            parsedDate = new SimpleDateFormat("yyyy-MM-dd").parse(flightDate);
        } catch (ParseException e) {
            return ResponseEntity.badRequest().body("Invalid date format. Use yyyy-MM-dd");
        }

        // VIOLATION: business logic check in controller
        if (origin.equals(destination)) {
            return ResponseEntity.badRequest().body("Origin and destination cannot be the same");
        }

        long miles = mileageService.accrueFlightMiles(
            memberNumber, flightNumber, origin, destination, bookingClass, parsedDate, ticketNumber);

        Map<String, Object> resp = new HashMap<>();
        resp.put("milesAccrued", miles);
        resp.put("memberNumber", memberNumber);
        return ResponseEntity.ok(resp);
    }

    @PostMapping("/{memberNumber}/redeem")
    public ResponseEntity<?> redeemMiles(
            @PathVariable String memberNumber,
            @RequestParam long miles,
            @RequestParam String redemptionType,
            @RequestParam(required = false) String description) {

        // VIOLATION: no CSRF check, no idempotency key
        boolean success = mileageService.redeemMiles(memberNumber, miles, redemptionType, description);
        if (!success) {
            return ResponseEntity.badRequest().body("Redemption failed — check balance");
        }
        return ResponseEntity.ok("Redemption successful");
    }

    @PostMapping("/admin/adjust")
    public ResponseEntity<?> adminAdjust(
            @RequestParam String memberNumber,
            @RequestParam long adjustment,
            @RequestParam String reason,
            @RequestParam String agentId) {
        // VIOLATION: no auth check on admin endpoint
        mileageService.adminAdjustMiles(memberNumber, adjustment, reason, agentId);
        return ResponseEntity.ok("Adjustment applied");
    }
}
