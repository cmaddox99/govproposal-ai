package com.aa.loyalty.tier.infrastructure;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.HashMap;
import java.util.Map;
import com.aa.loyalty.tier.application.TierService;

@RestController
@RequestMapping("/api/v1/tier")
public class TierController {

    @Autowired
    private TierService tierService;

    @GetMapping("/{memberNumber}")
    public ResponseEntity<Map<String, Object>> getTierStatus(@PathVariable String memberNumber) {
        String tier = tierService.getTierStatus(memberNumber);
        Map<String, Object> resp = new HashMap<>();
        resp.put("memberNumber", memberNumber);
        resp.put("tierStatus", tier);
        return ResponseEntity.ok(resp);
    }

    @PostMapping("/{memberNumber}/recalculate")
    public ResponseEntity<Void> recalculate(@PathVariable String memberNumber) {
        // VIOLATION: no auth check — any caller can trigger recalculation
        tierService.recalculateTier(memberNumber);
        return ResponseEntity.ok().build();
    }
}
