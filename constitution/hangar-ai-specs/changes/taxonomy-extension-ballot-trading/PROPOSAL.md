# Taxonomy Extension Proposal — Crew Self-Service & Trip Trading

## Request
Add new product-type taxonomy category: **"Crew Self-Service & Trip Trading"**

## Justification
The Pilot Ballot & Trip Trading platform (`hangar-w4-ballot-trading`) is a standalone product domain enabling pilots to trade, swap, and bid on flight trip pairings. It does not fit any existing product-type category:

| Nearest Existing Category | Why It Does Not Apply |
|---|---|
| `crew-training-scheduling` | Governs FAA/DO-178C training qualification and FAR Part 117 duty-rest. No trading/ballot functionality. |
| `schedule-change-self-serve` | Governs passenger flight booking changes. Different user base and CBA scope. |
| `gate-management` | Airport gate ops — unrelated. |

## Proposed Category Entry
```yaml
- id: ballot-trading
  name: "Pilot Ballot & Trip Trading"
  category: "Crew Self-Service & Trip Trading"
  description: CBA-governed pilot trip-pairing trades, ballot submissions, and reserve availability
  established: "2026-04-27"
  status: active
```

## Taxonomy Gates
- **domain_gate:** PASS — capability is business-domain-based, not team-name-based
- **user_journey_gate:** PASS — distinct journeys: trade submission, eligibility check, batch award, reserve check, dispute review
- **boundary_gate:** PASS — clearly separated from training scheduling and passenger booking
- **stability_gate:** PASS — survives org restructure; the CBA-governed trading capability is an enduring business function
- **retrieval_gate:** PASS — "ballot trading", "trip trade", "pilot bidding" queries route precisely to this avatar

## Approval Path
**STATUS: PENDING — awaiting Director+ (or designated taxonomy owner) sign-off**

Per BUS-7.1 (Audit Trail) and ENG-11.1 (Hangar SDD governance), a taxonomy extension
cannot be self-approved by the proposing author in the same PR that adopts it. An
independent, named approver at Director level or above (or the designated taxonomy
owner) must record their approval here before the registry adoption is considered
binding.

| Field | Value |
|---|---|
| Proposed by | (author of this PR) |
| Proposed date | 2026-04-27 |
| Approver name | _to be filled by approver_ |
| Approver role | _Director+ or designated taxonomy owner_ |
| Approval date | _to be filled by approver_ |
| Approval evidence | _link to approval (PR review, ticket, email artifact)_ |

Until this section is completed by an independent named approver, the
`ballot-trading` entries in `avatars/index.yaml`, `avatars/product-type/index.yaml`,
and `avatars/AVATAR-RAG-INDEX.yaml` are marked **provisional** via their
`taxonomy_extension_status` / `status` fields and MUST NOT be relied upon as
governance-authoritative classifications.
