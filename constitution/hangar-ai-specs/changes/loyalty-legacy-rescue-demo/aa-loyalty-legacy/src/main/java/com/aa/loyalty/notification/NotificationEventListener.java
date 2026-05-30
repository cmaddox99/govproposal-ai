package com.aa.loyalty.notification;

import com.aa.loyalty.events.MilesAccruedEvent;
import com.aa.loyalty.events.MilesExpiredEvent;
import com.aa.loyalty.events.MilesRedeemedEvent;
import com.aa.loyalty.events.TierChangedEvent;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.event.EventListener;
import org.springframework.stereotype.Component;

/**
 * ENG-2.1 — Infrastructure listener: translates domain events into email notifications.
 * Services no longer depend on NotificationService directly — they publish events.
 * This class is the ONLY place that bridges domain events to email infrastructure.
 */
@Component
public class NotificationEventListener {

    @Autowired
    private NotificationService notificationService;

    @EventListener
    public void onMilesAccrued(MilesAccruedEvent event) {
        notificationService.sendMilesAccruedEmail(
            event.getMemberNumber(), event.getMiles(), event.getTransactionRef());
    }

    @EventListener
    public void onTierChanged(TierChangedEvent event) {
        notificationService.sendTierChangeEmail(
            event.getMemberNumber(),
            event.getPreviousTier().name(),
            event.getNewTier().name());
    }

    @EventListener
    public void onMilesRedeemed(MilesRedeemedEvent event) {
        notificationService.sendRedemptionConfirmationEmail(
            event.getMemberNumber(), event.getMiles(), event.getAwardCategory());
    }

    @EventListener
    public void onMilesExpired(MilesExpiredEvent event) {
        notificationService.sendMilesExpiredEmail(
            event.getMemberNumber(), event.getExpiredMiles());
    }
}
