import json
import re
from pathlib import Path

from bs4 import BeautifulSoup

root = Path(__file__).parent
draft = BeautifulSoup(Path('.book-work/income-pdf-candidates/4facfb157843d25e/clean-draft.html').read_text(encoding='utf-8'), 'html.parser')
out = BeautifulSoup(
    '<!doctype html><html lang="en"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1">'
    '<title>Star Wars Universe</title></head><body><article data-reader-content></article></body></html>',
    'html.parser',
)
article = out.article
title = out.new_tag('h1', id='book-title')
title.string = 'Star Wars Universe'
article.append(title)
heads = {
    8: ('Introduction', 1),
    11: ('Midichlorians and the Force: What Would It Mean for Humanity Today?', 1),
    16: ('The Force and Philosophy in Star Wars', 2),
    21: ('Anthropology and Society in a Galaxy Far, Far Away', 2),
    29: ('Science and Technology in the Star Wars Universe', 2),
    36: ('Key Sequences and Plot Summary', 2),
    43: ('The Legacy and Impact', 2),
    45: ('Conclusion', 1),
    53: ('Bibliography', 1),
}
kept = list(range(8, 47)) + [53]
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

# Several original scene labels are printed inline with their first sentence.
subsections = (
    'The Original Trilogy (Episodes IV-VI, 1977-1983)',
    'The Prequel Trilogy (Episodes I-III, 1999-2005)',
    'The Sequel Trilogy (Episodes VII-IX, 2015-2019)',
)
for p in list(article.find_all('p', recursive=False)):
    value = p.get_text(' ', strip=True)
    for label in subsections:
        if value.startswith(label + ' '):
            h = out.new_tag('h3')
            h.string = label
            p.insert_before(h)
            p.string = value[len(label):].strip()
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
    'source': 'income/Star_Wars_Universe/content.pdf',
    'retainedPdfPages': kept,
    'excludedPdfPages': list(range(1, 8)) + list(range(47, 53)),
    'reason': 'Preserve introduction, six source chapters, conclusion, and bibliography; remove old rights, promotional preface, contents, and former-project annex. Source misnumbers the fifth chapter as Four; headings use section titles without numbers.',
    'sections': sections,
    'readerWords': len(body.split()),
}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Prepared original reader:', len(body.split()), 'words')
