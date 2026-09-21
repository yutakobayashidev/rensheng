# Rensheng

## 1. What Rensheng Is

Rensheng is **a system that stores your digital life under your own control and continuously compiles it into context that both humans and AI can retrace later**.

Rensheng itself is not a:

* TODO app
* Knowledge Base
* AI Chat
* Digital Garden
* Lifelogger
* Personal CRM

It exists at a lower layer, supporting these as needed.

The state it aims to achieve is:

> **Simply by living your life, the context about you grows.**

To develop Rensheng, users do not need to:

* Add tags
* Design folder structures
* Copy information manually every day
* Manually sort every saved item
* Explain themselves to AI every time

---

# 2. Core Outcome

The ultimate outcome of Rensheng is:

> **Not losing the continuity of your life.**

For example, it creates a state in which you do not need to keep all of the following solely in your head:

* How far you had gotten with yesterday's work
* Who had replied to you
* What you were thinking several months ago
* Which article you had previously saved
* What you had intended to tell your doctor
* What you have been spending money on recently
* What your past test results were
* What you previously discussed with someone

In particular, it reduces the burden of having to begin with:

> "What was I doing again?"
>
> "Where did I save that again?"
>
> "Who was I supposed to reply to, and about what?"

---

# 3. Three Kinds of Information

Rensheng broadly divides information into three types.

## Personal Context

**Information about yourself.**

This is the center of Rensheng.

Examples:

* Health
* Money
* Relationships
* Work
* Education
* Housing
* Habits
* Schedule
* Past events
* Current state

Private by default.

---

## Knowledge

**What you know about the world.**

This is managed in a Digital Garden separate from the Life repository.

For example:

```text
garden/
├── OAuth.md
├── Agent Memory.md
├── Speech Acts.md
├── Rensheng.md
└── Katasu.md
```

Rensheng and the Garden may reference each other, but they do not share the same data model or directory tree.

Rensheng is about "yourself."

The Garden is about "the world."

---

## Captures

**Things you noticed and saved.**

These differ from both Knowledge and Personal Context.

For example:

* Twitter/X Bookmark
* YouTube Watch Later
* GitHub Star
* Browser Bookmark
* Pocket
* Readwise Highlight
* Screenshot
* Saved URL

The important point is:

> Merely capturing something does not make it Knowledge or an Interest.

For example, bookmarking a single cat video should not result in profiling you as:

> "A person who is interested in cats."

A Capture is simply stored as:

> **Something that drew your attention at that moment.**

---

# 4. Directory Structure

The current user-facing structure is:

```text
rensheng/
├── README.md
├── AGENTS.md
├── philosophy.md
├── goals.md
├── recent-updates.md
│
├── .agents/
│   └── skills/
│
├── profile/
│   ├── overview.md
│   ├── background.md
│   ├── communication.md
│   ├── work-patterns.md
│   └── preferences.md
│
├── people/
├── health/
├── money/
├── career/
├── education/
├── home/
├── routines/
├── recipes/
│
├── captures/
│   └── daily/
└── briefs/
    └── daily/
```

The repository may also contain agent configuration or maintenance files, but they are not part of the Rensheng information model.

---

# 5. Core Files

## `profile/`

Information about the person that remains relatively stable over long periods is split into focused files.

```text
profile/
├── overview.md
├── background.md
├── communication.md
├── work-patterns.md
└── preferences.md
```

For example:

* An overview of your personal history
* Values
* Preferences
* Things you struggle with
* Background you want AI to know

This is not a place where Rensheng automatically rewrites your identity.

The individual has final authority.

---

## `goals.md`

Goals the person has accepted and wants Rensheng to track.

For example:

* Long-term goals
* Short-term goals
* Things they want to do
* Things they do not want to do
* States they want to avoid

AI may propose a Goal or update its supporting evidence from behavioral history, but it must not silently turn an inference into an authoritative long-term Goal.

---

## `recent-updates.md`

A reverse-chronological changelog of how the Rensheng wiki and its Personal Context views were assembled or updated.

Together, `recent-updates.md` and `goals.md` serve the role that a single `now.md` might otherwise play:

* `recent-updates.md` explains what the wiki learned or changed
* `goals.md` explains what currently matters

This is a practical replacement for `now.md`, not a standalone current-state summary. An Agent reads both files first, then verifies the present state in the relevant profile or Domain files.

---

# 6. Personal Domains

Rensheng treats only areas that tend to be especially private and maintain ongoing state as first-class Domains.

## `people/`

Relationships.

```text
people/
├── alice.md
├── bob.md
└── ...
```

For example:

```markdown
# Alice

## Relationship

...

## Current context

...

## Recent

...

## Open loops

...
```

These can be updated with assistance from Beeper, email, Calendar, and similar sources.

---

## `health/`

Personal health context, such as:

* Test results
* Medical records
* Prescriptions
* Health checkups

The directory contains compiled Personal Context, not a general-purpose archive of original documents.

---

## `money/`

Personal financial context, such as:

* Accounts
* Income
* Subscriptions
* Spending patterns
* Financial obligations

---

## `career/`

Your current state regarding work and career.

For example:

* Employment history
* Current work
* Work style
* Career plans
* Interviews and meetings
* Offers
* Work-related concerns

Knowledge about the projects themselves belongs in the Garden.

---

## `education/`

* Enrollment information
* Grades
* Applications
* Educational path
* Coursework
* Learning progress

And similar information.

---

## `home/`

* Housing
* Moving
* Rent
* Facilities and equipment
* Repairs
* Utilities

And similar information.

---

## `routines/`

Procedures that support your daily life.

This is Personal Context, not Knowledge.

It can also be used for Daily Briefs and Reminders.

---

## `recipes/`

Personal cooking instructions that are used as part of daily life.

Recipes remain in Rensheng when they represent the person's own practical routine. General culinary knowledge belongs in the Garden.

---

# 7. Captures

```text
captures/
└── daily/
```

The existing files under `captures/daily/` are historical generated trend snapshots. They are retained as capture views, not treated as proof of durable interests or as Personal Context.

New personalized news outputs belong in `briefs/`. Items the person deliberately saves may then become Captures.

These Markdown files are views. Their linked sources remain the original evidence; a local canonical raw store is planned but not yet implemented.

For example:

```text
2026-09-19 17:30
X Bookmark
"Persistent memory for AI agents"
```

The important flow is:

```text
Capture
    ↓
Save
    ↓
Forget
```

The person does not need to remember it.

Later, an Agent can search the Markdown views and, when necessary, trace an item back to its source data. Rensheng does not require a dedicated CLI or MCP interface for this.

It is not automatically promoted to Knowledge.

It is written to the Garden only when the person decides:

> I want to preserve this as part of my own understanding.

---

# 8. Timeline

Timeline design is **TBD**.

There is currently no `timeline/` directory, and Agents must not assume one exists.

Until the model is decided, recent continuity is represented by `recent-updates.md`, while legacy dated trend snapshots remain under `captures/daily/`. Raw source history remains outside the Markdown views.

If a Timeline is introduced later, it should be a compiled chronology rather than a raw event dump.

---

# 9. Briefs

A Brief is not a place for storing facts, but an **Output that brings together the information you need at a particular moment**.

The current repository reserves a single root directory:

```text
briefs/
```

Subdirectories may be added only when actual Briefs require them.

The news itself is not Personal Context.

However, because it is an output selected using:

> your current interests and circumstances,

it belongs in Rensheng as a Brief.

The flow is:

```text
Public news
     +
Rensheng context
     ↓
Personalized News Brief
     ↓
briefs/
```

If you find a piece of news interesting and save it, it becomes:

```text
brief
 ↓
capture
```

If you then preserve it as part of your own understanding, it moves into the separate Garden:

```text
capture
 ↓
Garden
```

In other words, the flow is:

```text
News
 ↓ personalized
Brief
 ↓ save
Capture
 ↓ understand
Knowledge
```

---

# 10. Original Sources

Rensheng does not use a root `records/` directory.

Original files and raw data remain in their source systems or existing local locations. Compiled Markdown links back to that evidence when necessary instead of copying every original into the repository.

Preserve the original, but do not force it into a second directory hierarchy.

---

# 11. No Inbox

Rensheng does not use an `inbox/` directory.

New information should go directly to one of three places:

* Source-specific local storage for raw data
* `captures/daily/` for saved items
* The relevant compiled Personal Context or Brief

The user should not have to maintain a staging area or perform routine inbox cleanup.

---

# 12. Internal Storage (Planned)

Large volumes of raw data should not be stored in the Markdown repository.

The planned local storage layout is:

```text
~/.local/share/rensheng/
├── life.db
├── blobs/
├── indexes/
└── state/
```

For example, data such as:

* Beeper Messages
* X Bookmarks
* Calendar Events
* Bank Transactions
* Health Records
* GitHub Activity

would be stored in SQLite or as blobs.

The basic Record can remain simple.

```text
id
source
kind
occurred_at
observed_at
external_id
content
metadata
raw
```

Do not create an enormous shared schema.

---

# 13. Compilation Model

The heart of Rensheng is not Ingestion, but Compilation.

```text
Raw personal data
        ↓
Local archive
        ↓
Index
        ↓
Compiler
        ↓
Personal Context
```

For example, when the following accumulate:

```text
Beeper 180 messages
Calendar 7 events
Bank 12 transactions
X 8 bookmarks
```

The target compiler updates the following as needed:

```text
recent-updates.md
goals.md
profile/*.md
people/*.md
captures/daily/*.md
briefs/*.md
```

Generated artifacts are not the canonical truth, but regenerable views.

---

# 14. Save Broadly, Compile Selectively

Rensheng completely separates:

> how much is saved

from

> how much is always shown to AI.

For example, even if one million DMs are stored, the AI will ordinarily read only:

```text
recent-updates.md
goals.md
profile/overview.md
relevant person page
```

When needed, it can drill down through:

```text
relevant Domain
 ↓
captures / briefs
 ↓
source evidence
```

---

# 15. File-based Retrieval Model

Rensheng does not turn everything into Wiki pages in advance.

Retrieval happens by reading and searching the repository directly with the file tools an Agent already has. Rensheng does not implement a dedicated CLI or MCP server.

The basic path is:

```text
recent-updates.md + goals.md
              ↓
     profile / relevant Domain
              ↓
       captures / briefs
              ↓
         source evidence
```

This supports questions such as:

* "What did I talk about with A last year?"
* "What was I thinking about AI memory around 2025?"
* "Which things did I save and then forget?"
* "What was happening around September 19, 2026?"

## Interest Is a Query

Interest is not a folder, a permanent label, or a fixed Entity. It is an answer derived from evidence for a particular question and time window.

For an ADHD user, a system that depends on perfect PKM, stable PARA classification, exhaustive tagging, or regular review creates maintenance debt. Missing a review or filing something inconsistently must not make the system stop working.

Rensheng stores evidence first and derives interests only when they are needed. For example:

* What topics have repeatedly drawn attention in the last 30 days?
* Which saved items overlap with current Goals?
* What themes appear across recent updates, Captures, and work patterns?

A single Capture is evidence of attention at one moment, not proof of identity or durable Interest. Repeated evidence may support a provisional inference, while an explicit statement in `profile/preferences.md` remains authoritative.

PARA, topic pages, and interest lists may be generated as temporary Views when useful, but they are not canonical structures the user must maintain.

> **Interest is a query over history, not a filing obligation.**

---

# 16. Agents

Rensheng itself is not an Agent.

Hermes, Claude Code, Codex, ChatGPT, and others use Rensheng.

```text
              Rensheng Markdown repository
                         │
          ┌──────────────┼──────────────┐
          │              │              │
       Agents          Human      Existing file tools
          │
    ┌─────┼─────┐
    │     │     │
 Hermes Claude Codex
```

Do not lock a person's life inside an Agent's Memory.

---

# 17. Agent Skill

A Skill does not contain user information itself.

The only thing a Skill knows is:

> **How to navigate Rensheng.**

Basic exploration:

```text
Personal question
      ↓
recent-updates.md + goals.md
      ↓
profile / relevant Domain
      ↓
captures / briefs
      ↓
source evidence
```

For Knowledge, read the separate Garden repository. Rensheng does not expose it through a symlink, CLI, or MCP server.

---

# 18. Difference from Tool-only Agents

If Hermes is connected to tools such as:

* gws
* Beeper
* gh
* Browser
* Finance API

it can produce a Daily Brief.

However, every time, it still needs to:

```text
Read Calendar
Read Beeper
Read GitHub
Search the past
Reconstruct context
```

Rensheng continuously materializes this understanding.

```text
Life
 ↓ continuously
Rensheng
 ↓
compiled personal context
 ↓
Agent
```

This means an Agent does not need to understand the person again from scratch every time.

---

# 19. Onboarding

Onboarding should not hand the user an empty Vault.

For example:

```text
Choose local Life directory
       ↓
Connect Google Calendar / Contacts
       ↓
Import existing context
       ↓
Generate:
  profile draft
  goals
  recent updates
  people pages
       ↓
Show first Daily Brief
       ↓
Connect optional sources
  Beeper
  Health
  Money
  etc.
```

Do not require the user to design folders or classify information.

---

# 20. Product Boundary

Rensheng manages:

> **Private context about oneself.**

The Garden contains:

> What you know about the world.

Captures are:

> Things you noticed and saved.

Briefs are:

> Outputs generated for you at a particular point in time.

Timeline remains TBD and is not part of the current repository model.

Maintain these boundaries.

---

# 21. Final Architecture

```text
                    DIGITAL LIFE

       Google / Beeper / Health / Bank / X
            / GitHub / Browser / Files
                        │
                        ▼
             Local raw store (planned)
              SQLite + original files
                        │
                 Index / Search
                        │
                     Compiler
                        │
                        ▼
            Rensheng Markdown repository
                        │
                        ├── Current Context
                        │   ├── goals
                        │   ├── recent updates
                        │   └── profile
                        │
                        ├── Personal Domains
                        │   ├── people
                        │   ├── health
                        │   ├── money
                        │   ├── career
                        │   ├── education
                        │   ├── home
                        │   ├── routines
                        │   └── recipes
                        │
                        ├── Outputs
                        │   ├── captures
                        │   └── briefs
                        │
                        └── Direct readers
                            ├── Agents
                            └── Human
```

Agents and humans read the Markdown repository directly. There is no Rensheng-specific CLI or MCP layer.

The Knowledge Base exists independently in the Garden. It is not mounted into the Life repository.

---

# 22. Design Principles

When a Rensheng design decision is unclear, use the following principles.

**1. Prioritize private personal context**

Leave the world's Knowledge Base to a separate system.

**2. Do not assign meaning merely because something was captured**

A Bookmark can remain a Bookmark.

**3. Preserve the original**

AI-generated summaries can be regenerated.

**4. Generated Views must be disposable and reconstructible**

Do not treat compiled profile files, recent updates, or Briefs as canonical truth.

**5. Do not make AI read everything**

Start with a small context and go deeper only when necessary.

**6. Do not require the user to organize**

Rensheng bears the cost of organization.

**7. Remain independent of Agents**

A person's memory belongs to that person.

**8. Treat Interest as a Query**

Do not require perfect PKM, PARA upkeep, or exhaustive classification. Preserve evidence and derive relevant interests on demand.

---

# North Star

> **Simply living should cause your context to grow.**

The shortest definition of Rensheng is:

> **A local-first compiler for your private life context.**

The Japanese formulation translates to:

> **A local-first foundation that automatically compiles your life into a form that you and AI can retrace later.**

As an implementation principle:

> **Save broadly. Compile selectively. Organize minimally. Keep the original.**
