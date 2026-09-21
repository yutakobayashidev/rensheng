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

## Personal repository template

[`template/`](template/) is an anonymous starter for a private Rensheng repository. It contains no personal data and provides only:

- `philosophy.md` — Rensheng's boundaries and design principles
- `profile/`, `goals.md`, and `recent-updates.md` — the minimal Personal Context structure
- `people/`, `health/`, `money/`, and other directories — Domain guides with file conventions and fictional examples; create personal pages only when there is information to record
- `index.md`, `index-state.json`, and [`scripts/index.py`](template/scripts/README.md) — navigation and an optional Python helper for detecting changed pages or descriptions; timestamp conventions distinguish editing, evidence checks, and index reviews
- `.agents/skills/` — reusable Skills for Agents that work with Rensheng

Copy it into a new private repository:

```console
mkdir -p /path/to/private-rensheng
cp -a template/. /path/to/private-rensheng/
```

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
