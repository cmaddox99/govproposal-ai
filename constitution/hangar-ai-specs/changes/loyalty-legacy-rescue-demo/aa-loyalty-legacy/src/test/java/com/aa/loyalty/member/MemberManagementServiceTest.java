package com.aa.loyalty.member;

import com.aa.loyalty.tier.domain.TierStatus;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.context.ApplicationEventPublisher;
import java.util.Date;
import java.util.List;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;
import com.aa.loyalty.member.application.MemberService;
import com.aa.loyalty.member.domain.Member;
import com.aa.loyalty.member.domain.MemberRepository;
import com.aa.loyalty.member.domain.MemberSelfServicePort;

/**
 * CHARACTERIZATION TEST (ENG-4.10) — ISP violation documented here.
 *
 * ORIGINAL VIOLATION: MemberManagementService is a fat interface with 11 methods
 * across 4 bounded contexts. MemberService implements all 11, throwing
 * UnsupportedOperationException for admin/compliance/fraud operations.
 *
 * POST-FIX (Phase 5 ISP): MemberManagementService is split into focused ports:
 *   - MemberSelfServicePort (self-service ops — what MemberService implements)
 *   - MemberAdminPort (admin ops — AdminMemberService)
 *   - MemberCompliancePort (compliance ops — ComplianceMemberService)
 *   - MemberFraudPort (fraud ops — FraudManagementService)
 *
 * These tests verify the ISP-compliant state AFTER the fix.
 */
@ExtendWith(MockitoExtension.class)
class MemberManagementServiceTest {

    @Mock
    MemberRepository memberRepository;

    @Mock
    ApplicationEventPublisher eventPublisher;

    @InjectMocks
    MemberService service;

    @Test
    void memberService_implementsMemberSelfServicePort() {
        assertTrue(service instanceof MemberSelfServicePort,
            "MemberService must implement MemberSelfServicePort after ISP fix");
    }

    @Test
    void memberSelfServicePort_enroll_isImplemented() {
        when(memberRepository.findByEmail("isp@aa.com")).thenReturn(null);
        when(memberRepository.save(any())).thenAnswer(i -> i.getArgument(0));
        MemberSelfServicePort port = service;
        Member result = port.enroll("John", "Doe", "isp@aa.com", "555-0000", new Date());
        assertNotNull(result);
    }

    @Test
    void memberSelfServicePort_updateProfile_isImplemented() {
        Member member = new Member();
        member.setMemberNumber("AA-ISP-01");
        when(memberRepository.findByMemberNumber("AA-ISP-01")).thenReturn(member);
        when(memberRepository.save(any())).thenAnswer(i -> i.getArgument(0));
        MemberSelfServicePort port = service;
        Member result = port.updateProfile("AA-ISP-01", "new@aa.com", null, null);
        assertEquals("new@aa.com", result.getEmail());
    }

    @Test
    void memberSelfServicePort_getMember_isImplemented() {
        Member member = new Member();
        member.setMemberNumber("AA-ISP-02");
        when(memberRepository.findByMemberNumber("AA-ISP-02")).thenReturn(member);
        MemberSelfServicePort port = service;
        assertSame(member, port.getMember("AA-ISP-02"));
    }

    @Test
    void memberSelfServicePort_searchByLastName_isImplemented() {
        List<Member> members = List.of(new Member());
        when(memberRepository.searchByLastName("Doe")).thenReturn(members);
        MemberSelfServicePort port = service;
        assertEquals(members, port.searchByLastName("Doe"));
    }

    @Test
    void memberSelfServicePort_deactivateMember_isImplemented() {
        Member member = new Member();
        member.setMemberNumber("AA-ISP-03");
        member.setActive(true);
        when(memberRepository.findByMemberNumber("AA-ISP-03")).thenReturn(member);
        when(memberRepository.save(any())).thenAnswer(i -> i.getArgument(0));
        MemberSelfServicePort port = service;
        port.deactivateMember("AA-ISP-03");
        assertFalse(member.getActive());
    }

    @Test
    void memberSelfServicePort_updateTierStatus_isImplemented() {
        Member member = new Member();
        member.setMemberNumber("AA-ISP-04");
        member.setTierStatus(TierStatus.GENERAL);
        when(memberRepository.findByMemberNumber("AA-ISP-04")).thenReturn(member);
        when(memberRepository.save(any())).thenAnswer(i -> i.getArgument(0));
        MemberSelfServicePort port = service;
        port.updateTierStatus("AA-ISP-04", "GOLD");
        assertEquals(TierStatus.GOLD, member.getTierStatus());
    }

    @Test
    void memberSelfServicePort_getAllEliteMembers_isImplemented() {
        List<Member> elites = List.of(new Member());
        when(memberRepository.findAllEliteMembers()).thenReturn(elites);
        MemberSelfServicePort port = service;
        assertEquals(elites, port.getAllEliteMembers());
    }
}
