# Index maintenance

`index.md` is a navigation map: relative page links and short descriptions, grouped by life domain. An Agent maintains the descriptions after reading the pages. The helper only compares bytes and records an explicit navigation review; it does not infer facts or generate summaries.

This follows [Karpathy's LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f#indexing-and-logging): a maintained index plus a dated operation log. Rensheng uses `recent-updates.md` for meaningful compilation changes. The hash receipts and timestamp meanings below are Rensheng conventions, not requirements from the original LLM Wiki proposal.

## Files

| File | Responsibility |
| --- | --- |
| `index.md` | Human- and Agent-readable navigation; no duplicated personal state |
| `index-state.json` | Machine-written hashes binding each reviewed index entry to a version of its page |
| `recent-updates.md` | Why the compiled context changed, newest first; not a raw event log |

Use this entry format, with an em dash and a nonempty one-line description:

```markdown
- [Subscriptions](money/subscriptions.md) — Subscription terms, renewal status, and access end dates.
```

This is a formatting example; add it only when that page exists. Percent-encode spaces and parentheses in link targets. Descriptions should help choose a page, rather than copy its balances, commitments, or other changing facts. Keep individual entries at the start of the line. Headings and introductory prose are free-form; their edits do not invalidate page receipts.

The helper covers `goals.md`, `recent-updates.md`, and Markdown pages under the life domains, `captures/`, and `briefs/`. It excludes `README.md`, `index.md`, hidden paths, symlinks, instructions, skills, and scripts. Do not add excluded files as page entries. Use ordinary prose links for guide navigation. A new personal domain requires an explicit update to the helper's `DOMAINS` list.

## Timestamp meanings

| Field | Meaning | Update rule |
| --- | --- | --- |
| `updated_at` | When the page content was edited | Agent records a timezone-bearing timestamp when creating or changing a personal page; unchanged runs leave it alone |
| `verified_at` | When specified facts were checked against evidence | Record beside the relevant claim or section, with its source; do not advance it just because wording or an index changed |
| `indexed_at` | When a page version and its index description were acknowledged together | Written by the helper in UTC; it says nothing about whether external facts remain true |

For new or edited personal pages, use optional YAML frontmatter for the page timestamp, preserving other existing metadata:

```yaml
---
updated_at: "2026-01-15T18:30:00+09:00"
---
```

The value above is illustrative. Use the actual edit time; never infer it from an event date, checkout time, or filesystem mtime. Legacy pages and empty starter placeholders remain readable without it. `recent-updates.md` uses its existing dated change entries; index-only maintenance does not create a changelog entry. Keep event/effective dates separate from verification and editing dates. A section's existing `Verified as of:` label is also valid; use a whole-page verification date only after checking the whole claimed scope.

## Check, review, record

Requires Python 3.10+ and its standard library only. From the instance root:

```console
python3 scripts/index.py check
```

`check` is read-only and prints JSON. Exit codes: **0** = navigation receipts match; **1** = review needed; **2** = invalid input or an I/O error. It reports:

- `unlisted`: existing pages without index entries.
- `missing`: index entries pointing to absent or excluded pages.
- `pending`: unreviewed entries, changed page bytes, or changed entry text; includes both current hashes.
- `orphaned`: stored receipts whose entries were removed.

After an authorized page update:

1. Finish the actual page edits and any meaningful `recent-updates.md` entry.
2. Read the affected pages. Add or correct their index descriptions; remove links to deleted pages.
3. Run `check`. Use the hashes for the page and entry versions you have reviewed, and record each affected entry:

```console
python3 scripts/index.py record money/subscriptions.md --sha256 PAGE_HASH --entry-sha256 ENTRY_HASH
```

`PAGE_HASH` and `ENTRY_HASH` are placeholders for the full values returned by `check`. The command refuses different input versions. If the text changes, review it again before recording. An unchanged receipt is a no-op, including its timestamp. The helper writes only `index-state.json`, using atomic file replacement. Run write commands sequentially.

For a deleted or renamed page, remove its old index entry, then discard only the obsolete receipt:

```console
python3 scripts/index.py prune people/old-name.md
```

Pruning refuses a page still present in either the indexed file set or the index. Add and review the new path separately after a rename. Finish with `check`; report any remaining gaps rather than marking unrelated pages reviewed. A partial backfill need only review its in-scope changes.

The root defaults to the parent of `scripts/`, so the helper also works when called from another directory. Use `--root /path/to/private-instance` before the command to target another instance explicitly. If the helper is unavailable, update navigation as authorized and report hash checking as pending. Never invent hashes or verification timestamps.

## What the hashes mean

Each receipt stores a SHA-256 of the complete page bytes and a SHA-256 of the exact UTF-8 index entry line, excluding its line ending. This detects both page edits and independent description edits. A mismatch asks for review; it does not prove the description is wrong. Even whitespace or a timestamp edit can change the page hash.

`record` acknowledges the Agent's or person's review. The helper cannot check semantic correctness or whether an external source has changed. An unchanged hash is not proof of fresh real-world information. Git still provides version history; the receipt records which version the index description was checked against, including uncommitted content.

The state file is disposable. If it is lost, `check` marks entries unreviewed; rebuilding requires reading the affected pages and recording their current descriptions. Do not recreate receipts by blindly accepting every current hash. The template's initial receipts cover only its empty starter pages and navigation descriptions.

## Local checks

```console
python3 -m unittest discover -s scripts/tests -v
```
