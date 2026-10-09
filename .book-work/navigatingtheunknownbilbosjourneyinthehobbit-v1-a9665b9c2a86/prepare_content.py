import json
import re
from pathlib import Path

from bs4 import BeautifulSoup

root = Path(__file__).parent
draft = BeautifulSoup(Path('.book-work/income-pdf-candidates/a9665b9c2a862ae3/clean-draft.html').read_text(encoding='utf-8'), 'html.parser')
out = BeautifulSoup(
    '<!doctype html><html lang="en"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1">'
    '<title>Navigating the Unknown: Bilbo’s Journey in The Hobbit</title>'
    '</head><body><article data-reader-content></article></body></html>',
    'html.parser',
)
article = out.article
h1 = out.new_tag('h1', id='book-title')
h1.string = 'Navigating the Unknown: Bilbo’s Journey in The Hobbit'
article.append(h1)
heads = {
    10: ('Introduction', 1),
    13: ('Chapter 1 — Bilbo’s Journey: A Hobbit out of His Depth', 3),
    19: ('Chapter 2 — Confronting Trolls and Goblins', 2),
    26: ('Chapter 3 — Defying the Dragon: Bilbo’s Bold Gambit', 3),
    32: ('Chapter 4 — Bilbo’s Newfound Wisdom', 2),
    38: ('Conclusion', 1),
    48: ('Bibliography', 1),
}
kept = list(range(10, 40)) + [48, 49]
sections = []
for page in kept:
    sec = draft.select_one(f'section[data-source-page="{page}"]')
    assert sec, page
    paragraphs = sec.find_all('p', recursive=False)
    if page in heads:
        label, skip = heads[page]
        heading = out.new_tag('h2', id='bibliography' if page == 48 else f'chapter-{len(sections)+1}')
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
# The delivered conclusion switches from interpretation to a direct sales
# invitation and a list advertising unrelated books. Keep its literary argument.
for p in article.find_all('p', recursive=False):
    value = p.get_text(' ', strip=True)
    marker = 'If you have yet to read The Hobbit, it is an adventure worth taking.'
    if marker in value:
        p.string = value.split(marker, 1)[0].rstrip()
assert len(sections) == 7
assert not any(x in article.get_text(' ', strip=True).lower() for x in ('outfinitygift', 'outfinity srl', 'about ai author'))
(root / 'book/en/full_content.html').write_text(str(out) + '\n', encoding='utf-8')
(root / 'qa').mkdir(exist_ok=True)
(root / 'qa/source-selection.json').write_text(json.dumps({
    'source': 'income/Navigating_the_Unknown__Bilbo_s_Journey_in_The_Hobbit/content.pdf',
    'retainedPdfPages': kept,
    'excludedPdfPages': list(range(1, 10)) + list(range(40, 48)) + [50],
    'reason': 'Keep thematic introduction, four original literary chapters, conclusion and bibliography; remove rights, table of contents, promotional preface, former-project annex and the conclusion’s direct sales invitation and unrelated book list.',
    'sections': sections,
    'readerWords': len(article.get_text(' ', strip=True).split()),
}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Prepared original reader:', len(article.get_text(' ', strip=True).split()), 'words')
