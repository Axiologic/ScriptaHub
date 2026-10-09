import json
import re
from pathlib import Path

from bs4 import BeautifulSoup

root = Path(__file__).parent
draft = BeautifulSoup(Path('.book-work/income-pdf-candidates/14d2c81bc33b6186/clean-draft.html').read_text(encoding='utf-8'), 'html.parser')
title_text = 'Salary or Servitude?'
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
    8: ('Chapter One — In Defense of the Status Quo', 2),
    13: ('Chapter Two — The Evolution of the Employee-Employer Relationship', 4),
    23: ('Chapter Three — Challenges of the Current System', 3),
    32: ('Chapter Four — Alternatives and Potential Innovations', 3),
    45: ('Chapter Five — Towards a New Paradigm', 2),
    56: ('Conclusion — Technology, Freedom, and the Future of Work', 3),
    68: ('Bibliography', 1),
}
kept = list(range(8, 61)) + [68, 69, 70]
sections = []
for page in kept:
    source = draft.select_one(f'section[data-source-page="{page}"]')
    assert source, page
    paragraphs = source.find_all('p', recursive=False)
    if page in heads:
        label, skip = heads[page]
        h = out.new_tag('h2', id='bibliography' if page == 68 else f'chapter-{len(sections)+1}')
        h.string = label
        article.append(h)
        sections.append({'id': h['id'], 'title': label, 'page': page})
        paragraphs = paragraphs[skip:]
    for source_p in paragraphs:
        value = re.sub(r'\s+', ' ', source_p.get_text(' ', strip=True))
        value = value.replace('hamster wheel But fear not', 'hamster wheel? But fear not')
        value = value.replace('slide’s s instead of stairs', 'slides instead of stairs')
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
    'source': 'income/Salary_or_Servitude/content.pdf',
    'retainedPdfPages': kept,
    'excludedPdfPages': list(range(1, 8)) + list(range(61, 68)),
    'reason': 'Keep the original five chapters, conclusion and bibliography; remove old rights, promotional preface, contents and former-project annex.',
    'sections': sections,
    'readerWords': len(body.split()),
}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Prepared original reader:', len(body.split()), 'words')
