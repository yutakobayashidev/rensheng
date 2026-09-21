# Money

Current financial arrangements: accounts, income, subscriptions, other recurring payments, and obligations. The aim is to answer what is active, what it costs, and what is coming up.

## Files

Create only the files for which there is information.

| File | Contents | Suggested headings |
| --- | --- | --- |
| `overview.md` | A short current summary and upcoming payments or renewals | Current / Upcoming obligations / Open loops / References |
| `accounts.md` | Account or payment-method labels, purposes, and status | Accounts / Purpose / Status / References |
| `income.md` | Income sources and documented payment terms | Income sources / Terms / Changes / References |
| `subscriptions.md` | Software, media, memberships, and other subscription services | Active subscriptions / Details / Changes / References |
| `recurring.md` | Other recurring payments, such as rent, utilities, and insurance | Other recurring payments / Terms / Changes / References |
| `obligations.md` | Outstanding payments, repayments, and other amounts due | Obligations / Changes / Sources |

Keep each payment in one detailed location. For example, `recurring.md` holds rent payment terms while [home/](../home/README.md) holds the housing arrangements. `obligations.md` may reference a specific overdue payment without duplicating the full contract.

## Example: subscriptions.md

Fictional services, amounts, and dates; these are not the user's subscriptions.

```markdown
# Subscriptions

Verified as of: 2026-01-15.

## Active subscriptions

| Service / plan | Charge | Billing cycle | Next charge | Status | Source |
| --- | --- | --- | --- | --- | --- |
| Example Service / Standard | 900 JPY | Monthly | 2026-02-01 | Active; auto-renewal on | S1 |
| Example Storage / Personal | 6,000 JPY | Annual | None scheduled | Cancellation confirmed; access through 2026-06-30 | S2 |

## Details

### Example Service

- Purpose: sharing files for a volunteer project, as stated by the user.
- Manage billing: reference to the service's account settings.
- Cancellation deadline and conditions: not verified.
- Verified: 2026-01-15. [S1]

### Example Storage

- Auto-renewal: off. [S2]
- Access ends: 2026-06-30. [S2]
- Verified: 2026-01-15. [S2]

## Changes

- 2026-01-15: Example Service changed to Standard. [S1]
- 2026-01-15: Example Storage cancellation confirmed; access remains available until the end of the paid term. [S2]

## References

- S1: references to Example Service's billing page and plan-change confirmation.
- S2: reference to Example Storage's cancellation confirmation.
```

Keep subscriptions in one file initially. Split out a service page only when its terms or history become long enough to need one, leaving a short entry and reference in `subscriptions.md`.

## Dates, amounts, and status

- Distinguish the next charge, contract renewal, trial end, cancellation deadline, and access end. Include only dates that are useful and known. A previous charge alone does not confirm the next renewal date.
- “Want to cancel,” “cancellation requested,” “cancellation confirmed with access remaining,” and “ended” are different states. Remove ended subscriptions from the active list and retain meaningful history.
- Include amount, currency, and billing cycle together. State whether tax is included only when known. A monthly equivalent, if useful, is a separate estimate with its calculation; it is not the actual amount due that month. Do not silently combine different currencies.
- Optional payment-method references point to `accounts.md` using a recognizable label. Do not store credentials or full account/card numbers.
- Record the user's stated purpose or intention when known. An Agent's suggestion to review or cancel a subscription is not a decision or an instruction already executed.

## Updating

Follow [the shared update rules](../AGENTS.md). Billing pages, receipts, and confirmation messages can substantiate changes. Keep transaction histories and financial originals in their source systems; any balance summary needs an as-of date. Link review or cancellation tasks to the execution app when one is used, and keep the contract state grounded in evidence.
