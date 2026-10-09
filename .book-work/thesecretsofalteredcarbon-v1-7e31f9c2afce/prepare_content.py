import json
import re
from pathlib import Path

from bs4 import BeautifulSoup

root = Path(__file__).parent
draft = BeautifulSoup(Path('.book-work/income-pdf-candidates/7e31f9c2afce6582/clean-draft.html').read_text(encoding='utf-8'), 'html.parser')
out = BeautifulSoup(
    '<!doctype html><html lang="en"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1">'
    '<title>The Secrets of Altered Carbon</title></head>'
    '<body><article data-reader-content></article></body></html>',
    'html.parser',
)
article = out.article
title = out.new_tag('h1', id='book-title')
title.string = 'The Secrets of Altered Carbon'
article.append(title)
heads = {
    7: ('Introduction', 1),
    10: ('Chapter One — The Silent Reaper: Unraveling the Enigma of the Rawling Virus', 2),
    13: ('Chapter Two — The Concept of Digital Immortality', 2),
    20: ('Chapter Three — Philosophical Implications of Mind-Body Separation', 2),
    27: ('Chapter Four — Anthropological Perspectives on Identity and Consciousness', 2),
    34: ('Chapter Five — The Role of Science and Technology', 2),
    41: ('Chapter Six — Societal Structure and Inequality', 2),
    47: ('Chapter Seven — Ethics and Morality in a Post-Death World', 2),
    54: ('Chapter Eight — Key Sequences and Plot Summary', 2),
    58: ('Conclusion', 1),
    65: ('Bibliography', 1),
}
kept = list(range(7, 59)) + [65]
sections = []
for page in kept:
    source = draft.select_one(f'section[data-source-page="{page}"]')
    assert source, page
    paragraphs = source.find_all('p', recursive=False)
    if page in heads:
        label, skip = heads[page]
        h = out.new_tag('h2', id='bibliography' if page == 65 else f'chapter-{len(sections)+1}')
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

subsections = (
    'Takeshi Kovacs’ Re-Sleeving',
    "Flashbacks to Kovacs' Past",
    'Revealing the Role of the Envoys',
    'Fight Against Corruption and the Meth Elite',
    'Final Moral Choice',
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

# The delivered page stops mid-word after “internal conflic” before a new
# subsection heading. Keep its complete sentences and do not invent an ending.
for p in article.find_all('p', recursive=False):
    value = p.get_text(' ', strip=True)
    if value.endswith("becomes a critical theme in Kovacs' internal conflic"):
        p.string = value[:value.rfind(' Quell’s philosophy,')]

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
    'source': 'income/The_Secrets_of_Altered_Carbon/content.pdf',
    'retainedPdfPages': kept,
    'excludedPdfPages': list(range(1, 7)) + list(range(59, 65)),
    'reason': 'Preserve introduction, eight original chapters, conclusion and bibliography; remove old rights, promotional preface, contents and former-project annex.',
    'sections': sections,
    'readerWords': len(body.split()),
}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Prepared original reader:', len(body.split()), 'words')
