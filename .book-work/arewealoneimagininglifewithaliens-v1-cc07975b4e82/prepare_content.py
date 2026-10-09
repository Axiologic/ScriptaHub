import json
import re
from pathlib import Path

from bs4 import BeautifulSoup


root = Path(__file__).parent
source = Path('.book-work/income-pdf-candidates/cc07975b4e8298fb/clean-draft.html')
draft = BeautifulSoup(source.read_text(encoding='utf-8'), 'html.parser')
out = BeautifulSoup(
    '<!doctype html><html lang="en"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1">'
    '<title>Are We Alone? Imagining Life with Aliens</title></head>'
    '<body><article data-reader-content></article></body></html>',
    'html.parser',
)
article = out.article
title = out.new_tag('h1', id='book-title')
title.string = 'Are We Alone? Imagining Life with Aliens'
article.append(title)
heads = {
    9: ('Introduction', 1),
    13: ('Chapter 1 — The Universe: An Infinite Web of Possibilities', 2),
    20: ("Chapter 2 — What Extremophiles Teach Us About Life's Limits", 2),
    26: ('Chapter 3 — Technology: Our Eyes in the Search for Life', 2),
    32: ('Chapter 4 — The Impact of Discovery: What If We’re Not Alone?', 2),
    39: ('Conclusion — A Universe Full of Possibilities', 2),
    51: ('Bibliography', 1),
}
kept = list(range(9, 45)) + [51, 52]
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

# The PDF extraction retains page boundaries as separate paragraphs. Rejoin
# sentences that cross a physical page without changing the author's wording.
for p in list(article.find_all('p', recursive=False)):
    previous = p.find_previous_sibling()
    if previous and previous.name == 'p':
        left = previous.get_text(' ', strip=True)
        right = p.get_text(' ', strip=True)
        if left and right and not re.search(r'[.!?:;”"\)]$', left) and re.match(r'^[a-z]', right):
            previous.string = left + ' ' + right
            p.decompose()

assert len(sections) == 7
assert not any(x in article.get_text(' ', strip=True).lower() for x in ('outfinitygift', 'outfinity srl', 'about ai author'))
(root / 'book/en/full_content.html').write_text(str(out) + '\n', encoding='utf-8')
(root / 'qa').mkdir(exist_ok=True)
(root / 'qa/source-selection.json').write_text(json.dumps({
    'source': 'income/Are_We_Alone__Imagining_Life_with_Aliens/content.pdf',
    'retainedPdfPages': kept,
    'excludedPdfPages': list(range(1, 9)) + list(range(45, 51)),
    'reason': 'Keep original thematic introduction, four chapters, conclusion and bibliography; remove cover, old rights, table of contents, promotional preface and former project annex.',
    'sections': sections,
    'readerWords': len(article.get_text(' ', strip=True).split()),
}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Prepared original reader:', len(article.get_text(' ', strip=True).split()), 'words')
