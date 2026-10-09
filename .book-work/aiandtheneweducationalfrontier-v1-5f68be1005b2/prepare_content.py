import json
import re
import subprocess
from pathlib import Path

from bs4 import BeautifulSoup


root = Path(__file__).parent
source = Path('income/AI_and_the_New_Educational_Frontier/content.pdf')
out = BeautifulSoup(
    '<!doctype html><html lang="en"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1">'
    '<title>AI and the New Educational Frontier</title></head>'
    '<body><article data-reader-content></article></body></html>',
    'html.parser',
)
article = out.article
h1 = out.new_tag('h1', id='book-title')
h1.string = 'AI and the New Educational Frontier'
article.append(h1)

chapters = {
    9: ('Chapter I — The State of Education Today', 2),
    46: ("Chapter II — Personalized Education: AI's Role in Shaping Learning", 3),
    55: ('Chapter III — Social Stratification in Education', 2),
    82: ('Chapter IV — Preparing Young Minds for a Complex Future', 3),
    96: ('Chapter V — Early Childhood Education: Planting Seeds of Wisdom', 3),
    109: ('Chapter VI — Primary and Secondary Education: Building Resilient Minds', 3),
    134: ('Chapter VII — Higher Education: Balancing Knowledge and Social Responsibility', 4),
    169: ('Chapter VIII — Vocational Training and the New Labor Economy', 3),
    181: ('Chapter IX — Education for Cognitive Elites and Societal Leaders', 3),
    206: ('Chapter X — Philosophical Education: Wisdom as a Societal Imperative', 2),
    218: ('Conclusion', 1),
}
raw = subprocess.run(
    ['pdftotext', '-f', '9', '-l', '221', '-layout', str(source), '-'],
    capture_output=True, text=True, check=True,
).stdout.split('\f')
assert len(raw) >= 213

def page_blocks(page_text):
    blocks = []
    current = []
    for line in page_text.splitlines():
        if re.fullmatch(r'\s*\d+\s*', line):
            continue
        if not line.strip():
            if current:
                blocks.append(' '.join(current))
                current = []
            continue
        stripped = line.strip()
        indent = len(line) - len(line.lstrip(' '))
        if indent >= 5 and current:
            blocks.append(' '.join(current))
            current = []
        if current and current[-1].endswith('-') and stripped[0].islower():
            current[-1] = current[-1] + stripped
        else:
            current.append(stripped)
    if current:
        blocks.append(' '.join(current))
    return [re.sub(r'\s+', ' ', block).strip() for block in blocks]

sections = []
for page in range(9, 222):
    paragraphs = page_blocks(raw[page - 9])
    assert paragraphs, page
    if page in chapters:
        title, drop = chapters[page]
        heading = out.new_tag('h2', id='conclusion' if page == 218 else f'chapter-{len(sections)+1}')
        heading.string = title
        article.append(heading)
        sections.append({'id': heading['id'], 'title': title, 'pdfPage': page})
        assert paragraphs[0].startswith('Chapter') if page != 218 else paragraphs[0] == 'Conclusion'
        if page != 218:
            label = title.split(' — ', 1)[1]
            assert ' '.join(paragraphs[1:drop]) == label, (page, paragraphs[:drop], label)
        if page == 109:
            assert paragraphs[1:3] == ['Primary and Secondary Education:', 'Building Resilient Minds']
        if page == 206:
            assert paragraphs[:2] == ['Chapter X', 'Philosophical Education: Wisdom as a Societal Imperative']
        paragraphs = paragraphs[drop:]
    for value in paragraphs:
        if not value:
            continue
        p = out.new_tag('p')
        p.string = value
        p['data-source-page'] = str(page)
        article.append(p)

# Source pagination sometimes divides one sentence into two paragraphs.
joins = []
for p in list(article.find_all('p', recursive=False)):
    previous = p.find_previous_sibling()
    if previous and previous.name == 'p' and previous.get('data-source-page') != p.get('data-source-page'):
        left = previous.get_text(' ', strip=True)
        right = p.get_text(' ', strip=True)
        if left and right and not re.search(r'[.!?:;”"\)\]]$', left) and re.match(r'^[a-z]', right):
            joins.append({'fromPage': int(previous['data-source-page']), 'toPage': int(p['data-source-page']), 'left': left[-70:], 'right': right[:70]})
            previous.string = left + ('-' if left.endswith('-') else ' ') + right
            if left.endswith('-'):
                previous.string = left[:-1] + right
            p.decompose()

for p in article.find_all('p'):
    p.attrs.pop('data-source-page', None)

text = article.get_text(' ', strip=True)
assert len(sections) == 11
assert len(text.split()) > 45000
assert 'OutfinityGift' not in text and 'outfinitygift.com' not in text
assert text.rstrip().endswith('compassionate, and enlightened world.')
target = root / 'book/en/full_content.html'
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(str(out) + '\n', encoding='utf-8')
qa = root / 'qa'
qa.mkdir(exist_ok=True)
(qa / 'source-selection.json').write_text(json.dumps({
    'source': 'income/AI_and_the_New_Educational_Frontier/content.pdf',
    'retainedPdfPages': list(range(9, 222)),
    'excludedPdfPages': list(range(1, 9)) + list(range(222, 228)),
    'reason': 'Keep ten original chapters and conclusion; omit title artwork page, old rights, duplicate contents and promotional preface, plus former-project self-description and promotional letter in annexes.',
    'chapters': sections,
    'pageBoundaryJoins': joins,
    'readerWords': len(text.split()),
}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(len(text.split()), 'words', len(sections), 'sections', len(joins), 'page joins')
