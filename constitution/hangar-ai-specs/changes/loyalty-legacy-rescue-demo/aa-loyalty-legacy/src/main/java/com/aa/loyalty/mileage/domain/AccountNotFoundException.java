package com.aa.loyalty.mileage.domain;

/**
 * ENG-3.7 — Domain-specific exception; never throw generic RuntimeException from service layer.
 */
public class AccountNotFoundException extends RuntimeException {
    public AccountNotFoundException(String memberNumber) {
        super("Mileage account not found for member: " + memberNumber);
    }
}
