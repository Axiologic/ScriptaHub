import json
import re
from pathlib import Path

from bs4 import BeautifulSoup

root = Path(__file__).parent
draft_path = next(Path('.book-work/income-pdf-candidates').glob('3cd052cdecba*/clean-draft.html'))
draft = BeautifulSoup(draft_path.read_text(encoding='utf-8'), 'html.parser')
title_text = 'Inventors & Ideas: For Curious Kids, Big and Small'
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
heads = {
    9: ('Chapter One — Accidental Genius', 2),
    25: ('Chapter Two — Nature’s Blueprints: Inventions from the Wild', 3),
    50: ('Chapter Three — Unsung Inventors', 2),
    63: ('Chapter Four — The Architects of Tomorrow', 2),
    77: ('Final Words', 1),
    87: ('Bibliography', 1),
}
kept = list(range(9, 79)) + [87, 88]
sections = []
for page in kept:
    source = draft.select_one(f'section[data-source-page="{page}"]')
    assert source, page
    paragraphs = source.find_all('p', recursive=False)
    if page in heads:
        label, skip = heads[page]
        h = out.new_tag('h2', id='bibliography' if page == 87 else f'section-{len(sections)+1}')
        h.string = label
        article.append(h)
        sections.append({'id': h['id'], 'title': label, 'page': page})
        paragraphs = paragraphs[skip:]
    for source_p in paragraphs:
        value = re.sub(r'\s+', ' ', source_p.get_text(' ', strip=True))
        value = value.replace('history books..', 'history books.')
        if (page == 72 and (value.startswith('Shimon Whiteson: Reinforcement Learning Expert') or value.startswith('Timnit Gebru, a prominent researcher in AI ethics'))) or (page == 73 and value.startswith('AI systems, making her a key figure')):
            continue
        if not value or re.fullmatch(r'\d+', value):
            continue
        p = out.new_tag('p')
        p.string = value
        article.append(p)

for p in list(article.find_all('p', recursive=False)):
    prev = p.find_previous_sibling()
    if prev and prev.name == 'p':
        left, right = prev.get_text(' ', strip=True), p.get_text(' ', strip=True)
        bibliography_join = left.endswith('The Invisible Gorilla: How Our Intuitions Deceive') and right.startswith('Us. Crown Publishing, 2010.')
        heading_join = (left.endswith('Margaret Knight: The Woman Who Made Flat-Bottomed Paper') and right == 'Bags') or (left.endswith('Emmett Chappelle: Advancing Bioluminescence and Space') and right == 'Exploration')
        if left and right and (bibliography_join or heading_join or (not re.search(r'[.!?:;”"\)]$', left) and re.match(r'^[a-z]', right))):
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
assert len(body.split()) > 7000
assert not any(term in body.lower() for term in ('outfinitygift', 'outfinity srl', 'about ai author'))
target = root / 'book/en/full_content.html'
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(str(out) + '\n', encoding='utf-8')
(root / 'qa').mkdir(exist_ok=True)
(root / 'qa/source-selection.json').write_text(json.dumps({
    'source': 'income/Inventors___Ideas__For_Curious_Kids__Big_and_Small/content.pdf',
    'retainedPdfPages': kept,
    'excludedPdfPages': list(range(1, 9)) + list(range(79, 87)),
    'reason': 'Keep the four original chapters, final words and bibliography; remove the promotional preface, rights and former-project annex.',
    'sourceDefects': ['PDF page 72 labels a paragraph about Timnit Gebru as Shimon Whiteson and repeats her page-67 biography; omit the orphan heading and repeated text through the page-73 continuation.', 'Join headings split across two paragraphs for Margaret Knight and Emmett Chappelle; correct the doubled terminal period in the Otis Boykin paragraph.', 'Rejoin the bibliography title split between source pages 87 and 88.'],
    'sections': sections,
    'readerWords': len(body.split()),
}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Prepared original reader:', len(body.split()), 'words')
