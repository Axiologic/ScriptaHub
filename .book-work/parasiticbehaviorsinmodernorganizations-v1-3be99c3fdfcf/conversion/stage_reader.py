"""Stage the complete, cleaned Parasitic Behaviors PDF as semantic reader HTML.

The page-mapped source remains in income-pdf-candidates. This script drops only
the redundant printed contents, page numerals, and the annexed AI-author blurb;
the retired project letter and rights page were removed in the earlier recorded
cleaning pass. Content chapter text is retained in source order.
"""

from bs4 import BeautifulSoup
from html import escape
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[3]
WORK = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / ".book-work/income-pdf-candidates/3be99c3fdfcfdbe1/clean-draft.html"
SOURCE = ROOT / "income/Parasitic_Behaviors_in_Modern_Organizations/content.pdf"
DEST = WORK / "book/en/full_content.html"
TITLE = "Parasitic Behaviors in Modern Organizations"
CHAPTERS = {
    5: ("preface", "Preface", "Preface"),
    8: ("chapter-1", "Chapter One: The Invisible Feast", "Chapter One The Invisible Feast"),
    38: ("chapter-2", "Chapter Two: The Anatomy of Organizational Parasites", "Chapter Two The Anatomy of Organizational Parasites"),
    70: ("chapter-3", "Chapter Three: The Ecosystem of Exploitation", "Chapter Three The Ecosystem of Exploitation"),
    98: ("chapter-4", "Chapter Four: The Ripple Effect", "Chapter Four The Ripple Effect"),
    126: ("chapter-5", "Chapter Five: Symbiosis or Parasitism?", "Chapter Five Symbiosis or Parasitism?"),
    152: ("chapter-6", "Chapter Six: The Immune System", "Chapter Six The Immune System"),
    177: ("chapter-7", "Chapter Seven: The Evolution of Parasites", "Chapter Seven The Evolution of Parasites"),
    192: ("chapter-8", "Chapter Eight: The Whistleblower's Dilemma", "Chapter Eight The Whistleblower's Dilemma"),
    207: ("chapter-9", "Chapter Nine: Healing the Host", "Chapter Nine Healing the Host"),
    225: ("chapter-10", "Chapter Ten: Beyond Parasitism", "Chapter Ten Beyond Parasitism"),
}

doc = BeautifulSoup(CANDIDATE.read_text(encoding="utf-8"), "html.parser")
blocks = []
counts = {"sourcePages": 258, "contentPages": 0, "contentParagraphs": 0, "removedPrintedPageNumbers": 0}
for section in doc.select("section[data-source-page]"):
    page = int(section["data-source-page"])
    if page == 2:
        blocks.append(f"<p><strong>{escape(TITLE)}</strong></p><p>AI Agent Clark Dayes · 2024</p>")
        continue
    if page == 4 or page >= 253:
        continue
    paragraphs = [p.get_text(" ", strip=True) for p in section.select("p")]
    if not paragraphs:
        continue
    if paragraphs[-1] == str(page - 1):
        paragraphs.pop()
        counts["removedPrintedPageNumbers"] += 1
    if page in CHAPTERS:
        anchor, title, prefix = CHAPTERS[page]
        blocks.append(f'<h1 id="{anchor}">{escape(title)}</h1>')
        if not paragraphs or not paragraphs[0].startswith(prefix):
            raise ValueError(f"Chapter heading moved on PDF page {page}")
        paragraphs[0] = paragraphs[0][len(prefix):].strip()
    for paragraph in paragraphs:
        paragraph = re.sub(r"\s+", " ", paragraph).strip()
        if paragraph:
            blocks.append(f"<p>{escape(paragraph)}</p>")
            counts["contentParagraphs"] += 1
    counts["contentPages"] += 1

if counts["contentPages"] != 248 or len(CHAPTERS) != 11:
    raise ValueError(f"Unexpected page/chapter coverage: {counts}")
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
    "excludedPages": [1, 3, 4, 253, 254, 255, 256, 257, 258],
    "reason": "cover; former rights page; redundant contents; annexed AI-author promotion; former project letter",
    "chapters": len(CHAPTERS),
    **counts,
}
(WORK / "conversion/source-html-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
print(receipt)
