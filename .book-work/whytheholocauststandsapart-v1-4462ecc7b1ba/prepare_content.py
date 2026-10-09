"""Select the authored preface and six chapters; exclude rights and old-project annexes."""

import json
import re
from pathlib import Path

from bs4 import BeautifulSoup

root = Path(__file__).resolve().parent
source = Path('.book-work/income-pdf-candidates/4462ecc7b1ba7ec9/clean-draft.html')
draft = BeautifulSoup(source.read_text(encoding='utf-8'), 'html.parser')
out = BeautifulSoup('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Why the Holocaust Stands Apart</title></head><body><article data-reader-content></article></body></html>', 'html.parser')
article = out.article
h = out.new_tag('h1', id='book-title')
h.string = 'Why the Holocaust Stands Apart'
article.append(h)

chapters = {
 7: 'Chapter One — The Major Genocides of History',
 49: 'Chapter Two — European History, Values, and the Risk of Genocide',
 56: 'Chapter Three — Colonialism and Genocidal Practices',
 65: 'Chapter Four — The Holocaust: A Case Apart',
 74: 'Chapter Five — Theories Behind the Holocaust’s Unique PR',
 82: 'Chapter Six — Lessons, Memory, and Global Responsibility',
}
kept = list(range(5, 90))
sections = []
for page in kept:
    sec = draft.select_one(f'section[data-source-page="{page}"]')
    assert sec is not None, page
    parts = [re.sub(r'\s+', ' ', p.get_text(' ', strip=True)).strip() for p in sec.find_all('p', recursive=False)]
    parts = [p for p in parts if p and not re.fullmatch(r'\d+', p)]
    if page == 5:
        assert parts.pop(0) == 'Preface'
        title = 'Preface'
    elif page in chapters:
        raw = parts.pop(0)
        assert raw == f'Chapter {"One Two Three Four Five Six".split()[list(chapters).index(page)]}', (page, raw)
        raw_sub = parts.pop(0)
        assert raw_sub == chapters[page].split(' — ', 1)[1], (page, raw_sub)
        title = chapters[page]
    else:
        title = None
    if title:
        node = out.new_tag('h2', id=f'section-{len(sections)+1}')
        node.string = title
        article.append(node)
        sections.append({'id': node['id'], 'title': title, 'sourcePage': page})
    for value in parts:
        p = out.new_tag('p')
        p.string = value
        article.append(p)

# The extraction records paragraph continuations across page boundaries.
# Join those continuations, never crossing a chapter heading.
for p in list(article.find_all('p', recursive=False)):
    previous = p.find_previous_sibling()
    if previous and previous.name == 'p':
        left = previous.get_text(' ', strip=True)
        right = p.get_text(' ', strip=True)
        if left and right and (not re.search(r'[.!?:;”"’\)]$', left) or re.match(r'^[a-z]', right)):
            previous.string = left + ' ' + right
            p.decompose()

for p in list(article.find_all('p', recursive=False)):
    value = p.get_text(' ', strip=True)
    if len(value.split()) <= 190:
        continue
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z“‘])', value)
    if len(sentences) < 3:
        continue
    groups, group, words = [], [], 0
    for sentence in sentences:
        count = len(sentence.split())
        if group and words + count > 145:
            groups.append(' '.join(group))
            group, words = [], 0
        group.append(sentence)
        words += count
    if group:
        groups.append(' '.join(group))
    if len(groups) > 1:
        for value in groups:
            node = out.new_tag('p')
            node.string = value
            p.insert_before(node)
        p.decompose()

body = article.get_text(' ', strip=True)
assert len(body.split()) > 17000, len(body.split())
assert len(article.find_all('h2')) == 7
assert not any(x in body.lower() for x in ('outfinity', 'about ai authour', 'outfinitygift'))
target = root / 'book/en/full_content.html'
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(str(out) + '\n', encoding='utf-8')
qa = root / 'qa'
qa.mkdir(exist_ok=True)
(qa / 'source-selection.json').write_text(json.dumps({
 'source': 'income/Why_the_Holocaust_Stands_Apart/content.pdf',
 'retainedPdfPages': kept,
 'excludedPdfPages': list(range(1, 5)) + list(range(90, 96)),
 'reason': 'Retain the substantive authored preface and all six chapters. Exclude title/rights/contents and the retired-project author advertisement and OutfinityGift letter.',
 'sections': sections,
 'readerWords': len(body.split()),
}, ensure_ascii=False, indent=2) + '\n')
print('Prepared', len(body.split()), 'words in', len(sections), 'sections')
