package com.aa.loyalty.member.infrastructure;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;
import com.aa.loyalty.member.application.MemberService;
import com.aa.loyalty.member.domain.Address;
import com.aa.loyalty.member.domain.EnrollmentRequest;
import com.aa.loyalty.member.domain.Member;
import com.aa.loyalty.member.domain.ProfileUpdateRequest;

/**
 * VIOLATIONS:
 * - No @Valid input validation
 * - Exposes full Member entity directly (over-exposure)
 * - No authentication check on sensitive endpoints
 */
@RestController
@RequestMapping("/api/v1/members")
public class MemberController {

    @Autowired
    private MemberService memberService;

    // VIOLATION: exposes full internal entity — PII over-exposure
    @GetMapping("/{memberNumber}")
    public ResponseEntity<Member> getMember(@PathVariable String memberNumber) {
        Member m = memberService.getMember(memberNumber);
        if (m == null) return ResponseEntity.notFound().build();
        return ResponseEntity.ok(m);  // VIOLATION: date of birth, full address returned to any caller
    }

    @PostMapping("/enroll")
    public ResponseEntity<Member> enroll(@RequestBody EnrollmentRequest request) {
        // VIOLATION: no @Valid, no sanitization — XSS risk on name fields
        Member m = memberService.enroll(
            request.getFirstName(), request.getLastName(),
            request.getEmail(), request.getPhone(),
            request.getDateOfBirth());
        return ResponseEntity.ok(m);
    }

    @PutMapping("/{memberNumber}/profile")
    public ResponseEntity<Member> updateProfile(
            @PathVariable String memberNumber,
            @RequestBody ProfileUpdateRequest request) {
        Address address = new Address(request.getAddressLine1(), null,
            request.getCity(), request.getState(), request.getPostalCode(), request.getCountry());
        Member m = memberService.updateProfile(memberNumber, request.getEmail(), request.getPhone(), address);
        return ResponseEntity.ok(m);
    }

    @GetMapping("/search")
    public ResponseEntity<List<Member>> search(@RequestParam String lastName) {
        // VIOLATION: no authentication, exposes PII of all matched members
        return ResponseEntity.ok(memberService.searchByLastName(lastName));
    }

    @DeleteMapping("/{memberNumber}")
    public ResponseEntity<Void> deactivate(@PathVariable String memberNumber) {
        // VIOLATION: no authorization check — any caller can deactivate any member
        memberService.deactivateMember(memberNumber);
        return ResponseEntity.noContent().build();
    }
}
