import json
import re
from pathlib import Path

from bs4 import BeautifulSoup

root = Path(__file__).parent
draft_path = next(Path('.book-work/income-pdf-candidates').glob('634628ba98d5*/clean-draft.html'))
draft = BeautifulSoup(draft_path.read_text(encoding='utf-8'), 'html.parser')
title_text = 'The Legend of Sleepy Hollow'
out = BeautifulSoup(
    '<!doctype html><html lang="en"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1">'
    f'<title>{title_text}</title>'
    '</head><body><article data-reader-content></article></body></html>',
    'html.parser',
)
article = out.article
title = out.new_tag('h1', id='book-title')
title.string = title_text
article.append(title)
byline = out.new_tag('p', id='byline')
byline.string = 'Washington Irving'
article.append(byline)
kept = list(range(22, 60))
sections = []
for page in kept:
    source = draft.select_one(f'section[data-source-page="{page}"]')
    assert source, page
    paragraphs = source.find_all('p', recursive=False)
    if page == 22:
        heading = out.new_tag('h2', id='the-tale')
        heading.string = 'Found among the papers of the late Diedrich Knickerbocker'
        article.append(heading)
        sections.append({'id': heading['id'], 'title': heading.get_text(), 'page': page})
        paragraphs = paragraphs[2:]
    if page == 58:
        heading = out.new_tag('h2', id='postscript')
        heading.string = 'Postscript'
        article.append(heading)
        sections.append({'id': heading['id'], 'title': heading.get_text(), 'page': page})
        paragraphs = paragraphs[1:]
    for source_p in paragraphs:
        value = re.sub(r'\s+', ' ', source_p.get_text(' ', strip=True))
        if not value or re.fullmatch(r'\d+', value):
            continue
        p = out.new_tag('p')
        p.string = value
        article.append(p)

for p in list(article.find_all('p', recursive=False)):
    prev = p.find_previous_sibling()
    if prev and prev.name == 'p' and prev.get('id') != 'byline':
        left, right = prev.get_text(' ', strip=True), p.get_text(' ', strip=True)
        if left and right and not re.search(r'[.!?:;”"\)]$', left) and re.match(r'^[a-z]', right):
            prev.string = left + ' ' + right
            p.decompose()

for p in list(article.find_all('p', recursive=False)):
    value = p.get_text(' ', strip=True)
    if len(value.split()) <= 230:
        continue
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z“])', value)
    if len(sentences) < 3:
        continue
    groups, group, words = [], [], 0
    for sentence in sentences:
        count = len(sentence.split())
        if group and words + count > 170:
            groups.append(' '.join(group))
            group, words = [], 0
        group.append(sentence)
        words += count
    if group:
        groups.append(' '.join(group))
    if len(groups) > 1:
        for group_text in groups:
            node = out.new_tag('p')
            node.string = group_text
            p.insert_before(node)
        p.decompose()

body = article.get_text(' ', strip=True)
assert len(body.split()) > 6000
assert not any(term in body.lower() for term in ('outfinitygift', 'outfinity srl', 'about ai author'))
target = root / 'book/en/full_content.html'
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(str(out) + '\n', encoding='utf-8')
(root / 'qa').mkdir(exist_ok=True)
(root / 'qa/source-selection.json').write_text(json.dumps({
    'source': 'income/The_Legend_of_Sleepy_Hollow/content.pdf',
    'retainedPdfPages': kept,
    'excludedPdfPages': list(range(1, 22)) + list(range(60, 64)),
    'reason': 'Retain Washington Irving’s original tale and postscript; remove added AI preface, plot analysis and former-project promotional annex.',
    'sections': sections,
    'readerWords': len(body.split()),
}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Prepared original reader:', len(body.split()), 'words')
