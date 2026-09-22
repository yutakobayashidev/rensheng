# Rensheng

This is a private, local-first repository for Personal Context that both you and your Agents can retrace later.

## Start here

Ask an Agent to follow the [Rensheng setup guide](https://github.com/yutakobayashidev/rensheng/blob/main/docs/setup.md), using this private repository as the destination:

1. Keep this repository private and connect the sources you want to use, such as Gmail, Calendar, or Beeper.
2. Choose the output language in [AGENTS.md](AGENTS.md). The starter defaults to Japanese; setup confirms your choice before writing personal content. Existing instance settings are preserved unless you request a change.
3. Run [rensheng-backfill](.agents/skills/rensheng-backfill/SKILL.md) to initialize `profile/`, relevant `people/` pages, accepted `goals.md` entries, and the compilation history in `recent-updates.md` from available evidence.

You can also write these files directly. Add only Goals you have accepted and want tracked, and record meaningful changes in `recent-updates.md`. Use the guides below when creating a page; there is no requirement to fill every file or heading.

Read [`philosophy.md`](philosophy.md) for the information boundaries and design principles.

## Current context

`recent-updates.md` and `goals.md` together serve as the practical current-context entrypoint. They do not replace evidence in profile, Domain, Capture, Brief, or source files.

`recent-updates.md` records which pages changed and why. Daily events, measurements, and journal entries remain in their source applications or stores; do not copy them all into this changelog.

Use [`index.md`](index.md) to find existing pages by their purpose. It complements the current-context entrypoint; its descriptions do not replace the pages or their evidence. Agents maintain the index alongside authorized page edits. [`index-state.json`](index-state.json) records the page and description versions reviewed together.

## Files and guides

| Location | What belongs here | Guide |
| --- | --- | --- |
| `index.md`, `index-state.json` | Navigation descriptions and machine-written review hashes | [Index maintenance](scripts/README.md) |
| `profile/` | Stable background, communication preferences, and working conditions | [Profile](profile/README.md) |
| `people/` | A person's relationship with you and its current context | [People](people/README.md) |
| `health/` | Current care, prescriptions, and relevant medical history | [Health](health/README.md) |
| `money/` | Accounts, income, subscriptions, other recurring payments, and obligations | [Money](money/README.md) |
| `career/` | Your roles, commitments, and work opportunities | [Career](career/README.md) |
| `education/` | Enrollment, applications, and learning progress | [Education](education/README.md) |
| `home/` | Housing, utilities, maintenance, and practical procedures | [Home](home/README.md) |
| `routines/` | Procedures you use in daily life | [Routines](routines/README.md) |
| `recipes/` | Personal cooking instructions | [Recipes](recipes/README.md) |
| `captures/` | Items deliberately saved for later retrieval | [Captures](captures/README.md) |
| `briefs/` | Outputs assembled for a particular time and purpose | [Briefs](briefs/README.md) |
| `.agents/skills/` | Reusable Agent procedures, without personal data | Individual `SKILL.md` files |

Each folder's `README.md` explains its purpose, file names, and example contents. An `overview.md`, where useful, describes your current situation and points to details. Individual pages are created only when there is information to put in them. An Agent can create or split pages as needed; you do not need to maintain an empty hierarchy.

All examples in these guides are fictional and appear inside code blocks. They are documentation, not facts about the repository owner. Do not copy them into live pages as onboarding data. Suggested headings are optional; no universal `template.md`, frontmatter, tags, or UUID scheme is required.

Common evidence and update rules live in [AGENTS.md](AGENTS.md).

## Index freshness

With Python 3.10+, check navigation without modifying any files:

```console
python3 scripts/index.py check
```

The helper detects unlisted or missing pages and changed page/description hashes. It never writes personal pages, infers facts, or generates descriptions. An Agent reviews the affected entries before recording their hashes. See [Index maintenance](scripts/README.md) for the complete workflow and the separate meanings of `updated_at`, `verified_at`, and `indexed_at`.

The initial index and receipts describe empty starter pages only. Existing private instances can adopt the index without filling missing profile facts or rewriting every page. The helper is optional maintenance tooling; ordinary file reading and search remain sufficient to use Rensheng.

## Goals and updates

An accepted Goal can include the user's wording, acceptance date, desired outcome, and a link to supporting context. Include a deadline only when one is known. The existing time horizons are optional groupings, not a requirement to set a new Goal every day.

Fictional `goals.md` entry:

```markdown
## This month

- Set up a usable workspace at home.
  - Accepted: 2026-01-15, in the user's own note.
  - Done when: the desk and required equipment are ready to use.
  - Context: home/housing.md.
```

Fictional `recent-updates.md` entry, newest date first:

```markdown
## 2026-01-15

- people/alice.md: recorded the agreed demo responsibilities and review still pending; linked the source message.
- money/subscriptions.md: reflected Example Service's confirmed plan change.
```

## OpenBrief

[OpenBrief](https://github.com/yutakobayashidev/rensheng) is an optional Rensheng component for metadata-minimal Attention Handoff and context resumption. A Rensheng repository remains useful without installing OpenBrief.

## Privacy

Do not commit credentials, raw private-message archives, unredacted financial or medical originals, or other secrets. Keep large raw data in its source system or a separate local store and compile only the context needed here.
