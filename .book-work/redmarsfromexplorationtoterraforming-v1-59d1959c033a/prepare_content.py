import json
import re
from pathlib import Path

from bs4 import BeautifulSoup

root = Path(__file__).parent
source = Path('.book-work/income-pdf-candidates/59d1959c033a69d1/clean-draft.html')
draft = BeautifulSoup(source.read_text(encoding='utf-8'), 'html.parser')
out = BeautifulSoup(
    '<!doctype html><html lang="en"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1">'
    '<title>Red Mars: From Exploration to Terraforming</title></head>'
    '<body><article data-reader-content></article></body></html>',
    'html.parser',
)
article = out.article
title = out.new_tag('h1', id='book-title')
title.string = 'Red Mars: From Exploration to Terraforming'
article.append(title)
heads = {
    8: ('Introduction', 1),
    13: ('Chapter One — Solar System Colonization: What’s Next for Humanity?', 2),
    18: ('Chapter Two — Martian Civilization: The Foundations of a New Civilization', 2),
    24: ('Chapter Three — The Terraforming Debate', 2),
    31: ('Chapter Four — The Power of Corporations', 2),
    34: ('Chapter Five — The Earth–Mars Relationship', 2),
    41: ('Chapter Six — Key Events and Plot Summaries', 2),
    46: ('Conclusion', 1),
    54: ('Bibliography', 1),
}
kept = list(range(8, 48)) + [54]
sections = []
for page in kept:
    section = draft.select_one(f'section[data-source-page="{page}"]')
    assert section, page
    paragraphs = section.find_all('p', recursive=False)
    if page in heads:
        label, skip = heads[page]
        h = out.new_tag('h2', id='bibliography' if page == 54 else f'chapter-{len(sections)+1}')
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

# Rejoin paragraphs split by physical PDF page breaks, retaining genuine
# paragraph boundaries and the original prose.
for p in list(article.find_all('p', recursive=False)):
    prev = p.find_previous_sibling()
    if prev and prev.name == 'p':
        left, right = prev.get_text(' ', strip=True), p.get_text(' ', strip=True)
        if left and right and not re.search(r'[.!?:;”"\)]$', left) and re.match(r'^[a-z]', right):
            prev.string = left + ' ' + right
            p.decompose()

# The PDF extractor puts several chapter-six subsection labels in the same
# text block as their opening sentence. Restore their document hierarchy.
subsections = (
    'The Journey to Mars',
    'Establishing the First Martian Colony',
    'The Debate Over Terraforming',
    'Earth’s Corporate Involvement and Martian Resistance',
    'The Martian Revolution',
    'The Assassination of John Boone',
    'Aftermath and Seeds of Future Conflict',
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

# Reflow unusually large PDF text blocks at sentence boundaries for readable
# HTML and manageable translation segments, without rewriting source text.
for p in list(article.find_all('p', recursive=False)):
    value = p.get_text(' ', strip=True)
    if len(value.split()) <= 230:
        continue
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z“])', value)
    if len(sentences) < 3:
        continue
    groups = []
    group = []
    words = 0
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
assert len(body.split()) > 6000
assert not any(term in body.lower() for term in ('outfinitygift', 'outfinity srl', 'about ai author'))
target = root / 'book/en/full_content.html'
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(str(out) + '\n', encoding='utf-8')
(root / 'qa').mkdir(exist_ok=True)
(root / 'qa/source-selection.json').write_text(json.dumps({
    'source': 'income/Red_Mars__From_Exploration_to_Terraforming/content.pdf',
    'retainedPdfPages': kept,
    'excludedPdfPages': list(range(1, 8)) + list(range(48, 54)),
    'reason': 'Retain the introduction, six original chapters, conclusion, and bibliography; exclude old rights, promotional preface, contents, and former-project annex.',
    'sections': sections,
    'readerWords': len(body.split()),
}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Prepared original reader:', len(body.split()), 'words')
