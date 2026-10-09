#!/usr/bin/env python3
"""Reflow the cleaned, page-indexed PDF extraction into the complete reader."""

from bs4 import BeautifulSoup
from html import escape
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[3]
WORK = Path(__file__).resolve().parents[1]
SOURCE = ROOT / ".book-work/income-pdf-candidates/45859534d7ccbbf3/clean-draft.html"
DEST = WORK / "book/en/full_content.html"

parsed = BeautifulSoup(SOURCE.read_text(encoding="utf-8"), "html.parser")
pages = {int(section["data-source-page"]): [p.get_text(" ", strip=True) for p in section.select("p")] for section in parsed.select("section[data-source-page]")}


def para(*items: tuple[int, int]) -> str:
    return " ".join(pages[page][index] for page, index in items)


parts = [
    '<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Was the 2008 Crash Planned for Bitcoin?</title></head><body><article>',
    '<h1>Was the 2008 Crash Planned for Bitcoin?</h1>',
    '<h2 id="preface">Preface</h2>',
    f'<p>{escape(para((5, 1), (6, 0)))}</p>',
    '<h2 id="ch1">Chapter One</h2>',
    f'<h3>{escape(pages[7][1])}</h3>',
    f'<p>{escape(para((7, 2)))}</p>',
    f'<p>{escape(para((8, 0)))}</p>',
    '<h2 id="ch2">Chapter Two</h2>',
    f'<h3>{escape(pages[9][1])}</h3>',
    f'<p>{escape(para((9, 2), (10, 0)))}</p>',
    '<h2 id="ch3">Chapter Three</h2>',
    f'<h3>{escape(pages[11][1])}</h3>',
    f'<p>{escape(para((11, 2)))}</p>',
    f'<p>{escape(para((12, 0)))}</p>',
    '<h2 id="ch4">Chapter Four</h2>',
    f'<h3>{escape(pages[13][1])}</h3>',
    f'<p>{escape(para((13, 2)))}</p>',
    f'<p>{escape(para((13, 3), (14, 0)))}</p>',
    '<h2 id="conclusion">Conclusion</h2>',
    f'<h3>{escape(pages[15][1])}</h3>',
    *(f'<p>{escape(para((page, index)))}</p>' for page, index in ((15, 2), (15, 3), (16, 0), (16, 1))),
    f'<h3>{escape(pages[16][2])}</h3>',
    *(f'<p>{escape(para((page, index)))}</p>' for page, index in ((16, 3), (16, 4), (17, 0))),
    '<h2 id="bibliography">Bibliography</h2>',
    *(f'<p>{escape(para((24, index)))}</p>' for index in (1, 2)),
    '</article></body></html>',
]

DEST.parent.mkdir(parents=True, exist_ok=True)
DEST.write_text("\n".join(parts) + "\n", encoding="utf-8")
source_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
receipt = {
    "cleanDraft": str(SOURCE.relative_to(ROOT)),
    "cleanDraftSha256": source_hash,
    "fullReader": str(DEST.relative_to(ROOT)),
    "sections": {"preface": [5, 6], "chapterOne": [7, 8], "chapterTwo": [9, 10], "chapterThree": [11, 12], "chapterFour": [13, 14], "conclusion": [15, 16, 17], "bibliography": [24]},
    "omittedParatextPages": [2, 3, 4, 18, 19, 20, 21, 22, 23],
}
(WORK / "conversion/receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
print(DEST)
