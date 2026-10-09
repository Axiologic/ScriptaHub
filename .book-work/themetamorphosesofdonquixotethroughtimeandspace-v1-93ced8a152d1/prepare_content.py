import json
import re
from pathlib import Path

from bs4 import BeautifulSoup

root = Path(__file__).parent
draft = BeautifulSoup(Path('.book-work/income-pdf-candidates/93ced8a152d16dd9/clean-draft.html').read_text(encoding='utf-8'), 'html.parser')
out = BeautifulSoup(
    '<!doctype html><html lang="en"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1">'
    '<title>The Metamorphoses of Don Quixote Through Time and Space</title>'
    '</head><body><article data-reader-content></article></body></html>',
    'html.parser',
)
article = out.article
h1 = out.new_tag('h1', id='book-title')
h1.string = 'The Metamorphoses of Don Quixote Through Time and Space'
article.append(h1)
heads = {
    7: ('Chapter 1 — Don Quixote in a Broken World: The Knight of the Wasteland', 2),
    11: ('Chapter 2 — The Masked Dreamer: Justice in the Urban Jungle', 2),
    17: ('Chapter 3 — The Last Knight in a World Gone Mad', 2),
    21: ('Chapter 4 — The Most Loyal (and Hungry) Squire in History', 2),
    25: ('Chapter 5 — The Virtual Knight: DQ 2.0', 2),
    31: ('Chapter 6 — Don Quixote in Space: The Cosmic Knight', 2),
    38: ('Conclusion', 1),
    50: ('Bibliography', 1),
}
kept = list(range(7, 43)) + [50]
sections = []
for page in kept:
    sec = draft.select_one(f'section[data-source-page="{page}"]')
    assert sec, page
    paragraphs = sec.find_all('p', recursive=False)
    if page in heads:
        label, skip = heads[page]
        heading = out.new_tag('h2', id='bibliography' if page == 50 else f'chapter-{len(sections)+1}')
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
# Rejoin only an incomplete sentence at a physical page boundary. Preserve
# dialogue and deliberate short paragraphs inside the chapters.
for p in list(article.find_all('p', recursive=False)):
    prev = p.find_previous_sibling()
    if prev and prev.name == 'p':
        left, right = prev.get_text(' ', strip=True), p.get_text(' ', strip=True)
        if left and right and not re.search(r'[.!?:;”"\)]$', left) and (re.match(r'^[a-z]', right) or left.endswith(',') and re.match(r'^[A-Z]', right)):
            prev.string = left + ' ' + right
            p.decompose()
assert len(sections) == 8
assert not any(x in article.get_text(' ', strip=True).lower() for x in ('outfinitygift', 'outfinity srl', 'about ai author'))
(root / 'book/en/full_content.html').write_text(str(out) + '\n', encoding='utf-8')
(root / 'qa').mkdir(exist_ok=True)
(root / 'qa/source-selection.json').write_text(json.dumps({
    'source': 'income/The_Metamorphoses_of_Don_Quixote_Through_Time_and_Space/content.pdf',
    'retainedPdfPages': kept,
    'excludedPdfPages': list(range(1, 7)) + list(range(43, 50)),
    'reason': 'Keep the six original speculative retellings, thematic conclusion and bibliography; remove old rights, promotional preface, table of contents and former-project author annex.',
    'sections': sections,
    'readerWords': len(article.get_text(' ', strip=True).split()),
}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Prepared original reader:', len(article.get_text(' ', strip=True).split()), 'words')
