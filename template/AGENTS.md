# Agent Guidelines

This repository is a private Rensheng instance. Treat every file as personal data unless the user explicitly says otherwise.

## Output language

- Expected output language: Japanese (`ja`).
- Respond to the user and write new or substantially revised Personal Context in Japanese unless the user explicitly requests another language.
- Preserve existing wording, quotations, proper nouns, source titles, and technical terms when translation would reduce fidelity. Do not translate unchanged pages only for consistency.

## Reading order

For questions about the user's current situation:

1. Read `recent-updates.md` and `goals.md`.
2. Use `index.md`, when present, to locate relevant pages; read `profile/overview.md` and the relevant profile or Domain files. Index descriptions are navigation, not evidence of current facts.
3. Read `captures/` or `briefs/` only when the question requires them.
4. Return to external source evidence only when the compiled Markdown is insufficient.

## Boundaries

- Do not infer a durable Goal from behavior alone. Propose it and wait for user acceptance.
- Treat Interest as a query over history, not a permanent label. A single Capture is not proof of identity.
- Do not copy secrets, raw message archives, financial statements, or medical originals into generated summaries.
- Keep Knowledge about the world in the separate Garden, not in Personal Context.
- Prefer small, focused updates. Preserve user-authored statements unless the user requests rewriting.

## Creating and updating pages

- Read the relevant folder's `README.md` before creating or restructuring its pages. README examples, instructional comments, and placeholders are not evidence about the user; never import fictional examples as personal facts.
- Create a page only when there is information to record. Use the suggested file names and headings when useful; omit empty sections and add subdirectories only when needed. Do not make the user complete a template or perform routine filing.
- Keep each detailed fact in one primary location and link to it from related pages. An `overview.md` is a short current summary and entrypoint, not a copy of every page.
- State when a current condition was verified. Separate event dates from verification dates; a file's edit date does not establish that its contents are still current.
- Keep source links or references near material claims and state changes. Reuse source IDs where available. Distinguish the user's statements, external evidence, and Agent interpretations. Do not mark an unfetched source as verified.
- Missing information means unknown, not absent. Preserve uncertainty and conflicting evidence instead of silently choosing a value.
- Keep `Recent` or `Changes` sections to meaningful developments. Remove resolved items from current open loops and retain a short outcome when useful.
- Open loops explain what remains unresolved in that context. Link to tasks in an execution app when one is used; do not maintain a second task completion state here.
- Record meaningful compilation changes in `recent-updates.md`, newest first, with the affected paths and a short explanation. Do not turn it into a raw life-event log.
- Preserve user-authored wording separately from generated summaries when regenerating views. Originals remain in their source systems or existing stores; this template does not introduce a raw-data store or a new Timeline.

## Index and timestamps

- Maintain `index.md` with links to existing personal pages and one-line descriptions, grouped by Domain. Keep details in their primary pages. Do not list every guide, skill, or raw source.
- Follow [scripts/README.md](scripts/README.md) for timestamp meanings and the index helper. Record `updated_at` when editing a personal page; preserve legacy formats and leave unchanged pages alone. Keep `verified_at` or `Verified as of:` beside the facts actually checked, with evidence. Do not invent dates for starter placeholders.
- After finishing authorized page and changelog edits, read the affected pages and review their index entries. Run `python3 scripts/index.py check`; record only the reviewed page/entry versions using the returned hashes. `index-state.json` contains navigation receipts, not verification of external facts. Never refresh hashes blindly to clear a warning.
- Repeated checks are read-only; unchanged receipts keep their timestamps. Index-only maintenance does not create a `recent-updates.md` entry. Missing or stale receipts do not prevent reading the original pages.
- If the helper cannot run, maintain the index as authorized and report hash checking as pending. Never fabricate hashes. Keep partial or unrelated indexing gaps visible rather than expanding a bounded task automatically.
