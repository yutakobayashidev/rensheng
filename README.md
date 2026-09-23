# Rensheng

Rensheng is a local-first foundation for keeping private life context under your control. It defines how external Agents compile that context into small Markdown files that both you and AI can read and trace back to their sources.

## Problems Rensheng addresses

### Keeping records becomes another job

Copying messages, receipts, and documents into another app creates a second collection to classify, reconcile, and maintain. Rensheng leaves originals in their source systems or existing local stores, and asks external Agents to maintain small, relevant views of your current situation. The aim is less total upkeep, including the effort of reviewing and correcting generated summaries.

### Observed behavior gets mistaken for personal intent

What you do, save, or read does not automatically define what you want or who you are. Rensheng keeps observations, AI interpretations, and your explicit decisions distinct. Goals become authoritative only when you accept them and want them tracked; your statements and corrections must survive later updates.

### Plausible summaries become unchecked facts

A fluent summary can hide an unsupported inference, an outdated fact, or a gap in the evidence. Rensheng separates personal facts from general knowledge and requires source references and verification dates where relevant. Agents can then check the evidence behind a claim and preserve uncertainty where it is unresolved. Traceability supports verification; it does not guarantee correctness or freshness.

### Changing tools means rebuilding your context

When personal context lives only inside one app or Agent's memory, switching tools can mean explaining your life again. Rensheng keeps that context in ordinary Markdown files with explicit conventions, readable by people and different Agents. You can carry the files forward independently of any single provider; access to original sources and connector permissions still needs to be maintained separately.

These principles guide the repository template and Agent workflows. Rensheng itself does not perform inference or run a continuous update service; external Agents handle that work.

Read [Rensheng in Context](COMPARISON.md) for comparison matrices with Karpathy's LLM Wiki, Obsidian, and Notion, historical context from Memex and MyLifeBits, and the distinction between the current implementation and intended behavior.

## Set up with an Agent

Paste this into ChatGPT, Hermes Agent, Codex, or another Agent:

```text
Set up my private Rensheng repository by following this guide:
https://raw.githubusercontent.com/yutakobayashidev/rensheng/main/docs/setup.md
```

The Agent will first create a private instance from `template/` or reuse your existing repository, then help you connect sources such as Gmail, Calendar, and Beeper, confirm the output language in your private `AGENTS.md`, and run `rensheng-backfill`. Existing connections and settings are reused. You only need to supply missing choices and complete any required sign-in or permission steps.

Read the [setup guide](docs/setup.md) for the full workflow. Available integrations and file-writing capabilities depend on your Agent environment; setup can start with a subset of sources or produce a private draft when direct writes are unavailable.

## Personal repository template

[`template/`](template/) is an anonymous starter for a private Rensheng repository. It contains no personal data and provides only:

- `philosophy.md` — Rensheng's boundaries and design principles
- `profile/`, `goals.md`, and `recent-updates.md` — the minimal Personal Context structure
- `people/`, `health/`, `money/`, and other directories — Domain guides with file conventions and fictional examples; `records/` keeps explicitly retained raw snapshots separate from compiled context
- `index.md`, `index-state.json`, and [`scripts/`](template/scripts/README.md) — navigation maintenance plus an optional resumable X following exporter and TSV converter; the template contains no account identifiers or exported data
- `.agents/skills/` — reusable Skills for Agents that work with Rensheng

Follow [Step 0 of the setup guide](docs/setup.md#0-create-or-locate-the-private-repository) for commands to clone this repository temporarily, copy only `template/` into a new private directory, and initialize independent Git history. The commands refuse existing destinations and do not carry over the public repository's `origin`. Existing private instances are reused without copying the template over them.

Keep the destination private. Do not commit personal data such as profile, health, financial, or relationship information to this public repository.

## Building Blocks

Tools that can provide source data for captures:

| Tool | Interface | Capture source |
| --- | --- | --- |
| [OpenBrief](docs/openbrief.md) | Daemon, CLI, and desktop app | Foreground app metadata and observations |
| [Bird](https://git.yutakobayashi.com/yuta/bird) | CLI | X/Twitter |
| [twitter-api-safe](https://github.com/fa0311/twitter_api_safe_relay) | API relay | X/Twitter |
| [Grafana](https://grafana.com/) | Dashboards and API | Vitals and environment |
| [Beeper](https://www.beeper.com/) | Messaging app | Messages |
| [Oura Ring](https://ouraring.com/) | Wearable and app | Sleep, readiness, activity, and health metrics |
| [Mnie](https://github.com/pnsk-lab/mnie) | App, API, MCP, and CLI | Financial data |
