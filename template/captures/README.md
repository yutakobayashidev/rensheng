# Captures

Items the user deliberately saved and may want to find again. A saved item is evidence of attention at that moment, not an accepted Goal, stable preference, or piece of Knowledge.

## Files

New daily views may use `daily/YYYY-MM-DD.md`. Each entry preserves enough information to find its source again: saved time when known, title or short description, source, and original link or ID.

Existing `daily/YYYYMMDD-trend.md` files, if present in a private instance, are historical generated snapshots. Retain them as legacy views. New personalized news outputs belong in [briefs/](../briefs/README.md); only items deliberately saved by the user become new Captures. There is no need to rename existing files in bulk.

## Example: daily/2026-01-15.md

Fictional example, not an item saved by the repository owner:

```markdown
# Captures — 2026-01-15

## 17:30 +09:00 — Example article

- Saved at: 2026-01-15T17:30:00+09:00.
- Source: browser bookmark.
- URL: https://example.invalid/articles/example.
- Source ID: bookmark-example-123.
- User note: "Keep this for the next discussion."
```

## Updating

Follow [the shared update rules](../AGENTS.md). Record the saved time separately from publication time; do not invent a missing timestamp. Retain an original ID when available and use source identity to avoid adding the same saved event again on re-import. Include user notes only when the user actually wrote them.

These are searchable views with references to evidence, not a new canonical archive. Do not infer why something was saved, add mandatory tags, or promote it into the Garden without the user's decision.
