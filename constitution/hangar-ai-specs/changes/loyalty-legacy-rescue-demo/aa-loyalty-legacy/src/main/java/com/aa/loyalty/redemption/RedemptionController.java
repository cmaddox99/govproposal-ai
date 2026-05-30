package com.aa.loyalty.redemption;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.Date;
import java.util.List;

@RestController
@RequestMapping("/api/v1/redemptions")
public class RedemptionController {

    @Autowired
    private RedemptionService redemptionService;

    @PostMapping("/award-flight")
    public ResponseEntity<Redemption> bookAwardFlight(
            @RequestParam String memberNumber,
            @RequestParam String origin,
            @RequestParam String destination,
            @RequestParam @DateTimeFormat(pattern = "yyyy-MM-dd") Date travelDate,
            @RequestParam(defaultValue = "COACH") String cabinClass) {
        return ResponseEntity.ok(
            redemptionService.bookAwardFlight(memberNumber, origin, destination, travelDate, cabinClass));
    }

    @GetMapping("/{memberNumber}/history")
    public ResponseEntity<List<Redemption>> getHistory(@PathVariable String memberNumber) {
        return ResponseEntity.ok(redemptionService.getRedemptionHistory(memberNumber));
    }

    @DeleteMapping("/{reservationCode}")
    public ResponseEntity<Void> cancel(@PathVariable String reservationCode) {
        redemptionService.cancelRedemption(reservationCode);
        return ResponseEntity.noContent().build();
    }
}
