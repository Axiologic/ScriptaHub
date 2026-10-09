import json
import re
from pathlib import Path

from bs4 import BeautifulSoup

root = Path(__file__).parent
draft = BeautifulSoup(Path('.book-work/income-pdf-candidates/0f941981301f1e6f/clean-draft.html').read_text(encoding='utf-8'), 'html.parser')
out = BeautifulSoup(
    '<!doctype html><html lang="en"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1">'
    '<title>Mastering Economic Principles with Marshall’s Wisdom</title>'
    '</head><body><article data-reader-content></article></body></html>',
    'html.parser',
)
article = out.article
title = out.new_tag('h1', id='book-title')
title.string = 'Mastering Economic Principles with Marshall’s Wisdom'
article.append(title)
heads = {
    8: ('Introduction', 1),
    15: ('Chapter I — Decoding Supply and Demand Dynamics', 1),
    21: ('Chapter II — The Art of Market Equilibrium', 1),
    26: ('Chapter III — The Value Puzzle', 1),
    32: ('Chapter IV — Economic Principles in Action', 1),
    38: ('Conclusion — The Enduring Relevance of Marshall’s Economic Principles', 1),
    52: ('Bibliography', 1),
}
kept = list(range(8, 44)) + [52]
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
# The delivered conclusion ends with a direct advertisement for another
# volume. Keep the substantive closing argument and omit that sales passage.
for p in article.find_all('p', recursive=False):
    value = p.get_text(' ', strip=True)
    marker = 'For those eager to delve deeper into the intricate world of economics'
    if marker in value:
        p.string = value.split(marker, 1)[0].rstrip()
assert len(sections) == 7
assert not any(x in article.get_text(' ', strip=True).lower() for x in ('outfinitygift', 'outfinity srl', 'about ai author'))
(root / 'book/en/full_content.html').write_text(str(out) + '\n', encoding='utf-8')
(root / 'qa').mkdir(exist_ok=True)
(root / 'qa/source-selection.json').write_text(json.dumps({
    'source': 'income/Mastering_Economic_Principles_with_Marshall_s_Wisdom/content.pdf',
    'retainedPdfPages': kept,
    'excludedPdfPages': list(range(1, 8)) + list(range(44, 52)),
    'reason': 'Keep original thematic introduction, four chapters, conclusion and bibliography; remove old rights, table of contents, promotional preface, former-project annex and the conclusion’s direct advertisement for another book.',
    'sections': sections,
    'readerWords': len(article.get_text(' ', strip=True).split()),
}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Prepared original reader:', len(article.get_text(' ', strip=True).split()), 'words')
