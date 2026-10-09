"""Stage the cleaned full Formal Logic PDF text in reading order as HTML."""

from bs4 import BeautifulSoup
from html import escape
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[3]
WORK = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / ".book-work/income-pdf-candidates/bc57ff5a86bb1198/clean-draft.html"
SOURCE = ROOT / "income/Exploring_Formal_Logic____An_AI_Assisted_Educational_Journey/content.pdf"
DEST = WORK / "book/en/full_content.html"
TITLE = "Exploring Formal Logic: An AI-Assisted Educational Journey"
# PDF page, zero-based paragraph on that page, stable anchor, displayed heading,
# literal source prefix. Some new chapters follow the previous chapter's close
# on the same page, hence paragraph indices must be preserved.
CHAPTERS = {
    6: (0, "preface", "Preface", "Preface"),
    8: (0, "introduction", "Introduction", "Introduction"),
    11: (0, "chapter-1", "Chapter One: Foundations of Formal Logic", "Chapter One Foundations of Formal Logic"),
    60: (0, "chapter-2", "Chapter Two: Propositional Logic", "Chapter Two Propositional Logic"),
    99: (0, "chapter-3", "Chapter Three: Predicate Logic", "Chapter Three Predicate Logic"),
    131: (0, "chapter-4", "Chapter Four: Modal Logic and Other Non-Classical Logic", "Chapter Four Modal Logic and Other Non-Classical Logic"),
    165: (0, "chapter-5", "Chapter Five: Formal Logic and Mathematics", "Chapter Five Formal Logic and Mathematics"),
    192: (1, "chapter-6", "Chapter Six: Formal Logic and Artificial Intelligence", "Chapter Six Formal Logic and Artificial Intelligence"),
    212: (1, "chapter-7", "Chapter Seven: Formal Logic in Computer Science and Programming", "Chapter Seven Formal Logic in Computer Science and Programming"),
    235: (0, "chapter-8", "Chapter Eight: Formal Logic in Philosophy and Ethics", "Chapter Eight Formal Logic in Philosophy and Ethics"),
    262: (0, "chapter-9", "Chapter Nine: The Future of Formal Logic", "Chapter Nine The Future of Formal Logic"),
}

doc = BeautifulSoup(CANDIDATE.read_text(encoding="utf-8"), "html.parser")
blocks = [f"<p><strong>{escape(TITLE)}</strong></p><p>Albert Meta One · 2024</p>"]
counts = {"sourcePages": 296, "contentPages": 0, "contentParagraphs": 0, "removedPrintedPageNumbers": 0}
for section in doc.select("section[data-source-page]"):
    page = int(section["data-source-page"])
    # Page 1 is source cover; 3 is the retired rights notice; 4–5 are a
    # printed contents list; 291–292 are a promotional AI-author profile;
    # 293 onward contained the retired project letter.
    if page < 6 or page > 290:
        continue
    paragraphs = [p.get_text(" ", strip=True) for p in section.select("p")]
    if paragraphs and re.fullmatch(r"\d+", paragraphs[-1]):
        paragraphs.pop()
        counts["removedPrintedPageNumbers"] += 1
    for i, paragraph in enumerate(paragraphs):
        if page in CHAPTERS and i == CHAPTERS[page][0]:
            _, anchor, heading, prefix = CHAPTERS[page]
            if not paragraph.startswith(prefix):
                raise ValueError(f"Heading moved on page {page}: {paragraph[:90]}")
            blocks.append(f'<h1 id="{anchor}">{escape(heading)}</h1>')
            paragraph = paragraph[len(prefix):].strip()
        paragraph = re.sub(r"\s+", " ", paragraph).strip()
        if paragraph:
            blocks.append(f"<p>{escape(paragraph)}</p>")
            counts["contentParagraphs"] += 1
    counts["contentPages"] += 1

if counts["contentPages"] != 285 or len(CHAPTERS) != 11:
    raise ValueError(f"Incomplete Formal Logic page/chapter coverage: {counts}")
body = "\n".join(blocks)
if re.search(r"OutfinityGift|outfinitygift\.com", body, re.I):
    raise ValueError("Retired brand survived in reader")
html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(TITLE)}</title><style>body{{font:1.08rem/1.65 Georgia,serif;margin:0;color:#222;background:#fff}}article{{max-width:74ch;margin:auto;padding:2rem 1.2rem}}h1{{font:700 1.8rem/1.25 system-ui,sans-serif;margin:2em 0 .8em}}p{{margin:0 0 1em;text-align:justify}}@media print{{article{{max-width:none;padding:0}}h1{{break-after:avoid}}}}</style></head><body><article data-reader-content>
{body}
</article></body></html>
'''
DEST.parent.mkdir(parents=True, exist_ok=True)
DEST.write_text(html, encoding="utf-8")
receipt = {
    "source": SOURCE.relative_to(ROOT).as_posix(),
    "sourceSha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    "cleanDraft": CANDIDATE.relative_to(ROOT).as_posix(),
    "cleanDraftSha256": hashlib.sha256(CANDIDATE.read_bytes()).hexdigest(),
    "reader": DEST.relative_to(ROOT).as_posix(),
    "readerSha256": hashlib.sha256(DEST.read_bytes()).hexdigest(),
    "excludedPages": [1, 2, 3, 4, 5, 291, 292, 293, 294, 295, 296],
    "reason": "cover/byline; former rights; redundant contents; AI-author promotion; former project letter",
    "chapters": len(CHAPTERS),
    **counts,
}
(WORK / "conversion/source-html-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
print(receipt)
