import json
import re
from pathlib import Path

from bs4 import BeautifulSoup

root = Path(__file__).parent
draft = BeautifulSoup(Path('.book-work/income-pdf-candidates/08968f12dc205e91/clean-draft.html').read_text(encoding='utf-8'), 'html.parser')
out = BeautifulSoup(
    '<!doctype html><html lang="en"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1">'
    '<title>Thomas Edison: The Wizard of Menlo Park</title></head>'
    '<body><article data-reader-content></article></body></html>',
    'html.parser',
)
article = out.article
h1 = out.new_tag('h1', id='book-title')
h1.string = 'Thomas Edison: The Wizard of Menlo Park'
article.append(h1)
heads = {
    7: ('Introduction', 1),
    10: ('Chapter 1 — Edison’s Research Revolution', 2),
    15: ('Chapter 2 — Early Interests in Technology', 2),
    20: ('Chapter 3 — Major Innovations and Inventions', 2),
    25: ('Chapter 4 — Work Method and Approach to Innovation', 2),
    30: ('Chapter 5 — Impact on Society and Industry', 2),
    35: ('Chapter 6 — Controversies and Criticisms', 1),
    37: ('Chapter 7 — Thomas Edison’s Legacy', 1),
    43: ('Conclusion', 1),
    52: ('Bibliography', 1),
}
kept = list(range(7, 46)) + [52]
sections = []
for page in kept:
    sec = draft.select_one(f'section[data-source-page="{page}"]')
    assert sec, page
    paragraphs = sec.find_all('p', recursive=False)
    if page in heads:
        label, skip = heads[page]
        heading = out.new_tag('h2', id='bibliography' if page == 52 else f'chapter-{len(sections)+1}')
        heading.string = label
        article.append(heading)
        sections.append({'id': heading['id'], 'title': label, 'page': page})
        paragraphs = paragraphs[skip:]
    for source_p in paragraphs:
        value = re.sub(r'\s+', ' ', source_p.get_text(' ', strip=True))
        if not value or re.fullmatch(r'\d+', value):
            continue
        p = out.new_tag('p')
        p.string = value
        article.append(p)
for p in list(article.find_all('p', recursive=False)):
    prev = p.find_previous_sibling()
    if prev and prev.name == 'p':
        left, right = prev.get_text(' ', strip=True), p.get_text(' ', strip=True)
        if left and right and not re.search(r'[.!?:;”"\)]$', left) and re.match(r'^[a-z]', right):
            prev.string = left + ' ' + right
            p.decompose()
assert len(sections) == 10
assert not any(x in article.get_text(' ', strip=True).lower() for x in ('outfinitygift', 'outfinity srl', 'about ai author'))
(root / 'book/en/full_content.html').write_text(str(out) + '\n', encoding='utf-8')
(root / 'qa').mkdir(exist_ok=True)
(root / 'qa/source-selection.json').write_text(json.dumps({
    'source': 'income/Thomas_Edison__The_Wizard_of_Menlo_Park/content.pdf',
    'retainedPdfPages': kept,
    'excludedPdfPages': list(range(1, 7)) + list(range(46, 52)),
    'reason': 'Keep original thematic introduction, seven chapters, conclusion and bibliography; remove cover, rights, table of contents, promotional preface and old-project annex.',
    'sections': sections,
    'readerWords': len(article.get_text(' ', strip=True).split()),
}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Prepared original reader:', len(article.get_text(' ', strip=True).split()), 'words')
