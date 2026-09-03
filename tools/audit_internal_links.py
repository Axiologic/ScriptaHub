#!/usr/bin/env python3
"""Report broken local links and fragment anchors in the static HTML site.

Run from the repository root:

    python3 tools/audit_internal_links.py --check

External URLs, email links, data URLs and JavaScript links are deliberately
ignored.  The command has no network dependency.  With ``--check`` it exits
non-zero when at least one local target or anchor is missing, so it is suitable
for a release check or CI.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
import sys
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SITE = ROOT / "docs"
LINK_ATTRIBUTES = {"href", "src", "poster"}
IGNORED_SCHEMES = {"data", "javascript", "mailto", "tel", "http", "https"}


@dataclass(frozen=True)
class Link:
    value: str
    line: int
    attribute: str


class HtmlInventory(HTMLParser):
    """Collect navigable local references and anchors from an HTML file."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[Link] = []
        self.anchors: set[str] = set()

    def handle_starttag(self, _tag: str, attrs: list[tuple[str, str | None]]) -> None:
        line, _ = self.getpos()
        for attribute, value in attrs:
            name = attribute.lower()
            if name in {"id", "name"} and value:
                self.anchors.add(value)
            elif name in LINK_ATTRIBUTES and value:
                self.links.append(Link(value, line, name))
            elif name == "srcset" and value:
                for candidate in value.split(","):
                    url = candidate.strip().split(maxsplit=1)[0]
                    if url:
                        self.links.append(Link(url, line, name))


def is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def is_local(reference: str) -> bool:
    parts = urlsplit(reference)
    return not (
        reference.startswith("//")
        or parts.scheme.lower() in IGNORED_SCHEMES
    )


def parse_html(path: Path) -> HtmlInventory:
    parser = HtmlInventory()
    parser.feed(path.read_text(encoding="utf-8", errors="replace"))
    parser.close()
    return parser


def audit(site: Path) -> list[str]:
    site = site.resolve()
    inventory = {path.resolve(): parse_html(path) for path in sorted(site.rglob("*.html"))}
    anchors = {path: data.anchors for path, data in inventory.items()}
    problems: list[str] = []

    for source, data in inventory.items():
        for link in data.links:
            reference = link.value.strip()
            if not reference or not is_local(reference):
                continue
            parts = urlsplit(reference)
            target = source if not parts.path else (source.parent / unquote(parts.path)).resolve()
            if not is_within(target, site):
                problems.append(f"{source.relative_to(site)}:{link.line}: {link.attribute} escapes docs/: {reference}")
                continue
            if target.is_dir():
                target = target / "index.html"
            if not target.is_file():
                problems.append(f"{source.relative_to(site)}:{link.line}: missing local target: {reference}")
                continue
            if parts.fragment:
                target_anchors = anchors.get(target)
                if target_anchors is None and target.suffix.lower() == ".html":
                    target_anchors = parse_html(target).anchors
                    anchors[target] = target_anchors
                if target_anchors is not None and unquote(parts.fragment) not in target_anchors:
                    problems.append(f"{source.relative_to(site)}:{link.line}: missing anchor #{unquote(parts.fragment)} in {target.relative_to(site)}")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_SITE, help="static-site root to scan (default: docs)")
    parser.add_argument("--check", action="store_true", help="return 1 if a broken local link or anchor is found")
    args = parser.parse_args(argv)
    if not args.root.is_dir():
        print(f"Missing site root: {args.root}", file=sys.stderr)
        return 2
    problems = audit(args.root)
    if problems:
        print("\n".join(problems))
        print(f"\n{len(problems)} local-link problem(s) found.", file=sys.stderr)
        return 1 if args.check else 0
    print(f"No broken local HTML links or fragment anchors in {args.root}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
