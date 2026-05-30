package com.aa.loyalty.tier;

import com.aa.loyalty.member.domain.Member;
import com.aa.loyalty.member.domain.MemberRepository;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;
import com.aa.loyalty.tier.infrastructure.TierMemberAdapter;
import com.aa.loyalty.tier.domain.TierStatus;

@ExtendWith(MockitoExtension.class)
class TierMemberAdapterTest {

    @Mock MemberRepository memberRepository;
    @InjectMocks TierMemberAdapter adapter;

    @Test
    void getCurrentTier_memberExists_returnsTierStatus() {
        Member member = new Member();
        member.setTierStatus(TierStatus.PLATINUM);
        when(memberRepository.findByMemberNumber("AA001")).thenReturn(member);
        assertEquals(TierStatus.PLATINUM, adapter.getCurrentTier("AA001"));
    }

    @Test
    void getCurrentTier_memberNotFound_returnsGeneral() {
        when(memberRepository.findByMemberNumber("NONE")).thenReturn(null);
        assertEquals(TierStatus.GENERAL, adapter.getCurrentTier("NONE"));
    }

    @Test
    void saveTier_updatesMemberTierAndPersists() {
        Member member = new Member();
        member.setTierStatus(TierStatus.GENERAL);
        when(memberRepository.findByMemberNumber("AA002")).thenReturn(member);
        adapter.saveTier("AA002", TierStatus.GOLD);
        assertEquals(TierStatus.GOLD, member.getTierStatus());
        verify(memberRepository).save(member);
    }

    @Test
    void saveTier_memberNotFound_doesNothing() {
        when(memberRepository.findByMemberNumber("NONE")).thenReturn(null);
        assertDoesNotThrow(() -> adapter.saveTier("NONE", TierStatus.GOLD));
        verify(memberRepository, never()).save(any());
    }

    @Test
    void getAllMemberNumbers_returnsAllNumbers() {
        Member m1 = new Member(); m1.setMemberNumber("AA001");
        Member m2 = new Member(); m2.setMemberNumber("AA002");
        when(memberRepository.findAll()).thenReturn(List.of(m1, m2));
        List<String> result = adapter.getAllMemberNumbers();
        assertEquals(List.of("AA001", "AA002"), result);
    }
}
