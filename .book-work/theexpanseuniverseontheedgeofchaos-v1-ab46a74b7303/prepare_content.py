import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

root = Path('.book-work/theexpanseuniverseontheedgeofchaos-v1-ab46a74b7303')
source = Path('.book-work/income-pdf-candidates/ab46a74b7303fc35/clean-draft.html')
target = root / 'book/en/full_content.html'
draft = BeautifulSoup(source.read_text(encoding='utf-8'), 'html.parser')
out = BeautifulSoup('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>The Expanse Universe: On the Edge of Chaos</title></head><body><article data-reader-content></article></body></html>', 'html.parser')
article = out.article
h1 = out.new_tag('h1', id='book-title')
h1.string = 'The Expanse Universe: On the Edge of Chaos'
article.append(h1)

keep_pages = list(range(11, 41)) + [47]
sections = []
chapter = 0
await_title = False
for page in keep_pages:
    sec = draft.select_one(f'section[data-source-page="{page}"]')
    assert sec, page
    for source_p in sec.find_all('p', recursive=False):
        text = re.sub(r'\s+', ' ', source_p.get_text(' ', strip=True))
        if not text or re.fullmatch(r'\d+', text):
            continue
        if re.fullmatch(r'Chapter (One|Two|Three|Four|Five)', text):
            chapter += 1
            await_title = True
            continue
        if await_title:
            heading = out.new_tag('h2', id=f'chapter-{chapter}')
            heading.string = f'Chapter {chapter} — {text}'
            article.append(heading)
            sections.append({'id': heading['id'], 'title': heading.string, 'page': page})
            await_title = False
            continue
        if text in {'Conclusion', 'Bibliography'}:
            heading = out.new_tag('h2', id=text.lower())
            heading.string = text
            article.append(heading)
            sections.append({'id': heading['id'], 'title': text, 'page': page})
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

for paragraph in list(article.find_all('p', recursive=False)):
    value = paragraph.get_text(' ', strip=True)
    if len(value.split()) <= 190:
        continue
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z“"\'])', value)
    groups = []
    current = []
    for sentence in sentences:
        if current and len((' '.join(current) + ' ' + sentence).split()) > 155:
            groups.append(' '.join(current))
            current = []
        current.append(sentence)
    if current:
        groups.append(' '.join(current))
    if len(groups) > 1:
        for text in groups:
            new = out.new_tag('p')
            new.string = text
            paragraph.insert_before(new)
        paragraph.decompose()

assert chapter == 5 and len(sections) == 7, sections
assert not any(word in article.get_text(' ', strip=True).lower() for word in ('outfinitygift', 'outfinity srl', 'about ai author'))
target.write_text(str(out) + '\n', encoding='utf-8')
(root / 'qa').mkdir(exist_ok=True)
(root / 'qa/source-selection.json').write_text(json.dumps({
    'source': 'income/The_Expanse_Universe___On_the_Edge_of_Chaos/content.pdf',
    'retainedPdfPages': keep_pages,
    'excludedPdfPages': list(range(1, 11)) + list(range(41, 47)),
    'reason': 'Retain five original analytical chapters, conclusion and bibliography; remove rights, TOC, promotional preface/introduction and legacy annexes.',
    'sections': sections,
    'readerWords': len(article.get_text(' ', strip=True).split()),
}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Prepared original reader,', len(article.get_text(' ', strip=True).split()), 'words')
