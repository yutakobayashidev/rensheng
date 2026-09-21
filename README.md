# Rensheng

Rensheng is a local-first foundation that keeps your private life context under your control and continuously compiles it into small Markdown files that both you and AI can retrace later.

Read [Rensheng in Context](COMPARISON.md) for comparison matrices with Karpathy's LLM Wiki, Obsidian, and Notion, historical context from Memex and MyLifeBits, and the distinction between the current implementation and intended behavior.

## Personal repository template

[`template/`](template/) is an anonymous starter for a private Rensheng repository. It contains no personal data and provides only:

- `philosophy.md` — Rensheng's boundaries and design principles
- `profile/`, `goals.md`, and `recent-updates.md` — the minimal Personal Context structure
- `people/`, `health/`, `money/`, and other directories — Domain guides with file conventions and fictional examples; create personal pages only when there is information to record
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
