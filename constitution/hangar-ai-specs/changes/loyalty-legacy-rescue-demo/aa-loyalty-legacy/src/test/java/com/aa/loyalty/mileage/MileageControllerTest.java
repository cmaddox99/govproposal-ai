package com.aa.loyalty.mileage;

// CHARACTERIZATION TEST — ENG-4.10
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;
import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@ExtendWith(MockitoExtension.class)
class MileageControllerTest {

    @Mock MileageService mileageService;
    @InjectMocks MileageController controller;

    MockMvc mockMvc;

    @BeforeEach
    void setup() {
        mockMvc = MockMvcBuilders.standaloneSetup(controller).build();
    }

    @Test
    void getBalance_returns200WithMiles() throws Exception {
        when(mileageService.getTotalMiles("AA001")).thenReturn(42000L);
        mockMvc.perform(get("/api/v1/mileage/AA001/balance"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.totalMiles").value(42000));
    }

    @Test
    void accrueFlightMiles_validRequest_returns200() throws Exception {
        when(mileageService.accrueFlightMiles(any(), any(), any(), any(), any(), any(), any())).thenReturn(1543L);
        mockMvc.perform(post("/api/v1/mileage/AA001/accrue/flight")
            .param("flightNumber", "AA100")
            .param("origin", "DFW")
            .param("destination", "LAX")
            .param("bookingClass", "Y")
            .param("flightDate", "2026-03-15"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.milesAccrued").value(1543));
    }

    @Test
    void accrueFlightMiles_badDateFormat_returns400() throws Exception {
        mockMvc.perform(post("/api/v1/mileage/AA001/accrue/flight")
            .param("flightNumber", "AA100")
            .param("origin", "DFW")
            .param("destination", "LAX")
            .param("bookingClass", "Y")
            .param("flightDate", "not-a-date"))
            .andExpect(status().isBadRequest());
    }

    @Test
    void accrueFlightMiles_sameOriginDestination_returns400() throws Exception {
        mockMvc.perform(post("/api/v1/mileage/AA001/accrue/flight")
            .param("flightNumber", "AA100")
            .param("origin", "DFW")
            .param("destination", "DFW")
            .param("bookingClass", "Y")
            .param("flightDate", "2026-03-15"))
            .andExpect(status().isBadRequest());
    }

    @Test
    void redeemMiles_success_returns200() throws Exception {
        when(mileageService.redeemMiles("AA001", 12500L, "AWARD_FLIGHT", "test")).thenReturn(true);
        mockMvc.perform(post("/api/v1/mileage/AA001/redeem")
            .param("miles", "12500")
            .param("redemptionType", "AWARD_FLIGHT")
            .param("description", "test"))
            .andExpect(status().isOk());
    }

    @Test
    void redeemMiles_insufficientMiles_returns400() throws Exception {
        when(mileageService.redeemMiles("AA001", 99999L, "AWARD_FLIGHT", null)).thenReturn(false);
        mockMvc.perform(post("/api/v1/mileage/AA001/redeem")
            .param("miles", "99999")
            .param("redemptionType", "AWARD_FLIGHT"))
            .andExpect(status().isBadRequest());
    }

    @Test
    void adminAdjust_returns200() throws Exception {
        doNothing().when(mileageService).adminAdjustMiles("AA001", 500L, "goodwill", "AGENT01");
        mockMvc.perform(post("/api/v1/mileage/admin/adjust")
            .param("memberNumber", "AA001")
            .param("adjustment", "500")
            .param("reason", "goodwill")
            .param("agentId", "AGENT01"))
            .andExpect(status().isOk());
    }

    @Test
    void getBalance_serviceThrowsException_returns500() throws Exception {
        when(mileageService.getTotalMiles("AA999")).thenThrow(new RuntimeException("DB down"));
        mockMvc.perform(get("/api/v1/mileage/AA999/balance"))
            .andExpect(status().is5xxServerError());
    }
}
