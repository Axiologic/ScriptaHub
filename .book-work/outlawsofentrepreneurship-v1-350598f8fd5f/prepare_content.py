import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

root = Path(__file__).parent
draft = BeautifulSoup(Path('.book-work/income-pdf-candidates/350598f8fd5fd7fd/clean-draft.html').read_text(encoding='utf-8'), 'html.parser')
out = BeautifulSoup('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Outlaws of Entrepreneurship</title></head><body><article data-reader-content></article></body></html>', 'html.parser')
article = out.article
h1 = out.new_tag('h1', id='book-title')
h1.string = 'Outlaws of Entrepreneurship'
article.append(h1)
headings = {
    7: ('Chapter 1 — Fraud, Piracy, and Smuggling: The Shadow Entrepreneurs', 3),
    15: ('Chapter 2 — Subversive Entrepreneurs', 2),
    22: ('Chapter 3 — Whispers of Revolution: Quiet Innovators', 3),
    29: ('Chapter 4 — The Edge of Failure: Comebacks and Collapse', 3),
    35: ('Conclusion — Hope, Risk, and the Promise of Change', 3),
    48: ('Bibliography', 1),
}
keep_pages = list(range(7, 41)) + [48, 49]
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

assert len(sections) == 6
assert not any(word in article.get_text(' ', strip=True).lower() for word in ('outfinitygift', 'outfinity srl', 'about ai author'))
(root / 'book/en/full_content.html').write_text(str(out) + '\n', encoding='utf-8')
(root / 'qa').mkdir(exist_ok=True)
(root / 'qa/source-selection.json').write_text(json.dumps({
    'source': 'income/Outlaws_of_Entrepreneurship/content.pdf',
    'retainedPdfPages': keep_pages,
    'excludedPdfPages': list(range(1, 7)) + list(range(41, 48)),
    'reason': 'Keep four content chapters, conclusion and bibliography; remove retired rights, TOC, promotional preface and old-project annexes.',
    'sections': sections,
    'readerWords': len(article.get_text(' ', strip=True).split()),
}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Prepared original reader:', len(article.get_text(' ', strip=True).split()), 'words')
