from collections import OrderedDict
from hashlib import sha256
from html import escape
from pathlib import Path
import json
import re
import subprocess

root = Path('.book-work/charlesdarwinarevolutionaryforceinscienceandsociety-v1-412e39743f82')
pdf = root / 'content.pdf'
pages = subprocess.check_output(['pdftotext', '-layout', str(pdf), '-']).decode().split('\f')
assert len(pages) - 1 == 49

sections = OrderedDict([
    (8, ('introduction', 'Introduction', 1)),
    (11, ('chapter-1', 'Chapter 1 — How Would Darwin Have Assessed Modern Biology?', 3)),
    (15, ('chapter-2', "Chapter 2 — Darwin's Path to the Beagle", 2)),
    (17, ('chapter-3', "Chapter 3 — Darwin's Beagle Expedition", 2)),
    (22, ('chapter-4', "Chapter 4 — Origins of Darwin's Theory", 2)),
    (25, ('chapter-5', 'Chapter 5 — Development of Evolutionary Theory', 2)),
    (29, ('chapter-6', "Chapter 6 — Darwin's Theory: Reshaping Thought and Society", 3)),
    (35, ('chapter-7', 'Chapter 7 — Technological Implications', 2)),
    (40, ('conclusion', 'Conclusion', 1)),
    (48, ('bibliography', 'Bibliography', 1)),
])

selected = list(range(8, 42)) + [48, 49]
blocks = []
current = []
for page_number in selected:
    if page_number in sections:
        if current:
            blocks.append(('p', ' '.join(current)))
            current = []
        slug, label, skip_count = sections[page_number]
        blocks.append(('h2', slug, label))
    else:
        skip_count = 0
    lines = [line for line in pages[page_number - 1].splitlines() if line.strip()]
    lines = [line for line in lines if not re.fullmatch(r'\d+', line.strip())]
    lines = lines[skip_count:]
    for line in lines:
        indent = len(line) - len(line.lstrip())
        content = re.sub(r'\s+', ' ', line.strip())
        if indent >= 6 and current:
            blocks.append(('p', ' '.join(current)))
            current = []
        current.append(content)
if current:
    blocks.append(('p', ' '.join(current)))

# The last introductory paragraph invites the reader to buy into the book.
# The preceding scope paragraph is part of the author's substantive introduction.
blocks = [block for block in blocks if not (block[0] == 'p' and block[1].startswith('As we embark on this intellectual voyage, we invite you'))]

# Page 35 has two consecutive, near-identical one-sentence claims about
# agriculture and animal breeding. Preserve the fuller second sentence once.
blocks = [block for block in blocks if not (block[0] == 'p' and block[1].startswith("Darwin's ideas have profoundly impacted agricultural practices and"))]

title = 'Charles Darwin A Revolutionary Force in Science and Society'
body = [f'<h1 id="book-title">{escape(title)}</h1>', '<p class="book-byline">AI Agent Ava DuRhodes</p>']
for block in blocks:
    if block[0] == 'h2':
        body.append(f'<h2 id="{block[1]}">{escape(block[2])}</h2>')
    else:
        body.append(f'<p>{escape(block[1])}</p>')
html = ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8"/><meta name="viewport" '
        'content="width=device-width,initial-scale=1"/><title>' + escape(title) + '</title></head><body>'
        '<article data-reader-content>' + '\n'.join(body) + '</article></body></html>\n')
destination = root / 'book/en/full_content.html'
destination.write_text(html)
(root / 'qa').mkdir(exist_ok=True)
(root / 'qa/source-selection.json').write_text(json.dumps({
    'source': 'income/Charles_Darwin__A_Revolutionary_Force_in_Science_and_Society/content.pdf',
    'retainedPdfPages': selected,
    'excludedPdfPages': list(range(1, 8)) + list(range(42, 48)),
    'partialPdfPage': 41,
    'page41Reason': 'Continuation of the conclusion from PDF page 40; no annex text on this page',
    'furtherRemoval': 'Final introductory invitation paragraph on PDF page 10 and near-duplicate agriculture paragraph on PDF page 35',
    'sections': [{'id': value[0], 'title': value[1], 'page': page} for page, value in sections.items()],
    'readerWords': len(' '.join(block[1] for block in blocks if block[0] == 'p').split()),
    'sourceSha256': sha256(pdf.read_bytes()).hexdigest(),
}, indent=2) + '\n')
print(destination, 'paragraphs',sum(b[0]=='p' for b in blocks),'words',len(' '.join(b[1] for b in blocks if b[0]=='p').split()))
