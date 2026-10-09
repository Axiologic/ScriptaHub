"""Select only Conan Doyle's foreword, epigraph and sixteen novel chapters."""
import json
import re
from pathlib import Path

from bs4 import BeautifulSoup

root = Path(__file__).resolve().parent
draft = BeautifulSoup(Path('.book-work/income-pdf-candidates/2ebda2ee8051d809/clean-draft.html').read_text(), 'html.parser')
out = BeautifulSoup('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>The Lost World</title></head><body><article data-reader-content></article></body></html>', 'html.parser')
article = out.article
title = out.new_tag('h1', id='book-title'); title.string = 'The Lost World'; article.append(title)
credit = out.new_tag('p'); credit.string = 'Arthur Conan Doyle'; article.append(credit)
sections = []

def para(text):
    node = out.new_tag('p'); node.string = text; article.append(node)

def heading(text, page, ident):
    node = out.new_tag('h2', id=ident); node.string = text; article.append(node)
    sections.append({'id': ident, 'title': text, 'sourcePage': page})

def parts(page):
    section = draft.select_one(f'section[data-source-page="{page}"]')
    assert section is not None, page
    values = [re.sub(r'\s+', ' ', p.get_text(' ', strip=True)).strip() for p in section.find_all('p', recursive=False)]
    return [v for v in values if v and not re.fullmatch(r'\d+', v)]

foreword = parts(6)
assert foreword[0] == 'FOREWORD' and len(foreword) == 2
heading('Foreword', 6, 'foreword'); para(foreword[1])
epigraph = parts(22)
assert epigraph[0] == 'ORIGINAL BOOK' and epigraph[2] == 'by Sir Arthur Conan Doyle'
assert epigraph[1].startswith('THE LOST WORLD ')
para(epigraph[1][len('THE LOST WORLD '):])

roman = ['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII','XIII','XIV','XV','XVI']
chapter_pages = []
for page in range(24, 269):
    values = parts(page)
    if values[0].startswith('CHAPTER '):
        chapter = values.pop(0)
        subtitle = values.pop(0)
        idx = len(chapter_pages)
        assert chapter == f'CHAPTER {roman[idx]}'
        chapter_pages.append(page)
        heading(f'Chapter {roman[idx]} — {subtitle}', page, f'chapter-{idx+1}')
    for value in values:
        para(value)

# The PDF exporter divides some single paragraphs at a physical page edge.
# Join only a continuation that begins with a lower-case letter or follows a
# clearly nonterminal ending; chapter headings remain hard boundaries.
for node in list(article.find_all('p', recursive=False)):
    prev = node.find_previous_sibling()
    if prev is None or prev.name != 'p':
        continue
    left, right = prev.get_text(' ', strip=True), node.get_text(' ', strip=True)
    if left and right and (re.match(r'^[a-z]', right) or not re.search(r'[.!?:;”"’\)]$', left)):
        prev.string = left + ' ' + right
        node.decompose()

# Keep HTML translation units tractable without changing the book's words.
for node in list(article.find_all('p', recursive=False)):
    value = node.get_text(' ', strip=True)
    if len(value.split()) <= 180:
        continue
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z“‘])', value)
    if len(sentences) < 3:
        continue
    groups, current, words = [], [], 0
    for sentence in sentences:
        count = len(sentence.split())
        if current and words + count > 145:
            groups.append(' '.join(current)); current, words = [], 0
        current.append(sentence); words += count
    if current:
        groups.append(' '.join(current))
    if len(groups) > 1:
        for text in groups:
            p = out.new_tag('p'); p.string = text; node.insert_before(p)
        node.decompose()

body = article.get_text(' ', strip=True)
assert len(chapter_pages) == 16 and len(body.split()) > 65000, (chapter_pages, len(body.split()))
assert not any(x in body.casefold() for x in ('outfinity', 'taler vox', 'ai perspective', 'all rights reserved'))
target = root / 'book/en/full_content.html'; target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(str(out) + '\n')
qa = root / 'qa'; qa.mkdir(exist_ok=True)
(qa / 'source-selection.json').write_text(json.dumps({
    'source': 'income/The_Lost_World/content.pdf',
    'retainedPdfPages': [6, 22] + list(range(24, 269)),
    'excludedPdfPages': list(range(1, 6)) + list(range(7, 22)) + [23] + list(range(269, 273)),
    'reason': 'Retain Conan Doyle’s original foreword, epigraph, and chapters I–XVI. Exclude rights, duplicate contents, OutfinityGift promotional preface, AI commentary and project annexes.',
    'chapterPages': chapter_pages,
    'sections': sections,
    'readerWords': len(body.split())
}, ensure_ascii=False, indent=2) + '\n')
print(f'Prepared {len(body.split())} words, {len(chapter_pages)} chapters')
