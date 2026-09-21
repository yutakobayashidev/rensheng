# Health

Current health context and the relevant history needed to understand care or prepare for an appointment. Original medical documents and full measurement streams remain in their source systems or existing stores.

## Files

Start with `overview.md` when there is context to summarize. Split out the following only as needed.

| File | Contents | Suggested headings |
| --- | --- | --- |
| `overview.md` | Current concerns and links to care and history | Current / Relevant history / Open questions / References |
| `medications.md` | Documented prescriptions or medication settings and their changes | Current medications / Changes / References |
| `care.md` | Care providers, current care, and confirmed appointments | Care team / Current care / Next appointments / References |
| `visits/YYYY-MM-DD-topic.md` | A particular visit | Reason / Reported symptoms / Findings / Plan / Follow-up / Sources |
| `tests/YYYY-MM-DD-topic.md` | Relevant results and attributed clinical explanations | Test / Results / Clinician explanation / Follow-up / Sources |

A single dated visit page may live directly in `health/` until a subdirectory is useful. Date visit and test pages by the actual event; state the verification date separately when needed.

## Example: a visit page

The text below describes fields to fill from evidence; it is not a medical record.

```markdown
# YYYY-MM-DD — Visit topic

## Reason

Why the appointment took place.

## Reported symptoms

What the user reported, in their own terms where possible.

## Findings

What the clinician or medical record actually stated; include the source.

## Plan

Agreed care plan. Refer to medications.md for documented prescription details.

## Follow-up

Confirmed next appointment or unresolved questions. Keep uncertain dates uncertain.

## Sources

References to the visit note, prescription information, or original document.
```

For `medications.md`, useful fields are the medication name, documented dose and schedule, current status, effective date, and source. Include only known details; do not fill missing instructions from general medical knowledge.

## Updating

Follow [the shared update rules](../AGENTS.md). Separate the user's reports, clinician findings, and Agent interpretations. A prescription is not evidence that a dose was taken, and missing intake records do not prove a missed dose.

Actual intake events and weight or blood-pressure measurements remain in the recording app or original data store. Add a useful period summary with dates, units, and a source reference when needed, rather than copying every value into Markdown. App integration is optional; these guides do not imply an implemented export pipeline.
