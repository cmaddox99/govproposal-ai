package com.aa.loyalty.notification;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.stereotype.Service;
import java.util.logging.Logger;

/**
 * VIOLATIONS:
 * - No email template system — message bodies hardcoded in Java strings
 * - No queue/async sending — synchronous SMTP blocks request thread
 * - No retry logic
 * - Hardcoded from-address
 * - 4 near-identical methods violate DRY (ENG-6.1 NON-NEGOTIABLE)
 */
@Service
public class NotificationService {

    private static final Logger LOG = Logger.getLogger(NotificationService.class.getName());

    // VIOLATION: hardcoded sender address
    private static final String FROM = "aadvantage-noreply@aa.com";

    @Autowired
    private JavaMailSender mailSender;

    // VIOLATION: all notification methods nearly identical — no template abstraction
    public void sendMilesAccruedEmail(String memberNumber, long miles, String flightNumber) {
        try {
            SimpleMailMessage msg = new SimpleMailMessage();
            msg.setFrom(FROM);
            msg.setTo(memberNumber + "@example.com");
            msg.setSubject("Miles Accrued: " + miles + " miles for flight " + flightNumber);
            msg.setText("Dear Member " + memberNumber + ",\n\n"
                + "You have earned " + miles + " miles for flight " + flightNumber + ".\n\n"
                + "Your total miles will be updated within 24 hours.\n\n"
                + "AAdvantage Team");
            mailSender.send(msg);
        } catch (Exception e) {
            LOG.warning("Email failed for accrual: " + e.getMessage()); // VIOLATION: swallowed
        }
    }

    public void sendRedemptionConfirmationEmail(String memberNumber, long miles, String type) {
        try {
            SimpleMailMessage msg = new SimpleMailMessage();
            msg.setFrom(FROM);
            msg.setTo(memberNumber + "@example.com");
            msg.setSubject("Redemption Confirmation: " + miles + " miles redeemed");
            msg.setText("Dear Member " + memberNumber + ",\n\n"
                + "Your redemption of " + miles + " miles (" + type + ") has been confirmed.\n\n"
                + "AAdvantage Team");
            mailSender.send(msg);
        } catch (Exception e) {
            LOG.warning("Email failed for redemption: " + e.getMessage());
        }
    }

    public void sendMilesExpiredEmail(String memberNumber, long expiredMiles) {
        try {
            SimpleMailMessage msg = new SimpleMailMessage();
            msg.setFrom(FROM);
            msg.setTo(memberNumber + "@example.com");
            msg.setSubject("IMPORTANT: Your AAdvantage miles have expired");
            msg.setText("Dear Member " + memberNumber + ",\n\n"
                + expiredMiles + " miles have expired due to account inactivity.\n\n"
                + "AAdvantage Team");
            mailSender.send(msg);
        } catch (Exception e) {
            LOG.warning("Email failed for expiry: " + e.getMessage());
        }
    }

    public void sendTierChangeEmail(String memberNumber, String oldTier, String newTier) {
        try {
            SimpleMailMessage msg = new SimpleMailMessage();
            msg.setFrom(FROM);
            msg.setTo(memberNumber + "@example.com");
            msg.setSubject("Congratulations! Your AAdvantage status has changed to " + newTier);
            msg.setText("Dear Member " + memberNumber + ",\n\n"
                + "Your AAdvantage status has changed from " + oldTier + " to " + newTier + ".\n\n"
                + "AAdvantage Team");
            mailSender.send(msg);
        } catch (Exception e) {
            LOG.warning("Email failed for tier change: " + e.getMessage());
        }
    }
}
