import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

root = Path(__file__).parent
source = Path('.book-work/income-pdf-candidates/5952af7eae3a373a/clean-draft.html')
target = root / 'book/en/full_content.html'
draft = BeautifulSoup(source.read_text(encoding='utf-8'), 'html.parser')
out = BeautifulSoup('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>A Cheeky Guide to Ancient Greek Philosophy</title></head><body><article data-reader-content></article></body></html>', 'html.parser')
article = out.article
h1 = out.new_tag('h1', id='book-title')
h1.string = 'A Cheeky Guide to Ancient Greek Philosophy'
article.append(h1)

keep_pages = list(range(10, 50))
sections = []
chapter = 0
for page in keep_pages:
    sec = draft.select_one(f'section[data-source-page="{page}"]')
    assert sec, page
    for source_p in sec.find_all('p', recursive=False):
        text = re.sub(r'\s+', ' ', source_p.get_text(' ', strip=True))
        if not text or re.fullmatch(r'\d+', text):
            continue
        if text.startswith('Chapter ') or text.startswith('Conclusion What Have We Learned?'):
            chapter += 1
            heading = out.new_tag('h2', id=f'chapter-{chapter}')
            heading.string = text.replace('Chapter One ', 'Chapter 1 — ').replace('Chapter Two ', 'Chapter 2 — ').replace('Chapter Three ', 'Chapter 3 — ').replace('Chapter Four ', 'Chapter 4 — ').replace('Conclusion What Have We Learned?', 'Conclusion — What Have We Learned?')
            article.append(heading)
            sections.append({'id': heading['id'], 'title': heading.string, 'page': page})
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

assert chapter == 5, sections
assert not any(word in article.get_text(' ', strip=True).lower() for word in ('outfinitygift', 'outfinity srl', 'about ai author'))
target.write_text(str(out) + '\n', encoding='utf-8')
(root / 'qa').mkdir(exist_ok=True)
(root / 'qa/source-selection.json').write_text(json.dumps({
    'source': 'income/A_Cheeky_Guide_to_Ancient_Greek_Philosophy/content.pdf',
    'retainedPdfPages': keep_pages,
    'excludedPdfPages': list(range(1, 10)) + list(range(50, 59)),
    'reason': 'Retain four original chapters and their conclusion; remove former rights, TOC, project preface and old-project annexes.',
    'sections': sections,
    'readerWords': len(article.get_text(' ', strip=True).split()),
}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Prepared original reader,', len(article.get_text(' ', strip=True).split()), 'words')
