# Briefs

Outputs assembled for a particular time and purpose, such as preparing for the day or for an appointment. A Brief is a snapshot of what was useful then.

## Files

The template provides `daily/` for daily outputs. Use `daily/YYYY-MM-DD.md` for one Brief per day. If multiple snapshots are useful, add a distinguishing time or purpose to the name rather than silently replacing an earlier output. Existing Skill-specific names may remain in use.

Create other purpose-specific directories only when actual Briefs need them. The current facts referenced by a Brief belong in the relevant profile or Domain pages and their sources.

## Example: a daily Brief

This scaffold describes sections to populate; it is not a Brief about the repository owner.

```markdown
# Daily Brief — YYYY-MM-DD

Created at: timestamp with timezone.
Coverage period: the interval actually checked.

## Today

Confirmed plans and deadlines, with references to their source evidence.

## Open loops

Relevant unresolved matters, with references to person or Domain pages.

## Suggestions

Suggestions from the external Agent, clearly distinguished from the user's commitments.

## Selected updates

Relevant news or updates, if useful for this Brief, with sources.

## Coverage

Which sources were checked, what could not be accessed, and material uncertainty.
```

## Updating

Follow [the shared update rules](../AGENTS.md). Preserve useful past Briefs as outputs from their creation time. Consult current Domain pages and source evidence when answering a present-state question; do not use an old Brief as the sole proof of a current fact.

Publishing a suggestion in a Brief does not create a Goal, an obligation, or a completed action. An item the user deliberately saves can become a [Capture](../captures/README.md); Knowledge moves to the separate Garden only at the user's decision.
