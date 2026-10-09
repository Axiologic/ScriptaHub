import json
import re
from pathlib import Path

from bs4 import BeautifulSoup

root = Path(__file__).parent
draft = BeautifulSoup(Path('.book-work/income-pdf-candidates/af5095401cffcdd4/clean-draft.html').read_text(encoding='utf-8'), 'html.parser')
out = BeautifulSoup(
    '<!doctype html><html lang="en"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1">'
    '<title>An Exploration of the Warhammer 40,000 Universe</title></head>'
    '<body><article data-reader-content></article></body></html>',
    'html.parser',
)
article = out.article
title = out.new_tag('h1', id='book-title')
title.string = 'An Exploration of the Warhammer 40,000 Universe'
article.append(title)
heads = {
    8: ('Introduction', 1),
    11: ('Chapter One — Eternal War, Humanity Lost?', 2),
    15: ('Chapter Two — The Major Powers of the 41st Millennium', 2),
    21: ('Chapter Three — Guardians of Humanity: Empire and Inquisition', 2),
    27: ('Chapter Four — Technology and Warfare in the 41st Millennium', 2),
    33: ('Chapter Five — Society and Culture in the Imperium', 2),
    38: ('Chapter Six — The Horus Heresy: The Defining Event of Warhammer 40K', 3),
    44: ('Conclusion', 1),
    53: ('Bibliography', 1),
}
kept = list(range(8, 46)) + [53]
sections = []
for page in kept:
    source = draft.select_one(f'section[data-source-page="{page}"]')
    assert source, page
    paragraphs = source.find_all('p', recursive=False)
    if page in heads:
        label, skip = heads[page]
        h = out.new_tag('h2', id='bibliography' if page == 53 else f'chapter-{len(sections)+1}')
        h.string = label
        article.append(h)
        sections.append({'id': h['id'], 'title': label, 'page': page})
        paragraphs = paragraphs[skip:]
    for source_p in paragraphs:
        value = re.sub(r'\s+', ' ', source_p.get_text(' ', strip=True))
        # The delivered PDF truncates this heading to "tus Administratum".
        # Restore a readable subject without supplying any missing claims.
        value = value.replace('tus Administratum. This vast bureaucracy manages', 'The Administratum, a vast bureaucracy, manages')
        if not value or re.fullmatch(r'\d+', value):
            continue
        p = out.new_tag('p')
        p.string = value
        article.append(p)

for p in list(article.find_all('p', recursive=False)):
    prev = p.find_previous_sibling()
    if prev and prev.name == 'p':
        left, right = prev.get_text(' ', strip=True), p.get_text(' ', strip=True)
        if left and right and not re.search(r'[.!?:;”"\)]$', left) and re.match(r'^[a-z]', right):
            prev.string = left + ' ' + right
            p.decompose()

for p in list(article.find_all('p', recursive=False)):
    prev = p.find_previous_sibling()
    if prev and prev.name == 'p' and prev.get_text(' ', strip=True).endswith('At his side were the') and p.get_text(' ', strip=True).startswith('Primarchs,'):
        prev.string = prev.get_text(' ', strip=True) + ' ' + p.get_text(' ', strip=True)
        p.decompose()

for p in list(article.find_all('p', recursive=False)):
    prev = p.find_previous_sibling()
    if prev and prev.name == 'p' and prev.get_text(' ', strip=True).endswith('across the') and p.get_text(' ', strip=True).startswith('Imperium.'):
        prev.string = prev.get_text(' ', strip=True) + ' ' + p.get_text(' ', strip=True)
        p.decompose()

subsections = (
    'The Great Crusade: Prelude to Disaster',
    'The Fall of Horus',
    'The Corruption Spreads',
    'The Betrayal at Isstvan',
    'Civil War Engulfs the Galaxy',
    'The Siege of Terra',
    "The Emperor's Sacrifice",
    'The Aftermath and Legacy',
)
for p in list(article.find_all('p', recursive=False)):
    value = p.get_text(' ', strip=True)
    for label in subsections:
        if value == label or value.startswith(label + ' '):
            h = out.new_tag('h3')
            h.string = label
            p.insert_before(h)
            rest = value[len(label):].strip()
            if rest:
                p.string = rest
            else:
                p.decompose()
            break

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
assert len(body.split()) > 5000
assert not any(term in body.lower() for term in ('outfinitygift', 'outfinity srl', 'about ai author'))
target = root / 'book/en/full_content.html'
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(str(out) + '\n', encoding='utf-8')
(root / 'qa').mkdir(exist_ok=True)
(root / 'qa/source-selection.json').write_text(json.dumps({
    'source': 'income/An_Exploration_of_the_Warhammer_40_000_Universe/content.pdf',
    'retainedPdfPages': kept,
    'excludedPdfPages': list(range(1, 8)) + list(range(46, 53)),
    'reason': 'Retain the six original chapters, introduction, conclusion and bibliography; remove old rights, promotional preface, contents and former-project annex.',
    'sections': sections,
    'readerWords': len(body.split()),
}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Prepared original reader:', len(body.split()), 'words')
