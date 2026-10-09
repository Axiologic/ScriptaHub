"""Select the edition's original narrative and substantive editorial perspective."""

import json
import re
from pathlib import Path

from bs4 import BeautifulSoup

root = Path(__file__).resolve().parent
draft = BeautifulSoup(
    Path('.book-work/income-pdf-candidates/59895dab5563de70/clean-draft.html').read_text(encoding='utf-8'),
    'html.parser',
)
out = BeautifulSoup(
    '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Alice’s Adventures in Wonderland</title></head><body><article data-reader-content></article></body></html>',
    'html.parser',
)
article = out.article
heading = out.new_tag('h1', id='book-title')
heading.string = 'Alice’s Adventures in Wonderland'
article.append(heading)

perspective = {
    6: 'About Lewis Carroll',
    9: 'Historical and Cultural Context',
    13: 'Main Characters',
    19: 'Plot Summary by Narrative Threads',
}
chapters = {
    25: 'Down the Rabbit-Hole',
    32: 'The Pool of Tears',
    39: 'A Caucus-Race and a Long Tale',
    46: 'The Rabbit Sends in a Little Bill',
    54: 'Advice from a Caterpillar',
    62: 'Pig and Pepper',
    71: 'A Mad Tea-Party',
    80: 'The Queen’s Croquet-Ground',
    89: 'The Mock Turtle’s Story',
    98: 'The Lobster Quadrille',
    107: 'Who Stole the Tarts?',
    114: 'Alice’s Evidence',
}
roman = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']
kept_pages = list(range(6, 24)) + list(range(25, 122))
sections = []

def add_heading(tag, text, page):
    identifier = f'section-{len(sections)+1}' if tag == 'h2' else f'subsection-{page}'
    element = out.new_tag(tag, id=identifier)
    element.string = text
    article.append(element)
    sections.append({'id': identifier, 'title': text, 'sourcePage': page})

for page in kept_pages:
    source = draft.select_one(f'section[data-source-page="{page}"]')
    assert source, page
    parts = [re.sub(r'\s+', ' ', p.get_text(' ', strip=True)).strip() for p in source.find_all('p', recursive=False)]
    parts = [p for p in parts if p and not re.fullmatch(r'\d+', p) and p != 'THE END']
    if not parts:
        assert page == 18, page  # Blank verso between editorial sections.
        continue
    if page == 6:
        add_heading('h2', 'AI Perspective', page)
        assert parts[0] == 'AI PERSPECTIVE About Lewis Carroll'
        parts.pop(0)
        add_heading('h3', perspective[page], page)
    elif page in perspective:
        label = perspective[page]
        assert parts[0].lower().startswith(label.lower()), (page, parts[0][:100])
        parts[0] = parts[0][len(label):].strip()
        add_heading('h3', label, page)
    elif page in chapters:
        position = list(chapters).index(page)
        title = f'Chapter {roman[position]} — {chapters[page]}'
        add_heading('h2', title, page)
        prefix = f'CHAPTER {roman[position]} {chapters[page]}'
        assert parts[0].startswith(prefix), (page, parts[0][:100], prefix)
        parts[0] = parts[0][len(prefix):].strip()
    for value in parts:
        if not value:
            continue
        p = out.new_tag('p')
        p.string = value
        article.append(p)

# The PDF extractor creates one paragraph per page. Rejoin page continuations
# without crossing a chapter/perspective heading.
for p in list(article.find_all('p', recursive=False)):
    previous = p.find_previous_sibling()
    if previous and previous.name == 'p':
        left, right = previous.get_text(' ', strip=True), p.get_text(' ', strip=True)
        if left and right and (not re.search(r'[.!?:;”"’\)]$', left) or re.match(r'^[a-z]', right)):
            previous.string = left + ' ' + right
            p.decompose()

# Avoid page-sized blocks while retaining the source words and order.
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
        for piece in groups:
            node = out.new_tag('p')
            node.string = piece
            p.insert_before(node)
        p.decompose()

body = article.get_text(' ', strip=True)
assert len(body.split()) > 28000, len(body.split())
assert len(article.find_all('h2')) == 13
assert not any(term in body.lower() for term in ('outfinity', 'millennium fulcrum', 'about ai author'))

target = root / 'book/en/full_content.html'
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(str(out) + '\n', encoding='utf-8')
qa = root / 'qa'
qa.mkdir(exist_ok=True)
(qa / 'source-selection.json').write_text(json.dumps({
    'source': 'income/Alice_s_Adventures_in_Wonderland/content.pdf',
    'retainedPdfPages': kept_pages,
    'excludedPdfPages': list(range(1, 6)) + [24] + list(range(122, 126)),
    'reason': 'Retain Taler Vox’s substantive AI Perspective and all twelve chapters of Lewis Carroll’s original narrative. Exclude the rights page, table of contents, project-promotional preface, retired-edition title leaf and former-project annex.',
    'sections': sections,
    'readerWords': len(body.split()),
}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Prepared', len(body.split()), 'words in', len(sections), 'sections')
