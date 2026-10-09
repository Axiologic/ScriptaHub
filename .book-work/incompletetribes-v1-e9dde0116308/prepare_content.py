from bs4 import BeautifulSoup
from copy import deepcopy
from html import escape
from pathlib import Path
import json
import re

root = Path('.book-work/incompletetribes-v1-e9dde0116308')
source = root / 'conversion/Incomplete_Tribes.html'
target = root / 'book/en/full_content.html'
original = BeautifulSoup(target.read_text(encoding='utf-8'), 'html.parser')
if original.article and original.article.get('data-prepared-incomplete-tribes') == 'true':
    for paragraph in original.article.find_all('p'):
        if paragraph.get_text(' ', strip=True).lower() in {'— end of draft —', 'end of draft'}:
            paragraph.decompose()
    target.write_text(str(original) + '\n', encoding='utf-8')
    print('Already prepared:', target)
    raise SystemExit(0)
items = list(original.article.find_all(recursive=False))
start = next(i for i, item in enumerate(items) if item.name == 'p' and item.get_text(' ', strip=True) == 'PRELUDE')
subtitle = items[1].get_text(' ', strip=True)
opening = items[4:6]

out = BeautifulSoup('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Incomplete Tribes</title></head><body><article data-reader-content></article></body></html>', 'html.parser')
article = out.article
article['data-prepared-incomplete-tribes'] = 'true'
title = out.new_tag('h1', id='book-title')
title.string = 'Incomplete Tribes'
article.append(title)
sub = out.new_tag('p', **{'class': 'book-subtitle'})
sub.string = subtitle
article.append(sub)
for item in opening:
    if item.name == 'p' and label.lower() in {'— end of draft —', 'end of draft'}:
        i += 1
        continue
    article.append(deepcopy(item))

sections = []
i = start
while i < len(items):
    item = items[i]
    label = item.get_text(' ', strip=True)
    if item.name == 'p' and re.fullmatch(r'PART [IVX]+', label):
        assert i + 1 < len(items)
        part_title = items[i + 1].get_text(' ', strip=True).title()
        heading = out.new_tag('h2', id=label.lower().replace(' ', '-'))
        heading.string = f'{label.title()} — {part_title}'
        article.append(heading)
        sections.append({'id': heading['id'], 'title': heading.get_text(' ', strip=True)})
        i += 2
        continue
    if item.name == 'p' and re.fullmatch(r'CHAPTER \d+', label):
        assert i + 1 < len(items) and items[i + 1].name == 'h1'
        heading = out.new_tag('h3', id='chapter-' + label.split()[-1])
        heading.string = f'{label.title()} — {items[i + 1].get_text(" ", strip=True)}'
        article.append(heading)
        sections.append({'id': heading['id'], 'title': heading.get_text(' ', strip=True)})
        i += 2
        continue
    if item.name == 'p' and label in {'PRELUDE', 'EPILOGUE', 'NOTES'}:
        assert i + 1 < len(items) and items[i + 1].name == 'h1'
        heading = out.new_tag('h2', id=label.lower())
        heading.string = f'{label.title()} — {items[i + 1].get_text(" ", strip=True)}'
        article.append(heading)
        sections.append({'id': heading['id'], 'title': heading.get_text(' ', strip=True)})
        i += 2
        continue
    article.append(deepcopy(item))
    i += 1

target.write_text(str(out) + '\n', encoding='utf-8')
(root / 'qa').mkdir(exist_ok=True)
(root / 'qa/source-selection.json').write_text(json.dumps({
    'source': str(source),
    'retained': 'Original epigraph, opening, prelude, sixteen chapters, epilogue, notes and citation links',
    'removed': 'Duplicated title-page block, draft status and table of contents; chapter labels merged into semantic headings',
    'sections': sections,
    'sourceWords': len(original.article.get_text(' ', strip=True).split()),
    'readerWords': len(article.get_text(' ', strip=True).split()),
}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('sections', len(sections), 'reader words', len(article.get_text(' ', strip=True).split()))
