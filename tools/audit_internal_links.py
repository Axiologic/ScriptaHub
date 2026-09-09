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
from dataclasses import dataclass
import errno
from html.parser import HTMLParser
import os
from pathlib import Path
import re
import sys
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SITE = ROOT / "docs"
LINK_ATTRIBUTES = {"href", "src", "poster"}
ASCII_SPACE = "\t\n\f\r "
EXTERNAL_REFERENCE = re.compile(r"^(?:[\\/]{2}|[a-z][a-z\d+.-]*:)", re.IGNORECASE)


def srcset_urls(value: str) -> list[str]:
    """Extract candidates without treating commas inside URLs as separators."""
    urls: list[str] = []
    position = 0
    while position < len(value):
        while position < len(value) and value[position] in ASCII_SPACE + ",":
            position += 1
        start = position
        while position < len(value) and value[position] not in ASCII_SPACE:
            position += 1
        url = value[start:position]
        if not url:
            break
        if url.endswith(","):
            url = url.rstrip(",")
        else:
            # Data URLs may contain commas. Only descriptor commas outside
            # parentheses delimit candidates after the URL's first whitespace.
            parentheses = 0
            while position < len(value):
                character = value[position]
                position += 1
                if character == "(":
                    parentheses += 1
                elif character == ")" and parentheses:
                    parentheses -= 1
                elif character == "," and not parentheses:
                    break
        if url:
            urls.append(url)
    return urls


@dataclass(frozen=True)
class Link:
    value: str
    line: int
    attribute: str


class HtmlInventory(HTMLParser):
    """Collect navigable local references and anchors from an HTML file."""

    # Older Python versions only suppress markup parsing inside script/style.
    # These additional HTML text elements also cannot contain navigable links.
    CDATA_CONTENT_ELEMENTS = ("script", "style", "textarea", "title", "xmp", "iframe", "noembed", "noframes")

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[Link] = []
        self.anchors: set[str] = set()
        self.tags: list[dict] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        line, _ = self.getpos()
        attributes: dict[str, str | None] = {}
        for attribute, value in attrs:
            attributes.setdefault(attribute.lower(), value)
        self.tags.append({"tagName": tag, "attrs": attributes, "line": line})
        for name, value in attributes.items():
            if name in {"id", "name"} and value:
                self.anchors.add(value)
            elif name in LINK_ATTRIBUTES and value:
                self.links.append(Link(value, line, name))
            elif name == "srcset" and value:
                self.links.extend(Link(url, line, name) for url in srcset_urls(value))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        # In HTML, a trailing slash does not make a script/text element void.
        if tag in self.CDATA_CONTENT_ELEMENTS:
            self.set_cdata_mode(tag)


def is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def is_local(reference: str) -> bool:
    return EXTERNAL_REFERENCE.match(reference) is None


def parse_html_inventory(source: str) -> HtmlInventory:
    parser = HtmlInventory()
    parser.feed(source)
    parser.close()
    return parser


def parse_html(path: Path) -> HtmlInventory:
    return parse_html_inventory(path.read_text(encoding="utf-8", errors="replace"))


def missing_or_loop(error: OSError | RuntimeError) -> bool:
    return isinstance(error, RuntimeError) or error.errno in {errno.ENOENT, errno.ENOTDIR, errno.ELOOP}


def html_sources(site: Path, problems: list[str]) -> list[Path]:
    """Scan real directories; never read HTML through an out-of-root symlink."""
    files: list[Path] = []

    def visit(folder: Path) -> None:
        for path in sorted(folder.iterdir()):
            if path.is_symlink():
                if path.suffix.lower() != ".html":
                    continue
                display = path.relative_to(site).as_posix()
                try:
                    target = path.resolve()
                    if not is_within(target, site):
                        problems.append(f"{display}:1: HTML source escapes docs/: {display}")
                    elif target.is_file():
                        files.append(path)
                    else:
                        problems.append(f"{display}:1: missing local HTML source")
                except (OSError, RuntimeError) as error:
                    if not missing_or_loop(error):
                        raise
                    problems.append(f"{display}:1: missing local HTML source")
            elif path.is_dir():
                visit(path)
            elif path.is_file() and path.suffix.lower() == ".html":
                files.append(path)

    visit(site)
    return sorted(files)


def audit(site: Path) -> list[str]:
    site = Path(site).resolve()
    problems: list[str] = []
    inventory: dict[Path, list[Link]] = {}
    anchors: dict[Path, set[str]] = {}
    for source in html_sources(site, problems):
        data = parse_html(source)
        inventory[source] = data.links
        anchors[source.resolve()] = data.anchors

    for source, links in inventory.items():
        for link in links:
            reference = link.value.strip()
            if not reference or not is_local(reference):
                continue
            before_hash, _, raw_fragment = reference.partition("#")
            path = unquote(before_hash.partition("?")[0]).replace("\\", "/")
            fragment = unquote(raw_fragment)
            prefix = f"{source.relative_to(site).as_posix()}:{link.line}:"
            if "\0" in path:
                problems.append(f"{prefix} invalid local target: {reference}")
                continue
            if not path:
                lexical_target = source
            elif path.startswith("/"):
                lexical_target = site / path[1:]
            else:
                lexical_target = source.parent / path
            try:
                # Browsers collapse URL dot segments before the server follows
                # filesystem symlinks, so alias/../page.html stays at this level.
                lexical_target = Path(os.path.abspath(lexical_target))
                # strict=False resolves existing symlink ancestors and dangling
                # destinations too, even when the final file does not exist.
                target = lexical_target.resolve()
                if not is_within(target, site):
                    problems.append(f"{prefix} {link.attribute} escapes docs/: {reference}")
                    continue
                if target.is_dir():
                    target = (target / "index.html").resolve()
                if not is_within(target, site):
                    problems.append(f"{prefix} {link.attribute} escapes docs/: {reference}")
                    continue
                if not target.is_file():
                    problems.append(f"{prefix} missing local target: {reference}")
                    continue
            except (OSError, RuntimeError) as error:
                if not missing_or_loop(error):
                    raise
                problems.append(f"{prefix} missing local target: {reference}")
                continue
            if fragment:
                target_anchors = anchors.get(target)
                if target_anchors is None and target.suffix.lower() == ".html":
                    target_anchors = parse_html(target).anchors
                    anchors[target] = target_anchors
                if target_anchors is not None and fragment not in target_anchors:
                    problems.append(f"{prefix} missing anchor #{fragment} in {target.relative_to(site).as_posix()}")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_SITE, help="static-site root to scan (default: docs)")
    parser.add_argument("--check", action="store_true", help="return 1 if a broken local link or anchor is found")
    args = parser.parse_args(argv)
    if not args.root.is_dir():
        print(f"Missing site root: {args.root}", file=sys.stderr)
        return 2
    try:
        problems = audit(args.root)
    except (OSError, RuntimeError) as error:
        print(f"Unable to audit site: {error}", file=sys.stderr)
        return 2
    if problems:
        print("\n".join(problems))
        print(f"\n{len(problems)} local-link problem(s) found.", file=sys.stderr)
        return 1 if args.check else 0
    print(f"No broken local HTML links or fragment anchors in {args.root}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
