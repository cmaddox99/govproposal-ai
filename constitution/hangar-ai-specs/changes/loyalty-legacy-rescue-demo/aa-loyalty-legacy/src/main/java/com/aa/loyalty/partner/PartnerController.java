package com.aa.loyalty.partner;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/v1/partners")
public class PartnerController {

    @Autowired
    private PartnerService partnerService;

    @GetMapping
    public ResponseEntity<List<Partner>> getPartners() {
        return ResponseEntity.ok(partnerService.getActivePartners());
    }

    // VIOLATION: exposes full Partner including apiKey field to any caller
    @GetMapping("/{partnerCode}")
    public ResponseEntity<Partner> getPartner(@PathVariable String partnerCode) {
        Partner p = partnerService.getPartnerDetails(partnerCode);
        if (p == null) return ResponseEntity.notFound().build();
        return ResponseEntity.ok(p);
    }

    @PostMapping("/accrue")
    public ResponseEntity<?> processAccrual(
            @RequestParam String memberNumber,
            @RequestParam String partnerCode,
            @RequestParam double spendAmount,
            @RequestParam String transactionRef) {
        long miles = partnerService.processPartnerAccrual(memberNumber, partnerCode, spendAmount, transactionRef);
        return ResponseEntity.ok("Partner miles accrued: " + miles);
    }
}
