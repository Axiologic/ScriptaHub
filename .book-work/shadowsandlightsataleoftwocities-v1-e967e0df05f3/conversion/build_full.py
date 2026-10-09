#!/usr/bin/env python3
"""Reflow the source's four content chapters and substantive conclusion."""
from bs4 import BeautifulSoup
from html import escape
from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parents[3]
work = Path(__file__).resolve().parents[1]
source = root / ".book-work/income-pdf-candidates/e967e0df05f3e967/clean-draft.html"
out = work / "book/en/full_content.html"
parsed = BeautifulSoup(source.read_text(encoding="utf-8"), "html.parser")
pages = {int(sec["data-source-page"]): [p.get_text(" ", strip=True) for p in sec.select("p")] for sec in parsed.select("section[data-source-page]")}
sections = [(7, 9, "ch1"), (10, 14, "ch2"), (15, 19, "ch3"), (20, 23, "ch4")]
parts = [
    '<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Shadows and Lights: A Tale of Two Cities</title></head><body><article>',
    '<h1>Shadows and Lights: A Tale of Two Cities</h1>',
]
for start, end, anchor in sections:
    parts.append(f'<h2 id="{anchor}">{escape(pages[start][0])}</h2>')
    parts.append(f'<h3>{escape(pages[start][1])}</h3>')
    paragraphs = []
    for page in range(start, end + 1):
        first = 2 if page == start else 0
        for index, paragraph in enumerate(pages[page][first:]):
            if paragraph.isdigit():
                continue
            # Page-boundary continuations begin with a lower-case word.
            if page > start and index == 0 and paragraph[0].islower() and paragraphs:
                paragraphs[-1] += " " + paragraph
            else:
                paragraphs.append(paragraph)
    parts.extend(f'<p>{escape(paragraph)}</p>' for paragraph in paragraphs)
parts.append('<h2 id="conclusion">Conclusion</h2>')
parts.extend(f'<p>{escape(pages[24][index])}</p>' for index in (1, 2))
parts.append('<h2 id="bibliography">Bibliography</h2>')
parts.extend(f'<p>{escape(pages[34][index])}</p>' for index in range(1, 6))
parts.append('</article></body></html>')
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text("\n".join(parts) + "\n", encoding="utf-8")
(work / "conversion/receipt.json").write_text(json.dumps({
    "sourceCleanDraft": str(source.relative_to(root)),
    "sourceCleanDraftSha256": hashlib.sha256(source.read_bytes()).hexdigest(),
    "contentPages": [7, 23],
    "conclusionParagraphs": ["24:1", "24:2"],
    "bibliographyPage": 34,
    "excluded": "source title, rights, contents, promotional preface, promotional reading invitation, project/author annexes",
}, indent=2) + "\n", encoding="utf-8")
print(out)
