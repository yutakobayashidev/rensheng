# People

Context about a person's relationship with the user, enough to resume a conversation or understand an unresolved commitment.

## Files

Use one file per person, such as `alice.md`. Add a stable distinguishing term when names collide, such as `alice-example-studio.md`. Create `index.md` only when an overview of existing pages becomes useful.

Keep only the identity and contact references needed to distinguish the person. A full address book, message archive, relationship score, or personality assessment is unnecessary.

## Example: alice.md

Fictional example, not information about the repository owner:

```markdown
# Alice

## Relationship

- Collaborator on Example Project.
- Contact reference: @alice in Example Workspace.

## Current context

Verified as of: 2026-01-15.

- Preparing the next demo together. I handle implementation; Alice reviews the draft. [S1]

## Recent

- 2026-01-15: agreed on the scope of the demo. [S1]
- 2026-01-12: held the first planning meeting. [S2]

## Open loops

- Waiting for Alice's review of the draft. No deadline was established. [S1]
- My follow-up is tracked in the execution app: reference to the demo-sharing task.

## Sources

- S1: reference to the scope-agreement message, 2026-01-15.
- S2: reference to the meeting note, 2026-01-12.
```

## Updating

Follow [the shared update rules](../AGENTS.md). Keep `Current context` short, retain meaningful developments in `Recent`, and remove resolved open loops. Link to related work or education pages for their details. Create pages for relevant relationships instead of automatically turning every sender into a person page.
