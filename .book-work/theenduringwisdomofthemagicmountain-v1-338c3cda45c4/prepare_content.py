import json
import re
from pathlib import Path

from bs4 import BeautifulSoup

root = Path(__file__).parent
draft = BeautifulSoup(Path('.book-work/income-pdf-candidates/338c3cda45c43ac7/clean-draft.html').read_text(encoding='utf-8'), 'html.parser')
out = BeautifulSoup(
    '<!doctype html><html lang="en"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1">'
    '<title>The Enduring Wisdom of The Magic Mountain</title>'
    '</head><body><article data-reader-content></article></body></html>',
    'html.parser',
)
article = out.article
h1 = out.new_tag('h1', id='book-title')
h1.string = 'The Enduring Wisdom of The Magic Mountain'
article.append(h1)
heads = {
    7: ('Introduction', 1),
    9: ('Chapter 1 — The Battlefield of Ideas', 2),
    14: ('Chapter 2 — The Alchemy of Time', 2),
    19: ('Chapter 3 — Echoes of Affliction: Society’s Persistent Maladies', 2),
    26: ('Chapter 4 — The Human Condition in Flux: From Berghof to the Digital Age', 2),
    32: ('Chapter 5 — The Alchemy of Art and Culture', 2),
    37: ('Chapter 6 — Descending from the Mountain: Reflections for a New Age', 2),
    42: ('Conclusion', 1),
    51: ('Bibliography', 1),
}
kept = list(range(7, 44)) + [51]
sections = []
for page in kept:
    sec = draft.select_one(f'section[data-source-page="{page}"]')
    assert sec, page
    paragraphs = sec.find_all('p', recursive=False)
    if page in heads:
        label, skip = heads[page]
        heading = out.new_tag('h2', id='bibliography' if page == 51 else f'chapter-{len(sections)+1}')
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
# A physical page break splits the protagonist's proper name; the generic
# lower-case continuation rule cannot recognize it.
for p in list(article.find_all('p', recursive=False)):
    prev = p.find_previous_sibling()
    if prev and prev.name == 'p' and prev.get_text(' ', strip=True).endswith('Hans') and p.get_text(' ', strip=True).startswith('Castorp,'):
        prev.string = prev.get_text(' ', strip=True) + ' ' + p.get_text(' ', strip=True)
        p.decompose()
assert len(sections) == 9
assert not any(x in article.get_text(' ', strip=True).lower() for x in ('outfinitygift', 'outfinity srl', 'about ai author'))
(root / 'book/en/full_content.html').write_text(str(out) + '\n', encoding='utf-8')
(root / 'qa').mkdir(exist_ok=True)
(root / 'qa/source-selection.json').write_text(json.dumps({
    'source': 'income/The_Enduring_Wisdom_of_The_Magic_Mountain/content.pdf',
    'retainedPdfPages': kept,
    'excludedPdfPages': list(range(1, 7)) + list(range(44, 51)),
    'reason': 'Keep original literary analysis in introduction, six chapters, conclusion and bibliography; remove old rights, promotional preface, table of contents and former-project annex.',
    'sections': sections,
    'readerWords': len(article.get_text(' ', strip=True).split()),
}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Prepared original reader:', len(article.get_text(' ', strip=True).split()), 'words')
