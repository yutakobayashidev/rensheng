#!/usr/bin/env python3
"""Check navigation freshness and record explicit index reviews. Python 3.10+."""

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit


DOMAINS = (
    "profile", "people", "health", "money", "career", "education", "home",
    "routines", "recipes", "captures", "briefs",
)
ROOT_PAGES = ("goals.md", "recent-updates.md")
STATE = "index-state.json"
ENTRY = re.compile(r"^- \[([^\]]+)\]\(([^)]+)\) — (\S.*)$")
HASH = re.compile(r"[0-9a-f]{64}")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def page_path(value):
    path = PurePosixPath(value)
    if (
        not value or path.is_absolute() or str(path) != value
        or "\\" in value or any(p.startswith(".") for p in path.parts)
        or path.suffix != ".md" or path.name.lower() in ("readme.md", "index.md")
        or not (value in ROOT_PAGES or (len(path.parts) > 1 and path.parts[0] in DOMAINS))
    ):
        raise ValueError(f"Not an indexable page path: {value!r}")
    return value


def local_bytes(root, name):
    path = root / name
    if path.is_symlink():
        raise ValueError(f"Refusing a symlink: {name}")
    return path.read_bytes()


def pages(root):
    result = {}
    for name in ROOT_PAGES:
        path = root / name
        if path.is_file() and not path.is_symlink():
            result[name] = digest(path.read_bytes())
    for domain in DOMAINS:
        start = root / domain
        if start.is_symlink() or not start.is_dir():
            continue
        for directory, dirs, files in os.walk(start, followlinks=False):
            dirs[:] = sorted(d for d in dirs if not d.startswith(".") and not (Path(directory) / d).is_symlink())
            for filename in sorted(files):
                path = Path(directory) / filename
                if path.is_symlink() or not path.is_file():
                    continue
                name = path.relative_to(root).as_posix()
                try:
                    page_path(name)
                except ValueError:
                    continue
                result[name] = digest(path.read_bytes())
    return result


def entries(root):
    result = {}
    in_fence = False
    for number, line in enumerate(local_bytes(root, "index.md").decode("utf-8").splitlines(), 1):
        if line.startswith("```"):
            in_fence = not in_fence
        if in_fence or not line.startswith("- ["):
            continue
        match = ENTRY.fullmatch(line)
        if not match:
            raise ValueError(f"index.md:{number}: use '- [Title](path.md) — one-line description'")
        target = urlsplit(match[2])
        if target.scheme or target.netloc or target.query or target.fragment:
            raise ValueError(f"index.md:{number}: use a relative page path without query or fragment")
        name = page_path(unquote(target.path, errors="strict"))
        if name in result:
            raise ValueError(f"index.md:{number}: duplicate entry for {name}")
        result[name] = digest(line.encode("utf-8"))
    return result


def read_state(root):
    if not (root / STATE).exists() and not (root / STATE).is_symlink():
        return {"version": 1, "pages": {}}
    state = json.loads(local_bytes(root, STATE))
    if not isinstance(state, dict) or state.get("version") != 1 or not isinstance(state.get("pages"), dict):
        raise ValueError("index-state.json must contain version 1 and a pages object")
    for name, entry in state["pages"].items():
        page_path(name)
        if not isinstance(entry, dict) or any(
            not isinstance(entry.get(key), str) or not HASH.fullmatch(entry[key])
            for key in ("sha256", "entry_sha256")
        ):
            raise ValueError(f"Invalid stored hashes for {name}")
        stamp = entry.get("indexed_at")
        if not isinstance(stamp, str) or datetime.fromisoformat(stamp.replace("Z", "+00:00")).utcoffset() is None:
            raise ValueError(f"indexed_at needs a timezone for {name}")
    return state


def write_state(root, state):
    data = (json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    target = root / STATE
    if target.is_symlink():
        raise ValueError(f"Refusing a symlink: {STATE}")
    if target.exists() and target.read_bytes() == data:
        return
    fd, temporary = tempfile.mkstemp(prefix=".index-state-", suffix=".tmp", dir=root)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
        os.replace(temporary, target)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def status(current, index, state):
    pending = []
    for name in sorted(current.keys() & index.keys()):
        old = state["pages"].get(name)
        reasons = []
        if old is None:
            reasons.append("unreviewed")
        else:
            if old["sha256"] != current[name]:
                reasons.append("page_changed")
            if old["entry_sha256"] != index[name]:
                reasons.append("entry_changed")
        if reasons:
            pending.append({"path": name, "reasons": reasons, "sha256": current[name], "entry_sha256": index[name]})
    return {
        "unlisted": sorted(current.keys() - index.keys()),
        "missing": sorted(index.keys() - current.keys()),
        "orphaned": sorted(state["pages"].keys() - index.keys()),
        "pending": pending,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent,
                        help="private instance root; defaults to the directory containing scripts/")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("check", help="read-only JSON report; exit 1 means navigation needs review")
    record = commands.add_parser("record", help="record one index entry after reviewing its page and description")
    record.add_argument("path")
    record.add_argument("--sha256", required=True, help="page hash from check, for the version reviewed")
    record.add_argument("--entry-sha256", required=True, help="index entry hash from check, for the entry reviewed")
    prune = commands.add_parser("prune", help="remove state for a page absent from both disk and index")
    prune.add_argument("path")
    args = parser.parse_args(argv)
    try:
        root = args.root.resolve(strict=True)
        if not all((root / name).is_file() for name in ("AGENTS.md", "philosophy.md", "index.md")):
            raise ValueError("Root must contain AGENTS.md, philosophy.md, and index.md")
        current, index, state = pages(root), entries(root), read_state(root)
        if args.command == "check":
            report = status(current, index, state)
            print(json.dumps(report, ensure_ascii=False, indent=2))
            return int(any(report.values()))
        name = page_path(args.path)
        if args.command == "record":
            if name not in current or name not in index:
                raise ValueError("The page and its index entry must both exist")
            if current[name] != args.sha256 or index[name] != args.entry_sha256:
                raise ValueError("Page or index entry changed; review the current versions before recording")
            old = state["pages"].get(name, {})
            if old.get("sha256") == current[name] and old.get("entry_sha256") == index[name]:
                print(json.dumps({"recorded": name, "changed": False}))
                return 0
            # Recheck the input versions immediately before recording; later edits remain detectable.
            if pages(root).get(name) != args.sha256 or entries(root).get(name) != args.entry_sha256:
                raise ValueError("Inputs changed during recording; retry after review")
            state["pages"][name] = {
                "sha256": args.sha256, "entry_sha256": args.entry_sha256,
                "indexed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            }
        else:
            if name in current or name in index:
                raise ValueError("Remove the page and its index entry before pruning its state")
            state["pages"].pop(name, None)
        write_state(root, state)
        print(json.dumps({"recorded" if args.command == "record" else "pruned": name, "changed": True}))
        return 0
    except (OSError, ValueError) as error:
        print(f"index: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
