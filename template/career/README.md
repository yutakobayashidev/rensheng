# Career

The user's roles, responsibilities, work arrangements, and career decisions. Technical knowledge about a project belongs in the separate Garden or the project's own documentation.

## Files

| File | Contents | Suggested headings |
| --- | --- | --- |
| `overview.md` | Current roles and explicitly stated direction | Current engagements / Direction / Open loops / References |
| `engagements/organization.md` | One ongoing role, affiliation, or contract | Relationship / Current context / Commitments / Recent / Open loops / References |
| `opportunities/role.md` | An application, offer, or negotiation | Position / Stage / Conditions / Next step / Recent / Sources |

Use distinguishing names for multiple roles at the same organization. Start with files directly in `career/` if there are too few to need subdirectories.

## Example: an engagement page

Fictional example, not information about the repository owner:

```markdown
# Example Studio

## Relationship

- Short-term contractor for a prototype. [S1]

## Current context

Verified as of: 2026-01-15.

- The prototype is in review. [S2]

## Commitments

- Agreed deliverable: one prototype and a handover note. [S1]
- Day-to-day tasks: reference to the project's task tracker.

## Recent

- 2026-01-15: submitted the prototype for review. [S2]

## Open loops

- Waiting for review feedback; timing has not been confirmed. [S2]

## References

- S1: reference to the agreed scope.
- S2: reference to the submission message.
- Related person: people/alice.md, relative to the repository root.
- Payment terms: money/income.md, relative to the repository root.
```

## Updating

Follow [the shared update rules](../AGENTS.md). Distinguish an opportunity, an offer, and an accepted arrangement. Store financial terms in [money/](../money/README.md), relationship details in [people/](../people/README.md), and link them from here. Do not infer a career Goal from a burst of work activity.
