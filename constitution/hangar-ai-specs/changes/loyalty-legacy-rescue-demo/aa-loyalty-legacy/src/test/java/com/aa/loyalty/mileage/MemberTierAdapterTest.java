package com.aa.loyalty.mileage;

import com.aa.loyalty.member.domain.Member;
import com.aa.loyalty.member.domain.MemberRepository;
import com.aa.loyalty.tier.domain.TierStatus;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;
import com.aa.loyalty.mileage.infrastructure.MemberTierAdapter;

@ExtendWith(MockitoExtension.class)
class MemberTierAdapterTest {

    @Mock MemberRepository memberRepository;
    @InjectMocks MemberTierAdapter adapter;

    @Test
    void getTierStatus_memberExists_returnsTierName() {
        Member member = new Member();
        member.setTierStatus(TierStatus.GOLD);
        when(memberRepository.findByMemberNumber("AA001")).thenReturn(member);
        assertEquals("GOLD", adapter.getTierStatus("AA001"));
    }

    @Test
    void getTierStatus_memberNotFound_returnsGeneral() {
        when(memberRepository.findByMemberNumber("NONE")).thenReturn(null);
        assertEquals("GENERAL", adapter.getTierStatus("NONE"));
    }
}
