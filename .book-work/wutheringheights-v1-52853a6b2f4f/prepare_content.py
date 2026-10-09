"""Select Emily Brontë's original novel from the supplied annotated PDF."""
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

root = Path(__file__).resolve().parent
source = BeautifulSoup(Path('.book-work/income-pdf-candidates/52853a6b2f4f66ff/source-draft.html').read_text(), 'html.parser')
out = BeautifulSoup('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Wuthering Heights</title></head><body><article data-reader-content></article></body></html>', 'html.parser')
article = out.article
title = out.new_tag('h1', id='book-title'); title.string = 'Wuthering Heights'; article.append(title)
author = out.new_tag('p', attrs={'class': 'book-byline'}); author.string = 'Emily Brontë'; article.append(author)

chapters = []
fragments = []
for page in range(23, 407):
    section = source.select_one(f'section[data-source-page="{page}"]')
    assert section is not None, page
    blocks = [re.sub(r'\s+', ' ', p.get_text(' ', strip=True)).strip() for p in section.find_all('p', recursive=False)]
    blocks = [value for value in blocks if value and value != str(page)]
    if blocks and re.fullmatch(r'CHAPTER [IVXLCDM]+', blocks[0]):
        chapter = blocks.pop(0)
        chapters.append({'sourcePage': page, 'label': chapter, 'id': chapter.lower().replace(' ', '-')})
    assert blocks, page
    for value in blocks:
        fragments.append((page, value))

assert len(chapters) == 34, len(chapters)
# The source's page-break text fragments are joined only when the preceding
# fragment is an unfinished sentence or the next fragment starts in lower case.
paragraphs = []
joins = []
for page, value in fragments:
    if paragraphs and paragraphs[-1][1] == page - 1 and (
        not re.search(r'[.!?…][”’\)]?$', paragraphs[-1][0]) or re.match(r'^[a-z]', value)
    ):
        previous, before = paragraphs.pop()
        paragraphs.append((previous + ' ' + value, page))
        joins.append({'fromPage': before, 'toPage': page, 'leftEnd': previous[-65:], 'rightStart': value[:65]})
    else:
        paragraphs.append((value, page))

by_page = {}
for value, page in paragraphs:
    by_page.setdefault(page, []).append(value)
by_heading_page = {chapter['sourcePage']: chapter for chapter in chapters}
for page in range(23, 407):
    chapter = by_heading_page.get(page)
    if chapter:
        h = out.new_tag('h2', id=chapter['id'])
        # Preserve the Roman numeral exactly; titlecase only the word.
        h.string = 'Chapter ' + chapter['label'].split(' ', 1)[1]
        article.append(h)
    for value in by_page.get(page, []):
        # Keep the original wording while avoiding multi-page, multi-thousand-
        # word paragraphs that would make translation chunks unmanageable.
        sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z“‘])', value)
        group = []
        count = 0
        for sentence in sentences:
            words = len(sentence.split())
            if group and count + words > 145:
                p = out.new_tag('p'); p.string = ' '.join(group); article.append(p)
                group, count = [], 0
            group.append(sentence)
            count += words
        if group:
            p = out.new_tag('p'); p.string = ' '.join(group); article.append(p)

body = article.get_text(' ', strip=True)
assert len(body.split()) > 100000, len(body.split())
assert 'outfinitygift' not in body.casefold()
assert 'AI Agent Zira Luthor' not in body
target = root / 'book/en/full_content.html'
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(str(out) + '\n')
qa = root / 'qa'; qa.mkdir(exist_ok=True)
(qa / 'source-selection.json').write_text(json.dumps({
    'source': 'income/Wuthering_Heights/content.pdf',
    'retainedPdfPages': list(range(23, 407)),
    'excludedPdfPages': list(range(1, 23)) + list(range(407, 411)),
    'selection': 'Emily Brontë’s 34 original chapters only; omit former rights, preface, AI perspective, author commentary, plot summary, AI biography and former project letter.',
    'chapters': chapters,
    'pageBoundaryJoins': joins,
    'readerWords': len(body.split()),
}, ensure_ascii=False, indent=2) + '\n')
print(len(body.split()), 'words;', len(chapters), 'chapters;', len(joins), 'page joins')
