# Set up Rensheng with an Agent

This guide is for an Agent helping a person initialize a private Rensheng instance. First create or locate the private repository, then connect the chosen sources, set the output language in the instance's `AGENTS.md`, and run `rensheng-backfill`.

Work with the capabilities of the current host. Setup does not require OpenBrief, a Rensheng server, or a new connector service.

## For the person

Paste this into your Agent:

```text
Set up my private Rensheng repository by following this guide:
https://raw.githubusercontent.com/yutakobayashidev/rensheng/main/docs/setup.md
```

You can include your existing private repository or directory, preferred output language, and sources to use. Otherwise, the Agent will ask for the missing choices. Complete account sign-in in the host's supported interface when prompted.

## For the Agent

Read the complete guide, then carry out the setup. Reuse choices and authorization already supplied; do not ask the person to repeat them. Group missing choices into one short question where possible: destination, sources, and output language. Authentication may require a separate interaction.

### 0. Create or locate the private repository

- Discover the current host's available file, repository, integration, and skill capabilities. A named or recommended plugin is not proof that it is installed, connected, or callable.
- Use an existing instance when supplied. Read its applicable `AGENTS.md`, `README.md`, `philosophy.md`, and backfill skill before editing. Preserve local instructions, personal content, and unrelated changes.
- For a new instance, obtain [`template/`](../template/) from one inspected revision of this repository and record that revision in the setup report. Copy the complete template, including its Agent skills and index helper, into a new private destination. Do not copy the development repository or populate its public `template/` with personal data.
- Inspect the destination before copying. Never overlay an existing instance with the starter files. If setup is being resumed, inspect what succeeded and continue only the missing steps. Add a missing guide or skill only when needed, without replacing existing configuration.
- Verify privacy before writing to a remote destination. If the host cannot write there, offer a private draft bundle through its supported file-delivery workflow, retaining relative paths. Make clear that it has not been applied. If no private destination or delivery route is available, resolve that before retrieving personal records.
- Read the current instance's `rensheng-backfill/SKILL.md` and its referenced files in full. A new copy contains them under `.agents/skills/`. If a host needs explicit skill registration, use its supported mechanism. Otherwise, read and follow the files directly; do not claim native skill installation or automatic discovery without checking it. A previously installed copy must not override newer instructions in this instance.

#### New local instance: clone, copy, and initialize

When Bash, Git, and standard file tools are available, run the following after resolving the person's destination. Replace `/absolute/path/to/private-rensheng` with that absolute path, properly shell-quoted. Choose a private local directory outside the public development checkout and other Git worktrees. This command creates a **new** directory; it refuses any existing path, including an empty directory or a symlink. Inspect and reuse existing instances instead of rerunning the copy over them.

```bash
(
  set -eu
  umask 077
  rensheng_dir='/absolute/path/to/private-rensheng'

  case "$rensheng_dir" in
    /*) ;;
    *) printf '%s\n' 'Use an absolute destination path.' >&2; exit 1 ;;
  esac
  if [ -e "$rensheng_dir" ] || [ -L "$rensheng_dir" ]; then
    printf '%s\n' 'Destination exists; inspect and reuse it without copying over it.' >&2
    exit 1
  fi

  rensheng_tmp="$(mktemp -d)"
  trap 'rm -rf -- "$rensheng_tmp"' EXIT
  git clone --depth 1 --single-branch --branch main \
    https://github.com/yutakobayashidev/rensheng.git "$rensheng_tmp/source"
  rensheng_revision="$(git -C "$rensheng_tmp/source" rev-parse HEAD)"

  mkdir -p -- "$(dirname -- "$rensheng_dir")"
  mkdir -- "$rensheng_dir"
  cp -R "$rensheng_tmp/source/template/." "$rensheng_dir/"
  git -C "$rensheng_dir" init -b main

  printf 'Template revision: %s\nPrivate destination: %s\n' "$rensheng_revision" "$rensheng_dir"
  git -C "$rensheng_dir" status --short
  git -C "$rensheng_dir" remote -v
)
```

The temporary clone is removed on exit. Only the contents of `template/`, including `.agents/` and other dotfiles, are copied. The new `.git` belongs to the personal instance: the public repository's history and `origin` are not inherited. No commit, remote repository, or push is created by these commands.

Before continuing, verify that `AGENTS.md`, `philosophy.md`, `profile/`, and `.agents/skills/rensheng-backfill/SKILL.md` exist at the destination root. The new repository should have no commits or remotes; its template files are initially untracked. Read the copied instructions and retain the printed template revision for the completion report. If a command failed after creating the destination, inspect the partial result and resume only missing work; do not delete it or blindly repeat the copy.

#### Existing instance or no shell

For an existing instance, read its instructions and inspect its working tree and remotes when possible. Keep its Git history, configuration, and personal files; skip the new-instance commands and proceed to source setup.

If the host has repository/file tools but no shell, resolve one source commit, enumerate all files beneath `template/`, and copy their contents from that same revision into the verified private destination, removing only the leading `template/` path. Include dotfiles and nested skill references, and check for existing destination files before writing. Use supported repository tools to initialize an independent private repository only when that action is authorized and available. Do not copy the public repository's history or configure it as the personal instance's remote.

If only private file delivery is available, deliver the same directory layout as a draft bundle and report Git initialization as not performed. In every route, verify successful writes before continuing; a draft bundle is not an applied repository setup.

### 1. Connect the chosen sources

Use the sources the person selected. If none were specified, offer the services they actually use; Gmail, Calendar, and Beeper are examples, not mandatory dependencies.

| Source | Useful initial context | Connection to look for |
| --- | --- | --- |
| Gmail or another mail service | Introductions, agreements, and relevant follow-ups | The host's supported mail app, connector, or configured tool |
| Google Calendar or another calendar | Upcoming plans and ongoing commitments | The host's supported calendar integration |
| Beeper or another messaging service | Direct interactions, relationship context, and open loops | An available messaging plugin, MCP tool, or configured CLI |
| User-supplied files or notes | Explicit background, preferences, and accepted goals | A private file-reading capability |

Discover integrations by capability instead of assuming product names, package names, or tool schemas. For ChatGPT, Hermes Agent, or another host, use its available integration management tools and current official setup instructions. Do not assume the same integration exists on every host. Install or enable the selected integrations through supported mechanisms when authorized; reuse working connections. Account sign-in and consent must use the host's supported flow. Never ask the person to paste passwords or tokens into the repository or conversation.

For each chosen source, distinguish installed, connected, and verified readable. Confirm access with a small read-only request when authorized. A successful empty response can verify access without establishing that useful records exist. Do not send messages, change calendar events, or modify source data as a connection test.

Report each source as ready, needing user authentication, unavailable, or skipped. If one source is unavailable or declined, continue with the usable subset. If none is usable, request a supplied note/file or leave setup partial; do not manufacture a backfill or claim completion. Do not build a replacement connector or perform a full-history export.

Integration setup happens here. The backfill skill intentionally consumes already available sources and does not install tools or connect accounts itself.

### 2. Set the output language in AGENTS.md

For an existing instance, honor its configured language unless the person requests a change. For a newly copied template, confirm the person's choice once; the starter's Japanese default is not evidence of their preference. An explicit choice already given in this conversation is sufficient. The conversation language can inform a suggestion, but is not itself confirmation.

Update only the `Output language` section of the private instance's `AGENTS.md`, or add it if absent. Record the confirmed language name and, when known, its language code. Apply it to user-facing responses and newly generated or substantially revised Personal Context, including headings, changelog prose, and index descriptions. Preserve the repository's filenames, metadata keys, source identifiers, quotations, proper nouns, and authored wording; do not translate unchanged pages just for consistency.

For example, **only after English was chosen**:

```markdown
## Output language

- Expected output language: English (`en`).
- Respond to the user and write new or substantially revised Personal Context in English unless the user explicitly requests another language.
- Preserve existing wording, quotations, proper nouns, source titles, and technical terms when translation would reduce fidelity. Do not translate unchanged pages only for consistency.
```

Read the section back before starting the backfill. A repository output setting does not establish a broader personal communication preference; do not also add it to `profile/communication.md` unless the person said that is what they want.

### 3. Run rensheng-backfill

Invoke or follow the instance's [`rensheng-backfill`](../template/.agents/skills/rensheng-backfill/SKILL.md), using the private destination, confirmed output language, and sources verified above. Follow its workflow and referenced evidence rules rather than replacing them with a generic import.

- Reuse existing source choices and consent. The setup request authorizes the skill's in-scope changes to the resolved private destination; ask only for consequential missing decisions.
- Initialize or update `profile/*.md`, relevant `people/*.md`, `goals.md`, and `recent-updates.md`. Maintain `index.md` and `index-state.json` for affected pages under the instance's rules. Other personal Domains are outside this initial backfill.
- Use the skill's bounded search windows and stopping rules. Its current defaults are 90 days for interactions, 30 days for recent changes, and the next 30 days for calendar context, with selective older searches. Report actual coverage, gaps, and a continuation point.
- Preserve evidence references, uncertainty, existing prose, and distinct identities. Import an active Goal only when the person accepted it and wanted Rensheng to track it; otherwise leave it as a conversational candidate. An empty `goals.md` can be a valid result.
- Follow the skill's verification and index-maintenance steps. Do not invent hashes when the helper cannot run. Repeated setup must not duplicate facts, people pages, goals, or changelog entries.

Proceed through the authorized steps without asking for a second generic approval to run the backfill. Leave unresolved facts deferred. Creating a new remote repository or committing/pushing a personal instance still requires authorization covering that action; reuse it when already given. Do not schedule recurring updates as part of initial setup.

## Completion report

Report briefly in the chosen language:

- The private destination, whether files were applied or only drafted, and the template revision used for a new instance.
- The output language recorded in `AGENTS.md`.
- Which sources were verified readable, actually searched, unavailable, or skipped, with date coverage.
- Files changed, index-check status, and deferred goal candidates or other essential follow-ups.

Distinguish a completed bounded backfill from a partial setup. If the person returns after authentication or with another source, reread the instance and resume the missing work. Never report an installation, connection, write, or source search as successful without checking its result.
