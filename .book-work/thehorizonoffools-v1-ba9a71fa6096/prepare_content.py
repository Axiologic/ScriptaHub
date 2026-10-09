import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

root = Path('.book-work/thehorizonoffools-v1-ba9a71fa6096')
source = Path('.book-work/income-pdf-candidates/ba9a71fa6096a8f2/clean-draft.html')
target = root / 'book/en/full_content.html'
draft = BeautifulSoup(source.read_text(encoding='utf-8'), 'html.parser')
out = BeautifulSoup('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>The Horizon of Fools</title></head><body><article data-reader-content></article></body></html>', 'html.parser')
article = out.article
h1 = out.new_tag('h1', id='book-title')
h1.string = 'The Horizon of Fools'
article.append(h1)

keep_pages = list(range(10, 45))
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

assert chapter == 5 and len(sections) == 5, sections
assert not any(word in article.get_text(' ', strip=True).lower() for word in ('outfinitygift', 'outfinity srl', 'about ai author'))
target.write_text(str(out) + '\n', encoding='utf-8')
(root / 'qa').mkdir(exist_ok=True)
(root / 'qa/source-selection.json').write_text(json.dumps({
    'source': 'income/The_Horizon_of_Fools/content.pdf',
    'retainedPdfPages': keep_pages,
    'excludedPdfPages': list(range(1, 10)) + list(range(45, 51)),
    'reason': 'Retain all five original fiction chapters; remove rights, TOC, promotional preface/introduction and old-project annexes.',
    'sections': sections,
    'readerWords': len(article.get_text(' ', strip=True).split()),
}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Prepared original reader,', len(article.get_text(' ', strip=True).split()), 'words')
