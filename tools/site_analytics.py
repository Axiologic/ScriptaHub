"""Install and audit the single shared analytics loader on every public HTML page."""
from __future__ import annotations

import hashlib
from html.parser import HTMLParser
import os
from pathlib import Path
import re

DOCS = Path(__file__).resolve().parents[1] / "docs"
LOADER = DOCS / "assets/analytics.js"
SCRIPT = re.compile(r'[ \t]*<script\b[^>]*>.*?</script\s*>', re.I | re.S)


class Scripts(HTMLParser):
    def __init__(self, source: str):
        super().__init__()
        self.scripts = []
        self.in_head = False
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        if tag == "head":
            self.in_head = True
        if tag == "script":
            self.scripts.append((dict(attrs), self.in_head))

    def handle_endtag(self, tag):
        if tag == "head":
            self.in_head = False


def is_tracker(attrs: dict) -> bool:
    src = attrs.get("src") or ""
    return "data-website-id" in attrs or src.split("?", 1)[0].split("/")[-1] == "analytics.js" or "cloud.umami.is/script.js" in src


def install(source: str, page_dir: Path) -> str:
    """Keep content intact; replace tracker tags with one deferred head include."""
    def remove(match):
        scripts = Scripts(match.group()).scripts
        return "" if scripts and is_tracker(scripts[0][0]) else match.group()

    source = SCRIPT.sub(remove, source)
    relative = Path(os.path.relpath(LOADER, page_dir)).as_posix()
    if not relative.startswith("."):
        relative = "./" + relative
    digest = hashlib.sha256(LOADER.read_bytes()).hexdigest()[:12]
    tag = f'<script defer src="{relative}?v={digest}"></script>'
    if re.search(r'<head\b[^>]*>', source, re.I):
        return re.sub(r'(<head\b[^>]*>)\s*', lambda m: m.group(1) + '\n  ' + tag + '\n', source, count=1, flags=re.I)
    # The standalone SHF preview originally relied on an implicit HTML head.
    return re.sub(r'(<!doctype\s+html\s*>)', lambda m: m.group(1) + '<head>' + tag + '</head>', source, count=1, flags=re.I)


def refresh() -> int:
    changed = 0
    for page in DOCS.rglob("*.html"):
        source = page.read_text(encoding="utf-8")
        updated = install(source, page.parent)
        if updated != source:
            page.write_text(updated, encoding="utf-8")
            changed += 1
    return changed


def check() -> list[str]:
    problems = []
    for page in DOCS.rglob("*.html"):
        scripts = Scripts(page.read_text(encoding="utf-8")).scripts
        trackers = [(attrs, head) for attrs, head in scripts if is_tracker(attrs)]
        if len(trackers) != 1:
            problems.append(f"{page.relative_to(DOCS)}: expected one shared analytics include, found {len(trackers)}")
            continue
        attrs, in_head = trackers[0]
        target = (page.parent / (attrs.get("src") or "").split("?", 1)[0]).resolve()
        if target != LOADER.resolve() or not in_head or "defer" not in attrs or "data-website-id" in attrs:
            problems.append(f"{page.relative_to(DOCS)}: analytics must use the deferred shared head include")
    return problems


if __name__ == "__main__":
    print(f"Updated analytics on {refresh()} HTML pages.")
    errors = check()
    if errors:
        raise SystemExit("\n".join(errors))
