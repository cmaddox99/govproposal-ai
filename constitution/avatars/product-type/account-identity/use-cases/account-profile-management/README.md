```yaml
use_case:
  id: uc-account-profile-management
  name: Account Profile Management
  jtbd: "When a traveler needs to update their contact information, travel preferences, or secure
    traveler details, they need to edit their account profile so their reservations and
    communications are accurate."
  actor: Authenticated Traveler
  laws: [PRD-1.2, PRD-1.5, BUS-4.3, BUS-7.1, BUS-9.3]
  source_modules:
    - AccountProfileEndpoint
    - SecureTravelerEndpoint
    - SecureTravelerSubmitEndpoint
    - UserAccountInfo
    - AccountInfoActor
    - TravelCreditEndpoint
    - MyAccountBridgedWebViewController
    - MyAccountNavigationManager
```

---

# Use Case: Account Profile Management

**Avatar:** avatar-account-identity
**Framework:** account-ios — AmericanAccount (358 Swift files)

---

## Scope

Account profile management covers the ability for an authenticated traveler to view and edit the personal data stored on their American Airlines account. This includes:

- **Contact information:** email address, phone number, mailing address — via `AccountProfileEndpoint` and `UserAccountInfo`.
- **Secure traveler details:** Known Traveler Number (KTN), TSA PreCheck, Global Entry — via `SecureTravelerEndpoint` and `SecureTravelerSubmitEndpoint`.
- **Travel preferences:** seat preferences, meal preferences, communication preferences — via `AccountProfileEndpoint`.
- **Profile data assembly:** `AccountInfoActor` orchestrates retrieval and caching of profile state; `UserAccountInfo` is the primary profile data model.
- **Travel credit view:** `TravelCreditEndpoint` surfaces travel credit balances on the account profile screen.

**Out of scope:** AAdvantage miles balance, status tier, upgrade waitlists, and loyalty benefits — these are owned by **loyalty-aadvantage**. AAdvantage member number appears in `UserAccountInfo` as an identifier only.

---

## Web-Bridge Architecture Note (ENG-3.1)

> ⚠️ **Profile screens are rendered via `MyAccountBridgedWebViewController` (WKWebView).** This is an ENG-3.1 architectural risk. Profile editing UI is web content, not native SwiftUI or UIKit. Product must coordinate with engineering for any profile screen change, as:
> - Field-level instrumentation is limited compared to native screens.
> - Web-bridge screens have a 4.6% error rate vs. 2.0% for native screens.
> - Web-bridge screens load in 3.1s median vs. 1.3s for native screens.
> - Any migration of profile screens to native requires evidence per PRD-1.5 — do not migrate without error-rate and load-time data confirming the problem.

`MyAccountNavigationManager` routes authenticated users to the profile screens. Navigation entry points are native; screen rendering is web-bridge.

---

## Data Subject Rights (BUS-4.3)

Account profile contains PII subject to the full set of data subject rights under BUS-4.3. This is the **primary compliance obligation** for this use case.

### Right to Access
Users have the right to access all profile data held by American Airlines on their account. Data accessible via `AccountProfileEndpoint` and `UserAccountInfo` must be producible in a data subject access response. `AccountInfoActor` is the integration point for assembling a complete profile data record.

### Right to Correct
Users must be able to correct inaccurate profile data. Every editable field accessible via `AccountProfileEndpoint` and `SecureTravelerSubmitEndpoint` must be correctable by the data subject. A submit failure from `SecureTravelerSubmitEndpoint` that prevents correction is a BUS-4.3 compliance gap and must be treated as a priority defect.

### Right to Delete
Users may request deletion of their account profile. Deletion requests must flow through the appropriate systems to remove `UserAccountInfo`, `AccountCache`, and `AccountProfileEndpoint` records. Partial deletion (e.g., removing a KTN without closing the account) must also be supported where applicable.

### Data Classification for Profile Fields

| Field Category | Classification | Notes |
|---|---|---|
| Name, email, phone | PII — Standard | Covered by BUS-4.3 access/correct/delete |
| Mailing address | PII — Standard | Covered by BUS-4.3 |
| Known Traveler Number (KTN) | PII — Government ID | SecureTravelerEndpoint; heightened care |
| TSA PreCheck number | PII — Government ID | SecureTravelerEndpoint; heightened care |
| Global Entry number | PII — Government ID | SecureTravelerEndpoint; heightened care |
| Passport details | PII — Sensitive | If in scope; highest classification |
| Travel preferences | PII — Behavioral | Covered by BUS-4.3 |

New fields added to `AccountProfileEndpoint` or `UserAccountInfo` require a data classification review before shipping.

---

## Audit Trail Requirements (BUS-7.1)

All profile change events must be captured in the account audit log:

| Event | Log Required |
|---|---|
| Profile view (data accessed) | Yes — with timestamp, authenticated session ID |
| Profile field update submitted | Yes — field name (not value), old/new change indicator, outcome |
| SecureTravelerSubmitEndpoint submission success | Yes |
| SecureTravelerSubmitEndpoint submission failure | Yes — with error type |
| Data subject deletion request received | Yes |
| Data subject access request fulfilled | Yes |

**Note:** BUS-7.1 audit log entries must capture the field name but **must not** capture the plaintext value of PII fields (e.g., do not log KTN or passport number in audit records). Log the change event, not the data content.

---

## Breach Notification Scope (BUS-9.3)

Account profile data — particularly government ID fields (KTN, TSA PreCheck, Global Entry) and contact information — is high-value PII. A breach of `AccountProfileEndpoint` or `UserAccountInfo` data would trigger BUS-9.3 notification obligations.

Applicable scenarios:
- Unauthorized read access to `AccountProfileEndpoint` records for more than one user.
- Unauthorized modification of `SecureTravelerEndpoint` data (KTN, TSA PreCheck, Global Entry numbers).
- `AccountCache` or `UserAccountCache` data exposure via a caching vulnerability that surfaces one user's profile data to another user's session.

BUS-9.3 notification timelines and affected-user calculation must account for the full scope of `UserAccountInfo` records potentially exposed — not just the triggering record.

---

## Evidence Standards for Profile Feature Investment (PRD-1.5)

Profile feature decisions must be backed by data:

- **Completion rate:** What percentage of users who initiate a profile edit complete the submission via `SecureTravelerSubmitEndpoint` or `AccountProfileEndpoint`? Completion rate below 60% indicates a UX or technical friction problem that must be addressed before expanding profile scope.
- **Error rate:** `SecureTravelerSubmitEndpoint` submission error rate is the primary quality signal. Track error type distribution (validation error, network error, backend error) to direct fixes.
- **Support deflection:** Profile feature value is partly measured by reduction in "update profile" support contact volume. This requires support ticket tagging coordination.
- **Web-bridge performance:** Load time and error rate for `MyAccountBridgedWebViewController`-rendered profile screens must be tracked as baseline metrics before any migration or change decision per PRD-1.5.

---

## MVP Discipline (PRD-5.1)

Profile management has a large potential feature surface. Apply MVP discipline:

- **Start with the highest-value, lowest-risk field.** KTN update via `SecureTravelerSubmitEndpoint` is the recommended first increment — it has a clear support deflection signal and a narrow backend integration.
- **Do not bundle profile field types.** Government ID fields (KTN, TSA PreCheck, Global Entry) have different compliance requirements than contact fields. Ship and validate them separately.
- **Web-bridge constraint.** `MyAccountBridgedWebViewController` limits native instrumentation on profile screens. Factor this into MVP metric design — ensure the success signal (completion rate, error rate) is measurable before defining the MVP success threshold.
