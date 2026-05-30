package com.aa.loyalty.tier;

// CHARACTERIZATION TEST — ENG-4.10
import com.aa.loyalty.member.Member;
import com.aa.loyalty.member.MemberRepository;
import com.aa.loyalty.mileage.MileageAccount;
import com.aa.loyalty.mileage.MileageRepository;
import com.aa.loyalty.notification.NotificationService;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import java.util.*;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class TierServiceTest {

    @Mock MemberRepository memberRepository;
    @Mock MileageRepository mileageRepository;
    @Mock TierCalculator tierCalculator;
    @Mock NotificationService notificationService;

    @InjectMocks TierService service;

    @Test
    void recalculateTier_memberNotFound_doesNothing() {
        when(memberRepository.findByMemberNumber("NONE")).thenReturn(null);
        when(mileageRepository.findByMemberNumber("NONE")).thenReturn(null);
        assertDoesNotThrow(() -> service.recalculateTier("NONE"));
    }

    @Test
    void recalculateTier_tierUnchanged_doesNotSaveOrNotify() {
        Member member = new Member();
        member.setMemberNumber("AA001");
        member.setTierStatus("GOLD");
        MileageAccount account = new MileageAccount("AA001");
        account.setEliteQualifyingMiles(25000L);
        account.setEliteQualifyingSegments(30);
        when(memberRepository.findByMemberNumber("AA001")).thenReturn(member);
        when(mileageRepository.findByMemberNumber("AA001")).thenReturn(account);
        when(tierCalculator.calculateNewTier(25000L, 30, 0L)).thenReturn("GOLD");
        service.recalculateTier("AA001");
        verify(memberRepository, never()).save(any());
        verify(notificationService, never()).sendTierChangeEmail(any(), any(), any());
    }

    @Test
    void recalculateTier_tierChanged_savesAndNotifies() {
        Member member = new Member();
        member.setMemberNumber("AA002");
        member.setTierStatus("GENERAL");
        MileageAccount account = new MileageAccount("AA002");
        account.setEliteQualifyingMiles(25000L);
        account.setEliteQualifyingSegments(30);
        when(memberRepository.findByMemberNumber("AA002")).thenReturn(member);
        when(mileageRepository.findByMemberNumber("AA002")).thenReturn(account);
        when(tierCalculator.calculateNewTier(25000L, 30, 0L)).thenReturn("GOLD");
        when(memberRepository.save(any())).thenAnswer(i -> i.getArgument(0));
        service.recalculateTier("AA002");
        assertEquals("GOLD", member.getTierStatus());
        verify(notificationService).sendTierChangeEmail("AA002", "GENERAL", "GOLD");
    }

    @Test
    void getTierStatus_memberNotFound_returnsGeneral() {
        when(memberRepository.findByMemberNumber("NONE")).thenReturn(null);
        assertEquals("GENERAL", service.getTierStatus("NONE"));
    }

    @Test
    void getTierStatus_memberFound_returnsTier() {
        Member member = new Member();
        member.setTierStatus("PLATINUM");
        when(memberRepository.findByMemberNumber("AA003")).thenReturn(member);
        assertEquals("PLATINUM", service.getTierStatus("AA003"));
    }

    @Test
    void yearEndTierReset_execPlatRetainsToPlatinumPro() {
        Member member = new Member();
        member.setMemberNumber("AA004");
        member.setTierStatus("EXECUTIVE_PLATINUM");
        when(memberRepository.findAll()).thenReturn(List.of(member));
        when(memberRepository.save(any())).thenAnswer(i -> i.getArgument(0));
        service.yearEndTierReset();
        assertEquals("PLATINUM_PRO", member.getTierStatus());
    }

    @Test
    void yearEndTierReset_platinumProDropsToPlatinum() {
        Member member = new Member();
        member.setMemberNumber("AA009");
        member.setTierStatus("PLATINUM_PRO");
        when(memberRepository.findAll()).thenReturn(List.of(member));
        when(memberRepository.save(any())).thenAnswer(i -> i.getArgument(0));
        service.yearEndTierReset();
        assertEquals("PLATINUM", member.getTierStatus());
    }

    @Test
    void yearEndTierReset_platinumDropsToGold() {
        Member member = new Member();
        member.setMemberNumber("AA010");
        member.setTierStatus("PLATINUM");
        when(memberRepository.findAll()).thenReturn(List.of(member));
        when(memberRepository.save(any())).thenAnswer(i -> i.getArgument(0));
        service.yearEndTierReset();
        assertEquals("GOLD", member.getTierStatus());
    }

    @Test
    void yearEndTierReset_goldDropsToGeneral() {
        Member member = new Member();
        member.setMemberNumber("AA005");
        member.setTierStatus("GOLD");
        when(memberRepository.findAll()).thenReturn(List.of(member));
        when(memberRepository.save(any())).thenAnswer(i -> i.getArgument(0));
        service.yearEndTierReset();
        assertEquals("GENERAL", member.getTierStatus());
    }

    @Test
    void yearEndTierReset_generalStaysGeneral() {
        Member member = new Member();
        member.setMemberNumber("AA006");
        member.setTierStatus("GENERAL");
        when(memberRepository.findAll()).thenReturn(List.of(member));
        when(memberRepository.save(any())).thenAnswer(i -> i.getArgument(0));
        service.yearEndTierReset();
        assertEquals("GENERAL", member.getTierStatus());
    }

    @Test
    void recalculateTier_tierChanged_notificationFailure_doesNotRethrow() {
        Member member = new Member();
        member.setMemberNumber("AA007");
        member.setTierStatus("GENERAL");
        MileageAccount account = new MileageAccount("AA007");
        account.setEliteQualifyingMiles(25000L);
        account.setEliteQualifyingSegments(30);
        when(memberRepository.findByMemberNumber("AA007")).thenReturn(member);
        when(mileageRepository.findByMemberNumber("AA007")).thenReturn(account);
        when(tierCalculator.calculateNewTier(25000L, 30, 0L)).thenReturn("GOLD");
        when(memberRepository.save(any())).thenAnswer(i -> i.getArgument(0));
        doThrow(new RuntimeException("SMTP")).when(notificationService).sendTierChangeEmail(any(), any(), any());
        assertDoesNotThrow(() -> service.recalculateTier("AA007"));
    }

    @Test
    void recalculateTier_memberFoundButAccountNull_doesNothing() {
        Member member = new Member();
        member.setMemberNumber("AA008");
        when(memberRepository.findByMemberNumber("AA008")).thenReturn(member);
        when(mileageRepository.findByMemberNumber("AA008")).thenReturn(null);
        assertDoesNotThrow(() -> service.recalculateTier("AA008"));
        verify(memberRepository, never()).save(any());
    }

    @Test
    void recalculateTier_memberNullAccountNotNull_doesNothing() {
        MileageAccount account = new MileageAccount("AA099");
        when(memberRepository.findByMemberNumber("AA099")).thenReturn(null);
        when(mileageRepository.findByMemberNumber("AA099")).thenReturn(account);
        assertDoesNotThrow(() -> service.recalculateTier("AA099"));
        verify(memberRepository, never()).save(any());
    }
}
