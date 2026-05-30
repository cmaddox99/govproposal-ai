# AADvantage Loyalty — Core Member Journeys

**Avatar:** `avatar-loyalty-aadvantage`
**Domain:** Member Loyalty Program
**BFF Modules:** `mobile-aadvantage-bff` · `aa-ct-fly-mobile-loyalty-bff` · `Mobile-Loyalty-Events-Qualifier`

---

## Journey 1: Member Enrollment & Onboarding

**Trigger:** Passenger creates AAdvantage account (web, app, or at check-in) — handled by `aa-ct-fly-mobile-loyalty-bff` (CHUB enrollment).

**Steps:**
1. Account creation (email, name, home airport, password)
2. Identity verification and duplicate account check
3. Welcome email with account number and benefits summary
4. First-login onboarding flow: program overview, tier structure, earning basics
5. Credit card offer presented (AAdvantage Citi / Barclays)
6. First earning opportunity: link upcoming booking to new account

**Success criteria:**
- Account created and verified within 2 minutes
- Welcome email delivered within 5 minutes
- First earning event linked within 30 days (onboarding success)

**Exception flows:**
- Duplicate account detected → merge flow or support handoff
- Email verification failure → resend with 24-hour expiry

---

## Journey 2: Points Earning Through Travel & Partners

**Trigger:** Member completes a qualifying flight segment or partner transaction — PNR feed processed by `Mobile-Loyalty-Events-Qualifier` (PnrFeedReceiver / TailoredOffersReceiver via Kafka).

**Steps:**
1. Flight completed (or partner transaction posted)
2. PNR matched to AAdvantage number
3. Base miles calculated (distance × earning tier multiplier)
4. Bonus miles applied (elite status, credit card, promotion)
5. Points ledger updated; member notified via email/app
6. Elite Qualifying Miles (EQM/EQD) credited toward status threshold

**Partner earning sub-flow (shopping/dining/hotel):**
1. Member clicks through AAdvantage shopping portal or uses linked card
2. Partner transaction reported to AAdvantage API
3. Points posted within 3–7 business days
4. Member notified of partner earning

**Success criteria:**
- Flight miles posted within 72 hours of segment completion
- Partner miles posted within SLA window
- Member can view pending and posted miles in app

---

## Journey 3: Points Redemption (Award Booking)

**Trigger:** Member initiates award flight search in app or web — served by `mobile-aadvantage-bff` (GraphQL + WSDL downstream).

**Steps:**
1. Member searches available award inventory (origin, destination, date, cabin)
2. System queries award seat availability (saver and anytime tiers)
3. Member selects flight; system displays miles required + fees
4. Member confirms redemption; balance validated in real time
5. Award booking confirmed; PNR created; e-ticket issued
6. Points deducted from ledger; member notified with booking confirmation

**Exception flows:**
- Insufficient points balance → present upgrade options or co-pay paths
- No award availability on selected date → alternative date suggestions
- Booking failure → points not deducted; retry prompt

**Success criteria:**
- Award search returns results in < 3 seconds
- Booking completion rate ≥ target threshold
- Points deducted accurately with zero double-deduction incidents

---

## Journey 4: Elite Status Tracking & Qualification

**Trigger:** Member approaches elite status threshold (Gold, Platinum, Executive Platinum, ConciergeKey).

**Steps:**
1. Member views real-time EQM/EQD progress in app dashboard
2. System surfaces milestone notification at 75%, 90%, 100% of threshold
3. Member reviews accelerator options (partner earning, promotions, mileage boosts)
4. Threshold reached: status upgrade processing initiated
5. New elite card mailed; benefits activated in system
6. Member receives elite welcome communications with benefit guide

**Exception flows:**
- EQM posted incorrectly → member files missing miles claim
- Status extension request (illness, travel disruption) → ConciergeKey review

**Success criteria:**
- Real-time progress accuracy within 24 hours of flight completion
- Status upgrade processing completed within 48 hours of qualification
- Elite achievement rate ≥ target (25% of frequent traveler cohort)

---

## Journey 5: Retention & Win-Back Campaigns

**Trigger:** Member inactivity signal (no earning/redemption in 90–180 days) or churn risk score threshold — win-back offers delivered via `mobile-aadvantage-bff` push notifications.

**Steps:**
1. Churn model scores members weekly; flags at-risk cohort
2. Win-back offer selected based on member segment (casual/frequent/elite)
3. Offer delivered via preferred channel (email, app push, or loyalty portal)
4. Member engages with offer → booking or earning action taken
5. Re-engagement recorded; cohort removed from win-back queue
6. 90-day outcome tracked for incrementality measurement (PRD-6.2)

**Exception flows:**
- Member opted out of all communications → offer suppressed; logged
- Member books but subsequently cancels → re-enter win-back queue after 30 days

**Success criteria:**
- Win-back 90-day re-engagement rate ≥ 8%
- Churn model AUC ≥ 0.75 in production monitoring
- Re-engagement incremental lift measured vs. holdout group
