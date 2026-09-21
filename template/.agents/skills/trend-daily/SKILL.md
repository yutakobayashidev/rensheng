---
name: trend-daily
description: Collect daily public technology trends and create a personalized Markdown Brief using the Rensheng profile, accepted Goals, and recent context. Use when the user asks for today's trends, a daily technology digest, relevant news, or an interest-aware news Brief.
---

# Daily Trend Brief

Create a source-backed daily technology Brief without turning one day's attention into a permanent Interest.

## Context

Read these files when present:

1. `profile/preferences.md` for explicit interests and exclusions.
2. `goals.md` for accepted Goals.
3. `recent-updates.md` and `profile/work-patterns.md` for time-sensitive context.

Treat missing files as empty. Do not invent a profile. Explicit preferences are authoritative; inferred interests are provisional and scoped to this Brief.

## Sources

Collect current entries from primary feeds or APIs:

- Hatena Bookmark IT official RSS: `https://b.hatena.ne.jp/hotentry/it.rss`
- Hacker News official API: `https://hacker-news.firebaseio.com/v0/topstories.json`
- GitHub Trending: `https://github.com/trending`

Use the available URL-fetching tools. Prefer official feeds and APIs over scraping. Preserve the original article URL for Hatena entries and the Hacker News discussion URL for Hacker News entries.

## Selection

Rank entries using both public attention and current relevance:

- Match explicit preferences and accepted Goals first.
- Use recent context only as a temporary signal.
- Keep high-impact items that challenge or broaden the existing profile.
- Do not claim that a single viewed or saved item establishes a durable Interest.

Explain each selected item's relevance in one sentence. Keep uncertainty visible when the match is inferred.

## Output

Save the result to `briefs/daily/YYYY-MM-DD.md` in the active Rensheng repository.

Use this structure:

```markdown
# Daily Trend Brief: YYYY-MM-DD

## Top picks

| Item | Signal | Relevance | Why now |
|------|--------|-----------|---------|
| [Title](URL) | score | High / Medium / Exploratory | One-sentence reason |

## Hatena Bookmark IT

1. [Title](original article URL) — bookmark count — summary

## Hacker News

1. [Japanese title](HN discussion URL) — points — summary

## GitHub Trending

1. [owner/repository](repository URL) — language and stars today — summary

## Interest queries

- Repeated themes in the recent evidence
- Connections to accepted Goals
- Exploratory topics that should not yet become profile facts
```

Translate Hacker News titles into the user's primary language while preserving product and project names.

## Safety and maintenance

- Include a working URL for every item.
- Do not write source credentials, cookies, or raw private messages into the Brief.
- Do not modify `profile/preferences.md` or `goals.md` automatically.
- Keep the report reproducible by naming its public sources and date.
