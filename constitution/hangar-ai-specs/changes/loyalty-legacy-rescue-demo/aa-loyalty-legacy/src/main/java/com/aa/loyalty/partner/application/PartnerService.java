package com.aa.loyalty.partner.application;

import com.aa.loyalty.events.MilesAccruedEvent;
import com.aa.loyalty.mileage.domain.MileageCalculationPort;
import com.aa.loyalty.mileage.application.MileageService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.stereotype.Service;
import java.util.Date;
import java.util.List;
import java.util.logging.Logger;
import com.aa.loyalty.partner.domain.Partner;
import com.aa.loyalty.partner.domain.PartnerRepository;

@Service
public class PartnerService {

    private static final Logger LOG = Logger.getLogger(PartnerService.class.getName());

    @Autowired
    private PartnerRepository partnerRepository;

    @Autowired
    private MileageService mileageService;

    @Autowired
    private MileageCalculationPort mileageCalculationPort;

    @Autowired
    private ApplicationEventPublisher eventPublisher;

    public List<Partner> getActivePartners() {
        return partnerRepository.findByActive(true);
    }

    public long processPartnerAccrual(String memberNumber, String partnerCode,
                                      double spendAmount, String transactionRef) {
        Partner partner = partnerRepository.findByPartnerCode(partnerCode);
        if (partner == null || !partner.getActive()) {
            LOG.warning("Unknown or inactive partner: " + partnerCode);
            return 0;
        }

        long miles = mileageCalculationPort.calculatePartnerMiles(
            partnerCode, spendAmount, "GENERAL"); // ENG-2.1 FIX: use calculatePartnerMiles, not accrueFlightMiles
        if (miles <= 0) return 0;

        mileageService.accrueFlightMiles(memberNumber, transactionRef, "PARTNER", partnerCode,
            null, new Date(), transactionRef);

        eventPublisher.publishEvent(new MilesAccruedEvent(memberNumber, miles, transactionRef, "PARTNER"));

        return miles;
    }

    // VIOLATION: returns Partner including apiKey — security over-exposure
    public Partner getPartnerDetails(String partnerCode) {
        return partnerRepository.findByPartnerCode(partnerCode);
    }
}
