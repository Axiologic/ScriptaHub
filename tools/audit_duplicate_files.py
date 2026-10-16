#!/usr/bin/env python3
"""Report byte-identical files without deleting or rewriting anything.

Files are grouped by size before SHA-256 hashing. Hard links are counted as
multiple paths to one physical file, so they do not inflate the space estimate.
The estimate is an upper bound, not a cleanup recommendation: published editions
and their historical downloads must remain available.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
import fnmatch
import hashlib
import json
import os
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def collect(root: Path, excluded: list[str], include_git: bool) -> tuple[list[dict], dict]:
    by_size: dict[int, list[tuple[str, tuple[int, int]]]] = defaultdict(list)
    counts = {"files": 0, "symlinks_skipped": 0, "unreadable": [], "logical_bytes": 0}
    for directory, dirs, files in os.walk(root, followlinks=False):
        parent = Path(directory)
        dirs[:] = sorted(name for name in dirs if (include_git or name != ".git")
                         and not any(fnmatch.fnmatch((parent / name).relative_to(root).as_posix(), pattern) for pattern in excluded)
                         and not (parent / name).is_symlink())
        for name in sorted(files):
            path = parent / name
            relative = path.relative_to(root).as_posix()
            if any(fnmatch.fnmatch(relative, pattern) for pattern in excluded):
                continue
            if path.is_symlink():
                counts["symlinks_skipped"] += 1
                continue
            try:
                stat = path.stat()
            except OSError as error:
                counts["unreadable"].append({"path": relative, "error": str(error)})
                continue
            if not path.is_file():
                continue
            counts["files"] += 1
            counts["logical_bytes"] += stat.st_size
            by_size[stat.st_size].append((relative, (stat.st_dev, stat.st_ino)))

    groups = []
    hashed_inodes: dict[tuple[int, int], str] = {}
    for size, candidates in sorted(by_size.items(), reverse=True):
        if len(candidates) < 2:
            continue
        by_hash: dict[str, list[tuple[str, tuple[int, int]]]] = defaultdict(list)
        for relative, inode in candidates:
            try:
                if inode not in hashed_inodes:
                    hashed_inodes[inode] = sha256(root / relative)
                by_hash[hashed_inodes[inode]].append((relative, inode))
            except OSError as error:
                counts["unreadable"].append({"path": relative, "error": str(error)})
        for digest, members in by_hash.items():
            if len(members) < 2:
                continue
            paths = sorted(relative for relative, _ in members)
            physical = len({inode for _, inode in members})
            groups.append({"sha256": digest, "bytes_each": size, "paths": paths,
                           "path_count": len(paths), "physical_copies": physical,
                           "hardlink_aliases": len(paths) - physical,
                           "extra_physical_bytes_upper_bound": max(0, physical - 1) * size})
    groups.sort(key=lambda group: (-group["extra_physical_bytes_upper_bound"], -group["bytes_each"], group["sha256"]))
    counts.update(duplicate_groups=len(groups), duplicate_paths=sum(group["path_count"] for group in groups),
                  hardlink_aliases=sum(group["hardlink_aliases"] for group in groups),
                  extra_physical_bytes_upper_bound=sum(group["extra_physical_bytes_upper_bound"] for group in groups))
    return groups, counts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--exclude", action="append", default=[], metavar="GLOB", help="Exclude a relative path glob; repeatable")
    parser.add_argument("--include-git", action="store_true", help="Include the .git object store")
    parser.add_argument("--json-out", type=Path, help="Write all groups and summary as JSON")
    parser.add_argument("--top", type=int, default=20, help="Number of largest groups shown in the terminal")
    args = parser.parse_args()
    root = args.root.resolve()
    groups, summary = collect(root, args.exclude, args.include_git)
    result = {"root": str(root), "method": "exact file bytes, SHA-256; symlinks and .git skipped by default",
              "summary": summary, "groups": groups}
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    for group in groups[:max(0, args.top)]:
        print(f"\n{group['extra_physical_bytes_upper_bound']:,} extra bytes (upper bound); "
              f"{group['bytes_each']:,} each; {group['path_count']} paths; "
              f"{group['physical_copies']} physical copies; SHA-256 {group['sha256'][:16]}")
        for path in group["paths"][:8]:
            print(f"  {path}")
        if group["path_count"] > 8:
            print(f"  ... {group['path_count'] - 8} more paths in JSON report")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
