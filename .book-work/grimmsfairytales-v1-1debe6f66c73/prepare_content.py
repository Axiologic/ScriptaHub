"""Extract only the Grimm tales from the delivered anthology."""
import json
import re
from pathlib import Path

from bs4 import BeautifulSoup

root = Path(__file__).resolve().parent
draft = BeautifulSoup(Path('.book-work/income-pdf-candidates/1debe6f66c7388b2/clean-draft.html').read_text(), 'html.parser')
out = BeautifulSoup('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Grimms’ Fairy Tales</title></head><body><article data-reader-content></article></body></html>', 'html.parser')
article = out.article
h1 = out.new_tag('h1', id='book-title'); h1.string = 'Grimms’ Fairy Tales'; article.append(h1)
by = out.new_tag('p'); by.string = 'Jacob Grimm and Wilhelm Grimm'; article.append(by)

def add_para(value):
    p = out.new_tag('p'); p.string = value; article.append(p)

headings = []
def add_heading(value, page, level=2):
    ident = f'tale-{len([h for h in headings if h["level"] == 2])+1}' if level == 2 else f'section-{len(headings)+1}'
    h = out.new_tag(f'h{level}', id=ident); h.string = value.title() if value.isupper() else value; article.append(h)
    headings.append({'id': ident, 'title': h.string, 'page': page, 'level': level})

inline_titles = {
    118: 'THE MOUSE, THE BIRD, AND THE SAUSAGE',
    120: 'MOTHER HOLLE',
    125: 'LITTLE RED-CAP [LITTLE RED RIDING HOOD]',
    321: 'CAT-SKIN',
}

for page in range(19, 335):
    section = draft.select_one(f'section[data-source-page="{page}"]')
    assert section is not None, page
    values = [re.sub(r'\s+', ' ', p.get_text(' ', strip=True)).strip() for p in section.find_all('p', recursive=False)]
    for value in values:
        if not value or re.fullmatch(r'\d+', value) or value == 'THE END':
            continue
        if page == 334 and 'The Brothers Grimm, Jacob' in value:
            value = value.split('The Brothers Grimm, Jacob', 1)[0].strip()
            assert value.endswith('white and red.'), value
        title = inline_titles.get(page)
        if title and value.startswith(title + ' '):
            add_heading(title, page)
            value = value[len(title):].strip()
        if value.isupper() and len(value) < 120:
            add_heading(value, page, 3 if re.match(r'^(?:\d+\.|FIRST STORY|SECOND STORY)', value) else 2)
        else:
            add_para(value)

# The source PDF cuts continuous prose at physical page edges. Join those
# paragraphs without crossing a tale heading; then split long units for review.
for node in list(article.find_all('p', recursive=False)):
    prev = node.find_previous_sibling()
    if prev is None or prev.name != 'p':
        continue
    left, right = prev.get_text(' ', strip=True), node.get_text(' ', strip=True)
    if left and right and (re.match(r'^[a-z]', right) or not re.search(r'[.!?:;”"’\)]$', left)):
        prev.string = left + ' ' + right
        node.decompose()

for node in list(article.find_all('p', recursive=False)):
    value = node.get_text(' ', strip=True)
    if len(value.split()) <= 180:
        continue
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z“‘])', value)
    if len(sentences) < 3:
        continue
    groups, current, words = [], [], 0
    for sentence in sentences:
        count = len(sentence.split())
        if current and words + count > 145:
            groups.append(' '.join(current)); current, words = [], 0
        current.append(sentence); words += count
    if current: groups.append(' '.join(current))
    if len(groups) > 1:
        for group in groups:
            p = out.new_tag('p'); p.string = group; node.insert_before(p)
        node.decompose()

body = article.get_text(' ', strip=True)
assert len(body.split()) > 80000, len(body.split())
assert len([h for h in headings if h['level'] == 2]) >= 50, len(headings)
assert not any(x in body.casefold() for x in ('outfinity', 'zira luthor', 'modern perspective', 'all rights reserved'))
target = root/'book/en/full_content.html'; target.parent.mkdir(parents=True, exist_ok=True); target.write_text(str(out)+'\n')
qa = root/'qa'; qa.mkdir(exist_ok=True)
(qa/'source-selection.json').write_text(json.dumps({
    'source': 'income/Grimms__Fairy_Tales/content.pdf',
    'retainedPdfPages': list(range(18,335)),
    'excludedPdfPages': list(range(1,18)) + list(range(335,339)),
    'reason': 'Retain the original title/credit and the tale anthology from The Golden Bird through Snow-White and Rose-Red. Exclude rights, duplicate contents, promotional preface, modern AI commentary, AI-author biography, and OutfinityGift annex.',
    'lastPageNote': 'Page 334 contains the final tale paragraph, a later biographical note in the same extracted paragraph, and THE END. The note is split off and excluded.',
    'emptySourcePages': [124,130],
    'sections': headings,
    'readerWords': len(body.split()),
}, ensure_ascii=False, indent=2)+'\n')
print(f'Prepared {len(body.split())} words; {len([h for h in headings if h["level"]==2])} tales; {len(headings)} headings')
