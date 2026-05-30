package com.aa.loyalty.notification;

// CHARACTERIZATION TEST — ENG-4.10
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class NotificationServiceTest {

    @Mock JavaMailSender mailSender;

    @InjectMocks NotificationService service;

    @Test
    void sendMilesAccruedEmail_verifiesAllMessageFields() {
        ArgumentCaptor<SimpleMailMessage> captor = ArgumentCaptor.forClass(SimpleMailMessage.class);
        service.sendMilesAccruedEmail("AA001", 1000L, "AA100");
        verify(mailSender).send(captor.capture());
        SimpleMailMessage msg = captor.getValue();
        assertEquals("aadvantage-noreply@aa.com", msg.getFrom());
        assertNotNull(msg.getTo());
        assertEquals("AA001@example.com", msg.getTo()[0]);
        assertNotNull(msg.getSubject());
        assertTrue(msg.getSubject().contains("1000"));
        assertNotNull(msg.getText());
        assertTrue(msg.getText().contains("AA001"));
        assertTrue(msg.getText().contains("AA100"));
    }

    @Test
    void sendMilesAccruedEmail_mailException_swallowsException() {
        doThrow(new RuntimeException("SMTP failure")).when(mailSender).send(any(SimpleMailMessage.class));
        assertDoesNotThrow(() -> service.sendMilesAccruedEmail("AA001", 500L, "AA100"));
    }

    @Test
    void sendRedemptionConfirmationEmail_verifiesAllMessageFields() {
        ArgumentCaptor<SimpleMailMessage> captor = ArgumentCaptor.forClass(SimpleMailMessage.class);
        service.sendRedemptionConfirmationEmail("AA002", 12500L, "AWARD_FLIGHT");
        verify(mailSender).send(captor.capture());
        SimpleMailMessage msg = captor.getValue();
        assertEquals("aadvantage-noreply@aa.com", msg.getFrom());
        assertNotNull(msg.getTo());
        assertEquals("AA002@example.com", msg.getTo()[0]);
        assertNotNull(msg.getSubject());
        assertTrue(msg.getSubject().contains("12500"));
        assertNotNull(msg.getText());
        assertTrue(msg.getText().contains("AA002"));
        assertTrue(msg.getText().contains("AWARD_FLIGHT"));
    }

    @Test
    void sendRedemptionConfirmationEmail_mailException_swallowsException() {
        doThrow(new RuntimeException("SMTP failure")).when(mailSender).send(any(SimpleMailMessage.class));
        assertDoesNotThrow(() -> service.sendRedemptionConfirmationEmail("AA001", 5000L, "UPGRADE"));
    }

    @Test
    void sendMilesExpiredEmail_verifiesAllMessageFields() {
        ArgumentCaptor<SimpleMailMessage> captor = ArgumentCaptor.forClass(SimpleMailMessage.class);
        service.sendMilesExpiredEmail("AA003", 2000L);
        verify(mailSender).send(captor.capture());
        SimpleMailMessage msg = captor.getValue();
        assertEquals("aadvantage-noreply@aa.com", msg.getFrom());
        assertNotNull(msg.getTo());
        assertEquals("AA003@example.com", msg.getTo()[0]);
        assertNotNull(msg.getSubject());
        assertNotNull(msg.getText());
        assertTrue(msg.getText().contains("AA003"));
        assertTrue(msg.getText().contains("2000"));
    }

    @Test
    void sendMilesExpiredEmail_mailException_swallowsException() {
        doThrow(new RuntimeException("SMTP failure")).when(mailSender).send(any(SimpleMailMessage.class));
        assertDoesNotThrow(() -> service.sendMilesExpiredEmail("AA001", 999L));
    }

    @Test
    void sendTierChangeEmail_verifiesAllMessageFields() {
        ArgumentCaptor<SimpleMailMessage> captor = ArgumentCaptor.forClass(SimpleMailMessage.class);
        service.sendTierChangeEmail("AA004", "GENERAL", "GOLD");
        verify(mailSender).send(captor.capture());
        SimpleMailMessage msg = captor.getValue();
        assertEquals("aadvantage-noreply@aa.com", msg.getFrom());
        assertNotNull(msg.getTo());
        assertEquals("AA004@example.com", msg.getTo()[0]);
        assertNotNull(msg.getSubject());
        assertTrue(msg.getSubject().contains("GOLD"));
        assertNotNull(msg.getText());
        assertTrue(msg.getText().contains("AA004"));
        assertTrue(msg.getText().contains("GENERAL"));
        assertTrue(msg.getText().contains("GOLD"));
    }

    @Test
    void sendTierChangeEmail_mailException_swallowsException() {
        doThrow(new RuntimeException("SMTP failure")).when(mailSender).send(any(SimpleMailMessage.class));
        assertDoesNotThrow(() -> service.sendTierChangeEmail("AA001", "GENERAL", "GOLD"));
    }
}
