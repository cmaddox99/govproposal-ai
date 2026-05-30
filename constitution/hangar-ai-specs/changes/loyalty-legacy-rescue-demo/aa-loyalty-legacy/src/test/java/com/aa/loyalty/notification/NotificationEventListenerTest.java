package com.aa.loyalty.notification;

import com.aa.loyalty.events.*;
import com.aa.loyalty.tier.domain.TierStatus;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.mockito.Mockito.verify;

/**
 * ENG-2.1 — Verifies NotificationEventListener translates domain events to NotificationService calls.
 * ENG-4.1 — Written before NotificationEventListener was created (TDD).
 */
@ExtendWith(MockitoExtension.class)
class NotificationEventListenerTest {

    @Mock
    NotificationService notificationService;

    @InjectMocks
    NotificationEventListener listener;

    @Test
    void onMilesAccrued_delegatesToNotificationService() {
        MilesAccruedEvent event = new MilesAccruedEvent("AA001", 1500L, "AA100", "FLIGHT");
        listener.onMilesAccrued(event);
        verify(notificationService).sendMilesAccruedEmail("AA001", 1500L, "AA100");
    }

    @Test
    void onTierChanged_delegatesToNotificationService() {
        TierChangedEvent event = new TierChangedEvent("AA002", TierStatus.GENERAL, TierStatus.GOLD);
        listener.onTierChanged(event);
        verify(notificationService).sendTierChangeEmail("AA002", "GENERAL", "GOLD");
    }

    @Test
    void onMilesRedeemed_delegatesToNotificationService() {
        MilesRedeemedEvent event = new MilesRedeemedEvent("AA003", 25000L, "AWARD_FLIGHT");
        listener.onMilesRedeemed(event);
        verify(notificationService).sendRedemptionConfirmationEmail("AA003", 25000L, "AWARD_FLIGHT");
    }

    @Test
    void onMilesExpired_delegatesToNotificationService() {
        MilesExpiredEvent event = new MilesExpiredEvent("AA004", 5000L);
        listener.onMilesExpired(event);
        verify(notificationService).sendMilesExpiredEmail("AA004", 5000L);
    }
}
