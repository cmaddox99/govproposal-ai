package com.aa.loyalty.member;

// CHARACTERIZATION TEST — ENG-4.10
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;
import java.util.*;
import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@ExtendWith(MockitoExtension.class)
class MemberControllerTest {

    @Mock MemberService memberService;
    @InjectMocks MemberController controller;

    MockMvc mockMvc;
    ObjectMapper mapper = new ObjectMapper();

    @BeforeEach
    void setup() {
        mockMvc = MockMvcBuilders.standaloneSetup(controller).build();
    }

    @Test
    void getMember_found_returns200() throws Exception {
        Member m = new Member();
        m.setMemberNumber("AA001");
        when(memberService.getMember("AA001")).thenReturn(m);
        mockMvc.perform(get("/api/v1/members/AA001"))
            .andExpect(status().isOk());
    }

    @Test
    void getMember_notFound_returns404() throws Exception {
        when(memberService.getMember("NONE")).thenReturn(null);
        mockMvc.perform(get("/api/v1/members/NONE"))
            .andExpect(status().isNotFound());
    }

    @Test
    void enroll_validRequest_returns200() throws Exception {
        EnrollmentRequest req = new EnrollmentRequest();
        req.setFirstName("John");
        req.setLastName("Doe");
        req.setEmail("john@aa.com");
        Member saved = new Member();
        saved.setMemberNumber("AA999");
        when(memberService.enroll(any(), any(), any(), any(), any())).thenReturn(saved);
        mockMvc.perform(post("/api/v1/members/enroll")
            .contentType(MediaType.APPLICATION_JSON)
            .content(mapper.writeValueAsString(req)))
            .andExpect(status().isOk());
    }

    @Test
    void updateProfile_returns200() throws Exception {
        ProfileUpdateRequest req = new ProfileUpdateRequest();
        req.setEmail("new@aa.com");
        Member updated = new Member();
        when(memberService.updateProfile(any(), any(), any(), any(), any(), any(), any(), any())).thenReturn(updated);
        mockMvc.perform(put("/api/v1/members/AA001/profile")
            .contentType(MediaType.APPLICATION_JSON)
            .content(mapper.writeValueAsString(req)))
            .andExpect(status().isOk());
    }

    @Test
    void search_byLastName_returns200() throws Exception {
        when(memberService.searchByLastName("Smith")).thenReturn(Collections.emptyList());
        mockMvc.perform(get("/api/v1/members/search").param("lastName", "Smith"))
            .andExpect(status().isOk());
    }

    @Test
    void deactivate_returns204() throws Exception {
        doNothing().when(memberService).deactivateMember("AA001");
        mockMvc.perform(delete("/api/v1/members/AA001"))
            .andExpect(status().isNoContent());
    }
}
