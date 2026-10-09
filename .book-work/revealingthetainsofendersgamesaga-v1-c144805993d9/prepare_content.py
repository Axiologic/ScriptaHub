import json
import re
from pathlib import Path

from bs4 import BeautifulSoup

w = Path(__file__).resolve().parent
source = BeautifulSoup(Path('.book-work/income-pdf-candidates/c144805993d9bb87/clean-draft.html').read_text(), 'html.parser')
out = BeautifulSoup('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Revealing the Tains of Ender’s Game Saga</title></head><body><article data-reader-content></article></body></html>', 'html.parser')
a = out.article
h = out.new_tag('h1', id='book-title'); h.string = 'Revealing the Tains of Ender’s Game Saga'; a.append(h)
headings = {
    8: ('Introduction', 1),
    11: ('Chapter One — The Ender Effect: How a Sci-Fi Classic Shaped Popular Culture', 2),
    17: ('Chapter Two — Philosophical Ideas and Anthropological Perspectives', 2),
    21: ('Chapter Three — Scientific Concepts', 2),
    26: ('Chapter Four — The Architecture of Society', 2),
    31: ('Chapter Five — Leadership Principles Explored', 2),
    36: ('Chapter Six — Morality in Warfare and Psychological Impact', 2),
    43: ('Chapter Seven — Key Events and Plot Summary', 2),
    46: ("Chapter Eight — The Legacy’s Impact on Today's World", 2),
    52: ('Conclusion', 1),
    60: ('Bibliography', 1),
}
kept = list(range(8, 54)) + [60]
sections = []
for page in kept:
    s = source.select_one(f'section[data-source-page="{page}"]')
    assert s, page
    paragraphs = s.find_all('p', recursive=False)
    if page in headings:
        label, skip = headings[page]
        h = out.new_tag('h2', id='bibliography' if page == 60 else f'chapter-{len(sections)+1}')
        h.string = label; a.append(h)
        sections.append({'id': h['id'], 'title': label, 'page': page})
        paragraphs = paragraphs[skip:]
    for source_p in paragraphs:
        value = re.sub(r'\s+', ' ', source_p.get_text(' ', strip=True))
        if not value or re.fullmatch(r'\d+', value): continue
        p = out.new_tag('p'); p.string = value; a.append(p)

for p in list(a.find_all('p', recursive=False)):
    prev = p.find_previous_sibling()
    if prev and prev.name == 'p':
        left, right = prev.get_text(' ', strip=True), p.get_text(' ', strip=True)
        if left and right and not re.search(r'[.!?:;”"\)]$', left) and re.match(r'^[a-z]', right):
            prev.string = left + ' ' + right; p.decompose()

# The delivered Chapter Seven uses inline labels for plot stages.
for p in list(a.find_all('p', recursive=False)):
    value = p.get_text(' ', strip=True)
    for label in ('Introduction to Ender Wiggin', 'Battle School and Training', 'Isolation and Leadership', 'The Formic War', 'The Final Battle', 'Aftermath and Redemption'):
        if value == label or value.startswith(label + ' '):
            h = out.new_tag('h3'); h.string = label; p.insert_before(h)
            rest = value[len(label):].strip()
            if rest: p.string = rest
            else: p.decompose()
            break

for p in list(a.find_all('p', recursive=False)):
    value = p.get_text(' ', strip=True)
    if len(value.split()) <= 230: continue
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z“])', value)
    groups, group, words = [], [], 0
    for sentence in sentences:
        count = len(sentence.split())
        if group and words + count > 170:
            groups.append(' '.join(group)); group, words = [], 0
        group.append(sentence); words += count
    if group: groups.append(' '.join(group))
    if len(groups) > 1:
        for chunk in groups:
            node = out.new_tag('p'); node.string = chunk; p.insert_before(node)
        p.decompose()

body = a.get_text(' ', strip=True)
assert len(body.split()) > 6000, len(body.split())
assert not any(s in body.lower() for s in ('outfinitygift', 'outfinity srl', 'about ai author'))
target = w / 'book/en/full_content.html'
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(str(out) + '\n')
qa = w / 'qa'; qa.mkdir(exist_ok=True)
(qa / 'source-selection.json').write_text(json.dumps({
    'source': 'income/Revealing_the_Tains_of_Ender_s_Game_Saga/content.pdf',
    'retainedPdfPages': kept,
    'excludedPdfPages': list(range(1,8)) + list(range(54,60)),
    'reason': 'Retain the original introduction, eight substantive chapters, conclusion and bibliography; exclude retired rights, promotional preface, contents and former-project annex.',
    'sections': sections, 'readerWords': len(body.split()),
}, ensure_ascii=False, indent=2) + '\n')
print('Prepared', len(body.split()), 'words')
