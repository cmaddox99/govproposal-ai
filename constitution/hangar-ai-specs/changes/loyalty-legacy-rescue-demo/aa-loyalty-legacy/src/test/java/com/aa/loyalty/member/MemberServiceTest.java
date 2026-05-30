package com.aa.loyalty.member;

// CHARACTERIZATION TEST — ENG-4.10
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import java.util.*;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class MemberServiceTest {

    @Mock MemberRepository memberRepository;
    @InjectMocks MemberService service;

    @Test
    void enroll_newEmail_savesAndReturnsMember() {
        when(memberRepository.findByEmail("test@aa.com")).thenReturn(null);
        Member saved = new Member();
        saved.setMemberNumber("AA9999");
        when(memberRepository.save(any())).thenReturn(saved);
        Member result = service.enroll("John", "Doe", "test@aa.com", "555-1234", new Date());
        assertEquals("AA9999", result.getMemberNumber());
    }

    @Test
    void enroll_verifiesAllMemberFieldsSet() {
        when(memberRepository.findByEmail("fields@aa.com")).thenReturn(null);
        ArgumentCaptor<Member> captor = ArgumentCaptor.forClass(Member.class);
        when(memberRepository.save(captor.capture())).thenAnswer(i -> i.getArgument(0));
        Date dob = new Date(90000000L);
        service.enroll("Jane", "Smith", "fields@aa.com", "555-9999", dob);
        Member saved = captor.getValue();
        assertEquals("Jane", saved.getFirstName());
        assertEquals("Smith", saved.getLastName());
        assertEquals("fields@aa.com", saved.getEmail());
        assertEquals("555-9999", saved.getPhone());
        assertEquals(dob, saved.getDateOfBirth());
        assertNotNull(saved.getEnrollmentDate());
        assertNotNull(saved.getLastUpdated());
        assertNotNull(saved.getMemberNumber());
        assertTrue(saved.getMemberNumber().startsWith("AA"));
    }

    @Test
    void enroll_duplicateEmail_returnsSilently() {
        Member existing = new Member();
        existing.setMemberNumber("AA0001");
        when(memberRepository.findByEmail("dup@aa.com")).thenReturn(existing);
        Member result = service.enroll("Jane", "Doe", "dup@aa.com", null, null);
        assertSame(existing, result);
        verify(memberRepository, never()).save(any());
    }

    @Test
    void updateProfile_memberNotFound_throwsRuntimeException() {
        when(memberRepository.findByMemberNumber("GONE")).thenReturn(null);
        RuntimeException ex = assertThrows(RuntimeException.class,
            () -> service.updateProfile("GONE", "new@aa.com", null, null, null, null, null, null));
        assertEquals("Member not found", ex.getMessage());
    }

    @Test
    void updateProfile_nullFieldsDoNotClearExistingValues() {
        Member member = new Member();
        member.setMemberNumber("AA099");
        member.setEmail("existing@aa.com");
        member.setPhone("555-1234");
        member.setAddressLine1("100 Oak St");
        member.setCity("Phoenix");
        member.setState("AZ");
        member.setPostalCode("85001");
        member.setCountry("US");
        when(memberRepository.findByMemberNumber("AA099")).thenReturn(member);
        when(memberRepository.save(any())).thenAnswer(i -> i.getArgument(0));
        service.updateProfile("AA099", null, null, null, null, null, null, null);
        assertEquals("existing@aa.com", member.getEmail());
        assertEquals("555-1234", member.getPhone());
        assertEquals("100 Oak St", member.getAddressLine1());
        assertEquals("Phoenix", member.getCity());
        assertEquals("AZ", member.getState());
        assertEquals("85001", member.getPostalCode());
        assertEquals("US", member.getCountry());
    }

    @Test
    void updateProfile_updatesOnlyNonNullFields() {
        Member member = new Member();
        member.setMemberNumber("AA002");
        member.setEmail("old@aa.com");
        when(memberRepository.findByMemberNumber("AA002")).thenReturn(member);
        when(memberRepository.save(any())).thenAnswer(i -> i.getArgument(0));
        service.updateProfile("AA002", "new@aa.com", null, null, null, null, null, null);
        assertEquals("new@aa.com", member.getEmail());
    }

    @Test
    void updateProfile_allFieldsNonNull_setsAllFields() {
        Member member = new Member();
        member.setMemberNumber("AA012");
        when(memberRepository.findByMemberNumber("AA012")).thenReturn(member);
        when(memberRepository.save(any())).thenAnswer(i -> i.getArgument(0));
        service.updateProfile("AA012", "full@aa.com", "555-8888", "123 Main St", "Dallas", "TX", "75201", "US");
        assertEquals("full@aa.com", member.getEmail());
        assertEquals("555-8888", member.getPhone());
        assertEquals("123 Main St", member.getAddressLine1());
        assertEquals("Dallas", member.getCity());
        assertEquals("TX", member.getState());
        assertEquals("75201", member.getPostalCode());
        assertEquals("US", member.getCountry());
        assertNotNull(member.getLastUpdated());
    }

    @Test
    void updateProfile_returnsUpdatedMember() {
        Member member = new Member();
        member.setMemberNumber("AA013");
        when(memberRepository.findByMemberNumber("AA013")).thenReturn(member);
        when(memberRepository.save(any())).thenAnswer(i -> i.getArgument(0));
        Member result = service.updateProfile("AA013", "ret@aa.com", null, null, null, null, null, null);
        assertNotNull(result);
        assertEquals("ret@aa.com", result.getEmail());
    }

    @Test
    void getMember_delegatesToRepository() {
        Member member = new Member();
        member.setMemberNumber("AA003");
        when(memberRepository.findByMemberNumber("AA003")).thenReturn(member);
        assertSame(member, service.getMember("AA003"));
    }

    @Test
    void getMember_notFound_returnsNull() {
        when(memberRepository.findByMemberNumber("NONE")).thenReturn(null);
        assertNull(service.getMember("NONE"));
    }

    @Test
    void deactivateMember_found_setsActiveFalse() {
        Member member = new Member();
        member.setMemberNumber("AA004");
        member.setActive(true);
        when(memberRepository.findByMemberNumber("AA004")).thenReturn(member);
        when(memberRepository.save(any())).thenAnswer(i -> i.getArgument(0));
        service.deactivateMember("AA004");
        assertFalse(member.getActive());
        assertNotNull(member.getLastUpdated());
    }

    @Test
    void deactivateMember_notFound_doesNotThrow() {
        when(memberRepository.findByMemberNumber("GONE")).thenReturn(null);
        assertDoesNotThrow(() -> service.deactivateMember("GONE"));
    }

    @Test
    void updateTierStatus_found_updatesTierAndLastUpdated() {
        Member member = new Member();
        member.setMemberNumber("AA005");
        member.setTierStatus("GENERAL");
        when(memberRepository.findByMemberNumber("AA005")).thenReturn(member);
        when(memberRepository.save(any())).thenAnswer(i -> i.getArgument(0));
        service.updateTierStatus("AA005", "GOLD");
        assertEquals("GOLD", member.getTierStatus());
        assertNotNull(member.getLastUpdated());
    }

    @Test
    void updateTierStatus_notFound_doesNothing() {
        when(memberRepository.findByMemberNumber("GONE")).thenReturn(null);
        assertDoesNotThrow(() -> service.updateTierStatus("GONE", "GOLD"));
        verify(memberRepository, never()).save(any());
    }

    @Test
    void searchByLastName_delegatesToRepository() {
        List<Member> members = List.of(new Member());
        when(memberRepository.searchByLastName("Smith")).thenReturn(members);
        assertEquals(members, service.searchByLastName("Smith"));
    }

    @Test
    void getAllEliteMembers_delegatesToRepository() {
        List<Member> elites = List.of(new Member());
        when(memberRepository.findAllEliteMembers()).thenReturn(elites);
        assertEquals(elites, service.getAllEliteMembers());
    }
}
