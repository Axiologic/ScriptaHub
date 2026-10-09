import json
import re
from pathlib import Path

from bs4 import BeautifulSoup

root = Path(__file__).parent
draft = BeautifulSoup(Path('.book-work/income-pdf-candidates/86510b6a89aafdbd/clean-draft.html').read_text(encoding='utf-8'), 'html.parser')
title_text = 'Unlocking Economic Solutions for Modern Crises: J. M. Keynes’ Theory'
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
    8: 'Introduction',
    15: 'Chapter I — Economics and the Employment Crisis: Pandemic Lessons',
    23: 'Chapter II — Demand Theory: Recovery from Recession',
    32: 'Chapter III — Money and Interest: The Engine of the Economy',
    41: 'Chapter IV — Government’s Role: Fiscal Policy for Recovery',
    51: 'Chapter V — The Legacy of Keynes: How His Ideas Shape the World',
    59: 'Conclusion — The Relevance of Keynes Today',
    76: 'Bibliography',
}
kept = list(range(8, 68)) + [76]
sections = []
for page in kept:
    source = draft.select_one(f'section[data-source-page="{page}"]')
    assert source, page
    paragraphs = source.find_all('p', recursive=False)
    if page in heads:
        label = heads[page]
        h = out.new_tag('h2', id='bibliography' if page == 76 else f'chapter-{len(sections)+1}')
        h.string = label
        article.append(h)
        sections.append({'id': h['id'], 'title': label, 'page': page})
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
    if prev and prev.name == 'p':
        left, right = prev.get_text(' ', strip=True), p.get_text(' ', strip=True)
        page_join = (left.endswith('financial bubbles') and right.startswith('(such as housing bubbles)')) or (left.endswith('another Great') and right.startswith('Depression, and without'))
        if left and right and (page_join or (not re.search(r'[.!?:;”"\)]$', left) and re.match(r'^[a-z]', right))):
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
    'source': 'income/Unlocking_Economic_Solutions_for_Modern_Crises___J_M_Keynes__Theory/content.pdf',
    'retainedPdfPages': kept,
    'excludedPdfPages': list(range(1, 8)) + list(range(68, 76)),
    'reason': 'Keep the original introduction, five chapters, conclusion and bibliography; remove old rights, promotional preface, contents and former-project annex.',
    'sections': sections,
    'readerWords': len(body.split()),
}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Prepared original reader:', len(body.split()), 'words')
