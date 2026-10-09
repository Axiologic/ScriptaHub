import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

root = Path(__file__).parent
draft = BeautifulSoup(Path('.book-work/income-pdf-candidates/361494dcee97db28/clean-draft.html').read_text(encoding='utf-8'), 'html.parser')
out = BeautifulSoup('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Silent Spies: How Do Your Devices Watch You?</title></head><body><article data-reader-content></article></body></html>', 'html.parser')
article = out.article
h1 = out.new_tag('h1', id='book-title')
h1.string = 'Silent Spies: How Do Your Devices Watch You?'
article.append(h1)
headings = {
    8: ('Introduction', 1),
    12: ('Chapter 1 — Whispers from Your Pocket: When Phones Listen without You Knowing', 2),
    18: ('Chapter 2 — The Silent Network: How Devices Communicate through Wi-Fi without You Knowing', 2),
    24: ('Chapter 3 — Who’s Really Listening? How Companies Use Your Data', 2),
    30: ('Chapter 4 — Who Holds the Remote? How to Take Control of Your Data', 2),
    36: ('Conclusion — Taking Back Control in a Connected World', 2),
    48: ('Bibliography', 1),
}
keep_pages = list(range(8, 42)) + [48, 49]
sections = []
for page in keep_pages:
    sec = draft.select_one(f'section[data-source-page="{page}"]')
    assert sec, page
    paragraphs = sec.find_all('p', recursive=False)
    if page in headings:
        label, skip = headings[page]
        heading = out.new_tag('h2', id=f'chapter-{len(sections)+1}' if page != 48 else 'bibliography')
        heading.string = label
        article.append(heading)
        sections.append({'id': heading['id'], 'title': label, 'page': page})
        paragraphs = paragraphs[skip:]
    for source_p in paragraphs:
        text = re.sub(r'\s+', ' ', source_p.get_text(' ', strip=True))
        if not text or re.fullmatch(r'\d+', text):
            continue
        paragraph = out.new_tag('p')
        paragraph.string = text
        article.append(paragraph)

for paragraph in list(article.find_all('p', recursive=False)):
    previous = paragraph.find_previous_sibling()
    if previous and previous.name == 'p':
        left = previous.get_text(' ', strip=True)
        right = paragraph.get_text(' ', strip=True)
        if left and right and not re.search(r'[.!?:;”"\)]$', left) and re.match(r'^[a-z]', right):
            previous.string = left + ' ' + right
            paragraph.decompose()

assert len(sections) == 7
assert not any(word in article.get_text(' ', strip=True).lower() for word in ('outfinitygift', 'outfinity srl', 'about ai author'))
(root / 'book/en/full_content.html').write_text(str(out) + '\n', encoding='utf-8')
(root / 'qa').mkdir(exist_ok=True)
(root / 'qa/source-selection.json').write_text(json.dumps({
    'source': 'income/Silent_Spies___How_Your_Watch_You/content.pdf',
    'retainedPdfPages': keep_pages,
    'excludedPdfPages': list(range(1, 8)) + list(range(42, 48)),
    'reason': 'Retain thematic introduction, four content chapters, conclusion and bibliography; remove retired rights, TOC, promotional preface and old-project annexes. Omit unrelated template words before chapter-one title.',
    'sections': sections,
    'readerWords': len(article.get_text(' ', strip=True).split()),
}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Prepared original reader:', len(article.get_text(' ', strip=True).split()), 'words')
